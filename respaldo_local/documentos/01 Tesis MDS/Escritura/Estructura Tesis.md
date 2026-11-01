# Estructura Tesis

Transcripción del esqueleto LaTeX de la tesis (borrador actual), con las secciones completables rellenadas a partir de la presentación de avances. Las secciones sin contenido real se marcan como *(pendiente)*.

## Capítulo 1: Introducción

### Contexto Problema
El desarrollo de plataformas digitales ha cambiado la forma en que las personas interactúan con contenidos, productos y otras personas.

Hoy en día, una parte no menor de las actividades laborales, comerciales y de entretenimiento se usa mediante interfaces digitales donde los usuarios están expuestos a información y estímulos. Es por esto que entender cómo las personas interactúan con plataformas digitales, cómo distribuyen su atención y qué emociones experimentan resulta relevante para el diseño de experiencias digitales más ad hoc a las necesidades del usuario.

### Descripción Proyecto
El presente trabajo se enmarca en el proyecto Fondecyt 1231122, dirigido por el Dr. Juan D. Velásquez y codirigido por la Dra. Flavia Guiñazú. El foco de este proyecto es comprender y adaptar las experiencias digitales mediante el análisis multimodal de respuestas neurofisiológicas, incluyendo señales EEG, seguimiento ocular, respuesta galvánica de la piel y expresiones faciales.

Particularmente, esta investigación trabaja sobre la **Toma de Muestra 2** del proyecto, que registra cuatro de esas señales: **EEG, GSR, eye tracking y pupilometría**. La expresión facial fue registrada en la Toma de Muestra 1 y es utilizada por otras tesis del grupo, pero **no está disponible en este dataset**; el diseño de esta tesis se construye por completo sobre las cuatro señales anteriores para identificar patrones asociados a atención y activación emocional durante la interacción con contenidos digitales (navegación web).

### Hipótesis de Investigación
- **Hipótesis:** Los modelos temporales multimodales obtienen un mejor desempeño fuera de muestra que los modelos estáticos comparables en la detección de emociones y atención durante la navegación web.

(Detalle en [[Problema e hipótesis]])

### Preguntas de Investigación
*(pendiente)*

### Objetivos
*(22-09-2026 — formulación científica revisada a solicitud de Mario. Reemplaza la redacción del 17-08-2026 y coincide con la presentación del tema. Ver [[Avance - 22-09-2026 (Objetivos Cientificos y Metodologia KDD)]].)*

#### Objetivo General
Evaluar si la información temporal y la fusión multimodal mejoran la predicción de pseudoetiquetas de atención y activación emocional durante la navegación web, comparando modelos temporales y estáticos en participantes no utilizados para su ajuste.

#### Objetivos Específicos
1. Revisar la literatura sobre atención y activación emocional, con énfasis en modelos temporales y fusión de señales.
2. Caracterizar las señales disponibles y sincronizar EEG, GSR, eye tracking y pupilometría con criterios de calidad definidos.
3. Definir las pseudoetiquetas continuas y categóricas de atención y activación, comprobar su estabilidad y separar las señales de etiquetado y predicción.
4. Comparar modelos temporales y estáticos en participantes no usados para su ajuste, seleccionando hiperparámetros dentro del entrenamiento.
5. Medir el aporte de señales e historial mediante estudios de ablación y comparaciones entre fusión temprana, intermedia y tardía.
6. Describir los cambios durante la sesión en los scores de atención y activación, buscando patrones compatibles con fatiga o habituación.
7. Contrastar la hipótesis a partir de las diferencias de desempeño, sus intervalos de incertidumbre y la variación entre participantes.

> Se conserva el compromiso del objetivo 6: requiere mantener el score continuo además del discretizado ([[Etiqueta Atencion]], [[Etiqueta Emocion]]). Su alcance es descriptivo. Evaluar la estabilidad de las pseudoetiquetas no equivale a validar externamente los constructos ni autoriza a cambiarlas entre modelos comparados.

### Alcances y limitaciones
*Criterio de separación: **alcance** = recorte decidido; **limitación** = restricción sufrida.*

#### Alcances
1. **Datos y contexto.** Solo Toma de Muestra 2 (Fondecyt 1231122), navegación web en laboratorio. Sin nueva toma de muestras ni datasets externos. Cuatro señales: EEG, GSR, eye tracking, pupilometría. Sin expresión facial.
2. **Constructos.** Atención y activación emocional, ambos como pseudoetiquetas por ventana, no como medición directa. Sin valencia ni emociones discretas.
3. **Objeto de evaluación.** El *Modelo Estudiante*. El *Modelo Profesor* es infraestructura de etiquetado y no se evalúa por desempeño predictivo propio.
4. **Comparaciones.** Temporal vs. estático, y fusión temprana / intermedia / tardía. Arquitecturas ya establecidas; no se propone una nueva.
5. **Producto.** Modelos entrenados y evaluados offline. Sin sistema en tiempo real ni interfaz. *(Deducido, no consta en notas previas — confirmar.)*
6. **Delimitaciones explícitas.** No entrega recomendaciones de diseño web, no establece causalidad estímulo–estado, no pretende representar a la población general. El análisis de fatiga/habituación es descriptivo.

#### Limitaciones
**Pseudoetiquetas** — el estudiante está acotado por la calidad de la regla del profesor; eye tracking mide Observado y no Atendido; GSR aproxima activación y no valencia; no hay validación externa para ninguna de las dos etiquetas.

**Señales y sincronización** — sin triggers compartidos, la alineación defendible es por reloj absoluto y no submuestra; frecuencias nativas distintas imponen granularidad mínima; la latencia SCR (1–5 s) puede exceder la ventana de 2 s; la pupila responde a luminancia y la corrección depende de conservar las páginas observadas (pendiente de verificar).

**Diseño e inferencia** — el solapamiento del 50 % genera dependencia entre ventanas (partición por participante obligatoria); las líneas base fisiológicas varían entre personas y la normalización debe estimarse sin el conjunto de evaluación; el número de participantes limita la potencia estadística; entorno de laboratorio, no navegación naturalista.

> Los conteos de sesiones utilizables van al Cap. 5, no acá: siguen moviéndose ([[Avance EDA y Sincronizacion - 15-08-2026]]).

### Contribuciones del Trabajo
*Redactadas como entregables (forma de Villanueva), no como objetivos en pasado (forma de Subiabre).*

1. **Evidencia empírica sobre el rol de la temporalidad** en la detección de atención y activación durante navegación web, comparando fuera de muestra modelos temporales y baselines estáticos sobre la misma variable objetivo.
2. **Evidencia comparativa sobre estrategias de fusión** —temprana, intermedia y tardía— en un contexto donde un trabajo previo del grupo no obtuvo mejoras con fusión tardía de EEG y GSR, dejando abierto si el resultado se debía a la fusión o a la arquitectura.
3. **Un protocolo de construcción de pseudoetiquetas mediante partición disjunta de señales**, que asigna a cada variable objetivo un conjunto para construir la etiqueta y otro distinto para predecirla, de modo que el desempeño sea interpretable como información genuina y no como reconstrucción de la regla de etiquetado. Aplicable a cualquier estudio multimodal sin *ground truth*.
4. **Un corpus multimodal sincronizado y documentado**, con criterios explícitos de calidad por participante, sesión y canal.
5. **La cuantificación del aporte marginal de cada modalidad y de la componente temporal** mediante *ablation*, útil para decidir qué señales justifican su costo de registro.
6. **Una caracterización descriptiva de la evolución intra-sesión** de atención y activación, fenómeno que la literatura revisada no modela sistemáticamente.

> 1, 2 y 6 dicen "evidencia sobre", no prometen hallazgo: un resultado nulo las mantiene en pie. 3, 4 y 5 están garantizadas pase lo que pase con los modelos.
> Sobre la 3: revisar su parecido con el supuesto de *view independence* de co-training / aprendizaje multi-vista (fuera del vault, sin verificar). Si se sostiene, citarlo primero y presentar el aporte como adaptación a señales neurofisiológicas sin *ground truth*. La partición evita circularidad **por definición**, no la dependencia estadística entre modalidades — declararlo en limitaciones.

## Capítulo 2: Marco Teórico

### Interacción Humano-Máquina / Comportamiento usuario en entornos digitales
*(17-08-2026 — esqueleto con referencias tomadas de las bibliografías de López (2.1) y Saffie (2.1.1). **Ninguna está leída ni verificada: no citar sin abrir la fuente.**)*

#### Interacción Humano-Máquina
- Definición: área que estudia no solo la interfaz sino cómo la persona interactúa con el sistema, integrando técnica, psicología y ergonomía (Chao, 2009; Castro & Rodríguez, 2018).
- Alcance de los tres términos: *humano* = usuario o grupo; *computadora* = cualquier sistema con interfaz interactiva; *interacción* = comunicación vía dispositivos de entrada/salida (Selzer, 2018).
- Hito: estudio formal desde 1973 con el Xerox Alto, primera interfaz gráfica.
- Cuatro formas de interacción (Chao, 2009): imágenes, voz, datos e **interacción inteligente**. La cuarta —sensores biométricos, ondas cerebrales, información fisiológica— es donde se sitúa esta tesis.
- BCI: control de dispositivos desde actividad encefálica sin sistema nervioso periférico (Cornejo Plaza & Guiñazú — codirectora del proyecto).
- Eye tracking con uso consolidado en IHC y usabilidad (Jacob & Karn, 2003).

#### Experiencia Usuario (UX)
*(22-08-2026 — redactado. Referencias contrastadas contra las bibliografías de López y Saffie: la entrada bibliográfica y el uso que cada memoria les da están confirmados, **las fuentes primarias siguen sin leer**.)*

La norma ISO 9241-210 define la experiencia de usuario como "la percepción de una persona y
las respuestas que resultan del uso previsto de un producto, sistema o servicio" (González &
Marcos, 2013). La definición incorpora dos elementos que la usabilidad por sí sola no cubre:
lo que el usuario percibe y cómo responde ante el sistema. Ambos dependen de quién interactúa
y en qué contexto lo hace, de modo que una misma interfaz no produce la misma experiencia en
todos los usuarios. Por eso la optimización de una estructura web se plantea por segmento de
usuario, tamaño de pantalla y tipo de dispositivo, y no como una configuración única.

El propósito de estudiar la experiencia de usuario es mejorar la relación entre el usuario y
el producto mediante el análisis cualitativo y cuantitativo de su comportamiento, sus emociones
y sus actitudes (Hassan Montero, 2015). Esa doble entrada, conducta observable y estado interno,
es la que conecta la disciplina con el trabajo de esta tesis: el comportamiento se puede observar
directamente, mientras que el estado interno hay que inferirlo.

Aplicada al diseño web, la experiencia de usuario se apoya en cinco principios (Husseniy et al.,
2021):

1. **Jerarquía visual:** la forma en que se dispone el contenido en la página. El nivel más alto
   suele ser un menú desde el cual se accede a las secciones principales del sitio.
2. **Consistencia:** el usuario asume que un sitio se usa de manera similar a otros productos que
   ya conoce, lo que reduce el costo de aprendizaje frente a una interfaz nueva.
3. **Confirmación:** el sistema debe permitir verificar, confirmar y revertir las acciones antes
   de ejecutarlas.
4. **Control de usuario:** el usuario debe percibir que controla el sistema y que puede
   personalizar su experiencia según sus preferencias.
5. **Accesibilidad:** el diseño debe poder ser usado por la mayor cantidad de personas posible,
   incluidas las que tienen alguna discapacidad, considerando color, contraste, imágenes, texto
   y compatibilidad con tecnologías asistivas.

La experiencia web también incide en la conducta de compra. Constantinides (2004) distingue tres
fuerzas no controlables por el consumidor que lo llevan a adquirir un producto o servicio en
línea: sus factores demográficos, personales y culturales; los estímulos del marketing
tradicional; y la experiencia web. Esta última es la única que el diseño del sitio interviene de
forma directa. En Chile la exposición a estas interfaces es alta: el tiempo promedio diario de
uso de internet alcanza 8 horas y 31 minutos, frente a un promedio mundial de 6 horas y 40
minutos, lo que ubica al país en el quinto lugar a nivel mundial (Statista, 2024).

Medir la experiencia de usuario sigue siendo el punto débil de la disciplina. Los instrumentos
habituales son cuestionarios estandarizados y pruebas de usabilidad (Kushendriawan et al., 2021),
que se aplican una vez terminada la interacción y dependen de lo que el usuario recuerde y quiera
reportar. Entregan un valor agregado por sesión, útil para comparar sitios entre sí, pero que no
indica en qué momento de la navegación el usuario dejó de atender ni qué elemento provocó una
reacción. Las señales neurofisiológicas se registran de manera continua mientras la interacción
ocurre y no exigen que el usuario describa su propio estado. Wang (2024) propone integrar
reconocimiento emocional y seguimiento ocular en la evaluación de experiencia de usuario. Esta
tesis sigue esa dirección y estima atención y activación emocional por ventanas a lo largo de la
sesión, en lugar de resumir cada sesión en un valor único.

> Referencias de esta subsección, transcritas de las bibliografías de López ([16], [17], [18]) y
> Saffie ([134], [135], [137], [142]). Verificar contra la fuente primaria antes de citar:
> **González & Marcos (2013)**, *Responsive web design: diseño multidispositivo para mejorar la
> experiencia de usuario*, BiD 31 · **Hassan Montero (2015)**, *Experiencia de Usuario: Principios
> y Métodos* · **Husseniy, Abdellatif & Nakhil (2021)**, *Improving the Websites User Experience
> (UX) Through the Human-Centered Design Approach*, Journal of Design Sciences and Applied Arts
> 2(2), 24-31 · **Constantinides (2004)**, *Influencing the online consumer's behavior: the Web
> experience*, Internet Research 14(2), 111-126 · **Statista (2024, 12 sep.)**, *¿Cuántas horas al
> día pasamos conectados a internet?* · **Kushendriawan, Santoso, Putra & Schrepp (2021)**,
> *Evaluating user experience of a mobile health application 'Halodoc' using user experience
> questionnaire and usability testing*, Jurnal Sistem Informasi 17(1), 58-71 · **Wang (2024)**,
> *Enhancing User Experience Using a Framework Integrating Emotion Recognition and Eye-Tracking*,
> Highlights in Science, Engineering and Technology 85, 298-308.

> Pendientes de esta subsección:
> - **La definición ISO viene de segunda mano.** González & Marcos (2013) citan la norma; lo
>   correcto es citar ISO 9241-210 directamente y dejar a González & Marcos para el argumento
>   multidispositivo.
> - **El dato de Statista es de 2024** (versión que usa Saffie). Buscar la edición 2026 y
>   reemplazar las tres cifras, o declarar el año en el texto como está ahora.
> - **No** usar el "70 % de la información se obtiene por la vista" (Mandal, 2003) sin verificar el
>   original: cifra muy repetida y de procedencia floja.
> - La cifra de ventanas de dos segundos no se menciona aquí a propósito; el soporte temporal se
>   define en el Cap. 4. Si cambia, esta subsección no necesita edición.
> - Mantener "Interacción Humano-Máquina" como nombre y aclarar la sigla en el primer uso.

### Emociones Humanas
#### Naturaleza de las Emociones Humanas
*(pendiente)*

#### Evolución de las Teorías Emocionales
*(pendiente)*

#### Expresión de las Emociones
*(pendiente)*

#### Clasificación de las Emociones
*(pendiente — insumo preliminar en Estado del Arte: modelo discreto de Ekman (6 emociones básicas) y modelo dimensional de Russell (valencia-arousal))*

### Atención Humana
#### Definición de Atención
*(pendiente)*

#### Tipos de Atención
*(pendiente)*

#### Nivel de Atención
*(pendiente)*

#### Atención en Entornos Digitales
*(pendiente)*

### Señales Fisiológicas
#### Definición de Señales Fisiológicas
*(pendiente)*

#### Clasificación Sistema Nervioso
*(pendiente)*

#### Electroencefalograma (EEG)
*(pendiente)*

#### Respuesta Galvánica de la Piel (GSR)
*(pendiente)*

### KDD como Marco Teórico
#### Etapas de KDD
*(pendiente)*

#### KDD aplicado a detección y clasificación de emociones
*(pendiente)*

### EDA
#### Propósito EDA
*(pendiente)*

#### Visualización de Datos
*(pendiente)*

#### Estadística Descriptiva
*(pendiente)*

#### Distribución de Variables
*(pendiente)*

#### Tratamiento de Outliers
*(pendiente)*

#### Análisis de Correlación
*(pendiente)*

### Modelamiento
#### Propósito del Modelamiento
*(pendiente)*

#### Aprendizaje Automático
Existen cinco categorías de aprendizaje automático: aprendizaje supervisado, aprendizaje no supervisado, aprendizaje semisupervisado, aprendizaje autosupervisado y aprendizaje por refuerzo.

1. **Aprendizaje Supervisado:** tipo de aprendizaje de máquinas en el que se entrena el modelo con un conjunto de datos etiquetados, es decir, se conoce la variable objetivo. Comprende varios algoritmos: algoritmos de regresión, algoritmos de clasificación, clasificadores Naive Bayes, Bosques Aleatorios, etc.
2. **Aprendizaje No Supervisado:** tipo de aprendizaje de máquinas en el que se entrena al modelo con datos no etiquetados. Ejemplos son los modelos de clustering como k-means o el análisis de componentes principales (PCA).
3. **Aprendizaje Semisupervisado:** tipo de aprendizaje en que los modelos se entrenan con datos sin etiquetas, pero aprenden una parte de la entrada, generando automáticamente etiquetas, pasando así de no supervisado a supervisado.
4. **Aprendizaje Autosupervisado:** combina aprendizaje supervisado y no supervisado. Los algoritmos se entrenan con un pequeño conjunto de datos etiquetados y un gran conjunto sin etiquetar, donde los etiquetados guían el proceso de aprendizaje.
5. **Aprendizaje por Refuerzo:** algoritmo con sistema de recompensa y penalización; el agente es recompensado o penalizado en base a una métrica establecida, que con repetición mejora la estrategia.

##### Sobreajuste y Subajuste
La capacidad de generalización de un modelo es su desempeño para nuevos datos. Un modelo sobreajustado genera alta precisión en datos de entrenamiento, pero mal desempeño en nuevos datos; esto ocurre cuando los modelos memorizan ruido o datos específicos en vez de patrones generales. Además, conjuntos de datos de alta dimensión también pueden provocar sobreajuste — esto es conocido como "la maldición de la dimensionalidad", ya que a medida que aumentan las características, los datos se vuelven escasos aumentando la varianza.

Un modelo subajustado tiene mal desempeño tanto en datos de entrenamiento como de prueba, ya que no logra capturar los patrones que existen en los datos. Esto suele suceder en modelos simplistas.

Para lograr un ajuste óptimo, el modelo debe capturar los patrones subyacentes en los datos sin ser sensible a ruido o a fluctuaciones aleatorias. Tiene que haber equilibrio entre la complejidad del modelo y la generalización, equilibrando sesgo y varianza. Una forma de evaluar esto es mediante las curvas de aprendizaje.

#### Algoritmos Clásicos de Clasificación
*(pendiente — regresión logística, SVM, KNN, Random Forest, Gradient Boosting)*

#### Redes Neuronales
##### Arquitectura y Funcionamiento
*(pendiente)*
##### Backpropagation y Optimización
*(pendiente)*
##### Regularización
*(pendiente)*

#### Redes Neuronales Convolucionales (CNN)
##### Operación de Convolución
*(pendiente)*
##### Arquitecturas Relevantes
*(pendiente)*

#### Transformers y Vision Transformers (ViT)
##### Mecanismo de Atención
*(pendiente)*
##### Aplicación a Imágenes
*(pendiente)*

#### Aprendizaje por Transferencia
*(pendiente)*

#### Modelos Multimodales y Fusión de Fuentes
*(pendiente — ver Estado del Arte: fusión temprana/intermedia/tardía)*

#### División de Datos, Validación Cruzada y Ajuste de Hiperparámetros
*(pendiente)*

### Evaluación de Modelos
#### Propósito
*(pendiente)*
#### Matriz de Confusión
*(pendiente)*
#### Métricas Principales de Evaluación
*(pendiente)*
#### Métricas Agregadas para Clasificación Multiclase
*(pendiente)*
#### Curva ROC y AUC
*(pendiente)*
#### Consideraciones Prácticas
*(pendiente)*

### Detección Automática de Emociones
#### Definición
*(pendiente)*
#### Fuentes para Detectar Emociones
*(pendiente)*
#### Enfoques de Clasificación
*(pendiente)*
#### Pipeline de Detección
*(pendiente)*
#### Enfoque Multimodal
*(pendiente)*

### Detección Automática de Atención
#### Definición
*(pendiente)*
#### Fuentes para Detectar Atención
*(pendiente)*
#### Enfoques de Clasificación de Atención
*(pendiente)*
#### Pipeline de Detección de Atención
*(pendiente)*
#### Enfoque Multimodal
*(pendiente)*

### Consideraciones Éticas
*(pendiente)*

### Pseudo Etiquetas
*(pendiente — ver riesgos identificados en [[Atencion]]: pseudoetiquetas no son verdad absoluta, ruido en las etiquetas, riesgo de fuga de información entre entrenamiento y evaluación)*

## Capítulo 3: Estado del Arte

### Detección Automática de Atención
#### Detección Automática de Atención mediante EEG
Panorama y tendencia de arquitecturas multimodales recientes:

| Paper | Señales | Arquitectura | Principal aporte |
|---|---|---|---|
| TACOformer (2023) | EEG + GSR + ECG | Cross-Attention Transformer | Atención conjunta token–canal; SOTA en DEAP y DREAMER |
| Feng et al. (2025) | EEG + Facial | Multi-Head Self-Attention | Fusión adaptativa EEG–Facial (81.1% en MED-HI) |
| Milmer (2025) | EEG + Facial | Swin Transformer + Cross-Attention | Modelado temporal sobre secuencias faciales (96.7% en DEAP) |
| Wang et al. (2025) | EEG + Eye-Tracking | Cross-Modal Attention | Alineación entre actividad cerebral y movimiento ocular (90.6% en SEED-IV) |
| MuMTAffect (2025) | Gaze + Pupila + AU + GSR | Transformers por modalidad | Aprendizaje multitarea para emoción y personalidad |
| GBV-Net (2025) | EEG + GSR + ECG + Facial | Fusión jerárquica con compuertas | Integración profunda de señales visuales y fisiológicas |

**Modelamiento temporal — referencias clave por arquitectura:**
- LSTM: Saffie (2023) — EEG web.
- TCN: Bai et al. (2018); Kamrud et al. (2021) — EEG; Elmadjian et al. (2022) — eye-tracking.
- Transformer: Vaswani et al. (2017); MNT (2022) — EEG+PPG+GSR; TEREE (2025) — EEG+eye-tracking.

**Modelos de emoción (marco de referencia):** enfoque discreto (Ekman, 6 emociones básicas) y enfoque dimensional (Russell, valencia–arousal).

### Detección de fatiga y habituación
Zali-Vargahan et al. (2023): 95,3% con fusión CNN+Stockwell (EEG+fisio+facial). Saavedra (2024): sin mejora significativa con fusión tardía EEG+GSR en contexto web. La fatiga y habituación no están modeladas sistemáticamente como variable de interés en la literatura (brecha identificada).

### Pseudo etiquetas
*(pendiente desarrollo — ver Metodología > Definición Variable Objetivo y [[Atencion]])*

### Modelos profesores
Trabajos previos del grupo (Subiabre) usan un clasificador facial para generar etiquetas de atención, a partir de las cuales otro modelo aprende. Limitación general del enfoque: el modelo estudiante nunca podrá ser mejor que las etiquetas que recibe.

Esta tesis conserva el patrón profesor → estudiante pero **no el clasificador facial**, porque la señal no existe en la Toma de Muestra 2. El profesor de atención se construye con Eye Tracking + Pupilometría y el de activación con GSR ([[Resumen Diseño Etiquetas y Modelos]]).

### Enfoque multimodales
Estrategias de fusión multimodal:
- **Fusión Temprana:** todas las señales entran a un modelo único
- **Fusión Intermedia:** atención cruzada entre modalidades
- **Fusión Tardía:** modelo por modalidad + voto/promedio

La ganancia multimodal depende de la arquitectura de fusión, no solo de agregar modalidades.

### Brechas de investigación
1. Señales tratadas como vectores estáticos, sin dinámica temporal.
2. Fusión de EEG + GSR + eye tracking + pupilometría en contexto web: no encontrada en la literatura revisada. *(La brecha estaba formulada para la combinación con expresión facial; **re-verificar la búsqueda** para esta combinación antes de sostenerla en la defensa.)*
3. Fatiga y habituación no modeladas como variable de interés.
4. Sin ablation studies sistemáticos.

**Aporte de esta tesis:**
- Modelos secuenciales sobre EEG + GSR + eye tracking + pupilometría.
- Comparación de fusión early / intermediate / late.
- Análisis complementario de patrones compatibles con fatiga y habituación.
- Ablation study por modalidad y temporalidad.
- Baseline estático como control.

## Capítulo 4: Metodología

### Diseño de Investigación
Estudio cuantitativo y comparativo, con evaluación offline sobre los registros existentes de la Toma de Muestra 2. La comparación entre modelos temporales y estáticos busca estimar el aporte predictivo de la temporalidad y de la fusión multimodal a las pseudoetiquetas. Las particiones se establecen por participante; las ventanas de una persona no se distribuyen entre entrenamiento y evaluación de una misma comparación. El diseño no permite atribuir causalidad ni validar fisiológicamente las pseudoetiquetas.

### Metodología KDD
Se adopta **KDD (Knowledge Discovery in Databases)** como marco del trabajo. Fayyad, Piatetsky-Shapiro y Smyth (1996) describen un proceso iterativo que comprende la preparación de los datos, la minería y la interpretación de los patrones. La minería de datos es una etapa de ese proceso. Se adapta a esta tesis mediante cinco bloques de presentación:

| Etapa | Aplicación en la tesis |
|---|---|
| Selección | Delimitar participantes, sesiones y señales de la Toma de Muestra 2 según la pregunta de investigación. |
| Preprocesamiento | Auditar calidad, tratar datos faltantes y sincronizar EEG, GSR, eye tracking y pupilometría. |
| Transformación | Extraer características y pseudoetiquetas por ventana; construir secuencias y preparar representaciones para las fusiones. |
| Minería de datos | Ajustar modelos estáticos y temporales, estrategias de fusión e hiperparámetros mediante selección interna en entrenamiento. |
| Interpretación y evaluación | Comparar desempeño por participante, estimar incertidumbre, estudiar ablaciones y trayectorias intra-sesión, y documentar resultados y límites. |

La iteración entre etapas se realiza dentro del desarrollo. Para cada comparación se mantienen las mismas pseudoetiquetas y particiones, y se separan las señales del **Modelo Profesor** y del **Modelo Estudiante**. Las transformaciones aprendidas, incluidos escalado y PCA, se ajustan dentro del entrenamiento correspondiente. Se informa exactitud balanceada (BA), macro-F1 y recall por clase, junto con la variabilidad entre participantes. La evaluación final reservada no se utiliza para seleccionar configuraciones.

Esta formalización no convierte las búsquedas adaptativas ya realizadas en evidencia confirmatoria: sus comparaciones conservan el carácter exploratorio documentado en la bitácora. La normalización original por sesión también limita la interpretación en tiempo real. La estabilidad de las reglas de etiquetado y la validez externa de los constructos son cuestiones distintas.

**Fuente primaria consultada el 22-09-2026:** Fayyad, U., Piatetsky-Shapiro, G., & Smyth, P. (1996). *From Data Mining to Knowledge Discovery in Databases*. AI Magazine, 17(3), 37–54. [Texto en el sitio del autor](https://fayyad.com/from-data-mining-to-knowledge-discovery-in-databases/). DOI: [10.1609/aimag.v17i3.1230](https://doi.org/10.1609/aimag.v17i3.1230). Los cinco bloques son una síntesis adaptada; el artículo desarrolla el proceso en nueve pasos.

### Participantes
*(pendiente — ver EDA: 48 participantes registrados en la toma de muestras)*

### Fuentes de Información

#### EEG
Potencia por bandas (delta, theta, alpha, beta, gamma) y relaciones entre bandas.

#### GSR
- Número de picos (SCR)
- Amplitud de respuesta
- Nivel tónico (SCL)
- Variabilidad de la señal

#### Eye Tracking
- Número de fijaciones
- Duración promedio de fijaciones
- Amplitud y velocidad de sacadas
- Dispersión de la mirada

#### Pupilometría
- Diámetro pupilar por ojo y validez de la medición
- Dilatación relativa respecto de la línea base del participante
- *(Pendiente: corrección por luminancia de la página observada — ver limitaciones del Cap. 1.)*

### Definición Variable Objetivo

#### Definición Nivel de Atención
Se construye una pseudoetiqueta mediante un **Modelo Profesor**. Se evaluaron tres enfoques:

1. **Solo Eye Tracking:** índice de atención con reglas fisiológicas (duración de fijaciones, número de fijaciones, mirada dentro de áreas de interés, pérdida de mirada).
2. **Expresión facial:** clasificador facial que entrega la etiqueta de atención. **Descartado**: la señal no existe en la Toma de Muestra 2.
3. **Estimación multimodal:** Attention Score combinando Eye Tracking + Pupilometría, discretizado por persona.

**Decisión (08-08-2026): enfoque 3**, con pupilometría en lugar de expresión facial. Eye Tracking aporta la dimensión espacial y temporal; la pupilometría, la dimensión cognitiva como proxy de carga atencional. El Modelo Estudiante correspondiente usa EEG + GSR, de modo que ninguna señal que construye la etiqueta se reutiliza para predecirla. Detalle en [[Etiqueta Atencion]] y [[Resumen Diseño Etiquetas y Modelos]]; riesgos de la pseudoetiqueta en [[Atencion]].

> Sigue abierto el método de fusión de ambas señales y el umbral de discretización.

#### Definición Emoción
*(pendiente)*

#### Modelos Profesores
El **Modelo Profesor** de atención utiliza eye tracking y pupilometría; su **Modelo Estudiante** utiliza EEG y GSR. Para activación emocional, el profesor utiliza GSR y el estudiante EEG, eye tracking y pupilometría. Este es el diseño vigente para la Toma de Muestra 2, sin señal facial. Ver [[Resumen Diseño Etiquetas y Modelos]].

#### Pseudoetiquetas
Riesgos identificados: las pseudoetiquetas no son verdad absoluta, puede existir ruido en las etiquetas, y debe evitarse fuga de información entre entrenamiento y evaluación (ver [[Atencion]]).

### Preprocesamiento de Señales

#### Sincronización de Fuentes
*(pendiente)*

#### Preprocesamiento EEG
**Adquisición:** OpenBCI Cyton + módulo Daisy — 16 canales, 125 Hz, 24-bit ADC. *(Verificado contra los datos crudos el 22-08-2026: el Cyton muestrea a 250 Hz con 8 canales; con la Daisy para llegar a 16 el muestreo por canal baja a 125 Hz.)* Conversión de señal hex a µV (Vref = 4.5V, Gain = 24).

**Filtrado (Butterworth orden 4, fase cero):**
- Pasa-altos 1 Hz → elimina drift DC
- Pasa-bajos 40 Hz → elimina EMG
- Notch 50 Hz → elimina interferencia de red eléctrica

**Calidad y artefactos:** muestras > ±150 µV se descartan; canales clasificados como bueno / plano / ruidoso; solo los canales buenos ingresan al modelamiento.

**Segmentación:** ventanas de 2 s (250 muestras) con 50% de solapamiento (paso de 125 muestras); ventanas con >20% de NaN se descartan.

**Extracción de características (por época y canal, método de Welch):**
- Potencia absoluta y relativa en 5 bandas: δ (0.5–4 Hz), θ (4–8 Hz), α (8–13 Hz), β (13–30 Hz), γ (30–40 Hz).
- 7 índices inter-banda: carga cognitiva (θ/α), déficit atencional (θ/β), relajación (α/β), engagement (β/(α+θ)), fatiga mental ((α+θ)/β), ondas lentas ((δ+θ)/(α+β)), alto nivel cognitivo (γ/(δ+θ)).
- Asimetría hemisférica alpha (proxy de valencia emocional).
- Total: 273 features por época (160 potencias + 112 índices + 1 asimetría, × 16 canales).

#### Preprocesamiento GSR
*(pendiente)*

#### Preprocesamiento Eye Tracking
*(pendiente)*

#### Preprocesamiento Pupilometría
*(pendiente)*

### Extracción de Características
*(pendiente — detalle de EEG ya cubierto en Preprocesamiento EEG)*

### Modelos Considerados

#### Fusión de Modalidades
Comparación de fusión early / intermediate / late (ver Estado del Arte).

#### División de Datos
*(pendiente)*

#### Métricas de Evaluación
*(pendiente)*

## Capítulo 5: Análisis Exploratorio de Datos

### Descripción General del Conjunto de Datos
Fuente: "Toma de Muestras 2 - EEG raw".
- 48 participantes registrados.
- 16 canales EEG por participante.
- No se detectaron valores faltantes (NaN = 0).

### Duración y Registros
- Duración promedio de las grabaciones: 13,4 ± 1,5 minutos.
- Duración mediana: 13,1 minutos.

**Calidad de la señal:**
- 21 de 48 participantes presentan al menos un canal saturado.
- Mediana: 0 canales saturados (más de la mitad de los registros no presenta saturación).
- Promedio: 1 canal saturado por participante, concentrado en un grupo reducido de sujetos.
- Se identificó un pico de potencia cercano a 50 Hz, atribuible al ruido de la red eléctrica → se incorporará filtro notch durante el preprocesamiento.

## Capítulo 6: Modelamiento y Experimento
*(pendiente)*

## Capítulo 7: Resultados
*(pendiente)*

## Capítulo 8: Discusión
*(pendiente)*

## Capítulo 9: Conclusiones
*(pendiente)*

## Notas relacionadas
- [[Tesis_MDS]]
- [[Problema e hipótesis]]
- [[Atencion]]
