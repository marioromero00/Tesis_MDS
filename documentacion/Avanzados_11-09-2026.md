# Boosting, ordinalidad y balanceo por participante: 11-09-2026

El contraste principal obtiene 0.3522 de BA macro,
frente a 0,3651 de la fusión geométrica anterior. Diferencia -1.29 puntos
porcentuales, intervalo descriptivo [-3.43; +0.96],
mejora en 10/25 personas. Interpretar junto con las limitaciones
de investigación repetida sobre train; no es validación independiente.

## Qué se cambió

- CatBoost multiclase: 300 iteraciones fijas, profundidad 4, learning rate 0,03, L2=20,
  bootstrap Bernoulli, subsample=0,8, rsm=0,8, cuatro hilos, sin early stopping ni eval_set.
- Logística nominal C=0,1 como control.
- Modelo ordinal: dos logísticas C=0,1 para P(y≥medio) y P(y≥alto). Si la segunda excede
  la primera, ambas se proyectan a su promedio; se reconstruyen tres probabilidades válidas.
- Dos ponderaciones de entrenamiento: inversa de frecuencia global de clase, o inversa
  del número de filas de la clase dentro de cada persona y del número de clases presentes
  en esa persona. Se normaliza peso medio a uno. La segunda da igual masa a cada persona
  y a cada clase observada dentro de ella; su accuracy ponderada coincide con la BA macro.
  Los pesos se calculan exclusivamente en el subconjunto de ajuste.
- Dos paneles: pupila + mirada (15) y pupila + mirada + EEG (24); ventana actual o resumen
  causal de ocho ventanas. El resumen conserva actual/media/std/diferencia con la más antigua
  y longitud. El contexto de grabación puede cruzar estímulos, sin ventanas futuras.
- Suavizado causal de probabilidades de 1/4 ventanas. Ajustes de decisión multiplicando
  por exp([bajo,0,alto]) con cada sesgo en -0,3/0/0,3 y renormalizando. Esto cambia la regla
  de predicción, no las etiquetas reales. Las salidas ajustadas no implican calibración.

Las etiquetas de activación GSR de 6 s y el split se mantienen. GSR no entra como predictor.
No se reentrena atención ni regresión. La normalización de features y pseudoetiquetas sigue
siendo offline por persona. El máximo soporte combinado de features/suavizado es de 12 s.

La configuración de CatBoost y el uso de pesos están basados en su
[API oficial](https://catboost.ai/docs/en/concepts/python-reference_catboostclassifier).
La ejecución fija CatBoost 1.2.10 en `requirements_avanzados.txt`.

## Resultados de las reglas de selección

`all`: selecciona entre las 432 configuraciones. `unadjusted`: entre 24 modelos sin
suavizado ni sesgos. `participant`: entre 216 con balanceo por persona. `ordinal` y
`catboost`: entre 144 de cada familia. Todas son reglas predefinidas; no se escoge una
por su resultado externo. `global` es un comparador secundario entre las 216 configuraciones
con balanceo global, declarado antes de cualquier resultado externo. Reutiliza las mismas
puntuaciones internas y añade diez modelos. Comparar sus selecciones con `participant`
contrasta reglas completas; no aísla causalmente el efecto del peso si cambian otras opciones.
BA macro y BA global promedian métricas de dos semillas.

| scope | macro_score | balanced_accuracy | macro_f1 |
|---|---|---|---|
| all | 0.3522 | 0.3385 | 0.3128 |
| catboost | 0.3555 | 0.3417 | 0.3086 |
| global | 0.3479 | 0.3490 | 0.3315 |
| ordinal | 0.3582 | 0.3526 | 0.3154 |
| participant | 0.3522 | 0.3385 | 0.3128 |
| unadjusted | 0.3457 | 0.3393 | 0.3388 |

| scope | reference | mean_delta | ci_low | ci_high | positive_participants |
|---|---|---|---|---|---|
| all | previous_late_geometric | -0.0129 | -0.0343 | 0.0096 | 10 |
| all | previous_fixed_logistic | -0.0064 | -0.0238 | 0.0132 | 11 |
| all | unadjusted | 0.0065 | -0.0116 | 0.0269 | 12 |
| all | global | 0.0043 | -0.0131 | 0.0210 | 15 |
| unadjusted | previous_late_geometric | -0.0194 | -0.0359 | -0.0038 | 11 |
| unadjusted | previous_fixed_logistic | -0.0129 | -0.0273 | -0.0003 | 11 |
| unadjusted | global | -0.0022 | -0.0209 | 0.0162 | 13 |
| participant | previous_late_geometric | -0.0129 | -0.0343 | 0.0096 | 10 |
| participant | previous_fixed_logistic | -0.0064 | -0.0238 | 0.0132 | 11 |
| participant | unadjusted | 0.0065 | -0.0116 | 0.0269 | 12 |
| participant | global | 0.0043 | -0.0131 | 0.0210 | 15 |
| ordinal | previous_late_geometric | -0.0069 | -0.0256 | 0.0127 | 11 |
| ordinal | previous_fixed_logistic | -0.0003 | -0.0143 | 0.0142 | 11 |
| ordinal | unadjusted | 0.0125 | -0.0065 | 0.0319 | 15 |
| ordinal | global | 0.0103 | -0.0023 | 0.0238 | 16 |
| catboost | previous_late_geometric | -0.0096 | -0.0350 | 0.0161 | 11 |
| catboost | previous_fixed_logistic | -0.0031 | -0.0218 | 0.0180 | 14 |
| catboost | unadjusted | 0.0098 | -0.0099 | 0.0308 | 15 |
| catboost | global | 0.0076 | -0.0141 | 0.0335 | 15 |
| global | previous_late_geometric | -0.0172 | -0.0387 | 0.0033 | 10 |
| global | previous_fixed_logistic | -0.0107 | -0.0256 | 0.0040 | 10 |
| global | unadjusted | 0.0022 | -0.0162 | 0.0209 | 12 |

## Distribución y acierto por clase

Fracción predicha y recall de cada clase, promediados entre semillas. El recall por persona
promedia solo personas que presentan esa clase. Una mejora de BA no garantiza que mejoren
los tres niveles; esta tabla permite identificar el coste de la regla de decisión.

| scope | label | predicted_fraction | global_recall | participant_recall |
|---|---|---|---|---|
| all | alto | 0.3610 | 0.3595 | 0.3669 |
| all | bajo | 0.5426 | 0.5633 | 0.5682 |
| all | medio | 0.0964 | 0.0928 | 0.0964 |
| catboost | alto | 0.2721 | 0.2714 | 0.2771 |
| catboost | bajo | 0.6471 | 0.6580 | 0.6681 |
| catboost | medio | 0.0808 | 0.0958 | 0.0899 |
| global | alto | 0.2229 | 0.2320 | 0.2276 |
| global | bajo | 0.5867 | 0.6220 | 0.6084 |
| global | medio | 0.1904 | 0.1930 | 0.1955 |
| ordinal | alto | 0.1379 | 0.1458 | 0.1412 |
| ordinal | bajo | 0.6900 | 0.7328 | 0.7365 |
| ordinal | medio | 0.1721 | 0.1792 | 0.1822 |
| participant | alto | 0.3610 | 0.3595 | 0.3669 |
| participant | bajo | 0.5426 | 0.5633 | 0.5682 |
| participant | medio | 0.0964 | 0.0928 | 0.0964 |
| unadjusted | alto | 0.3417 | 0.3394 | 0.3479 |
| unadjusted | bajo | 0.3910 | 0.4014 | 0.4036 |
| unadjusted | medio | 0.2673 | 0.2770 | 0.2778 |

## Selecciones por fold

| fold | scope | panel | context | family | weighting | smoothing | low_bias | high_bias | inner_score |
|---|---|---|---|---|---|---|---|---|---|
| 1 | all | full | 1 | catboost | participant | 4 | 0.3000 | 0.3000 | 0.3778 |
| 1 | unadjusted | full | 1 | catboost | participant | 1 | 0.0000 | 0.0000 | 0.3640 |
| 1 | participant | full | 1 | catboost | participant | 4 | 0.3000 | 0.3000 | 0.3778 |
| 1 | ordinal | full | 1 | ordinal | participant | 4 | 0.3000 | 0.3000 | 0.3688 |
| 1 | catboost | full | 1 | catboost | participant | 4 | 0.3000 | 0.3000 | 0.3778 |
| 2 | all | full | 8 | logistic | participant | 4 | 0.3000 | 0.3000 | 0.3883 |
| 2 | unadjusted | full | 8 | ordinal | participant | 1 | 0.0000 | 0.0000 | 0.3714 |
| 2 | participant | full | 8 | logistic | participant | 4 | 0.3000 | 0.3000 | 0.3883 |
| 2 | ordinal | full | 8 | ordinal | participant | 4 | 0.3000 | 0.0000 | 0.3864 |
| 2 | catboost | full | 8 | catboost | global | 1 | 0.3000 | -0.3000 | 0.3676 |
| 3 | all | full | 1 | ordinal | participant | 4 | 0.0000 | -0.3000 | 0.3548 |
| 3 | unadjusted | full | 8 | ordinal | global | 1 | 0.0000 | 0.0000 | 0.3502 |
| 3 | participant | full | 1 | ordinal | participant | 4 | 0.0000 | -0.3000 | 0.3548 |
| 3 | ordinal | full | 1 | ordinal | participant | 4 | 0.0000 | -0.3000 | 0.3548 |
| 3 | catboost | full | 1 | catboost | global | 4 | 0.3000 | -0.3000 | 0.3461 |
| 4 | all | full | 1 | catboost | participant | 4 | 0.3000 | 0.3000 | 0.3626 |
| 4 | unadjusted | full | 8 | logistic | global | 1 | 0.0000 | 0.0000 | 0.3476 |
| 4 | participant | full | 1 | catboost | participant | 4 | 0.3000 | 0.3000 | 0.3626 |
| 4 | ordinal | full | 1 | ordinal | global | 4 | 0.3000 | -0.3000 | 0.3531 |
| 4 | catboost | full | 1 | catboost | participant | 4 | 0.3000 | 0.3000 | 0.3626 |
| 5 | all | full | 1 | catboost | participant | 4 | 0.3000 | 0.3000 | 0.3613 |
| 5 | unadjusted | full | 1 | catboost | global | 1 | 0.0000 | 0.0000 | 0.3443 |
| 5 | participant | full | 1 | catboost | participant | 4 | 0.3000 | 0.3000 | 0.3613 |
| 5 | ordinal | full | 8 | ordinal | global | 4 | 0.3000 | -0.3000 | 0.3538 |
| 5 | catboost | full | 1 | catboost | participant | 4 | 0.3000 | 0.3000 | 0.3613 |
| 1 | global | full | 8 | catboost | global | 1 | 0.3000 | 0.0000 | 0.3706 |
| 2 | global | full | 8 | ordinal | global | 4 | 0.3000 | 0.3000 | 0.3841 |
| 3 | global | full | 1 | logistic | global | 4 | 0.0000 | -0.3000 | 0.3532 |
| 4 | global | full | 1 | catboost | global | 4 | 0.3000 | 0.3000 | 0.3622 |
| 5 | global | full | 8 | catboost | global | 4 | 0.3000 | -0.3000 | 0.3558 |

## Protocolo y registro

Se trabaja solo con las 25 personas originales de train. Cinco folds externos de 20/5;
tres folds internos dentro de los 20. Se promedian sus BA macro dando igual peso a cada
fold interno, con desempate por identificador. Se congelan todas las elecciones antes
de evaluar externamente. Dos semillas de reajuste: 20260911/20260912; logística es
determinista en este ajuste, por lo que dos semillas no aportan dos réplicas independientes.
Imputación, indicadores de ausencia y escalado se ajustan por separado en cada entrenamiento.

360 ajustes internos de modelos (480 clasificadores contando los dos ordinales),
6.480 puntuaciones de decisión, 30 selecciones y 60 bundles externos guardados
(50 principales y diez del control global cuando está presente).
`bitacora.jsonl` registra todos los ajustes; `todos_los_intentos.csv`, cada resultado.
Las probabilidades internas de los 24 modelos por fold se conservan en NPZ junto con
identificadores originales, y se verifican las 6.480 puntuaciones a partir de ellas.

Se recargaron los 60 modelos y se verificaron 162,288 predicciones OOF,
60 métricas de fold y 300 de participante. Se reconstruyeron los preprocesadores para
verificar ajuste solo en entrenamiento. `pruebas.txt` conserva las 42 pruebas aprobadas.
Los modelos internos no se guardan; sí sus predicciones, particiones y configuraciones.
Los modelos externos corresponden a 20 personas cada uno, sin ajuste final nuevo sobre 25.

## Alcance de la mejora

El objetivo es subir la BA de las etiquetas originales sin cambiar el problema para
obtener un número mayor. Los intervalos usan 2.000 remuestreos pareados de personas,
promediando semillas primero; son descriptivos, sin corrección por múltiples contrastes,
dependencia entre folds ni búsquedas repetidas. La selección anidada evita usar las personas
externas dentro del ajuste de cada ejecución, pero no elimina la adaptación entre rondas.
Validation y test originales no se vuelven a evaluar. La comparación con la fusión anterior
comparte personas externas, aunque cambia la partición interna y el método de selección.
No se puede atribuir una diferencia exclusivamente al modelo ni afirmar confirmación externa.

## Reproducción y carga

```powershell
python -m pip install -r requirements_avanzados.txt
python -m unittest discover -s tests
python scripts/entrenar_avanzados.py --output resultados/NUEVO_AVANZADO
python scripts/informe_avanzados.py --output resultados/NUEVO_AVANZADO
```

El comparador secundario de esta entrega se ejecutó con `python scripts/control_balanceo_global.py`
sobre el directorio original, después del entrenamiento principal y antes del informe.
Su declaración fechada, protocolo y resultados se conservan en `control_global_plan.json`
y `control_global/`; no vuelve a buscar configuraciones ni usa resultados externos para elegir.

Para cargar: añadir `scripts` al path, `joblib.load` de un bundle del catálogo y llamar
`avanzados_core.predict(bundle, frame)`. El frame contiene las features originales y
persona/grabación/timestamp, ordenado por esos tres campos; no requiere etiquetas.
Los parámetros de panel, contexto, ponderación y decisión están dentro del bundle.
