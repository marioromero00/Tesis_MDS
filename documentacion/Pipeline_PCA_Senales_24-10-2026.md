# Pipeline nuevo: pseudoetiquetas y predicción con PCA por señal

**Versión superada:** la auditoría posterior encontró que la normalización incluía ventanas no elegibles, que el PC de GSR estaba dominado por SCR escasos y que el contexto cruzaba huecos. La [versión v2 auditada](Auditoria_PCA_Senales_v2_24-10-2026.md) corrige esos puntos; las métricas de esta página se conservan como registro exploratorio.

## Motivo de la reconstrucción

Al reconstruir los componentes del profesor se detectó un error en `scripts/preparar_modelado.py`: `groupby.apply` ordenaba los participantes lexicográficamente y `reset_index` reasignaba componentes a otras filas. En las **21.719 ventanas primarias elegibles**, el componente pupilar histórico difería del valor correctamente alineado en **21.719**. Una recomputación de las clases originales con filas alineadas coincide solo en 33,2 % para atención y 32,5 % para activación. Por ello, las métricas anteriores no son una referencia válida para calcular la mejora de este pipeline. El código de generación histórica se corrigió y se añadió una prueba con P2/P10 para impedir esa regresión; los archivos históricos se conservan sin sobrescribir.

Este pipeline nuevo lee `caracteristicas_multimodales.csv` y únicamente el archivo de partición congelada. No importa columnas de scores o clases anteriores. Mantiene 25 personas en train, ocho en validation, ocho en test y P29 solo como sensibilidad. Las ventanas elegibles primarias son 13.062/4.640/4.017.

## 1. Profesor: una componente por señal

Se transforman y normalizan las características por participante. Cada PCA se ajusta con ventanas elegibles de train. Su signo se fija allí contra el promedio firmado de las mismas características. Los scores y cuantiles son offline por participante, como en el protocolo anterior. Mirada y pupila se promedian a igual peso para atención; GSR se suaviza con cinco ventanas de 2 s separadas por 1 s (soporte de 6 s) para activación.

| Señal del profesor | Variables originales | PC usados | Varianza explicada en train |
| --- | ---: | ---: | ---: |
| Mirada | 4 | 1 | 63,9 % |
| Pupila | 1 | 1 | 100 % |
| GSR | 4 | 1 | 52,4 % |

Un PC es la compresión mínima planteada, pero descarta 36,1 % de varianza de mirada y 47,6 % de GSR. Por ello las nuevas pseudoetiquetas son **experimentales**; la varianza retenida no demuestra validez psicológica. Todas las ventanas primarias elegibles tienen una de las tres clases y las no elegibles no reciben etiqueta nueva.

## 2. Estudiante: reducción por señal

Atención usa EEG + GSR; activación usa EEG + mirada + pupila. La señal que construye cada etiqueta no entra como predictor. Los imputadores, escaladores, PCA y regresiones logísticas se ajustan solo con train. Se comparan, sobre las **mismas etiquetas nuevas**, entradas completas, el mínimo de PC que conserva al menos 90 % de varianza por señal y exactamente un PC por señal. Dummy usa el prior de train.

| Tarea | Entradas completas | PCA ≥90 % | Un PC por señal |
| --- | ---: | ---: | ---: |
| Atención | 18 | 9 (EEG 4, GSR 5) | 2 |
| Activación | 25 | 15 (EEG 4, mirada 7, pupila 4) | 3 |

La varianza retenida real por señal con el criterio ≥90 % fue EEG 94,2 %, GSR 96,3 %, mirada 92,9 % y pupila 96,0 %. Los detalles y hashes de cada pipeline están en `manifiesto_estudiante.json`.

## 3. Predicción y compresión

Precisión balanceada, mismas ventanas elegibles y ocho participantes por split:

| Etiqueta nueva | Split | Dummy | Completo | PCA ≥90 % | Un PC/señal | Solo estímulo |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Atención | Validation | 0,3333 | 0,3538 | 0,3530 | 0,3424 | 0,4642 |
| Atención | Test | 0,3333 | 0,3864 | 0,3856 | 0,3831 | 0,4635 |
| Activación | Validation | 0,3333 | 0,3556 | 0,3533 | 0,3364 | 0,3679 |
| Activación | Test | 0,3333 | 0,3727 | 0,3669 | 0,3754 | 0,4088 |

El PCA ≥90 % reduce aproximadamente a la mitad las entradas con una pérdida de **0,0007 BA** en atención y **0,0057 BA** en activación frente al modelo completo en test. Las diferencias medias pareadas por participante son −0,0009 (intervalo descriptivo 95 %: −0,0079 a +0,0045) y −0,0053 (−0,0217 a +0,0098). Un PC por señal es más compacto, pero pierde 0,0114 BA en atención y 0,0192 en activación frente al completo en validation; su aparente ventaja de activación en test no se repite allí.

El control de solo estímulo supera a todos los modelos con señales. Esto limita la interpretación: el pipeline comprime y predice sus nuevas pseudoetiquetas, pero **no demuestra una mejor medición de atención o activación**. La comparación con cifras históricas no es válida por el error de alineación y porque las etiquetas cambiaron. Test ya había sido observado en otros estudios; estas métricas son exploratorias.

## Archivos y reproducción

- `config/pca_senales.json`: entradas, partición, umbrales y reglas fijas.
- `resultados/pca_senales_24-10-2026/dataset_pca_senales.csv`: ventanas y etiquetas nuevas.
- `manifiesto_profesor.json` y `teacher_models/`: PCA del profesor y procedencia.
- `manifiesto_estudiante.json` y `student_models/`: reducción por señal, modelos y verificación de recarga.
- `metricas_estudiante.csv`, `ganancias_pca.csv`, `control_estimulo.csv` y `desalineacion_historica.json`: evaluación.

```powershell
python scripts/generar_pseudoetiquetas_pca_senales.py
python scripts/predecir_pseudoetiquetas_pca_senales.py
python scripts/control_estimulo_pca_senales.py
python scripts/resumir_pca_senales.py
python -m unittest tests.test_pca_senales tests.test_preprocesamiento -v
```
