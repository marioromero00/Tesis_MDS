# Resumen — Diseño de Etiquetas y Modelos (Toma de Muestra 2)

Cuadro de referencia rápida del diseño acordado para las variables objetivo y los modelos predictivos, usando las 4 señales de la **Toma de Muestra 2**: EEG, GSR, Pupilometría, Eye Tracking (sin expresión facial). Detalle completo en [[Etiqueta Atencion]] y [[Etiqueta Emocion]].

## Cuadro resumen

|                                                         | **Atención**                                                                                                                       | **Emoción (redefinida como Arousal)**                                                                          |
| ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Etapa 1 — Modelo Profesor** (construye la etiqueta)   | Eye Tracking + Pupilometría → Attention Score                                                                                      | GSR → Arousal Score                                                                                            |
| **Etapa 2 — Modelo Estudiante** (se evalúa en la tesis) | EEG + GSR                                                                                                                          | EEG + Eye Tracking + Pupilometría                                                                              |
| **Por qué esas señales y no otras**                     | Eye Tracking mide dimensión espacial/temporal; Pupilometría es proxy de carga cognitiva (dimensión cognitiva del marco conceptual) | GSR es el único proxy limpio de activación simpática entre las 4 señales disponibles                           |
| **Riesgo/limitación central**                           | Confundir "mirar" (Observado) con "atender" (Atendido) — mitigado combinando 2 fuentes                                             | GSR mide solo activación, no permite hablar de "emoción" en sentido amplio — se declara como límite de alcance |
| **Ventana temporal**                                    | 2 s, 50% solapamiento (igual que EEG)                                                                                              | 2 s, 50% solapamiento — *a validar por latencia típica de SCR (1–5 s)*                                         |
| **Circularidad evitada**                                | No se usa EEG/GSR para construir su propia etiqueta                                                                                | No se usa EEG/EyeTracking/Pupilometría para construir su propia etiqueta                                       |

## Cómo se contrasta la hipótesis en ambos modelos

**Hipótesis central — Los modelos temporales multimodales obtienen un mejor desempeño fuera de muestra que los modelos estáticos comparables:**
Con el profesor fijo (misma etiqueta para todas las comparaciones), se evalúa cada Modelo Estudiante en:
- Baseline **estático** (sin dinámica temporal) vs. modelos **temporales** (LSTM / TCN / Transformer).
- Dentro de los temporales, tipo de **fusión** de las señales predictoras: **temprana** (concatenar en un encoder), **intermedia** (encoders separados + cross-attention), **tardía** (modelo por señal + voto/promedio).
- Como la etiqueta no cambia entre comparaciones, cualquier diferencia de desempeño es atribuible al modelo, no a la etiqueta.

**Análisis complementario — Fatiga y habituación:**
Se puede observar si el Attention Score y el Arousal Score decaen a lo largo de la sesión. Este análisis no constituye una segunda hipótesis y no permite atribución causal sin una medida externa.

## El argumento de rigor (para defender con el profesor)
Ninguna señal usada para **construir** una etiqueta se reutiliza como **input** para predecir esa misma etiqueta — evita que el modelo aprenda a reproducir una regla en vez de extraer información nueva desde EEG. La limitación de cada "modelo profesor" (nunca puede ser mejor que su propia regla de construcción) está identificada y documentada explícitamente, no oculta.

## Decisiones aún abiertas (consolidado)
- [ ] Método de fusión y umbral de discretización del Attention Score ([[Etiqueta Atencion]]).
- [ ] Método de combinación de features GSR y umbral de discretización del Arousal Score ([[Etiqueta Emocion]]).
- [ ] Ventana de agregación específica para GSR (por latencia de SCR).
- [ ] Confirmar con el profesor si redefinir "emoción" como "arousal" es aceptable dado el alcance de la hipótesis central.
- [ ] Disponibilidad de alguna fuente de validación externa para cualquiera de las dos etiquetas.

## Notas relacionadas
- [[Etiqueta Atencion]]
- [[Etiqueta Emocion]]
- [[Atencion]]
- [[Estructura Tesis]]
- [[Problema e hipótesis]]
