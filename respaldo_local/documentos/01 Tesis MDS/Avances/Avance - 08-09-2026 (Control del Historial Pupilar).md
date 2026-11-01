# Avance — 08-09-2026: Control del Historial Pupilar

Fuente: entrenamiento y auditoría local del 08-09-2026 en
`C:/Users/MarioRomero/desktop/mds/Tesis_MDS/`.
Complementa [[Avance - 07-09-2026 (TCN LSTM y BiLSTM)]] y pasa a ser la fuente vigente
del contraste entre historial pupilar y ventana actual con las mismas cinco variables.
La evaluación de test del 07-09-2026 se conserva como registro de esa ejecución.

## Trabajo completado

Se entrenaron TCN, LSTM y BiLSTM con historial real y controles de la misma arquitectura
entrenados con la ventana actual repetida. Se agregó el MLP de cinco variables que faltaba,
junto con Dummy, logística/Ridge y Random Forest comparables.

Entradas fijas: `pupil_mean_z`, `pupil_std_z`, `pupil_min_z`, `pupil_max_z` y
`pupil_slope_z_s`. Clasificación y regresión de activación con etiquetas GSR de 6 s.
GSR no se usa como entrada. Se conservan las etiquetas y la partición original 25/8/8.

Se usaron exclusivamente los 25 participantes originales de entrenamiento. Cinco folds
externos separan 20 para ajuste y cinco para evaluación. Dentro de los 20, una división
16/4 selecciona la época. Luego se reinicia la red y se reajusta sobre los 20 durante ese
número de épocas. Imputación y escalado se ajustan por separado en ambos niveles.
Los ocho participantes originales de validación y los ocho de test no se vuelven a evaluar.

Hay dos semillas neuronales. El control repetido conserva longitud, padding, arquitectura
e inicialización, pero sustituye cada vector pasado por el actual durante entrenamiento
y evaluación. Cada configuración selecciona su época con la misma regla interna.
El contraste mide el aporte de valores históricos bajo ese procedimiento; no aísla
únicamente el orden temporal ni constituye un efecto causal.

## Resultados de clasificación

Balanced accuracy calculada por participante y promediada entre 25 personas y dos semillas
para las redes. Los baselines estáticos tienen una semilla.

| Modelo | BA macro por participante |
|---|---:|
| Logística, ventana actual | 0,3536 |
| LSTM, historial real | 0,3534 |
| BiLSTM, historial real | 0,3526 |
| LSTM, ventana repetida | 0,3478 |
| Dummy | 0,3467 |
| TCN, historial real | 0,3455 |
| BiLSTM, ventana repetida | 0,3453 |
| MLP, ventana actual | 0,3451 |
| TCN, ventana repetida | 0,3443 |
| Random Forest, ventana actual | 0,3371 |

Dummy macro difiere de 1/3 porque dos personas solo tienen dos clases observadas;
la métrica conserva la convención previa de promediar recalls de clases presentes.
La BA global de Dummy sí es 1/3. El informe incluye ambas métricas sin mezclarlas.

Diferencia del historial real frente a la misma arquitectura con ventana actual repetida:

| Arquitectura | Diferencia, puntos porcentuales | Intervalo descriptivo 95% | Personas con mejora |
|---|---:|---:|---:|
| TCN | +0,12 | [-0,42; +0,70] | 14/25 |
| LSTM | +0,56 | [-0,08; +1,21] | 17/25 |
| BiLSTM | +0,74 | [-0,41; +1,88] | 16/25 |

Todos incluyen cero. Frente al MLP comparable, LSTM gana 0,84 puntos e intervalo
[-0,36; +2,23]; BiLSTM gana 0,76 e intervalo [-0,50; +2,24]. La señal favorable es pequeña
y variable entre participantes. Las recurrentes no superan a la logística en promedio.
LSTM mejora frente a RF, pero esa comparación por sí sola no prueba una ventaja temporal.

Los intervalos usan 2.000 remuestreos pareados de personas después de promediar semillas.
Son descriptivos: no corrigen múltiples comparaciones ni incorporan la dependencia entre
folds por compartir participantes de ajuste. La hipótesis surge de resultados previos ya
observados; este seguimiento no es una confirmación externa independiente.

## Score continuo y alcance

R² OOF medio: TCN -0,0034, LSTM -0,0039 y BiLSTM -0,0010. Las tres tienen mayor MSE
medio por persona que sus controles repetidos; no se obtiene mejora del score continuo.

Las 13.524 ventanas tienen historial medio de 4,89 ventanas; el 33,1% dispone de ocho
y el 16,9% solo de la actual. Se reinicia en cada cambio de persona, grabación, segmento,
estímulo o hueco temporal. El máximo soporte es 9 s. La BiLSTM no accede a ventanas futuras.
Las features y etiquetas heredan normalización offline por persona; no hay validación
de un sistema en tiempo real. Los indicadores de ausencias pueden conservar información
de calidad aun sin usar `pupil_both_valid_fraction`.

Para acotar la tesis, se conserva el panel pupilar de cinco variables como candidato,
logística como referencia compacta y MLP como control neuronal. No se demuestra que el
panel sea suficiente para una predicción útil. La importancia previa de `pupil_std_z`
no permite atribuirle una ganancia temporal reproducible. Atención y otras estrategias
de fusión quedan fuera de este contraste.

## Entrega y verificación

- 170 modelos externos guardados: 140 redes `.pt` y 30 pipelines estáticos `.joblib`.
- Diez preprocesadores y 140 historiales de selección interna/reajuste.
- 140 ajustes internos adicionales para seleccionar época; se guardan sus curvas.
- 459.816 predicciones OOF verificadas al recargar todos los modelos.
- 170 registros de métricas por fold y 850 por participante recalculados.
- Diez preprocesadores reconstruidos independientemente y 140 épocas seleccionadas auditadas.
- 29 pruebas aprobadas, incluidas aislamiento de participantes y borrado de información pasada.

Los modelos guardados corresponden a los folds: cada uno usa 20 participantes. No hay
un nuevo ajuste final con los 25 ni una nueva evaluación sobre test.

[Informe reproducible](../../Tesis_MDS/documentacion/Control_Historial_Pupilar_08-09-2026.md).
[Modelos, resultados, gráficos y guía de carga](../../Tesis_MDS/resultados/control_historial_08-09-2026/).

## Publicación en GitHub

Se completó `git push origin main` el 08-09-2026. GitHub confirmó el commit `e0e3730`
con 683 archivos de esta entrega: código, modelos, predicciones, resultados e informe.
Se verificaron 679 hashes de código y resultados contra los objetos preparados en Git.
La nueva regla de `.gitattributes` preserva los bytes de esta ejecución entre sistemas.

Esta nota, el índice y la sección de tesis se respaldan en
`documentacion/Tesis_Vault_08-09-2026.zip`, con inventario y hashes por archivo.
Se conservan los respaldos anteriores.

## Notas relacionadas

- [[Tesis_MDS]]
- [[Avance - 07-09-2026 (TCN LSTM y BiLSTM)]]
- [[Avance - 07-09-2026 (Estabilidad y Reduccion de Variables)]]
- [[Avance - 07-09-2026 (Importancia de Variables)]]
