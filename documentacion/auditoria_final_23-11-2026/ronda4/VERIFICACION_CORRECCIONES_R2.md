# Verificación de las correcciones del commit `d2a90e8` — ronda 4 (26-11-2026)

Objeto: `git diff aef0f32 d2a90e8`. Hecha por un agente independiente del que aplicó los cambios. No se editó ningún archivo existente, no se entrenó ningún modelo y no se hicieron commits. Este informe es el único archivo creado.

## 1. Resumen

- **Cambios revisados:** 391 líneas añadidas o modificadas en 10 archivos fuente (cierre, cuatro borradores, minuta, `relato.py`, `ENSAYO.md`, README del espacio de trabajo y nota del bucle), que equivalen a unos 190 pasajes de prosa y 4 tablas nuevas, más los generados (`GUIÓN.md`, `index.html`, 28 SVG). De ellos, unas 150 cifras nuevas o cambiadas y unos 45 hechos de proceso o de método.
- **Errores encontrados: 12**, todos menores. Ninguno bloqueante ni importante. Una sola cifra está mal redondeada (`+0,102`, en dos documentos). El resto son: un hecho de proceso impreciso, una referencia cruzada que contradice la lista del mismo documento, una afirmación estadística cierta pero sin fuente, y frases a medio editar o desordenadas.
- **Hechos falsos introducidos:** ninguno.
- **Duplicados por la interrupción:** ninguno. No hay ninguna oración de 70 caracteres o más repetida dentro de un mismo documento, ni límites repetidos en las listas. Quedaron cuatro rastros de edición a medias (errores 4, 5, 6 y 7).
- **Hallazgos de los tres informes:** los 7 bloqueantes, los 24 importantes y H1 a H4 están aplicados en todos los documentos a los que iban dirigidos. Quedan dos propagaciones menores a medias y dos menores de la auditoría de código sin declarar (sección 3).
- **Presentación:** `GUIÓN.md`, `index.html`, `FUENTES.md` y `LEEME.md` del repositorio son idénticos byte a byte a lo que genera `relato.py` en una copia temporal fuera del repositorio. Los 28 SVG cambian solo en identificadores internos y fecha. Los 66 títulos de las dos tablas de `ENSAYO.md` coinciden con `GUIÓN.md`. Los planes de tiempo suman 1.200 s y 600 s, y sus subtotales también cuadran. Hay 37 preguntas numeradas de 1 a 37 y las dos referencias cruzadas ("pregunta 37" y "pregunta 25") apuntan a la pregunta correcta.
- **Reglas del proyecto:** el diff no toca `Estructura Tesis.md`, ningún `INFORME.md`, ningún CSV ni ningún script de `scripts/`. Ninguna línea añadida afirma aprobación del profesor guía, cierra una decisión abierta ni usa "emociones" por activación fuera de la cita de la hipótesis.

## 2. Errores encontrados

Las rutas son relativas a `/Users/mario/Proyectos/tesis-mds/`. Los documentos del vault se citan en su ubicación original. Todos los errores son de gravedad menor.

| N.º | Archivo | Texto exacto actual | Por qué está mal (fuente) | Texto exacto corregido |
|---|---|---|---|---|
| 1a | `documentos/01 Tesis MDS/Escritura/Borrador Resultados y Discusión 23-11-2026.md`, tabla de 7.1 | `\| GRU hasta 32 − GRU una ventana (sin búsqueda) \| +0,051 \| +0,045 [+0,007; +0,083] \| +0,059 [+0,014; +0,102] \|` | Redondeo doble. Con `F.ci` sobre las predicciones de `cierre_final_41p_16-11-2026`, el límite superior de las 16 personas es 0,101496, que redondea a 0,101. La auditoría de código lo imprimió como 0,1015 y de ahí pasó a 0,102 | `\| GRU hasta 32 − GRU una ventana (sin búsqueda) \| +0,051 \| +0,045 [+0,007; +0,083] \| +0,059 [+0,014; +0,101] \|` |
| 1b | `repos/Tesis_MDS/documentacion/Cierre_Experimental_Final_23-11-2026.md`, tabla de la ronda 3 | `\| GRU hasta 32 − GRU una ventana \| +0,051 \| +0,045 [+0,007; +0,083] \| +0,059 [+0,014; +0,102] \|` | Igual que 1a | `\| GRU hasta 32 − GRU una ventana \| +0,051 \| +0,045 [+0,007; +0,083] \| +0,059 [+0,014; +0,101] \|` |
| 2a | `.../Cierre_Experimental_Final_23-11-2026.md`, "Conclusión general" | `se registró cuatro minutos después de publicar ese resultado (`005a499`, 11:35, y `1bbb083`, 11:39).` | `git log`: `005a499` es de las 11:35:40 y `1bbb083` de las 11:39:06, es decir, 3 min 26 s. Además son horas de commit, no de publicación: cuándo se publicó cada uno no consta en el repositorio | `se registró menos de cuatro minutos después del commit de ese resultado (`005a499`, 11:35:40, y `1bbb083`, 11:39:06).` |
| 2b | `repos/Tesis_MDS/presentaciones/avances_tesis_06-11-2026/ENSAYO.md`, pregunta 24 | `El análisis con 41 personas lo registré cuatro minutos después de publicar ese resultado, para tener más potencia y sin cambiar la configuración.` | Igual que 2a | `El análisis con 41 personas lo registré menos de cuatro minutos después del commit de ese resultado, para tener más potencia y sin cambiar la configuración.` |
| 3 | `.../Borrador Conclusiones 23-11-2026.md`, 9.7 | `(encuadre provisorio, que depende de la quinta decisión abierta)` | En la lista del aviso inicial de este mismo documento, el encuadre es el punto (4) y el (5) es la cohorte nueva. "Quinta" es la numeración de la minuta y de la lámina 33 | `(encuadre provisorio, que depende de la decisión abierta sobre el encuadre: el punto 4 del aviso inicial y la decisión 5 de la minuta)` |
| 4 | `.../Borrador Resultados y Discusión 23-11-2026.md`, 6.3 | `Que "respaldo" exija Holm e "inferior" no es una asimetría de la regla registrada que no tiene una justificación escrita.` | Frase a medio editar: se lee "no es una asimetría", lo contrario de lo que quiere decir (`cierre_final_41p.py`, `decide`: "respaldo" exige `p_holm < .05` e "inferior" no) | `Que "respaldo" exija Holm e "inferior" no lo exija es una asimetría de la regla registrada, sin justificación escrita.` |
| 5 | `.../ENSAYO.md`, párrafo inicial | ``(`documentacion/auditoria_final_23-11-2026/ronda3/LECTURA_CRITICA_COMITE.md`): y tras la auditoría de código`` | Dos puntos sobrantes, resto de una edición a medias | ``(`documentacion/auditoria_final_23-11-2026/ronda3/LECTURA_CRITICA_COMITE.md`) y tras la auditoría de código`` |
| 6 | `.../ENSAYO.md`, guion de la lámina 29 | `En activación lo es en parte: +0,046 sobre el placebo en el contraste registrado` | La frase anterior cambió de "no es información temporal" a "no viene de las ventanas previas", y "lo es" quedó sin antecedente | `En activación sí viene en parte del historial: +0,046 sobre el placebo en el contraste registrado` |
| 7 | `.../Cierre_Experimental_Final_23-11-2026.md`, "Auditoría de código, ronda 3" | `Cuatro afectan lecturas y este documento los declara en "Límites":` | Los dos puntos anuncian los cuatro hallazgos, pero lo que sigue es la tabla por grupo de personas; la lista H1 a H4 quedó debajo de la tabla | `Cuatro afectan lecturas y este documento los declara en "Límites"; se listan bajo la tabla, que separa los contrastes de activación por grupo de personas (descriptiva, no registrada):` |
| 8 | `.../Borrador Resultados y Discusión 23-11-2026.md`, 7.1 | `los intervalos de ambos grupos se solapan y, según la auditoría, la diferencia entre grupos no es significativa con 16 personas.` | La afirmación es cierta, pero no tiene fuente: `AUDITORIA_CODIGO.md` la enuncia sin prueba y `c07` no calcula ninguna. La calculé (anexo): en el contraste principal del 16-11 la diferencia entre grupos es +0,054, con p = 0,15 (Welch y permutación); con cinco particiones, p = 0,38. Ninguno de los nueve contrastes de la tabla baja de 0,05, pero dos quedan cerca: con tiempo de sesión (p = 0,08) e historial menos posición (p = 0,09). La frase se repite sin cifra en 8.4, Conclusiones 9.5, minuta, cierre y pregunta 37 del ensayo; basta con dar la fuente aquí | `los intervalos de ambos grupos se solapan y la diferencia entre grupos no alcanza significación en ninguno de los nueve contrastes de la tabla (principal del 16-11: +0,054, p = 0,15; con cinco particiones, p = 0,38; los más cercanos al umbral son el contraste con tiempo de sesión, p = 0,08, y el de historial menos posición, p = 0,09; prueba de Welch sobre las diferencias por persona, comprobación no registrada del 26-11).` |
| 9a | `.../Borrador Conclusiones 23-11-2026.md`, 9.5 | `y su soporte real excede los 6 s: el 49 % del peso cae en las ventanas nominales, el 25 % antes y el 25 % después.` | `c03` mide el peso de la GSR sobre la parte tónica de la etiqueta, no sobre la etiqueta entera (los otros tres componentes no pasan por ese núcleo). El borrador de Resultados (7.3) y el de Secciones pendientes (4.5.2) lo dicen bien | `y su soporte real excede los 6 s: en su parte tónica, el 49 % del peso de la GSR cae en las ventanas nominales, el 25 % antes y el 25 % después.` |
| 9b | `.../Cierre_Experimental_Final_23-11-2026.md`, "Límites" | `deja el 49 % del peso en las ventanas nominales, el 25 % antes y el 25 % después.` | Igual que 9a | `deja el 49 % del peso de la parte tónica en las ventanas nominales, el 25 % antes y el 25 % después.` |
| 10 | `.../relato.py`, nota de la lámina 23 (y `GUIÓN.md`/`index.html` al regenerar) | `así que no puedo decir que no haya solapamiento. Este contraste es positivo tanto en las 25 personas con que elegí la configuración (+0,035) como en las otras 16 (+0,064). Aun así le gana al placebo por +0,046 y mejora en 28 de 41 personas, p Holm 0,004.` | La frase insertada separó "Aun así" de la salvedad a la que responde. `ENSAYO.md` tiene el orden correcto | `así que no puedo decir que no haya solapamiento. Aun así le gana al placebo por +0,046 y mejora en 28 de 41 personas, p Holm 0,004; es positivo tanto en las 25 personas con que elegí la configuración (+0,035) como en las otras 16 (+0,064).` |
| 11 | `.../ENSAYO.md`, guion de la lámina 33 | `que además lista los objetivos y contribuciones que conviene revisar y la información de participantes y ética que tengo que pedir al proyecto.` | La nota de la lámina 33 en `relato.py` agrega un tercer punto que el ensayo omite, y el ensayo declara que no quedan diferencias con `relato.py` | `que además lista los objetivos y contribuciones que conviene revisar, la información de participantes y ética que tengo que pedir al proyecto, y cómo declarar el uso de asistentes automáticos en las revisiones.` |
| 12 | `.../Borrador Secciones pendientes 23-11-2026.md`, 4.8.3 | `Rigen desde el análisis del 16-11-2026 y se fijaron antes de ejecutar cada análisis posterior;` | "Posterior" deja fuera al propio análisis del 16-11, cuyas reglas también entraron antes de correr (`1bbb083` contiene `protocolo.json` y `cierre_final_41p.py` con `decide`) | `Rigen desde el análisis con 41 personas del 16-11-2026 y se fijaron antes de ejecutar cada análisis, incluido ese;` |

El error 10 está en `relato.py`: después de corregirlo hay que regenerar la presentación.

Frases relacionadas con el error 9 que usan "cerca de un cuarto de su peso" (Conclusiones 9.1, minuta, Discusión fisiológica "Escala temporal", nota de la lámina 23): son ambiguas, no falsas, porque "su" puede leerse como el nivel tónico. Si se quiere precisión, cambiar `de su peso` por `del peso de esa componente` en las tres primeras.

## 3. Lo no aplicado o no propagado

Ninguno es bloqueante ni importante.

1. **I2 de la lectura crítica ("no es información temporal"), propagación a medias.** El borrador de Resultados cambió la fila de 8.1 a "¿La mejora proviene de la fisiología de las ventanas previas?"; el cierre y la lámina 29 conservan la pregunta antigua.
   - Cierre, tabla inicial: `| ¿La mejora es información temporal? |` → `| ¿La mejora proviene de la fisiología de las ventanas previas? |`
   - `relato.py`, lámina 29: `'¿Es información temporal?'` → `'¿Viene de las ventanas previas?'` (regenerar después).
2. **Tabla por grupo, distinta en los dos documentos que la traen.** La del cierre no tiene la fila que sí está en el borrador de Resultados, y no avisa que la banda de 6 s tiene 40 personas (24 y 16, no 25 y 16).
   - Cierre, agregar tras la fila "Historial − posición (18-11)": `| Historial − placebo (16-11) | +0,038 | +0,057 [+0,023; +0,092] | +0,008 [−0,048; +0,058] |`
   - Cierre: `| Banda de 6 s − placebo |` → `| Banda de 6 s − placebo (40 personas: 24 y 16) |`
   - Resultados 7.1: `| Banda de 6 s − placebo (40 personas) |` → `| Banda de 6 s − placebo (40 personas: 24 y 16) |`
3. **M2 de la auditoría de código (resolución "Declarar"), sin aplicar.** Agregar en Resultados 8.8, en la viñeta que termina en `La GRU y los MLP no tuvieron búsqueda de hiperparámetros.`: `La GRU se entrenó con tres hilos y sin forzar algoritmos deterministas: el fold 0 se reproduce exacto en el equipo usado, lo que no está garantizado en otro.`
4. **M12 de la auditoría de código (resolución "Declarar"), sin aplicar.** Agregar en Secciones pendientes 4.6.5, tras `frente a las 120 muestras esperadas a 60 Hz.`: `Además, al preparar la GSR y la pupila se conserva la primera fila de cada marca de tiempo; si una fila de otro sensor comparte la marca con la del ojo, puede desplazarla. No se cuantificó.`
5. **"Al menos un tercio" junto a "cerca de un tercio".** Resultados 7.6 y Conclusiones 9.3 y 9.7 pasaron a "cerca de un tercio, que se lee como cota inferior sin ser una demostración". Resultados 8.3 (`al menos un tercio de lo que el *Modelo Estudiante* de atención recupera desde el EEG depende de componentes oculares` y `depende, al menos en un tercio, de la huella`) y Discusión fisiológica 8.x.3 (`al menos un tercio de lo que el *Modelo Estudiante* recupera`) conservan "al menos". La lectura crítica solo pidió cambiar "es la huella" por "depende de", así que no es una omisión; es una tensión de tono dentro del mismo documento. Opción: `al menos un tercio` → `cerca de un tercio` en esos tres lugares.
6. **Dirección del desfase de reloj: se puede cerrar el "por confirmar".** `scripts/montaje_ocular_41p.py`, `lagged_corr` (líneas 60 a 65) correlaciona la referencia ocular en t con el EEG en t + desfase, y el desfase elegido (línea 83) es positivo en las 41 personas (`personas.csv`, `lag_parpadeo_s` de 0,184 a 0,528). El EEG con marca T contiene la conducta ocular de T − desfase. Lo escrito es correcto.
   - Resultados 7.6: `esa dirección falta confirmarla en el script de montaje.` → `esa dirección se comprobó en el script de montaje (función `lagged_corr`).`
   - Secciones pendientes 4.6.1: `Falta declarar la dirección del corrimiento: por el signo con que se estimó, cada ventana de EEG contendría actividad ligada a la conducta ocular de unas décimas de segundo antes de la ventana, y no posterior, lo que queda por confirmar en `scripts/montaje_ocular_41p.py`.` → `La dirección del corrimiento es hacia el pasado: por el signo con que se estimó (función `lagged_corr` de `scripts/montaje_ocular_41p.py`), cada ventana de EEG contiene actividad ligada a la conducta ocular de unas décimas de segundo antes de la ventana, y no posterior.`
7. **Menores de claridad de la lectura crítica sin aplicar**, todos de estilo global y a criterio del autor: 1 a 6 y 11 a 13 (nombres de etapas, códigos de prueba, material de proceso en los capítulos), 7 ("señal cruda" para una señal filtrada), 8 ("placebo disperso" y "placebo de bloque" sin definir en 6.2), 9 y 10. Sobre el 10: Resultados 6.1 ya no dice "quietud de la mirada", pero sigue sin decir con qué signo entra cada variable ni qué significa "alta"; la pregunta 15 del ensayo lo reconoce como pendiente.
8. **`ENSAYO.md`, párrafo inicial y última sección:** dicen que en la lámina 12 cambió el título. También cambió su pie visible ("cada una se predice con un modelo ajustado sin ella"). Detalle sin consecuencia.
9. **Fuera del commit:** `notas/loop-revision-26-11-2026.md` del espacio de trabajo ya tiene la ronda 3 y es más nueva que su copia en `respaldo_local/`. Se pondrá al día con el próximo respaldo.

## 4. Qué se comprobó y coincide

Cifras, recalculadas desde la fuente y redondeadas desde el valor completo:

- **Tabla por grupo (25 y 16).** Recalculada con `c07` y con seis decimales desde las predicciones guardadas. Las nueve filas del borrador de Resultados y las ocho del cierre coinciden, salvo el `+0,102` (error 1). Casos límite que están bien: +0,100505 → +0,101; −0,065521 → −0,066; +0,050532 → +0,051; +0,006544 → +0,007. La fila "Historial − placebo (16-11)", que no está en la auditoría de código, también coincide: +0,0379; +0,0569 [+0,0227; +0,0923]; +0,0082 [−0,0476; +0,0583].
- **Búsqueda interna de V3** (`busqueda_interna_activacion.csv`): 0,5123, 0,5121, 0,5341, 0,5311, 0,4994, 0,5311; medias 0,5152 y 0,5248; historial menos sin historial −0,013 y +0,019; en atención +0,0135 y +0,0124. El criterio es la media sobre los contextos 1, 8 y 32 en validación interna (`cierre_experimental_v3.py`, líneas 314 a 334).
- **Cierre V3** (`contrastes.csv`): +0,059 en validación, +0,033 en test, +0,016 [−0,036; +0,070] en entrenamiento.
- **Pesos del profesor PCA** (`c09`, `profesor_final.joblib`): 0,557, 0,520, 0,508, 0,398 y −0,052; varianza explicada 51,5 %; ajuste con 25 personas.
- **Soporte de la etiqueta de activación** (`c03`): 49,2 %, 25,4 % y 25,4 %; 3,7 % antes de t−10; núcleo con 24,8 % a más de 5 s y 6,5 % a más de 10 s. AUC por componente 0,911, 0,595, 0,522 y 0,522. GSR desplazada: 0,871 a 6 s, 0,851 a 12 s y 0,804 a 30 s antes.
- **Fijaciones** (`c09`): 27,7 % de las ventanas etiquetadas sobre 2.000 ms, 4,0 % sobre 3.000 ms, máximo 11.365 ms.
- **Orden de estímulos por grupo** (`caracteristicas_multimodales.csv`, recalculado): grupos de 13, 12, 12 y 11 personas; 265 pares dentro de grupo, los 265 con el mismo orden en los estímulos que comparten; ningún par de grupos distintos coincide; Kendall entre grupos de 0,261 a 0,705.
- **Ocho filas con dos reglas** (`curva_temporal.csv`, `x1_placebo_bloque.csv`, `x2_estratificada.csv`, `e1_confirmatorio.csv`): seis "inferior" y dos "respaldo", todas de atención y todas con el intervalo de 90 % dentro de ±0,02. Precedencia del código: respaldo, inferior, nulo concluyente.
- **P4:** aporta 0,0094 de los 0,036 y conserva 26 ventanas. La etiqueta conserva 11.796 de 22.211 ventanas (53,1 %).
- **Desfase:** dos grupos, P2 a P21 más P36 y P37 (0,18 a 0,35 s) y el resto (0,44 a 0,53 s).

Hechos de proceso y de método:

- `005a499` es ancestro de `1bbb083`, ambos del 16-11; el segundo solo agrega `protocolo.json` y `cierre_final_41p.py`. La bitácora del 16-11 da la experimentación por cerrada tras el V3, antes del análisis con 41 personas.
- La versión 1 del cierre V3 se detuvo en el fold 1 por una auditoría de código (INFORME del V3 y bitácora).
- Filtro tónico: Butterworth de orden 2 a 0,05 Hz con `filtfilt` sobre la grabación completa; fásica igual a señal menos tónica; z con toda la grabación (`prepare_gsr`).
- El informe del 29-10 trae la tabla en que el PCA se predice mejor y la advertencia de que eso no prueba validez. La nota `Modelo Profesor - Decisiones.md` existe y deja la componente principal como sensibilidad.
- La aprobación de las etiquetas V2 que comunicó Mario está en `notas/bitacora.md`.
- La sección nueva de la minuta tiene 18 filas, como dice la nota del bucle.
- Las láminas que `ENSAYO.md` dice que cambiaron son exactamente las que cambian entre los dos commits: título de la 12; cuerpo de la 5, 10, 12, 29, 30 y 31; notas de la 1, 3, 5, 10, 11, 12, 18, 20, 21, 22, 23, 25, 26, 29, 30 y 33.
- Las 21 preguntas de defensa de la lectura crítica están cubiertas: 14 como preguntas nuevas (23 a 36) y 7 fusionadas en las preguntas 5, 10, 11, 12, 15, 17 y 22. La pregunta 37 es nueva y cubre el hallazgo H1 de la auditoría de código.

No comprobado por mí: el contenido de los artículos citados y las cifras que el commit no tocó.

## Anexo: prueba de la diferencia entre grupos (error 8)

Diferencia por persona de cada contraste, separada entre las 25 personas de entrenamiento y las 16 de validación y test, desde las mismas predicciones que usa `c07`. Prueba de Welch y permutación de etiquetas de grupo (20.000 permutaciones). No entrena ni escribe nada.

| Contraste de activación | Diferencia entre grupos | p (Welch) | p (permutación) |
|---|---|---|---|
| Principal, 16-11 | +0,054 | 0,149 | 0,147 |
| Principal, 5 particiones | +0,025 | 0,383 | 0,411 |
| Con tiempo de sesión | +0,061 | 0,079 | 0,064 |
| Con posición (Q1) | +0,044 | 0,148 | 0,131 |
| Historial − posición (18-11) | +0,064 | 0,090 | 0,088 |
| Historial − placebo (16-11) | +0,049 | 0,155 | 0,133 |
| Historial desplazado 6 − placebo | −0,029 | 0,348 | 0,313 |
| Banda de 6 s − placebo | +0,028 | 0,344 | 0,387 |
| GRU hasta 32 − GRU una ventana | −0,013 | 0,665 | 0,673 |

Son nueve pruebas sin corrección, descriptivas y no registradas.
