import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np,pandas as pd
from grid_atencion_meta07 import FEATURES,base_features,features,preprocessor,candidates,choose
class GridTests(unittest.TestCase):
    def frame(self):
        rng=np.random.default_rng(9)
        f=pd.DataFrame(rng.uniform(.1,2,(24,len(FEATURES))),columns=FEATURES)
        return f.assign(participant=np.repeat(['A','B'],12),split='train',recording='r',segment_id=1,stimulus='s',window_start_utc=list(pd.date_range('2026-01-01',periods=12,freq='s',tz='UTC'))*2)
    def test_inductive_history_causal(self):
        f=self.frame();p=preprocessor().fit(base_features(f,'inductivo'));a=features(p,f,'inductivo',128)
        f.loc[8:11,FEATURES]=9999;b=features(p,f,'inductivo',128)
        np.testing.assert_array_equal(a[:8],b[:8])
    def test_offline_calibration_persons_isolated(self):
        f=self.frame();a=base_features(f,'relativo_offline');f.loc[f.participant.eq('B'),FEATURES]=99
        b=base_features(f,'relativo_offline');np.testing.assert_array_equal(a.iloc[:12],b.iloc[:12])
    def test_teacher_features_excluded(self):
        f=self.frame();a=base_features(f,'inductivo');f['pupil_mean_z']=99;f['attention_binary']=1;f['teacher_score']=-999
        pd.testing.assert_frame_equal(a,base_features(f,'inductivo'))
    def test_grids_and_inner_selection(self):
        self.assertEqual(len(candidates(1)),32);self.assertEqual(len(candidates(2)),32);self.assertEqual(len(candidates(3)),48)
        t=[dict(candidate={'id':'a'},auc_inner=.6,auc_outer=.99),dict(candidate={'id':'b'},auc_inner=.7,auc_outer=.1)]
        self.assertEqual(choose(t)['candidate']['id'],'b')
if __name__=='__main__':unittest.main()
