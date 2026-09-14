"""32 configs x 5 folds, seleccion interna; procesos independientes y reanudacion."""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime,timezone
import json
import time
import joblib
import numpy as np
import pandas as pd
import torch
from threadpoolctl import threadpool_limits
from recurrentes_grid_core import grid,train,predict,FAMILY
from entrenar_hiperparametros import load_train
from control_historial import nested_folds
from temporales_core import ROOT,CLASSES,digest,write_json,metric_record,individual_scores
from hiperparametros_core import FULL,TARGET
from optimizar_historial import smooth

OUT=ROOT/'resultados/grids_recurrentes_13-09-2026'/FAMILY
FRAME=None


def initialize():
    global FRAME
    torch.set_num_threads(2)
    FRAME=load_train()


def worker(task):
    with threadpool_limits(limits=2): return run_task(task)


def run_task(task):
    fold=task['fold']; config=task['config']; name=task['name']; inner=task['kind']=='inner'
    fit_people=fold['inner_fit' if inner else 'fit']; val_people=fold['inner_validation' if inner else 'evaluation']
    fit=FRAME.loc[FRAME.participant.isin(fit_people)].reset_index(drop=True)
    val=FRAME.loc[FRAME.participant.isin(val_people)].reset_index(drop=True)
    attempts=[]; catalog=[]; start=time.time()
    def save(epoch,b,curve):
        if epoch not in [2,4,8,16]: return
        path=OUT/'internos'/f'{name}_e{epoch}.joblib'; joblib.dump(b,path,compress=3)
        scores=predict(b,val)
        np.savez_compressed(OUT/'predicciones_internas'/f'{name}_e{epoch}.npz',
                           source_row=val.source_row.to_numpy(),scores=scores)
        catalog.append(dict(path=path.relative_to(OUT).as_posix(),sha256=digest(path),fold=fold['fold'],
                            fit=fit_people,evaluation=val_people,config=config,epoch=epoch))
        for window in [1,8,32]:
            pred=np.asarray(CLASSES)[smooth(val,scores,window).argmax(axis=1)]
            attempts.append(dict(fold=fold['fold'],id=config['id'],epoch=epoch,smoothing=window,
                                 score=metric_record(val,TARGET,pred,'classification')['macro_score']))
        write_json(OUT/'curvas'/f'{name}.json',curve)
    if inner:
        train(fit,config,20260913,16,save)
        result=dict(task=task,attempts=attempts,catalog=catalog,seconds=time.time()-start)
    else:
        choice=task['choice']; repeat=task['scope']=='repeat_current'
        b,curve=train(fit,config,task['seed'],int(choice['epoch']),repeat=repeat)
        b['smoothing']=int(choice['smoothing'])
        path=OUT/'modelos'/f'{name}.joblib'; joblib.dump(b,path,compress=3)
        scores=predict(b,val); np.testing.assert_array_equal(scores,predict(joblib.load(path),val))
        pred=np.asarray(CLASSES)[scores.argmax(axis=1)]
        identity=dict(fold=fold['fold'],scope=task['scope'],seed=task['seed'])
        p=val[['source_row','participant','window_start_utc']].copy(); p['true']=val[TARGET].to_numpy(); p['prediction']=pred
        for k,v in identity.items(): p[k]=v
        for i,c in enumerate(CLASSES): p['score_'+c]=scores[:,i]
        p.to_csv(OUT/'predicciones'/f'{name}.csv.gz',index=False)
        write_json(OUT/'curvas'/f'{name}.json',curve)
        result=dict(task=task,catalog=dict(path=path.relative_to(OUT).as_posix(),sha256=digest(path),
            fit=fit_people,evaluation=val_people,choice=choice,**identity),
            metric=dict(**identity,**metric_record(val,TARGET,pred,'classification')),
            people=[dict(**identity,participant=k,score=v) for k,v in individual_scores(val,TARGET,pred,'classification').items()],
            seconds=time.time()-start)
    write_json(OUT/'tareas'/f'{name}.json',result)
    return result


def execute(tasks):
    done=[]; pending=[]
    for task in tasks:
        path=OUT/'tareas'/f'{task["name"]}.json'
        if path.exists():
            result=json.loads(path.read_text(encoding='utf-8')); assert result['task']==task
            entries=result['catalog'] if isinstance(result['catalog'],list) else [result['catalog']]
            for item in entries: assert digest(OUT/item['path'])==item['sha256']
            done.append(result)
        else: pending.append(task)
    with ProcessPoolExecutor(max_workers=4,initializer=initialize) as pool:
        futures={pool.submit(worker,t):t for t in pending}
        for future in as_completed(futures):
            result=future.result(); done.append(result)
            print(f'{len(done)}/{len(tasks)} {result["task"]["name"]} {result["seconds"]:.1f}s',flush=True)
    return sorted(done,key=lambda r:r['task']['name'])


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--resume',action='store_true'); args=parser.parse_args()
    frame=load_train(); folds=nested_folds(frame)
    sources=['recurrentes_grid_core.py','entrenar_recurrentes_grid.py','redes_secuencia_13.py',
        'temporales_core.py','entrenar_hiperparametros.py','hiperparametros_core.py',
        'control_historial.py','optimizar_historial.py','avanzados_core.py','baselines_estaticos.py']
    if args.resume:
        protocol=json.loads((OUT/'protocolo.json').read_text(encoding='utf-8'))
        for n,h in protocol['sources'].items(): assert digest(ROOT/'scripts'/n)==h
        assert protocol['grid']==grid() and protocol['folds']==folds
    else:
        OUT.mkdir(parents=True,exist_ok=False)
        for n in ['internos','modelos','curvas','predicciones_internas','predicciones','tareas']: (OUT/n).mkdir()
        protocol=dict(created_utc=datetime.now(timezone.utc).isoformat(),grid=grid(),folds=folds,
            features=FULL,target=TARGET,seeds=[20260913,20260914],inner_seed=20260913,
            checkpoints=[2,4,8,16],smoothing=[1,8,32],workers=4,threads_per_worker=2,
            selection='single inner 16/4 split; participant observed-class BA; ties id epoch smoothing; freeze all before outer',
            family=FAMILY,primary='family-specific grid-selected model versus Ridge and Transformer grid; no post-hoc best-family primary',
            secondary='matched repeat_current with same hyperparameters and epoch, refit separately; two outer seeds averaged per participant',
            architecture='RNN packed past sequences; TCN depth maps 1 to 2 blocks and 2 to 4 blocks; endpoint dropout all families',
            initialization='prediction and checkpoint callback preserve torch RNG; earlier sources left intact',
            scope='exploratory adaptive train reuse; original feature normalization offline',
            validation_evaluated=False,test_evaluated=False,torch=str(torch.__version__),
            sources={n:digest(ROOT/'scripts'/n) for n in sources},
            dataset_sha256=digest(ROOT/'resultados/modelado/dataset_modelado.csv'),
            partition_sha256=digest(ROOT/'resultados/modelado/particion_participantes.csv'))
        write_json(OUT/'protocolo.json',protocol)
    tasks=[dict(kind='inner',fold=f,config=c,name=f'fold{f["fold"]}_{c["id"]}') for f in folds for c in grid()]
    results=execute(tasks)
    scores=pd.DataFrame([a for r in results for a in r['attempts']]); scores.to_csv(OUT/'intentos.csv',index=False)
    write_json(OUT/'catalogo_interno.json',[c for r in results for c in r['catalog']])
    choices=[]
    for f in folds:
        best=scores.loc[scores.fold.eq(f['fold'])].sort_values(['score','id','epoch','smoothing'],
            ascending=[False,True,True,True]).iloc[0].to_dict(); choices.append(best)
    selection_path=OUT/'selecciones.json'
    if selection_path.exists(): assert json.loads(selection_path.read_text())==choices
    else: write_json(selection_path,choices)
    frozen=digest(selection_path); print('Selections frozen',frozen,flush=True)
    tasks=[dict(kind='outer',fold=folds[int(c['fold'])-1],config=next(g for g in grid() if g['id']==c['id']),
                choice=c,scope=scope,seed=seed,name=f'fold{int(c["fold"])}_{scope}_{seed}')
           for c in choices for scope in [FAMILY,'repeat_current'] for seed in protocol['seeds']]
    results=execute(tasks)
    write_json(OUT/'catalogo_modelos.json',[r['catalog'] for r in results])
    pd.DataFrame([r['metric'] for r in results]).to_csv(OUT/'metricas_folds.csv',index=False)
    people=pd.DataFrame([p for r in results for p in r['people']]); people.to_csv(OUT/'metricas_participantes.csv',index=False)
    pred=pd.concat([pd.read_csv(OUT/'predicciones'/f'{r["task"]["name"]}.csv.gz') for r in results])
    pred.to_csv(OUT/'predicciones_oof.csv.gz',index=False)
    assert digest(selection_path)==frozen
    write_json(OUT/'completo.json',dict(inner_fits=160,inner_checkpoints=640,internal_scores=len(scores),
        outer_models=len(results),predictions=len(pred),selection_sha256=frozen))
    print(people.groupby(['scope','seed']).score.mean().to_string(),flush=True)


if __name__=='__main__': main()
