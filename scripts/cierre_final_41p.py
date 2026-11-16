"""Análisis final con las 41 personas (16-11-2026).

Objetivo: obtener una respuesta concluyente (positiva, nula o inconclusa, según reglas fijadas
antes de correr) a la hipótesis, aumentando la potencia de 8 a 41 personas.

- Validación cruzada agrupada por persona: 8 folds sobre las 41 personas del análisis principal.
- Configuración congelada del cierre V3 (elegida solo con train): HGB con 7 hojas en atención y
  15 en activación; GRU fija. Sin búsqueda de ningún tipo.
- Etiquetas: las mismas de V3 (atención: Modelo Profesor PCA congelado; activación: GSR V2).
- Contrastes fijados: un principal por tarea (HGB hasta 32 − HGB sin historial) y tres secundarios.
- Inferencia: diferencia de AUC por persona (n = 41), IC 95 % bootstrap, prueba de permutación de
  signos (200 000), Holm sobre los dos principales. Equivalencia con margen ±0,02 AUC (IC 90 %).
- Reglas de decisión (se aplican tal cual, una sola vez):
    respaldo:            p Holm < 0,05 e IC 95 % inferior > 0
    efecto relevante:    además, IC 95 % inferior > 0,02
    nulo concluyente:    IC 90 % completo dentro de (−0,02; +0,02)
    inferior concluyente: IC 95 % superior < 0
    en otro caso:        inconcluso
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import roc_auc_score, balanced_accuracy_score
from threadpoolctl import threadpool_limits
from atencion_binaria import ROOT, digest, write
import cierre_experimental_v3 as V3

OUT = ROOT / 'resultados/cierre_final_41p_16-11-2026'
LEAVES = {'atencion': 7, 'activacion': 15}  # congeladas en resultados/cierre_v3_16-11-2026/congelacion_*.json
N_FOLDS = 8
SEED = 20261116
MARGIN = .02
PRIMARY = {'atencion': ('hgb_c32', 'hgb_c1'), 'activacion': ('hgb_c32', 'hgb_c1')}
SECONDARY = [('hgb_c5', 'hgb_c1'), ('gru_c32', 'gru_c1'), ('gru_c32', 'hgb_c32')]


def plan():
    return json.loads((OUT / 'protocolo.json').read_text())


def inputs():
    v3 = ROOT / 'resultados/cierre_v3_16-11-2026'
    paths = [Path(__file__), ROOT / 'scripts/cierre_experimental_v3.py', v3 / 'congelacion_atencion.json',
             v3 / 'congelacion_activacion.json', V3.SOURCE, V3.PARTS, V3.LABELS_ACT, V3.TEACHER, *V3.SPATIAL]
    return {str(p.relative_to(ROOT)): digest(p) for p in paths}


def folds(people):
    rng = np.random.default_rng(SEED)
    order = rng.permutation(sorted(people))
    return [sorted(order[i::N_FOLDS].tolist()) for i in range(N_FOLDS)]


def prepare():
    OUT.mkdir(exist_ok=False)
    v3 = ROOT / 'resultados/cierre_v3_16-11-2026'
    for t in LEAVES:
        assert json.loads((v3 / f'congelacion_{t}.json').read_text())['leaves'] == LEAVES[t]
    people = sorted(pd.read_csv(V3.PARTS).query("split in ['train','validation','test']").participant)
    assert len(people) == 41
    write(OUT / 'protocolo.json', dict(
        created_utc=pd.Timestamp.now(tz='UTC').isoformat(),
        approval='Mario pide resultados concluyentes, 16-11-2026. Análisis registrado antes de correr; se ejecuta una vez.',
        inputs=inputs(), leaves=LEAVES, gru=V3.GRU, hgb=V3.HGB, folds=folds(people), n_folds=N_FOLDS, seed=SEED,
        primary=PRIMARY, secondary=SECONDARY, margin=MARGIN,
        inference='Diferencia de AUC por persona (41). IC 95 % y 90 % bootstrap por persona (20000, semilla 20261029). '
                  'Permutación de signos bilateral (200000, semilla 20261116). Holm sobre los dos principales; '
                  'secundarios descriptivos con p sin ajustar.',
        decision=dict(respaldo='p Holm < 0,05 e IC95 inferior > 0', relevante='además IC95 inferior > 0,02',
                      nulo='IC90 dentro de (−0,02; +0,02)', inferior='IC95 superior < 0', resto='inconcluso'),
        limits='Las 16 personas de validación y test ya se consultaron; la configuración se eligió solo con train y no '
               'se cambia. Etiquetas offline. Variables transductivas por persona (ver protocolo V3).'))
    print('Protocolo registrado', OUT / 'protocolo.json')


def run(task):
    p = plan()
    for path, h in p['inputs'].items():
        assert digest(ROOT / path) == h, path
    dest = OUT / f'predicciones_{task}.csv.gz'
    assert not dest.exists()
    torch.set_num_threads(3)
    data = V3.load_data()
    T = V3.Task(data, task)
    leaves = p['leaves'][task]
    preds = []
    for k, test_people in enumerate(p['folds']):
        fit = np.flatnonzero(~T.lab.participant.isin(test_people).to_numpy())
        ev = np.flatnonzero(T.lab.participant.isin(test_people).to_numpy())
        assert set(T.lab.participant.iloc[fit]).isdisjoint(test_people)
        prep = V3.preprocessor().fit(T.lab.iloc[fit][T.cols])
        Za = prep.transform(T.all[T.cols]).astype('float32')
        Zl = prep.transform(T.lab[T.cols]).astype('float32')
        y, w = T.lab.y.to_numpy()[fit], V3.weights(T.lab.iloc[fit])
        out = {}
        for name, kind in [('hgb_c1', 1), ('hgb_c5', 5), ('hgb_c32', 32)]:
            m = V3.fit_hgb(V3.hgb_matrix(T, Za, Zl, fit, kind), y, w, leaves)
            out[name] = m.predict_proba(V3.hgb_matrix(T, Za, Zl, ev, kind))[:, 1]
        for c in [1, 32]:
            xf, lf = V3.sequences(T, Za, fit, c)
            xe, le = V3.sequences(T, Za, ev, c)
            out[f'gru_c{c}'] = np.mean([V3.predict_gru(V3.fit_gru(xf, lf, y, w, s), xe, le) for s in V3.GRU['seeds']], axis=0)
        base = T.lab.iloc[ev][['source_row', 'participant', 'split', 'y']]
        preds += [base.assign(prob=v, strategy=n, fold=k) for n, v in out.items()]
        pd.concat(preds).to_csv(OUT / f'parcial_{task}.csv.gz', index=False)
        print(task, 'fold', k, flush=True)
    pd.concat(preds).to_csv(dest, index=False)
    (OUT / f'parcial_{task}.csv.gz').unlink()


def ci(v, levels=(.025, .975)):
    v = np.asarray(v)
    b = v[np.random.default_rng(20261029).integers(0, len(v), (20000, len(v)))].mean(axis=1)
    return [float(x) for x in np.quantile(b, levels)]


def sign_flip(d, n=200000):
    d = np.asarray(d)
    signs = np.random.default_rng(SEED).choice([-1, 1], size=(n, len(d)))
    null = np.abs((signs * d).mean(axis=1))
    return float((1 + (null >= abs(d.mean()) - 1e-15).sum()) / (n + 1))


def decide(mean, lo95, hi95, lo90, hi90, p_holm):
    if p_holm is not None and p_holm < .05 and lo95 > 0:
        return 'efecto relevante' if lo95 > MARGIN else 'respaldo'
    if hi95 < 0:
        return 'inferior'
    if -MARGIN < lo90 and hi90 < MARGIN:
        return 'nulo concluyente'
    return 'inconcluso'


def report():
    rows, people = [], []
    for task in LEAVES:
        pred = pd.read_csv(OUT / f'predicciones_{task}.csv.gz')
        for (strat, person), g in pred.groupby(['strategy', 'participant']):
            people.append(dict(task=task, strategy=strat, participant=person, split=g.split.iloc[0], windows=len(g),
                               auc=roc_auc_score(g.y, g.prob), ba=balanced_accuracy_score(g.y, g.prob >= .5)))
    people = pd.DataFrame(people)
    people.to_csv(OUT / 'metricas_personas.csv', index=False)
    summ = []
    for (task, strat), g in people.groupby(['task', 'strategy']):
        lo, hi = ci(g.auc)
        summ.append(dict(task=task, strategy=strat, people=len(g), auc=g.auc.mean(), low=lo, high=hi, ba=g.ba.mean()))
    pd.DataFrame(summ).to_csv(OUT / 'metricas.csv', index=False)
    for task in LEAVES:
        wide = people[people.task.eq(task)].pivot(index='participant', columns='strategy', values='auc')
        for role, (a, b) in [('principal', PRIMARY[task])] + [('secundario', s) for s in SECONDARY]:
            d = (wide[a] - wide[b]).to_numpy()
            lo95, hi95 = ci(d)
            lo90, hi90 = ci(d, (.05, .95))
            rows.append(dict(task=task, role=role, contrast=f'{a} − {b}', delta=float(d.mean()), low95=lo95, high95=hi95,
                             low90=lo90, high90=hi90, p=sign_flip(d), improved=int((d > 0).sum()), people=len(d)))
    res = pd.DataFrame(rows)
    prim = res.role.eq('principal')
    ps = res.loc[prim, 'p'].sort_values()
    holm = {}
    running = 0
    for i, (ix, p) in enumerate(ps.items()):
        running = max(running, min(1, p * (len(ps) - i)))
        holm[ix] = running
    res['p_holm'] = res.index.map(holm)
    res['decision'] = [decide(r.delta, r.low95, r.high95, r.low90, r.high90, r.p_holm if r.role == 'principal' else
                              (r.p if r.p < .05 else 1)) for r in res.itertuples()]
    res.to_csv(OUT / 'contrastes.csv', index=False)
    print(pd.DataFrame(summ).to_string(index=False))
    print(res.to_string(index=False))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['prepare', 'run', 'report'])
    ap.add_argument('--task', choices=list(LEAVES))
    a = ap.parse_args()
    with threadpool_limits(limits=3):
        if a.phase == 'run':
            run(a.task)
        else:
            globals()[a.phase]()
