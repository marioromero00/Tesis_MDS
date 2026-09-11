"""Busqueda anidada de boosting, ordinalidad, pesos por persona y decision."""
import argparse
import itertools
import json
import platform
from datetime import datetime,timezone
import catboost
import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import GroupKFold
from threadpoolctl import threadpool_limits
from avanzados_core import PANELS,TARGET,inputs,sample_weights,fit_bundle,raw_probabilities,adjust,predict
from control_historial import nested_folds
from optimizar_historial import smooth
from temporales_core import ROOT,CLASSES,digest,write_json,metric_record,individual_scores
from baselines_estaticos import validate_partition

OUT=ROOT/'resultados/avanzados_11-09-2026'


def model_grid():
    return [dict(base_id=f'{panel}__{context}__{family}__{weighting}',panel=panel,context=context,family=family,weighting=weighting)
            for panel,context,family,weighting in itertools.product(PANELS,[1,8],['logistic','ordinal','catboost'],['global','participant'])]


def choose(scores,scope):
    eligible=scores
    if scope=='unadjusted': eligible=scores.loc[scores.smoothing.eq(1)&scores.low_bias.eq(0)&scores.high_bias.eq(0)]
    elif scope=='participant': eligible=scores.loc[scores.weighting.eq('participant')]
    elif scope=='ordinal': eligible=scores.loc[scores.family.eq('ordinal')]
    elif scope=='catboost': eligible=scores.loc[scores.family.eq('catboost')]
    elif scope!='all': raise ValueError(scope)
    return eligible.sort_values(['score','candidate_id'],ascending=[False,True]).iloc[0]


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',default=str(OUT.relative_to(ROOT)))
    args=parser.parse_args(); out=ROOT/args.output; out.mkdir(parents=True,exist_ok=False)
    for name in ['modelos','predicciones_internas']: (out/name).mkdir()
    dataset=ROOT/'resultados/modelado/dataset_modelado.csv'; partition=ROOT/'resultados/modelado/particion_participantes.csv'
    old=json.loads((ROOT/'resultados/fusiones_10-09-2026_completa/protocolo.json').read_text(encoding='utf-8'))
    assert digest(dataset)==old['dataset_sha256'] and digest(partition)==old['partition_sha256']
    data=pd.read_csv(dataset); data['source_row']=np.arange(len(data)); validate_partition(data,pd.read_csv(partition))
    train=data.loc[data.split.eq('train')&data[TARGET].notna()].sort_values(['participant','recording','window_start_utc']).reset_index(drop=True)
    del data
    folds=nested_folds(train); grid=model_grid()
    protocol=dict(created_utc=datetime.now(timezone.utc).isoformat(),task='arousal',target=TARGET,panels=PANELS,base_grid=grid,
        folds=folds,seeds=[20260911,20260912],biases=[-.3,0.,.3],smoothing=[1,4],inner_folds=3,
        scopes=['all','unadjusted','participant','ordinal','catboost'],candidates=432,
        primary='all selected internally vs previous late geometric fusion; other scopes are secondary and not selected by outer scores',
        weighting='global class inverse counts or inverse participant-class count divided by number of classes present in person; normalized mean one',
        ordinal='two weighted binary logistic models P(y>=medio), P(y>=alto); project violations by averaging cumulative probabilities',
        decision='multiply smoothed probabilities by exp([low_bias,0,high_bias]), normalize; labels and target stay fixed',
        selection='mean over three internal fold participant BA; tie by candidate id; all outer choices frozen before outer evaluation',
        scope='exploratory follow-up on repeatedly used train participants, no independent confirmation',
        validation_evaluated=False,test_evaluated=False,dataset_sha256=digest(dataset),partition_sha256=digest(partition),
        sources={n:digest(ROOT/'scripts'/n) for n in ['entrenar_avanzados.py','avanzados_core.py','explorar_fusiones.py','optimizar_historial.py','temporales_core.py','control_historial.py']},
        requirements_sha256=digest(ROOT/'requirements_avanzados.txt'),
        versions=dict(python=platform.python_version(),catboost=catboost.__version__,sklearn=sklearn.__version__,numpy=np.__version__,pandas=pd.__version__))
    write_json(out/'protocolo.json',protocol)
    def log(stage,**kw):
        with (out/'bitacora.jsonl').open('a',encoding='utf-8') as f:
            f.write(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),stage=stage,**kw),ensure_ascii=False)+'\n')
    xs={(p,c):inputs(train,p,c) for p in PANELS for c in [1,8]}
    search=[]; choices=[]; internal=[]
    for fold in folds:
        outer=np.flatnonzero(train.participant.isin(fold['fit'])); fit=train.iloc[outer]
        splitter=GroupKFold(n_splits=3,shuffle=True,random_state=20260911+fold['fold'])
        for inner,(ii,vv) in enumerate(splitter.split(fit,groups=fit.participant),1):
            ti,vi=outer[ii],outer[vv]; fitting=train.iloc[ti].reset_index(drop=True); validation=train.iloc[vi].reset_index(drop=True)
            true=validation[TARGET].map({c:i for i,c in enumerate(CLASSES)}).to_numpy(int)
            eval_weights=sample_weights(validation,'participant'); arrays=dict(source_row=validation.source_row.to_numpy(),true=true)
            for number,base in enumerate(grid):
                log('fit_started',fold=fold['fold'],inner=inner,**base)
                x=xs[(base['panel'],base['context'])]
                bundle=fit_bundle(x[ti],fitting,base['family'],base['weighting'],20260911)
                raw=raw_probabilities(bundle,x[vi]); arrays[f'm{number}']=raw
                for smoothing in protocol['smoothing']:
                    smoothed=smooth(validation,raw,smoothing)
                    for low,high in itertools.product(protocol['biases'],repeat=2):
                        prob=smoothed*np.exp([low,0,high])[None,:]
                        pred=prob.argmax(axis=1)
                        score=float(np.average(pred==true,weights=eval_weights))
                        cid=f'{base["base_id"]}__{smoothing}__{low}__{high}'
                        search.append(dict(fold=fold['fold'],inner=inner,candidate_id=cid,**base,smoothing=smoothing,
                            low_bias=low,high_bias=high,score=score))
                log('fit_completed',fold=fold['fold'],inner=inner,base_id=base['base_id'])
            path=out/'predicciones_internas'/f'fold{fold["fold"]}__inner{inner}.npz'
            np.savez_compressed(path,**arrays)
            internal.append(dict(fold=fold['fold'],inner=inner,path=path.relative_to(out).as_posix(),sha256=digest(path),
                train_participants=sorted(fitting.participant.unique()),evaluation_participants=sorted(validation.participant.unique())))
            pd.DataFrame(search).to_csv(out/'todos_los_intentos.csv',index=False); write_json(out/'catalogo_interno.json',internal)
            print(f'Fold {fold["fold"]}/5, interno {inner}/3 completado: 24 modelos, 432 decisiones',flush=True)
        s=pd.DataFrame(search); s=s.loc[s.fold.eq(fold['fold'])]
        fields=['candidate_id','base_id','panel','context','family','weighting','smoothing','low_bias','high_bias']
        scores=s.groupby(fields,as_index=False).score.mean()
        for scope in protocol['scopes']:
            winner=choose(scores,scope)
            choices.append(dict(fold=fold['fold'],scope=scope,**{k:winner[k].item() if hasattr(winner[k],'item') else winner[k] for k in fields},inner_score=float(winner.score)))
        write_json(out/'selecciones.json',choices)
    frozen=digest(out/'selecciones.json'); log('selection_frozen',sha256=frozen)
    artifacts=[]; predictions=[]; people=[]; metrics=[]
    for choice in choices:
        fold=folds[choice['fold']-1]; ti=np.flatnonzero(train.participant.isin(fold['fit'])); vi=np.flatnonzero(train.participant.isin(fold['evaluation']))
        fitting=train.iloc[ti].reset_index(drop=True); validation=train.iloc[vi].reset_index(drop=True)
        x=xs[(choice['panel'],choice['context'])]
        for seed in protocol['seeds']:
            bundle=fit_bundle(x[ti],fitting,choice['family'],choice['weighting'],seed); bundle['choice']=choice
            name=f'fold{fold["fold"]}__{choice["scope"]}__{seed}'; path=out/'modelos'/f'{name}.joblib'
            joblib.dump(bundle,path,compress=3)
            prob=predict(bundle,validation); np.testing.assert_array_equal(prob,predict(joblib.load(path),validation))
            pred=np.asarray(CLASSES)[prob.argmax(axis=1)]; ident=dict(model_id=name,scope=choice['scope'],fold=fold['fold'],seed=seed)
            artifacts.append(dict(**ident,choice=choice,path=path.relative_to(out).as_posix(),sha256=digest(path),
                train_participants=fold['fit'],evaluation_participants=fold['evaluation'],reload_verified=True))
            p=validation[['source_row','participant','window_start_utc']].copy(); p['true']=validation[TARGET].to_numpy(); p['prediction']=pred
            for k,v in ident.items(): p[k]=v
            for i,c in enumerate(CLASSES): p['prob_'+c]=prob[:,i]
            predictions.append(p); metrics.append(dict(**ident,**metric_record(validation,TARGET,pred,'classification')))
            people.extend(dict(**ident,participant=p,score=s) for p,s in individual_scores(validation,TARGET,pred,'classification').items())
        write_json(out/'catalogo_modelos.json',artifacts); log('outer_completed',fold=fold['fold'],scope=choice['scope'])
        print(f'Evaluado fold {fold["fold"]}, {choice["scope"]}: {choice["family"]} {choice["weighting"]}',flush=True)
    assert digest(out/'selecciones.json')==frozen
    pd.concat(predictions).to_csv(out/'predicciones_oof.csv.gz',index=False,compression='gzip')
    pd.DataFrame(metrics).to_csv(out/'metricas_folds.csv',index=False); pd.DataFrame(people).to_csv(out/'metricas_participantes.csv',index=False)
    write_json(out/'completo.json',dict(models=len(artifacts),inner_model_bundles=360,inner_primitive_fits=480,
        protocol_sha256=digest(out/'protocolo.json'),selection_sha256=frozen,catalog_sha256=digest(out/'catalogo_modelos.json'),
        predictions_sha256=digest(out/'predicciones_oof.csv.gz'),validation_evaluated=False,test_evaluated=False))
    log('completed',models=len(artifacts)); print(pd.DataFrame(people).groupby('scope').score.mean().to_string(),flush=True)


if __name__=='__main__':
    with threadpool_limits(limits=4): main()
