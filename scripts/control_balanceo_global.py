"""Comparador global predeclarado antes de evaluar externamente la busqueda avanzada."""
import json
from datetime import datetime,timezone
import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits
from entrenar_avanzados import OUT,choose
from avanzados_core import TARGET,fit_bundle,inputs,predict
from temporales_core import ROOT,CLASSES,digest,write_json,metric_record,individual_scores


def main():
    protocol=json.loads((OUT/'protocolo.json').read_text(encoding='utf-8'))
    plan=json.loads((OUT/'control_global_plan.json').read_text(encoding='utf-8'))
    events=[json.loads(line) for line in (OUT/'bitacora.jsonl').read_text(encoding='utf-8').splitlines()]
    first=min(e['utc'] for e in events if e['stage']=='outer_completed')
    assert plan['created_utc']<first and not plan['outer_evaluation_started']
    out=OUT/'control_global'; out.mkdir(exist_ok=False); (out/'modelos').mkdir()
    search=pd.read_csv(OUT/'todos_los_intentos.csv'); fields=['candidate_id','base_id','panel','context','family','weighting','smoothing','low_bias','high_bias']
    choices=[]
    for fold in protocol['folds']:
        group=search.loc[search.fold.eq(fold['fold'])&search.weighting.eq('global')].groupby(fields,as_index=False).score.mean()
        w=choose(group,'all')
        choices.append(dict(fold=fold['fold'],scope='global',**{k:w[k].item() if hasattr(w[k],'item') else w[k] for k in fields},inner_score=float(w.score)))
    write_json(out/'selecciones.json',choices); frozen=digest(out/'selecciones.json')
    write_json(out/'protocolo.json',dict(source_sha256=digest(__file__),core_sha256=digest(ROOT/'scripts/avanzados_core.py'),
        plan_sha256=digest(OUT/'control_global_plan.json'),selection_sha256=frozen,
        created_utc=datetime.now(timezone.utc).isoformat(),validation_evaluated=False,test_evaluated=False))
    dataset=ROOT/'resultados/modelado/dataset_modelado.csv'; assert digest(dataset)==protocol['dataset_sha256']
    data=pd.read_csv(dataset); data['source_row']=np.arange(len(data)); train=data.loc[data.split.eq('train')&data[TARGET].notna()].sort_values(['participant','recording','window_start_utc']).reset_index(drop=True); del data
    artifacts=[]; predictions=[]; metrics=[]; people=[]
    for choice in choices:
        fold=protocol['folds'][choice['fold']-1]; fit=train.loc[train.participant.isin(fold['fit'])].reset_index(drop=True)
        val=train.loc[train.participant.isin(fold['evaluation'])].reset_index(drop=True)
        x=inputs(fit,choice['panel'],choice['context'])
        for seed in protocol['seeds']:
            bundle=fit_bundle(x,fit,choice['family'],'global',seed); bundle['choice']=choice
            name=f'fold{fold["fold"]}__global__{seed}'; path=out/'modelos'/f'{name}.joblib'; joblib.dump(bundle,path,compress=3)
            probability=predict(bundle,val); np.testing.assert_array_equal(probability,predict(joblib.load(path),val))
            pred=np.asarray(CLASSES)[probability.argmax(axis=1)]; ident=dict(model_id=name,fold=fold['fold'],scope='global',seed=seed)
            artifacts.append(dict(**ident,choice=choice,path=path.relative_to(out).as_posix(),sha256=digest(path),train_participants=fold['fit'],evaluation_participants=fold['evaluation'],reload_verified=True))
            p=val[['source_row','participant','window_start_utc']].copy(); p['true']=val[TARGET].to_numpy(); p['prediction']=pred
            for k,v in ident.items(): p[k]=v
            for i,c in enumerate(CLASSES): p['prob_'+c]=probability[:,i]
            predictions.append(p); metrics.append(dict(**ident,**metric_record(val,TARGET,pred,'classification')))
            people.extend(dict(**ident,participant=p,score=s) for p,s in individual_scores(val,TARGET,pred,'classification').items())
        print(f'Control global fold {fold["fold"]} completado',flush=True)
    write_json(out/'catalogo_modelos.json',artifacts); pd.concat(predictions).to_csv(out/'predicciones_oof.csv.gz',index=False,compression='gzip')
    pd.DataFrame(metrics).to_csv(out/'metricas_folds.csv',index=False); pd.DataFrame(people).to_csv(out/'metricas_participantes.csv',index=False)
    write_json(out/'completo.json',dict(models=10,selection_sha256=frozen,predictions_sha256=digest(out/'predicciones_oof.csv.gz'),catalog_sha256=digest(out/'catalogo_modelos.json'),validation_evaluated=False,test_evaluated=False))


if __name__=='__main__':
    with threadpool_limits(limits=4): main()
