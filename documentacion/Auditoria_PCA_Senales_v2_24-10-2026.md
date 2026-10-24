# Auditoría y reconstrucción v2 del pipeline PCA por señal

## Hallazgos de la auditoría de v1

1. La normalización de las características del profesor y de sus scores usaba toda la sesión de cada participante, incluidas ventanas marcadas como no elegibles. Esas ventanas podían cambiar el peso relativo de mirada, pupila y GSR en una etiqueta elegible.
2. El PC1 del profesor GSR usaba cuatro variables y cargaba principalmente en `gsr_scr_count` (0,656) y `gsr_scr_mean_prominence_z` (0,655). En train, aproximadamente 97,1 % de las ventanas tenía ambos valores en cero. La componente estaba dominada por un evento escaso y duplicado en dos columnas.
3. El promedio causal de activación cruzaba 28 huecos entre ventanas elegibles dentro de un mismo segmento. Su soporte real podía exceder los 6 s declarados.
4. Los modelos y PCA del estudiante se ajustaban correctamente en train, pero estos problemas del profesor impedían interpretar limpiamente sus etiquetas. El control de solo estímulo era superior a todos los modelos con señales.

## Correcciones aplicadas en v2

- La normalización por participante del profesor utiliza solo ventanas multimodales elegibles. Las no elegibles quedan sin score ni etiqueta nuevos.
- El PC1 de GSR usa únicamente sus componentes continuas tónica y fásica: dos entradas, una componente. Su varianza explicada en train es 52,1 %; las cargas son 0,707 y 0,707. Los recuentos SCR permanecen en las características originales para auditoría, pero no crean esta etiqueta.
- El contexto de cinco ventanas de 2 s, separadas por 1 s, se reinicia al encontrar un salto distinto de 1 s, además de cambios de grabación o segmento. Se registraron 28 reinicios por huecos.
- Se mantiene el split congelado de 25/8/8 personas, el ajuste del PCA y su orientación en train elegible y la separación entre señales del profesor y del estudiante.

La etiqueta v2 de atención cambia en 154 de las 21.719 ventanas primarias elegibles respecto a v1 (0,7 %). La de activación cambia en 4.724 (21,8 %); sus métricas, por tanto, no son directamente comparables. Los scores v2 están presentes en todas las ventanas elegibles y las no elegibles no tienen clase nueva.

## Reducción del estudiante y resultado

El estudiante compara entradas completas, PCA por señal que retiene al menos 90 % de varianza de train y exactamente un PC por señal. Las mismas etiquetas v2 y ventanas se usan en cada comparación.

| Objetivo | Entradas completas | PCA ≥90 % | Un PC/señal | BA test completo | BA test ≥90 % | BA test 1 PC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Atención | 18 | 9 | 2 | 0,3893 | 0,3871 | 0,3834 |
| Activación | 25 | 15 | 3 | 0,3637 | 0,3635 | 0,3757 |

En validation, el modelo de un PC por señal obtiene 0,3424 para atención y 0,3431 para activación, bastante menos que PCA ≥90 % (0,3530 y 0,3877). La aparente ventaja de un PC en test de activación no se repite en validation. El PCA ≥90 % es la reducción más estable de las dos probadas: en test pierde 0,0022 BA para atención y 0,0002 para activación frente a entradas completas. Los intervalos descriptivos pareados por participante del cambio PCA ≥90 % menos completo son [−0,0079; +0,0027] y [−0,0176; +0,0172]; ambos incluyen cero.

El control que recibe **solo el nombre del estímulo** obtiene BA 0,4610 en atención y 0,4167 en activación en test, por encima de los modelos con señales. Esta v2 corrige el pipeline y conserva capacidad predictiva al reducir entradas; **no valida** que las pseudoetiquetas midan atención o activación más allá del efecto del estímulo. La normalización y los cuantiles siguen siendo offline por participante, y el test ya fue inspeccionado en trabajos anteriores.

## Verificación y reproducción

El dataset v2 coincide en identidad de ventanas con v1, conserva 13.062/4.640/4.017 ventanas elegibles en train/validation/test y no arrastra etiquetas históricas. Coinciden los hashes de dataset en los manifiestos de profesor y estudiante; se verificó la recarga de los ocho modelos del estudiante. Las pruebas comprueban normalización elegible, alineación por participante, ajuste del PCA solo en train y reinicio de contexto ante huecos.

```powershell
python scripts/generar_pseudoetiquetas_pca_senales.py --config config/pca_senales_v2.json
python scripts/predecir_pseudoetiquetas_pca_senales.py --config config/pca_senales_v2.json
python scripts/control_estimulo_pca_senales.py --config config/pca_senales_v2.json
python scripts/resumir_pca_senales.py --config config/pca_senales_v2.json
python -m unittest tests.test_pca_senales tests.test_preprocesamiento -v
```

Configuración: `config/pca_senales_v2.json`. Productos: `resultados/pca_senales_v2_24-10-2026/`, incluidos dataset, PCA guardados, predicciones, métricas, diferencias pareadas y manifiestos con hashes.

La [presentación final PCA](../presentaciones/Presentacion-Final-Tesis-PCA-24-10-2026.pptx) agrega tres láminas con la auditoría, el nuevo flujo PCA y las métricas de test. `scripts/verificar_presentacion_final_pca_24_10_2026.py` contrasta las cifras de la lámina final con los CSV y verifica el archivo PowerPoint.
