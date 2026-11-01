# Cierre de interpretación de temporalidad — 01-11-2026

Este cierre documenta la evidencia disponible; no modifica la hipótesis, las etiquetas aprobadas ni los objetivos académicos. No se continuará buscando configuraciones para obtener una conclusión favorable. La ablación de modalidades se informa por separado.

## Activación con etiquetas V2

La evaluación no lineal fijó HistGradientBoosting y seleccionó sus hiperparámetros exclusivamente dentro de train. El contraste principal predefinido fue historial máximo de 32 ventanas frente a ventana actual, con familia e hiperparámetros compartidos. El de 8 ventanas fue secundario. Los modelos finales se guardaron en Git antes de evaluar validation/test.

| Evaluación | AUC actual | AUC hasta 8 | AUC hasta 32 |
|---|---:|---:|---:|
| OOF train (25 personas) | 0,5021 | 0,5001 | 0,5260 |
| Validation (8 personas) | 0,5182 | 0,5209 | 0,5245 |
| Test (8 personas) | 0,5141 | 0,5470 | 0,5363 |

En test, el contraste principal 32−1 obtuvo ΔAUC +0,0222, IC descriptivo 95% [−0,0130; +0,0585], con mejora en 4/8 personas. En validation obtuvo +0,0063 [−0,0243; +0,0369]. Estos resultados son inconclusos: no prueban superioridad ni equivalencia.

El contraste secundario 8−1 obtuvo en test +0,0329 [+0,0076; +0,0592], con mejora en 7/8 personas. En validation fue +0,0027 [−0,0260; +0,0333] y en OOF train −0,0019 [−0,0495; +0,0491]. Es una señal exploratoria favorable en test, sin consistencia entre particiones; no se convierte retrospectivamente en el contraste principal ni se elige un modelo nuevo a partir de test.

Los intervalos descriptivos de AUC absoluta en test incluyen 0,50 para los tres modelos. Una diferencia pareada favorable frente a otro modelo no demuestra por sí sola capacidad predictiva robusta sobre el nivel de referencia.

El baseline logístico previo con V2 tuvo AUC OOF de 0,5261 / 0,5183 / 0,5139 para contextos 1/8/32. Tampoco mostró una mejora temporal consistente. Comparar con este baseline solo es pertinente en OOF sobre las mismas etiquetas/filas, no comparando su OOF con test del modelo no lineal.

## Qué historial se evaluó realmente

Las ventanas duran 2 s con paso de 1 s: los contextos de 8/32 son límites de hasta 9/33 s de señal. La representación agrega ventana actual, media y desviación histórica; no modela explícitamente el orden de la secuencia.

El historial se construye solo con filas retenidas y se reinicia en huecos y cambios de participante, registro, segmento o estímulo. Ninguna ventana de validation/test tenía 32 ventanas consecutivas retenidas. En test, ctx32 tuvo longitud media de 8,75 ventanas, promediando participantes. Ctx8 tuvo media 5,06 y estuvo completo en 40,84% de las ventanas, promediando participantes. En train, ctx32 estuvo completo solo en 0,39%.

Por ello, el estudio no responde cómo rendiría un modelo con 32 ventanas completas ni permite rechazar toda arquitectura temporal. La baja continuidad limita el contraste de historial largo, pero no demuestra que sea la causa del rendimiento. No se rellenaron huecos ni se relajó la calidad para obtener más historial.

## Atención: evidencia previa y alcance conjunto

En la comparación común de atención, EEG con historial obtuvo AUC test 0,6963 frente a 0,6644 estática: Δ +0,0319, IC descriptivo [0,0037; 0,0562]. La fusión EEG+GSR con historial obtuvo 0,6927 frente a 0,6602 estática: Δ +0,0325 [0,0059; 0,0591]. Son resultados exploratorios favorables bajo esa representación, no confirmación independiente.

En otro contraste principal predefinido de atención, la mejora fue +0,0277 [−0,0041; +0,0505], inconclusa. No se deben mezclar representaciones ni elegir solo la comparación favorable. La atención y activación emplean distintos profesores y predictores: sus AUC no forman un ranking de una misma tarea.

**Conclusión conjunta:** la evidencia sugiere beneficios del historial en algunas comparaciones de atención, pero no una ventaja consistente en activación V2. La hipótesis de superioridad temporal en ambos objetivos no recibe apoyo conjunto suficiente con estos experimentos. Esto no constituye un rechazo universal de los modelos temporales.

## Límites de inferencia

- Train, validation y test fueron consultados históricamente. Congelar esta corrida evita nuevos ajustes a partir de su evaluación, pero no recupera independencia confirmatoria.
- Los intervalos bootstrap se calculan por participante, no por ventanas solapadas. Son descriptivos, sin corrección por búsqueda histórica ni comparaciones múltiples.
- Las etiquetas V2 fueron aprobadas para uso según comunicación de Mario; siguen siendo pseudoetiquetas offline de GSR, sin validación psicológica externa. Aprobación de uso y validez del constructo son cosas distintas.
- El cierre de temporalidad no determina el resultado de la ablación ni implica haber evaluado fusión tardía/intermedia.

## Fuentes verificables

- [Comparación final V2 y auditoría](../resultados/activacion_v2_comparacion_final_01-11-2026/INFORME.md).
- [Baseline logístico V2](../resultados/activacion_v2_historial_01-11-2026/INFORME.md).
- [Comparación común previa de atención y activación](../resultados/comparacion_comun_binaria_30-10-2026/INFORME.md). Su activación usa etiquetas anteriores y no sustituye la evaluación V2.
- [Contraste principal previo de atención](../resultados/temporalidad_eeg_v2_test_29-10-2026/INFORME.md).
