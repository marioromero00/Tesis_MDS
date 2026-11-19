# Avances de tesis · guion editable

## 01. ¿Sirve el historial de señales para predecir atención y activación?

Le cuento qué pasó desde la última reunión. En atención hay una mejora con historial, pero chica. En activación encontré un error en la etiqueta; ya antes el modelo andaba cerca del azar y con la etiqueta corregida sigue igual. Al final hay cuatro cosas que necesito decidir con usted.

## 02. De qué voy a hablar

Son ocho partes. La más larga es la del error en la etiqueta de activación, porque cambió todo lo que tenía de activación.

## 03. La hipótesis

Es la hipótesis tal cual está en el manuscrito. Para probarla comparo siempre el mismo modelo, con la misma etiqueta, y lo único que cambia es si ve las ventanas anteriores. Dice emociones, pero con GSR lo que mido es activación; eso lo vemos al final.

## 04. Los datos: Toma de Muestra 2, navegación web en laboratorio

Los datos son de la Toma de Muestra 2 del Fondecyt 1231122, en laboratorio, en agosto de 2025. Tobii registra la mirada, la pupila y la GSR en un mismo archivo; el EEG viene aparte, de un OpenBCI de 16 canales a 125 Hz. Los junté por persona y hora, y corté todo en ventanas de dos segundos. No hay expresión facial en este set, y la ubicación de los electrodos no está documentada.

## 05. Unas señales arman la etiqueta y otras la predicen

No hay una etiqueta directa, así que la armo con unas señales y la predigo con las otras. La mediana usa toda la sesión, así que esto no sirve tal cual en línea.

## 06. 48 personas registradas, 41 en el análisis

Registré 48 personas. Entrenamiento tiene 25 y validación y test, 8 cada uno. P29 la dejo para un análisis de sensibilidad por un desfase de sincronización. Como las ventanas se solapan, la unidad es la persona: promedio la AUC por persona.

## 07. Qué señales combinan los trabajos recientes

La tendencia es fusionar varias señales con modelos de atención tipo Transformer. Lo más cercano en contexto web es la tesis de Saavedra en el mismo grupo, con EEG y GSR, que no encontró mejora clara con fusión tardía. Ninguno de los que revisé combina estas cuatro señales navegando la web; esa búsqueda la tengo que volver a revisar antes de afirmarlo en la defensa.

## 08. Lo que falta en la literatura y lo que intento aportar

Las tres brechas salen de mi revisión. Cada una tiene su respuesta en el diseño. Lo que todavía no hago es comparar fusión temprana, intermedia y tardía con la etiqueta nueva; está en los pendientes.

## 09. Sigo KDD, adaptado en cinco etapas

Uso KDD como marco. Es un proceso iterativo: cuando encontré el error en la etiqueta volví de la evaluación a la transformación, y eso es justamente lo que muestro más adelante.

## 10. Qué hago con cada señal

El EEG es lo que más trabajo tuvo: lo filtro entre 1 y 40 Hz con notch en 50, saco artefactos y desde octubre lo uso por canal. La pupila todavía no la corrijo por el brillo de cada página; eso está en las limitaciones.

## 11. Cómo comparo un modelo con y sin historial

Elijo los hiperparámetros solo dentro de entrenamiento. Después congelo esa configuración y la evalúo con las 41 personas en validación cruzada por persona. Cada análisis lo registré en GitHub antes de correrlo. Como las ventanas se solapan, todo lo calculo por persona. El borrador también pide BA, macro-F1 y recall por clase; en esta presentación muestro solo la AUC.

## 12. Con PCA, la etiqueta de atención se predice mejor

Probé dos formas de armar la etiqueta de atención: pesos iguales y PCA. Con PCA todos los modelos la predicen mejor y seguí con esa. Las dos coinciden en dos tercios de las ventanas.

## 13. Con la etiqueta antigua había tres personas raras

Esto fue lo que me hizo dudar. P4 casi no tenía señal y aun así todas sus ventanas tenían etiqueta. P34 y P46 tenían muchos puntajes repetidos, o sea empates, y P34 quedaba con 8,6 % de clase alta. Ahí paré de ajustar modelos y revisé la etiqueta.

## 14. El generador mezclaba las ventanas

Repitiendo el cálculo con el error obtengo los mismos puntajes que tenía guardados, así que las AUC de activación de antes no sirven. El 25.992 es el archivo completo, incluidas personas fuera del análisis.

## 15. "Alta" es estar más activado que su propia mediana: así se ve en P22

Este es un tramo real de P22. La línea es el puntaje GSR de seis segundos y la punteada, su mediana en toda la sesión. Los puntos azules quedan como “alta” y los grises como “baja”. La etiqueta dice si P22 está más activada que de costumbre en ese momento.

## 16. La etiqueta antigua y la nueva coinciden solo en la mitad de las ventanas

Comparé la etiqueta antigua con la nueva en las mismas ventanas: cambia casi la mitad. Con clases balanceadas, eso es lo que esperaría si no tuvieran relación.

## 17. La etiqueta nueva (V2) deja 11.796 de 22.211 ventanas

Rehice la etiqueta en cuatro pasos. Lo que más saca es pedir cinco ventanas válidas seguidas dentro del mismo estímulo; si hay un hueco o cambia el estímulo, parte de cero. Por calidad se van 401, todas de P4. Las 41 personas mantienen las dos clases.

## 18. Con 41 personas, el historial mejora atención; en activación no alcanza

Para tener más potencia usé las 41 personas en validación cruzada, con la configuración ya congelada y sin búsqueda. En atención la mejora es +0,026 y mejoran 36 de 41; se repite con otras tres particiones. En activación da +0,034 pero el intervalo de la partición registrada toca el cero.

## 19. ¿De dónde viene la mejora?

Comparé el historial real con un placebo y con una sola variable: los segundos que lleva la persona en la página. En atención, el placebo y los segundos solos dan lo mismo que el historial real. En activación, el placebo y los segundos no aportan, y el historial sí, incluso sin los 6 s que usa la etiqueta.

## 20. En atención, la etiqueta depende de cuánto lleva la persona en la página

Al entrar a una página, la etiqueta de atención cae a 0,37 entre el segundo 2 y 3 y después sube hasta 0,62. El modelo con historial aprendía eso a través del largo del historial. Lo más probable es que refleje cómo se arma la etiqueta con fijaciones y pupila al cambiar de página. Este análisis lo hice después de ver el placebo, así que es explicativo.

## 21. En activación, los segundos previos sí aportan

Excluí del historial los 6 s que definen la etiqueta, para que no haya solapamiento. Aun así le gana al placebo por +0,046 y mejora en 28 de 41 personas, p Holm 0,004. Y controlando los segundos en la página, el historial sigue sumando +0,038. Ojo que el modelo sigue siendo débil: AUC alrededor de 0,57.

## 22. En atención, la fusión tardía rinde mejor

Con la misma familia de modelo, en atención la fusión tardía le gana a la temprana por +0,012 y también a la intermedia. En activación no hay diferencias. La intermedia que probé es más profunda, así que compara también capacidad.

## 23. El modelo de atención rinde mejor al final de la sesión y en sitios web

En atención la AUC sube a lo largo de la sesión. Por tipo de página, funciona mejor en sitios web y peor en textos. En activación, la proporción de ventanas altas cae al final, compatible con habituación. Todo esto es descriptivo.

## 24. Qué responde la tesis

La respuesta corta: el historial de las señales sí ayuda a predecir activación, aunque con modelos débiles. En atención la mejora existe pero no es temporal. Todo esto con datos que ya había consultado antes, así que confirmarlo requiere personas nuevas.

## 25. Necesito decidir cuatro cosas con usted

La experimentación está cerrada y auditada. Lo que más me urge es la primera pregunta, porque define si escribo o recluto.

## 26. Atención: curvas ROC en test

La AUC de la leyenda es la media de las AUC por persona.

## 27. Activación: curvas ROC en test

Las tres curvas van pegadas a la diagonal.

## 28. Señales

La EEG la uso por canal desde octubre; antes promediaba los canales.

## 29. Configuración del entrenamiento de activación

La misma configuración para los tres largos de historial.

## 30. Para activación, la muestra necesaria cambia de 72 a 767 según qué variabilidad use

El número depende mucho de qué variabilidad uso. Las de validación y test salen de 8 personas; la de entrenamiento, de 25 pero mezclando folds, así que 767 es el escenario pesimista. Para las dos tareas manda la de activación; con 20 % de pérdidas serían 90 a 959 a reclutar. Y el +0,02 es una propuesta mía.