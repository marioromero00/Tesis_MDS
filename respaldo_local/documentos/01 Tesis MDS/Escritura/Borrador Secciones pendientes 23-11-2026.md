# Borrador: secciones pendientes con insumo documentado

> [!info] Estado
> Borrador redactado el 23-11-2026 a pedido de Mario. **No reemplaza a [[Estructura Tesis]]**: las secciones que aquí se redactan siguen marcadas como *(pendiente)* en el esqueleto hasta que él las revise. **No hay aprobación registrada del profesor guía** sobre este texto. Complementa a [[Borrador Resultados y Discusión 18-11-2026]], [[Borrador Discusión fisiológica 23-11-2026]] y [[Borrador Conclusiones 23-11-2026]]. No se entrenó ningún modelo ni se modificó ningún archivo existente para escribirlo.

> [!warning] Decisiones abiertas que este texto no cierra
> Las cinco decisiones con checkbox de [[Resumen Diseño Etiquetas y Modelos]] siguen abiertas: (1) método de fusión y umbral de discretización del *Attention Score*; (2) combinación de variables de GSR y umbral del *Arousal Score*; (3) ventana de agregación específica para GSR; (4) si redefinir "emoción" como activación (*arousal*) es aceptable para el alcance de la hipótesis; (5) si existe alguna fuente de validación externa para las etiquetas. Donde este borrador describe una etiqueta, describe **la operacionalización que se usó en los experimentos**, no una decisión tomada. Lo único registrado sobre el profesor guía es que Mario comunicó el 01-11-2026 que aprobó usar las pseudoetiquetas GSR V2 (`notas/bitacora.md`); eso no marca ningún checkbox ni equivale a una validación externa.

> [!note] Cómo leer este borrador
> - **Numeración.** El esqueleto no trae números; se usa el orden de sus títulos (capítulo.sección.subsección), que es el que produciría LaTeX.
> - **Rutas.** Las fuentes se dan relativas a `/Users/mario/Proyectos/tesis-mds/`.
> - **Versiones.** La tabla de características por ventana (`caracteristicas_multimodales.csv`) y la partición por participante son del 22-08-2026 y **siguen vigentes**: todos los análisis posteriores las leen. Las **etiquetas** del 22-08-2026 (tres clases) **no** están vigentes: las vigentes son la atención binaria reconstruida del 29-10-2026 y las pseudoetiquetas GSR V2 del 01-11-2026. Cada cifra indica a qué versión pertenece.
> - **Cifras calculadas para este borrador.** Algunas no aparecen escritas en ningún informe y se obtuvieron contando o resumiendo una tabla existente; van marcadas como *(calculado desde …)*.

---

## Capítulo 1: Introducción

### 1.4 Preguntas de Investigación

Las preguntas se derivan de la hipótesis y de los objetivos específicos 2 a 7, sin modificar su alcance. El objetivo 1 (revisión de literatura) no origina una pregunta propia.

1. **Temporalidad.** ¿Obtienen los modelos temporales multimodales un mejor desempeño fuera de muestra que los modelos estáticos comparables al predecir las pseudoetiquetas de atención y de activación durante la navegación web, en participantes no usados para su ajuste? *(Hipótesis; objetivos 4 y 7.)*
2. **Fusión y aporte de las señales.** ¿Cuánto aportan al desempeño cada señal y el historial de ventanas anteriores, y cambia ese desempeño entre fusión temprana, intermedia y tardía? *(Objetivo 5.)*
3. **Pseudoetiquetas.** ¿Es posible definir pseudoetiquetas continuas y categóricas de atención y de activación a partir de señales distintas de las que luego las predicen, con registros sincronizados bajo criterios de calidad definidos, y qué tan estables son esas pseudoetiquetas frente a decisiones razonables de construcción? *(Objetivos 2 y 3.)*
4. **Evolución durante la sesión.** ¿Cómo cambian el *Attention Score* y el *Arousal Score* a lo largo de la sesión, y son esos cambios compatibles con fatiga o habituación? *(Objetivo 6; pregunta descriptiva.)*

Tres precisiones de alcance. Primero, la pregunta 1 es la única que contrasta la hipótesis; las preguntas 2 a 4 no son hipótesis adicionales. Segundo, la hipótesis habla de "emociones" y estas preguntas hablan de activación (*arousal*): esa redefinición es una propuesta de alcance que el profesor guía aún no confirma. Tercero, la pregunta 3 se refiere a la estabilidad de las reglas de etiquetado; no a la validez externa de los constructos, que este diseño no permite establecer.

Fuentes: `documentos/01 Tesis MDS/Escritura/Estructura Tesis.md` (hipótesis y objetivos, formulación del 22-09-2026); `documentos/01 Tesis MDS/Marco Teorico/Problema e hipótesis.md` (operacionalización, criterios de interpretación y análisis complementario); `documentos/01 Tesis MDS/Marco Teorico/Referencia Tesis Previas.md` (uso de preguntas de investigación en tesis previas del grupo).

---

## Capítulo 4: Metodología

### 4.3 Participantes

> [!warning] Sección parcial
> Las notas solo permiten describir cuántas personas hay y cómo se seleccionaron para el análisis. **No hay insumo** sobre reclutamiento, criterios de inclusión, edad, sexo, consentimiento informado ni comité de ética; tampoco sobre el significado de los grupos experimentales ni el protocolo de estímulos. Esos párrafos quedan por escribir con información del proyecto.

La Toma de Muestra 2 registra 48 participantes, identificados como P1 a P48, con una sesión principal cada uno. Las grabaciones se realizaron entre el 8 y el 30 de agosto de 2025 *(calculado desde `coordinacion_sesiones.csv`)*. La exportación del seguidor ocular contiene además una grabación de prueba (`Test_Participant`), que no corresponde a un participante y no se usa.

Cada participante pertenece a uno de cuatro grupos experimentales, registrados en la exportación como `SlowWeb G1` a `SlowWeb G4`, con 13, 12, 12 y 11 personas respectivamente *(calculado desde `coordinacion_sesiones.csv`)*. Las notas no documentan qué distingue a los grupos; aquí solo se usan para estratificar la partición (sección 4.8.2).

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

**Por qué activación.** La Toma de Muestra 2 no tiene expresión facial. De sus cuatro señales, la respuesta galvánica de la piel (GSR, *galvanic skin response*) registra activación simpática y no informa valencia ni permite identificar emociones discretas. Una etiqueta de valencia exigiría usar el EEG, que es señal de entrada del *Modelo Estudiante*, o la expresión facial, que no existe en este conjunto de datos. Por eso la variable objetivo se limita a un solo eje, la activación, y se nombra así en todo el documento.

**Modelo Profesor y Modelo Estudiante.** El *Modelo Profesor* de activación usa únicamente GSR y produce el *Arousal Score*. El *Modelo Estudiante* lo predice con EEG, eye tracking y pupilometría. Se cumple la regla de no-circularidad: **ninguna señal que construye una etiqueta se usa para predecirla**; la GSR no aparece entre las entradas del estudiante de activación. Eye tracking y pupilometría construyen la etiqueta de atención, pero aquí actúan solo como predictores de otra etiqueta.

**Construcción del *Arousal Score*.** Se calcula por ventana de 2 s con paso de 1 s, a partir de la tabla de características de la sección 4.7:

1. *Control de calidad.* Una ventana es válida si su cobertura de GSR es de al menos 50 %, si sus cuatro componentes son finitos y si los conteos de respuestas no son negativos.
2. *Componentes.* Nivel tónico medio, componente fásica media, número de respuestas de conductancia (SCR, *skin conductance responses*) y prominencia media de las SCR.
3. *Normalización.* Cada componente se estandariza dentro de la persona usando solo sus ventanas válidas. Un componente constante aporta cero; un componente ausente no se rellena.
4. *Score de 2 s.* Promedio de los cuatro componentes estandarizados, vuelto a estandarizar dentro de la persona.
5. *Score de 6 s.* Promedio del score de 2 s sobre cinco ventanas consecutivas válidas, lo que equivale a 6 s de señal, estandarizado otra vez dentro de la persona. La secuencia se reinicia al cambiar de participante, grabación, segmento o estímulo, ante una ventana inválida o ante un hueco. Es causal: usa la ventana actual y las cuatro anteriores.
6. *Discretización.* La versión categórica es binaria: activación alta si el score de 6 s supera la mediana de la persona, baja si queda por debajo. Los empates con la mediana (tolerancia 1e-8) quedan sin etiqueta en vez de asignarse a una clase.

El score continuo se conserva junto a la etiqueta binaria, como exige el objetivo 6.

**Qué resulta.** De las 22.211 ventanas de las 41 personas del análisis principal, 11.796 quedan etiquetadas (53,1 %): 7.028 en las 25 personas de entrenamiento, 2.584 en las 8 de validación y 2.184 en las 8 de prueba. Las 10.415 restantes se pierden por historial insuficiente (9.995), por cobertura o indicador de calidad inválido (401) y por empate con la mediana (19). La mayor pérdida proviene de exigir cinco ventanas consecutivas dentro de un mismo estímulo, no de mala calidad de la GSR. Las 41 personas conservan ambas clases; el equilibrio entre clases (5.898 y 5.898) es consecuencia del umbral por mediana y no dice nada sobre su validez. P4 conserva solo 26 de sus 459 ventanas, porque apenas 58 tienen GSR válida.

**Por qué V2.** La auditoría del 02-11-2026 encontró un error de alineación de índices en el generador anterior de etiquetas (`scripts/preparar_modelado.py`): 25.498 de 25.992 posiciones de componentes quedaban desplazadas. Las métricas de activación calculadas con esas etiquetas no permiten respaldar ni rechazar la hipótesis. La versión V2 asigna por índice, se reprodujo de forma independiente con tolerancia 1e-12 y es la única que se usa en los resultados.

**Límites.** La normalización y la mediana usan la sesión completa de cada persona: la etiqueta es relativa a la sesión y se calcula offline, no sirve como detector en tiempo real. No se aplicó un desfase para compensar la latencia de las SCR (1 a 5 s); el contexto de 6 s cumple esa función de forma aproximada, y la ventana específica para GSR sigue siendo una decisión abierta. El control de calidad opera sobre variables derivadas, sin un detector de artefactos sobre la señal cruda. No existe una medida externa de activación contra la cual validar la etiqueta, y la unidad física de la GSR no está declarada en la exportación.

Fuentes: `repos/Tesis_MDS/resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md`, `protocolo.json`, `motivos.csv`, `resumen_personas.csv` y `auditoria_independiente_02-11-2026.json` de la misma carpeta; `repos/Tesis_MDS/scripts/reconstruir_etiquetas_gsr_calidad_v2.py` (pasos 3 a 6); `repos/Tesis_MDS/resultados/cierre_final_41p_16-11-2026/predicciones_activacion.csv.gz` (conteo por clase, *calculado para este borrador*); `documentos/01 Tesis MDS/Diseno Metodologico/Etiqueta Emocion.md` y `Resumen Diseño Etiquetas y Modelos.md` (justificación y decisiones abiertas); `notas/bitacora.md` (entradas del 01-11 y 02-11-2026).

### 4.6.1 Sincronización de Fuentes

Los registros provienen de dos sistemas sin una clave común. El seguidor ocular Tobii exporta en un solo archivo el eye tracking, la pupilometría y la GSR, que por lo tanto comparten reloj. El electroencefalograma (EEG) se registró con un equipo OpenBCI Cyton con módulo Daisy, en archivos separados por sesión. No existen marcas de sincronización compartidas por hardware (*triggers*) entre ambos sistemas.

**Dominio temporal común.** Todas las marcas de tiempo se llevan a tiempo universal coordinado (UTC). En Tobii, cada muestra se ubica sumando su tiempo relativo, en microsegundos, al inicio UTC de la grabación. En OpenBCI se usa la marca de tiempo de cada muestra: la hora local de los archivos de texto se interpreta como UTC−4, que corresponde a Chile en agosto de 2025, y la marca Unix de los archivos BrainFlow ya es absoluta. El desfase entre equipos se informa como inicio de Tobii menos inicio de EEG; un valor positivo indica que el EEG comenzó antes.

**Emparejamiento de sesiones.** El archivo de EEG contiene 104 carpetas de sesión: 48 principales, 51 de prueba y 5 sin identificador de participante *(calculado desde `eeg_resumen_sesiones.csv`)*. Para cada grabación Tobii se normaliza el identificador del participante, se restringen los candidatos a sesiones EEG de la misma persona y se elige la de inicio más cercano. Cuando una sesión tiene más de un archivo se usa el más largo, para evitar fragmentos de arranque. Cada par queda con un estado de revisión.

De las 49 grabaciones Tobii, 47 quedaron como candidatas directas. P29 quedó para revisión, porque su EEG comienza 329,9 s antes; la grabación de prueba no tiene pareja válida. Entre las 47 candidatas el desfase va de −79,6 s (P25, único caso en que Tobii comenzó antes) a +86,2 s, con mediana de 13,2 s *(calculado desde `coordinacion_sesiones.csv`)*.

**Deriva de los relojes.** No se estimó ni se corrigió. Estimarla exige al menos dos eventos observados de forma independiente en ambos equipos, y los eventos disponibles solo existen en Tobii. El procedimiento del cuaderno de referencia buscaba la muestra de EEG más cercana a cada evento Tobii, con lo que reutilizaba el mismo reloj que pretendía validar. El factor de escala se fija en 1,0, que significa "sin corrección identificable" y no "sin deriva".

**Ventanas comunes.** Las señales conservan su frecuencia nativa: cerca de 125 Hz el EEG, 60 Hz el eye tracking y la pupila, y 15 Hz la GSR. No se remuestrean a una frecuencia común. Las ventanas se definen en el reloj de Tobii y el EEG se recorta con los mismos límites en UTC.

**Precisión alcanzada.** La alineación es por reloj absoluto y no llega al nivel de muestra. Una comprobación del 23-11-2026, que compara el EEG con la mirada y los parpadeos registrados por el seguidor ocular, encontró que el EEG va atrasado entre 0,18 y 0,53 s en las 41 personas (mediana 0,45 s). Ese desfase no se corrigió, porque las ventanas ya estaban congeladas. Equivale a correr las ventanas de EEG entre 12 % y 25 % respecto de las otras señales: no invalida los resultados, pero atenúa cualquier relación entre el EEG y el resto, incluidas las etiquetas.

Fuentes: `documentos/01 Tesis MDS/Analisis de Datos/SINCRONIZACION_SENALES.md` y `DOCUMENTACION_DATOS_MDS.md` (sincronizadas al 22-08-2026; la tabla de coordinación sigue vigente); `repos/Tesis_MDS/resultados/sincronizacion/coordinacion_sesiones.csv`; `repos/Tesis_MDS/resultados/eda/eeg/eeg_resumen_sesiones.csv`; `documentos/01 Tesis MDS/Analisis de Datos/PREPROCESAMIENTO_MULTIMODAL.md` (frecuencias y recorte por UTC); `repos/Tesis_MDS/resultados/montaje_ocular_41p_23-11-2026/INFORME.md` (desfase empírico).

### 4.6.3 Preprocesamiento GSR

La GSR se lee de las filas del archivo Tobii cuyo sensor es `GSR`. Su frecuencia efectiva es cercana a 15 Hz en todas las grabaciones; el valor de 8 Hz del cuaderno de referencia no se confirmó en los datos. La unidad física no está declarada en la exportación, por lo que se trabaja con valores estandarizados y no se interpretan amplitudes absolutas.

El procesamiento es el siguiente:

1. La señal se estandariza por sesión.
2. La componente tónica se obtiene con un filtro Butterworth pasa-bajos de segundo orden a 0,05 Hz, y la fásica como la diferencia entre la señal y la tónica.
3. Las SCR se detectan como picos de la componente fásica con prominencia mínima de 0,05 unidades estandarizadas.
4. Para cada ventana de 2 s se calculan la cobertura y las variables de la sección 4.7. Una ventana es válida si su cobertura es de al menos 50 %.

Dos límites condicionan el uso posterior. La estandarización por sesión y el filtro tónico, que se aplica en ambos sentidos, usan información de toda la sesión: estas variables no son causales a nivel de muestra. Además, no se aplicó un detector de artefactos sobre la señal cruda.

En el diseño, la GSR es entrada del *Modelo Estudiante* de atención y fuente única del *Modelo Profesor* de activación. Por la regla de no-circularidad no se usa para predecir la activación.

Fuentes: `documentos/01 Tesis MDS/Analisis de Datos/PREPROCESAMIENTO_MULTIMODAL.md`; `repos/Tesis_MDS/resultados/preprocesamiento/configuracion_efectiva.json` (0,05 Hz, prominencia 0,05, cobertura 50 %); `documentos/01 Tesis MDS/Analisis de Datos/EDA_GSR.md` (frecuencia y unidad); `repos/Tesis_MDS/resultados/cierre_v3_16-11-2026/INFORME.md` (variables no causales por muestra).

### 4.6.4 Preprocesamiento Eye Tracking

El eye tracking se lee de las filas del sensor `Eye Tracker`, a una frecuencia cercana a 60 Hz. Se usan el punto de mirada en píxeles y la clasificación de movimientos oculares que entrega Tobii con su filtro I-VT (identificación por umbral de velocidad), que distingue fijaciones, sacadas, ojos no encontrados y muestras sin clasificar.

Los eventos se deduplican por su índice dentro de cada participante, porque la exportación repite la duración del evento en cada muestra que le pertenece; sin ese paso, las duraciones se contarían varias veces. No se interpolan las pérdidas de mirada ni se corrigen los parpadeos. La calibración declarada (`Eyetracker Calibration`) se excluye, y ninguna ventana atraviesa un cambio de estímulo. Una ventana es válida si su cobertura de mirada es de al menos 50 %.

En el diseño, el eye tracking construye junto con la pupilometría la etiqueta de atención y es entrada del *Modelo Estudiante* de activación. Mide lo **Observado**: indica hacia dónde se dirigió la mirada, no que ese contenido haya sido **Atendido**.

Fuentes: `documentos/01 Tesis MDS/Analisis de Datos/PREPROCESAMIENTO_MULTIMODAL.md`; `documentos/01 Tesis MDS/Analisis de Datos/EDA_EYE_PUPIL.md` (deduplicación y cautelas); `documentos/01 Tesis MDS/Analisis de Datos/DOCUMENTACION_DATOS_MDS.md` (columnas y filtro I-VT); `repos/Tesis_MDS/resultados/preprocesamiento/configuracion_efectiva.json`; `documentos/01 Tesis MDS/Marco Teorico/Atencion.md` (Observado y Atendido).

### 4.6.5 Preprocesamiento Pupilometría

Se usan solo los diámetros que el equipo marca como válidos. Los dos ojos se combinan mediante su media. Los huecos interiores de hasta 0,2 s se interpolan; los más largos no. La serie se estandariza por sesión, y una ventana es válida si su cobertura es de al menos 50 %.

**No se corrige por luminancia.** El diámetro pupilar responde al brillo de lo que se mira, y en navegación web ese brillo cambia con cada página y con cada zona de la pantalla. La corrección propuesta en las notas de diseño, que consiste en estimar la luminancia en el punto de mirada y quedarse con el residuo, requiere una serie de luminancia sincronizada que no existe en los datos. Queda como limitación declarada: la componente pupilar del *Attention Score* puede reflejar en parte el brillo del estímulo y no solo carga cognitiva. Como en la GSR, la estandarización por sesión usa información de toda la sesión.

Fuentes: `documentos/01 Tesis MDS/Analisis de Datos/PREPROCESAMIENTO_MULTIMODAL.md`; `repos/Tesis_MDS/resultados/preprocesamiento/configuracion_efectiva.json` (0,2 s y cobertura 50 %); `documentos/01 Tesis MDS/Diseno Metodologico/Modelo Profesor - Decisiones.md` (§1.1, propuesta de corrección no confirmada con el profesor); `repos/Tesis_MDS/resultados/modelado/manifiesto_etiquetas.json` (nota "Pupila sin corrección lumínica").

### 4.7 Extracción de Características

La unidad de análisis es la ventana de 2 s con paso de 1 s (50 % de solapamiento), definida dentro de cada segmento de estímulo. La tabla resultante tiene 25.992 ventanas de 48 participantes y 59 columnas: 10 de identificación y tiempo, 44 de señal y 5 indicadores de validez.

| Señal | Variables por ventana |
|---|---|
| GSR | Número de muestras y cobertura; media, desviación, mínimo y máximo estandarizados; nivel tónico medio; componente fásica media; pendiente; número de SCR; prominencia media de las SCR |
| Pupilometría | Número de muestras y cobertura; fracción con ambos ojos válidos; media, desviación, mínimo y máximo estandarizados; pendiente |
| Eye tracking | Número de muestras y cobertura; dispersión horizontal, vertical y conjunta de la mirada; longitud del recorrido; número, duración total, media y mediana de las fijaciones; número y duración media de las sacadas |
| EEG (resumen de los 16 canales) | Número de muestras y cobertura; valor cuadrático medio, desviación y rango pico a pico; potencia relativa en delta (1–4 Hz), theta (4–8 Hz), alfa (8–13 Hz), beta (13–30 Hz) y gamma (30–45 Hz); razón de ruido de línea; estado del emparejamiento y de la calidad de la sesión |

Las potencias de este resumen se calculan con la transformada rápida de Fourier y ventana de Hann, tras restar la mediana de cada canal.

**EEG por canal.** Desde el 29-10-2026 los modelos usan además una representación que conserva los 16 canales por separado. Dentro de cada ventana se elimina la tendencia lineal, se aplica un filtro *notch* de 50 Hz y un pasa-banda Butterworth de orden 4 entre 1 y 45 Hz, y se estima el espectro con el método de Welch. Por canal se obtienen la potencia logarítmica y la relativa en las cinco bandas, la entropía, la frecuencia media y el borde espectral, los parámetros de Hjorth, medidas de amplitud e indicadores de calidad. Se agregan medidas entre canales, hasta completar 342 variables. Un canal se marca ausente en una ventana si tiene menos de 95 % de valores finitos, más de 1 % de muestras saturadas, 99 % o más de diferencias planas, menos de 200 muestras o huecos mayores de 0,1 s. Estas reglas se fijaron antes de observar el resultado de los modelos; los canales ausentes generan variables faltantes, que se imputan solo con datos de entrenamiento.

No se asigna anatomía a los canales en esta extracción: el montaje de los electrodos no está documentado. Una comprobación del 23-11-2026 mostró que los artefactos oculares se distribuyen como corresponde al montaje por defecto del equipo, lo que respalda distinguir zonas, pero no reemplaza la documentación del experimento.

**Qué recibe cada Modelo Estudiante.** La regla de no-circularidad se aplica al elegir las columnas: ninguna señal que construye una etiqueta se usa para predecirla.

| Tarea | Señales que construyen la etiqueta (*Modelo Profesor*) | Señales que la predicen (*Modelo Estudiante*) |
|---|---|---|
| Atención | Eye tracking y pupilometría | EEG y GSR |
| Activación | GSR | EEG, eye tracking y pupilometría |

La regla separa señales, no fuentes fisiológicas. El EEG registra también la actividad eléctrica de los movimientos oculares, de modo que la separación por señal no asegura independencia entre el EEG y la conducta ocular con que se define la atención. Ese punto se trata en la discusión.

Las variables de historial, que resumen las ventanas anteriores del mismo estímulo, pertenecen al modelamiento y están descritas en [[Borrador Resultados y Discusión 18-11-2026]], sección 6.2.

> [!warning] Diferencia con el esqueleto
> La subsección "Preprocesamiento EEG" de [[Estructura Tesis]] describe otro procesamiento: pasa-banda de 1 a 40 Hz, descarte de muestras sobre ±150 µV, bandas delta desde 0,5 Hz y gamma hasta 40 Hz, y 273 características por época. Ese texto proviene de la presentación de avances y no coincide con lo implementado. No se modificó; debe revisarse.

Fuentes: `repos/Tesis_MDS/resultados/preprocesamiento/caracteristicas_multimodales.csv` (59 columnas, 25.992 filas; SHA-256 actual `dc51dc19…`, mismo contenido que el del manifiesto del 22-08-2026 con otros finales de línea, comprobado para este borrador); `repos/Tesis_MDS/resultados/preprocesamiento/configuracion_efectiva.json` (bandas y coberturas); `documentos/01 Tesis MDS/Analisis de Datos/PREPROCESAMIENTO_MULTIMODAL.md`; `repos/Tesis_MDS/scripts/preprocesamiento_secuencial.py` (resta de la mediana por canal y ventana de Hann); `repos/Tesis_MDS/documentacion/Crudos_V2_y_EEG_Por_Canal_29-10-2026.md` y `repos/Tesis_MDS/resultados/eeg_por_canal_v2_29-10-2026/verificacion.json` (342 variables); `repos/Tesis_MDS/resultados/cierre_v3_16-11-2026/protocolo.json` (lista de variables por tarea); `repos/Tesis_MDS/resultados/montaje_ocular_41p_23-11-2026/INFORME.md`; `repos/Tesis_MDS/documentacion/Cierre_Experimental_Final_23-11-2026.md` (límite de la regla de no-circularidad).

### 4.8.2 División de Datos

**Unidad de partición.** Los datos se dividen por participante. Con 50 % de solapamiento, dos ventanas vecinas de una misma persona comparten la mitad de su señal; repartirlas entre ajuste y evaluación inflaría el desempeño. Ninguna persona aparece a la vez en ambos lados de una comparación.

**Partición congelada.** El 22-08-2026 se fijó una partición por participante, estratificada por grupo experimental. El orden dentro de cada grupo lo define el hash SHA-256 de una semilla (`20260822`) y el identificador del participante, de modo que la asignación es reproducible y no depende de los resultados.

| División | Participantes | Uso |
|---|---:|---|
| Entrenamiento | 25 | Ajuste de modelos y de transformaciones; selección de hiperparámetros |
| Validación | 8 | Comparación de modelos |
| Prueba | 8 | Evaluación fuera de muestra |
| Sensibilidad | 1 (P29) | Efecto del desfase por revisar |
| Excluidos | 6 | P1, P7, P14, P17, P25 y P42 |

Cada uno de los cuatro grupos experimentales aporta dos personas a validación y dos a prueba. Las 41 personas del análisis principal suman 22.211 ventanas: 13.524 de entrenamiento, 4.662 de validación y 4.025 de prueba.

**Selección de hiperparámetros.** Se hace dentro del entrenamiento. Las 25 personas se organizan en cinco grupos de evaluación; en cada uno, las 20 personas de ajuste se dividen a su vez en 16 de ajuste interno y 4 de validación interna, que es donde se eligen los hiperparámetros. La imputación y el escalamiento de los modelos se ajustan solo con las personas de ajuste de cada grupo.

**Diseño del análisis final.** Validación y prueba, de 8 personas cada una, se consultaron más de una vez entre el 29-10 y el 16-11-2026, por lo que dejaron de ser una evaluación independiente. Desde el 16-11-2026 el análisis principal se hace de otro modo: la configuración elegida solo con las 25 personas de entrenamiento se congela y se evalúa con validación cruzada agrupada por persona sobre las 41 (8 grupos); desde el 22-11-2026 esa validación cruzada se repite en 5 particiones y la medida de cada persona se promedia entre ellas. Esto estima los efectos con más precisión, pero **no es una confirmación independiente**: una confirmación requeriría personas nuevas.

**Lo que no se ajusta solo con entrenamiento.** Tres elementos usan información que excede el conjunto de entrenamiento y deben declararse:

- Las pseudoetiquetas se normalizan y discretizan con la sesión completa de cada persona, incluidas las personas evaluadas. Describen el estado relativo de cada persona en su sesión y se calculan offline.
- Las variables de GSR y de pupila están estandarizadas por sesión (secciones 4.6.3 y 4.6.5).
- El *Modelo Profesor* de atención utilizado es la primera componente principal ajustada con las 25 personas de entrenamiento. En la validación cruzada sobre 41 personas eso introduce una fuga leve de etiquetas; al reajustarlo sin las personas evaluadas, el contraste principal de atención pasa de +0,026 a +0,024.

> [!warning] Diferencia con el esqueleto
> [[Estructura Tesis]] (1.6 Alcances y limitaciones y 4.2 Metodología KDD) y [[Problema e hipótesis]] dicen que la normalización y los umbrales se estiman sin usar el conjunto de evaluación. Eso vale para la imputación, el escalamiento y los hiperparámetros de los modelos, pero no para las pseudoetiquetas ni para las variables estandarizadas por sesión. El protocolo del 06-11-2026 ya pide reconciliar esa redacción.

Fuentes: `repos/Tesis_MDS/resultados/modelado/particion_participantes.csv` y `manifiesto_etiquetas.json`; `documentos/01 Tesis MDS/Analisis de Datos/ETIQUETAS_Y_BASELINES.md` (partición congelada; sus etiquetas y resultados son históricos); `repos/Tesis_MDS/resultados/profesor_binario_reconstruido_29-10-2026/protocolo.json` (cinco grupos y validación interna); `repos/Tesis_MDS/resultados/cierre_v3_16-11-2026/INFORME.md` y `protocolo.json`; `repos/Tesis_MDS/resultados/cierre_final_41p_16-11-2026/INFORME.md` y `protocolo.json` (8 grupos sobre 41 personas); `repos/Tesis_MDS/resultados/cierre_robustez_41p_16-11-2026/INFORME.md` (+0,024 sin fuga); `repos/Tesis_MDS/resultados/reapertura_41p_22-11-2026/INFORME.md` (5 particiones); `repos/Tesis_MDS/resultados/protocolo_hipotesis_reintento_06-11-2026/INFORME.md`; conteos de ventanas *calculados desde* `caracteristicas_multimodales.csv` y la partición.

### 4.8.3 Métricas de Evaluación

**Medida de desempeño.** Las dos pseudoetiquetas vigentes son binarias. La medida de decisión es el área bajo la curva ROC (AUC), calculada por persona y promediada entre personas; un valor de 0,5 equivale al azar. Se informan además, de forma descriptiva y con umbral fijo de 0,5, la exactitud balanceada (BA, *balanced accuracy*), el macro-F1 y el *recall* por clase.

**Unidad de inferencia.** Es la persona, no la ventana. Para comparar dos modelos se calcula, en cada persona, la diferencia entre sus AUC, y se resume la media de esas diferencias junto con el número de personas que mejoran. Las ventanas, las semillas y los grupos de la validación cruzada no aumentan el tamaño de muestra.

**Incertidumbre.** Los intervalos de confianza de 95 % y de 90 % se obtienen por *bootstrap* de personas (20.000 réplicas). El valor p proviene de una prueba de permutación de signos bilateral (200.000 permutaciones). Los contrastes principales de cada análisis se corrigen con el método de Holm; los secundarios se informan sin corrección y se presentan como descriptivos.

**Reglas de decisión.** Se fijaron antes de ejecutar cada análisis:

| Decisión | Condición |
|---|---|
| Respaldo | p de Holm menor que 0,05 y límite inferior del intervalo de 95 % mayor que 0 |
| Efecto relevante | Además, límite inferior del intervalo de 95 % mayor que el margen práctico |
| Nulo concluyente | Intervalo de 90 % contenido entre menos y más el margen práctico |
| Inferior | Límite superior del intervalo de 95 % menor que 0 |
| Inconcluso | Cualquier otro caso |

El margen práctico usado es 0,02 de AUC. **Es una propuesta sin justificación independiente y sin aprobación del profesor guía.** La hipótesis original plantea superioridad, es decir, una diferencia mayor que 0; descartar una mejora de al menos 0,02 no equivale a descartar toda mejora, y por eso se informa siempre la relación del intervalo con cero.

**Registro previo.** Desde el 16-11-2026 cada análisis confirmatorio se registró en el repositorio con sus contrastes y reglas antes de ejecutarse, y se ejecutó una sola vez. Los análisis añadidos después de ver resultados se identifican como post hoc.

**Criterio para la hipótesis.** Se usan los criterios de interpretación de [[Problema e hipótesis]]: evidencia a favor si los modelos temporales superan a los estáticos en atención y en activación; apoyo parcial si la ventaja aparece en una sola de las dos; sin evidencia si no aparece en ninguna. Una diferencia entre estrategias de fusión es un resultado comparativo y no demuestra por sí sola la hipótesis.

> [!warning] Diferencia con el esqueleto
> La sección "Metodología KDD" de [[Estructura Tesis]] dice que se informan BA, macro-F1 y *recall* por clase; esa redacción es de septiembre, cuando las etiquetas tenían tres clases. Con las etiquetas binarias la decisión se toma con AUC por persona, y las otras tres medidas quedaron como descriptivas. Queda por decidir cuál se presenta como métrica principal en el manuscrito.

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

**EEG.** Las sesiones principales duran en promedio 13,4 minutos (desviación 1,5; mediana 13,1) *(calculado desde `eeg_resumen_sesiones.csv`; coincide con la cifra del esqueleto)*. La frecuencia efectiva, estimada desde las marcas de tiempo, tiene mediana de 125,14 Hz, coherente con los 125 Hz nominales. El principal problema de calidad es la saturación: muestras en el límite del rango del equipo (±187.500 µV), que indican desconexión o ganancia inadecuada y no actividad cerebral. Se excluyen P17 (59,2 % de muestras saturadas), P1 (37,9 %), P14 (31,2 %) y P25 (36,1 % de repetición plana). P15 (26,3 %) y P16 (25,0 %) quedan bajo el umbral y permanecen en el análisis. El umbral de 30 % es permisivo y exploratorio, y los porcentajes se calcularon con una muestra sistemática de una de cada diez filas. La representación por canal de la sección 4.7 trata después la saturación ventana a ventana.

**GSR.** Hay 47 grabaciones con GSR y 530.407 muestras válidas, a unos 15 Hz, sin marcas de tiempo duplicadas ni desordenadas. P7 y P42 no tienen GSR en la exportación. Una de las 47 grabaciones es la de prueba, de modo que 46 de los 48 participantes tienen GSR. Las grabaciones tienen entre 2.040 y 14.615 muestras; el mínimo corresponde a P4 *(calculado desde `gsr_por_grabacion.csv`)*, que por eso aporta pocas ventanas con etiqueta de activación.

**Eye tracking y pupilometría.** De las 2.187.110 muestras, 1.743.227 se clasifican como fijación, 311.735 como sacada, 104.102 como ojos no encontrados y 28.046 quedan sin clasificar. Se identifican 122.302 fijaciones, con duración mediana de 183 ms (percentiles 5 y 95: 83 y 516 ms). La validez varía entre personas: la fracción con ambos ojos válidos baja a 43,1 % en P6 y a 52,4 % en P41 *(calculado desde `calidad_por_participante.csv`)*. Ambas personas pertenecen al conjunto de validación.

**Ventanas resultantes.** El preprocesamiento produce 25.992 ventanas de 2 s en los 48 participantes, entre 414 y 757 por persona *(calculado desde `caracteristicas_multimodales.csv`)*. Tienen cobertura suficiente 24.541 en GSR, 25.964 en pupila, 25.887 en mirada y 25.958 en EEG. Cumplen a la vez todos los criterios 22.201, cifra que incluye las 482 de P29 y excluye por completo a las seis personas apartadas.

Las figuras de este análisis están en `documentos/01 Tesis MDS/attachments/Analisis de Datos/`.

Fuentes: `repos/Tesis_MDS/resultados/resumen_calidad_fuentes.csv`; `documentos/01 Tesis MDS/Analisis de Datos/EDA_EEG.md`, `EDA_GSR.md`, `EDA_EYE_PUPIL.md`, `EDA_SENALES.md` y `RESUMEN_PROCESO.md` (sincronizadas al 22-08-2026); `repos/Tesis_MDS/resultados/eda/eeg/eeg_resumen_sesiones.csv` y `eeg_resumen.json`; `repos/Tesis_MDS/resultados/eda/gsr/gsr_por_grabacion.csv` y `resumen_gsr.json`; `repos/Tesis_MDS/resultados/eda/eye_pupil/movimientos_oculares.csv`, `resumen_fijaciones.csv` y `calidad_por_participante.csv`; `repos/Tesis_MDS/resultados/preprocesamiento/auditoria_participantes.csv` y `manifiesto_ejecucion.json`; `documentos/01 Tesis MDS/Analisis de Datos/PREPROCESAMIENTO_MULTIMODAL.md`.

---

## Secciones que siguen pendientes

Se listan las secciones marcadas *(pendiente)* en [[Estructura Tesis]] que **no** se redactaron aquí.

| Sección del esqueleto | Razón |
|---|---|
| 2.2 Emociones Humanas (Naturaleza, Evolución de las Teorías, Expresión, Clasificación) | Requiere literatura que no está en las notas. Solo hay una mención sin referencia verificada a Ekman y a Russell. |
| 2.3 Atención Humana (Definición, Tipos, Nivel, Entornos Digitales) | La única fuente es `Marco Teorico/Atencion.md`, que recoge un marco conceptual planteado por el profesor en una conversación (niveles Visible, Observado, Atendido, Comprendido), sin bibliografía. No se puede citar como teoría sin referencia. |
| 2.4 Señales Fisiológicas (Definición, Clasificación Sistema Nervioso, EEG, GSR) | Requiere literatura. `notas/sustento-fisiologico-23-11-2026.md` tiene 18 referencias verificadas solo en OpenAlex, sin lectura del texto completo, y tratan de artefactos oculares en EEG, no de las definiciones que pide la sección. |
| 2.5 KDD como Marco Teórico (Etapas; KDD aplicado a emociones) | La única fuente primaria consultada es Fayyad et al. (1996), ya usada en la sección 4.2. No hay literatura verificada sobre KDD aplicado a detección de emociones. |
| 2.6 EDA (Propósito, Visualización, Estadística Descriptiva, Distribución, Outliers, Correlación) | Requiere literatura; no hay referencias en las notas. |
| 2.7 Modelamiento: Propósito, Algoritmos Clásicos, Redes Neuronales, CNN, Transformers y ViT, Aprendizaje por Transferencia, Modelos Multimodales y Fusión, División de Datos y Validación Cruzada | Requiere literatura. Además, las subsecciones de CNN, ViT, aplicación a imágenes y transferencia parecen heredadas de una plantilla con expresión facial; conviene decidir si se mantienen. |
| 2.8 Evaluación de Modelos (Propósito, Matriz de Confusión, Métricas, Multiclase, ROC y AUC, Consideraciones) | Requiere literatura. La parte aplicada está en 4.8.3 de este borrador. |
| 2.9 Detección Automática de Emociones (cinco subsecciones) | Requiere literatura, y su título depende de la decisión abierta sobre presentar "emoción" como activación. |
| 2.10 Detección Automática de Atención (cinco subsecciones) | Requiere literatura. |
| 2.11 Consideraciones Éticas | No hay insumo: las notas no documentan consentimiento informado, comité de ética ni tratamiento de datos personales. |
| 2.12 Pseudo Etiquetas (marco teórico) | Solo hay una lista de riesgos en `Marco Teorico/Atencion.md`. El vínculo con co-training y aprendizaje multi-vista figura en el esqueleto como "fuera del vault, sin verificar". |
| 3.3 Pseudo etiquetas (estado del arte) | Requiere literatura; el esqueleto la marca como pendiente de desarrollo. |
| 4.3 Participantes (parte no redactada) | Faltan reclutamiento, criterios de inclusión, datos demográficos, consentimiento, significado de los grupos `SlowWeb G1` a `G4` y protocolo de estímulos. |
| 4.4 Pupilometría: corrección por luminancia | No existe una serie de luminancia sincronizada ni está verificado que se conserven las páginas observadas. Se declara como limitación en 4.6.5. |
| 6 Modelamiento y Experimento; 7 Resultados; 8 Discusión; 9 Conclusiones | Fuera del alcance pedido. Ya existen borradores aparte: [[Borrador Resultados y Discusión 18-11-2026]], [[Borrador Discusión fisiológica 23-11-2026]] y [[Borrador Conclusiones 23-11-2026]]. El del 18-11 no incluye los resultados del 22 y 23-11. Todos dependen de decisiones abiertas con el profesor guía. |

### Secciones no pendientes cuyo texto quedó desactualizado

No se tocaron, porque no están marcadas como pendientes, pero no coinciden con lo implementado:

| Sección del esqueleto | Qué no coincide |
|---|---|
| 4.5.1 Definición Nivel de Atención | Dice "discretizado por persona" y deja abiertos la fusión y el umbral. La etiqueta usada desde el 29-10-2026 es binaria por mediana personal, con un *Modelo Profesor* de primera componente principal. Las notas de diseño proponían la fusión igualitaria como primaria y la componente principal como sensibilidad. Ambos profesores concuerdan en 66,28 % de las etiquetas (kappa 0,3255), por lo que la elección importa y sigue abierta. |
| 4.6.2 Preprocesamiento EEG | Describe filtros, umbral de ±150 µV, bandas y 273 características que no corresponden al procesamiento ejecutado (ver 4.7). |
| 4.2 Metodología KDD y 1.6 Alcances y limitaciones | Afirman que la normalización se estima solo con entrenamiento y que se informa BA, macro-F1 y *recall* (ver 4.8.2 y 4.8.3). |
| 5.1 y 5.2 (Descripción General; Duración y Registros) | "21 de 48 participantes con al menos un canal saturado" y "NaN = 0" vienen de una presentación anterior y usan un criterio por canal distinto del criterio por sesión del análisis vigente (44 de 48). No se pudo reproducir esa cifra con las tablas actuales. |

## Notas relacionadas
- [[Estructura Tesis]]
- [[Problema e hipótesis]]
- [[Resumen Diseño Etiquetas y Modelos]]
- [[Etiqueta Atencion]] · [[Etiqueta Emocion]] · [[Modelo Profesor - Decisiones]]
- [[Borrador Resultados y Discusión 18-11-2026]] · [[Borrador Discusión fisiológica 23-11-2026]] · [[Borrador Conclusiones 23-11-2026]]
