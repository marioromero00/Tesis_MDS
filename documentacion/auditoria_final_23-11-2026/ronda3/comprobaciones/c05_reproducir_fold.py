"""Diagnostico de un solo fold (fold 0 del analisis final): reentrena hgb_c1 y hgb_c32 con el codigo del
repositorio y compara con las predicciones guardadas. No escribe en resultados/."""
import json, time
from c00_carga import *
import torch
import cierre_final_41p as F, cierre_robustez_41p as RB, explicativo_posicion_41p as X
from threadpoolctl import threadpool_limits
d = data()
p = F.plan()
with threadpool_limits(limits=3):
    torch.set_num_threads(3)
    for task in ['activacion', 'atencion']:
        t0 = time.time()
        T = V3.Task(d, task)
        saved = pd.read_csv(F.OUT / f'predicciones_{task}.csv.gz')
        test_people = p['folds'][0]
        fit = np.flatnonzero(~T.lab.participant.isin(test_people).to_numpy()); ev = np.flatnonzero(T.lab.participant.isin(test_people).to_numpy())
        prep = V3.preprocessor().fit(T.lab.iloc[fit][T.cols])
        Za = prep.transform(T.all[T.cols]).astype('float32'); Zl = prep.transform(T.lab[T.cols]).astype('float32')
        y, w = T.lab.y.to_numpy()[fit], V3.weights(T.lab.iloc[fit])
        wsum = pd.Series(w).groupby(T.lab.participant.to_numpy()[fit]).sum()
        print(task, 'pesos: suma por persona min/max', round(wsum.min(), 4), round(wsum.max(), 4), '| suma por clase', pd.Series(w).groupby(y).sum().round(2).to_dict())
        for name, kind in [('hgb_c1', 1), ('hgb_c32', 32)]:
            m = V3.fit_hgb(V3.hgb_matrix(T, Za, Zl, fit, kind), y, w, p['leaves'][task])
            pr = m.predict_proba(V3.hgb_matrix(T, Za, Zl, ev, kind))[:, 1]
            s = saved[(saved.strategy == name) & (saved.fold == 0)]
            assert (s.source_row.to_numpy() == T.lab.source_row.to_numpy()[ev]).all() and (s.y.to_numpy() == T.lab.y.to_numpy()[ev]).all()
            print(f'  {task} {name}: filas {len(pr)}, max |dif prob| = {np.abs(pr - s.prob.to_numpy()).max():.2e}, columnas {V3.hgb_matrix(T, Za, Zl, ev, kind).shape[1]}')
        if task == 'activacion':
            xf, lf = V3.sequences(T, Za, fit, 1); xe, le = V3.sequences(T, Za, ev, 1)
            pr = np.mean([V3.predict_gru(V3.fit_gru(xf, lf, y, w, s_), xe, le) for s_ in V3.GRU['seeds']], axis=0)
            s = saved[(saved.strategy == 'gru_c1') & (saved.fold == 0)]
            print(f'  {task} gru_c1: max |dif prob| = {np.abs(pr - s.prob.to_numpy()).max():.2e}')
        print('  segundos', round(time.time() - t0, 1))
