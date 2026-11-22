"""Reapertura, fase 2 (22-11-2026): controles POST HOC motivados por la auditoría de código de la fase 1.

Se registra ANTES de ver cualquier resultado de la fase 1 (las corridas de la fase 1 siguen en ejecución al
registrar esto). Aun así es exploratorio: lo motivó una auditoría y no estaba en el protocolo de la fase 1.

La auditoría de código de `reapertura_41p.py` señaló, sin mirar resultados:
  A. El placebo de la curva temporal son ventanas sueltas repartidas por la sesión, mientras que las bandas son
     bloques contiguos; además las bandas cercanas pertenecen en parte al mismo estímulo que la ventana actual
     (73 % en el desfase 6 de activación, 0 % desde el desfase 48) y la etiqueta está muy agrupada por estímulo.
     La curva mezcla cercanía temporal, contigüidad y pertenecer al mismo estímulo.
  B. La etiqueta de activación deriva a lo largo de la sesión con dirección distinta en cada persona; el control
     del tiempo de sesión de P2 solo corrige la tendencia común.
  C. El historial hasta 32 codifica la posición dentro del estímulo.

Controles (misma configuración congelada, mismos folds, mismas filas):
  X1 Placebo de bloque (entrena un modelo por tarea): el mismo número de ventanas que la banda de 6 s, de la
     misma persona, contiguas (dentro de 6 s) y a 150 s o más. Contraste: desfase L − placebo de bloque, para los
     5 desfases, en las filas comunes de la fase 1. Holm sobre los 5 desfases dentro de cada tarea. Aísla la
     cercanía temporal de la contigüidad. Los desfases 48 y 96 no comparten estímulo con la ventana actual, así
     que ahí el contraste mide cercanía temporal entre estímulos distintos.
  X2 AUC estratificada (sin entrenar; usa las predicciones de las 5 particiones de la fase 1). La AUC de cada
     persona se calcula solo con pares de ventanas del mismo estrato, ponderada por número de pares, y se promedia
     sobre las 5 particiones. Estratos: (a) mismo estímulo/segmento, (b) mismo bloque de 60 s de sesión,
     (c) misma posición dentro del estímulo. Contraste: HGB hasta 32 − HGB sin historial dentro de cada
     estratificación. Holm sobre las 6 pruebas (3 estratificaciones × 2 tareas).
     (a) pregunta si el historial distingue momentos dentro de un mismo estímulo; (b) si la ganancia sobrevive
     al quitar la deriva lenta de cada persona; (c) si sobrevive al quitar la posición.

Reglas de decisión: las del análisis final (margen 0,02), aplicadas como lectura exploratoria.
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

OUT = ROOT / 'resultados/reapertura_fase2_41p_22-11-2026'
BLOCK_SEED = 20261123
SESSION_BLOCK = 60
STRATA = ['estimulo', 'bloque60', 'posicion']


def plan():
    return json.loads((OUT / 'protocolo.json').read_text())


def prepare():
    OUT.mkdir(exist_ok=False)
    for t in F.LEAVES:  # se registra antes de que exista ningún resultado de la fase 1
        assert not (R.OUT / 'confirmatorio.csv').exists()
    paths = [Path(__file__), ROOT / 'scripts/reapertura_41p.py', R.OUT / 'protocolo.json']
    write(OUT / 'protocolo.json', dict(
        created_utc=pd.Timestamp.now(tz='UTC').isoformat(), post_hoc=True,
        motive='Auditoría independiente de código de la fase 1 (hallazgos A, B y C), recibida con la fase 1 en '
               'ejecución y sin resultados vistos.',
        inputs={str(p.relative_to(ROOT)): digest(p) for p in paths},
        phase1_files_present=sorted(p.name for p in R.OUT.glob('*.csv.gz')),
        block_seed=BLOCK_SEED, session_block=SESSION_BLOCK, strata=STRATA,
        x1=dict(tests=[f'lag{L} − placebo_bloque' for L in R.LAGS], holm='5 desfases dentro de cada tarea'),
        x2=dict(tests=[f'hgb_c32 − hgb_c1 estratificada por {s}' for s in STRATA], holm='6 pruebas (3 × 2 tareas)',
                unit='AUC estratificada por persona, promediada sobre las 5 particiones de la fase 1'),
        decision='Reglas del análisis final con margen 0,02, como lectura exploratoria.'))
    print('Registrado', OUT / 'protocolo.json')


def block_placebo(T, counts):
    """Bloque contiguo (dentro de BAND s) de `counts` ventanas de la misma persona, a PLACEBO_GAP s o más."""
    t = R.seconds(T)
    person = T.all.participant.to_numpy()
    rng = np.random.default_rng(BLOCK_SEED)
    ix = np.full((len(t), R.BAND + 2), -1, dtype=np.int64)
    n = np.zeros(len(t), dtype=np.int64)
    for p in np.unique(person):
        rows = np.flatnonzero(person == p)
        rows = rows[np.argsort(t[rows], kind='stable')]
        tt = t[rows]
        starts = {}
        for k in range(1, R.BAND + 1):
            j = np.arange(len(rows) - k + 1)
            starts[k] = j[tt[j + k - 1] - tt[j] < R.BAND]
        for r in rows:
            k = counts[r]
            if k == 0:
                continue
            j = starts[k]
            far = j[(tt[j + k - 1] <= t[r] - R.PLACEBO_GAP) | (tt[j] >= t[r] + R.PLACEBO_GAP)]
            if not len(far):
                continue
            s = rng.choice(far)
            ix[r, :k] = rows[s:s + k]
            n[r] = k
    return ix, n


def common_rows(T):
    """Las mismas filas comunes de la fase 1."""
    bands = {L: R.band_indices(T, L) for L in R.LAGS}
    plc = R.placebo_indices(T, bands[R.LAGS[0]][1])
    ok = np.all([n >= R.MIN_BAND for _, n in bands.values()], axis=0) & (plc[1] >= R.MIN_BAND)
    return np.flatnonzero(ok[T.lab_pos]), bands


def run(task):
    p = plan()
    for path, h in p['inputs'].items():
        assert digest(ROOT / path) == h, path
    dest = OUT / f'bloque_{task}.csv.gz'
    assert not dest.exists()
    T = V3.Task(V3.load_data(), task)
    common, bands = common_rows(T)
    blk = block_placebo(T, bands[R.LAGS[0]][1])
    assert (blk[1][T.lab_pos[common]] == bands[R.LAGS[0]][1][T.lab_pos[common]]).all(), 'fila común sin placebo de bloque'
    preds = []
    for k, test_people in enumerate(R.plan()['folds_main']):
        fit, ev, Za, Zl = R.fold_setup(T, test_people)
        fit, ev = np.intersect1d(fit, common), np.intersect1d(ev, common)
        y, w = T.lab.y.to_numpy()[fit], V3.weights(T.lab.iloc[fit])
        Xf, Xe = (np.column_stack([Zl[r], R.summary(Za, blk[0][T.lab_pos[r]], blk[1][T.lab_pos[r]])]) for r in (fit, ev))
        m = V3.fit_hgb(Xf, y, w, R.plan()['leaves'][task])
        preds.append(T.lab.iloc[ev][['source_row', 'participant', 'y']].assign(prob=m.predict_proba(Xe)[:, 1], strategy='placebo_bloque', fold=k))
        print(task, 'bloque fold', k, flush=True)
    pd.concat(preds).to_csv(dest, index=False)


def strata_table(T):
    """Estrato de cada fila etiquetada, por source_row."""
    a = T.all
    seg = a.groupby(['participant', 'recording', 'segment_id', 'stimulus'], sort=False).ngroup().to_numpy()
    out = pd.DataFrame(dict(source_row=a.source_row.to_numpy(), estimulo=seg,
                            bloque60=(R.session_time(T) // SESSION_BLOCK).astype(int),
                            posicion=R.stimulus_position(T).astype(int)))
    return out.iloc[T.lab_pos].set_index('source_row')


def pair_share(g, col):
    """Fracción de los pares positivo-negativo de la persona que caen dentro de un mismo estrato."""
    total = int(g.y.sum()) * int((1 - g.y).sum())
    within = sum(int(s.y.sum()) * int((1 - s.y).sum()) for _, s in g.groupby(col))
    return within / total if total else np.nan


def report():
    x1, x2, extra = [], [], []
    for task in F.LEAVES:
        T = V3.Task(V3.load_data(), task)
        # ---- X1
        lag = pd.read_csv(R.OUT / f'lag_{task}.csv.gz')
        blk = pd.read_csv(OUT / f'bloque_{task}.csv.gz')
        assert set(blk.source_row) == set(lag[lag.strategy.eq('placebo')].source_row)
        wl = R.person_auc(pd.concat([lag, blk])).pivot(index='participant', columns='strategy', values='auc')
        rows = [dict(task=task, test=f'lag{L} − placebo_bloque', lag=L, **R.contrast(wl, f'lag{L}', 'placebo_bloque')) for L in R.LAGS]
        for r, h in zip(rows, R.holm([r['p'] for r in rows])):
            r['p_holm'] = float(h)
        x1 += rows
        extra.append(dict(task=task, item='placebo_bloque − placebo disperso', **R.contrast(wl, 'placebo_bloque', 'placebo')))
        extra.append(dict(task=task, item='placebo_bloque − c1_common', **R.contrast(wl, 'placebo_bloque', 'c1_common')))
        # ---- X2
        st = strata_table(T)
        rep = pd.concat([pd.read_csv(R.OUT / f'rep_{task}_{s}.csv.gz') for s in R.REP_SEEDS])
        rep = rep[rep.strategy.isin(R.REP_MODELS)].join(st, on='source_row')
        assert rep[STRATA].notna().all().all()
        for col in STRATA:
            vals = rep.groupby(['seed', 'strategy', 'participant']).apply(lambda g: R.stratified_auc(g, col)).rename('auc').reset_index()
            wide = vals.groupby(['participant', 'strategy']).auc.mean().unstack()
            x2.append(dict(task=task, strata=col, test='hgb_c32 − hgb_c1', **R.contrast(wide, 'hgb_c32', 'hgb_c1')))
            extra.append(dict(task=task, item=f'{col}: c32_ts − c1_ts', **R.contrast(wide, 'c32_ts', 'c1_ts')))
            for s in ['hgb_c1', 'hgb_c32']:
                v = wide[s].dropna()
                lo, hi = F.ci(v)
                extra.append(dict(task=task, item=f'{col}: AUC estratificada {s}', delta=float(v.mean()), low95=lo, high95=hi, people=len(v)))
            one = rep[rep.seed.eq(R.REP_SEEDS[0]) & rep.strategy.eq('hgb_c1')]
            share = one.groupby('participant').apply(lambda g: pair_share(g, col))
            extra.append(dict(task=task, item=f'{col}: fracción de pares dentro del estrato', delta=float(share.mean()), people=len(share)))
    x1, x2 = pd.DataFrame(x1), pd.DataFrame(x2)
    x2['p_holm'] = R.holm(x2.p)
    for d in (x1, x2):
        d['decision'] = [F.decide(r.delta, r.low95, r.high95, r.low90, r.high90, r.p_holm) for r in d.itertuples()]
    x1.to_csv(OUT / 'x1_placebo_bloque.csv', index=False)
    x2.to_csv(OUT / 'x2_estratificada.csv', index=False)
    pd.DataFrame(extra).to_csv(OUT / 'descriptivos.csv', index=False)
    pd.set_option('display.width', 250)
    for name, d in [('X1', x1), ('X2', x2), ('DESCRIPTIVOS', pd.DataFrame(extra))]:
        print('\n' + name)
        print(d.round(4).to_string(index=False))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['prepare', 'run', 'report'])
    ap.add_argument('--task', choices=list(F.LEAVES))
    a = ap.parse_args()
    with threadpool_limits(limits=1):
        run(a.task) if a.phase == 'run' else globals()[a.phase]()
