# Evaluación independiente y validez de pseudoetiquetas — revisión del 24-10-2026

## Estado de la evidencia

La partición por participante contiene 25 personas en train, 8 en validation y 8 en test; P29 permanece solo para sensibilidad. **Validation ya se usó para comparar entradas y test ya se evaluó en baselines y modelos temporales** (ver `Analisis_Variables_07-09-2026.md` y `Modelos_Temporales_07-09-2026.md`). Reutilizarlos puede aportar una comprobación fuera de los folds recientes, pero no una confirmación independiente nueva del proceso completo de investigación.

El dataset de modelado no contiene autorreportes, desempeño de tarea ni anotaciones humanas independientes de las señales. Solo contiene features de EEG, GSR, pupila y mirada, y scores/etiquetas construidos desde ellas. No se identificó una fuente adicional de validación en los archivos locales revisados. Su disponibilidad sigue pendiente de confirmación; no se interpreta ausencia en este repositorio como prueba de que no exista en el proyecto.

## Auditoría interna realizada

Se ejecutó `scripts/auditar_pseudoetiquetas_24_10_2026.py` sobre las 13.524 ventanas de las 25 personas de train, sin consultar etiquetas de validation o test. Archivos: `resultados/auditoria_pseudoetiquetas_24-10-2026/`, con concordancia global y por persona, clases, umbrales relativos y hashes de fuentes.

| Comparación de reglas | Ventanas con ambas etiquetas | Acuerdo exacto | Kappa | Spearman de scores |
|---|---:|---:|---:|---:|
| Atención: fusión igualitaria vs. PCA | 13.518 | 48,9 % | 0,234 | 0,460 |
| Activación: GSR 6 s vs. PCA | 13.124 | 67,0 % | 0,504 | 0,668 |
| Activación: GSR 6 s vs. GSR 2 s | 13.524 | 82,0 % | 0,728 | 0,852 |

La correlación Spearman entre los componentes de mirada y pupila del score principal de atención es **-0,097** en train. Esto y el acuerdo de 48,9 % con la variante PCA muestran que la definición concreta del profesor de atención influye mucho en la etiqueta. Las comparaciones de activación son más concordantes, pero comparten señal GSR: tampoco constituyen validación externa de activación psicológica.

Las etiquetas son terciles calculados por participante después de normalizar con toda su sesión. Por ello, `alto` significa valor relativamente alto para esa persona; no es un umbral fisiológico común ni una etiqueta disponible de forma causal en tiempo real. La pupila no tiene corrección lumínica documentada. El contexto de GSR de 6 s es una decisión provisional frente a la latencia de respuesta. Ninguna de estas observaciones cambia la construcción actual de etiquetas.

## Evaluación adicional en test existente

Se fijó en `resultados/evaluacion_test_existente_24-10-2026/protocolo.json` la regla de predicción antes de leer las etiquetas de test: media de probabilidades de los cinco Ridge sin `fixation_count` ya guardados, con peso 0,2 cada uno. Los modelos usan solamente los 25 participantes de train; las entradas del estudiante excluyen GSR. El programa guardó `predicciones_ciegas.csv.gz` antes de calcular métricas y registró hashes de datos, modelos y predicciones. Código: `scripts/evaluar_ridge_test_existente_24_10_2026.py`.

En las 4.025 ventanas de ocho participantes de test se obtuvo **BA macro por persona 0,3557**, con intervalo bootstrap descriptivo entre personas **[0,2988; 0,4109]**. BA global: 0,3338; macro-F1 global: 0,3226. El recall por clase fue 0,3115 para `bajo`, 0,2175 para `medio` y 0,4723 para `alto`. La BA por persona varió de 0,2211 a 0,4596. P37 tiene solo dos clases presentes y su BA individual promedia esas dos clases, según la métrica fijada.

El 0,3557 está por debajo del 0,3843 exploratorio obtenido mediante predicciones fuera de fold en train. Son reglas de estimación distintas (ensamble de cinco modelos frente a predicciones de un modelo por fold), así que la diferencia es solo descriptiva. **Esta corrida no confirma una mejora ni constituye una evaluación independiente nueva:** esos ocho participantes de test ya se habían consultado en estudios anteriores. Tampoco valida el constructo de activación, pues la referencia sigue siendo la pseudoetiqueta basada en GSR.

## Protocolo para una evaluación independiente real

1. Obtener participantes de la misma toma de muestra que no hayan intervenido en diseño, selección, análisis o presentación de resultados. Mantener sus identificadores fuera de los 41 participantes de train/validation/test y fuera de P29. Documentar diferencias de dispositivo, tarea, estímulos y calidad antes de calcular métricas.
2. Fijar el predictor **antes** de ver sus etiquetas: como candidato actual, el Ridge sin `fixation_count` de activación. Para aplicación directa se pueden promediar las probabilidades de los cinco modelos guardados en `resultados/ablacion_pca_12-09-2026/modelos/`; cada uno usa solo personas de train. El ensamble de cinco modelos es una regla nueva y debe quedar congelado antes de evaluar. Alternativamente, entrenar una versión final sobre las 25 personas de train con una configuración única elegida solo con train. No elegir entre ambas reglas usando los participantes nuevos.
3. Aplicar el mismo preprocesamiento y la misma construcción del Modelo Profesor a los nuevos registros, conservando su carácter **offline por participante**. Predecir primero desde las entradas permitidas y guardar probabilidades, hashes y predicciones. Abrir las pseudoetiquetas solo después para calcular métricas.
4. Métrica principal: BA macro por persona, promediada entre personas con igual peso. Informar BA global, macro-F1, recall/fracción predicha por clase, distribución individual e intervalo descriptivo por remuestreo de participantes. Comparar con una regla constante documentada y con el desempeño exploratorio de train como referencia contextual, sin tratar este último como un umbral de éxito garantizado.
5. Para validar el **constructo**, obtener una medida independiente de GSR para activación y de mirada/pupila para atención. Definir por adelantado la unidad temporal compartida. Un autorreporte por estímulo solo permite contraste por estímulo o sesión, no una verdad de cada ventana de 2 s. Reportar cobertura, ceguera de anotadores, concordancia y relaciones entre medidas sin adaptar los umbrales después de ver los resultados.

Si solo están disponibles validation/test existentes, registrar la corrida como **evaluación adicional en particiones previamente consultadas**, nunca como confirmación independiente. No cambiar el Modelo Profesor ni los umbrales en medio de esa comparación: cualquier nueva etiqueta crea una tarea distinta y requiere un protocolo aparte. Las cinco decisiones científicas abiertas del vault siguen abiertas.
