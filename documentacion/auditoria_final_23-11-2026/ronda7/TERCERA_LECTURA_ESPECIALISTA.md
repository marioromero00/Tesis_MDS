# Tercera lectura, como evaluador especialista en neurociencia cognitiva y psicofisiología — ronda 7 (27-11-2026)

Lectura de convergencia. No se editó ningún archivo existente, no se entrenó ni ajustó ningún modelo, no se corrió ningún análisis nuevo y no se hicieron commits. Este informe es el único archivo creado. Las consultas al repositorio fueron de lectura (scripts, informes, CSV y documentación); no se recalculó ninguna cifra de resultados.

Siglas de este informe: SP, RD y CO son los borradores de Secciones pendientes, Resultados y Discusión y Conclusiones del vault (`documentos/01 Tesis MDS/Escritura/`, versiones del 23-11-2026); RE es `presentaciones/avances_tesis_06-11-2026/relato.py` (y su `GUIÓN.md`); EN es `ENSAYO.md` de la misma carpeta. Las rutas sin prefijo son relativas a `repos/Tesis_MDS/`.

Orden de trabajo: primero se leyeron SP, RD, CO, GUIÓN, RE y EN completos y se cerró la lista de objeciones; después se consultó el repositorio para comprobar cada hecho; al final se leyeron los dos informes anteriores (`ronda3/LECTURA_CRITICA_COMITE.md` y `ronda6/SEGUNDA_LECTURA_COMITE.md`) solo para marcar qué es nuevo.

Regla de fuentes: toda afirmación fisiológica nueva que se propone va respaldada por una de las 18 referencias ya verificadas (`VERIFICACION_REFERENCIAS.md`) o marcada **[requiere fuente]**. Las cifras de los textos propuestos salen de los borradores, de un INFORME o de un CSV, con su ruta.

---

## Resumen

**Lo que yo concluiría, en tres frases.** Con un EEG de 16 canales sin electrooculograma, un modelo recupera cuánto se movieron los ojos en una ventana de 2 s: los canales frontales funcionan en la práctica como un electrooculograma, al menos un tercio de la detección pasa por componentes identificables con la mirada y nada en estos datos permite hablar de un correlato cerebral de la atención. El nivel lento de la conductancia de la piel, relativo a la sesión, no se recupera desde 2 s de EEG, mirada y pupila, y la pequeña ganancia del historial es la esperable para una señal lenta y autocorrelada cuyo curso está ligado al inicio de cada estímulo; no es evidencia de dinámica fisiológica. Lo que la tesis aporta a mi área es metodológico y está bien ganado: una pseudoetiqueta ocular no sirve para evaluar un modelo de EEG, y una ventaja "temporal" puede ser el reloj del estímulo.

**¿Convergen los textos?** Casi. Tras tres rondas, el argumento estadístico y de diseño está declarado con un cuidado poco común. Lo que queda sin declarar es de mi especialidad y es poco: **2 objeciones bloqueantes, 10 importantes y 11 menores**. Las dos bloqueantes se arreglan redactando, con información que ya está en el repositorio:

1. **Los textos dicen "navegación web" y no describen los estímulos.** Menos de un tercio de las ventanas con etiqueta de atención son sitios web; el resto son textos, diseños, estímulos numerados e imágenes rotuladas `emotion` y `blur`, cuyo contenido no se describe en ninguna parte. La tabla existe (`resultados/ampliacion_41p_16-11-2026/por_categoria.csv`).
2. **No se muestra ni se declara qué tan "EEG" es el EEG.** No constan referencia, tipo de electrodo ni impedancias; no hay rechazo por amplitud ni comprobación espectral; la saturación es el principal problema de calidad y, en el control de la limpieza, tres componentes no oculares concentran una mediana de 72 % de la varianza. Un resultado negativo (activación) y un remanente "que podría ser cerebral" (atención) se leen distinto según esto, y los borradores no lo dicen.

Entre las importantes, la que más conviene corregir es un hecho mal afirmado: RD 8.4 y EN 27 dicen que "el movimiento no se midió", y los archivos de OpenBCI traen tres canales de acelerómetro y la exportación de Tobii, la posición del mouse (`DOCUMENTACION_DATOS_MDS.md`, secciones 3.2 y 2.5). No se usaron; eso es distinto de que no existan.

**No encontré errores conceptuales graves en la fisiología escrita.** Lo que RD 8.3 y 8.5 afirman sobre el dipolo córneo-retinal, el parpadeo, el potencial de espiga sacádica, la actividad muscular, la respuesta lambda, la inervación simpática de las glándulas sudoríparas, la superposición de respuestas, la pupila y alfa es correcto y no excede a sus fuentes. Los problemas son de nomenclatura ("tónico", "cruda", "GSR"), de un argumento anatómico que el propio texto dice no haber confirmado, y de alternativas que un especialista propondría y que faltan.

---

## A. Fisiología y señales

### A1. Lo que está bien y no requiere cambios

| Afirmación | Dónde | Juicio |
|---|---|---|
| Dipolo córneo-retinal, córnea positiva; cada rotación cambia el potencial en electrodos cercanos | RD 8.3.1; RE lámina 27 | Correcta y bien atribuida (Plöchl et al., 2012; Croft y Barry, 2000) |
| Parpadeo: gran amplitud, máximo frontopolar, deslizamiento del párpado sobre la córnea | RD 8.3.1 | Correcta. Los 148–151 µV frontopolares y el gradiente hacia atrás son plausibles para un parpadeo |
| Potencial de espiga sacádica: breve, banda ancha, músculos extraoculares, 20 a 90 Hz | RD 8.3.1 y 8.3.2 | Correcta y sin exceder a Keren et al. (2010) |
| Actividad muscular frontal y temporal; "esta asociación no se midió" | RD 8.3.3 | Bien matizada |
| Respuesta lambda como actividad cerebral ligada a la fijación | RD 8.3.3 | Correcta (Dimigen et al., 2011) |
| La ICA separa a lo sumo tantas fuentes como canales; con 16 la separación es gruesa | RD 8.3.2 | Correcta y bien atribuida a Jung et al. (2000), no a Dimigen |
| Glándulas sudoríparas con inervación exclusivamente simpática; superposición de respuestas; ventana de 1–3 o 1–5 s | RD 8.5 | Correcta (Benedek y Kaernbach, 2010) |
| Pupila: luz, enfoque cercano, activación o esfuerzo | RD 8.5; SP 4.6.5 | Correcta (Mathôt, 2018) |
| Relación tónica alfa–conductancia, observada entre condiciones | RD 8.5 | Correcta y bien acotada (Barry et al., 2005, 2007) |
| Cyton + Daisy a 125 Hz; ±187.500 µV como límite del equipo y signo de desconexión | SP 4.6.1 y 5.3 | Correcto |
| Filtro por ventana: no mezcla ventanas, deja efectos de borde y mala resolución en lo lento | SP 4.7 | Declarado. Precisión menor en m11 |
| Filtro tónico bidireccional y normalización por sesión: soporte real mayor que el nominal | SP 4.5.2, 4.6.3; RD 6.1 | Muy bien declarado, con cifras |
| Pupila sin corrección por luminancia | SP 4.6.5 | Declarado |
| Desfase de 0,18 a 0,53 s entre EEG y seguidor ocular, sin corregir, dirección y dos grupos | SP 4.6.1; RD 7.8 | Bien declarado. Falta un dato que consta (m3) |

### A2. Lo que un psicofisiólogo objetaría

Se detalla en las objeciones numeradas de la sección "Objeciones". En síntesis:

- **"Nivel tónico" no es lo que se calculó** (O4). Un pasa-bajos de 0,05 Hz sobre la señal estandarizada no entrega el nivel de conductancia: deja dentro la acumulación de las colas lentas de las respuestas, que es justamente la superposición que describe la referencia que el texto cita.
- **El conteo de SCR no es un conteo de respuestas** (O4): máximos locales de la fásica dentro de una ventana de 2 s, con umbral en unidades estandarizadas por sesión. En 9 de las 41 personas esas variables no varían.
- **La limpieza por ICA no se dirigió al potencial de espiga sacádica**, y los puntajes "oculares" son bajos (O5).
- **La caída de alfa y beta tiene explicaciones más simples** que las que el texto da (O6).
- **Un argumento anatómico sin confirmar** se mantiene con disculpa (O11).
- **"Señal cruda"** designa una señal filtrada, escalada por persona y recortada (m2). **"GSR"** es un término en desuso (m1).

### A3. ¿Es defendible el preprocesamiento y están declarados sus efectos?

| Paso | ¿Defendible? | ¿Efecto declarado? |
|---|---|---|
| Ventanas de 2 s con paso de 1 s | Sí para mirada y EEG; cortas para una señal electrodérmica lenta | Sí (RD 8.5, 8.7) |
| EEG: tendencia lineal, *notch* 50 Hz, pasa-banda 1–45 Hz por ventana, Welch | Aceptable para variables de potencia | Sí, salvo que Welch usa segmentos de 1 s (m11) |
| EEG: sin re-referenciar, sin rechazo por amplitud, referencia y electrodos no documentados | Solo si se declara | **No** (O2) |
| EEG: canal ausente por saturación, repetición plana o huecos; umbral de sesión de 30 % | Permisivo | Sí (SP 5.3) |
| 125 Hz con contenido hasta 45 Hz | Sí. Queda la duda del filtro antisolapamiento del equipo en modo Daisy | No; solo como pregunta de defensa (F13), **[requiere fuente]** |
| GSR: estandarización por sesión, tónica por pasa-bajos bidireccional, fásica por resta | Es una aproximación, no una descomposición validada | A medias (O4) |
| GSR: SCR por máximos locales en 2 s | Débil | **No** (O4) |
| GSR: sin detector de artefactos, unidad no declarada | Solo si se declara | Sí |
| Mirada: clasificación I-VT de la exportación, 60 Hz, sin interpolar pérdidas | Aceptable | A medias: faltan parámetros del filtro, límite de 60 Hz y efecto de los parpadeos (O7, O9) |
| Pupila: media de ojos, interpolación de hasta 12 filas, estandarización por sesión | Aceptable; la pupila casi no pesa en la etiqueta | A medias (m5) |
| Normalización por sesión de etiquetas y de variables | Solo offline | Sí, repetidamente |

---

## B. Constructos

**Juicio general.** La cautela es la debida y es constante. RD 6.1 dice sin rodeos que "alta" es una mirada más quieta que lo habitual en la persona y que "no designa mayor atención en ningún sentido validado"; que el *Arousal Score* es un nivel lento relativo a la sesión y que no hay medida externa. La distinción Observado/Atendido está en SP 4.6.4, RD 6.1, 8.2, 8.3.3 y 8.7, CO 9.3 y RE láminas 27 y 31. **No encontré ningún pasaje que lea la detección por EEG como cerebral.** No encontré ninguno que llame emoción a la activación en los tres borradores (el título "4.5.2 Definición Emoción" está advertido).

Quedan cuatro puntos:

1. **Falta decir que el sentido de la etiqueta tampoco está establecido** (O8, importante). El texto niega la validación, pero conserva "alta" y "baja", y un lector de mi área preguntará por qué la mirada quieta sería más atención y no menos.
2. **Los parpadeos entran a la etiqueta por pérdida de mirada** (O7, importante): un constructo "mirada" que en parte es "ojos cerrados".
3. **Dos frases de la presentación leen la etiqueta como estado** (m7, menor): "La etiqueta dice si P22 está más activada que de costumbre" (RE lámina 15 y EN) y "la proporción de ventanas con atención alta cae a 37 %" (EN, guion de la lámina 22).
4. **"Detección de atención" como abreviatura** (m9, menor). Títulos y tablas dicen "atención" y "activación" por *Attention Score* y *Arousal Score*. Basta una frase de convención.

Sobre "activación": la frase "la GSR registra activación simpática" (SP 4.5.2) es aceptable. Conviene no ir más allá: la conductancia de la piel también cambia con la temperatura, la hidratación del contacto y el movimiento, y el nivel relativo a la sesión es especialmente sensible a esas derivas. `EDA_GSR.md` ya lo advierte ("contacto de electrodos, temperatura, humedad o configuración"); los borradores solo hablan de "deriva lenta de la señal". Está cubierto en O10.

---

## C. Interpretaciones alternativas que faltan

| Resultado | Lo que el texto considera | Lo que un especialista agregaría | Objeción |
|---|---|---|---|
| Detección de la etiqueta ocular desde el EEG | Dipolo, parpadeo, espiga, músculo, lambda, alfa, variables de calidad | (a) Los parpadeos como vía directa: cortan las fijaciones de la etiqueta y dan la mayor deflexión del EEG. (b) Las potencias relativas llevan la potencia lenta en el denominador. | O7, O6 |
| Caída al quitar componentes oculares | Selección con la mirada; control no igualado; arrastre de actividad frontal | (c) Los puntajes oculares son bajos (medianas 0,38; 0,23; 0,17; 0,13): el tercer componente puede no ser ocular. (d) El criterio, entre 1 y 15 Hz y con un seguidor de 60 Hz, no puede identificar el potencial de espiga. | O5 |
| Caída de alfa y beta al limpiar (L4) | Espiga en beta alta, músculo, arrastre no ocular | (e) El aumento de potencia del dipolo llega hasta cerca de 10 Hz (Plöchl) y toca alfa baja. (f) Fuga espectral y bordes de transitorios de 150 µV en ventanas de 2 s filtradas una a una. | O6 |
| Remanente tras la limpieza | Cuatro candidatos fisiológicos y las variables de calidad | (g) Espiga sacádica no tratada, como candidato explícito. (h) No hay evidencia de que el registro contenga actividad cerebral medible; el candidato "alfa posterior" presupone un EEG válido. | O5, O2 |
| Patrón de la etiqueta al inicio de cada página | Reorientación, cálculo de fijaciones, composición por largo | (i) Tiempo de carga o pantalla en blanco al inicio. (j) Fase inicial de exploración con fijaciones breves y sacadas amplias **[requiere fuente]**. (k) Desplazamiento de la página: seguimiento ocular mal clasificado por un filtro de velocidad **[requiere fuente]**. (l) Mezcla de tipos de estímulo muy distintos. | O9, O1 |
| Efecto del historial en activación | Estado que dura segundos, soporte del filtro, misma página, deriva, movimiento o respiración | (m) Respuesta de conductancia al cambio de estímulo: curso de la GSR ligado al inicio de cada página (Benedek y Kaernbach, 2010). (n) Derivas lentas no neurales comunes a varias señales. (o) El movimiento sí quedó registrado y no se usó. | O10, O3 |
| No detección de la activación desde la ventana actual | Etiqueta poco válida; regiones profundas; escala temporal; relación tónica; rango estrecho; pupila dominada por la luz | (p) Calidad del EEG como registro cerebral. (q) El nivel lento relativo a la sesión puede ser en buena parte deriva no neural. (r) El argumento de las regiones profundas contradice el párrafo de Barry. | O2, O11 |
| Ventaja de la red sobre la señal sin variables | Formas de onda del artefacto; escala por persona y canal | (s) La red combina canales con signo y puede formar derivaciones tipo electrooculograma (por ejemplo, la diferencia entre los frontales laterales); las variables por canal pierden el signo. | O12 |

Un dato que apoya la lectura ocular y que el texto no usa: la etiqueta se predice peor en textos (0,60; RD 7.12). En la lectura las sacadas son pequeñas y regulares **[requiere fuente; posiblemente Dimigen et al., 2011]**, y dejarían menos huella en el EEG (m10).

---

## D. Lo que falta para juzgar el trabajo, y dónde está

"Consta" significa que lo encontré en el repositorio o en el vault; "en la tesis" indica si ya está en los borradores.

### EEG

| Dato | ¿Consta? | Ruta | ¿En la tesis? |
|---|---|---|---|
| Equipo: OpenBCI Cyton con Daisy, 16 canales | Sí | `documentos/01 Tesis MDS/Analisis de Datos/DOCUMENTACION_DATOS_MDS.md` §3.2 (cabecera `%Board = OpenBCI_GUI$BoardCytonSerialDaisy`) | Sí (SP 4.6.1) |
| Frecuencia: 125 Hz nominal; mediana efectiva 125,14 Hz | Sí | `resultados/eda/eeg/eeg_resumen.json` | Sí (SP 5.3) |
| Programa de adquisición: OpenBCI GUI (TXT) y BrainFlow (CSV) | Sí | `DOCUMENTACION_DATOS_MDS.md` §3 | Parcial (SP 4.6.1) |
| Montaje | No documentado; compatible con el montaje por defecto (Fp1, Fp2, C3, C4, P7, P8, O1, O2, F7, F8, F3, F4, T7, T8, P3, P4) | `resultados/montaje_ocular_41p_23-11-2026/INFORME.md` | Dice "montaje por defecto" sin listar las 16 posiciones: **agregar la lista** |
| Referencia y tierra | **No consta** | `DOCUMENTACION_DATOS_MDS.md` §3.2: "la ubicación y referencia de los electrodos no están documentadas" | **No lo declara** (O2) |
| Tipo de electrodo (seco o con gel; gorro o casco), impedancias, ganancia | **No consta** | — | **No lo declara** (O2). El límite de ±187.500 µV sí consta |
| Re-referencia | No se aplica | `scripts/eeg_por_canal_v2.py`, `extract_window` | **No lo declara** |
| Rechazo de ventanas por amplitud | No se aplica | Ídem (solo saturación ≥ 180.000 µV, repetición plana, huecos, muestras) | **No lo declara** |
| Comprobación espectral (máximo alfa, forma del espectro) | **No consta** | `EDA_EEG.md`: "Tampoco estima potencia por bandas"; "no sustituye revisión de montaje, impedancias, espectro" | No. Requeriría un descriptivo nuevo |
| Saturación global | Sí: mediana de 27,9 % de canal-muestras en el límite, sobre las 104 sesiones | `resultados/eda/eeg/eeg_resumen.json` (`rail_pct_median`) | No (SP 5.3 da solo las sesiones excluidas y dos conservadas) |
| Canales utilizables por persona: 11 a 16, mediana 15; más pérdidas en P4, O1, P7 y P3 | Sí | `montaje_ocular_41p_23-11-2026/INFORME.md`, "Calidad" | Parcial ("11 a 16") |
| Acelerómetro de tres ejes en el archivo de EEG | Sí, las columnas; **contenido no comprobado** | `DOCUMENTACION_DATOS_MDS.md` §3.2 ("3 canales de acelerómetro") | **No; y RD 8.4 dice que el movimiento no se midió** (O3) |
| Detalle de la ICA: FastICA, tantos componentes como canales utilizables, ajuste sobre la sesión continua filtrada entre 1 y 45 Hz con *notch*, sin las muestras a menos de 1 s de una saturación; puntaje ocular entre 1 y 15 Hz; k = 3 fijo, sin umbral | Sí | `scripts/limpieza_ocular_41p.py` (docstring y `fit_person`); `resultados/limpieza_ocular_41p_23-11-2026/protocolo.json` | **No** (O5) |
| Puntajes oculares medianos: 0,38; 0,23; 0,17; 0,13; control 0,06 como máximo | Sí | `resultados/limpieza_ocular_41p_23-11-2026/INFORME.md` | **No** (O5) |
| Definición de parpadeo (50 a 500 ms con ambos ojos no válidos); 19 a 393 por persona | Sí | `scripts/montaje_ocular_41p.py`; su INFORME | **No** (m4) |
| Las tres referencias oculares dan el mismo desfase | Sí | `montaje_ocular_41p_23-11-2026/INFORME.md`, Resultado 2 | **No** (m3) |
| Acoplamiento horizontal mayor en canales del lado derecho | Sí | Ídem, Resultado 1 | No. Sería esperable con una referencia a la izquierda; es una conjetura mía que solo sirve como pista para pedir la documentación |

### Seguidor ocular y pupila

| Dato | ¿Consta? | Ruta | ¿En la tesis? |
|---|---|---|---|
| Programa: Tobii Pro Lab, versión 1.241.54542; filtro `Tobii I-VT (Fixation)` | Sí | `DOCUMENTACION_DATOS_MDS.md` §2.1 | Parcial (falta la versión) |
| Modelo del seguidor ocular | **No consta** | — | No |
| Frecuencia: cerca de 60 Hz | Sí | SP 4.6.4 | Sí |
| Parámetros del filtro I-VT (umbral de velocidad, fusión y descarte) | **No consta** en notas | — | No (O9) |
| Pantalla: 1920 × 1080 píxeles; latencia de monitor configurada, 10 ms | Sí | `DOCUMENTACION_DATOS_MDS.md` §2.1 | **No: agregar** |
| Tamaño físico de la pantalla y distancia de observación | No consta escrito; derivable de las columnas `Eye position … (DACSmm)` y de las exactitudes en mm y píxeles | `DOCUMENTACION_DATOS_MDS.md` §2.3 y §2.4 | No |
| Calibración y validación por grabación (exactitud y precisión en mm, grados y píxeles) | Sí en la exportación cruda (columnas 19 a 36); **no hay tabla resumen por persona** | `DOCUMENTACION_DATOS_MDS.md` §2.3 (ejemplo: validación 0,60°; calibración 5,75°, "debe revisarse") | No. Un resumen exigiría leer la exportación |
| Validez de mirada y de pupila por persona | Sí | `resultados/eda/eye_pupil/calidad_por_participante.csv` | Sí (SP 5.3) |
| Diámetro pupilar: mediana 3,0 mm; percentiles 5 y 95, 2,4 y 3,9 mm (columna filtrada, muestra determinista) | Sí | `resultados/eda/eye_pupil/resumen_numerico.csv` | No. Es el único indicio disponible del régimen de luz |
| Iluminación de la sala | **No consta** | — | No |
| Posición del mouse, área visible del navegador, alto de la página | Sí, las columnas | `DOCUMENTACION_DATOS_MDS.md` §2.5 | No (O3, O9) |

### Actividad electrodérmica

| Dato | ¿Consta? | Ruta | ¿En la tesis? |
|---|---|---|---|
| Frecuencia: cerca de 15 Hz | Sí | `EDA_GSR.md`; `configuracion_efectiva.json` | Sí |
| Equipo, tipo de electrodo, sitio de registro, mano | **No consta** | — | No |
| Unidad | **No consta** (valor de ejemplo 1,888) | `DOCUMENTACION_DATOS_MDS.md` §2.6; `EDA_GSR.md` | Sí, declarado |
| Si la mano de los electrodos usaba el mouse | **No consta** | — | No |
| Temperatura de la sala | **No consta** | — | No |
| Implementación: Butterworth de orden 2 a 0,05 Hz con `filtfilt`; fásica por resta; SCR con `find_peaks` dentro de la ventana, prominencia 0,05 | Sí | `scripts/preprocesamiento_secuencial.py` (`prepare_gsr`, `modality_features`) | Sí, sin sus consecuencias (O4) |

### Estímulos, tarea y participantes

| Dato | ¿Consta? | Ruta | ¿En la tesis? |
|---|---|---|---|
| Tipos de estímulo y ventanas por tipo | Sí | `resultados/ampliacion_41p_16-11-2026/por_categoria.csv`; regla en `scripts/ampliacion_41p.py` (`category`) | **No** (O1) |
| Contenido de los estímulos numerados, `emotion` y `blur` | **No consta** | — | No |
| Número de estímulos | 116 solo en RE lámina 4. En una consulta de lectura de `caracteristicas_multimodales.csv` conté 95 nombres distintos tras quitar el sufijo de repetición; no es una cifra auditada: **conviene comprobar el 116** | — | No |
| Duración de los estímulos | Derivable de la tabla de ventanas; solo consta "mediana de tres ventanas por segmento" | `resultados/enfoques_41p_22-11-2026/INFORME.md` | Parcial |
| Si los sitios web eran navegables (desplazamiento, clics) o capturas | **No consta**; comprobable con las columnas del navegador | `DOCUMENTACION_DATOS_MDS.md` §2.5 | No |
| Instrucciones y tarea | **No consta**. Hay estímulos `Bienvenida` y `Explicacion1` | `caracteristicas_multimodales.csv`, columna `stimulus` | No |
| Duración de la sesión | Sí (EEG: 13,4 min en promedio) | `resultados/eda/eeg/eeg_resumen_sesiones.csv`; `resultados/sincronizacion/inventario_tobii.csv` | Sí |
| Edad, sexo, corrección visual, lateralidad, cafeína, consentimiento, ética | **No consta** | — | Declarado como pendiente (SP 4.3) |

---

## Objeciones

Para cada una: gravedad, ubicación, texto actual, texto propuesto y estado frente a los dos informes anteriores. Los textos propuestos no cierran ninguna de las siete decisiones abiertas ni afirman aprobación del profesor guía.

### Bloqueantes

#### O1. "Navegación web" sin descripción de los estímulos: menos de un tercio de las ventanas son sitios web

- **Qué pasa.** La hipótesis, el título de la presentación y RD hablan de navegación web. RD 6.3 define estímulo como "un sitio web, un texto o un diseño". La tabla por categoría del propio repositorio dice otra cosa. De las 22.176 ventanas con etiqueta de atención, 6.423 son de sitios web, 6.637 de estímulos identificados solo con un número, 4.082 de diseños, 2.255 de textos, 1.792 de imágenes `emotion`, 891 de imágenes `blur` y 96 de instrucciones. De las 11.796 de activación, 5.457 son de sitios web. Los sitios web son cinco (`scripts/ampliacion_41p.py`: `Meg`, `diario_financiero`, `temu`, `Despega`, `Nint`).
- **Por qué es bloqueante.** (i) Un lector de mi área no puede interpretar una etiqueta de mirada ni una de conductancia sin saber qué se estaba mirando: leer un texto, explorar una imagen y recorrer un sitio producen conductas oculares distintas. (ii) Los resultados no describen "navegación web" sino una batería mixta, y el texto no lo dice. (iii) Hay estímulos rotulados `emotion`. Si son imágenes afectivas con valores normativos de activación, son el criterio externo que SP 4.5.2 dice que no existe; si no lo son, hay que decirlo. No se puede dejar sin nombrar en una tesis cuya hipótesis dice "emociones". (iv) La nota de trabajo de RD 6.3 dice que el párrafo no se agregó porque las cifras "no están comprobadas en un informe": los conteos por categoría sí están en un CSV de resultados.
- **Texto actual (RD 6.3, "Términos"):** "*Estímulo* es cada página o imagen que se presenta (un sitio web, un texto o un diseño); "página" se usa como sinónimo al hablar de lo que la persona ve."
- **Texto propuesto:** "*Estímulo* es cada página o imagen que se presenta. Por su nombre en la exportación se distinguen siete categorías: sitios web, textos, diseños, estímulos identificados solo con un número, imágenes rotuladas `emotion`, imágenes rotuladas `blur` e instrucciones. El contenido de las cuatro últimas, la tarea y las instrucciones no están documentados en las notas y deben pedirse al proyecto. De las 22.176 ventanas con etiqueta de atención, 6.423 corresponden a sitios web, 6.637 a estímulos numerados, 4.082 a diseños, 2.255 a textos, 1.792 a imágenes `emotion`, 891 a imágenes `blur` y 96 a instrucciones; de las 11.796 con etiqueta de activación, 5.457 corresponden a sitios web (`resultados/ampliacion_41p_16-11-2026/por_categoria.csv`). "Navegación web" nombra, entonces, el contexto del experimento y no el contenido de la mayoría de las ventanas. "Página" se usa como sinónimo de estímulo al hablar de lo que la persona ve."
- **Texto propuesto (RD 8.8, "Etiquetas", viñeta nueva):** "Menos de un tercio de las ventanas con etiqueta de atención corresponde a sitios web (6.423 de 22.176); el resto son textos, diseños, estímulos numerados e imágenes. Los resultados describen la sesión completa de estímulos y no solo la navegación web; por tipo de estímulo solo hay un descriptivo (sección 7.12)."
- **Texto actual (SP 4.5.2, "Límites"):** "No existe una medida externa de activación contra la cual validar la etiqueta, y la unidad física de la GSR no está declarada en la exportación."
- **Texto propuesto:** "No existe una medida externa de activación contra la cual validar la etiqueta, y la unidad física de la GSR no está declarada en la exportación. La sesión incluye imágenes rotuladas `emotion`, cuyo contenido y propósito no están documentados en las notas: si tuvieran valores normativos de activación serían un criterio externo posible, que aquí no se usó. Corresponde a la decisión abierta sobre validación externa."
- **Texto actual (RE lámina 4, dato):** "116 estímulos: sitios como Diario Financiero, Temu o Despegar, textos y diseños"
- **Texto propuesto:** "116 estímulos: cinco sitios web (como Diario Financiero, Temu o Despegar), textos, diseños e imágenes; los sitios web son 6.423 de las 22.176 ventanas de atención" (y comprobar el 116; ver sección D).
- **Estado:** ya planteada por el segundo lector (D4, "¿Cómo son los estímulos?") y **no resuelta**: quedó como nota de trabajo en RD 6.3. Son nuevos la proporción de sitios web, la existencia de las imágenes `emotion` y `blur` y su relación con la validación externa.

#### O2. No se declara la calidad del EEG como registro de actividad cerebral

- **Qué pasa.** Los borradores declaran que el montaje no está documentado. No declaran que tampoco constan la referencia, la tierra, el tipo de electrodo ni las impedancias; que no se re-referencia; que no hay rechazo de ventanas por amplitud; y que nunca se comprobó que el espectro tenga forma de EEG (`EDA_EEG.md` lo dice expresamente: no se estimó potencia por bandas porque "un espectro de canales clavados estaría dominado por el defecto de adquisición"). Lo que sí consta apunta a un registro difícil: la mediana de canal-muestras en el límite del equipo es 27,9 % sobre las 104 sesiones (`eeg_resumen.json`), se conservan sesiones con 25 % y 26 % de saturación (SP 5.3), y en el control de la limpieza tres componentes no oculares concentran una mediana de 72 % de la varianza (RD 7.9).
- **Por qué es bloqueante.** Dos lecturas de la tesis dependen de esto y no lo dicen. La primera: "no se demostró que el EEG de la ventana actual detecte el *Arousal Score*" (CO 9.3) se lee como un dato sobre el EEG y la activación, y puede ser un dato sobre este registro. La segunda: el candidato "modulación de alfa posterior" del remanente (RD 8.3.3) presupone que hay alfa medible. El 72 % se usa como fortaleza del control ("quita veinte veces más varianza"), y lo es; pero también dice que la señal está dominada por fuentes de gran amplitud que nadie caracterizó. Es lo primero que preguntaría un evaluador de EEG, y hoy no hay respuesta escrita.
- **Texto actual (SP 4.7):** "No se asigna anatomía a los canales en esta extracción: el montaje de los electrodos no está documentado."
- **Texto propuesto:** "No se asigna anatomía a los canales en esta extracción: el montaje de los electrodos no está documentado. Tampoco constan la referencia y la tierra del registro, el tipo de electrodo ni las impedancias. La señal se analiza con la referencia de adquisición, sin re-referenciar. No se rechazan ventanas por amplitud: un canal solo se marca ausente por saturación, repetición plana, pocas muestras o huecos, de modo que las ventanas con artefactos de gran amplitud que no alcanzan el límite del equipo permanecen en el análisis. No se comprobó que el espectro de la señal tenga las propiedades esperables de un EEG, por ejemplo un máximo en la banda alfa en los canales posteriores."
- **Texto actual (RD 7.9):** "Quitar tres componentes no oculares, con una mediana de 72 % de la varianza, la deja en 0,674 (caída de 0,007 [−0,001; +0,015])."
- **Texto propuesto:** agregar a continuación: "Esos tres componentes no se caracterizaron. Que tres componentes de entre 11 y 16 concentren esa fracción de la varianza indica que la señal registrada está dominada por fuentes de gran amplitud de naturaleza desconocida, que no informan sobre la etiqueta."
- **Texto actual (RD 8.5, primer párrafo):** "No se validó contra ninguna medida externa y no tiene control de artefactos sobre la señal cruda."
- **Texto propuesto:** agregar a continuación: "Hay una explicación equivalente del lado de la entrada: la calidad del EEG como registro de actividad cerebral no está establecida (sección 4.7), de modo que el resultado no permite distinguir entre "el EEG no informa sobre el *Arousal Score*" y "este registro no lo permite"."
- **Texto propuesto (RD 8.8, "Señales y procesamiento", viñeta nueva):** "No constan la referencia, el tipo de electrodo ni las impedancias del EEG; no se rechazaron ventanas por amplitud ni se comprobó la forma del espectro. La saturación es el principal problema de calidad del registro (sección 5.3). Los resultados sobre el EEG valen para este registro."
- **Texto propuesto (CO 9.5, tercer punto, al final):** "No constan la referencia ni las impedancias del EEG y no se comprobó su calidad como registro de actividad cerebral, lo que condiciona tanto el remanente de atención como el resultado negativo de activación."
- **Estado:** **nueva**. Los informes anteriores trataron el montaje sin documentar (declarado) y el filtrado por ventana (I14, bien resuelto), no esto.

### Importantes

#### O3. "El movimiento no se midió" no es exacto: hay acelerómetro y posición del mouse

- **Qué pasa.** `DOCUMENTACION_DATOS_MDS.md` §3.2 lista "3 canales de acelerómetro" en cada archivo de OpenBCI, y §2.5, la "posición X/Y del mouse" y del área visible del navegador en la exportación de Tobii. Ningún script los usa (búsqueda de `accel` en `scripts/`: sin resultados en el procesamiento). No comprobé su contenido.
- **Texto actual (RD 8.4):** "La etiqueta no tiene control de artefactos sobre la señal cruda y el movimiento no se midió."
- **Texto propuesto:** "La etiqueta no tiene control de artefactos sobre la señal cruda y el movimiento no se analizó: los archivos del equipo de EEG traen tres canales de acelerómetro y la exportación del seguidor ocular, la posición del mouse, pero ninguno se usó ni se comprobó su contenido."
- **Texto actual (RD 8.9):** "…fijar un mínimo de ventanas por persona y registrar un indicador de movimiento que permita descartar artefactos compartidos entre la GSR y las demás señales."
- **Texto propuesto:** "…fijar un mínimo de ventanas por persona y usar un indicador de movimiento (el acelerómetro del equipo de EEG, cuyo contenido falta comprobar, o un registro dedicado) para descartar artefactos compartidos entre la GSR y las demás señales."
- **Texto actual (EN 27):** "La etiqueta no tiene detector de artefactos sobre la GSR cruda y no medí movimiento."
- **Texto propuesto:** "La etiqueta no tiene detector de artefactos sobre la GSR cruda y no analicé movimiento: el archivo del EEG trae tres canales de acelerómetro y Tobii registra la posición del mouse, pero no los usé ni comprobé qué contienen."
- **Estado:** ya planteada por el primer lector (I16, D7) y **mal resuelta** en este punto: la corrección introdujo una afirmación que el repositorio contradice. El dato del acelerómetro y del mouse es nuevo.

#### O4. Lo que se llama "nivel tónico" es la componente lenta de la señal, y el conteo de SCR no es un conteo de respuestas

- **Qué pasa.** `prepare_gsr` aplica un Butterworth de orden 2 a 0,05 Hz con `filtfilt` y define la fásica como la señal menos esa salida. Eso no separa el nivel de base de las respuestas: como las respuestas sucesivas se superponen y decaen lentamente (Benedek y Kaernbach, 2010, que es la referencia que el texto cita), su acumulación queda dentro de la banda lenta. Por otra parte, las SCR se cuentan como máximos locales de la fásica dentro de cada ventana de 2 s (`find_peaks` con prominencia 0,05 en unidades estandarizadas por sesión), sin criterio de amplitud en unidades físicas ni de tiempo de subida. Una respuesta dura más que la ventana. El resultado es coherente con una medida débil: el número y la prominencia de las SCR ordenan la etiqueta con AUC 0,522 y no varían en 9 de las 41 personas (RD 6.1: "en las 32 personas en que esas variables varían").
- **Consecuencia.** RD 8.5 y EN 7 oponen "parte fásica, que pesa poco" a "nivel tónico". La oposición es más fuerte de lo que el cálculo permite: las respuestas pesan poco como componente fásica, pero entran en la componente lenta. Y que el *Arousal Score* sea "en lo esencial tónico" puede deberse en parte a que la medida fásica es pobre.
- **Texto actual (RD 6.1):** "En la práctica el *Arousal Score* es, en lo esencial, el nivel tónico de la GSR relativo a la sesión."
- **Texto propuesto:** "En la práctica el *Arousal Score* es, en lo esencial, la componente lenta de la GSR (por debajo de 0,05 Hz) relativa a la sesión, que aquí se llama nivel tónico. Incluye el nivel de base y la acumulación de las colas lentas de las respuestas, que el filtro no separa (sección 4.6.3)."
- **Texto propuesto (SP 4.6.3, párrafo nuevo antes de "Dos límites condicionan el uso posterior"):** "Dos precisiones de nomenclatura. La componente que aquí se llama tónica es la parte de la señal por debajo de 0,05 Hz; no es el nivel de conductancia que entregaría una descomposición por deconvolución, porque las respuestas sucesivas se superponen y sus colas lentas quedan dentro de esa banda (Benedek y Kaernbach, 2010). Y el número de SCR es un conteo de máximos locales de la componente fásica dentro de cada ventana de 2 s, con un umbral en unidades estandarizadas por sesión y sin criterio de amplitud en unidades físicas ni de tiempo de subida: no se validó contra un método de referencia. En 9 de las 41 personas el número y la prominencia de las SCR no varían (sección 6.1)."
- **Texto actual (RD 8.5, "Escala temporal"):** "Esa latencia describe la parte fásica, que pesa poco en la etiqueta usada: el *Arousal Score* es, en lo esencial, el nivel tónico (sección 6.1), que se obtiene con un filtro pasa-bajos de 0,05 Hz aplicado hacia atrás y hacia adelante y cambia en decenas de segundos."
- **Texto propuesto:** "Esa latencia describe las respuestas individuales. Como componente fásica pesan poco en la etiqueta usada, pero no están ausentes de ella: al superponerse, su acumulación entra en la componente lenta. El *Arousal Score* es, en lo esencial, esa componente (sección 6.1), que se obtiene con un filtro pasa-bajos de 0,05 Hz aplicado hacia atrás y hacia adelante y cambia en decenas de segundos."
- **Estado:** **nueva**. El primer lector nombró de paso el "umbral de prominencia fijo" (I5) y el segundo trató latencia frente a nivel tónico (C3, bien resuelta); ninguno objetó la descomposición ni el conteo.

#### O5. La limpieza ocular no se dirigió al potencial de espiga sacádica, y los puntajes "oculares" son bajos

- **Qué pasa.** Según `scripts/limpieza_ocular_41p.py`, el puntaje ocular de cada componente es su correlación máxima, entre 1 y 15 Hz, con la mirada horizontal, la vertical o los parpadeos del seguidor ocular; se quitan los tres de mayor puntaje sin umbral. El INFORME da las medianas: 0,38; 0,23; 0,17 y 0,13 para los componentes 1 a 4, y 0,06 como máximo en el control. RD no trae ni la banda ni los puntajes. Dos consecuencias. (i) Con correlaciones de 0,17, "componente ocular" es un orden y no una identificación: el tercero puede no ser ocular, lo que refuerza la segunda objeción de RD 7.9. (ii) Un criterio entre 1 y 15 Hz, con un seguidor de 60 Hz, no puede identificar por construcción el potencial de espiga sacádica, que ocupa de 20 a 90 Hz (Keren et al., 2010) y cuya corrección mejora cuando el ajuste se hace sobre datos en que esos potenciales están sobrerrepresentados (Dimigen, 2020). El texto describe esa fuente en 8.3.1 y no dice que la limpieza la dejó intacta.
- **Texto actual (RD 6.2):** "La limpieza ocular se hizo por persona con análisis de componentes independientes (ICA): cada componente recibe un puntaje ocular (su correlación máxima con la mirada horizontal, la mirada vertical o los parpadeos del seguidor ocular) y se quitan los tres de mayor puntaje."
- **Texto propuesto:** "La limpieza ocular se hizo por persona con análisis de componentes independientes (ICA, algoritmo FastICA), ajustado sobre la sesión completa filtrada entre 1 y 45 Hz, con tantos componentes como canales utilizables y sin las muestras cercanas a una saturación. Cada componente recibe un puntaje ocular: su correlación máxima, entre 1 y 15 Hz, con la mirada horizontal, la mirada vertical o los parpadeos del seguidor ocular (un parpadeo es aquí un tramo de 50 a 500 ms con ambos ojos no válidos). Se quitan los tres de mayor puntaje, sea cual sea su valor: no hay un umbral."
- **Texto actual (RD 7.9, "Lectura"):** "La primera es que la limpieza es parcial. La correlación máxima entre algún canal y los parpadeos baja de 0,28 a 0,08 (mediana entre personas), sin anularse, y la probabilidad del modelo limpio sigue asociada al recorrido de la mirada (Spearman 0,28; antes 0,41)."
- **Texto propuesto:** agregar a continuación: "Los puntajes oculares son bajos: la mediana entre personas es 0,38 para el primer componente, 0,23 para el segundo, 0,17 para el tercero y 0,13 para el cuarto (0,06 como máximo en los del control), de modo que "ocular" designa aquí un orden y no una identificación segura. Además, el puntaje se calcula entre 1 y 15 Hz y con un seguidor ocular de 60 Hz: por construcción no identifica el potencial de espiga sacádica, que ocupa aproximadamente de 20 a 90 Hz (Keren, Yuval-Greenberg y Deouell, 2010). La limpieza no se dirigió a esa fuente."
- **Texto actual (RD 8.3.3, candidato 1):** "**Artefacto ocular residual.** El remanente conserva el patrón espacial y espectral del artefacto: los canales frontales superan a los posteriores y la potencia lenta supera a alfa y beta."
- **Texto propuesto:** agregar a continuación: "A ello se suma el potencial de espiga sacádica, al que la limpieza no se dirigió (sección 7.9)."
- **Estado:** **nueva**. El primer lector trató la selección circular de los componentes (B6, bien resuelta), no el criterio ni los puntajes.

#### O6. La caída de alfa y beta tiene explicaciones más simples, y falta decir que ese subconjunto usa potencia absoluta

- **Qué pasa.** (i) `scripts/enfoques_41p.py` (`eeg_sets`) define "alfa y beta" como la potencia logarítmica de alfa y de beta por canal; no incluye potencias relativas. Conviene decirlo, porque descarta la objeción aritmética obvia (que la potencia relativa cae cuando sube la potencia lenta del denominador). Esa objeción sí vale para el modelo con todo el EEG, que incluye las potencias relativas. (ii) La frase "Esas fuentes no explican por sí solas la caída en alfa" es más fuerte que lo leído: el aumento de potencia ligado al dipolo córneo-retinal aparece en frecuencias bajo 10 Hz (Plöchl et al., 2012; cita textual en `VERIFICACION_REFERENCIAS.md`), que alcanza la parte baja de alfa (8 a 13 Hz). (iii) Falta la explicación de procesamiento: un parpadeo de 150 µV o el escalón de una sacada son transitorios muy grandes frente al EEG, y en una ventana de 2 s filtrada por separado dejan potencia fuera de su banda principal. SP 4.7 declara que los efectos de borde no se evaluaron; RD 8.3.2 no los relaciona con este resultado.
- **Texto actual (RD 8.3.2):** "Esas fuentes no explican por sí solas la caída en alfa; otra posibilidad, que el diseño no separa, es que los tres componentes retirados arrastren actividad no ocular en esas bandas."
- **Texto propuesto:** "El subconjunto de alfa y beta usa la potencia logarítmica absoluta de cada canal, no la relativa, de modo que su caída no es un efecto aritmético de la potencia lenta. Quedan tres lecturas que el diseño no separa. El aumento de potencia ligado al dipolo córneo-retinal llega hasta cerca de 10 Hz (Plöchl, Ossandón y König, 2012) y alcanza la parte baja de alfa. Los parpadeos y los escalones de las sacadas son transitorios de gran amplitud frente al EEG y, en una ventana de 2 s filtrada por separado, pueden dejar potencia fuera de su banda principal; ese efecto de borde no se evaluó (sección 4.7). Y los tres componentes retirados pueden arrastrar actividad no ocular en esas bandas."
- **Texto propuesto (RD 7.7, tras la tabla de subconjuntos):** "El subconjunto "solo alfa y beta" contiene la potencia logarítmica absoluta de esas bandas en cada canal. En el modelo con todo el EEG entran además las potencias relativas, que dependen de la potencia lenta a través del denominador: también las variables de bandas altas pueden llevar información del artefacto lento."
- **Estado:** ya planteada por el primer lector (I3) y **mal resuelta** (incompleta): se agregó la frase del arrastre, pero quedó una negación más fuerte que la fuente y sin las otras dos lecturas.

#### O7. Los parpadeos entran a la etiqueta por pérdida de mirada

- **Qué pasa.** SP 4.6.4 dice que "no se interpolan las pérdidas de mirada ni se corrigen los parpadeos". Un parpadeo interrumpe el registro y, con él, las fijaciones que suman el tiempo total y la duración media de fijación, dos de las cuatro variables que definen la etiqueta. En los seguidores por video, además, el cierre y la apertura del párpado pueden producir desplazamientos aparentes de la mirada **[requiere fuente]**, que entrarían en la dispersión y el recorrido. A la vez, el parpadeo es la deflexión más grande medida en el EEG (148 y 151 µV; RD 7.8). Es una vía directa entre etiqueta y entrada que no pasa por "mover los ojos", y los borradores hablan siempre de "mirada y parpadeos" en bloque. No se midió cuánto de la etiqueta depende de la fracción de mirada perdida ni cuánto de la detección depende de los parpadeos.
- **Texto actual (SP 4.6.4):** "No se interpolan las pérdidas de mirada ni se corrigen los parpadeos."
- **Texto propuesto:** "No se interpolan las pérdidas de mirada ni se corrigen los parpadeos. Un parpadeo puede acortar o dividir las fijaciones de la ventana: la pérdida de mirada entra así en las variables de fijación y, con ellas, en la etiqueta de atención."
- **Texto propuesto (RD 8.3.3, antes de "Como la etiqueta se define con la conducta ocular"):** "Hay además una vía que no pasa por el movimiento de los ojos: los parpadeos. Un parpadeo interrumpe el registro de la mirada y, por lo tanto, las fijaciones con que se calcula el *Attention Score*, y a la vez produce en el EEG la deflexión de mayor amplitud medida aquí (sección 7.8). No se midió cuánto de la etiqueta depende de la pérdida de mirada dentro de la ventana ni cuánto de la detección depende de los parpadeos."
- **Estado:** **nueva**.

#### O8. El sentido de "mirada quieta" como atención no está establecido

- **Qué pasa.** RD 6.1 niega la validación. Falta la mitad del argumento: la lectura inversa es igual de plausible. Una mirada más quieta acompaña a la lectura detenida, pero también a la espera, a la fatiga o a una mirada que no procesa lo que tiene delante; y una mirada que recorre más puede ser exploración activa **[requiere fuente]**. Con el rótulo "alta", el lector asume una dirección.
- **Texto actual (RD 6.1):** "No designa mayor atención en ningún sentido validado."
- **Texto propuesto:** "No designa mayor atención en ningún sentido validado. Tampoco está establecido su sentido: una mirada más quieta puede acompañar a la lectura detenida de un contenido, pero también a la espera, a la fatiga o a una mirada que no procesa lo que tiene delante, y una mirada que recorre más puede ser exploración activa de la página [requiere fuente]. "Alta" y "baja" son los rótulos del diseño, no una dirección comprobada del constructo."
- **Estado:** el significado conductual de "alta" fue planteado por ambos lectores (menor 10; D2) y quedó **bien resuelto**. La lectura inversa es **nueva**.

#### O9. Patrón de la etiqueta al inicio de cada página: faltan tres alternativas, dos de ellas comprobables con columnas que existen

- **Qué pasa.** RD 8.2 ofrece reorientación, cálculo de fijaciones y composición. Faltan: (i) carga de la página o pantalla en blanco al inicio, que haría de la mirada quieta del primer segundo (prevalencia 0,51) una espera; (ii) la regularidad de que las primeras fijaciones sobre una imagen nueva son más breves y las sacadas más amplias **[requiere fuente]**, que daría la caída de los segundos 2 y 3 sin apelar a la atención; (iii) si los sitios permitían desplazar la página, el contenido en movimiento se sigue con la mirada, y un filtro de velocidad pensado para fijaciones y sacadas clasifica ese seguimiento de forma inconsistente **[requiere fuente]**. La exportación trae el área visible del navegador y la posición del mouse (`DOCUMENTACION_DATOS_MDS.md` §2.5). Además no constan los parámetros del filtro I-VT, y a 60 Hz cada muestra dura 16,7 ms.
- **Texto actual (RD 8.2):** "Hay dos explicaciones más que no se separaron."
- **Texto propuesto:** "Hay otras explicaciones que no se separaron." Y, al final del párrafo: "Otras dos dependen de información del protocolo que no consta. Si al inicio de cada estímulo hay un tiempo de carga o una pantalla en blanco, la mirada quieta del primer segundo puede ser espera. Y si los sitios web permitían desplazar la página, el contenido en movimiento se sigue con la mirada, y el filtro de velocidad, pensado para fijaciones y sacadas, puede clasificar ese seguimiento de forma inconsistente [requiere fuente]. La exportación trae la posición del área visible del navegador y la del mouse, que permitirían comprobarlo; no se usaron."
- **Texto actual (SP 4.6.4):** "Se usan el punto de mirada en píxeles y la clasificación de movimientos oculares que entrega Tobii con su filtro I-VT (identificación por umbral de velocidad), que distingue fijaciones, sacadas, ojos no encontrados y muestras sin clasificar."
- **Texto propuesto:** agregar a continuación: "La clasificación se usa tal como viene en la exportación (filtro `Tobii I-VT (Fixation)`, Tobii Pro Lab 1.241.54542; pantalla de 1920 × 1080 píxeles); no constan el modelo del seguidor ocular ni los parámetros del filtro. A 60 Hz cada muestra dura 16,7 ms: la duración de las sacadas se resuelve en pocos pasos y las más pequeñas pueden no detectarse [requiere fuente]."
- **Estado:** el efecto del cálculo y la composición los planteó el primer lector (I15, **bien resuelto**). Las tres alternativas y la declaración del filtro son **nuevas**.

#### O10. Efecto del historial en activación: falta la respuesta al cambio de estímulo

- **Qué pasa.** RD 7.3 informa que, dentro de un mismo estímulo, el tiempo transcurrido predice la etiqueta por sí solo (+0,049 [+0,027; +0,072]) y no lo interpreta. Hay una lectura fisiológica directa: cada cambio de estímulo es un evento; una respuesta de conductancia a un evento comienza entre 1 y 5 s después y decae lentamente (Benedek y Kaernbach, 2010). Si el cambio de página provoca una respuesta, la GSR sigue dentro de cada estímulo un curso ligado a su inicio, y las ventanas etiquetadas, que empiezan a los 6 s, caen sobre ese curso. Eso basta para que la posición prediga dentro del estímulo y para que un resumen de ventanas previas, que informa de cuánto lleva la persona en la página, también lo haga. No se examinó la GSR alineada al inicio de los estímulos. Segunda adición: las derivas lentas no neurales (temperatura, hidratación del contacto de la GSR; contacto de los electrodos del EEG; pupila que cambia con el tiempo en la tarea **[requiere fuente]**) pueden ser comunes a etiqueta y entradas; el texto habla de "deriva lenta de la señal" solo para la GSR.
- **Texto actual (RD 8.4):** "La etiqueta no tiene control de artefactos sobre la señal cruda y el movimiento no se midió." (con la corrección de O3)
- **Texto propuesto:** agregar a continuación: "Hay otra lectura, propia de la señal. Cada cambio de estímulo es un evento, y una respuesta de conductancia a un evento comienza entre 1 y 5 s después y decae lentamente (Benedek y Kaernbach, 2010). Si el cambio de página provoca una respuesta, la GSR sigue dentro de cada estímulo un curso ligado a su inicio, y las ventanas etiquetadas, que empiezan a los 6 s, caen sobre ese curso. Eso bastaría para que el tiempo transcurrido prediga la etiqueta dentro de un mismo estímulo (+0,049; sección 7.3) y para que un resumen de las ventanas previas, que informa de cuánto lleva la persona en la página, también lo haga. No se examinó la GSR alineada al inicio de los estímulos."
- **Estado:** **nueva**. El segundo lector trató "misma página" (B2, bien resuelta) y el primero el movimiento (I16); ninguno propuso la respuesta al cambio de estímulo.

#### O11. RD 8.5, "Origen de la señal": un argumento anatómico que el texto dice no haber confirmado, y que contradice el párrafo siguiente

- **Qué pasa.** La frase propone que el EEG de superficie ve poco las regiones que regulan la conductancia, y a la vez declara que no se puso a prueba y que "su base anatómica no se confirmó en la fuente". En una tesis, una hipótesis explicativa sin fuente no se defiende con una disculpa: se quita. Además se contradice con el párrafo "Tipo de relación", que cita una relación entre el nivel de conductancia y la potencia alfa, es decir, un correlato de superficie. La presentación lo dice en voz alta (RE lámina 28: "eso último no lo pude confirmar en la fuente").
- **Texto actual (RD 8.5):** "Si varias de esas regiones son mediales o profundas, su actividad contribuiría poco a un EEG de superficie de 16 canales; esa lectura es una hipótesis que este trabajo no puso a prueba y cuya base anatómica no se confirmó en la fuente."
- **Texto propuesto:** "De ello no se sigue que el EEG de superficie no pueda reflejar ese estado: los trabajos citados más abajo relacionan el nivel de conductancia con la potencia alfa (Barry et al., 2005, 2007)." (Y suprimir la nota de trabajo que sigue, o dejarla solo como pendiente de lectura.)
- **Texto actual (RE lámina 28, nota):** "Esa vía es lenta, y es posible que dependa de regiones profundas que el EEG de superficie ve poco; eso último no lo pude confirmar en la fuente."
- **Texto propuesto:** "Esa vía es lenta."
- **Texto actual (EN, guion de la lámina 28):** "Es posible que además dependa de regiones profundas que el EEG de superficie ve poco; eso no lo pude confirmar en la fuente."
- **Texto propuesto:** suprimir la frase. En EN 2 (respuesta larga), cambiar "quizá con un origen que el EEG de superficie ve poco (eso no lo pude confirmar en la fuente), y que la etiqueta…" por "y que la etiqueta…".
- **Estado:** **nueva** frente a los dos informes de comité. `VERIFICACION_REFERENCIAS.md` (punto 3, opción B) ya había señalado que la lista de estructuras no se confirmó; la opción elegida conservó la hipótesis, y por eso queda **mal resuelta**.

#### O12. Ventaja de la red: falta la explicación espacial

- **Qué pasa.** RD 8.3.4 propone formas de onda y escala. La más inmediata para quien registra electrooculograma es otra: la primera etapa de EEGNet aprende filtros espaciales (Lawhern et al., 2018), es decir, combina canales con signo, y puede formar por sí sola derivaciones como la diferencia entre los dos canales frontales laterales, donde la mirada horizontal entra con signo opuesto en 31 de 37 personas (RD 7.8). Las variables del modelo de referencia se calculan canal por canal y pierden el signo; de la relación entre canales solo recibe dos resúmenes (correlación media y fracción dominante de la covarianza; SP 4.7).
- **Texto actual (RD 8.3.4):** "Otra, igual de plausible y tampoco puesta a prueba, es la escala por persona y canal que recibe la red y no el modelo de referencia."
- **Texto propuesto:** agregar a continuación: "Una tercera es espacial: la red aprende filtros que combinan canales con signo (Lawhern et al., 2018) y puede formar por sí sola derivaciones como la diferencia entre los dos canales frontales laterales, donde la mirada horizontal entra con signo opuesto (sección 7.8), mientras que las variables del modelo de referencia se calculan canal por canal y pierden el signo. Tampoco se puso a prueba."
- **Estado:** **nueva**.

### Menores

| # | Ubicación | Texto actual | Texto propuesto | Estado |
|---|---|---|---|---|
| m1 | SP, "Cómo leer este borrador", siglas | "EEG es electroencefalograma y GSR es respuesta galvánica de la piel (*galvanic skin response*)." | "EEG es electroencefalograma y GSR es respuesta galvánica de la piel (*galvanic skin response*), nombre de la columna en la exportación; el término vigente es actividad electrodérmica o conductancia de la piel [requiere fuente: Boucsein et al., 2012, leída solo por resumen]. No se usa la sigla EDA para la señal porque en este documento designa el análisis exploratorio de datos." | Nueva |
| m2 | RD 6.2 | "(en adelante, "señal cruda")" | "(en adelante, "señal sin variables calculadas"; los informes y las láminas la llaman "señal cruda", aunque está filtrada, escalada por persona y canal y recortada)" | Nueva. La escala y el recorte constan en `scripts/red_cruda_41p.py` |
| m3 | SP 4.6.1, "Precisión alcanzada", tras "encontró que el EEG va atrasado entre 0,18 y 0,53 s en las 41 personas (mediana 0,45 s)." | — | Agregar: "Las tres referencias oculares (mirada horizontal, mirada vertical y parpadeos) dan el mismo desfase en casi todas las personas, lo que apunta a una diferencia de relojes o de transmisión y no a un retardo fisiológico." | I11 del primer lector, bien resuelta; el dato es nuevo |
| m4 | RD 7.8 | "La respuesta promedio al parpadeo es de 148 y 151 µV en los dos canales frontopolares" | "La respuesta promedio al parpadeo (amplitud pico a pico del promedio alineado a su inicio, entre 1 y 15 Hz; mediana entre personas) es de 148 y 151 µV en los dos canales frontopolares". Y agregar al párrafo: "El montaje por defecto asigna los 16 canales a Fp1, Fp2, C3, C4, P7, P8, O1, O2, F7, F8, F3, F4, T7, T8, P3 y P4. Parpadeo designa aquí un tramo de 50 a 500 ms con ambos ojos no válidos, lo que incluye pérdidas de seguimiento que no son parpadeos; se detectaron entre 19 y 393 por persona." | Nueva |
| m5 | SP 4.6.5, tras "La serie se estandariza por sesión, excluida la calibración, y una ventana es válida si su cobertura es de al menos 50 %." | — | Agregar: "No se descartan las muestras contiguas a los parpadeos, en las que el párpado ocluye parcialmente la pupila, ni se corrige el efecto de la posición de la mirada sobre el diámetro medido [requiere fuente]. Al pasar de dos ojos válidos a uno, la serie puede dar un salto si los diámetros de ambos ojos difieren. El diámetro mediano fue de 3,0 mm (percentiles 5 y 95: 2,4 y 3,9 mm; `resultados/eda/eye_pupil/resumen_numerico.csv`, columna filtrada, sobre una muestra de las filas); no consta la iluminación de la sala." | Nueva |
| m6 | RD 7.9, encabezado de la tabla y prosa | "componentes oculares" / "componentes no oculares" | Mantener, con la precisión de O5 ("designa un orden"). Sin texto adicional | Nueva (cubierta por O5) |
| m7 | RE lámina 15, nota; EN, guion de la lámina 15 | "La etiqueta dice si P22 está más activada que de costumbre en ese momento." / "La etiqueta dice si P22 está más activada que de costumbre." | "La etiqueta dice si el puntaje de GSR de P22 está sobre su mediana de la sesión en ese momento; no es una medida validada de activación." | Nueva |
| m7b | EN, guion de la lámina 22 | "la proporción de ventanas con atención alta cae a 37 %" | "la proporción de ventanas con etiqueta alta, es decir, de mirada más quieta, cae a 37 %" | Nueva |
| m8 | CO 9.5, "Tamaño del efecto" | "por lo que el efecto temporal tiene interés científico pero poca utilidad práctica con las variables actuales" | "por lo que el efecto temporal, aun si se confirmara, tendría poca utilidad práctica con las variables actuales" | Nueva |
| m9 | RD 6.1, párrafo "Ambas etiquetas son relativas…" | — | Agregar al final: "En los títulos y las tablas, "atención" y "activación" abrevian *Attention Score* y *Arousal Score*: nombran la etiqueta definida, no el constructo." | Nueva |
| m10 | RD 7.12, "Tipo de página" | "La etiqueta de atención se predice mejor en sitios web (0,71) y peor en textos (0,60 sin historial y 0,63 con historial)." | Agregar: "Que se prediga peor en textos es coherente con la lectura ocular de la sección 8.3: en la lectura las sacadas son pequeñas y regulares [requiere fuente; posiblemente Dimigen et al., 2011] y dejarían una huella menor en el EEG. No se puso a prueba." | Nueva |
| m11 | SP 4.7, "EEG por canal" | "…y se estima el espectro con el método de Welch." | "…y se estima el espectro con el método de Welch, con segmentos de 1 s solapados a la mitad, lo que da una resolución de 1 Hz: la banda delta (1–4 Hz) queda descrita por pocos puntos." | I14 del primer lector, bien resuelta; la resolución es nueva. Consta en `scripts/eeg_por_canal_v2.py` (`nperseg=125`) |

---

## E. ¿Dicen las conclusiones algo defendible y útil para mi área?

**Sí, y más de lo que el capítulo 9 deja ver.** Lo defendible y útil:

1. **El caso de la etiqueta ocular.** Un EEG de pocos canales sin electrooculograma decodifica la conducta de mirada; los frontales funcionan como electrooculograma (parpadeo de unos 150 µV adelante y 20 µV atrás; mirada horizontal con signo opuesto en los frontales laterales). Cualquier trabajo que evalúe modelos de EEG con etiquetas derivadas de un seguidor ocular tiene este problema. El tamaño medido (0,060 de 0,181, como cota inferior) es un dato que mi área puede usar.
2. **El caso de la posición.** Una ventaja de +0,029 en 36 de 41 personas que se reduce a un número. Es una advertencia de diseño aplicable a cualquier estudio con estímulos breves y etiquetas relativas.
3. **El resultado negativo de activación**, si se enuncia como lo que es: el nivel lento de la conductancia, relativo a la sesión, no se recupera desde 2 s de señal.

**Dónde el texto afirma de más:**

- **Título de RD 8.4**, "el historial reciente supera al placebo, con respaldo solo a 6 s", y **título de RE lámina 23**, "En activación, los segundos previos aportan frente al placebo". El cuerpo dice que el contraste no separa la fisiología previa de la página, del tramo de la sesión ni del soporte del filtro; con O10 se suma el curso de la GSR tras el cambio de estímulo. Los títulos conservan un sujeto ("los segundos previos") que el cuerpo ya no sostiene. Sugerencia sin cifras: "En activación, el historial del mismo estímulo supera a un placebo de otros estímulos".
- **CO 9.5**, "tiene interés científico" (m8).
- **RD 8.5, "Origen de la señal"** (O11).
- **CO 9.1 y 9.7**, "evidencia acotada de que un resumen del historial reciente de las señales ayuda a predecir el *Arousal Score*". Es defendible como descripción. No lo es si se lee como evidencia sobre la fisiología: conviene que la frase diga "ayuda a predecir" y no deje implícito "porque el estado previo informa del actual".
- **"Navegación web"** en todo el material (O1).

**Dónde se disculpa de más:**

- **CO 9.7** antepone seis reservas al hallazgo y deja para el final lo más sólido. Un lector de mi área querría el orden inverso: primero las dos advertencias metodológicas, que no dependen de una cohorte nueva, y después la evidencia acotada de activación.
- **CO 9.3** empieza con "lo que estos datos no permiten establecer". El hallazgo positivo se puede afirmar sin reservas: los canales frontales registran la mirada y el parpadeo con la topografía esperable, y el modelo los usa. Eso está medido.
- **"No es una confirmación independiente"** y sus variantes aparecen en RD 6.3, 6.5, 6.6, 7.1, 8.1, 8.4 y 8.8, y en CO 9.1 y 9.5. Con decirlo una vez en 6.5 y otra en 9.1 basta.
- **CO 9.5**, primer punto: cerca de 250 palabras en un solo párrafo, que repite la sección 8.8. Puede remitir a ella y conservar tres frases.
- **Las advertencias de aprobación del profesor guía** dentro de la prosa (por ejemplo RD 6.4, "El margen de 0,02 no está aprobado por el profesor guía") son material de proceso, como las notas de trabajo; en la tesis final no van.
- **RE lámina 27 y EN**: "De las 18 referencias, 10 las contrasté con el texto completo y 8 solo con el resumen". Dicho en una defensa invita a la objeción. Lo correcto es leer las ocho antes de defender, no anunciarlo.

---

## F. Preguntas de defensa propias de mi área que EN no prepara o responde mal

EN tiene 49 preguntas, casi todas de diseño y estadística. De mi área prepara bien la 1, 7, 10, 11, 20, 25, 27 (con el error de O3), 34 y 41. Faltan estas. Las respuestas usan solo lo que consta.

1. **¿Qué referencia usó el EEG, qué electrodos y con qué impedancias?** No consta. Los archivos dicen que es un OpenBCI Cyton con Daisy, de 16 canales a 125 Hz; ni la referencia, ni la tierra, ni el tipo de electrodo ni las impedancias están documentados, y no re-referencié. Tengo que pedirlo al proyecto. Lo que comprobé es que la distribución de los parpadeos y de la mirada horizontal es compatible con el montaje por defecto.
2. **¿Qué evidencia tiene de que su EEG contiene actividad cerebral? ¿Vio un máximo alfa?** No hice esa comprobación. El análisis exploratorio no estimó el espectro, porque la saturación era el principal problema de calidad. Lo que tengo es que los artefactos oculares se distribuyen como se espera y que, en el control de la limpieza, tres componentes no oculares concentran una mediana de 72 % de la varianza, sin que yo sepa qué son. Por eso no afirmo origen cerebral, y por eso el resultado negativo de activación vale para este registro.
3. **¿Qué parte de sus datos es navegación web? ¿Qué son los estímulos `emotion`, `blur` y los numerados?** De las 22.176 ventanas de atención, 6.423 son de cinco sitios web; el resto son textos, diseños, estímulos numerados e imágenes. El contenido de los numerados y de las imágenes `emotion` y `blur` no está en mis notas; tengo que pedir el protocolo. Mis resultados describen la sesión completa.
4. **Si hay imágenes de emoción, ¿por qué no las usó para validar el *Arousal Score*?** Porque no sé qué son ni si tienen valores normativos. Si los tuvieran serían un criterio externo posible; hoy no lo puedo afirmar. La validación externa es una decisión abierta.
5. **Su "nivel tónico", ¿es el nivel de conductancia? ¿Por qué no usó una deconvolución?** No lo es en sentido estricto: es la parte de la señal bajo 0,05 Hz, que incluye el nivel de base y la acumulación de las colas de las respuestas. No apliqué una descomposición por deconvolución. Y mi conteo de respuestas son máximos locales dentro de cada ventana de 2 s, con umbral en unidades estandarizadas; no lo validé, y en 9 de las 41 personas no varía.
6. **¿Dónde iban los electrodos de la conductancia? ¿En la mano del mouse? ¿En qué unidad está?** No consta ninguna de las tres cosas. La exportación no declara la unidad y por eso trabajo con valores estandarizados. La exportación sí trae la posición del mouse, que no usé.
7. **Usted dice que no midió movimiento. ¿El equipo no trae acelerómetro?** Lo trae: tres canales en cada archivo. No los usé ni comprobé su contenido. Lo correcto es decir que no analicé el movimiento.
8. **¿Con qué criterio llamó "ocular" a un componente? ¿Qué correlación tenían?** Por orden, no por umbral: los tres de mayor correlación con la mirada o los parpadeos, entre 1 y 15 Hz. Las medianas son 0,38, 0,23 y 0,17; el control, 0,06 como máximo. Son correlaciones bajas, y el tercero puede no ser ocular. El número, tres, estaba fijado de antemano.
9. **Con ese criterio, ¿cómo habría detectado el potencial de espiga sacádica?** No lo habría detectado: ocupa de 20 a 90 Hz y mi puntaje llega a 15 Hz, con un seguidor de 60 Hz. La limpieza no se dirigió a esa fuente. Es una razón más para leer la caída como cota inferior.
10. **Los parpadeos, ¿entran en su etiqueta?** Pueden entrar: no interpolo las pérdidas de mirada, así que un parpadeo acorta o divide las fijaciones de la ventana, y el parpadeo es la mayor deflexión del EEG. No medí cuánto pesa esa vía.
11. **Una mirada quieta, ¿es atención o es una mirada perdida?** No lo sé, y la etiqueta no lo distingue. "Alta" es el rótulo del diseño. Una mirada quieta puede ser lectura detenida, espera o fatiga.
12. **¿Los participantes podían desplazar las páginas? ¿Cómo trata el filtro de fijaciones un contenido que se mueve?** No sé si podían: no tengo el protocolo. Usé la clasificación de Tobii tal como viene y no conozco sus parámetros. La exportación trae el área visible del navegador, con la que se podría comprobar.
13. **A 125 Hz, ¿hay solapamiento espectral de la actividad sobre 62,5 Hz?** No lo sé. No revisé el filtro antisolapamiento del equipo en modo de 16 canales **[requiere fuente]**. Filtro entre 1 y 45 Hz después de muestrear, lo que no corrige un solapamiento previo.
14. **El desfase de 0,45 s, ¿es de reloj o es fisiológico?** Lo leo como de reloj o de transmisión: las tres referencias (mirada horizontal, vertical y parpadeos) dan el mismo desfase en casi todas las personas, y un retardo fisiológico no sería igual para las tres. No investigué por qué hay dos grupos. (EN 10 no da este argumento.)
15. **¿Por qué llama "cruda" a una señal filtrada?** Es una abreviatura mía para "sin variables calculadas a mano". La señal está filtrada entre 1 y 45 Hz, escalada por persona y canal y recortada.
16. **La etiqueta se predice peor en textos. ¿Por qué?** No lo puse a prueba. Es coherente con la lectura ocular: al leer, las sacadas son pequeñas y dejarían menos huella en el EEG **[requiere fuente]**.
17. **¿Corrigió la pupila por la posición de la mirada y por los bordes de los parpadeos?** No. Uso los diámetros que el equipo marca como válidos, promedio los dos ojos e interpolo huecos breves. La pupila casi no pesa en la etiqueta de atención; en activación es una entrada y no se demostró su aporte.

**Respuestas de EN que conviene corregir** (además de la 27, O3): la 2 y el guion de la lámina 28 repiten el argumento de las regiones profundas (O11); la 7 opone latencia fásica y nivel tónico con más nitidez que la que el cálculo permite (O4).

---

## G. Legibilidad para un lector de mi área

1. **RD 6.2, lista de controles.** Cinco controles con cuatro placebos (de otros estímulos, desplazado, disperso, de bloque) en una lista. Me perdí en la diferencia entre el placebo del 16-11 y los dos de la curva. Una tabla de cuatro filas (de dónde salen las ventanas, qué iguala, qué no iguala) lo resolvería.
2. **RD 7.2, "AUC estratificada".** Un párrafo con tres estratos, dos comparadores y tres niveles de registro. Hay que leerlo tres veces para ver que no contradice al control de posición. Merece una tabla.
3. **Las fechas como nombres.** "El análisis del 16-11", "la fase 2 del 22-11", "E1 del 16-11 frente a E1 del 22-11". Un lector externo no retiene doce etapas por su fecha. En la tesis conviene nombrarlas por contenido y dejar las fechas para el anexo.
4. **RD 6.4, precedencia de las reglas.** El párrafo de las ocho filas es correcto y casi ilegible; es material de anexo.
5. **RD 7.9 antes que la descripción del método.** Para saber cómo se eligieron los componentes hay que volver a 6.2, que no da la banda ni los puntajes (O5).
6. **"Estímulo", "página", "segmento".** El glosario de 6.3 ayuda, pero "página" para una imagen `blur` o un estímulo numerado confunde (O1).
7. **RD 7.8.** Habla de "canales frontopolares" y "frontales laterales" sin dar las posiciones; la lámina 27 dice F7 y F8. Un lector de EEG quiere los nombres (m4).
8. **RD 6.1, soporte de la etiqueta de activación.** El párrafo "[t−4, t+2)" con los porcentajes de peso es exacto y denso; un esquema lo haría evidente.
9. **Las notas de trabajo y las advertencias de aprobación** interrumpen la lectura en casi todas las secciones. Entiendo su función en el borrador.
10. **SP 4.6.5, límite de interpolación.** "Se cuenta sobre todas las filas de la exportación, incluidas las de GSR, por lo que en tiempo es algo menor que 0,2 s": se entiende a la segunda lectura.

---

## Recuento y relación con los dos informes anteriores

| # | Objeción | Gravedad | Estado |
|---|---|---|---|
| O1 | "Navegación web" sin descripción de estímulos; imágenes `emotion` y `blur` | Bloqueante | Ya planteada (segundo lector, D4) y **no resuelta**; proporción, categorías y vínculo con la validación externa, nuevos |
| O2 | Calidad del EEG como registro cerebral no declarada | Bloqueante | **Nueva** |
| O3 | "El movimiento no se midió": hay acelerómetro y mouse | Importante | Ya planteada (primer lector, I16) y **mal resuelta**; el dato es nuevo |
| O4 | "Nivel tónico" y conteo de SCR | Importante | **Nueva** |
| O5 | ICA: criterio ciego a la espiga sacádica; puntajes bajos | Importante | **Nueva** |
| O6 | Caída de alfa y beta: lecturas más simples; potencia absoluta | Importante | Ya planteada (primer lector, I3) y **mal resuelta** (incompleta) |
| O7 | Los parpadeos entran a la etiqueta | Importante | **Nueva** |
| O8 | Sentido de "mirada quieta" | Importante | **Nueva** (el significado conductual, D2, quedó bien resuelto) |
| O9 | Patrón al inicio de página: carga, fase inicial, desplazamiento; filtro I-VT | Importante | **Nueva** (I15, cálculo y composición, bien resuelta) |
| O10 | Historial en activación: respuesta al cambio de estímulo | Importante | **Nueva** |
| O11 | Argumento de las regiones profundas | Importante | **Nueva** frente a los dos lectores; conocida en la verificación de referencias y **mal resuelta** |
| O12 | Red: explicación espacial | Importante | **Nueva** |
| m1–m11 (y m7b) | Nomenclatura, datos de método que constan, frases de la presentación | Menores | Nuevas, salvo m3 y m11, que completan I11 e I14 (bien resueltas) |

**Totales:** 2 bloqueantes, 10 importantes y 11 menores (m7 tiene dos partes; m6 no pide texto). Nuevas por completo: 1 bloqueante (O2), 7 importantes (O4, O5, O7, O8, O9, O10, O12) y 9 menores (m1, m2 y m4 a m10). Ya planteadas y no resueltas: 1 (O1). Ya planteadas y mal resueltas: 3 (O3, O6, O11). Ya planteadas y bien resueltas que solo reciben un dato adicional: 2 (m3, m11).

**Sobre la convergencia.** En diseño e inferencia no encontré nada que los dos lectores anteriores no hubieran visto. Lo nuevo es de registro y de fisiología, y casi todo se resuelve con redacción y con datos que ya están en el repositorio. Dos cosas no se resuelven redactando y hay que pedirlas al proyecto: el protocolo de estímulos (qué son, cuánto duran, qué tarea había, si se podía desplazar la página) y las condiciones de registro (referencia, electrodos e impedancias del EEG; equipo, sitio y unidad de la conductancia; modelo del seguidor ocular, distancia e iluminación). Sin ellas, el capítulo de método no pasa una evaluación de mi área, por cuidadosos que sean los capítulos 6 a 9.

**Lo que requeriría análisis nuevo** (solo se lista; la experimentación está cerrada): espectro del EEG por canal como comprobación de calidad; GSR alineada al inicio de los estímulos; relación entre la etiqueta de atención y la fracción de mirada perdida por ventana; contenido del acelerómetro; resumen por persona de la calibración del seguidor ocular; resultados por tipo de estímulo con intervalo.

**Lo que no pude comprobar.** El contenido de los canales de acelerómetro y de las columnas del navegador (solo consta que existen). El número de estímulos (116 en la lámina 4; mi conteo de lectura dio 95 nombres distintos y no está auditado). Las afirmaciones marcadas [requiere fuente] son conocimiento corriente de mi área, pero ninguna está entre las 18 referencias verificadas y no deben entrar a la tesis sin su cita.
