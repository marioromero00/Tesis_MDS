"""Cuatro enfoques nuevos (22-11-2026), pedidos por Mario y registrados antes de correr.

Tras tres fases de reapertura, la hipótesis de temporalidad queda en apoyo parcial. Mario pide explorar cuatro
enfoques distintos. Cada uno tiene su familia de pruebas con Holm propio y las reglas de decisión del análisis
final (margen 0,02). Se ejecuta una vez. Configuración de modelos congelada (HGB 7 hojas en atención, 15 en
activación), 5 particiones por persona (semillas 1101-1105), AUC por persona promediada sobre particiones.
Las 41 personas ya se consultaron: son análisis dirigidos, no confirmaciones independientes. E1 y E3 cambian la
definición del objetivo por orden explícita de Mario; las etiquetas originales no se modifican ni se reemplazan.

E1 Etiqueta de atención corregida por posición.
   La etiqueta original es 1 si el puntaje ocular (PCA de fijaciones, dispersión, recorrido y pupila) supera la
   mediana de la persona. Su prevalencia depende de los segundos transcurridos en el estímulo. Etiqueta corregida:
   1 si el puntaje supera la mediana de la persona DENTRO del mismo tramo de posición (1, 2, 3, 4, 5, 6-8, 9-12,
   13-20, 21-32 s). Así cada persona tiene la mitad de positivos en cada tramo y la posición deja de informar.
   Pruebas (Holm sobre 3):
     A1 AUC sin historial con etiqueta corregida − AUC sin historial con etiqueta original (¿se conserva la detección?)
     A2 historial hasta 32 − sin historial, etiqueta corregida (¿desaparece la mejora del historial?)
     A3 (historial + posición) − (actual + posición), etiqueta corregida
   Descriptivos: AUC de la posición sola, concordancia entre etiquetas, prevalencia por tramo.

E2 Detección cruzada: señales no oculares que predicen una etiqueta construida con mirada y pupila (atención,
   etiqueta original).
   Modelos sin historial: solo EEG, solo GSR, EEG + GSR (este último ya existe de la fase 1).
   Pruebas (Holm sobre 4): AUC solo EEG − 0,5; AUC solo GSR − 0,5; (EEG + GSR) − solo EEG; solo EEG − solo GSR.
   Control negativo: modelo entrenado con etiquetas barajadas dentro de cada persona (una partición); debe dar 0,5.
   Descriptivos: correlación de Spearman por persona entre la probabilidad del modelo y el puntaje ocular continuo
   y cada uno de sus cinco componentes; AUC a igual posición; personas sobre 0,5.

E3 Activación a nivel de estímulo.
   Unidad: el segmento (persona, grabación, segmento, estímulo). Objetivo: mayoría de las etiquetas de activación
   de sus ventanas (se excluyen empates). Entradas: media y desviación, sobre todas las ventanas del segmento, de
   las mismas variables (EEG, mirada, pupila; sin GSR). Es una clasificación offline del estímulo completo.
   Referencia: promediar por segmento las probabilidades de los modelos por ventana de la fase 1.
   Pruebas (Holm sobre 3): AUC del modelo de segmento − 0,5; modelo de segmento − promedio del modelo por ventana
   con historial; (segmento + duración) − solo duración.
   Descriptivos: solo duración, promedio del modelo por ventana sin historial, AUC absolutas.

E4 Diferencias entre personas.
   (a) Fiabilidad, sin entrenar: se separan los segmentos de cada persona en pares e impares por orden temporal y
       se correlaciona entre personas (Spearman) la AUC sin historial y la ganancia del historial de una mitad con
       la otra. Si la ganancia individual no es fiable, las diferencias entre personas son ruido.
   (b) Correlatos, sin entrenar: Spearman entre la AUC y la ganancia de cada persona y sus características
       (ventanas etiquetadas, calidad y cobertura de señales, deriva de la etiqueta en la sesión, largo de segmentos).
       Holm dentro de cada tarea y resultado. Descriptivo.
   (c) Adaptación a la persona: al modelo general se le agregan, para entrenar, las ventanas etiquetadas de los
       segmentos que empiezan en el primer 40 % de la sesión de cada persona evaluada. Se evalúa en los segmentos
       que empiezan después de ese punto más 10 s, y se compara con el modelo general en esas mismas ventanas.
       Pruebas (Holm sobre 4): adaptado − general, sin historial y con historial, en atención y activación.

Reglas de decisión: respaldo: p Holm < 0,05 e IC 95 % inferior > 0; efecto relevante: además IC 95 % inferior
> 0,02; nulo concluyente: IC 90 % dentro de (−0,02; +0,02); inferior: IC 95 % superior < 0; resto: inconcluso.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import roc_auc_score, cohen_kappa_score
from threadpoolctl import threadpool_limits
from atencion_binaria import ROOT, digest, write
from reconstruir_profesor_atencion_binaria import components, binary, COLUMNS
import cierre_experimental_v3 as V3
import cierre_final_41p as F
import reapertura_41p as R

OUT = ROOT / 'resultados/enfoques_41p_22-11-2026'
SEEDS = R.REP_SEEDS
POS_EDGES = [1, 2, 3, 4, 5, 8, 12, 20]   # tramos: 1, 2, 3, 4, 5, 6-8, 9-12, 13-20, 21-32
SHUFFLE_SEED = 20261124
CAL_FRACTION, CAL_GAP = .4, 10
SEG = ['participant', 'recording', 'segment_id', 'stimulus']
COVARIATES = ['ventanas_etiquetadas', 'eeg_utilizable', 'cobertura_eeg', 'cobertura_pupila', 'cobertura_mirada',
              'deriva_sesion', 'largo_medio_segmento', 'duracion_sesion']


def plan():
    return json.loads((OUT / 'protocolo.json').read_text())


def inputs():
    paths = [Path(__file__), ROOT / 'scripts/reapertura_41p.py', ROOT / 'scripts/cierre_final_41p.py',
             ROOT / 'scripts/cierre_experimental_v3.py', ROOT / 'scripts/temporales_core.py',
             ROOT / 'scripts/reconstruir_profesor_atencion_binaria.py', R.OUT / 'protocolo.json',
             V3.SOURCE, V3.PARTS, V3.LABELS_ACT, V3.TEACHER, *V3.SPATIAL]
    paths += [R.OUT / f'rep_{t}_{s}.csv.gz' for t in F.LEAVES for s in SEEDS]
    return {str(p.relative_to(ROOT)): digest(p) for p in paths}


def prepare():
    OUT.mkdir(exist_ok=False)
    write(OUT / 'protocolo.json', dict(
        created_utc=pd.Timestamp.now(tz='UTC').isoformat(),
        approval='Mario pide los enfoques 1 a 4 el 22-11-2026 (etiqueta de atención corregida, detección cruzada, '
                 'activación a nivel de estímulo, diferencias entre personas). Registrado antes de correr.',
        directed=True, inputs=inputs(), leaves=F.LEAVES, hgb=V3.HGB, folds_rep=R.plan()['folds_rep'], seeds=SEEDS,
        pos_edges=POS_EDGES, shuffle_seed=SHUFFLE_SEED, cal_fraction=CAL_FRACTION, cal_gap=CAL_GAP, margin=F.MARGIN,
        families=dict(
            E1=['A1 c1 corregida − c1 original', 'A2 c32 − c1 (corregida)', 'A3 c32_pos − pos_c1 (corregida)'],
            E2=['eeg_c1 − 0,5', 'gsr_c1 − 0,5', 'hgb_c1 − eeg_c1', 'eeg_c1 − gsr_c1'],
            E3=['seg − 0,5', 'seg − agg_c32', 'seg_dur − dur_only'],
            E4c=['pers_c1 − hgb_c1 y pers_c32 − hgb_c32, en atención y activación']),
        holm='dentro de cada familia', unit='AUC por persona promediada sobre las 5 particiones; diferencia pareada',
        descriptive=['E1 posición sola, concordancia, prevalencias', 'E2 control barajado, Spearman con puntaje y '
                     'componentes, AUC a igual posición', 'E3 duración sola, agg_c1', 'E4a fiabilidad por mitades',
                     'E4b correlatos con Holm por tarea y resultado'],
        decision=dict(respaldo='p Holm < 0,05 e IC95 inferior > 0', relevante='además IC95 inferior > 0,02',
                      nulo='IC90 dentro de (−0,02; +0,02)', inferior='IC95 superior < 0', resto='inconcluso'),
        limits='Análisis dirigidos sobre personas y resultados ya vistos. Etiquetas offline y variables '
               'transductivas por persona. E1: la etiqueta corregida usa medianas por persona y tramo calculadas con '
               'toda la sesión (offline, como la original). E3: usa todas las ventanas del segmento, incluidas las '
               'posteriores a cada etiqueta; no es causal. E4c: el modelo adaptado ve un 6 % más de datos; la '
               'evaluación es sobre la parte final de la sesión, distinta de la de los análisis anteriores.'))
    print('Registrado', OUT / 'protocolo.json')


def verify():
    p = plan()
    for path, h in p['inputs'].items():
        assert digest(ROOT / path) == h, path
    return p


# ---------------------------------------------------------------- variables comunes
def ocular(d):
    """Puntaje continuo del profesor (el mismo que define la etiqueta original) y sus componentes z."""
    teacher = joblib.load(V3.TEACHER)
    z, _ = components(d)
    ok = z.notna().all(axis=1)
    score = pd.Series(np.nan, index=d.index)
    score.loc[ok] = teacher['pca'].transform(z.loc[ok, COLUMNS]).ravel() * teacher['sign']
    y, _ = binary(score, d)
    assert (y.astype('float').fillna(-1).to_numpy() == d.y_atencion.fillna(-1).to_numpy()).all()
    return score, z


def corrected_attention(d):
    """Etiqueta de atención relativa a la mediana de la persona dentro del mismo tramo de posición."""
    score, _ = ocular(d)
    pos = R.stimulus_position(V3.Task(d, 'atencion')).astype(int)   # T.all conserva el orden de d
    tramo = np.digitize(pos, POS_EDGES, right=True)
    g = pd.DataFrame(dict(p=d.participant.to_numpy(), b=tramo, s=score.to_numpy()))
    med = g.groupby(['p', 'b']).s.transform('median')
    y = (g.s > med).astype(float).where(g.s.notna())
    return y.to_numpy(), tramo


def segment_ids(T):
    return T.all.groupby(SEG, sort=False).ngroup().to_numpy()


def folds_of(p, seed):
    return p['folds_rep'][str(seed)]


def base_of(T, rows):
    return T.lab.iloc[rows][['source_row', 'participant', 'y']]


# ---------------------------------------------------------------- corridas
def run_e1(seed):
    p = verify()
    dest = OUT / f'e1_{seed}.csv.gz'
    assert not dest.exists()
    d = V3.load_data()
    d['y_atencion'], _ = corrected_attention(d)
    T = V3.Task(d, 'atencion')
    pos = R.stimulus_position(T)
    preds = []
    for k, test_people in enumerate(folds_of(p, seed)):
        fit, ev, Za, Zl = R.fold_setup(T, test_people)
        y, w = T.lab.y.to_numpy()[fit], V3.weights(T.lab.iloc[fit])
        mats = {}
        for name, kind in [('hgb_c1', 1), ('hgb_c32', 32)]:
            mats[name] = tuple(V3.hgb_matrix(T, Za, Zl, r, kind) for r in (fit, ev))
        mats['pos_c1'] = tuple(np.column_stack([m, pos[T.lab_pos[r]]]) for m, r in zip(mats['hgb_c1'], (fit, ev)))
        mats['c32_pos'] = tuple(np.column_stack([m, pos[T.lab_pos[r]]]) for m, r in zip(mats['hgb_c32'], (fit, ev)))
        mats['pos_only'] = tuple(pos[T.lab_pos[r]][:, None] for r in (fit, ev))
        for name, (Xf, Xe) in mats.items():
            m = V3.fit_hgb(Xf, y, w, p['leaves']['atencion'])
            preds.append(base_of(T, ev).assign(prob=m.predict_proba(Xe)[:, 1], strategy=name, fold=k, seed=seed))
        print('e1', seed, 'fold', k, flush=True)
    pd.concat(preds).to_csv(dest, index=False)


def run_e2(seed):
    p = verify()
    dest = OUT / f'e2_{seed}.csv.gz'
    assert not dest.exists()
    T = V3.Task(V3.load_data(), 'atencion')
    groups = {'eeg_c1': V3.GROUPS['atencion']['EEG'], 'gsr_c1': V3.GROUPS['atencion']['GSR']}
    rng = np.random.default_rng(SHUFFLE_SEED)
    preds = []
    for k, test_people in enumerate(folds_of(p, seed)):
        fit, ev, Za, Zl = R.fold_setup(T, test_people)
        y, w = T.lab.y.to_numpy()[fit], V3.weights(T.lab.iloc[fit])
        for name, cols in groups.items():   # preprocesador propio por señal (imputación e indicadores de esa señal)
            prep = V3.preprocessor().fit(T.lab.iloc[fit][cols])
            Xf, Xe = (prep.transform(T.lab.iloc[r][cols]).astype('float32') for r in (fit, ev))
            m = V3.fit_hgb(Xf, y, w, p['leaves']['atencion'])
            preds.append(base_of(T, ev).assign(prob=m.predict_proba(Xe)[:, 1], strategy=name, fold=k, seed=seed))
        if seed == SEEDS[0]:   # control negativo: etiquetas barajadas dentro de cada persona, solo al entrenar
            ys = y.copy()
            person = T.lab.participant.to_numpy()[fit]
            for q in np.unique(person):
                ix = np.flatnonzero(person == q)
                ys[ix] = rng.permutation(ys[ix])
            m = V3.fit_hgb(Zl[fit], ys, w, p['leaves']['atencion'])
            preds.append(base_of(T, ev).assign(prob=m.predict_proba(Zl[ev])[:, 1], strategy='control_barajado', fold=k, seed=seed))
        print('e2', seed, 'fold', k, flush=True)
    pd.concat(preds).to_csv(dest, index=False)


def segment_table(T):
    """Segmentos con etiqueta de activación: objetivo por mayoría (sin empates) y número de ventanas."""
    seg = segment_ids(T)
    lab = pd.DataFrame(dict(seg=seg[T.lab_pos], participant=T.lab.participant.to_numpy(), y=T.lab.y.to_numpy()))
    t = lab.groupby('seg').agg(participant=('participant', 'first'), mean=('y', 'mean'), labelled=('y', 'size'))
    t['windows'] = pd.Series(seg).value_counts().reindex(t.index).to_numpy()
    t = t[t['mean'].ne(.5)].copy()
    t['y'] = (t['mean'] > .5).astype(int)
    return t.reset_index(), seg


def run_e3(seed):
    p = verify()
    dest = OUT / f'e3_{seed}.csv.gz'
    assert not dest.exists()
    T = V3.Task(V3.load_data(), 'activacion')
    tab, seg = segment_table(T)
    preds = []
    for k, test_people in enumerate(folds_of(p, seed)):
        _, _, Za, _ = R.fold_setup(T, test_people)
        g = pd.DataFrame(Za).groupby(seg)
        feats = np.column_stack([g.mean().reindex(tab.seg).to_numpy(), g.std(ddof=0).reindex(tab.seg).to_numpy()]).astype('float32')
        dur = tab.windows.to_numpy(dtype='float32')[:, None]
        te = tab.participant.isin(test_people).to_numpy()
        w = V3.weights(tab[~te])
        for name, X in [('seg', feats), ('seg_dur', np.column_stack([feats, dur])), ('dur_only', dur)]:
            m = V3.fit_hgb(X[~te], tab.y.to_numpy()[~te], w, p['leaves']['activacion'])
            preds.append(tab.loc[te, ['seg', 'participant', 'y']].assign(prob=m.predict_proba(X[te])[:, 1], strategy=name, fold=k, seed=seed))
        print('e3', seed, 'fold', k, flush=True)
    pd.concat(preds).to_csv(dest, index=False)


def calibration_split(T):
    """Para cada fila etiquetada: 'cal' si su segmento empieza en el primer 40 % de la sesión de la persona,
    'eval' si empieza después de ese punto + 10 s, '' en la franja intermedia."""
    ts = R.session_time(T)
    seg = segment_ids(T)
    start = pd.Series(ts).groupby(seg).transform('min').to_numpy()
    dur = pd.Series(ts).groupby(T.all.participant.to_numpy()).transform('max').to_numpy()
    cut = CAL_FRACTION * dur
    role = np.where(start <= cut, 'cal', np.where(start > cut + CAL_GAP, 'eval', ''))
    return role[T.lab_pos]


def run_e4(task, seed):
    p = verify()
    dest = OUT / f'e4_{task}_{seed}.csv.gz'
    assert not dest.exists()
    T = V3.Task(V3.load_data(), task)
    role = calibration_split(T)
    preds = []
    for k, test_people in enumerate(folds_of(p, seed)):
        fit, ev, Za, Zl = R.fold_setup(T, test_people)
        cal, ev = ev[role[ev] == 'cal'], ev[role[ev] == 'eval']
        rows = np.concatenate([fit, cal])
        y, w = T.lab.y.to_numpy()[rows], V3.weights(T.lab.iloc[rows])
        for name, kind in [('pers_c1', 1), ('pers_c32', 32)]:
            m = V3.fit_hgb(V3.hgb_matrix(T, Za, Zl, rows, kind), y, w, p['leaves'][task])
            preds.append(base_of(T, ev).assign(prob=m.predict_proba(V3.hgb_matrix(T, Za, Zl, ev, kind))[:, 1],
                                               strategy=name, fold=k, seed=seed, cal_rows=len(cal)))
        print('e4', task, seed, 'fold', k, flush=True)
    pd.concat(preds).to_csv(dest, index=False)


# ---------------------------------------------------------------- informe
def mean_auc(pred, key='participant'):
    """AUC por persona y estrategia, promediada sobre semillas. Filas: persona; columnas: estrategia."""
    rows = []
    for (seed, strat, person), g in pred.groupby(['seed', 'strategy', key]):
        if g.y.nunique() == 2:
            rows.append(dict(seed=seed, strategy=strat, participant=person, auc=roc_auc_score(g.y, g.prob)))
    return pd.DataFrame(rows).groupby(['participant', 'strategy']).auc.mean().unstack()


def family(rows):
    r = pd.DataFrame(rows)
    r['p_holm'] = R.holm(r.p)
    r['decision'] = [F.decide(x.delta, x.low95, x.high95, x.low90, x.high90, x.p_holm) for x in r.itertuples()]
    return r


def absolute(wide, cols, **extra):
    out = []
    for s in cols:
        v = wide[s].dropna()
        lo, hi = F.ci(v)
        out.append(dict(**extra, item=f'AUC {s}', delta=float(v.mean()), low95=lo, high95=hi, people=len(v),
                        improved=int((v > .5).sum())))
    return out


def load(prefix, task=None):
    name = (lambda s: f'{prefix}_{task}_{s}.csv.gz') if task else (lambda s: f'{prefix}_{s}.csv.gz')
    return pd.concat([pd.read_csv(OUT / name(s)) for s in SEEDS])


def rep(task, strategies=('hgb_c1', 'hgb_c32')):
    r = pd.concat([pd.read_csv(R.OUT / f'rep_{task}_{s}.csv.gz') for s in SEEDS])
    return r[r.strategy.isin(strategies)]


def report_e1(d):
    y_new, tramo = corrected_attention(d)
    T0 = V3.Task(d, 'atencion')
    new, old = load('e1'), rep('atencion')
    assert set(new.source_row) == set(old.source_row)
    wn, wo = mean_auc(new), mean_auc(old)
    both = wn.join(wo.add_suffix('_orig'))
    conf = family([dict(test='A1', contrast='hgb_c1 corregida − hgb_c1 original', **R.contrast(both, 'hgb_c1', 'hgb_c1_orig')),
                   dict(test='A2', contrast='hgb_c32 − hgb_c1 (corregida)', **R.contrast(wn, 'hgb_c32', 'hgb_c1')),
                   dict(test='A3', contrast='c32_pos − pos_c1 (corregida)', **R.contrast(wn, 'c32_pos', 'pos_c1'))])
    desc = absolute(wn, ['hgb_c1', 'hgb_c32', 'pos_c1', 'c32_pos', 'pos_only']) + absolute(wo, ['hgb_c1', 'hgb_c32'], label='original')
    desc.append(dict(item='pos_c1 − hgb_c1 (corregida)', **R.contrast(wn, 'pos_c1', 'hgb_c1')))
    desc.append(dict(item='hgb_c32 − hgb_c1 (original)', **R.contrast(wo, 'hgb_c32', 'hgb_c1')))
    lab = pd.DataFrame(dict(participant=d.participant.to_numpy(), tramo=tramo, orig=d.y_atencion.to_numpy(), corr=y_new)).dropna()
    kap = lab.groupby('participant').apply(lambda g: cohen_kappa_score(g.orig, g['corr']))
    lo, hi = F.ci(kap)
    desc.append(dict(item='kappa entre etiqueta original y corregida (por persona)', delta=float(kap.mean()), low95=lo, high95=hi, people=len(kap)))
    desc.append(dict(item='concordancia global entre etiquetas', delta=float((lab.orig == lab['corr']).mean()), people=lab.participant.nunique()))
    prev = lab.groupby('tramo')[['orig', 'corr']].mean()
    for b, r in prev.iterrows():
        desc.append(dict(item=f'prevalencia tramo {b}: original', delta=float(r.orig)))
        desc.append(dict(item=f'prevalencia tramo {b}: corregida', delta=float(r['corr'])))
    assert len(T0.lab) == len(lab)
    return conf, pd.DataFrame(desc)


def report_e2(d):
    T = V3.Task(d, 'atencion')
    new, old = load('e2'), rep('atencion', ('hgb_c1',))
    ctrl = new[new.strategy.eq('control_barajado')]
    pred = pd.concat([new[~new.strategy.eq('control_barajado')], old])
    w = mean_auc(pred)
    w['azar'] = .5
    conf = family([dict(test='B1', contrast='eeg_c1 − 0,5', **R.contrast(w, 'eeg_c1', 'azar')),
                   dict(test='B2', contrast='gsr_c1 − 0,5', **R.contrast(w, 'gsr_c1', 'azar')),
                   dict(test='B3', contrast='hgb_c1 − eeg_c1', **R.contrast(w, 'hgb_c1', 'eeg_c1')),
                   dict(test='B4', contrast='eeg_c1 − gsr_c1', **R.contrast(w, 'eeg_c1', 'gsr_c1'))])
    desc = absolute(w, ['eeg_c1', 'gsr_c1', 'hgb_c1'])
    wc = mean_auc(ctrl)
    wc['azar'] = .5
    desc.append(dict(item='control barajado − 0,5 (una partición)', **R.contrast(wc, 'control_barajado', 'azar')))
    # AUC a igual posición
    pos = pd.Series(R.stimulus_position(T)[T.lab_pos].astype(int), index=T.lab.source_row.to_numpy())
    pp = pred.assign(pos=pred.source_row.map(pos))
    st = pp.groupby(['seed', 'strategy', 'participant']).apply(lambda g: R.stratified_auc(g, 'pos')).rename('auc').reset_index()
    ws = st.groupby(['participant', 'strategy']).auc.mean().unstack()
    desc += absolute(ws, ['eeg_c1', 'gsr_c1', 'hgb_c1'], label='a igual posición')
    # Spearman por persona entre probabilidad media y puntaje ocular / componentes
    score, z = ocular(d)
    ref = z.assign(puntaje=score, source_row=d.source_row.to_numpy(), participant=d.participant.to_numpy())
    for strat in ['eeg_c1', 'hgb_c1']:
        m = pred[pred.strategy.eq(strat)].groupby('source_row').prob.mean().rename('prob').reset_index().merge(ref, on='source_row')
        for c in ['puntaje'] + COLUMNS:
            rho = m.groupby('participant').apply(lambda g: spearmanr(g.prob, g[c]).statistic).dropna()
            lo, hi = F.ci(rho)
            desc.append(dict(item=f'Spearman prob {strat} con {c}', delta=float(rho.mean()), low95=lo, high95=hi,
                             people=len(rho), improved=int((rho > 0).sum()), p=F.sign_flip(rho.to_numpy())))
    return conf, pd.DataFrame(desc)


def report_e3(d):
    T = V3.Task(d, 'activacion')
    tab, seg = segment_table(T)
    new = load('e3')
    smap = pd.Series(seg[T.lab_pos], index=T.lab.source_row.to_numpy())
    old = rep('activacion')
    old = old.assign(seg=old.source_row.map(smap))
    agg = old.groupby(['seed', 'strategy', 'seg']).prob.mean().reset_index().merge(tab[['seg', 'participant', 'y']], on='seg')
    agg['strategy'] = agg.strategy.map({'hgb_c1': 'agg_c1', 'hgb_c32': 'agg_c32'})
    w = mean_auc(pd.concat([new, agg]))
    w['azar'] = .5
    conf = family([dict(test='C1', contrast='seg − 0,5', **R.contrast(w, 'seg', 'azar')),
                   dict(test='C2', contrast='seg − agg_c32', **R.contrast(w, 'seg', 'agg_c32')),
                   dict(test='C3', contrast='seg_dur − dur_only', **R.contrast(w, 'seg_dur', 'dur_only'))])
    desc = absolute(w, ['seg', 'seg_dur', 'dur_only', 'agg_c1', 'agg_c32'])
    for a, b in [('seg', 'agg_c1'), ('agg_c32', 'agg_c1'), ('seg_dur', 'seg'), ('agg_c32', 'azar'), ('dur_only', 'azar')]:
        desc.append(dict(item=f'{a} − {b}', **R.contrast(w, a, b)))
    per = tab.groupby('participant').size()
    desc.append(dict(item='segmentos por persona (mediana)', delta=float(per.median()), low95=float(per.min()), high95=float(per.max()), people=len(per)))
    desc.append(dict(item='segmentos con etiqueta unánime (fracción)', delta=float(tab['mean'].isin([0, 1]).mean())))
    desc.append(dict(item='AUC ventana (rep) hgb_c32, referencia', delta=float(mean_auc(rep('activacion'))['hgb_c32'].mean())))
    return conf, pd.DataFrame(desc)


def halves(T):
    """Mitad (0/1) de cada fila etiquetada: segmentos de la persona alternados por orden temporal."""
    ts, seg = R.session_time(T), segment_ids(T)
    start = pd.DataFrame(dict(p=T.all.participant.to_numpy(), seg=seg, t=ts)).groupby(['p', 'seg']).t.min().reset_index()
    start = start[start.seg.isin(np.unique(seg[T.lab_pos]))].copy()   # solo segmentos con ventanas etiquetadas
    start['half'] = start.groupby('p').t.rank(method='first').astype(int) % 2
    return pd.Series(start.set_index('seg').half.reindex(seg[T.lab_pos]).to_numpy(), index=T.lab.source_row.to_numpy())


def spearman_ci(a, b, n=5000, seed=20261029):
    a, b = np.asarray(a, float), np.asarray(b, float)
    rng = np.random.default_rng(seed)
    ix = rng.integers(0, len(a), (n, len(a)))
    boot = [spearmanr(a[i], b[i]).statistic for i in ix]
    r = spearmanr(a, b)
    lo, hi = np.nanquantile(boot, [.025, .975])
    return dict(delta=float(r.statistic), low95=float(lo), high95=float(hi), p=float(r.pvalue), people=len(a))


def covariates(d, T):
    ts = R.session_time(T)
    a = T.all.assign(ts=ts, seg=segment_ids(T))
    rows = []
    for person, g in a.groupby('participant'):
        lab = g[g.y.notna()]
        raw = d[d.participant.eq(person)]
        drift = abs(roc_auc_score(lab.y.astype(int), lab.ts) - .5) if lab.y.nunique() == 2 else np.nan
        rows.append(dict(participant=person, ventanas_etiquetadas=len(lab), eeg_utilizable=raw.eeg_quality_usable.astype(float).mean(),
                         cobertura_eeg=raw.eeg_coverage.mean(), cobertura_pupila=raw.pupil_coverage.mean(),
                         cobertura_mirada=raw.gaze_coverage.mean(), deriva_sesion=drift,
                         largo_medio_segmento=g.groupby('seg').size().mean(), duracion_sesion=g.ts.max()))
    return pd.DataFrame(rows).set_index('participant')


def report_e4(d):
    conf, desc = [], []
    for task in F.LEAVES:
        T = V3.Task(d, task)
        base = rep(task)
        w = mean_auc(base)
        gain = (w.hgb_c32 - w.hgb_c1).rename('ganancia')
        # (a) fiabilidad por mitades
        h = halves(T)
        b = base.assign(half=base.source_row.map(h))
        assert b.half.notna().all()
        w0, w1 = mean_auc(b[b.half.eq(0)]), mean_auc(b[b.half.eq(1)])
        for name, f in [('AUC sin historial', lambda x: x.hgb_c1), ('AUC con historial', lambda x: x.hgb_c32),
                        ('ganancia del historial', lambda x: x.hgb_c32 - x.hgb_c1)]:
            j = pd.concat([f(w0).rename('a'), f(w1).rename('b')], axis=1).dropna()
            s = spearman_ci(j.a, j.b)
            desc.append(dict(task=task, part='E4a', item=f'fiabilidad por mitades: {name}', **s,
                             spearman_brown=2 * s['delta'] / (1 + s['delta'])))
        # (b) correlatos
        cov = covariates(d, T)
        for outcome, v in [('AUC sin historial', w.hgb_c1), ('ganancia del historial', gain)]:
            rows = []
            for c in COVARIATES:
                j = pd.concat([v.rename('v'), cov[c]], axis=1).dropna()
                rows.append(dict(task=task, part='E4b', item=f'{outcome} ~ {c}', **spearman_ci(j.v, j[c])))
            for r, hp in zip(rows, R.holm([r['p'] for r in rows])):
                r['p_holm'] = float(hp)
            desc += rows
        # (c) adaptación
        new = load('e4', task)
        glob = base.merge(new[['seed', 'source_row']].drop_duplicates(), on=['seed', 'source_row'])
        assert len(glob) == len(new)
        wp = mean_auc(pd.concat([new, glob]))
        for a, bb in [('pers_c1', 'hgb_c1'), ('pers_c32', 'hgb_c32')]:
            conf.append(dict(task=task, test='D', contrast=f'{a} − {bb}', **R.contrast(wp, a, bb)))
        desc += absolute(wp, ['hgb_c1', 'pers_c1', 'hgb_c32', 'pers_c32'], task=task, part='E4c')
        desc.append(dict(task=task, part='E4c', item='pers_c32 − pers_c1', **R.contrast(wp, 'pers_c32', 'pers_c1')))
        desc.append(dict(task=task, part='E4c', item='hgb_c32 − hgb_c1 (mismas filas)', **R.contrast(wp, 'hgb_c32', 'hgb_c1')))
        n = new[new.seed.eq(SEEDS[0]) & new.strategy.eq('pers_c1')].groupby('participant').size()
        desc.append(dict(task=task, part='E4c', item='ventanas de evaluación por persona (mediana)', delta=float(n.median()),
                         low95=float(n.min()), high95=float(n.max()), people=len(n)))
    return family(conf), pd.DataFrame(desc)


def report(only=None):
    d = V3.load_data()
    pd.set_option('display.width', 250)
    pd.set_option('display.max_rows', 300)
    for name, fn in [('e1', report_e1), ('e2', report_e2), ('e3', report_e3), ('e4', report_e4)]:
        if only and name != only:
            continue
        conf, desc = fn(d)
        conf.to_csv(OUT / f'{name}_confirmatorio.csv', index=False)
        desc.to_csv(OUT / f'{name}_descriptivos.csv', index=False)
        print(f'\n===== {name.upper()} confirmatorio')
        print(conf.round(4).to_string(index=False))
        print(f'----- {name.upper()} descriptivos')
        print(desc.round(4).to_string(index=False))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['prepare', 'e1', 'e2', 'e3', 'e4', 'report'])
    ap.add_argument('--task', choices=list(F.LEAVES))
    ap.add_argument('--seed', type=int)
    ap.add_argument('--only')
    a = ap.parse_args()
    with threadpool_limits(limits=1):
        if a.phase == 'prepare':
            prepare()
        elif a.phase == 'report':
            report(a.only)
        elif a.phase == 'e4':
            run_e4(a.task, a.seed)
        else:
            globals()[f'run_{a.phase}'](a.seed)
