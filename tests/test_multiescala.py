import sys
import unittest
import tempfile
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from multiescala_core import feature_cache,fit,predict,grid
from hiperparametros_core import FULL,TARGET
from test_hiperparametros import frame


class MultiscaleTests(unittest.TestCase):
    def test_future_and_other_people_do_not_change_features(self):
        f=frame(); x=feature_cache(f); changed=f.copy(); changed.loc[75:,FULL]=1e6
        for name,a in feature_cache(changed).items(): np.testing.assert_array_equal(a[:75],x[name][:75])
        for name,a in feature_cache(f.drop(columns=[TARGET])).items(): np.testing.assert_array_equal(a,x[name])
        for person in f.participant.unique():
            mask=f.participant.eq(person).to_numpy()
            for name,a in feature_cache(f.loc[mask].reset_index(drop=True)).items(): np.testing.assert_array_equal(a,x[name][mask])

    def test_gap_reset_and_delayed_support(self):
        f=frame().iloc[:30].copy(); f['window_start_utc']=pd.date_range('2026-01-01',periods=30,freq='s')
        f.loc[15:,'window_start_utc']+=pd.Timedelta(seconds=10)
        x=feature_cache(f)
        for name,a in feature_cache(f.iloc[15:].reset_index(drop=True)).items(): np.testing.assert_array_equal(a,x[name][15:])
        np.testing.assert_array_equal(x['delayed4'][4:15],x['multiscale'][:11])

    def test_saved_models_predict_without_teacher(self):
        f=pd.concat([frame(),frame().assign(participant=lambda x:x.participant+'b')],ignore_index=True)
        x=feature_cache(f)
        with threadpool_limits(limits=2),tempfile.TemporaryDirectory() as tmp:
            for family in ['ridge','rbf','trees']:
                d=next(d for d in grid() if d['family']==family and d['representation']=='multiscale')
                b=fit(x['multiscale'],f,d,3); b['smoothing']=8
                p=predict(b,f.drop(columns=[TARGET])); np.testing.assert_allclose(p.sum(axis=1),1)
                path=Path(tmp)/'m.joblib'; joblib.dump(b,path)
                np.testing.assert_array_equal(p,predict(joblib.load(path),f))


if __name__=='__main__': unittest.main()
