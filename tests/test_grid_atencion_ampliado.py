import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np,pandas as pd
from grid_atencion_caracteristicas_ampliadas import FEATURES,base_features,features,preprocessor
class ExtendedGridTests(unittest.TestCase):
    def frame(self):
        f=pd.DataFrame(np.random.default_rng(13).uniform(.01,2,(20,len(FEATURES))),columns=FEATURES)
        return f.assign(participant=['A']*10+['B']*10,split='train',recording='r',segment_id=1,stimulus='s',window_start_utc=list(pd.date_range('2026-01-01',periods=10,freq='s',tz='UTC'))*2)
    def test_ranks_never_share_people(self):
        f=self.frame();a=base_features(f,'rangos_offline');f.loc[10:,FEATURES]=999
        b=base_features(f,'rangos_offline');np.testing.assert_array_equal(a.iloc[:10],b.iloc[:10])
    def test_no_teacher_inputs(self):
        f=self.frame();a=base_features(f,'rangos_offline');f['attention_binary']=1;f['pupil_mean_z']=999;f['fixation_count']=-999
        pd.testing.assert_frame_equal(a,base_features(f,'rangos_offline'))
        self.assertFalse(any(c.startswith(('pupil','fixation','gaze','attention')) for c in FEATURES))
    def test_history_remains_causal_without_person_calibration(self):
        f=self.frame();prep=preprocessor().fit(base_features(f,'inductivo'));a=features(prep,f,'inductivo',32)
        f.loc[6:9,FEATURES]=99;b=features(prep,f,'inductivo',32);np.testing.assert_array_equal(a[:6],b[:6])
if __name__=='__main__':unittest.main()
