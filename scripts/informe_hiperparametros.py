"""Audita el barrido completo y redacta el informe de hiperparametros."""
import argparse
import json
from datetime import datetime,timezone
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold
from threadpoolctl import threadpool_limits
from entrenar_hiperparametros import load_train
from hiperparametros_core import TARGET,grid,feature_cache,predict,choose
from avanzados_core import sample_weights
from optimizar_historial import smooth
from temporales_core import ROOT,CLASSES,digest,write_json,preprocessor,metric_record,individual_scores
from informe_control_historial import bootstrap,markdown


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',default='resultados/hiperparametros_11-09-2026_paralelo')
    out=ROOT/parser.parse_args().output
    protocol=json.loads((out/'protocolo.json').read_text(encoding='utf-8'))
    complete=json.loads((out/'completo.json').read_text(encoding='utf-8'))
    for key,name in [('protocol_sha256','protocolo.json'),('selection_sha256','selecciones.json'),
                     ('catalog_sha256','catalogo_modelos.json'),('predictions_sha256','predicciones_oof.csv.gz')]:
        assert digest(out/name)==complete[key]
    for name,sha in protocol['sources'].items(): assert digest(ROOT/'scripts'/name)==sha
    runtime=protocol.get('runtime')
    execution=None
    if runtime:
        assert digest(ROOT/'scripts'/runtime['runner'])==runtime['sha256']
        assert digest(ROOT/runtime['serial_partial']/'interrupcion.json')==runtime['serial_interruption_sha256']
        partial=ROOT/runtime['serial_partial']
        inventory=json.loads((partial/'inventario_parcial.json').read_text(encoding='utf-8'))
        for item in inventory['files']:
            assert digest(partial/item['path'])==item['sha256']
        partial_events=[json.loads(line) for line in (partial/'bitacora.jsonl').read_text().splitlines()]
        assert not any(e['stage']=='outer_completed' for e in partial_events)
        execution=json.loads((out/'ejecucion_paralela.json').read_text(encoding='utf-8'))
        assert len(execution['fits'])==execution['unique_bundles_fitted']
    assert digest(ROOT/'requirements_avanzados.txt')==protocol['requirements_sha256']
    assert digest(ROOT/'resultados/modelado/dataset_modelado.csv')==protocol['dataset_sha256']
    assert digest(ROOT/'resultados/modelado/particion_participantes.csv')==protocol['partition_sha256']
    assert protocol['grid']==grid()
    train=load_train(); definitions=protocol['grid']; cache=feature_cache(train)
    search=pd.read_csv(out/'todos_los_intentos.csv'); assert len(search)==15*2*len(definitions)
    selections=json.loads((out/'selecciones.json').read_text(encoding='utf-8'))
    inner=json.loads((out/'catalogo_interno.json').read_text(encoding='utf-8')); assert len(inner)==15
    fields=['candidate_id','base_id','family','context','smoothing']
    for meta in inner:
        fold=protocol['folds'][meta['fold']-1]; outer=np.flatnonzero(train.participant.isin(fold['fit'])); fit=train.iloc[outer]
        splitter=GroupKFold(n_splits=3,shuffle=True,random_state=protocol['inner_seed']+meta['fold'])
        ii,vv=list(splitter.split(fit,groups=fit.participant))[meta['inner']-1]
        assert sorted(fit.iloc[ii].participant.unique())==meta['train_participants']
        assert sorted(fit.iloc[vv].participant.unique())==meta['evaluation_participants']
        assert set(meta['train_participants']).isdisjoint(meta['evaluation_participants'])
        assert set(meta['train_participants']).isdisjoint(fold['evaluation'])
        assert digest(out/meta['path'])==meta['sha256']
        val=fit.iloc[vv].reset_index(drop=True)
        arrays=np.load(out/meta['path'],allow_pickle=False)
        truth=val[TARGET].map({c:i for i,c in enumerate(CLASSES)}).to_numpy(int)
        np.testing.assert_array_equal(arrays['source_row'],val.source_row); np.testing.assert_array_equal(arrays['true'],truth)
        weights=sample_weights(val,'participant'); local=search.loc[search.fold.eq(meta['fold'])&search.inner.eq(meta['inner'])]
        for i,definition in enumerate(definitions):
            raw=arrays[f'm{i}']; assert np.isfinite(raw).all() and (raw>=0).all()
            np.testing.assert_allclose(raw.sum(axis=1),1,rtol=1e-12,atol=1e-12)
            for window in protocol['smoothing']:
                score=np.average(smooth(val,raw,window).argmax(axis=1)==truth,weights=weights)
                saved=local.loc[local.base_id.eq(definition['base_id'])&local.smoothing.eq(window)]
                assert len(saved)==1
                np.testing.assert_allclose(score,saved.iloc[0].score,rtol=1e-12,atol=1e-12)
    for fold in protocol['folds']:
        scores=search.loc[search.fold.eq(fold['fold'])].groupby(fields,as_index=False).score.mean()
        for scope in protocol['scopes']:
            selected=next(s for s in selections if s['fold']==fold['fold'] and s['scope']==scope)
            assert choose(scores,scope).candidate_id==selected['candidate_id']
    events=[json.loads(line) for line in (out/'bitacora.jsonl').read_text(encoding='utf-8').splitlines()]
    frozen=next(i for i,e in enumerate(events) if e['stage']=='selection_frozen')
    assert sum(e['stage']=='fit_completed' for e in events)==15*len(definitions)
    assert all(i>frozen for i,e in enumerate(events) if e['stage']=='outer_completed')
    primitive=sum(e['components'] for e in events if e['stage']=='fit_completed')
    if execution:
        assert sum(len(f['participants'])<20 for f in execution['fits'])==15*len(definitions)
        assert all(f['started_utc']>events[frozen]['utc'] for f in execution['fits'] if len(f['participants'])==20)
    print(f'Verificadas {len(search)} puntuaciones internas y {len(selections)} selecciones',flush=True)
    predictions=pd.read_csv(out/'predicciones_oof.csv.gz')
    catalog=json.loads((out/'catalogo_modelos.json').read_text(encoding='utf-8'))
    assert len(catalog)==2*len(selections)==complete['models']
    metrics=[]; people=[]; preprocessing=0; prep_checked={}; evaluation_caches={}
    for meta in catalog:
        fold=protocol['folds'][meta['fold']-1]; choice=meta['choice']; definition=choice['definition']
        assert meta['train_participants']==fold['fit'] and meta['evaluation_participants']==fold['evaluation']
        assert digest(out/meta['path'])==meta['sha256']
        bundle=joblib.load(out/meta['path'])
        assert bundle['definition']==definition and bundle['smoothing']==choice['smoothing'] and bundle['seed']==meta['seed']
        ti=np.flatnonzero(train.participant.isin(fold['fit'])); vi=np.flatnonzero(train.participant.isin(fold['evaluation']))
        val=train.iloc[vi].reset_index(drop=True)
        if meta['fold'] not in evaluation_caches:
            independent=feature_cache(val)
            for key in cache: np.testing.assert_array_equal(independent[key],cache[key][vi])
            evaluation_caches[meta['fold']]=independent
        for panel,component in bundle['components'].items():
            key=(meta['fold'],panel,definition['context'])
            xf=np.ascontiguousarray(cache[(panel,definition['context'])][ti])
            if key not in prep_checked: prep_checked[key]=preprocessor().fit(xf)
            np.testing.assert_array_equal(prep_checked[key].transform(xf),component['preprocessor'].transform(xf))
            preprocessing+=1
        score=predict(bundle,val,evaluation_caches[meta['fold']]); pred=np.asarray(CLASSES)[score.argmax(axis=1)]
        p=predictions.loc[predictions.model_id.eq(meta['model_id'])].reset_index(drop=True)
        np.testing.assert_array_equal(p.source_row,val.source_row); np.testing.assert_array_equal(p.true,val[TARGET])
        np.testing.assert_array_equal(p.prediction,pred)
        np.testing.assert_allclose(p[['score_'+c for c in CLASSES]],score,rtol=1e-12,atol=1e-12)
        identity={k:meta[k] for k in ['model_id','fold','scope','seed']}
        metrics.append(dict(**identity,**metric_record(val,TARGET,pred,'classification')))
        people.extend(dict(**identity,participant=p,score=s) for p,s in individual_scores(val,TARGET,pred,'classification').items())
    people=pd.DataFrame(people); checked=people.set_index(['model_id','participant'])
    saved=pd.read_csv(out/'metricas_participantes.csv').set_index(['model_id','participant'])
    np.testing.assert_allclose(saved.loc[checked.index,'score'],checked.score,rtol=1e-12,atol=1e-12)
    checked=pd.DataFrame(metrics).set_index('model_id'); saved=pd.read_csv(out/'metricas_folds.csv').set_index('model_id')
    for col in ['macro_score','balanced_accuracy','macro_f1']:
        np.testing.assert_allclose(saved.loc[checked.index,col],checked[col],rtol=1e-12,atol=1e-12)
    by_seed=[]; diagnosis=[]
    for (scope,seed),g in predictions.groupby(['scope','seed']):
        assert len(g)==len(train) and set(g.source_row)==set(train.source_row)
        by_seed.append(dict(scope=scope,seed=seed,**metric_record(g.reset_index(drop=True),'true',g.prediction.to_numpy(),'classification')))
        for label in CLASSES:
            observed=g.loc[g.true.eq(label)]
            diagnosis.append(dict(scope=scope,seed=seed,label=label,true_rows=len(observed),
                predicted_fraction=float(g.prediction.eq(label).mean()),global_recall=float(observed.prediction.eq(label).mean()),
                participant_recall=float((observed.prediction==label).groupby(observed.participant).mean().mean())))
    by_seed=pd.DataFrame(by_seed); by_seed.to_csv(out/'resumen_por_semilla.csv',index=False)
    summary=by_seed.groupby('scope',as_index=False)[['macro_score','balanced_accuracy','macro_f1']].mean()
    summary.to_csv(out/'resumen_oof.csv',index=False); pd.DataFrame(diagnosis).to_csv(out/'diagnostico_clases.csv',index=False)
    previous_path=ROOT/'resultados/fusiones_10-09-2026_completa/metricas_participantes.csv'
    previous=pd.read_csv(previous_path); previous=previous.loc[previous.task.eq('arousal')]
    scores=people.groupby(['scope','participant']).score.mean().unstack('scope')
    for reference in ['late_geometric','fixed_logistic']:
        ref=previous.loc[previous.scope.eq(reference)].groupby('participant').score.mean()
        assert set(ref.index)==set(scores.index); scores['previous_'+reference]=ref.reindex(scores.index)
    gains=[]; deltas=[]
    for scope in protocol['scopes']:
        for reference in ['previous_late_geometric','previous_fixed_logistic']:
            delta=scores[scope]-scores[reference]; low,high=bootstrap(delta)
            gains.append(dict(scope=scope,reference=reference,mean_delta=float(delta.mean()),ci_low=low,ci_high=high,
                positive_participants=int((delta>0).sum())))
            deltas.extend(dict(scope=scope,reference=reference,participant=p,delta=float(v)) for p,v in delta.items())
    gains=pd.DataFrame(gains); gains.to_csv(out/'ganancias_pareadas.csv',index=False)
    pd.DataFrame(deltas).to_csv(out/'ganancias_participantes.csv',index=False)
    selected=pd.DataFrame([dict(fold=s['fold'],scope=s['scope'],family=s['definition']['family'],context=s['definition']['context'],
        params=json.dumps(s['definition']['params'],sort_keys=True),smoothing=s['smoothing'],inner_score=s['inner_score']) for s in selections])
    selected.to_csv(out/'hiperparametros_elegidos.csv',index=False)
    ranking=search.groupby(fields,as_index=False).score.agg(['mean','std','min','max'])
    ranking.sort_values('mean',ascending=False).to_csv(out/'ranking_interno.csv',index=False)
    main_gain=gains.loc[gains.scope.eq('all')&gains.reference.eq('previous_late_geometric')].iloc[0]
    primary=float(summary.set_index('scope').loc['all','macro_score'])
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    names={'all':'Búsqueda conjunta','svm_rbf':'SVM RBF','hgb':'Boosting HGB','qda':'QDA',
           'fusion_logistic':'Fusión logística','fusion_lda':'Fusión LDA','fusion':'Selección entre fusiones'}
    order=protocol['scopes']; values=summary.set_index('scope').loc[order,'macro_score']
    contrast=gains.loc[gains.reference.eq('previous_late_geometric')].set_index('scope').loc[order]
    fig,axes=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
    positions=np.arange(len(order)); colors=['#17666b']+['#63788b']*(len(order)-1)
    axes[0].barh(positions,values,color=colors)
    axes[0].axvline(float(scores.previous_late_geometric.mean()),color='#ad4b37',linestyle='--',label='Fusión anterior')
    axes[0].set(yticks=positions,yticklabels=[names[k] for k in order],xlabel='BA macro por participante',xlim=(0,max(.45,values.max()+.06)))
    axes[0].invert_yaxis(); axes[0].legend(loc='upper left',bbox_to_anchor=(0,1.10),frameon=False)
    for i,v in enumerate(values): axes[0].text(v-.008,i,f'{v:.4f}',ha='right',va='center',fontsize=9,color='white')
    for i,row in enumerate(contrast.itertuples()):
        axes[1].plot([100*row.ci_low,100*row.ci_high],[i,i],color=colors[i],linewidth=2)
        axes[1].plot(100*row.mean_delta,i,'o',color=colors[i])
    axes[1].axvline(0,color='#ad4b37',linestyle='--')
    axes[1].set(yticks=positions,yticklabels=[],xlabel='Diferencia frente a fusión anterior (pp)')
    axes[1].set_ylim(axes[0].get_ylim()); axes[1].set_title('Intervalos descriptivos por participante')
    fig.suptitle('Activación: nuevos modelos e hiperparámetros')
    for extension in ['png','pdf']: fig.savefig(out/f'comparacion.{extension}',dpi=180)
    plt.close(fig)
    decision='supera numericamente' if main_gain.mean_delta>0 else 'no supera'
    uncertainty=('El intervalo incluye cero; la diferencia sigue siendo incierta.'
                 if main_gain.ci_low<=0<=main_gain.ci_high else
                 'El intervalo no incluye cero, pero el contraste sigue siendo exploratorio por las búsquedas repetidas.')
    class_summary=pd.DataFrame(diagnosis).groupby(['scope','label'],as_index=False)[['predicted_fraction','global_recall','participant_recall']].mean()
    report=f'''# Nuevos modelos e hiperparámetros: 11-09-2026

La búsqueda conjunta obtiene BA macro por participante **{primary:.4f}** y {decision} la
fusión geométrica anterior, 0,3651. Diferencia: {100*main_gain.mean_delta:+.2f} puntos
porcentuales, intervalo descriptivo [{100*main_gain.ci_low:+.2f}; {100*main_gain.ci_high:+.2f}],
con mejora en {main_gain.positive_participants}/25 personas. Las reglas por familia son
contrastes secundarios: no se elige una retrospectivamente por su puntuación externa.

{uncertainty}

## Modelos e hiperparámetros probados

| Familia | Grilla |
|---|---|
| SVM RBF exacta | C=0,1/1/10; gamma=0,1/d o 1/d, donde d es la dimensión transformada |
| Histogram Gradient Boosting | 7/15/31 hojas; perfil regular: tasa 0,03, 150 iteraciones, hoja mínima 100, L2=20; perfil flexible: tasa 0,1, 200 iteraciones, hoja mínima 30, L2=1 |
| QDA | regularización de covarianza 0,1/0,5/0,9; priors iguales |
| Fusión de logísticas | C=0,001/0,01/0,1/1; un modelo por modalidad, media geométrica igualitaria |
| Fusión de LDA | shrinkage=0,1/0,5/0,9; priors iguales y media geométrica igualitaria |

Cada configuración compara ventana actual y resumen causal de ocho ventanas. Se obtienen
44 configuraciones base; suavizar sus salidas en una o cuatro ventanas produce 88 decisiones.
Los perfiles de boosting son combinaciones predefinidas: no es un factorial completo de sus
cuatro hiperparámetros. No se aplica early stopping ni ajuste de umbrales por clase.

SVM y boosting usan pesos globales de clase; logística utiliza class_weight balanced.
QDA y LDA tienen priors uniformes. El balanceo por persona no se busca en esta ronda.
Imputación por mediana, indicadores de ausencia y escalado se ajustan solo en entrenamiento.
Cada modalidad de fusión tiene su propio preprocesador. Los modelos conjuntos reciben
las 24 variables de pupila, mirada y EEG. GSR no entra como predictor.

SVM se entrena sin calibración interna de probabilidades. Se aplica softmax a sus scores
OVR para poder suavizarlos; estas salidas son **scores normalizados, no probabilidades
calibradas**. Sin suavizado, argmax coincide con SVC usando break_ties=True. Los modelos
de fusión combinan las probabilidades emitidas por sus clasificadores sin calibración adicional.

Parámetros contrastados con las APIs oficiales de
[SVC](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html),
[HGB](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingClassifier.html)
y [QDA](https://scikit-learn.org/stable/modules/generated/sklearn.discriminant_analysis.QuadraticDiscriminantAnalysis.html).
La versión ejecutada de scikit-learn es {protocol['versions']['sklearn']}, fijada en requirements.txt.

## Resultados

`all` selecciona sobre toda la grilla; las familias restringen el espacio a esa familia;
`fusion` selecciona entre las dos familias de fusión. Las BA son promedios entre semillas.

{markdown(summary,['scope','macro_score','balanced_accuracy','macro_f1'])}

{markdown(gains,['scope','reference','mean_delta','ci_low','ci_high','positive_participants'])}

![Comparación de modelos y diferencias pareadas](../{out.relative_to(ROOT).as_posix()}/comparacion.png)

La misma figura se conserva en PDF para incorporarla a la tesis.

## Diagnóstico por clase

Recall global y promedio por persona que presenta la clase. Revisar junto con macro-F1:
una mejora del promedio no implica una mejora simultánea de los tres niveles de activación.

{markdown(class_summary,['scope','label','predicted_fraction','global_recall','participant_recall'])}

## Hiperparámetros elegidos internamente

{markdown(selected,['fold','scope','family','context','params','smoothing','inner_score'])}

## Protocolo y verificación

Se preservan las etiquetas GSR de 6 s y el split original. Solo se usan las 25 personas de
train: cinco folds externos de 20/5, con tres internos de 13/7 o 14/6 dentro de cada grupo
de 20. Se usa la misma partición interna de la ronda avanzada anterior, semilla 20260911+fold.
Se promedia BA macro de los tres folds con igual peso por fold y desempate por identificador.
Se congelan las 35 elecciones antes de evaluar externamente; dos semillas de reajuste,
20260911/20260912. Los modelos deterministas no aportan réplicas independientes por cambiar
de semilla. Las particiones por persona quedan en los manifiestos.

La ejecución completa usa cuatro procesos, con un hilo numérico por proceso. Se reutiliza
un ajuste externo cuando varias reglas seleccionan exactamente el mismo modelo, personas
y semilla. Los 70 archivos guardados corresponden a reglas de selección, no necesariamente
a 70 ajustes distintos. `ejecucion_paralela.json` conserva tiempos reales y componentes
de cada ajuste único; la bitácora principal registra cuando el proceso coordinador recoge
cada resultado. El runner y sus opciones están incluidos en el hash del protocolo.
El primer intento serial se conservó en `resultados/hiperparametros_11-09-2026/`: completó
57 ajustes antes de detenerse para acelerar la ejecución, sin evaluar folds externos.
Se repitió la misma grilla completa; ninguna configuración se cambió por sus resultados.
Ese intento parcial conserva 88 puntuaciones y salidas de su primera partición interna;
los 13 ajustes completos posteriores quedaron registrados en la bitácora, pero sus salidas
no llegaron al checkpoint por partición. La ejecución completa conserva las 1.320 puntuaciones.

Se completaron **660 bundles internos ({primitive} clasificadores)**, 1.320 puntuaciones,
35 selecciones y {len(catalog)} bundles externos. Cada fusión contiene tres clasificadores.
No se guardan estimadores internos, pero sí todas sus salidas en 15 NPZ y sus configuraciones.
La bitácora guarda inicio/fin, número de componentes y advertencias de cada ajuste.

Auditoría: {len(catalog)} bundles recargados, {len(predictions):,} predicciones reproducidas,
{preprocessing} preprocesadores verificados, {len(metrics)} métricas de fold y {len(people)}
métricas por persona recalculadas. Las 1.320 puntuaciones se reconstruyen desde las salidas
internas, y se comprueban las 35 selecciones. Las 45 pruebas están en pruebas.txt.
Los bundles externos entrenan con 20 personas cada uno; no se ajusta un modelo final nuevo
con las 25. Se conservan hashes de fuentes, dataset, partición, modelos y predicciones.

## Límites

Esta es una iteración exploratoria sobre train reutilizado. La validación anidada evita
usar etiquetas de participantes externos al elegir hiperparámetros dentro de cada fold,
pero no elimina la adaptación entre rondas. Los intervalos usan 2.000 remuestreos pareados
de personas después de promediar semillas; no corrigen búsquedas múltiples ni dependencia
entre folds. No equivalen a confirmación independiente.

La comparación con la fusión anterior comparte los participantes externos, pero cambia
la búsqueda y su partición interna; no aísla el efecto de un hiperparámetro por sí solo.

Validation y test originales no se vuelven a evaluar. Las features y pseudoetiquetas siguen
normalizadas offline por persona. El resumen y suavizado son causales dentro de grabación,
reinician ante cambios de persona, grabación o huecos y pueden cruzar estímulos; soporte
máximo combinado de 12 s. No se afirma funcionamiento en tiempo real ni superioridad temporal
solo por seleccionar contexto. Atención y regresión no se reentrenan en esta ronda.

## Reproducción

```powershell
python -m pip install -r requirements_avanzados.txt
python -m unittest discover -s tests -v
python scripts/ejecutar_hiperparametros_paralelo.py --output resultados/NUEVA_BUSQUEDA
python scripts/informe_hiperparametros.py --output resultados/NUEVA_BUSQUEDA
```

Para cargar: agregar scripts al path, joblib.load sobre un archivo del catálogo y llamar
hiperparametros_core.predict(bundle, frame). El frame debe estar ordenado por persona,
grabación y timestamp y contener las features; no necesita etiquetas. La salida sigue
el orden bajo, medio, alto. Paneles, parámetros y suavizado se guardan con el bundle.
'''
    (ROOT/'documentacion/Hiperparametros_11-09-2026.md').write_text(report,encoding='utf-8')
    write_json(out/'verificacion.json',dict(models_reloaded=len(catalog),predictions_verified=len(predictions),
        inner_scores_verified=len(search),selections_verified=len(selections),preprocessing_fits_verified=preprocessing,
        inner_bundles=15*len(definitions),inner_classifiers=primitive,fold_metrics=len(metrics),participant_metrics=len(people),
        unique_bundles_fitted=execution['unique_bundles_fitted'] if execution else None,
        previous_reference_sha256=digest(previous_path),report_script_sha256=digest(__file__),
        validation_evaluated=False,test_evaluated=False,completed_utc=datetime.now(timezone.utc).isoformat()))
    print(summary.to_string(index=False)); print(gains.to_string(index=False))


if __name__=='__main__':
    with threadpool_limits(limits=4): main()
