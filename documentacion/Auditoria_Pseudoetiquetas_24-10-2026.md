# Auditoría y nueva versión de pseudoetiquetas (24-10-2026)

**Corrección posterior:** se detectó una desalineación de filas en los componentes del profesor usados por esta versión. Sus etiquetas y métricas son históricas y no deben interpretarse como evaluación válida. Véase [Pipeline_PCA_Senales_24-10-2026.md](Pipeline_PCA_Senales_24-10-2026.md).

## Cambios aplicados

- La partición por participante, los scores continuos y las señales del profesor conservan su definición original.
- Las clases se calculan con cuantiles de ventanas multimodales elegibles de cada participante. Las ventanas no elegibles no reciben clase.
- P29 conserva su condición de sensibilidad y sus ventanas válidas reciben clase; no entra a train, validation ni test primarios.
- El PCA se ajusta y orienta exclusivamente con ventanas elegibles de train. El signo se decide por correlación con el score de referencia en esas ventanas.
- Los baselines requieren y aplican el indicador de elegibilidad en entrenamiento, verificación y evaluación.
- Los empates exactos conservan una sola clase. No se separan scores iguales para fabricar tres grupos. El manifiesto registra los conteos por clase y participante.

## Alcance de la nueva ejecución

Configuración: `config/modelado_auditado.json`. Datos: `resultados/modelado_auditado_24-10-2026/`. La ejecución anterior en `resultados/modelado/` se conserva como referencia histórica. Sus métricas y los experimentos posteriores que usaron ese dataset no son métricas de esta nueva versión.

Hay 21.719 ventanas primarias elegibles (13.062 train, 4.640 validation y 4.017 test), además de 482 ventanas de sensibilidad de P29. No hay etiquetas principales ausentes entre las ventanas elegibles ni etiquetas en las ventanas no elegibles.

En activación de 6 s, P34, P37 y P46 carecen de clase media por empates. Esto limita la comparación de balanced accuracy por participante: su referencia casual no es necesariamente 1/3. Los conteos exactos de cada variante están en `manifiesto_etiquetas.json`.

## Baselines recalculados

La corrida definitiva está en `resultados/modelado_auditado_24-10-2026/baselines_final/`: 30 modelos, 90 filas de métricas y un manifiesto con hashes del dataset y los modelos. La primera corrida, en `baselines/`, fue interrumpida antes de completar el ajuste de PCA; se excluye de los resultados y de Git.

| Objetivo principal, test | Modelo | BA anterior (4.025 ventanas) | BA auditada (4.017 ventanas) |
| --- | --- | ---: | ---: |
| Atención | Dummy | 0,333333 | 0,333333 |
| Atención | Logística | 0,323972 | 0,316405 |
| Atención | Random Forest | 0,319741 | 0,320139 |
| Activación 6 s | Dummy | 0,333333 | 0,333333 |
| Activación 6 s | Logística | 0,316902 | 0,317076 |
| Activación 6 s | Random Forest | 0,336462 | 0,340232 |

Las métricas anteriores proceden de `resultados/modelado/ejecuciones/baselines_05-09-2026_02/metricas_baselines.csv`. Las nuevas están en `baselines_final/metricas_baselines.csv`. No hay una ventaja general sobre Dummy en los objetivos principales. Las métricas por participante de activación deben interpretarse junto a los conteos de clases, dado que algunos participantes tienen solo dos clases.

## Reproducción

```powershell
python scripts/preparar_modelado.py --config config/modelado_auditado.json
python scripts/baselines_estaticos.py --config config/modelado_auditado.json --run-dir resultados/modelado_auditado_24-10-2026/baselines_final
python -m unittest tests.test_preprocesamiento tests.test_baselines -v
```

Para repetir los baselines, usar un `--run-dir` nuevo. El generador de etiquetas sí sobrescribe los tres productos en el directorio configurado.

## Límite metodológico

Los scores y la normalización siguen siendo offline por participante. Estas referencias no están validadas con etiquetas humanas ni confirman por sí solas atención o activación psicológica.
