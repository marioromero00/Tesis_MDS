# Problema e hipótesis de investigación

> [!info] Alcance de esta versión
> Actualizada el 10-08-2026 para la **Toma de Muestra 2**, que contiene EEG, GSR,
> Eye Tracking y Pupilometría. No existe señal de expresión facial en este dataset.
> El uso de **arousal/activación** como alcance operacional de “emoción” sigue pendiente
> de confirmación con el profesor guía. Por eso, las formulaciones relativas a arousal
> deben entenderse como una propuesta de alcance, no como una decisión cerrada.

## Planteamiento del problema

La atención y la activación emocional cambian durante una sesión de navegación web. Sin
embargo, resumir las señales neurofisiológicas y conductuales mediante promedios o medianas
produce una representación estática que elimina el orden de las observaciones. Dos sesiones
con trayectorias distintas pueden quedar descritas por el mismo vector agregado: una puede
mantener un nivel estable de atención y otra presentar una caída progresiva, aunque ambas
tengan el mismo promedio.

El problema no se resuelve agregando más modalidades de manera directa. EEG, GSR, Eye
Tracking y Pupilometría registran manifestaciones diferentes y tienen frecuencias, escalas y
latencias distintas. La literatura consolidada en [[Conocimiento Presentaciones Pasadas]]
muestra que la ganancia multimodal depende de cómo se integran las señales. En particular,
un trabajo previo del grupo no obtuvo una mejora significativa mediante fusión tardía de
EEG y GSR en contexto web. Este antecedente justifica comparar estrategias de fusión
temprana, intermedia y tardía en vez de asumir que una de ellas es superior.

Existe además una dificultad de medición: la Toma de Muestra 2 no contiene una etiqueta
directa y continua de atención o activación emocional. Eye Tracking informa principalmente
qué fue **Observado**, pero mirar una zona no demuestra que haya sido **Atendida**. GSR
registra activación simpática, pero no informa la valencia ni permite identificar emociones
discretas. Por lo tanto, el trabajo requiere pseudoetiquetas cuyos alcances y errores deben
quedar incorporados al diseño experimental.

Esta tesis aborda el problema mediante modelos multimodales que conservan la secuencia de
las observaciones y separan las señales que construyen cada pseudoetiqueta de las señales que
intentan predecirla. El aporte se concentra en la **temporalidad** y en el **tipo de fusión**,
no en afirmar que una modalidad aislada mide directamente los estados internos del usuario.

## Brecha de investigación

De acuerdo con la revisión registrada en [[Estructura Tesis]] y
[[Conocimiento Presentaciones Pasadas]], el trabajo se sitúa en tres brechas:

1. Las señales suelen transformarse en vectores estáticos, perdiendo transiciones y
   dependencias entre ventanas consecutivas.
2. La incorporación de varias modalidades no garantiza una mejora: el efecto de la fusión
   temprana, intermedia o tardía debe compararse manteniendo constante la variable objetivo.
3. Las trayectorias intra-sesión suelen quedar fuera del análisis cuando las señales se
   resumen mediante estadísticos agregados.

## Propuesta de investigación

El diseño sigue una arquitectura de dos etapas. Un *Modelo Profesor* construye una
pseudoetiqueta por ventana temporal. Un *Modelo Estudiante* recibe señales diferentes e
intenta predecir esa pseudoetiqueta. La separación evita que el modelo aprenda a reproducir
directamente la regla con que se definió su variable objetivo.

| Constructo | *Modelo Profesor* | Pseudoetiqueta | *Modelo Estudiante* |
|---|---|---|---|
| Atención | Eye Tracking + Pupilometría | *Attention Score* | EEG + GSR |
| Arousal/activación | GSR | *Arousal Score* | EEG + Eye Tracking + Pupilometría |

En ambos casos, las entradas del *Modelo Profesor* y del *Modelo Estudiante* son disjuntas
para una misma variable objetivo. Esta regla de no-circularidad es innegociable. El detalle
del diseño y de sus decisiones abiertas está en [[Resumen Diseño Etiquetas y Modelos]],
[[Etiqueta Atencion]] y [[Etiqueta Emocion]].

## Hipótesis de investigación

> **Hipótesis:** Los modelos temporales multimodales obtienen un mejor desempeño fuera de
> muestra que los modelos estáticos comparables en la detección de emociones y atención
> durante la navegación web.

Esta formulación es la hipótesis central de la tesis. Emociones y atención son los dos
resultados sobre los que se contrasta la misma proposición; no constituyen hipótesis
independientes.

### Operacionalización

| Resultado | Variable objetivo | Entradas del *Modelo Estudiante* | Comparación |
|---|---|---|---|
| Atención | *Attention Score* construido con Eye Tracking + Pupilometría | EEG + GSR | Temporal multimodal vs. estático comparable |
| Emociones | *Arousal Score* construido con GSR, si se confirma este alcance | EEG + Eye Tracking + Pupilometría | Temporal multimodal vs. estático comparable |

La fila de emociones depende de que el profesor guía confirme que el constructo puede
operacionalizarse como arousal/activación. GSR no permite detectar valencia ni emociones
discretas, por lo que esa decisión afecta la validez del constructo, aunque no cambia la
redacción de la hipótesis definida por el investigador.

La hipótesis nula asociada establece que, bajo el mismo protocolo, los modelos temporales
multimodales no obtienen un mejor desempeño fuera de muestra que los modelos estáticos
comparables. El tipo de fusión se trata como un factor experimental. Se compararán fusión
temprana, intermedia y tardía, pero no se postula de antemano cuál será superior porque las
notas actuales no contienen evidencia suficiente para sostener una hipótesis direccional
entre ellas.

Para contrastar la hipótesis, cada comparación debe conservar:

- la misma pseudoetiqueta del *Modelo Profesor*;
- las mismas modalidades de entrada para el baseline y el modelo temporal de cada tarea;
- la misma partición por participante y las mismas ventanas de evaluación;
- el mismo preprocesamiento y las mismas métricas;
- ajuste de normalización, umbrales y cualquier transformación utilizando solo datos de
  entrenamiento.

La métrica primaria, la prueba estadística y el número de repeticiones aún deben definirse en
la metodología. Una diferencia aislada en una partición no bastará para sostener la
hipótesis: la mejora deberá ser consistente fuera de muestra y reportarse con su
incertidumbre.

## Criterios de interpretación

| Resultado | Interpretación |
|---|---|
| Los modelos temporales superan a los estáticos en emociones y atención | Evidencia a favor de la hipótesis |
| La ventaja aparece solo en uno de los dos resultados | Evidencia mixta; la hipótesis recibe apoyo parcial |
| No existe una ventaja consistente en ninguno de los dos resultados | No hay evidencia para sostener la hipótesis |
| Una estrategia de fusión supera a otra | Resultado comparativo sobre fusión; no demuestra por sí solo la hipótesis |

## Análisis complementario

La evolución intra-sesión de los scores puede analizarse para identificar patrones
compatibles con fatiga o habituación, pero ese análisis **no constituye una segunda
hipótesis**. Si se incorpora, debe realizarse con scores continuos y sin interpretar una
caída como diagnóstico o atribución causal en ausencia de una medida externa.

## Supuestos y amenazas a la validez

1. **Calidad de las pseudoetiquetas.** El desempeño del *Modelo Estudiante* está limitado
   por la calidad de la regla del *Modelo Profesor*.
2. **Validez de constructo de atención.** Eye Tracking mide observación; la Pupilometría
   agrega un proxy cognitivo, pero no convierte el *Attention Score* en una medición directa
   de atención.
3. **Confusión por luminancia.** El diámetro pupilar puede variar por el brillo del estímulo.
   La corrección lumínica depende de verificar si se conservaron las páginas o capturas
   observadas por cada participante.
4. **Alcance del arousal.** GSR permite aproximar activación simpática, no valencia ni
   categorías emocionales.
5. **Latencia de GSR.** La ventana o el desfase del *Arousal Score* debe considerar la
   latencia de la respuesta SCR; esta decisión sigue abierta.
6. **Dependencia entre ventanas.** El solapamiento del 50 % produce ventanas cercanas muy
   similares. La separación de entrenamiento y evaluación debe hacerse por participante para
   evitar fuga de información.
7. **Diferencias individuales.** Las líneas base fisiológicas varían entre personas; los
   parámetros de normalización deben estimarse sin utilizar el conjunto de evaluación.

## Relación con el resto de la tesis

- [[Tesis_MDS]] — estado general y decisiones vigentes.
- [[Estructura Tesis]] — ubicación de las hipótesis en el manuscrito.
- [[Resumen Diseño Etiquetas y Modelos]] — diseño comparativo de ambas tareas.
- [[Etiqueta Atencion]] — construcción del *Attention Score*.
- [[Etiqueta Emocion]] — propuesta de construcción del *Arousal Score*.
- [[Modelo Profesor - Decisiones]] — decisiones metodológicas propuestas y pendientes.
- [[Referencia Tesis Previas]] — formas de presentación de hipótesis aceptadas en tesis del
  mismo grupo.
