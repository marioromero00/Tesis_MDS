---
tipo: referencia
fuente: Tesis MDS junio 2026.pdf — 20 láminas, presentación de avances
fecha_presentacion: 06-2026
fecha_incorporacion: 08-08-2026
---

# Conocimiento de presentaciones pasadas

Consolidado de lo presentado en avances anteriores, para no volver a levantarlo y para tener
trazabilidad de qué cambió. Fuente única hasta ahora: `Tesis MDS junio 2026.pdf`.

> Buena parte de este contenido **no estaba en ninguna nota del vault** — en particular los
> números del EDA, los parámetros del pipeline EEG y la revisión de literatura.

---

## ⚠️ Contradicciones detectadas (revisar antes del 10-08)

### 1. Frecuencia de muestreo del EEG — RESUELTO 22-08-2026: son **125 Hz**

**Verificado contra los datos crudos**
(`~/tesis/Tesis_MDS/EDA/Datos EEG/P*.txt`). Tres evidencias
independientes coinciden:

| Evidencia | Resultado |
|---|---|
| Cabecera del archivo OpenBCI | `%Sample Rate = 125 Hz` |
| Frecuencia efectiva medida sobre los timestamps (6 participantes) | 125,07 – 125,16 Hz |
| Código de epoching real (`EDA/epoching.ipynb`) | `EPOCH_SAMPLES = 250 # 2 s`, paso 125 |

**Causa de la confusión:** la placa es `OpenBCI_GUI$BoardCytonSerialDaisy`, es decir **Cyton +
módulo Daisy**. El Cyton solo muestrea a 250 Hz con 8 canales; al agregar la Daisy para llegar a
16 canales, el muestreo por canal cae a la mitad — 125 Hz. El `Sample Index` de los archivos
avanza de 2 en 2 (0, 2, 4, …) por el entrelazado de la Daisy, y eso es probablemente lo que se
leyó como 250 Hz.

**Consecuencias:**
- La lámina de junio (250 Hz) está **equivocada**, y con ella el tensor `× 500 muestras`: la
  ventana de 2 s son **250 muestras**, no 500, tal como está implementado en el código.
- La "corrección" del 08-08-2026 en [[presentacion 10-08-26]] invirtió el error y quedó revertida.
- Los 273 features por época no cambian: dependen del número de bandas e índices, no de la
  frecuencia.
- Sí cambia el techo de banda útil: con 125 Hz el Nyquist es 62,5 Hz, de modo que el pasa-bajos
  en 40 Hz y la banda gamma hasta 40 Hz siguen siendo válidos, pero **no se puede extender gamma
  por sobre ~60 Hz** en este dataset.

### 2. La expresión facial seguía viva en junio

En junio el diseño **incluía expresión facial**: FaceReader, embeddings faciales, y el "Enfoque 2"
de construcción de etiqueta era precisamente un clasificador facial como modelo profesor. El
aporte declarado era "modelos secuenciales EEG+GSR+Eye+**Facial**".

Ese es el cambio central entre junio y agosto, y explica por qué el rediseño existe. Ya está
registrado en [[Tesis_MDS]] > Qué no funcionó.

### 3. El modelo estudiante cambió de señales

- **Junio**, próximos pasos: "Entrenar un modelo que prediga atención usando **solo EEG**".
- **Agosto**: el estudiante de atención es **EEG + GSR**.

No es contradicción, es evolución — pero conviene poder explicar por qué se agregó GSR.

---

## Dataset — EDA de la Toma de Muestra 2 (EEG raw)

| Dato | Valor |
|---|---|
| Participantes registrados | **48** |
| Canales EEG por participante | 16 |
| Duración promedio de grabación | 13,4 ± 1,5 min |
| Duración mediana | 13,1 min |
| Valores faltantes | **NaN = 0** |

- **P25** aparece marcado como `P25_REVISAR` en los gráficos. Queda pendiente saber por qué.
- Rango de duración observado: de ~10,9 min (P23) a ~17,2 min (P29).

### Calidad de señal

- **21 de 48 participantes** presentan al menos un canal saturado.
- **Mediana: 0** canales saturados — más de la mitad de los registros no tiene saturación.
- **Promedio: 1** canal saturado por participante, concentrado en un grupo reducido.
- Peor caso observado: **7 canales** al 100% saturados en un participante (P17).
- Se identificó un **pico de potencia cercano a 50 Hz**, atribuible a la red eléctrica → de ahí
  el filtro notch.

Canales presentes en el mapa de saturación: Fp1, Fp2, C3, C4, P7, P8, O1, O2, F7, F8, F3, F4,
T7, T8, P3, P4.

---

## Pipeline de preprocesamiento EEG (definido en junio)

### Adquisición
OpenBCI Cyton + Daisy · 16 canales · **125 Hz** · 24-bit ADC.
*(Junio declaró 250 Hz; corregido el 22-08-2026 contra los datos crudos — ver Contradicciones § 1.)*
Conversión hex → µV con **Vref = 4,5 V** y **Gain = 24**: `V = ADC × Vref / (Gain × 2²³)`.
Se detectan canales desconectados en la lectura.

### Filtrado — Butterworth orden 4, fase cero (`filtfilt`)
| Filtro | Corte | Para qué |
|---|---|---|
| Pasa-altos | 1 Hz | elimina drift DC |
| Pasa-bajos | 40 Hz | elimina EMG |
| Notch | 50 Hz | interferencia de red eléctrica |

### Rechazo de artefactos y calidad
- Muestras con `|amplitud| > 150 µV` → NaN.
- Canales clasificados en **bueno / plano / ruidoso**. Solo los buenos entran al modelamiento.

### Segmentación
- Ventana **2 s**, **50% de solapamiento**.
- Época con **>20% de NaN → se descarta**.
- Tensor resultante: `N_épocas × N_canales × 250 muestras`.
  *(Junio declaró 500; a 125 Hz una ventana de 2 s son 250 muestras. Corregido el 22-08-2026.)*

### Features espectrales — método de Welch (PSD)

| Banda | Nombre | Rango | Potencia |
|---|---|---|---|
| δ | Delta | 0,5–4 Hz | absoluta y relativa |
| θ | Theta | 4–8 Hz | absoluta y relativa |
| α | Alpha | 8–13 Hz | absoluta y relativa |
| β | Beta | 13–30 Hz | absoluta y relativa |
| γ | Gamma | 30–40 Hz | absoluta y relativa |

### Los 7 índices inter-banda

| Índice | Fórmula |
|---|---|
| Carga cognitiva | θ / α |
| Déficit atencional | θ / β |
| Relajación | α / β |
| Engagement | β / (α + θ) |
| Fatiga mental | (α + θ) / β |
| Ondas lentas | (δ + θ) / (α + β) |
| Alto nivel cognitivo | γ / (δ + θ) |

Más **asimetría hemisférica alpha**: `ln(α_derecha) − ln(α_izquierda)` → se interpretó como
proxy de **valencia emocional**.

> Nota relevante para el diseño actual: en junio la asimetría alpha figuraba como proxy de
> valencia. Hoy [[Etiqueta Emocion]] descarta la valencia porque obtenerla desde EEG sería
> circular (el EEG es input del estudiante). **La asimetría alpha sigue siendo una feature de
> entrada, no una fuente de etiqueta.** Vale la pena tenerlo claro si el profesor pregunta por
> qué no se usa para valencia.

### Vector de features por época
**160 potencias + 112 índices + 1 asimetría = 273 features**
(5 bandas × 2 tipos × 16 canales = 160 · 7 índices × 16 canales = 112)

---

## Features definidas por modalidad (lámina 13)

| Modalidad | Features |
|---|---|
| **Eye-tracking** | número de fijaciones · duración promedio de fijaciones · amplitud y velocidad de sacadas · dispersión de la mirada · diámetro pupilar promedio |
| **GSR** | número de picos (SCR) · amplitud de respuesta · nivel tónico (SCL) · variabilidad de la señal |
| **EEG** | potencia por bandas · relaciones entre bandas |
| **Expresión facial** *(ya no disponible)* | embeddings faciales · probabilidades de emoción (FaceReader) |

En junio la pupilometría figuraba **dentro de eye-tracking**, no como modalidad separada. El
diseño de agosto la trata como fuente propia, con su propia dimensión (cognitiva).

---

## Los tres enfoques de construcción de etiqueta (lámina 18)

Se planteó usar una fuente como **pseudo ground truth**, con tres enfoques:

1. **Enfoque 1 — Eye Tracking:** índice de atención por reglas fisiológicas (duración de
   fijaciones, número de fijaciones, mirada dentro de áreas de interés, pérdida de mirada,
   dilatación pupilar).
2. **Enfoque 2 — Expresión facial:** clasificador facial que entrega la etiqueta, y otro modelo
   aprende de esas etiquetas. Se cita como referencia el trabajo de **Subiabre**.
3. **Enfoque 3 — Estimación multimodal:** Attention Score a partir de N señales, discretizado
   por persona.

**El diseño actual es el Enfoque 3**, con el Enfoque 2 descartado por falta de señal facial.

Limitación declarada ya en junio, y que sigue vigente:
> El modelo nunca podrá ser mejor que las etiquetas que recibe.

---

## Revisión de literatura presentada

### Panorama multimodal

| Trabajo | Señales | Arquitectura | Aporte |
|---|---|---|---|
| **TACOformer** (2023) | EEG + GSR + ECG | Cross-Attention Transformer | Atención conjunta token–canal; SOTA en DEAP y DREAMER |
| **Feng et al.** (2025) | EEG + Facial | Multi-Head Self-Attention | Fusión adaptativa EEG–Facial (81,1% en MED-HI) |
| **Milmer** (2025) | EEG + Facial | Swin Transformer + Cross-Attention | Modelado temporal sobre secuencias faciales (96,7% en DEAP) |
| **Wang et al.** (2025) | EEG + Eye-Tracking | Cross-Modal Attention | Alineación actividad cerebral–movimiento ocular (90,6% en SEED-IV) |
| **MuMTAffect** (2025) | Gaze + Pupila + AU + GSR | Transformers por modalidad | Aprendizaje multitarea para emoción y personalidad |
| **GBV-Net** (2025) | EEG + GSR + ECG + Facial | Fusión jerárquica con compuertas | Integración profunda de señales visuales y fisiológicas |

### Sobre fusión
> La ganancia multimodal depende de la **arquitectura** de fusión, no solo de agregar modalidades.

- **Zali-Vargahan et al. (2023):** 95,3% con fusión CNN+Stockwell (EEG+fisio+facial).
- **Saavedra (2024):** **sin mejora significativa** con fusión tardía EEG+GSR en contexto web.

El dato de Saavedra es el más directamente relevante: es el mismo contexto (web) y las mismas
señales que usa el modelo estudiante de atención. Sostiene la decisión de comparar los tres
tipos de fusión en vez de asumir la tardía.

### Referencias por arquitectura temporal
- **LSTM:** Saffie (2023) — EEG web.
- **TCN:** Bai et al. (2018); Kamrud et al. (2021) — EEG; Elmadjian et al. (2022) — eye-tracking.
- **Transformer:** Vaswani et al. (2017); MNT (2022) — EEG+PPG+GSR; TEREE (2025) — EEG+eye-tracking.

---

## Brechas y aporte, según se declaró en junio

**Brechas en la literatura**
1. Señales tratadas como vectores estáticos, sin dinámica temporal.
2. Fusión de 4 señales en contexto web: inexistente.
3. Fatiga y habituación no modeladas como variable de interés.
4. Sin *ablation studies* sistemáticos.

**Aporte declarado**
- Modelos secuenciales EEG+GSR+Eye+Facial *(la parte facial ya no aplica)*.
- Comparación early / intermediate / late fusion.
- Detección de fatiga y habituación (H2).
- Ablation study por modalidad y temporalidad.
- Baseline estático como control.

> El **ablation study** aparece en junio como aporte comprometido y **no está en el punteo de
> agosto ni en [[Resumen Diseño Etiquetas y Modelos]]**. Conviene decidir si sigue en el alcance.

---

## Marco conceptual (lámina 4)

1. **Comportamiento del usuario como fenómeno dinámico** — atención y respuestas emocionales
   varían continuamente durante la interacción; su análisis requiere considerar la evolución
   temporal.
2. **Naturaleza multimodal de los estados cognitivos y emocionales** — el estado se manifiesta
   en múltiples canales fisiológicos y conductuales, cada uno con información complementaria.
3. **Fusión multimodal** — la integración da una representación más completa; la literatura
   distingue fusión temprana, intermedia y tardía.
4. **Modelamiento temporal** — captura dependencias entre observaciones consecutivas y facilita
   identificar habituación, fatiga y transiciones entre estados.

### Modelos de emoción presentados
- **Discreto (Ekman):** 6 emociones básicas, reconocibles transculturalmente vía FACS.
- **Dimensional (Russell):** valencia–arousal.

El diseño actual se queda con **la dimensión arousal del modelo de Russell**, sin valencia.

---

## Erratas menores del PDF de junio
- Lámina 17: "cada **venta**" → debería decir "cada ventana".
- Lámina 18: "Definicion Nivel de **Anteción**" → "Atención".
- Las láminas usan el marcador `XX.` en vez de numeración de sección.

## Notas relacionadas
- [[presentacion 10-08-26]]
- [[Tesis_MDS]]
- [[Etiqueta Atencion]]
- [[Etiqueta Emocion]]
- [[Modelo Profesor - Decisiones]]
- [[Estructura Tesis]]
