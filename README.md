# MDS — señales neurofisiológicas multimodales

> [!abstract] Navegación Obsidian
> Consulte [[Mapa del proyecto]] para recorrer datos, sincronización, EDA, resultados y scripts.

Proyecto con EEG, GSR, pupilometría y eye tracking, sus manifiestos de sincronización y análisis exploratorios reproducibles.

## Estructura

```text
MDS/
├── datos/                 # originales sin modificar
├── scripts/               # sincronización y EDA reproducibles
├── documentacion/         # metodología e informes por señal
├── resultados/
│   ├── sincronizacion/    # inventarios y coordinación EEG–Tobii
│   └── eda/               # tablas y gráficos por modalidad
└── README.md
```

## Resumen de lo realizado

1. Se inventariaron el TSV Tobii/GSR y las 104 sesiones OpenBCI del ZIP.
2. Se reconstruyó un dominio UTC común y se emparejaron sesiones por participante y proximidad temporal.
3. No se estimó drift sin triggers compartidos; `drift_scale=1.0` significa que no existe una corrección identificable.
4. Se ejecutaron EDA independientes para EEG, GSR, pupilometría y eye tracking.
5. Se implementó y ejecutó un preprocesamiento multimodal secuencial sobre ventanas UTC comunes.
6. Se fijaron configuración, dependencias, pruebas, hashes y auditoría para reproducirlo.
7. Se adoptó un criterio EEG exploratorio flexible: utilizable si saturación y repetición plana son ≤30 %.

## Calidad por fuente

| Fuente | Criterio | Utilizable/válido |
|---|---|---:|
| EEG | Sesiones principales con saturación y repetición plana ≤30 % | 44/48 = **91,67 %** |
| GSR | Grabaciones con señal correcta sobre las 49 Tobii | 47/49 = **95,92 %** |
| Pupilometría | Ambos ojos válidos simultáneamente | **90,25 %** de muestras |
| Eye tracking | Punto de mirada válido | **94,98 %** de muestras |

En EEG se excluyen P1, P14, P17 y P25. P25 se identificó al corregir la selección de sesiones con varios TXT. La regla es útil para exploración tolerante al ruido, pero los casos cercanos al umbral deben seguir marcados como baja calidad.

## Ejecución

Desde la raíz `MDS`:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" .\scripts\ejecutar_todo.py
```

Todos los scripts procesan los archivos grandes por streaming o directamente dentro del ZIP.

La ejecución completa es estrictamente secuencial. Preparación y validación:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python .\scripts\ejecutar_todo.py
```

## Documentación principal

- `documentacion/DOCUMENTACION_DATOS_MDS.md`: estructura y diccionario de fuentes.
- `documentacion/SINCRONIZACION_SENALES.md`: coordinación, offsets y limitaciones.
- `documentacion/EDA_SENALES.md`: índice de las cuatro señales.
- `documentacion/EDA_EEG.md`, `EDA_GSR.md`, `EDA_EYE_PUPIL.md`: detalle por modalidad.
- `documentacion/PREPROCESAMIENTO_MULTIMODAL.md`: protocolo, características, calidad y reproducción.
- `documentacion/Sincronizacion señales.ipynb`: notebook original de referencia.

## Notas relacionadas

- [[documentacion/RESUMEN_PROCESO|Resumen del procesamiento]]
- [[documentacion/EDA_SENALES|EDA de las cuatro señales]]
- [[documentacion/GRAFICOS_TESIS|Gráficos para la tesis]]
- [[datos/README|Datos locales]]

## Precauciones

- No mezclar sesiones `test` con principales sin justificarlo.
- Revisar P29 por offset y `Test_Participant` por falta de correspondencia.
- P7 y P42 no tienen GSR.
- Mantener las frecuencias nativas y recortar epochs mediante timestamps comunes.
- Una sincronización submuestra requiere triggers observables en ambos dispositivos.
