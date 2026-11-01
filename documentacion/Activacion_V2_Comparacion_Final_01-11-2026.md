# Activación V2: comparación final

Etiquetas V2 aprobadas por el profesor según comunicación de Mario el 01-11-2026. Se completó el contraste no lineal con HistGradientBoosting, selección solo en train y congelación anterior a la evaluación externa.

[Informe completo, métricas y alcance](../resultados/activacion_v2_comparacion_final_01-11-2026/INFORME.md).

El contraste principal 32−1 sigue inconcluso; el secundario 8−1 muestra una diferencia favorable en test, sin reproducirse con claridad en validation/OOF. No demuestra superioridad temporal general ni validación psicológica. No se realizó la ablación de modalidades: es una tarea separada.

Reproducción en directorio nuevo: el script `scripts/activacion_v2_comparacion_final.py` separa `prepare`, `train`, `evaluate` y `report`. Conserva las salidas actuales; no relanzar fases que creen o sobrescriban estos resultados. `scripts/auditar_activacion_v2_final.py` verifica desde disco la corrida.
