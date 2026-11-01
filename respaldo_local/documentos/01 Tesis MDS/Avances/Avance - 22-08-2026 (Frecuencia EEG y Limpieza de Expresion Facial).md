# Avance - 22-08-2026 (Frecuencia EEG y Limpieza de Expresión Facial)

## Trabajo realizado

### 1. Frecuencia de muestreo del EEG: resuelta en 125 Hz

La contradicción abierta desde el 08-08-2026 ([[Conocimiento Presentaciones Pasadas]] § 1) queda
cerrada **con verificación directa sobre los datos crudos**, no por argumento.

| Evidencia | Fuente | Resultado |
|---|---|---|
| Cabecera del archivo OpenBCI | `~/Tesis_MDS/EDA/Datos EEG/P01.txt` | `%Sample Rate = 125 Hz` |
| Frecuencia efectiva medida sobre timestamps | P01–P06, cálculo filas/duración | 125,07 – 125,16 Hz |
| Código de epoching en uso | `EDA/epoching.ipynb` | `EPOCH_SAMPLES = 250 # 2 s`, paso 125 |

**Causa de la confusión.** La placa declarada en la cabecera es
`OpenBCI_GUI$BoardCytonSerialDaisy`: Cyton **más módulo Daisy**. El Cyton solo alcanza 250 Hz con
8 canales; al agregar la Daisy para llegar a 16, el muestreo por canal cae a la mitad. Además el
`Sample Index` de los archivos avanza de 2 en 2 por el entrelazado de la Daisy, y esa es
probablemente la lectura que originó el "250 Hz".

**La presentación de junio 2026 está equivocada** en este punto, y con ella el tensor declarado
`N_épocas × N_canales × 500 muestras`: a 125 Hz una ventana de 2 s son **250 muestras**, que es
justamente lo que el código implementa. La "corrección" del 08-08-2026, que había invertido el
error, queda revertida.

**Lo que no cambia:** los 273 features por época dependen del número de bandas e índices, no de
la frecuencia. **Lo que sí:** el Nyquist es 62,5 Hz, de modo que el pasa-bajos en 40 Hz y la banda
gamma hasta 40 Hz siguen siendo válidos, pero **gamma no se puede extender por sobre ~60 Hz** en
este dataset.

Notas corregidas: [[Conocimiento Presentaciones Pasadas]], [[presentacion 10-08-26]],
`presentacion-10-08-26.html` y [[Estructura Tesis]] (Cap. 4, Adquisición y Segmentación).

### 2. Expresión facial eliminada del borrador

El pendiente del 17-08 anotaba dos menciones por corregir; en la revisión resultaron **siete**
lugares donde el diseño descartado seguía escrito como vigente en [[Estructura Tesis]]:

| Ubicación | Qué decía | Qué dice ahora |
|---|---|---|
| Cap. 1, Descripción Proyecto | "esta investigación tendrá foco en … expresiones faciales" | Las cuatro señales de la Toma de Muestra 2, con la exclusión declarada |
| Cap. 3, Modelos profesores | El clasificador facial como el enfoque | Se describe como trabajo previo del grupo y se explicita que esta tesis no lo usa |
| Cap. 3, Brecha 2 | "Fusión de 4 señales (EEG+GSR+Eye+Facial)" | La combinación real, **marcada para re-verificar** la búsqueda bibliográfica |
| Cap. 3, Aporte | "Modelos secuenciales EEG+GSR+Eye+Facial" | EEG + GSR + eye tracking + pupilometría |
| Cap. 4, Fuentes de Información | Subsección "Expresión Facial" (embeddings, FaceReader) | Sustituida por "Pupilometría"; el diámetro pupilar se movió allí desde Eye Tracking |
| Cap. 4, Definición Nivel de Atención | Tres enfoques, "Decisión: pendiente" | Enfoque 2 marcado como descartado con su razón; decisión del 08-08-2026 registrada |
| Cap. 4, Preprocesamiento | "Preprocesamiento Expresión Facial *(pendiente)*" | "Preprocesamiento Pupilometría *(pendiente)*" |

Se conservan las menciones legítimas: la descripción del proyecto Fondecyt (que sí incluye la
señal), los papers de la tabla del Estado del Arte, y los enunciados de exclusión.

### 3. Índice actualizado

[[Tesis_MDS]] declaraba como objetivo "predecir niveles de atención usando señales EEG", que
quedó corto frente al objetivo general escrito el 17-08. Se alineó con [[Estructura Tesis]] y se
reescribieron los próximos pasos, que seguían apuntando a tareas ya hechas.

## Decisiones tomadas

- **El EEG se registró a 125 Hz.** Verificado, no supuesto. Cualquier nota o lámina que diga
  250 Hz está equivocada.
- La pupilometría pasa a ser una fuente de información propia en el Cap. 4, separada del eye
  tracking, en línea con el cuadro de [[Resumen Diseño Etiquetas y Modelos]].

## Pendientes que esto deja

- [ ] **Re-verificar la brecha 2** del Estado del Arte: la afirmación "inexistente en la
  literatura" se formuló para la combinación con expresión facial. No se puede sostener en la
  defensa sin rehacer la búsqueda para EEG + GSR + eye tracking + pupilometría.
- [ ] Revisar si la presentación de junio 2026 se usó como fuente de algún otro dato derivado de
  los 250 Hz.
- [ ] Los pendientes del 17-08 siguen abiertos: score continuo, referencias de 2.1 sin verificar,
  Statista 2026, *view independence*, y la confirmación de *arousal* con el profesor guía.

## Notas relacionadas

- [[Estructura Tesis]]
- [[Conocimiento Presentaciones Pasadas]]
- [[Resumen Diseño Etiquetas y Modelos]]
- [[Avance - 17-08-2026 (Capitulo 1 y Marco Teorico 2.1)]]
- [[Tesis_MDS]]
