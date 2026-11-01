# Avance: 13-09-2026, Grid Search Transformer

Continúa [[Avance - 13-09-2026 (Transformer y TCN)]]. Fuente:
`documentacion/Grid_Transformer_13-09-2026.md` y
`resultados/transformer_grid_13-09-2026/`, commit de resultados `9d25c47`.

## Grilla ejecutada

Se completó el producto cartesiano de contexto 8/32 ventanas, ancho 16/32,
capas 1/2, learning rate 0,0003/0,001 y dropout 0,1/0,4: 32 configuraciones.
Se evaluaron épocas 2/4/8/16 y suavizado causal 1/8/32. Cuatro cabezas,
feedforward de dos veces el ancho, weight decay 0,01 y batch 256 permanecen fijos.

160 entrenamientos internos en cinco folds; 640 checkpoints y 1.920 puntuaciones
de decisiones internas. Cada fold usa las mismas 16/4 personas para elegir y
20/5 para reajustar/evaluar. Las cinco elecciones se congelaron antes de evaluar
externamente. Se ajustaron 20 modelos externos: cinco folds, dos semillas y dos
modos (historial y ventana actual repetida). Se conservaron 54.096 predicciones.

La etiqueta arousal_label_6s y las 24 variables de EEG, pupila y mirada no cambian.
GSR permanece exclusivo del Modelo Profesor. Validation/test sin reevaluar;
atención no se reentrenó en esta ronda. La solicitud de reintento encontró la
búsqueda completa y se continuó con la auditoría, sin duplicar entrenamientos.

## Resultados

| Modelo | BA macro por persona |
|---|---:|
| Transformer, semilla 20260913 | 0,348097 |
| Transformer, semilla 20260914 | 0,357105 |
| Transformer, promedio de semillas | 0,352601 |
| Control repetido, promedio de semillas | 0,357451 |
| Transformer anterior | 0,363442 |
| Ridge anterior | 0,374750 |

La grilla ampliada no mejoró la evaluación externa. Pierde 1,084 puntos porcentuales
frente al Transformer anterior, IC descriptivo [-3,080; +0,818]. Frente a Ridge,
pierde 2,215 pp, IC [-4,875; +0,376]. Meta BA macro 0,50 no alcanzada.

El contraste de historial frente al control repetido es -0,485 pp, IC
[-1,417; +0,410]. El control conserva el mismo suavizado de salida y se entrena
desde cero con configuración/época/semilla emparejadas; no tiene búsqueda propia.
No hay ventaja clara de la secuencia de entrada. Recall medio del Transformer:
17,46 %. Macro-F1 agrupando ambas semillas: 0,332667; no es un ensamble.

## Selección y límites

Los cinco folds eligieron época 2, learning rate 0,0003 y dropout 0,4. Cuatro
eligieron contexto 8; uno, 32. Solo un fold eligió dos capas. Los scores internos
ganadores estuvieron entre 0,3871 y 0,4222: no equivalen al resultado externo.

La búsqueda usa una semilla interna; dos externas miden variación del reajuste,
no estabilidad de la búsqueda. Un único split interno de cuatro personas y la
selección entre 384 decisiones por fold pueden producir selección inestable.
Los intervalos remuestrean 2.000 veces las 25 personas después de promediar semillas,
sin corregir búsqueda múltiple ni dependencia entre folds. El uso repetido de train
sigue haciendo esta comparación exploratoria, sin confirmación independiente.

Se inicializaron las capas independientemente y se preservó el RNG durante
predicción y callbacks. La implementación anterior consumía RNG al crear una red
para evaluar un checkpoint; se conservó intacta. Comparar ambas rondas no aísla
exclusivamente el tamaño de la grilla. Las pruebas confirman que, en esta nueva
versión, los checkpoints no cambian los pesos finales del entrenamiento.

Preprocesado ajustado solo con fit, máscaras causales y de padding, reinicios por
persona/grabación/discontinuidad. Se puede cruzar estímulos; la normalización
original sigue siendo offline. No se valida un sistema completo en tiempo real.

## Auditoría y artefactos

660 modelos recargados; preprocesado, selección, métricas por fold/persona y
predicciones recalculados. Error máximo de scores 2,98e-8, tolerancia float32/CSV
1e-7; clases idénticas. Predicción auditada sin etiquetas ni señales del profesor.
Las 64 pruebas pasaron en 16,737 segundos. Registro completo en pruebas.json.

Se guardaron todos los intentos, curvas, checkpoints, ranking interno, efectos
descriptivos de hiperparámetros, resultados por semilla y una matriz PNG/PDF.
1.717 hashes verificados frente a los archivos preparados para Git.
Código y resultados en `9d25c47`. Respaldo de notas:
`documentacion/Tesis_Vault_Grid_Transformer_13-09-2026.zip`, con inventario
`documentacion/inventario_vault_grid_transformer_13-09-2026.json`.

Ver [[Tesis_MDS]], [[Avance - 13-09-2026 (Transformer y TCN)]] y
[[Avance - 12-09-2026 (Ablacion y PCA)]].
