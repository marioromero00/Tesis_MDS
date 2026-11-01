import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np
import pandas as pd
from reconstruir_profesor_atencion_binaria import COLUMNS, components, binary, fit_teacher

class TeacherTests(unittest.TestCase):
    def data(self):
        rng=np.random.default_rng(42)
        return pd.DataFrame(rng.uniform(.1,3,(18,5)),columns=COLUMNS).assign(participant=np.repeat(['A','B','C'],6))
    def test_binary_median_missing_and_ties(self):
        frame=pd.DataFrame({'participant':['A']*6})
        labels,thresholds=binary(pd.Series([0.,1.,1.,2.,3.,np.nan]),frame)
        self.assertEqual(labels.tolist()[:5],[0,0,0,1,1]); self.assertTrue(pd.isna(labels.iloc[5]))
        self.assertEqual(thresholds.n_ties.iloc[0],2)
    def test_old_labels_and_scores_irrelevant(self):
        f=self.data(); z,_=components(f)
        a=fit_teacher(f,z,['A','B'],'igualitario')[1]
        f['attention_score_equal']=99999; f['attention_label_equal']='alto'
        zz,_=components(f); b=fit_teacher(f,zz,['A','B'],'igualitario')[1]
        pd.testing.assert_series_equal(a,b)
    def test_pca_fit_never_uses_evaluation_people(self):
        f=self.data(); z,_=components(f)
        original=fit_teacher(f,z,['A','B'],'pca')[3]['pca']
        changed=z.copy(); changed.loc[f.participant.eq('C')]=99999
        altered=fit_teacher(f,changed,['A','B'],'pca')[3]['pca']
        np.testing.assert_array_equal(original.components_,altered.components_)
        np.testing.assert_array_equal(original.mean_,altered.mean_)
    def test_no_label_when_teacher_component_missing(self):
        f=self.data(); z,_=components(f); z.loc[0,COLUMNS[0]]=np.nan
        label=fit_teacher(f,z,['A','B'],'igualitario')[1]
        self.assertTrue(pd.isna(label.iloc[0]))

if __name__=='__main__': unittest.main()
