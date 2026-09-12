import sys
import unittest
import tempfile
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from regresion_ordinal_core import fit,predict,grid,feature_cache,decide
from test_hiperparametros import frame


class OrdinalRegressionTests(unittest.TestCase):
    def test_kernel_prediction_is_independent_of_array_layout(self):
        from continuar_regresion_ordinal import raw_scores
        f=pd.concat([frame(),frame().assign(participant=lambda x:x.participant+'b')],ignore_index=True)
        x=feature_cache(f)['current']; d=next(d for d in grid() if d['family']=='rbf' and d['representation']=='current')
        with threadpool_limits(limits=2):
            b=fit(np.ascontiguousarray(x),f,d,5)
            np.testing.assert_array_equal(raw_scores(b,np.ascontiguousarray(x)),raw_scores(b,np.asfortranarray(x)))

    def test_thresholds_and_future_independence(self):
        f=frame(); score=np.linspace(-1,1,len(f))
        np.testing.assert_array_equal(decide(f,score,1,-.1,.1),np.where(score<-.1,0,np.where(score>.1,2,1)))
        changed=score.copy(); changed[15:]=100
        np.testing.assert_array_equal(decide(f,score,16,-.1,.1)[:15],decide(f,changed,16,-.1,.1)[:15])

    def test_all_families_reload_without_label(self):
        f=pd.concat([frame(),frame().assign(participant=lambda x:x.participant+'b')],ignore_index=True); cache=feature_cache(f)
        with threadpool_limits(limits=2),tempfile.TemporaryDirectory() as tmp:
            for d in [d for d in grid() if d['representation']=='current']:
                bundle=fit(cache['current'],f,d,5); bundle.update(smoothing=16,low=-.1,high=.1)
                path=Path(tmp)/'m.joblib'; joblib.dump(bundle,path)
                np.testing.assert_array_equal(predict(bundle,f),predict(joblib.load(path),f.drop(columns=['arousal_label_6s'])))


if __name__=='__main__': unittest.main()
