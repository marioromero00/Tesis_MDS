from estilo_tecnico import img,table

# Versión 4 (15-11-2026): relato reescrito tras auditoría de estilo y cifras.
# Cada diapositiva define aquí su capítulo, título, cuerpo, notas del orador y fuentes.
# Las cifras provienen de los informes citados en `source`; los gráficos, de estilo_tecnico.py.

R='resultados/'
T29=R+'temporalidad_eeg_v2_test_29-10-2026/INFORME.md'
C30=R+'comparacion_comun_binaria_30-10-2026/INFORME.md'
GSR=R+'etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md'
ACT=R+'activacion_gsr_v2_recalculo_02-11-2026/'
ABL=R+'ablacion_modalidades_v2_01-11-2026/INFORME.md'
PROT=R+'protocolo_hipotesis_reintento_06-11-2026/'
HIP='../../documentos/01 Tesis MDS/Marco Teorico/Problema e hipótesis.md'

def para(t):return '<p class="prose">'+t+'</p>'
def caption(t):return '<p class="caption">'+t+'</p>'
def pair(left,right):return '<div class="editorial-pair"><div>'+left+'</div><div>'+right+'</div></div>'

def apply(old):
 out=[]
 def S(chapter,title,body,notes,source,kind=''):
  out.append(dict(chapter=chapter,title=title,body=body,notes=notes,source=source,kind=kind))
 D1='01 / HIPÓTESIS Y DISEÑO';D2='02 / ETAPAS PREVIAS';D3='03 / ATENCIÓN'
 D4='04 / CORRECCIÓN DE LA ETIQUETA DE ACTIVACIÓN';D5='05 / ACTIVACIÓN CON LA ETIQUETA GSR V2';D6='06 / SÍNTESIS Y DECISIONES'

 S('UNIVERSIDAD DE CHILE · MAGÍSTER EN CIENCIA DE DATOS',
   '¿El historial de señales mejora<br>la predicción de atención<br>y activación?',
   '<p class="cover-sub">Modelos multimodales con EEG, GSR, mirada y pupila<br>durante la navegación web</p>'
   '<div class="byline"><b>Mario Romero</b><span>Profesor guía: Dr. Juan D. Velásquez<br>Avance de tesis · resultados al 6 de noviembre de 2026</span></div>',
   'Hoy quiero mostrar qué pasó desde la última reunión: en atención hay una señal favorable, pero en activación encontré un error en la etiqueta, la corregí y al rehacer los modelos el resultado quedó cerca del azar. Al final traigo cuatro preguntas para decidir cómo cerrar.',
   HIP,'story-cover')

 S(D1,'La hipótesis',
   '<blockquote>«Los modelos temporales multimodales obtienen un mejor desempeño fuera de muestra que los modelos estáticos comparables en la detección de emociones y atención durante la navegación web.»</blockquote>'
   +pair('<h3>Cómo la contrasto</h3>'+para('Mismo modelo, misma etiqueta y mismas ventanas. Lo único que cambia es si el modelo recibe el historial de ventanas anteriores.'),
         '<h3>En qué resultados</h3>'+para('En dos resultados: atención y activación (GSR). La hipótesis pide la mejora en ambos.')),
   'Esta es la hipótesis tal como está en el manuscrito. Dice «emociones», pero lo que puedo medir con GSR es activación; eso lo dejo como pregunta al final. Para aislar el aporte del historial comparo siempre pares de modelos que solo difieren en eso. El tipo de fusión es el otro factor del diseño; hoy solo traigo una ablación parcial.',
   HIP)

 S(D1,'Las etiquetas salen de unas señales y se predicen con otras',
   table(['Resultado','Modelo Profesor: construye la etiqueta','Modelo Estudiante: la predice'],[['Atención','<i>Attention Score</i> con mirada + pupila','EEG + GSR'],['Activación','<i>Arousal Score</i> con GSR','EEG + mirada + pupila']])
   +caption('Son pseudoetiquetas: cada ventana es «alta» o «baja» respecto de la mediana de su persona, calculada con la sesión completa. La AUC (área bajo la curva ROC) mide qué tan bien se predice esa regla.'),
   'Los registros no traen una etiqueta directa. El Modelo Profesor la construye a partir de unas señales y el Modelo Estudiante la predice con las demás, para no usar la misma información en ambos lados. Como la mediana y la normalización usan la sesión completa, la etiqueta no sirve tal cual para predecir en línea.',
   R+'profesor_binario_reconstruido_29-10-2026/INFORME.md; '+GSR)

 S(D1,'Cada persona queda en una sola partición',
   '<div class="split-counts"><div><b>25</b><span>personas en entrenamiento</span></div><div><b>8</b><span>en validación</span></div><div><b>8</b><span>en test</span></div></div>'
   '<div class="method-line"><span><b>41</b> de 48 personas (6 excluidas por EEG o GSR; P29 en sensibilidad)</span><span>Ventanas de <b>2 s</b> con paso de <b>1 s</b></span><span>AUC media <b>por persona</b>, IC 95 % bootstrap por persona</span></div>'
   +caption('Validación y test ya se consultaron en etapas anteriores, así que todos los resultados que siguen son exploratorios.'),
   'De las 48 personas registradas, 41 entran al análisis principal: excluí 4 por EEG no utilizable y 2 sin GSR, y P29 queda solo para un análisis de sensibilidad por un desfase de sincronización. Como las ventanas se solapan, la unidad de análisis es la persona: promedio la AUC por persona y las diferencias entre modelos las calculo dentro de cada persona.',
   R+'modelado/particion_participantes.csv; documentacion/Modelos_Temporales_07-09-2026.md')

 S(D2,'Septiembre: armé el pipeline y las comparaciones base',
   table(['Etapa','Qué probé','Para qué'],[['Modelos sin historial','Logística, Random Forest, CatBoost y HGB (Histogram Gradient Boosting)','Tener una referencia con solo la ventana actual'],['Redes temporales','Redes convolucionales temporales (TCN), LSTM y BiLSTM','Separar el aporte del historial del de la arquitectura'],['Fusión','Temprana y tardía, señales por separado','Ver si combinar señales supera a cada una']])
   +caption('Esa etapa usó etiquetas anteriores, así que sus métricas no se comparan con las de ahora. Lo que me sirvió de esa etapa fue el pipeline y la forma de comparar.'),
   'En la primera comparación temporal entrené 104 redes. No traigo esas cifras porque las etiquetas cambiaron después; además, la auditoría de noviembre encontró que el generador de la etiqueta de activación de esa época tenía un error.',
   'documentacion/Modelos_Temporales_07-09-2026.md; documentacion/Fusiones_10-09-2026.md')

 S(D2,'Octubre: nueva etiqueta de atención y EEG por canal',
   pair('<h3>La etiqueta de atención</h3>'+para('Recalculé el Modelo Profesor desde mirada y pupila y comparé dos formas de combinarlas: pesos iguales y PCA ajustado dentro de cada fold.')+para('Seguí con PCA, que los Modelos Estudiante predecían mejor; eso no prueba que mida mejor la atención. Las dos versiones coinciden en el 66 % de las ventanas (kappa 0,33), así que la elección pesa.'),
        '<h3>Los predictores EEG</h3><p class="feature-count">16 <span>canales por separado</span></p>'+para('Antes promediaba los canales. Recuperé los archivos crudos y extraje 342 variables EEG nuevas.')),
   'Los crudos los recuperé y verifiqué su integridad; las muestras y la selección temporal coinciden con el procesamiento anterior. No atribuyo localización anatómica a los canales porque no tengo el mapa de electrodos.',
   'documentacion/Crudos_V2_y_EEG_Por_Canal_29-10-2026.md; '+R+'profesor_binario_reconstruido_29-10-2026/INFORME.md')

 S(D3,'En atención, el historial suma +0,028 de AUC,<br>pero el intervalo incluye cero',
   table(['Atención · test · 8 personas','AUC','IC 95 %'],[['HGB · solo ventana actual','0,660','[0,614; 0,704]'],['HGB · hasta 32 ventanas','<b>0,688</b>','[0,643; 0,730]'],['<span class="ref">Referencia: CatBoost · solo ventana actual</span>','<span class="ref">0,674</span>','<span class="ref">[0,635; 0,712]</span>']])
   +'<div class="contrast-line"><strong>+0,028</strong><span>HGB con historial − sin historial<br>IC 95 % [−0,004; +0,051]</span><p>Mejora en 7 de 8 personas.<br>Frente al CatBoost: +0,014 [−0,015; +0,034]</p></div>',
   'Creo que el 0,67 que comentamos antes es este CatBoost, el mejor sin historial de este análisis (0,674 en test); si se refería a otro, lo reviso. La comparación justa es la del HGB con y sin historial, con los mismos parámetros: sube 0,028 y mejora en 7 de las 8 personas, pero el intervalo toca el cero. Frente al CatBoost la diferencia es la mitad. Este contraste lo fijé como principal antes de mirar test. Me falta revisar cuánto historial tuvo realmente cada ventana en atención, como hice para activación en la lámina 16.',
   T29)

 S(D3,'Con otra representación del historial la mejora<br>sube a +0,033, pero la elegí después de ver test',
   img('contrastes_atencion','Atención · test · diferencia de AUC por persona con IC 95 % bootstrap. Ambas filas usan el mismo test.'),
   'El 29 de octubre el historial resumía el panel EEG/GSR anterior y las potencias relativas por canal; el 30 pasé a media y desviación de todas las variables. En atención el intervalo ya no toca el cero. Lo tomo con cuidado: elegí esa representación después de ver el primer resultado, y en esa misma corrida la activación, todavía con la etiqueta antigua, bajó 0,079 [−0,129; −0,030].',
   T29+'; '+C30)

 S(D4,'Antes de la auditoría ya había señales de alerta<br>en la etiqueta de activación',
   pair('<p class="opening">P4: solo el <b>12,6 %</b><br>de sus ventanas<br>tenía GSR válido.</p><p class="opening-sub">Pero todas sus ventanas recibían etiqueta.</p>',
        '<h3>Otras señales de alerta</h3>'+para('Empates, personas con clases muy desbalanceadas (P34 tenía 8,6 % de positivos) y poco historial completo.')+para('Por eso dejé de ajustar modelos y revisé primero cómo se construía la etiqueta.')),
   'Los resultados de activación que tenía se podían reproducir, pero eso no me decía nada sobre cómo estaba construida la etiqueta. Por eso la audité.',
   R+'activacion_diagnostico_nested_30-10-2026/INFORME.md; ../../notas/bitacora.md')

 S(D4,'La auditoría encontró un error de índices<br>en el generador de la etiqueta',
   '<p class="intro">Al agrupar por persona y reiniciar el índice, los componentes GSR quedaban asignados a ventanas que no les correspondían.</p>'
   '<div class="audit-layout"><div><b>25.498</b><span>de 25.992 posiciones del archivo completo (98 %;<br>incluye personas fuera del análisis) quedaron desplazadas</span></div><div><p>Si reproduzco el cálculo con el error, obtengo los mismos puntajes que tenía guardados (diferencias menores que 10⁻⁶).</p><p>Las AUC de activación anteriores dejan de servir como evidencia.</p></div></div>',
   'Al reagrupar por persona se perdía el índice original de cada ventana. Ojo, eso no es cuántas etiquetas cambiaron de clase; ese número no lo tengo separado del cambio de reglas de V2. Las diferencias al reproducir fueron del orden de 10⁻⁷, que es la precisión con que se exportó. El mismo patrón aparece en el Modelo Profesor histórico de atención; esta auditoría no revisó la etiqueta de atención de octubre; eso lo tengo pendiente.',
   GSR+'; '+R+'etiquetas_gsr_calidad_v2_01-11-2026/auditoria_independiente_02-11-2026.json')

 S(D4,'Reconstruí la etiqueta de activación (GSR V2)',
   table(['Paso','Regla'],[['1 · Calidad','Cobertura de al menos 50 %, cuatro componentes válidos y respuestas de conductancia (SCR) no negativas'],['2 · Normalización','Solo con ventanas válidas, sin perder a qué ventana pertenece cada valor'],['3 · Contexto','Cinco ventanas válidas seguidas para calcular el puntaje de 6 s'],['4 · Clase','Mediana de cada persona; los empates quedan sin etiqueta']])
   +caption('El contexto se reinicia si hay un hueco o cambia el estímulo.'),
   'Cinco ventanas de dos segundos con paso de uno cubren seis segundos. Si un componente es constante aporta cero; si falta, la ventana queda sin puntaje. Todo esto lo calculo sobre las variables que ya tenía extraídas.',
   GSR)

 S(D4,'La etiqueta GSR V2 deja 11.796 ventanas (53 %)',
   img('retencion','De las 10.415 ventanas sin etiqueta, 9.995 no completan cinco ventanas válidas seguidas (la actual y las cuatro anteriores), 401 no cumplen la calidad GSR y 19 son empates. Las 41 personas conservan ambas clases.'),
   'Las 22.211 filas originales se conservan con su motivo de exclusión. Casi toda la pérdida viene de exigir cinco ventanas seguidas dentro del mismo estímulo; por calidad de señal se pierden solo 401. El caso extremo es P4, que conserva 26 de 459 ventanas.',
   GSR)

 S(D5,'Volví a entrenar desde cero con la etiqueta GSR V2',
   table(['Decisión','Cómo'],[['Modelo','HGB con tres contextos: solo ventana actual, hasta 8 y hasta 32'],['Contraste principal','Hasta 32 frente a solo ventana actual, fijado en el protocolo de la primera corrida V2'],['Selección','5 folds por persona dentro de entrenamiento; una configuración común'],['Comprobación','Repetí todo y obtuve exactamente los mismos números que el 1 de noviembre']])
   +caption('Mismas filas, personas y etiquetas en todos los contextos. Detalle de la configuración en el anexo D.'),
   'Lo repetí después de auditar la etiqueta, para asegurarme de que los números salían del código corregido. El modelo con historial recibe la ventana actual más la media y la desviación del historial disponible. Hasta 8 quedó definido como secundario desde el protocolo.',
   ACT+'protocolo.json; '+ACT+'auditoria_desde_disco.json')

 S(D5,'Con la etiqueta GSR V2, la activación queda cerca del azar (AUC 0,51–0,55)',
   img('auc_activacion','HGB con EEG, mirada y pupila · AUC media por persona e IC 95 % bootstrap. En test, los tres intervalos incluyen 0,50.'),
   'Test son 8 personas y 2.184 ventanas. Ninguno de los tres modelos se separa del azar en test. Esto no lo leo como que el historial no sirve: con un modelo que casi no discrimina, una diferencia entre contextos es difícil de interpretar.',
   ACT+'INFORME.md')

 S(D5,'En activación, el contraste principal (+0,022) incluye cero;<br>«hasta 8» sube solo en test',
   img('contrastes_activacion','Diferencias por persona con IC 95 % bootstrap. OOF: entrenamiento evaluado fuera de fold.'),
   'El contraste principal es positivo en las tres particiones, pero en ninguna se distingue de cero y en test mejora en 4 de 8 personas. Hasta 8 mejora en 7 de 8 personas en test; como es el secundario y no aparece en validación ni en entrenamiento, no lo tomo como resultado. Las diferencias las calculo dentro de cada persona.',
   ACT+'contrastes.csv')

 S(D5,'«Hasta 32 ventanas» tuvo en promedio 8,7:<br>ninguna ventana de test llegó a 32',
   img('historial','Activación GSR V2 · test, ponderado por ventanas. El historial se corta en huecos, cambios de estímulo y ventanas sin etiqueta. El modelo recibe la media y la desviación del historial.'),
   'Esto viene de la etiqueta: como V2 exige cinco ventanas válidas seguidas y el historial solo usa filas etiquetadas, se pierden las ventanas iniciales. Entonces lo que evalué es un resumen de un historial corto; en la tesis tengo que describirlo así.',
   ACT+'INFORME.md')

 S(D5,'En activación, la fusión no se distingue de cada señal sola;<br>con AUC cercanas a 0,5, esto dice poco',
   img('ablaciones','Activación GSR V2 · test · 8 personas · diferencia de AUC por persona entre la fusión y cada señal sola, con IC 95 % bootstrap. Los nueve intervalos incluyen cero.'),
   'Son 54 modelos nuevos con los mismos parámetros, personas y filas. Como casi todas las AUC están cerca de 0,5, esta comparación sirve poco para decidir sobre la fusión; hay un par de intervalos aislados que excluyen 0,5, como pupila con hasta 8 en test, pero sin corregir por comparaciones múltiples. Además solo compara fusión temprana con cada señal sola; temprana, intermedia y tardía con GSR V2 está pendiente.',
   ABL)

 S(D6,'Atención muestra una mejora sin confirmar;<br>activación no se separa del azar',
   table(['','Atención','Activación (GSR V2)'],[['AUC en test','0,66–0,69','0,51–0,55'],['Aporte del historial','+0,028 (IC incluye cero)<br>+0,033 con otra representación elegida después','+0,022 en test; el IC incluye cero en test, validación y entrenamiento<br>hasta 8: +0,033 solo en test'],['Cómo lo leo','Mejora sin confirmar','El modelo multimodal no se distingue de 0,5']])
   +caption('Con los criterios del manuscrito, hoy no hay una ventaja consistente en ninguno de los dos resultados. Si la señal de atención se confirmara, la hipótesis tendría apoyo parcial.'),
   'En atención el modelo predice la etiqueta y el historial ayuda un poco, pero no lo puedo confirmar. En activación el modelo no predice, así que no puedo decir nada del historial. Me falta revisar si el error de índices toca la etiqueta de atención.',
   'documentacion/Cierre_Experimental_V2_01-11-2026.md; '+ACT+'INFORME.md')

 S(D6,'Si planifico una cohorte nueva,<br>¿cuántas personas harían falta?',
   table(['Resultado','Variabilidad que uso para el cálculo','Personas evaluables'],[['Atención','La del test','62'],['Activación','La de validación','72'],['Activación','La del test','101'],['Activación','La de entrenamiento (OOF)','767']])
   +caption('Supuestos: mejora mínima relevante +0,02 AUC, efecto real +0,04, potencia 90 % e IC de 97,5 % por resultado. Si las mismas personas aportan a ambos resultados, manda el N mayor. Con 20 % de pérdidas habría que reclutar 78 (atención) y hasta 959 (activación). En activación el cálculo supone un modelo que predice la etiqueta; con AUC ≈ 0,5 lo tomo solo como referencia.'),
   'El N de activación depende mucho de qué variabilidad uso. Las estimaciones de validación y test salen de solo 8 personas; la de entrenamiento sale de 25, pero mezcla modelos de distintos folds, así que el 767 lo tomo como escenario pesimista. Los cálculos los comprobé simulando 100.000 veces cada escenario. El +0,02 es una propuesta mía, todavía sin justificación independiente.',
   PROT+'INFORME.md; '+PROT+'verificacion_simulada.json')

 S(D6,'Cuatro decisiones para cerrar la evaluación',
   '<ol class="questions">'
   '<li><b>¿Cierro con los datos actuales o planifico una cohorte nueva?</b><span>Con los datos actuales el resultado queda inconcluso. Una cohorte nueva permitiría un contraste definido de antemano, si es factible reclutar.</span></li>'
   '<li><b>¿Qué cuenta como «mejor»?</b><span>Cualquier mejora mayor que 0, como dice la hipótesis, o una mejora mínima relevante, por ejemplo +0,02 AUC.</span></li>'
   '<li><b>¿Acepto etiquetas normalizadas con la sesión completa?</b><span>El manuscrito pide normalizar solo con entrenamiento; habría que ajustar esa redacción.</span></li>'
   '<li><b>¿Escribo «activación (GSR)» en lugar de «emociones»?</b><span>La GSR por sí sola no sostiene afirmaciones sobre emoción en sentido amplio.</span></li>'
   '</ol><p class="next-step">Mientras tanto: reviso si el error de índices afecta la etiqueta de atención y comparo fusión temprana, intermedia y tardía con GSR V2.</p>',
   'Lo que está resuelto: el error de la etiqueta de activación, el reentrenamiento con la etiqueta corregida y la comparación en igualdad de condiciones. Lo que necesito de usted son estas cuatro decisiones; la primera define cómo sigue el resto del trabajo.',
   PROT+'INFORME.md; ../../notas/pautas-escritura-recuperadas.md','closing-questions')

 AX='ANEXO'
 S(AX+' A · CURVAS ROC','Atención: curvas ROC en test',
   img('roc_atencion','Curvas por persona interpoladas sobre una malla común y promediadas (8 personas). La AUC de la leyenda es la media de las AUC por persona.'),
   'La AUC de la leyenda es la media de las AUC por persona; coincide con la de las tablas.',
   T29+'; '+R+'temporalidad_eeg_v2_test_29-10-2026/predicciones_test.csv.gz')
 S(AX+' B · CURVAS ROC','Activación GSR V2: curvas ROC en test',
   img('roc_activacion','8 personas · 2.184 ventanas. Misma construcción que el anexo A.'),
   'Las tres curvas quedan pegadas a la diagonal, que es lo mismo que muestran las AUC.',
   ACT+'predicciones_externas.csv.gz; '+ACT+'metricas.csv')
 S(AX+' C · DATOS','Señales disponibles',
   table(['Señal','Qué uso'],[['EEG','Potencia por banda, descriptores espectrales y temporales por canal'],['GSR','Componentes tónico y fásico, respuestas SCR'],['Mirada','Fijaciones, dispersión y trayectoria'],['Pupila','Cambios en el diámetro pupilar']])
   +caption('Toma de Muestra 2: registros de navegación web de 2025. No incluye expresión facial.'),
   'Son medidas fisiológicas y de mirada; ninguna es un autorreporte.',
   HIP+'; ../../documentos/01 Tesis MDS/Analisis de Datos/DOCUMENTACION_DATOS_MDS.md')
 S(AX+' D · CONFIGURACIÓN','Configuración del entrenamiento de activación',
   table(['Componente','Valor'],[['Estimador','HistGradientBoostingClassifier (HGB)'],['Búsqueda interna','7 o 15 hojas · 5 folds por persona · solo ventana actual, hasta 8 y hasta 32'],['Configuración final','15 hojas · 300 iteraciones · tasa de aprendizaje 0,05 · L2 = 10'],['Preprocesamiento','Mediana, indicadores de ausencia y estandarización, ajustados solo en entrenamiento'],['Volumen','30 ajustes internos · 15 modelos OOF · 3 modelos finales']])
   +caption('min_samples_leaf = 30 · sin early stopping · semilla 20261101 · ponderación por persona y clase.'),
   'La misma configuración se comparte entre los tres contextos para que la única diferencia sea el historial.',
   ACT+'protocolo.json')
 S(AX+' E · PROTOCOLO','Regla de decisión propuesta para una cohorte nueva',
   table(['Si…','Entonces'],[['Ambos límites inferiores superan el margen','Respaldo la mejora en ambos resultados'],['Algún límite superior queda bajo el margen','Rechazo esa mejora para estos modelos'],['Los intervalos cruzan el margen','El resultado queda inconcluso']])
   +caption('Intervalos de 97,5 % por resultado para controlar ambos a la vez. Modelos, etiquetas y contexto principal se fijan antes de evaluar.'),
   'La regla la dejo escrita antes de tener datos, sabiendo que puede terminar en inconcluso. Si rechazo +0,02, igual puede haber una mejora más chica.',
   PROT+'INFORME.md')
 S(AX+' F · FUENTES','De dónde sale cada cifra',
   '<ol class="sources"><li>Hipótesis · manuscrito (vault del 24-09-2026)</li><li>Primeras redes y fusión · septiembre de 2026</li><li>Modelo Profesor de atención y EEG por canal · 29 de octubre</li><li>Historial en atención · 29 y 30 de octubre</li><li>Auditoría y etiqueta GSR V2 · 1 y 2 de noviembre</li><li>Ablación (1 de noviembre), reentrenamiento y protocolo (2 al 6 de noviembre)</li></ol>'
   +caption('Las rutas exactas de cada informe están en FUENTES.md y en las notas de cada lámina.'),
   'Si quiere revisar alguna cifra en detalle, le puedo mostrar el informe correspondiente.',
   'FUENTES.md')
 for x in out:
  for k in ('title','body'):x[k]=x[k].replace(' %','\u00a0%')
 for i in [1,2,3,5,8,22]:out[i]['kind']=(out[i]['kind']+' roomy').strip()
 return out

CSS='''
:root{--ink:#142a44;--muted:#5e7085;--line:#dce4ee;--paper:#fff;--accent:#145ac7}
body{background:#e8edf3;font-family:"Helvetica Neue",Arial,sans-serif}.slide{border:0;padding:48px 70px 45px}.slide:before{content:'';position:absolute;left:70px;right:70px;top:88px;height:1px;background:#dce4ee}.chapter{height:32px;margin:0 0 35px;color:#34516f;letter-spacing:1.6px;font-size:13px;font-weight:500}h1{font-weight:500;font-size:43px;line-height:1.15;letter-spacing:-1.35px;margin-bottom:35px;max-width:1120px}h3{font-size:17px;color:#185bac;letter-spacing:.1px;font-weight:600;margin-bottom:16px}p{font-size:23px;line-height:1.43}.prose{font-size:25px;line-height:1.45;margin-bottom:25px}.editorial-pair{display:grid;grid-template-columns:1.1fr 1fr;gap:85px;padding-top:16px}.opening{font-size:40px;line-height:1.25;letter-spacing:-1.3px}.opening span{color:#60758d}.opening b{color:#145ac7;font-weight:500}.intro{font-size:29px;line-height:1.4;letter-spacing:-.3px;margin-bottom:35px}.caption{font-size:18px;line-height:1.4;color:#5b6d82;margin-top:26px;border:0;padding:0;max-width:1080px}table{font-size:23px}th{font-size:14px;border-bottom:1px solid #6a8baa;letter-spacing:.65px;padding-bottom:16px;color:#34516f}td{font-size:22px;line-height:1.35;padding:20px 22px 20px 0;border-bottom:1px solid #dce4ee}tbody tr:nth-child(even){background:white}table td:first-child{width:29%;font-weight:500;color:#185bac}.story-cover:before{display:none}.story-cover .chapter{margin-bottom:70px;color:#145ac7}.story-cover h1{font-size:61px;line-height:1.12;letter-spacing:-2.5px;font-weight:500;max-width:1090px;margin-bottom:30px}.cover-sub{font-size:25px;line-height:1.4;color:#61748c}.byline{margin-top:52px;display:flex;gap:55px;align-items:flex-start;border-top:1px solid #dce4ee;padding-top:24px;width:100%}.byline b{font-size:21px;font-weight:500}.byline span{font-size:17px;line-height:1.55;color:#61748c}.split-counts{display:grid;grid-template-columns:repeat(3,1fr);gap:60px;margin:38px 0 48px}.split-counts b{font-size:108px;font-weight:400;letter-spacing:-5px;line-height:1;color:#145ac7}.split-counts span{display:block;font-size:22px;margin-top:16px;color:#536b85}.method-line{display:flex;gap:55px;border-top:1px solid #dce4ee;padding-top:28px;font-size:21px}.method-line b{font-weight:500;color:#145ac7}.feature-count{font-size:85px;color:#145ac7;line-height:1;letter-spacing:-3px;margin:16px 0 22px}.feature-count span{font-size:27px;letter-spacing:0;color:#61748c}.result-number{font-size:117px;color:#145ac7;letter-spacing:-7px;line-height:1;margin-top:22px}.metric-label{font-size:20px;color:#536b85;margin-top:20px}.secondary-number{font-size:38px;margin-top:38px;color:#34516f;letter-spacing:-1px}.secondary-number span{font-size:20px;letter-spacing:0;margin-left:10px}.result-slide .editorial-pair{grid-template-columns:1.1fr 1fr}.contrast-line{display:flex;gap:32px;align-items:center;margin-top:40px}.contrast-line strong{font-size:66px;font-weight:400;letter-spacing:-3px;color:#145ac7}.contrast-line span{font-size:20px;line-height:1.5;color:#536b85}.contrast-line p{font-size:22px;margin:0 0 0 auto;line-height:1.5}.person-id{font-size:17px;letter-spacing:1px;color:#145ac7;margin-bottom:20px}.audit-layout{display:grid;grid-template-columns:1fr 1.2fr;gap:60px;margin-top:40px}.audit-layout b{font-size:84px;font-weight:400;color:#145ac7;letter-spacing:-4px;line-height:1}.audit-layout span{display:block;font-size:19px;line-height:1.5;margin-top:18px;color:#61748c}.audit-layout p{font-size:24px;margin-bottom:25px}.data-figure img{height:400px}.data-figure figcaption{font-size:17px;margin-top:14px;border-top:0;padding:0;line-height:1.45}.next-decision{display:grid;grid-template-columns:245px 1fr;column-gap:42px;row-gap:22px;padding-top:15px}.next-decision h3,.next-decision p{padding:0 0 23px;margin:0;border-bottom:1px solid #dce4ee}.next-decision h3{font-size:21px;line-height:1.5}.next-decision p{font-size:27px;line-height:1.4}.folio{bottom:27px;right:70px;font-size:12px;color:#7b8b9b}.technical-note{border:0;padding:0;font-size:18px;margin-top:25px}.data-figure{margin:0}.dialog h2{font-weight:500}.index-list button{padding:16px 0}nav{background:#fff}nav button{color:#536b85}#counter{color:#536b85}.steps{font-size:22px}.columns{gap:80px}.lead{font-size:27px}
@media(max-width:650px){.reading .slide:before{display:none}.reading .chapter{height:auto;margin-bottom:24px;font-size:10px}.reading .editorial-pair,.reading .audit-layout,.reading .next-decision{grid-template-columns:1fr;gap:22px}.reading .opening{font-size:31px}.reading .prose,.reading .intro,.reading .audit-layout p{font-size:21px}.reading .story-cover h1{font-size:37px;letter-spacing:-1.2px}.reading .story-cover .chapter{margin-bottom:35px}.reading .cover-sub{font-size:21px}.reading .byline{margin-top:35px;gap:25px}.reading .byline span{font-size:14px}.reading .byline b{font-size:18px}.reading .split-counts{gap:18px;margin:25px 0}.reading .split-counts b{font-size:60px;letter-spacing:-3px}.reading .split-counts span{font-size:14px}.reading .method-line{display:block;font-size:18px}.reading .method-line span{display:block;margin-bottom:12px}.reading .caption{font-size:16px}.reading .result-number{font-size:82px;letter-spacing:-4px}.reading .contrast-line{flex-wrap:wrap;gap:18px}.reading .contrast-line strong{font-size:52px}.reading .contrast-line span,.reading .contrast-line p{font-size:18px;margin:0}.reading .audit-layout b{font-size:66px}.reading .next-decision h3{padding-bottom:0;border:0;font-size:18px}.reading .next-decision p{font-size:21px}.reading .feature-count{font-size:64px}}

h1{font-family:Cambria,Georgia,"Times New Roman",serif;font-weight:400;letter-spacing:-.6px;font-size:42px}.story-cover h1{font-family:Cambria,Georgia,serif;font-weight:400;letter-spacing:-1.2px;font-size:58px}
blockquote{font-family:Cambria,Georgia,serif;font-size:34px;line-height:1.3;color:#142a44;border-left:4px solid #145ac7;padding-left:28px;margin:10px 0 40px}
.opening-sub{font-size:24px;color:#60758d;margin-top:22px}
.questions{list-style:none;counter-reset:q;padding:0;margin:6px 0 0}.questions li{counter-increment:q;position:relative;padding:15px 0 15px 62px;border-bottom:1px solid #dce4ee}.questions li:before{content:counter(q);position:absolute;left:0;top:12px;font-family:Cambria,Georgia,serif;font-size:36px;color:#145ac7;line-height:1}.questions b{display:block;font-size:24px;font-weight:600;margin-bottom:5px}.questions span{font-size:19px;line-height:1.4;color:#536b85}
.sources{font-size:23px;line-height:1.5}.ref{color:#7b8b9b;font-weight:400}.next-step{font-size:20px;color:#145ac7;margin-top:22px}.roomy td{font-size:26px;padding-top:26px;padding-bottom:26px}.roomy th{font-size:15px}.roomy .prose{font-size:28px}.roomy .caption{font-size:21px;margin-top:34px}.roomy h3{font-size:20px}.roomy blockquote{font-size:37px;margin-bottom:50px}.roomy .split-counts{margin:50px 0 60px}.roomy .opening{font-size:46px}.roomy .opening-sub{font-size:27px}.data-figure img{height:372px}
td{font-size:23px}
@media(max-width:650px){.reading blockquote{font-size:22px}.reading .questions b{font-size:19px}.reading .questions span{font-size:16px}.reading .questions li{padding-left:40px}.reading h1{font-size:30px}}
'''
