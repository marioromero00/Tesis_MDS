"""CatBoost y modelos ordinales con pesos ajustados solo en entrenamiento."""
import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.linear_model import LogisticRegression
from baselines_estaticos import EEG,EYE,GSR
from control_historial import FEATURES
from explorar_fusiones import causal_features
from optimizar_historial import smooth
from temporales_core import CLASSES,preprocessor

PANELS={'eye_pupil':FEATURES+EYE,'full':FEATURES+EYE+EEG}
TARGET='arousal_label_6s'


def sample_weights(frame,mode):
    counts=frame[TARGET].value_counts()
    if mode=='global': weights=1/frame[TARGET].map(counts).to_numpy(float)
    elif mode=='participant':
        pair_counts=frame.groupby(['participant',TARGET])[TARGET].transform('size').to_numpy(float)
        classes=frame.groupby('participant')[TARGET].transform('nunique').to_numpy(float)
        weights=1/(pair_counts*classes)
    else: raise ValueError(mode)
    return weights/weights.mean()


def inputs(frame,panel,context):
    columns=PANELS[panel]
    assert set(columns).isdisjoint(GSR)
    return causal_features(frame,columns,context)


def ordinal_probabilities(at_least_medium,high):
    first=np.asarray(at_least_medium,float).copy(); second=np.asarray(high,float).copy()
    violated=second>first
    average=(first+second)/2
    first[violated]=average[violated]; second[violated]=average[violated]
    return np.column_stack([1-first,first-second,second])


def fit_bundle(x,frame,family,mode,seed):
    prep=preprocessor().fit(x); transformed=prep.transform(x)
    weights=sample_weights(frame,mode); y=frame[TARGET].map({c:i for i,c in enumerate(CLASSES)}).to_numpy(int)
    if family=='catboost':
        model=CatBoostClassifier(iterations=300,depth=4,learning_rate=.03,l2_leaf_reg=20,
            loss_function='MultiClass',bootstrap_type='Bernoulli',subsample=.8,rsm=.8,
            thread_count=4,random_seed=seed,verbose=False,allow_writing_files=False,use_best_model=False)
        model.fit(transformed,y,sample_weight=weights)
        models=[model]
    elif family=='ordinal':
        models=[LogisticRegression(C=.1,max_iter=2000,random_state=seed).fit(
            transformed,(y>=threshold).astype(int),sample_weight=weights) for threshold in [1,2]]
    elif family=='logistic':
        models=[LogisticRegression(C=.1,max_iter=2000,random_state=seed).fit(transformed,y,sample_weight=weights)]
    else: raise ValueError(family)
    return dict(preprocessor=prep,models=models,family=family,weighting=mode,seed=seed)


def raw_probabilities(bundle,x):
    transformed=bundle['preprocessor'].transform(x)
    if bundle['family']=='ordinal':
        probabilities=[m.predict_proba(transformed)[:,list(m.classes_).index(1)] for m in bundle['models']]
        return ordinal_probabilities(*probabilities)
    model=bundle['models'][0]
    return model.predict_proba(transformed)[:,[list(model.classes_).index(i) for i in range(3)]]


def adjust(frame,raw,smoothing,low_bias,high_bias):
    probability=smooth(frame,raw,smoothing)
    result=probability*np.exp([low_bias,0.,high_bias])[None,:]
    return result/result.sum(axis=1,keepdims=True)


def predict(bundle,frame):
    c=bundle['choice']
    raw=raw_probabilities(bundle,inputs(frame,c['panel'],c['context']))
    return adjust(frame,raw,c['smoothing'],c['low_bias'],c['high_bias'])
