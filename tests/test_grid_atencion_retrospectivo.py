import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np,pandas as pd
from grid_atencion_retrospectivo import FEATURES,base_features,features,preprocessor
class RetrospectiveTests(unittest.TestCase):
    def frame(self):
        f=pd.DataFrame(np.tile(np.arange(14,dtype=float)[:,None]+.1,(1,len(FEATURES))),columns=FEATURES)
        return f.assign(participant='A',split='train',recording='r',segment_id=[1]*7+[2]*7,stimulus='s',window_start_utc=pd.date_range('2026-01-01',periods=14,freq='s',tz='UTC'))
    def test_future_summary_has_declared_horizon(self):
        f=self.frame();p=preprocessor().fit(base_features(f,'inductivo'));z=p.transform(base_features(f,'inductivo')).astype('float32')
        a=features(p,f,'inductivo',8,False,4);d=z.shape[1]
        np.testing.assert_allclose(a[0,7*d:8*d],z[:5].mean(axis=0),atol=1e-6)
    def test_future_stops_at_segment_boundary(self):
        f=self.frame();p=preprocessor().fit(base_features(f,'inductivo'));a=features(p,f,'inductivo',8,False,4)
        f.loc[7:,FEATURES]=999;b=features(p,f,'inductivo',8,False,4);np.testing.assert_array_equal(a[:7],b[:7])
    def test_outside_horizon_cannot_change_early_window(self):
        f=self.frame();p=preprocessor().fit(base_features(f,'inductivo'));a=features(p,f,'inductivo',8,False,4)
        f.loc[5:6,FEATURES]=999;b=features(p,f,'inductivo',8,False,4);np.testing.assert_array_equal(a[0],b[0])
if __name__=='__main__':unittest.main()
