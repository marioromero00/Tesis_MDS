# Verificación de las correcciones de la ronda 7 (tercera lectura, especialista) — ronda 8 (27-11-2026)

Verificador independiente. Objeto: el diff `1c915df..1998b95`. No se editó ningún archivo existente, no se entrenó ni ajustó ningún modelo, no se corrió ningún análisis nuevo y no se hizo ningún commit. Lo único escrito es este informe. Las comprobaciones son recuentos y lecturas de CSV, scripts, informes y documentación ya existentes; la regeneración de la presentación se hizo en una copia temporal fuera del repositorio.

Abreviaturas: RD = `Escritura/Borrador Resultados y Discusión 23-11-2026.md`; SP = `Escritura/Borrador Secciones pendientes 23-11-2026.md`; CO = `Escritura/Borrador Conclusiones 23-11-2026.md`; MI = minuta del 23-11; CI = `documentacion/Cierre_Experimental_Final_23-11-2026.md`; EN = `presentaciones/avances_tesis_06-11-2026/ENSAYO.md`; RE = `relato.py` de la misma carpeta. Los borradores y las notas se citan por su original en el vault y en `notas/`; se comprobó que son idénticos byte a byte a las copias de `respaldo_local/` del commit.

## 1. Recuento

- Archivos del diff: 42. De ellos, 28 son gráficos SVG cuyo único cambio es la fecha y los identificadores internos (comprobado: sin otras líneas distintas); 1 es el informe nuevo de la ronda 7; 1 es el manifiesto del respaldo. Con contenido: CI, EN, RE, `GUIÓN.md`, `FUENTES.md`, `index.html`, RD, SP, CO, MI y las dos notas.
- Texto añadido: unas 8.900 palabras. RD pasó de 19.861 a 22.055 palabras en este commit (17.697 al cierre de la ronda 4).
- Afirmaciones con cifra, hecho de método o de equipo, o atribución bibliográfica comprobadas en la fuente primaria: 96. Coinciden 84. Con error o imprecisión: 12 (ninguna cambia una cifra de resultado).
- Errores: **0 bloqueantes, 2 importantes, 12 menores** (tabla de la sección 3; dos de los menores son la misma imprecisión en dos archivos).
- No propagado: 6 puntos (sección 4; cuatro de ellos están también en la tabla de errores).
- Afirmaciones fisiológicas nuevas en la prosa sin respaldo en las 18 referencias: ninguna con la marca "requiere fuente" (las 10 marcas están todas dentro de notas de trabajo). Tres frases de procesamiento de señal entraron sin cita y se comentan en la sección 2.7.
- Reglas del proyecto: se cumplen (sección 6).
- Presentación: todo lo pedido pasa (sección 5).

## 2. Lo que se comprobó y coincide

### 2.1 Estímulos y categorías

- `resultados/ampliacion_41p_16-11-2026/por_categoria.csv`: atención 6.423 (sitio web), 6.637 (numerado), 4.082 (diseño), 2.255 (texto), 1.792 (`emotion`), 891 (`blur`), 96 (instrucciones); suma 22.176. Activación 5.457, 3.291, 1.316, 1.285, 401, 46; sin `blur`; suma 11.796. Coincide con RD 6.3, MI, CI, EN (pregunta 52) y la nota de la lámina 4.
- 6.423 / 22.176 = 28,96 % (29 %); 5.457 / 11.796 = 46,26 % (46 %). "Menos de un tercio" es correcto para atención; "la mayoría de las ventanas" no web vale en las dos tareas.
- La regla está en `scripts/ampliacion_41p.py` (`category`), tal como la describe la nota de RD 6.3: quita el sufijo "(n)", `Text` a texto, prefijos `Meg`, `diario_financiero`, `temu`, `Despega`, `Nint` a sitio web, y el resto (`Bienvenida`, `Explicacion1 (1)`) a instrucciones. Son siete categorías.
- `caracteristicas_multimodales.csv`, columna `stimulus`: 116 valores distintos (116 también en las 41 personas), 95 sin el sufijo. La diferencia de 21 son 15 variantes de `Text` (entre `Text (19)` y `Text (35)`), 3 de `emotion` y 3 de `diseño`. Los cinco sitios son ocho nombres (`Nint`, `Ninte`, `Ninten`, `Nintend`, uno por grupo experimental). Cada persona tiene ventanas en 68 a 98 nombres (igual con 48 y con 41 personas).

### 2.2 Calidad del EEG y equipo

- `resultados/eda/eeg/eeg_resumen_sesiones.csv`: 104 sesiones (48 principales, 51 de prueba, 5 sin identificador). Mediana de saturación: 2,49 % en las 48 principales, 42,6 % en las de prueba, 27,94 % en las 104 (coincide con `eeg_resumen.json`). P17 59,2 %, P1 37,9 %, P14 31,2 %, P25 36,0 % de repetición plana; P15 26,2 % y P16 25,0 % se conservan.
- `scripts/eeg_por_canal_v2.py` (`extract_window`): un canal se marca ausente solo por valores finitos bajo 95 %, más de 1 % de muestras sobre 180.000 µV, 99 % de diferencias planas, menos de 200 muestras o huecos sobre 0,1 s. No hay re-referencia ni rechazo por amplitud. Welch con `nperseg=125`, `noverlap=62`, `nfft=256`. La potencia relativa divide por la potencia total de 1 a 45 Hz.
- `DOCUMENTACION_DATOS_MDS.md`: sección 2.1 (versión 1.241.54542, filtro `Tobii I-VT (Fixation)`, 1920 × 1080, latencia de 10 ms); 2.5 (área visible del navegador, alto de página, posición del mouse); 3.2 (`%Board = OpenBCI_GUI$BoardCytonSerialDaisy`, 16 canales, 125 Hz, tres canales de acelerómetro; "la ubicación y referencia de los electrodos no están documentadas"); 3.3 (CSV de BrainFlow en parte de las sesiones). No hay en el vault ni en el repositorio ningún dato de tierra, tipo de electrodo, impedancias, modelo del seguidor ocular ni equipo o sitio de la GSR: "no consta" es correcto.
- `EDA_EEG.md`: el análisis exploratorio no estimó potencia por bandas y lo atribuye a la saturación.

### 2.3 Limpieza ocular

- `scripts/limpieza_ocular_41p.py` y su `protocolo.json`: FastICA con tantos componentes como canales utilizables; ajuste sobre la señal de 1 a 45 Hz con filtro de red; se excluyen las muestras a menos de 1 s de una saturación (convolución de 251 muestras); puntaje entre 1 y 15 Hz; se quitan los tres de mayor puntaje sin umbral; el control toma los tres de mayor varianza entre los que quedan fuera de los cuatro de mayor puntaje (`rest = order[4:]`).
- `personas_limpieza.csv`: medianas 0,381; 0,231; 0,169; 0,132; máximo del control 0,059; varianza 3,5 % y 72,1 %; 11 a 16 canales.

### 2.4 Montaje, parpadeos, pupila

- `resultados/montaje_ocular_41p_23-11-2026/INFORME.md` y `scripts/montaje_ocular_41p.py` (`blink_onsets`): parpadeo = tramo de 50 a 500 ms con ambos ojos no válidos; 19 a 393 por persona; lista de los 16 canales en el orden que da SP 4.7; 148 y 151, 74 y 77, 57 y 56 µV; 18 a 29 µV atrás; canales utilizables 11 a 16 (mediana 15), con más pérdidas en P4, O1, P7 y P3; las tres referencias dan el mismo desfase "en casi todas las personas".
- `resultados/eda/eye_pupil/resumen_numerico.csv`: columna `Pupil diameter filtered`, mediana 3,000 mm, percentiles 2,435 y 3,918; ojos izquierdo y derecho, 2,993 y 3,013. Los percentiles son de una muestra determinista y el recorrido cubre 49 grabaciones (`metadata.json`). El preprocesamiento usa las columnas de cada ojo, no la filtrada.

### 2.5 GSR

- `scripts/preprocesamiento_secuencial.py`: `butter(2, …)` con `filtfilt` sobre la señal estandarizada; fásica = señal menos tónica; `find_peaks` con prominencia sobre la fásica de la ventana.
- Las 9 de 41 personas con número y prominencia de SCR constantes: `ronda6/RECALCULO_DESCRIPTIVOS.md`.

### 2.6 Subconjunto de alfa y beta y red

- `scripts/enfoques_41p.py` (`eeg_sets`): `logpower_alpha` y `logpower_beta`, sin potencias relativas.
- `scripts/red_cruda_41p.py`: `CLIP = 8`; escala por persona y canal con la mediana de la desviación de sus ventanas.

### 2.7 Atribuciones bibliográficas

Contra `VERIFICACION_REFERENCIAS.md`:

- Benedek y Kaernbach (2010): "típicamente entre 1 y 3 s o entre 1 y 5 s" y la cola en descenso de la respuesta anterior. Correcto en RD 8.4, RD 8.5 y SP 4.6.3; el matiz se respetó (el lector proponía "entre 1 y 5 s" y se aplicó la forma verificada).
- Keren et al. (2010): "aproximadamente de 20 a 90 Hz". Correcto en RD 7.9 y EN 58.
- Plöchl et al. (2012): aumento de potencia ligado al dipolo "en frecuencias bajo 10 Hz". Correcto en RD 8.3.2.
- Lawhern et al. (2018): filtros espaciales. La atribución es válida; la posición dentro de la red está mal dicha (error 3).
- Barry et al. (2005, 2007), frase nueva de RD 8.5 ("relacionan el nivel de conductancia con la potencia alfa"): sostenida por el resumen de 2005 (correlación negativa entre condiciones de ojos cerrados). El de 2007 muestra que ambos cambian con la cafeína y no informa una correlación; "relacionan" lo cubre a los dos sin exceso. No contradice el resto de la sección: "Tipo de relación" ya dice que esa relación se observó al comparar condiciones. Queda una tensión solo en la lámina 28 (sección 4, punto 6).
- Critchley (2002): se cita solo para lo que sostiene el resumen. Correcto.

Tres frases de procesamiento, no de fisiología, entraron sin cita. Son inferencias del propio cálculo y están redactadas con reserva; se dejan anotadas para que el autor decida si las quiere así:

1. SP 4.6.3 y RD 6.1: la acumulación de las respuestas queda dentro de la banda que deja pasar el filtro de 0,05 Hz.
2. RD 8.3.2: un transitorio grande en una ventana de 2 s filtrada por separado puede dejar potencia fuera de su banda (ver error 6).
3. SP 4.6.4: las muestras sin ojos detectados no se clasifican como fijación, de modo que un parpadeo puede acortar o dividir fijaciones. Consta la categoría `EyesNotFound`; no se midió en los datos.

## 3. Tabla de errores

| # | Archivo original | Texto exacto actual | Por qué está mal (fuente) | Texto exacto corregido | Gravedad |
|---|---|---|---|---|---|
| 1 | EN, "Cinco lecturas que la segunda lectura pidió corregir" (línea 27) | `La latencia vale para la parte fásica; la etiqueta es en lo esencial el nivel tónico, más lento.` | Es la oposición que la ronda 7 corrigió en la pregunta 7 y en RD 8.5 (O4): las respuestas entran en la componente lenta. El mismo archivo dice ahora las dos cosas. | `La latencia vale para las respuestas individuales; la etiqueta es en lo esencial la componente lenta, que llamo nivel tónico e incluye la acumulación de esas respuestas.` | Importante |
| 2 | RD 8.5, "Tipo de relación" | `es plausible que la navegación web produzca un rango de activación estrecho; este trabajo no lo midió.` | RD 6.3 dice desde este commit que los sitios web son el 46 % de las ventanas de activación (`por_categoria.csv`). La frase describe la sesión como navegación web. | `es plausible que una sesión de estímulos en pantalla como esta produzca un rango de activación estrecho; este trabajo no lo midió.` | Importante |
| 3 | RD 8.3.4 | `la primera etapa de la red aprende filtros espaciales, es decir, combinaciones ponderadas de los canales (Lawhern et al., 2018)` | En EEGNet y en `scripts/red_cruda_41p.py` la primera capa es una convolución temporal; los filtros espaciales son la segunda (`VERIFICACION_REFERENCIAS.md`, ref. Lawhern, Figura 1). | `tras una convolución temporal, el primer bloque de la red aprende filtros espaciales, es decir, combinaciones ponderadas de los canales (Lawhern et al., 2018)` | Menor |
| 4 | RD 8.2 | `la mirada quieta del primer segundo puede ser espera.` | La prevalencia de etiqueta alta en el primer segundo es 0,51 (RD 7.2; INFORME del 18-11): está en la mediana, no es "quieta" en términos absolutos. Lo que hay es que es más quieta que la de los dos segundos siguientes. | `la mirada del primer segundo, más quieta que la de los dos siguientes (prevalencia 0,51 frente a 0,37–0,38; sección 7.2), puede ser espera.` | Menor |
| 5 | RD 7.9 | `cuya naturaleza no se estableció y que no informan sobre la etiqueta (sección 4.7).` | Afirma ausencia. Lo medido es una caída de 0,007 [−0,001; +0,015] al quitarlos (misma sección). | `cuya naturaleza no se estableció y cuya retirada casi no cambia la detección (sección 4.7).` | Menor |
| 6 | RD 8.3.2 | `son transitorios de gran amplitud frente al resto de la señal (sección 7.8)` | La sección 7.8 no compara con el resto de la señal, y 7.9 dice que los tres componentes oculares son una mediana de 3,5 % de la varianza. | `son transitorios de gran amplitud (unos 150 µV en los canales frontopolares; sección 7.8)` | Menor |
| 7 | RD 7.9, "Lectura" | `(0,06 como máximo en los del control)` | 0,06 es la mediana entre personas del puntaje más alto del control (`personas_limpieza.csv`, `score_control_max`: mediana 0,059, máximo 0,155). Leído suelto parece un tope. | `(en los del control, la mediana del puntaje más alto es 0,06)` | Menor |
| 8 | EN, pregunta 57 | `en el control, 0,06 como máximo.` | Igual que el 7. | `en el control, la mediana del puntaje más alto es 0,06.` | Menor |
| 9 | EN, guion hablado, lámina 4 | `Los datos son de la Toma de Muestra 2 del Fondecyt, en laboratorio, de agosto de 2025. El Tobii registra mirada, pupila y GSR en un mismo archivo; el EEG viene aparte, de un OpenBCI de 16 canales a 125 Hz. Los sincronicé por persona y hora, en ventanas de 2 segundos que avanzan de a 1. No hay expresión facial ni documentación del montaje. Y ojo: los sitios web son menos de un tercio de las ventanas de atención; el resto son textos, diseños e imágenes.` | "El resto son" omite los estímulos numerados, que son la categoría más grande de atención (6.637, más que los sitios web). | `Los datos son de la Toma de Muestra 2 del Fondecyt, en laboratorio, de agosto de 2025. El Tobii registra mirada, pupila y GSR en un archivo; el EEG viene aparte, de un OpenBCI de 16 canales a 125 Hz. Los sincronicé por persona y hora, en ventanas de 2 segundos con paso de 1. No hay expresión facial ni documentación del montaje. Ojo: los sitios web son menos de un tercio de las ventanas de atención; el resto son estímulos numerados, diseños, textos e imágenes.` (86 palabras, 147 por minuto) | Menor |
| 10 | RE, lámina 4, texto visible | `nombres de estímulo: cinco sitios web (Diario Financiero, Temu, Despegar…), textos, diseños e imágenes` | Igual que el 9. | `nombres de estímulo: cinco sitios web (Diario Financiero, Temu, Despegar…), textos, diseños, imágenes y estímulos numerados` (probado en la copia temporal: cabe en cinco líneas sin desbordar) | Menor |
| 11 | EN, pregunta 58 | `Es una razón más para leer la caída de 0,060 como cota inferior de la contribución ocular.` | La introducción de la sección 3 dice que 57, 58 y 11 se remiten entre sí; la 58 no remite a ninguna. | `Es una razón más para leer la caída de 0,060 como cota inferior de la contribución ocular (preguntas 11 y 57).` | Menor |
| 12 | CO 9.5, "Definición de las etiquetas" | `La de activación es en lo esencial el nivel tónico de la GSR relativo a la sesión y su soporte real excede los 6 s` | La precisión de O4 llegó a RD 6.1, RD 8.8, SP y CI, y no a CO. | `La de activación es en lo esencial la componente lenta de la GSR relativa a la sesión, que aquí se llama nivel tónico e incluye la acumulación de las respuestas (sección 6.1), y su soporte real excede los 6 s` | Menor |
| 13 | `notas/loop-revision-26-11-2026.md`, ronda 7 | `los parpadeos entran a la etiqueta de atención por pérdida de mirada` | Grado de certeza distinto del de los borradores, que dicen "pueden entrar" y "no se midió cuánto". | `los parpadeos pueden entrar a la etiqueta de atención por pérdida de mirada (no se midió cuánto)` | Menor |
| 14 | RE, lámina 28, tabla visible, fila "Origen" | `['Origen','La GSR depende del sistema simpático y de regiones de emoción y atención','EEG de 16 canales: AUC 0,52']` | RD 8.5 trata ahora el origen como una precisión y deja dos explicaciones; la lámina lo sigue mostrando como una de cuatro "razones", junto a la AUC de 0,52. Es el resto visible del argumento suprimido. | `['Origen','La GSR depende del sistema simpático y de regiones de emoción y atención; eso no impide que el EEG la refleje','EEG de 16 canales: AUC 0,52']` (no se probó cómo queda en pantalla) | Menor |

## 4. No propagado

1. **La oposición "parte fásica" frente a "nivel tónico"** sigue en la lista de frases corregidas de EN (error 1).
2. **"Navegación web" como descripción del contenido** sigue en RD 8.5 (error 2). Uso parecido y más leve en SP 4.6.5: "en navegación web ese brillo cambia con cada página". No se cuenta como error porque vale para cualquier estímulo en pantalla; conviene "en esta sesión".
3. **La precisión sobre el nivel tónico** no llegó a CO 9.5 (error 12) ni a CO 9.2 (línea 15, "la etiqueta es en lo esencial el nivel tónico de la respuesta galvánica de la piel"). La minuta (línea 10) y las láminas 5 y 23 conservan "nivel tónico" sin precisión; en la presentación la precisión está en la lámina 28 y en las preguntas 7 y 54, y basta.
4. **Los estímulos numerados** faltan en el guion hablado y en el texto visible de la lámina 4 (errores 9 y 10). CO 9.5 dice "que incluye textos, diseños e imágenes", que es correcto porque no pretende ser exhaustivo.
5. **Alcance de "no documentado".** RD 6.3 lo limita a los estímulos numerados, las imágenes `emotion` y `blur`, la tarea y las instrucciones. RD 8.8, CI, EN y la nota de la lámina 4 lo extienden a todo lo que no es sitio web ("textos, diseños, estímulos numerados e imágenes, cuyo contenido no está documentado"). Las dos cosas son ciertas (no hay descripción de ningún estímulo en el vault), pero un lector puede leerlas como distintas. Basta con que RD 6.3 diga, después de su frase, "tampoco está descrito el contenido de los textos y los diseños".
6. **Supresión del argumento de las regiones profundas.** Hecha en RD 8.5, en la nota de la lámina 28, en el guion hablado de la lámina 28 y en la pregunta 2 de EN; no queda en CO, SP, MI ni CI. El pendiente 23 lo registra. Queda la fila "Origen" de la tabla visible de la lámina 28 (error 14).

Coherencia que sí quedó bien: cifras de estímulos iguales en RD, MI, CI, EN y la nota de la lámina 4; saturación 2,5 % frente a 27,9 % igual en SP 5.3, EN 51 y la nota del bucle; medianas de los puntajes iguales en RD 7.9, EN (lista y pregunta 57) y la nota del bucle; "no se analizó" el movimiento en RD 8.4, RD 8.8, RD 8.9, CI, EN 27 y 56 y el pendiente 44; títulos de RD 8.4 y de la lámina 23 equivalentes; la minuta tiene 19 filas, como dice el pendiente 12; las secciones a las que remiten CI, CO y RD existen. Vocabulario vigente respetado en todo lo añadido: "respaldo" solo como rótulo, "apoyo parcial" solo para la hipótesis, "evidencia acotada", "cerca de un tercio", "Modelo Profesor con PCA", "activación".

## 5. Presentación

- Regenerada en una copia temporal fuera del repositorio (scripts copiados; `resultados/`, `scripts/` y `documentacion/` por enlace). `GUIÓN.md`, `index.html`, `FUENTES.md` y `LEEME.md` son idénticos byte a byte a los del commit. El repositorio quedó sin cambios.
- Los 33 títulos de las dos tablas de tiempo de EN son iguales a los de `GUIÓN.md`; también los seis anexos.
- Sumas de tiempo: 1.200 s y 600 s (17 láminas mostradas, 16 saltadas).
- Guion hablado: ninguna lámina supera 150 palabras por minuto. Las tocadas: lámina 4, 149; 15, 147; 22, 131; 23, 146; 28, 135. Los segundos del guion coinciden con la tabla.
- Preguntas: 66, numeradas de corrido. Ninguna línea `Corta:` supera 70 palabras; las preguntas 50 a 66 tienen entre 33 y 69 palabras; ninguna respuesta de más de 100 palabras quedó sin línea `Corta:`.
- Referencias cruzadas nuevas: 51→1, 54→7, 56→27, 57→11, 60→15 y 41, 63→10, 66→20 y 7→54 apuntan a la pregunta correcta. Falta la de la 58 (error 11).
- Capturas de las láminas 4, 23, 27 y 28 (1280 × 720): sin desbordes ni cortes. El título de la 23 ocupa dos líneas y cabe. Los pies de la 27 y la 28 terminan en "referencias en el anexo F". Las capturas quedaron en `/private/tmp/claude-501/-Users-mario/bfaa0f9d-b2ac-4cab-9a3d-852bdb888a53/scratchpad/ronda8/`.

## 6. Reglas del proyecto

- Nada de lo añadido afirma aprobación del profesor guía. Ninguna de las siete decisiones se cierra: la fila nueva de la minuta ofrece dos redacciones como opciones, y las imágenes `emotion` se remiten a la decisión abierta sobre validación externa.
- El diff no toca `Estructura Tesis.md`, ningún `INFORME.md`, ningún CSV, ningún protocolo ni ningún script. El único archivo nuevo es el informe de la ronda 7. No hay archivos nuevos en `resultados/`.

## 7. Legibilidad y volumen

RD creció unas 2.200 palabras en este commit. El crecimiento es casi todo salvedad: de los 30 bloques añadidos a RD, 4 son hechos de método que faltaban (6.2, 6.3, 7.7, 7.8) y el resto son reservas. No se propone quitar ningún hecho ni salvedad; se propone que cada uno viva en un solo lugar.

### 7.1 Dónde debe vivir cada cosa

| Hecho o salvedad | Dónde aparece hoy en RD | Dónde debe vivir | En los demás lugares |
|---|---|---|---|
| Composición de los estímulos | 6.3 (viñeta del glosario), 8.2, 8.8 | 6.3, como párrafo propio con tabla (caso 1) | remisión |
| Calidad del EEG como registro | 7.9, 8.3.3, 8.5, 8.8 (y SP 4.7, 5.3) | SP 4.7 | 8.5 conserva la frase de la disyuntiva; 7.9, 8.3.3 y 8.8, remisión (ya lo son) |
| Componente lenta y nivel tónico | 6.1, 8.5, dos viñetas de 8.8 (y SP 4.5.2, 4.6.3) | SP 4.6.3, con la definición en RD 6.1 | una sola viñeta en 8.8 (caso 5) |
| Potencia absoluta en alfa y beta | 7.7 y 8.3.2 | 7.7 | 8.3.2 ya es casi una remisión; está bien |
| Definición de parpadeo | 6.2, 7.8 (dos veces en el mismo párrafo) (y SP 4.6.4) | SP 4.6.4 | 7.8: basta la frase final; el paréntesis del inicio ya dice cómo se midió |
| Espiga sacádica no tratada | 7.9, 8.3.3, 8.8 | 7.9 | remisión (ya lo son) |
| Sentido de "alta" no establecido | 6.1 (tres frases seguidas y una cuarta al final), 8.8 | 6.1, en una frase | 8.8, remisión (ya lo es) |

### 7.2 Secciones donde las salvedades apiladas ya impiden ver qué se afirma

- **RD 8.4**, párrafo "Lo que el historial aportaría es, con mayor probabilidad…": 230 palabras con una afirmación y siete reservas. La afirmación ("un resumen del historial reciente y no dinámica dentro del estímulo") está en la octava frase. Con el párrafo nuevo de la respuesta al cambio de estímulo, la sección ofrece cinco lecturas alternativas en cuatro párrafos sin numerarlas.
- **RD 8.5**, párrafo inicial (caso 4).
- **RD 8.2**, párrafo "La lectura más coherente…" (caso 3).
- **RD 8.3.3**: "al menos cuatro candidatos", después "una vía que no pasa por el movimiento de los ojos", después "las cuatro fuentes fisiológicas" y "una quinta posibilidad". El lector no sabe si los parpadeos son el quinto o no. Basta numerarlos: cinco fisiológicos y uno de procesamiento.
- **RD 8.8**: 1.492 palabras y 35 viñetas. La frase inicial promete que cada limitación "se enuncia aquí una vez"; con este commit el nivel tónico tiene dos viñetas.
- **RD 6.1**, párrafo "Aunque el *Modelo Profesor* recibe mirada y pupila…": "No designa mayor atención en ningún sentido validado. Tampoco está establecido su sentido… 'Alta' y 'baja' son los rótulos del diseño, no una dirección comprobada del constructo", y dos párrafos después, "nombran la etiqueta definida, no el constructo".
- **SP 4.6.1**, "Equipos y programas": la frase "No constan…" encadena cuatro grupos con "ni" y punto y coma; se lee mejor como lista de cuatro viñetas (seguidor ocular y pantalla; EEG; GSR; sala).

### 7.3 Los cinco peores casos, con texto exacto

**Caso 1. RD 6.3, viñeta "Estímulo" del glosario.** Una definición de términos carga 13 cifras.

Texto actual:

> - *Estímulo* es cada página o imagen que se presenta. Por su nombre en la exportación se distinguen siete categorías: sitios web, textos, diseños, estímulos identificados solo con un número, imágenes rotuladas `emotion`, imágenes rotuladas `blur` e instrucciones. La categoría se asigna por el nombre del estímulo, no por su contenido: el contenido y el propósito de los estímulos numerados y de las imágenes `emotion` y `blur`, la tarea y las instrucciones no están documentados en las notas y deben pedirse al proyecto. De las 22.176 ventanas con etiqueta de atención, 6.423 corresponden a sitios web (29 %), 6.637 a estímulos numerados, 4.082 a diseños, 2.255 a textos, 1.792 a imágenes `emotion`, 891 a imágenes `blur` y 96 a instrucciones. De las 11.796 con etiqueta de activación, 5.457 corresponden a sitios web (46 %), 3.291 a estímulos numerados, 1.316 a diseños, 1.285 a textos, 401 a imágenes `emotion` y 46 a instrucciones; ninguna a imágenes `blur`. Los sitios web son cinco. La exportación trae 116 nombres de estímulo distintos, 95 si no se cuenta el sufijo de repetición; ninguna de las dos cifras es un conteo comprobado de contenidos distintos. "Navegación web" nombra, entonces, el contexto del experimento y no el contenido de la mayoría de las ventanas. "Página" se usa como sinónimo de estímulo al hablar de lo que la persona ve, también cuando el estímulo es una imagen.

Texto propuesto (la viñeta, y un párrafo nuevo después de la lista de términos):

> - *Estímulo* es cada página o imagen que se presenta. "Página" se usa como sinónimo de estímulo al hablar de lo que la persona ve, también cuando el estímulo es una imagen. Sus categorías están en "Composición de los estímulos", al final de esta lista.

> **Composición de los estímulos.** Por su nombre en la exportación se distinguen siete categorías. La categoría se asigna por el nombre del estímulo, no por su contenido: el contenido y el propósito de los estímulos numerados y de las imágenes `emotion` y `blur`, la tarea y las instrucciones no están documentados en las notas y deben pedirse al proyecto.
>
> | Categoría | Ventanas con etiqueta de atención | Ventanas con etiqueta de activación |
> |---|---:|---:|
> | Sitios web (cinco) | 6.423 (29 %) | 5.457 (46 %) |
> | Estímulos identificados solo con un número | 6.637 | 3.291 |
> | Diseños | 4.082 | 1.316 |
> | Textos | 2.255 | 1.285 |
> | Imágenes rotuladas `emotion` | 1.792 | 401 |
> | Imágenes rotuladas `blur` | 891 | 0 |
> | Instrucciones | 96 | 46 |
> | Total | 22.176 | 11.796 |
>
> La exportación trae 116 nombres de estímulo distintos, 95 si no se cuenta el sufijo de repetición; ninguna de las dos cifras es un conteo comprobado de contenidos distintos. "Navegación web" nombra, entonces, el contexto del experimento y no el contenido de la mayoría de las ventanas.

**Caso 2. RD 6.2, párrafo "Análisis del EEG (22 y 23-11)".** Un solo párrafo de unas 300 palabras con tres métodos y un paréntesis de 45 palabras dentro de una frase.

Texto actual (desde "La limpieza ocular se hizo" hasta el final del párrafo):

> La limpieza ocular se hizo por persona con análisis de componentes independientes (ICA, algoritmo FastICA), ajustado sobre la sesión completa filtrada entre 1 y 45 Hz y con el filtro de red, con tantos componentes como canales utilizables y sin las muestras a menos de 1 s de una saturación. Cada componente recibe un puntaje ocular: su correlación máxima, entre 1 y 15 Hz, con la mirada horizontal, la mirada vertical o los parpadeos del seguidor ocular (definición de parpadeo en la sección 4.6.4). Se quitan los tres de mayor puntaje, sea cual sea su valor: no hay un umbral. Como control se quitan los tres componentes de mayor varianza entre los que no están entre los cuatro de mayor puntaje ocular; en adelante, "no oculares". Por último, se entrenó una red convolucional compacta del tipo EEGNet (1.217 parámetros) sobre la señal de 16 canales y 2 s, filtrada como en la extracción de variables y sin variables calculadas a mano (en adelante, "señal cruda", como en los informes y las láminas; el nombre abrevia "sin variables calculadas": la señal está filtrada, escalada por persona y canal con toda la sesión y recortada a ±8 unidades de esa escala), con una sola arquitectura y configuración fijadas de antemano, sin búsqueda. En estos análisis, "modelo de referencia" designa al HGB con variables calculadas.

Texto propuesto (tres párrafos; el primero conserva las dos frases iniciales del párrafo actual, sin cambios):

> **Limpieza ocular.** Se hizo por persona con análisis de componentes independientes (ICA, algoritmo FastICA). El ajuste usa la sesión completa filtrada entre 1 y 45 Hz y con el filtro de red, tantos componentes como canales utilizables, y deja fuera las muestras a menos de 1 s de una saturación. Cada componente recibe un puntaje ocular: su correlación máxima, entre 1 y 15 Hz, con la mirada horizontal, la mirada vertical o los parpadeos del seguidor ocular (definición de parpadeo en la sección 4.6.4). Se quitan los tres de mayor puntaje, sea cual sea su valor: no hay un umbral. Como control se quitan los tres componentes de mayor varianza entre los que no están entre los cuatro de mayor puntaje ocular; en adelante, "no oculares".

> **Red convolucional.** Por último, se entrenó una red convolucional compacta del tipo EEGNet (1.217 parámetros) sobre la señal de 16 canales y 2 s, con una sola arquitectura y configuración fijadas de antemano, sin búsqueda. La señal que recibe está filtrada como en la extracción de variables, escalada por persona y canal con toda la sesión y recortada a ±8 unidades de esa escala. Se la llama "señal cruda", como en los informes y las láminas; el nombre abrevia "sin variables calculadas a mano". En estos análisis, "modelo de referencia" designa al HGB con variables calculadas.

**Caso 3. RD 8.2, segunda mitad del párrafo "La lectura más coherente…".** "Una… La otra… Otras dos": la cuenta no se sigue, y la explicación del desplazamiento quedó sin su razón.

Texto actual:

> Hay otras explicaciones que no se separaron. Una es de cálculo: la duración de cada fijación se suma completa aunque exceda la ventana (la suma supera los 2.000 ms en cerca del 28 % de las ventanas etiquetadas), y las ventanas no cruzan el cambio de estímulo, lo que por sí solo acorta las duraciones al inicio de cada página. La otra es de composición: las posiciones tardías solo existen en los estímulos largos, de modo que la prevalencia por posición mezcla el tiempo transcurrido con el tipo de estímulo, y los tipos son muy distintos entre sí (sección 6.3). Otras dos dependen de información del protocolo que no consta. Si al inicio de cada estímulo hay un tiempo de carga o una pantalla en blanco, la mirada quieta del primer segundo puede ser espera. Y no consta si los sitios web permitían desplazar la página. La exportación trae la posición del área visible del navegador y la del mouse, que permitirían comprobarlo; no se usaron.

Texto propuesto (incluye la corrección del error 4):

> Hay cuatro explicaciones más que no se separaron. La primera es de cálculo: la duración de cada fijación se suma completa aunque exceda la ventana (la suma supera los 2.000 ms en cerca del 28 % de las ventanas etiquetadas), y las ventanas no cruzan el cambio de estímulo, lo que por sí solo acorta las duraciones al inicio de cada página. La segunda es de composición: las posiciones tardías solo existen en los estímulos largos, de modo que la prevalencia por posición mezcla el tiempo transcurrido con el tipo de estímulo, y los tipos son muy distintos entre sí (sección 6.3). Las otras dos dependen de información del protocolo que no consta. La tercera es la espera: si al inicio de cada estímulo hay un tiempo de carga o una pantalla en blanco, la mirada del primer segundo, más quieta que la de los dos siguientes (prevalencia 0,51 frente a 0,37–0,38; sección 7.2), puede ser espera. La cuarta es el desplazamiento de la página: no consta si los sitios web lo permitían, y no se examinó cómo clasifica el filtro de fijaciones un contenido que se mueve. La exportación trae la posición del área visible del navegador y la del mouse, que permitirían comprobarlo; no se usaron.

**Caso 4. RD 8.5, párrafo inicial.** Cuatro explicaciones presentadas como "una más simple", "una equivalente" y "después de una precisión, dos".

Texto actual:

> Con la ventana actual, ningún modelo queda claramente por sobre el azar en activación, y no se demostró aporte del EEG de la ventana actual (sección 7.11). Antes de las explicaciones fisiológicas hay una más simple que el diseño no descarta: que el *Arousal Score* por ventana refleje poco la activación. No se validó contra ninguna medida externa y no tiene control de artefactos sobre la señal cruda. Hay una explicación equivalente del lado de la entrada: la calidad del EEG como registro de actividad cerebral no está establecida (sección 4.7), de modo que el resultado no permite distinguir entre "el EEG no informa sobre el *Arousal Score*" y "este registro no lo permite". La fisiología de la respuesta electrodérmica ofrece, después de una precisión sobre el origen de la señal, dos explicaciones compatibles con este resultado: la escala temporal y el tipo de relación.

Texto propuesto:

> Con la ventana actual, ningún modelo queda claramente por sobre el azar en activación, y no se demostró aporte del EEG de la ventana actual (sección 7.11). Hay cuatro explicaciones que el diseño no separa. Dos son anteriores a la fisiología. La primera es de la etiqueta: el *Arousal Score* por ventana puede reflejar poco la activación, porque no se validó contra ninguna medida externa y no tiene control de artefactos sobre la señal cruda. La segunda es de la entrada: la calidad del EEG como registro de actividad cerebral no está establecida (sección 4.7), de modo que el resultado no permite distinguir entre "el EEG no informa sobre el *Arousal Score*" y "este registro no lo permite". Las otras dos vienen de la fisiología de la respuesta electrodérmica y se desarrollan abajo, después de una precisión sobre el origen de la señal: la escala temporal y el tipo de relación.

**Caso 5. RD 8.8, "Etiquetas": dos viñetas para el nivel tónico.** La lista promete enunciar cada limitación una vez.

Texto actual (cuarta y séptima viñetas de "Etiquetas"):

> - La etiqueta de activación es en lo esencial el nivel tónico de la GSR relativo a la sesión, y su soporte real excede los 6 s nominales hacia el pasado y hacia el futuro: el contraste "sin las ventanas de la etiqueta" no excluye ese soporte (secciones 6.1 y 7.3).

> - Lo que aquí se llama nivel tónico es la componente lenta de la GSR, que incluye la acumulación de las respuestas, y el conteo de SCR no se validó (sección 4.6.3).

Texto propuesto (una sola viñeta en el lugar de la cuarta; la séptima se elimina):

> - La etiqueta de activación es en lo esencial la componente lenta de la GSR relativa a la sesión, que aquí se llama nivel tónico e incluye la acumulación de las respuestas; el conteo de SCR no se validó (sección 4.6.3). Su soporte real excede los 6 s nominales hacia el pasado y hacia el futuro: el contraste "sin las ventanas de la etiqueta" no excluye ese soporte (secciones 6.1 y 7.3).

## 8. Fuentes consultadas

`resultados/ampliacion_41p_16-11-2026/por_categoria.csv`; `resultados/preprocesamiento/caracteristicas_multimodales.csv`; `resultados/modelado/particion_participantes.csv`; `resultados/eda/eeg/eeg_resumen.json` y `eeg_resumen_sesiones.csv`; `resultados/eda/eye_pupil/resumen_numerico.csv` y `metadata.json`; `resultados/limpieza_ocular_41p_23-11-2026/personas_limpieza.csv` e `INFORME.md`; `resultados/montaje_ocular_41p_23-11-2026/INFORME.md` y `personas.csv`; `resultados/explicativo_posicion_41p_18-11-2026/INFORME.md`; `scripts/ampliacion_41p.py`, `eeg_por_canal_v2.py`, `preprocesamiento_secuencial.py`, `limpieza_ocular_41p.py`, `montaje_ocular_41p.py`, `enfoques_41p.py`, `red_cruda_41p.py`; `Analisis de Datos/DOCUMENTACION_DATOS_MDS.md`, `EDA_EEG.md`, `EDA_EYE_PUPIL.md`; `documentacion/auditoria_final_23-11-2026/VERIFICACION_REFERENCIAS.md`, `ronda6/RECALCULO_DESCRIPTIVOS.md` y `ronda7/TERCERA_LECTURA_ESPECIALISTA.md`. Fecha: 27-11-2026.
