"""Auditoria de modelos, seleccion y predicciones; informe de todas las fusiones."""
import argparse
import json
from datetime import datetime,timezone
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from threadpoolctl import threadpool_limits
from explorar_fusiones import OUT,TASKS,predict_bundle,select_candidates
from temporales_core import ROOT,CLASSES,digest,write_json,metric_record,individual_scores
from informe_control_historial import bootstrap,markdown


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',default=str(OUT.relative_to(ROOT)))
    args=parser.parse_args(); out=ROOT/args.output
    protocol=json.loads((out/'protocolo.json').read_text(encoding='utf-8'))
    complete=json.loads((out/'completo.json').read_text(encoding='utf-8'))
    catalog=json.loads((out/'catalogo_modelos.json').read_text(encoding='utf-8'))
    selections=json.loads((out/'selecciones.json').read_text(encoding='utf-8'))
    assert len(catalog)==120 and len(selections)==60
    for key,path in [('protocol_sha256','protocolo.json'),('selection_sha256','selecciones.json'),
                     ('catalog_sha256','catalogo_modelos.json'),('predictions_sha256','predicciones_oof.csv.gz')]:
        assert digest(out/path)==complete[key]
    for name,sha in protocol['sources'].items(): assert digest(ROOT/'scripts'/name)==sha
    if (out/'reanudacion.json').exists():
        resume=json.loads((out/'reanudacion.json').read_text(encoding='utf-8'))
        assert digest(out/'reanudacion.json')==complete['resumption_sha256']
        assert digest(ROOT/'scripts/completar_fusiones.py')==resume['source_sha256']
        assert resume['selection_sha256']==complete['selection_sha256']
    dataset=ROOT/'resultados/modelado/dataset_modelado.csv'
    assert digest(dataset)==protocol['dataset_sha256']
    assert digest(ROOT/'resultados/modelado/particion_participantes.csv')==protocol['partition_sha256']
    data=pd.read_csv(dataset); data['source_row']=np.arange(len(data)); data=data.loc[data.split.eq('train')].copy()
    search=pd.read_csv(out/'busqueda_interna.csv'); assert len(search)==1530
    for (task,fold),group in search.groupby(['task','fold']):
        outer=protocol['folds'][task][fold-1]
        for row in group.itertuples():
            fit=set(row.fit_participants.split('|')); val=set(row.evaluation_participants.split('|'))
            assert fit.isdisjoint(val) and fit|val==set(outer['fit'])
            assert (fit|val).isdisjoint(outer['evaluation'])
        avg=group.groupby('candidate_id',as_index=False).score.mean()
        reconstructed=select_candidates(avg,protocol['candidates'][task])
        for choice in reconstructed:
            saved=next(s for s in selections if s['task']==task and s['fold']==fold and s['scope']==choice['scope'])
            assert choice['candidate_id']==saved['candidate_id']
            np.testing.assert_allclose(choice['inner_score'],saved['inner_score'],rtol=1e-12,atol=1e-12)
    events=[json.loads(line) for line in (out/'bitacora.jsonl').read_text(encoding='utf-8').splitlines()]
    frozen=next(i for i,e in enumerate(events) if e['stage']=='selection_frozen')
    assert all(i>frozen for i,e in enumerate(events) if e['stage']=='outer_completed')
    assert sum(e['stage']=='fit_started' for e in events)==sum(e['stage']=='fit_completed' for e in events)==180
    predictions=pd.read_csv(out/'predicciones_oof.csv.gz'); people=[]; metrics=[]
    for meta in catalog:
        spec=TASKS[meta['task']]; fold=protocol['folds'][meta['task']][meta['fold']-1]
        assert meta['train_participants']==fold['fit'] and meta['evaluation_participants']==fold['evaluation']
        frame=data.loc[data.participant.isin(fold['evaluation'])&data[spec['target']].notna()].sort_values(
            ['participant','recording','window_start_utc']).reset_index(drop=True)
        assert digest(out/meta['path'])==meta['sha256']
        bundle=joblib.load(out/meta['path']); assert bundle['modalities']==spec['modalities']
        assert bundle['definition']==meta['definition']
        prob=predict_bundle(bundle,frame); pred=np.asarray(CLASSES)[prob.argmax(axis=1)]
        saved=predictions.loc[predictions.model_id.eq(meta['model_id'])].reset_index(drop=True)
        np.testing.assert_array_equal(saved.source_row,frame.source_row)
        np.testing.assert_array_equal(saved.true,frame[spec['target']])
        np.testing.assert_array_equal(saved.prediction,pred)
        np.testing.assert_allclose(saved[['prob_'+c for c in CLASSES]],prob,rtol=1e-12,atol=1e-12)
        ident={k:meta[k] for k in ['model_id','task','scope','fold','seed']}
        metrics.append(dict(**ident,**metric_record(frame,spec['target'],pred,'classification')))
        people.extend(dict(**ident,participant=p,score=s) for p,s in individual_scores(frame,spec['target'],pred,'classification').items())
    people=pd.DataFrame(people)
    stored=pd.read_csv(out/'metricas_participantes.csv').set_index(['model_id','participant'])
    checked=people.set_index(['model_id','participant']); np.testing.assert_allclose(stored.loc[checked.index,'score'],checked.score,rtol=1e-12,atol=1e-12)
    stored=pd.read_csv(out/'metricas_folds.csv').set_index('model_id'); checked=pd.DataFrame(metrics).set_index('model_id')
    for c in ['macro_score','balanced_accuracy','macro_f1']:
        np.testing.assert_allclose(stored.loc[checked.index,c],checked[c],rtol=1e-12,atol=1e-12)
    by_seed=[]
    for (task,scope,seed),g in predictions.groupby(['task','scope','seed']):
        expected=set(data.loc[data[TASKS[task]['target']].notna()].source_row)
        assert set(g.source_row)==expected and len(g)==len(expected)
        by_seed.append(dict(task=task,scope=scope,seed=seed,**metric_record(g.reset_index(drop=True),'true',g.prediction.to_numpy(),'classification')))
    by_seed=pd.DataFrame(by_seed); by_seed.to_csv(out/'resumen_por_semilla.csv',index=False)
    summary=by_seed.groupby(['task','scope'],as_index=False)[['macro_score','balanced_accuracy','macro_f1']].mean()
    summary.to_csv(out/'resumen_oof.csv',index=False)
    gains=[]; deltas=[]
    for task,g in people.groupby('task'):
        scores=g.groupby(['scope','participant']).score.mean().unstack('scope')
        references=['early','fixed_logistic']
        if task=='arousal':
            prior=pd.read_csv(ROOT/'resultados/control_historial_08-09-2026/metricas_participantes.csv')
            prior=prior.loc[prior.kind.eq('classification')&prior.architecture.eq('logistic')]
            ref=prior.groupby('participant').score.mean()
            assert set(ref.index)==set(scores.index)
            scores['previous_pupil_logistic']=ref.reindex(scores.index)
            references.append('previous_pupil_logistic')
        for scope in ['late_weighted','late_mean','late_geometric','unimodal','early']:
            for reference in references:
                if scope==reference: continue
                delta=scores[scope]-scores[reference]; low,high=bootstrap(delta)
                gains.append(dict(task=task,scope=scope,reference=reference,mean_delta=float(delta.mean()),ci_low=low,ci_high=high,
                                  positive_participants=int((delta>0).sum()),participants=len(delta)))
                deltas.extend(dict(task=task,scope=scope,reference=reference,participant=p,delta=float(d)) for p,d in delta.items())
    gains=pd.DataFrame(gains); gains.to_csv(out/'ganancias_pareadas.csv',index=False)
    pd.DataFrame(deltas).to_csv(out/'ganancias_participantes.csv',index=False)
    expanded=search.merge(pd.DataFrame([dict(task=t,**d) for t,defs in protocol['candidates'].items() for d in defs]),on=['task','candidate_id'])
    expanded.to_csv(out/'todos_los_intentos.csv',index=False)
    pd.DataFrame(selections).to_csv(out/'configuraciones_elegidas.csv',index=False)
    fig,axes=plt.subplots(1,2,figsize=(10,4))
    for ax,task in zip(axes,['attention','arousal']):
        rows=gains.loc[gains.task.eq(task)&gains.reference.eq('early')].set_index('scope').loc[['late_mean','late_geometric','late_weighted']]
        mean=rows.mean_delta.to_numpy()*100
        ax.errorbar(mean,np.arange(3),xerr=np.vstack([mean-100*rows.ci_low.to_numpy(),100*rows.ci_high.to_numpy()-mean]),fmt='o',capsize=4,color='#176b74')
        ax.axvline(0,color='grey',linestyle='--'); ax.set_yticks(np.arange(3),['Promedio','Geométrica','Pesos internos'])
        ax.set_title('Atención' if task=='attention' else 'Activación'); ax.set_xlabel('Diferencia frente a fusión temprana (pp BA)')
    fig.suptitle('Fusión tardía: diferencia de BA por participante e intervalo descriptivo 95%')
    fig.tight_layout()
    for ext in ['png','pdf']: fig.savefig(out/f'comparacion_fusiones.{ext}',dpi=180,bbox_inches='tight')
    plt.close(fig)
    primary=gains.loc[gains.scope.eq('late_weighted')&gains.reference.eq('early')]
    findings='\n'.join(f'- {r.task}: fusión ponderada {r.mean_delta*100:+.2f} pp frente a temprana, intervalo '
        f'[{r.ci_low*100:+.2f}; {r.ci_high*100:+.2f}], mejora en {r.positive_participants}/25 personas.' for r in primary.itertuples())
    report=f'''# Nuevos modelos y fusiones: 10-09-2026

Se probaron LDA regularizada y Extra Trees junto con logística, en clasificación de atención
y activación. Se registra cada ajuste, configuración y puntuación; los resultados desfavorables
se conservan. El contraste principal compara fusión tardía ponderada y temprana, con
selección interna de modelo/contexto en cada una.

{findings}

En activación, los mejores promedios observados corresponden a fusión geométrica (0,3651)
y media (0,3646). La geométrica gana 0,57 pp frente a temprana y 0,65 pp frente a logística
con las mismas 24 entradas; ambos intervalos incluyen cero. Frente a la logística pupilar
previa (0,3536), gana 1,15 pp, intervalo [-0,85; +3,31]. Es una señal favorable exploratoria,
sin superioridad estable confirmada. Elegir el máximo entre estrategias después de ver
estos resultados no equivale a una nueva validación independiente.

La selección interna diferencia las tareas: activación elige contexto de ocho ventanas
en todos los folds de fusión; en las fusiones tardías elige logística en tres folds y LDA
en dos. Atención elige Extra Trees con ventana actual en los cinco folds tardíos.
Su control unimodal (0,3450) queda prácticamente igual que la fusión ponderada (0,3444),
por lo que tampoco se demuestra una ventaja general de combinar modalidades para atención.

En activación, cuatro folds asignan peso 0,5 a pupila y 0,25 a mirada/EEG; uno asigna
0,5 a EEG. Estos son pesos seleccionados dentro de una grilla limitada, no contribuciones
causales ni porcentajes de varianza explicada. En atención, GSR recibe 0,75 en tres folds
y se usa reparto 0,5/0,5 en dos. Las selecciones sugieren qué contrastar después; no prueban
por sí mismas que un sensor o el historial sea necesario.

## Resultados OOF

{markdown(summary,['task','scope','macro_score','balanced_accuracy','macro_f1'])}

BA macro promedia por participante y luego por semilla. BA global agrupa ventanas por
semilla y luego promedia métricas. Los estimadores deterministas pueden coincidir entre
semillas. `fixed_logistic` usa todas las entradas actuales permitidas: 18 para atención,
24 para activación; esta última referencia difiere de la logística pupilar de cinco
variables del experimento anterior. No confundir esos baselines.
`previous_pupil_logistic` conserva esa referencia pupilar de cinco variables, evaluada
en las mismas 25 personas y cinco folds, como comparación secundaria para activación.

{markdown(gains,['task','scope','reference','mean_delta','ci_low','ci_high','positive_participants'])}

![Comparación](../{out.relative_to(ROOT).as_posix()}/comparacion_fusiones.png)

## Alternativas probadas

- Fusión temprana: concatenación de entradas antes de ajustar un modelo.
- Fusión tardía media: un modelo por modalidad y promedio de probabilidades.
- Fusión tardía geométrica: promedio de log-probabilidades, exponenciación y normalización.
  Se recortan probabilidades por debajo de 1e-12 para estabilidad numérica.
- Fusión tardía ponderada: pesos positivos en cuartos, suman uno y mantienen todas las
  modalidades. En atención: 0,25/0,75, 0,5/0,5, 0,75/0,25. En activación: permutaciones de
  0,5/0,25/0,25. Los pesos se eligen exclusivamente con datos internos.
- Control unimodal: modalidad, modelo y contexto elegidos internamente. Los bundles
  conservan todos los expertos, pero solo uno recibe peso uno; los demás pesan cero.
- Logística fija C=1, balanceada, con todas las entradas actuales, como referencia adicional.

Atención usa EEG (9) y GSR (9); eye tracking y pupila construyen la etiqueta y no entran.
Activación usa pupila (5, sin fracción de validez), mirada (10) y EEG (9); GSR construye
la etiqueta y no entra. Las features exactas y su orden se guardan en `protocolo.json`.

Tres familias: logística C=0,1 balanceada; LDA `lsqr`, shrinkage automático y priors uniformes;
Extra Trees con 100 árboles, profundidad máxima 8, mínimo 40 filas por hoja y clases
balanceadas. Imputación por mediana con indicadores de ausencia y escalado se ajustan
solo en personas de entrenamiento; cada experto tardío tiene su propio preprocesador.

Cada familia usa ventana actual o hasta ocho ventanas causales. Por modalidad se conservan
valores actuales, media, desviación estándar, diferencia con la ventana más antigua y
longitud disponible normalizada. El historial se reinicia ante huecos distintos de 1 s o
cambios de persona/grabación; puede atravesar estímulos. Soporte máximo de 9 s.
No se introducen etiquetas pasadas. La fusión temprana concatena una longitud por modalidad;
esas columnas coinciden y pueden influir en la regularización. No se afirma causalidad
fisiológica ni que una eventual ventaja de fusión demuestre una ventaja del historial.

## Selección y alcance

48 candidatos para atención y 54 para activación. Cinco folds externos dentro de train:
20 personas para ajustar y cinco para evaluar. Tres folds internos por cada conjunto de
20, promediando BA macro con igual peso por fold (seis o siete personas). Se selecciona
por separado cada estrategia, con desempate por identificador. Todas las selecciones de
ambas tareas se congelan antes de la primera evaluación externa. Reajuste con dos semillas,
20260910 y 20260911. No se elige entre estrategias usando su resultado externo.

Las búsquedas tienen distinto tamaño: temprana/media/geométrica evalúan seis candidatos
cada una; ponderada, 18; unimodal, 12 en atención y 18 en activación. Los intervalos no
corrigen ese conjunto de comparaciones. Se aplican 2.000 remuestreos pareados de personas,
después de promediar semillas; son descriptivos y no incorporan dependencia entre folds.
El train original ya se ha usado en iteraciones previas: esto es seguimiento exploratorio,
no confirmación con participantes nuevos. Validation y test originales no se vuelven a
evaluar. Se mantienen etiquetas y split; features y pseudoetiquetas son offline por persona.
No hay nueva regresión ni entrenamiento de TCN/LSTM en esta entrega.
Las probabilidades de los expertos no tienen una calibración externa adicional; su escala
y confianza pueden influir en las combinaciones aritméticas y geométricas.

## Registro y artefactos

La primera ejecución se interrumpió al exigir igualdad exacta de probabilidades tras
recargar Extra Trees con predicción paralela: diferencia máxima observada 2,22e-16.
Se conserva en `resultados/fusiones_10-09-2026/`, con `interrupcion.json`. La entrega
completa en `fusiones_10-09-2026_completa` reutiliza la búsqueda y las selecciones
congeladas; reajusta y evalúa los modelos externos con predicción en un solo hilo.
`reanudacion.json` registra la corrección y sus hashes. No se cambió una elección por
haber visto resultados externos. El wrapper reproducible fija un hilo desde el inicio.

- `bitacora.jsonl`: inicio/fin de cada grupo de ajustes, congelación y evaluación externa.
- `todos_los_intentos.csv`: 1.530 puntuaciones internas con modelo, contexto, estrategia,
  pesos y participantes. `busqueda_interna.csv` conserva el registro original.
- `selecciones.json`: 60 elecciones de estrategia/fold/tarea, incluida logística fija.
- `modelos/` y `catalogo_modelos.json`: 120 bundles con pipelines, modalidades, definición,
  participantes y hashes. Hubo {complete['inner_fits']} ajustes internos y
  {complete['outer_component_fits']} ajustes de componentes externos. Se conservan las puntuaciones
  internas y los pesos de fusión elegidos; los estimadores de folds internos se descartan
  de memoria sin guardarlos como artefactos.
- `predicciones_oof.csv.gz`: {len(predictions):,} predicciones externas con probabilidades.
- Métricas por fold, participante y semilla; diferencias pareadas; figuras PNG/PDF.
- `verificacion.json`: recarga de los 120 bundles, reproducción de predicciones, auditoría
  de selecciones y recálculo de 120 métricas de fold y 600 de participante.
- `pruebas.txt`: pruebas de causalidad, mezcla de probabilidades y separación de modalidades.

```powershell
python -m unittest discover -s tests
python scripts/ejecutar_fusiones_estables.py --output resultados/NUEVA_FUSION
python scripts/informe_fusiones.py --output resultados/NUEVA_FUSION
```

Para cargar desde Python, añadir `scripts` al path, cargar un bundle con `joblib.load`
y llamar `explorar_fusiones.predict_bundle(bundle, frame)`. El frame debe estar ordenado
por participante, grabación y timestamp, con las columnas originales. No requiere etiquetas
para predecir. Cada bundle corresponde a un fold entrenado con 20 personas; no hay un
ajuste final nuevo sobre las 25. Las ejecuciones exigen una carpeta nueva.
'''
    (ROOT/'documentacion/Fusiones_10-09-2026.md').write_text(report,encoding='utf-8')
    write_json(out/'verificacion.json',dict(models_reloaded=len(catalog),predictions_verified=len(predictions),
        fold_metrics=120,participant_metrics=600,internal_scores=len(search),selections=len(selections),
        all_selections_frozen_before_outer=True,validation_evaluated=False,test_evaluated=False,
        report_script_sha256=digest(__file__),completed_utc=datetime.now(timezone.utc).isoformat()))
    print(summary.to_string(index=False)); print(primary.to_string(index=False))


if __name__=='__main__':
    with threadpool_limits(limits=4): main()
