# Resumen completo del procesamiento MDS

## Fuentes originales

- `datos/Toma_muestras_v2 Data export.tsv`: 99 columnas de Tobii, con eye tracking, pupila, eventos y GSR.
- `datos/eeg_recordings_exp_V2.zip`: sesiones OpenBCI/BrainFlow de EEG de 16 canales a aproximadamente 125 Hz.

Los originales solamente fueron trasladados a `datos/`; no se modificaron ni descomprimieron permanentemente.

## Sincronización

`scripts/sincronizar_senales.py` lee el TSV por streaming y las cabeceras dentro del ZIP. Normaliza participantes, convierte los tiempos a UTC y propone pares EEG–Tobii por participante y cercanía de inicio. El resultado está en `resultados/sincronizacion/`.

Se obtuvieron 47 candidatos directos, un caso P29 para revisar por offset y `Test_Participant` sin pareja directa. No se aplicó una corrección artificial de drift: faltan triggers independientes observados por ambos equipos.

## EDA por señal

### EEG

Se analizaron 104 sesiones y 16 canales directamente dentro del ZIP. Se calcularon duración, frecuencia efectiva, saturación en rail, repetición plana, saltos temporales y estadísticas por canal. Para el resumen final se usan solo 48 sesiones principales.

Regla flexible final:

```text
utilizable = rail_pct <= 30 % y flat_repeat_pct <= 30 %
```

Resultado: 45/48 (93,75 %) utilizables. Se excluyen P1, P14 y P17. La regla es permisiva: una sesión utilizable aún puede contener ruido considerable y debe revisarse antes de inferencia neurofisiológica.

### GSR

Se procesaron 2.984.636 filas por streaming. Se encontraron 47 grabaciones con 530.407 muestras válidas, frecuencia efectiva cercana a 15 Hz y controles temporales correctos. P7 y P42 no contienen GSR. Resultado sobre 49 grabaciones: 95,92 % disponible/válido.

### Pupilometría

Se evaluó la validez por ojo sobre 2.187.110 muestras de eye tracker. El criterio resumen exige ambos ojos válidos simultáneamente: 1.973.941 muestras, equivalentes a 90,25 %.

### Eye tracking

Se evaluó disponibilidad del punto de mirada y movimientos I-VT. Hay 2.077.373 muestras de mirada válidas (94,98 %) y 122.302 fijaciones únicas; la duración mediana es 183 ms.

## Coordinación para análisis

Las señales conservan sus frecuencias nativas. Los epochs deben recortarse con límites temporales comunes en UTC, usando los manifiestos de sincronización. GSR, pupila y mirada ya comparten el reloj Tobii; EEG usa su reloj OpenBCI convertido al mismo dominio absoluto.

## Reproducción

Ejecutar desde la raíz:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" .\scripts\ejecutar_todo.py
```

Los scripts escriben en `resultados/`; las decisiones, limitaciones y métricas están documentadas en `documentacion/`.
