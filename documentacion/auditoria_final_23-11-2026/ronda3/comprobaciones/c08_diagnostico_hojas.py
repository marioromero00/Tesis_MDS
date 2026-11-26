"""Diagnostico de UN fold (fold 0 del analisis final, activacion): sensibilidad del contraste hgb_c32 − hgb_c1
al numero de hojas (7 frente a 15, el congelado). No es un resultado: 6 personas. No escribe en resultados/."""
from c00_carga import *
import cierre_final_41p as F
from sklearn.metrics import roc_auc_score
from threadpoolctl import threadpool_limits
d = data(); p = F.plan()
with threadpool_limits(limits=3):
    T = V3.Task(d, 'activacion')
    te = p['folds'][0]
    fit = np.flatnonzero(~T.lab.participant.isin(te).to_numpy()); ev = np.flatnonzero(T.lab.participant.isin(te).to_numpy())
    prep = V3.preprocessor().fit(T.lab.iloc[fit][T.cols])
    Za = prep.transform(T.all[T.cols]).astype('float32'); Zl = prep.transform(T.lab[T.cols]).astype('float32')
    y, w = T.lab.y.to_numpy()[fit], V3.weights(T.lab.iloc[fit])
    e = T.lab.iloc[ev]
    for leaves in [7, 15]:
        auc = {}
        for name, kind in [('c1', 1), ('c32', 32)]:
            pr = V3.fit_hgb(V3.hgb_matrix(T, Za, Zl, fit, kind), y, w, leaves).predict_proba(V3.hgb_matrix(T, Za, Zl, ev, kind))[:, 1]
            auc[name] = pd.Series({q: roc_auc_score(e.y.to_numpy()[ix], pr[ix]) for q, ix in e.groupby('participant').indices.items()})
        dd = auc['c32'] - auc['c1']
        print(f'hojas {leaves}: AUC c1 {auc["c1"].mean():.4f}, c32 {auc["c32"].mean():.4f}, c32 − c1 = {dd.mean():+.4f}; por persona {dd.round(3).to_dict()}')
