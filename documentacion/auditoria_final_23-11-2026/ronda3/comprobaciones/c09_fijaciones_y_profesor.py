"""Soporte temporal de la etiqueta de atencion: fijaciones cuya duracion completa excede la ventana de 2 s,
y pesos del profesor PCA. Sin modelos."""
from c00_carga import *
import joblib
from reconstruir_profesor_atencion_binaria import COLUMNS, components
from sklearn.metrics import roc_auc_score
d = data()
L = d[d.y_atencion.notna()]
print('fixation_total_ms > 2000 ms (suma de duraciones completas de fijaciones que tocan la ventana):', round(float((L.fixation_total_ms > 2000).mean()), 4),
      '| > 3000:', round(float((L.fixation_total_ms > 3000).mean()), 4), '| p50/p90/p99/max:', L.fixation_total_ms.quantile([.5, .9, .99, 1]).round(0).tolist())
print('fixation_mean_ms > 2000:', round(float((L.fixation_mean_ms > 2000).mean()), 4), '| max', L.fixation_mean_ms.max())
t = joblib.load(V3.TEACHER)
print('PCA profesor: pesos', dict(zip(COLUMNS, np.round(t['pca'].components_[0] * t['sign'], 3))), 'var explicada', round(float(t['pca'].explained_variance_ratio_[0]), 3), '| personas de ajuste', len(t['fit_participants']))
z, _ = components(d)
for c in COLUMNS:
    a = [roc_auc_score(g.y_atencion, z.loc[g.index, c]) for _, g in L.groupby('participant')]
    print(f'   AUC intra-persona de z({c}) orientada contra la etiqueta: {np.mean(a):.3f}')
