# Auditoría del borrador de Resultados y Discusión — ronda 2 (26-11-2026)

Objeto: `documentos/01 Tesis MDS/Escritura/Borrador Resultados y Discusión 23-11-2026.md` (capítulos 6, 7 y 8).

Hecha por un agente independiente. No se editó ningún archivo existente, no se entrenó ningún modelo y no se hicieron commits. Fuentes de verdad: los CSV de `resultados/<etapa>/` (redondeados a 3 decimales desde el valor completo, redondeo "mitad hacia arriba" con `Decimal`) y, en segundo lugar, los `INFORME.md`, `protocolo.json` y la auditoría del 23-11 (`AUDITORIA_EXPERIMENTO.md`, `recalculo.json`). Dos comprobaciones se recalcularon desde las predicciones guardadas: la prevalencia de atención alta por posición en el estímulo y la coincidencia entre las particiones del 16-11 y las del 22-11.

## 1. Resumen

- **Cifras revisadas:** unas 1.015 cifras en los capítulos 6 a 8 (AUC, diferencias, límites de intervalo, p, conteos, porcentajes, correlaciones y parámetros; sin contar fechas, rutas ni números de sección).
- **Coinciden con la fuente:** unas 990.
- **Difieren:** 24. De ellas, 19 son del tercer decimal (redondeo doble heredado de los INFORME; el borrador ya corrige dos casos, +0,017 y +0,044, y deja los demás) y 5 son de fondo: el porcentaje de corrimiento de las ventanas (2 cifras), la prevalencia "0,62 hacia los 12 s" y la afirmación, en dos secciones, de que tres de las cinco particiones del 22-11 ya se habían visto.
- **Sin CSV, respaldadas solo por INFORME o protocolo:** unas 25 (pesos del *Attention Score*, 73 %/48 %/13 %/0 % de mismo estímulo, 0,0199 de R1, "0,009 de los 0,036", 1.217 parámetros, mediana de 3 ventanas, entre otras). Todas coinciden con su INFORME.
- **Sin fuente localizable:** 2 afirmaciones (8.5 "la navegación web produce un rango de activación estrecho"; 8.8 "la redacción actual del manuscrito pide normalizar solo con entrenamiento", manuscrito no disponible en este espacio).
- **Decisiones:** todas las etiquetas de decisión (respaldo, efecto relevante, nulo concluyente, inferior, inconcluso) coinciden con la columna `decision` de su CSV. Ninguna discrepancia de cifras cambia una decisión.
- **Rótulos de registro:** coinciden con los `protocolo.json`, con tres omisiones (heterogeneidad por grupo, "+0,058" de la adaptación, sensibilidades de la curva) y una frase general que las contradice (6.3).
- **Hallazgos de la auditoría del 23-11:** I1, I2, I4, I5 e I6 están bien incorporados. I3 está incorporado, pero con un error de hecho sobre las particiones. M13 (orden frente a historial en la GRU) no está incorporado en la tabla 8.1. M2 y M5 no se mencionan.
- **Citas:** las 17 citas del borrador existen en la lista de referencias de la discusión fisiológica; "10 en texto completo y 8 por resumen" coincide con `VERIFICACION_REFERENCIAS.md`. Una atribución sigue excediendo a su fuente (Goncharova et al., 2003) y dos conservan un matiz pendiente (Iwasaki, Dimigen).
- **Rutas y enlaces:** todas las rutas de "Fuentes:" y los seis enlaces internos existen.

**Bloqueantes: 0. Importantes: 12. Menores: 17 de redondeo, 11 de lectura y 9 de forma.**

## 2. Importantes

### 2.1 Discrepancias de cifras y hechos

| # | Sección | Texto actual exacto | Fuente | Corrección exacta |
|---|---|---|---|---|
| I-1 | 6.4, fila "Reapertura, fase 1" | `Se hizo sobre personas ya consultadas y tres de las particiones del contraste de activación ya se habían visto: no es una confirmación independiente` | `reapertura_41p_22-11-2026/protocolo.json` (`folds_rep` 1101–1105; `limits`: "tres particiones alternativas ya se habían visto en la prueba de robustez R3") y `cierre_robustez_41p_16-11-2026/protocolo.json` (`folds_r3` 101, 202, 303). Comparadas: ningún grupo en común entre las 3 del 16-11 y las 5 del 22-11. Además contradice 6.3 y 7.1 del propio borrador ("5 particiones nuevas") | `Se hizo sobre personas ya consultadas y con el contraste de activación ya visto en tres particiones alternativas el 16-11 (las cinco particiones del 22-11 son nuevas y no comparten ningún grupo con aquellas): no es una confirmación independiente` |
| I-2 | 8.4 | `que promedia cinco particiones cuando tres ya se habían visto: es una estimación más precisa de lo ya observado, no una confirmación` | Igual que I-1 | `que promedia cinco particiones nuevas cuando el mismo contraste ya se había visto positivo en otras tres particiones el 16-11: es una estimación más precisa de lo ya observado, no una confirmación` |
| I-3 | 7.7, tabla de adaptación | `\| +0,028 [+0,007; +0,049] \| 29/40 \| 0,050 \| Respaldo \|` | `enfoques_41p_22-11-2026/e4_confirmatorio.csv`, `p_holm` = 0,049455 → 0,049. Con 0,050 la fila contradice la regla de 6.3 (p de Holm < 0,05) | `\| +0,028 [+0,007; +0,049] \| 29/40 \| 0,049 \| Respaldo \|` |
| I-3b | 7.7, texto | `La decisión de la adaptación sin historial está pegada al umbral (p Holm 0,0495 en el CSV).` | Ídem | `La decisión de la adaptación sin historial está pegada al umbral (p Holm 0,049; 0,0495 en el CSV, que el INFORME muestra como 0,050 por un redondeo doble).` |
| I-4 | 7.2, "Posición en el estímulo" | `0,51 en el primer segundo, 0,37 entre el segundo y el tercero y 0,62 hacia los 12 s.` | Recalculado desde `explicativo_posicion_41p_18-11-2026/predicciones_atencion.csv.gz` (22.176 ventanas, 41 personas): posición 1 = 0,509; 2 = 0,374; 3 = 0,381; 9–12 = 0,535; exactamente 12 = 0,544; **12 o más = 0,620**. Coincide con `enfoques_41p_22-11-2026/e1_descriptivos.csv` (tramo 9–12 s: 0,535; 13–20 s: 0,591; 21–32 s: 0,656). El 0,62 no es "hacia los 12 s": es el promedio de todas las ventanas desde los 12 s | `0,51 en el primer segundo, 0,37–0,38 en el segundo y el tercero, 0,53 entre los 9 y los 12 s y 0,62 desde los 12 s en adelante.` |
| I-5 | 7.6, "Montaje y sincronía" | `Las ventanas de 2 s del EEG están corridas entre un 12 % y un 25 % respecto de las de mirada, pupila y GSR.` | `montaje_ocular_41p_23-11-2026/personas.csv`, `lag_parpadeo_s`: mínimo 0,184, mediana 0,448, máximo 0,528 → 9,2 %, 22,4 % y 26,4 % de 2 s. El 12–25 % viene del INFORME del montaje y corresponde a 0,25–0,5 s, no al rango 0,18–0,53 s que el mismo párrafo cita | `Las ventanas de 2 s del EEG están corridas entre un 9 % y un 26 % (mediana 22 %) respecto de las de mirada, pupila y GSR.` |

### 2.2 Lecturas que van más lejos que la evidencia, contradicciones internas y rótulos

| # | Sección | Texto actual exacto | Problema | Texto propuesto |
|---|---|---|---|---|
| I-6 | 7.3, AUC estratificada | `La ganancia se mantiene dentro del mismo minuto, lo que descarta que sea solo una deriva lenta de la sesión.` | Es un análisis post hoc con reglas usadas como lectura descriptiva; el control registrado (P2, tiempo de sesión) quedó inconcluso. Contradice 8.4, que dice "habla contra una deriva lenta […] como única explicación" | `La ganancia se mantiene dentro del mismo minuto, lo que habla contra una deriva lenta de la sesión como única explicación; es un análisis post hoc, y el control registrado del tiempo de sesión quedó inconcluso (sección 7.1).` |
| I-7 | 8.1, tabla | `\| ¿Aporta el orden de las ventanas? \| No: +0,008 [−0,004; +0,020] \| Indicio secundario, sin corrección \|` | Hallazgo M13 de la auditoría: GRU con historial − GRU de una ventana mide el aporte del historial en la GRU, no el del orden. El contraste propio del orden (GRU − HGB, ambos con historial) es inconcluso en activación (+0,020 [−0,017; +0,057], `cierre_final_41p_16-11-2026/contrastes.csv`). "Indicio" de aporte del orden no tiene contraste que lo sostenga | `\| ¿Aporta el orden de las ventanas? \| No: la GRU con historial no supera a su control (+0,008 [−0,004; +0,020]) y rinde 0,040 menos que el HGB \| No demostrado: el contraste propio del orden (GRU − HGB, ambos con historial) es inconcluso, +0,020 [−0,017; +0,057]. La GRU con historial supera a su control de una ventana (+0,051 [+0,021; +0,080], secundario sin corrección), lo que mide el historial y no el orden \|` |
| I-7b | 7.4, último párrafo | `Es un indicio secundario, no un resultado.` | Ídem | `Ese contraste mide el aporte del historial dentro de la GRU, no el del orden; el contraste propio del orden (GRU menos HGB, ambos con historial) es inconcluso. Es un indicio secundario, no un resultado.` |
| I-8 | 7.7, adaptación | `y en el modelo adaptado el historial aporta +0,058 [+0,032; +0,084].` | La cifra coincide con `e4_descriptivos.csv`, pero no está en la lista `descriptive` de `enfoques_41p_22-11-2026/protocolo.json` (solo E4a y E4b). La auditoría del 23-11 la señala como contenido no registrado y no rotulado | `y en el modelo adaptado el historial aporta +0,058 [+0,032; +0,084] (descriptivo que no figura en la lista registrada del protocolo).` |
| I-9 | 7.1, lecturas descriptivas | `- Por grupo de origen (16-11), el efecto de atención` | `heterogeneidad_por_grupo.csv` no está en el protocolo ni en el script del análisis final y sus intervalos no se reproducen exactamente (hallazgo M5). El borrador la presenta sin rótulo | `- Por grupo de origen (16-11; análisis no registrado en el protocolo, sin código versionado y con intervalos que la auditoría final reproduce con diferencias de hasta 0,0013), el efecto de atención` |
| I-10 | 8.3, "Qué puede explicar la detección que permanece" | `actividad muscular de la frente y las sienes asociada a los movimientos de los ojos (Goncharova et al., 2003);` | `VERIFICACION_REFERENCIAS.md`, ref. 9 y frase 5: el artículo estudia contracciones voluntarias y **no** relaciona esa actividad con los movimientos oculares. Es la única corrección de esa lista que el borrador no aplicó | `actividad muscular de la frente y las sienes, que contamina el EEG en un rango amplio de frecuencias (Goncharova et al., 2003) y que podría acompañar a los movimientos de los ojos, asociación que no se midió;` |
| I-11 | 8.5, "Tipo de relación" | `Además, el *Arousal Score* es relativo a la mediana de cada persona y la navegación web produce un rango de activación estrecho.` | Afirmación de hecho sin dato ni cita. Ningún CSV ni INFORME mide el rango de activación | `Además, el *Arousal Score* es relativo a la mediana de cada persona, y es plausible que la navegación web produzca un rango de activación estrecho; este trabajo no lo midió.` |
| I-12 | 6.3 | `Cada análisis se registró en el repositorio antes de ejecutarse y se ejecutó una sola vez.` | Contradicho por el mismo párrafo y por 6.4, 7.1 y 7.2: hay una comprobación no registrada, sensibilidades no registradas y la heterogeneidad por grupo | `Cada etapa con modelos se registró en el repositorio antes de ejecutarse y se ejecutó una sola vez; las excepciones (la heterogeneidad por grupo del 16-11, las sensibilidades a personas individuales y la comprobación estratificada del 22-11) se rotulan como no registradas donde aparecen.` |

## 3. Menores

### 3.1 Redondeo doble (tercer decimal; ninguna cambia una decisión)

El borrador copia la cifra del INFORME, que redondeó dos veces. El valor correcto sale del CSV.

| # | Sección | Texto actual exacto | Fuente (archivo, fila, columna = valor) | Corrección exacta |
|---|---|---|---|---|
| R-1 | 7.2, curva | `\| 48 s \| −0,013 [−0,020; −0,005] · inferior \|` | `reapertura_41p_22-11-2026/curva_temporal.csv`, atención lag 48, `delta` = −0,012461 | `\| 48 s \| −0,012 [−0,020; −0,005] · inferior \|` |
| R-2 | 7.2, curva | `\| 96 s \| −0,010 [−0,016; −0,004] · inferior \| −0,009 [−0,016; −0,003] · inferior \|` | `curva_temporal.csv`, atención lag 96, `high95` = −0,003450; `reapertura_fase2_41p_22-11-2026/x1_placebo_bloque.csv`, atención lag 96, `high95` = −0,002469 | `\| 96 s \| −0,010 [−0,016; −0,003] · inferior \| −0,009 [−0,016; −0,002] · inferior \|` |
| R-3 | 7.2 | `(hasta −0,013)` | Igual que R-1 | `(hasta −0,012)` |
| R-4 | 7.2 | `real menos placebo −0,003 [−0,005; +0,000] según el informe (−0,0025 en el CSV).` | `ampliacion_41p_16-11-2026/enmienda_e1_lag6/contrastes.csv`, atención, `delta` = −0,002493 | `real menos placebo −0,002 [−0,005; +0,000] (−0,0025 en el CSV; el INFORME muestra −0,003 por un redondeo doble).` |
| R-5 | 7.2, AUC estratificada | `(+0,013 [+0,007; +0,021])` | `reapertura_fase2_41p_22-11-2026/x2_estratificada.csv`, atención, estímulo, `low95` = 0,006460 | `(+0,013 [+0,006; +0,021])` |
| R-6 | 7.2, reloj | `0,677 [0,655; 0,699]` | `reapertura_41p_22-11-2026/descriptivos.csv`, "D1 AUC sin historial, estratificada por posición", `low95` = 0,654499 | `0,677 [0,654; 0,699]` |
| R-7 | 7.3 | `+0,040 [+0,013; +0,066]` | `ampliacion_41p_16-11-2026/contrastes.csv`, activación, E1 principal, `low95` = 0,012484 | `+0,040 [+0,012; +0,066]` |
| R-8 | 7.3, curva | `+0,010 [−0,027; +0,045] · inconcluso` | `x1_placebo_bloque.csv`, activación lag 24, `delta` = 0,009467 | `+0,009 [−0,027; +0,045] · inconcluso` |
| R-9 | 7.3, fase 3 | `(+0,005 [−0,026; +0,035])` | `reapertura_fase3_41p_22-11-2026/descriptivos.csv`, activación, estímulo, "hgb_c32 − pos_c1", `low95` = −0,025491 | `(+0,005 [−0,025; +0,035])` |
| R-10 | 7.3 | `posición menos sin historial −0,004 [−0,024; +0,017]` | `explicativo_posicion_41p_18-11-2026/contrastes.csv`, activación, "pos_c1 − hgb_c1", `low95` = −0,023483 | `posición menos sin historial −0,004 [−0,023; +0,017]` |
| R-11 | 7.5, tabla | `\| +0,005 [−0,003; +0,013] \| −0,008 [−0,014; −0,001] \|` | `ampliacion_41p_16-11-2026/contrastes.csv`, atención, "mlp_intermedia − mlp_tardia", `delta` = −0,007453 | `\| +0,005 [−0,003; +0,013] \| −0,007 [−0,014; −0,001] \|` |
| R-12 | 7.5, tabla | `\| Activación \| +0,007 [−0,032; +0,042] \|` | Ídem, activación, "mlp_tardia − mlp_temprana", `delta` = 0,006462 | `\| Activación \| +0,006 [−0,032; +0,042] \|` |
| R-13 | 7.6, tabla B | `\| B1 Solo EEG − 0,5 \| +0,181 [+0,165; +0,197] \|` | `enfoques_41p_22-11-2026/e2_confirmatorio.csv`, B1, `low95` = 0,164452 | `\| B1 Solo EEG − 0,5 \| +0,181 [+0,164; +0,197] \|` |
| R-14 | 7.6, tabla de variables | `\| 0,673 \| 0,659 \| 0,603 \| 0,070 \|` | `limpieza_ocular_41p_23-11-2026/descriptivos.csv`, "AUC ica3_lento_amp", `delta` = 0,602486 (la caída, 0,0700, queda igual) | `\| 0,673 \| 0,659 \| 0,602 \| 0,070 \|` |
| R-15 | 7.6, tabla L | `\| −0,045 [−0,059; −0,033] \| 6/41 \|` | `limpieza_ocular_41p_23-11-2026/confirmatorio.csv`, L4, `high95` = −0,032476 | `\| −0,045 [−0,059; −0,032] \| 6/41 \|` |
| R-16 | 7.6, tabla de AUC | `\| HGB, EEG original \| 0,681 [0,665; 0,697] \|` | `red_cruda_41p_23-11-2026/descriptivos.csv`, "AUC eeg_c1", `low95` = 0,664452 | `\| HGB, EEG original \| 0,681 [0,664; 0,697] \|` |
| R-17 | 7.7, tabla | `\| HGB, solo EEG \| 0,524 [0,497; 0,551] \| 26/41 \|` | Ídem, "AUC hgb_eeg_act", `high95` = 0,550493 | `\| HGB, solo EEG \| 0,524 [0,497; 0,550] \| 26/41 \|` |

### 3.2 Lecturas y precisiones menores

| # | Sección | Texto actual exacto | Problema | Texto propuesto |
|---|---|---|---|---|
| m-1 | 8.1, tabla | `\| ¿Queda algo al controlar la posición? \| Nada \|` | Es un nulo concluyente dentro de ±0,02, no un cero; a igual posición el estrato descriptivo da +0,005 [+0,001; +0,010] | `\| ¿Queda algo al controlar la posición? \| No: nulo concluyente dentro de ±0,02 \|` |
| m-2 | 7.2, curva | `Las ventanas de los segundos anteriores no contienen información sobre la etiqueta de atención.` | Lo medido es frente a un placebo, con reglas usadas como lectura descriptiva | `Las ventanas de los segundos anteriores no aportan sobre la etiqueta de atención más que un placebo de la misma persona.` |
| m-3 | 8.2 | `Las ventanas de 6 a 96 s antes no contienen información sobre la etiqueta.` | Ídem | `Las ventanas de 6 a 96 s antes no aportan más que un placebo de la misma persona.` |
| m-4 | 7.2, etiqueta corregida | `Las decisiones de A1 y A3 están pegadas al umbral (p Holm 0,055).` | La regla es asimétrica (hallazgo M3): "inferior" no exige Holm. A1 es "inferior" por su límite superior (−0,001), no por el p. Falta además el hallazgo M2 | `Las decisiones de A1 y A3 están al filo: A1 es "inferior" porque el límite superior de su intervalo es −0,001 (la regla no exige Holm para "inferior"), y A3 sería "respaldo" con un p de Holm bajo 0,05 (es 0,055). En este análisis las predicciones del modelo con historial y posición son idénticas a las del modelo con historial, por lo que A3 equivale a historial menos (actual + posición); un diagnóstico del 26-11 confirmó que no es un error: con la etiqueta corregida el modelo nunca usa la columna de posición.` (fuente: `ronda2/DIAGNOSTICO_E1_POSICION.md`, que no es mío y solo leí) |
| m-5 | 7.3, curva | `Los resultados no dependen de una sola persona: sin la más influyente,` | Sensibilidad no registrada (INFORME de la reapertura: "no estaba registrada") | `Los resultados no dependen de una sola persona (sensibilidad no registrada, pedida por la auditoría de resultados): sin la más influyente,` |
| m-6 | 7.3, fase 3 | `coincide con la fase 3 en el sentido:` | Coincide el signo de posición − sin historial (+0,040 y +0,049); el de historial − posición no (−0,015 y +0,005), ambos con intervalos que incluyen el cero | `coincide con la fase 3 en lo cualitativo:` |
| m-7 | 7.7 | `la decisión pasa a "inferior" al quitar una de cinco personas` | Ambiguo | `la decisión pasa a "inferior" al quitar cualquiera de cinco personas concretas` |
| m-8 | 7.8, tipo de página | `y peor en textos (0,60 sin historial; 0,63 con historial)` | `por_categoria.csv`: con historial la AUC más baja es "imagen blur" (0,599, 25 personas), no texto | `y peor en textos (0,60 sin historial; 0,63 con historial, donde solo queda por debajo una categoría con 25 personas)` |
| m-9 | 8.4 y 8.8 | `las AUC absolutas van de 0,52 a 0,59` y `En activación las AUC absolutas son bajas (0,52 a 0,59).` | La red da 0,498 y el modelo general en la parte final de la sesión, 0,502 | `las AUC absolutas van de 0,50 a 0,59` y `En activación las AUC absolutas son bajas (0,50 a 0,59).` |
| m-10 | 6.3, tabla de reglas | `\| Inferior \| límite superior del intervalo de 95 % bajo cero \|` | Falta la precedencia del código (respaldo, inferior, nulo): por eso la banda de 24 s de atención es "inferior" aunque su intervalo de 90 % cabe en ±0,02 | `\| Inferior \| límite superior del intervalo de 95 % bajo cero; no exige Holm y tiene precedencia sobre "nulo concluyente" \|` |
| m-11 | 6.2 | `sobre la señal cruda de 16 canales y 2 s,` | La red recibe la señal con el mismo filtrado que la extracción de variables y escala por persona y canal (INFORME de la red); "cruda" significa sin variables calculadas | `sobre la señal de 16 canales y 2 s, filtrada como en la extracción de variables y sin variables calculadas a mano,` |

Citas con matiz pendiente según `VERIFICACION_REFERENCIAS.md`:

| # | Sección | Texto actual exacto | Problema | Texto propuesto |
|---|---|---|---|---|
| c-1 | 8.3 | `Los parpadeos agregan una deflexión de gran amplitud y máximo frontopolar (Iwasaki et al., 2005).` | El resumen de Iwasaki respalda el máximo frontopolar; la amplitud está en Plöchl et al. (2012) | `Los parpadeos agregan una deflexión de gran amplitud y máximo frontopolar (Iwasaki et al., 2005; Plöchl, Ossandón y König, 2012).` |
| c-2 | 8.3 | `es imperfecta en exploración visual libre: puede dejar artefacto residual o retirar actividad cerebral (Dimigen, 2020).` | Dimigen muestra el defecto con la configuración habitual; con el procedimiento optimizado la corrección es casi completa | `es imperfecta en exploración visual libre cuando se aplica con la configuración habitual: puede dejar artefacto residual o retirar actividad cerebral (Dimigen, 2020).` |
| c-3 | 8.3 | `el dipolo córneo-retinal se concentra en frecuencias bajas, pero` | Sin cita; la sostiene Plöchl et al. (2012) | `el dipolo córneo-retinal se concentra en frecuencias bajas (Plöchl, Ossandón y König, 2012), pero` |

Citas comprobadas sin observaciones: Croft y Barry (2000) junto a Plöchl; Yuval-Greenberg (2008), Keren (2010) e Hipp y Siegel (2013) en conjunto; Keren para 20–90 Hz; Goncharova para "ocultar o imitar los ritmos beta y alfa"; Jung (2000); Dimigen et al. (2011); Klimesch (2012); Lawhern (2018); Benedek y Kaernbach (2010) para inervación simpática exclusiva, ventana de 1–3 s o 1–5 s y superposición; Critchley (2002) en su versión acotada; Barry (2005, 2007) como comparación entre condiciones; Mathôt (2018).

### 3.3 Forma

1. **AUC y ROC** solo se desarrollan en el aviso inicial, que no pasará a LaTeX. Desarrollarlas en 6.3, en la primera mención del cuerpo.
2. **"folds"** (7.8: `La desviación entre los 8 folds supera a la media en los tres`) frente a "grupos" en 6.3. Proponer: `La desviación entre los 8 grupos de la validación cruzada supera a la media en los tres`.
3. **"INFORME" y "CSV"** aparecen en el cuerpo como notas de proceso (7.2, 7.3, 7.6, 7.7). Sirven al borrador; quitarlas o llevarlas a nota al pie antes de LaTeX.
4. **"V2" y "V3"** ("GSR V2", "cierre V3") son nombres internos de versión sin explicación.
5. **Kappa** sin apellido (6.1): "kappa de Cohen".
6. **Préstamos sin criterio único:** *bootstrap*, *offline*, *post hoc* van en redonda; *arousal* y los nombres de modelos, en cursiva.
7. **Columna "A favor"** en la tabla L (7.6): en L4 "6/41" son las personas en que la limpieza sube la AUC. Aclararlo en una nota bajo la tabla.
8. **Fuentes incompletas:** 7.3 usa `reapertura_fase2_41p_22-11-2026/descriptivos.csv` (AUC 0,501, fracción de pares, bloque − disperso) y no lo lista; 7.1, 7.5, 7.6 y 7.8 citan el "recálculo de la auditoría final" sin su ruta (`documentacion/auditoria_final_23-11-2026/recalculo.json`); 7.7 usa 0,518 de `reapertura_41p_22-11-2026/auc_absolutas.csv`.
9. **Términos fijos y "emociones":** sin problemas. *Modelo Profesor*, *Modelo Estudiante*, *Attention Score*, *Arousal Score*, Observado y Atendido están en su forma acordada; "emociones" solo aparece como decisión abierta (aviso inicial y 8.10) y en la cita de Critchley. No se encontraron erratas ortográficas.

## 4. Qué se comprobó y cómo

| Sección | Fuente contrastada | Resultado |
|---|---|---|
| 6.1 | INFORME de profesor, GSR V2 y enfoques; `e1_descriptivos.csv` | Coincide (25 personas, 5 variables, 11.796 de 22.211, 90,6 %, kappa 0,81). Pesos 0,40–0,56 y −0,05: solo en el INFORME de enfoques |
| 6.2 | `cobertura_historial.csv`, `congelacion_*.json`, protocolos | Coincide (7,8 y 12,6 ventanas; 7 y 15 hojas; 1.217 parámetros; desfases; 150 s; 40 %) |
| 6.3 | `protocolo.json` del análisis final y de la reapertura | Coincide (8 grupos, 5 particiones, 20.000 réplicas, reglas, margen 0,02) |
| 6.4 | Protocolos (`post_hoc`, `directed`, `confirmatory`, `secondary`, `descriptive`) y tabla de trazabilidad | Coincide, salvo I-1 |
| 7.1 | `contrastes.csv`, `metricas.csv`, `heterogeneidad_por_grupo.csv`, `resultados.csv`, `confirmatorio.csv`, `descriptivos.csv`, V3 `contrastes.csv` | Todas las cifras coinciden |
| 7.2 | Robustez, ampliación y enmienda, explicativo, curva, fase 2, fase 3, E1 | Coincide salvo R-1 a R-6 e I-4 |
| 7.3 | Ídem y `cobertura_activacion.json` | Coincide salvo R-7 a R-10 |
| 7.4 | `cierre_final_41p_16-11-2026/contrastes.csv`, V3 | Coincide |
| 7.5 | Ampliación, V3, `recalculo.json` | Coincide salvo R-11 y R-12 |
| 7.6 | E2, montaje, limpieza, red | Coincide salvo R-13 a R-16 e I-5 |
| 7.7 | Red, E3, E4 | Coincide salvo R-17 e I-3 |
| 7.8 | `fatiga_por_quintil.csv`, `importancia_resumen.csv`, `por_categoria.csv` | Coincide (ver m-8) |
| 8 | Repite cifras del capítulo 7 | Coinciden con el capítulo 7 y con los CSV; observaciones en la sección 2.2 |

No verificado: que los INFORME reflejen bien lo que no tiene CSV (pesos del *Attention Score*, proporción de ventanas del mismo estímulo por desfase, sensibilidades dejando personas fuera de la red), y el contenido del manuscrito al que alude 8.8.
