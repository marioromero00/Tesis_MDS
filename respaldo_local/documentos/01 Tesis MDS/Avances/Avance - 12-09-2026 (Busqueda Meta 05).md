# Avance: 12-09-2026, Busqueda Meta 05

Continúa [[Avance - 11-09-2026 (Auditoria y Ensambles)]]. Meta solicitada: superar
0,50 de BA macro de activación. Las búsquedas comenzaron la noche del 11-09-2026 y
continuaron el 12-09-2026. Se conserva arousal_label_6s, las tres clases y el split.
El estudiante usa EEG, mirada y pupila; GSR sigue reservado al Modelo Profesor.

## Búsquedas completadas

| Enfoque | Selección principal | Mejor familia secundaria |
|---|---:|---:|
| Persistencia: media, EMA y Markov | 0,3506 | Markov: 0,3698 |
| Historial multiescala, desfase y cambios relativos | 0,3649 | Ridge: 0,3748 |
| Adaptación offline por persona, sin etiquetas | 0,3645 | Centrado: 0,3672 |
| Regresión ordinal con umbrales internos | 0,3642 | Ridge: 0,3642 |

Persistencia compara 16 configuraciones y 240 puntuaciones internas. Las transiciones
de Markov se estiman solo con etiquetas de las personas de ajuste; al predecir se usa
el estado estimado, sin consumir etiquetas. Se conservan 20 modelos completos.

Multiescala compara 24 modelos sobre cuatro representaciones: actual, estadísticas
de 4/16/64 ventanas, desfase de cuatro ventanas y desviaciones locales relativas.
Clasificadores Ridge, kernel RBF aproximado con Nystroem y Extra Trees; suavizado
1/8/32. Se completaron 360 ajustes internos, 1.080 puntuaciones y 40 modelos externos.

Adaptación compara 60 reglas de centrado de log-probabilidades o rangos por persona,
con 900 puntuaciones y 15 modelos. Usa la sesión completa sin etiquetas, incluidas
entradas futuras de esa persona. Es una variante offline y transductiva, no una
demostración de predicción causal o en tiempo real.

## Qué significa el máximo de 0,3748

Ridge obtiene BA macro 0,37475 frente al máximo anterior 0,37160: +0,315 puntos
porcentuales; IC pareado descriptivo [-2,262; +2,770], mejora en 14/25 personas.
El máximo es secundario. La selección conjunta multiescala obtiene 0,36485.
Recall de bajo/medio/alto: 0,4995/0,2327/0,3758. La mezcla previa reconocía 0,2881
de medio; la subida de BA oculta una pérdida en esa clase. No se confirma superioridad.

Las etiquetas originales usan cuantiles por persona. Un mismo Arousal Score puede
recibir clases distintas entre personas. Se comprobó en `scripts/preparar_modelado.py`;
no se cambiaron umbrales ni etiquetas para mejorar resultados.

## Incidentes, reintento y auditoría

La comprobación de igualdad exacta detuvo el primer entrenamiento multiescala con
diferencias de scores de 1,67e-16. El intento quedó conservado en
`resultados/multiescala_11-09-2026/`. La continuación usa exactamente las mismas
selecciones y predicciones internas; repite solo los ajustes externos en
`resultados/multiescala_11-09-2026_completa/`. Exige clases idénticas y tolerancia
relativa/absoluta 1e-12 para scores. Su diferencia máxima de recarga fue 4,94e-13.
El escalado reajustado se compara con esa misma tolerancia, por diferencias de
redondeo al recorrer matrices con distinta disposición en memoria.

Se recargaron los 75 modelos de estas tres rondas y se verificaron 202.860 predicciones.
La auditoría recalcula puntuaciones internas, elecciones y métricas de fold/persona;
comprueba disjunción de personas y reajusta los 40 preprocesadores multiescala.
Las 56 pruebas finales del proyecto pasaron, incluidas causalidad, reinicio por huecos/persona,
ausencia de dependencia de etiquetas y recarga. Una prueba de adaptación se corrigió
antes de entrenar porque su ejemplo no cruzaba el umbral que pretendía comprobar.

## Regresión ordinal completada

Se completó otra búsqueda con codificación bajo=-1, medio=0 y alto=1, manteniendo la
etiqueta evaluada. Compara Ridge, RBF, HGB y Extra Trees sobre tres representaciones,
con selección interna de dos umbrales y suavizado. 180 ajustes internos, 3.240
puntuaciones, 25 modelos completos y 67.620 predicciones verificadas. Selección
principal/Ridge: 0,3642; RBF: 0,3551; HGB: 0,3532; Extra Trees: 0,3576.

El primer intento se detuvo en un kernel RBF con diferencia de 2,83e-11. La auditoría
comprobó que los valores de entrada eran exactamente iguales, pero su disposición en
memoria cambiaba el redondeo. Convertir ambas entradas a C-contiguas produjo diferencia
cero. Se conservó el intento parcial y se repitieron solo los ajustes externos, con
las mismas elecciones y umbrales. Los 25 modelos de la continuación reprodujeron sus
scores exactamente. No se relajó la tolerancia 1e-12 ni la igualdad de clases.

Resultados completos: `resultados/regresion_ordinal_12-09-2026_completa/`.
Carga y auditoría mediante `scripts/continuar_regresion_ordinal.py`; el predictor
canónico es `continuar_regresion_ordinal.predict(bundle, frame)`.

## Balance de las cuatro búsquedas

**Meta 0,50 no alcanzada.** Mejor BA macro observada 0,3748, con ganancia secundaria
incierta y pérdida de recall medio. Se guardaron y auditaron 100 modelos completos,
270.480 predicciones y 5.460 puntuaciones internas. Se hicieron 540 ajustes internos
nuevos. Además se conservan 11 archivos de modelos de los dos intentos parciales.
Las 56 pruebas finales pasaron en 6,468 segundos; el registro conserva sus advertencias.

Informe consolidado: `documentacion/Busqueda_Meta_05_12-09-2026.md`; tabla y figuras
PNG/PDF: `resultados/meta_05_12-09-2026/`. Incluye todos los contrastes principales
y secundarios. Entorno y pruebas: `documentacion/ambiente_busqueda_05_12-09-2026.json`.

## Alcance

Cinco folds externos sobre las mismas 25 personas de train; tres internos por persona.
Los contrastes principales se eligen internamente antes de la evaluación externa de
cada ronda. Los intervalos no corrigen búsquedas repetidas ni dependencia entre folds.
La normalización original sigue siendo offline. Validation/test no se reevaluaron.
Los resultados actuales no alcanzan 0,50 ni demuestran que sea imposible alcanzarlo.

Fuentes: `documentacion/Busqueda_persistencia_11-09-2026.md`,
`Busqueda_multiescala_11-09-2026.md`, `Busqueda_adaptacion_11-09-2026.md` y manifiestos
de verificación de esas rondas. Ver [[Tesis_MDS]] y [[Resumen Diseño Etiquetas y Modelos]].

## Publicación

Código, modelos, resultados, informes y figuras publicados en GitHub `main`, commit
`255a79b`. Se comprobaron 295 hashes de archivos frente a los bytes preparados para Git.
Respaldo de los 71 archivos de esta sección: `documentacion/Tesis_Vault_Meta_05_12-09-2026.zip`,
con inventario `documentacion/inventario_vault_meta_05_12-09-2026.json`.
