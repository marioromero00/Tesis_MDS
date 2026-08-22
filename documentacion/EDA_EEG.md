# EDA reproducible de la señal EEG

> [!info] Relacionado
> [[EDA_SENALES|EDA multimodal]] · [[SINCRONIZACION_SENALES|Sincronización]] · [[GRAFICOS_TESIS|Gráficos]] · [[../resultados/eda/eeg/eeg_resumen_sesiones.csv|Resultados EEG]]

## Objetivo y alcance

`eda_eeg.py` caracteriza los 16 canales EXG de cada sesión incluida en
`eeg_recordings_exp_V2.zip`. Usa como fuente de identidad y metadatos
`sincronizacion_output/inventario_eeg.csv`, y añade el estado y *offset* de
`sincronizacion_output/coordinacion_sesiones.csv`. El ZIP se lee directamente:
no se extraen copias de varios GB.

## Ejecución

En este equipo, Python está en:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" .\eda_eeg.py
```

Para una comprobación rápida:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" .\eda_eeg.py --limit 2 --output eda_output/eeg_prueba
```

No requiere pandas, NumPy ni matplotlib. Los argumentos `--zip`, `--manifest`,
`--coordination`, `--output`, `--stride` y `--limit` permiten reproducir o
adaptar el análisis. El valor predeterminado `--stride 10` inspecciona todas
las filas para contarlas, pero calcula métricas de señal con una muestra
sistemática de una de cada diez filas. Use `--stride 1` para el cálculo exacto,
a costa de más tiempo.

## Métricas

Por sesión se informa formato, tamaños, filas, duración por timestamp,
frecuencia efectiva, errores de parseo, saltos temporales, saturación y
repetición plana. Por canal se calcula número analizado, media, desviación
estándar, mínimo y máximo en µV mediante un algoritmo en línea estable.

- **Frecuencia efectiva:** `(muestras analizadas - 1) × stride / duración`.
  Se contrasta con los 125 Hz nominales del manifiesto.
- **Saturación (rail):** proporción de canal-muestras con magnitud de al menos
  187499 µV, cercana al límite observado de Cyton/Daisy (±187500 µV).
- **Repetición plana:** valores exactamente iguales entre observaciones
  consecutivas de la muestra sistemática. Es un indicador de canal clavado,
  no una prueba clínica de señal plana.
- **Saltos temporales:** intervalos mayores que el máximo entre 0,1 s y cinco
  veces la mediana de los intervalos muestreados.

El criterio final acordado es deliberadamente flexible: `utilizable` cuando la
saturación y la repetición plana son ambas ≤30 %, y `excluir` cuando cualquiera
supera 30 %. Las métricas continuas se conservan para auditoría. Esta regla está
orientada a exploración tolerante al ruido y no sustituye revisión de montaje,
impedancias, espectro y protocolo experimental.

## Salidas

La carpeta `resultados/eda/eeg` contiene:

- `eeg_resumen_sesiones.csv`: inventario y calidad por sesión, enlazado con la
  sincronización.
- `eeg_estadisticas_canales.csv`: estadística descriptiva de los 16 canales.
- `eeg_resumen.json`: parámetros, conteos de calidad y cuantiles globales.
- `eeg_frecuencia_efectiva.svg`, `eeg_saturacion.svg` y
  `eeg_repeticion_plana.svg`: gráficos autocontenidos, abribles en navegador.

## Interpretación y limitaciones

Las amplitudes extremas y canales sostenidos en rail indican desconexión,
ganancia/configuración inadecuada o saturación; no deben interpretarse como
actividad cerebral. Las medias grandes sugieren offset DC. Esta EDA opera
sobre señal cruda y no aplica referencia, notch, pasa-banda, ICA ni rechazo de
artefactos. Tampoco estima potencia por bandas: hacerlo correctamente requiere
decidir referencia, filtros y tratamiento de segmentos saturados. La
sincronización actual usa offset constante (`drift_scale=1`); las métricas EEG
no demuestran ausencia de deriva frente a Tobii.

Los registros TXT y BrainFlow alternan índices de muestra pares en algunos
archivos, pero sus timestamps avanzan aproximadamente cada 8 ms; por eso la
frecuencia se estima desde timestamps y no desde la diferencia del índice.

## Resultado actualizado el 22 de agosto de 2026

Se procesaron las 104 sesiones del manifiesto sin errores. Para el informe final
se consideran las 48 sesiones principales: 44 son `utilizable` y 4 se marcan
`excluir`, equivalentes a 91,67 % utilizable. Se excluyen P17 (59,21 %), P1
(37,90 %), P14 (31,24 %) y P25, cuya repetición plana alcanza 36,05 %. La
frecuencia efectiva mediana global fue 125,144 Hz, coherente con 125 Hz nominales. En
cambio, la mediana global de canal-muestras en rail fue 27,945%, evidencia de
que la saturación es el principal problema de calidad del conjunto crudo.

Las sesiones principales con mayor saturación estimada fueron P17 (59,21%), P1
(37,90%), P14 (31,24%), P15 (26,25%) y P16 (25,00%). Estos porcentajes se
calcularon con `stride=10`; conviene confirmarlos con `--stride 1` antes de
excluir datos. La alta saturación explica por qué no se presenta potencia por
bandas como resultado primario: un espectro de canales clavados estaría
dominado por el defecto de adquisición y podría inducir conclusiones erróneas.

La actualización corrige sesiones con varios TXT: se usa el archivo más largo,
evitando fragmentos de arranque. Esto recuperó la adquisición completa de P48
(846,55 s) y reveló la baja calidad del registro principal de P25.
