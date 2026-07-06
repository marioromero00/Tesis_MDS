# EDA v2 — EEG por Estímulo

EDA de señales EEG segmentadas por estímulo, ejecutada en cluster Ray.

## Notebooks

| Notebook | Estímulos |
|----------|-----------|
| `eda_estimulos.ipynb` | Estímulos Emocionales |
| `eda_paginas_web.ipynb` | Estímulos Páginas Web |

## Pipeline por trial

1. Leer CSV sin header (columnas asignadas por posición)
2. Botar fila 0 — todos los canales en ±187500 (valor rail OpenBCI)
3. Detectar canales muertos: `>DEAD_THRESH%` de muestras en rail → excluir
4. Band-pass **1–45 Hz** con `filtfilt` (zero-phase, sin desfase)
5. Stats + PSD (Welch con numpy) sobre canales buenos filtrados

## Parámetros configurables

```python
FS          = 125       # Hz
SAT_THRESH  = 90_000   # µV — umbral de rail
DEAD_THRESH = 10       # % muestras en rail para declarar canal muerto
```

## Estructura de archivos

```
PXX_Estimulo_YY.csv
│
├── Col 0       : SampleIndex
├── Col 1–16    : EXG Channel 0–15  (EEG)
├── Col 17–19   : Accel / extras
└── Col 20      : Estimulo (número de estímulo)
```

> Sin fila de encabezado — la primera fila de datos (índice 0) contiene valores rail y se descarta.

## Acceso a datos

- Disco remoto montado en un nodo del cluster Ray (`ray://localhost:10001`)
- Las tareas se fijan al nodo con el disco via `NodeAffinitySchedulingStrategy`
- Ruta: `/Volumes/Externo4T/GoogleDrive/Tesistas Neurodatos/Datos  Crudos/EEG/EEG por Estímulo/`
