# Presentación 10-08-26 — Punteo

Contenido base para armar en Canva (u otra herramienta). Estructura: 9 diapositivas. Cada bloque = 1 diapositiva. Sin diseño, solo título + bullets.

> **Deck armado (08-08-2026):** `presentacion-10-08-26.html`, en esta misma carpeta. Las 9
> diapositivas de este punteo, navegables con flechas desde el navegador. Las cuatro señales van
> codificadas por color (paleta Okabe-Ito, segura para daltonismo) y ese código se mantiene en
> todas las láminas, de modo que la disyunción profesor/estudiante se ve sin explicarla.
> Si cambias el contenido, cámbialo aquí primero: este punteo sigue siendo la fuente.

Referencia completa: [[Resumen Diseño Etiquetas y Modelos]], [[Etiqueta Atencion]], [[Etiqueta Emocion]].

---

## 1. Portada
- **Título:** Etiquetas sin señal facial: rediseño Profesor → Estudiante
- **Subtítulo:** Cómo construir y predecir atención y activación emocional usando solo las señales de la Toma de Muestra 2
- Chips/etiquetas: EEG · GSR · Pupilometría · Eye Tracking
- Pie: Mario Romero · Detección multimodal de emociones y atención · Agosto 2026

---

## 2. Contexto
- **Título:** La Toma de Muestra 2 no incluye expresión facial
- El diseño previo usaba un clasificador facial como "modelo profesor" para atención y emoción.
- Esa señal existe en la Toma de Muestra 1 (usada en otras tesis del grupo), no en mi dataset.
- Señales reales disponibles: EEG (16 canales, **125 Hz**) · GSR (Tobii Pro, ~8 Hz efectivos) · Pupilometría (Tobii Pro, 60 Hz) · Eye Tracking (Tobii Pro, fijaciones/sacadas)
  - *22-08-2026 — verificado contra los datos crudos: son **125 Hz**. La cabecera OpenBCI lo declara, la frecuencia efectiva medida da 125,1 Hz y el epoching real usa 250 muestras por ventana de 2 s. La placa es Cyton + Daisy: 16 canales a 125 Hz. Queda revertida la "corrección" a 250 Hz del 08-08-2026.* Ver [[Conocimiento Presentaciones Pasadas]].
- Escala del dataset: 48 participantes, 13,4 ± 1,5 min por sesión, sin valores faltantes.
- Callout: sin facial no hay clasificador de categorías de emoción ni proxy de valencia directo — obliga a repensar qué es "emoción" en este trabajo.

---

## 2b. Qué cambió desde junio *(nueva, 08-08-2026)*
- **Título:** Qué cambió desde la presentación de junio
- Tabla Junio → Hoy: señales del diseño (con Facial → con Pupilometría) · profesor de atención (clasificador facial, Enfoque 2 → Eye Tracking + Pupilometría, Enfoque 3) · emoción (Ekman / valencia–arousal → solo arousal) · estudiante de atención (solo EEG → EEG + GSR).
- Callout: el rediseño no es cambio de rumbo, es consecuencia de que la Toma de Muestra 2 no tiene la señal facial.

---

## 3. El patrón: Modelo Profesor → Modelo Estudiante
- **Título:** El patrón que se repite en ambos modelos
- El "modelo profesor" ya no es solo un clasificador facial: es cualquier combinación de señales que construye la pseudoetiqueta.
- El "modelo estudiante" es el que se evalúa en la tesis, y nunca recibe como input la señal que definió su propia etiqueta.
- Esquema: Señales fuente (A) → Profesor (regla/score) → Pseudoetiqueta
- Esquema: Señales predictoras (B, B≠A) → Estudiante (modelo temporal multimodal) → se evalúa contra la pseudoetiqueta
- Nota: A ∩ B = ∅ — ninguna señal cumple los dos roles a la vez.

---

## 4. Atención
- **Título:** Eye Tracking + Pupilometría como profesor
- Profesor: Eye Tracking + Pupilometría → Attention Score
- Estudiante: EEG + GSR
- Eye Tracking aporta: dimensión espacial y temporal (dónde y cuánto tiempo mira)
- Pupilometría aporta: dimensión cognitiva (dilatación como proxy de carga atencional)
- Riesgo: el eye tracking solo mide "Observado", no "Atendido". Combinar ambas fuentes mitiga —no elimina— ese riesgo.

---

## 5. Emoción → Arousal
- **Título:** GSR como profesor de activación
- Profesor: GSR (SCR + SCL) → Arousal Score
- Estudiante: EEG + Eye Tracking + Pupilometría
- Por qué no Ekman: requiere un clasificador de categorías (típicamente facial), no disponible.
- Por qué no valencia-arousal completo: ninguna de las 4 señales da valencia sin usar EEG (circular) o facial (inexistente).
- Callout: la trayectoria de activación puede analizarse de forma complementaria para identificar patrones compatibles con fatiga/habituación; no constituye una segunda hipótesis.

---

## 6. Cuadro comparativo
- **Título:** Los dos modelos, lado a lado

| | Atención | Emoción (Arousal) |
|---|---|---|
| Profesor | Eye Tracking + Pupilometría | GSR |
| Etiqueta | Attention Score | Arousal Score |
| Estudiante | EEG + GSR | EEG + Eye Tracking + Pupilometría |
| Ventana | 2 s, 50% solapamiento | 2 s — a validar por latencia SCR (1–5 s) |
| Riesgo central | Observado ≠ Atendido | Mide activación, no valencia |

---

## 7. Hipótesis central
- **Título:** Mismo profesor, se compara el estudiante
- **Hipótesis:** Los modelos temporales multimodales obtienen un mejor desempeño fuera de muestra que los modelos estáticos comparables en la detección de emociones y atención durante la navegación web.
- La etiqueta no cambia entre comparaciones, así que cualquier diferencia de desempeño es atribuible al modelo.
  - Fusión temprana: concatenar señales en un encoder
  - Fusión intermedia: encoders separados + cross-attention
  - Fusión tardía: modelo por señal + voto/promedio
- **Análisis complementario:** se puede observar la trayectoria intra-sesión de Attention Score y Arousal Score para identificar patrones compatibles con fatiga/habituación.

---

## 7b. Lo que ya está construido *(nueva, 08-08-2026)*
- **Título:** Lo que ya está construido
- Columna izquierda — **EDA Toma de Muestra 2**: 48 participantes, 16 canales · 13,4 ± 1,5 min por sesión (mediana 13,1) · sin valores faltantes · 21 de 48 con al menos un canal saturado, mediana 0 · pico de potencia en 50 Hz (red eléctrica).
- Columna derecha — **Pipeline EEG implementado**: Butterworth orden 4 fase cero (HP 1 Hz · LP 40 Hz · Notch 50 Hz) · rechazo sobre ±150 µV · épocas de 2 s con 50% de solapamiento, descarte sobre 20% de NaN · potencia por banda (Welch) en δ θ α β γ, absoluta y relativa · 7 índices inter-banda + asimetría hemisférica alpha.
- Callout: **273 features por época** (160 potencias + 112 índices + 1 asimetría). El pipeline EEG está cerrado; falta el EDA de Eye Tracking y Pupilometría.
- Fuente de todos estos números: [[Conocimiento Presentaciones Pasadas]].

---

## 8. Próximos pasos
- **Título:** Qué falta para poder implementar
- Subtítulo: ordenado por lo que bloquea al resto
1. Confirmar con el profesor si redefinir "emoción" como "arousal/activación" es aceptable para el alcance de la hipótesis central. — *Requiere profesor*
2. EDA de Eye Tracking y Pupilometría (aún pendiente; ya está hecho para EEG). — *Decisión propia*
3. Cerrar método de fusión y umbral de discretización del Attention Score y del Arousal Score. — *Decisión propia*
4. Confirmar ventana de agregación para GSR, dada la latencia típica de la SCR (1–5 s). — *Decisión propia*
5. Implementar el pipeline de etiquetado sobre las señales ya sincronizadas. — *Implementación*
6. Entrenar el primer modelo estudiante — baseline EEG+GSR para atención. — *Implementación*

---

## 9. Cierre
- **Título:** Mismo rigor, señales distintas
- Ninguna señal usada para construir una etiqueta se reutiliza como input para predecirla.
- El límite de cada modelo profesor —nunca mejor que su propia regla— queda documentado, no oculto.
- **Preguntas para el profesor:**
  - ¿Es aceptable redefinir "emoción" como "arousal/activación" dado el alcance real de los datos?
  - ¿Existe alguna fuente de valencia en el proyecto que no estemos considerando?
  - ¿El argumento anti-circularidad (profesor/estudiante disjuntos) es suficiente para la defensa metodológica?

## Notas relacionadas
- [[Resumen Diseño Etiquetas y Modelos]]
- [[Etiqueta Atencion]]
- [[Etiqueta Emocion]]
