"""Reproduce predicciones externas, decisiones internas y comparaciones pareadas."""
import argparse
import json
from datetime import datetime,timezone
import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits
from entrenar_avanzados import OUT,choose
from avanzados_core import TARGET,inputs,predict,sample_weights,adjust
from temporales_core import ROOT,CLASSES,digest,write_json,metric_record,individual_scores,preprocessor
from optimizar_historial import smooth
from informe_control_historial import bootstrap,markdown


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',default=str(OUT.relative_to(ROOT)))
    args=parser.parse_args(); out=ROOT/args.output
    protocol=json.loads((out/'protocolo.json').read_text(encoding='utf-8'))
    complete=json.loads((out/'completo.json').read_text(encoding='utf-8'))
    for key,path in [('protocol_sha256','protocolo.json'),('selection_sha256','selecciones.json'),
                     ('catalog_sha256','catalogo_modelos.json'),('predictions_sha256','predicciones_oof.csv.gz')]:
        assert digest(out/path)==complete[key]
    for name,sha in protocol['sources'].items(): assert digest(ROOT/'scripts'/name)==sha
    assert digest(ROOT/'requirements_avanzados.txt')==protocol['requirements_sha256']
    dataset=ROOT/'resultados/modelado/dataset_modelado.csv'; assert digest(dataset)==protocol['dataset_sha256']
    data=pd.read_csv(dataset); data['source_row']=np.arange(len(data))
    train=data.loc[data.split.eq('train')&data[TARGET].notna()].sort_values(['participant','recording','window_start_utc']).reset_index(drop=True)
    del data
    search=pd.read_csv(out/'todos_los_intentos.csv'); assert len(search)==6480
    selections=json.loads((out/'selecciones.json').read_text(encoding='utf-8')); assert len(selections)==25
    inner=json.loads((out/'catalogo_interno.json').read_text(encoding='utf-8')); assert len(inner)==15
    for meta in inner:
        fold=protocol['folds'][meta['fold']-1]
        assert set(meta['train_participants']).isdisjoint(meta['evaluation_participants'])
        assert set(meta['train_participants'])|set(meta['evaluation_participants'])==set(fold['fit'])
        assert digest(out/meta['path'])==meta['sha256']
        arrays=np.load(out/meta['path'],allow_pickle=False)
        frame=train.loc[train.participant.isin(meta['evaluation_participants'])].reset_index(drop=True)
        np.testing.assert_array_equal(arrays['source_row'],frame.source_row)
        truth=frame[TARGET].map({c:i for i,c in enumerate(CLASSES)}).to_numpy(int)
        np.testing.assert_array_equal(truth,arrays['true'])
        weights=sample_weights(frame,'participant')
        records=search.loc[search.fold.eq(meta['fold'])&search.inner.eq(meta['inner'])]
        for index,base in enumerate(protocol['base_grid']):
            raw=arrays[f'm{index}']; np.testing.assert_allclose(raw.sum(axis=1),1,atol=1e-12)
            assert np.isfinite(raw).all() and (raw>=0).all()
            for window in protocol['smoothing']:
                smoothed=smooth(frame,raw,window)
                for row in records.loc[records.base_id.eq(base['base_id'])&records.smoothing.eq(window)].itertuples():
                    pred=(smoothed*np.exp([row.low_bias,0,row.high_bias])[None,:]).argmax(axis=1)
                    score=np.average(pred==truth,weights=weights)
                    np.testing.assert_allclose(score,row.score,rtol=1e-12,atol=1e-12)
    fields=['candidate_id','base_id','panel','context','family','weighting','smoothing','low_bias','high_bias']
    for fold in protocol['folds']:
        scores=search.loc[search.fold.eq(fold['fold'])].groupby(fields,as_index=False).score.mean()
        for scope in protocol['scopes']:
            winner=choose(scores,scope); saved=next(s for s in selections if s['fold']==fold['fold'] and s['scope']==scope)
            assert winner.candidate_id==saved['candidate_id']
    events=[json.loads(line) for line in (out/'bitacora.jsonl').read_text(encoding='utf-8').splitlines()]
    freeze=next(i for i,e in enumerate(events) if e['stage']=='selection_frozen')
    assert sum(e['stage']=='fit_completed' for e in events)==360
    assert all(i>freeze for i,e in enumerate(events) if e['stage']=='outer_completed')
    catalog=json.loads((out/'catalogo_modelos.json').read_text(encoding='utf-8')); assert len(catalog)==50
    predictions=pd.read_csv(out/'predicciones_oof.csv.gz'); people=[]; metrics=[]
    stored_people=pd.read_csv(out/'metricas_participantes.csv')
    stored_metrics=pd.read_csv(out/'metricas_folds.csv')
    scopes=list(protocol['scopes'])
    control=out/'control_global'
    if control.exists():
        cp=json.loads((control/'protocolo.json').read_text(encoding='utf-8'))
        cc=json.loads((control/'completo.json').read_text(encoding='utf-8'))
        assert digest(ROOT/'scripts/control_balanceo_global.py')==cp['source_sha256']
        assert digest(ROOT/'scripts/avanzados_core.py')==cp['core_sha256']
        assert digest(out/'control_global_plan.json')==cp['plan_sha256']
        plan=json.loads((out/'control_global_plan.json').read_text(encoding='utf-8'))
        assert plan['created_utc']<min(e['utc'] for e in events if e['stage']=='outer_completed')
        for key,path in [('selection_sha256','selecciones.json'),('catalog_sha256','catalogo_modelos.json'),('predictions_sha256','predicciones_oof.csv.gz')]:
            assert digest(control/path)==cc[key]
        assert cp['selection_sha256']==cc['selection_sha256']
        extra=json.loads((control/'selecciones.json').read_text(encoding='utf-8')); assert len(extra)==5
        for saved in extra:
            scores=search.loc[search.fold.eq(saved['fold'])&search.weighting.eq('global')].groupby(fields,as_index=False).score.mean()
            assert choose(scores,'all').candidate_id==saved['candidate_id']
        selections.extend(extra); scopes.append('global')
        extra_catalog=json.loads((control/'catalogo_modelos.json').read_text(encoding='utf-8')); assert len(extra_catalog)==10
        for meta in extra_catalog: meta['path']='control_global/'+meta['path']
        catalog.extend(extra_catalog)
        predictions=pd.concat([predictions,pd.read_csv(control/'predicciones_oof.csv.gz')],ignore_index=True)
        stored_people=pd.concat([stored_people,pd.read_csv(control/'metricas_participantes.csv')],ignore_index=True)
        stored_metrics=pd.concat([stored_metrics,pd.read_csv(control/'metricas_folds.csv')],ignore_index=True)
    for meta in catalog:
        fold=protocol['folds'][meta['fold']-1]; choice=meta['choice']
        assert meta['train_participants']==fold['fit'] and meta['evaluation_participants']==fold['evaluation']
        assert digest(out/meta['path'])==meta['sha256']
        fit=train.loc[train.participant.isin(fold['fit'])].reset_index(drop=True)
        frame=train.loc[train.participant.isin(fold['evaluation'])].reset_index(drop=True)
        bundle=joblib.load(out/meta['path']); assert bundle['choice']==choice
        xf=inputs(fit,choice['panel'],choice['context'])
        # Main training uses NumPy advanced row indexing (C contiguous). Reproduce
        # that layout: floating-point scaler reductions otherwise differ for F arrays.
        if meta['scope']!='global': xf=np.ascontiguousarray(xf)
        independently_fitted=preprocessor().fit(xf)
        np.testing.assert_array_equal(independently_fitted.transform(xf),bundle['preprocessor'].transform(xf))
        prob=predict(bundle,frame); pred=np.asarray(CLASSES)[prob.argmax(axis=1)]
        p=predictions.loc[predictions.model_id.eq(meta['model_id'])].reset_index(drop=True)
        np.testing.assert_array_equal(p.source_row,frame.source_row); np.testing.assert_array_equal(p.true,frame[TARGET])
        np.testing.assert_array_equal(p.prediction,pred)
        np.testing.assert_allclose(p[['prob_'+c for c in CLASSES]],prob,rtol=1e-12,atol=1e-12)
        identity={k:meta[k] for k in ['model_id','scope','seed','fold']}
        metrics.append(dict(**identity,**metric_record(frame,TARGET,pred,'classification')))
        people.extend(dict(**identity,participant=p,score=s) for p,s in individual_scores(frame,TARGET,pred,'classification').items())
    people=pd.DataFrame(people); checked=people.set_index(['model_id','participant'])
    stored=stored_people.set_index(['model_id','participant'])
    np.testing.assert_allclose(stored.loc[checked.index,'score'],checked.score,rtol=1e-12,atol=1e-12)
    checked=pd.DataFrame(metrics).set_index('model_id'); stored=stored_metrics.set_index('model_id')
    for col in ['macro_score','balanced_accuracy','macro_f1']:
        np.testing.assert_allclose(stored.loc[checked.index,col],checked[col],rtol=1e-12,atol=1e-12)
    by_seed=[]
    for (scope,seed),g in predictions.groupby(['scope','seed']):
        assert len(g)==len(train) and set(g.source_row)==set(train.source_row)
        by_seed.append(dict(scope=scope,seed=seed,**metric_record(g.reset_index(drop=True),'true',g.prediction.to_numpy(),'classification')))
    by_seed=pd.DataFrame(by_seed); by_seed.to_csv(out/'resumen_por_semilla.csv',index=False)
    summary=by_seed.groupby('scope',as_index=False)[['macro_score','balanced_accuracy','macro_f1']].mean()
    summary.to_csv(out/'resumen_oof.csv',index=False)
    diagnosis=[]
    for (scope,seed),g in predictions.groupby(['scope','seed']):
        for label in CLASSES:
            observed=g.loc[g.true.eq(label)]
            recall=(observed.prediction==label).groupby(observed.participant).mean()
            diagnosis.append(dict(scope=scope,seed=seed,label=label,true_rows=len(observed),
                predicted_rows=int(g.prediction.eq(label).sum()),predicted_fraction=float(g.prediction.eq(label).mean()),
                global_recall=float(observed.prediction.eq(label).mean()),participant_recall=float(recall.mean())))
    diagnosis=pd.DataFrame(diagnosis); diagnosis.to_csv(out/'diagnostico_clases.csv',index=False)
    class_summary=diagnosis.groupby(['scope','label'],as_index=False)[['predicted_fraction','global_recall','participant_recall']].mean()
    source=ROOT/'resultados/fusiones_10-09-2026_completa/metricas_participantes.csv'
    previous=pd.read_csv(source); previous=previous.loc[previous.task.eq('arousal')]
    scores=people.groupby(['scope','participant']).score.mean().unstack('scope')
    for reference in ['late_geometric','early','fixed_logistic']:
        ref=previous.loc[previous.scope.eq(reference)].groupby('participant').score.mean()
        assert set(ref.index)==set(scores.index); scores['previous_'+reference]=ref.reindex(scores.index)
    gains=[]; deltas=[]
    for scope in scopes:
        for reference in ['previous_late_geometric','previous_fixed_logistic','unadjusted']+(['global'] if 'global' in scopes else []):
            if scope==reference: continue
            delta=scores[scope]-scores[reference]; low,high=bootstrap(delta)
            gains.append(dict(scope=scope,reference=reference,mean_delta=float(delta.mean()),ci_low=low,ci_high=high,
                              positive_participants=int((delta>0).sum()),participants=len(delta)))
            deltas.extend(dict(scope=scope,reference=reference,participant=p,delta=float(d)) for p,d in delta.items())
    gains=pd.DataFrame(gains); gains.to_csv(out/'ganancias_pareadas.csv',index=False)
    pd.DataFrame(deltas).to_csv(out/'ganancias_participantes.csv',index=False)
    primary=gains.loc[gains.scope.eq('all')&gains.reference.eq('previous_late_geometric')].iloc[0]
    report=f'''# Boosting, ordinalidad y balanceo por participante: 11-09-2026

El contraste principal obtiene {summary.set_index('scope').loc['all','macro_score']:.4f} de BA macro,
frente a 0,3651 de la fusión geométrica anterior. Diferencia {100*primary.mean_delta:+.2f} puntos
porcentuales, intervalo descriptivo [{100*primary.ci_low:+.2f}; {100*primary.ci_high:+.2f}],
mejora en {primary.positive_participants}/25 personas. Interpretar junto con las limitaciones
de investigación repetida sobre train; no es validación independiente.

## Qué se cambió

- CatBoost multiclase: 300 iteraciones fijas, profundidad 4, learning rate 0,03, L2=20,
  bootstrap Bernoulli, subsample=0,8, rsm=0,8, cuatro hilos, sin early stopping ni eval_set.
- Logística nominal C=0,1 como control.
- Modelo ordinal: dos logísticas C=0,1 para P(y≥medio) y P(y≥alto). Si la segunda excede
  la primera, ambas se proyectan a su promedio; se reconstruyen tres probabilidades válidas.
- Dos ponderaciones de entrenamiento: inversa de frecuencia global de clase, o inversa
  del número de filas de la clase dentro de cada persona y del número de clases presentes
  en esa persona. Se normaliza peso medio a uno. La segunda da igual masa a cada persona
  y a cada clase observada dentro de ella; su accuracy ponderada coincide con la BA macro.
  Los pesos se calculan exclusivamente en el subconjunto de ajuste.
- Dos paneles: pupila + mirada (15) y pupila + mirada + EEG (24); ventana actual o resumen
  causal de ocho ventanas. El resumen conserva actual/media/std/diferencia con la más antigua
  y longitud. El contexto de grabación puede cruzar estímulos, sin ventanas futuras.
- Suavizado causal de probabilidades de 1/4 ventanas. Ajustes de decisión multiplicando
  por exp([bajo,0,alto]) con cada sesgo en -0,3/0/0,3 y renormalizando. Esto cambia la regla
  de predicción, no las etiquetas reales. Las salidas ajustadas no implican calibración.

Las etiquetas de activación GSR de 6 s y el split se mantienen. GSR no entra como predictor.
No se reentrena atención ni regresión. La normalización de features y pseudoetiquetas sigue
siendo offline por persona. El máximo soporte combinado de features/suavizado es de 12 s.

La configuración de CatBoost y el uso de pesos están basados en su
[API oficial](https://catboost.ai/docs/en/concepts/python-reference_catboostclassifier).
La ejecución fija CatBoost {protocol['versions']['catboost']} en `requirements_avanzados.txt`.

## Resultados de las reglas de selección

`all`: selecciona entre las 432 configuraciones. `unadjusted`: entre 24 modelos sin
suavizado ni sesgos. `participant`: entre 216 con balanceo por persona. `ordinal` y
`catboost`: entre 144 de cada familia. Todas son reglas predefinidas; no se escoge una
por su resultado externo. `global` es un comparador secundario entre las 216 configuraciones
con balanceo global, declarado antes de cualquier resultado externo. Reutiliza las mismas
puntuaciones internas y añade diez modelos. Comparar sus selecciones con `participant`
contrasta reglas completas; no aísla causalmente el efecto del peso si cambian otras opciones.
BA macro y BA global promedian métricas de dos semillas.

{markdown(summary,['scope','macro_score','balanced_accuracy','macro_f1'])}

{markdown(gains,['scope','reference','mean_delta','ci_low','ci_high','positive_participants'])}

## Distribución y acierto por clase

Fracción predicha y recall de cada clase, promediados entre semillas. El recall por persona
promedia solo personas que presentan esa clase. Una mejora de BA no garantiza que mejoren
los tres niveles; esta tabla permite identificar el coste de la regla de decisión.

{markdown(class_summary,['scope','label','predicted_fraction','global_recall','participant_recall'])}

## Selecciones por fold

{markdown(pd.DataFrame(selections),['fold','scope','panel','context','family','weighting','smoothing','low_bias','high_bias','inner_score'])}

## Protocolo y registro

Se trabaja solo con las 25 personas originales de train. Cinco folds externos de 20/5;
tres folds internos dentro de los 20. Se promedian sus BA macro dando igual peso a cada
fold interno, con desempate por identificador. Se congelan todas las elecciones antes
de evaluar externamente. Dos semillas de reajuste: 20260911/20260912; logística es
determinista en este ajuste, por lo que dos semillas no aportan dos réplicas independientes.
Imputación, indicadores de ausencia y escalado se ajustan por separado en cada entrenamiento.

360 ajustes internos de modelos (480 clasificadores contando los dos ordinales),
6.480 puntuaciones de decisión, {len(selections)} selecciones y {len(catalog)} bundles externos guardados
(50 principales y diez del control global cuando está presente).
`bitacora.jsonl` registra todos los ajustes; `todos_los_intentos.csv`, cada resultado.
Las probabilidades internas de los 24 modelos por fold se conservan en NPZ junto con
identificadores originales, y se verifican las 6.480 puntuaciones a partir de ellas.

Se recargaron los {len(catalog)} modelos y se verificaron {len(predictions):,} predicciones OOF,
{len(metrics)} métricas de fold y {len(people)} de participante. Se reconstruyeron los preprocesadores para
verificar ajuste solo en entrenamiento. `pruebas.txt` conserva las 42 pruebas aprobadas.
Los modelos internos no se guardan; sí sus predicciones, particiones y configuraciones.
Los modelos externos corresponden a 20 personas cada uno, sin ajuste final nuevo sobre 25.

## Alcance de la mejora

El objetivo es subir la BA de las etiquetas originales sin cambiar el problema para
obtener un número mayor. Los intervalos usan 2.000 remuestreos pareados de personas,
promediando semillas primero; son descriptivos, sin corrección por múltiples contrastes,
dependencia entre folds ni búsquedas repetidas. La selección anidada evita usar las personas
externas dentro del ajuste de cada ejecución, pero no elimina la adaptación entre rondas.
Validation y test originales no se vuelven a evaluar. La comparación con la fusión anterior
comparte personas externas, aunque cambia la partición interna y el método de selección.
No se puede atribuir una diferencia exclusivamente al modelo ni afirmar confirmación externa.

## Reproducción y carga

```powershell
python -m pip install -r requirements_avanzados.txt
python -m unittest discover -s tests
python scripts/entrenar_avanzados.py --output resultados/NUEVO_AVANZADO
python scripts/informe_avanzados.py --output resultados/NUEVO_AVANZADO
```

El comparador secundario de esta entrega se ejecutó con `python scripts/control_balanceo_global.py`
sobre el directorio original, después del entrenamiento principal y antes del informe.
Su declaración fechada, protocolo y resultados se conservan en `control_global_plan.json`
y `control_global/`; no vuelve a buscar configuraciones ni usa resultados externos para elegir.

Para cargar: añadir `scripts` al path, `joblib.load` de un bundle del catálogo y llamar
`avanzados_core.predict(bundle, frame)`. El frame contiene las features originales y
persona/grabación/timestamp, ordenado por esos tres campos; no requiere etiquetas.
Los parámetros de panel, contexto, ponderación y decisión están dentro del bundle.
'''
    (ROOT/'documentacion/Avanzados_11-09-2026.md').write_text(report,encoding='utf-8')
    write_json(out/'verificacion.json',dict(models_reloaded=len(catalog),predictions_verified=len(predictions),inner_scores_verified=6480,
        preprocessing_fits_verified=len(catalog),fold_metrics=len(metrics),participant_metrics=len(people),selections=len(selections),
        previous_reference_sha256=digest(source),report_script_sha256=digest(__file__),
        validation_evaluated=False,test_evaluated=False,completed_utc=datetime.now(timezone.utc).isoformat()))
    print(summary.to_string(index=False)); print(gains.to_string(index=False))


if __name__=='__main__':
    with threadpool_limits(limits=4): main()
