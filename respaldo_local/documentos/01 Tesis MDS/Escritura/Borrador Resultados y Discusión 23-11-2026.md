# Borrador: Modelamiento, Resultados y Discusión

> [!info] Estado
> Borrador redactado el 23-11-2026 a partir de los informes de resultados del repositorio (rutas al final de cada sección). Reemplaza como versión vigente a [[Borrador Resultados y Discusión 18-11-2026]], que se conserva. Integra los análisis del 22 y 23-11-2026 y resume [[Borrador Discusión fisiológica 23-11-2026]]. No reemplaza a [[Estructura Tesis]] ni cierra decisiones abiertas de [[Resumen Diseño Etiquetas y Modelos]]. **No hay aprobación registrada del profesor guía** sobre estos resultados ni sobre su encuadre. Las cifras son AUC (área bajo la curva ROC) por persona, con intervalo de confianza de 95 % entre corchetes, salvo que se indique otra cosa. Revisar redacción, citas y numeración antes de pasar a LaTeX. Redacción ajustada el 23-11-2026 a la auditoría final de resultados (`repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/AUDITORIA_EXPERIMENTO.md`).

> [!warning] Decisiones abiertas que este texto no cierra
> El texto usa de forma provisoria: (1) "emociones" presentada como activación (*arousal*); (2) el margen práctico de 0,02 en las reglas de decisión; (3) la etiqueta de atención original como etiqueta principal, con la corregida por posición informada como análisis; (4) el encuadre de apoyo parcial; (5) la cohorte nueva como trabajo futuro; (6) las etiquetas normalizadas con la sesión completa de cada persona, declaradas como límite; (7) el profesor PCA como definición del *Attention Score*. Las siete dependen del profesor guía (sección 8.10).

## Capítulo 6: Modelamiento y Experimento

### 6.1 Variables objetivo

Se usan dos pseudoetiquetas binarias por ventana de 2 s (paso de 1 s), construidas por un **Modelo Profesor** y predichas por un **Modelo Estudiante** con señales distintas, de acuerdo con la regla de no-circularidad. Aquí *Modelo Profesor* designa una regla fija de etiquetado (un promedio estandarizado o una componente principal), no un modelo entrenado cuyo conocimiento se transfiere: no es destilación de conocimiento.

- **Atención.** El *Attention Score* se obtiene como la primera componente principal de cinco variables de mirada y pupila (tiempo y duración de fijaciones, dispersión y recorrido de la mirada, pupila normalizada), ajustada con las 25 personas de entrenamiento. Las notas de diseño proponían la fusión con pesos iguales como definición principal y la componente principal como análisis de sensibilidad. Los análisis siguieron con la componente principal después de observar, en entrenamiento, que los modelos la predecían mejor. Una etiqueta más predecible no es por eso más válida, y ese criterio puede favorecer a la versión más ligada a los movimientos oculares que el EEG registra. Las dos versiones coinciden en 66 % de las ventanas (kappa 0,33); cuál define el *Attention Score* es una decisión abierta, y los resultados de atención de este capítulo valen solo para la versión usada. Cada ventana se clasifica como alta si supera la mediana de su persona. El *Modelo Estudiante* usa electroencefalograma (EEG) y respuesta galvánica de la piel (GSR). Aunque el *Modelo Profesor* recibe mirada y pupila, en la práctica la etiqueta es conducta de mirada: en la componente pesan el recorrido de la mirada (0,557), la dispersión (0,520), la duración media de las fijaciones (0,508) y su tiempo total (0,398), y la pupila casi no pesa y entra con signo contrario (−0,052). La componente explica el 51,5 % de la varianza de las cinco variables. Dos de esas variables suman la duración completa de las fijaciones que tocan la ventana, de modo que el soporte temporal de la etiqueta excede los 2 s (sección 8.2).
- **Activación.** El *Arousal Score* se calcula a partir de cuatro componentes de GSR promediados sobre cinco ventanas consecutivas válidas (6 s). La versión utilizada (GSR V2, la segunda versión de estas etiquetas) corrige un error de alineación de índices de la versión anterior, exige cobertura de al menos 50 % y deja sin etiqueta los empates con la mediana personal. Conserva 11.796 de 22.211 ventanas. El *Modelo Estudiante* usa EEG, mirada y pupila. En la práctica el *Arousal Score* es, en lo esencial, el nivel tónico de la GSR relativo a la sesión: dentro de cada persona, el nivel tónico de la ventana ordena la etiqueta con AUC 0,911, frente a 0,595 de la componente fásica y 0,522 del número y de la prominencia de las respuestas (comprobación de la auditoría de código del 26-11). Su soporte temporal real excede los 6 s nominales (sección 7.3).

Ambas etiquetas son relativas a la sesión de cada persona y se calculan offline; describen el *Attention Score* y el *Arousal Score* definidos, no una medida externa de atención o activación. En el caso de atención, la etiqueta se apoya en lo **Observado** (mirada y pupila) como aproximación a lo **Atendido**, sin validarlo.

El 22-11 se construyó además una **etiqueta de atención corregida por posición**: en lugar de la mediana de la persona en toda la sesión, usa la mediana de la persona dentro del mismo tramo de posición en el estímulo (1, 2, 3, 4, 5, 6–8, 9–12, 13–20 y 21–32 s). Coincide con la original en el 90,6 % de las ventanas (kappa de Cohen por persona 0,81). Existe como análisis (sección 7.2); si reemplaza a la original es una decisión abierta.

Fuentes: `resultados/profesor_binario_reconstruido_29-10-2026/INFORME.md`, `resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md`, `resultados/enfoques_41p_22-11-2026/INFORME.md`.

### 6.2 Representaciones y modelos

**Ventana actual e historial.** Para cada ventana se compara un modelo que recibe solo la ventana actual con el mismo modelo que recibe además un resumen del historial: media y desviación de las variables en las ventanas previas del mismo estímulo, hasta 32 ventanas. El historial se reinicia al cambiar de estímulo o ante huecos, y se construye con todas las ventanas válidas, tengan o no etiqueta. Como los estímulos son cortos, el historial efectivo promedia 7,8 ventanas en atención y 12,6 en activación. El resumen incluye la ventana actual y, por su largo, codifica la posición de la ventana dentro del estímulo.

**Familias de modelos.** Se usan dos familias: *HistGradientBoosting* (HGB, árboles con potenciación del gradiente sobre histogramas), con el número de hojas elegido en validación interna de entrenamiento (7 en atención y 15 en activación), y una red recurrente GRU (*Gated Recurrent Unit*) que recibe la secuencia ordenada, con configuración fija. Las tres estrategias de fusión (temprana, intermedia y tardía) se comparan con una misma familia, un perceptrón multicapa (MLP).

**Controles del origen de la mejora.** Para separar la información temporal de otros efectos se usan:

- un *historial placebo*: el mismo número de ventanas de la misma persona, tomadas de otros momentos;
- la *posición en el estímulo*: los segundos transcurridos desde el inicio del segmento, como única variable adicional;
- un *historial desplazado*, que excluye las ventanas más recientes para no coincidir con las ventanas de 6 s que promedia el *Arousal Score* (el filtro tónico de la GSR tiene un soporte más largo; sección 7.3). Estos modelos reciben además una columna con el número de ventanas desplazadas, que codifica la posición en el estímulo y que el informe de origen no declara; es igual en el historial real y en el placebo, pero entra en el contraste "desplazado menos sin historial";
- una *curva temporal* (22-11): la ventana actual más la media y la desviación de las ventanas cuyo inicio cae entre L y L+6 s antes, con L de 6, 12, 24, 48 y 96 s, sin importar el estímulo, frente a un placebo de la misma persona a 150 s o más;
- la *AUC estratificada*: la AUC (área bajo la curva ROC, o característica operativa del receptor) de cada persona calculada solo con pares de ventanas del mismo estímulo, del mismo minuto de sesión o de la misma posición.

**Análisis del EEG (22 y 23-11).** Para estudiar qué detecta el *Modelo Estudiante* de atención se entrenaron modelos sin historial con subconjuntos de variables (solo EEG, solo GSR, bandas alfa y beta, potencia lenta y amplitud, canales frontales y posteriores). El EEG original no tiene limpieza de artefactos oculares: solo se le quita la tendencia lineal y se aplican un filtro de red y un pasabanda de 1 a 45 Hz. La limpieza ocular se hizo por persona con análisis de componentes independientes (ICA): cada componente recibe un puntaje ocular (su correlación máxima con la mirada horizontal, la mirada vertical o los parpadeos del seguidor ocular) y se quitan los tres de mayor puntaje. Como control se quitan los tres componentes de mayor varianza entre los no oculares. Por último, se entrenó una red convolucional compacta del tipo EEGNet (1.217 parámetros) sobre la señal de 16 canales y 2 s, filtrada como en la extracción de variables y sin variables calculadas a mano (en adelante, "señal cruda"), con una sola arquitectura y configuración fijadas de antemano, sin búsqueda.

**Otros modelos (22-11).** Un modelo de activación por estímulo, que usa la media y la desviación de las señales en todas las ventanas del segmento, y un modelo adaptado a la persona, que agrega al entrenamiento las ventanas etiquetadas del primer 40 % de la sesión de la persona evaluada.

Fuentes: `resultados/cierre_v3_16-11-2026/INFORME.md`, `resultados/reapertura_41p_22-11-2026/INFORME.md`, `resultados/enfoques_41p_22-11-2026/INFORME.md`, `resultados/limpieza_ocular_41p_23-11-2026/INFORME.md`, `resultados/red_cruda_41p_23-11-2026/INFORME.md`.

### 6.3 Diseño de evaluación

La configuración se eligió solo con las 25 personas de entrenamiento y luego se congeló. El número de hojas se eligió por la AUC media, en validación interna, de los modelos con 1, 8 y 32 ventanas de contexto; el criterio incluye, por lo tanto, al modelo con historial. Para estimar los efectos con más precisión se usó validación cruzada agrupada por persona sobre las 41 personas del análisis principal (8 grupos), de modo que ninguna persona aparece a la vez en ajuste y evaluación. Este diseño se adoptó el 16-11, después de ver los resultados del cierre V3 con las particiones originales (entrenamiento, validación y test por separado), que no mostraron una ventaja consistente del modelo con historial en ninguna de las dos variables. Es un cambio de diseño posterior a los datos y todo lo que sigue debe leerse así. El análisis del 16-11 usó una partición. Desde el 22-11 la validación cruzada se repite en 5 particiones nuevas y la AUC de cada persona se promedia sobre las cinco.

La unidad de análisis es la persona: se calcula la AUC de cada persona y se comparan modelos con la diferencia pareada dentro de cada persona. La incertidumbre se estima con bootstrap por persona (20.000 réplicas) y una prueba de permutación de signos; los contrastes de cada familia se corrigen por Holm.

Las reglas de decisión se registraron antes de correr, con un margen práctico de 0,02 de AUC:

| Decisión | Condición |
|---|---|
| Respaldo | p de Holm < 0,05 y límite inferior del intervalo de 95 % sobre cero |
| Efecto relevante | además, límite inferior del intervalo de 95 % sobre 0,02 |
| Nulo concluyente | intervalo de 90 % dentro de (−0,02; +0,02) |
| Inferior | límite superior del intervalo de 95 % bajo cero; no exige Holm y tiene precedencia sobre "nulo concluyente" |
| Inconcluso | cualquier otro caso |

El margen de 0,02 no está aprobado por el profesor guía. Varias decisiones dependen de él y quedan cerca del umbral; se indican en cada caso. Que "respaldo" exija Holm e "inferior" no es una asimetría de la regla registrada que no tiene una justificación escrita. El código aplica las reglas con la precedencia respaldo, inferior, nulo concluyente; los protocolos las listan sin fijarla. Ocho filas cumplen dos reglas a la vez, todas en atención y todas con el intervalo de 90 % dentro de ±0,02: seis quedan como "inferior" (las bandas de 24, 48 y 96 s de la curva temporal, las de 48 y 96 s frente al placebo de bloque, y A1 de la etiqueta corregida) y dos como "respaldo" (la AUC estratificada dentro del mismo estímulo y A2). Con la precedencia inversa, las seis "inferior" serían "nulo concluyente".

El protocolo de cada etapa con modelos entró al repositorio antes que sus predicciones (orden de commits verificado) y cada etapa se ejecutó una sola vez, salvo la primera versión del cierre V3, que se detuvo por una revisión de código. No hay un registro externo con sello de tiempo: esto ordena el trabajo, pero no equivale a un prerregistro. Los análisis no registrados (la heterogeneidad por grupo del 16-11, las sensibilidades a personas individuales, la comprobación estratificada del 22-11 y el aporte del historial en el modelo adaptado de la sección 7.7) se rotulan como tales donde aparecen. Las revisiones de código detectaron problemas antes de evaluar (por ejemplo, indicadores de faltantes ausentes en la fusión tardía y 1 s de solapamiento entre el historial desplazado y la etiqueta de activación), que se corrigieron con enmiendas registradas antes de ver resultados. Desde el 22-11, cada etapa con modelos tuvo además una revisión adicional del código antes de ver resultados y un recálculo de los resultados con código separado, ambos hechos con un asistente automático a pedido del autor; no son revisiones de un tercero, y es a ellos a los que este texto llama "auditoría". La comprobación no registrada de la fase 2 no pasó por esa revisión.

**Alcance de la evidencia.** La configuración se eligió con 25 de las 41 personas que luego se evalúan, y en activación la elección de 15 hojas la decidió el modelo con historial (sección 7.1): eso permite un sesgo a favor del historial en esas 25 personas, que no está demostrado. Las 16 personas de validación y test habían sido consultadas en etapas anteriores, y los análisis del 22 y 23-11 se pidieron después de ver los resultados del 16 al 18-11. "Confirmatorio" designa aquí la familia de contrastes fijada antes de correr dentro de un análisis dirigido; no designa una confirmación independiente. Ningún resultado de este capítulo se obtuvo en personas nuevas.

Fuentes: `resultados/cierre_v3_16-11-2026/`, `resultados/cierre_final_41p_16-11-2026/protocolo.json`, `resultados/reapertura_41p_22-11-2026/protocolo.json`, `documentacion/Cierre_Experimental_Final_23-11-2026.md`.

### 6.4 Etapas del análisis y su estatus

| Etapa | Fecha | Estatus | Carpeta en `resultados/` |
|---|---|---|---|
| Cierre V3 (tercera versión del cierre experimental): elección y congelación de la configuración | 16-11 | Registrado; exploratorio | `cierre_v3_16-11-2026` |
| Análisis final con 41 personas | 16-11 | Registrado; contraste principal fijado de antemano | `cierre_final_41p_16-11-2026` |
| Robustez (placebo, sin fuga, particiones) | 16-11 | Registrado | `cierre_robustez_41p_16-11-2026` |
| Ampliación E1–E6 y enmienda del historial desplazado | 16 al 18-11 | Registrado; E1 principal, E2–E3 secundarios, E4–E6 descriptivos | `ampliacion_41p_16-11-2026` |
| Explicativo de posición | 18-11 | Registrado, pero motivado por resultados vistos: post hoc | `explicativo_posicion_41p_18-11-2026` |
| Reapertura, fase 1: 5 particiones y curva temporal | 22-11 | Registrado; familia fijada antes de correr (P1, P2) y curva secundaria. Se hizo sobre personas ya consultadas y con el contraste de activación ya visto en tres particiones alternativas el 16-11 (las cinco particiones del 22-11 son nuevas y no comparten ningún grupo con aquellas): no es una confirmación independiente | `reapertura_41p_22-11-2026` |
| Reapertura, fase 2: placebo de bloque y AUC estratificada | 22-11 | Post hoc, registrado sin resultados a la vista | `reapertura_fase2_41p_22-11-2026` |
| Comprobación estratificada con la posición | 22-11 | No registrada, hecha después de ver resultados | `reapertura_fase2_41p_22-11-2026` |
| Reapertura, fase 3: historial frente a posición | 22-11 | Registrado; dirigido | `reapertura_fase3_41p_22-11-2026` |
| Cuatro enfoques E1–E4 | 22-11 | Registrado; dirigido | `enfoques_41p_22-11-2026` |
| Montaje y sincronía | 23-11 | Descriptivo, sin etiquetas ni modelos | `montaje_ocular_41p_23-11-2026` |
| Limpieza ocular | 23-11 | Registrado; dirigido | `limpieza_ocular_41p_23-11-2026` |
| Red convolucional sobre la señal cruda | 23-11 | Registrado; dirigido | `red_cruda_41p_23-11-2026` |

Los enfoques E1–E4 del 22-11 no deben confundirse con los experimentos E1–E6 de la ampliación del 16-11; en este texto se identifican siempre por su fecha o por su contenido.

Fuente: `documentacion/Cierre_Experimental_Final_23-11-2026.md` (tabla de trazabilidad con los commits de registro, enmienda y resultados).

## Capítulo 7: Resultados

### 7.1 Efecto del historial

Contraste: HGB con hasta 32 ventanas de historial menos HGB con la ventana actual.

| Tarea | Análisis | Sin historial | Con historial | Diferencia | Mejoran | p (Holm) | Decisión |
|---|---|---|---|---|---|---|---|
| Atención | 16-11, una partición | 0,684 | 0,710 | +0,026 [+0,018; +0,035] | 36/41 | 0,00001 | Respaldo |
| Atención | 22-11, 5 particiones | 0,683 | 0,712 | +0,029 [+0,021; +0,037] | 36/41 | < 0,0001 | Efecto relevante |
| Activación | 16-11, una partición | 0,529 | 0,563 | +0,034 [−0,001; +0,069] | 24/41 | 0,066 | Inconcluso |
| Activación | 22-11, 5 particiones | 0,518 | 0,554 | +0,036 [+0,010; +0,065] | 23/41 | 0,021 | Respaldo |

Las dos filas de cada tarea miden el mismo contraste, con los mismos modelos y etiquetas. Difieren en la partición: el 16-11 se usó una partición de 8 grupos y el 22-11 se promedió la AUC de cada persona sobre 5 particiones nuevas, lo que reduce el ruido debido a la partición. El tamaño del efecto casi no cambia; cambia la precisión, y con ella la decisión. En atención el límite inferior pasa de 0,018 a 0,021 y cruza el margen de 0,02. En activación el intervalo deja de incluir el cero. La repetición no es una confirmación independiente: usa las mismas 41 personas, y el contraste de activación ya se había visto positivo en tres particiones alternativas el 16-11 (+0,042 a +0,043, con límites inferiores de +0,006 a +0,013).

Por partición, la diferencia del 22-11 va de +0,028 a +0,030 en atención y de +0,028 a +0,047 en activación. En activación el signo es estable, pero no todos los intervalos por partición excluyen el cero (recálculo de la auditoría final).

**Controles registrados.**

- *Tiempo de sesión* (22-11, segundo contraste de la familia confirmatoria): con el tiempo de sesión como variable en ambos modelos, la diferencia es +0,032 [+0,024; +0,040] en atención (37/41; efecto relevante) y +0,026 [−0,006; +0,056] en activación (27/41; p Holm 0,111; inconcluso).
- *Modelo Profesor sin las personas evaluadas* (16-11): en atención la diferencia es +0,024 [+0,015; +0,034] (34/41).

**Lecturas descriptivas.**

- En activación el efecto es desigual entre personas: la mediana es +0,014, mejoran 23 de 41 y una persona, P4, aporta 0,009 de los 0,036; es la que conserva solo 26 ventanas con etiqueta (sección 4.5.2), de modo que su AUC es muy imprecisa. La AUC por persona pesa igual a todas las personas y no se fijó un mínimo de ventanas. Sin la persona más influyente la diferencia es +0,028 [+0,006; +0,050] (sensibilidad no registrada, pedida por la auditoría de resultados).
- Por grupo de origen (16-11; análisis no registrado en el protocolo), el efecto de atención se repite en las 25 personas de entrenamiento (+0,023 [+0,014; +0,031]) y en las 16 de validación y test (+0,032 [+0,016; +0,048]). El de activación aparece en las primeras (+0,055 [+0,012; +0,101]) y no en las segundas (+0,001 [−0,052; +0,055]); se discute abajo, junto con la selección de la configuración.
- En el cierre V3, con las particiones originales, el contraste de atención fue +0,018 [+0,009; +0,027] en entrenamiento (25 personas), +0,020 [−0,003; +0,042] en validación (8) y +0,029 [+0,004; +0,052] en test (8). El de activación incluyó el cero en las tres: +0,016 [−0,036; +0,070], +0,059 [−0,004; +0,131] y +0,033 [−0,021; +0,094].

**Selección de la configuración y grupos de personas (límite destacado).** Las 15 hojas de activación se eligieron con las 25 personas de entrenamiento, por la AUC media en validación interna de los modelos con 1, 8 y 32 ventanas de contexto. La elección la decide el contexto de 32:

| Contexto | 7 hojas | 15 hojas |
|---|---|---|
| 1 ventana | 0,5123 | 0,5121 |
| 8 ventanas | 0,5341 | 0,5311 |
| 32 ventanas | 0,4994 | 0,5311 |
| Media (criterio) | 0,5152 | 0,5248 |

En esa búsqueda, historial menos sin historial vale −0,013 con 7 hojas y +0,019 con 15: se congeló la configuración en que el historial gana. En atención la elección no importa (+0,0135 con 7 hojas y +0,0124 con 15). Como esas 25 personas son 25 de las 41 que luego se evalúan, el diseño permite un sesgo a favor del historial en ellas. Separando por grupo las predicciones guardadas (comprobación de la auditoría de código del 26-11, descriptiva y no registrada):

| Contraste de activación | 41 personas | 25 de la búsqueda | 16 restantes |
|---|---|---|---|
| Principal, 16-11 | +0,034 | +0,055 [+0,012; +0,101] | +0,001 [−0,052; +0,055] |
| Principal, 5 particiones (22-11) | +0,036 | +0,046 [+0,012; +0,086] | +0,021 [−0,017; +0,060] |
| Con tiempo de sesión | +0,026 | +0,050 [+0,013; +0,085] | −0,011 [−0,066; +0,038] |
| Con posición (Q1) | +0,032 | +0,049 [+0,018; +0,081] | +0,006 [−0,043; +0,049] |
| Historial − posición (18-11) | +0,038 | +0,063 [+0,021; +0,109] | −0,001 [−0,056; +0,054] |
| Historial − placebo (16-11) | +0,038 | +0,057 [+0,023; +0,092] | +0,008 [−0,048; +0,058] |
| Historial desplazado 6 − placebo | +0,046 | +0,035 [+0,003; +0,064] | +0,064 [+0,015; +0,115] |
| Banda de 6 s − placebo (40 personas) | +0,047 | +0,058 [+0,015; +0,101] | +0,030 [−0,003; +0,068] |
| GRU hasta 32 − GRU una ventana (sin búsqueda) | +0,051 | +0,045 [+0,007; +0,083] | +0,059 [+0,014; +0,102] |

Los contrastes del HGB con historial hasta 32 se concentran en las 25 personas de la búsqueda. El sesgo es posible y no está demostrado: los intervalos de ambos grupos se solapan y, según la auditoría, la diferencia entre grupos no es significativa con 16 personas. En el cierre V3, con modelos ajustados solo con las 25, el mismo contraste fue +0,059 en validación y +0,033 en test (8 personas cada uno, con intervalos que incluyen el cero), y +0,016 [−0,036; +0,070] en las propias 25 con selección anidada: el patrón inverso. Los dos contrastes que no dependen de esa elección de la misma forma, el historial desplazado frente al placebo y la GRU, que no tuvo búsqueda, son positivos en ambos grupos. Lo que queda es que el efecto no es estable entre subconjuntos de personas ni entre diseños de evaluación, y que el "respaldo" del contraste principal es más débil de lo que indica su intervalo. Una sensibilidad con 7 hojas o con selección anidada lo resolvería; no se corrió.

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

El análisis del 18-11 se motivó tras observar el placebo y se reporta como post hoc. La fase 3 repitió la pregunta con el contraste fijado antes de correr; sus dos pruebas de atención son las dos últimas filas. Con la posición como variable, el historial no agrega nada. Un modelo con la ventana actual y un solo número, los segundos en el estímulo, rinde lo mismo que el modelo con todo el historial (0,711 frente a 0,712; con ambos, 0,713).

**Curva temporal (22-11, secundaria).** Las ventanas de los segundos anteriores no aportan sobre la etiqueta de atención más que un placebo de la misma persona.

| Desfase | Desfase − placebo disperso (fase 1) | Desfase − placebo de bloque (fase 2, post hoc) |
|---|---|---|
| 6 s | −0,004 [−0,010; +0,002] · nulo concluyente | −0,003 [−0,010; +0,004] · nulo concluyente |
| 12 s | −0,004 [−0,012; +0,004] · nulo concluyente | −0,003 [−0,011; +0,004] · nulo concluyente |
| 24 s | −0,007 [−0,013; −0,000] · inferior | −0,006 [−0,013; +0,001] · nulo concluyente |
| 48 s | −0,012 [−0,020; −0,005] · inferior | −0,012 [−0,020; −0,004] · inferior |
| 96 s | −0,010 [−0,016; −0,003] · inferior | −0,009 [−0,016; −0,002] · inferior |

A 24 s las dos variantes dan decisiones distintas con cifras casi iguales, porque el límite superior del intervalo queda en el borde del cero. Las diferencias "inferiores" son pequeñas (hasta −0,012). En esta curva y en la fase 2 las reglas de decisión se usan como lectura descriptiva. No hay tendencia clara con el desfase (−0,002 por duplicación; p 0,071). El análisis del 16-11 con historial desplazado seis ventanas va en el mismo sentido: real menos placebo −0,002 [−0,005; +0,000] (−0,0025 en el CSV; el INFORME muestra −0,003 por un redondeo doble).

**AUC estratificada (22-11, fase 2, post hoc).** Con el contraste historial menos sin historial, la ganancia en atención se mantiene dentro del mismo estímulo (+0,013 [+0,006; +0,021]), dentro del mismo minuto (+0,023 [+0,016; +0,030]) y a igual posición (+0,017 [+0,010; +0,024]); las tres con decisión de respaldo. La ganancia a igual posición parecía contradecir el análisis del 18-11. Una comprobación no registrada, hecha después de ver los resultados y con una sola partición, mostró que no: al comparar con el modelo que ya recibe la posición, el historial agrega +0,004 [−0,001; +0,009] a igual posición, −0,003 [−0,007; +0,002] dentro del mismo estímulo y −0,004 [−0,008; +0,001] dentro del mismo minuto. En la fase 3, el contraste registrado calculado a igual posición da +0,005 [+0,001; +0,010] (estrato descriptivo).

**Cuánto depende la etiqueta del reloj (descriptivo).** Un modelo que recibe solo los segundos transcurridos en el estímulo, sin fisiología, llega a 0,598 [0,581; 0,614]. El tiempo de sesión como única variable adicional agrega +0,025 [+0,019; +0,032]. La detección no es un artefacto de la posición: comparando solo ventanas de la misma posición, la AUC sin historial es 0,677 [0,654; 0,699], frente a 0,684 sin estratificar en la misma partición.

**Etiqueta corregida por posición (22-11, enfoque E1, registrado).**

| Prueba | Diferencia | Mejoran | p (Holm) | Decisión |
|---|---|---|---|---|
| A1 Detección sin historial: corregida − original | −0,008 [−0,015; −0,001] | 17/41 | 0,055 | Inferior |
| A2 Historial − sin historial, etiqueta corregida | +0,010 [+0,006; +0,015] | 31/41 | 0,0003 | Respaldo |
| A3 (Historial + posición) − (actual + posición), corregida | +0,004 [+0,000; +0,009] | 24/41 | 0,055 | Nulo concluyente |

Con la etiqueta corregida la posición sola deja de predecir (0,504 [0,498; 0,510]; con la original, 0,598) y la detección baja poco (0,675 frente a 0,683), aunque la decisión registrada de ese contraste (A1) fue "inferior" (−0,008). La mejora del historial baja de +0,029 a +0,010 y, con la posición como variable, queda en +0,004. A1 compara AUC frente a dos objetivos distintos (cambia el 9,4 % de las etiquetas), por lo que no implica que la detección original fuera espuria. Las decisiones de A1 y A3 están al filo: A1 es "inferior" porque el límite superior de su intervalo es −0,001 (la regla no exige Holm para "inferior"), y A3 sería "respaldo" con un p de Holm bajo 0,05 (es 0,055). En este análisis las predicciones del modelo con historial y posición son idénticas a las del modelo con historial, de modo que A3 equivale a comparar el modelo con historial con el de la ventana actual con posición. Un diagnóstico del 26-11, que reajustó un solo grupo de una partición, indica que no es un error: el modelo recibe la columna de posición y no la usa en ninguna de sus 1.800 divisiones, lo que es coherente con que la posición sola no prediga la etiqueta corregida.

Fuentes: `resultados/cierre_robustez_41p_16-11-2026/INFORME.md`, `resultados/ampliacion_41p_16-11-2026/INFORME.md` (y `enmienda_e1_lag6/contrastes.csv`), `resultados/explicativo_posicion_41p_18-11-2026/INFORME.md`, `resultados/reapertura_41p_22-11-2026/INFORME.md` (y `curva_temporal.csv`), `resultados/reapertura_fase2_41p_22-11-2026/` (`x1_placebo_bloque.csv`, `x2_estratificada.csv`, `posthoc_no_registrado_estratos_con_posicion.csv`), `resultados/reapertura_fase3_41p_22-11-2026/INFORME.md`, `resultados/enfoques_41p_22-11-2026/INFORME.md` (y `e1_confirmatorio.csv`), `documentacion/auditoria_final_23-11-2026/ronda2/DIAGNOSTICO_E1_POSICION.md`.

### 7.3 Activación: alcance temporal y controles

**Placebo e historial desplazado (16-11, registrados).** El historial real supera al placebo en +0,038 [+0,006; +0,068] (26/41; p Holm 0,043) y el placebo no aporta sobre el modelo sin historial (−0,004 [−0,030; +0,024]). El historial que excluye las seis ventanas más recientes, y que por lo tanto no se solapa con las ventanas que promedia el *Arousal Score* (aunque sí con el soporte de su filtro tónico; ver "Límites de la curva"), supera a un placebo equivalente en +0,046 [+0,018; +0,073] (28/41; p Holm 0,004; respaldo, no efecto relevante: el límite inferior es 0,018) y al modelo sin historial en +0,053 [+0,022; +0,083]. Con cinco ventanas de desplazamiento, que dejan 1 s de solapamiento, la diferencia frente al placebo es +0,040 [+0,012; +0,066]. La calibración con los primeros minutos de la persona agrega entre +0,001 y +0,009. Por grupo de personas (tabla de la sección 7.1), el historial real frente al placebo se concentra en las 25 personas con que se eligió la configuración (+0,057 frente a +0,008), mientras que el historial desplazado frente al placebo es positivo en ambos grupos (+0,035 y +0,064).

**Curva temporal (22-11).**

| Desfase | Desfase − placebo disperso (fase 1, secundaria) | Desfase − placebo de bloque (fase 2, post hoc) |
|---|---|---|
| 6 s | +0,047 [+0,017; +0,078] · p Holm 0,017 · respaldo | +0,053 [+0,026; +0,081] · p Holm 0,003 · efecto relevante |
| 12 s | +0,024 [−0,011; +0,060] · inconcluso | +0,030 [−0,005; +0,064] · inconcluso |
| 24 s | +0,004 [−0,033; +0,042] · inconcluso | +0,009 [−0,027; +0,045] · inconcluso |
| 48 s | −0,023 [−0,053; +0,010] · inconcluso | −0,017 [−0,041; +0,009] · inconcluso |
| 96 s | +0,019 [−0,016; +0,053] · inconcluso | +0,024 [−0,011; +0,059] · inconcluso |

Solo el desfase de 6 s alcanza respaldo. Su límite inferior es +0,017 (0,017474 en `curva_temporal.csv`); el INFORME muestra +0,018 por un redondeo doble. A 12 s el resultado es inconcluso, y desde 24 s también: inconcluso, no nulo. Ningún intervalo de 90 % cabe en ±0,02, de modo que la curva no demuestra que el efecto desaparezca; desde 24 s el contraste no se distingue del placebo, sin que eso demuestre ausencia. El contraste cae 0,010 por cada duplicación del desfase [−0,018; −0,003] (p 0,009; 27 de 40 personas); es una sola prueba, sin ajuste. El placebo no aporta sobre la ventana actual (+0,009 [−0,024; +0,043]) y los dos placebos rinden igual (bloque menos disperso, −0,006). Los resultados no dependen de una sola persona (sensibilidad no registrada, pedida por la auditoría de resultados): sin la más influyente, el contraste de 6 s queda en +0,039 [+0,012; +0,065] frente al placebo disperso y en +0,046 [+0,021; +0,070] frente al de bloque.

El +0,047 del 22-11 y el +0,046 del 16-11 se parecen, pero no son el mismo contraste. El del 16-11 usa el historial del mismo estímulo sin sus seis ventanas más recientes, un placebo de otros estímulos, una partición y 41 personas. El del 22-11 usa una banda de 6 s situada 6 s antes, sin importar el estímulo, un placebo a 150 s o más, también una sola partición (la registrada el 16-11) y las filas con cobertura completa hasta 102 s atrás (6.268 filas de 40 personas, el 53 % de las de activación).

**AUC estratificada (22-11, fase 2, post hoc).** Contraste: historial menos sin historial.

| Estrato | Diferencia | p (Holm) | Decisión |
|---|---|---|---|
| Mismo estímulo | +0,054 [+0,015; +0,094] | 0,022 | Respaldo |
| Mismo minuto de sesión | +0,058 [+0,027; +0,092] | 0,003 | Efecto relevante |
| Misma posición en el estímulo | +0,027 [−0,003; +0,059] | 0,092 | Inconcluso |

La ganancia se mantiene dentro del mismo minuto, lo que habla contra una deriva lenta de la sesión como única explicación; es un análisis post hoc, y el control registrado del tiempo de sesión quedó inconcluso (sección 7.1). Dentro de un mismo estímulo o de un mismo minuto, la ventana actual sola no distingue nada (AUC 0,501 en ambos); con historial sube a 0,555 y 0,560. Estas AUC usan una fracción pequeña de las comparaciones: el 2–3 % de los pares de una persona cae dentro de un mismo estímulo y el 7 % dentro de un mismo minuto.

**Historial frente a posición (22-11, fase 3, registrado).** Contraste: (historial + posición) − (ventana actual + posición).

| Prueba | Diferencia | Mejoran | p | p (Holm) | Decisión |
|---|---|---|---|---|---|
| Q1 Todas las comparaciones | +0,032 [+0,004; +0,059] | 28/41 | 0,027 | 0,108 | Inconcluso |
| Q2 Dentro del mismo estímulo | +0,009 [−0,020; +0,037] | 20/41 | 0,57 | 1,00 | Inconcluso |

En Q1 el intervalo sin ajustar queda sobre cero, pero no pasa la corrección de Holm sobre las cuatro pruebas de la fase. La media y la mediana coinciden (+0,032 y +0,031) y la persona más influyente empuja en contra: sin ella la diferencia es +0,039 [+0,015; +0,063] (sensibilidad descriptiva, sin ajuste).

| Modelo | AUC, todas las comparaciones | AUC, mismo estímulo |
|---|---|---|
| Ventana actual | 0,518 | 0,501 |
| Ventana actual + posición | 0,523 | 0,550 |
| Historial hasta 32 | 0,554 | 0,555 |
| Historial + posición | 0,555 | 0,559 |

La posición actúa de forma distinta según la comparación. Entre todas las ventanas no se observa aporte de la posición (+0,006 [−0,015; +0,026]) y sí del historial (+0,031 [+0,004; +0,057] sobre el modelo con posición; descriptivo, sin ajuste). Dentro de un mismo estímulo el tiempo transcurrido mejora la predicción por sí solo (+0,049 [+0,027; +0,072]) y no se demostró que el historial lo supere (+0,005 [−0,025; +0,035]). Esta comparación es descriptiva y Q2 es inconcluso y de poca potencia: no demuestran que, dentro de un mismo estímulo, el aporte del historial se explique por el tiempo transcurrido, ni que no exista. El análisis post hoc del 18-11, con una partición, había dado historial menos posición +0,038 [+0,002; +0,074] y posición menos sin historial −0,004 [−0,023; +0,017]. La comprobación no registrada del 22-11 (una partición) coincide con la fase 3 en el signo del aporte de la posición dentro de un mismo estímulo (posición menos sin historial, +0,040 [+0,014; +0,067]); en historial menos posición el signo difiere (−0,015 [−0,056; +0,024], frente a +0,005 en la fase 3), con intervalos que incluyen el cero en ambos casos.

**Persistencia de la etiqueta (descriptivo).** La etiqueta de activación de 6 s antes en el mismo estímulo predice la actual con AUC 0,680 [0,634; 0,724] (5.035 pares, 40 personas). En atención esa AUC es 0,535 [0,519; 0,552] (8.818 pares). El estado de activación, tal como lo define la etiqueta, persiste varios segundos; el de atención casi no. La etiqueta binaria subestima esa persistencia: la media de la GSR de 30 s antes ordena la etiqueta actual con AUC 0,80 (0,87 a 6 s y 0,85 a 12 s antes; comprobación de la auditoría de código).

**Límites de la curva.** En el desfase de 6 s el 73 % de las ventanas pertenece al mismo estímulo que la actual (48 % a 12 s, 13 % a 24 s y 0 % desde 48 s): la curva mezcla cercanía temporal con pertenecer al mismo estímulo. La etiqueta de activación integra GSR en [t−4, t+2) s y la banda de 6 s usa fisiología hasta t−4: en su soporte nominal son contiguas, sin holgura entre ambas. Esa contigüidad vale para el soporte nominal de las ventanas, no para la señal. La componente tónica se obtiene con un filtro pasa-bajos de 0,05 Hz aplicado en ambos sentidos sobre la sesión completa, la fásica es la señal menos la tónica y la señal se estandariza por sesión (sección 4.6.3). Como la etiqueta es en lo esencial el nivel tónico (sección 6.1), su soporte real excede los 6 s: del peso de la GSR sobre la parte tónica de la etiqueta de una ventana, el 49 % cae dentro de [t−4, t+2), el 25 % antes de t−4 y el 25 % después de t+2; antes de t−10 queda el 3,7 % (comprobación de la auditoría de código del 26-11). El historial "sin las ventanas de la etiqueta", tanto el desplazado del 16-11 como la banda de 6 s, coincide entonces en el tiempo con GSR que pesa cerca de un cuarto en la componente dominante de la etiqueta. Además la etiqueta de una ventana incluye GSR de varios segundos después, de modo que parte de la tarea es anticipar la GSR inmediata. No es fuga, porque la GSR no es entrada del *Modelo Estudiante* de activación, pero cambia lo que estos contrastes demuestran (sección 8.4).

Fuentes: `resultados/cierre_robustez_41p_16-11-2026/INFORME.md`, `resultados/ampliacion_41p_16-11-2026/INFORME.md`, `resultados/explicativo_posicion_41p_18-11-2026/INFORME.md`, `resultados/reapertura_41p_22-11-2026/INFORME.md`, `resultados/reapertura_fase2_41p_22-11-2026/` (`x1_placebo_bloque.csv`, `x2_estratificada.csv`, `descriptivos.csv`, `posthoc_no_registrado_estratos_con_posicion.csv`), `resultados/reapertura_fase3_41p_22-11-2026/INFORME.md`.

### 7.4 Orden de las ventanas

La red GRU es el único modelo que usa el orden de las ventanas. Se evaluó el 16-11 con una partición, como contraste secundario y sin corrección por multiplicidad. Los análisis del 22 y 23-11 no la incluyen.

| Tarea | GRU hasta 32 − GRU una ventana | GRU hasta 32 − HGB hasta 32 |
|---|---|---|
| Atención | +0,008 [−0,004; +0,020] · 26/41 · intervalo de 90 % dentro de ±0,02 | −0,040 [−0,055; −0,027] · 9/41 |
| Activación | +0,051 [+0,021; +0,080] · 28/41 · p 0,002 sin corregir | +0,020 [−0,017; +0,057] · 22/41 |

En atención el orden no agrega un efecto relevante y la GRU rinde 0,040 menos que el resumen estadístico. En activación la GRU con historial supera a su control de una ventana, pero no supera de forma demostrable al HGB con historial. En el cierre V3 esa mejora apareció en validación (+0,091) y en test (+0,084) y no en entrenamiento (−0,016). Ese contraste mide el aporte del historial dentro de la GRU, no el del orden; el contraste propio del orden (GRU menos HGB, ambos con historial) es inconcluso. Es un indicio secundario, no un resultado.

Fuentes: `resultados/cierre_final_41p_16-11-2026/INFORME.md`, `resultados/cierre_v3_16-11-2026/INFORME.md`.

### 7.5 Tipos de fusión

Con una misma familia (MLP), 41 personas y una partición (16-11, secundario):

| Tarea | Tardía − temprana | Intermedia − temprana | Intermedia − tardía |
|---|---|---|---|
| Atención | +0,012 [+0,005; +0,021] | +0,005 [−0,003; +0,013] | −0,007 [−0,014; −0,001] |
| Activación | +0,006 [−0,032; +0,042] | +0,002 [−0,019; +0,023] | −0,004 [−0,042; +0,039] |

En atención, entre redes MLP, la fusión tardía supera a la temprana (+0,012 [+0,005; +0,021]) y a la intermedia; son contrastes secundarios, sin corrección. En activación no se demostraron diferencias. La arquitectura intermedia evaluada es más profunda que la temprana, por lo que la comparación incluye también una diferencia de capacidad.

El resultado depende de la familia de modelos. En el cierre V3, con HGB y las particiones originales, la fusión tardía no superó a la temprana: en atención la diferencia fue −0,010 [−0,018; −0,003] en entrenamiento, −0,008 [−0,020; +0,005] en validación y −0,002 [−0,015; +0,008] en test; en activación, +0,009 [−0,025; +0,042], −0,107 [−0,223; −0,011] y −0,001 [−0,065; +0,066]. La ventaja de la fusión tardía en atención vale para el MLP y no puede generalizarse: con HGB el signo fue el contrario. Además, la red MLP con fusión tardía rinde 0,024 menos que el HGB con fusión temprana sobre la misma representación (0,686 frente a 0,710; [−0,038; −0,012], recálculo de la auditoría final). No puede concluirse que la fusión tardía sea mejor en general. La fusión no se volvió a evaluar el 22 ni el 23-11.

Fuentes: `resultados/ampliacion_41p_16-11-2026/INFORME.md`, `resultados/cierre_v3_16-11-2026/INFORME.md`, `documentacion/auditoria_final_23-11-2026/recalculo.json` (recálculo de la auditoría final).

### 7.6 Qué detecta el Modelo Estudiante de atención

**Aporte de cada señal (22-11, enfoque E2, registrado).** Etiqueta original, modelos sin historial.

| Prueba | Diferencia | Mejoran | Decisión |
|---|---|---|---|
| B1 Solo EEG − 0,5 | +0,181 [+0,164; +0,197] | 41/41 | Efecto relevante |
| B2 Solo GSR − 0,5 | +0,045 [+0,030; +0,062] | 36/41 | Efecto relevante |
| B3 (EEG + GSR) − solo EEG | +0,002 [−0,001; +0,005] | 24/41 | Nulo concluyente |
| B4 Solo EEG − solo GSR | +0,136 [+0,113; +0,158] | 40/41 | Efecto relevante |
| B5 Solo alfa y beta − 0,5 | +0,093 [+0,079; +0,106] | 40/41 | Efecto relevante |
| B6 Canales posteriores − 0,5 | +0,102 [+0,083; +0,121] | 38/41 | Efecto relevante |
| B7 (Potencia lenta y amplitud) − (alfa y beta) | +0,080 [+0,067; +0,092] | 40/41 | Efecto relevante |
| B8 Frontales − posteriores | +0,073 [+0,054; +0,092] | 38/41 | Efecto relevante |

Las pruebas B5 a B8 forman una segunda familia, agregada por la auditoría de código antes de correr. La detección descansa en el EEG y la GSR no le agrega nada. Esto coincide con la importancia por permutación del 16-11 (descriptiva): la AUC cae 0,207 al permutar el EEG y 0,004 al permutar la GSR.

| Variables de EEG | AUC original | AUC a igual posición | AUC sin 3 componentes oculares | Caída |
|---|---|---|---|---|
| Todo el EEG | 0,681 | 0,675 | 0,621 | 0,060 |
| Potencia lenta (delta, theta) y amplitud | 0,673 | 0,659 | 0,602 | 0,070 |
| Canales frontales | 0,675 | 0,667 | 0,621 | 0,054 |
| Canales posteriores | 0,602 | 0,600 | 0,562 | 0,040 |
| Solo alfa y beta | 0,593 | 0,593 | 0,547 | 0,045 |

Las variables que más detectan son las que suelen llevar la firma de los movimientos oculares en el EEG: potencia lenta, amplitud y electrodos frontales. Ese patrón es compatible con un origen ocular, pero no lo mide; la medición directa es la limpieza ocular, más abajo. La probabilidad del modelo de EEG se asocia sobre todo con el recorrido de la mirada (correlación de Spearman media por persona 0,41), luego con la dispersión (0,30) y la duración total de fijaciones (0,29); con la pupila, −0,09. Un control con etiquetas barajadas da 0,496 [0,482; 0,510].

**Montaje y sincronía (23-11, descriptivo).** El montaje de los electrodos no estaba documentado y la división entre canales frontales y posteriores del 22-11 era un supuesto. La respuesta promedio al parpadeo es de 148 y 151 µV en los dos canales frontopolares, 74 y 77 µV en los frontales laterales, 57 y 56 µV en los frontales, y de 18 a 29 µV en los centrales, temporales, parietales y occipitales. La mirada horizontal entra con signo opuesto en los dos canales frontales laterales en 31 de las 37 personas con ambos canales utilizables. El patrón es compatible con el montaje por defecto del equipo (OpenBCI Cyton+Daisy); esto respalda la división usada, pero no reemplaza la documentación del experimento.

El mismo análisis mostró que el EEG va entre 0,18 y 0,53 s atrasado respecto del reloj del seguidor ocular en las 41 personas (mediana 0,45 s; cuartiles 0,28 y 0,48 s). Las ventanas de 2 s del EEG están corridas entre un 9 % y un 26 % (mediana 22 %) respecto de las de mirada, pupila y GSR. El desfase no se corrigió, porque las ventanas vigentes están congeladas; puede atenuar la relación entre el EEG y las demás señales, incluidas las etiquetas; ese efecto no se midió. El desfase se agrupa en dos valores (cerca de 0,27 s en P2 a P21, P36 y P37, y cerca de 0,47 s en el resto), lo que sugiere una causa sistemática de adquisición que no se investigó, y su estimación es poco segura en las personas con acoplamiento bajo. Según el signo con que se estimó (el EEG responde al parpadeo después de su marca en el seguidor ocular), cada ventana de EEG contendría actividad ligada a la conducta ocular de unas décimas de segundo antes de la ventana, y no posterior; esa dirección falta confirmarla en el script de montaje.

**Limpieza ocular (23-11, registrado).** Modelos de atención solo con EEG, ventana actual, las mismas 5 particiones.

| Prueba | Contraste | Diferencia | A favor | Decisión |
|---|---|---|---|---|
| L1 | EEG original − EEG limpio | +0,060 [+0,044; +0,075] | 39/41 | Efecto relevante |
| L2 | Control − EEG limpio | +0,054 [+0,037; +0,070] | 37/41 | Efecto relevante |
| L3 | EEG limpio − 0,5 | +0,121 [+0,107; +0,135] | 41/41 | Efecto relevante |
| L4 | Alfa y beta limpio − alfa y beta original | −0,045 [−0,059; −0,032] | 6/41 | Inferior |

La columna "A favor" cuenta las personas con diferencia positiva. En L4 son las 6 personas en que la limpieza sube la AUC de alfa y beta.

Quitar tres componentes oculares, que representan una mediana de 3,5 % de la varianza, baja la AUC de 0,681 a 0,621. Quitar tres componentes no oculares, con una mediana de 72 % de la varianza, la deja en 0,674 (caída de 0,007 [−0,001; +0,015]). La caída es específica de los componentes elegidos por su relación con la mirada y los parpadeos, y no una consecuencia de quitar varianza. Como esos componentes se eligen con las mismas señales oculares que definen la etiqueta, quitarlos puede retirar también actividad cerebral acoplada a los movimientos de los ojos; el control, que no está igualado en esa relación, acota la objeción y no la elimina. La caída equivale a cerca de un tercio de lo que el modelo tiene sobre el azar (0,060 de 0,181), y el modelo limpio sigue sobre el azar en las 41 personas (0,621; L3). El límite inferior de L1 es +0,044 (0,044497 en el CSV); el INFORME muestra +0,045 por un redondeo doble. La detección por alfa y beta, que el 22-11 parecía la parte menos expuesta al artefacto, también cae (de 0,593 a 0,547); la lectura fijada de antemano solo contemplaba que no cambiara.

La caída crece con el número de componentes quitados y se va frenando: 0,661 con uno, 0,638 con dos, 0,621 con tres y 0,613 con cuatro (el cuarto agrega 0,007 [−0,000; +0,015]). Un segundo método, la regresión sobre los cuatro canales frontales, coincide en el sentido pero limpia poco: descartar esos canales baja la AUC de 0,681 a 0,646 y la regresión resta otros 0,012 [−0,000; +0,024].

La limpieza es parcial. La correlación máxima entre algún canal y los parpadeos baja de 0,28 a 0,08 (mediana entre personas), sin anularse, y la probabilidad del modelo limpio sigue asociada al recorrido de la mirada (Spearman 0,28; antes 0,41). Tras la limpieza se mantiene el mismo orden: canales frontales sobre posteriores (+0,059) y potencia lenta sobre alfa y beta (+0,055). Por eso 0,060 se lee como cota inferior de la contribución ocular. Es la lectura más defendible y no una demostración, porque la objeción contraria también vale: con 11 a 16 canales, tres componentes arrastran actividad frontal no ocular (sección 8.8). Lo medido es que la AUC sobre el azar baja cerca de un tercio al quitar esos componentes, y no puede descartarse que el resto de la detección también dependa de los ojos. Esto último es una inferencia apoyada en el patrón espacial y espectral del remanente, que el diseño no separa. La detección que podría defenderse como no ocular baja de 0,59–0,60 (estimación del 22-11) a 0,55–0,56, sobre el azar en 38 de 41 personas.

**Red convolucional sobre la señal cruda (23-11, registrado).**

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

En atención la red supera al modelo de referencia. La GRU y los MLP no lo habían logrado, pero usaban otras entradas, de modo que esa comparación no es directa. Su detección depende de lo ocular: al quitar los tres componentes oculares pierde 0,067 (R3, sin control propio), algo más que el HGB (0,060), y su probabilidad se asocia con el recorrido de la mirada más que la del HGB (Spearman 0,48 frente a 0,41; tras la limpieza, 0,33). Su ventaja sobre el HGB, en cambio, se mantiene con el EEG limpio: +0,028, frente a +0,035 con el original. La diferencia entre ambas ventajas, calculada por la auditoría final y no registrada, es +0,007 [−0,005; +0,020]: no se demostró que la ventaja cambie al limpiar.

Cuatro límites acotan esta lectura. R1 es efecto relevante con holgura mínima: el límite inferior es 0,023 y, sin las dos personas más favorables, queda en 0,0199. R3 no tiene control propio: no se entrenó una red con el filtro de control, de modo que la especificidad ocular de su pérdida descansa en el control del modelo de referencia (L2). Es una sola arquitectura, sin búsqueda, con una inicialización por grupo y sin curva de convergencia. Y la red recibe la señal escalada por persona y canal con toda la sesión, mientras el modelo de referencia usa variables sin esa escala y con su configuración congelada: la ventaja no puede atribuirse a la arquitectura sin separar ese factor.

Fuentes: `resultados/enfoques_41p_22-11-2026/INFORME.md`, `resultados/ampliacion_41p_16-11-2026/INFORME.md`, `resultados/montaje_ocular_41p_23-11-2026/INFORME.md`, `resultados/limpieza_ocular_41p_23-11-2026/INFORME.md`, `resultados/red_cruda_41p_23-11-2026/INFORME.md`, `documentacion/auditoria_final_23-11-2026/recalculo.json` (recálculo de la auditoría final).

### 7.7 Activación: ventana actual, estímulo y persona

**Ventana actual.** Ningún modelo de la ventana actual queda claramente sobre el azar (5 particiones):

| Modelo | AUC | Personas sobre 0,5 |
|---|---|---|
| HGB, solo EEG | 0,524 [0,497; 0,550] | 26/41 |
| HGB, EEG + mirada + pupila | 0,518 [0,491; 0,545] | 22/41 |
| Red convolucional, EEG crudo | 0,498 [0,478; 0,518] | 20/41 |

La comparación entre la red y el HGB (R4) es inconclusa e inestable: el signo cambia en una de las cinco particiones y la decisión pasa a "inferior" al quitar una sola persona, si es cualquiera de cinco personas concretas. Compara dos modelos sin señal demostrada. No se demostró que un modelo más complejo ayude en activación, ni tampoco que perjudique.

**Predicción por estímulo (22-11, enfoque E3, registrado).** La unidad es el segmento y el objetivo, la mayoría de las etiquetas de sus ventanas (1.589 segmentos).

| Prueba | Diferencia | Mejoran | p (Holm) | Decisión |
|---|---|---|---|---|
| C1 Modelo de estímulo − 0,5 | +0,087 [+0,050; +0,122] | 32/41 | 0,0001 | Efecto relevante |
| C2 Modelo de estímulo − promedio del modelo por ventana con historial | +0,020 [−0,007; +0,046] | 23/41 | 0,27 | Inconcluso |
| C3 (Estímulo + duración) − solo duración | +0,048 [−0,014; +0,109] | 25/41 | 0,27 | Inconcluso |

El modelo de estímulo llega a 0,587 [0,550; 0,622], la AUC más alta obtenida en activación. No se demuestra que supere a promediar el modelo por ventana con historial (0,567) ni que aporte sobre la duración del estímulo (0,535 [0,488; 0,583] por sí sola). Este modelo usa todas las ventanas del segmento, también las posteriores a cada etiqueta: no es causal.

**Diferencias entre personas (22-11, enfoque E4).** La detectabilidad de cada persona es estable entre dos mitades de su sesión: la correlación de Spearman de la AUC sin historial es 0,76 [0,58; 0,86] en atención y 0,66 [0,44; 0,80] en activación. La ganancia del historial de cada persona no es fiable (0,30 [−0,05; 0,61] y 0,25 [−0,04; 0,51]). Ninguna característica de la persona se asocia con la AUC ni con la ganancia tras Holm.

**Adaptación a la persona (22-11, enfoque E4, registrado).**

| Tarea | Contraste | Diferencia | Mejoran | p (Holm) | Decisión |
|---|---|---|---|---|---|
| Atención | Adaptado − general, sin historial | +0,006 [+0,000; +0,011] | 25/41 | 0,098 | Nulo concluyente |
| Atención | Adaptado − general, con historial | +0,000 [−0,007; +0,008] | 19/41 | 0,97 | Nulo concluyente |
| Activación | Adaptado − general, sin historial | +0,028 [+0,007; +0,049] | 29/40 | 0,049 | Respaldo |
| Activación | Adaptado − general, con historial | +0,045 [+0,023; +0,069] | 30/40 | 0,0004 | Efecto relevante |

En activación la adaptación se suma al historial: en la parte final de la sesión la AUC pasa de 0,502 (general, sin historial) a 0,587 (adaptado, con historial), y en el modelo adaptado el historial aporta +0,058 [+0,032; +0,084] (descriptivo que no figura en la lista registrada del protocolo). La decisión de la adaptación sin historial está pegada al umbral (p Holm 0,049; 0,0495 en el CSV, que el INFORME muestra como 0,050 por un redondeo doble). La adaptación es offline: las etiquetas de calibración se definen con la normalización de toda la sesión, por lo que no equivale a una calibración utilizable en línea. Se evalúa sobre la parte final de la sesión, que es una muestra distinta de la de los demás análisis.

Fuentes: `resultados/red_cruda_41p_23-11-2026/INFORME.md`, `resultados/enfoques_41p_22-11-2026/INFORME.md` (y `e4_confirmatorio.csv`), `resultados/reapertura_41p_22-11-2026/auc_absolutas.csv`.

### 7.8 Análisis descriptivos

Ninguno de estos patrones se sometió a contraste. Provienen del análisis del 16-11, con una partición.

- **Evolución en la sesión.** En atención, la AUC sube del primer al último quinto de la sesión: de 0,65 a 0,71 sin historial y de 0,69 a 0,74 con historial. En activación, la proporción de ventanas de clase alta cae a 0,37 en el último quinto, un patrón compatible con habituación, y también con una deriva lenta de la señal, con el orden de los estímulos o con el propio cálculo (nivel tónico estandarizado por sesión y filtrado en ambos sentidos). Se midió con la etiqueta binaria y no con el score continuo.
- **Importancia por bloques.** En atención, la caída de AUC al permutar el EEG es 0,207 y al permutar la GSR 0,004; la ventana actual pesa más que el historial, y las bandas theta y delta más que las restantes. En activación las caídas son 0,053 para el EEG, 0,050 para la media del historial y 0,021 para la pupila, y no se observa caída para la mirada. La desviación entre los 8 grupos de la validación cruzada supera a la media en los tres casos (±0,075, ±0,053 y ±0,027, según la auditoría final). Es un descriptivo ruidoso y no demuestra que el EEG aporte: no se demostró aporte del EEG de la ventana actual (0,524; sección 7.7).
- **Tipo de página.** La atención se predice mejor en sitios web (0,71) y peor en textos (0,60 sin historial; 0,63 con historial, donde solo queda por debajo una categoría con 25 personas). En activación, el historial mejora sobre todo en sitios web (de 0,525 a 0,588).

Fuentes: `resultados/ampliacion_41p_16-11-2026/INFORME.md` (y `por_categoria.csv`), `documentacion/auditoria_final_23-11-2026/recalculo.json` (recálculo de la auditoría final).

## Capítulo 8: Discusión

### 8.1 Respuesta a la hipótesis

La hipótesis central plantea que los modelos temporales multimodales rinden mejor fuera de muestra que los modelos estáticos comparables. Con el diseño de evaluación original (entrenamiento, validación y test por separado), el cierre V3 del 16-11 no encontró una ventaja consistente del modelo con historial en ninguna de las dos variables. El análisis con validación cruzada sobre las 41 personas se registró ese mismo día, después de conocer ese resultado, para ganar precisión. Con este segundo diseño y sus controles, y aplicando la tabla de criterios de interpretación del manuscrito, el resultado se lee como **evidencia mixta, con apoyo parcial**, que proviene de la activación. Esa lectura depende del cambio de diseño y no es el resultado del contraste planificado en un principio.

Dos precisiones sobre cómo se operacionalizó la hipótesis. En el contraste principal, "modelo temporal" designa un modelo no secuencial (HGB) que recibe un resumen estadístico de las ventanas previas; el único modelo que usa el orden de las ventanas (GRU) no mostró una ventaja demostrable. Y "multimodal" describe las señales de entrada, no un aporte demostrado de combinarlas: en atención la GSR no agrega al EEG, y en activación no se demostró el aporte de ninguna señal por separado. El apoyo parcial se refiere, entonces, al historial reciente de las señales, no a una arquitectura temporal ni a la fusión.

| Pregunta | Atención | Activación |
|---|---|---|
| ¿Mejora el modelo con historial? | Sí: +0,029 [+0,021; +0,037], efecto relevante | Sí, con respaldo al promediar 5 particiones: +0,036 [+0,010; +0,065]. Por partición, de +0,028 a +0,047, y no todos los intervalos excluyen el cero. Desigual entre personas: mediana +0,014; 23 de 41. Concentrado en las 25 personas con que se eligió la configuración (+0,046, frente a +0,021 en las otras 16; sección 7.1) |
| ¿La mejora proviene de la fisiología de las ventanas previas? | No: con la posición como variable, +0,001 [−0,002; +0,005], nulo concluyente | Apoyo acotado. El más sólido: el historial sin las ventanas de 6 s que promedia la etiqueta (pero dentro del soporte de su filtro tónico) supera a un placebo en +0,046 (p Holm 0,004; registrado antes de correr). En la curva, +0,047 [+0,017; +0,078] a 6 s; a 12 s es inconcluso y desde 24 s no se distingue del placebo, sin que eso demuestre ausencia. Los controles de tiempo de sesión, posición y mismo estímulo quedaron inconclusos |
| ¿Queda algo al controlar la posición? | No: nulo concluyente dentro de ±0,02 | +0,032 [+0,004; +0,059], inconcluso tras Holm |
| ¿Aporta el orden de las ventanas? | No: la GRU con historial no supera a su control (+0,008 [−0,004; +0,020]) y rinde 0,040 menos que el HGB | No demostrado: el contraste propio del orden (GRU − HGB, ambos con historial) es inconcluso, +0,020 [−0,017; +0,057]. La GRU con historial supera a su control de una ventana (+0,051 [+0,021; +0,080], secundario sin corrección), lo que mide el historial y no el orden |

Este encuadre es provisorio. Todos los análisis se hicieron sobre las mismas 41 personas, que incluyen las de validación y test ya consultadas, y los del 22 y 23-11 se diseñaron después de ver los anteriores. El apoyo en activación es evidencia acotada, no una confirmación.

### 8.2 Atención: una ventaja que no proviene de las ventanas previas

El modelo con historial rinde mejor en atención, de forma estable y en casi todas las personas. Esa ventaja no proviene de lo que ocurrió antes. La reproduce un historial de otros momentos, la reproduce un solo número (los segundos transcurridos en el estímulo) y desaparece cuando el modelo conoce ese número, tanto en el análisis post hoc del 18-11 como en el contraste registrado de la fase 3. Las ventanas de 6 a 96 s antes no aportan más que un placebo de la misma persona.

La lectura más coherente es que el *Attention Score* tiene una estructura sistemática al inicio de cada página: una caída a los 2–3 s seguida de un aumento. El modelo con historial la capturaba a través del largo del historial. La etiqueta depende mucho del reloj: la posición sola predice con AUC 0,598. Dado que la etiqueta se construye con fijaciones y mirada, este patrón podría reflejar la reorientación de la mirada al cambiar de página, es decir, lo **Observado** más que lo **Atendido**. Hay dos explicaciones más que no se separaron. Una es de cálculo: la duración de cada fijación se suma completa aunque exceda la ventana (la suma supera los 2.000 ms en cerca del 28 % de las ventanas etiquetadas), y las ventanas no cruzan el cambio de estímulo, lo que por sí solo acorta las duraciones al inicio de cada página. La otra es de composición: las posiciones tardías solo existen en los estímulos largos, de modo que la prevalencia por posición mezcla el tiempo transcurrido con el tipo de estímulo. La posición es, además, tiempo transcurrido: lo que el resultado descarta es un aporte del contenido fisiológico de las ventanas previas, no que el modelo use contexto temporal.

La etiqueta corregida por posición elimina ese efecto y la detección baja poco (0,675 frente a 0,683), aunque la decisión registrada de ese contraste (A1) fue "inferior", por −0,008 y al filo (límite superior del intervalo, −0,001). Es un resultado útil para decidir cómo definir la etiqueta, pero la decisión de reemplazar la original corresponde al profesor guía. La corrección no resuelve el problema de fondo de la sección siguiente, porque la etiqueta corregida también se define con los ojos.

El modelo secuencial (GRU) no agregó información sobre el resumen estadístico y rindió peor. Con 41 personas y estímulos breves (mediana de tres ventanas por segmento), la información disponible para aprender dependencias de orden es limitada.

### 8.3 Atención: qué detecta el EEG

Esta sección resume [[Borrador Discusión fisiológica 23-11-2026]], donde está el detalle y la lista de referencias. Las referencias se verificaron en un catálogo bibliográfico (título, autores, revista y DOI), y el 23-11-2026 se contrastaron con las fuentes: 10 en texto completo y 8 solo por resumen. Las frases se ajustaron a lo verificado; el detalle está en `repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/VERIFICACION_REFERENCIAS.md`.

**La huella de los ojos en el EEG.** La regla de no-circularidad se cumple en el nivel de las señales de entrada, pero no garantiza que el EEG sea independiente de los ojos. El ojo se comporta como un dipolo eléctrico, de modo que cada rotación del globo ocular modifica el potencial de los electrodos cercanos (Croft y Barry, 2000; Plöchl, Ossandón y König, 2012). Los parpadeos agregan una deflexión de gran amplitud y máximo frontopolar (Iwasaki et al., 2005; Plöchl, Ossandón y König, 2012). A esto se suma el potencial de espiga sacádica, una descarga breve y de banda ancha de los músculos extraoculares al inicio de cada sacada, que contamina las frecuencias altas (Yuval-Greenberg et al., 2008; Keren, Yuval-Greenberg y Deouell, 2010; Hipp y Siegel, 2013). Los registros de esta tesis muestran ese patrón: el gradiente de amplitud del parpadeo desde los canales frontopolares hacia los posteriores (sección 7.6).

**Cuánto depende la detección de los componentes oculares.** Al retirar tres componentes oculares la AUC baja de 0,681 a 0,621, y un control que retira mucha más varianza casi no la cambia. La caída es de 0,060 sobre los 0,181 que el modelo tiene sobre el azar, cerca de un tercio. La detección por alfa y beta también disminuye, lo que es coherente con la literatura: el dipolo córneo-retinal se concentra en frecuencias bajas (Plöchl, Ossandón y König, 2012), pero el potencial de espiga sacádica abarca aproximadamente de 20 a 90 Hz, con lo que alcanza la parte alta de beta (Keren, Yuval-Greenberg y Deouell, 2010), y la actividad de los músculos frontal y temporal puede ocultar o imitar los ritmos beta y alfa (Goncharova et al., 2003). Esas fuentes no explican por sí solas la caída en alfa; otra posibilidad, que el diseño no separa, es que los tres componentes retirados arrastren actividad no ocular en esas bandas. La cifra de 0,060 se lee como cota inferior, con las reservas de la sección 7.6. La separación por componentes independientes, propuesta para este fin por Jung et al. (2000), es imperfecta en exploración visual libre cuando se aplica con la configuración habitual: puede dejar artefacto residual o retirar actividad cerebral (Dimigen, 2020). Con 16 canales la separación es gruesa, y en estos datos la limpieza fue parcial.

**Qué puede explicar la detección que permanece.** Tras la limpieza el modelo sigue sobre el azar (0,621 con todas las variables, en las 41 personas; 0,55–0,56 con alfa y beta o con canales posteriores). El diseño no permite atribuir ese remanente a una sola fuente. Hay al menos cuatro candidatos: artefacto ocular residual, cuyo patrón espacial y espectral se conserva; actividad muscular de la frente y las sienes, que contamina el EEG en un rango amplio de frecuencias (Goncharova et al., 2003) y que podría acompañar a los movimientos de los ojos, asociación que no se midió; la respuesta visual ligada a cada fijación, o respuesta lambda, que es actividad cerebral pero cuya ocurrencia depende de los movimientos oculares (Dimigen et al., 2011); y la modulación de alfa posterior, relacionada con la atención (Klimesch, 2012), que es el candidato más cercano a un correlato cerebral y el más débil en estos datos. El informe de limpieza agrega una quinta posibilidad, no fisiológica: las variables de calidad de canal que la limpieza no altera. Como la etiqueta se define con la conducta ocular, todas las fuentes covarían con ella y no pueden separarse.

**Un modelo más complejo detecta mejor y también depende de lo ocular.** La red convolucional del tipo EEGNet (Lawhern et al., 2018) supera al modelo de referencia. Al limpiar la señal pierde 0,067 (R3, sin control propio) y su salida se asocia más con el recorrido de la mirada: su detección depende de lo ocular. Su ventaja sobre el modelo de referencia se mantiene con el EEG limpio (+0,028, frente a +0,035 con el original), de modo que los datos no permiten decir que esa ventaja sea ocular. Una explicación plausible de la dependencia, que este trabajo no puso a prueba, es que los artefactos oculares tienen formas de onda características que las variables de potencia por banda promedian y que una red convolucional puede aprender. Otra, igual de plausible y tampoco puesta a prueba, es la escala por persona que recibe la red. La mayor capacidad del modelo no cambia la interpretación de qué se detecta.

En términos del diseño, al menos un tercio de lo que el *Modelo Estudiante* de atención recupera desde el EEG depende de componentes oculares, es decir, de lo **Observado**, y no puede descartarse que el resto también lo sea. Estos datos no permiten afirmar que detecte lo **Atendido** ni que exista un marcador cerebral de atención. El resultado debe presentarse como una detección que depende, al menos en un tercio, de la huella de la conducta ocular en el EEG, sin atribuir el resto a un origen cerebral ni ocular.

### 8.4 Activación: indicio de información temporal de corto alcance

En activación el modelo con historial rinde mejor, y hay apoyo acotado a que esa mejora no se explique solo por la persona. El apoyo más sólido es el contraste registrado antes de correr en la enmienda del 16-11: el historial sin las ventanas de 6 s que promedia la etiqueta supera a un placebo en +0,046 (p Holm 0,004). Ese contraste excluye las ventanas que promedia la etiqueta, pero no el soporte del filtro tónico de la GSR: cerca de un cuarto del peso de la componente dominante de la etiqueta cae antes de esas ventanas (sección 7.3). Por sí solo no separa "la fisiología previa predice la activación posterior" de "la fisiología de un momento se relaciona con la GSR de ese mismo momento, que la etiqueta posterior todavía contiene". El contraste principal se estimó varias veces sobre las mismas 41 personas, con diferencias de AUC entre +0,028 y +0,047, y no todos los intervalos excluyen el cero. El respaldo de la fase 1 del 22-11 sale de un análisis registrado sobre personas ya consultadas, que promedia cinco particiones nuevas cuando el mismo contraste ya se había visto positivo en otras tres particiones el 16-11: es una estimación más precisa de lo ya observado, no una confirmación. El efecto es desigual entre personas (mediana +0,014; mejoran 23 de 41). Tampoco es estable entre subconjuntos de personas, y esa inestabilidad se cruza con la forma en que se eligió la configuración (sección 7.1): las 15 hojas de activación las decidió el modelo con historial, con las 25 personas de entrenamiento, y es en esas 25 donde se concentra el contraste principal (+0,055, frente a +0,001 en las otras 16; con cinco particiones, +0,046 frente a +0,021). El sesgo que eso permite es posible y no está demostrado: la diferencia entre grupos no es significativa con 16 personas y con las particiones originales del cierre V3 el patrón había sido el inverso. El contraste del historial desplazado frente al placebo (+0,035 y +0,064) y el de la GRU (+0,045 y +0,059) son positivos en ambos grupos. Estas comparaciones son descriptivas y no registradas, pero impiden tratar el efecto como una propiedad establecida de la muestra y debilitan el "respaldo" del contraste principal.

En cuanto al alcance, solo la banda de 6 s tiene respaldo. A 12 s el resultado es inconcluso, y desde 24 s el contraste no se distingue del placebo, sin que eso demuestre ausencia: ningún intervalo de 90 % cabe en ±0,02. La ganancia se mantiene dentro del mismo minuto (análisis post hoc), lo que habla contra una deriva lenta de la sesión como única explicación; el control registrado del tiempo de sesión quedó inconcluso.

Lo que el historial aportaría es, con mayor probabilidad, una mejor estimación de un estado que dura segundos: la propia etiqueta se parece a la de 6 s antes. Los resultados no demuestran más que eso. Tampoco descartan una explicación no neural: un movimiento o una respiración profunda pueden producir a la vez una respuesta en la GSR y artefactos de varios segundos en el EEG, la mirada y la pupila. La etiqueta no tiene control de artefactos sobre la señal cruda y el movimiento no se midió. Tres controles quedan inconclusos (el tiempo de sesión como variable, la comparación a igual posición y el contraste con la posición como variable tras la corrección de Holm). Dentro de un mismo estímulo no se demostró que el historial supere al tiempo transcurrido; ese resultado es inconcluso y de poca potencia, y no demuestra ausencia de efecto ni que el aporte se explique por el tiempo transcurrido. Por eso corresponde hablar de un resumen del historial reciente y no de dinámica dentro del estímulo. El resultado por estímulo y la persistencia de la etiqueta son compatibles con que la activación, tal como la define el *Arousal Score*, se comporte como un estado del estímulo completo más que de cada ventana; es una lectura sin contraste propio (C2 es inconcluso).

El efecto es pequeño y su utilidad práctica es baja con las variables actuales: las AUC absolutas van de 0,50 a 0,59, y la ganancia es desigual entre personas.

### 8.5 Activación: por qué el Arousal Score no se detecta desde la ventana actual

Con la ventana actual ningún modelo queda claramente sobre el azar. Antes de las explicaciones fisiológicas hay una más simple que el diseño no descarta: que el *Arousal Score* por ventana refleje poco la activación. No se validó contra ninguna medida externa y no tiene control de artefactos sobre la señal cruda. La fisiología de la respuesta electrodérmica ofrece tres explicaciones compatibles con ese resultado; el detalle está en [[Borrador Discusión fisiológica 23-11-2026]], con la misma advertencia sobre las citas.

- **Origen de la señal.** La conductancia de la piel refleja la actividad de las glándulas sudoríparas, inervadas exclusivamente por el sistema nervioso simpático (Benedek y Kaernbach, 2010). Su regulación central depende de regiones implicadas en la emoción, la atención y la cognición (Critchley, 2002). Si varias de ellas son mediales o profundas, su actividad contribuiría poco a un EEG de superficie de 16 canales; es una hipótesis que este trabajo no puso a prueba y cuya base anatómica falta confirmar en el texto completo.
- **Escala temporal.** Una respuesta de conductancia se atribuye a un evento cuando comienza típicamente entre 1 y 3 s, o entre 1 y 5 s, después de él; sube con rapidez y decae lentamente, de modo que las respuestas sucesivas se superponen (Benedek y Kaernbach, 2010). Una ventana de EEG de 2 s no coincide con la respuesta que define la etiqueta. Esto es coherente con que el historial de los segundos previos mejore la predicción (con respaldo a 6 s).
- **Tipo de relación.** La relación entre el EEG y la conductancia de la piel que documentan estos trabajos es tónica: en reposo, mayor conductancia acompaña a una menor potencia alfa global (Barry et al., 2005, 2007). Esa relación se observó al comparar condiciones (cafeína frente a placebo, ojos abiertos frente a cerrados) y no implica que el estado pueda distinguirse ventana a ventana dentro de una sesión. Además, el *Arousal Score* es relativo a la mediana de cada persona, y es plausible que la navegación web produzca un rango de activación estrecho; este trabajo no lo midió.

En cuanto a la pupila, su diámetro responde a la luz, al enfoque cercano y a la activación o el esfuerzo mental (Mathôt, 2018). Frente a una pantalla cuyo brillo cambia con el contenido, las dos primeras respuestas pueden dominar sobre la tercera.

Estas explicaciones son compatibles con los resultados, pero el diseño no las pone a prueba. El resultado de la red convolucional vale para una arquitectura y una configuración; no permite concluir que el EEG crudo carezca de información sobre la activación.

### 8.6 Fusión y complejidad del modelo

Entre redes MLP, la fusión tardía rindió mejor que la temprana en atención (+0,012 [+0,005; +0,021]), en un contraste secundario sin corrección. Una explicación posible, que no se puso a prueba, es que entrenar un modelo por señal y combinar sus salidas evite que el EEG, con muchas más variables, domine el ajuste conjunto. Con HGB en el cierre V3 el signo fue el contrario (−0,010 [−0,018; −0,003] en entrenamiento, −0,008 en validación y −0,002 en test), y la red MLP con fusión tardía rinde 0,024 menos que el HGB con fusión temprana (0,686 frente a 0,710). En atención la GSR no agrega nada al EEG, de modo que hay poco que fusionar. En activación ninguna estrategia se distinguió. No puede concluirse que la fusión tardía sea mejor en general, y ningún contraste establece qué papel tiene la fusión en el desempeño.

Dos modelos más complejos dieron resultados opuestos. La GRU, que usa el orden de las ventanas, no mejoró la atención y rindió peor que el resumen. La red convolucional sobre la señal cruda sí mejoró la atención. Su detección depende de lo ocular (pierde 0,067 al limpiar, sin control propio), pero su ventaja sobre el HGB se mantiene con el EEG limpio (+0,028, frente a +0,035 con el original). En activación no se demostró que un modelo más complejo ayude: la comparación entre la red y el HGB (R4) es inconclusa.

### 8.7 Implicancias para el diseño

- **La no-circularidad entre señales no asegura independencia fisiológica.** El EEG contiene una copia eléctrica de la conducta ocular con que se construye el *Attention Score*.
- **Sincronía entre equipos.** El desfase de 0,18 a 0,53 s entre el EEG y el seguidor ocular no se corrigió y puede atenuar la relación entre el EEG y las demás señales; ese efecto no se midió. El desfase se agrupa en dos valores (cerca de 0,27 s y cerca de 0,47 s), lo que sugiere una causa sistemática de adquisición que no se investigó (sección 7.6).
- **Para separar lo Observado de lo Atendido** se requiere una etiqueta de atención que no dependa de los ojos (por ejemplo, desempeño en una tarea) o un diseño que mantenga la conducta ocular constante entre condiciones.
- **Para la activación**, la escala temporal de la respuesta electrodérmica sugiere trabajar con ventanas más largas o con la componente tónica, en lugar de ventanas de 2 s.

### 8.8 Limitaciones

- Las 41 personas incluyen las de validación y test, consultadas en etapas anteriores. Los análisis posteriores al 16-11 son exploratorios o dirigidos; ninguno es una confirmación independiente en personas nuevas.
- Las etiquetas son pseudoetiquetas offline, normalizadas con la sesión completa de cada persona, y no se validaron contra una medida externa. La normalización por sesión difiere de la redacción actual del manuscrito, que pide normalizar solo con entrenamiento.
- Varias variables (GSR y pupila normalizadas por sesión; componente tónica con filtro bidireccional) usan información de toda la sesión: el historial es causal por ventana, no por muestra.
- El explicativo de posición del 18-11 y la fase 2 son post hoc; la comprobación estratificada con la posición no fue registrada ni auditada. En la curva temporal y en la fase 2 las reglas de decisión se usan como lectura descriptiva.
- El procesamiento congelado tiene dos imprecisiones conocidas que no se corrigieron: la fracción de muestras con ambos ojos válidos, que es una entrada del *Modelo Estudiante* de activación, se calcula sobre todas las filas de la exportación y queda bajo la validez real; y los eventos oculares se deduplican solo por índice, con lo que se pierde cerca del 0,2 % de las fijaciones (medido en una muestra de 11 personas). Detalle en `documentacion/auditoria_final_23-11-2026/ronda2/AUDITORIA_SECCIONES_PENDIENTES.md`.
- El diseño de evaluación cambió después de un resultado nulo: con las particiones originales el cierre V3 no mostró una ventaja consistente, y el análisis con 41 personas se registró a continuación (secciones 6.3 y 8.1).
- La etiqueta de atención usada (componente principal) se siguió usando tras observar que los modelos la predecían mejor que la de pesos iguales; los análisis no se repitieron con esta última (sección 6.1).
- **Selección de la configuración.** Las 15 hojas de activación se eligieron con la AUC media de los modelos con 1, 8 y 32 ventanas, la elección la decidió el de 32, y las 25 personas de esa búsqueda son 25 de las 41 evaluadas. Los contrastes del HGB con historial hasta 32 se concentran en ellas (+0,055 frente a +0,001 el 16-11). El sesgo a favor del historial es posible y no está demostrado; el historial desplazado frente al placebo y la GRU son positivos en ambos grupos (sección 7.1).
- La etiqueta de activación es en lo esencial el nivel tónico de la GSR relativo a la sesión, y su soporte real excede los 6 s nominales hacia el pasado y hacia el futuro: el contraste "sin las ventanas de la etiqueta" no excluye ese soporte (sección 7.3).
- La etiqueta de atención es, en la práctica, conducta de mirada: la pupila pesa −0,052 en la componente principal. Las variables de fijación suman la duración completa de las fijaciones que tocan la ventana (la suma supera los 2.000 ms en cerca del 28 % de las ventanas etiquetadas y los 3.000 ms en el 4 %), de modo que el soporte de la etiqueta de atención no es de 2 s; en activación esas dos variables son entradas y arrastran mirada posterior a la ventana.
- Ocho filas cumplen dos reglas de decisión a la vez y su rótulo depende de una precedencia que los protocolos no fijan (sección 6.3). Los modelos de historial desplazado reciben una columna no declarada con el número de ventanas (sección 6.2).
- Los resultados de activación se refieren al 53 % de las ventanas que conserva la etiqueta: desde la quinta ventana de cada estímulo (6 s transcurridos), en estímulos suficientemente largos. No describen el inicio de cada página ni los estímulos breves.
- La AUC por persona pesa igual a todas las personas y no se fijó un mínimo de ventanas: P4, la más influyente del contraste principal de activación, conserva 26 ventanas con etiqueta.
- Las personas de un mismo grupo experimental vieron los estímulos en el mismo orden (sección 4.3). La validación cruzada separa personas, no grupos: un modelo puede aprender regularidades ligadas a la secuencia de páginas a partir de otras personas del mismo grupo. No se evaluó dejando grupos completos fuera, y el bootstrap trata a las personas como independientes.
- Los contrastes secundarios no llevan corrección por multiplicidad. La corrección de Holm se aplica dentro de cada etapa y no entre etapas: son doce etapas de análisis sobre las mismas 41 personas. Varias decisiones están pegadas al umbral: A1 y A3 de la etiqueta corregida, la adaptación de activación sin historial y la ventaja de la red (R1).
- La limpieza ocular es parcial, usa la sesión completa de cada persona y elige los componentes con la mirada; su calidad se mide en los mismos datos. Con 11 a 16 canales utilizables, tres componentes son entre el 19 % y el 27 % de las dimensiones y arrastran actividad frontal no ocular.
- El desfase de reloj entre el EEG y el seguidor ocular no se corrigió.
- La GRU y los MLP no tuvieron búsqueda de hiperparámetros. La red convolucional es una sola arquitectura sin búsqueda, y su pérdida al limpiar no tiene control propio.
- En activación las AUC absolutas son bajas (0,50 a 0,59). El modelo por estímulo no es causal y la adaptación a la persona no es utilizable en línea.
- Las AUC estratificadas dentro de un mismo estímulo usan el 2–3 % de los pares y tienen poca potencia en activación: un resultado inconcluso no demuestra ausencia de efecto.
- La comprobación de reproducibilidad del cierre verifica hashes y el orden del registro; no vuelve a entrenar los modelos.

### 8.9 Trabajo futuro

- Confirmar el efecto temporal en activación con personas nuevas y un contraste definido de antemano (el cálculo de tamaño de muestra está en `resultados/protocolo_hipotesis_reintento_06-11-2026/`).
- Definir una etiqueta de atención que no dependa de la conducta ocular, o registrar electrooculograma y más canales para separar mejor la actividad cerebral de la ocular.
- Corregir el desfase entre el EEG y el seguidor ocular y analizar el EEG alineado a las fijaciones.
- Evaluar etiquetas y normalizaciones calculadas solo con información previa, para una versión utilizable en línea.
- Entrenar una red con el filtro de control, para dar a la pérdida de la red un control propio, y un modelo de referencia con variables escaladas por persona, para separar la arquitectura de la escala.
- Evaluar dejando grupos experimentales completos fuera, fijar un mínimo de ventanas por persona y registrar un indicador de movimiento que permita descartar artefactos compartidos entre la GSR y las demás señales.
- Describir la evolución en la sesión con el score continuo y sus intervalos, como compromete el objetivo 6.

La experimentación está cerrada desde el 23-11-2026: reabrirla requiere una decisión explícita y un protocolo registrado antes de correr.

### 8.10 Decisiones abiertas

No hay aprobación registrada del profesor guía sobre los puntos siguientes. Este borrador los usa de forma provisoria y debe revisarse si alguno cambia.

1. **Si "emociones" se presenta como activación (*arousal*).** La GSR solo mide activación simpática, por lo que el texto habla de activación; la redefinición aún no está confirmada.
2. **Si el margen práctico de 0,02 queda como criterio.** De él dependen las etiquetas "efecto relevante" y "nulo concluyente". Con otro margen cambiarían, entre otras, la decisión del contraste principal de atención (límite inferior 0,021) y la de la red (límite inferior 0,023).
3. **Si la etiqueta de atención corregida por posición reemplaza a la original.** Hoy existe como análisis; las etiquetas congeladas son la de atención binaria original y las pseudoetiquetas GSR V2.
4. **El encuadre.** Apoyo parcial a la hipótesis, con la detección de atención por EEG presentada como dependiente, al menos en parte, de la huella ocular, sin atribuir el resto a un origen cerebral ni ocular.
5. **Si se planifica una cohorte nueva** para confirmar el efecto de activación.
6. **Si se aceptan las etiquetas normalizadas con la sesión completa de cada persona** (el manuscrito pide normalizar solo con entrenamiento).
7. **Si el profesor PCA queda como definición del *Attention Score*** (la nota de diseño proponía la fusión igualitaria como principal).

Ninguna de las siete está tomada. Las dos últimas son las de mayor consecuencia si no se aceptan, porque obligan a repetir análisis.

Fuentes del capítulo: `documentacion/Cierre_Experimental_Final_23-11-2026.md`; `documentos/01 Tesis MDS/Escritura/Borrador Discusión fisiológica 23-11-2026.md` (discusión fisiológica y referencias); los `INFORME.md` citados en el Capítulo 7.

## Capítulo 9: Conclusiones

Ver [[Borrador Conclusiones 23-11-2026]].

## Notas relacionadas
- [[Borrador Resultados y Discusión 18-11-2026]]
- [[Borrador Discusión fisiológica 23-11-2026]]
- [[Borrador Conclusiones 23-11-2026]]
- [[Estructura Tesis]]
- [[Problema e hipótesis]]
- [[Resumen Diseño Etiquetas y Modelos]]
