# Ensayo de la presentación de avances

Escrito el 23-11-2026 para la versión 7 de la presentación (39 láminas: 33 principales y 6 anexos) y puesto al día ese mismo día, después de la corrección de la presentación: fusión y sesión pasaron a ser las láminas 19 y 20, el bloque "qué explica la mejora" quedó en 21 a 23, y la última lámina pregunta cinco cosas. No reemplaza a `GUIÓN.md`, que se regenera desde `relato.py`; este archivo es solo para ensayar.

**Supuesto de duración.** Mario no fijó cuánto dura la reunión. Este ensayo asume **20 minutos de exposición más preguntas**, y trae una versión corta de 10 minutos por si el tiempo se acorta. Si la duración real es otra, hay que rehacer la tabla.

**Fuentes.** `GUIÓN.md` y `relato.py` de esta carpeta; `documentacion/Cierre_Experimental_Final_23-11-2026.md`; `Escritura/Borrador Conclusiones 23-11-2026.md` y `Escritura/Borrador Discusión fisiológica 23-11-2026.md` del vault; los `INFORME.md` de `resultados/` entre el 16 y el 23-11-2026, más `etiquetas_gsr_calidad_v2_01-11-2026`, `protocolo_hipotesis_reintento_06-11-2026` y `cierre_v3_16-11-2026`. Ante cualquier diferencia mandan los informes.

**Lo que no se puede decir.**

- No consta aprobación del profesor guía sobre los resultados de noviembre ni sobre el margen de 0,02. Lo único registrado es que Mario comunicó el 01-11 que el profesor aprobó usar las etiquetas GSR V2 (`notas/resumen-ultimo-mes-22-11-2026.md`).
- Siguen abiertas cinco decisiones, en el orden de la lámina 33: cohorte nueva o escribir, margen de 0,02, activación en vez de emociones, etiqueta de atención original o corregida por posición, y encuadre de apoyo parcial. Se presentan como preguntas, no como hechos. La normalización con la sesión completa es un sexto punto, menor, que va solo de palabra.
- Nada es una confirmación independiente: las 41 personas ya se habían consultado.
- Términos fijos: Modelo Profesor, Modelo Estudiante, Attention Score, Arousal Score. Distinguir siempre lo Observado (mirar) de lo Atendido (atender).

## Antes de ensayar: lo que todavía no calza en la presentación

Las cinco diferencias grandes de la versión anterior quedaron corregidas en `relato.py` (filtro de 1 a 45 Hz en la lámina 10; activación en las láminas 1, 2 y 18; fusión ya no "pendiente" en la lámina 8; "En parte" en la lámina 29; las mismas cinco decisiones en las láminas 32 y 33). Quedan solo detalles menores; el detalle está en la última sección y el guion hablado de abajo ya los esquiva.

1. Lámina 23: el +0,046 frente al placebo es del 16-11; las láminas 29 y 30 usan el +0,047 del 22-11.
2. Lámina 23: la nota fecha el +0,038 en el 16-11; sale del análisis post hoc del 18-11.
3. Láminas 29 y 30: una dice "a 12 s, inconcluso" y la otra "está en los 6 a 12 s anteriores".
4. Lámina 26: la nota dice que la red "pasa el margen de 0,02", y el margen es una decisión abierta.

---

## 1. Plan de tiempo

### Versión de 20 minutos (1.200 s)

Ritmo: "rápido" es una frase y avanzar; "normal" es el guion completo; "clave" es donde conviene frenar y mirar al profesor.

| Lámina | Título | Segundos | Ritmo | La única idea que hay que dejar |
|---|---|---:|---|---|
| 1 | ¿Sirve el historial de señales para predecir atención y activación? | 25 | normal | Hay resultados nuevos y cinco decisiones que tomar hoy |
| 2 | De qué voy a hablar | 10 | rápido | Nueve partes; lo nuevo son las tres últimas |
| 3 | La hipótesis | 40 | normal | Comparo el mismo modelo con y sin historial |
| 4 | Los datos: Toma de Muestra 2, navegación web en laboratorio | 35 | normal | Cuatro señales, dos equipos, ventanas de 2 s |
| 5 | Unas señales arman la etiqueta y otras la predicen | 50 | clave | Modelo Profesor arma la etiqueta, Modelo Estudiante la predice con otras señales |
| 6 | 48 personas registradas, 41 en el análisis | 35 | normal | La unidad es la persona, y todas ya se habían mirado |
| 7 | Qué señales combinan los trabajos recientes | 25 | rápido | No encontré estas cuatro señales juntas en navegación web |
| 8 | Lo que falta en la literatura y lo que intento aportar | 25 | rápido | Mismo modelo con y sin historial, sobre las mismas ventanas |
| 9 | Sigo KDD, adaptado en cinco etapas | 15 | rápido | El proceso es iterativo: volví atrás por la etiqueta |
| 10 | Qué hago con cada señal | 25 | rápido | El EEG se usa por canal; la pupila no está corregida por brillo |
| 11 | Cómo comparo un modelo con y sin historial | 45 | clave | Configuración congelada y diferencia pareada por persona; el placebo se registró antes y la posición es post hoc |
| 12 | Con PCA, la etiqueta de atención se predice mejor | 20 | rápido | Seguí con PCA; las dos versiones coinciden en dos tercios |
| 13 | Con la etiqueta antigua, tres personas tenían datos anómalos | 30 | normal | Tres personas con datos anómalos me hicieron revisar la etiqueta |
| 14 | El generador mezclaba las ventanas | 35 | clave | El 98 % de los valores GSR quedó en otra ventana; lo anterior de activación no sirve |
| 15 | "Alta" es estar sobre su propia mediana de activación: así se ve en P22 | 20 | rápido | La etiqueta es relativa a cada persona |
| 16 | La etiqueta antigua y la nueva coinciden solo en la mitad de las ventanas | 20 | rápido | La etiqueta antigua no tenía relación con la corregida |
| 17 | La etiqueta nueva (V2) deja 11.796 de 22.211 ventanas | 30 | normal | Se pierde casi la mitad, por exigir continuidad y no por mala señal |
| 18 | Primer análisis con 41 personas (16-11): mejora en atención; en activación, inconcluso | 55 | clave | Con historial atención mejora; activación queda inconclusa el 16-11 y pasa a +0,036 al repetir el 22-11 |
| 19 | En atención, la fusión tardía rinde mejor con el mismo modelo (MLP) | 25 | rápido | La fusión no es lo que explica el desempeño, y vale solo para MLP |
| 20 | El modelo de atención rinde mejor al final de la sesión y peor en textos | 20 | rápido | Es descriptivo |
| 21 | ¿De dónde viene la mejora? | 50 | clave | En atención el placebo rinde igual; en activación no |
| 22 | En atención, la etiqueta depende de cuánto lleva la persona en la página | 45 | normal | Lo que parecía temporal es la posición dentro de la página |
| 23 | En activación, los segundos previos sí aportan | 55 | clave | El historial le gana al placebo sin tocar la etiqueta, con un modelo débil |
| 24 | Los movimientos de los ojos se ven en el EEG | 45 | normal | El parpadeo se ve en la frente; hay un desfase de reloj sin corregir |
| 25 | Al quitar los componentes oculares, la detección de atención cae | 60 | clave | De 0,681 a 0,621 al quitar el 3,5 % de la varianza |
| 26 | Una red sobre la señal cruda rinde más, y su ventaja también depende de la huella ocular | 45 | normal | Un modelo más complejo aprovecha mejor los ojos, no el cerebro |
| 27 | Por qué: el ojo genera señal eléctrica que llega a los electrodos | 35 | normal | Detecto sobre todo lo Observado, no lo Atendido |
| 28 | Por qué puede costar detectar la activación desde el EEG | 35 | normal | La GSR es lenta y profunda; 2 s de EEG no calzan |
| 29 | Qué responde la tesis | 60 | clave | Apoyo parcial, y viene de activación |
| 30 | Conclusiones: la hipótesis tiene apoyo parcial | 40 | normal | Efecto pequeño, de pocos segundos, con AUC bajas |
| 31 | Conclusiones: qué detecta el EEG | 40 | normal | Separar señales no asegura independencia fisiológica |
| 32 | Qué falta para cerrar la tesis | 30 | normal | Faltan decisiones y escritura, no experimentos |
| 33 | Necesito decidir cinco cosas con usted | 75 | clave | ¿Escribo o planifico una cohorte nueva? |
| | **Total** | **1.200** | | |

Subtotales: láminas 1 a 6, 195 s; 7 a 11, 135 s; 12 a 17, 155 s; 18 a 23, 250 s; 24 a 28, 220 s; 29 a 33, 245 s.

- **No se salta ninguna** de las 33 principales.
- **Se pasan rápido** (una frase y avanzar): 2, 7, 8, 9, 10, 12, 15, 16, 19 y 20.
- **Si a los 10 minutos todavía no llego a la lámina 18**, salto 19 y 20 (45 s) y acorto 27 y 28 a una frase cada una.
- **Candidatas a pasar a anexos en una próxima versión**, si se quiere más aire: 9, 12, 15 y 20. No las moví; habría que cambiar `relato.py`.
- **Anexos (láminas 34 a 39):** no se muestran en la exposición. Se abren solo si preguntan:

| Lámina | Anexo | Se abre si preguntan por |
|---|---|---|
| 34 | A. Atención: curvas ROC en test | El desempeño en las 8 personas de test |
| 35 | B. Activación: curvas ROC en test | Qué tan cerca del azar está activación |
| 36 | C. Señales | Qué variables se sacan de cada señal |
| 37 | D. Configuración del entrenamiento de activación | Hiperparámetros y búsqueda |
| 38 | E. Muestra necesaria: de 72 a 767 | La cohorte nueva y el margen de 0,02 |
| 39 | F. Referencias de la explicación fisiológica | El respaldo bibliográfico de las láminas 27 y 28 |

### Versión corta de 10 minutos (600 s)

Se muestran 17 láminas y se saltan 16. Con las flechas hay que pasar por las saltadas sin detenerse, o usar el índice (tecla I).

| Lámina | Título | Segundos | Qué hago | La única idea que hay que dejar |
|---|---|---:|---|---|
| 1 | Portada | 20 | mostrar | Resultados nuevos y cinco decisiones |
| 2 | De qué voy a hablar | 0 | saltar | |
| 3 | La hipótesis | 30 | mostrar | Mismo modelo con y sin historial |
| 4 | Los datos | 0 | saltar | Se dice en una frase en la lámina 5 |
| 5 | Unas señales arman la etiqueta y otras la predicen | 40 | mostrar | Modelo Profesor y Modelo Estudiante usan señales distintas |
| 6 | 48 personas registradas, 41 en el análisis | 25 | mostrar | La unidad es la persona; todas ya vistas |
| 7 | Qué señales combinan los trabajos recientes | 0 | saltar | |
| 8 | Lo que falta en la literatura | 0 | saltar | |
| 9 | KDD | 0 | saltar | |
| 10 | Qué hago con cada señal | 0 | saltar | |
| 11 | Cómo comparo un modelo con y sin historial | 30 | mostrar | Configuración congelada y diferencia pareada por persona |
| 12 | Etiqueta de atención con PCA | 0 | saltar | |
| 13 | Tres personas con datos anómalos | 0 | saltar | Se menciona en la lámina 14 |
| 14 | El generador mezclaba las ventanas | 30 | mostrar | Lo anterior de activación no sirve |
| 15 | Ejemplo en P22 | 0 | saltar | |
| 16 | Antigua y nueva coinciden en la mitad | 0 | saltar | Se menciona en la lámina 14 |
| 17 | La etiqueta nueva (V2) | 20 | mostrar | Quedan 11.796 de 22.211 ventanas |
| 18 | Primer análisis con 41 personas (16-11) | 40 | mostrar | Atención mejora; activación pasa de inconclusa a +0,036 al repetir |
| 19 | Fusión | 0 | saltar | |
| 20 | Sesión y tipo de página | 0 | saltar | |
| 21 | ¿De dónde viene la mejora? | 45 | mostrar | En atención el placebo rinde igual; en activación no |
| 22 | La etiqueta depende de la posición en la página | 30 | mostrar | En atención no es temporal |
| 23 | En activación, los segundos previos sí aportan | 40 | mostrar | Le gana al placebo, con un modelo débil |
| 24 | Los movimientos de los ojos se ven en el EEG | 15 | pasar rápido | El parpadeo se ve en la frente |
| 25 | Al quitar los componentes oculares, la detección cae | 55 | mostrar | De 0,681 a 0,621 |
| 26 | Red sobre la señal cruda | 30 | mostrar | Más complejo, misma huella ocular |
| 27 | Por qué: el ojo | 0 | saltar | Se dice en una frase en la lámina 25 |
| 28 | Por qué puede costar detectar la activación | 0 | saltar | |
| 29 | Qué responde la tesis | 60 | mostrar | Apoyo parcial, y viene de activación |
| 30 | Conclusiones 1 | 0 | saltar | Cubierta por la lámina 29 |
| 31 | Conclusiones 2 | 0 | saltar | Cubierta por la lámina 29 |
| 32 | Qué falta para cerrar la tesis | 20 | pasar rápido | Faltan decisiones, no experimentos |
| 33 | Necesito decidir cinco cosas con usted | 70 | mostrar | ¿Escribo o planifico una cohorte nueva? |
| | **Total** | **600** | | |

Subtotales: láminas 1 a 11, 145 s; 14 y 17, 50 s; 18 y 21 a 23, 155 s; 24 a 26, 100 s; 29 a 33, 150 s.

- **Se saltan:** 2, 4, 7, 8, 9, 10, 12, 13, 15, 16, 19, 20, 27, 28, 30 y 31.
- **Se pasan rápido:** 24 y 32.
- **Anexos:** igual que en la versión larga, solo a pedido.
- Entre la lámina 18 y la 21 hay que pasar por la 19 y la 20 sin detenerse; la frase de puente es: "Falta saber de dónde viene esa mejora".
- En la versión corta, la frase de la lámina 14 es: "Tres personas con datos anómalos me hicieron revisar la etiqueta de activación; encontré que el generador mezclaba las ventanas y que la etiqueta antigua coincidía con la corregida solo en la mitad de los casos".
- En la versión corta, la lámina 33 se acorta leyendo solo el enunciado de cada pregunta y deteniéndose en la primera; el sexto punto (normalización) se deja para las preguntas.

---

## 2. Guion hablado, versión de 20 minutos

**Lámina 1 · Portada (25 s).** Profesor, le cuento qué pasó desde la última reunión. Corregí un error en la etiqueta de activación y repetí todo con 41 personas. El historial ayuda a predecir activación, con un efecto pequeño y de pocos segundos. En atención la mejora existe, pero no es temporal, y lo que detecta el EEG es sobre todo la huella de los ojos. Al final hay cinco decisiones que necesito tomar con usted.

**Lámina 2 · De qué voy a hablar (10 s).** Son nueve partes. Voy rápido por las primeras, porque lo nuevo son las tres últimas: qué explica la mejora, qué detecta el EEG y las conclusiones.

**Lámina 3 · La hipótesis (40 s).** Esta es la hipótesis tal como está en el manuscrito: que los modelos temporales multimodales rinden mejor fuera de muestra que los estáticos comparables. Para probarla comparo siempre el mismo modelo, con la misma etiqueta, y lo único que cambia es si ve las ventanas anteriores, hasta 32. La hipótesis dice emociones, pero con GSR lo que mido es activación; esa es una de las preguntas del final.

**Lámina 4 · Los datos (35 s).** Los datos son de la Toma de Muestra 2 del Fondecyt, en laboratorio, de agosto de 2025. El Tobii registra mirada, pupila y GSR en un mismo archivo; el EEG viene aparte, de un OpenBCI de 16 canales a 125 Hz. Los sincronicé por persona y hora, y corté todo en ventanas de 2 segundos que avanzan de a 1. Este set no tiene expresión facial, y la ubicación de los electrodos no está documentada.

**Lámina 5 · Unas señales arman la etiqueta y otras la predicen (50 s).** No tengo una etiqueta directa de atención ni de activación, así que la construyo. El Modelo Profesor arma la etiqueta con unas señales y el Modelo Estudiante la predice con otras distintas. En atención, el Attention Score sale de la mirada y la pupila, y lo predigo con EEG y GSR. En activación, el Arousal Score sale de la GSR, y lo predigo con EEG, mirada y pupila. "Alta" significa sobre la mediana de esa persona en su sesión completa, así que esto no sirve tal cual en línea.

**Lámina 6 · 48 personas, 41 en el análisis (35 s).** Se registraron 48 personas y quedan 41 en el análisis: 25 de entrenamiento, 8 de validación y 8 de test. Salen cuatro por EEG no utilizable y dos sin GSR, y a P29 la dejo aparte, para un análisis de sensibilidad, por un desfase de sincronización. Como las ventanas se solapan, la unidad es la persona: calculo la AUC por persona y después promedio. Validación y test ya los había mirado antes, así que todo lo que muestro es exploratorio.

**Lámina 7 · Qué señales combinan los trabajos recientes (25 s).** La tendencia es fusionar varias señales con modelos tipo Transformer. Lo más cercano en contexto web es la tesis de Saavedra, del mismo grupo, con EEG y GSR, que no encontró mejora clara con fusión tardía. Ninguno de los que revisé combina estas cuatro señales navegando la web, pero esa búsqueda la tengo que repetir antes de afirmarlo en la defensa.

**Lámina 8 · Lo que falta y lo que intento aportar (25 s).** De la revisión salen tres brechas, y cada una tiene su respuesta en el diseño. La principal: comparo el mismo modelo con y sin historial sobre las mismas ventanas. La comparación entre fusión temprana, intermedia y tardía la muestro en resultados.

**Lámina 9 · KDD (15 s).** Uso KDD como marco, en cinco etapas. Es iterativo: cuando encontré el error en la etiqueta volví de la evaluación a la transformación.

**Lámina 10 · Qué hago con cada señal (25 s).** El EEG fue lo que más trabajo dio: lo filtro entre 1 y 45 Hz, con notch en 50; marco los canales saturados, planos o con huecos y no los uso; y desde octubre lo trabajo por canal, con 342 variables por ventana. La GSR la separo en parte tónica y fásica. La pupila todavía no la corrijo por el brillo de cada página; eso va en las limitaciones.

**Lámina 11 · Cómo comparo (45 s).** Elijo la configuración solo con las 25 personas de entrenamiento y la congelo. Después la evalúo con las 41 personas en validación cruzada por persona, igual para el modelo con y sin historial. Lo que miro es la diferencia pareada dentro de cada persona, con intervalo bootstrap remuestreando personas y no ventanas. El placebo lo registré antes de correrlo; el análisis de posición también lo registré, pero después de ver el placebo, así que es post hoc. Aquí muestro solo la AUC, aunque el borrador pide también otras métricas.

**Lámina 12 · Etiqueta de atención con PCA (20 s).** Probé dos formas de armar la etiqueta de atención: pesos iguales y PCA. Con PCA los modelos la predicen mejor y seguí con esa. Ojo que las dos coinciden solo en dos tercios de las ventanas.

**Lámina 13 · Tres personas con datos anómalos (30 s).** Esto fue lo que me hizo dudar de activación. P4 casi no tenía señal de GSR y aun así todas sus ventanas tenían etiqueta. P34 y P46 tenían muchos puntajes repetidos, y P34 quedaba con 8,6 % de clase alta. Ahí dejé de ajustar modelos y revisé la etiqueta.

**Lámina 14 · El generador mezclaba las ventanas (35 s).** El problema estaba en el código que generaba la etiqueta: al agrupar por persona, cada valor de GSR perdía su ventana. El 98 % de los valores del archivo quedó en una ventana que no era la suya. Repitiendo el cálculo con el error reproduzco los puntajes que tenía guardados, así que las AUC de activación anteriores no sirven.

**Lámina 15 · Ejemplo en P22 (20 s).** Así se ve la etiqueta corregida en un tramo real de P22. La línea es el puntaje de GSR de seis segundos y la punteada es su mediana en toda la sesión; los puntos azules, sobre la mediana, son "alta". La etiqueta dice si P22 está más activada que de costumbre en ese momento.

**Lámina 16 · Antigua y nueva coinciden en la mitad (20 s).** Comparé la etiqueta antigua con la nueva en las mismas ventanas, y cambia casi la mitad. Con clases balanceadas, eso es lo que esperaría si no tuvieran relación.

**Lámina 17 · La etiqueta nueva, V2 (30 s).** Rehíce la etiqueta en cuatro pasos y quedan 11.796 de 22.211 ventanas. Lo que más saca es exigir cinco ventanas válidas seguidas dentro del mismo estímulo. Por calidad se van 401, todas de P4. Las 41 personas conservan las dos clases.

**Lámina 18 · Primer análisis con 41 personas, 16-11 (55 s).** Para tener más potencia usé las 41 personas en validación cruzada, con la configuración congelada y sin búsqueda. En atención el historial mejora +0,026 y mejoran 36 de 41 personas; se repite con otras tres particiones. En activación da +0,034, pero en la partición que registré el intervalo toca el cero: inconcluso. Cuando lo repetí el 22 de noviembre con cinco particiones, activación quedó en +0,036, con el intervalo entre +0,010 y +0,065; esas son las cifras que uso en las conclusiones. Falta saber de dónde viene la mejora; antes, dos resultados rápidos.

**Lámina 19 · Fusión (25 s).** Con la misma familia de modelo, un MLP, en atención la fusión tardía le gana a la temprana por +0,012, y también a la intermedia. En activación no hay diferencias. La intermedia que probé es más profunda, así que ahí se mezcla tipo de fusión con capacidad. Y vale solo para esta familia: con HGB, en el cierre V3, la tardía no superó a la temprana.

**Lámina 20 · Sesión y tipo de página (20 s).** En atención el modelo rinde mejor hacia el final de la sesión, mejor en sitios web y peor en textos. En activación, la proporción de ventanas altas baja al final, compatible con habituación. Todo esto es descriptivo.

**Lámina 21 · ¿De dónde viene la mejora? (50 s).** Vuelvo a la mejora con historial. La comparé con dos controles. Uno es un placebo: la misma cantidad de ventanas, de la misma persona, pero de otras páginas. El otro es una sola variable: cuántos segundos lleva la persona en la página. En atención, el placebo y los segundos solos dan lo mismo que el historial real. En activación pasa lo contrario: el placebo y los segundos no aportan, y el historial sí, incluso sin los 6 segundos que usa la etiqueta. Hasta la lámina 18 parecía que la hipótesis se apoyaba en atención; esto lo da vuelta.

**Lámina 22 · La etiqueta depende de la posición en la página (45 s).** Al entrar a una página, la proporción de ventanas con atención alta cae a 37 % entre el segundo 2 y 3 y después sube hasta 62 %. El modelo con historial aprendía eso a través del largo del historial, no del contenido. Lo más probable es que refleje cómo se arma el Attention Score con fijaciones y pupila al cambiar de página. Este análisis lo hice después de ver el placebo, así que es explicativo y no confirmatorio.

**Lámina 23 · En activación, los segundos previos sí aportan (55 s).** Aquí saqué del historial los 6 segundos que definen la etiqueta, para que no se solapen. Aun así le gana al placebo por +0,046, en 28 de 41 personas, con p de Holm 0,004. Frente a un modelo que conoce los segundos en la página, el historial sumaba +0,038 en el primer análisis; al repetirlo el 22 de noviembre con cinco particiones da +0,032, con intervalo entre +0,004 y +0,059, y queda inconcluso tras la corrección de Holm. Y el modelo sigue siendo débil: la AUC está alrededor de 0,57.

**Lámina 24 · Los ojos se ven en el EEG (45 s).** La etiqueta de atención se arma con la mirada y la predigo con EEG, así que revisé cuánto de los ojos se cuela en el EEG. El parpadeo llega a unos 150 microvoltios en los dos canales de la frente y baja a unos 20 atrás. Ese patrón, además, es compatible con el montaje por defecto del equipo, que no estaba documentado. Y encontré que el EEG va entre 0,18 y 0,53 segundos atrasado respecto del seguidor ocular; eso no lo corregí.

**Lámina 25 · Al quitar los componentes oculares, la detección cae (60 s).** Este es el resultado más importante de la semana. Por persona separé el EEG en componentes independientes y quité los tres más ligados a la mirada y a los parpadeos, que son el 3,5 % de la varianza. La AUC de atención baja de 0,681 a 0,621, en 39 de 41 personas. Como control quité tres componentes no oculares, con veinte veces más varianza, y casi no cambia. Alfa y beta, que parecía lo más limpio, también cae, de 0,593 a 0,547. La limpieza es parcial, así que leo ese 0,06 como una cota inferior. Lo registré antes de correrlo y está auditado.

**Lámina 26 · Red sobre la señal cruda (45 s).** Probé un modelo más complejo: una red convolucional tipo EEGNet que aprende directo de la señal cruda. En atención le gana al modelo de referencia, 0,716 contra 0,681, o sea +0,035. Pero al quitar los componentes oculares cae a 0,649, y su predicción sigue el recorrido de la mirada más que la del modelo de referencia: su ventaja también depende de la huella ocular. En activación queda en el azar. Es una sola arquitectura, sin búsqueda, y no entrené una red con el filtro de control.

> Ojo: la nota de la lámina dice que la red "pasa el margen de 0,02 por poco". Si lo dices, que sea "el margen de 0,02 que propongo": el margen es la segunda decisión de la lámina 33 y no está aprobado.

**Lámina 27 · Por qué: el ojo (35 s).** La explicación es fisiológica. El ojo es un dipolo, con la córnea positiva y la retina negativa, y cada movimiento cambia el potencial en los electrodos. Como la etiqueta se define con los ojos, todo lo que los ojos dejan en el EEG la predice. Cumplí la regla de no usar las mismas señales, pero eso no asegura independencia fisiológica. Lo que detecto es sobre todo lo Observado, no lo Atendido. Las referencias están verificadas en catálogo; me falta confirmarlas en el texto completo.

**Lámina 28 · Por qué puede costar detectar la activación (35 s).** La etiqueta de activación viene de la GSR, que mide glándulas sudoríparas bajo control simpático. Esa vía depende de estructuras profundas y es lenta: la respuesta tarda de 1 a 3 segundos en aparecer y varios en recuperarse. Una ventana de EEG de 2 segundos no calza con eso, y con 16 canales la AUC queda en 0,52. Es coherente con el resultado temporal: lo que ayuda en activación es el historial de los segundos previos. Es una interpretación mía, con referencias por confirmar en el texto completo.

**Lámina 29 · Qué responde la tesis (60 s).** Esta tabla es el resumen. Con historial las dos tareas mejoran: +0,029 en atención y +0,036 en activación. En atención no es información temporal: si el modelo conoce la posición en la página, el historial agrega +0,001. En activación lo es en parte: +0,047 sobre el placebo a 6 segundos; a 12 segundos queda inconcluso. El modelo con orden, la GRU, no agrega en atención, y la fusión tardía solo gana en atención y con MLP. Y la última fila es lo nuevo: en atención, el EEG detecta sobre todo los ojos. Todo esto con personas que ya había consultado, así que confirmarlo requiere personas nuevas.

**Lámina 30 · Conclusiones: apoyo parcial (40 s).** Son las conclusiones del borrador del capítulo 9. La hipótesis tiene apoyo parcial, y viene solo de activación. Ese efecto se sostiene frente al placebo, pero es pequeño, de corto alcance —desaparece desde los 24 segundos— y con AUC de 0,52 a 0,59. Cuando además controlo la posición, conserva su tamaño, +0,032, pero queda inconcluso. En atención, lo que parecía temporal era la posición dentro de la página. Y el orden de las ventanas no aportó de forma demostrable: la GRU rinde 0,040 menos en atención.

**Lámina 31 · Conclusiones: qué detecta el EEG (40 s).** La conclusión metodológica más importante es la tercera: separar las señales no asegura independencia fisiológica. La etiqueta se define con lo Observado y el EEG registra esa misma conducta, así que no puedo afirmar que detecte lo Atendido. El aporte queda doble: evidencia acotada de que el historial de los segundos previos ayuda a predecir la activación, y una advertencia sobre evaluar modelos de EEG con etiquetas oculares. Estas conclusiones suponen, de forma provisoria, las decisiones que le consulto en la última lámina.

**Lámina 32 · Qué falta para cerrar la tesis (30 s).** Mi propuesta es cerrar la experimentación aquí: no espero que más corridas sobre estas 41 personas cambien las conclusiones. Lo que falta son decisiones y escritura: integrar los resultados del 22 y 23 de noviembre al borrador y ajustar las conclusiones según lo que decidamos. Sobre la etiqueta: el 22 de noviembre probé una etiqueta de atención corregida por la posición en la página, y hay que decidir si reemplaza a la original. De los experimentos opcionales, el único que cambiaría el estatus de los resultados es una cohorte nueva.

**Lámina 33 · Cinco decisiones (75 s).** Necesito decidir cinco cosas con usted. Primero, si escribo con estos resultados o planifico una cohorte para confirmar activación; es la que más me urge, porque define si escribo o recluto. Segundo, qué cuenta como "mejor": cualquier mejora sobre cero, como dice la hipótesis, o un mínimo como +0,02 de AUC. Tercero, si escribo "activación (GSR)" en vez de "emociones". Cuarto, si uso la etiqueta de atención original o la corregida por posición: la corregida ya no se predice con la posición, 0,504, y la detección casi no cambia, 0,675 frente a 0,683. Y quinto, si encuadro la tesis como apoyo parcial más una advertencia metodológica, con la atención por EEG presentada como huella ocular. Hay un sexto punto, menor: las etiquetas se normalizan con la sesión completa de cada persona y el manuscrito pide normalizar solo con entrenamiento; necesito saber si basta con declararlo como límite. El detalle de cada opción está en la minuta.

---

## 3. Preguntas difíciles y respuestas

Las rutas son relativas a `repos/Tesis_MDS/` salvo que se indique otra cosa.

**1. ¿La detección de atención por EEG no es circular, si la etiqueta sale de los ojos?**
En el sentido fisiológico, sí en buena parte. Cumplo la regla de no usar la misma señal para etiquetar y para predecir, pero el EEG registra la huella eléctrica de los ojos. Al quitar tres componentes oculares, que son el 3,5 % de la varianza, la AUC baja de 0,681 a 0,621 [diferencia 0,060; IC 0,045 a 0,075], y un control que quita el 72 % de la varianza la deja en 0,674. Lo que queda sobre el azar no lo puedo atribuir al cerebro: conserva el patrón de un artefacto ocular residual. Por eso digo que detecto lo Observado y no lo Atendido.
Fuente: `resultados/limpieza_ocular_41p_23-11-2026/INFORME.md`.

**2. ¿Por qué el AUC de activación es tan bajo? ¿Sirve para algo?**
Con la ventana actual el modelo está en el azar: 0,518 con EEG, mirada y pupila, y 0,524 con solo EEG. Con historial sube a 0,554, y lo más alto que obtuve es 0,587. Para uso práctico no sirve, y así lo escribo en las limitaciones. Lo que tiene interés es el contraste pareado: el historial reciente mejora y un placebo no. Las razones probables son que la GSR es lenta y de origen profundo, y que la etiqueta es relativa a la mediana de cada persona en un rango de activación estrecho; eso es compatible con los datos, pero no lo puse a prueba.
Fuentes: `resultados/reapertura_41p_22-11-2026/INFORME.md`; `resultados/red_cruda_41p_23-11-2026/INFORME.md`; `resultados/enfoques_41p_22-11-2026/INFORME.md`.

**3. ¿Por qué dice que la mejora de atención no es temporal?**
Por tres resultados que apuntan a lo mismo (láminas 21 y 22). Un historial placebo, con ventanas de la misma persona en otras páginas, da la misma mejora: la diferencia es −0,000 [−0,003; +0,003]. Los segundos en la página, como única variable, reproducen la mejora: +0,028 [+0,021; +0,035]. Y si el modelo conoce la posición, el historial agrega +0,001 [−0,002; +0,005]. El límite: el análisis de posición del 18-11 es post hoc, y como los segmentos son cortos el nulo vale en la práctica para historiales de 2 a 10 ventanas, no para historiales largos.
Fuentes: `resultados/cierre_robustez_41p_16-11-2026/INFORME.md`; `resultados/explicativo_posicion_41p_18-11-2026/INFORME.md`; `resultados/reapertura_fase3_41p_22-11-2026/INFORME.md`.

**4. Reabrió el análisis y corrió muchas pruebas. ¿Cómo sé que no hubo p-hacking?**
No lo puedo descartar del todo, y por eso no presento nada como confirmatorio. Lo que hice para acotarlo: cada etapa se registró en Git antes de correr, se ejecutó una vez, usa Holm dentro de su familia y tuvo auditoría independiente; de 289 archivos con hash, 288 coinciden y la diferencia está documentada. Pero son doce etapas sobre las mismas 41 personas, y reabrí el 22-11 después de ver un resultado inconcluso en activación (+0,034 [−0,001; +0,069]), que con cinco particiones pasó a +0,036 [+0,010; +0,065]. Holm corrige dentro de cada etapa y no entre etapas, los contrastes secundarios no llevan corrección, y tres decisiones quedaron pegadas al umbral (p de Holm 0,055, 0,055 y 0,049). La única salida limpia es una cohorte nueva con el contraste fijado de antemano.
Fuentes: `documentacion/Cierre_Experimental_Final_23-11-2026.md`; `resultados/reapertura_41p_22-11-2026/INFORME.md`; `resultados/enfoques_41p_22-11-2026/INFORME.md`.

**5. ¿Por qué 41 personas? ¿Las de test ya se habían visto?**
Hay 48 registradas; salen 4 por EEG no utilizable, 2 sin GSR y P29 queda para sensibilidad. El 41 no viene de un cálculo de potencia: es lo que había disponible. Y sí, las 16 de validación y test ya se habían consultado; la configuración se eligió solo con las 25 de entrenamiento, pero eso no las vuelve nuevas. Además, en el análisis del 16-11 el efecto de activación aparecía en las 25 de entrenamiento (+0,055) y no en las otras 16 (+0,001 [−0,052; +0,055]). Por eso todo va como exploratorio.
Fuentes: `resultados/modelado/particion_participantes.csv`; `resultados/cierre_final_41p_16-11-2026/INFORME.md`.

**6. ¿De dónde sale el margen de 0,02?**
Es una propuesta mía, sin justificación sustantiva independiente todavía; así quedó escrito en el protocolo del 06-11. No está aprobado ni se deduce de los resultados, y la hipótesis del manuscrito dice "mejor", o sea mayor que cero. Importa porque varias lecturas dependen de él: en atención el límite inferior fue 0,018 el 16-11 y 0,021 el 22-11, justo a cada lado del margen, y la ventaja de la red lo supera con un límite inferior de 0,023. Es la segunda de las cinco decisiones de la lámina 33; sin margen, las reglas vuelven a ser contra cero.
Fuente: `resultados/protocolo_hipotesis_reintento_06-11-2026/INFORME.md`.

**7. ¿Por qué usar GSR como etiqueta? ¿Y la latencia de la respuesta?**
Porque en este set no hay expresión facial ni autorreporte, y la GSR es la medida de activación simpática disponible. El Arousal Score combina cuatro componentes e integra seis segundos, exigiendo cinco ventanas válidas seguidas del mismo estímulo. La respuesta de conductancia empieza de 1 a 3 segundos después del evento, así que la etiqueta de un instante refleja algo que pasó antes; ese desfase no lo modelé. Tampoco verifiqué si los filtros de la GSR tienen un soporte más largo que los seis segundos, lo que importa para el contraste sin solapamiento. Y el dato de latencia viene de una referencia verificada en catálogo, no leída en texto completo.
Fuentes: `resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md`; límites de `resultados/reapertura_41p_22-11-2026/INFORME.md`; `Escritura/Borrador Discusión fisiológica 23-11-2026.md` (vault).

**8. ¿Por qué "activación" y no "emociones", si la hipótesis dice emociones?**
Porque la GSR mide activación simpática y no distingue valencia: no puedo separar una emoción agradable de una desagradable. Sin facial ni autorreporte, hablar de emociones en general sería afirmar más de lo que mido. Esto cambia la redacción de la hipótesis, y no lo doy por decidido: no consta su confirmación y es la tercera pregunta de la lámina 33. Si prefiere mantener "emociones", habría que declarar que la tesis cubre solo su dimensión de activación.
Fuentes: `CLAUDE.md` del vault (`documentos/01 Tesis MDS/`); `documentacion/Cierre_Experimental_Final_23-11-2026.md`.

**9. ¿Por qué la GRU rinde peor que un resumen estadístico?**
En atención la GRU con historial queda 0,040 bajo el HGB [−0,055; −0,027] y no mejora sobre su propia versión de una ventana: +0,008 [−0,004; +0,020]. No sé con certeza por qué. La GRU es una configuración fija sin búsqueda de hiperparámetros, y los segmentos son cortos: el historial de 32 se completa en menos del 2 % de las ventanas. Así que no puedo concluir que los modelos secuenciales no sirvan; solo que esta GRU, con estos datos, no aprovechó el orden. En activación la GRU sí mostró una señal (+0,051 [+0,021; +0,080]), pero es secundaria y sin corrección.
Fuentes: `resultados/cierre_final_41p_16-11-2026/INFORME.md`; `resultados/cierre_v3_16-11-2026/INFORME.md`.

**10. ¿Qué pasa con el desfase de reloj entre el EEG y el seguidor ocular?**
El EEG va entre 0,18 y 0,53 segundos atrasado, con mediana 0,45, en las 41 personas. Eso corre las ventanas de EEG entre un 12 % y un 25 % respecto de las de mirada, pupila y GSR. No lo corregí, porque las ventanas estaban congeladas y corregirlo obliga a recalcular todo. El efecto esperado es atenuar la relación entre el EEG y las etiquetas, pero no lo medí; y en algunas personas el acoplamiento es bajo y el desfase estimado es poco seguro. Corregirlo es uno de los experimentos opcionales.
Fuente: `resultados/montaje_ocular_41p_23-11-2026/INFORME.md`.

**11. ¿Por qué dice que la limpieza ocular es una cota inferior?**
Porque la limpieza fue parcial. La correlación máxima entre algún canal y los parpadeos baja de 0,28 a 0,08, sin anularse, y la predicción del modelo limpio sigue asociada al recorrido de la mirada (Spearman 0,28, antes 0,41). Lo que queda conserva el patrón de un artefacto: frontales sobre posteriores y potencia lenta sobre alfa y beta. Pero la objeción contraria también vale: con 11 a 16 canales, tres componentes son entre el 19 % y el 27 % de las dimensiones y arrastran actividad frontal no ocular. El control acota esa objeción y no la elimina, así que "cota inferior" es mi lectura más defendible, no una demostración.
Fuente: `resultados/limpieza_ocular_41p_23-11-2026/INFORME.md`.

**12. ¿Una red más grande o mejor ajustada cambiaría el resultado?**
No lo sé, y no puedo descartarlo. Probé una sola arquitectura, de 1.217 parámetros, sin búsqueda ni curva de convergencia. En atención le ganó al modelo de referencia por +0,035 [+0,023; +0,047], pero al limpiar el EEG cayó de 0,716 a 0,649, y su predicción sigue la mirada más que la del modelo de referencia (0,48 frente a 0,41). Mi expectativa es que una red más grande subiría la AUC de atención aprovechando mejor la huella ocular, porque la etiqueta es ocular; eso es una conjetura. En activación el 0,498 vale para esta red y no permite decir que el EEG crudo no tenga información. Tampoco entrené la red con el filtro de control.
Fuente: `resultados/red_cruda_41p_23-11-2026/INFORME.md`.

**13. Entonces, ¿qué aporta la tesis?**
Dos cosas, y ninguna es un detector utilizable. Una es evidencia acotada de que el historial reciente, de 6 a 12 segundos, ayuda a predecir la activación: +0,047 [+0,018; +0,078] frente a un placebo. La otra es metodológica: muestro que una mejora que parecía temporal era la posición en la página, y que una detección que parecía cerebral era en buena parte ocular. A eso se suma haber encontrado y corregido el error de alineación en la etiqueta de GSR. El aporte más sólido es el metodológico; si ese encuadre es suficiente para la tesis es justamente lo que necesito conversar.
Fuentes: `Escritura/Borrador Conclusiones 23-11-2026.md` (vault), sección 9.7; `resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md`.

**14. Si tuviera una cohorte nueva, ¿qué haría?**
Una sola cosa, definida antes de reclutar: evaluar los modelos ya congelados, sin reentrenar, con un contraste y un tamaño de muestra registrados y una única evaluación. Confirmaría el efecto de activación, que es el único que sostiene la hipótesis. El problema es el tamaño: según qué variabilidad use, salen 72, 101 o 767 personas evaluables, y las dos primeras cifras se estiman con solo 8 personas. Además, ese protocolo es del 06-11 y contrasta el historial contra el modelo sin historial; habría que reescribirlo para el contraste contra placebo antes de usarlo. Si se hace, aprovecharía de corregir el desfase de relojes y registrar electrooculograma.
Fuentes: `resultados/protocolo_hipotesis_reintento_06-11-2026/INFORME.md`; `Escritura/Borrador Conclusiones 23-11-2026.md` (vault), sección 9.6.

**15. ¿Qué validez tienen las pseudoetiquetas, si no hay una medida externa?**
Validez externa no tienen: no las comparé con autorreporte, desempeño en una tarea ni ninguna otra medida. Son offline y relativas a la mediana de cada persona, así que las clases salen balanceadas por construcción y eso no demuestra nada psicológico. En atención, el Attention Score está dominado por fijaciones, dispersión y recorrido, y la pupila casi no pesa: mide quietud de la mirada. Y la etiqueta cambia según cómo se arme: las versiones de pesos iguales y PCA coinciden en el 66 % de las ventanas. Todo lo que afirmo es sobre predecir estas etiquetas, no sobre atención o activación reales.
Fuentes: `resultados/enfoques_41p_22-11-2026/INFORME.md` (E2); `resultados/profesor_binario_reconstruido_29-10-2026/INFORME.md`; `resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md`.

**16. Si al controlar la posición el efecto de activación queda inconcluso, ¿por qué habla de apoyo parcial?**
Es una objeción justa, y el encuadre es una decisión abierta (la quinta de la lámina 33). Con la posición como variable en los dos modelos, el historial suma +0,032 [+0,004; +0,059], pero no pasa Holm sobre las cuatro pruebas (p 0,108). Dentro de un mismo estímulo suma +0,009 y lo que ayuda es el tiempo transcurrido. Con el tiempo de sesión en ambos modelos queda en +0,026 [−0,006; +0,056]. El apoyo descansa en el contraste contra placebo a 6 segundos; lo que el historial aporta es un mejor resumen del estado de los últimos segundos, no evidencia de dinámica dentro del estímulo.
Fuentes: `resultados/reapertura_fase3_41p_22-11-2026/INFORME.md`; `resultados/reapertura_41p_22-11-2026/INFORME.md`.

**17. ¿El efecto de activación depende de unas pocas personas?**
En parte es desigual. En el contraste principal mejoran 23 de 41, la media es +0,036 y la mediana +0,014; una persona, P4, aporta 0,009 de esos 0,036. Sin la persona más influyente queda en +0,028 [+0,006; +0,050], así que no depende de una sola. El contraste contra placebo a 6 segundos es más parejo: mejoran 30 de 40 y la mediana es +0,042. Esa sensibilidad la pidió la auditoría y no estaba registrada.
Fuente: `resultados/reapertura_41p_22-11-2026/INFORME.md`.

**18. La fusión tardía, ¿es mejor o no? El cierre V3 decía otra cosa.**
Depende de la familia de modelo, y eso debilita la conclusión. Con HGB, en el cierre V3, la tardía no superó a la temprana y en atención fue levemente peor (−0,010 en entrenamiento). Con MLP y las 41 personas (lámina 19), la tardía gana en atención por +0,012 [+0,005; +0,021]. Es un contraste secundario, sin corrección por multiplicidad, y la fusión intermedia que probé es más profunda. Lo que sí sostengo es lo más modesto: la fusión no es lo que explica el desempeño.
Fuentes: `resultados/ampliacion_41p_16-11-2026/INFORME.md` (E3); `resultados/cierre_v3_16-11-2026/INFORME.md`.

**19. Si normaliza con la sesión completa, ¿esto sirve en línea?**
No, tal como está. La mediana que define "alta" y varias variables por persona usan la sesión entera, incluido el futuro. El manuscrito pide normalizar solo con entrenamiento, así que hay una diferencia entre lo escrito y lo hecho que tengo que resolver con usted; ya no es una de las cinco preguntas de la lámina 33, sino el sexto punto, menor, que digo de palabra en esa lámina. La adaptación a la persona que mejoró activación (+0,045 [+0,023; +0,069]) tampoco es desplegable, porque sus etiquetas de calibración usan esa misma normalización. Evaluar etiquetas calculadas solo con información previa queda como trabajo futuro.
Fuentes: `resultados/protocolo_hipotesis_reintento_06-11-2026/INFORME.md`; `resultados/enfoques_41p_22-11-2026/INFORME.md` (E4).

**20. La pupila responde al brillo de la pantalla. ¿Eso no contamina todo?**
No está corregido y es una limitación declarada. En la etiqueta de atención el daño parece acotado, porque la pupila casi no pesa en el Attention Score; pero eso también significa que la etiqueta casi no usa la pupila. En activación la pupila es una entrada y aporta poco: al permutarla la AUC cae 0,021, frente a 0,053 del EEG. No sé cuánto de ese poco es brillo y cuánto es activación. Para separarlo habría que medir la luminancia de cada página.
Fuentes: `resultados/enfoques_41p_22-11-2026/INFORME.md` (E2); `resultados/ampliacion_41p_16-11-2026/INFORME.md` (E5).

---

## 4. Tres frases de cierre, si queda un minuto

1. La hipótesis tiene apoyo parcial y viene de activación: el historial de los últimos segundos ayuda un poco, con modelos que siguen siendo débiles.
2. En atención aprendí dos cosas que no esperaba: lo que parecía temporal era la posición en la página, y lo que parecía cerebral eran en buena parte los ojos; detecto lo Observado, no lo Atendido.
3. Nada de esto está confirmado en personas nuevas, así que lo que necesito de usted hoy es saber si escribo con estos resultados o planifico una cohorte.

---

## Láminas donde la nota, el contenido o los informes no calzan

Revisado el 23-11-2026 contra `relato.py` y `GUIÓN.md` ya corregidos. Quedaron resueltas y se sacaron de esta tabla: el filtro del EEG (lámina 10, ahora 1–45 Hz), las notas y títulos de las láminas 1, 2 y 18 sobre activación, la fusión "pendiente" de la lámina 8, el "Sí" de la lámina 29 (ahora "En parte"), las decisiones distintas entre las láminas 32 y 33 (ahora las mismas cinco), el "Registré" de la lámina 6 y el comentario de versión de `relato.py`. Lo que sigue son detalles menores que siguen vigentes; ninguno se corrigió aquí, porque este ensayo no toca `relato.py`.

| Lámina | Qué no calza | Dónde está el dato correcto |
|---|---|---|
| 23, 29 y 30 | La lámina 23 da +0,046 para el historial frente al placebo (16-11; 28 de 41; p Holm 0,004) y las láminas 29 y 30 dan +0,047 (22-11; p Holm 0,017). Son dos análisis distintos, no un error. El pie de la lámina 29 avisa que usa la repetición del 22-11; la lámina 23 no dice que su cifra es la del 16-11. | `resultados/ampliacion_41p_16-11-2026/INFORME.md`; `resultados/reapertura_41p_22-11-2026/INFORME.md` |
| 23 | La nota dice que frente al modelo que conoce los segundos en la página "el historial sumaba +0,038 el 16-11". Ese +0,038 [+0,002; +0,074] es del análisis post hoc del 18-11 (la propia lámina lo cita como fuente). Además, el +0,032 del 22-11 no es la misma prueba repetida: usa cinco particiones y la posición en los dos modelos. En el guion hablado se dice "en el primer análisis", sin fecha. | `resultados/explicativo_posicion_41p_18-11-2026/INFORME.md`; `resultados/reapertura_fase3_41p_22-11-2026/INFORME.md` |
| 29 y 30 (y 28) | La tabla de la lámina 29 dice "a 12 s, inconcluso" y la lámina 30 dice que la información "está en los 6 a 12 s anteriores"; la lámina 28 habla de "los 6 s previos". Las dos frases salen del mismo informe: a 6 s hay respaldo (+0,047 [+0,018; +0,078]), a 12 s el contraste es inconcluso (+0,024 [−0,011; +0,060]) y desde 24 s no se distingue del placebo. Si preguntan, decir exactamente eso. | `resultados/reapertura_41p_22-11-2026/INFORME.md` |
| 26 | La nota dice que la red "pasa el margen de 0,02 por poco". El margen de 0,02 es una propuesta de Mario y es la segunda decisión de la lámina 33; no está aprobado. Decir "el margen que propongo" o no mencionarlo. | `resultados/protocolo_hipotesis_reintento_06-11-2026/INFORME.md`; `resultados/red_cruda_41p_23-11-2026/INFORME.md` |
| 2 y 28 | Menor: el punto 8 del índice dice "por qué activación no sale"; el título de la lámina 28 ahora es más prudente ("Por qué puede costar detectar la activación desde el EEG"). | `relato.py`, lámina 28 |
| 33 | Menor: la nota remite a la minuta para el detalle de cada opción. La minuta trae siete puntos; el séptimo (si el profesor PCA queda como definición del Attention Score) no está en la lámina ni en la nota. | `documentos/01 Tesis MDS/Avances/Avance - 23-11-2026 (Minuta de decisiones con el profesor).md` |
