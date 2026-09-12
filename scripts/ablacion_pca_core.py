"""Ablaciones reentrenadas y PCA, con hiperparametros de referencia fijos."""
import numpy as np
from sklearn.decomposition import PCA
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from hiperparametros_core import FULL,MODALITIES,TARGET
from multiescala_core import feature_cache as original_cache
from avanzados_core import sample_weights
from temporales_core import preprocessor,CLASSES
from optimizar_historial import smooth


def feature_cache(frame): return {k:np.ascontiguousarray(v) for k,v in original_cache(frame).items()}


def names(representation):
    if representation=='current': prefixes=['current']
    elif representation in ['multiscale','delayed4']:
        prefixes=['current']+[f'{kind}{w}' for w in [4,16,64] for kind in ['mean','std','delta']]
    elif representation=='relative': prefixes=['relative_current','relative_mean4','relative_mean16','ratio_std4','ratio_std16']
    else: raise ValueError(representation)
    return [(f'{prefix}__{column}',column) for prefix in prefixes for column in FULL]


def variants():
    definitions=[dict(variant='reference',kind='reference',keep=FULL)]
    for modality,columns in MODALITIES.items():
        definitions.append(dict(variant='without_'+modality,kind='modality',keep=[c for c in FULL if c not in columns]))
        definitions.append(dict(variant='only_'+modality,kind='unimodal',keep=columns))
    definitions += [dict(variant=v,kind='temporal',keep=FULL) for v in ['current_keep_smooth','no_smooth','current_no_smooth']]
    definitions += [dict(variant='drop_'+c,kind='variable',removed=c,keep=[x for x in FULL if x!=c]) for c in FULL]
    definitions += [dict(variant=f'pca_{v}',kind='pca',keep=FULL,pca=v) for v in [.8,.9,.95,'full']]
    return definitions


def design(reference,variant):
    representation='current' if variant['variant'] in ['current_keep_smooth','current_no_smooth'] else reference['definition']['representation']
    smoothing=1 if variant['variant'] in ['no_smooth','current_no_smooth'] else reference['smoothing']
    pairs=names(representation); indices=[i for i,(_,c) in enumerate(pairs) if c in variant['keep']]
    return dict(representation=representation,smoothing=smoothing,indices=indices,input_names=[pairs[i][0] for i in indices],
        alpha=reference['definition']['alpha'],variant=variant)


def fit(x,frame,spec):
    steps=[('prep',preprocessor())]
    if spec['variant']['kind']=='pca':
        n=spec['variant']['pca']; steps.append(('pca',PCA(n_components=None if n=='full' else n,svd_solver='full',whiten=False)))
    steps.append(('model',RidgeClassifier(alpha=spec['alpha'],solver='cholesky')))
    model=Pipeline(steps).fit(np.ascontiguousarray(x),frame[TARGET],model__sample_weight=sample_weights(frame,'participant'))
    return dict(model=model,spec=spec)


def inputs(cache,spec): return np.ascontiguousarray(cache[spec['representation']][:,spec['indices']])


def predict(bundle,frame,cache=None):
    if cache is None: cache=feature_cache(frame)
    x=inputs(cache,bundle['spec']); model=bundle['model']; order=[list(model.classes_).index(c) for c in CLASSES]
    logits=model.decision_function(x)[:,order]; probability=np.exp(logits-logits.max(axis=1,keepdims=True)); probability/=probability.sum(axis=1,keepdims=True)
    return smooth(frame,probability,bundle['spec']['smoothing'])
