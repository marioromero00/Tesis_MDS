# EDA reproducible de la señal GSR

## Objetivo

`eda_gsr.py` caracteriza la señal de respuesta galvánica de la piel incluida en `Toma_muestras_v2 Data export.tsv`. El análisis se hace por participante y grabación, usa el inventario creado durante la sincronización y evita cargar el archivo de 1,37 GiB completo en memoria.

La unidad física de `Galvanic skin response (GSR)` no está declarada en la exportación. Por ello, los resultados hablan de **valor GSR** y no presuponen µS. Antes de interpretar amplitudes fisiológicamente se debe confirmar el dispositivo y su configuración.

## Ejecución

Desde la carpeta `MDS`:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" .\eda_gsr.py
```

No necesita paquetes externos. Las rutas pueden cambiarse con `--input`, `--manifest` y `--output`. `--seed` fija el muestreo reproducible; `--reservoir` y `--trace-points` controlan el tamaño de las muestras usadas para cuantiles y gráficos.

## Método

1. Lee la cabecera y luego recorre el TSV línea por línea.
2. Separa grabaciones mediante `Participant name` y `Recording name`.
3. Considera una observación válida cuando la columna GSR contiene un número finito; también contabiliza filas cuyo `Sensor` es `GSR` pero cuyo valor está vacío.
4. Calcula exactamente, en una pasada: cantidad, media, desviación estándar, mínimo, máximo, timestamps duplicados y no monótonos.
5. Estima cuartiles y mediana con *reservoir sampling* determinista de hasta 10.000 valores por grabación. No son cuantiles exactos, pero escalan sin depender del tamaño del TSV.
6. Estima la frecuencia como `1 / mediana(Δt positivo)`, usando `Recording timestamp` en microsegundos.
7. Cruza cada grabación con `sincronizacion_output/inventario_tobii.csv` para conservar su inicio UTC.

Una grabación queda marcada `review` si tiene menos de 100 valores válidos, más de 5% de faltantes dentro de sus filas GSR, timestamps no monótonos o una frecuencia estimada fuera del intervalo amplio 0,5–2000 Hz. Estos umbrales son controles técnicos, no criterios de exclusión fisiológica.

## Productos

En `eda_output/gsr` se generan:

- `gsr_por_grabacion.csv`: estadísticas y banderas de calidad por grabación.
- `gsr_muestra_trazas.csv`: muestra reproducible y acotada para visualización o análisis rápido.
- `resumen_gsr.json`: procedencia, parámetros y totales del procesamiento.
- `01_muestras_validas.svg`: cobertura por participante.
- `02_frecuencia_muestreo.svg`: frecuencia efectiva estimada.
- `03_mediana_gsr.svg`: nivel central por participante.
- `04_trazas_normalizadas.svg`: trazas exploratorias; el tiempo se normaliza a 0–1 y cada señal se centra por su mediana y escala por el intervalo P05–P95.

Los SVG se abren directamente en un navegador y no requieren Matplotlib.

## Resultado de la ejecución verificada

La ejecución completa del 12 de agosto de 2026 recorrió **2.984.636 filas** (1.470.821.789 bytes) y encontró:

- 47 grabaciones con GSR;
- 530.407 valores GSR válidos;
- entre 2.040 y 14.615 muestras válidas por grabación;
- frecuencia estimada de aproximadamente 15 Hz en todas las grabaciones encontradas;
- cero filas GSR vacías, valores no numéricos, timestamps duplicados o timestamps no monótonos;
- cero grabaciones marcadas para revisión por los umbrales técnicos definidos.

Hay inventario Tobii para 49 grabaciones, pero solo 47 contienen GSR. No aparecen grabaciones GSR de `P7` ni `P42`; esto debe interpretarse como ausencia de la señal en la exportación, no como un error del lector. `Test_Participant` sí contiene GSR y se conserva explícitamente para que el equipo decida si pertenece al análisis final.

## Interpretación y límites

- Diferencias de nivel basal entre personas pueden provenir de contacto de electrodos, temperatura, humedad o configuración; no deben interpretarse automáticamente como diferencias emocionales.
- La EDA no descompone aún componentes tónica (SCL) y fásica (SCR), porque eso requiere confirmar unidad, frecuencia y filtros del sensor.
- Los cuantiles y las trazas son aproximaciones reproducibles; media, desviación, extremos y conteos son exactos sobre todos los valores leídos.
- Una frecuencia estable y pocos faltantes indican integridad temporal, pero no garantizan calidad fisiológica.
- Para comparar con EEG o mirada se debe usar la tabla de coordinación y mantener explícito el offset estimado. Este script no modifica ni remuestrea la señal original.

## Siguiente análisis recomendado

Tras confirmar la unidad y el hardware: detectar saltos y artefactos, filtrar suavemente según la frecuencia real, separar SCL/SCR, extraer número/amplitud/latencia de respuestas y calcular métricas en ventanas definidas por eventos experimentales. Las decisiones y exclusiones deben quedar registradas por participante.
