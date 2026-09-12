"""Audita linaje OOF, componentes, combinadores y resultados de ensambles."""
import argparse
import json
import tempfile
from pathlib import Path
from datetime import datetime,timezone
import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits
from entrenar_ensambles import OUT,SOURCE,load_inner,audit_stability
from ensambles_core import BASES,pool,meta_matrix,fit_meta,combine,choose
from hiperparametros_core import TARGET,feature_cache,raw_scores
from entrenar_hiperparametros import load_train
from avanzados_core import sample_weights
from temporales_core import ROOT,CLASSES,digest,write_json,preprocessor,metric_record,individual_scores
from informe_control_historial import bootstrap,markdown


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',default=str(OUT.relative_to(ROOT)))
    out=ROOT/parser.parse_args().output
    protocol=json.loads((out/'protocolo.json').read_text()); complete=json.loads((out/'completo.json').read_text())
    for key,name in [('protocol_sha256','protocolo.json'),('selection_sha256','selecciones.json'),
                     ('catalog_sha256','catalogo_modelos.json'),('predictions_sha256','predicciones_oof.csv.gz')]:
        assert digest(out/name)==complete[key]
    for name,sha in protocol['sources'].items(): assert digest(ROOT/'scripts'/name)==sha
    for key,name in [('source_protocol_sha256','protocolo.json'),('source_inner_catalog_sha256','catalogo_interno.json'),('source_verification_sha256','verificacion.json')]:
        assert digest(SOURCE/name)==protocol[key]
    assert digest(ROOT/'requirements_avanzados.txt')==protocol['requirements_sha256']
    train=load_train(); prior=json.loads((SOURCE/'protocolo.json').read_text()); source_catalog=json.loads((SOURCE/'catalogo_interno.json').read_text())
    assert prior['dataset_sha256']==protocol['dataset_sha256'] and prior['partition_sha256']==protocol['partition_sha256']
    selections=json.loads((out/'selecciones.json').read_text()); assert len(selections)==55
    internal=pd.read_csv(out/'todos_los_intentos.csv'); assert len(internal)==900
    meta_catalog=json.loads((out/'catalogo_meta_oof.json').read_text()); matrices={}
    for fold in protocol['folds']:
        assert set(fold['fit']).isdisjoint(fold['evaluation'])
        fitting=train.loc[train.participant.isin(fold['fit'])].reset_index(drop=True)
        blocks=[]; ids=[]
        for meta in [m for m in source_catalog if m['fold']==fold['fold']]:
            assert set(meta['train_participants']).isdisjoint(meta['evaluation_participants'])
            assert set(meta['train_participants'])|set(meta['evaluation_participants'])==set(fold['fit'])
            val,probabilities=load_inner(meta,prior,train); blocks.append(meta_matrix(probabilities)); ids.extend(val.source_row.tolist())
            weights=sample_weights(val,'participant'); truth=val[TARGET].map({c:i for i,c in enumerate(CLASSES)}).to_numpy(int)
            saved=internal.loc[internal.fold.eq(fold['fold'])&internal.inner.eq(meta['inner'])].set_index('candidate_id')
            for candidate in protocol['pool_grid']:
                score=np.average(pool(val,probabilities,candidate).argmax(axis=1)==truth,weights=weights)
                np.testing.assert_allclose(saved.loc[candidate['candidate_id'],'score'],score,rtol=1e-12,atol=1e-12)
        assert len(ids)==len(set(ids))==len(fitting) and set(ids)==set(fitting.source_row)
        x=np.ascontiguousarray(np.concatenate(blocks)[pd.Index(ids).get_indexer(fitting.source_row)])
        m=next(m for m in meta_catalog if m['fold']==fold['fold']); assert digest(out/m['path'])==m['sha256']
        stored=np.load(out/m['path'],allow_pickle=False)
        np.testing.assert_array_equal(stored['source_row'],fitting.source_row); np.testing.assert_array_equal(stored['x'],x)
        matrices[fold['fold']]=x
        scores=internal.loc[internal.fold.eq(fold['fold'])].groupby(['candidate_id','family'],as_index=False).score.mean()
        for scope in protocol['scopes'][:3]:
            saved=next(c for c in selections if c['fold']==fold['fold'] and c['scope']==scope)
            assert choose(scores,scope).candidate_id==saved['pool']['candidate_id']
        for choice in [s for s in selections if s['fold']==fold['fold']]:
            if choice['kind']=='stack':
                expected=next(s for s in protocol['stacks'] if s['scope']==choice['scope'])
                assert all(choice[k]==v for k,v in expected.items())
            elif choice['scope'].startswith('pool_fixed_'):
                p=choice['pool']; assert p['family']=='both' and p['aggregation']=='mean' and p['smoothing']==1
                assert p['history_weight']==(1. if choice['scope']=='pool_fixed_history' else .5)
    with tempfile.TemporaryDirectory() as temporary:
        audit_stability(Path(temporary),train)
        for name in ['auditoria_seleccion.csv','auditoria_ranking.csv','referencias_constantes.csv']:
            pd.testing.assert_frame_equal(pd.read_csv(out/name),pd.read_csv(Path(temporary)/name),check_exact=False,rtol=1e-12,atol=1e-12)
    events=[json.loads(line) for line in (out/'bitacora.jsonl').read_text().splitlines()]
    freeze=next(i for i,e in enumerate(events) if e['stage']=='selection_frozen')
    assert sum(e['stage']=='base_fit_completed' for e in events)==140
    assert sum(e['stage']=='meta_fit_completed' for e in events)==60
    assert all(i>freeze for i,e in enumerate(events) if e['stage'].startswith(('base_fit','meta_fit','outer_')))
    print('Linaje OOF, 900 puntuaciones, elecciones y auditoria de estabilidad verificados',flush=True)
    catalog=json.loads((out/'catalogo_modelos.json').read_text()); assert len(catalog)==110
    predictions=pd.read_csv(out/'predicciones_oof.csv.gz'); cache=feature_cache(train)
    checked_bases={}; checked_prep={}; evaluation_cache={}; meta_count=0; metrics=[]; people=[]; coefficient_rows=[]
    for item in catalog:
        fold=protocol['folds'][item['fold']-1]
        assert item['train_participants']==fold['fit'] and item['evaluation_participants']==fold['evaluation']
        assert digest(out/item['path'])==item['sha256']
        bundle=joblib.load(out/item['path']); assert bundle['choice']==item['choice'] and bundle['seed']==item['seed']
        ti=np.flatnonzero(train.participant.isin(fold['fit'])); vi=np.flatnonzero(train.participant.isin(fold['evaluation']))
        fit=train.iloc[ti].reset_index(drop=True); val=train.iloc[vi].reset_index(drop=True)
        if item['fold'] not in evaluation_cache:
            own=feature_cache(val)
            for key in cache: np.testing.assert_array_equal(own[key],cache[key][vi])
            evaluation_cache[item['fold']]=own
        probabilities={}
        for name,base in bundle['bases'].items():
            key=(item['fold'],item['seed'],name); fingerprint=joblib.hash(base)
            assert base['definition']==next(d for d in BASES if d['base_id']==name)
            if key not in checked_bases:
                for panel,component in base['components'].items():
                    prep_key=(item['fold'],panel,base['definition']['context'])
                    x=np.ascontiguousarray(cache[(panel,base['definition']['context'])][ti])
                    if prep_key not in checked_prep: checked_prep[prep_key]=preprocessor().fit(x)
                    np.testing.assert_array_equal(checked_prep[prep_key].transform(x),component['preprocessor'].transform(x))
                probability=raw_scores(base,evaluation_cache[item['fold']],np.arange(len(val)))
                checked_bases[key]=(fingerprint,probability)
            assert fingerprint==checked_bases[key][0]
            probabilities[name]=checked_bases[key][1]
        if bundle['choice']['kind']=='stack':
            # Refit the complete meta pipeline from OOF data, not just its scaler.
            fitted=fit_meta(matrices[item['fold']],fit,TARGET,bundle['choice'],item['seed'])
            np.testing.assert_array_equal(fitted['scale'].mean_,bundle['meta']['scale'].mean_)
            np.testing.assert_array_equal(fitted['scale'].scale_,bundle['meta']['scale'].scale_)
            np.testing.assert_array_equal(fitted['model'].coef_,bundle['meta']['model'].coef_)
            np.testing.assert_array_equal(fitted['model'].intercept_,bundle['meta']['model'].intercept_)
            meta_count+=1
            columns=[(d['base_id'],c) for d in BASES for c in CLASSES]
            for cls,coef in zip(fitted['model'].classes_,fitted['model'].coef_):
                coefficient_rows.extend(dict(model_id=item['model_id'],target_class=cls,base_id=k,input_class=c,coefficient=float(v)) for (k,c),v in zip(columns,coef))
        score=combine(val,probabilities,bundle['choice'],bundle['meta']); pred=np.asarray(CLASSES)[score.argmax(axis=1)]
        stored=predictions.loc[predictions.model_id.eq(item['model_id'])].reset_index(drop=True)
        np.testing.assert_array_equal(stored.source_row,val.source_row); np.testing.assert_array_equal(stored.true,val[TARGET])
        np.testing.assert_array_equal(stored.prediction,pred)
        np.testing.assert_allclose(stored[['prob_'+c for c in CLASSES]],score,rtol=1e-12,atol=1e-12)
        identity={k:item[k] for k in ['model_id','fold','scope','seed']}
        metrics.append(dict(**identity,**metric_record(val,TARGET,pred,'classification')))
        people.extend(dict(**identity,participant=p,score=s) for p,s in individual_scores(val,TARGET,pred,'classification').items())
    assert len(checked_bases)==140 and meta_count==60
    coeff_keys=['model_id','target_class','base_id','input_class']
    expected=pd.DataFrame(coefficient_rows).set_index(coeff_keys); stored=pd.read_csv(out/'coeficientes_meta.csv').set_index(coeff_keys)
    np.testing.assert_allclose(stored.loc[expected.index,'coefficient'],expected.coefficient,rtol=1e-12,atol=1e-12)
    people=pd.DataFrame(people); expected=people.set_index(['model_id','participant'])
    stored=pd.read_csv(out/'metricas_participantes.csv').set_index(['model_id','participant'])
    np.testing.assert_allclose(stored.loc[expected.index,'score'],expected.score,rtol=1e-12,atol=1e-12)
    expected=pd.DataFrame(metrics).set_index('model_id'); stored=pd.read_csv(out/'metricas_folds.csv').set_index('model_id')
    for col in ['macro_score','balanced_accuracy','macro_f1']:
        np.testing.assert_allclose(stored.loc[expected.index,col],expected[col],rtol=1e-12,atol=1e-12)
    by_seed=[]; diagnosis=[]
    for (scope,seed),g in predictions.groupby(['scope','seed']):
        assert len(g)==len(train) and set(g.source_row)==set(train.source_row)
        by_seed.append(dict(scope=scope,seed=seed,**metric_record(g.reset_index(drop=True),'true',g.prediction.to_numpy(),'classification')))
        for label in CLASSES:
            observed=g.loc[g.true.eq(label)]
            diagnosis.append(dict(scope=scope,seed=seed,label=label,predicted_fraction=float(g.prediction.eq(label).mean()),
                global_recall=float(observed.prediction.eq(label).mean()),participant_recall=float((observed.prediction==label).groupby(observed.participant).mean().mean())))
    by_seed=pd.DataFrame(by_seed); by_seed.to_csv(out/'resumen_por_semilla.csv',index=False)
    summary=by_seed.groupby('scope',as_index=False)[['macro_score','balanced_accuracy','macro_f1']].mean()
    summary.to_csv(out/'resumen_oof.csv',index=False); pd.DataFrame(diagnosis).to_csv(out/'diagnostico_clases.csv',index=False)
    scores=people.groupby(['scope','participant']).score.mean().unstack('scope'); reference_files={}
    for name,path,scope in [('previous_geometric',ROOT/'resultados/fusiones_10-09-2026_completa/metricas_participantes.csv','late_geometric'),
                            ('previous_tuned_logistic',SOURCE/'metricas_participantes.csv','fusion_logistic')]:
        ref=pd.read_csv(path)
        if 'task' in ref: ref=ref.loc[ref.task.eq('arousal')]
        ref=ref.loc[ref.scope.eq(scope)].groupby('participant').score.mean(); assert set(ref.index)==set(scores.index)
        scores[name]=ref.reindex(scores.index); reference_files[path.relative_to(ROOT).as_posix()]=digest(path)
    gains=[]; deltas=[]
    for scope in protocol['scopes']:
        for reference in ['previous_geometric','previous_tuned_logistic']:
            delta=scores[scope]-scores[reference]; lo,hi=bootstrap(delta)
            gains.append(dict(scope=scope,reference=reference,mean_delta=float(delta.mean()),ci_low=lo,ci_high=hi,
                positive_participants=int((delta>1e-12).sum()),tied_participants=int((delta.abs()<=1e-12).sum())))
            deltas.extend(dict(scope=scope,reference=reference,participant=p,delta=float(v)) for p,v in delta.items())
    gains=pd.DataFrame(gains); gains.to_csv(out/'ganancias_pareadas.csv',index=False); pd.DataFrame(deltas).to_csv(out/'ganancias_participantes.csv',index=False)
    stability=pd.read_csv(out/'auditoria_seleccion.csv'); rank=pd.read_csv(out/'auditoria_ranking.csv')
    primary=gains.loc[gains.scope.eq('pool_selected')&gains.reference.eq('previous_geometric')].iloc[0]
    value=summary.set_index('scope').loc['pool_selected','macro_score']
    best=summary.sort_values('macro_score',ascending=False).iloc[0]
    class_summary=pd.DataFrame(diagnosis).groupby(['scope','label'],as_index=False)[['predicted_fraction','global_recall']].mean()
    chosen=pd.DataFrame([dict(fold=s['fold'],scope=s['scope'],candidate=s['pool']['candidate_id'],inner_score=s['inner_score']) for s in selections if s['kind']=='pool'])
    chosen.to_csv(out/'combinaciones_elegidas.csv',index=False)
    report=f'''# Auditoría de selección y ensambles: 11-09-2026

El contraste principal, selección interna de promedios, obtiene BA macro **{value:.4f}**.
Frente a la fusión geométrica anterior (0,3651), la diferencia es {100*primary.mean_delta:+.2f}
puntos porcentuales, intervalo descriptivo [{100*primary.ci_low:+.2f}; {100*primary.ci_high:+.2f}],
con mejora en {primary.positive_participants}/25 personas. El mayor promedio observado entre
los contrastes de esta ronda es {best.macro_score:.4f}, de {best.scope}; no se convierte por
ello en una elección validada independientemente.

## Qué mostró la auditoría de selección anterior

La auditoría numérica anterior verificó modelos y métricas. Esta auditoría adicional
examina cuánto cambia el ranking de configuraciones entre particiones internas.
Un empate cuenta como acuerdo con el ganador; una brecha interna-externa también refleja
que se evalúan personas distintas y no estima por sí sola el sesgo de sobreajuste.

{markdown(stability,['fold','scope','runner_up_margin','inner_winner_agreements','inner_score','outer_score','inner_outer_gap'])}

La correlación de Spearman media entre rankings internos es {rank.spearman.mean():.4f};
el detalle por fold y par está en auditoria_ranking.csv. Estos diagnósticos se recalcularon.
Las tres reglas constantes de referencias_constantes.csv explicitan el nivel trivial
con la métrica por persona y sus clases observadas; no se selecciona una constante por
su resultado externo. No se presupone que toda regla constante tenga BA macro 1/3.

## Qué se probó

- Promedio aritmético o geométrico de varias regularizaciones de fusión logística
  (C=0,001/0,01/0,1/1) y LDA (shrinkage=0,1/0,5/0,9), por separado o juntas.
- Ventana actual, historial de ocho ventanas y mezclas de ambos: peso del historial
  0/0,25/0,5/0,75/1. Suavizado causal de una o cuatro ventanas. Son 60 configuraciones.
  En la mezcla conjunta, cada modelo de una escala recibe el mismo peso: logística
  representa 4/7 y LDA 3/7 del peso de esa escala.
- Tres reglas seleccionadas internamente: pool_selected, pool_logistic y pool_lda.
  Dos controles fijos: promedio de los siete modelos con historial y promedio de los
  catorce modelos entre ambas escalas, ambos sin suavizado adicional.
- Stacking: una logística recibe las 42 probabilidades de 14 modelos base. Se fijan
  seis contrastes (C=0,001/0,01/0,1, pesos globales o por persona), sin elegir C ni pesos
  usando los resultados externos. No se aplica suavizado adicional al stacking.

Cada modelo base ya fusiona geométricamente pupila, mirada y EEG. No se introduce GSR
como predictor ni se cambian etiquetas. Los coeficientes del combinador están guardados;
son asociaciones con salidas de modelos correlacionadas, no importancia causal de sensores.

El stacking usa exclusivamente predicciones OOF de las personas de ajuste: cada fila fue
predicha por modelos base entrenados sin esa persona. La matriz se conserva y su linaje
se verifica contra los NPZ originales. El combinador se ajusta en las 20 personas del fold;
los modelos base se reajustan en esas 20 para predecir las cinco externas. No se utiliza
la opción prefit con predicciones sobre las mismas filas usadas para ajustar los modelos.
Este diseño sigue el principio de entrenamiento cruzado de la
[documentación oficial de stacking](https://scikit-learn.org/stable/auto_examples/ensemble/plot_stack_predictors.html),
implementando explícitamente las particiones por persona. Las probabilidades resultantes
no cuentan con una calibración externa independiente.

## Resultados

Promedio de dos semillas; los clasificadores deterministas no generan dos réplicas
independientes por cambiar la semilla.

{markdown(summary,['scope','macro_score','balanced_accuracy','macro_f1'])}

{markdown(gains,['scope','reference','mean_delta','ci_low','ci_high','positive_participants'])}

{markdown(class_summary,['scope','label','predicted_fraction','global_recall'])}

## Combinaciones elegidas

{markdown(chosen,['fold','scope','candidate','inner_score'])}

## Registro y verificación

Se reutilizan las predicciones internas verificadas de la ronda de hiperparámetros;
no se repiten sus 660 ajustes. Se recalculan 900 puntuaciones de combinaciones y se
congelan 55 elecciones o definiciones antes de evaluar externamente: 15 seleccionadas,
10 controles fijos y 30 definiciones de stacking.

Reajuste externo: 140 modelos base, que contienen 420 clasificadores por modalidad,
y 60 combinadores. Se conservan 110 bundles completos que incluyen sus modelos base,
{len(predictions):,} predicciones, cinco matrices meta-OOF y 7.560 coeficientes.

Auditoría: se recargaron todos los bundles; se verificaron los 140 modelos base únicos
y sus 420 preprocesadores. Las copias compartidas se contrastaron mediante hash de
objetos antes de reutilizar su predicción verificada. Se reajustaron los 60 combinadores
desde sus matrices OOF y se exigió igualdad exacta de escalado, coeficientes e interceptos.
Se reprodujeron las predicciones y se recalcularon 110 métricas de fold y 550 de persona.
Las 47 pruebas están en pruebas.txt. Catálogos, hashes y bitácora acompañan los resultados.

## Límites

Esta ronda es adaptativa: se diseñó después de observar las rondas anteriores sobre
las mismas personas de train. La selección interna y el stacking OOF evitan fugas dentro
del ajuste, pero no convierten esta exploración repetida en confirmación independiente.
Los intervalos usan 2.000 remuestreos pareados de personas, promediando semillas primero,
sin corrección por múltiples contrastes ni dependencia entre folds. Una subida puntual
no confirma superioridad estable ni demuestra que el historial explique la mejora.
Al contar personas que mejoran se usa tolerancia 1e-12 para no contar redondeos como ganancias.

Validation y test originales no se evalúan de nuevo. Las features y pseudoetiquetas
siguen normalizadas offline por persona; el contexto causal puede cruzar estímulos
dentro de una grabación, con soporte máximo de 12 s contando el suavizado. No se entrena
atención ni regresión, ni se ajusta un modelo final nuevo sobre las 25 personas.

## Reproducción

```powershell
python -m pip install -r requirements_avanzados.txt
python -m unittest discover -s tests -v
python scripts/entrenar_ensambles.py --output resultados/NUEVO_ENSAMBLE
python scripts/informe_ensambles.py --output resultados/NUEVO_ENSAMBLE
```

Se requiere la ronda de hiperparámetros conservada en el repositorio. Para cargar,
agregar scripts al path, usar joblib.load y ensambles_core.predict(bundle, frame).
El frame contiene las features y persona/grabación/timestamp, ordenados por esos campos;
no necesita etiquetas. La salida sigue el orden bajo, medio, alto.
'''
    (ROOT/'documentacion/Ensambles_11-09-2026.md').write_text(report,encoding='utf-8')
    write_json(out/'verificacion.json',dict(models_reloaded=110,unique_bases_verified=140,base_preprocessors_verified=420,
        meta_pipelines_refitted=60,meta_coefficients_verified=len(coefficient_rows),predictions_verified=len(predictions),
        inner_scores_verified=900,definitions_verified=55,fold_metrics=110,participant_metrics=550,
        references=reference_files,report_script_sha256=digest(__file__),validation_evaluated=False,test_evaluated=False,
        completed_utc=datetime.now(timezone.utc).isoformat()))
    print(summary.to_string(index=False)); print(gains.to_string(index=False))


if __name__=='__main__':
    with threadpool_limits(limits=4): main()
