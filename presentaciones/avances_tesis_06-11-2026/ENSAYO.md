# Ensayo de la presentación de avances

Escrito el 23-11-2026 para la versión 7 de la presentación (39 láminas: 33 principales y 6 anexos) y puesto al día ese mismo día, después de la corrección de la presentación: fusión y sesión pasaron a ser las láminas 19 y 20, el bloque "qué explica la mejora" quedó en 21 a 23, y la última lámina pregunta cinco cosas. Se volvió a poner al día el 23-11-2026 tras la auditoría de los resultados (`documentacion/auditoria_final_23-11-2026/AUDITORIA_EXPERIMENTO.md`): las cifras se reprodujeron y hubo que moderar varias lecturas, que cambiaron las láminas 1, 26, 27, 28, 29, 30, 31 y 33. El 26-11-2026 se puso al día otra vez, tras la auditoría de coherencia (`documentacion/auditoria_final_23-11-2026/ronda2/AUDITORIA_COHERENCIA.md`): el +0,047 es la curva temporal en una partición y no una repetición con cinco, cambió el título de la lámina 23 y se ajustaron pies y notas. El 26-11-2026 se puso al día una vez más, tras una lectura crítica del material (`documentacion/auditoria_final_23-11-2026/ronda3/LECTURA_CRITICA_COMITE.md`) y tras la auditoría de código de la misma ronda (`documentacion/auditoria_final_23-11-2026/ronda3/AUDITORIA_CODIGO.md`): cambiaron el título y el pie de la lámina 12, el texto visible de las láminas 5, 10, 29, 30 y 31 y varias notas, y la sección de preguntas pasó de 22 a 37. Ese mismo día se puso al día por última vez, tras la segunda auditoría de la presentación (`documentacion/auditoria_final_23-11-2026/ronda4/AUDITORIA_PRESENTACION_R2.md`): se redistribuyeron los tiempos, se recortó el guion hablado para que ninguna lámina pase de 150 palabras por minuto, cada respuesta larga lleva delante una versión corta, y se ajustaron títulos, pies y notas (detalle al final). El 27-11-2026 se puso al día tras una segunda lectura crítica (`documentacion/auditoria_final_23-11-2026/ronda6/SEGUNDA_LECTURA_COMITE.md`), después de comprobar cada hecho en las fuentes: cambiaron el título de la lámina 30, el texto visible de las láminas 28 y 30, las notas de las láminas 1, 7, 21, 23, 28 y 30 y el guion hablado de las láminas 21, 23, 28 y 30; se corrigieron doce respuestas (2, 4, 6, 7, 13, 14, 15, 16, 21, 22, 28 y 34) y la sección de preguntas pasó de 37 a 49. No reemplaza a `GUIÓN.md`, que se regenera desde `relato.py`; este archivo es solo para ensayar y no se regenera: hay que revisarlo a mano después de cada cambio en `relato.py`.

**Supuesto de duración.** Mario no fijó cuánto dura la reunión. Este ensayo asume **20 minutos de exposición más preguntas**, y trae una versión corta de 10 minutos por si el tiempo se acorta. Si la duración real es otra, hay que rehacer la tabla.

**Fuentes.** `GUIÓN.md` y `relato.py` de esta carpeta; `documentacion/auditoria_final_23-11-2026/AUDITORIA_EXPERIMENTO.md`; `documentacion/Cierre_Experimental_Final_23-11-2026.md`; `Escritura/Borrador Conclusiones 23-11-2026.md` y `Escritura/Borrador Resultados y Discusión 23-11-2026.md` (vigente; desde el 26-11 integra la discusión fisiológica) del vault; los `INFORME.md` de `resultados/` entre el 16 y el 23-11-2026, más `etiquetas_gsr_calidad_v2_01-11-2026`, `protocolo_hipotesis_reintento_06-11-2026` y `cierre_v3_16-11-2026`. Ante cualquier diferencia de cifras mandan los CSV y los informes; para las lecturas mandan los borradores del 23-11, que moderan varias frases de los informes.

**Lo que no se puede decir.**

- No consta aprobación del profesor guía sobre los resultados de noviembre ni sobre el margen de 0,02. Lo único registrado es que Mario comunicó el 01-11 que el profesor aprobó usar las etiquetas GSR V2 (`notas/bitacora.md`).
- Siguen abiertas siete decisiones. Las cinco primeras van en la lámina 33, en el orden de la minuta: cohorte nueva o escribir, margen de 0,02, activación en vez de emociones, etiqueta de atención original o corregida por posición, y encuadre de apoyo parcial. Se presentan como preguntas, no como hechos. La normalización con la sesión completa y el Modelo Profesor con PCA como definición del Attention Score son el sexto y el séptimo punto; van en el pie de la lámina 33 y de palabra, y pueden pesar más que los otros, porque si no se aceptan obligan a repetir análisis. La minuta del 23-11 lista las siete y ninguna está tomada.
- Nada es una confirmación independiente: las 41 personas ya se habían consultado. No usar "confirmado" ni "confirmatorio" para el efecto de activación; la palabra es "respaldo".
- Lecturas que la auditoría pidió moderar y que no deben aparecer al hablar:
  - "El EEG detecta sobre todo los ojos" o "un tercio es la huella de los ojos". Lo medido: la AUC sobre el azar baja cerca de un tercio al quitar los componentes más ligados a la mirada (0,060 de 0,181). Lo leo como cota inferior, sin que sea una demostración: esos componentes se eligen con la mirada, que también define la etiqueta. El modelo limpio sigue sobre el azar en las 41 personas, y no se puede descartar que el resto también dependa de los ojos.
  - "Sin solapamiento con la etiqueta". El contraste de activación excluye las ventanas de 6 s que promedia la etiqueta, pero el filtro tónico de la GSR usa toda la sesión.
  - "Auditoría independiente" o "prerregistro". Las auditorías son revisiones y recálculos con código separado, hechos con un asistente automático a pedido mío; el registro es el orden de commits de mi propio repositorio.
  - "La configuración se eligió solo con entrenamiento", sin más. Es cierto, pero las 15 hojas de activación las decidió el modelo con historial y esas 25 personas son 25 de las 41 evaluadas; el efecto se concentra en ellas. Sesgo posible, no demostrado.
  - "La etiqueta de atención sale de la mirada y la pupila", sin más. En el Modelo Profesor con PCA la pupila pesa −0,05: en la práctica es conducta de mirada.
  - "Elegí PCA porque es mejor". Seguí con PCA tras ver que se predecía mejor, y eso no es un argumento de validez.
  - "La ventaja de la red es ocular". Lo medido: la red pierde 0,067 al limpiar; su ventaja sobre el HGB se mantiene con el EEG limpio (+0,028 frente a +0,035).
  - "El efecto está en los 6 a 12 s" o "desaparece desde los 24 s". Solo hay respaldo a 6 s; a 12 s es inconcluso (+0,024) y desde 24 s no se distingue del placebo, sin demostrar ausencia.
  - "La fusión tardía es mejor". Es un secundario entre redes MLP (+0,012); con HGB, en el cierre V3, el signo fue el contrario.
- Tres lecturas que la segunda lectura crítica (27-11) pidió moderar:
  - "Registrado antes de correr", sin más, para el +0,046. Su protocolo se fijó antes de sus predicciones, pero después de ver, el mismo día y en las mismas personas, que el historial completo le ganaba al placebo (+0,038): es un análisis dirigido, no una segunda evidencia.
  - "El placebo controla todo menos el tiempo". Iguala la persona y el largo del historial; viene de otras páginas y de cualquier momento de la sesión. Dentro de una misma página los segundos transcurridos aportan y no demostré que el historial los supere.
  - "La GSR tarda segundos y por eso no calza con el EEG", sin más. La latencia vale para la parte fásica; la etiqueta es en lo esencial el nivel tónico, más lento.
- Dos intervalos corregidos por la auditoría (redondeo): activación a 6 s frente al placebo, 22-11, [+0,017; +0,078]; caída por limpieza ocular, [+0,044; +0,075].
- Términos fijos: Modelo Profesor, Modelo Estudiante, Attention Score, Arousal Score. Distinguir siempre lo Observado (mirar) de lo Atendido (atender).

## Antes de ensayar: lo que todavía no calza en la presentación

Las diferencias de las versiones anteriores quedaron corregidas en `relato.py`, incluidas las seis que este ensayo listaba antes de la auditoría (fechas del +0,046 y del +0,038 en la lámina 23; "6 a 12 s" en la lámina 30; el margen de 0,02 en la nota de la lámina 26; el índice de la lámina 2; el séptimo punto de la minuta en la lámina 33). No queda ninguna diferencia conocida entre este ensayo y `relato.py` (revisado el 26-11-2026, después de la lectura crítica y de la segunda auditoría de la presentación, y otra vez el 27-11-2026, después de la segunda lectura crítica); la única diferencia conocida con los borradores está en la tabla del final (lámina 31). El detalle que quedaba fuera de `relato.py` también se corrigió, en `estilo_tecnico.py`: la sigla "OOF" salió del eje del gráfico de la lámina 12, igual que del gráfico de la lámina 38 y de la tabla de la 37.

---

## 1. Plan de tiempo

### Versión de 20 minutos (1.200 s)

Ritmo: "rápido" es una frase y avanzar; "normal" es el guion completo; "clave" es donde conviene frenar y mirar al profesor.

| Lámina | Título | Segundos | Ritmo | La única idea que hay que dejar |
|---|---|---:|---|---|
| 1 | ¿Sirve el historial de señales para predecir atención y activación? | 25 | normal | Hay resultados nuevos y siete decisiones que tomar |
| 2 | De qué voy a hablar | 10 | rápido | Nueve partes; lo nuevo va desde los resultados con 41 personas |
| 3 | La hipótesis | 40 | normal | Comparo el mismo modelo con y sin historial |
| 4 | Los datos: Toma de Muestra 2, navegación web en laboratorio | 35 | normal | Cuatro señales, dos equipos, ventanas de 2 s |
| 5 | Unas señales arman la etiqueta y otras la predicen | 50 | clave | Modelo Profesor arma la etiqueta, Modelo Estudiante la predice con otras señales |
| 6 | 48 personas registradas, 41 en el análisis | 35 | normal | La unidad es la persona, y todas ya se habían mirado |
| 7 | Qué señales combinan los trabajos recientes | 25 | rápido | No encontré estas cuatro señales juntas en navegación web |
| 8 | Lo que falta en la literatura y lo que intento aportar | 25 | rápido | Mismo modelo con y sin historial, sobre las mismas ventanas |
| 9 | Sigo KDD, adaptado en cinco etapas | 10 | rápido | El proceso es iterativo: volví atrás por la etiqueta |
| 10 | Qué hago con cada señal | 25 | rápido | El EEG se usa por canal; la pupila no está corregida por brillo, porque no hay datos de luminancia |
| 11 | Cómo comparo un modelo con y sin historial | 45 | clave | Configuración congelada y diferencia pareada por persona; el placebo se registró antes y la posición es post hoc |
| 12 | Dos formas de armar la etiqueta de atención coinciden solo en dos tercios de las ventanas | 25 | rápido | Seguí con PCA porque se predecía mejor, y eso no la valida; cuál queda es una decisión abierta |
| 13 | Con la etiqueta antigua, tres personas tenían datos anómalos | 15 | rápido | Tres personas con datos anómalos me hicieron revisar la etiqueta |
| 14 | El generador mezclaba las ventanas | 30 | clave | El 98 % de los valores GSR quedó en otra ventana; lo anterior de activación no sirve |
| 15 | “Alta” es estar sobre su propia mediana de activación: así se ve en P22 | 20 | rápido | La etiqueta es relativa a cada persona |
| 16 | La etiqueta antigua y la nueva coinciden solo en la mitad de las ventanas | 15 | rápido | La etiqueta antigua no tenía relación con la corregida |
| 17 | La etiqueta nueva (V2) deja 11.796 de 22.211 ventanas | 20 | normal | Se pierde casi la mitad, por exigir continuidad y no por mala señal |
| 18 | Primer análisis con 41 personas (16-11): mejora en atención; en activación, inconcluso | 70 | clave | Con historial atención mejora; activación queda inconclusa el 16-11 y pasa a +0,036 al repetir el 22-11 |
| 19 | En atención, la fusión tardía rinde mejor entre redes MLP; con HGB, no | 25 | rápido | Es un secundario entre redes MLP (+0,012); con HGB el signo fue el contrario |
| 20 | El modelo de atención rinde mejor al final de la sesión y peor en textos | 25 | rápido | Es descriptivo |
| 21 | ¿De dónde viene la mejora? | 50 | clave | En atención el placebo rinde igual; en activación no, con un placebo que viene de otras páginas |
| 22 | En atención, la etiqueta depende de cuánto lleva la persona en la página | 45 | normal | Lo que parecía venir del historial es la posición dentro de la página |
| 23 | En activación, los segundos previos aportan frente al placebo | 65 | clave | El historial le gana al placebo sin las ventanas que promedia la etiqueta, con un modelo débil; el filtro de la GSR mira más lejos |
| 24 | Los parpadeos y los movimientos de los ojos se ven en el EEG | 45 | normal | El parpadeo se ve en la frente; hay un desfase de reloj sin corregir |
| 25 | Al quitar los componentes oculares, la detección de atención cae | 60 | clave | De 0,681 a 0,621: cerca de un tercio de lo que hay sobre el azar depende de componentes ligados a los ojos; lo leo como cota inferior |
| 26 | Una red sobre la señal cruda rinde más, y también depende de la huella ocular | 45 | normal | La red pierde 0,067 al limpiar, pero su ventaja sobre el modelo de referencia se mantiene (+0,028) |
| 27 | Por qué: el ojo genera señal eléctrica que llega a los electrodos | 35 | normal | Cerca de un tercio de lo que detecto depende de componentes ligados a lo Observado (cota inferior); no puedo afirmar que el resto sea lo Atendido |
| 28 | Por qué puede costar detectar la activación desde el EEG | 35 | normal | La etiqueta es un nivel lento de la GSR; 2 s de EEG no calzan con él |
| 29 | Qué responde la tesis | 60 | clave | Apoyo parcial, y viene de activación; en atención, cerca de un tercio depende de componentes ligados a los ojos |
| 30 | Conclusiones provisorias: apoyo parcial | 45 | normal | Efecto pequeño, desigual entre personas y con respaldo solo para los 6 s anteriores |
| 31 | Conclusiones: qué detecta el EEG | 40 | normal | Separar señales no asegura independencia fisiológica: no puedo afirmar que detecte lo Atendido |
| 32 | Qué falta para cerrar la tesis | 30 | normal | Faltan decisiones y escritura, no experimentos |
| 33 | Necesito decidir cinco cosas con usted | 75 | clave | ¿Escribo o planifico una cohorte nueva? Al pie van los dos puntos adicionales de la minuta |
| | **Total** | **1.200** | | |

Subtotales: láminas 1 a 6, 195 s; 7 a 11, 130 s; 12 a 17, 125 s; 18 a 23, 280 s; 24 a 28, 220 s; 29 a 33, 250 s.

Redistribución del 26-11-2026 respecto del plan anterior: la lámina 9 baja de 15 a 10 s y la 30 sube de 40 a 45; la 13 baja de 30 a 15 y la 17 de 30 a 20, y esos 25 s pasan a la 18 (de 55 a 70) y a la 23 (de 55 a 65); la 14 baja de 35 a 30 y la 16 de 20 a 15, y la 12 y la 20 suben de 20 a 25. El guion de la sección 2 está recortado a esos tiempos: ninguna lámina pasa de 150 palabras por minuto y el total queda bajo 2.800 palabras.

- **No se salta ninguna** de las 33 principales.
- **Se pasan rápido** (una frase y avanzar): 2, 7, 8, 9, 10, 12, 13, 15, 16, 19 y 20.
- **Si a los 10 minutos todavía no llego a la lámina 18**, salto 19 y 20 (50 s) y acorto 27 y 28 a una frase cada una.
- **Candidatas a pasar a anexos en una próxima versión**, si se quiere más aire: 9, 12, 15 y 20. No las moví; habría que cambiar `relato.py`.
- **Anexos (láminas 34 a 39):** no se muestran en la exposición. Se abren solo si preguntan. Los anexos A, B, D y E llevan al pie que son análisis anteriores al de 41 personas y se conservan como antecedente:

| Lámina | Anexo | Se abre si preguntan por |
|---|---|---|
| 34 | A. Atención: curvas ROC en test | El desempeño en las 8 personas de test |
| 35 | B. Activación: curvas ROC en test | Qué tan cerca del azar está activación |
| 36 | C. Señales | Qué variables se sacan de cada señal |
| 37 | D. Configuración del entrenamiento de activación | Hiperparámetros y búsqueda |
| 38 | E. Activación: la muestra necesaria va de 72 a 767 según la variabilidad | La cohorte nueva y el margen de 0,02 |
| 39 | F. Referencias de la explicación fisiológica | El sustento bibliográfico de las láminas 27 y 28. Su pie dice 10 en texto completo y 8 solo por resumen, y dos atribuciones sin comprobar (Boucsein, Critchley) |

### Versión corta de 10 minutos (600 s)

Se muestran 17 láminas y se saltan 16. Con las flechas hay que pasar por las saltadas sin detenerse, o usar el índice (tecla I).

| Lámina | Título | Segundos | Qué hago | La única idea que hay que dejar |
|---|---|---:|---|---|
| 1 | ¿Sirve el historial de señales para predecir atención y activación? | 20 | mostrar | Resultados nuevos y siete decisiones |
| 2 | De qué voy a hablar | 0 | saltar | |
| 3 | La hipótesis | 30 | mostrar | Mismo modelo con y sin historial |
| 4 | Los datos: Toma de Muestra 2, navegación web en laboratorio | 0 | saltar | Se dice en una frase en la lámina 5 |
| 5 | Unas señales arman la etiqueta y otras la predicen | 40 | mostrar | Modelo Profesor y Modelo Estudiante usan señales distintas |
| 6 | 48 personas registradas, 41 en el análisis | 25 | mostrar | La unidad es la persona; todas ya vistas |
| 7 | Qué señales combinan los trabajos recientes | 0 | saltar | |
| 8 | Lo que falta en la literatura y lo que intento aportar | 0 | saltar | |
| 9 | Sigo KDD, adaptado en cinco etapas | 0 | saltar | |
| 10 | Qué hago con cada señal | 0 | saltar | |
| 11 | Cómo comparo un modelo con y sin historial | 30 | mostrar | Configuración congelada y diferencia pareada por persona |
| 12 | Dos formas de armar la etiqueta de atención coinciden solo en dos tercios de las ventanas | 0 | saltar | |
| 13 | Con la etiqueta antigua, tres personas tenían datos anómalos | 0 | saltar | Se menciona en la lámina 14 |
| 14 | El generador mezclaba las ventanas | 30 | mostrar | Lo anterior de activación no sirve |
| 15 | “Alta” es estar sobre su propia mediana de activación: así se ve en P22 | 0 | saltar | |
| 16 | La etiqueta antigua y la nueva coinciden solo en la mitad de las ventanas | 0 | saltar | Se menciona en la lámina 14 |
| 17 | La etiqueta nueva (V2) deja 11.796 de 22.211 ventanas | 20 | mostrar | Quedan 11.796 de 22.211 ventanas |
| 18 | Primer análisis con 41 personas (16-11): mejora en atención; en activación, inconcluso | 40 | mostrar | Atención mejora; activación pasa de inconclusa a +0,036 al repetir |
| 19 | En atención, la fusión tardía rinde mejor entre redes MLP; con HGB, no | 0 | saltar | |
| 20 | El modelo de atención rinde mejor al final de la sesión y peor en textos | 0 | saltar | |
| 21 | ¿De dónde viene la mejora? | 45 | mostrar | En atención el placebo rinde igual; en activación no |
| 22 | En atención, la etiqueta depende de cuánto lleva la persona en la página | 30 | mostrar | En atención la mejora no viene de las ventanas previas |
| 23 | En activación, los segundos previos aportan frente al placebo | 40 | mostrar | Le gana al placebo, con un modelo débil |
| 24 | Los parpadeos y los movimientos de los ojos se ven en el EEG | 15 | pasar rápido | El parpadeo se ve en la frente |
| 25 | Al quitar los componentes oculares, la detección de atención cae | 55 | mostrar | De 0,681 a 0,621: cerca de un tercio depende de componentes ligados a los ojos; lo leo como cota inferior |
| 26 | Una red sobre la señal cruda rinde más, y también depende de la huella ocular | 30 | mostrar | Pierde 0,067 al limpiar; su ventaja se mantiene (+0,028) |
| 27 | Por qué: el ojo genera señal eléctrica que llega a los electrodos | 0 | saltar | Se dice en una frase en la lámina 25 |
| 28 | Por qué puede costar detectar la activación desde el EEG | 0 | saltar | |
| 29 | Qué responde la tesis | 60 | mostrar | Apoyo parcial, y viene de activación; en atención, cerca de un tercio depende de componentes ligados a los ojos |
| 30 | Conclusiones provisorias: apoyo parcial | 0 | saltar | Cubierta por la lámina 29 |
| 31 | Conclusiones: qué detecta el EEG | 0 | saltar | Cubierta por la lámina 29 |
| 32 | Qué falta para cerrar la tesis | 20 | pasar rápido | Faltan decisiones, no experimentos |
| 33 | Necesito decidir cinco cosas con usted | 70 | mostrar | ¿Escribo o planifico una cohorte nueva? |
| | **Total** | **600** | | |

Subtotales: láminas 1 a 11, 145 s; 14 y 17, 50 s; 18 y 21 a 23, 155 s; 24 a 26, 100 s; 29 a 33, 150 s.

- **Se saltan:** 2, 4, 7, 8, 9, 10, 12, 13, 15, 16, 19, 20, 27, 28, 30 y 31.
- **Se pasan rápido:** 24 y 32.
- **Anexos:** igual que en la versión larga, solo a pedido.
- Entre la lámina 18 y la 21 hay que pasar por la 19 y la 20 sin detenerse; la frase de puente es: "Falta saber de dónde viene esa mejora".
- En la versión corta, la frase de la lámina 14 es: "Tres personas con datos anómalos me hicieron revisar la etiqueta de activación; encontré que el generador mezclaba las ventanas y que la etiqueta antigua coincidía con la corregida solo en la mitad de los casos".
- En la versión corta, la lámina 33 se acorta leyendo solo el enunciado de cada pregunta y deteniéndose en la primera; los puntos sexto y séptimo (normalización y Modelo Profesor con PCA) quedan en el pie de la lámina y se dejan para las preguntas.

---

## 2. Guion hablado, versión de 20 minutos

**Lámina 1 · Portada (25 s).** Profesor, desde la última reunión corregí un error en la etiqueta de activación y repetí todo con 41 personas. El historial ayuda a predecir activación, con un efecto pequeño. En atención la mejora no viene de las ventanas previas, y cerca de un tercio de la detección por EEG depende de componentes ligados a los ojos. Al final traigo siete decisiones.

**Lámina 2 · De qué voy a hablar (10 s).** Son nueve partes. Voy rápido por las primeras: lo nuevo va desde los resultados con 41 personas.

**Lámina 3 · La hipótesis (40 s).** Esta es la hipótesis tal como está en el manuscrito: que los modelos temporales multimodales rinden mejor fuera de muestra que los estáticos comparables. Para probarla comparo siempre el mismo modelo, con la misma etiqueta, y lo único que cambio es si ve las ventanas anteriores, hasta 32; más adelante se ve que con eso el modelo también se entera de cuánto lleva la persona en la página. La hipótesis dice emociones, pero con GSR lo que mido es activación; esa es una de las preguntas del final.

**Lámina 4 · Los datos (35 s).** Los datos son de la Toma de Muestra 2 del Fondecyt, en laboratorio, de agosto de 2025. El Tobii registra mirada, pupila y GSR en un mismo archivo; el EEG viene aparte, de un OpenBCI de 16 canales a 125 Hz. Los sincronicé por persona y hora, y corté todo en ventanas de 2 segundos que avanzan de a 1. Este conjunto de datos no tiene expresión facial, y la ubicación de los electrodos no está documentada.

**Lámina 5 · Unas señales arman la etiqueta y otras la predicen (50 s).** No tengo una etiqueta directa, así que la construyo. El Modelo Profesor arma la etiqueta con unas señales y el Modelo Estudiante la predice con otras. En atención, el Attention Score sale de la mirada y la pupila, y lo predigo con EEG y GSR. En activación, el Arousal Score sale de la GSR, y lo predigo con EEG, mirada y pupila. "Alta" significa sobre la mediana de esa persona en su sesión completa, así que esto no sirve tal cual en línea. Dos precisiones: en el Attention Score la pupila casi no pesa, así que en la práctica es conducta de mirada; y el Arousal Score es, en lo esencial, el nivel tónico de la GSR.

**Lámina 6 · 48 personas, 41 en el análisis (35 s).** Se registraron 48 personas y quedan 41 en el análisis: 25 de entrenamiento, 8 de validación y 8 de test. Salen cuatro por EEG no utilizable y dos sin GSR, y P29 queda aparte, para sensibilidad, por un desfase de sincronización. Como las ventanas se solapan, la unidad es la persona: calculo la AUC por persona y después promedio. Validación y test ya los había mirado, así que todo es exploratorio.

**Lámina 7 · Qué señales combinan los trabajos recientes (25 s).** La tendencia es fusionar varias señales con modelos tipo Transformer. Lo más cercano en contexto web es la tesis de Saavedra, del mismo grupo, con EEG y GSR, que no encontró mejora clara con fusión tardía. Ninguno de los que revisé combina estas cuatro señales navegando la web; esa búsqueda la tengo que repetir antes de afirmarlo.

**Lámina 8 · Lo que falta y lo que intento aportar (25 s).** De la revisión salen tres brechas, y cada una tiene su respuesta en el diseño. La principal: comparo el mismo modelo con y sin historial sobre las mismas ventanas. La comparación entre fusión temprana, intermedia y tardía la muestro en resultados.

**Lámina 9 · KDD (10 s).** Uso KDD como marco, en cinco etapas. Es iterativo: por el error en la etiqueta volví de la evaluación a la transformación.

**Lámina 10 · Qué hago con cada señal (25 s).** El EEG lo filtro entre 1 y 45 Hz, con notch en 50, descarto los canales no utilizables y lo trabajo por canal: 342 variables por ventana. La GSR la separo en parte tónica y fásica. La pupila no está corregida por el brillo de cada página, porque no hay datos de luminancia; va en las limitaciones.

**Lámina 11 · Cómo comparo (45 s).** Elijo la configuración solo con las 25 personas de entrenamiento y la congelo. Después la evalúo con las 41 personas en validación cruzada por persona, igual con y sin historial. Ojo: esas 25 son parte de las 41 que evalúo, y en activación la elección la decidió el modelo con historial; lo detallo en la lámina 18. Miro la diferencia pareada dentro de cada persona, con intervalo bootstrap remuestreando personas. Cada protocolo entró al repositorio antes que sus predicciones, el placebo incluido; el de posición también, pero después de ver el placebo, así que es post hoc. Es mi propio repositorio: no es un prerregistro.

**Lámina 12 · Dos formas de armar la etiqueta de atención (25 s).** Probé dos formas de armar la etiqueta de atención: pesos iguales y PCA. Los análisis siguieron con PCA, que es la que los modelos predicen mejor; eso no la valida. Las dos coinciden solo en dos tercios de las ventanas, y cuál queda como definición es una decisión que le traigo.

**Lámina 13 · Tres personas con datos anómalos (15 s).** Esto me hizo dudar de activación. P4 casi no tenía señal de GSR y aun así tenía etiqueta en todas sus ventanas; P34 y P46 tenían muchos puntajes repetidos. Ahí revisé la etiqueta.

**Lámina 14 · El generador mezclaba las ventanas (30 s).** El problema estaba en el código que generaba la etiqueta: al agrupar por persona, cada valor de GSR perdía su ventana. El 98 % de los valores del archivo quedó en una ventana que no era la suya. Repitiendo el cálculo con el error reproduzco los puntajes que tenía guardados, así que las AUC de activación anteriores no sirven.

**Lámina 15 · Ejemplo en P22 (20 s).** Así se ve la etiqueta corregida en un tramo real de P22. La línea es el puntaje de GSR de seis segundos y la punteada, su mediana en toda la sesión; los puntos azules son "alta". La etiqueta dice si P22 está más activada que de costumbre.

**Lámina 16 · Antigua y nueva coinciden en la mitad (15 s).** Comparé la etiqueta antigua con la nueva en las mismas ventanas, y cambia casi la mitad. Con clases balanceadas, eso es lo que esperaría si no tuvieran relación.

**Lámina 17 · La etiqueta nueva, V2 (20 s).** Rehíce la etiqueta en cuatro pasos y quedan 11.796 de 22.211 ventanas. Lo que más saca es exigir cinco ventanas válidas seguidas dentro del mismo estímulo. Por calidad se van 401, todas de P4. Las 41 personas conservan las dos clases.

**Lámina 18 · Primer análisis con 41 personas, 16-11 (70 s).** Con las particiones originales, el cierre V3 no mostró una ventaja consistente en ninguna de las dos tareas. Después de ver eso, y para tener más potencia, usé las 41 personas en validación cruzada, con la configuración congelada y sin búsqueda: es un cambio de diseño posterior a los datos. Y las 15 hojas del modelo de activación las elegí con las 25 personas de entrenamiento, donde la elección la decidió el modelo con historial; el efecto de activación se concentra en esas 25. Ese sesgo es posible, no está demostrado. En atención el historial mejora +0,026, en 36 de 41 personas, y se repite con otras tres particiones. En activación da +0,034, pero el intervalo de la partición registrada toca el cero: inconcluso. Al repetirlo el 22 de noviembre con cinco particiones quedó en +0,036, con intervalo entre +0,010 y +0,065; esas cifras uso en las conclusiones. Es una estimación más precisa de lo ya visto, no una confirmación. Falta saber de dónde viene la mejora; antes, dos resultados rápidos.

**Lámina 19 · Fusión (25 s).** Entre redes MLP, en atención la fusión tardía le gana a la temprana por +0,012, y también a la intermedia, que es más profunda. En activación no se demostraron diferencias. Es un resultado secundario y vale solo para esta familia: con HGB, en el cierre V3, el signo fue el contrario. No concluyo que una fusión sea mejor.

**Lámina 20 · Sesión y tipo de página (25 s).** En atención el modelo rinde mejor hacia el final de la sesión, mejor en sitios web y peor en textos. En activación, la proporción de ventanas altas baja al final, compatible con habituación y también con una deriva lenta de la señal o con el orden de las páginas. Todo esto es descriptivo.

**Lámina 21 · ¿De dónde viene la mejora? (50 s).** Vuelvo a la mejora con historial. La comparé con dos controles. Uno es un placebo: la misma cantidad de ventanas, de la misma persona, pero de otras páginas. El otro es una sola variable: cuántos segundos lleva la persona en la página. En atención, el placebo y los segundos solos dan lo mismo que el historial real. En activación, al comparar entre todas las ventanas, pasa lo contrario: el placebo y los segundos no aportan, y el historial sí. Ojo: el placebo viene de otras páginas, y dentro de una misma página los segundos sí aportan y no demostré que el historial los supere. Hasta la lámina 18 parecía que la hipótesis se apoyaba en atención; esto lo da vuelta.

**Lámina 22 · La etiqueta depende de la posición en la página (45 s).** Al entrar a una página, la proporción de ventanas con atención alta cae a 37 % entre el segundo 2 y 3 y después sube hasta 62 %. El modelo con historial aprendía eso a través del largo del historial, no del contenido. Lo más probable es que refleje cómo se arma el Attention Score con fijaciones y mirada al cambiar de página; no separé cuánto es conducta y cuánto es el cálculo de las fijaciones. Este análisis lo hice después de ver el placebo, así que es explicativo y no confirmatorio.

**Lámina 23 · En activación, los segundos previos aportan frente al placebo (65 s).** Aquí saqué del historial las ventanas de 6 segundos que promedia la etiqueta. Ojo: el filtro tónico de la GSR usa toda la sesión, y cerca de un cuarto del peso de la etiqueta cae antes de esas ventanas, así que no puedo decir que no haya solapamiento. Aun así le gana al placebo por +0,046, en 28 de 41 personas, con p de Holm 0,004; es positivo en las 25 personas con que elegí la configuración y en las otras 16. Es el contraste mejor sostenido que tengo, con dos reservas: lo fijé después de ver que el historial completo le ganaba al placebo, y el placebo viene de otras páginas. Frente a un modelo que conoce los segundos en la página, el historial sumaba +0,038 el 18 de noviembre, post hoc; el 22, con cinco particiones, da +0,032 y queda inconcluso tras Holm. Y el modelo sigue siendo débil: la AUC queda entre 0,55 y 0,58.

**Lámina 24 · Los parpadeos y los ojos se ven en el EEG (45 s).** La etiqueta de atención se arma con la mirada y la predigo con EEG, así que revisé cuánto de los ojos se cuela en el EEG. El parpadeo llega a unos 150 microvoltios en los dos canales de la frente y baja a unos 20 atrás. Ese patrón, además, es compatible con el montaje por defecto del equipo, que no estaba documentado. Y encontré que el EEG va entre 0,18 y 0,53 segundos atrasado respecto del seguidor ocular; eso no lo corregí.

**Lámina 25 · Al quitar los componentes oculares, la detección cae (60 s).** Este es el resultado más importante de la semana. Por persona separé el EEG en componentes independientes y quité los tres más ligados a la mirada y a los parpadeos, que son el 3,5 % de la varianza. La AUC de atención baja de 0,681 a 0,621, en 39 de 41 personas. Como control quité tres componentes no oculares, con veinte veces más varianza, y casi no cambia. Alfa y beta, que parecía lo más limpio, también cae, de 0,593 a 0,547. Esa caída de 0,06 es cerca de un tercio de lo que el modelo tiene sobre el azar; como la limpieza es parcial la leo como cota inferior, y no es una demostración, porque elijo los componentes con la mirada, que también define la etiqueta. El modelo limpio sigue sobre el azar en las 41 personas; no puedo descartar que ese resto también dependa de los ojos.

**Lámina 26 · Red sobre la señal cruda (45 s).** Probé un modelo más complejo: una red convolucional tipo EEGNet sobre la señal cruda. En atención le gana al modelo de referencia, 0,716 contra 0,681, o sea +0,035. Pero al quitar los componentes oculares cae a 0,649, pierde 0,067: su detección también depende de la huella ocular. Su ventaja sobre el modelo de referencia, en cambio, se mantiene con el EEG limpio: +0,028. En activación queda en el azar, 0,498 frente a 0,524, inconcluso. Es una sola arquitectura, sin búsqueda ni red con filtro de control, y no puedo separar si la ventaja viene de la arquitectura o de la escala por persona.

> Ojo: no decir que "la ventaja de la red es ocular". Lo que depende de lo ocular es su detección (pierde 0,067 al limpiar); la ventaja sobre el HGB casi no cambia (+0,035 con el EEG original, +0,028 con el limpio). Si mencionas el margen de 0,02, que sea como en la nota de la lámina: "una propuesta mía sin aprobar".

**Lámina 27 · Por qué: el ojo (35 s).** La explicación es fisiológica. El ojo es un dipolo, y cada movimiento cambia el potencial en los electrodos. Como la etiqueta se define con los ojos, todo lo que los ojos dejan en el EEG la predice. Cumplí la regla de no usar las mismas señales, pero eso no asegura independencia fisiológica. Cerca de un tercio de lo que detecto depende de componentes ligados a lo Observado; lo leo como cota inferior, no es una demostración, y no puedo afirmar que el resto sea lo Atendido.

**Lámina 28 · Por qué puede costar detectar la activación (35 s).** La etiqueta de activación viene de la GSR, que mide glándulas sudoríparas bajo control simpático. Es una señal lenta, y mi etiqueta es en lo esencial su nivel tónico, más lento aún que las respuestas. Es posible que además dependa de regiones profundas que el EEG de superficie ve poco; eso no lo pude confirmar en la fuente. Dos segundos de EEG no calzan con un nivel tan lento, y con 16 canales la AUC queda en 0,52. Es interpretación mía.

**Lámina 29 · Qué responde la tesis (60 s).** Esta tabla es el resumen. Con historial las dos tareas mejoran: +0,029 en atención y +0,036 en activación. En atención no viene de las ventanas previas: si el modelo conoce la posición en la página, el historial agrega +0,001. En activación sí viene en parte del historial: +0,046 sobre el placebo en el contraste registrado, y solo hay respaldo para los 6 segundos previos. El modelo con orden, la GRU, no agrega en atención, y la fusión tardía solo gana en atención y con MLP. Y la última fila es lo nuevo: en atención, cerca de un tercio de lo que el EEG tiene sobre el azar depende de componentes ligados a los ojos, como cota inferior, y no puedo descartar que el resto también. Todo esto con personas que ya había consultado: confirmarlo requiere personas nuevas.

> Ojo con las dos cifras: las láminas 23, 29 y 30 usan el +0,046, que es el contraste registrado el 16-11, después de ver que el historial completo le ganaba al placebo. El +0,047, que ya no está en pantalla (queda en la nota de la lámina 30), sale de la curva temporal del 22-11, calculada en una sola partición (la registrada el 16-11) y con 40 personas; no es una repetición con cinco particiones del +0,046. Con cinco particiones se estimaron el +0,029, el +0,036 y el +0,001.

**Lámina 30 · Conclusiones provisorias: apoyo parcial (45 s).** Son las conclusiones del capítulo 9, con un encuadre provisorio. La hipótesis tendría apoyo parcial, y viene solo de activación; lo que tiene apoyo es un resumen del historial reciente, no un modelo secuencial ni la combinación de señales. El efecto se sostiene frente a un placebo de otras páginas, pero es pequeño, desigual entre personas —mejoran 23 de 41, y se concentra en las 25 con que elegí la configuración— y solo tiene respaldo para los 6 segundos anteriores. Al controlar la posición conserva su tamaño, +0,032, pero queda inconcluso. En atención, lo que parecía temporal era la posición en la página. Y el orden de las ventanas no mostró aporte.

**Lámina 31 · Conclusiones: qué detecta el EEG (40 s).** En atención, cerca de un tercio de la detección por EEG depende de componentes ligados a los ojos, como cota inferior. Una red más compleja no cambia qué se detecta: llega a 0,716 pero pierde 0,067 al limpiar. La más importante es la tercera: separar las señales no asegura independencia fisiológica. La etiqueta se define con lo Observado y el EEG registra esa misma conducta, así que no puedo afirmar que detecte lo Atendido. El aporte sería doble: evidencia acotada sobre el historial en activación y una advertencia sobre etiquetas oculares. Todo supone, provisoriamente, las decisiones de la última lámina.

**Lámina 32 · Qué falta para cerrar la tesis (30 s).** Mi propuesta es cerrar la experimentación aquí: no espero que más corridas sobre estas 41 personas cambien las conclusiones. Faltan decisiones y escritura: revisar el borrador integrado del 23 de noviembre y ajustar las conclusiones según lo que decidamos. El 22 probé una etiqueta de atención corregida por la posición, y hay que decidir si reemplaza a la original. De los opcionales, solo una cohorte nueva cambiaría el estatus de los resultados.

**Lámina 33 · Cinco decisiones (75 s).** La experimentación sobre estas 41 personas la doy por cerrada, salvo que usted indique otra cosa, y traigo las decisiones abiertas. Primero, si escribo con estos resultados o planifico una cohorte para confirmar activación; es la que más me urge. Segundo, qué cuenta como "mejor": cualquier mejora sobre cero, como dice la hipótesis, o un mínimo como +0,02. Tercero, si escribo "activación (GSR)" en vez de "emociones". Cuarto, si uso la etiqueta de atención original o la corregida por posición, con la que la detección baja poco: 0,675 frente a 0,683. Quinto, si encuadro la tesis como apoyo parcial más una advertencia metodológica. Al pie van dos puntos más, que pueden pesar más, porque rechazarlos obliga a repetir análisis: las etiquetas se normalizan con la sesión completa y el manuscrito pide solo entrenamiento; y los análisis usan el Modelo Profesor con PCA, cuando la nota de diseño proponía la fusión igualitaria. El detalle está en la minuta, que además lista objetivos y contribuciones por revisar, la información de participantes y ética que debo pedir al proyecto, y cómo declarar el uso de asistentes automáticos en las revisiones.

> Ojo con la cuarta: la corregida da 0,504 al predecirla con la posición, y la decisión registrada para esa prueba fue "inferior", al filo: la diferencia es −0,008 [−0,015; −0,001], con p de Holm 0,055.

---

## 3. Preguntas difíciles y respuestas

Las rutas son relativas a `repos/Tesis_MDS/` salvo que se indique otra cosa. Las respuestas de más de 100 palabras llevan delante una línea `Corta:` (a lo más 70 palabras, unos 30 segundos), hecha solo con frases y cifras de la respuesta completa; eso es lo que se dice primero. Lo que sigue a `Si repreguntan:` es la respuesta completa. Las preguntas que comparten contenido no se fusionaron, para no perder matices: se remiten entre sí (4, 21 y 32; 5, 24 y 37; 1 y 11; 7 y 25; 2, 4 y 16; 15 y 41; 19 y 44). Las preguntas 38 a 49 se agregaron el 27-11-2026; sus respuestas tienen a lo más 70 palabras y no llevan línea `Corta:`. En las respuestas corregidas ese día, un segundo `Si repreguntan` trae entre paréntesis la repregunta que la segunda lectura anticipa.

**1. ¿La detección de atención por EEG no es circular, si la etiqueta sale de los ojos?**
Corta: En el sentido fisiológico, en parte sí. Cumplo la regla de no usar la misma señal, pero el EEG registra la huella eléctrica de los ojos. Al quitar tres componentes oculares la AUC baja de 0,681 a 0,621; esa caída es cerca de un tercio de lo que el modelo tiene sobre el azar y la leo como cota inferior. No puedo afirmar que detecte lo Atendido.

Si repreguntan: En el sentido fisiológico, en parte sí. Cumplo la regla de no usar la misma señal para etiquetar y para predecir, pero el EEG registra la huella eléctrica de los ojos. Al quitar tres componentes oculares, que son el 3,5 % de la varianza, la AUC baja de 0,681 a 0,621 [diferencia 0,060; IC 0,044 a 0,075], y un control que quita componentes no oculares con el 72 % de la varianza la deja en 0,674. Esa caída es cerca de un tercio de lo que el modelo tiene sobre el azar (0,060 de 0,181) y la leo como cota inferior, porque la limpieza es parcial. El modelo limpio sigue sobre el azar en las 41 personas. Ese resto conserva el patrón del artefacto, así que no puedo descartar que también sea ocular, pero el diseño no lo separa: no puedo afirmar que sea cerebral ni que sea ocular. Por eso digo que no puedo afirmar que detecte lo Atendido. Por qué lo leo como cota inferior, y la objeción de que la caída era esperable, están en la pregunta 11.
Fuente: `resultados/limpieza_ocular_41p_23-11-2026/INFORME.md`.

**2. ¿Por qué el AUC de activación es tan bajo? ¿Sirve para algo?**
Corta: Con la ventana actual el modelo está en el azar: 0,518. Con historial sube a 0,554, y lo más alto que obtuve es 0,587. Para uso práctico no sirve, y así lo escribo en las limitaciones. Lo que tiene interés es el contraste pareado: el historial real mejora y un placebo de otras páginas no; qué demuestra eso tiene límites.

Si repreguntan: Con la ventana actual el modelo está en el azar: 0,518 con EEG, mirada y pupila, y 0,524 con solo EEG. Con historial sube a 0,554, y lo más alto que obtuve es 0,587. Para uso práctico no sirve, y así lo escribo en las limitaciones. Lo que tiene interés es el contraste pareado: el historial real mejora y un placebo de otras páginas no. Las razones probables son que la GSR es lenta, quizá con un origen que el EEG de superficie ve poco (eso no lo pude confirmar en la fuente), y que la etiqueta es relativa a la mediana de cada persona en un rango de activación estrecho; eso es compatible con los datos, pero no lo puse a prueba.

Si repreguntan (el placebo es de otras páginas; dentro de una misma página, ¿el historial supera al tiempo transcurrido?, ¿qué mide entonces el contraste?): No lo demostré. Dentro de un mismo estímulo los segundos en la página aportan por sí solos +0,049 [+0,027; +0,072], y el historial sobre ellos, +0,005 [−0,025; +0,035]. El placebo iguala la persona y el largo del historial, no la página ni la cercanía en la sesión. El contraste mide entonces tres cosas juntas: la fisiología de los segundos previos, estar en la misma página y estar en el mismo tramo de la sesión. No las separé. El contraste que lo haría, historial desplazado menos placebo dentro de un mismo estímulo, no está calculado y sería un análisis nuevo.
Fuentes: `resultados/reapertura_41p_22-11-2026/INFORME.md`; `resultados/red_cruda_41p_23-11-2026/INFORME.md`; `resultados/enfoques_41p_22-11-2026/INFORME.md`; `resultados/reapertura_fase3_41p_22-11-2026/descriptivos.csv`; `scripts/cierre_robustez_41p.py` y `scripts/ampliacion_41p.py` (de dónde salen las ventanas del placebo).

**3. ¿Por qué dice que la mejora de atención no es temporal? ¿La posición no es tiempo?**
Corta: La posición es tiempo transcurrido, así que lo preciso es decir que la mejora no viene de la fisiología de las ventanas previas. Un historial placebo da la misma mejora, los segundos en la página la reproducen (+0,028) y, si el modelo conoce la posición, el historial agrega +0,001. El límite: el análisis de posición del 18-11 es post hoc.

Si repreguntan: La posición es tiempo transcurrido, así que lo preciso es decir que la mejora no viene de la fisiología de las ventanas previas. Lo digo por tres resultados que apuntan a lo mismo (láminas 21 y 22). Un historial placebo, con ventanas de la misma persona en otras páginas, da la misma mejora: la diferencia es −0,000 [−0,003; +0,003]. Los segundos en la página, como única variable, reproducen la mejora: +0,028 [+0,021; +0,035]. Y si el modelo conoce la posición, el historial agrega +0,001 [−0,002; +0,005]. El límite: el análisis de posición del 18-11 es post hoc, y como los segmentos son cortos el nulo vale en la práctica para historiales de 2 a 10 ventanas, no para historiales largos.
Fuentes: `resultados/cierre_robustez_41p_16-11-2026/INFORME.md`; `resultados/explicativo_posicion_41p_18-11-2026/INFORME.md`; `resultados/reapertura_fase3_41p_22-11-2026/INFORME.md`.

**4. Reabrió el análisis y corrió muchas pruebas. ¿Cómo sé que no hubo p-hacking?**
Corta: No lo puedo descartar, y por eso no presento nada como confirmatorio. Cada protocolo entró a Git antes que sus predicciones y cada etapa se ejecutó una vez, con Holm dentro de su familia. Pero son doce etapas sobre las mismas 41 personas, varias dirigidas por resultados ya vistos, y Holm no corrige entre etapas. La única salida limpia es una cohorte nueva con el contraste fijado de antemano.

Si repreguntan: No lo puedo descartar del todo, y por eso no presento nada como confirmatorio. Lo que hice para acotarlo: el protocolo de cada etapa entró a Git antes que sus predicciones, cada una se ejecutó una vez y usa Holm dentro de su familia; desde el 22-11 cada una tuvo una revisión de código y un recálculo con código separado, hechos con un asistente automático a pedido mío, y la auditoría final del 23-11 recalculó las doce; de 289 archivos con hash, 288 coinciden y la diferencia está documentada. Pero son doce etapas sobre las mismas 41 personas, y reabrí el 22-11 después de ver un resultado inconcluso en activación (+0,034 [−0,001; +0,069]), que con cinco particiones pasó a +0,036 [+0,010; +0,065]. Ese contraste se estimó nueve veces sobre las mismas personas y 3 de los 9 intervalos incluyen el cero: es una estimación más precisa de lo ya visto, no una confirmación. Holm corrige dentro de cada etapa y no entre etapas, los contrastes secundarios no llevan corrección, y tres decisiones quedaron pegadas al umbral (p de Holm 0,055, 0,055 y 0,049). La única salida limpia es una cohorte nueva con el contraste fijado de antemano. El detalle de las nueve estimaciones está en la pregunta 21, y qué garantiza el registro en mi repositorio, en la 32.

Si repreguntan (el contraste contra placebo se registró después de ver que el historial le ganaba al placebo: ¿en qué se diferencia del control de posición, que llamo post hoc?): En el criterio, en nada. El 16-11 el commit de resultados de la robustez, con el +0,038 del historial completo frente al placebo, es de las 13:25; registré la ampliación a las 14:21 y su enmienda a las 14:25, cerca de una hora después, con las mismas personas y la misma partición. Lo único distinto es que su protocolo quedó fijado antes de sus predicciones. Es un refinamiento dirigido de un resultado ya visto, no una segunda evidencia, y así lo rotula ahora el borrador (sección 6.6).
Fuentes: `documentacion/Cierre_Experimental_Final_23-11-2026.md`; `git log` del 16-11 (commits `550f924`, `d2d5530` y `8beb675`); `resultados/reapertura_41p_22-11-2026/INFORME.md`; `resultados/enfoques_41p_22-11-2026/INFORME.md`.

**5. ¿Por qué 41 personas? ¿Las de test ya se habían visto?**
Corta: El 41 no viene de un cálculo de potencia: es lo que había disponible. Y sí, las 16 de validación y test ya se habían consultado; la configuración se eligió solo con las 25 de entrenamiento, pero eso no las vuelve nuevas. Además, el efecto de activación aparecía en las 25 de entrenamiento (+0,055) y no en las otras 16 (+0,001). Por eso todo va como exploratorio.

Si repreguntan: Hay 48 registradas; salen 4 por EEG no utilizable, 2 sin GSR y P29 queda para sensibilidad. El 41 no viene de un cálculo de potencia: es lo que había disponible. Y sí, las 16 de validación y test ya se habían consultado; la configuración se eligió solo con las 25 de entrenamiento, pero eso no las vuelve nuevas. Además, en el análisis del 16-11 el efecto de activación aparecía en las 25 de entrenamiento (+0,055 [+0,012; +0,101]) y no en las otras 16 (+0,001 [−0,052; +0,055]); en el cierre V3, con las particiones originales, había sido al revés (+0,016 en entrenamiento; +0,059 y +0,033 en validación y test). No sé por qué, pero hay una explicación posible en cómo elegí la configuración (pregunta 37; el cambio de diseño tras el cierre V3 está en la 24). Ninguna de las dos comparaciones estaba registrada, y la auditoría no reprodujo de forma exacta los intervalos de la primera. Lo leo como inestabilidad del efecto, y es otra razón para pedir personas nuevas. Por eso todo va como exploratorio.
Fuentes: `resultados/modelado/particion_participantes.csv`; `resultados/cierre_final_41p_16-11-2026/INFORME.md`.

**6. ¿De dónde sale el margen de 0,02?**
Corta: Es una propuesta mía, sin justificación independiente; no está aprobado, y la hipótesis dice "mejor", o sea mayor que cero. Varias lecturas dependen de él, pero no el nulo del historial en atención: con la posición como variable el historial agrega +0,001 [−0,002; +0,005], dentro de cualquier margen de 0,005 o más. Es la segunda decisión de la lámina 33.

Si repreguntan: Es una propuesta mía, sin justificación sustantiva independiente todavía; así quedó escrito en el protocolo del 06-11. No está aprobado ni se deduce de los resultados, y la hipótesis del manuscrito dice "mejor", o sea mayor que cero. Importa porque varias lecturas dependen de él: en atención el límite inferior fue 0,018 el 16-11 y 0,021 el 22-11, justo a cada lado del margen, y la ventaja de la red lo supera con un límite inferior de 0,023. Es la segunda de las cinco decisiones de la lámina 33; sin margen, las reglas vuelven a ser contra cero.

Si repreguntan (¿con qué margen dejaría de ser nulo el resultado de atención?, ¿por qué usa el mismo margen contra 0,5?): Con ninguno de 0,005 o más: el intervalo de 95 % del contraste registrado es [−0,002; +0,005], frente a los 0,183 que el modelo sin historial tiene sobre el azar. Ese nulo no depende del margen. El margen se propuso para diferencias entre modelos; en las pruebas contra 0,5 el rótulo "efecto relevante" solo dice que el límite inferior de la AUC supera 0,52 y no califica la utilidad: la GSR sola queda en 0,545 y no agrega nada al EEG.
Fuentes: `resultados/protocolo_hipotesis_reintento_06-11-2026/INFORME.md`; `resultados/reapertura_fase3_41p_22-11-2026/confirmatorio.csv`.

**7. ¿Por qué usar GSR como etiqueta? ¿Y la latencia de la respuesta?**
Corta: Porque en este set no hay expresión facial ni autorreporte, y la GSR es la medida de activación simpática disponible. La latencia de 1 a 5 s vale para las respuestas fásicas, que pesan poco: mi etiqueta es en lo esencial el nivel tónico, más lento, y su soporte real es más largo que los seis segundos. Ese desfase no lo modelé.

Si repreguntan: Porque en este set no hay expresión facial ni autorreporte, y la GSR es la medida de activación simpática disponible. El Arousal Score combina cuatro componentes e integra seis segundos, exigiendo cinco ventanas válidas seguidas del mismo estímulo. La respuesta de conductancia empieza segundos después del evento (la lámina 28 dice 1 a 5 s), así que la etiqueta de un instante refleja algo que pasó antes; ese desfase no lo modelé. Y el filtro tónico de la GSR es bidireccional y usa toda la sesión, así que el soporte real de la etiqueta es más largo que los seis segundos (pregunta 25). El "1 a 5 s" lo sostiene Benedek y Kaernbach (2010); la latencia que atribuía a Boucsein no la pude comprobar.

Si repreguntan (la etiqueta es nivel tónico: ¿qué tiene que ver la latencia?): Poco, y lo corregí en el borrador. Dentro de cada persona el nivel tónico de la ventana ordena la etiqueta con AUC 0,911, y el número de respuestas, con 0,522. La latencia explica la parte fásica. Lo que importa para mi etiqueta es otra diferencia de escalas: una ventana de EEG de 2 s frente a un nivel filtrado a 0,05 Hz y relativo a la sesión.
Fuentes: `documentacion/auditoria_final_23-11-2026/ronda3/AUDITORIA_CODIGO.md` (H2); `resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md`; límites de `resultados/reapertura_41p_22-11-2026/INFORME.md`; `Escritura/Borrador Resultados y Discusión 23-11-2026.md` (vault), sección 8.5; `notas/sustento-fisiologico-23-11-2026.md` (verificación de referencias).

**8. ¿Por qué "activación" y no "emociones", si la hipótesis dice emociones?**
Porque la GSR mide activación simpática y no distingue valencia: no puedo separar una emoción agradable de una desagradable. Sin facial ni autorreporte, hablar de emociones en general sería afirmar más de lo que mido. Esto cambia la redacción de la hipótesis, y no lo doy por decidido: no consta su confirmación y es la tercera pregunta de la lámina 33. Si prefiere mantener "emociones", habría que declarar que la tesis cubre solo su dimensión de activación.
Fuentes: `CLAUDE.md` del vault (`documentos/01 Tesis MDS/`); `documentacion/Cierre_Experimental_Final_23-11-2026.md`.

**9. ¿Por qué la GRU rinde peor que un resumen estadístico?**
Corta: No sé con certeza por qué. En atención la GRU con historial queda 0,040 bajo el HGB. Es una configuración fija sin búsqueda de hiperparámetros, y los segmentos son cortos. No puedo concluir que los modelos secuenciales no sirvan; solo que esta GRU, con estos datos, no aprovechó el orden.

Si repreguntan: En atención la GRU con historial queda 0,040 bajo el HGB [−0,055; −0,027] y no mejora sobre su propia versión de una ventana: +0,008 [−0,004; +0,020]. No sé con certeza por qué. La GRU es una configuración fija sin búsqueda de hiperparámetros, y los segmentos son cortos: el historial de 32 se completa en menos del 2 % de las ventanas. Así que no puedo concluir que los modelos secuenciales no sirvan; solo que esta GRU, con estos datos, no aprovechó el orden. En activación la GRU sí mostró una señal (+0,051 [+0,021; +0,080]), pero es secundaria y mide el aporte del historial en la GRU, no el del orden; el contraste del orden (GRU frente a HGB, +0,020) es inconcluso.
Fuentes: `resultados/cierre_final_41p_16-11-2026/INFORME.md`; `resultados/cierre_v3_16-11-2026/INFORME.md`.

**10. ¿Qué pasa con el desfase de reloj entre el EEG y el seguidor ocular?**
Corta: El EEG va entre 0,18 y 0,53 segundos atrasado, con mediana 0,45, en las 41 personas. No lo corregí, porque las ventanas estaban congeladas y corregirlo obliga a recalcular todo. El efecto esperado es atenuar la relación entre el EEG y las etiquetas, pero no lo medí. Corregirlo es uno de los experimentos opcionales.

Si repreguntan: El EEG va entre 0,18 y 0,53 segundos atrasado, con mediana 0,45, en las 41 personas. Eso corre las ventanas de EEG entre un 9 % y un 26 % respecto de las de mirada, pupila y GSR. No lo corregí, porque las ventanas estaban congeladas y corregirlo obliga a recalcular todo. El efecto esperado es atenuar la relación entre el EEG y las etiquetas, pero no lo medí; y en algunas personas el acoplamiento es bajo y el desfase estimado es poco seguro. Hay dos grupos de desfase, uno cerca de 0,28 s (P2 a P21, P36 y P37) y otro cerca de 0,48 s, lo que sugiere una causa sistemática de adquisición; no la investigué. Lo encontré el 23-11, con las ventanas ya congeladas. Corregirlo es uno de los experimentos opcionales.
Fuente: `resultados/montaje_ocular_41p_23-11-2026/INFORME.md`.

**11. ¿Por qué dice que la limpieza ocular es una cota inferior? Eligió los componentes por su correlación con la mirada, que define la etiqueta: ¿no es esperable que la predicción caiga?**
Corta: En parte sí es esperable. El experimento mide cuánto depende la detección de los componentes más ligados a la mirada; no distingue artefacto de actividad cerebral acoplada a los ojos. El control muestra que no es un efecto de quitar varianza, pero no está igualado en su relación con la etiqueta. "Cota inferior" es mi lectura más defendible, porque la limpieza fue parcial; no es una demostración.

Si repreguntan: En parte sí es esperable. Lo que mide el experimento es cuánto depende la detección de los componentes más ligados a la mirada; no distingue artefacto de actividad cerebral acoplada a los movimientos de los ojos. El control muestra que no es un efecto de quitar varianza, pero no está igualado en su relación con la etiqueta. El número de componentes, tres, estaba fijado de antemano. Lo de cota inferior lo digo porque la limpieza fue parcial. La correlación máxima entre algún canal y los parpadeos baja de 0,28 a 0,08, sin anularse, y la predicción del modelo limpio sigue asociada al recorrido de la mirada (Spearman 0,28, antes 0,41). Lo que queda conserva el patrón de un artefacto: frontales sobre posteriores y potencia lenta sobre alfa y beta. Pero la objeción contraria también vale: con 11 a 16 canales, tres componentes son entre el 19 % y el 27 % de las dimensiones y arrastran actividad frontal no ocular. El control acota esa objeción y no la elimina, así que "cota inferior" es mi lectura más defendible, no una demostración. Las cifras de la caída y del control están en la pregunta 1.
Fuente: `resultados/limpieza_ocular_41p_23-11-2026/INFORME.md`.

**12. ¿Una red más grande o mejor ajustada cambiaría el resultado? La ventaja de la red, ¿es la arquitectura o la normalización por persona?**
Corta: No lo sé. Probé una sola arquitectura, sin búsqueda. Le ganó al modelo de referencia por +0,035, y al limpiar el EEG perdió 0,067: su detección depende de lo ocular. Su ventaja sobre el modelo de referencia se mantiene con el EEG limpio (+0,028), así que no puedo decir que la ventaja sea ocular. Tampoco puedo separar arquitectura de normalización por persona.

Si repreguntan: No lo sé, y no puedo descartarlo. Probé una sola arquitectura, de 1.217 parámetros, sin búsqueda ni curva de convergencia. En atención le ganó al modelo de referencia por +0,035 [+0,023; +0,047]. Al limpiar el EEG cayó de 0,716 a 0,649, o sea perdió 0,067, y su predicción sigue la mirada más que la del modelo de referencia (0,48 frente a 0,41): la detección de la red depende de lo ocular. Pero su ventaja sobre el modelo de referencia se mantiene con el EEG limpio (+0,028 frente a +0,035), así que no puedo decir que la ventaja sea ocular. Esa pérdida, además, no tiene control propio. Qué haría una red más grande no lo sé. En activación el 0,498 vale para esta red y no permite decir que el EEG crudo no tenga información. Tampoco entrené la red con el filtro de control. Y no puedo separar arquitectura de normalización: la red recibe la señal escalada por persona y canal con toda la sesión, y el modelo de referencia usa variables sin esa escala y con la configuración congelada; no entrené un modelo de referencia con variables escaladas por persona.
Fuente: `resultados/red_cruda_41p_23-11-2026/INFORME.md`.

**13. Entonces, ¿qué aporta la tesis?**
Corta: Dos cosas, y ninguna es un detector utilizable. Una es evidencia acotada de que un resumen del historial reciente ayuda a predecir la activación: le gana a un placebo por +0,046, con límites. La otra es metodológica y es la más sólida: una mejora que parecía temporal era la posición en la página, y cerca de un tercio de una detección depende de componentes ligados a la conducta ocular.

Si repreguntan: Dos cosas, y ninguna es un detector utilizable. Una es evidencia acotada de que un resumen del historial reciente ayuda a predecir la activación: sin las ventanas de 6 s que promedia la etiqueta le gana a un placebo por +0,046 [+0,018; +0,073] en el contraste registrado el 16-11, que fijé después de ver el placebo del historial completo, y un análisis distinto del 22-11, la curva temporal, da +0,047 [+0,017; +0,078] para la banda de 6 s (una partición, 40 personas). Solo hay respaldo para los 6 s anteriores, y el efecto es pequeño; el contraste simple, con y sin historial, es además desigual entre personas. La otra es metodológica: muestro que una mejora que parecía temporal era la posición en la página, y que cerca de un tercio de una detección que parecía cerebral depende de componentes del EEG ligados a la conducta ocular. A eso se suma haber encontrado y corregido el error de alineación en la etiqueta de GSR. El aporte más sólido es el metodológico; si ese encuadre es suficiente para la tesis es justamente lo que necesito conversar.

Si repreguntan (que los ojos contaminan el EEG se sabe hace décadas, y cito a Croft y Barry, 2000: ¿qué agrega la tesis?): El hecho no es nuevo. Lo que agrego es una medida de su tamaño en un diseño de Modelo Profesor y Modelo Estudiante con etiqueta ocular: cerca de un tercio de lo que el modelo tiene sobre el azar, como cota inferior. Y el caso de la posición: una ventaja de un modelo con historial, estable y en 36 de 41 personas, que reproduce un solo número y que solo se ve con un placebo y con la posición como control.
Fuentes: `Escritura/Borrador Conclusiones 23-11-2026.md` (vault), sección 9.7; `resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md`.

**14. Si tuviera una cohorte nueva, ¿qué haría?**
Corta: Una sola cosa, definida antes de reclutar: un contraste, un tamaño de muestra y una única evaluación, registrados de antemano, para confirmar el efecto de activación. Dos cosas no están resueltas: qué modelo se evalúa, porque en el análisis con 41 personas hay un modelo por grupo de la validación cruzada y no uno solo, y el tamaño, calculado para otro contraste: salen 72, 101 o 767 personas.

Si repreguntan: Una sola cosa, definida antes de reclutar: evaluar una configuración ya congelada, con un contraste y un tamaño de muestra registrados y una única evaluación. Confirmaría el efecto de activación, que es el único que sostiene la hipótesis. El problema es el tamaño: según qué variabilidad use, salen 72, 101 o 767 personas evaluables, y las dos primeras cifras se estiman con solo 8 personas. Además, ese protocolo es del 06-11 y contrasta el historial contra el modelo sin historial; habría que reescribirlo para el contraste contra placebo antes de usarlo. Si se hace, aprovecharía de corregir el desfase de relojes y registrar electrooculograma.

Si repreguntan (¿qué modelo exactamente: el ajustado con las 25 o uno nuevo con las 41?): No está definido, y es un pendiente. Lo congelado es la configuración; en el análisis con 41 personas cada partición tiene ocho modelos, uno por grupo de la validación cruzada, y ninguno es "el modelo". Habría que fijar en el protocolo cuál se evalúa, antes de ver la cohorte. Y el tamaño de muestra del 06-11 se calculó para el contraste con y sin historial, no para el contraste contra placebo.
Fuentes: `resultados/protocolo_hipotesis_reintento_06-11-2026/INFORME.md`; `Escritura/Borrador Conclusiones 23-11-2026.md` (vault), sección 9.6.

**15. ¿Qué validez tienen las pseudoetiquetas, si no hay una medida externa? ¿Qué significa "atención alta"?**
Corta: Validez externa no tienen: no las comparé con autorreporte, desempeño en una tarea ni ninguna otra medida. El Attention Score describe un patrón de mirada relativo a la persona, no cuánto atendió, y "alta" es estar sobre la propia mediana. Todo lo que afirmo es sobre predecir estas etiquetas, no sobre atención o activación reales.

Si repreguntan: Validez externa no tienen: no las comparé con autorreporte, desempeño en una tarea ni ninguna otra medida. Son offline y relativas a la mediana de cada persona, así que las clases salen balanceadas por construcción y eso no demuestra nada psicológico. En atención, el Attention Score está dominado por fijaciones, dispersión y recorrido, y la pupila casi no pesa (−0,05): describe un patrón de mirada relativo a la persona, no cuánto atendió. "Alta" es estar sobre la propia mediana, así que alguien que atendió toda la sesión igual tiene la mitad de sus ventanas "bajas". El signo de cada variable ya está en el borrador (sección 6.1): la dispersión y el recorrido entran invertidos, así que "alta" es una mirada más quieta (pregunta 41). Y la etiqueta cambia según cómo se arme: las versiones de pesos iguales y PCA coinciden en el 66 % de las ventanas. Todo lo que afirmo es sobre predecir estas etiquetas, no sobre atención o activación reales.
Fuentes: `resultados/enfoques_41p_22-11-2026/INFORME.md` (E2); `resultados/profesor_binario_reconstruido_29-10-2026/INFORME.md`; `resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md`.

**16. Si al controlar la posición el efecto de activación queda inconcluso, ¿por qué habla de apoyo parcial?**
Corta: Es una objeción justa, y el encuadre es una decisión abierta. Con la posición en los dos modelos, el historial suma +0,032, pero no pasa Holm. Los tres controles conservan el signo y quedan inconclusos. El apoyo descansa en el contraste contra placebo (+0,046, p de Holm 0,004), con sus límites: lo fijé después de ver el placebo del historial completo, y el placebo viene de otras páginas.

Si repreguntan: Es una objeción justa, y el encuadre es una decisión abierta (la quinta de la lámina 33). Con la posición como variable en los dos modelos, el historial suma +0,032 [+0,004; +0,059], pero no pasa Holm sobre las cuatro pruebas (p 0,108). Dentro de un mismo estímulo suma +0,009 [−0,020; +0,037], también inconcluso, lo que no demuestra ausencia de efecto. Con el tiempo de sesión en ambos modelos queda en +0,026 [−0,006; +0,056]. Los tres controles conservan el signo y quedan inconclusos. El apoyo descansa en el contraste registrado contra placebo, sin las ventanas de 6 s que promedia la etiqueta (+0,046, p de Holm 0,004), que tiene sus propios límites: no excluye el soporte del filtro tónico de la GSR y, en la curva del 22-11, el 73 % de las ventanas de la banda de 6 s pertenece al mismo estímulo. Además lo fijé después de ver que el historial completo le ganaba al placebo (pregunta 4), y el placebo viene de otras páginas: dentro de una misma página no demostré que el historial supere al tiempo transcurrido (pregunta 2).
Fuentes: `resultados/reapertura_fase3_41p_22-11-2026/INFORME.md`; `resultados/reapertura_41p_22-11-2026/INFORME.md`; `documentacion/auditoria_final_23-11-2026/AUDITORIA_EXPERIMENTO.md` (I3 e I4).

**17. ¿El efecto de activación depende de unas pocas personas? Una persona con 26 ventanas pesa igual que una con cientos: ¿es razonable?**
Corta: En parte es desigual. En el contraste principal mejoran 23 de 41, la media es +0,036 y la mediana +0,014. Sin la persona más influyente queda en +0,028, así que no depende de una sola. Que una persona con 26 ventanas pese igual que las demás es una consecuencia de usar la persona como unidad; no fijé un mínimo de ventanas por persona.

Si repreguntan: En parte es desigual. En el contraste principal mejoran 23 de 41, la media es +0,036 y la mediana +0,014; una persona, P4, aporta 0,009 de esos 0,036. Sin la persona más influyente queda en +0,028 [+0,006; +0,050], así que no depende de una sola. En la curva del 22-11, el contraste contra placebo a 6 segundos es más parejo: mejoran 30 de 40 (28 de 41 en el contraste registrado) y la mediana es +0,042. Esa sensibilidad la pidió la auditoría y no estaba registrada. P4 es además la persona que conserva solo 26 ventanas con etiqueta de activación, así que su AUC es muy imprecisa. Que pese igual que las demás es una consecuencia de usar la persona como unidad; no fijé un mínimo de ventanas por persona.
Fuente: `resultados/reapertura_41p_22-11-2026/INFORME.md`.

**18. La fusión tardía, ¿es mejor o no? El cierre V3 decía otra cosa.**
No puedo concluir que una sea mejor: depende de la familia de modelo. Entre redes MLP y con las 41 personas (lámina 19), la tardía gana en atención por +0,012 [+0,005; +0,021]; es un contraste secundario, sin corrección por multiplicidad, y la fusión intermedia que probé es más profunda. Con HGB, en el cierre V3, el signo fue el contrario: −0,010 [−0,018; −0,003] en entrenamiento. En activación ninguna estrategia se distinguió de las demás. Lo que sostengo es lo más modesto: la comparación no permite elegir una fusión.
Fuentes: `resultados/ampliacion_41p_16-11-2026/INFORME.md` (E3); `resultados/cierre_v3_16-11-2026/INFORME.md`.

**19. Si normaliza con la sesión completa, ¿esto sirve en línea?**
Corta: No, tal como está. La mediana que define "alta" y varias variables por persona usan la sesión entera, incluido el futuro. El manuscrito pide normalizar solo con entrenamiento, así que hay una diferencia entre lo escrito y lo hecho que tengo que resolver con usted. Evaluar etiquetas calculadas solo con información previa queda como trabajo futuro.

Si repreguntan: No, tal como está. La mediana que define "alta" y varias variables por persona usan la sesión entera, incluido el futuro. El manuscrito pide normalizar solo con entrenamiento, así que hay una diferencia entre lo escrito y lo hecho que tengo que resolver con usted; ya no es una de las cinco preguntas de la lámina 33, sino el sexto punto, que va en el pie de esa lámina y digo de palabra. La adaptación a la persona que mejoró activación (+0,045 [+0,023; +0,069]) tampoco es desplegable, porque sus etiquetas de calibración usan esa misma normalización. Evaluar etiquetas calculadas solo con información previa queda como trabajo futuro.
Fuentes: `resultados/protocolo_hipotesis_reintento_06-11-2026/INFORME.md`; `resultados/enfoques_41p_22-11-2026/INFORME.md` (E4).

**20. La pupila responde al brillo de la pantalla. ¿Eso no contamina todo?**
Corta: No está corregido y es una limitación declarada. En la etiqueta de atención el daño parece acotado, porque la pupila casi no pesa en el Attention Score. En activación la pupila es una entrada, y no sé cuánto de lo poco que aporta es brillo y cuánto es activación. Para separarlo habría que medir la luminancia de cada página.

Si repreguntan: No está corregido y es una limitación declarada. En la etiqueta de atención el daño parece acotado, porque la pupila casi no pesa en el Attention Score; pero eso también significa que la etiqueta casi no usa la pupila. En activación la pupila es una entrada, y no se demostró el aporte de ninguna señal por separado: al permutarla la AUC cae 0,021, frente a 0,053 del EEG, pero esas importancias son descriptivas y ruidosas (la desviación entre folds supera a la media). No sé cuánto de ese poco es brillo y cuánto es activación. Para separarlo habría que medir la luminancia de cada página.
Fuentes: `resultados/enfoques_41p_22-11-2026/INFORME.md` (E2); `resultados/ampliacion_41p_16-11-2026/INFORME.md` (E5).

**21. ¿Cuántas veces estimó el efecto de activación sobre las mismas personas?**
Corta: Nueve veces el contraste principal, sobre las mismas 41 personas. Las diferencias van de +0,028 a +0,047; el signo es estable, pero 3 de los 9 intervalos incluyen el cero. El +0,036 es una estimación más precisa de lo ya visto, no una confirmación. El contraste mejor sostenido es otro, +0,046 frente al placebo; lo fijé después de ver el placebo del historial completo, así que tampoco es evidencia independiente.

Si repreguntan: Nueve veces el contraste principal, con y sin historial, siempre sobre las mismas 41 personas: la partición registrada el 16-11, tres particiones de robustez ese mismo día y cinco el 22-11. Las diferencias van de +0,028 a +0,047. El signo es estable, pero 3 de los 9 intervalos incluyen el cero. El +0,036 [+0,010; +0,065] sale de promediar las cinco del 22-11 cuando ya conocía las anteriores: es una estimación más precisa de lo ya visto, no una confirmación. Además el efecto es desigual entre personas: mediana +0,014 y mejoran 23 de 41. El contraste mejor sostenido es otro: el historial sin las ventanas de 6 s que promedia la etiqueta frente al placebo, +0,046, con p de Holm 0,004. Su protocolo quedó fijado antes de sus predicciones, pero después de ver, el mismo día y en las mismas personas, que el historial completo le ganaba al placebo (+0,038): es un refinamiento dirigido y no una evidencia independiente (pregunta 4). Qué hice para acotar el riesgo de p-hacking está en la pregunta 4.
Fuentes: `documentacion/auditoria_final_23-11-2026/AUDITORIA_EXPERIMENTO.md` (hallazgo I3); `Escritura/Borrador Conclusiones 23-11-2026.md` (vault), secciones 9.1 y 9.5.

**22. ¿Hubo una auditoría y qué encontró? ¿Quién la hizo?**
Corta: La hizo un asistente automático, a pedido mío, con código separado y sin reentrenar modelos. No es la revisión de un tercero ni valida el diseño, y nadie externo revisó esas revisiones. Reprodujo las cifras: 2.638 valores comparados, sin discrepancias. Tuvo seis hallazgos importantes, todos de lectura, ya incorporados. Cómo declararlo en la tesis es un pendiente real.

Si repreguntan: La hizo un asistente automático, a pedido mío, el 23-11, con código separado que no usa los scripts del repositorio y sin reentrenar modelos. No es la revisión de un tercero ni valida el diseño. Cómo declarar el uso de esas herramientas en la tesis lo tengo que resolver con la norma del programa. Reprodujo las cifras: 2.638 valores comparados, sin discrepancias. No tuvo hallazgos bloqueantes. Tuvo seis hallazgos importantes, todos de lectura y ninguno de cifras, que ya están incorporados en la presentación y en el borrador de conclusiones: la ventaja de la red, cuánto de la detección es ocular, la firmeza y el alcance del efecto temporal de activación, la fusión y el aporte de cada señal. Lo que no se puede verificar sin reentrenar es que las predicciones vengan de la configuración declarada. Y sigue valiendo lo de fondo: la auditoría revisa los cálculos, no reemplaza una cohorte nueva.

Si repreguntan (¿cuál asistente, con qué instrucciones, quién verificó al verificador, dónde lo declara la tesis?): Los informes de cada revisión están en el repositorio, con su alcance y sus hallazgos. Las revisiones se revisaron entre sí en rondas sucesivas, todas con asistentes automáticos y a pedido mío; eso no es independencia, y nadie externo las verificó. La tesis todavía no lo declara: falta conocer la norma del programa y es una de las preguntas de la minuta.

> Ojo: llevar anotados el nombre y la versión del asistente y dónde quedaron las instrucciones; este ensayo no los registra.

Fuente: `documentacion/auditoria_final_23-11-2026/AUDITORIA_EXPERIMENTO.md` y las carpetas `ronda2` a `ronda6` de esa auditoría.

**23. ¿Eligió la etiqueta de atención porque se predecía mejor?**
Corta: Seguí con ella después de ver eso, sí. Los modelos predecían mejor la de PCA, y eso no es un argumento de validez. Las dos coinciden en 66 % de las ventanas, y en la de PCA la pupila pesa −0,052: en la práctica es conducta de mirada. No repetí los análisis finales con la igualitaria; es la séptima decisión de la minuta y está abierta.

Si repreguntan: Seguí con ella después de ver eso, sí. Comparé pesos iguales y PCA en las 25 personas de entrenamiento y los modelos predecían mejor la de PCA; la nota de diseño proponía la igualitaria como principal y el PCA como sensibilidad. Eso no es un argumento de validez, como advierte el informe del 29-10, y puede favorecer a la versión más ligada a los movimientos de los ojos. Las dos coinciden en 66 % de las ventanas (kappa 0,33). En la de PCA pesan el recorrido de la mirada (0,557), la dispersión (0,520) y las fijaciones (0,508 y 0,398), y la pupila pesa −0,052: en la práctica es conducta de mirada. No repetí los análisis finales con la igualitaria; es la séptima decisión de la minuta y está abierta.
Fuentes: `resultados/profesor_binario_reconstruido_29-10-2026/INFORME.md`; `Diseno Metodologico/Modelo Profesor - Decisiones.md` (vault).

**24. Con el diseño original, ¿qué daba la hipótesis?**
Con entrenamiento, validación y test por separado, el cierre V3 del 16-11 no mostró una ventaja consistente del modelo con historial en ninguna de las dos variables. El análisis con 41 personas lo registré menos de cuatro minutos después del commit de ese resultado, para tener más potencia y sin cambiar la configuración. Es un cambio de diseño posterior a los datos, y por eso todo lo que sigue es exploratorio. Qué pasa con las 16 personas ya vistas está en la pregunta 5, y cómo elegí la configuración, en la 37.
Fuentes: `resultados/cierre_v3_16-11-2026/INFORME.md` (sección "Lectura"); commits `005a499` (11:35) y `1bbb083` (11:39) del 16-11.

**25. El filtro tónico de la GSR es bidireccional y usa toda la sesión. ¿Sirve entonces el contraste "sin los 6 s de la etiqueta"?**
Corta: Excluye las ventanas que la etiqueta promedia, no el soporte del filtro: del peso de la GSR, el 49 % cae en las ventanas nominales, el 25 % antes y el 25 % después. El contraste muestra que el historial real supera a un placebo; no demuestra que el pasado prediga el presente. Tampoco es fuga: la GSR no es entrada del Modelo Estudiante de activación.

Si repreguntan: Excluye las ventanas que la etiqueta promedia, no el soporte del filtro. La componente tónica sale de un pasa-bajos de 0,05 Hz aplicado en ambos sentidos sobre la sesión completa, y la fásica es la señal menos la tónica; las dos dependen de GSR anterior y posterior a esos 6 s. Además la etiqueta es en lo esencial el nivel tónico (dentro de cada persona, el nivel tónico de la ventana ordena la etiqueta con AUC 0,911, frente a 0,595 de la fásica). Del peso de la GSR sobre esa parte tónica, el 49 % cae en las ventanas nominales, el 25 % antes y el 25 % después. El contraste muestra que el historial real supera a un placebo, pero no separa "el pasado predice el presente" de "la fisiología de un momento se relaciona con la GSR de ese momento, que la etiqueta posterior aún contiene". Tampoco es fuga: la GSR no es entrada del Modelo Estudiante de activación. Por qué uso la GSR como etiqueta, y su latencia, están en la pregunta 7.
Fuentes: `scripts/preprocesamiento_secuencial.py` (función `prepare_gsr`); `resultados/preprocesamiento/configuracion_efectiva.json`; `documentacion/auditoria_final_23-11-2026/ronda3/AUDITORIA_CODIGO.md` (H2, comprobación `c03`).

**26. Un HGB con medias y desviaciones, ¿es un "modelo temporal"? ¿Y dónde está lo multimodal?**
No es secuencial: resume el historial. El único modelo que usa el orden, la GRU, no mostró una ventaja demostrable. Y no demostré que combinar señales aporte: en atención la GSR no agrega al EEG, y en activación no se demostró el aporte de ninguna señal por separado. Lo que tiene apoyo es más estrecho que la hipótesis: el historial reciente, resumido.
Fuentes: `resultados/cierre_final_41p_16-11-2026/INFORME.md`; `resultados/enfoques_41p_22-11-2026/INFORME.md` (E2).

**27. ¿Puede el efecto de activación ser movimiento o respiración?**
No lo puedo descartar. La etiqueta no tiene detector de artefactos sobre la GSR cruda y no medí movimiento. Un movimiento puede afectar a la vez a la GSR y, durante segundos, al EEG, la mirada y la pupila. El placebo no controla eso.
Fuente: `resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md`.

**28. Las personas de un mismo grupo vieron la misma secuencia de páginas. ¿Basta con separar por persona?**
Corta: No del todo. La validación cruzada separa personas, no grupos, y las personas de un mismo grupo vieron los estímulos en el mismo orden: el modelo puede aprender regularidades de la secuencia desde otras personas del grupo. No evalué dejando grupos fuera; se puede hacer y la inferencia seguiría siendo por persona, pero requiere volver a entrenar.

Si repreguntan: La partición estratifica por grupo y la validación cruzada separa personas, no grupos. Por qué se armaron cuatro grupos no está en mis notas y tengo que confirmarlo con el proyecto; lo que consta en los datos es que las personas de un mismo grupo vieron los estímulos en el mismo orden. Entonces el modelo puede aprender regularidades de la secuencia desde otras personas del grupo. No evalué dejando grupos fuera; se puede hacer con cuatro grupos de evaluación y la inferencia seguiría siendo por persona, pero requiere volver a entrenar. Lo que cambiaría es que cada modelo se ajusta con menos personas y solo hay cuatro modelos.
Fuentes: `resultados/sincronizacion/coordinacion_sesiones.csv`; `resultados/preprocesamiento/caracteristicas_multimodales.csv` (orden de estímulos por persona).

**29. El patrón de la etiqueta de atención al inicio de cada página, ¿es conducta o es cómo calcula las fijaciones?**
No lo separé. La duración de cada fijación se suma completa aunque exceda la ventana (pasa de 2.000 ms en cerca del 28 % de las ventanas y de 3.000 ms en el 4 % de las etiquetadas) y las ventanas no cruzan el cambio de estímulo, lo que acorta las duraciones al inicio. Por lo mismo, el soporte de la etiqueta de atención no es de 2 s. Además las posiciones tardías solo existen en estímulos largos. El nulo del historial se mantiene dentro de un mismo estímulo, pero el origen del patrón no lo estudié.
Fuentes: `scripts/preprocesamiento_secuencial.py`; `resultados/reapertura_fase3_41p_22-11-2026/INFORME.md`.

**30. ¿Hubo consentimiento informado y comité de ética? ¿Edad y sexo de los participantes?**
No lo tengo en mis notas. Los datos son del proyecto Fondecyt 1231122 y tengo que pedir esa documentación, junto con el protocolo de estímulos, antes de escribir la sección de participantes.

**31. Si ya tiene un seguidor ocular, ¿para qué predecir con EEG una etiqueta ocular?**
Tal como quedó, no tiene utilidad práctica. El diseño buscaba llegar a lo Atendido desde señales distintas de las que etiquetan, y lo que muestra es que eso no se logra con una etiqueta ocular. El valor es la advertencia metodológica.

**32. Registrar en su propio repositorio, ¿es un prerregistro?**
No. Lo verificable es que el protocolo entró a Git antes que las predicciones; que se publicara antes de correr no se puede verificar desde el repositorio, y las fechas las controlo yo. No hay un registro externo. Además, la primera versión del cierre V3 se detuvo por una revisión de código. Sirve para ordenar el trabajo, no para garantizarlo ante terceros. Lo que hice para acotar el riesgo de p-hacking está en la pregunta 4.
Fuente: `documentacion/Cierre_Experimental_Final_23-11-2026.md` (trazabilidad).

**33. La caída de la activación al final de la sesión, ¿es habituación?**
Es compatible, y también lo es con una deriva lenta de la señal o con el orden de los estímulos. Es descriptivo, sin contraste, y lo medí con la etiqueta binaria y no con el score continuo que comprometía el objetivo 6.
Fuente: `resultados/ampliacion_41p_16-11-2026/INFORME.md`.

**34. Si el Arousal Score no se detecta desde la ventana actual, ¿cómo sabe que mide activación y no ruido?**
No lo sé. No tiene validación externa, ni control de artefactos sobre la señal cruda, ni unidad física declarada. Lo que tiene a favor es interno: persiste entre ventanas (la etiqueta de 6 s antes predice la actual con AUC 0,680) y cae hacia el final de la sesión. Eso no demuestra que sea activación. Y la persistencia viene en buena parte de la construcción: la etiqueta es en lo esencial un nivel filtrado a 0,05 Hz, que cambia lento por definición. No tengo evidencia a favor que no venga del filtro o de una deriva de la señal.
Fuentes: `resultados/reapertura_fase2_41p_22-11-2026/descriptivos.csv`; `resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md`.

**35. ¿Qué queda de las contribuciones que prometía sobre fusión y sobre el protocolo de etiquetas?**
La de fusión queda sin conclusión: el signo cambia con la familia de modelo. La del protocolo cambia de sentido: prometía que el desempeño sería interpretable como información genuina, y el resultado muestra que separar señales no basta. Cómo reformularlas no lo decido yo solo: es parte de la quinta decisión, y la minuta lista cada punto con una redacción posible.

**36. Sus resultados de activación, ¿a qué parte de la navegación se refieren?**
Al 53 % de las ventanas que conserva la etiqueta (11.796 de 22.211): desde la quinta ventana de cada estímulo, en estímulos lo bastante largos. No dicen nada del inicio de cada página ni de los estímulos breves.
Fuente: `resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md`.

**37. ¿Cómo eligió la configuración del modelo de activación? ¿No favorece eso al historial?**
Corta: Puede favorecerlo. Las 15 hojas las elegí con las 25 personas de entrenamiento y la elección la decidió el modelo con historial; el contraste principal se concentra en esas 25: +0,055 frente a +0,001 en las otras 16. No está demostrado que esté inflado, y el contraste frente al placebo es positivo en los dos grupos (+0,035 y +0,064). Una sensibilidad con 7 hojas lo resolvería; no la corrí.

Si repreguntan: Puede favorecerlo, y no lo había declarado. El número de hojas lo elegí con las 25 personas de entrenamiento, por la AUC media de los modelos con 1, 8 y 32 ventanas. En activación la elección entre 7 y 15 hojas la decidió el de 32 (0,4994 con 7 hojas y 0,5311 con 15; con 1 ventana, 0,5123 y 0,5121): congelé la configuración en que el historial gana. Esas 25 personas son 25 de las 41 que después evalúo, y el contraste principal se concentra en ellas: +0,055 [+0,012; +0,101] frente a +0,001 [−0,052; +0,055] en las otras 16 el 16-11, y +0,046 frente a +0,021 con cinco particiones. No está demostrado que el contraste esté inflado: la diferencia entre grupos no es significativa con 16 personas, y en el cierre V3, con modelos ajustados solo con las 25, el mismo contraste fue +0,059 y +0,033 en validación y test. Y los dos contrastes que no dependen de esa elección de la misma forma son positivos en ambos grupos: el historial desplazado frente al placebo (+0,035 y +0,064) y la GRU, que no tuvo búsqueda (+0,045 y +0,059). En atención la elección no importa. Una sensibilidad con 7 hojas o con selección anidada lo resolvería; no la corrí, y hacerlo es reabrir la experimentación. Lo demás sobre las 41 personas está en la pregunta 5, y el cambio de diseño tras el cierre V3, en la 24.
Fuentes: `documentacion/auditoria_final_23-11-2026/ronda3/AUDITORIA_CODIGO.md` (H1, comprobación `c07`); `resultados/cierre_v3_16-11-2026/busqueda_interna_activacion.csv`; `resultados/cierre_final_41p_16-11-2026/INFORME.md` (heterogeneidad por grupo).

**38. Sus intervalos, ¿son percentil? ¿Qué pasa con los rótulos que quedan a una milésima del umbral?**
Sí: *bootstrap* percentil de personas, con 20.000 réplicas y la misma semilla en todos los contrastes. Con 41 personas el percentil puede quedar algo estrecho. Tres rótulos viven a milésimas de un umbral: atención (límite inferior 0,021), la red (0,023) y el historial desplazado (0,018). No los interpreto como distintos de sus vecinos, y lo digo en la sección 6.4 del borrador.
Fuente: `scripts/cierre_final_41p.py` (función `ci`); protocolos del 16 y del 22-11.

**39. En validación cruzada las AUC por persona comparten modelos. ¿Qué cubre su intervalo y qué no?**
Cubre la variación entre las personas evaluadas, con estos modelos. No cubre la dependencia entre personas que comparten modelo ni cuánto cambiaría el resultado con otras personas de entrenamiento. Por eso los intervalos describen a estas 41 personas y pueden ser optimistas para personas nuevas. Promediar cinco particiones no cambia la unidad, que sigue siendo la persona; cambia lo que estimo: el desempeño medio sobre particiones.
Fuente: `Escritura/Borrador Resultados y Discusión 23-11-2026.md` (vault), sección 6.4.

**40. El modelo de atención, ¿reconoce la página o la conducta?**
No se explica por reconocer la página. Comparando solo ventanas de un mismo estímulo, la AUC sin historial es 0,684 [0,667; 0,700], igual que con todas (0,683); dentro del mismo minuto, 0,675 [0,660; 0,689]. Es descriptivo, y el estrato del mismo estímulo usa cerca del 2 % de los pares. Que no sea la página no dice que sea atención: sigue siendo conducta de mirada.
Fuente: `resultados/reapertura_fase3_41p_22-11-2026/descriptivos.csv`; `resultados/reapertura_fase2_41p_22-11-2026/descriptivos.csv` (fracción de pares).

**41. ¿Qué es, en conducta, una ventana "alta" de atención: más movimiento o menos?**
Menos. En el puntaje las fijaciones entran con su signo y la dispersión y el recorrido de la mirada entran invertidos; la pupila casi no pesa. "Alta" es una ventana con fijaciones más largas y una mirada que se dispersa y recorre menos que lo habitual en esa persona: una mirada más quieta. No designa mayor atención en ningún sentido validado.
Fuente: `scripts/reconstruir_profesor_atencion_binaria.py` (direcciones declaradas); `resultados/temporalidad_eeg_v2_validacion_29-10-2026/profesor_final.joblib`.

**42. ¿Por qué dicotomizar por la mediana un puntaje continuo, si el objetivo 3 comprometía etiquetas continuas y categóricas?**
No tengo una justificación mejor que la práctica: la mediana por persona da clases cercanas al equilibrio y permite comparar la AUC entre personas. El costo es que la etiqueta cambia cerca de la mediana aunque el estado no cambie. Los resultados usan solo la etiqueta binaria; esa parte del objetivo 3 no está cumplida y está en la minuta para revisar.

**43. ¿Por qué la GSR sola predice una etiqueta ocular?**
No lo estudié. La GSR sola llega a 0,545 y no agrega nada al EEG (+0,002). Una lectura posible es que, estandarizada por sesión, informe del tramo de la sesión, y la etiqueta depende del reloj: el tiempo de sesión como única variable adicional agrega +0,025. Es una conjetura, sin contraste.
Fuente: `resultados/enfoques_41p_22-11-2026/INFORME.md` (E2).

**44. La adaptación a la persona, ¿no se beneficia de que la mediana de la sesión fije la proporción de clases del resto?**
Sí, puede. Las etiquetas de calibración se definen con la mediana de toda la sesión; como cada persona tiene cerca de la mitad de sus ventanas en cada clase, la proporción de "alta" al inicio condiciona la del resto. Por eso la adaptación (+0,045) no es utilizable en línea ni comparable con los demás contrastes (pregunta 19). Además evalúa 40 personas, sin un mínimo de ventanas por clase.
Fuente: `resultados/enfoques_41p_22-11-2026/INFORME.md` (E4); `scripts/enfoques_41p.py`.

**45. La metodología comprometía BA, macro-F1 y *recall*. ¿Por qué decide con AUC, y qué dicen las otras?**
Esa redacción es de septiembre, cuando las etiquetas tenían tres clases. Con etiquetas binarias decido con AUC por persona. Las otras tres están calculadas solo en el cierre V3, con umbral fijo de 0,5 y como descriptivas; el análisis con 41 personas conserva la BA, y los del 22 y 23-11 informan solo AUC. No las tengo para los resultados finales, y cuál va como métrica principal está por decidir.
Fuente: `Escritura/Borrador Secciones pendientes 23-11-2026.md` (vault), sección 4.8.3.

**46. ¿Cuántas pruebas hizo en total en las doce etapas?**
No tengo ese recuento hecho; es un pendiente. Holm corrige dentro de cada etapa y no entre las doce, los contrastes secundarios no llevan corrección y varias etapas fueron dirigidas por resultados ya vistos. Por eso no presento nada como confirmación y rotulo cada resultado con su estatus.

**47. Si hoy empezara de nuevo con estos datos, ¿qué diseño usaría?**
Reservaría personas que no se miran hasta el final, con un contraste y una regla fijados antes. Elegiría la configuración con selección anidada. Evaluaría dejando grupos experimentales fuera y con un mínimo de ventanas por persona. Definiría la etiqueta de activación con un filtro causal y la predeciría con ventanas más largas. Y no evaluaría un modelo de EEG con una etiqueta ocular sin registrar electrooculograma.
Fuente: `Escritura/Borrador Resultados y Discusión 23-11-2026.md` (vault), secciones 7.5, 8.7 y 8.9.

**48. ¿Qué resultado habría refutado la hipótesis?**
El que obtuve primero. Con el diseño y la regla planificados, el cierre V3 no mostró una ventaja consistente del modelo con historial en ninguna de las dos variables: con ese diseño no hay evidencia para sostener la hipótesis. El apoyo parcial sale de un segundo diseño, adoptado después de ver ese resultado, y de una lectura más exigente del criterio. Así lo dice el borrador (sección 8.1; pregunta 24).

**49. Saavedra, en su mismo grupo, no halló mejora con fusión tardía. ¿Su resultado lo confirma, lo contradice o no dice nada?**
No dice nada concluyente. Entre redes MLP la fusión tardía gana en atención por +0,012, como contraste secundario sin corrección; con HGB, en el cierre V3, el signo fue el contrario, y en activación no hubo diferencias. Además en atención la GSR no agrega al EEG, así que hay poco que fusionar. No puedo decir que confirme ni que contradiga su resultado (pregunta 18).
Fuente: `resultados/ampliacion_41p_16-11-2026/INFORME.md` (E3); `resultados/cierre_v3_16-11-2026/INFORME.md`.

---

## 4. Tres frases de cierre, si queda un minuto

1. Con el encuadre que propongo, la hipótesis tiene apoyo parcial y viene de activación: el historial de los últimos segundos ayuda un poco, de forma desigual entre personas y con modelos que siguen siendo débiles.
2. En atención aprendí dos cosas que no esperaba: lo que parecía temporal era la posición en la página, y cerca de un tercio de lo que parecía cerebral depende de componentes ligados a los ojos; no puedo afirmar que detecte lo Atendido.
3. Nada de esto está confirmado en personas nuevas, así que lo que necesito de usted hoy es saber si escribo con estos resultados o planifico una cohorte.

---

## Láminas donde la nota, el contenido o los informes no calzan

Revisado el 23-11-2026, fila por fila, contra `relato.py` y `GUIÓN.md` regenerados después de la auditoría. Las seis filas que tenía esta tabla quedaron resueltas y se sacaron: la lámina 23 ahora dice que sus cifras son del 16 y del 18-11 y fecha el +0,038 en el análisis post hoc del 18-11; la lámina 30 ya no dice "6 a 12 s" (dice que solo hay respaldo para los 6 s anteriores) y desde el 26-11 muestra el contraste registrado, +0,046 [+0,018; +0,073]; la nota de la lámina 26 presenta el margen de 0,02 como "una propuesta mía sin aprobar"; el punto 8 del índice (lámina 2) dice "por qué cuesta detectar activación"; y la nota de la lámina 33 menciona el séptimo punto de la minuta. También quedaron corregidas las lecturas que objetó la auditoría en las láminas 1, 26, 27, 28, 29, 30, 31 y 33. Los cinco detalles que quedaban se corrigieron después en `relato.py`. El 26-11-2026, tras la auditoría de coherencia, se ajustaron además en `relato.py` las láminas 4, 7, 13 a 17, 19, 20, 23, 26 a 35, 37 y 38, y este ensayo se puso al día con ellas. El 26-11-2026, tras la lectura crítica, cambiaron en `relato.py` el título de la lámina 12, el texto visible de las láminas 5, 10, 29, 30 y 31 y las notas de las láminas 1, 3, 5, 10, 11, 12, 18, 20, 21, 22, 23, 25, 26, 29, 30 y 33; este ensayo se puso al día con ellas. El 26-11-2026, tras la segunda auditoría de la presentación (`documentacion/auditoria_final_23-11-2026/ronda4/AUDITORIA_PRESENTACION_R2.md`) y la verificación del diff de la ronda 2, cambiaron en `relato.py` los títulos de las láminas 15 (comillas) y 24; el texto visible de las láminas 5, 7, 27, 28, 29, 30, 31, 33 y 37; los pies de las láminas 12, 21, 23, 24, 27, 28, 29 y 33 (este último es nuevo: los dos puntos adicionales de la minuta); y las notas de las láminas 1, 2, 5, 11, 18, 23, 24, 27, 28, 29, 30, 31 y 33. En `estilo_tecnico.py` cambiaron solo rótulos de texto de los gráficos de las láminas 6, 12, 21 y 38 (sin tocar datos ni cálculos), y en `crear_presentacion.py`, la fecha de corte de `LEEME.md`. Este ensayo se puso al día con todo eso: títulos, tiempos, guion recortado y respuestas cortas. El 27-11-2026, tras la segunda lectura crítica (`documentacion/auditoria_final_23-11-2026/ronda6/SEGUNDA_LECTURA_COMITE.md`), cambiaron en `relato.py` el título de la lámina 30 ("Conclusiones provisorias: apoyo parcial"), el texto visible de las láminas 28 (fila "Tiempos") y 30 (punto 1) y las notas de las láminas 1, 7, 21, 23, 28 y 30; este ensayo se puso al día con ellas.

Diferencias conocidas entre este ensayo, `relato.py` y los informes, al 27-11-2026:

| Lámina | Qué no calza | Dónde está el dato correcto |
|---|---|---|
| — | Ninguna diferencia conocida entre este ensayo y `relato.py`. La de la lámina 12 (el eje decía "OOF") se corrigió en `estilo_tecnico.py` | — |
| 31 | La lámina y su guion dicen "una advertencia sobre etiquetas oculares"; el borrador de conclusiones (9.7) nombra desde el 27-11 dos advertencias metodológicas (la posición y las etiquetas oculares). No se cambió la lámina: depende de la decisión 5 | `Escritura/Borrador Conclusiones 23-11-2026.md`, sección 9.7 |
| 2 | Pendiente de confirmar, no es una diferencia: la nota y el guion dicen que lo nuevo "va desde los resultados con 41 personas"; depende de qué vio el profesor en la última reunión | Mario |
