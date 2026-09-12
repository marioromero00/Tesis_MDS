# Busqueda multiescala: 11-09-2026

**Entrega completa tras reintento:** `resultados/multiescala_11-09-2026_completa/`.
Verificar con `scripts/continuar_multiescala.py --audit`. El directorio sin `_completa`
conserva el intento detenido por igualdad exacta de scores. La continuación reutiliza
los 360 ajustes internos y las mismas elecciones; acepta rtol=atol=1e-12 en scores y
exige clases idénticas. Fuentes y corrección en `continuacion.json`.

Meta solicitada: superar 0,50 de BA macro de activacion. Etiqueta fija arousal_label_6s;
25 participantes de train, cinco folds externos por persona y tres internos. Estos
participantes ya se usaron en exploraciones anteriores: no es confirmacion independiente.
Contraste principal: seleccion interna conjunta (all); familias separadas son secundarias.

## Resultados

| scope | macro_score | balanced_accuracy | macro_f1 |
|---|---|---|---|
| all | 0.3649 | 0.3565 | 0.3476 |
| rbf | 0.3696 | 0.3590 | 0.3472 |
| ridge | 0.3747 | 0.3693 | 0.3646 |
| trees | 0.3628 | 0.3428 | 0.2926 |

| scope | reference | mean_delta | ci_low | ci_high | improved | tied |
|---|---|---|---|---|---|---|
| all | geometric_0.3651 | -0.0002 | -0.0266 | 0.0275 | 12 | 0 |
| ridge | geometric_0.3651 | 0.0097 | -0.0160 | 0.0372 | 13 | 0 |
| rbf | geometric_0.3651 | 0.0045 | -0.0197 | 0.0338 | 15 | 0 |
| trees | geometric_0.3651 | -0.0023 | -0.0247 | 0.0250 | 10 | 0 |
| all | mixture_0.3716 | -0.0068 | -0.0321 | 0.0189 | 14 | 0 |
| ridge | mixture_0.3716 | 0.0031 | -0.0226 | 0.0277 | 14 | 0 |
| rbf | mixture_0.3716 | -0.0020 | -0.0258 | 0.0216 | 15 | 1 |
| trees | mixture_0.3716 | -0.0088 | -0.0274 | 0.0126 | 11 | 0 |

Los intervalos son descriptivos, con 2.000 remuestreos pareados de participantes despues
de promediar semillas; no corrigen busquedas repetidas ni dependencia entre folds. Una
semilla en filtros deterministas; dos en multiescala, con seleccion usando la primera.
La referencia 0,3716 tambien es un maximo secundario exploratorio. No se alcanzo 0,50
si ninguna fila de BA macro supera ese valor; no se sustituye por accuracy o un fold aislado.

## Protocolo y auditoria

Configuraciones y semillas en protocolo.json; todas las puntuaciones en intentos.csv,
elecciones en selecciones.json. Se congelaron antes de la evaluacion externa. Se conserva
la prediccion interna de cada modelo y su linaje por persona. La auditoria recalcula
1080 puntuaciones y 20 elecciones; recarga 40 modelos,
verifica 108192 predicciones, 40 metricas de fold y 200 por persona.
Se reajustaron 40 preprocesadores para comprobar que usan solo personas de ajuste.
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

Reproducción: `scripts/entrenar_multiescala.py` conserva el intento inicial;
`scripts/continuar_multiescala.py` completa sus ajustes externos. Usar una copia sin
directorios de salida existentes. Verificar con `scripts/continuar_multiescala.py --audit`.
Carga: agregar scripts al path, joblib.load(archivo) y multiescala_core.predict(bundle, frame),
con frame ordenado por participant/recording/window_start_utc y señales originales.

Fuentes metodologicas: [aproximacion de kernels](https://scikit-learn.org/1.9/modules/kernel_approximation.html)
y [prevencion de fugas](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage).
