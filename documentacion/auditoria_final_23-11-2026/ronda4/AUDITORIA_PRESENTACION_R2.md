# Auditoría de la presentación, ronda 4 (segunda revisión completa)

Fecha: 26-11-2026. Revisión independiente de `presentaciones/avances_tesis_06-11-2026/` (versión 7; `index.html`, `GUIÓN.md`, `FUENTES.md` y `LEEME.md` generados el 26-11-2026 a las 20:15). Solo revisión: no se modificó ningún archivo existente ni se hizo commit. Hecha con un asistente automático a pedido del autor; no es la revisión de un tercero.

## Resultado

- **Bloqueantes: 0.** Ninguna lámina tiene texto cortado ni desbordado, ningún título pasa de dos líneas, ninguna cifra visible difiere de su CSV.
- **Importantes: 8** (5 en `relato.py`, 3 en `ENSAYO.md`). Son de lectura, coherencia y tiempo; ninguno es de cifras.
- **Menores: 22.**
- `index.html` y `GUIÓN.md` coinciden con `relato.py` (títulos, cuerpos, pies y notas de las 39 láminas). Las 41 rutas de `FUENTES.md` existen y son exactamente las que cita `relato.py`. Los 29 CSV de entrada de los gráficos conservan el hash registrado en `graficos/auditoria_graficos.json`.

## Qué se revisó y cómo

- **Visual:** 39 capturas con Chrome headless a 1280×720, vistas una por una. Están en `/private/tmp/claude-501/-Users-mario/bfaa0f9d-b2ac-4cab-9a3d-852bdb888a53/scratchpad/ronda4_pres/` (`l01.png` a `l39.png`; carpeta temporal).
- **Cifras:** cada número visible y de las notas contra el CSV de su etapa, redondeando desde el valor completo (tabla al final).
- **Referencia de contenido:** `documentacion/Cierre_Experimental_Final_23-11-2026.md` y `Escritura/Borrador Conclusiones 23-11-2026.md`.
- **`ENSAYO.md`:** plan de tiempo (sumas), guion hablado lámina por lámina contra `relato.py`, las 37 preguntas, referencias cruzadas a láminas y preguntas, y largo en palabras.

**No se comprobó:** el gráfico de la lámina 22 no se recalculó (necesita `cierre_experimental_v3.load_data()`); se contrastó con `e1_descriptivos.csv` (0,51; 0,37; 0,38 en los tres primeros tramos). La tabla de literatura de la lámina 7. Los parámetros de la lámina 37 más allá de `protocolo.json` citado. De `ENSAYO.md`: 1.217 parámetros de la red (pregunta 12), medianas +0,014 y +0,042 y el +0,028 sin la persona más influyente (pregunta 17), importancias 0,021 y 0,053 (pregunta 20), "menos del 2 %" (pregunta 9); todas coinciden con el cierre o los informes citados, pero no se recalcularon.

## Hallazgos importantes

| # | Dónde | Tipo | Texto actual | Problema | Corrección propuesta |
|---|---|---|---|---|---|
| I1 | Lámina 27, nota (`relato.py`) y guion de la lámina 27 (`ENSAYO.md`) | Lectura que excede el cierre | `Lo que detecto es, al menos en un tercio, lo Observado, y no puedo afirmar que sea lo Atendido.` | Afirma que un tercio de la detección **es** lo Observado. Lo medido es que cerca de un tercio **depende de componentes ligados a la mirada**, leído como cota inferior y sin ser una demostración. Es la lectura que el propio `ENSAYO.md` prohíbe ("un tercio es la huella de los ojos"). La fila 27 del plan de tiempo ya lo dice bien. | `Cerca de un tercio de lo que detecto depende de componentes ligados a lo Observado; lo leo como cota inferior, no es una demostración, y no puedo afirmar que el resto sea lo Atendido.` (igual en la nota y en el guion) |
| I2 | Lámina 11, nota (`relato.py`) y guion de la lámina 11 (`ENSAYO.md`) | Salvedad obligatoria ausente | Nota: `Elijo los hiperparámetros solo dentro de entrenamiento. Después congelo esa configuración y la evalúo con las 41 personas en validación cruzada por persona.` Guion: `Elijo la configuración solo con las 25 personas de entrenamiento y la congelo. Después la evalúo con las 41 personas en validación cruzada por persona, igual para el modelo con y sin historial.` | Es exactamente la frase que "Lo que no se puede decir" prohíbe sin más ("La configuración se eligió solo con entrenamiento"). La salvedad está en la lámina 18, siete láminas después; la lámina 11 es donde el profesor preguntará. | Nota: `Elijo los hiperparámetros solo dentro de entrenamiento. Después congelo esa configuración y la evalúo con las 41 personas en validación cruzada por persona. Ojo: esas 25 personas son parte de las 41 que después evalúo, y en activación la elección la decidió el modelo con historial; el detalle va en la lámina 18.` Guion: agregar tras la segunda frase `Ojo: esas 25 son parte de las 41 que evalúo, y en activación la elección la decidió el modelo con historial; lo detallo en la lámina 18.` |
| I3 | Lámina 23, pie (`relato.py`) | Dato inexacto y pie largo (3 líneas) | `Historial sin las 6 ventanas que usa la etiqueta, contra un placebo con la misma cantidad de ventanas. Filas 3 y 4: historial completo contra un modelo que solo conoce los segundos en la página. Repetido con 5 particiones (22-11): frente a la posición, +0,032 [+0,004; +0,059], inconcluso tras Holm.` | La etiqueta usa **cinco** ventanas seguidas, que cubren 6 s (láminas 17 y 22; `etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md`); lo que vale 6 es el desplazamiento. "Que usa la etiqueta" además sugiere que no queda solapamiento, lectura que la nota de la misma lámina desmiente. "Repetido" se puede leer como repetición del +0,046. | `Filas 1 y 2: historial sin las ventanas de 6 s que promedia la etiqueta, contra un placebo igual de largo. Filas 3 y 4: historial completo contra un modelo que solo conoce los segundos en la página; el 22-11, con 5 particiones, +0,032 [+0,004; +0,059], inconcluso tras Holm.` (sin cifras nuevas; queda en 3 líneas justas o 2) |
| I4 | Láminas 12 (nota), 33 (cuerpo) y 2 (índice) | Coherencia: decisiones anunciadas, mostradas y dichas | Lámina 12, nota: `cuál queda como definición es una decisión que le traigo`. Lámina 33: título `Necesito decidir cinco cosas con usted` y cinco preguntas; la nota agrega `Hay dos puntos más que no caben en la lámina y que pueden pesar más que los anteriores`. | El cierre y la minuta listan **siete** decisiones. La que la lámina 12 promete (profesor PCA o pesos iguales) no aparece en pantalla en la 33, y las dos que "pueden pesar más" solo se dicen de palabra. La lámina 33 tiene espacio libre bajo la lista (termina a dos tercios de la altura). | Agregar un pie a la lámina 33, después de `</ol>`: `+caption('En la minuta van dos puntos más: normalizar las etiquetas con la sesión completa y usar el Modelo Profesor con PCA como definición del Attention Score.')`. Título, índice y portada pueden seguir diciendo "cinco". |
| I5 | Lámina 27, fila 3 de la tabla (`relato.py`) | Dato de literatura en la columna "En mis datos" | `['Músculos del ojo al iniciar una sacada','Descarga breve de banda ancha','Llega a beta alta (20 a 90 Hz); no explica por sí sola la caída en alfa']` | "20 a 90 Hz" es la banda del potencial de espiga sacádica según el resumen de Keren et al. (2010), no un resultado propio; "beta alta" no es 20 a 90 Hz; y el EEG de la tesis está filtrado a 1–45 Hz (lámina 10). | `['Músculos del ojo al iniciar una sacada','Descarga breve de banda ancha (unos 20 a 90 Hz)','Compatible con parte de la caída en beta; no explica la de alfa']` |
| I6 | Lámina 31, puntos 1 y 4 (`relato.py`) | Dice más que las conclusiones vigentes | Punto 1: `<b>En atención, al menos un tercio de lo que detecta el EEG depende de los ojos.</b>` Punto 4: `<b>El aporte es doble.</b>` | Punto 1: el cierre dice "depende de componentes ligados a los ojos". Punto 4: el encuadre es la quinta decisión abierta; las conclusiones (9.7) dicen "sería entonces doble (encuadre provisorio)". | Punto 1: `<b>En atención, al menos un tercio de lo que detecta el EEG depende de componentes ligados a los ojos.</b>` (queda en una línea a 24 px; si pasa a dos, usar `cerca de un tercio`). Punto 4: `<b>El aporte sería doble (encuadre por decidir).</b>` |
| I7 | `ENSAYO.md`, plan de tiempo y guion de 20 minutos | El guion no cabe en el tiempo asignado | Total 1.200 s para 3.120 palabras (156 palabras por minuto sin pausas ni transiciones). Por lámina: 30 (156 palabras en 40 s, 234 ppm), 20 (72 en 20 s, 216), 12 (70 en 20 s, 210), 31 (138 en 40 s, 207), 10 (85 en 25 s, 204), 18 (181 en 55 s, 197), 23 (180 en 55 s, 196), 33 (240 en 75 s, 192), 1 (77 en 25 s, 185). | A 140 ppm el guion dura 22 min 17 s. Las láminas "clave" 18, 23 y 33 son las que más se pasan. | Recortes exactos en la sección "Reemplazos de guion" de este informe (láminas 30 y 31: −70 palabras; aun así quedan en unos 165 ppm, así que conviene además pasar la 30 de 40 a 45 s tomando 5 s de la 9). Además: mover 15 s de la lámina 13 (49 palabras en 30 s) y 10 s de la 17 (41 en 30 s) a las láminas 18 y 23; y pasar las láminas 12 y 20 de 20 a 25 s tomando 5 s de la 14 y 5 s de la 16. Los subtotales por bloque cambian: 12 a 17, 135 s; 18 a 23, 270 s. |
| I8 | `ENSAYO.md`, sección 3 | Respuestas demasiado largas para decirlas | 22 de las 37 respuestas pasan de 100 palabras (más de 40 s a 150 ppm). Las peores: 37 (214 palabras, 86 s), 4 (197, 79 s), 12 (190, 76 s), 11 (181, 72 s), 5 (165), 13 (165), 1 (161), 25 (161), 22 (152), 15 (151), 16 (143). | Sirven como ficha de estudio, no como respuesta hablada. | Anteponer a cada respuesta larga una línea `Corta:` con lo que se dice primero; el resto queda "si repregunta". Versiones cortas de las cuatro peores en la sección "Respuestas cortas" de este informe (solo frases y cifras que ya están en la respuesta actual). |

### Reemplazos de guion (I7)

**Lámina 30** (de 156 a 109 palabras; ninguna cifra nueva):

> **Lámina 30 · Conclusiones: apoyo parcial (40 s).** Son las conclusiones del borrador del capítulo 9. La hipótesis tiene apoyo parcial, y viene solo de activación; lo que tiene apoyo es un resumen del historial reciente, no un modelo secuencial ni la combinación de señales. El efecto se sostiene frente al placebo, pero es pequeño, desigual entre personas —mejoran 23 de 41, y se concentra en las 25 con que elegí la configuración— y solo tiene respaldo para los 6 segundos anteriores. Al controlar la posición conserva su tamaño, +0,032, pero queda inconcluso. En atención, lo que parecía temporal era la posición dentro de la página. Y el orden de las ventanas no aportó de forma demostrable.

**Lámina 31** (de 138 a 115 palabras):

> **Lámina 31 · Conclusiones: qué detecta el EEG (40 s).** En atención, al menos un tercio de lo que detecta el EEG depende de componentes ligados a los ojos, y lo leo como cota inferior. Un modelo más complejo no cambia qué se detecta: la red llega a 0,716 pero pierde 0,067 al limpiar. La conclusión metodológica más importante es la tercera: separar las señales no asegura independencia fisiológica. La etiqueta se define con lo Observado y el EEG registra esa misma conducta, así que no puedo afirmar que detecte lo Atendido. El aporte sería doble: evidencia acotada sobre el historial en activación, y una advertencia sobre evaluar modelos de EEG con etiquetas oculares. Todo supone, de forma provisoria, las decisiones de la última lámina.

### Respuestas cortas (I8)

- **Pregunta 37.** `Corta: Puede favorecerlo. Las 15 hojas las elegí con las 25 personas de entrenamiento y la elección la decidió el modelo con historial; esas 25 son parte de las 41 que evalúo y el contraste principal se concentra en ellas: +0,055 frente a +0,001 en las otras 16. No está demostrado que esté inflado, y el contraste frente al placebo es positivo en los dos grupos (+0,035 y +0,064). Una sensibilidad con 7 hojas lo resolvería; no la corrí.`
- **Pregunta 4.** `Corta: No lo puedo descartar del todo, y por eso no presento nada como confirmatorio. Cada protocolo entró a Git antes que sus predicciones y cada etapa se ejecutó una vez, con Holm dentro de su familia. Pero son doce etapas sobre las mismas 41 personas, y Holm no corrige entre etapas. La única salida limpia es una cohorte nueva con el contraste fijado de antemano.`
- **Pregunta 12.** `Corta: No lo sé. Probé una sola arquitectura, sin búsqueda. Le ganó al modelo de referencia por +0,035, y al limpiar el EEG perdió 0,067: su detección depende de lo ocular. Su ventaja sobre el modelo de referencia se mantiene con el EEG limpio (+0,028), así que no puedo decir que la ventaja sea ocular. Tampoco puedo separar arquitectura de normalización por persona.`
- **Pregunta 11.** `Corta: En parte sí es esperable. El experimento mide cuánto depende la detección de los componentes más ligados a la mirada; no distingue artefacto de actividad cerebral acoplada a los ojos. El control muestra que no es un efecto de quitar varianza, pero no está igualado en su relación con la etiqueta. "Cota inferior" es mi lectura más defendible, porque la limpieza fue parcial; no es una demostración.`

## Hallazgos menores

| # | Dónde | Tipo | Texto actual | Corrección propuesta |
|---|---|---|---|---|
| M1 | Lámina 2, nota; guion de la lámina 2 | Coherencia con la portada | `Lo nuevo desde la última reunión son las tres últimas: qué explica la mejora, qué detecta el EEG y las conclusiones.` La portada dice que lo nuevo incluye haber repetido todo con 41 personas (parte 6). | `Lo nuevo desde la última reunión va desde los resultados con 41 personas: de dónde viene la mejora, qué detecta el EEG y las conclusiones.` (confirmar con Mario qué vio el profesor en la última reunión) |
| M2 | Lámina 12, eje del gráfico (`estilo_tecnico.py`, línea 166) | Rótulo desactualizado | `AUC en entrenamiento (OOF)` | `AUC en entrenamiento (cada persona, sin ella en el ajuste)` |
| M3 | Lámina 38, rótulo de la cuarta barra (`estilo_tecnico.py`, línea 224) y lámina 37, última fila (`relato.py`) | Sigla sin explicar | `Activación · variabilidad de entrenamiento (OOF)`; `30 ajustes internos · 15 OOF · 3 finales` | `Activación · variabilidad de entrenamiento (fuera de muestra)`; `30 ajustes internos · 15 fuera de muestra · 3 finales` |
| M4 | Lámina 12 | Título y gráfico no muestran lo mismo | El título habla de la coincidencia (66 %), que solo aparece en el pie; el gráfico muestra que PCA se predice mejor, justo lo que la nota pide no leer como validez. | Agregar al pie: ` Que una se prediga mejor no la valida.` |
| M5 | Lámina 21, rótulo de la cuarta fila (`estilo_tecnico.py`, línea 290) y pie | Rótulo y fecha | `Historial sin los 6 s de la etiqueta`; el pie no dice de cuándo son las cifras (16 y 18-11) | Rótulo: `Historial sin las ventanas de 6 s de la etiqueta`. Pie: agregar ` Cifras del 16 y 18-11.` |
| M6 | Lámina 23, nota; guion de la lámina 23 | Cifra sin fuente única | `AUC alrededor de 0,57` (los CSV dan 0,554 con 5 particiones el 22-11, 0,563 el 16-11 y 0,582 en la banda de 6 s) | `la AUC queda entre 0,55 y 0,58 según el análisis` |
| M7 | Lámina 24, nota | Verbo más fuerte que el cierre | `Ese patrón además respalda el montaje por defecto` (el cierre y el guion del ensayo dicen "compatible") | `Ese patrón además es compatible con el montaje por defecto` |
| M8 | Lámina 24, título y pie | Precisión | Título `Los movimientos de los ojos se ven en el EEG` con un gráfico solo de parpadeos; pie `mediana de las 41 personas` (cada canal es utilizable en 33 a 41 personas, `resumen_canales.csv`) | Título: `Los parpadeos y los movimientos de los ojos se ven en el EEG`. Pie: `mediana de las personas con ese canal utilizable (33 a 41)` |
| M9 | Láminas 27 y 28, pie | Puntuación y repetición (la salvedad está tres veces en pantalla: 27, 28 y 39) | `Interpretación propia; 8 de las 18 referencias, contrastadas solo con el resumen.` | `Interpretación propia; 8 de las 18 referencias las contrasté solo con el resumen (anexo F).` |
| M10 | Lámina 28, fila "Tiempos" | Verbo más fuerte que "respaldo" | `El historial de los 6 s previos sí ayuda` | `Solo hay respaldo para los 6 s previos` |
| M11 | Lámina 29, pie | Pie denso (2 líneas, 6 cifras y 5 fechas) | `Apoyo parcial, y viene de activación. Fila 1 y el +0,001: 5 particiones, 22-11 (el 16-11 dio +0,026 y +0,034). El +0,046: contraste registrado el 16-11; la curva del 22-11 da +0,047 a 6 s. GRU y fusión: 16-11. EEG: 23-11.` | `Apoyo parcial, y viene de activación. Fila 1 y el +0,001: 22-11, 5 particiones. El +0,046, GRU y fusión: 16-11. EEG: 23-11.` (el +0,026, el +0,034 y el +0,047 ya están en las láminas 18 y 30 o en sus notas) |
| M12 | Lámina 30, cuerpo | Sobrecarga: 138 palabras y 12 cifras; no se lee en 30 s | Punto 1: `Con historial: +0,036 [+0,010; +0,065]; mejoran 23 de 41 personas y se concentra en las 25 con que elegí la configuración. Frente al placebo y sin las ventanas de la etiqueta: +0,046 [+0,018; +0,073], registrado antes. Al controlar la posición: +0,032, inconcluso.` Punto 2: `A 12 s es inconcluso (+0,024) y desde los 24 s no se distingue del placebo, sin demostrar que desaparezca. AUC bajas: 0,50 a 0,59.` | Punto 1: `Frente al placebo y sin las ventanas de la etiqueta: +0,046 [+0,018; +0,073], registrado antes. Con historial: +0,036 [+0,010; +0,065], concentrado en las 25 personas con que elegí la configuración.` Punto 2: `A 12 s es inconcluso y desde los 24 s no se distingue del placebo, sin demostrar que desaparezca. Al controlar la posición: +0,032, inconcluso. AUC bajas: 0,50 a 0,59.` Puntos 3 y 4 sin cambios. Sin cifras nuevas; salen de pantalla "23 de 41" y "+0,024", que siguen en el guion y en la nota. |
| M13 | Lámina 30, punto 4 | Encabezado y contenido | Encabezado `El orden de las ventanas no aportó de forma demostrable.` con una frase de fusión debajo | `Ni el orden de las ventanas ni el tipo de fusión aportaron de forma demostrable.` |
| M14 | Láminas 1 (nota), 29 y 31 | Redondeo | `al menos un tercio` (0,060 de 0,181 es 33,2 %; el cierre usa "al menos un tercio" en la tabla y "cerca de un tercio" en el texto y en las conclusiones) | Unificar en `cerca de un tercio, como cota inferior` si se quiere el rótulo exacto; no contradice al cierre tal como está |
| M15 | Láminas 5 y 33 (cuerpo) y 15 (título) | Tipografía | Comillas rectas `"Alta"`, `"mejor"`, `"emociones"`, `"inferior"`; la lámina 3 y las notas usan comillas curvas | Usar `“ ”` en todo el texto visible |
| M16 | Notas de las láminas 5 y 33; `ENSAYO.md` | Término fijo y ambigüedad al hablar | `en el profesor PCA la pupila pesa −0,05`; `los análisis usan el profesor PCA` (dicho frente al profesor guía, "el profesor" se confunde) | `en el Modelo Profesor con PCA` |
| M17 | Lámina 6, gráfico | Espaciado | El encabezado `Sensibilidad (P29)` queda pegado a la columna `Test` | Rótulo en dos líneas o `P29 (sensibilidad)` en `estilo_tecnico.py` |
| M18 | Lámina 7, tabla | Redacción | `Saavedra (2024, grupo, web)` | `Saavedra (2024; mismo grupo, web)` |
| M19 | Lámina 18, nota | Rótulo de registro | `el efecto de activación se concentra en esas 25 (+0,055, frente a +0,001 en las otras 16)` no dice que esa comparación por grupo no estaba registrada (la pregunta 5 sí) | Agregar `; esa comparación por grupo no estaba registrada` |
| M20 | `LEEME.md` (texto en `crear_presentacion.py`, línea 72) y comentario inicial de `relato.py` | Fecha | `Corte de información: 23 de noviembre de 2026.` | `Corte de resultados: 23 de noviembre de 2026; texto corregido el 26 de noviembre de 2026.` |
| M21 | `ENSAYO.md`: encabezado; "Antes de ensayar"; guion de la lámina 33 | Detalles | (a) `(...LECTURA_CRITICA_COMITE.md`): y tras la auditoría de código`; (b) `Queda un detalle fuera de relato.py: el eje del gráfico de la lámina 12 todavía dice "OOF"`; (c) el guion de la 33 omite `y cómo declarar el uso de asistentes automáticos en las revisiones`, que sí está en la nota | (a) quitar los dos puntos: `) y tras la auditoría de código`; (b) agregar `, igual que el gráfico de la lámina 38 y la tabla de la 37`; (c) agregar la frase al final del guion |
| M22 | `ENSAYO.md`, preguntas | Precisión y repetición | (a) Pregunta 17: `El contraste contra placebo a 6 segundos es más parejo: mejoran 30 de 40` no dice que es la curva del 22-11; la lámina 23 muestra 28 de 41 para el contraste registrado. (b) Pregunta 7: `la cifra de latencia no la pude comprobar en la fuente a la que la atribuyo`, pero el "1 a 5 s" de la lámina 28 sí lo respalda Benedek y Kaernbach (2010), citado en su pie; lo no comprobado es el "1 a 3 s" atribuido a Boucsein. (c) Contenido repetido: 4, 21 y 32 (nueve estimaciones, registro); 5, 24 y 37 (cambio de diseño y las 25 personas); 1 y 11 (cota inferior); 7 y 25 (filtro tónico). | (a) `En la curva del 22-11, el contraste contra placebo a 6 segundos es más parejo: mejoran 30 de 40 (28 de 41 en el contraste registrado)`. (b) `El "1 a 5 s" lo respalda Benedek y Kaernbach (2010); la latencia que atribuía a Boucsein no la pude comprobar`. (c) Dejar la respuesta completa en una y remitir desde las otras |

## Lo que pedía comprobar el encargo (punto 4)

| Contenido que debe estar | Dónde está | Estado |
|---|---|---|
| El diseño con 41 personas se adoptó tras el nulo del cierre V3 | Nota de la 18 ("cambio de diseño posterior a los datos"); nota de la 30; pregunta 24 | Cumple (solo en notas) |
| Configuración de activación elegida con el modelo con historial sobre 25 de las 41; +0,055 y +0,001 | Nota de la 18; pantalla de la 30 ("se concentra en las 25"); preguntas 5 y 37 | Cumple; falta en la lámina 11 (I2) |
| El soporte de la etiqueta excede los 6 s por el filtro tónico | Nota de la 23; preguntas 7, 16 y 25 | Cumple; el pie de la 23 lo contradice en la forma (I3) |
| Solo hay respaldo a 6 s | Pantalla de la 29 y de la 30 | Cumple; la 28 dice "sí ayuda" (M10) |
| Cerca de un tercio, cota inferior, sin ser demostración | Nota de la 25; pantalla de la 31 ("Se lee como cota inferior") | Cumple; la nota de la 27 lo excede (I1) |
| En el Modelo Profesor PCA la pupila casi no pesa | Pie y nota de la 5 | Cumple |
| La fusión tardía solo gana entre redes MLP | Título de la 19; pantalla de la 29 y de la 30 | Cumple |

**Salvedades que se repiten en pantalla.** "Análisis anterior al de 41 personas; se conserva como antecedente" en cuatro anexos (34, 35, 37, 38): aceptable, son anexos. "8 de las 18 referencias… solo con el resumen" en 27, 28 y 39: sobra en una de las dos primeras (M9). "+0,032, inconcluso" en 23 y 30, y "0,498 frente a 0,524: inconcluso" en 26 y 31: aceptable. No sobra ninguna otra.

**Láminas que ya no se leen en 30 segundos:** 30 (138 palabras, 12 cifras) y 31 (141 palabras, 8 cifras); en menor grado 27, 28 y 29 (tablas de 114 a 124 palabras, que se recorren hablando) y 33 (117 palabras, con 75 s asignados). Solo se propone recortar la 30 (M12) y el pie de la 29 (M11).

## Coherencia del relato

- Portada, índice (9 partes), barra lateral (9 capítulos más anexos), títulos de resultados, lámina 29, conclusiones y lámina 33 cuentan la misma historia: apoyo parcial que viene de activación; en atención la mejora es la posición en la página; cerca de un tercio de la detección depende de componentes oculares.
- Conteos: 48 = 41 + 1 (P29) + 6; 41 = 25 + 8 + 8; 22.211 = 13.524 + 4.662 + 4.025; 22.211 − 401 − 9.995 − 19 = 11.796; 39 = 33 + 6. El índice anuncia "cinco decisiones" y la lámina 33 muestra cinco; la nota agrega dos (I4).
- Las mismas cantidades llevan el mismo valor en todas las láminas: +0,026 y +0,034 (18, 21, pie de la 29); +0,029 y +0,036 (18 pie, 29, 30); +0,046 [+0,018; +0,073] (23, 29, 30); +0,032 (23, 30); +0,012 (19, 29, 30); 0,681, 0,621 y 0,674 (25, 26, 29, 31); 0,716, 0,649, 0,498 y 0,524 (26, 31); 0,52 (28, 29).
- Términos fijos: Modelo Profesor, Modelo Estudiante, Attention Score y Arousal Score se usan bien en pantalla; "Observado" y "Atendido" van con mayúscula en la 31 y en la nota de la 27. "Emociones" solo aparece en la cita literal de la hipótesis (3), en las decisiones (32, 33) y en "regiones de emoción y atención" (28, que es lo que dice el resumen de Critchley). Ninguna lámina ni nota afirma aprobación del profesor guía. Único desvío: "profesor PCA" (M16).

## Cifras: origen y comprobación

| Lámina | Cifra | Análisis y fecha | CSV (valor completo) | ¿La lámina dice de dónde sale? |
|---|---|---|---|---|
| 4 | 48 personas; 4 secuencias; 116 estímulos | Datos | `particion_participantes.csv` (48; G1 a G4); `caracteristicas_multimodales.csv` (116 estímulos distintos) | Sí |
| 6 | 25/8/8/1/6; 13.524, 4.662, 4.025 | Partición | `particion_participantes.csv`; `resumen_personas.csv` | Sí |
| 10 | 342 variables | 29-10 | `Crudos_V2_y_EEG_Por_Canal_29-10-2026.md` | Sí |
| 12 | 0,563/0,597; 0,557/0,581; 0,605/0,625; 0,593/0,600; 66 % | Profesor reconstruido, 29-10 | `comparacion_profesores_modelos.csv` (0,5633/0,5975; 0,5569/0,5813; 0,6048/0,6254; 0,5932/0,6005) | Parcial: no dice la fecha |
| 13 | 12,6 %; P34 8,6 % | Diagnóstico, 30-10 | `diagnostico_personas.csv` (0,1264; 0,0858) | Sí |
| 14 | 25.498 de 25.992 (98 %) | Auditoría de la etiqueta, 02-11 | `auditoria_independiente_02-11-2026.json` (98,1 %) | Sí |
| 16 | 5.824 de 11.796 (49,4 %) | Etiquetas V2, 01-11 | `resumen_personas.csv` (49,37 %) | Sí |
| 17 | 22.211; −401; −9.995; −19; 11.796 | Etiquetas V2, 01-11 | `motivos.csv` | Sí |
| 18 | +0,026; +0,030; +0,028; +0,026; +0,034; +0,043; +0,042; +0,042 | Análisis final y robustez, 16-11 | `contrastes.csv` (0,02641; 0,03419); `resultados.csv` (0,02998; 0,02754; 0,02559; 0,04324; 0,04159; 0,04160) | Sí (título) |
| 18 pie, 29, 30 | +0,036 [+0,010; +0,065]; +0,029 [+0,021; +0,037]; 23 de 41 | Reapertura fase 1, 22-11 | `confirmatorio.csv` (0,03645 [0,01027; 0,06475]; 0,02901 [0,02119; 0,03679]; 23/41) | Sí |
| 18 nota | +0,055 y +0,001; 36 de 41 | Análisis final, 16-11 (por grupo, no registrado) | `INFORME.md` del análisis final, tabla de heterogeneidad; `contrastes.csv` | Solo en nota |
| 19 | +0,012; +0,005; +0,006; +0,002 | Ampliación E3, 16-11 | `contrastes.csv` (0,01237; 0,00492; 0,00646; 0,00231) | No dice la fecha (sí la 29) |
| 20 | Curvas por quinto; 0,71/0,71; 0,68/0,70; 0,65/0,64; 0,60/0,63 | Ampliación, 16-11 | `fatiga_por_quintil.csv`; `por_categoria.csv` (0,7067/0,7096; 0,6810/0,6978; 0,6486/0,6370; 0,6044/0,6328) | No dice la fecha |
| 21 | +0,026; +0,027; +0,028; +0,008; +0,034; −0,004; −0,004; +0,053 | 16-11 y 18-11 | `contrastes.csv`, `resultados.csv` (0,02655; −0,00369), `explicativo…/contrastes.csv` (0,02814; −0,00396), `enmienda_e1_lag6/contrastes.csv` (0,00834; 0,05297) | No (M5) |
| 23 | +0,046 [+0,018; +0,073]; −0,002 [−0,005; +0,000]; +0,038 [+0,002; +0,074]; −0,002 [−0,006; +0,002]; 28 de 41; p Holm 0,004 | Enmienda E1 (registrada 16-11, corrida 18-11); explicativo 18-11 | 0,04604 [0,01844; 0,07315]; −0,00249 [−0,00529; 0,00010]; 0,03815 [0,00244; 0,07367]; −0,00173 [−0,00561; 0,00228]; 0,00436 | Sí (nota) |
| 23 pie, 30 | +0,032 [+0,004; +0,059] | Reapertura fase 3, 22-11 | `confirmatorio.csv` (0,03225 [0,00443; 0,05879]; p Holm 0,108) | Sí |
| 24 | 148, 151, 74, 77, 57, 56, 27, 29, 26, 25, 19, 18, 21, 24, 19, 20 µV | Montaje, 23-11 | `resumen_canales.csv` | No dice la fecha (sí la 29) |
| 25, 31 | 0,681; 0,661; 0,638; 0,621; 0,613; 0,674; 3,5 %; 72 %; 39 de 41; 0,593 a 0,547 | Limpieza ocular, 23-11 | `descriptivos.csv` (0,68090; 0,66077; 0,63768; 0,62078; 0,61335; 0,67430; 0,03497; 0,72070; 0,59268; 0,54741) | Ídem |
| 26, 31 | 0,716; 0,681; 0,649; 0,621; 0,498; 0,524; +0,035; +0,028; 0,067 | Red cruda, 23-11 | `descriptivos.csv` y `confirmatorio.csv` (0,71592; 0,64862; 0,49849; 0,52370; 0,03502; 0,02784; 0,06730) | Ídem |
| 29, 30 | +0,001; +0,047; +0,024; 0,040 | Fase 3 y curva, 22-11; análisis final, 16-11 | 0,00142; 0,04712; 0,02407; −0,04020 | Sí (pie de la 29) |
| 33 | 0,504; 0,675 y 0,683 | Enfoque E1, 22-11 | `e1_descriptivos.csv` (0,50442; 0,67503; 0,68297) | No dice la fecha (sí la nota de la 32) |
| 34, 35 | 0,674; 0,660; 0,688; 0,514; 0,547; 0,536; 2.184 | Test, 29-10 y 02-11 | `auditoria_graficos.json`; `metricas.csv`; `resumen_personas.csv` | Sí ("antecedente") |
| 38 | 62; 72; 101; 767 (nota: 90 a 959) | Protocolo, 06-11 | `INFORME.md` del protocolo | Sí |
| 39 | 18 referencias; 10 y 8 | Verificación, 23-11 | `VERIFICACION_REFERENCIAS.md` | Sí |

## `ENSAYO.md`: comprobaciones que pasan

- Plan de 20 minutos: suma 1.200 s; subtotales 195, 135, 155, 250, 220 y 245 s correctos. Plan de 10 minutos: suma 600 s; 17 mostradas y 16 saltadas; subtotales correctos.
- Los títulos de las 33 filas coinciden con `relato.py`. Las tablas de anexos (34 a 39) coinciden.
- Referencias cruzadas correctas: preguntas 5→37, 7→25, 3→láminas 21 y 22, 6→segunda decisión, 8→tercera, 16 y 35→quinta, 18→lámina 19, 19→sexto punto, 23→séptima de la minuta.
- Las respuestas no se contradicen entre sí ni con las láminas en ninguna cifra; salvo M22 (a) y (b), que son de precisión.
- El guion de cada lámina corresponde a su contenido y nota actuales, salvo I1, I2, M7 y M21 (c).

## `FUENTES.md` y `LEEME.md`

- `FUENTES.md`: 41 rutas, todas existen; coincide con el conjunto de fuentes de `relato.py`.
- `LEEME.md`: correcto en versión (7), conteo (39 = 33 + 6), archivos y teclas; `version_1` a `version_6` existen. Único ajuste: la fecha de corte (M20).

## Láminas revisadas sin hallazgos

3, 4, 8, 9, 10, 13, 14, 16, 17, 19, 20, 22, 25, 26, 32, 34, 35, 36 y 39.

Con hallazgos solo menores: 1, 2, 5, 6, 7, 12, 15, 18, 21, 24, 28, 29, 30, 37 y 38. Con algún hallazgo importante: 11, 23, 27, 31 y 33 (la 12 solo por su nota, en I4).
