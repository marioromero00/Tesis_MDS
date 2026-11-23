"""Reapertura, fase 3 (22-11-2026): separar el historial de la posición dentro del estímulo.

Pedido por Mario tras ver las fases 1 y 2. Registrado antes de correr; se ejecuta una vez.

Motivo (resultados ya vistos, por eso es un análisis dirigido y no una confirmación independiente):
  - En activación, el historial mejora la predicción (P1 +0,036) pero el contraste a igual posición quedó
    inconcluso (+0,027 [−0,003; +0,059]) y una comprobación no registrada con una sola partición sugirió que,
    dentro de un mismo estímulo, la posición sola rinde tanto como el historial.
  - El explicativo del 18-11 (una partición) dio historial − posición +0,038 [+0,002; +0,074] en activación y
    −0,002 en atención.

Modelos nuevos, en las mismas 5 particiones de la fase 1 (semillas 1101-1105), misma configuración congelada:
  pos_c1  : ventana actual + segundos transcurridos en el estímulo (misma definición del 18-11)
  c32_pos : historial hasta 32 + la misma variable de posición
Se reutilizan hgb_c1 y hgb_c32 de la fase 1 (mismas particiones y filas).

Familia confirmatoria (4 pruebas, Holm): contraste c32_pos − pos_c1, es decir, qué agrega el contenido del
historial cuando el modelo ya conoce la posición.
  Q1 AUC por persona habitual (todas las comparaciones), en atención y activación.
  Q2 AUC por persona calculada solo entre ventanas del mismo estímulo, en atención y activación.
La AUC de cada persona se promedia sobre las 5 particiones antes de la inferencia.

Descriptivos: pos_c1 − hgb_c1 (qué aporta la posición sola), hgb_c32 − pos_c1, c32_pos − hgb_c32, los mismos
contrastes estratificados por estímulo, minuto de sesión y posición, y sensibilidad al quitar la persona más
influyente en las 4 pruebas confirmatorias.

Reglas de decisión (las del análisis final, margen 0,02):
  respaldo: p Holm < 0,05 e IC 95 % inferior > 0; efecto relevante: además IC 95 % inferior > 0,02;
  nulo concluyente: IC 90 % dentro de (−0,02; +0,02); inferior: IC 95 % superior < 0; resto: inconcluso.
Lectura fijada de antemano: si Q1 da respaldo, el historial aporta más allá de la posición; si da nulo
concluyente, la mejora del historial se explica por la posición; si queda inconcluso, se reporta así.
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
import reapertura_41p as R
import reapertura_fase2_41p as X

OUT = ROOT / 'resultados/reapertura_fase3_41p_22-11-2026'
MODELS = ['hgb_c1', 'hgb_c32', 'pos_c1', 'c32_pos']
DESCRIPTIVE = [('pos_c1', 'hgb_c1'), ('hgb_c32', 'pos_c1'), ('c32_pos', 'hgb_c32'), ('hgb_c32', 'hgb_c1')]


def plan():
    return json.loads((OUT / 'protocolo.json').read_text())


def prepare():
    OUT.mkdir(exist_ok=False)
    paths = [Path(__file__), ROOT / 'scripts/reapertura_41p.py', ROOT / 'scripts/reapertura_fase2_41p.py',
             R.OUT / 'protocolo.json'] + [R.OUT / f'rep_{t}_{s}.csv.gz' for t in F.LEAVES for s in R.REP_SEEDS]
    write(OUT / 'protocolo.json', dict(
        created_utc=pd.Timestamp.now(tz='UTC').isoformat(),
        approval='Mario pide el experimento para separar historial y posición, 22-11-2026. Registrado antes de correr.',
        directed=True, inputs={str(p.relative_to(ROOT)): digest(p) for p in paths},
        leaves=F.LEAVES, folds_rep=R.plan()['folds_rep'], margin=F.MARGIN,
        confirmatory=dict(contrast='c32_pos − pos_c1', tests=['Q1 AUC habitual', 'Q2 AUC dentro del mismo estímulo'],
                          tasks=list(F.LEAVES), holm='sobre las 4 pruebas',
                          unit='AUC por persona promediada sobre las 5 particiones; diferencia pareada por persona'),
        descriptive=[f'{a} − {b}' for a, b in DESCRIPTIVE] + ['estratos: estímulo, minuto, posición',
                                                              'sensibilidad sin la persona más influyente'],
        decision=dict(respaldo='p Holm < 0,05 e IC95 inferior > 0', relevante='además IC95 inferior > 0,02',
                      nulo='IC90 dentro de (−0,02; +0,02)', inferior='IC95 superior < 0', resto='inconcluso'),
        limits='Las 41 personas y resultados previos ya se vieron; análisis dirigido. La posición es '
               'min(largo del segmento previo, 32) s, como el 18-11. La posición como variable permite al modelo '
               'usar su efecto principal y sus interacciones con la fisiología.'))
    print('Registrado', OUT / 'protocolo.json')


def run(task, seed):
    p = plan()
    for path, h in p['inputs'].items():
        assert digest(ROOT / path) == h, path
    dest = OUT / f'pos_{task}_{seed}.csv.gz'
    assert not dest.exists()
    T = V3.Task(V3.load_data(), task)
    pos = R.stimulus_position(T)
    preds = []
    for k, test_people in enumerate(p['folds_rep'][str(seed)]):
        fit, ev, Za, Zl = R.fold_setup(T, test_people)
        y, w = T.lab.y.to_numpy()[fit], V3.weights(T.lab.iloc[fit])
        base = T.lab.iloc[ev][['source_row', 'participant', 'y']]
        for name, kind in [('pos_c1', 1), ('c32_pos', 32)]:
            Xf, Xe = (np.column_stack([V3.hgb_matrix(T, Za, Zl, r, kind), pos[T.lab_pos[r]]]) for r in (fit, ev))
            m = V3.fit_hgb(Xf, y, w, p['leaves'][task])
            preds.append(base.assign(prob=m.predict_proba(Xe)[:, 1], strategy=name, fold=k, seed=seed))
        print(task, 'pos', seed, 'fold', k, flush=True)
    pd.concat(preds).to_csv(dest, index=False)


def without_most_influential(wide, a, b):
    d = (wide[a] - wide[b]).dropna()
    i = (d - d.mean()).abs().idxmax()
    r = d.drop(i).to_numpy()
    lo, hi = F.ci(r)
    return dict(median=float(d.median()), influential=i, influential_delta=float(d[i]), delta_without=float(r.mean()),
                low95_without=lo, high95_without=hi, p_without=F.sign_flip(r))


def report():
    conf, desc = [], []
    for task in F.LEAVES:
        T = V3.Task(V3.load_data(), task)
        st = X.strata_table(T)
        old = pd.concat([pd.read_csv(R.OUT / f'rep_{task}_{s}.csv.gz') for s in R.REP_SEEDS])
        new = pd.concat([pd.read_csv(OUT / f'pos_{task}_{s}.csv.gz') for s in R.REP_SEEDS])
        pred = pd.concat([old[old.strategy.isin(['hgb_c1', 'hgb_c32'])], new]).join(st, on='source_row')
        key = pred.groupby(['seed', 'strategy']).source_row.apply(lambda s: tuple(sorted(s)))
        assert key.nunique() == 1 and pred.groupby(['seed', 'strategy']).source_row.apply(lambda s: s.is_unique).all()
        assert pred.groupby(['seed', 'source_row']).y.nunique().eq(1).all()
        wides = {'todas': R.person_auc(pred, ('seed', 'strategy')).groupby(['participant', 'strategy']).auc.mean().unstack()}
        for col in X.STRATA:
            v = pred.groupby(['seed', 'strategy', 'participant']).apply(lambda g: R.stratified_auc(g, col)).rename('auc').reset_index()
            wides[col] = v.groupby(['participant', 'strategy']).auc.mean().unstack()
        assert len(wides['todas']) == 41
        for name, scope in [('Q1', 'todas'), ('Q2', 'estimulo')]:
            conf.append(dict(task=task, test=name, scope=scope, contrast='c32_pos − pos_c1', **R.contrast(wides[scope], 'c32_pos', 'pos_c1'),
                             **without_most_influential(wides[scope], 'c32_pos', 'pos_c1')))
        for scope, w in wides.items():
            for a, b in DESCRIPTIVE + ([('c32_pos', 'pos_c1')] if scope in ('bloque60', 'posicion') else []):
                desc.append(dict(task=task, scope=scope, item=f'{a} − {b}', **R.contrast(w, a, b)))
            for s in MODELS:
                v = w[s].dropna()
                lo, hi = F.ci(v)
                desc.append(dict(task=task, scope=scope, item=f'AUC {s}', delta=float(v.mean()), low95=lo, high95=hi, people=len(v)))
    conf = pd.DataFrame(conf)
    conf['p_holm'] = R.holm(conf.p)
    conf['decision'] = [F.decide(r.delta, r.low95, r.high95, r.low90, r.high90, r.p_holm) for r in conf.itertuples()]
    conf.to_csv(OUT / 'confirmatorio.csv', index=False)
    pd.DataFrame(desc).to_csv(OUT / 'descriptivos.csv', index=False)
    pd.set_option('display.width', 280)
    print(conf.round(4).to_string(index=False))
    print(pd.DataFrame(desc).round(4).to_string(index=False))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['prepare', 'run', 'report'])
    ap.add_argument('--task', choices=list(F.LEAVES))
    ap.add_argument('--seed', type=int)
    a = ap.parse_args()
    with threadpool_limits(limits=1):
        run(a.task, a.seed) if a.phase == 'run' else globals()[a.phase]()
