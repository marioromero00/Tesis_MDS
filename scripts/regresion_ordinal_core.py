"""Misma etiqueta evaluada; entrenamiento escalar bajo=-1, medio=0, alto=1."""
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor,ExtraTreesRegressor
from sklearn.kernel_approximation import Nystroem
from sklearn.pipeline import Pipeline
from multiescala_core import feature_cache
from hiperparametros_core import TARGET
from avanzados_core import sample_weights
from optimizar_historial import smooth
from temporales_core import preprocessor,CLASSES


def grid():
    return [dict(base_id=f'{rep}_{family}',representation=rep,family=family)
            for rep in ['current','multiscale','relative'] for family in ['ridge','rbf','hgb','trees']]


def fit(x,frame,definition,seed):
    family=definition['family']; steps=[('prep',preprocessor())]
    if family=='rbf': steps.append(('kernel',Nystroem(kernel='rbf',gamma=.1/x.shape[1],n_components=192,random_state=seed,n_jobs=1)))
    if family=='hgb': model=HistGradientBoostingRegressor(max_iter=150,max_leaf_nodes=7,min_samples_leaf=100,learning_rate=.05,l2_regularization=20,early_stopping=False,random_state=seed)
    elif family=='trees': model=ExtraTreesRegressor(n_estimators=150,max_depth=8,min_samples_leaf=40,random_state=seed,n_jobs=1)
    else: model=Ridge(alpha=100 if family=='ridge' else 1,solver='cholesky')
    estimator=Pipeline(steps+[('model',model)])
    estimator.fit(x,frame[TARGET].map(dict(zip(CLASSES,[-1.,0.,1.]))),model__sample_weight=sample_weights(frame,'participant'))
    return dict(model=estimator,definition=definition,seed=seed)


def raw_scores(bundle,x): return bundle['model'].predict(x)


def decide(frame,score,window,low,high):
    value=smooth(frame,np.asarray(score).reshape(-1,1),window)[:,0]
    return np.where(value<low,0,np.where(value>high,2,1))


def predict(bundle,frame):
    x=feature_cache(frame)[bundle['definition']['representation']]
    return np.asarray(CLASSES)[decide(frame,raw_scores(bundle,x),bundle['smoothing'],bundle['low'],bundle['high'])]
