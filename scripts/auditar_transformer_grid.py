"""Audita cada checkpoint, fuente, split, decision y prediccion externa."""
from concurrent.futures import ProcessPoolExecutor,as_completed
import json
import joblib
import numpy as np
import pandas as pd
import torch
from threadpoolctl import threadpool_limits
from transformer_grid_core import grid,predict
from entrenar_transformer_grid import OUT
from entrenar_hiperparametros import load_train
from temporales_core import ROOT,digest,write_json,preprocessor,CLASSES,metric_record,individual_scores
from hiperparametros_core import FULL,TARGET
from optimizar_historial import smooth

FRAME=None


def initialize():
    global FRAME
    FRAME=load_train(); torch.set_num_threads(2)


def audit_task(result):
    with threadpool_limits(limits=2): return check(result)


def check(result):
    task=result['task']; fold=task['fold']; inner=task['kind']=='inner'
    fit_people=fold['inner_fit' if inner else 'fit']; eval_people=fold['inner_validation' if inner else 'evaluation']
    assert set(fit_people).isdisjoint(eval_people)
    fit=FRAME.loc[FRAME.participant.isin(fit_people)].reset_index(drop=True)
    val=FRAME.loc[FRAME.participant.isin(eval_people)].reset_index(drop=True)
    prep=preprocessor().fit(fit[FULL]); attempts=[]; people=[]; metrics=[]; error=0.
    minimal=val[FULL+['participant','recording','window_start_utc']]
    catalog=result['catalog'] if inner else [result['catalog']]
    if inner:
        assert len(catalog)==4 and {c['epoch'] for c in catalog}=={2,4,8,16}
    for item in catalog:
        assert item['fit']==fit_people and item['evaluation']==eval_people
        path=OUT/item['path']; assert digest(path)==item['sha256']; b=joblib.load(path)
        assert b['config']==task['config'] and b['features']==FULL
        assert b['seed']==(20260913 if inner else task['seed'])
        assert b['repeat']==(not inner and task['scope']=='repeat_current')
        np.testing.assert_array_equal(prep.transform(fit[FULL]),b['prep'].transform(fit[FULL]))
        scores=predict(b,minimal)
        if inner:
            saved=np.load(OUT/'predicciones_internas'/f'{path.stem}.npz')
            np.testing.assert_array_equal(saved['source_row'],val.source_row)
            expected=saved['scores']; assert b['epoch']==item['epoch'] and b['smoothing']==1
            for w in [1,8,32]:
                pred=np.asarray(CLASSES)[smooth(val,scores,w).argmax(axis=1)]
                attempts.append(dict(fold=fold['fold'],id=b['config']['id'],epoch=b['epoch'],smoothing=w,
                    score=metric_record(val,TARGET,pred,'classification')['macro_score']))
        else:
            saved=pd.read_csv(OUT/'predicciones'/f'{task["name"]}.csv.gz')
            np.testing.assert_array_equal(saved.source_row,val.source_row); np.testing.assert_array_equal(saved.true,val[TARGET])
            expected=saved[['score_'+c for c in CLASSES]].to_numpy()
            pred=np.asarray(CLASSES)[scores.argmax(axis=1)]; np.testing.assert_array_equal(pred,saved.prediction)
            assert b['epoch']==task['choice']['epoch'] and b['smoothing']==task['choice']['smoothing']
            identity=dict(fold=fold['fold'],scope=task['scope'],seed=task['seed'])
            for k,v in identity.items(): assert saved[k].eq(v).all()
            people.extend(dict(**identity,participant=k,score=v) for k,v in individual_scores(val,TARGET,pred,'classification').items())
            metrics.append(dict(**identity,**metric_record(val,TARGET,pred,'classification')))
        np.testing.assert_allclose(scores,expected,atol=1e-7,rtol=0)
        np.testing.assert_array_equal(scores.argmax(axis=1),expected.argmax(axis=1))
        error=max(error,float(np.max(abs(scores-expected))))
    return dict(models=len(catalog),attempts=attempts,people=people,metrics=metrics,error=error)


def main():
    protocol=json.loads((OUT/'protocolo.json').read_text()); assert protocol['grid']==grid()
    for n,h in protocol['sources'].items(): assert digest(ROOT/'scripts'/n)==h
    for name,key in [('dataset_modelado.csv','dataset_sha256'),('particion_participantes.csv','partition_sha256')]:
        assert digest(ROOT/'resultados/modelado'/name)==protocol[key]
    tasks=[json.loads(p.read_text()) for p in sorted((OUT/'tareas').glob('*.json'))]; assert len(tasks)==180
    selected=json.loads((OUT/'selecciones.json').read_text())
    expected={(f['fold'],c['id']) for f in protocol['folds'] for c in grid()}
    actual={(r['task']['fold']['fold'],r['task']['config']['id']) for r in tasks if r['task']['kind']=='inner'}
    assert actual==expected
    external={(r['task']['fold']['fold'],r['task']['scope'],r['task']['seed']) for r in tasks if r['task']['kind']=='outer'}
    assert external=={(f['fold'],s,seed) for f in protocol['folds'] for s in ['Transformer','repeat_current'] for seed in protocol['seeds']}
    complete=json.loads((OUT/'completo.json').read_text())
    assert complete['selection_sha256']==digest(OUT/'selecciones.json')
    for r in tasks:
        task=r['task']; assert task['fold']==protocol['folds'][task['fold']['fold']-1]
        if task['kind']=='outer': assert task['choice']==selected[task['fold']['fold']-1]
    checks=[]
    with ProcessPoolExecutor(max_workers=4,initializer=initialize) as pool:
        futures=[pool.submit(audit_task,r) for r in tasks]
        for future in as_completed(futures):
            checks.append(future.result())
            if len(checks)%20==0: print('Audited tasks',len(checks),'/180',flush=True)
    scores=pd.DataFrame([a for r in checks for a in r['attempts']])
    people=pd.DataFrame([a for r in checks for a in r['people']]); metrics=pd.DataFrame([a for r in checks for a in r['metrics']])
    for actual,name,keys,columns in [(scores,'intentos.csv',['fold','id','epoch','smoothing'],['score']),
        (people,'metricas_participantes.csv',['fold','scope','seed','participant'],['score']),
        (metrics,'metricas_folds.csv',['fold','scope','seed'],['macro_score','balanced_accuracy','macro_f1','rows','participants'])]:
        old=pd.read_csv(OUT/name); assert len(old)==len(actual)
        for k in keys: np.testing.assert_array_equal(actual.sort_values(keys)[k],old.sort_values(keys)[k])
        for k in columns: np.testing.assert_allclose(actual.sort_values(keys)[k],old.sort_values(keys)[k],atol=1e-14,rtol=0)
    for choice in selected:
        best=scores.loc[scores.fold.eq(choice['fold'])].sort_values(['score','id','epoch','smoothing'],ascending=[False,True,True,True]).iloc[0]
        for k in ['id','epoch','smoothing']: assert choice[k]==best[k]
    for inner,name in [(True,'catalogo_interno.json'),(False,'catalogo_modelos.json')]:
        entries=[]
        for r in tasks:
            if (r['task']['kind']=='inner')==inner: entries.extend(r['catalog'] if inner else [r['catalog']])
        assert sorted(entries,key=lambda r:r['path'])==sorted(json.loads((OUT/name).read_text()),key=lambda r:r['path'])
    pred=pd.read_csv(OUT/'predicciones_oof.csv.gz')
    aggregate=pd.concat([pd.read_csv(p) for p in sorted((OUT/'predicciones').glob('*.csv.gz'))])
    keys=['fold','scope','seed','source_row']
    pd.testing.assert_frame_equal(pred.sort_values(keys).reset_index(drop=True),aggregate.sort_values(keys).reset_index(drop=True))
    assert sum(c['models'] for c in checks)==660 and len(scores)==1920 and len(pred)==54096
    write_json(OUT/'verificacion.json',dict(models=660,internal_scores=len(scores),outer_predictions=len(pred),
        max_prediction_error=max(c['error'] for c in checks),selection_verified=True,train_only_preprocessing=True,
        teacher_free_prediction=True,validation_evaluated=False,test_evaluated=False,auditor_sha256=digest(__file__)))


if __name__=='__main__': main()
