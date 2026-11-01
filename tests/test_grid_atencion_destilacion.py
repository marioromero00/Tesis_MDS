import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np,pandas as pd
from grid_atencion_destilacion import FEATURES,components,labeled_frame,features,base_features,preprocessor
from reconstruir_profesor_atencion_binaria import COLUMNS
class DistillationTests(unittest.TestCase):
    def frame(self):
        columns=list(dict.fromkeys(FEATURES+COLUMNS));rng=np.random.default_rng(17)
        return pd.DataFrame(rng.uniform(.1,2,(30,len(columns))),columns=columns).assign(participant=['A']*10+['B']*10+['C']*10,split='train',recording='r',segment_id=1,stimulus='s',window_start_utc=list(pd.date_range('2026-01-01',periods=10,freq='s',tz='UTC'))*3)
    def test_binary_labels_agree_with_continuous_target_sign(self):
        f=self.frame();z,_=components(f);d=labeled_frame(f,z,['A','B'],'pca')
        np.testing.assert_array_equal(d.y,d.teacher_margin.gt(0).astype(int))
        self.assertEqual(len(d),30)
    def test_teacher_margin_never_enters_input_matrix(self):
        f=self.frame();z,_=components(f);d=labeled_frame(f,z,['A','B'],'pca');p=preprocessor().fit(base_features(d,'inductivo'))
        a=features(p,d,'inductivo',8);d['teacher_margin']=999;d['y']=1
        b=features(p,d,'inductivo',8);np.testing.assert_array_equal(a,b)
        self.assertNotIn('teacher_margin',FEATURES)
if __name__=='__main__':unittest.main()
