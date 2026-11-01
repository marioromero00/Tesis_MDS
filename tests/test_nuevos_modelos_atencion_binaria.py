import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np
import pandas as pd
from nuevos_modelos_atencion_binaria import choose,macro_auc,estimator,paired
class NewModelsTests(unittest.TestCase):
    def test_selection_ignores_outer_scores(self):
        records=[dict(family='LDA',mode='current',config_index=0,auc_inner=.65,auc_outer=.1),dict(family='QDA',mode='current',config_index=0,auc_inner=.6,auc_outer=.99)]
        self.assertEqual(choose(records)['family'],'LDA')
        records[1]['auc_outer']=1.;self.assertEqual(choose(records)['family'],'LDA')
    def test_macro_auc_equal_weight_people(self):
        f=pd.DataFrame({'participant':['A']*4+['B']*2,'y':[0,0,1,1,0,1]})
        self.assertEqual(macro_auc(f,[0,.1,.9,1,1,0]),.5)
    def test_no_random_window_early_stopping(self):
        self.assertFalse(estimator('HistBoost',dict(max_leaf_nodes=7,l2_regularization=5),18).early_stopping)
    def test_paired_interval_preserves_person_differences(self):
        result=paired([.02]*25)
        self.assertAlmostEqual(result['mean'],.02);self.assertAlmostEqual(result['ci_low'],.02);self.assertAlmostEqual(result['ci_high'],.02)
if __name__=='__main__':unittest.main()
