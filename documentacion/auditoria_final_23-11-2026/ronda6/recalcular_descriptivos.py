"""Recálculo independiente de las cifras descriptivas que la auditoría del 23-11-2026 dejó sin recalcular.

Ronda 6. No importa ningún script del repositorio, no ajusta ni entrena modelos, no modifica archivos existentes
y solo escribe dentro de su propia carpeta (`registro.csv`, `registro.json`, `salida.txt`).

Uso:  .venv/bin/python documentacion/auditoria_final_23-11-2026/ronda6/recalcular_descriptivos.py

Todo sale de (a) las predicciones guardadas en `resultados/<etapa>/`, (b) la tabla de ventanas y variables
`resultados/preprocesamiento/caracteristicas_multimodales.csv`, (c) las tablas de etiquetas y (d), donde se indica,
los crudos en caché de `datos/locales/v2_2025` (solo lectura). El único objeto binario del proyecto que se abre
es `profesor_final.joblib`, para leer los pesos guardados; los mismos pesos se recalculan aparte con una
descomposición propia de la matriz de covarianza.

Convenciones propias (reimplementadas aquí):
  AUC            por rangos medios (Mann-Whitney), por persona.
  IC bootstrap   percentil sobre personas, 20.000 réplicas, semilla 20261029 (la declarada en los protocolos).
  permutación    de signos bilateral, 200.000, semilla 20261116 (la declarada).
  Spearman       correlación de Pearson de los rangos medios.
"""
from __future__ import annotations
import json, sys, time, warnings
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import rankdata

warnings.filterwarnings('ignore')
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RES = ROOT / 'resultados'
LOCAL = (ROOT / '../../datos/locales/v2_2025').resolve()
SOURCE = RES / 'preprocesamiento/caracteristicas_multimodales.csv'
PARTS = RES / 'modelado/particion_participantes.csv'
SEEDS = [1101, 1102, 1103, 1104, 1105]
SEGKEY = ['participant', 'recording', 'segment_id', 'stimulus']
T0 = time.time()
REG: list[dict] = []
LOG = open(HERE / 'salida.txt', 'w')


def say(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    LOG.write(s + '\n')
    LOG.flush()


# ------------------------------------------------------------------ utilidades estadísticas
def auc(y, s):
    y = np.asarray(y).astype(bool)
    n1, n0 = int(y.sum()), int((~y).sum())
    if n1 == 0 or n0 == 0:
        return np.nan
    r = rankdata(np.asarray(s, float))
    return float((r[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def boot(v, levels=(.025, .975), n=20000, seed=20261029):
    v = np.asarray(v, float)
    b = v[np.random.default_rng(seed).integers(0, len(v), (n, len(v)))].mean(axis=1)
    return [float(x) for x in np.quantile(b, levels)]


def signflip(d, n=200000, seed=20261116):
    d = np.asarray(d, float)
    s = np.random.default_rng(seed).choice([-1, 1], size=(n, len(d)))
    null = np.abs((s * d).mean(axis=1))
    return float((1 + (null >= abs(d.mean()) - 1e-15).sum()) / (n + 1))


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ra, rb = rankdata(a), rankdata(b)
    ra, rb = ra - ra.mean(), rb - rb.mean()
    den = np.sqrt((ra ** 2).sum() * (rb ** 2).sum())
    return float((ra * rb).sum() / den) if den > 0 else np.nan


def spearman_p(r, n):
    from scipy.stats import t as tdist
    if not np.isfinite(r) or abs(r) >= 1:
        return 0.0
    tt = r * np.sqrt((n - 2) / (1 - r * r))
    return float(2 * tdist.sf(abs(tt), n - 2))


def spearman_boot(a, b, n=5000, seed=20261029):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ix = np.random.default_rng(seed).integers(0, len(a), (n, len(a)))
    bs = [spearman(a[i], b[i]) for i in ix]
    return [float(x) for x in np.nanquantile(bs, [.025, .975])]


def holm(ps):
    ps = np.asarray(ps, float)
    order = np.argsort(ps, kind='stable')
    out, run = np.empty(len(ps)), 0.
    for i, j in enumerate(order):
        run = max(run, min(1., ps[j] * (len(ps) - i)))
        out[j] = run
    return out


def kappa(a, b):
    a, b = np.asarray(a).astype(int), np.asarray(b).astype(int)
    po = (a == b).mean()
    pe = sum((a == k).mean() * (b == k).mean() for k in (0, 1))
    return float((po - pe) / (1 - pe))


def strat_auc(y, s, strata):
    """AUC dentro de estratos, ponderada por pares positivo-negativo."""
    num = den = 0.
    df = pd.DataFrame(dict(y=np.asarray(y), s=np.asarray(s), g=np.asarray(strata)))
    for _, h in df.groupby('g'):
        pairs = int(h.y.sum()) * int((1 - h.y).sum())
        if pairs:
            num += auc(h.y, h.s) * pairs
            den += pairs
    return num / den if den else np.nan


def person_auc(pred, extra=()):
    """AUC por (extra..., estrategia, persona)."""
    keys = list(extra) + ['strategy', 'participant']
    rows = [(*k, auc(g.y.to_numpy(), g.prob.to_numpy())) for k, g in pred.groupby(keys, sort=False)]
    return pd.DataFrame(rows, columns=keys + ['auc']).dropna(subset=['auc'])


def wide_mean(pred):
    """AUC por persona y estrategia promediada sobre semillas."""
    pa = person_auc(pred, ('seed',))
    return pa.groupby(['participant', 'strategy']).auc.mean().unstack()


def contrast(d):
    d = np.asarray(pd.Series(d).dropna(), float)
    lo, hi = boot(d)
    lo90, hi90 = boot(d, (.05, .95))
    return dict(delta=float(d.mean()), low95=lo, high95=hi, low90=lo90, high90=hi90, p=signflip(d),
                mejoran=int((d > 0).sum()), n=len(d), mediana=float(np.median(d)))


# ------------------------------------------------------------------ registro de comparaciones
def rnd(x, d):
    return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP))


def fmt(x, d=None):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return '—'
    if isinstance(x, (int, np.integer)):
        return f'{int(x):,}'.replace(',', '.')
    s = repr(float(x)) if d is None else f'{rnd(x, d):.{d}f}'
    return s.replace('.', ',')


def reg(sec, cifra, informado, fuente, valor, dec=None, guardado=None, veredicto=None, nota='', escala=1.):
    """informado: número tal como aparece en el informe (float o int) o None; dec: decimales con que se informa.
    valor: recalculado completo. guardado: valor del CSV/JSON del repositorio, si existe. escala: 100 para %."""
    v = None if valor is None else float(valor) * escala
    if veredicto is None:
        if v is None or not np.isfinite(v):
            veredicto = 'no recalculable'
        elif informado is None:
            veredicto = 'sin cifra informada'
        elif dec is None or dec == 0 and float(informado).is_integer() and abs(v - round(v)) < 1e-9:
            veredicto = 'coincide' if abs(v - informado) < 1e-9 else 'difiere'
        else:
            r = rnd(v, dec)
            if abs(r - informado) < 1e-12:
                veredicto = 'coincide'
            elif abs(v - informado) <= 10 ** -dec + 1e-12:
                veredicto = 'coincide con redondeo'
            else:
                veredicto = 'difiere'
    dif_csv = None if guardado is None or valor is None else float(valor) - float(guardado)
    REG.append(dict(seccion=sec, cifra=cifra, informado=informado, decimales=dec, fuente=fuente,
                    recalculado=None if valor is None else float(valor), escala=escala, guardado=guardado,
                    dif_guardado=dif_csv, veredicto=veredicto, nota=nota))
    say(f'[{sec}] {cifra}: informado {informado} | recalculado {valor!r} | guardado {guardado!r} | {veredicto} {nota}')


# ------------------------------------------------------------------ tabla de ventanas (reconstrucción propia)
def load_windows():
    src = pd.read_csv(SOURCE)
    src['source_row'] = np.arange(len(src))
    parts = pd.read_csv(PARTS).set_index('participant')
    src['split'] = src.participant.map(parts.split)
    spatial = [RES / 'eeg_por_canal_v2_29-10-2026/caracteristicas_eeg_por_canal.csv.gz',
               RES / 'temporalidad_eeg_v2_validacion_29-10-2026/caracteristicas_validation.csv.gz',
               RES / 'temporalidad_eeg_v2_test_29-10-2026/caracteristicas_test.csv.gz']
    rows = np.concatenate([pd.read_csv(p, usecols=['source_row']).source_row.to_numpy() for p in spatial])
    assert len(rows) == len(set(rows))
    W = src[src.split.isin(['train', 'validation', 'test'])].copy()
    n41 = len(W)
    W = W[W.source_row.isin(set(rows))].copy()
    assert len(W) == n41, 'la tabla por canal no cubre todas las ventanas de las 41 personas'
    W['t'] = pd.to_datetime(W.window_start_utc, utc=True).astype('int64').to_numpy() / 1e9 if False else \
        pd.to_datetime(W.window_start_utc, utc=True).dt.as_unit('ns').astype('int64').to_numpy() / 1e9
    W = W.sort_values(SEGKEY + ['t']).reset_index(drop=True)
    assert not W.duplicated(SEGKEY + ['t']).any()
    # segmento continuo y posición (número de ventanas consecutivas a 1 s dentro del segmento, tope 32)
    W['seg'] = W.groupby(SEGKEY, sort=False).ngroup()
    gap = W.groupby('seg').t.diff()
    newrun = gap.isna() | ~np.isclose(gap.fillna(1.), 1.0, atol=1e-4, rtol=0)
    assert (gap.dropna() > 0).all()
    W['run'] = newrun.cumsum()
    W['pos'] = np.minimum(W.groupby('run').cumcount() + 1, 32)
    W['ts'] = W.t - W.groupby('participant').t.transform('min')          # s desde la primera ventana de la persona
    W['ts_rec'] = W.t - W.groupby('recording').t.transform('min')        # s desde la primera ventana de la grabación
    return src, W


def attention_score(W):
    """Puntaje ocular del Modelo Profesor (PCA guardada) y etiqueta original; pesos leídos del .joblib."""
    import joblib
    teacher = joblib.load(RES / 'temporalidad_eeg_v2_validacion_29-10-2026/profesor_final.joblib')
    comp, mean, sign = teacher['pca'].components_[0].copy(), teacher['pca'].mean_.copy(), teacher['sign']
    evr = float(teacher['pca'].explained_variance_ratio_[0])
    cols = ['fixation_total_ms', 'fixation_mean_ms', 'gaze_dispersion_2d_px', 'gaze_path_length_px', 'pupil_mean_z']
    direc = np.array([1, 1, -1, -1, 1.])
    v = W[cols].astype(float).copy()
    for c in cols[:4]:
        v[c] = np.log1p(v[c].clip(lower=0))
    g = v.groupby(W.participant)
    mu, sd = g.transform('mean'), g.transform(lambda s: s.std(ddof=0))
    z = (v - mu) / sd.where(sd > 0) * direc
    ok = z.notna().all(axis=1)
    score = pd.Series(np.nan, index=W.index)
    score[ok] = ((z[ok].to_numpy() - mean) @ comp) * sign
    med = score.groupby(W.participant).transform('median')
    y = (score > med).astype(float).where(score.notna())
    return z, score, y, dict(comp=comp, mean=mean, sign=sign, evr=evr, cols=cols)


def read_pred(path, **kw):
    return pd.read_csv(path, **kw)


def rep(task, strategies=None):
    r = pd.concat([pd.read_csv(RES / f'reapertura_41p_22-11-2026/rep_{task}_{s}.csv.gz') for s in SEEDS])
    return r if strategies is None else r[r.strategy.isin(strategies)]


# ================================================================== 8. Etiquetas
def rebuild_gsr_v2(W):
    """Reimplementación propia de la etiqueta GSR V2 a partir de las variables (sin leer la tabla de etiquetas)."""
    C = ['gsr_tonic_mean_z', 'gsr_phasic_mean_z', 'gsr_scr_count', 'gsr_scr_mean_prominence_z']
    f = W.copy()
    X = f[C].astype(float)
    finite = np.isfinite(X.to_numpy()).all(axis=1)
    covered = (f.gsr_coverage >= .5) & (f.gsr_n > 0) & (f.gsr_window_valid.astype(str).str.lower() == 'true')
    plaus = (f.gsr_scr_count >= 0) & (f.gsr_scr_mean_prominence_z >= 0)
    valid = (covered & finite & plaus).to_numpy()
    V = X.copy()
    V[C[2]], V[C[3]] = np.log1p(V[C[2]]), np.log1p(V[C[3]])
    Z = pd.DataFrame(np.nan, index=f.index, columns=C)
    for _, ix in f[valid].groupby('participant').groups.items():
        for c in C:
            v = V.loc[ix, c]
            sd = v.std(ddof=0)
            Z.loc[ix, c] = (v - v.mean()) / sd if (len(v) >= 2 and np.isfinite(sd) and sd > 1e-8) else 0.
    s = Z.mean(axis=1, skipna=False)
    s2 = pd.Series(np.nan, index=f.index)
    for _, ix in f.groupby('participant').groups.items():
        v = s.loc[ix]
        sd = v.std(ddof=0)
        if np.isfinite(sd) and sd > 1e-8:
            s2.loc[ix] = (v - v.mean()) / sd
    good = valid & np.isfinite(s2.to_numpy())
    brk = (f.run != f.run.shift()).to_numpy() | ~good | ~np.r_[False, good[:-1]]
    rid = np.cumsum(brk)
    k = pd.Series(np.where(good, 1, 0)).groupby(rid).cumsum().to_numpy() * good
    roll = s2.where(good).groupby(rid).transform(lambda v: v.rolling(5).mean()).to_numpy()
    s6 = np.where(k >= 5, roll, np.nan)
    y = pd.Series(np.nan, index=f.index)
    ties = 0
    s6 = pd.Series(s6, index=f.index)
    for _, ix in f.groupby('participant').groups.items():
        v = s6.loc[ix].dropna()
        sd = v.std(ddof=0)
        if len(v) < 2 or not np.isfinite(sd) or sd <= 1e-8:
            continue
        z = (v - v.mean()) / sd
        med = z.median()
        tie = (z - med).abs() <= 1e-8
        ties += int(tie.sum())
        y.loc[z.index[~tie]] = (z[~tie] > med).astype(float)
    return y, valid, np.minimum(k, 5), ties, s6


def sec_etiquetas(src, W, att):
    S = '8 Etiquetas'
    z, score, y_att, info = att
    F1 = 'INFORME etiquetas_gsr_calidad_v2'
    reg(S, 'Ventanas de las 41 personas', 22211, F1, len(W), 0)
    for sp, n in [('train', 13524), ('validation', 4662), ('test', 4025)]:
        reg(S, f'Ventanas en {sp}', n, F1, int((W.split == sp).sum()), 0)
    E = pd.read_csv(RES / 'etiquetas_gsr_calidad_v2_01-11-2026/etiquetas.csv.gz')
    reg(S, 'Ventanas con etiqueta de activación (tabla guardada)', 11796, F1, int(E.activation_binary_v2.notna().sum()), 0)
    y, valid, k, ties, s6 = rebuild_gsr_v2(W)
    reg(S, 'Ventanas con etiqueta de activación (reconstrucción propia desde las variables)', 11796, F1, int(y.notna().sum()), 0)
    m = W[['source_row']].assign(y=y.to_numpy()).merge(E[['source_row', 'activation_binary_v2', 'label_reason']], on='source_row')
    same = ((m.y.fillna(-1)) == (m.activation_binary_v2.astype(float).fillna(-1))).all()
    reg(S, 'Etiquetas de activación reconstruidas idénticas a las guardadas (ventanas distintas)', 0, F1,
        int(((m.y.fillna(-1)) != (m.activation_binary_v2.astype(float).fillna(-1))).sum()), 0)
    reg(S, '% de ventanas que conserva la etiqueta de activación', 53.1, F1, y.notna().mean(), 1, escala=100)
    reg(S, '% de ventanas que conserva la etiqueta (cierre: "53 %")', 53, 'Cierre, límites', y.notna().mean(), 0, escala=100)
    reg(S, 'Ventanas sin etiqueta', 10415, F1, int(y.isna().sum()), 0)
    reg(S, 'Sin etiqueta por cobertura/flag inválido', 401, F1, int((~valid).sum()), 0)
    reg(S, 'Sin etiqueta por empate con la mediana', 19, F1, ties, 0)
    reg(S, 'Sin etiqueta por historial insuficiente', 9995, F1, int(y.isna().sum() - (~valid).sum() - ties), 0)
    for sp, n in [('train', 7028), ('validation', 2584), ('test', 2184)]:
        reg(S, f'Etiquetas de activación en {sp}', n, F1, int(y[W.split == sp].notna().sum()), 0)
    p4 = W.participant == 'P4'
    reg(S, 'P4: ventanas con etiqueta de activación', 26, F1, int(y[p4].notna().sum()), 0)
    reg(S, 'P4: ventanas totales', 459, F1, int(p4.sum()), 0)
    both = y.groupby(W.participant).agg(lambda v: v.dropna().nunique()).eq(2).sum()
    reg(S, 'Personas con ambas clases de activación', 41, F1, int(both), 0)
    # atención
    reg(S, 'Ventanas con etiqueta de atención (reconstrucción propia del puntaje)', 22176, 'Auditoría 23-11, integridad', int(y_att.notna().sum()), 0)
    r1 = pd.read_csv(RES / 'reapertura_41p_22-11-2026/rep_atencion_1101.csv.gz')
    r1 = r1[r1.strategy.eq('hgb_c1')]
    reg(S, 'Ventanas de atención en las predicciones guardadas', 22176, 'Auditoría 23-11', len(r1), 0)
    mm = r1.merge(W[['source_row']].assign(ya=y_att.to_numpy()), on='source_row')
    reg(S, 'Etiquetas de atención de las predicciones distintas de las reconstruidas', 0, '—', int((mm.y != mm.ya).sum()), 0)
    # PCA del Modelo Profesor: recalculada con descomposición propia sobre las 25 personas de entrenamiento
    tr = (W.split == 'train') & z.notna().all(axis=1)
    Zt = z[tr].to_numpy()
    reg(S, 'Ventanas válidas de entrenamiento del Modelo Profesor', 13498, 'INFORME profesor_binario', int(tr.sum()), 0)
    reg(S, 'Ventanas de entrenamiento omitidas por componentes incompletos', 26, 'INFORME profesor_binario', int((W.split == 'train').sum() - tr.sum()), 0)
    cov = np.cov(Zt - Zt.mean(0), rowvar=False)
    val, vec = np.linalg.eigh(cov)
    c1 = vec[:, -1]
    if c1 @ np.array([.125] * 4 + [.5]) < 0:
        c1 = -c1
    evr = val[-1] / val.sum()
    reg(S, '% de varianza de la primera componente', 51.5, 'Borrador Resultados §2', evr, 1, guardado=info['evr'], escala=100)
    names = ['duración total de fijaciones', 'duración media de fijación', 'dispersión de la mirada', 'recorrido de la mirada', 'pupila']
    informed = [0.398, None, None, None, -0.052]
    for nm, w_, st, inf in zip(names, c1, info['comp'] * info['sign'], informed):
        reg(S, f'Peso PCA: {nm}', inf, 'Borrador Resultados §2; cierre H3', w_, 3, guardado=float(st))
    reg(S, 'Peso mínimo de las cuatro variables de mirada', 0.40, 'INFORME enfoques ("0,40 a 0,56")', float(c1[:4].min()), 2)
    reg(S, 'Peso máximo de las cuatro variables de mirada', 0.56, 'INFORME enfoques ("0,40 a 0,56")', float(c1[:4].max()), 2)
    # concordancia de los dos profesores (25 personas de entrenamiento)
    Wt = W[W.split == 'train']
    zt = z.loc[Wt.index]
    okt = zt.notna().all(axis=1)
    s_ig = ((zt.iloc[:, :4].mean(axis=1) + zt.iloc[:, 4]) / 2).where(okt)
    s_pc = pd.Series(np.where(okt, (zt.to_numpy() - Zt.mean(0)) @ c1, np.nan), index=Wt.index)
    lab = lambda s: (s > s.groupby(Wt.participant).transform('median')).astype(float).where(s.notna())
    a, b = lab(s_ig), lab(s_pc)
    okk = a.notna() & b.notna()
    conc = json.loads((RES / 'profesor_binario_reconstruido_29-10-2026/concordancia_profesores.json').read_text())
    reg(S, '% de concordancia entre profesor igualitario y PCA', 66.28, 'INFORME profesor_binario', float((a[okk] == b[okk]).mean()), 2, guardado=conc['agreement'], escala=100)
    reg(S, 'Kappa entre profesor igualitario y PCA', 0.3255, 'INFORME profesor_binario', kappa(a[okk], b[okk]), 4, guardado=conc['kappa'])
    reg(S, 'Ventanas comparadas entre profesores', 13498, 'INFORME profesor_binario', int(okk.sum()), 0)
    # otros descriptivos del cierre
    lab_att = y_att.notna()
    reg(S, '% de ventanas con etiqueta de atención y fijaciones > 2.000 ms', 28, 'Cierre, límites ("cerca del 28 %")',
        float((W.fixation_total_ms[lab_att] > 2000).mean()), 0, escala=100)
    yy = y.notna()
    ton = W.gsr_tonic_mean_z
    pa = [auc(y[yy & (W.participant == p)], ton[yy & (W.participant == p)]) for p in sorted(W.participant.unique())]
    reg(S, 'AUC del nivel tónico de la ventana contra la etiqueta de activación (media por persona)', 0.911, 'Cierre H2', float(np.nanmean(pa)), 3)
    reg(S, 'Ídem, juntando todas las ventanas', None, '—', auc(y[yy], ton[yy]))
    for col, inf, nm in [('gsr_phasic_mean_z', .595, 'componente fásica'), ('gsr_scr_count', .522, 'número de respuestas'), ('gsr_scr_mean_prominence_z', .522, 'prominencia de las respuestas')]:
        ppl = sorted(W.participant.unique())
        pa_ = np.array([auc(y[yy & (W.participant == p)], W[col][yy & (W.participant == p)]) for p in ppl])
        var_ = np.array([W[col][yy & (W.participant == p)].nunique() > 1 for p in ppl])
        reg(S, f'AUC de la {nm} de la ventana contra la etiqueta de activación (media de las personas en que la variable varía)', inf, 'Borrador Resultados §2; AUDITORIA_CODIGO',
            float(pa_[var_].mean()), 3, nota=f'{int(var_.sum())} personas; con las 41 (constante = 0,5): {pa_.mean():.6f}')
    reg(S, 'Ventanas de activación de clase alta', 5898, 'Borrador Secciones pendientes §4.6', int((y == 1).sum()), 0)
    reg(S, 'Ventanas de activación de clase baja', 5898, 'Borrador Secciones pendientes §4.6', int((y == 0).sum()), 0)
    reg(S, 'P4: ventanas con GSR válida', 58, 'Borrador Secciones pendientes §4.6', int(valid[p4.to_numpy()].sum()), 0)
    reg(S, 'Ventanas del archivo completo', 25992, 'Borrador Secciones pendientes §4.7', len(src), 0)
    reg(S, '% de ventanas del archivo con fijaciones > 2.000 ms', 27.8, 'Borrador Secciones pendientes §4.7', float((src.fixation_total_ms > 2000).mean()), 1, escala=100)
    reg(S, '% de ventanas de las 41 personas con fijaciones > 2.000 ms', 27.7, 'Borrador Secciones pendientes §4.7', float((W.fixation_total_ms > 2000).mean()), 1, escala=100)
    reg(S, '% de ventanas de las 41 personas con fijaciones > 3.000 ms', 4, 'Borrador Secciones pendientes §4.7', float((W.fixation_total_ms > 3000).mean()), 0, escala=100)
    reg(S, 'Duración total máxima de fijaciones en una ventana, ms', 11365, 'Borrador Secciones pendientes §4.7', float(W.fixation_total_ms.max()), 0)
    return y


# ================================================================== 1. Ampliación E4, E6
def category(stim):
    s = pd.Series(stim).astype(str).str.replace(r'\s*\(\d+\)$', '', regex=True)
    out = pd.Series('instrucciones', index=s.index)
    out[s.str.fullmatch(r'\d+')] = 'numerado'
    out[s.str.startswith('blur')] = 'imagen blur'
    out[s.str.startswith('emotion')] = 'imagen emotion'
    out[s.str.startswith('diseño')] = 'diseño'
    out[s.str.match(r'^(Meg|diario_financiero|temu|Despega|Nint)')] = 'sitio web'
    out[s.eq('Text')] = 'texto'
    return out.to_numpy()


def sec_ampliacion(W):
    S = '1 Ampliación'
    D = RES / 'ampliacion_41p_16-11-2026'
    q_csv = pd.read_csv(D / 'fatiga_por_quintil.csv').set_index(['task', 'strategy', 'quintil'])
    c_csv = pd.read_csv(D / 'por_categoria.csv').set_index(['task', 'strategy', 'categoria'])
    info = W.set_index('source_row')[['ts_rec']].assign(cat=category(W.stimulus.to_numpy()))
    maxd = {'q': 0., 'c': 0.}
    got_q, got_c = {}, {}
    for task in ['atencion', 'activacion']:
        main = pd.read_csv(RES / f'cierre_final_41p_16-11-2026/predicciones_{task}.csv.gz')
        for strat in ['hgb_c1', 'hgb_c32']:
            g = main[main.strategy.eq(strat)].join(info, on='source_row')
            n = g.groupby('participant').ts_rec.transform('size')
            rk = g.groupby('participant').ts_rec.rank(method='first')
            g['q'] = sum((rk > 1 + (n - 1) * j / 5).astype(int) for j in range(1, 5)) + 1
            for q, h in g.groupby('q'):
                a = [auc(x.y, x.prob) for _, x in h.groupby('participant')]
                a = [v for v in a if np.isfinite(v)]
                got_q[(task, strat, q)] = (h.y.mean(), h.prob.mean(), float(np.mean(a)), len(a))
                ref = q_csv.loc[(task, strat, q)]
                maxd['q'] = max(maxd['q'], abs(h.y.mean() - ref.prevalencia_alta), abs(np.mean(a) - ref.auc), abs(len(a) - ref.people), abs(h.prob.mean() - ref.prob_media))
            for c, h in g.groupby('cat'):
                a = [auc(x.y, x.prob) for _, x in h.groupby('participant') if len(x) >= 20]
                a = [v for v in a if np.isfinite(v)]
                got_c[(task, strat, c)] = (len(h), float(np.mean(a)) if a else np.nan, len(a))
                ref = c_csv.loc[(task, strat, c)]
                dv = 0 if (not a and np.isnan(ref.auc)) else abs(np.mean(a) - ref.auc)
                maxd['c'] = max(maxd['c'], dv, abs(len(h) - ref.ventanas), abs(len(a) - ref.people))
    reg(S, 'E4: diferencia máxima con fatiga_por_quintil.csv (20 filas × prevalencia, prob. media, AUC, personas)', 0, 'fatiga_por_quintil.csv', maxd['q'], 9,
        veredicto='coincide' if maxd['q'] < 1e-9 else 'difiere')
    reg(S, 'E6: diferencia máxima con por_categoria.csv (26 filas × ventanas, AUC, personas)', 0, 'por_categoria.csv', maxd['c'], 9,
        veredicto='coincide' if maxd['c'] < 1e-9 else 'difiere')
    F = 'INFORME ampliación E4'
    for key, col, inf, d, name in [
            (('atencion', 'hgb_c1', 1), 2, 0.65, 2, 'atención, AUC sin historial, quintil 1'),
            (('atencion', 'hgb_c1', 5), 2, 0.71, 2, 'atención, AUC sin historial, quintil 5'),
            (('atencion', 'hgb_c32', 1), 2, 0.69, 2, 'atención, AUC con historial, quintil 1'),
            (('atencion', 'hgb_c32', 5), 2, 0.74, 2, 'atención, AUC con historial, quintil 5'),
            (('atencion', 'hgb_c1', 3), 0, 0.32, 2, 'atención, prevalencia de alta, quintil 3'),
            (('activacion', 'hgb_c1', 5), 0, 0.37, 2, 'activación, prevalencia de alta, quintil 5'),
            (('activacion', 'hgb_c32', 5), 2, 0.64, 2, 'activación, AUC con historial, quintil 5')]:
        csvcol = {0: 'prevalencia_alta', 2: 'auc'}[col]
        reg(S, f'E4 {name}', inf, F, got_q[key][col], d, guardado=float(q_csv.loc[key][csvcol]))
    for key, v in got_q.items():
        reg(S, f'E4 {key[0]} {key[1]} quintil {key[2]}: prevalencia / AUC / personas', None, 'fatiga_por_quintil.csv', v[2],
            guardado=float(q_csv.loc[key].auc), veredicto='coincide' if abs(v[2] - q_csv.loc[key].auc) < 1e-9 else 'difiere',
            nota=f'prevalencia {v[0]!r}; personas {v[3]}')
    F = 'INFORME ampliación E6'
    T6 = {('atencion', 'hgb_c1'): dict(zip(['sitio web', 'numerado', 'diseño', 'imagen emotion', 'imagen blur', 'texto'], [.707, .681, .649, .668, .696, .604])),
          ('atencion', 'hgb_c32'): dict(zip(['sitio web', 'numerado', 'diseño', 'imagen emotion', 'imagen blur', 'texto'], [.710, .698, .637, .667, .599, .633])),
          ('activacion', 'hgb_c1'): dict(zip(['sitio web', 'numerado', 'diseño', 'texto'], [.525, .588, .506, .506])),
          ('activacion', 'hgb_c32'): dict(zip(['sitio web', 'numerado', 'diseño', 'texto'], [.588, .591, .506, .524]))}
    for (task, strat), row in T6.items():
        for c, inf in row.items():
            v = got_c[(task, strat, c)]
            reg(S, f'E6 {task} {strat} {c}: AUC', inf, F, v[1], 3, guardado=float(c_csv.loc[(task, strat, c)].auc), nota=f'{v[2]} personas; {v[0]} ventanas')
    for c in ['imagen emotion']:
        for strat in ['hgb_c1', 'hgb_c32']:
            v = got_c[('activacion', strat, c)]
            reg(S, f'E6 activacion {strat} {c}: AUC (el informe pone "—")', None, 'por_categoria.csv', v[1], guardado=float(c_csv.loc[('activacion', strat, c)].auc),
                veredicto='coincide', nota=f'{v[2]} personas; {v[0]} ventanas; el informe la omite')
    # cobertura del historial desplazado 6 ventanas
    for task, inf in [('activacion', 73), ('atencion', 40)]:
        main = pd.read_csv(RES / f'cierre_final_41p_16-11-2026/predicciones_{task}.csv.gz')
        rows = main[main.strategy.eq('hgb_c1')].source_row
        pos = W.set_index('source_row').pos.loc[rows]
        cj = json.loads((D / f'enmienda_e1_lag6/cobertura_{task}.json').read_text())
        reg(S, f'E1: % de filas de {task} con historial desplazado 6 ventanas', inf, 'INFORME ampliación E1', float((pos > 6).mean()), 0,
            guardado=cj['rows_with_lag'], escala=100)
    return got_q, got_c


# ================================================================== 2. Cuatro enfoques
def ci_reg(S, cifra, inf, fuente, c, dec=3, guardado=None, with_ci=True, nota=''):
    """Registra media e IC de un contraste/AUC. inf = (media, lo, hi) informados o solo media."""
    if not isinstance(inf, tuple):
        inf = (inf, None, None)
    g = guardado if isinstance(guardado, (tuple, list)) else (guardado, None, None)
    reg(S, cifra, inf[0], fuente, c['delta'], dec, guardado=g[0], nota=nota)
    if with_ci and inf[1] is not None:
        reg(S, cifra + ' · IC 95 % inferior', inf[1], fuente, c['low95'], dec, guardado=g[1])
        reg(S, cifra + ' · IC 95 % superior', inf[2], fuente, c['high95'], dec, guardado=g[2])


def absol(v):
    v = pd.Series(v).dropna()
    lo, hi = boot(v)
    return dict(delta=float(v.mean()), low95=lo, high95=hi, n=len(v), sobre=int((v > .5).sum()))


def sec_enfoques(W, y_act):
    S = '2 Enfoques'
    D = RES / 'enfoques_41p_22-11-2026'
    Wi = W.set_index('source_row')
    # ---------------- E1
    F = 'INFORME enfoques E1'
    d1 = pd.read_csv(D / 'e1_descriptivos.csv')
    g1 = lambda item, lab=None: d1[(d1.item == item) & (d1.label.isna() if lab is None else d1.label.eq(lab))].iloc[0]
    tramo = np.digitize(W.pos.to_numpy(), [1, 2, 3, 4, 5, 8, 12, 20], right=True)
    med = W.score.groupby([W.participant, tramo]).transform('median')
    y_corr = (W.score > med).astype(float).where(W.score.notna())
    e1 = pd.concat([pd.read_csv(D / f'e1_{s}.csv.gz') for s in SEEDS])
    chk = e1.merge(pd.DataFrame(dict(source_row=W.source_row, yc=y_corr)), on='source_row')
    reg(S, 'E1: etiquetas corregidas de las predicciones distintas de mi reconstrucción', 0, '—', int((chk.y != chk.yc).sum()), 0)
    lab = pd.DataFrame(dict(p=W.participant, tramo=tramo, o=W.y_att, c=y_corr)).dropna()
    kap = lab.groupby('p').apply(lambda g: kappa(g.o, g.c))
    k = absol(kap)
    r = g1('kappa entre etiqueta original y corregida (por persona)')
    ci_reg(S, 'E1: kappa por persona entre etiqueta original y corregida', 0.81, F, k, 2, guardado=(r.delta, r.low95, r.high95))
    conc = float((lab.o == lab.c).mean())
    reg(S, 'E1: % de ventanas en que coinciden ambas etiquetas', 90.6, F, conc, 1, guardado=float(g1('concordancia global entre etiquetas').delta), escala=100)
    reg(S, 'E1: % de etiquetas que cambian', 9.4, F, 1 - conc, 1, escala=100)
    reg(S, 'E1: % de etiquetas que cambian (auditorías: 9,36 %)', 9.36, 'AUDITORIA_RESULTADOS enfoques', 1 - conc, 2, escala=100)
    reg(S, 'E1: personas con algún cambio de etiqueta', 41, 'AUDITORIA_RESULTADOS enfoques', int((lab.o != lab.c).groupby(lab.p).any().sum()), 0)
    prev = lab.groupby('tramo')[['o', 'c']].mean()
    names = ['1 s', '2 s', '3 s', '4 s', '5 s', '6–8 s', '9–12 s', '13–20 s', '21–32 s']
    late = lab[W.pos.loc[lab.index] >= 12]
    for nm, inf, v in [('primer segundo', .51, prev.o[0]), ('segundo 2', .37, prev.o[1]), ('segundo 3', .38, prev.o[2]), ('9 a 12 s', .53, prev.o[6]),
                       ('12 s o más', .62, late.o.mean())]:
        reg(S, f'E1/posición: prevalencia de atención alta, {nm}', inf, 'Borrador Resultados §7.2; INFORME explicativo', float(v), 2)
    reg(S, 'Posición: prevalencia de atención alta, 13 s o más (tramos 13–20 y 21–32 juntos)', None, '—', float(lab[lab.tramo >= 7].o.mean()))
    for b, row in prev.iterrows():
        reg(S, f'E1: prevalencia de atención alta, etiqueta original, tramo {names[b]}', None, 'e1_descriptivos.csv', row.o,
            guardado=float(g1(f'prevalencia tramo {b}: original').delta), veredicto='coincide' if abs(row.o - g1(f'prevalencia tramo {b}: original').delta) < 1e-9 else 'difiere',
            nota=f'corregida {row.c!r}; n={int((lab.tramo == b).sum())}')
    we = wide_mean(e1)
    wo = wide_mean(rep('atencion', ['hgb_c1', 'hgb_c32']))
    for s_, inf in [('hgb_c1', .675), ('hgb_c32', .685), ('pos_c1', .681), ('pos_only', (.504, .498, .510))]:
        r = g1(f'AUC {s_}')
        ci_reg(S, f'E1: AUC {s_} con etiqueta corregida', inf, F, absol(we[s_]), 3, guardado=(r.delta, r.low95, r.high95))
    reg(S, 'E1: AUC hgb_c1 con etiqueta original', .683, F, float(wo.hgb_c1.mean()), 3, guardado=float(g1('AUC hgb_c1', 'original').delta))
    reg(S, 'E1: mejora del historial con etiqueta original', .029, F, float((wo.hgb_c32 - wo.hgb_c1).mean()), 3)
    reg(S, 'E1: mejora del historial con etiqueta corregida (A2)', .010, F, float((we.hgb_c32 - we.hgb_c1).mean()), 3)
    reg(S, 'E1: A1 detección corregida − original', -.008, F, float((we.hgb_c1 - wo.hgb_c1).mean()), 3)
    # ---------------- E2
    F = 'INFORME enfoques E2'
    d2 = pd.read_csv(D / 'e2_descriptivos.csv')
    g2 = lambda item, lab=None: d2[(d2.item == item) & (d2.label.isna() if lab is None else d2.label.eq(lab))].iloc[0]
    e2 = pd.concat([pd.read_csv(D / f'e2_{s}.csv.gz') for s in SEEDS])
    ctrl = e2[e2.strategy.eq('control_barajado')]
    pred = pd.concat([e2[~e2.strategy.eq('control_barajado')], rep('atencion', ['hgb_c1'])])
    w2 = wide_mean(pred)
    pred = pred.assign(pos=pred.source_row.map(Wi.pos))
    rows = [(k_[0], k_[1], k_[2], strat_auc(g.y, g.prob, g.pos)) for k_, g in pred.groupby(['seed', 'strategy', 'participant'], sort=False)]
    ws = pd.DataFrame(rows, columns=['seed', 'strategy', 'participant', 'auc']).groupby(['participant', 'strategy']).auc.mean().unstack()
    T2 = [('eeg_c1', 'Todo el EEG', .681, .675), ('eeg_lento_amp', 'Potencia lenta y amplitud', .673, .659), ('eeg_frontal', 'Canales frontales', .675, .667),
          ('eeg_posterior', 'Canales posteriores', .602, .600), ('eeg_alfa_beta', 'Solo alfa y beta', .593, .593), ('gsr_c1', 'Solo GSR', .545, .547)]
    for s_, nm, a, b in T2:
        r = g2(f'AUC {s_}')
        reg(S, f'E2: AUC {nm}', a, F, float(w2[s_].mean()), 3, guardado=float(r.delta), nota=f'{int((w2[s_] > .5).sum())}/41 sobre 0,5')
        r = g2(f'AUC {s_}', 'a igual posición')
        reg(S, f'E2: AUC {nm}, a igual posición', b, F, float(ws[s_].mean()), 3, guardado=float(r.delta))
    for nm, a, b, inf in [('B7 (lento y amplitud) − (alfa y beta)', 'eeg_lento_amp', 'eeg_alfa_beta', .080), ('B8 frontales − posteriores', 'eeg_frontal', 'eeg_posterior', .073),
                          ('B3 (EEG + GSR) − solo EEG', 'hgb_c1', 'eeg_c1', .002), ('B4 solo EEG − solo GSR', 'eeg_c1', 'gsr_c1', .136)]:
        reg(S, f'E2: {nm}', inf, F, float((w2[a] - w2[b]).mean()), 3, nota=f'{int((w2[a] > w2[b]).sum())}/41')
    wc = person_auc(ctrl).set_index('participant').auc.sort_index()
    c = absol(wc)
    r = g2('control barajado − 0,5 (una partición)')
    ci_reg(S, 'E2: control con etiquetas barajadas, AUC', (.496, .482, .510), F, c, 3, guardado=(r.delta + .5, r.low95 + .5, r.high95 + .5))
    ref = pd.concat([-W[['gaze_path_length_px', 'gaze_dispersion_2d_px']].rename(columns=lambda c_: c_), W[['fixation_total_ms', 'fixation_mean_ms', 'pupil_mean_z', 'score', 'participant', 'source_row']]], axis=1)
    def rho_by_person(preds, strat, col):
        m = preds[preds.strategy.eq(strat)].groupby('source_row').prob.mean().rename('prob').reset_index().merge(ref, on='source_row')
        m = m.dropna(subset=[col])
        return m.groupby('participant').apply(lambda g: spearman(g.prob, g[col]))
    sp = {}
    for strat, col, inf, nm in [('eeg_c1', 'gaze_path_length_px', .41, 'recorrido de la mirada (invertido)'), ('eeg_c1', 'gaze_dispersion_2d_px', .30, 'dispersión (invertida)'),
                                ('eeg_c1', 'fixation_total_ms', .29, 'duración total de fijaciones'), ('eeg_c1', 'pupil_mean_z', -.09, 'pupila'),
                                ('eeg_c1', 'score', None, 'puntaje ocular'), ('eeg_alfa_beta', 'gaze_path_length_px', None, 'recorrido (invertido)')]:
        rho = rho_by_person(pred, strat, col)
        item = f"Spearman prob {strat} con {'puntaje' if col == 'score' else col}"
        reg(S, f'E2: Spearman medio por persona, prob. {strat} con {nm}', inf, F, float(rho.mean()), 2, guardado=float(g2(item).delta))
    # ---------------- E3
    F = 'INFORME enfoques E3'
    d3 = pd.read_csv(D / 'e3_descriptivos.csv').set_index('item')
    A = W.assign(ya=y_act.to_numpy())
    labd = A[A.ya.notna()]
    tab = labd.groupby('seg').agg(participant=('participant', 'first'), mean=('ya', 'mean'), labelled=('ya', 'size'))
    nties = int((tab['mean'] == .5).sum())
    tab = tab[tab['mean'] != .5].copy()
    tab['y'] = (tab['mean'] > .5).astype(int)
    reg(S, 'E3: segmentos con objetivo (sin empates)', 1589, F, len(tab), 0)
    reg(S, 'E3: segmentos excluidos por empate', 47, F, nties, 0)
    reg(S, 'E3: % de segmentos con etiqueta unánime', 79, F, float(tab['mean'].isin([0, 1]).mean()), 0, guardado=float(d3.loc['segmentos con etiqueta unánime (fracción)'].delta), escala=100)
    reg(S, 'E3: mediana de segmentos por persona', 36, F, float(tab.groupby('participant').size().median()), 0)
    reg(S, 'E3: segmentos con 3 o más ventanas etiquetadas', 1348, F, int((tab.labelled >= 3).sum()), 0)
    reg(S, 'E3: segmentos con dos o menos ventanas etiquetadas', 241, F, int((tab.labelled <= 2).sum()), 0)
    e3 = pd.concat([pd.read_csv(D / f'e3_{s}.csv.gz') for s in SEEDS])
    # la numeración de segmentos del archivo es la del script; se empareja por persona y objetivo, no por el número
    reg(S, 'E3: filas por estrategia y partición en las predicciones', 1589, F, int(e3.groupby(['seed', 'strategy']).size().iloc[0]), 0)
    old = rep('activacion', ['hgb_c1', 'hgb_c32'])
    old = old.assign(seg=old.source_row.map(Wi.seg))
    agg = old.groupby(['seed', 'strategy', 'seg']).prob.mean().reset_index().merge(tab[['participant', 'y', 'labelled']].reset_index(), on='seg')
    agg['strategy'] = agg.strategy.map({'hgb_c1': 'agg_c1', 'hgb_c32': 'agg_c32'})
    w3 = wide_mean(pd.concat([e3, agg]))
    for s_, inf in [('seg', (.587, .550, .622)), ('agg_c32', .567), ('agg_c1', .532), ('dur_only', (.535, .488, .583))]:
        r = d3.loc[f'AUC {s_}']
        ci_reg(S, f'E3: AUC {s_}', inf, F, absol(w3[s_]), 3, guardado=(r.delta, r.low95, r.high95))
    reg(S, 'E3: personas con AUC del modelo de estímulo sobre 0,5', 32, F, int((w3.seg > .5).sum()), 0)
    for nm, a, b, inf, key in [('C2 modelo de estímulo − promedio por ventana con historial', 'seg', 'agg_c32', (.020, -.007, .046), None),
                               ('modelo de estímulo − promedio por ventana sin historial', 'seg', 'agg_c1', (.054, .013, .095), 'seg − agg_c1'),
                               ('C3 (estímulo + duración) − solo duración', 'seg_dur', 'dur_only', (.048, -.014, .109), None)]:
        c = contrast(w3[a] - w3[b])
        g_ = None if key is None else (d3.loc[key].delta, d3.loc[key].low95, d3.loc[key].high95)
        ci_reg(S, f'E3: {nm}', inf, F, c, 3, guardado=g_, nota=f"{c['mejoran']}/{c['n']}; p {c['p']:.4f}")
    c = contrast(w3.seg - .5)
    ci_reg(S, 'E3: C1 modelo de estímulo − 0,5', (.087, .050, .122), F, c, 3, nota=f"p {c['p']:.5f}")
    # sensibilidad 3+: emparejar segmentos del archivo e3 con los míos por (persona, orden) no es posible sin el número;
    # se comprueba que la numeración coincide: mismo objetivo y persona por número de segmento
    mine = tab.reset_index()[['seg', 'participant', 'y']]
    j = e3[e3.seed.eq(1101) & e3.strategy.eq('seg')].merge(mine, on='seg', how='left', suffixes=('', '_m'))
    same_ids = bool((j.participant == j.participant_m).all() and (j.y == j.y_m).all())
    reg(S, 'E3: la numeración de segmentos del archivo coincide con mi reconstrucción (0 = sí)', 0, '—', 0 if same_ids else 1, 0)
    if same_ids:
        keep = set(tab.index[tab.labelled >= 3])
        both = pd.concat([e3, agg])
        w33 = wide_mean(both[both.seg.isin(keep)])
        for nm, d_, inf, key in [('estímulo − 0,5', w33.seg - .5, (.099, .062, .134), 'seg − azar (segmentos con 3+ etiquetas)'),
                                 ('estímulo − promedio por ventana', w33.seg - w33.agg_c32, (.020, -.006, .046), 'seg − agg_c32 (segmentos con 3+ etiquetas)'),
                                 ('(estímulo + duración) − solo duración', w33.seg_dur - w33.dur_only, (.054, -.005, .108), 'seg_dur − dur_only (segmentos con 3+ etiquetas)')]:
            r = d3.loc[key]
            ci_reg(S, f'E3 (3+ ventanas): {nm}', inf, F, contrast(d_), 3, guardado=(r.delta, r.low95, r.high95))
    # ---------------- E4
    F = 'INFORME enfoques E4'
    d4 = pd.read_csv(D / 'e4_descriptivos.csv').set_index(['task', 'item'])
    minholm = {}
    for task, yv in [('atencion', W.y_att), ('activacion', y_act)]:
        A = W.assign(yl=yv.to_numpy())
        base = rep(task, ['hgb_c1', 'hgb_c32'])
        w = wide_mean(base)
        gain = w.hgb_c32 - w.hgb_c1
        # (a) mitades alternadas
        segs = A.groupby('seg').agg(p=('participant', 'first'), t=('ts', 'min'), blur=('stimulus', lambda s: 'blur' in str(s.iloc[0]).lower()), nlab=('yl', 'count'))
        segs = segs[segs.nlab > 0].copy()
        segs['half'] = segs.groupby(['p', 'blur']).t.rank(method='first').astype(int) % 2
        b = base.assign(half=base.source_row.map(Wi.seg).map(segs.half))
        assert b.half.notna().all()
        w0, w1 = wide_mean(b[b.half.eq(0)]), wide_mean(b[b.half.eq(1)])
        INF = {'atencion': [(.76, .58, .86), (.64, .40, .80), (.30, -.05, .61)], 'activacion': [(.66, .44, .80), (.58, .30, .78), (.25, -.04, .51)]}[task]
        for (nm, f), inf in zip([('AUC sin historial', lambda x: x.hgb_c1), ('AUC con historial', lambda x: x.hgb_c32), ('ganancia del historial', lambda x: x.hgb_c32 - x.hgb_c1)], INF):
            jn = pd.concat([f(w0).rename('a'), f(w1).rename('b')], axis=1).dropna()
            r_ = spearman(jn.a, jn.b)
            lo, hi = spearman_boot(jn.a, jn.b)
            ref_ = d4.loc[(task, f'fiabilidad por mitades: {nm}')]
            ci_reg(S, f'E4a {task}: fiabilidad entre mitades, {nm}', inf, F, dict(delta=r_, low95=lo, high95=hi), 2, guardado=(ref_.delta, ref_.low95, ref_.high95), nota=f'n={len(jn)}')
        # (b) correlatos
        rows = []
        for person, g in A.groupby('participant'):
            l = g[g.yl.notna()]
            rows.append(dict(participant=person, ventanas_etiquetadas=len(l), cobertura_eeg=g.eeg_coverage.mean(), cobertura_pupila=g.pupil_coverage.mean(),
                             cobertura_mirada=g.gaze_coverage.mean(), deriva_sesion=abs(auc(l.yl, l.ts) - .5),
                             largo_medio_segmento=g.groupby('seg').size().mean(), duracion_sesion=g.ts.max()))
        cov = pd.DataFrame(rows).set_index('participant')
        dmax = 0.
        for outcome, v in [('AUC sin historial', w.hgb_c1), ('ganancia del historial', gain)]:
            ps, rs = [], []
            for c_ in cov.columns:
                jn = pd.concat([v.rename('v'), cov[c_]], axis=1).dropna()
                r_ = spearman(jn.v, jn[c_])
                rs.append(r_)
                ps.append(spearman_p(r_, len(jn)))
                ref_ = d4.loc[(task, f'{outcome} ~ {c_}')]
                dmax = max(dmax, abs(r_ - ref_.delta), abs(ps[-1] - ref_.p))
            hp = holm(ps)
            dmax = max(dmax, max(abs(h - d4.loc[(task, f'{outcome} ~ {c_}')].p_holm) for h, c_ in zip(hp, cov.columns)))
            minholm[(task, outcome)] = float(hp.min())
        reg(S, f'E4b {task}: diferencia máxima con e4_descriptivos.csv (14 correlaciones, p y p Holm)', 0, 'e4_descriptivos.csv', dmax, 9, veredicto='coincide' if dmax < 1e-9 else 'difiere')
        # (c) adaptación
        new = pd.concat([pd.read_csv(D / f'e4_{task}_{s}.csv.gz') for s in SEEDS])
        glob = base.merge(new[['seed', 'source_row']].drop_duplicates(), on=['seed', 'source_row'])
        assert len(glob) == len(new)
        wp = wide_mean(pd.concat([new, glob])).dropna()
        if task == 'activacion':
            reg(S, 'E4c activación: personas con evaluación', 40, F, len(wp), 0)
            for s_, inf, nm in [('hgb_c1', .502, 'general sin historial'), ('pers_c1', .530, 'adaptado sin historial'), ('hgb_c32', .543, 'general con historial'), ('pers_c32', .587, 'adaptado con historial')]:
                reg(S, f'E4c activación: AUC {nm} en la parte final de la sesión', inf, F, float(wp[s_].mean()), 3, guardado=float(d4.loc[(task, f'AUC {s_}')].delta))
            c = contrast(wp.pers_c32 - wp.pers_c1)
            r_ = d4.loc[(task, 'pers_c32 − pers_c1')]
            ci_reg(S, 'E4c activación: historial en el modelo adaptado (adaptado con − adaptado sin)', (.058, .032, .084), F, c, 3, guardado=(r_.delta, r_.low95, r_.high95), nota=f"{c['mejoran']}/{c['n']}")
            for a_, b_, inf in [('pers_c1', 'hgb_c1', (.028, .007, .049)), ('pers_c32', 'hgb_c32', (.045, .023, .069))]:
                c = contrast(wp[a_] - wp[b_])
                ci_reg(S, f'E4c activación: {a_} − {b_}', inf, F, c, 3, nota=f"{c['mejoran']}/{c['n']}; p sin ajuste {c['p']:.6f}")
            c = contrast(wp.hgb_c32 - wp.hgb_c1)
            r_ = d4.loc[(task, 'hgb_c32 − hgb_c1 (mismas filas)')]
            ci_reg(S, 'E4c activación: historial en el modelo general, mismas filas', None, 'e4_descriptivos.csv', c, 3, guardado=(r_.delta, None, None), with_ci=False)
            reg(S, 'E4c activación: AUC "de 0,50 a 0,59" (extremos)', .59, F, float(wp.pers_c32.mean()), 2)
        else:
            for a_, b_, inf in [('pers_c1', 'hgb_c1', (.006, .000, .011)), ('pers_c32', 'hgb_c32', (.000, -.007, .008))]:
                c = contrast(wp[a_] - wp[b_])
                ci_reg(S, f'E4c atención: {a_} − {b_}', inf, F, c, 3, nota=f"{c['mejoran']}/{c['n']}")
        first = new[new.seed.eq(1101) & new.strategy.eq('pers_c1')]
        frac = first.source_row.map(Wi.ts) / first.participant.map(W.groupby('participant').ts.max())
        reg(S, f'E4c {task}: fracción mínima de sesión de una fila de evaluación', .40, 'AUDITORIA_RESULTADOS enfoques ("ninguna anterior al 40 %")', float(frac.min()), 2,
            veredicto='coincide' if frac.min() > .40 else 'difiere')
    reg(S, 'E4b: p Holm mínimo entre todos los correlatos', .23, F + ' ("todos los p Holm ≥ 0,23")', min(minholm.values()), 2)


# ================================================================== 3. Reapertura (fases 1, 2 y 3)
def drop_influential(d):
    d = pd.Series(d).dropna()
    i = (d - d.mean()).abs().idxmax()
    r = d.drop(i).to_numpy()
    lo, hi = boot(r)
    return dict(persona=i, delta_persona=float(d[i]), delta=float(r.mean()), low95=lo, high95=hi, p=signflip(r), mediana=float(d.median()),
                mejoran=int((d > 0).sum()), n=len(d), media=float(d.mean()))


def band_counts(W, lags=(6, 12, 24, 48, 96), band=6, gap=150):
    """Por ventana: nº de ventanas de la misma persona con inicio en [t−L−6, t−L), y tamaño del conjunto a ≥150 s."""
    n = {L: np.zeros(len(W), int) for L in lags}
    same = {L: np.zeros(len(W), int) for L in lags}
    pool = np.zeros(len(W), int)
    t_all, seg_all = W.t.to_numpy(), W.seg.to_numpy()
    for _, ix in W.groupby('participant').indices.items():
        o = ix[np.argsort(t_all[ix], kind='stable')]
        tt, sg = t_all[o], seg_all[o]
        for L in lags:
            lo = np.searchsorted(tt, tt - L - band, side='left')
            hi = np.searchsorted(tt, tt - L, side='left')
            n[L][o] = hi - lo
            same[L][o] = [int((sg[a:b] == sg[j]).sum()) for j, (a, b) in enumerate(zip(lo, hi))]
        far = np.searchsorted(tt, tt - gap, side='right') + (len(tt) - np.searchsorted(tt, tt + gap, side='left'))
        pool[o] = far
    return n, same, pool


def sec_reapertura(W, y_act):
    S = '3 Reapertura'
    D1, D2_, D3 = RES / 'reapertura_41p_22-11-2026', RES / 'reapertura_fase2_41p_22-11-2026', RES / 'reapertura_fase3_41p_22-11-2026'
    F = 'INFORME reapertura'
    Wi = W.set_index('source_row')
    desc = pd.read_csv(D1 / 'descriptivos.csv').set_index(['task', 'item'])
    absc = pd.read_csv(D1 / 'auc_absolutas.csv').set_index(['task', 'strategy'])
    d2 = pd.read_csv(D2_ / 'descriptivos.csv').set_index(['task', 'item'])
    x2 = pd.read_csv(D2_ / 'x2_estratificada.csv').set_index(['task', 'strata'])
    d3 = pd.read_csv(D3 / 'descriptivos.csv').set_index(['task', 'scope', 'item'])
    c3 = pd.read_csv(D3 / 'confirmatorio.csv').set_index(['task', 'test'])
    n, same, pool = band_counts(W)
    INF = dict(
        atencion=dict(d2=(.535, .519, .552), pairs=8818, people=41, abs=(.683, .712), common=12613, pct=57,
                      ts=(.025, .019, .032), slope=(-.002, None, None), slope_p=.071, slope_n=None, p1=(.028, .030)),
        activacion=dict(d2=(.680, .634, .724), pairs=5035, people=40, abs=(.518, .554), common=6268, pct=53,
                        ts=(.019, -.023, .061), slope=(-.010, -.018, -.003), slope_p=.009, slope_n=27, p1=(.028, .047)))
    MATCH = {}
    for task, yv in [('atencion', W.y_att), ('activacion', y_act)]:
        I = INF[task]
        A = W.assign(yl=yv.to_numpy())
        L = A[A.yl.notna()].copy()
        # ---- D2 persistencia de la etiqueta a 6 s dentro del mismo estímulo
        prev = L[['seg', 't', 'yl']].rename(columns={'yl': 'y_prev'})
        prev['t'] = prev.t + 6
        m = pd.merge_asof(L.sort_values('t'), prev.sort_values('t'), on='t', by='seg', tolerance=1e-3, direction='nearest').dropna(subset=['y_prev'])
        ac = pd.Series({q: auc(g.yl, g.y_prev) for q, g in m.groupby('participant')}).dropna()
        r = desc.loc[(task, 'D2 AUC de la etiqueta 6 s antes')]
        ci_reg(S, f'D2 {task}: AUC de la etiqueta 6 s antes en el mismo estímulo', I['d2'], F, absol(ac), 3, guardado=(r.delta, r.low95, r.high95))
        reg(S, f'D2 {task}: pares', I['pairs'], F, len(m), 0, guardado=float(r.rows))
        reg(S, f'D2 {task}: personas', I['people'], F, len(ac), 0)
        # ---- familia confirmatoria: AUC absolutas, por partición, tiempo de sesión
        R = rep(task)
        pa = person_auc(R[R.strategy.isin(['hgb_c1', 'hgb_c32', 'c1_ts', 'c32_ts'])], ('seed',))
        w = pa.groupby(['participant', 'strategy']).auc.mean().unstack()
        for s_, inf in zip(['hgb_c1', 'hgb_c32'], I['abs']):
            reg(S, f'{task}: AUC absoluta {s_} (5 particiones)', inf, F, float(w[s_].mean()), 3, guardado=float(absc.loc[(task, s_)].auc))
        for s_ in ['c1_ts', 'c32_ts']:
            reg(S, f'{task}: AUC absoluta {s_}', None, 'auc_absolutas.csv', float(w[s_].mean()), guardado=float(absc.loc[(task, s_)].auc),
                veredicto='coincide' if abs(w[s_].mean() - absc.loc[(task, s_)].auc) < 1e-9 else 'difiere')
        per = {sd: (g.pivot(index='participant', columns='strategy', values='auc')) for sd, g in pa.groupby('seed')}
        p1 = [float((x.hgb_c32 - x.hgb_c1).mean()) for x in per.values()]
        reg(S, f'{task}: P1 por partición, mínimo', I['p1'][0], F, min(p1), 3, nota='por partición: ' + '; '.join(f'{v:.6f}' for v in p1))
        reg(S, f'{task}: P1 por partición, máximo', I['p1'][1], F, max(p1), 3)
        c = contrast(w.c1_ts - w.hgb_c1)
        r = desc.loc[(task, 'c1_ts − hgb_c1 (tiempo de sesión solo)')]
        ci_reg(S, f'{task}: tiempo de sesión solo (c1_ts − hgb_c1)', I['ts'], F, c, 3, guardado=(r.delta, r.low95, r.high95))
        # ---- cobertura de la curva (reconstrucción propia desde la tabla de ventanas)
        k6 = n[6]
        ok = np.all([n[Lg] >= 3 for Lg in n], axis=0) & (pool >= k6) & (k6 >= 3)
        common = A.source_row[ok & A.yl.notna().to_numpy()]
        lag = pd.read_csv(D1 / f'lag_{task}.csv.gz')
        saved = set(lag[lag.strategy.eq('placebo')].source_row)
        reg(S, f'Curva {task}: filas con cobertura completa (reconstrucción propia)', I['common'], F, len(common), 0)
        reg(S, f'Curva {task}: filas reconstruidas que no están en las predicciones guardadas, o al revés', 0, '—', len(set(common) ^ saved), 0)
        reg(S, f'Curva {task}: personas con filas comunes', I['people'], F, int(Wi.participant.loc[list(saved)].nunique()), 0)
        reg(S, f'Curva {task}: % de las filas etiquetadas', I['pct'], F, len(saved) / len(L), 0, escala=100)
        reg(S, f'Curva {task}: mínimo de filas comunes por persona', {'atencion': 149, 'activacion': 62}[task], f'cobertura_{task}.json',
            int(Wi.participant.loc[list(saved)].value_counts().min()), 0)
        okrow = ok & A.yl.notna().to_numpy()
        for Lg, inf in zip([6, 12, 24, 48, 96], [73, 48, 13, 0, 0] if task == 'activacion' else [None] * 5):
            reg(S, f'Curva {task}: % de las ventanas de la banda de {Lg} s que son del mismo estímulo', inf, F + ', límites',
                float(same[Lg][okrow].sum() / n[Lg][okrow].sum()), 0, escala=100)
        for Lg in [12, 24, 48, 96]:
            MATCH[(task, Lg)] = float((n[Lg][okrow] == k6[okrow]).mean())
        # ---- curva: tendencia y AUC
        blk = pd.read_csv(D2_ / f'bloque_{task}.csv.gz')
        wl = person_auc(pd.concat([lag, blk])).pivot(index='participant', columns='strategy', values='auc').sort_index()
        Dm = np.column_stack([(wl[f'lag{Lg}'] - wl.placebo).to_numpy() for Lg in [6, 12, 24, 48, 96]])
        keep = ~np.isnan(Dm).any(axis=1)
        x = np.log2([6, 12, 24, 48, 96]); x = x - x.mean()
        slope = (Dm[keep] * x).sum(axis=1) / (x ** 2).sum()
        r = desc.loc[(task, 'pendiente de (lagL − placebo) por duplicación del desfase')]
        lo, hi = boot(slope)
        ci_reg(S, f'Curva {task}: pendiente del contraste por duplicación del desfase', I['slope'], F, dict(delta=float(slope.mean()), low95=lo, high95=hi), 3,
               guardado=(r.delta, r.low95, r.high95))
        reg(S, f'Curva {task}: p de la pendiente', I['slope_p'], F, signflip(slope), 3, guardado=float(r.p))
        if I['slope_n']:
            reg(S, f'Curva {task}: personas con pendiente negativa', I['slope_n'], F, int((slope < 0).sum()), 0, nota=f'de {int(keep.sum())}')
        for s_ in wl.columns:
            if s_ == 'placebo_bloque':
                continue
            reg(S, f'Curva {task}: AUC absoluta {s_}', None, 'auc_absolutas.csv', float(wl[s_].mean()), guardado=float(absc.loc[(task, f'curva:{s_}')].auc),
                veredicto='coincide' if abs(wl[s_].mean() - absc.loc[(task, f'curva:{s_}')].auc) < 1e-9 else 'difiere')
        if task == 'activacion':
            c = contrast(wl.placebo - wl.c1_common)
            ci_reg(S, 'Curva activación: placebo − ventana actual', (.009, -.024, .043), F, c, 3)
            c = contrast(wl.lag6 - wl.placebo)
            ci_reg(S, 'Curva activación: 6 s − placebo', (.047, .017, .078), 'Cierre (el INFORME dice +0,018)', c, 3, nota=f"{c['mejoran']}/{c['n']}; mediana {c['mediana']:.4f}")
            reg(S, 'Curva activación: 6 s − placebo, mediana', .042, F + ', sensibilidad', c['mediana'], 3)
            reg(S, 'Curva activación: 6 s − placebo, personas a favor', 30, F, c['mejoran'], 0)
            for nm, a_, b_, inf in [('6 s − placebo', 'lag6', 'placebo', (.039, .012, .065)), ('6 s − placebo de bloque', 'lag6', 'placebo_bloque', (.046, .021, .070))]:
                di = drop_influential(wl[a_] - wl[b_])
                ci_reg(S, f'Sensibilidad activación: {nm}, sin la persona más influyente', inf, F, di, 3, nota=f"persona {di['persona']} ({di['delta_persona']:+.3f}); p {di['p']:.4f}")
            c = contrast(wl.lag6 - wl.placebo_bloque)
            reg(S, 'X1 activación: 6 s − placebo de bloque, mediana', .056, F, c['mediana'], 3, nota=f"media {c['delta']:.6f}; {c['mejoran']}/{c['n']}")
        c = contrast(wl.placebo_bloque - wl.placebo)
        reg(S, f'X1 {task}: placebo de bloque − placebo disperso', {'atencion': -.001, 'activacion': -.006}[task], F, c['delta'], 3,
            guardado=float(d2.loc[(task, 'placebo_bloque − placebo disperso')].delta))
        # ---- AUC estratificadas (5 particiones) con las cuatro estrategias + posición (fase 3)
        P3 = pd.concat([pd.read_csv(D3 / f'pos_{task}_{sd}.csv.gz') for sd in SEEDS])
        allp = pd.concat([R[R.strategy.isin(['hgb_c1', 'hgb_c32'])], P3])
        allp = allp.assign(estimulo=allp.source_row.map(Wi.seg), bloque60=(allp.source_row.map(Wi.ts) // 60).astype(int), posicion=allp.source_row.map(Wi.pos))
        wides = {'todas': wide_mean(allp)}
        for col in ['estimulo', 'bloque60', 'posicion']:
            rows = [(*k_, strat_auc(g.y, g.prob, g[col])) for k_, g in allp.groupby(['seed', 'strategy', 'participant'], sort=False)]
            wides[col] = pd.DataFrame(rows, columns=['seed', 'strategy', 'participant', 'auc']).groupby(['participant', 'strategy']).auc.mean().unstack()
        X2I = dict(atencion=dict(estimulo=(.013, .007, .021), bloque60=(.023, .016, .030), posicion=(.017, .010, .024)),
                   activacion=dict(estimulo=(.054, .015, .094), bloque60=(.058, .027, .092), posicion=(.027, -.003, .059)))[task]
        nm_ = dict(estimulo='mismo estímulo', bloque60='mismo minuto', posicion='misma posición')
        for col in ['estimulo', 'bloque60', 'posicion']:
            wv = wides[col]
            c = contrast(wv.hgb_c32 - wv.hgb_c1)
            r = x2.loc[(task, col)]
            ci_reg(S, f'X2 {task}: historial − sin historial, {nm_[col]}', X2I[col], F, c, 3, guardado=(r.delta, r.low95, r.high95), nota=f"{c['mejoran']}/{c['n']}; p {c['p']:.6f}")
            for s_ in ['hgb_c1', 'hgb_c32']:
                inf = {('activacion', 'estimulo', 'hgb_c1'): .501, ('activacion', 'bloque60', 'hgb_c1'): .501, ('activacion', 'estimulo', 'hgb_c32'): .555,
                       ('activacion', 'bloque60', 'hgb_c32'): .560, ('atencion', 'posicion', 'hgb_c1'): .677 if False else None}.get((task, col, s_))
                reg(S, f'X2 {task}: AUC estratificada {s_}, {nm_[col]}', inf, F, float(wv[s_].mean()), 3, guardado=float(d2.loc[(task, f'{col}: AUC estratificada {s_}')].delta),
                    veredicto=None if inf is not None else ('coincide' if abs(wv[s_].mean() - d2.loc[(task, f'{col}: AUC estratificada {s_}')].delta) < 1e-9 else 'difiere'))
            one = R[R.seed.eq(1101) & R.strategy.eq('hgb_c1')]
            strat = {'estimulo': one.source_row.map(Wi.seg), 'bloque60': (one.source_row.map(Wi.ts) // 60).astype(int), 'posicion': one.source_row.map(Wi.pos)}[col]
            sh = []
            for q, g in one.assign(st=strat.to_numpy()).groupby('participant'):
                tot = int(g.y.sum()) * int((1 - g.y).sum())
                sh.append(sum(int(h.y.sum()) * int((1 - h.y).sum()) for _, h in g.groupby('st')) / tot)
            reg(S, f'X2 {task}: % de pares dentro de {nm_[col]}', {'estimulo': {'atencion': 2, 'activacion': 3}[task], 'bloque60': 7, 'posicion': None}[col],
                F + ' ("2–3 %" y "7 %")', float(np.mean(sh)), 0, guardado=float(d2.loc[(task, f'{col}: fracción de pares dentro del estrato')].delta), escala=100)
        # ---- D1
        first = R[R.seed.eq(1101)]
        po = person_auc(first[first.strategy.eq('pos_only')]).set_index('participant').auc.sort_index()
        r = desc.loc[(task, 'D1 AUC solo posición en el estímulo')]
        ci_reg(S, f'D1 {task}: AUC de la posición sola', {'atencion': (.598, .581, .614), 'activacion': (.543, .492, .595)}[task], F, absol(po), 3, guardado=(r.delta, r.low95, r.high95))
        if task == 'atencion':
            c1 = first[first.strategy.eq('hgb_c1')]
            st = pd.Series({q: strat_auc(g.y, g.prob, g.source_row.map(Wi.pos)) for q, g in c1.groupby('participant')}).sort_index()
            r = desc.loc[(task, 'D1 AUC sin historial, estratificada por posición')]
            ci_reg(S, 'D1 atención: AUC sin historial entre ventanas de la misma posición (partición 1101)', (.677, .655, .699), F, absol(st), 3, guardado=(r.delta, r.low95, r.high95))
            un = person_auc(c1).auc
            reg(S, 'D1 atención: AUC sin historial sin estratificar (partición 1101)', .684, F, float(un.mean()), 3)
        # ---- sensibilidades (fase 1 y 2)
        if task == 'activacion':
            for nm, d_, inf, med, mej in [('P1 historial − sin historial', w.hgb_c32 - w.hgb_c1, (.028, .006, .050), .014, 23),
                                          ('mismo minuto', wides['bloque60'].hgb_c32 - wides['bloque60'].hgb_c1, (.050, .021, .081), .042, 24),
                                          ('mismo estímulo', wides['estimulo'].hgb_c32 - wides['estimulo'].hgb_c1, (.044, .009, .080), .052, 26)]:
                di = drop_influential(d_)
                ci_reg(S, f'Sensibilidad activación: {nm}, sin la persona más influyente', inf, F + ' / AUDITORIA_RESULTADOS', di, 3,
                       nota=f"persona {di['persona']} ({di['delta_persona']:+.3f}); p {di['p']:.4f}")
                reg(S, f'Sensibilidad activación: {nm}, mediana', med, F, di['mediana'], 3)
                reg(S, f'Sensibilidad activación: {nm}, personas a favor', mej, F, di['mejoran'], 0)
            d_ = (w.hgb_c32 - w.hgb_c1)
            reg(S, 'P1 activación: aporte de P4 a la media (0,009 de 0,036)', .009, F, float(d_['P4'] / len(d_)), 3, nota=f"delta de P4 {d_['P4']:+.4f}")
            reg(S, 'P1 activación: media', .036, F, float(d_.mean()), 3)
        # ---- fase 3
        F3 = 'INFORME fase 3'
        T3 = dict(atencion=dict(hgb_c1=(.683,), pos_c1=(.711,), hgb_c32=(.712,), c32_pos=(.713,)),
                  activacion=dict(hgb_c1=(.518, .501), pos_c1=(.523, .550), hgb_c32=(.554, .555), c32_pos=(.555, .559)))[task]
        for s_, inf in T3.items():
            reg(S, f'Fase 3 {task}: AUC {s_}', inf[0], F3, float(wides['todas'][s_].mean()), 3, guardado=float(d3.loc[(task, 'todas', f'AUC {s_}')].delta))
            if len(inf) > 1:
                reg(S, f'Fase 3 {task}: AUC {s_}, mismo estímulo', inf[1], F3, float(wides['estimulo'][s_].mean()), 3, guardado=float(d3.loc[(task, 'estimulo', f'AUC {s_}')].delta))
        C3 = dict(atencion=[('todas', 'pos_c1', 'hgb_c1', (.028, .021, .036)), ('todas', 'hgb_c32', 'pos_c1', (.001, -.003, .004)),
                            ('bloque60', 'c32_pos', 'pos_c1', (-.000, -.004, .003)), ('posicion', 'c32_pos', 'pos_c1', (.005, .001, .010))],
                  activacion=[('todas', 'pos_c1', 'hgb_c1', (.006, -.015, .026)), ('todas', 'hgb_c32', 'pos_c1', (.031, .004, .057)),
                              ('estimulo', 'pos_c1', 'hgb_c1', (.049, .027, .072)), ('estimulo', 'hgb_c32', 'pos_c1', (.005, -.026, .035)),
                              ('bloque60', 'c32_pos', 'pos_c1', (.033, .005, .062)), ('posicion', 'c32_pos', 'pos_c1', (.026, -.000, .052))])[task]
        for scope, a_, b_, inf in C3:
            c = contrast(wides[scope][a_] - wides[scope][b_])
            r = d3.loc[(task, scope, f'{a_} − {b_}')]
            ci_reg(S, f'Fase 3 {task}: {a_} − {b_} ({scope})', inf, F3, c, 3, guardado=(r.delta, r.low95, r.high95))
        Q = dict(atencion=[('Q1', 'todas', .001, .001, 'P36', (.001, -.002, .003)), ('Q2', 'estimulo', -.000, .001, 'P46', (.001, -.002, .003))],
                 activacion=[('Q1', 'todas', .032, .031, 'P10', (.039, .015, .063)), ('Q2', 'estimulo', .009, -.001, 'P44', (.015, -.012, .042))])[task]
        for q_, scope, dq, med, who, inf in Q:
            d_ = wides[scope].c32_pos - wides[scope].pos_c1
            di = drop_influential(d_)
            r = c3.loc[(task, q_)]
            reg(S, f'Fase 3 {task} {q_}: delta', dq, F3, di['media'], 3, guardado=float(r.delta))
            reg(S, f'Fase 3 {task} {q_}: mediana', med, F3, di['mediana'], 3, guardado=float(r['median']))
            reg(S, f'Fase 3 {task} {q_}: persona más influyente es {who} (0 = sí)', 0, F3, 0 if di['persona'] == who else 1, 0, nota=f"{di['persona']} ({di['delta_persona']:+.3f})")
            ci_reg(S, f'Fase 3 {task} {q_}: sin la persona más influyente', inf, F3, di, 3, guardado=(r.delta_without, r.low95_without, r.high95_without), nota=f"p {di['p']:.4f}")
    det = '; '.join(f'{k_[0]} {k_[1]} s {v:.4f}' for k_, v in MATCH.items())
    reg(S, 'Curva: % de filas en que el placebo iguala el nº de ventanas de la banda, mínimo (bandas 12–96 s, ambas tareas)', 30, F + ', límites ("30–44 %")', min(MATCH.values()), 0, escala=100, nota=det)
    reg(S, 'Curva: ídem, máximo', 44, F + ', límites ("30–44 %")', max(MATCH.values()), 0, escala=100)
    # P4: pares dentro del mismo estímulo
    L = W[y_act.notna().to_numpy() & (W.participant == 'P4').to_numpy()].assign(yl=y_act[y_act.notna().to_numpy() & (W.participant == 'P4').to_numpy()].to_numpy())
    reg(S, 'P4: pares positivo-negativo dentro del mismo estímulo en activación', 4, 'INFORME fase 3, auditorías',
        int(sum(int(h.yl.sum()) * int((1 - h.yl).sum()) for _, h in L.groupby('seg'))), 0)


# ================================================================== crudos (solo lectura)
FS = 125.
EEGNAMES = ['Fp1', 'Fp2', 'C3', 'C4', 'P7', 'P8', 'O1', 'O2', 'F7', 'F8', 'F3', 'F4', 'T7', 'T8', 'P3', 'P4']


def raw_person(p):
    from scipy.signal import butter, sosfiltfilt
    d = np.load(LOCAL / 'cache_ocular' / f'{p}.npz')
    t, x, gt = d['eeg_t'], d['eeg'], d['gaze_t']
    ins = (t >= gt[0]) & (t <= gt[-1])
    t, x = t[ins], x[ins]
    good = (np.isfinite(x).mean(0) >= .95) & ((np.abs(x) >= 180000).mean(0) <= .01) & ((np.abs(np.diff(x, axis=0)) < 1e-12).mean(0) < .99)
    inv = d['both_invalid'].astype(int)
    edge = np.diff(np.r_[0, inv, 0])
    a, b = np.flatnonzero(edge == 1), np.flatnonzero(edge == -1) - 1
    dur = gt[b] - gt[a]
    k = (dur >= .05) & (dur <= .5)
    on, dur = gt[a][k], dur[k]
    blink = np.zeros(len(gt))
    for o_, w_ in zip(on, dur):
        blink[np.searchsorted(gt, o_, 'left'):np.searchsorted(gt, o_ + w_, 'right')] = 1
    ok = np.isfinite(d['gaze_x']) & np.isfinite(d['gaze_y'])
    sos15 = butter(2, [1, 15], btype='bandpass', fs=FS, output='sos')
    ref = sosfiltfilt(sos15, np.column_stack([np.interp(t, gt[ok], d['gaze_x'][ok]), np.interp(t, gt[ok], d['gaze_y'][ok]), np.interp(t, gt, blink)]), axis=0)
    return dict(t=t, x=x, good=good, onsets=on, ref=ref, sos15=sos15)


def lagcorr(ref, x, lag):
    a = ref[max(0, -lag):len(ref) - max(0, lag)]
    b = x[max(0, lag):len(x) - max(0, -lag)]
    a = (a - a.mean()) / (a.std() + 1e-12)
    b = (b - b.mean(0)) / (b.std(0) + 1e-12)
    return (a[:, None] * b).mean(0)


def blink_erp_ptp(t, y, onsets, lag_s):
    idx = np.searchsorted(t, onsets + lag_s)
    pre, post = int(.3 * FS), int(.7 * FS)
    idx = idx[(idx > pre) & (idx < len(t) - post)]
    if not len(idx):
        return np.full(y.shape[1], np.nan), 0
    return np.ptp(np.mean([y[i - pre:i + post] for i in idx], axis=0), axis=0), len(idx)


def sample_people():
    people = sorted(pd.read_csv(PARTS).query("split in ['train','validation','test']").participant)
    return sorted(np.random.default_rng(20261127).choice(people, 5, replace=False).tolist()), people


# ================================================================== 6. Montaje
def sec_montaje():
    from scipy.signal import sosfiltfilt
    S = '6 Montaje'
    D = RES / 'montaje_ocular_41p_23-11-2026'
    F = 'INFORME montaje'
    pe, ch, rc = pd.read_csv(D / 'personas.csv'), pd.read_csv(D / 'canales_por_persona.csv'), pd.read_csv(D / 'resumen_canales.csv').set_index('channel')
    lag = pe.lag_parpadeo_s
    reg(S, 'Desfase EEG–seguidor ocular (parpadeo): mínimo, s', .18, F, float(lag.min()), 2)
    reg(S, 'Desfase: máximo, s', .53, F, float(lag.max()), 2)
    reg(S, 'Desfase: mediana, s', .45, F, float(lag.median()), 2)
    reg(S, 'Desfase: cuartil inferior, s', .28, F, float(lag.quantile(.25)), 2)
    reg(S, 'Desfase: cuartil superior, s', .48, F, float(lag.quantile(.75)), 2)
    reg(S, 'Personas con desfase positivo (parpadeo)', 41, F, int((lag > 0).sum()), 0)
    reg(S, 'Personas con desfase positivo (mirada horizontal)', 41, 'Auditoría 23-11, M9', int((pe.lag_horizontal_s > 0).sum()), 0)
    reg(S, 'Personas con desfase no positivo (mirada vertical)', 4, 'Auditoría 23-11, M9', int((pe.lag_vertical_s <= 0).sum()), 0, nota=f'mínimo {pe.lag_vertical_s.min():.3f} s')
    reg(S, 'Desfase como % de la ventana de 2 s: mínimo', 9, 'Borradores ("9–26 %"); el INFORME dice 12 %', float(lag.min() / 2), 0, escala=100)
    reg(S, 'Desfase como % de la ventana de 2 s: máximo', 26, 'Borradores ("9–26 %"); el INFORME dice 25 %', float(lag.max() / 2), 0, escala=100)
    reg(S, 'Desfase como % de la ventana de 2 s: mediana', 22, 'Borradores', float(lag.median() / 2), 0, escala=100)
    reg(S, 'INFORME montaje: "entre un 12 % y un 25 %" — mínimo', 12, F, float(lag.min() / 2), 0, escala=100)
    reg(S, 'INFORME montaje: "entre un 12 % y un 25 %" — máximo', 25, F, float(lag.max() / 2), 0, escala=100)
    # dos grupos de desfase
    num = pe.participant.str[1:].astype(int)
    g1 = ((num >= 2) & (num <= 21)) | num.isin([36, 37])
    lo_, hi_ = lag[g1], lag[~g1]
    reg(S, 'Grupo 1 (P2 a P21, P36, P37): mediana del desfase, s', .27, F + '; cierre', float(lo_.median()), 2, nota=f'n={len(lo_)}; rango {lo_.min():.3f}–{lo_.max():.3f}; media {lo_.mean():.4f}')
    reg(S, 'Grupo 2 (resto): mediana del desfase, s', .47, F + '; cierre', float(hi_.median()), 2, nota=f'n={len(hi_)}; rango {hi_.min():.3f}–{hi_.max():.3f}; media {hi_.mean():.4f}')
    reg(S, 'Separación limpia entre grupos (0 = el máximo del grupo 1 es menor que el mínimo del grupo 2)', 0, F, 0 if lo_.max() < hi_.min() else 1, 0)
    # amplitud del parpadeo por canal
    med = ch.groupby('channel').blink_ptp_uv.median()
    for c_, inf in [(0, 148), (1, 151), (8, 74), (9, 77), (10, 57), (11, 56)]:
        reg(S, f'Amplitud del parpadeo, canal {c_} ({EEGNAMES[c_]}), mediana µV', inf, F, float(med[c_]), 0, guardado=float(rc.blink_ptp_uv_median[c_]))
    reg(S, 'Central y temporal (2, 3, 12, 13): mínimo µV', 25, F, float(med[[2, 3, 12, 13]].min()), 0)
    reg(S, 'Central y temporal: máximo µV', 29, F, float(med[[2, 3, 12, 13]].max()), 0)
    reg(S, 'Parietal y occipital (4–7, 14, 15): mínimo µV', 18, F, float(med[[4, 5, 6, 7, 14, 15]].min()), 0)
    reg(S, 'Parietal y occipital: máximo µV', 24, F, float(med[[4, 5, 6, 7, 14, 15]].max()), 0)
    reg(S, 'Frontopolar "unos 150 µV": media de Fp1 y Fp2', 150, 'Borradores', float(med[[0, 1]].mean()), 0)
    reg(S, 'Posterior "unos 20 µV": mediana de las 6 medianas posteriores', 20, 'Borradores', float(med[[4, 5, 6, 7, 14, 15]].median()), 0)
    top = ch[ch.usable].sort_values('blink_ptp_uv', ascending=False).groupby('participant').head(1)
    reg(S, 'Personas cuyo canal de mayor respuesta al parpadeo es 0 o 1', 27, F, int(top.channel.isin([0, 1]).sum()), 0)
    wide = ch.pivot(index='participant', columns='channel', values='r_horizontal')[[8, 9]].dropna()
    reg(S, 'Personas con F7 y F8 utilizables', 37, F, len(wide), 0)
    reg(S, 'Personas con signo opuesto de la mirada horizontal en F7 y F8', 31, F, int((np.sign(wide[8]) != np.sign(wide[9])).sum()), 0)
    rh = ch.assign(a=ch.r_horizontal.abs()).groupby('channel').a.median().sort_values(ascending=False)
    reg(S, 'Canales con mayor acoplamiento horizontal son 9, 13, 5 y 3 (0 = sí)', 0, F, 0 if list(rh.index[:4]) == [9, 13, 5, 3] else 1, 0, nota=str(list(rh.index[:4])))
    reg(S, 'Canales utilizables por persona: mínimo', 11, F, int(pe.usable_channels.min()), 0)
    reg(S, 'Canales utilizables por persona: máximo', 16, F, int(pe.usable_channels.max()), 0)
    reg(S, 'Canales utilizables por persona: mediana', 15, F, float(pe.usable_channels.median()), 0)
    worst = ch.groupby('name_default').usable.sum().sort_values().index[:4].tolist()
    reg(S, 'Canales con más pérdidas son P4, O1, P7 y P3 (0 = sí)', 0, F, 0 if set(worst) == {'P4', 'O1', 'P7', 'P3'} else 1, 0, nota=str(worst))
    reg(S, 'Parpadeos detectados por persona: mínimo', 19, F, int(pe.blinks.min()), 0)
    reg(S, 'Parpadeos detectados por persona: máximo', 393, F, int(pe.blinks.max()), 0)
    reg(S, 'Frecuencia de muestreo efectiva, Hz', 125.1, F, float(pe.fs_effective.median()), 1, nota=f'rango {pe.fs_effective.min():.3f}–{pe.fs_effective.max():.3f}')
    reg(S, 'Mayor hueco entre muestras, s', .19, F, float(pe.max_gap_s.max()), 2)
    reg(S, 'Correlación máxima más baja entre personas (parpadeo) — "cercana a 0,1"', .1, F, float(pe.maxabs_r_parpadeo.min()), 1)
    # ---- desde los crudos: las 41 personas (y detalle de 5 elegidas con semilla fija)
    five, people = sample_people()
    say('   personas elegidas para el detalle (semilla 20261127):', five)
    LAGS = np.arange(-125, 126)
    rows, prow = [], []
    for p in people:
        r = raw_person(p)
        xf = sosfiltfilt(r['sos15'], np.nan_to_num(r['x']), axis=0)
        best = {}
        for j, nm in enumerate(['horizontal', 'vertical', 'parpadeo']):
            cc = np.array([lagcorr(r['ref'][:, j], xf, int(Lg)) for Lg in LAGS])
            cc[:, ~r['good']] = 0
            i = np.abs(cc).max(1).argmax()
            best[nm] = (float(LAGS[i] / FS), cc[i])
        amp, nb = blink_erp_ptp(r['t'], xf, r['onsets'], best['parpadeo'][0])
        g = r['good']
        prow.append(dict(participant=p, usable=int(g.sum()), blinks=nb, lag=best['parpadeo'][0], lag_h=best['horizontal'][0], lag_v=best['vertical'][0]))
        for c_ in range(16):
            rows.append(dict(participant=p, channel=c_, usable=bool(g[c_]), amp=float(amp[c_]) if g[c_] else np.nan,
                             rh=float(best['horizontal'][1][c_]) if g[c_] else np.nan))
    RP, RC = pd.DataFrame(prow).set_index('participant'), pd.DataFrame(rows)
    pe_i = pe.set_index('participant').loc[RP.index]
    j = RC.merge(ch, on=['participant', 'channel'])
    FR = 'crudos en caché (41 personas)'
    dl = float((RP.lag - pe_i.lag_parpadeo_s).abs().max())
    reg(S, 'Crudos, 41 personas: diferencia máxima del desfase del parpadeo frente a personas.csv, s', 0, FR, dl, 9, veredicto='coincide' if dl < 1e-9 else 'difiere')
    du = int((RP.usable != pe_i.usable_channels).sum() + (RP.blinks != pe_i.blinks).sum() + (j.usable_x != j.usable_y).sum())
    reg(S, 'Crudos, 41 personas: discrepancias en canales utilizables, parpadeos o canal utilizable', 0, FR, du, 0)
    da = float((j.amp - j.blink_ptp_uv).abs().max())
    reg(S, 'Crudos, 41 personas: diferencia máxima de amplitud del parpadeo por canal, µV', 0, FR, da, 6, veredicto='coincide' if da < 1e-6 else 'difiere')
    dr = float((j.rh - j.r_horizontal).abs().max())
    reg(S, 'Crudos, 41 personas: diferencia máxima de la correlación horizontal por canal', 0, FR, dr, 9, veredicto='coincide' if dr < 1e-9 else 'difiere')
    reg(S, 'Crudos: desfase mínimo, s', .18, FR, float(RP.lag.min()), 2)
    reg(S, 'Crudos: desfase máximo, s', .53, FR, float(RP.lag.max()), 2)
    reg(S, 'Crudos: desfase mediano, s', .45, FR, float(RP.lag.median()), 2)
    m2 = RC.groupby('channel').amp.median()
    reg(S, 'Crudos: amplitud mediana del parpadeo en Fp1, µV', 148, FR, float(m2[0]), 0)
    reg(S, 'Crudos: amplitud mediana del parpadeo en Fp2, µV', 151, FR, float(m2[1]), 0)
    w2 = RC.pivot(index='participant', columns='channel', values='rh')[[8, 9]].dropna()
    reg(S, 'Crudos: personas con signo opuesto en F7 y F8', 31, FR, int((np.sign(w2[8]) != np.sign(w2[9])).sum()), 0, nota=f'de {len(w2)}')
    for p in five:
        cp = RC[RC.participant == p].set_index('channel')
        reg(S, f'Detalle {p}: desfase del parpadeo, s', float(pe_i.lag_parpadeo_s[p]), 'personas.csv', float(RP.lag[p]), 3,
            nota=f'{RP.usable[p]} canales; {RP.blinks[p]} parpadeos; Fp1 {cp.amp[0]:.2f} µV; Fp2 {cp.amp[1]:.2f} µV; F7 {cp.rh[8]:+.4f}; F8 {cp.rh[9]:+.4f}')
    return five

# ================================================================== 4. Limpieza ocular
def sec_limpieza(W, five):
    from scipy.signal import butter, sosfiltfilt, iirnotch, filtfilt
    S = '4 Limpieza'
    D = RES / 'limpieza_ocular_41p_23-11-2026'
    F = 'INFORME limpieza'
    desc = pd.read_csv(D / 'descriptivos.csv').set_index('item')
    new = pd.concat([pd.read_csv(D / f'pred_{sd}.csv.gz') for sd in SEEDS])
    e2 = pd.concat([pd.read_csv(RES / f'enfoques_41p_22-11-2026/e2_{sd}.csv.gz') for sd in SEEDS])
    old = e2[~e2.strategy.isin(['control_barajado', 'gsr_c1'])]
    single = ['control_barajado', 'identidad_full']
    pred = pd.concat([new[~new.strategy.isin(single)], old])
    w = wide_mean(pred)
    T = [('eeg_c1', .681), ('ica1_full', .661), ('ica2_full', .638), ('ica3_full', .621), ('ica4_full', .613), ('ctrl3_full', .674),
         ('ica3_lento_amp', .603), ('ica3_frontal', .621), ('ica3_posterior', .562), ('ica3_alfa_beta', .547), ('orig12', .646), ('reg12', .634)]
    for s_, inf in T:
        reg(S, f'AUC {s_}', inf, F, float(w[s_].mean()), 3, guardado=float(desc.loc[f'AUC {s_}'].delta), nota=f'{int((w[s_] > .5).sum())}/41 sobre 0,5')
    reg(S, 'Personas con alfa y beta limpio sobre el azar', 38, F, int((w.ica3_alfa_beta > .5).sum()), 0)
    reg(S, 'Personas con canales posteriores limpios sobre el azar', None, '—', int((w.ica3_posterior > .5).sum()))
    C = [('eeg_c1', 'ica1_full', .020, None), ('eeg_c1', 'ica2_full', .043, None), ('eeg_c1', 'ica3_full', .060, None), ('eeg_c1', 'ica4_full', .068, None),
         ('eeg_c1', 'ctrl3_full', (.007, -.001, .015), None), ('eeg_lento_amp', 'ica3_lento_amp', .070, None), ('eeg_frontal', 'ica3_frontal', .054, None),
         ('eeg_posterior', 'ica3_posterior', .040, None), ('eeg_alfa_beta', 'ica3_alfa_beta', .045, None), ('ica3_frontal', 'ica3_posterior', .059, None),
         ('ica3_lento_amp', 'ica3_alfa_beta', .055, None), ('orig12', 'reg12', (.012, -.000, .024), None), ('ica3_full', 'ica4_full', (.007, -.000, .015), None)]
    for a_, b_, inf, _ in C:
        c = contrast(w[a_] - w[b_])
        key = f'{a_} − {b_}'
        g_ = (desc.loc[key].delta, desc.loc[key].low95, desc.loc[key].high95) if key in desc.index else None
        ci_reg(S, f'{a_} − {b_}', inf, F, c, 3, guardado=g_, nota=f"{c['mejoran']}/{c['n']}")
    reg(S, 'Caída de alfa y beta sobre el azar: de +0,093 a +0,047 — después', .047, 'AUDITORIA_RESULTADOS limpieza', float(w.ica3_alfa_beta.mean() - .5), 3)
    one = new[new.seed.eq(1101)]
    cb = person_auc(one[one.strategy.eq('control_barajado')]).set_index('participant').auc.sort_index()
    c = contrast(cb - .5)
    r = desc.loc['control barajado − 0,5 (una partición)']
    ci_reg(S, 'Control con etiquetas barajadas − 0,5 (una partición)', (-.011, -.023, .001), F, c, 3, guardado=(r.delta, r.low95, r.high95))
    reg(S, 'Control con etiquetas barajadas, AUC', .489, 'AUDITORIA_RESULTADOS limpieza', float(cb.mean()), 3)
    reg(S, 'Control barajado: IC 90 % inferior', -.021, 'AUDITORIA_RESULTADOS limpieza', c['low90'], 3)
    reg(S, 'Control barajado: IC 90 % superior', -.001, 'AUDITORIA_RESULTADOS limpieza', c['high90'], 3)
    a_ = one[one.strategy.eq('identidad_full')].set_index('source_row').prob
    b_ = e2[e2.seed.eq(1101) & e2.strategy.eq('eeg_c1')].set_index('source_row').prob
    reg(S, 'Máxima diferencia de probabilidad entre el filtro identidad y eeg_c1', 0, F, float((a_ - b_.loc[a_.index]).abs().max()), 12)
    # Spearman con el recorrido de la mirada
    ref = pd.concat([-W[['gaze_path_length_px', 'gaze_dispersion_2d_px']], W[['fixation_total_ms', 'fixation_mean_ms', 'pupil_mean_z', 'score', 'participant', 'source_row']]], axis=1)
    def rho(preds, strat, col='gaze_path_length_px'):
        m = preds[preds.strategy.eq(strat)].groupby('source_row').prob.mean().rename('prob').reset_index().merge(ref, on='source_row').dropna(subset=[col])
        return m.groupby('participant').apply(lambda g: spearman(g.prob, g[col]))
    for s_, inf in [('eeg_c1', .41), ('ica3_full', .28), ('ica3_alfa_beta', .11), ('reg12', None)]:
        reg(S, f'Spearman medio por persona de la prob. {s_} con el recorrido de la mirada (invertido)', inf, F, float(rho(pred, s_).mean()), 2,
            guardado=float(desc.loc[f'Spearman prob {s_} con gaze_path_length_px'].delta))
    # sensibilidades
    for lab_, out_, inf1, inf2 in [('sin P23 y P39', ['P23', 'P39'], .060, .052), ('sin P23, P39 ni las cinco de identificación débil', ['P23', 'P39', 'P12', 'P18', 'P22', 'P35', 'P40'], .061, .054)]:
        ww = w.drop(index=out_)
        reg(S, f'L1 {lab_}', inf1, F, float((ww.eeg_c1 - ww.ica3_full).mean()), 3)
        reg(S, f'L2 {lab_}', inf2, F, float((ww.ctrl3_full - ww.ica3_full).mean()), 3)
    for nm, d_, inf_mean, inf_med, inf_wo in [('L1', w.eeg_c1 - w.ica3_full, .060, .060, .064), ('L2', w.ctrl3_full - w.ica3_full, .054, .053, .058)]:
        di = drop_influential(d_)
        reg(S, f'{nm}: mediana', inf_med, 'AUDITORIA_RESULTADOS limpieza ("0,060 y 0,053")', di['mediana'], 3, nota=f"media {di['media']:.6f}")
        reg(S, f'{nm}: sin la persona más influyente', inf_wo, 'AUDITORIA_RESULTADOS limpieza', di['delta'], 3, nota=f"persona {di['persona']} ({di['delta_persona']:+.3f})")
    reg(S, 'P9: AUC original', .569, F, float(w.eeg_c1['P9']), 3)
    reg(S, 'P9: AUC tras la limpieza', .680, F, float(w.ica3_full['P9']), 3)
    info = pd.read_csv(D / 'personas_limpieza.csv').set_index('participant')
    drop_ = (w.eeg_c1 - w.ica3_full)
    reg(S, 'Spearman entre la caída por persona y el puntaje del primer componente', .12, F, spearman(drop_, info.score_1.loc[drop_.index]), 2,
        nota=f'p {spearman_p(spearman(drop_, info.score_1.loc[drop_.index]), 41):.3f}')
    reg(S, 'Spearman entre la caída por persona y la AUC de partida', .55, F, spearman(drop_, w.eeg_c1), 2)
    # calidad de la limpieza, desde los CSV
    q = pd.read_csv(D / 'calidad_limpieza.csv')
    md = q.groupby('condition')[['r_horizontal', 'r_vertical', 'r_parpadeo', 'blink_max_uv']].median()
    for col, nm, vals in [('r_parpadeo', 'parpadeo', (.28, .08, .31)), ('r_horizontal', 'mirada horizontal', (.21, .11, .22)), ('r_vertical', 'mirada vertical', (.18, .07, .18))]:
        for cond, inf in zip(['identidad', 'ica3', 'ctrl3'], vals):
            reg(S, f'Correlación máxima canal–{nm}, mediana entre personas, {cond}', inf, F, float(md.loc[cond, col]), 2, guardado=float(desc.loc[f'calidad {cond}: mediana {col}'].delta))
    reg(S, '% de la varianza en los 3 componentes oculares (mediana)', 3.5, F, float(info.var_share_ica3.median()), 1, guardado=float(desc.loc['limpieza: mediana var_share_ica3'].delta), escala=100,
        nota=f'rango {info.var_share_ica3.min():.4f}–{info.var_share_ica3.max():.4f}')
    reg(S, '% de la varianza en los 3 componentes de control (mediana)', 72, F, float(info.var_share_ctrl3.median()), 0, guardado=float(desc.loc['limpieza: mediana var_share_ctrl3'].delta), escala=100,
        nota=f'rango {info.var_share_ctrl3.min():.4f}–{info.var_share_ctrl3.max():.4f}')
    reg(S, 'Razón de varianza control / ocular ("veinte veces más")', 20, F, float(info.var_share_ctrl3.median() / info.var_share_ica3.median()), 0)
    for i_, inf in zip(range(1, 5), [.38, .23, .17, .13]):
        reg(S, f'Puntaje ocular mediano del componente {i_}', inf, F, float(info[f'score_{i_}'].median()), 2)
    reg(S, 'Puntaje ocular del control (mediana del máximo por persona)', .06, F + ' ("0,06 como máximo")', float(info.score_control_max.median()), 2,
        nota=f'máximo entre personas {info.score_control_max.max():.4f}')
    reg(S, 'Canales utilizables por persona: mínimo', 11, F, int(info.usable_channels.min()), 0)
    reg(S, 'Canales utilizables por persona: máximo', 16, F, int(info.usable_channels.max()), 0)
    reg(S, '3 componentes como % de las dimensiones: mínimo', 19, F, float(3 / info.usable_channels.max()), 0, escala=100)
    reg(S, '3 componentes como % de las dimensiones: máximo', 27, F, float(3 / info.usable_channels.min()), 0, escala=100)
    weak = sorted(info.index[info.score_1 < .15])
    reg(S, 'Personas con puntaje del primer componente bajo 0,15 son P12, P18, P22, P35 y P40 (0 = sí)', 0, 'enmienda_v2 limpieza', 0 if weak == ['P12', 'P18', 'P22', 'P35', 'P40'] else 1, 0,
        nota=f'{weak}; P18 {info.score_1["P18"]:.4f}; siguiente {info.score_1[info.score_1 >= .15].min():.4f}')
    reg(S, 'Desfase usado en la limpieza: mínimo, s', .25, F + ' ("0,25–0,5 s")', float(info.lag_s.min()), 2)
    reg(S, 'Desfase usado en la limpieza: máximo, s', .5, F + ' ("0,25–0,5 s")', float(info.lag_s.max()), 1)
    reg(S, 'Ventanas en que el filtro identidad reproduce la tabla vigente', 22211, F, int(json.loads((D / 'limpieza.json').read_text())['rows']), 0)
    # ---- desde los crudos y los filtros guardados (sin reajustar la ICA): 5 personas
    BROAD = butter(4, [1, 45], btype='bandpass', fs=FS, output='sos')
    NOTCH = iirnotch(50, 30, fs=FS)
    _, people = sample_people()
    rows = []
    LAGS = np.arange(-125, 126)
    for p in people:
        r = raw_person(p)
        G = np.flatnonzero(r['good'])
        x = r['x']
        xb = sosfiltfilt(BROAD, filtfilt(*NOTCH, x[:, G], axis=0), axis=0)
        rail = (np.abs(x[:, G]) >= 180000).any(axis=1).astype(float)
        keep = np.convolve(rail, np.ones(int(2 * FS) + 1), 'same') < .5
        x15 = sosfiltfilt(r['sos15'], xb, axis=0)
        cc = np.array([[np.abs(lagcorr(r['ref'][:, j], x15, int(Lg))).max() for Lg in LAGS] for j in range(3)])
        lag = int(LAGS[np.unravel_index(cc.argmax(), cc.shape)[1]])
        filt = np.load(D / 'filtros' / f'{p}.npz')
        cov = np.cov(xb[keep], rowvar=False)
        row = dict(participant=p, usable=len(G), lag=lag / FS)
        for cond in ['ica3', 'ctrl3']:
            P = filt[cond][np.ix_(G, G)]
            row[f'var_{cond}'] = float(np.trace(P @ cov @ P.T) / np.trace(cov))
        for cond in ['identidad', 'ica3', 'ctrl3']:
            P = np.zeros((len(G), len(G))) if cond == 'identidad' else filt[cond][np.ix_(G, G)]
            y = x15 - x15 @ P.T
            for j, nm in enumerate(['h', 'v', 'b']):
                row[f'r{nm}_{cond}'] = float(np.abs(lagcorr(r['ref'][:, j], y, lag)).max())
        rows.append(row)
    RR = pd.DataFrame(rows).set_index('participant')
    inf_ = info.loc[RR.index]
    FR = 'crudos en caché + filtros guardados (41 personas, sin reajustar la ICA)'
    reg(S, 'Crudos, 41 personas: discrepancias en canales utilizables frente a personas_limpieza.csv', 0, FR, int((RR.usable != inf_.usable_channels).sum()), 0)
    dl = float((RR.lag - inf_.lag_s).abs().max())
    reg(S, 'Crudos, 41 personas: diferencia máxima del desfase, s', 0, FR, dl, 9, veredicto='coincide' if dl < 1e-9 else 'difiere')
    for cond, col in [('ica3', 'var_share_ica3'), ('ctrl3', 'var_share_ctrl3')]:
        dv = float((RR[f'var_{cond}'] - inf_[col]).abs().max())
        reg(S, f'Crudos, 41 personas: diferencia máxima de la fracción de varianza retirada por {cond}', 0, FR, dv, 6,
            veredicto='coincide' if dv < 1e-6 else ('coincide con redondeo' if dv < 5e-3 else 'difiere'))
    reg(S, 'Crudos: % de varianza retirada por los 3 componentes oculares (mediana)', 3.5, FR, float(RR.var_ica3.median()), 1, escala=100)
    reg(S, 'Crudos: % de varianza retirada por el control (mediana)', 72, FR, float(RR.var_ctrl3.median()), 0, escala=100)
    qw = q.pivot(index='participant', columns='condition')
    dq = 0.
    for cond in ['identidad', 'ica3', 'ctrl3']:
        for nm, col in [('h', 'r_horizontal'), ('v', 'r_vertical'), ('b', 'r_parpadeo')]:
            dq = max(dq, float((RR[f'r{nm}_{cond}'] - qw[(col, cond)].loc[RR.index]).abs().max()))
    reg(S, 'Crudos, 41 personas: diferencia máxima de las correlaciones canal–referencia (3 condiciones × 3 referencias)', 0, FR, dq, 9, veredicto='coincide' if dq < 1e-9 else 'difiere')
    for cond, inf in zip(['identidad', 'ica3', 'ctrl3'], [.28, .08, .31]):
        reg(S, f'Crudos: correlación máxima canal–parpadeo, mediana, {cond}', inf, FR, float(RR[f'rb_{cond}'].median()), 2)
    reg(S, 'Crudos: canales utilizables, mínimo', 11, FR, int(RR.usable.min()), 0)
    reg(S, 'Crudos: canales utilizables, máximo', 16, FR, int(RR.usable.max()), 0)
    for p in five:
        reg(S, f'Detalle {p}: fracción de varianza retirada por ica3', float(inf_.var_share_ica3[p]), 'personas_limpieza.csv', float(RR.var_ica3[p]), 6, guardado=float(inf_.var_share_ica3[p]),
            veredicto='coincide' if abs(RR.var_ica3[p] - inf_.var_share_ica3[p]) < 1e-6 else 'difiere',
            nota=f'control {RR.var_ctrl3[p]:.6f}; parpadeo {RR.rb_identidad[p]:.4f} → {RR.rb_ica3[p]:.4f} (control {RR.rb_ctrl3[p]:.4f}); {RR.usable[p]} canales; desfase {RR.lag[p]:.3f} s')

# ================================================================== 5. Red sobre la señal cruda
def sec_red(W, y_act):
    S = '5 Red cruda'
    D = RES / 'red_cruda_41p_23-11-2026'
    F = 'INFORME red cruda'
    desc = pd.read_csv(D / 'descriptivos.csv').set_index('item')
    read = lambda m: pd.concat([pd.read_csv(D / f'{m}_{sd}.csv.gz') for sd in SEEDS])
    e2 = pd.concat([pd.read_csv(RES / f'enfoques_41p_22-11-2026/e2_{sd}.csv.gz') for sd in SEEDS])
    cl = pd.concat([pd.read_csv(RES / f'limpieza_ocular_41p_23-11-2026/pred_{sd}.csv.gz') for sd in SEEDS])
    att = pd.concat([read('red_orig'), read('red_ica3'), e2[e2.strategy.eq('eeg_c1')], cl[cl.strategy.eq('ica3_full')]])
    act = pd.concat([read('red_act'), read('hgb_eeg_act'), rep('activacion', ['hgb_c1'])])
    pa_att, pa_act = person_auc(att, ('seed',)), person_auc(act, ('seed',))
    wa = pa_att.groupby(['participant', 'strategy']).auc.mean().unstack()
    wc = pa_act.groupby(['participant', 'strategy']).auc.mean().unstack()
    for wv, s_, inf, n5 in [(wa, 'red_orig', (.716, .697, .735), 41), (wa, 'eeg_c1', (.681, .665, .697), 41), (wa, 'red_ica3', (.649, .630, .667), 41), (wa, 'ica3_full', (.621, .607, .635), 41),
                            (wc, 'red_act', (.498, .478, .518), 20), (wc, 'hgb_eeg_act', (.524, .497, .551), 26), (wc, 'hgb_c1', (.518, .491, .545), 22)]:
        r = desc.loc[f'AUC {s_}']
        ci_reg(S, f'AUC {s_}', inf, F, absol(wv[s_]), 3, guardado=(r.delta, r.low95, r.high95))
        reg(S, f'Personas con AUC {s_} sobre 0,5', n5, F, int((wv[s_] > .5).sum()), 0)
    CON = dict(R1=(wa.red_orig - wa.eeg_c1), R2=(wa.red_ica3 - wa.ica3_full), R3=(wa.red_orig - wa.red_ica3), R4=(wc.red_act - wc.hgb_eeg_act))
    INFC = dict(R1=(.035, .023, .047, 32), R2=(.028, .013, .043, 30), R3=(.067, .053, .082, 39), R4=(-.025, -.055, .003, 15))
    for k_, d_ in CON.items():
        c = contrast(d_)
        ci_reg(S, f'{k_}', INFC[k_][:3], F, c, 3, nota=f"{c['mejoran']}/41; p {c['p']:.6f}; IC90 [{c['low90']:.4f}; {c['high90']:.4f}]")
    # robustez por partición
    PART = dict(R1=[.033, .036, .039, .037, .030], R2=[.028, .024, .030, .032, .026], R3=[.068, .068, .068, .067, .065], R4=[-.039, -.042, -.021, .002, -.028])
    per_a = {sd: g.pivot(index='participant', columns='strategy', values='auc') for sd, g in pa_att.groupby('seed')}
    per_c = {sd: g.pivot(index='participant', columns='strategy', values='auc') for sd, g in pa_act.groupby('seed')}
    for i, sd in enumerate(SEEDS):
        a_, c_ = per_a[sd], per_c[sd]
        vals = dict(R1=(a_.red_orig - a_.eeg_c1), R2=(a_.red_ica3 - a_.ica3_full), R3=(a_.red_orig - a_.red_ica3), R4=(c_.red_act - c_.hgb_eeg_act))
        for k_, v in vals.items():
            reg(S, f'{k_} en la partición {sd}', PART[k_][i], F + ', robustez', float(v.mean()), 3)
        if sd == 1105:
            reg(S, 'R1 con la partición 1105 sola: IC 95 % inferior', .017, F + ', límites', boot(vals['R1'].to_numpy())[0], 3)
    # sin P23 y P39
    for k_, inf in zip(['R1', 'R2', 'R3', 'R4'], [(.0364, .0248, .0482), (.0282, .0126, .0439), (.0680, .0529, .0838), (-.0273, -.0574, .0026)]):
        c = contrast(CON[k_].drop(index=['P23', 'P39']))
        ci_reg(S, f'{k_} sin P23 y P39', inf, 'AUDITORIA_RESULTADOS red', c, 4)
        reg(S, f'{k_} sin P23 y P39 (informe, 3 decimales)', round(inf[0], 3), F, c['delta'], 3)
    # dejando una persona fuera
    loo = {}
    for k_, d_ in CON.items():
        rows = []
        for q in d_.index:
            r_ = d_.drop(index=q).to_numpy()
            lo, hi = boot(r_)
            rows.append((q, lo, hi))
        loo[k_] = pd.DataFrame(rows, columns=['p', 'lo', 'hi']).set_index('p')
    reg(S, 'R1 dejando una persona fuera: IC 95 % inferior mínimo', .0215, 'AUDITORIA_RESULTADOS red', float(loo['R1'].lo.min()), 4)
    reg(S, 'R1 dejando una persona fuera: IC 95 % inferior máximo', .0257, 'AUDITORIA_RESULTADOS red', float(loo['R1'].lo.max()), 4)
    reg(S, 'R2 dejando una persona fuera: IC 95 % inferior mínimo', .0100, 'AUDITORIA_RESULTADOS red', float(loo['R2'].lo.min()), 4)
    reg(S, 'R2 dejando una persona fuera: IC 95 % inferior máximo', .0173, 'AUDITORIA_RESULTADOS red', float(loo['R2'].lo.max()), 4)
    reg(S, 'R3 dejando una persona fuera: IC 95 % inferior mínimo', .0508, 'AUDITORIA_RESULTADOS red', float(loo['R3'].lo.min()), 4)
    inferior = sorted(loo['R4'].index[loo['R4'].hi < 0])
    reg(S, 'R4 pasa a "inferior" al quitar a P10, P24, P33, P34 o P40 (0 = exactamente esas cinco)', 0, F, 0 if inferior == ['P10', 'P24', 'P33', 'P34', 'P40'] else 1, 0,
        nota=f'{inferior}; IC superior al quitarlas: ' + '; '.join(f'{q} {loo["R4"].hi[q]:+.5f}' for q in inferior))
    keepdec = lambda k_, thr: bool((loo[k_].lo > thr).all())
    reg(S, 'R1 mantiene "efecto relevante" al quitar cualquier persona (0 = sí)', 0, F, 0 if keepdec('R1', .02) else 1, 0)
    reg(S, 'R3 mantiene "efecto relevante" al quitar cualquier persona (0 = sí)', 0, F, 0 if keepdec('R3', .02) else 1, 0)
    reg(S, 'R2 mantiene IC 95 % inferior > 0 al quitar cualquier persona (0 = sí)', 0, F, 0 if keepdec('R2', 0) else 1, 0)
    two = CON['R1'].sort_values(ascending=False).index[:2].tolist()
    reg(S, 'Las dos personas más favorables a R1 son P21 y P18 (0 = sí)', 0, F, 0 if set(two) == {'P21', 'P18'} else 1, 0, nota=str(two))
    reg(S, 'R1 sin P21 y P18: IC 95 % inferior', .0199, F, boot(CON['R1'].drop(index=['P21', 'P18']).to_numpy())[0], 4)
    v2 = CON['R1'].drop(index=['P21', 'P18']).to_numpy()
    lows = [boot(v2, seed=sd_)[0] for sd_ in range(1, 31)]
    reg(S, 'R1 sin P21 y P18: IC 95 % inferior con otras 30 semillas de remuestreo (mínimo)', None, '—', float(min(lows)),
        nota=f'máximo {max(lows):.5f}; bajo 0,02 en {sum(l < .02 for l in lows)} de 30; t de Student {v2.mean() - 2.0244 * v2.std(ddof=1) / np.sqrt(len(v2)):.5f}')
    lows1 = [boot(CON['R1'].to_numpy(), seed=sd_)[0] for sd_ in range(1, 31)]
    reg(S, 'R1: IC 95 % inferior con 30 semillas, mínimo', .0230, 'AUDITORIA_RESULTADOS red ("entre 0,0230 y 0,0234")', float(min(lows1)), 4, nota=f'máximo {max(lows1):.5f}')
    c = contrast(CON['R1'] - CON['R2'])
    ci_reg(S, 'R1 − R2 (cambio de la ventaja de la red al limpiar)', (.007, -.005, .020), 'Auditoría 23-11, I1', c, 3, nota=f"p {c['p']:.3f}; {c['mejoran']}/41; IC90 [{c['low90']:.4f}; {c['high90']:.4f}]")
    reg(S, 'R1 − R2: p', .29, 'Auditoría 23-11, I1', c['p'], 2)
    reg(S, 'R1 − R2: personas', 20, 'Auditoría 23-11, I1', c['mejoran'], 0)
    c = contrast(wc.hgb_c1 - wc.hgb_eeg_act)
    ci_reg(S, '(EEG + mirada + pupila) − solo EEG, activación', (-.006, -.022, .009), 'Auditoría 23-11, I6', c, 3, guardado=(desc.loc['hgb_c1 − hgb_eeg_act'].delta, desc.loc['hgb_c1 − hgb_eeg_act'].low95, desc.loc['hgb_c1 − hgb_eeg_act'].high95))
    c = contrast(wc.hgb_eeg_act - .5)
    reg(S, 'HGB solo EEG en activación − 0,5: p', .09, F, c['p'], 2, guardado=float(desc.loc['hgb_eeg_act − 0,5'].p))
    sdp = pa_act[pa_act.strategy.eq('red_act')].groupby('participant').auc.std(ddof=1)
    reg(S, 'Desviación entre semillas de la AUC por persona, red de activación (media)', .045, 'AUDITORIA_RESULTADOS red ("cercana a 0,045")', float(sdp.mean()), 3,
        nota=f'HGB solo EEG {pa_act[pa_act.strategy.eq("hgb_eeg_act")].groupby("participant").auc.std(ddof=1).mean():.4f}')
    # AUC juntando todas las ventanas
    ro = att[att.strategy.eq('red_orig')]
    pooled = [auc(g.y, g.prob) for _, g in ro.groupby('seed')]
    reg(S, 'AUC de la red original juntando todas las ventanas (media de 5 particiones)', .684, F, float(np.mean(pooled)), 3, nota='por partición: ' + '; '.join(f'{v:.5f}' for v in pooled))
    mp = ro.groupby('source_row').agg(y=('y', 'first'), prob=('prob', 'mean'))
    reg(S, 'Ídem, con la probabilidad promediada sobre particiones', None, '—', auc(mp.y, mp.prob))
    # Spearman con el recorrido
    ref = pd.concat([-W[['gaze_path_length_px']], W[['score', 'participant', 'source_row']]], axis=1)
    def rho(preds, strat, col):
        m = preds[preds.strategy.eq(strat)].groupby('source_row').prob.mean().rename('prob').reset_index().merge(ref, on='source_row').dropna(subset=[col])
        return float(m.groupby('participant').apply(lambda g: spearman(g.prob, g[col])).mean())
    for s_, col, inf, key in [('red_orig', 'gaze_path_length_px', .48, 'Spearman prob red_orig con gaze_path_length_px'), ('eeg_c1', 'gaze_path_length_px', .41, None),
                              ('red_ica3', 'gaze_path_length_px', .33, 'Spearman prob red_ica3 con gaze_path_length_px'),
                              ('red_orig', 'score', .45, 'Spearman prob red_orig con puntaje'), ('red_ica3', 'score', .32, 'Spearman prob red_ica3 con puntaje')]:
        reg(S, f"Spearman medio por persona, prob. {s_} con {'el recorrido de la mirada (invertido)' if col != 'score' else 'el puntaje ocular'}", inf, F if col != 'score' else 'AUDITORIA_RESULTADOS red',
            rho(att, s_, col), 2, guardado=None if key is None else float(desc.loc[key].delta))
    # parámetros de la red (conteo analítico de la arquitectura declarada en el protocolo)
    net = json.loads((D / 'protocolo.json').read_text())['net']
    f1, dp, f2, k1, k2 = net['f1'], net['depth'], net['f2'], net['k1'], net['k2']
    t1 = 240 + 2 * (k1 // 2) - k1 + 1
    t2 = t1 // 4
    t3 = (t2 + 2 * (k2 // 2) - k2 + 1) // 8
    npar = f1 * k1 + 2 * f1 + (f1 * dp) * 16 + 2 * f1 * dp + (f1 * dp) * k2 + (f1 * dp) * f2 + 2 * f2 + f2 * t3 + 1
    reg(S, 'Parámetros entrenables de la red (conteo analítico)', 1217, F, npar, 0, nota=f'capa lineal con {f2 * t3} entradas')
    reg(S, 'Duración del núcleo temporal, s', .26, F, k1 / FS, 2)
    # ventanas con entrada en cero (tensores locales, solo lectura)
    tdir = LOCAL / 'red_cruda_tensores'
    if (tdir / 'orig.npy').exists():
        rows = np.load(tdir / 'source_row.npy')
        X = np.load(tdir / 'orig.npy', mmap_mode='r')
        zero = np.array([not X[i:i + 2000].reshape(min(2000, len(X) - i), -1).any(axis=1).all() for i in range(0, 0)])
        zr = np.concatenate([~np.abs(X[i:i + 2000]).reshape(len(X[i:i + 2000]), -1).any(axis=1) for i in range(0, len(X), 2000)])
        lab_att = set(W.source_row[W.y_att.notna()])
        lab_act = set(W.source_row[y_act.notna().to_numpy()])
        reg(S, 'Ventanas con la entrada toda en cero (tensor original, 22.211 ventanas)', 50, F, int(zr.sum()), 0,
            nota=f'con etiqueta de atención {sum(r_ in lab_att for r_ in rows[zr])}; con etiqueta de activación {sum(r_ in lab_act for r_ in rows[zr])}; '
                 f'personas {sorted(set(W.set_index("source_row").participant.loc[rows[zr]]))}')
        X2 = np.load(tdir / 'ica3.npy', mmap_mode='r')
        zr2 = np.concatenate([~np.abs(X2[i:i + 2000]).reshape(len(X2[i:i + 2000]), -1).any(axis=1) for i in range(0, len(X2), 2000)])
        reg(S, 'Ventanas con la entrada toda en cero (tensor limpio)', 50, F, int(zr2.sum()), 0)
        reg(S, 'Forma del tensor: ventanas', 22211, F, int(X.shape[0]), 0, nota=str(X.shape))
    else:
        reg(S, 'Ventanas con la entrada toda en cero', 50, F, None, veredicto='no recalculable por falta de archivo')


# ================================================================== 7. Etapas del 16-11
def clf_metrics(y, prob):
    y = np.asarray(y).astype(int)
    h = (np.asarray(prob) >= .5).astype(int)
    tp, tn, fp, fn = ((y == 1) & (h == 1)).sum(), ((y == 0) & (h == 0)).sum(), ((y == 0) & (h == 1)).sum(), ((y == 1) & (h == 0)).sum()
    r1, r0 = tp / (tp + fn), tn / (tn + fp)
    f1p = 2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) else 0.
    f1n = 2 * tn / (2 * tn + fn + fp) if (2 * tn + fn + fp) else 0.
    return dict(ba=(r1 + r0) / 2, f1_macro=(f1p + f1n) / 2, recall_alta=r1, recall_baja=r0)


def sec_1611(W):
    S = '7 Etapas del 16-11'
    split = pd.read_csv(PARTS).set_index('participant').split
    # ---------- cierre V3
    D = RES / 'cierre_v3_16-11-2026'
    F = 'INFORME cierre V3'
    met = pd.read_csv(D / 'metricas.csv').set_index(['task', 'split', 'strategy'])
    con = pd.read_csv(D / 'contrastes.csv').set_index(['task', 'split', 'contrast'])
    pred = pd.concat([pd.read_csv(D / f'{k}_{t}.csv.gz') for t in ['atencion', 'activacion'] for k in ['oof', 'externas']], ignore_index=True)
    rows = []
    for (task, sp, strat, person), g in pred.groupby(['task', 'split', 'strategy', 'participant']):
        rows.append(dict(task=task, split=sp, strategy=strat, participant=person, auc=auc(g.y, g.prob), **clf_metrics(g.y, g.prob)))
    PM = pd.DataFrame(rows)
    dmax = {m: 0. for m in ['auc', 'ba', 'f1_macro', 'recall_alta', 'recall_baja']}
    dci = 0.
    for (task, sp, strat), g in PM.groupby(['task', 'split', 'strategy']):
        g = g.sort_values('participant')
        for m in dmax:
            dmax[m] = max(dmax[m], abs(g[m].mean() - met.loc[(task, sp, strat), m]))
            lo, hi = boot(g[m].to_numpy())
            dci = max(dci, abs(lo - met.loc[(task, sp, strat), f'{m}_low']), abs(hi - met.loc[(task, sp, strat), f'{m}_high']))
    nm = dict(auc='AUC', ba='BA', f1_macro='macro-F1', recall_alta='recall de la clase alta', recall_baja='recall de la clase baja')
    for m, v in dmax.items():
        reg(S, f'V3: diferencia máxima de {nm[m]} media frente a metricas.csv ({len(met)} filas)', 0, 'cierre_v3 metricas.csv', v, 9, veredicto='coincide' if v < 1e-9 else 'difiere')
    reg(S, 'V3: diferencia máxima de los IC 95 % de las cinco métricas (misma semilla)', 0, 'cierre_v3 metricas.csv', dci, 9, veredicto='coincide' if dci < 1e-9 else 'difiere')
    reg(S, 'V3: personas por partición — entrenamiento', 25, F, PM[PM.split.eq('oof_train')].participant.nunique(), 0)
    reg(S, 'V3: personas por partición — validación', 8, F, PM[PM.split.eq('validation')].participant.nunique(), 0)
    reg(S, 'V3: personas por partición — test', 8, F, PM[PM.split.eq('test')].participant.nunique(), 0)
    for task in ['atencion', 'activacion']:
        for strat in ['hgb_c1', 'hgb_c32', 'gru_c32']:
            g = PM[(PM.task == task) & (PM.split == 'test') & (PM.strategy == strat)]
            reg(S, f'V3 test {task} {strat}: BA / macro-F1 / recall alta / recall baja (se registra BA)', None, 'cierre_v3 metricas.csv', float(g.ba.mean()),
                guardado=float(met.loc[(task, 'test', strat), 'ba']), veredicto='coincide' if abs(g.ba.mean() - met.loc[(task, 'test', strat), 'ba']) < 1e-9 else 'difiere',
                nota=f'macro-F1 {g.f1_macro.mean():.6f}; recall alta {g.recall_alta.mean():.6f}; recall baja {g.recall_baja.mean():.6f}')
    T = {('atencion', 'hgb_c1'): (.662, .619, .703), ('atencion', 'hgb_c32'): (.690, .644, .733), ('atencion', 'gru_c32'): (.640, .583, .696),
         ('activacion', 'hgb_c1'): (.514, .451, .579), ('activacion', 'hgb_c32'): (.547, .466, .623), ('activacion', 'gru_c32'): (.583, .488, .676)}
    for (task, strat), inf in T.items():
        g = PM[(PM.task == task) & (PM.split == 'test') & (PM.strategy == strat)].sort_values('participant')
        ci_reg(S, f'V3 test {task} {strat}: AUC', inf, F, absol(g.auc.to_numpy()), 3)
    tr = PM[(PM.task == 'activacion') & (PM.split == 'oof_train')].groupby('strategy').auc.mean()
    reg(S, 'V3 activación, entrenamiento: AUC mínima entre estrategias ("entre 0,50 y 0,53")', .50, F, float(tr.min()), 2, nota=f'máxima {tr.max():.4f}')
    reg(S, 'V3 activación, entrenamiento: AUC máxima entre estrategias', .53, F, float(tr.max()), 2)
    CT = [('atencion', 'hgb_c32', 'hgb_c1', 'hgb_resumen', [(.018, .009, .027, 20), (.020, -.003, .042, 6), (.029, .004, .052, 7)]),
          ('atencion', 'gru_c32', 'gru_c1', 'gru_orden', [(.001, -.013, .014, 11), (-.004, -.036, .028, 4), (.010, -.019, .035, 5)]),
          ('activacion', 'hgb_c32', 'hgb_c1', 'hgb_resumen', [(.016, -.036, .070, 15), (.059, -.004, .131, 5), (.033, -.021, .094, 4)]),
          ('activacion', 'gru_c32', 'gru_c1', 'gru_orden', [(-.016, -.089, .048, 13), (.091, .018, .188, 6), (.084, -.011, .165, 7)]),
          ('atencion', 'tardia_c32', 'hgb_c32', 'tardia_vs_temprana_c32', [(-.010, -.018, -.003, 7), (-.008, -.020, .005, None), (-.002, -.015, .008, None)]),
          ('atencion', 'gru_c32', 'hgb_c32', 'gru_vs_hgb_c32', [(-.042, -.063, -.022, None), (-.044, -.092, -.007, None), (-.050, -.088, -.019, None)])]
    for task, a_, b_, name, infs in CT:
        for sp, inf in zip(['oof_train', 'validation', 'test'], infs):
            wv = PM[(PM.task == task) & (PM.split == sp)].pivot(index='participant', columns='strategy', values='auc').sort_index()
            d_ = (wv[a_] - wv[b_]).dropna().to_numpy()
            lo, hi = boot(d_)
            r = con.loc[(task, sp, name)]
            ci_reg(S, f'V3 {task} {a_} − {b_}, {sp}', inf[:3], F, dict(delta=float(d_.mean()), low95=lo, high95=hi), 3, guardado=(r.delta, r.low, r.high))
            if inf[3] is not None:
                reg(S, f'V3 {task} {a_} − {b_}, {sp}: personas que mejoran', inf[3], F, int((d_ > 0).sum()), 0)
    dcon = 0.
    for (task, sp, name), r in con.iterrows():
        a_, b_ = {'gru_orden': ('gru_c32', 'gru_c1'), 'hgb_resumen': ('hgb_c32', 'hgb_c1'), 'hgb_c8': ('hgb_c8', 'hgb_c1'), 'hgb_c5_soporte': ('hgb_c5', 'hgb_c1'),
                  'hgb_c32_vs_c5': ('hgb_c32', 'hgb_c5'), 'historial_completo': ('hgb_c32', 'hgb_c32_etiq'), 'tardia_vs_temprana_c1': ('tardia_c1', 'hgb_c1'),
                  'tardia_vs_temprana_c32': ('tardia_c32', 'hgb_c32'), 'gru_vs_hgb_c32': ('gru_c32', 'hgb_c32')}[name]
        wv = PM[(PM.task == task) & (PM.split == sp)].pivot(index='participant', columns='strategy', values='auc').sort_index()
        d_ = (wv[a_] - wv[b_]).dropna().to_numpy()
        lo, hi = boot(d_)
        dcon = max(dcon, abs(d_.mean() - r.delta), abs(lo - r.low), abs(hi - r.high), abs(int((d_ > 0).sum()) - r.improved))
    reg(S, f'V3: diferencia máxima de los {len(con)} contrastes (delta, IC, personas) frente a contrastes.csv', 0, 'cierre_v3 contrastes.csv', dcon, 9, veredicto='coincide' if dcon < 1e-9 else 'difiere')
    bq = pd.read_csv(D / 'busqueda_interna_activacion.csv')
    sel = bq[bq.context.eq(32)].groupby('leaves').auc.mean()
    reg(S, 'V3: selección de hojas de activación, AUC media del modelo de 32 ventanas con 15 hojas (solo agregación del CSV)', .5311, 'Cierre, límites', float(sel[15]), 4)
    reg(S, 'V3: ídem con 7 hojas (solo agregación del CSV)', .4994, 'Cierre, límites', float(sel[7]), 4)
    allm = bq.groupby('leaves').auc.mean()
    reg(S, 'V3: hojas elegidas con la media de los tres largos de historial (0 = 15 hojas)', 0, 'INFORME cierre V3', 0 if allm.idxmax() == 15 else 1, 0, nota=f'7 hojas {allm[7]:.6f}; 15 hojas {allm[15]:.6f}')
    # ---------- análisis final: heterogeneidad por grupo
    Df = RES / 'cierre_final_41p_16-11-2026'
    F = 'INFORME análisis final'
    het = pd.read_csv(Df / 'heterogeneidad_por_grupo.csv')
    mf = pd.read_csv(Df / 'metricas.csv').set_index(['task', 'strategy'])
    wf = {}
    dba = 0.
    for task in ['atencion', 'activacion']:
        pr = pd.read_csv(Df / f'predicciones_{task}.csv.gz')
        wf[task] = person_auc(pr).pivot(index='participant', columns='strategy', values='auc').sort_index()
        for (strat, q), g in pr.groupby(['strategy', 'participant']):
            pass
        ba = pr.groupby(['strategy', 'participant']).apply(lambda g: clf_metrics(g.y, g.prob)['ba']).groupby('strategy').mean()
        for strat, v in ba.items():
            dba = max(dba, abs(v - mf.loc[(task, strat), 'ba']), abs(wf[task][strat].mean() - mf.loc[(task, strat), 'auc']))
    reg(S, 'Análisis final: diferencia máxima de AUC y BA medias frente a metricas.csv (10 filas)', 0, 'cierre_final metricas.csv', dba, 9, veredicto='coincide' if dba < 1e-9 else 'difiere')
    HI = {('atencion', 'hgb'): [(.023, .014, .031, 22), (.032, .016, .048, 14)], ('activacion', 'hgb'): [(.055, .012, .101, 17), (.001, -.052, .055, 7)],
          ('activacion', 'gru'): [(.045, .007, .083, 17), (.059, .014, .102, 11)], ('atencion', 'gru'): [(None, None, None, 15), (None, None, None, 11)]}
    for (task, fam), infs in HI.items():
        d_ = wf[task][f'{fam}_c32'] - wf[task][f'{fam}_c1']
        istr = d_.index.map(split).isin(['train'])
        for grp, mask, inf in [('train (25)', istr, infs[0]), ('validación+test (16)', ~istr, infs[1])]:
            v = d_[mask].to_numpy()
            lo, hi = boot(v)
            r = het[(het.task == task) & (het.grupo == grp) & (het.contraste == f'{fam}_c32 − {fam}_c1')].iloc[0]
            nmg = '25 de entrenamiento' if grp.startswith('train') else '16 de validación y test'
            if inf[0] is None:
                reg(S, f'Heterogeneidad {task} {fam.upper()} 32 − 1, {nmg}: delta', float(r.delta), 'heterogeneidad_por_grupo.csv', float(v.mean()), 4, guardado=float(r.delta))
            else:
                reg(S, f'Heterogeneidad {task} {fam.upper()} 32 − 1, {nmg}: delta', inf[0], F + '; cierre', float(v.mean()), 3, guardado=float(r.delta), nota=f'n={len(v)}')
                reg(S, f'Heterogeneidad {task} {fam.upper()} 32 − 1, {nmg}: IC 95 % inferior (semilla registrada)', inf[1], F + '; cierre', lo, 3, guardado=float(r.low95),
                    nota=f'el CSV guarda {r.low95}; diferencia {lo - r.low95:+.5f}')
                reg(S, f'Heterogeneidad {task} {fam.upper()} 32 − 1, {nmg}: IC 95 % superior (semilla registrada)', inf[2], F + '; cierre', hi, 3, guardado=float(r.high95),
                    nota=f'el CSV guarda {r.high95}; diferencia {hi - r.high95:+.5f}')
            reg(S, f'Heterogeneidad {task} {fam.upper()} 32 − 1, {nmg}: personas que mejoran', inf[3], F, int((v > 0).sum()), 0, nota=f'de {len(v)}')
    # ---------- tabla del cierre: contrastes de activación por grupo de personas
    FC = 'Cierre, tabla de la auditoría de código'
    Ract = rep('activacion')
    wr = wide_mean(Ract[Ract.strategy.isin(['hgb_c1', 'hgb_c32', 'c1_ts', 'c32_ts'])])
    P3 = wide_mean(pd.concat([pd.read_csv(RES / f'reapertura_fase3_41p_22-11-2026/pos_activacion_{sd}.csv.gz') for sd in SEEDS]))
    ex = person_auc(pd.read_csv(RES / 'explicativo_posicion_41p_18-11-2026/predicciones_activacion.csv.gz')).pivot(index='participant', columns='strategy', values='auc').sort_index()
    r1 = person_auc(pd.read_csv(RES / 'cierre_robustez_41p_16-11-2026/r1_activacion.csv.gz')).pivot(index='participant', columns='strategy', values='auc').sort_index()
    l6 = person_auc(pd.read_csv(RES / 'ampliacion_41p_16-11-2026/enmienda_e1_lag6/predicciones_activacion.csv.gz')).pivot(index='participant', columns='strategy', values='auc').sort_index()
    lg = person_auc(pd.read_csv(RES / 'reapertura_41p_22-11-2026/lag_activacion.csv.gz')).pivot(index='participant', columns='strategy', values='auc').sort_index()
    wa = wf['activacion']
    l6cols = list(l6.columns)
    real6 = [c for c in l6cols if 'real' in c][0]
    plc6 = [c for c in l6cols if 'placebo' in c][0]
    TAB = [('Principal, 16-11', wa.hgb_c32 - wa.hgb_c1, .034, (.055, .012, .101), (.001, -.052, .055)),
           ('Principal, 5 particiones', wr.hgb_c32 - wr.hgb_c1, .036, (.046, .012, .086), (.021, -.017, .060)),
           ('Con tiempo de sesión', wr.c32_ts - wr.c1_ts, .026, (.050, .013, .085), (-.011, -.066, .038)),
           ('Con posición (Q1)', P3.c32_pos - P3.pos_c1, .032, (.049, .018, .081), (.006, -.043, .049)),
           ('Historial − posición (18-11)', wa.hgb_c32 - ex.pos_c1, .038, (.063, .021, .109), (-.001, -.056, .054)),
           ('Historial − placebo (16-11)', wa.hgb_c32 - r1.placebo_c32, .038, (.057, .023, .092), (.008, -.048, .058)),
           ('Historial desplazado 6 − placebo', l6[real6] - l6[plc6], .046, (.035, .003, .064), (.064, .015, .115)),
           ('Banda de 6 s − placebo', lg.lag6 - lg.placebo, .047, (.058, .015, .101), (.030, -.003, .068)),
           ('GRU hasta 32 − GRU una ventana', wa.gru_c32 - wa.gru_c1, .051, (.045, .007, .083), (.059, .014, .101))]
    for name, d_, tot, i25, i16 in TAB:
        d_ = d_.dropna()
        istr = d_.index.map(split).isin(['train'])
        reg(S, f'Tabla por grupo · {name}: todas', tot, FC, float(d_.mean()), 3, nota=f'n={len(d_)}')
        for lab_, mask, inf in [('25 de la búsqueda', istr, i25), ('16 restantes', ~istr, i16)]:
            v = d_[mask].to_numpy()
            lo, hi = boot(v)
            ci_reg(S, f'Tabla por grupo · {name}: {lab_}', inf, FC, dict(delta=float(v.mean()), low95=lo, high95=hi), 3, nota=f'n={len(v)}; {int((v > 0).sum())} a favor')
    # diferencia entre grupos del contraste principal (permutación de etiquetas de grupo, descriptiva)
    d_ = (wa.hgb_c32 - wa.hgb_c1)
    istr = d_.index.map(split).isin(['train'])
    obs = d_[istr].mean() - d_[~istr].mean()
    rng = np.random.default_rng(20261127)
    v = d_.to_numpy()
    perm = np.array([(lambda m: v[m].mean() - v[~m].mean())(rng.permutation(istr)) for _ in range(20000)])
    reg(S, 'Principal 16-11 de activación: diferencia entre grupos (25 − 16) y p por permutación de grupo', None, 'Cierre, límites ("no es significativa con 16 personas")', float(obs),
        nota=f'p bilateral {float((np.abs(perm) >= abs(obs)).mean()):.4f} (20.000 permutaciones, semilla 20261127)')
    # robustez: frase "+0,042 en las tres"
    r3 = pd.read_csv(RES / 'cierre_robustez_41p_16-11-2026/r3_activacion.csv.gz')
    for sd, g in r3.groupby('seed'):
        wv = person_auc(g).pivot(index='participant', columns='strategy', values='auc')
        reg(S, f'Robustez R3 activación, partición {sd}', .042, 'INFORME robustez ("+0,042 en las tres")', float((wv.hgb_c32 - wv.hgb_c1).mean()), 3)


SECTIONS = {}


def main():
    want = sys.argv[1:]
    src, W = load_windows()
    say('ventanas', len(W), 'personas', W.participant.nunique(), f'{time.time() - T0:.0f}s')
    att = attention_score(W)
    W['score'], W['y_att'] = att[1].to_numpy(), att[2].to_numpy()
    ctx = dict(src=src, W=W, att=att, y_act=rebuild_gsr_v2(W)[0])
    for name, fn in SECTIONS.items():
        if want and name not in want:
            continue
        say(f'\n===== {name}')
        fn(ctx)
        say(f'    ({time.time() - T0:.0f}s)')
    if not want:
        df = pd.DataFrame(REG)
        df.to_csv(HERE / 'registro.csv', index=False)
        (HERE / 'registro.json').write_text(json.dumps(REG, indent=1, ensure_ascii=False, default=float))
        say('\nRecuento por veredicto:\n' + df.veredicto.value_counts().to_string())


SECTIONS['etiquetas'] = lambda c: c.update(y_act=sec_etiquetas(c['src'], c['W'], c['att']))
SECTIONS['ampliacion'] = lambda c: sec_ampliacion(c['W'])
SECTIONS['enfoques'] = lambda c: sec_enfoques(c['W'], c['y_act'])
SECTIONS['reapertura'] = lambda c: sec_reapertura(c['W'], c['y_act'])
SECTIONS['montaje'] = lambda c: c.update(five=sec_montaje())
SECTIONS['limpieza'] = lambda c: sec_limpieza(c['W'], c.get('five') or sample_people()[0])
SECTIONS['red'] = lambda c: sec_red(c['W'], c['y_act'])
SECTIONS['etapas1611'] = lambda c: sec_1611(c['W'])
# --FIN-SECCIONES--
if __name__ == '__main__':
    main()
