# Auditoría independiente del experimento — 23-11-2026

Alcance: las 12 etapas experimentales del 16 al 23-11-2026 de la tabla "Trazabilidad" de `documentacion/Cierre_Experimental_Final_23-11-2026.md`, ese cierre y `Escritura/Borrador Conclusiones 23-11-2026.md`.

Hecha por un agente independiente con código propio (`auditar_experimento.py`, en esta carpeta). El script no importa ningún script del repositorio: reimplementa la AUC por rangos, el bootstrap sobre personas, la permutación de signos, Holm y la regla de decisión, y reconstruye estímulo, minuto de sesión y posición desde la tabla de ventanas del preprocesamiento. No se entrenó ni se relanzó ningún modelo, no se modificó ningún archivo existente y no se hicieron commits ni push.

## Veredicto global

**Los números se reproducen. Las lecturas van, en varios puntos, más lejos que los números.**

- **Cifras:** 2.638 valores comparados contra los CSV. Ninguna discrepancia. Las AUC por persona, las diferencias pareadas, el número de personas a favor, las etiquetas de decisión y los Holm coinciden; los intervalos y los valores p difieren solo por la semilla de remuestreo (IC: 0,002 como máximo; p: 0,004 como máximo) y ninguna decisión cambia.
- **Integridad:** 429 comprobaciones, 428 correctas. La única que falla es la ya documentada (hash de `scripts/limpieza_ocular_41p.py`, enmienda v2).
- **Documentos:** 122 cifras del cierre y de las conclusiones contrastadas con su CSV: 119 coinciden y 3 tienen un error de redondeo en el tercer decimal.
- **Hallazgos bloqueantes:** ninguno.
- **Hallazgos importantes:** 6, todos de interpretación en el cierre y en el borrador de conclusiones. Ninguno cambia una cifra; sí cambian frases.

## Qué se comprobó con código y qué solo se leyó

| Comprobado con código | Solo leído o no verificable |
|---|---|
| AUC por persona, diferencia media, IC 95 % y 90 %, p, Holm, personas a favor y decisión de todos los contrastes confirmatorios y de casi todos los descriptivos con predicciones guardadas | Que las predicciones salgan de la configuración declarada: exige reentrenar |
| AUC estratificadas (estímulo, minuto, posición), con estratos reconstruidos de forma independiente | Qué personas entraron al ajuste de cada modelo: las predicciones solo muestran el fold de evaluación |
| Mismas ventanas, personas y etiquetas entre modelos pareados y entre etapas; sin duplicados, NaN ni valores fuera de [0, 1] | Fuga dentro de las variables (normalizaciones por sesión): declarada como límite, no auditable desde predicciones |
| Cada persona evaluada en un solo fold, igual al del protocolo; folds del protocolo disjuntos | Importancias por bloques (E5 de la ampliación): solo se comprobó la agregación de los valores guardados |
| Hashes de los 289 archivos registrados (196 entradas, 82 crudos en caché, 3 tensores, 8 tablas de variables): 288 coinciden | E6 por tipo de página, correlatos E4b, kappa de la etiqueta corregida, correlaciones de Spearman con el puntaje ocular, calidad de la limpieza: no recalculados |
| Orden en Git: protocolo antes que predicciones en las 12 etapas; fechas locales de los archivos | Que el protocolo se *publicara* (push) antes de correr: Git solo guarda la hora del commit |
| Montaje: cifras del informe contra sus CSV (27 de 41, 31 de 37, desfase) | Montaje desde los crudos; auditorías de código "antes de ver resultados" |

## Veredicto por etapa

| Etapa | Veredicto | Comparaciones | Nota |
|---|---|---|---|
| Cierre V3 (`cierre_v3_16-11-2026`) | **Reproduce** | 432 | 54 contrastes y 54 AUC en train, validación y test. La regla registrada (IC 95 % sobre 0 en validación y test) da "sin ventaja consistente" en los cuatro principales, como informa |
| Análisis final (`cierre_final_41p_16-11-2026`) | **Reproduce con diferencias menores** | 138 | Principal y secundarios exactos. `heterogeneidad_por_grupo.csv` no está en el protocolo ni en el script; sus IC no se reproducen con la semilla registrada (diferencia máxima 0,0013) |
| Robustez (`cierre_robustez_41p_16-11-2026`) | **Reproduce** | 68 | R1, R2 y R3 exactos. El informe dice "+0,042 en las tres" particiones; son +0,043, +0,042 y +0,042 |
| Ampliación E1–E6 (`ampliacion_41p_16-11-2026`) | **Reproduce con diferencias menores** | 219 | E1 a E4 reproducidos. Tres redondeos dobles en el informe. E5 no recalculable; E6 no recalculado |
| Enmienda E1 a 6 ventanas (`enmienda_e1_lag6`) | **Reproduce** | 26 | Un redondeo doble en el informe |
| Explicativo de posición (`explicativo_posicion_41p_18-11-2026`) | **Reproduce** | 56 | Un redondeo doble |
| Reapertura, fase 1 (`reapertura_41p_22-11-2026`) | **Reproduce con diferencias menores** | 308 | Confirmatoria, curva, tendencia, D1 y D2 reproducidos. Tres redondeos dobles; uno llega al cierre y a las conclusiones |
| Reapertura, fase 2 (`reapertura_fase2_41p_22-11-2026`) | **Reproduce** | 386 | X1, X2 (los tres estratos) y la comprobación no registrada. Cuatro redondeos dobles |
| Reapertura, fase 3 (`reapertura_fase3_41p_22-11-2026`) | **Reproduce** | 380 | Q1, Q2, sensibilidad y los 4 ámbitos descriptivos. Dos redondeos dobles |
| Cuatro enfoques (`enfoques_41p_22-11-2026`) | **Reproduce con diferencias menores** | 267 | Las 18 filas confirmatorias. `c32_pos` es idéntico a `hgb_c32` (ver M2). Dos redondeos dobles |
| Montaje (`montaje_ocular_41p_23-11-2026`) | **No se pudo comprobar desde los crudos**; coherencia interna correcta | 4 | Es descriptivo y no tiene predicciones. Las cifras del informe coinciden con sus CSV |
| Limpieza ocular (`limpieza_ocular_41p_23-11-2026`) | **Reproduce** | 258 | L1 a L4, 16 AUC por persona, curva, subconjuntos y sensibilidades. Dos redondeos dobles; uno llega al cierre |
| Red sobre la señal cruda (`red_cruda_41p_23-11-2026`) | **Reproduce** | 96 | R1 a R4. Dos redondeos dobles en los IC de las AUC |

Detalle fila por fila en `comparaciones.csv`, `integridad.csv` y `coherencia_documentos.csv`.

## Integridad (punto 2)

- **Personas.** 41 en todas las etapas; 40 en la curva temporal de activación y en la adaptación de activación, como se declara. En el cierre V3: 25, 8 y 8, sin solapamiento.
- **Ventanas.** 22.176 de atención y 11.796 de activación en todos los modelos y particiones; 12.613 y 6.268 en la curva, iguales a `cobertura_*.json`.
- **Etiquetas.** Idénticas entre modelos pareados y entre las 12 etapas. Dos excepciones por diseño: la etiqueta corregida de E1 (cambia el 9,36 % de las ventanas) y R2 de robustez (profesor reajustado).
- **Ajuste y evaluación.** Cada persona aparece en un solo fold de evaluación por partición y ese fold es el del protocolo. Los folds del protocolo son disjuntos. En el cierre V3 la validación interna sale siempre del ajuste.
- **Registro.** En las 12 etapas el commit del protocolo es anterior al de las predicciones, y la fecha local de la primera predicción es posterior a `created_utc` del protocolo.
- **Adaptación (E4c).** Ninguna fila de evaluación cae antes del 41 % de la sesión.

## Protocolo frente a lo informado (punto 3)

Los contrastes confirmatorios informados son los registrados en las 11 etapas con protocolo, con la familia de Holm declarada. Lo que aparece en los informes sin estar en el protocolo:

| Etapa | Contenido no registrado | ¿Rotulado? |
|---|---|---|
| Análisis final | Heterogeneidad por grupo (25 de train frente a 16 de validación y test) | **No** |
| Reapertura, fase 1 | Sensibilidad a personas individuales | Sí ("no estaba registrada") |
| Reapertura, fase 2 | Estratos con la posición como variable | Sí ("comprobación no registrada") |
| Cuatro enfoques | "En el modelo adaptado el historial aporta +0,058" y la ganancia del historial en las mismas filas | **No** (la lista de descriptivos del protocolo solo nombra E4a y E4b) |
| Red sobre la señal cruda | Robustez por partición y dejando una persona fuera | Sí ("auditoría de resultados") |

El explicativo de posición y la fase 2 están rotulados como post hoc. El explicativo no fija regla de decisión ni corrección.

## Tabla de discrepancias (punto 4)

Todas son del tercer decimal. Casi todas tienen el mismo origen: el valor se redondeó a 4 decimales al imprimirlo y otra vez a 3 al escribir el informe. Ninguna cambia una decisión. La columna "Recalculada" usa mi propia semilla: en las diferencias medias es exacta; en los límites de IC se mueve ±0,0005 según la semilla, así que estas diferencias son menores que el ruido del propio remuestreo (en la fila 4 mi semilla da el valor informado).

| # | Archivo | Cifra | Informada | En el CSV | Recalculada | Tipo |
|---|---|---|---|---|---|---|
| 1 | INFORME de la reapertura; **cierre** (tabla general y fase 1); **conclusiones** 9.1 | Activación, 6 s − placebo, IC 95 % inferior | +0,018 | 0,017474 | 0,0174 (0,0171 a 0,0182 con 20 semillas) | Redondeo doble: es +0,017 |
| 2 | INFORME de limpieza; **cierre** (23-11) | L1, IC 95 % inferior | +0,045 | 0,044497 | 0,0447 (0,0442 a 0,0448) | Redondeo doble: es +0,044 |
| 3 | INFORME de limpieza | L4, IC 95 % superior | −0,033 | −0,032476 | −0,0323 | Redondeo doble |
| 4 | INFORME de ampliación | E1 con 5 ventanas, activación, IC inferior | +0,013 | 0,012484 | 0,0130 | Redondeo doble |
| 5 | INFORME de ampliación | E3 atención, intermedia − tardía | −0,008 | −0,007453 | −0,00745 (exacta) | Redondeo doble |
| 6 | INFORME de ampliación | E3 activación, tardía − temprana | +0,007 | 0,006462 | 0,00646 (exacta) | Redondeo doble |
| 7 | INFORME de ampliación (enmienda) | E1 con 6 ventanas, atención, real − placebo | −0,003 | −0,002493 | −0,00249 (exacta) | Redondeo doble |
| 8 | INFORME del explicativo | Activación, posición − sin historial, IC inferior | −0,024 | −0,023483 | −0,0238 | Redondeo doble |
| 9 | INFORME de la reapertura | Curva, atención 48 s − placebo | −0,013 | −0,012461 | −0,01246 (exacta) | Redondeo doble |
| 10 | INFORME de la reapertura | Curva, atención 96 s, IC superior | −0,004 | −0,003450 | −0,0034 | Redondeo doble |
| 11 | INFORME de la reapertura (fase 2) | X1 atención 96 s, IC superior | −0,003 | −0,002469 | −0,0024 | Redondeo doble |
| 12 | INFORME de la reapertura (fase 2) | X1 activación 24 s − bloque | +0,010 | 0,009467 | 0,00947 (exacta) | Redondeo doble |
| 13 | INFORME de la reapertura (fase 2) | X2 atención, mismo estímulo, IC inferior | +0,007 | 0,006460 | 0,0063 | Redondeo doble |
| 14 | INFORME de la reapertura (no registrada) | Activación, misma posición, historial − posición | +0,028 | 0,027477 | 0,02748 (exacta) | Redondeo doble |
| 15 | INFORME de la fase 3 | Activación, mismo estímulo, historial − (actual + posición), IC inferior | −0,026 | −0,025491 | −0,0254 | Redondeo doble |
| 16 | INFORME de la fase 3 | Activación, igual posición, IC superior | +0,052 | 0,051468 | 0,0514 | Redondeo doble |
| 17 | INFORME de enfoques | B1, IC inferior | +0,165 | 0,164452 | 0,1646 | Redondeo doble |
| 18 | INFORME de enfoques (tabla E4c) | Adaptación de activación sin historial, p Holm | 0,050 | 0,049455 | 0,0490 | Redondeo doble. La tabla muestra 0,050 junto a "Respaldo"; el texto del mismo informe dice 0,049 |
| 19 | INFORME de la red | AUC HGB con EEG original, IC inferior | 0,665 | 0,664452 | no recalculada (solo la media: 0,6809) | Redondeo doble |
| 20 | INFORME de la red | AUC HGB solo EEG en activación, IC superior | 0,551 | 0,550493 | no recalculada (solo la media: 0,5237) | Redondeo doble |
| 21 | INFORME de robustez | Activación R3 | "+0,042 en las tres" | 0,0432; 0,0416; 0,0416 | iguales | Texto impreciso; la tabla del mismo informe dice "+0,042 a +0,043" |
| 22 | INFORME de limpieza (lectura y límites) | Desfase entre EEG y seguidor ocular | 0,25–0,5 s | 0,184 a 0,528 (`personas.csv` del montaje); 0,232 a 0,544 (`personas_limpieza.csv`) | iguales | Incoherencia entre informes; el cierre usa 0,18 a 0,53 |
| 23 | `heterogeneidad_por_grupo.csv` | 16 límites de IC | p. ej. 0,1005 | — | 0,1002 con la semilla registrada | No reproduce exactamente; diferencia máxima 0,0013. Su código no está versionado |

**Sobre 0,046 frente a 0,047.** No es un error: son contrastes distintos y ambos están bien transcritos.

| | +0,046 [+0,018; +0,073] | +0,047 [+0,017; +0,078] |
|---|---|---|
| Etapa | Enmienda E1 de la ampliación (16-11) | Curva temporal de la reapertura (22-11) |
| Historial | Hasta 32 ventanas del mismo estímulo, sin las 6 más recientes | Ventanas entre 6 y 12 s antes, sin importar el estímulo |
| Personas | 41 (28 a favor) | 40 (30 a favor) |
| Holm | 2 tareas, p 0,004 | 5 desfases, p 0,017 |

El cierre usa cada cifra en su fila. Las conclusiones (9.1) usan +0,047 con una descripción que corresponde a la curva.

## Hallazgos por gravedad

### Bloqueantes

Ninguno.

### Importantes

**I1. La ventaja de la red no es "también ocular": no cambia de forma demostrable al limpiar.**
- Cierre, tabla general: "su ventaja también es ocular". Conclusiones 9.3: "La ventaja de la red también disminuye al limpiar la señal".
- La ventaja sobre el HGB es +0,035 con el EEG original (R1) y +0,028 con el EEG limpio (R2, respaldo).
- Recalculé la diferencia entre ambas, que no estaba registrada: **+0,007 [−0,005; +0,020], p 0,29, 20 de 41 personas**. El IC 90 % [−0,003; +0,018] queda dentro de ±0,02: con la regla del propio proyecto sería un nulo concluyente.
- Lo que sí está respaldado: la red pierde 0,067 al limpiar (R3), sin control propio. Eso dice que la *detección* de la red depende de lo ocular, no que su *ventaja* sobre el HGB lo sea. El 80 % de la ventaja se mantiene.

**I2. "Sobre todo conducta ocular" excede lo medido.**
- Cierre: "Sobre todo la conducta ocular: 0,681, que baja a 0,621". Conclusiones 9.3: "corresponde sobre todo a la huella eléctrica de los movimientos oculares y los parpadeos".
- La limpieza quita 0,060 de los 0,181 que el modelo tiene sobre el azar: **un tercio**. Quedan 0,121 sobre el azar en 41 de 41 personas (L3, efecto relevante).
- Que el resto también sea ocular es una inferencia a partir del patrón residual. El informe de limpieza lo dice: "el diseño no los separa".
- Redacción que la evidencia sostiene: al menos un tercio de la detección depende de componentes oculares; del resto no se puede afirmar origen cerebral ni ocular. Las conclusiones 9.7 ("en gran parte") y el límite "0,060 es una cota inferior" son más cuidadosos que la frase principal.

**I3. El efecto temporal en activación se afirma con más firmeza que la que dan los datos.**
- Conclusiones 9.1: "La mejora corresponde a información temporal". 9.7: "La temporalidad aporta a la detección de la activación". Informes de la reapertura y de la fase 3: "efecto del historial **confirmado**". Cierre: "Fase 1, confirmatoria".
- El contraste principal se estimó nueve veces sobre las mismas 41 personas. Recalculado por partición:

| Partición | ΔAUC | IC 95 % | p |
|---|---|---|---|
| 16-11, registrada | +0,034 | [−0,001; +0,070] | 0,065 |
| 16-11, R3 (tres) | +0,042 a +0,043 | inferior entre +0,006 y +0,013 | 0,008 a 0,028 |
| 22-11, 1101 | +0,034 | [−0,001; +0,072] | 0,078 |
| 22-11, 1102 | +0,041 | [+0,011; +0,072] | 0,013 |
| 22-11, 1103 | +0,047 | [+0,013; +0,085] | 0,013 |
| 22-11, 1104 | +0,032 | [+0,003; +0,062] | 0,042 |
| 22-11, 1105 | +0,028 | [−0,001; +0,061] | 0,085 |

- El signo es estable; la significación no (3 de 9 intervalos incluyen el cero). El "respaldo" de la fase 1 sale de promediar cinco particiones cuando ya se conocían las tres de R3, como declara su protocolo. Es una estimación más precisa de lo ya visto, no una confirmación.
- El efecto es desigual: media +0,036, **mediana +0,014**, 23 de 41 personas.
- Los controles que separarían "información temporal" de otras explicaciones quedaron inconclusos: tiempo de sesión (+0,026 [−0,006; +0,056]), posición como variable (+0,032, p Holm 0,108) y dentro del mismo estímulo (+0,009 [−0,020; +0,037]).
- El apoyo más sólido es otro: el historial sin los 6 s de la etiqueta frente a placebo (+0,046, p Holm 0,004, principal registrado antes de correr; +0,047 en la curva). Tiene su propio límite, declarado: el 73 % de esas ventanas pertenece al mismo estímulo.
- El cierre usa "respaldo" y declara que nada es confirmación independiente. Los dos informes y el borrador de conclusiones deberían usar el mismo lenguaje.

**I4. "De 6 a 12 s" y "desaparece desde 24 s" no están demostrados.**
- Cierre: "La información está en los 6 a 12 s anteriores […] y desaparece desde 24 s". Conclusiones 9.1: "se concentra en los 6 a 12 s anteriores y desaparece desde los 24 s".
- Solo la banda de 6 s tiene respaldo. La de 12 s es inconclusa: +0,024 [−0,011; +0,059], p Holm 0,68.
- De 24 a 96 s los resultados son inconclusos, no nulos: ningún IC 90 % cabe en ±0,02 (24 s: [−0,028; +0,036]; 96 s: +0,019 [−0,017; +0,054]). Leerlos como "desaparece" es tomar un nulo por equivalencia sin cumplir la regla.
- La tendencia decreciente (−0,010 por duplicación, p 0,009) es una sola prueba sin ajuste.
- Mismo problema en el cierre: "dentro de un mismo estímulo se explica por el tiempo transcurrido". Se apoya en un descriptivo y en Q2, inconcluso y con poca potencia; el informe de la fase 3 advierte que "no demuestra ausencia de efecto".

**I5. La conclusión sobre fusión depende de la familia de modelos y solo se cita un lado.**
- Cierre: "¿Qué fusión? Tardía sobre temprana: +0,012". Conclusiones 9.2: "La fusión tardía superó a la temprana en atención".
- Ese +0,012 [+0,005; +0,021] es un secundario sin corrección, entre redes MLP. Resiste un Holm propio sobre los 6 contrastes de E3 (p 0,007).
- Con HGB, en el cierre V3, el signo es el contrario: tardía − temprana **−0,010 [−0,018; −0,003]** en train (7 de 25), −0,008 en validación y −0,002 en test. El informe de V3 concluye que la tardía "no supera a la temprana en ninguna tarea".
- La red con fusión tardía rinde **0,024 menos** que el HGB con fusión temprana sobre la misma representación: 0,686 frente a 0,710, [−0,038; −0,012].
- La frase "La fusión no es, entonces, el factor que explica el desempeño" no se sigue de ningún contraste.

**I6. El aporte de cada señal en activación (9.2) descansa en un descriptivo ruidoso y contradice otros resultados.**
- Conclusiones 9.2: "En activación aportan el EEG y el historial, la pupila en menor medida, y la mirada no aporta".
- Proviene de E5 (caída de AUC al permutar bloques): EEG 0,053 ± 0,075, media del historial 0,050 ± 0,053, pupila 0,021 ± 0,027 entre 8 folds. La desviación supera a la media en los tres. Es descriptivo, permuta filas entre personas y no se pudo recalcular.
- Contradice 9.3 del mismo borrador: el EEG de la ventana actual "no detecta el *Arousal Score* de forma demostrable" (0,524, p 0,09).
- Contradice un descriptivo de la red cruda: (EEG + mirada + pupila) − solo EEG = **−0,006 [−0,022; +0,009]**, IC 90 % dentro de ±0,02. En la ventana actual, pupila y mirada no agregan nada.
- En el cierre, la fila "¿Ayuda un modelo más complejo? Activación: No" tiene un problema parecido: R4 es inconcluso y el informe de la red excluye expresamente esa lectura (una sola arquitectura, sin búsqueda).

### Menores

**M1. Redondeo doble sistemático** (filas 1 a 20 de la tabla). Tres casos llegan al cierre o a las conclusiones: +0,018 por +0,017 (dos veces) y +0,045 por +0,044.

**M2. En E1, `c32_pos` es idéntico a `hgb_c32`.** Las 110.880 predicciones coinciden bit a bit. Consecuencias:
- A3 ("historial + posición" − "actual + posición") es numéricamente `hgb_c32 − pos_c1`, y la fila "AUC c32_pos" de `e1_descriptivos.csv` repite la de `hgb_c32`.
- Lo más probable es que el modelo nunca use la columna de posición cuando la etiqueta ya está corregida por posición. En la fase 3 pasa lo mismo en el 78 % de las predicciones de activación, y en ninguna de atención con la etiqueta original.
- No se puede descartar un error sin reentrenar un fold. La cifra de A3 no cambia; ni el informe ni la auditoría anterior lo mencionan.

**M3. Decisiones al filo y regla asimétrica.**
- E1: A1 ("inferior") y A3 ("nulo concluyente") tienen p Holm 0,055 (0,054 recalculado). Con 0,049, A3 sería "respaldo", porque su IC 95 % excluye el cero ([+0,000; +0,009]).
- La regla exige Holm para "respaldo" pero no para "inferior". Por eso A1 es "inferior" con p Holm 0,055, y la banda de 24 s de atención figura como "inferior" en el CSV con p Holm 0,16 (el informe deja esa celda sin rótulo).
- El cierre dice de E1 que "la detección se conserva (0,675 frente a 0,683)"; la decisión registrada para esa prueba es "inferior" (−0,008 [−0,015; −0,001]).
- Adaptación de activación sin historial: p Holm 0,049.

**M4. "Efecto relevante" en atención supera el margen por 0,001.** IC 95 % inferior 0,021 con cinco particiones (0,0211 a 0,0214 según la semilla). Por partición va de 0,019 a 0,021; el 16-11 fue 0,018 ("respaldo"). El margen de 0,02 no está aprobado. Tiene poca consecuencia: esa mejora se atribuye a la posición.

**M5. Heterogeneidad por grupo** (análisis final): no registrada, no rotulada, sin código versionado y con IC que no se reproducen exactamente.

**M6. Explicativo de posición:** destaca en negrita "+0,038 [+0,002; +0,074]" para activación y concluye que "el contenido del historial sí" aporta. Es p 0,044 sin ajuste en un análisis post hoc; con Holm sobre sus 6 contrastes, 0,17.

**M7. Informe de robustez sin actualizar.** Atribuye la mejora de atención a "contexto de la persona (una especie de calibración individual)". E2 de la ampliación (+0,001 a +0,004) y el explicativo lo desmintieron después. El informe del análisis final tiene una nota de actualización; el de robustez no.

**M8. Cronología.** El registro previo se verifica en las 12 etapas. Tres notas:
- La enmienda E1 se registró el 16-11 a las 14:25, antes de las primeras predicciones de la ampliación (14:49). Su corrida es del 18-11 a las 21:39, dos días después de existir las predicciones con 5 ventanas. El registro es válido; "antes de ver resultados" vale para el registro, no para la ejecución.
- El protocolo del explicativo se confirmó 53 s después de escribirse `contrastes.csv` de la ampliación. Es coherente con su rótulo post hoc.
- "Se publicó antes de correr" no es verificable desde el repositorio.

**M9. Montaje.** "El desfase […] es positivo en las 41 personas" vale para parpadeo y mirada horizontal. Con la mirada vertical no es positivo en 4 personas (mínimo −0,81 s), todas con acoplamiento débil.

**M10. Redacción en conclusiones 9.3:** "un control que retira 72 % de la varianza no ocular". El control retira componentes no oculares que suman el 72 % de la varianza total (mediana).

**M11. Lecturas sin contraste en el informe de enfoques.** "La activación es un estado del estímulo completo más que de cada ventana" (C2 es inconcluso). "Rasgo estable" es fiabilidad por mitades dentro de una sola sesión.

**M12. Límites que faltan en el borrador de conclusiones** y sí están en el cierre: los secundarios no llevan corrección; el explicativo y la fase 2 son post hoc; la pérdida de la red al limpiar no tiene control; el contraste principal de activación fue inconcluso en la partición registrada.

**M13. GRU en activación.** El secundario GRU con historial − GRU sin historial (+0,051 [+0,021; +0,080], p 0,002) resiste un Holm propio sobre los 6 secundarios (0,008). No contradice las conclusiones: mide el aporte del historial en la GRU, no el del orden; el contraste específico del orden (GRU − HGB, +0,020) es inconcluso.

## Notas de proceso

- A las 18:54, otro proceso hizo el commit `7b46b67`, que incluyó una versión intermedia de `auditar_experimento.py`, `comparaciones.csv`, `integridad.csv` y `recalculo.json`. Las versiones finales, este informe, `coherencia_documentos.csv` y `redondeos_candidatos.csv` quedan sin confirmar en el árbol de trabajo.
- `AGENTS.md` pide commit y push al cerrar cada etapa. No se hizo porque el encargo de esta auditoría lo excluye.
- El script tarda unos 25 s. Para repetirlo: `.venv/bin/python documentacion/auditoria_final_23-11-2026/auditar_experimento.py`.
