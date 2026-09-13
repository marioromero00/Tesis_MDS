# Transformer y TCN: 13-09-2026

Esta búsqueda no mejora el Ridge anterior: selección conjunta 0,371558, TCN 0,366822 y Transformer 0,363442 frente a Ridge 0,374750. Los intervalos de las diferencias incluyen cero. El control con ventana actual repetida obtiene 0,374911: no hay evidencia clara de aporte del historial. Recall medio de la selección conjunta: 19,62 %, frente a 23,27 % del Ridge de referencia.

Se evaluaron redes nuevas para activación, con las mismas 24 variables y arousal_label_6s. Seis configuraciones, 30 entrenamientos internos, 90 checkpoints y 270 decisiones internas (época 4/8/12 por suavizado 1/8/32). Se guardaron además 20 modelos externos.

## Resultados

| Modelo | BA macro por persona | BA global | Macro-F1 |
|---|---:|---:|---:|
| TCN | 0.366822 | 0.362543 | 0.353388 |
| Transformer | 0.363442 | 0.353765 | 0.344896 |
| all | 0.371558 | 0.362569 | 0.354706 |
| repeat_current | 0.374911 | 0.361626 | 0.350649 |

Referencia Ridge anterior: 0.374750. Ridge sin fixation_count: 0.384325; este último es un máximo exploratorio de la ablación previa, no una referencia confirmatoria.

| Contraste frente a Ridge | Ganancia (pp) | IC descriptivo 95 % (pp) | Personas que mejoran |
|---|---:|---:|---:|
| TCN | -0.793 | [-2.951; +1.564] | 12/25 |
| Transformer | -1.131 | [-3.944; +1.454] | 10/25 |
| all | -0.319 | [-2.612; +1.993] | 12/25 |
| repeat_current | +0.016 | [-2.173; +2.292] | 13/25 |

Historial frente al control de ventana actual repetida: -0.335 pp, IC [-1.466; +0.863]. El control se reajusta desde cero con la arquitectura, época y suavizado elegidos para all; no tiene una búsqueda propia. Ambos pueden aprovechar historial mediante suavizado de salida.

## Iteraciones y selección

Cada arquitectura se probó con (contexto, ancho, dropout, learning rate, weight decay): (8,16,0.2,0.001,0.01), (32,16,0.3,0.0005,0.01) y (32,32,0.4,0.001,0.1). Estas variantes cambian varios hiperparámetros a la vez; no identifican efectos aislados. Las épocas y el suavizado se eligen dentro del fold. No se siguió entrenando en respuesta a métricas externas.

| Fold | Selección | Configuración | Época | Suavizado | BA interna |
|---|---|---|---:|---:|---:|
| 1 | all | Transformer_0 | 4 | 1 | 0.387297 |
| 1 | Transformer | Transformer_0 | 4 | 1 | 0.387297 |
| 1 | TCN | TCN_0 | 4 | 1 | 0.371414 |
| 2 | all | TCN_1 | 4 | 1 | 0.379621 |
| 2 | Transformer | Transformer_2 | 4 | 32 | 0.371857 |
| 2 | TCN | TCN_1 | 4 | 1 | 0.379621 |
| 3 | all | Transformer_0 | 4 | 8 | 0.371912 |
| 3 | Transformer | Transformer_0 | 4 | 8 | 0.371912 |
| 3 | TCN | TCN_0 | 12 | 1 | 0.351924 |
| 4 | all | Transformer_2 | 12 | 1 | 0.346612 |
| 4 | Transformer | Transformer_2 | 12 | 1 | 0.346612 |
| 4 | TCN | TCN_2 | 8 | 8 | 0.338858 |
| 5 | all | TCN_1 | 8 | 32 | 0.407533 |
| 5 | Transformer | Transformer_0 | 8 | 32 | 0.377575 |
| 5 | TCN | TCN_1 | 8 | 32 | 0.407533 |

Promedio descriptivo interno sobre cinco folds y tres suavizados, por configuración y época. Resume lo probado; no se usa para volver a elegir un ganador externo.

| Configuración | Época 4 | Época 8 | Época 12 |
|---|---:|---:|---:|
| TCN_0 | 0.3404 | 0.3369 | 0.3379 |
| TCN_1 | 0.3497 | 0.3480 | 0.3397 |
| TCN_2 | 0.3329 | 0.3363 | 0.3340 |
| Transformer_0 | 0.3477 | 0.3487 | 0.3482 |
| Transformer_1 | 0.3289 | 0.3274 | 0.3275 |
| Transformer_2 | 0.3365 | 0.3409 | 0.3385 |

## Diagnóstico por clase

| Modelo | Clase | Recall | Fracción predicha |
|---|---|---:|---:|
| TCN | bajo | 0.5055 | 0.4659 |
| TCN | medio | 0.1863 | 0.1747 |
| TCN | alto | 0.3959 | 0.3594 |
| Transformer | bajo | 0.4712 | 0.4391 |
| Transformer | medio | 0.1814 | 0.1576 |
| Transformer | alto | 0.4087 | 0.4033 |
| all | bajo | 0.4899 | 0.4538 |
| all | medio | 0.1962 | 0.1705 |
| all | alto | 0.4016 | 0.3757 |
| repeat_current | bajo | 0.4786 | 0.4448 |
| repeat_current | medio | 0.1727 | 0.1532 |
| repeat_current | alto | 0.4336 | 0.4020 |

## Alcance y auditoría

Cinco folds externos de 20/5 personas; selección en una división interna fija 16/4 de cada fold. Se conservan las 25 personas de train y sus 13.524 ventanas. Validation y test originales no se reevaluaron. Una semilla (20260913): los intervalos no incorporan variación entre semillas. El único split interno puede dar una selección inestable.

Imputación con mediana e indicadores de ausencia y escalado ajustados únicamente con personas de fit. Pérdida ponderada para dar igual peso a cada persona y a sus clases observadas. BA macro promedia el recall de clases presentes en cada persona; dos personas no tienen las tres clases. Los controles constantes bajo/alto alcanzan 0,346667 en esta métrica; medio, 0,306667.

TCN usa cuatro bloques residuales, dilataciones 1/2/4/8, dos convoluciones de kernel 3 por bloque. Transformer usa una capa, cuatro cabezas, posiciones aprendidas y máscaras causales y de padding. Solo se entrega historia hasta la ventana evaluada, reiniciando por persona, grabación o salto distinto de un segundo. Se permite cruzar límites de estímulo. El contexto máximo de 32 ventanas abarca 33 segundos de señal; con suavizado de 32 puede abarcar 64 segundos. La normalización original de señales sigue siendo offline.

Fuente de implementación: [PyTorch TransformerEncoder](https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoder). GSR y etiquetas no son entradas del estudiante. La auditoría predice con señales y metadatos únicamente.

Auditoría: 110 modelos recargados, preprocesadores reajustados, 270 decisiones internas recalculadas y 54096 predicciones externas verificadas. Error máximo de scores 2.98e-08; tolerancia 1e-7 para float32/CSV, clases idénticas. Hashes de fuentes, particiones y modelos comprobados; selección reconstruida antes de interpretar resultados. Las 61 pruebas del proyecto pasaron en 11,760 segundos, incluidas las nuevas pruebas de causalidad, padding, reinicios y control repetido. Registro en pruebas.json.

Intervalos de 2.000 remuestreos pareados de personas, descriptivos, sin corrección por selección múltiple ni dependencia entre folds. Reutilizar train en muchas rondas hace esta comparación exploratoria. Los resultados no prueban importancia fisiológica ni superioridad confirmada.

Meta BA macro 0,50: no alcanzada.

Artefactos: protocolo.json, intentos.csv, selecciones.json, curvas/, internos/, modelos/, predicciones_internas/, predicciones_oof.csv.gz, contrastes.csv y verificacion.json. Carga: joblib.load del bundle y redes_secuencia_13.predict(bundle, frame).
