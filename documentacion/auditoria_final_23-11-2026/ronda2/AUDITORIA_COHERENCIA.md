# Auditoría de coherencia (segunda pasada) — 26-11-2026

Alcance: comprobar que las correcciones pedidas por la auditoría del 23-11 (I1 a I6 y menores) quedaron aplicadas en todos los documentos y que estos son coherentes entre sí. Solo revisión: no se editó ningún archivo existente, no se entrenó nada y no se hicieron commits. Este informe es el único archivo creado.

Estado revisado: `main` en `af345a2` (igual a `origin/main`). Al empezar, el árbol de trabajo estaba limpio; a las 19:12 del 26-11 otro proceso había cambiado una línea de A (hallazgo A1), y este informe ya refleja ese cambio. Los demás textos citados se volvieron a comprobar por programa contra los archivos a esa hora. Las copias de `respaldo_local/` son idénticas a los documentos vivos del vault y de `notas/`.

## Qué se comprobó y cómo

- **Leídos completos:** los tres informes de la auditoría del 23-11; A (cierre), B (conclusiones), C (discusión fisiológica), D (minuta); `relato.py`, `GUIÓN.md`, `ENSAYO.md`, `LEEME.md`, `FUENTES.md`; los dos README; las dos notas.
- **Cifras:** cada número de A, B, C, D, de las 39 láminas y de `ENSAYO.md` contra los CSV de `resultados/<etapa>/` leídos con pandas (valor completo, redondeo a 3 decimales). Los valores de `redondeos_candidatos.csv` se buscaron en todos los documentos.
- **Presentación:** `GUIÓN.md`, `FUENTES.md` y el JSON de `index.html` se compararon por programa con lo que produce `relato.apply()`. Se abrieron siete gráficos (`final_principal`, `fusion_final`, `origen_mejora`, `activacion_temporal`, `limpieza_ocular`, `red_cruda`, `sesion_pagina`) y sus rótulos se contrastaron con los CSV. Los otros once gráficos no se volvieron a comprobar: los cubrió la auditoría de presentación del 23-11 y el generador no cambió.
- **Proceso:** `git log` por archivo en las 13 carpetas de resultados, los protocolos, la etiqueta `cierre-experimental-2026-11-23`, y los conteos de `comparaciones.csv`, `integridad.csv` y `coherencia_documentos.csv`.
- **No comprobado:** el aspecto visual de las láminas, el borrador largo de Resultados y Discusión (lo audita otro agente; solo se miró una cifra) y los artículos citados (se tomó `VERIFICACION_REFERENCIAS.md` como fuente).

## Resumen

- **2 bloqueantes**, **46 importantes**, **53 menores**.
- **Cifras:** todas las de A, B, C, D, láminas y ensayo coinciden con los CSV. No queda ningún redondeo doble (+0,017 y +0,044 están corregidos en todos lados).
- **El problema principal es un error nuevo, introducido al corregir:** B y `ENSAYO.md` dicen que el +0,046 del 16-11 se mantuvo "al repetirlo con cinco particiones" (+0,047). No es así. El +0,047 es la curva temporal del 22-11, que es otro análisis y corrió en **una sola partición** (la registrada el 16-11), con 40 personas. `scripts/reapertura_41p.py` usa `folds_main` en `run_lag` y `folds_rep` solo en `run_rep`; `lag_activacion.csv.gz` tiene cada fila una vez por estrategia.
- **A tiene una frase de proceso inexacta:** "se registró y publicó antes de correr y se ejecutó una vez" (lo de publicar no es verificable, y el cierre V3 tuvo una versión 1 abortada). La otra, "5 particiones; tres ya vistas el 16-11", la corrigió otro proceso durante esta auditoría.
- **Restos de lecturas objetadas:** quedan en A (dos celdas), B (una frase), D (una celda), cuatro láminas, y sobre todo en los dos README y en `notas/resumen-ultimo-mes-22-11-2026.md`, que no se tocaron tras la auditoría.
- **`ENSAYO.md` quedó atrasado respecto de `relato.py`** (19:08 frente a 19:21 del 23-11): lista como pendientes cinco detalles ya corregidos y usa el título antiguo de la lámina 19.
- **Decisiones abiertas:** A, B y la lámina 33 listan 5; D lista 7.
- **Nota para quien audita el borrador largo:** `Borrador Resultados y Discusión 23-11-2026.md`, línea 181, dice que el contraste del 22-11 (+0,047) usó "5 particiones". Es el mismo error.

Dos correcciones propuestas por `AUDITORIA_PRESENTACION.md` eran erróneas y, correctamente, **no se aplicaron**: rotular −0,003 y +0,007 en los gráficos de las láminas 23 y 19. Los CSV dan −0,002493 y +0,006462; los rótulos actuales (−0,002 y +0,006) son los correctos y los informes eran los que tenían el redondeo doble.

## Coherencia cruzada

### Número de decisiones abiertas

| Documento | Cuántas | Cuáles |
|---|---|---|
| A, "Queda abierto" | 5 | etiqueta de atención, margen, emociones, encuadre, cohorte |
| B, aviso inicial | 5 | las mismas, en otro orden |
| D, minuta | 7 (+ cuatro casillas de diseño) | las cinco, más normalización con la sesión completa y profesor PCA |
| Lámina 1, 2, 32 y 33 | 5 en pantalla | las cinco; la nota de la 33 menciona de palabra la sexta y la séptima |
| `ENSAYO.md` | 5 + sexta + séptima | igual que la lámina 33 |
| `resumen-ultimo-mes` | 5 pendientes distintos | lista anterior al 23-11 |

La sexta y la séptima no son menores en sus consecuencias: según D, no aceptarlas obliga a rehacer las etiquetas y todos los análisis, o a repetir todos los de atención. A y B deberían nombrarlas.

### La misma cantidad en cada documento

| Cantidad | A | B | C | D | Láminas | ¿Coherente? |
|---|---|---|---|---|---|---|
| Activación, historial sin 6 s − placebo, 16-11: +0,046 [+0,018; +0,073] | sí | sí | +0,046 | — | 23 | Sí |
| Activación, curva 6 s, 22-11: +0,047 [+0,017; +0,078] | sí | **como "repetición con cinco particiones"** | — | sí | 29, 30 | **No (B, ensayo, pie de la 29)** |
| ¿Queda dicho que son dos análisis? | cada cifra en su fila | **no** | usa solo +0,046 | usa solo +0,047 | **no** | Parcial |
| Activación P1: +0,036 [+0,010; +0,065], respaldo | sí | sí | — | — | 18, 29, 30 | Sí |
| Activación con posición: +0,032 [+0,004; +0,059], inconcluso | sí | +0,032 | — | — | 23, 30 | Sí |
| Activación, mismo estímulo: +0,009, inconcluso | sí | **omitido** | — | — | — | No (B) |
| E1 corregida: 0,675 frente a 0,683, "inferior" | "baja poco… inferior, al filo" | — | — | **"casi no cambia"** | 33: "baja poco", sin rótulo | **No (D, 33, ensayo)** |
| Fusión en activación | **"Sin diferencias"** | "ninguna se distinguió" | — | — | 19 y 29: **"sin diferencias"** | No (lectura de nulo) |
| Fusión tardía en atención | fila general acotada a MLP; **fila de etapa sin acotar** | acotada | — | — | acotada | No (A, una celda) |
| EEG atención: 0,681 → 0,621, +0,060 [+0,044; +0,075] | sí | sí | sí | sí | 25, 29, 31 | Sí |
| Red: +0,035 [+0,023; +0,047]; +0,028 con EEG limpio | sí | sí | sí | 0,023 | 26, 31 | Sí |
| Red en activación: 0,498 frente a 0,524, inconcluso | sí | sí | sí | — | 26 y 31: sin "inconcluso" | Parcial |
| Desfase EEG–seguidor ocular: 0,18 a 0,53 s | sí | sí | sí | — | 24 | Sí (`resumen`: 0,25–0,5) |

## A. `documentacion/Cierre_Experimental_Final_23-11-2026.md`

| # | Ubicación | Texto exacto actual | Problema | Corrección exacta propuesta | Gravedad |
|---|---|---|---|---|---|
| A1 | Reapertura, fila fase 1 | `Fase 1, registrada (5 particiones nuevas; el contraste ya se había visto en otras tres el 16-11)` | **Corregido por otro proceso mientras corría esta auditoría** (26-11, cambio sin confirmar en el árbol de trabajo). En `af345a2` decía `(5 particiones; tres ya vistas el 16-11)`, que era inexacto: las cinco particiones (1101 a 1105) son nuevas. Al texto nuevo le falta la partición registrada: el 16-11 se habían visto cuatro particiones, no tres. | `Fase 1, registrada (5 particiones nuevas; el contraste ya se había visto el 16-11 en la partición registrada y en otras tres)` | menor |
| A2 | Reapertura, fila curva | `\| Fase 1, curva temporal \|` | No dice que la curva corrió en una sola partición y con 40 personas. De ahí salió el error de B. | `\| Fase 1, curva temporal (una partición, la registrada el 16-11; 40 personas en activación) \|` | importante |
| A3 | 16 al 18-11, fila ampliación | `Fusión tardía mejor en atención \|` | Resto de I5: sin acotar a redes MLP ni decir que es secundario. | `Fusión tardía sobre temprana en atención solo entre redes MLP (+0,012, secundario sin corrección) \|` | importante |
| A4 | Tabla general, fila fusión | `el signo es el contrario \| Sin diferencias \|` | Nulo leído como equivalencia: tardía − temprana en activación es +0,006 [−0,032; +0,042], inconcluso. | `el signo es el contrario \| Sin diferencias demostradas (inconcluso: +0,006 [−0,032; +0,042]) \|` | importante |
| A5 | Trazabilidad, primera frase | `Cada etapa confirmatoria se registró y publicó antes de correr y se ejecutó una vez.` | (a) "Publicó" no es verificable desde el repositorio (M8). (b) La versión 1 del cierre V3 se abortó en el primer fold y dejó `oof_activacion.csv.gz` en `cierre_v3_16-11-2026_abortado_fusion`. (c) La enmienda E1 se corrió dos días después del registro. (d) La fase 2 se registró con la fase 1 en marcha. | `Cada etapa con protocolo entró a Git antes que sus predicciones (orden de commits verificado; que se publicara antes de correr no es verificable desde el repositorio) y se ejecutó una vez. Salvedades: la versión 1 del cierre V3 se detuvo en el primer fold de entrenamiento por una auditoría de código y se conserva en \`cierre_v3_16-11-2026_abortado_fusion\`; la enmienda E1 se registró el 16-11 y se corrió el 18-11; la fase 2 se registró con la fase 1 en marcha y es post hoc.` | importante |
| A6 | Queda abierto, decisiones | `5. Si se planifica una cohorte nueva para confirmar activación.` | A lista 5 decisiones y la minuta 7. | `5. Si se planifica una cohorte nueva para confirmar activación.`<br>`6. Si se aceptan las etiquetas normalizadas con la sesión completa de cada persona (el manuscrito pide normalizar solo con entrenamiento).`<br>`7. Si el profesor PCA queda como definición del *Attention Score* (la nota de diseño proponía la fusión igualitaria como principal).`<br><br>`Las opciones de cada una están en la minuta del 23-11 (\`Avances/Avance - 23-11-2026 (Minuta de decisiones con el profesor).md\`).` | importante |
| A7 | Queda abierto, trabajo de cierre | `1. Integrar los resultados del 22 y 23-11 al borrador de Resultados y Discusión del 18-11 (\`Escritura/Borrador Discusión fisiológica 23-11-2026.md\` ya cubre la parte fisiológica).`<br>`2. Escribir Conclusiones, que depende de las decisiones anteriores.`<br>`3. Confirmar en el texto completo las 18 referencias de \`notas/sustento-fisiologico-23-11-2026.md\`.` | Los tres puntos están atrasados: el borrador integrado existe (`Borrador Resultados y Discusión 23-11-2026.md`, que reemplaza al del 18-11), el de Conclusiones también, y 10 de las 18 referencias ya se leyeron. | `1. Revisar el borrador integrado \`Escritura/Borrador Resultados y Discusión 23-11-2026.md\` (reemplaza al del 18-11) y pasarlo a LaTeX.`<br>`2. Ajustar \`Escritura/Borrador Conclusiones 23-11-2026.md\` según las decisiones anteriores.`<br>`3. Leer en texto completo las 8 referencias contrastadas solo por resumen (Barry 2005 y 2007, Boucsein 2012, Critchley 2002, Croft y Barry 2000, Iwasaki 2005, Keren 2010 y Yuval-Greenberg 2008); detalle en \`documentacion/auditoria_final_23-11-2026/VERIFICACION_REFERENCIAS.md\`.` | importante |
| A8 | Auditoría final, menores | `lo más probable es que el modelo no use la columna de posición; no se puede descartar un error sin reentrenar, y la cifra no cambia.` | Atrasado: el diagnóstico del 26-11 lo resolvió. | `un diagnóstico del 26-11 (\`documentacion/auditoria_final_23-11-2026/ronda2/DIAGNOSTICO_E1_POSICION.md\`) mostró que el modelo recibe la columna de posición y no la usa en ninguna división; no es un error y la cifra no cambia.` | importante |
| A9 | Trazabilidad, fila montaje | `\| Montaje \| \`montaje_ocular_41p_23-11-2026\` \| descriptivo \| — \| \`441bae9\` \| — \|` | Los CSV del montaje entraron en `06547f5`; `441bae9` es el informe. | `\| Montaje \| \`montaje_ocular_41p_23-11-2026\` \| descriptivo \| — \| \`06547f5\` (CSV), \`441bae9\` (informe) \| — \|` | menor |
| A10 | Cuatro enfoques, E4 | `es estable (fiabilidad 0,76 y 0,66)` | M11: es fiabilidad por mitades dentro de una sola sesión. | `es estable dentro de la sesión (fiabilidad por mitades 0,76 y 0,66)` | menor |
| A11 | Encabezado, etiqueta | `Etiqueta de Git: \`cierre-experimental-2026-11-23\` (anterior a la auditoría final; el texto vigente es el de \`main\`).` | Correcto. Falta el commit: la etiqueta apunta a `aee6ab6` (15:14), donde este documento todavía dice "sobre todo la conducta ocular" y "su ventaja también es ocular". | Agregar: `Apunta a \`aee6ab6\`; la versión auditada es \`af345a2\` o posterior.` Opción: crear una etiqueta nueva (por ejemplo `cierre-experimental-2026-11-23-auditado`) sin mover la anterior. | menor |
| A12 | Auditoría final, lista | `No verificable sin reentrenar. Que las predicciones provengan de la configuración declarada` | El diagnóstico del 26-11 lo comprobó para un fold de E1. | Agregar: `(comprobado para un fold del enfoque E1 el 26-11)` | menor |

## B. `Escritura/Borrador Conclusiones 23-11-2026.md`

| # | Ubicación | Texto exacto actual | Problema | Corrección exacta propuesta | Gravedad |
|---|---|---|---|---|---|
| B1 | 9.1, segundo párrafo | `Al repetirlo con cinco particiones el resultado se mantiene (+0,047 [+0,017; +0,078]).` | Falso. El +0,047 es la curva temporal: otro historial (banda de 6 s, sin importar el estímulo), otro placebo, **una sola partición** y 40 personas. Presenta como repetición lo que la auditoría del 23-11 ya había separado como contrastes distintos. | `Un análisis distinto del 22-11, la curva temporal, da un valor parecido para la banda de los 6 s anteriores (+0,047 [+0,017; +0,078]; una partición, 40 personas); no es una repetición del mismo contraste.` | **bloqueante** |
| B2 | 9.1, tercer párrafo | `Los controles por tiempo de sesión y por posición dentro del estímulo conservan el signo y el tamaño (+0,026 y +0,032), pero quedan inconclusos.` | Omite el tercer control, donde el tamaño no se conserva: dentro de un mismo estímulo, +0,009 [−0,020; +0,037]. A sí lo trae. | `Los controles por tiempo de sesión y por posición en el estímulo conservan el signo y un tamaño parecido (+0,026 y +0,032), pero quedan inconclusos; al comparar solo ventanas de un mismo estímulo la diferencia baja a +0,009 [−0,020; +0,037], también inconclusa.` | importante |
| B3 | 9.2, primer párrafo | `En activación ninguna estrategia se distinguió de las demás. La fusión no es el factor que explica el desempeño.` | La segunda frase es la que I5 objetó: no se sigue de ningún contraste. | `En activación ninguna estrategia se distinguió de las demás, con intervalos anchos (inconcluso). Estos contrastes no permiten elegir una fusión ni atribuirle el desempeño.` | importante |
| B4 | Aviso de decisiones abiertas | `(5) que la cohorte nueva queda como trabajo futuro. Si alguna cambia, hay que revisar las secciones 9.1 y 9.6.` | Lista 5; la minuta, 7. El texto también supone las otras dos. | `(5) que la cohorte nueva queda como trabajo futuro; (6) que se aceptan las etiquetas normalizadas con la sesión completa, declaradas como límite; (7) que el profesor PCA define el *Attention Score*. Las siete están en [[Avance - 23-11-2026 (Minuta de decisiones con el profesor)]]. Si alguna cambia, hay que revisar las secciones 9.1, 9.5 y 9.6.` | importante |
| B5 | 9.3, primer párrafo | `un control que retira 72 % de la varianza no ocular la deja en 0,674` | M10 sin aplicar: el control retira componentes no oculares que suman el 72 % de la varianza total. | `un control que retira tres componentes no oculares, que suman 72 % de la varianza, la deja en 0,674` | menor |
| B6 | 9.4 | `La detección de atención mejora a lo largo de la sesión (de 0,65 a 0,71).` | Son las AUC del modelo sin historial (0,653 y 0,713). La lámina 20 muestra el modelo con historial (0,69 a 0,74). | `La detección de atención mejora a lo largo de la sesión (de 0,65 a 0,71 entre el primer y el último quinto con el modelo sin historial; de 0,69 a 0,74 con historial).` | menor |
| B7 | 9.5 | (lista de limitaciones) | M12 a medias: falta decir que los secundarios no llevan corrección y que el explicativo de posición y la fase 2 son post hoc. | Agregar: `- Los contrastes secundarios no llevan corrección por multiplicidad; el explicativo de posición y la fase 2 de la reapertura son post hoc.` | menor |
| B8 | 9.3, último párrafo | `El desempeño más alto en activación se obtuvo al adaptar el modelo a cada persona (+0,045 [+0,023; +0,069]) y al predecir por estímulo (0,587)` | Mezcla una diferencia con una AUC. | `Las mayores mejoras en activación se obtuvieron al adaptar el modelo a cada persona (+0,045 [+0,023; +0,069] sobre el modelo con historial) y al predecir por estímulo (AUC 0,587)` | menor |

## C. `Escritura/Borrador Discusión fisiológica 23-11-2026.md`

| # | Ubicación | Texto exacto actual | Problema | Corrección exacta propuesta | Gravedad |
|---|---|---|---|---|---|
| C1 | 8.y, "Tipo de relación" | `La relación documentada entre el EEG y la conductancia de la piel es tónica: en reposo, un mayor nivel de conductancia se asocia con menor potencia alfa global (Barry et al., 2005, 2007).` | Corrección 7 de `VERIFICACION_REFERENCIAS.md` aplicada a medias: se cambió la frase siguiente, pero sigue "la relación documentada", como si fuera toda la literatura. Barry 2005 no informa una correlación. | `La relación entre el EEG y la conductancia de la piel que documentan estos trabajos es tónica: en reposo, un mayor nivel de conductancia acompaña a una menor potencia alfa global (Barry et al., 2005, 2007).` | importante |
| C2 | Pie de las referencias | `Años por confirmar: OpenAlex registra Iwasaki et al. con 2004, Keren et al. con 2009 y Dimigen con 2019 (fecha en línea). Los autores de Boucsein et al. (2012) figuran en el catálogo solo como comité de la Society for Psychophysiological Research.` | Contradice el encabezado, que dice que las referencias ya se contrastaron. Los años están confirmados. | `Años confirmados en Crossref el 23-11-2026: Iwasaki et al. 2005, Keren et al. 2010 y Dimigen 2020 corresponden al volumen impreso.` | menor |
| C3 | Referencias | `- Boucsein, W., et al. (2012). Publication recommendations for electrodermal measurements.` | Tras las correcciones, Boucsein ya no se cita en el cuerpo: referencia huérfana. | Quitar la entrada, o restituir la cita cuando se lea el PDF. Si se conserva, autores completos: `Boucsein, W., Fowles, D. C., Grimnes, S., Ben-Shakhar, G., Roth, W. T., Dawson, M. E., y Filion, D. L. (2012).` | menor |
| C4 | 8.x.2, segundo párrafo | `el dipolo córneo-retinal se concentra en frecuencias bajas, pero el potencial` | La corrección propuesta traía la cita; se omitió. | `el dipolo córneo-retinal se concentra en frecuencias bajas (Plöchl, Ossandón y König, 2012), pero el potencial` | menor |
| C5 | 8.x.4, primera frase | `que aprende directamente de la señal cruda (del tipo EEGNet; Lawhern et al., 2018)` | Corrección 9 sin aplicar: EEGNet trabaja sobre señal filtrada y remuestreada, y la red de la tesis también recibe señal filtrada. | `que aprende directamente de la serie temporal del EEG, sin variables calculadas a mano (del tipo EEGNet; Lawhern et al., 2018)` | menor |
| C6 | 8.z, sincronía | `El desfase no se corrigió y atenúa cualquier relación entre el EEG y las demás señales.` | Afirma un efecto que no se midió. | `El desfase no se corrigió y puede atenuar la relación entre el EEG y las demás señales; ese efecto no se midió.` | menor |
| C7 | 8.x.2, primer párrafo | `El límite inferior es 0,044 (0,044497 en el CSV); el INFORME muestra 0,045 por un redondeo doble.` | Es una nota de trabajo dentro de la prosa de la tesis. | Mover a una nota al pie del borrador o quitarla. | menor |
| C8 | Encabezado | `10 en texto completo y 8 solo por resumen` | Correcto. Matiz no dicho: tres de las diez se leyeron en preprint o manuscrito de autor (Dimigen 2020, Dimigen 2011, Lawhern 2018), y la lectura fue por búsqueda dirigida. | Agregar: `(tres de ellas en preprint o manuscrito de autor; lectura por búsqueda dirigida de los pasajes)` | menor |

## D. `Avances/Avance - 23-11-2026 (Minuta de decisiones con el profesor).md`

| # | Ubicación | Texto exacto actual | Problema | Corrección exacta propuesta | Gravedad |
|---|---|---|---|---|---|
| D1 | Decisión 4, opción B | `la detección casi no cambia (0,675 frente a 0,683)` | Resto de M3: la decisión registrada fue "inferior" (−0,008 [−0,015; −0,001]). A dice "baja poco… inferior, al filo". | `la detección baja poco (0,675 frente a 0,683; −0,008 [−0,015; −0,001], decisión registrada "inferior", al filo)` | importante |
| D2 | Decisión 1, opción B | `72, 101 o 767 personas según la varianza usada, cada estimación externa basada en 8 personas` | Ambiguo: 72 y 101 salen de 8 personas cada una; 767 sale de las 25 de entrenamiento mezclando folds. | `72, 101 o 767 personas según la varianza usada (las dos primeras, estimadas con 8 personas cada una; la tercera, con las 25 de entrenamiento mezclando folds)` | menor |
| D3 | Material de apoyo | `- [[Borrador Conclusiones 23-11-2026]] · [[Borrador Discusión fisiológica 23-11-2026]].` | Faltan el borrador integrado y la auditoría. | `- [[Borrador Resultados y Discusión 23-11-2026]] · [[Borrador Conclusiones 23-11-2026]] · [[Borrador Discusión fisiológica 23-11-2026]].`<br>`- Auditoría final: \`repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/\`.` | menor |

Las demás cifras de D coinciden: +0,047 [+0,017; +0,078], 0,681, 0,621, 0,023, 0,598, 0,504, 9,4 % (1 − 0,906), 66 % y kappa 0,33 (66,28 % y 0,3255).

## E. Presentación (`presentaciones/avances_tesis_06-11-2026/`)

### `relato.py`

| # | Lámina | Texto exacto actual | Problema | Corrección exacta propuesta | Gravedad |
|---|---|---|---|---|---|
| E1 | 29, pie | `Filas 1 y 2: repetición del 22-11 (el 16-11 dio +0,026 y +0,034).` | El +0,047 de la fila 2 no viene de la repetición con 5 particiones: es la curva, en una partición y con 40 personas. | `Fila 1 y el +0,001: 5 particiones, 22-11 (el 16-11 dio +0,026 y +0,034). El +0,047: curva del 22-11, una partición, 40 personas.` | importante |
| E2 | 33, pregunta 4 | `y la detección baja poco: 0,675 frente a 0,683.` | Sin el rótulo de decisión que usa A. | `y la detección baja poco: 0,675 frente a 0,683 (decisión registrada: "inferior").` | importante |
| E3 | 27, tabla | `'Compatible con que alfa y beta también caigan al limpiar'` | La espiga sacádica abarca unos 20 a 90 Hz: llega a beta alta, no a alfa (Keren, por resumen; Hipp y Siegel solo sobre 30 Hz). C ya se corrigió; la lámina no. | `'Llega a beta alta (20 a 90 Hz); no explica por sí sola la caída en alfa'` | importante |
| E4 | 28, tabla | `'La relación conocida entre EEG y GSR es tónica, entre condiciones o personas'` | "Conocida" generaliza y "entre personas" no se pudo comprobar. | `'La relación que documenta Barry es tónica, al comparar condiciones'` | importante |
| E5 | 28, pie | `Boucsein et al. (2012); Critchley (2002); Benedek y Kaernbach (2010); Barry et al. (2007); Mathôt (2018).` | Nada de la lámina se apoya ya en Boucsein (sus dos atribuciones quedaron sin comprobar), y la fila de Barry usa también el trabajo de 2005. | `Critchley (2002); Benedek y Kaernbach (2010); Barry et al. (2005, 2007); Mathôt (2018).` | importante |
| E6 | 29, tabla | `['Fusión','Tardía mejor con MLP (+0,012)','Sin diferencias']` | Nulo leído como equivalencia (ver A4). | `['Fusión','Tardía mejor con MLP (+0,012)','Sin diferencias demostradas']` | importante |
| E7 | 19, nota | `En activación no hay diferencias.` | Igual que E6. | `En activación no se demostraron diferencias (inconcluso).` | importante |
| E8 | 31, punto 2 | `En activación queda en 0,498.` | No dice que la comparación con el modelo de referencia es inconclusa. | `En activación queda en 0,498, frente a 0,524 del modelo de referencia: inconcluso.` | menor |
| E9 | 26, nota | `En activación queda en el azar.` | Igual que E8. | `En activación queda en el azar (0,498 frente a 0,524; comparación inconclusa).` | menor |
| E10 | 27, nota | `Lo que detecto es en buena parte lo observado` | Más fuerte que lo medido ("al menos un tercio"). | `Lo que detecto es, al menos en un tercio, lo observado` | menor |
| E11 | 30, punto 2 | `A 12 s es inconclusa (+0,024)` | Concordancia. | `A 12 s es inconcluso (+0,024)` | menor |
| E12 | 30, nota | `El efecto se sostiene frente al placebo, pero es pequeño` | Ninguna lámina dice que +0,046 (lámina 23) y +0,047 (láminas 29 y 30) son análisis distintos. | Agregar a la nota: `El +0,047 es de la curva del 22-11 (una partición, 40 personas); el +0,046 de la lámina 23 es el contraste registrado el 16-11.` | menor |
| E13 | 32, columna "Cierre" | `Integrar los resultados del 22 y 23-11 al borrador y ajustar las conclusiones según lo que se decida.` | El borrador integrado ya existe. | `Revisar el borrador integrado del 23-11 y ajustar las conclusiones según lo que se decida.` | menor |
| E14 | 32, fuentes | `'../../notas/resumen-ultimo-mes-22-11-2026.md; '+LIM+'; '+RED` | Cita como fuente una nota que conserva lecturas objetadas ("confirmada", "6 a 12 s"). | `'documentacion/Cierre_Experimental_Final_23-11-2026.md; '+LIM+'; '+RED` | menor |
| E15 | 33, fuentes | `../../notas/pautas-escritura-recuperadas.md','closing-questions')` | La nota remite a la minuta, que no está entre las fuentes. | Agregar `; ../../documentos/01 Tesis MDS/Avances/Avance - 23-11-2026 (Minuta de decisiones con el profesor).md` | menor |
| E16 | 34, 35, 37, 38 (anexos A, B, D, E) | pies actuales, por ejemplo `Test, 8 personas. Curva promedio de las curvas por persona.` | Hallazgo 24 del 23-11 sin aplicar: son análisis del diseño anterior (8 personas de test; 29-10, 02-11 y 06-11) y no lo dicen. | Agregar al pie de cada uno: `Análisis anterior al de 41 personas; se conserva como antecedente.` | menor |
| E17 | 2, nota | `Son nueve partes.` | Hallazgo 20 sin aplicar: la barra lateral muestra diez secciones ("El problema con la etiqueta de activación" va aparte). | Usar el capítulo `'LAS ETIQUETAS'` en las láminas 13 a 17 (variable `D4`). | menor |
| E18 | 23, título | `En activación, los segundos previos sí aportan` | La salvedad (inconcluso al controlar la posición) solo está en el pie. | `En activación, los segundos previos aportan frente al placebo` | menor |
| E19 | 20, nota | `En activación, la proporción de ventanas altas cae al final, compatible con habituación.` | El gráfico muestra otra cosa en activación (la AUC sube a 0,64 en el último quinto, con 34 personas) y la nota no lo comenta. | Agregar: `La línea gris es la AUC de activación por quinto; es descriptiva y con 34 a 41 personas por punto.` | menor |
| E20 | 27 y 31 frente a B, C y ensayo | `lo observado` / `lo atendido` | Minúscula en láminas; **Observado** y **Atendido** con mayúscula en B, C y `ENSAYO.md`. | Elegir una forma. La regla del vault los escribe con mayúscula. | menor |
| E21 | 7 y 4 | `Saavedra (grupo, web)`; `No hay expresión facial en este set` | Hallazgo 35 a medias. | `Saavedra (2024, grupo, web)`; `en este conjunto de datos` | menor |

### `ENSAYO.md`

No se regenera: se escribió a las 19:08 del 23-11 y `relato.py` cambió a las 19:21.

| # | Ubicación | Texto exacto actual | Problema | Corrección exacta propuesta | Gravedad |
|---|---|---|---|---|---|
| N1 | Pregunta 13 | `y por +0,047 [+0,017; +0,078] al repetirlo con cinco particiones.` | El mismo error de B1, en una respuesta que se dirá al profesor. | `y un análisis distinto del 22-11, la curva temporal, da +0,047 [+0,017; +0,078] para la banda de 6 s (una partición, 40 personas).` | **bloqueante** |
| N2 | Tablas de 20 y de 10 minutos (dos veces) | `\| 19 \| En atención, la fusión tardía rinde mejor con el mismo modelo (MLP) \|` | Título antiguo. | `\| 19 \| En atención, la fusión tardía rinde mejor entre redes MLP; con HGB, no \|` | importante |
| N3 | "Antes de ensayar" | `Quedan cinco detalles menores; están en la última sección y el guion hablado de abajo ya los esquiva.` y los cinco puntos numerados que siguen | Los cinco ya están corregidos en `relato.py`: el pie de la 39 dice "10 en texto completo y 8 solo por resumen"; en la 30, "mejoran 23 de 41" va junto al +0,036; la 33 dice "baja poco"; el título de la 19 cambió; la nota de la 11 dice "cada análisis principal". | Reemplazar la frase y los cinco puntos por: `No queda ninguna diferencia conocida entre este ensayo y \`relato.py\` (revisado el 26-11-2026).` | importante |
| N4 | Última sección | La tabla "Láminas donde la nota, el contenido o los informes no calzan" (cinco filas) y la frase `Lo que sigue son detalles menores que siguen vigentes; ninguno se corrigió aquí, porque este ensayo no toca \`relato.py\`.` | Igual que N3: las cinco filas describen texto que ya no existe. | Quitar la tabla y reemplazar la frase por: `Los cinco detalles que quedaban se corrigieron después en \`relato.py\`.` | importante |
| N5 | Guion, lámina 33 | `y la detección casi no cambia, 0,675 frente a 0,683.` | La lámina ya no dice "casi no cambia". | `y la detección baja poco, 0,675 frente a 0,683; la decisión registrada para esa prueba fue "inferior".` | importante |
| N6 | Guion, aviso tras la lámina 33 | `> Ojo con la cuarta: si preguntan por el "casi no cambia", la diferencia es −0,008 [−0,015; −0,001] y la decisión registrada para esa prueba fue "inferior".` | Remite a un texto que ya no está. | `> Ojo con la cuarta: la diferencia es −0,008 [−0,015; −0,001], con p de Holm 0,055; "inferior", al filo.` | menor |
| N7 | Tabla de anexos, fila 39 | `Ojo: su pie dice que falta confirmarlas en el texto completo; lo vigente es 10 de 18 con texto completo y 8 solo con el resumen` | El pie ya está corregido. | `Su pie dice 10 en texto completo y 8 solo por resumen, y dos atribuciones sin comprobar (Boucsein, Critchley)` | menor |
| N8 | Guion, lámina 19 | `En activación no hay diferencias.` | Ver E7. | `En activación no se demostraron diferencias.` | menor |
| N9 | Guion, lámina 32 | `integrar los resultados del 22 y 23 de noviembre al borrador y ajustar las conclusiones según lo que decidamos` | Ver E13. | `revisar el borrador integrado del 23 de noviembre y ajustar las conclusiones según lo que decidamos` | menor |
| N10 | Pregunta 10 | `Eso corre las ventanas de EEG entre un 12 % y un 25 % respecto de las de mirada` | Corresponde al rango 0,25–0,5 s del informe de limpieza. Con 0,18 a 0,53 s sobre ventanas de 2 s es entre 9 % y 27 %. | `Eso corre las ventanas de EEG entre un 9 % y un 27 % respecto de las de mirada` | menor |
| N11 | Pregunta 2 | `Las razones probables son que la GSR es lenta y de origen profundo` | "Origen profundo" es la atribución a Critchley que no se pudo comprobar. | `Las razones probables son que la GSR es lenta, quizá con un origen que el EEG de superficie ve poco (eso no lo pude confirmar en la fuente)` | menor |
| N12 | Pregunta 4 | `cada etapa se registró en Git antes de correr, se ejecutó una vez, usa Holm dentro de su familia y tuvo auditoría independiente` | Las cuatro etapas del 16 al 18-11 (final, robustez, ampliación, explicativo) no tuvieron auditoría propia; las cubrió la auditoría final. | `cada etapa se registró en Git antes de sus predicciones, se ejecutó una vez y usa Holm dentro de su familia; desde el 22-11 cada una tuvo auditoría independiente, y la auditoría final del 23-11 recalculó las doce` | menor |
| N13 | Primer párrafo y última sección | `que cambiaron las láminas 1, 26, 27, 28, 29, 30, 31 y 33` frente a `en las láminas 1, 26, 27, 29, 30, 31 y 33` | Las dos listas no coinciden (falta la 28 en la segunda). | Usar la primera lista en ambos lugares. | menor |

El resto de `ENSAYO.md` corresponde a `relato.py`: los otros 32 títulos de las tablas, el orden, las cinco decisiones en el orden de la lámina 33 y todas las cifras del guion y de las 22 preguntas (comprobadas contra los CSV, incluidas +0,055 y +0,001 [−0,052; +0,055] por grupo, +0,028 [+0,006; +0,050] sin la persona más influyente, 30 de 40 y mediana +0,042, 1.217 parámetros, p de Holm 0,055, 0,055 y 0,049).

### `GUIÓN.md`, `FUENTES.md`, `LEEME.md` y gráficos

| # | Archivo | Texto exacto actual | Problema | Corrección exacta propuesta | Gravedad |
|---|---|---|---|---|---|
| G1 | `LEEME.md` (se genera en `crear_presentacion.py`) | `regenera el HTML, gráficos y guion.` | No avisa que `ENSAYO.md` no se regenera; por eso quedó atrasado. | `regenera el HTML, gráficos y guion. ENSAYO.md no se regenera: hay que revisarlo a mano después de cada cambio en relato.py.` | menor |
| G2 | `FUENTES.md` (ídem) | `Los resultados antiguos son antecedentes, no resultados V2.` | Frase de la versión de noviembre temprano; hoy las fuentes son sobre todo las de 41 personas. | `Los resultados anteriores al 16-11-2026 son antecedentes.` | menor |

`GUIÓN.md`, `FUENTES.md` y el contenido de `index.html` son idénticos a lo que genera `relato.py` hoy. `LEEME.md` dice 39 diapositivas (33 + 6): correcto. Las 41 rutas de `FUENTES.md` existen. Los rótulos de los siete gráficos abiertos coinciden con sus CSV.

## F. README y notas

### `repos/Tesis_MDS/README.md`

| # | Ubicación | Texto exacto actual | Problema | Corrección exacta propuesta | Gravedad |
|---|---|---|---|---|---|
| F1 | Párrafo de la red | `así que la ventaja está ligada a la señal ocular. En activación` | Resto de I1. | `así que su detección depende de la señal ocular; su ventaja sobre el HGB se mantiene con el EEG limpio (+0,028 frente a +0,035). En activación` | importante |
| F2 | Párrafo de montaje y limpieza | `y la parte defendible como no ocular queda en 0,55–0,56.` | Resto de I2: da por ocular todo lo demás. | `: al menos un tercio de la detección sobre el azar es ocular (0,060 de 0,181, cota inferior), y del resto no se puede afirmar origen cerebral ni ocular.` | importante |
| F3 | Párrafo del cierre | `Etiqueta de Git \`cierre-experimental-2026-11-23\`.` | No dice que la etiqueta es anterior a la auditoría. En ese commit el cierre conserva las lecturas objetadas. | `Etiqueta de Git \`cierre-experimental-2026-11-23\` (apunta a \`aee6ab6\`, anterior a la auditoría final; el texto vigente es el de \`main\` desde \`af345a2\`).` | importante |
| F4 | Párrafo de los cuatro enfoques | `Es lo más reciente.` | Contradice los párrafos del 23-11 que tiene encima. | `Es anterior a los análisis del 23-11 de arriba.` | importante |
| F5 | Reapertura | `que es el estado más reciente de los resultados.` | Igual que F4. | `que cierra la reapertura del 22-11.` | importante |
| F6 | Experimentación cerrada — 22-11 | `Evidencia mixta con apoyo parcial: información temporal real en activación;` | Resto de I3, sin aviso de que ese cierre está reemplazado. | `Documento reemplazado por el cierre del 23-11. Decía: evidencia mixta con apoyo parcial, información temporal en activación (lectura moderada después);` | menor |
| F7 | Encabezado y título de sección | `Estado experimental actualizado al 24-10-2026.` y `## Cuatro enfoques nuevos — 22-11-2026` | La fecha de estado es de octubre; el título del 22-11 encabeza párrafos del 23-11; la auditoría final quedó al final del archivo. | `Estado experimental actualizado al 23-11-2026 (cierre consolidado y auditoría final).` y `## Cierre consolidado y análisis del 22 y 23-11-2026`; subir a esa sección el párrafo "Auditoría final (23-11-2026)". | menor |

### `tesis-mds/README.md`

| # | Ubicación | Texto exacto actual | Problema | Corrección exacta propuesta | Gravedad |
|---|---|---|---|---|---|
| F8 | Párrafo de la red | `así que la ventaja está ligada a la señal ocular. En activación` | Igual que F1. | La de F1. | importante |
| F9 | Párrafo de montaje y limpieza | `y la parte defendible como no ocular queda en 0,55–0,56.` | Igual que F2. | La de F2. | importante |
| F10 | Párrafo del cierre | `Etiqueta de Git \`cierre-experimental-2026-11-23\`.` | Igual que F3. Además, este README no menciona la auditoría final. | La de F3, seguida de: `**Auditoría final (23-11-2026):** un agente independiente recalculó las 12 etapas; cifras reproducidas, sin hallazgos bloqueantes y seis lecturas moderadas. Informes en \`repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/\`.` | importante |
| F11 | Reapertura | `Activación: efecto del historial confirmado (+0,036, respaldo) y de corto alcance (6–12 s). Atención: sin información temporal a ningún desfase.` | Restos de I3 y de I4. | `Activación: el contraste principal pasa a respaldo al promediar 5 particiones (+0,036 [+0,010; +0,065]); no es una confirmación. Solo la banda de 6 s tiene respaldo (+0,047 [+0,017; +0,078]); desde 12 s es inconcluso. Atención: nulo concluyente a 6 y 12 s.` | importante |
| F12 | Cuatro enfoques | `**Cuatro enfoques nuevos del 22-11-2026 (lo más reciente):**` | Contradice los párrafos del 23-11. | `**Cuatro enfoques nuevos del 22-11-2026:**` | importante |
| F13 | Cierre del 22-11 | `(información temporal real en activación; en atención la mejora se explica por el tiempo transcurrido en el estímulo)` | Resto de I3 en la descripción de un documento reemplazado. | `(reemplazado por el cierre del 23-11)` | menor |
| F14 | Para continuar y Versiones | `Bitácora reciente, hasta el 01-11-2026`; `el README del código (actualizado al 24-10)`; `El repositorio local está en \`main\`, commit \`8ace73d\` […] No se hicieron commits, push ni cambios a esos experimentos.` | Estado del 01-11. Hoy `main` está en `af345a2`, publicado, y la bitácora llega al 23-11. | `Bitácora reciente, hasta el 23-11-2026`; quitar el paréntesis; reemplazar el párrafo por `El repositorio local está en \`main\`, commit \`af345a2\`, igual a \`origin/main\` (26-11-2026).` | menor |

### `notas/resumen-ultimo-mes-22-11-2026.md`

No se tocó tras la auditoría (última modificación 14:35 del 23-11) y lo citan la lámina 32 y `ENSAYO.md`.

| # | Ubicación | Texto exacto actual | Problema | Corrección exacta propuesta | Gravedad |
|---|---|---|---|---|---|
| F15 | Antes de "## En una mirada" | (no hay aviso) | La nota conserva casi todas las lecturas que la auditoría objetó. | Insertar: `> **Aviso (26-11-2026).** Esta síntesis es anterior a la auditoría final del 23-11, que reprodujo las cifras y pidió moderar varias lecturas. La referencia vigente es \`repos/Tesis_MDS/documentacion/Cierre_Experimental_Final_23-11-2026.md\`.` | importante |
| F16 | Tabla, fila 22 nov | `Activación confirmada y de corto alcance; atención sin información temporal; la detección por EEG tiene firma ocular` | I3. | `Activación con respaldo, solo para los 6 s anteriores; atención sin información temporal demostrable; parte de la detección por EEG es ocular` | importante |
| F17 | 22 de noviembre, fase 1 | `La información está en los 6 a 12 s anteriores y desaparece desde 24 s.` | I4. | `Solo la banda de 6 s tiene respaldo (+0,047 [+0,017; +0,078]); a 12 s es inconcluso y desde 24 s no se distingue del placebo, sin demostrar ausencia.` | importante |
| F18 | Fase 3 | `dentro de un mismo estímulo manda el tiempo transcurrido.` | I4: se apoya en un contraste inconcluso. | `dentro de un mismo estímulo agrega +0,009, también inconcluso.` | importante |
| F19 | E1 | `y conserva la detección (0,675 frente a 0,683).` | M3. | `y la detección baja poco (0,675 frente a 0,683; decisión registrada "inferior", al filo).` | importante |
| F20 | E2 | `La mayor parte tiene firma de movimiento ocular` | I2. | `Una parte tiene firma de movimiento ocular` | importante |
| F21 | Dónde queda, hipótesis | `de forma local (6 a 12 s)` | I4. | `con respaldo solo para los 6 s anteriores` | importante |
| F22 | Dónde queda, atención | `pero en su mayor parte coincide con artefactos oculares; la parte más defendible como no ocular ronda 0,59–0,60.` | I2, y cifra anterior a la limpieza. | `pero al menos un tercio de lo que tiene sobre el azar es ocular (0,060 de 0,181, cota inferior); del resto no se puede afirmar origen cerebral ni ocular.` | importante |
| F23 | Dónde queda, método | `Desde el 16-11 todo análisis se registra y publica antes de correr, se ejecuta una vez y pasa por auditoría independiente.` | Las etapas del 16 al 18-11 no tuvieron auditoría propia de resultados; "publica" no es verificable. | `Desde el 16-11 todo análisis con protocolo se registra en Git antes de sus predicciones y se ejecuta una vez; desde el 22-11 cada etapa pasa además por auditoría independiente.` | importante |
| F24 | Actualización del 23-11, red | `cae a 0,649: la ventaja está ligada a la señal ocular.` | I1. | `cae a 0,649: su detección depende de lo ocular, pero su ventaja sobre el HGB se mantiene con el EEG limpio (+0,028).` | importante |
| F25 | Actualización del 23-11, limpieza | `La parte defendible como no ocular queda en 0,55–0,56.` | I2. | `El modelo limpio sigue sobre el azar en las 41 personas; el diseño no separa si ese resto es ocular o cerebral.` | importante |
| F26 | 15 al 18 de noviembre | `Fusión tardía mejor en atención (+0,012).` | I5. | `Fusión tardía sobre temprana en atención entre redes MLP (+0,012, secundario); con HGB el signo es el contrario.` | importante |
| F27 | Actualización del 23-11, montaje | `El EEG va 0,25–0,5 s desfasado respecto del seguidor ocular.` | Los demás documentos usan 0,18 a 0,53 s (mínimo y máximo de `personas.csv`). | `El EEG va entre 0,18 y 0,53 s atrasado respecto del seguidor ocular.` | menor |
| F28 | E4 y Dónde queda, activación | `la detectabilidad es un rasgo estable`; `Se comporta como un estado del estímulo completo.` | M11. | `la detectabilidad es estable dentro de la sesión (fiabilidad por mitades)`; `El modelo por estímulo rinde más (0,587), sin superar de forma demostrable al promedio por ventana.` | menor |
| F29 | Pendiente | (lista de cinco) | Lista anterior al 23-11; no coincide con las decisiones de A ni de D. | Agregar al final: `Lista superada: las decisiones vigentes son las siete de la minuta del 23-11.` | menor |

### `notas/sustento-fisiologico-23-11-2026.md`

El aviso inicial declara que la nota conserva el texto original y nombra las tres atribuciones con problemas. Por eso las frases sobre Boucsein, Critchley y Hipp y Siegel se anotan como menores.

| # | Ubicación | Texto exacto actual | Problema | Corrección exacta propuesta | Gravedad |
|---|---|---|---|---|---|
| F30 | Sección 4, tiempos | `y es coherente con que el historial de 6 a 12 s sí ayudara en activación.` | I4. Es una lectura de resultados, no una cita, y el aviso inicial no la cubre. | `y es coherente con que el historial de los 6 s previos sí ayudara en activación (a 12 s el resultado es inconcluso).` | importante |
| F31 | Segundo párrafo | `**No se leyeron los textos completos**: lo que se atribuye a cada trabajo` | Contradice el aviso de tres líneas más arriba (10 leídas en texto completo). | `**Al escribir esta síntesis no se habían leído los textos completos** (después se leyeron 10; ver la verificación de arriba): lo que se atribuye a cada trabajo` | menor |
| F32 | Sección 1, espiga sacádica | `*Relación con los datos:* explica que la detección por alfa y beta también cayera al limpiar (0,593 a 0,547)` | No respaldado: la espiga llega a beta alta, no a alfa. | `*Relación con los datos:* es compatible con parte de la caída en beta al limpiar; no explica la de alfa (ver verificación)` | menor |
| F33 | Título de la sección 4 | `## 4. Por qué la activación no se detecta desde el EEG` | Afirma como causa una interpretación; la lámina 28 ya lo moderó. | `## 4. Por qué puede costar detectar la activación desde el EEG` | menor |
| F34 | Nota final sobre años | `aquí se usa el año del volumen, que hay que confirmar.` | Ya están confirmados. | `aquí se usa el año del volumen, confirmado en Crossref el 23-11-2026.` | menor |

## Afirmaciones sobre el proceso, contra Git y contra la auditoría

| Afirmación | Dónde | Resultado |
|---|---|---|
| 2.638 valores comparados, sin discrepancias | A, `ENSAYO.md`, bitácora | Correcto: `comparaciones.csv` tiene 2.638 filas, todas "coincide" (1.290 difieren solo por la semilla de remuestreo). |
| 288 de 289 hashes | A, `ENSAYO.md` | Correcto: 196 + 82 + 3 + 8 = 289; la única diferencia es `scripts/limpieza_ocular_41p.py`. |
| Sin hallazgos bloqueantes; seis importantes | A, README del repositorio, `ENSAYO.md` | Correcto para la auditoría del experimento. La de presentación sí tuvo uno (lámina 10, filtro de 1 a 45 Hz), ya corregido. |
| Protocolo antes que predicciones | A | Verificado en Git para las 12 carpetas con protocolo. |
| "Registró y publicó antes de correr y se ejecutó una vez" | A, `resumen` | Inexacto (A5, F23). |
| "5 particiones; tres ya vistas el 16-11" | A (en `af345a2`) | Inexacto; corregido en el árbol de trabajo el 26-11 (A1). |
| "Registrado antes de correr" para el +0,046 | A, B, C, lámina 23, `ENSAYO.md` | Correcto para el registro (`8beb675`, 16-11 14:25). La corrida es del 18-11; A lo dice. |
| "Registrado antes de correr y auditado" para la limpieza | lámina 25 | Correcto (`06547f5`, enmienda `441bae9`, resultados y auditoría `afe7e98`). |
| "La experimentación está cerrada y auditada" | lámina 33 | Correcto. |
| Auditoría de código antes de ver resultados desde la reapertura | A | Lo dicen los informes de las cinco etapas; no es verificable desde Git, como ya anotó la auditoría del 23-11. |
| Etiqueta `cierre-experimental-2026-11-23` | A, los dos README, bitácora | Apunta a `aee6ab6` (23-11, 15:14), dos commits de contenido antes de `af345a2`. A y la bitácora lo dicen; los README no (F3, F10). |
| "Los `INFORME.md` no se modificaron" | A | Correcto respecto de la auditoría: ni `7b46b67` ni `af345a2` tocan un `INFORME.md`. |

## Reglas del proyecto

- **Aprobación del profesor guía:** ningún documento la afirma. A, B, D, `ENSAYO.md` y `resumen` dicen que no hay aprobación registrada. La única mención positiva es la de las etiquetas GSR V2 ("Mario comunicó el 01-11 que el profesor aprobó"), que coincide con la bitácora del 01-11.
- **"Emociones":** no se usa por activación en ningún documento; aparece solo en la cita de la hipótesis y como decisión abierta.
- **Términos:** Modelo Profesor, Modelo Estudiante, Attention Score y Arousal Score están en su forma acordada en todos. Observado y Atendido se distinguen siempre; solo varía la mayúscula (E20).

## Revisado sin hallazgos

- **A:** todas las cifras e intervalos de las siete tablas (82 valores), incluidos +0,017 y +0,044; la tabla de trazabilidad salvo la fila del montaje (11 de 12 filas coinciden con Git); la sección de reproducibilidad; los seis hallazgos resumidos; los límites.
- **B:** todas las cifras (40 valores); 9.3 (I1 e I2 aplicados), 9.5, 9.6 y 9.7; el aviso de que nada es una confirmación independiente.
- **C:** todas las cifras (0,207; 0,004; 150 y 20 µV; 31 de 37; 0,060 [0,044; 0,075]; 39 de 41; 3,5 % y 72 %; 0,593 y 0,547; 0,28 y 0,08; 0,716, 0,681, 0,649; 32 de 41; 0,48 y 0,41; 0,524, 0,518, 0,498; +0,007 [−0,005; +0,020]); las correcciones 1 (salvo una cita, C4), 2 a 6, 8 y 10 de `VERIFICACION_REFERENCIAS.md`, aplicadas; 8.x.3 y 8.x.4; las limitaciones.
- **D:** las siete decisiones y la tabla de secciones afectadas; todas las cifras; los cuatro enlaces a notas del vault existen.
- **Presentación:** `GUIÓN.md`, `FUENTES.md` y `index.html` frente a `relato.py`; 39 láminas (33 + 6); las 41 rutas de fuentes; láminas 1, 3, 5, 6, 8 a 18, 21, 22, 24, 25 y 39 sin hallazgos nuevos; los siete gráficos abiertos; el hallazgo bloqueante del 23-11 (lámina 10) y los importantes 2 a 13, aplicados (el 9, salvo lo anotado en E4 y E5).
- **Etiqueta `cierre-experimental-2026-11-22`:** apunta a `749b35e`; el cierre del 22-11 está marcado como reemplazado y el borrador del 18-11 también.
- **Respaldo:** las copias de `respaldo_local/` de B, C, D, las dos notas y el README son idénticas a los originales.
