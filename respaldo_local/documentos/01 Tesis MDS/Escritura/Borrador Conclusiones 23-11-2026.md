# Borrador: Conclusiones

> [!info] Estado
> Borrador redactado el 23-11-2026 a pedido de Mario, a partir de `documentacion/Cierre_Experimental_Final_23-11-2026.md` y de los informes del repositorio. Complementa a [[Borrador Resultados y Discusión 23-11-2026]] y a [[Borrador Discusión fisiológica 23-11-2026]]; no reemplaza a [[Estructura Tesis]], donde el Capítulo 9 sigue *(pendiente)*. Las cifras son AUC por persona con intervalo de confianza de 95 %. Redacción ajustada el mismo día a la auditoría final de resultados (`repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/AUDITORIA_EXPERIMENTO.md`), que reprodujo las cifras y pidió moderar varias lecturas.

> [!warning] Decisiones abiertas que este texto no cierra
> No hay aprobación registrada del profesor guía. El borrador supone, de forma provisoria: (1) que "emociones" se presenta como activación (*arousal*); (2) que el margen práctico es 0,02; (3) que la etiqueta de atención es la original y la corregida por posición se informa como análisis; (4) el encuadre de apoyo parcial; (5) que la cohorte nueva queda como trabajo futuro. Si alguna cambia, hay que revisar las secciones 9.1 y 9.6.

## Capítulo 9: Conclusiones

### 9.1 Respuesta a la hipótesis

La hipótesis planteaba que los modelos temporales multimodales obtienen un mejor desempeño fuera de muestra que los modelos estáticos comparables. Los resultados la apoyan de forma parcial: el apoyo proviene de la activación y no de la atención. Todos los análisis usan las mismas 41 personas, que ya se habían consultado, por lo que ninguno es una confirmación independiente.

En activación, agregar el historial de las señales mejora la predicción del *Arousal Score*. El apoyo más sólido es el contraste registrado antes de correr: el historial, sin los 6 s que definen la etiqueta, supera a un placebo de la misma persona (+0,046 [+0,018; +0,073]). Al repetirlo con cinco particiones el resultado se mantiene (+0,047 [+0,017; +0,078]). El contraste simple entre el modelo con y sin historial es menos estable: en la partición registrada el 16-11 fue inconcluso (+0,034 [−0,001; +0,069]) y al promediar cinco particiones quedó respaldado (+0,036 [+0,010; +0,065]). El efecto es además desigual entre personas (mediana +0,014; mejoran 23 de 41).

Sobre su alcance, solo hay respaldo para los 6 s anteriores. A 12 s el resultado es inconcluso (+0,024), y desde los 24 s el historial no se distingue del placebo, sin que eso demuestre que el efecto desaparece. Los controles por tiempo de sesión y por posición dentro del estímulo conservan el signo y el tamaño (+0,026 y +0,032), pero quedan inconclusos.

En atención, el modelo con historial también rinde mejor (+0,029 [+0,021; +0,037]), pero esa ventaja no es información temporal. Cuando el modelo conoce la posición de la ventana dentro del estímulo, el historial no agrega nada (+0,001 [−0,002; +0,005]). Lo que el historial capturaba es que el *Attention Score* sigue un patrón sistemático al inicio de cada página.

En ninguna de las dos variables el orden de las ventanas aportó de forma demostrable: la red recurrente no superó al resumen estadístico del historial y en atención rindió 0,040 menos.

### 9.2 Fusión y aporte de cada señal

La comparación de estrategias de fusión no permite concluir que una sea mejor. Entre redes de una misma familia (perceptrón multicapa), la fusión tardía superó a la temprana en atención (+0,012 [+0,005; +0,021]), en un contraste secundario sin corrección. Con HistGradientBoosting, en el cierre V3, el signo fue el contrario (−0,010 [−0,018; −0,003] en entrenamiento). En activación ninguna estrategia se distinguió de las demás. La fusión no es el factor que explica el desempeño.

En atención la detección depende casi por completo del EEG; la GSR no agrega nada (+0,002). En activación no se demostró el aporte de ninguna señal por separado: las importancias por permutación sugieren al EEG y al historial, pero son descriptivas y ruidosas.

### 9.3 Qué detecta el EEG

El *Modelo Estudiante* de atención alcanza una AUC de 0,681 con el EEG, y una red convolucional sobre la señal cruda llega a 0,716. Una parte de esa detección es la huella eléctrica de los movimientos oculares y los parpadeos. Al retirar tres componentes oculares, que representan 3,5 % de la varianza, la AUC baja a 0,621; un control que retira 72 % de la varianza no ocular la deja en 0,674. La caída equivale a cerca de un tercio de lo que el modelo tiene sobre el azar (0,060 de 0,181) y es una cota inferior, porque la limpieza es parcial. El modelo limpio sigue sobre el azar en las 41 personas. El remanente conserva el patrón espacial y espectral del artefacto, de modo que no puede descartarse que también sea ocular, pero el diseño no lo separa.

La red también depende de lo ocular: pierde 0,067 al limpiar la señal. Su ventaja sobre el modelo de referencia, en cambio, se mantiene con el EEG limpio (+0,028 frente a +0,035).

De aquí se desprende la conclusión metodológica más importante del trabajo. La regla de no-circularidad separa las señales con que se construye la etiqueta de las señales con que se predice, pero no asegura independencia fisiológica entre ellas. La etiqueta de atención se define con la conducta ocular, es decir, con lo **Observado**, y el EEG registra esa misma conducta. Con estos datos no se puede afirmar que el modelo detecte lo **Atendido** a partir de actividad cerebral.

En activación, no se demostró que el EEG de la ventana actual detecte el *Arousal Score* (0,524 con variables calculadas y 0,498 con la red), ni que un modelo más complejo ayude. El desempeño más alto en activación se obtuvo al adaptar el modelo a cada persona (+0,045 [+0,023; +0,069]) y al predecir por estímulo (0,587), y aun así es bajo.

### 9.4 Evolución durante la sesión

De forma descriptiva, la proporción de ventanas de activación alta disminuye hacia el final de la sesión (0,37 en el último quinto), lo que es compatible con habituación. La detección de atención mejora a lo largo de la sesión (de 0,65 a 0,71). Ninguno de los dos patrones se sometió a contraste.

### 9.5 Limitaciones

- Las 41 personas incluyen las de validación y test, consultadas en etapas anteriores. Los análisis posteriores al 16-11-2026 son exploratorios o dirigidos; ninguno es una confirmación independiente en personas nuevas.
- El contraste principal de activación se estimó varias veces sobre las mismas personas, con diferencias entre +0,028 y +0,047, y no todos los intervalos excluyen el cero.
- Las pseudoetiquetas se calculan offline, son relativas a la sesión de cada persona y no se validaron contra una medida externa de atención ni de activación.
- La limpieza ocular es parcial: la caída de 0,060 es una cota inferior de la contribución ocular.
- El EEG y el seguidor ocular tienen un desfase de reloj de 0,18 a 0,53 s que no se corrigió.
- En activación las AUC son bajas (0,52 a 0,59), por lo que el efecto temporal tiene interés científico pero poca utilidad práctica con las variables actuales.
- La red convolucional es una sola arquitectura, sin búsqueda de configuración, y su pérdida al limpiar no tiene control propio.

### 9.6 Trabajo futuro

- Confirmar el efecto temporal en activación en una cohorte nueva, con el contraste y el tamaño de muestra definidos de antemano.
- Definir una etiqueta de atención que no dependa de la conducta ocular, o registrar electrooculograma y más canales para separar mejor la actividad cerebral de la ocular.
- Corregir el desfase entre el EEG y el seguidor ocular y analizar el EEG alineado a las fijaciones.
- Evaluar etiquetas y normalizaciones calculadas solo con información previa, para una versión utilizable en línea.

### 9.7 Conclusión general

Las señales de los segundos previos ayudan a predecir la activación, con un efecto pequeño, desigual entre personas y que requiere confirmación en una cohorte nueva. En atención, lo que parecía un aporte temporal es la estructura de la etiqueta dentro de cada estímulo, y al menos un tercio de lo que parecía detección cerebral es conducta ocular registrada por el EEG. El aporte de la tesis es entonces doble: evidencia acotada de que el historial reciente de las señales ayuda a predecir la activación, y una advertencia metodológica sobre el uso de pseudoetiquetas oculares para evaluar modelos basados en EEG.

Fuentes: `documentacion/Cierre_Experimental_Final_23-11-2026.md`; `documentacion/auditoria_final_23-11-2026/AUDITORIA_EXPERIMENTO.md`; `resultados/cierre_final_41p_16-11-2026/`, `ampliacion_41p_16-11-2026/`, `cierre_v3_16-11-2026/`, `reapertura_41p_22-11-2026/`, `reapertura_fase3_41p_22-11-2026/`, `enfoques_41p_22-11-2026/`, `limpieza_ocular_41p_23-11-2026/` y `red_cruda_41p_23-11-2026/` (`INFORME.md` de cada una).

## Notas relacionadas
- [[Estructura Tesis]]
- [[Problema e hipótesis]]
- [[Resumen Diseño Etiquetas y Modelos]]
