"""Busqueda agrupada anidada; congela elecciones antes de evaluar externamente."""
import json
from datetime import datetime,timezone
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold
from threadpoolctl import threadpool_limits
from multiescala_core import grid,feature_cache,fit,raw_scores,predict
from hiperparametros_core import TARGET,FULL
from entrenar_hiperparametros import load_train
from control_historial import nested_folds
from avanzados_core import sample_weights
from optimizar_historial import smooth
from temporales_core import ROOT,CLASSES,digest,write_json,metric_record,individual_scores

OUT=ROOT/'resultados/multiescala_11-09-2026'


def main():
    OUT.mkdir(exist_ok=False)
    for name in ['modelos','internos']: (OUT/name).mkdir()
    train=load_train(); folds=nested_folds(train); definitions=grid(); seeds=[20260911,20260912]
    protocol=dict(created_utc=datetime.now(timezone.utc).isoformat(),target=TARGET,features=FULL,folds=folds,grid=definitions,
        smoothing=[1,8,32],seeds=seeds,inner_seed=20260912,inner_folds=3,scopes=['all','ridge','rbf','trees'],primary='all',
        weighting='equal participant and observed class',selection='mean BA per participant across three inner folds; ties by candidate_id',
        temporal='causal 4/16/64 windows; reset participant/recording/gap; delayed4 repeats first available representation for first four rows',
        sources={str(p.relative_to(ROOT)):digest(p) for p in [ROOT/'scripts/multiescala_core.py',ROOT/'scripts/entrenar_multiescala.py',
            ROOT/'scripts/persistencia_core.py',ROOT/'scripts/temporales_core.py',ROOT/'scripts/avanzados_core.py',ROOT/'scripts/optimizar_historial.py',
            ROOT/'scripts/control_historial.py',ROOT/'scripts/entrenar_hiperparametros.py',ROOT/'scripts/hiperparametros_core.py',
            ROOT/'resultados/modelado/dataset_modelado.csv',ROOT/'resultados/modelado/particion_participantes.csv']},
        validation_evaluated=False,test_evaluated=False,scope='adaptive exploratory training cohort; target 0.5 not guaranteed')
    write_json(OUT/'protocolo.json',protocol)
    def log(stage,**kwargs):
        with (OUT/'bitacora.jsonl').open('a',encoding='utf-8') as f:
            f.write(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),stage=stage,**kwargs))+'\n')
    cache=feature_cache(train); attempts=[]; selections=[]; catalog=[]
    for fold in folds:
        outer=np.flatnonzero(train.participant.isin(fold['fit'])); fitting=train.iloc[outer]
        splitter=GroupKFold(n_splits=3,shuffle=True,random_state=protocol['inner_seed']+fold['fold'])
        for inner,(ii,vv) in enumerate(splitter.split(fitting,groups=fitting.participant),1):
            ti,vi=outer[ii],outer[vv]; f=train.iloc[ti].reset_index(drop=True); v=train.iloc[vi].reset_index(drop=True)
            assert set(f.participant).isdisjoint(v.participant)
            y=v[TARGET].to_numpy(); weight=sample_weights(v,'participant'); arrays=dict(source_row=v.source_row.to_numpy())
            for i,d in enumerate(definitions):
                identity=dict(fold=fold['fold'],inner=inner,base_id=d['base_id'])
                log('fit_started',**identity)
                bundle=fit(cache[d['representation']][ti],f,d,seeds[0]); raw=raw_scores(bundle,cache[d['representation']][vi]); arrays[f'm{i}']=raw
                for w in protocol['smoothing']:
                    pred=np.asarray(CLASSES)[smooth(v,raw,w).argmax(axis=1)]
                    attempts.append(dict(**identity,family=d['family'],representation=d['representation'],smoothing=w,
                        candidate_id=f'{d["base_id"]}_s{w}',score=float(np.average(pred==y,weights=weight))))
                log('fit_completed',**identity)
            path=OUT/'internos'/f'fold{fold["fold"]}_inner{inner}.npz'; np.savez_compressed(path,**arrays)
            catalog.append(dict(fold=fold['fold'],inner=inner,path=path.relative_to(OUT).as_posix(),sha256=digest(path),
                train_participants=sorted(f.participant.unique()),evaluation_participants=sorted(v.participant.unique())))
            pd.DataFrame(attempts).to_csv(OUT/'intentos.csv',index=False); write_json(OUT/'catalogo_interno.json',catalog)
            print(f'Multiescala interno {fold["fold"]}/5 - {inner}/3: 24 ajustes completos',flush=True)
        scores=pd.DataFrame(attempts); scores=scores.loc[scores.fold.eq(fold['fold'])].groupby(['candidate_id','base_id','family','smoothing'],as_index=False).score.mean()
        for scope in protocol['scopes']:
            eligible=scores if scope=='all' else scores.loc[scores.family.eq(scope)]
            winner=eligible.sort_values(['score','candidate_id'],ascending=[False,True]).iloc[0]
            selections.append(dict(fold=fold['fold'],scope=scope,definition=next(d for d in definitions if d['base_id']==winner.base_id),
                smoothing=int(winner.smoothing),candidate_id=winner.candidate_id,inner_score=float(winner.score)))
    write_json(OUT/'selecciones.json',selections); frozen=digest(OUT/'selecciones.json'); log('selection_frozen',sha256=frozen)
    rows=[]; models=[]; metrics=[]; people=[]
    for choice in selections:
        fold=folds[choice['fold']-1]; ti=np.flatnonzero(train.participant.isin(fold['fit'])); vi=np.flatnonzero(train.participant.isin(fold['evaluation']))
        f=train.iloc[ti].reset_index(drop=True); v=train.iloc[vi].reset_index(drop=True); d=choice['definition']
        for seed in seeds:
            identity=dict(model_id=f'fold{fold["fold"]}_{choice["scope"]}_{seed}',fold=fold['fold'],scope=choice['scope'],seed=seed)
            log('outer_fit_started',**identity)
            bundle=fit(cache[d['representation']][ti],f,d,seed); bundle['smoothing']=choice['smoothing']
            path=OUT/'modelos'/f'{identity["model_id"]}.joblib'; joblib.dump(bundle,path,compress=3)
            proba=smooth(v,raw_scores(bundle,cache[d['representation']][vi]),choice['smoothing'])
            np.testing.assert_array_equal(proba,predict(joblib.load(path),v))
            pred=np.asarray(CLASSES)[proba.argmax(axis=1)]; p=v[['source_row','participant','window_start_utc']].copy()
            p['true']=v[TARGET].to_numpy(); p['prediction']=pred
            for k,value in identity.items(): p[k]=value
            for i,c in enumerate(CLASSES): p['prob_'+c]=proba[:,i]
            rows.append(p); models.append(dict(**identity,path=path.relative_to(OUT).as_posix(),sha256=digest(path),choice=choice,
                train_participants=fold['fit'],evaluation_participants=fold['evaluation']))
            metrics.append(dict(**identity,**metric_record(v,TARGET,pred,'classification')))
            people.extend(dict(**identity,participant=p,score=s) for p,s in individual_scores(v,TARGET,pred,'classification').items())
            log('outer_fit_completed',**identity)
        write_json(OUT/'catalogo_modelos.json',models); print(f'Multiescala externo {fold["fold"]}/5: {choice["scope"]}',flush=True)
    pd.concat(rows).to_csv(OUT/'predicciones_oof.csv.gz',index=False,compression='gzip')
    pd.DataFrame(metrics).to_csv(OUT/'metricas_folds.csv',index=False); pd.DataFrame(people).to_csv(OUT/'metricas_participantes.csv',index=False)
    assert digest(OUT/'selecciones.json')==frozen
    write_json(OUT/'completo.json',dict(models=len(models),predictions=sum(map(len,rows)),inner_fits=360,inner_scores=len(attempts),
        selection_sha256=frozen,completed_utc=datetime.now(timezone.utc).isoformat(),validation_evaluated=False,test_evaluated=False))
    print(pd.DataFrame(people).groupby('scope').score.mean().to_string(),flush=True)


if __name__=='__main__':
    with threadpool_limits(limits=2): main()
