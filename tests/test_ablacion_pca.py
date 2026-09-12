import sys
import unittest
import numpy as np
from pathlib import Path
from threadpoolctl import threadpool_limits
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from ablacion_pca_core import variants,design,feature_cache,inputs,fit,predict,names
from hiperparametros_core import FULL,TARGET,MODALITIES
from test_hiperparametros import frame


class AblationTests(unittest.TestCase):
    def test_deployed_reduced_model_accepts_only_retained_signals(self):
        from predecir_ablacion_pca import predict as reduced_predict
        f=frame(); ref=dict(definition=dict(representation='relative',alpha=1),smoothing=8)
        definition=next(v for v in variants() if v['variant']=='only_eeg'); spec=design(ref,definition)
        with threadpool_limits(limits=2):
            bundle=fit(inputs(feature_cache(f),spec),f,spec)
            reduced=f[definition['keep']+['participant','recording','window_start_utc']]
            np.testing.assert_array_equal(reduced_predict(bundle,reduced),predict(bundle,f))
            with self.assertRaises(ValueError): reduced_predict(bundle,reduced.drop(columns=[definition['keep'][0]]))

    def test_removed_signal_and_teacher_cannot_change_inputs(self):
        f=frame(); reference=dict(definition=dict(representation='multiscale',alpha=1),smoothing=8)
        for definition in [v for v in variants() if v['kind'] in ['modality','variable']]:
            spec=design(reference,definition); altered=f.copy()
            removed=[c for c in FULL if c not in definition['keep']]; altered[removed]=1e9; altered[TARGET]='alto'; altered['gsr_mean_z']=1e9
            np.testing.assert_array_equal(inputs(feature_cache(f),spec),inputs(feature_cache(altered),spec))
        for rep,value in feature_cache(f).items(): self.assertEqual(len(names(rep)),value.shape[1])

    def test_pca_full_rotation_preserves_ridge_and_pca_is_train_only(self):
        f=frame(); fitting=f.iloc[:90].reset_index(drop=True); val=f.iloc[90:].reset_index(drop=True)
        reference=dict(definition=dict(representation='current',alpha=1),smoothing=1); cache=feature_cache(fitting)
        with threadpool_limits(limits=2):
            ref=fit(inputs(cache,design(reference,variants()[0])),fitting,design(reference,variants()[0]))
            for definition in [v for v in variants() if v['kind']=='pca']:
                spec=design(reference,definition); bundle=fit(inputs(cache,spec),fitting,spec)
                p=predict(bundle,val.drop(columns=[TARGET])); np.testing.assert_allclose(p.sum(axis=1),1)
                self.assertEqual(bundle['model']['pca'].n_samples_,len(fitting))
                if definition['pca']=='full': np.testing.assert_allclose(p,predict(ref,val),rtol=1e-9,atol=1e-9)


if __name__=='__main__': unittest.main()
