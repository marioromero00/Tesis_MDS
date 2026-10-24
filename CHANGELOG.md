# Registro de cambios

Los cambios de código, datos derivados, evaluaciones y presentaciones se registran aquí antes de publicarlos en Git.

## 24-10-2026 — Auditoría de pseudoetiquetas y pipeline PCA v2

- Se detectó y corrigió una desalineación de filas en `scripts/preparar_modelado.py`. El componente pupilar histórico era incorrecto en las 21.719 ventanas primarias válidas. Los documentos de resultados anteriores se marcaron como históricos no comparables.
- Se generó una versión auditada que filtra ventanas no elegibles al crear clases, entrenar y evaluar. Se preservó la ejecución anterior en su directorio.
- Se estudiaron estabilidad, señales del profesor y fusiones; los controles basados solo en el estímulo mostraron que la predictibilidad de las etiquetas no equivale a validez del constructo. Estos estudios se conservan con sus resultados y limitaciones documentadas.
- Se construyó `config/pca_senales_v2.json`: PCA del profesor ajustado con train elegible; GSR continuo tónico/fásico; normalización solo con ventanas elegibles; contexto causal reiniciado ante huecos.
- Se compararon modelos del estudiante con entradas completas, PCA que conserva al menos 90 % de varianza por señal y un PC por señal. Se guardaron modelos, predicciones, métricas, manifiestos e intervalos pareados en `resultados/pca_senales_v2_24-10-2026/`.
- Se creó la [presentación final PCA](presentaciones/Presentacion-Final-Tesis-PCA-24-10-2026.pptx) con diez láminas: las siete visuales vigentes y tres nuevas sobre auditoría, pipeline y resultados. El script generador y la verificación de cifras están en `scripts/`.
- Se añadieron pruebas para la alineación por participante, exclusión de ventanas descartadas, ajuste PCA en train y reinicio del contexto. La [auditoría v2](documentacion/Auditoria_PCA_Senales_v2_24-10-2026.md) contiene cifras, límites y comandos de reproducción.
