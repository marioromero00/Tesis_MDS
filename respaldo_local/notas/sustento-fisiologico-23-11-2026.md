# Sustento fisiológico de los resultados del 22 y 23-11-2026

Síntesis del 23-11-2026. Referencias buscadas en OpenAlex ese día: título, autores, revista, año y DOI verificados contra el catálogo. **No se leyeron los textos completos**: lo que se atribuye a cada trabajo viene de su título, su resumen o del conocimiento general del área, y debe confirmarse en la fuente antes de citarlo en el manuscrito. Que estos mecanismos sean la causa en los datos de la tesis es interpretación, salvo donde se indica que los datos lo muestran.

## 1. Por qué los ojos aparecen en el EEG

- **Dipolo córneo-retinal.** La córnea es positiva respecto de la retina; al girar el ojo cambia el potencial en los electrodos cercanos. Plöchl, Ossandón y König (2012) caracterizan estos artefactos registrando EEG y seguimiento ocular a la vez, y distinguen tres fuentes: dipolo córneo-retinal, párpado y potencial de espiga sacádica. Croft y Barry (2000) revisan el problema y los métodos de corrección.
- **Parpadeos.** Iwasaki et al. (2005) describen el efecto del cierre del párpado, los parpadeos y los movimientos oculares sobre el EEG: el párpado al deslizarse sobre la córnea produce una deflexión grande de máximo frontopolar. *En los datos:* 150 µV en Fp1/Fp2, decreciendo hasta unos 20 µV en los posteriores; mirada horizontal con signo opuesto en F7 y F8 en 31 de 37 personas.
- **Potencial de espiga sacádica.** Al inicio de cada sacada los músculos extraoculares producen un potencial breve y de banda ancha. Yuval-Greenberg et al. (2008) mostraron que la respuesta gamma inducida del EEG reflejaba microsacadas; Keren, Yuval-Greenberg y Deouell (2010) caracterizan ese potencial y cómo suprimirlo; Hipp y Siegel (2013) separan la actividad gamma neuronal de la de músculos craneales y oculares. *Relación con los datos:* explica que la detección por alfa y beta también cayera al limpiar (0,593 a 0,547), aunque el dipolo córneo-retinal es de baja frecuencia.

## 2. Por qué la limpieza es parcial y qué puede ser el residuo

- **ICA.** Jung et al. (2000) introducen la separación ciega de fuentes para quitar artefactos oculares. Dimigen (2020) evalúa la ICA en experimentos de visión libre y muestra que su resultado depende mucho del filtrado y de los datos de entrenamiento, y que puede corregir de menos o quitar actividad cerebral. *Relación con los datos:* con 16 canales y visión libre, que la limpieza sea parcial es lo esperable; por eso 0,06 es una cota inferior.
- **Actividad muscular.** Goncharova et al. (2003) muestran que la actividad de los músculos frontal y temporal contamina el EEG en un rango amplio de frecuencias, que alcanza beta y alfa, con máximo en electrodos frontales y temporales.
- **Potenciales ligados a la fijación.** Dimigen et al. (2011) revisan el registro conjunto de EEG y movimientos oculares: tras cada sacada aparece una respuesta visual occipital (respuesta lambda) ligada al inicio de la fijación. Es actividad cerebral, pero sigue a los ojos.
- **Alfa posterior.** Klimesch (2012) revisa el papel de alfa en la atención (inhibición y temporización). Es el candidato más cercano a un marcador cerebral y el más débil en los datos (0,547 tras la limpieza).

## 3. Por qué la red sobre la señal cruda supera al modelo con variables

- Lawhern et al. (2018) proponen EEGNet, una red compacta que aprende filtros temporales y espaciales directamente de la señal.
- *Interpretación propia:* los artefactos oculares tienen forma de onda característica (escalón de la sacada, onda del parpadeo, espiga sacádica) que la potencia por banda promedia. Una red convolucional puede aprender esas formas. Es coherente con que su probabilidad siga el recorrido de la mirada más que la del HGB (Spearman 0,48 frente a 0,41) y con que pierda más al limpiar (0,067 frente a 0,060). No se encontró una referencia verificada específica para esta afirmación.

## 4. Por qué la activación no se detecta desde el EEG

- **Origen de la etiqueta.** La conductancia de la piel refleja la actividad de las glándulas sudoríparas ecrinas bajo control simpático (Boucsein et al., 2012, recomendaciones de la Society for Psychophysiological Research).
- **Vía central.** Critchley (2002) revisa qué ocurre en el cerebro: la respuesta electrodérmica depende de corteza prefrontal ventromedial, cíngulo anterior, amígdala, hipotálamo y tronco. Son estructuras mediales y profundas, poco visibles en un EEG de superficie de 16 canales.
- **Tiempos.** La respuesta de conductancia aparece 1 a 3 s después del estímulo, tarda 1 a 3 s en subir y varios segundos en recuperarse (Boucsein et al., 2012); las respuestas sucesivas se superponen (Benedek y Kaernbach, 2010). *Relación con los datos:* una ventana de EEG de 2 s no coincide con la respuesta, y es coherente con que el historial de 6 a 12 s sí ayudara en activación.
- **EEG y activación tónica.** El grupo de Barry (Barry et al., 2005, 2007) relaciona el nivel de conductancia de la piel en reposo con la potencia alfa global (más activación, menos alfa). Es una relación tónica, entre condiciones o personas; no implica que se pueda detectar ventana a ventana dentro de una persona.
- **Pupila.** Mathôt (2018): la pupila responde a tres cosas, la luz, el enfoque cercano y la activación o esfuerzo mental. Frente a una pantalla de brillo variable, las dos primeras pueden dominar. *Relación con los datos:* agregar pupila y mirada al EEG no mejoró la activación (0,518).

## Referencias

- Barry, R. J., Rushby, J. A., Wallace, M. J., et al. (2005). Caffeine effects on resting-state arousal. *Clinical Neurophysiology*. https://doi.org/10.1016/j.clinph.2005.08.008
- Barry, R. J., Clarke, A. R., Johnstone, S. J., et al. (2007). EEG differences between eyes-closed and eyes-open resting conditions. *Clinical Neurophysiology*. https://doi.org/10.1016/j.clinph.2007.07.028
- Benedek, M., y Kaernbach, C. (2010). A continuous measure of phasic electrodermal activity. *Journal of Neuroscience Methods*. https://doi.org/10.1016/j.jneumeth.2010.04.028
- Boucsein, W., et al. (Society for Psychophysiological Research Ad Hoc Committee on Electrodermal Measures) (2012). Publication recommendations for electrodermal measurements. *Psychophysiology*. https://doi.org/10.1111/j.1469-8986.2012.01384.x
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

Nota sobre años: OpenAlex registra Iwasaki et al. con 2004, Keren et al. con 2009 y Dimigen con 2019 (fecha en línea); aquí se usa el año del volumen, que hay que confirmar. Los autores de Boucsein et al. (2012) aparecen en el catálogo solo como comité.
