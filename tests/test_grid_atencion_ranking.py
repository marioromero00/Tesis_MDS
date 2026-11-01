import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np,pandas as pd
from grid_atencion_ranking import ranking_group_weights,make_model,candidates,FEATURES
class RankingTests(unittest.TestCase):
    def test_group_weights_equalize_capped_pair_counts(self):
        f=pd.DataFrame({'participant':['A']*8+['B']*12,'y':[0]*4+[1]*4+[0]*6+[1]*6})
        w=ranking_group_weights(f)
        self.assertAlmostEqual(w[0]*16,1000);self.assertAlmostEqual(w[-1]*36,1000)
        self.assertNotIn('participant',FEATURES)
    def test_ranker_accepts_groups_without_identity_feature(self):
        f=pd.DataFrame({'participant':['A']*8+['B']*8,'y':[0,1]*8});x=np.arange(32,dtype=float).reshape(16,2)
        c=candidates(1)[0];c['params']['iterations']=2;m=make_model(c)
        m.fit(x,f.y,group_id=f.participant.to_numpy(),group_weight=ranking_group_weights(f))
        self.assertTrue(np.isfinite(m.predict(x)).all())
if __name__=='__main__':unittest.main()
