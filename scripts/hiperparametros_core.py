"""Modelos y grilla explicita; todas las transformaciones se ajustan en train."""
import itertools
import warnings
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from baselines_estaticos import EEG, EYE, GSR
from control_historial import FEATURES
from explorar_fusiones import causal_features, fuse
from optimizar_historial import smooth
from temporales_core import CLASSES, preprocessor

TARGET='arousal_label_6s'
MODALITIES={'pupil':FEATURES,'eye':EYE,'eeg':EEG}
FULL=FEATURES+EYE+EEG
SCOPES=['all','svm_rbf','hgb','qda','fusion_logistic','fusion_lda','fusion']


def grid():
    definitions=[]
    for c,gamma_factor in itertools.product([.1,1.,10.],[.1,1.]):
        definitions.append(dict(family='svm_rbf',params=dict(C=c,gamma_factor=gamma_factor)))
    for leaves in [7,15,31]:
        for regular in [True,False]:
            definitions.append(dict(family='hgb',params=dict(max_leaf_nodes=leaves,
                learning_rate=.03 if regular else .1,max_iter=150 if regular else 200,
                min_samples_leaf=100 if regular else 30,l2_regularization=20. if regular else 1.)))
    for reg in [.1,.5,.9]:
        definitions.append(dict(family='qda',params=dict(reg_param=reg)))
    for c in [.001,.01,.1,1.]:
        definitions.append(dict(family='fusion_logistic',params=dict(C=c)))
    for shrinkage in [.1,.5,.9]:
        definitions.append(dict(family='fusion_lda',params=dict(shrinkage=shrinkage)))
    return [dict(base_id=f'b{i:02d}_ctx{context}',context=context,**definition)
            for i,definition in enumerate(definitions) for context in [1,8]]


def feature_cache(frame):
    panels=dict(full=FULL,**MODALITIES)
    assert set(FULL).isdisjoint(GSR)
    return {(name,context):np.ascontiguousarray(causal_features(frame,columns,context))
            for name,columns in panels.items() for context in [1,8]}


def fit_bundle(cache,indices,frame,definition,seed):
    family=definition['family']; params=definition['params']; context=definition['context']
    panels=list(MODALITIES) if family.startswith('fusion_') else ['full']
    y=frame[TARGET].to_numpy(); components={}; captured=[]
    for panel in panels:
        x=np.ascontiguousarray(cache[(panel,context)][indices])
        prep=preprocessor().fit(x); z=prep.transform(x)
        if family=='svm_rbf':
            # Uniform gamma definition after scaling; no implicit random-fold calibration.
            model=SVC(C=params['C'],gamma=params['gamma_factor']/z.shape[1],
                kernel='rbf',class_weight='balanced',
                decision_function_shape='ovr',break_ties=True,cache_size=512,random_state=seed)
        elif family=='hgb':
            model=HistGradientBoostingClassifier(**params,class_weight='balanced',
                early_stopping=False,random_state=seed)
        elif family=='qda':
            model=QuadraticDiscriminantAnalysis(**params,priors=np.ones(3)/3)
        elif family=='fusion_logistic':
            model=LogisticRegression(**params,class_weight='balanced',max_iter=4000,random_state=seed)
        elif family=='fusion_lda':
            model=LinearDiscriminantAnalysis(**params,solver='lsqr',priors=np.ones(3)/3)
        else: raise ValueError(family)
        with warnings.catch_warnings(record=True) as observed:
            warnings.simplefilter('always'); model.fit(z,y)
        captured.extend(dict(panel=panel,category=w.category.__name__,message=str(w.message)) for w in observed)
        if family=='svm_rbf' and model.fit_status_!=0: raise RuntimeError('SVC no convergio')
        if any(w['category']=='ConvergenceWarning' for w in captured): raise RuntimeError(captured)
        components[panel]=dict(preprocessor=prep,model=model)
    return dict(definition=definition,seed=seed,components=components,warnings=captured)


def raw_scores(bundle,cache,indices):
    definition=bundle['definition']; values=[]
    for panel,component in bundle['components'].items():
        z=component['preprocessor'].transform(cache[(panel,definition['context'])][indices])
        model=component['model']; order=[list(model.classes_).index(c) for c in CLASSES]
        if definition['family']=='svm_rbf':
            logits=model.decision_function(z)[:,order]
            value=np.exp(logits-logits.max(axis=1,keepdims=True)); value/=value.sum(axis=1,keepdims=True)
        else: value=model.predict_proba(z)[:,order]
        assert np.isfinite(value).all()
        values.append(value)
    return fuse(values,np.ones(len(values))/len(values),geometric=True) if len(values)>1 else values[0]


def predict(bundle,frame,cache=None):
    if cache is None: cache=feature_cache(frame)
    raw=raw_scores(bundle,cache,np.arange(len(frame)))
    return smooth(frame,raw,bundle['smoothing'])


def choose(scores,scope):
    eligible=scores
    if scope=='fusion': eligible=scores.loc[scores.family.str.startswith('fusion_')]
    elif scope!='all': eligible=scores.loc[scores.family.eq(scope)]
    if eligible.empty: raise ValueError(scope)
    return eligible.sort_values(['score','candidate_id'],ascending=[False,True]).iloc[0]
