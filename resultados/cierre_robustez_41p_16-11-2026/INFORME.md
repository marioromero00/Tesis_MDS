# Pruebas de robustez del análisis final — 16-11-2026

Script: `scripts/cierre_robustez_41p.py`. Registrado y publicado antes de correr (commit `6447236`), ejecutado una vez. Misma configuración congelada, sin búsqueda. Se verificó que el historial placebo no comparte ninguna ventana con el real (0 % de filas) y que sus predicciones difieren (correlación 0,94 en atención y 0,50 en activación).

## Resultados (41 personas, ΔAUC por persona)

| Tarea | Prueba | Contraste | ΔAUC | IC 95 % | Mejoran | p (Holm en R1) |
|---|---|---|---|---|---|---|
| Atención | R1 placebo | historial real − placebo | **−0,000** | [−0,003; +0,003] · IC 90 % [−0,003; +0,003] | 18/41 | 0,93 |
| Atención | R1 referencia | placebo − sin historial | +0,027 | [+0,018; +0,035] | 34/41 | — |
| Atención | R2 sin fuga | hasta 32 − sin historial | +0,024 | [+0,015; +0,034] | 34/41 | — |
| Atención | R3 particiones | hasta 32 − sin historial | +0,026 a +0,030 | todas con límite inferior ≥ +0,019 | 35–37/41 | — |
| Activación | R1 placebo | historial real − placebo | **+0,038** | [+0,006; +0,068] | 26/41 | 0,043 |
| Activación | R1 referencia | placebo − sin historial | −0,004 | [−0,030; +0,024] | 16/41 | — |
| Activación | R3 particiones | hasta 32 − sin historial | +0,042 a +0,043 | todas con límite inferior > 0 (+0,006 a +0,013) | 25–28/41 | — |

## Lectura

**Atención: la mejora es real, pero no es temporal.** Pasa R2 (sin fuga de etiquetas) y R3 (estable en tres particiones), pero falla R1: un historial armado con ventanas de la misma persona tomadas de otros momentos y estímulos da exactamente la misma mejora que el historial real. El IC 90 % de la diferencia ([−0,003; +0,003]) queda muy dentro de ±0,02, así que hay un **nulo concluyente para la información temporal**: lo que ayuda es tener más contexto de la persona (una especie de calibración individual), no lo que pasó justo antes. Según la regla registrada, la conclusión de atención **no es robusta como efecto temporal**.

**Activación: hay información temporal.** El historial real supera al placebo (+0,038, p Holm 0,043) y el placebo no aporta nada sobre el modelo sin historial (−0,004). El contraste principal es positivo en las tres particiones alternativas (+0,042 en las tres, límites inferiores sobre cero), aunque en la partición registrada originalmente el intervalo tocaba cero. Hay que leerlo con cuidado: la etiqueta de activación integra los últimos 6 s de GSR, así que el historial de las otras señales coincide en el tiempo con lo que define la etiqueta. Es información temporal, pero ligada a cómo se construyó la etiqueta.

## Conclusión respecto de la hipótesis

- **Atención:** el historial no aporta información temporal (nulo concluyente frente al placebo). La mejora de +0,026 AUC se explica por contexto de la persona.
- **Activación:** el historial reciente aporta una mejora pequeña (+0,03 a +0,04 AUC) que no se explica por contexto de la persona, con modelos que en términos absolutos siguen cerca del azar (AUC 0,56–0,58) y con la salvedad del soporte temporal de la etiqueta.
- En conjunto, con los criterios del manuscrito: **evidencia mixta, apoyo parcial**, pero con el signo invertido respecto de lo que sugería el análisis sin placebo: el apoyo viene de activación, no de atención.
