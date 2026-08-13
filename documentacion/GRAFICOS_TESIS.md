# Gráficos EDA para la tesis

El script `scripts/graficos_tesis.py` transforma las tablas EDA ya calculadas en seis figuras editoriales consistentes. No vuelve a leer los archivos crudos.

## Figuras

1. `01_resumen_calidad_modalidades`: comparación de EEG, GSR, pupilometría y eye tracking.
2. `02_eeg_saturacion_participantes`: saturación EEG ordenada, con umbral flexible de 30 %.
3. `03_eeg_resumen_calidad`: frecuencia efectiva y proporción utilizable/excluida.
4. `04_gsr_resumen`: muestreo, disponibilidad y variabilidad GSR.
5. `05_eye_pupil_validez_participantes`: mapa de calor de validez ocular.
6. `06_eye_tracking_movimientos_fijaciones`: movimientos oculares y duración de fijaciones.

Cada figura se exporta únicamente como PNG a 300 dpi. Los archivos están en `resultados/figuras_tesis/`.

## Reproducción

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" .\scripts\graficos_tesis.py
```

## Recomendación de uso

- Use directamente los PNG; no los sustituya por capturas de pantalla.
- Mantenga el pie de figura separado del título gráfico y explique que los criterios difieren por modalidad.
- En EEG indique que el umbral de 30 % es exploratorio y permisivo.
