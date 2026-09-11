# Segunda iteración: combinación de probabilidades

08-09-2026. Se ejecuta después de observar la primera búsqueda; es exploratoria.
Se combina logística fija con el candidato temporal de cada fold. Peso temporal elegido
entre 0/0,25/0,5/0,75/1 por los mismos tres folds internos. Un control usa siempre 0,5.
Los pesos se congelan antes de evaluar las combinaciones en los folds externos.
No se usa validation/test original ni se elige entre ambas reglas por sus métricas OOF.

| scope | macro_score | balanced_accuracy | macro_f1 |
|---|---|---|---|
| fixed_half | 0.3534 | 0.3539 | 0.3510 |
| selected | 0.3525 | 0.3540 | 0.3521 |

| scope | reference | mean_delta | ci_low | ci_high | positive_participants |
|---|---|---|---|---|---|
| selected | all | -0.0021 | -0.0100 | 0.0048 | 10 |
| selected | fixed_logistic | -0.0011 | -0.0125 | 0.0100 | 14 |
| fixed_half | all | -0.0012 | -0.0101 | 0.0076 | 11 |
| fixed_half | fixed_logistic | -0.0002 | -0.0082 | 0.0076 | 14 |

Los intervalos son descriptivos: 2.000 remuestreos pareados de personas, media previa
entre semillas, sin ajuste por dependencia de folds ni por comparaciones múltiples.
La adaptación entre iteraciones sobre train sigue limitando la interpretación.

| fold | weight | inner_score |
|---|---|---|
| 1.0000 | 0.7500 | 0.3578 |
| 2.0000 | 1.0000 | 0.3590 |
| 3.0000 | 1.0000 | 0.3534 |
| 4.0000 | 1.0000 | 0.3430 |
| 5.0000 | 0.7500 | 0.3667 |

Se conservan 20 bundles `.joblib` con ambos pipelines, representación, suavizado y peso;
54.096 predicciones externas verificadas tras recargar, predicciones internas para
recalcular los 75 puntajes de pesos, catálogo y resultados por persona. Se realizaron
30 ajustes internos adicionales; los componentes externos reutilizan la primera búsqueda.
La combinación usa las probabilidades ordenadas bajo/medio/alto. Antes de combinarlas,
aplicar al componente temporal su representación y su suavizado causal.

Código: `scripts/combinar_historial.py`. Requiere la primera búsqueda completa.
La carpeta de esta segunda ejecución debe ser nueva; el script conserva la anterior.
