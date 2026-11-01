import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np,pandas as pd
from modelar_eeg_por_canal_v2 import FEATURES,HISTORY_COLUMNS,LEGACY_FEATURES,base_features,features,preprocessor,candidates
class SpatialModelTests(unittest.TestCase):
    def frame(self):
        f=pd.DataFrame(np.random.default_rng(23).uniform(.1,2,(24,len(FEATURES))),columns=FEATURES)
        return f.assign(participant=['A']*12+['B']*12,split='train',recording='r',segment_id=1,stimulus='s',window_start_utc=list(pd.date_range('2026-01-01',periods=12,freq='s',tz='UTC'))*2)
    def test_temporal_panel_is_bounded_and_causal(self):
        f=self.frame();p=preprocessor().fit(base_features(f,'inductivo'));a=features(p,f,'inductivo',8)
        z=p.transform(base_features(f,'inductivo'))
        self.assertEqual(a.shape[1],z.shape[1]+len(HISTORY_COLUMNS)+len(LEGACY_FEATURES))
        f.loc[7:11,FEATURES]=999;b=features(p,f,'inductivo',8);np.testing.assert_array_equal(a[:7],b[:7])
    def test_teacher_inputs_are_excluded(self):
        self.assertEqual(len(FEATURES),len(set(FEATURES)))
        self.assertFalse(any(c.startswith(('pupil','gaze','fixation','attention')) for c in FEATURES))
        f=self.frame();p=preprocessor().fit(base_features(f,'inductivo'));a=features(p,f,'inductivo',1)
        f['attention_binary']=1;f['pupil_mean_z']=999;b=features(p,f,'inductivo',1);np.testing.assert_array_equal(a,b)
    def test_predeclared_grid_has_36_configs(self):self.assertEqual(len(candidates(1)),36)
if __name__=='__main__':unittest.main()
