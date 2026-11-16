# Avances de tesis · guion editable

## 01. ¿El historial de señales mejora la predicción de atención y activación?

Hoy quiero mostrar qué pasó desde la última reunión: en atención hay una señal favorable, pero en activación encontré un error en la etiqueta, la corregí y al rehacer los modelos el resultado quedó cerca del azar. Al final traigo cuatro preguntas para decidir cómo cerrar.

Fuente: ../../documentos/01 Tesis MDS/Marco Teorico/Problema e hipótesis.md

## 02. La hipótesis

Esta es la hipótesis tal como está en el manuscrito. Dice «emociones», pero lo que puedo medir con GSR es activación; eso lo dejo como pregunta al final. Para aislar el aporte del historial comparo siempre pares de modelos que solo difieren en eso. El tipo de fusión es el otro factor del diseño; hoy solo traigo una ablación parcial.

Fuente: ../../documentos/01 Tesis MDS/Marco Teorico/Problema e hipótesis.md

## 03. Las etiquetas salen de unas señales y se predicen con otras

Los registros no traen una etiqueta directa. El Modelo Profesor la construye a partir de unas señales y el Modelo Estudiante la predice con las demás, para no usar la misma información en ambos lados. Como la mediana y la normalización usan la sesión completa, la etiqueta no sirve tal cual para predecir en línea.

Fuente: resultados/profesor_binario_reconstruido_29-10-2026/INFORME.md; resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md

## 04. Cada persona queda en una sola partición

De las 48 personas registradas, 41 entran al análisis principal: excluí 4 por EEG no utilizable y 2 sin GSR, y P29 queda solo para un análisis de sensibilidad por un desfase de sincronización. Como las ventanas se solapan, la unidad de análisis es la persona: promedio la AUC por persona y las diferencias entre modelos las calculo dentro de cada persona.

Fuente: resultados/modelado/particion_participantes.csv; documentacion/Modelos_Temporales_07-09-2026.md

## 05. Septiembre: armé el pipeline y las comparaciones base

En la primera comparación temporal entrené 104 redes. No traigo esas cifras porque las etiquetas cambiaron después; además, la auditoría de noviembre encontró que el generador de la etiqueta de activación de esa época tenía un error.

Fuente: documentacion/Modelos_Temporales_07-09-2026.md; documentacion/Fusiones_10-09-2026.md

## 06. Octubre: nueva etiqueta de atención y EEG por canal

Los crudos los recuperé y verifiqué su integridad; las muestras y la selección temporal coinciden con el procesamiento anterior. No atribuyo localización anatómica a los canales porque no tengo el mapa de electrodos.

Fuente: documentacion/Crudos_V2_y_EEG_Por_Canal_29-10-2026.md; resultados/profesor_binario_reconstruido_29-10-2026/INFORME.md

## 07. En atención, el historial suma +0,028 de AUC, pero el intervalo incluye cero

Creo que el 0,67 que comentamos antes es este CatBoost, el mejor sin historial de este análisis (0,674 en test); si se refería a otro, lo reviso. La comparación justa es la del HGB con y sin historial, con los mismos parámetros: sube 0,028 y mejora en 7 de las 8 personas, pero el intervalo toca el cero. Frente al CatBoost la diferencia es la mitad. Este contraste lo fijé como principal antes de mirar test. Me falta revisar cuánto historial tuvo realmente cada ventana en atención, como hice para activación en la lámina 16.

Fuente: resultados/temporalidad_eeg_v2_test_29-10-2026/INFORME.md

## 08. Con otra representación del historial la mejora sube a +0,033, pero la elegí después de ver test

El 29 de octubre el historial resumía el panel EEG/GSR anterior y las potencias relativas por canal; el 30 pasé a media y desviación de todas las variables. En atención el intervalo ya no toca el cero. Lo tomo con cuidado: elegí esa representación después de ver el primer resultado, y en esa misma corrida la activación, todavía con la etiqueta antigua, bajó 0,079 [−0,129; −0,030].

Fuente: resultados/temporalidad_eeg_v2_test_29-10-2026/INFORME.md; resultados/comparacion_comun_binaria_30-10-2026/INFORME.md

## 09. Antes de la auditoría ya había señales de alerta en la etiqueta de activación

Los resultados de activación que tenía se podían reproducir, pero eso no me decía nada sobre cómo estaba construida la etiqueta. Por eso la audité.

Fuente: resultados/activacion_diagnostico_nested_30-10-2026/INFORME.md; ../../notas/bitacora.md

## 10. La auditoría encontró un error de índices en el generador de la etiqueta

Al reagrupar por persona se perdía el índice original de cada ventana. Ojo, eso no es cuántas etiquetas cambiaron de clase; ese número no lo tengo separado del cambio de reglas de V2. Las diferencias al reproducir fueron del orden de 10⁻⁷, que es la precisión con que se exportó. El mismo patrón aparece en el Modelo Profesor histórico de atención; esta auditoría no revisó la etiqueta de atención de octubre; eso lo tengo pendiente.

Fuente: resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md; resultados/etiquetas_gsr_calidad_v2_01-11-2026/auditoria_independiente_02-11-2026.json

## 11. Reconstruí la etiqueta de activación (GSR V2)

Cinco ventanas de dos segundos con paso de uno cubren seis segundos. Si un componente es constante aporta cero; si falta, la ventana queda sin puntaje. Todo esto lo calculo sobre las variables que ya tenía extraídas.

Fuente: resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md

## 12. La etiqueta GSR V2 deja 11.796 ventanas (53 %)

Las 22.211 filas originales se conservan con su motivo de exclusión. Casi toda la pérdida viene de exigir cinco ventanas seguidas dentro del mismo estímulo; por calidad de señal se pierden solo 401. El caso extremo es P4, que conserva 26 de 459 ventanas.

Fuente: resultados/etiquetas_gsr_calidad_v2_01-11-2026/INFORME.md

## 13. Volví a entrenar desde cero con la etiqueta GSR V2

Lo repetí después de auditar la etiqueta, para asegurarme de que los números salían del código corregido. El modelo con historial recibe la ventana actual más la media y la desviación del historial disponible. Hasta 8 quedó definido como secundario desde el protocolo.

Fuente: resultados/activacion_gsr_v2_recalculo_02-11-2026/protocolo.json; resultados/activacion_gsr_v2_recalculo_02-11-2026/auditoria_desde_disco.json

## 14. Con la etiqueta GSR V2, la activación queda cerca del azar (AUC 0,51–0,55)

Test son 8 personas y 2.184 ventanas. Ninguno de los tres modelos se separa del azar en test. Esto no lo leo como que el historial no sirve: con un modelo que casi no discrimina, una diferencia entre contextos es difícil de interpretar.

Fuente: resultados/activacion_gsr_v2_recalculo_02-11-2026/INFORME.md

## 15. En activación, el contraste principal (+0,022) incluye cero; «hasta 8» sube solo en test

El contraste principal es positivo en las tres particiones, pero en ninguna se distingue de cero y en test mejora en 4 de 8 personas. Hasta 8 mejora en 7 de 8 personas en test; como es el secundario y no aparece en validación ni en entrenamiento, no lo tomo como resultado. Las diferencias las calculo dentro de cada persona.

Fuente: resultados/activacion_gsr_v2_recalculo_02-11-2026/contrastes.csv

## 16. «Hasta 32 ventanas» tuvo en promedio 8,7: ninguna ventana de test llegó a 32

Esto viene de la etiqueta: como V2 exige cinco ventanas válidas seguidas y el historial solo usa filas etiquetadas, se pierden las ventanas iniciales. Entonces lo que evalué es un resumen de un historial corto; en la tesis tengo que describirlo así.

Fuente: resultados/activacion_gsr_v2_recalculo_02-11-2026/INFORME.md

## 17. En activación, la fusión no se distingue de cada señal sola; con AUC cercanas a 0,5, esto dice poco

Son 54 modelos nuevos con los mismos parámetros, personas y filas. Como casi todas las AUC están cerca de 0,5, esta comparación sirve poco para decidir sobre la fusión; hay un par de intervalos aislados que excluyen 0,5, como pupila con hasta 8 en test, pero sin corregir por comparaciones múltiples. Además solo compara fusión temprana con cada señal sola; temprana, intermedia y tardía con GSR V2 está pendiente.

Fuente: resultados/ablacion_modalidades_v2_01-11-2026/INFORME.md

## 18. Atención muestra una mejora sin confirmar; activación no se separa del azar

En atención el modelo predice la etiqueta y el historial ayuda un poco, pero no lo puedo confirmar. En activación el modelo no predice, así que no puedo decir nada del historial. Me falta revisar si el error de índices toca la etiqueta de atención.

Fuente: documentacion/Cierre_Experimental_V2_01-11-2026.md; resultados/activacion_gsr_v2_recalculo_02-11-2026/INFORME.md

## 19. Si planifico una cohorte nueva, ¿cuántas personas harían falta?

El N de activación depende mucho de qué variabilidad uso. Las estimaciones de validación y test salen de solo 8 personas; la de entrenamiento sale de 25, pero mezcla modelos de distintos folds, así que el 767 lo tomo como escenario pesimista. Los cálculos los comprobé simulando 100.000 veces cada escenario. El +0,02 es una propuesta mía, todavía sin justificación independiente.

Fuente: resultados/protocolo_hipotesis_reintento_06-11-2026/INFORME.md; resultados/protocolo_hipotesis_reintento_06-11-2026/verificacion_simulada.json

## 20. Cuatro decisiones para cerrar la evaluación

Lo que está resuelto: el error de la etiqueta de activación, el reentrenamiento con la etiqueta corregida y la comparación en igualdad de condiciones. Lo que necesito de usted son estas cuatro decisiones; la primera define cómo sigue el resto del trabajo.

Fuente: resultados/protocolo_hipotesis_reintento_06-11-2026/INFORME.md; ../../notas/pautas-escritura-recuperadas.md

## 21. Atención: curvas ROC en test

La AUC de la leyenda es la media de las AUC por persona; coincide con la de las tablas.

Fuente: resultados/temporalidad_eeg_v2_test_29-10-2026/INFORME.md; resultados/temporalidad_eeg_v2_test_29-10-2026/predicciones_test.csv.gz

## 22. Activación GSR V2: curvas ROC en test

Las tres curvas quedan pegadas a la diagonal, que es lo mismo que muestran las AUC.

Fuente: resultados/activacion_gsr_v2_recalculo_02-11-2026/predicciones_externas.csv.gz; resultados/activacion_gsr_v2_recalculo_02-11-2026/metricas.csv

## 23. Señales disponibles

Son medidas fisiológicas y de mirada; ninguna es un autorreporte.

Fuente: ../../documentos/01 Tesis MDS/Marco Teorico/Problema e hipótesis.md; ../../documentos/01 Tesis MDS/Analisis de Datos/DOCUMENTACION_DATOS_MDS.md

## 24. Configuración del entrenamiento de activación

La misma configuración se comparte entre los tres contextos para que la única diferencia sea el historial.

Fuente: resultados/activacion_gsr_v2_recalculo_02-11-2026/protocolo.json

## 25. Regla de decisión propuesta para una cohorte nueva

La regla la dejo escrita antes de tener datos, sabiendo que puede terminar en inconcluso. Si rechazo +0,02, igual puede haber una mejora más chica.

Fuente: resultados/protocolo_hipotesis_reintento_06-11-2026/INFORME.md

## 26. De dónde sale cada cifra

Si quiere revisar alguna cifra en detalle, le puedo mostrar el informe correspondiente.

Fuente: FUENTES.md