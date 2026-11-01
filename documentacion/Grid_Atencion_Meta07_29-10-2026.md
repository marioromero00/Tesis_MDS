# Grid e iteraciones para atención binaria, meta ROC-AUC > 0,70

Se conserva la definición 1 = score docente sobre la mediana personal, 0 = score menor o igual, y las etiquetas PCA de los cinco folds de participantes de la corrida reconstruida. La fuente, etiquetas, partición y métrica permanecen fijas; la meta se aplica a ROC-AUC promedio de 25 personas, con predicciones fuera de fold, no al rendimiento de entrenamiento ni a una persona seleccionada.

Se comienza por PCA porque fue la tarea más prometedora de rondas anteriores. Esta elección y la búsqueda reiterada sobre train hacen que los resultados sean exploratorios. La regla de parada al superar 0,70 no los convierte en una evaluación confirmatoria; no se evalúan validation, test ni P29.

## Rondas predefinidas

1. Grid HistGradientBoosting: contextos 1/8/32/128, máximo de hojas 7/15, iteraciones 200/600, regularización L2 10, tasa 0,05; dos escenarios de preprocesamiento. 32 combinaciones × cinco folds = 160 ajustes internos y diez modelos externos.
2. Grid CatBoost: contextos 1/8/32/128, profundidad 4/6, regularización L2 3/15, 500 iteraciones y tasa 0,05; dos escenarios. 32 combinaciones × cinco folds.
3. Refinamiento multiescala HistGradientBoosting: contextos máximos 32/128/256, hojas 15/31, L2 1/30 e iteraciones 400/1000; dos escenarios. 48 combinaciones × cinco folds.

Cada combinación se ajusta en 16 participantes y se puntúa en cuatro participantes internos. En el nivel interno, el profesor PCA se reconstruye con las personas de ajuste interno. La mejor configuración de cada escenario se reajusta en 20 participantes y evalúa en cinco participantes externos. Se reporta también una estrategia que escoge entre escenarios dentro del holdout interno. No se escoge configuración con resultados externos. Se conserva la limitación del holdout interno único y la reutilización adaptativa entre rondas.

## Escenarios distintos

- **Inductivo:** transformaciones logarítmicas fijas, imputación/escalado aprendidos únicamente con train. EEG y GSR como únicas fuentes de entradas.
- **Relativo offline:** antes del preprocesamiento aprendido se normalizan EEG/GSR con la media y desviación de la sesión completa no etiquetada de cada persona, también para personas externas. Esta es adaptación transductiva offline y requiere una sesión completa; no debe describirse como detector online ni como protocolo idéntico al inductivo. Se compara y reporta por separado.

Los resúmenes de historial incluyen media, desviación, mínimo, máximo, cambio y cambio por paso; se calculan únicamente con ventanas anteriores y actual, reiniciando al cambiar segmento o al encontrar huecos. La calibración personal offline usa ventanas futuras para estimar su referencia personal; por eso ese escenario no es causal en conjunto. No se incluyen mirada/pupila, etiquetas, scores docentes, identidad ni tiempo de sesión en las matrices predictoras.

Bootstrap descriptivo: 2.000 remuestreos de personas; semilla del helper histórico 20261031. Semilla de modelos nuevos: 20261101. Los parámetros, fuentes y versiones completas se guardan en cada protocolo. Los resultados anteriores se conservan.

```sh
.venv/bin/python -m unittest discover -s tests -p test_grid_atencion_meta07.py -v
.venv/bin/python scripts/grid_atencion_meta07.py --round 1
.venv/bin/python scripts/auditar_grid_atencion_meta07.py --round 1
```

Repetir con `--round 2` o `--round 3` para las rondas adicionales. Entorno reproducible en `requirements_grid_atencion_macos.lock.txt`.

## Iteración con características ampliadas

El grid adicional conserva etiquetas y particiones y añade únicamente características de EEG/GSR: número de muestras, cobertura y validez de ventana de ambas señales; log-razones theta/beta, alpha/beta, theta/alpha y beta/(alpha+theta). Son hipótesis de representación, sin afirmar que una razón equivalga a atención validada. Se mantienen excluidas todas las variables de mirada y pupila.

Se prueban 24 combinaciones de contextos 8/32, hojas 7/15 e iteraciones 200/400, con L2 5, en tres escenarios: sin calibración adicional, z personal offline y rangos personales offline. Este último aplica rango percentil por persona y función normal inversa; también necesita la sesión completa no etiquetada de la persona externa.

Ejecutar `scripts/grid_atencion_caracteristicas_ampliadas.py --round 1` y auditar con `scripts/auditar_grid_atencion_ampliado.py --round 1`. La consolidación `scripts/informe_busqueda_atencion_meta07.py` incluye solo métricas completas y auditadas, identificando las corridas parciales.

## Contraste retrospectivo separado

Se añade un grid de clasificación retrospectiva offline con el mismo profesor PCA, etiquetas, personas y folds, usando además ventanas EEG/GSR posteriores. Este escenario requiere conocer señales futuras de la sesión; no se interpreta como detección en tiempo real ni como cumplimiento de una meta causal.

Se prueban 24 combinaciones: contextos previos 8/32, ventanas posteriores 4/8/16, hojas 7/15, 300 iteraciones, L2 10 y tasa 0,05, con/sin z personal offline. El contexto posterior se limita al mismo segmento y participante, y se corta ante huecos. Incluye media, desviación, mínimo, máximo y cambio hacia el extremo posterior. No se usan etiquetas futuras como predictores; el uso de señales futuras se declara en protocolo.json y en los informes. Los tests verifican horizonte y límites de segmento.

Ejecutar `scripts/grid_atencion_retrospectivo.py --round 1` y auditar con `scripts/auditar_grid_atencion_retrospectivo.py --round 1`.

## Ejecución de folds en paralelo

El refinamiento multiescala de la ronda 3 usa `scripts/grid_atencion_meta07_worker.py --round 3 --fold N` para completar folds independientes, reutilizando exactamente las funciones del grid original y sus parámetros. Cada worker escribe solo archivos de su fold y guarda su hash en `worker_foldN.json`. El proceso serial inicial fue detenido conservando checkpoints para distribuir el trabajo. Al finalizar, el script original recorre los checkpoints, verifica hashes y genera la evaluación agregada. La paralelización no cambia grupos de personas, etiquetas, representación ni selección interna.

## Destilación del score continuo del profesor

Otra iteración entrena estudiantes regresores para aproximar el margen docente continuo: (score PCA − mediana personal) / desviación personal. Las etiquetas binarias externas siguen idénticas y se verifica que el signo del margen coincide con 1/0. El margen se usa únicamente como objetivo de ajuste del estudiante, nunca como predictor. Las entradas siguen siendo EEG/GSR y los contextos son pasados/actuales.

Se prueban Ridge (alpha 1/100), HistGradientBoostingRegressor (hojas 7/15, 300 iteraciones) y CatBoostRegressor (profundidad 4/6, 300 iteraciones), en contextos 8/32, con/sin z personal offline: 24 combinaciones por fold, 120 ajustes internos. Se evalúa AUC binaria de los scores continuos predichos por personas externas. La sigmoid utilizada para exportar scores a [0,1] no es calibración probabilística.

Ejecutar `scripts/grid_atencion_destilacion.py --round 1` y auditar con `scripts/auditar_grid_atencion_destilacion.py --round 1`.

## Ranking por pares y ensamble ampliado

Se prueba CatBoostRanker con PairLogit, hasta 1.000 pares positivo/negativo por persona, profundidad 4/6, L2 3/15, 400 iteraciones y contextos 8/32, con/sin z personal offline: 16 configuraciones por fold, 80 ajustes internos. El identificador se usa exclusivamente para construir grupos de entrenamiento, sin formar parte de las entradas. La AUC se calcula en personas nuevas del fold. La sigmoid exportada del margen de ranking no es una probabilidad calibrada.

Ejecutar `scripts/grid_atencion_ranking.py --round 1` y auditar con `scripts/auditar_grid_atencion_ranking.py --round 1`.

El ensamble ampliado considera seis corridas sin ventanas posteriores (boosting, CatBoost, multiescala, características ampliadas, destilación y ranking). Se predefine un grid de 41 mezclas uniformes de 1/2/3 miembros por escenario; composición escogida en las cuatro personas internas de cada fold. No añade modelos entrenados ni usa los resultados externos para escoger pesos. El plan inicial de cinco familias se conserva y se documenta la incorporación de ranking antes de conocer su evaluación externa completa. Ejecutar `scripts/ensamblar_busqueda_atencion_meta07.py` después de las auditorías de todas las fuentes.
