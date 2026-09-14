# Grid Search de Transformer: 13-09-2026

El Transformer seleccionado dentro de cada fold obtiene BA macro por persona 0.352601, promediando dos semillas. La ronda anterior obtuvo 0.363442; Ridge, 0.374750. La meta 0,50 no se alcanza.

## Grilla ejecutada

Producto cartesiano completo de cinco ejes binarios: 32 configuraciones de arquitectura y optimización. Cada configuración se entrena una vez por fold hasta 16 épocas y se guardan cuatro checkpoints. Evaluar checkpoints y suavizado produce 384 decisiones candidatas por fold y 1.920 en total.

| Parámetro | Valores |
|---|---|
| Contexto | 8, 32 ventanas |
| Ancho d_model | 16, 32 |
| Capas | 1, 2 |
| Learning rate | 0,0003; 0,001 |
| Dropout | 0,1; 0,4 |
| Épocas candidatas | 2, 4, 8, 16 |
| Suavizado causal de salida | 1, 8, 32 ventanas |

Fijos: cuatro cabezas, feedforward de dos veces d_model, AdamW con weight decay 0,01, batch 256, clip de gradiente 1, posiciones aprendidas, pre-norm y pérdida ponderada por persona/clase observada. No se buscaron cabezas, batch o weight decay en esta grilla.

## Evaluación externa

| Modelo | BA macro por persona | BA global | Macro-F1 agrupada |
|---|---:|---:|---:|
| Transformer | 0.352601 | 0.341509 | 0.332667 |
| repeat_current | 0.357451 | 0.344870 | 0.331243 |

BA macro se calcula primero por persona y semilla y luego se promedia. BA global y macro-F1 de la tabla agrupan las predicciones de ambas semillas; no representan un ensamble ni 50 participantes independientes.

| Referencia | Ganancia Transformer (pp) | IC descriptivo 95 % (pp) | Personas que mejoran |
|---|---:|---:|---:|
| Transformer previo | -1.084 | [-3.080; +0.818] | 13/25 |
| Ridge | -2.215 | [-4.875; +0.376] | 10/25 |
| Ridge sin fixation_count | -3.172 | [-5.941; -0.419] | 10/25 |
| Control repetido | -0.485 | [-1.417; +0.410] | 11/25 |

| Modelo | Semilla | BA macro |
|---|---:|---:|
| Transformer | 20260913 | 0.348097 |
| Transformer | 20260914 | 0.357105 |
| repeat_current | 20260913 | 0.352060 |
| repeat_current | 20260914 | 0.362841 |

El control se reajusta con la ventana actual repetida en todas las posiciones reales, con la misma configuración, época, suavizado y semilla seleccionados. Conserva suavizado de salida; el contraste mide el aporte de la secuencia de entrada y no el de toda temporalidad. El control no tiene selección interna propia.

## Configuraciones elegidas

| Fold | ID | Contexto | Ancho | Capas | LR | Dropout | Época | Suavizado | BA interna |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | g09 | 8 | 32 | 1 | 0.0003 | 0.4 | 2 | 8 | 0.422226 |
| 2 | g05 | 8 | 16 | 2 | 0.0003 | 0.4 | 2 | 32 | 0.395936 |
| 3 | g09 | 8 | 32 | 1 | 0.0003 | 0.4 | 2 | 32 | 0.387058 |
| 4 | g01 | 8 | 16 | 1 | 0.0003 | 0.4 | 2 | 32 | 0.398838 |
| 5 | g25 | 32 | 32 | 1 | 0.0003 | 0.4 | 2 | 32 | 0.418637 |

## Clases y estabilidad

| Modelo | Clase | Recall | Fracción predicha |
|---|---|---:|---:|
| Transformer | bajo | 0.4786 | 0.4654 |
| Transformer | medio | 0.1746 | 0.1689 |
| Transformer | alto | 0.3713 | 0.3657 |
| repeat_current | bajo | 0.4776 | 0.4656 |
| repeat_current | medio | 0.1455 | 0.1366 |
| repeat_current | alto | 0.4115 | 0.3978 |

## Protocolo, auditoría y límites

Mismas 25 personas y 13.524 ventanas de train; etiqueta arousal_label_6s fija y 24 variables de EEG, pupila y mirada. GSR sigue siendo exclusivo del Modelo Profesor. Atención no se reentrenó. Cinco folds externos 20/5; cada uno contiene un split interno fijo 16/4. Se eligió por BA media de las clases observadas de cada persona, con desempate ID, época y suavizado. Todas las elecciones quedaron congeladas antes de evaluar fuera del fit. Validation/test no se reevaluaron.

160 entrenamientos internos, 640 checkpoints, 20 modelos externos (cinco folds por dos semillas por dos modos) y 54.096 predicciones externas. La búsqueda interna usa una semilla; las dos externas miden variación del reajuste, no estabilidad de la búsqueda. Un único split interno de cuatro personas puede producir selección inestable. Un score interno alto no equivale a desempeño en personas nuevas.

Preprocesadores ajustados solo con fit. Capas inicializadas independientemente. Predicción y callbacks conservan el RNG: una prueba confirma que checkpoints no cambian pesos finales. La nueva implementación cambia este detalle respecto a la ronda previa, que consumía RNG al crear una red para predecir dentro del callback. Se conserva aquella ejecución sin modificar; la comparación entre rondas no aísla exclusivamente el tamaño de grilla.

Máscaras causales y de padding; historial reiniciado por participante, grabación o salto distinto de un segundo. Se puede cruzar estímulos. Contexto y suavizado máximos abarcan 64 segundos de señal. La normalización original sigue siendo offline; esto no valida un sistema completo en tiempo real.

Auditoría: 660 modelos recargados, preprocesado reajustado, 1920 scores internos y 54096 predicciones externas recalculadas. Error máximo 2.98e-08, tolerancia 1e-7 float32/CSV, clases idénticas. Se verifican hashes de fuentes, datos, modelos, splits y elecciones; predicción sin profesor o etiquetas. Las 64 pruebas del proyecto pasaron en 16,737 segundos; registro completo en pruebas.json.

IC de 2.000 remuestreos pareados de las 25 personas después de promediar semillas. Son descriptivos: no corrigen selección múltiple ni dependencia entre folds. La repetición adaptativa de experimentos sobre train impide interpretar el resultado como confirmación independiente. Ridge sin fixation_count es un máximo exploratorio anterior. Constantes bajo/alto obtienen 0,346667 en BA macro, medio 0,306667, porque dos personas carecen de alguna clase.

El ranking interno toma el máximo sobre épocas/suavizados por configuración y fold; resume la búsqueda y no elige un nuevo ganador externo. Los efectos marginales promedian todas las épocas y suavizados y no prueban importancia causal de un hiperparámetro.

Fuentes: [PyTorch TransformerEncoderLayer](https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html), protocolo.json, intentos.csv, selecciones.json, verificacion.json y pruebas.json. Carga: joblib.load y transformer_grid_core.predict(bundle, frame). Reanudación: entrenar_transformer_grid.py --resume comprueba las fuentes y reutiliza tareas terminadas.
