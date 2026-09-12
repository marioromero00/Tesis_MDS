# Mezclas posteriores al diagnóstico de stacking: 11-09-2026

Auditoría de entrega adicional: se recalcularon desde el CSV guardado las 30 métricas
de fold y 150 por participante; coincidieron con tolerancia 1e-12. Se verificaron los
hashes de los 140 modelos de ambas rondas, la cadena de fuentes y que el plan precediera
al cálculo. Registro: `auditoria_entrega.json`; inventario: `inventario_entrega.json`.

Se probaron tres mezclas fijas de pool_fixed_history y stack_participant_C0.01: 5 %, 10 %
y 25 % del segundo. El 10 % es el contraste principal declarado en plan.json antes de
calcular las predicciones mezcladas. Esta ronda es adaptativa: se diseñó después de
observar BA macro 0,3685 y recall de medio 0,0641 en el stacking. No es confirmación
independiente ni ajuste de pesos con una validación interna nueva.

## Resultados

Promedio de dos semillas sobre las mismas 25 personas de train, evaluadas por cinco folds.
La referencia anterior de fusión geométrica es 0,3651 de BA macro.

| scope | macro_score | balanced_accuracy | macro_f1 |
|---|---|---|---|
| stack_weight_0.05 | 0.3684 | 0.3678 | 0.3677 |
| stack_weight_0.1 | 0.3687 | 0.3676 | 0.3676 |
| stack_weight_0.25 | 0.3716 | 0.3691 | 0.3681 |

| scope | mean_delta | ci_low | ci_high | positive_participants | tied_participants |
|---|---|---|---|---|---|
| stack_weight_0.05 | 0.0033 | -0.0032 | 0.0109 | 14 | 0 |
| stack_weight_0.1 | 0.0036 | -0.0030 | 0.0114 | 12 | 1 |
| stack_weight_0.25 | 0.0065 | -0.0031 | 0.0171 | 15 | 0 |

| scope | label | predicted_fraction | recall |
|---|---|---|---|
| stack_weight_0.05 | alto | 0.3187 | 0.3358 |
| stack_weight_0.05 | bajo | 0.3555 | 0.4100 |
| stack_weight_0.05 | medio | 0.3258 | 0.3575 |
| stack_weight_0.1 | alto | 0.3227 | 0.3403 |
| stack_weight_0.1 | bajo | 0.3649 | 0.4191 |
| stack_weight_0.1 | medio | 0.3124 | 0.3433 |
| stack_weight_0.25 | alto | 0.3421 | 0.3657 |
| stack_weight_0.25 | bajo | 0.3958 | 0.4534 |
| stack_weight_0.25 | medio | 0.2621 | 0.2881 |

Los intervalos son descriptivos: 2.000 remuestreos pareados por persona, sin corregir
las búsquedas repetidas ni la dependencia entre folds. Las mejoras por persona se
cuentan con tolerancia 1e-12. Evaluar BA junto con el recall de medio evita ocultar una
pérdida de reconocimiento de esa clase detrás de una subida del promedio.

## Auditoría y archivos

No se reentrenan modelos ni se cambian etiquetas. Cada bundle contiene los dos modelos
fuente y el peso fijo; las predicciones se calculan desde esos objetos y se exigen
idénticas después de recargarlos. Se comprobaron los hashes y salidas de los 20 modelos
fuente, se recargaron los 30 bundles nuevos y se verificaron 81,144 predicciones.
El guardado se volvió a leer antes de calcular los resúmenes. Protocolos, catálogo,
métricas, diagnósticos y diferencias por persona están en resultados/mezclas_ensambles_11-09-2026.

Validation y test originales no se vuelven a evaluar. Continúan las limitaciones de
normalización offline y pseudoetiquetas. No se elige retrospectivamente el mayor peso
por su resultado externo. La comparación de esta grilla pequeña sigue siendo exploratoria.

Código reproducible: scripts/mezclas_ensambles.py --output resultados/NUEVA_MEZCLA.
Requiere la ronda de ensambles y un directorio con plan.json, sin subcarpeta modelos
existente; se puede copiar el plan conservado para repetir exactamente sus pesos.
Para cargar, agregar scripts
al path, usar joblib.load y mezclas_ensambles.predict(bundle, frame), con el frame ordenado
por persona/grabación/timestamp; no necesita etiquetas. El código conserva las rutas de
los modelos fuente para mantener el linaje de esta entrega.
