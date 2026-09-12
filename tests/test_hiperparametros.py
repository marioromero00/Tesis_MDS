import sys
import tempfile
import unittest
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from hiperparametros_core import FULL,TARGET,grid,feature_cache,fit_bundle,predict
from temporales_core import CLASSES


def frame():
    rng=np.random.default_rng(87)
    f=pd.DataFrame(rng.normal(size=(120,len(FULL))),columns=FULL)
    f['participant']=np.repeat(['P1','P2','P3','P4'],30)
    f['recording']='r1'; f['window_start_utc']=pd.date_range('2026-01-01',periods=120,freq='s').astype(str)
    f[TARGET]=np.tile(CLASSES,40)
    f.loc[::10,FULL[0]]=np.nan
    return f


class HyperparameterTests(unittest.TestCase):
    def test_all_families_reload_and_svm_argmax_matches_predict(self):
        f=frame(); cache=feature_cache(f); index=np.arange(len(f))
        with threadpool_limits(limits=2),tempfile.TemporaryDirectory() as temporary:
            for family in ['svm_rbf','hgb','qda','fusion_logistic','fusion_lda']:
                definition=next(d for d in grid() if d['family']==family and d['context']==1)
                bundle=fit_bundle(cache,index,f,definition,5); bundle['smoothing']=1
                p=predict(bundle,f,cache)
                self.assertTrue(np.isfinite(p).all()); self.assertTrue((p>=0).all())
                np.testing.assert_allclose(p.sum(axis=1),1,atol=1e-12)
                path=Path(temporary)/f'{family}.joblib'; joblib.dump(bundle,path)
                np.testing.assert_array_equal(p,predict(joblib.load(path),f,cache))
                if family=='svm_rbf':
                    component=bundle['components']['full']; z=component['preprocessor'].transform(cache[('full',1)])
                    np.testing.assert_array_equal(np.asarray(CLASSES)[p.argmax(axis=1)],component['model'].predict(z))

    def test_held_out_people_cannot_change_training_features_or_scaler(self):
        f=frame(); altered=f.copy(); altered.loc[90:,FULL]=1e9
        original=feature_cache(f); changed=feature_cache(altered)
        for key in original: np.testing.assert_array_equal(original[key][:90],changed[key][:90])
        definition=next(d for d in grid() if d['family']=='svm_rbf' and d['context']==8)
        with threadpool_limits(limits=2):
            a=fit_bundle(original,np.arange(90),f.iloc[:90],definition,5)
            b=fit_bundle(changed,np.arange(90),altered.iloc[:90],definition,5)
        for name in ['mean_','scale_']:
            np.testing.assert_array_equal(getattr(a['components']['full']['preprocessor']['scale'],name),
                getattr(b['components']['full']['preprocessor']['scale'],name))

    def test_current_history_not_affected_by_future_features_or_labels(self):
        f=frame(); changed=f.copy(); changed.loc[20:29,FULL]=1e8; changed[TARGET]='alto'
        a=feature_cache(f); b=feature_cache(changed)
        for key in a: np.testing.assert_array_equal(a[key][:20],b[key][:20])


if __name__=='__main__': unittest.main()
