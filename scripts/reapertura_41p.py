"""Reapertura de la experimentación (22-11-2026), registrada antes de correr.

Mario reabre la experimentación el 22-11-2026 para obtener conclusiones más firmes. "Más firme" significa
una respuesta más precisa y mejor controlada (positiva, nula o inconclusa) bajo reglas fijadas de antemano;
no se buscan variantes hasta lograr significancia. Etiquetas, variables, modelos y configuración congelada
(HGB 7 hojas en atención y 15 en activación) no cambian. Las 41 personas ya se consultaron en los análisis
anteriores: nada de esto es una confirmación independiente en una cohorte nueva.

Familia confirmatoria (4 pruebas, Holm; reglas de decisión del análisis final):
  P1 Precisión del contraste principal. HGB hasta 32 − HGB sin historial, con validación cruzada agrupada
     por persona repetida en 5 particiones nuevas (semillas 1101-1105). La AUC de cada persona se promedia
     sobre las 5 particiones antes de la inferencia. Reduce el ruido de partición del análisis final
     (una sola partición), que dejó activación en +0,034 [−0,001; +0,069].
  P2 Control del tiempo de sesión. (HGB hasta 32 + segundos desde el inicio de la sesión) −
     (HGB sin historial + segundos desde el inicio de la sesión), mismas 5 particiones. Amenaza que pone a
     prueba: la prevalencia de activación cae a lo largo de la sesión y las señales derivan; el historial
     podría estar codificando solo el momento de la sesión.
  Ambas en atención y activación.

Familia secundaria: curva temporal (5 pruebas por tarea, Holm dentro de la tarea), partición del análisis final.
  Para cada desfase L en {6, 12, 24, 48, 96} s el modelo recibe la ventana actual más la media y la desviación
  de las ventanas de la misma persona cuyo inicio cae en [t−L−6, t−L) s de reloj, sin importar el estímulo.
  Placebo: el mismo número de ventanas de la misma persona, tomadas al azar a 150 s o más de distancia.
  Todos los modelos se entrenan y evalúan en las mismas filas (las que tienen al menos 3 ventanas en las 5
  bandas). Contraste: desfase L − placebo. Tendencia: pendiente por persona de ese contraste contra log2(L),
  prueba de signos sobre la pendiente media.

Descriptivos (sin inferencia confirmatoria):
  D1 Modelo que solo recibe los segundos transcurridos en el estímulo (sin fisiología) y AUC del modelo sin
     historial estratificada por esa posición: cuánto de la detección no depende del momento del estímulo.
  D2 Autocorrelación de la etiqueta: AUC de la etiqueta de la misma persona 6 s antes (mismo segmento) como
     predictor de la actual. Referencia de cuánto es predecible desde su propio pasado.

Reglas de decisión (idénticas al análisis final, margen 0,02):
  respaldo: p Holm < 0,05 e IC 95 % inferior > 0; efecto relevante: además IC 95 % inferior > 0,02;
  nulo concluyente: IC 90 % dentro de (−0,02; +0,02); inferior: IC 95 % superior < 0; resto: inconcluso.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from threadpoolctl import threadpool_limits
from atencion_binaria import ROOT, digest, write
import cierre_experimental_v3 as V3
import cierre_final_41p as F

OUT = ROOT / 'resultados/reapertura_41p_22-11-2026'
REP_SEEDS = [1101, 1102, 1103, 1104, 1105]
LAGS = [6, 12, 24, 48, 96]
BAND = 6            # ancho de la banda, s
MIN_BAND = 3        # ventanas mínimas por banda
PLACEBO_GAP = 150   # distancia mínima del placebo, s
PLACEBO_SEED = 20261122
LABEL_LAG = 6
REP_MODELS = ['hgb_c1', 'hgb_c32', 'c1_ts', 'c32_ts']
CONFIRMATORY = [('P1', 'hgb_c32', 'hgb_c1'), ('P2', 'c32_ts', 'c1_ts')]


def plan():
    return json.loads((OUT / 'protocolo.json').read_text())


def inputs():
    paths = [Path(__file__), ROOT / 'scripts/cierre_final_41p.py', ROOT / 'scripts/cierre_experimental_v3.py',
             ROOT / 'scripts/temporales_core.py', F.OUT / 'protocolo.json', F.OUT / 'predicciones_atencion.csv.gz',
             F.OUT / 'predicciones_activacion.csv.gz', V3.SOURCE, V3.PARTS, V3.LABELS_ACT, V3.TEACHER, *V3.SPATIAL]
    return {str(p.relative_to(ROOT)): digest(p) for p in paths}


def prepare():
    OUT.mkdir(exist_ok=False)
    people = sorted(pd.read_csv(V3.PARTS).query("split in ['train','validation','test']").participant)
    assert len(people) == 41
    reps = {}
    for s in REP_SEEDS:
        order = np.random.default_rng(s).permutation(people)
        reps[str(s)] = [sorted(order[i::F.N_FOLDS].tolist()) for i in range(F.N_FOLDS)]
    write(OUT / 'protocolo.json', dict(
        created_utc=pd.Timestamp.now(tz='UTC').isoformat(),
        approval='Mario reabre la experimentación el 22-11-2026 y pide conclusiones más firmes. Registrado antes de '
                 'correr; se ejecuta una vez.',
        inputs=inputs(), leaves=F.LEAVES, hgb=V3.HGB, folds_rep=reps, folds_main=F.plan()['folds'],
        lags=LAGS, band=BAND, min_band=MIN_BAND, placebo_gap=PLACEBO_GAP, placebo_seed=PLACEBO_SEED,
        label_lag=LABEL_LAG, margin=F.MARGIN,
        confirmatory=dict(tests=[f'{n}: {a} − {b}' for n, a, b in CONFIRMATORY], tasks=list(F.LEAVES),
                          holm='sobre las 4 pruebas (2 contrastes × 2 tareas)',
                          unit='AUC por persona promediada sobre las 5 particiones; diferencia pareada por persona (41)'),
        secondary=dict(tests=[f'lag{L} − placebo' for L in LAGS], holm='sobre los 5 desfases dentro de cada tarea',
                       trend='pendiente por persona de (lagL − placebo) contra log2(L); prueba de signos bilateral '
                             'sobre la pendiente media, sin ajuste',
                       rows='filas etiquetadas con al menos MIN_BAND ventanas en las 5 bandas; todos los modelos '
                            'se entrenan y evalúan en esas mismas filas'),
        descriptive=['D1 posición sola y AUC sin historial estratificada por posición',
                     'D2 autocorrelación de la etiqueta a 6 s'],
        inference='IC 95 % y 90 % bootstrap por persona (20000, semilla 20261029). Permutación de signos bilateral '
                  '(200000, semilla 20261116).',
        decision=dict(respaldo='p Holm < 0,05 e IC95 inferior > 0', relevante='además IC95 inferior > 0,02',
                      nulo='IC90 dentro de (−0,02; +0,02)', inferior='IC95 superior < 0', resto='inconcluso'),
        limits='Las 41 personas ya se consultaron: no es confirmación independiente. P1 repite el contraste principal '
               'con otras particiones para ganar precisión; tres particiones alternativas ya se habían visto en la '
               'prueba de robustez R3 (+0,042 en activación). Etiquetas offline y variables transductivas por persona '
               '(ver protocolo V3). La etiqueta de activación integra 6 s de GSR; el GSR no es entrada en activación. '
               'La curva temporal usa las personas con filas comunes (40 en activación: una persona con 26 filas '
               'etiquetadas no tiene ninguna; 41 en atención), contado antes de correr y sin mirar resultados.'))
    print('Protocolo registrado', OUT / 'protocolo.json')


# ---------------------------------------------------------------- variables
def seconds(T):
    return pd.to_datetime(T.all.window_start_utc, utc=True).dt.as_unit('ns').astype('int64').to_numpy() / 1e9


def session_time(T):
    """Segundos desde la primera ventana de la persona."""
    t = seconds(T)
    start = pd.Series(t).groupby(T.all.participant.to_numpy()).transform('min').to_numpy()
    return (t - start).astype('float32')


def stimulus_position(T):
    """Segundos transcurridos en el estímulo (misma definición del explicativo del 18-11)."""
    return np.minimum(T.hist[32][1], 32).astype('float32')


def band_indices(T, lag):
    """Para cada ventana, ventanas de la misma persona con inicio en [t−lag−BAND, t−lag). -1 = relleno."""
    t = seconds(T)
    person = T.all.participant.to_numpy()
    width = BAND + 2
    ix = np.full((len(t), width), -1, dtype=np.int64)
    n = np.zeros(len(t), dtype=np.int64)
    for p in np.unique(person):
        rows = np.flatnonzero(person == p)
        rows = rows[np.argsort(t[rows], kind='stable')]
        tt = t[rows]
        lo = np.searchsorted(tt, tt - lag - BAND, side='left')
        hi = np.searchsorted(tt, tt - lag, side='left')
        for j, r in enumerate(rows):
            sel = rows[lo[j]:hi[j]]
            assert len(sel) <= width
            ix[r, :len(sel)] = sel
            n[r] = len(sel)
    return ix, n


def placebo_indices(T, counts):
    """Mismo número de ventanas de la misma persona, al azar, a PLACEBO_GAP s o más (antes o después)."""
    t = seconds(T)
    person = T.all.participant.to_numpy()
    rng = np.random.default_rng(PLACEBO_SEED)
    ix = np.full((len(t), BAND + 2), -1, dtype=np.int64)
    n = np.zeros(len(t), dtype=np.int64)
    pools = {p: np.flatnonzero(person == p) for p in np.unique(person)}
    for r in range(len(t)):
        k = counts[r]
        if k == 0:
            continue
        pool = pools[person[r]]
        pool = pool[np.abs(t[pool] - t[r]) >= PLACEBO_GAP]
        if len(pool) < k:
            continue
        ix[r, :k] = rng.choice(pool, size=k, replace=False)
        n[r] = k
    return ix, n


def summary(Z, ix, n):
    """Media y desviación de las ventanas indicadas (filas con n >= 1)."""
    x = Z[np.maximum(ix, 0)]
    mask = (ix >= 0)[:, :, None]
    x = np.where(mask, x, 0)
    mean = x.sum(axis=1) / n[:, None]
    var = (((x - mean[:, None, :]) ** 2) * mask).sum(axis=1) / n[:, None]
    return np.column_stack([mean, np.sqrt(np.maximum(var, 0))]).astype('float32')


def fold_setup(T, test_people):
    fit = np.flatnonzero(~T.lab.participant.isin(test_people).to_numpy())
    ev = np.flatnonzero(T.lab.participant.isin(test_people).to_numpy())
    assert set(T.lab.participant.iloc[fit]).isdisjoint(test_people) and len(ev)
    prep = V3.preprocessor().fit(T.lab.iloc[fit][T.cols])
    Za = prep.transform(T.all[T.cols]).astype('float32')
    Zl = prep.transform(T.lab[T.cols]).astype('float32')
    return fit, ev, Za, Zl


# ---------------------------------------------------------------- corridas
def verify():
    p = plan()
    for path, h in p['inputs'].items():
        assert digest(ROOT / path) == h, path
    return p


def run_rep(task, seed):
    p = verify()
    dest = OUT / f'rep_{task}_{seed}.csv.gz'
    assert not dest.exists()
    T = V3.Task(V3.load_data(), task)
    ts, pos = session_time(T), stimulus_position(T)
    leaves = p['leaves'][task]
    preds = []
    for k, test_people in enumerate(p['folds_rep'][str(seed)]):
        fit, ev, Za, Zl = fold_setup(T, test_people)
        y, w = T.lab.y.to_numpy()[fit], V3.weights(T.lab.iloc[fit])
        base = T.lab.iloc[ev][['source_row', 'participant', 'y']]
        mats = {}
        for name, kind in [('hgb_c1', 1), ('hgb_c32', 32)]:
            mats[name] = (V3.hgb_matrix(T, Za, Zl, fit, kind), V3.hgb_matrix(T, Za, Zl, ev, kind))
        mats['c1_ts'] = tuple(np.column_stack([m, ts[T.lab_pos[r]]]) for m, r in zip(mats['hgb_c1'], (fit, ev)))
        mats['c32_ts'] = tuple(np.column_stack([m, ts[T.lab_pos[r]]]) for m, r in zip(mats['hgb_c32'], (fit, ev)))
        if seed == REP_SEEDS[0]:  # D1: solo posición en el estímulo, sin fisiología
            mats['pos_only'] = (pos[T.lab_pos[fit]][:, None], pos[T.lab_pos[ev]][:, None])
        for name, (Xf, Xe) in mats.items():
            m = V3.fit_hgb(Xf, y, w, leaves)
            preds.append(base.assign(prob=m.predict_proba(Xe)[:, 1], strategy=name, fold=k, seed=seed))
        print(task, 'rep', seed, 'fold', k, flush=True)
    pd.concat(preds).to_csv(dest, index=False)


def run_lag(task):
    p = verify()
    dest = OUT / f'lag_{task}.csv.gz'
    assert not dest.exists()
    T = V3.Task(V3.load_data(), task)
    bands = {L: band_indices(T, L) for L in p['lags']}
    plc = placebo_indices(T, bands[p['lags'][0]][1])
    ok_all = np.all([n >= p['min_band'] for _, n in bands.values()], axis=0) & (plc[1] >= p['min_band'])
    common = np.flatnonzero(ok_all[T.lab_pos])  # filas etiquetadas con cobertura en todas las bandas
    cov = dict(task=task, labelled=int(len(T.lab)), common=int(len(common)),
               people=int(T.lab.participant.iloc[common].nunique()),
               per_person_min=int(T.lab.participant.iloc[common].value_counts().min()))
    write(OUT / f'cobertura_{task}.json', cov)
    leaves = p['leaves'][task]
    preds = []
    for k, test_people in enumerate(p['folds_main']):
        fit, ev, Za, Zl = fold_setup(T, test_people)
        fit, ev = np.intersect1d(fit, common), np.intersect1d(ev, common)
        y, w = T.lab.y.to_numpy()[fit], V3.weights(T.lab.iloc[fit])
        base = T.lab.iloc[ev][['source_row', 'participant', 'y']]
        mats = {'c1_common': (Zl[fit], Zl[ev])}
        for name, (ix, n) in [(f'lag{L}', bands[L]) for L in p['lags']] + [('placebo', plc)]:
            mats[name] = tuple(np.column_stack([Zl[r], summary(Za, ix[T.lab_pos[r]], n[T.lab_pos[r]])]) for r in (fit, ev))
        for name, (Xf, Xe) in mats.items():
            m = V3.fit_hgb(Xf, y, w, leaves)
            preds.append(base.assign(prob=m.predict_proba(Xe)[:, 1], strategy=name, fold=k))
        print(task, 'lag fold', k, flush=True)
    pd.concat(preds).to_csv(dest, index=False)


# ---------------------------------------------------------------- informe
def person_auc(pred, keys=('strategy',)):
    rows = []
    for key, g in pred.groupby(list(keys) + ['participant']):
        if g.y.nunique() == 2:
            rows.append(dict(zip(list(keys) + ['participant'], key), auc=roc_auc_score(g.y, g.prob)))
    return pd.DataFrame(rows)


def holm(ps):
    ps = pd.Series(ps)
    out, running = {}, 0
    for i, (ix, p) in enumerate(ps.sort_values().items()):
        running = max(running, min(1, p * (len(ps) - i)))
        out[ix] = running
    return pd.Series(out).reindex(ps.index).to_numpy()


def contrast(wide, a, b):
    d = (wide[a] - wide[b]).dropna().to_numpy()
    lo95, hi95 = F.ci(d)
    lo90, hi90 = F.ci(d, (.05, .95))
    return dict(delta=float(d.mean()), low95=lo95, high95=hi95, low90=lo90, high90=hi90, p=F.sign_flip(d),
                improved=int((d > 0).sum()), people=len(d))


def stratified_auc(g, strata):
    """AUC dentro de estratos, ponderada por el número de pares positivo-negativo."""
    num = den = 0
    for _, s in g.groupby(strata):
        pairs = int(s.y.sum()) * int((1 - s.y).sum())
        if pairs:
            num += roc_auc_score(s.y, s.prob) * pairs
            den += pairs
    return num / den if den else np.nan


def report():
    p = plan()
    conf, sec, desc, absol = [], [], [], []
    for task in F.LEAVES:
        T = V3.Task(V3.load_data(), task)
        # ---- confirmatoria: promedio por persona sobre las 5 particiones
        rep = pd.concat([pd.read_csv(OUT / f'rep_{task}_{s}.csv.gz') for s in REP_SEEDS])
        pa = person_auc(rep, ('seed', 'strategy'))
        wide = pa[pa.strategy.isin(REP_MODELS)].groupby(['participant', 'strategy']).auc.mean().unstack()
        assert len(wide) == 41 and pa[pa.strategy.isin(REP_MODELS)].groupby(['participant', 'strategy']).size().eq(5).all()
        for name, a, b in CONFIRMATORY:
            conf.append(dict(task=task, test=name, contrast=f'{a} − {b}', **contrast(wide, a, b)))
        desc.append(dict(task=task, item='c1_ts − hgb_c1 (tiempo de sesión solo)', **contrast(wide, 'c1_ts', 'hgb_c1')))
        for s, g in pa[pa.strategy.isin(REP_MODELS)].groupby('seed'):
            w = g.pivot(index='participant', columns='strategy', values='auc')
            for name, a, b in CONFIRMATORY:
                desc.append(dict(task=task, item=f'{name} partición {s}', delta=float((w[a] - w[b]).mean())))
        for s in REP_MODELS:
            lo, hi = F.ci(wide[s])
            absol.append(dict(task=task, strategy=s, auc=float(wide[s].mean()), low95=lo, high95=hi))
        # ---- secundaria: curva temporal
        lag = pd.read_csv(OUT / f'lag_{task}.csv.gz')
        wl = person_auc(lag).pivot(index='participant', columns='strategy', values='auc')
        rows = [dict(task=task, test=f'lag{L} − placebo', lag=L, **contrast(wl, f'lag{L}', 'placebo')) for L in p['lags']]
        for r, h in zip(rows, holm([r['p'] for r in rows])):
            r['p_holm'] = float(h)
        sec += rows
        D = np.column_stack([(wl[f'lag{L}'] - wl['placebo']).to_numpy() for L in p['lags']])
        keep = ~np.isnan(D).any(axis=1)
        slope = np.polyfit(np.log2(p['lags']), D[keep].T, 1)[0]
        lo, hi = F.ci(slope)
        desc.append(dict(task=task, item='pendiente de (lagL − placebo) por duplicación del desfase', delta=float(slope.mean()),
                         low95=lo, high95=hi, p=F.sign_flip(slope), improved=int((slope < 0).sum()), people=int(keep.sum())))
        desc.append(dict(task=task, item='placebo − c1_common', **contrast(wl, 'placebo', 'c1_common')))
        for L in p['lags']:
            desc.append(dict(task=task, item=f'lag{L} − c1_common', **contrast(wl, f'lag{L}', 'c1_common')))
        for s in wl.columns:
            lo, hi = F.ci(wl[s].dropna())
            absol.append(dict(task=task, strategy=f'curva:{s}', auc=float(wl[s].mean()), low95=lo, high95=hi))
        # ---- D1 posición
        first = rep[rep.seed.eq(REP_SEEDS[0])]
        pos = pd.Series(stimulus_position(T)[T.lab_pos], index=T.lab.source_row.to_numpy())
        c1 = first[first.strategy.eq('hgb_c1')].assign(pos=lambda d: d.source_row.map(pos))
        po = person_auc(first[first.strategy.eq('pos_only')]).auc
        lo, hi = F.ci(po)
        desc.append(dict(task=task, item='D1 AUC solo posición en el estímulo', delta=float(po.mean()), low95=lo, high95=hi, people=len(po)))
        st = c1.groupby('participant').apply(lambda g: stratified_auc(g, 'pos')).dropna()
        un = person_auc(c1).auc
        lo, hi = F.ci(st)
        desc.append(dict(task=task, item='D1 AUC sin historial, estratificada por posición', delta=float(st.mean()), low95=lo, high95=hi, people=len(st)))
        lo, hi = F.ci(un)
        desc.append(dict(task=task, item='D1 AUC sin historial, sin estratificar (misma partición)', delta=float(un.mean()), low95=lo, high95=hi, people=len(un)))
        # ---- D2 autocorrelación de la etiqueta
        t = seconds(T)[T.lab_pos]
        lab = T.lab.assign(t=t)
        key = ['participant', 'recording', 'segment_id', 'stimulus']
        prev = lab[key + ['t', 'y']].rename(columns={'y': 'y_prev'})
        prev['t'] = prev.t + LABEL_LAG
        m = pd.merge_asof(lab.sort_values('t'), prev.sort_values('t'), on='t', by=key, tolerance=1e-3, direction='nearest').dropna(subset=['y_prev'])
        ac = person_auc(m.rename(columns={'y_prev': 'prob'}).assign(strategy='y_prev')).auc
        lo, hi = F.ci(ac)
        desc.append(dict(task=task, item=f'D2 AUC de la etiqueta {LABEL_LAG} s antes', delta=float(ac.mean()), low95=lo, high95=hi,
                         people=len(ac), rows=int(len(m))))
    conf = pd.DataFrame(conf)
    conf['p_holm'] = holm(conf.p)
    conf['decision'] = [F.decide(r.delta, r.low95, r.high95, r.low90, r.high90, r.p_holm) for r in conf.itertuples()]
    sec = pd.DataFrame(sec)
    sec['decision'] = [F.decide(r.delta, r.low95, r.high95, r.low90, r.high90, r.p_holm) for r in sec.itertuples()]
    conf.to_csv(OUT / 'confirmatorio.csv', index=False)
    sec.to_csv(OUT / 'curva_temporal.csv', index=False)
    pd.DataFrame(desc).to_csv(OUT / 'descriptivos.csv', index=False)
    pd.DataFrame(absol).to_csv(OUT / 'auc_absolutas.csv', index=False)
    pd.set_option('display.width', 250)
    for name, df in [('CONFIRMATORIO', conf), ('CURVA TEMPORAL', sec), ('DESCRIPTIVOS', pd.DataFrame(desc)), ('AUC', pd.DataFrame(absol))]:
        print('\n' + name)
        print(df.round(4).to_string(index=False))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['prepare', 'rep', 'lag', 'report'])
    ap.add_argument('--task', choices=list(F.LEAVES))
    ap.add_argument('--seed', type=int)
    ap.add_argument('--threads', type=int, default=1)
    a = ap.parse_args()
    with threadpool_limits(limits=a.threads):
        if a.phase == 'rep':
            run_rep(a.task, a.seed)
        elif a.phase == 'lag':
            run_lag(a.task)
        else:
            globals()[a.phase]()
