# Minuta: decisiones para la reunión con el profesor guía

> [!info] Estado
> Preparada el 23-11-2026 a pedido de Mario. Es una propuesta para la reunión; **ninguna decisión está tomada** y no hay aprobación registrada del profesor guía sobre los resultados de noviembre. Las cifras son AUC por persona con intervalo de 95 % y salen de `documentacion/Cierre_Experimental_Final_23-11-2026.md` y de los informes citados. Puesta al día el 27-11-2026 con una segunda lectura crítica (`repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/ronda6/SEGUNDA_LECTURA_COMITE.md`): agrega insumos y no decide nada.

## Lo que se presenta en una frase

Con 41 personas, la hipótesis tiene apoyo parcial: el historial de las señales ayuda a predecir la activación (+0,046 [+0,018; +0,073] sobre un placebo en el contraste registrado el 16-11; con respaldo solo para los 6 s anteriores), no la atención; y cerca de un tercio de la detección de atención por EEG (0,681) depende de componentes ligados a los ojos (0,621 al quitarlos).

Tres salvedades que conviene decir junto con esa frase: con el diseño original (entrenamiento, validación y test) el cierre V3 no había mostrado una ventaja consistente, y el análisis con 41 personas se registró después de verlo; el apoyo se refiere a un resumen del historial reciente, no a un modelo secuencial ni a la combinación de señales; y el contraste contra placebo excluye las ventanas de 6 s que promedia la etiqueta, pero no el soporte de su filtro tónico, que usa toda la sesión: la etiqueta es en lo esencial el nivel tónico de la GSR, y cerca de un cuarto de su peso cae antes de esas ventanas y otro cuarto después.

Dos salvedades más, agregadas el 27-11: ese contraste se fijó antes de obtener sus predicciones, pero después de ver, el mismo día y en las mismas personas, que el historial completo superaba al placebo, de modo que es un análisis dirigido y no una evidencia independiente; y el placebo proviene de otros estímulos de la misma persona, así que el contraste no separa la fisiología de los segundos previos de pertenecer a la misma página (secciones 6.6 y 8.4 del borrador de Resultados y Discusión).

## Decisiones

### 1. ¿Se escribe con estos resultados o se planifica una cohorte nueva?

| Opción | Qué implica |
|---|---|
| A. Escribir con lo que hay | La tesis se cierra como estudio exploratorio con apoyo parcial. La cohorte queda como trabajo futuro. No requiere más experimentos. |
| B. Cohorte nueva para confirmar activación | Daría una confirmación independiente, que hoy no existe. El tamaño necesario no está bien estimado: 72, 101 o 767 personas según la varianza usada (las dos primeras, estimadas con 8 personas cada una; la tercera, con las 25 de entrenamiento mezclando folds). Requiere reclutamiento y plazo. |

Por qué importa: las 41 personas incluyen las de validación y test ya consultadas. Es la decisión que define si se escribe o se recluta.

Dato agregado el 26-11 (auditoría de código, `repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/ronda3/AUDITORIA_CODIGO.md`): las 15 hojas del modelo de activación se eligieron con la AUC media de los modelos con 1, 8 y 32 ventanas, la elección la decidió el de 32, y las 25 personas de esa búsqueda son 25 de las 41 evaluadas. El contraste principal de activación se concentra en ellas: +0,055 [+0,012; +0,101] frente a +0,001 [−0,052; +0,055] en las otras 16 el 16-11, y +0,046 frente a +0,021 con cinco particiones. El sesgo a favor del historial es posible y no está demostrado: la diferencia entre grupos no es significativa con 16 personas, y el historial desplazado frente al placebo (+0,035 y +0,064) y la GRU (+0,045 y +0,059) son positivos en ambos grupos. Con la opción A hay que declararlo como límite destacado. Experimento opcional, que aquí solo se lista: una sensibilidad con 7 hojas o con selección anidada; requiere volver a correr y reabrir la experimentación.

Otros dos experimentos opcionales, no corridos, que aquí solo se listan (agregados el 27-11): historial desplazado menos placebo dentro de un mismo estímulo (saldría de predicciones guardadas, sin entrenar; requiere orden del autor y protocolo registrado); y evaluación dejando grupos experimentales fuera (requiere volver a entrenar).
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
| A. Sí | Se ajustan título, hipótesis y objetivos para decir activación. La etiqueta sale de la GSR, que mide activación simpática y no valencia. |
| B. Mantener "emociones" | Habría que justificar que la GSR representa emociones, y no hay señal de valencia ni expresión facial en esta toma de muestra. |

### 4. ¿Qué etiqueta de atención se usa como principal?

| Opción | Qué implica |
|---|---|
| A. La original, y la corregida como análisis | No cambia ningún resultado principal. Hay que explicar que la etiqueta tiene un patrón sistemático al inicio de cada página (la posición sola la predice con 0,598). |
| B. La corregida por posición | La posición deja de predecirla (0,504) y la detección baja poco (0,675 frente a 0,683; −0,008 [−0,015; −0,001], decisión registrada "inferior", al filo). Cambia el 9,4 % de las etiquetas y las comparaciones anteriores dejan de ser directas. |

Por qué importa: la regla del diseño es que la etiqueta se mantiene fija al comparar modelos.
Fuente: `resultados/enfoques_41p_22-11-2026/INFORME.md`.

### 5. ¿Cómo se encuadra la tesis?

| Opción | Qué implica |
|---|---|
| A. Apoyo parcial más advertencia metodológica | Aporte doble: evidencia acotada de que el historial reciente ayuda a predecir la activación, y evidencia de que separar señales no asegura independencia fisiológica (la etiqueta ocular y el EEG comparten la conducta de los ojos). |
| B. Solo la hipótesis de temporalidad | Más simple, pero deja fuera el hallazgo sobre el EEG y expone la detección de atención a la crítica de circularidad. |

Esta decisión incluye con qué lectura del criterio de la hipótesis se llega a "apoyo parcial". El criterio escrito dice que hay apoyo parcial si la ventaja aparece en una sola de las dos variables. Con el análisis de 41 personas la ventaja de desempeño aparece en las dos; el borrador concluye apoyo parcial porque exige además que la ventaja provenga de las ventanas previas, exigencia que no está en el criterio escrito (sección 8.1 del borrador de Resultados y Discusión).

Insumo agregado el 27-11 (segunda lectura crítica), sin decidir: "apoyo parcial" es la más favorable de tres lecturas posibles, y conviene verlas juntas.

| Lectura | Diseño y regla | Qué se concluye |
|---|---|---|
| i | El diseño de evaluación y la regla planificados (entrenamiento, validación y test por separado) | No hay evidencia para sostener la hipótesis: sin ventaja consistente en ninguna de las dos variables |
| ii | El segundo diseño (41 personas en validación cruzada) y el criterio escrito, al pie de la letra | Ventaja de desempeño en las dos variables |
| iii | El segundo diseño y la exigencia añadida de que la ventaja provenga de las ventanas previas | Ventaja solo en activación. Descansa en el contraste del historial desplazado frente al placebo, que se fijó después de ver el placebo del historial completo y cuyo placebo proviene de otros estímulos |

El borrador usa la lectura iii de forma provisoria. Otro insumo para el aporte de la opción A: la advertencia metodológica tiene dos partes, la huella ocular en el EEG y el caso de la posición (una ventaja de un modelo con historial que reproduce un solo número, el tiempo transcurrido en el estímulo).

### 6. ¿Se aceptan etiquetas normalizadas con la sesión completa?

El manuscrito pide normalizar solo con entrenamiento. Las etiquetas vigentes son relativas a la sesión completa de cada persona y se calculan offline. Aceptarlo implica declararlo como límite; no aceptarlo implica rehacer las etiquetas y todos los análisis.

### 7. ¿Queda el *Modelo Profesor* con PCA como definición del *Attention Score*?

La nota [[Modelo Profesor - Decisiones]] proponía la fusión igualitaria como principal y el PCA como análisis de sensibilidad. Los análisis finales usan el *Modelo Profesor* con PCA reconstruido el 29-10. Ambos coinciden en 66 % de las ventanas de entrenamiento (kappa 0,33), y no hay registro de que el cambio se haya decidido con el profesor. Los análisis siguieron con el PCA después de observar, en las 25 personas de entrenamiento, que los modelos lo predecían mejor; eso no es un argumento de validez (el informe del 29-10 lo advierte) y puede favorecer a la versión más ligada a los movimientos oculares que el EEG registra. Dato para esta decisión: en el *Modelo Profesor* con PCA pesan el recorrido de la mirada (0,557), la dispersión (0,520), la duración media de las fijaciones (0,508) y su tiempo total (0,398), y la pupila pesa −0,052; la etiqueta usada es, en la práctica, conducta de mirada, no "mirada y pupila". Confirmarlo deja los resultados como están; no confirmarlo obliga a repetir los análisis de atención.

## Otros puntos abiertos del diseño

Siguen con casilla sin marcar en [[Resumen Diseño Etiquetas y Modelos]]: método de fusión y umbral del *Attention Score*, combinación de variables y umbral del *Arousal Score*, ventana de agregación de la GSR, y si existe alguna fuente de validación externa para las etiquetas. Conviene confirmar que lo usado en los experimentos queda como definición final.

## Hipótesis, objetivos y contribuciones que conviene revisar

Agregado el 26-11-2026 a partir de una lectura crítica del material (`repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/ronda3/LECTURA_CRITICA_COMITE.md`). Lista los textos de [[Estructura Tesis]] que quedaron en tensión con los resultados. **No se editó el esqueleto y nada de esto está decidido**: las redacciones alternativas son opciones para conversar.

| Elemento del esqueleto | Texto actual | Por qué quedó en tensión | Redacción alternativa posible |
|---|---|---|---|
| Hipótesis | "Los modelos temporales multimodales obtienen un mejor desempeño fuera de muestra que los modelos estáticos comparables en la detección de emociones y atención durante la navegación web." | El contraste que la sostiene compara un modelo no secuencial con y sin un resumen del historial; el único modelo que usa el orden (GRU) no mostró ventaja demostrable. No se demostró que combinar señales aporte. "Emociones" depende de la decisión 3, y lo que se predice son pseudoetiquetas. | Mantenerla y declarar en la discusión cómo se operacionalizó; o acotarla a "incorporar el historial reciente de las señales mejora la predicción de las pseudoetiquetas de atención y activación". |
| Objetivo general y objetivos 1 y 6; alcance 2; contribución 1 | "activación emocional" | La GSR mide activación simpática, que no es específicamente emocional: también responde a carga cognitiva, orientación y movimiento. | "activación" o "activación fisiológica (*arousal*)"; conviene decidirlo junto con la decisión 3. |
| Objetivo 1 | "Revisar la literatura sobre atención y activación emocional, con énfasis en modelos temporales y fusión de señales." | El marco teórico sigue casi entero pendiente y varias referencias están sin verificar. | No cambia la redacción; queda como trabajo por hacer. |
| Objetivo 2 | "…sincronizar EEG, GSR, eye tracking y pupilometría con criterios de calidad definidos." | La alineación es por reloj absoluto: hay un desfase de 0,18 a 0,53 s sin corregir, la deriva no se estimó y el montaje no está documentado. | "…sincronizarlas por reloj absoluto y documentar la precisión alcanzada y sus límites." |
| Objetivo 3 | "Definir las pseudoetiquetas continuas y categóricas…, comprobar su estabilidad y separar las señales de etiquetado y predicción." | Los resultados usan solo las etiquetas binarias y no hay un resultado de estabilidad. Lo que hay apunta en contra: las dos versiones del *Modelo Profesor* de atención coinciden en 66 % de las ventanas de entrenamiento (kappa 0,33). | Agregar un análisis de estabilidad (sería análisis nuevo) o cambiar "comprobar su estabilidad" por "describir su sensibilidad a la regla de construcción". |
| Objetivo 4 | "…seleccionando hiperparámetros dentro del entrenamiento." | Se cumple para HGB. La GRU, los MLP y la red convolucional no tuvieron búsqueda, de modo que la comparación entre familias no es pareja. | Mantener y declarar el límite. |
| Objetivo 5 | "Medir el aporte de señales e historial mediante estudios de ablación y comparaciones entre fusión temprana, intermedia y tardía." | En atención la ablación por señal está completa. En activación solo hay importancias descriptivas y ruidosas. La fusión se comparó con una familia y una partición, como contraste secundario. | Mantener y declarar qué parte quedó descriptiva. |
| Objetivo 6 | "Describir los cambios durante la sesión en los scores de atención y activación…" | Hay dos descriptivos hechos con la etiqueta binaria, sin score continuo ni intervalos. | Completar con el score continuo (análisis nuevo) o acotar a "describir de forma exploratoria". |
| Contribución 2 | "Evidencia comparativa sobre estrategias de fusión… dejando abierto si el resultado se debía a la fusión o a la arquitectura." | El signo cambia con la familia de modelo (MLP frente a HGB): no resuelve la pregunta que plantea. | "Evidencia de que la comparación entre fusiones depende de la familia de modelo y no permite elegir una." |
| Contribución 3 | "Un protocolo de construcción de pseudoetiquetas mediante partición disjunta de señales, …de modo que el desempeño sea interpretable como información genuina y no como reconstrucción de la regla de etiquetado. Aplicable a cualquier estudio multimodal sin *ground truth*." | Es lo que la conclusión metodológica principal contradice: separar señales no asegura independencia fisiológica (parte de la detección de la etiqueta ocular desde el EEG depende de componentes del EEG ligados a los ojos). | "Un protocolo de construcción de pseudoetiquetas mediante partición disjunta de señales, y la evidencia de su límite: separar las señales evita la circularidad por definición, pero no asegura independencia fisiológica entre ellas." |
| Nota bajo las contribuciones | "3, 4 y 5 están garantizadas pase lo que pase con los modelos." | La 3 cambió de sentido con los resultados, y la 4 y la 5 tienen los límites de las filas siguientes. | Retirar la nota o corregirla. |
| Contribución 4 | "Un corpus multimodal sincronizado y documentado, con criterios explícitos de calidad por participante, sesión y canal." | La sincronía tiene un desfase conocido; el montaje, la unidad de la GSR, los grupos y la ética no están documentados; no consta que el corpus se publique. | "Un procedimiento reproducible de preprocesamiento y control de calidad, con sus límites." |
| Contribución 5 | "La cuantificación del aporte marginal de cada modalidad y de la componente temporal…, útil para decidir qué señales justifican su costo de registro." | En activación no se cuantificó el aporte por señal. En atención el EEG aporta en parte como registro indirecto de los ojos, lo que cambia la lectura de "costo". | Acotarla a atención y declarar que el aporte del EEG incluye la conducta ocular. |
| Contribución 6 | "Una caracterización descriptiva de la evolución intra-sesión de atención y activación…" | Son dos frases descriptivas, sin score continuo. | Fusionarla con otra o presentarla como observación exploratoria. |
| "Metodología KDD" | "La evaluación final reservada no se utiliza para seleccionar configuraciones." | Validación y test se consultaron varias veces y el análisis final no usa una evaluación reservada. | Describir el diseño que se usó: configuración elegida con 25 personas y validación cruzada sobre 41. |
| "Experiencia Usuario" | Los cuestionarios no indican "en qué momento de la navegación el usuario dejó de atender"; "Esta tesis sigue esa dirección y estima atención y activación emocional por ventanas". | Promete lo **Atendido**; los resultados solo permiten hablar de lo **Observado**. | "…estima, por ventanas, pseudoetiquetas de atención construidas con la conducta ocular y de activación construidas con la GSR." |
| 4.5.1 | "**Decisión (08-08-2026): enfoque 3**" | No dice quién la tomó, y la fusión y el umbral de esa etiqueta siguen abiertos. | "Opción de trabajo desde el 08-08-2026." |
| Norte del proyecto (`CLAUDE.md` del vault) | "el aporte de la tesis está en la temporalidad y el tipo de fusión" | El tipo de fusión no aportó nada concluyente; lo que hay es evidencia acotada sobre el historial y una advertencia metodológica. | Revisarlo junto con la decisión 5. |

## Información que hay que pedir al proyecto

No está en las notas y la tesis no puede cerrarse sin ella: consentimiento informado, aprobación del comité de ética, reclutamiento y criterios de inclusión, edad y sexo de los participantes, protocolo de estímulos y criterio con que se armaron los cuatro grupos (en los datos, cada grupo corresponde a un orden de presentación de los estímulos). También faltan la documentación del montaje de los electrodos y la unidad física de la GSR, que la exportación no declara. Los datos son del proyecto Fondecyt 1231122; hay que pedir esos documentos antes de escribir la sección de participantes y las consideraciones éticas.

## Pregunta adicional: cómo declarar el uso de asistentes automáticos

Las "auditorías" citadas en los borradores y en el cierre son revisiones de código y recálculos de resultados con código separado, hechos con un asistente automático a pedido de Mario. No son la revisión de un tercero. ¿Cómo debe declararse ese uso en la tesis, según la norma del programa?

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
- [[Borrador Resultados y Discusión 23-11-2026]] (vigente; desde el 26-11 integra la discusión fisiológica) · [[Borrador Conclusiones 23-11-2026]] · [[Borrador Secciones pendientes 23-11-2026]]. [[Borrador Discusión fisiológica 23-11-2026]] se conserva solo como registro.
- Auditoría final: `repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/`.
- Lista única de pendientes, armada el 26-11-2026 (ninguna decisión tomada): `notas/pendientes-cierre-26-11-2026.md`, en la raíz del espacio de trabajo `tesis-mds/`.
