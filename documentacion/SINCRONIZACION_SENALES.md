# Coordinación y sincronización de señales MDS

## Objetivo

El programa `sincronizar_senales.py` coordina las grabaciones existentes de EEG OpenBCI con las señales Tobii (eye tracking, pupila y GSR). Está basado en `Sincronizacion señales.ipynb`, pero transforma la parte de sincronización en un proceso ejecutable, auditable y conservador.

El programa no modifica ni descomprime los originales. Produce inventarios y una tabla de candidatos de emparejado. Esto es deliberado: los datos no contienen triggers compartidos por hardware, por lo que la alineación absoluta puede estimarse con los relojes del sistema, pero el drift entre dispositivos no puede calcularse de manera válida a partir de eventos que solo existen en Tobii.

## Ejecución

Desde PowerShell, dentro de `MDS`:

```powershell
python .\sincronizar_senales.py
```

Se requiere Python 3.10 o posterior. En el equipo inspeccionado, el comando
`python` actualmente apunta al alias de Microsoft Store y no a una instalación
funcional; habrá que instalar/activar Python antes de ejecutar el programa.

Opcionalmente:

```powershell
python .\sincronizar_senales.py --max-offset-s 180 --output-dir sincronizacion_output
```

Solo utiliza la biblioteca estándar de Python. La lectura del TSV se realiza por streaming para no cargar 1,37 GiB en memoria.

## Archivos generados

Dentro de `sincronizacion_output`:

| Archivo | Propósito |
|---|---|
| `coordinacion_sesiones.csv` | Relación propuesta Tobii ↔ EEG, offset y estado de revisión. |
| `inventario_tobii.csv` | Una fila por grabación única detectada en el TSV. |
| `inventario_eeg.csv` | Una fila por sesión EEG legible dentro del ZIP. |
| `diagnosticos.json` | Archivos vacíos o entradas que no pudieron interpretarse. |

## Dominio temporal común

Para Tobii se usan directamente `Recording date UTC` y `Recording start time UTC`. `Recording timestamp` es un desplazamiento relativo en microsegundos:

```text
t_tobii(i) = inicio_tobii_utc + Recording timestamp(i) × 10⁻⁶ s
```

Para OpenBCI TXT se usa `Timestamp (Formatted)`. Como las sesiones fueron adquiridas en Chile durante agosto de 2025, el script interpreta esa hora local como UTC−4 y la convierte a UTC. Para BrainFlow se usa la columna Unix (posición 31, índice 30), que ya define un instante absoluto UTC.

El offset reportado es:

```text
offset = inicio_tobii_utc − inicio_eeg_utc
```

Un offset positivo significa que EEG comenzó antes. Esto es esperable si el operador activó OpenBCI antes de iniciar Tobii.

## Regla de emparejado

Para cada grabación Tobii:

1. Se normaliza el participante (`P01`, `p1` y `P1` pasan a `P1`).
2. Se restringen candidatos EEG al mismo participante cuando existen.
3. Se elige el inicio temporal más cercano.
4. Se etiqueta el resultado para revisión.

Estados posibles:

- `candidato`: mismo participante, sesión principal y offset dentro del umbral.
- `revisar_offset`: mismo participante, pero separación superior a `--max-offset-s`.
- `revisar_tipo_sesion`: el candidato parece ser `test`, `sold` o `prueba`.
- `revisar_participante`: no se encontró EEG con el mismo identificador y se propuso el más cercano global.
- `sin_candidato`: no existe ninguna sesión EEG legible.

La tabla es una propuesta, no una confirmación experimental. Debe revisarse antes de extraer epochs.

## Drift: corrección importante al notebook

El notebook propone calcular drift tomando el primer y último evento Tobii y buscando las muestras EEG temporalmente más cercanas. Ese procedimiento no dispone de observaciones del mismo evento en EEG: al elegir el vecino más cercano se reutiliza el reloj absoluto que se intenta validar. El resultado tenderá mecánicamente a 1 y no identifica el drift físico de los osciladores.

Por esa razón, `drift_scale` se fija en `1.0`. Una corrección afín solo debe activarse si se obtienen al menos dos pares de anclajes observados independientemente en ambos sistemas, por ejemplo pulsos TTL, marcas LSL o artefactos deliberados identificables en EEG y Tobii:

```text
escala = (tobii_anchor_2 − tobii_anchor_1) / (eeg_anchor_2 − eeg_anchor_1)
t_eeg_corregido = tobii_anchor_1 + (t_eeg − eeg_anchor_1) × escala
```

Con un solo anclaje solo puede estimarse offset, no drift. Sin ningún trigger compartido, la precisión queda limitada por los relojes del sistema, su configuración y la latencia de software.

## Coordinación de las modalidades

GSR, pupila y eye tracking provienen del mismo TSV Tobii y comparten `Recording timestamp`; por tanto, deben mantenerse en el mismo eje Tobii. EEG conserva 125 Hz y Tobii su frecuencia nativa/objetivo (por ejemplo, 60 Hz). No es necesario igualar frecuencias para sincronizar: los epochs se recortan usando límites de tiempo comunes.

Para una fila aprobada de `coordinacion_sesiones.csv`:

1. Reconstruir cada timestamp Tobii con el inicio UTC y el tiempo relativo.
2. Convertir los timestamps EEG a UTC.
3. Seleccionar la ventana de solapamiento:

```text
inicio_común = max(inicio_eeg, inicio_tobii)
fin_común    = min(fin_eeg, fin_tobii)
```

4. Extraer EEG y señales Tobii por los mismos límites absolutos.
5. Conservar los arrays a sus frecuencias nativas y guardar el tiempo relativo al evento o al inicio común.

## Controles de calidad obligatorios

- Confirmar manualmente cada fila cuyo estado no sea `candidato`.
- Comprobar que la sesión EEG cubra la duración Tobii, no solo que sus inicios sean cercanos.
- Revisar nombres irregulares (`P29test`, espacios y sesiones técnicas).
- Excluir los archivos vacíos informados en `diagnosticos.json`.
- Comprobar monotonicidad y saltos de timestamps en ambas modalidades.
- Estimar la frecuencia EEG efectiva a partir de timestamps, además de leer los 125 Hz declarados.
- No interpretar `drift_scale = 1.0` como prueba de ausencia de drift; significa “sin corrección identificable”.
- Mantener fechas en UTC internamente y convertir a hora de Chile solo para visualización.

## Alcance

Este programa resuelve el inventario y la coordinación inicial de sesiones con evidencia disponible en los archivos. Para una sincronización submuestra científicamente defendible se requieren triggers compartidos o una señal de anclaje observable en ambos dispositivos. Sin ellos, la tabla permite una alineación por reloj absoluto y deja explícita su incertidumbre.
