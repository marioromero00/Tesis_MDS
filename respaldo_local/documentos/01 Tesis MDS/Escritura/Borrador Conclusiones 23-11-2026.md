# Borrador: Conclusiones

> [!info] Estado
> Borrador redactado el 23-11-2026 a pedido de Mario, a partir de `documentacion/Cierre_Experimental_Final_23-11-2026.md` y de los informes del repositorio. Complementa a [[Borrador Resultados y Discusión 23-11-2026]] y a [[Borrador Discusión fisiológica 23-11-2026]]; no reemplaza a [[Estructura Tesis]], donde el Capítulo 9 sigue *(pendiente)*. Las cifras son AUC por persona con intervalo de confianza de 95 %.

> [!warning] Decisiones abiertas que este texto no cierra
> No hay aprobación registrada del profesor guía. El borrador supone, de forma provisoria: (1) que "emociones" se presenta como activación (*arousal*); (2) que el margen práctico es 0,02; (3) que la etiqueta de atención es la original y la corregida por posición se informa como análisis; (4) el encuadre de apoyo parcial; (5) que la cohorte nueva queda como trabajo futuro. Si alguna cambia, hay que revisar las secciones 9.1 y 9.5.

## Capítulo 9: Conclusiones

### 9.1 Respuesta a la hipótesis

La hipótesis planteaba que los modelos temporales multimodales obtienen un mejor desempeño fuera de muestra que los modelos estáticos comparables. Los resultados la apoyan de forma parcial: el apoyo proviene de la activación y no de la atención.

En activación, agregar el historial de las señales mejora la predicción del *Arousal Score* (+0,036 [+0,010; +0,065]). La mejora corresponde a información temporal: se mantiene frente a un placebo de la misma persona y al excluir el intervalo que define la etiqueta (+0,047 [+0,018; +0,078]). Es de corto alcance: es clara a 6 s, a 12 s es menor e inconclusa (+0,024) y desde los 24 s no se distingue del placebo. Al controlar la posición dentro del estímulo el efecto conserva su tamaño (+0,032 [+0,004; +0,059]), pero queda inconcluso tras la corrección por comparaciones múltiples.

En atención, el modelo con historial también rinde mejor (+0,029 [+0,021; +0,037]), pero esa ventaja no es información temporal. Cuando el modelo conoce la posición de la ventana dentro del estímulo, el historial no agrega nada (+0,001 [−0,002; +0,005]). Lo que el historial capturaba es que el *Attention Score* sigue un patrón sistemático al inicio de cada página.

En ninguna de las dos variables el orden de las ventanas aportó de forma demostrable: la red recurrente no superó al resumen estadístico del historial y en atención rindió 0,040 menos.

### 9.2 Fusión y aporte de cada señal

Al comparar las tres estrategias con una misma familia de modelo (perceptrón multicapa), la fusión tardía superó a la temprana en atención (+0,012 [+0,005; +0,021]); en activación ninguna se distinguió de las demás. El resultado no se generaliza a otras familias: con HistGradientBoosting, en el cierre V3, la tardía no superó a la temprana. La fusión no es, entonces, el factor que explica el desempeño.

En atención la detección depende casi por completo del EEG; la GSR no agrega nada (+0,002). En activación aportan el EEG y el historial, la pupila en menor medida, y la mirada no aporta.

### 9.3 Qué detecta el EEG

El *Modelo Estudiante* de atención alcanza una AUC de 0,681 con el EEG, y una red convolucional sobre la señal cruda llega a 0,716. Sin embargo, esa detección corresponde sobre todo a la huella eléctrica de los movimientos oculares y los parpadeos. Al retirar tres componentes oculares, que representan 3,5 % de la varianza, la AUC baja a 0,621; un control que retira 72 % de la varianza no ocular la deja en 0,674. La ventaja de la red también disminuye al limpiar la señal.

De aquí se desprende la conclusión metodológica más importante del trabajo. La regla de no-circularidad separa las señales con que se construye la etiqueta de las señales con que se predice, pero no asegura independencia fisiológica entre ellas. La etiqueta de atención se define con la conducta ocular, es decir, con lo **Observado**, y el EEG registra esa misma conducta. Con estos datos no se puede afirmar que el modelo detecte lo **Atendido** a partir de actividad cerebral.

En activación, el EEG de la ventana actual no detecta el *Arousal Score* de forma demostrable (0,524 con variables calculadas y 0,498 con la red). El desempeño más alto en activación se obtuvo al adaptar el modelo a cada persona (+0,045 [+0,023; +0,069]) y al predecir por estímulo (0,587), y aun así es bajo.

### 9.4 Evolución durante la sesión

De forma descriptiva, la proporción de ventanas de activación alta disminuye hacia el final de la sesión (0,37 en el último quinto), lo que es compatible con habituación. La detección de atención mejora a lo largo de la sesión (de 0,65 a 0,71). Ninguno de los dos patrones se sometió a contraste.

### 9.5 Limitaciones

- Las 41 personas incluyen las de validación y test, consultadas en etapas anteriores. Los análisis posteriores al 16-11-2026 son exploratorios o dirigidos; ninguno es una confirmación independiente en personas nuevas.
- Las pseudoetiquetas se calculan offline, son relativas a la sesión de cada persona y no se validaron contra una medida externa de atención ni de activación.
- La limpieza ocular es parcial: la caída de 0,060 es una cota inferior de la contribución ocular.
- El EEG y el seguidor ocular tienen un desfase de reloj de 0,18 a 0,53 s que no se corrigió.
- En activación las AUC son bajas (0,52 a 0,59), por lo que el efecto temporal tiene interés científico pero poca utilidad práctica con las variables actuales.
- La red convolucional es una sola arquitectura, sin búsqueda de configuración.

### 9.6 Trabajo futuro

- Confirmar el efecto temporal en activación en una cohorte nueva, con el contraste y el tamaño de muestra definidos de antemano.
- Definir una etiqueta de atención que no dependa de la conducta ocular, o registrar electrooculograma y más canales para separar mejor la actividad cerebral de la ocular.
- Corregir el desfase entre el EEG y el seguidor ocular y analizar el EEG alineado a las fijaciones.
- Evaluar etiquetas y normalizaciones calculadas solo con información previa, para una versión utilizable en línea.

### 9.7 Conclusión general

La temporalidad aporta a la detección de la activación, en una escala de segundos y con un efecto pequeño. En atención, lo que parecía un aporte temporal es la estructura de la etiqueta dentro de cada estímulo, y lo que parecía detección cerebral es en gran parte conducta ocular registrada por el EEG. El aporte de la tesis es entonces doble: evidencia acotada de que las señales de los segundos previos ayudan a predecir la activación, y una advertencia metodológica sobre el uso de pseudoetiquetas oculares para evaluar modelos basados en EEG.

Fuentes: `documentacion/Cierre_Experimental_Final_23-11-2026.md`; `resultados/reapertura_41p_22-11-2026/`, `reapertura_fase3_41p_22-11-2026/`, `enfoques_41p_22-11-2026/`, `ampliacion_41p_16-11-2026/`, `limpieza_ocular_41p_23-11-2026/` y `red_cruda_41p_23-11-2026/` (`INFORME.md` de cada una).

## Notas relacionadas
- [[Estructura Tesis]]
- [[Problema e hipótesis]]
- [[Resumen Diseño Etiquetas y Modelos]]
