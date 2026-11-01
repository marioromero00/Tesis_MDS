# Avance — 11-09-2026: SVM, QDA e Hiperparametros

Fuente: código y ejecución local del 11-09-2026, hora de Chile; parte de los manifiestos
usa UTC del 12-09-2026. Complementa [[Avance - 11-09-2026 (Boosting Ordinalidad y Balanceo)]].

## Grilla congelada

| Familia | Hiperparámetros |
|---|---|
| SVM con kernel RBF exacto | C=0,1/1/10 y gamma=0,1/d o 1/d, con d igual a la dimensión transformada |
| Histogram Gradient Boosting | 7/15/31 hojas; perfil regular: tasa 0,03, 150 iteraciones, hoja mínima 100 y L2=20; perfil flexible: tasa 0,1, 200 iteraciones, hoja mínima 30 y L2=1 |
| QDA | Regularización de covarianza 0,1/0,5/0,9 y priors iguales |
| Fusión de logísticas | C=0,001/0,01/0,1/1; media geométrica de tres modalidades |
| Fusión de LDA | Shrinkage=0,1/0,5/0,9; media geométrica de tres modalidades |

Cada modelo compara ventana actual con contexto causal de ocho ventanas. Son 44
configuraciones base; suavizar las salidas en una o cuatro ventanas produce 88 decisiones.
Boosting usa dos perfiles predefinidos, no todas las combinaciones posibles de sus parámetros.

Los modelos conjuntos reciben pupila, mirada y EEG: 24 variables actuales. Las fusiones
ajustan un clasificador y un preprocesador por modalidad. GSR queda fuera de los inputs;
las etiquetas de activación GSR de 6 s, las tres clases y el split original se mantienen.

## Evaluación

Cinco folds externos de 20/5 personas dentro de las 25 de train; tres internos por fold.
Se promedia la BA macro por participante de los folds internos, con igual peso por fold
y desempate por identificador. Todas las elecciones se congelan antes de evaluar externamente.
La búsqueda conjunta es el contraste principal; cada familia y la selección entre fusiones
son contrastes secundarios predefinidos. Validation y test originales no se vuelven a evaluar.

SVM, boosting y logística usan balanceo global de clases; LDA/QDA, priors uniformes.
El balanceo por persona no se busca en esta ronda. Imputación, escalado y estimadores
se ajustan únicamente con las personas de entrenamiento de cada fold. No hay early stopping.

SVM usa softmax de sus scores de decisión OVR para permitir suavizado. Son scores
normalizados, no probabilidades calibradas; se evita su calibración interna con folds
aleatorios de ventanas. Las otras familias usan las probabilidades de sus clasificadores.

## Ejecución y archivos

El primer intento serial completó 57 ajustes antes de detenerse para acelerar la búsqueda.
Se conserva en `resultados/hiperparametros_11-09-2026/`, sin evaluaciones externas.
Guarda las 88 puntuaciones de la primera partición; los 13 ajustes completos posteriores
figuran en la bitácora, pero sus salidas no llegaron al checkpoint por partición.
La ejecución completa repite la misma grilla en cuatro procesos con un hilo numérico
por proceso, en `resultados/hiperparametros_11-09-2026_paralelo/`.

Cuando varias reglas seleccionan el mismo modelo, personas y semilla, comparten el ajuste.
Cada regla conserva su propio bundle con el suavizado elegido. El registro paralelo guarda
tiempos reales y componentes de cada ajuste; la bitácora principal registra su recepción.

Las 45 pruebas pasaron, incluidas recarga de las cinco familias, aislamiento entre personas,
causalidad de features y equivalencia entre argmax de scores y predicción SVM sin suavizado.
Código en `scripts/hiperparametros_core.py`, `entrenar_hiperparametros.py`,
`ejecutar_hiperparametros_paralelo.py` e `informe_hiperparametros.py`.
Dependencias fijadas en `requirements_avanzados.txt` y sus archivos incluidos.

## Resultados

La búsqueda y el entrenamiento terminaron. Ninguna regla supera la referencia anterior
de BA macro 0,3651. Las puntuaciones promedian la BA por participante entre dos semillas.

| Regla de selección | BA macro |
|---|---:|
| Fusión geométrica anterior | 0,3651 |
| Fusión logística ajustada | 0,3605 |
| Fusión LDA ajustada | 0,3593 |
| Selección entre ambas fusiones | 0,3575 |
| Búsqueda conjunta | 0,3548 |
| QDA ajustado | 0,3544 |
| Boosting HGB ajustado | 0,3510 |
| SVM RBF ajustada | 0,3501 |

La búsqueda conjunta pierde 1,03 puntos porcentuales frente a la referencia, intervalo
descriptivo [-2,95; +0,63], con mejora en 11/25 personas. La fusión logística pierde
0,45 puntos, intervalo [-1,90; +0,90], con mejora en 12/25. Los intervalos incluyen cero.
La fusión logística tiene el mayor promedio de esta ronda, como contraste secundario;
no se transforma retrospectivamente en el contraste principal.

Sus hiperparámetros elegidos por fold fueron:

| Fold | C | Contexto en ventanas | Suavizado en ventanas |
|---|---:|---:|---:|
| 1 | 1 | 1 | 1 |
| 2 | 0,1 | 8 | 4 |
| 3 | 0,01 | 1 | 4 |
| 4 | 0,001 | 8 | 1 |
| 5 | 0,1 | 1 | 1 |

No aparece una regularización ni un contexto único que resulte elegido en todos los folds.
La búsqueda conjunta elige HGB en tres folds, logística en uno y LDA en uno.
La fusión logística obtiene recall global de 0,4018 en bajo, 0,3834 en medio y 0,2930 en alto;
el reconocimiento es más equilibrado que en el ordinal de la ronda anterior, pero su BA
macro no supera la mejor fusión previa. Esto no confirma una ventaja temporal.

Se completaron 660 ajustes internos que contienen 1.080 clasificadores y 1.320 puntuaciones.
Las 35 elecciones generan 70 bundles guardados, con 50 ajustes externos únicos y 90
clasificadores externos únicos. La reutilización entre reglas evita repetir ajustes idénticos.
Hay 189.336 predicciones externas guardadas y reproducidas después de recargar los 70 bundles.
Se verificaron 138 preprocesadores, 70 métricas de fold, 350 métricas por participante,
las 1.320 puntuaciones internas y las 35 selecciones. No hubo fallos en la auditoría.
El informe completo está en `documentacion/Hiperparametros_11-09-2026.md`; las figuras PNG/PDF,
el catálogo de modelos, los hiperparámetros elegidos y el registro de pruebas están junto
a los resultados. Los modelos externos se ajustan sobre 20 personas cada uno; no se
genera un estimador final nuevo sobre las 25.

## Alcance

Es una exploración sobre train reutilizado en varias rondas. La evaluación anidada protege
cada ajuste de sus personas externas, pero no elimina la adaptación entre rondas. Las
features y pseudoetiquetas siguen normalizadas offline por persona. No se deduce validación
independiente ni superioridad temporal de una puntuación interna o de un hiperparámetro elegido.

Referencias técnicas: APIs oficiales de
[SVC](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html),
[HGB](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingClassifier.html)
y [QDA](https://scikit-learn.org/stable/modules/generated/sklearn.discriminant_analysis.QuadraticDiscriminantAnalysis.html).

Ver [[Tesis_MDS]], [[Avance - 10-09-2026 (Nuevos Modelos y Fusiones)]] y
[[Resumen Diseño Etiquetas y Modelos]].

## Publicacion

Resultados publicados en GitHub `main`, commit `1ffb0ea`. Respaldo de las notas
en `documentacion/Tesis_Vault_Hiperparametros_11-09-2026.zip`, con inventario de hashes.
