# Revisión editorial de los borradores — ronda 4

Fecha: 26-11-2026. Revisión de lectura, sin recálculo: no se verificó ninguna cifra ni se modificó ningún archivo. Las cifras que aparecen aquí están copiadas de los textos revisados.

Documentos leídos completos:

- **RD**: `Escritura/Borrador Resultados y Discusión 23-11-2026.md` (capítulos 6, 7 y 8)
- **DF**: `Escritura/Borrador Discusión fisiológica 23-11-2026.md`
- **CO**: `Escritura/Borrador Conclusiones 23-11-2026.md` (capítulo 9)
- **SP**: `Escritura/Borrador Secciones pendientes 23-11-2026.md` (capítulos 1, 4 y 5)
- **CI**: `repos/Tesis_MDS/documentacion/Cierre_Experimental_Final_23-11-2026.md`

Reglas consultadas: `documentos/01 Tesis MDS/CLAUDE.md`, `notas/pautas-escritura-recuperadas.md`, `Escritura/Estructura Tesis.md` y la minuta del 23-11 (solo su índice de decisiones).

Gravedad: **importante** = afecta la comprensión del argumento; **menor** = estilo.

---

## Diagnóstico general

Los textos no se contradicen en el fondo y no encontré ninguna afirmación que exceda lo que sus propias cifras permiten, salvo dos frases (hallazgos C2 y C6). El problema es el inverso al que tenían hace tres rondas: el argumento existe, pero hay que excavarlo.

1. **El mismo límite se declara entre cuatro y siete veces por documento.** En RD, la selección de la configuración aparece en ocho lugares, el soporte del filtro tónico en siete y "no es una confirmación independiente" en siete. Cada repetición trae una redacción algo distinta, y el lector no sabe si son siete límites o uno.
2. **Las salvedades se pegan al resultado equivocado.** El caso más serio es la sección 8.4 de RD: el contraste mejor sostenido de activación (historial desplazado frente al placebo) queda enterrado bajo las objeciones que valen para otro contraste (historial menos sin historial). El propio texto dice que la objeción de la selección de configuración no lo alcanza, pero lo dice seis frases después.
3. **Material de proceso dentro del texto corrido.** Fechas como nombre de análisis ("el 16-11", "la fase 2 del 22-11"), "redondeo doble del INFORME" cuatro veces, "pedida por la auditoría", nombres de CSV y de scripts. Un lector que no vivió el proceso no puede seguir 7.2 ni 7.3.
4. **Seis expresiones para una misma fuerza de evidencia** en activación: "respaldo", "apoyo acotado", "apoyo parcial", "evidencia acotada", "indicio" y "en parte". Y dos para la contribución ocular: "al menos un tercio" y "cerca de un tercio", que no significan lo mismo.

---

## 1. Mensaje por documento

### RD — Capítulos 6, 7 y 8

**Qué concluye.** El modelo con historial rinde mejor en las dos variables. En atención esa ventaja es la posición de la ventana dentro del estímulo y no la fisiología previa (nulo concluyente), y cerca de un tercio de lo que el EEG detecta sobre el azar depende de componentes oculares. En activación el historial reciente supera a un placebo, con alcance demostrado de unos 6 s, sin que pueda separarse "el pasado predice" de "señales simultáneas", y con un contraste principal inestable entre grupos de personas. Ni el orden de las ventanas ni el tipo de fusión mostraron un aporte.

**¿Se entiende?** Atención se entiende bien: 7.2 y 8.2 son las secciones más limpias. Activación no: el lector termina 8.4 sin saber si hay o no un resultado.

**Dónde se pierde.**
- 6.1: los límites de cada etiqueta llegan antes que su definición completa.
- 6.3: la regla de precedencia, las ocho filas, las revisiones de código y el alcance de la evidencia van en un mismo bloque con el diseño.
- 7.1: el bloque "Selección de la configuración" usa contrastes que se definen en 7.3 y 7.4.
- 7.3 "Límites de la curva": mezcla un límite de la curva con una propiedad de la etiqueta que ya se dijo en 6.1.
- 7.6: cinco temas en una sección (aporte por señal, montaje, sincronía, limpieza, red).
- 8.4, primer párrafo: unas 330 palabras, una afirmación y nueve salvedades.
- 8.8: 21 viñetas sin orden ni jerarquía.

### DF — Discusión fisiológica

**Qué concluye.** El EEG lleva la huella eléctrica de los ojos, la limpieza quita cerca de un tercio de la detección y el resto no puede atribuirse; el *Arousal Score* no se detecta desde la ventana actual, y hay tres explicaciones fisiológicas compatibles que el diseño no prueba.

**¿Se entiende?** Sí; es el documento mejor escrito de los cinco. Su problema es estructural: las secciones 8.3, 8.5 y 8.7 de RD dicen que lo "resumen", pero tienen casi su mismo largo y repiten sus frases. Hoy hay dos versiones del mismo texto con diferencias pequeñas (hallazgos C7, C8). Hay que elegir una.

### CO — Conclusiones

**Qué concluye.** Apoyo parcial a la hipótesis, que proviene de activación y del historial resumido, no de un modelo secuencial ni de la fusión; advertencia metodológica sobre pseudoetiquetas oculares evaluadas con EEG.

**¿Se entiende?** A medias. 9.1 empieza con la respuesta y la desdice en la misma frase y en las tres siguientes. 9.5 copia 16 de las 21 limitaciones de 8.8: un capítulo de conclusiones con más viñetas de límites que conclusiones. 9.7 dice lo mismo dos veces dentro de un párrafo de tres frases.

### SP — Secciones pendientes

**Qué concluye.** No concluye: describe participantes, la etiqueta de activación, la sincronización, el preprocesamiento, las variables, la partición y las métricas. Es coherente con RD.

**¿Se entiende?** Sí como documento de trabajo. Como texto de tesis tiene el mayor volumen de material de proceso de los cinco (nombres de columnas, scripts, hash, semilla, "calculado desde…", historia de errores corregidos). Los marcadores están justificados por la convención del propio borrador, pero hay que retirarlos al pasar a LaTeX.

### CI — Documento de cierre

**Qué concluye.** Lo mismo que RD, en una tabla. Es un documento de proceso y está bien que lo sea. Dos observaciones: la tabla de la auditoría de código quedó insertada entre la frase que la anuncia y la lista H1–H4 que la explica, y su orden de decisiones abiertas difiere del de los borradores y del de la minuta (hallazgo C9).

### ¿Concluyen lo mismo, con la misma fuerza?

Lo mismo, sí. Con la misma fuerza, no:

| Punto | RD | DF | CO | CI |
|---|---|---|---|---|
| Activación, origen temporal | "Apoyo acotado" (8.1); "indicio" (título 8.4); "Sí, con respaldo" (8.1, fila 1) | "apoyo más sólido" con salvedad completa (8.y) | "apoyo parcial"; "evidencia acotada de que… ayudan a predecir la activación" (9.7) | "En parte" |
| Contribución ocular | "cerca de un tercio" (7.6); "al menos un tercio" (8.3, dos veces) | "al menos un tercio" (8.x.3, 8.z) | "cerca de un tercio" (9.3, 9.7) | "Al menos un tercio… (no es una demostración)" |
| Límites de la red | cuatro (7.6) | dos (8.x.4) | uno (9.5) | dos |
| Candidatos para el remanente | cuatro más un quinto no fisiológico (8.3) | cuatro (8.x.3) | — | — |
| Decisiones abiertas | siete | no las lista | siete | siete, en otro orden |
| Decisiones abiertas en SP | cinco de diseño más **cuatro** de noviembre (faltan la 6 y la 7) | | | |

---

## 2. Repeticiones

Para cada una: ubicaciones en RD (sección y frase inicial), ubicaciones en los otros documentos y lugar único propuesto.

### R1. Personas ya consultadas; nada es confirmación independiente — importante

- RD, callout de estado y 6.3 "**Alcance de la evidencia.** La configuración se eligió…"
- RD 6.4, tabla, fila "Reapertura, fase 1" (celda de 60 palabras)
- RD 7.1 "La repetición no es una confirmación independiente…"
- RD 8.1 "Este encuadre es provisorio. Todos los análisis…"
- RD 8.4 "El respaldo de la fase 1 del 22-11 sale de un análisis registrado sobre personas ya consultadas…"
- RD 8.8, primera viñeta
- CO 9.1 (primer párrafo), 9.5 (viñetas 1 y 2); DF "Limitaciones de esta sección"; SP 4.8.2 "Diseño del análisis final"; CI "Límites"

**Lugar único:** 6.3 "Alcance de la evidencia" (declaración completa) y una viñeta en 8.8. En 7.1 basta "(mismas 41 personas; sección 6.3)". Quitar de la celda de 6.4, de 8.1 y de 8.4. En CO, una sola vez en 9.1.

### R2. Selección de la configuración (15 hojas, 25 frente a 16 personas) — importante

- RD 6.3 "El número de hojas se eligió por la AUC media…"
- RD 6.3 "Alcance de la evidencia"
- RD 7.1, "Lecturas descriptivas", segunda viñeta "Por grupo de origen (16-11…"
- RD 7.1, bloque "**Selección de la configuración y grupos de personas (límite destacado).**" con dos tablas; la segunda tabla repite las cifras de la viñeta anterior
- RD 7.3 "Por grupo de personas (tabla de la sección 7.1)…"
- RD 8.1, tabla, fila 1 de activación
- RD 8.4 "Tampoco es estable entre subconjuntos de personas…"
- RD 8.8 "**Selección de la configuración.**"
- CO 9.1 y 9.5; SP 4.8.2; CI (tres veces: tabla inicial, auditoría de código, límites)

**Lugar único:** una subsección propia de resultados, después de 7.4 (ver O3), con las dos tablas. En 6.3 una frase de método (cómo se eligió). En 8.4 una frase de interpretación. En 8.8 una viñeta de una línea con remisión. Eliminar la viñeta de "Lecturas descriptivas" de 7.1, que duplica la tabla.

### R3. Soporte real del *Arousal Score* (nivel tónico, filtro en ambos sentidos, 49/25/25 %) — importante

- RD 6.1, viñeta de activación: "En la práctica el *Arousal Score* es…" y "Su soporte temporal real excede…"
- RD 6.2, viñeta del historial desplazado: "(el filtro tónico de la GSR tiene un soporte más largo; sección 7.3)"
- RD 7.3, primer párrafo: "(aunque sí con el soporte de su filtro tónico; ver "Límites de la curva")"
- RD 7.3 "**Límites de la curva.**" (desarrollo completo)
- RD 8.1, tabla: "(pero dentro del soporte de su filtro tónico)"
- RD 8.4 "Ese contraste excluye las ventanas que promedia la etiqueta, pero no…"
- RD 8.8 "La etiqueta de activación es en lo esencial…"
- DF 8.y "Escala temporal"; CO 9.1 (dos veces en el mismo párrafo) y 9.5; SP 4.5.2 (paso 5 y "Límites") y 4.6.3; CI (tres veces)

**Lugar único:** la propiedad de la etiqueta (qué es y cuánto pesa cada tramo) va en 4.5.2 "Límites" o en 6.1, una sola vez y con las cifras. 7.3 la cita en una frase. 8.4 la interpreta (qué impide concluir). En DF 8.y no debe ir: allí interrumpe un argumento fisiológico.

### R4. La etiqueta de atención es conducta de mirada (pupila −0,052; fijaciones completas, 28 % sobre 2.000 ms) — menor

- RD 6.1 (viñeta de atención, dos frases); 8.2 "Una es de cálculo: la duración de cada fijación…"; 8.8 "La etiqueta de atención es, en la práctica…"
- DF 8.x.1; CO 9.5; SP 4.6.4 y tabla final (4.5.1); CI (dos veces)

**Lugar único:** 6.1 (o 4.5.1 cuando se actualice). En 8.2 se usa como explicación y está bien; en 8.8 basta la remisión.

### R5. Alcance de 6 s: "a 12 s inconcluso; desde 24 s no se distingue del placebo, sin que eso demuestre ausencia" — importante

- RD 7.3, tras la tabla de la curva: la idea aparece **tres veces en tres frases seguidas** ("y desde 24 s también: inconcluso, no nulo" / "la curva no demuestra que el efecto desaparezca" / "sin que eso demuestre ausencia")
- RD 8.1, tabla; RD 8.4 "En cuanto al alcance, solo la banda de 6 s…"
- DF 8.y; CO 9.1; CI (dos veces)

**Lugar único:** 7.3, una vez (pasaje reescrito 4). En 8.4 una frase.

### R6. Efecto de activación desigual entre personas (mediana +0,014; 23 de 41; P4 con 26 ventanas) — menor

- RD 7.1 (tabla y primera viñeta de "Lecturas descriptivas"); 8.1 (tabla); 8.4 (primer párrafo); 8.4 último párrafo ("la ganancia es desigual entre personas"); 8.8 (P4)
- CO 9.1, 9.5, 9.7; SP 4.5.2 y 5.3 (P4)

**Lugar único:** 7.1. En 8.4 una vez, no dos.

### R7. "La ganancia se mantiene dentro del mismo minuto… el control registrado del tiempo de sesión quedó inconcluso" — menor

- RD 7.3 "La ganancia se mantiene dentro del mismo minuto, lo que habla contra…" y RD 8.4 "La ganancia se mantiene dentro del mismo minuto (análisis post hoc)…": casi literales.

**Lugar único:** el dato en 7.3; la lectura ("habla contra una deriva lenta") en 8.4.

### R8. Contribución ocular: un tercio, cota inferior, "no puede descartarse que el resto" — importante

- RD 7.6 "La caída equivale a cerca de un tercio…"; 7.6 "La limpieza es parcial…" (cota inferior, más defendible, lo medido, inferencia); 8.3 "Cuánto depende…" ; 8.3 párrafo final (dos veces "un tercio" en dos frases); 8.8
- DF 8.x.2 (dos veces), 8.x.3, 8.z; CO 9.3, 9.5, 9.7; CI (tres veces)

**Lugar único:** el dato y sus dos objeciones en 7.6 (pasaje reescrito 5); la interpretación en 8.3, una vez. El párrafo final de 8.3 dice lo mismo en sus frases primera y tercera: dejar una.

### R9. La red: "pierde 0,067, sin control propio; su ventaja se mantiene con el EEG limpio (+0,028 frente a +0,035)" — menor

- RD 7.6 "Su detección depende de lo ocular…"; 7.6 "Cuatro límites acotan…"; 8.3 "Un modelo más complejo…"; 8.6 "Su detección depende de lo ocular (pierde 0,067…"; 8.8
- DF 8.x.4; CO 9.3, 9.5; CI

**Lugar único:** 7.6. En 8.3 **o** en 8.6, no en ambas: propongo dejarlo en 8.6, que es la sección sobre complejidad del modelo, y que 8.3 remita.

### R10. Desfase entre el EEG y el seguidor ocular (0,18 a 0,53 s; dos valores, 0,27 y 0,47 s) — menor

- RD 7.6 "El mismo análisis mostró que el EEG va entre 0,18 y 0,53 s…"; 8.7 "**Sincronía entre equipos.**"; 8.8 "El desfase de reloj…"; 8.9
- DF 8.z; SP 4.6.1 "Precisión alcanzada" (casi literal respecto de RD 7.6); CI

**Lugar único:** SP 4.6.1 (es metodología de sincronización). En RD 7.6 una frase con remisión; en 8.8 una viñeta. Quitar de 8.7: no es una implicancia de diseño sino un límite.

### R11. Fusión (+0,012 con MLP; signo contrario con HGB; MLP tardía 0,024 bajo el HGB) — menor

- RD 7.5: la cifra +0,012 [+0,005; +0,021] aparece en la tabla y otra vez en la frase siguiente; "no puede generalizarse" y "No puede concluirse que la fusión tardía sea mejor en general" en el mismo párrafo
- RD 8.6, primer párrafo: repite las mismas cifras y la misma frase final
- CO 9.2; CI

**Lugar único:** cifras en 7.5; en 8.6 solo la lectura y la explicación posible.

### R12. Decisiones al filo (A1, A3, adaptación sin historial, R1) — menor

- RD 7.2 "Las decisiones de A1 y A3 están al filo…"; 7.6 "R1 es efecto relevante con holgura mínima…"; 7.7 "pegada al umbral"; 8.2 "aunque la decisión registrada de ese contraste (A1) fue "inferior"…" (casi literal respecto de 7.2); 8.8; 8.10 punto 2

**Lugar único:** cada una en su sección de resultados; una viñeta en 8.8. Quitar de 8.2.

### R13. Precedencia de las reglas y las ocho filas — menor

- RD 6.3 (desarrollo), 8.8 (viñeta); SP 4.8.3; CO 9.5; CI

**Lugar único:** SP 4.8.3 (allí se definen las reglas). RD 6.3 no debería repetir la tabla de reglas que ya está en 4.8.3: hoy la tabla existe dos veces, con redacciones distintas.

### R14. Cambio de diseño tras el resultado nulo del cierre V3 — importante

- RD 6.3 "Este diseño se adoptó el 16-11, después de ver…"; 7.1 (tercera viñeta descriptiva); 8.1 (primer párrafo, dos frases); 8.8
- CO 9.1, 9.5; SP 4.8.2 (dos veces: "Diseño del análisis final" y primera viñeta de "Otros tres límites"); CI

**Lugar único:** 6.3 (hecho) y 8.1 (consecuencia para la hipótesis). Es un límite que conviene repetir una vez en la discusión; no cuatro.

### R15. Otras repeticiones dentro de RD — menor

- "La posición sola predice con AUC 0,598": 7.2 (dos veces) y 8.2.
- Importancia por permutación 0,207 y 0,004: 7.6 y 7.8.
- "No se demostró aporte del EEG de la ventana actual (0,524)": 7.7, 7.8 y 8.5.
- R4 inconcluso, "no se demostró que un modelo más complejo ayude": 7.7 y 8.6.
- AUC bajas, 0,50 a 0,59: 8.4 y 8.8.
- "En la curva y en la fase 2 las reglas se usan como lectura descriptiva": 7.2 y 8.8.
- Etiquetas offline y relativas a la sesión: 6.1, 7.7 y dos viñetas contiguas de 8.8 ("Las etiquetas son pseudoetiquetas offline…" y "Varias variables…"), que pueden fusionarse.

### R16. Repeticiones dentro de CO — importante

9.5 repite lo que 9.1 y 9.3 ya dijeron: selección de configuración (9.1 y 9.5), soporte tónico (9.1 dos veces, 9.5), particiones originales (9.1 y 9.5), ninguna confirmación independiente (9.1 y 9.5), cota inferior (9.3 y 9.5), efecto desigual (9.1 y 9.7). **Propuesta:** 9.5 se reduce a los cuatro o cinco límites que condicionan las conclusiones, agrupados (muestra y diseño de evaluación; definición de las etiquetas; separación ocular; tamaño del efecto) y remite a 8.8 para la lista completa.

### R17. Repeticiones dentro de SP — menor

- Regla de no-circularidad enunciada en negrita en 4.5.2 y de nuevo en 4.7, y recordada en 4.6.3 y 4.6.4.
- Estandarización por sesión no causal: 4.5.2 "Límites", 4.6.3, 4.6.5 y 4.8.2.
- "No se corrigió, porque el código y los resultados están congelados; se describe tal como es": 4.6.4 y 4.6.5, literal.
- Fracción con ambos ojos válidos (0,755 frente a 0,942): 4.6.5 y la tabla de 4.7.
- P29 y sus 329,9 s: 4.3 y 4.6.1.

**Lugar único:** la regla en 4.7 (donde está la tabla Profesor/Estudiante); la estandarización por sesión en 4.8.2 "Lo que no se ajusta solo con entrenamiento".

### R18. Repeticiones dentro de DF — menor

"No puede descartarse que el resto también dependa de los ojos" en 8.x.2, 8.x.3 y 8.z. Dejarla en 8.x.3, que es donde se discute el remanente.

---

## 3. Contradicciones de tono o de fondo

### C1. "Sí, con respaldo" frente a "indicio" — importante

- A: RD 8.1, tabla, activación: "Sí, con respaldo al promediar 5 particiones". RD 7.1, tabla: "Respaldo".
- B: RD 8.4, título: "indicio de información temporal de corto alcance". RD 7.1: "el "respaldo" del contraste principal es más débil de lo que indica su intervalo". RD 8.4: "debilitan el "respaldo"".
- **Qué sostienen los datos según el texto:** las dos cosas, de contrastes distintos. "Respaldo" es la decisión de la regla registrada; la debilidad proviene de comparaciones descriptivas no registradas. **Propuesta:** fijar el vocabulario. "Respaldo", "efecto relevante", "inconcluso" solo para decisiones de la regla. "Apoyo parcial" solo para la hipótesis. Eliminar "indicio" para el contraste con placebo y reservarlo para la GRU (7.4). Título propuesto para 8.4: "Activación: el historial reciente supera al placebo, con alcance de segundos".

### C2. "Al menos un tercio" frente a "cerca de un tercio" — importante

- A: RD 8.3, párrafo final: "al menos un tercio de lo que el *Modelo Estudiante* de atención recupera desde el EEG depende de componentes oculares" y "depende, al menos en un tercio". DF 8.x.3 y 8.z. CI, tabla.
- B: RD 7.6: "Lo medido es que la AUC sobre el azar baja cerca de un tercio… 0,060 se lee como cota inferior… Es la lectura más defendible y no una demostración". CO 9.3 y 9.7: "cerca de un tercio".
- **Qué sostienen los datos según el texto:** B. "Al menos" afirma la cota inferior como hecho, y 7.6 dice expresamente que es una lectura. **Propuesta:** "cerca de un tercio" en todos los documentos; donde se quiera conservar la lectura, "cerca de un tercio, que se lee como cota inferior".

### C3. El criterio de la hipótesis frente a su aplicación — importante

- A: SP 4.8.3 "Criterio para la hipótesis": apoyo parcial "si la ventaja aparece en una sola de las dos".
- B: RD 8.1, tabla, primera fila: "Sí" en atención (efecto relevante) y "Sí" en activación (respaldo).
- Con el criterio leído al pie de la letra, la ventaja aparece en las dos y correspondería "evidencia a favor". El texto concluye "apoyo parcial" porque descuenta la ventaja de atención al mostrar que es la posición. Es la lectura correcta y la más conservadora, pero el paso no está escrito: 8.1 dice "con este segundo diseño y sus controles" y nada más. **Propuesta:** una frase explícita en 8.1: el criterio registrado compara desempeño; aquí se aplica un criterio más exigente, que pide además que la ventaja provenga de las ventanas previas, y bajo él atención no cuenta. Si el profesor prefiere el criterio literal, cambia el encuadre: es parte de la decisión abierta sobre el encuadre.

### C4. "Desde el 22-11 la validación cruzada se repite en 5 particiones" frente a la curva temporal — menor

- A: RD 6.3 "Desde el 22-11 la validación cruzada se repite en 5 particiones nuevas".
- B: RD 7.3 "El del 22-11 usa… también una sola partición (la registrada el 16-11)"; RD 7.2 "Una comprobación no registrada… con una sola partición".
- **Sostiene el texto:** B para la curva y para la comprobación. **Propuesta:** en 6.3, "…se repite en 5 particiones nuevas en los contrastes principales; la curva temporal y la comprobación no registrada usan una sola".

### C5. "El historial no agrega nada" frente a los estratos — menor

- A: RD 7.2 "Con la posición como variable, el historial no agrega nada". RD 8.2 "desaparece cuando el modelo conoce ese número". CO 9.1 "el historial no agrega nada".
- B: RD 7.2 "el contraste registrado calculado a igual posición da +0,005 [+0,001; +0,010]"; A3, +0,004 [+0,000; +0,009].
- **Sostiene el texto:** nulo concluyente dentro de ±0,02, no ausencia exacta. **Propuesta:** "no agrega un efecto que supere el margen" o "queda dentro de ±0,02". La misma corrección para "la GSR no le agrega nada" (7.6, B3: +0,002, nulo concluyente). En 7.6 conviene además aclarar que la GSR sola sí detecta (B2, +0,045) y lo que no hace es sumar al EEG: hoy las dos filas parecen contradecirse.

### C6. 8.5 usa el resultado temporal sin sus salvedades — importante

- A: RD 8.5, "Escala temporal": "Esto es coherente con que el historial de los segundos previos mejore la predicción (con respaldo a 6 s)".
- B: RD 7.3 y 8.4: el contraste no separa el pasado del presente porque la etiqueta contiene GSR anterior.
- En DF 8.y, la misma frase lleva pegada la salvedad completa (y por eso mide más de 60 palabras). Los dos documentos difieren en el mismo punto. **Propuesta, igual en ambos:** "Esto es coherente con el resultado temporal de activación, con las reservas de la sección 8.4", sin cifras ni salvedades propias.

### C7. Cuatro límites de la red en RD, dos en DF — menor

- RD 7.6 "Cuatro límites acotan esta lectura" (holgura de R1, R3 sin control, una arquitectura sin búsqueda, escala por persona).
- DF 8.x.4 "Este resultado tiene dos límites" (los dos primeros; la escala por persona aparece antes como "explicación plausible" y la arquitectura única no aparece).
- **Propuesta:** una sola versión; la de RD es la completa.

### C8. Candidatos para el remanente: cuatro o cinco — menor

- RD 8.3 lista cuatro, añade "una quinta posibilidad, no fisiológica" y cierra con "todas las fuentes covarían con ella".
- DF 8.x.3 lista cuatro y cierra con "las cuatro fuentes covarían".
- Además, que las variables de calidad de canal "covaríen" con la conducta ocular es una afirmación distinta de la de los otros cuatro candidatos y el texto no la apoya. **Propuesta:** en RD, "las cuatro fuentes fisiológicas covarían con ella" y dejar la quinta aparte.

### C9. Tres numeraciones para las mismas siete decisiones — importante

- RD (callout y 8.10) y CO (callout): 1 emociones, 2 margen, 3 etiqueta corregida, 4 encuadre, 5 cohorte, 6 normalización, 7 profesor PCA.
- CI: 1 etiqueta corregida, 2 margen, 3 emociones, 4 encuadre, 5 cohorte.
- Minuta del 23-11: 1 cohorte, 2 margen, 3 emociones, 4 etiqueta, 5 encuadre.
- Consecuencia: CO 9.7 dice "encuadre provisorio, que depende de la quinta decisión abierta". En la minuta la quinta es el encuadre; en el callout del propio CO la quinta es la cohorte y el encuadre es la cuarta. **Propuesta:** una sola numeración (la de la minuta, que es la que verá el profesor) en los cuatro documentos, o nombrar la decisión en vez de numerarla: "que depende de la decisión abierta sobre el encuadre".
- SP, callout: de las siete solo nombra cuatro ("margen práctico, etiqueta corregida por posición, encuadre y cohorte nueva"). Faltan la normalización por sesión y la definición del *Attention Score*, que son justamente las dos que SP describe en 4.8.2 y 4.5.2.

### C10. "Debe presentarse como…" frente a encuadre abierto — menor

- A: RD 8.3, última frase: "El resultado debe presentarse como una detección que depende…". DF 8.z: "debe presentarse como…".
- B: RD 8.10, punto 4: el encuadre es una decisión abierta.
- **Propuesta:** "Con el encuadre provisorio de este borrador, el resultado se presenta como…".

### C11. "Doce etapas" frente a trece filas — menor

- RD 8.8 y CO 9.5: "son doce etapas de análisis". RD 6.4: la tabla tiene trece filas (incluye la comprobación estratificada no registrada). CI: doce filas.
- No es un error de cifra, pero el lector cuenta trece. **Propuesta:** en 6.4, presentar la comprobación no registrada como nota al pie de la fase 2 y no como fila.

### C12. Afirmar y desdecir en frases contiguas — menor

- RD 8.2: "Esa ventaja no proviene de lo que ocurrió antes" y, al final del párrafo siguiente, "La posición es, además, tiempo transcurrido: lo que el resultado descarta es un aporte del contenido fisiológico de las ventanas previas, no que el modelo use contexto temporal". **Propuesta:** decirlo bien la primera vez: "Esa ventaja no proviene de la fisiología de las ventanas previas, sino del tiempo transcurrido en el estímulo".
- RD 7.3: "Los resultados no dependen de una sola persona" (curva) frente a 7.1 "una persona, P4, aporta 0,009 de los 0,036" (contraste principal). No se contradicen, pero conviene que 7.3 diga "El resultado de 6 s no depende…".
- RD 7.8: "las caídas son 0,053 para el EEG…" y en la misma viñeta "no demuestra que el EEG aporte". Ordenar: primero el aviso de ruido, después las cifras.

### C13. DF dice "OpenAlex"; RD dice "un catálogo bibliográfico" — menor

Mismo hecho, dos nombres. Unificar en la nota de trabajo (ver P7).

### C14. CO pierde "mediana" — menor

- RD 7.6: "una mediana de 3,5 % de la varianza", "una mediana de 72 %".
- CO 9.3: "que representan 3,5 % de la varianza", "que suman 72 % de la varianza".
- **Propuesta:** restituir "una mediana de" en CO.

---

## 4. Frases a medio editar

| # | Ubicación (frase inicial) | Problema | Gravedad | Propuesta |
|---|---|---|---|---|
| F1 | RD 6.3 "Que "respaldo" exija Holm e "inferior" no es una asimetría…" | Sintaxis ambigua: se lee "inferior no es una asimetría" | importante | Pasaje reescrito 1 |
| F2 | RD 6.1, viñeta "**Atención.**" | Una viñeta de unas 230 palabras y 11 frases; definición, historia y límites intercalados | importante | Pasaje reescrito 2 |
| F3 | RD 7.3 "El historial que excluye las seis ventanas más recientes, y que por lo tanto…" | Más de 60 palabras, dos paréntesis encadenados, uno con dos puntos dentro | importante | Pasaje reescrito 3 |
| F4 | RD 7.3 "Solo el desfase de 6 s alcanza respaldo…" | La misma idea tres veces; nota de redondeo en medio | importante | Pasaje reescrito 4 |
| F5 | RD 7.6 "La limpieza es parcial. La correlación máxima…" | Párrafo de añadidos: afirma la cota, la desdice, redefine lo medido, vuelve a inferir | importante | Pasaje reescrito 5 |
| F6 | RD 7.2 "Con la etiqueta corregida la posición sola deja de predecir…" | Seis añadidos sucesivos; "aunque la decisión registrada…" corta la primera frase | importante | Pasaje reescrito 6 |
| F7 | RD 8.4 "En activación el modelo con historial rinde mejor, y hay apoyo acotado…" | Un párrafo de unas 330 palabras; mezcla dos contrastes | importante | Pasaje reescrito 7 |
| F8 | RD 8.1, tabla | Celdas de hasta cinco frases | importante | Pasaje reescrito 8 |
| F9 | CO 9.1 "En activación, agregar el historial de las señales…" | Inciso entre paréntesis dentro del sujeto; la salvedad tónica dos veces | importante | Pasaje reescrito 9 |
| F10 | CO 9.7 | La primera y la tercera frase dicen lo mismo | importante | Pasaje reescrito 10 |
| F11 | CO 9.3 "Las mayores mejoras en activación se obtuvieron… y aun así es bajo." | Concordancia: "es bajo" no tiene sujeto | menor | "…y al predecir por estímulo (AUC 0,587); aun así, el desempeño es bajo." |
| F12 | CO 9.3 "…se lee como una cota inferior, porque la limpieza es parcial; es la lectura más defendible y no una demostración, porque los componentes…" | Dos "porque" de sentido opuesto en una frase | menor | Partir en dos frases, como en el pasaje reescrito 5 |
| F13 | RD 7.6 "El desfase no se corrigió, porque las ventanas vigentes están congeladas; puede atenuar…; ese efecto no se midió." | Tres oraciones unidas con punto y coma | menor | "El desfase no se corrigió, porque las ventanas vigentes están congeladas. Puede atenuar la relación entre el EEG y las demás señales, incluidas las etiquetas; ese efecto no se midió." |
| F14 | RD 7.6 "Según el signo con que se estimó (el EEG responde al parpadeo…), cada ventana de EEG contendría…; esa dirección falta confirmarla en el script de montaje." | Pendiente de trabajo dentro del texto | menor | Mover a nota de trabajo (P9) |
| F15 | RD 7.7 "…la decisión pasa a "inferior" al quitar una sola persona, si es cualquiera de cinco personas concretas." | Construcción torpe | menor | "…y la decisión pasa a "inferior" al quitar a cualquiera de cinco personas." |
| F16 | RD 7.7 "(p Holm 0,049; 0,0495 en el CSV, que el INFORME muestra como 0,050 por un redondeo doble)" | Proceso en paréntesis | menor | "(p Holm 0,049)" y nota de trabajo (P2) |
| F17 | RD 7.8 "…y peor en textos (0,60 sin historial; 0,63 con historial, donde solo queda por debajo una categoría con 25 personas)" | No se entiende qué categoría ni por qué importa | menor | "…y peor en textos (0,60 sin historial y 0,63 con historial). Con historial, la única categoría con AUC menor es una que solo tiene 25 personas." |
| F18 | RD 7.8 "Es un descriptivo ruidoso y no demuestra que el EEG aporte: no se demostró aporte del EEG de la ventana actual (0,524; sección 7.7)." | "no demuestra… no se demostró" | menor | "Es un descriptivo ruidoso: no demuestra que el EEG aporte, y el EEG de la ventana actual no supera el azar de forma demostrable (0,524; sección 7.7)." |
| F19 | RD 6.2, viñeta del historial desplazado, "Estos modelos reciben además una columna…" | Dos relativas y un punto y coma; "que el informe de origen no declara" es proceso | menor | "Estos modelos reciben además una columna con el número de ventanas desplazadas, que codifica la posición en el estímulo. Es igual en el historial real y en el placebo, de modo que no afecta ese contraste, pero sí entra en el contraste "desplazado menos sin historial"." La frase sobre el informe va a nota de trabajo. **Atención:** "de modo que no afecta ese contraste" es una inferencia que el original no escribe; confirmar antes de usarla o suprimirla. |
| F20 | RD 6.3 "…ambos hechos con un asistente automático a pedido del autor; no son revisiones de un tercero, y es a ellos a los que este texto llama "auditoría"." | Definición al final de una frase larga | menor | Ver P1: va a la declaración de uso de asistentes |
| F21 | RD 6.4, fila "Reapertura, fase 1", columna Estatus | 60 palabras en una celda | menor | Celda: "Registrado; familia fijada antes de correr (P1, P2) y curva secundaria". El resto ya está en 6.3 y 7.1 |
| F22 | RD 8.2 "…aunque la decisión registrada de ese contraste (A1) fue "inferior", por −0,008 y al filo (límite superior del intervalo, −0,001)." | Repetición literal de 7.2 con dos incisos | menor | "La etiqueta corregida por posición elimina ese efecto y la detección baja poco (0,675 frente a 0,683; sección 7.2)." |
| F23 | RD 8.3 "Esta sección resume… Las referencias se verificaron…" | Tres frases de proceso abren la sección | menor | Nota de trabajo (P7) |
| F24 | RD 8.3 "La detección por alfa y beta también disminuye, lo que es coherente con la literatura: el dipolo…" | 62 palabras tras los dos puntos, tres citas | menor | Partir: "…coherente con la literatura. El dipolo córneo-retinal se concentra en frecuencias bajas (…). El potencial de espiga sacádica, en cambio, abarca aproximadamente de 20 a 90 Hz y alcanza la parte alta de beta (…). Además, la actividad de los músculos frontal y temporal puede ocultar o imitar los ritmos beta y alfa (…)." Igual en DF 8.x.2 |
| F25 | RD 8.4 "Dentro de un mismo estímulo no se demostró que el historial supere al tiempo transcurrido; ese resultado es inconcluso y de poca potencia, y no demuestra ausencia de efecto ni que el aporte se explique por el tiempo transcurrido." | Tres negaciones | menor | "Dentro de un mismo estímulo la comparación entre el historial y el tiempo transcurrido es inconclusa y de poca potencia: no permite afirmar que el historial aporte ni que su aporte se reduzca al tiempo transcurrido." |
| F26 | DF 8.y "Esta diferencia de escalas es coherente con el resultado temporal de la tesis, cuyo apoyo más sólido…" y la frase siguiente | Dos frases de más de 60 palabras; salvedad ajena al argumento | importante | Ver C6 |
| F27 | DF 8.x.4 "Una red convolucional compacta que aprende… (del tipo EEGNet; Lawhern et al., 2018) supera…" | El paréntesis separa sujeto y verbo sin coma de cierre | menor | "Una red convolucional compacta del tipo EEGNet (Lawhern et al., 2018), que aprende directamente de la serie temporal del EEG sin variables calculadas a mano, supera…" |
| F28 | SP 4.6.1 "Equivale a correr las ventanas de EEG… (0,184 a 0,528 s sobre 2 s, *calculado desde*…; el informe de origen dice…): no invalida…" | Paréntesis de proceso de 25 palabras antes de los dos puntos | menor | "Equivale a correr las ventanas de EEG entre 9 % y 26 % de su duración respecto de las otras señales. No invalida los resultados, pero…" y nota de trabajo |
| F29 | SP 4.3 "Las notas no documentan con qué criterio se armaron los grupos; lo que consta en los datos es que…" | Más de 60 palabras con la nota de cálculo incluida | menor | Partir en tres frases y sacar la nota de cálculo |
| F30 | SP 4.7, tabla, fila "Pupilometría" | Dos paréntesis explicativos dentro de una celda | menor | Celda con nombres de variables; la explicación ya está en 4.6.5 |
| F31 | SP 4.5.2 "…25.498 de 25.992 posiciones de componentes quedaban desplazadas; ese denominador es el archivo completo de 48 personas, no el número de etiquetas que cambian." | Aclaración de auditoría incrustada | menor | Anexo (P10) |

---

## 5. Material de proceso y dónde reubicarlo

Ningún elemento se propone borrar. Tres destinos:

- **Anexo de trazabilidad** (nuevo, en la tesis): tabla de análisis con nombre, fecha, estatus, carpeta y commits; correspondencia sección → fuentes; fe de erratas de los informes.
- **Nota de trabajo** al pie de la sección, con el formato que DF ya usa en 8.x.2 ("> Nota de trabajo (no va en la tesis): …"). Es el modelo correcto y solo existe en un lugar.
- **Documento de cierre** (CI), que ya contiene casi todo.

| # | Qué | Dónde está | Destino |
|---|---|---|---|
| P1 | "El protocolo de cada etapa… (orden de commits verificado)… revisión de código… asistente automático… es a ellos a los que este texto llama "auditoría"" | RD 6.3; SP 4.8.3 "Registro previo"; callouts de los cuatro borradores | En el capítulo queda una frase de método: los contrastes se fijaron antes de ejecutar y no hay registro externo con sello de tiempo. El detalle va al anexo. La declaración de uso de asistentes automáticos va en una sección propia, cuya forma es una pregunta abierta para el profesor según CI |
| P2 | "el INFORME muestra … por un redondeo doble" | RD 7.2 (−0,0025), 7.3 (0,017474), 7.6 (0,044497), 7.7 (0,0495) | Fe de erratas del anexo; CI ya lo registra en "Menores". En el texto queda la cifra correcta, sola |
| P3 | "(comprobación de la auditoría de código del 26-11)", "(recálculo de la auditoría final)", "pedida por la auditoría de resultados", "agregada por la auditoría de código antes de correr", "según la auditoría" | RD 6.1, 7.1 (cuatro veces), 7.3 (tres), 7.5, 7.6 (dos), 7.8; SP 4.5.2, 4.6.3, 4.6.4 ("comprobación `c03`", "`c09`") | En el texto: "análisis descriptivo no registrado", que es lo que el lector necesita saber. Quién lo pidió va al anexo |
| P4 | "Un diagnóstico del 26-11, que reajustó un solo grupo de una partición…" | RD 7.2 | Pasaje reescrito 6: queda el hecho; fecha y ruta van a nota de trabajo |
| P5 | Líneas "Fuentes:" con rutas de `INFORME.md` y CSV | Final de cada sección de RD, DF, CO y SP | Tabla sección → fuentes en el anexo. Mientras sean borradores pueden quedar, marcadas como nota de trabajo |
| P6 | Fechas como nombre de análisis: "el 16-11", "la fase 1 del 22-11", "enmienda", "reapertura", "cierre V3", "ampliación E1–E6", "enfoques E1–E4" | Todo RD; CO 9.1, 9.2, 9.5; DF | Nombrar cada análisis por su contenido y dejar la fecha solo en el anexo. Propuesta de nombres: *evaluación con particiones originales* (cierre V3), *análisis principal* (16-11), *análisis principal repetido* (22-11, cinco particiones), *control con placebo*, *historial desplazado*, *curva temporal*, *control de posición post hoc* (18-11) y *registrado* (fase 3), *AUC estratificada*, *etiqueta corregida por posición*, *aporte por señal*, *limpieza ocular*, *red sobre la señal cruda*. La tabla 6.4 completa pasa al anexo |
| P7 | "Las referencias se verificaron en un catálogo bibliográfico… 10 en texto completo y 8 solo por resumen…" | RD 8.3; DF callout | Nota de trabajo; CI ya lo lista como trabajo de cierre |
| P8 | "cuya base anatómica falta confirmar en el texto completo" | RD 8.5; DF 8.y | Nota de trabajo junto a la frase. No retirarla hasta leer la fuente: es un pendiente real |
| P9 | "esa dirección falta confirmarla en el script de montaje"; "lo que queda por confirmar en `scripts/montaje_ocular_41p.py`"; "el informe de origen dice "entre un 12 % y un 25 %"" | RD 7.6; SP 4.6.1 | Nota de trabajo; pendiente real |
| P10 | Historia de la etiqueta V2: "Por qué V2", fechas de detección, 25.498 de 25.992 posiciones, "se reprodujo… con tolerancia 1e-12" | SP 4.5.2 | En el capítulo: "una versión anterior tenía un error de alineación; no se usa". El resto al anexo |
| P11 | Nombres de columnas, archivos, semilla y hash: `pupil_n`, `pupil_both_valid_fraction`, `Test_Participant`, `SlowWeb G1`, `20260822`, `dc51dc19…`, "tolerancia 1e-8" | SP 4.3, 4.5.2, 4.6.5, 4.7, 4.8.2 | Anexo de reproducibilidad. En el texto, el nombre en español |
| P12 | "*(calculado desde …)*" | SP, 16 veces | Convención declarada del borrador: correcta mientras sea borrador. Al pasar a LaTeX, tabla del anexo |
| P13 | "No se corrigió, porque el código y los resultados están congelados; se describe tal como es" | SP 4.6.4, 4.6.5; RD 8.8 (con ruta a `AUDITORIA_SECCIONES_PENDIENTES.md`) | En el texto: "No se corrigió". El motivo y la ruta, al anexo |
| P14 | "La comprobación de reproducibilidad del cierre verifica hashes y el orden del registro; no vuelve a entrenar los modelos" | RD 8.8 | No es una limitación científica: va al anexo; CI ya lo dice |
| P15 | "La experimentación está cerrada desde el 23-11-2026: reabrirla requiere…"; "(el cálculo de tamaño de muestra está en `resultados/protocolo_…`)" | RD 8.9 | CI ya lo contiene; en la tesis, anexo |
| P16 | Sección 8.10 "Decisiones abiertas" y callouts de advertencia | RD, CO, SP | No es una sección de tesis, pero las reglas del proyecto exigen que las decisiones abiertas sigan visibles: debe quedar como nota de trabajo al final del borrador hasta que se resuelvan, y no entrar al LaTeX |
| P17 | "*Redacción ajustada el 26-11-2026… pendiente de revisión por Mario.*" | SP 1.4 | Nota de trabajo |
| P18 | Códigos de contraste sin tabla a la vista: "(R3)", "(R4)", "(A1)", "C2", "L2", "Q1", "P1, P2" | RD capítulo 8; DF 8.x.4 y 8.y; CO no los usa (bien) | En la discusión, nombrar el contraste; los códigos solo en las tablas de resultados y en el anexo |
| P19 | "La ganancia a igual posición parecía contradecir el análisis del 18-11. Una comprobación no registrada… mostró que no" | RD 7.2, "AUC estratificada" | Es relato de proceso. En el texto: los dos resultados y por qué son compatibles (se comparan con modelos distintos) |
| P20 | "Mario comunicó el 01-11-2026 que su profesor aprobó usar las pseudoetiquetas GSR V2 (`notas/bitacora.md`)" | SP, callout | Está bien donde está (callout de estado, presentado como registro y no como aprobación). No debe pasar al cuerpo de la tesis |

---

## 6. Orden y estructura

### O1. RD 6.1: definir primero, limitar después — importante
Cada viñeta debería seguir el mismo orden: cómo se calcula, cómo se binariza, qué señales usa el *Modelo Estudiante*, qué es en la práctica, qué queda abierto. Pasaje reescrito 2 para atención; la de activación ya tiene casi ese orden.

### O2. RD 6.3 son tres secciones — importante
Dividir en: **6.3 Diseño de evaluación** (configuración, validación cruzada, cambio de diseño); **6.4 Inferencia y reglas de decisión** (unidad, bootstrap, Holm y remisión a la tabla de 4.8.3, que hoy está duplicada); **6.5 Registro y alcance de la evidencia** (qué se fijó antes, qué es post hoc, personas ya consultadas). La tabla actual de 6.4 va al anexo, y en el capítulo queda una versión de tres columnas (análisis, pregunta que responde, estatus).

### O3. El bloque de selección de configuración está antes de lo que necesita — importante
RD 7.1 "Selección de la configuración y grupos de personas" usa en su tabla "Con posición (Q1)", "Historial − placebo", "Historial desplazado 6 − placebo", "Banda de 6 s − placebo" y "GRU hasta 32 − GRU una ventana", que se presentan en 7.3 y 7.4. **Propuesta:** nueva sección después de 7.4, "Estabilidad del efecto de activación entre grupos de personas", con las dos tablas y el párrafo "Los contrastes del HGB con historial hasta 32 se concentran…". En 7.1 queda una frase con remisión.

### O4. RD 7.3: reordenar — importante
Orden actual: placebo, curva, comparación de dos contrastes, estratificada, historial frente a posición, persistencia, límites. Orden propuesto: (1) persistencia de la etiqueta, porque da el marco: el estado dura segundos; (2) placebo e historial desplazado; (3) curva temporal y sus límites propios (73 % del mismo estímulo); (4) controles: estratificada y posición. La parte de "Límites de la curva" que describe el filtro tónico sale de aquí (R3).

### O5. RD 7.6 son tres secciones — importante
"Aporte de cada señal", "Limpieza ocular" y "Red sobre la señal cruda" como secciones propias. "Montaje y sincronía" es calidad de datos y pertenece al capítulo 4 o 5: SP 4.6.1 y 4.7 ya contienen esos párrafos casi literales.

### O6. Elegir entre RD 8.3/8.5/8.7 y DF — importante
Son el mismo texto dos veces. Opción recomendada: DF es el texto de las secciones 8.3 y 8.5 (es más claro y trae las referencias) y las versiones de RD se eliminan del borrador, dejando el enlace. RD 8.7 y DF 8.z son literales: conservar una.

### O7. RD 8.8: 21 viñetas en cinco grupos — importante
(1) **Muestra y evaluación:** personas ya consultadas; cambio de diseño; selección de configuración; grupos con el mismo orden de estímulos; multiplicidad entre etapas; precedencia de reglas; post hoc. (2) **Etiquetas:** offline y relativas a la sesión; elección de la componente principal; conducta de mirada y soporte mayor de 2 s; nivel tónico y soporte mayor de 6 s; 53 % de las ventanas. (3) **Señales y procesamiento:** desfase de reloj; dos imprecisiones del procesamiento; limpieza parcial. (4) **Modelos:** sin búsqueda; red sin control propio; modelo por estímulo no causal; adaptación offline. (5) **Tamaño y potencia:** AUC bajas; peso igual por persona sin mínimo de ventanas; estratos con 2–3 % de los pares. Abrir la sección con una frase que diga cuáles tres condicionan las conclusiones.

### O8. RD 8.7 — menor
La viñeta "Sincronía entre equipos" es un límite (ya está en 8.8), no una implicancia. Quedan tres implicancias.

### O9. El capítulo 8 no discute la adaptación a la persona — importante
Ver E3.

### O10. Tablas que no se entienden solas

| Tabla | Problema | Propuesta | Gravedad |
|---|---|---|---|
| RD 7.1, primera | Columna "Análisis" con fechas; no dice que las dos filas son el mismo contraste | Columna "Particiones" (una; cinco, promedio); la explicación ya está debajo | menor |
| RD 7.1, por grupo | Sin título; filas con códigos y fechas; la columna de 41 personas sin intervalos y las otras con ellos | Título, nota de que es descriptiva y no registrada, nombres de contraste sin fecha | importante |
| RD 7.2 y 7.3, curvas | "placebo disperso" y "placebo de bloque" no se definen en ningún lugar del documento | Definirlos en 6.2, donde hoy solo dice "un placebo de la misma persona a 150 s o más" | importante |
| RD 7.6, B1–B8; 7.7, C1 | Columna "Mejoran" en contrastes contra 0,5: no es "mejoran" sino "personas sobre el azar" | "A favor", con la nota que ya existe bajo la tabla L1–L4 | menor |
| RD 7.6, variables de EEG | "Caída" no dice entre qué columnas | "Caída (original − sin componentes oculares)" | menor |
| RD 7.6, L1–L4 | "Control" sin definir en la tabla | "EEG sin 3 componentes no oculares (control)" | menor |
| RD 7.3, Q1–Q2 | Dos columnas de p sin explicación | Nota: "p sin ajustar y p de Holm sobre las cuatro pruebas de la fase" | menor |
| RD 8.1 | Celdas con cinco frases | Pasaje reescrito 8 | importante |
| CI, auditoría de código | La tabla está entre "Cuatro afectan lecturas…:" y la lista H1–H4 | Tabla después de H1, que es el hallazgo que la usa | menor |

### O11. Términos usados antes de definirse

| Término | Primer uso | Definición | Gravedad |
|---|---|---|---|
| AUC | RD 6.1 ("AUC 0,911") | RD 6.2, última viñeta; antes solo en el callout, que no irá a la tesis. En CO no se define | menor |
| kappa | RD 6.1 ("kappa 0,33") | "kappa de Cohen" dos párrafos después | menor |
| cierre V3 | RD 6.3 | RD 6.4 (tabla). En CO 9.2 se usa sin definir | importante |
| fase 2, A1, A2 | RD 6.3 | 6.4 y 7.2 | menor |
| Q1 | RD 7.1 (tabla) | 7.3 | menor |
| placebo disperso, placebo de bloque | RD 7.2 | nunca | importante |
| selección anidada | RD 7.1 | nunca | menor |
| modelo de referencia | RD 7.6 ("supera al modelo de referencia") | nunca; se entiende que es el HGB con variables calculadas | menor |
| PCA | RD callout y 8.10 ("profesor PCA"); CO 9.5 | nunca se desarrolla (análisis de componentes principales) | importante (ver N3) |
| GRU | CO 9.5 ("la GRU") | en CO no; 9.1 dice "la red recurrente" | menor |
| IC 95 % | DF 8.x.2 | nunca | menor |
| EEGNet, OpenBCI Cyton+Daisy | RD 6.2, 7.6 | nombres propios; basta la cita y el modelo del equipo en 4.6.1 | menor |
| "tabla de criterios de interpretación del manuscrito" | RD 8.1 | está en SP 4.8.3; falta la remisión | menor |
| E1–E6 (ampliación) | RD 6.4 | nunca se dice qué es cada uno | menor; desaparece con P6 |

---

## 7. Equilibrio

### E1. El historial desplazado frente al placebo quedó con menos fuerza de la que sus datos permiten — importante

Lo que el propio texto dice de este contraste, repartido en cinco lugares:

- registrado antes de correr (enmienda del 16-11);
- +0,046 [+0,018; +0,073], 28 de 41 personas, p de Holm 0,004;
- positivo en los dos grupos de personas, con intervalos que excluyen el cero en ambos: +0,035 [+0,003; +0,064] en las 25 de la búsqueda y +0,064 [+0,015; +0,115] en las otras 16 (tabla de 7.1);
- estable ante el tamaño del desplazamiento: +0,040 [+0,012; +0,066] con cinco ventanas;
- un análisis distinto da un valor parecido: +0,047 [+0,017; +0,078] con placebo disperso y +0,053 [+0,026; +0,081] con placebo de bloque;
- no depende de una persona: +0,039 y +0,046 sin la más influyente;
- la GRU, que no tuvo búsqueda de configuración, da +0,051 y también es positiva en ambos grupos.

Cómo se presenta:

- RD 7.3: en mitad de un párrafo, dentro de una frase de más de 60 palabras, con el paréntesis "(respaldo, no efecto relevante: el límite inferior es 0,018)".
- RD 8.4: una frase, seguida de nueve frases de salvedades. Seis de ellas (varias estimaciones del contraste principal, no confirmación, efecto desigual, concentración en las 25, sesgo de selección, patrón inverso en V3) describen **otro contraste**. El dato de que este es positivo en ambos grupos llega al final, como excepción, cuando es lo que lo distingue.
- RD 8.4, título: "indicio".
- CO 9.1: sin el p de Holm, sin las 28 de 41 personas, sin la palabra "respaldo", y con el inciso de salvedad dentro del sujeto de la frase.
- CO 9.7: "efecto pequeño, desigual entre personas". "Desigual" (mediana +0,014; 23 de 41) es una propiedad del contraste simple, no de este.

La única salvedad que le corresponde de lleno es la del soporte tónico de la etiqueta, y es seria: impide leerlo como "el pasado predice el presente". Pero es una salvedad sobre **qué** demuestra, no sobre **si** el efecto existe. Hoy el texto mezcla las dos. **Propuesta:** pasajes reescritos 3, 7 y 9, que separan "lo que se sostiene y su límite propio" de "lo que es frágil".

### E2. La detección de atención desde el EEG nunca se afirma en positivo — importante

Según el texto: 0,681, sobre el azar en 41 de 41 personas (B1: +0,181 [+0,164; +0,197]); control con etiquetas barajadas 0,496; a igual posición 0,677; tras quitar los componentes oculares 0,621, sobre el azar en 41 de 41 (L3: +0,121 [+0,107; +0,135]). Es el resultado más robusto del trabajo, y en 8.3, CO 9.3 y CO 9.7 solo aparece como aquello de lo que hay que desconfiar. La desconfianza sobre su **origen** es correcta; la detección de la etiqueta definida no está en duda. **Propuesta:** una frase al inicio de 8.3 y de CO 9.3, con cifras que ya están en el texto: "El *Modelo Estudiante* predice el *Attention Score* desde el EEG con claridad (0,681; sobre el azar en las 41 personas), y sigue haciéndolo tras retirar los componentes oculares (0,621, también en las 41). Lo que estos datos no permiten establecer es el origen de esa detección."

### E3. La adaptación a la persona, un "efecto relevante" registrado, no se discute — importante

RD 7.7: adaptado menos general con historial en activación, +0,045 [+0,023; +0,069], 30 de 40, p de Holm 0,0004, efecto relevante; y la detectabilidad por persona es estable entre mitades (0,76 y 0,66). El capítulo 8 solo lo menciona en 8.8 ("no es utilizable en línea"). CO 9.3 lo cita en una frase que termina en "y aun así es bajo". Es uno de los dos únicos "efecto relevante" de activación en contrastes registrados y sugiere que la activación tiene un componente individual fuerte. **Propuesta:** un párrafo en 8.4 u 8.5, con su límite (offline; se evalúa en la parte final de la sesión).

### E4. El nulo de atención es el resultado mejor establecido, y está bien contado — sin cambios
Registrado, replicado (post hoc y fase 3), con intervalo de 90 % dentro del margen. 8.2 lo presenta con la fuerza que tiene. Solo sobra el "nada" (C5).

### E5. Dos excesos en sentido contrario — importante

- RD 8.1, tabla: "Sí" para el contraste principal de activación sin matiz en la misma celda hasta la tercera frase; y CO 9.7 "ayudan a predecir la activación". Según 6.1, las etiquetas "describen el *Attention Score* y el *Arousal Score* definidos, no una medida externa". **Propuesta:** "predecir el *Arousal Score*" en CO 9.7 y en el título y primera frase de 8.4.
- RD 8.5 y DF 8.y usan el resultado temporal como corroboración de la explicación fisiológica (C6).

### E6. La especificidad del control de la limpieza — menor
El control (quitar una mediana de 72 % de la varianza deja la AUC en 0,674) es un buen diseño y el texto lo dice. La frase que lo sigue ("acota la objeción y no la elimina") es justa. Aquí el equilibrio es correcto en RD 7.6; se rompe después, en el párrafo "La limpieza es parcial" (pasaje reescrito 5).

---

## 8. Cumplimiento de reglas

| # | Regla | Estado | Ubicación y propuesta | Gravedad |
|---|---|---|---|---|
| N1 | Decisiones abiertas presentadas como abiertas | Cumple en general | Excepciones: C10 ("debe presentarse"); SP 4.5.2 "Por eso la variable objetivo se limita a un solo eje, la activación, y se nombra así en todo el documento" → agregar "de forma provisoria"; C9 (numeración y lista incompleta en SP) | importante |
| N2 | Ninguna aprobación del profesor afirmada | Cumple | La única mención (SP, callout, pseudoetiquetas GSR V2) está presentada como registro de bitácora y no como aprobación de resultados. No debe salir del callout | — |
| N3 | Términos acordados | **No cumple en un caso** | "el profesor PCA" (RD callout punto 7 y 8.10 punto 7; CO callout y 9.5 dos veces; CI cuatro veces): reduce *Modelo Profesor* a "profesor", usa una sigla sin desarrollar y, en 8.10, convive con "profesor guía" en la misma lista ("Si el profesor PCA queda…"). Propuesta: "el *Modelo Profesor* de componente principal". También SP, tabla final: "Los dos *Modelos Profesores*" → "las dos versiones del *Modelo Profesor*" | importante |
| N4 | "Activación" y no "emociones" | Cumple | "emociones" solo entre comillas o al citar la hipótesis. "Emoción" en RD 8.5 y DF 8.y pertenece a la cita de Critchley (2002): correcto. Título "4.5.2 Definición Emoción" es el del esqueleto y lleva advertencia | — |
| N5 | Observado / Atendido | Cumple | Bien usado en RD 6.1, 8.2, 8.3, 8.7; DF 8.x.3, 8.z; CO 9.3; SP 4.6.4. En SP 1.4 la pregunta 3 habla de "pseudoetiquetas de atención" sin la distinción; no es necesario allí | — |
| N6 | *Attention Score*, *Arousal Score* | Cumple, con un desliz | "predecir la activación" por "predecir el *Arousal Score*" en CO 9.7 (dos veces), RD 8.4 y 8.5 (E5) | menor |
| N7 | Siglas desarrolladas en el primer uso | Parcial | Ver O11. En RD, AUC se usa antes de desarrollarse y PCA nunca; ROC se desarrolla dos veces (callout y 6.2). En CO no se desarrolla ninguna (AUC, EEG, GSR, GRU): si el capítulo 9 se lee solo, conviene al menos AUC. En DF, IC. SP cumple (tiene glosario en el callout y desarrolla SCR, UTC, I-VT, BA en el texto) | menor |
| N8 | No completar pendientes con texto supuesto | Cumple | SP declara lo que no tiene insumo (4.3, tabla final). CO declara que el capítulo 9 sigue pendiente en el esqueleto | — |
| N9 | No presentar test consultado como confirmación | Cumple, en exceso | Ver R1: dicho siete veces en RD | — |

---

## 9. Diez pasajes reescritos

Regla seguida: no se agregan ni se quitan cifras, hechos ni salvedades de fondo; se reordena, se fusionan repeticiones y se limpia la sintaxis. Cuando un dato de proceso sale del párrafo, queda en una "Nota de trabajo" inmediatamente debajo, con el formato que DF ya usa.

### Pasaje 1 — RD 6.3, reglas de decisión

- **Inicio:** "El margen de 0,02 no está aprobado por el profesor guía."
- **Fin:** "Con la precedencia inversa, las seis "inferior" serían "nulo concluyente"."

> El margen de 0,02 no está aprobado por el profesor guía. Varias decisiones dependen de él y quedan cerca del umbral; se indican en cada caso.
>
> Dos aspectos de la regla registrada condicionan la lectura. El primero es una asimetría que no tiene una justificación escrita: "respaldo" exige la corrección de Holm e "inferior" no. El segundo es la precedencia. Los protocolos listan las reglas sin fijar cuál prevalece cuando una fila cumple dos a la vez, y el código las aplica en el orden respaldo, inferior, nulo concluyente. Eso ocurre en ocho filas, todas de atención y todas con el intervalo de 90 % dentro de ±0,02. Seis quedan como "inferior": las bandas de 24, 48 y 96 s de la curva temporal, las de 48 y 96 s frente al placebo de bloque, y A1 de la etiqueta corregida. Dos quedan como "respaldo": la AUC estratificada dentro del mismo estímulo y A2. Con la precedencia inversa, las seis "inferior" serían "nulo concluyente".

### Pasaje 2 — RD 6.1, viñeta de atención

- **Inicio:** "- **Atención.** El *Attention Score* se obtiene como la primera componente principal…"
- **Fin:** "…de modo que el soporte temporal de la etiqueta excede los 2 s (sección 8.2)."

> - **Atención.** El *Attention Score* se obtiene como la primera componente principal de cinco variables de mirada y pupila (tiempo y duración de fijaciones, dispersión y recorrido de la mirada, pupila normalizada), ajustada con las 25 personas de entrenamiento. La componente explica el 51,5 % de la varianza de las cinco variables. Cada ventana se clasifica como alta si supera la mediana de su persona. El *Modelo Estudiante* usa electroencefalograma (EEG) y respuesta galvánica de la piel (GSR).
>
>   Aunque el *Modelo Profesor* recibe mirada y pupila, en la práctica la etiqueta es conducta de mirada: en la componente pesan el recorrido de la mirada (0,557), la dispersión (0,520), la duración media de las fijaciones (0,508) y su tiempo total (0,398), y la pupila casi no pesa y entra con signo contrario (−0,052). Además, dos de esas variables suman la duración completa de las fijaciones que tocan la ventana, de modo que el soporte temporal de la etiqueta excede los 2 s (sección 8.2).
>
>   Cuál de dos versiones define el *Attention Score* es una decisión abierta. Las notas de diseño proponían la fusión con pesos iguales como definición principal y la componente principal como análisis de sensibilidad. Los análisis siguieron con la componente principal después de observar, en entrenamiento, que los modelos la predecían mejor. Una etiqueta más predecible no es por eso más válida, y ese criterio puede favorecer a la versión más ligada a los movimientos oculares que el EEG registra. Las dos versiones coinciden en 66 % de las ventanas (kappa 0,33), y los resultados de atención de este capítulo valen solo para la versión usada.

### Pasaje 3 — RD 7.3, placebo e historial desplazado

- **Inicio:** "**Placebo e historial desplazado (16-11, registrados).** El historial real supera al placebo…"
- **Fin:** "…mientras que el historial desplazado frente al placebo es positivo en ambos grupos (+0,035 y +0,064)."

> **Placebo e historial desplazado (16-11, registrados).** El historial real supera al placebo en +0,038 [+0,006; +0,068] (26/41; p Holm 0,043), y el placebo no aporta sobre el modelo sin historial (−0,004 [−0,030; +0,024]). La calibración con los primeros minutos de la persona agrega entre +0,001 y +0,009.
>
> El historial desplazado excluye las seis ventanas más recientes y, por lo tanto, no se solapa con las ventanas que promedia el *Arousal Score*. Supera a un placebo equivalente en +0,046 [+0,018; +0,073] (28/41; p Holm 0,004) y al modelo sin historial en +0,053 [+0,022; +0,083]. La decisión registrada es respaldo y no efecto relevante, porque el límite inferior es 0,018. Con cinco ventanas de desplazamiento, que dejan 1 s de solapamiento, la diferencia frente al placebo es +0,040 [+0,012; +0,066]. El desplazamiento no evita el solapamiento con el soporte del filtro tónico de la etiqueta (ver "Límites de la curva").
>
> Por grupo de personas (tabla de la sección 7.1), el historial real frente al placebo se concentra en las 25 personas con que se eligió la configuración (+0,057 frente a +0,008), mientras que el historial desplazado frente al placebo es positivo en ambos grupos (+0,035 y +0,064).

### Pasaje 4 — RD 7.3, lectura de la curva temporal

- **Inicio:** "Solo el desfase de 6 s alcanza respaldo. Su límite inferior es +0,017…"
- **Fin:** "…y en +0,046 [+0,021; +0,070] frente al de bloque."

> Solo el desfase de 6 s alcanza respaldo; su límite inferior es +0,017. A 12 s el resultado es inconcluso, y desde 24 s el contraste no se distingue del placebo. En ningún caso es un resultado nulo: ningún intervalo de 90 % cabe en ±0,02, de modo que la curva no demuestra que el efecto desaparezca. El contraste cae 0,010 por cada duplicación del desfase [−0,018; −0,003] (p 0,009; 27 de 40 personas); es una sola prueba, sin ajuste. El placebo no aporta sobre la ventana actual (+0,009 [−0,024; +0,043]) y los dos placebos rinden igual (bloque menos disperso, −0,006). Los resultados no dependen de una sola persona (sensibilidad no registrada): sin la más influyente, el contraste de 6 s queda en +0,039 [+0,012; +0,065] frente al placebo disperso y en +0,046 [+0,021; +0,070] frente al de bloque.
>
> > Nota de trabajo (no va en la tesis): el límite inferior del desfase de 6 s es 0,017474 en `curva_temporal.csv`; el INFORME muestra +0,018 por un redondeo doble. La sensibilidad sin la persona más influyente la pidió la auditoría de resultados.

### Pasaje 5 — RD 7.6, lectura de la limpieza ocular

- **Inicio:** "La limpieza es parcial. La correlación máxima entre algún canal y los parpadeos…"
- **Fin:** "…baja de 0,59–0,60 (estimación del 22-11) a 0,55–0,56, sobre el azar en 38 de 41 personas."

> Lo medido es que la AUC sobre el azar baja cerca de un tercio al quitar esos componentes. La lectura del resto enfrenta dos objeciones de sentido opuesto, que el diseño no separa.
>
> La primera es que la limpieza es parcial. La correlación máxima entre algún canal y los parpadeos baja de 0,28 a 0,08 (mediana entre personas), sin anularse, y la probabilidad del modelo limpio sigue asociada al recorrido de la mirada (Spearman 0,28; antes 0,41). Tras la limpieza se mantiene además el mismo orden: canales frontales sobre posteriores (+0,059) y potencia lenta sobre alfa y beta (+0,055). Por eso no puede descartarse que el resto de la detección también dependa de los ojos; es una inferencia apoyada en el patrón espacial y espectral del remanente.
>
> La segunda es la contraria: con 11 a 16 canales, tres componentes arrastran actividad frontal no ocular (sección 8.8).
>
> Con ambas a la vista, 0,060 se lee como cota inferior de la contribución ocular. Es la lectura más defendible y no una demostración. La detección que podría defenderse como no ocular baja de 0,59–0,60 (estimación del 22-11) a 0,55–0,56, sobre el azar en 38 de 41 personas.

### Pasaje 6 — RD 7.2, etiqueta corregida por posición

- **Inicio:** "Con la etiqueta corregida la posición sola deja de predecir (0,504 [0,498; 0,510]…"
- **Fin:** "…lo que es coherente con que la posición sola no prediga la etiqueta corregida."

> Con la etiqueta corregida la posición sola deja de predecir (0,504 [0,498; 0,510]; con la original, 0,598). La mejora del historial baja de +0,029 a +0,010 y, con la posición como variable, queda en +0,004. La detección baja poco (0,675 frente a 0,683).
>
> Dos de las tres decisiones están al filo. A1 (−0,008) es "inferior" porque el límite superior de su intervalo es −0,001, y la regla no exige Holm para "inferior". Además compara AUC frente a dos objetivos distintos (cambia el 9,4 % de las etiquetas), por lo que no implica que la detección original fuera espuria. A3 sería "respaldo" con un p de Holm bajo 0,05; es 0,055.
>
> En este análisis las predicciones del modelo con historial y posición son idénticas a las del modelo con historial, de modo que A3 equivale a comparar el modelo con historial con el de la ventana actual con posición. Un diagnóstico posterior, que reajustó un solo grupo de una partición, indica que no es un error: el modelo recibe la columna de posición y no la usa en ninguna de sus 1.800 divisiones, lo que es coherente con que la posición sola no prediga la etiqueta corregida.
>
> > Nota de trabajo (no va en la tesis): el diagnóstico es del 26-11 y está en `documentacion/auditoria_final_23-11-2026/ronda2/DIAGNOSTICO_E1_POSICION.md`.

### Pasaje 7 — RD 8.4, primer párrafo

- **Inicio:** "En activación el modelo con historial rinde mejor, y hay apoyo acotado…"
- **Fin:** "…impiden tratar el efecto como una propiedad establecida de la muestra y debilitan el "respaldo" del contraste principal."

> En activación el modelo con historial rinde mejor, y hay apoyo acotado a que esa mejora no se explique solo por la persona. Los dos contrastes que lo sostienen no tienen la misma solidez.
>
> El apoyo más sólido es el contraste registrado antes de correr en la enmienda del 16-11: el historial sin las ventanas de 6 s que promedia la etiqueta supera a un placebo en +0,046 (p Holm 0,004). Es positivo tanto en las 25 personas con que se eligió la configuración como en las otras 16 (+0,035 y +0,064), igual que el contraste de la GRU (+0,045 y +0,059); la comparación por grupo es descriptiva y no registrada. Su límite es otro. Ese contraste excluye las ventanas que promedia la etiqueta, pero no el soporte del filtro tónico de la GSR: cerca de un cuarto del peso de la componente dominante de la etiqueta cae antes de esas ventanas (sección 7.3). Por sí solo no separa "la fisiología previa predice la activación posterior" de "la fisiología de un momento se relaciona con la GSR de ese mismo momento, que la etiqueta posterior todavía contiene".
>
> El contraste principal, historial menos sin historial, es más frágil. Se estimó varias veces sobre las mismas 41 personas, con diferencias de AUC entre +0,028 y +0,047, y no todos los intervalos excluyen el cero. El respaldo de la fase 1 del 22-11 sale de un análisis registrado sobre personas ya consultadas, que promedia cinco particiones nuevas cuando el mismo contraste ya se había visto positivo en otras tres particiones el 16-11: es una estimación más precisa de lo ya observado, no una confirmación. El efecto es desigual entre personas (mediana +0,014; mejoran 23 de 41). Tampoco es estable entre subconjuntos de personas, y esa inestabilidad se cruza con la forma en que se eligió la configuración (sección 7.1): las 15 hojas de activación las decidió el modelo con historial, con las 25 personas de entrenamiento, y es en esas 25 donde se concentra el contraste principal (+0,055, frente a +0,001 en las otras 16; con cinco particiones, +0,046 frente a +0,021). El sesgo que eso permite es posible y no está demostrado: la diferencia entre grupos no es significativa con 16 personas, y con las particiones originales del cierre V3 el patrón había sido el inverso. Estas comparaciones son descriptivas y no registradas, pero impiden tratar el efecto como una propiedad establecida de la muestra y debilitan el "respaldo" del contraste principal.

### Pasaje 8 — RD 8.1, tabla de respuesta a la hipótesis

- **Inicio:** "| Pregunta | Atención | Activación |"
- **Fin:** "…(+0,051 [+0,021; +0,080], secundario sin corrección), lo que mide el historial y no el orden |"

> | Pregunta | Atención | Activación |
> |---|---|---|
> | ¿Mejora el modelo con historial? | Sí: +0,029 [+0,021; +0,037], efecto relevante | Sí, con respaldo al promediar 5 particiones: +0,036 [+0,010; +0,065] (nota a) |
> | ¿La mejora proviene de la fisiología de las ventanas previas? | No: con la posición como variable, +0,001 [−0,002; +0,005], nulo concluyente | Apoyo acotado. El más sólido: el historial sin las ventanas de 6 s que promedia la etiqueta supera a un placebo en +0,046 (p Holm 0,004; registrado antes de correr) (nota b) |
> | ¿Queda algo al controlar la posición? | No: nulo concluyente dentro de ±0,02 | +0,032 [+0,004; +0,059], inconcluso tras Holm |
> | ¿Aporta el orden de las ventanas? | No: la GRU con historial no supera a su control (+0,008 [−0,004; +0,020]) y rinde 0,040 menos que el HGB | No demostrado: el contraste propio del orden (GRU − HGB, ambos con historial) es inconcluso, +0,020 [−0,017; +0,057] (nota c) |
>
> Notas de la columna de activación:
>
> - **a.** Por partición la diferencia va de +0,028 a +0,047, y no todos los intervalos excluyen el cero. El efecto es desigual entre personas (mediana +0,014; 23 de 41) y está concentrado en las 25 personas con que se eligió la configuración (+0,046, frente a +0,021 en las otras 16; sección 7.1).
> - **b.** Ese historial excluye las ventanas que promedia la etiqueta, pero queda dentro del soporte de su filtro tónico. En la curva, el contraste es +0,047 [+0,017; +0,078] a 6 s; a 12 s es inconcluso y desde 24 s no se distingue del placebo, sin que eso demuestre ausencia. Los controles de tiempo de sesión, posición y mismo estímulo quedaron inconclusos.
> - **c.** La GRU con historial supera a su control de una ventana (+0,051 [+0,021; +0,080], secundario sin corrección), lo que mide el historial y no el orden.

### Pasaje 9 — CO 9.1, segundo párrafo

- **Inicio:** "En activación, agregar el historial de las señales mejora la predicción del *Arousal Score*."
- **Fin:** "…el contraste del historial desplazado frente al placebo es positivo en ambos grupos (+0,035 y +0,064)."

> En activación, agregar el historial de las señales mejora la predicción del *Arousal Score*. El apoyo más sólido es el contraste registrado antes de correr: el historial sin las ventanas de 6 s que promedia la etiqueta supera a un placebo de la misma persona (+0,046 [+0,018; +0,073]), y es positivo tanto en las 25 personas con que se eligió la configuración como en las otras 16 (+0,035 y +0,064). Su límite está en la etiqueta. Ese historial queda dentro del soporte del filtro tónico, que usa toda la sesión; la etiqueta es en lo esencial el nivel tónico de la GSR, y cerca de un cuarto de su peso cae antes de esas ventanas. Por eso el contraste no demuestra por sí solo que el pasado prediga el presente. Un análisis distinto del 22-11, la curva temporal, da un valor parecido para la banda de los 6 s anteriores (+0,047 [+0,017; +0,078]; una partición, 40 personas); no es una repetición del mismo contraste.
>
> El contraste simple entre el modelo con y sin historial es menos estable: en la partición registrada el 16-11 fue inconcluso (+0,034 [−0,001; +0,069]) y al promediar cinco particiones quedó respaldado (+0,036 [+0,010; +0,065]). El efecto es además desigual entre personas (mediana +0,014; mejoran 23 de 41) y se concentra en las 25 personas con que se eligió la configuración (+0,046, frente a +0,021 en las otras 16): las 15 hojas del modelo de activación las decidió el modelo con historial, lo que permite un sesgo a su favor en esas personas. Ese sesgo es posible y no está demostrado.

### Pasaje 10 — CO 9.7, conclusión general

- **Inicio:** "Hay evidencia acotada de que las señales de los segundos previos ayudan a predecir la activación…"
- **Fin:** "…y una advertencia metodológica sobre el uso de pseudoetiquetas oculares para evaluar modelos basados en EEG."

> En activación hay evidencia acotada de que el historial reciente de las señales, el de los segundos previos, ayuda a predecir la activación: el efecto es pequeño, desigual entre personas y requiere confirmación en una cohorte nueva. En atención, lo que parecía un aporte temporal es la estructura de la etiqueta dentro de cada estímulo, y cerca de un tercio de la detección sobre el azar depende de componentes del EEG ligados a la conducta ocular, sin que el resto pueda atribuirse a un origen cerebral ni ocular. El aporte de la tesis sería entonces doble: esa evidencia acotada sobre la activación y una advertencia metodológica sobre el uso de pseudoetiquetas oculares para evaluar modelos basados en EEG. Este encuadre es provisorio y depende de la quinta decisión abierta.

**Tres avisos sobre el pasaje 10.** No cambié nada de fondo, pero al aplicarlo conviene resolver: (1) "la quinta decisión abierta" es el encuadre en la numeración de la minuta y la cohorte nueva en la del callout del propio documento (C9); (2) "predecir la activación" debería ser "predecir el *Arousal Score*" (E5), cambio que no hice porque altera un término; (3) "desigual entre personas" describe el contraste simple y no el del placebo (E1).

---

## Orden sugerido para aplicar

1. Decidir O6 (una sola versión de la discusión fisiológica) antes de tocar 8.3 y 8.5.
2. Unificar vocabulario y numeración: C1, C2, C9, N3.
3. Aplicar los pasajes 7, 8, 9 y 10 (activación) y E2 (frase positiva sobre atención).
4. Reubicar: O2, O3, O5, R1 a R3.
5. Aplicar los pasajes 1 a 6 y las correcciones de la tabla F.
6. Sacar el material de proceso a notas de trabajo y preparar el anexo de trazabilidad (P1 a P20).
7. Reducir CO 9.5 y agrupar RD 8.8 (R16, O7).

Lo que esta revisión no hizo: no recalculó ninguna cifra, no contrastó los borradores con los `INFORME.md` ni con el esqueleto sección por sección, y no revisó las referencias bibliográficas.
