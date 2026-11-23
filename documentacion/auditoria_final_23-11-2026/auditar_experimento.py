#!/usr/bin/env python
"""Auditoría independiente de las 12 etapas experimentales del 16 al 23-11-2026.

Código propio: no importa ningún script del repositorio ni usa sus funciones de reporte.
Solo lee `resultados/` (predicciones, CSV, protocolos) y la tabla de ventanas del preprocesamiento
(para reconstruir estímulo, minuto de sesión y posición). No entrena, no escribe fuera de esta carpeta.

Salidas (en esta misma carpeta):
  comparaciones.csv   una fila por cifra comparada (informada frente a recalculada)
  integridad.csv      una fila por comprobación de integridad
  recalculo.json      cifras recalculadas que se usan en el informe

Uso:  .venv/bin/python documentacion/auditoria_final_23-11-2026/auditar_experimento.py
"""
import gzip
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RES = ROOT / 'resultados'
MARGIN = .02
NBOOT, NPERM = 20000, 200000
OWN_BOOT, OWN_PERM = 97531, 86420            # semillas propias del auditor
REG_BOOT, REG_PERM = 20261029, 20261116      # semillas declaradas en los protocolos ('inference')
TOL_EXACT, TOL_BOOT, TOL_P = 1e-9, 2e-3, 3e-3

COMP, INTEG, OUTJ = [], [], {}
LABELS = {}   # (tarea) -> Serie source_row -> y, para comprobar etiquetas idénticas entre etapas
PEOPLE = {}   # source_row -> persona


# ------------------------------------------------------------------ estadística propia
def auc(y, p):
    """AUC por rangos (Mann-Whitney) con empates promediados. NaN si hay una sola clase."""
    y = np.asarray(y)
    n1 = int((y == 1).sum())
    n0 = len(y) - n1
    if n1 == 0 or n0 == 0:
        return np.nan
    r = rankdata(np.asarray(p, dtype=float))
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


def person_auc(df, keys=('strategy',)):
    keys = list(keys)
    out = df.groupby(keys + ['participant'], sort=False).apply(lambda g: auc(g.y.to_numpy(), g.prob.to_numpy()))
    return out.rename('auc').reset_index().dropna(subset=['auc'])


def wide_mean(df, extra=()):
    """AUC por persona y estrategia; si hay semillas, se promedia sobre ellas."""
    keys = list(extra) + ['strategy']
    if 'seed' in df.columns:
        pa = person_auc(df, ['seed'] + keys)
    else:
        pa = person_auc(df, keys)
    return pa.groupby(['participant'] + keys).auc.mean().unstack(keys)


_BOOT, _SIGN = {}, {}


def _boot_idx(seed, n):
    if (seed, n) not in _BOOT:
        _BOOT[(seed, n)] = np.random.default_rng(seed).integers(0, n, (NBOOT, n))
    return _BOOT[(seed, n)]


def _signs(seed, n, registered):
    k = (seed, n, registered)
    if k not in _SIGN:
        rng = np.random.default_rng(seed)
        if registered:   # mismo generador que declara el protocolo, para comprobar determinismo
            s = rng.choice([-1, 1], size=(NPERM, n)).astype(np.int8)
        else:
            s = (rng.integers(0, 2, (NPERM, n), dtype=np.int8) * 2 - 1).astype(np.int8)
        _SIGN[k] = s
    return _SIGN[k]


def boot_ci(d, seed):
    d = np.asarray(d, dtype=float)
    m = d[_boot_idx(seed, len(d))].mean(axis=1)
    return [float(x) for x in np.quantile(m, [.025, .975, .05, .95])]


def sign_perm(d, seed, registered):
    d = np.asarray(d, dtype=float)
    null = np.abs(_signs(seed, len(d), registered) @ d) / len(d)
    return float((1 + (null >= abs(d.mean()) - 1e-15).sum()) / (NPERM + 1))


def holm(ps):
    ps = np.asarray(ps, dtype=float)
    order = np.argsort(ps, kind='stable')
    out, run = np.empty(len(ps)), 0.
    for i, ix in enumerate(order):
        run = max(run, min(1., ps[ix] * (len(ps) - i)))
        out[ix] = run
    return out


def decide(lo95, hi95, lo90, hi90, p_holm):
    """Reglas registradas (protocolo 'decision'), con la precedencia que declara el análisis final."""
    if p_holm is not None and not math.isnan(p_holm) and p_holm < .05 and lo95 > 0:
        return 'efecto relevante' if lo95 > MARGIN else 'respaldo'
    if hi95 < 0:
        return 'inferior'
    if -MARGIN < lo90 and hi90 < MARGIN:
        return 'nulo concluyente'
    return 'inconcluso'


def stats(d):
    d = np.asarray(d, dtype=float)
    d = d[~np.isnan(d)]
    lo95, hi95, lo90, hi90 = boot_ci(d, OWN_BOOT)
    r = boot_ci(d, REG_BOOT)
    return dict(delta=float(d.mean()), low95=lo95, high95=hi95, low90=lo90, high90=hi90,
                p=sign_perm(d, OWN_PERM, False), improved=int((d > 0).sum()), people=len(d), median=float(np.median(d)),
                reg=dict(low95=r[0], high95=r[1], low90=r[2], high90=r[3], p=sign_perm(d, REG_PERM, True)))


# ------------------------------------------------------------------ registro de comparaciones
def add(stage, file, item, field, reported, own, reg=None, kind='exact'):
    try:
        rep = float(reported)
    except (TypeError, ValueError):
        rep = np.nan
    if kind == 'text':
        ok = str(reported) == str(own)
        COMP.append(dict(stage=stage, file=file, item=item, field=field, reported=reported, recalculated=own,
                         recalculated_regseed='', diff='', kind=kind, verdict='coincide' if ok else 'DISCREPA'))
        return ok
    if isinstance(reported, float) and math.isnan(rep) and (own is None or (isinstance(own, float) and math.isnan(own))):
        return True
    diff = abs(rep - own)
    tol = dict(exact=TOL_EXACT, boot=TOL_BOOT, perm=TOL_P, int=0, loose=5e-4)[kind]
    if kind == 'perm':
        tol = max(TOL_P, .15 * rep)
    ok = diff <= tol
    verdict = 'coincide' if ok else 'DISCREPA'
    if ok and kind in ('boot', 'perm') and diff > TOL_EXACT:
        verdict = 'coincide (difiere solo por semilla de remuestreo)'
    if reg is not None and abs(rep - reg) > 1e-7:
        verdict += '; no reproduce con la semilla registrada' if ok else ''
    COMP.append(dict(stage=stage, file=file, item=item, field=field, reported=rep, recalculated=own,
                     recalculated_regseed='' if reg is None else reg, diff=diff, kind=kind, verdict=verdict))
    return ok


def check(stage, name, ok, detail=''):
    INTEG.append(dict(stage=stage, check=name, ok=bool(ok), detail=str(detail)))
    return ok


def cmp_contrast(stage, file, item, row, d, low='low95', high='high95', has90=True, has_p=True, count='improved'):
    s = stats(d)
    add(stage, file, item, 'delta', row['delta'], s['delta'])
    add(stage, file, item, 'low95', row[low], s['low95'], s['reg']['low95'], 'boot')
    add(stage, file, item, 'high95', row[high], s['high95'], s['reg']['high95'], 'boot')
    if has90 and 'low90' in row and not pd.isna(row['low90']):
        add(stage, file, item, 'low90', row['low90'], s['low90'], s['reg']['low90'], 'boot')
        add(stage, file, item, 'high90', row['high90'], s['high90'], s['reg']['high90'], 'boot')
    if has_p and 'p' in row and not pd.isna(row['p']):
        add(stage, file, item, 'p', row['p'], s['p'], s['reg']['p'], 'perm')
    if count in row and not pd.isna(row[count]):
        add(stage, file, item, 'improved', row[count], s['improved'], kind='int')
    if 'people' in row and not pd.isna(row['people']):
        add(stage, file, item, 'people', row['people'], s['people'], kind='int')
    return s


def cmp_family(stage, file, items, rows, ss, decision=True):
    """Holm sobre la familia y decisión por la regla registrada, con p propios y con los informados."""
    hp = holm([s['p'] for s in ss])
    hr = holm([s['reg']['p'] for s in ss])
    for item, row, s, h, h2 in zip(items, rows, ss, hp, hr):
        s['p_holm'] = float(h)
        add(stage, file, item, 'p_holm', row['p_holm'], float(h), float(h2), 'perm')
        if decision:
            s['decision'] = decide(s['low95'], s['high95'], s['low90'], s['high90'], float(h))
            add(stage, file, item, 'decision', row['decision'], s['decision'], kind='text')


def read(path):
    return pd.read_csv(path)


def proto(stage):
    return json.loads((RES / stage / 'protocolo.json').read_text())


# ------------------------------------------------------------------ integridad
def integrity(stage, name, df, task, folds=None, by_seed=False, people=41, label_check=True, key='source_row',
              fold_base=0, rows_expected=None):
    """Duplicados, NaN, rango, mismas filas y etiquetas entre estrategias, personas, y folds del protocolo."""
    g = ['strategy'] + (['seed'] if by_seed and 'seed' in df.columns else [])
    tag = f'{name}'
    check(stage, f'{tag}: sin filas duplicadas (fila, estrategia{", semilla" if len(g) > 1 else ""})',
          not df.duplicated(g + [key]).any(), int(df.duplicated(g + [key]).sum()))
    check(stage, f'{tag}: sin NaN y probabilidades en [0, 1]',
          df[['y', 'prob']].notna().all().all() and df.prob.between(0, 1).all(),
          f'NaN={int(df[["y", "prob"]].isna().sum().sum())}, min={df.prob.min():.4g}, max={df.prob.max():.4g}')
    sets = df.groupby(g)[key].apply(frozenset)
    same = sets.nunique() == 1
    check(stage, f'{tag}: mismas ventanas en todas las estrategias{" y semillas" if len(g) > 1 else ""}', same,
          f'{len(sets)} grupos, tamaños {sorted(set(len(s) for s in sets))}')
    yy = df.groupby(key).y.nunique()
    check(stage, f'{tag}: etiqueta idéntica entre estrategias para cada ventana', (yy == 1).all(), int((yy > 1).sum()))
    pp = df.groupby(key).participant.nunique()
    check(stage, f'{tag}: cada ventana pertenece a una sola persona', (pp == 1).all(), int((pp > 1).sum()))
    n = df.participant.nunique()
    check(stage, f'{tag}: {people} personas', n == people, n)
    if rows_expected is not None:
        check(stage, f'{tag}: {rows_expected} ventanas por estrategia', set(len(s) for s in sets) == {rows_expected},
              sorted(set(len(s) for s in sets)))
    one_class = df.groupby(g + ['participant']).y.nunique().eq(1).sum()
    check(stage, f'{tag}: ninguna persona con una sola clase', one_class == 0, int(one_class))
    const = df.groupby(g).prob.nunique().eq(1).sum()
    check(stage, f'{tag}: sin predicciones constantes', const == 0, int(const))
    if folds is not None and 'fold' in df.columns:
        seeds = sorted(df.seed.unique()) if 'seed' in df.columns and isinstance(folds, dict) else [None]
        bad, detail = 0, []
        for s in seeds:
            fl = folds[str(s)] if s is not None else folds
            allp = sum(fl, [])
            if len(allp) != len(set(allp)):
                bad += 1
                detail.append(f'{s}: persona repetida en folds del protocolo')
            mp = {p: k + fold_base for k, f in enumerate(fl) for p in f}
            sub = df if s is None else df[df.seed.eq(s)]
            pf = sub.groupby('participant').fold.agg(['nunique', 'first'])
            if (pf['nunique'] != 1).any():
                bad += 1
                detail.append(f'{s}: persona evaluada en más de un fold')
            miss = [p for p in pf.index if mp.get(p) != pf.loc[p, 'first']]
            if miss:
                bad += 1
                detail.append(f'{s}: fold distinto al protocolo en {miss[:5]}')
            if set(pf.index) - set(allp):
                bad += 1
                detail.append(f'{s}: personas fuera del protocolo')
        check(stage, f'{tag}: cada persona se evalúa en un solo fold, igual al del protocolo (nunca en su propio ajuste)',
              bad == 0, '; '.join(detail))
    if label_check and key == 'source_row':
        cur = df.drop_duplicates('source_row').set_index('source_row').y
        if task in LABELS:
            ref = LABELS[task]
            common = cur.index.intersection(ref.index)
            check(stage, f'{tag}: etiquetas iguales a las de la etapa de referencia ({task})',
                  (cur.loc[common] == ref.loc[common]).all() and len(common) == len(cur),
                  f'{len(common)} de {len(cur)} ventanas en común; distintas={(cur.loc[common] != ref.loc[common]).sum()}')
        else:
            LABELS[task] = cur
        per = df.drop_duplicates('source_row').set_index('source_row').participant
        bad = sum(1 for r, p in per.items() if PEOPLE.setdefault(r, p) != p)
        check(stage, f'{tag}: persona de cada ventana coherente con las demás etapas', bad == 0, bad)


# ------------------------------------------------------------------ tabla de ventanas (estratos)
def windows_table():
    """Estímulo, minuto de sesión y posición en el estímulo de cada ventana, reconstruidos desde el preprocesamiento."""
    src = pd.read_csv(RES / 'preprocesamiento/caracteristicas_multimodales.csv',
                      usecols=['participant', 'recording', 'segment_id', 'stimulus', 'window_start_utc'])
    src['source_row'] = np.arange(len(src))
    parts = pd.read_csv(RES / 'modelado/particion_participantes.csv').set_index('participant').split
    src['split'] = src.participant.map(parts)
    w = src[src.split.isin(['train', 'validation', 'test'])].copy()
    w['t'] = pd.to_datetime(w.window_start_utc, utc=True).dt.as_unit('ns').astype('int64') / 1e9
    w = w.sort_values(['participant', 'recording', 'segment_id', 'stimulus', 'window_start_utc']).reset_index(drop=True)
    w['seg'] = w.groupby(['participant', 'recording', 'segment_id', 'stimulus'], sort=False).ngroup()
    gap = w.groupby('seg').t.diff()
    new_run = gap.isna() | ~np.isclose(gap.fillna(1.), 1., atol=1e-4, rtol=0)
    run = new_run.cumsum()
    w['posicion'] = np.minimum(w.groupby(run).cumcount() + 1, 32)
    w['st'] = (w.t - w.groupby('participant').t.transform('min')).astype('float32')
    w['bloque60'] = (w.st // 60).astype(int)
    w['estimulo'] = w.seg
    return w.set_index('source_row'), parts


def strat_auc(g, col):
    num = den = 0.
    for _, s in g.groupby(col, sort=False):
        n1 = int(s.y.sum())
        pairs = n1 * (len(s) - n1)
        if pairs:
            num += auc(s.y.to_numpy(), s.prob.to_numpy()) * pairs
            den += pairs
    return num / den if den else np.nan


def wide_strat(df, col):
    v = df.groupby(['seed', 'strategy', 'participant'], sort=False).apply(lambda g: strat_auc(g, col)).rename('auc').reset_index()
    return v.groupby(['participant', 'strategy']).auc.mean().unstack()


def keep(name, value):
    OUTJ[name] = value
    return value


def s3(s):
    return {k: round(v, 5) if isinstance(v, float) else v for k, v in s.items() if k != 'reg'}


# ================================================================== ETAPAS
def stage_v3():
    st = 'cierre_v3_16-11-2026'
    p = proto(st)
    W, parts = WT
    con = read(RES / st / 'contrastes.csv')
    met = read(RES / st / 'metricas.csv')
    train = set(parts[parts.eq('train')].index)
    ext_people = {s: set(parts[parts.eq(s)].index) for s in ['validation', 'test']}
    check(st, 'partición: 25 train, 8 validación, 8 test, disjuntas',
          len(train) == 25 and len(ext_people['validation']) == 8 and len(ext_people['test']) == 8, '')
    ok = True
    for f in p['folds']:
        fit, ev, inf, inv = map(set, (f['fit'], f['evaluation'], f['inner_fit'], f['inner_validation']))
        ok &= not (fit & ev) and (fit | ev) == train and not (inf & inv) and (inf | inv) == fit
    check(st, 'protocolo: en los 5 folds ajuste y evaluación son disjuntos, cubren las 25 de train, y la validación interna sale del ajuste', ok)
    ev_all = sum((f['evaluation'] for f in p['folds']), [])
    check(st, 'protocolo: cada persona de train se evalúa en un solo fold', len(ev_all) == len(set(ev_all)) == 25)
    for task in ['atencion', 'activacion']:
        oof = read(RES / st / f'oof_{task}.csv.gz')
        ext = read(RES / st / f'externas_{task}.csv.gz')
        integrity(st, f'oof_{task}', oof, task + '_v3', folds=[f['evaluation'] for f in p['folds']], people=25, fold_base=1,
                  label_check=False)
        check(st, f'oof_{task}: solo personas de train', set(oof.participant) <= train, '')
        for s in ['validation', 'test']:
            e = ext[ext.split.eq(s)]
            integrity(st, f'externas_{task} ({s})', e, task + '_v3', people=8, label_check=False)
            check(st, f'externas_{task} ({s}): solo personas de {s}, ninguna de train',
                  set(e.participant) == ext_people[s] and not (set(e.participant) & train), '')
        both = pd.concat([oof.assign(split='oof_train'), ext])
        # etiquetas de estas filas frente a las del análisis final (se comprueban más adelante al cargar esa etapa)
        LABELS.setdefault(task + '_v3ref', both.drop_duplicates('source_row').set_index('source_row').y)
        for split, g in both.groupby('split'):
            w = wide_mean(g.drop(columns=[c for c in ['seed'] if c in g.columns]))
            for _, r in met[(met.task.eq(task)) & (met.split.eq(split))].iterrows():
                v = w[r.strategy].dropna()
                add(st, 'metricas.csv', f'{task} {split} AUC {r.strategy}', 'auc', r.auc, float(v.mean()))
                b = boot_ci(v, OWN_BOOT)
                add(st, 'metricas.csv', f'{task} {split} AUC {r.strategy}', 'low95', r.auc_low, b[0], boot_ci(v, REG_BOOT)[0], 'boot')
                add(st, 'metricas.csv', f'{task} {split} AUC {r.strategy}', 'high95', r.auc_high, b[1], boot_ci(v, REG_BOOT)[1], 'boot')
            for name, a, b_, role in p['contrasts']:
                row = con[(con.task.eq(task)) & (con.split.eq(split)) & (con.contrast.eq(name))].iloc[0]
                s = cmp_contrast(st, 'contrastes.csv', f'{task} {split} {name}', dict(row), (w[a] - w[b_]).to_numpy(),
                                 low='low', high='high', has90=False, has_p=False)
                keep(f'v3|{task}|{split}|{name}', s3(s))
    # regla registrada: ventaja consistente = IC95 > 0 en validación y en test
    for task in ['atencion', 'activacion']:
        for name in ['gru_orden', 'hgb_resumen']:
            v, t = OUTJ[f'v3|{task}|validation|{name}'], OUTJ[f'v3|{task}|test|{name}']
            keep(f'v3|{task}|{name}|ventaja_consistente', bool(v['low95'] > 0 and t['low95'] > 0))


def stage_final():
    st = 'cierre_final_41p_16-11-2026'
    p = proto(st)
    con = read(RES / st / 'contrastes.csv')
    met = read(RES / st / 'metricas.csv')
    het = read(RES / st / 'heterogeneidad_por_grupo.csv')
    mp = read(RES / st / 'metricas_personas.csv')
    W, parts = WT
    fam_items, fam_rows, fam_s = [], [], []
    for task in ['atencion', 'activacion']:
        pred = read(RES / st / f'predicciones_{task}.csv.gz')
        integrity(st, f'predicciones_{task}', pred, task, folds=p['folds'])
        check(st, f'predicciones_{task}: columna split coincide con la partición original',
              (pred.participant.map(parts) == pred.split).all(), '')
        ref = LABELS.get(task + '_v3ref')
        cur = LABELS[task]
        common = cur.index.intersection(ref.index)
        check(st, f'predicciones_{task}: etiquetas iguales a las del cierre V3',
              (cur.loc[common] == ref.loc[common]).all(), f'{len(common)} ventanas en común de {len(cur)} (final) y {len(ref)} (V3)')
        w = wide_mean(pred)
        FINAL[task] = (pred, w)
        m = mp[mp.task.eq(task)].pivot(index='participant', columns='strategy', values='auc')
        add(st, 'metricas_personas.csv', f'{task}: AUC por persona (máxima diferencia, {m.size} valores)', 'auc', 0.,
            float((m - w[m.columns]).abs().max().max()))
        for _, r in met[met.task.eq(task)].iterrows():
            v = w[r.strategy]
            b, b2 = boot_ci(v, OWN_BOOT), boot_ci(v, REG_BOOT)
            add(st, 'metricas.csv', f'{task} AUC {r.strategy}', 'auc', r.auc, float(v.mean()))
            add(st, 'metricas.csv', f'{task} AUC {r.strategy}', 'low95', r.low, b[0], b2[0], 'boot')
            add(st, 'metricas.csv', f'{task} AUC {r.strategy}', 'high95', r.high, b[1], b2[1], 'boot')
            keep(f'final|{task}|AUC {r.strategy}', [round(float(v.mean()), 5), round(b[0], 5), round(b[1], 5)])
        for _, r in con[con.task.eq(task)].iterrows():
            a, b_ = r.contrast.split(' − ')
            s = cmp_contrast(st, 'contrastes.csv', f'{task} {r.contrast}', dict(r), (w[a] - w[b_]).to_numpy())
            if r.role == 'principal':
                fam_items.append(f'{task} {r.contrast}'); fam_rows.append(dict(r)); fam_s.append(s)
            else:   # secundarios: p sin ajustar, decisión descriptiva con la misma regla
                s['decision'] = decide(s['low95'], s['high95'], s['low90'], s['high90'], s['p'] if s['p'] < .05 else 1.)
                add(st, 'contrastes.csv', f'{task} {r.contrast}', 'decision (secundario, p sin ajustar)', r.decision, s['decision'], kind='text')
            keep(f'final|{task}|{r.contrast}', s3(s))
        grp = {'train (25)': parts[parts.eq('train')].index, 'validación+test (16)': parts[parts.isin(['validation', 'test'])].index}
        for _, r in het[het.task.eq(task)].iterrows():
            a, b_ = r.contraste.split(' − ')
            d = (w[a] - w[b_]).reindex(grp[r.grupo]).dropna().to_numpy()
            s = stats(d)
            for f_, k in [('delta', 'delta'), ('low95', 'low95'), ('high95', 'high95')]:
                add(st, 'heterogeneidad_por_grupo.csv', f'{task} {r.grupo} {r.contraste}', f_, r[f_], s[k],
                    None if f_ == 'delta' else s['reg'][k], 'loose' if f_ == 'delta' else 'boot')
            add(st, 'heterogeneidad_por_grupo.csv', f'{task} {r.grupo} {r.contraste}', 'mejoran', r.mejoran,
                f"{s['improved']}/{s['people']}", kind='text')
    cmp_family(st, 'contrastes.csv', fam_items, fam_rows, fam_s)
    for i, s in zip(fam_items, fam_s):
        keep(f'final|{i}|holm', s3(s))


def stage_robustez():
    st = 'cierre_robustez_41p_16-11-2026'
    p = proto(st)
    res = read(RES / st / 'resultados.csv')
    fam = []
    for task in ['atencion', 'activacion']:
        _, w0 = FINAL[task]
        r1 = read(RES / st / f'r1_{task}.csv.gz')
        integrity(st, f'r1_{task}', r1, task, folds=p['folds_main'])
        w = w0.join(wide_mean(r1))
        r3 = read(RES / st / f'r3_{task}.csv.gz')
        integrity(st, f'r3_{task}', r3, task, folds=p['folds_r3'], by_seed=True)
        w3 = wide_mean(r3.rename(columns={'seed': 'particion'}), extra=('particion',))
        for _, r in res[res.task.eq(task)].iterrows():
            if r.prueba == 'R1 placebo':
                d = w.hgb_c32 - w.placebo_c32
            elif r.prueba == 'R1 referencia':
                d = w.placebo_c32 - w.hgb_c1
            elif r.prueba.startswith('R3'):
                s_ = int(r.prueba.split()[-1])
                d = w3[(s_, 'hgb_c32')] - w3[(s_, 'hgb_c1')]
            elif r.prueba == 'R2 sin fuga':
                r2 = read(RES / st / f'r2_{task}.csv.gz')
                integrity(st, f'r2_{task}', r2, task + '_r2', folds=p['folds_main'], label_check=False)
                cur = r2.drop_duplicates('source_row').set_index('source_row').y
                ref = LABELS[task]
                common = cur.index.intersection(ref.index)
                check(st, 'r2_atencion: mismas ventanas que el análisis final (las etiquetas cambian por diseño: profesor reajustado sin fuga)',
                      len(common) == len(cur) == len(ref), f'etiquetas distintas a las originales: {(cur.loc[common] != ref.loc[common]).mean():.3%}')
                w2 = wide_mean(r2)
                d = w2.hgb_c32 - w2.hgb_c1
            s = cmp_contrast(st, 'resultados.csv', f'{task} {r.prueba}', dict(r), d.to_numpy(), has90=False)
            keep(f'robustez|{task}|{r.prueba}', s3(s))
            if r.prueba == 'R1 placebo':
                fam.append((f'{task} {r.prueba}', dict(r), s))
        cor = FINAL[task][0][FINAL[task][0].strategy.eq('hgb_c32')].set_index('source_row').prob.corr(
            r1[r1.strategy.eq('placebo_c32')].set_index('source_row').prob)
        keep(f'robustez|{task}|corr real-placebo', round(float(cor), 3))
    cmp_family(st, 'resultados.csv', [f[0] for f in fam], [f[1] for f in fam], [f[2] for f in fam], decision=False)
    for name, _, s in fam:
        keep(f'robustez|{name}|holm', s3(s))


def stage_ampliacion():
    st = 'ampliacion_41p_16-11-2026'
    p = proto(st)
    W, _ = WT
    con = read(RES / st / 'contrastes.csv')
    met = read(RES / st / 'metricas.csv')
    e4 = read(RES / st / 'fatiga_por_quintil.csv')
    fam = []
    for task in ['atencion', 'activacion']:
        pred = read(RES / st / f'predicciones_{task}.csv.gz')
        integrity(st, f'predicciones_{task}', pred, task, folds=p['folds'])
        main, w0 = FINAL[task]
        w = w0.join(wide_mean(pred))
        AMPL[task] = w
        for _, r in met[met.task.eq(task)].iterrows():
            add(st, 'metricas.csv', f'{task} AUC {r.strategy}', 'auc', r.auc, float(w[r.strategy].mean()))
        for _, r in con[con.task.eq(task)].iterrows():
            a, b_ = r.contrast.split(' − ')
            s = cmp_contrast(st, 'contrastes.csv', f'{task} {r.experiment} {r.contrast}', dict(r), (w[a] - w[b_]).to_numpy(), has90=False)
            keep(f'ampliacion|{task}|{r.experiment}|{r.contrast}', s3(s))
            if r.experiment == 'E1 principal':
                fam.append((f'{task} {r.experiment} {r.contrast}', dict(r), s))
        # E4 descriptivo: quintiles del tiempo de sesión por persona, con las predicciones del análisis final
        for strat in ['hgb_c1', 'hgb_c32']:
            g = main[main.strategy.eq(strat)].copy()
            g['t'] = g.source_row.map(W.t)
            g['q'] = g.groupby('participant').t.transform(lambda s_: pd.qcut(s_.rank(method='first'), 5, labels=False)).astype(int)
            for q, h in g.groupby('q'):
                a_ = person_auc(h).auc
                r = e4[(e4.task.eq(task)) & (e4.strategy.eq(strat)) & (e4.quintil.eq(q + 1))].iloc[0]
                add(st, 'fatiga_por_quintil.csv', f'{task} {strat} quintil {q + 1}', 'prevalencia_alta', r.prevalencia_alta, float(h.y.mean()), kind='loose')
                add(st, 'fatiga_por_quintil.csv', f'{task} {strat} quintil {q + 1}', 'auc', r.auc, float(a_.mean()), kind='loose')
        # E5: solo coherencia interna (importancias por fold frente al resumen); no se puede recalcular sin los modelos
        im = read(RES / st / f'importancia_{task}.csv')
        agg = im.groupby(['block', 'fold'])['drop'].mean().groupby('block').agg(['mean', 'std'])
        rs = read(RES / st / 'importancia_resumen.csv')
        for _, r in rs[rs.task.eq(task)].iterrows():
            add(st, 'importancia_resumen.csv', f'{task} {r.block}', 'mean', r['mean'], float(agg.loc[r.block, 'mean']))
            keep(f'ampliacion|{task}|importancia|{r.block}', [round(float(agg.loc[r.block, 'mean']), 4), round(float(agg.loc[r.block, 'std']), 4)])
    cmp_family(st, 'contrastes.csv', [f[0] for f in fam], [f[1] for f in fam], [f[2] for f in fam], decision=False)
    # enmienda E1 con 6 ventanas
    st2 = st + '/enmienda_e1_lag6'
    con = read(RES / st2 / 'contrastes.csv')
    fam = []
    for task in ['atencion', 'activacion']:
        pred = read(RES / st2 / f'predicciones_{task}.csv.gz')
        integrity(st2, f'predicciones_{task}', pred, task, folds=p['folds'])
        w = FINAL[task][1].join(wide_mean(pred))
        for _, r in con[con.task.eq(task)].iterrows():
            a, b_ = r.contrast.split(' − ')
            s = cmp_contrast(st2, 'contrastes.csv', f'{task} {r.contrast}', dict(r), (w[a] - w[b_]).to_numpy(), has90=False)
            if 'placebo' in r.contrast:
                fam.append((f'{task} {r.contrast}', dict(r), s))
            keep(f'enmienda|{task}|{r.contrast}', s3(s))
    cmp_family(st2, 'contrastes.csv', [f[0] for f in fam], [f[1] for f in fam], [f[2] for f in fam], decision=False)
    for name, _, s in fam:
        s['decision'] = decide(s['low95'], s['high95'], s['low90'], s['high90'], s['p_holm'])
        keep(f'enmienda|{name}|holm', s3(s))


def stage_explicativo():
    st = 'explicativo_posicion_41p_18-11-2026'
    p = proto(st)
    con = read(RES / st / 'contrastes.csv')
    for task in ['atencion', 'activacion']:
        pred = read(RES / st / f'predicciones_{task}.csv.gz')
        integrity(st, f'predicciones_{task}', pred, task, folds=p['folds'])
        w = FINAL[task][1].join(wide_mean(pred))
        EXPL[task] = pred
        for _, r in con[con.task.eq(task)].iterrows():
            if r.contrast.startswith('AUC '):
                add(st, 'contrastes.csv', f'{task} {r.contrast}', 'auc', r.delta, float(w[r.contrast[4:]].mean()))
                continue
            a, b_ = r.contrast.split(' − ')
            s = cmp_contrast(st, 'contrastes.csv', f'{task} {r.contrast}', dict(r), (w[a] - w[b_]).to_numpy(), has90=False)
            keep(f'explicativo|{task}|{r.contrast}', s3(s))


def stage_reapertura():
    st = 'reapertura_41p_22-11-2026'
    p = proto(st)
    W, _ = WT
    conf = read(RES / st / 'confirmatorio.csv')
    cur = read(RES / st / 'curva_temporal.csv')
    desc = read(RES / st / 'descriptivos.csv')
    absol = read(RES / st / 'auc_absolutas.csv')
    fam = []
    for task in ['atencion', 'activacion']:
        rep = pd.concat([read(RES / st / f'rep_{task}_{s}.csv.gz') for s in p['folds_rep']])
        integrity(st, f'rep_{task} (5 particiones)', rep[rep.strategy.ne('pos_only')], task, folds=p['folds_rep'], by_seed=True,
                  rows_expected=len(LABELS[task]))
        REP[task] = rep
        pa = person_auc(rep, ['seed', 'strategy'])
        w = pa.groupby(['participant', 'strategy']).auc.mean().unstack()
        REPW[task] = w
        for _, r in conf[conf.task.eq(task)].iterrows():
            a, b_ = r.contrast.split(' − ')
            s = cmp_contrast(st, 'confirmatorio.csv', f'{task} {r.test}', dict(r), (w[a] - w[b_]).to_numpy())
            fam.append((f'{task} {r.test}', dict(r), s))
        for s_ in p['folds_rep']:
            ws = pa[pa.seed.eq(int(s_))].pivot(index='participant', columns='strategy', values='auc')
            for name, a, b_ in [('P1', 'hgb_c32', 'hgb_c1'), ('P2', 'c32_ts', 'c1_ts')]:
                r = desc[(desc.task.eq(task)) & (desc.item.eq(f'{name} partición {s_}'))].iloc[0]
                add(st, 'descriptivos.csv', f'{task} {name} partición {s_}', 'delta', r.delta, float((ws[a] - ws[b_]).mean()))
                keep(f'reapertura|{task}|{name}|{s_}', stats((ws[a] - ws[b_]).to_numpy())['low95'] if name == 'P1' else None)
        r = desc[(desc.task.eq(task)) & desc.item.str.startswith('c1_ts − hgb_c1')].iloc[0]
        cmp_contrast(st, 'descriptivos.csv', f'{task} c1_ts − hgb_c1', dict(r), (w.c1_ts - w.hgb_c1).to_numpy())
        for _, r in absol[absol.task.eq(task) & ~absol.strategy.str.startswith('curva')].iterrows():
            add(st, 'auc_absolutas.csv', f'{task} AUC {r.strategy}', 'auc', r.auc, float(w[r.strategy].mean()))
        # sensibilidad sin la persona más influyente (no registrada; pedida por la auditoría previa)
        d = (w.hgb_c32 - w.hgb_c1)
        top = (d - d.mean()).abs().idxmax()
        keep(f'reapertura|{task}|P1 influencia', dict(persona=top, delta_persona=round(float(d[top]), 4), mediana=round(float(d.median()), 4),
                                                     sin=s3(stats(d.drop(top).to_numpy()))))
        # ---- curva temporal (una partición)
        lag = read(RES / st / f'lag_{task}.csv.gz')
        cob = json.loads((RES / st / f'cobertura_{task}.json').read_text())
        integrity(st, f'lag_{task}', lag, task, folds=p['folds_main'], people=cob['people'], rows_expected=cob['common'])
        LAG[task] = lag
        wl = wide_mean(lag)
        rows, ss = [], []
        for _, r in cur[cur.task.eq(task)].iterrows():
            s = cmp_contrast(st, 'curva_temporal.csv', f'{task} lag{r.lag} − placebo', dict(r), (wl[f'lag{r.lag}'] - wl.placebo).to_numpy())
            rows.append(dict(r)); ss.append(s)
        cmp_family(st, 'curva_temporal.csv', [f'{task} lag{r["lag"]} − placebo' for r in rows], rows, ss)
        for r, s in zip(rows, ss):
            keep(f'reapertura|{task}|lag{r["lag"]} − placebo', s3(s))
        for _, r in absol[absol.task.eq(task) & absol.strategy.str.startswith('curva')].iterrows():
            add(st, 'auc_absolutas.csv', f'{task} AUC {r.strategy}', 'auc', r.auc, float(wl[r.strategy[6:]].mean()))
        L = np.log2(p['lags'])
        diffs = np.column_stack([(wl[f'lag{l}'] - wl.placebo).to_numpy() for l in p['lags']])
        slope = ((diffs - diffs.mean(1, keepdims=True)) * (L - L.mean())).sum(1) / ((L - L.mean()) ** 2).sum()
        r = desc[(desc.task.eq(task)) & desc.item.str.startswith('pendiente')].iloc[0]
        s = stats(slope)
        add(st, 'descriptivos.csv', f'{task} pendiente por duplicación del desfase', 'delta', r.delta, s['delta'])
        add(st, 'descriptivos.csv', f'{task} pendiente por duplicación del desfase', 'p', r.p, s['p'], s['reg']['p'], 'perm')
        add(st, 'descriptivos.csv', f'{task} pendiente por duplicación del desfase', 'improved', r.improved, int((slope < 0).sum()), kind='int')
        keep(f'reapertura|{task}|pendiente', s3(s))
        for it in ['placebo'] + [f'lag{l}' for l in p['lags']]:
            r = desc[(desc.task.eq(task)) & desc.item.eq(f'{it} − c1_common')].iloc[0]
            cmp_contrast(st, 'descriptivos.csv', f'{task} {it} − c1_common', dict(r), (wl[it] - wl.c1_common).to_numpy())
        d = wl.lag6 - wl.placebo
        top = (d - d.mean()).abs().idxmax()
        keep(f'reapertura|{task}|lag6 influencia', dict(persona=top, delta_persona=round(float(d[top]), 4), mediana=round(float(d.median()), 4),
                                                       sin=s3(stats(d.drop(top).to_numpy()))))
        # ---- D1 (partición 1101)
        first = rep[rep.seed.eq(1101)]
        po = person_auc(first[first.strategy.eq('pos_only')]).auc
        r = desc[(desc.task.eq(task)) & desc.item.eq('D1 AUC solo posición en el estímulo')].iloc[0]
        add(st, 'descriptivos.csv', f'{task} D1 solo posición', 'auc', r.delta, float(po.mean()))
        c1 = first[first.strategy.eq('hgb_c1')].assign(pos=lambda x: x.source_row.map(W.posicion))
        sa = c1.groupby('participant').apply(lambda g: strat_auc(g, 'pos'))
        r = desc[(desc.task.eq(task)) & desc.item.eq('D1 AUC sin historial, estratificada por posición')].iloc[0]
        add(st, 'descriptivos.csv', f'{task} D1 AUC sin historial a igual posición', 'auc', r.delta, float(sa.mean()))
        # ---- D2 autocorrelación de la etiqueta a 6 s dentro del mismo estímulo
        lab = first[first.strategy.eq('hgb_c1')][['source_row', 'participant', 'y']].copy()
        lab['seg'], lab['t'] = lab.source_row.map(W.seg), (lab.source_row.map(W.t) * 1000).round().astype('int64')
        prev = lab[['seg', 't', 'y']].assign(t=lambda x: x.t + 1000 * p['label_lag']).rename(columns={'y': 'prob'})
        j = lab.merge(prev, on=['seg', 't'])
        ac = person_auc(j.assign(strategy='ac')).auc
        r = desc[(desc.task.eq(task)) & desc.item.str.startswith('D2')].iloc[0]
        add(st, 'descriptivos.csv', f'{task} D2 AUC etiqueta 6 s antes', 'auc', r.delta, float(ac.mean()), kind='loose')
        add(st, 'descriptivos.csv', f'{task} D2 pares', 'rows', r.rows, len(j), kind='int')
    cmp_family(st, 'confirmatorio.csv', [f[0] for f in fam], [f[1] for f in fam], [f[2] for f in fam])
    for name, _, s in fam:
        keep(f'reapertura|{name}', s3(s))


def stage_fase2():
    st = 'reapertura_fase2_41p_22-11-2026'
    p1 = proto('reapertura_41p_22-11-2026')
    W, _ = WT
    x1 = read(RES / st / 'x1_placebo_bloque.csv')
    x2 = read(RES / st / 'x2_estratificada.csv')
    desc = read(RES / st / 'descriptivos.csv')
    ph = read(RES / st / 'posthoc_no_registrado_estratos_con_posicion.csv')
    fam2 = []
    for task in ['atencion', 'activacion']:
        blk = read(RES / st / f'bloque_{task}.csv.gz')
        lag = LAG[task]
        integrity(st, f'bloque_{task}', blk, task, folds=p1['folds_main'], people=lag.participant.nunique())
        check(st, f'bloque_{task}: mismas ventanas que la curva de la fase 1', set(blk.source_row) == set(lag.source_row), len(blk))
        wl = wide_mean(pd.concat([lag, blk]))
        rows, ss = [], []
        for _, r in x1[x1.task.eq(task)].iterrows():
            s = cmp_contrast(st, 'x1_placebo_bloque.csv', f'{task} lag{r.lag} − placebo_bloque', dict(r), (wl[f'lag{r.lag}'] - wl.placebo_bloque).to_numpy())
            rows.append(dict(r)); ss.append(s)
        cmp_family(st, 'x1_placebo_bloque.csv', [f'{task} lag{r["lag"]} − placebo_bloque' for r in rows], rows, ss)
        for r, s in zip(rows, ss):
            keep(f'fase2|{task}|lag{r["lag"]} − placebo_bloque', s3(s))
        r = desc[(desc.task.eq(task)) & desc.item.eq('placebo_bloque − placebo disperso')].iloc[0]
        cmp_contrast(st, 'descriptivos.csv', f'{task} placebo_bloque − placebo disperso', dict(r), (wl.placebo_bloque - wl.placebo).to_numpy())
        rep = REP[task][REP[task].strategy.ne('pos_only')].join(W[['estimulo', 'bloque60', 'posicion']], on='source_row')
        check(st, f'{task}: todas las ventanas tienen estrato reconstruido', rep[['estimulo', 'bloque60', 'posicion']].notna().all().all())
        for col in ['estimulo', 'bloque60', 'posicion']:
            ws = wide_strat(rep, col)
            STRAT[(task, col)] = ws
            r = x2[(x2.task.eq(task)) & (x2.strata.eq(col))].iloc[0]
            s = cmp_contrast(st, 'x2_estratificada.csv', f'{task} {col} hgb_c32 − hgb_c1', dict(r), (ws.hgb_c32 - ws.hgb_c1).to_numpy())
            fam2.append((f'{task} {col} hgb_c32 − hgb_c1', dict(r), s))
            for sname in ['hgb_c1', 'hgb_c32']:
                r = desc[(desc.task.eq(task)) & desc.item.eq(f'{col}: AUC estratificada {sname}')].iloc[0]
                add(st, 'descriptivos.csv', f'{task} {col} AUC estratificada {sname}', 'auc', r.delta, float(ws[sname].mean()))
            one = rep[rep.seed.eq(1101) & rep.strategy.eq('hgb_c1')]

            def share(g):
                tot = int(g.y.sum()) * int((1 - g.y).sum())
                return sum(int(s_.y.sum()) * int((1 - s_.y).sum()) for _, s_ in g.groupby(col)) / tot
            r = desc[(desc.task.eq(task)) & desc.item.eq(f'{col}: fracción de pares dentro del estrato')].iloc[0]
            add(st, 'descriptivos.csv', f'{task} {col} fracción de pares', 'share', r.delta, float(one.groupby('participant').apply(share).mean()))
        # comprobación post hoc no registrada: misma estratificación sobre predicciones del 16 y 18-11
        old = pd.concat([FINAL[task][0][FINAL[task][0].strategy.isin(['hgb_c1', 'hgb_c32'])][['source_row', 'participant', 'y', 'prob', 'strategy']],
                         EXPL[task][['source_row', 'participant', 'y', 'prob', 'strategy']]]).assign(seed=0)
        old = old.join(W[['estimulo', 'bloque60', 'posicion']], on='source_row')
        for col in ['estimulo', 'bloque60', 'posicion']:
            ws = wide_strat(old, col)
            for _, r in ph[(ph.task.eq(task)) & (ph.strata.eq(col))].iterrows():
                a, b_ = r.contrast.split(' − ')
                s = cmp_contrast(st, 'posthoc_no_registrado_estratos_con_posicion.csv', f'{task} {col} {r.contrast}', dict(r), (ws[a] - ws[b_]).to_numpy())
                keep(f'fase2|posthoc|{task}|{col}|{r.contrast}', s3(s))
    cmp_family(st, 'x2_estratificada.csv', [f[0] for f in fam2], [f[1] for f in fam2], [f[2] for f in fam2])
    for name, _, s in fam2:
        keep(f'fase2|{name}', s3(s))
    w = STRAT[('activacion', 'bloque60')]
    d = w.hgb_c32 - w.hgb_c1
    top = (d - d.mean()).abs().idxmax()
    keep('fase2|activacion|bloque60 influencia', dict(persona=top, delta_persona=round(float(d[top]), 4), mediana=round(float(d.median()), 4),
                                                      sin=s3(stats(d.drop(top).to_numpy()))))


def stage_fase3():
    st = 'reapertura_fase3_41p_22-11-2026'
    p1 = proto('reapertura_41p_22-11-2026')
    W, _ = WT
    conf = read(RES / st / 'confirmatorio.csv')
    desc = read(RES / st / 'descriptivos.csv')
    fam = []
    for task in ['atencion', 'activacion']:
        pos = pd.concat([read(RES / st / f'pos_{task}_{s}.csv.gz') for s in p1['folds_rep']])
        integrity(st, f'pos_{task} (5 particiones)', pos, task, folds=p1['folds_rep'], by_seed=True, rows_expected=len(LABELS[task]))
        rep = REP[task][REP[task].strategy.isin(['hgb_c1', 'hgb_c32'])]
        m = pos[pos.strategy.eq('pos_c1')].merge(rep[rep.strategy.eq('hgb_c1')], on=['seed', 'source_row'], suffixes=('', '_f1'))
        check(st, f'pos_{task}: mismas filas, etiqueta, persona y fold que la fase 1 en cada partición',
              len(m) == pos.strategy.eq('pos_c1').sum() and (m.y == m.y_f1).all() and (m.fold == m.fold_f1).all() and (m.participant == m.participant_f1).all())
        allp = pd.concat([pos, rep]).join(W[['estimulo', 'bloque60', 'posicion']], on='source_row')
        POS[task] = allp
        scopes = {'todas': wide_mean(allp)}
        for col in ['estimulo', 'bloque60', 'posicion']:
            scopes[col] = wide_strat(allp, col)
        for _, r in conf[conf.task.eq(task)].iterrows():
            w = scopes[r.scope]
            d = (w.c32_pos - w.pos_c1)
            s = cmp_contrast(st, 'confirmatorio.csv', f'{task} {r.test}', dict(r), d.to_numpy())
            add(st, 'confirmatorio.csv', f'{task} {r.test}', 'median', r['median'], s['median'])
            top = (d - d.mean()).abs().idxmax()
            add(st, 'confirmatorio.csv', f'{task} {r.test}', 'influential', r.influential, top, kind='text')
            s2 = stats(d.drop(top).to_numpy())
            add(st, 'confirmatorio.csv', f'{task} {r.test}', 'delta_without', r.delta_without, s2['delta'])
            add(st, 'confirmatorio.csv', f'{task} {r.test}', 'low95_without', r.low95_without, s2['low95'], s2['reg']['low95'], 'boot')
            add(st, 'confirmatorio.csv', f'{task} {r.test}', 'high95_without', r.high95_without, s2['high95'], s2['reg']['high95'], 'boot')
            fam.append((f'{task} {r.test}', dict(r), s))
        for _, r in desc[desc.task.eq(task)].iterrows():
            w = scopes[r.scope]
            if r['item'].startswith('AUC '):
                add(st, 'descriptivos.csv', f'{task} {r.scope} {r["item"]}', 'auc', r.delta, float(w[r['item'][4:]].mean()))
                continue
            a, b_ = r['item'].split(' − ')
            s = cmp_contrast(st, 'descriptivos.csv', f'{task} {r.scope} {r["item"]}', dict(r), (w[a] - w[b_]).to_numpy())
            keep(f'fase3|{task}|{r.scope}|{r["item"]}', s3(s))
        one = allp[allp.seed.eq(1101) & allp.strategy.eq('pos_c1')]
        pairs = one.groupby('participant').apply(lambda g: sum(int(s_.y.sum()) * int((1 - s_.y).sum()) for _, s_ in g.groupby('estimulo')))
        keep(f'fase3|{task}|pares dentro del estímulo', dict(min=int(pairs.min()), persona_min=pairs.idxmin(), mediana=float(pairs.median())))
    cmp_family(st, 'confirmatorio.csv', [f[0] for f in fam], [f[1] for f in fam], [f[2] for f in fam])
    for name, _, s in fam:
        keep(f'fase3|{name}', s3(s))


def stage_enfoques():
    st = 'enfoques_41p_22-11-2026'
    p = proto(st)
    p1 = proto('reapertura_41p_22-11-2026')
    W, _ = WT
    seeds = p['seeds']

    def load(prefix):
        return pd.concat([read(RES / st / f'{prefix}_{s}.csv.gz') for s in seeds])

    def fam_check(file, items, rows, ss):
        cmp_family(st, file, items, rows, ss)
        for i, s in zip(items, ss):
            keep(f'enfoques|{i}', s3(s))

    # ---- E1
    e1 = load('e1')
    integrity(st, 'e1 (5 particiones)', e1, 'atencion_corregida', folds=p1['folds_rep'], by_seed=True, rows_expected=len(LABELS['atencion']))
    new = e1.drop_duplicates('source_row').set_index('source_row').y
    old = LABELS['atencion']
    check(st, 'e1: mismas ventanas que la etiqueta original', set(new.index) == set(old.index))
    keep('enfoques|E1|fracción de etiquetas cambiadas', round(float((new != old.reindex(new.index)).mean()), 4))
    wn, wo = wide_mean(e1), REPW['atencion']
    c = read(RES / st / 'e1_confirmatorio.csv')
    dsc = read(RES / st / 'e1_descriptivos.csv')
    spec = {'A1': wn.hgb_c1 - wo.hgb_c1, 'A2': wn.hgb_c32 - wn.hgb_c1, 'A3': wn.c32_pos - wn.pos_c1}
    ss = [cmp_contrast(st, 'e1_confirmatorio.csv', f'E1 {r.test}', dict(r), spec[r.test].to_numpy()) for _, r in c.iterrows()]
    fam_check('e1_confirmatorio.csv', [f'E1 {t}' for t in c.test], [dict(r) for _, r in c.iterrows()], ss)
    for _, r in dsc[dsc['item'].str.startswith('AUC ') & dsc.label.isna()].iterrows():
        add(st, 'e1_descriptivos.csv', f'E1 {r["item"]} (corregida)', 'auc', r.delta, float(wn[r['item'][4:]].mean()))
        keep(f'enfoques|E1|{r["item"]}', round(float(wn[r['item'][4:]].mean()), 5))
    same = e1[e1.strategy.eq('c32_pos')].set_index(['seed', 'source_row']).prob.sub(
        e1[e1.strategy.eq('hgb_c32')].set_index(['seed', 'source_row']).prob).abs().max()
    keep('enfoques|E1|max |prob c32_pos − prob hgb_c32|', float(same))
    cmp_contrast(st, 'e1_descriptivos.csv', 'E1 pos_c1 − hgb_c1 (corregida)', dict(dsc[dsc['item'].eq('pos_c1 − hgb_c1 (corregida)')].iloc[0]),
                 (wn.pos_c1 - wn.hgb_c1).to_numpy())
    keep('enfoques|E1|c32_pos − hgb_c32 (corregida)', s3(stats((wn.c32_pos - wn.hgb_c32).to_numpy())))
    keep('enfoques|E1|hgb_c32 − pos_c1 (corregida)', s3(stats((wn.hgb_c32 - wn.pos_c1).to_numpy())))

    # ---- E2
    e2 = load('e2')
    E2[0] = e2
    integrity(st, 'e2 (5 particiones)', e2[e2.strategy.ne('control_barajado')], 'atencion', folds=p1['folds_rep'], by_seed=True,
              rows_expected=len(LABELS['atencion']))
    ctrl = e2[e2.strategy.eq('control_barajado')]
    keep('enfoques|E2|control barajado: fracción de etiquetas distintas de la original',
         round(float((ctrl.set_index('source_row').y != LABELS['atencion'].reindex(ctrl.source_row).to_numpy()).mean()), 3))
    pred = pd.concat([e2[e2.strategy.ne('control_barajado')], REP['atencion'][REP['atencion'].strategy.eq('hgb_c1')]])
    w = wide_mean(pred)
    w['azar'] = .5
    E2W[0] = w
    c = read(RES / st / 'e2_confirmatorio.csv')
    dsc = read(RES / st / 'e2_descriptivos.csv')
    spec = {'B1': ('eeg_c1', 'azar'), 'B2': ('gsr_c1', 'azar'), 'B3': ('hgb_c1', 'eeg_c1'), 'B4': ('eeg_c1', 'gsr_c1'),
            'B5': ('eeg_alfa_beta', 'azar'), 'B6': ('eeg_posterior', 'azar'), 'B7': ('eeg_lento_amp', 'eeg_alfa_beta'),
            'B8': ('eeg_frontal', 'eeg_posterior')}
    for famname in ['E2', 'E2b']:
        cc = c[c.family.eq(famname)]
        ss = [cmp_contrast(st, 'e2_confirmatorio.csv', f'E2 {r.test}', dict(r), (w[spec[r.test][0]] - w[spec[r.test][1]]).to_numpy()) for _, r in cc.iterrows()]
        fam_check('e2_confirmatorio.csv', [f'E2 {t}' for t in cc.test], [dict(r) for _, r in cc.iterrows()], ss)
    for _, r in dsc[dsc['item'].str.startswith('AUC ') & dsc.label.isna()].iterrows():
        add(st, 'e2_descriptivos.csv', f'E2 {r["item"]}', 'auc', r.delta, float(w[r['item'][4:]].mean()))
    wc = wide_mean(ctrl)
    add(st, 'e2_descriptivos.csv', 'E2 control barajado − 0,5', 'delta', dsc[dsc['item'].str.startswith('control barajado')].delta.iloc[0],
        float((wc.control_barajado - .5).mean()))
    ws = wide_strat(pred.join(W[['posicion']], on='source_row'), 'posicion')
    for _, r in dsc[dsc['item'].str.startswith('AUC ') & dsc.label.eq('a igual posición')].iterrows():
        add(st, 'e2_descriptivos.csv', f'E2 {r["item"]} a igual posición', 'auc', r.delta, float(ws[r['item'][4:]].mean()))

    # ---- E3 (unidad: segmento)
    e3 = load('e3')
    integrity(st, 'e3 (5 particiones)', e3, 'activacion_seg', folds=p1['folds_rep'], by_seed=True, key='seg', label_check=False)
    lab = REP['activacion'][(REP['activacion'].seed.eq(1101)) & REP['activacion'].strategy.eq('hgb_c1')][['source_row', 'participant', 'y']]
    lab = lab.assign(seg=lab.source_row.map(W.seg))
    tab = lab.groupby('seg').agg(participant=('participant', 'first'), mean=('y', 'mean'), labelled=('y', 'size'))
    ties = int(tab['mean'].eq(.5).sum())
    tab = tab[tab['mean'].ne(.5)]
    tab['y'] = (tab['mean'] > .5).astype(int)
    one = e3[(e3.seed.eq(1101)) & e3.strategy.eq('seg')].set_index('seg')
    ok = set(one.index) == set(tab.index) and (one.y == tab.y.reindex(one.index)).all() and (one.participant == tab.participant.reindex(one.index)).all()
    check(st, 'e3: los segmentos, su persona y su etiqueta por mayoría se reconstruyen desde las ventanas (numeración de segmentos propia igual a la del archivo)',
          ok, f'{len(tab)} segmentos, {ties} empates excluidos')
    keep('enfoques|E3|segmentos', dict(n=len(tab), empates=ties, unanimes=round(float(tab['mean'].isin([0, 1]).mean()), 4),
                                       con_3_o_mas=int((tab.labelled >= 3).sum())))
    old = REP['activacion'][REP['activacion'].strategy.isin(['hgb_c1', 'hgb_c32'])].assign(seg=lambda x: x.source_row.map(W.seg))
    agg = old.groupby(['seed', 'strategy', 'seg']).prob.mean().reset_index().merge(tab[['participant', 'y']].reset_index(), on='seg')
    agg['strategy'] = agg.strategy.map({'hgb_c1': 'agg_c1', 'hgb_c32': 'agg_c32'})
    both = pd.concat([e3, agg])
    w = wide_mean(both)
    w['azar'] = .5
    c = read(RES / st / 'e3_confirmatorio.csv')
    dsc = read(RES / st / 'e3_descriptivos.csv')
    spec = {'C1': ('seg', 'azar'), 'C2': ('seg', 'agg_c32'), 'C3': ('seg_dur', 'dur_only')}
    ss = [cmp_contrast(st, 'e3_confirmatorio.csv', f'E3 {r.test}', dict(r), (w[spec[r.test][0]] - w[spec[r.test][1]]).to_numpy()) for _, r in c.iterrows()]
    fam_check('e3_confirmatorio.csv', [f'E3 {t}' for t in c.test], [dict(r) for _, r in c.iterrows()], ss)
    for _, r in dsc[dsc['item'].str.startswith('AUC ') & ~dsc['item'].str.contains('ventana')].iterrows():
        add(st, 'e3_descriptivos.csv', f'E3 {r["item"]}', 'auc', r.delta, float(w[r['item'][4:]].mean()))
    r = dsc[dsc['item'].eq('seg − agg_c1')].iloc[0]
    cmp_contrast(st, 'e3_descriptivos.csv', 'E3 seg − agg_c1', dict(r), (w.seg - w.agg_c1).to_numpy())
    w3 = wide_mean(both[both.seg.isin(tab.index[tab.labelled >= 3])])
    for a, b_ in [('seg', 'agg_c32'), ('seg_dur', 'dur_only')]:
        r = dsc[dsc['item'].eq(f'{a} − {b_} (segmentos con 3+ etiquetas)')].iloc[0]
        cmp_contrast(st, 'e3_descriptivos.csv', f'E3 {a} − {b_} (3+ etiquetas)', dict(r), (w3[a] - w3[b_]).to_numpy())

    # ---- E4c adaptación a la persona
    c = read(RES / st / 'e4_confirmatorio.csv')
    dsc = read(RES / st / 'e4_descriptivos.csv')
    rows, ss, items = [], [], []
    for task in ['atencion', 'activacion']:
        e4 = pd.concat([read(RES / st / f'e4_{task}_{s}.csv.gz') for s in seeds])
        integrity(st, f'e4_{task} (5 particiones)', e4, task, folds=p1['folds_rep'], by_seed=True, people=41 if task == 'atencion' else 40)
        base = REP[task][REP[task].strategy.isin(['hgb_c1', 'hgb_c32'])]
        glob = base.merge(e4[['seed', 'source_row']].drop_duplicates(), on=['seed', 'source_row'])
        check(st, f'e4_{task}: el modelo general se evalúa en las mismas filas que el adaptado', len(glob) == len(e4), f'{len(glob)} / {len(e4)}')
        # las filas de evaluación son posteriores al 40 % de la sesión, con 10 s de separación de la calibración
        ev = e4[e4.seed.eq(1101) & e4.strategy.eq('pers_c1')].assign(st=lambda x: x.source_row.map(W.st))
        dur = W.groupby('participant').st.max()
        frac = (ev.st / ev.participant.map(dur)).groupby(ev.participant).min()
        keep(f'enfoques|E4c|{task}|fracción mínima de sesión de una fila evaluada', round(float(frac.min()), 3))
        check(st, f'e4_{task}: ninguna fila de evaluación cae en el primer 40 % de la sesión', frac.min() > p['cal_fraction'], round(float(frac.min()), 4))
        wp = wide_mean(pd.concat([e4.drop(columns='cal_rows'), glob]))
        for _, r in c[c.task.eq(task)].iterrows():
            a, b_ = r.contrast.split(' − ')
            ss.append(cmp_contrast(st, 'e4_confirmatorio.csv', f'E4c {task} {r.contrast}', dict(r), (wp[a] - wp[b_]).to_numpy()))
            rows.append(dict(r)); items.append(f'E4c {task} {r.contrast}')
        for sname in ['hgb_c1', 'pers_c1', 'hgb_c32', 'pers_c32']:
            r = dsc[(dsc.task.eq(task)) & dsc['item'].eq(f'AUC {sname}')].iloc[0]
            add(st, 'e4_descriptivos.csv', f'E4c {task} AUC {sname}', 'auc', r.delta, float(wp[sname].mean()))
        r = dsc[(dsc.task.eq(task)) & dsc['item'].eq('pers_c32 − pers_c1')].iloc[0]
        cmp_contrast(st, 'e4_descriptivos.csv', f'E4c {task} pers_c32 − pers_c1', dict(r), (wp.pers_c32 - wp.pers_c1).to_numpy())
        # ---- E4a fiabilidad por mitades: segmentos alternados por orden temporal dentro de (persona, blur o no)
        sg = W.loc[LABELS[task].index]
        start = W.groupby('seg').agg(p=('participant', 'first'), t=('st', 'min'), blur=('stimulus', lambda s_: 'blur' in str(s_.iloc[0]).lower()))
        start = start.loc[np.unique(sg.seg)]
        start['half'] = start.groupby(['p', 'blur']).t.rank(method='first').astype(int) % 2
        b = base.assign(half=base.source_row.map(W.seg).map(start.half))
        w0, w1 = wide_mean(b[b.half.eq(0)]), wide_mean(b[b.half.eq(1)])
        for name, f in [('AUC sin historial', lambda x: x.hgb_c1), ('AUC con historial', lambda x: x.hgb_c32),
                        ('ganancia del historial', lambda x: x.hgb_c32 - x.hgb_c1)]:
            j = pd.concat([f(w0).rename('a'), f(w1).rename('b')], axis=1).dropna()
            r = dsc[(dsc.task.eq(task)) & dsc['item'].eq(f'fiabilidad por mitades: {name}')].iloc[0]
            rho = float(spearmanr(j.a, j.b).statistic)
            add(st, 'e4_descriptivos.csv', f'E4a {task} fiabilidad {name}', 'spearman', r.delta, rho, kind='loose')
            keep(f'enfoques|E4a|{task}|{name}', round(rho, 4))
    fam_check('e4_confirmatorio.csv', items, rows, ss)


def stage_montaje():
    st = 'montaje_ocular_41p_23-11-2026'
    per = read(RES / st / 'personas.csv')
    ch = read(RES / st / 'resumen_canales.csv')
    cj = json.loads((RES / st / 'comprobaciones.json').read_text())
    check(st, 'personas.csv: 41 personas', len(per) == 41, len(per))
    out = dict(lag_min=float(per.lag_parpadeo_s.min()), lag_max=float(per.lag_parpadeo_s.max()), lag_mediana=float(per.lag_parpadeo_s.median()),
               lag_q1=float(per.lag_parpadeo_s.quantile(.25)), lag_q3=float(per.lag_parpadeo_s.quantile(.75)),
               lag_h_min=float(per.lag_horizontal_s.min()), lag_h_max=float(per.lag_horizontal_s.max()),
               lag_v_min=float(per.lag_vertical_s.min()), lag_v_max=float(per.lag_vertical_s.max()),
               todos_positivos=bool((per[['lag_parpadeo_s', 'lag_horizontal_s', 'lag_vertical_s']] > 0).all().all()),
               canales_min=int(per.usable_channels.min()), canales_max=int(per.usable_channels.max()), canales_mediana=float(per.usable_channels.median()),
               parpadeos_min=int(per.blinks.min()), parpadeos_max=int(per.blinks.max()), fs=float(per.fs_effective.mean()), hueco_max=float(per.max_gap_s.max()),
               blink_uv={r.name_default: round(r.blink_ptp_uv_median, 1) for r in ch.itertuples()})
    add(st, 'comprobaciones.json', 'mediana del desfase (parpadeo)', 'lag', cj['lag_parpadeo_median_s'], out['lag_mediana'], kind='loose')
    cp = read(RES / st / 'canales_por_persona.csv')
    keep('montaje|columnas canales_por_persona', list(cp.columns))
    keep('montaje', out)


def stage_limpieza():
    st = 'limpieza_ocular_41p_23-11-2026'
    p = proto(st)
    W, _ = WT
    conf = read(RES / st / 'confirmatorio.csv')
    desc = read(RES / st / 'descriptivos.csv')
    app = read(RES / st / 'auc_por_persona.csv').set_index('participant')
    pred = pd.concat([read(RES / st / f'pred_{s}.csv.gz') for s in p['folds_rep']])
    main = pred[~pred.strategy.isin(['control_barajado', 'identidad_full'])]
    integrity(st, 'pred (5 particiones)', main, 'atencion', folds=p['folds_rep'], by_seed=True, rows_expected=len(LABELS['atencion']))
    ident = pred[pred.strategy.eq('identidad_full')].set_index('source_row').prob
    e2 = E2[0]
    ref = e2[(e2.seed.eq(1101)) & e2.strategy.eq('eeg_c1')].set_index('source_row').prob
    keep('limpieza|max |prob identidad − prob eeg_c1| (partición 1101)', float((ident - ref.reindex(ident.index)).abs().max()))
    check(st, 'filtro identidad reproduce las probabilidades de eeg_c1 del 22-11', (ident - ref.reindex(ident.index)).abs().max() < 1e-12)
    w = wide_mean(main).join(E2W[0][['eeg_c1', 'eeg_alfa_beta', 'eeg_lento_amp', 'eeg_posterior', 'eeg_frontal']])
    w['azar'] = .5
    LIMP[0] = w
    add(st, 'auc_por_persona.csv', f'AUC por persona (máxima diferencia, {app.size} valores)', 'auc', 0., float((app - w[app.columns]).abs().max().max()))
    spec = {'L1': ('eeg_c1', 'ica3_full'), 'L2': ('ctrl3_full', 'ica3_full'), 'L3': ('ica3_full', 'azar'), 'L4': ('ica3_alfa_beta', 'eeg_alfa_beta')}
    ss = [cmp_contrast(st, 'confirmatorio.csv', r.test, dict(r), (w[spec[r.test][0]] - w[spec[r.test][1]]).to_numpy()) for _, r in conf.iterrows()]
    cmp_family(st, 'confirmatorio.csv', list(conf.test), [dict(r) for _, r in conf.iterrows()], ss)
    for t, s in zip(conf.test, ss):
        keep(f'limpieza|{t}', s3(s))
    for _, r in desc.iterrows():
        it = r['item']
        if it.startswith('AUC '):
            add(st, 'descriptivos.csv', it, 'auc', r.delta, float(w[it[4:]].mean()))
        elif ' − ' in it and not it.startswith(('control', 'identidad', 'L', 'Spearman')):
            a, b_ = it.split(' − ')
            b_ = 'azar' if b_ == '0,5' else b_
            s = cmp_contrast(st, 'descriptivos.csv', it, dict(r), (w[a] - w[b_]).to_numpy())
            keep(f'limpieza|{it}', s3(s))
    for label, drop in [('sin P23 y P39 (canales planos a ratos)', ['P23', 'P39']),
                        ('sin P23, P39 ni identificación ocular débil', ['P23', 'P39', 'P12', 'P18', 'P22', 'P35', 'P40'])]:
        for t in spec:
            name = f'{t} {label}'
            r = desc[desc['item'].eq(name)].iloc[0]
            cmp_contrast(st, 'descriptivos.csv', name, dict(r), (w[spec[t][0]] - w[spec[t][1]]).drop(drop).to_numpy())
    wc = wide_mean(pred[pred.strategy.eq('control_barajado')])
    add(st, 'descriptivos.csv', 'control barajado − 0,5', 'delta', desc[desc['item'].str.startswith('control barajado')].delta.iloc[0],
        float((wc.control_barajado - .5).mean()))
    pl = read(RES / st / 'personas_limpieza.csv')
    keep('limpieza|personas', dict(n=len(pl), var_ica3_mediana=float(pl.var_share_ica3.median()), var_ctrl3_mediana=float(pl.var_share_ctrl3.median()),
                                   score1_bajo_015=sorted(pl[pl.score_1 < .15].participant), score1_hasta_014=sorted(pl[pl.score_1 <= .14].participant),
                                   lag_min=float(pl.lag_s.min()), lag_max=float(pl.lag_s.max()), canales_min=int(pl.usable_channels.min()),
                                   canales_max=int(pl.usable_channels.max())))


def stage_red():
    st = 'red_cruda_41p_23-11-2026'
    p = proto(st)
    conf = read(RES / st / 'confirmatorio.csv')
    desc = read(RES / st / 'descriptivos.csv')
    app = read(RES / st / 'auc_por_persona.csv').set_index('participant')
    seeds = list(p['folds_rep'])
    att = pd.concat([read(RES / st / f'{m}_{s}.csv.gz') for m in ['red_orig', 'red_ica3'] for s in seeds])
    act = pd.concat([read(RES / st / f'{m}_{s}.csv.gz') for m in ['red_act', 'hgb_eeg_act'] for s in seeds])
    integrity(st, 'redes de atención (5 particiones)', att, 'atencion', folds=p['folds_rep'], by_seed=True, rows_expected=len(LABELS['atencion']))
    integrity(st, 'red y HGB de activación (5 particiones)', act, 'activacion', folds=p['folds_rep'], by_seed=True, rows_expected=len(LABELS['activacion']))
    w = wide_mean(att).join(wide_mean(act)).join(LIMP[0][['eeg_c1', 'ica3_full']]).join(REPW['activacion'][['hgb_c1']])
    w['azar'] = .5
    add(st, 'auc_por_persona.csv', f'AUC por persona (máxima diferencia, {app.size} valores)', 'auc', 0., float((app - w[app.columns]).abs().max().max()))
    spec = {'R1': ('red_orig', 'eeg_c1'), 'R2': ('red_ica3', 'ica3_full'), 'R3': ('red_orig', 'red_ica3'), 'R4': ('red_act', 'hgb_eeg_act')}
    ss = [cmp_contrast(st, 'confirmatorio.csv', r.test, dict(r), (w[spec[r.test][0]] - w[spec[r.test][1]]).to_numpy()) for _, r in conf.iterrows()]
    cmp_family(st, 'confirmatorio.csv', list(conf.test), [dict(r) for _, r in conf.iterrows()], ss)
    for t, s in zip(conf.test, ss):
        keep(f'red|{t}', s3(s))
    for _, r in desc.iterrows():
        it = r['item']
        if it.startswith('AUC '):
            add(st, 'descriptivos.csv', it, 'auc', r.delta, float(w[it[4:]].mean()))
            keep(f'red|{it}|sobre 0,5', int((w[it[4:]] > .5).sum()))
        elif ' − ' in it:
            a, b_ = it.split(' (')[0].split(' − ')
            b_ = 'azar' if b_ == '0,5' else b_
            cmp_contrast(st, 'descriptivos.csv', it, dict(r), (w[a] - w[b_]).to_numpy())
    # robustez de R1: por partición y sin las dos personas más favorables
    pa = person_auc(att, ['seed', 'strategy'])
    e2 = E2[0]
    pe = person_auc(e2[e2.strategy.eq('eeg_c1')], ['seed', 'strategy'])
    for s_ in seeds:
        d = pa[(pa.seed.eq(int(s_))) & pa.strategy.eq('red_orig')].set_index('participant').auc - pe[pe.seed.eq(int(s_))].set_index('participant').auc
        keep(f'red|R1 partición {s_}', s3(stats(d.to_numpy())))
    d = (w.red_orig - w.eeg_c1).sort_values()
    keep('red|R1 sin las dos personas más favorables', dict(personas=list(d.index[-2:]), **s3(stats(d.iloc[:-2].to_numpy()))))
    all_auc = float(np.mean([auc(g.y.to_numpy(), g.prob.to_numpy()) for _, g in att[att.strategy.eq('red_orig')].groupby('seed')]))
    keep('red|AUC red_orig con todas las ventanas juntas', round(all_auc, 4))


# ------------------------------------------------------------------ registro en Git y hashes
def git(*a):
    return subprocess.run(['git', '-C', str(ROOT), *a], capture_output=True, text=True).stdout.strip()


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def chronology():
    rows = []
    stages = ['cierre_v3_16-11-2026', 'cierre_final_41p_16-11-2026', 'cierre_robustez_41p_16-11-2026', 'ampliacion_41p_16-11-2026',
              'ampliacion_41p_16-11-2026/enmienda_e1_lag6', 'explicativo_posicion_41p_18-11-2026', 'reapertura_41p_22-11-2026',
              'reapertura_fase2_41p_22-11-2026', 'reapertura_fase3_41p_22-11-2026', 'enfoques_41p_22-11-2026',
              'limpieza_ocular_41p_23-11-2026', 'red_cruda_41p_23-11-2026']
    for st in stages:
        d = RES / st
        pj = json.loads((d / 'protocolo.json').read_text())
        first_proto = git('log', '--diff-filter=A', '--format=%h %cI', '--', f'resultados/{st}/protocolo.json').splitlines()[-1]
        preds = sorted(x for x in d.glob('*.csv.gz'))
        commits = [git('log', '--diff-filter=A', '--format=%h %cI', '--', str(x.relative_to(ROOT))).splitlines()[-1] for x in preds]
        first_pred = min(commits, key=lambda c: c.split()[1]) if commits else ''
        mt = min((x.stat().st_mtime for x in preds), default=np.nan)
        hashes = pj.get('inputs', {})
        bad = [k for k, v in hashes.items() if (ROOT / k).exists() and sha(ROOT / k) != v]
        missing = [k for k in hashes if not (ROOT / k).exists()]
        rows.append(dict(stage=st, protocolo_created_utc=pj.get('created_utc'), commit_protocolo=first_proto, primer_commit_predicciones=first_pred,
                         mtime_local_primera_prediccion_utc=pd.Timestamp(mt, unit='s', tz='UTC').isoformat() if not np.isnan(mt) else '',
                         hashes=len(hashes), hashes_distintos=bad, hashes_sin_archivo=missing))
        ok = bool(first_pred) and first_proto.split()[1] <= first_pred.split()[1]
        check(st, 'Git: el protocolo entró al repositorio antes o junto con las predicciones', ok and first_proto.split()[0] != first_pred.split()[0],
              f'protocolo {first_proto}; predicciones {first_pred}')
        check(st, 'hashes de entradas del protocolo coinciden con los archivos actuales', not bad, f'{len(hashes)} hashes; distintos: {bad}; sin archivo: {missing}')
    keep('cronologia', rows)


# ------------------------------------------------------------------ comprobaciones adicionales del auditor
def extras():
    W, _ = WT
    # (a) ¿la ventaja de la red sobre el HGB cambia al limpiar? diferencia de diferencias, no registrada
    st = 'red_cruda_41p_23-11-2026'
    seeds = list(proto(st)['folds_rep'])
    att = pd.concat([read(RES / st / f'{m}_{s}.csv.gz') for m in ['red_orig', 'red_ica3'] for s in seeds])
    w = wide_mean(att).join(LIMP[0][['eeg_c1', 'ica3_full']])
    keep('extra|red: (red_orig − eeg_c1) − (red_ica3 − ica3_full)', s3(stats(((w.red_orig - w.eeg_c1) - (w.red_ica3 - w.ica3_full)).to_numpy())))
    # (b) fracción de la detección sobre el azar que desaparece con la limpieza
    l = LIMP[0]
    keep('extra|limpieza: caída / (AUC original − 0,5)', round(float((l.eeg_c1 - l.ica3_full).mean() / (l.eeg_c1 - .5).mean()), 3))
    keep('extra|limpieza: alfa-beta caída / (AUC − 0,5)', round(float((l.eeg_alfa_beta - l.ica3_alfa_beta).mean() / (l.eeg_alfa_beta - .5).mean()), 3))
    # (c) ¿c32_pos difiere de hgb_c32 en la fase 3 (etiqueta original)? contraste con E1, donde son idénticas
    for task in ['atencion', 'activacion']:
        a_ = POS[task]
        x = a_[a_.strategy.eq('c32_pos')].set_index(['seed', 'source_row']).prob
        y = a_[a_.strategy.eq('hgb_c32')].set_index(['seed', 'source_row']).prob.reindex(x.index)
        keep(f'extra|fase3 {task}: fracción de predicciones c32_pos idénticas a hgb_c32', round(float((x == y).mean()), 4))
    e1 = pd.concat([read(RES / 'enfoques_41p_22-11-2026' / f'e1_{s}.csv.gz') for s in seeds])
    for a_, b_ in [('c32_pos', 'hgb_c32'), ('pos_c1', 'hgb_c1')]:
        x = e1[e1.strategy.eq(a_)].set_index(['seed', 'source_row']).prob
        y = e1[e1.strategy.eq(b_)].set_index(['seed', 'source_row']).prob.reindex(x.index)
        keep(f'extra|E1: fracción de predicciones {a_} idénticas a {b_}', dict(fraccion=round(float((x == y).mean()), 4), n=len(x)))
    # (d) estabilidad de los límites pegados a un umbral, con 20 semillas de bootstrap propias
    def lows(d, q=.025):
        d = np.asarray(d, dtype=float)
        out = [float(np.quantile(d[np.random.default_rng(1000 + k).integers(0, len(d), (NBOOT, len(d)))].mean(1), q)) for k in range(20)]
        return [round(min(out), 5), round(max(out), 5)]
    ra, rc = REPW['atencion'], REPW['activacion']
    keep('extra|reapertura atención P1: rango del IC95 inferior', lows(ra.hgb_c32 - ra.hgb_c1))
    keep('extra|reapertura activación P1: rango del IC95 inferior', lows(rc.hgb_c32 - rc.hgb_c1))
    wl = wide_mean(LAG['activacion'])
    keep('extra|reapertura activación lag6 − placebo: rango del IC95 inferior', lows(wl.lag6 - wl.placebo))
    keep('extra|limpieza L1: rango del IC95 inferior', lows(l.eeg_c1 - l.ica3_full))
    w4 = AMPL['activacion']
    keep('extra|final activación principal: rango del IC95 inferior', lows(w4.hgb_c32 - w4.hgb_c1))
    # (e) multiplicidad: secundarios del análisis final y de la ampliación con Holm propio (no registrado)
    for name, keys in [('final secundarios (6)', [k for k in OUTJ if k.startswith('final|') and ' − ' in k and 'holm' not in k and 'hgb_c32 − hgb_c1' not in k]),
                       ('ampliacion E3 (6)', [k for k in OUTJ if k.startswith('ampliacion|') and '|E3|' in k]),
                       ('explicativo (6)', [k for k in OUTJ if k.startswith('explicativo|') and 'hgb_c32 − hgb_c1' not in k])]:
        h = holm([OUTJ[k]['p'] for k in keys])
        keep(f'extra|Holm del auditor sobre {name}', {k: round(float(x), 4) for k, x in zip(keys, h)})
    # (f) contraste principal de activación en todas las particiones vistas (misma hipótesis, mismas 41 personas)
    hist = {'16-11 partición registrada': OUTJ['final|activacion|hgb_c32 − hgb_c1']}
    for s_ in ['101', '202', '303']:
        hist[f'16-11 R3 {s_}'] = OUTJ[f'robustez|activacion|R3 partición {s_}']
    pa = person_auc(REP['activacion'], ['seed', 'strategy'])
    for s_ in seeds:
        ws = pa[pa.seed.eq(int(s_))].pivot(index='participant', columns='strategy', values='auc')
        hist[f'22-11 partición {s_}'] = s3(stats((ws.hgb_c32 - ws.hgb_c1).to_numpy()))
    keep('extra|activación principal por partición', {k: [v['delta'], v['low95'], v['high95'], v['p']] for k, v in hist.items()})
    pa = person_auc(REP['atencion'], ['seed', 'strategy'])
    keep('extra|atención P1 por partición: IC95 inferior', {s_: stats((lambda ws: (ws.hgb_c32 - ws.hgb_c1).to_numpy())(
        pa[pa.seed.eq(int(s_))].pivot(index='participant', columns='strategy', values='auc')))['low95'] for s_ in seeds})
    # (g) activación: ¿mirada y pupila agregan al EEG en la ventana actual? (descriptivo de la red cruda)
    act = pd.concat([read(RES / st / f'hgb_eeg_act_{s}.csv.gz') for s in seeds])
    wa = wide_mean(act).join(rc[['hgb_c1']])
    s_ = stats((wa.hgb_c1 - wa.hgb_eeg_act).to_numpy())
    s_['decision'] = decide(s_['low95'], s_['high95'], s_['low90'], s_['high90'], 1.)
    keep('extra|activación: (EEG + mirada + pupila) − solo EEG, ventana actual', s3(s_))
    # (h) hashes de datos locales fuera de Git
    loc = ROOT.parents[1] / 'datos/locales/v2_2025'
    res = {}
    for stage, key, folder in [('limpieza_ocular_41p_23-11-2026', 'raw', 'cache_ocular'), ('red_cruda_41p_23-11-2026', 'raw', 'cache_ocular')]:
        hs = proto(stage).get(key, {})
        bad = [k for k, v in hs.items() if not (loc / folder / k).exists() or sha(loc / folder / k) != v]
        res[f'{stage} {key}'] = [len(hs), bad]
        check(stage, f'hashes de crudos en caché ({len(hs)}) coinciden con datos/locales', not bad, bad)
    hs = json.loads((RES / 'red_cruda_41p_23-11-2026/tensores.json').read_text())
    bad = [k for k, v in hs.items() if not (loc / 'red_cruda_tensores' / k).exists() or sha(loc / 'red_cruda_tensores' / k) != v]
    check('red_cruda_41p_23-11-2026', f'hashes de tensores ({len(hs)}) coinciden con datos/locales', not bad, bad)
    hs = json.loads((RES / 'limpieza_ocular_41p_23-11-2026/limpieza.json').read_text())['features']
    bad = [k for k, v in hs.items() if not (loc / 'limpieza_ocular_variables' / f'{k}.pkl').exists() or sha(loc / 'limpieza_ocular_variables' / f'{k}.pkl') != v]
    check('limpieza_ocular_41p_23-11-2026', f'hashes de variables recalculadas ({len(hs)}) coinciden con datos/locales', not bad, bad)


# ------------------------------------------------------------------ coherencia entre documentos
def r_half_up(x, nd):
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))


def cell(stage, file, col, **q):
    df = read(RES / stage / file)
    for k, v in q.items():
        df = df[df[k].astype(object).where(df[k].notna(), 'nan').astype(str).eq(str(v))]
    assert len(df) == 1, (stage, file, q, len(df))
    return float(df[col].iloc[0])


def documents():
    F_, RB, AM, EN, EX = 'cierre_final_41p_16-11-2026', 'cierre_robustez_41p_16-11-2026', 'ampliacion_41p_16-11-2026', 'ampliacion_41p_16-11-2026/enmienda_e1_lag6', 'explicativo_posicion_41p_18-11-2026'
    R1, R2, R3, EF, MO, LI, RD = ('reapertura_41p_22-11-2026', 'reapertura_fase2_41p_22-11-2026', 'reapertura_fase3_41p_22-11-2026', 'enfoques_41p_22-11-2026',
                                 'montaje_ocular_41p_23-11-2026', 'limpieza_ocular_41p_23-11-2026', 'red_cruda_41p_23-11-2026')
    c = cell
    S = {   # clave -> (valores fuente, descripción de la fuente)
        'P1 atención': ([c(R1, 'confirmatorio.csv', k, task='atencion', test='P1') for k in ('delta', 'low95', 'high95')], f'{R1}/confirmatorio.csv atención P1'),
        'P1 activación': ([c(R1, 'confirmatorio.csv', k, task='activacion', test='P1') for k in ('delta', 'low95', 'high95')], f'{R1}/confirmatorio.csv activación P1'),
        'P2 activación': ([c(R1, 'confirmatorio.csv', k, task='activacion', test='P2') for k in ('delta', 'low95', 'high95')], f'{R1}/confirmatorio.csv activación P2'),
        'Q1 atención': ([c(R3, 'confirmatorio.csv', k, task='atencion', test='Q1') for k in ('delta', 'low95', 'high95')], f'{R3}/confirmatorio.csv atención Q1'),
        'Q2 atención': ([c(R3, 'confirmatorio.csv', 'delta', task='atencion', test='Q2')], f'{R3}/confirmatorio.csv atención Q2'),
        'Q1 activación': ([c(R3, 'confirmatorio.csv', k, task='activacion', test='Q1') for k in ('delta', 'low95', 'high95')], f'{R3}/confirmatorio.csv activación Q1'),
        'Q2 activación': ([c(R3, 'confirmatorio.csv', 'delta', task='activacion', test='Q2')], f'{R3}/confirmatorio.csv activación Q2'),
        'lag6 activación': ([c(R1, 'curva_temporal.csv', k, task='activacion', lag=6) for k in ('delta', 'low95', 'high95')], f'{R1}/curva_temporal.csv activación lag 6'),
        'lag12 activación': ([c(R1, 'curva_temporal.csv', 'delta', task='activacion', lag=12)], f'{R1}/curva_temporal.csv activación lag 12'),
        'GRU atención': ([c(F_, 'contrastes.csv', k, task='atencion', contrast='gru_c32 − gru_c1') for k in ('delta', 'low95', 'high95')], f'{F_}/contrastes.csv atención gru_c32 − gru_c1'),
        'GRU−HGB atención': ([c(F_, 'contrastes.csv', 'delta', task='atencion', contrast='gru_c32 − hgb_c32')], f'{F_}/contrastes.csv atención gru_c32 − hgb_c32'),
        'tardía−temprana atención': ([c(AM, 'contrastes.csv', k, task='atencion', contrast='mlp_tardia − mlp_temprana') for k in ('delta', 'low95', 'high95')], f'{AM}/contrastes.csv atención mlp_tardia − mlp_temprana'),
        'AUC eeg_c1': ([c(EF, 'e2_descriptivos.csv', 'delta', item='AUC eeg_c1', label='nan')], f'{EF}/e2_descriptivos.csv AUC eeg_c1'),
        'AUC ica3_full': ([c(LI, 'descriptivos.csv', 'delta', item='AUC ica3_full')], f'{LI}/descriptivos.csv AUC ica3_full'),
        'AUC hgb_eeg_act': ([c(RD, 'descriptivos.csv', 'delta', item='AUC hgb_eeg_act')], f'{RD}/descriptivos.csv AUC hgb_eeg_act'),
        'AUC red_orig': ([c(RD, 'descriptivos.csv', 'delta', item='AUC red_orig')], f'{RD}/descriptivos.csv AUC red_orig'),
        'AUC red_ica3': ([c(RD, 'descriptivos.csv', 'delta', item='AUC red_ica3')], f'{RD}/descriptivos.csv AUC red_ica3'),
        'AUC red_act': ([c(RD, 'descriptivos.csv', 'delta', item='AUC red_act')], f'{RD}/descriptivos.csv AUC red_act'),
        'R1 red': ([c(RD, 'confirmatorio.csv', k, test='R1') for k in ('delta', 'low95', 'high95')], f'{RD}/confirmatorio.csv R1'),
        'final atención': ([c(F_, 'contrastes.csv', k, task='atencion', role='principal') for k in ('delta', 'low95', 'high95')], f'{F_}/contrastes.csv atención principal'),
        'final activación': ([c(F_, 'contrastes.csv', k, task='activacion', role='principal') for k in ('delta', 'low95', 'high95')], f'{F_}/contrastes.csv activación principal'),
        'R1 placebo atención': ([c(RB, 'resultados.csv', k, task='atencion', prueba='R1 placebo') for k in ('delta', 'low95', 'high95')], f'{RB}/resultados.csv atención R1 placebo'),
        'R1 placebo activación': ([c(RB, 'resultados.csv', k, task='activacion', prueba='R1 placebo') for k in ('delta', 'low95', 'high95')], f'{RB}/resultados.csv activación R1 placebo'),
        'lag6 enmienda': ([c(EN, 'contrastes.csv', k, task='activacion', contrast='lag6_real − lag6_placebo') for k in ('delta', 'low95', 'high95')], f'{EN}/contrastes.csv activación lag6_real − lag6_placebo'),
        'posición atención': ([c(EX, 'contrastes.csv', k, task='atencion', contrast='pos_c1 − hgb_c1') for k in ('delta', 'low95', 'high95')], f'{EX}/contrastes.csv atención pos_c1 − hgb_c1'),
        'mismo minuto activación': ([c(R2, 'x2_estratificada.csv', k, task='activacion', strata='bloque60') for k in ('delta', 'low95', 'high95')], f'{R2}/x2_estratificada.csv activación bloque60'),
        'E1 pos_only': ([c(EF, 'e1_descriptivos.csv', 'delta', item='AUC pos_only')], f'{EF}/e1_descriptivos.csv AUC pos_only'),
        'E1 hgb_c1 corregida': ([c(EF, 'e1_descriptivos.csv', 'delta', item='AUC hgb_c1', label='nan')], f'{EF}/e1_descriptivos.csv AUC hgb_c1 (corregida)'),
        'E1 hgb_c1 original': ([c(EF, 'e1_descriptivos.csv', 'delta', item='AUC hgb_c1', label='original')], f'{EF}/e1_descriptivos.csv AUC hgb_c1 (original)'),
        'B3 GSR sobre EEG': ([c(EF, 'e2_confirmatorio.csv', 'delta', test='B3')], f'{EF}/e2_confirmatorio.csv B3'),
        'AUC eeg_lento_amp': ([c(EF, 'e2_descriptivos.csv', 'delta', item='AUC eeg_lento_amp', label='nan')], f'{EF}/e2_descriptivos.csv AUC eeg_lento_amp'),
        'AUC eeg_alfa_beta': ([c(EF, 'e2_descriptivos.csv', 'delta', item='AUC eeg_alfa_beta', label='nan')], f'{EF}/e2_descriptivos.csv AUC eeg_alfa_beta'),
        'AUC ica3_alfa_beta': ([c(LI, 'descriptivos.csv', 'delta', item='AUC ica3_alfa_beta')], f'{LI}/descriptivos.csv AUC ica3_alfa_beta'),
        'E3 seg': ([c(EF, 'e3_descriptivos.csv', 'delta', item='AUC seg')], f'{EF}/e3_descriptivos.csv AUC seg'),
        'E3 C2': ([c(EF, 'e3_confirmatorio.csv', 'delta', test='C2')], f'{EF}/e3_confirmatorio.csv C2'),
        'E4 fiabilidad atención': ([c(EF, 'e4_descriptivos.csv', 'delta', task='atencion', item='fiabilidad por mitades: AUC sin historial')], f'{EF}/e4_descriptivos.csv'),
        'E4 fiabilidad activación': ([c(EF, 'e4_descriptivos.csv', 'delta', task='activacion', item='fiabilidad por mitades: AUC sin historial')], f'{EF}/e4_descriptivos.csv'),
        'E4 adaptación activación': ([c(EF, 'e4_confirmatorio.csv', k, task='activacion', contrast='pers_c32 − hgb_c32') for k in ('delta', 'low95', 'high95')], f'{EF}/e4_confirmatorio.csv activación pers_c32 − hgb_c32'),
        'L1': ([c(LI, 'confirmatorio.csv', k, test='L1') for k in ('delta', 'low95', 'high95')], f'{LI}/confirmatorio.csv L1'),
        'AUC ctrl3_full': ([c(LI, 'descriptivos.csv', 'delta', item='AUC ctrl3_full')], f'{LI}/descriptivos.csv AUC ctrl3_full'),
        'var ica3': ([c(LI, 'descriptivos.csv', 'delta', item='limpieza: mediana var_share_ica3')], f'{LI}/descriptivos.csv mediana var_share_ica3'),
        'var ctrl3': ([c(LI, 'descriptivos.csv', 'delta', item='limpieza: mediana var_share_ctrl3')], f'{LI}/descriptivos.csv mediana var_share_ctrl3'),
        'desfase': ([OUTJ['montaje']['lag_min'], OUTJ['montaje']['lag_max']], f'{MO}/personas.csv lag_parpadeo_s mín y máx'),
        'prevalencia último quintil': ([c(AM, 'fatiga_por_quintil.csv', 'prevalencia_alta', task='activacion', strategy='hgb_c1', quintil=5)], f'{AM}/fatiga_por_quintil.csv'),
        'AUC atención quintil 1 y 5': ([c(AM, 'fatiga_por_quintil.csv', 'auc', task='atencion', strategy='hgb_c1', quintil=q) for q in (1, 5)], f'{AM}/fatiga_por_quintil.csv'),
        'AUC activación mín y máx': ([c(R1, 'auc_absolutas.csv', 'auc', task='activacion', strategy='hgb_c1'), c(EF, 'e3_descriptivos.csv', 'delta', item='AUC seg')], 'reapertura hgb_c1 y enfoques E3 seg'),
    }
    CI, CO = 'Cierre_Experimental_Final_23-11-2026.md', 'Borrador Conclusiones 23-11-2026.md'
    claims = [  # (documento, lugar, clave, valores informados, decimales)
        (CI, 'Conclusión general / fase 1', 'P1 atención', [.029, .021, .037], 3), (CI, 'Conclusión general / fase 1', 'P1 activación', [.036, .010, .065], 3),
        (CI, 'Conclusión general / fase 3', 'Q1 atención', [.001, -.002, .005], 3), (CI, 'Conclusión general / curva', 'lag6 activación', [.047, .018, .078], 3),
        (CI, 'Conclusión general / fase 3', 'Q1 activación', [.032, .004, .059], 3), (CI, 'Conclusión general (GRU)', 'GRU atención', [.008, -.004, .020], 3),
        (CI, 'Conclusión general (GRU bajo HGB)', 'GRU−HGB atención', [-.040], 3), (CI, 'Conclusión general (fusión)', 'tardía−temprana atención', [.012, .005, .021], 3),
        (CI, 'Conclusión general / limpieza', 'AUC eeg_c1', [.681], 3), (CI, 'Conclusión general / limpieza', 'AUC ica3_full', [.621], 3),
        (CI, 'Conclusión general / red', 'AUC hgb_eeg_act', [.524], 3), (CI, 'Conclusión general / red', 'AUC red_orig', [.716], 3),
        (CI, 'Conclusión general / red', 'R1 red', [.035, .023, .047], 3), (CI, 'Conclusión general / red', 'AUC red_act', [.498], 3), (CI, 'Red', 'AUC red_ica3', [.649], 3),
        (CI, '16 al 18-11: análisis final', 'final atención', [.026, .018, .035], 3), (CI, '16 al 18-11: análisis final', 'final activación', [.034, -.001, .069], 3),
        (CI, '16 al 18-11: robustez', 'R1 placebo atención', [-.000, -.003, .003], 3), (CI, '16 al 18-11: robustez', 'R1 placebo activación', [.038, .006, .068], 3),
        (CI, '16 al 18-11: ampliación', 'lag6 enmienda', [.046, .018, .073], 3), (CI, '16 al 18-11: explicativo', 'posición atención', [.028, .021, .035], 3),
        (CI, '22-11: fase 1', 'P2 activación', [.026, -.006, .056], 3), (CI, '22-11: curva', 'lag12 activación', [.024], 3),
        (CI, '22-11: fase 2', 'mismo minuto activación', [.058, .027, .092], 3), (CI, '22-11: fase 3', 'Q2 atención', [-.000], 3), (CI, '22-11: fase 3', 'Q2 activación', [.009], 3),
        (CI, 'E1', 'E1 pos_only', [.504], 3), (CI, 'E1', 'E1 hgb_c1 corregida', [.675], 3), (CI, 'E1', 'E1 hgb_c1 original', [.683], 3),
        (CI, 'E2', 'B3 GSR sobre EEG', [.002], 3), (CI, 'E2', 'AUC eeg_lento_amp', [.673], 3), (CI, 'E2', 'AUC eeg_alfa_beta', [.593], 3),
        (CI, 'E3', 'E3 seg', [.587], 3), (CI, 'E3', 'E3 C2', [.020], 3), (CI, 'E4', 'E4 fiabilidad atención', [.76], 2), (CI, 'E4', 'E4 fiabilidad activación', [.66], 2),
        (CI, 'E4', 'E4 adaptación activación', [.045, .023, .069], 3), (CI, 'Montaje', 'desfase', [.18, .53], 2),
        (CI, 'Limpieza', 'L1', [.060, .045, .075], 3), (CI, 'Limpieza', 'var ica3', [.035], 3), (CI, 'Limpieza', 'var ctrl3', [.72], 2), (CI, 'Limpieza', 'AUC ctrl3_full', [.674], 3),
        (CI, 'Limpieza', 'AUC ica3_alfa_beta', [.547], 3), (CI, 'Límites', 'AUC activación mín y máx', [.52, .59], 2),
        (CO, '9.1', 'P1 activación', [.036, .010, .065], 3), (CO, '9.1', 'lag6 activación', [.047, .018, .078], 3), (CO, '9.1', 'Q1 activación', [.032, .004, .059], 3),
        (CO, '9.1', 'P1 atención', [.029, .021, .037], 3), (CO, '9.1', 'Q1 atención', [.001, -.002, .005], 3), (CO, '9.1', 'GRU−HGB atención', [-.040], 3),
        (CO, '9.2', 'tardía−temprana atención', [.012, .005, .021], 3), (CO, '9.2', 'B3 GSR sobre EEG', [.002], 3),
        (CO, '9.3', 'AUC eeg_c1', [.681], 3), (CO, '9.3', 'AUC red_orig', [.716], 3), (CO, '9.3', 'var ica3', [.035], 3), (CO, '9.3', 'AUC ica3_full', [.621], 3),
        (CO, '9.3', 'var ctrl3', [.72], 2), (CO, '9.3', 'AUC ctrl3_full', [.674], 3), (CO, '9.3', 'AUC hgb_eeg_act', [.524], 3), (CO, '9.3', 'AUC red_act', [.498], 3),
        (CO, '9.3', 'E4 adaptación activación', [.045, .023, .069], 3), (CO, '9.3', 'E3 seg', [.587], 3),
        (CO, '9.4', 'prevalencia último quintil', [.37], 2), (CO, '9.4', 'AUC atención quintil 1 y 5', [.65, .71], 2),
        (CO, '9.5', 'L1', [.060], 3), (CO, '9.5', 'desfase', [.18, .53], 2), (CO, '9.5', 'AUC activación mín y máx', [.52, .59], 2),
    ]
    rows = []
    for doc, where, key, rep, nd in claims:
        src, desc = S[key]
        for r_, s_ in zip(rep, src):
            right = r_half_up(s_, nd)
            dbl = r_half_up(r_half_up(s_, nd + 1), nd)
            v = 'coincide' if abs(right - r_) < 1e-12 else ('redondeo doble (se redondeó dos veces)' if abs(dbl - r_) < 1e-12 else 'DISCREPA')
            rows.append(dict(documento=doc, lugar=where, cifra=key, informada=r_, fuente=s_, fuente_redondeada=right, veredicto=v, archivo_fuente=desc))
    d = pd.DataFrame(rows)
    d.to_csv(HERE / 'coherencia_documentos.csv', index=False)
    print('\nCOHERENCIA CIERRE Y CONCLUSIONES:', d.veredicto.value_counts().to_dict())
    print(d[d.veredicto.ne('coincide')].to_string(index=False))
    # ---- cifras de cada INFORME frente a los CSV de su etapa: búsqueda de redondeos dobles
    import re
    cand = []
    for st in sorted({r['stage'] for r in COMP}):
        folder = RES / st
        inf = folder / 'INFORME.md' if (folder / 'INFORME.md').exists() else folder.parent / 'INFORME.md'
        text = inf.read_text().replace('−', '-') if inf.exists() else ''
        for f in sorted(folder.glob('*.csv')):
            df = read(f)
            for col in df.select_dtypes('number').columns:
                for i, v in df[col].dropna().items():
                    if abs(v) >= 1 or abs(v) < 1e-4:
                        continue
                    right, dbl = r_half_up(v, 3), r_half_up(r_half_up(v, 4), 3)
                    if right != dbl:
                        sr, sd = f'{abs(right):.3f}'.replace('.', ','), f'{abs(dbl):.3f}'.replace('.', ',')
                        label = ' '.join(str(x) for x in df.loc[i].tolist()[:4] if isinstance(x, str))
                        cand.append(dict(stage=st, file=f.name, fila=label, columna=col, valor=v, correcto=sr, doble=sd,
                                         informe_contiene_doble=sd in text, informe_contiene_correcto=sr in text))
    cd = pd.DataFrame(cand)
    cd.to_csv(HERE / 'redondeos_candidatos.csv', index=False)
    print('\nREDONDEOS DOBLES CANDIDATOS presentes en el INFORME de su etapa:')
    print(cd[cd.informe_contiene_doble].to_string(index=False))


FINAL, AMPL, EXPL, REP, REPW, LAG, STRAT, POS, E2, E2W, LIMP = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}

if __name__ == '__main__':
    WT = windows_table()
    for f in [stage_v3, stage_final, stage_robustez, stage_ampliacion, stage_explicativo, stage_reapertura, stage_fase2, stage_fase3,
              stage_enfoques, stage_montaje, stage_limpieza, stage_red, chronology, extras]:
        print('>>', f.__name__, flush=True)
        f()
    comp, integ = pd.DataFrame(COMP), pd.DataFrame(INTEG)
    documents()
    comp.to_csv(HERE / 'comparaciones.csv', index=False)
    integ.to_csv(HERE / 'integridad.csv', index=False)
    (HERE / 'recalculo.json').write_text(json.dumps(OUTJ, ensure_ascii=False, indent=1, default=str))
    pd.set_option('display.width', 250, 'display.max_colwidth', 90, 'display.max_rows', 500)
    print('\nCOMPARACIONES POR ETAPA')
    print(comp.assign(v=comp.verdict.str.split(';').str[0]).groupby(['stage', 'v']).size().unstack(fill_value=0).to_string())
    num = comp[comp.kind.ne('text')]
    print('\nDIFERENCIA MÁXIMA POR ETAPA Y TIPO')
    print(num.assign(diff=num['diff'].astype(float)).groupby(['stage', 'kind'])['diff'].max().unstack().to_string())
    print('\nNO REPRODUCE CON LA SEMILLA REGISTRADA:', int(comp.verdict.str.contains('semilla registrada').sum()))
    bad = comp[comp.verdict.str.startswith('DISCREPA')]
    print('\nDISCREPANCIAS:', len(bad))
    print(bad.to_string(index=False))
    print('\nINTEGRIDAD: fallan', int((~integ.ok).sum()), 'de', len(integ))
    print(integ[~integ.ok].to_string(index=False))
