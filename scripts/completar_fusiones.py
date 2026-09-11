"""Completa selecciones congeladas; Extra Trees predice en un hilo para recarga exacta."""
import argparse
import json
import shutil
from datetime import datetime,timezone
import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits
from explorar_fusiones import OUT,TASKS,causal_features,make_model,predict_bundle
from temporales_core import ROOT,CLASSES,digest,write_json,metric_record,individual_scores

FINAL=ROOT/'resultados/fusiones_10-09-2026_completa'


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--input',default=str(OUT.relative_to(ROOT)))
    parser.add_argument('--output',default=str(FINAL.relative_to(ROOT))); args=parser.parse_args()
    source=ROOT/args.input; out=ROOT/args.output
    protocol=json.loads((source/'protocolo.json').read_text(encoding='utf-8'))
    selected=json.loads((source/'selecciones.json').read_text(encoding='utf-8')); assert len(selected)==60
    for n,sha in protocol['sources'].items(): assert digest(ROOT/'scripts'/n)==sha
    out.mkdir(parents=True,exist_ok=False); (out/'modelos').mkdir()
    for name in ['protocolo.json','selecciones.json','busqueda_interna.csv','bitacora.jsonl','pruebas.txt']:
        shutil.copyfile(source/name,out/name)
    correction=dict(utc=datetime.now(timezone.utc).isoformat(),source=source.relative_to(ROOT).as_posix(),
        issue='Exact reload assertion failed under parallel Extra Trees prediction; observed max absolute probability difference 2.22044605e-16',
        correction='Preserve frozen inner selections; refit outer pipelines; set Extra Trees n_jobs=1 before saving/predicting',
        failed_run_preserved=True,selection_sha256=digest(out/'selecciones.json'),source_sha256=digest(__file__),
        inner_search_repeated=False,outer_results_used_for_selection=False)
    write_json(source/'interrupcion.json',correction); write_json(out/'reanudacion.json',correction)
    def event(stage,**kwargs):
        with (out/'bitacora.jsonl').open('a',encoding='utf-8') as f:
            f.write(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),stage=stage,**kwargs),ensure_ascii=False)+'\n')
    event('resumed',correction='Extra Trees prediction single thread; frozen selections retained')
    dataset=ROOT/'resultados/modelado/dataset_modelado.csv'; assert digest(dataset)==protocol['dataset_sha256']
    data=pd.read_csv(dataset); data['source_row']=np.arange(len(data)); data=data.loc[data.split.eq('train')]
    frames={t:data.loc[data[s['target']].notna()].sort_values(['participant','recording','window_start_utc']).reset_index(drop=True)
            for t,s in TASKS.items()}; del data
    artifacts=[]; predictions=[]; metrics=[]; people=[]; outer_fits=0
    for choice in selected:
        task=choice['task']; frame=frames[task]; spec=TASKS[task]; modalities=spec['modalities']; target=spec['target']
        fold=protocol['folds'][task][choice['fold']-1]
        fit=frame.loc[frame.participant.isin(fold['fit'])].reset_index(drop=True)
        val=frame.loc[frame.participant.isin(fold['evaluation'])].reset_index(drop=True)
        x={m:causal_features(fit,cols,choice['context']) for m,cols in modalities.items()}
        for seed in protocol['seeds']:
            inputs={'early':np.column_stack(list(x.values()))} if choice['strategy']=='early' else x
            models={m:make_model(choice['estimator'],seed).fit(value,fit[target]) for m,value in inputs.items()}; outer_fits+=len(models)
            for model in models.values():
                if hasattr(model.named_steps['model'],'n_jobs'): model.named_steps['model'].set_params(n_jobs=1)
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
        print(f'{task} fold {fold["fold"]} {choice["scope"]} verificado',flush=True)
    assert digest(out/'selecciones.json')==correction['selection_sha256']
    pd.concat(predictions).to_csv(out/'predicciones_oof.csv.gz',index=False,compression='gzip')
    pd.DataFrame(metrics).to_csv(out/'metricas_folds.csv',index=False); pd.DataFrame(people).to_csv(out/'metricas_participantes.csv',index=False)
    write_json(out/'completo.json',dict(models=len(artifacts),inner_fits=630,outer_component_fits=outer_fits,
        protocol_sha256=digest(out/'protocolo.json'),selection_sha256=digest(out/'selecciones.json'),catalog_sha256=digest(out/'catalogo_modelos.json'),
        predictions_sha256=digest(out/'predicciones_oof.csv.gz'),resumption_sha256=digest(out/'reanudacion.json'),
        validation_evaluated=False,test_evaluated=False))
    event('completed',models=len(artifacts),inner_fits=630,outer_component_fits=outer_fits)
    print(pd.DataFrame(people).groupby(['task','scope']).score.mean().to_string(),flush=True)


if __name__=='__main__':
    with threadpool_limits(limits=4): main()
