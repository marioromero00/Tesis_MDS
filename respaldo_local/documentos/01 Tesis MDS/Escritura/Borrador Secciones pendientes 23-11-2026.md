# Borrador: secciones pendientes con insumo documentado

> [!info] Estado
> Borrador redactado el 23-11-2026 a pedido de Mario. **No reemplaza a [[Estructura Tesis]]**: las secciones que aquí se redactan siguen marcadas como *(pendiente)* en el esqueleto hasta que él las revise. **No hay aprobación registrada del profesor guía** sobre este texto. Complementa a [[Borrador Resultados y Discusión 23-11-2026]] (versión vigente; reemplaza al del 18-11-2026, que se conserva), [[Borrador Discusión fisiológica 23-11-2026]] (integrado el 26-11-2026 en el capítulo 8 del anterior; se conserva como registro) y [[Borrador Conclusiones 23-11-2026]]. No se entrenó ningún modelo ni se modificó ningún archivo existente para escribirlo. Revisado el 26-11-2026 contra el código y los datos (`repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/ronda2/AUDITORIA_SECCIONES_PENDIENTES.md`). Las auditorías que cita este borrador son revisiones y recálculos con código separado, hechos con un asistente automático a pedido del autor; no son revisiones de un tercero. Revisión editorial aplicada el 26-11-2026 (`repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/ronda4/REVISION_EDITORIAL.md`), sin cambios de cifras: el material de proceso que salió de la prosa quedó en líneas "Nota de trabajo (no va en la tesis)", y las remisiones a los capítulos 6 a 8 siguen la numeración nueva de [[Borrador Resultados y Discusión 23-11-2026]]. Ajustado el 27-11-2026 en la sección 4.8.3 a una segunda lectura crítica (`repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/ronda6/SEGUNDA_LECTURA_COMITE.md`).

> [!warning] Decisiones abiertas que este texto no cierra
> Las cinco decisiones con checkbox de [[Resumen Diseño Etiquetas y Modelos]] siguen abiertas: (1) método de fusión y umbral de discretización del *Attention Score*; (2) combinación de variables de GSR y umbral del *Arousal Score*; (3) ventana de agregación específica para GSR; (4) si redefinir "emoción" como activación (*arousal*) es aceptable para el alcance de la hipótesis; (5) si existe alguna fuente de validación externa para las etiquetas. Donde este borrador describe una etiqueta, describe **la operacionalización que se usó en los experimentos**, no una decisión tomada. Lo único registrado sobre el profesor guía es que Mario comunicó el 01-11-2026 que su profesor aprobó usar las pseudoetiquetas GSR V2 (`notas/bitacora.md`); eso no marca ningún checkbox ni equivale a una validación externa. Además siguen abiertas las siete decisiones de noviembre que lista la sección 8.10 de [[Borrador Resultados y Discusión 23-11-2026]], con la numeración de [[Avance - 23-11-2026 (Minuta de decisiones con el profesor)]]: (1) cohorte nueva o escribir con las personas ya registradas; (2) margen práctico de 0,02; (3) "emociones" presentada como activación; (4) etiqueta de atención original o corregida por posición; (5) encuadre; (6) etiquetas normalizadas con la sesión completa de cada persona (sección 4.8.2); (7) *Modelo Profesor* con PCA (análisis de componentes principales) como definición del *Attention Score* (tabla final, fila 4.5.1). Ninguna está tomada.

> [!note] Cómo leer este borrador
> - **Numeración.** El esqueleto no trae números; se usa el orden de sus títulos (capítulo.sección.subsección), que es el que produciría LaTeX.
> - **Rutas.** Las fuentes se dan relativas a `/Users/mario/Proyectos/tesis-mds/`.
> - **Siglas.** EEG es electroencefalograma y GSR es respuesta galvánica de la piel (*galvanic skin response*). KDD es descubrimiento de conocimiento en bases de datos (*knowledge discovery in databases*); EDA, análisis exploratorio de datos (*exploratory data analysis*); CNN, red neuronal convolucional; ViT, *Vision Transformer*; SHA-256, una función de resumen criptográfico que aquí se usa para identificar archivos y ordenar participantes. Las demás se desarrollan donde aparecen.
> - **Versiones.** La tabla de características por ventana (`caracteristicas_multimodales.csv`) y la partición por participante son del 22-08-2026 y **siguen vigentes**: todos los análisis posteriores las leen. Las **etiquetas** del 22-08-2026 (tres clases) **no** están vigentes: las vigentes son la atención binaria reconstruida del 29-10-2026 y las pseudoetiquetas GSR V2 del 01-11-2026. Cada cifra indica a qué versión pertenece.
> - **Cifras calculadas para este borrador.** Algunas no aparecen escritas en ningún informe y se obtuvieron contando o resumiendo una tabla existente; van marcadas como *(calculado desde …)*.

---

## Capítulo 1: Introducción

### 1.4 Preguntas de Investigación

Las preguntas se derivan de la hipótesis y de los objetivos específicos 2 a 7, sin modificar su alcance. El objetivo 1 (revisión de literatura) no origina una pregunta propia.

1. **Temporalidad.** ¿Obtienen los modelos temporales multimodales un mejor desempeño fuera de muestra que los modelos estáticos comparables al predecir las pseudoetiquetas de atención y de activación durante la navegación web, en participantes no usados para su ajuste? *(Hipótesis; objetivos 4 y 7.)*
2. **Fusión y aporte de las señales.** ¿Cuánto aportan al desempeño cada señal y el historial de ventanas anteriores, y cambia ese desempeño entre fusión temprana, intermedia y tardía? *(Objetivo 5.)*
3. **Señales y pseudoetiquetas.** ¿Qué calidad y disponibilidad tienen las señales registradas una vez sincronizadas con criterios de calidad definidos, y qué tan estables son las pseudoetiquetas continuas y categóricas de atención y de activación, definidas con señales distintas de las que luego las predicen? *(Objetivos 2 y 3.)*

   > Nota de trabajo (no va en la tesis): redacción ajustada el 26-11-2026 para no cambiar el alcance de los objetivos 2 y 3; pendiente de revisión por Mario.

4. **Evolución durante la sesión.** ¿Cómo cambian el *Attention Score* y el *Arousal Score* a lo largo de la sesión, y son esos cambios compatibles con fatiga o habituación? *(Objetivo 6; pregunta descriptiva.)*

Tres precisiones de alcance. Primero, la pregunta 1 es la única que contrasta la hipótesis; las preguntas 2 a 4 no son hipótesis adicionales. Segundo, la hipótesis habla de "emociones" y estas preguntas hablan de activación (*arousal*): esa redefinición es una propuesta de alcance que el profesor guía aún no confirma. Tercero, la pregunta 3 se refiere a la estabilidad de las reglas de etiquetado; no a la validez externa de los constructos, que este diseño no permite establecer.

Fuentes: `documentos/01 Tesis MDS/Escritura/Estructura Tesis.md` (hipótesis y objetivos, formulación del 22-09-2026); `documentos/01 Tesis MDS/Marco Teorico/Problema e hipótesis.md` (operacionalización, criterios de interpretación y análisis complementario); `documentos/01 Tesis MDS/Marco Teorico/Referencia Tesis Previas.md` (uso de preguntas de investigación en tesis previas del grupo).

---

## Capítulo 4: Metodología

### 4.3 Participantes

> [!warning] Sección parcial
> Las notas solo permiten describir cuántas personas hay y cómo se seleccionaron para el análisis. **No hay insumo** sobre reclutamiento, criterios de inclusión, edad, sexo, consentimiento informado ni comité de ética; tampoco sobre el criterio con que se armaron los grupos experimentales ni el protocolo de estímulos. Esos párrafos quedan por escribir con información del proyecto.

La Toma de Muestra 2 registra 48 participantes, identificados como P1 a P48, con una sesión principal cada uno. Las grabaciones se realizaron entre el 8 y el 30 de agosto de 2025 *(calculado desde `coordinacion_sesiones.csv`)*. La exportación del seguidor ocular contiene además una grabación de prueba (`Test_Participant`), que no corresponde a un participante y no se usa.

Cada participante pertenece a uno de cuatro grupos experimentales, registrados en la exportación como `SlowWeb G1` a `SlowWeb G4`, con 13, 12, 12 y 11 personas respectivamente *(calculado desde `coordinacion_sesiones.csv`)*. La exportación registra el grupo como nombre de la línea de tiempo de la grabación. Las notas no documentan con qué criterio se armaron los grupos. Lo que consta en los datos es que cada grupo corresponde a un orden de presentación: las personas de un mismo grupo vieron los estímulos que comparten en el mismo orden, y entre grupos el orden difiere. El orden coincide en los 265 pares de personas de un mismo grupo; entre grupos, la correlación de rangos de Kendall va de 0,26 a 0,70 *(calculado desde `caracteristicas_multimodales.csv`)*. Falta confirmarlo con el protocolo del proyecto. Aquí los grupos solo se usan para estratificar la partición (sección 4.8.2).

De las 48 personas, 41 integran el análisis principal. Las siete restantes se apartaron con criterios fijados antes de entrenar modelos:

| Participantes | Motivo | Destino |
|---|---|---|
| P1, P14, P17, P25 | EEG no utilizable: saturación o repetición plana sobre 30 % | Excluidos |
| P7, P42 | La exportación no contiene GSR | Excluidos |
| P29 | El EEG comienza 329,9 s antes que el seguidor ocular; emparejamiento por revisar | Solo análisis de sensibilidad |

Ninguna persona se excluyó por el desempeño de los modelos.

Fuentes: `repos/Tesis_MDS/resultados/sincronizacion/coordinacion_sesiones.csv`; `repos/Tesis_MDS/resultados/modelado/particion_participantes.csv`; `repos/Tesis_MDS/resultados/preprocesamiento/auditoria_participantes.csv`; `documentos/01 Tesis MDS/Analisis de Datos/ETIQUETAS_Y_BASELINES.md` (partición y auditoría de P29, 22-08-2026); `documentos/01 Tesis MDS/Analisis de Datos/EDA_GSR.md` (P7, P42 y `Test_Participant`).

### 4.5.2 Definición Emoción

> [!warning] Alcance abierto
> El título es el del esqueleto. El contenido describe **activación (*arousal*)**, no emoción en sentido amplio. Que la hipótesis, que dice "emociones", pueda operacionalizarse así es una decisión abierta del profesor guía. También siguen abiertas la combinación de variables de GSR, el umbral de discretización, la ventana de agregación y la existencia de validación externa. Lo que sigue es la operacionalización usada en los experimentos (pseudoetiquetas GSR V2, 01-11-2026).

**Por qué activación.** La Toma de Muestra 2 no tiene expresión facial. De sus cuatro señales, la respuesta galvánica de la piel (GSR, *galvanic skin response*) registra activación simpática y no informa valencia ni permite identificar emociones discretas. Una etiqueta de valencia exigiría usar el EEG, que es señal de entrada del *Modelo Estudiante*, o la expresión facial, que no existe en este conjunto de datos. Por eso, de forma provisoria, la variable objetivo se limita a un solo eje, la activación, y se nombra así en todo el documento (decisión abierta sobre presentar "emociones" como activación).

**Modelo Profesor y Modelo Estudiante.** El *Modelo Profesor* de activación usa únicamente GSR y produce el *Arousal Score*. El *Modelo Estudiante* lo predice con EEG, eye tracking y pupilometría. Se cumple la regla de no-circularidad (sección 4.7): la GSR no aparece entre las entradas del *Modelo Estudiante* de activación. Eye tracking y pupilometría construyen la etiqueta de atención, pero aquí actúan solo como predictores de otra etiqueta.

**Construcción del *Arousal Score*.** Se calcula por ventana de 2 s con paso de 1 s, a partir de la tabla de características de la sección 4.7:

1. *Control de calidad.* Una ventana es válida si su cobertura de GSR es de al menos 50 %, si sus cuatro componentes son finitos y si los conteos de respuestas no son negativos.
2. *Componentes.* Nivel tónico medio, componente fásica media, número de respuestas de conductancia (SCR, *skin conductance responses*) y prominencia media de las SCR.
3. *Normalización.* Al número de SCR y a su prominencia media se les aplica primero la transformación log(1 + x). Luego cada componente se estandariza dentro de la persona usando solo sus ventanas válidas. Un componente constante aporta cero; un componente ausente no se rellena.
4. *Score de 2 s.* Promedio de los cuatro componentes estandarizados, vuelto a estandarizar dentro de la persona.
5. *Score de 6 s.* Promedio del score de 2 s sobre cinco ventanas consecutivas válidas, lo que equivale a 6 s de señal, estandarizado otra vez dentro de la persona. La secuencia se reinicia al cambiar de participante, grabación, segmento o estímulo, ante una ventana inválida o ante un hueco. Es causal solo en las ventanas que promedia (la actual y las cuatro anteriores); los componentes que entran en ese promedio no lo son, por el filtro tónico (ver "Límites").
6. *Discretización.* La versión categórica es binaria: activación alta si el score de 6 s supera la mediana de la persona, baja si queda por debajo. Los empates con la mediana (tolerancia 1e-8) quedan sin etiqueta en vez de asignarse a una clase.

El score continuo se conserva junto a la etiqueta binaria, como exige el objetivo 6.

**Qué resulta.** De las 22.211 ventanas de las 41 personas del análisis principal, 11.796 quedan etiquetadas (53,1 %): 7.028 en las 25 personas de entrenamiento, 2.584 en las 8 de validación y 2.184 en las 8 de prueba. Las 10.415 restantes se pierden por historial insuficiente (9.995), por cobertura o indicador de calidad inválido (401) y por empate con la mediana (19). La mayor pérdida proviene de exigir cinco ventanas consecutivas dentro de un mismo estímulo, no de mala calidad de la GSR. Las 41 personas conservan ambas clases; el equilibrio entre clases (5.898 y 5.898) es consecuencia del umbral por mediana y no dice nada sobre su validez. P4 conserva solo 26 de sus 459 ventanas, porque apenas 58 tienen GSR válida.

**Por qué V2.** La versión V2 se construyó el 01-11-2026 para corregir problemas de calidad de la etiqueta anterior: ventanas etiquetadas sin GSR válida (P4) y empates con la mediana asignados a una clase (P34). Una revisión posterior encontró además un error de alineación de índices en el generador anterior, que dejaba desplazada la mayor parte de las posiciones de componentes. Las métricas de activación calculadas con esas etiquetas no permiten sostener ni rechazar la hipótesis. La versión V2 asigna por índice, se reprodujo de forma independiente y es la única que se usa en los resultados.

> Nota de trabajo (no va en la tesis): los problemas de calidad se detectaron el 30-10-2026. El error de alineación lo encontró la auditoría del 02-11-2026 en `repos/Tesis_MDS/scripts/preparar_modelado.py`: 25.498 de 25.992 posiciones de componentes quedaban desplazadas; ese denominador es el archivo completo de 48 personas, no el número de etiquetas que cambian. La reproducción independiente de la V2 usó tolerancia 1e-12.

**Límites.** En la práctica el *Arousal Score* es, en lo esencial, el nivel tónico de la GSR relativo a la sesión: dentro de cada persona, el nivel tónico de la ventana ordena la etiqueta con AUC 0,911, frente a 0,595 de la componente fásica y 0,522 del número y de la prominencia de las SCR. Como la componente tónica sale de un filtro aplicado en ambos sentidos (sección 4.6.3), el soporte temporal real de la etiqueta excede los 6 s nominales: del peso de la GSR sobre su parte tónica, el 49 % cae dentro de las cinco ventanas, el 25 % antes y el 25 % después (análisis descriptivo no registrado; lo que esto cambia en la lectura de los contrastes está en la sección 6.1 de [[Borrador Resultados y Discusión 23-11-2026]]). La normalización y la mediana usan la sesión completa de cada persona: la etiqueta es relativa a la sesión y se calcula offline, no sirve como detector en tiempo real. No se aplicó un desfase para compensar la latencia de las SCR (1 a 5 s); el contexto de 6 s cumple esa función de forma aproximada, y la ventana específica para GSR sigue siendo una decisión abierta. El control de calidad opera sobre variables derivadas, sin un detector de artefactos sobre la señal cruda. No existe una medida externa de activación contra la cual validar la etiqueta, y la unidad física de la GSR no está declarada en la exportación.

> Nota de trabajo (no va en la tesis): el reparto del peso del filtro tónico y la comparación entre componentes son la comprobación `c03` de la auditoría de código del 26-11-2026.

Fuentes: `repos/Tesis_MDS/resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md`, `protocolo.json`, `motivos.csv`, `resumen_personas.csv` y `auditoria_independiente_02-11-2026.json` de la misma carpeta; `repos/Tesis_MDS/scripts/reconstruir_etiquetas_gsr_calidad_v2.py` (pasos 1 a 6); `repos/Tesis_MDS/resultados/cierre_final_41p_16-11-2026/predicciones_activacion.csv.gz` (conteo por clase, *calculado para este borrador*); `documentos/01 Tesis MDS/Diseno Metodologico/Etiqueta Emocion.md` y `Resumen Diseño Etiquetas y Modelos.md` (justificación y decisiones abiertas); `notas/bitacora.md` (entradas del 30-10, 01-11 y 02-11-2026).

### 4.6.1 Sincronización de Fuentes

Los registros provienen de dos sistemas sin una clave común. El programa Tobii Pro Lab exporta en un solo archivo el eye tracking, la pupilometría y la GSR, que por lo tanto comparten reloj. El electroencefalograma (EEG) se registró con un equipo OpenBCI Cyton con módulo Daisy, en archivos separados por sesión. No existen marcas de sincronización compartidas por hardware (*triggers*) entre ambos sistemas.

**Dominio temporal común.** Todas las marcas de tiempo se llevan a tiempo universal coordinado (UTC). En Tobii, cada muestra se ubica sumando su tiempo relativo, en microsegundos, al inicio UTC de la grabación. En OpenBCI, el inicio de cada sesión se toma de la hora local de la primera muestra del archivo de texto, que se interpreta como UTC−4 (Chile en agosto de 2025). Las 104 sesiones se leyeron desde archivos de texto, de modo que la lectura alternativa de archivos BrainFlow, cuya marca Unix ya es absoluta, no llegó a usarse. Para recortar las ventanas se usa la marca Unix de cada muestra (columna `Timestamp` del archivo de texto). El desfase entre equipos se informa como inicio de Tobii menos inicio de EEG; un valor positivo indica que el EEG comenzó antes.

**Emparejamiento de sesiones.** El archivo de EEG contiene 104 carpetas de sesión: 48 principales, 51 de prueba y 5 sin identificador de participante *(calculado desde `eeg_resumen_sesiones.csv`)*. Para cada grabación Tobii se normaliza el identificador del participante, se restringen los candidatos a sesiones EEG de la misma persona y se elige la de inicio más cercano. Cuando una sesión tiene más de un archivo se usa el más largo, para evitar fragmentos de arranque. Cada par queda con un estado de revisión; un desfase mayor de 180 s entre inicios lo deja para revisión.

De las 49 grabaciones Tobii, 47 quedaron como candidatas directas. P29 quedó para revisión, porque su EEG comienza 329,9 s antes; la grabación de prueba no tiene pareja válida. Entre las 47 candidatas el desfase va de −79,6 s (P25, único caso en que Tobii comenzó antes) a +86,2 s, con mediana de 13,2 s *(calculado desde `coordinacion_sesiones.csv`)*.

**Deriva de los relojes.** No se estimó ni se corrigió. Estimarla exige al menos dos eventos observados de forma independiente en ambos equipos, y los eventos disponibles solo existen en Tobii. El procedimiento del cuaderno de referencia buscaba la muestra de EEG más cercana a cada evento Tobii, con lo que reutilizaba el mismo reloj que pretendía validar. El factor de escala se fija en 1,0, que significa "sin corrección identificable" y no "sin deriva".

**Ventanas comunes.** Las señales conservan su frecuencia nativa: cerca de 125 Hz el EEG, 60 Hz el eye tracking y la pupila, y 15 Hz la GSR. No se remuestrean a una frecuencia común. Las ventanas se definen en el reloj de Tobii y el EEG se recorta con los mismos límites en UTC.

**Precisión alcanzada.** La alineación es por reloj absoluto y no llega al nivel de muestra. Una comprobación del 23-11-2026, que compara el EEG con la mirada y los parpadeos registrados por el seguidor ocular, encontró que el EEG va atrasado entre 0,18 y 0,53 s en las 41 personas (mediana 0,45 s). Ese desfase no se corrigió, porque las ventanas ya estaban congeladas. Equivale a correr las ventanas de EEG entre 9 % y 26 % de su duración respecto de las otras señales. No invalida los resultados, pero puede atenuar la relación entre el EEG y el resto, incluidas las etiquetas; ese efecto no se midió. El desfase se agrupa en dos valores (cerca de 0,28 s en P2 a P21, P36 y P37, y cerca de 0,48 s en el resto), lo que sugiere una causa sistemática de adquisición que no se investigó, y su estimación es poco segura en las personas con acoplamiento bajo. La dirección del corrimiento es hacia el pasado: cada ventana de EEG contiene actividad ligada a la conducta ocular de unas décimas de segundo antes de la ventana, y no posterior. El rango, la mediana y los dos valores en que se agrupa el desfase están en la sección 7.8 de [[Borrador Resultados y Discusión 23-11-2026]].

> Nota de trabajo (no va en la tesis): el corrimiento de 9 % a 26 % corresponde a 0,184 a 0,528 s sobre 2 s (*calculado desde `personas.csv`*); el informe de origen dice "entre un 12 % y un 25 %". La dirección se comprobó por el signo con que se estimó el desfase (función `lagged_corr` de `scripts/montaje_ocular_41p.py`).

Fuentes: `documentos/01 Tesis MDS/Analisis de Datos/SINCRONIZACION_SENALES.md` y `DOCUMENTACION_DATOS_MDS.md` (sincronizadas al 22-08-2026; la tabla de coordinación sigue vigente); `repos/Tesis_MDS/resultados/sincronizacion/coordinacion_sesiones.csv`; `repos/Tesis_MDS/resultados/eda/eeg/eeg_resumen_sesiones.csv`; `documentos/01 Tesis MDS/Analisis de Datos/PREPROCESAMIENTO_MULTIMODAL.md` (frecuencias y recorte por UTC); `repos/Tesis_MDS/resultados/montaje_ocular_41p_23-11-2026/INFORME.md` y `personas.csv` de la misma carpeta (desfase empírico); `repos/Tesis_MDS/scripts/sincronizar_senales.py` y `preprocesamiento_secuencial.py` (lectura de las marcas de tiempo y umbral de 180 s); `repos/Tesis_MDS/resultados/sincronizacion/inventario_eeg.csv` (formato de las 104 sesiones).

### 4.6.3 Preprocesamiento GSR

La GSR se lee de las filas del archivo Tobii cuyo sensor es `GSR`. Su frecuencia efectiva es cercana a 15 Hz en todas las grabaciones; el valor de 8 Hz del cuaderno de referencia no se confirmó en los datos. La unidad física no está declarada en la exportación, por lo que se trabaja con valores estandarizados y no se interpretan amplitudes absolutas.

El procesamiento es el siguiente:

1. La señal se estandariza por sesión, excluida la calibración.
2. La componente tónica se obtiene con un filtro Butterworth pasa-bajos de segundo orden a 0,05 Hz, y la fásica como la diferencia entre la señal y la tónica.
3. Las SCR se detectan dentro de cada ventana como picos de la componente fásica con prominencia mínima de 0,05 unidades estandarizadas.
4. Para cada ventana de 2 s se calculan la cobertura y las variables de la sección 4.7. Una ventana es válida si su cobertura es de al menos 50 %.

Dos límites condicionan el uso posterior. La estandarización por sesión y el filtro tónico, que se aplica en ambos sentidos, usan información de toda la sesión: estas variables no son causales a nivel de muestra. El núcleo del filtro tónico tiene el 25 % de su masa a más de 5 s del centro y el 6,5 % a más de 10 s (análisis descriptivo no registrado). Además, no se aplicó un detector de artefactos sobre la señal cruda.

> Nota de trabajo (no va en la tesis): la masa del núcleo del filtro tónico es la comprobación `c03` de la auditoría de código del 26-11-2026.

En el diseño, la GSR es entrada del *Modelo Estudiante* de atención y fuente única del *Modelo Profesor* de activación. Por la regla de no-circularidad no se usa para predecir la activación.

Fuentes: `documentos/01 Tesis MDS/Analisis de Datos/PREPROCESAMIENTO_MULTIMODAL.md`; `repos/Tesis_MDS/resultados/preprocesamiento/configuracion_efectiva.json` (0,05 Hz, prominencia 0,05, cobertura 50 %); `documentos/01 Tesis MDS/Analisis de Datos/EDA_GSR.md` (frecuencia y unidad); `repos/Tesis_MDS/resultados/cierre_v3_16-11-2026/INFORME.md` (variables no causales por muestra).

### 4.6.4 Preprocesamiento Eye Tracking

El eye tracking se lee de las filas del sensor `Eye Tracker`, a una frecuencia cercana a 60 Hz. Se usan el punto de mirada en píxeles y la clasificación de movimientos oculares que entrega Tobii con su filtro I-VT (identificación por umbral de velocidad), que distingue fijaciones, sacadas, ojos no encontrados y muestras sin clasificar.

Los eventos se deduplican por su índice dentro de cada ventana (en el análisis exploratorio, por participante e índice), porque la exportación repite la duración del evento en cada muestra que le pertenece; sin ese paso, las duraciones se contarían varias veces. La duración que se suma es la del evento completo aunque se extienda fuera de la ventana; por eso la duración total de las fijaciones supera los 2.000 ms en el 27,8 % de las 25.992 ventanas del archivo *(calculado desde `caracteristicas_multimodales.csv`)*, en el 27,7 % de las 22.211 de las 41 personas, y los 3.000 ms en el 4 % de estas últimas, con un máximo de 11.365 ms (análisis descriptivo no registrado). La consecuencia es que el soporte temporal de dos de las variables que construyen la etiqueta de atención no es de 2 s: incluyen conducta ocular anterior y posterior a la ventana, lo que por sí solo puede acortar las duraciones al inicio de cada estímulo. En activación esas mismas variables son entradas del *Modelo Estudiante* y arrastran mirada posterior a la ventana. No se interpolan las pérdidas de mirada ni se corrigen los parpadeos. La calibración declarada (`Eyetracker Calibration`) se excluye, y ninguna ventana atraviesa un cambio de estímulo. Una ventana es válida si su cobertura de mirada es de al menos 50 %.

**Limitación conocida del procesamiento.** El índice que entrega Tobii es propio de cada tipo de evento, de modo que una fijación y una sacada pueden llevar el mismo número. La deduplicación usa solo el índice y no el tipo: cuando una fijación y una sacada con el mismo número coinciden en una ventana, se cuenta una sola. En una muestra de 5.918 ventanas (P1 a P11) se pierde así cerca de 0,2 % de las fijaciones. El efecto es pequeño y no se corrigió, porque el código y los resultados están congelados.

> Nota de trabajo (no va en la tesis): las duraciones sobre 3.000 ms y el máximo son la comprobación `c09` de la auditoría de código del 26-11-2026. La pérdida de fijaciones se recalculó desde la exportación cruda (`repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/ronda2/AUDITORIA_SECCIONES_PENDIENTES.md`).

En el diseño, el eye tracking construye junto con la pupilometría la etiqueta de atención y es entrada del *Modelo Estudiante* de activación. Mide lo **Observado**: indica hacia dónde se dirigió la mirada, no que ese contenido haya sido **Atendido**.

Fuentes: `documentos/01 Tesis MDS/Analisis de Datos/PREPROCESAMIENTO_MULTIMODAL.md`; `documentos/01 Tesis MDS/Analisis de Datos/EDA_EYE_PUPIL.md` (deduplicación del análisis exploratorio y cautelas); `repos/Tesis_MDS/scripts/preprocesamiento_secuencial.py` (deduplicación por ventana); `repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/ronda2/AUDITORIA_SECCIONES_PENDIENTES.md` (pérdida de fijaciones, recalculada desde la exportación cruda); `documentos/01 Tesis MDS/Analisis de Datos/DOCUMENTACION_DATOS_MDS.md` (columnas y filtro I-VT); `repos/Tesis_MDS/resultados/preprocesamiento/configuracion_efectiva.json`; `documentos/01 Tesis MDS/Marco Teorico/Atencion.md` (Observado y Atendido).

### 4.6.5 Preprocesamiento Pupilometría

Se usan solo los diámetros que el equipo marca como válidos. Los dos ojos se combinan mediante su media; si solo uno es válido, se usa ese. La interpolación lineal rellena hasta 12 filas consecutivas sin dato (0,2 s nominales a 60 Hz) dentro de huecos interiores. En un hueco más largo se rellenan solo sus primeras 12 filas. El límite se cuenta sobre todas las filas de la exportación, incluidas las de GSR, por lo que en tiempo es algo menor que 0,2 s. La serie se estandariza por sesión, excluida la calibración, y una ventana es válida si su cobertura es de al menos 50 %.

**Limitación conocida del procesamiento.** El número de muestras de pupila (`pupil_n`) y la fracción con ambos ojos válidos (`pupil_both_valid_fraction`) se calculan sobre todas las filas de la exportación que caen en la ventana, incluidas las de GSR y las de eventos, que no traen dato de pupila, y no solo sobre las muestras del seguidor ocular. Por eso la fracción queda bajo la validez real (0,755 frente a 0,942 en una ventana de ejemplo de P1) y `pupil_n` promedia 164,4 filas por ventana frente a las 120 muestras esperadas a 60 Hz. Además, al preparar la GSR y la pupila se conserva la primera fila de cada marca de tiempo; si una fila de otro sensor comparte la marca con la del ojo, puede desplazarla. No se cuantificó. La cobertura de pupila cuenta también las filas de otros sensores que la interpolación rellena. Esa fracción es una de las seis variables de pupila que recibe el *Modelo Estudiante* de activación. Tampoco se corrigió, por el mismo motivo que en la sección 4.6.4.

**No se corrige por luminancia.** El diámetro pupilar responde al brillo de lo que se mira, y en navegación web ese brillo cambia con cada página y con cada zona de la pantalla. La corrección propuesta en las notas de diseño, que consiste en estimar la luminancia en el punto de mirada y quedarse con el residuo, requiere una serie de luminancia sincronizada que no existe en los datos. Queda como limitación declarada: la componente pupilar del *Attention Score* puede reflejar en parte el brillo del estímulo y no solo carga cognitiva. Como en la GSR, la estandarización por sesión usa información de toda la sesión.

Fuentes: `documentos/01 Tesis MDS/Analisis de Datos/PREPROCESAMIENTO_MULTIMODAL.md`; `repos/Tesis_MDS/resultados/preprocesamiento/configuracion_efectiva.json` (0,2 s y cobertura 50 %); `repos/Tesis_MDS/scripts/preprocesamiento_secuencial.py` (combinación de ojos, interpolación y cálculo de `pupil_n` y de la fracción con ambos ojos válidos); `documentos/01 Tesis MDS/Diseno Metodologico/Modelo Profesor - Decisiones.md` (§1.1, propuesta de corrección no confirmada con el profesor); `repos/Tesis_MDS/resultados/modelado/manifiesto_etiquetas.json` (nota "Pupila sin corrección lumínica").

### 4.7 Extracción de Características

La unidad de análisis es la ventana de 2 s con paso de 1 s (50 % de solapamiento), definida dentro de cada segmento de estímulo. La tabla resultante tiene 25.992 ventanas de 48 participantes y 59 columnas: 10 de identificación y tiempo, 44 de señal y 5 indicadores de validez.

| Señal | Variables por ventana |
|---|---|
| GSR | Número de muestras y cobertura; media, desviación, mínimo y máximo estandarizados; nivel tónico medio; componente fásica media; pendiente; número de SCR; prominencia media de las SCR |
| Pupilometría | Número de filas de la exportación en la ventana y cobertura; fracción de esas filas con ambos ojos válidos; media, desviación, mínimo y máximo estandarizados; pendiente (las dos primeras tienen la limitación descrita en la sección 4.6.5) |
| Eye tracking | Número de muestras y cobertura; dispersión horizontal, vertical y conjunta de la mirada; longitud del recorrido; número, duración total, media y mediana de las fijaciones; número y duración media de las sacadas |
| EEG (resumen de los 16 canales) | Número de muestras y cobertura; valor cuadrático medio, desviación y rango pico a pico; potencia relativa en delta (1–4 Hz), theta (4–8 Hz), alfa (8–13 Hz), beta (13–30 Hz) y gamma (30–45 Hz); razón de ruido de línea; estado del emparejamiento y de la calidad de la sesión |

Las potencias de este resumen se calculan con la transformada rápida de Fourier y ventana de Hann, tras restar la mediana de cada canal.

**EEG por canal.** Desde el 29-10-2026 los modelos usan además una representación que conserva los 16 canales por separado. Dentro de cada ventana se elimina la tendencia lineal, se aplica un filtro *notch* de 50 Hz y un pasa-banda Butterworth de orden 4 entre 1 y 45 Hz, y se estima el espectro con el método de Welch. El filtro se aplica a cada ventana por separado: no mezcla información entre ventanas, pero en 2 s deja efectos de borde y una resolución pobre en las frecuencias más bajas, que no se evaluaron. Por canal se obtienen la potencia logarítmica y la relativa en las cinco bandas, la entropía, la frecuencia media y el borde espectral, los parámetros de Hjorth, medidas de amplitud e indicadores de calidad. Se agregan seis variables comunes a la ventana (muestras, cobertura, hueco máximo, canales utilizables, correlación media entre canales y fracción dominante de la covarianza), hasta completar 342 variables. Un canal se marca ausente en una ventana si tiene menos de 95 % de valores finitos, más de 1 % de muestras saturadas, 99 % o más de diferencias planas, menos de 200 muestras o huecos mayores de 0,1 s. Estas reglas se fijaron antes de observar el resultado de los modelos; los canales ausentes generan variables faltantes, que se imputan solo con datos de entrenamiento.

No se asigna anatomía a los canales en esta extracción: el montaje de los electrodos no está documentado. Una comprobación del 23-11-2026 mostró que los artefactos oculares se distribuyen como corresponde al montaje por defecto del equipo, lo que es coherente con distinguir zonas, pero no reemplaza la documentación del experimento.

**Qué recibe cada Modelo Estudiante.** La regla de no-circularidad se aplica al elegir las columnas: ninguna señal que construye una etiqueta se usa para predecirla.

| Tarea | Señales que construyen la etiqueta (*Modelo Profesor*) | Señales que la predicen (*Modelo Estudiante*) |
|---|---|---|
| Atención | Eye tracking y pupilometría | EEG y GSR |
| Activación | GSR | EEG, eye tracking y pupilometría |

El *Modelo Estudiante* de atención recibe 360 variables por ventana (351 de EEG y 9 de GSR) y el de activación 367 (351 de EEG, 10 de eye tracking y 6 de pupilometría). Las 351 de EEG son las 342 por canal y 9 del resumen. De GSR, eye tracking y pupilometría no reciben los conteos de muestras ni las coberturas. La cobertura mínima del EEG es 80 %.

La regla separa señales, no fuentes fisiológicas. El EEG registra también la actividad eléctrica de los movimientos oculares, de modo que la separación por señal no asegura independencia entre el EEG y la conducta ocular con que se define la atención. Ese punto se trata en la discusión.

Las variables de historial, que resumen las ventanas anteriores del mismo estímulo, pertenecen al modelamiento y están descritas en [[Borrador Resultados y Discusión 23-11-2026]], sección 6.2.

> [!warning] Diferencia con el esqueleto
> La subsección "Preprocesamiento EEG" de [[Estructura Tesis]] describe otro procesamiento: pasa-banda de 1 a 40 Hz, descarte de muestras sobre ±150 µV, bandas delta desde 0,5 Hz y gamma hasta 40 Hz, y 273 características por época. Ese texto proviene de la presentación de avances y no coincide con lo implementado. No se modificó; debe revisarse.

Fuentes: `repos/Tesis_MDS/resultados/preprocesamiento/caracteristicas_multimodales.csv` (59 columnas, 25.992 filas; SHA-256 actual `dc51dc19…`, mismo contenido que el del manifiesto del 22-08-2026 con otros finales de línea, comprobado para este borrador); `repos/Tesis_MDS/resultados/preprocesamiento/configuracion_efectiva.json` (bandas y coberturas); `documentos/01 Tesis MDS/Analisis de Datos/PREPROCESAMIENTO_MULTIMODAL.md`; `repos/Tesis_MDS/scripts/preprocesamiento_secuencial.py` (resta de la mediana por canal y ventana de Hann); `repos/Tesis_MDS/documentacion/Crudos_V2_y_EEG_Por_Canal_29-10-2026.md` y `repos/Tesis_MDS/resultados/eeg_por_canal_v2_29-10-2026/verificacion.json` (342 variables); `repos/Tesis_MDS/resultados/cierre_v3_16-11-2026/protocolo.json` (lista de variables por tarea); `repos/Tesis_MDS/resultados/montaje_ocular_41p_23-11-2026/INFORME.md`; `repos/Tesis_MDS/documentacion/Cierre_Experimental_Final_23-11-2026.md` (límite de la regla de no-circularidad).

### 4.8.2 División de Datos

**Unidad de partición.** Los datos se dividen por participante. Con 50 % de solapamiento, dos ventanas vecinas de una misma persona comparten la mitad de su señal; repartirlas entre ajuste y evaluación inflaría el desempeño. Ninguna persona aparece a la vez en ambos lados de una comparación.

**Partición congelada.** El 22-08-2026 se fijó una partición por participante, estratificada por grupo experimental. El orden dentro de cada grupo lo define el hash SHA-256 de una semilla fija y el identificador del participante, de modo que la asignación es reproducible y no depende de los resultados.

| División | Participantes | Uso |
|---|---:|---|
| Entrenamiento | 25 | Ajuste de modelos y de transformaciones; selección de hiperparámetros |
| Validación | 8 | Comparación de modelos |
| Prueba | 8 | Evaluación fuera de muestra |
| Sensibilidad | 1 (P29) | Efecto del desfase por revisar |
| Excluidos | 6 | P1, P7, P14, P17, P25 y P42 |

Cada uno de los cuatro grupos experimentales aporta dos personas a validación y dos a prueba. Las 41 personas del análisis principal suman 22.211 ventanas: 13.524 de entrenamiento, 4.662 de validación y 4.025 de prueba.

> Nota de trabajo (no va en la tesis): la semilla de la partición es `20260822`.

**Selección de hiperparámetros.** Se hace dentro del entrenamiento. Las 25 personas se organizan en cinco grupos de evaluación; en cada uno, las 20 personas de ajuste se dividen a su vez en 16 de ajuste interno y 4 de validación interna, que es donde se eligen los hiperparámetros. La imputación y el escalamiento de los modelos se ajustan solo con las personas de ajuste de cada grupo.

**Diseño del análisis final.** Validación y prueba, de 8 personas cada una, se consultaron más de una vez entre el 29-10 y el 16-11-2026, por lo que dejaron de ser una evaluación independiente. Desde el 16-11-2026 el análisis principal se hace de otro modo: la configuración elegida solo con las 25 personas de entrenamiento se congela y se evalúa con validación cruzada agrupada por persona sobre las 41 (8 grupos); desde el 22-11-2026 esa validación cruzada se repite en 5 particiones y la medida de cada persona se promedia entre ellas. Esto estima los efectos con más precisión, pero **no es una confirmación independiente**: una confirmación requeriría personas nuevas.

**Lo que no se ajusta solo con entrenamiento.** Tres elementos usan información que excede el conjunto de entrenamiento y deben declararse:

- Las pseudoetiquetas se normalizan y discretizan con la sesión completa de cada persona, incluidas las personas evaluadas. Describen el estado relativo de cada persona en su sesión y se calculan offline.
- Las variables de GSR y de pupila están estandarizadas por sesión (secciones 4.6.3 y 4.6.5).
- El *Modelo Profesor* de atención utilizado es la primera componente principal ajustada con las 25 personas de entrenamiento. En la validación cruzada sobre 41 personas eso introduce una fuga leve de etiquetas; al reajustarlo sin las personas evaluadas, el contraste principal de atención pasa de +0,026 a +0,024.

Otros tres límites del diseño de evaluación deben declararse junto a los anteriores:

- El diseño con 41 personas se adoptó el 16-11-2026, después de ver que el cierre V3, con las particiones originales, no mostraba una ventaja consistente del modelo con historial. Es un cambio de diseño posterior a los datos.
- La configuración se eligió con 25 de las 41 personas que luego se evalúan. El número de hojas se eligió por la AUC media de los modelos con 1, 8 y 32 ventanas de contexto, y en activación la elección de 15 hojas la decidió el de 32 (0,5311 frente a 0,4994 con 7 hojas). Eso permite un sesgo a favor del historial en esas 25 personas, que no está demostrado; el detalle por grupo de personas está en [[Borrador Resultados y Discusión 23-11-2026]], sección 7.5.
- Las personas de un mismo grupo experimental vieron los estímulos en el mismo orden (sección 4.3). La validación cruzada separa personas, no grupos: un modelo puede aprender regularidades ligadas a la secuencia de páginas a partir de otras personas del mismo grupo. No se evaluó dejando grupos completos fuera.

> [!warning] Diferencia con el esqueleto
> [[Estructura Tesis]] (1.6 Alcances y limitaciones) y [[Problema e hipótesis]] dicen que la normalización y los umbrales se estiman sin usar el conjunto de evaluación; la sección 4.2 dice que las transformaciones aprendidas, incluido el PCA, se ajustan dentro del entrenamiento, aunque ya declara la normalización por sesión. Eso vale para la imputación, el escalamiento y los hiperparámetros de los modelos, pero no para las pseudoetiquetas ni para las variables estandarizadas por sesión. El protocolo del 06-11-2026 ya pide reconciliar esa redacción.

Fuentes: `repos/Tesis_MDS/resultados/modelado/particion_participantes.csv` y `manifiesto_etiquetas.json`; `documentos/01 Tesis MDS/Analisis de Datos/ETIQUETAS_Y_BASELINES.md` (partición congelada; sus etiquetas y resultados son históricos); `repos/Tesis_MDS/resultados/profesor_binario_reconstruido_29-10-2026/protocolo.json` (cinco grupos y validación interna); `repos/Tesis_MDS/resultados/cierre_v3_16-11-2026/INFORME.md` y `protocolo.json`; `repos/Tesis_MDS/resultados/cierre_final_41p_16-11-2026/INFORME.md` y `protocolo.json` (8 grupos sobre 41 personas); `repos/Tesis_MDS/resultados/cierre_robustez_41p_16-11-2026/INFORME.md` (+0,024 sin fuga); `repos/Tesis_MDS/resultados/reapertura_41p_22-11-2026/INFORME.md` (5 particiones); `repos/Tesis_MDS/resultados/protocolo_hipotesis_reintento_06-11-2026/INFORME.md`; conteos de ventanas *calculados desde* `caracteristicas_multimodales.csv` y la partición.

### 4.8.3 Métricas de Evaluación

**Medida de desempeño.** Las dos pseudoetiquetas vigentes son binarias. La medida de decisión es el área bajo la curva ROC (característica operativa del receptor; AUC), calculada por persona y promediada entre personas; un valor de 0,5 equivale al azar. En el cierre V3 del 16-11-2026, con las particiones originales, se informan además, de forma descriptiva y con umbral fijo de 0,5, la exactitud balanceada (BA, *balanced accuracy*), el macro-F1 y el *recall* por clase. El análisis con 41 personas del 16-11-2026 agrega solo la BA, y los análisis del 22 y 23-11-2026 informan únicamente AUC.

**Unidad de inferencia.** Es la persona, no la ventana. Para comparar dos modelos se calcula, en cada persona, la diferencia entre sus AUC, y se resume la media de esas diferencias junto con el número de personas que mejoran. Las ventanas, las semillas y los grupos de la validación cruzada no aumentan el tamaño de muestra. Esta inferencia tiene límites que deben declararse (intervalo percentil con 41 personas y dependencia entre las AUC por persona de una validación cruzada); están en la sección 6.4 de [[Borrador Resultados y Discusión 23-11-2026]].

**Incertidumbre.** Los intervalos de confianza de 95 % y de 90 % se obtienen por *bootstrap* percentil de personas (20.000 réplicas, con la misma semilla en todos los contrastes). El valor p proviene de una prueba de permutación de signos bilateral (200.000 permutaciones). Los contrastes principales de cada análisis se corrigen con el método de Holm; los secundarios se informan sin corrección y se presentan como descriptivos.

**Reglas de decisión.** Rigen desde el análisis con 41 personas del 16-11-2026 y se fijaron antes de ejecutar cada análisis, incluido ese; el margen práctico se propuso el 06-11-2026, después de varias rondas de resultados:

| Decisión | Condición |
|---|---|
| Respaldo | p de Holm menor que 0,05 y límite inferior del intervalo de 95 % mayor que 0 |
| Efecto relevante | Además, límite inferior del intervalo de 95 % mayor que el margen práctico |
| Nulo concluyente | Intervalo de 90 % contenido entre menos y más el margen práctico |
| Inferior | Límite superior del intervalo de 95 % menor que 0 |
| Inconcluso | Cualquier otro caso |

El código aplica las reglas con la precedencia respaldo, inferior, nulo concluyente; los protocolos las listan sin fijarla. Ocho filas, todas de atención, cumplen dos reglas a la vez: seis quedan como "inferior" y dos como "respaldo", y todas cumplen también "nulo concluyente".

El margen práctico usado es 0,02 de AUC. **Es una propuesta sin justificación independiente y sin aprobación del profesor guía.** La hipótesis original plantea superioridad, es decir, una diferencia mayor que 0; descartar una mejora de al menos 0,02 no equivale a descartar toda mejora, y por eso se informa siempre la relación del intervalo con cero. El nulo del historial en atención no depende de este margen (sección 8.2 de [[Borrador Resultados y Discusión 23-11-2026]]).

**Registro previo.** Desde el 16-11-2026 el protocolo de cada etapa con modelos, con sus contrastes y reglas, se fijó antes de obtener sus predicciones y cada etapa se ejecutó una sola vez, salvo la primera versión del cierre V3, que se detuvo por una revisión de código. No hay un registro externo con sello de tiempo: esto ordena el trabajo, pero no equivale a un prerregistro. Los análisis añadidos después de ver resultados se identifican como post hoc, y los que se registraron motivados por un resultado ya visto, como dirigidos (sección 6.6 de [[Borrador Resultados y Discusión 23-11-2026]]).

> Nota de trabajo (no va en la tesis): el protocolo de cada etapa entró al repositorio antes que sus predicciones (orden de commits verificado; los commits están en `repos/Tesis_MDS/documentacion/Cierre_Experimental_Final_23-11-2026.md`).

**Criterio para la hipótesis.** Se usan los criterios de interpretación de [[Problema e hipótesis]]: evidencia a favor si los modelos temporales superan a los estáticos en atención y en emociones (operacionalizadas aquí como activación, alcance que el profesor guía aún no confirma); apoyo parcial si la ventaja aparece en una sola de las dos; sin evidencia si no aparece en ninguna. Una diferencia entre estrategias de fusión es un resultado comparativo y no demuestra por sí sola la hipótesis.

Este criterio compara desempeño y no dice de dónde debe provenir la ventaja. La discusión (sección 8.1 de [[Borrador Resultados y Discusión 23-11-2026]]) llega a "apoyo parcial" con una lectura más exigente, que pide además que la ventaja provenga de las ventanas previas; leído al pie de la letra y con el análisis de 41 personas, el criterio escrito daría otra respuesta, porque la ventaja de desempeño aparece en las dos variables; con las particiones originales no aparecía de forma consistente en ninguna. Cuál de las dos lecturas corresponde no está resuelto: es parte de la decisión abierta sobre el encuadre.

> [!warning] Diferencia con el esqueleto
> La sección "Metodología KDD" de [[Estructura Tesis]] dice que se informan BA, macro-F1 y *recall* por clase; esa redacción es de septiembre, cuando las etiquetas tenían tres clases. Con las etiquetas binarias la decisión se toma con AUC por persona, y las otras tres medidas quedaron como descriptivas y solo están calculadas en el cierre V3 (el análisis con 41 personas conserva la BA). Queda por decidir cuál se presenta como métrica principal en el manuscrito.

Fuentes: `repos/Tesis_MDS/resultados/cierre_final_41p_16-11-2026/protocolo.json` (inferencia y reglas de decisión) e `INFORME.md`; `repos/Tesis_MDS/resultados/cierre_v3_16-11-2026/protocolo.json` (métricas y umbral 0,5); `repos/Tesis_MDS/resultados/protocolo_hipotesis_reintento_06-11-2026/INFORME.md` y `protocolo.json` (margen 0,02 como propuesta; unidad de análisis); `repos/Tesis_MDS/documentacion/Cierre_Experimental_Final_23-11-2026.md` (registro previo y trazabilidad); `documentos/01 Tesis MDS/Marco Teorico/Problema e hipótesis.md` (criterios de interpretación).

---

## Capítulo 5: Análisis Exploratorio de Datos

> [!note] Sección agregada
> El Capítulo 5 del esqueleto no tiene secciones marcadas como pendientes, pero solo describe el EEG. La sección siguiente es un **complemento propuesto**, con título nuevo, que cubre las cuatro señales. Si no corresponde, puede omitirse sin afectar al resto.

### 5.3 Calidad y disponibilidad por señal (complemento propuesto)

El análisis exploratorio se hizo sobre los archivos originales, sin filtrar ni imputar, y por separado para cada señal. Los criterios difieren entre señales, de modo que los porcentajes no son comparables entre sí.

| Señal | Unidad evaluada | Válido | Total | Porcentaje | Criterio |
|---|---|---:|---:|---:|---|
| EEG | Sesiones principales | 44 | 48 | 91,67 % | Saturación y repetición plana de 30 % o menos |
| GSR | Grabaciones Tobii | 47 | 49 | 95,92 % | Señal presente y controles temporales correctos |
| Pupilometría | Muestras del seguidor ocular | 1.973.941 | 2.187.110 | 90,25 % | Ambos ojos válidos a la vez |
| Eye tracking | Muestras del seguidor ocular | 2.077.373 | 2.187.110 | 94,98 % | Punto de mirada válido |

**EEG.** Las sesiones principales duran en promedio 13,4 minutos (desviación 1,5; mediana 13,1) *(calculado desde `eeg_resumen_sesiones.csv`; coincide con la cifra del esqueleto)*. La frecuencia efectiva, estimada desde las marcas de tiempo, tiene mediana de 125,14 Hz en las 104 sesiones (125,14 Hz también en las 48 principales), coherente con los 125 Hz nominales. El principal problema de calidad es la saturación: muestras en el límite del rango del equipo (±187.500 µV), que indican desconexión o ganancia inadecuada y no actividad cerebral. Se excluyen P17 (59,2 % de muestras saturadas), P1 (37,9 %), P14 (31,2 %) y P25 (36,0 % de repetición plana). P15 (26,2 %) y P16 (25,0 %) quedan bajo el umbral y permanecen en el análisis. El umbral de 30 % es permisivo y exploratorio, y los porcentajes se calcularon con una muestra sistemática de una de cada diez filas. La representación por canal de la sección 4.7 trata después la saturación ventana a ventana.

**GSR.** Hay 47 grabaciones con GSR y 530.407 muestras válidas, a unos 15 Hz, sin marcas de tiempo duplicadas ni desordenadas. P7 y P42 no tienen GSR en la exportación. Una de las 47 grabaciones es la de prueba, de modo que 46 de los 48 participantes tienen GSR. Las grabaciones tienen entre 2.040 y 14.615 muestras; el mínimo corresponde a P4 *(calculado desde `gsr_por_grabacion.csv`)*, que por eso aporta pocas ventanas con etiqueta de activación.

**Eye tracking y pupilometría.** De las 2.187.110 muestras de las 49 grabaciones (incluida la de prueba), 1.743.227 se clasifican como fijación, 311.735 como sacada, 104.102 como ojos no encontrados y 28.046 quedan sin clasificar. Se identifican 122.302 fijaciones, con duración mediana de 183 ms (percentiles 5 y 95: 83 y 516 ms). La validez varía entre personas: la fracción con ambos ojos válidos baja a 43,1 % en P6 y a 52,4 % en P41 *(calculado desde `calidad_por_participante.csv`)*. Ambas personas pertenecen al conjunto de validación.

**Ventanas resultantes.** El preprocesamiento produce 25.992 ventanas de 2 s en los 48 participantes, entre 414 y 757 por persona *(calculado desde `caracteristicas_multimodales.csv`)*. Tienen cobertura suficiente 24.541 en GSR, 25.964 en pupila, 25.887 en mirada y 25.958 en EEG. Cumplen a la vez todos los criterios 22.201, cifra que incluye las 482 de P29 y excluye por completo a las seis personas apartadas (21.719 en las 41 personas del análisis principal, que suman 22.211 ventanas en total).

Las figuras de este análisis están en `documentos/01 Tesis MDS/attachments/Analisis de Datos/`.

Fuentes: `repos/Tesis_MDS/resultados/resumen_calidad_fuentes.csv`; `documentos/01 Tesis MDS/Analisis de Datos/EDA_EEG.md`, `EDA_GSR.md`, `EDA_EYE_PUPIL.md`, `EDA_SENALES.md` y `RESUMEN_PROCESO.md` (sincronizadas al 22-08-2026); `repos/Tesis_MDS/resultados/eda/eeg/eeg_resumen_sesiones.csv` y `eeg_resumen.json`; `repos/Tesis_MDS/resultados/eda/gsr/gsr_por_grabacion.csv` y `resumen_gsr.json`; `repos/Tesis_MDS/resultados/eda/eye_pupil/movimientos_oculares.csv`, `resumen_fijaciones.csv` y `calidad_por_participante.csv`; `repos/Tesis_MDS/resultados/preprocesamiento/auditoria_participantes.csv` y `manifiesto_ejecucion.json`; `documentos/01 Tesis MDS/Analisis de Datos/PREPROCESAMIENTO_MULTIMODAL.md`.

---

## Secciones que siguen pendientes

Se listan las secciones marcadas *(pendiente)* en [[Estructura Tesis]] que **no** se redactaron aquí.

| Sección del esqueleto | Razón |
|---|---|
| 2.2 Emociones Humanas (Naturaleza, Evolución de las Teorías, Expresión, Clasificación) | Requiere literatura que no está en las notas. Solo hay una mención sin referencia verificada a Ekman y a Russell. |
| 2.3 Atención Humana (Definición, Tipos, Nivel, Entornos Digitales) | La única fuente es `Marco Teorico/Atencion.md`, que recoge un marco conceptual planteado por el profesor en una conversación (niveles Visible, Observado, Atendido, Comprendido), sin bibliografía. No se puede citar como teoría sin referencia. |
| 2.4 Señales Fisiológicas (Definición, Clasificación Sistema Nervioso, EEG, GSR) | Requiere literatura. `notas/sustento-fisiologico-23-11-2026.md` tiene 18 referencias, contrastadas con las fuentes el 23-11-2026 (10 en texto completo y 8 solo por resumen; detalle en `repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/VERIFICACION_REFERENCIAS.md`). Tratan de artefactos oculares y musculares en el EEG, de la respuesta electrodérmica y de la pupila, como apoyo a la discusión, no de las definiciones que pide la sección. |
| 2.5 KDD (descubrimiento de conocimiento en bases de datos) como Marco Teórico (Etapas; KDD aplicado a emociones) | La única fuente primaria consultada es Fayyad et al. (1996), ya usada en la sección 4.2. No hay literatura verificada sobre KDD aplicado a detección de emociones. |
| 2.6 EDA, análisis exploratorio de datos (Propósito, Visualización, Estadística Descriptiva, Distribución, Outliers, Correlación) | Requiere literatura; no hay referencias en las notas. |
| 2.7 Modelamiento: Propósito, Algoritmos Clásicos, Redes Neuronales, CNN, Transformers y ViT, Aprendizaje por Transferencia, Modelos Multimodales y Fusión, División de Datos y Validación Cruzada | Requiere literatura. Además, las subsecciones de CNN, ViT, aplicación a imágenes y transferencia parecen heredadas de una plantilla con expresión facial; conviene decidir si se mantienen. |
| 2.8 Evaluación de Modelos (Propósito, Matriz de Confusión, Métricas, Multiclase, ROC y AUC, Consideraciones) | Requiere literatura. La parte aplicada está en 4.8.3 de este borrador. |
| 2.9 Detección Automática de Emociones (cinco subsecciones) | Requiere literatura, y su título depende de la decisión abierta sobre presentar "emoción" como activación. |
| 2.10 Detección Automática de Atención (cinco subsecciones) | Requiere literatura. |
| 2.11 Consideraciones Éticas | No hay insumo: las notas no documentan consentimiento informado, comité de ética ni tratamiento de datos personales. |
| 2.12 Pseudo Etiquetas (marco teórico) | Solo hay una lista de riesgos en `Marco Teorico/Atencion.md`. El vínculo con co-training y aprendizaje multi-vista figura en el esqueleto como "fuera del vault, sin verificar". |
| 3.3 Pseudo etiquetas (estado del arte) | Requiere literatura; el esqueleto la marca como pendiente de desarrollo. |
| 4.3 Participantes (parte no redactada) | Faltan reclutamiento, criterios de inclusión, datos demográficos, consentimiento, comité de ética, criterio con que se armaron los grupos `SlowWeb G1` a `G4` (en los datos, cada grupo es un orden de presentación) y protocolo de estímulos. Hay que pedirlos al proyecto. |
| 4.4 Pupilometría: corrección por luminancia | No existe una serie de luminancia sincronizada ni está verificado que se conserven las páginas observadas. Se declara como limitación en 4.6.5. |
| 6 Modelamiento y Experimento; 7 Resultados; 8 Discusión; 9 Conclusiones | Fuera del alcance pedido. Ya existen borradores aparte: [[Borrador Resultados y Discusión 23-11-2026]] (capítulos 6 a 8; integra los resultados del 22 y 23-11 y reemplaza al del 18-11-2026, que se conserva), [[Borrador Discusión fisiológica 23-11-2026]] (integrado el 26-11-2026 en el capítulo 8 del anterior) y [[Borrador Conclusiones 23-11-2026]]. Todos dependen de decisiones abiertas con el profesor guía. |

### Secciones no pendientes cuyo texto quedó desactualizado

No se tocaron, porque no están marcadas como pendientes, pero no coinciden con lo implementado:

| Sección del esqueleto | Qué no coincide |
|---|---|
| 4.5.1 Definición Nivel de Atención | Dice "discretizado por persona" y deja abiertos la fusión y el umbral. La etiqueta usada desde el 29-10-2026 es binaria por mediana personal, con un *Modelo Profesor* de primera componente principal. Las notas de diseño proponían la fusión igualitaria como primaria y la componente principal como sensibilidad. En la componente principal la pupila pesa −0,052, frente a 0,40 a 0,56 de las cuatro variables de mirada: la etiqueta usada es, en la práctica, conducta de mirada, y no "mirada y pupila". Las dos versiones del *Modelo Profesor* (fusión igualitaria y componente principal) concuerdan en 66,28 % de las 13.498 ventanas de entrenamiento comparadas (kappa 0,3255), por lo que la elección importa y sigue abierta. Los análisis siguieron con la componente principal tras observar que los modelos la predecían mejor en entrenamiento; eso no es un argumento de validez, como advierte el propio informe del 29-10-2026. |
| 4.4 Fuentes de Información | Lista variables que el procesamiento ejecutado no calcula: relaciones entre bandas del EEG, amplitud y velocidad de las sacadas y dilatación pupilar relativa a una línea base (la pupila se estandariza por sesión). Lo implementado está en 4.7. |
| 4.6.2 Preprocesamiento EEG | Describe filtros, umbral de ±150 µV, bandas y 273 características que no corresponden al procesamiento ejecutado (ver 4.7). |
| 4.2 Metodología KDD y 1.6 Alcances y limitaciones | Afirman que la normalización se estima solo con entrenamiento y que se informa BA, macro-F1 y *recall* (ver 4.8.2 y 4.8.3). |
| 5.1 y 5.2 (Descripción General; Duración y Registros) | "21 de 48 participantes presentan al menos un canal saturado" y "NaN = 0" vienen de una presentación anterior y usan un criterio por canal distinto del criterio por sesión del análisis vigente (44 de 48). No se pudo reproducir esa cifra con las tablas actuales: con el criterio "algún canal toca el límite del equipo" las tablas actuales dan 37 de 48. |

## Notas relacionadas
- [[Estructura Tesis]]
- [[Problema e hipótesis]]
- [[Resumen Diseño Etiquetas y Modelos]]
- [[Etiqueta Atencion]] · [[Etiqueta Emocion]] · [[Modelo Profesor - Decisiones]]
- [[Borrador Resultados y Discusión 23-11-2026]] · [[Borrador Discusión fisiológica 23-11-2026]] · [[Borrador Conclusiones 23-11-2026]]
