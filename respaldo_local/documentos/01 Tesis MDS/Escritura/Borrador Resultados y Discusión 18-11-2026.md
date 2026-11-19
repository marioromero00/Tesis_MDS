# Borrador: Modelamiento, Resultados y Discusión

> [!info] Estado
> Borrador redactado el 18-11-2026 a partir de los informes de resultados del repositorio (rutas al final de cada sección). No reemplaza a [[Estructura Tesis]] ni cierra decisiones abiertas de [[Resumen Diseño Etiquetas y Modelos]]. Las cifras son AUC por persona salvo que se indique otra cosa. Revisar redacción, citas y numeración antes de pasar a LaTeX.

## Capítulo 6: Modelamiento y Experimento

### 6.1 Variables objetivo

Se usan dos pseudoetiquetas binarias por ventana de 2 s (paso de 1 s), construidas por un **Modelo Profesor** y predichas por un **Modelo Estudiante** con señales distintas, de acuerdo con la regla de no-circularidad.

- **Atención.** El *Attention Score* se obtiene como la primera componente principal de cinco variables de mirada y pupila (tiempo y duración de fijaciones, dispersión y recorrido de la mirada, pupila normalizada), ajustada con las 25 personas de entrenamiento. Cada ventana se clasifica como alta si supera la mediana de su persona. El *Modelo Estudiante* usa EEG y GSR.
- **Activación.** El *Arousal Score* se calcula a partir de cuatro componentes de GSR promediados sobre cinco ventanas consecutivas válidas (6 s). La versión utilizada (GSR V2) corrige un error de alineación de índices de la versión anterior, exige cobertura de al menos 50 % y deja sin etiqueta los empates con la mediana personal. Conserva 11.796 de 22.211 ventanas. El *Modelo Estudiante* usa EEG, mirada y pupila.

Ambas etiquetas son relativas a la sesión de cada persona y se calculan offline; describen el *Attention Score* y el *Arousal Score* definidos, no una medida externa de atención o activación. En el caso de atención, la etiqueta se apoya en lo **Observado** (mirada y pupila) como aproximación a lo **Atendido**, sin validarlo.

Fuentes: `resultados/profesor_binario_reconstruido_29-10-2026/INFORME.md`, `resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md`.

### 6.2 Representaciones y modelos

Para cada ventana se compara un modelo que recibe solo la ventana actual con el mismo modelo que recibe además un resumen del historial: media y desviación de las variables en las ventanas previas del mismo estímulo, hasta 32 ventanas. El historial se reinicia al cambiar de estímulo o ante huecos, y se construye con todas las ventanas válidas, tengan o no etiqueta. Como los estímulos son cortos, el historial efectivo promedia 7,8 ventanas en atención y 12,6 en activación.

Se usan dos familias: HistGradientBoosting (HGB), con el número de hojas elegido en validación interna de entrenamiento (7 en atención y 15 en activación), y una red recurrente GRU que recibe la secuencia ordenada, con configuración fija. Las tres estrategias de fusión (temprana, intermedia y tardía) se comparan con una misma familia (MLP).

### 6.3 Diseño de evaluación

La configuración se eligió solo con las 25 personas de entrenamiento y luego se congeló. Para estimar los efectos con más precisión se usó validación cruzada agrupada por persona sobre las 41 personas del análisis principal (8 grupos), de modo que ninguna persona aparece a la vez en ajuste y evaluación. La unidad de análisis es la persona: se calcula la AUC de cada persona y se comparan modelos con la diferencia pareada dentro de cada persona. La incertidumbre se estima con bootstrap por persona (20.000 réplicas) y una prueba de permutación de signos; los contrastes principales se corrigen por Holm.

Cada análisis se registró en el repositorio antes de ejecutarse, con sus reglas de decisión, y se ejecutó una sola vez. Dos auditorías de código detectaron problemas antes de evaluar (indicadores de faltantes ausentes en la fusión tardía y 1 s de solapamiento entre el historial desplazado y la etiqueta de activación), que se corrigieron con enmiendas registradas antes de ver resultados.

Las 16 personas de validación y test habían sido consultadas en etapas anteriores, por lo que los resultados son exploratorios: estiman efectos con más potencia, pero no constituyen una confirmación independiente.

Fuentes: `resultados/cierre_v3_16-11-2026/`, `resultados/cierre_final_41p_16-11-2026/protocolo.json`.

## Capítulo 7: Resultados

### 7.1 Efecto del historial

| Tarea | Sin historial | Con historial (hasta 32) | Diferencia | Personas que mejoran | p (Holm) |
|---|---|---|---|---|---|
| Atención | 0,684 | 0,710 | +0,026 [+0,018; +0,035] | 36/41 | < 0,001 |
| Activación | 0,529 | 0,563 | +0,034 [−0,001; +0,069] | 24/41 | 0,066 |

En atención, el historial mejora la predicción en 36 de 41 personas. El resultado se mantiene al reajustar el *Modelo Profesor* sin las personas evaluadas (+0,024) y con tres particiones alternativas (+0,026 a +0,030). En activación, la diferencia es de magnitud similar pero el intervalo de la partición registrada incluye cero; en las tres particiones alternativas es positivo (+0,042 a +0,043).

La red GRU, que sí usa el orden de las ventanas, no mejora sobre su propio control de una ventana en atención (+0,008 [−0,004; +0,020], intervalo del 90 % dentro de ±0,02) y rinde 0,040 por debajo del HGB con historial.

Fuentes: `resultados/cierre_final_41p_16-11-2026/INFORME.md`, `resultados/cierre_robustez_41p_16-11-2026/INFORME.md`.

### 7.2 Origen de la mejora

Para distinguir información temporal de otros efectos se compararon cuatro variantes frente al modelo sin historial:

| Variante | Atención | Activación |
|---|---|---|
| Historial real | +0,026 [+0,018; +0,035] | +0,034 [−0,001; +0,069] |
| Historial placebo (mismo número de ventanas, misma persona, otros estímulos) | +0,027 [+0,018; +0,035] | −0,004 [−0,030; +0,024] |
| Solo los segundos transcurridos en el estímulo | +0,028 [+0,021; +0,035] | −0,004 [−0,024; +0,017] |
| Historial sin las 6 ventanas más recientes | +0,008 [+0,002; +0,015] | +0,053 [+0,022; +0,083] |

**Atención.** El placebo reproduce completa la mejora del historial real (diferencia −0,000 [−0,003; +0,003]) y una sola variable, los segundos transcurridos en el estímulo, también la reproduce. Controlando esa variable, el historial no agrega nada (−0,002 [−0,006; +0,002]). La prevalencia de la clase alta de atención depende del tiempo dentro del estímulo: es 0,51 en el primer segundo, baja a 0,37 entre el segundo y tercer segundo y sube hasta 0,62 hacia los 12 s. Este análisis se motivó tras observar el placebo y se reporta como explicativo.

**Activación.** El historial que excluye las seis ventanas más recientes, sin solapamiento temporal con el *Arousal Score*, supera a un placebo equivalente en +0,046 [+0,018; +0,073] (28/41 personas; p Holm 0,004). Los segundos dentro del estímulo no aportan, y el historial agrega +0,038 [+0,002; +0,074] sobre ellos. La calibración con contexto de la persona (sus primeros minutos de sesión) no mejora ninguna de las dos tareas (+0,001 a +0,009).

Fuentes: `resultados/cierre_robustez_41p_16-11-2026/`, `resultados/ampliacion_41p_16-11-2026/` (incluye `enmienda_e1_lag6/`), `resultados/explicativo_posicion_41p_18-11-2026/`.

### 7.3 Tipos de fusión

| Tarea | Tardía − temprana | Intermedia − temprana | Intermedia − tardía |
|---|---|---|---|
| Atención | +0,012 [+0,005; +0,021] | +0,005 [−0,003; +0,013] | −0,008 [−0,014; −0,001] |
| Activación | +0,007 [−0,032; +0,042] | +0,002 [−0,019; +0,023] | −0,004 [−0,042; +0,039] |

En atención la fusión tardía supera a la temprana y a la intermedia; en activación no se observan diferencias. La arquitectura intermedia evaluada es más profunda que la temprana, por lo que la comparación incluye también una diferencia de capacidad.

### 7.4 Análisis descriptivos

- **Evolución en la sesión.** En atención, la AUC del modelo con historial pasa de 0,69 en el primer quinto de la sesión a 0,74 en el último. En activación, la proporción de ventanas de clase alta cae a 0,37 en el último quinto, un patrón compatible con habituación.
- **Importancia por bloques.** En atención, la caída de AUC al permutar el EEG es 0,207 y al permutar la GSR 0,004; la ventana actual pesa más que el historial, y las bandas theta y delta más que las restantes. En activación pesan el EEG (0,053) y la media del historial (0,050).
- **Tipo de página.** La atención se predice mejor en sitios web (0,71) y peor en textos (0,60 sin historial; 0,63 con historial).

Fuente: `resultados/ampliacion_41p_16-11-2026/INFORME.md`.

## Capítulo 8: Discusión

### 8.1 Respuesta a la hipótesis

Con los criterios de interpretación del manuscrito, el resultado corresponde a **evidencia mixta, con apoyo parcial**. El apoyo proviene de activación: la información de los segundos previos de EEG, mirada y pupila mejora la predicción del *Arousal Score*, aun excluyendo el intervalo que define la etiqueta y frente a un placebo de la misma persona. En atención, el modelo con historial es mejor, pero esa ventaja no es temporal en el sentido de la hipótesis.

### 8.2 Atención: una ventaja que no es temporal

La mejora en atención desaparece cuando se controla el tiempo transcurrido dentro del estímulo, y un historial armado con ventanas de otros momentos produce el mismo efecto. La lectura más coherente es que el *Attention Score* tiene una estructura sistemática al inicio de cada página (una caída a los 2–3 s seguida de un aumento), y que el modelo con historial la capturaba a través del largo del historial. Dado que la etiqueta se construye con fijaciones y pupila, este patrón podría reflejar la reorientación de la mirada y la respuesta pupilar al cambio de página, es decir, el nivel **Observado** más que el **Atendido**. Esto refuerza la cautela del diseño: la pseudoetiqueta de atención captura en parte la dinámica de exploración visual de cada página.

El modelo secuencial (GRU) no agregó información sobre el resumen estadístico del historial y rindió peor. Con 41 personas y estímulos breves (mediana de tres ventanas por segmento), la información disponible para aprender dependencias de orden es limitada.

### 8.3 Activación: información temporal con modelos débiles

En activación el historial sí aporta información que no se explica por la persona ni por la posición en el estímulo. Sin embargo, los modelos absolutos siguen cerca del azar (AUC alrededor de 0,56–0,57), y el *Arousal Score* depende de la latencia de la respuesta electrodérmica (1–5 s), por lo que es plausible que las señales de segundos previos anticipen la respuesta de GSR. El resultado es consistente con tratar la activación como un proceso dinámico, pero su utilidad práctica es baja con las variables actuales.

### 8.4 Fusión

La fusión tardía rindió mejor en atención, lo que sugiere que entrenar un modelo por señal y combinar sus salidas evita que el EEG, con muchas más variables, domine el ajuste conjunto. En activación ninguna estrategia de fusión se distinguió, coherente con el bajo desempeño general.

### 8.5 Limitaciones

- Las 16 personas de validación y test ya se habían consultado; los resultados con 41 personas son exploratorios.
- Las etiquetas son pseudoetiquetas offline, normalizadas con la sesión completa de cada persona, y no se validaron contra una medida externa. La normalización por sesión difiere de la redacción actual del manuscrito, que pide normalizar solo con entrenamiento.
- Varias variables (GSR y pupila normalizadas por sesión; componente tónica con filtro bidireccional) usan información de toda la sesión: el historial es causal por ventana, no por muestra.
- El análisis de posición dentro del estímulo es explicativo y post hoc.
- No se corrigió por multiplicidad en los contrastes secundarios.
- No se hizo búsqueda de hiperparámetros para la GRU ni para los MLP.

### 8.6 Trabajo futuro

- Confirmar el efecto temporal en activación con personas nuevas y un contraste definido de antemano (el cálculo de tamaño de muestra está en `resultados/protocolo_hipotesis_reintento_06-11-2026/`).
- Revisar la construcción del *Attention Score* al inicio de cada estímulo, o definir la etiqueta controlando el tiempo dentro de la página.
- Evaluar etiquetas normalizadas solo con información previa, para una versión utilizable en línea.

## Capítulo 9: Conclusiones

*(pendiente: depende de las decisiones con el profesor guía sobre el alcance de "emociones" frente a activación y sobre una posible cohorte nueva)*

## Notas relacionadas
- [[Estructura Tesis]]
- [[Problema e hipótesis]]
- [[Resumen Diseño Etiquetas y Modelos]]
