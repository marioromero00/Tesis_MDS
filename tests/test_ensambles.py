import sys
import tempfile
import unittest
from pathlib import Path
import joblib
import numpy as np
from threadpoolctl import threadpool_limits
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from ensambles_core import BASES,pool_grid,pool,meta_matrix,fit_meta,combine,predict
from hiperparametros_core import TARGET,feature_cache,fit_bundle,raw_scores
from test_hiperparametros import frame


class EnsembleTests(unittest.TestCase):
    def test_pool_weights_and_order(self):
        f=frame(); rng=np.random.default_rng(1)
        probabilities={d['base_id']:rng.dirichlet([1,1,1],size=len(f)) for d in BASES}
        self.assertEqual(meta_matrix(probabilities).shape,(len(f),42))
        for choice in pool_grid():
            self.assertAlmostEqual(sum(choice['weights']),1)
            actual=pool(f,probabilities,choice)
            np.testing.assert_allclose(actual.sum(axis=1),1)
            self.assertTrue((actual>=0).all())
            if choice['aggregation']=='mean' and choice['smoothing']==1:
                expected=sum(w*probabilities[k] for w,k in zip(choice['weights'],choice['members']))
                np.testing.assert_allclose(actual,expected)

    def test_meta_fit_and_self_contained_reload(self):
        f=frame(); cache=feature_cache(f); indices=np.arange(len(f))
        with threadpool_limits(limits=2),tempfile.TemporaryDirectory() as temporary:
            bank={d['base_id']:fit_bundle(cache,indices,f,d,2) for d in BASES}
            probabilities={k:raw_scores(b,cache,indices) for k,b in bank.items()}
            # Synthetic fixture tests serialization only; real meta training uses group-OOF.
            definition=dict(kind='stack',C=.01,weighting='participant')
            estimator=fit_meta(meta_matrix(probabilities),f,TARGET,definition,2)
            for choice,meta in [(definition,estimator),(dict(kind='pool',pool=pool_grid()[0]),None)]:
                bundle=dict(choice=choice,bases=bank,meta=meta)
                path=Path(temporary)/'ensemble.joblib'; joblib.dump(bundle,path)
                p=predict(bundle,f,cache)
                np.testing.assert_array_equal(p,predict(joblib.load(path),f,cache))
                np.testing.assert_array_equal(p,combine(f,probabilities,choice,meta))


if __name__=='__main__': unittest.main()
