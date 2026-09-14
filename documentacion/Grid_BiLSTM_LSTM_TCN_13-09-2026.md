# Grid Search de BiLSTM, LSTM y TCN: 13-09-2026

Se completaron y auditaron las tres familias en el orden solicitado: BiLSTM, LSTM y TCN. Cada familia se evaluó con 32 configuraciones, cinco folds y dos semillas externas. Se conservan todos los intentos; cada familia tiene su propio contraste frente a referencias fijas.

## Resultados externos

| Familia | BA macro por persona | BA global | Macro-F1 agrupada | BA del control repetido |
|---|---:|---:|---:|---:|
| BiLSTM | 0.341003 | 0.330889 | 0.321478 | 0.347688 |
| LSTM | 0.333267 | 0.324662 | 0.312699 | 0.350505 |
| TCN | 0.352902 | 0.343171 | 0.329343 | 0.345768 |

Referencias: Ridge 0.374750, Transformer grid 0.352601, Ridge sin fixation_count 0.384325. Este último es un máximo exploratorio de una ablación previa.

BA macro se calcula por persona y semilla y después se promedia. BA global y macro-F1 de la tabla agrupan las predicciones de ambas semillas: no son un ensamble ni 50 personas independientes.

| Familia | Referencia | Ganancia BA (pp) | IC descriptivo 95 % (pp) | Personas que mejoran |
|---|---|---:|---:|---:|
| BiLSTM | Ridge | -3.375 | [-6.065; -0.513] | 9/25 |
| BiLSTM | Ridge sin fixation_count | -4.332 | [-7.236; -1.385] | 5/25 |
| BiLSTM | Transformer grid | -1.160 | [-3.277; +0.845] | 11/25 |
| BiLSTM | Control_repetido | -0.668 | [-1.997; +0.711] | 11/25 |
| LSTM | Ridge | -4.148 | [-6.563; -1.643] | 4/25 |
| LSTM | Ridge sin fixation_count | -5.106 | [-7.634; -2.540] | 3/25 |
| LSTM | Transformer grid | -1.933 | [-3.211; -0.701] | 4/25 |
| LSTM | Control_repetido | -1.724 | [-2.959; -0.618] | 9/25 |
| TCN | Ridge | -2.185 | [-4.815; +0.771] | 10/25 |
| TCN | Ridge sin fixation_count | -3.142 | [-5.692; -0.196] | 8/25 |
| TCN | Transformer grid | +0.030 | [-1.937; +1.894] | 13/25 |
| TCN | Control_repetido | +0.713 | [-0.134; +1.515] | 20/25 |

Meta BA macro 0,50: no alcanzada por ninguna familia.

## Grillas y selección

Producto cartesiano por familia: contexto 8/32 ventanas, hidden size 16/32, profundidad 1/2, learning rate 0,0003/0,001 y dropout 0,1/0,4. En LSTM/BiLSTM profundidad es número de capas recurrentes. En TCN profundidad 1 significa dos bloques con dilataciones 1/2; profundidad 2, cuatro bloques con 1/2/4/8. Cada bloque tiene dos convoluciones de kernel 3: campo receptivo de 13 o 61 pasos, limitado por la historia disponible.

Épocas candidatas 2/4/8/16 y suavizado causal 1/8/32: 384 decisiones por fold, 1.920 por familia, 5.760 en total. Fijos: AdamW, weight decay 0,01, batch 256 y clip de gradiente 1. Dropout en la cabeza de todas las redes, entre capas recurrentes cuando hay dos, y dentro de cada bloque TCN. Igual hidden size no implica igual cantidad de parámetros entre familias; se registra el número para cada selección.

| Familia | Fold | ID | Contexto | Hidden | Profundidad | LR | Dropout | Época | Suavizado | Parámetros | BA interna |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BiLSTM | 1 | g21 | 32 | 16 | 2 | 0.0003 | 0.4 | 2 | 32 | 12387 | 0.390359 |
| BiLSTM | 2 | g17 | 32 | 16 | 1 | 0.0003 | 0.4 | 8 | 8 | 7011 | 0.389229 |
| BiLSTM | 3 | g10 | 8 | 32 | 1 | 0.001 | 0.1 | 8 | 1 | 18115 | 0.392600 |
| BiLSTM | 4 | g31 | 32 | 32 | 2 | 0.001 | 0.4 | 16 | 8 | 43203 | 0.385518 |
| BiLSTM | 5 | g07 | 8 | 16 | 2 | 0.001 | 0.4 | 2 | 32 | 13411 | 0.400891 |
| LSTM | 1 | g05 | 8 | 16 | 2 | 0.0003 | 0.4 | 2 | 1 | 5171 | 0.396159 |
| LSTM | 2 | g12 | 8 | 32 | 2 | 0.0003 | 0.1 | 2 | 32 | 17507 | 0.397725 |
| LSTM | 3 | g27 | 32 | 32 | 1 | 0.001 | 0.4 | 16 | 8 | 9059 | 0.399206 |
| LSTM | 4 | g30 | 32 | 32 | 2 | 0.001 | 0.1 | 16 | 32 | 17507 | 0.376775 |
| LSTM | 5 | g20 | 32 | 16 | 2 | 0.0003 | 0.1 | 8 | 32 | 5683 | 0.399580 |
| TCN | 1 | g11 | 8 | 32 | 1 | 0.001 | 0.4 | 2 | 1 | 13059 | 0.405334 |
| TCN | 2 | g07 | 8 | 16 | 2 | 0.001 | 0.4 | 2 | 32 | 7875 | 0.393889 |
| TCN | 3 | g26 | 32 | 32 | 1 | 0.001 | 0.1 | 16 | 1 | 14083 | 0.384350 |
| TCN | 4 | g25 | 32 | 32 | 1 | 0.0003 | 0.4 | 2 | 1 | 14083 | 0.355661 |
| TCN | 5 | g13 | 8 | 32 | 2 | 0.0003 | 0.4 | 2 | 32 | 26499 | 0.401338 |

## Semillas y clase media

| Familia | Modo | Semilla | BA macro |
|---|---|---:|---:|
| BiLSTM | BiLSTM | 20260913 | 0.332691 |
| BiLSTM | BiLSTM | 20260914 | 0.349316 |
| BiLSTM | repeat_current | 20260913 | 0.341327 |
| BiLSTM | repeat_current | 20260914 | 0.354049 |
| LSTM | LSTM | 20260913 | 0.336785 |
| LSTM | LSTM | 20260914 | 0.329750 |
| LSTM | repeat_current | 20260913 | 0.350513 |
| LSTM | repeat_current | 20260914 | 0.350497 |
| TCN | TCN | 20260913 | 0.349132 |
| TCN | TCN | 20260914 | 0.356672 |
| TCN | repeat_current | 20260913 | 0.342333 |
| TCN | repeat_current | 20260914 | 0.349204 |

| Familia | Modo | Clase | Recall | Fracción predicha |
|---|---|---|---:|---:|
| BiLSTM | BiLSTM | bajo | 0.4323 | 0.4319 |
| BiLSTM | BiLSTM | medio | 0.1622 | 0.1585 |
| BiLSTM | BiLSTM | alto | 0.3982 | 0.4096 |
| BiLSTM | repeat_current | bajo | 0.4264 | 0.4318 |
| BiLSTM | repeat_current | medio | 0.1127 | 0.1146 |
| BiLSTM | repeat_current | alto | 0.4529 | 0.4537 |
| LSTM | LSTM | bajo | 0.4870 | 0.4879 |
| LSTM | LSTM | medio | 0.1448 | 0.1559 |
| LSTM | LSTM | alto | 0.3422 | 0.3562 |
| LSTM | repeat_current | bajo | 0.4816 | 0.4784 |
| LSTM | repeat_current | medio | 0.1162 | 0.1128 |
| LSTM | repeat_current | alto | 0.4106 | 0.4088 |
| TCN | TCN | bajo | 0.4396 | 0.4278 |
| TCN | TCN | medio | 0.1450 | 0.1394 |
| TCN | TCN | alto | 0.4449 | 0.4328 |
| TCN | repeat_current | bajo | 0.4450 | 0.4398 |
| TCN | repeat_current | medio | 0.1355 | 0.1365 |
| TCN | repeat_current | alto | 0.4249 | 0.4237 |

## Diseño y auditoría

Activación, etiqueta arousal_label_6s fija, mismas 24 variables de EEG/pupila/mirada y 25 personas (13.524 ventanas) de train. GSR sigue siendo exclusivo del Modelo Profesor. Atención no se reentrenó. Mismos cinco folds externos 20/5. Cada fold selecciona con una división interna fija 16/4; desempate por ID, época y suavizado. Se congelan las cinco elecciones de cada familia antes de su evaluación externa. Las grillas de las tres familias quedaron definidas antes del primer entrenamiento.

Una semilla interna (20260913), dos externas (20260913/20260914). Las dos externas miden variación del reajuste, no estabilidad de la búsqueda. El control repite la ventana actual en todas las posiciones reales, se entrena desde cero con la configuración/época/semilla elegidas y conserva el mismo suavizado de salida. No tiene búsqueda propia; mide aporte de la secuencia de entrada, no de toda temporalidad.

BiLSTM recorre en ambos sentidos solamente el bloque pasado que termina en la ventana predicha. Se concatenan los estados finales forward/reverse de la última capa; las secuencias empaquetadas excluyen padding. Esto no utiliza ventanas posteriores al endpoint, pero requiere recomputar el bloque pasado y no equivale a un estado recurrente incremental. LSTM usa el estado final de su última capa; TCN aplica padding izquierdo causal. Fuente: [PyTorch LSTM 2.14](https://docs.pytorch.org/docs/2.14/generated/torch.nn.modules.rnn.LSTM.html).

Preprocesadores ajustados solo con fit. Historial reiniciado por participante, grabación o salto distinto de un segundo; puede cruzar estímulos. Hasta 64 segundos de soporte combinado de contexto y suavizado. La normalización original de señales sigue siendo offline: no se valida el pipeline completo en tiempo real.

480 entrenamientos internos, 1.920 checkpoints y 60 modelos externos: 1.980 modelos guardados y recargados. Se recalcularon los 5.760 scores internos, el preprocesado, las elecciones y 162.288 predicciones externas, además de métricas por fold/persona. Tolerancia 1e-7 para float32/CSV y clases idénticas. Se verificaron hashes de fuentes/datos/modelos y el orden efectivo en orden_ejecucion.jsonl. Las 66 pruebas del proyecto pasaron en 14,740 segundos, incluidas exclusión de futuro/padding y preservación del RNG.

Validation/test originales no se reevaluaron. IC descriptivos de 2.000 remuestreos pareados de las 25 personas, promediando semillas antes del bootstrap. Sin corrección por búsqueda múltiple ni dependencia entre folds. Usar repetidamente train mantiene el estudio exploratorio, sin confirmación independiente. Un único split interno de cuatro personas puede seleccionar configuraciones inestables. Los scores internos no son desempeño externo.

La métrica principal promedia recalls de clases presentes en cada persona. Dos personas carecen de una clase; constantes bajo/alto alcanzan 0,346667, medio 0,306667. El ranking interno maximiza época/suavizado dentro de cada fold y configuración; los efectos descriptivos promedian todas las épocas/suavizados. Ninguno redefine el ganador externo ni prueba importancia causal de un hiperparámetro.

Artefactos por familia: protocolo, intentos, selecciones, curvas, checkpoints, modelos, predicciones y auditoría. Carga: joblib.load y recurrentes_grid_core.predict(bundle, frame); la familia se conserva en el bundle. Reanudar: python scripts/ejecutar_grids_recurrentes.py. Las tareas terminadas se conservan y se comprueban las fuentes.
