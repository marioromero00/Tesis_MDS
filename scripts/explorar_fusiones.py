"""Registro de fusiones tempranas/tardias con seleccion agrupada interna."""
import argparse
import itertools
import json
from datetime import datetime, timezone

import joblib
import numpy as np
import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from threadpoolctl import threadpool_limits

from baselines_estaticos import EEG, GSR, EYE, validate_partition
from control_historial import FEATURES, nested_folds
from optimizar_historial import histories
from temporales_core import ROOT, CLASSES, digest, write_json, preprocessor, metric_record, individual_scores

OUT=ROOT/'resultados/fusiones_10-09-2026'
TASKS={
    'attention':dict(target='attention_label_equal',modalities={'EEG':EEG,'GSR':GSR},forbidden=EYE+FEATURES),
    'arousal':dict(target='arousal_label_6s',modalities={'Pupil':FEATURES,'Eye':EYE,'EEG':EEG},forbidden=GSR)}


def causal_features(frame, columns, context):
    raw=frame[columns].to_numpy(float)
    if context==1: return raw
    rows=[]
    for i,ix in histories(frame,context,'recording'):
        value=raw[ix]; count=np.isfinite(value).sum(axis=0)
        mean=np.divide(np.nansum(value,axis=0),count,out=np.full(len(columns),np.nan),where=count>0)
        var=np.divide(np.nansum((value-mean)**2,axis=0),count,out=np.full(len(columns),np.nan),where=count>0)
        rows.append(np.r_[raw[i],mean,np.sqrt(var),raw[i]-value[0],len(ix)/context])
    return np.asarray(rows)


def make_model(name,seed):
    if name=='logistic': model=LogisticRegression(C=.1,class_weight='balanced',max_iter=2000,random_state=seed)
    elif name=='logistic_reference': model=LogisticRegression(C=1,class_weight='balanced',max_iter=2000,random_state=seed)
    elif name=='lda': model=LinearDiscriminantAnalysis(solver='lsqr',shrinkage='auto',priors=np.ones(3)/3)
    elif name=='extra_trees': model=ExtraTreesClassifier(n_estimators=100,max_depth=8,min_samples_leaf=40,
        class_weight='balanced',random_state=seed,n_jobs=4)
    else: raise ValueError(name)
    return Pipeline([('prep',preprocessor()),('model',model)])


def proba(model,x):
    return model.predict_proba(x)[:,[list(model.classes_).index(c) for c in CLASSES]]


def fuse(probabilities, weights, geometric=False):
    stack=np.stack(probabilities,axis=1); weights=np.asarray(weights,float)
    if len(weights)!=stack.shape[1] or (weights<0).any() or not np.isclose(weights.sum(),1):
        raise ValueError('Pesos invalidos')
    if geometric:
        logits=(np.log(np.clip(stack,1e-12,1))*weights[None,:,None]).sum(axis=1)
        result=np.exp(logits-logits.max(axis=1,keepdims=True))
        return result/result.sum(axis=1,keepdims=True)
    return (stack*weights[None,:,None]).sum(axis=1)


def candidates(modalities):
    n=len(modalities); equal=[1/n]*n
    definitions=[dict(strategy='early',weights=None),dict(strategy='late_mean',weights=equal),
                 dict(strategy='late_geometric',weights=equal)]
    # Positive weights retain every modality; unimodal controls are evaluated separately.
    for units in itertools.product(range(1,4),repeat=n):
        if sum(units)==4:
            definitions.append(dict(strategy='late_weighted',weights=[v/4 for v in units]))
    for i,name in enumerate(modalities):
        weights=[0.]*n; weights[i]=1.
        definitions.append(dict(strategy='unimodal',weights=weights,modality=name))
    result=[]
    for context in [1,8]:
        for estimator in ['logistic','lda','extra_trees']:
            for definition in definitions:
                ident=f'{context}__{estimator}__{definition["strategy"]}__'+','.join(map(str,definition['weights'] or []))
                result.append(dict(candidate_id=ident,context=context,estimator=estimator,**definition))
    return result


def select_candidates(scores,definitions):
    merged=scores.merge(pd.DataFrame(definitions),on='candidate_id',validate='one_to_one')
    choices=[]
    for strategy in ['early','late_mean','late_geometric','late_weighted','unimodal']:
        row=merged.loc[merged.strategy.eq(strategy)].sort_values(['score','candidate_id'],ascending=[False,True]).iloc[0]
        chosen=next(d for d in definitions if d['candidate_id']==row.candidate_id)
        choices.append(dict(scope=strategy,inner_score=float(row.score),**chosen))
    return choices


def predict_bundle(bundle, frame):
    definition=bundle['definition']; context=definition['context']; modalities=bundle['modalities']
    xs={m:causal_features(frame,columns,context) for m,columns in modalities.items()}
    if definition['strategy']=='early':
        return proba(bundle['models']['early'],np.column_stack(list(xs.values())))
    ps=[proba(bundle['models'][m],xs[m]) for m in modalities]
    return fuse(ps,definition['weights'],definition['strategy']=='late_geometric')


def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--output',default=str(OUT.relative_to(ROOT)))
    args=parser.parse_args(); out=ROOT/args.output; out.mkdir(parents=True,exist_ok=False); (out/'modelos').mkdir()
    dataset=ROOT/'resultados/modelado/dataset_modelado.csv'; partition=ROOT/'resultados/modelado/particion_participantes.csv'
    old=json.loads((ROOT/'resultados/modelado/ejecuciones/baselines_05-09-2026_02/manifiesto_baselines.json').read_text(encoding='utf-8'))
    assert digest(dataset)==old['dataset_sha256'] and digest(partition)==old['partition_sha256']
    data=pd.read_csv(dataset); data['source_row']=np.arange(len(data)); validate_partition(data,pd.read_csv(partition))
    data=data.loc[data.split.eq('train')].copy()
    frames={task:data.loc[data[spec['target']].notna()].sort_values(['participant','recording','window_start_utc']).reset_index(drop=True)
            for task,spec in TASKS.items()}
    del data
    for spec in TASKS.values():
        assert set(sum(spec['modalities'].values(),[])).isdisjoint(spec['forbidden'])
    definitions={task:candidates(list(spec['modalities'])) for task,spec in TASKS.items()}
    folds={task:nested_folds(frame) for task,frame in frames.items()}
    protocol=dict(created_utc=datetime.now(timezone.utc).isoformat(),tasks=TASKS,candidates=definitions,folds=folds,
        seeds=[20260910,20260911],inner_folds=3,selection='mean BA macro across three internal participant folds; tie by candidate id',
        primary='late_weighted vs early, each selected internally among identical estimator/context panel',
        secondary='mean/geometric/unimodal vs early and fixed logistic on all current permitted predictors',
        history='current or up to eight consecutive past/current 2s windows, 1s step, within recording and person; may cross stimulus',
        scope='exploratory repeated research on original train; unchanged labels and participant split; no fresh confirmation',
        late_weights='positive quarter increments, sum one; all modalities retained; separate unimodal controls',
        preprocessing='each modality separately fit in late fusion; concatenated features jointly fit in early fusion, training people only',
        validation_evaluated=False,test_evaluated=False,dataset_sha256=digest(dataset),partition_sha256=digest(partition),
        sources={n:digest(ROOT/'scripts'/n) for n in ['explorar_fusiones.py','temporales_core.py','optimizar_historial.py','control_historial.py']})
    write_json(out/'protocolo.json',protocol)
    log=out/'bitacora.jsonl'
    def event(stage,**kwargs):
        with log.open('a',encoding='utf-8') as f:
            f.write(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),stage=stage,**kwargs),ensure_ascii=False)+'\n')
    search=[]; selected=[]; inner_fits=0
    for task,frame in frames.items():
        spec=TASKS[task]; target=spec['target']; modalities=spec['modalities']
        xs={c:{m:causal_features(frame,cols,c) for m,cols in modalities.items()} for c in [1,8]}
        for fold in folds[task]:
            fi=np.flatnonzero(frame.participant.isin(fold['fit'])); fit=frame.iloc[fi]
            splitter=GroupKFold(n_splits=3,shuffle=True,random_state=20260910+fold['fold'])
            for inner,(ii,vv) in enumerate(splitter.split(fit,groups=fit.participant),1):
                ti,vi=fi[ii],fi[vv]; validation=frame.iloc[vi].reset_index(drop=True)
                for context in [1,8]:
                    for estimator in ['logistic','lda','extra_trees']:
                        event('fit_started',task=task,fold=fold['fold'],inner=inner,context=context,estimator=estimator)
                        predictions={}
                        for m,x in {**xs[context],'early':np.column_stack(list(xs[context].values()))}.items():
                            model=make_model(estimator,20260910).fit(x[ti],frame.iloc[ti][target]); inner_fits+=1
                            predictions[m]=proba(model,x[vi])
                        for candidate in definitions[task]:
                            if candidate['context']!=context or candidate['estimator']!=estimator: continue
                            probs=predictions['early'] if candidate['strategy']=='early' else fuse(
                                [predictions[m] for m in modalities],candidate['weights'],candidate['strategy']=='late_geometric')
                            pred=np.asarray(CLASSES)[probs.argmax(axis=1)]
                            score=metric_record(validation,target,pred,'classification')['macro_score']
                            search.append(dict(task=task,fold=fold['fold'],inner=inner,candidate_id=candidate['candidate_id'],score=score,
                                fit_participants='|'.join(sorted(frame.iloc[ti].participant.unique())),
                                evaluation_participants='|'.join(sorted(validation.participant.unique()))))
                        event('fit_completed',task=task,fold=fold['fold'],inner=inner,context=context,estimator=estimator)
                pd.DataFrame(search).to_csv(out/'busqueda_interna.csv',index=False)
                print(f'{task} fold {fold["fold"]}/5 interno {inner}/3',flush=True)
            scores=pd.DataFrame(search); scores=scores.loc[scores.task.eq(task)&scores.fold.eq(fold['fold'])].groupby('candidate_id',as_index=False).score.mean()
            selected.extend(dict(task=task,fold=fold['fold'],**choice) for choice in select_candidates(scores,definitions[task]))
            selected.append(dict(task=task,fold=fold['fold'],scope='fixed_logistic',candidate_id='fixed_logistic',context=1,
                                 estimator='logistic_reference',strategy='early',weights=None,inner_score=None))
            write_json(out/'selecciones.json',selected)
    frozen=digest(out/'selecciones.json'); event('selection_frozen',sha256=frozen,inner_fits=inner_fits)
    artifacts=[]; predictions=[]; metrics=[]; people=[]; outer_fits=0
    for choice in selected:
        task=choice['task']; frame=frames[task]; spec=TASKS[task]; modalities=spec['modalities']; target=spec['target']
        fold=folds[task][choice['fold']-1]
        fit=frame.loc[frame.participant.isin(fold['fit'])].reset_index(drop=True)
        val=frame.loc[frame.participant.isin(fold['evaluation'])].reset_index(drop=True)
        x={m:causal_features(fit,cols,choice['context']) for m,cols in modalities.items()}
        for seed in protocol['seeds']:
            inputs={'early':np.column_stack(list(x.values()))} if choice['strategy']=='early' else x
            models={m:make_model(choice['estimator'],seed).fit(value,fit[target]) for m,value in inputs.items()}; outer_fits+=len(models)
            bundle=dict(definition=choice,modalities=modalities,models=models)
            name=f'{task}__fold{fold["fold"]}__{choice["scope"]}__{seed}'; path=out/'modelos'/f'{name}.joblib'
            joblib.dump(bundle,path,compress=3)
            prob=predict_bundle(bundle,val); np.testing.assert_array_equal(prob,predict_bundle(joblib.load(path),val))
            pred=np.asarray(CLASSES)[prob.argmax(axis=1)]
            identity=dict(model_id=name,task=task,fold=fold['fold'],scope=choice['scope'],seed=seed)
            artifacts.append(dict(**identity,path=path.relative_to(out).as_posix(),sha256=digest(path),definition=choice,
                train_participants=fold['fit'],evaluation_participants=fold['evaluation'],reload_verified=True))
            p=val[['source_row','participant','window_start_utc']].copy(); p['true']=val[target].to_numpy(); p['prediction']=pred
            for k,v in identity.items(): p[k]=v
            for i,c in enumerate(CLASSES): p['prob_'+c]=prob[:,i]
            predictions.append(p); metrics.append(dict(**identity,**metric_record(val,target,pred,'classification')))
            people.extend(dict(**identity,participant=p,score=s) for p,s in individual_scores(val,target,pred,'classification').items())
        event('outer_completed',task=task,fold=fold['fold'],scope=choice['scope'])
        write_json(out/'catalogo_modelos.json',artifacts)
    assert digest(out/'selecciones.json')==frozen
    pd.concat(predictions).to_csv(out/'predicciones_oof.csv.gz',index=False,compression='gzip')
    pd.DataFrame(metrics).to_csv(out/'metricas_folds.csv',index=False); pd.DataFrame(people).to_csv(out/'metricas_participantes.csv',index=False)
    write_json(out/'completo.json',dict(models=len(artifacts),inner_fits=inner_fits,outer_component_fits=outer_fits,
        protocol_sha256=digest(out/'protocolo.json'),selection_sha256=frozen,catalog_sha256=digest(out/'catalogo_modelos.json'),
        predictions_sha256=digest(out/'predicciones_oof.csv.gz'),validation_evaluated=False,test_evaluated=False))
    event('completed',models=len(artifacts),inner_fits=inner_fits,outer_component_fits=outer_fits)
    print(pd.DataFrame(people).groupby(['task','scope']).score.mean().to_string(),flush=True)


if __name__=='__main__':
    with threadpool_limits(limits=4): main()
