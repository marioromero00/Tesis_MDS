# Regresion ordinal: 12-09-2026

**Entrega completa tras reintento:** `resultados/regresion_ordinal_12-09-2026_completa/`.
El predictor canónico usa entradas C-contiguas; sus 25 recargas dieron diferencia de
scores cero. Ejecutar `scripts/continuar_regresion_ordinal.py --audit` para auditar esta
entrega. Para cargar: `continuar_regresion_ordinal.predict(bundle, frame)`. El directorio
sin `_completa` conserva el intento inicial interrumpido y sus 180 ajustes internos.
El manifiesto `continuacion.json` registra fuentes, umbrales congelados y corrección.

Se evalua la misma etiqueta arousal_label_6s. Para entrenar se codifica bajo=-1,
medio=0 y alto=1; no se introduce GSR ni el score del profesor como predictor.
Se prueban Ridge (alpha=100), Nystroem RBF con Ridge (alpha=1, 192 componentes,
gamma=0,1/dimensiones), HistGradientBoostingRegressor y ExtraTreesRegressor.
Tres representaciones: actual, multiescala y relativa. Parametros completos en codigo
y fuentes congeladas en protocolo.json. No se cambia la etiqueta ni se elimina medio.

12 modelos base, 18 reglas por modelo (suavizado 1/16, umbral bajo -0,3/-0,1/-0,03,
alto 0,03/0,1/0,3). 180 ajustes internos y 3.240 puntuaciones. Seleccion conjunta all
como contraste principal, familias como secundarios. Se congelaron 25 elecciones antes
de los 25 ajustes externos; una semilla. Particiones: mismos cinco folds de train,
tres internos por persona, sin reevaluar validation/test originales.

## Resultados

| scope | macro_score | rows | participants | balanced_accuracy | macro_f1 |
|---|---|---|---|---|---|
| all | 0.3642 | 13524 | 25 | 0.3542 | 0.3457 |
| hgb | 0.3532 | 13524 | 25 | 0.3474 | 0.3438 |
| rbf | 0.3551 | 13524 | 25 | 0.3464 | 0.3402 |
| ridge | 0.3642 | 13524 | 25 | 0.3542 | 0.3457 |
| trees | 0.3576 | 13524 | 25 | 0.3575 | 0.3558 |

Diferencias pareadas frente a la mezcla previa 0,3716:

| scope | mean_delta | ci_low | ci_high | improved | tied |
|---|---|---|---|---|---|
| all | -0.0075 | -0.0335 | 0.0195 | 10 | 0 |
| ridge | -0.0075 | -0.0335 | 0.0195 | 10 | 0 |
| rbf | -0.0165 | -0.0360 | 0.0039 | 7 | 0 |
| hgb | -0.0184 | -0.0429 | 0.0046 | 11 | 0 |
| trees | -0.0140 | -0.0395 | 0.0103 | 10 | 0 |

IC descriptivos: 2.000 remuestreos pareados por persona; no corrigen busqueda adaptativa
ni dependencia de folds. Esta comparacion tampoco es confirmacion independiente.

La auditoria verifica 3240 puntuaciones, 25 elecciones, 25 preprocesadores
reajustados, 25 modelos recargados, 67620 predicciones y metricas por fold
y persona. Scores y escalado con rtol=atol=1e-12; clases exactamente iguales.
La codificacion ordinal no garantiza distancias fisiologicas iguales entre clases.

Reproducción desde cero: `scripts/entrenar_regresion_ordinal.py` conserva el comportamiento
del intento original. Después, `scripts/continuar_regresion_ordinal.py` reutiliza los
ajustes internos y completa la evaluación con entradas canónicas. Usar una copia sin
directorios de salida existentes. Agregar scripts al path y cargar mediante joblib.load;
ordenar frame por participant/recording/window_start_utc. No requiere etiquetas al predecir.
