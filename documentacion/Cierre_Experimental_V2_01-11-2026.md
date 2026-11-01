# Cierre experimental: temporalidad y fusión con activación V2

Se completaron las dos tareas solicitadas por Mario: ablación de modalidades con las etiquetas V2 aprobadas y cierre de interpretación de temporalidad. Los resultados se conservan con sus modelos, predicciones, protocolos previos y auditorías.

## Resultado de fusión

| Modalidad | Test: ventana actual | Test: hasta 8 | Test: hasta 32 |
|---|---:|---:|---:|
| EEG | 0,4982 | 0,5123 | 0,5173 |
| Mirada | 0,5151 | 0,5129 | 0,5215 |
| Pupila | 0,5172 | 0,5461 | 0,5386 |
| Combinadas | 0,5141 | 0,5470 | 0,5363 |

Métrica: ROC-AUC macro por participante, ocho personas de test. Las nueve diferencias pareadas de fusión frente a modalidades individuales en test tienen intervalos descriptivos que incluyen cero. No se demuestra superioridad de la fusión temprana ni equivalencia entre modelos. La configuración fue controlada e idéntica a la del modelo completo, elegida solo en train; no se optimizó por separado cada modalidad.

Se conservaron 7.028 ventanas train, 2.584 validation y 2.184 test en todas las variantes. Se entrenaron 45 modelos OOF y nueve finales unimodales, congelados en Git antes de evaluación externa. La fusión completa se reutilizó sin cambios.

[Resultados completos, contrastes e interpretación de fusión](../resultados/ablacion_modalidades_v2_01-11-2026/INFORME.md). [Auditoría](../resultados/ablacion_modalidades_v2_01-11-2026/auditoria.json): 63 recargas predictivas, 492 AUC y 27 contrastes verificados.

## Resultado de temporalidad

En activación V2, el contraste principal de hasta32 frente a ventana actual fue inconcluso. El secundario de hasta8 fue favorable en test, sin consistencia entre validation y OOF train. Ninguna ventana validation/test tuvo 32 ventanas consecutivas retenidas: se evaluó un límite máximo de historial, no historias completas de esa longitud. No se afirma superioridad temporal general ni se rechazan todas las arquitecturas temporales.

[Cierre detallado de temporalidad](Cierre_Temporalidad_V2_01-11-2026.md).

## Conclusión que puede sostenerse

En este conjunto de experimentos, algunas comparaciones de atención muestran beneficios exploratorios del historial. En activación con pseudoetiquetas V2, la ventaja temporal no es consistente entre particiones y la fusión temprana no demuestra mejorar frente a modalidades individuales en test. La hipótesis de superioridad temporal multimodal conjunta no recibe apoyo suficiente bajo las configuraciones y datos evaluados. Esto no implica equivalencia, ausencia universal de efecto ni invalida otras arquitecturas.

Las particiones tienen exposición histórica; todas las inferencias siguen siendo exploratorias. Los intervalos son descriptivos por participante, sin corrección de comparaciones múltiples. La aprobación de las etiquetas para uso no constituye validación psicológica externa. No se seleccionarán nuevas modalidades o contextos usando estos resultados de test, ni se abrirán nuevas búsquedas para obtener un resultado favorable.

## Conservación

Protocolos, código, modelos, predicciones y cierre quedan en Git local. La subida remota está pendiente por fallo de resolución de github.com en esta sesión; no se declara respaldo remoto completado. Datos crudos externos permanecen fuera del repositorio.
