"""Pruebas de robustez del análisis final con 41 personas (16-11-2026).

No buscan un resultado: ponen a prueba el resultado principal ya obtenido. Se registran antes de
correr y se ejecutan una vez. Misma configuración congelada (HGB 7/15 hojas), sin búsqueda.

R1 Placebo temporal (ambas tareas): el historial se reemplaza por ventanas de la misma persona
   tomadas al azar de OTROS segmentos/estímulos, con el mismo largo. Misma dimensión que el
   historial real. Contraste: HGB hasta 32 real − HGB hasta 32 placebo. Si es > 0, la mejora viene
   de la información temporal y no solo de tener más variables.
R2 Sin fuga de etiquetas (atención): el Modelo Profesor PCA se reajusta en cada fold sin las
   personas evaluadas. Contraste: HGB hasta 32 − HGB sin historial.
R3 Estabilidad de la partición (ambas tareas): el contraste principal se repite con 3 particiones
   en 8 folds generadas con otras semillas.

Reglas (fijadas de antemano):
  R1: placebo superado si p Holm (sobre las 2 tareas) < 0,05 e IC 95 % inferior > 0.
  R2: se mantiene si IC 95 % inferior > 0.
  R3: estable si las 3 particiones dan IC 95 % inferior > 0 (atención) / se reporta igual en activación.
  Atención se declara "robusta" si cumple R1, R2 y R3.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from threadpoolctl import threadpool_limits
from atencion_binaria import ROOT, digest, write
from reconstruir_profesor_atencion_binaria import components, fit_teacher
import cierre_experimental_v3 as V3
import cierre_final_41p as F

OUT = ROOT / 'resultados/cierre_robustez_41p_16-11-2026'
SEEDS_R3 = [101, 202, 303]
PLACEBO_SEED = 20261117


def plan():
    return json.loads((OUT / 'protocolo.json').read_text())


def inputs():
    paths = [Path(__file__), ROOT / 'scripts/cierre_final_41p.py', ROOT / 'scripts/cierre_experimental_v3.py',
             ROOT / 'scripts/reconstruir_profesor_atencion_binaria.py', F.OUT / 'protocolo.json',
             F.OUT / 'predicciones_atencion.csv.gz', F.OUT / 'predicciones_activacion.csv.gz']
    return {str(p.relative_to(ROOT)): digest(p) for p in paths}


def prepare():
    OUT.mkdir(exist_ok=False)
    people = sorted(pd.read_csv(V3.PARTS).query("split in ['train','validation','test']").participant)
    alt = {}
    for s in SEEDS_R3:
        order = np.random.default_rng(s).permutation(people)
        alt[str(s)] = [sorted(order[i::F.N_FOLDS].tolist()) for i in range(F.N_FOLDS)]
    write(OUT / 'protocolo.json', dict(
        created_utc=pd.Timestamp.now(tz='UTC').isoformat(),
        approval='Mario pide resultados más concluyentes, 16-11-2026. Pruebas de robustez registradas antes de correr.',
        inputs=inputs(), leaves=F.LEAVES, folds_main=F.plan()['folds'], folds_r3=alt, placebo_seed=PLACEBO_SEED,
        rules=dict(R1='p Holm (2 tareas) < 0,05 e IC95 inferior > 0', R2='IC95 inferior > 0',
                   R3='las 3 particiones con IC95 inferior > 0', robusta='R1 y R2 y R3 en atención'),
        note='Las predicciones reales hasta 32 y sin historial se reutilizan del análisis final (mismos folds y '
             'configuración, verificado por hash); solo se entrenan los modelos nuevos.'))
    print('Protocolo registrado')


def placebo_hist(T, seed):
    """Historial placebo: mismo largo, ventanas de la misma persona en otros segmentos/estímulos."""
    ix, l = T.hist[32]
    rng = np.random.default_rng(seed)
    grp = T.all.groupby(['split', 'participant', 'recording', 'segment_id', 'stimulus'], sort=False).ngroup().to_numpy()
    person = T.all.participant.to_numpy()
    pools = {p: np.flatnonzero(person == p) for p in np.unique(person)}
    out = ix.copy()
    for r in range(len(ix)):
        n = l[r]
        if n <= 1:
            continue
        pool = pools[person[r]]
        pool = pool[grp[pool] != grp[r]]
        out[r, :n - 1] = rng.choice(pool, size=n - 1, replace=len(pool) < n - 1)
        assert out[r, n - 1] == r
    return out, l


def hgb_placebo(T, Z_all, Z_lab, rows, hist):
    ix, l = hist
    pos = T.lab_pos[rows]
    mean, sd = V3.summary_rep(Z_all, ix[pos], l[pos])
    return np.column_stack([Z_lab[rows], mean, sd]).astype('float32')


def fit_predict(T, folds, leaves, kinds, placebo=None):
    preds = []
    for k, test_people in enumerate(folds):
        fit = np.flatnonzero(~T.lab.participant.isin(test_people).to_numpy())
        ev = np.flatnonzero(T.lab.participant.isin(test_people).to_numpy())
        prep = V3.preprocessor().fit(T.lab.iloc[fit][T.cols])
        Za = prep.transform(T.all[T.cols]).astype('float32')
        Zl = prep.transform(T.lab[T.cols]).astype('float32')
        y, w = T.lab.y.to_numpy()[fit], V3.weights(T.lab.iloc[fit])
        base = T.lab.iloc[ev][['source_row', 'participant', 'y']]
        for name in kinds:
            if name == 'placebo_c32':
                Xf, Xe = hgb_placebo(T, Za, Zl, fit, placebo), hgb_placebo(T, Za, Zl, ev, placebo)
            else:
                kind = {'hgb_c1': 1, 'hgb_c32': 32}[name]
                Xf, Xe = V3.hgb_matrix(T, Za, Zl, fit, kind), V3.hgb_matrix(T, Za, Zl, ev, kind)
            m = V3.fit_hgb(Xf, y, w, leaves)
            preds.append(base.assign(prob=m.predict_proba(Xe)[:, 1], strategy=name, fold=k))
    return pd.concat(preds)


def run(task):
    p = plan()
    for path, h in p['inputs'].items():
        assert digest(ROOT / path) == h, path
    assert not (OUT / f'r1_{task}.csv.gz').exists()
    data = V3.load_data()
    T = V3.Task(data, task)
    leaves = p['leaves'][task]
    # R1 placebo
    r1 = fit_predict(T, p['folds_main'], leaves, ['placebo_c32'], placebo=placebo_hist(T, p['placebo_seed']))
    r1.to_csv(OUT / f'r1_{task}.csv.gz', index=False)
    print(task, 'R1 listo', flush=True)
    # R3 estabilidad
    r3 = []
    for s, fl in p['folds_r3'].items():
        r3.append(fit_predict(T, fl, leaves, ['hgb_c1', 'hgb_c32']).assign(seed=int(s)))
        print(task, 'R3 semilla', s, flush=True)
    pd.concat(r3).to_csv(OUT / f'r3_{task}.csv.gz', index=False)
    # R2 sin fuga (solo atención)
    if task == 'atencion':
        z, _ = components(data)
        r2 = []
        for k, test_people in enumerate(p['folds_main']):
            fit_people = sorted(set(data.participant) - set(test_people))
            _, labels, _, _ = fit_teacher(data, z, fit_people, 'pca')
            d2 = data.copy()
            d2['y_atencion'] = labels.astype('float').to_numpy()
            T2 = V3.Task(d2, task)
            r2.append(fit_predict(T2, [test_people], leaves, ['hgb_c1', 'hgb_c32']).assign(fold=k))
            print(task, 'R2 fold', k, flush=True)
        pd.concat(r2).to_csv(OUT / f'r2_{task}.csv.gz', index=False)


def per_person(pred, keys=()):
    rows = []
    for key, g in pred.groupby(list(keys) + ['strategy', 'participant']):
        rows.append(dict(zip(list(keys) + ['strategy', 'participant'], key if isinstance(key, tuple) else (key,)),
                         auc=roc_auc_score(g.y, g.prob)))
    return pd.DataFrame(rows)


def contrast(pp, a, b):
    w = pp.pivot(index='participant', columns='strategy', values='auc')
    d = (w[a] - w[b]).dropna().to_numpy()
    lo, hi = F.ci(d)
    return dict(delta=float(d.mean()), low95=lo, high95=hi, p=F.sign_flip(d), improved=int((d > 0).sum()), people=len(d))


def report():
    rows = []
    for task in F.LEAVES:
        main = pd.read_csv(F.OUT / f'predicciones_{task}.csv.gz')
        main = main[main.strategy.isin(['hgb_c1', 'hgb_c32'])]
        r1 = pd.read_csv(OUT / f'r1_{task}.csv.gz')
        pp = per_person(pd.concat([main, r1]))
        rows.append(dict(task=task, prueba='R1 placebo', contraste='hgb_c32 real − hgb_c32 placebo', **contrast(pp, 'hgb_c32', 'placebo_c32')))
        rows.append(dict(task=task, prueba='R1 referencia', contraste='hgb_c32 placebo − hgb_c1', **contrast(pp, 'placebo_c32', 'hgb_c1')))
        r3 = pd.read_csv(OUT / f'r3_{task}.csv.gz')
        for s, g in r3.groupby('seed'):
            rows.append(dict(task=task, prueba=f'R3 partición {s}', contraste='hgb_c32 − hgb_c1', **contrast(per_person(g), 'hgb_c32', 'hgb_c1')))
        if task == 'atencion':
            r2 = pd.read_csv(OUT / f'r2_{task}.csv.gz')
            rows.append(dict(task=task, prueba='R2 sin fuga', contraste='hgb_c32 − hgb_c1', **contrast(per_person(r2), 'hgb_c32', 'hgb_c1')))
    res = pd.DataFrame(rows)
    r1 = res.prueba.eq('R1 placebo')
    ps = res.loc[r1, 'p'].sort_values()
    run_, holm = 0, {}
    for i, (ix, p) in enumerate(ps.items()):
        run_ = max(run_, min(1, p * (len(ps) - i)))
        holm[ix] = run_
    res['p_holm'] = res.index.map(holm)
    res.to_csv(OUT / 'resultados.csv', index=False)
    print(res.to_string(index=False))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['prepare', 'run', 'report'])
    ap.add_argument('--task', choices=list(F.LEAVES))
    a = ap.parse_args()
    with threadpool_limits(limits=3):
        if a.phase == 'run':
            run(a.task)
        else:
            globals()[a.phase]()
