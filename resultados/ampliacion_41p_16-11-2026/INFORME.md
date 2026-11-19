# Ampliación experimental E1–E6 — 41 personas (16-18/11/2026)

Script `scripts/ampliacion_41p.py`, registrado antes de correr (commit `d2d5530`). Enmienda de E1 a 6 ventanas registrada antes de ver resultados (`enmienda_e1_lag6/`, commit `8beb675`) tras auditoría de código. Mismos 8 folds y configuración congelada del análisis final. Sin hgb_c1 nuevo: se reutiliza del análisis final.

## E1 — ¿Hay información temporal más allá de la etiqueta? (principal, Holm sobre 2 tareas)

Historial que excluye las ventanas más recientes contra un placebo con el mismo número de ventanas de la misma persona en otros estímulos.

| Tarea | Desplazamiento | Real − placebo | IC 95 % | Mejoran | p Holm | Real − sin historial |
|---|---|---|---|---|---|---|
| Activación | 6 ventanas (principal; sin solapamiento con la etiqueta) | **+0,046** | [+0,018; +0,073] | 28/41 | **0,004** | +0,053 [+0,022; +0,083] |
| Activación | 5 ventanas (secundario; 1 s de solapamiento) | +0,040 | [+0,013; +0,066] | 29/41 | 0,013 | +0,041 [+0,011; +0,071] |
| Atención | 6 ventanas | −0,003 | [−0,005; +0,000] | 17/41 | 0,080 | +0,008 [+0,002; +0,015] |
| Atención | 5 ventanas | −0,002 | [−0,005; +0,000] | 13/41 | 0,088 | +0,009 [+0,002; +0,016] |

Cobertura con 6 ventanas: el 73 % de las filas de activación y el 40 % de las de atención tienen historial desplazado.

**Lectura:** en activación, la señal de los segundos anteriores (sin tocar los 6 s que definen la etiqueta) mejora la predicción y el placebo no la reproduce: respaldo según la regla registrada (no "relevante": límite inferior 0,018 < 0,02). En atención no hay información temporal.

## E2 — Calibración personal (secundario)

Ventana actual + media/desviación de las ventanas de la persona en los primeros M de la sesión. Por el anclaje de la grabación, "30 s" equivale a las primeras 5 ventanas y "1 min" a unas 15.

| Tarea | 30 s | 1 min | 2 min | 5 min | Sesión |
|---|---|---|---|---|---|
| Atención | +0,002 | +0,001 | +0,004 [+0,001; +0,007] | +0,002 | +0,003 |
| Activación | +0,001 | +0,006 | +0,006 | +0,009 | +0,005 |

Conocer a la persona no explica la mejora del historial (que era +0,026 en atención).

## E3 — Tipos de fusión con la misma familia (MLP, secundario)

| Tarea | Intermedia − temprana | Intermedia − tardía | Tardía − temprana |
|---|---|---|---|
| Atención | +0,005 [−0,003; +0,013] | −0,008 [−0,014; −0,001] | **+0,012 [+0,005; +0,021]** |
| Activación | +0,002 [−0,019; +0,023] | −0,004 [−0,042; +0,039] | +0,007 [−0,032; +0,042] |

En atención la fusión tardía supera a la temprana y a la intermedia; en activación no hay diferencias. La intermedia es más profunda que la temprana, así que compara tipo de fusión y capacidad.

## E4 — Evolución en la sesión (descriptivo, `fatiga_por_quintil.csv`)

- Atención: la AUC sube del primer al último quintil (0,65 → 0,71 sin historial; 0,69 → 0,74 con historial). La prevalencia de "alta" cae a 0,32 en el tercer quintil, que coincide con un bloque de estímulos común a las secuencias.
- Activación: la prevalencia de "alta" baja a 0,37 en el último quintil, compatible con habituación; la AUC con historial es mayor al final (0,64).

## E5 — Importancia por bloques (descriptivo, caída de AUC al permutar)

- Atención: EEG 0,207, GSR 0,004; ventana actual 0,157, desviación del historial 0,035, media 0,018; bandas theta 0,018 y delta 0,017 por sobre beta, alfa y gamma.
- Activación: EEG 0,053, media del historial 0,050, pupila 0,021, mirada ~0; bandas sin efecto claro.

## E6 — Por tipo de página (descriptivo, AUC media por persona)

| Tarea | Sitio web | Numerado | Diseño | Emotion | Blur | Texto |
|---|---|---|---|---|---|---|
| Atención sin historial | 0,707 | 0,681 | 0,649 | 0,668 | 0,696 | 0,604 |
| Atención con historial | 0,710 | 0,698 | 0,637 | 0,667 | 0,599 | 0,633 |
| Activación sin historial | 0,525 | 0,588 | 0,506 | — | — | 0,506 |
| Activación con historial | 0,588 | 0,591 | 0,506 | — | — | 0,524 |

En activación, el historial mejora sobre todo en sitios web. Categorías con pocas personas o ventanas (blur, emotion) son poco fiables.

## Límites declarados

E2 es transductivo (usa ventanas sin etiqueta de la persona, en M ≥ 2 min incluso posteriores). E5 permuta filas entre personas y los bloques de banda no incluyen sus indicadores. E4–E6 son descriptivos. Ver además los límites del análisis final y del protocolo V3.
