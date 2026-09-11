import sys
import tempfile
import unittest
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from avanzados_core import sample_weights,ordinal_probabilities,fit_bundle,raw_probabilities,adjust,TARGET
from temporales_core import individual_scores


class AdvancedTests(unittest.TestCase):
    def test_person_weights_equal_macro_recall_even_with_absent_class(self):
        frame=pd.DataFrame(dict(participant=['P1']*6+['P2']*3))
        frame[TARGET]=['bajo']*4+['medio','alto']+['bajo','bajo','alto']
        pred=np.array(['bajo','medio','bajo','alto','medio','alto','bajo','alto','medio'])
        weights=sample_weights(frame,'participant')
        expected=np.mean(list(individual_scores(frame,TARGET,pred,'classification').values()))
        self.assertAlmostEqual(np.average(pred==frame[TARGET],weights=weights),expected)
        totals=pd.Series(weights).groupby(frame.participant).sum()
        self.assertAlmostEqual(totals.iloc[0],totals.iloc[1]); self.assertAlmostEqual(weights.mean(),1)

    def test_ordinal_projection_has_valid_probabilities(self):
        p=ordinal_probabilities([.8,.2,0,1],[.1,.7,0,1])
        np.testing.assert_allclose(p.sum(axis=1),1)
        self.assertTrue((p>=0).all())
        np.testing.assert_allclose(p[1],[.55,0,.45])
        np.testing.assert_allclose(p[0],[.2,.7,.1])

    def test_new_model_families_reload_with_same_probabilities(self):
        rng=np.random.default_rng(2); x=rng.normal(size=(90,4))
        frame=pd.DataFrame(dict(participant=np.repeat(['P1','P2','P3'],30)))
        frame[TARGET]=np.tile(['bajo','medio','alto'],30)
        with tempfile.TemporaryDirectory() as temporary:
            for family in ['logistic','ordinal','catboost']:
                bundle=fit_bundle(x,frame,family,'participant',2)
                path=Path(temporary)/f'{family}.joblib'; joblib.dump(bundle,path)
                before=raw_probabilities(bundle,x); after=raw_probabilities(joblib.load(path),x)
                np.testing.assert_array_equal(before,after); np.testing.assert_allclose(before.sum(axis=1),1)

    def test_decision_adjustment_preserves_identity_and_simplex(self):
        frame=pd.DataFrame(index=range(2)); raw=np.array([[.2,.3,.5],[.8,.1,.1]])
        np.testing.assert_array_equal(adjust(frame,raw,1,0,0),raw)
        changed=adjust(frame,raw,1,.3,-.3)
        np.testing.assert_allclose(changed.sum(axis=1),1)
        self.assertTrue((changed[:,0]>raw[:,0]).all())


if __name__=='__main__': unittest.main()
