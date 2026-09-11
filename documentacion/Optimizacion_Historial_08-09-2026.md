# Iteración de representación y modelos: 08-09-2026

La búsqueda mejora el promedio frente a logística fija: diferencia de **+0.11 puntos porcentuales** de BA macro
por participante, intervalo descriptivo del 95% [-1.03; +1.16].
Mejora en 16/25 participantes. El intervalo descriptivo incluye cero.

Complementa el [control del historial pupilar](Control_Historial_Pupilar_08-09-2026.md).
Esta iteración se concentra en clasificación de activación, manteniendo las cinco variables
pupilares y las etiquetas GSR de 6 s. No reentrena atención ni regresión.

## Resultados fuera del ajuste

`all`: selección entre 105 candidatos. `temporal`: selección entre 100 que usan pasado.
`current`: selección entre cinco modelos de ventana actual sin suavizado.
`fixed_logistic`: control anterior, logística balanceada C=1 con cinco entradas actuales.
Se evalúan las cuatro reglas completas de selección; no se elige una por su resultado OOF.

| scope | macro_score | balanced_accuracy | macro_f1 |
|---|---|---|---|
| all | 0.3546 | 0.3572 | 0.3560 |
| current | 0.3461 | 0.3475 | 0.3473 |
| fixed_logistic | 0.3536 | 0.3530 | 0.3456 |
| temporal | 0.3519 | 0.3542 | 0.3525 |

BA macro da igual peso a cada persona; BA global agrupa ventanas. Ambas promedian métricas
de dos semillas, no probabilidades. Las configuraciones deterministas pueden coincidir
entre semillas; las dos semillas no equivalen a dos muestras independientes.

| scope | reference | mean_delta | ci_low | ci_high | positive_participants |
|---|---|---|---|---|---|
| all | fixed_logistic | 0.0011 | -0.0103 | 0.0116 | 16 |
| all | current | 0.0085 | 0.0015 | 0.0163 | 13 |
| all | previous_MLP_current | 0.0096 | -0.0016 | 0.0215 | 15 |
| all | previous_LSTM | 0.0012 | -0.0145 | 0.0152 | 13 |
| all | previous_BiLSTM | 0.0020 | -0.0171 | 0.0182 | 16 |
| temporal | fixed_logistic | -0.0017 | -0.0138 | 0.0102 | 14 |
| temporal | current | 0.0058 | -0.0049 | 0.0159 | 14 |
| temporal | previous_MLP_current | 0.0068 | -0.0055 | 0.0196 | 13 |
| temporal | previous_LSTM | -0.0015 | -0.0166 | 0.0124 | 12 |
| temporal | previous_BiLSTM | -0.0007 | -0.0195 | 0.0157 | 15 |
| current | fixed_logistic | -0.0075 | -0.0173 | 0.0006 | 10 |
| current | previous_MLP_current | 0.0010 | -0.0074 | 0.0088 | 12 |
| current | previous_LSTM | -0.0073 | -0.0214 | 0.0041 | 11 |
| current | previous_BiLSTM | -0.0065 | -0.0226 | 0.0070 | 11 |

## Búsqueda y controles

Se congelaron 105 candidatos antes de evaluar: siete representaciones por cinco modelos y
tres tamaños de suavizado de probabilidades (1, 4 u 8). Representaciones: ventana actual
y resúmenes causales de 4, 8 o 16 ventanas, limitados al segmento o a la grabación.
Las cinco variables son `pupil_mean_z`, `pupil_std_z`, `pupil_min_z`, `pupil_max_z`, `pupil_slope_z_s`.
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

| fold | scope | representation | estimator | smoothing | inner_score |
|---|---|---|---|---|---|
| 1 | all | recording_4 | logistic_0.1 | 1 | 0.3564 |
| 1 | temporal | recording_4 | logistic_0.1 | 1 | 0.3564 |
| 1 | current | current | rbf | 1 | 0.3485 |
| 1 | fixed_logistic | current | logistic_1 | 1 | nan |
| 2 | all | current | logistic_0.1 | 4 | 0.3590 |
| 2 | temporal | current | logistic_0.1 | 4 | 0.3590 |
| 2 | current | current | logistic_1 | 1 | 0.3508 |
| 2 | fixed_logistic | current | logistic_1 | 1 | nan |
| 3 | all | current | logistic_0.01 | 8 | 0.3534 |
| 3 | temporal | current | logistic_0.01 | 8 | 0.3534 |
| 3 | current | current | logistic_0.01 | 1 | 0.3412 |
| 3 | fixed_logistic | current | logistic_1 | 1 | nan |
| 4 | all | current | hgb | 1 | 0.3459 |
| 4 | temporal | recording_4 | hgb | 1 | 0.3430 |
| 4 | current | current | hgb | 1 | 0.3459 |
| 4 | fixed_logistic | current | logistic_1 | 1 | nan |
| 5 | all | current | rbf | 4 | 0.3665 |
| 5 | temporal | current | rbf | 4 | 0.3665 |
| 5 | current | current | rbf | 1 | 0.3617 |
| 5 | fixed_logistic | current | logistic_1 | 1 | nan |

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

## Combinación de probabilidades

| scope | macro_score | balanced_accuracy | macro_f1 |
|---|---|---|---|
| fixed_half | 0.3534 | 0.3539 | 0.3510 |
| selected | 0.3525 | 0.3540 | 0.3521 |

[Protocolo, selecciones y limitaciones de esta iteración](../resultados/optimizacion_historial_08-09-2026/segunda_iteracion/Informe.md).

## Fusión de mirada y EEG

| scope | macro_score | balanced_accuracy | macro_f1 |
|---|---|---|---|
| all | 0.3527 | 0.3533 | 0.3524 |
| current | 0.3438 | 0.3419 | 0.3413 |
| temporal | 0.3527 | 0.3533 | 0.3524 |

[Protocolo, selecciones y limitaciones de esta iteración](../resultados/optimizacion_historial_08-09-2026/tercera_iteracion/Informe.md).

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
