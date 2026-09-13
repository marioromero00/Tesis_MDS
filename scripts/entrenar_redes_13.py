"""Seis configuraciones, tres checkpoints y tres suavizados; cinco folds fijos."""
import json
from datetime import datetime, timezone
import joblib
import numpy as np
import pandas as pd
import torch
from redes_secuencia_13 import grid, train, predict
from entrenar_hiperparametros import load_train
from control_historial import nested_folds
from temporales_core import ROOT, CLASSES, write_json, digest, metric_record, individual_scores
from hiperparametros_core import TARGET, FULL
from optimizar_historial import smooth

OUT = ROOT/'resultados/redes_13-09-2026'


def main():
    OUT.mkdir(exist_ok=False)
    for name in ['internos', 'modelos', 'curvas', 'predicciones_internas']:
        (OUT/name).mkdir()
    frame = load_train(); folds = nested_folds(frame)
    sources = ['redes_secuencia_13.py', 'entrenar_redes_13.py', 'temporales_core.py',
        'entrenar_hiperparametros.py', 'control_historial.py', 'optimizar_historial.py',
        'avanzados_core.py', 'hiperparametros_core.py', 'baselines_estaticos.py']
    protocol = dict(created_utc=datetime.now(timezone.utc).isoformat(), grid=grid(), folds=folds,
        seed=20260913, checkpoints=[4, 8, 12], smoothing=[1, 8, 32], features=FULL, target=TARGET,
        primary='all internally selected versus previous Ridge; family and repeat-current secondary',
        selection='single inner 16/4 participant split per outer fold; mean observed-class participant BA; ties id epoch smoothing',
        control='refit selected all architecture from scratch with repeated endpoint; matched hyperparameters and epochs',
        causal='right padding; reset participant recording or gap !=1 second; original preprocessing offline',
        scope='exploratory adaptive train reuse; no independent confirmation; one neural seed',
        validation_evaluated=False, test_evaluated=False, torch=str(torch.__version__),
        sources={n: digest(ROOT/'scripts'/n) for n in sources},
        dataset_sha256=digest(ROOT/'resultados/modelado/dataset_modelado.csv'),
        partition_sha256=digest(ROOT/'resultados/modelado/particion_participantes.csv'))
    write_json(OUT/'protocolo.json', protocol)
    attempts=[]; selections=[]; catalog=[]
    for fold in folds:
        fit=frame.loc[frame.participant.isin(fold['inner_fit'])].reset_index(drop=True)
        val=frame.loc[frame.participant.isin(fold['inner_validation'])].reset_index(drop=True)
        for config in grid():
            identity=f'fold{fold["fold"]}_{config["id"]}'
            def checkpoint(epoch, b, curve):
                if epoch not in protocol['checkpoints']: return
                path=OUT/'internos'/f'{identity}_epoch{epoch}.joblib'; joblib.dump(b,path,compress=3)
                raw=predict(b,val)
                np.savez_compressed(OUT/'predicciones_internas'/f'{identity}_epoch{epoch}.npz',
                                   source_row=val.source_row.to_numpy(), scores=raw)
                for window in protocol['smoothing']:
                    pred=np.asarray(CLASSES)[smooth(val,raw,window).argmax(axis=1)]
                    score=metric_record(val,TARGET,pred,'classification')['macro_score']
                    attempts.append(dict(fold=fold['fold'],id=config['id'],family=config['family'],
                                         epoch=epoch,smoothing=window,score=score))
                catalog.append(dict(path=path.relative_to(OUT).as_posix(),sha256=digest(path),fold=fold['fold'],
                                    fit=fold['inner_fit'],evaluation=fold['inner_validation']))
                pd.DataFrame(attempts).to_csv(OUT/'intentos.csv',index=False)
                write_json(OUT/'catalogo_interno.json',catalog)
                print(identity, 'epoch',epoch,'done',flush=True)
            _,curve=train(fit,config,protocol['seed'],12,checkpoint)
            write_json(OUT/'curvas'/f'{identity}.json',curve)
        scores=pd.DataFrame(attempts); scores=scores.loc[scores.fold.eq(fold['fold'])]
        for scope in ['all','Transformer','TCN']:
            eligible=scores if scope=='all' else scores.loc[scores.family.eq(scope)]
            best=eligible.sort_values(['score','id','epoch','smoothing'],ascending=[False,True,True,True]).iloc[0].to_dict()
            selections.append(dict(**best,scope=scope))
        write_json(OUT/'selecciones.json',selections)
    frozen=digest(OUT/'selecciones.json'); rows=[]; people=[]; metrics=[]; models=[]
    choices=selections+[dict(c,scope='repeat_current') for c in selections if c['scope']=='all']
    for choice in choices:
        fold=folds[int(choice['fold'])-1]
        fit=frame.loc[frame.participant.isin(fold['fit'])].reset_index(drop=True)
        val=frame.loc[frame.participant.isin(fold['evaluation'])].reset_index(drop=True)
        config=next(c for c in grid() if c['id']==choice['id'])
        b,curve=train(fit,config,protocol['seed'],int(choice['epoch']),repeat=choice['scope']=='repeat_current')
        b['smoothing']=int(choice['smoothing'])
        identity=f'fold{fold["fold"]}_{choice["scope"]}'
        path=OUT/'modelos'/f'{identity}.joblib'; joblib.dump(b,path,compress=3)
        raw=predict(b,val); restored=predict(joblib.load(path),val)
        np.testing.assert_array_equal(raw,restored)
        pred=np.asarray(CLASSES)[raw.argmax(axis=1)]
        p=val[['source_row','participant','window_start_utc']].copy()
        p['true']=val[TARGET].to_numpy(); p['prediction']=pred; p['scope']=choice['scope']; p['fold']=fold['fold']
        for i,c in enumerate(CLASSES): p['score_'+c]=raw[:,i]
        rows.append(p)
        people.extend(dict(fold=fold['fold'],scope=choice['scope'],participant=k,score=v)
                      for k,v in individual_scores(val,TARGET,pred,'classification').items())
        metrics.append(dict(fold=fold['fold'],scope=choice['scope'],**metric_record(val,TARGET,pred,'classification')))
        models.append(dict(path=path.relative_to(OUT).as_posix(),sha256=digest(path),choice=choice,
                           fit=fold['fit'],evaluation=fold['evaluation']))
        write_json(OUT/'curvas'/f'{identity}_outer.json',curve)
        write_json(OUT/'catalogo_modelos.json',models)
        pd.concat(rows).to_csv(OUT/'predicciones_oof.csv.gz',index=False)
        pd.DataFrame(people).to_csv(OUT/'metricas_participantes.csv',index=False)
        pd.DataFrame(metrics).to_csv(OUT/'metricas_folds.csv',index=False)
        print('OUTER',identity,metrics[-1]['macro_score'],flush=True)
    assert frozen==digest(OUT/'selecciones.json')
    write_json(OUT/'completo.json',dict(inner_models=len(catalog),outer_models=len(models),
        predictions=sum(len(p) for p in rows),selections_sha256=frozen))
    print(pd.DataFrame(people).groupby('scope').score.mean().to_string(),flush=True)


if __name__=='__main__': main()
