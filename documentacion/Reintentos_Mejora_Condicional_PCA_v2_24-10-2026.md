# Reintentos de mejora condicional con PCA v2

Fecha: 24-10-2026. Esta evaluación usa las mismas pseudoetiquetas y la misma partición por participante de la auditoría v2. El modelo estudiante de atención recibe EEG y GSR; el de activación recibe EEG, mirada y pupila. No recibe la señal que usa el profesor para definir cada etiqueta. Imputación, escala y PCA se ajustan solo con train. Validation y test tienen ocho participantes cada uno. La métrica principal es precisión balanceada (BA).

## Pregunta y protocolo

Se comparó cada modelo que combina estímulo y fisiología con otro del **mismo algoritmo que recibe solo el estímulo**. Se probaron regresión logística regularizada, CatBoost, variables completas, PCA que conserva al menos 90 % de la varianza por modalidad, un PC por modalidad y un historial causal de seis ventanas. El historial se reinicia en cambios de grabación, segmento y huecos. El clasificador se ajustó únicamente con train (25 participantes). El test ya se había inspeccionado en estudios previos y se volvió a consultar durante estos reintentos: es **exploratorio**, no una prueba independiente para elegir el mejor modelo.

| Tarea | Modelo | Validation BA | Test BA | Control comparable en test |
|---|---|---:|---:|---:|
| Atención | Estímulo, CatBoost | 0,4659 | 0,4613 | — |
| Atención | Estímulo + PCA ≥90 %, CatBoost | **0,4728** | 0,4608 | 0,4613 |
| Activación | Estímulo, CatBoost | 0,4082 | **0,4120** | — |
| Activación | Estímulo + PCA ≥90 %, CatBoost | **0,4325** | 0,3766 | 0,4120 |
| Atención | Estímulo, logística | 0,4631 | 0,4610 | — |
| Atención | Estímulo + PCA ≥90 %, logística | 0,4694 | 0,4625 | 0,4610 |
| Activación | Estímulo, logística | 0,4125 | 0,4135 | — |
| Activación | Estímulo + PCA ≥90 %, logística | 0,4132 | 0,4055 | 0,4135 |
| Atención | Estímulo + 1 PC/señal, logística | 0,4698 | 0,4658 | 0,4610 |
| Activación | Estímulo + 1 PC/señal, CatBoost | 0,4304 | 0,4025 | 0,4120 |

La validación por grupos de cinco pliegues en **train** dio una mejora media de apenas +0,0007 BA para atención y +0,0010 para activación con logística + PCA ≥90 % sobre logística de solo estímulo. En test, el intervalo bootstrap por participante para la diferencia de atención con logística fue [−0,0032; +0,0055]; cinco de ocho participantes mejoraron. Para activación con logística fue [−0,0287; +0,0132]; tres de ocho mejoraron. Con CatBoost + PCA ≥90 %, atención mejoró en tres de ocho y activación en dos de ocho; el intervalo de activación fue [−0,0713; −0,0019]. Estos intervalos son descriptivos con solo ocho participantes y sin independencia del test.

## Control negativo

Se desordenaron **juntas** las columnas PCA dentro de cada participante y estímulo, manteniendo esas dos distribuciones. Así se rompe la asociación de cada ventana entre señales y etiqueta sin cambiar el contenido visto. En test, atención con CatBoost pasó de 0,4608 a 0,4513; activación de 0,3766 a 0,3764. En el intento de un PC por señal, atención pasó de 0,4658 a **0,4722** al desordenar: la pequeña mejora observada no demuestra aporte fisiológico. Este control es una permutación descriptiva única, no una prueba de significación.

## Conclusión y límite práctico

**No se obtuvo una mejora robusta sobre el control por estímulo.** Los aumentos en validation no se reprodujeron en test, o fueron demasiado pequeños y no superaron el control negativo. No corresponde elegir el modelo que vio el test repetidas veces ni modificar las pseudoetiquetas para maximizar BA: eso mediría ajuste a la partición en vez de validez de atención y activación. El PCA sí reduce de 18 a 9 entradas en atención y de 25 a 15 en activación, como muestra la auditoría principal, pero esa compresión por sí sola no crea información nueva.

Para un avance defendible se necesita fijar antes del próximo experimento una etiqueta validada con una medida externa, reclutar o reservar participantes nunca consultados y evaluar si la fisiología mejora sobre el estímulo con intervalos por participante. El conjunto actual permite depurar y comparar modelos, pero no demostrar una mejora grande de generalización.

## Reproducción

```powershell
python scripts/experimentar_mejora_condicional_v2.py
python scripts/experimentar_mejora_condicional_v2.py --one-pc-only
python scripts/verificar_mejora_condicional_v2.py
python scripts/evaluar_logistica_condicional_v2.py
python scripts/evaluar_un_pc_condicional_v2.py
```

Resultados y modelos completos: `resultados/mejora_condicional_v2_24-10-2026/`. Las predicciones se conservan para auditoría; los reportes JSON incluyen resultados por participante y el bootstrap pareado.
