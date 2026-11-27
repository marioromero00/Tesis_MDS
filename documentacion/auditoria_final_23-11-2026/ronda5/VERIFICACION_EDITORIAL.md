# Verificación independiente de la edición editorial — ronda 5

Fecha: 26-11-2026. Verificador: asistente automático, a pedido del autor; no es la revisión de un tercero. No se editó ningún borrador, no se entrenó ningún modelo y no se hizo ningún commit. Este archivo es lo único que se escribió.

Abreviaturas: RD = Borrador Resultados y Discusión; DF = Borrador Discusión fisiológica; CO = Borrador Conclusiones; SP = Borrador Secciones pendientes (todos del 23-11-2026). "Anterior" = `ronda4/pre_editorial/`; "actual" = `documentos/01 Tesis MDS/Escritura/`.

## Resultado en una frase

Ninguna cifra de RD cambió de contraste, modelo, etiqueta, fecha, número de particiones, número de personas ni decisión, y no hay errores bloqueantes. Hay 7 problemas importantes y 17 menores. Los importantes son de dos tipos: salvedades que salieron de CO sin quedar en el lugar al que CO remite (el script del editor no las ve porque la cifra sigue en otra frase o en RD), y cuatro frases nuevas que afirman o priorizan más de lo que afirmaba el texto anterior.

## Método

1. Lectura completa y en paralelo de RD anterior y RD actual, de DF anterior, de CO anterior y actual, y de las diferencias palabra por palabra de SP y DF.
2. Emparejamiento por programa de cada oración o fila de tabla con cifra de la versión anterior con su mejor equivalente actual (mismas cifras y mayor similitud de texto). Las unidades idénticas se dan por buenas; las demás se revisaron a mano, mirando contraste, fecha, particiones, n, intervalo y decisión.
3. Emparejamiento inverso: cada oración actual sin equivalente cercano en ninguno de los cuatro archivos anteriores se listó y se revisó como "afirmación nueva".
4. Contraste con fuentes primarias de los hechos nuevos y de las cifras dudosas: `protocolo.json` de `reapertura_41p`, `reapertura_fase2_41p`, `reapertura_fase3_41p`, `enfoques_41p` y `ampliacion_41p`; `INFORME.md` de `reapertura_41p`, `enfoques_41p`, `profesor_binario_reconstruido` y `cierre_v3`; `e2_descriptivos.csv`, `e4_confirmatorio.csv`, `enmienda_e1_lag6/contrastes.csv` y sus predicciones; `etiquetas_gsr_calidad_v2/etiquetas.csv.gz`.
5. Comprobación por programa del Markdown (celdas por fila de cada tabla, niveles y orden de encabezados, párrafos y oraciones duplicados, paréntesis, comillas y negritas sin cerrar), de la igualdad entre el anexo y la tabla 6.4 anterior, y de la igualdad de la lista de referencias.
6. Búsqueda de remisiones en RD, CO, SP y DF, y de citas a secciones de RD o CO en la minuta, el documento de cierre, `relato.py` y `ENSAYO.md`.

Los scripts usados quedaron en el directorio temporal de la sesión y no forman parte del repositorio.

## Recuento

| Comprobación | Cantidad | Resultado |
|---|---|---|
| Unidades con cifra, RD + DF anteriores | 437 | 317 idénticas en la versión actual; 120 revisadas a mano; 0 con cambio de dueño |
| Unidades con cifra, CO anterior | 48 | 23 idénticas; 25 revisadas a mano; 6 salvedades o cifras que salieron de CO (errores 1, 3, 14, 15, 16 y la mención de la GRU) |
| Unidades con cifra, SP anterior | 143 | 125 idénticas; 18 revisadas a mano; 0 problemas de cifra |
| Tablas de RD | 24 | Todas bien formadas. Las filas numéricas son idénticas a las anteriores; solo cambian rótulos de la primera o segunda columna (lista abajo) |
| Salvedades de fondo comprobadas | 24 | 24 presentes en RD; 5 debilitadas o ausentes en CO; 2 pasaron de la prosa a una nota de trabajo |
| Oraciones actuales sin equivalente anterior | 213 (RD 164, CO 23, SP 26) | Todas revisadas; 12 hechos nuevos comprobados en la fuente; 2 hechos imprecisos (errores 9 y 10); 5 lecturas que afirman o priorizan más (errores 4 a 7 y 20) |
| Remisiones revisadas | 147 en RD, CO y SP (130 a secciones, 9 a decisiones, 3 notas a/b/c, 5 a tablas o anexo), más 7 en la minuta, `ENSAYO.md` y `relato.py` | 0 rotas; 3 que apuntan a un destino que no contiene lo que dicen (errores 2, 12 y 13); 2 desactualizadas fuera de los borradores (error 17) |
| Referencias | 18 en la lista; 17 citadas en el cuerpo | Lista idéntica a la de DF anterior; Boucsein et al. (2012) sigue marcada como no citada; ninguna cita del cuerpo falta en la lista |
| Oraciones con cita en DF anterior | 15 | 12 literales en RD 8.3–8.5; 3 partidas o reordenadas sin cambio de atribución ni de matiz |

Rótulos de tabla que cambiaron sin cambiar cifras: 7.1 ("16-11, una partición" pasa a "Una (16-11)"; "22-11, 5 particiones" pasa a "Cinco, promedio (22-11)"); 7.5 ("Principal, 16-11" pasa a "Principal, una partición (16-11)"; se agregan "(sección 7.1)", "(Q1; sección 7.3)" y "(18-11, post hoc)"; "desplazado 6" pasa a "desplazado seis ventanas"); 7.7 y 7.11 ("Mejoran" pasa a "A favor" en las tablas B y C); 7.9 (L2: "Control − EEG limpio" pasa a "EEG sin 3 componentes no oculares (control) − EEG limpio"); 8.1 (parte de las celdas de activación pasa a las notas a, b y c, con las mismas cifras).

## 1. Cifra en contexto

Sin hallazgos en RD. Casos que miré con más cuidado y que están bien:

- +0,046 [+0,018; +0,073] (historial desplazado seis ventanas menos placebo, 16-11, una partición, 41 personas, 28/41, p de Holm 0,004, respaldo y no efecto relevante). Coincide con `enmienda_e1_lag6/contrastes.csv` (0,04604 [0,01844; 0,07315]; p de Holm 0,00436; 28 de 41). Conserva su dueño en RD 7.3, 7.5, 8.1, 8.4 y CO 9.1.
- +0,047 [+0,017; +0,078] (banda de 6 s menos placebo disperso, 22-11, una partición, 40 personas, respaldo). Sigue separado del anterior en 7.3 ("no son el mismo contraste") y en CO 9.1.
- +0,036 [+0,010; +0,065] frente a +0,034 [−0,001; +0,069]: cada uno conserva su número de particiones y su decisión en 7.1, 8.1 y CO 9.1.
- Tabla por grupo (25 y 16 personas) y los p de la prueba de Welch (0,15; 0,38; 0,08; 0,09): pasaron completos de 7.1 a 7.5, con la misma atribución a contraste.
- 49 %, 25 %, 25 % y 3,7 % del filtro tónico: pasaron de 7.3 a 6.1, con el mismo sujeto (peso de la GSR sobre la parte tónica de la etiqueta de una ventana).
- +0,045 [+0,023; +0,069], 30 de 40, p de Holm 0,0004, efecto relevante (adaptación con historial): la frase nueva de 8.5 coincide con `e4_confirmatorio.csv` (0,0448 [0,0234; 0,0686]; 30 de 40; 0,00040).
- 0,681, 0,675 y 0,496 en la frase nueva de 8.3: coinciden con `e2_descriptivos.csv` (solo EEG 0,6809, 41 de 41; a igual posición 0,6745; control barajado 0,496 [0,482; 0,510], una partición).
- P4 con 26 ventanas y 11.796 de 22.211: comprobados en `etiquetas.csv.gz`.

En CO las cifras que quedan conservan su dueño. Las que salieron de CO están en la sección siguiente.

## 2. Salvedades de fondo

| Salvedad | RD actual | CO actual | Estado |
|---|---|---|---|
| Personas ya consultadas; nada es confirmación independiente | 6.5, 7.1, 8.1, 8.8 | 9.1, 9.5 | Presente |
| Diseño con 41 personas adoptado tras el nulo del cierre V3 | 6.3, 8.1, 8.8 | 9.1, 9.5 | Presente |
| Configuración de activación elegida por el modelo con historial con 25 de 41; tabla por grupo y p | 7.5 completa; 6.3, 6.5, 8.4, 8.8 con remisión | 9.1 (+0,046 y +0,021); 9.5 sin +0,055 y +0,001, sin "patrón inverso", sin "no significativa con 16 personas", sin la GRU | Debilitada en CO (error 15) |
| Contraste principal estimado varias veces (+0,028 a +0,047; no todos los intervalos excluyen el cero) | 7.1, 8.1 nota a, 8.4 | Ausente; tampoco está en RD 8.8 | Desapareció de CO (error 1) |
| Soporte tónico más largo que 6 s, con 49 %, 25 %, 25 % y 3,7 % | 6.1 completa; 7.3, 8.4 y 8.8 con remisión | 9.1 ("cerca de un cuarto"); 9.5 sin porcentajes, remite a 6.1 | Perdió cifras en CO; la remisión funciona (error 16) |
| Solo hay respaldo a 6 s; 12 s inconcluso; desde 24 s no se distingue, sin demostrar ausencia | 7.3, 8.1 nota b, 8.4 | 9.1 | Presente |
| Multiplicidad entre etapas (doce) | 8.8 | 9.5 | Presente |
| Etiqueta con *Modelo Profesor* de componente principal elegida por más predecible; 66 %, kappa 0,33 | 6.1, 8.8 | 9.5 sin el 66 % | Perdió cifra en CO (error 14) |
| Pupila casi no pesa (−0,052) | 6.1; 8.8 remite | 9.5 | Presente |
| Fijaciones sumadas con su duración completa (28 % y 4 %) | 6.1, 8.2, 8.8 | Ausente | Desapareció de CO (error 3) |
| Limpieza ocular parcial; componentes elegidos con la mirada | 7.9, 8.3.2, 8.8 | 9.3, 9.5 | Presente |
| Desfase de reloj (0,18 a 0,53 s; dos valores) | 7.8, 8.8; ya no está en 8.7 | 9.5 | Presente; salió de "Implicancias" (sigue en 8.9 como trabajo futuro) |
| Orden de estímulos compartido dentro de cada grupo | 8.8 | 9.5, sin "no se evaluó dejando grupos completos fuera" | Presente |
| P4 con 26 ventanas | 7.1, 8.8 | 9.5 | Presente |
| Normalización con la sesión completa | 8.8 (decisión 6) | 9.5 ("relativas a la sesión") | Presente, igual que antes |
| Red: una arquitectura, sin control propio, escala por persona | 7.10, 8.3.4, 8.8 | 9.5, sin la escala, igual que antes | Presente |
| Fusión solo entre MLP; signo contrario con HGB | 7.6; 8.6 ya sin cifras, con remisión | 9.2 | Presente |
| Dos imprecisiones del procesamiento congelado | 8.8, con remisión a SP 4.6.4 y 4.6.5 | No estaba | Presente |
| Uso de asistentes automáticos en las revisiones | 6.5 | Aviso de estado | Presente |
| Ocho filas que cumplen dos reglas | 6.4, 8.8 | 9.5, sin "seis y dos, todas en atención" | Presente |
| Decisiones al filo (A1, A3, adaptación, R1) | 7.2, 7.10, 7.11, 8.8 | No estaba | Presente en RD; salió de 8.2 (error 4) |
| 53 % de las ventanas de activación | 8.8 | 9.5 | Presente |
| Reproducibilidad: se verifican hashes, no se reentrena | Solo en nota de trabajo de 8.8 | No estaba | Pasó a nota de trabajo (error 18) |
| Base anatómica de la hipótesis sobre Critchley (2002) sin confirmar | Solo en nota de trabajo de 8.5 | No estaba | Pasó a nota de trabajo (error 19) |

## 3. Afirmaciones nuevas

Hechos nuevos comprobados y correctos:

- "kappa de Cohen 0,33" (6.1): el informe dice "kappa 0,3255" y los scripts usan `cohen_kappa_score`.
- *Placebo de bloque* (6.2): coincide con `reapertura_41p_22-11-2026/INFORME.md`, línea 58. El *placebo disperso* tiene una imprecisión (error 10).
- "modelo de referencia designa al HGB con variables calculadas" (6.2): coincide con el uso anterior en 7.6.
- "Son las mismas de la sección 4.8.3" (6.4): la tabla de SP 4.8.3 tiene las mismas cinco reglas y el mismo párrafo de precedencia.
- Códigos P1 y P2 (6.4): `protocolo.json` de la fase 1 dice "P1: hgb_c32 − hgb_c1" y "P2: c32_ts − c1_ts". Q1 y Q2, A1 a A3, B1 a B8 y C1 a C3 coinciden con los protocolos de la fase 3 y de los enfoques.
- Columna "Pregunta que responde" (6.6): E1 a E6 de la ampliación coinciden con su protocolo (E1 historial desplazado frente al placebo; E2 calibración; E3 fusión; E4 a E6 descriptivos); E1 a E4 del 22-11 coinciden con las familias del protocolo de enfoques. Doce filas, doce etapas.
- "selección anidada, es decir, con la configuración elegida en una validación interna que no incluye a las personas evaluadas (sección 4.8.2)" (7.5): coincide con SP 4.8.2.
- "Los intervalos de la columna de 41 personas están en las secciones 7.1, 7.3 y 7.4" (7.5): los nueve están donde dice.
- "El criterio escrito habla de apoyo parcial si la ventaja aparece en una sola de las dos variables" (8.1 y SP 4.8.3): coincide con la tabla de `Marco Teorico/Problema e hipótesis.md`.
- Frase positiva sobre la detección (8.3 y CO 9.3): las cifras son correctas; la lectura está en el error 5.
- Párrafo de adaptación a la persona (8.5): cifras correctas; la lectura está cubierta ("ningún contraste pone a prueba esa lectura") y conserva los dos límites. Tiene una imprecisión heredada (error 11).
- "El contraste simple entre el modelo con y sin historial es desigual entre personas" (CO 9.7), que antes se decía del efecto en general: es correcto reasignarlo. En el contraste del historial desplazado frente al placebo la mediana por persona es +0,054 y mejoran 28 de 41 (calculado para esta verificación desde `enmienda_e1_lag6/predicciones_activacion.csv.gz`; descriptivo, no registrado), frente a mediana +0,014 y 23 de 41 del contraste simple.

Lecturas nuevas sin objeción: 7.9 ("dos objeciones de sentido opuesto"), 8.4 ("Los dos contrastes que la sostienen no tienen la misma solidez"; "es más frágil"), 8.3.4 ("Los dos que más la condicionan": son los dos límites que ya traía DF), 8.10 punto 5 (amplía una decisión abierta, no la cierra).

Lecturas nuevas con objeción: errores 4, 5, 6, 7 y 20.

## 4. Remisiones y numeración

Todas las remisiones de RD, CO y SP apuntan a secciones que existen. Las referencias a "decisión N" coinciden con el orden de la minuta y de 8.10 (1 cohorte nueva o escribir, 2 margen 0,02, 3 emociones como activación, 4 etiqueta original o corregida, 5 encuadre, 6 normalización con la sesión completa, 7 *Modelo Profesor* con PCA). Las notas a, b y c de 8.1 existen y corresponden a su fila. "Las dos últimas son las de mayor consecuencia" sigue apuntando a 6 y 7.

La minuta, el documento de cierre y `relato.py` no citan números de sección de RD. `ENSAYO.md` cita secciones de CO (9.1, 9.5, 9.6 y 9.7), que existen; una de esas citas quedó sin contenido (error 17).

Problemas: errores 2, 12, 13 y 17.

## 5. Integración de la discusión fisiológica

Las diez correcciones que pide `VERIFICACION_REFERENCIAS.md` siguen aplicadas en RD 8.3–8.5 (dipolo con Plöchl; espiga sacádica de 20 a 90 Hz con Keren; músculo con Goncharova, "puede ocultar o imitar"; parpadeo con Iwasaki para el máximo frontopolar y Plöchl para el mecanismo; "atribuida a los músculos extraoculares"; Dimigen "con la configuración habitual"; Jung "a lo sumo tantas fuentes como canales"; Benedek y Kaernbach para la inervación y las latencias; Barry "que documentan estos trabajos" y "al comparar condiciones"; Lawhern "serie temporal del EEG, sin variables calculadas a mano"). La versión actual mejora al resumen que traía RD anterior, que citaba a Iwasaki junto con Plöchl para el parpadeo y daba el origen muscular de la espiga sin atenuar.

La lista de referencias tiene 18 entradas, idénticas a las de DF anterior. Las 17 citadas en el cuerpo están en la lista; Boucsein et al. (2012) aparece solo en la lista y en una nota de trabajo, y sigue marcada como no citada. Único cambio de fondo: error 19.

## 6. Notas de trabajo y anexo

La tabla del Anexo de trazabilidad es idéntica, fila por fila, a la tabla 6.4 anterior (15 líneas). RD tiene 24 notas de trabajo y SP y CO suman 9. Todo el material de proceso que salió de la prosa está en una nota o en el anexo: comprobaciones de la auditoría de código del 26-11 (6.1, 7.3, 7.5; SP 4.5.2, 4.6.3, 4.6.4); recálculos de la auditoría final (7.1, 7.6, 7.10, 7.12); sensibilidades pedidas por la auditoría de resultados (7.1, 7.3); redondeos dobles de los informes (7.2, 7.3, 7.9, 7.11); columna no declarada por el informe de origen (6.2); orden de commits y significado de "auditoría" (6.5; SP 4.8.3); segunda familia agregada por la auditoría (7.7); `lagged_corr` (7.8; SP 4.6.1); diagnóstico del 26-11 (7.2); `AUDITORIA_SECCIONES_PENDIENTES.md` y reproducibilidad (8.8); tamaño de muestra y cierre de la experimentación (8.9); catálogo y lecturas de referencias (8.3 y lista); semilla, fechas de detección y tolerancia (SP). No encontré nada borrado.

Dos elementos que pasaron a nota de trabajo no son solo proceso: errores 18 y 19.

## 7. Vocabulario

- "apoyo parcial": solo para la hipótesis. Correcto. "Apoyo acotado" y "apoyo más sólido" ya no aparecen.
- "cerca de un tercio": único uso en RD, CO y DF. Correcto.
- "profesor PCA" y "Modelos Profesores": sin apariciones. 8.10 dice "*Modelo Profesor* con PCA"; los avisos iniciales, 6.1 y CO 9.5 dicen "*Modelo Profesor* de componente principal (PCA)", que es compatible.
- Siete decisiones en el orden pedido en RD (aviso y 8.10), CO (aviso), SP (aviso) y la minuta. Ninguna cerrada.
- Ninguna aprobación del profesor guía afirmada. La única mención en SP (pseudoetiquetas GSR V2, bitácora del 01-11) sigue en el aviso.
- "emociones": solo entre comillas, al nombrar la decisión 3 y la hipótesis; "emoción" en 8.5 pertenece a la cita de Critchley.
- "respaldo": como rótulo de la regla en todos los usos sustantivos. Quedan tres usos del verbo con otro sentido (error 21) y un "indicio" (error 8).

## 8. Calidad del Markdown

Las 24 tablas de RD y las 8 de SP tienen el mismo número de celdas en todas sus filas y línea separadora. No hay saltos de nivel de encabezado, encabezados repetidos, numeración fuera de orden, párrafos duplicados (salvo dos líneas de fuentes, error 22), ni paréntesis, comillas o negritas sin cerrar. No encontré frases rotas. Una frase es ambigua (error 6).

## Tabla de errores

Gravedad: no hay bloqueantes.

| # | Archivo | Sección | Texto exacto actual | Problema y fuente | Texto exacto corregido | Gravedad |
|---|---|---|---|---|---|---|
| 1 | CO | 9.5 | "Ningún resultado se obtuvo en personas nuevas, y los análisis posteriores al 16-11-2026 son exploratorios o dirigidos (sección 9.1). El diseño de evaluación cambió después de un resultado nulo" | Desapareció la viñeta anterior de CO 9.5 sobre la estimación repetida del contraste principal. +0,028 y +0,047 siguen en CO, pero pegados a otras afirmaciones (ventaja de la red; curva temporal), por eso el script no la echa de menos. Tampoco está en RD 8.8, a la que CO remite. `ENSAYO.md`, pregunta 21, la cita en CO 9.5 | "Ningún resultado se obtuvo en personas nuevas, y los análisis posteriores al 16-11-2026 son exploratorios o dirigidos (sección 9.1). El contraste principal de activación se estimó varias veces sobre las mismas personas, con diferencias entre +0,028 y +0,047, y no todos los intervalos excluyen el cero. El diseño de evaluación cambió después de un resultado nulo" | Importante |
| 2 | CO | 9.5 | "La lista completa, con sus cifras, está en la sección 8.8 de [[Borrador Resultados y Discusión 23-11-2026]]." | RD 8.8 ya no trae las cifras de varios límites (49 %, 25 % y 25 %; +0,055 y +0,001; −0,052; 66 %): dice de sí misma que "remite a la sección donde están sus cifras" | "La lista completa está en la sección 8.8 de [[Borrador Resultados y Discusión 23-11-2026]], que remite a las secciones donde están las cifras de cada límite." | Importante |
| 3 | CO | 9.5 | "La de atención es, en la práctica, conducta de mirada: la pupila pesa −0,052 en el *Modelo Profesor* de componente principal (PCA)." | CO anterior agregaba "y las variables de fijación suman la duración completa de las fijaciones que tocan la ventana". Desapareció de CO; sigue en RD 6.1 y 8.8 | "La de atención es, en la práctica, conducta de mirada: la pupila pesa −0,052 en el *Modelo Profesor* de componente principal (PCA), y las variables de fijación suman la duración completa de las fijaciones que tocan la ventana." | Importante |
| 4 | RD | 8.2 | "La etiqueta corregida por posición elimina ese efecto y la detección baja poco (0,675 frente a 0,683; sección 7.2)." | La versión anterior agregaba que la decisión registrada de ese contraste fue "inferior", por −0,008 y al filo. En la discusión queda "baja poco" sin la decisión registrada | "La etiqueta corregida por posición elimina ese efecto y la detección baja poco (0,675 frente a 0,683), aunque la decisión registrada de ese contraste fue "inferior", por −0,008 y al filo (sección 7.2)." | Importante |
| 5a | RD | 8.3 | "La detección de la etiqueta definida no está en duda." | Frase nueva y categórica. Las cifras son correctas, pero la detección se midió en 41 personas ya consultadas, con una sola versión de la etiqueta y con validación cruzada que separa personas y no grupos con el mismo orden de estímulos (8.8) | "La detección de la etiqueta definida es el resultado más estable de estos análisis, dentro de las 41 personas evaluadas y con los límites de la sección 8.8." | Importante |
| 5b | CO | 9.3 | "Lo que está en duda es el origen de esa detección, no la detección." | Misma lectura que 5a | "Lo que estos datos no permiten establecer es el origen de esa detección; la detección misma es estable en estas 41 personas." | Importante |
| 6 | RD | 8.8 | "Tres de ellas condicionan directamente las conclusiones del capítulo 9: ningún resultado se obtuvo en personas nuevas; la etiqueta de activación tiene un soporte temporal mayor que el nominal; y la etiqueta de atención se define con la conducta ocular, que el EEG también registra." | Frase nueva. "Ellas" son las cinco familias, pero se enumeran tres limitaciones. Además deja fuera el cambio de diseño tras el resultado nulo y la selección de la configuración, que CO 9.1 usa para condicionar el contraste principal, y contradice a CO 9.5 ("Cuatro grupos de límites condicionan estas conclusiones") | "Cinco limitaciones condicionan directamente las conclusiones del capítulo 9: ningún resultado se obtuvo en personas nuevas; el diseño con 41 personas se adoptó después de un resultado nulo; la configuración de activación la decidió el modelo con historial, con 25 de las 41 personas evaluadas; la etiqueta de activación tiene un soporte temporal mayor que el nominal; y la etiqueta de atención se define con la conducta ocular, que el EEG también registra." | Importante |
| 7a | RD | 8.1 | "Leído al pie de la letra, la ventaja de desempeño aparece en las dos (primera fila de la tabla siguiente)." | Frase nueva sobre la decisión 5. Es cierta solo con el segundo diseño; con el diseño planificado en un principio no hubo ventaja consistente en ninguna (6.3). Presenta dos lecturas del criterio cuando hay tres | "Leído al pie de la letra y con el segundo diseño, la ventaja de desempeño aparece en las dos (primera fila de la tabla siguiente); con el diseño original no aparecía de forma consistente en ninguna." | Importante |
| 7b | SP | 4.8.3 | "leído al pie de la letra, el criterio escrito daría otra respuesta, porque la ventaja de desempeño aparece en las dos variables." | Igual que 7a | "leído al pie de la letra y con el análisis de 41 personas, el criterio escrito daría otra respuesta, porque la ventaja de desempeño aparece en las dos variables; con las particiones originales no aparecía de forma consistente en ninguna." | Importante |
| 8 | RD | 7.4 | "Es un indicio secundario, no un resultado." | "Indicio" está en la lista de términos vetados del propio script del editor, que lo informa en esta línea | "Es una observación secundaria, no un resultado." | Menor |
| 9 | RD | 6.3 | "la curva temporal y la comprobación no registrada de la sección 7.2 usan una sola partición." | Incompleto: la misma comprobación no registrada se usa en 7.3 para activación. Las AUC estratificadas de la fase 2 sí promedian cinco particiones (`reapertura_fase2_41p/protocolo.json`) | "la curva temporal, con sus dos placebos, y la comprobación no registrada de las secciones 7.2 y 7.3 usan una sola partición." | Menor |
| 10 | RD | 6.2 | "el *placebo disperso*, formado por el mismo número de ventanas sueltas, y el *placebo de bloque*, formado por un bloque contiguo de ventanas;" | Hecho nuevo impreciso. `reapertura_41p_22-11-2026/INFORME.md`, línea 136: "El placebo iguala el número de ventanas de la banda de 6 s; en las demás bandas coincide en el 30–44 % de las filas" | "el *placebo disperso*, formado por ventanas sueltas, tantas como las de la banda de 6 s, y el *placebo de bloque*, formado por un bloque contiguo de ventanas;" | Menor |
| 11a | RD | 8.5 | "la detectabilidad de cada persona es estable entre las dos mitades de su sesión" | El informe de enfoques (línea 94) dice "dos mitades alternadas por orden temporal", no primera y segunda mitad. La imprecisión ya estaba en 7.7 anterior; la frase nueva la acentúa con "las dos" | "la detectabilidad de cada persona es estable entre dos mitades alternadas de su sesión" | Menor |
| 11b | RD | 7.11 | "La detectabilidad de cada persona es estable entre dos mitades de su sesión:" | Igual que 11a; heredado | "La detectabilidad de cada persona es estable entre dos mitades alternadas de su sesión:" | Menor |
| 12 | RD | 7.1 | "es la que conserva solo 26 ventanas con etiqueta (sección 4.5.2), de modo que su AUC es muy imprecisa." | SP 4.5.2 nombra a P4, pero no trae la cifra de 26 ventanas. Heredado. La cifra es correcta (`etiquetas.csv.gz`) | "es la que conserva solo 26 ventanas con etiqueta, de modo que su AUC es muy imprecisa." (o agregar la cifra a SP 4.5.2 y conservar la remisión) | Menor |
| 13 | SP | 4.6.1 | "Los valores por persona y por canal están en la sección 7.8 de [[Borrador Resultados y Discusión 23-11-2026]]." | RD 7.8 no trae valores por persona; trae rango, mediana, cuartiles y los dos grupos. Los valores por canal son de amplitud del parpadeo, no de desfase | "El rango, la mediana y los dos valores en que se agrupa el desfase están en la sección 7.8 de [[Borrador Resultados y Discusión 23-11-2026]]." | Menor |
| 14 | CO | 9.5 | "Se siguió con esa versión, y no con la de pesos iguales, tras observar que se predecía mejor, lo que no es un argumento de validez." | CO anterior daba la concordancia entre versiones (66 %). Salió de CO; está en RD 6.1 | "Esa versión coincide con la de pesos iguales en 66 % de las ventanas, y se siguió con ella tras observar que se predecía mejor, lo que no es un argumento de validez." | Menor |
| 15 | CO | 9.5 | "La configuración del modelo de activación se eligió con 25 de las 41 personas evaluadas y el contraste principal se concentra en ellas;" | CO anterior daba las cifras del 16-11 y el contrapeso. +0,046 y +0,021 están en 9.1; +0,055 y +0,001 ya no están en CO. La remisión a 7.5 funciona | "La configuración del modelo de activación se eligió con 25 de las 41 personas evaluadas y el contraste principal se concentra en ellas (+0,055 frente a +0,001 el 16-11; +0,046 frente a +0,021 con cinco particiones), aunque con las particiones originales el patrón había sido el inverso;" | Menor |
| 16 | CO | 9.5 | "La de activación es en lo esencial el nivel tónico de la GSR relativo a la sesión y su soporte real excede los 6 s:" | CO anterior daba el reparto del peso. La remisión a 6.1 funciona | "La de activación es en lo esencial el nivel tónico de la GSR relativo a la sesión y su soporte real excede los 6 s (en su parte tónica, el 49 % del peso de la GSR cae en las ventanas nominales, el 25 % antes y el 25 % después):" | Menor |
| 17a | `ENSAYO.md` | Pregunta 21, fuentes | "`Escritura/Borrador Conclusiones 23-11-2026.md` (vault), secciones 9.1 y 9.5." | CO 9.5 ya no contiene la estimación repetida (error 1) | Sin cambio si se aplica la corrección 1. Si no: "`Escritura/Borrador Resultados y Discusión 23-11-2026.md` (vault), secciones 7.1 y 8.4." | Menor |
| 17b | Minuta | Decisión 5 | (la tabla de opciones A y B) | RD 8.10 punto 5 dice ahora que la decisión "incluye con qué lectura del criterio de la hipótesis se llega a 'apoyo parcial'"; la minuta no lo menciona | Agregar a la decisión 5 una línea: "Incluye con qué lectura del criterio de la hipótesis se llega a "apoyo parcial" (RD 8.1)." | Menor |
| 18 | RD | Anexo de trazabilidad | "Los commits de registro, enmienda y resultados de cada etapa están en `documentacion/Cierre_Experimental_Final_23-11-2026.md`." | La limitación "la comprobación de reproducibilidad verifica hashes y no reentrena" pasó de 8.8 a una nota de trabajo que no va en la tesis. El informe editorial (P14) pedía llevarla al anexo | "Los commits de registro, enmienda y resultados de cada etapa están en `documentacion/Cierre_Experimental_Final_23-11-2026.md`. La comprobación de reproducibilidad del cierre verifica hashes y el orden del registro; no vuelve a entrenar los modelos." | Menor |
| 19 | RD | 8.5 | "esa lectura es una hipótesis que este trabajo no puso a prueba." | DF anterior agregaba "y cuya base anatómica falta confirmar en el texto completo"; ahora solo está en la nota de trabajo. `VERIFICACION_REFERENCIAS.md`, corrección 3, pide eliminar la cláusula anatómica si no se confirma | "esa lectura es una hipótesis que este trabajo no puso a prueba y cuya base anatómica no se confirmó en la fuente." | Menor |
| 20 | RD | 7.2 | "Este resultado es compatible con el del control de posición, porque se comparan con modelos distintos. Frente al modelo que ya recibe la posición, el historial agrega +0,004 [−0,001; +0,009] a igual posición, −0,003 [−0,007; +0,002] dentro del mismo estímulo y −0,004 [−0,008; +0,001] dentro del mismo minuto; es una comprobación no registrada, hecha después de ver los resultados y con una sola partición." | Antes la compatibilidad era lo que "mostró" la comprobación no registrada; ahora se afirma primero y sin condición | "Este resultado no contradice el del control de posición, porque se comparan con modelos distintos; así lo indica una comprobación no registrada, hecha después de ver los resultados y con una sola partición: frente al modelo que ya recibe la posición, el historial agrega +0,004 [−0,001; +0,009] a igual posición, −0,003 [−0,007; +0,002] dentro del mismo estímulo y −0,004 [−0,008; +0,001] dentro del mismo minuto." | Menor |
| 21a | RD | 7.8 | "esto respalda la división usada, pero no reemplaza la documentación del experimento." | "Respaldo" reservado para la regla registrada. Heredado | "esto es coherente con la división usada, pero no reemplaza la documentación del experimento." | Menor |
| 21b | SP | 4.7 | "lo que respalda distinguir zonas, pero no reemplaza la documentación" | Igual que 21a | "lo que es coherente con distinguir zonas, pero no reemplaza la documentación" | Menor |
| 21c | SP | 4.5.2 | "no permiten respaldar ni rechazar la hipótesis." | Igual que 21a | "no permiten sostener ni rechazar la hipótesis." | Menor |
| 22 | RD | 7.5, fuentes | "Fuentes: `resultados/cierre_v3_16-11-2026/INFORME.md`, `resultados/cierre_final_41p_16-11-2026/INFORME.md`, `resultados/cierre_robustez_41p_16-11-2026/INFORME.md`, `resultados/reapertura_41p_22-11-2026/INFORME.md`, `documentacion/auditoria_final_23-11-2026/recalculo.json` (recálculo de la auditoría final)." | Es copia de la línea de 7.1. La tabla de 7.5 usa además la enmienda del historial desplazado, el control de posición del 18-11 y la fase 3 | "Fuentes: `resultados/cierre_v3_16-11-2026/INFORME.md`, `resultados/cierre_final_41p_16-11-2026/INFORME.md`, `resultados/cierre_robustez_41p_16-11-2026/INFORME.md`, `resultados/ampliacion_41p_16-11-2026/INFORME.md`, `resultados/explicativo_posicion_41p_18-11-2026/INFORME.md`, `resultados/reapertura_41p_22-11-2026/INFORME.md`, `resultados/reapertura_fase3_41p_22-11-2026/INFORME.md`, `documentacion/auditoria_final_23-11-2026/recalculo.json` (recálculo de la auditoría final)." | Menor |
| 23 | RD | 6.4 | "En la discusión los contrastes se nombran por su contenido." | 8.8 usa "A1 y A3" y "R1" | "En la discusión los contrastes se nombran por su contenido, con el código entre paréntesis cuando ayuda a ubicarlos." | Menor |
| 24 | RD | 8.4, título | "### 8.4 Activación: el historial reciente supera al placebo, con alcance de segundos" | Reemplaza a "indicio de información temporal de corto alcance". "Con alcance de segundos" puede leerse como un alcance establecido; solo hay respaldo a 6 s y dentro del soporte del filtro tónico | "### 8.4 Activación: el historial reciente supera al placebo, con respaldo solo a 6 s" | Menor |

## Observaciones que no son errores

- RD 7.8: "cada ventana de EEG contendría actividad" pasó a "contiene". SP 4.6.1 ya lo decía en indicativo y la dirección se comprobó en el script; lo dejo anotado por si se prefiere conservar el condicional mientras la estimación sea "poco segura en las personas con acoplamiento bajo".
- RD 8.2: "sino del tiempo transcurrido en el estímulo" es más directa que la versión anterior. La sostienen el control de posición (+0,028 con la posición sola; nulo concluyente del historial sobre ella), y el párrafo siguiente conserva "la lectura más coherente" para el origen del patrón.
- RD 8.6 ya no repite las cifras de fusión, y 8.7 ya no trae la viñeta de sincronía; ambas cosas están en 7.6, 7.8, 8.8 y 8.9.
- Las columnas "Mejoran" y "A favor" conviven en el capítulo 7 (7.1, 7.2 y la tabla de adaptación de 7.11 dicen "Mejoran"). No cambia ninguna cifra.
- CO habla de "cuatro grupos de límites" y RD de "cinco familias"; no es una contradicción, pero conviene que la frase de RD 8.8 (error 6) y la de CO 9.5 digan lo mismo.
- `ENSAYO.md`, pregunta 13, dice "el efecto es pequeño y desigual entre personas" con fuente en CO 9.7, que ahora atribuye "desigual" solo al contraste simple.
- El script del editor informa "NUEVA p|p:0,0004": no es una cifra nueva; es el p de Holm de la tabla de adaptación, citado ahora en la prosa de 8.5.
