# Avances Tesis — 22-08-2026

Punteo fuente del deck `presentacion-22-08-26.html`, en esta misma carpeta. 10 diapositivas,
navegables con flechas desde el navegador; tecla `P` para modo lista.
**Si cambias el contenido, cámbialo aquí primero.**

Formato institucional: fondo blanco, franja azul superior, identidad Universidad de Chile /
Magíster en Data Science en portada y pie. Las cuatro señales llevan color y forma propia
(cuadrado, rombo, triángulo, círculo), de modo que se distinguen sin depender del matiz.
Textos revisados con [[no-ai-slop]].

Fuentes: [[Estructura Tesis]] (Cap. 1), [[Avance - 22-08-2026 (Frecuencia EEG y Limpieza de Expresion Facial)]],
[[Resumen Diseño Etiquetas y Modelos]], [[Avance EDA y Sincronizacion - 15-08-2026]].

---

## 1. Portada
- **Título:** Avances Tesis
- **Subtítulo:** Detección de atención y activación emocional durante la navegación web a partir de señales neurofisiológicas.
- Chips: EEG · GSR · Pupilometría · Eye Tracking
- Bloque de identificación: Estudiante (Mario Romero) · Profesor guía (Dr. Juan D. Velásquez) · Proyecto (Fondecyt 1231122) · Fecha (22 de agosto de 2026)

---

## 2. Contexto general
- **Título:** Atención y activación medidas durante la navegación
- El trabajo se enmarca en el proyecto Fondecyt 1231122, que estudia las respuestas neurofisiológicas durante la interacción con contenidos digitales.
- Los métodos clásicos de evaluación de experiencia de usuario (cuestionarios, *usability testing*, autorreporte) son retrospectivos y dependen del recuerdo del usuario.
- Las señales neurofisiológicas permiten observar durante la interacción misma, pero la literatura previa las resume en promedios por sesión y pierde la dinámica temporal.
- Chips con la ficha técnica: EEG (16 canales, 125 Hz) · GSR (Tobii Pro, ~8 Hz efectivos) · Pupilometría (Tobii Pro, 60 Hz) · Eye Tracking (fijaciones y sacadas).
- Callout — **Hipótesis central:** los modelos temporales multimodales obtienen un mejor desempeño fuera de muestra que los modelos estáticos comparables en la detección de emociones y atención durante la navegación web.

---

## 3. Objetivo general
- Cita destacada: "Desarrollar y evaluar modelos temporales multimodales para la detección de emociones y atención durante la navegación web, comparando su desempeño fuera de muestra con modelos estáticos comparables y analizando distintas estrategias de fusión multimodal."
- Callout: la etiqueta se mantiene fija en todas las comparaciones, de modo que cualquier diferencia de desempeño se atribuye al modelo y no al etiquetado.

---

## 4. Objetivos específicos
1. Sistematizar el estado del arte, con foco en dinámica temporal y estrategias de fusión.
2. Construir el corpus multimodal sincronizado, con criterios de calidad por participante, sesión y canal.
3. Diseñar las pseudoetiquetas mediante modelos profesor, sin circularidad entre señales.
4. Desarrollar los modelos temporales (LSTM, TCN, Transformer) y el baseline estático comparable.
5. Comparar fusión temprana, intermedia y tardía, y cuantificar cada modalidad mediante *ablation*.
6. Analizar la evolución intra-sesión de los scores: fatiga y habituación.
7. Contrastar los resultados con la hipótesis y establecer alcances y limitaciones.

---

## 5. Estado actual
- **Título:** Cuatro avances desde la última presentación

| Avance | Resultado |
|---|---|
| Capítulo 1 incorporado al manuscrito | Objetivos, alcances, limitaciones y contribuciones escritos, con la forma calibrada contra seis memorias previas del grupo |
| EDA de las cuatro señales | EEG 45/48 sesiones utilizables · GSR 47/49 grabaciones · pupilometría 90,25 % con ambos ojos válidos · mirada 94,98 % válida, 122.302 fijaciones |
| Coordinación temporal de las señales | 47 pares EEG–Tobii sobre reloj UTC común, conservando frecuencias nativas. Quedan P29 con offset y `Test_Participant` sin pareja directa |
| Arquitectura de etiquetas definida | Esquema Profesor → Estudiante con partición disjunta, tras descartar el clasificador facial por no existir en este dataset |

- Callout: el pipeline es reproducible y no modifica los archivos originales. El código y los datos viven fuera del manuscrito, y las notas los citan por nombre de archivo.

---

## 6. Arquitectura de etiquetas
- **Título:** Ninguna señal construye la etiqueta que después debe predecir
- Dos paneles con las señales reales, uno por variable. En cada uno: las señales del profesor
  arriba, flecha *construye* hacia abajo, el score al centro, flecha *se evalúa contra* hacia
  arriba, y las señales del estudiante abajo.

| | Modelo Profesor (construye) | Score | Modelo Estudiante (predice) |
|---|---|---|---|
| **Atención** | Eye Tracking + Pupilometría | Attention Score | EEG + GSR |
| **Arousal** | GSR | Arousal Score | EEG + Eye Tracking + Pupilometría |

- Callout: dentro de cada panel, ninguna señal aparece arriba y abajo a la vez. Sin esa separación, un buen desempeño sería indistinguible de que el modelo reconstruyó la regla de etiquetado.
- *Reemplazó al diagrama abstracto de señales A y B con `A ∩ B = ∅`: no se entendía sin explicarlo.*

---

## 7. Contribuciones
- **Quedan escritas pase lo que pase:**
  - Protocolo de pseudoetiquetas por partición disjunta de señales, aplicable a cualquier estudio multimodal sin *ground truth*.
  - Corpus multimodal sincronizado y documentado, con criterios explícitos de calidad.
  - Cuantificación del aporte marginal de cada modalidad y de la componente temporal.
- **Dependen del resultado:**
  - Evidencia sobre el rol de la temporalidad frente a baselines estáticos sobre la misma variable objetivo.
  - Evidencia sobre las estrategias de fusión, donde un trabajo previo del grupo no obtuvo mejoras con fusión tardía de EEG y GSR.
  - Evidencia sobre la evolución intra-sesión de atención y activación.
- Callout: las tres de la derecha dicen "evidencia sobre" y no prometen un hallazgo, de modo que un resultado nulo las mantiene en pie.

---

## 8. Limitaciones
- **Título:** Tres frentes, con su contramedida
- **Pseudoetiquetas:** el estudiante está acotado por la calidad de la regla del profesor; el eye tracking mide Observado y no Atendido; el GSR aproxima activación y no valencia. Ninguna etiqueta tiene validación externa, y por eso ambas se declaran como pseudoetiquetas.
- **Señales y sincronización:** sin triggers compartidos la alineación defendible es por reloj absoluto; las frecuencias nativas fijan la granularidad mínima; la latencia de SCR (1 a 5 s) puede exceder la ventana de 2 s, de modo que la ventana del GSR queda a validar.
- **Diseño e inferencia:** el solapamiento del 50 % genera dependencia entre ventanas, y por eso la partición es por participante; las líneas base varían entre personas, de modo que la normalización se estima sin el conjunto de evaluación; entorno de laboratorio, no navegación naturalista.

---

## 9. Próximos pasos
1. Preprocesar GSR, eye tracking y pupilometría. El EEG ya está especificado. *(pipeline)*
2. Recortar las ventanas comunes por evento con los manifiestos de sincronización. *(pipeline)*
3. Cerrar los umbrales de discretización de ambos scores. *(metodología)*
4. Validar la ventana de agregación del GSR contra la latencia de SCR. *(metodología)*
5. Implementar ambas etiquetas y entrenar los primeros baselines. *(modelamiento)*
- Callout: el Capítulo 2 sigue en desarrollo y los Capítulos 6 a 9 están en blanco. Los pasos 3 y 4 dependen de las decisiones de la lámina siguiente.

---

## 10. Preguntas
- **Título:** Cuatro decisiones que necesito cerrar
1. **¿Es aceptable redefinir "emoción" como *arousal*?** El GSR solo mide activación simpática. De esta decisión cuelgan el objetivo específico 3, el alcance 2 y la contribución 1.
2. **¿Aprueba el manifiesto de sincronización y los criterios de calidad?** Quedan P29 con offset y `Test_Participant` sin pareja directa.
3. **¿Rehago la búsqueda bibliográfica de la brecha 2?** Estaba formulada para la combinación con expresión facial; sin esa señal hay que re-verificarla antes de sostenerla.
4. **¿Cito *view independence* de co-training como antecedente?** La partición disjunta se le parece. Si corresponde, presento el aporte como adaptación a señales neurofisiológicas sin *ground truth*.

---

## Qué se sacó respecto de la versión anterior
- La portada "El Capítulo 1, cerrado" pasó a ser **Avances Tesis** con bloque institucional.
- Se eliminó la lámina de alcances ("Lo que esta tesis decide no hacer").
- Se eliminó el callout bajo los objetivos específicos (el que explicaba el objetivo 6).
- Se reemplazó la lámina "Dónde quedamos" por **Contexto general** al inicio y **Estado actual** después de los objetivos.
- Se eliminó la lámina de verificación de la frecuencia del EEG. La corrección sigue registrada en
  [[Avance - 22-08-2026 (Frecuencia EEG y Limpieza de Expresion Facial)]] y el dato correcto
  (125 Hz) aparece en la ficha técnica de la lámina de contexto.
- El diagrama abstracto A / B de la lámina 6 se reemplazó por dos paneles con las señales reales.

## Notas relacionadas
- [[Estructura Tesis]]
- [[Avance - 22-08-2026 (Frecuencia EEG y Limpieza de Expresion Facial)]]
- [[Resumen Diseño Etiquetas y Modelos]]
- [[presentacion 10-08-26]]
- [[Tesis_MDS]]
