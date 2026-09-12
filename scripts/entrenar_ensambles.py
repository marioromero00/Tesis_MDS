"""Iteracion de ensambles reutilizando exclusivamente predicciones internas verificadas."""
import argparse
import json
from datetime import datetime,timezone
import joblib
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from threadpoolctl import threadpool_limits
from ensambles_core import BASES,STACKS,SCOPES,pool_grid,pool,meta_matrix,fit_meta,combine,choose,predict
from hiperparametros_core import TARGET,feature_cache,fit_bundle,raw_scores
from entrenar_hiperparametros import load_train
from avanzados_core import sample_weights
from temporales_core import ROOT,CLASSES,digest,write_json,metric_record,individual_scores

SOURCE=ROOT/'resultados/hiperparametros_11-09-2026_paralelo'
OUT=ROOT/'resultados/ensambles_11-09-2026'


def load_inner(meta,source_protocol,train):
    path=SOURCE/meta['path']; assert digest(path)==meta['sha256']
    arrays=np.load(path,allow_pickle=False)
    val=train.loc[train.participant.isin(meta['evaluation_participants'])].reset_index(drop=True)
    np.testing.assert_array_equal(val.source_row,arrays['source_row'])
    truth=val[TARGET].map({c:i for i,c in enumerate(CLASSES)}).to_numpy(int)
    np.testing.assert_array_equal(truth,arrays['true'])
    ids={d['base_id']:i for i,d in enumerate(source_protocol['grid'])}
    probabilities={d['base_id']:arrays[f'm{ids[d["base_id"]]}'] for d in BASES}
    return val,probabilities


def audit_stability(out,train):
    attempts=pd.read_csv(SOURCE/'todos_los_intentos.csv'); selected=json.loads((SOURCE/'selecciones.json').read_text())
    outside=pd.read_csv(SOURCE/'metricas_participantes.csv').groupby(['fold','scope']).score.mean()
    rows=[]; correlations=[]
    for fold in range(1,6):
        frame=attempts.loc[attempts.fold.eq(fold)]
        for scope in ['all','fusion']:
            subset=frame if scope=='all' else frame.loc[frame.family.str.startswith('fusion_')]
            pivot=subset.pivot(index='candidate_id',columns='inner',values='score')
            average=pivot.mean(axis=1).sort_values(ascending=False)
            winner=next(s for s in selected if s['fold']==fold and s['scope']==scope)['candidate_id']
            individual=[winner if np.isclose(pivot.loc[winner,column],pivot[column].max(),rtol=0,atol=1e-12)
                        else None for column in pivot]
            rows.append(dict(fold=fold,scope=scope,selected=winner,inner_score=float(pivot.loc[winner].mean()),
                runner_up_margin=float(average.iloc[0]-average.iloc[1]),inner_winner_agreements=individual.count(winner),
                outer_score=float(outside.loc[(fold,scope)]),inner_outer_gap=float(pivot.loc[winner].mean()-outside.loc[(fold,scope)])))
            for a,b in [(1,2),(1,3),(2,3)]:
                correlations.append(dict(fold=fold,scope=scope,inner_a=a,inner_b=b,spearman=float(spearmanr(pivot[a],pivot[b]).statistic)))
    pd.DataFrame(rows).to_csv(out/'auditoria_seleccion.csv',index=False)
    pd.DataFrame(correlations).to_csv(out/'auditoria_ranking.csv',index=False)
    pd.DataFrame([dict(constant=c,**metric_record(train,TARGET,np.repeat(c,len(train)),'classification')) for c in CLASSES]).to_csv(out/'referencias_constantes.csv',index=False)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',default=str(OUT.relative_to(ROOT)))
    out=ROOT/parser.parse_args().output; out.mkdir(parents=True,exist_ok=False)
    for name in ['modelos','meta_oof']: (out/name).mkdir()
    train=load_train(); prior=json.loads((SOURCE/'protocolo.json').read_text())
    completed=json.loads((SOURCE/'completo.json').read_text()); verified=json.loads((SOURCE/'verificacion.json').read_text())
    assert digest(SOURCE/'protocolo.json')==completed['protocol_sha256']
    for name,sha in prior['sources'].items(): assert digest(ROOT/'scripts'/name)==sha
    assert digest(ROOT/'scripts/informe_hiperparametros.py')==verified['report_script_sha256']
    catalog_inner=json.loads((SOURCE/'catalogo_interno.json').read_text()); definitions=pool_grid(); folds=prior['folds']
    protocol=dict(created_utc=datetime.now(timezone.utc).isoformat(),task='arousal',target=TARGET,folds=folds,
        bases=BASES,pool_grid=definitions,stacks=STACKS,scopes=SCOPES,seeds=[20260911,20260912],
        primary='pool_selected vs previous geometric fusion; six stacking configurations are fixed secondary contrasts, not selected on outer scores',
        stacking='14 base variants produce 42 probability features; meta estimator fitted on group-OOF predictions for outer-fit people only; all six meta definitions fixed before outer evaluation',
        pool='average or geometric pool across regularizations, weighted current/history mix; weights, context and smoothing selected only using three inner folds',
        source=SOURCE.relative_to(ROOT).as_posix(),source_protocol_sha256=digest(SOURCE/'protocolo.json'),
        source_inner_catalog_sha256=digest(SOURCE/'catalogo_interno.json'),source_verification_sha256=digest(SOURCE/'verificacion.json'),
        dataset_sha256=prior['dataset_sha256'],partition_sha256=prior['partition_sha256'],
        sources={n:digest(ROOT/'scripts'/n) for n in ['ensambles_core.py','entrenar_ensambles.py','hiperparametros_core.py',
            'entrenar_hiperparametros.py','avanzados_core.py','optimizar_historial.py','temporales_core.py']},
        requirements_sha256=digest(ROOT/'requirements_avanzados.txt'),versions=prior['versions'],
        scope='adaptive exploration on repeatedly used train participants; no independent confirmation',validation_evaluated=False,test_evaluated=False)
    write_json(out/'protocolo.json',protocol); audit_stability(out,train)
    def log(stage,**kw):
        with (out/'bitacora.jsonl').open('a',encoding='utf-8') as f:
            f.write(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),stage=stage,**kw))+'\n')
    choices=[]; attempts=[]; matrices={}; meta_catalog=[]
    for fold in folds:
        indices=np.flatnonzero(train.participant.isin(fold['fit'])); fit=train.iloc[indices].reset_index(drop=True)
        block=[]; rows=[]
        for meta in [m for m in catalog_inner if m['fold']==fold['fold']]:
            assert set(meta['train_participants']).isdisjoint(meta['evaluation_participants'])
            assert set(meta['train_participants'])|set(meta['evaluation_participants'])==set(fold['fit'])
            val,probabilities=load_inner(meta,prior,train)
            block.append(meta_matrix(probabilities)); rows.extend(val.source_row.tolist())
            truth=val[TARGET].map({c:i for i,c in enumerate(CLASSES)}).to_numpy(int); weights=sample_weights(val,'participant')
            for definition in definitions:
                prediction=pool(val,probabilities,definition).argmax(axis=1)
                attempts.append(dict(fold=fold['fold'],inner=meta['inner'],candidate_id=definition['candidate_id'],
                    family=definition['family'],score=float(np.average(prediction==truth,weights=weights))))
        assert len(rows)==len(set(rows))==len(fit) and set(rows)==set(fit.source_row)
        order=pd.Index(rows).get_indexer(fit.source_row); x=np.ascontiguousarray(np.concatenate(block)[order]); matrices[fold['fold']]=x
        path=out/'meta_oof'/f'fold{fold["fold"]}.npz'; np.savez_compressed(path,source_row=fit.source_row.to_numpy(),x=x)
        meta_catalog.append(dict(fold=fold['fold'],path=path.relative_to(out).as_posix(),sha256=digest(path),participants=fold['fit']))
        scores=pd.DataFrame(attempts); scores=scores.loc[scores.fold.eq(fold['fold'])].groupby(['candidate_id','family'],as_index=False).score.mean()
        for scope in SCOPES[:3]:
            winner=choose(scores,scope); definition=next(d for d in definitions if d['candidate_id']==winner.candidate_id)
            choices.append(dict(fold=fold['fold'],scope=scope,kind='pool',pool=definition,inner_score=float(winner.score)))
        for scope,history in [('pool_fixed_history',1.),('pool_fixed_multiscale',.5)]:
            definition=next(d for d in definitions if d['family']=='both' and d['history_weight']==history and d['aggregation']=='mean' and d['smoothing']==1)
            choices.append(dict(fold=fold['fold'],scope=scope,kind='pool',pool=definition,inner_score=None))
        choices.extend(dict(fold=fold['fold'],kind='stack',inner_score=None,**s) for s in STACKS)
        print(f'Fold {fold["fold"]}: matriz OOF por persona y 60 combinaciones preparadas',flush=True)
    write_json(out/'catalogo_meta_oof.json',meta_catalog); write_json(out/'selecciones.json',choices)
    pd.DataFrame(attempts).to_csv(out/'todos_los_intentos.csv',index=False)
    frozen=digest(out/'selecciones.json'); log('selection_frozen',sha256=frozen)
    cache=feature_cache(train); models=[]; predictions=[]; people=[]; metrics=[]; coefficients=[]
    for fold in folds:
        ti=np.flatnonzero(train.participant.isin(fold['fit'])); vi=np.flatnonzero(train.participant.isin(fold['evaluation']))
        fit=train.iloc[ti].reset_index(drop=True); val=train.iloc[vi].reset_index(drop=True)
        for seed in protocol['seeds']:
            bank={}; probabilities={}
            for definition in BASES:
                log('base_fit_started',fold=fold['fold'],seed=seed,base_id=definition['base_id'])
                base=fit_bundle(cache,ti,fit,definition,seed); bank[definition['base_id']]=base
                probabilities[definition['base_id']]=raw_scores(base,cache,vi)
                log('base_fit_completed',fold=fold['fold'],seed=seed,base_id=definition['base_id'],components=len(base['components']))
            for choice in [s for s in choices if s['fold']==fold['fold']]:
                meta=fit_meta(matrices[fold['fold']],fit,TARGET,choice,seed) if choice['kind']=='stack' else None
                ids=choice['pool']['members'] if choice['kind']=='pool' else [d['base_id'] for d in BASES]
                bundle=dict(choice=choice,bases={k:bank[k] for k in ids},meta=meta,seed=seed)
                name=f'fold{fold["fold"]}_{choice["scope"]}_{seed}'; path=out/'modelos'/f'{name}.joblib'; joblib.dump(bundle,path,compress=3)
                score=combine(val,probabilities,choice,meta)
                loaded=joblib.load(path); restored=combine(val,probabilities,loaded['choice'],loaded['meta'])
                np.testing.assert_array_equal(score,restored)
                pred=np.asarray(CLASSES)[score.argmax(axis=1)]; identity=dict(model_id=name,fold=fold['fold'],scope=choice['scope'],seed=seed)
                models.append(dict(**identity,path=path.relative_to(out).as_posix(),sha256=digest(path),choice=choice,
                    train_participants=fold['fit'],evaluation_participants=fold['evaluation']))
                p=val[['source_row','participant','window_start_utc']].copy(); p['true']=val[TARGET].to_numpy(); p['prediction']=pred
                for k,v in identity.items(): p[k]=v
                for i,c in enumerate(CLASSES): p['prob_'+c]=score[:,i]
                predictions.append(p); metrics.append(dict(**identity,**metric_record(val,TARGET,pred,'classification')))
                people.extend(dict(**identity,participant=p,score=s) for p,s in individual_scores(val,TARGET,pred,'classification').items())
                if meta is not None:
                    log('meta_fit_completed',fold=fold['fold'],seed=seed,scope=choice['scope'])
                    columns=[(d['base_id'],c) for d in BASES for c in CLASSES]
                    for cls,coef in zip(meta['model'].classes_,meta['model'].coef_):
                        coefficients.extend(dict(**identity,target_class=cls,base_id=k,input_class=c,coefficient=float(v)) for (k,c),v in zip(columns,coef))
            log('outer_completed',fold=fold['fold'],seed=seed); write_json(out/'catalogo_modelos.json',models)
            print(f'Evaluado fold {fold["fold"]}, semilla {seed}: 11 reglas',flush=True)
    assert digest(out/'selecciones.json')==frozen
    pd.concat(predictions).to_csv(out/'predicciones_oof.csv.gz',index=False,compression='gzip')
    pd.DataFrame(people).to_csv(out/'metricas_participantes.csv',index=False); pd.DataFrame(metrics).to_csv(out/'metricas_folds.csv',index=False)
    pd.DataFrame(coefficients).to_csv(out/'coeficientes_meta.csv',index=False)
    write_json(out/'completo.json',dict(models=len(models),base_fits=140,base_classifiers=420,meta_fits=60,
        protocol_sha256=digest(out/'protocolo.json'),selection_sha256=frozen,catalog_sha256=digest(out/'catalogo_modelos.json'),
        predictions_sha256=digest(out/'predicciones_oof.csv.gz'),validation_evaluated=False,test_evaluated=False))
    log('completed',models=len(models)); print(pd.DataFrame(people).groupby('scope').score.mean().to_string(),flush=True)


if __name__=='__main__':
    with threadpool_limits(limits=4): main()
