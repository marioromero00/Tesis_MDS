import sys
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from explorar_fusiones import fuse,candidates,causal_features,TASKS


class FusionTests(unittest.TestCase):
    def test_probability_fusions_preserve_simplex_and_unimodal_limit(self):
        p=np.array([[.1,.2,.7],[.3,.3,.4]])
        q=np.array([[.8,.1,.1],[.1,.8,.1]])
        np.testing.assert_array_equal(fuse([p,q],[1,0]),p)
        for geometric in [False,True]:
            r=fuse([p,q],[.25,.75],geometric)
            np.testing.assert_allclose(r.sum(axis=1),1)
            self.assertTrue(np.isfinite(r).all() and (r>=0).all())
            np.testing.assert_allclose(r,fuse([q,p],[.75,.25],geometric))
        with self.assertRaises(ValueError): fuse([p,q],[.5,.6])

    def test_equal_experts_and_zero_probabilities(self):
        p=np.array([[0.,.3,.7]])
        np.testing.assert_allclose(fuse([p,p],[.5,.5],True),p,atol=1e-11)

    def test_temporal_features_never_read_future_or_other_participant(self):
        frame=pd.DataFrame(dict(participant=['P1']*3+['P2'],recording=['R']*4,
            window_start_utc=['2026-01-01T00:00:00Z','2026-01-01T00:00:01Z',
                              '2026-01-01T00:00:02Z','2026-01-01T00:00:00Z'],a=[1.,3.,5.,99.]))
        original=causal_features(frame,['a'],8)
        frame.loc[2:,'a']=-999
        np.testing.assert_array_equal(original[:2],causal_features(frame,['a'],8)[:2])
        self.assertEqual(original[3,1],99.)

    def test_late_weights_retain_modalities_and_teacher_excluded(self):
        for spec in TASKS.values():
            self.assertTrue(set(sum(spec['modalities'].values(),[])).isdisjoint(spec['forbidden']))
            for c in candidates(list(spec['modalities'])):
                if c['strategy']=='late_weighted':
                    self.assertTrue(all(w>0 for w in c['weights']))
                    self.assertAlmostEqual(sum(c['weights']),1.)

    def test_extra_trees_repeated_serial_probabilities_are_exact(self):
        from ejecutar_fusiones_estables import serial_model
        from explorar_fusiones import proba
        x=np.random.default_rng(10).normal(size=(300,5)); y=np.tile(['bajo','medio','alto'],100)
        model=serial_model('extra_trees',10).fit(x,y)
        self.assertEqual(model.named_steps['model'].n_jobs,1)
        np.testing.assert_array_equal(proba(model,x),proba(model,x))


if __name__=='__main__': unittest.main()
