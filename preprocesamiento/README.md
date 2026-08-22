# Preprocesamiento Tobii — GSR, pupilometría y eye tracking

Lleva las tres señales del Tobii Pro desde el export crudo hasta una tabla de
features en **ventanas de 2 s con 50 % de solapamiento**, el mismo soporte que
ya tienen las épocas del EEG en `EDA/epochs_output/epochs_features.parquet`.

Continúa el diseño de `Sincronizacion_señales.ipynb` (secciones 1.2, 3.1 a 3.5)
y agrega lo que faltaba: la extracción de features por ventana. Sin ese paso
las señales quedaban limpias pero no comparables con el EEG.

## Estado

**El pipeline no ha tocado los datos reales.** El export de Tobii vive en Drive
y no está en esta máquina. Lo que sí está verificado es la mecánica: la prueba
`test_sintetico.py` fabrica un export con propiedades conocidas (picos SCR,
parpadeos, fijaciones y sacadas inyectados) y comprueba que el pipeline los
recupera.

Dos cosas quedan por confirmar contra el archivo real:

1. **Los nombres de columna.** `columnas.py` declara candidatos por campo y los
   resuelve contra el archivo. Si falta una columna obligatoria, el pipeline
   falla de inmediato y lista lo que encontró. Si un nombre real no está entre
   los candidatos, se agrega ahí.
2. **El formato de fecha.** Se asume `mm/dd/yyyy`, como dice el diseño previo.
   La reconstrucción valida que el año resultante sea plausible.

## Uso

```bash
cd preprocesamiento

# Verificar que todo corre, sin datos reales
python test_sintetico.py

# Corrida completa desde el export
python procesar_tobii.py \
    --tsv "../datos/Toma_muestras_v2 Data export.tsv" \
    --salida ../resultados/tobii

# Un participante, para inspeccionar antes de correr los 48
python procesar_tobii.py --parquets ../resultados/tobii/interim \
    --salida /tmp/prueba --participante P01
```

Opciones que importan:

| Opción | Para qué |
|---|---|
| `--tipos` | Tipos de segmento a procesar. Por defecto `exposicion_imagen`, la entrada de entrenamiento. `todos` no filtra. |
| `--contexto-gsr` | Ventana de contexto de la SCR, en segundos. Por defecto 6. |
| `--metodo-eda` | `butter` (por defecto) o `cvxeda` si está instalado cvxopt. |

## Salida

`resultados/tobii/features_tobii.parquet`, una fila por ventana:

```
participante, segmento_id, estimulo, tipo, idx_ventana, inicio, fin, inicio_s
gsr_*  (10 + 4 de contexto)
pup_*  (8)
et_*   (13)
```

`inicio` y `fin` son timestamps absolutos UTC. La unión con la tabla del EEG
**no la hace este módulo**: requiere los manifiestos de sincronización y la
corrección de deriva, que son una decisión aparte.

## Features

**GSR** — `gsr_scl_media`, `gsr_scl_pendiente`, `gsr_scl_z`, `gsr_std`,
`gsr_rango`, `gsr_scr_n_picos`, `gsr_scr_amp_media`, `gsr_scr_amp_max`,
`gsr_scr_auc`, `gsr_pct_valido`, más las cuatro de SCR sobre la ventana de
contexto (`_ctx6s`).

**Pupilometría** — `pup_media`, `pup_std`, `pup_pendiente`, `pup_z_media`,
`pup_dilatacion_rel`, `pup_min`, `pup_max`, `pup_pct_valido`.

**Eye tracking** — `et_n_fijaciones`, `et_fij_dur_media`, `et_fij_dur_total`,
`et_pct_tiempo_fijando`, `et_n_sacadas`, `et_sac_dur_media`, `et_sac_amp_media`,
`et_sac_amp_max`, `et_sac_vel_pico`, `et_disp_x`, `et_disp_y`, `et_disp_rms`,
`et_disp_bbox`.

## Decisiones que el módulo NO cierra

**La ventana de agregación del GSR.** La latencia de una SCR va de 1 a 5 s y la
ventana del diseño es de 2 s, de modo que una respuesta puede caer varias
ventanas después del estímulo que la causó. El módulo emite las features de SCR
sobre los dos soportes —la ventana de 2 s y una ventana de contexto de 6 s que
termina en el mismo instante— para poder comparar cuál predice mejor. Elegir es
decisión del profesor guía.

**La corrección por luminancia de la pupila.** `pupila.corregir_luminancia`
está declarada y lanza `NotImplementedError` a propósito. Requiere la
luminancia de la página observada por instante, que a su vez exige conservar
las capturas de los estímulos. Mientras no exista, el diámetro pupilar mezcla
carga cognitiva y reflejo fotomotor, y así está declarado en las limitaciones
del Capítulo 1.

**La descomposición tónico/fásica por defecto es un pasa-bajos Butterworth de
0,05 Hz**, no cvxEDA. El diseño original prefiere cvxEDA porque impone la
no-negatividad de los impulsos sudomotores, pero `cvxopt` no está instalado.
`--metodo-eda cvxeda` lo usa si se instala.

## Notas de implementación

- El orden es rechazo de artefactos, resampleo, descomposición y recién ahí
  normalización. El z-score va último porque centra en cero e introduce valores
  negativos, que rompen el supuesto de la descomposición.
- El eye tracking **no** se resamplea a 60 Hz. Sus unidades son eventos con
  duración propia, y promediarlos sobre una grilla uniforme destruiría la
  información de conteo y duración que alimenta el Attention Score.
- Un evento se asigna a una ventana por su instante de inicio. Una fijación que
  empieza al final de una ventana cuenta completa ahí y no se prorratea.
- Una ventana nunca cruza el borde de un estímulo: mezclaría dos condiciones
  experimentales dentro de la misma etiqueta.
- La grilla no emite ventanas truncadas. Una ventana más corta tendría menos
  muestras y sesgaría las features de conteo.
- El z-score de GSR y pupila se estima sobre la sesión completa del
  participante. Con partición por participante eso no filtra información entre
  entrenamiento y evaluación, porque un participante entra entero a un lado u
  otro. Sí es **no causal dentro de la sesión**, lo que es consistente con el
  alcance declarado (modelos evaluados offline, sin sistema en tiempo real).

## Archivos

| Archivo | Qué hace |
|---|---|
| `columnas.py` | Resuelve los nombres de columna del export contra candidatos |
| `tobii_io.py` | Separa por participante, reconstruye timestamps, grilla de 60 Hz, segmentos de estímulo |
| `ventanas.py` | Grilla de ventanas de 2 s / 50 %, compartida por las tres señales |
| `gsr.py` | Artefactos, descomposición SCL/SCR, features |
| `pupila.py` | Parpadeos, interpolación cúbica, features |
| `eye_tracking.py` | Eventos I-VT a fijaciones y sacadas, features |
| `procesar_tobii.py` | Runner CLI |
| `test_sintetico.py` | Prueba de extremo a extremo con datos fabricados |

## Dependencias

`pandas`, `numpy`, `scipy`, `pyarrow`. Opcional: `cvxopt` + `cvxEDA`.
