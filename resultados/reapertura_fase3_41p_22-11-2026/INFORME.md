# Reapertura, fase 3: historial frente a posición en el estímulo — 22-11-2026

Script `scripts/reapertura_fase3_41p.py`. Protocolo registrado y publicado antes de correr (commit `7046d92`), ejecutado una vez. Pedido por Mario después de ver las fases 1 y 2: es un análisis dirigido, no una confirmación independiente.

**Pregunta:** cuando el modelo ya conoce cuántos segundos lleva la persona en el estímulo, ¿el historial agrega algo?

Dos modelos nuevos en las mismas 5 particiones de la fase 1, con la configuración congelada: ventana actual + posición, e historial hasta 32 + posición. La AUC de cada persona se promedia sobre las 5 particiones. Holm sobre las 4 pruebas.

## Resultado confirmatorio

Contraste: (historial + posición) − (ventana actual + posición).

| Tarea | Prueba | ΔAUC | IC 95 % | Mejoran | p | p Holm | Decisión |
|---|---|---|---|---|---|---|---|
| Atención | Q1 todas las comparaciones | +0,001 | [−0,002; +0,005] | 21/41 | 0,41 | 1,00 | **Nulo concluyente** |
| Atención | Q2 dentro del mismo estímulo | −0,000 | [−0,003; +0,003] | 22/41 | 0,97 | 1,00 | **Nulo concluyente** |
| Activación | Q1 todas las comparaciones | +0,032 | [+0,004; +0,059] | 28/41 | 0,027 | 0,108 | Inconcluso |
| Activación | Q2 dentro del mismo estímulo | +0,009 | [−0,020; +0,037] | 20/41 | 0,57 | 1,00 | Inconcluso |

En activación Q1 el intervalo sin ajustar queda sobre cero, pero no pasa la corrección de Holm sobre las cuatro pruebas. Según la regla registrada es inconcluso.

Sensibilidad (descriptiva, sin ajuste), quitando la persona más influyente:

| Prueba | Mediana | Persona | Sin esa persona |
|---|---|---|---|
| Atención Q1 | +0,001 | P36 (+0,038) | +0,001 [−0,002; +0,003] |
| Atención Q2 | +0,001 | P46 (−0,024) | +0,001 [−0,002; +0,003] |
| Activación Q1 | +0,031 | P10 (−0,241) | +0,039 [+0,015; +0,063], p 0,004 |
| Activación Q2 | −0,001 | P44 (−0,231) | +0,015 [−0,012; +0,042] |

En activación Q1 la media y la mediana coinciden (+0,032 y +0,031) y la persona más influyente empuja en contra.

## Qué aporta cada cosa

AUC media por persona, 5 particiones.

| Modelo | Atención | Activación | Activación, mismo estímulo |
|---|---|---|---|
| Ventana actual | 0,683 | 0,518 | 0,501 |
| Ventana actual + posición | 0,711 | 0,523 | 0,550 |
| Historial hasta 32 | 0,712 | 0,554 | 0,555 |
| Historial + posición | 0,713 | 0,555 | 0,559 |

| Contraste | Atención | Activación | Activación, mismo estímulo |
|---|---|---|---|
| Posición sola: (actual + posición) − actual | +0,028 [+0,021; +0,036] | +0,006 [−0,015; +0,026] | **+0,049 [+0,027; +0,072]** |
| Historial − (actual + posición) | +0,001 [−0,003; +0,004] | +0,031 [+0,004; +0,057] | +0,005 [−0,026; +0,035] |

Otros estratos, contraste confirmatorio: dentro del mismo minuto, atención −0,000 [−0,004; +0,003] y activación +0,033 [+0,005; +0,062]; a igual posición, atención +0,005 [+0,001; +0,010] y activación +0,026 [−0,000; +0,052].

## Lectura

**Atención: cerrado.** Con la posición como variable, el historial no agrega nada, ni en general ni dentro de un mismo estímulo. Un modelo con la ventana actual y un solo número (los segundos en el estímulo) rinde lo mismo que el modelo con todo el historial (0,711 frente a 0,712). La mejora del historial en atención es la posición.

**Activación: dos componentes distintos.**
- *Dentro de un mismo estímulo*, lo que mejora la predicción es el tiempo transcurrido (+0,049) y el historial no lo supera. Aquí la ventaja del historial se explica por la posición.
- *Entre estímulos*, la posición no aporta (+0,006) y el historial sí (+0,031, +0,032 con ambos modelos conociendo la posición). Esta parte no se explica por la posición, pero no alcanza el criterio registrado tras la corrección por cuatro pruebas.

Lo que el historial aporta en activación más allá de la posición es, entonces, distinguir entre momentos de estímulos distintos: un mejor resumen del estado de los últimos segundos. No es evidencia de dinámica dentro del estímulo.

**Hipótesis.** Atención: sin información temporal, con nulo concluyente. Activación: efecto del historial confirmado en la fase 1; su parte independiente de la posición es positiva y pareja entre personas, pero queda inconclusa bajo la regla registrada.

## Límites

- El contraste mide lo que agregan la media y la desviación de hasta 32 ventanas, que incluyen la actual. Una diferencia positiva puede venir de suavizar el estado actual, de una línea base local o de la identidad del estímulo. Por eso se habla de "resumen del historial reciente" y no de dinámica.
- En atención los segmentos son cortos (mediana de posición 5; el 17 % de las filas está en la primera ventana, donde ambos modelos tienen la misma información). El nulo vale para historiales de 2 a 10 ventanas en la práctica.
- La AUC dentro del mismo estímulo usa el 2–3 % de los pares y es desigual entre personas. En activación tiene poca potencia: su resultado inconcluso no demuestra ausencia de efecto.
- "Posición en el estímulo" es la posición en el segmento contiguo: empieza en 1, llega como máximo a 32 y coincide con los segundos desde el inicio del segmento en todas las filas (no hay huecos dentro de los segmentos).
- Análisis dirigido sobre personas y resultados ya vistos. Etiquetas offline y variables transductivas por persona, como en las fases anteriores.

## Auditorías

- Código, por un agente independiente con las corridas en marcha y sin ver resultados: sin hallazgos bloqueantes. Los modelos nuevos difieren de los de la fase 1 solo en la columna de posición; sin fuga entre personas ni entradas prohibidas. Sus advertencias de interpretación están en la sección de límites. Se verificó aparte que los datos de origen de la fase 1 no cambiaron.
- Resultados, por otro agente independiente con código propio: pasa los cuatro puntos (cifras reproducidas exactamente, integridad, hashes y cronología del registro). Detalle en `AUDITORIA_RESULTADOS.md`. Una persona (P4) tiene solo 4 pares dentro del mismo estímulo en activación; pesa igual que las demás en Q2.
