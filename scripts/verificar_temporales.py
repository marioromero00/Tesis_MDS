"""Auditoria independiente de cobertura, pesos, seleccion y metricas temporales."""
import json
import numpy as np
import pandas as pd
from temporales_core import (ROOT,OUT,STATIC,digest,write_json,prepare_frame,history_indices,metric_record)


def main():
    config=json.loads((OUT/'protocolo.json').read_text(encoding='utf-8'))
    catalog=json.loads((OUT/'catalogo_modelos.json').read_text(encoding='utf-8'))
    training=json.loads((OUT/'entrenamiento_completo.json').read_text(encoding='utf-8'))
    evaluation=json.loads((OUT/'evaluacion_completa.json').read_text(encoding='utf-8'))
    assert training['test_used'] is False and evaluation['test_used_for_selection'] is False
    assert digest(OUT/'seleccion_antes_test.json')==training['selection_sha256']==evaluation['selection_sha256']
    assert digest(OUT/'protocolo.json')==training['protocol_sha256']
    for name,value in config['source_hashes'].items(): assert digest(ROOT/'scripts'/name)==value
    assert digest(ROOT/'scripts/evaluar_temporales.py')==evaluation['source_sha256']
    data_path=ROOT/'resultados/modelado/dataset_modelado.csv'
    assert digest(data_path)==config['dataset_sha256']
    data=pd.read_csv(data_path);data['source_row']=np.arange(len(data))
    frames={};sequence_windows=0
    train_people=set(data.loc[data.split.eq('train'),'participant'])
    for task in config['features']:
        for split in ['train','validation','test']:
            frame=prepare_frame(data,task,config['targets'],split)
            idx,lengths=history_indices(frame,8)
            row_ids=np.arange(len(frame))
            assert (idx[row_ids,lengths-1]==row_ids).all() and (idx<=row_ids[:,None]).all()
            present=idx>=0;safe=np.maximum(idx,0)
            for column in ['split','participant','recording','segment_id','stimulus']:
                values=frame[column].to_numpy()
                assert ((values[safe]==values[:,None])|~present).all()
            ns=pd.to_datetime(frame.window_start_utc,utc=True).dt.as_unit('ns').astype('int64').to_numpy()
            assert (np.diff(ns[safe],axis=1)[present[:,1:]]==1_000_000_000).all()
            audit=pd.read_csv(OUT/f'secuencias_{task}_{split}.csv.gz')
            np.testing.assert_array_equal(audit.source_row,frame.source_row)
            np.testing.assert_array_equal(audit.history_length,lengths)
            sequence_windows+=len(frame)
            frames[(task,split)]=frame
            if split!='train': assert train_people.isdisjoint(frame.participant)
    for meta in catalog:
        assert meta['reload_verified'] and digest(OUT/meta['path'])==meta['sha256']
        assert digest(OUT/meta['preprocessor'])==meta['preprocessor_sha256']
        assert set(meta['train_participants'])==train_people
        assert meta['features']==config['features'][meta['task']][meta['subset']]
    predictions=pd.read_csv(OUT/'predicciones_temporales.csv.gz',dtype={'actual':str,'predicted':str})
    grouping=['task','kind','subset','architecture','seed','split']
    assert not predictions.duplicated(grouping+['source_row']).any()
    metrics=pd.read_csv(OUT/'metricas_temporales.csv')
    checked=0
    for key,group in predictions.groupby(grouping):
        task,kind,subset,architecture,seed,split=key
        frame=frames[(task,split)]
        ordered=group.set_index('source_row').loc[frame.source_row]
        assert len(group)==len(frame)
        target=config['targets'][task][1 if kind=='classification' else 0]
        pred=ordered.predicted.to_numpy() if kind=='classification' else ordered.predicted.to_numpy(float)
        if kind=='classification':
            np.testing.assert_array_equal(ordered.actual,frame[target])
            probs=ordered[['prob_bajo','prob_medio','prob_alto']].to_numpy(float)
            np.testing.assert_allclose(probs.sum(axis=1),1,atol=2e-7)
        else:
            np.testing.assert_allclose(ordered.actual.to_numpy(float),frame[target],rtol=1e-7)
        mask=metrics.scope.eq('all')
        for name,value in zip(grouping,key): mask &= metrics[name].eq(value)
        row=metrics.loc[mask].iloc[0]
        fresh=metric_record(frame,target,pred,kind)
        for name,value in fresh.items(): np.testing.assert_allclose(value,row[name],rtol=1e-7,atol=1e-10)
        checked+=1
    # El promedio de validation que eligio cada configuracion coincide con el registro congelado.
    choices=json.loads((OUT/'seleccion_antes_test.json').read_text(encoding='utf-8'))['models']
    for c in choices:
        part=metrics.loc[metrics.task.eq(c['task'])&metrics.kind.eq(c['kind'])&metrics.subset.eq(c['subset'])&
                         metrics.architecture.eq(c['architecture'])&metrics.split.eq('validation')&metrics.scope.eq('all')]
        assert len(part)==2
        np.testing.assert_allclose(part.macro_score.mean(),c['validation_mean'],rtol=1e-10)
    importance=pd.read_csv(OUT/'importancia_vs_baseline.csv')
    np.testing.assert_allclose(importance.temporal_importance-importance.baseline_importance,
                               importance.differential_importance,atol=1e-12)
    np.testing.assert_allclose(importance.gain_before-importance.gain_after,
                               importance.differential_importance,atol=1e-12)
    log=(OUT/'pruebas.txt').read_text(errors='replace')
    assert 'Ran 26 tests' in log and 'OK' in log
    write_json(OUT/'verificacion_entrega.json',dict(models_verified=len(catalog),tests_passed=26,
        sequence_windows_audited=sequence_windows,predictions_verified=len(predictions),metrics_recomputed=checked,
        importance_identities_verified=len(importance),test_used_for_selection=False,
        output_hashes={str(p.relative_to(OUT)):digest(p) for p in OUT.rglob('*')
                       if p.is_file() and p.name!='verificacion_entrega.json'},
        source_hashes={name:digest(ROOT/'scripts'/name) for name in
                       ['temporales_core.py','entrenar_temporales.py','evaluar_temporales.py','verificar_temporales.py']}))
    print(f'Verificados {len(catalog)} modelos, {len(predictions)} predicciones y {checked} metricas; 26 pruebas aprobadas')


if __name__=='__main__': main()
