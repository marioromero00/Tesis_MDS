# Tercera iteración: fusión temprana con mirada y EEG

08-09-2026. Seguimiento exploratorio después de ver los dos intentos pupilares.
Se mantiene la etiqueta GSR de activación y la división original. Inputs actuales de mirada
(10) más pupila (5), con/sin EEG (9). Alternativa temporal: los cinco valores pupilares
actuales más sus 16 estadísticas de historia, concatenados con mirada/EEG actuales.
No se incluye GSR ni fracción de validez pupilar en las entradas.

48 candidatos: cuatro representaciones, cuatro estimadores y suavizado causal 1/4/8.
Los estimadores y las reglas causales son los de la primera búsqueda. Cinco folds externos,
tres internos, selección por media de BA macro interna y dos semillas de reajuste externo.
Se congelan las 15 selecciones antes de evaluar. `all` busca en 48, `current` en ocho
y `temporal` en 40. No se selecciona una regla usando sus resultados externos.

| scope | macro_score | balanced_accuracy | macro_f1 |
|---|---|---|---|
| all | 0.3527 | 0.3533 | 0.3524 |
| current | 0.3438 | 0.3419 | 0.3413 |
| temporal | 0.3527 | 0.3533 | 0.3524 |

| scope | reference | mean_delta | ci_low | ci_high | positive_participants |
|---|---|---|---|---|---|
| all | previous_all | -0.0019 | -0.0216 | 0.0200 | 11 |
| all | previous_fixed_logistic | -0.0009 | -0.0175 | 0.0174 | 12 |
| temporal | previous_all | -0.0019 | -0.0216 | 0.0200 | 11 |
| temporal | previous_fixed_logistic | -0.0009 | -0.0175 | 0.0174 | 12 |
| current | previous_all | -0.0108 | -0.0255 | 0.0044 | 10 |
| current | previous_fixed_logistic | -0.0097 | -0.0218 | 0.0013 | 10 |

| fold | scope | representation | estimator | smoothing | inner_score |
|---|---|---|---|---|---|
| 1 | all | full__current | logistic_1 | 8 | 0.3602 |
| 1 | current | full__current | logistic_0.1 | 1 | 0.3574 |
| 1 | temporal | full__current | logistic_1 | 8 | 0.3602 |
| 2 | all | full__recording_8 | logistic_0.1 | 8 | 0.3550 |
| 2 | current | full__current | logistic_0.1 | 1 | 0.3473 |
| 2 | temporal | full__recording_8 | logistic_0.1 | 8 | 0.3550 |
| 3 | all | full__current | hgb | 8 | 0.3561 |
| 3 | current | eye__current | rbf | 1 | 0.3403 |
| 3 | temporal | full__current | hgb | 8 | 0.3561 |
| 4 | all | full__current | hgb | 4 | 0.3395 |
| 4 | current | eye__current | rbf | 1 | 0.3393 |
| 4 | temporal | full__current | hgb | 4 | 0.3395 |
| 5 | all | eye__current | rbf | 4 | 0.3556 |
| 5 | current | eye__current | rbf | 1 | 0.3445 |
| 5 | temporal | eye__current | rbf | 4 | 0.3556 |

240 ajustes internos, 720 puntuaciones guardadas y 30 pipelines externos recargados;
81.144 predicciones verificadas. Cada pipeline usa 20 participantes. Reconstruir entradas
con `inputs(frame, meta['representation'])`, cargar `.joblib`, aplicar `probabilities`
y `smooth` con el contexto del catálogo. Ordenar frame por persona/grabación/timestamp.
Imputación, escalado y aproximación RBF se ajustan dentro de cada pipeline en entrenamiento.

Intervalos descriptivos del 95%, 2.000 remuestreos pareados de personas tras promediar semillas.
No corrigen adaptación entre iteraciones, comparaciones múltiples ni dependencia de folds.
Validation/test originales sin nueva evaluación. Normalización y pseudoetiquetas offline.
Los conjuntos mayores prueban una ampliación del problema, no demuestran que más sensores
sean necesarios. Una mejora sobre pupila no aislaría el aporte de historial frente al de
modalidades. Código reproducible: `scripts/fusion_modalidades.py`, carpeta nueva obligatoria.
