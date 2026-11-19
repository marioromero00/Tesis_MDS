"""Análisis explicativo POST HOC (18-11-2026), registrado antes de correrlo.

Motivo (observado tras E2): la calibración personal no reproduce la mejora del historial en atención,
pero el placebo sí. El placebo conserva el largo del historial real, que codifica el tiempo transcurrido
dentro del estímulo; la prevalencia de la etiqueta de atención varía con ese tiempo (0,37 a los 2-4 s,
0,62 a los 12 s). Hipótesis explicativa: la mejora del historial en atención se debe a la posición
dentro del estímulo, no al contenido de las ventanas previas.

Modelos (mismos folds y configuración congelada del análisis final):
  pos_c1     : ventana actual + segundos transcurridos en el estímulo (min(largo del segmento previo, 32))
  hgb_c32+pos: historial hasta 32 + la misma variable de posición
Contrastes: pos_c1 − hgb_c1 (¿la posición sola reproduce la mejora?), hgb_c32 − pos_c1 (¿queda algo del
historial tras controlar posición?), hgb_c32pos − pos_c1. Ambas tareas. Es post hoc: se reporta como tal.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits
from atencion_binaria import ROOT, digest, write
import cierre_experimental_v3 as V3
import cierre_final_41p as F
import ampliacion_41p as A

OUT = ROOT / 'resultados/explicativo_posicion_41p_18-11-2026'


def prepare():
    OUT.mkdir(exist_ok=False)
    paths = [Path(__file__), ROOT / 'scripts/ampliacion_41p.py', ROOT / 'scripts/cierre_final_41p.py',
             F.OUT / 'predicciones_atencion.csv.gz', F.OUT / 'predicciones_activacion.csv.gz']
    write(OUT / 'protocolo.json', dict(created_utc=pd.Timestamp.now(tz='UTC').isoformat(), post_hoc=True,
                                      inputs={str(p.relative_to(ROOT)): digest(p) for p in paths},
                                      leaves=F.LEAVES, folds=F.plan()['folds'],
                                      contrasts=['pos_c1 − hgb_c1', 'hgb_c32 − pos_c1', 'hgb_c32pos − pos_c1']))
    print('Registrado')


def run(task):
    p = json.loads((OUT / 'protocolo.json').read_text())
    for path, h in p['inputs'].items():
        assert digest(ROOT / path) == h, path
    T = V3.Task(V3.load_data(), task)
    pos_all = np.minimum(T.hist[32][1], 32).astype('float32')
    preds = []
    for k, test_people in enumerate(p['folds']):
        fit = np.flatnonzero(~T.lab.participant.isin(test_people).to_numpy())
        ev = np.flatnonzero(T.lab.participant.isin(test_people).to_numpy())
        prep = V3.preprocessor().fit(T.lab.iloc[fit][T.cols])
        Za = prep.transform(T.all[T.cols]).astype('float32')
        Zl = prep.transform(T.lab[T.cols]).astype('float32')
        y, w = T.lab.y.to_numpy()[fit], V3.weights(T.lab.iloc[fit])
        base = T.lab.iloc[ev][['source_row', 'participant', 'y']]
        for name, kind in [('pos_c1', 1), ('hgb_c32pos', 32)]:
            Xf = np.column_stack([V3.hgb_matrix(T, Za, Zl, fit, kind), pos_all[T.lab_pos[fit]]])
            Xe = np.column_stack([V3.hgb_matrix(T, Za, Zl, ev, kind), pos_all[T.lab_pos[ev]]])
            m = V3.fit_hgb(Xf, y, w, p['leaves'][task])
            preds.append(base.assign(prob=m.predict_proba(Xe)[:, 1], strategy=name, fold=k))
        print(task, 'fold', k, flush=True)
    pd.concat(preds).to_csv(OUT / f'predicciones_{task}.csv.gz', index=False)


def report():
    rows = []
    for task in F.LEAVES:
        main = pd.read_csv(F.OUT / f'predicciones_{task}.csv.gz')
        new = pd.read_csv(OUT / f'predicciones_{task}.csv.gz')
        w = A.pp(pd.concat([main[main.strategy.isin(['hgb_c1', 'hgb_c32'])], new]))
        for a, b in [('pos_c1', 'hgb_c1'), ('hgb_c32', 'pos_c1'), ('hgb_c32pos', 'pos_c1'), ('hgb_c32', 'hgb_c1')]:
            rows.append(dict(task=task, contrast=f'{a} − {b}', **A.con(w, a, b)))
        for s in ['hgb_c1', 'pos_c1', 'hgb_c32', 'hgb_c32pos']:
            rows.append(dict(task=task, contrast=f'AUC {s}', delta=w[s].mean()))
    r = pd.DataFrame(rows)
    r.to_csv(OUT / 'contrastes.csv', index=False)
    print(r.round(4).to_string(index=False))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['prepare', 'run', 'report'])
    ap.add_argument('--task', choices=list(F.LEAVES))
    a = ap.parse_args()
    with threadpool_limits(limits=3):
        globals()[a.phase](a.task) if a.phase == 'run' else globals()[a.phase]()
