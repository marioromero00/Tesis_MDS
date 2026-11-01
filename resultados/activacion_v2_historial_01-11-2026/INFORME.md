# Activación V2: primer contraste fijo de historial

Regresión logística C=1 en los cinco folds heredados de train. Mismas filas y etiquetas V2 en los tres contextos; preprocesamiento ajustado solo en personas de entrenamiento de cada fold. Modelo fijo sin búsqueda ni selección por resultados. EEG, mirada y pupila como entradas; GSR reservado al profesor.

| Contexto | AUC macro persona | IC descriptivo 95% |
|---|---|---|
| 1 | 0.5261 | [0.4896; 0.5678] |
| 8 | 0.5183 | [0.4700; 0.5712] |
| 32 | 0.5139 | [0.4660; 0.5661] |

| Historial menos actual | ΔAUC | IC descriptivo 95% | Personas mejoran |
|---|---|---|---|
| 8 | -0.0078 | [-0.0512; 0.0405] | 12/25 |
| 32 | -0.0122 | [-0.0613; 0.0404] | 10/25 |

El historial se limita a ventanas retenidas consecutivas; se reinicia en huecos y cambios de segmento. Consultar cobertura_historial.csv. Son agregados históricos, no modelos sensibles al orden de la secuencia. Los intervalos bootstrap por persona son descriptivos, sin corrección por comparaciones múltiples. Train fue reutilizado históricamente. No se evaluó validation ni test. Las etiquetas offline no validan un constructo psicológico y cambiaron frente a las corridas anteriores: no interpretar diferencias de AUC entre versiones como mejora del modelo.
