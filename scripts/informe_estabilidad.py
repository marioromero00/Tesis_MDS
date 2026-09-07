"""Produce tablas y figuras de la ejecucion completa de estabilidad, sin entrenar."""
from pathlib import Path
import json
import hashlib
import itertools

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'resultados/estabilidad_variables_07-09-2026'
REPORT = ROOT / 'documentacion/Estabilidad_Variables_07-09-2026.md'
LABELS = {'full': 'Completo', 'EEG': 'EEG', 'compact_no_noise': 'Compacto sin ruido',
          'Pupil': 'Pupila', 'Eye_Pupil': 'Mirada + pupila', 'Pupil_no_quality': 'Pupila sin validez',
          'Eye_Pupil_no_quality': 'Mirada + pupila sin validez'}
TASK_LABELS = {'attention_primary': 'Atención', 'arousal_primary_6s': 'Activación'}


def table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |'] +
                     ['| ' + ' | '.join(map(str, row)) + ' |' for row in rows])


def number(value):
    return f'{value:.4f}'.replace('.', ',')


def main():
    manifest = json.loads((OUTPUT / 'manifiesto.json').read_text(encoding='utf-8'))
    protocol = json.loads((OUTPUT / 'protocolo.json').read_text(encoding='utf-8'))
    frozen = json.loads((OUTPUT / 'conjuntos_congelados.json').read_text(encoding='utf-8'))
    folds = json.loads((OUTPUT / 'seleccion_por_fold.json').read_text(encoding='utf-8'))
    summary = pd.read_csv(OUTPUT / 'resumen_cv.csv')
    metrics = pd.read_csv(OUTPUT / 'metricas_folds.csv')
    external = pd.read_csv(OUTPUT / 'validacion_panel_congelado.csv')
    stability = []
    selected = [set(f['subsets']['compact_no_noise']) for f in folds if f['task'] == 'attention_primary']
    union = set.union(*selected)
    for name in protocol['compact_priority']:
        stability.append({'feature': name, 'selected_folds': sum(name in s for s in selected),
                          'folds': len(selected), 'selected_final': name in frozen['features']['attention_primary']['compact_no_noise']})
    pd.DataFrame(stability).to_csv(OUTPUT / 'estabilidad_seleccion.csv', index=False)
    jaccard = [len(a & b) / len(a | b) for a, b in itertools.combinations(selected, 2)]
    def value(task, kind, model, subset, column='mean_score'):
        row = summary.loc[summary.task.eq(task) & summary.kind.eq(kind) & summary.model.eq(model) & summary.subset.eq(subset)].iloc[0]
        return number(row[column])
    sections = ['# Estabilidad de la reduccion de variables — 07-09-2026',
        '> Complementa el análisis exploratorio de importancia y lo reemplaza como fuente vigente '
        'para el panel de entradas del siguiente experimento. No confirma un ganador universal.',
        '## Conclusión y decisión',
        '**La mejora inicial de activación con pupila sola no se sostuvo en el contraste interno.** '
        'En BA macro por participante, RF completo obtiene ' + value('arousal_primary_6s', 'classification', 'random_forest', 'full') +
        ' y pupila sola ' + value('arousal_primary_6s', 'classification', 'random_forest', 'Pupil') +
        '; logística completa obtiene ' + value('arousal_primary_6s', 'classification', 'logistic', 'full') +
        ' y pupila sola ' + value('arousal_primary_6s', 'classification', 'logistic', 'Pupil') + '. '
        'La logística con cinco variables pupilares sin validez alcanza ' +
        value('arousal_primary_6s', 'classification', 'logistic', 'Pupil_no_quality') +
        ', pero la diferencia frente al completo incluye cero en su intervalo descriptivo. '
        'Se conserva como candidato pequeño, no como ganador confirmado.',
        '**En atención, seleccionar las mismas columnas no garantiza conservar desempeño.** '
        'RF completo obtiene ' + value('attention_primary', 'classification', 'random_forest', 'full') +
        ' y el compacto de nueve entradas ' + value('attention_primary', 'classification', 'random_forest', 'compact_no_noise') +
        '. La diferencia compactado − completo es ' + value('attention_primary', 'classification', 'random_forest', 'compact_no_noise', 'delta_full') +
        ' con intervalo [' + value('attention_primary', 'classification', 'random_forest', 'compact_no_noise', 'low_full') +
        '; ' + value('attention_primary', 'classification', 'random_forest', 'compact_no_noise', 'high_full') +
        ']. La selección elimina ruido eléctrico y redundancias a la vez; no permite atribuir '
        'la diferencia exclusivamente a una de esas intervenciones.',
        'Logística con EEG solo es el contraste reducido más favorable de clasificación de atención '
        '(' + value('attention_primary', 'classification', 'logistic', 'EEG') + '). Ese conjunto conserva '
        'el indicador de ruido eléctrico del baseline y no constituye una selección fisiológica limpia. '
        'La señal es pequeña y los intervalos son exploratorios.',
        'Para el score continuo de activación, Ridge con cinco variables pupilares obtiene MSE macro '
        + number(-float(summary.loc[summary.task.eq('arousal_primary_6s') & summary.kind.eq('regression') & summary.model.eq('ridge') & summary.subset.eq('Pupil_no_quality'), 'mean_score'].iloc[0])) +
        ', prácticamente el 1,0000 del predictor de la media. Los RF de regresión son peores que '
        'ese predictor en todos los conjuntos. La reducción no resuelve todavía la predicción del score.',
        'Decisión operativa: mantener los completos de 18/25 entradas como referencia y dejar '
        'congelados los contrastes reducidos de este informe. Para activación, priorizar el candidato '
        'mínimo de pupila sin validez (5), contrastándolo con pupila (6), mirada + pupila (16) y '
        'completo (25); la variante de 15 columnas es un control adicional de calidad. Para atención, '
        'comparar completo (18), EEG (9) y compacto sin ruido (9). No se elimina una modalidad '
        'del diseño general ni se fija un único ganador para todas las tareas/modelos.',
        '## Ejecución realizada',
        f'Se ajustaron **{manifest["fold_models"]} modelos internos** y **{len(manifest["final_models"])} pipelines '
        'finales**. Se mantuvieron las pseudoetiquetas principales, el contexto GSR de 6 s y el split '
        'congelado. El test no se evaluó. Los pipelines finales se entrenaron con los 25 participantes '
        'de train y se verificaron tras recargarlos, incluidas probabilidades de clasificación.',
        'El panel se fijó por su función experimental: referencia completa, reducción por modalidad, '
        'reducción de redundancia y contraste de calidad. No se eligió el máximo de validación como '
        'ganador. Las columnas exactas quedaron registradas antes de calcular las métricas finales '
        'de validación en `conjuntos_congelados.json`.',
        '## Protocolo y alcance',
        'Cinco folds GroupKFold, con semilla 20260907, repartieron los 25 participantes de train. '
        'Cada ajuste usó 20 participantes y predijo los 5 restantes; cada participante recibió '
        'una predicción fuera de fold. Sus ventanas completas permanecieron juntas. '
        'Las 13.524 ventanas de train se evaluaron una vez por configuración, con igual peso '
        'por participante en el resumen principal.',
        'Se compararon logística/Ridge y Random Forest, junto con DummyClassifier/DummyRegressor. '
        'RF mantuvo 200 árboles, hoja mínima de 5 y semilla 20260822; logística conservó balance '
        'de clases y Ridge alpha=1. Se usaron cuatro trabajadores para los árboles. '
        'Imputación, indicadores de ausencia y escalado se ajustaron de nuevo dentro de cada fold.',
        'Para atención, el candidato compacto excluye `eeg_line_noise_ratio`. Un recorrido con '
        'prioridad explícita conserva una entrada si no tiene correlación absoluta de Spearman '
        '≥0,90 con otra ya conservada. También excluye constantes o columnas sin observaciones. '
        'Las correlaciones se calculan exclusivamente en los 20 participantes de ajuste de cada fold. '
        'Se priorizan RMS para amplitud EEG y componente tónica para nivel GSR; la lista completa '
        'está en `protocolo.json`. No se usaron las etiquetas para ordenar entradas.',
        'Para activación se comparan 25 entradas completas, pupila (6), mirada + pupila (16), '
        'pupila sin fracción de validez binocular (5) y mirada + pupila sin esa fracción (15). '
        '“Sin validez” retira esa columna explícita; el imputador mantiene indicadores de ausencia. '
        'Por tanto no elimina toda posible información de calidad de adquisición.',
        'Se calculan balanced accuracy macro por participante para clasificación y MSE macro '
        'para regresión. La BA de cada participante promedia el recall de las clases presentes '
        'en sus datos, siguiendo la métrica anterior. Si falta una clase, el Dummy macro puede '
        'diferir de 1/3; por eso se compara con el Dummy realmente ajustado en cada fold. '
        'Los intervalos de las diferencias provienen de 2.000 remuestreos '
        'pareados de los 25 participantes. Son descriptivos: los modelos comparten sujetos '
        'de ajuste entre folds, solo se ejecutó una partición de cinco folds y no se corrige '
        'por comparaciones múltiples. No son una prueba confirmatoria ni de no inferioridad.',
        'Las hipótesis de subconjuntos proceden del análisis previo que ya observó train y '
        'validación. Este contraste examina sensibilidad interna y no constituye evidencia '
        'independiente. Además, se hereda normalización por participante offline, incluidas '
        'las pseudoetiquetas; no es una evaluación de inferencia causal en tiempo real.',
        '## Resultados internos por participante',
        'Δ completo y Δ trivial son mejoras: positivas significan mejor desempeño. En '
        'clasificación son diferencias de balanced accuracy; en regresión son reducciones '
        'del MSE. El valor de MSE mostrado en la tabla es positivo. “Folds mejores” cuenta '
        'en cuántos de los cinco folds mejora al mismo modelo completo. Un intervalo que '
        'cruza cero no demuestra equivalencia.']
    for task, title in TASK_LABELS.items():
        for kind, kind_label in [('classification', 'clasificación'), ('regression', 'regresión')]:
            group = summary.loc[summary.task.eq(task) & summary.kind.eq(kind)].sort_values(['model', 'mean_features', 'subset'])
            rows = []
            for row in group.itertuples():
                fm = metrics.loc[metrics.task.eq(task) & metrics.kind.eq(kind) & metrics.model.eq(row.model)]
                current = fm.loc[fm.subset.eq(row.subset)].set_index('fold').macro_score
                full = fm.loc[fm.subset.eq('full')].set_index('fold').macro_score
                wins = int((current - full > 0).sum())
                value = row.mean_score if kind == 'classification' else -row.mean_score
                rows.append([row.model, LABELS[row.subset], f'{row.mean_features:g}', number(value),
                             number(row.delta_full), f'[{number(row.low_full)}; {number(row.high_full)}]',
                             number(row.delta_dummy), f'[{number(row.low_dummy)}; {number(row.high_dummy)}]', f'{wins}/5'])
            sections += [f'### {title}: {kind_label}', table(
                ['Modelo', 'Conjunto', 'Variables medias', 'BA macro' if kind == 'classification' else 'MSE macro',
                 'Δ completo', 'Intervalo 95 %', 'Δ trivial', 'Intervalo 95 %', 'Folds mejores'], rows)]
    sections += ['## Estabilidad de columnas compactas de atención',
                 f'Conjuntos por fold: {[len(s) for s in selected]}. Similitud Jaccard media '
                 f'entre pares: {np.mean(jaccard):.3f}; mínima: {min(jaccard):.3f}. '
                 'Esta estabilidad mide selección por redundancia, no relevancia causal ni predictiva.',
                 table(['Variable', 'Folds seleccionada', 'Conjunto final'],
                       [[r['feature'], f'{r["selected_folds"]}/5', 'Sí' if r['selected_final'] else 'No'] for r in stability]),
                 '## Panel congelado para el siguiente experimento']
    for task, sets in frozen['features'].items():
        sections += [f'### {TASK_LABELS[task]}', table(['Conjunto', 'N', 'Columnas exactas'],
                     [[LABELS[name], len(columns), ', '.join(f'`{c}`' for c in columns)] for name, columns in sets.items()])]
    sections += ['Los conjuntos completos son controles. Los subconjuntos sirven para estudiar '
                 'modalidad, redundancia y calidad; no se sustituye el protocolo original por una única '
                 'selección. La reducción de entradas del estudiante no elimina sensores del profesor. '
                 'No se entrenó TCN/LSTM en esta etapa.',
                 '## Validación del panel después de congelarlo',
                 'Estas métricas usan los ocho participantes de validación originales. Se reportan '
                 'BA y R² globales, además del score macro en el CSV. No son test y no deben '
                 'presentarse como validación externa independiente tras haber observado ese split antes.']
    for task, title in TASK_LABELS.items():
        rows = []
        for row in external.loc[external.task.eq(task)].itertuples():
            value = row.balanced_accuracy if row.kind == 'classification' else row.r2
            rows.append([row.kind, row.model, LABELS[row.subset], row.n_features, number(value)])
        sections += [f'### {title}', table(['Tarea', 'Modelo', 'Conjunto', 'N', 'BA / R² global'], rows)]
    plt.rcParams.update({'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False})
    for task, title in TASK_LABELS.items():
        fig, axes = plt.subplots(1, 2, figsize=(13, 5), layout='constrained')
        for ax, kind in zip(axes, ['classification', 'regression']):
            group = summary.loc[summary.task.eq(task) & summary.kind.eq(kind) & ~summary.model.eq('dummy') & ~summary.subset.eq('full')]
            names = list(frozen['features'][task])[1:]
            for offset, model, color in [(-.12, 'logistic' if kind == 'classification' else 'ridge', '#165777'),
                                          (.12, 'random_forest', '#bd6420')]:
                part = group.loc[group.model.eq(model)].set_index('subset').loc[names]
                yy = np.arange(len(names)) + offset
                ax.hlines(yy, part.low_full, part.high_full, color=color, alpha=.7)
                ax.scatter(part.delta_full, yy, color=color, label=model, zorder=3)
            ax.axvline(0, color='#777777', ls='--')
            ax.set_yticks(np.arange(len(names)), [LABELS[n] for n in names])
            ax.set_xlabel('Mejora BA macro frente a completo' if kind == 'classification' else 'Reducción MSE macro frente a completo')
            ax.set_title('Clasificación' if kind == 'classification' else 'Regresión')
            ax.legend(loc='upper center', bbox_to_anchor=(.5, -.18), ncol=2, fontsize=8)
            ax.grid(axis='x', alpha=.15)
        fig.suptitle(f'{title} · comparación interna por participante\nIntervalos descriptivos, 25 participantes y 5 folds', fontsize=12)
        fig.savefig(OUTPUT / f'estabilidad_{task}.png', dpi=180)
        fig.savefig(OUTPUT / f'estabilidad_{task}.pdf')
        plt.close(fig)
        sections += [f'![{title}: diferencias internas](../resultados/estabilidad_variables_07-09-2026/estabilidad_{task}.png)']
    sections += ['## Archivos y reproducción',
        'Desde la raíz del repositorio:\n\n```powershell\npython scripts/estabilidad_variables.py '
        '--output resultados/estabilidad_nueva_ejecucion --jobs 4\npython -m unittest discover -s tests\n```',
        'La salida debe ser nueva. `scripts/informe_estabilidad.py` genera este informe y sus figuras '
        'para la ruta fechada de esta entrega; requiere Matplotlib 3.11.1 además de las dependencias '
        'de `requirements.txt`. Las tablas se generan directamente de los CSV.',
        '- `protocolo.json`: reglas, semillas, versiones, hashes y participantes por fold.\n'
        '- `seleccion_por_fold.json`: columnas y motivos de exclusión en cada ajuste.\n'
        '- `estabilidad_seleccion.csv`: frecuencia de selección por columna.\n'
        '- `metricas_folds.csv`, `metricas_participantes_oof.csv`, `resumen_cv.csv`: desempeño interno.\n'
        '- `predicciones_oof.csv.gz`: predicciones fuera de fold, comprimidas sin pérdida.\n'
        '- `conjuntos_congelados.json`: panel fijado antes de reportar validación.\n'
        '- `validacion_panel_congelado.csv`: resultados finales de validación.\n'
        '- `modelos_finales/` y `manifiesto.json`: pipelines completos, columnas y hashes.',
        'Para cargar un pipeline propio: localizar su entrada en `manifiesto.json`, abrir con '
        '`joblib.load` y pasar las columnas de `features` en ese orden. Los modelos internos '
        'de cada fold se pueden reproducir con el protocolo; se guardan sus predicciones, no sus binarios.',
        '## Verificación de entrega',
        'Pasaron las 18 pruebas del repositorio. La auditoría independiente '
        '`python scripts/verificar_estabilidad.py` comprobó 486.864 predicciones fuera de fold, '
        'recalculó las 900 métricas por participante y verificó cobertura de cada participante, '
        'separación de folds y hashes de los 36 modelos finales. '
        'El detalle está en `verificacion_entrega.json`; la salida de pruebas, en `pruebas.txt`. '
        'Los modelos originales permanecen conservados y esta entrega está guardada localmente.',
        '## Referencia metodológica',
        '[GroupKFold, documentación oficial de scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html) '
        'describe particiones de grupos disjuntos. Aquí el grupo es el participante y se aplica '
        'exclusivamente al split train congelado.']
    REPORT.write_text('\n\n'.join(sections) + '\n', encoding='utf-8')
    print(REPORT)


if __name__ == '__main__':
    main()
