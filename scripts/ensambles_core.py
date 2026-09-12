"""Promedio de regularizaciones y stacking con predicciones OOF por persona."""
import itertools
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from hiperparametros_core import grid,feature_cache,raw_scores
from avanzados_core import sample_weights
from optimizar_historial import smooth
from temporales_core import CLASSES

BASES=[d for d in grid() if d['family'].startswith('fusion_')]
STACKS=[dict(scope=f'stack_{weight}_C{c}',weighting=weight,C=c)
        for weight,c in itertools.product(['global','participant'],[.001,.01,.1])]
SCOPES=['pool_selected','pool_logistic','pool_lda','pool_fixed_history','pool_fixed_multiscale']+[s['scope'] for s in STACKS]


def pool_grid():
    result=[]
    for family,history_weight,aggregation,window in itertools.product(
            ['both','logistic','lda'],[0.,.25,.5,.75,1.],['mean','geometric'],[1,4]):
        members=[]; weights=[]
        for context,mass in [(1,1-history_weight),(8,history_weight)]:
            selected=[d for d in BASES if d['context']==context and
                      (family=='both' or d['family']==f'fusion_{family}')]
            if mass:
                members.extend(d['base_id'] for d in selected); weights.extend([mass/len(selected)]*len(selected))
        result.append(dict(candidate_id=f'{family}_h{history_weight}_{aggregation}_s{window}',
            family=family,history_weight=history_weight,aggregation=aggregation,smoothing=window,
            members=members,weights=weights))
    return result


def pool(frame,probabilities,choice):
    values=np.stack([probabilities[k] for k in choice['members']],axis=1)
    weights=np.asarray(choice['weights'])[None,:,None]
    if choice['aggregation']=='mean': result=(values*weights).sum(axis=1)
    elif choice['aggregation']=='geometric':
        logits=(np.log(np.clip(values,1e-12,1))*weights).sum(axis=1)
        result=np.exp(logits-logits.max(axis=1,keepdims=True)); result/=result.sum(axis=1,keepdims=True)
    else: raise ValueError(choice['aggregation'])
    return smooth(frame,result,choice['smoothing'])


def meta_matrix(probabilities):
    return np.ascontiguousarray(np.concatenate([probabilities[d['base_id']] for d in BASES],axis=1))


def fit_meta(x,frame,target,definition,seed):
    estimator=Pipeline([('scale',StandardScaler()),('model',LogisticRegression(C=definition['C'],
        max_iter=4000,random_state=seed))])
    return estimator.fit(x,frame[target],model__sample_weight=sample_weights(frame,definition['weighting']))


def combine(frame,probabilities,choice,meta=None):
    if choice['kind']=='pool': return pool(frame,probabilities,choice['pool'])
    model=meta['model']; order=[list(model.classes_).index(c) for c in CLASSES]
    return meta.predict_proba(meta_matrix(probabilities))[:,order]


def predict(bundle,frame,cache=None):
    if cache is None: cache=feature_cache(frame)
    probabilities={k:raw_scores(base,cache,np.arange(len(frame))) for k,base in bundle['bases'].items()}
    return combine(frame,probabilities,bundle['choice'],bundle.get('meta'))


def choose(scores,scope):
    selected=scores
    if scope=='pool_logistic': selected=scores.loc[scores.family.eq('logistic')]
    elif scope=='pool_lda': selected=scores.loc[scores.family.eq('lda')]
    elif scope!='pool_selected': raise ValueError(scope)
    return selected.sort_values(['score','candidate_id'],ascending=[False,True]).iloc[0]
