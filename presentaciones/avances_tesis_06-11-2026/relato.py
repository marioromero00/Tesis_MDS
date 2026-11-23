from estilo_tecnico import img,table

# Versión 7 (23-11-2026; la estructura viene de la versión 5 del 15-11-2026): más gráficos y diagramas, menos texto.
# Cada diapositiva define capítulo, título, cuerpo, notas del orador y fuentes.

R='resultados/'
T29=R+'temporalidad_eeg_v2_test_29-10-2026/'
C30=R+'comparacion_comun_binaria_30-10-2026/INFORME.md'
GSR=R+'etiquetas_gsr_calidad_v2_01-11-2026/'
ACT=R+'activacion_gsr_v2_recalculo_02-11-2026/'
ABL=R+'ablacion_modalidades_v2_01-11-2026/'
PROT=R+'protocolo_hipotesis_reintento_06-11-2026/'
PROF=R+'profesor_binario_reconstruido_29-10-2026/'
HIP='../../documentos/01 Tesis MDS/Marco Teorico/Problema e hipótesis.md'

def para(t):return '<p class="prose">'+t+'</p>'
def caption(t):return '<p class="caption">'+t+'</p>'
def pair(left,right):return '<div class="editorial-pair"><div>'+left+'</div><div>'+right+'</div></div>'

def strip(n_hist,label,total=32,real=None):
 real=n_hist if real is None else real
 cells=''.join('<i class="w %s"></i>'%('now' if k==total-1 else ('hist' if k>=total-1-real else ('nom' if k>=total-1-n_hist else ''))) for k in range(total))
 return '<div class="strip"><span class="strip-label">'+label+'</span><div class="cells">'+cells+'</div></div>'

def flow(boxes):
 out=[]
 for k,(cls,txt) in enumerate(boxes):
  out.append('<div class="box %s">%s</div>'%(cls,txt))
  if k<len(boxes)-1:out.append('<div class="arrow">→</div>')
 return '<div class="flow">'+''.join(out)+'</div>'

def apply(old):
 out=[]
 def S(chapter,title,body,notes,source,kind=''):
  out.append(dict(chapter=chapter,title=title,body=body,notes=notes,source=source,kind=kind))
 D1='LA PREGUNTA';D2='CÓMO LLEGUÉ HASTA AQUÍ';D3='ATENCIÓN'
 D4='EL PROBLEMA CON LA ETIQUETA DE ACTIVACIÓN';D5='ACTIVACIÓN CON LA ETIQUETA NUEVA';D6='DÓNDE QUEDO'

 S('UNIVERSIDAD DE CHILE · MAGÍSTER EN CIENCIA DE DATOS',
   '¿Sirve el historial de señales<br>para predecir atención y activación?',
   '<p class="cover-sub">EEG, GSR, mirada y pupila durante la navegación web</p>'
   +'<div class="byline"><b>Mario Romero</b><span>Profesor guía: Dr. Juan D. Velásquez<br>Avance de tesis · noviembre de 2026</span></div>',
   'Le cuento qué pasó desde la última reunión. Corregí un error en la etiqueta de activación y repetí todo con 41 personas. El historial ayuda a predecir activación, con un efecto pequeño y de pocos segundos. En atención la mejora existe pero no es temporal, y al menos un tercio de lo que detecta el EEG es la huella de los ojos. Al final hay cinco decisiones que necesito tomar con usted.',
   HIP,'story-cover')

 S('ÍNDICE','De qué voy a hablar',
   '<ol class="agenda">'
   '<li><b>La pregunta</b><span>Hipótesis y cómo la contrasto</span></li>'
   '<li><b>Los datos</b><span>De dónde vienen y cómo se etiquetan</span></li>'
   '<li><b>Estado del arte</b><span>Qué se ha hecho y qué falta</span></li>'
   '<li><b>Metodología</b><span>KDD, señales y cómo evalúo</span></li>'
   '<li><b>Las etiquetas</b><span>Atención con PCA y un error en activación</span></li>'
   '<li><b>Resultados con 41 personas</b><span>Con historial mejoran las dos; en activación, primero inconcluso</span></li>'
   '<li><b>Qué explica la mejora</b><span>Placebo, segundos en la página y activación</span></li>'
   '<li><b>Qué detecta el EEG</b><span>La huella de los ojos y por qué cuesta detectar activación</span></li>'
   '<li><b>Dónde quedo</b><span>Conclusiones, qué falta y cinco decisiones</span></li>'
   '</ol>',
   'Son nueve partes. Lo nuevo desde la última reunión son las tres últimas: qué explica la mejora, qué detecta el EEG y las conclusiones.',
   'FUENTES.md','roomy')
 S(D1,'La hipótesis',
   '<blockquote>“Los modelos temporales multimodales obtienen un mejor desempeño fuera de muestra que los modelos estáticos comparables en la detección de emociones y atención durante la navegación web.”</blockquote>'
   +'<div class="strips">'+strip(0,'Sin historial')+strip(31,'Con historial (hasta 32)')+'</div>'
   +caption('Cada cuadro es una ventana de 2 s; avanzan de a 1 s, así que se solapan.'),
   'Es la hipótesis tal cual está en el manuscrito. Para probarla comparo siempre el mismo modelo, con la misma etiqueta, y lo único que cambia es si ve las ventanas anteriores. Dice emociones, pero con GSR lo que mido es activación; eso lo vemos al final.',
   HIP,'roomy')

 S('LOS DATOS','Los datos: Toma de Muestra 2, navegación web en laboratorio',
   flow([('sig','<b>Tobii Pro Lab</b><br><small>mirada, pupila y GSR</small>'),('sig','<b>OpenBCI Cyton + Daisy</b><br><small>EEG, 16 canales, 125 Hz</small>'),('prof','Sincronización<br><small>por persona y hora UTC</small>'),('stud','Ventanas de 2 s<br><small>avanzan de a 1 s</small>')])
   +'<div class="facts"><div><b>48</b><span>personas registradas</span></div><div><b>4</b><span>secuencias de páginas (SlowWeb G1–G4)</span></div><div><b>116</b><span>estímulos: sitios como Diario Financiero, Temu o Despegar, textos y diseños</span></div><div><b>ago 2025</b><span>adquisición, proyecto Fondecyt 1231122</span></div></div>',
   'Los datos son de la Toma de Muestra 2 del Fondecyt 1231122, en laboratorio, en agosto de 2025. Tobii registra la mirada, la pupila y la GSR en un mismo archivo; el EEG viene aparte, de un OpenBCI de 16 canales a 125 Hz. Los junté por persona y hora, y corté todo en ventanas de dos segundos. No hay expresión facial en este set, y la ubicación de los electrodos no está documentada.',
   '../../documentos/01 Tesis MDS/Analisis de Datos/DOCUMENTACION_DATOS_MDS.md; ../../documentos/01 Tesis MDS/Analisis de Datos/SINCRONIZACION_SENALES.md; resultados/modelado/particion_participantes.csv; resultados/etiquetas_gsr_calidad_v2_01-11-2026/etiquetas.csv.gz','roomy')
 S('LOS DATOS','Unas señales arman la etiqueta y otras la predicen',
   '<div class="flows">'
   +'<h3>Atención</h3>'+flow([('sig','Mirada + pupila'),('prof','Modelo Profesor<br><small>Attention Score</small>'),('lab','Etiqueta<br>alta / baja'),('stud','Modelo Estudiante<br><small>EEG + GSR</small>')])
   +'<h3>Activación</h3>'+flow([('sig','GSR'),('prof','Modelo Profesor<br><small>Arousal Score</small>'),('lab','Etiqueta<br>alta / baja'),('stud','Modelo Estudiante<br><small>EEG + mirada + pupila</small>')])
   +'</div>'+caption('"Alta" es sobre la mediana de cada persona en su sesión.'),
   'No hay una etiqueta directa, así que la armo con unas señales y la predigo con las otras. La mediana usa toda la sesión, así que esto no sirve tal cual en línea.',
   PROF+'INFORME.md; '+GSR+'INFORME.md')

 S('LOS DATOS','48 personas registradas, 41 en el análisis',
   img('particiones','')
   +caption('Fuera: 4 por EEG no utilizable y 2 sin GSR. Validación y test ya los había mirado, así que todo es exploratorio.'),
   'Se registraron 48 personas. Entrenamiento tiene 25 y validación y test, 8 cada uno. P29 la dejo para un análisis de sensibilidad por un desfase de sincronización. Como las ventanas se solapan, la unidad es la persona: promedio la AUC por persona.',
   R+'modelado/particion_participantes.csv')

 S('ESTADO DEL ARTE','Qué señales combinan los trabajos recientes',
   '<table class="matrix"><thead><tr><th>Trabajo</th><th>EEG</th><th>GSR</th><th>Mirada</th><th>Pupila</th><th>Facial</th><th>ECG</th><th>Enfoque</th></tr></thead><tbody><tr class=""><td>TACOformer (2023)</td><td class="m">●</td><td class="m">●</td><td class="m"></td><td class="m"></td><td class="m"></td><td class="m">●</td><td class="n">Transformer con atención cruzada</td></tr><tr class=""><td>Feng et al. (2025)</td><td class="m">●</td><td class="m"></td><td class="m"></td><td class="m"></td><td class="m">●</td><td class="m"></td><td class="n">Autoatención multicabeza</td></tr><tr class=""><td>Milmer (2025)</td><td class="m">●</td><td class="m"></td><td class="m"></td><td class="m"></td><td class="m">●</td><td class="m"></td><td class="n">Swin Transformer</td></tr><tr class=""><td>Wang et al. (2025)</td><td class="m">●</td><td class="m"></td><td class="m">●</td><td class="m"></td><td class="m"></td><td class="m"></td><td class="n">Atención entre modalidades</td></tr><tr class=""><td>MuMTAffect (2025)</td><td class="m"></td><td class="m">●</td><td class="m">●</td><td class="m">●</td><td class="m">●</td><td class="m"></td><td class="n">Transformer por modalidad</td></tr><tr class=""><td>GBV-Net (2025)</td><td class="m">●</td><td class="m">●</td><td class="m"></td><td class="m"></td><td class="m">●</td><td class="m">●</td><td class="n">Fusión jerárquica</td></tr><tr class=""><td>Saavedra (grupo, web)</td><td class="m">●</td><td class="m">●</td><td class="m"></td><td class="m"></td><td class="m"></td><td class="m"></td><td class="n">Fusión tardía sin mejora clara</td></tr><tr class="me"><td>Esta tesis (web)</td><td class="m">●</td><td class="m">●</td><td class="m">●</td><td class="m">●</td><td class="m"></td><td class="m"></td><td class="n">Historial + fusión, contra modelo sin historial</td></tr></tbody></table>'
   +caption('Varios reportan sus resultados en bases como DEAP, SEED-IV o DREAMER; no son comparables con los míos.'),
   'La tendencia es fusionar varias señales con modelos de atención tipo Transformer. Lo más cercano en contexto web es la tesis de Saavedra en el mismo grupo, con EEG y GSR, que no encontró mejora clara con fusión tardía. Ninguno de los que revisé combina estas cuatro señales navegando la web; esa búsqueda la tengo que volver a revisar antes de afirmarlo en la defensa.',
   '../../documentos/01 Tesis MDS/Escritura/Estructura Tesis.md','roomy')
 S('ESTADO DEL ARTE','Lo que falta en la literatura y lo que intento aportar',
   '<div class="gaps">'
   '<div><h3>Lo que falta</h3><ol><li>Las señales se tratan como vectores estáticos, sin su evolución en el tiempo.</li><li>No encontré EEG + GSR + mirada + pupila en navegación web.</li><li>Pocas ablaciones sistemáticas por señal.</li></ol></div>'
   '<div><h3>Lo que hago</h3><ol><li>Mismo modelo con y sin historial, sobre las mismas ventanas.</li><li>Las cuatro señales con sitios web reales, en laboratorio.</li><li>Ablación por señal y por largo de historial.</li></ol></div>'
   '</div>'+caption('También uso el esquema Modelo Profesor → Modelo Estudiante del grupo, pero sin el clasificador facial, porque este conjunto de datos no tiene video.'),
   'Las tres brechas salen de mi revisión. Cada una tiene su respuesta en el diseño. La comparación de fusión temprana, intermedia y tardía la muestro en resultados.',
   '../../documentos/01 Tesis MDS/Escritura/Estructura Tesis.md','roomy')
 S('METODOLOGÍA','Sigo KDD, adaptado en cinco etapas',
   flow([('step','<b>1</b> Selección<br><small>Toma de Muestra 2: personas, sesiones y cuatro señales</small>'),('step','<b>2</b> Preprocesamiento<br><small>calidad, datos faltantes y sincronización</small>'),('step','<b>3</b> Transformación<br><small>variables y etiquetas por ventana de 2 s</small>'),('step','<b>4</b> Minería<br><small>modelos sin y con historial, fusión de señales</small>'),('step','<b>5</b> Evaluación<br><small>AUC por persona, diferencias e intervalos</small>')])
   +caption('Fayyad, Piatetsky-Shapiro y Smyth (1996). El artículo describe nueve pasos; los agrupé en cinco.'),
   'Uso KDD como marco. Es un proceso iterativo: cuando encontré el error en la etiqueta volví de la evaluación a la transformación, y eso es justamente lo que muestro más adelante.',
   '../../documentos/01 Tesis MDS/Escritura/Estructura Tesis.md','roomy kdd')
 S('METODOLOGÍA','Qué hago con cada señal',
   '<div class="cards4">'
   '<div><h3>EEG</h3><p>Filtro 1–45 Hz y notch de 50 Hz. Marco los canales saturados, planos o con huecos y no los uso.</p><b>342</b><span>variables por ventana, 16 canales</span></div>'
   '<div><h3>GSR</h3><p>Separo el nivel tónico y la parte fásica, y cuento las respuestas de conductancia (SCR).</p><b>4</b><span>componentes que forman el Arousal Score</span></div>'
   '<div><h3>Mirada</h3><p>Fijaciones, su duración, sacadas y dispersión de la mirada en la página.</p><span class="foot">Con la pupila forma el Attention Score</span></div>'
   '<div><h3>Pupila</h3><p>Diámetro por ojo y dilatación respecto de la línea base de cada persona.</p><span class="foot">Pendiente: corregir por el brillo de cada página</span></div>'
   '</div>'+caption('Todo se calcula en ventanas de 2 s que avanzan de a 1 s.'),
   'El EEG es lo que más trabajo tuvo: lo filtro entre 1 y 45 Hz con notch en 50, marco los canales no utilizables y desde octubre lo uso por canal. La pupila todavía no la corrijo por el brillo de cada página; eso está en las limitaciones.',
   '../../documentos/01 Tesis MDS/Escritura/Estructura Tesis.md; documentacion/Crudos_V2_y_EEG_Por_Canal_29-10-2026.md; resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md')
 S('METODOLOGÍA','Cómo comparo un modelo con y sin historial',
   flow([('sig','<b>Selección</b><br><small>solo con 25 personas de entrenamiento</small>'),('prof','Configuración congelada<br><small>misma con y sin historial</small>'),('lab','Validación cruzada<br><small>41 personas en 8 grupos</small>'),('stud','Controles<br><small>placebo, registrado antes; posición, post hoc</small>')])
   +'<div class="eval3"><div><b>AUC por persona</b><span>y luego el promedio, para que ninguna persona pese más por tener más ventanas</span></div><div><b>Diferencia pareada</b><span>con historial menos sin historial, dentro de cada persona</span></div><div><b>IC 95 % bootstrap</b><span>remuestreando personas, no ventanas</span></div></div>',
   'Elijo los hiperparámetros solo dentro de entrenamiento. Después congelo esa configuración y la evalúo con las 41 personas en validación cruzada por persona. Cada análisis principal lo registré en GitHub antes de correrlo, aunque siempre sobre personas ya consultadas; el de posición lo registré, pero después de ver el placebo. Como las ventanas se solapan, todo lo calculo por persona. El borrador también pide BA, macro-F1 y recall por clase; en esta presentación muestro solo la AUC.',
   'resultados/cierre_v3_16-11-2026/INFORME.md; resultados/cierre_final_41p_16-11-2026/protocolo.json; resultados/activacion_gsr_v2_recalculo_02-11-2026/protocolo.json; resultados/temporalidad_eeg_v2_test_29-10-2026/INFORME.md; ../../documentos/01 Tesis MDS/Escritura/Estructura Tesis.md','roomy')
 S('LAS ETIQUETAS','Con PCA, la etiqueta de atención se predice mejor',
   img('profesores','Entrenamiento, 25 personas (OOF). Las dos versiones coinciden en el 66 % de las ventanas.'),
   'Probé dos formas de armar la etiqueta de atención: pesos iguales y PCA. Con PCA todos los modelos la predicen mejor y seguí con esa. Las dos coinciden en dos tercios de las ventanas.',
   PROF+'comparacion_profesores_modelos.csv; '+PROF+'INFORME.md')

 S(D4,'Con la etiqueta antigua, tres personas tenían datos anómalos',
   img('calidad_gsr','Etiqueta antigua, 25 personas de entrenamiento.'),
   'Esto fue lo que me hizo dudar. P4 casi no tenía señal y aun así todas sus ventanas tenían etiqueta. P34 y P46 tenían muchos puntajes repetidos, o sea empates, y P34 quedaba con 8,6 % de clase alta. Ahí paré de ajustar modelos y revisé la etiqueta.',
   R+'activacion_diagnostico_nested_30-10-2026/diagnostico_personas.csv; '+R+'activacion_diagnostico_nested_30-10-2026/INFORME.md')

 S(D4,'El generador mezclaba las ventanas',
   '<div class="shift"><div class="col"><h3>Lo que debía pasar</h3>'
   +''.join('<div class="row"><span class="win">Ventana %d</span><span class="gsr g%d">GSR %d</span></div>'%(k,k,k) for k in range(1,6))
   +'</div><div class="col"><h3>Lo que pasaba</h3>'
   +''.join('<div class="row"><span class="win">Ventana %d</span><span class="gsr g%d bad">GSR %d</span></div>'%(k,j,j) for k,j in zip(range(1,6),[3,1,5,2,4]))
   +'</div><div class="col big"><b>98 %</b><span>de los valores GSR del archivo<br>quedaron en otra ventana<br>(25.498 de 25.992)</span></div></div>'
   +caption('Al agrupar por persona y reiniciar el índice, cada valor perdía su ventana.'),
   'Repitiendo el cálculo con el error obtengo los mismos puntajes que tenía guardados, así que las AUC de activación de antes no sirven. El 25.992 es el archivo completo, incluidas personas fuera del análisis.',
   GSR+'INFORME.md; '+GSR+'auditoria_independiente_02-11-2026.json')

 S(D4,'"Alta" es estar sobre su propia mediana de activación: así se ve en P22',
   img('ejemplo_etiqueta','P22, un estímulo. Cada punto es una ventana.'),
   'Este es un tramo real de P22. La línea es el puntaje GSR de seis segundos y la punteada, su mediana en toda la sesión. Los puntos azules quedan como “alta” y los grises como “baja”. La etiqueta dice si P22 está más activada que de costumbre en ese momento.',
   GSR+'etiquetas.csv.gz; '+GSR+'umbrales.csv')

 S(D4,'La etiqueta antigua y la nueva coinciden solo en la mitad de las ventanas',
   img('cambio_etiquetas','Ventanas con etiqueta en ambas versiones.'),
   'Comparé la etiqueta antigua con la nueva en las mismas ventanas: cambia casi la mitad. Con clases balanceadas, eso es lo que esperaría si no tuvieran relación.',
   GSR+'resumen_personas.csv')

 S(D4,'La etiqueta nueva (V2) deja 11.796 de 22.211 ventanas',
   img('cascada','El paso 2 corrige el error y no saca ventanas.'),
   'Rehice la etiqueta en cuatro pasos. Lo que más saca es pedir cinco ventanas válidas seguidas dentro del mismo estímulo; si hay un hueco o cambia el estímulo, parte de cero. Por calidad se van 401, todas de P4. Las 41 personas mantienen las dos clases.',
   GSR+'motivos.csv; '+GSR+'INFORME.md')
 S('RESULTADOS CON 41 PERSONAS','Primer análisis con 41 personas (16-11): mejora en atención; en activación, inconcluso',
   img('final_principal','Cada punto es una partición de las 41 personas en 8 grupos; la oscura es la registrada de antemano. Al repetirlo con 5 particiones (22-11), activación pasa a +0,036 [+0,010; +0,065].'),
   'Para tener más potencia usé las 41 personas en validación cruzada, con la configuración ya congelada y sin búsqueda. En atención la mejora es +0,026 y mejoran 36 de 41; se repite con otras tres particiones. En activación da +0,034 pero el intervalo de la partición registrada toca el cero.',
   'resultados/cierre_final_41p_16-11-2026/INFORME.md; resultados/cierre_robustez_41p_16-11-2026/INFORME.md')
 S('RESULTADOS CON 41 PERSONAS','En atención, la fusión tardía rinde mejor entre redes MLP; con HGB, no',
   img('fusion_final','Misma familia de modelo (MLP) y misma entrada en las tres fusiones.'),
   'Con la misma familia de modelo, en atención la fusión tardía le gana a la temprana por +0,012 y también a la intermedia. En activación no hay diferencias. La intermedia que probé es más profunda, así que compara también capacidad. Es un contraste secundario y vale para esta familia (MLP): con HGB, en el cierre V3, el signo fue el contrario (−0,010 en entrenamiento).',
   'resultados/ampliacion_41p_16-11-2026/INFORME.md')
 S('RESULTADOS CON 41 PERSONAS','El modelo de atención rinde mejor al final de la sesión y peor en textos',
   img('sesion_pagina','Modelo con historial. Izquierda: quintos del tiempo de sesión. Derecha: AUC por tipo de página, sin las categorías con pocas personas (blur, emotion). Descriptivo.'),
   'En atención la AUC sube a lo largo de la sesión. Por tipo de página, funciona mejor en sitios web y peor en textos. En activación, la proporción de ventanas altas cae al final, compatible con habituación. Todo esto es descriptivo.',
   'resultados/ampliacion_41p_16-11-2026/INFORME.md')
 S('QUÉ EXPLICA LA MEJORA','¿De dónde viene la mejora?',
   img('origen_mejora','Mejora frente al modelo sin historial. Placebo: misma cantidad de ventanas, de la misma persona, en otras páginas.'),
   'Comparé el historial real con un placebo y con una sola variable: los segundos que lleva la persona en la página. En atención, el placebo y los segundos solos dan lo mismo que el historial real. En activación, el placebo y los segundos no aportan, y el historial sí, incluso sin los 6 s que usa la etiqueta.',
   'resultados/cierre_robustez_41p_16-11-2026/INFORME.md; resultados/explicativo_posicion_41p_18-11-2026/INFORME.md; resultados/ampliacion_41p_16-11-2026/INFORME.md')
 S('QUÉ EXPLICA LA MEJORA','En atención, la etiqueta depende de cuánto lleva la persona en la página',
   img('posicion_etiqueta','Promedio de las 41 personas. Activación empieza en 5 s porque su etiqueta exige cinco ventanas seguidas.'),
   'Al entrar a una página, la etiqueta de atención cae a 37 % entre el segundo 2 y 3 y después sube hasta 62 %. El modelo con historial aprendía eso a través del largo del historial. Lo más probable es que refleje cómo se arma la etiqueta con fijaciones y pupila al cambiar de página. Este análisis lo hice después de ver el placebo, así que es explicativo.',
   'resultados/explicativo_posicion_41p_18-11-2026/INFORME.md')
 S('QUÉ EXPLICA LA MEJORA','En activación, los segundos previos sí aportan',
   img('activacion_temporal','Historial sin las 6 ventanas que usa la etiqueta, contra un placebo con la misma cantidad de ventanas. Filas 3 y 4: historial completo contra un modelo que solo conoce los segundos en la página. Repetido con 5 particiones (22-11): frente a la posición, +0,032 [+0,004; +0,059], inconcluso tras Holm.'),
   'Excluí del historial los 6 s que definen la etiqueta, para que no haya solapamiento. Aun así le gana al placebo por +0,046 y mejora en 28 de 41 personas, p Holm 0,004. Frente a un modelo que conoce los segundos en la página, el historial sumaba +0,038 en el análisis post hoc del 18-11; el 22-11, con 5 particiones y la posición en ambos modelos, da +0,032 y queda inconcluso tras la corrección. Las cifras del gráfico son del 16 y 18-11. Ojo que el modelo sigue siendo débil: AUC alrededor de 0,57.',
   'resultados/ampliacion_41p_16-11-2026/enmienda_e1_lag6/contrastes.csv; resultados/explicativo_posicion_41p_18-11-2026/contrastes.csv')
 D7='QUÉ DETECTA EL EEG'
 MON='resultados/montaje_ocular_41p_23-11-2026/INFORME.md';LIM='resultados/limpieza_ocular_41p_23-11-2026/INFORME.md';RED='resultados/red_cruda_41p_23-11-2026/INFORME.md'
 FIS='../../notas/sustento-fisiologico-23-11-2026.md'
 S(D7,'Los movimientos de los ojos se ven en el EEG',
   img('ocular_parpadeo','Respuesta promedio al parpadeo por canal, mediana de las 41 personas. Nombres según el montaje por defecto del equipo.'),
   'La etiqueta de atención se arma con la mirada y la predigo con EEG. Antes de interpretar eso revisé cuánto de los ojos se cuela en el EEG. El parpadeo pega 150 µV en los dos canales de la frente y baja hasta unos 20 atrás. Ese patrón además respalda el montaje por defecto, que no estaba documentado. Otro hallazgo: el EEG va entre 0,18 y 0,53 s atrasado respecto del seguidor ocular; no lo corregí.',
   MON)
 S(D7,'Al quitar los componentes oculares, la detección de atención cae',
   img('limpieza_ocular','Componentes oculares: 3,5 % de la varianza del EEG. Componentes del control: 72 %.'),
   'Por persona separé el EEG en componentes independientes y quité los más ligados a la mirada y a los parpadeos. Con tres, la AUC baja de 0,681 a 0,621, en 39 de 41 personas. El control quita tres componentes no oculares, con veinte veces más varianza, y casi no cambia. Alfa y beta, que parecía lo más limpio, también cae: de 0,593 a 0,547. La limpieza es parcial, así que 0,06 es una cota inferior. Registrado antes de correr y auditado.',
   LIM)
 S(D7,'Una red sobre la señal cruda rinde más, y también depende de la huella ocular',
   img('red_cruda','Red convolucional tipo EEGNet sobre el EEG crudo. HGB: modelo de referencia con variables calculadas.'),
   'Probé un modelo más complejo: una red convolucional que aprende directo de la señal cruda. En atención le gana al modelo de referencia, 0,716 contra 0,681, por +0,035; pasa por poco el margen de 0,02, que es una propuesta mía sin aprobar. Pero al quitar los componentes oculares cae a 0,649, y su probabilidad sigue el recorrido de la mirada más que la del modelo de referencia. Su ventaja sobre el modelo de referencia se mantiene con el EEG limpio: +0,028. En activación queda en el azar. Es una sola arquitectura sin búsqueda, y no entrené una red con el filtro de control.',
   RED)
 S(D7,'Por qué: el ojo genera señal eléctrica que llega a los electrodos',
   table(['Mecanismo','Qué produce en el EEG','En mis datos'],[['Dipolo córneo-retinal','Cada giro del ojo cambia el potencial frontal','Mirada horizontal con signo opuesto en F7 y F8'],['Párpado sobre la córnea','Onda grande en la frente al parpadear','150 µV adelante, 20 µV atrás'],['Músculos del ojo al iniciar una sacada','Descarga breve de banda ancha','Compatible con que alfa y beta también caigan al limpiar'],['Respuesta visual tras cada fijación','Actividad occipital real, pero sigue a los ojos','No se puede separar del artefacto']])
   +caption('Croft y Barry (2000); Plöchl et al. (2012); Iwasaki et al. (2005); Keren et al. (2010); Dimigen et al. (2011). Interpretación propia; 8 de las 18 referencias, contrastadas solo con el resumen.'),
   'La explicación fisiológica. El ojo es un dipolo: córnea positiva, retina negativa. Como la etiqueta se define con los ojos, todo lo que los ojos dejan en el EEG la predice. La regla de no usar las mismas señales se cumple, pero no asegura independencia fisiológica. Lo que detecto es en buena parte lo observado, y no puedo afirmar que sea lo atendido. De las 18 referencias, 10 las contrasté con el texto completo y 8 solo con el resumen.',
   FIS+'; '+LIM)
 S(D7,'Por qué puede costar detectar la activación desde el EEG',
   table(['Razón','Qué dice la fisiología','En mis datos'],[['Origen','La GSR depende del sistema simpático y de regiones de emoción y atención','EEG de 16 canales: AUC 0,52'],['Tiempos','La respuesta empieza 1 a 5 s después del evento y decae lento','El historial de los 6 s previos sí ayuda'],['Tipo de relación','La relación conocida entre EEG y GSR es tónica, entre condiciones o personas','Etiqueta relativa a la mediana de la persona'],['Pupila','Responde a la luz y al enfoque, además de la activación','Agregar pupila y mirada no mejora']])
   +caption('Boucsein et al. (2012); Critchley (2002); Benedek y Kaernbach (2010); Barry et al. (2007); Mathôt (2018). Interpretación propia; 8 de las 18 referencias, contrastadas solo con el resumen.'),
   'La etiqueta de activación viene de la GSR, que mide glándulas sudoríparas bajo control simpático. Esa vía es lenta, y es posible que dependa de regiones profundas que el EEG de superficie ve poco; eso último no lo pude confirmar en la fuente. Una ventana de EEG de 2 s no calza con una respuesta que tarda segundos. Esto es coherente con mi resultado temporal: lo que ayuda en activación es el historial de los segundos previos.',
   FIS+'; '+RED)
 S('DÓNDE QUEDO','Qué responde la tesis',
   table(['','Atención','Activación'],[['Mejora con historial','+0,029 [+0,021; +0,037]','+0,036 [+0,010; +0,065]'],['¿Es información temporal?','No: con la posición, el historial agrega +0,001','En parte: +0,047 sobre el placebo a 6 s; desde 12 s, inconcluso'],['Modelo con orden (GRU)','No agrega y rinde peor','Señal secundaria'],['Fusión','Tardía mejor con MLP (+0,012)','Sin diferencias'],['¿Qué detecta el EEG?','Al menos un tercio son los ojos: 0,681 → 0,621 al limpiar','Nada demostrable: 0,52']])+caption('Apoyo parcial, y viene de activación. Filas 1 y 2: repetición del 22-11 (el 16-11 dio +0,026 y +0,034). GRU y fusión: 16-11. EEG: 23-11.'),
   'La respuesta corta: el historial de las señales sí ayuda a predecir activación, aunque con modelos débiles. En atención la mejora existe pero no es temporal. Lo nuevo es la última fila: en atención, al menos un tercio de lo que el EEG tiene sobre el azar es la huella de los ojos, y no puedo descartar que el resto también lo sea. Todo esto con datos que ya había consultado antes, así que confirmarlo requiere personas nuevas.',
   'resultados/reapertura_41p_22-11-2026/INFORME.md; resultados/reapertura_fase3_41p_22-11-2026/INFORME.md; resultados/cierre_final_41p_16-11-2026/INFORME.md; '+LIM+'; '+RED,'compact')
 CON='../../documentos/01 Tesis MDS/Escritura/Borrador Conclusiones 23-11-2026.md; documentacion/Cierre_Experimental_Final_23-11-2026.md'
 S(D6,'Conclusiones: la hipótesis tiene apoyo parcial',
   '<ol class="questions">'
   '<li><b>El apoyo viene de activación.</b><span>Con historial: +0,036 [+0,010; +0,065], y mejoran 23 de 41 personas. Frente al placebo y sin el intervalo de la etiqueta: +0,047 [+0,017; +0,078]. Al controlar la posición queda en +0,032, inconcluso.</span></li>'
   '<li><b>En activación solo hay respaldo para los 6 s anteriores.</b><span>A 12 s es inconclusa (+0,024) y desde los 24 s no se distingue del placebo, sin demostrar que desaparezca. AUC bajas: 0,52 a 0,59.</span></li>'
   '<li><b>En atención la mejora no es temporal.</b><span>Con historial: +0,029 [+0,021; +0,037]. Si el modelo conoce la posición en la página, el historial agrega +0,001.</span></li>'
   '<li><b>El orden de las ventanas no aportó de forma demostrable.</b><span>La GRU rinde 0,040 menos en atención. La fusión tardía solo gana en atención y con MLP: +0,012.</span></li>'
   '</ol>',
   'Son las conclusiones del borrador del capítulo 9. La hipótesis se apoya en parte, y solo por activación. El efecto se sostiene frente al placebo, pero es pequeño, desigual entre personas y de pocos segundos. En atención, lo que parecía temporal era la posición dentro de la página. Al controlar la posición, el efecto de activación conserva su tamaño (+0,032) pero queda inconcluso.',
   CON+'; '+LIM)
 S(D6,'Conclusiones: qué detecta el EEG',
   '<ol class="questions">'
   '<li><b>En atención, al menos un tercio de lo que detecta el EEG son los ojos.</b><span>La AUC baja de 0,681 a 0,621 al quitar tres componentes oculares (3,5 % de la varianza); el control queda en 0,674. Es una cota inferior.</span></li>'
   '<li><b>Un modelo más complejo no cambia la lectura.</b><span>La red sobre la señal cruda llega a 0,716, pero pierde 0,067 al quitar los componentes oculares. En activación queda en 0,498.</span></li>'
   '<li><b>Separar las señales no asegura independencia fisiológica.</b><span>La etiqueta se define con lo observado (mirar) y el EEG registra esa misma conducta. No puedo afirmar que detecte lo atendido.</span></li>'
   '<li><b>El aporte es doble.</b><span>Evidencia acotada de que el historial de los segundos previos ayuda a predecir la activación, y una advertencia sobre evaluar modelos de EEG con etiquetas oculares.</span></li>'
   '</ol>',
   'La conclusión metodológica más importante es la tercera. Cumplí la regla de no-circularidad entre señales, pero el EEG contiene la huella eléctrica de los ojos, así que la etiqueta y la entrada no son independientes. Estas conclusiones suponen de forma provisoria las decisiones que le consulto en la última lámina.',
   CON+'; '+RED)
 S(D6,'Qué falta para cerrar la tesis',
   '<div class="timeline3"><div><b>Experimentos</b><span>Ninguno imprescindible</span><p>No espero que más corridas sobre estas 41 personas cambien las conclusiones; ya se habían consultado todas.</p></div>'
   '<div><b>Decisiones</b><span>Con el profesor guía</span><p>Cohorte nueva o no, el margen de 0,02, activación en vez de emociones, qué etiqueta de atención usar y el encuadre.</p></div>'
   '<div><b>Cierre</b><span>Sin experimentos nuevos</span><p>Integrar los resultados del 22 y 23-11 al borrador y ajustar las conclusiones según lo que se decida.</p></div></div>'
   +caption('Opcionales, solo si se piden: red con filtro de control, corregir el desfase entre EEG y seguidor ocular, y una cohorte nueva para confirmar.'),
   'Mi propuesta es cerrar aquí. Lo que falta son decisiones y escritura. Sobre la etiqueta: el 22 de noviembre probé una etiqueta de atención corregida por la posición en la página, y hay que decidir si reemplaza a la original. De los opcionales, el único que cambiaría el estatus de los resultados es la cohorte nueva.',
   '../../notas/resumen-ultimo-mes-22-11-2026.md; '+LIM+'; '+RED)
 S(D6,'Necesito decidir cinco cosas con usted',
   '<ol class="questions five">'
   '<li><b>¿Escribo con estos resultados o planifico una cohorte para confirmar activación?</b><span>Las 41 personas ya se habían consultado: nada es una confirmación independiente.</span></li>'
   '<li><b>¿Qué cuenta como "mejor"?</b><span>Cualquier mejora sobre 0, como dice la hipótesis, o un mínimo como +0,02 de AUC.</span></li>'
   '<li><b>¿Escribo "activación (GSR)" en vez de "emociones"?</b><span>Con GSR no puedo hablar de emociones en general.</span></li>'
   '<li><b>¿Uso la etiqueta de atención original o la corregida por posición?</b><span>La corregida ya no se predice con la posición (0,504) y la detección baja poco: 0,675 frente a 0,683.</span></li>'
   '<li><b>¿Encuadro la tesis como apoyo parcial más una advertencia metodológica?</b><span>La atención por EEG se presentaría como ligada, al menos en parte, a la huella ocular.</span></li>'
   '</ol>',
   'La experimentación está cerrada y auditada. Lo que más me urge es la primera pregunta, porque define si escribo o recluto. Hay un sexto punto, menor: las etiquetas se normalizan con la sesión completa de cada persona, y el manuscrito pide normalizar solo con entrenamiento; necesito saber si basta con declararlo como límite. El detalle de cada opción está en la minuta, que agrega un séptimo punto: confirmar el profesor PCA como definición del Attention Score.',
   'documentacion/Cierre_Experimental_Final_23-11-2026.md; resultados/enfoques_41p_22-11-2026/INFORME.md; '+PROT+'INFORME.md; ../../notas/pautas-escritura-recuperadas.md','closing-questions')

 AX='ANEXO'
 S(AX+' A','Atención: curvas ROC en test',
   img('roc_atencion','Test, 8 personas. Curva promedio de las curvas por persona.'),
   'La AUC de la leyenda es la media de las AUC por persona.',
   T29+'INFORME.md; '+T29+'predicciones_test.csv.gz')
 S(AX+' B','Activación: curvas ROC en test',
   img('roc_activacion','Test, 8 personas (2.184 ventanas). Curva promedio de las curvas por persona.'),
   'Las tres curvas van pegadas a la diagonal.',
   ACT+'predicciones_externas.csv.gz; '+ACT+'metricas.csv')
 S(AX+' C','Señales',
   table(['Señal','Qué uso'],[['EEG','Potencia por banda y descriptores espectrales y temporales, 16 canales'],['GSR','Componentes tónico y fásico, respuestas de conductancia (SCR)'],['Mirada','Fijaciones, dispersión y trayectoria'],['Pupila','Cambios en el diámetro']])
   +caption('Toma de Muestra 2: navegación web, agosto de 2025. Sin expresión facial.'),
   'El EEG lo uso por canal desde octubre; antes promediaba los canales.',
   HIP+'; ../../documentos/01 Tesis MDS/Analisis de Datos/DOCUMENTACION_DATOS_MDS.md')
 S(AX+' D','Configuración del entrenamiento de activación',
   table(['Componente','Configuración'],[['Modelo','HistGradientBoostingClassifier (HGB)'],['Búsqueda','7 o 15 hojas · 5 folds agrupados por persona'],['Final','15 hojas · 300 iteraciones · tasa 0,05 · L2 = 10'],['Preprocesamiento','Mediana, indicadores de ausencia y estandarización, solo con entrenamiento'],['Modelos','30 ajustes internos · 15 OOF · 3 finales']]),
   'La misma configuración para los tres largos de historial.',
   ACT+'protocolo.json')
 S(AX+' E','Activación: la muestra necesaria va de 72 a 767 según la variabilidad',
   img('muestra','Gris: atención. Azul: activación. Mejora relevante +0,02; efecto real +0,04.'),
   'El número depende mucho de qué variabilidad uso. Las de validación y test salen de 8 personas; la de entrenamiento, de 25 pero mezclando folds, así que 767 es el escenario pesimista. Para las dos tareas manda la de activación; con 20 % de pérdidas serían 90 a 959 a reclutar. Y el +0,02 es una propuesta mía.',
   PROT+'INFORME.md; '+PROT+'verificacion_simulada.json')

 S(AX+' F','Referencias de la explicación fisiológica',
   table(['Tema','Referencias'],[['Artefactos oculares en el EEG','Croft y Barry (2000) · Iwasaki et al. (2005) · Plöchl, Ossandón y König (2012)'],['Sacadas y actividad muscular','Yuval-Greenberg et al. (2008) · Keren et al. (2010) · Hipp y Siegel (2013) · Goncharova et al. (2003)'],['Limpieza y potenciales de fijación','Jung et al. (2000) · Dimigen (2020) · Dimigen et al. (2011)'],['Atención y red convolucional','Klimesch (2012) · Lawhern et al. (2018)'],['Activación, GSR y pupila','Boucsein et al. (2012) · Critchley (2002) · Benedek y Kaernbach (2010) · Barry et al. (2005, 2007) · Mathôt (2018)']])
   +caption('Datos bibliográficos verificados el 23-11-2026. Contrastadas con la fuente: 10 en texto completo y 8 solo por resumen; dos atribuciones sin comprobar (Boucsein, Critchley).'),
   'La lista completa con DOI está en la nota de sustento fisiológico. Los años de tres trabajos difieren entre la fecha en línea y la del volumen.',
   FIS,'compact')
 for x in out:
  for k in ('title','body'):x[k]=x[k].replace(' %',' %')
 return out

CSS='''
:root{--ink:#142a44;--muted:#5e7085;--line:#dce4ee;--paper:#fff;--accent:#145ac7}
body{background:#e8edf3;font-family:"Helvetica Neue",Arial,sans-serif}.slide{border:0;padding:48px 70px 45px}.slide:before{content:'';position:absolute;left:70px;right:70px;top:88px;height:1px;background:#dce4ee}.chapter{height:32px;margin:0 0 35px;color:#34516f;letter-spacing:1.6px;font-size:13px;font-weight:500}h1{font-weight:500;font-size:43px;line-height:1.15;letter-spacing:-1.35px;margin-bottom:35px;max-width:1120px}h3{font-size:17px;color:#185bac;letter-spacing:.1px;font-weight:600;margin-bottom:16px}p{font-size:23px;line-height:1.43}.prose{font-size:25px;line-height:1.45;margin-bottom:25px}.editorial-pair{display:grid;grid-template-columns:1.1fr 1fr;gap:85px;padding-top:16px}.opening{font-size:40px;line-height:1.25;letter-spacing:-1.3px}.opening span{color:#60758d}.opening b{color:#145ac7;font-weight:500}.intro{font-size:29px;line-height:1.4;letter-spacing:-.3px;margin-bottom:35px}.caption{font-size:18px;line-height:1.4;color:#5b6d82;margin-top:26px;border:0;padding:0;max-width:1080px}table{font-size:23px}th{font-size:14px;border-bottom:1px solid #6a8baa;letter-spacing:.65px;padding-bottom:16px;color:#34516f}td{font-size:22px;line-height:1.35;padding:20px 22px 20px 0;border-bottom:1px solid #dce4ee}tbody tr:nth-child(even){background:white}table td:first-child{width:29%;font-weight:500;color:#185bac}.story-cover:before{display:none}.story-cover .chapter{margin-bottom:70px;color:#145ac7}.story-cover h1{font-size:61px;line-height:1.12;letter-spacing:-2.5px;font-weight:500;max-width:1090px;margin-bottom:30px}.cover-sub{font-size:25px;line-height:1.4;color:#61748c}.byline{margin-top:52px;display:flex;gap:55px;align-items:flex-start;border-top:1px solid #dce4ee;padding-top:24px;width:100%}.byline b{font-size:21px;font-weight:500}.byline span{font-size:17px;line-height:1.55;color:#61748c}.split-counts{display:grid;grid-template-columns:repeat(3,1fr);gap:60px;margin:38px 0 48px}.split-counts b{font-size:108px;font-weight:400;letter-spacing:-5px;line-height:1;color:#145ac7}.split-counts span{display:block;font-size:22px;margin-top:16px;color:#536b85}.method-line{display:flex;gap:55px;border-top:1px solid #dce4ee;padding-top:28px;font-size:21px}.method-line b{font-weight:500;color:#145ac7}.feature-count{font-size:85px;color:#145ac7;line-height:1;letter-spacing:-3px;margin:16px 0 22px}.feature-count span{font-size:27px;letter-spacing:0;color:#61748c}.result-number{font-size:117px;color:#145ac7;letter-spacing:-7px;line-height:1;margin-top:22px}.metric-label{font-size:20px;color:#536b85;margin-top:20px}.secondary-number{font-size:38px;margin-top:38px;color:#34516f;letter-spacing:-1px}.secondary-number span{font-size:20px;letter-spacing:0;margin-left:10px}.result-slide .editorial-pair{grid-template-columns:1.1fr 1fr}.contrast-line{display:flex;gap:32px;align-items:center;margin-top:40px}.contrast-line strong{font-size:66px;font-weight:400;letter-spacing:-3px;color:#145ac7}.contrast-line span{font-size:20px;line-height:1.5;color:#536b85}.contrast-line p{font-size:22px;margin:0 0 0 auto;line-height:1.5}.person-id{font-size:17px;letter-spacing:1px;color:#145ac7;margin-bottom:20px}.audit-layout{display:grid;grid-template-columns:1fr 1.2fr;gap:60px;margin-top:40px}.audit-layout b{font-size:84px;font-weight:400;color:#145ac7;letter-spacing:-4px;line-height:1}.audit-layout span{display:block;font-size:19px;line-height:1.5;margin-top:18px;color:#61748c}.audit-layout p{font-size:24px;margin-bottom:25px}.data-figure img{height:400px}.data-figure figcaption{font-size:17px;margin-top:14px;border-top:0;padding:0;line-height:1.45}.next-decision{display:grid;grid-template-columns:245px 1fr;column-gap:42px;row-gap:22px;padding-top:15px}.next-decision h3,.next-decision p{padding:0 0 23px;margin:0;border-bottom:1px solid #dce4ee}.next-decision h3{font-size:21px;line-height:1.5}.next-decision p{font-size:27px;line-height:1.4}.folio{bottom:27px;right:70px;font-size:12px;color:#7b8b9b}.technical-note{border:0;padding:0;font-size:18px;margin-top:25px}.data-figure{margin:0}.dialog h2{font-weight:500}.index-list button{padding:16px 0}nav{background:#fff}nav button{color:#536b85}#counter{color:#536b85}.steps{font-size:22px}.columns{gap:80px}.lead{font-size:27px}
@media(max-width:650px){.reading .slide:before{display:none}.reading .chapter{height:auto;margin-bottom:24px;font-size:10px}.reading .editorial-pair,.reading .audit-layout,.reading .next-decision{grid-template-columns:1fr;gap:22px}.reading .opening{font-size:31px}.reading .prose,.reading .intro,.reading .audit-layout p{font-size:21px}.reading .story-cover h1{font-size:37px;letter-spacing:-1.2px}.reading .story-cover .chapter{margin-bottom:35px}.reading .cover-sub{font-size:21px}.reading .byline{margin-top:35px;gap:25px}.reading .byline span{font-size:14px}.reading .byline b{font-size:18px}.reading .split-counts{gap:18px;margin:25px 0}.reading .split-counts b{font-size:60px;letter-spacing:-3px}.reading .split-counts span{font-size:14px}.reading .method-line{display:block;font-size:18px}.reading .method-line span{display:block;margin-bottom:12px}.reading .caption{font-size:16px}.reading .result-number{font-size:82px;letter-spacing:-4px}.reading .contrast-line{flex-wrap:wrap;gap:18px}.reading .contrast-line strong{font-size:52px}.reading .contrast-line span,.reading .contrast-line p{font-size:18px;margin:0}.reading .audit-layout b{font-size:66px}.reading .next-decision h3{padding-bottom:0;border:0;font-size:18px}.reading .next-decision p{font-size:21px}.reading .feature-count{font-size:64px}}

h1{font-family:Cambria,Georgia,"Times New Roman",serif;font-weight:400;letter-spacing:-.6px;font-size:42px}.story-cover h1{font-family:Cambria,Georgia,serif;font-weight:400;letter-spacing:-1.2px;font-size:58px}
blockquote{font-family:Cambria,Georgia,serif;font-size:34px;line-height:1.3;color:#142a44;border-left:4px solid #145ac7;padding-left:28px;margin:10px 0 40px}
.opening-sub{font-size:24px;color:#60758d;margin-top:22px}
.questions{list-style:none;counter-reset:q;padding:0;margin:6px 0 0}.questions li{counter-increment:q;position:relative;padding:15px 0 15px 62px;border-bottom:1px solid #dce4ee}.questions li:before{content:counter(q);position:absolute;left:0;top:12px;font-family:Cambria,Georgia,serif;font-size:36px;color:#145ac7;line-height:1}.questions.five li{padding-top:10px;padding-bottom:10px}.questions.five b{font-size:22px}.questions.five span{font-size:18px}.questions b{display:block;font-size:24px;font-weight:600;margin-bottom:5px}.questions span{font-size:19px;line-height:1.4;color:#536b85}
.sources{font-size:23px;line-height:1.5}.ref{color:#7b8b9b;font-weight:400}.next-step{font-size:20px;color:#145ac7;margin-top:22px}.roomy td{font-size:26px;padding-top:26px;padding-bottom:26px}.roomy th{font-size:15px}.roomy .prose{font-size:28px}.roomy .caption{font-size:21px;margin-top:34px}.roomy h3{font-size:20px}.roomy blockquote{font-size:37px;margin-bottom:50px}.roomy .split-counts{margin:50px 0 60px}.roomy .opening{font-size:46px}.roomy .opening-sub{font-size:27px}.data-figure img{height:372px}
td{font-size:23px}
@media(max-width:650px){.reading blockquote{font-size:22px}.reading .questions b{font-size:19px}.reading .questions span{font-size:16px}.reading .questions li{padding-left:40px}.reading h1{font-size:30px}}

.strips{margin:8px 0 6px}.strip{display:flex;align-items:center;gap:22px;margin:16px 0}.strip-label{width:230px;font-size:20px;color:#34516f;text-align:right}.cells{display:flex;gap:4px}.w{display:block;width:22px;height:40px;border:1.5px solid #c3cfdc;border-radius:3px;background:#fff}.w.hist{background:#9fc1e6;border-color:#9fc1e6}.w.nom{border:1.5px dashed #5e9bd6;background:#eef3f9}.w.now{background:#145ac7;border-color:#145ac7}
.flows h3{margin:18px 0 10px}.flow{display:flex;align-items:stretch;gap:12px}.box{flex:1;border-radius:6px;padding:16px 14px;font-size:21px;line-height:1.3;text-align:center;display:flex;flex-direction:column;justify-content:center}.box small{font-size:16px;color:inherit;opacity:.8;margin-top:4px}.box.sig{background:#eef3f9;color:#34516f}.box.prof{background:#145ac7;color:#fff}.box.lab{background:#fff;border:2px solid #145ac7;color:#145ac7;font-weight:600}.box.stud{background:#142a44;color:#fff}.box.step{background:#eef3f9;color:#142a44;text-align:left;justify-content:flex-start;padding:26px 20px;font-size:25px;min-height:250px;margin-top:20px}.box.step small{font-size:19px;line-height:1.4;margin-top:10px}.box.step em{font-style:normal;margin-top:auto;padding-top:18px;font-size:22px;color:#145ac7;font-weight:600}.box.step b{font-family:Cambria,Georgia,serif;color:#145ac7;font-size:34px;font-weight:400;display:block;margin-bottom:6px}.arrow{align-self:center;font-size:30px;color:#9aa8b8}
.shift{display:grid;grid-template-columns:1fr 1fr 1.1fr;gap:46px;margin-top:6px}.shift h3{margin-bottom:12px}.shift .row{display:flex;gap:10px;margin:7px 0}.win{width:130px;font-size:19px;padding:8px 10px;background:#eef3f9;border-radius:4px;color:#34516f}.gsr{width:100px;font-size:19px;padding:8px 10px;border-radius:4px;color:#fff;text-align:center}.g1{background:#145ac7}.g2{background:#2f74d0}.g3{background:#5e9bd6}.g4{background:#88b4e2}.g5{background:#a9c8ec}.gsr.bad{outline:2px dashed #142a44}.shift .big b{display:block;font-family:Cambria,Georgia,serif;font-size:110px;font-weight:400;color:#142a44;line-height:1;margin-top:28px}.shift .big span{font-size:21px;line-height:1.45;color:#536b85}
.timeline3{display:grid;grid-template-columns:repeat(3,1fr);gap:34px;margin-top:20px}.timeline3 div{border-top:4px solid #145ac7;padding-top:20px}.timeline3 b{font-family:Cambria,Georgia,serif;font-size:32px;font-weight:400;color:#145ac7;display:block}.timeline3 span{display:block;font-size:19px;color:#536b85;margin:6px 0 16px;letter-spacing:.3px;text-transform:uppercase}.timeline3 p{font-size:23px;line-height:1.45}
@media(max-width:650px){.reading .strip-label{width:110px;font-size:13px}.reading .w{width:16px;height:22px}.reading .flow{flex-direction:column}.reading .arrow{transform:rotate(90deg)}.reading .shift,.reading .timeline3{grid-template-columns:1fr}}

.agenda{list-style:none;counter-reset:a;padding:0;margin:4px 0 0;columns:1}.agenda li{counter-increment:a;display:flex;align-items:baseline;gap:22px;padding:7px 0;border-bottom:1px solid #dce4ee}.agenda li:before{content:counter(a);font-family:Cambria,Georgia,serif;font-size:34px;color:#145ac7;width:34px}.agenda b{font-size:26px;font-weight:500;min-width:470px}.agenda span{font-size:20px;color:#536b85}
.facts{display:grid;grid-template-columns:repeat(4,1fr);gap:28px;margin-top:44px;border-top:1px solid #dce4ee;padding-top:26px}.facts b{display:block;font-family:Cambria,Georgia,serif;font-size:52px;font-weight:400;color:#145ac7;line-height:1}.facts span{display:block;font-size:18px;line-height:1.4;color:#536b85;margin-top:10px}
table.matrix{font-size:19px}table.matrix th{text-align:center}table.matrix th:first-child,table.matrix th:last-child{text-align:left}table.matrix td{padding:9px 10px;font-size:19px}table.matrix td:first-child{width:auto;font-weight:500}.matrix td.m{text-align:center;color:#145ac7;font-size:20px;width:70px}.matrix td.n{color:#536b85;font-size:17px}.matrix tr.me{background:#eef3f9!important}.matrix tr.me td{font-weight:600;color:#142a44}.matrix tr.me td.m{color:#142a44}
.gaps{display:grid;grid-template-columns:1fr 1fr;gap:56px}.gaps ol{padding-left:24px;margin:0}.gaps li{font-size:23px;line-height:1.4;margin-bottom:16px}
@media(max-width:650px){.reading .facts,.reading .gaps{grid-template-columns:1fr}.reading .agenda b{min-width:0;font-size:19px}.reading table.matrix td{font-size:12px;padding:5px}}

.kdd .box.step{min-height:230px;font-size:22px;padding:22px 16px}.kdd .box.step small{font-size:17px}.kdd .arrow{font-size:24px}
.cards4{display:grid;grid-template-columns:repeat(4,1fr);gap:22px}.cards4>div{background:#eef3f9;border-radius:6px;padding:20px 18px;display:flex;flex-direction:column}.cards4 h3{margin:0 0 10px;font-size:22px}.cards4 p{font-size:18px;line-height:1.4;margin:0 0 14px}.cards4 b{margin-top:auto;font-family:Cambria,Georgia,serif;font-size:44px;font-weight:400;color:#145ac7;line-height:1}.cards4 span{font-size:16px;color:#536b85;margin-top:6px}.cards4 span.foot{margin-top:auto;font-size:17px;color:#145ac7;font-weight:600}
.eval3{display:grid;grid-template-columns:repeat(3,1fr);gap:30px;margin-top:40px;border-top:1px solid #dce4ee;padding-top:24px}.eval3 b{display:block;font-size:24px;font-weight:600;color:#145ac7;margin-bottom:8px}.eval3 span{font-size:19px;line-height:1.45;color:#536b85}
@media(max-width:650px){.reading .cards4,.reading .eval3{grid-template-columns:1fr}}
'''
