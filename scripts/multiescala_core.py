"""Historial multiescala y cambios locales; solo señales del estudiante."""
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.kernel_approximation import Nystroem
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from hiperparametros_core import FULL,TARGET
from baselines_estaticos import GSR
from persistencia_core import starts
from temporales_core import CLASSES,preprocessor
from avanzados_core import sample_weights
from optimizar_historial import smooth

REPRESENTATIONS=['current','multiscale','delayed4','relative']


def feature_cache(frame):
    assert set(FULL).isdisjoint(GSR)
    raw=frame[FULL].to_numpy(float); reset=starts(frame); bounds=np.r_[np.flatnonzero(reset),len(frame)]
    means={w:np.full_like(raw,np.nan) for w in [4,16,64]}; stds={w:np.full_like(raw,np.nan) for w in means}
    delta={w:np.full_like(raw,np.nan) for w in means}
    for lo,hi in zip(bounds[:-1],bounds[1:]):
        block=pd.DataFrame(raw[lo:hi])
        for w in means:
            means[w][lo:hi]=block.rolling(w,min_periods=1).mean().to_numpy()
            stds[w][lo:hi]=block.rolling(w,min_periods=1).std(ddof=0).to_numpy()
            lag=np.maximum(np.arange(hi-lo)-w+1,0)
            delta[w][lo:hi]=raw[lo:hi]-raw[lo+lag]
    multi=np.column_stack([raw]+[a[w] for w in means for a in [means,stds,delta]])
    delayed=np.full_like(multi,np.nan)
    for lo,hi in zip(bounds[:-1],bounds[1:]):
        delayed[lo:hi]=multi[lo+np.maximum(np.arange(hi-lo)-4,0)]
    # Dimensionless local deviations suppress participant-specific levels.
    scale=stds[64]+.1
    relative=np.column_stack([(raw-means[64])/scale,(means[4]-means[64])/scale,
        (means[16]-means[64])/scale,stds[4]/scale,stds[16]/scale])
    return dict(current=raw,multiscale=multi,delayed4=delayed,relative=np.clip(relative,-10,10))


def grid():
    models=[dict(family='ridge',alpha=a) for a in [1.,100.]]
    models += [dict(family='rbf',alpha=a,gamma_factor=g) for a,g in [(1.,.1),(100.,1.)]]
    models += [dict(family='trees',depth=d,leaf=l) for d,l in [(8,40),(None,100)]]
    return [dict(base_id=f'{rep}_m{i}',representation=rep,**m) for rep in REPRESENTATIONS for i,m in enumerate(models)]


def fit(x,frame,definition,seed):
    steps=[('prep',preprocessor())]
    if definition['family']=='rbf':
        steps.append(('kernel',Nystroem(kernel='rbf',gamma=definition['gamma_factor']/x.shape[1],n_components=192,random_state=seed,n_jobs=1)))
    if definition['family']=='trees':
        model=ExtraTreesClassifier(n_estimators=150,max_depth=definition['depth'],min_samples_leaf=definition['leaf'],random_state=seed,n_jobs=1)
    else: model=RidgeClassifier(alpha=definition['alpha'],solver='cholesky')
    estimator=Pipeline(steps+[('model',model)])
    estimator.fit(x,frame[TARGET],model__sample_weight=sample_weights(frame,'participant'))
    return dict(model=estimator,definition=definition,seed=seed)


def raw_scores(bundle,x):
    model=bundle['model']; order=[list(model.classes_).index(c) for c in CLASSES]
    if bundle['definition']['family']=='trees': return model.predict_proba(x)[:,order]
    logits=model.decision_function(x)[:,order]
    result=np.exp(logits-logits.max(axis=1,keepdims=True)); return result/result.sum(axis=1,keepdims=True)


def predict(bundle,frame):
    return smooth(frame,raw_scores(bundle,feature_cache(frame)[bundle['definition']['representation']]),bundle['smoothing'])
