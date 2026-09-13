"""Recarga checkpoints y modelos; recalcula seleccion, preprocesado y predicciones."""
import json
import joblib
import numpy as np
import pandas as pd
import torch
from entrenar_redes_13 import OUT
from entrenar_hiperparametros import load_train
from redes_secuencia_13 import predict, sequences
from temporales_core import ROOT, digest, write_json, preprocessor, CLASSES, metric_record, individual_scores
from hiperparametros_core import FULL, TARGET
from optimizar_historial import smooth


def main():
    torch.set_num_threads(2)
    frame=load_train(); protocol=json.loads((OUT/'protocolo.json').read_text())
    for n,h in protocol['sources'].items(): assert digest(ROOT/'scripts'/n)==h
    for name,key in [('dataset_modelado.csv','dataset_sha256'),('particion_participantes.csv','partition_sha256')]:
        assert digest(ROOT/'resultados/modelado'/name)==protocol[key]
    attempts=[]; checked=0; max_error=0.; people=[]; fold_metrics=[]
    choices=json.loads((OUT/'selecciones.json').read_text())
    predictions=pd.read_csv(OUT/'predicciones_oof.csv.gz')
    for kind,catalog in [('inner','catalogo_interno.json'),('outer','catalogo_modelos.json')]:
        for item in json.loads((OUT/catalog).read_text()):
            assert set(item['fit']).isdisjoint(item['evaluation'])
            assert set(item['fit'])|set(item['evaluation']) <= set(frame.participant)
            fold=protocol['folds'][int(item.get('fold',item.get('choice',{}).get('fold')))-1]
            assert item['fit']==fold['inner_fit' if kind=='inner' else 'fit']
            assert item['evaluation']==fold['inner_validation' if kind=='inner' else 'evaluation']
            path=OUT/item['path']; assert digest(path)==item['sha256']; b=joblib.load(path)
            fit=frame.loc[frame.participant.isin(item['fit'])].reset_index(drop=True)
            val=frame.loc[frame.participant.isin(item['evaluation'])].reset_index(drop=True)
            prep=preprocessor().fit(fit[FULL])
            np.testing.assert_array_equal(prep.transform(fit[FULL]),b['prep'].transform(fit[FULL]))
            # Deployment uses retained signals and chronological metadata only.
            minimal=val[FULL+['participant','recording','window_start_utc']].copy()
            scores=predict(b,minimal)
            if kind=='inner':
                saved=np.load(OUT/'predicciones_internas'/(path.stem+'.npz'))
                np.testing.assert_array_equal(saved['source_row'],val.source_row)
                expected=saved['scores']
                for w in protocol['smoothing']:
                    pred=np.asarray(CLASSES)[smooth(val,scores,w).argmax(axis=1)]
                    attempts.append(dict(fold=fold['fold'],id=b['config']['id'],family=b['config']['family'],
                        epoch=b['epoch'],smoothing=w,score=metric_record(val,TARGET,pred,'classification')['macro_score']))
            else:
                choice=item['choice']; saved=predictions.loc[predictions.fold.eq(fold['fold']) & predictions.scope.eq(choice['scope'])]
                selected=next(c for c in choices if c['fold']==choice['fold'] and
                              c['scope']==('all' if choice['scope']=='repeat_current' else choice['scope']))
                for key in ['id','epoch','smoothing','score']: assert selected[key]==choice[key]
                np.testing.assert_array_equal(saved.source_row,val.source_row)
                np.testing.assert_array_equal(saved.true,val[TARGET])
                expected=saved[['score_'+c for c in CLASSES]].to_numpy()
                pred=np.asarray(CLASSES)[scores.argmax(axis=1)]
                np.testing.assert_array_equal(pred,saved.prediction)
                people.extend(dict(fold=fold['fold'],scope=choice['scope'],participant=k,score=v)
                              for k,v in individual_scores(val,TARGET,pred,'classification').items())
                fold_metrics.append(dict(fold=fold['fold'],scope=choice['scope'],
                                         **metric_record(val,TARGET,pred,'classification')))
                assert b['epoch']==choice['epoch'] and b['smoothing']==choice['smoothing']
                assert b['config']['id']==choice['id'] and b['repeat']==(choice['scope']=='repeat_current')
            np.testing.assert_allclose(scores,expected,atol=1e-7,rtol=0)
            np.testing.assert_array_equal(scores.argmax(axis=1),expected.argmax(axis=1))
            max_error=max(max_error,float(np.max(np.abs(scores-expected))))
            checked+=1
            if checked%10==0: print('Verified',checked,flush=True)
    scores=pd.DataFrame(attempts); old=pd.read_csv(OUT/'intentos.csv')
    keys=['fold','id','epoch','smoothing']
    np.testing.assert_allclose(scores.sort_values(keys).score,old.sort_values(keys).score,atol=1e-14,rtol=0)
    for c in json.loads((OUT/'selecciones.json').read_text()):
        eligible=scores.loc[scores.fold.eq(c['fold'])]
        if c['scope']!='all': eligible=eligible.loc[eligible.family.eq(c['scope'])]
        best=eligible.sort_values(['score','id','epoch','smoothing'],ascending=[False,True,True,True]).iloc[0]
        for k in ['id','epoch','smoothing']: assert best[k]==c[k]
    actual=pd.DataFrame(people); old=pd.read_csv(OUT/'metricas_participantes.csv')
    keys=['fold','scope','participant']
    np.testing.assert_allclose(actual.sort_values(keys).score,old.sort_values(keys).score,atol=1e-14,rtol=0)
    saved_metrics=pd.read_csv(OUT/'metricas_folds.csv').sort_values(['fold','scope'])
    actual_metrics=pd.DataFrame(fold_metrics).sort_values(['fold','scope'])
    for name in ['macro_score','balanced_accuracy','macro_f1','rows','participants']:
        np.testing.assert_allclose(saved_metrics[name],actual_metrics[name],atol=1e-14,rtol=0)
    assert checked==110 and len(scores)==270 and len(predictions)==4*len(frame)
    write_json(OUT/'verificacion.json',dict(models=checked,internal_scores=len(scores),
        outer_predictions=len(predictions),max_prediction_error=max_error,
        selection_verified=True,train_only_preprocessing=True,teacher_free_prediction=True,
        validation_evaluated=False,test_evaluated=False,auditor_sha256=digest(__file__)))


if __name__=='__main__': main()
