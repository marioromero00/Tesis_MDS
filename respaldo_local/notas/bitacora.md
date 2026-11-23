# Bitácora de tesis

Registrar fecha, avances, decisiones y próximos pasos en cada sesión.

## 29-10-2026 — Evaluación EEG por canal con temporalidad

Completada selección de 36 candidatos en cinco folds (180 ajustes) y evaluación de seis modelos en ocho personas de validation. Principal congelado: HistBoost, contexto32, AUC 0,694068; offline secundario: CatBoost profundidad4, contexto32, AUC 0,703861. Temporalidad inductiva +0,014318 frente a contexto1, intervalo pareado incluye cero. Validación previamente consultada; test/P29 no evaluados. Auditoría independiente aprobada.

Resultados: ../repos/Tesis_MDS/resultados/temporalidad_eeg_v2_validacion_29-10-2026/INFORME.md. Scripts: evaluar_temporalidad_eeg_v2.py, auditar_temporalidad_eeg_v2.py, graficar_temporalidad_eeg_v2.py. La comparación ya concluyó; no relanzar buscando elevar el resultado en validation. Modelos, profesor, protocolo previo y predicciones quedan guardados.

## 29-10-2026 — Test temporalidad y contraste de hipótesis

Por solicitud explícita se evaluaron ocho personas de test (4.024 ventanas etiquetadas). Se conservaron los seis modelos congelados y se añadieron dos controles estáticos con familia/parámetros emparejados, ajustados solo en train antes de consultar test. Inductivo ctx32 AUC 0,687901 vs estático pareado 0,660179: Δ0,027722, IC descriptivo [-0,004095; 0,050523], mejora en 7/8. Offline ctx32 AUC 0,691865. Todos los intervalos de contrastes temporales incluyen cero. Conclusión: indicios favorables, evidencia inconclusa; no confirmar ni rechazar definitivamente la hipótesis. Esta corrida solo analiza atención, no activación/fusión. Test ya expuesto históricamente. Auditoría independiente aprobada. No reajustar modelos a partir de test.

Informe: ../repos/Tesis_MDS/resultados/temporalidad_eeg_v2_test_29-10-2026/INFORME.md. Scripts: evaluar_test_temporalidad_eeg_v2.py, auditar_test_temporalidad_eeg_v2.py, graficar_test_temporalidad_eeg_v2.py.

## Comparación común binaria completada
20 modelos nuevos: atención y activación, contextos 1/32, ablaciones unimodales y leave-one-modality-out. Resultados en ../repos/Tesis_MDS/resultados/comparacion_comun_binaria_30-10-2026/INFORME.md. Atención temporal mejora; activación temporal empeora; fusión no supera claramente a EEG individual. Parámetros fijos, etiquetas activación binaria nuevas, todas las evaluaciones exploratorias.

## 30-10-2026 — Diagnóstico y búsqueda propia de activación completados

60 ajustes internos, 15 modelos externos, folds congelados y etiquetas binarias idénticas. AUC OOF: actual 0,536599, ctx8 0,534243, ctx32 0,540102. Diferencias temporales inconclusas. Hallazgos críticos: P4 GSR válido12,6 % con todas sus ventanas etiquetadas; P34 positivos8,6 % por empates; contexto32 completo0,95 %. No se evaluaron validation/test. Auditorías aprobadas. Informe en ../repos/Tesis_MDS/resultados/activacion_diagnostico_nested_30-10-2026/INFORME.md y diagnóstico separado. Priorizar protocolo de calidad docente antes de nuevos ajustes.

## 01-11-2026 — Reintento completo de activación
Por solicitud del usuario se reentrenaron 60 ajustes internos y 15 modelos externos en carpeta nueva. Predicciones OOF, métricas, contrastes, selecciones y diagnóstico coinciden con la corrida original con tolerancia1e-10. AUC contextos1/8/32:0,536599/0,534243/0,540102. No se modificaron etiquetas ni se evaluaron validation/test. Evidencia: ../repos/Tesis_MDS/resultados/activacion_diagnostico_nested_reintento_01-11-2026/reproduccion.json.

## 01-11-2026 — Organización de carpetas en el Mac

Vault recuperado movido a `../documentos/01 Tesis MDS`, con enlace de compatibilidad en `../repos/01 Tesis MDS`. Índices y pautas actualizados. Se verificaron los hashes de los 80 archivos y el estado Git sin cambios. Código, datos y experimentos conservan sus ubicaciones. Recuperar la redacción posterior no es una prioridad actual para Mario. Detalle: `organizacion-carpetas-01-11-2026.json`.

## 01-11-2026 — Primer contraste fijo de activación V2 y respaldo Git

15 regresiones logísticas C=1, cinco folds y contextos 1/8/32; 7.028 filas de train con etiquetas V2 idénticas entre modelos. AUC macro persona 0,526132 / 0,518344 / 0,513917. Diferencias frente a ventana actual −0,007788 y −0,012215, con intervalos descriptivos que incluyen cero. No hay mejora temporal clara en esta comparación. No se evaluaron validation/test. Auditoría de recarga y verificación de 75 AUC desde disco aprobadas; cuatro pruebas de calidad de etiquetas aprobadas.

Informe: ../repos/Tesis_MDS/resultados/activacion_v2_historial_01-11-2026/INFORME.md. Script: experimento_activacion_v2.py. La representación temporal agrega media y desviación: no evalúa modelos sensibles al orden. No comparar directamente esta AUC con etiquetas anteriores.

Mario pidió guardar y subir cada etapa a Git. Se incorporaron los avances pendientes y copia verificable de documentos/notas al commit 6c02bb3. El envío a GitHub falló por resolución DNS (`Could not resolve host: github.com`); el respaldo remoto queda pendiente. Datos crudos externos, entornos, cachés y logs externos no están incluidos en esta copia Git.

## 01-11-2026 — Aprobación de etiquetas V2 y protocolo final

Mario comunica que su profesor aprobó usar las etiquetas V2 y solicita completar la comparación no lineal con/sin historial. Se fijó HistGradientBoosting, contextos 1/8/32 y dos candidatos de máximo de hojas (7/15), con los cinco folds heredados. Configuración compartida elegida por promedio de AUC internas entre contextos; ajuste final elegido solo desde las puntuaciones internas de train. Contraste principal 32−1 y secundario 8−1. Modelos se congelan antes de consultar validation/test; una corrida acotada sin ampliación posterior por rendimiento.

Protocolo: ../repos/Tesis_MDS/resultados/activacion_v2_comparacion_final_01-11-2026/protocolo.json. La aprobación de uso no implica validación psicológica externa ni elimina la exposición histórica de las particiones. El estudio de ablación de modalidades queda fuera de esta solicitud (punto 2).

## 01-11-2026 — Comparación final no lineal V2 completada

30 ajustes internos HistGradientBoosting; 15 modelos OOF y tres finales. La selección interna fijó 15 hojas compartidas entre contextos. Modelos finales guardados y comprometidos en Git antes de evaluar validation/test. Test AUC contextos 1/8/32: 0,514087 / 0,546964 / 0,536320. Contraste principal 32−1: +0,022233, IC [−0,013004; +0,058518], inconcluso. Secundario 8−1: +0,032878, IC [+0,007625; +0,059155], 7/8 mejoran; validation y OOF no confirman esa mejora. No seleccionar contexto usando test. No hay evidencia consistente de superioridad temporal general; intervalos de AUC absoluta incluyen 0,50.

Se evaluaron 7.028 ventanas train, 2.584 validation y 2.184 test, con idénticas etiquetas/filas por contexto. Auditoría desde disco: 30 scores internos, 123 AUC por persona y 21 recargas predictivas aprobadas. Informe: ../repos/Tesis_MDS/resultados/activacion_v2_comparacion_final_01-11-2026/INFORME.md. Regla de parada cumplida, sin nueva búsqueda. Subida a GitHub continúa pendiente por fallo DNS; commits locales conservados.

Limitación de cobertura de la corrida final: ninguna ventana validation/test dispone de 32 ventanas consecutivas retenidas; ctx32 en test tiene longitud media por persona de 8,75. Contexto es máximo disponible, no longitud completa garantizada. Registrado en el informe.

## 01-11-2026 — Ablación V2 y cierre de temporalidad solicitados

Mario solicitó ejecutar la comparación EEG/mirada/pupila frente a fusión y cerrar interpretación temporal. Protocolo de ablación guardado antes del entrenamiento: contextos 1/8/32, mismas filas V2, hiperparámetros controlados heredados de selección interna previa, sin nueva búsqueda. Se reutilizan modelos completos con hashes y se entrenan 45 variantes OOF más nueve finales unimodales. Cierre temporal en ../repos/Tesis_MDS/documentacion/Cierre_Temporalidad_V2_01-11-2026.md. No se afirma superioridad temporal general; se explicita la insuficiencia de historial completo y la diferencia entre contraste principal y secundario.

## 01-11-2026 — Ablación de modalidades y cierre completados

54 modelos nuevos (45 OOF y nueve finales), con hiperparámetros heredados de selección interna del modelo completo. Mismas etiquetas V2, participantes y filas. Auditoría aprobada: 63 recargas, 492 AUC y 27 contrastes. Test: EEG 0,4982/0,5123/0,5173; mirada 0,5151/0,5129/0,5215; pupila 0,5172/0,5461/0,5386; fusión 0,5141/0,5470/0,5363 (contextos1/8/32). Los nueve intervalos pareados de fusión en test incluyen cero; no hay ventaja clara sobre las modalidades individuales. Solo validation contexto32 frente a mirada tiene intervalo de diferencia positivo, sin reproducirse en test. No elegir un ganador ni ajustar de nuevo usando test.

Cierre conjunto: ../repos/Tesis_MDS/documentacion/Cierre_Experimental_V2_01-11-2026.md. Cierre temporal: Cierre_Temporalidad_V2_01-11-2026.md en la misma carpeta. No se obtiene apoyo conjunto suficiente a superioridad temporal multimodal; resultados exploratorios, sin validar constructos psicológicos. Subida GitHub pendiente por DNS; commits locales conservados.


## 2026-11-02 — Reintento y auditoría GSR V2


## Auditoría independiente del 2 de noviembre de 2026

Se confirmó un error de alineación en el generador histórico `scripts/preparar_modelado.py`: `groupby(..., group_keys=False).apply(...).reset_index(level=0, drop=True)` sustituye los índices originales por posiciones en el orden de los grupos. En estas entradas, 25.498 de 25.992 posiciones de componentes quedan desplazadas. Este denominador corresponde al archivo completo, incluyendo personas fuera de las particiones principales; no equivale al número de etiquetas binarias que cambian.

El generador histórico reprodujo los scores archivados de activación con errores máximos absolutos de 4,82e-7 (2 s) y 2,92e-7 (6 s), compatibles con la precisión de exportación. Por tanto, el problema afecta efectivamente a esos resultados guardados. Los AUC anteriores de activación basados en esas etiquetas no permiten respaldar ni rechazar la hipótesis; deben recalcularse con el profesor corregido. El patrón también aparece en el profesor histórico de atención, pero esta auditoría no certifica ni invalida las reconstrucciones posteriores de atención.

La V2 conserva la identidad de las ventanas mediante asignación por índice. Se reprodujeron sus scores y etiquetas guardadas a tolerancia 1e-12, se verificó la normalización con un cálculo independiente y se comprobó el soporte temporal de cada etiqueta. Se preservaron hashes de la fuente y partición. Evidencia: `auditoria_independiente_02-11-2026.json`; ejecución reproducible: `.venv/bin/python scripts/auditar_etiquetas_gsr_v2.py`. El generador histórico se conserva como evidencia y no debe utilizarse para nuevas etiquetas de activación; usar `reconstruir_etiquetas_gsr_calidad_v2.py`.

Quedan 11.796 etiquetas de 22.211 ventanas (53,1%). Las otras 10.415 corresponden a 9.995 con historial insuficiente, 401 con cobertura/flag inválido y 19 empates. La mayor pérdida proviene de exigir cinco ventanas consecutivas dentro del mismo estímulo/segmento, no de mala calidad GSR. P4 conserva 26 de 459 ventanas. Las 41 personas conservan ambas clases. Las clases aproximadamente equilibradas son consecuencia del umbral por mediana y no demuestran validez psicológica.

Siguiente evaluación: entrenar desde cero los modelos estático y temporal sobre las mismas filas V2 y particiones, sin cruzar huecos, y comparar AUC y diferencias con incertidumbre por participante. No se calcularon nuevos AUC en esta reconstrucción; el test previamente consultado continúa siendo exploratorio.


## 2026-11-02 — Recálculo solicitado de AUC con GSR V2
Resultados: resultados/activacion_gsr_v2_recalculo_02-11-2026


## Interpretación de la hipótesis y cierre de auditoría (02-11-2026)

Reentrenamiento completo: 30 ajustes internos, 15 modelos OOF y tres finales, con las mismas etiquetas GSR V2, filas y particiones. La auditoría independiente recalculó 123 AUC por participante, verificó 30 scores internos y realizó 21 comprobaciones de predicciones desde modelos guardados. Búsqueda, predicciones y métricas reproducen exactamente la ejecución V2 previa; ver `reproducibilidad.json` y `auditoria_desde_disco.json`.

La comparación principal (hasta 32 ventanas frente a actual) obtiene ΔAUC test +0,02223, IC descriptivo 95% [-0,01300; +0,05852]. No permite afirmar superioridad temporal ni demostrar ausencia de efecto. La secundaria (hasta 8 ventanas) obtiene +0,03288 [+0,00763; +0,05916], con mejora en 7/8 personas, pero no se confirma en validación: +0,00269 [-0,02600; +0,03325], ni en OOF train. Es una señal exploratoria, no validación robusta de la hipótesis general. Los AUC absolutos siguen próximos a 0,5 y sus intervalos incluyen 0,5. Los intervalos de diferencias son pareados por participante; no se infieren de la superposición de los intervalos individuales.

Las etiquetas son pseudoetiquetas GSR relativas a la sesión y normalizadas offline; este resultado no valida una medida psicológica externa. La reutilización histórica de test impide presentarlo como confirmación independiente. No se alteró el protocolo según estos resultados.

### Historial efectivo en test

- Contexto 1: historial medio 1.00 ventanas; 100.0% con contexto completo.
- Contexto 8: historial medio 5.06 ventanas; 40.8% con contexto completo.
- Contexto 32: historial medio 8.73 ventanas; 0.0% con contexto completo.

Ninguna fila de test dispone de 32 ventanas completas: la comparación principal prueba agregación sobre el historial disponible, no secuencias completas de 32. El historial usa solo filas etiquetadas consecutivas, por lo que omite ventanas iniciales válidas sin etiqueta. Mantener esta limitación explícita en la tesis. Las medias y desviaciones temporales tampoco prueban una arquitectura sensible al orden.


## 2026-11-06 — Protocolo de hipótesis reproducido
/Users/mario/Proyectos/tesis-mds/repos/Tesis_MDS/resultados/protocolo_hipotesis_reintento_06-11-2026


## Cierre del reintento — 6 de noviembre de 2026

Los cálculos se reprodujeron y se contrastaron mediante 100.000 simulaciones por escenario de varianza bajo el supuesto normal del diseño. Los cuatro modelos seleccionados conservan sus hashes. No se adquirieron participantes ni se ejecutó una evaluación confirmatoria nueva.

El N de activación es muy sensible a la fuente de dispersión: 72 con la varianza de validación, 101 con la de test y 767 con la de OOF train. No son límites de un intervalo ni opciones para escoger por conveniencia. OOF mezcla modelos entrenados en distintos folds, mientras que la cohorte futura evalúa un par fijo; por tanto, 767 debe tratarse como escenario conservador de sensibilidad, no como requerimiento de reclutamiento demostrado. Las estimaciones externas se basan en solo ocho personas cada una. El diseño final necesita una estimación de variabilidad más defendible y factibilidad de adquisición antes de fijar N.

La referencia al AUC 0,67 corresponde provisionalmente al CatBoost de atención con 0,6744 en test. Su buen desempeño relativo al azar y la superioridad de un modelo temporal son afirmaciones distintas. El resultado de atención no desapareció al corregir GSR: el recálculo de activación trabaja sobre otra variable objetivo y otras entradas. Esta revisión verifica la procedencia de las métricas, no constituye una nueva auditoría completa del profesor de atención.

El margen práctico 0,02 sigue siendo una propuesta, no un umbral aprobado ni deducido de los resultados. Rechazar una mejora de al menos ese tamaño no equivale a rechazar cualquier mejora positiva. Si se mantiene la hipótesis original de superioridad >0, la frontera debe ser 0 y la potencia se calcula para un efecto verdadero separado de 0, sin cambiarla después de observar el test.


## 2026-11-16 — Cierre experimental V3

Resultados: repos/Tesis_MDS/resultados/cierre_v3_16-11-2026 (INFORME.md). Protocolo registrado y publicado antes de entrenar (v2, commit 82affdb; v1 abortada en el fold 1 de train por auditoría de código). Etiqueta de atención verificada sin el error de índices: todas las corridas actuales leen caracteristicas_multimodales.csv, y las etiquetas coinciden 100 % con las del 30-10.

Mejoras: historial armado con todas las ventanas válidas, GRU sensible al orden contra GRU de una ventana, fusión tardía contra temprana, BA/macro-F1/recall con umbral 0,5 y control de 5 ventanas.

Atención: el resumen del historial (HGB hasta 32 − sin historial) es positivo en train (+0,018 [+0,009; +0,027]), validación (+0,020 [−0,003; +0,042]) y test (+0,029 [+0,004; +0,052]); no alcanza el criterio del manuscrito por validación. La ganancia aparece casi entera con 5 ventanas. La GRU no mejora sobre su control y queda 0,04–0,05 bajo el HGB en las tres particiones. Fusión tardía ≤ temprana.

Activación: AUC de train 0,50–0,53. Las mejoras de la GRU en validación (+0,091) y test (+0,084) no aparecen en train (−0,016); no se toman como señal.

Hipótesis: sin ventaja consistente en ninguno de los dos resultados. Auditoría independiente de resultados: PASA en los seis puntos. Experimentación cerrada; lo pendiente es escritura y las decisiones con el profesor guía.


## 2026-11-16 — Análisis final con 41 personas

Resultados: repos/Tesis_MDS/resultados/cierre_final_41p_16-11-2026 (INFORME.md). Registrado antes de correr (commit 1bbb083); CV agrupada por persona en las 41, configuración congelada de V3, sin búsqueda; Holm, permutación de signos y equivalencia ±0,02.

Atención: HGB hasta 32 − sin historial +0,026 [+0,018; +0,035], 36/41, p Holm 0,00001 → respaldo (no "relevante": límite inferior < 0,02). Se repite en las 25 de train (+0,023) y en las 16 de validación+test (+0,032). La GRU no agrega sobre el resumen (+0,008, IC 90 % dentro de ±0,02) y queda 0,040 por debajo del HGB.

Activación: +0,034 [−0,001; +0,069], p Holm 0,066 → inconcluso. Secundario: GRU 32 − GRU 1 +0,051 [+0,021; +0,080], sin corrección.

Hipótesis: evidencia mixta, apoyo parcial (criterio del manuscrito). Experimentación cerrada.


## 2026-11-16 — Pruebas de robustez (placebo temporal)

Resultados: repos/Tesis_MDS/resultados/cierre_robustez_41p_16-11-2026 (registrado antes, commit 6447236).

Atención: la mejora (+0,026) se mantiene sin fuga de etiquetas (+0,024) y en tres particiones (+0,026 a +0,030), pero un historial placebo de la misma persona la reproduce entera: real − placebo −0,000 [−0,003; +0,003]. Nulo concluyente para la información temporal; la ganancia es contexto de la persona.

Activación: real − placebo +0,038 [+0,006; +0,068], p Holm 0,043; placebo − sin historial −0,004. Contraste principal positivo en las tres particiones alternativas (+0,042). Información temporal real, ligada al soporte de 6 s de la etiqueta.

Conclusión: evidencia mixta; el apoyo temporal viene de activación, no de atención. Esto corrige la lectura del análisis de 41 personas.


## 2026-11-18 — Ampliación E1–E6 y explicativo de posición

Resultados: resultados/ampliacion_41p_16-11-2026 (con enmienda_e1_lag6) y resultados/explicativo_posicion_41p_18-11-2026.

Activación: el historial que excluye por completo los 6 s de la etiqueta supera al placebo: +0,046 [+0,018; +0,073], 28/41, p Holm 0,004. La posición dentro del estímulo no aporta (−0,004) y el historial agrega +0,038 sobre ella. Información temporal real en las señales, con AUC absolutas bajas (0,56–0,57).

Atención: el historial no tiene información temporal (E1 real − placebo −0,003). Toda su mejora (+0,026) se reproduce con una sola variable, los segundos transcurridos en el estímulo (+0,028); controlando posición, el historial agrega −0,002 [−0,006; +0,002]. La calibración personal no explica nada (+0,001 a +0,004); corrige la lectura del 16-11.

Fusión (MLP): en atención la tardía supera a la temprana (+0,012) y a la intermedia; en activación sin diferencias. Fatiga: AUC de atención sube a lo largo de la sesión; prevalencia de activación cae al final (habituación compatible). Importancia: atención depende del EEG actual (theta, delta); activación del EEG y la media del historial. Por página: atención mejor en sitios web y peor en textos.

Nota: el comando de espera de la enmienda quedó en espera indefinida (se emparejaba consigo mismo); se detectó el 18-11 y se corrió la enmienda ese día.


## 2026-11-22 — Cierre formal de la experimentación

Mario decidió cerrar la fase experimental. Documento de cierre: repos/Tesis_MDS/documentacion/Cierre_Experimental_Final_22-11-2026.md (síntesis de los informes del 16 al 18-11, sin resultados nuevos ni entrenamientos). Verificado antes de cerrar: las cinco carpetas de resultados finales están completas en Git, no había procesos activos y HEAD coincidía con origin/main. Etiquetas, particiones y configuración quedan congeladas; reabrir requiere decisión explícita y protocolo registrado antes de correr. Sin aprobación registrada del profesor guía. Pendiente: escritura, margen práctico 0,02 y revisión de la presentación v6.


## 2026-11-22 — Reapertura: conclusiones más firmes

Mario reabrió la experimentación el mismo día del cierre. Resultados: repos/Tesis_MDS/resultados/reapertura_41p_22-11-2026 (INFORME.md) y reapertura_fase2_41p_22-11-2026. Fase 1 registrada antes de correr (commit 5076307); fase 2, controles post hoc pedidos por la auditoría de código, registrada con la fase 1 aún corriendo (commit e3d9c71). Sin cambios de etiquetas ni de configuración.

Activación: el contraste principal con 5 particiones pasa a respaldo, +0,036 [+0,010; +0,065], p Holm 0,021. Con el tiempo de sesión como variable queda inconcluso (+0,026 [−0,006; +0,056]). Curva temporal: solo el desfase de 6 s supera al placebo (+0,047, p Holm 0,017; +0,053 contra placebo de bloque); a 12 s inconcluso y desde 24 s nada; el contraste cae 0,010 por duplicación del desfase (p 0,009). Dentro del mismo minuto de sesión la ganancia se mantiene (+0,058 [+0,027; +0,092]); dentro de la misma posición queda inconclusa (+0,027). Etiqueta de 6 s antes predice la actual con AUC 0,68.

Atención: P1 +0,029 [+0,021; +0,037]. El pasado a 6–96 s no aporta: nulo concluyente a 6 y 12 s, igual o peor que el placebo después. Posición sola AUC 0,598; detección sin historial entre ventanas de la misma posición 0,677 (0,684 sin estratificar). Comprobación no registrada: también con AUC estratificada la posición como variable reproduce la ganancia del historial.

Advertencia de la comprobación no registrada (una partición): en activación, dentro de un mismo estímulo, la posición sola mejora (+0,040) y el historial no la supera.

Lectura: apoyo parcial, mejor delimitado. Activación: efecto del historial confirmado, de corto alcance (6–12 s), no deriva lenta. Atención: sin información temporal. Pendiente: decidir con el profesor guía cómo presentar los controles inconclusos de activación.

Nota de cómputo: el ajuste de HGB con pesos está dominado por el cálculo de los cortes (unos 40 ms por variable, en Python y sin paralelizar); 12 procesos en paralelo tardaron 55 min.


## 2026-11-22 — Reapertura, fase 3: historial frente a posición

Resultados: repos/Tesis_MDS/resultados/reapertura_fase3_41p_22-11-2026 (INFORME.md). Registrado antes de correr (commit 7046d92), pedido por Mario tras ver las fases 1 y 2 (análisis dirigido). Contraste: (historial + posición) − (ventana actual + posición), 5 particiones, Holm sobre 4.

Atención: +0,001 [−0,002; +0,005] en general y −0,000 [−0,003; +0,003] dentro del mismo estímulo: nulo concluyente en ambos. Ventana actual + posición rinde 0,711; historial completo 0,712.

Activación: +0,032 [+0,004; +0,059], 28/41, p 0,027, p Holm 0,108: inconcluso por la regla registrada (mediana +0,031; sin la persona más influyente, que empuja en contra, +0,039 [+0,015; +0,063]). Dentro del mismo estímulo +0,009 [−0,020; +0,037], inconcluso; ahí la posición sola aporta +0,049 [+0,027; +0,072] y el historial no la supera.

Lectura: en atención la mejora del historial es la posición (cerrado). En activación hay dos componentes: dentro del estímulo manda el tiempo transcurrido; entre estímulos el historial aporta y la posición no, pero sin alcanzar el criterio tras Holm. No hay evidencia de dinámica dentro del estímulo.


## 2026-11-22 — Cuatro enfoques nuevos

Pedidos por Mario. Resultados: repos/Tesis_MDS/resultados/enfoques_41p_22-11-2026 (INFORME.md). Protocolo v1 en el commit cd25134 y v2 en 4a4798c, ambos antes de ejecutar; la v2 incorpora dos auditorías de código hechas sin resultados. Cinco repeticiones de la CV por persona, Holm por familia.

E1 etiqueta de atención corregida por posición (mediana de la persona dentro del tramo de posición; concuerda 90,6 % con la original): posición sola 0,504; detección sin historial 0,675 frente a 0,683 (−0,008 [−0,015; −0,001]); historial − sin historial +0,010 [+0,006; +0,015]; con posición como variable +0,004, nulo concluyente.

E2 detección cruzada (atención, sin historial): solo EEG 0,681 (41/41), solo GSR 0,545, GSR no agrega al EEG (nulo concluyente). Firma ocular: lento y amplitud 0,673; alfa y beta 0,593; frontales 0,675 y posteriores 0,602 (montaje por defecto OpenBCI, NO verificado). Control barajado 0,496. La probabilidad del modelo se correlaciona sobre todo con el recorrido de la mirada (0,41). El EEG no tiene limpieza de artefactos oculares.

E3 activación por estímulo (1.589 segmentos): AUC 0,587 [0,550; 0,622]; frente al promedio del modelo por ventana con historial +0,020 inconcluso; frente a solo duración +0,048 inconcluso.

E4: fiabilidad por mitades de la AUC 0,76 (atención) y 0,66 (activación); de la ganancia del historial 0,30 y 0,25 (no fiable). Sin correlatos tras Holm. Adaptación a la persona (primer 40 % de la sesión): activación +0,028 sin historial y +0,045 [+0,023; +0,069] con historial; atención nulo concluyente. Es adaptación offline.

Pendiente nuevo: verificar el montaje de electrodos y evaluar limpieza de artefactos oculares; decidir si la etiqueta corregida reemplaza a la original. Resumen del mes en notas/resumen-ultimo-mes-22-11-2026.md.

## 23-11-2026 — Montaje EEG y limpieza de artefactos oculares

Mario pide continuar. Se aborda el pendiente 2 de los cuatro enfoques.

- **Montaje** (`resultados/montaje_ocular_41p_23-11-2026/`, descriptivo, sin etiquetas): la respuesta a parpadeos por canal (Fp1/Fp2 ≈150 µV, F7/F8 ≈75, F3/F4 ≈57, posteriores ≈19) y el signo opuesto de la mirada horizontal en F7 y F8 (31 de 37 personas) son compatibles con el montaje por defecto de OpenBCI. El EEG va 0,18–0,53 s atrasado respecto del seguidor ocular (mediana 0,45 s); no se corrigió.
- **Limpieza ocular** (`resultados/limpieza_ocular_41p_23-11-2026/`, registrado antes de correr en `06547f5`, enmienda `441bae9`, auditorías de código y de resultados sin hallazgos bloqueantes): quitar 3 componentes oculares por ICA (3,5 % de la varianza) baja la AUC de atención por EEG de 0,681 a 0,621 (+0,060 [+0,045; +0,075], 39/41); quitar 3 componentes no oculares (72 % de la varianza) la deja en 0,674. Alfa y beta baja de 0,593 a 0,547; posteriores de 0,602 a 0,562.
- Lectura: al menos 0,06 de AUC viene de componentes oculares (cota inferior); la parte defendible como no ocular baja a 0,55–0,56; no se puede afirmar detección cerebral de atención.
- Crudos por persona en caché local `datos/locales/v2_2025/cache_ocular/`; variables recalculadas en `datos/locales/v2_2025/limpieza_ocular_variables/` (fuera de Git, con hashes).

## 23-11-2026 — Red convolucional sobre el EEG crudo

Mario pide probar modelos más complejos. Los modelos complejos sobre variables calculadas ya se habían probado sin superar al HGB; se prueba una red tipo EEGNet (1.217 parámetros) sobre la señal cruda.

- `resultados/red_cruda_41p_23-11-2026/`, registrado antes de correr en `0074c60`, enmienda `7e1f1e0` antes de ver resultados de las redes, auditorías de código y de resultados sin hallazgos bloqueantes.
- Atención: red 0,716 frente a HGB 0,681 (R1 +0,035 [+0,023; +0,047], efecto relevante con holgura mínima). Con EEG limpio: red 0,649 frente a HGB 0,621 (R2 +0,028, respaldo). Red original − red limpia: +0,067 [+0,053; +0,082] (R3, efecto relevante, sin control propio).
- Activación: red 0,498, HGB solo EEG 0,524; R4 −0,025 [−0,055; +0,003], inconcluso.
- Lectura: la red aprovecha mejor la huella ocular en el EEG; no cambia la conclusión de la limpieza ni el resultado de activación. Vale para una sola arquitectura sin búsqueda.
- Tensores en `datos/locales/v2_2025/red_cruda_tensores/` (fuera de Git, con hashes).

## 23-11-2026 — Sustento fisiológico y borrador de discusión

A pedido de Mario: `notas/sustento-fisiologico-23-11-2026.md` (18 referencias verificadas en OpenAlex, textos completos no leídos) y `documentos/01 Tesis MDS/Escritura/Borrador Discusión fisiológica 23-11-2026.md` (borrador para el Capítulo 8; no reemplaza el del 18-11 ni cierra decisiones abiertas).

## 23-11-2026 — Presentación versión 7 (estilo tipo Beamer)

A pedido de Mario. `repos/Tesis_MDS/presentaciones/avances_tesis_06-11-2026/`: la versión 6 quedó archivada en `version_6/`. Cambios: capítulo nuevo «Qué detecta el EEG» (5 diapositivas: huella ocular, limpieza, red sobre la señal cruda y explicación fisiológica de atención y activación), fila nueva en «Qué responde la tesis», diapositiva «Qué falta para cerrar la experimentación» y anexo F con referencias. 37 diapositivas. Tema visual nuevo en `tema_beamer.py` (barra lateral y franja superior azules, portada con título en recuadro); los gráficos se regeneraron con el mismo azul. Sin resultados nuevos. Corrección: la AUC de la red en activación es 0,498 (0,4985), no 0,499; corregida en informe, READMEs y notas.

## 23-11-2026 — Cierre consolidado y comprobación de reproducibilidad

A pedido de Mario. `repos/Tesis_MDS/documentacion/Cierre_Experimental_Final_23-11-2026.md` reemplaza como referencia al cierre del 22-11: reúne las 12 etapas del 16 al 23-11 con sus decisiones y commits. `scripts/verificar_cierre.py` (salida en `resultados/verificacion_cierre_23-11-2026/`): 288 de 289 archivos con hash coinciden con lo registrado; la diferencia es el script de limpieza ocular, por la enmienda v2 documentada (`441bae9`). Protocolo anterior al informe en las 10 etapas con informe propio; carpetas sin cambios pendientes; HEAD igual a origin/main. No se reentrenó nada. Etiqueta `cierre-experimental-2026-11-23`.

## 23-11-2026 — Borrador de Conclusiones

A pedido de Mario se redactó `documentos/01 Tesis MDS/Escritura/Borrador Conclusiones 23-11-2026.md` (Capítulo 9, secciones 9.1 a 9.7) a partir del cierre consolidado y los informes. No cierra las cinco decisiones abiertas con el profesor: las supone de forma provisoria y lo declara al inicio. `Estructura Tesis` conserva el capítulo como pendiente. Sin experimentos nuevos.

## 23-11-2026 — Conclusiones en la presentación

A pedido de Mario se agregaron dos láminas de conclusiones (30 y 31) a `presentaciones/avances_tesis_06-11-2026`, tomadas del borrador de Conclusiones. La presentación queda en 39 láminas (33 principales y 6 anexos), versión 7. Verificadas con captura.

## 23-11-2026 — Lámina 29 al día

A pedido de Mario, la lámina "Qué responde la tesis" pasó a las cifras de la reapertura del 22-11 (+0,029 y +0,036; +0,001 con posición; +0,047 sobre el placebo), para coincidir con las conclusiones. El pie indica las cifras del 16-11.
