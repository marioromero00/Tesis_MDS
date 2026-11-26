"""Soporte temporal real de la etiqueta de activacion: nucleo del filtro tonico (Butterworth 2, 0,05 Hz,
filtfilt, 15 Hz) combinado con la ventana de 2 s y el promedio de 5 ventanas. Sin modelos."""
from c00_carga import *
from scipy.signal import butter, filtfilt
hz, fc = 15., .05
b, a = butter(2, fc / (hz / 2), btype='low')
n = int(600 * hz); imp = np.zeros(2 * n + 1); imp[n] = 1
k = filtfilt(b, a, imp)                      # nucleo de fase cero (respuesta a un impulso en t=0)
tt = (np.arange(2 * n + 1) - n) / hz
print('nucleo tonico filtfilt: masa |k| fuera de ±s ->', {s: round(float(np.abs(k[np.abs(tt) > s]).sum() / np.abs(k).sum()), 3) for s in [2, 3, 5, 8, 10, 15, 20, 30]})
# peso de la muestra GSR en el instante u sobre el promedio tonico del soporte nominal [t-4, t+2) (t=0)
box = ((tt >= -4) & (tt < 2)).astype(float); box /= box.sum()
w = np.convolve(box, k, 'same')
tot = np.abs(w).sum()
print('peso tonico de la etiqueta (soporte nominal [-4,+2) s):')
for lo, hi, name in [(-1e9, -4, 'antes de t-4 (zona del historial desplazado 6 s / banda 6 s)'), (-4, 2, 'dentro de los 6 s nominales'), (2, 1e9, 'despues de t+2 (futuro)'),
                     (-1e9, -10, 'antes de t-10'), (-1e9, -16, 'antes de t-16 (banda 12 s)'), (8, 1e9, 'despues de t+8')]:
    m = (tt >= lo) & (tt < hi)
    print(f'   {name}: {np.abs(w[m]).sum() / tot:.3f}')
# composicion empirica de la etiqueta
d = data()
lab = pd.read_csv(V3.LABELS_ACT)[['source_row', 'score2s_quality', 'score6s_quality', 'activation_binary_v2', 'gsr_quality_valid']]
m = d.merge(lab, on='source_row')
from sklearn.metrics import roc_auc_score
L = m[m.y_activacion.notna()]
comp = ['gsr_tonic_mean_z', 'gsr_phasic_mean_z', 'gsr_scr_count', 'gsr_scr_mean_prominence_z', 'gsr_mean_z']
print('AUC intra-persona de cada componente GSR de la MISMA ventana contra la etiqueta (cuanto pesa cada uno):')
for c in comp:
    a_ = [roc_auc_score(g.y_activacion, g[c]) for _, g in L.groupby('participant') if g[c].nunique() > 1]
    print(f'   {c}: {np.mean(a_):.3f}')
# la etiqueta predicha por el tonico de ventanas lejanas del MISMO registro (pasado y futuro), sin restringir a segmento
m = m.sort_values(['participant', 'recording', 'window_start_utc']).reset_index(drop=True)
t = pd.to_datetime(m.window_start_utc, utc=True).dt.as_unit('ns').astype('int64').to_numpy() / 1e9
key = m.participant.astype(str) + '|' + m.recording.astype(str)
print('AUC intra-persona de gsr_tonic_mean_z desplazado k s (misma grabacion) contra la etiqueta en t; y de gsr_mean_z:')
m['t'] = t; m['key'] = key.to_numpy()
for kshift in [-30, -20, -12, -8, -6, 0, 4, 8, 12, 20, 30]:
    left = m[m.y_activacion.notna()][['key', 'participant', 't', 'y_activacion']].assign(ts=lambda f: f.t + kshift).sort_values('ts')
    right = m[['key', 't', 'gsr_tonic_mean_z', 'gsr_mean_z', 'pupil_mean_z']].rename(columns={'t': 'ts'}).sort_values('ts')
    f = pd.merge_asof(left, right, on='ts', by='key', tolerance=.5, direction='nearest')
    res = {}
    for c in ['gsr_tonic_mean_z', 'gsr_mean_z', 'pupil_mean_z']:
        h = f.dropna(subset=[c])
        res[c] = np.mean([roc_auc_score(g.y_activacion, g[c]) for _, g in h.groupby('participant') if g.y_activacion.nunique() == 2 and len(g) > 20])
    print(f'   k={kshift:+d} s: tonico {res["gsr_tonic_mean_z"]:.3f} | gsr_mean {res["gsr_mean_z"]:.3f} | pupil_mean_z {res["pupil_mean_z"]:.3f} | filas {int(f.gsr_mean_z.notna().sum())}')
