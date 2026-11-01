import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np
import pandas as pd
from atencion_binaria import FEATURES, preprocessor, representation
from temporales_core import history_indices

class BinaryAttentionTests(unittest.TestCase):
    def frame(self):
        f=pd.DataFrame({c:np.arange(6,dtype=float)+i for i,c in enumerate(FEATURES)})
        return f.assign(split='train',participant='P2',recording='r',segment_id=1,stimulus='s',
            window_start_utc=pd.date_range('2026-01-01',periods=6,freq='s',tz='UTC'))
    def test_history_never_uses_future(self):
        f=self.frame(); prep=preprocessor().fit(f[FEATURES]); a,x,l=representation(prep,f,'history')
        changed=f.copy(); changed.loc[4:,FEATURES]=9999
        b,v,ll=representation(prep,changed,'history')
        np.testing.assert_array_equal(a[:4],b[:4]); np.testing.assert_array_equal(x[:4],v[:4])
    def test_reset_after_gap_and_segment(self):
        f=self.frame(); f.loc[3:,'window_start_utc']+=pd.Timedelta(seconds=10); f.loc[5:,'segment_id']=2
        ix,lengths=history_indices(f,8)
        np.testing.assert_array_equal(lengths,[1,2,3,1,2,1])
        self.assertEqual(ix[3,0],3)
    def test_teacher_variables_do_not_change_input(self):
        f=self.frame(); prep=preprocessor().fit(f[FEATURES]); a,x,l=representation(prep,f,'history')
        f['pupil_mean_z']=99999; f['attention_label_equal']='alto'; f['fixation_total_ms']=-999
        b,v,ll=representation(prep,f,'history')
        np.testing.assert_array_equal(a,b); np.testing.assert_array_equal(x,v)

if __name__=='__main__': unittest.main()
