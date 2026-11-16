# Cierre experimental V3 — 16-11-2026

Script: `scripts/cierre_experimental_v3.py`. Protocolo v2 registrado y publicado antes de entrenar (commit `82affdb`); la versión 1 se detuvo en el fold 1 de train por una auditoría de código (fusión tardía sin indicadores de faltantes) y se conserva en `../cierre_v3_16-11-2026_abortado_fusion`. Validación y test se evaluaron una sola vez, después de congelar (`congelacion_previa_*.json`).

## Qué cambia respecto de V2

| Mejora | Qué se hizo |
|---|---|
| A. Historial completo | Las ventanas previas salen de todas las ventanas del mismo segmento/estímulo (no solo las etiquetadas). Solo cambia en activación: historial medio de `hasta 32` pasa de 8,5 a 12,6 ventanas en train. En atención casi todo está etiquetado (7,8 en ambos casos). |
| B. Modelo sensible al orden | GRU (proyección 64 + GRU 64, 12 épocas, 3 semillas, sin búsqueda) sobre la secuencia ordenada de hasta 32 ventanas, contra la misma GRU con una ventana. |
| C. Métricas del manuscrito | BA, macro-F1 y recall por clase con umbral fijo 0,5 (`metricas.csv`). La decisión se toma con AUC por persona. |
| D. Fusión tardía | Promedio de probabilidades de un HGB por señal (cada uno con sus indicadores de faltantes) contra la fusión temprana. |
| Control | `hgb_c5`: historial de 5 ventanas, igual al soporte de 6 s de la etiqueta de activación. |

Selección de hojas HGB (7/15) solo con validación interna de train: final 7 en atención y 15 en activación.

## Contrastes principales (ΔAUC por persona, IC 95 % bootstrap, personas que mejoran)

| Tarea | Contraste | Train (OOF, 25) | Validación (8) | Test (8) |
|---|---|---|---|---|
| Atención | HGB hasta 32 − sin historial | +0,018 [+0,009; +0,027] · 20/25 | +0,020 [−0,003; +0,042] · 6/8 | +0,029 [+0,004; +0,052] · 7/8 |
| Atención | GRU hasta 32 − GRU 1 ventana | +0,001 [−0,013; +0,014] · 11/25 | −0,004 [−0,036; +0,028] · 4/8 | +0,010 [−0,019; +0,035] · 5/8 |
| Activación | HGB hasta 32 − sin historial | +0,016 [−0,036; +0,070] · 15/25 | +0,059 [−0,004; +0,131] · 5/8 | +0,033 [−0,021; +0,094] · 4/8 |
| Activación | GRU hasta 32 − GRU 1 ventana | −0,016 [−0,089; +0,048] · 13/25 | +0,091 [+0,018; +0,188] · 6/8 | +0,084 [−0,011; +0,165] · 7/8 |

## Contrastes secundarios

| Tarea | Contraste | Train (OOF) | Validación | Test |
|---|---|---|---|---|
| Atención | HGB 5 − sin historial | +0,014 [+0,006; +0,022] | +0,012 [−0,007; +0,029] | +0,026 [+0,016; +0,038] · 8/8 |
| Atención | HGB 32 − HGB 5 | +0,005 [−0,002; +0,012] | +0,009 [+0,001; +0,017] | +0,003 [−0,017; +0,018] |
| Atención | GRU 32 − HGB 32 | −0,042 [−0,063; −0,022] | −0,044 [−0,092; −0,007] | −0,050 [−0,088; −0,019] |
| Atención | Tardía − temprana (32) | −0,010 [−0,018; −0,003] | −0,008 [−0,020; +0,005] | −0,002 [−0,015; +0,008] |
| Activación | Historial completo − etiquetado (32) | +0,014 [−0,030; +0,060] | +0,068 [+0,004; +0,141] | +0,020 [−0,001; +0,040] |
| Activación | HGB 5 − sin historial | +0,010 [−0,020; +0,038] | −0,019 [−0,084; +0,040] | +0,039 [−0,001; +0,078] |
| Activación | Tardía − temprana (32) | +0,009 [−0,025; +0,042] | −0,107 [−0,223; −0,011] | −0,001 [−0,065; +0,066] |

Tablas completas: `metricas.csv`, `metricas_personas.csv`, `contrastes.csv`, `cobertura_historial.csv`.

## AUC absolutas (test, media por persona)

| Tarea | Sin historial (HGB) | HGB hasta 32 | GRU hasta 32 |
|---|---|---|---|
| Atención | 0,662 [0,619; 0,703] | 0,690 [0,644; 0,733] | 0,640 [0,583; 0,696] |
| Activación | 0,514 [0,451; 0,579] | 0,547 [0,466; 0,623] | 0,583 [0,488; 0,676] |

En activación, todas las AUC de train (OOF) quedan entre 0,50 y 0,53 con intervalos que incluyen 0,5.

## Lectura

**Atención.** El resumen del historial (HGB) mejora en las tres particiones: +0,018, +0,020 y +0,029, con 20/25, 6/8 y 7/8 personas. El intervalo excluye cero en train y test, pero no en validación (por 0,003). Con la regla del manuscrito (excluir cero en validación y test) no alcanza a ser una ventaja consistente, pero es el resultado más estable de toda la tesis. Casi toda la ganancia aparece con 5 ventanas; pasar de 5 a 32 agrega poco. La GRU, que sí usa el orden, no mejora sobre su propio control y queda 0,04–0,05 por debajo del HGB en las tres particiones: con estos datos, el orden no aporta y el modelo secuencial rinde peor que el resumen.

**Activación.** El modelo no aprende la etiqueta en train (AUC 0,50–0,53). Las mejoras de la GRU en validación (+0,091) y test (+0,084) no aparecen en train (−0,016), así que no se pueden tomar como señal. El historial completo ayuda en validación y apenas en test, sin respaldo en train.

**Fusión.** La fusión tardía no supera a la temprana en ninguna tarea; en atención es levemente peor.

**Hipótesis.** Según los criterios del manuscrito, no hay una ventaja consistente del modelo temporal en ninguno de los dos resultados. En atención hay una mejora pequeña y estable del resumen del historial (+0,02 a +0,03 AUC) que no alcanza el criterio por validación; en activación no hay señal.

## Alcance y límites

- Exploratorio: validación y test ya se habían consultado en V2 y las mejoras se diseñaron después. Son 18 contrastes por partición sin corrección por multiplicidad; algunos intervalos que excluyen cero pueden ser azar.
- Bootstrap percentil con 8 personas: la cobertura real puede ser menor al 95 %.
- Variables transductivas por persona (z de GSR y pupila con la sesión completa; componente tónica con filtro bidireccional). El historial es causal por ventana, no por muestra.
- La etiqueta de activación integra 6 s; el control de 5 ventanas existe por eso.
- El PCA del Modelo Profesor de atención se ajustó con las 25 personas de train: fuga leve solo en el OOF de atención.
- Los segmentos son cortos: `hasta 32` rara vez se completa (menos del 2 % de las ventanas).
- La GRU no tuvo búsqueda de hiperparámetros; otra configuración podría rendir distinto.

## Auditorías

- **Código, antes de evaluar:** sin bloqueantes; detectó la falta de indicadores en la fusión tardía (corregida en el protocolo v2) y las limitaciones listadas arriba.
- **Resultados, después de evaluar** (`auditoria_independiente/`): PASA en los seis puntos. Hashes de entradas, modelos y predicciones; congelación previa anterior a la evaluación externa; búsqueda y OOF solo con personas de train; sin solapamiento de personas ni filas; métricas, IC y contrastes recalculados con diferencia 0; modelos HGB y GRU recargados y reentrenados reproducen las predicciones; etiquetas idénticas a las de referencia.
- **Nota de ejecución:** la evaluación de ambas tareas se lanzó en dos procesos paralelos desde un mismo comando (logs `cierre-v3-eval-*.log`); por eso las dos `congelacion_previa_*` comparten timestamp. La única ventaja consistente en validación y test es en contra de la GRU frente al HGB en atención.
