# Protocolo de robustez sin cohorte nueva — 24-10-2026

## Preguntas y alcance

1. ¿Cuánto varía entre participantes el rendimiento del Ridge sin `fixation_count` al predecir la pseudoetiqueta principal `arousal_label_6s`?
2. ¿Cuánto cambia la evaluación de **las mismas predicciones** si se compara con `arousal_label_2s` o `arousal_label_pca`?
3. ¿Qué proporción de ventanas cambia de clase al cambiar la regla del Modelo Profesor?

El análisis es retrospectivo y exploratorio. Los 25 participantes de train intervinieron en la selección de modelos. Las ocho personas de test ya se consultaron en investigaciones previas. Validation y P29 no participan. Ningún resultado será llamado validación independiente ni validez psicológica del constructo.

## Predicciones y referencias congeladas

- Train: una predicción fuera de fold por cada una de las 13.524 ventanas de 25 personas, variante `drop_fixation_count` de `resultados/ablacion_pca_12-09-2026/predicciones_oof.csv.gz`.
- Test: las 4.025 predicciones ciegas del ensamble fijo de cinco Ridge de `resultados/evaluacion_test_existente_24-10-2026/predicciones_ciegas.csv.gz`.
- Referencia principal: GSR causal de 6 s. Sensibilidades existentes: GSR de 2 s y PCA de features GSR. El Modelo Estudiante mantiene entradas EEG, mirada y pupila; no usa GSR.
- No se reentrena ni selecciona una regla usando los resultados de sensibilidad. La comparación con una etiqueta distinta es una **discordancia entre objetivos**: no estima cómo rendiría un modelo entrenado específicamente para ella.

## Métricas fijadas antes de calcular

- Balanced accuracy (BA) por participante: media de recall entre las clases presentes en su referencia. Reportar media de BA entre participantes con igual peso, mínimo, máximo, desviación estándar y percentiles descriptivos bootstrap de 2,5 y 97,5 % con 5.000 remuestreos de participantes y semilla 20261024. Informar cuántas clases están presentes y la referencia de predicción constante `1 / clases presentes`.
- Para cada variante de etiqueta: cobertura de ventanas, BA y recall por clase. Para comparar dos etiquetas, usar exactamente las mismas ventanas y participantes con ambas etiquetas no nulas; informar la diferencia pareada de BA por participante y su intervalo bootstrap descriptivo. La etiqueta principal se recalcula en ese soporte común.
- Estabilidad de etiquetas: acuerdo exacto global y macro por participante, kappa global, distribución de cambios de clase. Reportar fracción de personas con BA por encima del valor constante como descriptivo, sin prueba de significancia.
- No sumar ventanas solapadas como observaciones independientes. Los intervalos remuestrean personas, no ventanas. Todos los intervalos son descriptivos; la selección previa de modelos y el uso anterior de test impiden interpretarlos como confirmación.

## Control reproducible

Verificar hashes de fuentes, partición y predicciones; correspondencia por `source_row`, identidad de participante, `split`, ausencia de duplicados y etiqueta principal; guardar protocolo ejecutable, tablas por persona, resúmenes, comparaciones pareadas y matriz de transición. No modificar la partición ni las decisiones científicas abiertas del vault.
