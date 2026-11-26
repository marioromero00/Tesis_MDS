"""Seleccion de hojas en V3 (busqueda interna) y contrastes de activacion/atencion separados entre las 25
personas con las que se eligio la configuracion y las 16 restantes. Solo usa predicciones guardadas."""
import json
from c00_carga import *
from sklearn.metrics import roc_auc_score
import cierre_final_41p as F
RES = ROOT / 'resultados'
d = data()
split = d.groupby('participant').split.first()
for task in ['activacion', 'atencion']:
    b = pd.read_csv(RES/f'cierre_v3_16-11-2026/busqueda_interna_{task}.csv')
    print('==', task, 'busqueda interna V3 (AUC en validacion interna)')
    print(b.pivot_table(index='fold', columns=['context', 'leaves'], values='auc').round(3).to_string())
    w = b.pivot_table(index='fold', columns=['leaves', 'context'], values='auc')
    print('   c32 − c1 con 7 hojas por fold:', (w[7][32] - w[7][1]).round(3).tolist(), 'media', round((w[7][32] - w[7][1]).mean(), 4))
    print('   c32 − c1 con 15 hojas por fold:', (w[15][32] - w[15][1]).round(3).tolist(), 'media', round((w[15][32] - w[15][1]).mean(), 4))
    fo = json.loads((RES/'cierre_v3_16-11-2026/protocolo.json').read_text())['folds']
    print('   personas en validacion interna por fold:', [len(f['inner_validation']) for f in fo])
def wide(pred, seed=False):
    keys = (['seed'] if seed else []) + ['strategy', 'participant']
    r = pd.DataFrame([dict(zip(keys, k), auc=roc_auc_score(g.y, g.prob)) for k, g in pred.groupby(keys)])
    return r.groupby(['participant', 'strategy']).auc.mean().unstack()
def show(name, w, a, b):
    dd = (w[a] - w[b]).dropna()
    out = []
    for lab, m in [('41', dd.index == dd.index), ('25 train', split.reindex(dd.index).eq('train').to_numpy()), ('16 val+test', ~split.reindex(dd.index).eq('train').to_numpy())]:
        v = dd[m].to_numpy(); lo, hi = F.ci(v)
        out.append(f'{lab}: {v.mean():+.4f} [{lo:+.4f}; {hi:+.4f}] {int((v > 0).sum())}/{len(v)}')
    print(f'  {name}: ' + ' | '.join(out))
for task in ['activacion', 'atencion']:
    print('==', task, 'contrastes por grupo de personas')
    main = pd.read_csv(RES/f'cierre_final_41p_16-11-2026/predicciones_{task}.csv.gz')
    w = wide(pd.concat([main, pd.read_csv(RES/f'cierre_robustez_41p_16-11-2026/r1_{task}.csv.gz'), pd.read_csv(RES/f'ampliacion_41p_16-11-2026/enmienda_e1_lag6/predicciones_{task}.csv.gz'),
                        pd.read_csv(RES/f'explicativo_posicion_41p_18-11-2026/predicciones_{task}.csv.gz')]))
    show('16-11 principal hgb_c32 − hgb_c1', w, 'hgb_c32', 'hgb_c1')
    show('16-11 gru_c32 − gru_c1', w, 'gru_c32', 'gru_c1')
    show('R1 real − placebo', w, 'hgb_c32', 'placebo_c32')
    show('E1 lag6 real − placebo', w, 'lag6_real', 'lag6_placebo')
    show('18-11 hgb_c32 − pos_c1', w, 'hgb_c32', 'pos_c1')
    rep = pd.concat([pd.read_csv(RES/f'reapertura_41p_22-11-2026/rep_{task}_{s}.csv.gz') for s in [1101, 1102, 1103, 1104, 1105]])
    pos = pd.concat([pd.read_csv(RES/f'reapertura_fase3_41p_22-11-2026/pos_{task}_{s}.csv.gz') for s in [1101, 1102, 1103, 1104, 1105]])
    w = wide(pd.concat([rep, pos]), seed=True)
    show('22-11 P1 hgb_c32 − hgb_c1 (5 particiones)', w, 'hgb_c32', 'hgb_c1')
    show('22-11 P2 c32_ts − c1_ts', w, 'c32_ts', 'c1_ts')
    show('22-11 Q1 c32_pos − pos_c1', w, 'c32_pos', 'pos_c1')
    lag = pd.read_csv(RES/f'reapertura_41p_22-11-2026/lag_{task}.csv.gz')
    lag = lag[lag.groupby(['strategy', 'participant']).y.transform('nunique').eq(2)]
    show('22-11 lag6 − placebo', wide(lag), 'lag6', 'placebo')
    show('AUC hgb_c1 − 0,5', w.assign(azar=.5), 'hgb_c1', 'azar')
