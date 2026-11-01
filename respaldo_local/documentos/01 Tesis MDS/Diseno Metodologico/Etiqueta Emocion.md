# Etiqueta Emoción (Arousal) — Metodología

> [!warning] Actualización 22-08-2026
> Se implementaron scores GSR de 2 s, contexto causal de 6 s y PCA. La variante de 6 s es
> primaria, pero redefinir emoción como activación aún requiere aprobación del profesor.
> Véase [[Avance - 22-08-2026 (Etiquetas Particion y Baselines)]].

Documento de trabajo para la construcción de la variable objetivo "emoción" del modelo EEG. **Redefinida como Arousal/Activación** (un solo eje del modelo dimensional de Russell), en paralelo a [[Etiqueta Atencion]] y alineado con el preprocesamiento de [[Estructura Tesis]].

**Nota de alcance:** trabajo con la **Toma de Muestra 2** (EEG, GSR, Pupilometría, Eye Tracking) — no hay señal de expresión facial. Por eso este documento reemplaza el enfoque discreto de Ekman (que requería un clasificador facial como fuente) por un enfoque de **arousal**, que sí es medible con las señales disponibles.

## Por qué Arousal y no Ekman discreto ni Valencia-Arousal completo
De las 4 señales de la Toma de Muestra 2, **GSR y Pupilometría solo dan información de arousal** (activación simpática / carga cognitiva), no de valencia. No existe ninguna fuente limpia de valencia sin usar EEG (asimetría hemisférica alpha) o expresión facial — y ambas están descartadas: EEG porque es la señal de entrada del modelo de atención y de este mismo modelo (circularidad), y facial porque no existe en la Toma de Muestra 2. Por lo tanto:
- **Ekman discreto**: no factible — requiere un clasificador de categorías (típicamente facial) que no está disponible.
- **Valencia-Arousal completo (Russell)**: no factible — falta el eje de valencia.
- **Arousal únicamente**: factible y defendible — es lo único medible de forma limpia con las señales disponibles.

La trayectoria del arousal también puede servir para un análisis complementario de patrones compatibles con fatiga/habituación. Este análisis no forma parte de la hipótesis central.

## Arquitectura de dos etapas: Modelo Profesor → Modelo Estudiante
- **Etapa 1 — Modelo Profesor (esta etiqueta):** **GSR** → nivel de Arousal. Señal única (no requiere fusión): SCR (picos, amplitud) + SCL (nivel tónico) + variabilidad, todas ya reconocidas en la literatura psicofisiológica como indicadores de activación simpática.
- **Etapa 2 — Modelo Estudiante (lo que se evalúa en la tesis):** **EEG + Eye Tracking + Pupilometría** → predice el nivel de Arousal del profesor. Sobre este modelo se contrasta la **hipótesis central** (estático vs. temporal, fusión temprana/intermedia/tardía). La trayectoria temporal queda como análisis complementario.

Ver [[Resumen Diseño Etiquetas y Modelos]] para el cuadro comparativo con el diseño de atención. Nota importante: Eye Tracking y Pupilometría son las señales fuente de la etiqueta de **Atención**, pero aquí actúan como **predictoras** de Arousal — no hay circularidad porque no se usan para construir su propia etiqueta, solo la del otro modelo.

## Fuente de datos
| Señal | Rol | Features relevantes |
|---|---|---|
| GSR | Única fuente del Modelo Profesor de Arousal | Número de picos (SCR), amplitud de respuesta, nivel tónico (SCL), variabilidad de la señal |

**EEG queda excluido** de la construcción de la etiqueta, por la misma razón que en atención: es señal de entrada del modelo estudiante.
**Eye Tracking y Pupilometría también quedan excluidos** de la construcción de esta etiqueta (aunque sí se usan como input del modelo estudiante) — para no mezclar el rol de "fuente de atención" con "fuente de arousal".

## Supuestos
1. **GSR es un proxy válido de arousal, no de valencia:** el nivel de activación simpática no indica si la experiencia es positiva o negativa, solo cuán intensa/activada es.
2. **El "modelo profesor" es un techo de calidad:** el nivel de arousal derivado de GSR no puede validarse contra otra medida de activación (a menos que aparezca una fuente adicional), por lo que su calidad depende enteramente de qué tan bien las reglas/umbrales usados reflejan activación real.
3. **Estacionariedad dentro de la ventana:** se asume un nivel de arousal representativo por ventana de 2 s (misma ventana que EEG/atención).
4. **Latencia de la respuesta GSR:** las SCR tienen una latencia típica de 1–5 s tras el estímulo que las provoca (dato confirmado en el pipeline de sincronización revisado) — esto puede requerir un desfase o ventana de agregación más ancha que la de atención para capturar la respuesta completa.
5. **La pseudoetiqueta no es verdad absoluta**, igual que en atención — ruido y artefactos de sensor (desconexiones, saltos abruptos) son esperables.

## Construcción paso a paso

**Paso 1 — Alineación temporal**
Segmentar GSR en las mismas ventanas de EEG (2 s, 50% de solapamiento), descartando ventanas con datos faltantes o de mala calidad (mismo criterio usado en preprocesamiento EEG y en [[Etiqueta Atencion]]). *(Decisión pendiente: evaluar si 2 s es suficiente dado el supuesto 4 de latencia, o si conviene una ventana de agregación más ancha específicamente para GSR.)*

**Paso 2 — Extracción de features por ventana**
Calcular dentro de cada ventana: número de picos SCR, amplitud promedio de SCR, nivel tónico SCL, variabilidad de la señal (ya definidas como features de GSR en [[Estructura Tesis]]).

**Paso 3 — Normalización**
Normalizar por participante (z-score), para controlar diferencias individuales en conductividad basal de la piel — mismo criterio ya usado en el pipeline de sincronización revisado para GSR.

**Paso 4 — Fusión en un Arousal Score**
A diferencia de atención, aquí no hay que fusionar señales distintas (GSR es la única fuente), pero sí hay que combinar sus múltiples features (SCR, SCL, variabilidad) en un score único.
- *(Decisión pendiente: promedio simple, ponderación por feature, o usar solo SCL o solo SCR como indicador principal — a decidir con literatura de referencia.)*

**Paso 5 — Discretización**
Convertir el Arousal Score continuo en categorías (ej. alta/baja activación, o terciles).
- *(Decisión pendiente: mismo dilema que en atención — umbral relativo por participante vs. absoluto/global.)*

**Paso 6 — Validación**
Si existe alguna fuente adicional (autoreporte, contexto del estímulo), usarla para verificar que la etiqueta tiene sentido. Si no, declarar como limitación explícita.

## Conexión con el Modelo Estudiante (Etapa 2) y la hipótesis
- **Predictores del modelo:** EEG + Eye Tracking + Pupilometría.
- **Hipótesis central (temporal vs. estático, tipo de fusión):** mismo diseño que en atención — profesor fijo (Arousal Score de GSR), se compara estático vs. temporal, y fusión temprana/intermedia/tardía de las 3 señales predictoras.
- **Análisis complementario:** se puede observar la trayectoria intra-sesión del Arousal Score para identificar patrones compatibles con fatiga/habituación.

## Riesgos y mitigaciones
| Riesgo | Mitigación |
|---|---|
| GSR mide solo activación, no permite hablar de "emoción" en sentido amplio | Declarar explícitamente el alcance como Arousal/Activación, no Emoción completa, en la tesis |
| El modelo profesor (GSR) nunca será mejor que su propia regla de construcción | Reportarlo como límite superior de calidad de la pseudoetiqueta |
| Artefactos de sensor (desconexión, saltos abruptos) | Filtrado por umbral adaptativo antes de construir la etiqueta (igual que en el pipeline de sincronización revisado) |
| Latencia de la respuesta GSR no capturada por ventana de 2s | Evaluar ventana de agregación específica para GSR (Paso 1) |
| Fuga de información entre entrenamiento y evaluación | EEG, Eye Tracking y Pupilometría nunca se usan para construir esta etiqueta |

## Decisiones aún pendientes (a resolver o validar con el profesor/guía)
- [ ] Ventana de agregación para GSR (2 s estándar vs. ventana más ancha por latencia de SCR).
- [ ] Método de combinación de features GSR en un Arousal Score único (Paso 4).
- [ ] Criterio de discretización (Paso 5).
- [ ] Disponibilidad de alguna fuente de validación externa.
- [ ] Confirmar con el profesor si redefinir "emoción" como "arousal/activación" es aceptable para el alcance de la tesis, dado que la hipótesis menciona "emociones" en términos generales.

## Notas relacionadas
- [[Etiqueta Atencion]]
- [[Atencion]]
- [[Resumen Diseño Etiquetas y Modelos]]
- [[Estructura Tesis]]
- [[Problema e hipótesis]]
