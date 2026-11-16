"""Enmienda a la ampliación (16-11-2026), registrada ANTES de ver resultados de E1.

La auditoría de código mostró que con LAG=5 la ventana t-5 (2 s, paso 1 s) aún comparte 1 s de señal
con el soporte de 6 s de la etiqueta de activación. E1 principal pasa a LAG=6 (historial t-31..t-6, sin
solapamiento). LAG=5 queda como secundario. Mismos folds, configuración, placebo y reglas (Holm sobre
2 tareas; respaldo si p Holm < 0,05 e IC95 inferior > 0).
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

A.LAG = 6
OUT = A.OUT / 'enmienda_e1_lag6'


def prepare():
    OUT.mkdir(exist_ok=False)
    paths = [Path(__file__), ROOT / 'scripts/ampliacion_41p.py', A.OUT / 'protocolo.json']
    write(OUT / 'protocolo.json', dict(
        created_utc=pd.Timestamp.now(tz='UTC').isoformat(), lag=6,
        inputs={str(p.relative_to(ROOT)): digest(p) for p in paths},
        reason='Auditoría: con LAG=5 hay 1 s de solapamiento con la etiqueta de activación (ventanas de 2 s, paso 1 s).',
        primary='E1 lag6 real − lag6 placebo, Holm sobre 2 tareas', secondary_from_original='E1 lag5',
        declared=['E2: rel_time se ancla en una primera ventana aislada seguida de 42-89 s sin ventanas; calib_30s equivale '
                  'a las primeras 5 ventanas (respaldo) y calib_1min a ~15 ventanas.',
                  'E2 es transductivo: con M >= 2 min el contexto puede incluir la ventana evaluada y posteriores; '
                  'calib_sesion usa toda la sesión (offline, no causal). Solo variables, nunca etiquetas.',
                  'E5 permuta filas entre personas del fold (no dentro de cada persona) y los bloques de banda no incluyen '
                  'sus indicadores de faltantes; es descriptivo.',
                  'E3: la arquitectura intermedia es más profunda que la temprana; compara tipo de fusión y capacidad.']))
    print('Enmienda registrada')


def run(task):
    p = json.loads((OUT / 'protocolo.json').read_text())
    for path, h in p['inputs'].items():
        assert digest(ROOT / path) == h, path
    dest = OUT / f'predicciones_{task}.csv.gz'
    assert not dest.exists()
    T = V3.Task(V3.load_data(), task)
    real, plac = A.lag_index(T), A.lag_index(T, placebo=True, seed=A.PLACEBO_SEED)
    leaves = F.LEAVES[task]
    preds = []
    for k, test_people in enumerate(F.plan()['folds']):
        fit = np.flatnonzero(~T.lab.participant.isin(test_people).to_numpy())
        ev = np.flatnonzero(T.lab.participant.isin(test_people).to_numpy())
        prep = V3.preprocessor().fit(T.lab.iloc[fit][T.cols])
        Za = prep.transform(T.all[T.cols]).astype('float32')
        Zl = prep.transform(T.lab[T.cols]).astype('float32')
        y, w = T.lab.y.to_numpy()[fit], V3.weights(T.lab.iloc[fit])
        base = T.lab.iloc[ev][['source_row', 'participant', 'y']]
        for name, lag in [('lag6_real', real), ('lag6_placebo', plac)]:
            m = V3.fit_hgb(A.lag_matrix(T, Za, Zl, fit, lag), y, w, leaves)
            preds.append(base.assign(prob=m.predict_proba(A.lag_matrix(T, Za, Zl, ev, lag))[:, 1], strategy=name, fold=k))
        print(task, 'fold', k, flush=True)
    pd.concat(preds).to_csv(dest, index=False)
    pos = T.lab_pos
    write(OUT / f'cobertura_{task}.json', dict(rows_with_lag=float(np.mean(real[1][pos] > 0)), mean_lag=float(real[1][pos].mean())))


def report():
    rows = []
    for task in F.LEAVES:
        main = pd.read_csv(F.OUT / f'predicciones_{task}.csv.gz')
        new = pd.read_csv(OUT / f'predicciones_{task}.csv.gz')
        w = A.pp(pd.concat([main[main.strategy.eq('hgb_c1')], new]))
        rows.append(dict(task=task, contrast='lag6_real − lag6_placebo', **A.con(w, 'lag6_real', 'lag6_placebo')))
        rows.append(dict(task=task, contrast='lag6_real − hgb_c1', **A.con(w, 'lag6_real', 'hgb_c1')))
    res = pd.DataFrame(rows)
    prim = res.contrast.eq('lag6_real − lag6_placebo')
    ps = res.loc[prim, 'p'].sort_values()
    run_, holm = 0, {}
    for i, (ix, p) in enumerate(ps.items()):
        run_ = max(run_, min(1, p * (len(ps) - i)))
        holm[ix] = run_
    res['p_holm'] = res.index.map(holm)
    res.to_csv(OUT / 'contrastes.csv', index=False)
    print(res.round(4).to_string(index=False))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['prepare', 'run', 'report'])
    ap.add_argument('--task', choices=list(F.LEAVES))
    a = ap.parse_args()
    with threadpool_limits(limits=3):
        globals()[a.phase](a.task) if a.phase == 'run' else globals()[a.phase]()
