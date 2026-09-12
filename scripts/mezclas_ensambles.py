"""Tres mezclas fijas posteriores al diagnostico de bajo recall de la clase media."""
import argparse
import json
from datetime import datetime,timezone
import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits
from ensambles_core import predict as predict_source
from hiperparametros_core import TARGET,feature_cache
from entrenar_hiperparametros import load_train
from temporales_core import ROOT,CLASSES,digest,write_json,metric_record,individual_scores
from informe_control_historial import bootstrap,markdown

OUT=ROOT/'resultados/mezclas_ensambles_11-09-2026'
SOURCE=ROOT/'resultados/ensambles_11-09-2026'


def predict(bundle,frame,cache=None):
    if cache is None: cache=feature_cache(frame)
    weight=bundle['stack_weight']
    return (1-weight)*predict_source(bundle['pool'],frame,cache)+weight*predict_source(bundle['stack'],frame,cache)


def main():
    global OUT
    parser=argparse.ArgumentParser(); parser.add_argument('--output',default=str(OUT.relative_to(ROOT)))
    OUT=ROOT/parser.parse_args().output
    plan=json.loads((OUT/'plan.json').read_text()); plan_hash=digest(OUT/'plan.json')
    assert digest(SOURCE/'predicciones_oof.csv.gz')==plan['source_predictions_sha256']
    verified=json.loads((SOURCE/'verificacion.json').read_text())
    assert digest(ROOT/'scripts/informe_ensambles.py')==verified['report_script_sha256']
    (OUT/'modelos').mkdir(exist_ok=False)
    protocol=json.loads((SOURCE/'protocolo.json').read_text()); catalog=json.loads((SOURCE/'catalogo_modelos.json').read_text())
    write_json(OUT/'protocolo.json',dict(created_utc=datetime.now(timezone.utc).isoformat(),plan_sha256=plan_hash,
        source_verification_sha256=digest(SOURCE/'verificacion.json'),source_catalog_sha256=digest(SOURCE/'catalogo_modelos.json'),
        source_protocol_sha256=digest(SOURCE/'protocolo.json'),script_sha256=digest(__file__),
        source_core_sha256=digest(ROOT/'scripts/ensambles_core.py'),validation_evaluated=False,test_evaluated=False))
    train=load_train(); originals=pd.read_csv(SOURCE/'predicciones_oof.csv.gz')
    rows=[]; people=[]; folds=[]; models=[]
    for fold in protocol['folds']:
        val=train.loc[train.participant.isin(fold['evaluation'])].reset_index(drop=True); cache=feature_cache(val)
        for seed in protocol['seeds']:
            children={}
            for child,scope in [('pool',plan['pool_scope']),('stack',plan['stack_scope'])]:
                item=next(m for m in catalog if m['fold']==fold['fold'] and m['seed']==seed and m['scope']==scope)
                assert digest(SOURCE/item['path'])==item['sha256']
                children[child]=joblib.load(SOURCE/item['path'])
                saved=originals.loc[originals.model_id.eq(item['model_id'])].reset_index(drop=True)
                np.testing.assert_array_equal(saved.source_row,val.source_row)
                np.testing.assert_allclose(predict_source(children[child],val,cache),saved[['prob_'+c for c in CLASSES]],rtol=1e-12,atol=1e-12)
            for weight in plan['stack_weights']:
                bundle=dict(**children,stack_weight=weight); scope=f'stack_weight_{weight}'
                name=f'fold{fold["fold"]}_{scope}_{seed}'; path=OUT/'modelos'/f'{name}.joblib'
                probability=predict(bundle,val,cache); joblib.dump(bundle,path,compress=3)
                restored=predict(joblib.load(path),val,cache); np.testing.assert_array_equal(probability,restored)
                pred=np.asarray(CLASSES)[probability.argmax(axis=1)]
                identity=dict(model_id=name,fold=fold['fold'],scope=scope,seed=seed)
                models.append(dict(**identity,path=path.relative_to(OUT).as_posix(),sha256=digest(path),stack_weight=weight,
                    train_participants=fold['fit'],evaluation_participants=fold['evaluation']))
                p=val[['source_row','participant','window_start_utc']].copy(); p['true']=val[TARGET].to_numpy(); p['prediction']=pred
                for k,v in identity.items(): p[k]=v
                for i,c in enumerate(CLASSES): p['prob_'+c]=probability[:,i]
                rows.append(p); folds.append(dict(**identity,**metric_record(val,TARGET,pred,'classification')))
                people.extend(dict(**identity,participant=p,score=s) for p,s in individual_scores(val,TARGET,pred,'classification').items())
        print(f'Mezclas fold {fold["fold"]}: archivos recargados y predicciones verificadas',flush=True)
    predictions=pd.concat(rows); predictions.to_csv(OUT/'predicciones_oof.csv.gz',index=False,compression='gzip')
    write_json(OUT/'catalogo_modelos.json',models); people=pd.DataFrame(people); people.to_csv(OUT/'metricas_participantes.csv',index=False)
    pd.DataFrame(folds).to_csv(OUT/'metricas_folds.csv',index=False)
    # Verify persisted outputs and recompute aggregate metrics from their serialized rows.
    saved=pd.read_csv(OUT/'predicciones_oof.csv.gz'); np.testing.assert_array_equal(saved.prediction,predictions.prediction)
    np.testing.assert_allclose(saved[['prob_'+c for c in CLASSES]],predictions[['prob_'+c for c in CLASSES]],rtol=1e-12,atol=1e-12)
    by_seed=[]; diagnosis=[]
    for (scope,seed),g in saved.groupby(['scope','seed']):
        assert len(g)==len(train) and set(g.source_row)==set(train.source_row)
        by_seed.append(dict(scope=scope,seed=seed,**metric_record(g.reset_index(drop=True),'true',g.prediction.to_numpy(),'classification')))
        for label in CLASSES:
            subset=g.loc[g.true.eq(label)]
            diagnosis.append(dict(scope=scope,seed=seed,label=label,predicted_fraction=float(g.prediction.eq(label).mean()),recall=float(subset.prediction.eq(label).mean())))
    summary=pd.DataFrame(by_seed).groupby('scope',as_index=False)[['macro_score','balanced_accuracy','macro_f1']].mean()
    summary.to_csv(OUT/'resumen_oof.csv',index=False); pd.DataFrame(diagnosis).to_csv(OUT/'diagnostico_clases.csv',index=False)
    ref_path=ROOT/'resultados/fusiones_10-09-2026_completa/metricas_participantes.csv'
    ref=pd.read_csv(ref_path); ref=ref.loc[ref.task.eq('arousal')&ref.scope.eq('late_geometric')].groupby('participant').score.mean()
    gains=[]; deltas=[]
    for scope,g in people.groupby('scope'):
        current=g.groupby('participant').score.mean(); assert set(current.index)==set(ref.index)
        delta=current-ref; low,high=bootstrap(delta)
        gains.append(dict(scope=scope,mean_delta=float(delta.mean()),ci_low=low,ci_high=high,
            positive_participants=int((delta>1e-12).sum()),tied_participants=int((delta.abs()<=1e-12).sum())))
        deltas.extend(dict(scope=scope,participant=p,delta=float(v)) for p,v in delta.items())
    gains=pd.DataFrame(gains); gains.to_csv(OUT/'ganancias_pareadas.csv',index=False); pd.DataFrame(deltas).to_csv(OUT/'ganancias_participantes.csv',index=False)
    class_summary=pd.DataFrame(diagnosis).groupby(['scope','label'],as_index=False)[['predicted_fraction','recall']].mean()
    assert digest(OUT/'plan.json')==plan_hash
    write_json(OUT/'verificacion.json',dict(models_reloaded=30,predictions_verified=len(saved),source_models_reloaded=20,
        plan_sha256=plan_hash,protocol_sha256=digest(OUT/'protocolo.json'),script_sha256=digest(__file__),
        catalog_sha256=digest(OUT/'catalogo_modelos.json'),predictions_sha256=digest(OUT/'predicciones_oof.csv.gz'),
        previous_reference_sha256=digest(ref_path),validation_evaluated=False,test_evaluated=False,completed_utc=datetime.now(timezone.utc).isoformat()))
    report=f'''# Mezclas posteriores al diagnóstico de stacking: 11-09-2026

Se probaron tres mezclas fijas de pool_fixed_history y stack_participant_C0.01: 5 %, 10 %
y 25 % del segundo. El 10 % es el contraste principal declarado en plan.json antes de
calcular las predicciones mezcladas. Esta ronda es adaptativa: se diseñó después de
observar BA macro 0,3685 y recall de medio 0,0641 en el stacking. No es confirmación
independiente ni ajuste de pesos con una validación interna nueva.

## Resultados

Promedio de dos semillas sobre las mismas 25 personas de train, evaluadas por cinco folds.
La referencia anterior de fusión geométrica es 0,3651 de BA macro.

{markdown(summary,['scope','macro_score','balanced_accuracy','macro_f1'])}

{markdown(gains,['scope','mean_delta','ci_low','ci_high','positive_participants','tied_participants'])}

{markdown(class_summary,['scope','label','predicted_fraction','recall'])}

Los intervalos son descriptivos: 2.000 remuestreos pareados por persona, sin corregir
las búsquedas repetidas ni la dependencia entre folds. Las mejoras por persona se
cuentan con tolerancia 1e-12. Evaluar BA junto con el recall de medio evita ocultar una
pérdida de reconocimiento de esa clase detrás de una subida del promedio.

## Auditoría y archivos

No se reentrenan modelos ni se cambian etiquetas. Cada bundle contiene los dos modelos
fuente y el peso fijo; las predicciones se calculan desde esos objetos y se exigen
idénticas después de recargarlos. Se comprobaron los hashes y salidas de los 20 modelos
fuente, se recargaron los 30 bundles nuevos y se verificaron {len(saved):,} predicciones.
El guardado se volvió a leer antes de calcular los resúmenes. Protocolos, catálogo,
métricas, diagnósticos y diferencias por persona están en resultados/mezclas_ensambles_11-09-2026.

Validation y test originales no se vuelven a evaluar. Continúan las limitaciones de
normalización offline y pseudoetiquetas. No se elige retrospectivamente el mayor peso
por su resultado externo. La comparación de esta grilla pequeña sigue siendo exploratoria.

Código reproducible: scripts/mezclas_ensambles.py --output resultados/NUEVA_MEZCLA.
Requiere la ronda de ensambles y un directorio con plan.json, sin subcarpeta modelos
existente; se puede copiar el plan conservado para repetir exactamente sus pesos.
Para cargar, agregar scripts
al path, usar joblib.load y mezclas_ensambles.predict(bundle, frame), con el frame ordenado
por persona/grabación/timestamp; no necesita etiquetas. El código conserva las rutas de
los modelos fuente para mantener el linaje de esta entrega.
'''
    (ROOT/'documentacion/Mezclas_Ensambles_11-09-2026.md').write_text(report,encoding='utf-8')
    print(summary.to_string(index=False)); print(gains.to_string(index=False))


if __name__=='__main__':
    with threadpool_limits(limits=4): main()
