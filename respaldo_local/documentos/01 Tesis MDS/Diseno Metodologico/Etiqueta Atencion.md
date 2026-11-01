# Etiqueta Atención — Metodología

> [!warning] Actualización 22-08-2026
> Primera implementación ejecutada: fusión igualitaria primaria y PCA de sensibilidad.
> La concordancia fue baja (Spearman ρ=0,454), por lo que la etiqueta sigue siendo provisional.
> Véase [[Avance - 22-08-2026 (Etiquetas Particion y Baselines)]].

Documento de trabajo para la construcción de la variable objetivo "atención" del modelo EEG. Complementa [[Atencion]] (alternativas y marco conceptual) y se alinea con el preprocesamiento definido en [[Estructura Tesis]].

**Nota de alcance:** trabajo con la **Toma de Muestra 2**, que contiene 4 señales: **EEG, GSR, Pupilometría y Eye Tracking**. No hay señal de expresión facial (esa señal existe en la Toma de Muestra 1, usada por otras tesis del grupo, pero no en mis datos). Esto reemplaza el rol que originalmente se pensaba para "modelo facial" por **Pupilometría**.

## Objetivo
Construir una pseudoetiqueta de nivel de atención por ventana temporal, que sirva como variable objetivo para entrenar y evaluar el modelo EEG, siguiendo el **Enfoque 3: Estimación Multimodal** de [[Atencion]] (adaptado a las señales disponibles).

## Por qué multimodal y no solo Eye Tracking
Según el marco conceptual del profesor ([[Atencion]]), el eye tracking por sí solo mide el nivel **Observado** (dónde mira el usuario), pero no garantiza que hubo procesamiento cognitivo (**Atendido**) ni comprensión (**Comprendido**). Usar solo fijaciones como etiqueta arriesga confundir "mirar" con "atender". Por eso se combina Eye Tracking (dimensión espacial y temporal) con **Pupilometría** (proxy de dimensión cognitiva/carga atencional — la dilatación pupilar como *task-evoked pupillary response* es un marcador clásico de carga cognitiva en psicofisiología).

## Arquitectura de dos etapas: Modelo Profesor → Modelo Estudiante
Este diseño generaliza el "modelo profesor" (originalmente pensado como un clasificador facial, Enfoque 2 de [[Atencion]]) a **cualquier combinación de señales que no sea la que el modelo final usará como input**.

- **Etapa 1 — Modelo Profesor (esta etiqueta):** Eye Tracking + Pupilometría → Attention Score. No es el objeto de evaluación de la tesis; es infraestructura para tener variable objetivo. Por eso puede (y debe) ser simple/basado en reglas o umbrales — no hay ground truth contra el cual entrenar un profesor más sofisticado. Su justificación viene de la literatura psicofisiológica, no de desempeño predictivo propio.
- **Etapa 2 — Modelo Estudiante (lo que se evalúa en la tesis):** **EEG + GSR** → predice el Attention Score del profesor. Sobre este modelo se contrasta la **hipótesis central** (estático vs. temporal y tipo de fusión: temprana/intermedia/tardía). La trayectoria temporal puede estudiarse como análisis complementario de fatiga/habituación, no como una segunda hipótesis.

Ver [[Resumen Diseño Etiquetas y Modelos]] para el cuadro comparativo con el diseño de emoción.

## Supuestos
1. **Aditividad de evidencia:** combinar Eye Tracking + Pupilometría aproxima mejor el estado atencional real que cualquiera de las dos señales por separado (no lo reemplaza ni lo mide directamente).
2. **Proxy cognitivo:** la dilatación pupilar es un indicador razonable —aunque imperfecto— de la dimensión cognitiva de la atención (carga/esfuerzo cognitivo). Es una limitación conocida (ver Riesgos): pupila también responde a luz, no solo a cognición.
3. **Dimensión intencional controlada:** todos los participantes navegan el mismo estímulo bajo la misma tarea, por lo que la dimensión intencional se asume constante dentro de cada sesión y no se mide por separado.
4. **Granularidad temporal suficiente:** la ventana de 2 s con 50% de solapamiento (definida para el preprocesamiento EEG) es adecuada para capturar fluctuaciones de atención relevantes.
5. **Estacionariedad dentro de la ventana:** se asume que el nivel de atención no cambia drásticamente dentro de una misma ventana de 2 s.
6. **La pseudoetiqueta no es verdad absoluta:** se trata explícitamente como una aproximación ruidosa, no como ground truth (ver [[Atencion]] > Riesgos).

## Fuentes de datos utilizadas
| Señal | Features relevantes para la etiqueta | Dimensión que aporta |
|---|---|---|
| Eye Tracking | Número de fijaciones, duración de fijaciones, mirada dentro de áreas de interés (AOI), dispersión de la mirada | Espacial y temporal |
| Pupilometría | Diámetro pupilar (dilatación) | Cognitiva (proxy de carga atencional) |

*(EEG y GSR no se usan para construir esta etiqueta — quedan reservados como señales de entrada del Modelo Estudiante, evitando fuga de información/circularidad. GSR se reserva además porque construye la etiqueta de **Emoción/Arousal**, ver [[Etiqueta Emocion]].)*

## Alineación temporal
1. Segmentar Eye Tracking y Pupilometría en las mismas ventanas usadas para EEG: **2 s, 50% de solapamiento**.
2. Descartar ventanas con datos faltantes o de mala calidad en cualquiera de las señales fuente (mismo criterio que el preprocesamiento EEG: >20% de datos inválidos → descartar).
3. Cada ventana queda con un identificador (Participante, Estímulo, N° de ventana) para poder unirla luego al tensor de features EEG. Requiere que ambas señales estén sincronizadas entre sí y con EEG (ver pipeline de sincronización revisado — offset + corrección de drift).

## Construcción paso a paso

**Paso 1 — Features por ventana y por señal**
- Eye Tracking: agregar (promedio/conteo) fijaciones, duración, tiempo dentro de AOI, dispersión dentro de cada ventana.
- Pupilometría: agregar diámetro pupilar (promedio y/o variación) dentro de cada ventana.

**Paso 2 — Normalización**
- Normalizar cada feature (ej. z-score o min-max) **por participante**, para controlar diferencias individuales en línea base de atención antes de combinar señales. *(Decisión a validar: normalizar por participante vs. globalmente — afecta cuánto se comparan personas entre sí.)*

**Paso 3 — Fusión en un Attention Score**
- Combinar las features normalizadas de ambas fuentes en un score único por ventana.
- Métodos posibles a evaluar (no decidido aún):
  - Promedio ponderado simple de los componentes espacial/temporal (Eye Tracking) y cognitivo (Pupilometría).
  - Un modelo simple (ej. regresión) si existe alguna referencia de validación para ajustar pesos.
- *(Decisión pendiente: definir los pesos o el método de fusión. No hay evidencia aún para fijarlos — deben decidirse y justificarse, no asumirse arbitrariamente.)*

**Paso 4 — Discretización**
- Convertir el Attention Score continuo en categorías (ej. alta/media/baja, o binaria atento/no-atento).
- Opciones de umbral a evaluar:
  - **Relativo por participante** (ej. terciles de su propia distribución): controla diferencias individuales, pero pierde comparabilidad entre personas.
  - **Absoluto/global**: comparable entre personas, pero sensible a diferencias individuales de línea base ocular/pupilar.
- *(Decisión pendiente: elegir y justificar el criterio de corte.)*

**Paso 5 — Validación de la pseudoetiqueta**
- Si existe alguna fuente adicional (autoreporte, desempeño en tarea, anotación humana parcial), usarla para chequear que la etiqueta se aproxima a "Atendido" y no solo a "Observado" — es decir, que no es pura fijación ocular disfrazada de atención.
- Si no existe validación externa disponible, dejarlo explícito como limitación del trabajo.

## Conexión con el Modelo Estudiante (Etapa 2) y la hipótesis
- **Predictores del modelo:** EEG + GSR.
- **Hipótesis central (temporal vs. estático, tipo de fusión):** se compara un baseline estático contra modelos temporales (LSTM/TCN/Transformer), y dentro de los temporales, fusión temprana / intermedia / tardía de EEG+GSR — todo prediciendo el mismo Attention Score fijo, así cualquier diferencia de desempeño es atribuible al modelo, no a la etiqueta.
- **Análisis complementario:** se puede observar la trayectoria intra-sesión del Attention Score para identificar patrones compatibles con fatiga/habituación.

## Riesgos y mitigaciones
| Riesgo | Mitigación |
|---|---|
| La etiqueta puede reflejar solo "mirar", no "atender" (ver marco conceptual) | Usar ambas fuentes (ocular + pupilar), no solo Eye Tracking |
| El "modelo profesor" (Eye+Pupil) nunca será mejor que su propia regla de construcción | Reportarlo explícitamente como límite superior de la calidad de la pseudoetiqueta |
| Pupila responde a luz ambiental, no solo a cognición | Controlar/reportar si el estímulo tiene luminosidad variable; considerar corrección lumínica si aplica |
| Ruido en las etiquetas | Discretizar en pocas categorías (no continuo fino) para tolerar ruido |
| Fuga de información entre entrenamiento y evaluación | Calcular normalización/umbrales solo con datos de entrenamiento; EEG/GSR nunca se usan para construir la etiqueta |
| Diferencias individuales en línea base ocular/pupilar | Evaluar normalización por participante (Paso 2) |

## Decisiones aún pendientes (a resolver o validar con el profesor/guía)
- [ ] Método exacto de fusión del Attention Score (pesos o modelo).
- [ ] Criterio de discretización (relativo vs. absoluto, número de categorías).
- [ ] Disponibilidad de alguna fuente de validación externa de la etiqueta.
- [ ] Confirmar si se normaliza por participante o globalmente.
- [ ] Confirmar si existe corrección lumínica disponible para la pupilometría (pendiente en el pipeline de sincronización revisado).

## Notas relacionadas
- [[Atencion]]
- [[Etiqueta Emocion]]
- [[Resumen Diseño Etiquetas y Modelos]]
- [[Estructura Tesis]]
- [[Problema e hipótesis]]
