"""Evalua modelos congelados y explica dependencia de variables frente al baseline.

La seleccion procede solo de validation. Importancias en test son diagnostico post hoc.
"""
from __future__ import annotations
import json
from datetime import datetime, timezone
import joblib
import numpy as np
import pandas as pd

from temporales_core import (ROOT,OUT,STATIC,CLASSES,seed_all,digest,write_json,prepare_frame,history_indices,
    sequence_array,load_net,raw_predict,decode,metric_record,individual_scores)
from analisis_variables import shift_indices,bootstrap_mean
from baselines_estaticos import EEG,GSR,EYE,PUPIL


def difference(frame,target,a,b,kind):
    aa=individual_scores(frame,target,a,kind); bb=individual_scores(frame,target,b,kind)
    return np.array([aa[p]-bb[p] for p in sorted(aa)])


def main():
    seed_all(20260907)
    complete=json.loads((OUT/'entrenamiento_completo.json').read_text(encoding='utf-8'))
    assert digest(OUT/'catalogo_modelos.json')==complete['catalog_sha256']
    assert digest(OUT/'seleccion_antes_test.json')==complete['selection_sha256']
    config=json.loads((OUT/'protocolo.json').read_text(encoding='utf-8'))
    catalog=json.loads((OUT/'catalogo_modelos.json').read_text(encoding='utf-8'))
    selected=json.loads((OUT/'seleccion_antes_test.json').read_text(encoding='utf-8'))['models']
    baseline_catalog=json.loads((STATIC/'manifiesto.json').read_text(encoding='utf-8'))['final_models']
    baseline_validation=pd.read_csv(STATIC/'validacion_panel_congelado.csv')
    references=[]
    for task,sets in config['features'].items():
        for kind in ['classification','regression']:
            for subset in sets:
                candidates=baseline_validation.loc[baseline_validation.task.eq(task)&baseline_validation.kind.eq(kind)&
                    (baseline_validation.subset.eq(subset)|baseline_validation.model.str.startswith('dummy'))]
                best=candidates.sort_values(['macro_score','model'],ascending=[False,True]).iloc[0]
                references.append(dict(task=task,kind=kind,subset=subset,model=best.model,baseline_subset=best.subset))
    write_json(OUT/'referencias_estaticas_antes_test.json',dict(frozen_utc=datetime.now(timezone.utc).isoformat(),
        rule='best validation participant macro score, matched feature subset with dummy allowed',references=references))
    write_json(OUT/'protocolo_explicacion.json',dict(created_utc=datetime.now(timezone.utc).isoformat(),
        source_sha256=digest(__file__),repeats=5,seed=20260907,
        selected_models='best panel and best full by mean validation over seeds; primary seed only for explanations',
        scopes=['validation','test_post_hoc'],
        importance='circular raw-feature shifts within participant/recording/segment; rebuilt sequences; group modalities jointly',
        differential='temporal importance minus baseline importance = original gain minus perturbed gain',
        history_controls=['repeat_endpoint_in_past','reverse_past_keep_endpoint'],
        disclaimer='model dependence, not additive causal explanation; test importance not used for model or feature selection'))
    path=ROOT/'resultados/modelado/dataset_modelado.csv'
    assert digest(path)==config['dataset_sha256']
    data=pd.read_csv(path); data['source_row']=np.arange(len(data))
    data=data.loc[data.split.isin(['validation','test'])].copy()
    frames={(task,s):prepare_frame(data,task,config['targets'],s) for task in config['features'] for s in ['validation','test']}
    identities={key:history_indices(f,config['context_windows']) for key,f in frames.items()}
    baseline_cache={}; static_objects={}; static_metrics=[]
    for meta in baseline_catalog:
        bpath=STATIC/meta['path']; assert digest(bpath)==meta['sha256']
        obj=joblib.load(bpath)
        static_objects[(meta['task'],meta['kind'],meta['subset'],meta['model'])]=(obj,meta)
        for split in ['validation','test']:
            frame=frames[(meta['task'],split)]
            prediction=obj.predict(frame[meta['features']])
            key=(meta['task'],meta['kind'],meta['subset'],meta['model'],split)
            baseline_cache[key]=prediction
            lengths=identities[(meta['task'],split)][1]
            for scope,mask in [('all',np.ones(len(frame),dtype=bool)),('history_8',lengths==8)]:
                if mask.any():
                    static_metrics.append({k:meta[k] for k in ['task','kind','subset','model']}|
                        {'split':split,'scope':scope}|metric_record(frame.loc[mask].reset_index(drop=True),
                            meta['target'],prediction[mask],meta['kind']))
    pd.DataFrame(static_metrics).to_csv(OUT/'metricas_estaticos_mismas_ventanas.csv',index=False)
    def reference(task,kind,subset,split):
        r=next(r for r in references if r['task']==task and r['kind']==kind and r['subset']==subset)
        key=(task,kind,r['baseline_subset'],r['model'])
        return r,key,baseline_cache[(*key,split)]
    metric_rows=[]; prediction_frames=[]; paired=[]; coverage=[]; history_rows=[]; neural_full={}
    for (task,split),(idx,lengths) in identities.items():
        coverage.append(dict(task=task,split=split,rows=len(lengths),mean_history=float(lengths.mean()),
            singleton_fraction=float(np.mean(lengths==1)),full_history_fraction=float(np.mean(lengths==8))))
        if split=='test':
            frame=frames[(task,split)]
            frame[['source_row','participant','recording','segment_id','stimulus','window_start_utc']].assign(
                history_length=lengths,history_start_utc=frame.iloc[idx[:,0]].window_start_utc.to_numpy()).to_csv(
                OUT/f'secuencias_{task}_{split}.csv.gz',index=False,compression='gzip')
    for number,meta in enumerate(catalog,1):
        identity={k:meta[k] for k in ['task','kind','subset','architecture','seed']}
        model=load_net(meta); assert digest(OUT/meta['preprocessor'])==meta['preprocessor_sha256']
        prep=joblib.load(OUT/meta['preprocessor'])
        for split in ['validation','test']:
            frame=frames[(meta['task'],split)]; idx,lengths=identities[(meta['task'],split)]
            x=sequence_array(prep.transform(frame[meta['features']]),idx)
            raw=raw_predict(model,x,lengths); pred=decode(raw,meta['kind'])
            if meta['subset']=='full':
                neural_full[(meta['task'],meta['kind'],meta['architecture'],meta['seed'],split)]=pred
            for scope,mask in [('all',np.ones(len(frame),dtype=bool)),('history_8',lengths==8)]:
                if mask.any():
                    metric_rows.append(identity|dict(split=split,scope=scope)|metric_record(
                        frame.loc[mask].reset_index(drop=True),meta['target'],pred[mask],meta['kind']))
            saved=frame[['source_row','participant','window_start_utc']].copy()
            for k,v in identity.items(): saved[k]=v
            saved['split']=split; saved['history_length']=lengths
            saved['actual']=frame[meta['target']]; saved['predicted']=pred
            if meta['kind']=='classification':
                probs=np.exp(raw-raw.max(axis=1,keepdims=True));probs/=probs.sum(axis=1,keepdims=True)
                for i,c in enumerate(CLASSES): saved['prob_'+c]=probs[:,i]
            prediction_frames.append(saved)
            for reference_scope,reference_subset in [('matched',meta['subset']),('full','full')]:
                ref,_,bp=reference(meta['task'],meta['kind'],reference_subset,split)
                delta=difference(frame,meta['target'],pred,bp,meta['kind'])
                for p,v in zip(sorted(frame.participant.unique()),delta):
                    paired.append(identity|dict(split=split,reference_scope=reference_scope,baseline=ref['model'],
                        baseline_subset=ref['baseline_subset'],participant=p,gain=float(v)))
        if number%8==0: print(f'evaluados {number}/{len(catalog)}',flush=True)
    for key,pred in neural_full.items():
        task,kind,architecture,seed,split=key
        if architecture=='MLP_current': continue
        bp=neural_full[(task,kind,'MLP_current',seed,split)]
        frame=frames[(task,split)];target=config['targets'][task][1 if kind=='classification' else 0]
        delta=difference(frame,target,pred,bp,kind)
        for p,v in zip(sorted(frame.participant.unique()),delta):
            paired.append(dict(task=task,kind=kind,subset='full',architecture=architecture,seed=seed,split=split,
                reference_scope='MLP_current_full',baseline='MLP_current',baseline_subset='full',participant=p,gain=float(v)))
    pd.DataFrame(metric_rows).to_csv(OUT/'metricas_temporales.csv',index=False)
    pd.concat(prediction_frames,ignore_index=True).to_csv(OUT/'predicciones_temporales.csv.gz',index=False,compression='gzip')
    paired_frame=pd.DataFrame(paired)
    paired_frame.to_csv(OUT/'ganancias_por_participante.csv',index=False)
    summary=[]
    grouping=['task','kind','subset','architecture','split','reference_scope','baseline','baseline_subset']
    for key,group in paired_frame.groupby(grouping):
        values=group.groupby('participant').gain.mean().to_numpy()
        low,high=bootstrap_mean(values)
        summary.append(dict(zip(grouping,key))|dict(mean_gain=float(values.mean()),low=low,high=high,
            positive_participants=int((values>0).sum()),participants=len(values),seeds=group.seed.nunique()))
    pd.DataFrame(summary).to_csv(OUT/'ganancias_vs_baseline.csv',index=False)
    pd.DataFrame(coverage).to_csv(OUT/'cobertura_evaluacion.csv',index=False)
    explanation_models=[]
    seen=set()
    for choice in selected:
        key=(choice['task'],choice['kind'],choice['subset'],choice['architecture'])
        if key not in seen:
            explanation_models.append(next(m for m in catalog if all(m[k]==choice[k] for k in ['task','kind','subset','architecture']) and m['seed']==config['seeds'][0]))
            seen.add(key)
    importance_rows=[]; importance_subjects=[]
    for meta in explanation_models:
        identity={k:meta[k] for k in ['task','kind','subset','architecture','seed']}
        model=load_net(meta);prep=joblib.load(OUT/meta['preprocessor'])
        columns=meta['features']
        groups={c:[c] for c in columns}
        groups.update({'modalidad:'+name:[c for c in cols if c in columns]
                       for name,cols in [('EEG',EEG),('GSR',GSR),('Eye',EYE),('Pupil',PUPIL)]})
        groups={k:v for k,v in groups.items() if v}
        for split in ['validation','test']:
            print(f'explicacion {identity} {split}',flush=True)
            frame=frames[(meta['task'],split)];idx,lengths=identities[(meta['task'],split)]
            x=sequence_array(prep.transform(frame[columns]),idx)
            original=decode(raw_predict(model,x,lengths),meta['kind'])
            ref,bkey,bp=reference(meta['task'],meta['kind'],meta['subset'],split)
            static,static_meta=static_objects[bkey]
            gain=difference(frame,meta['target'],original,bp,meta['kind'])
            # Solo diagnostico: alterar pasado manteniendo endpoint y longitud.
            for variant in ['repeat_endpoint_in_past','reverse_past_keep_endpoint']:
                altered=x.copy()
                for i,n in enumerate(lengths):
                    if variant=='repeat_endpoint_in_past': altered[i,:n]=x[i,n-1]
                    else: altered[i,:n-1]=x[i,:n-1][::-1]
                changed=decode(raw_predict(model,altered,lengths),meta['kind'])
                drop=difference(frame,meta['target'],original,changed,meta['kind'])
                low,high=bootstrap_mean(drop)
                history_rows.append(identity|dict(split=split,control=variant,importance=float(drop.mean()),low=low,high=high,
                                                   gain_before=float(gain.mean()),gain_after=float((gain-drop).mean())))
            permutations=[shift_indices(frame,20260907+r) for r in range(5)]
            for feature,features in groups.items():
                drops=[];bdrops=[]
                for perm in permutations:
                    changed_frame=frame.copy()
                    changed_frame.loc[:,features]=frame.iloc[perm][features].to_numpy()
                    altered=sequence_array(prep.transform(changed_frame[columns]),idx)
                    temporal=decode(raw_predict(model,altered,lengths),meta['kind'])
                    baseline=static.predict(changed_frame[static_meta['features']])
                    drops.append(difference(frame,meta['target'],original,temporal,meta['kind']))
                    bdrops.append(difference(frame,meta['target'],bp,baseline,meta['kind']))
                td=np.mean(drops,axis=0);bd=np.mean(bdrops,axis=0);differential=td-bd
                lo,hi=bootstrap_mean(differential);tlo,thi=bootstrap_mean(td)
                importance_rows.append(identity|dict(split=split,feature=feature,baseline=ref['model'],
                    temporal_importance=float(td.mean()),temporal_low=tlo,temporal_high=thi,
                    baseline_importance=float(bd.mean()),differential_importance=float(differential.mean()),
                    differential_low=lo,differential_high=hi,positive_participants=int((differential>0).sum()),
                    participants=len(td),gain_before=float(gain.mean()),gain_after=float((gain-differential).mean()),repeats=5))
                for person,t,b in zip(sorted(frame.participant.unique()),td,bd):
                    importance_subjects.append(identity|dict(split=split,feature=feature,participant=person,
                        temporal_importance=float(t),baseline_importance=float(b),differential_importance=float(t-b)))
            pd.DataFrame(importance_rows).to_csv(OUT/'importancia_vs_baseline.csv',index=False)
            pd.DataFrame(history_rows).to_csv(OUT/'dependencia_del_historial.csv',index=False)
    pd.DataFrame(importance_subjects).to_csv(OUT/'importancia_vs_baseline_por_participante.csv',index=False)
    write_json(OUT/'evaluacion_completa.json',dict(completed_utc=datetime.now(timezone.utc).isoformat(),
        source_sha256=digest(__file__),evaluated_models=len(catalog),explained_models=len(explanation_models),
        importance_rows=len(importance_rows),test_used_for_selection=False,
        selection_sha256=digest(OUT/'seleccion_antes_test.json'),references_sha256=digest(OUT/'referencias_estaticas_antes_test.json')))
    print('EVALUACION COMPLETA',flush=True)


if __name__=='__main__': main()
