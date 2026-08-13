# EDA de eye tracking y pupilometría

Este análisis explora las señales Tobii del archivo `Toma_muestras_v2 Data export.tsv`. Se diseñó para ser reproducible y evitar cargar los 1,47 GB completos en memoria: lee únicamente 18 columnas y procesa bloques de 250.000 filas.

## Ejecución

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" .\eda_eye_pupil.py
```

Dependencias: Python 3.10 o superior, `pandas`, `numpy` y `matplotlib`. Se pueden cambiar las rutas y el tamaño de bloque con `--input`, `--manifest`, `--output` y `--chunksize`.

## Qué calcula

- Conteos globales y por participante de muestras con coordenadas de mirada, pupila izquierda, derecha y ambos ojos.
- Categorías originales de `Validity left/right`, sin reinterpretarlas ni imputarlas.
- Distribución de tipos de movimiento (`Fixation`, `Saccade`, `EyesNotFound`, etc.).
- Fijaciones únicas identificadas por participante e índice del evento; así la duración no se suma repetidamente por cada muestra del mismo evento.
- Media, desviación, mínimo y máximo exactos mediante acumuladores en streaming.
- Percentiles aproximados a partir de una muestra aleatoria determinista (semilla fija), declarados como tales en la tabla.
- Distribuciones pupilares, mapa de densidad espacial y completitud por participante.

Una fila se considera de eye tracking si `Sensor == Eye Tracker` o contiene mirada/pupila. La mirada válida operativa exige X e Y presentes; la pupila válida exige un diámetro numérico presente. Estas métricas de completitud no sustituyen las banderas de validez del equipo.

## Resultados

La carpeta `eda_output/eye_pupil` contiene:

- `metadata.json`: trazabilidad, volumen leído, participantes y tamaño de muestra.
- `resumen_numerico.csv`: estadística descriptiva de coordenadas, pupila y duración.
- `calidad_por_participante.csv`: completitud absoluta y porcentual.
- `validez_ojos.csv`: categorías de validez izquierda/derecha.
- `movimientos_oculares.csv`: frecuencia de estados o movimientos.
- `fijaciones_unicas.csv`: tabla de eventos de fijación no duplicados.
- `resumen_fijaciones.csv`: distribución de duración calculada sobre eventos únicos (no sobre muestras repetidas).
- `manifiesto_tobii_usado.csv`: copia del inventario usado para trazabilidad.
- `pupila_y_movimientos.png`, `densidad_mirada.png` y `calidad_por_participante.png`.

## Interpretación y cautelas

Los histogramas y el mapa espacial usan una muestra determinista para mantener bajo el consumo de memoria; los conteos y estadísticas acumulables recorren todas las filas. Los valores pupilares extremos se preservan en CSV, aunque el gráfico limita su visualización a 1–10 mm para que los artefactos no oculten la distribución principal. No se interpolan pérdidas, no se corrige parpadeo y no se filtran participantes: esas decisiones deben realizarse después de revisar la calidad individual.

`Gaze event duration` en `resumen_numerico.csv` describe las filas y repite el valor durante las muestras que pertenecen al mismo evento. Para describir fijaciones debe usarse `resumen_fijaciones.csv`, que deduplica por participante e índice de evento.

Las coordenadas en píxeles dependen de la resolución y del estímulo. Para comparaciones entre resoluciones deben preferirse las coordenadas `MCSnorm`. El mapa agregado tampoco representa una prueba estadística de atención: mezcla participantes, estímulos y tiempos. Para análisis inferencial se recomienda segmentar primero según eventos sincronizados y usar participante como unidad experimental.
