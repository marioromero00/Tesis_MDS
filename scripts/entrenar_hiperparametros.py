"""Grilla anidada por persona de modelos nuevos e hiperparametros."""
import argparse
import json
import platform
from datetime import datetime,timezone
import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import GroupKFold
from threadpoolctl import threadpool_limits
from hiperparametros_core import TARGET,MODALITIES,SCOPES,grid,feature_cache,fit_bundle,raw_scores,predict,choose
from avanzados_core import sample_weights
from control_historial import nested_folds
from optimizar_historial import smooth
from temporales_core import ROOT,CLASSES,digest,write_json,metric_record,individual_scores
from baselines_estaticos import validate_partition

OUT=ROOT/'resultados/hiperparametros_11-09-2026'


def load_train():
    dataset=ROOT/'resultados/modelado/dataset_modelado.csv'
    partition=ROOT/'resultados/modelado/particion_participantes.csv'
    previous=json.loads((ROOT/'resultados/avanzados_11-09-2026/protocolo.json').read_text(encoding='utf-8'))
    assert digest(dataset)==previous['dataset_sha256'] and digest(partition)==previous['partition_sha256']
    data=pd.read_csv(dataset); data['source_row']=np.arange(len(data))
    validate_partition(data,pd.read_csv(partition))
    return data.loc[data.split.eq('train')&data[TARGET].notna()].sort_values(['participant','recording','window_start_utc']).reset_index(drop=True)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',default=str(OUT.relative_to(ROOT)))
    out=ROOT/parser.parse_args().output; out.mkdir(parents=True,exist_ok=False)
    for name in ['modelos','predicciones_internas']: (out/name).mkdir()
    train=load_train(); folds=nested_folds(train); definitions=grid()
    protocol=dict(created_utc=datetime.now(timezone.utc).isoformat(),task='arousal',target=TARGET,
        modalities=MODALITIES,grid=definitions,folds=folds,scopes=SCOPES,seeds=[20260911,20260912],
        inner_seed=20260911,inner_folds=3,smoothing=[1,4],base_candidates=len(definitions),decision_candidates=2*len(definitions),
        primary='all selected internally vs previous geometric fusion; each family and pooled fusion are secondary',
        selection='mean participant BA over 3 inner folds; ties by candidate_id; all selections frozen before outer evaluation',
        svm_scores='softmax of OVR decision scores, not calibrated probabilities; no SVC internal probability cross-validation',
        scope='exploratory adaptive follow-up on repeatedly used train; no independent confirmation',
        validation_evaluated=False,test_evaluated=False,
        dataset_sha256=digest(ROOT/'resultados/modelado/dataset_modelado.csv'),
        partition_sha256=digest(ROOT/'resultados/modelado/particion_participantes.csv'),
        sources={n:digest(ROOT/'scripts'/n) for n in ['entrenar_hiperparametros.py','hiperparametros_core.py',
            'avanzados_core.py','explorar_fusiones.py','optimizar_historial.py','temporales_core.py','control_historial.py','baselines_estaticos.py']},
        requirements_sha256=digest(ROOT/'requirements_avanzados.txt'),
        versions=dict(python=platform.python_version(),sklearn=sklearn.__version__,numpy=np.__version__,pandas=pd.__version__))
    write_json(out/'protocolo.json',protocol)
    def log(stage,**kw):
        with (out/'bitacora.jsonl').open('a',encoding='utf-8') as f:
            f.write(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),stage=stage,**kw),ensure_ascii=False)+'\n')
    cache=feature_cache(train); attempts=[]; selections=[]; inner_catalog=[]; warnings=[]
    for fold in folds:
        outer=np.flatnonzero(train.participant.isin(fold['fit'])); fitting=train.iloc[outer]
        splitter=GroupKFold(n_splits=3,shuffle=True,random_state=protocol['inner_seed']+fold['fold'])
        for inner,(ii,vv) in enumerate(splitter.split(fitting,groups=fitting.participant),1):
            ti,vi=outer[ii],outer[vv]; fit=train.iloc[ti].reset_index(drop=True); val=train.iloc[vi].reset_index(drop=True)
            truth=val[TARGET].map({c:i for i,c in enumerate(CLASSES)}).to_numpy(int)
            weights=sample_weights(val,'participant'); arrays=dict(source_row=val.source_row.to_numpy(),true=truth)
            for index,definition in enumerate(definitions):
                identity=dict(fold=fold['fold'],inner=inner,base_id=definition['base_id'])
                log('fit_started',**identity)
                bundle=fit_bundle(cache,ti,fit,definition,protocol['seeds'][0])
                raw=raw_scores(bundle,cache,vi); arrays[f'm{index}']=raw
                warnings.extend(dict(**identity,**w) for w in bundle['warnings'])
                for window in protocol['smoothing']:
                    scores=smooth(val,raw,window); score=float(np.average(scores.argmax(axis=1)==truth,weights=weights))
                    attempts.append(dict(**identity,family=definition['family'],context=definition['context'],
                        smoothing=window,candidate_id=f'{definition["base_id"]}_smooth{window}',score=score))
                log('fit_completed',**identity,components=len(bundle['components']),warnings=bundle['warnings'])
            path=out/'predicciones_internas'/f'fold{fold["fold"]}_inner{inner}.npz'; np.savez_compressed(path,**arrays)
            inner_catalog.append(dict(fold=fold['fold'],inner=inner,path=path.relative_to(out).as_posix(),sha256=digest(path),
                train_participants=sorted(fit.participant.unique()),evaluation_participants=sorted(val.participant.unique())))
            pd.DataFrame(attempts).to_csv(out/'todos_los_intentos.csv',index=False)
            write_json(out/'catalogo_interno.json',inner_catalog); write_json(out/'advertencias.json',warnings)
            print(f'Fold {fold["fold"]}/5, interno {inner}/3: {len(definitions)} modelos y {2*len(definitions)} decisiones',flush=True)
        scores=pd.DataFrame(attempts); scores=scores.loc[scores.fold.eq(fold['fold'])]
        scores=scores.groupby(['candidate_id','base_id','family','context','smoothing'],as_index=False).score.mean()
        for scope in SCOPES:
            winner=choose(scores,scope)
            definition=next(d for d in definitions if d['base_id']==winner.base_id)
            selections.append(dict(fold=fold['fold'],scope=scope,candidate_id=winner.candidate_id,
                definition=definition,smoothing=int(winner.smoothing),inner_score=float(winner.score)))
        write_json(out/'selecciones.json',selections)
    frozen=digest(out/'selecciones.json'); log('selection_frozen',sha256=frozen)
    catalog=[]; rows=[]; metrics=[]; people=[]
    for choice in selections:
        fold=folds[choice['fold']-1]; ti=np.flatnonzero(train.participant.isin(fold['fit'])); vi=np.flatnonzero(train.participant.isin(fold['evaluation']))
        fit=train.iloc[ti].reset_index(drop=True); val=train.iloc[vi].reset_index(drop=True)
        val_cache={k:v[vi] for k,v in cache.items()}
        for seed in protocol['seeds']:
            bundle=fit_bundle(cache,ti,fit,choice['definition'],seed); bundle['smoothing']=choice['smoothing']
            name=f'fold{fold["fold"]}_{choice["scope"]}_{seed}'; path=out/'modelos'/f'{name}.joblib'
            joblib.dump(bundle,path,compress=3); score=predict(bundle,val,val_cache)
            np.testing.assert_array_equal(score,predict(joblib.load(path),val,val_cache))
            pred=np.asarray(CLASSES)[score.argmax(axis=1)]; identity=dict(model_id=name,fold=fold['fold'],scope=choice['scope'],seed=seed)
            catalog.append(dict(**identity,choice=choice,path=path.relative_to(out).as_posix(),sha256=digest(path),
                train_participants=fold['fit'],evaluation_participants=fold['evaluation'],warnings=bundle['warnings']))
            p=val[['source_row','participant','window_start_utc']].copy(); p['true']=val[TARGET].to_numpy(); p['prediction']=pred
            for k,v in identity.items(): p[k]=v
            for i,c in enumerate(CLASSES): p['score_'+c]=score[:,i]
            rows.append(p); metrics.append(dict(**identity,**metric_record(val,TARGET,pred,'classification')))
            people.extend(dict(**identity,participant=p,score=s) for p,s in individual_scores(val,TARGET,pred,'classification').items())
        write_json(out/'catalogo_modelos.json',catalog); log('outer_completed',fold=fold['fold'],scope=choice['scope'])
        print(f'Evaluado fold {fold["fold"]}: {choice["scope"]}',flush=True)
    assert digest(out/'selecciones.json')==frozen
    pd.concat(rows).to_csv(out/'predicciones_oof.csv.gz',index=False,compression='gzip')
    pd.DataFrame(metrics).to_csv(out/'metricas_folds.csv',index=False); pd.DataFrame(people).to_csv(out/'metricas_participantes.csv',index=False)
    write_json(out/'completo.json',dict(models=len(catalog),inner_bundles=15*len(definitions),
        protocol_sha256=digest(out/'protocolo.json'),selection_sha256=frozen,
        catalog_sha256=digest(out/'catalogo_modelos.json'),predictions_sha256=digest(out/'predicciones_oof.csv.gz'),
        validation_evaluated=False,test_evaluated=False))
    log('completed',models=len(catalog)); print(pd.DataFrame(people).groupby('scope').score.mean().to_string(),flush=True)


if __name__=='__main__':
    with threadpool_limits(limits=4): main()
