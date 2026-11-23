# Reapertura de la experimentación — 22-11-2026

Mario reabrió la experimentación el 22-11-2026 para obtener conclusiones más firmes. Se hizo en dos fases, cada una registrada y publicada antes de correr y ejecutada una sola vez. Etiquetas, variables, modelos y configuración congelada no cambiaron.

- Fase 1: `scripts/reapertura_41p.py`, protocolo en el commit `5076307`. Resultados en esta carpeta.
- Fase 2: `scripts/reapertura_fase2_41p.py`, protocolo en el commit `e3d9c71`. Resultados en `resultados/reapertura_fase2_41p_22-11-2026`. Son controles post hoc motivados por la auditoría de código de la fase 1; se registraron cuando la fase 1 aún corría y no existía ningún resultado.
- Comprobación no registrada, hecha después de ver los resultados: `scripts/reapertura_posthoc_estratos.py`. Va marcada como tal más abajo.

Las 41 personas ya se habían consultado en los análisis anteriores. Nada de esto es una confirmación independiente en una cohorte nueva.

> **Fase 3 (misma noche).** El punto que aquí queda abierto, separar el historial de la posición en el estímulo, se abordó en [la fase 3](../reapertura_fase3_41p_22-11-2026/INFORME.md): atención, nulo concluyente (el historial no agrega nada sobre la posición); activación, +0,032 [+0,004; +0,059] sobre la posición, inconcluso tras Holm, y dentro de un mismo estímulo la ventaja del historial se explica por el tiempo transcurrido.

## Qué cambia respecto del cierre del 18-11

| Tema | Antes | Ahora |
|---|---|---|
| Activación, contraste principal | Inconcluso: +0,034 [−0,001; +0,069] | **Respaldo**: +0,036 [+0,010; +0,065], p Holm 0,021 |
| Activación, alcance temporal | Sin caracterizar | La información está en los **6 a 12 s anteriores**; desde 24 s no se distingue del placebo |
| Activación, deriva lenta de la sesión | Sin controlar | La ganancia se mantiene dentro del mismo minuto (+0,058), pero el control con el tiempo de sesión como variable queda inconcluso |
| Atención, información en el pasado | Nulo frente al placebo (un solo contraste) | **Nulo concluyente** a 6 y 12 s; a 24–96 s el pasado rinde igual o peor que el placebo |
| Atención, detección desde EEG | 0,684 sin controlar el momento | **0,677 al comparar solo ventanas de la misma posición**: la detección no depende del momento del estímulo |

## Fase 1 — familia confirmatoria

Validación cruzada agrupada por persona repetida en 5 particiones nuevas. La AUC de cada persona se promedia sobre las 5 particiones. Holm sobre las 4 pruebas.

| Tarea | Prueba | ΔAUC | IC 95 % | Mejoran | p Holm | Decisión |
|---|---|---|---|---|---|---|
| Atención | P1 historial hasta 32 − sin historial | +0,029 | [+0,021; +0,037] | 36/41 | <0,0001 | Efecto relevante |
| Atención | P2 lo mismo, ambos con tiempo de sesión | +0,032 | [+0,024; +0,040] | 37/41 | <0,0001 | Efecto relevante |
| Activación | P1 historial hasta 32 − sin historial | +0,036 | [+0,010; +0,065] | 23/41 | 0,021 | Respaldo |
| Activación | P2 lo mismo, ambos con tiempo de sesión | +0,026 | [−0,006; +0,056] | 27/41 | 0,111 | Inconcluso |

AUC absolutas (media por persona): atención 0,683 sin historial y 0,712 con historial; activación 0,518 y 0,554.

P1 por partición: atención entre +0,028 y +0,030; activación entre +0,028 y +0,047. El tiempo de sesión solo agrega +0,025 [+0,019; +0,032] en atención y +0,019 [−0,023; +0,061] en activación.

"Efecto relevante" en atención describe el tamaño de la mejora del historial, no su origen. El origen se discute más abajo y no es temporal.

## Fase 1 — curva temporal (secundaria)

El modelo recibe la ventana actual más la media y desviación de las ventanas cuyo inicio cae entre L y L+6 s antes, sin importar el estímulo. Placebo: el mismo número de ventanas de la misma persona, a 150 s o más. Todos los modelos usan las mismas filas (6.268 de activación en 40 personas; 12.613 de atención en 41). Holm sobre los 5 desfases por tarea.

| Desfase | Atención: desfase − placebo | Activación: desfase − placebo |
|---|---|---|
| 6 s | −0,004 [−0,010; +0,002] · nulo concluyente | **+0,047 [+0,018; +0,078]** · p Holm 0,017 · respaldo |
| 12 s | −0,004 [−0,012; +0,004] · nulo concluyente | +0,024 [−0,011; +0,060] · inconcluso |
| 24 s | −0,007 [−0,013; −0,000] | +0,004 [−0,033; +0,042] · inconcluso |
| 48 s | −0,013 [−0,020; −0,005] · inferior | −0,023 [−0,053; +0,010] · inconcluso |
| 96 s | −0,010 [−0,016; −0,004] · inferior | +0,019 [−0,016; +0,053] · inconcluso |

Tendencia en activación: el contraste cae 0,010 por cada duplicación del desfase [−0,018; −0,003], p 0,009, en 27 de 40 personas. En atención no hay tendencia clara (−0,002, p 0,071).

En activación el placebo no aporta sobre la ventana actual (+0,009 [−0,024; +0,043]).

## Fase 2 — controles post hoc de la auditoría

**X1, placebo de bloque.** El placebo de la fase 1 eran ventanas sueltas; este es un bloque contiguo de la misma persona a 150 s o más.

| Desfase | Atención: desfase − bloque | Activación: desfase − bloque |
|---|---|---|
| 6 s | −0,003 [−0,010; +0,004] · nulo concluyente | **+0,053 [+0,026; +0,081]** · p Holm 0,003 |
| 12 s | −0,003 [−0,011; +0,004] · nulo concluyente | +0,030 [−0,005; +0,064] |
| 24 s | −0,006 [−0,013; +0,001] · nulo concluyente | +0,010 [−0,027; +0,045] |
| 48 s | −0,012 [−0,020; −0,004] | −0,017 [−0,041; +0,009] |
| 96 s | −0,009 [−0,016; −0,003] | +0,024 [−0,011; +0,059] |

El resultado no depende del tipo de placebo. Los dos placebos rinden igual (bloque − disperso: −0,001 en atención, −0,006 en activación).

**X2, AUC estratificada.** La AUC de cada persona se calcula solo con pares de ventanas del mismo estrato. Contraste: historial hasta 32 − sin historial. Holm sobre las 6 pruebas.

| Estrato | Atención | Activación |
|---|---|---|
| Mismo estímulo | +0,013 [+0,007; +0,021] · respaldo | +0,054 [+0,015; +0,094] · p Holm 0,022 · respaldo |
| Mismo minuto de sesión | +0,023 [+0,016; +0,030] · respaldo | **+0,058 [+0,027; +0,092]** · p Holm 0,003 · efecto relevante |
| Misma posición en el estímulo | +0,017 [+0,010; +0,024] · respaldo | +0,027 [−0,003; +0,059] · inconcluso |

En activación, la ventana actual sola no distingue nada dentro de un mismo estímulo ni dentro de un mismo minuto (AUC 0,501 en ambos); con historial sube a 0,555 y 0,560.

Solo el 2–3 % de los pares de una persona cae dentro de un mismo estímulo y el 7 % dentro de un mismo minuto: estas AUC usan una fracción pequeña de las comparaciones.

## Sensibilidad a personas individuales (activación)

Pedida por la auditoría de resultados; no estaba registrada.

| Contraste | Media | Mediana | Mejoran | Sin la persona más influyente |
|---|---|---|---|---|
| P1 historial − sin historial | +0,036 | +0,014 | 23/41 | +0,028 [+0,006; +0,050] |
| Desfase 6 s − placebo | +0,047 | +0,042 | 30/40 | +0,039 [+0,012; +0,065] |
| Desfase 6 s − placebo de bloque | +0,053 | +0,056 | 31/40 | +0,046 [+0,021; +0,070] |
| Mismo minuto | +0,058 | +0,042 | 24/41 | +0,050 [+0,021; +0,081] |

Ningún resultado depende de una sola persona. El efecto promedio de P1 es desigual: una persona (P4) aporta 0,009 de los 0,036 y poco más de la mitad mejora. El contraste del desfase de 6 s es más parejo.

## Descriptivos

- **Posición sola (D1).** Un modelo que solo recibe los segundos transcurridos en el estímulo, sin fisiología, llega a AUC 0,598 [0,581; 0,614] en atención y 0,543 [0,492; 0,595] en activación.
- **Detección de atención sin el efecto de la posición (D1).** AUC sin historial 0,684; comparando solo ventanas de la misma posición, 0,677 [0,655; 0,699].
- **Autocorrelación de la etiqueta (D2).** La etiqueta de 6 s antes en el mismo estímulo predice la actual con AUC 0,680 [0,634; 0,724] en activación (5.035 pares, 40 personas) y 0,535 [0,519; 0,552] en atención (8.818 pares). El estado de activación persiste varios segundos; el de atención casi no.

## Comprobación no registrada (después de ver resultados)

X2 dio una ganancia del historial en atención al estratificar por posición (+0,017), en aparente tensión con el explicativo del 18-11. Se aplicó la misma estratificación a las predicciones guardadas del 16 y 18-11, que incluyen el modelo con la posición como variable (una sola partición; `posthoc_no_registrado_estratos_con_posicion.csv` en la carpeta de la fase 2).

| Estrato | Atención: historial − posición | Activación: posición − sin historial | Activación: historial − posición |
|---|---|---|---|
| Misma posición | +0,004 [−0,001; +0,009] | −0,008 [−0,021; +0,005] | +0,028 [−0,005; +0,061] |
| Mismo estímulo | −0,003 [−0,007; +0,002] | **+0,040 [+0,014; +0,067]** | −0,015 [−0,056; +0,024] |
| Mismo minuto | −0,004 [−0,008; +0,001] | +0,015 [−0,002; +0,034] | +0,012 [−0,027; +0,051] |

- Atención: no hay tensión. También con AUC estratificada, la posición como variable reproduce la ganancia del historial.
- Activación: dentro de un mismo estímulo, los segundos transcurridos mejoran la predicción por sí solos y el historial no los supera. Con una sola partición estos intervalos son anchos; es una advertencia, no un resultado.

## Lectura

**Activación.**
1. El historial mejora la predicción. El contraste principal, antes inconcluso, pasa a respaldo con cinco particiones.
2. La información es de corto alcance: está en los 6 a 12 s anteriores y desaparece a partir de 24 s. No es deriva lenta de la persona: el pasado lejano no ayuda y la ganancia se mantiene dentro del mismo minuto.
3. Lo que el historial aporta es una mejor estimación de un estado que dura segundos (la propia etiqueta se parece a la de 6 s antes, AUC 0,68).
4. No queda demostrado que sea más que eso. Dos controles quedan inconclusos (tiempo de sesión como variable, +0,026; misma posición, +0,027) y, dentro de un mismo estímulo, el tiempo transcurrido rinde tanto como el historial.
5. La AUC absoluta sigue baja (0,55–0,58) y el efecto es desigual entre personas (en P1 mejoran 23 de 41).

**Atención.**
1. El pasado no contiene información: nulo concluyente a 6 y 12 s frente a dos placebos distintos, y de 24 a 96 s rinde igual o peor que ventanas tomadas al azar.
2. La mejora del historial (+0,029) es real y estable, pero su origen sigue siendo el tiempo dentro del estímulo; lo confirma la comprobación estratificada.
3. La etiqueta de atención depende mucho del reloj: la posición sola da AUC 0,60 y el tiempo de sesión agrega +0,025. Esto habla de cómo se construye la etiqueta.
4. La detección desde EEG no es un artefacto de ese reloj: 0,677 entre ventanas de la misma posición.

**Hipótesis.** Sigue siendo apoyo parcial, ahora mejor delimitado: en activación hay un efecto del historial confirmado y de corto alcance; en atención no hay información temporal.

## Límites

- Las ventanas duran 2 s con paso de 1 s. La etiqueta de activación integra GSR en [t−4, t+2) s y la banda de 6 s usa fisiología hasta t−4: son contiguas, sin solapamiento ni holgura. No se verificó si los filtros del GSR aguas arriba tienen un soporte más largo.
- En el desfase de 6 s de activación el 73 % de las ventanas pertenece al mismo estímulo que la actual (48 % a 12 s, 13 % a 24 s, 0 % desde 48 s). La curva mezcla cercanía temporal con pertenecer al mismo estímulo.
- El placebo incluye ventanas futuras (16–36 % según la tarea). Es fisiología, no etiqueta, y si sesga lo hace en contra del historial real.
- El placebo iguala el número de ventanas de la banda de 6 s; en las demás bandas coincide en el 30–44 % de las filas.
- La curva usa las filas con cobertura hasta 102 s atrás (53 % de activación, 57 % de atención), más frecuentes hacia el final de la sesión.
- P2 solo corrige la tendencia de sesión común a las personas. En activación la deriva tiene dirección distinta en cada persona; el estrato de un minuto es el control más estricto, pero es post hoc.
- El historial hasta 32 incluye la ventana actual y codifica la posición en el estímulo.
- Las reglas de decisión se definieron para la familia confirmatoria; en la curva y en la fase 2 se usan como lectura descriptiva.
- Etiquetas offline (activación: pseudoetiqueta GSR relativa a la sesión) y variables transductivas por persona, como en los análisis anteriores.

## Auditorías

- Código de la fase 1, por un agente independiente, antes de ver resultados: sin hallazgos bloqueantes (sin fuga entre personas; bandas, placebo y resúmenes verificados numéricamente). Sus hallazgos de interpretación originaron la fase 2 y la sección de límites.
- Resultados, por otro agente independiente con código propio: pasa los seis puntos (cifras reproducidas, integridad, hashes y cronología del registro). Detalle en `AUDITORIA_RESULTADOS.md`. La comprobación no registrada no fue auditada.
