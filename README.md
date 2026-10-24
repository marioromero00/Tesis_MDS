# Tesis MDS — Baselines multimodales

Estado experimental actualizado al 24-10-2026. Esta entrada reemplaza la descripción anterior del repositorio.

Detección temporal multimodal de atención y activación durante navegación web, con EEG,
GSR, eye tracking y pupilometría. Los baselines estáticos están entrenados y guardados;
se completó el primer contraste con TCN, LSTM y BiLSTM sobre el mismo split y etiquetas.

## Entrega actual

- [Presentación simplificada y avance del manuscrito, 24-10-2026](documentacion/Presentacion_y_Manuscrito_24-10-2026.md):
  seis diapositivas en [PowerPoint editable](presentaciones/Avances-Experimentales-Simplificados-24-10-2026.pptx)
  y [PDF](presentaciones/Avances-Experimentales-Simplificados-24-10-2026.pdf).
  Se amplió la metodología del borrador en `../01 Tesis MDS/Escritura/Estructura Tesis.md`
  y se redactaron experimentos, resultados y discusión, con límites de validez explícitos.

- [Control negativo temporal y errores, 24-10-2026](documentacion/Control_Negativo_Temporal_y_Errores_24-10-2026.md):
  con los cinco folds originales se reprodujo BA 0,3843 y se entrenaron 12 controles
  que desplazan etiquetas GSR por persona; BA promedio 0,3268 (rango 0,3097–0,3488).
  Diferencia descriptiva +5,76 pp, con 19/25 personas sobre su control promedio.
  El análisis de errores muestra recall medio de 21,8 % en test y variación entre
  personas y estímulos. Incluye predicciones, hashes, tablas y figura PNG/PDF.
  Es un control interno retrospectivo, no validez psicológica ni confirmación nueva.

- [Robustez sin cohorte nueva, 24-10-2026](documentacion/Robustez_Sin_Cohorte_Nueva_24-10-2026.md):
  se reutilizaron predicciones fijas de 25 personas de train y ocho de test para
  medir variación individual y sensibilidad a pseudoetiquetas GSR 6 s, GSR 2 s
  y PCA GSR. BA en test: 0,3557 con GSR 6 s, cercana a la referencia aritmética
  0,3542 (`1/k` por persona). Cambió 19,7 % de etiquetas de test al usar 2 s
  y 30,5 % al usar PCA; las diferencias de BA tuvieron intervalos descriptivos
  que incluyen cero. Incluye tablas y figura PNG/PDF. Test ya había sido consultado.

- [Evaluación adicional y auditoría de pseudoetiquetas, 24-10-2026](documentacion/Evaluacion_Independiente_y_Validez_24-10-2026.md):
  el ensamble fijado de cinco Ridge sin `fixation_count` obtuvo BA macro por persona
  0,3557 en las ocho personas de test existentes (4.025 ventanas; intervalo descriptivo
  [0,2988; 0,4109]). El test ya había sido consultado antes: no es confirmación
  independiente nueva. La auditoría interna de etiquetas encontró 48,9 % de acuerdo
  entre las reglas igualitaria y PCA de atención, y 67,0 % entre GSR 6 s y PCA de
  activación. Falta una medida externa para validar ambos constructos.

- [Tres intentos adicionales de mejora, 24-10-2026](documentacion/Mejoras_Adicionales_24-10-2026.md):
  ajuste de decisión del TCN, mezcla fija con Ridge y ablación conjunta de
  variables de fijación. Ninguno superó al Ridge sin `fixation_count` (BA macro
  0,3843); se registraron resultados por clase, intervalos descriptivos,
  protocolos y artefactos. 71 pruebas aprobadas; validation/test no usados en esos intentos.

- [Contraste de temporalidad y fusión, 24-10-2026](documentacion/Contraste_Temporalidad_Fusion_24-10-2026.md):
  diseño 2 × 2 ejecutado en activación y atención con 25 participantes de train,
  cinco folds y dos semillas. 140 modelos y 216.384 predicciones auditadas.
  Activación: historial +0,88 pp de BA en fusión temprana, IC descriptivo
  [-0,28; +2,00]; fusión tardía con historial +0,18 pp, IC [-0,80; +1,37],
  pero recall medio cae de 23,4 % a 8,2 %. Atención: historial -0,65 pp y
  fusión tardía con historial +1,01 pp, ambas diferencias exploratorias.
  No se reevaluaron validation ni test.

- [Ablación de modalidades, variables e historial y PCA](documentacion/Ablacion_PCA_12-09-2026.md):
  38 variantes, 190 modelos, 513.912 predicciones verificadas y 59 pruebas.
  Quitar EEG baja BA macro de 0,3748 a 0,3546. Solo EEG conserva 0,3722, con pérdida
  de recall medio. Quitar fixation_count da 0,3843, máximo secundario exploratorio.
  PCA al 90 % conserva 13–45 componentes y obtiene 0,3764, con mejora incierta.
  Incluye ranking de variables, cargas PCA, intervalos y cuatro figuras PNG/PDF.

- [Búsqueda de BA macro sobre 0,50](documentacion/Busqueda_Meta_05_12-09-2026.md):
  cuatro enfoques nuevos: persistencia, historial multiescala, adaptación offline y
  regresión ordinal. Mejor BA macro observada: **0,3748**, Ridge multiescala, frente
  a 0,3716 anterior. **Meta 0,50 no alcanzada**; ganancia secundaria e incierta y
  menor recall medio. Incluye resultados completos, fallos numéricos y correcciones,
  configuraciones, modelos, predicciones y figuras. Validation/test sin reevaluar.

- [Auditoría y ensambles](documentacion/Ensambles_11-09-2026.md) y
  [mezclas fijas de stacking e historial](documentacion/Mezclas_Ensambles_11-09-2026.md):
  140 archivos de modelos y 378.672 predicciones verificadas; 47 pruebas aprobadas.
  Mejor BA macro observada 0,3716 con 25 % de stacking, frente a 0,3651 anterior
  (+0,65 pp; IC descriptivo [-0,31; +1,71]). Es un contraste secundario exploratorio;
  la mezcla principal de 10 % obtiene 0,3687. La auditoría detectó selección inestable
  y pérdida de recall medio en stacking solo. La mezcla recupera parte de ese recall,
  con incertidumbre que impide confirmar superioridad. Validation/test sin reevaluar.

- [SVM, QDA e hiperparámetros de boosting y fusiones](documentacion/Hiperparametros_11-09-2026.md):
  44 configuraciones de modelos y 88 decisiones; 660 ajustes internos, 1.320 puntuaciones
  y 70 bundles externos guardados. Fusión logística: BA macro 0,3605; fusión LDA: 0,3593;
  búsqueda conjunta: 0,3548. Ninguna supera el 0,3651 anterior. Incluye hiperparámetros
  elegidos, diagnóstico por clase y el intento serial conservado. 45 pruebas aprobadas.
  Se verificaron 189.336 predicciones, 138 preprocesadores y las 35 selecciones.

- [Boosting, ordinalidad y balanceo por participante](documentacion/Avanzados_11-09-2026.md):
  432 configuraciones de decisión, 360 ajustes internos y comparación con balanceo global.
  La búsqueda conjunta obtiene BA macro 0,3522 y la ordinal 0,3582: no superan el 0,3651
  de la fusión geométrica anterior. Se conservan modelos, predicciones internas y externas,
  registro de cada intento y diagnóstico por clase. Sin nueva evaluación de validation/test.
  60 bundles recargados, 162.288 predicciones verificadas y 42 pruebas aprobadas.

- [Nuevos modelos y fusiones para atención y activación](documentacion/Fusiones_10-09-2026.md):
  LDA, Extra Trees y logística; fusión temprana y tardía. 120 bundles guardados, 324.576
  predicciones verificadas y 38 pruebas. Activación llega a BA macro 0,3651 y atención
  a 0,3444 con fusión tardía; las diferencias frente a temprana siguen siendo inciertas.
  Incluye bitácora, 1.530 puntuaciones internas y conservación del intento interrumpido.

- [Tres iteraciones para mejorar activación](documentacion/Optimizacion_Historial_08-09-2026.md):
  búsqueda temporal/no lineal, combinación y mirada/EEG. 795 ajustes internos, 90 archivos
  de modelos y 243.432 predicciones verificadas. Mejor BA macro observada 0,3546 frente a
  logística 0,3536: mejora mínima e incierta. 33 pruebas; sin nueva evaluación de validation/test.

- [Control del historial pupilar con las mismas cinco variables](documentacion/Control_Historial_Pupilar_08-09-2026.md):
  cinco folds por participante dentro de train, selección interna de época y 170 modelos
  guardados. LSTM/BiLSTM mejoran puntualmente frente a controles de ventana actual,
  con intervalos que incluyen cero y sin superar a logística en promedio. 459.816
  predicciones verificadas y 29 pruebas aprobadas; sin nueva evaluación de validation/test.

- [TCN, LSTM y BiLSTM: resultados y variables frente al baseline](documentacion/Modelos_Temporales_07-09-2026.md):
  104 redes guardadas, dos semillas, evaluación en test y explicaciones por variable e historial.
  Mejoras puntuales de clasificación de activación; todavía sin ventaja general del historial.

- [Estabilidad y panel de entradas congelado](documentacion/Estabilidad_Variables_07-09-2026.md):
  cinco folds por participante, 180 ajustes internos y 36 pipelines finales. La reducción
  queda como contraste experimental; se conservan los completos como referencia.

- [Análisis de importancia y reducción de variables](documentacion/Analisis_Variables_07-09-2026.md):
  56 comparaciones en validación, 48 pipelines reducidos y figuras exportables.

- [Presentación HTML, 16 diapositivas](presentaciones/avance-eda-sincronizacion-15-08-2026.html).
- [30 modelos entrenados](resultados/modelado/ejecuciones/baselines_05-09-2026_02/modelos/).
- [Métricas](resultados/modelado/ejecuciones/baselines_05-09-2026_02/metricas_baselines.csv).
- [Guía de carga](resultados/modelado/ejecuciones/baselines_05-09-2026_02/COMO_CARGAR.txt).
- [Manifiesto de entrenamiento](resultados/modelado/ejecuciones/baselines_05-09-2026_02/manifiesto_baselines.json).
- [Verificación de entrega](resultados/modelado/ejecuciones/baselines_05-09-2026_02/verificacion_entrega.json).
- [Respaldo de notas con ablación y PCA, 12-09-2026](documentacion/Tesis_Vault_Ablacion_PCA_12-09-2026.zip).
- [Inventario y hashes del respaldo](documentacion/inventario_vault_ablacion_pca_12-09-2026.json).
- [Auditoría de la presentación](documentacion/auditoria_presentacion_06-09-2026.json).

Para visualizar el HTML, descargar o clonar el repositorio y abrir el archivo local.
Las imágenes están en `attachments/Analisis de Datos/`; conservar esa estructura.
GitHub muestra el código del HTML, no una presentación alojada.

## Reproducción

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/baselines_estaticos.py --run-dir resultados/modelado/ejecuciones/NOMBRE_NUEVO
```

El entrenamiento utiliza `resultados/modelado/dataset_modelado.csv` y comprueba la
partición congelada por participante. El directorio de ejecución debe ser nuevo.
Solo entrenamiento ajusta imputadores, escaladores y estimadores; validación, prueba
y P29 se evalúan por separado. El protocolo de etiquetas es offline por participante.

## Modelos y resultados

Cinco objetivos: atención principal, activación principal de 6 s, atención PCA,
activación de 2 s y activación PCA. Cada objetivo incluye Dummy, Ridge y Random Forest
para regresión, y Dummy, logística y Random Forest para clasificación.

La clasificación principal en prueba obtiene balanced accuracy de 0,3240/0,3197
para atención (logística/Random Forest), y 0,3169/0,3365 para activación de 6 s.
La referencia Dummy es 0,3333. Los resultados estáticos permanecen cerca de esa referencia.
Diez pruebas aprobadas; los 30 pipelines producen las mismas predicciones tras recargarse.

## Documentación del vault

Las notas Markdown de trabajo se mantienen en la sección `01 Tesis MDS` del vault.
El ZIP conserva su estructura completa, notas, presentaciones y adjuntos. Reemplaza como
snapshot documental a las copias antiguas que fueron retiradas del árbol de trabajo durante
la consolidación del vault. El archivo no incluye Vinson, inglés ni configuración personal.
El inventario registra SHA256 y tamaño de cada archivo para verificar la copia.

Los modelos y predicciones de la ejecución final se versionan por solicitud expresa del
06-09-2026. Datos crudos, credenciales y cachés permanecen excluidos. Los incidentes de
ejecuciones documentadas se conservan para mantener la trazabilidad de los intentos.
