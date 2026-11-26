"""D2 (autocorrelacion de la etiqueta) recalculada de forma independiente, y comparacion con el GSR
continuo desplazado, dentro del mismo segmento y entre segmentos. Sin modelos."""
from c00_carga import *
from sklearn.metrics import roc_auc_score
d = data()
d = d.assign(t=pd.to_datetime(d.window_start_utc, utc=True).dt.as_unit('ns').astype('int64') / 1e9)
SEG = ['participant', 'recording', 'segment_id', 'stimulus']
def pauc(f, y, x):
    return np.mean([roc_auc_score(g[y], g[x]) for _, g in f.groupby('participant') if g[y].nunique() == 2 and g[x].nunique() > 1]), f.participant.nunique()
for task, ycol in [('activacion', 'y_activacion'), ('atencion', 'y_atencion')]:
    print('==', task)
    for k in [1, 2, 4, 6, 12, 24]:
        a = d[SEG + ['window_index', ycol, 'gsr_mean_z', 'gsr_tonic_mean_z']]
        b = a.rename(columns={ycol: 'y_prev', 'gsr_mean_z': 'g_prev', 'gsr_tonic_mean_z': 'ton_prev'}).assign(window_index=lambda f: f.window_index + k)
        m = a.merge(b, on=SEG + ['window_index']).dropna(subset=[ycol])
        mm = m.dropna(subset=['y_prev'])
        r1 = pauc(mm, ycol, 'y_prev'); agree = (mm[ycol] == mm.y_prev).mean()
        line = f'  k={k:>2} s mismo segmento: AUC etiqueta previa {r1[0]:.3f} (pares {len(mm)}, personas {r1[1]}), acuerdo {agree:.3f}'
        if task == 'activacion':
            line += f' | AUC gsr_mean_z previo {pauc(m.dropna(subset=["g_prev"]), ycol, "g_prev")[0]:.3f}'
            # AUC estratificada por segmento del GSR previo (solo pares dentro del mismo segmento)
        print(line)
