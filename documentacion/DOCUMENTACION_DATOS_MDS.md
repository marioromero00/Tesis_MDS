# Documentación de los datos de MDS

> [!info] Relacionado
> [[../Mapa del proyecto|Mapa]] · [[SINCRONIZACION_SENALES|Sincronización]] · [[EDA_SENALES|EDA]] · [[../datos/README|Datos locales]]

## 1. Resumen general

La carpeta contiene dos conjuntos de datos fisiológicos obtenidos durante un experimento denominado `Toma_muestras_v2`:

| Archivo | Tamaño aproximado | Contenido |
|---|---:|---|
| `Toma_muestras_v2 Data export.tsv` | 1,37 GiB | Exportación tabular de Tobii Pro Lab con seguimiento ocular (eye tracking), eventos, fijaciones, pupila y respuesta galvánica de la piel (GSR). |
| `eeg_recordings_exp_V2.zip` | 1,55 GiB comprimido; 5,38 GiB sin comprimir | Registros EEG de OpenBCI organizados en sesiones, en formatos OpenBCI TXT y BrainFlow CSV. |

Los archivos parecen corresponder al mismo estudio y período de adquisición (principalmente agosto de 2025), pero no contienen una clave explícita y universal que sincronice automáticamente ambos conjuntos. La unión debe hacerse mediante participante, condición de prueba y marcas temporales.

## 2. Archivo de eye tracking y GSR

### 2.1 Formato

`Toma_muestras_v2 Data export.tsv` es un archivo de texto delimitado por tabulaciones (TSV), con una fila de encabezado y 99 columnas. No debe leerse como CSV separado por comas. El archivo mezcla distintos tipos de filas: muestras del eye tracker, muestras GSR y eventos. Por eso muchas celdas están vacías; una fila solo completa los campos aplicables al sensor o evento que representa.

Ejemplos observados en `Sensor`:

- `Eye Tracker`: muestra de mirada, pupila o movimiento ocular.
- `GSR`: muestra de respuesta galvánica de la piel.
- Vacío: puede representar eventos generales, como `RecordingStart`.

La resolución registrada es 1920 × 1080 píxeles y la latencia de monitor indicada es 10 ms. El filtro de fijaciones observado es `Tobii I-VT (Fixation)`, con versión de software `1.241.54542`.

### 2.2 Identificación y tiempo

Las columnas 1–18 describen la grabación:

- `Recording timestamp`: tiempo relativo dentro de la grabación, aparentemente en microsegundos. Por ejemplo, `50276` corresponde aproximadamente a 50,276 ms desde el comienzo.
- `Computer timestamp`: reloj interno del computador usado para ordenar o sincronizar muestras.
- `Sensor`: origen de la fila.
- `Project name`: nombre del proyecto (`Toma_muestras_v2`).
- `Export date`: fecha en que se produjo la exportación, no la fecha de captura.
- `Participant name` y `Recording name`: identificadores de participante y grabación, por ejemplo `P1`.
- `Recording date` / `Recording date UTC`: fecha local y UTC.
- `Recording start time` / `Recording start time UTC`: hora local y UTC. En la muestra revisada existe una diferencia de cuatro horas, coherente con Chile en UTC−4 para agosto.
- `Recording duration`: duración total, aparentemente en milisegundos; `755225` equivale a unos 12 min 35,225 s.
- `Timeline name`: condición o secuencia experimental; se observó `SlowWeb G1`.
- `Recording Fixation filter name`: algoritmo utilizado para clasificar fijaciones.
- `Recording software version`: versión del programa exportador.
- `Recording resolution height` / `width`: dimensiones del área registrada.
- `Recording monitor latency`: latencia configurada del monitor.

Para análisis temporal conviene usar `Recording timestamp` como eje relativo dentro de cada grabación y conservar las fechas/horas absolutas para relacionarlas con EEG. No se deben mezclar directamente `Computer timestamp` y `Eyetracker timestamp` sin verificar sus unidades y origen.

### 2.3 Calibración y validación

Las columnas 19–36 contienen métricas agregadas de calidad:

- exactitud promedio (`accuracy`);
- precisión como desviación estándar (`precision SD`);
- precisión RMS (`precision RMS`);
- cada una expresada en milímetros, grados visuales y píxeles;
- resultados separados para calibración y validación.

En la grabación de ejemplo, la exactitud media de calibración fue 65,2 mm, 5,75° o 261 píxeles; la validación fue 6,7 mm, 0,60° o 27 píxeles. La diferencia es considerable y debe revisarse por participante antes de aceptar los datos. Estas métricas se repiten en muchas filas porque pertenecen a toda la grabación, no a cada muestra individual.

### 2.4 Mirada, pupila y posición ocular

Las columnas 37–72 contienen los datos principales del eye tracker:

- `Eyetracker timestamp`: reloj propio del dispositivo.
- `Event` y `Event value`: eventos discretos y su valor.
- `Gaze point X/Y`: punto de mirada binocular combinado en píxeles.
- `Gaze point left/right X/Y`: puntos de mirada por ojo en píxeles.
- `Gaze direction left/right X/Y/Z`: vectores tridimensionales de dirección de la mirada.
- `Pupil diameter left/right`: diámetro pupilar por ojo.
- `Pupil diameter filtered`: valor combinado o filtrado.
- `Validity left/right`: validez de la detección; se observaron `Valid` e `Invalid`.
- `Eye position ... (DACSmm)`: posición 3D de cada ojo en milímetros dentro del sistema de coordenadas del área de visualización.
- `Gaze point ... (DACSmm)`: punto de mirada por ojo en milímetros.
- `Gaze point ... (MCSnorm)`: coordenadas normalizadas relativas al medio presentado.

`DACS` se refiere al sistema de coordenadas del área de visualización y `MCSnorm` a coordenadas normalizadas del medio. Las coordenadas en píxeles sirven para superponer la mirada sobre una pantalla de tamaño conocido; las normalizadas son preferibles cuando los estímulos tienen tamaños o posiciones diferentes.

### 2.5 Estímulos, movimientos oculares y navegador

Las columnas 73–98 describen el contexto visual:

- nombre del estímulo y medio presentado;
- ancho, alto y posición del medio en píxeles DACS;
- dimensiones originales del medio;
- `Eye movement type`: clasificación como `Fixation`, `Saccade`, `EyesNotFound`, etc.;
- `Gaze event duration` e índice del evento ocular;
- punto de fijación en píxeles y en coordenadas normalizadas;
- posición del área cliente y viewport del navegador;
- ancho y alto del viewport y de la página completa;
- posición X/Y del mouse.

El campo `Ungrouped` parece ser una columna auxiliar generada por la exportación. Debe inspeccionarse antes de descartarlo, pero su nombre no expresa una variable experimental definida.

### 2.6 GSR

La columna 99, `Galvanic skin response (GSR)`, contiene la señal electrodérmica. Solo se completa en filas cuyo sensor es `GSR`; por ejemplo, se observó el valor `1.8882759809494019`. La unidad no aparece declarada en el encabezado, por lo que no debe asumirse formalmente que sea µS sin consultar la configuración del dispositivo o la documentación de adquisición.

### 2.7 Lista exacta de columnas por grupo

| Rango | Grupo |
|---|---|
| 1–18 | Grabación, participante, tiempos, resolución y software |
| 19–27 | Calidad de calibración |
| 28–36 | Calidad de validación |
| 37–39 | Reloj del eye tracker y eventos |
| 40–45 | Puntos de mirada en píxeles |
| 46–51 | Dirección 3D de la mirada |
| 52–56 | Pupila y validez |
| 57–66 | Posición ocular y mirada en DACSmm |
| 67–72 | Mirada normalizada en MCS |
| 73–80 | Estímulo y medio presentado |
| 81–87 | Movimientos oculares y fijaciones |
| 88–98 | Navegador, página y mouse |
| 99 | GSR |

## 3. Archivo comprimido de EEG

### 3.1 Organización

`eeg_recordings_exp_V2.zip` contiene:

- 270 entradas totales;
- 104 directorios de sesión;
- 166 archivos;
- 164 archivos con contenido: 109 `.txt` y 55 `.csv`;
- 2 archivos de longitud cero.

Los directorios siguen nombres como:

- `OpenBCISession_P1`: sesión principal del participante P1;
- `OpenBCISession_P1_test`: sesión de prueba asociada;
- nombres con variantes como espacios, mayúsculas/minúsculas o ausencia de separador (`P29test`);
- sesiones preliminares identificadas solo por fecha/hora;
- pruebas técnicas como `sold_test`, `prueba_soldar` o `TEST`.

La nomenclatura no está totalmente normalizada. No se debe inferir que las 104 carpetas sean 104 participantes: hay múltiples sesiones por participante, pruebas y ensayos técnicos. Los nombres visibles cubren al menos `P1` a `P48`, pero deben validarse contra el protocolo experimental antes de fijar el número final de sujetos válidos.

### 3.2 TXT de OpenBCI

Los archivos `OpenBCI-RAW-....txt` incluyen metadatos al comienzo. En la muestra revisada:

```text
%OpenBCI Raw EXG Data
%Number of channels = 16
%Sample Rate = 125 Hz
%Board = OpenBCI_GUI$BoardCytonSerialDaisy
```

Después aparece una cabecera separada por comas con 33 campos:

- `Sample Index`;
- 16 canales `EXG Channel 0` a `EXG Channel 15`;
- 3 canales de acelerómetro;
- 7 campos genéricos `Other`;
- 3 canales analógicos;
- `Timestamp` Unix;
- otro campo `Other`;
- `Timestamp (Formatted)` legible.

El equipo declarado es una OpenBCI Cyton con Daisy, que proporciona 16 canales EXG, y la frecuencia declarada es 125 Hz. `EXG` es una etiqueta genérica; en este experimento los registros se interpretan como EEG, pero la ubicación y referencia de los electrodos no están documentadas dentro de estos archivos.

Los valores EXG parecen estar expresados en microvoltios según el formato habitual de OpenBCI GUI, pero la unidad debe confirmarse con la configuración original. Valores cercanos a ±187500 sugieren saturación o límite de rango, por lo que se recomienda cuantificar clipping, canales desconectados y artefactos antes de analizar potencia o conectividad.

### 3.3 CSV de BrainFlow

Los archivos `BrainFlow-RAW_...csv` observados:

- están delimitados por tabulaciones, pese a la extensión `.csv`;
- no contienen fila de encabezado;
- poseen 32 valores por muestra;
- almacenan el índice de muestra, 16 canales EXG, acelerómetro, campos auxiliares, analógicos y timestamp numérico;
- no incluyen la última columna de fecha formateada presente en los TXT.

El orden coincide con los primeros 32 campos del TXT asociado y permite usar la cabecera del TXT como referencia estructural. Esta equivalencia debe comprobarse por sesión antes de automatizar la carga, pues algunas carpetas no contienen ambos formatos y existen archivos vacíos.

### 3.4 Relación entre TXT y CSV

TXT y CSV no representan necesariamente dos experimentos diferentes. Parecen ser dos salidas de la misma adquisición: una generada por OpenBCI GUI y otra por BrainFlow. Dependiendo de la sesión puede existir solo un TXT, un TXT más un CSV, o más de un registro. Antes de concatenar datos hay que comparar:

- carpeta de sesión;
- hora inicial incorporada en el nombre;
- timestamps Unix internos;
- duración y número de muestras;
- frecuencia efectiva estimada a partir de timestamps;
- coincidencia de las señales.

No conviene sumar ambos archivos sin esta comprobación, ya que podrían ser copias parciales o representaciones duplicadas de la misma señal.

## 4. Cómo relacionar eye tracking, GSR y EEG

La estrategia más segura es trabajar por participante y grabación:

1. Normalizar los identificadores de carpeta EEG, separando sesiones principales, `test` y pruebas técnicas.
2. En el TSV, agrupar por `Participant name` y `Recording name`.
3. Convertir las fechas y horas locales/UTC del TSV a timestamps absolutos con zona horaria explícita.
4. Convertir el `Timestamp` Unix del EEG a la misma zona o a UTC.
5. Comparar inicios, finales y duración para elegir el EEG correspondiente a cada grabación Tobii.
6. Establecer un eje relativo común desde el inicio real de la tarea o desde un evento compartido, si existe.
7. Verificar desfase y deriva de reloj; una coincidencia de hora inicial no garantiza sincronización a nivel de muestra.
8. Remuestrear solo después de conservar las señales originales y decidir la resolución temporal necesaria.

No se encontró, durante esta inspección estructural, un campo de trigger inequívoco compartido entre ambos sistemas. Por ello, cualquier alineación basada solo en nombres y horas debe marcarse como estimada.

## 5. Recomendaciones de carga y limpieza

- Leer el TSV por bloques (`chunks`) debido a su tamaño; cargarlo completo en memoria puede requerir varios gigabytes adicionales.
- Especificar separador tabulación y conservar inicialmente todas las columnas como texto para detectar formatos inconsistentes.
- Tratar cadenas vacías como datos ausentes, sin confundirlas con cero.
- Separar las filas por `Sensor` antes de procesar eye tracking y GSR.
- Aplicar `Validity left/right` al calcular métricas de mirada o pupila.
- Revisar la calidad de calibración y validación por grabación.
- No interpolar pérdidas largas marcadas como `EyesNotFound`.
- En EEG, ignorar las líneas iniciales que comienzan por `%` al cargar el TXT, pero conservarlas como metadatos.
- Detectar automáticamente el delimitador: coma en OpenBCI TXT y tabulación en BrainFlow CSV.
- Registrar y excluir explícitamente los dos archivos vacíos.
- Conservar una tabla maestra de sesiones con participante, condición, archivo, inicio, fin, muestras, frecuencia y estado de calidad.
- No descomprimir todo el ZIP si el espacio disponible es limitado: su contenido expande a unos 5,38 GiB.

## 6. Limitaciones de esta descripción

Esta documentación se basa en la estructura, encabezados, metadatos y muestras representativas de los archivos. No se realizó una auditoría estadística exhaustiva de los aproximadamente 6,8 GiB combinados ni se verificó el protocolo experimental, el montaje de electrodos, las unidades configuradas para GSR/EXG o la correspondencia definitiva entre cada sesión EEG y cada grabación Tobii. Esos elementos deben recuperarse del protocolo o del equipo de adquisición antes de realizar inferencias científicas.
