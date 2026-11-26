"""AUC intra-persona de cada columna de entrada por separado contra la etiqueta (sin ajustar modelos).
Sirve para detectar columnas que arrastran la etiqueta (p. ej. conteos de filas de otro sensor)."""
from c00_carga import *
from sklearn.metrics import roc_auc_score
from scipy.stats import spearmanr
d = data()
for task in V3.GROUPS:
    T = V3.Task(d, task)
    lab = T.lab
    rows = []
    for c in T.cols:
        a = []
        for _, g in lab.groupby('participant'):
            x = g[c]
            ok = x.notna()
            if ok.sum() > 20 and g.y[ok].nunique() == 2 and x[ok].nunique() > 1:
                a.append(roc_auc_score(g.y[ok], x[ok]))
        miss = lab[c].isna()
        # indicador de faltante como predictor
        am = [roc_auc_score(g.y, g[c].isna().astype(int)) for _, g in lab.groupby('participant') if 0 < g[c].isna().mean() < 1]
        rows.append(dict(col=c, auc=np.mean(a) if a else np.nan, dev=abs(np.mean(a) - .5) if a else np.nan, cons=np.mean(np.array(a) > .5) if a else np.nan,
                         n=len(a), miss=float(miss.mean()), auc_miss=np.mean(am) if am else np.nan, n_miss=len(am)))
    r = pd.DataFrame(rows).sort_values('dev', ascending=False)
    print('==', task, '(AUC media por persona de la columna sola; cons = fraccion de personas con AUC>0,5)')
    print(r.head(14).round(3).to_string(index=False))
    print('   no-EEG:'); print(r[~r.col.str.startswith('eeg')].round(3).to_string(index=False))
    print('   calidad EEG (eegsp_*, finite/rail/flat/usable): max |AUC-0,5| =', round(r[r.col.str.contains('eegsp_n|eegsp_cov|eegsp_max|eegsp_usable|finite_fraction|rail_fraction|flat_fraction|_usable')].dev.max(), 3))
    print('   indicadores de faltante con mayor |AUC-0,5|:'); print(r.assign(dm=(r.auc_miss - .5).abs()).sort_values('dm', ascending=False).head(5)[['col', 'miss', 'auc_miss', 'n_miss']].round(3).to_string(index=False))
# pupil_both_valid_fraction frente a conteo de filas GSR
print('== pupil_both_valid_fraction')
x = d[['participant', 'pupil_both_valid_fraction', 'gsr_n', 'pupil_n', 'gaze_n', 'gsr_coverage', 'y_activacion', 'gsr_tonic_mean_z', 'gsr_mean_z']]
print(x[['pupil_both_valid_fraction', 'gsr_n', 'pupil_n', 'gaze_n']].describe().round(3).to_string())
rho = x.groupby('participant').apply(lambda g: pd.Series({k: spearmanr(g.pupil_both_valid_fraction, g[k], nan_policy='omit').statistic for k in ['gsr_n', 'pupil_n', 'gaze_n', 'gsr_mean_z']}))
print('Spearman intra-persona (media) de pupil_both_valid_fraction con:', rho.mean().round(3).to_dict())
l = x.dropna(subset=['y_activacion'])
for k in ['gsr_n', 'pupil_n', 'gaze_n', 'pupil_both_valid_fraction']:
    a = [roc_auc_score(g.y_activacion, g[k]) for _, g in l.groupby('participant') if g[k].nunique() > 1 and g[k].notna().all()]
    print(f'  AUC intra-persona de {k} contra activacion: {np.mean(a):.3f} (n={len(a)}, >0,5 en {np.mean(np.array(a)>.5):.2f})')
