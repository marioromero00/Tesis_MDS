"""Ampliación experimental sobre las 41 personas (16-11-2026).

Mismos 8 folds y configuración congelada del análisis final (HGB 7/15 hojas). Registrado antes de
correr y ejecutado una vez. Ninguna decisión se toma con los resultados.

E1 Temporalidad más allá de la etiqueta: historial que excluye las 5 ventanas más recientes (las que
   integra la etiqueta de activación de 6 s): ventanas t-31..t-5 del mismo segmento. Real vs placebo
   (mismo número de ventanas de la misma persona en otros segmentos). Ambas tareas.
E2 Calibración personal: el modelo recibe la ventana actual más la media/desviación de las ventanas de
   la misma persona en los primeros M de la sesión (sin etiquetas). M = 30 s, 1, 2, 5 min y sesión completa.
E3 Tipos de fusión con una misma familia (MLP, 3 semillas, sin búsqueda) sobre la representación hasta 32:
   temprana (un encoder), intermedia (un encoder por señal y capa común) y tardía (un MLP por señal,
   promedio de probabilidades).
E4 Fatiga/habituación (descriptivo): prevalencia de la etiqueta, probabilidad predicha y AUC por quintil
   del tiempo de sesión, con las predicciones fuera de fold del análisis final.
E5 Importancia por bloques (descriptivo): caída de AUC al permutar bloques (señal; ventana actual vs
   media vs desviación del historial; bandas EEG) en los modelos HGB hasta 32 de cada fold.
E6 Tipo de página (descriptivo): mejora del historial por categoría de estímulo.

Principales (Holm sobre 2 tareas): E1 lag real − lag placebo.
Secundarios con IC: E1 lag real − sin historial; E2 cada M − sin historial; E3 intermedia − temprana,
intermedia − tardía, tardía − temprana.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from torch import nn
from sklearn.metrics import roc_auc_score
from threadpoolctl import threadpool_limits
from atencion_binaria import ROOT, digest, write
import cierre_experimental_v3 as V3
import cierre_final_41p as F

OUT = ROOT / 'resultados/ampliacion_41p_16-11-2026'
LAG = 5
CALIB = {'calib_30s': 30, 'calib_1min': 60, 'calib_2min': 120, 'calib_5min': 300, 'calib_sesion': 1e9}
MLP = dict(hidden=64, enc=32, dropout=.3, epochs=15, batch=256, lr=1e-3, weight_decay=1e-2, seeds=[1, 2, 3])
PLACEBO_SEED = 20261118
PERM_REPEATS = 3
BANDS = ['delta', 'theta', 'alpha', 'beta', 'gamma']


def category(stim):
    s = pd.Series(stim).str.replace(r'\s*\(\d+\)$', '', regex=True)
    out = np.where(s.eq('Text'), 'texto',
          np.where(s.str.match(r'^(Meg|diario_financiero|temu|Despega|Nint)'), 'sitio web',
          np.where(s.str.startswith('diseño'), 'diseño',
          np.where(s.str.startswith('emotion'), 'imagen emotion',
          np.where(s.str.startswith('blur'), 'imagen blur',
          np.where(s.str.fullmatch(r'\d+'), 'numerado', 'instrucciones'))))))
    return out


def plan():
    return json.loads((OUT / 'protocolo.json').read_text())


def inputs():
    paths = [Path(__file__), ROOT / 'scripts/cierre_final_41p.py', ROOT / 'scripts/cierre_experimental_v3.py',
             F.OUT / 'protocolo.json', F.OUT / 'predicciones_atencion.csv.gz', F.OUT / 'predicciones_activacion.csv.gz']
    return {str(p.relative_to(ROOT)): digest(p) for p in paths}


def prepare():
    OUT.mkdir(exist_ok=False)
    write(OUT / 'protocolo.json', dict(
        created_utc=pd.Timestamp.now(tz='UTC').isoformat(),
        approval='Mario elige E1-E6, 16-11-2026. Registrado antes de correr.',
        inputs=inputs(), leaves=F.LEAVES, folds=F.plan()['folds'], lag=LAG, calib_seconds=CALIB, mlp=MLP,
        placebo_seed=PLACEBO_SEED, perm_repeats=PERM_REPEATS,
        primary='E1 lag real − lag placebo, ambas tareas, Holm; respaldo si p Holm < 0,05 e IC95 inferior > 0',
        secondary='E1 lag real − sin historial; E2 cada M − sin historial; E3 intermedia − temprana, intermedia − tardía, '
                  'tardía − temprana. IC 95 % y permutación de signos sin corregir; descriptivos.',
        descriptive='E4, E5, E6 sin pruebas de hipótesis.',
        note='Sin historial (hgb_c1) se reutiliza del análisis final (mismos folds, configuración e hiperparámetros).'))
    print('Protocolo registrado')


# ------------------------------------------------------------- representaciones
def rel_time(T):
    t = pd.to_datetime(T.all.window_start_utc)
    return (t - t.groupby(T.all.recording).transform('min')).dt.total_seconds().to_numpy()


def lag_index(T, placebo=False, seed=PLACEBO_SEED):
    ix, l = T.hist[32]
    n = np.maximum(l - LAG, 0)
    out = np.full_like(ix, -1)
    rng = np.random.default_rng(seed)
    grp = T.all.groupby(['split', 'participant', 'recording', 'segment_id', 'stimulus'], sort=False).ngroup().to_numpy()
    person = T.all.participant.to_numpy()
    pools = {p: np.flatnonzero(person == p) for p in np.unique(person)}
    for r in np.flatnonzero(n > 0):
        if placebo:
            pool = pools[person[r]]
            pool = pool[grp[pool] != grp[r]]
            out[r, :n[r]] = rng.choice(pool, size=n[r], replace=len(pool) < n[r])
        else:
            out[r, :n[r]] = ix[r, :n[r]]
    return out, n


def summary(Z, ix, n):
    mask = (ix >= 0)[:, :, None]
    x = np.where(mask, Z[np.maximum(ix, 0)], 0)
    k = np.maximum(n, 1)[:, None]
    mean = x.sum(axis=1) / k
    sd = np.sqrt(np.maximum((((x - mean[:, None, :]) ** 2) * mask).sum(axis=1) / k, 0))
    return mean, sd


def lag_matrix(T, Za, Zl, rows, lag):
    ix, n = lag
    pos = T.lab_pos[rows]
    mean, sd = summary(Za, ix[pos], n[pos])
    return np.column_stack([Zl[rows], mean, sd, n[pos][:, None] / (32 - LAG)]).astype('float32')


def calib_matrix(T, Za, Zl, rows, seconds, rt):
    person = T.all.participant.to_numpy()
    vec = {}
    for p in np.unique(T.lab.participant.iloc[rows]):
        idx = np.flatnonzero((person == p) & (rt <= seconds))
        if len(idx) < 5:
            own = np.flatnonzero(person == p)
            idx = own[np.argsort(rt[own])[:5]]
        vec[p] = np.concatenate([Za[idx].mean(axis=0), Za[idx].std(axis=0)])
    ctx = np.stack([vec[p] for p in T.lab.participant.iloc[rows]])
    return np.column_stack([Zl[rows], ctx]).astype('float32')


# ------------------------------------------------------------- MLP para fusión
class Early(nn.Module):
    def __init__(self, d):
        super().__init__()
        self.f = nn.Sequential(nn.Linear(d, MLP['hidden']), nn.ReLU(), nn.Dropout(MLP['dropout']), nn.Linear(MLP['hidden'], 1))

    def forward(self, x):
        return self.f(x).squeeze(-1)


class Intermediate(nn.Module):
    def __init__(self, blocks):
        super().__init__()
        self.blocks = [torch.as_tensor(b) for b in blocks]
        self.enc = nn.ModuleList([nn.Sequential(nn.Linear(len(b), MLP['enc']), nn.ReLU()) for b in blocks])
        self.head = nn.Sequential(nn.Dropout(MLP['dropout']), nn.Linear(MLP['enc'] * len(blocks), MLP['enc']), nn.ReLU(),
                                  nn.Linear(MLP['enc'], 1))

    def forward(self, x):
        return self.head(torch.cat([e(x[:, b]) for e, b in zip(self.enc, self.blocks)], dim=1)).squeeze(-1)


def train_mlp(make, X, y, w, seed):
    torch.manual_seed(seed)
    net = make()
    opt = torch.optim.AdamW(net.parameters(), lr=MLP['lr'], weight_decay=MLP['weight_decay'])
    X, Y, W = torch.from_numpy(X), torch.from_numpy(y.astype('float32')), torch.from_numpy(w.astype('float32'))
    loss = nn.BCEWithLogitsLoss(reduction='none')
    g = torch.Generator().manual_seed(seed)
    for _ in range(MLP['epochs']):
        net.train()
        for b in torch.randperm(len(X), generator=g).split(MLP['batch']):
            opt.zero_grad()
            (loss(net(X[b]), Y[b]) * W[b]).mean().backward()
            opt.step()
    net.eval()
    return net


@torch.no_grad()
def prob(net, X):
    return torch.sigmoid(net(torch.from_numpy(X))).numpy()


def blocks_c32(T, prep, task):
    """Columnas de cada señal dentro de [actual | media | desviación] (incluye indicadores)."""
    ind = prep.named_steps['imputer'].indicator_.features_
    n, width = len(T.cols), len(T.cols) + len(ind)
    out = {}
    for k, v in V3.GROUPS[task].items():
        own = [T.cols.index(c) for c in v]
        base = own + [n + j for j, f in enumerate(ind) if f in set(own)]
        out[k] = np.array([b + part * width for part in range(3) for b in base])
    return out, width


# ------------------------------------------------------------- ejecución
def run(task):
    p = plan()
    for path, h in p['inputs'].items():
        assert digest(ROOT / path) == h, path
    dest = OUT / f'predicciones_{task}.csv.gz'
    assert not dest.exists()
    torch.set_num_threads(3)
    T = V3.Task(V3.load_data(), task)
    rt = rel_time(T)
    lag_real, lag_plac = lag_index(T), lag_index(T, placebo=True, seed=p['placebo_seed'])
    leaves = p['leaves'][task]
    preds, imp = [], []
    for k, test_people in enumerate(p['folds']):
        fit = np.flatnonzero(~T.lab.participant.isin(test_people).to_numpy())
        ev = np.flatnonzero(T.lab.participant.isin(test_people).to_numpy())
        prep = V3.preprocessor().fit(T.lab.iloc[fit][T.cols])
        Za = prep.transform(T.all[T.cols]).astype('float32')
        Zl = prep.transform(T.lab[T.cols]).astype('float32')
        y, w = T.lab.y.to_numpy()[fit], V3.weights(T.lab.iloc[fit])
        base = T.lab.iloc[ev][['source_row', 'participant', 'y']]
        out = {}
        # E1
        for name, lag in [('lag_real', lag_real), ('lag_placebo', lag_plac)]:
            m = V3.fit_hgb(lag_matrix(T, Za, Zl, fit, lag), y, w, leaves)
            out[name] = m.predict_proba(lag_matrix(T, Za, Zl, ev, lag))[:, 1]
        # E2
        for name, sec in CALIB.items():
            m = V3.fit_hgb(calib_matrix(T, Za, Zl, fit, sec, rt), y, w, leaves)
            out[name] = m.predict_proba(calib_matrix(T, Za, Zl, ev, sec, rt))[:, 1]
        # E3 y E5 sobre la representación hasta 32
        Xf, Xe = V3.hgb_matrix(T, Za, Zl, fit, 32), V3.hgb_matrix(T, Za, Zl, ev, 32)
        blocks, width = blocks_c32(T, prep, task)
        out['mlp_temprana'] = np.mean([prob(train_mlp(lambda: Early(Xf.shape[1]), Xf, y, w, s), Xe) for s in MLP['seeds']], axis=0)
        out['mlp_intermedia'] = np.mean([prob(train_mlp(lambda: Intermediate(list(blocks.values())), Xf, y, w, s), Xe)
                                         for s in MLP['seeds']], axis=0)
        late = []
        for b in blocks.values():
            late.append(np.mean([prob(train_mlp(lambda b=b: Early(len(b)), Xf[:, b], y, w, s), Xe[:, b]) for s in MLP['seeds']], axis=0))
        out['mlp_tardia'] = np.mean(late, axis=0)
        m = V3.fit_hgb(Xf, y, w, leaves)
        ref = m.predict_proba(Xe)[:, 1]
        evf = T.lab.iloc[ev].reset_index(drop=True)
        base_auc = F_auc(evf, ref)
        groups = {f'señal {k}': v for k, v in blocks.items()}
        groups.update({'parte actual': np.arange(width), 'parte media historial': np.arange(width, 2 * width),
                       'parte desviación historial': np.arange(2 * width, 3 * width)})
        for band in BANDS:
            cols = [i for i, c in enumerate(T.cols) if band in c]
            if cols:
                groups[f'banda {band}'] = np.array([c + part * width for part in range(3) for c in cols])
        rng = np.random.default_rng(k)
        for gname, cols in groups.items():
            for r in range(PERM_REPEATS):
                Xp = Xe.copy()
                Xp[:, cols] = Xp[rng.permutation(len(Xp))][:, cols]
                imp.append(dict(fold=k, block=gname, repeat=r, drop=base_auc - F_auc(evf, m.predict_proba(Xp)[:, 1])))
        preds += [base.assign(prob=v, strategy=n, fold=k) for n, v in out.items()]
        print(task, 'fold', k, flush=True)
    pd.concat(preds).to_csv(dest, index=False)
    pd.DataFrame(imp).to_csv(OUT / f'importancia_{task}.csv', index=False)


def F_auc(f, p):
    p = np.asarray(p)
    return float(np.mean([roc_auc_score(f.y.iloc[ix], p[ix]) for ix in f.groupby('participant').indices.values()]))


# ------------------------------------------------------------- informe
def pp(pred):
    return pd.DataFrame([dict(strategy=s, participant=q, auc=roc_auc_score(g.y, g.prob))
                         for (s, q), g in pred.groupby(['strategy', 'participant'])]).pivot(index='participant', columns='strategy', values='auc')


def con(w, a, b):
    d = (w[a] - w[b]).dropna().to_numpy()
    lo, hi = F.ci(d)
    return dict(delta=float(d.mean()), low95=lo, high95=hi, p=F.sign_flip(d), improved=int((d > 0).sum()), people=len(d))


def report():
    rows, summ, e4, e6, imp_all = [], [], [], [], []
    data = V3.load_data()
    for task in F.LEAVES:
        main = pd.read_csv(F.OUT / f'predicciones_{task}.csv.gz')
        new = pd.read_csv(OUT / f'predicciones_{task}.csv.gz')
        w = pp(pd.concat([main[main.strategy.isin(['hgb_c1', 'hgb_c32'])], new]))
        for s in w.columns:
            lo, hi = F.ci(w[s])
            summ.append(dict(task=task, strategy=s, auc=w[s].mean(), low=lo, high=hi))
        spec = [('E1 principal', 'lag_real', 'lag_placebo'), ('E1', 'lag_real', 'hgb_c1')]
        spec += [('E2', c, 'hgb_c1') for c in CALIB] + [('E2 ref', 'hgb_c32', 'hgb_c1')]
        spec += [('E3', 'mlp_intermedia', 'mlp_temprana'), ('E3', 'mlp_intermedia', 'mlp_tardia'), ('E3', 'mlp_tardia', 'mlp_temprana')]
        for exp, a, b in spec:
            rows.append(dict(task=task, experiment=exp, contrast=f'{a} − {b}', **con(w, a, b)))
        # E4 fatiga/habituación con predicciones fuera de fold del análisis final
        T = V3.Task(data, task)
        rt = pd.Series(rel_time(T)[T.lab_pos], index=T.lab.source_row)
        cat = pd.Series(category(T.lab.stimulus), index=T.lab.source_row)
        for strat in ['hgb_c1', 'hgb_c32']:
            g = main[main.strategy.eq(strat)].copy()
            g['t'] = g.source_row.map(rt)
            g['q'] = g.groupby('participant').t.transform(lambda s: pd.qcut(s.rank(method='first'), 5, labels=False))
            for q, h in g.groupby('q'):
                aucs = [roc_auc_score(x.y, x.prob) for _, x in h.groupby('participant') if x.y.nunique() == 2]
                e4.append(dict(task=task, strategy=strat, quintil=int(q) + 1, prevalencia_alta=h.y.mean(),
                               prob_media=h.prob.mean(), auc=np.mean(aucs), people=len(aucs)))
            g['cat'] = g.source_row.map(cat)
            for c, h in g.groupby('cat'):
                aucs = [roc_auc_score(x.y, x.prob) for _, x in h.groupby('participant') if x.y.nunique() == 2 and len(x) >= 20]
                e6.append(dict(task=task, strategy=strat, categoria=c, ventanas=len(h), auc=np.mean(aucs) if aucs else np.nan,
                               people=len(aucs)))
        im = pd.read_csv(OUT / f'importancia_{task}.csv')
        im = im.groupby(['block', 'fold']).drop.mean().groupby('block').agg(['mean', 'std', 'count']).reset_index()
        imp_all.append(im.assign(task=task))
    rows = pd.DataFrame(rows)
    prim = rows.experiment.eq('E1 principal')
    ps = rows.loc[prim, 'p'].sort_values()
    run_, holm = 0, {}
    for i, (ix, p) in enumerate(ps.items()):
        run_ = max(run_, min(1, p * (len(ps) - i)))
        holm[ix] = run_
    rows['p_holm'] = rows.index.map(holm)
    rows.to_csv(OUT / 'contrastes.csv', index=False)
    pd.DataFrame(summ).to_csv(OUT / 'metricas.csv', index=False)
    e4 = pd.DataFrame(e4); e4.to_csv(OUT / 'fatiga_por_quintil.csv', index=False)
    e6 = pd.DataFrame(e6); e6.to_csv(OUT / 'por_categoria.csv', index=False)
    imp = pd.concat(imp_all); imp.to_csv(OUT / 'importancia_resumen.csv', index=False)
    pd.set_option('display.width', 200)
    print(pd.DataFrame(summ).round(4).to_string(index=False))
    print(rows.round(4).to_string(index=False))
    print(e4.round(4).to_string(index=False))
    print(e6.round(4).to_string(index=False))
    print(imp.sort_values(['task', 'mean'], ascending=[True, False]).round(4).to_string(index=False))


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
