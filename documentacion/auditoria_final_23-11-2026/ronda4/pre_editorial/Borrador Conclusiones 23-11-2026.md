# Borrador: Conclusiones

> [!info] Estado
> Borrador redactado el 23-11-2026 a pedido de Mario, a partir de `documentacion/Cierre_Experimental_Final_23-11-2026.md` y de los informes del repositorio. Complementa a [[Borrador Resultados y Discusión 23-11-2026]] y a [[Borrador Discusión fisiológica 23-11-2026]]; no reemplaza a [[Estructura Tesis]], donde el Capítulo 9 sigue *(pendiente)*. Las cifras son AUC por persona con intervalo de confianza de 95 %. Redacción ajustada el mismo día a la auditoría final de resultados (`repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/AUDITORIA_EXPERIMENTO.md`), que reprodujo las cifras y pidió moderar varias lecturas. Esa auditoría es un recálculo con código separado, hecho con un asistente automático a pedido del autor; no es la revisión de un tercero.

> [!warning] Decisiones abiertas que este texto no cierra
> No hay aprobación registrada del profesor guía. El borrador supone, de forma provisoria: (1) que "emociones" se presenta como activación (*arousal*); (2) que el margen práctico es 0,02; (3) que la etiqueta de atención es la original y la corregida por posición se informa como análisis; (4) el encuadre de apoyo parcial; (5) que la cohorte nueva queda como trabajo futuro; (6) que se aceptan las etiquetas normalizadas con la sesión completa, declaradas como límite; (7) que el profesor PCA define el *Attention Score*. Las siete están en [[Avance - 23-11-2026 (Minuta de decisiones con el profesor)]] y ninguna está tomada. Si alguna cambia, hay que revisar las secciones 9.1, 9.5 y 9.6.

## Capítulo 9: Conclusiones

### 9.1 Respuesta a la hipótesis

La hipótesis planteaba que los modelos temporales multimodales obtienen un mejor desempeño fuera de muestra que los modelos estáticos comparables. Los resultados la apoyan de forma parcial: el apoyo proviene de la activación y no de la atención, y se refiere al historial reciente de las señales resumido con estadísticos, no a un modelo secuencial ni a la combinación de señales, cuyo aporte no se demostró. Todos los análisis usan las mismas 41 personas, que ya se habían consultado, por lo que ninguno es una confirmación independiente. Con las particiones originales de entrenamiento, validación y test no se había observado una ventaja consistente en ninguna de las dos variables; el apoyo parcial surge del análisis posterior con las 41 personas.

En activación, agregar el historial de las señales mejora la predicción del *Arousal Score*. El apoyo más sólido es el contraste registrado antes de correr: el historial, sin las ventanas de 6 s que promedia la etiqueta (pero dentro del soporte de su filtro tónico, que usa toda la sesión), supera a un placebo de la misma persona (+0,046 [+0,018; +0,073]). La etiqueta es en lo esencial el nivel tónico de la GSR, y cerca de un cuarto de su peso cae antes de esas ventanas, de modo que el contraste no demuestra por sí solo que el pasado prediga el presente. Un análisis distinto del 22-11, la curva temporal, da un valor parecido para la banda de los 6 s anteriores (+0,047 [+0,017; +0,078]; una partición, 40 personas); no es una repetición del mismo contraste. El contraste simple entre el modelo con y sin historial es menos estable: en la partición registrada el 16-11 fue inconcluso (+0,034 [−0,001; +0,069]) y al promediar cinco particiones quedó respaldado (+0,036 [+0,010; +0,065]). El efecto es además desigual entre personas (mediana +0,014; mejoran 23 de 41) y se concentra en las 25 personas con que se eligió la configuración (+0,046, frente a +0,021 en las otras 16): las 15 hojas del modelo de activación las decidió el modelo con historial, lo que permite un sesgo a su favor en esas personas. Ese sesgo es posible y no está demostrado; el contraste del historial desplazado frente al placebo es positivo en ambos grupos (+0,035 y +0,064).

Sobre su alcance, solo hay respaldo para los 6 s anteriores. A 12 s el resultado es inconcluso (+0,024), y desde los 24 s el historial no se distingue del placebo, sin que eso demuestre que el efecto desaparece. Los controles por tiempo de sesión y por posición en el estímulo conservan el signo y un tamaño parecido (+0,026 y +0,032), pero quedan inconclusos; al comparar solo ventanas de un mismo estímulo la diferencia baja a +0,009 [−0,020; +0,037], también inconclusa.

En atención, el modelo con historial también rinde mejor (+0,029 [+0,021; +0,037]), pero esa ventaja no proviene de la fisiología de las ventanas previas: la reproduce un solo dato, el tiempo transcurrido en el estímulo. Cuando el modelo conoce la posición de la ventana dentro del estímulo, el historial no agrega nada (+0,001 [−0,002; +0,005]). Lo que el historial capturaba es que el *Attention Score* sigue un patrón sistemático al inicio de cada página.

En ninguna de las dos variables el orden de las ventanas aportó de forma demostrable: la red recurrente no superó al resumen estadístico del historial y en atención rindió 0,040 menos.

### 9.2 Fusión y aporte de cada señal

La comparación de estrategias de fusión no permite concluir que una sea mejor. Entre redes de una misma familia (perceptrón multicapa), la fusión tardía superó a la temprana en atención (+0,012 [+0,005; +0,021]), en un contraste secundario sin corrección. Con HistGradientBoosting, en el cierre V3, el signo fue el contrario (−0,010 [−0,018; −0,003] en entrenamiento). En activación ninguna estrategia se distinguió de las demás, con intervalos anchos (inconcluso). Estos contrastes no permiten elegir una fusión ni atribuirle el desempeño.

En atención la detección depende casi por completo del EEG; la GSR no agrega nada (+0,002). En activación no se demostró el aporte de ninguna señal por separado: las importancias por permutación sugieren al EEG y al historial, pero son descriptivas y ruidosas.

### 9.3 Qué detecta el EEG

El *Modelo Estudiante* de atención alcanza una AUC de 0,681 con el EEG, y una red convolucional sobre la señal cruda llega a 0,716. Una parte de esa detección depende de componentes del EEG ligados a los movimientos oculares y los parpadeos. Al retirar tres componentes oculares, que representan 3,5 % de la varianza, la AUC baja a 0,621; un control que retira tres componentes no oculares, que suman 72 % de la varianza, la deja en 0,674. La caída equivale a cerca de un tercio de lo que el modelo tiene sobre el azar (0,060 de 0,181) y se lee como una cota inferior, porque la limpieza es parcial; es la lectura más defendible y no una demostración, porque los componentes se eligen con la mirada y pueden arrastrar actividad no ocular. El modelo limpio sigue sobre el azar en las 41 personas. El remanente conserva el patrón espacial y espectral del artefacto, de modo que no puede descartarse que también sea ocular, pero el diseño no lo separa.

La red también depende de lo ocular: pierde 0,067 al limpiar la señal. Su ventaja sobre el modelo de referencia, en cambio, se mantiene con el EEG limpio (+0,028 frente a +0,035).

De aquí se desprende la conclusión metodológica más importante del trabajo. La regla de no-circularidad separa las señales con que se construye la etiqueta de las señales con que se predice, pero no asegura independencia fisiológica entre ellas. La etiqueta de atención se define con la conducta ocular, es decir, con lo **Observado**, y el EEG registra esa misma conducta. Con estos datos no se puede afirmar que el modelo detecte lo **Atendido** a partir de actividad cerebral.

En activación, no se demostró que el EEG de la ventana actual detecte el *Arousal Score* (0,524 con variables calculadas y 0,498 con la red), ni que un modelo más complejo ayude. Las mayores mejoras en activación se obtuvieron al adaptar el modelo a cada persona (+0,045 [+0,023; +0,069] sobre el modelo con historial) y al predecir por estímulo (AUC 0,587), y aun así es bajo.

### 9.4 Evolución durante la sesión

De forma descriptiva, la proporción de ventanas de activación alta disminuye hacia el final de la sesión (0,37 en el último quinto), lo que es compatible con habituación, y también con una deriva lenta de la señal o con el orden de los estímulos; se midió con la etiqueta binaria y no con el score continuo. La detección de atención mejora a lo largo de la sesión (de 0,65 a 0,71 entre el primer y el último quinto con el modelo sin historial; de 0,69 a 0,74 con historial). Ninguno de los dos patrones se sometió a contraste.

### 9.5 Limitaciones

- Las 41 personas incluyen las de validación y test, consultadas en etapas anteriores. Los análisis posteriores al 16-11-2026 son exploratorios o dirigidos; ninguno es una confirmación independiente en personas nuevas.
- El contraste principal de activación se estimó varias veces sobre las mismas personas, con diferencias entre +0,028 y +0,047, y no todos los intervalos excluyen el cero.
- El diseño de evaluación cambió después de un resultado nulo: con las particiones originales no hubo una ventaja consistente, y el análisis con 41 personas se registró a continuación.
- **Selección de la configuración.** Las 15 hojas del modelo de activación se eligieron con la AUC media de los modelos con 1, 8 y 32 ventanas, la elección la decidió el de 32, y las 25 personas de esa búsqueda son 25 de las 41 evaluadas. El contraste principal se concentra en ellas (+0,055 frente a +0,001 el 16-11; +0,046 frente a +0,021 con cinco particiones) y con las particiones originales el patrón había sido el inverso: el efecto no es estable entre subconjuntos de personas ni entre diseños de evaluación (sección 7.1). El sesgo a favor del historial es posible y no está demostrado: la diferencia entre grupos no es significativa con 16 personas, y el historial desplazado frente al placebo y la GRU son positivos en ambos grupos. No se corrió una sensibilidad con 7 hojas ni con selección anidada.
- La etiqueta de activación es en lo esencial el nivel tónico de la GSR relativo a la sesión, y su soporte real excede los 6 s: en su parte tónica, el 49 % del peso de la GSR cae en las ventanas nominales, el 25 % antes y el 25 % después. El contraste "sin las ventanas de la etiqueta" no excluye ese soporte y no separa por sí solo "el pasado predice el presente" de una relación entre señales del mismo momento.
- La etiqueta de atención es, en la práctica, conducta de mirada: la pupila pesa −0,052 en el profesor PCA, y las variables de fijación suman la duración completa de las fijaciones que tocan la ventana.
- Los resultados de activación se refieren al 53 % de las ventanas que conserva la etiqueta: desde la quinta ventana de cada estímulo, en estímulos suficientemente largos. No describen el inicio de cada página ni los estímulos breves.
- La AUC por persona pesa igual a todas las personas, sin un mínimo de ventanas: la persona más influyente del contraste principal de activación conserva 26 ventanas con etiqueta.
- La validación cruzada separa personas, no grupos experimentales, y las personas de un mismo grupo vieron los estímulos en el mismo orden; no se evaluó dejando grupos completos fuera.
- Las pseudoetiquetas se calculan offline, son relativas a la sesión de cada persona y no se validaron contra una medida externa de atención ni de activación. La etiqueta de atención usada (profesor PCA) coincide con la de pesos iguales en 66 % de las ventanas, y se siguió con ella tras observar que se predecía mejor, lo que no es un argumento de validez.
- Ocho filas cumplen dos reglas de decisión a la vez y su rótulo (seis "inferior" y dos "respaldo", todas en atención) depende de una precedencia que los protocolos no fijan.
- La limpieza ocular es parcial y elige los componentes con la mirada: la caída de 0,060 se lee como cota inferior de la contribución ocular, sin que sea una demostración.
- El EEG y el seguidor ocular tienen un desfase de reloj de 0,18 a 0,53 s que no se corrigió y cuyo efecto no se midió.
- En activación las AUC son bajas (0,50 a 0,59), por lo que el efecto temporal tiene interés científico pero poca utilidad práctica con las variables actuales.
- La red convolucional es una sola arquitectura, sin búsqueda de configuración, y su pérdida al limpiar no tiene control propio.
- Los contrastes secundarios no llevan corrección por multiplicidad. La corrección de Holm se aplica dentro de cada etapa y no entre etapas: son doce etapas de análisis sobre las mismas 41 personas. El explicativo de posición y la fase 2 de la reapertura son post hoc.

### 9.6 Trabajo futuro

- Confirmar el efecto temporal en activación en una cohorte nueva, con el contraste y el tamaño de muestra definidos de antemano.
- Definir una etiqueta de atención que no dependa de la conducta ocular, o registrar electrooculograma y más canales para separar mejor la actividad cerebral de la ocular.
- Corregir el desfase entre el EEG y el seguidor ocular y analizar el EEG alineado a las fijaciones.
- Evaluar etiquetas y normalizaciones calculadas solo con información previa, para una versión utilizable en línea.

### 9.7 Conclusión general

Hay evidencia acotada de que las señales de los segundos previos ayudan a predecir la activación, con un efecto pequeño, desigual entre personas y que requiere confirmación en una cohorte nueva. En atención, lo que parecía un aporte temporal es la estructura de la etiqueta dentro de cada estímulo, y cerca de un tercio de la detección sobre el azar depende de componentes del EEG ligados a la conducta ocular, sin que el resto pueda atribuirse a un origen cerebral ni ocular. El aporte de la tesis sería entonces doble (encuadre provisorio, que depende de la decisión abierta sobre el encuadre: el punto 4 del aviso inicial y la decisión 5 de la minuta): evidencia acotada de que el historial reciente de las señales ayuda a predecir la activación, y una advertencia metodológica sobre el uso de pseudoetiquetas oculares para evaluar modelos basados en EEG.

Fuentes: `documentacion/Cierre_Experimental_Final_23-11-2026.md`; `documentacion/auditoria_final_23-11-2026/AUDITORIA_EXPERIMENTO.md`; `resultados/cierre_final_41p_16-11-2026/`, `ampliacion_41p_16-11-2026/`, `cierre_v3_16-11-2026/`, `reapertura_41p_22-11-2026/`, `reapertura_fase3_41p_22-11-2026/`, `enfoques_41p_22-11-2026/`, `limpieza_ocular_41p_23-11-2026/` y `red_cruda_41p_23-11-2026/` (`INFORME.md` de cada una).

## Notas relacionadas
- [[Estructura Tesis]]
- [[Problema e hipótesis]]
- [[Resumen Diseño Etiquetas y Modelos]]
