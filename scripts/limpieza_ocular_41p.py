"""Limpieza de artefactos oculares en el EEG y detección de atención (23-11-2026).

Continuación pedida por Mario el 23-11-2026 del pendiente 2 de los cuatro enfoques. Registrado antes de correr;
se ejecuta una vez. Análisis dirigido: las 41 personas y los resultados del 22-11 ya se vieron.

Pregunta: ¿cuánto de la detección de la etiqueta de atención desde el EEG (AUC 0,681 en el enfoque 2) se
sostiene cuando se quitan del EEG los componentes ligados a los movimientos de ojos y parpadeos?

Lo ya visto antes de registrar (sin etiquetas ni modelos, `montaje_ocular_41p.py`): la respuesta a parpadeos y
a la mirada horizontal por canal es compatible con el montaje por defecto de OpenBCI, y el EEG va 0,25–0,5 s
desfasado respecto del seguidor ocular. Con eso se fijaron las referencias y el desfase de abajo.

Limpieza (por persona, sin etiquetas, con toda la sesión; transductiva como la normalización por persona):
  ICA    FastICA (semilla fija) sobre los canales utilizables de la sesión, señal continua 1–45 Hz con notch
         de 50 Hz, sin las muestras a menos de 1 s de una saturación. Puntaje ocular de cada componente:
         máxima correlación absoluta (1–15 Hz) con mirada horizontal, mirada vertical o parpadeo del seguidor
         ocular, en el desfase de la persona ± 5 muestras. Se quitan los k componentes de mayor puntaje.
         Principal k = 3; k = 1, 2 y 4 son descriptivos.
  ctrl3  Control: se quitan los 3 componentes de mayor varianza entre los que NO están en los 4 más oculares.
  reg12  Segundo método, descriptivo: a cada canal se le resta su regresión lineal sobre Fp1, Fp2, F7 y F8
         (canales 0, 1, 8, 9 según el montaje por defecto) y esos cuatro canales se descartan. Se compara con
         orig12: los mismos 12 canales sin regresión.
La limpieza es un filtro espacial fijo por persona, aplicado a cada ventana cruda; las variables se recalculan
con el mismo código de extracción (`eeg_por_canal_v2.extract_window` y `eeg_features`). Con el filtro identidad
se debe reproducir la tabla de variables vigente (verificación obligatoria antes de modelar). En una ventana,
un canal no utilizable no entra en la estimación de los componentes y queda sin tocar.

Modelos: atención, solo EEG, ventana actual, configuración congelada (HGB, 7 hojas), las mismas 5 particiones
(semillas 1101–1105) y ventanas. Comparadores ya corridos el 22-11 (enfoque 2): eeg_c1 y los subconjuntos.

Familia confirmatoria (Holm sobre 4), AUC por persona promediada sobre las 5 particiones:
  L1 eeg_c1 − ica3_full                 cuánto cae la detección al quitar los componentes oculares
  L2 ctrl3_full − ica3_full             la caída es propia de los componentes oculares y no de quitar componentes
  L3 ica3_full − 0,5                    detección que queda tras la limpieza
  L4 ica3_alfa_beta − eeg_alfa_beta     la detección por alfa y beta no depende de los componentes quitados
Lectura fijada: L1 y L2 con respaldo = parte de la detección viaja en componentes oculares, de tamaño L1.
L3 con respaldo = queda detección tras la limpieza; no prueba origen cerebral, porque ninguna limpieza es
perfecta y la etiqueta es ocular. L4 nulo concluyente = la detección por alfa y beta no viene de esos
componentes.

Descriptivos: AUC de todos los modelos, curva por k, subconjuntos limpios (lento y amplitud, frontal,
posterior), reg12 frente a orig12, control con etiquetas barajadas (una partición), calidad de la limpieza
(amplitud del parpadeo y correlación con las referencias antes y después), Spearman de la probabilidad con las
variables oculares, y reproducción de eeg_c1 con el filtro identidad en una partición.

Reglas de decisión (las mismas, margen 0,02): respaldo: p Holm < 0,05 e IC 95 % inferior > 0; efecto relevante:
además IC 95 % inferior > 0,02; nulo concluyente: IC 90 % dentro de (−0,02; +0,02); inferior: IC 95 % superior
< 0; resto: inconcluso.
"""
from __future__ import annotations
import argparse, json
from multiprocessing import Pool
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.signal import butter, sosfiltfilt, iirnotch, filtfilt
from scipy.stats import spearmanr
from sklearn.decomposition import FastICA
from threadpoolctl import threadpool_limits
from atencion_binaria import ROOT, digest, write
from preprocesamiento_secuencial import eeg_features
from eeg_por_canal_v2 import extract_window, BANDS, FS
from reconstruir_profesor_atencion_binaria import COLUMNS
import cierre_experimental_v3 as V3
import cierre_final_41p as F
import reapertura_41p as R
import enfoques_41p as E
import montaje_ocular_41p as M

OUT = ROOT / 'resultados/limpieza_ocular_41p_23-11-2026'
FEAT = M.CACHE.parent / 'limpieza_ocular_variables'   # fuera de Git; se registran sus hashes
SEEDS = R.REP_SEEDS
ICA_SEED, SHUFFLE_SEED = 20261123, 20261125
KS, K_MAIN = [1, 2, 3, 4], 3
EOG = [0, 1, 8, 9]
CONDS = ['identidad'] + [f'ica{k}' for k in KS] + ['ctrl3', 'reg12', 'orig12']
BROAD = butter(4, [1, 45], btype='bandpass', fs=FS, output='sos')
NOTCH = iirnotch(50, 30, fs=FS)
FULL = V3.GROUPS['atencion']['EEG']
AGG = [c for c in FULL if not c.startswith(('eegch', 'eegsp'))]
COLS12 = [c for c in FULL if not (c.startswith('eegch') and int(c[5:7]) in EOG)]


def model_list():
    sets = E.eeg_sets()
    m = [(f'ica{k}_full', f'ica{k}', FULL) for k in KS] + [('ctrl3_full', 'ctrl3', FULL)]
    m += [(f'ica3_{name[4:]}', 'ica3', cols) for name, cols in sets.items()]
    return m + [('reg12', 'reg12', COLS12), ('orig12', 'orig12', COLS12)]


def plan():
    return json.loads((OUT / 'protocolo.json').read_text())


def inputs():
    paths = [Path(__file__), *(ROOT / f'scripts/{n}.py' for n in
             ['montaje_ocular_41p', 'cache_crudos_ocular', 'eeg_por_canal_v2', 'preprocesamiento_secuencial', 'enfoques_41p',
              'reapertura_41p', 'cierre_final_41p', 'cierre_experimental_v3']),
             R.OUT / 'protocolo.json', V3.SOURCE, V3.PARTS, V3.TEACHER, *V3.SPATIAL,
             *(E.OUT / f'e2_{s}.csv.gz' for s in SEEDS)]
    return {str(p.relative_to(ROOT)): digest(p) for p in paths}


def prepare():
    OUT.mkdir(exist_ok=False)
    write(OUT / 'protocolo.json', dict(
        created_utc=pd.Timestamp.now(tz='UTC').isoformat(),
        approval='Mario pide continuar el 23-11-2026; se aborda el pendiente 2 de los cuatro enfoques. Registrado antes de correr.',
        directed=True, inputs=inputs(),
        raw={p.name: digest(p) for p in sorted(M.CACHE.glob('*.npz'))},
        leaves=F.LEAVES, folds_rep=R.plan()['folds_rep'], margin=F.MARGIN,
        cleaning=dict(ica='FastICA unit-variance, max_iter 2000, tol 1e-4', ica_seed=ICA_SEED, ks=KS, k_main=K_MAIN,
                      control='3 componentes de mayor varianza fuera de los 4 más oculares', eog_channels=EOG,
                      band_fit=[1, 45], band_score=[1, 15], rail_guard_s=1, lag_window_samples=5),
        models=[m[0] for m in model_list()] + ['identidad_full (semilla 1101)', 'control_barajado (semilla 1101)'],
        confirmatory=['L1 eeg_c1 − ica3_full', 'L2 ctrl3_full − ica3_full', 'L3 ica3_full − 0,5',
                      'L4 ica3_alfa_beta − eeg_alfa_beta'], holm='sobre las 4 pruebas',
        decision=dict(respaldo='p Holm < 0,05 e IC95 inferior > 0', relevante='además IC95 inferior > 0,02',
                      nulo='IC90 dentro de (−0,02; +0,02)', inferior='IC95 superior < 0', resto='inconcluso'),
        limits='Análisis dirigido. La limpieza usa toda la sesión de cada persona, también de las evaluadas, y usa '
               'la mirada para elegir qué componentes quitar; solo puede restar información ligada a la mirada. '
               'Con 16 canales la ICA separa de forma imperfecta. Las ventanas de EEG conservan el desfase de '
               '0,25–0,5 s respecto del seguidor ocular. La zona frontal/posterior y reg12 usan el montaje por '
               'defecto, respaldado por los datos pero no documentado.'))
    print('Registrado', OUT / 'protocolo.json')


def verify():
    p = plan()
    for path, h in p['inputs'].items():
        assert digest(ROOT / path) == h, path
    return p


# ---------------------------------------------------------------- limpieza por persona
def fit_person(d):
    """Filtros espaciales de la persona. Devuelve matrices 16x16 de la parte que se resta, por condición."""
    t, x = d['eeg_t'], d['eeg']
    inside = (t >= d['gaze_t'][0]) & (t <= d['gaze_t'][-1])
    t, x = t[inside], x[inside]
    good = M.good_channels(x)
    G = np.flatnonzero(good)
    xb = sosfiltfilt(BROAD, filtfilt(*NOTCH, x[:, G], axis=0), axis=0)
    rail = (np.abs(x[:, G]) >= 180000).any(axis=1).astype(float)
    keep = np.convolve(rail, np.ones(int(2 * FS) + 1), 'same') < .5
    ica = FastICA(n_components=len(G), whiten='unit-variance', random_state=ICA_SEED, max_iter=2000, tol=1e-4)
    ica.fit(xb[keep])
    W, A = ica.components_, ica.mixing_
    x15 = sosfiltfilt(M.SOS, xb, axis=0)
    S15 = (x15 - x15.mean(0)) @ W.T
    ref, onsets = M.references(dict(d, eeg_t=t, eeg=x))
    cc = np.array([[np.abs(M.lagged_corr(ref[:, j], x15, L)).max() for L in M.LAGS] for j in range(3)])
    lag = int(M.LAGS[np.unravel_index(cc.argmax(), cc.shape)[1]])
    near = range(lag - 5, lag + 6)
    score = np.max([[np.abs(M.lagged_corr(ref[:, j], S15, L)) for L in near] for j in range(3)], axis=(0, 1))
    order = np.argsort(-score)
    var = (A ** 2).sum(axis=0)
    rest = order[4:]
    ctrl = rest[np.argsort(-var[rest])][:K_MAIN]

    def embed(part):
        m = np.zeros((16, 16))
        m[np.ix_(G, G)] = part
        return m
    removed = {f'ica{k}': embed(A[:, order[:k]] @ W[order[:k]]) for k in KS}
    removed['ctrl3'] = embed(A[:, ctrl] @ W[ctrl])
    eog, target = [c for c in G if c in EOG], [c for c in G if c not in EOG]
    reg = np.zeros((16, 16))
    if eog:
        gi = {c: i for i, c in enumerate(G)}
        beta = np.linalg.lstsq(xb[keep][:, [gi[c] for c in eog]], xb[keep][:, [gi[c] for c in target]], rcond=None)[0]
        reg[np.ix_(target, eog)] = beta.T
    removed['reg12'] = reg

    def quality(part, cols):   # canales `cols` (posiciones en G), 1–15 Hz, en el desfase de la persona
        y = (x15 - x15 @ part.T)[:, cols]
        r = [float(np.abs(M.lagged_corr(ref[:, j], y, lag)).max()) for j in range(3)]
        idx = np.searchsorted(t, onsets + lag / FS)
        pre, post = int(.3 * FS), int(.7 * FS)
        idx = idx[(idx > pre) & (idx < len(t) - post)]
        amp = float(np.ptp(np.mean([y[i - pre:i + post] for i in idx], axis=0), axis=0).max()) if len(idx) else np.nan
        return dict(r_horizontal=r[0], r_vertical=r[1], r_parpadeo=r[2], blink_max_uv=amp)
    zero, every = np.zeros((len(G), len(G))), np.arange(len(G))
    rest12 = np.array([i for i, c in enumerate(G) if c not in EOG])
    parts = {'identidad': (zero, every), **{k: (v[np.ix_(G, G)], every) for k, v in removed.items() if k != 'reg12'},
             'orig12': (zero, rest12), 'reg12': (removed['reg12'][np.ix_(G, G)], rest12)}
    qual = [dict(condition=k, **quality(*v)) for k, v in parts.items()]
    info = dict(usable_channels=len(G), eog_usable=len(eog), lag_s=lag / FS, iterations=int(ica.n_iter_),
                **{f'score_{i + 1}': float(score[order[i]]) for i in range(4)},
                score_control_max=float(score[ctrl].max()), var_share_ica3=float(var[order[:3]].sum() / var.sum()),
                var_share_ctrl3=float(var[ctrl].sum() / var.sum()))
    return removed, qual, info, good


def window_usable(x):
    return (np.isfinite(x).mean(0) >= .95) & ((np.abs(x) >= 180000).mean(0) <= .01) & \
           ((np.abs(np.diff(x, axis=0)) < 1e-12).mean(0) < .99)


def clean_window(x, removed):
    """Resta la parte ocular estimada con los canales utilizables de la ventana; los no utilizables no se tocan."""
    ok = window_usable(x)
    part = ((x - np.median(x, axis=0)) * ok) @ removed.T
    part[:, ~ok] = 0
    return x - part


def window_features(x, gap, drop):
    if drop:
        x16 = x.copy()
        x16[:, EOG] = np.nan
        agg = eeg_features(np.delete(x, EOG, axis=1), FS, BANDS)
    else:
        x16, agg = x, eeg_features(x, FS, BANDS)
    return {**{k: agg[k] for k in AGG}, **extract_window(x16, gap)}


def person(args):
    p, windows = args
    with threadpool_limits(limits=1):
        d = dict(np.load(M.CACHE / f'{p}.npz'))
        removed, qual, info, good = fit_person(d)
        removed = {'identidad': np.zeros((16, 16)), 'orig12': np.zeros((16, 16)), **removed}
        t, x = d['eeg_t'], d['eeg']
        rows = {c: [] for c in CONDS}
        partial = 0
        for w in windows.itertuples(index=False):
            lo, hi = np.searchsorted(t, [pd.Timestamp(w.window_start_utc).timestamp(), pd.Timestamp(w.window_end_utc).timestamp()])
            xs, ts = x[lo:hi], t[lo:hi]
            assert len(xs) == int(w.eeg_n), (p, w.source_row)
            gap = float(np.diff(ts).max()) if len(ts) > 1 else 2.
            partial += int(len(xs) > 1 and (~window_usable(xs) & good).any())
            for c in CONDS:
                xc = clean_window(xs, removed[c]) if len(xs) > 1 else xs
                rows[c].append(dict(source_row=w.source_row, **window_features(xc, gap, c in ('reg12', 'orig12'))))
        np.savez_compressed(OUT / 'filtros' / f'{p}.npz', **removed)
    info['windows'], info['windows_channel_dropped'] = len(windows), partial
    print(p, info, flush=True)
    return p, {c: pd.DataFrame(r) for c, r in rows.items()}, [dict(participant=p, **q) for q in qual], dict(participant=p, **info)


def clean():
    """Ajusta los filtros y recalcula las variables de todas las ventanas. No usa etiquetas."""
    p = verify()
    for name, h in p['raw'].items():
        assert digest(M.CACHE / name) == h, name
    FEAT.mkdir(exist_ok=False)
    (OUT / 'filtros').mkdir(exist_ok=False)
    d = V3.load_data()
    jobs = [(q, g[['source_row', 'window_start_utc', 'window_end_utc', 'eeg_n']]) for q, g in d.groupby('participant')]
    with Pool(10) as pool:
        res = pool.map(person, jobs, chunksize=1)
    feats = {c: pd.concat([r[1][c] for r in res], ignore_index=True) for c in CONDS}
    # verificación: el filtro identidad reproduce la tabla vigente
    ref = d.set_index('source_row').loc[feats['identidad'].source_row]
    new = feats['identidad'].set_index('source_row')
    np.testing.assert_allclose(new[V3.CHANNELS].to_numpy(float), ref[V3.CHANNELS].to_numpy(float), rtol=1e-9, atol=1e-12, equal_nan=True)
    np.testing.assert_allclose(new[AGG].to_numpy(float), ref[AGG].to_numpy(float), rtol=2e-6, atol=1e-8, equal_nan=True)
    assert len(new) == len(d) and not feats['identidad'].source_row.duplicated().any()
    for c, f in feats.items():
        f.to_pickle(FEAT / f'{c}.pkl')
    pd.DataFrame(sum((r[2] for r in res), [])).to_csv(OUT / 'calidad_limpieza.csv', index=False)
    pd.DataFrame([r[3] for r in res]).to_csv(OUT / 'personas_limpieza.csv', index=False)
    write(OUT / 'limpieza.json', dict(identity_reproduces_current_features=True, rows=len(new),
                                      features={c: digest(FEAT / f'{c}.pkl') for c in CONDS}))
    print('Limpieza completa y verificada')


# ---------------------------------------------------------------- modelos
def run(seed):
    p = verify()
    done = json.loads((OUT / 'limpieza.json').read_text())
    dest = OUT / f'pred_{seed}.csv.gz'
    assert not dest.exists()
    T = V3.Task(V3.load_data(), 'atencion')
    rows = T.lab.source_row.to_numpy()
    feats = {}
    for c in CONDS:
        assert digest(FEAT / f'{c}.pkl') == done['features'][c], c
        feats[c] = pd.read_pickle(FEAT / f'{c}.pkl').set_index('source_row').loc[rows]
    models = model_list() + ([('identidad_full', 'identidad', FULL)] if seed == SEEDS[0] else [])
    rng = np.random.default_rng(SHUFFLE_SEED)
    preds = []
    for k, test_people in enumerate(E.folds_of(p, seed)):
        test = T.lab.participant.isin(test_people).to_numpy()
        fit, ev = np.flatnonzero(~test), np.flatnonzero(test)
        y, w = T.lab.y.to_numpy()[fit], V3.weights(T.lab.iloc[fit])
        for name, cond, cols in models:
            prep = V3.preprocessor().fit(feats[cond].iloc[fit][cols])
            Xf, Xe = (prep.transform(feats[cond].iloc[r][cols]).astype('float32') for r in (fit, ev))
            m = V3.fit_hgb(Xf, y, w, p['leaves']['atencion'])
            preds.append(E.base_of(T, ev).assign(prob=m.predict_proba(Xe)[:, 1], strategy=name, fold=k, seed=seed))
            if name == 'ica3_full' and seed == SEEDS[0]:   # control negativo: etiquetas barajadas dentro de cada persona
                ys, who = y.copy(), T.lab.participant.to_numpy()[fit]
                for q in np.unique(who):
                    ix = np.flatnonzero(who == q)
                    ys[ix] = rng.permutation(ys[ix])
                m = V3.fit_hgb(Xf, ys, V3.weights(T.lab.iloc[fit].assign(y=ys)), p['leaves']['atencion'])
                preds.append(E.base_of(T, ev).assign(prob=m.predict_proba(Xe)[:, 1], strategy='control_barajado', fold=k, seed=seed))
        print('limpieza', seed, 'fold', k, flush=True)
    pd.concat(preds).to_csv(dest, index=False)


def report():
    d = V3.load_data()
    new = pd.concat([pd.read_csv(OUT / f'pred_{s}.csv.gz') for s in SEEDS])
    old = E.load('e2')
    old = old[~old.strategy.isin(['control_barajado', 'gsr_c1'])]
    single = ['control_barajado', 'identidad_full']
    pred = pd.concat([new[~new.strategy.isin(single)], old])
    key = pred.groupby(['seed', 'strategy']).source_row.apply(lambda s: tuple(sorted(s)))
    assert key.nunique() == 1 and pred.groupby(['seed', 'source_row']).y.nunique().eq(1).all()
    w = E.mean_auc(pred)
    assert len(w) == 41
    w['azar'] = .5
    conf = E.family([dict(test='L1', contrast='eeg_c1 − ica3_full', **R.contrast(w, 'eeg_c1', 'ica3_full')),
                     dict(test='L2', contrast='ctrl3_full − ica3_full', **R.contrast(w, 'ctrl3_full', 'ica3_full')),
                     dict(test='L3', contrast='ica3_full − 0,5', **R.contrast(w, 'ica3_full', 'azar')),
                     dict(test='L4', contrast='ica3_alfa_beta − eeg_alfa_beta', **R.contrast(w, 'ica3_alfa_beta', 'eeg_alfa_beta'))])
    names = [m[0] for m in model_list()]
    desc = E.absolute(w, ['eeg_c1'] + names + list(E.eeg_sets()))
    pairs = [('eeg_c1', f'ica{k}_full') for k in KS] + [('eeg_c1', 'ctrl3_full'), ('orig12', 'reg12'), ('eeg_c1', 'orig12'),
             ('eeg_lento_amp', 'ica3_lento_amp'), ('eeg_frontal', 'ica3_frontal'), ('eeg_posterior', 'ica3_posterior'),
             ('ica3_full', 'ica3_alfa_beta'), ('ica3_lento_amp', 'ica3_alfa_beta'), ('ica3_frontal', 'ica3_posterior')]
    desc += [dict(item=f'{a} − {b}', **R.contrast(w, a, b)) for a, b in pairs]
    desc += [dict(item=f'{s} − 0,5', **R.contrast(w, s, 'azar')) for s in ['reg12', 'ica4_full', 'ica3_alfa_beta', 'ica3_posterior']]
    one = new[new.seed.eq(SEEDS[0])]
    w1 = E.mean_auc(pd.concat([one[one.strategy.isin(single)], old[old.seed.eq(SEEDS[0]) & old.strategy.eq('eeg_c1')]]))
    w1['azar'] = .5
    desc.append(dict(item='control barajado − 0,5 (una partición)', **R.contrast(w1, 'control_barajado', 'azar')))
    desc.append(dict(item='identidad_full − eeg_c1 (una partición; debe ser 0)', **R.contrast(w1, 'identidad_full', 'eeg_c1')))
    a = one[one.strategy.eq('identidad_full')].set_index('source_row').prob
    b = old[old.seed.eq(SEEDS[0]) & old.strategy.eq('eeg_c1')].set_index('source_row').prob
    desc.append(dict(item='máxima diferencia de probabilidad identidad_full frente a eeg_c1', delta=float((a - b.loc[a.index]).abs().max())))
    score, z = E.ocular(d)
    ref = z.assign(puntaje=score, source_row=d.source_row.to_numpy(), participant=d.participant.to_numpy())
    for strat in ['eeg_c1', 'ica3_full', 'ica3_alfa_beta', 'reg12']:
        m = pred[pred.strategy.eq(strat)].groupby('source_row').prob.mean().rename('prob').reset_index().merge(ref, on='source_row')
        for c in ['puntaje'] + COLUMNS:
            rho = m.groupby('participant').apply(lambda g: spearmanr(g.prob, g[c]).statistic).dropna()
            lo, hi = F.ci(rho)
            desc.append(dict(item=f'Spearman prob {strat} con {c}', delta=float(rho.mean()), low95=lo, high95=hi,
                             people=len(rho), improved=int((rho > 0).sum()), p=F.sign_flip(rho.to_numpy())))
    q = pd.read_csv(OUT / 'calidad_limpieza.csv')
    for c, g in q.groupby('condition', sort=False):
        for col in ['r_horizontal', 'r_vertical', 'r_parpadeo', 'blink_max_uv']:
            desc.append(dict(item=f'calidad {c}: mediana {col}', delta=float(g[col].median()), people=int(g[col].notna().sum())))
    conf.to_csv(OUT / 'confirmatorio.csv', index=False)
    pd.DataFrame(desc).to_csv(OUT / 'descriptivos.csv', index=False)
    w.drop(columns='azar').to_csv(OUT / 'auc_por_persona.csv')
    pd.set_option('display.width', 280)
    pd.set_option('display.max_rows', 500)
    print(conf.round(4).to_string(index=False))
    print(pd.DataFrame(desc).round(4).to_string(index=False))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['prepare', 'clean', 'run', 'report'])
    ap.add_argument('--seed', type=int)
    a = ap.parse_args()
    if a.phase == 'run':
        with threadpool_limits(limits=1):
            run(a.seed)
    else:
        globals()[a.phase]()
