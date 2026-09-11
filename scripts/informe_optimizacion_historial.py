"""Audita y resume la busqueda anidada sin seleccionar con resultados externos."""
import json
import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits
from optimizar_historial import OUT, TARGET, FEATURES, represent, smooth, probabilities, select
from control_historial import TARGETS
from temporales_core import ROOT, CLASSES, digest, write_json, prepare_frame, metric_record, individual_scores
from informe_control_historial import bootstrap, markdown


def main():
    protocol=json.loads((OUT/'protocolo.json').read_text(encoding='utf-8'))
    complete=json.loads((OUT/'completo.json').read_text(encoding='utf-8'))
    catalog=json.loads((OUT/'catalogo_modelos.json').read_text(encoding='utf-8'))
    assert len(catalog)==40
    for name,sha in protocol['sources'].items(): assert digest(ROOT/'scripts'/name)==sha
    for key,path in [('selection_sha256','selecciones.json'),('protocol_sha256','protocolo.json'),
                     ('catalog_sha256','catalogo_modelos.json'),('predictions_sha256','predicciones_oof.csv.gz')]:
        assert complete[key]==digest(OUT/path)
    dataset=ROOT/'resultados/modelado/dataset_modelado.csv'
    assert digest(dataset)==protocol['dataset_sha256']
    data=pd.read_csv(dataset); data['source_row']=np.arange(len(data))
    train=prepare_frame(data.loc[data.split.eq('train')], 'arousal_primary_6s',TARGETS,'train')
    train=train.sort_values(['participant','recording','window_start_utc']).reset_index(drop=True)
    del data
    predictions=pd.read_csv(OUT/'predicciones_oof.csv.gz')
    search=pd.read_csv(OUT/'busqueda_interna.csv')
    choices=json.loads((OUT/'selecciones.json').read_text(encoding='utf-8'))
    assert len(search)==1575 and len(choices)==20
    for fold in protocol['folds']:
        group=search.loc[search.fold.eq(fold['fold'])]
        for row in group.itertuples():
            fit=set(row.fit_participants.split('|')); val=set(row.evaluation_participants.split('|'))
            assert fit.isdisjoint(val) and fit|val==set(fold['fit'])
            assert (fit|val).isdisjoint(fold['evaluation'])
        scores=group.groupby(['representation','estimator','smoothing'],as_index=False).score.mean()
        for choice in [c for c in choices if c['fold']==fold['fold'] and c['scope']!='fixed_logistic']:
            best=select(scores,choice['scope'])
            assert [choice[k] for k in ['representation','estimator','smoothing']]==[best.representation,best.estimator,int(best.smoothing)]
    matrices={r:represent(train,r) for r in protocol['representations']}
    people=[]; fold_metrics=[]
    for meta in catalog:
        fold=protocol['folds'][meta['fold']-1]
        assert meta['train_participants']==fold['fit'] and meta['evaluation_participants']==fold['evaluation']
        ix=np.flatnonzero(train.participant.isin(fold['evaluation']))
        frame=train.iloc[ix].reset_index(drop=True)
        assert digest(OUT/meta['path'])==meta['sha256']
        model=joblib.load(OUT/meta['path'])
        prob=smooth(frame,probabilities(model,matrices[meta['representation']][ix]),meta['smoothing'])
        prediction=np.asarray(CLASSES)[prob.argmax(axis=1)]
        saved=predictions.loc[predictions.model_id.eq(meta['model_id'])].reset_index(drop=True)
        np.testing.assert_array_equal(saved.source_row,frame.source_row)
        np.testing.assert_array_equal(saved[TARGET],frame[TARGET])
        np.testing.assert_array_equal(saved.prediction,prediction)
        np.testing.assert_allclose(saved[['prob_'+c for c in CLASSES]],prob,rtol=1e-12,atol=1e-12)
        ident={k:meta[k] for k in ['model_id','scope','fold','seed']}
        fold_metrics.append(dict(**ident,**metric_record(frame,TARGET,prediction,'classification')))
        people.extend(dict(**ident,participant=p,score=s) for p,s in individual_scores(frame,TARGET,prediction,'classification').items())
    people=pd.DataFrame(people)
    old=pd.read_csv(OUT/'metricas_participantes.csv').set_index(['model_id','participant'])
    checked=people.set_index(['model_id','participant'])
    np.testing.assert_allclose(old.loc[checked.index,'score'],checked.score,rtol=1e-12,atol=1e-12)
    fm=pd.DataFrame(fold_metrics).set_index('model_id'); stored=pd.read_csv(OUT/'metricas_folds.csv').set_index('model_id')
    np.testing.assert_allclose(fm[['macro_score','balanced_accuracy','macro_f1']],stored.loc[fm.index,['macro_score','balanced_accuracy','macro_f1']],rtol=1e-12,atol=1e-12)
    by_seed=[]
    for (scope,seed),g in predictions.groupby(['scope','seed']):
        assert len(g)==len(train) and not g.source_row.duplicated().any()
        assert set(g.source_row)==set(train.source_row)
        by_seed.append(dict(scope=scope,seed=seed,**metric_record(g.reset_index(drop=True),TARGET,g.prediction.to_numpy(),'classification')))
    by_seed=pd.DataFrame(by_seed); by_seed.to_csv(OUT/'resumen_por_semilla.csv',index=False)
    summary=by_seed.groupby('scope',as_index=False)[['macro_score','balanced_accuracy','macro_f1']].mean()
    summary.to_csv(OUT/'resumen_oof.csv',index=False)
    scores=people.groupby(['scope','participant']).score.mean().unstack('scope')
    previous_path=ROOT/'resultados/control_historial_08-09-2026/metricas_participantes.csv'
    previous=pd.read_csv(previous_path)
    previous=previous.loc[previous.kind.eq('classification')]
    for arch,mode in [('MLP_current','current'),('LSTM','history'),('BiLSTM','history')]:
        p=previous.loc[previous.architecture.eq(arch)&previous['mode'].eq(mode)].groupby('participant').score.mean()
        assert set(p.index)==set(scores.index)
        scores['previous_'+arch]=p.reindex(scores.index)
    gains=[]; deltas=[]
    for scope in ['all','temporal','current']:
        for reference in ['fixed_logistic','current','previous_MLP_current','previous_LSTM','previous_BiLSTM']:
            if scope==reference: continue
            delta=scores[scope]-scores[reference]; low,high=bootstrap(delta)
            gains.append(dict(scope=scope,reference=reference,mean_delta=float(delta.mean()),ci_low=low,ci_high=high,
                              positive_participants=int((delta>0).sum()),participants=len(delta)))
            deltas.extend(dict(scope=scope,reference=reference,participant=p,delta=float(d)) for p,d in delta.items())
    gains=pd.DataFrame(gains); gains.to_csv(OUT/'ganancias_pareadas.csv',index=False)
    pd.DataFrame(deltas).to_csv(OUT/'ganancias_participantes.csv',index=False)
    primary=gains.loc[gains.scope.eq('all')&gains.reference.eq('fixed_logistic')].iloc[0]
    description=('La búsqueda mejora el promedio frente a logística fija' if primary.mean_delta>0 else
                 'La búsqueda no mejora el promedio frente a logística fija')
    uncertainty=('El intervalo descriptivo incluye cero.' if primary.ci_low<=0<=primary.ci_high else
                 'El intervalo descriptivo no incluye cero; sigue siendo un contraste exploratorio.')
    report=f'''# Iteración de representación y modelos: 08-09-2026

{description}: diferencia de **{primary.mean_delta*100:+.2f} puntos porcentuales** de BA macro
por participante, intervalo descriptivo del 95% [{primary.ci_low*100:+.2f}; {primary.ci_high*100:+.2f}].
Mejora en {primary.positive_participants}/25 participantes. {uncertainty}

Complementa el [control del historial pupilar](Control_Historial_Pupilar_08-09-2026.md).
Esta iteración se concentra en clasificación de activación, manteniendo las cinco variables
pupilares y las etiquetas GSR de 6 s. No reentrena atención ni regresión.

## Resultados fuera del ajuste

`all`: selección entre 105 candidatos. `temporal`: selección entre 100 que usan pasado.
`current`: selección entre cinco modelos de ventana actual sin suavizado.
`fixed_logistic`: control anterior, logística balanceada C=1 con cinco entradas actuales.
Se evalúan las cuatro reglas completas de selección; no se elige una por su resultado OOF.

{markdown(summary,['scope','macro_score','balanced_accuracy','macro_f1'])}

BA macro da igual peso a cada persona; BA global agrupa ventanas. Ambas promedian métricas
de dos semillas, no probabilidades. Las configuraciones deterministas pueden coincidir
entre semillas; las dos semillas no equivalen a dos muestras independientes.

{markdown(gains,['scope','reference','mean_delta','ci_low','ci_high','positive_participants'])}

## Búsqueda y controles

Se congelaron 105 candidatos antes de evaluar: siete representaciones por cinco modelos y
tres tamaños de suavizado de probabilidades (1, 4 u 8). Representaciones: ventana actual
y resúmenes causales de 4, 8 o 16 ventanas, limitados al segmento o a la grabación.
Las cinco variables son {', '.join('`'+f+'`' for f in FEATURES)}.
Cada resumen agrega media, desviación estándar, diferencia entre actual y más antigua
y longitud disponible normalizada, junto con las cinco entradas actuales: 21 columnas.

Modelos: logística balanceada C=0,01/0,1/1; HistGradientBoosting con 100 iteraciones,
siete hojas, learning rate 0,05, mínimo 50 filas por hoja y L2=10; aproximación Nyström
RBF de 128 componentes, gamma=1/número de columnas y logística C=0,1.
HGB tiene early stopping desactivado. Imputadores, escaladores, aproximación RBF y
clasificadores se ajustan solo con las personas de cada entrenamiento.

Cinco folds externos de 20/5 personas, dentro de train original. Cada grupo de 20 realiza
tres folds internos agrupados. La selección promedia las tres BA macro internas, dando
igual peso a cada fold (tienen 6 o 7 personas de evaluación), con desempate determinista.
Se completan y congelan las selecciones de todos los folds antes de la primera evaluación
externa. Reajuste de cada selección sobre sus 20 personas, con semillas 20260908/20260909.
Se registran 525 ajustes internos y 1.575 puntuaciones, incluidos los intentos que pierden.

Las representaciones son funciones deterministas de las entradas de una sola persona;
se pueden calcular antes de dividir personas. El contexto de grabación permite cruzar
estímulos, pero reinicia ante huecos distintos de 1 s, cambio de grabación o persona.
No usa pseudoetiquetas pasadas. El suavizado usa probabilidades del pasado y del presente.
El soporte máximo puede alcanzar 24 s al combinar 16 ventanas con suavizado de ocho.

## Selecciones internas

{markdown(pd.DataFrame(choices),['fold','scope','representation','estimator','smoothing','inner_score'])}

## Interpretación y límites

El contraste principal es la regla `all` frente a logística fija. Una mejora de `all`
puede venir de modelo, regularización, representación o suavizado. `temporal` frente a
`current` compara dos búsquedas de tamaños diferentes; tampoco aísla causalmente el historial.
Las comparaciones con MLP/LSTM/BiLSTM previas usan las mismas 25 personas y promedian semillas
por persona, pero cambian el procedimiento de selección; se incluyen como referencias.

Intervalos mediante 2.000 remuestreos pareados de participantes tras promediar semillas.
Son descriptivos, sin ajuste por múltiples comparaciones ni por dependencia entre folds.
Estos participantes ya se han usado en investigaciones anteriores: la validación anidada
protege la selección dentro de esta ejecución, pero no elimina el sesgo de adaptación entre
iteraciones del proyecto. Validation y test originales no se vuelven a predecir ni evaluar.
Una mejora aquí debe confirmarse con participantes nuevos antes de sostener generalización.
Las features y pseudoetiquetas heredan normalización offline por persona.

## Entrega

40 pipelines externos guardados y recargados; 108.192 predicciones OOF verificadas,
40 métricas de fold y 200 métricas por participante recalculadas. Las curvas de búsqueda
y selecciones quedan disponibles aunque el contraste no mejore. Los 525 modelos internos
no conservan pesos; se conservan sus configuraciones, particiones y puntuaciones.
Las pruebas completas están en `pruebas.txt` (33 aprobadas al cierre de las tres iteraciones).

[Resultados y modelos](../resultados/optimizacion_historial_08-09-2026/).
`catalogo_modelos.json` indica representación, suavizado, participantes y hash de cada pipeline.
Para cargar: reconstruir `represent(frame, meta['representation'])`, cargar con `joblib.load`,
ordenar probabilidades con `probabilities` y aplicar `smooth(frame, prob, meta['smoothing'])`.
El frame debe estar ordenado por persona, grabación y timestamp. Los archivos `.joblib`
incluyen imputación/escalado/clasificador; la transformación causal se aplica externamente.

```powershell
python -m unittest discover -s tests
python scripts/optimizar_historial.py --output resultados/NUEVA_EJECUCION
```

El informe y auditoría de esta entrega se ejecutan con
`python scripts/informe_optimizacion_historial.py` sobre la ruta fechada original.
'''
    later=[]
    for directory,title in [('segunda_iteracion','Combinación de probabilidades'),('tercera_iteracion','Fusión de mirada y EEG')]:
        path=OUT/directory/'resumen_oof.csv'
        if path.exists():
            table=pd.read_csv(path)
            table.insert(0,'iteration',title)
            later.append(table)
            report+=f'\n## {title}\n\n'+markdown(table,['scope','macro_score','balanced_accuracy','macro_f1'])+'\n\n'
            report+=f'[Protocolo, selecciones y limitaciones de esta iteración](../resultados/optimizacion_historial_08-09-2026/{directory}/Informe.md).\n'
    if len(later)==2:
        report+='''
## Cierre de la búsqueda

Se ejecutaron tres iteraciones: 105 configuraciones pupilares, cinco pesos de combinación
y 48 configuraciones con mirada/EEG. En total hubo 795 ajustes internos y 70 pipelines
externos ajustados; se guardan además 20 combinaciones con sus componentes, para 90 archivos
de modelos. Se verificaron 243.432 predicciones externas y 33 pruebas.

Los intervalos de la primera búsqueda muestran una ganancia pequeña e incierta frente a
logística. El hecho de probar más variantes y reportar su máximo no convierte ese máximo
en evidencia confirmatoria. Se conservan todos los intentos, con sus protocolos fechados,
selecciones internas y resultados. Esta búsqueda no autoriza a declarar un nuevo modelo
superior sin examinar sus comparaciones e incertidumbre. Mantener la logística como referencia
y confirmar cualquier candidato con participantes nuevos antes de sostener superioridad.
'''
    (ROOT/'documentacion/Optimizacion_Historial_08-09-2026.md').write_text(report,encoding='utf-8')
    write_json(OUT/'verificacion.json',dict(models=40,predictions=len(predictions),fold_metrics=40,participant_metrics=200,
        selection_records=20,inner_score_records=1575,validation_evaluated=False,test_evaluated=False,
        report_script_sha256=digest(__file__),previous_reference_sha256=digest(previous_path)))
    print(summary.to_string(index=False)); print(gains.to_string(index=False))


if __name__=='__main__':
    with threadpool_limits(limits=4): main()
