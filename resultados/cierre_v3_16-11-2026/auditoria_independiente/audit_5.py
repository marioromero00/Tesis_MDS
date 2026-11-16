import sys, json
sys.path.insert(0, '/Users/mario/Proyectos/tesis-mds/repos/Tesis_MDS/scripts')
import numpy as np, pandas as pd, joblib, torch
from threadpoolctl import threadpool_limits
import cierre_experimental_v3 as C
torch.set_num_threads(4)
OUT = C.OUT
with threadpool_limits(limits=4):
    data = C.load_data()
    for task in ['atencion', 'activacion']:
        T = C.Task(data, task)
        ext = pd.read_csv(OUT/f'externas_{task}.csv.gz')
        train_people = sorted(T.lab[T.lab.split.eq('train')].participant.unique())
        fit = T.rows(train_people)
        prep = C.preprocessor().fit(T.lab.iloc[fit][T.cols])
        Za = prep.transform(T.all[T.cols]).astype('float32'); Zl = prep.transform(T.lab[T.cols]).astype('float32')
        ev = np.flatnonzero(T.lab.split.isin(['validation','test']).to_numpy())
        sr = T.lab.source_row.to_numpy()[ev]
        def ref(strat):
            s = ext[ext.strategy==strat].set_index('source_row').prob
            return s.loc[sr].to_numpy()
        tmask = T.lab.split.to_numpy()[ev]=='test'
        # y consistency
        ys = ext[ext.strategy=='hgb_c1'].set_index('source_row').y.loc[sr].to_numpy()
        print(task, 'y ext == T.lab y', (ys==T.lab.y.to_numpy()[ev]).all(), 'n ev', len(ev), 'n test', tmask.sum(), 'cols', len(T.cols))
        m = joblib.load(OUT/'modelos'/task/'hgb_c32.joblib')
        p = m.predict_proba(C.hgb_matrix(T, Za, Zl, ev, 32))[:, 1]
        r = ref('hgb_c32'); print(task, 'hgb_c32 cargado: maxdiff test', np.abs(p-r)[tmask].max(), 'val', np.abs(p-r)[~tmask].max(), 'leaves', m.max_leaf_nodes)
        # re-entrenamiento propio HGB c32
        leaves = json.loads((OUT/f'congelacion_{task}.json').read_text())['leaves']
        w = C.weights(T.lab.iloc[fit]); y = T.lab.y.to_numpy()[fit]
        m2 = C.fit_hgb(C.hgb_matrix(T, Za, Zl, fit, 32), y, w, leaves)
        p2 = m2.predict_proba(C.hgb_matrix(T, Za, Zl, ev, 32))[:, 1]
        print(task, 'hgb_c32 reentrenado: maxdiff test', np.abs(p2-r)[tmask].max())
        xe, le = C.sequences(T, Za, ev, 32)
        ps = []
        for s in [1,2,3]:
            net = C.Net(xe.shape[2]); net.load_state_dict(torch.load(OUT/'modelos'/task/f'gru_c32_s{s}.pt'))
            ps.append(C.predict_gru(net, xe, le))
        r = ref('gru_c32'); pm = np.mean(ps, axis=0)
        print(task, 'gru_c32 3 semillas cargadas: maxdiff test', np.abs(pm-r)[tmask].max(), 'val', np.abs(pm-r)[~tmask].max())
        xf, lf = C.sequences(T, Za, fit, 32)
        net = C.fit_gru(xf, lf, y, w, 1); p1 = C.predict_gru(net, xe, le)
        print(task, 'gru_c32 s1 reentrenado vs s1 cargado: maxdiff test', np.abs(p1-ps[0])[tmask].max())
        # busqueda interna fold 1 recalculada
        fold = C.plan()['folds'][0]; inner, iv = T.rows(fold['inner_fit']), T.rows(fold['inner_validation'])
        assert set(T.lab.iloc[np.r_[inner, iv]].split) == {'train'}
        pi = C.preprocessor().fit(T.lab.iloc[inner][T.cols]); A = pi.transform(T.all[T.cols]).astype('float32'); L = pi.transform(T.lab[T.cols]).astype('float32')
        b = pd.read_csv(OUT/f'busqueda_interna_{task}.csv'); b = b[b.fold==1]
        d = []
        for c in [1, 8, 32]:
            for lv in C.LEAVES:
                mm = C.fit_hgb(C.hgb_matrix(T, A, L, inner, c), T.lab.y.to_numpy()[inner], C.weights(T.lab.iloc[inner]), lv)
                a = C.macro_auc(T.lab.iloc[iv], mm.predict_proba(C.hgb_matrix(T, A, L, iv, c))[:, 1])
                d.append(abs(a - b[(b.context==c)&(b.leaves==lv)].auc.iloc[0]))
        print(task, 'busqueda fold1 recalculada maxdiff', max(d), flush=True)
