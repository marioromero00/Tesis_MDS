# Avances de tesis · guion editable

## 01. ¿Sirve el historial de señales para predecir atención y activación?

Le cuento qué pasó desde la última reunión. Corregí un error en la etiqueta de activación y repetí todo con 41 personas. El historial ayuda a predecir activación, con un efecto pequeño y con respaldo solo para los 6 s previos. En atención la mejora existe pero no viene de las ventanas previas, y cerca de un tercio de lo que detecta el EEG depende de componentes ligados a los ojos, leído como cota inferior. Al final hay siete decisiones que necesito tomar con usted: cinco en la última lámina y dos al pie.

## 02. De qué voy a hablar

Son nueve partes. Lo nuevo desde la última reunión va desde los resultados con 41 personas: de dónde viene la mejora, qué detecta el EEG y las conclusiones.

## 03. La hipótesis

Es la hipótesis tal cual está en el manuscrito. Para probarla comparo siempre el mismo modelo, con la misma etiqueta, y lo único que cambio es si ve las ventanas anteriores; más adelante se ve que con eso el modelo también se entera de cuánto lleva la persona en la página. Dice emociones, pero con GSR lo que mido es activación; eso lo vemos al final.

## 04. Los datos: Toma de Muestra 2, navegación web en laboratorio

Los datos son de la Toma de Muestra 2 del Fondecyt 1231122, en laboratorio, en agosto de 2025. Tobii registra la mirada, la pupila y la GSR en un mismo archivo; el EEG viene aparte, de un OpenBCI de 16 canales a 125 Hz. Los junté por persona y hora, y corté todo en ventanas de dos segundos. No hay expresión facial en este conjunto de datos, y no están documentadas la ubicación de los electrodos, la referencia ni las impedancias. Ojo con “navegación web”: los sitios web son cinco y reúnen 6.423 de las 22.176 ventanas con etiqueta de atención, menos de un tercio; el resto son textos, diseños, estímulos numerados e imágenes, y no tengo documentado su contenido. El 116 cuenta nombres en la exportación, no contenidos comprobados.

## 05. Unas señales arman la etiqueta y otras la predicen

No hay una etiqueta directa, así que la armo con unas señales y la predigo con las otras. En atención la etiqueta sale en la práctica de la mirada: en el Modelo Profesor con PCA la pupila pesa −0,05. En activación es, en lo esencial, el nivel tónico de la GSR. La mediana usa toda la sesión, así que esto no sirve tal cual en línea.

## 06. 48 personas registradas, 41 en el análisis

Se registraron 48 personas. Entrenamiento tiene 25 y validación y test, 8 cada uno. P29 la dejo para un análisis de sensibilidad por un desfase de sincronización. Como las ventanas se solapan, la unidad es la persona: promedio la AUC por persona.

## 07. Qué señales combinan los trabajos recientes

La tendencia es fusionar varias señales con modelos tipo Transformer. Lo más cercano en contexto web es la tesis de Saavedra en el mismo grupo, con EEG y GSR, que no encontró mejora clara con fusión tardía. Ninguno de los que revisé combina estas cuatro señales navegando la web; esa búsqueda la tengo que volver a revisar antes de afirmarlo en la defensa.

## 08. Lo que falta en la literatura y lo que intento aportar

Las tres brechas salen de mi revisión. Cada una tiene su respuesta en el diseño. La comparación de fusión temprana, intermedia y tardía la muestro en resultados.

## 09. Sigo KDD, adaptado en cinco etapas

Uso KDD como marco. Es un proceso iterativo: cuando encontré el error en la etiqueta volví de la evaluación a la transformación, y eso es justamente lo que muestro más adelante.

## 10. Qué hago con cada señal

El EEG es lo que más trabajo tuvo: lo filtro entre 1 y 45 Hz con notch en 50, marco los canales no utilizables y desde octubre lo uso por canal. La pupila no está corregida por el brillo de cada página, porque no hay datos de luminancia; eso está en las limitaciones.

## 11. Cómo comparo un modelo con y sin historial

Elijo los hiperparámetros solo dentro de entrenamiento. Después congelo esa configuración y la evalúo con las 41 personas en validación cruzada por persona. Ojo: esas 25 personas son parte de las 41 que después evalúo, y en activación la elección la decidió el modelo con historial; el detalle va en la lámina 18. El protocolo de cada análisis principal entró al repositorio antes que sus predicciones, aunque siempre sobre personas ya consultadas y sin un registro externo: no es un prerregistro; el de posición lo registré, pero después de ver el placebo. Como las ventanas se solapan, todo lo calculo por persona. El borrador también pide BA, macro-F1 y recall por clase; en esta presentación muestro solo la AUC.

## 12. Dos formas de armar la etiqueta de atención coinciden solo en dos tercios de las ventanas

Probé dos formas de armar la etiqueta de atención: pesos iguales y PCA. Los análisis siguieron con PCA, que es la que los modelos predicen mejor. Eso no es un argumento de validez: que una etiqueta sea más fácil de predecir desde el EEG no significa que mida mejor la atención. Las dos coinciden solo en dos tercios de las ventanas, y cuál queda como definición es una decisión que le traigo.

## 13. Con la etiqueta antigua, tres personas tenían datos anómalos

Esto fue lo que me hizo dudar. P4 casi no tenía señal y aun así todas sus ventanas tenían etiqueta. P34 y P46 tenían muchos puntajes repetidos, o sea empates, y P34 quedaba con 8,6 % de clase alta. Ahí paré de ajustar modelos y revisé la etiqueta.

## 14. El generador mezclaba las ventanas

Repitiendo el cálculo con el error obtengo los mismos puntajes que tenía guardados, así que las AUC de activación de antes no sirven. El 25.992 es el archivo completo, incluidas personas fuera del análisis.

## 15. “Alta” es estar sobre su propia mediana de activación: así se ve en P22

Este es un tramo real de P22. La línea es el puntaje GSR de seis segundos y la punteada, su mediana en toda la sesión. Los puntos azules quedan como “alta” y los grises como “baja”. La etiqueta dice si el puntaje de GSR de P22 está sobre su mediana de la sesión en ese momento; no es una medida validada de activación.

## 16. La etiqueta antigua y la nueva coinciden solo en la mitad de las ventanas

Comparé la etiqueta antigua con la nueva en las mismas ventanas: cambia casi la mitad. Con clases balanceadas, eso es lo que esperaría si no tuvieran relación.

## 17. La etiqueta nueva (V2) deja 11.796 de 22.211 ventanas

Rehice la etiqueta en cuatro pasos. Lo que más saca es pedir cinco ventanas válidas seguidas dentro del mismo estímulo; si hay un hueco o cambia el estímulo, parte de cero. Por calidad se van 401, todas de P4. Las 41 personas mantienen las dos clases.

## 18. Primer análisis con 41 personas (16-11): mejora en atención; en activación, inconcluso

Con las particiones originales, el cierre V3 no mostró una ventaja consistente en ninguna de las dos tareas. Después de ver eso, y para tener más potencia, usé las 41 personas en validación cruzada, con la configuración ya congelada y sin búsqueda: es un cambio de diseño posterior a los datos. Otro límite: las 15 hojas del modelo de activación las elegí con las 25 personas de entrenamiento y la elección la decidió el modelo con historial; el efecto de activación se concentra en esas 25 (+0,055, frente a +0,001 en las otras 16); esa comparación por grupo no estaba registrada. Ese sesgo es posible, no está demostrado. En atención la mejora es +0,026 y mejoran 36 de 41; se repite con otras tres particiones. En activación da +0,034 pero el intervalo de la partición registrada toca el cero.

## 19. En atención, la fusión tardía rinde mejor entre redes MLP; con HGB, no

Con la misma familia de modelo, en atención la fusión tardía le gana a la temprana por +0,012 y también a la intermedia. En activación no se demostraron diferencias (inconcluso). La intermedia que probé es más profunda, así que compara también capacidad. Es un contraste secundario y vale para esta familia (MLP): con HGB, en el cierre V3, el signo fue el contrario (−0,010 en entrenamiento).

## 20. El modelo de atención rinde mejor al final de la sesión y peor en textos

En atención la AUC sube a lo largo de la sesión. Por tipo de página, funciona mejor en sitios web y peor en textos. En activación, la proporción de ventanas altas cae al final, compatible con habituación y también con una deriva lenta de la señal o con el orden de las páginas. La línea gris es la AUC de activación por quinto; es descriptiva y con 34 a 41 personas por punto. Todo esto es descriptivo.

## 21. ¿De dónde viene la mejora?

Comparé el historial real con un placebo y con una sola variable: los segundos que lleva la persona en la página. En atención, el placebo y los segundos solos dan lo mismo que el historial real. En activación, al comparar entre todas las ventanas, el placebo y los segundos no aportan, y el historial sí, incluso sin las ventanas de 6 s que promedia la etiqueta. Ojo: el placebo viene de otras páginas, y dentro de una misma página los segundos sí aportan y no demostré que el historial los supere.

## 22. En atención, la etiqueta depende de cuánto lleva la persona en la página

Al entrar a una página, la etiqueta de atención cae a 37 % entre el segundo 2 y 3 y después sube hasta 62 %. El modelo con historial aprendía eso a través del largo del historial. Lo más probable es que refleje cómo se arma la etiqueta con fijaciones y mirada al cambiar de página; no separé cuánto es conducta y cuánto es el cálculo de las fijaciones. Este análisis lo hice después de ver el placebo, así que es explicativo.

## 23. En activación, el historial de la misma página supera a un placebo de otras páginas

Excluí del historial las ventanas de 6 s que promedia la etiqueta. Ojo: el filtro tónico de la GSR usa toda la sesión, y la etiqueta es en lo esencial el nivel tónico: cerca de un cuarto de su peso cae antes de esas ventanas, así que no puedo decir que no haya solapamiento. Aun así le gana al placebo por +0,046 y mejora en 28 de 41 personas, p Holm 0,004; es positivo tanto en las 25 personas con que elegí la configuración (+0,035) como en las otras 16 (+0,064). Ojo: fijé ese contraste antes de tener sus predicciones, pero después de ver que el historial completo le ganaba al placebo, y el placebo viene de otras páginas. Frente a un modelo que conoce los segundos en la página, el historial sumaba +0,038 en el análisis post hoc del 18-11; el 22-11, con 5 particiones y la posición en ambos modelos, da +0,032 y queda inconcluso tras la corrección. Las cifras del gráfico son del 16 y 18-11. Ojo que el modelo sigue siendo débil: la AUC queda entre 0,55 y 0,58 según el análisis.

## 24. Los parpadeos y los movimientos de los ojos se ven en el EEG

La etiqueta de atención se arma con la mirada y la predigo con EEG. Antes de interpretar eso revisé cuánto de los ojos se cuela en el EEG. El parpadeo pega 150 µV en los dos canales de la frente y baja hasta unos 20 atrás. Ese patrón además es compatible con el montaje por defecto, que no estaba documentado. Otro hallazgo: el EEG va entre 0,18 y 0,53 s atrasado respecto del seguidor ocular; no lo corregí.

## 25. Al quitar los componentes oculares, la detección de atención cae

Por persona separé el EEG en componentes independientes y quité los más ligados a la mirada y a los parpadeos. Con tres, la AUC baja de 0,681 a 0,621, en 39 de 41 personas. El control quita tres componentes no oculares, con veinte veces más varianza, y casi no cambia. Alfa y beta, que parecía lo más limpio, también cae: de 0,593 a 0,547. La limpieza es parcial, así que leo 0,06 como una cota inferior; no es una demostración, porque elijo los componentes con la mirada, que también define la etiqueta. El protocolo entró al repositorio antes que las predicciones.

## 26. Una red sobre la señal cruda rinde más, y también depende de la huella ocular

Probé un modelo más complejo: una red convolucional que aprende directo de la señal cruda. En atención le gana al modelo de referencia, 0,716 contra 0,681, por +0,035; pasa por poco el margen de 0,02, que es una propuesta mía sin aprobar. Pero al quitar los componentes oculares cae a 0,649, y su probabilidad sigue el recorrido de la mirada más que la del modelo de referencia. Su ventaja sobre el modelo de referencia se mantiene con el EEG limpio: +0,028. En activación queda en el azar (0,498 frente a 0,524; comparación inconclusa). Es una sola arquitectura sin búsqueda, y no entrené una red con el filtro de control. Tampoco puedo separar si la ventaja viene de la arquitectura o de la escala por persona que recibe la red. “Cruda” quiere decir sin variables calculadas: la señal está filtrada, escalada por persona y canal y recortada.

## 27. Por qué: el ojo genera señal eléctrica que llega a los electrodos

La explicación fisiológica. El ojo es un dipolo: córnea positiva, retina negativa. Como la etiqueta se define con los ojos, todo lo que los ojos dejan en el EEG la predice. La regla de no usar las mismas señales se cumple, pero no asegura independencia fisiológica. Cerca de un tercio de lo que detecto depende de componentes ligados a lo Observado; lo leo como cota inferior, no es una demostración, y no puedo afirmar que el resto sea lo Atendido. De las 18 referencias, 10 las contrasté con el texto completo y 8 solo con el resumen.

## 28. Por qué puede costar detectar la activación desde el EEG

La etiqueta de activación viene de la GSR, que mide glándulas sudoríparas bajo control simpático. Esa vía es lenta. Ojo: esa latencia vale para las respuestas individuales; mi etiqueta es en lo esencial la componente lenta de la GSR, que llamo nivel tónico e incluye la acumulación de esas respuestas, y es más lenta aún. Una ventana de EEG de 2 s no calza con un nivel que cambia tan lento. Esto es coherente con mi resultado temporal: en activación solo hay respaldo para el historial de los 6 s previos. Además no comprobé la calidad del EEG como registro cerebral, así que este resultado vale para este registro. De las 18 referencias, 8 las contrasté solo con el resumen.

## 29. Qué responde la tesis

La respuesta corta: hay evidencia acotada de que el historial reciente ayuda a predecir activación, con modelos débiles. En atención la mejora existe pero no viene de las ventanas previas. Lo nuevo es la última fila: en atención, cerca de un tercio de lo que el EEG tiene sobre el azar depende de componentes ligados a los ojos, leído como cota inferior, y no puedo descartar que el resto también. Todo esto con datos que ya había consultado antes, así que confirmarlo requiere personas nuevas.

## 30. Conclusiones provisorias: apoyo parcial

Son las conclusiones del borrador del capítulo 9. Con el encuadre provisorio, que es una de las decisiones abiertas, la hipótesis se apoya en parte, y solo por activación. El efecto se sostiene frente al placebo, que viene de otras páginas, pero es pequeño, desigual entre personas (en el contraste con y sin historial mejoran 23 de 41) y con respaldo solo para los 6 s previos: a 12 s es inconcluso (+0,024). En atención, lo que parecía temporal era la posición dentro de la página. Al controlar la posición, el efecto de activación conserva su tamaño (+0,032) pero queda inconcluso. El +0,046 de esta lámina, de la 23 y de la 29 es el contraste registrado el 16-11, después de ver que el historial completo le ganaba al placebo; la curva del 22-11 da +0,047 a 6 s (una partición, 40 personas). Con las particiones originales no había una ventaja consistente, y lo que tiene apoyo es un resumen del historial, no un modelo secuencial ni la combinación de señales.

## 31. Conclusiones: qué detecta el EEG

La conclusión metodológica más importante es la tercera. Cumplí la regla de no-circularidad entre señales, pero el EEG contiene la huella eléctrica de los ojos, así que la etiqueta y la entrada no son independientes. Los tres componentes oculares son el 3,5 % de la varianza, y en activación la red queda en 0,498 frente a 0,524 del modelo de referencia (inconcluso). Estas conclusiones suponen de forma provisoria las decisiones que le consulto en la última lámina.

## 32. Qué falta para cerrar la tesis

Mi propuesta es cerrar aquí. Lo que falta son decisiones y escritura. Sobre la etiqueta: el 22 de noviembre probé una etiqueta de atención corregida por la posición en la página, y hay que decidir si reemplaza a la original. De los opcionales, el único que cambiaría el estatus de los resultados es la cohorte nueva.

## 33. Necesito decidir cinco cosas con usted

La experimentación sobre estas 41 personas la doy por cerrada, salvo que usted indique otra cosa. Lo que más me urge es la primera pregunta, porque define si escribo o recluto. Hay dos puntos más, al pie de la lámina, que pueden pesar más que los anteriores, porque si no se aceptan obligan a repetir análisis: las etiquetas se normalizan con la sesión completa de cada persona y el manuscrito pide normalizar solo con entrenamiento; y los análisis usan el Modelo Profesor con PCA, cuando la nota de diseño proponía la fusión igualitaria. El detalle de cada opción está en la minuta, que además lista los objetivos y contribuciones que conviene revisar, la información de participantes y ética que tengo que pedir al proyecto, y cómo declarar el uso de asistentes automáticos en las revisiones.

## 34. Atención: curvas ROC en test

La AUC de la leyenda es la media de las AUC por persona.

## 35. Activación: curvas ROC en test

Las tres curvas van pegadas a la diagonal.

## 36. Señales

El EEG lo uso por canal desde octubre; antes promediaba los canales.

## 37. Configuración del entrenamiento de activación

La misma configuración para los tres largos de historial.

## 38. Activación: la muestra necesaria va de 72 a 767 según la variabilidad

El número depende mucho de qué variabilidad uso. Las de validación y test salen de 8 personas; la de entrenamiento, de 25 pero mezclando folds, así que 767 es el escenario pesimista. Para las dos tareas manda la de activación; con 20 % de pérdidas serían 90 a 959 a reclutar. Y el +0,02 es una propuesta mía.

## 39. Referencias de la explicación fisiológica

La lista completa con DOI está en la nota de sustento fisiológico. Los años de tres trabajos difieren entre la fecha en línea y la del volumen.