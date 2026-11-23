# Cuatro enfoques nuevos — 22-11-2026

Script `scripts/enfoques_41p.py`. Pedidos por Mario el 22-11-2026. Protocolo registrado antes de correr (versión 1 en el commit `cd25134`; versión 2 en `4a4798c`, con los cambios pedidos por dos auditorías de código hechas sin que existiera ningún resultado). Ejecutado una vez.

Configuración de modelos congelada, 5 repeticiones de la validación cruzada agrupada por persona, AUC por persona promediada sobre repeticiones, Holm dentro de cada familia, reglas de decisión del análisis final (margen 0,02). Son análisis dirigidos sobre personas y resultados ya vistos, no confirmaciones independientes. Las etiquetas originales no se modificaron.

## Resumen

| Enfoque | Resultado principal |
|---|---|
| E1 Etiqueta de atención corregida por posición | La corrección elimina el efecto del reloj (posición sola: AUC 0,504) y conserva casi toda la detección (0,675 frente a 0,683). La mejora del historial cae de +0,029 a +0,010 y, con la posición como variable, queda en nulo concluyente. |
| E2 Detección cruzada | El EEG solo detecta la etiqueta ocular con AUC 0,681 en las 41 personas, y el GSR no le agrega nada. **Pero la mayor parte de esa detección tiene firma de movimiento ocular**: potencia lenta y amplitud dan 0,673; alfa y beta solas, 0,593. |
| E3 Activación por estímulo | Un modelo a nivel de estímulo llega a AUC 0,587, la más alta obtenida en activación (32 de 41 personas sobre el azar). No supera de forma demostrable a promediar el modelo por ventana (+0,020, inconcluso). |
| E4 Diferencias entre personas | La detectabilidad de cada persona es un rasgo estable (fiabilidad 0,76 en atención y 0,66 en activación). La ganancia del historial de cada persona no es fiable. Adaptar el modelo a la persona mejora activación en +0,045 [+0,023; +0,069] y no cambia atención. |

## E1 — Etiqueta de atención corregida por posición

La etiqueta original es 1 si el puntaje ocular supera la mediana de la persona en toda la sesión. La corregida usa la mediana de la persona dentro del mismo tramo de posición en el estímulo (1, 2, 3, 4, 5, 6–8, 9–12, 13–20 y 21–32 s). Coinciden en el 90,6 % de las ventanas (kappa por persona 0,81).

| Prueba | ΔAUC | IC 95 % | Mejoran | p Holm | Decisión |
|---|---|---|---|---|---|
| A1 Detección sin historial: corregida − original | −0,008 | [−0,015; −0,001] | 17/41 | 0,055 | Inferior |
| A2 Historial − sin historial, etiqueta corregida | +0,010 | [+0,006; +0,015] | 31/41 | 0,0003 | Respaldo |
| A3 (Historial + posición) − (actual + posición), corregida | +0,004 | [+0,000; +0,009] | 24/41 | 0,055 | Nulo concluyente |

AUC con etiqueta corregida: sin historial 0,675; con historial 0,685; actual + posición 0,681; solo posición 0,504 [0,498; 0,510].

Lectura:
- La corrección cumple su objetivo: la posición sola deja de predecir la etiqueta (0,504; con la original era 0,598).
- La detección baja 0,008. Por la regla registrada es "inferior", pero la caída es pequeña. Compara AUC frente a dos objetivos distintos (cambia el 9,4 % de las etiquetas), así que no implica que la detección original fuera espuria.
- La mejora del historial se reduce a un tercio (de +0,029 a +0,010). Lo que queda se explica casi todo por la posición actuando en interacción con las señales: con la posición como variable el historial agrega +0,004, nulo concluyente.

## E2 — Detección cruzada: señales no oculares que predicen una etiqueta ocular

Etiqueta original de atención, modelos sin historial.

| Prueba | ΔAUC | IC 95 % | Mejoran | p Holm | Decisión |
|---|---|---|---|---|---|
| B1 Solo EEG − 0,5 | +0,181 | [+0,165; +0,197] | 41/41 | <0,0001 | Efecto relevante |
| B2 Solo GSR − 0,5 | +0,045 | [+0,030; +0,062] | 36/41 | <0,0001 | Efecto relevante |
| B3 (EEG + GSR) − solo EEG | +0,002 | [−0,001; +0,005] | 24/41 | 0,22 | Nulo concluyente |
| B4 Solo EEG − solo GSR | +0,136 | [+0,113; +0,158] | 40/41 | <0,0001 | Efecto relevante |

Segunda familia, agregada por la auditoría de código antes de correr: ¿la señal es cerebral o es movimiento de ojos captado por los electrodos? El EEG no tiene limpieza de artefactos oculares (solo tendencia lineal, filtro de red y pasabanda de 1 a 45 Hz).

| Prueba | ΔAUC | IC 95 % | Mejoran | p Holm | Decisión |
|---|---|---|---|---|---|
| B5 Solo alfa y beta − 0,5 | +0,093 | [+0,079; +0,106] | 40/41 | <0,0001 | Efecto relevante |
| B6 Canales posteriores − 0,5 (montaje supuesto) | +0,102 | [+0,083; +0,121] | 38/41 | <0,0001 | Efecto relevante |
| B7 (Lento y amplitud) − (alfa y beta) | +0,080 | [+0,067; +0,092] | 40/41 | <0,0001 | Efecto relevante |
| B8 Frontales − posteriores (montaje supuesto) | +0,073 | [+0,054; +0,092] | 38/41 | <0,0001 | Efecto relevante |

| Modelo | AUC | AUC a igual posición |
|---|---|---|
| Todo el EEG | 0,681 | 0,675 |
| Potencia lenta (delta, theta) y amplitud | 0,673 | 0,659 |
| Canales frontales (supuesto) | 0,675 | 0,667 |
| Canales posteriores (supuesto) | 0,602 | 0,600 |
| Solo alfa y beta | 0,593 | 0,593 |
| Solo GSR | 0,545 | 0,547 |

Otros descriptivos:
- Control negativo con etiquetas barajadas: AUC 0,496 [0,482; 0,510]. La tubería no fabrica señal.
- La probabilidad del modelo de EEG se correlaciona sobre todo con el recorrido de la mirada (Spearman medio por persona 0,41), luego con la dispersión (0,30) y la duración total de fijaciones (0,29); con la pupila, −0,09.
- El puntaje ocular que define la etiqueta está dominado por fijaciones, dispersión y recorrido (pesos 0,40 a 0,56); la pupila casi no pesa (−0,05). La etiqueta mide quietud de la mirada.

Lectura:
- El EEG predice la etiqueta ocular con claridad y en todas las personas, también a igual posición. El GSR aporta poco y nada sobre el EEG.
- La mayor parte de esa detección coincide con la firma de los movimientos oculares en el EEG: potencia lenta, amplitud y, bajo el montaje supuesto, electrodos frontales. Un modelo con solo esas variables rinde casi igual que el EEG completo (0,673 frente a 0,681).
- Queda una parte menos expuesta a ese artefacto: alfa y beta solas dan 0,593 en 40 de 41 personas, y los canales posteriores 0,602. No es prueba de actividad cerebral (alfa y beta también pueden contaminarse, y el montaje no está verificado), pero es la cota más defendible de detección no ocular: cerca de 0,59–0,60.
- Con estos datos, "el EEG detecta atención" debe leerse como "la señal de los electrodos, incluidos artefactos oculares, predice una medida de quietud de la mirada".

## E3 — Activación a nivel de estímulo

Unidad: el segmento (un estímulo continuo). Objetivo: mayoría de las etiquetas de activación de sus ventanas (1.589 segmentos; 47 empates excluidos; 79 % unánimes; mediana de 36 por persona). Entradas: media y desviación de EEG, mirada y pupila sobre todas las ventanas del segmento.

| Prueba | ΔAUC | IC 95 % | Mejoran | p Holm | Decisión |
|---|---|---|---|---|---|
| C1 Modelo de estímulo − 0,5 | +0,087 | [+0,050; +0,122] | 32/41 | 0,0001 | Efecto relevante |
| C2 Modelo de estímulo − promedio del modelo por ventana con historial | +0,020 | [−0,007; +0,046] | 23/41 | 0,27 | Inconcluso |
| C3 (Estímulo + duración) − solo duración | +0,048 | [−0,014; +0,109] | 25/41 | 0,27 | Inconcluso |

AUC: modelo de estímulo 0,587 [0,550; 0,622]; promedio del modelo por ventana con historial 0,567; sin historial 0,532; solo duración 0,535 [0,488; 0,583].

Con segmentos de 3 o más ventanas etiquetadas (1.348): estímulo − 0,5 = +0,099 [+0,062; +0,134]; frente al promedio por ventana +0,020 [−0,006; +0,046]; frente a solo duración +0,054 [−0,005; +0,108].

Lectura:
- A nivel de estímulo la activación se detecta con AUC 0,587, la más alta obtenida en esta tarea, y mejora sobre el modelo por ventana sin historial (+0,054 [+0,013; +0,095], descriptivo).
- No se demuestra que supere a promediar el modelo por ventana con historial, ni que aporte sobre la duración del estímulo, que por sí sola es muy variable entre personas.
- Refuerza la lectura de las fases anteriores: la activación es un estado del estímulo completo más que de cada ventana.

## E4 — Diferencias entre personas

**(a) Fiabilidad.** Segmentos de cada persona separados en dos mitades alternadas por orden temporal (dentro de cada tipo de estímulo); correlación de Spearman entre mitades.

| Medida | Atención | Activación |
|---|---|---|
| AUC sin historial | 0,76 [0,58; 0,86] | 0,66 [0,44; 0,80] |
| AUC con historial | 0,64 [0,40; 0,80] | 0,58 [0,30; 0,78] |
| Ganancia del historial | 0,30 [−0,05; 0,61] | 0,25 [−0,04; 0,51] |

Qué tan detectable es cada persona es un rasgo estable. Cuánto le sirve el historial a cada persona no se puede estimar con fiabilidad: las diferencias individuales en la ganancia son en buena parte ruido.

**(b) Correlatos.** Ninguna característica de la persona (ventanas etiquetadas, cobertura de señales, deriva de la etiqueta, largo de segmentos, duración de la sesión) se asocia con la AUC ni con la ganancia tras Holm (todos los p Holm ≥ 0,23).

**(c) Adaptación a la persona.** Al modelo general se le agregan las ventanas etiquetadas del primer 40 % de la sesión de cada persona evaluada; se evalúa en el resto, con al menos 10 s de separación.

| Tarea | Prueba | ΔAUC | IC 95 % | Mejoran | p Holm | Decisión |
|---|---|---|---|---|---|---|
| Atención | Adaptado − general, sin historial | +0,006 | [+0,000; +0,011] | 25/41 | 0,098 | Nulo concluyente |
| Atención | Adaptado − general, con historial | +0,000 | [−0,007; +0,008] | 19/41 | 0,97 | Nulo concluyente |
| Activación | Adaptado − general, sin historial | +0,028 | [+0,007; +0,049] | 29/40 | 0,050 | Respaldo |
| Activación | Adaptado − general, con historial | +0,045 | [+0,023; +0,069] | 30/40 | 0,0004 | Efecto relevante |

AUC de activación en la parte final de la sesión: general sin historial 0,502; adaptado sin historial 0,530; general con historial 0,543; adaptado con historial 0,587. En el modelo adaptado el historial aporta +0,058 [+0,032; +0,084].

Lectura:
- En activación, conocer a la persona ayuda, y se suma al historial: juntos llevan la AUC de 0,50 a 0,59.
- En atención la adaptación no cambia nada: el modelo general ya sirve igual para todas las personas.
- Es adaptación offline: las etiquetas de calibración se definen con la normalización de toda la sesión, así que contienen información del resto de la sesión. No equivale a una calibración desplegable en línea.

## Límites

- E1: la etiqueta corregida, como la original, usa medianas calculadas con toda la sesión de la persona. Los segmentos son cortos (mediana de 3 ventanas; 17 % de las filas en la primera ventana), lo que limita A2 y A3. El último tramo agrupa todo lo que supera los 32 s.
- E2: sin limpieza de artefactos oculares. El montaje de electrodos (OpenBCI de 16 canales, disposición por defecto) no está verificado en la documentación del experimento: las pruebas B6 y B8 son un supuesto. La correlación con el puntaje ocular no es independiente de la AUC. El control barajado usa una sola repetición.
- E3: usa todas las ventanas del segmento, también las posteriores a cada etiqueta; no es causal. Las variables codifican en parte la duración. La configuración del modelo no se reajustó para unos 1.400 segmentos de entrenamiento. El comparador de C2 (0,567) se conoció al probar el informe antes de correr. 241 segmentos tienen dos o menos ventanas etiquetadas.
- E4c: las personas evaluadas aportan cerca del 5 % de las filas y del 15 % del peso de entrenamiento. La evaluación es sobre la parte final de la sesión, distinta de la de los análisis anteriores. Una persona de activación queda sin evaluación (n = 40).
- Ventanas de 2 s con paso de 1 s: las AUC dentro de una persona no vienen de observaciones independientes; la inferencia es por persona.
- Etiquetas offline y variables transductivas por persona, como en todo el proyecto.

## Auditorías

- Código, antes de ejecutar, por dos agentes independientes: sin hallazgos bloqueantes. Verificaron la etiqueta corregida, la alineación de filas, la ausencia de fuga entre personas y que los informes corren. Sus observaciones originaron la versión 2 del protocolo y la sección de límites.
- Resultados: ver `AUDITORIA_RESULTADOS.md` en esta carpeta.
