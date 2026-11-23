# Cierre de la experimentación — 22-11-2026

> **Actualización del mismo 22-11-2026.** Horas después de este cierre Mario reabrió la experimentación para obtener conclusiones más firmes. Se corrieron dos fases registradas antes de ejecutar: [informe de la reapertura](../resultados/reapertura_41p_22-11-2026/INFORME.md). Cambios principales: el contraste principal de activación pasa de inconcluso a respaldo (+0,036 [+0,010; +0,065], p Holm 0,021, cinco particiones); la información temporal de activación está en los 6 a 12 s anteriores y desaparece desde 24 s; en atención el pasado no aporta a ningún desfase (nulo concluyente) y la detección desde EEG se mantiene al controlar la posición (0,677). Una [fase 3](../resultados/reapertura_fase3_41p_22-11-2026/INFORME.md) separó historial y posición: en atención el historial no agrega nada sobre la posición (nulo concluyente); en activación agrega +0,032 [+0,004; +0,059], inconcluso tras Holm, y dentro de un mismo estímulo su ventaja se explica por el tiempo transcurrido. La conclusión general sigue siendo apoyo parcial. Lo que sigue es el texto original del cierre.

Este documento declara cerrada la fase experimental de la tesis y reúne en un solo lugar los resultados finales, su trazabilidad y lo que queda abierto. No contiene resultados nuevos: sintetiza los informes ya versionados entre el 16 y el 18 de noviembre de 2026. Ante cualquier diferencia, mandan los `INFORME.md` y `contrastes.csv` de cada carpeta de resultados.

Decisión de cierre: Mario Romero, 22-11-2026. No hay aprobación del profesor guía registrada sobre estos resultados ni sobre el margen práctico de 0,02.

## Qué queda cerrado

- No se entrenan modelos nuevos ni se agregan contrastes sobre estos datos.
- Etiquetas (atención binaria, pseudoetiquetas GSR V2 de activación), particiones por persona y configuración de modelos quedan congeladas.
- Los resultados que se reportan en la tesis son los de la tabla siguiente. Los análisis anteriores (V2, protocolo de potencia, grids de octubre) quedan como historial.

Reabrir la experimentación requiere una decisión explícita y un protocolo registrado antes de correr, como en las etapas anteriores.

## Resultados finales (41 personas, validación cruzada agrupada por persona)

Diferencias de AUC por persona, IC 95 % bootstrap, permutación de signos, corrección de Holm.

| Pregunta | Contraste | Atención | Activación |
|---|---|---|---|
| ¿Ayuda el historial? | HGB hasta 32 ventanas − sin historial | +0,026 [+0,018; +0,035], 36/41, p Holm 0,00001 | +0,034 [−0,001; +0,069], 24/41, p Holm 0,066 |
| ¿Es información temporal? | Historial real − placebo de la misma persona | −0,000 [−0,003; +0,003] | +0,038 [+0,006; +0,068], 26/41, p Holm 0,043 |
| ¿Sin solapamiento con la etiqueta? | Historial desplazado 6 s: real − placebo | −0,003 [−0,005; +0,000], p Holm 0,080 | +0,046 [+0,018; +0,073], 28/41, p Holm 0,004 |
| ¿Lo explica la posición en el estímulo? (post hoc) | Posición sola − sin historial | +0,028 [+0,021; +0,035], 36/41 | −0,004 [−0,024; +0,017] |
| | Historial − posición | −0,002 [−0,006; +0,002] | +0,038 [+0,002; +0,074] |
| ¿Aporta el orden? | GRU 32 − GRU 1 | +0,008 [−0,004; +0,020] | +0,051 [+0,021; +0,080] (secundario, sin corrección) |
| ¿Qué fusión? (MLP) | Tardía − temprana | +0,012 [+0,005; +0,021] | +0,007 [−0,032; +0,042] |

AUC absolutas (media por persona): atención 0,684 sin historial y 0,710 con historial; activación 0,529 y 0,563. La GRU queda 0,040 bajo el HGB en atención.

## Conclusión

Evidencia mixta, con apoyo parcial a la hipótesis de temporalidad.

- **Activación:** hay información temporal real en las señales. El historial mejora la predicción incluso excluyendo los 6 s que definen la etiqueta, el placebo no lo reproduce y la posición en el estímulo no aporta. Las AUC absolutas son bajas (0,56–0,57) y el efecto no alcanza el margen de 0,02 propuesto (límite inferior 0,018).
- **Atención:** la mejora del historial es real y estable, pero no es temporal. Se reproduce entera con una sola variable, los segundos transcurridos en el estímulo, y controlando esa variable el historial no agrega nada. Tampoco es calibración personal (+0,001 a +0,004).
- **Fusión:** la tardía supera a la temprana en atención; sin diferencias en activación.
- **Orden:** la GRU no supera al resumen del historial en atención; en activación el indicio es positivo pero secundario.

## Trazabilidad

Cada etapa se registró y publicó antes de correr.

| Etapa | Registro previo | Resultados | Commit de resultados |
|---|---|---|---|
| Cierre V3 | `82affdb` (v2; v1 abortada por auditoría de código) | `resultados/cierre_v3_16-11-2026` | `005a499` |
| Análisis final 41 personas | `1bbb083` | `resultados/cierre_final_41p_16-11-2026` | `7435fec` |
| Robustez (placebo, sin fuga, particiones) | `6447236` | `resultados/cierre_robustez_41p_16-11-2026` | `550f924` |
| Ampliación E1–E6 | `d2d5530` | `resultados/ampliacion_41p_16-11-2026` | `8c7a6d4` |
| Enmienda E1 (desplazamiento 6 s) | `8beb675` | `resultados/ampliacion_41p_16-11-2026/enmienda_e1_lag6` | `8c7a6d4` |
| Explicativo de posición (post hoc) | `b3eacdc` | `resultados/explicativo_posicion_41p_18-11-2026` | `8c7a6d4` |

Verificado el 22-11-2026: las cinco carpetas tienen todos sus archivos versionados (61, 8, 8, 17 y 5), no había procesos de entrenamiento activos y el repositorio local coincidía con `origin/main` antes de este cierre.

Síntesis para la escritura: `Escritura/Borrador Resultados y Discusión 18-11-2026.md` en el vault. Presentación con resultados finales: `presentaciones/avances_tesis_06-11-2026` (v6).

## Límites que deben ir en la tesis

- La etiqueta de activación es una pseudoetiqueta GSR relativa a la sesión y normalizada offline; no valida una medida psicológica externa.
- El explicativo de posición es post hoc: se registró antes de correr, pero lo motivaron resultados ya vistos.
- E2 (calibración) es transductivo; E4–E6 son descriptivos; los secundarios no llevan corrección por multiplicidad.
- Las 41 personas incluyen las de test consultadas en etapas anteriores: el análisis final no es una confirmación independiente en una cohorte nueva.
- El patrón de atención al inicio del estímulo (prevalencia 0,51 en el primer segundo, 0,37 a los 2–3 s, 0,62 a los 12 s) puede deberse a cómo se construye la etiqueta al cambiar de página.

## Queda abierto (no es experimentación)

1. Escritura del manuscrito a partir del borrador del 18-11.
2. Decisiones con el profesor guía: margen práctico de 0,02 (propuesta, no aprobado) y redacción del "apoyo parcial".
3. Revisión de la presentación v6.
