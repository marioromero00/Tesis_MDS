# Borrador: Discusión fisiológica de los resultados con EEG

> [!info] Estado
> Borrador redactado el 23-11-2026 para el Capítulo 8 (Discusión). Complementa a [[Borrador Resultados y Discusión 18-11-2026]]; no lo reemplaza ni cierra decisiones abiertas de [[Resumen Diseño Etiquetas y Modelos]]. Las cifras son AUC por persona y provienen de los informes del repositorio indicados al final de cada sección. Las referencias se verificaron en OpenAlex el 23-11-2026 (título, autores, revista y DOI), pero **no se leyeron los textos completos**: cada afirmación atribuida debe confirmarse en la fuente antes de pasar a LaTeX. La numeración de secciones es provisoria.

## 8.x Qué detecta el Modelo Estudiante de atención a partir del EEG

### 8.x.1 La huella de los ojos en el EEG

El *Attention Score* se construye con variables de mirada y pupila, y el *Modelo Estudiante* lo predice principalmente desde el EEG: al permutar el EEG la AUC cae 0,207, y al permutar la GSR, 0,004. La regla de no-circularidad se cumple en el nivel de las señales de entrada, pero no garantiza que el EEG sea independiente de los ojos. El ojo se comporta como un dipolo eléctrico, con la córnea positiva respecto de la retina, de modo que cada rotación del globo ocular modifica el potencial que registran los electrodos cercanos (Croft y Barry, 2000; Plöchl, Ossandón y König, 2012). Los parpadeos agregan una deflexión de gran amplitud y máximo frontopolar, producida por el deslizamiento del párpado sobre la córnea (Iwasaki et al., 2005). A estas dos fuentes se suma el potencial de espiga sacádica, una descarga breve y de banda ancha de los músculos extraoculares al inicio de cada sacada, que contamina las frecuencias altas del EEG (Yuval-Greenberg et al., 2008; Keren, Yuval-Greenberg y Deouell, 2010; Hipp y Siegel, 2013).

Los registros de esta tesis muestran ese patrón. La respuesta promedio al parpadeo alcanza unos 150 µV en los dos canales frontopolares y decrece hasta unos 20 µV en los posteriores, y la mirada horizontal entra con signo opuesto en los canales frontales laterales en 31 de las 37 personas con ambos canales utilizables. Este gradiente es además compatible con el montaje por defecto del equipo, que no estaba documentado.

Fuente: `resultados/montaje_ocular_41p_23-11-2026/INFORME.md`.

### 8.x.2 Cuánto de la detección depende de los componentes oculares

Al retirar del EEG de cada persona los tres componentes independientes más asociados a la mirada y a los parpadeos, la AUC de atención baja de 0,681 a 0,621 (diferencia 0,060; IC 95 % [0,045; 0,075]; 39 de 41 personas). Esos componentes representan una mediana de 3,5 % de la varianza de la señal. Un control que retira tres componentes no oculares, con una mediana de 72 % de la varianza, deja la AUC en 0,674. La caída es, por lo tanto, propia de los componentes oculares y no una consecuencia de quitar señal.

La detección basada en las bandas alfa y beta, que antes de la limpieza parecía la parte menos expuesta al artefacto, también disminuye (de 0,593 a 0,547). Este resultado es coherente con la literatura: el dipolo córneo-retinal se concentra en frecuencias bajas, pero el potencial de espiga sacádica y la actividad de los músculos frontal y temporal alcanzan las bandas beta y alfa (Goncharova et al., 2003; Hipp y Siegel, 2013).

La cifra de 0,060 debe leerse como una cota inferior. La separación por componentes independientes, propuesta para este fin por Jung et al. (2000), es imperfecta en condiciones de exploración visual libre: puede dejar artefacto residual o retirar actividad cerebral, según el filtrado y los datos con que se ajusta (Dimigen, 2020). Con 16 canales la separación es necesariamente gruesa, y en estos datos la limpieza fue parcial: la correlación máxima entre algún canal y los parpadeos baja de 0,28 a 0,08, sin anularse, y la probabilidad del modelo limpio sigue asociada al recorrido de la mirada (correlación de Spearman 0,28).

Fuente: `resultados/limpieza_ocular_41p_23-11-2026/INFORME.md`.

### 8.x.3 Qué puede explicar la detección que permanece

Tras la limpieza, el modelo sigue por sobre el azar (0,621 con todas las variables; 0,55–0,56 con alfa y beta o con canales posteriores). El diseño no permite atribuir ese remanente a una sola fuente. Hay al menos cuatro candidatos:

1. **Artefacto ocular residual.** El remanente conserva el patrón espacial y espectral del artefacto: los canales frontales superan a los posteriores y la potencia lenta supera a alfa y beta.
2. **Actividad muscular** de la frente y las sienes asociada a los movimientos de los ojos (Goncharova et al., 2003).
3. **Respuesta visual ligada a cada fijación.** Después de cada sacada aparece en la corteza occipital una respuesta a la nueva imagen, conocida como respuesta lambda (Dimigen et al., 2011). Es actividad cerebral, pero su ocurrencia está determinada por los movimientos de los ojos.
4. **Modulación de alfa posterior.** La potencia alfa se relaciona con la atención y con la inhibición de regiones no relevantes para la tarea (Klimesch, 2012). Es el candidato más cercano a un correlato cerebral de la atención y, a la vez, el más débil en estos datos.

Como la etiqueta se define con la conducta ocular, las cuatro fuentes covarían con ella y no pueden separarse. En términos del diseño, el *Modelo Estudiante* recupera desde el EEG sobre todo lo **Observado**, y estos datos no permiten afirmar que detecte lo **Atendido**.

### 8.x.4 Un modelo más complejo aprovecha mejor la misma huella

Una red convolucional compacta que aprende directamente de la señal cruda (del tipo EEGNet; Lawhern et al., 2018) supera al modelo con variables calculadas: 0,716 frente a 0,681 (diferencia 0,035; IC 95 % [0,023; 0,047]; 32 de 41 personas). Sin embargo, al retirar los componentes oculares la red cae a 0,649, una pérdida algo mayor que la del modelo de referencia (0,067 frente a 0,060), y su probabilidad se asocia con el recorrido de la mirada más que la del modelo de referencia (correlación de Spearman 0,48 frente a 0,41).

Una explicación plausible, que este trabajo no puso a prueba, es que los artefactos oculares tienen formas de onda características —el escalón de una sacada, la onda de un parpadeo— que las variables de potencia por banda promedian y que una red convolucional puede aprender. En consecuencia, la mayor capacidad del modelo no cambia la interpretación: mejora la detección de la conducta ocular a través del EEG.

Este resultado tiene dos límites. La ventaja supera el margen de relevancia de 0,02 por poco, y no se entrenó una red con el filtro de control, por lo que la especificidad ocular de su pérdida descansa en el control del modelo de referencia.

Fuente: `resultados/red_cruda_41p_23-11-2026/INFORME.md`.

## 8.y Por qué el Arousal Score no se detecta desde el EEG

Con la ventana actual, ningún modelo queda claramente por sobre el azar en activación: 0,524 con el EEG, 0,518 al agregar mirada y pupila, y 0,499 con la red convolucional sobre la señal cruda. La fisiología de la respuesta electrodérmica ofrece tres explicaciones compatibles con este resultado.

**Origen de la señal.** La conductancia de la piel refleja la actividad de las glándulas sudoríparas ecrinas, bajo control del sistema nervioso simpático (Boucsein et al., 2012). Su regulación central involucra a la corteza prefrontal ventromedial, el cíngulo anterior, la amígdala, el hipotálamo y el tronco encefálico (Critchley, 2002). Se trata de estructuras mediales y profundas, cuya actividad contribuye poco a un EEG de superficie de 16 canales.

**Escala temporal.** La respuesta de conductancia comienza entre 1 y 3 s después del evento que la provoca, tarda un tiempo similar en alcanzar su máximo y varios segundos en recuperarse (Boucsein et al., 2012); las respuestas sucesivas se superponen (Benedek y Kaernbach, 2010). Una ventana de EEG de 2 s no coincide con la respuesta que define la etiqueta. Esta diferencia de escalas es coherente con el resultado temporal de la tesis: el historial de los segundos previos mejora la predicción del *Arousal Score*, y lo hace con información local de 6 a 12 s.

**Tipo de relación.** La relación documentada entre el EEG y la conductancia de la piel es tónica: en reposo, un mayor nivel de conductancia se asocia con menor potencia alfa global (Barry et al., 2005, 2007). Esa relación se observa entre condiciones o entre personas, y no implica que el estado de activación pueda distinguirse ventana a ventana dentro de una misma sesión. Además, el *Arousal Score* es relativo a la mediana de cada persona, y la navegación web produce un rango de activación estrecho.

En cuanto a la pupila, su diámetro responde a la luz, al enfoque cercano y a la activación o el esfuerzo mental (Mathôt, 2018). Frente a una pantalla cuyo brillo cambia con el contenido, las dos primeras respuestas pueden dominar sobre la tercera, lo que ayudaría a explicar que la pupila no aporte a la detección de la activación en la ventana actual.

El resultado de la red convolucional es específico de una arquitectura y una configuración, sin búsqueda de hiperparámetros ni registro de convergencia. No permite concluir que el EEG crudo carezca de información sobre la activación.

Fuentes: `resultados/red_cruda_41p_23-11-2026/INFORME.md`, `resultados/enfoques_41p_22-11-2026/`.

## 8.z Implicancias para el diseño

- **La no-circularidad entre señales no asegura independencia fisiológica.** El EEG contiene una copia eléctrica de la conducta ocular con que se construye el *Attention Score*. El resultado de atención debe presentarse como detección de la conducta ocular a través de su huella en el EEG, no como un marcador cerebral de atención.
- **Sincronía entre equipos.** El EEG va entre 0,18 y 0,53 s atrasado respecto del seguidor ocular. El desfase no se corrigió y atenúa cualquier relación entre el EEG y las demás señales.
- **Para separar lo Observado de lo Atendido** se requiere una etiqueta de atención que no dependa de los ojos (por ejemplo, desempeño en una tarea), o un diseño que mantenga la conducta ocular constante entre condiciones.
- **Para la activación**, la escala temporal de la respuesta electrodérmica sugiere trabajar con ventanas más largas o con la componente tónica, en lugar de ventanas de 2 s.

## Limitaciones de esta sección

- Los análisis del 22 y 23-11-2026 son dirigidos, sobre personas y resultados ya vistos; no son una confirmación independiente.
- La limpieza usa la sesión completa de cada persona y la mirada para elegir los componentes; la calidad de la limpieza se mide en los mismos datos.
- Las explicaciones fisiológicas son compatibles con los resultados, pero el diseño no las pone a prueba.

## Referencias

- Barry, R. J., Rushby, J. A., Wallace, M. J., et al. (2005). Caffeine effects on resting-state arousal. *Clinical Neurophysiology*. https://doi.org/10.1016/j.clinph.2005.08.008
- Barry, R. J., Clarke, A. R., Johnstone, S. J., et al. (2007). EEG differences between eyes-closed and eyes-open resting conditions. *Clinical Neurophysiology*. https://doi.org/10.1016/j.clinph.2007.07.028
- Benedek, M., y Kaernbach, C. (2010). A continuous measure of phasic electrodermal activity. *Journal of Neuroscience Methods*. https://doi.org/10.1016/j.jneumeth.2010.04.028
- Boucsein, W., et al. (2012). Publication recommendations for electrodermal measurements. *Psychophysiology*. https://doi.org/10.1111/j.1469-8986.2012.01384.x
- Critchley, H. D. (2002). Electrodermal responses: what happens in the brain. *The Neuroscientist*. https://doi.org/10.1177/107385840200800209
- Croft, R. J., y Barry, R. J. (2000). Removal of ocular artifact from the EEG: a review. *Neurophysiologie Clinique*. https://doi.org/10.1016/s0987-7053(00)00055-1
- Dimigen, O. (2020). Optimizing the ICA-based removal of ocular EEG artifacts from free viewing experiments. *NeuroImage*. https://doi.org/10.1016/j.neuroimage.2019.116117
- Dimigen, O., Sommer, W., Hohlfeld, A., et al. (2011). Coregistration of eye movements and EEG in natural reading: analyses and review. *Journal of Experimental Psychology: General*. https://doi.org/10.1037/a0023885
- Goncharova, I. I., McFarland, D. J., Vaughan, T. M., et al. (2003). EMG contamination of EEG: spectral and topographical characteristics. *Clinical Neurophysiology*. https://doi.org/10.1016/s1388-2457(03)00093-2
- Hipp, J. F., y Siegel, M. (2013). Dissociating neuronal gamma-band activity from cranial and ocular muscle activity in EEG. *Frontiers in Human Neuroscience*. https://doi.org/10.3389/fnhum.2013.00338
- Iwasaki, M., Kellinghaus, C., Alexopoulos, A. V., et al. (2005). Effects of eyelid closure, blinks, and eye movements on the electroencephalogram. *Clinical Neurophysiology*. https://doi.org/10.1016/j.clinph.2004.11.001
- Jung, T.-P., Makeig, S., Humphries, C., et al. (2000). Removing electroencephalographic artifacts by blind source separation. *Psychophysiology*. https://doi.org/10.1111/1469-8986.3720163
- Keren, A. S., Yuval-Greenberg, S., y Deouell, L. Y. (2010). Saccadic spike potentials in gamma-band EEG: characterization, detection and suppression. *NeuroImage*. https://doi.org/10.1016/j.neuroimage.2009.10.057
- Klimesch, W. (2012). Alpha-band oscillations, attention, and controlled access to stored information. *Trends in Cognitive Sciences*. https://doi.org/10.1016/j.tics.2012.10.007
- Lawhern, V. J., Solon, A. J., Waytowich, N. R., et al. (2018). EEGNet: a compact convolutional neural network for EEG-based brain–computer interfaces. *Journal of Neural Engineering*. https://doi.org/10.1088/1741-2552/aace8c
- Mathôt, S. (2018). Pupillometry: psychology, physiology, and function. *Journal of Cognition*. https://doi.org/10.5334/joc.18
- Plöchl, M., Ossandón, J. P., y König, P. (2012). Combining EEG and eye tracking: identification, characterization, and correction of eye movement artifacts in electroencephalographic data. *Frontiers in Human Neuroscience*. https://doi.org/10.3389/fnhum.2012.00278
- Yuval-Greenberg, S., Tomer, O., Keren, A. S., et al. (2008). Transient induced gamma-band response in EEG as a manifestation of miniature saccades. *Neuron*. https://doi.org/10.1016/j.neuron.2008.03.027

Años por confirmar: OpenAlex registra Iwasaki et al. con 2004, Keren et al. con 2009 y Dimigen con 2019 (fecha en línea). Los autores de Boucsein et al. (2012) figuran en el catálogo solo como comité de la Society for Psychophysiological Research.

## Notas relacionadas
- [[Borrador Resultados y Discusión 18-11-2026]]
- [[Estructura Tesis]]
- [[Resumen Diseño Etiquetas y Modelos]]
