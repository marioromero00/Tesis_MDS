# Avances de tesis · guion editable

## 01. ¿Qué aporta el historial a la predicción de atención y activación?

Versión inicial para discutir con el profesor. El recorrido diferencia hechos verificados, resultados históricos y decisiones aún abiertas. Los resultados de activación anteriores a GSR V2 no se usan para sostener la hipótesis.

Fuente: documentacion/Cierre_Experimental_V2_01-11-2026.md

## 02. La pregunta inicial

La tesis parte de la temporalidad y la fusión multimodal. El contraste más reciente usa estadísticas del historial; no demuestra por sí solo que el orden de la secuencia aporte información.

Fuente: ../../documentos/01 Tesis MDS/Marco Teorico/Problema e hipótesis.md

## 03. Antes de entrenar, había que definir qué predecir

El profesor es una regla de construcción de pseudoetiquetas, no una verdad externa. La separación reduce circularidad directa. Normalización y umbrales personales del profesor siguen siendo offline.

Fuente: resultados/profesor_binario_reconstruido_29-10-2026/INFORME.md; resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md

## 04. La evaluación quedó separada por persona

41 participantes en las particiones principales. P29 se mantiene fuera del análisis principal por sensibilidad de sincronización. Los recuentos de ventanas cambian según la tarea y la versión de etiquetas. Validación y test tienen exposición histórica.

Fuente: resultados/modelado/particion_participantes.csv; documentacion/Modelos_Temporales_07-09-2026.md

## 05. Primero comparé modelos y formas de usar el historial

En septiembre se guardaron 104 redes en la primera comparación temporal. También se exploraron fusión temprana y tardía, selección de variables, ensambles y otras arquitecturas. No se trasladan métricas antiguas al objetivo binario V2. La auditoría posterior detectó un problema en el generador histórico.

Fuente: documentacion/Modelos_Temporales_07-09-2026.md; documentacion/Fusiones_10-09-2026.md; resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md

## 06. Después reconstruí atención y recuperé el EEG por canal

La etapa previa agregaba EEG entre canales. Se recuperaron archivos crudos, verificando integridad, y se extrajeron características por canal. Se comprobaron muestras y selección temporal contra el procesamiento anterior. No se atribuye localización anatómica sin mapa de electrodos.

Fuente: documentacion/Crudos_V2_y_EEG_Por_Canal_29-10-2026.md; resultados/temporalidad_eeg_v2_test_29-10-2026/auditoria_extraccion.json; resultados/profesor_binario_reconstruido_29-10-2026/INFORME.md

## 07. El resultado de atención llegó a 0,6744

La comparación mantiene familia y parámetros emparejados. Es el contraste histórico principal del 29 de octubre y no debe confundirse con la comparación contra CatBoost 0,6744. IC bootstrap pareado descriptivo; test previamente consultado.

Fuente: resultados/temporalidad_eeg_v2_test_29-10-2026/INFORME.md

## 08. El historial subió la AUC de 0,6602 a 0,6879

La comparación mantiene familia y parámetros emparejados. Es el contraste histórico principal del 29 de octubre y no debe confundirse con la comparación contra CatBoost 0,6744. IC bootstrap pareado descriptivo; test previamente consultado.

Fuente: resultados/temporalidad_eeg_v2_test_29-10-2026/INFORME.md

## 09. La representación también cambió el resultado

La comparación común del 30 de octubre usa media y desviación histórica de todas las variables. No es la misma representación de la diapositiva anterior. Debe conservarse este resultado favorable, pero no presentarlo como réplica confirmatoria independiente ni como justificación de elegir una representación después de ver test.

Fuente: resultados/comparacion_comun_binaria_30-10-2026/INFORME.md

## 10. En activación aparecieron problemas con las etiquetas

P34 tenía aproximadamente 8,6% de positivos bajo la etiqueta binaria anterior. El diagnóstico de 60 ajustes internos y 15 modelos externos se reprodujo, pero reproducibilidad no equivale a validez del objetivo. Sus resultados se consideran históricos, no evidencia con GSR V2.

Fuente: resultados/activacion_diagnostico_nested_30-10-2026/INFORME.md; ../../notas/bitacora.md

## 11. La auditoría confirmó un error de índices

La operación groupby/apply seguida de reset_index descartaba los índices originales. Las cifras corresponden al archivo completo, incluidos participantes fuera del análisis principal; no son el número de etiquetas binarias que cambiaron. Los errores máximos de reproducción fueron 4,82e-7 y 2,92e-7, compatibles con precisión de exportación. El patrón también aparece en atención histórica; no se extrapola a profesores reconstruidos posteriores.

Fuente: resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md; resultados/etiquetas_gsr_calidad_v2_01-11-2026/auditoria_independiente_02-11-2026.json

## 12. Reconstruí las etiquetas conservando cada ventana

Cinco ventanas de dos segundos, desplazadas un segundo, cubren seis segundos. Los componentes observados constantes aportan cero; ausencias no se rellenan con cero. La mediana y normalización son offline. Esta revisión opera sobre características derivadas, no incorpora un detector fisiológico nuevo sobre señal cruda.

Fuente: resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md

## 13. La corrección dejó 11.796 ventanas etiquetables

Se preservan las 22.211 filas originales con motivo de exclusión. Sin etiqueta: 9.995 por historial insuficiente, 401 por cobertura/flag y 19 por empate. Las 41 personas conservan ambas clases. P4 conserva 26 ventanas etiquetables de 459. Los modelos comparados usan exactamente las mismas filas V2.

Fuente: resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md

## 14. Volví a entrenar con las mismas filas en cada comparación

min_samples_leaf=30; early_stopping=False; random_state=20261101. Preprocesamiento: mediana, indicadores de ausencia y StandardScaler. La representación temporal concatena ventana actual, media y desviación del historial disponible. Exposición histórica de test: esta congelación no restaura independencia.

Fuente: resultados/activacion_gsr_v2_recalculo_02-11-2026/protocolo.json; resultados/activacion_gsr_v2_recalculo_02-11-2026/auditoria_desde_disco.json

## 15. Con GSR V2, las AUC quedaron cerca de 0,50

Selección solo dentro de train: 30 ajustes internos, 15 modelos externos OOF y tres modelos finales. 15 hojas compartidas entre contextos. Se reentrenó el 2 de noviembre con resultados idénticos a la ejecución V2 previa. Test: 8 participantes y 2.184 ventanas. Contexto 8 es secundario, no nuevo ganador seleccionado por test.

Fuente: resultados/activacion_gsr_v2_recalculo_02-11-2026/INFORME.md

## 16. La mejora con 8 ventanas en test no se repitió en validación

El contraste de 8 mejora en 7/8 personas, pero en validación Δ=+0,00269 con IC [-0,0260;0,0333] y OOF Δ=-0,00194 con IC [-0,0495;0,0491]. No inferir diferencias comparando solapamiento de intervalos de AUC individuales: aquí se usan diferencias pareadas. Los intervalos son exploratorios, sin corrección por búsqueda histórica.

Fuente: resultados/activacion_gsr_v2_recalculo_02-11-2026/contrastes.csv

## 17. Además, casi nunca había un historial largo disponible

Promedio ponderado por ventanas en test. Hasta 8 tiene historia media 5,06 y 40,8% de historias completas. Hasta 32 reinicia ante huecos, segmento o estímulo. En V2 solo se utilizan filas etiquetadas para la representación histórica, por lo que se omiten ventanas iniciales válidas sin etiqueta.

Fuente: resultados/activacion_gsr_v2_recalculo_02-11-2026/INFORME.md

## 18. Combinar modalidades tampoco mostró una ventaja clara

Ablación V2 con 54 modelos nuevos, mismos hiperparámetros, participantes y filas. 63 recargas predictivas, 492 AUC y 27 contrastes auditados. Estas ablaciones comparan fusión temprana con modalidades individuales; no completan el contraste entre fusión temprana, intermedia y tardía bajo etiquetas corregidas.

Fuente: resultados/ablacion_modalidades_v2_01-11-2026/INFORME.md

## 19. Atención y activación dejan resultados distintos

No se concluye que la temporalidad nunca sirve. Tampoco se declara validada la hipótesis general. Distinguir discriminación de pseudoetiquetas, mejora frente al estático y validez psicológica. La versión actual documenta estas tres dimensiones por separado.

Fuente: documentacion/Cierre_Experimental_V2_01-11-2026.md; resultados/activacion_gsr_v2_recalculo_02-11-2026/INFORME.md

## 20. La siguiente decisión es cómo cerrar la evaluación

Cierre de la exposición principal. El aporte actual incluye auditoría y corrección del objetivo, controles comparables y una interpretación delimitada. Los anexos profundizan en métrica, muestras y fuentes. No se ha recolectado una cohorte nueva ni ejecutado el protocolo prospectivo.

Fuente: resultados/protocolo_hipotesis_reintento_06-11-2026/INFORME.md

## 21. ROC de atención

Este es el modelo encontrado que coincide con la referencia del usuario a 0,67; la identificación es provisional. La AUC evalúa discriminación y no es porcentaje de aciertos. El comparador estático emparejado con el HistBoost temporal tiene otra AUC. Las curvas se calculan por participante y se interpolan en una malla FPR de 501 puntos. No son curvas sobre ventanas agrupadas; la AUC de la leyenda se calcula antes de interpolar y se verifica contra metricas.csv.

Fuente: resultados/temporalidad_eeg_v2_test_29-10-2026/INFORME.md; resultados/temporalidad_eeg_v2_validacion_29-10-2026/INFORME.md; resultados/temporalidad_eeg_v2_test_29-10-2026/predicciones_test.csv.gz

## 22. ROC de activación GSR V2

Curvas individuales interpoladas sobre una malla FPR común y promediadas. La leyenda presenta media de AUC calculadas directamente por participante, no el área aproximada bajo la curva interpolada. Los IC de los tres AUC absolutos incluyen 0,50.

Fuente: resultados/activacion_gsr_v2_recalculo_02-11-2026/predicciones_externas.csv.gz; resultados/activacion_gsr_v2_recalculo_02-11-2026/metricas.csv

## 23. Señales y características utilizadas

La Toma de Muestra 2 corresponde a registros de navegación web de 2025. No hay expresión facial en este conjunto. El alcance de cada señal debe distinguirse del constructo psicológico que se pretende aproximar.

Fuente: ../../documentos/01 Tesis MDS/Marco Teorico/Problema e hipótesis.md

## 24. Cómo se calculó la AUC

Una AUC cercana a 0,67 no significa 67% de etiquetas correctas a un umbral dado. La discriminación se refiere a las pseudoetiquetas definidas. Para la hipótesis importa ΔAUC temporal menos estático y su incertidumbre, no superar un valor aislado.

Fuente: resultados/temporalidad_eeg_v2_test_29-10-2026/INFORME.md

## 25. Regla de decisión propuesta

El protocolo propuesto usa intervalos simultáneos en ambas tareas. Respaldo si ambos límites inferiores superan el margen; refutación de esa afirmación acotada si algún límite superior queda debajo; si cruzan el margen, el resultado sigue inconcluso. Un diseño honesto no garantiza una decisión binaria.

Fuente: resultados/protocolo_hipotesis_reintento_06-11-2026/INFORME.md

## 26. Escenarios de tamaño de muestra

Potencia 90% por tarea, intervalos bilaterales de 97,5% para control simultáneo. Se verificó el cálculo con 100.000 simulaciones por escenario bajo normalidad. Las varianzas externas usan ocho personas y OOF mezcla modelos de folds distintos; 767 es sensibilidad conservadora, no requerimiento demostrado. El estudio conjunto no suma los N si las personas son las mismas. El margen carece aún de justificación sustantiva independiente.

Fuente: resultados/protocolo_hipotesis_reintento_06-11-2026/INFORME.md; resultados/protocolo_hipotesis_reintento_06-11-2026/verificacion_simulada.json

## 27. Fuentes y resultados reproducibles

Todas las cifras proceden de los informes y tablas locales. Las comparaciones con etiquetas anteriores se presentan como historia de desarrollo. Consultar FUENTES.md para rutas completas y GUIÓN.md para el contenido y notas de toda la presentación.

Fuente: FUENTES.md