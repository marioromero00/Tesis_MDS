# Avance — 11-09-2026: Auditoria y Ensambles

Fuente: ejecuciones de la noche del 11-09-2026 en Chile, con manifiestos UTC del
12-09-2026. Complementa [[Avance - 11-09-2026 (SVM QDA e Hiperparametros)]].

## Qué detectó la auditoría

Los modelos anteriores reproducen sus predicciones, pero la selección de hiperparámetros
es poco estable entre particiones internas. La correlación media de Spearman entre rankings
es 0,1757 para la grilla completa y −0,0376 para las fusiones. La diferencia media entre
las dos configuraciones mejor puntuadas es de apenas 0,17 y 0,16 puntos porcentuales.
El ganador de la grilla completa coincide con el ganador interno en 3/15 comparaciones,
contando empates; en fusiones, en 5/15. Esto motivó probar promedios de configuraciones.

Las diferencias interna-externa también reflejan personas distintas: no se interpretan
como una estimación aislada del sesgo de sobreajuste. Se revisaron además tres reglas
constantes: bajo y alto obtienen BA macro 0,3467; medio, 0,3067. La métrica promedia las
clases observadas de cada persona y dos personas no presentan las tres clases. La BA
global de las tres reglas constantes sigue siendo 1/3.

Al contar mejoras por persona, diferencias absolutas de hasta 1e-12 se tratan como
empates; así no se cuentan redondeos como ganancias. Los resultados numéricos no cambian.

## Nuevos enfoques

Se reutilizaron las predicciones internas auditadas de 14 modelos: fusiones logísticas
con cuatro valores de C y fusiones LDA con tres valores de shrinkage, cada una con
ventana actual o historial de ocho ventanas. Cada modelo base combina pupila, mirada
y EEG; se mantienen etiquetas, clases, split y exclusión de GSR como predictor.

- 60 combinaciones de promedio aritmético/geométrico, familia, proporción entre ventana
  actual e historial y suavizado causal. Se eligen internamente tres reglas: todas las
  familias, solo logística o solo LDA.
- Dos controles fijos: promedio de los siete modelos con historial y promedio de los
  catorce modelos entre ambas escalas, sin suavizado adicional.
- Seis modelos de stacking: logística sobre 42 probabilidades, con C=0,001/0,01/0,1 y
  balanceo global o por persona. Sus hiperparámetros se fijaron antes de evaluar externamente.

El stacking se ajusta con predicciones OOF por participante: cada fila fue predicha por
modelos base entrenados sin esa persona. El combinador usa las 20 personas de ajuste;
después, los modelos base se reajustan sobre esas 20 para predecir las cinco externas.
Se conserva cada matriz OOF y se verifica su linaje. Los coeficientes del combinador
describen asociaciones con salidas correlacionadas de modelos, no importancia de sensores.

## Resultados y límite de la mejora

| Regla | BA macro |
|---|---:|
| Fusión geométrica anterior | 0,3651 |
| Selección interna de promedios, contraste principal | 0,3595 |
| Promedio fijo de modelos con historial | 0,3663 |
| Stacking global, C=0,01 | 0,3650 |
| Stacking por persona, C=0,001 | 0,3671 |
| Stacking por persona, C=0,01 | 0,3685 |

El máximo observado sube 0,34 puntos porcentuales respecto de la referencia anterior,
intervalo descriptivo [-3,11; +4,10], con mejora en 11/25 personas. Es un contraste
secundario con incertidumbre amplia. El contraste principal pierde 0,56 puntos,
intervalo [-1,89; +0,83]. No se confirma superioridad estable.

El diagnóstico por clase limita la utilidad del máximo de 0,3685:

| Modelo | Recall bajo | Recall medio | Recall alto | Macro-F1 |
|---|---:|---:|---:|---:|
| Promedio fijo con historial | 0,3962 | 0,3713 | 0,3310 | 0,3658 |
| Stacking por persona, C=0,01 | 0,5222 | 0,0641 | 0,4814 | 0,3201 |

El stacking predice medio en solo 6,1 % de las ventanas. Su mayor BA macro oculta una
pérdida importante en esa clase y variaciones amplias entre personas. El promedio fijo
con historial gana solo 0,12 puntos de BA macro, intervalo [-0,51; +0,80], pero conserva
un reconocimiento más equilibrado. Estos resultados motivaron otra prueba de mezclas.

## Auditoría y registro

900 puntuaciones de combinaciones y 55 elecciones/definiciones congeladas antes de la
evaluación externa. 140 reajustes base (420 clasificadores por modalidad) y 60 combinadores.
Se guardaron 110 bundles completos, 297.528 predicciones, cinco matrices OOF y 7.560 coeficientes.
No se repitió la búsqueda interna de 660 ajustes de la ronda anterior.

Se recargaron los 110 bundles y se verificaron los 140 modelos base únicos, sus 420
preprocesadores y las copias compartidas. Los 60 combinadores se reajustaron desde
sus matrices OOF: escalado, coeficientes e interceptos coincidieron exactamente.
Se recalcularon 110 métricas de fold y 550 por persona. Las 47 pruebas pasaron.

Código: `scripts/ensambles_core.py`, `entrenar_ensambles.py` e `informe_ensambles.py`.
Resultados: `resultados/ensambles_11-09-2026/`. Informe: `documentacion/Ensambles_11-09-2026.md`.
El diseño OOF sigue el principio descrito en la
[documentación oficial de stacking](https://scikit-learn.org/stable/auto_examples/ensemble/plot_stack_predictors.html),
con particiones explícitas por persona.

## Mezclas posteriores y resultados

Se declararon mezclas fijas con 5 %, 10 % y 25 % de stacking, usando como resto el
promedio con historial. El 10 % es el contraste principal de esa prueba. El plan se
guardó antes de calcular las mezclas, después de observar el problema de recall medio;
por tanto, es otra exploración adaptativa.

| Peso del stacking | BA macro | Ganancia frente a 0,3651 (pp) | IC descriptivo 95 % (pp) | Recall medio |
|---|---:|---:|---:|---:|
| 5 %, secundario | 0,3684 | +0,335 | [-0,321; +1,092] | 0,3575 |
| 10 %, principal | 0,3687 | +0,358 | [-0,299; +1,143] | 0,3433 |
| 25 %, secundario | 0,3716 | +0,652 | [-0,312; +1,707] | 0,2881 |

La mezcla con 25 % mejora en 15/25 personas y alcanza BA global 0,3691 y macro-F1
0,3681. Recupera reconocimiento de medio frente al stacking solo (0,0641), aunque pierde
frente al promedio con historial (0,3713). Sus recalls bajo/alto son 0,4534/0,3657.
El contraste principal de 10 % mejora en 12/25 personas, con un empate. Ningún intervalo
excluye cero. El máximo secundario no constituye una selección confirmada fuera de muestra.

Se guardaron y recargaron 30 modelos de mezcla completos, verificando 81.144 predicciones
y los 20 modelos fuente. Sumadas ambas rondas: 140 archivos de modelos y 378.672
predicciones verificadas. Las dos semillas producen resultados iguales en las mezclas;
no se cuentan como observaciones independientes. El bootstrap promedia semillas antes
de remuestrear personas. Código: `scripts/mezclas_ensambles.py`; resultados:
`resultados/mezclas_ensambles_11-09-2026/`; informe:
`documentacion/Mezclas_Ensambles_11-09-2026.md`.

Validation y test originales no se volvieron a evaluar. Continúan las limitaciones de
pseudoetiquetas y normalización offline por persona. Los intervalos no corrigen búsquedas
repetidas ni dependencia entre folds; una mejora puntual no demuestra superioridad temporal.

Ver [[Tesis_MDS]], [[Avance - 10-09-2026 (Nuevos Modelos y Fusiones)]] y
[[Resumen Diseño Etiquetas y Modelos]].

## Publicación

Código, modelos, resultados e informes publicados en GitHub `main`, commit `584b073`.
La comprobación final recalculó las 30 métricas de fold y 150 por persona de las mezclas
desde el CSV guardado y verificó 140 hashes de modelos. El inventario de entrega contiene
185 archivos; sus hashes coinciden con los bytes preparados para Git.
Respaldo de esta sección: `documentacion/Tesis_Vault_Ensambles_11-09-2026.zip`, con
inventario `documentacion/inventario_vault_ensambles_11-09-2026.json`.
