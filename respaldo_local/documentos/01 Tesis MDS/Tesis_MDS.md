
# Tesis MDS

## Objetivo
Evaluar si la información temporal y la fusión multimodal mejoran la predicción de pseudoetiquetas de atención y activación emocional durante la navegación web, comparando modelos temporales y estáticos en participantes no utilizados para su ajuste.

Cuatro señales de la Toma de Muestra 2: **EEG, GSR, eye tracking y pupilometría**. Sin
expresión facial — esa señal está en la Toma de Muestra 1, no en este dataset.
Objetivo general y los 7 específicos, en [[Estructura Tesis]] > Objetivos.

## Estado actual
- 23-09-2026 — **Presentación visual del tema y explicación de KDD.**
  Siete láminas con diagramas de temporalidad, etapas KDD, pseudoetiquetas y fusión.
  HTML autocontenido, PowerPoint editable y PDF; reemplazo en las rutas originales.
  Objetivos conservados íntegros. 34 comprobaciones del HTML y siete páginas verificadas
  en PowerPoint, con revisión de lectura en móvil.
  Entrega cerrada el 24-09-2026: commit de presentación `c1a75f2` y respaldo actualizado
  de la sección de tesis.
  Fuente: [[Avance - 23-09-2026 (Presentacion Visual y KDD)]].
- 22-09-2026 — **Objetivos científicos y metodología KDD incorporados.**
  Se reemplazaron el HTML y el PowerPoint del tema de tesis en sus rutas originales,
  conservando seis diapositivas. Objetivo general y siete específicos alineados con
  [[Estructura Tesis]]; KDD adaptado en cinco etapas con referencia a Fayyad et al. (1996).
  Segunda revisión del mismo día: redacción más directa, títulos más breves y menos
  repeticiones. Los siete objetivos conservan su alcance.
  HTML: 31 comprobaciones aprobadas; PowerPoint: seis páginas verificadas.
  Primera revisión en `46b054d`; redacción final en `da6152d`, con respaldo actualizado.
  Fuente: [[Avance - 22-09-2026 (Objetivos Cientificos y Metodologia KDD)]].
- 21-09-2026 — **Últimos avances resumidos en cinco diapositivas.**
  Nueva versión HTML autocontenida y PowerPoint editable: grids, control temporal,
  ablación/PCA y próximos pasos. Resume los experimentos cerrados al 14-09;
  35 comprobaciones del HTML y renderizado de cinco páginas en PowerPoint.
  Archivos: `Tesis_MDS/presentaciones/Avances-Resumen-Autocontenido-21-09-2026` (`.html` / `.pptx`).
  Commit `54684e4`. Fuente: [[Avance - 21-09-2026 (Resumen de Avances en Cinco Slides)]].
- 20-09-2026 — **Presentación breve del tema de tesis en HTML autocontenido.**
  Seis diapositivas: tema y profesor guía, antecedentes, objetivo general, siete
  específicos resumidos, metodología y datos disponibles. Funciona sin conexión
  ni archivos auxiliares; 31 comprobaciones y seis páginas de impresión verificadas.
  Archivo: `Tesis_MDS/presentaciones/Presentacion-Tema-Tesis-Autocontenida-20-09-2026.html`.
  Commit de presentación `51e390e`.
  También disponible en PowerPoint editable de seis diapositivas para importar en Canva;
  apertura y renderizado verificados en PowerPoint. Commit de conversión `4a8f192`.
  Fuente: [[Avance - 20-09-2026 (Presentacion Acotada del Tema)]].
- 17-09-2026 — **Presentación HTML de avances preparada y verificada.**
  14 diapositivas con resultados de grids, controles temporales, ablación y PCA;
  distingue hallazgos exploratorios y próximos pasos pendientes. Incluye navegación,
  lectura continua e impresión. 22 comprobaciones y revisión de accesibilidad.
  Archivo: `Tesis_MDS/presentaciones/Avances-Tesis-MDS-17-09-2026.html`.
  Commit de presentación `cfc23aa`.
  Fuente: [[Avance - 17-09-2026 (Presentacion de Avances)]].
- 14-09-2026 — **Grid Search BiLSTM → LSTM → TCN completado y auditado en ese orden.**
  32 configuraciones por familia, 480 entrenamientos internos, 1.920 checkpoints
  y 60 modelos externos con dos semillas. BA macro: BiLSTM 0,3410; LSTM 0,3333;
  TCN 0,3529. Ninguna supera a Ridge 0,3748 ni llega a 0,50.
  TCN gana 0,71 pp frente a su control repetido, con IC que incluye cero;
  LSTM pierde 1,72 pp. Recall medio entre 14,5 % y 16,2 %.
  1.980 modelos y 162.288 predicciones auditados; 66 pruebas. Validation/test sin reevaluar.
  Fuente: [[Avance - 14-09-2026 (Grid Search BiLSTM LSTM y TCN)]].
  Commit de resultados `40cfa2f`; respaldo actualizado de la sección de tesis.
- 13-09-2026 — **Grid Search de Transformer completado y auditado.**
  32 configuraciones cartesianas, 160 entrenamientos internos, 640 checkpoints,
  1.920 puntuaciones internas y 20 modelos externos con dos semillas.
  BA macro 0,3526 frente a Transformer anterior 0,3634 y Ridge 0,3748: no mejora.
  Todos los folds eligen época 2, learning rate bajo y dropout alto; recall medio 17,5 %.
  660 modelos y 54.096 predicciones auditados; 64 pruebas. Validation/test sin reevaluar.
  Fuente: [[Avance - 13-09-2026 (Grid Search Transformer)]]. Commit de resultados `9d25c47`.
- 13-09-2026 — **Transformer y TCN iterados y auditados.**
  Seis configuraciones, 270 decisiones internas, 90 checkpoints y 20 modelos externos.
  BA macro: selección conjunta 0,3716; Transformer 0,3634; TCN 0,3668;
  control de ventana actual repetida 0,3749. No hay mejora clara frente a Ridge 0,3748
  ni evidencia de ventaja del historial; recall medio conjunto 19,6 %. Meta 0,50 pendiente.
  54.096 predicciones verificadas y 61 pruebas; validation/test sin reevaluar.
  Fuente: [[Avance - 13-09-2026 (Transformer y TCN)]]. Commit de resultados `4427064`.
- 12-09-2026 — **Ablación y PCA completados y auditados.**
  38 variantes, 190 modelos y 513.912 predicciones verificadas; 59 pruebas.
  Quitar EEG baja BA macro de 0,3748 a 0,3546. Solo EEG mantiene 0,3722, pero
  recall medio cae a 10,8 %. Quitar fixation_count da 0,3843, máximo secundario
  exploratorio. PCA al 90 %: 0,3764 con 13–45 componentes; mejora incierta.
  Cargas PCA, ranking de 24 variables, intervalos y cuatro figuras conservados.
  Fuente: [[Avance - 12-09-2026 (Ablacion y PCA)]].
  Publicado en GitHub `main`, commit de resultados `3bbedf1`, con respaldo de notas actualizado.
- 12-09-2026 — **Cuatro rondas auditadas; meta BA macro 0,50 no alcanzada.**
  Persistencia, multiescala, adaptación offline y regresión ordinal. Mejor observación: Ridge
  0,3748 frente a 0,3716 anterior; ganancia incierta y menor recall medio. La selección
  principal multiescala obtiene 0,3649; la ordinal, 0,3642. 100 modelos recargados,
  270.480 predicciones verificadas, 5.460 puntuaciones internas y 56 pruebas.
  Se conservan también 11 modelos de intentos parciales y sus correcciones numéricas.
  Fuente: [[Avance - 12-09-2026 (Busqueda Meta 05)]].
  Publicado en GitHub `main`, commit de resultados `255a79b`, con respaldo de notas actualizado.
- 11-09-2026 — **Auditoría, ensambles y mezclas completados.**
  140 archivos de modelos, 378.672 predicciones verificadas y 47 pruebas. Mezcla con
  25 % de stacking: BA macro 0,3716 frente a 0,3651 anterior (+0,65 pp; IC [-0,31; +1,71]).
  Es un contraste secundario exploratorio; la mezcla principal de 10 % obtiene 0,3687.
  Recall medio recupera 28,8 % frente a 6,4 % del stacking, pero el promedio solo da 37,1 %.
  La selección principal de promedios no mejora (0,3595). Validation/test sin reevaluar.
  Fuente: [[Avance - 11-09-2026 (Auditoria y Ensambles)]].
  Publicado en GitHub `main`, commit de resultados `584b073`, con respaldo de notas actualizado.
- 11-09-2026 — **SVM, QDA y ajuste de hiperparámetros completados.**
  44 modelos base, 88 decisiones, 660 ajustes internos y 70 bundles externos guardados.
  Fusión logística: BA macro 0,3605; fusión LDA: 0,3593; búsqueda conjunta: 0,3548.
  Ninguna supera la fusión geométrica anterior, 0,3651. Intervalos incluyen cero.
  189.336 predicciones verificadas y 45 pruebas aprobadas; validation/test sin reevaluar.
  Se conservan hiperparámetros, diagnóstico por clase, figuras y el intento serial parcial.
  Fuente: [[Avance - 11-09-2026 (SVM QDA e Hiperparametros)]].
  Publicado en GitHub `main`, commit de resultados `1ffb0ea`, con respaldo de notas actualizado.
- 11-09-2026 — **Nueva búsqueda de activación completada: boosting, ordinalidad y balanceo.**
  432 configuraciones, 360 ajustes internos, 6.480 puntuaciones y 60 bundles externos.
  Búsqueda conjunta: BA macro 0,3522; ordinal: 0,3582; CatBoost: 0,3555.
  No superan la fusión geométrica anterior, 0,3651. Diagnóstico muestra bajo recall
  de medio/alto en el ordinal. Se conserva cada intento; validation/test sin reevaluar.
  162.288 predicciones verificadas y 42 pruebas aprobadas.
  Fuente: [[Avance - 11-09-2026 (Boosting Ordinalidad y Balanceo)]].
  Publicado en GitHub `main`, commit de resultados `82fef67`, con respaldo de notas actualizado.
- 10-09-2026 — **Nuevos modelos y fusiones completados para atención y activación.**
  LDA y Extra Trees, fusión temprana y tardía por media, geométrica y pesos internos.
  120 bundles, 324.576 predicciones verificadas, 1.530 puntuaciones internas y 38 pruebas.
  Activación llega a BA macro 0,3651 con fusión geométrica frente a temprana 0,3594;
  atención, a 0,3444 con pesos frente a temprana 0,3389. Intervalos incluyen cero.
  Bitácora completa, incluido incidente de redondeo y su corrección; sin nueva evaluación de test.
  Fuente: [[Avance - 10-09-2026 (Nuevos Modelos y Fusiones)]].
  Publicado en GitHub `main`, commit de resultados `543fd48`, con respaldo de notas actualizado.
- 10-09-2026 — **Iteraciones publicadas en GitHub**, commit de resultados `79d0b48`.
  Código, informe y 90 archivos de modelos publicados; respaldo de notas actualizado.
  Detalle: [[Avance - 10-09-2026 (Publicacion de Iteraciones)]].
- 08-09-2026 — **Tres iteraciones de mejora completadas para clasificación de activación.**
  Búsqueda de contexto/modelo, combinación de probabilidades y ampliación a mirada/EEG.
  795 ajustes internos, 90 archivos de modelos, 243.432 predicciones verificadas y 33 pruebas.
  Mejor promedio observado: BA macro 0,3546 frente a logística 0,3536 (+0,11 pp), con intervalo
  que incluye cero; las otras iteraciones no mejoran el baseline. Sin superioridad estable.
  Validation/test originales sin nueva evaluación. Fuente: [[Avance - 08-09-2026 (Iteraciones de Mejora)]].
- 08-09-2026 — **Control del historial pupilar completado en cinco folds de train.**
  TCN, LSTM y BiLSTM frente a controles entrenados con ventana actual repetida y MLP
  con las mismas cinco variables. 170 modelos guardados, 459.816 predicciones auditadas
  y 29 pruebas aprobadas. LSTM/BiLSTM ganan +0,56/+0,74 puntos de BA macro frente a sus
  controles repetidos, con intervalos que incluyen cero; no superan a logística en promedio.
  Regresión sigue sin mejora. Validación y test originales sin nueva evaluación.
  Fuente vigente de este contraste: [[Avance - 08-09-2026 (Control del Historial Pupilar)]].
  Publicado en GitHub `main`, commit de resultados `e0e3730`.
- 07-09-2026 — **TCN, LSTM y BiLSTM entrenadas y evaluadas**, junto con control MLP.
  104 redes guardadas, 26 pruebas y auditoría de 903.448 predicciones aprobadas.
  Hay mejoras puntuales de clasificación de activación, sin ventaja general confirmada
  del historial; los scores continuos siguen cerca de R² = 0. `pupil_std_z` destaca en
  la explicación diferencial de la BiLSTM pupilar. Fuente vigente del contraste temporal:
  [[Avance - 07-09-2026 (TCN LSTM y BiLSTM)]].
  Publicado en GitHub `main`, commit de resultados `23017c3`, con respaldo de notas actualizado.
- 07-09-2026 — **Análisis y modelos reducidos publicados en GitHub**, rama `main`,
  commit `2575183`: 84 modelos nuevos, informes, figuras, predicciones, código y pruebas.
  Respaldo actualizado de notas fechado 07-09-2026.
  Detalle: [[Avance - 07-09-2026 (Publicacion de Analisis en GitHub)]].
- 07-09-2026 — **Contraste de estabilidad terminado: 5 folds por participante en train.**
  180 ajustes internos, 36 pipelines finales y panel de entradas congelado. La mejora
  inicial de pupila sola no se sostuvo; el compacto de atención selecciona 9 columnas
  estables, pero pierde desempeño en RF. Se mantienen los completos como referencia.
  18 pruebas y auditoría de 486.864 predicciones aprobadas; test sin nueva evaluación.
  Fuente vigente: [[Avance - 07-09-2026 (Estabilidad y Reduccion de Variables)]].
- 07-09-2026 — **Análisis exploratorio de importancia y reducción de variables.**
  Activación: pupila sola (6) y mirada + pupila (16) son candidatas frente a 25 entradas;
  las mejoras puntuales de clasificación en validación aún tienen incertidumbre amplia.
  Atención sigue cerca del nivel trivial; el top-5 incluye redundancia y ruido eléctrico.
  Se conservaron etiquetas/split y no se volvió a evaluar test.
  Informe y resultados: [[Avance - 07-09-2026 (Importancia de Variables)]].
- 06-09-2026 — **Trabajo de tesis publicado en GitHub**, repositorio público
  `marioromero00/Tesis_MDS`, rama `main`, commit de entrega `8757e98`.
  Incluye modelos, predicciones, métricas, código, presentación y un respaldo completo de
  esta sección en ZIP. Es un respaldo de tesis, no sincronización de la bóveda completa.
  Detalle: [[Avance - 06-09-2026 (Respaldo Completo en GitHub)]].
- 06-09-2026 — **Presentación HTML actualizada con los resultados de los baselines.**
  `presentaciones/avance-eda-sincronizacion-15-08-2026.html` tiene 16 diapositivas: protocolo,
  clasificación, regresión, sensibilidad, guardado y próximo contraste temporal.
  Se verificaron 45 cifras contra el CSV, navegación, imágenes y vista móvil.
  Fuente: [[Avance - 06-09-2026 (Presentacion Resultados Baselines)]].
- 05-09-2026 — **30 baselines entrenados y guardados como pipelines completos `.joblib`.**
  Mario confirmó que la validación metodológica ya estaba resuelta y pidió continuar.
  Se conservaron etiquetas y partición 25/8/8; la recarga de los 30 modelos reproduce exactamente
  predicciones y probabilidades. Diez pruebas aprobadas; métricas consistentes con el 22-08-2026.
  Repositorio local en esta máquina: `C:/Users/MarioRomero/desktop/mds/Tesis_MDS/`.
  Entrega en `resultados/modelado/ejecuciones/baselines_05-09-2026_02/` dentro del repositorio.
  Fuente vigente: [[Avance - 05-09-2026 (Baselines Entrenados y Guardados)]].
- 22-08-2026 — **Primera evaluación fuera de muestra terminada.** Se construyeron
  pseudoetiquetas sin circularidad, se congeló una división 25/8/8 por participante y se
  ejecutaron baselines. Los resultados estáticos quedaron alrededor del nivel trivial; la
  etiqueta de atención mostró baja robustez entre fusión igualitaria y PCA (ρ=0,454).
  Detalle en [[Avance - 22-08-2026 (Etiquetas Particion y Baselines)]].
- 22-08-2026 — **Pipeline multimodal secuencial ejecutado con los datos reales**: 25.992
  ventanas de 2 s, 22.201 válidas en las cuatro modalidades y 48 participantes auditados.
  Código, configuración, pruebas, hashes y resultados quedaron en el repo `Tesis_MDS`.
  Detalle en [[Avance - 22-08-2026 (Pipeline Multimodal Reproducible)]].
- 22-08-2026 — La selección del TXT principal se corrigió usando el archivo más largo por
  sesión. P48 queda recuperado; P25 se agrega a las exclusiones EEG. Resultado actualizado:
  **44/48 EEG utilizables**; P1, P14, P17 y P25 marcados por calidad.
- 22-08-2026 — **Preprocesamiento de GSR, pupilometría y eye tracking especificado y probado**
  en `~/tesis/Tesis_MDS/preprocesamiento/`: features en ventanas de 2 s
  con 50 % de solapamiento, el
  mismo soporte que las épocas del EEG. Verificado con datos sintéticos; **falta correrlo sobre
  el export real**, que está en Drive. Detalle en
  [[Avance - 22-08-2026 (Preprocesamiento GSR Pupila y Eye Tracking)]].
- 22-08-2026 — **Frecuencia del EEG resuelta: son 125 Hz**, verificada contra los datos crudos.
  Se eliminó la expresión facial de las siete secciones de [[Estructura Tesis]] donde seguía
  declarada como vigente. Detalle en
  [[Avance - 22-08-2026 (Frecuencia EEG y Limpieza de Expresion Facial)]].
  Deck de la presentación de avances armado en
  [[Avance Capitulo 1 y Verificaciones - 22-08-2026]] (10 diapositivas,
  `presentacion-22-08-26.html`).
- 24-08-2026 — **Vault consolidado.** La documentación del pipeline existía en tres copias
  desincronizadas; quedó una sola en `Analisis de Datos/`, con el contenido del 22-08-2026:
  12 notas planas y 16 figuras. Entran [[PREPROCESAMIENTO_MULTIMODAL]] y
  [[ETIQUETAS_Y_BASELINES]], que solo existían en la copia de la raíz. Detalle del retiro en
  [[Archivo]].
- 20-08-2026 — Primera consolidación de la documentación del pipeline en el vault, con
  [[Mapa del proyecto]] como MOC.
- 17-08-2026 — Capítulo 1 completo en [[Estructura Tesis]]: objetivos (general + 7 específicos),
  alcances y limitaciones, y contribuciones. Marco teórico 2.1 (IHC y UX) esquematizado con
  referencias por verificar. Detalle en [[Avance - 17-08-2026 (Capitulo 1 y Marco Teorico 2.1)]].
- 10-08-2026 — Capítulo de problema e hipótesis definido en [[Problema e hipótesis]].
  La hipótesis central quedó operacionalizada para emociones y atención, con hipótesis
  nula asociada, criterios de interpretación y amenazas a la validez.
- EDA de EEG terminado y corregido para sesiones con varios TXT.
- Preprocesamiento multimodal ejecutado y reproducible.

## Próximos pasos

> Actualización 05-09-2026: Mario confirmó la validación metodológica y autorizó continuar con
> los baselines, ya guardados. Los pendientes de aprobación listados abajo provienen del estado
> del 22-08-2026; no deben volver a tratarse como bloqueo de esta ejecución. La confirmación y el
> alcance conservado están en [[Avance - 05-09-2026 (Baselines Entrenados y Guardados)]].

**Bloqueado por el profesor guía**
- [ ] Confirmar que redefinir "emoción" como *arousal* es aceptable. De esto cuelgan el objetivo
  específico 3, el alcance 2 y la contribución 1 del Cap. 1.
- [ ] Aprobar el manifiesto de sincronización y los criterios finales de calidad.

**Metodología**
- [ ] Cerrar las 5 decisiones abiertas de [[Resumen Diseño Etiquetas y Modelos]] (fusión y
  umbrales de ambos scores, ventana de GSR por latencia de SCR, validación externa). La ventana
  del GSR ya se puede cerrar con evidencia: el preprocesamiento emite las features de SCR sobre
  2 s y sobre 6 s de contexto para poder comparar.
- [x] Conservar scores continuos y etiquetas ternarias para atención y activación.
- [x] Separar estrictamente las señales profesor y estudiante para evitar circularidad.

**Pipeline**
- [x] Analizar importancia, redundancias y subconjuntos en train/validación (07-09-2026).
- [x] Comprobar estabilidad en 5 folds y congelar el panel comparativo de entradas (07-09-2026).
- [x] Preprocesar GSR, eye tracking y pupilometría con los datos reales.
- [x] Validar nombres de columna y formato de fecha contra el TSV real.
- [x] Recortar ventanas comunes de 2 s por estímulo y límites UTC.
- [x] Integrar EEG, GSR, pupila y mirada en una tabla auditable de 59 columnas.
- [ ] Revisar con el profesor el offset de P29 y la aceptación de los criterios de calidad.
- [x] Implementar ambas pseudoetiquetas provisionales y entrenar baselines estáticos.
- [x] Congelar partición por participante: 25 train, 8 validación, 8 prueba; P29 sensibilidad.
- [x] Validación metodológica confirmada por Mario el 05-09-2026 para continuar con los baselines.
- [x] Entrenar, guardar y verificar recarga de los baselines completos (05-09-2026).
- [x] Entrenar TCN/LSTM/BiLSTM con idéntica partición y etiquetas, y guardar explicaciones (07-09-2026).
- [ ] Ampliar el contraste de contexto y fusión con hipótesis fijadas y controles sin historial.

**Escritura**
- [ ] Verificar las referencias del Marco Teórico 2.1 antes de citarlas — fueron transcritas de
  bibliografías ajenas, no leídas. Actualizar el dato de Statista a 2026.
- [ ] Revisar si el protocolo de partición disjunta coincide con el supuesto de *view
  independence* de co-training; si es así, citarlo antes de presentarlo como aporte propio.
- [ ] Re-verificar la brecha 2 del Estado del Arte para la combinación sin expresión facial.
- [ ] Desarrollar el resto del Cap. 2; los Cap. 6 a 9 siguen en blanco.

## Decisiones importantes
- 22-08-2026 — **El EEG se registró a 125 Hz, no a 250 Hz.** La placa es OpenBCI Cyton + Daisy:
  el Cyton muestrea a 250 Hz con 8 canales y al agregar la Daisy para llegar a 16 el muestreo
  por canal cae a la mitad. La ventana de 2 s son **250 muestras**, no 500. Queda revertida la
  "corrección" a 250 Hz del 08-08-2026.
- 17-08-2026 — El análisis de fatiga y habituación **entra al alcance** como objetivo específico 6.
  Deja de ser opcional y obliga a conservar el score continuo además del discretizado.
- 10-08-2026 — La tesis tiene una sola hipótesis central. Fatiga y habituación quedan como
  posible análisis complementario, no como una segunda hipótesis. Detalle en
  [[Problema e hipótesis]].
- 08-08-2026 — Propuestas de resolución para las decisiones abiertas del modelo profesor en
  [[Modelo Profesor - Decisiones]]. Cuatro de siete se pueden cerrar sin el profesor guía; tres
  van a la reunión del 10-08. Sin confirmar aún.

## Qué no funcionó
Enfoques descartados y por qué — para no volver a razonarlos desde cero.

- **Clasificador facial como Modelo Profesor** (diseño previo, para atención y emoción).
  Descartado: la expresión facial existe en la Toma de Muestra 1, usada por otras tesis del
  grupo, pero **no en la Toma de Muestra 2**, que es este dataset. De ahí el rediseño
  profesor → estudiante con las 4 señales disponibles. Detalle en [[presentacion 10-08-26]].
- **Resumir las señales por promedios/medianas.** Descartado por pérdida de dinámica
  temporal — es justamente la limitación que la tesis busca atacar ([[Problema e hipótesis]]).
- **Fusión multimodal tardía como único enfoque.** No descartada, pero la literatura previa
  muestra mejoras marginales; por eso entra como una de tres alternativas a comparar, no
  como la elegida.

## Estructura

- `Avances/` — bitácora fechada.
- `Diseno Metodologico/` — etiquetas, modelos y decisiones metodológicas.
- `Marco Teorico/` — problema, conceptos y referencias previas.
- `Escritura/` — estructura y desarrollo del documento de tesis.
- `presentaciones/` — material para exposiciones: los punteos fechados, los HTML
  entregados y [[main_presentacion_mds]], la fuente LaTeX/Beamer del deck.
- `Analisis de Datos/` — documentación del pipeline en 12 notas planas, sincronizada al
  22-08-2026 desde el repositorio `~/tesis/Tesis_MDS`:
  [[Mapa del proyecto]] es su MOC.
- `attachments/Analisis de Datos/` — 16 figuras generadas por el pipeline.
  **El código y los datos viven fuera del vault**; las notas los citan por nombre de archivo
  (`eda_eeg.py`, `eeg_resumen_sesiones.csv`) en vez de enlazarlos.

## Notas relacionadas
- [[Avance - 07-09-2026 (TCN LSTM y BiLSTM)]] — 104 redes, evaluación frente a baselines,
  variables que sostienen la diferencia y límites del historial temporal.
- [[Avance - 07-09-2026 (Publicacion de Analisis en GitHub)]] — publicación de los dos
  análisis y respaldo de notas con inventario.
- [[Avance - 07-09-2026 (Estabilidad y Reduccion de Variables)]] — contraste interno,
  límites de la reducción y panel congelado para el siguiente experimento.
- [[Avance - 07-09-2026 (Importancia de Variables)]] — importancia por participante,
  reducción de entradas y candidatos para atención/activación.
- [[Avance - 06-09-2026 (Respaldo Completo en GitHub)]] — publicación de código, modelos,
  presentación y snapshot de las notas; alcance de la sincronización.
- [[Avance - 06-09-2026 (Presentacion Resultados Baselines)]] — HTML de 16 diapositivas,
  resultados y verificación de presentación.
- [[Avance - 05-09-2026 (Baselines Entrenados y Guardados)]] — modelos entrenados, ubicación,
  carga, métricas y confirmación de continuidad metodológica.
- [[Problema e hipótesis]] — problema, brechas, hipótesis central y criterios de
  interpretación.
- [[Avance - 10-08-2026 (Hipotesis de Investigacion)]] — registro del cierre de este
  capítulo.
- [[Avance - 17-08-2026 (Capitulo 1 y Marco Teorico 2.1)]] — objetivos, alcances,
  contribuciones y esqueleto de 2.1.
- [[Avance - 22-08-2026 (Marco Teorico 2.1.2 UX)]] — sección 2.1.2 de IHC y UX.
- [[Avance - 22-08-2026 (Frecuencia EEG y Limpieza de Expresion Facial)]] — verificación de la
  frecuencia contra los datos crudos y limpieza del diseño descartado en el borrador.
- [[Avance - 22-08-2026 (Preprocesamiento GSR Pupila y Eye Tracking)]] — módulo de features por
  ventana para las tres señales del Tobii.
- [[Avance - 22-08-2026 (Pipeline Multimodal Reproducible)]] — ejecución real, integración EEG,
  auditoría, hashes y correcciones P25/P48.
- [[Avance - 22-08-2026 (Etiquetas Particion y Baselines)]] — pseudoetiquetas, split congelado,
  auditoría P29 y primera evaluación fuera de muestra.
- [[Conocimiento Presentaciones Pasadas]] — consolidado de la presentación de junio 2026:
  EDA (48 participantes), pipeline EEG completo, los 273 features y la revisión de literatura.
