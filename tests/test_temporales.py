import sys
import tempfile
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
import torch

sys.path.insert(0,str(Path(__file__).parents[1]/'scripts'))
from temporales_core import history_indices, sequence_array, TemporalNet, CausalBlock, seed_all, raw_predict, digest, load_net, preprocessor


class TestTemporales(unittest.TestCase):
    def frame(self):
        return pd.DataFrame({'split':['train']*7,'participant':['P1']*5+['P2']*2,
            'recording':['R']*7,'segment_id':[1,1,1,1,2,1,1],'stimulus':['Text']*7,
            'window_start_utc':['2026-09-07T10:00:00Z','2026-09-07T10:00:01Z','2026-09-07T10:00:02Z',
                                '2026-09-07T10:00:04Z','2026-09-07T10:00:05Z','2026-09-07T10:00:00Z','2026-09-07T10:00:01Z']})

    def test_history_is_past_only_and_resets_at_gaps_and_people(self):
        ix,ll=history_indices(self.frame(),3)
        np.testing.assert_array_equal(ll,[1,2,3,1,1,1,2])
        np.testing.assert_array_equal(ix[2],[0,1,2])
        np.testing.assert_array_equal(ix[3],[3,-1,-1])
        self.assertTrue(np.all(ix <= np.arange(7)[:,None]))
        xx=sequence_array(np.arange(7)[:,None],ix)
        self.assertEqual(xx[3,1,0],0)
        np.testing.assert_array_equal(xx[2,:,0],[0,1,2])

    def test_unsorted_and_duplicate_sequences_fail(self):
        f=self.frame()
        f.loc[1,'window_start_utc']=f.loc[0,'window_start_utc']
        with self.assertRaises(ValueError): history_indices(f)
        with self.assertRaises(ValueError): history_indices(self.frame().iloc[[2,1,0]].reset_index(drop=True))

    def test_padding_does_not_change_any_network_prediction(self):
        seed_all(7)
        x=np.random.default_rng(7).normal(size=(3,8,4)).astype('float32')
        ll=np.array([1,3,8])
        altered=x.copy()
        for i,n in enumerate(ll): altered[i,n:]=999
        for name in ['TCN','LSTM','BiLSTM','MLP_current']:
            net=TemporalNet(name,4,3)
            np.testing.assert_allclose(raw_predict(net,x,ll),raw_predict(net,altered,ll),atol=1e-7)

    def test_tcn_cannot_read_future_positions(self):
        seed_all(8)
        block=CausalBlock(3,5,2,0).eval()
        x=torch.randn(2,3,12)
        altered=x.clone(); altered[:,:,7:]=100
        torch.testing.assert_close(block(x)[:,:,:7],block(altered)[:,:,:7])

    def test_bilstm_reads_history_but_mlp_only_endpoint(self):
        seed_all(9)
        x=np.zeros((2,8,3),dtype='float32'); ll=np.array([8,8])
        x[1,:7]=2
        bi=raw_predict(TemporalNet('BiLSTM',3,1),x,ll)
        self.assertGreater(abs(float(bi[0,0]-bi[1,0])),1e-5)
        mlp=raw_predict(TemporalNet('MLP_current',3,1),x,ll)
        np.testing.assert_array_equal(mlp[0],mlp[1])

    def test_all_architectures_weights_reload_exactly(self):
        seed_all(10)
        x=np.ones((4,8,3),dtype='float32'); ll=np.array([1,2,4,8])
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            for architecture in ['TCN','LSTM','BiLSTM','MLP_current']:
                model=TemporalNet(architecture,3,3)
                path=root/(architecture+'.pt'); torch.save(model.state_dict(),path)
                meta=dict(architecture=architecture,inputs=3,outputs=3,hidden=24,dropout=.2,
                          path=path.name,sha256=digest(path))
                np.testing.assert_array_equal(raw_predict(model,x,ll),raw_predict(load_net(meta,root),x,ll))

    def test_preprocessing_uses_training_values_only(self):
        train=pd.DataFrame({'x':[0.,1.,2.,np.nan]})
        prep=preprocessor().fit(train)
        before=prep['imputer'].statistics_.copy()
        prep.transform(pd.DataFrame({'x':[1e9,np.nan]}))
        np.testing.assert_array_equal(before,prep['imputer'].statistics_)
        self.assertEqual(before[0],1.)

    def test_differential_importance_equals_loss_of_baseline_advantage(self):
        from evaluar_temporales import difference
        frame=pd.DataFrame({'participant':['P1']*3+['P2']*3,'target':[1.,2.,3.,1.,2.,3.]})
        temporal=np.array([1.,2.,2.,1.,2.,2.]);baseline=np.array([0.,1.,2.,0.,1.,2.])
        changed_temporal=np.zeros(6);changed_baseline=np.ones(6)
        before=difference(frame,'target',temporal,baseline,'regression')
        after=difference(frame,'target',changed_temporal,changed_baseline,'regression')
        temporal_drop=difference(frame,'target',temporal,changed_temporal,'regression')
        baseline_drop=difference(frame,'target',baseline,changed_baseline,'regression')
        np.testing.assert_allclose(before-after,temporal_drop-baseline_drop)


if __name__=='__main__': unittest.main()
