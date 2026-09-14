import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np
import pandas as pd
import torch
from transformer_grid_core import grid,GridTransformer,train,predict
from hiperparametros_core import FULL,TARGET


class TestTransformerGrid(unittest.TestCase):
    def test_cartesian_grid_and_independent_layers(self):
        configs=grid(); self.assertEqual(len(configs),32)
        self.assertEqual(len({tuple(c[k] for k in ['context','hidden','layers','lr','dropout']) for c in configs}),32)
        c=next(c for c in configs if c['layers']==2)
        net=GridTransformer(5,c)
        self.assertFalse(torch.equal(net.layers[0].linear1.weight,net.layers[1].linear1.weight))

    def test_future_padding_invariance(self):
        torch.set_num_threads(2)
        for c in [grid()[0],grid()[-1]]:
            net=GridTransformer(5,c).eval(); x=torch.randn(2,c['context'],5); lengths=torch.tensor([2,4])
            z=x.clone(); z[0,2:]=999; z[1,4:]=-999
            with torch.no_grad(): np.testing.assert_allclose(net(x,lengths),net(z,lengths),atol=1e-6)

    def test_checkpoints_do_not_change_training_rng(self):
        rng=np.random.default_rng(5)
        frame=pd.DataFrame(rng.normal(size=(18,len(FULL))),columns=FULL)
        frame['participant']='p'; frame['recording']='r'
        frame['window_start_utc']=pd.date_range('2020-01-01',periods=18,freq='s',tz='UTC')
        frame[TARGET]=['bajo','medio','alto']*6
        a,_=train(frame,grid()[0],7,2)
        def checkpoint(epoch,b,curve):
            before=torch.get_rng_state().clone(); predict(b,frame)
            self.assertTrue(torch.equal(before,torch.get_rng_state()))
            torch.rand(10)  # Even an RNG-using callback is isolated by train.
        b,_=train(frame,grid()[0],7,2,checkpoint)
        for k in a['state']: self.assertTrue(torch.equal(a['state'][k],b['state'][k]),k)


if __name__=='__main__': unittest.main()
