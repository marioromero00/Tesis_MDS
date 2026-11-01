# Modelo Profesor — resolución de las decisiones abiertas

> Documento de trabajo iniciado el 08-08-2026. Aborda las decisiones que
> [[Etiqueta Atencion]] y [[Etiqueta Emocion]] dejan marcadas como pendientes.
> **Nada de aquí está confirmado con el profesor guía.** Son propuestas con su
> justificación, para llegar a la reunión con una posición y no con una pregunta abierta.

El principio que ordena todo el documento: donde no hay evidencia para fijar un parámetro,
**no se elige arbitrariamente — se convierte en un análisis de sensibilidad.** Si la etiqueta
resiste dos criterios razonables, la decisión deja de ser un punto débil de la defensa.

---

## 1. Dos problemas que no estaban registrados

### 1.1 El confound lumínico puede dominar la componente pupilar

Este es el riesgo más serio del profesor de atención y hoy figura en [[Etiqueta Atencion]]
solo como una fila de la tabla de riesgos ("pupila responde a luz ambiental").

El orden de magnitud importa. La respuesta pupilar evocada por tarea (*task-evoked pupillary
response*) está en el rango de **0,1–0,5 mm**. La respuesta a cambios de luminancia puede ser
de **varios milímetros**. En navegación web el estímulo cambia de página, de fondo y de zona
mirada todo el tiempo.

**Si no se corrige, la "dimensión cognitiva" de la etiqueta puede estar midiendo,
principalmente, el brillo de la pantalla.** Eso no es un detalle de preprocesamiento: es una
amenaza directa a la validez de constructo del Attention Score.

**Propuesta —** hay una corrección disponible que este dataset permite y que muchos trabajos
no pueden aplicar: el eye tracking entrega la **posición de la mirada**, y los estímulos son
páginas web que se pueden re-renderizar. Entonces:

1. Reconstruir el estímulo visible en cada instante (captura de la página).
2. Calcular la **luminancia local en el punto de mirada** — promedio ponderado en una ventana
   de unos pocos grados de ángulo visual alrededor de la fijación.
3. Regresar el diámetro pupilar contra esa luminancia local (y su derivada, por la latencia del
   reflejo fotomotor) y **quedarse con el residuo** como componente cognitiva.

El residuo, no el diámetro crudo, es lo que entra al Attention Score.

**Si la reconstrucción del estímulo no es viable**, la alternativa mínima es corrección por
línea base sustractiva respecto de una ventana previa al estímulo, y **declarar el confound
como limitación explícita**. Es más débil, pero es honesto.

- [ ] **Verificar primero:** ¿se guardaron las capturas o la identidad de las páginas
      navegadas por participante? Sin eso, la opción 1 no existe. Esto bloquea la decisión.

### 1.2 La discretización por participante puede invalidar el análisis de tendencias

[[Etiqueta Atencion]] propone discretizar por **terciles de la distribución de cada
participante**. Hay una interacción con el posible análisis complementario de
fatiga/habituación que no estaba anotada.

Si los terciles se calculan sobre **toda la sesión**, por construcción queda exactamente un
tercio de ventanas en cada categoría. Eso **impone** una distribución fija: si un participante
no mostró ninguna caída de atención, el procedimiento igual va a etiquetar su último tercio
como "baja". Y si la caída fue brutal, la comprime al mismo tercio.

O sea: el instrumento con el que se mide la fatiga ya trae la fatiga incorporada. Un revisor
puede objetar que el análisis es circular.

**Propuesta — separar el uso de la etiqueta según el propósito:**

| | Contraste de la hipótesis central | Análisis complementario de tendencias |
|---|---|---|
| Forma de la etiqueta | **Discretizada** (clasificación) | **Score continuo** (tendencia) |
| Por qué | La hipótesis compara arquitecturas contra una etiqueta fija; discretizar tolera ruido | El análisis es sobre la *trayectoria*; discretizar por terciles la destruiría |
| Baseline de normalización | Calculado solo en entrenamiento | Ventana de calibración inicial, no la sesión completa |

Esto además resuelve limpiamente la tensión: la discretización deja de ser una decisión global
y pasa a ser una decisión del experimento que contrasta la hipótesis central.

---

## 2. Fusión del Attention Score

**El problema real:** no hay ground truth para ajustar pesos entre la componente ocular y la
pupilar. Cualquier peso elegido a mano es atacable en la defensa.

**Propuesta — no elegir pesos. Reportar dos fusiones y comparar:**

- **Primaria — promedio de z-scores con peso igual.** Cero parámetros libres. Es la opción
  defendible por ausencia de información: sin evidencia para ponderar, ponderar igual es la
  postura neutral, no una elección arbitraria.
- **Sensibilidad — primera componente principal** de las features normalizadas. Los pesos
  salen de la estructura de covarianza de los datos, no de una decisión. Se interpreta como
  la varianza común entre la dimensión espacial y la cognitiva.

**Criterio de decisión:** calcular la correlación de rangos entre ambos scores. Si es alta, la
etiqueta es **robusta a la elección de fusión** y eso se reporta como fortaleza. Si es baja,
hay información real en desacuerdo entre las dos señales, y eso es un hallazgo que hay que
investigar antes de seguir — no un parámetro que tunear.

Este mismo criterio aplica al Arousal Score de [[Etiqueta Emocion]] al combinar features de SCR y SCL.

---

## 3. Normalización: por participante

**Propuesta: por participante**, con una precisión que la nota original no hace.

El argumento es directo: la línea base pupilar y de fijación varía enormemente entre personas
por razones que no tienen nada que ver con atención —edad, agudeza visual, tamaño pupilar
basal—. Sin normalizar, el score mide principalmente *quién es el participante*.

**La precisión que falta:** los parámetros de normalización (media, desviación, umbrales)
deben calcularse **solo con datos de entrenamiento**, no con la sesión completa. Calcularlos
sobre todo el dataset y luego partir en train/test filtra información del conjunto de prueba
hacia la etiqueta. [[Etiqueta Atencion]] ya lo dice para los umbrales, en la tabla de riesgos;
falta decirlo también para la normalización, y aplicarlo.

Y la partición train/test debe ser **por participante**, no por ventana. Ventanas del mismo
participante con 50% de solapamiento son casi idénticas: repartirlas entre train y test
produciría un desempeño inflado que no se sostiene.

---

## 4. Ventana de agregación para GSR

Pendiente heredado de [[Etiqueta Emocion]]: la ventana de 2 s viene del preprocesamiento EEG,
pero la respuesta de conductancia (SCR) tiene latencia de **1–5 s** respecto del estímulo.

Una ventana de 2 s es **más corta que la latencia de la propia respuesta que quiere medir**.
La activación de la ventana *t* aparecerá en la ventana *t+1* o *t+2*.

**Propuesta:** desacoplar la ventana de la etiqueta de la ventana del modelo.

- Mantener 2 s con 50% de solapamiento para las **features de entrada** del estudiante — esa
  ventana viene de la dinámica del EEG y está bien fundamentada.
- Para el **Arousal Score**, agregar GSR en una ventana más larga y **desplazada**: del orden
  de 4–6 s, con un retardo aplicado que compense la latencia de la SCR.
- El desplazamiento exacto no se elige a ojo: se estima por **correlación cruzada** entre la
  serie de SCR y los onsets de estímulo, y se toma el retardo que la maximiza.

Así el retardo se estima desde los datos y queda justificado.

---

## 5. Qué necesita al profesor y qué no

| Decisión | Estado | Bloquea a |
|---|---|---|
| Redefinir emoción como arousal | **Requiere profesor** | Todo el diseño de [[Etiqueta Emocion]] |
| ¿Existe validación externa de la etiqueta? | **Requiere profesor** | Paso 5 de [[Etiqueta Atencion]] |
| ¿Se guardaron los estímulos navegados? | **Requiere verificar en los datos** | Corrección lumínica (§1.1) |
| Fusión: igual vs. PCA | Resuelto — se reportan ambas | — |
| Discretización | Resuelto — separada por propósito (§1.2) | — |
| Normalización por participante | Resuelto — con partición por participante | — |
| Ventana GSR | Resuelto — retardo estimado por correlación cruzada | — |

De las siete decisiones abiertas, **cuatro se pueden cerrar sin esperar al profesor**. Las tres
restantes son las que conviene llevar a la reunión del 10-08.

---

## Pendiente de este documento

- [ ] Verificar en los datos si existe registro del estímulo por participante (§1.1).
- [ ] Revisar si la literatura del grupo ya fijó un criterio de corrección lumínica.
- [ ] Contrastar la propuesta de ventana GSR con [[Etiqueta Emocion]] y actualizar esa nota
      si se acepta.

## Notas relacionadas
- [[Etiqueta Atencion]]
- [[Etiqueta Emocion]]
- [[Resumen Diseño Etiquetas y Modelos]]
- [[Tesis_MDS]]
- [[presentacion 10-08-26]]
