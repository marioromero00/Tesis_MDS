# Auditoría de selección y ensambles: 11-09-2026

El contraste principal, selección interna de promedios, obtiene BA macro **0.3595**.
Frente a la fusión geométrica anterior (0,3651), la diferencia es -0.56
puntos porcentuales, intervalo descriptivo [-1.89; +0.83],
con mejora en 11/25 personas. El mayor promedio observado entre
los contrastes de esta ronda es 0.3685, de stack_participant_C0.01; no se convierte por
ello en una elección validada independientemente.

## Qué mostró la auditoría de selección anterior

La auditoría numérica anterior verificó modelos y métricas. Esta auditoría adicional
examina cuánto cambia el ranking de configuraciones entre particiones internas.
Un empate cuenta como acuerdo con el ganador; una brecha interna-externa también refleja
que se evalúan personas distintas y no estima por sí sola el sesgo de sobreajuste.

| fold | scope | runner_up_margin | inner_winner_agreements | inner_score | outer_score | inner_outer_gap |
|---|---|---|---|---|---|---|
| 1 | all | 0.0020 | 1 | 0.3702 | 0.3429 | 0.0274 |
| 1 | fusion | 0.0016 | 1 | 0.3529 | 0.3393 | 0.0136 |
| 2 | all | 0.0006 | 0 | 0.3723 | 0.3533 | 0.0191 |
| 2 | fusion | 0.0006 | 1 | 0.3723 | 0.3533 | 0.0191 |
| 3 | all | 0.0045 | 2 | 0.3529 | 0.3791 | -0.0262 |
| 3 | fusion | 0.0045 | 2 | 0.3529 | 0.3791 | -0.0262 |
| 4 | all | 0.0010 | 0 | 0.3685 | 0.3695 | -0.0011 |
| 4 | fusion | 0.0002 | 0 | 0.3402 | 0.3378 | 0.0023 |
| 5 | all | 0.0005 | 0 | 0.3504 | 0.3292 | 0.0213 |
| 5 | fusion | 0.0013 | 1 | 0.3412 | 0.3778 | -0.0366 |

La correlación de Spearman media entre rankings internos es 0.0690;
el detalle por fold y par está en auditoria_ranking.csv. Estos diagnósticos se recalcularon.
Las tres reglas constantes de referencias_constantes.csv explicitan el nivel trivial
con la métrica por persona y sus clases observadas; no se selecciona una constante por
su resultado externo. No se presupone que toda regla constante tenga BA macro 1/3.

## Qué se probó

- Promedio aritmético o geométrico de varias regularizaciones de fusión logística
  (C=0,001/0,01/0,1/1) y LDA (shrinkage=0,1/0,5/0,9), por separado o juntas.
- Ventana actual, historial de ocho ventanas y mezclas de ambos: peso del historial
  0/0,25/0,5/0,75/1. Suavizado causal de una o cuatro ventanas. Son 60 configuraciones.
  En la mezcla conjunta, cada modelo de una escala recibe el mismo peso: logística
  representa 4/7 y LDA 3/7 del peso de esa escala.
- Tres reglas seleccionadas internamente: pool_selected, pool_logistic y pool_lda.
  Dos controles fijos: promedio de los siete modelos con historial y promedio de los
  catorce modelos entre ambas escalas, ambos sin suavizado adicional.
- Stacking: una logística recibe las 42 probabilidades de 14 modelos base. Se fijan
  seis contrastes (C=0,001/0,01/0,1, pesos globales o por persona), sin elegir C ni pesos
  usando los resultados externos. No se aplica suavizado adicional al stacking.

Cada modelo base ya fusiona geométricamente pupila, mirada y EEG. No se introduce GSR
como predictor ni se cambian etiquetas. Los coeficientes del combinador están guardados;
son asociaciones con salidas de modelos correlacionadas, no importancia causal de sensores.

El stacking usa exclusivamente predicciones OOF de las personas de ajuste: cada fila fue
predicha por modelos base entrenados sin esa persona. La matriz se conserva y su linaje
se verifica contra los NPZ originales. El combinador se ajusta en las 20 personas del fold;
los modelos base se reajustan en esas 20 para predecir las cinco externas. No se utiliza
la opción prefit con predicciones sobre las mismas filas usadas para ajustar los modelos.
Este diseño sigue el principio de entrenamiento cruzado de la
[documentación oficial de stacking](https://scikit-learn.org/stable/auto_examples/ensemble/plot_stack_predictors.html),
implementando explícitamente las particiones por persona. Las probabilidades resultantes
no cuentan con una calibración externa independiente.

## Resultados

Promedio de dos semillas; los clasificadores deterministas no generan dos réplicas
independientes por cambiar la semilla.

| scope | macro_score | balanced_accuracy | macro_f1 |
|---|---|---|---|
| pool_fixed_history | 0.3663 | 0.3662 | 0.3658 |
| pool_fixed_multiscale | 0.3629 | 0.3634 | 0.3627 |
| pool_lda | 0.3602 | 0.3580 | 0.3560 |
| pool_logistic | 0.3608 | 0.3599 | 0.3579 |
| pool_selected | 0.3595 | 0.3597 | 0.3573 |
| stack_global_C0.001 | 0.3613 | 0.3600 | 0.3584 |
| stack_global_C0.01 | 0.3650 | 0.3642 | 0.3635 |
| stack_global_C0.1 | 0.3530 | 0.3564 | 0.3553 |
| stack_participant_C0.001 | 0.3671 | 0.3546 | 0.3133 |
| stack_participant_C0.01 | 0.3685 | 0.3559 | 0.3201 |
| stack_participant_C0.1 | 0.3586 | 0.3504 | 0.3266 |

| scope | reference | mean_delta | ci_low | ci_high | positive_participants |
|---|---|---|---|---|---|
| pool_selected | previous_geometric | -0.0056 | -0.0189 | 0.0083 | 11 |
| pool_selected | previous_tuned_logistic | -0.0011 | -0.0096 | 0.0071 | 14 |
| pool_logistic | previous_geometric | -0.0043 | -0.0174 | 0.0078 | 12 |
| pool_logistic | previous_tuned_logistic | 0.0002 | -0.0051 | 0.0049 | 15 |
| pool_lda | previous_geometric | -0.0049 | -0.0179 | 0.0088 | 11 |
| pool_lda | previous_tuned_logistic | -0.0003 | -0.0163 | 0.0162 | 13 |
| pool_fixed_history | previous_geometric | 0.0012 | -0.0051 | 0.0080 | 9 |
| pool_fixed_history | previous_tuned_logistic | 0.0057 | -0.0099 | 0.0215 | 16 |
| pool_fixed_multiscale | previous_geometric | -0.0022 | -0.0103 | 0.0059 | 12 |
| pool_fixed_multiscale | previous_tuned_logistic | 0.0024 | -0.0121 | 0.0170 | 14 |
| stack_global_C0.001 | previous_geometric | -0.0037 | -0.0286 | 0.0211 | 12 |
| stack_global_C0.001 | previous_tuned_logistic | 0.0008 | -0.0207 | 0.0223 | 15 |
| stack_global_C0.01 | previous_geometric | -0.0001 | -0.0248 | 0.0250 | 13 |
| stack_global_C0.01 | previous_tuned_logistic | 0.0044 | -0.0175 | 0.0263 | 15 |
| stack_global_C0.1 | previous_geometric | -0.0121 | -0.0365 | 0.0130 | 12 |
| stack_global_C0.1 | previous_tuned_logistic | -0.0076 | -0.0316 | 0.0164 | 11 |
| stack_participant_C0.001 | previous_geometric | 0.0020 | -0.0295 | 0.0357 | 9 |
| stack_participant_C0.001 | previous_tuned_logistic | 0.0066 | -0.0220 | 0.0355 | 15 |
| stack_participant_C0.01 | previous_geometric | 0.0034 | -0.0311 | 0.0410 | 11 |
| stack_participant_C0.01 | previous_tuned_logistic | 0.0080 | -0.0250 | 0.0427 | 14 |
| stack_participant_C0.1 | previous_geometric | -0.0065 | -0.0395 | 0.0292 | 12 |
| stack_participant_C0.1 | previous_tuned_logistic | -0.0019 | -0.0339 | 0.0328 | 13 |

| scope | label | predicted_fraction | global_recall |
|---|---|---|---|
| pool_fixed_history | alto | 0.3168 | 0.3310 |
| pool_fixed_history | bajo | 0.3445 | 0.3962 |
| pool_fixed_history | medio | 0.3387 | 0.3713 |
| pool_fixed_multiscale | alto | 0.3029 | 0.3173 |
| pool_fixed_multiscale | bajo | 0.3505 | 0.3954 |
| pool_fixed_multiscale | medio | 0.3466 | 0.3776 |
| pool_lda | alto | 0.2935 | 0.3040 |
| pool_lda | bajo | 0.3270 | 0.3649 |
| pool_lda | medio | 0.3795 | 0.4052 |
| pool_logistic | alto | 0.2744 | 0.2818 |
| pool_logistic | bajo | 0.3609 | 0.4030 |
| pool_logistic | medio | 0.3647 | 0.3950 |
| pool_selected | alto | 0.2687 | 0.2800 |
| pool_selected | bajo | 0.3560 | 0.3964 |
| pool_selected | medio | 0.3753 | 0.4028 |
| stack_global_C0.001 | alto | 0.2728 | 0.2798 |
| stack_global_C0.001 | bajo | 0.3950 | 0.4522 |
| stack_global_C0.001 | medio | 0.3322 | 0.3481 |
| stack_global_C0.01 | alto | 0.2904 | 0.3013 |
| stack_global_C0.01 | bajo | 0.3738 | 0.4359 |
| stack_global_C0.01 | medio | 0.3358 | 0.3556 |
| stack_global_C0.1 | alto | 0.3012 | 0.3099 |
| stack_global_C0.1 | bajo | 0.3378 | 0.3751 |
| stack_global_C0.1 | medio | 0.3610 | 0.3841 |
| stack_participant_C0.001 | alto | 0.4661 | 0.4873 |
| stack_participant_C0.001 | bajo | 0.4875 | 0.5276 |
| stack_participant_C0.001 | medio | 0.0464 | 0.0489 |
| stack_participant_C0.01 | alto | 0.4607 | 0.4814 |
| stack_participant_C0.01 | bajo | 0.4783 | 0.5222 |
| stack_participant_C0.01 | medio | 0.0610 | 0.0641 |
| stack_participant_C0.1 | alto | 0.4434 | 0.4583 |
| stack_participant_C0.1 | bajo | 0.4575 | 0.4915 |
| stack_participant_C0.1 | medio | 0.0992 | 0.1014 |

## Combinaciones elegidas

| fold | scope | candidate | inner_score |
|---|---|---|---|
| 1 | pool_selected | both_h0.0_mean_s4 | 0.3504 |
| 1 | pool_logistic | logistic_h0.0_geometric_s1 | 0.3497 |
| 1 | pool_lda | lda_h0.75_geometric_s1 | 0.3473 |
| 1 | pool_fixed_history | both_h1.0_mean_s1 | nan |
| 1 | pool_fixed_multiscale | both_h0.5_mean_s1 | nan |
| 2 | pool_selected | logistic_h0.75_geometric_s4 | 0.3719 |
| 2 | pool_logistic | logistic_h0.75_geometric_s4 | 0.3719 |
| 2 | pool_lda | lda_h0.5_geometric_s4 | 0.3562 |
| 2 | pool_fixed_history | both_h1.0_mean_s1 | nan |
| 2 | pool_fixed_multiscale | both_h0.5_mean_s1 | nan |
| 3 | pool_selected | logistic_h0.25_geometric_s4 | 0.3493 |
| 3 | pool_logistic | logistic_h0.25_geometric_s4 | 0.3493 |
| 3 | pool_lda | lda_h0.25_mean_s4 | 0.3414 |
| 3 | pool_fixed_history | both_h1.0_mean_s1 | nan |
| 3 | pool_fixed_multiscale | both_h0.5_mean_s1 | nan |
| 4 | pool_selected | lda_h0.0_mean_s4 | 0.3397 |
| 4 | pool_logistic | logistic_h1.0_mean_s1 | 0.3391 |
| 4 | pool_lda | lda_h0.0_mean_s4 | 0.3397 |
| 4 | pool_fixed_history | both_h1.0_mean_s1 | nan |
| 4 | pool_fixed_multiscale | both_h0.5_mean_s1 | nan |
| 5 | pool_selected | logistic_h0.0_mean_s1 | 0.3409 |
| 5 | pool_logistic | logistic_h0.0_mean_s1 | 0.3409 |
| 5 | pool_lda | lda_h0.0_mean_s1 | 0.3391 |
| 5 | pool_fixed_history | both_h1.0_mean_s1 | nan |
| 5 | pool_fixed_multiscale | both_h0.5_mean_s1 | nan |

## Registro y verificación

Se reutilizan las predicciones internas verificadas de la ronda de hiperparámetros;
no se repiten sus 660 ajustes. Se recalculan 900 puntuaciones de combinaciones y se
congelan 55 elecciones o definiciones antes de evaluar externamente: 15 seleccionadas,
10 controles fijos y 30 definiciones de stacking.

Reajuste externo: 140 modelos base, que contienen 420 clasificadores por modalidad,
y 60 combinadores. Se conservan 110 bundles completos que incluyen sus modelos base,
297,528 predicciones, cinco matrices meta-OOF y 7.560 coeficientes.

Auditoría: se recargaron todos los bundles; se verificaron los 140 modelos base únicos
y sus 420 preprocesadores. Las copias compartidas se contrastaron mediante hash de
objetos antes de reutilizar su predicción verificada. Se reajustaron los 60 combinadores
desde sus matrices OOF y se exigió igualdad exacta de escalado, coeficientes e interceptos.
Se reprodujeron las predicciones y se recalcularon 110 métricas de fold y 550 de persona.
Las 47 pruebas están en pruebas.txt. Catálogos, hashes y bitácora acompañan los resultados.

## Límites

Esta ronda es adaptativa: se diseñó después de observar las rondas anteriores sobre
las mismas personas de train. La selección interna y el stacking OOF evitan fugas dentro
del ajuste, pero no convierten esta exploración repetida en confirmación independiente.
Los intervalos usan 2.000 remuestreos pareados de personas, promediando semillas primero,
sin corrección por múltiples contrastes ni dependencia entre folds. Una subida puntual
no confirma superioridad estable ni demuestra que el historial explique la mejora.
Al contar personas que mejoran se usa tolerancia 1e-12 para no contar redondeos como ganancias.

Validation y test originales no se evalúan de nuevo. Las features y pseudoetiquetas
siguen normalizadas offline por persona; el contexto causal puede cruzar estímulos
dentro de una grabación, con soporte máximo de 12 s contando el suavizado. No se entrena
atención ni regresión, ni se ajusta un modelo final nuevo sobre las 25 personas.

## Reproducción

```powershell
python -m pip install -r requirements_avanzados.txt
python -m unittest discover -s tests -v
python scripts/entrenar_ensambles.py --output resultados/NUEVO_ENSAMBLE
python scripts/informe_ensambles.py --output resultados/NUEVO_ENSAMBLE
```

Se requiere la ronda de hiperparámetros conservada en el repositorio. Para cargar,
agregar scripts al path, usar joblib.load y ensambles_core.predict(bundle, frame).
El frame contiene las features y persona/grabación/timestamp, ordenados por esos campos;
no necesita etiquetas. La salida sigue el orden bajo, medio, alto.
