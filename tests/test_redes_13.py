import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np
import pandas as pd
import torch
from redes_secuencia_13 import SequenceNet, grid, sequences
from temporales_core import preprocessor
from hiperparametros_core import FULL


class TestRedes13(unittest.TestCase):
    def test_padding_and_future_do_not_change_endpoint(self):
        torch.manual_seed(1)
        for c in grid():
            net=SequenceNet(5,c).eval()
            x=torch.randn(2,c['context'],5); lengths=torch.tensor([3,5])
            changed=x.clone(); changed[0,3:]=100; changed[1,5:]=-100
            with torch.no_grad():
                np.testing.assert_allclose(net(x,lengths),net(changed,lengths),atol=1e-6)

    def test_sequence_boundary_repeat_and_teacher_exclusion(self):
        frame=pd.DataFrame({c:np.arange(6,dtype=float) for c in FULL})
        frame['participant']=['a']*4+['b']*2; frame['recording']='r'
        frame['window_start_utc']=pd.to_datetime(['2020-01-01 00:00:0'+str(i) for i in [0,1,4,5,0,1]],utc=True)
        prep=preprocessor().fit(frame[FULL]); c=grid()[0]
        x,l=sequences(prep,frame,c)
        np.testing.assert_array_equal(l,[1,2,1,2,1,2])
        changed=frame.copy(); changed.loc[3,FULL]=999; changed['arousal_label_6s']='alto'; changed['gsr_mean']=999
        xx,_=sequences(prep,changed,c)
        np.testing.assert_array_equal(x[:3],xx[:3])
        repeated,_=sequences(prep,frame,c,True)
        np.testing.assert_array_equal(repeated[1,0],repeated[1,1])


if __name__=='__main__': unittest.main()
