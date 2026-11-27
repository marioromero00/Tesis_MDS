# Verificación independiente de la consolidación de legibilidad (ronda 9)

Fecha: 27-11-2026. Verificador independiente (asistente automático, a pedido del autor; no es la revisión de un tercero). No se editó ningún archivo existente, no se entrenó ni ajustó ningún modelo, no se corrió ningún análisis nuevo y no se hizo ningún commit. El único archivo creado es este informe.

Abreviaturas: RD = Borrador Resultados y Discusión 23-11-2026; CO = Borrador Conclusiones 23-11-2026; SP = Borrador Secciones pendientes 23-11-2026; MI = minuta de decisiones; CI = Cierre_Experimental_Final_23-11-2026; EN = ENSAYO.md; PE = notas/pendientes-cierre-26-11-2026.md; R8 = `ronda8/VERIFICACION_CORRECCIONES_R7.md`.

## 1. Veredicto

La consolidación no perdió ninguna cifra ni ninguna salvedad, y ninguna cifra quedó pegada a otro contraste, modelo, etiqueta, fecha, número de particiones o de personas. Ninguna remisión quedó rota por la consolidación. No hay errores bloqueantes.

Hay dos problemas importantes, los dos de contenido agregado y no de contenido perdido:

1. RD 8.4 dice ahora que sus seis límites van "en orden de importancia". Ese orden no existía en el texto anterior, no coincide con CO 9.1 y es una priorización que el pendiente 30 deja al autor.
2. RD 8.2 incorpora a la prosa una cláusula ("no se examinó cómo clasifica el filtro de fijaciones un contenido que se mueve") que viene de una afirmación marcada "requiere fuente" (pendiente 56).

Además, la nota de cabecera de RD dice "sin cambiar cifras, decisiones ni la numeración", pero la consolidación incluyó tres agregados de contenido pedidos por R8 (dos son correctos y están sustentados; el tercero es el punto 2). El script del editor no podía verlos: compara conjuntos de cifras, y dos de los tres agregados no traen cifras nuevas.

## 2. Método

1. **Diff.** Comparación línea a línea (difflib) de las tres parejas de archivos. CO: 0 líneas cambiadas. SP: 2 bloques (cabecera y 4.6.1). RD: 20 bloques. Cada bloque se leyó completo en las dos versiones.
2. **Script del editor.** Se ejecutó `ronda8/comprobar_consolidacion.py`: 0 cifras faltantes, 0 nuevas, 25 + 8 tablas bien formadas, 0 notas de trabajo perdidas. Se confirmó qué mide y qué no (no ve el contexto de la cifra, ni frases sin cifras, ni si el destino de una remisión contiene lo prometido).
3. **Lectura completa de RD actual** (líneas 5 a 831, unas 22.300 palabras), de corrido, y de CO completo. De SP se leyeron completas 4.3, 4.6.1 (bloque cambiado), 4.6.3, 4.6.4, 4.7 y 5.3, y los pasajes de 4.5.2, 4.6.5, 4.8.2 y 4.8.3 a los que llega alguna remisión.
4. **Fuentes primarias consultadas:** `resultados/ampliacion_41p_16-11-2026/por_categoria.csv` (tabla de RD 6.3, celda a celda); `documentacion/auditoria_final_23-11-2026/ronda6/registro.csv` (filas 37, 47, 48 y 110 a 113: fijaciones sobre 2.000 ms y prevalencias por posición); `resultados/explicativo_posicion_41p_18-11-2026/INFORME.md` (prevalencias); `resultados/enfoques_41p_22-11-2026/INFORME.md` (79 % de segmentos unánimes); R8 (origen de cada cambio); `ronda7/TERCERA_LECTURA_ESPECIALISTA.md` (marcas "requiere fuente").
5. **Remisiones.** Se extrajeron con expresión regular todas las "sección X.Y" de RD (164), SP (45) y CO (20), y las de MI, CI, EN y PE (83 coincidencias, incluidas las formas "RD 7.8" y "SP 4.7"). Se comprobó contra el texto del destino, una por una: las 20 de CO; las 23 de SP a RD y las internas de SP que llegan a secciones leídas; las 25 de RD a SP; y las 117 de RD que salen de una sección cambiada o llegan a ella. Las 47 restantes de RD van de una sección sin cambios a otra sin cambios; se leyeron en la lectura de corrido sin encontrar fallas, pero no se contrastaron una por una.
6. **Salvedades.** Lista armada desde la versión anterior de RD 8.4 (15), RD 8.8 (32 viñetas) y CO 9.5 (4 grupos), y cotejada con la versión actual.

## 3. Recuento

| Comprobación | Resultado |
|---|---|
| Bloques cambiados | RD 20, SP 2, CO 0 |
| Cifras faltantes o cambiadas de contexto | 0 |
| Celdas de la tabla de RD 6.3 contra `por_categoria.csv` | 16 de 16 correctas (14 conteos y 2 porcentajes: 6.423/22.176 = 29,0 %; 5.457/11.796 = 46,3 %; `blur` no tiene fila de activación, de modo que 0 es correcto; las sumas dan 22.176 y 11.796) |
| Cifras movidas de lugar | 3 grupos, los tres con remisión que funciona: 28 % y 4 % (de 8.8 a 6.1), 19 % a 27 % (de 8.8 a 7.9), definición de parpadeo (de 7.8 a SP 4.6.4) |
| Contenido agregado no declarado | 3 frases (RD 6.3, RD 8.2 dos veces) y 1 priorización (RD 8.4) |
| Remisiones en RD, SP y CO | 229; rotas por la consolidación: 0 |
| Remisiones con destino insuficiente (todas anteriores a la consolidación) | 4: PE fila 18, PE fila 19, CI línea 171, RD 8.8 (viñeta sin remisión) |
| Salvedades de RD 8.4 (15) | 15 presentes; 1 con priorización nueva; 1 con rótulo algo más duro |
| Salvedades de RD 8.8 (32 viñetas) | 32 presentes, con la misma fuerza (2 fusionadas en 1 y 1 partida en 2) |
| Salvedades de CO 9.5 | Sin cambios; sus 10 remisiones funcionan |
| Salvedades debilitadas | 1 menor (RD 8.5: se perdió "más simple") |
| Errores | 0 bloqueantes, 2 importantes, 15 menores (7 de ellos anteriores a la consolidación) |
| Reglas del proyecto | Vocabulario correcto; ninguna de las siete decisiones cerrada; ninguna aprobación afirmada; ningún "requiere fuente" literal en la prosa (ver error 2) |

## 4. Tabla de errores

| # | Archivo | Sección | Texto exacto actual | Problema y fuente | Texto exacto corregido | Gravedad |
|---|---|---|---|---|---|---|
| 1 | RD | 8.4 | `**Qué lo limita.** En orden de importancia:` | El texto anterior no ordenaba los límites por importancia (ronda8/pre_consolidacion, líneas 607 a 615: "dos límites de contenido", "El primero", "El segundo"). CO 9.1 pone primero el de la etiqueta ("Su límite está en la etiqueta"), que aquí queda tercero. PE, fila 30, deja la priorización de límites al autor. | `**Qué lo limita.**` | Importante |
| 2 | RD | 8.2 | `La cuarta es el desplazamiento de la página: no consta si los sitios web lo permitían, y no se examinó cómo clasifica el filtro de fijaciones un contenido que se mueve.` | La cláusula no estaba en la versión anterior. Viene de la afirmación que `ronda7/TERCERA_LECTURA_ESPECIALISTA.md` (línea 271) marca "[requiere fuente]" y que PE, fila 56, y la nota de trabajo siguiente (RD línea 577) mantienen fuera de la prosa. La frase solo dice que no se examinó, pero su razón de ser es la afirmación sin fuente. | `La cuarta es el desplazamiento de la página: no consta si los sitios web lo permitían.` | Importante |
| 3 | RD | Cabecera (línea 4) | `sin cambiar cifras, decisiones ni la numeración de las secciones;` | La consolidación agregó contenido que R8 pedía (sección 4, punto 5; tabla de errores, fila 4; caso 3): la frase sobre textos y diseños en 6.3 y la comparación de prevalencias en 8.2. No son errores (ver sección 5), pero la cabecera no los declara. El texto propuesto supone aplicado el error 2. | `sin cambiar cifras, decisiones ni la numeración de las secciones, salvo dos agregados que pedía esa verificación (en 6.3, que tampoco está descrito el contenido de los textos y los diseños; en 8.2, la prevalencia del primer segundo frente a los dos siguientes);` | Menor |
| 4 | RD | 8.4 | `1. *Ninguno de los dos contrastes es una confirmación.*` | Para el historial desplazado el texto anterior decía "no una segunda evidencia independiente"; "no es una confirmación" es algo más duro. La fórmula vigente en RD 6.5, 7.1 y 8.8 es "confirmación independiente". | `1. *Ninguno de los dos contrastes es una confirmación independiente.*` | Menor |
| 5 | RD | 8.4 | `- *Estímulo completo.* El resultado por estímulo` | El bloque se titula "Qué se observó", y esta viñeta es una lectura "sin contraste propio", como dice ella misma. | `- *Estímulo completo (lectura, no observación).* El resultado por estímulo` | Menor |
| 6 | RD | 8.4 | `(mediana +0,014; mejoran 23 de 41) (sección 7.1).` | Dos paréntesis seguidos. | `(mediana +0,014; mejoran 23 de 41; sección 7.1).` | Menor |
| 7 | RD | 8.5 | `Dos son anteriores a la fisiología.` | El texto anterior decía "hay una más simple que el diseño no descarta" y "una explicación equivalente del lado de la entrada". Se perdió "más simple", que indicaba qué explicación mirar primero. | `Dos son más simples y anteriores a la fisiología.` | Menor |
| 8 | RD | 8.5 | `puede reflejar poco la activación, porque no se validó contra ninguna medida externa` | El texto anterior daba los dos hechos sin nexo causal. "Porque" presenta la falta de validación como causa de que refleje poco. | `puede reflejar poco la activación: no se validó contra ninguna medida externa` | Menor |
| 9 | RD | 8.3.3 | `Las explicaciones candidatas son al menos seis: cinco fisiológicas (1 a 5) y una que no lo es (6).` | El texto anterior contaba "cuatro candidatos fisiológicos" y "las cuatro fuentes fisiológicas", y trataba los parpadeos aparte, como "una vía que no pasa por el movimiento de los ojos". Ahora los parpadeos cuentan como quinta explicación fisiológica, y la frase final ("las fuentes 1 a 4 covarían") los deja sin explicar. | `Las explicaciones candidatas son al menos seis: cuatro fuentes fisiológicas (1 a 4), una vía que no pasa por el movimiento de los ojos (5) y una que no es fisiológica (6).` | Menor |
| 10 | RD | 6.3 | `Sus categorías están en "Composición de los estímulos", al final de esta lista.` | "Sus" queda después de la frase sobre "página" y es ambiguo. El párrafo no está al final de la lista sino después de ella. | `Las categorías de los estímulos están en "Composición de los estímulos", después de esta lista.` | Menor |
| 11 | RD | 8.8 | `No describen el inicio de cada página ni los estímulos breves.` | Anterior a la consolidación. La frase inicial de 8.8 promete que cada limitación "remite a la sección donde están sus cifras"; es la única viñeta con cifra y sin remisión. El 53 % sale de 11.796 de 22.211 (RD 6.1). | `No describen el inicio de cada página ni los estímulos breves (sección 6.1).` | Menor |
| 12 | RD | 8.8 | `el conteo de SCR no se validó (sección 4.6.3)` | Anterior. "SCR" aparece una sola vez en RD y no se define allí. | `el conteo de respuestas de conductancia (SCR) no se validó (sección 4.6.3)` | Menor |
| 13 | RD | 8.8 | `el fold 0 se reproduce exacto en el equipo usado` | Anterior. "Fold" no se usa en ningún otro lugar de RD; el término definido en 6.3 es "grupo de la validación cruzada". | `el grupo 0 de la validación cruzada se reproduce exacto en el equipo usado` | Menor |
| 14 | RD | 8.4 | `los archivos del equipo de EEG traen tres canales de acelerómetro y la exportación del seguidor ocular, la posición del mouse, pero ninguno se usó` | Anterior. La elipsis del verbo hace tropezar: se lee "traen acelerómetro y la exportación". | `los archivos del equipo de EEG traen tres canales de acelerómetro y la exportación del seguidor ocular trae la posición del mouse, pero ninguno se usó` | Menor |
| 15 | PE | Fila 18 | `RD 7.8; SP 4.5.2;` | Anterior. SP 4.5.2 no menciona el montaje; lo documenta SP 4.7 ("No se asigna anatomía a los canales…"). Las referencias de las filas 18 y 19 están cruzadas. | `RD 7.8; SP 4.7;` | Menor |
| 16 | PE | Fila 19 | `MI, misma sección (agregado el 26-11); SP 4.7 \|` | Anterior. SP 4.7 no menciona la unidad física de la GSR; está en SP 4.5.2 (línea 91) y SP 4.6.3 (línea 128). | `MI, misma sección (agregado el 26-11); SP 4.5.2 y 4.6.3 \|` | Menor |
| 17 | CI | "Límites" (línea 171) | `(secciones 6.1, 6.2, 6.3, 6.4, 6.6, 7.1, 7.7, 7.9, 7.11, 8.3.3 y 8.4)` | Anterior. Dice que allí está "el detalle de cada uno de estos límites", pero tres no están en esas secciones: el patrón por grupo de personas y el cierre V3 inverso (RD 7.5), la pérdida de la red sin control propio y la escala (RD 7.10), y la corrección de Holm entre etapas (RD 8.8). | `(secciones 6.1, 6.2, 6.3, 6.4, 6.6, 7.1, 7.5, 7.7, 7.9, 7.10, 7.11, 8.3.3, 8.4 y 8.8)` | Menor |

## 5. Cifra en contexto: secciones reescritas

- **RD 6.1.** El párrafo se partió en tres. Los pesos (0,557; 0,520; 0,508; 0,398; −0,052) y la orientación de las variables no cambian. "Alta" sigue designando una mirada más quieta, sin validación y sin sentido establecido. Las tres frases sobre el sentido se fundieron en una con "de modo que"; no cambia lo afirmado. Las cifras de fijaciones (28 % sobre 2.000 ms, 4 % sobre 3.000 ms) llegaron desde 8.8 y describen lo mismo. El 28 % coincide con `registro.csv`, fila 37 (27,7 %).
- **RD 6.2.** El párrafo se partió en tres con dos rótulos nuevos. Limpieza: FastICA, 1 a 45 Hz, tantos componentes como canales utilizables, 1 s en torno a saturaciones, puntaje entre 1 y 15 Hz, tres componentes sin umbral, control fuera de los cuatro más oculares. Todo igual. Red: 1.217 parámetros, 16 canales y 2 s, una arquitectura sin búsqueda, escala por persona y canal, recorte a ±8. Todo igual. Se perdió "en adelante" delante de "señal cruda", sin consecuencia.
- **RD 6.3.** Tabla correcta en todas sus celdas. La frase "tampoco está descrito el contenido de los textos y los diseños" es nueva. Es cierta (RD 8.8 ya lo decía, y la nota de trabajo de 6.3 dice "Siguen sin describirse el contenido y la duración de los estímulos") y la pidió R8, sección 4, punto 5. 116 y 95 nombres, sin cambios.
- **RD 7.8.** Las amplitudes, las 31 de 37 personas y las cifras de sincronía no cambian. La definición de parpadeo salió de RD y quedó como remisión a SP 4.6.4, que la contiene completa (tramo de 50 a 500 ms con ambos ojos no válidos; incluye pérdidas de seguimiento; entre 19 y 393 por persona). SP 4.7 contiene las 16 posiciones.
- **RD 7.9.** La segunda objeción recibió sus cifras desde 8.8: 3 de 16 es 19 % y 3 de 11 es 27 %. Describe lo mismo que antes. Ya no remite a 8.8.
- **RD 8.2.** Las cuatro explicaciones son las mismas cuatro, ahora numeradas. Dos cosas nuevas: la comparación "más quieta que la de los dos siguientes (prevalencia 0,51 frente a 0,37–0,38; sección 7.2)", correcta (`registro.csv`, filas 110 a 112: 0,509; 0,374; 0,381) y pedida por R8, fila 4; y la cláusula del filtro de fijaciones (error 2). El 28 % sigue aquí y también en 6.1: no quedó "en un solo lugar", sin que eso sea un error.
- **RD 8.3.3.** Mismos contenidos. Cambió la cuenta (error 9).
- **RD 8.4.** Ver sección 7.
- **RD 8.5, párrafo inicial.** Las cuatro explicaciones son las mismas. Dos matices (errores 7 y 8).
- **RD 8.8.** 32 viñetas antes y después. Las dos del nivel tónico se fundieron; la de parpadeos y sentido de "alta" se partió en dos. Tres viñetas ganaron remisión (8.4, 7.1 y 7.3) y los tres destinos contienen la cifra: 0,50 a 0,59; 26 ventanas de P4; 2–3 % de los pares.
- **SP 4.6.1.** La frase "No constan…" quedó como lista de cuatro viñetas con los mismos elementos; "ni si esa mano usaba el mouse" se conserva.

## 6. Salvedades

**RD 8.4 (15 en la versión anterior; todas presentes).** (1) Los dos contrastes no tienen la misma solidez. (2) El protocolo del historial desplazado se fijó después de ver el +0,038: refinamiento dirigido, no segunda evidencia independiente. (3) La comparación por grupo es descriptiva y no registrada. (4) El soporte del filtro tónico: un cuarto del peso cae antes; no separa "previa predice" de "mismo momento". (5) El placebo es de otros estímulos; identificar la página; 79 % de segmentos unánimes; no se calculó dentro de un mismo estímulo. (6) El contraste principal es más frágil: +0,028 a +0,047 y no todos los intervalos excluyen el cero. (7) La fase 1 es una estimación más precisa, no una confirmación. (8) Efecto desigual: mediana +0,014; 23 de 41. (9) Configuración elegida con 25 personas; +0,055 frente a +0,001; sesgo posible y no demostrado; patrón inverso en el cierre V3; debilita el "respaldo". (10) Alcance: solo 6 s; 12 s inconcluso; desde 24 s no se distingue, sin demostrar ausencia. (11) Deriva lenta: el mismo minuto habla en contra como única explicación; control inconcluso; deriva por persona fuera del control. (12) Explicación no neural, sin control de artefactos ni análisis del movimiento. (13) Cuatro controles inconclusos; dentro de un mismo estímulo, poca potencia. (14) Estado del estímulo completo: lectura sin contraste propio. (15) Respuesta al cambio de estímulo; efecto pequeño y de baja utilidad práctica.

- Endurecida, levemente: la (2), por el rótulo del límite 1 (error 4).
- Con priorización nueva: todas las del bloque "Qué lo limita" (error 1).
- Debilitadas o perdidas: ninguna.

**RD 8.8 (32 viñetas; todas presentes, con la misma fuerza).** Dos dejaron sus cifras en otro lugar y remiten a él: fijaciones (6.1) y dimensiones de los componentes (7.9). Las dos remisiones funcionan.

**CO 9.5.** Sin cambios. Sus remisiones a 8.8, 9.1, 7.5, 6.4, 6.2, 7.1, 6.1 (dos), 6.3 y 7.9 y a SP 4.7 llegan a secciones que contienen lo dicho. Observación sin error: CO 9.5 habla de "cuatro grupos de límites" y RD 8.8 de "cinco familias"; no se contradicen, pero un lector puede notarlo.

**RD 8.5.** Una salvedad debilitada, menor (error 7).

## 7. RD 8.4 en su forma nueva

**¿Dicen los tres bloques lo mismo que el texto anterior?** Sí en contenido: cada frase del texto anterior tiene su lugar y no falta ninguna. No en dos puntos: "En orden de importancia" (error 1) y el rótulo del límite 1 (error 4).

**¿El orden o las transiciones priorizan algo nuevo?**

- Sí, de forma explícita: "En orden de importancia".
- De forma implícita: la lectura favorable ("con mayor probabilidad, una mejor estimación de un estado que dura segundos") pasó del final del texto, después de todas las reservas, al primer párrafo. No cambia lo que se afirma y hace la sección más clara, pero le da más peso que antes. Esa frase no está en CO 9.1, en CO 9.7 ni en la tabla de RD 8.1. No se propone como error: es una decisión del autor.
- "Por eso corresponde hablar de un resumen…" quedó atado solo al límite 5. En el texto anterior venía inmediatamente después de los controles inconclusos, así que es fiel.

**¿Queda claro para un lector nuevo qué se afirma?** Sí, mejor que antes. Tropiezos: hay dos listas numeradas con los mismos números que se citan entre sí ("límite 3", "lectura 1"), y las remisiones a las lecturas aparecen antes que la lista de lecturas.

**Lo que entiendo que afirma, en tres frases:**

1. Con historial, el modelo predice mejor el *Arousal Score*, y hay evidencia acotada, no una confirmación, de que la mejora no se explica solo por la persona: el historial del mismo estímulo sin las ventanas de 6 s de la etiqueta supera a un placebo de otros estímulos en +0,046, en los dos grupos de personas, mientras que el contraste principal es más frágil.
2. Lo más probable es que el historial dé una mejor estimación de un estado que dura segundos (un resumen del historial reciente, no dinámica dentro del estímulo); solo los 6 s previos tienen respaldo y el efecto es pequeño (AUC entre 0,50 y 0,59).
3. Esa mejora no se separó del soporte temporal de la etiqueta, de pertenecer a la misma página, de una respuesta al cambio de estímulo, de una deriva lenta ni de un artefacto no neural; los controles quedaron inconclusos, la configuración se eligió con parte de las personas evaluadas y ningún análisis se hizo en personas nuevas.

**Comparación.**

- Con CO 9.7: coincide (evidencia acotada, resumen del historial reciente, efecto pequeño, no separado del mismo estímulo ni del soporte de la etiqueta, controles inconclusos, contraste simple desigual).
- Con CO 9.1: coincide en cifras y límites. Difiere en el orden: CO 9.1 pone primero el límite de la etiqueta y el del placebo; RD 8.4 los declara tercero y cuarto "en importancia".
- Con la fila de activación de la tabla de RD 8.1: coincide ("Evidencia acotada", +0,046, p Holm 0,004, protocolo fijado después de ver el placebo; nota b con los mismos límites).
- Una diferencia anterior a la consolidación, que conviene que el autor mire: "evidencia acotada" tiene tres objetos distintos. En RD 8.1 responde a "¿la mejora proviene de la fisiología de las ventanas previas?"; en RD 8.4, a que "no se explica solo por la persona"; en CO 9.7, a que el historial "ayuda a predecir". La de 8.1 es la más fuerte, y el límite 4 de 8.4 dice que el contraste no separa la fisiología previa de pertenecer a la misma página.

## 8. Lectura de corrido de RD

**Frases rotas, párrafos duplicados, tablas.** No hay párrafos ni frases duplicadas (búsqueda automática de frases de más de 70 caracteres repetidas: ninguna). Las 25 tablas están bien formadas. Frases que tropiezan: errores 6, 10 y 14, y en RD 6.1, `0,518 con las 41) (análisis descriptivo no registrado)`, con dos paréntesis seguidos (anterior).

**Listas.** Las numeraciones son correctas (8.3.3: 1 a 6; 8.4: 1 a 6 y 1 a 5; 8.10: 1 a 7). En 8.3.3 las entradas 2 y 6 no cierran el rótulo en negrita con punto, como hacen las otras cuatro. En 8.4 el rótulo del límite 5 es una oración con dos puntos y los otros cinco son frases nominales. La tabla de 7.5 lleva una línea "Tabla: …" de título y ninguna otra tabla la lleva.

**Términos usados antes de definirse.**

- "Segmento": se usa en 6.2 ("desde el inicio del segmento"; "todas las ventanas del segmento") y se define en 6.3.
- "Fase 2", "curva temporal", "placebo de bloque", "prueba A1": se usan en 6.4 y 6.5; las etapas se presentan en 6.6.
- "Ventanas de contexto" y "contexto de 32" (6.3 y 7.5) nombran lo que el resto del texto llama historial (ya anotado en PE, fila 50).
- "SCR" y "fold" (errores 12 y 13).
- "Las notas", "las notas de diseño", "las láminas" (6.1, 6.2, 6.3): remiten a material que el lector de la tesis no tiene.

**Los diez lugares donde un lector se pierde, con arreglo que no quita ni agrega contenido.**

1. **8.4, dos listas con los mismos números.** Rotular las lecturas con letras (a a e) y citar "lectura a", o citar cada lectura por su nombre ("deja abierta la lectura de la relación entre señales del mismo momento").
2. **8.8, frase inicial: dos "cinco" seguidos** (cinco familias; cinco limitaciones). Escribir "Entre ellas, las que condicionan directamente las conclusiones del capítulo 9 son cinco:".
3. **6.4 y 7.1: "P1 y P2" son contrastes; "P4" y "P2 a P21" son personas** (7.1, 7.8, 8.8). Escribir "la persona P4" y "las personas P2 a P21, P36 y P37".
4. **6.2, lista de controles: cuatro placebos distintos** en tres viñetas. Ponerlos en una tabla (qué iguala, de dónde salen las ventanas, en qué análisis se usa), como ya pide PE, fila 69.
5. **6.4, párrafo "Dos aspectos de la regla registrada".** Nombra ocho filas de resultados que el lector no ha visto. Dejar en 6.4 la asimetría y la precedencia, y mover la enumeración de las ocho filas a continuación de la tabla de la curva en 7.2, con remisión.
6. **7.2, párrafo "AUC estratificada".** Una sola oración larga con siete estimaciones de tres análisis. Partir en tres oraciones: el contraste post hoc, la comprobación no registrada, y la fase 3.
7. **7.3, párrafos "El +0,047 de la curva…" y "Límites de la curva".** Poner la comparación entre el contraste del 16-11 y el del 22-11 en una tabla de dos columnas (historial, placebo, particiones, personas y filas).
8. **7.9, "Lectura".** La segunda objeción quedó como párrafo de una sola frase y "la contraria" obliga a volver atrás. Unir ese párrafo con el siguiente ("Con ambas a la vista…").
9. **8.1, párrafo "El paso del criterio a esa lectura".** Presentar las dos lecturas del criterio como dos viñetas ("al pie de la letra"; "más exigente") y dejar la frase de la decisión 5 después.
10. **6.1, párrafo "Por eso el soporte temporal real…".** Tres intervalos y cuatro porcentajes en prosa. Añadir el esquema del soporte que pide PE, fila 69, o partir el párrafo en dos: el soporte nominal, y el del filtro.

También: en 7.8 se habla de parpadeos desde la segunda frase y la remisión a su definición está al final del párrafo; conviene llevar la remisión a la primera mención.

## 9. Material candidato a anexos

Es una decisión del autor; no se propone borrar nada. El cuerpo de los capítulos 6 a 8 tiene hoy unas 18.700 palabras sin contar las notas de trabajo (1.850) ni las líneas de fuentes (190). Las cifras son palabras aproximadas del cuerpo.

| Material | Sección | Palabras |
|---|---|---:|
| Lista completa de limitaciones (dejando en el cuerpo las cinco de la frase inicial) | 8.8 | 1.340 |
| Estabilidad entre grupos de personas: tabla de hojas, tabla de nueve contrastes y pruebas de Welch | 7.5 | 520 |
| Términos y composición de los estímulos (o a metodología, capítulo 4) | 6.3 | 430 |
| Tabla de las doce etapas (ya existe ampliada en el Anexo de trazabilidad) | 6.6 | 410 |
| Montaje y sincronía entre equipos (o a metodología, capítulo 4) | 7.8 | 380 |
| Diferencias entre personas y adaptación a la persona | 7.11 | 365 |
| Decisiones abiertas (no es sección de la tesis) | 8.10 | 285 |
| Análisis descriptivos (evolución en la sesión, importancia, tipo de página) | 7.12 | 280 |
| Etiqueta corregida por posición: tabla A1 a A3 y diagnóstico de predicciones idénticas | 7.2 | 275 |
| Tabla de subconjuntos de variables del EEG y composición de "solo alfa y beta" | 7.7 | 265 |
| Tipos de fusión (completa; 8.6 conserva la conclusión) | 7.6 | 235 |
| Explicaciones no probadas de la dependencia ocular de la red y sus límites | 8.3.4 | 220 |
| Curva temporal de atención (tabla de cinco desfases) | 7.2 | 210 |
| Límites de la curva temporal de activación | 7.3 | 200 |
| Orden de las ventanas, GRU (completa; 8.1 y 8.6 conservan el resultado) | 7.4 | 195 |
| Límites de la inferencia (intervalo, dependencia, promedio de particiones) | 6.4 | 195 |
| Lecturas descriptivas y cierre V3 por partición | 7.1 | 180 |
| Precedencia de las reglas y las ocho filas | 6.4 | 160 |
| AUC estratificada de atención y "cuánto depende la etiqueta del reloj" | 7.2 | 260 |
| Cuatro límites de la red convolucional | 7.10 | 130 |
| Comparación entre el +0,047 de la curva y el +0,046 del historial desplazado | 7.3 | 125 |
| Fusión con HGB en el cierre V3 | 7.6 | 130 |
| Códigos de los contrastes | 6.4 | 120 |
| "Otros dos análisis" con una sola partición | 7.3 | 90 |
| Número de componentes quitados y regresión frontal | 7.9 | 65 |

La suma no es aditiva (7.6 aparece completa y en parte). Sin repetir, son unas 6.900 palabras: el cuerpo quedaría cerca de 11.800.

## 10. Reglas del proyecto

- **Vocabulario.** "Respaldo" aparece solo como rótulo de la regla registrada (tablas, "decisión de respaldo", "el 'respaldo' del contraste principal"). "Apoyo parcial" solo para la hipótesis (RD 8.1, 8.10; CO 9.1; SP 4.8.3). "Evidencia acotada" en RD 8.1, 8.4 y CO 9.7. "Cerca de un tercio" en RD 7.9, 8.3.2, 8.3.3, 8.10 y CO 9.3, 9.7 ("menos de un tercio" se refiere a los sitios web, otro dato). "*Modelo Profesor* con PCA" en RD 6.1, 8.10 y CO. "Activación" en todo el texto; "emoción" solo en el nombre de la decisión 3, en el título heredado de SP 4.5.2, en los rótulos `emotion` de los archivos y en una frase de literatura (RD 8.5, "regiones implicadas en la emoción"). **Observado** y **Atendido** en RD 6.1, 8.2, 8.3.3, 8.7; CO 9.3; SP 4.6.4.
- **Decisiones abiertas.** Ninguna de las siete quedó cerrada. "En orden de importancia" (error 1) no toca ninguna de las siete, pero sí el pendiente 30.
- **Aprobación del profesor guía.** No se afirma ninguna. Las tres cabeceras conservan "No hay aprobación registrada".
- **"Requiere fuente".** La expresión aparece solo en notas de trabajo. La cláusula del error 2 lleva a la prosa la consecuencia de una afirmación marcada así.
