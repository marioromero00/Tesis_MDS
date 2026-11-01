# Revisión por participante y estrategia de evaluación — 29-10-2026

## Decisión

La estrategia principal será inductiva, sin normalización con datos de la persona evaluada. La estrategia relativo_offline queda como comparación secundaria explícitamente transductiva. Selección interna se conserva como análisis exploratorio, sin usarla para sustituir el resultado principal tras observar evaluación.

## Evidencia

Se recalcularon las 75 AUC por participante desde las predicciones guardadas; coinciden con las métricas publicadas a tolerancia 1e-12.

Offline menos inductivo: ΔAUC promedio 0.0055; intervalo descriptivo pareado 95 % [-0.0069, 0.0176], bootstrap de 20.000 muestras de participantes con semilla 20261029. Mejora en 15/25 personas. Este intervalo incluye cero; la revisión no establece superioridad offline. No corrige la búsqueda adaptativa previa.

| Estrategia | Media | Mediana | Mínimo | Máximo | Personas AUC >0,70 |
|---|---:|---:|---:|---:|---:|
| inductivo | 0.6982 | 0.7000 | 0.5698 | 0.7833 | 13/25 |
| relativo_offline | 0.7037 | 0.7035 | 0.6194 | 0.7883 | 15/25 |
| seleccion_interna | 0.7021 | 0.7028 | 0.5942 | 0.7833 | 15/25 |

P35 y P21 presentan las AUC inductivas menores; P3, P44 y P8 las mayores. Estas diferencias no justifican excluir personas ni cambiar etiquetas. Todos los intervalos de AUC macro publicados incluyen 0,70: superar ese valor puntualmente no prueba que la AUC poblacional lo supere.

## Protocolo definido para la próxima evaluación

1. Mantener participantes, etiquetas, ventanas, exclusiones originales y métrica principal: promedio no ponderado de ROC-AUC por persona. Conservar la extracción EEG por canal y GSR de esta ronda.
2. Elegir la configuración final de la estrategia inductiva exclusivamente dentro de los 25 participantes de train, mediante los cinco folds agrupados congelados, entre las 18 configuraciones inductivas ya especificadas. Reajustar el profesor PCA en cada partición de ajuste siguiendo el procedimiento existente. Elegir por AUC macro media; desempate por ID ascendente. Esa selección final no constituye una estimación independiente de rendimiento.
3. Reajustar la configuración elegida sobre todo train; congelar profesor, parámetros, imputación, escalado, código y hashes antes de evaluar. No escoger un único modelo por ser el mejor de los folds externos ni atribuirle automáticamente la AUC de la estrategia completa.
4. Seleccionar y congelar de la misma manera el comparador offline dentro de sus 18 configuraciones. Su normalización usa la sesión completa sin etiquetas de la persona evaluada; reportarlo separado y no presentarlo como inferencia online.
5. Evaluar una vez sobre la partición de validación congelada. Reportar AUC por persona, macro, intervalo por participantes y diferencias pareadas. Verificar primero el historial de uso de esa partición antes de describirla como independiente. No modificar decisiones después de ver sus métricas.
6. Reservar test para el informe final con decisiones congeladas. El test del proyecto fue consultado previamente en otros experimentos: documentar esa exposición y no presentarlo como confirmación completamente nueva. Una confirmación nueva requiere participantes no utilizados previamente.
7. No excluir participantes con AUC baja. Documentar cualquier persona sin ambas clases y denominadores. La etiqueta PCA es un proxy relativo offline; la evaluación no demuestra por sí sola atención psicológica ni funcionamiento en tiempo real.

Esta revisión define la estrategia; no entrena aún el modelo final ni consulta validation/test/P29.

## Detalle por persona

| Persona | Inductivo | Offline | Selección interna | Δ offline−inductivo |
|---|---:|---:|---:|---:|
| P2 | 0.7529 | 0.7639 | 0.7639 | +0.0110 |
| P3 | 0.7833 | 0.7300 | 0.7833 | -0.0533 |
| P4 | 0.7167 | 0.6944 | 0.7167 | -0.0222 |
| P8 | 0.7743 | 0.7521 | 0.7743 | -0.0221 |
| P9 | 0.6555 | 0.6199 | 0.6555 | -0.0356 |
| P12 | 0.6742 | 0.7154 | 0.7154 | +0.0411 |
| P13 | 0.7298 | 0.7363 | 0.7298 | +0.0065 |
| P18 | 0.7338 | 0.7883 | 0.7338 | +0.0544 |
| P19 | 0.6832 | 0.6657 | 0.6657 | -0.0176 |
| P20 | 0.6618 | 0.7065 | 0.6618 | +0.0447 |
| P21 | 0.5942 | 0.6413 | 0.5942 | +0.0472 |
| P22 | 0.7267 | 0.7104 | 0.7267 | -0.0163 |
| P24 | 0.6730 | 0.6813 | 0.6730 | +0.0083 |
| P26 | 0.6321 | 0.6620 | 0.6321 | +0.0299 |
| P27 | 0.7149 | 0.6915 | 0.7149 | -0.0234 |
| P30 | 0.7437 | 0.7482 | 0.7437 | +0.0045 |
| P33 | 0.6626 | 0.6308 | 0.6626 | -0.0317 |
| P34 | 0.7126 | 0.7526 | 0.7126 | +0.0400 |
| P35 | 0.5698 | 0.6194 | 0.6194 | +0.0496 |
| P36 | 0.6966 | 0.7417 | 0.6966 | +0.0450 |
| P40 | 0.6895 | 0.7028 | 0.7028 | +0.0133 |
| P43 | 0.7013 | 0.7035 | 0.7013 | +0.0022 |
| P44 | 0.7743 | 0.7429 | 0.7743 | -0.0314 |
| P46 | 0.6979 | 0.7024 | 0.6979 | +0.0045 |
| P48 | 0.7000 | 0.6884 | 0.7000 | -0.0116 |
