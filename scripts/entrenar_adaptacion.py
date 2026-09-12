"""Adaptacion offline: requiere la sesion completa sin sus etiquetas."""
import json
from datetime import datetime,timezone
import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits
from adaptacion_core import grid,adapt,predict
from entrenar_hiperparametros import load_train
from control_historial import nested_folds
from hiperparametros_core import TARGET
from avanzados_core import sample_weights
from temporales_core import ROOT,CLASSES,digest,write_json,metric_record,individual_scores

OUT=ROOT/'resultados/adaptacion_offline_11-09-2026'
SOURCE=ROOT/'resultados/persistencia_11-09-2026'
ENSEMBLES=ROOT/'resultados/ensambles_11-09-2026'


def main():
    OUT.mkdir(exist_ok=False); (OUT/'modelos').mkdir(); (OUT/'internos').mkdir()
    train=load_train(); folds=nested_folds(train); candidates=grid()
    catalog=json.loads((SOURCE/'catalogo_interno.json').read_text()); bases=json.loads((ENSEMBLES/'catalogo_modelos.json').read_text())
    protocol=dict(created_utc=datetime.now(timezone.utc).isoformat(),target=TARGET,folds=folds,grid=candidates,scopes=['all','rank','center'],primary='all',
        seed=20260911,base='pool_fixed_history',selection='mean inner participant BA; ties by candidate_id',
        deployment='OFFLINE TRANSDUCTIVE: complete unlabeled participant session needed; future inputs used for centering/ranking',
        sources={str(p.relative_to(ROOT)):digest(p) for p in [ROOT/'scripts/adaptacion_core.py',ROOT/'scripts/entrenar_adaptacion.py',
            SOURCE/'catalogo_interno.json',SOURCE/'protocolo.json',ENSEMBLES/'catalogo_modelos.json',ROOT/'resultados/modelado/dataset_modelado.csv',
            ROOT/'resultados/modelado/particion_participantes.csv']},validation_evaluated=False,test_evaluated=False,
        scope='adaptive exploratory offline alternative, not a causal performance claim; target 0.5 not guaranteed')
    write_json(OUT/'protocolo.json',protocol); attempts=[]; selections=[]; inner_catalog=[]
    for fold in folds:
        for item in [x for x in catalog if x['fold']==fold['fold']]:
            path=SOURCE/item['saved_path']; assert digest(path)==item['saved_sha256']
            with np.load(path) as saved:
                val=train.set_index('source_row',drop=False).loc[saved['source_row']].reset_index(drop=True); raw=saved['raw'].copy()
            assert set(val.participant)==set(item['evaluation_participants'])
            assert set(val.participant).isdisjoint(item['train_participants'])
            weight=sample_weights(val,'participant'); arrays=dict(source_row=val.source_row.to_numpy(),raw=raw)
            for i,choice in enumerate(candidates):
                proba=adapt(val,raw,choice); arrays[f'p{i}']=proba
                pred=np.asarray(CLASSES)[proba.argmax(axis=1)]
                attempts.append(dict(fold=fold['fold'],inner=item['inner'],**choice,score=float(np.average(pred==val[TARGET],weights=weight))))
            path=OUT/'internos'/f'fold{fold["fold"]}_inner{item["inner"]}.npz'; np.savez_compressed(path,**arrays)
            inner_catalog.append(dict(fold=fold['fold'],inner=item['inner'],path=path.relative_to(OUT).as_posix(),sha256=digest(path),
                source_path=item['saved_path'],source_sha256=item['saved_sha256'],train_participants=item['train_participants'],evaluation_participants=item['evaluation_participants']))
        scores=pd.DataFrame(attempts); scores=scores.loc[scores.fold.eq(fold['fold'])].groupby(['candidate_id','family'],as_index=False).score.mean()
        for scope in protocol['scopes']:
            eligible=scores if scope=='all' else scores.loc[scores.family.eq(scope)]
            winner=eligible.sort_values(['score','candidate_id'],ascending=[False,True]).iloc[0]
            selections.append(dict(fold=fold['fold'],scope=scope,choice=next(d for d in candidates if d['candidate_id']==winner.candidate_id),inner_score=float(winner.score)))
        pd.DataFrame(attempts).to_csv(OUT/'intentos.csv',index=False); print(f'Adaptacion offline interno {fold["fold"]}/5',flush=True)
    write_json(OUT/'catalogo_interno.json',inner_catalog); write_json(OUT/'selecciones.json',selections)
    frozen=digest(OUT/'selecciones.json'); write_json(OUT/'seleccion_congelada.json',dict(utc=datetime.now(timezone.utc).isoformat(),sha256=frozen))
    rows=[]; models=[]; metrics=[]; people=[]
    for choice in selections:
        fold=folds[choice['fold']-1]; val=train.loc[train.participant.isin(fold['evaluation'])].reset_index(drop=True)
        item=next(x for x in bases if x['fold']==fold['fold'] and x['scope']=='pool_fixed_history' and x['seed']==20260911)
        assert digest(ENSEMBLES/item['path'])==item['sha256']
        bundle=dict(base=joblib.load(ENSEMBLES/item['path']),choice=choice['choice'],offline=True)
        identity=dict(model_id=f'fold{fold["fold"]}_{choice["scope"]}',fold=fold['fold'],scope=choice['scope'],seed=20260911)
        path=OUT/'modelos'/f'{identity["model_id"]}.joblib'; joblib.dump(bundle,path,compress=3)
        proba=predict(bundle,val); np.testing.assert_array_equal(proba,predict(joblib.load(path),val))
        pred=np.asarray(CLASSES)[proba.argmax(axis=1)]; p=val[['source_row','participant','window_start_utc']].copy()
        p['true']=val[TARGET].to_numpy(); p['prediction']=pred
        for k,v in identity.items(): p[k]=v
        for i,c in enumerate(CLASSES): p['prob_'+c]=proba[:,i]
        rows.append(p); models.append(dict(**identity,path=path.relative_to(OUT).as_posix(),sha256=digest(path),choice=choice,
            train_participants=fold['fit'],evaluation_participants=fold['evaluation'],source_sha256=item['sha256']))
        metrics.append(dict(**identity,**metric_record(val,TARGET,pred,'classification')))
        people.extend(dict(**identity,participant=p,score=s) for p,s in individual_scores(val,TARGET,pred,'classification').items())
    pd.concat(rows).to_csv(OUT/'predicciones_oof.csv.gz',index=False,compression='gzip')
    pd.DataFrame(metrics).to_csv(OUT/'metricas_folds.csv',index=False); pd.DataFrame(people).to_csv(OUT/'metricas_participantes.csv',index=False)
    write_json(OUT/'catalogo_modelos.json',models); assert digest(OUT/'selecciones.json')==frozen
    write_json(OUT/'completo.json',dict(models=len(models),predictions=sum(map(len,rows)),inner_scores=len(attempts),selection_sha256=frozen,
        completed_utc=datetime.now(timezone.utc).isoformat(),validation_evaluated=False,test_evaluated=False,offline=True))
    print(pd.DataFrame(people).groupby('scope').score.mean().to_string(),flush=True)


if __name__=='__main__':
    with threadpool_limits(limits=2): main()
