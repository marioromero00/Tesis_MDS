# Estabilidad, señales del profesor y comparación acotada (24-10-2026)

**Corrección posterior:** este estudio usa pseudoetiquetas generadas con componentes desalineados entre ventanas. Sus métricas son históricas y no deben interpretarse como evaluación válida. Véase [Pipeline_PCA_Senales_24-10-2026.md](Pipeline_PCA_Senales_24-10-2026.md).

## Protocolo

Se partió del dataset auditado de 21.719 ventanas primarias elegibles y del split congelado de 25/8/8 participantes. Los diagnósticos y la definición de variantes se hicieron con train. La etiqueta auditada sigue siendo la referencia principal. Las dos alternativas son análisis de sensibilidad; no reemplazan la definición original. Los scores conservan normalización offline por participante.

Se compararon cuatro objetivos con tres modelos fijos: Dummy prior, regresión logística de la ventana actual y regresión logística con la ventana actual más el promedio causal de seis ventanas de 2 s separadas por 1 s (soporte máximo de 7 s). El historial se reinicia en cambios de grabación, segmento o saltos temporales. No hubo búsqueda de hiperparámetros. Validation y test se evaluaron una vez en esta comparación; dado el historial exploratorio del proyecto, estos resultados no son una confirmación independiente.

## 1. Estabilidad de las pseudoetiquetas

Concordancia de clases en train frente a la etiqueta auditada:

| Cambio | Atención | Activación |
| --- | ---: | ---: |
| Cuantiles 25/75 % | 83,5 % | 84,5 % |
| Cuantiles 40/60 % | 86,6 % | 87,8 % |
| Peso mirada 75 % / pupila 25 % | 69,8 % | — |
| Solo mirada | 50,5 % | — |
| Contexto GSR 2 s | — | 81,9 % |
| Contexto GSR 10 s | — | 92,4 % |
| GSR continuo de 6 s | — | 32,2 % |

La etiqueta de atención es bastante sensible al peso de pupila. El cambio de activación a GSR continuo define un objetivo sustancialmente distinto. El detalle por participante está en `estabilidad_participantes_train.csv` y los valores completos en `estabilidad_train.csv`.
Entre participantes de train, la concordancia con la candidata solo mirada va de 43,0 % a 57,7 % (mediana 50,8 %). Para GSR continuo va de 18,0 % a 58,0 % (mediana 32,0 %); la diferencia no está concentrada en una sola persona.

## 2. Revisión de señales del profesor

En train, 97,1 % de las ventanas tienen `gsr_scr_count = 0` y prominencia SCR igual a cero. P34 y P46 no tienen clase media con la etiqueta auditada de activación; la candidata continua sí produce tres clases en todos los participantes de train. La fracción de variación dentro de participante asociada al nombre del estímulo es 35,2 % para el componente de mirada, 54,8 % para el componente pupilar y 67,0 % para `pupil_mean_z`. No hay medición de luminancia disponible para separar su efecto.

La asociación con estímulo del score de activación auditado es 59,8 % y sube a 89,1 % en la alternativa de GSR continuo. Esa subida es una señal de posible deriva temporal o efecto del estímulo, no evidencia de una referencia más válida. Las cifras son descriptivas: el orden y duración de los estímulos también podrían contribuir.

## 4. Comparación fija y cuánto cambia

Precisión balanceada en test, 4.017 ventanas y ocho participantes:

| Etiqueta | Dummy | Logística estática | Logística temporal | Solo estímulo |
| --- | ---: | ---: | ---: | ---: |
| Atención auditada | 0,3333 | 0,3164 | 0,3331 | 0,3209 |
| Atención solo mirada | 0,3333 | 0,3465 | 0,3381 | 0,3485 |
| Activación auditada | 0,3333 | 0,3171 | 0,3234 | 0,3874 |
| Activación GSR continuo | 0,3333 | 0,3722 | 0,3861 | 0,3991 |

Con la **misma etiqueta auditada**, el historial suma 0,0167 puntos de BA en atención y 0,0063 en activación frente a logística estática; ambos quedan en torno a Dummy o por debajo. Cambiar la etiqueta de atención a solo mirada sube la logística estática 0,0301 puntos respecto de la estática auditada, pero el control de solo estímulo obtiene 0,3485 y la etiqueta coincide solo en 50,5 % con la anterior. Cambiar activación a GSR continuo sube la logística temporal 0,0627 puntos respecto de la temporal auditada y 0,0528 sobre Dummy; sin embargo, solo estímulo obtiene 0,3991 y la concordancia con la etiqueta anterior es 32,2 %.

**Conclusión:** hay mejoras numéricas sobre objetivos alternativos, pero no una mejora demostrada en predicción de atención o activación. El control de estímulo supera a los modelos con señales en ambas etiquetas alternativas y en activación auditada. Mantener la etiqueta auditada como referencia principal y tratar las candidatas como sensibilidad evita confundir facilidad de predicción con validez del constructo.

## Archivos y reproducción

- `resultados/estudio_pseudoetiquetas_24-10-2026/diagnosticos_train.json`
- `resultados/estudio_pseudoetiquetas_24-10-2026/estabilidad_train.csv`
- `resultados/estudio_pseudoetiquetas_24-10-2026/estabilidad_participantes_train.csv`
- `resultados/estudio_pseudoetiquetas_24-10-2026/comparacion_modelos.csv`
- `resultados/estudio_pseudoetiquetas_24-10-2026/control_estimulo.csv`

```powershell
python scripts/estudio_pseudoetiquetas.py
python scripts/comparar_pseudoetiquetas.py
python scripts/control_estimulo_pseudoetiquetas.py
python -m unittest tests.test_estudio_pseudoetiquetas -v
```
