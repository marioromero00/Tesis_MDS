# Minuta: decisiones para la reunión con el profesor guía

> [!info] Estado
> Preparada el 23-11-2026 a pedido de Mario. Es una propuesta para la reunión; **ninguna decisión está tomada** y no hay aprobación registrada del profesor guía sobre los resultados de noviembre. Las cifras son AUC por persona con intervalo de 95 % y salen de `documentacion/Cierre_Experimental_Final_23-11-2026.md` y de los informes citados.

## Lo que se presenta en una frase

Con 41 personas, la hipótesis tiene apoyo parcial: el historial de las señales aporta información temporal para la activación (+0,047 [+0,018; +0,078] sobre un placebo, solo en los 6 a 12 s anteriores), no para la atención; y la detección de atención por EEG (0,681) es sobre todo la huella de los ojos (0,621 al quitar los componentes oculares).

## Decisiones

### 1. ¿Se escribe con estos resultados o se planifica una cohorte nueva?

| Opción | Qué implica |
|---|---|
| A. Escribir con lo que hay | La tesis se cierra como estudio exploratorio con apoyo parcial. La cohorte queda como trabajo futuro. No requiere más experimentos. |
| B. Cohorte nueva para confirmar activación | Daría una confirmación independiente, que hoy no existe. El tamaño necesario no está bien estimado: 72, 101 o 767 personas según la varianza usada, cada estimación externa basada en 8 personas. Requiere reclutamiento y plazo. |

Por qué importa: las 41 personas incluyen las de validación y test ya consultadas. Es la decisión que define si se escribe o se recluta.
Fuente: `resultados/protocolo_hipotesis_reintento_06-11-2026/INFORME.md`.

### 2. ¿Qué cuenta como "mejor"? El margen práctico de 0,02

| Opción | Qué implica |
|---|---|
| A. Mantener 0,02 de AUC | Las decisiones quedan como están. Permite declarar nulos concluyentes (atención con posición: +0,001). |
| B. Cualquier mejora sobre 0, como dice la hipótesis | "Efecto relevante" y "respaldo" se funden. Se pierden los nulos concluyentes, que pasan a "sin diferencia demostrada". |
| C. Otro margen | Habría que reclasificar todas las decisiones. Hacerlo después de ver los resultados debe declararse como tal. |

Por qué importa: 0,02 es una propuesta del protocolo del 06-11 que nadie aprobó. Algunas decisiones están cerca del umbral, por ejemplo la red frente al modelo de referencia (límite inferior 0,023).

### 3. ¿"Emociones" se presenta como activación (*arousal*)?

| Opción | Qué implica |
|---|---|
| A. Sí | Se ajustan título, hipótesis y objetivos para decir activación. Es lo que los datos permiten: la etiqueta sale de la GSR, que mide activación simpática y no valencia. |
| B. Mantener "emociones" | Habría que justificar que la GSR representa emociones, y no hay señal de valencia ni expresión facial en esta toma de muestra. |

### 4. ¿Qué etiqueta de atención se usa como principal?

| Opción | Qué implica |
|---|---|
| A. La original, y la corregida como análisis | No cambia ningún resultado principal. Hay que explicar que la etiqueta tiene un patrón sistemático al inicio de cada página (la posición sola la predice con 0,598). |
| B. La corregida por posición | La posición deja de predecirla (0,504) y la detección casi no cambia (0,675 frente a 0,683). Cambia el 9,4 % de las etiquetas y las comparaciones anteriores dejan de ser directas. |

Por qué importa: la regla del diseño es que la etiqueta se mantiene fija al comparar modelos.
Fuente: `resultados/enfoques_41p_22-11-2026/INFORME.md`.

### 5. ¿Cómo se encuadra la tesis?

| Opción | Qué implica |
|---|---|
| A. Apoyo parcial más advertencia metodológica | Aporte doble: evidencia acotada de la activación como proceso dinámico, y la demostración de que separar señales no asegura independencia fisiológica (la etiqueta ocular y el EEG comparten la conducta de los ojos). |
| B. Solo la hipótesis de temporalidad | Más simple, pero deja fuera el hallazgo sobre el EEG y expone la detección de atención a la crítica de circularidad. |

### 6. ¿Se aceptan etiquetas normalizadas con la sesión completa?

El manuscrito pide normalizar solo con entrenamiento. Las etiquetas vigentes son relativas a la sesión completa de cada persona y se calculan offline. Aceptarlo implica declararlo como límite; no aceptarlo implica rehacer las etiquetas y todos los análisis.

### 7. ¿Queda el profesor PCA como definición del *Attention Score*?

La nota [[Modelo Profesor - Decisiones]] proponía la fusión igualitaria como principal y el PCA como análisis de sensibilidad. Los análisis finales usan el profesor PCA reconstruido el 29-10. Ambos coinciden en 66 % de las etiquetas (kappa 0,33), y no hay registro de que el cambio se haya decidido con el profesor. Confirmarlo deja los resultados como están; no confirmarlo obliga a repetir los análisis de atención.

## Otros puntos abiertos del diseño

Siguen con casilla sin marcar en [[Resumen Diseño Etiquetas y Modelos]]: método de fusión y umbral del *Attention Score*, combinación de variables y umbral del *Arousal Score*, ventana de agregación de la GSR, y si existe alguna fuente de validación externa para las etiquetas. Conviene confirmar que lo usado en los experimentos queda como definición final.

## Qué cambia en el texto según lo que se decida

| Decisión | Secciones afectadas |
|---|---|
| 1 | Conclusiones 9.1 y 9.6; alcances |
| 2 | Diseño de evaluación; todas las tablas con columna "decisión" |
| 3 | Título, hipótesis, objetivos, marco teórico de emociones |
| 4 | Capítulo de etiquetas; resultados de atención |
| 5 | Introducción, contribuciones y conclusión general |
| 6 | Limitaciones; diseño de etiquetas |
| 7 | Capítulo de etiquetas; todos los resultados de atención |

## Material de apoyo

- Presentación: `repos/Tesis_MDS/presentaciones/avances_tesis_06-11-2026/index.html`.
- Cierre consolidado: `repos/Tesis_MDS/documentacion/Cierre_Experimental_Final_23-11-2026.md`.
- [[Borrador Conclusiones 23-11-2026]] · [[Borrador Discusión fisiológica 23-11-2026]].
