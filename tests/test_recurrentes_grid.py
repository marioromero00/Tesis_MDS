import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np
import pandas as pd
import torch
from recurrentes_grid_core import grid,GridSequenceNet,train,predict,FAMILIES
from hiperparametros_core import FULL,TARGET


class TestRecurrentesGrid(unittest.TestCase):
    def test_grids_and_padding_exclusion(self):
        torch.set_num_threads(2)
        for family in FAMILIES:
            configs=grid(family); self.assertEqual(len(configs),32)
            self.assertEqual(len({tuple(c[k] for k in ['context','hidden','layers','lr','dropout']) for c in configs}),32)
            for c in [configs[0],configs[-1]]:
                net=GridSequenceNet(5,c).eval(); x=torch.randn(2,c['context'],5); lengths=torch.tensor([2,4])
                changed=x.clone(); changed[0,2:]=999; changed[1,4:]=-999
                with torch.no_grad(): np.testing.assert_allclose(net(x,lengths),net(changed,lengths),atol=1e-6)

    def test_checkpoints_and_future_rows_cannot_change_endpoint(self):
        rng=np.random.default_rng(5)
        frame=pd.DataFrame(rng.normal(size=(18,len(FULL))),columns=FULL)
        frame['participant']='p'; frame['recording']='r'
        frame['window_start_utc']=pd.date_range('2020-01-01',periods=18,freq='s',tz='UTC')
        frame[TARGET]=['bajo','medio','alto']*6
        for family in FAMILIES:
            a,_=train(frame,grid(family)[0],7,2)
            def checkpoint(epoch,b,curve):
                predict(b,frame); torch.rand(10)
            b,_=train(frame,grid(family)[0],7,2,checkpoint)
            for k in a['state']: self.assertTrue(torch.equal(a['state'][k],b['state'][k]),(family,k))
            full=predict(a,frame); prefix=predict(a,frame.iloc[:7])
            np.testing.assert_allclose(full[:7],prefix,atol=1e-6,rtol=0)


if __name__=='__main__': unittest.main()
