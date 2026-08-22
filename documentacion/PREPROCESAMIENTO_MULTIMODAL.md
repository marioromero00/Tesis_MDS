# Preprocesamiento multimodal secuencial y reproducible

> [!info] Relacionado
> [[../Mapa del proyecto|Mapa]] · [[SINCRONIZACION_SENALES|Sincronización]] · [[EDA_SENALES|EDA]] · [[../resultados/preprocesamiento/auditoria_participantes.csv|Auditoría]]

## Propósito

`scripts/preprocesamiento_secuencial.py` transforma los originales EEG y Tobii
en una tabla de características por ventana. El procedimiento es determinista,
no modifica los originales y detiene la ejecución ante cualquier error. La
configuración completa está en `config/preprocesamiento.json`.

## Orden de ejecución

1. Valida rutas, tamaños y SHA-256 de los insumos.
2. Lee el TSV Tobii por bloques y lo particiona temporalmente por participante.
3. Propaga la etiqueta de estímulo y excluye la calibración declarada.
4. Genera ventanas de 2 s con salto de 1 s dentro de cada segmento; ninguna
   ventana atraviesa un cambio de estímulo.
5. Extrae GSR, pupila y mirada en el reloj Tobii.
6. Extrae EEG sobre exactamente los mismos límites UTC.
7. Calcula calidad, auditoría, hashes y configuración efectiva y elimina los
   intermedios.

## Ejecución desde cero

Desde la raíz del repositorio:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python .\scripts\ejecutar_todo.py
```

Solo preprocesamiento:

```powershell
python .\scripts\preprocesamiento_secuencial.py
```

Prueba real acotada:

```powershell
python .\scripts\preprocesamiento_secuencial.py --only-participants P2 --skip-hashes
```

`--skip-hashes` es únicamente para pruebas. Las rutas se resuelven desde la raíz
del repositorio.

## Transformaciones

### GSR

- Frecuencia nativa aproximada de 15 Hz y normalización por sesión.
- Componente tónica mediante Butterworth pasa-bajos de segundo orden a 0,05 Hz;
  componente fásica como diferencia.
- Cobertura, media, desviación, extremos, pendiente, tónica, fásica y picos SCR.

### Pupila

- Solo diámetros marcados válidos; ambos ojos se combinan mediante su media.
- Interpolación interior de huecos de hasta 0,2 s y normalización por sesión.
- Cobertura, validez binocular, media, desviación, extremos y pendiente.
- No se corrige luminancia porque no existe una serie de luminancia sincronizada.

### Eye tracking

- Frecuencia Tobii aproximada de 60 Hz.
- Cobertura, dispersión, trayectoria y conteos/duraciones de fijaciones y
  sacádicos; eventos deduplicados por `Eye movement type index`.

### EEG

- 16 canales y timestamps Unix, frecuencia nominal 125 Hz.
- Mediana por canal, RMS, desviación, rango pico a pico, ruido de línea y
  potencias relativas delta, theta, alfa, beta y gamma con FFT y ventana Hann.
- P1, P14, P17 y P25 se conservan para auditoría, pero se marcan
  `eeg_quality_usable=False`.

## Calidad y casos especiales

- Cobertura mínima: GSR/pupila/mirada 50 %; EEG 80 %.
- P7 y P42 carecen de GSR.
- P29 conserva `eeg_match_status=revisar_offset` y requiere revisión.
- P48 tenía dos TXT; se selecciona el más largo, evitando un fragmento de 13 s
  y usando la adquisición principal de 846 s.
- `drift_scale=1.0` significa «sin corrección identificable», no ausencia
  demostrada de deriva.

## Resultado del 22 de agosto de 2026

- 48 participantes y 25.992 ventanas.
- 22.201 ventanas multimodales válidas.
- 24.541 ventanas con GSR suficiente.
- 25.964 con pupila, 25.887 con mirada y 25.958 con EEG suficiente.
- 25.510 ventanas `candidato` y 482 de P29 con `revisar_offset`.

## Productos

| Archivo | Contenido |
|---|---|
| `resultados/preprocesamiento/caracteristicas_multimodales.csv` | 25.992 ventanas y 59 columnas. |
| `resultados/preprocesamiento/auditoria_participantes.csv` | Conteos y calidad de 48 participantes. |
| `resultados/preprocesamiento/configuracion_efectiva.json` | Parámetros utilizados. |
| `resultados/preprocesamiento/manifiesto_ejecucion.json` | SHA-256, versiones, duración y hashes de salidas. |

Los intermedios `.work` y eventuales Parquet se ignoran en Git. Los resultados
tabulares y el manifiesto sí se versionan para auditar la ejecución publicada.

## Alcance metodológico

La tabla queda preparada para modelado exploratorio. Antes de entrenar modelos
debe confirmarse con el profesor si la etiqueta emocional corresponde a
activación (*arousal*) y cómo se incorporarán las señales del docente sin
circularidad con las del estudiante.
