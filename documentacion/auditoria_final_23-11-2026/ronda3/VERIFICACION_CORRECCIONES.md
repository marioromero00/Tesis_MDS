# Verificación de las correcciones del commit `aef0f32` — ronda 3 (26-11-2026)

Objeto: `git diff af345a2 aef0f32`. Hecha por un agente independiente. No se editó ningún archivo existente, no se entrenó ningún modelo y no se hicieron commits. Este informe es el único archivo creado (la carpeta `ronda3/` ya existía, con una subcarpeta `comprobaciones/` de otro proceso, que no se tocó).

## 1. Resumen

- **Cambios revisados:** unos 240 pasajes modificados en 15 archivos fuente (README del repositorio y del espacio de trabajo, cierre, cuatro borradores, minuta, tres notas, `relato.py`, `crear_presentacion.py`, `ENSAYO.md`), más los generados (`GUIÓN.md`, `FUENTES.md`, `LEEME.md`, `index.html`, 30 SVG). De ellos, unas 95 cifras nuevas o cambiadas y unos 40 hechos de proceso o de método.
- **Cifras:** todas las cifras nuevas o cambiadas coinciden con su CSV redondeando desde el valor completo, salvo una (`ENSAYO.md`, 27 %). Las 17 correcciones de redondeo doble del borrador de Resultados están bien.
- **Hechos de proceso y de método:** todos los comprobados coinciden con la fuente primaria (lista en la sección 4).
- **Errores encontrados: 13** (4 importantes, 9 menores). Ninguno bloqueante. Solo uno es una cifra mal escrita; los demás son correcciones aplicadas en un documento y no en los otros que dicen lo mismo, o frases de estado que quedaron atrasadas.
- **Correcciones bloqueantes e importantes de los tres informes:** todas quedaron aplicadas en el archivo al que iban dirigidas; el texto antiguo ya no aparece. Cuatro no se propagaron a otros documentos (sección 3).
- **Presentación:** `GUIÓN.md`, `FUENTES.md`, `LEEME.md` e `index.html` son idénticos byte a byte a lo que genera `relato.py` (regenerado en una copia temporal fuera del repositorio). Los SVG difieren solo en identificadores internos y fecha. 39 láminas (33 + 6 anexos); nueve partes en el índice y nueve capítulos de contenido. Los 72 títulos de las dos tablas de `ENSAYO.md` y los 33 del guion hablado coinciden con `relato.py`.

## 2. Errores encontrados

Las rutas son relativas a `/Users/mario/Proyectos/tesis-mds/`. Los documentos del vault y las notas se citan en su ubicación original, no en `respaldo_local/`.

| N.º | Archivo | Texto exacto actual | Por qué está mal (fuente) | Texto exacto corregido | Gravedad |
|---|---|---|---|---|---|
| 1 | `repos/Tesis_MDS/presentaciones/avances_tesis_06-11-2026/ENSAYO.md`, pregunta 10 | `Eso corre las ventanas de EEG entre un 9 % y un 27 % respecto de las de mirada, pupila y GSR.` | `resultados/montaje_ocular_41p_23-11-2026/personas.csv`, `lag_parpadeo_s`: mínimo 0,184 y máximo 0,528 s; sobre 2 s es 9,2 % y 26,4 %. El 27 % sale de redondear primero a 0,53 s (lo propuso así la auditoría de coherencia, N10). Contradice al borrador de Resultados (7.6) y al de Secciones pendientes (4.6.1), que dicen 26 % | `Eso corre las ventanas de EEG entre un 9 % y un 26 % respecto de las de mirada, pupila y GSR.` | importante |
| 2a | `repos/Tesis_MDS/documentacion/Cierre_Experimental_Final_23-11-2026.md`, límites | `- En activación las AUC absolutas son bajas (0,52 a 0,59).` | El borrador de Resultados se corrigió a `0,50 a 0,59` (8.4 y 8.8) y los demás documentos no. Fuentes: `red_cruda_41p_23-11-2026/descriptivos.csv` (red 0,498), `enfoques_41p_22-11-2026/e4_descriptivos.csv` (modelo general 0,502), `reapertura_fase2_41p_22-11-2026/descriptivos.csv` (0,501); máximo 0,587. La misma cantidad queda con dos valores | `- En activación las AUC absolutas son bajas (0,50 a 0,59).` | importante |
| 2b | `documentos/01 Tesis MDS/Escritura/Borrador Conclusiones 23-11-2026.md`, 9.5 | `- En activación las AUC son bajas (0,52 a 0,59), por lo que` | Igual que 2a | `- En activación las AUC son bajas (0,50 a 0,59), por lo que` | importante |
| 2c | `repos/Tesis_MDS/presentaciones/avances_tesis_06-11-2026/relato.py`, lámina 30 (y `GUIÓN.md`/`index.html` al regenerar) | `AUC bajas: 0,52 a 0,59.` | Igual que 2a | `AUC bajas: 0,50 a 0,59.` | importante |
| 2d | `.../ENSAYO.md`, guion de la lámina 30 | `Las AUC son bajas, de 0,52 a 0,59.` | Igual que 2a | `Las AUC son bajas, de 0,50 a 0,59.` | importante |
| 3 | `documentos/01 Tesis MDS/Escritura/Borrador Discusión fisiológica 23-11-2026.md`, 8.y "Tipo de relación" | `y la navegación web produce un rango de activación estrecho.` | Afirmación sin dato: ningún CSV ni INFORME mide el rango de activación (hallazgo I-11). Se corrigió en el borrador de Resultados (8.5), que dice resumir este documento, y aquí no. Los dos textos se contradicen | `y es plausible que la navegación web produzca un rango de activación estrecho; este trabajo no lo midió.` | importante |
| 4 | `documentos/01 Tesis MDS/Escritura/Borrador Resultados y Discusión 23-11-2026.md`, 8.5 "Tipo de relación" | `La relación documentada entre el EEG y la conductancia de la piel es tónica: en reposo, mayor conductancia se asocia con menor potencia alfa global (Barry et al., 2005, 2007).` | Hallazgo C1 (importante) aplicado solo en la Discusión fisiológica. `VERIFICACION_REFERENCIAS.md`, ref. 1: Barry 2005 es una manipulación con cafeína, no una correlación; "la relación documentada" generaliza a toda la literatura | `La relación entre el EEG y la conductancia de la piel que documentan estos trabajos es tónica: en reposo, mayor conductancia acompaña a una menor potencia alfa global (Barry et al., 2005, 2007).` | importante |
| 5 | `.../ENSAYO.md`, última sección | `(dice que solo hay respaldo para los 6 s anteriores) y usa el intervalo [+0,017; +0,078];` | Este commit cambió la lámina 30: ahora muestra `+0,046 [+0,018; +0,073], registrado antes` y ya no trae ese intervalo (`relato.py`, lámina 30). El propio ensayo lo dice más arriba ("la 30 usa el +0,046") | `(dice que solo hay respaldo para los 6 s anteriores) y desde el 26-11 muestra el contraste registrado, +0,046 [+0,018; +0,073];` | menor |
| 6 | `.../relato.py`, nota de la lámina 30 | `El +0,047 es de la curva del 22-11 (una partición, 40 personas); el +0,046 de la lámina 23 es el contraste registrado el 16-11.` | La nota se agregó pensando en una lámina 30 con +0,047. El mismo commit puso +0,046 en la lámina 30; el +0,047 quedó solo en la 29. La nota habla de una cifra que la lámina no muestra | `El +0,046 de esta lámina y de la 23 es el contraste registrado el 16-11; el +0,047 de la lámina 29 es de la curva del 22-11 (una partición, 40 personas).` | menor |
| 7a | `.../Borrador Resultados y Discusión 23-11-2026.md`, 7.6 | `atenúa cualquier relación entre el EEG y las demás señales, incluidas las etiquetas.` | El efecto no se midió (hallazgo C6). La Discusión fisiológica se corrigió a "puede atenuar […]; ese efecto no se midió" y `ENSAYO.md` dice "no lo medí"; aquí sigue como hecho | `puede atenuar la relación entre el EEG y las demás señales, incluidas las etiquetas; ese efecto no se midió.` | menor |
| 7b | `.../Borrador Resultados y Discusión 23-11-2026.md`, 8.9 "Sincronía entre equipos" | `no se corrigió y atenúa cualquier relación entre el EEG y las demás señales.` | Igual que 7a | `no se corrigió y puede atenuar la relación entre el EEG y las demás señales; ese efecto no se midió.` | menor |
| 7c | `documentos/01 Tesis MDS/Escritura/Borrador Secciones pendientes 23-11-2026.md`, 4.6.1 | `no invalida los resultados, pero atenúa cualquier relación entre el EEG y el resto, incluidas las etiquetas.` | Igual que 7a | `no invalida los resultados, pero puede atenuar la relación entre el EEG y el resto, incluidas las etiquetas; ese efecto no se midió.` | menor |
| 8a | `.../Cierre_Experimental_Final_23-11-2026.md`, tabla general, fila GRU, columna de activación | `\| Indicio secundario, sin corrección \|` | El borrador de Resultados (8.1) se corrigió por el hallazgo I-7: GRU con historial menos GRU de una ventana mide el historial, no el orden; el contraste propio del orden es inconcluso (`cierre_final_41p_16-11-2026/contrastes.csv`: `gru_c32 − hgb_c32` +0,020 [−0,017; +0,057]). El cierre conserva la lectura objetada | `\| No demostrado: GRU − HGB, ambos con historial, +0,020 [−0,017; +0,057], inconcluso. La GRU con historial supera a su control de una ventana (+0,051, secundario sin corrección), lo que mide el historial y no el orden \|` | menor |
| 8b | `.../relato.py`, lámina 29, fila GRU | `'Señal secundaria'` | Igual que 8a | `'No demostrado'` | menor |
| 8c | `.../Cierre_Experimental_Final_23-11-2026.md`, tabla general | `\| ¿Queda algo al controlar la posición? \| Nada \|` | Es un nulo concluyente dentro de ±0,02, no un cero (hallazgo m-1, aplicado solo en Resultados 8.1) | `\| ¿Queda algo al controlar la posición? \| No: nulo concluyente dentro de ±0,02 \|` | menor |
| 9 | `.../Cierre_Experimental_Final_23-11-2026.md`, "Menores" | `mostró que el modelo recibe la columna de posición y no la usa en ninguna división; no es un error y la cifra no cambia.` | `ronda2/DIAGNOSTICO_E1_POSICION.md`: se reajustó un solo fold (partición 1101, fold 0; 1.800 divisiones). La frase lo generaliza a todo el análisis. El borrador de Resultados sí lo acota ("reajustó un solo grupo de una partición") | `mostró, al reajustar un fold (partición 1101, fold 0), que el modelo recibe la columna de posición y no la usa en ninguna de sus 1.800 divisiones; no es un error y la cifra no cambia.` | menor |
| 10 | `README.md` (espacio de trabajo), "Versiones" | ``El repositorio local está en `main`, commit `af345a2`, igual a `origin/main` (26-11-2026).`` | Falso desde el mismo commit que lo introdujo: `git log -1` da `aef0f32` (26-11-2026, 19:21) | ``El repositorio local está en `main`, igual a `origin/main` al 26-11-2026; el commit vigente se consulta con `git log -1` (`aef0f32` o posterior).`` | menor |
| 11 | `.../ENSAYO.md`, última sección | `las láminas 2, 4, 7, 13 a 17, 19, 20, 23, 26 a 35, 37 y 38` | `git diff af345a2 aef0f32 -- relato.py` no toca la lámina 2 (el cambio de capítulo afecta a las láminas 13 a 17) | `las láminas 4, 7, 13 a 17, 19, 20, 23, 26 a 35, 37 y 38` | menor |
| 12a | `.../ENSAYO.md`, guion de la lámina 33 | `Hay un sexto punto, menor: las etiquetas se normalizan` | El commit quitó "menor" en "Lo que no se puede decir" (la auditoría de coherencia señaló que la sexta decisión no es menor: no aceptarla obliga a rehacer etiquetas y análisis) y lo dejó en otros tres lugares | `Hay un sexto punto: las etiquetas se normalizan` | menor |
| 12b | `.../ENSAYO.md`, pregunta sobre la normalización | `sino el sexto punto, menor, que digo de palabra en esa lámina.` | Igual que 12a | `sino el sexto punto, que digo de palabra en esa lámina.` | menor |
| 12c | `.../relato.py`, nota de la lámina 33 | `Hay un sexto punto, menor: las etiquetas se normalizan` | Igual que 12a | `Hay un sexto punto: las etiquetas se normalizan` | menor |
| 13 | `.../Borrador Resultados y Discusión 23-11-2026.md`, 6.3 | `las excepciones (la heterogeneidad por grupo del 16-11, las sensibilidades a personas individuales y la comprobación estratificada del 22-11) se rotulan como no registradas donde aparecen.` | La lista omite una excepción que el mismo commit rotuló en 7.7: el aporte del historial en el modelo adaptado (+0,058), que no figura en la lista `descriptive` de `enfoques_41p_22-11-2026/protocolo.json` | `las excepciones (la heterogeneidad por grupo del 16-11, las sensibilidades a personas individuales, la comprobación estratificada del 22-11 y el aporte del historial en el modelo adaptado de la sección 7.7) se rotulan como no registradas donde aparecen.` | menor |

Los errores 2c, 6, 8b y 12c están en `relato.py`: después de corregirlos hay que regenerar la presentación y revisar `ENSAYO.md` a mano.

## 3. Correcciones pedidas que no quedaron aplicadas o quedaron a medias

Bloqueantes (B1 y N1 de coherencia): aplicadas. El texto "al repetirlo con cinco particiones" ya no existe en ningún documento con ese sentido.

Importantes aplicadas en su archivo pero no en los demás que repiten la frase:

1. **I-11 de Resultados** ("rango de activación estrecho"): falta en la Discusión fisiológica (error 3).
2. **C1 de coherencia** ("la relación documentada"): falta en el borrador de Resultados, 8.5 (error 4).
3. **I-7 de Resultados** (orden frente a historial en la GRU): falta en el cierre y en la lámina 29 (errores 8a y 8b).
4. **I-9 de Resultados** (heterogeneidad por grupo): aplicada sin la última parte del texto propuesto, "con intervalos que la auditoría final reproduce con diferencias de hasta 0,0013". `ENSAYO.md` sí lo dice.

Menores no aplicadas o a medias:

- **m-9 de Resultados** (0,50 a 0,59): solo en el borrador de Resultados (errores 2a a 2d).
- **C6 de coherencia** ("puede atenuar"): solo en la Discusión fisiológica (errores 7a a 7c).
- **m-1 de Resultados** ("Nada"): solo en Resultados (error 8c).
- **N10 de coherencia**: aplicada tal como la propuso el informe, con el valor equivocado (error 1).
- **D35 de Secciones pendientes** ("prueba" frente a "test"): sin aplicar; la decide Mario.
- **Forma 3 y 6 de Resultados** (menciones a "INFORME" y "CSV" en el cuerpo; criterio único para préstamos): sin aplicar; son de estilo global.
- **A11 de coherencia**, parte opcional (etiqueta de Git nueva para la versión auditada): no se creó. El texto sí se agregó.
- **C3 de coherencia**: se eligió conservar la referencia de Boucsein con autores completos y la marca "no citada en el texto; pendiente de lectura". Es una de las dos opciones propuestas.

## 4. Qué se comprobó y coincide

Cifras, contra los CSV leídos con pandas a precisión completa:

- **Curva temporal y fase 2** (`curva_temporal.csv`, `x1_placebo_bloque.csv`, `x2_estratificada.csv`, `descriptivos.csv`, `posthoc_no_registrado_estratos_con_posicion.csv`): −0,012 [−0,020; −0,005]; −0,010 [−0,016; −0,003]; −0,009 [−0,016; −0,002]; +0,009 [−0,027; +0,045]; +0,013 [+0,006; +0,021]; 0,677 [0,654; 0,699]; +0,047 [+0,017; +0,078] con 40 personas.
- **Fase 3** (`confirmatorio.csv`, `descriptivos.csv`): +0,009 [−0,020; +0,037]; +0,005 [−0,025; +0,035]; +0,005 [+0,001; +0,010]; −0,015 [−0,056; +0,024] y +0,040 [+0,014; +0,067] del post hoc.
- **16 y 18-11** (`contrastes.csv` de ampliación, enmienda, explicativo, final y robustez): −0,002 [−0,005; +0,000] (−0,002493); +0,040 [+0,012; +0,066]; −0,004 [−0,023; +0,017]; fusión −0,007 [−0,014; −0,001] y +0,006 [−0,032; +0,042]; GRU +0,020 [−0,017; +0,057] y +0,051 [+0,021; +0,080]; +0,046 [+0,018; +0,073].
- **Enfoques, limpieza y red**: A1 −0,008 [−0,015; −0,001], p de Holm 0,055; A3 p de Holm 0,055 con límite inferior sobre cero; B1 +0,181 [+0,164; +0,197]; 0,602 y caída 0,070; L4 −0,045 [−0,059; −0,032], 6/41; 0,681 [0,664; 0,697]; 0,524 [0,497; 0,550]; p de Holm 0,049 (0,049455); +0,058 [+0,032; +0,084]; +0,045 [+0,023; +0,069] sobre el modelo con historial; fiabilidad por mitades 0,76 y 0,66; 0,498 frente a 0,524; +0,028 frente a +0,035.
- **Descriptivos**: quintos de sesión 0,65 a 0,71 sin historial y 0,69 a 0,74 con historial; 34 a 41 personas por punto en activación y la línea gris del gráfico es la AUC de activación (`estilo_tecnico.py`); tipo de página (con historial solo queda bajo "texto" la categoría de 25 personas); importancias ±0,075, ±0,053 y ±0,027 entre 8 grupos.
- **Prevalencia por posición**, recalculada con `cierre_experimental_v3.Task`: 0,509 (1 s), 0,374 (2 s), 0,381 (3 s), 0,535 (9 a 12 s), 0,620 (12 s o más).
- **Desfase**: 0,184 a 0,528 s, mediana 0,448 s; 9 %, 22 % y 26 % de una ventana de 2 s.
- **Secciones pendientes**: 27,8 % de ventanas con más de 2.000 ms de fijación (0,2775); `pupil_n` medio 164,4; 0,755 frente a 0,942 (114/151 y 114/121 en ventanas de P1 con 151 filas); 360 y 367 variables (351 + 9; 351 + 10 + 6) en `cierre_v3_16-11-2026/protocolo.json`; cobertura mínima de EEG 80 %; mediana 125,14 Hz en las 104 sesiones y en las 48 principales; P25 36,0 % y P15 26,2 %; 13.498 ventanas, 66,28 % y kappa 0,3255; 72, 101 y 767 con su origen (validación, test y entrenamiento).

Hechos de proceso y de método, contra código, protocolos y Git:

- Las cinco particiones del 22-11 (semillas 1101 a 1105) son nuevas y no comparten ningún grupo con la registrada ni con las tres de robustez del 16-11 (comparación de `folds_rep`, `folds_main` y `folds_r3`). La curva temporal usa `folds_main`, que es la partición del 16-11.
- La etiqueta `cierre-experimental-2026-11-23` apunta a `aee6ab6`. Montaje: `06547f5` y `441bae9`. Enmienda E1: `8beb675` (16-11) y resultados `8c7a6d4` (18-11). Fase 2: `e3d9c71`, registrada "cuando la fase 1 aún corría" según el INFORME. Versión 1 del cierre V3 abortada en el primer fold (bitácora; carpeta `cierre_v3_16-11-2026_abortado_fusion`).
- Regla de decisión (`cierre_final_41p.py`, `decide`): "inferior" no exige Holm y va antes que "nulo concluyente"; A3 sería "respaldo" con p de Holm bajo 0,05.
- `np.log1p` sobre el número de SCR y su prominencia; `interpolate(limit=12, limit_area="inside")`; `pupil_n = len(pw)`; deduplicación por ventana y solo por índice; `find_peaks` por ventana; `--max-offset-s` 180; las 104 sesiones en formato `OpenBCI TXT`; seis variables comunes del EEG por canal; ningún script genera `heterogeneidad_por_grupo.csv`.
- Bitácora: diagnóstico del 30-10 (P4 y P34); "Mario comunica que su profesor aprobó usar las etiquetas V2".
- Referencias: 10 en texto completo y 8 por resumen; tres de las diez en preprint o manuscrito de autor (Dimigen 2020, Dimigen 2011, Lawhern 2018); autores de Boucsein et al. (2012); años confirmados en Crossref; Saavedra (2024) en `Estructura Tesis.md`.
- Red: "mismo filtrado que la extracción de variables" y R4 pasa a "inferior" al quitar una de cinco personas (INFORME de la red).

No comprobado por mí: la pérdida de 0,2 % de fijaciones por la deduplicación (requiere la exportación cruda de Tobii; tomé la cifra del informe de la ronda 2) y el contenido de los artículos citados (tomé `VERIFICACION_REFERENCIAS.md`).
