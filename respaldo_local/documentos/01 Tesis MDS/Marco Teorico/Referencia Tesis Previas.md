# Referencia — Estructura y Estilo de Tesis Previas

Síntesis de 6 memorias previas del mismo grupo de investigación (líneas de neurodatos/emociones-atención, U. de Chile), revisadas para calibrar estructura, extensión y estilo de esta tesis. Se muestrearon índice, introducción, metodología, conclusiones y bibliografía de cada una (no se leyeron completas).

## Tesis revisadas
| Autor | Título (resumido) | Programa | Páginas |
|---|---|---|---|
| Cristóbal Subiabre (2024) | Detección y clasificación de emociones y nivel de atención a partir de expresiones faciales | Mag. Ciencia de Datos | 104 |
| Fernanda Saavedra (2025) | Reconocimiento de emociones en usuarios web basado en GSR y EEG | Mag. Ciencia de Datos | 120 |
| José Saffie (2025) | Detección de las mejores características para un modelo de aprendizaje de emociones con EEG e imágenes faciales | Mag. Ciencia de Datos | 172 |
| Lino Jeldez (2024) | Neuro-navegación: respuestas emocionales en usuarios chilenos al visualizar páginas web mediante EEG | Ing. Civil Industrial | 141 |
| Matías López (2025) | Detección de emociones y nivel de interés mediante seguimiento ocular y expresiones faciales | Mag. Ciencia de Datos | 186 |
| Pablo Villanueva (2024) | Development of a Multimodal Web User Dataset... for Visual Attention Prediction (en inglés) | Mag. Ciencia de Datos | 161 |

## Estructura de capítulos "consenso"

Casi universal en las 6 (varía el nombre exacto):
1. **Introducción**: motivación/antecedentes, preguntas de investigación, objetivos (general + específicos), y en 4/6 una sección explícita de hipótesis y/o metodología resumida.
2. **Marco Teórico/Conceptual**: capítulo largo (22–49 págs.), típicamente el 2° más extenso.
3. **Diseño experimental / metodología** (nombres variables: "Diseño y Planteamiento del Experimento", "Proceso Metodológico", "Metodología para la Captura de Datos", "Proposed Experiment"): instrumentos, participantes, protocolo.
4. **Resultados** (a veces fusionado con Discusión): sistemáticamente el capítulo más extenso (30–88 págs.), crece con el número de modalidades/sub-estudios.
5. **Conclusiones** (a veces con Discusión separada): 3–16 págs., casi siempre con "Trabajo Futuro"/"Recomendaciones".
6. **Bibliografía**.

**Puntos donde varían:**
- Separar Discusión de Conclusiones en capítulos independientes: solo López y Villanueva.
- Capítulo de "Estado del Arte" separado del Marco Teórico: solo Villanueva.
- Framework metodológico nombrado y explícito (KDD o CRISP-DM) como columna vertebral de la metodología: Saavedra (CRISP-DM), Saffie (KDD), Jeldez (CRISP-DM adaptado). Subiabre, López y Villanueva no nombran framework formal — su "metodología" es una lista de pasos ad hoc mapeada a los objetivos específicos.
- Anexos: extensos en Villanueva (32 págs.: consentimientos, formularios, arquitecturas) y Saffie (20 págs.); mínimos o ausentes en Saavedra, Jeldez y López.
- Sección de "Reflexión Ética" en Conclusiones: solo en López (vigilancia emocional, sesgos algorítmicos, marcos UNESCO/UE de IA).

## Extensión típica
- Rango observado: **104–186 páginas** totales.
- "Centro de masa" (excluyendo extremos): **~140–172 páginas**.
- Marco Teórico: 25–35% del total (22–49 págs.).
- Resultados: el capítulo más variable, domina el documento cuando hay múltiples modalidades de datos.
- Bibliografía: de ~30 (Subiabre) a >220 referencias (López) — no correlaciona con extensión total, sino con exhaustividad de la revisión.

## Convenciones de estilo

**Plantilla:** las 6 comparten portada de "Universidad de Chile / Facultad de Ciencias Físicas y Matemáticas / Departamento de Ingeniería Industrial", numeración de figuras/tablas por capítulo, resumen ejecutivo de ~1 página antes del índice, agradecimientos, e índices de tablas/ilustraciones separados.

**Citación/bibliografía — dos familias, sin consenso único (elegir una y ser consistente):**
- Numerada estilo IEEE/plain, sin autor-año en texto: Subiabre, Jeldez, Villanueva.
- Numerada con formato de entrada APA (bracket [n] pero cada referencia en formato APA, citación en texto tipo (Autor, año)): Saavedra, Saffie, López.

**Objetivos:** patrón universal — "Objetivo General" (1 párrafo, verbo en infinitivo: detectar/identificar/desarrollar/reconocer) + 4–7 "Objetivos Específicos" en infinitivo, ordenados como build-up (revisión bibliográfica → obtención de datos → construcción del modelo → evaluación → análisis de hallazgos).

**Hipótesis — heterogeneidad notable, todas aceptadas por el programa:**
- Sin hipótesis, solo preguntas de investigación (Saavedra).
- Hipótesis en prosa simple, un párrafo (Subiabre, López).
- Hipótesis formal con par H0/HA por cada pregunta de investigación (Saffie, Villanueva).
- Hipótesis planteada en la introducción y confirmada/refutada explícitamente en conclusiones (Jeldez, Villanueva).

## Ejemplos de frases tipo (con atribución, máx. 1 oración por caso)

**Objetivo general:**
- Subiabre: *"El objetivo general de la tesis es detectar, reconocer y analizar las reacciones faciales y nivel de atención de una persona al ser expuesta a distintos contenidos multimedia, a partir de una cámara y utilización de técnicas de deep learning."*
- Saffie: *"Desarrollar diversos modelos de aprendizaje emocional basados en respuestas fisiológicas y respuestas faciales ante estímulos visuales, con el fin de identificar las características más efectivas para predecir emociones y utilizar estos modelos creados en un contexto de uso web."*
- Villanueva: *"To develop a multimodal web user dataset and to fine-tune a saliency prediction model for web page saliency prediction, focusing on identifying potential differences in gaze behavior between males and females."*

**Hipótesis:**
- Subiabre (informal): *"este trabajo se basa en la hipótesis de que a pesar de la conciencia y control que se tiene sobre los gestos faciales, es posible clasificar las emociones y el nivel de atención que una persona experimenta al exponerse a contenidos multimedia a partir de su cara y expresiones."*
- Saffie (formal H0/HA): *"HO: No existen diferencias notables en la parte superior e inferior del rostro, que permitan predecir mejor algunas emociones."*
- Villanueva (formal, con hipótesis nula explícita): *"Significant differences exist in visual attention distribution patterns between males and females, evidenced by the intrinsic characteristics of their respective saliency maps."*

## Cómo se compara mi propio borrador ([[Estructura Tesis]])
- Mi estructura ya separa "Estado del Arte" del Marco Teórico como capítulo propio — igual que **Villanueva** (es la minoría, 1/6, pero es una opción válida y ya la tengo planificada).
- Mi metodología menciona "Metodología KDD" — coincide con el enfoque de **Saffie** (framework explícito), a diferencia de Subiabre/López/Villanueva que van con lista de pasos ad hoc.
- Mi hipótesis central en [[Problema e hipótesis]] está en formato de prosa, similar a Subiabre/López. La nota incluye una hipótesis nula asociada para orientar su contraste, sin reemplazar la formulación definida por el investigador.
- Aún no he decidido estilo de citación (IEEE vs. APA numerado) — ambos son válidos en el programa.

## Notas relacionadas
- [[Estructura Tesis]]
- [[Problema e hipótesis]]
- [[Etiqueta Atencion]]
- [[Etiqueta Emocion]]
