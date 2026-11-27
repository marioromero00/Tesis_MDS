# Revisión final de la presentación de avances (ronda 9)

Fecha: 27-11-2026. Revisión independiente, hecha con un asistente automático a pedido del autor. No se editó ningún archivo del repositorio ni se hizo commit; lo único que se escribió es este informe.

Objeto: `presentaciones/avances_tesis_06-11-2026/` (`relato.py`, `estilo_tecnico.py`, `index.html`, `GUIÓN.md`, `FUENTES.md`, `LEEME.md`, `ENSAYO.md`), versión 7, 39 láminas.

Referencias: `documentacion/Cierre_Experimental_Final_23-11-2026.md`; `Escritura/Borrador Conclusiones 23-11-2026.md` y `Escritura/Borrador Resultados y Discusión 23-11-2026.md` (sección 8.1) del vault; `Avances/Avance - 23-11-2026 (Minuta de decisiones con el profesor).md`; CSV de `resultados/`; `documentacion/auditoria_final_23-11-2026/ronda6/registro.csv`.

## Qué se hizo y qué no

- **Visual.** Las 39 láminas se capturaron con Chrome headless a 1280×720 y se miraron una por una (`/private/tmp/claude-501/-Users-mario/bfaa0f9d-b2ac-4cab-9a3d-852bdb888a53/scratchpad/ronda9_pres/`).
- **Cifras.** Se recalcularon o leyeron desde los CSV las cifras visibles y de notas de las láminas 4, 6, 12 a 14, 16 a 26, 28 a 31, 33, 35 y 38, y las de las respuestas del ensayo que se citan abajo. El resto se contrastó con `ronda6/registro.csv` (928 filas: 884 coinciden, 19 coinciden con redondeo, 5 difieren y 20 no tenían cifra informada; ninguna de las 5 que difieren está en la presentación). No se verificaron una por una todas las cifras de las 66 respuestas: se revisaron las que aparecen en más de una respuesta y las que sostienen una contradicción.
- **Regeneración.** Se copió la carpeta a `/private/tmp/claude-501/-Users-mario/bfaa0f9d-b2ac-4cab-9a3d-852bdb888a53/scratchpad/ronda9_regen/` (con enlaces a `resultados/`, `scripts/` y demás) y se ejecutó `crear_presentacion.py`. `GUIÓN.md`, `index.html`, `FUENTES.md` y `LEEME.md` salen **idénticos byte a byte** a los del repositorio. Las 44 rutas de `FUENTES.md` existen. `git status` quedó limpio.
- **Propuestas de texto visible.** Todas las de este informe se aplicaron en la copia temporal, se regeneró y se capturaron las láminas afectadas (5, 8, 10, 11, 15, 18, 20, 21, 23, 25, 29, 30, 31, 32 y 38): ninguna desborda, ningún título pasa de dos líneas y ningún pie toca el número de lámina. Ninguna agrega una cifra que no esté ya en pantalla.

## Resultado en una frase

No hay hallazgos bloqueantes: las cifras calzan con los CSV, los archivos generados están al día y ninguna lámina afirma aprobación del profesor ni usa "emociones" por activación. Hay **12 hallazgos importantes** y **21 menores**. Los importantes son de dos tipos: reservas que el cierre vigente pone en primer plano y que solo están en notas o no están (cambio de diseño, las tres lecturas del criterio, "alta" como mirada más quieta), y lugares donde lo visible o lo hablado dice algo más fuerte o distinto que el resto del material (lámina 20, rótulos de la 23, fila de fusión de la 29, guion de la 29, plan de 10 minutos).

## La historia que cuenta la presentación, en ocho líneas

1. La hipótesis dice que los modelos con historial rinden mejor que los que ven solo la ventana actual; se prueba con el mismo modelo con y sin historial, en datos de laboratorio de 48 personas (41 en el análisis) con EEG, GSR, mirada y pupila.
2. No hay etiqueta directa: un Modelo Profesor la arma con unas señales y un Modelo Estudiante la predice con otras; la de atención es en la práctica conducta de mirada y la de activación es el nivel lento de la GSR, las dos relativas a la mediana de cada persona.
3. La etiqueta de activación tenía un error que mezclaba las ventanas; corregida (V2) conserva cerca de la mitad de las ventanas y lo anterior de activación no sirve.
4. Con las 41 personas en validación cruzada, el historial mejora atención de forma estable y activación de forma pequeña y primero inconclusa; la fusión y el comportamiento por sesión son resultados secundarios o descriptivos.
5. En atención la mejora no viene de las ventanas previas: un placebo y los segundos en la página la reproducen, porque la etiqueta depende de cuánto lleva la persona en la página.
6. En activación el historial de la misma página le gana a un placebo de otras páginas, con respaldo solo para los 6 s previos, modelos débiles y controles que quedan inconclusos.
7. En atención, cerca de un tercio de lo que el EEG detecta depende de componentes ligados a los ojos (cota inferior); una red más compleja rinde más y depende de lo mismo; en activación el EEG no detecta nada demostrable.
8. Conclusión provisoria: apoyo parcial, que viene de activación, más una advertencia metodológica; no se proponen más experimentos y quedan siete decisiones para el profesor.

**¿Coincide con el cierre y las conclusiones vigentes?** En contenido, sí. En grado de certeza, casi: la presentación es algo más firme que el cierre en cuatro puntos.

- El cierre abre con el cambio de diseño ("con el diseño original el cierre V3 no había mostrado una ventaja consistente… el apoyo parcial depende de ese cambio"). En la presentación eso está solo en las notas de las láminas 18 y 30; ningún texto visible lo dice (hallazgo I1).
- El cierre y la minuta dicen que "apoyo parcial" sale de una de tres lecturas posibles del criterio, y que la exigencia de que la ventaja venga de las ventanas previas no está en el criterio escrito. `relato.py` no lo menciona ni en notas (I7).
- La conclusión 9.7 nombra dos advertencias metodológicas (la posición y la etiqueta ocular); la lámina 31 nombra una, y deja fuera justo el hallazgo que el propio ensayo llama "el más sólido" (I5).
- La fila de fusión de la lámina 29 ("Tardía mejor con MLP") es más fuerte que la lámina 30 y que el cierre (I4).

**¿Las láminas iniciales anticipan lo que concluyen las finales?** La portada, el índice y la lámina 3 sí: el título es una pregunta, el índice dice "con historial mejoran las dos; en activación, primero inconcluso" y la nota de la portada adelanta las tres reservas principales. La excepción es la lámina 8 ("Lo que intento aportar"): promete las cuatro señales "con sitios web reales" y una "ablación por señal", y las finales concluyen otra cosa (I8 y menor M1).

## Comprobación de los diez puntos pedidos

| Punto | ¿Está? | Dónde | Observación |
|---|---|---|---|
| Cambio de diseño tras el nulo del cierre V3 | Sí, solo en notas | Notas 18 y 30 | No está en ningún texto visible (I1) |
| Configuración de activación elegida por el modelo con historial, sobre 25 de las 41 | Sí | Notas 11 y 18; visible en la 30 | Bien |
| Contraste frente al placebo fijado tras ver el placebo de robustez; placebo de otras páginas | Sí | Título y nota de la 23; visible en la 30; notas 21 y 30 | El guion hablado de la 29 lo omite (I9) |
| Soporte de la etiqueta de activación | Sí | Nota 23 | Bien |
| Solo respaldo a 6 s | Sí | Visible en 28, 29 y 30 | Bien |
| "Cerca de un tercio" como cota inferior que no es demostración | Sí | Visible en 29 y 31; notas 1, 25, 27 y 29 | Bien |
| La pupila casi no pesa en el Modelo Profesor con PCA | Sí | Visible y nota en la 5 | Bien |
| "Alta" es una mirada más quieta | **No** | — | `relato.py` no contiene la idea; solo está en el guion hablado de la 22 y en las preguntas 15, 41 y 60 (I6) |
| Sitios web: menos de un tercio de las ventanas de atención | Sí | Nota 4 | La lámina 8 dice lo contrario en visible (I8) |
| Calidad del EEG como registro no establecida | Sí | Nota 28 (y nota 4 para el montaje) | Bien |
| Fusión tardía solo entre MLP | Sí | Título de la 19; visible en la 30 | La fila de la 29 lo dice más fuerte (I4) |

## Hallazgos

Gravedad: **bloqueante** (no se puede presentar así), **importante** (conviene corregir antes de la reunión), **menor** (pulido). No hay bloqueantes.

### Importantes

| N.º | Dónde | Tipo | Texto exacto actual | Corrección exacta propuesta |
|---|---|---|---|---|
| I1 | Lámina 18, pie (`relato.py`) | Reserva principal solo en notas | `Cada punto es una partición de las 41 personas en 8 grupos; la oscura es la registrada de antemano. Al repetirlo con 5 particiones (22-11), activación pasa a +0,036 [+0,010; +0,065].` | `Diseño adoptado después de que el diseño original (cierre V3) no mostrara una ventaja consistente. Cada punto es una partición de las 41 personas en 8 grupos; la oscura es la registrada antes de sus predicciones. Al repetirlo con 5 particiones (22-11), activación pasa a +0,036 [+0,010; +0,065].` (pie de tres líneas; comprobado) |
| I2 | Lámina 20, pie y guion; pregunta 2 | Rótulo de gráfico sin explicar que contradice otra lámina | El gráfico izquierdo muestra una línea gris "Activación" que llega a 0,64 en el último quinto (CSV: 0,640, con 34 personas). El pie no la menciona: `Modelo con historial. Izquierda: quintos del tiempo de sesión. Derecha: AUC por tipo de página, sin las categorías con pocas personas (blur, emotion). Descriptivo.` La lámina 30 dice "AUC bajas: 0,50 a 0,59" y la respuesta 2 dice "lo más alto que obtuve es 0,587". El guion hablado de la 20 tampoco la nombra. | Pie: `Modelo con historial. Izquierda: AUC por quintos del tiempo de sesión; la línea gris (activación) tiene menos personas por punto. Derecha: AUC por tipo de página, sin las categorías con pocas personas (blur, emotion). Todo es descriptivo, sin contraste.` En `ENSAYO.md`, respuesta 2 (línea `Corta:` y primera frase de `Si repreguntan`): cambiar `y lo más alto que obtuve es 0,587` por `y lo más alto que obtuve con un modelo completo es 0,587`. Y agregar al final de la respuesta completa: `La línea gris de la lámina 20 llega a 0,64 en el último quinto de la sesión: es un tramo descriptivo, con 34 personas, no un resultado.` |
| I3 | Lámina 23, rótulos del gráfico (`estilo_tecnico.py`, línea 307) y pie | Rótulo inexacto | Filas 1 y 2 rotuladas `Activación · historial real − placebo` y `Atención · historial real − placebo`. Son el historial **sin** las ventanas de la etiqueta (+0,046). En la lámina 21 "Historial real" es el historial completo, cuyo contraste con el placebo es +0,038; y +0,038 es además, por coincidencia, la fila 3 de esta lámina. | En `estilo_tecnico.py`: `f'{lab} · historial real − placebo'` → `f'{lab} · historial desplazado − placebo'`. En el pie de la lámina 23: `Filas 1 y 2: historial sin las ventanas de 6 s que promedia la etiqueta, contra un placebo igual de largo.` → `Filas 1 y 2: historial desplazado (sin las ventanas de 6 s que promedia la etiqueta), contra un placebo igual de largo.` Requiere regenerar el gráfico. |
| I4 | Lámina 29, fila "Fusión" y pie | Versión más fuerte; decisión abierta sin marca | Celda: `Tardía mejor con MLP (+0,012)`. Pie: `Apoyo parcial, y viene de activación. Fila 1 y el +0,001: …` | Celda: `Tardía sobre temprana solo con MLP (+0,012); con HGB, signo contrario`. Pie: `Con el encuadre provisorio: apoyo parcial, y viene de activación. Fila 1 y el +0,001: …` (el resto igual; pasa a dos líneas, comprobado) |
| I5 | Lámina 31, puntos 1 y 4 | No coincide con la conclusión 9.7; falta qué SÍ se encontró | Punto 1: `…el control queda en 0,674. Se lee como cota inferior; no es una demostración.` Punto 4: `Evidencia acotada sobre el historial en activación, y una advertencia sobre evaluar modelos de EEG con etiquetas oculares.` | Punto 1: `…el control queda en 0,674. El modelo limpio sigue sobre el azar en todas las personas. Cota inferior; no es una demostración.` Punto 4: `Evidencia acotada sobre el historial en activación, y una advertencia metodológica en dos partes: una mejora que parecía temporal era la posición en la página, y una etiqueta ocular no permite evaluar un modelo de EEG como si fueran señales independientes.` Con esto se saca la fila "31" de la tabla final de `ENSAYO.md`. No hace falta tocar la lámina 33: la minuta también habla de "advertencia metodológica" con dos partes. |
| I6 | Lámina 5, nota (`relato.py`) | Punto pedido que no está | La nota dice: `En atención la etiqueta sale en la práctica de la mirada: en el Modelo Profesor con PCA la pupila pesa −0,05.` No dice qué es "alta". | Agregar a continuación: `“Alta” en el Attention Score es una mirada más quieta que lo habitual en esa persona: fijaciones más largas, menos dispersión y menos recorrido; no designa más atención en un sentido validado.` |
| I7 | Lámina 30, nota (`relato.py`) | Reserva del cierre ausente | La nota dice: `Con el encuadre provisorio, que es una de las decisiones abiertas, la hipótesis se apoya en parte, y solo por activación.` | Agregar a continuación: `Ojo: “apoyo parcial” es una de tres lecturas. Con el diseño original no había evidencia; con el segundo diseño y el criterio escrito al pie de la letra, la ventaja aparece en las dos variables; yo pido además que venga de las ventanas previas, y esa exigencia no está en el criterio escrito. Cuál corresponde es parte de la decisión 5.` |
| I8 | Lámina 8, columna "Lo que hago", punto 2 | Versión más fuerte que el límite declarado | `Las cuatro señales con sitios web reales, en laboratorio.` | `Las cuatro señales en una sesión de laboratorio con sitios web reales y otros estímulos.` |
| I9 | `ENSAYO.md`, guion hablado de la lámina 29 | Hablado más fuerte que lo visible; usa una fórmula que el propio ensayo prohíbe ("registrado", sin más) | `En activación sí viene en parte del historial: +0,046 sobre el placebo en el contraste registrado, y solo hay respaldo para los 6 segundos previos.` El párrafo tampoco dice "no puedo afirmar que detecte lo Atendido" ni el cambio de diseño, y en el plan de 10 minutos esta es la única lámina de conclusiones. | Reemplazar el párrafo completo por (147 palabras, 147 por minuto): `Con historial las dos tareas mejoran: +0,029 en atención y +0,036 en activación. En atención no viene de las ventanas previas: si el modelo conoce la posición en la página, el historial agrega +0,001. En activación hay evidencia acotada: +0,046 sobre un placebo de otras páginas, en un contraste que fijé después de ver el placebo, y solo hay respaldo para los 6 segundos previos. El modelo con orden, la GRU, no agrega en atención, y la fusión tardía solo gana en atención y con MLP. La última fila es lo nuevo: en atención, cerca de un tercio de lo que el EEG tiene sobre el azar depende de componentes ligados a los ojos, como cota inferior, y no puedo afirmar que detecte lo Atendido. Todo con personas ya consultadas y con un diseño que adopté después de un primer resultado sin ventaja: confirmarlo requiere personas nuevas.` |
| I10 | `ENSAYO.md`, plan de 10 minutos | El plan no tiene guion | Las sumas calzan (600 s, 17 láminas mostradas). Pero el único guion es el de 20 minutos: dicho en los tiempos del plan corto, 14 de las 17 láminas pasan de 150 palabras por minuto (lámina 24, 328; 18, 256; 23, 237; 32, 216; 11, 210; 26, 206; 22, 192; 1, 183; 3 y 5, 176; 6, 170; 25, 161; 21 y 33, 160). Solo las láminas 14 y 33 tienen indicación de cómo acortar. Al improvisar el recorte, lo que se pierde son las reservas. | Las 17 láminas bastan para la historia si se corrige I9 y se agregan estas tres versiones cortas bajo el plan de 10 minutos (el resto se recorta a la frase de la columna "única idea"). **Lámina 11 (30 s, 62 palabras):** `Elijo la configuración con las 25 personas de entrenamiento, la congelo y la evalúo con las 41 en validación cruzada por persona. Esas 25 son parte de las 41, y en activación la elección la decidió el modelo con historial. Miro la diferencia pareada por persona, con intervalo bootstrap de personas. Los protocolos están en mi propio repositorio: no es un prerregistro.` **Lámina 18 (40 s, 94 palabras):** `Con las particiones originales no hubo una ventaja consistente en ninguna de las dos tareas. Después de ver eso pasé a validación cruzada con las 41 personas, con la configuración congelada: es un cambio de diseño posterior a los datos. Además, la configuración de activación la decidió el modelo con historial, con 25 de esas 41 personas, y ahí se concentra el efecto. Con ese diseño, atención mejora +0,026, en 36 de 41. Activación queda inconclusa el 16 de noviembre y pasa a +0,036 al repetir con cinco particiones: más precisión, no una confirmación.` **Lámina 23 (40 s, 83 palabras):** `Saqué del historial las ventanas que promedia la etiqueta, aunque el filtro de la GSR mira más lejos. Aun así le gana al placebo por +0,046, en 28 de 41 personas. Es el contraste mejor sostenido, con dos reservas: lo fijé después de ver que el historial completo le ganaba al placebo, y el placebo viene de otras páginas. Al controlar los segundos en la página queda en +0,032, inconcluso. Y el modelo sigue siendo débil: la AUC queda entre 0,55 y 0,58.` |
| I11 | `ENSAYO.md`, preguntas 2, 4, 5, 22, 38 y 52 | Contradicciones entre respuestas | Ver la tabla de contradicciones (C1 a C6) | Ver la tabla |
| I12 | Lámina 21, título | Lámina de resultados sin mensaje en el título | `¿De dónde viene la mejora?` | `En atención, un placebo da la misma mejora; en activación, no` (una línea; comprobado). Cambiar el título en las dos tablas de tiempo y en el guion de `ENSAYO.md`. |

### Menores (21)

| N.º | Dónde | Texto actual | Propuesta |
|---|---|---|---|
| M1 | Lámina 8, nota | `Cada una tiene su respuesta en el diseño.` | Agregar: `Lo que queda como aporte al final es más acotado; va en la lámina 31.` La ablación por señal que promete el punto 3 no se muestra en ninguna lámina. |
| M2 | Lámina 5, pie | `“Alta” es sobre la mediana de cada persona en su sesión.` | `“Alta” es estar sobre la mediana de cada persona en su sesión.` |
| M3 | Lámina 10, tarjeta Mirada | `Con la pupila forma el Attention Score` (la lámina 5 dice que la pupila casi no pesa) | `Forma el Attention Score; la pupila casi no pesa` |
| M4 | Lámina 11, caja Controles | `placebo, registrado antes; posición, post hoc` | `placebo, fijado antes de sus predicciones; posición, post hoc` (tres líneas dentro de la caja; comprobado) |
| M5 | Lámina 15, título | `“Alta” es estar sobre su propia mediana de activación: así se ve en P22` ("su" sin antecedente; "mediana de activación" afirma el constructo) | `“Alta” es estar sobre la mediana del propio puntaje de GSR: así se ve en P22` (dos líneas; comprobado) |
| M6 | Lámina 21, gráfico | El rótulo `+0,008` toca la línea punteada del cero | Desplazar el rótulo en `estilo_tecnico.py`; cosmético |
| M7 | Lámina 23, pie | Tres líneas con cuatro cifras | Aceptable; si se quiere acortar, pasar el intervalo `[+0,004; +0,059]` a la nota |
| M8 | Lámina 24, nota | `El parpadeo pega 150 µV` | `El parpadeo llega a unos 150 µV` (como en el guion hablado) |
| M9 | Lámina 25, pie | `Componentes oculares: 3,5 % de la varianza del EEG. Componentes del control: 72 %.` (el ensayo pide no usar "oculares" como identificación) | `“Oculares”: los tres componentes más correlacionados con la mirada o los parpadeos; 3,5 % de la varianza del EEG. Componentes del control: 72 %.` |
| M10 | Lámina 28, pie | Cita `Critchley (2002)`; el anexo F dice que esa atribución está sin comprobar | Dejarlo y saberlo, o quitar a Critchley del pie hasta leer el texto completo |
| M11 | Lámina 30, punto 1 | `Frente al placebo y sin las ventanas de la etiqueta:` | `Frente al placebo y sin las ventanas que promedia la etiqueta:` (la fórmula corta se parece a "sin solapamiento con la etiqueta", que el ensayo prohíbe) |
| M12 | Lámina 30 | Cuatro puntos con diez cifras; es la lámina más densa | No se lee en 30 segundos. Aceptable porque repite la 29; al exponer, leer solo las negritas |
| M13 | Lámina 32, subtítulo | `Ninguno imprescindible` (la cohorte nueva es la decisión 1, abierta) | `Propongo no hacer más` |
| M14 | Lámina 33, punto 4 | `(decisión registrada: “inferior”)` | Críptico para quien no conoce las reglas; `(en el análisis quedó rotulada como “inferior”, al filo)` |
| M15 | Lámina 38 (anexo E), pie | `Mejora relevante +0,02; efecto real +0,04.` (presenta el margen, decisión 2, como dado) | `Margen propuesto +0,02; efecto supuesto +0,04.` |
| M16 | `ENSAYO.md`, encabezado | El primer párrafo es un historial de cambios de más de 500 palabras | Moverlo al final, junto a la sección "Láminas donde la nota… no calzan", y dejar arriba dos líneas: versión, fecha y supuesto de duración |
| M17 | `ENSAYO.md`, preguntas 8, 18, 24, 29, 32 y 34 | Respuestas de 76 a 99 palabras sin línea `Corta:` (la regla del ensayo la exige solo sobre 100) | Agregarles `Corta:`; las más largas son la 34 (99) y la 29 (95) |
| M18 | `ENSAYO.md`, pregunta 22, fuente | `las carpetas ronda2 a ronda6` | `las carpetas ronda2 a ronda9` |
| M19 | `ENSAYO.md`, pregunta 8, fuente | `CLAUDE.md del vault` | Citar la minuta (decisión 3); no conviene tener como fuente de una respuesta el archivo de instrucciones de un asistente |
| M20 | `ENSAYO.md`, preguntas 46 y 30 | Respuestas que solo dicen "no lo tengo" (recuento de pruebas; consentimiento y ética) | La 46 se puede cerrar antes de la reunión contando filas con p en los CSV de las doce etapas. La 30 no depende del análisis: pedir la documentación al proyecto antes de presentar |
| M21 | `ENSAYO.md`, guion de la lámina 22 y nota de la 22 | El guion dice "es decir, de mirada más quieta"; la nota de `relato.py` no | Queda resuelto con I6; si no, agregar la frase a la nota de la 22 |

## Qué se lleva el oyente de cada lámina de resultados y de conclusiones

| Lámina | Qué se lleva (una frase) | ¿Deja mensaje? |
|---|---|---|
| 18 | Con historial, atención mejora de forma estable; activación es positiva pero primero inconclusa | Sí |
| 19 | La fusión tardía gana solo en atención y solo entre redes MLP | Sí |
| 20 | El modelo de atención rinde mejor al final de la sesión y peor en textos | Sí; la línea gris distrae (I2) |
| 21 | — | **No en el título**; el gráfico lo dice, el título es una pregunta (I12) |
| 22 | La etiqueta de atención depende de cuánto lleva la persona en la página | Sí |
| 23 | En activación el historial de la misma página le gana a un placebo de otras páginas | Sí; rótulos por corregir (I3) |
| 24 | Los parpadeos se ven en el EEG, sobre todo adelante | Sí |
| 25 | Al quitar los componentes ligados a los ojos, la detección de atención cae; el control no | Sí |
| 26 | Una red rinde más y también depende de la huella ocular | Sí |
| 27 | Hay un mecanismo fisiológico conocido que lo explica | Sí |
| 28 | La etiqueta de activación es lenta y 2 s de EEG no calzan con ella | Sí |
| 29 | Apoyo parcial, y viene de activación | Sí, en el pie; la tabla es el mejor resumen de la presentación |
| 30 | El apoyo viene de activación, solo para 6 s; en atención no es temporal | Sí; densa (M12) |
| 31 | Cerca de un tercio depende de los ojos y no puedo afirmar lo Atendido | A medias: dice lo que no se puede afirmar y omite lo que sí se encontró (I5) |
| 32 | Faltan decisiones y escritura, no experimentos | Sí |
| 33 | Cinco preguntas concretas, la primera es escribir o reclutar | Sí |

Con las salvedades actuales la presentación todavía dice qué se encontró, pero lo dice mejor la lámina 29 que las 30 y 31. Los cuatro hallazgos positivos que conviene que queden a la vista son: (a) la etiqueta de activación antigua estaba mal y se corrigió (lámina 14, bien); (b) una mejora que parecía temporal era la posición en la página (lámina 22, bien; falta en el aporte de la 31); (c) el EEG detecta la etiqueta de atención en todas las personas, antes y después de limpiar, y cerca de un tercio depende de componentes ligados a los ojos (falta la primera mitad en la 31); (d) en activación el historial de la misma página supera a un placebo (lámina 23, bien). Las correcciones I5 e I12 cubren lo que falta.

## `ENSAYO.md`

### a) Guion y tiempos

- **Sumas.** Plan de 20 minutos: 33 láminas, 1.200 s; subtotales 195, 130, 125, 280, 220 y 250, correctos. Plan de 10 minutos: 600 s, 17 láminas mostradas y 16 saltadas; subtotales 145, 50, 155, 100 y 150, correctos.
- **Palabras por minuto, plan de 20 minutos.** Ninguna lámina pasa de 150. Las más altas: 31 y 33 (150), 30 (149), 25 (148), 4, 15, 18 y 27 (147), 1 y 23 (146). Total 2.744 palabras. No queda margen: cualquier frase agregada a esas láminas obliga a quitar otra.
- **Coherencia con las notas.** El guion sigue las notas de `relato.py` salvo en tres puntos: lámina 29 (I9), lámina 20 (no nombra la línea gris, I2) y lámina 22 (dice "mirada más quieta", que la nota no tiene, I6 y M21).
- **Plan de 10 minutos.** Ver I10.

### b) Las 66 preguntas

- **Numeración.** De corrido, de 1 a 66.
- **Referencias cruzadas.** Todas las remisiones entre preguntas y a láminas que se encontraron son correctas, incluidas las dos listas del párrafo introductorio de la sección 3.
- **Largo.** Las 24 líneas `Corta:` tienen entre 50 y 70 palabras. Las respuestas 38 a 66 tienen a lo más 70. Seis respuestas anteriores sin `Corta:` tienen entre 76 y 99 (M17).
- **Estado vigente.** No se encontró ninguna respuesta que cuente una versión anterior de los resultados. La pregunta 22 cita rondas hasta la 6 (M18).

### Contradicciones entre respuestas

| N.º | Preguntas | Qué dice una | Qué dice la otra | Qué es cierto (CSV o cierre) | Corrección exacta |
|---|---|---|---|---|---|
| C1 | 2 y 16 | 2: dentro de un mismo estímulo, el historial sobre los segundos suma `+0,005 [−0,025; +0,035]` | 16: `Dentro de un mismo estímulo suma +0,009 [−0,020; +0,037]` | Son dos contrastes distintos de `reapertura_fase3_41p_22-11-2026`: el primero es descriptivo (`hgb_c32 − pos_c1`), el segundo es el registrado (`c32_pos − pos_c1`, Q2). El cierre y el borrador usan +0,009 | En la 2, reemplazar `y el historial sobre ellos, +0,005 [−0,025; +0,035]` por `y el historial sobre ellos, +0,009 [−0,020; +0,037] en el contraste registrado` |
| C2 | 4 y 32 | 4: `cada etapa se ejecutó una vez` | 32: `la primera versión del cierre V3 se detuvo por una revisión de código` | El cierre dice "se ejecutó una vez" con tres salvedades (cierre V3 detenido, enmienda E1, fase 2 post hoc) | En la respuesta completa de la 4: `cada una se ejecutó una vez` → `cada una se ejecutó una vez, salvo el cierre V3, cuya primera versión se detuvo (pregunta 32)`. En su `Corta:`: `cada etapa se ejecutó una vez` → `casi todas se ejecutaron una vez` (queda en 69 palabras) |
| C3 | 22 y 5 | 22: `2.638 valores comparados, sin discrepancias` | 5: `la auditoría no reprodujo de forma exacta los intervalos de la primera` | Cierre: sin discrepancias en las cifras; "los intervalos y los p difieren solo por la semilla del bootstrap" | En la 22 (`Corta:` y completa): `sin discrepancias` → `sin discrepancias en las cifras; los intervalos difieren solo por la semilla del remuestreo` (la `Corta:` queda en 70 palabras) |
| C4 | 52 y 36 | 52: `Mis resultados describen la sesión completa.` | 36: los de activación se refieren `al 53 % de las ventanas que conserva la etiqueta` | Las dos cosas, para variables distintas | En la 52: `Mis resultados describen la sesión completa.` → `Mis resultados describen la sesión completa de estímulos y no solo los sitios web; los de activación, el 53 % de las ventanas que conserva la etiqueta (pregunta 36).` |
| C5 | 4 y 38 | 4: `tres decisiones quedaron pegadas al umbral (p de Holm 0,055, 0,055 y 0,049)` | 38: `Tres rótulos viven a milésimas de un umbral: atención (límite inferior 0,021), la red (0,023) y el historial desplazado (0,018)` | Son dos listas distintas (una por p, otra por límite del intervalo); las seis cifras están en los CSV | En la 38, agregar al final: `Son otros tres, distintos de los tres que quedaron al filo por su p de Holm (pregunta 4).` |
| C6 | 5 y 37 (y lámina 30) | 5, `Corta:`: el efecto `aparecía en las 25 de entrenamiento (+0,055) y no en las otras 16 (+0,001)`, sin fecha | 37: `+0,046 frente a +0,021 con cinco particiones`; la lámina 30 une "concentrado en las 25" con el +0,036 de cinco particiones | Las dos parejas son correctas: la primera es del 16-11, la segunda del 22-11 | Reemplazar la `Corta:` de la 5 por (65 palabras): `El 41 no viene de un cálculo de potencia: es lo que había disponible. Las 16 de validación y test ya se habían consultado; elegir la configuración con las 25 de entrenamiento no las vuelve nuevas. El efecto de activación se concentra en esas 25: +0,055 frente a +0,001 el 16-11, y +0,046 frente a +0,021 con cinco particiones. Por eso todo va como exploratorio.` |

Sin contradicción, pero conviene saberlo: la respuesta 63 dice que las tres referencias dan el mismo desfase "en casi todas las personas"; en `montaje_ocular_41p_23-11-2026/personas.csv` la mirada horizontal y los parpadeos coinciden en 40 de 41, y la vertical con ellos en 34 de 41.

### Preguntas duplicadas o casi duplicadas

No se propone renumerar ni borrar. Se indica cuál conservar como principal; la otra queda como repregunta que remite a ella.

| Par | Tema | Conservar como principal | Qué hacer con la otra |
|---|---|---|---|
| 27 y 56 | Movimiento y acelerómetro | 27 | La 56 repite la 27 casi palabra por palabra; dejarla en una línea que remita |
| 18 y 49 | Fusión tardía | 18 | La 49 (Saavedra) pasa a ser su repregunta |
| 24 y 48 | Diseño original y qué habría refutado la hipótesis | 24 para el hecho; 48 para la lectura del criterio | En la 48, agregar las tres lecturas de la minuta (I7); no repetir el relato del cierre V3 |
| 15, 41 y 60 | Qué significa "alta" en atención | 15 (validez) y 41 (conducta) | La 60 repite la 41; dejar solo su primera frase y la remisión |
| 20 y 66 | Correcciones de la pupila | 20 | La 66 pasa a ser su repregunta |
| 7 (segunda repregunta) y 54 | Nivel tónico y conteo de respuestas | 54 | En la 7, acortar la segunda repregunta y remitir |
| 4, 21 y 46 | Multiplicidad y número de estimaciones | 4 y 21 | La 46 no agrega: una línea en la 4 ("no tengo el recuento total") |
| 4 (segunda repregunta) y 32 | Qué garantiza el registro propio | 32 | Ya se remiten; bien |
| 5 y 37 | Las 25 frente a las 16 | 37 | En la 5, dejar solo la frase de C6 y remitir |
| 13, 31 y 35 | Qué aporta la tesis | 13 | La 31 y la 35 son repreguntas naturales de la 13 |
| 10 y 63; 19 y 44; 36 y 52; 1 y 11 | — | Las dos | Complementarias, no duplicadas |

### Respuestas evasivas

Ninguna respuesta esquiva la pregunta con rodeos: las que no tienen respuesta lo dicen. Dos conviene cerrarlas antes de la reunión (M20): la 46 (recuento de pruebas, que sale de los CSV) y la 30 (consentimiento y ética, que hay que pedir al proyecto). Varias más terminan en "no consta" o "no lo sé" por falta de documentación del registro (50, 51, 53, 55, 61 y 62, entre otras); no son evasivas, pero juntas pesan: conviene llevar hecha la lista de lo que se pedirá al proyecto.

### c) Índice temático propuesto (sin renumerar)

Para pegar al inicio de la sección 3 de `ENSAYO.md`.

| Tema | Preguntas |
|---|---|
| A. Hipótesis, diseño y encuadre | 5, 16, 24, 26, 28, 48 |
| B. Estadística y multiplicidad | 4, 6, 17, 21, 38, 39, 45, 46 |
| C. Etiquetas: qué miden y cómo se arman | 15, 19, 23, 29, 34, 36, 41, 42, 44, 53, 60 |
| D. Atención y EEG: la huella ocular | 1, 3, 11, 40, 43, 57, 58, 59, 65 |
| E. Activación y GSR | 2, 7, 8, 25, 27, 33, 37, 54, 55, 56 |
| F. Datos, registro y preprocesamiento | 10, 20, 30, 50, 51, 52, 61, 62, 63, 64, 66 |
| G. Modelos y fusión | 9, 12, 18, 49 |
| H. Asistentes, registro y reproducibilidad | 22, 32 |
| I. Qué aporta y qué sigue | 13, 14, 31, 35, 47 |

Las 66 quedan asignadas a un solo tema (6 + 8 + 11 + 9 + 10 + 11 + 4 + 2 + 5).

### Las diez preguntas más probables, para ensayar primero

Es una estimación del revisor, no un dato: se eligieron las que tocan lo que la presentación misma deja abierto.

1. **13.** Entonces, ¿qué aporta la tesis?
2. **1.** ¿La detección de atención por EEG no es circular?
3. **16.** Si al controlar la posición queda inconcluso, ¿por qué apoyo parcial?
4. **24.** Con el diseño original, ¿qué daba la hipótesis? (con la 48)
5. **4.** ¿Cómo sé que no hubo p-hacking? (con la 21)
6. **2.** ¿Por qué el AUC de activación es tan bajo?
7. **15.** ¿Qué validez tienen las pseudoetiquetas?
8. **14.** Si tuviera una cohorte nueva, ¿qué haría?
9. **6.** ¿De dónde sale el margen de 0,02?
10. **22.** ¿Quién hizo la auditoría? (uso de asistentes)

Siguen de cerca la 8 (activación en vez de emociones) y la 5 (las 41 personas ya vistas).

## Redacción, términos y decisiones

- **Términos fijos.** Modelo Profesor, Modelo Estudiante, Attention Score y Arousal Score se usan siempre igual. Observado y Atendido aparecen con mayúscula en las láminas 27 (nota) y 31 y en el ensayo.
- **"Emociones".** Solo aparece en la cita literal de la hipótesis (lámina 3) y en la decisión 3 (láminas 32 y 33). Correcto.
- **Aprobación del profesor.** Ninguna lámina ni nota la afirma.
- **Decisiones abiertas presentadas como tomadas.** Tres roces, todos menores o ya listados: pie de la 29 sin "provisorio" (I4), subtítulo "Ninguno imprescindible" de la 32 (M13) y "Mejora relevante +0,02" en el anexo E (M15). Las siete decisiones aparecen como preguntas en la lámina 33 y su pie.
- **Ortografía.** No se encontraron faltas en el texto visible ni en las notas. Coloquialismos de las notas ("Ojo", "pega") son de registro oral; solo se propone cambiar el de la lámina 24 (M8).
- **"Navegación web".** Queda en la portada, el título de la lámina 4 y el pie del anexo C como nombre del contexto, con la aclaración en la nota de la 4; coincide con el cierre. La única frase que afirma de más es la de la lámina 8 (I8).

## Láminas revisadas sin hallazgos

1, 2, 3, 4, 6, 7, 9, 12, 13, 14, 16, 17, 19, 22, 26, 27, 34, 35, 36, 37 y 39 (21 láminas). En todas: sin texto cortado ni desbordes, títulos de una o dos líneas, cifras coincidentes con su CSV, barra lateral coherente con el índice de la lámina 2 (nueve partes más "Anexos").

## Qué revisar después de aplicar las correcciones

1. Regenerar con `crear_presentacion.py` (I3 cambia un gráfico) y volver a capturar las láminas 18, 20, 21, 23, 29 y 31.
2. En `ENSAYO.md`: título de la lámina 21 en las dos tablas y en el guion; guion de la 29; versiones cortas de la 11, la 18 y la 23; respuestas 2, 4, 5, 22, 38 y 52; quitar la fila "31" de la tabla final.
3. Volver a contar palabras por minuto de la lámina 29 (queda en 147) y las palabras de las líneas `Corta:` tocadas (2, 4, 5 y 22).
