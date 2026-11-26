# Resumen del último mes de tesis — 22-10 al 22-11-2026

Síntesis escrita el 22-11-2026 a partir de la bitácora, el historial de Git y los informes de cada carpeta de resultados. Ante cualquier diferencia mandan los `INFORME.md` de `repos/Tesis_MDS/resultados/`. No hay aprobación registrada del profesor guía sobre los resultados de noviembre ni sobre el margen práctico de 0,02; lo único registrado es que Mario comunicó el 01-11 que el profesor aprobó usar las etiquetas GSR V2.

> **Aviso (26-11-2026).** Esta síntesis es anterior a la auditoría final del 23-11, que reprodujo las cifras y pidió moderar varias lecturas. La referencia vigente es `repos/Tesis_MDS/documentacion/Cierre_Experimental_Final_23-11-2026.md`.

## En una mirada

| Semana | Qué se hizo | Qué salió |
|---|---|---|
| 22–24 oct | Contraste de temporalidad y fusión, control negativo temporal, robustez, presentación de avances | Resultados exploratorios; activación apenas sobre el control negativo |
| 29–30 oct | Atención binaria con profesor PCA reconstruido, EEG por canal, evaluación en validación y test | Atención AUC cercana a 0,69; mejora temporal +0,028 con intervalo que toca cero |
| 1–6 nov | Recuperación del vault, etiquetas GSR V2, comparación no lineal, ablación de modalidades, cierre V2, protocolo de potencia | Sin ventaja consistente de temporalidad ni de fusión en activación |
| 15–18 nov | Cierre V3, análisis final con 41 personas, placebo temporal, ampliación E1–E6, explicativo de posición, presentaciones v4–v6, borrador de resultados | Apoyo parcial: en atención la mejora es la posición en el estímulo; en activación hay información temporal |
| 22 nov | Cierre formal, reapertura en tres fases y cuatro enfoques nuevos | Activación con respaldo, solo para los 6 s anteriores; atención sin información temporal demostrable; parte de la detección por EEG es ocular |

## 22 al 24 de octubre

- Contraste de temporalidad y fusión, control negativo temporal y pruebas de robustez sin cohorte nueva, cada uno con protocolo propio.
- Referencia de esa etapa (activación en tres clases, exploratoria): mejor BA macro por persona 0,3843 con Ridge; 0,3557 en las ocho personas de test ya consultadas; control negativo temporal 0,3268.
- Presentación de avances y ampliación del manuscrito (capítulos 6 a 8). Ese manuscrito del 24-10 no se recuperó después; el vault vigente es el del respaldo del 24-09.

## 29 y 30 de octubre

- Etiqueta binaria de atención reconstruida desde las variables oculares con un *Modelo Profesor* con PCA, sin usar etiquetas antiguas. Modelos nuevos y grids de atención.
- Extracción de EEG por canal (16 canales por separado).
- Temporalidad en atención: en validación, HGB con contexto 32 AUC 0,694 y CatBoost 0,704; en test, contexto 32 AUC 0,688 frente a 0,660 del estático pareado (+0,028 [−0,004; +0,051], mejora en 7 de 8). Indicios favorables, evidencia inconclusa.
- Comparación común binaria (20 modelos) y diagnóstico de activación: AUC OOF 0,537 / 0,534 / 0,540 para contextos 1 / 8 / 32. Se detectaron problemas de calidad del GSR en algunas personas.

## 1 al 6 de noviembre

- Restauración del vault desde el respaldo del 24-09 (80 archivos verificados) y reorganización de carpetas en este Mac.
- Regla de respaldo obligatorio: commit y push verificado en cada etapa.
- Etiquetas de activación GSR V2 con control de calidad.
- Comparación no lineal con y sin historial (HGB): test 0,514 / 0,547 / 0,536; contraste principal +0,022 [−0,013; +0,059], inconcluso.
- Ablación de modalidades: la fusión no supera con claridad a las señales individuales.
- Cierre experimental V2 (01-11): sin apoyo suficiente a la superioridad temporal multimodal.
- Reentrenamiento completo y auditoría del 02-11: reproducen la corrida anterior.
- Protocolo de hipótesis y potencia (06-11): el N necesario en activación es muy sensible a la varianza usada (72, 101 o 767). El margen práctico de 0,02 quedó como propuesta.

## 15 al 18 de noviembre

- Presentaciones de avance v4 y v5.
- Cierre V3 (16-11): historial con todas las ventanas, GRU sensible al orden, fusión tardía y métricas del manuscrito. Sin ventaja temporal consistente; la GRU rinde peor que el HGB.
- Análisis final con 41 personas (16-11), registrado antes de correr: atención +0,026 [+0,018; +0,035], respaldo; activación +0,034 [−0,001; +0,069], inconcluso.
- Pruebas de robustez con placebo temporal (16-11): en atención el placebo reproduce toda la mejora; en activación no.
- Ampliación E1–E6 y explicativo de posición (18-11): en atención toda la mejora del historial se explica por los segundos transcurridos en el estímulo; en activación el historial sin solapamiento con la etiqueta supera al placebo (+0,046 [+0,018; +0,073]). Fusión tardía sobre temprana en atención entre redes MLP (+0,012, secundario); con HGB el signo es el contrario.
- Presentación v6 y borrador de Resultados y Discusión en el vault.

## 22 de noviembre

**Cierre formal** de la experimentación, con documento de cierre y etiqueta Git `cierre-experimental-2026-11-22`.

**Reapertura, pedida por Mario el mismo día.** Tres fases, cada una registrada antes de correr y con auditoría independiente de código y de resultados.

- Fase 1 (validación cruzada repetida, tiempo de sesión, curva temporal): el contraste principal de activación pasa a respaldo, +0,036 [+0,010; +0,065]. Solo la banda de 6 s tiene respaldo (+0,047 [+0,017; +0,078]; curva en una partición, 40 personas); a 12 s es inconcluso y desde 24 s no se distingue del placebo, sin demostrar ausencia. En atención el pasado no aporta a ningún desfase.
- Fase 2 (placebo de bloque, AUC estratificada): el resultado de activación no depende del tipo de placebo y se mantiene dentro del mismo minuto de sesión (+0,058).
- Fase 3 (historial frente a posición): en atención el historial no agrega nada sobre la posición (nulo concluyente). En activación agrega +0,032 [+0,004; +0,059], inconcluso tras Holm; dentro de un mismo estímulo agrega +0,009, también inconcluso.

**Cuatro enfoques nuevos**, registrados antes de correr (informe en `resultados/enfoques_41p_22-11-2026/INFORME.md`).

- E1, etiqueta de atención corregida por posición: elimina el efecto del reloj (posición sola 0,504) y la detección baja poco (0,675 frente a 0,683; decisión registrada "inferior", al filo). La mejora del historial cae a +0,010 y con la posición como variable queda en nulo concluyente.
- E2, detección cruzada: el EEG solo predice la etiqueta ocular con AUC 0,681 en las 41 personas. Una parte tiene firma de movimiento ocular (potencia lenta y amplitud 0,673; alfa y beta 0,593; canales posteriores 0,602 con montaje supuesto). El EEG no tiene limpieza de artefactos oculares.
- E3, activación por estímulo: AUC 0,587, la más alta en activación; no supera de forma demostrable a promediar el modelo por ventana.
- E4, diferencias entre personas: la detectabilidad es estable dentro de la sesión (fiabilidad por mitades 0,76 y 0,66); la ganancia del historial por persona no es fiable; adaptar el modelo a la persona mejora activación en +0,045 [+0,023; +0,069] y no cambia atención.

## Dónde queda la tesis

- **Hipótesis de temporalidad: apoyo parcial.** En activación el historial ayuda, con respaldo solo para los 6 s anteriores y con AUC absolutas bajas (0,55 a 0,59). En atención no hay información temporal: la mejora era el reloj del estímulo.
- **Atención.** La etiqueta mide quietud de la mirada y depende de la posición en el estímulo. La detección desde EEG es clara, pero cerca de un tercio de lo que tiene sobre el azar es ocular (0,060 de 0,181, cota inferior); del resto no se puede afirmar origen cerebral ni ocular.
- **Activación.** El modelo por estímulo rinde más (0,587), sin superar de forma demostrable al promedio por ventana. Las dos palancas que más la mejoran son trabajar a nivel de estímulo y adaptar el modelo a la persona.
- **Método.** Desde el 16-11 todo análisis con protocolo se registra en Git antes de sus predicciones y se ejecuta una vez; desde el 22-11 cada etapa pasa además por auditoría independiente.

## Pendiente

1. Decidir con el profesor guía el encuadre: la contribución más sólida es metodológica (qué parte de una mejora "temporal" es temporal de verdad y qué parte es artefacto del reloj o de los ojos).
2. Verificar el montaje real de los electrodos y evaluar una limpieza de artefactos oculares en el EEG; sin eso no se puede afirmar detección cerebral de atención.
3. Decidir si la etiqueta de atención corregida por posición reemplaza a la original en la tesis.
4. Margen práctico de 0,02: sigue como propuesta.
5. Escritura del manuscrito a partir del borrador del 18-11, y actualizar la presentación v6 con los resultados del 22-11.

Lista superada: las decisiones vigentes son las siete de la minuta del 23-11.

## Actualización del 23-11-2026

- **Montaje EEG:** los datos son compatibles con el montaje por defecto de OpenBCI (los parpadeos pegan en Fp1/Fp2 y decrecen hacia atrás). El EEG va entre 0,18 y 0,53 s atrasado respecto del seguidor ocular.
- **Limpieza ocular:** al quitar 3 componentes oculares (3,5 % de la varianza) la AUC de atención por EEG baja de 0,681 a 0,621; un control que quita 3 componentes no oculares (72 % de la varianza) la deja en 0,674. Alfa y beta baja de 0,593 a 0,547. El modelo limpio sigue sobre el azar en las 41 personas; el diseño no separa si ese resto es ocular o cerebral.
- El pendiente 2 queda resuelto en lo que permiten los datos: no se puede afirmar detección cerebral de atención. Informes en `repos/Tesis_MDS/resultados/montaje_ocular_41p_23-11-2026/INFORME.md` y `repos/Tesis_MDS/resultados/limpieza_ocular_41p_23-11-2026/INFORME.md`.
- **Red sobre el EEG crudo (modelo más complejo):** una red convolucional tipo EEGNet supera al modelo de referencia en atención (AUC 0,716 frente a 0,681; +0,035 [+0,023; +0,047]), pero al quitar los componentes oculares cae a 0,649: su detección depende de lo ocular, pero su ventaja sobre el HGB se mantiene con el EEG limpio (+0,028). En activación queda en el azar (0,498; comparación con el HGB inconclusa). Informe en `repos/Tesis_MDS/resultados/red_cruda_41p_23-11-2026/INFORME.md`.
