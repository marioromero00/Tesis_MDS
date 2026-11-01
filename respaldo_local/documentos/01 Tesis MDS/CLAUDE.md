# 01 Tesis MDS — Detección multimodal de atención y emoción

## Qué es esta sección
Notas de trabajo de la tesis del Magíster en Data Science: detectar atención y activación
emocional durante navegación web a partir de señales neurofisiológicas. Se enmarca en el
proyecto **Fondecyt 1231122** (dirigido por el Dr. Juan D. Velásquez, codirigido por la
Dra. Flavia Guiñazú).

**NO es** el repositorio de código ni de datos de la tesis: aquí vive el razonamiento, el
diseño de etiquetas y la escritura. El código y los datos del EDA y el preprocesamiento
viven en `~/tesis/Tesis_MDS`; en el vault está **solo su documentación**,
en `Analisis de Datos/`.
Si el pipeline cambia, se actualiza allá y se vuelve a traer — no se edita en los dos lados.

**Norte permanente:** el aporte de la tesis está en la **temporalidad y el tipo de fusión**,
no en la modalidad. Tratar atención y emoción como procesos dinámicos, no como promedios.

## Estado actual
**El estado vigente vive en [[Tesis_MDS]]**, no aquí: este archivo son las reglas, el índice
es la foto. Al 22-08-2026: EDA y preprocesamiento multimodal ejecutados y reproducibles,
primera evaluación fuera de muestra hecha con baselines estáticos alrededor del nivel
trivial. El diseño de etiquetas sigue rediseñado para la Toma de Muestra 2.

## Hipótesis
- **Hipótesis central:** los modelos temporales multimodales obtienen un mejor desempeño
  fuera de muestra que los modelos estáticos comparables en la detección de emociones y
  atención durante la navegación web.
- Fatiga y habituación pueden estudiarse como análisis complementario, pero **no son una
  segunda hipótesis**.

## El diseño en una línea
Dos etapas por variable. El **Modelo Profesor** construye la etiqueta desde unas señales;
el **Modelo Estudiante** la predice desde señales **distintas**. Detalle en
[[Resumen Diseño Etiquetas y Modelos]].

| | Atención | Emoción (redefinida como *arousal*) |
|---|---|---|
| Profesor (construye etiqueta) | Eye Tracking + Pupilometría | GSR |
| Estudiante (se evalúa) | EEG + GSR | EEG + Eye Tracking + Pupilometría |

Ventana: 2 s con 50 % de solapamiento (la de GSR está a validar por latencia de SCR, 1–5 s).

## Estructura de notas
- [[Tesis_MDS]] — índice: objetivo, estado, próximos pasos
- [[Problema e hipótesis]] — problema, antecedentes, aporte e hipótesis central
- [[Estructura Tesis]] — esqueleto LaTeX del borrador, con las secciones pendientes marcadas
- [[Resumen Diseño Etiquetas y Modelos]] — cuadro de referencia rápida del diseño acordado
- [[Etiqueta Atencion]] · [[Etiqueta Emocion]] — detalle por variable
- [[Atencion]] — marco conceptual
- [[Referencia Tesis Previas]] — tesis del grupo usadas como referencia
- `Analisis de Datos/` → [[Mapa del proyecto]] — documentación del pipeline (12 notas planas),
  sincronizada al 22-08-2026 desde el repositorio `~/tesis/Tesis_MDS`
- `attachments/Analisis de Datos/` — las 16 figuras que genera el pipeline
- `presentaciones/` — punteos para armar slides fuera del vault

## Audiencias
*(deducido de las notas — confírmame si está mal)*

| Quién | Qué espera |
|---|---|
| Profesor guía (Dr. Juan D. Velásquez) | Rigor metodológico; que las decisiones abiertas se cierren con argumento, no por conveniencia |
| Comité / defensa | El argumento de no-circularidad y los límites de alcance declarados explícitamente |

## Cuando me ayudes aquí

- **La Toma de Muestra 2 no incluye expresión facial.** Esa señal existe en la Toma de
  Muestra 1, que usan otras tesis del grupo, no en este dataset. Cualquier diseño que
  proponga usar el clasificador facial como profesor está mal: es exactamente lo que se
  descartó.
- **Regla de no-circularidad, innegociable:** ninguna señal usada para *construir* una
  etiqueta se reutiliza como *input* para predecir esa misma etiqueta. Si una propuesta la
  viola, dilo antes de seguir.
- **"Emoción" está redefinida como *arousal*** porque GSR solo mide activación simpática.
  No hables de emoción en sentido amplio. Esta redefinición **aún no la confirma el
  profesor** — es una decisión abierta, no un hecho.
- **Las decisiones abiertas de [[Resumen Diseño Etiquetas y Modelos]] no se cierran sin mi
  confirmación explícita.** Son cinco y están marcadas con checkbox.
- Al comparar modelos, la etiqueta se mantiene fija: cualquier diferencia de desempeño debe
  ser atribuible al modelo. Si un cambio toca la etiqueta, deja de ser comparable.
- En [[Estructura Tesis]], lo que dice *(pendiente)* está pendiente de verdad. No lo
  rellenes con texto plausible.

## Convenciones propias
- Los términos del diseño van en su forma acordada: *Modelo Profesor*, *Modelo Estudiante*,
  *Attention Score*, *Arousal Score*. No los traduzcas ni los renombres.
- Distinguir siempre **Observado** ("mirar") de **Atendido** ("atender"): confundirlos es el
  riesgo central de la etiqueta de atención.
