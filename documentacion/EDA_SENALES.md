# EDA multimodal de señales MDS

> [!info] Navegación
> [[../Mapa del proyecto|Mapa]] · [[EDA_EEG|EEG]] · [[EDA_GSR|GSR]] · [[EDA_EYE_PUPIL|Pupilometría y eye tracking]] · [[GRAFICOS_TESIS|Figuras]]

Este índice reúne los análisis exploratorios reproducibles de las cuatro señales del conjunto MDS. Los resultados se guardan bajo `resultados/eda/`.

## Ejecución

```powershell
$pythonExe = "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"
& $pythonExe .\scripts\eda_eeg.py
& $pythonExe .\scripts\eda_gsr.py
& $pythonExe .\scripts\eda_eye_pupil.py
```

Dependencias instaladas: NumPy, pandas, Matplotlib, SciPy y PyArrow.

## Resultados por señal

| Señal | Documentación | Salida | Resultado principal |
|---|---|---|---|
| EEG | `EDA_EEG.md` | `resultados/eda/eeg/` | 45/48 sesiones principales utilizables con el umbral flexible de 30 %. |
| GSR | `EDA_GSR.md` | `resultados/eda/gsr/` | 47/49 grabaciones disponibles y correctas; frecuencia cercana a 15 Hz. |
| Pupilometría | `EDA_EYE_PUPIL.md` | `resultados/eda/eye_pupil/` | 90,25 % de muestras con ambos ojos válidos. |
| Eye tracking | `EDA_EYE_PUPIL.md` | `resultados/eda/eye_pupil/` | 94,98 % de muestras con mirada válida y 122.302 fijaciones. |

## Lectura conjunta

- La frecuencia EEG efectiva es estable alrededor de 125 Hz. El criterio flexible excluye solo saturación o repetición plana >30 %; no reemplaza inspección visual.
- El GSR observado está aproximadamente a 15 Hz. Este resultado empírico corrige la aproximación de 8 Hz indicada en el notebook de referencia.
- Eye tracking y pupila tienen alta disponibilidad global, aunque la validez debe evaluarse por participante y ojo antes de modelar.
- Las modalidades no fueron remuestreadas a una frecuencia común. Deben coordinarse mediante timestamps y `resultados/sincronizacion/coordinacion_sesiones.csv`.
- Las salidas agregadas sirven para selección y control de calidad; los análisis inferenciales deben aplicarse después de confirmar sesiones y condiciones experimentales.

## Orden recomendado para análisis posterior

1. Aprobar o corregir las correspondencias del manifiesto de sincronización.
2. Excluir pruebas técnicas y archivos vacíos.
3. Definir criterios finales de calidad EEG, GSR y validez ocular.
4. Recortar ventanas comunes por evento manteniendo 125 Hz para EEG y la frecuencia nativa de Tobii.
5. Preprocesar cada modalidad y extraer características solo de sesiones aprobadas.

Los documentos específicos explican métricas, columnas generadas, gráficos, umbrales y limitaciones con mayor detalle.
