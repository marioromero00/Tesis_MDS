# Contraste de temporalidad y fusión — resultados del 24-10-2026

## Alcance

Se ejecutó el diseño 2 × 2 documentado en [Protocolo_Contraste_Temporalidad_Fusion_24-10-2026.md](Protocolo_Contraste_Temporalidad_Fusion_24-10-2026.md), tras la instrucción de Mario de realizar los experimentos. Activación fue el objetivo principal; atención, el secundario. Se mantuvieron las pseudoetiquetas y la partición originales. Los cinco folds externos usan únicamente los 25 participantes de `train` (13.524 ventanas por objetivo), con dos semillas de reajuste. Validation, test y P29 no se evaluaron.

Las cuatro condiciones son: **E-R** TCN con historial real y fusión temprana; **E-C** TCN con ventana actual repetida y fusión temprana; **T-R** historial real y media de expertos por modalidad; **T-C** control repetido y media de expertos. La arquitectura y los demás parámetros se fijaron antes de la corrida. Se reinicia el historial en cambios de participante, grabación, segmento, estímulo o paso temporal.

## Resultado observado

BA macro promedia primero los recalls de clases presentes por participante y después las personas y las dos semillas. Los valores siguientes son fuera de fold dentro del `train` original.

| Objetivo | E-C | E-R | T-C | T-R |
|---|---:|---:|---:|---:|
| Activación | 0,3524 | 0,3612 | 0,3596 | 0,3630 |
| Atención | 0,3336 | 0,3272 | 0,3423 | 0,3373 |

| Objetivo | Comparación planificada | Diferencia de BA (pp) | IC descriptivo 95 % (pp) | Personas que mejoran |
|---|---|---:|---:|---:|
| Activación | Historial, fusión temprana: E-R − E-C | +0,88 | [-0,28; +2,00] | 14/25 |
| Activación | Fusión con historial: T-R − E-R | +0,18 | [-0,80; +1,37] | 11/25 |
| Atención | Historial, fusión temprana: E-R − E-C | -0,65 | [-1,20; -0,05] | 8/25 |
| Atención | Fusión con historial: T-R − E-R | +1,01 | [+0,13; +1,86] | 16/25 |

Los intervalos son remuestreos pareados descriptivos de 2.000 muestras de las 25 personas, promediando semillas antes del remuestreo. No corrigen las rondas anteriores de búsqueda ni las comparaciones múltiples. El intervalo positivo del contraste secundario de fusión para atención no equivale a confirmación independiente.

El resto de los contrastes está en `contrastes.csv`: en activación, T-R − T-C = +0,33 pp, T-C − E-C = +0,73 pp y la interacción = -0,55 pp; los tres intervalos incluyen cero. En atención, T-R − T-C = -0,50 pp, T-C − E-C = +0,87 pp y la interacción = +0,14 pp; la diferencia de fusión entre controles tiene intervalo descriptivo positivo, pero también es secundaria.

## Diagnóstico por clase

En activación, el recall de la clase **medio** es 23,4 % para E-R y 8,2 % para T-R. La pequeña ventaja de BA media de T-R se acompaña de una pérdida grande en esa clase: no es una mejora uniforme. El historial real sube el recall medio de E-C (20,9 %) a E-R (23,4 %), pero baja el recall alto de 40,0 % a 35,6 %. En atención, el recall medio de E-R es 23,9 % y el de T-R 27,6 %. La tabla completa de recall y fracción predicha por clase está en `diagnostico_clases.csv`.

## Interpretación

**Observado:** el historial real mejora ligeramente la BA de activación en fusión temprana, con intervalo que incluye cero. En atención, la BA de ese mismo contraste baja. La fusión tardía no ofrece una ganancia clara en activación y perjudica el recall medio. En atención, su diferencia positiva es un resultado secundario exploratorio.

**Conclusión permitida:** este experimento tampoco demuestra una ventaja general y estable del historial o de la fusión tardía. Ayuda a precisar dónde aparecen diferencias y qué clases se sacrifican. No cambia la pseudoetiqueta ni prueba que las señales midan atención o activación verdaderas. El Ridge multiescala anterior (0,3748 en activación) sirve como referencia histórica exploratoria, pero no se presenta como control estático ni como contraste pareado de esta corrida.

## Ejecución y auditoría

- Código: `scripts/contraste_temporalidad_fusion.py`; auditoría posterior: `scripts/auditar_contraste_temporalidad_fusion.py`.
- Salida: `resultados/contraste_temporalidad_fusion_24-10-2026/`, con `protocolo.json`, 80 archivos de tarea, 140 modelos `.joblib`, curvas, predicciones por tarea y predicciones OOF consolidadas.
- 216.384 predicciones registradas (13.524 ventanas × 2 semillas × 4 condiciones × 2 objetivos). Cada ventana aparece una vez por semilla y condición en un fold externo. Hay métricas por fold/persona, resumen, contrastes e informe de clases.
- La corrida comprobó que las probabilidades son válidas y que la recarga reproduce exactamente cada modelo. La auditoría independiente volvió a cargar los 140 modelos y recalculó las 216.384 predicciones con un frame que excluye etiquetas y señales del Modelo Profesor; clases idénticas y diferencias numéricas bajo la tolerancia de exportación CSV. Los hashes de modelos, predicciones, fuente, dataset y partición coinciden. Registro: `auditoria_independiente.json`.
- `python -m unittest discover -s tests -v`: 69 pruebas aprobadas, incluidas tres nuevas sobre separación de señales, reinicio del historial y BA por persona.
- Reanudación: ejecutar de nuevo `python scripts/contraste_temporalidad_fusion.py`; comprueba protocolo y hashes antes de reutilizar tareas terminadas. Para repetir desde cero, usar una carpeta de salida nueva con `--output`. El código fuente original de la corrida queda identificado por SHA256 en el manifiesto.

## Límites

Las pseudoetiquetas siguen siendo provisionales y algunas normalizaciones de señal son offline. El historial de hasta ocho ventanas puede abarcar hasta nueve segundos de tiempo transcurrido; no se afirma procesamiento en tiempo real. La fusión tardía usa varios expertos y tiene distinta capacidad que el modelo temprano. El `train` se ha usado en múltiples rondas exploratorias anteriores; ni los intervalos ni un contraste positivo convierten esta corrida en validación confirmatoria. La evaluación final requiere un protocolo acordado y participantes reservados o nuevos.
