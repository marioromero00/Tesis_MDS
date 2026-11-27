# Borrador: Modelamiento, Resultados y Discusión

> [!info] Estado
> Borrador redactado el 23-11-2026 a partir de los informes de resultados del repositorio (rutas al final de cada sección). Reemplaza como versión vigente a [[Borrador Resultados y Discusión 18-11-2026]], que se conserva. Integra los análisis del 22 y 23-11-2026 y, desde el 26-11-2026, contiene en su capítulo 8 la discusión fisiológica completa y la lista de referencias de [[Borrador Discusión fisiológica 23-11-2026]], que se conserva como registro. No reemplaza a [[Estructura Tesis]] ni cierra decisiones abiertas de [[Resumen Diseño Etiquetas y Modelos]]. **No hay aprobación registrada del profesor guía** sobre estos resultados ni sobre su encuadre. Las cifras son AUC (área bajo la curva ROC) por persona, con intervalo de confianza de 95 % entre corchetes, salvo que se indique otra cosa. Revisar redacción, citas y numeración antes de pasar a LaTeX. Redacción ajustada el 23-11-2026 a la auditoría final de resultados (`repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/AUDITORIA_EXPERIMENTO.md`). Revisión editorial aplicada el 26-11-2026 (`repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/ronda4/REVISION_EDITORIAL.md`): reordena, fusiona repeticiones y renumera secciones, sin cambiar cifras ni decisiones; el texto anterior está en la carpeta `pre_editorial` de esa ronda. Las líneas "Nota de trabajo (no va en la tesis)" guardan el material de proceso que salió de la prosa. Ajustado el 27-11-2026 a una segunda lectura crítica (`repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/ronda6/SEGUNDA_LECTURA_COMITE.md`), después de comprobar cada hecho en los scripts, protocolos, CSV y el historial de Git: sin cifras nuevas ni análisis nuevos. Ajustado ese mismo día a una tercera lectura, hecha por un evaluador de neurociencia cognitiva y psicofisiología (`repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/ronda7/TERCERA_LECTURA_ESPECIALISTA.md`), con la misma regla: cada hecho se comprobó en su fuente, las afirmaciones fisiológicas nuevas se limitan a las 18 referencias verificadas y lo que requiere otra fuente quedó en notas de trabajo. Consolidación de legibilidad aplicada ese mismo día (`repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/ronda8/VERIFICACION_CORRECCIONES_R7.md`, sección de legibilidad): cada hecho o límite queda con sus cifras en un solo lugar y los demás lugares remiten a él, sin cambiar cifras, decisiones ni la numeración de las secciones; el texto anterior está en la carpeta `pre_consolidacion` de esa ronda.

> [!warning] Decisiones abiertas que este texto no cierra
> El texto usa de forma provisoria: (1) la cohorte nueva como trabajo futuro, es decir, se escribe con las personas ya registradas; (2) el margen práctico de 0,02 en las reglas de decisión; (3) "emociones" presentada como activación (*arousal*); (4) la etiqueta de atención original como etiqueta principal, con la corregida por posición informada como análisis; (5) el encuadre de apoyo parcial; (6) las etiquetas normalizadas con la sesión completa de cada persona, declaradas como límite; (7) el *Modelo Profesor* con PCA (análisis de componentes principales) como definición del *Attention Score*. Las siete dependen del profesor guía y ninguna está tomada (sección 8.10). La numeración es la de [[Avance - 23-11-2026 (Minuta de decisiones con el profesor)]].

## Capítulo 6: Modelamiento y Experimento

### 6.1 Variables objetivo

Se usan dos pseudoetiquetas binarias por ventana de 2 s (paso de 1 s), construidas por un **Modelo Profesor** y predichas por un **Modelo Estudiante** con señales distintas, de acuerdo con la regla de no-circularidad. Aquí *Modelo Profesor* designa una regla fija de etiquetado (un promedio estandarizado o una componente principal), no un modelo entrenado cuyo conocimiento se transfiere: no es destilación de conocimiento.

- **Atención.** El *Attention Score* se obtiene como la primera componente principal de cinco variables de mirada y pupila (tiempo y duración de fijaciones, dispersión y recorrido de la mirada, pupila normalizada), ajustada con las 25 personas de entrenamiento. La componente explica el 51,5 % de la varianza de las cinco variables. Cada ventana se clasifica como alta si supera la mediana de su persona. Quedan con etiqueta 22.176 ventanas de las 41 personas. El *Modelo Estudiante* usa electroencefalograma (EEG) y respuesta galvánica de la piel (GSR).

  Aunque el *Modelo Profesor* recibe mirada y pupila, en la práctica la etiqueta es conducta de mirada: en la componente pesan el recorrido de la mirada (0,557), la dispersión (0,520), la duración media de las fijaciones (0,508) y su tiempo total (0,398), y la pupila casi no pesa y entra con signo contrario (−0,052). Estos pesos se aplican a las variables ya orientadas con la dirección declarada en el diseño: el tiempo total y la duración media de las fijaciones entran con su signo, y la dispersión y el recorrido de la mirada entran invertidos.

  "Alta" designa, entonces, ventanas en que, en conjunto, las fijaciones son más largas y la mirada se dispersa y recorre menos que lo habitual en esa persona: una mirada más quieta. No designa mayor atención en ningún sentido validado, y su sentido tampoco está establecido: no se comprobó que una mirada más quieta corresponda a más atención y no a menos, de modo que "alta" y "baja" son los rótulos del diseño, no una dirección comprobada del constructo.

  Además, dos de las variables de la componente suman la duración completa de las fijaciones que tocan la ventana (la suma supera los 2.000 ms en cerca del 28 % de las ventanas etiquetadas y los 3.000 ms en el 4 %), de modo que el soporte temporal de la etiqueta excede los 2 s (sección 8.2).

  Cuál de dos versiones define el *Attention Score*, el *Modelo Profesor* con PCA o la fusión con pesos iguales, es una decisión abierta (decisión 7, sección 8.10). Las notas de diseño proponían la fusión con pesos iguales como definición principal y la componente principal como análisis de sensibilidad. Los análisis siguieron con la componente principal después de observar, en entrenamiento, que los modelos la predecían mejor. Una etiqueta más predecible no es por eso más válida, y ese criterio puede favorecer a la versión más ligada a los movimientos oculares que el EEG registra. Las dos versiones coinciden en 66 % de las ventanas de entrenamiento (kappa de Cohen 0,33), y los resultados de atención de este capítulo valen solo para la versión usada.

- **Activación.** El *Arousal Score* se calcula a partir de cuatro componentes de GSR promediados sobre cinco ventanas consecutivas válidas (6 s). La versión utilizada (GSR V2, la segunda versión de estas etiquetas) corrige un error de alineación de índices de la versión anterior, exige cobertura de al menos 50 % y deja sin etiqueta los empates con la mediana personal. Conserva 11.796 de 22.211 ventanas. El *Modelo Estudiante* usa EEG, mirada y pupila.

  En la práctica el *Arousal Score* es, en lo esencial, la componente lenta de la GSR (por debajo de 0,05 Hz) relativa a la sesión, que aquí se llama nivel tónico. Incluye el nivel de base y la acumulación de las colas lentas de las respuestas, que el filtro no separa (sección 4.6.3). Dentro de cada persona, el nivel tónico de la ventana ordena la etiqueta con un área bajo la curva ROC (característica operativa del receptor; en adelante, AUC) de 0,911, frente a 0,595 de la componente fásica y 0,522 del número y de la prominencia de las respuestas (en las 32 personas en que esas variables varían; 0,518 con las 41) (análisis descriptivo no registrado).

  Por eso el soporte temporal real de la etiqueta excede los 6 s nominales. En su soporte nominal, la etiqueta de una ventana integra GSR en [t−4, t+2) s. Pero la componente tónica se obtiene con un filtro pasa-bajos de 0,05 Hz aplicado en ambos sentidos sobre la sesión completa, la fásica es la señal menos la tónica y la señal se estandariza por sesión (sección 4.6.3). Del peso de la GSR sobre la parte tónica de la etiqueta de una ventana, el 49 % cae dentro de [t−4, t+2), el 25 % antes de t−4 y el 25 % después de t+2; antes de t−10 queda el 3,7 % (análisis descriptivo no registrado). Además la etiqueta de una ventana incluye GSR de varios segundos después, de modo que parte de la tarea es anticipar la GSR inmediata. No es fuga, porque la GSR no es entrada del *Modelo Estudiante* de activación, pero cambia lo que demuestran los contrastes de la sección 7.3 (se discute en la sección 8.4).

> Nota de trabajo (no va en la tesis): la comparación entre componentes de la GSR y el reparto del peso del filtro tónico son comprobaciones de la auditoría de código del 26-11. La orientación del *Attention Score* se comprobó el 27-11 en `scripts/reconstruir_profesor_atencion_binaria.py` (`DIRECTIONS = [1, 1, −1, −1, 1]` para tiempo total de fijación, duración media, dispersión, recorrido y pupila; las cuatro variables oculares entran en escala logarítmica) y en el archivo guardado del *Modelo Profesor* (`resultados/temporalidad_eeg_v2_validacion_29-10-2026/profesor_final.joblib`: signo +1 y los pesos citados). El informe de los cuatro enfoques la resume como "quietud de la mirada". La segunda lectura proponía describir "alta" como más recorrido y dispersión: no es lo que consta. El conteo de ventanas de atención sale de `resultados/reapertura_41p_22-11-2026/cobertura_atencion.json`.

> Nota de trabajo (no va en la tesis): la tercera lectura (27-11) propone ilustrar por qué el sentido de la etiqueta no está establecido: una mirada más quieta puede acompañar a la lectura detenida, pero también a la espera, a la fatiga o a una mirada que no procesa lo que tiene delante, y una mirada que recorre más puede ser exploración activa de la página. Ninguna de las 18 referencias verificadas lo sostiene: requiere fuente antes de incluirse.

Ambas etiquetas son relativas a la sesión de cada persona y se calculan offline; describen el *Attention Score* y el *Arousal Score* definidos, no una medida externa de atención o activación. En el caso de atención, la etiqueta se apoya en lo **Observado** (mirada y pupila) como aproximación a lo **Atendido**, sin validarlo. En los títulos y las tablas, "atención" y "activación" abrevian *Attention Score* y *Arousal Score*: nombran la etiqueta definida, no el constructo.

En los análisis del 22-11 (sección 6.6) se construyó además una **etiqueta de atención corregida por posición**: en lugar de la mediana de la persona en toda la sesión, usa la mediana de la persona dentro del mismo tramo de posición en el estímulo (1, 2, 3, 4, 5, 6–8, 9–12, 13–20 y 21–32 s). Coincide con la original en el 90,6 % de las ventanas (kappa de Cohen por persona 0,81). Existe como análisis (sección 7.2); si reemplaza a la original es una decisión abierta (decisión 4).

Fuentes: `resultados/profesor_binario_reconstruido_29-10-2026/INFORME.md`, `resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md`, `resultados/enfoques_41p_22-11-2026/INFORME.md`.

### 6.2 Representaciones y modelos

**Ventana actual e historial.** Para cada ventana se compara un modelo que recibe solo la ventana actual con el mismo modelo que recibe además un resumen del historial: media y desviación de las variables en las ventanas previas del mismo estímulo, hasta 32 ventanas. El historial se reinicia al cambiar de estímulo o ante huecos, y se construye con todas las ventanas válidas, tengan o no etiqueta. Como los estímulos son cortos, el historial efectivo promedia 7,8 ventanas en atención y 12,6 en activación. El resumen incluye la ventana actual. Informa además de cuántas ventanas lo forman, aunque ese número no sea una variable: con una sola ventana la desviación es cero, y con pocas la media y la desviación son más ruidosas. Por esa vía el modelo conoce la posición de la ventana dentro del estímulo.

**Familias de modelos.** Se usan dos familias: *HistGradientBoosting* (HGB, árboles con potenciación del gradiente sobre histogramas), con el número de hojas elegido en validación interna de entrenamiento (7 en atención y 15 en activación), y una red recurrente GRU (*Gated Recurrent Unit*) que recibe la secuencia ordenada, con configuración fija. Las tres estrategias de fusión (temprana, intermedia y tardía) se comparan con una misma familia, un perceptrón multicapa (MLP).

**Controles del origen de la mejora.** Para separar la información temporal de otros efectos se usan:

- un *historial placebo*: el mismo número de ventanas de la misma persona, tomadas al azar de otros estímulos, anteriores o posteriores. Iguala la persona y el largo del historial; no iguala el estímulo ni la cercanía en la sesión, de modo que el contraste entre el historial real y el placebo reúne tres cosas: la fisiología de los segundos previos, pertenecer a la misma página y estar en el mismo tramo de la sesión (lo que eso impide concluir se discute en la sección 8.4);
- la *posición en el estímulo*: los segundos transcurridos desde el inicio del segmento, como única variable adicional;
- un *historial desplazado*, que excluye las ventanas más recientes para no coincidir con las ventanas de 6 s que promedia el *Arousal Score* (el filtro tónico de la GSR tiene un soporte más largo; sección 6.1). Estos modelos reciben además una columna con el número de ventanas desplazadas, que codifica la posición en el estímulo. Es igual en el historial real y en el placebo, pero entra en el contraste "desplazado menos sin historial";
- una *curva temporal* (22-11): la ventana actual más la media y la desviación de las ventanas cuyo inicio cae entre L y L+6 s antes, con L de 6, 12, 24, 48 y 96 s, sin importar el estímulo, frente a un placebo de la misma persona a 150 s o más, antes o después. Ese placebo tiene dos variantes: el *placebo disperso*, formado por ventanas sueltas, tantas como las de la banda de 6 s, y el *placebo de bloque*, formado por un bloque contiguo de ventanas;
- la *AUC estratificada*: la AUC de cada persona calculada solo con pares de ventanas del mismo estímulo, del mismo minuto de sesión o de la misma posición.

> Nota de trabajo (no va en la tesis): el informe de origen no declara la columna con el número de ventanas desplazadas. Las definiciones de los dos placebos de la curva se tomaron de `resultados/reapertura_41p_22-11-2026/INFORME.md` (el placebo de la fase 1 "eran ventanas sueltas"; el de la fase 2 "es un bloque contiguo de la misma persona a 150 s o más"); los borradores anteriores no las traían. El detalle de la limpieza (FastICA, banda de ajuste de 1 a 45 Hz, banda del puntaje de 1 a 15 Hz, resguardo de 1 s en torno a las saturaciones, sin umbral, control entre los que no están en los cuatro más oculares) se comprobó el 27-11 en `scripts/limpieza_ocular_41p.py` (encabezado y `protocolo.json`: `band_fit=[1, 45]`, `band_score=[1, 15]`, `rail_guard_s=1`), y la escala y el recorte de la red, en `scripts/red_cruda_41p.py` (`CLIP = 8`). De dónde salen las ventanas de cada placebo se comprobó el 27-11 en el código: `scripts/cierre_robustez_41p.py` (`placebo_hist`) y `scripts/ampliacion_41p.py` (`lag_index`) las sortean entre las ventanas de la misma persona que no pertenecen al segmento de la ventana evaluada, sin restricción de tiempo; `scripts/reapertura_41p.py` (`placebo_indices`), entre las que están a 150 s o más, "antes o después".

**Análisis del EEG (22 y 23-11).** Para estudiar qué detecta el *Modelo Estudiante* de atención se entrenaron modelos sin historial con subconjuntos de variables (solo EEG, solo GSR, bandas alfa y beta, potencia lenta y amplitud, canales frontales y posteriores). El EEG original no tiene limpieza de artefactos oculares: solo se le quita la tendencia lineal y se aplican un filtro de red y un pasabanda de 1 a 45 Hz.

**Limpieza ocular.** Se hizo por persona con análisis de componentes independientes (ICA, algoritmo FastICA). El ajuste usa la sesión completa filtrada entre 1 y 45 Hz y con el filtro de red, tantos componentes como canales utilizables, y deja fuera las muestras a menos de 1 s de una saturación. Cada componente recibe un puntaje ocular: su correlación máxima, entre 1 y 15 Hz, con la mirada horizontal, la mirada vertical o los parpadeos del seguidor ocular (definición de parpadeo en la sección 4.6.4). Se quitan los tres de mayor puntaje, sea cual sea su valor: no hay un umbral. Como control se quitan los tres componentes de mayor varianza entre los que no están entre los cuatro de mayor puntaje ocular; en adelante, "no oculares".

**Red convolucional.** Por último, se entrenó una red convolucional compacta del tipo EEGNet (1.217 parámetros) sobre la señal de 16 canales y 2 s, con una sola arquitectura y configuración fijadas de antemano, sin búsqueda. La señal que recibe está filtrada como en la extracción de variables, escalada por persona y canal con toda la sesión y recortada a ±8 unidades de esa escala. Se la llama "señal cruda", como en los informes y las láminas; el nombre abrevia "sin variables calculadas a mano". En estos análisis, "modelo de referencia" designa al HGB con variables calculadas.

**Otros modelos (22-11).** Un modelo de activación por estímulo, que usa la media y la desviación de las señales en todas las ventanas del segmento, y un modelo adaptado a la persona, que agrega al entrenamiento las ventanas etiquetadas del primer 40 % de la sesión de la persona evaluada.

Fuentes: `resultados/cierre_v3_16-11-2026/INFORME.md`, `resultados/reapertura_41p_22-11-2026/INFORME.md`, `resultados/enfoques_41p_22-11-2026/INFORME.md`, `resultados/limpieza_ocular_41p_23-11-2026/INFORME.md`, `resultados/red_cruda_41p_23-11-2026/INFORME.md`.

### 6.3 Diseño de evaluación

La configuración se eligió solo con las 25 personas de entrenamiento y luego se congeló. El número de hojas se eligió por la AUC media, en validación interna, de los modelos con 1, 8 y 32 ventanas de contexto; el criterio incluye, por lo tanto, al modelo con historial (sus consecuencias están en la sección 7.5).

Para estimar los efectos con más precisión se usó validación cruzada agrupada por persona sobre las 41 personas del análisis principal (8 grupos), de modo que ninguna persona aparece a la vez en ajuste y evaluación. Este diseño se adoptó el 16-11, después de ver los resultados de la evaluación con las particiones originales (entrenamiento, validación y test por separado). Esa evaluación, que aquí se llama *cierre V3* por ser la tercera versión del cierre experimental, no mostró una ventaja consistente del modelo con historial en ninguna de las dos variables. Es un cambio de diseño posterior a los datos y todo lo que sigue debe leerse así.

El análisis del 16-11 usó una partición. Desde el 22-11 la validación cruzada se repite en 5 particiones nuevas y la AUC de cada persona se promedia sobre las cinco; la curva temporal, con sus dos placebos, y la comprobación no registrada de las secciones 7.2 y 7.3 usan una sola partición.

**Términos.** Varias palabras de este texto tienen más de un sentido y se usan así:

- *Estímulo* es cada página o imagen que se presenta. "Página" se usa como sinónimo de estímulo al hablar de lo que la persona ve, también cuando el estímulo es una imagen. Sus categorías están en "Composición de los estímulos", al final de esta lista.
- *Segmento* es una presentación continua de un estímulo a una persona. Dentro de él se definen las ventanas, se arma el historial y se cuenta la posición. "Dentro de un mismo estímulo" significa siempre dentro de un mismo segmento: misma persona y misma presentación. Los segmentos son breves (mediana de tres ventanas en atención).
- *Tramo* designa un intervalo de tiempo: un tramo de la sesión o los tramos de posición de la etiqueta corregida.
- *Partición* tiene dos sentidos. Las "particiones originales" son la división fija de las personas en entrenamiento, validación y test. "Una partición" de la validación cruzada es una asignación de las 41 personas a 8 grupos.
- *Grupo* tiene tres sentidos y lleva siempre su complemento: "grupo de la validación cruzada" (uno de los 8 de una partición), "grupo experimental" (una de las cuatro secuencias de presentación; sección 4.3) y "grupo de personas" (las 25 de entrenamiento frente a las 16 de validación y test; sección 7.5).

**Composición de los estímulos.** Por su nombre en la exportación se distinguen siete categorías. La categoría se asigna por el nombre del estímulo, no por su contenido: el contenido y el propósito de los estímulos numerados y de las imágenes `emotion` y `blur`, la tarea y las instrucciones no están documentados en las notas y deben pedirse al proyecto; tampoco está descrito el contenido de los textos y los diseños.

| Categoría | Ventanas con etiqueta de atención | Ventanas con etiqueta de activación |
|---|---:|---:|
| Sitios web (cinco) | 6.423 (29 %) | 5.457 (46 %) |
| Estímulos identificados solo con un número | 6.637 | 3.291 |
| Diseños | 4.082 | 1.316 |
| Textos | 2.255 | 1.285 |
| Imágenes rotuladas `emotion` | 1.792 | 401 |
| Imágenes rotuladas `blur` | 891 | 0 |
| Instrucciones | 96 | 46 |
| Total | 22.176 | 11.796 |

La exportación trae 116 nombres de estímulo distintos, 95 si no se cuenta el sufijo de repetición; ninguna de las dos cifras es un conteo comprobado de contenidos distintos. "Navegación web" nombra, entonces, el contexto del experimento y no el contenido de la mayoría de las ventanas.

> Nota de trabajo (no va en la tesis): los tipos de estímulo y sus conteos se agregaron el 27-11, tras la tercera lectura: salen de `resultados/ampliacion_41p_16-11-2026/por_categoria.csv` (las siete filas de atención suman 22.176 y las seis de activación, 11.796) y la regla está en `scripts/ampliacion_41p.py` (función `category`: quita el sufijo "(n)" del nombre y asigna `Text` a texto; los prefijos `Meg`, `diario_financiero`, `temu`, `Despega` y `Nint` a sitio web; `diseño`, `emotion` y `blur` a sus categorías; un nombre solo numérico a numerado; y el resto, `Bienvenida` y `Explicacion1`, a instrucciones). El 116 de la lámina 4 es el número de valores distintos de la columna `stimulus` de `caracteristicas_multimodales.csv` (también 116 en las 41 personas); el 95 que contó la tercera lectura es el mismo conteo sin el sufijo "(n)". La diferencia son 15 variantes de `Text` (`Text (19)` a `Text (35)`, distintas según el grupo experimental) y 3 repeticiones de `emotion` y 3 de `diseño`. Ninguna de las dos cifras cuenta contenidos: los textos comparten nombre, y el quinto sitio aparece con un nombre distinto en cada grupo (`Nint`, `Ninte`, `Ninten`, `Nintend`), de modo que los cinco sitios son ocho nombres. Cada persona tiene ventanas en 68 a 98 de esos nombres. Siguen sin describirse el contenido y la duración de los estímulos. La mediana de tres ventanas por segmento es de `resultados/enfoques_41p_22-11-2026/INFORME.md`; el segmento se define en `scripts/preprocesamiento_secuencial.py` (cambio de estímulo dentro de la grabación).

Fuentes: `resultados/cierre_v3_16-11-2026/`, `resultados/cierre_final_41p_16-11-2026/protocolo.json`, `resultados/reapertura_41p_22-11-2026/protocolo.json`, `resultados/ampliacion_41p_16-11-2026/por_categoria.csv` y `scripts/ampliacion_41p.py` (categorías de estímulo), `resultados/preprocesamiento/caracteristicas_multimodales.csv` (nombres de estímulo).

### 6.4 Inferencia y reglas de decisión

La unidad de análisis es la persona: se calcula la AUC de cada persona y se comparan modelos con la diferencia pareada dentro de cada persona. La incertidumbre se estima con *bootstrap* percentil por persona (20.000 réplicas, con la misma semilla en todos los contrastes) y una prueba de permutación de signos; los contrastes de cada familia se corrigen por Holm.

Las reglas de decisión se registraron antes de correr, con un margen práctico de 0,02 de AUC. Son las mismas de la sección 4.8.3:

| Decisión | Condición |
|---|---|
| Respaldo | p de Holm < 0,05 y límite inferior del intervalo de 95 % sobre cero |
| Efecto relevante | además, límite inferior del intervalo de 95 % sobre 0,02 |
| Nulo concluyente | intervalo de 90 % dentro de (−0,02; +0,02) |
| Inferior | límite superior del intervalo de 95 % bajo cero; no exige Holm y tiene precedencia sobre "nulo concluyente" |
| Inconcluso | cualquier otro caso |

El margen de 0,02 no está aprobado por el profesor guía (decisión 2). Varias decisiones dependen de él y quedan cerca del umbral; se indican en cada caso. El nulo del historial en atención no es una de ellas (sección 8.2).

Dos aspectos de la regla registrada condicionan la lectura. El primero es una asimetría que no tiene una justificación escrita: "respaldo" exige la corrección de Holm e "inferior" no la exige. El segundo es la precedencia. Los protocolos listan las reglas sin fijar cuál prevalece cuando una fila cumple dos a la vez, y el código las aplica en el orden respaldo, inferior, nulo concluyente. Eso ocurre en ocho filas, todas de atención y todas con el intervalo de 90 % dentro de ±0,02. Seis quedan como "inferior": las bandas de 24, 48 y 96 s de la curva temporal, las de 48 y 96 s frente al placebo de bloque, y la detección con la etiqueta corregida frente a la original (prueba A1, sección 7.2). Dos quedan como "respaldo": la AUC estratificada dentro del mismo estímulo y el efecto del historial con la etiqueta corregida (prueba A2). Con la precedencia inversa, las seis "inferior" serían "nulo concluyente".

**Límites de la inferencia.** Tres deben declararse. El primero es el tipo de intervalo: con 41 personas el intervalo percentil puede quedar algo estrecho, y por eso los rótulos cuyo límite está a milésimas de un umbral se señalan como tales y no se interpretan como distintos de sus vecinos (contraste principal de atención, límite inferior 0,021; red frente al modelo de referencia, 0,023; historial desplazado frente al placebo, 0,018). El segundo es la dependencia: las AUC por persona no son independientes entre sí, porque cada persona se predice con un modelo ajustado con las demás y las personas de un mismo grupo de la validación cruzada comparten modelo. El *bootstrap* de personas no recoge esa dependencia ni la variación debida al conjunto de entrenamiento, de modo que los intervalos describen a estas 41 personas con estos modelos y pueden ser optimistas como estimación para personas nuevas. El tercero es qué se estima al promediar: con cinco particiones la unidad sigue siendo la persona, pero lo que se estima es el desempeño medio sobre particiones, con menos varianza que en una sola, y el intervalo resultante sigue sin cubrir la variación por conjunto de entrenamiento.

> Nota de trabajo (no va en la tesis): el tipo de intervalo se comprobó el 27-11 en `scripts/cierre_final_41p.py` (función `ci`: cuantiles de 20.000 medias remuestreadas, semilla 20261029, la misma que declaran los protocolos del 16 y del 22-11).

**Códigos de los contrastes.** En las tablas del capítulo 7 los contrastes registrados llevan un código: P1 y P2 son el contraste principal y su control con el tiempo de sesión, en la repetición con cinco particiones (sección 7.1); Q1 y Q2, el historial frente a la posición en activación (sección 7.3); A1 a A3, la etiqueta corregida por posición (sección 7.2); B1 a B8, el aporte de cada señal (sección 7.7); L1 a L4, la limpieza ocular (sección 7.9); R1 a R4, la red convolucional (secciones 7.10 y 7.11); y C1 a C3, la predicción por estímulo (sección 7.11). En la discusión los contrastes se nombran por su contenido, con el código entre paréntesis cuando ayuda a ubicarlos.

Fuentes: `resultados/cierre_final_41p_16-11-2026/protocolo.json`, `resultados/reapertura_41p_22-11-2026/protocolo.json`.

### 6.5 Registro y alcance de la evidencia

**Qué se fijó antes de ejecutar.** El protocolo de cada etapa con modelos se fijó antes de obtener sus predicciones y cada etapa se ejecutó una sola vez, salvo la primera versión del cierre V3, que se detuvo por una revisión de código. No hay un registro externo con sello de tiempo: esto ordena el trabajo, pero no equivale a un prerregistro. Los análisis no registrados (la heterogeneidad por grupo del 16-11, las sensibilidades a personas individuales, la comprobación estratificada del 22-11 y el aporte del historial en el modelo adaptado de la sección 7.11) se rotulan como tales donde aparecen.

Las revisiones de código detectaron problemas antes de evaluar (por ejemplo, indicadores de faltantes ausentes en la fusión tardía y 1 s de solapamiento entre el historial desplazado y la etiqueta de activación), que se corrigieron con enmiendas registradas antes de ver resultados. Desde el 22-11, cada etapa con modelos tuvo además una revisión adicional del código antes de ver resultados y un recálculo de los resultados con código separado. Ambos se hicieron con un asistente automático a pedido del autor; no son revisiones de un tercero. La comprobación no registrada de la fase 2 no pasó por esa revisión.

> Nota de trabajo (no va en la tesis): el protocolo de cada etapa entró al repositorio antes que sus predicciones (orden de commits verificado; los commits están en la tabla de trazabilidad del documento de cierre). La revisión de código y el recálculo hechos con el asistente automático son lo que las notas de trabajo de este borrador y los informes llaman "auditoría". La forma de declarar el uso de asistentes automáticos en la tesis está pendiente.

**Alcance de la evidencia.** La configuración se eligió con 25 de las 41 personas que luego se evalúan, y en activación la elección de 15 hojas la decidió el modelo con historial (sección 7.5): eso permite un sesgo a favor del historial en esas 25 personas, que no está demostrado. Las 16 personas de validación y test habían sido consultadas en etapas anteriores, y los análisis del 22 y 23-11 se pidieron después de ver los resultados del 16 al 18-11. Una familia de contrastes "fijada de antemano" es la que se fijó antes de correr dentro de un análisis dirigido; no designa una confirmación independiente. Ningún resultado de este capítulo se obtuvo en personas nuevas.

Fuentes: `resultados/cierre_v3_16-11-2026/`, `resultados/cierre_final_41p_16-11-2026/protocolo.json`, `resultados/reapertura_41p_22-11-2026/protocolo.json`, `documentacion/Cierre_Experimental_Final_23-11-2026.md`.

### 6.6 Etapas del análisis

Los análisis se identifican en este texto por su contenido y, cuando hace falta distinguirlos, por su fecha. Son doce etapas:

| Análisis | Fecha | Pregunta que responde | Estatus |
|---|---|---|---|
| Cierre V3: evaluación con las particiones originales | 16-11 | Elección y congelación de la configuración; efecto del historial en entrenamiento, validación y test | Registrado; exploratorio |
| Análisis principal con 41 personas, una partición | 16-11 | ¿Rinde mejor el modelo con historial? ¿Aporta el orden de las ventanas? | Registrado; contraste principal fijado de antemano |
| Robustez | 16-11 | ¿Se mantiene la mejora frente a un placebo, sin fuga del *Modelo Profesor* y con otras particiones? | Registrado después de ver el contraste principal de ese día: dirigido |
| Ampliación (experimentos E1 a E6) y enmienda del historial desplazado | 16 al 18-11 | Historial desplazado frente al placebo (E1), calibración con los primeros minutos (E2), tipos de fusión (E3) y descriptivos de sesión, importancia y tipo de página (E4 a E6) | Registrado después de ver el placebo del análisis de robustez: dirigido; E1 principal, E2–E3 secundarios, E4–E6 descriptivos |
| Control de posición ("explicativo de posición") | 18-11 | ¿Se explica la mejora por la posición en el estímulo? | Registrado, pero motivado por resultados vistos: post hoc |
| Reapertura, fase 1: cinco particiones y curva temporal | 22-11 | Contraste principal con más precisión, control del tiempo de sesión y alcance temporal | Registrado; familia fijada antes de correr (P1, P2) y curva secundaria |
| Reapertura, fase 2: placebo de bloque y AUC estratificada | 22-11 | ¿Depende la curva del tipo de placebo? ¿Se mantiene la ganancia dentro del mismo estímulo, minuto o posición? | Post hoc, registrado sin resultados a la vista |
| Reapertura, fase 3: historial frente a posición | 22-11 | ¿Aporta el historial cuando el modelo ya recibe la posición? | Registrado; dirigido |
| Cuatro enfoques (E1 a E4 del 22-11) | 22-11 | Etiqueta corregida por posición (E1), aporte de cada señal (E2), predicción por estímulo (E3) y diferencias entre personas y adaptación (E4) | Registrado; dirigido |
| Montaje y sincronía | 23-11 | Disposición de los electrodos y desfase entre equipos | Descriptivo, sin etiquetas ni modelos |
| Limpieza ocular | 23-11 | ¿Cuánto de la detección de atención depende de componentes oculares del EEG? | Registrado; dirigido |
| Red convolucional sobre la señal cruda | 23-11 | ¿Detecta mejor un modelo más complejo, y de qué depende? | Registrado; dirigido |

La ampliación se registró el mismo 16-11, después de conocer el resultado del análisis de robustez: en activación el historial completo superaba al placebo (sección 7.3). Usa las mismas 41 personas y la misma partición, y su historial desplazado es el historial completo sin sus ventanas más recientes. Con el criterio que este texto aplica al control de posición, es un análisis dirigido por un resultado ya visto: su protocolo se fijó antes de obtener sus predicciones, pero su resultado no es una evidencia independiente de aquel (sección 8.4).

> Nota de trabajo (no va en la tesis): horas de los commits del 16-11, comprobadas el 27-11 con `git log`: resultados de la robustez, `550f924`, 13:25:45 (su informe ya trae el +0,038 con p de Holm 0,043); registro de la ampliación, `d2d5530`, 14:21:14; enmienda del historial desplazado, `8beb675`, 14:25:57. Los ocho grupos de `folds_main` en `resultados/cierre_robustez_41p_16-11-2026/protocolo.json` y de `folds` en `resultados/ampliacion_41p_16-11-2026/protocolo.json` son idénticos. La semilla del placebo es distinta en cada análisis.

La fase 2 incluyó además una comprobación estratificada con la posición, no registrada y hecha después de ver resultados (sección 7.2). Los enfoques E1–E4 del 22-11 no deben confundirse con los experimentos E1–E6 de la ampliación del 16-11; en este texto se identifican siempre por su fecha o por su contenido. La tabla completa, con el estatus detallado y las carpetas de resultados, está en el Anexo de trazabilidad.

Fuente: `documentacion/Cierre_Experimental_Final_23-11-2026.md` (tabla de trazabilidad con los commits de registro, enmienda y resultados).

## Capítulo 7: Resultados

### 7.1 Efecto del historial

Contraste: HGB con hasta 32 ventanas de historial menos HGB con la ventana actual.

| Tarea | Particiones | Sin historial | Con historial | Diferencia | Mejoran | p (Holm) | Decisión |
|---|---|---|---|---|---|---|---|
| Atención | Una (16-11) | 0,684 | 0,710 | +0,026 [+0,018; +0,035] | 36/41 | 0,00001 | Respaldo |
| Atención | Cinco, promedio (22-11) | 0,683 | 0,712 | +0,029 [+0,021; +0,037] | 36/41 | < 0,0001 | Efecto relevante |
| Activación | Una (16-11) | 0,529 | 0,563 | +0,034 [−0,001; +0,069] | 24/41 | 0,066 | Inconcluso |
| Activación | Cinco, promedio (22-11) | 0,518 | 0,554 | +0,036 [+0,010; +0,065] | 23/41 | 0,021 | Respaldo |

El p de Holm se calcula sobre las 2 pruebas del 16-11 (una por tarea) y sobre las 4 del 22-11 (este contraste y su control con el tiempo de sesión, en las dos tareas). Las dos filas de cada tarea miden el mismo contraste, con los mismos modelos y etiquetas. Difieren en la partición: el 16-11 se usó una partición de 8 grupos y el 22-11 se promedió la AUC de cada persona sobre 5 particiones nuevas, lo que reduce el ruido debido a la partición (qué estima ese promedio y qué no cubre su intervalo está en la sección 6.4). El tamaño del efecto casi no cambia; cambia la precisión, y con ella la decisión. En atención el límite inferior pasa de 0,018 a 0,021 y cruza el margen de 0,02. En activación el intervalo deja de incluir el cero. La repetición no es una confirmación independiente (mismas 41 personas; sección 6.5). Además, el contraste de activación ya se había visto positivo el 16-11 en tres particiones alternativas (+0,042 a +0,043, con límites inferiores de +0,006 a +0,013), que no comparten ningún grupo con las cinco del 22-11.

Por partición, la diferencia del 22-11 va de +0,028 a +0,030 en atención y de +0,028 a +0,047 en activación. En activación el signo es estable, pero no todos los intervalos por partición excluyen el cero.

> Nota de trabajo (no va en la tesis): los intervalos por partición son un recálculo de la auditoría final (`documentacion/auditoria_final_23-11-2026/recalculo.json`).

**Controles registrados.**

- *Tiempo de sesión* (22-11, segundo contraste de la familia fijada de antemano, P2): con el tiempo de sesión como variable en ambos modelos, la diferencia es +0,032 [+0,024; +0,040] en atención (37/41; efecto relevante) y +0,026 [−0,006; +0,056] en activación (27/41; p Holm 0,111; inconcluso). Este control solo corrige la tendencia de sesión común a las personas; una deriva lenta con dirección distinta en cada persona, que es lo que el informe de origen describe en activación, queda fuera de él.
- *Modelo Profesor sin las personas evaluadas* (16-11): en atención la diferencia es +0,024 [+0,015; +0,034] (34/41).

**Lecturas descriptivas.**

- En activación el efecto es desigual entre personas: la mediana es +0,014, mejoran 23 de 41 y una persona, P4, aporta 0,009 de los 0,036; es la que conserva solo 26 ventanas con etiqueta, de modo que su AUC es muy imprecisa. La AUC por persona pesa igual a todas las personas y no se fijó un mínimo de ventanas. Sin la persona más influyente la diferencia es +0,028 [+0,006; +0,050] (sensibilidad no registrada).
- Por grupo de personas, el efecto de atención se repite en las 25 de entrenamiento y en las 16 de validación y test; el de activación aparece en las primeras y no en las segundas. Las cifras y su relación con la selección de la configuración están en la sección 7.5.
- En el cierre V3, con las particiones originales, el contraste de atención fue +0,018 [+0,009; +0,027] en entrenamiento (25 personas), +0,020 [−0,003; +0,042] en validación (8) y +0,029 [+0,004; +0,052] en test (8). El de activación incluyó el cero en las tres: +0,016 [−0,036; +0,070], +0,059 [−0,004; +0,131] y +0,033 [−0,021; +0,094].

> Nota de trabajo (no va en la tesis): la sensibilidad sin la persona más influyente la pidió la auditoría de resultados.

"Efecto relevante" en atención describe el tamaño de la mejora, no su origen. El origen se analiza en la sección siguiente y no está en la fisiología de las ventanas previas.

Fuentes: `resultados/cierre_v3_16-11-2026/INFORME.md`, `resultados/cierre_final_41p_16-11-2026/INFORME.md`, `resultados/cierre_robustez_41p_16-11-2026/INFORME.md`, `resultados/reapertura_41p_22-11-2026/INFORME.md`, `documentacion/auditoria_final_23-11-2026/recalculo.json` (recálculo de la auditoría final).

### 7.2 Atención: origen de la mejora

**Placebo (16-11, registrado).** Un historial armado con ventanas de la misma persona tomadas de otros momentos y estímulos mejora tanto como el historial real: placebo menos sin historial, +0,027 [+0,018; +0,035]; real menos placebo, −0,000 [−0,003; +0,003], con intervalo de 90 % [−0,003; +0,003] (nulo concluyente). El informe del 16-11 atribuyó esa mejora al contexto de la persona. Esa lectura no se sostuvo: la calibración con los primeros minutos de sesión de la persona agrega entre +0,001 y +0,004 en atención.

**Posición en el estímulo.** El placebo conserva el largo del historial real, que indica cuántos segundos lleva la persona en el estímulo. La prevalencia de la clase alta de atención depende de ese tiempo: 0,51 en el primer segundo, 0,37–0,38 en el segundo y el tercero, 0,53 entre los 9 y los 12 s y 0,62 desde los 12 s en adelante.

| Contraste | 18-11 (post hoc, una partición) | 22-11, fase 3 (registrado, 5 particiones) |
|---|---|---|
| (Actual + posición) − actual | +0,028 [+0,021; +0,035] · 36/41 | +0,028 [+0,021; +0,036] |
| Historial − (actual + posición) | −0,002 [−0,006; +0,002] | +0,001 [−0,003; +0,004] |
| (Historial + posición) − (actual + posición) | −0,001 [−0,004; +0,002] | +0,001 [−0,002; +0,005] · 21/41 · nulo concluyente |
| Lo mismo, dentro del mismo estímulo | — | −0,000 [−0,003; +0,003] · 22/41 · nulo concluyente |

El análisis del 18-11 se motivó tras observar el placebo y se reporta como post hoc. La fase 3 repitió la pregunta con el contraste fijado antes de correr; sus dos pruebas de atención son las dos últimas filas. Con la posición como variable, lo que agrega el historial queda dentro de ±0,02 (nulo concluyente). Un modelo con la ventana actual y un solo número, los segundos en el estímulo, rinde lo mismo que el modelo con todo el historial (0,711 frente a 0,712; con ambos, 0,713).

**Curva temporal (22-11, secundaria).** Las ventanas de los segundos anteriores no aportan sobre la etiqueta de atención más que un placebo de la misma persona.

| Desfase | Desfase − placebo disperso (fase 1) | Desfase − placebo de bloque (fase 2, post hoc) |
|---|---|---|
| 6 s | −0,004 [−0,010; +0,002] · nulo concluyente | −0,003 [−0,010; +0,004] · nulo concluyente |
| 12 s | −0,004 [−0,012; +0,004] · nulo concluyente | −0,003 [−0,011; +0,004] · nulo concluyente |
| 24 s | −0,007 [−0,013; −0,000] · inferior | −0,006 [−0,013; +0,001] · nulo concluyente |
| 48 s | −0,012 [−0,020; −0,005] · inferior | −0,012 [−0,020; −0,004] · inferior |
| 96 s | −0,010 [−0,016; −0,003] · inferior | −0,009 [−0,016; −0,002] · inferior |

A 24 s las dos variantes dan decisiones distintas con cifras casi iguales, porque el límite superior del intervalo queda en el borde del cero. Las diferencias "inferiores" son pequeñas (hasta −0,012). En esta curva y en la fase 2 las reglas de decisión se usan como lectura descriptiva. No hay tendencia clara con el desfase (−0,002 por duplicación; p 0,071). El análisis del 16-11 con historial desplazado seis ventanas va en el mismo sentido: real menos placebo −0,002 [−0,005; +0,000].

> Nota de trabajo (no va en la tesis): la diferencia del historial desplazado es −0,0025 en el CSV; el INFORME muestra −0,003 por un redondeo doble.

**AUC estratificada (22-11, fase 2, post hoc).** Con el contraste historial menos sin historial, la ganancia en atención se mantiene dentro del mismo estímulo (+0,013 [+0,006; +0,021]), dentro del mismo minuto (+0,023 [+0,016; +0,030]) y a igual posición (+0,017 [+0,010; +0,024]); las tres con decisión de respaldo. Este resultado no contradice el del control de posición, porque se comparan con modelos distintos; así lo indica una comprobación no registrada, hecha después de ver los resultados y con una sola partición: frente al modelo que ya recibe la posición, el historial agrega +0,004 [−0,001; +0,009] a igual posición, −0,003 [−0,007; +0,002] dentro del mismo estímulo y −0,004 [−0,008; +0,001] dentro del mismo minuto. En la fase 3, el contraste registrado calculado a igual posición da +0,005 [+0,001; +0,010] (estrato descriptivo).

**Cuánto depende la etiqueta del reloj (descriptivo).** Un modelo que recibe solo los segundos transcurridos en el estímulo, sin fisiología, llega a 0,598 [0,581; 0,614]. El tiempo de sesión como única variable adicional agrega +0,025 [+0,019; +0,032]. La detección no es un artefacto de la posición: comparando solo ventanas de la misma posición, la AUC sin historial es 0,677 [0,654; 0,699], frente a 0,684 sin estratificar en la misma partición. Tampoco se explica por reconocer el estímulo o el tramo de la sesión: con cinco particiones, la AUC sin historial calculada solo con pares de ventanas del mismo estímulo es 0,684 [0,667; 0,700], frente a 0,683 con todas, y dentro del mismo minuto, 0,675 [0,660; 0,689] (descriptivo; el estrato del mismo estímulo usa cerca del 2 % de los pares).

**Etiqueta corregida por posición (22-11, enfoque E1, registrado).**

| Prueba | Diferencia | Mejoran | p (Holm) | Decisión |
|---|---|---|---|---|
| A1 Detección sin historial: corregida − original | −0,008 [−0,015; −0,001] | 17/41 | 0,055 | Inferior |
| A2 Historial − sin historial, etiqueta corregida | +0,010 [+0,006; +0,015] | 31/41 | 0,0003 | Respaldo |
| A3 (Historial + posición) − (actual + posición), corregida | +0,004 [+0,000; +0,009] | 24/41 | 0,055 | Nulo concluyente |

Con la etiqueta corregida la posición sola deja de predecir (0,504 [0,498; 0,510]; con la original, 0,598). La mejora del historial baja de +0,029 a +0,010 y, con la posición como variable, queda en +0,004. La detección baja poco (0,675 frente a 0,683).

Dos de las tres decisiones están al filo. A1 (−0,008) es "inferior" porque el límite superior de su intervalo es −0,001, y la regla no exige Holm para "inferior". Además compara AUC frente a dos objetivos distintos (cambia el 9,4 % de las etiquetas), por lo que no implica que la detección original fuera espuria. A3 sería "respaldo" con un p de Holm bajo 0,05; es 0,055.

En este análisis las predicciones del modelo con historial y posición son idénticas a las del modelo con historial, de modo que A3 equivale a comparar el modelo con historial con el de la ventana actual con posición. Un diagnóstico posterior, que reajustó un solo grupo de una partición, indica que no es un error: el modelo recibe la columna de posición y no la usa en ninguna de sus 1.800 divisiones, lo que es coherente con que la posición sola no prediga la etiqueta corregida.

> Nota de trabajo (no va en la tesis): el diagnóstico es del 26-11 y está en `documentacion/auditoria_final_23-11-2026/ronda2/DIAGNOSTICO_E1_POSICION.md`.

Fuentes: `resultados/cierre_robustez_41p_16-11-2026/INFORME.md`, `resultados/ampliacion_41p_16-11-2026/INFORME.md` (y `enmienda_e1_lag6/contrastes.csv`), `resultados/explicativo_posicion_41p_18-11-2026/INFORME.md`, `resultados/reapertura_41p_22-11-2026/INFORME.md` (y `curva_temporal.csv`), `resultados/reapertura_fase2_41p_22-11-2026/` (`x1_placebo_bloque.csv`, `x2_estratificada.csv`, `posthoc_no_registrado_estratos_con_posicion.csv`), `resultados/reapertura_fase3_41p_22-11-2026/INFORME.md`, `resultados/enfoques_41p_22-11-2026/INFORME.md` (y `e1_confirmatorio.csv`), `documentacion/auditoria_final_23-11-2026/ronda2/DIAGNOSTICO_E1_POSICION.md`.

### 7.3 Activación: alcance temporal y controles

**Persistencia de la etiqueta (descriptivo).** La etiqueta de activación de 6 s antes en el mismo estímulo predice la actual con AUC 0,680 [0,634; 0,724] (5.035 pares, 40 personas). En atención esa AUC es 0,535 [0,519; 0,552] (8.818 pares). El estado de activación, tal como lo define la etiqueta, persiste varios segundos; el de atención casi no. La etiqueta binaria subestima esa persistencia: la media de la GSR de 30 s antes ordena la etiqueta actual con AUC 0,80 (0,87 a 6 s y 0,85 a 12 s antes; análisis descriptivo no registrado).

> Nota de trabajo (no va en la tesis): la comparación con la media de la GSR es una comprobación de la auditoría de código.

**Placebo e historial desplazado (16-11, registrados).** El historial real supera al placebo en +0,038 [+0,006; +0,068] (26/41; p Holm 0,043), y el placebo no aporta sobre el modelo sin historial (−0,004 [−0,030; +0,024]). Ese placebo proviene de otros estímulos de la misma persona; qué iguala y qué no está en la sección 6.2. La calibración con los primeros minutos de la persona agrega entre +0,001 y +0,009.

El historial desplazado, cuyo protocolo se fijó después de conocer el resultado anterior (sección 6.6), excluye las seis ventanas más recientes y, por lo tanto, no se solapa con las ventanas que promedia el *Arousal Score*. Supera a un placebo equivalente en +0,046 [+0,018; +0,073] (28/41; p Holm 0,004) y al modelo sin historial en +0,053 [+0,022; +0,083]. La decisión registrada es respaldo y no efecto relevante, porque el límite inferior es 0,018. Con cinco ventanas de desplazamiento, que dejan 1 s de solapamiento, la diferencia frente al placebo es +0,040 [+0,012; +0,066]. El desplazamiento no evita el solapamiento con el soporte del filtro tónico de la etiqueta (sección 6.1).

Por grupo de personas (tabla de la sección 7.5), el historial real frente al placebo se concentra en las 25 personas con que se eligió la configuración (+0,057 frente a +0,008), mientras que el historial desplazado frente al placebo es positivo en ambos grupos (+0,035 y +0,064).

**Curva temporal (22-11).**

| Desfase | Desfase − placebo disperso (fase 1, secundaria) | Desfase − placebo de bloque (fase 2, post hoc) |
|---|---|---|
| 6 s | +0,047 [+0,017; +0,078] · p Holm 0,017 · respaldo | +0,053 [+0,026; +0,081] · p Holm 0,003 · efecto relevante |
| 12 s | +0,024 [−0,011; +0,060] · inconcluso | +0,030 [−0,005; +0,064] · inconcluso |
| 24 s | +0,004 [−0,033; +0,042] · inconcluso | +0,009 [−0,027; +0,045] · inconcluso |
| 48 s | −0,023 [−0,053; +0,010] · inconcluso | −0,017 [−0,041; +0,009] · inconcluso |
| 96 s | +0,019 [−0,016; +0,053] · inconcluso | +0,024 [−0,011; +0,059] · inconcluso |

Solo el desfase de 6 s alcanza respaldo; su límite inferior es +0,017. A 12 s el resultado es inconcluso, y desde 24 s el contraste no se distingue del placebo. En ningún caso es un resultado nulo: ningún intervalo de 90 % cabe en ±0,02, de modo que la curva no demuestra que el efecto desaparezca. El contraste cae 0,010 por cada duplicación del desfase [−0,018; −0,003] (p 0,009; 27 de 40 personas); es una sola prueba, sin ajuste. El placebo no aporta sobre la ventana actual (+0,009 [−0,024; +0,043]) y los dos placebos rinden igual (bloque menos disperso, −0,006). El resultado de 6 s no depende de una sola persona (sensibilidad no registrada): sin la más influyente, el contraste queda en +0,039 [+0,012; +0,065] frente al placebo disperso y en +0,046 [+0,021; +0,070] frente al de bloque.

> Nota de trabajo (no va en la tesis): el límite inferior del desfase de 6 s es 0,017474 en `curva_temporal.csv`; el INFORME muestra +0,018 por un redondeo doble. La sensibilidad sin la persona más influyente la pidió la auditoría de resultados.

El +0,047 de la curva (22-11) y el +0,046 del historial desplazado (16-11) se parecen, pero no son el mismo contraste. El del 16-11 usa el historial del mismo estímulo sin sus seis ventanas más recientes, un placebo de otros estímulos, una partición y 41 personas. El del 22-11 usa una banda de 6 s situada 6 s antes, sin importar el estímulo, un placebo a 150 s o más, también una sola partición (la registrada el 16-11) y las filas con cobertura completa hasta 102 s atrás (6.268 filas de 40 personas, el 53 % de las de activación; la persona que falta es la que conserva 26 filas con etiqueta, que no tiene ninguna con esa cobertura, lo que se contó antes de correr).

**Límites de la curva.** En el desfase de 6 s el 73 % de las ventanas pertenece al mismo estímulo que la actual (48 % a 12 s, 13 % a 24 s y 0 % desde 48 s): la curva mezcla cercanía temporal con pertenecer al mismo estímulo. Además, la etiqueta de activación integra GSR en [t−4, t+2) s y la banda de 6 s usa fisiología hasta t−4: en su soporte nominal son contiguas, sin holgura entre ambas. Esa contigüidad vale para el soporte nominal de las ventanas, no para la señal. Por el filtro tónico (sección 6.1), el historial "sin las ventanas de la etiqueta", tanto el desplazado del 16-11 como la banda de 6 s, coincide en el tiempo con GSR que pesa cerca de un cuarto en la componente dominante de la etiqueta. Lo que eso impide concluir se discute en la sección 8.4. El informe de origen declara otros dos límites: el placebo de la curva incluye ventanas futuras (entre el 16 % y el 36 % según la tarea), y solo iguala el número de ventanas de la banda de 6 s; en las demás bandas coincide en el 30–44 % de las filas.

**Control: AUC estratificada (22-11, fase 2, post hoc).** Contraste: historial menos sin historial.

| Estrato | Diferencia | p (Holm) | Decisión |
|---|---|---|---|
| Mismo estímulo | +0,054 [+0,015; +0,094] | 0,022 | Respaldo |
| Mismo minuto de sesión | +0,058 [+0,027; +0,092] | 0,003 | Efecto relevante |
| Misma posición en el estímulo | +0,027 [−0,003; +0,059] | 0,092 | Inconcluso |

La ganancia se mantiene dentro del mismo minuto; es un análisis post hoc, y el control registrado del tiempo de sesión quedó inconcluso (sección 7.1). Dentro de un mismo estímulo o de un mismo minuto, la ventana actual sola no distingue nada (AUC 0,501 en ambos); con historial sube a 0,555 y 0,560. Estas AUC usan una fracción pequeña de las comparaciones: el 2–3 % de los pares de una persona cae dentro de un mismo estímulo y el 7 % dentro de un mismo minuto.

**Control: historial frente a posición (22-11, fase 3, registrado).** Contraste: (historial + posición) − (ventana actual + posición).

| Prueba | Diferencia | Mejoran | p | p (Holm) | Decisión |
|---|---|---|---|---|---|
| Q1 Todas las comparaciones | +0,032 [+0,004; +0,059] | 28/41 | 0,027 | 0,108 | Inconcluso |
| Q2 Dentro del mismo estímulo | +0,009 [−0,020; +0,037] | 20/41 | 0,57 | 1,00 | Inconcluso |

Las dos columnas de p son el valor sin ajustar y el de Holm sobre las cuatro pruebas de la fase. En Q1 el intervalo sin ajustar queda sobre cero, pero no pasa esa corrección. La media y la mediana coinciden (+0,032 y +0,031) y la persona más influyente empuja en contra: sin ella la diferencia es +0,039 [+0,015; +0,063] (sensibilidad descriptiva, sin ajuste).

| Modelo | AUC, todas las comparaciones | AUC, mismo estímulo |
|---|---|---|
| Ventana actual | 0,518 | 0,501 |
| Ventana actual + posición | 0,523 | 0,550 |
| Historial hasta 32 | 0,554 | 0,555 |
| Historial + posición | 0,555 | 0,559 |

La posición actúa de forma distinta según la comparación. Entre todas las ventanas no se observa aporte de la posición (+0,006 [−0,015; +0,026]) y sí del historial (+0,031 [+0,004; +0,057] sobre el modelo con posición; descriptivo, sin ajuste). Dentro de un mismo estímulo el tiempo transcurrido mejora la predicción por sí solo (+0,049 [+0,027; +0,072]) y no se demostró que el historial lo supere (+0,005 [−0,025; +0,035]). Esta comparación es descriptiva y Q2 es inconcluso y de poca potencia: no demuestran que, dentro de un mismo estímulo, el aporte del historial se explique por el tiempo transcurrido, ni que no exista.

Otros dos análisis miran la misma pregunta con una sola partición. El control de posición post hoc del 18-11 había dado historial menos posición +0,038 [+0,002; +0,074] y posición menos sin historial −0,004 [−0,023; +0,017]. La comprobación no registrada del 22-11 coincide con la fase 3 en el signo del aporte de la posición dentro de un mismo estímulo (posición menos sin historial, +0,040 [+0,014; +0,067]); en historial menos posición el signo difiere (−0,015 [−0,056; +0,024], frente a +0,005 en la fase 3), con intervalos que incluyen el cero en ambos casos.

Fuentes: `resultados/cierre_robustez_41p_16-11-2026/INFORME.md`, `resultados/ampliacion_41p_16-11-2026/INFORME.md`, `resultados/explicativo_posicion_41p_18-11-2026/INFORME.md`, `resultados/reapertura_41p_22-11-2026/INFORME.md`, `resultados/reapertura_fase2_41p_22-11-2026/` (`x1_placebo_bloque.csv`, `x2_estratificada.csv`, `descriptivos.csv`, `posthoc_no_registrado_estratos_con_posicion.csv`), `resultados/reapertura_fase3_41p_22-11-2026/INFORME.md`.

### 7.4 Orden de las ventanas

La red GRU es el único modelo que usa el orden de las ventanas. Se evaluó el 16-11 con una partición, como contraste secundario y sin corrección por multiplicidad. Los análisis del 22 y 23-11 no la incluyen.

| Tarea | GRU hasta 32 − GRU una ventana | GRU hasta 32 − HGB hasta 32 |
|---|---|---|
| Atención | +0,008 [−0,004; +0,020] · 26/41 · intervalo de 90 % dentro de ±0,02 | −0,040 [−0,055; −0,027] · 9/41 |
| Activación | +0,051 [+0,021; +0,080] · 28/41 · p 0,002 sin corregir | +0,020 [−0,017; +0,057] · 22/41 |

En atención el orden no agrega un efecto relevante y la GRU rinde 0,040 menos que el resumen estadístico. En activación la GRU con historial supera a su control de una ventana, pero no supera de forma demostrable al HGB con historial. En el cierre V3 esa mejora apareció en validación (+0,091) y en test (+0,084) y no en entrenamiento (−0,016). Ese contraste mide el aporte del historial dentro de la GRU, no el del orden; el contraste propio del orden (GRU menos HGB, ambos con historial) es inconcluso. Es una observación secundaria, no un resultado.

Fuentes: `resultados/cierre_final_41p_16-11-2026/INFORME.md`, `resultados/cierre_v3_16-11-2026/INFORME.md`.

### 7.5 Estabilidad del efecto de activación entre grupos de personas

Esta sección reúne lo que se sabe sobre un límite del contraste principal de activación: la configuración se eligió con parte de las personas que luego se evalúan, y el efecto no es igual en ese grupo y en el resto. Las comparaciones por grupo son descriptivas y no registradas.

**Cómo se eligió la configuración.** Las 15 hojas de activación se eligieron con las 25 personas de entrenamiento, por la AUC media en validación interna de los modelos con 1, 8 y 32 ventanas de contexto. La elección la decide el contexto de 32:

| Contexto | 7 hojas | 15 hojas |
|---|---|---|
| 1 ventana | 0,5123 | 0,5121 |
| 8 ventanas | 0,5341 | 0,5311 |
| 32 ventanas | 0,4994 | 0,5311 |
| Media (criterio) | 0,5152 | 0,5248 |

En esa búsqueda, historial menos sin historial vale −0,013 con 7 hojas y +0,019 con 15: se congeló la configuración en que el historial gana. En atención la elección no importa (+0,0135 con 7 hojas y +0,0124 con 15). Como esas 25 personas son 25 de las 41 que luego se evalúan, el diseño permite un sesgo a favor del historial en ellas.

**El efecto por grupo.** En atención el efecto del historial se repite en los dos grupos (análisis del 16-11, no registrado en el protocolo): +0,023 [+0,014; +0,031] en las 25 personas de entrenamiento y +0,032 [+0,016; +0,048] en las 16 de validación y test. En activación no. La tabla separa por grupo las predicciones guardadas de cada contraste de activación:

Tabla: contrastes de activación en las 41 personas y por grupo (descriptiva y no registrada). Los intervalos de la columna de 41 personas están en las secciones 7.1, 7.3 y 7.4.

| Contraste de activación | 41 personas | 25 de la búsqueda | 16 restantes |
|---|---|---|---|
| Principal, una partición (16-11) | +0,034 | +0,055 [+0,012; +0,101] | +0,001 [−0,052; +0,055] |
| Principal, 5 particiones (22-11) | +0,036 | +0,046 [+0,012; +0,086] | +0,021 [−0,017; +0,060] |
| Con tiempo de sesión (sección 7.1) | +0,026 | +0,050 [+0,013; +0,085] | −0,011 [−0,066; +0,038] |
| Con posición (Q1; sección 7.3) | +0,032 | +0,049 [+0,018; +0,081] | +0,006 [−0,043; +0,049] |
| Historial − posición (18-11, post hoc) | +0,038 | +0,063 [+0,021; +0,109] | −0,001 [−0,056; +0,054] |
| Historial − placebo (16-11) | +0,038 | +0,057 [+0,023; +0,092] | +0,008 [−0,048; +0,058] |
| Historial desplazado seis ventanas − placebo | +0,046 | +0,035 [+0,003; +0,064] | +0,064 [+0,015; +0,115] |
| Banda de 6 s − placebo (40 personas: 24 y 16) | +0,047 | +0,058 [+0,015; +0,101] | +0,030 [−0,003; +0,068] |
| GRU hasta 32 − GRU una ventana (sin búsqueda) | +0,051 | +0,045 [+0,007; +0,083] | +0,059 [+0,014; +0,101] |

Los contrastes del HGB con historial hasta 32 se concentran en las 25 personas de la búsqueda. El sesgo es posible y no está demostrado. Los intervalos de ambos grupos se solapan y la diferencia entre grupos no alcanza significación en ninguno de los nueve contrastes de la tabla (principal del 16-11: +0,054, p = 0,15; con cinco particiones, p = 0,38; los más cercanos al umbral son el contraste con tiempo de sesión, p = 0,08, y el de historial menos posición, p = 0,09; prueba de Welch sobre las diferencias por persona, comprobación no registrada).

En el cierre V3, con modelos ajustados solo con las 25, el patrón había sido el inverso: el mismo contraste fue +0,059 en validación y +0,033 en test (8 personas cada uno, con intervalos que incluyen el cero), y +0,016 [−0,036; +0,070] en las propias 25 con selección anidada, es decir, con la configuración elegida en una validación interna que no incluye a las personas evaluadas (sección 4.8.2).

Los dos contrastes que no dependen de esa elección de la misma forma, el historial desplazado frente al placebo y la GRU, que no tuvo búsqueda, son positivos en ambos grupos. Lo que queda es que el efecto no es estable entre subconjuntos de personas ni entre diseños de evaluación, y que el "respaldo" del contraste principal es más débil de lo que indica su intervalo. Una sensibilidad con 7 hojas o con selección anidada lo resolvería; no se corrió.

> Nota de trabajo (no va en la tesis): la separación por grupo de las predicciones guardadas y la prueba de Welch son comprobaciones de la auditoría de código del 26-11.

Fuentes: `resultados/cierre_v3_16-11-2026/INFORME.md`, `resultados/cierre_final_41p_16-11-2026/INFORME.md`, `resultados/cierre_robustez_41p_16-11-2026/INFORME.md`, `resultados/reapertura_41p_22-11-2026/INFORME.md`, `documentacion/auditoria_final_23-11-2026/recalculo.json` (recálculo de la auditoría final).

### 7.6 Tipos de fusión

Con una misma familia (MLP), 41 personas y una partición (16-11, secundario):

| Tarea | Tardía − temprana | Intermedia − temprana | Intermedia − tardía |
|---|---|---|---|
| Atención | +0,012 [+0,005; +0,021] | +0,005 [−0,003; +0,013] | −0,007 [−0,014; −0,001] |
| Activación | +0,006 [−0,032; +0,042] | +0,002 [−0,019; +0,023] | −0,004 [−0,042; +0,039] |

En atención, entre redes MLP, la fusión tardía supera a la temprana y a la intermedia; son contrastes secundarios, sin corrección. En activación no se demostraron diferencias. La arquitectura intermedia evaluada es más profunda que la temprana, por lo que la comparación incluye también una diferencia de capacidad.

El resultado depende de la familia de modelos. En el cierre V3, con HGB y las particiones originales, la fusión tardía no superó a la temprana: en atención la diferencia fue −0,010 [−0,018; −0,003] en entrenamiento, −0,008 [−0,020; +0,005] en validación y −0,002 [−0,015; +0,008] en test; en activación, +0,009 [−0,025; +0,042], −0,107 [−0,223; −0,011] y −0,001 [−0,065; +0,066]. Además, la red MLP con fusión tardía rinde 0,024 menos que el HGB con fusión temprana sobre la misma representación (0,686 frente a 0,710; [−0,038; −0,012]). La ventaja de la fusión tardía en atención vale para el MLP, y con HGB el signo fue el contrario: no puede concluirse que la fusión tardía sea mejor en general. La fusión no se volvió a evaluar el 22 ni el 23-11.

> Nota de trabajo (no va en la tesis): la comparación entre el MLP con fusión tardía y el HGB con fusión temprana es un recálculo de la auditoría final.

Fuentes: `resultados/ampliacion_41p_16-11-2026/INFORME.md`, `resultados/cierre_v3_16-11-2026/INFORME.md`, `documentacion/auditoria_final_23-11-2026/recalculo.json` (recálculo de la auditoría final).

### 7.7 Atención: aporte de cada señal

Análisis del 22-11 (enfoque E2, registrado). Etiqueta original, modelos sin historial.

| Prueba | Diferencia | A favor | Decisión |
|---|---|---|---|
| B1 Solo EEG − 0,5 | +0,181 [+0,164; +0,197] | 41/41 | Efecto relevante |
| B2 Solo GSR − 0,5 | +0,045 [+0,030; +0,062] | 36/41 | Efecto relevante |
| B3 (EEG + GSR) − solo EEG | +0,002 [−0,001; +0,005] | 24/41 | Nulo concluyente |
| B4 Solo EEG − solo GSR | +0,136 [+0,113; +0,158] | 40/41 | Efecto relevante |
| B5 Solo alfa y beta − 0,5 | +0,093 [+0,079; +0,106] | 40/41 | Efecto relevante |
| B6 Canales posteriores − 0,5 | +0,102 [+0,083; +0,121] | 38/41 | Efecto relevante |
| B7 (Potencia lenta y amplitud) − (alfa y beta) | +0,080 [+0,067; +0,092] | 40/41 | Efecto relevante |
| B8 Frontales − posteriores | +0,073 [+0,054; +0,092] | 38/41 | Efecto relevante |

La columna "A favor" cuenta las personas con diferencia positiva; en las pruebas contra 0,5 son las personas sobre el azar. En las pruebas contra 0,5 el rótulo "efecto relevante" solo indica que el límite inferior de la AUC supera 0,52; no califica la utilidad de esa señal (vale también para L3, sección 7.9, y para C1, sección 7.11). La GSR sola queda en 0,545 y no agrega nada al EEG (B3). Las pruebas B5 a B8 forman una segunda familia, agregada antes de correr. La detección descansa en el EEG. La GSR sola detecta la etiqueta (B2), pero sumada al EEG no agrega un efecto que supere el margen (B3, nulo concluyente). Que la GSR sola detecte una etiqueta ocular no se estudió; una lectura posible es que, estandarizada por sesión, informe del tramo de la sesión, del que la etiqueta depende (sección 7.2). Esto coincide con la importancia por permutación del 16-11 (descriptiva): la AUC cae 0,207 al permutar el EEG y 0,004 al permutar la GSR.

> Nota de trabajo (no va en la tesis): la segunda familia (B5 a B8) la agregó la auditoría de código antes de correr.

La tabla siguiente compara subconjuntos de variables del EEG. Sus dos últimas columnas adelantan el resultado de la limpieza ocular (sección 7.9).

| Variables de EEG | AUC original | AUC a igual posición | AUC sin 3 componentes oculares | Caída (original − sin componentes oculares) |
|---|---|---|---|---|
| Todo el EEG | 0,681 | 0,675 | 0,621 | 0,060 |
| Potencia lenta (delta, theta) y amplitud | 0,673 | 0,659 | 0,602 | 0,070 |
| Canales frontales | 0,675 | 0,667 | 0,621 | 0,054 |
| Canales posteriores | 0,602 | 0,600 | 0,562 | 0,040 |
| Solo alfa y beta | 0,593 | 0,593 | 0,547 | 0,045 |

Las variables que más detectan son las que suelen llevar la firma de los movimientos oculares en el EEG: potencia lenta, amplitud y electrodos frontales. Ese patrón es compatible con un origen ocular, pero no lo mide; la medición directa es la limpieza ocular (sección 7.9). La probabilidad del modelo de EEG se asocia sobre todo con el recorrido de la mirada (correlación de Spearman media por persona 0,41), luego con la dispersión (0,30) y la duración total de fijaciones (0,29); con la pupila, −0,09. Un control con etiquetas barajadas da 0,496 [0,482; 0,510].

El subconjunto "solo alfa y beta" contiene la potencia logarítmica absoluta de esas bandas en cada canal, no la relativa. En el modelo con todo el EEG entran además las potencias relativas, que dependen de la potencia lenta a través del denominador: también las variables de las bandas altas pueden llevar información del artefacto lento.

> Nota de trabajo (no va en la tesis): la composición del subconjunto se comprobó el 27-11 en `scripts/enfoques_41p.py` (`eeg_sets`: `logpower_alpha` y `logpower_beta`).

Fuentes: `resultados/enfoques_41p_22-11-2026/INFORME.md`, `resultados/ampliacion_41p_16-11-2026/INFORME.md`, `resultados/limpieza_ocular_41p_23-11-2026/INFORME.md`.

### 7.8 Montaje y sincronía entre equipos

Análisis del 23-11, descriptivo, sin etiquetas ni modelos. El procedimiento de sincronización está en la sección 4.6.1; aquí quedan sus resultados.

**Montaje.** El montaje de los electrodos no estaba documentado y la división entre canales frontales y posteriores del 22-11 era un supuesto. La respuesta promedio al parpadeo (amplitud pico a pico del promedio del EEG alrededor de los parpadeos, entre 1 y 15 Hz; mediana entre personas) es de 148 y 151 µV en los dos canales frontopolares (Fp1 y Fp2 según el montaje por defecto), 74 y 77 µV en los frontales laterales (F7 y F8), 57 y 56 µV en los frontales (F3 y F4), y de 18 a 29 µV en los centrales, temporales, parietales y occipitales. La mirada horizontal entra con signo opuesto en los dos canales frontales laterales en 31 de las 37 personas con ambos canales utilizables. El patrón es compatible con el montaje por defecto del equipo (OpenBCI Cyton+Daisy); esto es coherente con la división usada, pero no reemplaza la documentación del experimento. La definición de parpadeo que usa este análisis, que incluye pérdidas de seguimiento que no son parpadeos, y su conteo están en la sección 4.6.4; las 16 posiciones del montaje por defecto, en la sección 4.7.

**Sincronía.** El mismo análisis mostró que el EEG va entre 0,18 y 0,53 s atrasado respecto del reloj del seguidor ocular en las 41 personas (mediana 0,45 s; cuartiles 0,28 y 0,48 s). Las ventanas de 2 s del EEG están corridas entre un 9 % y un 26 % (mediana 22 %) respecto de las de mirada, pupila y GSR. El desfase no se corrigió, porque las ventanas vigentes están congeladas. Puede atenuar la relación entre el EEG y las demás señales, incluidas las etiquetas; ese efecto no se midió. El desfase se agrupa en dos valores (cerca de 0,28 s en P2 a P21, P36 y P37, y cerca de 0,48 s en el resto), lo que sugiere una causa sistemática de adquisición que no se investigó, y su estimación es poco segura en las personas con acoplamiento bajo. El EEG responde al parpadeo después de su marca en el seguidor ocular: cada ventana de EEG contiene actividad ligada a la conducta ocular de unas décimas de segundo antes de la ventana, y no posterior.

> Nota de trabajo (no va en la tesis): la dirección del desfase se comprobó en el script de montaje, por el signo con que se estimó (función `lagged_corr`).

Fuente: `resultados/montaje_ocular_41p_23-11-2026/INFORME.md`.

### 7.9 Atención: limpieza ocular del EEG

Análisis del 23-11, registrado. Modelos de atención solo con EEG, ventana actual, las mismas 5 particiones.

| Prueba | Contraste | Diferencia | A favor | Decisión |
|---|---|---|---|---|
| L1 | EEG original − EEG limpio | +0,060 [+0,044; +0,075] | 39/41 | Efecto relevante |
| L2 | EEG sin 3 componentes no oculares (control) − EEG limpio | +0,054 [+0,037; +0,070] | 37/41 | Efecto relevante |
| L3 | EEG limpio − 0,5 | +0,121 [+0,107; +0,135] | 41/41 | Efecto relevante |
| L4 | Alfa y beta limpio − alfa y beta original | −0,045 [−0,059; −0,032] | 6/41 | Inferior |

La columna "A favor" cuenta las personas con diferencia positiva. En L4 son las 6 personas en que la limpieza sube la AUC de alfa y beta.

Quitar tres componentes oculares, que representan una mediana de 3,5 % de la varianza, baja la AUC de 0,681 a 0,621. Quitar tres componentes no oculares, con una mediana de 72 % de la varianza, la deja en 0,674 (caída de 0,007 [−0,001; +0,015]). Esos tres componentes no se caracterizaron: que tres componentes de entre 11 y 16 concentren esa fracción de la varianza indica que la señal registrada está dominada por fuentes de gran amplitud cuya naturaleza no se estableció y cuya retirada casi no cambia la detección (sección 4.7). La caída es específica de los componentes elegidos por su relación con la mirada y los parpadeos, y no una consecuencia de quitar varianza. Como esos componentes se eligen con las mismas señales oculares que definen la etiqueta, quitarlos puede retirar también actividad cerebral acoplada a los movimientos de los ojos; el control, que no está igualado en esa relación, acota la objeción y no la elimina. La detección por alfa y beta, que el 22-11 parecía la parte menos expuesta al artefacto, también cae (de 0,593 a 0,547); la lectura fijada de antemano solo contemplaba que no cambiara.

La caída crece con el número de componentes quitados y se va frenando: 0,661 con uno, 0,638 con dos, 0,621 con tres y 0,613 con cuatro (el cuarto agrega 0,007 [−0,000; +0,015]). Un segundo método, la regresión sobre los cuatro canales frontales, coincide en el sentido pero limpia poco: descartar esos canales baja la AUC de 0,681 a 0,646 y la regresión resta otros 0,012 [−0,000; +0,024].

**Lectura.** Lo medido es que la caída equivale a cerca de un tercio de lo que el modelo tiene sobre el azar (0,060 de 0,181), y que el modelo limpio sigue sobre el azar en las 41 personas (0,621; L3). La lectura del resto enfrenta dos objeciones de sentido opuesto, que el diseño no separa.

La primera es que la limpieza es parcial. La correlación máxima entre algún canal y los parpadeos baja de 0,28 a 0,08 (mediana entre personas), sin anularse, y la probabilidad del modelo limpio sigue asociada al recorrido de la mirada (Spearman 0,28; antes 0,41). Los puntajes oculares son bajos: la mediana entre personas es 0,38 para el primer componente, 0,23 para el segundo, 0,17 para el tercero y 0,13 para el cuarto (en los del control, la mediana del puntaje más alto es 0,06), de modo que "ocular" designa aquí un orden y no una identificación segura. Además, el puntaje se calcula entre 1 y 15 Hz y con un seguidor ocular de 60 Hz: por construcción no identifica el potencial de espiga sacádica, que ocupa aproximadamente de 20 a 90 Hz (Keren, Yuval-Greenberg y Deouell, 2010). La limpieza no se dirigió a esa fuente. Tras la limpieza se mantiene además el mismo orden: canales frontales sobre posteriores (+0,059) y potencia lenta sobre alfa y beta (+0,055). Por eso no puede descartarse que el resto de la detección también dependa de los ojos; es una inferencia apoyada en el patrón espacial y espectral del remanente.

La segunda es la contraria: con 11 a 16 canales utilizables, tres componentes son entre el 19 % y el 27 % de las dimensiones y arrastran actividad frontal no ocular.

Con ambas a la vista, 0,060 se lee como cota inferior de la contribución ocular. Es la lectura más defendible y no una demostración. La detección que podría defenderse como no ocular baja de 0,59–0,60 (estimación del 22-11) a 0,55–0,56, sobre el azar en 38 de 41 personas.

> Nota de trabajo (no va en la tesis): el límite inferior de L1 es 0,044 (0,044497 en el CSV); el INFORME muestra +0,045 por un redondeo doble.

Fuente: `resultados/limpieza_ocular_41p_23-11-2026/INFORME.md`.

### 7.10 Atención: red convolucional sobre la señal cruda

Análisis del 23-11, registrado.

| Prueba | Contraste | Diferencia | A favor | p (Holm) | Decisión |
|---|---|---|---|---|---|
| R1 | Red − HGB, atención, EEG original | +0,035 [+0,023; +0,047] | 32/41 | < 0,0001 | Efecto relevante |
| R2 | Red − HGB, atención, EEG limpio | +0,028 [+0,013; +0,043] | 30/41 | 0,0017 | Respaldo |
| R3 | Red original − red limpia, atención | +0,067 [+0,053; +0,082] | 39/41 | < 0,0001 | Efecto relevante |
| R4 | Red − HGB, activación | −0,025 [−0,055; +0,003] | 15/41 | 0,0995 | Inconcluso |

| Modelo de atención | AUC |
|---|---|
| Red, EEG original | 0,716 [0,697; 0,735] |
| HGB, EEG original | 0,681 [0,664; 0,697] |
| Red, EEG limpio | 0,649 [0,630; 0,667] |
| HGB, EEG limpio | 0,621 [0,607; 0,635] |

En atención la red supera al modelo de referencia. La GRU y los MLP no lo habían logrado, pero usaban otras entradas, de modo que esa comparación no es directa. Su detección depende de lo ocular: al quitar los tres componentes oculares pierde 0,067 (R3, sin control propio), algo más que el HGB (0,060), y su probabilidad se asocia con el recorrido de la mirada más que la del HGB (Spearman 0,48 frente a 0,41; tras la limpieza, 0,33). Su ventaja sobre el HGB, en cambio, se mantiene con el EEG limpio: +0,028, frente a +0,035 con el original. La diferencia entre ambas ventajas, no registrada, es +0,007 [−0,005; +0,020]: no se demostró que la ventaja cambie al limpiar.

Cuatro límites acotan esta lectura. R1 es efecto relevante con holgura mínima: el límite inferior es 0,023 y, sin las dos personas más favorables, queda en torno a 0,020 (entre 0,0197 y 0,0202 según la semilla del remuestreo). R3 no tiene control propio: no se entrenó una red con el filtro de control, de modo que la especificidad ocular de su pérdida descansa en el control del modelo de referencia (L2). Es una sola arquitectura, sin búsqueda, con una inicialización por grupo y sin curva de convergencia. Y la red recibe la señal escalada por persona y canal con toda la sesión, mientras el modelo de referencia usa variables sin esa escala y con su configuración congelada: la ventaja no puede atribuirse a la arquitectura sin separar ese factor.

> Nota de trabajo (no va en la tesis): la diferencia entre las dos ventajas de la red la calculó la auditoría final.

Fuentes: `resultados/red_cruda_41p_23-11-2026/INFORME.md`, `resultados/limpieza_ocular_41p_23-11-2026/INFORME.md`, `documentacion/auditoria_final_23-11-2026/recalculo.json` (recálculo de la auditoría final).

### 7.11 Activación: ventana actual, estímulo y persona

**Ventana actual.** Ningún modelo de la ventana actual queda claramente sobre el azar (5 particiones):

| Modelo | AUC | Personas sobre 0,5 |
|---|---|---|
| HGB, solo EEG | 0,524 [0,497; 0,550] | 26/41 |
| HGB, EEG + mirada + pupila | 0,518 [0,491; 0,545] | 22/41 |
| Red convolucional, EEG crudo | 0,498 [0,478; 0,518] | 20/41 |

La comparación entre la red y el HGB (R4, sección 7.10) es inconclusa e inestable: el signo cambia en una de las cinco particiones y la decisión pasa a "inferior" al quitar a cualquiera de cinco personas concretas. Compara dos modelos sin señal demostrada. No se demostró que un modelo más complejo ayude en activación, ni tampoco que perjudique.

**Predicción por estímulo (22-11, enfoque E3, registrado).** La unidad es el segmento y el objetivo, la mayoría de las etiquetas de sus ventanas (1.589 segmentos).

| Prueba | Diferencia | A favor | p (Holm) | Decisión |
|---|---|---|---|---|
| C1 Modelo de estímulo − 0,5 | +0,087 [+0,050; +0,122] | 32/41 | 0,0001 | Efecto relevante |
| C2 Modelo de estímulo − promedio del modelo por ventana con historial | +0,020 [−0,007; +0,046] | 23/41 | 0,27 | Inconcluso |
| C3 (Estímulo + duración) − solo duración | +0,048 [−0,014; +0,109] | 25/41 | 0,27 | Inconcluso |

El modelo de estímulo llega a 0,587 [0,550; 0,622], la AUC más alta obtenida en activación. No se demuestra que supere a promediar el modelo por ventana con historial (0,567) ni que aporte sobre la duración del estímulo (0,535 [0,488; 0,583] por sí sola). Este modelo usa todas las ventanas del segmento, también las posteriores a cada etiqueta: no es causal.

**Diferencias entre personas (22-11, enfoque E4).** La detectabilidad de cada persona es estable entre dos mitades alternadas de su sesión: la correlación de Spearman de la AUC sin historial es 0,76 [0,58; 0,86] en atención y 0,66 [0,44; 0,80] en activación. La ganancia del historial de cada persona no es fiable (0,30 [−0,05; 0,61] y 0,25 [−0,04; 0,51]). Ninguna característica de la persona se asocia con la AUC ni con la ganancia tras Holm.

**Adaptación a la persona (22-11, enfoque E4, registrado).**

| Tarea | Contraste | Diferencia | Mejoran | p (Holm) | Decisión |
|---|---|---|---|---|---|
| Atención | Adaptado − general, sin historial | +0,006 [+0,000; +0,011] | 25/41 | 0,098 | Nulo concluyente |
| Atención | Adaptado − general, con historial | +0,000 [−0,007; +0,008] | 19/41 | 0,97 | Nulo concluyente |
| Activación | Adaptado − general, sin historial | +0,028 [+0,007; +0,049] | 29/40 | 0,049 | Respaldo |
| Activación | Adaptado − general, con historial | +0,045 [+0,023; +0,069] | 30/40 | 0,0004 | Efecto relevante |

En activación la adaptación se suma al historial: en la parte final de la sesión la AUC pasa de 0,502 (general, sin historial) a 0,587 (adaptado, con historial), y en el modelo adaptado el historial aporta +0,058 [+0,032; +0,084] (descriptivo que no figura en la lista registrada del protocolo). La decisión de la adaptación sin historial está pegada al umbral (p Holm 0,049). La adaptación es offline: las etiquetas de calibración se definen con la normalización de toda la sesión, por lo que no equivale a una calibración utilizable en línea. Como cada persona tiene cerca de la mitad de sus ventanas en cada clase, la proporción de clase alta en la parte de calibración condiciona la de la parte evaluada: las etiquetas de calibración informan sobre el resto de la sesión. Se evalúa sobre la parte final de la sesión, que es una muestra distinta de la de los demás análisis. En activación se evalúan 40 personas: una queda sin evaluación en esa parte. Allí el equilibrio entre clases no está asegurado por la mediana de la sesión, y no se fijó un mínimo de ventanas por clase.

> Nota de trabajo (no va en la tesis): el p de Holm de la adaptación sin historial es 0,0495 en el CSV, que el INFORME muestra como 0,050 por un redondeo doble. La definición de las etiquetas de calibración se comprobó el 27-11 en `scripts/enfoques_41p.py` (`calibration_split` separa por tiempo las filas ya etiquetadas con la mediana de toda la sesión; la AUC solo exige que la persona tenga las dos clases) y en el informe ("contienen información del resto de la sesión"; "n = 40").

Fuentes: `resultados/red_cruda_41p_23-11-2026/INFORME.md`, `resultados/enfoques_41p_22-11-2026/INFORME.md` (y `e4_confirmatorio.csv`), `resultados/reapertura_41p_22-11-2026/auc_absolutas.csv`.

### 7.12 Análisis descriptivos

Ninguno de estos patrones se sometió a contraste. Provienen del análisis del 16-11, con una partición.

- **Evolución en la sesión.** En atención, la AUC sube del primer al último quinto de la sesión: de 0,65 a 0,71 sin historial y de 0,69 a 0,74 con historial. En activación, la proporción de ventanas de clase alta cae a 0,37 en el último quinto, un patrón compatible con habituación, y también con una deriva lenta de la señal, con el orden de los estímulos o con el propio cálculo (nivel tónico estandarizado por sesión y filtrado en ambos sentidos). Se midió con la etiqueta binaria y no con el score continuo.
- **Importancia por bloques.** En atención, la caída de AUC al permutar cada señal está en la sección 7.7; además, la ventana actual pesa más que el historial, y las bandas theta y delta más que las restantes. En activación el descriptivo es ruidoso: la desviación entre los 8 grupos de la validación cruzada supera a la media en los tres bloques con caída (±0,075, ±0,053 y ±0,027). Las caídas son 0,053 para el EEG, 0,050 para la media del historial y 0,021 para la pupila, y no se observa caída para la mirada. No demuestra que el EEG aporte, y el EEG de la ventana actual no supera el azar de forma demostrable (0,524; sección 7.11).
- **Tipo de página.** La etiqueta de atención se predice mejor en sitios web (0,71) y peor en textos (0,60 sin historial y 0,63 con historial). Con historial, la única categoría con AUC menor es una que solo tiene 25 personas. En activación, el historial mejora sobre todo en sitios web (de 0,525 a 0,588).

> Nota de trabajo (no va en la tesis): las desviaciones entre grupos de la importancia por bloques son de la auditoría final.

> Nota de trabajo (no va en la tesis): la tercera lectura propone leer el peor desempeño en textos como coherente con la lectura ocular de la sección 8.3, porque en la lectura las sacadas serían pequeñas y regulares y dejarían una huella menor en el EEG. La fuente posible es Dimigen et al. (2011), pero esa afirmación no está entre las verificadas: requiere fuente antes de incluirse, y no se puso a prueba.

Fuentes: `resultados/ampliacion_41p_16-11-2026/INFORME.md` (y `por_categoria.csv`), `documentacion/auditoria_final_23-11-2026/recalculo.json` (recálculo de la auditoría final).

## Capítulo 8: Discusión

### 8.1 Respuesta a la hipótesis

La hipótesis central plantea que los modelos temporales multimodales rinden mejor fuera de muestra que los modelos estáticos comparables. Con el diseño de evaluación original (entrenamiento, validación y test por separado), el cierre V3 del 16-11 no encontró una ventaja consistente del modelo con historial en ninguna de las dos variables. El análisis con validación cruzada sobre las 41 personas se registró ese mismo día, después de conocer ese resultado, para ganar precisión. Con este segundo diseño y sus controles, y aplicando los criterios de interpretación de la sección 4.8.3, el resultado se lee como **evidencia mixta, con apoyo parcial**, que proviene de la activación. Esa lectura depende del cambio de diseño y no es el resultado del contraste planificado en un principio.

El paso del criterio a esa lectura debe quedar a la vista. El criterio escrito habla de apoyo parcial si la ventaja de los modelos temporales aparece en una sola de las dos variables. Leído al pie de la letra y con el segundo diseño, la ventaja de desempeño aparece en las dos (primera fila de la tabla siguiente); con el diseño original no aparecía de forma consistente en ninguna. Este borrador aplica una lectura más exigente, que pide además que la ventaja provenga de las ventanas previas; bajo ella atención no cuenta, y por eso el apoyo es parcial. Esa exigencia adicional no está en el criterio escrito. Cuál de las dos lecturas corresponde es parte de la decisión abierta sobre el encuadre (decisión 5).

Dos precisiones sobre cómo se operacionalizó la hipótesis. En el contraste principal, "modelo temporal" designa un modelo no secuencial (HGB) que recibe un resumen estadístico de las ventanas previas; el único modelo que usa el orden de las ventanas (GRU) no mostró una ventaja demostrable. Y "multimodal" describe las señales de entrada, no un aporte demostrado de combinarlas: en atención la GSR no agrega al EEG, y en activación no se demostró el aporte de ninguna señal por separado. El apoyo parcial se refiere, entonces, al historial reciente de las señales, no a una arquitectura temporal ni a la fusión.

| Pregunta | Atención | Activación |
|---|---|---|
| ¿Mejora el modelo con historial? | Sí: +0,029 [+0,021; +0,037], efecto relevante | Sí, con respaldo al promediar 5 particiones: +0,036 [+0,010; +0,065] (nota a) |
| ¿La mejora proviene de la fisiología de las ventanas previas? | No: con la posición como variable, +0,001 [−0,002; +0,005], nulo concluyente | Evidencia acotada. El contraste mejor sostenido: el historial sin las ventanas de 6 s que promedia la etiqueta supera a un placebo en +0,046 (p Holm 0,004; protocolo fijado antes de sus predicciones y después de ver el placebo del historial completo) (nota b) |
| ¿Queda algo al controlar la posición? | No: nulo concluyente dentro de ±0,02 | +0,032 [+0,004; +0,059], inconcluso tras Holm |
| ¿Aporta el orden de las ventanas? | No: la GRU con historial no supera a su control (+0,008 [−0,004; +0,020]) y rinde 0,040 menos que el HGB | No demostrado: el contraste propio del orden (GRU − HGB, ambos con historial) es inconcluso, +0,020 [−0,017; +0,057] (nota c) |

Notas de la columna de activación:

- **a.** Por partición la diferencia va de +0,028 a +0,047, y no todos los intervalos excluyen el cero. El efecto es desigual entre personas (mediana +0,014; 23 de 41) y está concentrado en las 25 personas con que se eligió la configuración (+0,046, frente a +0,021 en las otras 16; sección 7.5).
- **b.** Ese historial excluye las ventanas que promedia la etiqueta, pero queda dentro del soporte de su filtro tónico (sección 6.1). Su placebo proviene de otros estímulos, de modo que el contraste no separa la fisiología previa de pertenecer a la misma página, y es un refinamiento dirigido de un resultado ya visto (secciones 6.6 y 8.4). En la curva, el contraste es +0,047 [+0,017; +0,078] a 6 s; a 12 s es inconcluso y desde 24 s no se distingue del placebo, sin que eso demuestre ausencia. Los controles de tiempo de sesión, posición y mismo estímulo quedaron inconclusos.
- **c.** La GRU con historial supera a su control de una ventana (+0,051 [+0,021; +0,080], secundario sin corrección), lo que mide el historial y no el orden.

Este encuadre es provisorio (decisión 5, abierta). Lo que hay en activación es evidencia acotada, no una confirmación: ningún análisis se hizo en personas nuevas (sección 6.5).

### 8.2 Atención: una ventaja que no proviene de la fisiología de las ventanas previas

El modelo con historial rinde mejor en atención, de forma estable y en casi todas las personas. Esa ventaja no proviene de la fisiología de las ventanas previas, sino del tiempo transcurrido en el estímulo. La reproduce un historial placebo de otros estímulos, la reproduce un solo número (los segundos transcurridos en el estímulo) y queda dentro de ±0,02 cuando el modelo conoce ese número, tanto en el análisis post hoc del 18-11 como en el contraste registrado de la fase 3. En ese contraste lo que agrega el historial es +0,001 [−0,002; +0,005]: quedaría dentro de cualquier margen de 0,005 o más, de modo que este resultado no depende del margen elegido. Las ventanas de 6 a 96 s antes no aportan más que un placebo de la misma persona. Lo que el resultado descarta es un aporte del contenido fisiológico de las ventanas previas, no que el modelo use contexto temporal: la posición es tiempo transcurrido.

La lectura más coherente es que el *Attention Score* tiene una estructura sistemática al inicio de cada página: una caída a los 2–3 s seguida de un aumento. El modelo con historial la capturaba a través del largo del historial. La etiqueta depende mucho del reloj: la posición sola predice con AUC 0,598. Dado que la etiqueta se construye con fijaciones y mirada, este patrón podría reflejar la reorientación de la mirada al cambiar de página, es decir, lo **Observado** más que lo **Atendido**.

Hay cuatro explicaciones más que no se separaron. La primera es de cálculo: la duración de cada fijación se suma completa aunque exceda la ventana (la suma supera los 2.000 ms en cerca del 28 % de las ventanas etiquetadas), y las ventanas no cruzan el cambio de estímulo, lo que por sí solo acorta las duraciones al inicio de cada página. La segunda es de composición: las posiciones tardías solo existen en los estímulos largos, de modo que la prevalencia por posición mezcla el tiempo transcurrido con el tipo de estímulo, y los tipos son muy distintos entre sí (sección 6.3). Las otras dos dependen de información del protocolo que no consta. La tercera es la espera: si al inicio de cada estímulo hay un tiempo de carga o una pantalla en blanco, la mirada del primer segundo, más quieta que la de los dos siguientes (prevalencia 0,51 frente a 0,37–0,38; sección 7.2), puede ser espera. La cuarta es el desplazamiento de la página: no consta si los sitios web lo permitían, y no se examinó cómo clasifica el filtro de fijaciones un contenido que se mueve. La exportación trae la posición del área visible del navegador y la del mouse, que permitirían comprobarlo; no se usaron.

> Nota de trabajo (no va en la tesis): la tercera lectura agrega dos explicaciones que requieren fuente antes de incluirse, porque ninguna de las 18 referencias verificadas las sostiene: que las primeras fijaciones sobre una imagen nueva son más breves y las sacadas más amplias, lo que daría la caída de los segundos 2 y 3 sin apelar a la atención; y que, si la página se desplaza, la mirada sigue al contenido y un filtro de velocidad pensado para fijaciones y sacadas clasifica ese seguimiento de forma inconsistente.

La etiqueta corregida por posición elimina ese efecto y la detección baja poco (0,675 frente a 0,683), aunque la decisión registrada de ese contraste fue "inferior", por −0,008 y al filo (sección 7.2). Es un resultado útil para decidir cómo definir la etiqueta, pero la decisión de reemplazar la original corresponde al profesor guía (decisión 4). La corrección no resuelve el problema de fondo de la sección siguiente, porque la etiqueta corregida también se define con los ojos.

El modelo secuencial (GRU) no agregó información sobre el resumen estadístico y rindió peor. Con 41 personas y estímulos breves (mediana de tres ventanas por segmento), la información disponible para aprender dependencias de orden es limitada.

### 8.3 Atención: qué detecta el EEG

El *Modelo Estudiante* detecta el *Attention Score* desde el EEG en las 41 personas (AUC 0,681 solo con EEG; 0,675 a igual posición; el control con etiquetas barajadas da 0,496; con EEG y GSR, la detección es la misma al comparar solo ventanas de un mismo estímulo, sección 7.2), y sigue haciéndolo tras retirar los componentes oculares (0,621, también en las 41). La detección de la etiqueta definida es el resultado más estable de estos análisis, dentro de las 41 personas evaluadas y con los límites de la sección 8.8. Lo que estos datos no permiten establecer es su origen, y de eso trata esta sección.

> Nota de trabajo (no va en la tesis): esta sección y la 8.5 integran el texto de [[Borrador Discusión fisiológica 23-11-2026]]. Las referencias se verificaron en un catálogo bibliográfico (OpenAlex: título, autores, revista y DOI), y el 23-11-2026 se contrastaron con las fuentes: 10 en texto completo (tres de ellas en preprint o manuscrito de autor; lectura por búsqueda dirigida de los pasajes) y 8 solo por resumen (Barry 2005 y 2007, Boucsein 2012, Critchley 2002, Croft y Barry 2000, Iwasaki 2005, Keren 2010 y Yuval-Greenberg 2008). Las frases se ajustaron a lo verificado; el detalle está en `repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/VERIFICACION_REFERENCIAS.md`.

#### 8.3.1 La huella de los ojos en el EEG

El *Attention Score* se construye con variables de mirada y pupila, aunque en la práctica es conducta de mirada (sección 6.1), y el *Modelo Estudiante* lo predice principalmente desde el EEG (sección 7.7). La regla de no-circularidad se cumple en el nivel de las señales de entrada, pero no garantiza que el EEG sea independiente de los ojos. El ojo se comporta como un dipolo eléctrico, con la córnea positiva respecto de la retina, de modo que cada rotación del globo ocular modifica el potencial que registran los electrodos cercanos (Croft y Barry, 2000; Plöchl, Ossandón y König, 2012). Los parpadeos agregan una deflexión de gran amplitud y máximo frontopolar (Iwasaki et al., 2005), atribuida principalmente al deslizamiento del párpado sobre la córnea (Plöchl, Ossandón y König, 2012). A estas dos fuentes se suma el potencial de espiga sacádica, una descarga breve y de banda ancha al inicio de cada sacada, atribuida a los músculos extraoculares, que contamina las frecuencias altas del EEG (Yuval-Greenberg et al., 2008; Keren, Yuval-Greenberg y Deouell, 2010; Hipp y Siegel, 2013).

Los registros de esta tesis muestran ese patrón. La respuesta promedio al parpadeo alcanza unos 150 µV en los dos canales frontopolares y decrece hasta unos 20 µV en los posteriores, y la mirada horizontal entra con signo opuesto en los canales frontales laterales en 31 de las 37 personas con ambos canales utilizables (sección 7.8). Este gradiente es además compatible con el montaje por defecto del equipo, que no estaba documentado.

#### 8.3.2 Cuánto de la detección depende de los componentes oculares

Al retirar del EEG de cada persona los tres componentes independientes más asociados a la mirada y a los parpadeos, la AUC de atención baja de 0,681 a 0,621 (diferencia 0,060; intervalo de confianza de 95 % [0,044; 0,075]; 39 de 41 personas), y un control que retira mucha más varianza casi no la cambia. La caída equivale a cerca de un tercio de los 0,181 que el modelo tiene sobre el azar. Es específica de los componentes elegidos por su relación con la mirada y los parpadeos, con la objeción que el control acota y no elimina (sección 7.9).

La detección basada en las bandas alfa y beta, que antes de la limpieza parecía la parte menos expuesta al artefacto, también disminuye. Este resultado es coherente con la literatura. El dipolo córneo-retinal se concentra en frecuencias bajas (Plöchl, Ossandón y König, 2012). El potencial de espiga sacádica, en cambio, abarca aproximadamente de 20 a 90 Hz y alcanza la parte alta de beta (Keren, Yuval-Greenberg y Deouell, 2010). Además, la actividad de los músculos frontal y temporal puede ocultar o imitar los ritmos beta y alfa (Goncharova et al., 2003). El subconjunto de alfa y beta usa la potencia logarítmica absoluta de cada canal, no la relativa (sección 7.7), de modo que su caída no es un efecto aritmético de la potencia lenta. Para la caída en alfa quedan tres lecturas que el diseño no separa. El aumento de potencia ligado al dipolo córneo-retinal aparece en frecuencias bajo 10 Hz (Plöchl, Ossandón y König, 2012), que incluyen la parte baja de alfa. Los parpadeos y los escalones de las sacadas son transitorios de gran amplitud (unos 150 µV en los canales frontopolares; sección 7.8) y, en una ventana de 2 s filtrada por separado, pueden dejar potencia fuera de su banda principal; ese efecto de borde no se evaluó (sección 4.7). Y los tres componentes retirados pueden arrastrar actividad no ocular en esas bandas.

La cifra de 0,060 se lee como cota inferior de la contribución ocular, con las reservas de la sección 7.9: es la lectura más defendible y no una demostración. La separación por componentes independientes, propuesta para este fin por Jung et al. (2000), es imperfecta en condiciones de exploración visual libre cuando se aplica con la configuración habitual: puede dejar artefacto residual o retirar actividad cerebral, según el filtrado y los datos con que se ajusta (Dimigen, 2020). Además, el método separa a lo sumo tantas fuentes como canales (Jung et al., 2000), por lo que con 16 canales la separación es gruesa, y en estos datos la limpieza fue parcial.

#### 8.3.3 Qué puede explicar la detección que permanece

Tras la limpieza, el modelo sigue por sobre el azar (0,621 con todas las variables, en las 41 personas; 0,55–0,56 con alfa y beta o con canales posteriores). El diseño no permite atribuir ese remanente a una sola fuente. Las explicaciones candidatas son al menos seis: cinco fisiológicas (1 a 5) y una que no lo es (6).

1. **Artefacto ocular residual.** El remanente conserva el patrón espacial y espectral del artefacto: los canales frontales superan a los posteriores y la potencia lenta supera a alfa y beta. A ello se suma el potencial de espiga sacádica, al que la limpieza no se dirigió (sección 7.9).
2. **Actividad muscular** de la frente y las sienes, que contamina el EEG en un rango amplio de frecuencias (Goncharova et al., 2003) y que podría acompañar a los movimientos de los ojos; esta asociación no se midió.
3. **Respuesta visual ligada a cada fijación.** Después de cada sacada aparece en la corteza occipital una respuesta a la nueva imagen, conocida como respuesta lambda (Dimigen et al., 2011). Es actividad cerebral, pero su ocurrencia está determinada por los movimientos de los ojos.
4. **Modulación de alfa posterior.** La potencia alfa se relaciona con la atención y con la inhibición de regiones no relevantes para la tarea (Klimesch, 2012). Es el candidato más cercano a un correlato cerebral de la atención y, a la vez, el más débil en estos datos. Presupone además que el registro contiene alfa medible, lo que no se comprobó (sección 4.7).
5. **Parpadeos.** Es una vía que no pasa por el movimiento de los ojos. Un parpadeo interrumpe el registro de la mirada y, por lo tanto, las fijaciones con que se calcula el *Attention Score* (sección 4.6.4), y a la vez produce en el EEG la deflexión de mayor amplitud medida aquí (sección 7.8). No se midió cuánto de la etiqueta depende de la pérdida de mirada dentro de la ventana ni cuánto de la detección depende de los parpadeos.
6. **Variables de calidad de canal** que la limpieza no altera. Es la posibilidad que agrega el informe de limpieza, y no es fisiológica.

Como la etiqueta se define con la conducta ocular, las fuentes 1 a 4 covarían con ella y no pueden separarse.

En términos del diseño, cerca de un tercio de lo que el *Modelo Estudiante* de atención recupera desde el EEG depende de componentes oculares, es decir, de lo **Observado**. No puede descartarse que el resto también lo sea: es una inferencia apoyada en el patrón espacial y espectral del remanente, que el diseño no separa. Estos datos no permiten afirmar que el modelo detecte lo **Atendido** ni que exista un marcador cerebral de atención. De forma provisoria, el resultado se presenta como una detección que depende, en cerca de un tercio, de la huella de la conducta ocular en el EEG, sin atribuir el resto a un origen cerebral ni ocular (decisión 5, abierta).

#### 8.3.4 Un modelo más complejo detecta mejor y también depende de lo ocular

Una red convolucional compacta del tipo EEGNet (Lawhern et al., 2018), que aprende directamente de la serie temporal del EEG sin variables calculadas a mano, supera al modelo con variables calculadas: 0,716 frente a 0,681 (diferencia 0,035; intervalo de confianza de 95 % [0,023; 0,047]; 32 de 41 personas). Sin embargo, al retirar los componentes oculares la red cae a 0,649, una pérdida algo mayor que la del modelo de referencia (0,067 frente a 0,060), y su probabilidad se asocia con el recorrido de la mirada más que la del modelo de referencia (sección 7.10). La detección de la red depende, entonces, de lo ocular. Su ventaja sobre el modelo de referencia, en cambio, se mantiene con el EEG limpio (+0,028, frente a +0,035 con el original), y no se demostró que cambie al limpiar: los datos no permiten decir que esa ventaja sea ocular.

Una explicación plausible de esa dependencia, que este trabajo no puso a prueba, es que los artefactos oculares tienen formas de onda características —el escalón de una sacada, la onda de un parpadeo— que las variables de potencia por banda promedian y que una red convolucional puede aprender. Otra, igual de plausible y tampoco puesta a prueba, es la escala por persona y canal que recibe la red y no el modelo de referencia. Una tercera es espacial: tras una convolución temporal, el primer bloque de la red aprende filtros espaciales, es decir, combinaciones ponderadas de los canales (Lawhern et al., 2018), y puede formar por sí sola derivaciones como la diferencia entre los dos canales frontales laterales, donde la mirada horizontal entra con signo opuesto (sección 7.8), mientras que las variables del modelo de referencia se calculan canal por canal y pierden el signo. Tampoco se puso a prueba. La mayor capacidad del modelo no cambia la interpretación de qué se detecta.

Esta lectura tiene los cuatro límites de la sección 7.10. Los dos que más la condicionan son que la ventaja supera el margen de relevancia de 0,02 por poco, y que no se entrenó una red con el filtro de control, por lo que la especificidad ocular de su pérdida descansa en el control del modelo de referencia.

Fuentes: `resultados/montaje_ocular_41p_23-11-2026/INFORME.md`, `resultados/limpieza_ocular_41p_23-11-2026/INFORME.md`, `resultados/red_cruda_41p_23-11-2026/INFORME.md`.

### 8.4 Activación: el historial del mismo estímulo supera a un placebo de otros estímulos

En la predicción del *Arousal Score* el modelo con historial rinde mejor, y hay evidencia acotada de que esa mejora no se explica solo por la persona. Lo que el historial aportaría es, con mayor probabilidad, una mejor estimación de un estado que dura segundos: la propia etiqueta se parece a la de 6 s antes. Los resultados no demuestran más que eso: por los controles inconclusos (límite 5, más abajo), corresponde hablar de un resumen del historial reciente y no de dinámica dentro del estímulo. Los dos contrastes que sostienen esa evidencia no tienen la misma solidez.

**Qué se observó.**

- *Historial desplazado frente al placebo.* Es el contraste mejor sostenido: el historial sin las ventanas de 6 s que promedia la etiqueta supera a un placebo en +0,046 (p Holm 0,004; sección 7.3). Es positivo tanto en las 25 personas con que se eligió la configuración como en las otras 16 (+0,035 y +0,064), igual que el contraste de la GRU (+0,045 y +0,059); la comparación por grupo es descriptiva y no registrada (sección 7.5).
- *Contraste principal, historial menos sin historial.* Es más frágil. Se estimó varias veces sobre las mismas 41 personas, con diferencias de AUC entre +0,028 y +0,047, y no todos los intervalos excluyen el cero. El efecto es desigual entre personas (mediana +0,014; mejoran 23 de 41) (sección 7.1).
- *Alcance temporal.* Solo la banda de 6 s tiene respaldo; a 12 s el resultado es inconcluso y desde 24 s el contraste no se distingue del placebo, sin que eso demuestre ausencia (sección 7.3).
- *Estímulo completo.* El resultado por estímulo y la persistencia de la etiqueta son compatibles con que la activación, tal como la define el *Arousal Score*, se comporte como un estado del estímulo completo más que de cada ventana; es una lectura sin contraste propio (la comparación entre el modelo de estímulo y el promedio del modelo por ventana es inconclusa; sección 7.11).
- *Tamaño.* El efecto es pequeño y su utilidad práctica es baja con las variables actuales: las AUC absolutas van de 0,50 a 0,59.

**Qué lo limita.** En orden de importancia:

1. *Ninguno de los dos contrastes es una confirmación.* El respaldo de la fase 1 del 22-11 para el contraste principal sale de un análisis registrado sobre personas ya consultadas, que promedia cinco particiones nuevas cuando el mismo contraste ya se había visto positivo en otras tres particiones el 16-11: es una estimación más precisa de lo ya observado, no una confirmación. El protocolo del historial desplazado se fijó antes de obtener sus predicciones, pero después de conocer, ese mismo día y en las mismas personas y la misma partición, que el historial completo superaba al placebo (+0,038; secciones 6.6 y 7.3). Es un refinamiento dirigido de un resultado ya visto, con un historial que comparte ventanas con aquel, y no una segunda evidencia independiente.
2. *La configuración se eligió con parte de las personas evaluadas.* El contraste principal tampoco es estable entre subconjuntos de personas, y esa inestabilidad se cruza con la forma en que se eligió la configuración (sección 7.5): las 15 hojas de activación las decidió el modelo con historial, con las 25 personas de entrenamiento, y es en esas 25 donde se concentra el contraste principal (+0,055, frente a +0,001 en las otras 16; con cinco particiones, +0,046 frente a +0,021). El sesgo que eso permite es posible y no está demostrado: la diferencia entre grupos no es significativa con 16 personas, y con las particiones originales del cierre V3 el patrón había sido el inverso. Estas comparaciones son descriptivas y no registradas, pero impiden tratar el efecto como una propiedad establecida de la muestra y debilitan el "respaldo" del contraste principal.
3. *El soporte de la etiqueta.* El historial desplazado excluye las ventanas que promedia la etiqueta, pero no el soporte del filtro tónico de la GSR: cerca de un cuarto del peso de la componente dominante de la etiqueta cae antes de esas ventanas (sección 6.1). Deja abierta la lectura 1.
4. *El placebo.* El historial real pertenece al mismo estímulo que la ventana evaluada y el placebo no (sección 6.2). El contraste del historial desplazado frente al placebo no se calculó dentro de un mismo estímulo. Deja abierta la lectura 2.
5. *Los controles quedan inconclusos:* el tiempo de sesión como variable, el contraste con la posición como variable tras la corrección de Holm, ese mismo contraste dentro de un mismo estímulo y la comparación a igual posición. Dentro de un mismo estímulo la comparación entre el historial y el tiempo transcurrido es inconclusa y de poca potencia: no permite afirmar que el historial aporte ni que su aporte se reduzca al tiempo transcurrido.
6. *No hay control de artefactos ni análisis del movimiento.* La etiqueta no tiene control de artefactos sobre la señal cruda y el movimiento no se analizó: los archivos del equipo de EEG traen tres canales de acelerómetro y la exportación del seguidor ocular, la posición del mouse, pero ninguno se usó ni se comprobó su contenido (sección 4.6.1). Deja abierta la lectura 5.

**Qué lecturas alternativas no se separaron.**

1. *Una relación entre señales del mismo momento.* Por el límite 3, el contraste del historial desplazado no separa por sí solo "la fisiología previa predice la activación posterior" de "la fisiología de un momento se relaciona con la GSR de ese mismo momento, que la etiqueta posterior todavía contiene".
2. *Identificar la página.* Las entradas de activación incluyen mirada y pupila, que dependen de lo que muestra la página, y la etiqueta cambia poco dentro de un estímulo: en el 79 % de los segmentos todas las ventanas tienen la misma etiqueta. Un resumen de las ventanas de la misma página podría identificar la página o el tramo de la sesión mejor que una sola ventana, sin que intervenga la fisiología de los segundos previos. Los controles que aislarían esa lectura no la descartan: dentro de un mismo estímulo el tiempo transcurrido aporta por sí solo y no se demostró que el historial lo supere (sección 7.3).
3. *Una respuesta al cambio de estímulo.* Es una lectura propia de la señal. Cada cambio de estímulo es un evento, y una respuesta de conductancia se atribuye a un evento cuando comienza típicamente entre 1 y 3 s o entre 1 y 5 s después de él, y decae lentamente (Benedek y Kaernbach, 2010). Si el cambio de página provoca una respuesta, la GSR sigue dentro de cada estímulo un curso ligado a su inicio, y las ventanas etiquetadas, que empiezan a los 6 s, caen sobre ese curso. Eso bastaría para que el tiempo transcurrido prediga la etiqueta dentro de un mismo estímulo (+0,049; sección 7.3) y para que un resumen de las ventanas previas, que informa de cuánto lleva la persona en la página, también lo haga. No se examinó la GSR alineada al inicio de los estímulos.
4. *Una deriva lenta de la sesión.* Que la ganancia se mantenga dentro del mismo minuto (análisis post hoc) habla contra una deriva lenta de la sesión como única explicación; el control registrado del tiempo de sesión quedó inconcluso y, además, solo corrige la tendencia común a las personas: una deriva lenta con dirección distinta en cada persona queda fuera de ese control (sección 7.1).
5. *Una explicación no neural.* Los resultados tampoco la descartan: un movimiento o una respiración profunda pueden producir a la vez una respuesta en la GSR y artefactos de varios segundos en el EEG, la mirada y la pupila (límite 6).

> Nota de trabajo (no va en la tesis): la tercera lectura agrega que derivas lentas no neurales (temperatura de la sala, hidratación del contacto de la GSR, contacto de los electrodos del EEG, pupila que cambia con el tiempo en la tarea) pueden ser comunes a la etiqueta y a las entradas. Ninguna de las 18 referencias verificadas lo sostiene: requiere fuente antes de incluirse.

### 8.5 Activación: por qué el Arousal Score no se detecta desde la ventana actual

Con la ventana actual, ningún modelo queda claramente por sobre el azar en activación, y no se demostró aporte del EEG de la ventana actual (sección 7.11). Hay cuatro explicaciones que el diseño no separa. Dos son anteriores a la fisiología. La primera es de la etiqueta: el *Arousal Score* por ventana puede reflejar poco la activación, porque no se validó contra ninguna medida externa y no tiene control de artefactos sobre la señal cruda. La segunda es de la entrada: la calidad del EEG como registro de actividad cerebral no está establecida (sección 4.7), de modo que el resultado no permite distinguir entre "el EEG no informa sobre el *Arousal Score*" y "este registro no lo permite". Las otras dos vienen de la fisiología de la respuesta electrodérmica y se desarrollan abajo, después de una precisión sobre el origen de la señal: la escala temporal y el tipo de relación.

**Origen de la señal.** La conductancia de la piel refleja la actividad de las glándulas sudoríparas, inervadas exclusivamente por el sistema nervioso simpático (Benedek y Kaernbach, 2010). Su regulación central depende de regiones cerebrales implicadas en la emoción, la atención y la cognición, identificadas con estudios de lesiones y de neuroimagen (Critchley, 2002). De ello no se sigue que el EEG de superficie no pueda reflejar ese estado: los trabajos citados más abajo relacionan el nivel de conductancia con la potencia alfa (Barry et al., 2005, 2007).

> Nota de trabajo (no va en la tesis): hasta el 27-11-2026 este párrafo proponía que esas regiones, por ser mediales o profundas, contribuirían poco a un EEG de superficie. Se suprimió tras la tercera lectura: no tiene fuente y contradice el párrafo "Tipo de relación". Requiere fuente antes de incluirse: Critchley (2002) solo se leyó por resumen, que no nombra estructuras, y mientras no se lea el texto completo se cita solo para lo que ese resumen sostiene.

**Escala temporal.** Una respuesta de conductancia se atribuye a un evento cuando comienza en una ventana que típicamente va de 1 a 3 s o de 1 a 5 s después de él; sube con rapidez y decae lentamente, de modo que las respuestas sucesivas se superponen (Benedek y Kaernbach, 2010). Esa latencia describe las respuestas individuales. Como componente fásica pesan poco en la etiqueta usada, pero no están ausentes de ella: al superponerse, su acumulación entra en la componente lenta. El *Arousal Score* es, en lo esencial, esa componente (sección 6.1), que se obtiene con un filtro pasa-bajos de 0,05 Hz aplicado hacia atrás y hacia adelante y cambia en decenas de segundos. La diferencia de escalas que importa es entonces otra: una ventana de EEG de 2 s frente a un nivel lento y relativo a la sesión. Es coherente con el resultado temporal de activación, con las reservas de la sección 8.4.

**Tipo de relación.** La relación entre el EEG y la conductancia de la piel que documentan estos trabajos es tónica: en reposo, un mayor nivel de conductancia acompaña a una menor potencia alfa global (Barry et al., 2005, 2007). Esa relación se observó al comparar condiciones (cafeína frente a placebo, ojos abiertos frente a cerrados), y no implica que el estado de activación pueda distinguirse ventana a ventana dentro de una misma sesión. Además, el *Arousal Score* es relativo a la mediana de cada persona, y es plausible que una sesión de estímulos en pantalla como esta produzca un rango de activación estrecho; este trabajo no lo midió.

En cuanto a la pupila, su diámetro responde a la luz, al enfoque cercano y a la activación o el esfuerzo mental (Mathôt, 2018). Frente a una pantalla cuyo brillo cambia con el contenido, las dos primeras respuestas pueden dominar sobre la tercera, lo que ayudaría a explicar que no se haya demostrado aporte de la pupila a la detección de la activación en la ventana actual.

Estas explicaciones son compatibles con los resultados, pero el diseño no las pone a prueba. El resultado de la red convolucional es específico de una arquitectura y una configuración, sin búsqueda de hiperparámetros ni registro de convergencia; no permite concluir que el EEG crudo carezca de información sobre la activación.

**Adaptación a la persona.** Un resultado de activación con decisión de efecto relevante en un contraste registrado es la adaptación a la persona: agregar al entrenamiento las ventanas etiquetadas del inicio de su sesión mejora al modelo general con historial en +0,045 [+0,023; +0,069] (30 de 40 personas; p Holm 0,0004), y la detectabilidad de cada persona es estable entre dos mitades alternadas de su sesión (correlación de Spearman 0,66 [0,44; 0,80] en activación; sección 7.11). Los dos resultados son compatibles con que parte de la relación entre las señales y el *Arousal Score* sea propia de cada persona, lo que un modelo general no puede aprovechar; ningún contraste pone a prueba esa lectura, y ninguna característica de la persona se asoció con la AUC tras Holm. Sus límites son dos: la adaptación es offline, porque las etiquetas de calibración se definen con la normalización de toda la sesión y por eso informan sobre la parte evaluada (sección 7.11), y se evalúa sobre la parte final de la sesión, que es una muestra distinta de la de los demás análisis. No es comparable con los demás contrastes. Aun con adaptación e historial, la AUC es 0,587.

Fuentes: `resultados/red_cruda_41p_23-11-2026/INFORME.md`, `resultados/enfoques_41p_22-11-2026/`.

### 8.6 Fusión y complejidad del modelo

Entre redes MLP, la fusión tardía rindió mejor que la temprana en atención, en un contraste secundario sin corrección; con HGB y las particiones originales el signo fue el contrario, y la red MLP con fusión tardía rinde menos que el HGB con fusión temprana (sección 7.6). Una explicación posible de la ventaja entre redes, que no se puso a prueba, es que entrenar un modelo por señal y combinar sus salidas evite que el EEG, con muchas más variables, domine el ajuste conjunto. En atención la GSR no agrega al EEG un efecto que supere el margen, de modo que hay poco que fusionar. En activación ninguna estrategia se distinguió. No puede concluirse que la fusión tardía sea mejor en general, y ningún contraste establece qué papel tiene la fusión en el desempeño.

Dos modelos más complejos dieron resultados opuestos. La GRU, que usa el orden de las ventanas, no mejoró la atención y rindió peor que el resumen. La red convolucional sobre la señal cruda sí mejoró la atención; su detección depende de lo ocular, pero su ventaja sobre el HGB se mantiene con el EEG limpio (secciones 7.10 y 8.3.4). En activación no se demostró que un modelo más complejo ayude: la comparación entre la red y el HGB es inconclusa (sección 7.11).

### 8.7 Implicancias para el diseño

- **La no-circularidad entre señales no asegura independencia fisiológica.** El EEG contiene una copia eléctrica de la conducta ocular con que se construye el *Attention Score*.
- **Para separar lo Observado de lo Atendido** se requiere una etiqueta de atención que no dependa de los ojos (por ejemplo, desempeño en una tarea) o un diseño que mantenga la conducta ocular constante entre condiciones.
- **Para la activación**, la etiqueta usada ya es en lo esencial el nivel tónico; su escala temporal sugiere predecirla con ventanas más largas que 2 s y definirla con un filtro causal.

### 8.8 Limitaciones

Las limitaciones se agrupan en cinco familias. Cada una se enuncia aquí una vez y remite a la sección donde están sus cifras. Cinco limitaciones condicionan directamente las conclusiones del capítulo 9: ningún resultado se obtuvo en personas nuevas; el diseño con 41 personas se adoptó después de un resultado nulo; la configuración de activación la decidió el modelo con historial, con 25 de las 41 personas evaluadas; la etiqueta de activación tiene un soporte temporal mayor que el nominal; y la etiqueta de atención se define con la conducta ocular, que el EEG también registra.

**Muestra y diseño de evaluación**

- Las 41 personas incluyen las de validación y test, consultadas en etapas anteriores. Los análisis posteriores al 16-11 son exploratorios o dirigidos; ninguno es una confirmación independiente en personas nuevas (sección 6.5).
- El diseño de evaluación cambió después de un resultado nulo: con las particiones originales el cierre V3 no mostró una ventaja consistente, y el análisis con 41 personas se registró a continuación (secciones 6.3 y 8.1).
- **Selección de la configuración.** Las 15 hojas de activación las decidió el modelo con historial, con 25 de las 41 personas evaluadas, y los contrastes del HGB con historial hasta 32 se concentran en ellas. El sesgo a favor del historial es posible y no está demostrado; el historial desplazado frente al placebo y la GRU son positivos en ambos grupos (sección 7.5).
- Las personas de un mismo grupo experimental vieron los estímulos en el mismo orden (sección 4.3). La validación cruzada separa personas, no grupos: un modelo puede aprender regularidades ligadas a la secuencia de páginas a partir de otras personas del mismo grupo. No se evaluó dejando grupos completos fuera, y el bootstrap trata a las personas como independientes.
- La ampliación con el historial desplazado se registró después de ver que el historial completo superaba al placebo, en las mismas personas y la misma partición: es un análisis dirigido y su resultado no es una evidencia independiente de aquel (sección 6.6).
- El placebo iguala la persona y el largo del historial, pero no el estímulo ni la cercanía en la sesión: el contraste entre el historial real y el placebo no separa la fisiología previa de pertenecer a la misma página (secciones 6.2 y 8.4).
- Los intervalos son percentiles de un *bootstrap* de personas, que no recoge la dependencia entre las AUC de una validación cruzada ni la variación por conjunto de entrenamiento (sección 6.4).
- El control del tiempo de sesión solo corrige la tendencia común a las personas (sección 7.1).
- Los contrastes secundarios no llevan corrección por multiplicidad. La corrección de Holm se aplica dentro de cada etapa y no entre etapas: son doce etapas de análisis sobre las mismas 41 personas (sección 6.6).
- Ocho filas cumplen dos reglas de decisión a la vez y su rótulo depende de una precedencia que los protocolos no fijan (sección 6.4).
- El control de posición del 18-11 y la fase 2 son post hoc; la comprobación estratificada con la posición no fue registrada ni pasó por la revisión de código. En la curva temporal y en la fase 2 las reglas de decisión se usan como lectura descriptiva (sección 7.2).
- Varias decisiones están pegadas al umbral: A1 y A3 de la etiqueta corregida (sección 7.2), la adaptación de activación sin historial (sección 7.11) y la ventaja de la red sobre el modelo de referencia (R1, sección 7.10).

**Etiquetas**

- Las etiquetas son pseudoetiquetas offline, normalizadas con la sesión completa de cada persona, y no se validaron contra una medida externa. La normalización por sesión difiere de la redacción actual del manuscrito, que pide normalizar solo con entrenamiento (decisión 6). También varias variables de entrada (GSR y pupila normalizadas por sesión; componente tónica con filtro bidireccional) usan información de toda la sesión: el historial es causal por ventana, no por muestra.
- La etiqueta de atención usada (componente principal) se siguió usando tras observar que los modelos la predecían mejor que la de pesos iguales; los análisis no se repitieron con esta última (sección 6.1).
- La etiqueta de atención es, en la práctica, conducta de mirada, y su soporte no es de 2 s: las variables de fijación suman la duración completa de las fijaciones que tocan la ventana (sección 6.1). En activación esas dos variables son entradas y arrastran mirada posterior a la ventana.
- No está establecido que una mirada más quieta corresponda a más atención y no a menos (sección 6.1).
- Los parpadeos pueden entrar en la etiqueta de atención por la pérdida de mirada, y no se midió cuánto (secciones 4.6.4 y 8.3.3).
- La etiqueta de activación es en lo esencial la componente lenta de la GSR relativa a la sesión, que aquí se llama nivel tónico e incluye la acumulación de las respuestas; el conteo de SCR no se validó (sección 4.6.3). Su soporte real excede los 6 s nominales hacia el pasado y hacia el futuro: el contraste "sin las ventanas de la etiqueta" no excluye ese soporte (secciones 6.1 y 7.3).
- Los resultados de activación se refieren al 53 % de las ventanas que conserva la etiqueta: desde la quinta ventana de cada estímulo (6 s transcurridos), en estímulos suficientemente largos. No describen el inicio de cada página ni los estímulos breves.
- Menos de un tercio de las ventanas con etiqueta de atención corresponde a sitios web; el resto son textos, diseños, estímulos numerados e imágenes, cuyo contenido no está documentado. Los resultados describen la sesión completa de estímulos y no solo la navegación web; por tipo de estímulo solo hay un descriptivo (secciones 6.3 y 7.12).

**Señales y procesamiento**

- No constan la referencia, el tipo de electrodo ni las impedancias del EEG; no se rechazaron ventanas por amplitud ni se examinó el espectro de la señal. La calidad del EEG como registro de actividad cerebral no está establecida, y los resultados sobre el EEG, incluido el de activación, valen para este registro (secciones 4.7 y 5.3).
- El movimiento no se analizó: el acelerómetro del equipo de EEG y la posición del mouse están en los archivos y no se usaron (secciones 4.6.1 y 8.4).
- El desfase de reloj entre el EEG y el seguidor ocular no se corrigió y su efecto no se midió (secciones 7.8 y 4.6.1).
- El procesamiento congelado tiene dos imprecisiones conocidas que no se corrigieron: la fracción de muestras con ambos ojos válidos, que es una entrada del *Modelo Estudiante* de activación, se calcula sobre todas las filas de la exportación y queda bajo la validez real; y los eventos oculares se deduplican solo por índice, con lo que se pierde cerca del 0,2 % de las fijaciones (medido en una muestra de 11 personas). Están descritas en las secciones 4.6.4 y 4.6.5.
- La limpieza ocular es parcial, usa la sesión completa de cada persona y elige los componentes con la mirada; su calidad se mide en los mismos datos. Como la mirada también define la etiqueta, el experimento mide dependencia de componentes ligados a la mirada, no de artefacto. Los tres componentes retirados arrastran actividad frontal no ocular, sus puntajes oculares son bajos y la limpieza no se dirigió al potencial de espiga sacádica (sección 7.9).

**Modelos**

- La GRU y los MLP no tuvieron búsqueda de hiperparámetros. La GRU se entrenó con tres hilos y sin forzar algoritmos deterministas: el fold 0 se reproduce exacto en el equipo usado, lo que no está garantizado en otro. La red convolucional es una sola arquitectura sin búsqueda, y su pérdida al limpiar no tiene control propio (sección 7.10).
- El modelo por estímulo no es causal y la adaptación a la persona no es utilizable en línea: sus etiquetas de calibración informan sobre la parte evaluada (sección 7.11).
- Los modelos de historial desplazado reciben una columna no declarada con el número de ventanas (sección 6.2).

**Tamaño del efecto, potencia e interpretación**

- En activación las AUC absolutas son bajas (0,50 a 0,59; sección 8.4).
- La AUC por persona pesa igual a todas las personas y no se fijó un mínimo de ventanas: P4, la más influyente del contraste principal de activación, conserva 26 ventanas con etiqueta (sección 7.1).
- Las AUC estratificadas dentro de un mismo estímulo usan el 2–3 % de los pares y tienen poca potencia en activación: un resultado inconcluso no demuestra ausencia de efecto (sección 7.3).
- Las explicaciones fisiológicas de las secciones 8.3 y 8.5 son compatibles con los resultados, pero el diseño no las pone a prueba.

> Nota de trabajo (no va en la tesis): el detalle de las dos imprecisiones del procesamiento está en `documentacion/auditoria_final_23-11-2026/ronda2/AUDITORIA_SECCIONES_PENDIENTES.md`. La comprobación de reproducibilidad del cierre verifica hashes y el orden del registro; no vuelve a entrenar los modelos. La comprobación estratificada con la posición no fue auditada.

### 8.9 Trabajo futuro

- Confirmar el efecto temporal en activación con personas nuevas y un contraste definido de antemano.
- Definir una etiqueta de atención que no dependa de la conducta ocular, o registrar electrooculograma y más canales para separar mejor la actividad cerebral de la ocular.
- Corregir el desfase entre el EEG y el seguidor ocular y analizar el EEG alineado a las fijaciones.
- Evaluar etiquetas y normalizaciones calculadas solo con información previa, para una versión utilizable en línea.
- Entrenar una red con el filtro de control, para dar a la pérdida de la red un control propio, y un modelo de referencia con variables escaladas por persona, para separar la arquitectura de la escala.
- Evaluar dejando grupos experimentales completos fuera, fijar un mínimo de ventanas por persona y usar un indicador de movimiento (el acelerómetro del equipo de EEG, cuyo contenido falta comprobar, o un registro dedicado) para descartar artefactos compartidos entre la GSR y las demás señales.
- Describir la evolución en la sesión con el score continuo y sus intervalos, como compromete el objetivo 6.

> Nota de trabajo (no va en la tesis): el cálculo de tamaño de muestra para la cohorte nueva está en `resultados/protocolo_hipotesis_reintento_06-11-2026/`. La experimentación está cerrada desde el 23-11-2026: reabrirla requiere una decisión explícita y un protocolo registrado antes de correr.

### 8.10 Decisiones abiertas

> Nota de trabajo (no va en la tesis): esta sección no es una sección de la tesis. Se mantiene visible en el borrador hasta que las decisiones se resuelvan.

No hay aprobación registrada del profesor guía sobre los puntos siguientes. Este borrador los usa de forma provisoria y debe revisarse si alguno cambia. La numeración es la de [[Avance - 23-11-2026 (Minuta de decisiones con el profesor)]].

1. **Si se planifica una cohorte nueva** para confirmar el efecto de activación, o se escribe con las personas ya registradas.
2. **Si el margen práctico de 0,02 queda como criterio.** De él dependen las etiquetas "efecto relevante" y "nulo concluyente". Con otro margen cambiarían, entre otras, la decisión del contraste principal de atención (límite inferior 0,021) y la de la red (límite inferior 0,023).
3. **Si "emociones" se presenta como activación (*arousal*).** La GSR solo mide activación simpática, por lo que el texto habla de activación; la redefinición aún no está confirmada.
4. **Si la etiqueta de atención es la original o la corregida por posición.** La corregida existe hoy como análisis; las etiquetas congeladas son la de atención binaria original y las pseudoetiquetas GSR V2.
5. **El encuadre.** Apoyo parcial a la hipótesis, con la detección de atención por EEG presentada como dependiente, en cerca de un tercio, de la huella ocular, sin atribuir el resto a un origen cerebral ni ocular. Incluye con qué lectura del criterio de la hipótesis se llega a "apoyo parcial" (sección 8.1).
6. **Si se aceptan las etiquetas normalizadas con la sesión completa de cada persona** (el manuscrito pide normalizar solo con entrenamiento).
7. **Si el *Modelo Profesor* con PCA queda como definición del *Attention Score*** (la nota de diseño proponía la fusión igualitaria como principal).

Ninguna de las siete está tomada. Las dos últimas son las de mayor consecuencia si no se aceptan, porque obligan a repetir análisis.

Fuentes del capítulo: `documentacion/Cierre_Experimental_Final_23-11-2026.md`; `documentos/01 Tesis MDS/Escritura/Borrador Discusión fisiológica 23-11-2026.md` (texto de origen de las secciones 8.3 y 8.5, conservado como registro); los `INFORME.md` citados en el Capítulo 7.

## Capítulo 9: Conclusiones

Ver [[Borrador Conclusiones 23-11-2026]].

## Referencias

- Barry, R. J., Rushby, J. A., Wallace, M. J., et al. (2005). Caffeine effects on resting-state arousal. *Clinical Neurophysiology*. https://doi.org/10.1016/j.clinph.2005.08.008
- Barry, R. J., Clarke, A. R., Johnstone, S. J., et al. (2007). EEG differences between eyes-closed and eyes-open resting conditions. *Clinical Neurophysiology*. https://doi.org/10.1016/j.clinph.2007.07.028
- Benedek, M., y Kaernbach, C. (2010). A continuous measure of phasic electrodermal activity. *Journal of Neuroscience Methods*. https://doi.org/10.1016/j.jneumeth.2010.04.028
- Boucsein, W., Fowles, D. C., Grimnes, S., Ben-Shakhar, G., Roth, W. T., Dawson, M. E., y Filion, D. L. (2012). Publication recommendations for electrodermal measurements. *Psychophysiology*. https://doi.org/10.1111/j.1469-8986.2012.01384.x (no citada en el texto; pendiente de lectura)
- Critchley, H. D. (2002). Electrodermal responses: what happens in the brain. *The Neuroscientist*. https://doi.org/10.1177/107385840200800209
- Croft, R. J., y Barry, R. J. (2000). Removal of ocular artifact from the EEG: a review. *Neurophysiologie Clinique*. https://doi.org/10.1016/s0987-7053(00)00055-1
- Dimigen, O. (2020). Optimizing the ICA-based removal of ocular EEG artifacts from free viewing experiments. *NeuroImage*. https://doi.org/10.1016/j.neuroimage.2019.116117
- Dimigen, O., Sommer, W., Hohlfeld, A., et al. (2011). Coregistration of eye movements and EEG in natural reading: analyses and review. *Journal of Experimental Psychology: General*. https://doi.org/10.1037/a0023885
- Goncharova, I. I., McFarland, D. J., Vaughan, T. M., et al. (2003). EMG contamination of EEG: spectral and topographical characteristics. *Clinical Neurophysiology*. https://doi.org/10.1016/s1388-2457(03)00093-2
- Hipp, J. F., y Siegel, M. (2013). Dissociating neuronal gamma-band activity from cranial and ocular muscle activity in EEG. *Frontiers in Human Neuroscience*. https://doi.org/10.3389/fnhum.2013.00338
- Iwasaki, M., Kellinghaus, C., Alexopoulos, A. V., et al. (2005). Effects of eyelid closure, blinks, and eye movements on the electroencephalogram. *Clinical Neurophysiology*. https://doi.org/10.1016/j.clinph.2004.11.001
- Jung, T.-P., Makeig, S., Humphries, C., et al. (2000). Removing electroencephalographic artifacts by blind source separation. *Psychophysiology*. https://doi.org/10.1111/1469-8986.3720163
- Keren, A. S., Yuval-Greenberg, S., y Deouell, L. Y. (2010). Saccadic spike potentials in gamma-band EEG: characterization, detection and suppression. *NeuroImage*. https://doi.org/10.1016/j.neuroimage.2009.10.057
- Klimesch, W. (2012). Alpha-band oscillations, attention, and controlled access to stored information. *Trends in Cognitive Sciences*. https://doi.org/10.1016/j.tics.2012.10.007
- Lawhern, V. J., Solon, A. J., Waytowich, N. R., et al. (2018). EEGNet: a compact convolutional neural network for EEG-based brain–computer interfaces. *Journal of Neural Engineering*. https://doi.org/10.1088/1741-2552/aace8c
- Mathôt, S. (2018). Pupillometry: psychology, physiology, and function. *Journal of Cognition*. https://doi.org/10.5334/joc.18
- Plöchl, M., Ossandón, J. P., y König, P. (2012). Combining EEG and eye tracking: identification, characterization, and correction of eye movement artifacts in electroencephalographic data. *Frontiers in Human Neuroscience*. https://doi.org/10.3389/fnhum.2012.00278
- Yuval-Greenberg, S., Tomer, O., Keren, A. S., et al. (2008). Transient induced gamma-band response in EEG as a manifestation of miniature saccades. *Neuron*. https://doi.org/10.1016/j.neuron.2008.03.027

> Nota de trabajo (no va en la tesis): faltan volumen, número y páginas en la lista de referencias. Años confirmados en Crossref el 23-11-2026: Iwasaki et al. 2005, Keren et al. 2010 y Dimigen 2020 corresponden al volumen impreso.

## Anexo de trazabilidad

Tabla completa de etapas y estatus (era la sección 6.4 hasta el 26-11-2026; la versión corta está en la sección 6.6).

| Etapa | Fecha | Estatus | Carpeta en `resultados/` |
|---|---|---|---|
| Cierre V3 (tercera versión del cierre experimental): elección y congelación de la configuración | 16-11 | Registrado; exploratorio | `cierre_v3_16-11-2026` |
| Análisis final con 41 personas | 16-11 | Registrado; contraste principal fijado de antemano | `cierre_final_41p_16-11-2026` |
| Robustez (placebo, sin fuga, particiones) | 16-11 | Registrado después de ver el contraste principal de ese día: dirigido | `cierre_robustez_41p_16-11-2026` |
| Ampliación E1–E6 y enmienda del historial desplazado | 16 al 18-11 | Registrado después de ver el placebo del análisis de robustez: dirigido; E1 principal, E2–E3 secundarios, E4–E6 descriptivos | `ampliacion_41p_16-11-2026` |
| Explicativo de posición | 18-11 | Registrado, pero motivado por resultados vistos: post hoc | `explicativo_posicion_41p_18-11-2026` |
| Reapertura, fase 1: 5 particiones y curva temporal | 22-11 | Registrado; familia fijada antes de correr (P1, P2) y curva secundaria. Se hizo sobre personas ya consultadas y con el contraste de activación ya visto en tres particiones alternativas el 16-11 (las cinco particiones del 22-11 son nuevas y no comparten ningún grupo con aquellas): no es una confirmación independiente | `reapertura_41p_22-11-2026` |
| Reapertura, fase 2: placebo de bloque y AUC estratificada | 22-11 | Post hoc, registrado sin resultados a la vista | `reapertura_fase2_41p_22-11-2026` |
| Comprobación estratificada con la posición | 22-11 | No registrada, hecha después de ver resultados | `reapertura_fase2_41p_22-11-2026` |
| Reapertura, fase 3: historial frente a posición | 22-11 | Registrado; dirigido | `reapertura_fase3_41p_22-11-2026` |
| Cuatro enfoques E1–E4 | 22-11 | Registrado; dirigido | `enfoques_41p_22-11-2026` |
| Montaje y sincronía | 23-11 | Descriptivo, sin etiquetas ni modelos | `montaje_ocular_41p_23-11-2026` |
| Limpieza ocular | 23-11 | Registrado; dirigido | `limpieza_ocular_41p_23-11-2026` |
| Red convolucional sobre la señal cruda | 23-11 | Registrado; dirigido | `red_cruda_41p_23-11-2026` |

La tabla tiene trece filas porque lista aparte la comprobación estratificada con la posición, que no fue registrada y pertenece a la fase 2; las etapas son doce. Los commits de registro, enmienda y resultados de cada etapa están en `documentacion/Cierre_Experimental_Final_23-11-2026.md`. La comprobación de reproducibilidad del cierre verifica hashes y el orden del registro; no vuelve a entrenar los modelos. Las cifras de los informes que difieren de las del texto por un redondeo doble están anotadas en las notas de trabajo de las secciones 7.2, 7.3, 7.9 y 7.11.

Fuente: `documentacion/Cierre_Experimental_Final_23-11-2026.md` (tabla de trazabilidad con los commits de registro, enmienda y resultados).

## Notas relacionadas
- [[Borrador Resultados y Discusión 18-11-2026]]
- [[Borrador Discusión fisiológica 23-11-2026]]
- [[Borrador Conclusiones 23-11-2026]]
- [[Estructura Tesis]]
- [[Problema e hipótesis]]
- [[Resumen Diseño Etiquetas y Modelos]]
