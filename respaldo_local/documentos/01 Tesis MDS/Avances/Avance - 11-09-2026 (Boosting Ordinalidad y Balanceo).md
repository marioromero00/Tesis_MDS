# Avance — 11-09-2026: Boosting, Ordinalidad y Balanceo

Fuente: ejecución local del 11-09-2026, código y artefactos en
`Tesis_MDS/resultados/avanzados_11-09-2026/`. Complementa
[[Avance - 10-09-2026 (Nuevos Modelos y Fusiones)]]. Es la fuente vigente de esta ronda;
la mejor referencia observada de activación sigue siendo la fusión geométrica anterior.

## Resultado

La nueva búsqueda no superó la BA macro por participante de 0,3651.
Se mantienen las etiquetas originales de activación GSR de 6 s, las tres clases y
la partición por participante. Ninguna señal GSR se usa como entrada del estudiante.

| Regla de selección interna | BA macro |
|---|---:|
| Referencia anterior: fusión geométrica | 0,3651 |
| Familia ordinal | 0,3582 |
| Familia CatBoost | 0,3555 |
| Búsqueda conjunta de las tres familias | 0,3522 |
| Solo balanceo por participante | 0,3522 |
| Solo balanceo global de clases | 0,3479 |
| Sin suavizado ni ajustes de decisión | 0,3457 |

Son resultados de cinco folds externos dentro de las 25 personas originales de train,
promediados entre dos semillas. No son resultados nuevos del test original. Las reglas
eligen modelos dentro de cada fold; la tabla no justifica escoger retrospectivamente
una familia por su promedio externo.

La búsqueda conjunta pierde 1,29 puntos porcentuales frente a la referencia anterior,
intervalo descriptivo [-3,43; +0,96], con mejora en 10/25 personas. El ordinal pierde
0,69 puntos, intervalo [-2,56; +1,27], con mejora en 11/25. Los intervalos incluyen cero:
no hay una mejora numérica ni evidencia para afirmar una diferencia estable.

## Qué se probó

- CatBoost multiclase, 300 iteraciones, profundidad 4, tasa 0,03 y L2=20.
- Dos logísticas ordinales C=0,1 para los cortes bajo/medio y medio/alto, con proyección
  de sus probabilidades para conservar el orden; logística nominal C=0,1 como control.
- Balanceo global de clases frente a igual peso total por persona y por clase observada
  dentro de ella. Los pesos se calculan solo con el subconjunto de ajuste.
- Pupila + mirada (15 variables) y pupila + mirada + EEG (24), ventana actual o resumen
  causal de ocho ventanas dentro de la grabación. Sin uso de ventanas futuras.
- Suavizado causal de una o cuatro probabilidades y nueve ajustes de decisión sobre
  los niveles bajo/alto. Las etiquetas permanecen fijas. Estas salidas ajustadas no
  equivalen a probabilidades calibradas.

Se compararon 24 modelos base y 432 configuraciones de decisión. Tres folds internos
por cada uno de los cinco externos producen 360 ajustes de modelos y 6.480 puntuaciones.
Los ordinales contienen dos clasificadores: son 480 clasificadores internos en total.
Se congelaron las 25 elecciones principales antes de evaluar los folds externos.

El comparador secundario de balanceo global se declaró antes del primer resultado
externo. Reutiliza las puntuaciones internas y añade cinco elecciones y diez modelos.
Comparar ambas reglas de balanceo no aísla el efecto de los pesos: también pueden
cambiar la familia, el panel, el contexto o la regla de decisión seleccionados.

## Qué limita el resultado

El ordinal tiene recall global de 0,7328 en bajo, 0,1792 en medio y 0,1458 en alto.
Su promedio oculta un reconocimiento muy desigual de las clases. En la búsqueda
conjunta el recall de medio cae a 0,0928. Se guarda el diagnóstico por clase y semilla
en `diagnostico_clases.csv`, junto con BA global y macro-F1.

En esta ronda, aumentar la flexibilidad del modelo, aprovechar el orden de las clases
y alinear los pesos con la métrica no produce una mejora frente a la fusión anterior.
Esto no demuestra que sea imposible mejorar; sí evita atribuir superioridad a estos
métodos con la evidencia actual. La hipótesis temporal todavía no queda confirmada.

La exploración reutiliza train de rondas anteriores. Los intervalos por remuestreo
pareado de personas son descriptivos, sin corrección por búsquedas repetidas ni
dependencia entre folds. Las features y pseudoetiquetas siguen normalizadas offline
por persona. Validation y test originales no se vuelven a evaluar.

## Archivos y reproducción

Los 60 bundles externos incluyen preprocesamiento, modelos y reglas de decisión.
Cada uno se ajusta sobre 20 personas; no se genera un modelo final nuevo sobre las 25.
Se conservan probabilidades internas NPZ, 162.288 predicciones externas, catálogos,
hashes, selecciones y bitácora. Los estimadores internos no se guardan.

La primera auditoría se detuvo al reconstruir el escalado con una disposición distinta
del array en memoria: diferencia máxima 1,17e-11. Se reprodujo la disposición original
del entrenamiento, conservando la exigencia de igualdad exacta. Los modelos y resultados
no cambiaron. El incidente se conserva en `incidente_auditoria.json`.

Auditoría final aprobada: 60 modelos recargados, 162.288 predicciones reproducidas,
60 preprocesadores reconstruidos, 60 métricas de fold, 300 métricas de participante,
30 selecciones y 6.480 puntuaciones internas verificadas. Las 42 pruebas pasaron;
`pruebas.txt` y `verificacion.json` conservan la evidencia.

Código: `avanzados_core.py`, `entrenar_avanzados.py`, `control_balanceo_global.py` e
`informe_avanzados.py`, dentro de `scripts/`. Dependencias en `requirements_avanzados.txt`.
Informe completo: `documentacion/Avanzados_11-09-2026.md`.
La API utilizada para CatBoost está documentada por su
[fuente oficial](https://catboost.ai/docs/en/concepts/python-reference_catboostclassifier).

Ver también [[Tesis_MDS]], [[Resumen Diseño Etiquetas y Modelos]] y
[[Avance - 08-09-2026 (Iteraciones de Mejora)]].

## Publicacion

Código, modelos, predicciones, informe y auditoría publicados en GitHub `main`,
commit de resultados `82fef67`. El respaldo de esta sección se conserva en
`documentacion/Tesis_Vault_Avanzados_11-09-2026.zip`, con inventario de hashes.
