"""Particiones, columnas, historial, posicion, placebo. Solo lectura; no ajusta modelos."""
import json, sys
from c00_carga import *
import cierre_final_41p as F, cierre_robustez_41p as RB, ampliacion_41p as A, reapertura_41p as R
from sklearn.metrics import roc_auc_score
d = data()
RES = ROOT / 'resultados'
print('== 1. Particiones')
people = sorted(d.participant.unique())
def check(folds, name):
    flat = sum(folds, [])
    ok = sorted(flat) == people and len(flat) == len(set(flat))
    print(f'  {name}: {len(folds)} grupos, tamaños {[len(f) for f in folds]}, cubre 41 una vez: {ok}')
check(json.loads((RES/'cierre_final_41p_16-11-2026/protocolo.json').read_text())['folds'], 'cierre_final')
assert F.folds(people) == json.loads((RES/'cierre_final_41p_16-11-2026/protocolo.json').read_text())['folds']
print('  folds() regenerado coincide con protocolo')
for s, f in json.loads((RES/'cierre_robustez_41p_16-11-2026/protocolo.json').read_text())['folds_r3'].items(): check(f, 'robustez R3 '+s)
for s, f in json.loads((RES/'reapertura_41p_22-11-2026/protocolo.json').read_text())['folds_rep'].items(): check(f, 'reapertura '+s)
v3 = json.loads((RES/'cierre_v3_16-11-2026/protocolo.json').read_text())['folds']
tr = set(d[d.split.eq('train')].participant)
for f in v3:
    assert set(f['fit']).isdisjoint(f['evaluation']) and set(f['inner_fit']).isdisjoint(f['inner_validation'])
    assert set(f['inner_fit']) | set(f['inner_validation']) <= set(f['fit']) and set(f['fit']) | set(f['evaluation']) == tr, f['fold']
print('  V3: 5 folds de train; interno dentro del ajuste; evaluacion disjunta; union = 25 train')
print('  ¿inner_fit ∪ inner_validation == fit?', [set(f['inner_fit']) | set(f['inner_validation']) == set(f['fit']) for f in v3])

print('== 2. Columnas por tarea')
for task in V3.GROUPS:
    T = V3.Task(d, task)
    bad = {'atencion': ('gaze', 'fix', 'sacc', 'pupil', 'eye'), 'activacion': ('gsr', 'scr', 'eda', 'tonic', 'phasic', 'arousal', 'activation')}[task]
    sus = [c for c in T.cols if any(b in c.lower() for b in bad)]
    pref = sorted({c.split('_')[0] if not c.startswith('eegch') else 'eegchNN' for c in T.cols})
    print(f'  {task}: {len(T.cols)} columnas, prefijos {pref}, sospechosas por nombre: {sus}, duplicadas: {len(T.cols)-len(set(T.cols))}')
    print('     no-EEG:', [c for c in T.cols if not c.startswith('eeg')])
    print('     eegsp/agregadas:', [c for c in T.cols if c.startswith('eegsp') or (c.startswith('eeg_'))])
    print(f'     filas todas {len(T.all)}, etiquetadas {len(T.lab)}, personas {T.lab.participant.nunique()}')
    cls = T.lab.groupby('participant').y.agg(['size', 'mean', 'nunique'])
    print('     personas con una clase:', int((cls['nunique'] < 2).sum()), '| min filas', int(cls['size'].min()), cls['size'].idxmin(), '| prevalencia min/max', round(cls['mean'].min(), 3), round(cls['mean'].max(), 3))
    # historial
    ix, l = T.hist[32]
    a = T.all
    grp = a.groupby(['split', 'participant', 'recording', 'segment_id', 'stimulus'], sort=False).ngroup().to_numpy()
    t = R.seconds(T)
    v = ix >= 0
    rr = np.repeat(np.arange(len(ix))[:, None], 32, 1)
    assert (grp[ix[v]] == grp[rr[v]]).all(), 'historial cruza segmento'
    assert (t[ix[v]] <= t[rr[v]]).all(), 'historial usa futuro'
    assert (ix[np.arange(len(ix)), l - 1] == np.arange(len(ix))).all()
    dt = t[rr[v]] - t[ix[v]]
    print('     historial c32: mismo segmento, sin futuro, ultima = actual; antiguedad max (s):', dt.max())
    # posicion
    wi = d.window_index.to_numpy() if 'window_index' in d else None
    pos = np.minimum(l, 32)
    print('     posicion == min(window_index+1,32) en todas las filas:', bool((pos == np.minimum(wi + 1, 32)).all()))
    seglen = pd.Series(grp).map(pd.Series(grp).value_counts()).to_numpy()
    lp = T.lab_pos
    print('     filas etiquetadas con posicion saturada (>=32):', round(float((l[lp] == 32).mean()), 4), '| con window_index+1 > 32:', round(float((wi[lp] + 1 > 32).mean()), 4),
          '| largo de segmento mediana/max:', int(np.median(seglen[lp])), int(seglen.max()))
    # segmentos repetidos de la misma clave con huecos
    gaps = sum(1 for _, g in pd.Series(t).groupby(grp) if (np.diff(np.sort(g.to_numpy())) > 1.0001).any())
    print('     segmentos con huecos internos:', gaps, 'de', len(np.unique(grp)))
    # historial etiquetado vs completo
    if task == 'activacion':
        lab_hist = l[lp]
        print('     activacion: fraccion de filas etiquetadas con historial<5 (imposible si la etiqueta exige 5 consecutivas):', float((lab_hist < 5).mean()))
    # placebo R1
    px, pl = RB.placebo_hist(T, json.loads((RES/'cierre_robustez_41p_16-11-2026/protocolo.json').read_text())['placebo_seed'])
    v = (px >= 0); v[np.arange(len(px)), pl - 1] = False
    assert (grp[px[v]] != grp[rr[v]]).all() and (a.participant.to_numpy()[px[v]] == a.participant.to_numpy()[rr[v]]).all() and (pl == l).all()
    fut = (t[px[v]] > t[rr[v]]).mean()
    near = (np.abs(t[px[v]] - t[rr[v]]) < 33).mean()
    print(f'     placebo R1: otra seccion, misma persona, mismo largo. Fraccion de ventanas placebo del futuro: {fut:.3f}; a <33 s de la actual: {near:.3f}')
    # E1 lag
    lx, ln = A.lag_index(T)
    v = lx >= 0
    assert (t[rr[v]] - t[lx[v]] >= 5 - 1e-6).all() and (grp[lx[v]] == grp[rr[v]]).all()
    print('     E1 lag real: todas las ventanas a >=5 s antes; filas etiquetadas sin ninguna ventana de lag:', round(float((ln[lp] == 0).mean()), 4))
