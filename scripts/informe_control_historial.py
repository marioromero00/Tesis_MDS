"""Reproduce todos los modelos OOF y documenta el contraste pupilar."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone

import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch

from control_historial import OUT, FEATURES, TARGETS, VARIANTS, current_control, nested_folds
from temporales_core import (ROOT, CLASSES, digest, write_json, seed_all, prepare_frame,
    history_indices, sequence_array, load_net, raw_predict, decode, metric_record, individual_scores, preprocessor)


def bootstrap(values, seed=20260908):
    values = np.asarray(values, dtype=float)
    means = np.random.default_rng(seed).choice(values, size=(2000, len(values)), replace=True).mean(axis=1)
    return np.quantile(means, [.025, .975]).tolist()


def markdown(frame, columns):
    lines = ['| ' + ' | '.join(columns) + ' |', '|' + '|'.join(['---']*len(columns)) + '|']
    for _, row in frame.iterrows():
        lines.append('| ' + ' | '.join(f'{row[c]:.4f}' if isinstance(row[c], (float, np.floating)) else str(row[c]) for c in columns) + ' |')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default=str(OUT.relative_to(ROOT)))
    args = parser.parse_args()
    output = ROOT/args.output
    protocol = json.loads((output/'protocolo.json').read_text(encoding='utf-8'))
    complete = json.loads((output/'entrenamiento_completo.json').read_text(encoding='utf-8'))
    catalog = json.loads((output/'catalogo_modelos.json').read_text(encoding='utf-8'))
    assert complete['protocol_sha256'] == digest(output/'protocolo.json')
    assert complete['catalog_sha256'] == digest(output/'catalogo_modelos.json')
    assert len(catalog) == 170
    for name, sha in protocol['source_hashes'].items():
        assert digest(ROOT/'scripts'/name) == sha
    dataset = ROOT/'resultados/modelado/dataset_modelado.csv'
    assert digest(dataset) == protocol['dataset_sha256']
    assert digest(ROOT/'resultados/modelado/particion_participantes.csv') == protocol['partition_sha256']
    data = pd.read_csv(dataset)
    data['source_row'] = np.arange(len(data))
    train = prepare_frame(data.loc[data.split.eq('train')].copy(), 'arousal_primary_6s', TARGETS, 'train')
    del data
    assert nested_folds(train) == protocol['folds']
    expected = set()
    for fold in protocol['folds']:
        for kind in ['classification', 'regression']:
            for architecture, mode in VARIANTS:
                for seed in protocol['seeds']:
                    expected.add(f'fold{fold["fold"]}__{kind}__{architecture}__{mode}__{seed}')
            for name in (['dummy_prior', 'logistic', 'random_forest'] if kind=='classification'
                         else ['dummy_mean', 'ridge', 'random_forest']):
                expected.add(f'fold{fold["fold"]}__{kind}__{name}__current__{protocol["seeds"][0]}')
    assert {m['model_id'] for m in catalog} == expected
    by_id = {m['model_id']:m for m in catalog}
    for meta in catalog:
        if meta['mode'] == 'history':
            paired_id = meta['model_id'].replace('__history__', '__repeat_current__')
            assert meta['parameters'] == by_id[paired_id]['parameters']
            assert meta['preprocessor_sha256'] == by_id[paired_id]['preprocessor_sha256']
    prep_catalog = json.loads((output/'preprocesadores.json').read_text(encoding='utf-8'))
    assert len(prep_catalog) == 10
    for meta in prep_catalog:
        fold = protocol['folds'][meta['fold']-1]
        assert meta['participants'] == fold[meta['stage']]
        assert digest(output/meta['path']) == meta['sha256']
        fit = train.loc[train.participant.isin(meta['participants']), FEATURES]
        independent = preprocessor().fit(fit)
        saved = joblib.load(output/meta['path'])
        np.testing.assert_array_equal(independent.get_feature_names_out(), saved.get_feature_names_out())
        np.testing.assert_array_equal(independent.transform(train[FEATURES]), saved.transform(train[FEATURES]))
    seed_all(protocol['seeds'][0])
    predicted_frames, recomputed, participant_rows = [], [], []
    for meta in catalog:
        fold = protocol['folds'][meta['fold']-1]
        assert meta['train_participants'] == fold['fit']
        assert meta['evaluation_participants'] == fold['evaluation']
        frame = train.loc[train.participant.isin(fold['evaluation'])].reset_index(drop=True)
        idx, lengths = history_indices(frame, protocol['context_windows'])
        path = output/meta['path']
        assert digest(path) == meta['sha256']
        assert digest(output/meta['predictions']) == meta['predictions_sha256']
        saved = pd.read_csv(output/meta['predictions'])
        assert set(saved.split) == {'train_oof'}
        np.testing.assert_array_equal(saved.source_row, frame.source_row)
        np.testing.assert_array_equal(saved.history_length, lengths)
        np.testing.assert_array_equal(saved.participant, frame.participant)
        kind, target = meta['kind'], meta['target']
        if kind == 'classification':
            np.testing.assert_array_equal(saved.true, frame[target])
        else:
            np.testing.assert_allclose(saved.true.to_numpy(float), frame[target], rtol=1e-12, atol=1e-12)
        if path.suffix == '.pt':
            assert digest(output/meta['preprocessor']) == meta['preprocessor_sha256']
            prep = joblib.load(output/meta['preprocessor'])
            x = current_control(sequence_array(prep.transform(frame[FEATURES]), idx), lengths, meta['mode'])
            raw = raw_predict(load_net(meta, output), x, lengths)
            prediction = decode(raw, kind)
            probabilities = torch.softmax(torch.from_numpy(raw), dim=1).numpy() if kind == 'classification' else None
            losses = pd.read_csv(output/'historiales'/f'{meta["model_id"]}.csv')
            assert len(losses.loc[losses.stage.eq('outer_refit')]) == meta['best_epoch']
            assert losses.loc[losses.stage.eq('outer_refit'), 'validation_macro_score'].isna().all()
            best, selected = -np.inf, 0
            for row in losses.loc[losses.stage.eq('inner')].itertuples():
                if row.validation_macro_score > best + protocol['min_delta']:
                    best, selected = row.validation_macro_score, row.epoch
            assert selected == meta['best_epoch']
        else:
            model = joblib.load(path)
            prediction = model.predict(frame[FEATURES])
            probabilities = (model.predict_proba(frame[FEATURES])[:, [list(model.classes_).index(c) for c in CLASSES]]
                             if kind == 'classification' else None)
        if kind == 'classification':
            np.testing.assert_array_equal(saved.prediction, prediction)
            np.testing.assert_allclose(saved[['prob_'+c for c in CLASSES]].to_numpy(), probabilities, rtol=1e-6, atol=1e-8)
        else:
            np.testing.assert_allclose(saved.prediction.to_numpy(float), prediction, rtol=1e-6, atol=1e-8)
        identity = {k:meta[k] for k in ['model_id', 'fold', 'kind', 'architecture', 'mode', 'seed']}
        recomputed.append(dict(**identity, **metric_record(frame, target, prediction, kind)))
        participant_rows.extend(dict(**identity, participant=p, score=s) for p, s in individual_scores(frame, target, prediction, kind).items())
        predicted_frames.append(saved)
    stored_metrics = pd.read_csv(output/'metricas_folds.csv').set_index('model_id')
    checked = pd.DataFrame(recomputed).set_index('model_id')
    for col in ['macro_score', 'balanced_accuracy', 'macro_f1', 'r2', 'mae', 'mse']:
        np.testing.assert_allclose(stored_metrics.loc[checked.index, col], checked[col], rtol=1e-6, atol=1e-8, equal_nan=True)
    people = pd.DataFrame(participant_rows)
    stored_people = pd.read_csv(output/'metricas_participantes.csv').set_index(['model_id', 'participant'])
    checked_people = people.set_index(['model_id', 'participant'])
    np.testing.assert_allclose(stored_people.loc[checked_people.index, 'score'], checked_people.score, rtol=1e-6, atol=1e-8)
    predictions = pd.concat(predicted_frames, ignore_index=True)
    assert len(predictions) == len(train)*34
    by_seed = []
    for (kind, architecture, mode, seed), group in predictions.groupby(['kind', 'architecture', 'mode', 'seed']):
        assert len(group) == len(train) and not group.source_row.duplicated().any()
        assert set(group.source_row) == set(train.source_row)
        frame = group.reset_index(drop=True)
        prediction = frame.prediction.to_numpy(str if kind=='classification' else float)
        if kind == 'regression':
            frame['true'] = frame.true.astype(float)
        by_seed.append(dict(kind=kind, architecture=architecture, mode=mode, seed=seed,
                            **metric_record(frame, 'true', prediction, kind)))
    pd.DataFrame(by_seed).to_csv(output/'metricas_oof_por_semilla.csv', index=False)
    summary = pd.DataFrame(by_seed).groupby(['kind', 'architecture', 'mode'], as_index=False).agg(
        macro_score=('macro_score', 'mean'), balanced_accuracy=('balanced_accuracy', 'mean'),
        r2=('r2', 'mean'), mse=('mse', 'mean'), mae=('mae', 'mean'), seeds=('seed', 'nunique'))
    summary.to_csv(output/'resumen_oof.csv', index=False)
    averaged = people.groupby(['kind', 'architecture', 'mode', 'participant'], as_index=False).score.mean()
    gains, deltas = [], []
    for kind in ['classification', 'regression']:
        scores = averaged.loc[averaged.kind.eq(kind)]
        linear, dummy = ('logistic', 'dummy_prior') if kind=='classification' else ('ridge', 'dummy_mean')
        for architecture in ['TCN', 'LSTM', 'BiLSTM']:
            temporal = scores.loc[scores.architecture.eq(architecture) & scores['mode'].eq('history')].set_index('participant').score
            for reference, mode in [(architecture, 'repeat_current'), ('MLP_current', 'current'),
                                    (linear, 'current'), ('random_forest', 'current'), (dummy, 'current')]:
                baseline = scores.loc[scores.architecture.eq(reference) & scores['mode'].eq(mode)].set_index('participant').score
                assert set(temporal.index) == set(baseline.index) == set(train.participant)
                delta = temporal.sort_index() - baseline.reindex(temporal.sort_index().index)
                low, high = bootstrap(delta)
                identity = dict(kind=kind, architecture=architecture, reference=reference, reference_mode=mode)
                gains.append(dict(**identity, mean_delta=float(delta.mean()), ci_low=low, ci_high=high,
                    participants=len(delta), positive_participants=int((delta>0).sum())))
                deltas.extend(dict(**identity, participant=p, delta=float(d)) for p, d in delta.items())
    gains = pd.DataFrame(gains)
    gains.to_csv(output/'ganancias_pareadas.csv', index=False)
    pd.DataFrame(deltas).to_csv(output/'ganancias_por_participante.csv', index=False)
    idx, lengths = history_indices(train, 8)
    sequences = train[['source_row', 'participant', 'recording', 'segment_id', 'stimulus', 'window_start_utc']].copy()
    sequences['history_length'] = lengths
    sequences['history_start_utc'] = train.iloc[idx[:, 0]].window_start_utc.to_numpy()
    sequences['fold'] = sequences.participant.map({p:f['fold'] for f in protocol['folds'] for p in f['evaluation']})
    sequences.to_csv(output/'secuencias_train_oof.csv.gz', index=False, compression='gzip')
    coverage = dict(rows=len(train), participants=train.participant.nunique(), mean_history=float(lengths.mean()),
                    singleton_fraction=float(np.mean(lengths==1)), full_history_fraction=float(np.mean(lengths==8)))
    write_json(output/'cobertura_historial.json', coverage)
    draw(output, gains)
    make_report(output, summary, gains, coverage)
    verification = dict(models_reloaded=len(catalog), predictions_verified=len(predictions),
        preprocessors_independently_refitted=len(prep_catalog), neural_epoch_selections_verified=140,
        fold_metrics_verified=len(checked), participant_metrics_verified=len(people),
        all_outer_participants_excluded_from_fit_and_epoch_selection=True,
        all_original_train_windows_predicted_once_per_configuration_and_seed=True,
        validation_evaluated=False, test_evaluated=False,
        protocol_sha256=digest(output/'protocolo.json'), catalog_sha256=digest(output/'catalogo_modelos.json'),
        report_script_sha256=digest(__file__), completed_utc=datetime.now(timezone.utc).isoformat())
    write_json(output/'verificacion_entrega.json', verification)
    print(summary.to_string(index=False))
    print(gains.loc[gains.reference_mode.eq('repeat_current')].to_string(index=False))
    print(json.dumps(verification, indent=2))


def draw(output, gains):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for ax, reference_mode, title in zip(axes, ['repeat_current', 'current'],
                                       ['Historial real frente a ventana repetida', 'Historial real frente a MLP actual']):
        rows = gains.loc[gains.kind.eq('classification') & gains.reference_mode.eq(reference_mode)]
        if reference_mode == 'current':
            rows = rows.loc[rows.reference.eq('MLP_current')]
        rows = rows.set_index('architecture').loc[['TCN', 'LSTM', 'BiLSTM']]
        values = rows.mean_delta.to_numpy()*100
        ax.errorbar(values, np.arange(3), xerr=np.vstack([values-rows.ci_low.to_numpy()*100,
                    rows.ci_high.to_numpy()*100-values]), fmt='o', color='#156b77', capsize=5)
        ax.axvline(0, color='#777', linestyle='--', linewidth=1)
        ax.set_yticks(np.arange(3), rows.index)
        ax.set_title(title, fontsize=11)
        ax.set_xlabel('Diferencia de BA macro (puntos porcentuales)')
        ax.grid(axis='x', alpha=.2)
    fig.suptitle('Activacion · cinco variables pupilares · OOF en 25 participantes')
    fig.text(.5, .02, 'Intervalos descriptivos del 95%; media de dos semillas; validacion/test originales sin nueva evaluacion.', ha='center', fontsize=8)
    fig.tight_layout(rect=[0, .05, 1, .94])
    for ext in ['png', 'pdf']:
        fig.savefig(output/f'contraste_historial.{ext}', dpi=180, bbox_inches='tight')
    plt.close(fig)


def make_report(output, summary, gains, coverage):
    cls = summary.loc[summary.kind.eq('classification')]
    reg = summary.loc[summary.kind.eq('regression')]
    paired = gains.loc[gains.kind.eq('classification') &
                       (gains.reference_mode.eq('repeat_current') | gains.reference.eq('MLP_current'))]
    history_gains = paired.loc[paired.reference_mode.eq('repeat_current')]
    gain_lines = '\n'.join(f'- {r.architecture}: {100*r.mean_delta:+.2f} puntos porcentuales; intervalo '
                           f'[{100*r.ci_low:+.2f}; {100*r.ci_high:+.2f}]; mejora en '
                           f'{r.positive_participants}/25 participantes.' for r in history_gains.itertuples())
    neural = cls.loc[cls['mode'].eq('history')].set_index('architecture')
    logistic = cls.loc[cls.architecture.eq('logistic')].iloc[0]
    mlp = cls.loc[cls.architecture.eq('MLP_current')].iloc[0]
    text = f'''# Control del historial pupilar: 08-09-2026

Este contraste complementa [los modelos temporales del 07-09-2026](Modelos_Temporales_07-09-2026.md).
Evalúa el aporte de hasta ocho ventanas de historia para predecir activación con las mismas
cinco variables. Los datos de validación y prueba originales no se vuelven a evaluar.
Es un seguimiento exploratorio motivado por resultados ya observados; la separación interna
evita que las etiquetas de cada participante evaluado seleccionen la época de su modelo,
pero no convierte la hipótesis elegida previamente en una confirmación independiente.

## Lectura de los resultados

La logística con cinco variables obtiene BA macro {logistic.macro_score:.4f}, frente a
{neural.loc['LSTM', 'macro_score']:.4f} de LSTM y {neural.loc['BiLSTM', 'macro_score']:.4f}
de BiLSTM con historial. El MLP comparable obtiene {mlp.macro_score:.4f}.
Las recurrentes mejoran puntualmente frente al MLP, pero sus intervalos pareados incluyen
cero y no superan a logística en promedio. La referencia estática elegida cambia la lectura:
LSTM sí supera a Random Forest en este contraste descriptivo, aunque eso no demuestra
superioridad frente a los controles de ventana actual en general.

Frente a la misma arquitectura entrenada con ventana actual repetida:

{gain_lines}

Los tres intervalos incluyen cero. Hay una señal pequeña favorable al historial en
clasificación, con variación entre personas; este resultado no establece una mejora estable.
En regresión, todas las redes con historial tienen R² negativo cercano a cero y mayor MSE
medio por participante que sus controles repetidos. La clasificación ordinal es por ahora
el contraste más informativo, sin descartar futuras formulaciones del score continuo.

Para acotar el trabajo, estos resultados sostienen conservar el panel pupilar de cinco
variables, logística como referencia compacta y MLP como control neuronal. El panel es
experimental: no se ha demostrado que sea suficiente para predecir activación con utilidad
práctica. La importancia previa de `pupil_std_z` sigue siendo dependencia del modelo;
este control no demuestra que su variación histórica explique una ganancia reproducible.
Mantener etiquetas y registrar el siguiente protocolo de contexto/fusión antes de evaluarlo.

## Diseño ejecutado

- Entradas fijas: {', '.join('`'+f+'`' for f in FEATURES)}.
- Etiquetas originales: `arousal_label_6s` y `arousal_score_6s`, construidas desde GSR.
  GSR no entra al estudiante. No se modifican etiquetas, exclusiones ni split 25/8/8.
- Cinco folds externos por participante dentro de train: 20 para ajustar, cinco para evaluar.
  De los 20, una partición interna 16/4 elige época; luego se reinicia la red y se ajusta
  con los 20 durante ese número de épocas. Cada participante tiene predicciones OOF una vez
  por configuración y semilla. Se conservan los folds del protocolo de estabilidad.
- Imputación por mediana con indicadores de ausencias y escalado ajustados separadamente
  en inner16 y outer20. Las columnas originales heredan normalización offline por participante.
- TCN, LSTM y BiLSTM con historial real frente a la misma arquitectura entrenada con
  cada vector pasado reemplazado por la ventana actual. Ambas conservan longitud, padding,
  parámetros e inicialización por semilla. Las épocas pueden diferir porque cada configuración
  sigue la misma regla de selección interna. Se estima el aporte de la información histórica
  bajo este procedimiento, no un efecto causal ni únicamente el efecto del orden temporal.
- MLP con las mismas cinco variables y acceso solo al endpoint; Dummy, logística/Ridge
  y Random Forest estáticos con esas mismas entradas y los mismos participantes externos.
- Dos semillas neuronales, 20260907 y 20260908. Baselines con semilla 20260907, RF de 200 árboles.
  Hiperparámetros neuronales del protocolo anterior: 24 unidades, dropout 0,2, AdamW 0,001,
  máximo 30 épocas, paciencia 6, mínimo 8 antes de detener, batches de 256 y clipping 1.
  La mejor época puede ser anterior a ocho; ocho limita cuándo detener la búsqueda.
  La pérdida se promedia por ventana; clasificación usa pesos de clase calculados en ajuste.
  La métrica de selección da igual peso a cada participante de validación interna.

La separación entre selección interna y evaluación externa sigue el principio descrito
en la [documentación de validación anidada de scikit-learn](https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html).
Los grupos de evaluación son disjuntos de los de ajuste mediante
[GroupKFold](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html).
Se usa un holdout interno por fold, no una búsqueda exhaustiva de hiperparámetros.

## Clasificación

Métrica principal: balanced accuracy calculada por participante y luego promediada entre
participantes y semillas. BA global agrupa todas las ventanas OOF por semilla y después
promedia semillas. No es un ensemble de probabilidades.

{markdown(cls, ['architecture', 'mode', 'macro_score', 'balanced_accuracy', 'seeds'])}

Dummy puede diferir de 1/3 en la métrica macro: se promedian recalls de las clases observadas
en cada persona, como en el protocolo previo; dos participantes de train tienen dos clases.
La BA global mantiene la referencia de tres clases. Usar el Dummy observado al comparar.

## Aporte del historial

Diferencia positiva favorece el historial real. Intervalos descriptivos de percentiles:
2.000 remuestreos pareados de los 25 participantes, después de promediar semillas.
No corrigen múltiples contrastes ni incorporan la dependencia por solapamiento de los
conjuntos de ajuste entre folds; no son pruebas confirmatorias de significación.
La selección de época con cuatro personas y solo dos semillas deja variación de ajuste
que estos intervalos no resumen por completo.

{markdown(paired, ['architecture', 'reference', 'reference_mode', 'mean_delta', 'ci_low', 'ci_high', 'positive_participants'])}

![Diferencias e intervalos](../{output.relative_to(ROOT).as_posix()}/contraste_historial.png)

## Score continuo

`macro_score` es MSE negativo promediado por participante; una diferencia positiva indica
menor error. R², MSE y MAE agrupan las predicciones OOF por semilla y luego se promedian.

{markdown(reg, ['architecture', 'mode', 'macro_score', 'r2', 'mse', 'mae'])}

## Cobertura y alcance

Se evalúan {coverage['rows']:,} ventanas de {coverage['participants']} participantes.
Historial medio: {coverage['mean_history']:.2f} ventanas; solo {coverage['full_history_fraction']:.1%}
dispone de ocho ventanas y {coverage['singleton_fraction']:.1%} tiene únicamente la actual.
Cada secuencia reinicia ante cambio de participante, grabación, segmento, estímulo o hueco.
Máximo soporte de 9 s, con ventanas de 2 s y stride de 1 s. BiLSTM recorre solamente
el pasado y la ventana actual. Los controles repetidos retienen la longitud como información
potencial; la comparación con MLP puede incluir su efecto. No se aísla orden frente a
promediado/suavizado del pasado. No se reestima aquí la importancia individual de variables.
La ausencia de `pupil_both_valid_fraction` no elimina toda posible información de calidad:
los indicadores de valores ausentes permanecen en el preprocesador.

Las pseudoetiquetas y la normalización por sesión son offline. No se afirma validación en
tiempo real, desempeño sobre etiquetas humanas ni confirmación de toda la hipótesis multimodal.
Este experimento se limita a activación y pupila; no incluye atención ni nuevas fusiones.

## Artefactos y reproducción

Se guardan **170 modelos externos evaluados: 140 redes y 30 pipelines estáticos**, diez
preprocesadores, 140 historiales de búsqueda interna/reajuste, metadatos con hashes y
459.816 predicciones OOF con probabilidades de clasificación. Hubo 140 ajustes neuronales
internos adicionales para seleccionar época; sus curvas están guardadas, no sus pesos.
Cada modelo externo usa 20 participantes. No hay un nuevo modelo final ajustado con los 25.

En [resultados](../{output.relative_to(ROOT).as_posix()}/): `protocolo.json`,
`catalogo_modelos.json`, `modelos/`, `predicciones/`, `historiales/`, `resumen_oof.csv`,
`metricas_oof_por_semilla.csv`, `metricas_folds.csv`, `metricas_participantes.csv`,
`ganancias_pareadas.csv`, `ganancias_por_participante.csv`, `secuencias_train_oof.csv.gz`,
`verificacion_entrega.json` y figuras PNG/PDF. La auditoría recarga todos los modelos,
reproduce predicciones, verifica cobertura y recalcula métricas de folds y participantes.

```powershell
python -m pip install -r requirements_temporales.txt
python -m unittest discover -s tests
python scripts/control_historial.py --output resultados/NUEVA_EJECUCION
python scripts/informe_control_historial.py --output resultados/NUEVA_EJECUCION
```

El directorio de entrenamiento debe ser nuevo. El informe se regenera sin entrenar y
exige los hashes originales. Consultar `COMO_CARGAR.md` en resultados para recuperar un modelo.
'''
    (ROOT/'documentacion/Control_Historial_Pupilar_08-09-2026.md').write_text(text, encoding='utf-8')
    (output/'COMO_CARGAR.md').write_text('''# Cargar un modelo del contraste

Desde la raíz del repositorio, con `requirements_temporales.txt` instalado:

```python
import sys, json, joblib, pandas as pd, numpy as np
sys.path.insert(0, 'scripts')
from control_historial import OUT, FEATURES, TARGETS, current_control
from temporales_core import prepare_frame, history_indices, sequence_array, load_net, raw_predict, decode
catalog = json.loads((OUT/'catalogo_modelos.json').read_text(encoding='utf-8'))
meta = next(m for m in catalog if m['fold']==1 and m['kind']=='classification'
            and m['architecture']=='BiLSTM' and m['mode']=='history' and m['seed']==20260907)
data = pd.read_csv('resultados/modelado/dataset_modelado.csv')
frame = prepare_frame(data.loc[data.participant.isin(meta['evaluation_participants'])],
                      'arousal_primary_6s', TARGETS, 'train')
indices, lengths = history_indices(frame, 8)
prep = joblib.load(OUT/meta['preprocessor'])
x = current_control(sequence_array(prep.transform(frame[FEATURES]), indices), lengths, meta['mode'])
prediction = decode(raw_predict(load_net(meta, OUT), x, lengths), meta['kind'])
```

`mode` debe aplicarse también a los controles repetidos. El MLP lee solo la ventana actual.
Los `.joblib` estáticos ya incluyen su preprocesador y aceptan las cinco columnas en orden.
Los modelos corresponden a folds de evaluación, no a un ajuste final sobre los 25 participantes.
''', encoding='utf-8')


if __name__ == '__main__':
    main()
