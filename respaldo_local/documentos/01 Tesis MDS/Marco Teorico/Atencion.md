# Etiquetado de atención

## Objetivo
Definir la variable que el modelo EEG deberá predecir.

## Marco conceptual: ¿qué es realmente "atención"?
Aporte del profesor (conversación). La mirada no es sinónimo de atención, y la atención no es sinónimo de comprensión. Que un usuario fije la vista sobre un elemento no implica que lo esté procesando cognitivamente (ej.: leer un párrafo completo y no recordar nada de lo leído).

### Niveles
1. **Visible:** el contenido está presente en la pantalla.
2. **Observado:** el usuario dirige la mirada hacia ese contenido.
3. **Atendido:** el cerebro asigna recursos cognitivos para procesarlo.
4. **Comprendido:** el usuario interpreta, integra y puede utilizar esa información.

Que un elemento sea visible o incluso observado no significa que haya sido atendido o comprendido.

### Dimensiones
1. **Espacial:** ¿dónde mira el usuario?
2. **Temporal:** ¿durante cuánto tiempo mantiene su atención?
3. **Cognitiva:** ¿está realmente procesando la información o solo la está observando?
4. **Intencional:** ¿con qué objetivo está mirando ese contenido?

### Implicancia para esta tesis
El eye tracking (fijaciones, sacadas, tiempo de permanencia) es solo un **indicador indirecto** de atención: evidencia que el usuario miró un lugar, no que procesó la información. La pregunta de investigación relevante no es "¿dónde miró el usuario?" sino **"¿qué contenido recibió realmente atención cognitiva?"**. Responder esto requiere integrar múltiples fuentes de evidencia — no solo eye tracking, sino también EEG, diámetro pupilar, GSR, patrones de navegación, movimientos del mouse, comportamiento de scroll, e incluso el desempeño posterior del usuario en una tarea.

Esto refuerza el enfoque multimodal de la tesis: ninguna señal individual (incluido el eye tracking) basta por sí sola para afirmar que hubo atención real.

## Alternativas

### Modelo facial profesor
Utilizar un modelo facial para generar pseudoetiquetas de atención.

### Anotaciones existentes
Revisar si existen etiquetas humanas o variables conductuales.

### Fatiga y habituación
Construir etiquetas a partir de la evolución temporal de la sesión.

## Decisión actual
Pendiente.

## Riesgos
- Las pseudoetiquetas no son verdad absoluta.
- Puede existir ruido en las etiquetas.
- Debe evitarse fuga de información entre entrenamiento y evaluación.
- El eye tracking por sí solo mide el nivel "Observado", no necesariamente "Atendido" o "Comprendido" (ver Marco conceptual) — una etiqueta basada solo en fijaciones puede confundir mirar con atender.

## Relacionado
- [[Problema e hipótesis]]
- [[Datos EEG]]
- [[Experimentos]]