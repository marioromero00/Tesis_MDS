# Segunda lectura como miembro de comisión — ronda 6 (27-11-2026)

Lector: estadístico, con experiencia en aprendizaje automático sobre señales fisiológicas. No participó en las rondas anteriores. No se editó ningún archivo existente, no se entrenó nada y no se hicieron commits. Este informe es el único archivo creado.

## Qué se leyó y qué no

Completos y en este orden: `Estructura Tesis.md` (ET), `Borrador Secciones pendientes 23-11-2026.md` (SP), `Borrador Resultados y Discusión 23-11-2026.md` (RD), `Borrador Conclusiones 23-11-2026.md` (CO), `GUIÓN.md`, `relato.py` (RE) y `ENSAYO.md` (EN).

Consultados para entender qué se hizo: `scripts/cierre_final_41p.py`, `cierre_robustez_41p.py` y la primera mitad de `cierre_experimental_v3.py`; los `protocolo.json` de `cierre_final_41p`, `cierre_robustez_41p`, `reapertura_41p` y `reapertura_fase3_41p`; los `INFORME.md` de `reapertura_41p`, `enfoques_41p`, `ampliacion_41p` y `cierre_v3`; `x2_estratificada.csv` y `descriptivos.csv` de las fases 2 y 3; `Problema e hipótesis.md`; el orden de commits del 16 al 18-11.

No se revisó: los gráficos de las láminas, los artículos citados, los scripts de limpieza ocular, red convolucional y enfoques, ni los informes anteriores al 16-11.

El informe del primer lector (`ronda3/LECTURA_CRITICA_COMITE.md`) se leyó al final, con la lista de objeciones ya cerrada; solo se usó para la última columna de la tabla de la sección H.

Una comprobación propia, hecha desde las predicciones guardadas y solo para graduar la gravedad de A1 y A2 (no es cifra para el texto): con un intervalo t en vez del percentil, el límite inferior del contraste principal de atención con cinco particiones queda en 0,0210 (percentil: 0,0212), y el de activación en 0,008 (percentil: 0,010). La correlación media entre particiones de la diferencia por persona es 0,82 en atención y 0,61 en activación.

## Resumen

- **2 bloqueantes nuevas**, **9 importantes nuevas**, **8 menores nuevas**; **6 ya planteadas por el primer lector que quedaron mal o no resueltas**.
- Las cifras no están en cuestión. Lo que una comisión objetaría hoy es, sobre todo, qué demuestra el único contraste que sostiene el "apoyo parcial".
- El texto tiene además el problema contrario: tres resultados firmes están enterrados bajo cautelas (sección C).

---

## A. Estadística e inferencia

### A1 (menor, nueva). El tipo de intervalo no se declara y hay rótulos que dependen de él

- **Dónde.** SP 4.8.3, "Incertidumbre"; RD 6.4, primer párrafo.
- **Qué pasa.** `ci()` en `cierre_final_41p.py` es un bootstrap percentil de la media de 41 diferencias. Con 41 personas el percentil es algo estrecho. El protocolo del cierre V3 lo advierte para 8 personas; los borradores no lo dicen para 41. Tres rótulos viven a milésimas del umbral (atención 0,021; red 0,023; historial desplazado 0,018).
- **Texto actual (SP 4.8.3):** "Los intervalos de confianza de 95 % y de 90 % se obtienen por *bootstrap* de personas (20.000 réplicas)."
- **Texto propuesto:** "Los intervalos de confianza de 95 % y de 90 % se obtienen por *bootstrap* percentil de personas (20.000 réplicas, con la misma semilla en todos los contrastes). Con 41 personas el intervalo percentil puede quedar algo estrecho; por eso los rótulos cuyo límite está a milésimas de un umbral se señalan como tales y no se interpretan como distintos de sus vecinos."
- Mismo agregado ("percentil") en RD 6.4.

### A2 (importante, nueva). Las AUC por persona de una validación cruzada no son independientes, y el bootstrap las trata como si lo fueran

- **Dónde.** SP 4.8.3, "Unidad de inferencia"; RD 6.4; RD 7.1, párrafo bajo la tabla.
- **Qué pasa.** Cada persona se predice con un modelo ajustado con las otras 36, y las personas de un mismo grupo de la validación cruzada comparten modelo. El bootstrap de personas mide la variación entre personas evaluadas, condicionada a estos modelos; no mide cuánto cambiaría el resultado con otras personas de entrenamiento. En activación esa parte no es chica: la diferencia por persona cambia bastante de una partición a otra (por eso promediar cinco estrecha el intervalo). Promediar particiones no cambia la unidad de inferencia, que sigue siendo la persona, pero sí cambia lo que se estima (el desempeño medio sobre particiones de estas 41 personas) y reduce una fuente de varianza que el intervalo de una partición sí incluía. RD 7.1 dice "reduce el ruido debido a la partición"; no dice que el intervalo resultante sigue sin cubrir la variación por conjunto de entrenamiento.
- **Se arregla redactando.**
- **Texto actual (SP 4.8.3):** "Las ventanas, las semillas y los grupos de la validación cruzada no aumentan el tamaño de muestra."
- **Texto propuesto:** agregar a continuación: "Dos límites de esta inferencia deben declararse. Las AUC por persona no son independientes entre sí, porque cada persona se predice con un modelo ajustado con las demás y las personas de un mismo grupo de la validación cruzada comparten modelo; el *bootstrap* de personas no recoge esa dependencia ni la variación debida al conjunto de entrenamiento, de modo que los intervalos describen a estas 41 personas con estos modelos y pueden ser optimistas como estimación para personas nuevas. Y al promediar la AUC de cada persona sobre cinco particiones la unidad sigue siendo la persona, pero lo que se estima es el desempeño medio sobre particiones, con menos varianza que en una sola."

### A3 (menor, nueva). La familia de Holm no se dice en la tabla principal, y mezcla tareas

- **Dónde.** RD 7.1, tabla, columna "p (Holm)".
- **Qué pasa.** El 16-11 la familia son 2 pruebas (una por tarea); el 22-11 son 4 (P1 y P2 en las dos tareas). El lector no puede saberlo desde la tabla. Las familias son razonables; lo discutible es que atención, con p minúsculos, no "gasta" nada y activación se corrige en la práctica por 2.
- **Texto propuesto (RD 7.1, primera frase bajo la tabla):** anteponer "El p de Holm se calcula sobre las 2 pruebas del 16-11 (una por tarea) y sobre las 4 del 22-11 (este contraste y su control con el tiempo de sesión, en las dos tareas)."

### A4 (importante, nueva). El nulo de atención cumple la lógica de equivalencia con holgura, y el texto no lo dice

Va en la sección C (C4), porque es un resultado que el texto debilita sin necesidad. El "nulo concluyente" es un TOST al 5 % (intervalo de 90 % dentro del margen) y eso es correcto. Sus dos debilidades reales sí están declaradas (margen propuesto después de varias rondas; sin corrección por multiplicidad en las equivalencias). Lo que falta es decir que el nulo que importa no depende del margen.

### A5 (importante; ya planteada como menor 6 del primer lector, mal resuelta). "Efecto relevante" aplicado a contrastes contra 0,5

- **Dónde.** RD 7.7 (B1, B2, B5, B6), 7.9 (L3) y 7.11 (C1).
- **Qué pasa.** El margen de 0,02 se propuso para diferencias entre modelos. Aplicado a "AUC − 0,5" rotula como "efecto relevante" a la GSR sola (0,545), tres líneas antes de decir que la GSR no agrega nada. La tabla no se entiende sola y el rótulo dice más que el dato.
- **Texto actual (RD 7.7):** "La columna "A favor" cuenta las personas con diferencia positiva; en las pruebas contra 0,5 son las personas sobre el azar."
- **Texto propuesto:** agregar a continuación: "En las pruebas contra 0,5 el rótulo "efecto relevante" solo indica que el límite inferior de la AUC supera 0,52; no califica la utilidad de esa señal. La GSR sola queda en 0,545 y no agrega nada al EEG (B3)."

### A6 (menor, nueva). Personas que faltan en algunos contrastes, sin explicación en el texto

- **Dónde.** RD 7.3 ("6.268 filas de 40 personas"), RD 7.11 (adaptación, "29/40" y "30/40").
- **Qué pasa.** El protocolo de la reapertura explica el 40 de la curva (la persona con 26 filas etiquetadas no tiene ninguna con cobertura completa, contado antes de correr). El INFORME de enfoques dice "una persona de activación queda sin evaluación". RD no dice ninguna de las dos cosas. En la adaptación, además, se evalúa sobre el 60 % final de la sesión, donde el equilibrio de clases ya no está garantizado por la mediana y no hay mínimo por clase.
- **Texto propuesto (RD 7.3, tras "6.268 filas de 40 personas, el 53 % de las de activación"):** "; la persona que falta es la que conserva 26 filas con etiqueta, que no tiene ninguna con esa cobertura, lo que se contó antes de correr".
- **Texto propuesto (RD 7.11, tras la tabla de adaptación):** "En activación se evalúan 40 personas: una queda sin evaluación en la parte final de su sesión. En esa parte el equilibrio entre clases no está asegurado por la mediana de la sesión, y no se fijó un mínimo de ventanas por clase."

### A7 (sin objeción). Lo que está bien

La prueba de permutación de signos es adecuada para diferencias pareadas por persona. La precedencia entre reglas y la asimetría de "inferior" están declaradas. El tratamiento de P4 está declarado y tiene sensibilidad. La regresión a la media entre las 25 y las 16 personas está declarada con cifras. La enmienda del historial desplazado se registró antes de que existieran las predicciones con cinco ventanas (comprobado por fechas de archivo: protocolo de la enmienda 14:25, predicciones 14:49 del 16-11).

---

## B. Diseño

### B1 (bloqueante, nueva). El contraste que sostiene el "apoyo parcial" se presenta como "registrado antes de correr" sin decir que se diseñó tras ver el resultado que refina

- **Dónde.** RD 8.4, segundo párrafo; RD 8.1, tabla, fila 2; RD 6.6, fila "Ampliación"; CO 9.1, segundo párrafo; RE lámina 30 ("registrado antes"); EN, guion de la lámina 23 ("es el apoyo más sólido que tengo") y respuestas 13, 16 y 21.
- **Qué pasa.** El historial frente al placebo en activación (+0,038, p Holm 0,043) se conoció el 16-11 (commit de resultados de robustez, 13:25, titulado "en activación sí"). La ampliación con el historial desplazado se registró después, el mismo día (14:21 y 14:25), sobre las mismas 41 personas, las mismas particiones y un historial que comparte buena parte de sus ventanas con el ya visto. RD 6.6 rotula el control de posición como "Registrado, pero motivado por resultados vistos: post hoc". Con ese mismo criterio, el historial desplazado es un refinamiento de un resultado visto, y su p de Holm de 0,004 no es evidencia independiente del +0,038. El texto usa "registrado antes de correr" como el argumento de solidez del contraste.
- **Por qué es bloqueante.** Es el único contraste que sostiene la parte de la hipótesis que queda en pie, y la tesis aplica a otro análisis el criterio que aquí omite. No hay nada irregular en lo que se hizo; falta decirlo.
- **Se arregla redactando.**
- **Texto actual (RD 8.4):** "El contraste mejor sostenido es el que se registró antes de correr en la enmienda del 16-11: el historial sin las ventanas de 6 s que promedia la etiqueta supera a un placebo en +0,046 (p Holm 0,004)."
- **Texto propuesto:** "El contraste mejor sostenido es el del historial sin las ventanas de 6 s que promedia la etiqueta, que supera a un placebo en +0,046 (p Holm 0,004). Su protocolo se fijó antes de obtener sus predicciones, pero después de conocer, ese mismo día y en las mismas personas y particiones, que el historial completo superaba al placebo (+0,038; sección 7.3). Es un refinamiento dirigido de un resultado ya visto, con un historial que comparte ventanas con aquel, y no una segunda evidencia independiente."
- **Texto actual (RD 6.6, fila "Ampliación", estatus):** "Registrado; E1 principal, E2–E3 secundarios, E4–E6 descriptivos"
- **Texto propuesto:** "Registrado después de ver el placebo del análisis de robustez: dirigido; E1 principal, E2–E3 secundarios, E4–E6 descriptivos" (y lo mismo en el Anexo de trazabilidad).
- **Texto actual (CO 9.1):** "El contraste mejor sostenido es el que se registró antes de correr: el historial sin las ventanas de 6 s que promedia la etiqueta supera a un placebo de la misma persona"
- **Texto propuesto:** "El contraste mejor sostenido, fijado antes de obtener sus predicciones pero después de ver que el historial completo superaba al placebo en las mismas personas, es este: el historial sin las ventanas de 6 s que promedia la etiqueta supera a un placebo de la misma persona"
- **RE lámina 30, punto 1:** cambiar "registrado antes" por "protocolo fijado antes de sus predicciones, después de ver el placebo".

### B2 (bloqueante, nueva). El placebo no controla el contenido del estímulo, y dentro de un mismo estímulo no queda nada demostrado

- **Dónde.** RD 6.2, "Controles del origen de la mejora"; RD 7.3; RD 8.4; CO 9.1 y 9.7; RE láminas 21, 23 y 29; EN respuestas 2 y 16.
- **Qué pasa.** El historial real son ventanas del mismo estímulo; el placebo, ventanas de la misma persona en otros estímulos (o a 150 s o más en la curva). La diferencia entre ambos no es solo "segundos previos": es también estar en la misma página. En activación las entradas incluyen mirada y pupila, que dependen de la página (disposición, brillo), y la etiqueta es un nivel tónico lento que casi no cambia dentro de un estímulo (79 % de los segmentos son unánimes, según el INFORME de enfoques). Promediar las ventanas del mismo estímulo da una mejor descripción de "qué página es" y "en qué tramo de la sesión está la persona", que un placebo de otras páginas no puede dar. Los datos propios apuntan ahí: dentro de un mismo estímulo la ventana actual sola no distingue nada (0,501), el tiempo transcurrido solo aporta +0,049 y el historial no lo supera (+0,005 [−0,025; +0,035]; Q2, +0,009). RD 8.4 dice que los controles quedaron inconclusos y que "corresponde hablar de un resumen del historial reciente"; no dice que el placebo deja sin controlar el estímulo, que es la explicación alternativa más simple. La lámina 21 afirma "En activación, el placebo y los segundos no aportan, y el historial sí", lo que solo vale al comparar entre estímulos.
- **Por qué es bloqueante.** La pregunta B del encargo ("¿el placebo controla lo que dice controlar?") tiene respuesta: controla la persona y el largo del historial; no controla el estímulo ni la cercanía en la sesión. De eso depende lo que demuestra el +0,046.
- **Se arregla redactando.** El contraste historial desplazado menos placebo calculado solo dentro de un mismo estímulo saldría de predicciones guardadas, pero es análisis nuevo: se lista en D.
- **Texto actual (RD 6.2):** "un *historial placebo*: el mismo número de ventanas de la misma persona, tomadas de otros momentos;"
- **Texto propuesto:** "un *historial placebo*: el mismo número de ventanas de la misma persona, tomadas de otros estímulos. Iguala la persona y el largo del historial; no iguala el estímulo ni la cercanía en la sesión, de modo que el contraste entre el historial real y el placebo reúne tres cosas: la fisiología de los segundos previos, pertenecer a la misma página y estar en el mismo tramo de la sesión;"
- **Texto actual (RD 8.4):** "Por sí solo no separa "la fisiología previa predice la activación posterior" de "la fisiología de un momento se relaciona con la GSR de ese mismo momento, que la etiqueta posterior todavía contiene"."
- **Texto propuesto:** agregar a continuación: "Tampoco separa ninguna de las dos de una tercera lectura: el historial real pertenece al mismo estímulo que la ventana evaluada y el placebo no. Las entradas de activación incluyen mirada y pupila, que dependen de la página, y la etiqueta cambia poco dentro de un estímulo; un resumen de las ventanas de la misma página puede identificar la página o el tramo de la sesión mejor que una sola ventana. Los controles que aislarían esa lectura no la descartan: dentro de un mismo estímulo el tiempo transcurrido aporta por sí solo (+0,049 [+0,027; +0,072]) y no se demostró que el historial lo supere (+0,005 [−0,025; +0,035])."
- **Texto actual (CO 9.1):** "Por eso el contraste no demuestra por sí solo que el pasado prediga el presente."
- **Texto propuesto:** "Por eso, y porque el placebo proviene de otros estímulos y el historial real del mismo, el contraste no demuestra por sí solo que el pasado prediga el presente: no separa la fisiología previa de pertenecer a la misma página."
- **Texto actual (RE lámina 21, nota):** "En activación, el placebo y los segundos no aportan, y el historial sí, incluso sin las ventanas de 6 s que promedia la etiqueta."
- **Texto propuesto:** "En activación, al comparar entre todas las ventanas, el placebo y los segundos no aportan, y el historial sí, incluso sin las ventanas de 6 s que promedia la etiqueta. Ojo: el placebo viene de otras páginas, y dentro de una misma página los segundos sí aportan y no demostré que el historial los supere."

### B3 (importante, nueva). El control del tiempo de sesión solo corrige la tendencia común a las personas

- **Dónde.** RD 7.1, "Controles registrados"; RD 8.4, tercer párrafo.
- **Qué pasa.** El INFORME de la reapertura lo declara ("P2 solo corrige la tendencia de sesión común a las personas. En activación la deriva tiene dirección distinta en cada persona"); los borradores no. Con etiquetas relativas a la mediana de cada sesión, una deriva lenta propia de cada persona es justo lo que un historial cercano capta y un placebo lejano no.
- **Texto actual (RD 8.4):** "el control registrado del tiempo de sesión quedó inconcluso."
- **Texto propuesto:** "el control registrado del tiempo de sesión quedó inconcluso y, además, solo corrige la tendencia común a las personas: una deriva lenta con dirección distinta en cada persona queda fuera de ese control."
- El INFORME lista otros dos límites de la curva que RD 7.3 no recoge y conviene copiar en "Límites de la curva": "El placebo incluye ventanas futuras (16–36 % según la tarea)" y "El placebo iguala el número de ventanas de la banda de 6 s; en las demás bandas coincide en el 30–44 % de las filas".

### B4 (importante, nueva). La adaptación a la persona se concluye sin su límite

- **Dónde.** CO 9.3, último párrafo; RD 8.5, "Adaptación a la persona".
- **Qué pasa.** Las etiquetas de calibración se definen con la mediana de toda la sesión. Como cada persona tiene la mitad de sus ventanas en cada clase por construcción, la proporción de clase alta en el 40 % inicial determina la del resto: las etiquetas de calibración informan sobre la parte evaluada. RD 7.11 dice que la adaptación "es offline"; no dice este mecanismo, y CO 9.3 la presenta como una de "las mayores mejoras" sin ningún límite.
- **Texto actual (CO 9.3):** "Las mayores mejoras en activación se obtuvieron al adaptar el modelo a cada persona (+0,045 [+0,023; +0,069] sobre el modelo con historial) y al predecir por estímulo (AUC 0,587); aun así, el desempeño es bajo."
- **Texto propuesto:** "Las mayores diferencias en activación se obtuvieron al adaptar el modelo a cada persona (+0,045 [+0,023; +0,069] sobre el modelo con historial) y al predecir por estímulo (AUC 0,587). Ninguna de las dos es utilizable en línea ni comparable con los demás contrastes: las etiquetas de calibración se definen con la mediana de toda la sesión, de modo que informan sobre la parte evaluada, y el modelo por estímulo usa ventanas posteriores a cada etiqueta. Aun así, el desempeño es bajo."
- **Texto propuesto (RD 7.11, tras "no equivale a una calibración utilizable en línea"):** "Como cada persona tiene la mitad de sus ventanas en cada clase, la proporción de clase alta en la parte de calibración fija la de la parte evaluada."

### B5 (sin objeción nueva). Lo demás del diseño

La validación cruzada por persona con grupos que comparten orden está declarada (SP 4.8.2, RD 8.8). La fuga del *Modelo Profesor* con PCA está medida. Las etiquetas relativas a la mediana no crean dependencia entre personas de entrenamiento y de evaluación; crean las dependencias dentro de la persona de B3 y B4. El historial filtra el número de ventanas y la posición, y eso está declarado y controlado en atención; falta explicar el mecanismo (ver E4).

---

## C. Argumento

### La conclusión en una frase

> Con 41 personas y pseudoetiquetas relativas a cada sesión, un modelo con EEG distingue de forma estable la etiqueta ocular alta de la baja (AUC 0,68, también dentro de un mismo estímulo y a igual posición), pero parte de esa detección depende de componentes oculares del propio EEG y lo que parecía un aporte del historial es el tiempo transcurrido en la página; en la activación medida con GSR hay un indicio pequeño y no confirmado de que resumir los segundos previos ayuda, que no se separó del estímulo ni del soporte de la etiqueta, de modo que la superioridad de los modelos temporales multimodales no queda establecida.

### ¿CO dice exactamente eso?

Casi. CO 9.1 a 9.5 lo dicen con sus límites. Se aparta en cuatro lugares por exceso y en tres por defecto.

### Donde se afirma más de lo que se sostiene

**C1 (importante, nueva). CO 9.7 no carga los límites que CO 9.1 sí declara.**
- **Texto actual:** "En activación hay evidencia acotada de que el historial reciente de las señales, el de los segundos previos, ayuda a predecir el *Arousal Score*. El efecto es pequeño y requiere confirmación en una cohorte nueva, y el contraste simple entre el modelo con y sin historial es desigual entre personas."
- **Texto propuesto:** "En activación hay evidencia acotada de que un resumen del historial reciente de las señales ayuda a predecir el *Arousal Score*. Proviene de un análisis posterior al diseño original, que no había mostrado una ventaja consistente; el efecto es pequeño y desigual entre personas, no se separó de pertenecer al mismo estímulo ni del soporte temporal de la etiqueta, sus controles quedaron inconclusos y requiere confirmación en una cohorte nueva."

**C2 (importante, nueva; toca la decisión 5 y no la cierra). "Apoyo parcial" es la lectura más favorable de tres.** RD 8.1 lo expone con honestidad. Para la decisión conviene que el profesor guía vea las tres juntas: (i) con el diseño y la regla planificados, "no hay evidencia para sostener la hipótesis"; (ii) con el segundo diseño y el criterio literal, ventaja en las dos variables; (iii) con el segundo diseño y la exigencia añadida, ventaja solo en activación, sobre un contraste con los límites de B1 y B2. No se propone texto: es insumo para la minuta.

**C3 (importante, nueva). La explicación por latencia de las respuestas no corresponde a una etiqueta que es nivel tónico.**
- **Dónde.** RD 8.5, "Escala temporal"; RD 8.7, tercera viñeta; RE lámina 28, fila "Tiempos" y nota; EN respuesta 7.
- **Qué pasa.** RD 6.1 establece que el *Arousal Score* es, en lo esencial, el nivel tónico (AUC 0,911, frente a 0,522 del número de respuestas). RD 8.5 explica la falta de detección con la latencia de las respuestas fásicas y habla de "la respuesta que define la etiqueta". RD 8.7 recomienda "trabajar con ventanas más largas o con la componente tónica", que es lo que la etiqueta ya es. Un evaluador de psicofisiología lo ve de inmediato.
- **Texto actual (RD 8.5):** "Una ventana de EEG de 2 s no coincide con la respuesta que define la etiqueta. Esta diferencia de escalas es coherente con el resultado temporal de activación, con las reservas de la sección 8.4."
- **Texto propuesto:** "Este argumento vale para la parte fásica, que pesa poco en la etiqueta usada: el *Arousal Score* es, en lo esencial, el nivel tónico (sección 6.1), que cambia en decenas de segundos y se obtuvo con un filtro que mira hacia atrás y hacia adelante. La diferencia de escalas que importa es entonces otra: una ventana de EEG de 2 s frente a un nivel lento y relativo a la sesión. Es coherente con el resultado temporal de activación, con las reservas de la sección 8.4."
- **Texto actual (RD 8.7):** "**Para la activación**, la escala temporal de la respuesta electrodérmica sugiere trabajar con ventanas más largas o con la componente tónica, en lugar de ventanas de 2 s."
- **Texto propuesto:** "**Para la activación**, la etiqueta usada ya es en lo esencial el nivel tónico; su escala temporal sugiere predecirla con ventanas más largas que 2 s y definirla con un filtro causal."
- **RE lámina 28, fila "Tiempos", columna "Qué dice la fisiología":** agregar "; mi etiqueta es sobre todo nivel tónico, más lento aún".

**C4 (menor, nueva). Lámina 1 y lámina 30.** "con un efecto pequeño y de pocos segundos" (nota de la lámina 1) afirma un alcance que la curva no demuestra; propuesto: "con un efecto pequeño y con respaldo solo para los 6 s previos". El título de la lámina 30, "Conclusiones: la hipótesis tiene apoyo parcial", enuncia como hecho la decisión 5; propuesto: "Conclusiones: apoyo parcial a la hipótesis (encuadre por decidir)", como ya hace la lámina 31.

### Donde el texto se disculpa tanto que oculta un resultado que sí se sostiene

**C5 (importante, nueva). La detección de atención se mantiene dentro de un mismo estímulo, y RD no lo informa.**
- **Dónde.** RD 7.2, "Cuánto depende la etiqueta del reloj"; RD 8.3, primer párrafo; CO 9.3.
- **Qué pasa.** La pregunta obvia ante una etiqueta ocular es si el modelo solo reconoce el tipo de página (texto, sitio, imagen), dado que el grupo comparte orden. Está respondida en `reapertura_fase3_41p_22-11-2026/descriptivos.csv` y no llega al texto: la AUC sin historial calculada solo con pares del mismo estímulo es 0,684 [0,667; 0,700], igual que la global (0,683), y dentro del mismo minuto 0,675 [0,660; 0,689]. RD solo da el estrato de posición (0,677).
- **Texto actual (RD 7.2):** "La detección no es un artefacto de la posición: comparando solo ventanas de la misma posición, la AUC sin historial es 0,677 [0,654; 0,699], frente a 0,684 sin estratificar en la misma partición."
- **Texto propuesto:** agregar a continuación: "Tampoco se explica por reconocer el estímulo o el tramo de la sesión: con cinco particiones, la AUC sin historial calculada solo con pares de ventanas del mismo estímulo es 0,684 [0,667; 0,700], frente a 0,683 con todas, y dentro del mismo minuto, 0,675 [0,660; 0,689] (descriptivo; el estrato del mismo estímulo usa cerca del 2 % de los pares)."
- **CO 9.3**, tras "(0,621, también en las 41)": agregar "; la detección es la misma al comparar solo ventanas de un mismo estímulo (0,684)".

**C6 (importante, nueva). El nulo del historial en atención no depende del margen de 0,02.**
- **Dónde.** SP 4.8.3 ("Es una propuesta sin justificación independiente"); RD 6.4; RD 8.2; CO 9.1.
- **Qué pasa.** El texto repite que el margen no está aprobado y deja la impresión de que el nulo cuelga de él. El intervalo de 95 % del contraste registrado es [−0,002; +0,005]: el nulo se sostiene con cualquier margen de 0,005 o más, muy por debajo de los 0,181 que el modelo tiene sobre el azar. Es el resultado negativo más limpio de la tesis.
- **Texto actual (CO 9.1):** "Cuando el modelo conoce la posición de la ventana dentro del estímulo, lo que agrega el historial queda dentro del margen de ±0,02 (+0,001 [−0,002; +0,005])."
- **Texto propuesto:** "Cuando el modelo conoce la posición de la ventana dentro del estímulo, lo que agrega el historial es +0,001 [−0,002; +0,005]: queda dentro del margen de ±0,02 y lo estaría con cualquier margen de 0,005 o más, de modo que este resultado no depende del margen elegido."
- Misma frase en RD 8.2, tras "queda dentro de ±0,02 cuando el modelo conoce ese número".

**C7 (importante, nueva). La lección del placebo y la posición no figura como aporte.** CO 9.7 nombra como advertencia metodológica solo "el uso de pseudoetiquetas oculares para evaluar modelos basados en EEG". El otro hallazgo es igual de general y está mejor demostrado: una mejora "temporal" estable, en 36 de 41 personas, la reproduce un solo número.
- **Texto actual (CO 9.7):** "y una advertencia metodológica sobre el uso de pseudoetiquetas oculares para evaluar modelos basados en EEG."
- **Texto propuesto:** "y dos advertencias metodológicas: que una ventaja de un modelo con historial puede provenir del tiempo transcurrido en el estímulo y no de las señales previas, lo que solo se ve con un placebo y con la posición como control; y que las pseudoetiquetas oculares no permiten evaluar modelos basados en EEG como si las dos señales fueran independientes."

---

## D. Lagunas

### Se responden con redacción o con datos ya calculados

1. **¿El modelo de atención reconoce el estímulo y no la conducta?** Respondida en los CSV (C5).
2. **¿Qué significa "alta" en el *Attention Score*?** (importante; ya planteada como menor 10 del primer lector, no resuelta). RD 6.1 da los pesos (recorrido 0,557; dispersión 0,520; duración media 0,508; tiempo total 0,398; pupila −0,052) sin decir la orientación. El script orienta la componente para que su suma ponderada sea positiva. El INFORME de enfoques dice que "la etiqueta mide quietud de la mirada", lo que no calza con pesos positivos del recorrido y la dispersión. **Texto propuesto (RD 6.1, tras los pesos):** "La componente se orienta de modo que estos pesos sean positivos: "alta" designa ventanas con más recorrido y dispersión de la mirada y fijaciones más largas que la mediana de la persona [confirmar en `reconstruir_profesor_atencion_binaria.py` si alguna variable entra invertida antes de la componente]. No designa mayor atención en ningún sentido validado."
3. **¿Por qué la GSR sola detecta la etiqueta ocular (0,545)?** RD 7.7 no lo interpreta. Con los datos que hay, la lectura prudente es que la GSR estandarizada por sesión informa del tramo de la sesión, y la etiqueta depende del reloj (el tiempo de sesión agrega +0,025; el INFORME de ampliación anota que la prevalencia de "alta" cae a 0,32 en el tercer quinto, "que coincide con un bloque de estímulos común a las secuencias"). **Texto propuesto (RD 7.7, tras "(B3, nulo concluyente)"):** "Que la GSR sola detecte una etiqueta ocular no se estudió; una lectura posible es que, estandarizada por sesión, informe del tramo de la sesión, del que la etiqueta depende (sección 7.2)."
4. **¿Cómo son los estímulos?** Los capítulos 6 a 8 no dicen cuántos son, de qué tipos ni cuánto duran. "Mediana de tres ventanas por segmento" aparece por primera vez en RD 8.2, y los 116 estímulos solo en la lámina 4. Hace falta un párrafo en RD 6.1 o SP 4.3 con número, tipos y distribución de duraciones; con una mediana de tres ventanas, "historial hasta 32" confunde.
5. **¿Cuántas ventanas tiene la etiqueta de atención?** RD da el conteo de activación (11.796) y no el de atención.
6. **Familia de Holm, tipo de intervalo, personas faltantes:** A1, A3, A6.
7. **Límite del control de sesión y del placebo de la curva:** B3.
8. **¿Qué pasó con los objetivos 3 y 6 y con las contribuciones 2 a 6 de ET?** (ya planteada: I24 y B4 del primer lector; no resuelta en ET, que no se tocó). EN 35 lo responde a medias.

### Requiere análisis nuevo (solo se lista; la experimentación está cerrada)

- Historial desplazado menos placebo calculado solo con pares del mismo estímulo (sale de predicciones guardadas; no requiere entrenar).
- Línea base de "identidad del estímulo": prevalencia de la etiqueta por estímulo aprendida con las demás personas del grupo.
- Intervalos t o BCa y bootstrap por grupo experimental; validación cruzada dejando grupos fuera.
- Sensibilidad con un mínimo de ventanas por persona y por clase.
- Sensibilidad con 7 hojas o selección anidada (ya declarada).
- Placebo del mismo estímulo con ventanas posteriores, para separar "misma página" de "segundos previos".
- Etiqueta de activación con filtro causal; etiqueta de atención con pesos iguales (ya declaradas).
- Un recuento del total de pruebas hechas en las doce etapas.

---

## E. Legibilidad de los capítulos 6 a 8

Un evaluador externo entiende 6.1 a 6.4, 7.7 a 7.10 y 8.3. Se pierde en 7.1 a 7.5 y en 8.4. Pasajes concretos:

1. **Fechas como nombres** (ya planteada: menor 1; mal resuelta). RD 6.6 promete identificar "por su contenido" y el capítulo 7 sigue con "16-11", "22-11, fase 3", "cierre V3", "reapertura", "ampliación", "enmienda". En RD 7.3 una misma tabla tiene columnas "fase 1, secundaria" y "fase 2, post hoc". Propuesta: nombres fijos de contenido (evaluación con particiones originales; análisis principal; repetición con cinco particiones; control de posición; curva temporal) y fechas solo en el anexo.
2. **RD 7.3, párrafo "El +0,047 de la curva (22-11) y el +0,046 del historial desplazado (16-11) se parecen, pero no son el mismo contraste".** Hay que leerlo tres veces. Pide una tabla de dos filas (ventanas usadas, placebo, particiones, personas).
3. **RD 7.5, tabla.** "25 de la búsqueda" no se entiende sin la sección 4.8.2; la fila "Banda de 6 s − placebo (40 personas: 24 y 16)" cambia el denominador sin aviso en el encabezado; "GRU hasta 32 − GRU una ventana (sin búsqueda)" mezcla dos ideas.
4. **RD 6.2: "por su largo, codifica la posición"** (ya planteada: menor 9; no resuelta). No se explica cómo. **Texto propuesto:** "El resumen incluye la ventana actual. Informa además de cuántas ventanas lo forman, aunque ese número no sea una variable: con una sola ventana la desviación es cero, y con pocas la media y la desviación son más ruidosas. Por esa vía el modelo conoce la posición de la ventana dentro del estímulo."
5. **"Estímulo", "segmento", "página", "tramo"; "partición" y "grupo" con dos y tres sentidos** (ya planteada: menores 4 y 5; no resuelta).
6. **RD 7.2, "AUC estratificada".** Un solo párrafo con siete intervalos, dos modelos de comparación y tres estatus de registro. Pide tabla.
7. **RD 7.7.** La segunda tabla trae columnas de un análisis que se explica dos secciones después.
8. **"Hojas", "contexto de 32", "c32"** aparecen en RD 7.5 sin haber dicho en 6.2 que el número de hojas es el único hiperparámetro buscado y que la búsqueda fue entre dos valores.
9. **RD 8.10 y las "Notas de trabajo"** están rotuladas como ajenas a la tesis; bien. Las líneas "Fuentes:" con rutas siguen dentro de cada sección.
10. **"Confirmatorio"** se redefine en RD 6.5 y luego EN prohíbe usarlo. En RD 7.1 aparece "segundo contraste de la familia confirmatoria". Mejor "familia fijada de antemano" en todas partes.

---

## F. Presentación y defensa

### ¿Cuenta la misma historia?

Sí en lo esencial y con las mismas cifras. Tres diferencias: la lámina 21 afirma más que RD 7.3 (B2); la lámina 28 hereda la explicación por latencia (C3); el título de la lámina 30 enuncia el encuadre como hecho (C4). Una cuarta es de procedimiento: EN, "Fuentes", dice "Ante cualquier diferencia mandan los informes". Los `INFORME.md` conservan lecturas que los borradores moderaron ("un efecto del historial confirmado y de corto alcance", "desaparece a partir de 24 s", "agente independiente"). **Texto propuesto (EN):** "Ante cualquier diferencia de cifras mandan los CSV y los informes; para las lecturas mandan los borradores del 23-11, que moderan varias frases de los informes."

### Respuestas que no resistirían una repregunta

| N.º | Punto débil de la respuesta | Repregunta |
|---|---|---|
| 2 | "Lo que tiene interés es el contraste pareado: el historial reciente mejora y un placebo no" | El placebo es de otras páginas. Dentro de una misma página, ¿el historial supera al tiempo transcurrido? (No demostrado: +0,005.) Entonces, ¿qué mide el contraste? |
| 4 | "Cada protocolo entró a Git antes que sus predicciones" | El contraste que usted llama más sólido se registró una hora después de ver que el historial le ganaba al placebo en las mismas personas. ¿En qué se diferencia del control de posición, que usted llama post hoc? |
| 6 | "Es una propuesta mía, sin justificación" | ¿Con qué margen dejaría de ser nulo el resultado de atención? (Con ninguno de 0,005 o más; hoy la respuesta no lo dice y pierde su mejor argumento.) ¿Y por qué usa el mismo margen para "AUC − 0,5"? |
| 7 | Explica con la latencia de las respuestas | Su etiqueta es nivel tónico (0,911) y el número de respuestas casi no la ordena (0,522). ¿Qué tiene que ver la latencia? |
| 13 | "El aporte más sólido es el metodológico" | Que los movimientos oculares contaminan el EEG se sabe desde hace décadas; usted mismo cita a Croft y Barry (2000). ¿Qué agrega su tesis? (Respuesta posible con lo que hay: la medida del tamaño en un diseño profesor–estudiante, y el caso de la posición.) |
| 14 | "Evaluar los modelos ya congelados, sin reentrenar" | ¿Qué modelo exactamente? En el análisis con 41 personas hay ocho modelos por partición. ¿El ajustado con las 25, o uno nuevo con las 41? Y el tamaño de muestra se calculó para otro contraste. |
| 16 | "El apoyo descansa en el contraste registrado contra placebo" | Mismas dos repreguntas de 2 y 4. |
| 21 | "El apoyo más sólido es otro contraste, registrado antes de correr" | Ídem 4. |
| 22 | "La hizo un asistente automático" | ¿Cuál, con qué instrucciones, y quién verificó al verificador? ¿Dónde lo declara la tesis? (Pendiente real.) |
| 28 | "con cuatro grupos eso daría poca inferencia" (ya planteada: respuesta 8 del primer lector; mal resuelta) | Dejando un grupo fuera se obtienen igual 41 AUC por persona; la inferencia sigue siendo por persona. ¿Por qué daría poca? (Lo que cambia es que cada modelo se ajusta con menos personas y solo hay cuatro modelos.) **Texto propuesto:** "No evalué dejando grupos fuera; se puede hacer con cuatro grupos de evaluación y la inferencia seguiría siendo por persona, pero requiere volver a entrenar." |
| 34 | "Lo que tiene a favor es interno: persiste entre ventanas" | Un nivel filtrado a 0,05 Hz persiste por construcción. ¿Qué evidencia hay que no venga del filtro? |

### Preguntas que faltan

1. Sus intervalos, ¿son percentil? ¿Qué pasa con los rótulos que están a una milésima del umbral? (A1)
2. En validación cruzada las AUC por persona comparten modelos. ¿Qué cubre y qué no cubre su intervalo? (A2)
3. ¿El modelo de atención reconoce la página o la conducta? (C5; hay respuesta y es buena.)
4. ¿Qué es, en conducta, una ventana "alta" de atención: más movimiento o menos? (D2)
5. ¿Por qué dicotomizar por la mediana un puntaje continuo, si el objetivo 3 comprometía etiquetas continuas y categóricas?
6. ¿Por qué la GSR sola predice una etiqueta ocular? (D3)
7. La adaptación a la persona, ¿no se beneficia de que la mediana de la sesión fije la proporción de clases del resto? (B4)
8. Los objetivos pedían BA, macro-F1 y *recall*; ¿por qué la decisión es con AUC y qué dicen las otras?
9. ¿Cuántas pruebas hizo en total en las doce etapas?
10. Si hoy empezara de nuevo con estos datos, ¿qué diseño usaría? (Respuesta disponible en RD 8.7 y 8.9.)
11. ¿Qué resultado habría refutado la hipótesis? (El del cierre V3; conviene decirlo sin rodeos.)
12. Su trabajo previo de referencia (Saavedra) no halló mejora con fusión tardía. ¿Su resultado lo confirma, lo contradice o no dice nada? (No dice nada concluyente: RD 7.6.)

---

## G. Reglas del proyecto

- **Aprobación del profesor guía:** no se encontró ninguna afirmada. La única mención (etiquetas GSR V2, 01-11) está como lo que Mario comunicó.
- **Siete decisiones abiertas:** ninguna cerrada en el cuerpo de los borradores. Dos roces menores: el título de la lámina 30 (C4) y RD 8.9 y CO 9.6, que escriben el trabajo futuro como si la decisión 1 ya fuera "sin cohorte nueva"; lo cubre el aviso inicial.
- **"Activación" y no "emociones":** cumplido en SP, RD, CO, RE y EN. "Activación emocional" sigue en los objetivos y alcances de ET (ya planteado por el primer lector; ET no se tocó). Uso suelto en RD 7.12: "La atención se predice mejor en sitios web"; propuesto: "La etiqueta de atención se predice mejor en sitios web".
- **Atención por EEG no leída como cerebral:** cumplido. La lámina 7 dice "modelos de atención tipo Transformer", donde "atención" es el mecanismo de la red; propuesto: "modelos tipo Transformer".

---

## H. Recuento y relación con el primer lector

| N.º | Objeción | Gravedad | Estado frente al primer lector |
|---|---|---|---|
| B1 | Contraste "registrado antes" diseñado tras ver el placebo | Bloqueante | Nueva (su I7 trató el registro en general) |
| B2 | El placebo no controla el estímulo | Bloqueante | Nueva (su I16 trató el movimiento) |
| A2 | Dependencia de las AUC en validación cruzada | Importante | Nueva |
| A4/C6 | El nulo de atención no depende del margen | Importante | Nueva |
| B3 | El control de sesión solo corrige la tendencia común | Importante | Nueva |
| B4 | Adaptación concluida sin su límite | Importante | Nueva |
| C1 | CO 9.7 sin los límites de 9.1 | Importante | Nueva (su B1 quedó bien resuelta en RD 8.1 y CO 9.1) |
| C2 | Tres lecturas del veredicto | Importante | Nueva como insumo; el fondo ya planteado (B1, B5) y bien resuelto |
| C3 | Latencia fásica frente a etiqueta tónica | Importante | Nueva (su I5 quedó bien resuelta) |
| C5 | Detección dentro del mismo estímulo, sin informar | Importante | Nueva |
| C7 | La lección del placebo no figura como aporte | Importante | Nueva |
| A5 | "Efecto relevante" contra 0,5 | Importante | Ya planteada (menor 6), mal resuelta |
| D2 | Orientación del *Attention Score* | Importante | Ya planteada (menor 10), no resuelta |
| E1 | Fechas como nombres de etapa | Menor | Ya planteada (menor 1), mal resuelta |
| E4 | "Por su largo, codifica la posición" | Menor | Ya planteada (menor 9), no resuelta |
| E5 | Términos con varios sentidos | Menor | Ya planteada (menores 4 y 5), no resuelta |
| F-28 | "Con cuatro grupos daría poca inferencia" | Menor | Ya planteada (su respuesta 8), mal resuelta |
| D8 | Objetivos y contribuciones de ET | (conocida) | Ya planteada (B4, I24), no resuelta en ET, que no se editó |
| A1, A3, A6, C4, D3, D4, D5, EN "mandan los informes" | — | Menor | Nuevas (8) |

Bien resueltas del primer lector, comprobadas en esta lectura: B1, B2, B3, B5 y B6; I1 a I5, I7 a I13, I15 a I17. B7 (participantes y ética) sigue pendiente de documentos del proyecto.

Recuento: 2 bloqueantes nuevas; 9 importantes nuevas; 8 menores nuevas; 2 importantes y 4 menores ya planteadas que quedaron mal o no resueltas; 1 conocida (ET).
