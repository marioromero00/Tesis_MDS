# Busqueda adaptacion: 11-09-2026

Meta solicitada: superar 0,50 de BA macro de activacion. Etiqueta fija arousal_label_6s;
25 participantes de train, cinco folds externos por persona y tres internos. Estos
participantes ya se usaron en exploraciones anteriores: no es confirmacion independiente.
Contraste principal: seleccion interna conjunta (all); familias separadas son secundarias.

## Resultados

| scope | macro_score | balanced_accuracy | macro_f1 |
|---|---|---|---|
| all | 0.3645 | 0.3637 | 0.3520 |
| center | 0.3672 | 0.3654 | 0.3442 |
| rank | 0.3626 | 0.3577 | 0.3558 |

| scope | reference | mean_delta | ci_low | ci_high | improved | tied |
|---|---|---|---|---|---|---|
| all | geometric_0.3651 | -0.0005 | -0.0182 | 0.0170 | 16 | 0 |
| rank | geometric_0.3651 | -0.0025 | -0.0270 | 0.0262 | 11 | 0 |
| center | geometric_0.3651 | 0.0021 | -0.0172 | 0.0211 | 17 | 0 |
| all | mixture_0.3716 | -0.0071 | -0.0231 | 0.0091 | 10 | 1 |
| rank | mixture_0.3716 | -0.0090 | -0.0319 | 0.0148 | 10 | 0 |
| center | mixture_0.3716 | -0.0044 | -0.0217 | 0.0135 | 11 | 1 |

Los intervalos son descriptivos, con 2.000 remuestreos pareados de participantes despues
de promediar semillas; no corrigen busquedas repetidas ni dependencia entre folds. Una
semilla en filtros deterministas; dos en multiescala, con seleccion usando la primera.
La referencia 0,3716 tambien es un maximo secundario exploratorio. No se alcanzo 0,50
si ninguna fila de BA macro supera ese valor; no se sustituye por accuracy o un fold aislado.

## Protocolo y auditoria

Configuraciones y semillas en protocolo.json; todas las puntuaciones en intentos.csv,
elecciones en selecciones.json. Se congelaron antes de la evaluacion externa. Se conserva
la prediccion interna de cada modelo y su linaje por persona. La auditoria recalcula
900 puntuaciones y 15 elecciones; recarga 15 modelos,
verifica 40572 predicciones, 15 metricas de fold y 75 por persona.
Se reajustaron 0 preprocesadores para comprobar que usan solo personas de ajuste.
Scores y estadisticas de escalado usan rtol=atol=1e-12; etiquetas predichas coinciden exactamente.
Cada archivo guardado incluye sus componentes necesarios para predecir.

Persistencia compara media causal, EMA y filtrado de Markov con transiciones aprendidas
solo de etiquetas de ajuste, sin etiquetas al predecir. Multiescala compara Ridge,
Nystroem RBF (192 componentes) y Extra Trees; entradas actuales, estadisticas de 4/16/64
ventanas, desfase de cuatro ventanas o desviaciones locales relativas. Se excluyen GSR,
etiquetas, identidad de participante y metadatos del estimador. Los grupos solo reinician
el historial. El soporte de 64 ventanas de 2 s y salto 1 s es 65 s; desfase 4 y suavizado
32 pueden ampliarlo a 100 s. Los huecos y cambios de persona/grabacion reinician el historial.

Adaptacion usa la sesion completa SIN etiquetas para centrar log-probabilidades o
clasificar rangos del log-cociente alto/bajo. Es OFFLINE y transductiva: utiliza entradas
futuras de la misma persona; no debe presentarse como prediccion causal o en tiempo real.
Los rangos producen decisiones one-hot, no probabilidades calibradas. Ridge tambien
produce scores transformados por softmax, sin calibracion probabilistica.

Validation y test originales no se reevaluaron. Las pseudoetiquetas y la normalizacion
offline original siguen limitando todas las comparaciones. No se modificaron etiquetas,
participantes, clases o metrica para perseguir 0,50.

Reproduccion: scripts/entrenar_adaptacion.py en una copia
sin el directorio de salida existente; scripts/auditar_busquedas_05.py --round adaptacion.
Carga: agregar scripts al path, joblib.load(archivo) y adaptacion_core.predict(bundle, frame),
con frame ordenado por participant/recording/window_start_utc y señales originales.

Fuentes metodologicas: [aproximacion de kernels](https://scikit-learn.org/1.9/modules/kernel_approximation.html)
y [prevencion de fugas](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage).
