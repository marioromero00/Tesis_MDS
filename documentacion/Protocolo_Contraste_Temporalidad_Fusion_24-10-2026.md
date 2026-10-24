# Protocolo propuesto: temporalidad y fusión multimodal — 24-10-2026

**Estado:** diseño previo a ejecución. No contiene resultados nuevos ni modifica las cinco decisiones abiertas sobre las pseudoetiquetas. Las comparaciones, parámetros y criterios de lectura de este documento deben quedar aceptados antes de entrenar; cualquier cambio posterior se registra como desviación, sin reemplazar esta versión.

## Pregunta

Con pseudoetiquetas y participantes fijos, ¿aporta la secuencia de ventanas pasadas a la predicción y cambia el desempeño al fusionar las modalidades antes o después del modelo? El análisis principal es de **activación** (`arousal_label_6s`); **atención** (`attention_label_equal`) repite el mismo diseño como contraste secundario. El objetivo es estimar diferencias de desempeño, no buscar otra vez el máximo BA 0,50.

## Datos y separación de señales

- Usar solo el `train` original del `dataset_modelado.csv`: 25 participantes, con los cinco folds externos por participante del protocolo anterior (20 para ajustar y 5 para evaluar). No usar `validation`, `test` ni P29 para elegir arquitectura, umbrales o ganadores. Verificar hashes de dataset, partición y código antes de iniciar.
- Mantener etiquetas, umbrales, exclusiones y partición congelados. No recalcular el Modelo Profesor.
- Activación: entradas de pupila (5), mirada (10) y EEG (9); GSR solo construye la pseudoetiqueta. Atención: EEG (9) y GSR (9); pupila y mirada solo construyen la pseudoetiqueta. Usar exactamente las listas de `scripts/explorar_fusiones.py` y registrar sus columnas en el manifiesto de ejecución.
- Ajustar imputación con indicadores de ausencia y escalado únicamente en las personas de ajuste de cada fold. Separar el ajuste de cada modalidad en fusión tardía. Ninguna etiqueta ni señal del Modelo Profesor entra al predictor correspondiente.

## Diseño de cuatro condiciones por objetivo

| Código | Entrada del TCN | Fusión | Predicción |
|---|---|---|---|
| E-R | Historial real | Temprana | Un TCN con todas las entradas permitidas concatenadas |
| E-C | Ventana actual repetida | Temprana | Mismo TCN, entrenado desde cero con el control |
| T-R | Historial real | Tardía | Un TCN por modalidad; media aritmética de probabilidades con pesos iguales |
| T-C | Ventana actual repetida | Tardía | Mismos expertos y pesos, entrenados desde cero con el control |

El control repite la ventana actual en las posiciones válidas del mismo bloque, conservando longitud y padding. Los cuatro brazos usan los mismos folds, etiquetas, semillas y regla de decisión (`argmax`, con orden de clases `bajo`, `medio`, `alto`). La fusión tardía no aprende pesos ni elige un experto ganador. No aplicar suavizado de salida: ventana igual a 1. Así, el contraste de historial incluye solo la secuencia de entrada. Los modelos tardíos suman más capacidad que el temprano; el contraste de fusión describe el sistema completo, no aísla causalmente el punto de fusión.

## Parámetros fijados para esta propuesta

- TCN causal ya implementada en `recurrentes_grid_core.py`: contexto de 8 ventanas de 2 s con paso de 1 s, hidden size 32, dos bloques con dilataciones 1 y 2, kernel 3, dropout 0,1.
- Entrenar 8 épocas completas, AdamW con learning rate 0,001 y weight decay 0,01, batch 256 y clip de gradiente 1. Sin búsqueda de hiperparámetros, selección de época ni early stopping.
- Dos semillas de reajuste, 20261024 y 20261025. Cada brazo se ajusta desde cero en cada fold y semilla. Orden de ejecución y recursos: una tarea a la vez; guardar cada intento para poder reanudar sin repetirlo.
- Reiniciar el historial al cambiar participante, grabación, segmento o estímulo, o si el paso temporal deja de ser 1 s. Esta regla debe aplicarse igual en ajuste y evaluación y comprobarse con una prueba de exclusión de futuro y de cruce entre segmentos.

Estos valores son una elección simple dentro de las grillas ya exploradas, fijada antes de observar cualquier resultado de este nuevo contraste. No se debe ajustarlos usando las métricas externas del mismo experimento. Una logística de ventana actual, ajustada en los mismos folds, puede servir como referencia estática adicional si se conserva su configuración anterior. El Ridge multiescala de activación (BA macro histórica 0,3748) usa historial resumido: mostrarlo como contexto exploratorio, no como baseline estático ni como diferencia pareada nueva sin reconstruir sus predicciones por persona.

## Comparaciones y lectura

La métrica principal es BA macro por participante: promediar el recall de las clases presentes en cada persona, luego promediar personas con igual peso y finalmente semillas. Conservar además BA global, macro-F1, recall y fracción predicha por clase. Reportar resultados por fold, persona y semilla; no tratar las dos semillas como 50 personas independientes.

1. **Temporalidad principal, activación:** E-R menos E-C. El mismo contraste en atención es secundario.
2. **Fusión principal, activación:** T-R menos E-R. El mismo contraste en atención es secundario.
3. **Controles descriptivos:** T-R menos T-C, T-C menos E-C y la interacción `(T-R − T-C) − (E-R − E-C)` para cada objetivo. No seleccionar un ganador entre estos contrastes después de observarlos.

Para cada diferencia, informar valor medio, número de personas que mejoran y un intervalo descriptivo del 95 % con 2.000 remuestreos pareados de los 25 participantes, después de promediar semillas. Informar también resultados negativos o nulos. Dada la reutilización exploratoria de `train`, los intervalos no constituyen confirmación independiente ni corrigen todas las comparaciones previas. Evitar afirmar superioridad estable solo porque una media sea positiva; observar amplitud del intervalo y desempeño de la clase media.

## Entrega y condiciones de cierre

- Antes del primer ajuste: guardar manifiesto con hashes, listas de columnas, folds, semillas, parámetros y las comparaciones anteriores. La implementación debe leer ese manifiesto y rechazar cambios de fuentes o partición.
- Guardar modelos recargables, probabilidades y predicciones fuera de fold, métricas por persona/fold/semilla, trazas de entrenamiento, fallos y reanudaciones. Auditar que recargar los modelos reproduce predicciones y que nunca se usan señales del Modelo Profesor como entradas.
- Correr las pruebas del proyecto y añadir pruebas específicas para causalidad de secuencia, control repetido, separación de modalidades y pesos de fusión. Mantener `validation` y `test` sin evaluar en esta ronda.
- El resultado será un contraste **exploratorio**. Una evaluación confirmatoria requerirá acordar aparte un protocolo final y una fuente independiente; no cambiar aquí los criterios científicos aún abiertos.

## Base documental

- `documentacion/Grid_BiLSTM_LSTM_TCN_13-09-2026.md`: cinco folds, controles repetidos, TCN causal y límites de la inferencia anterior.
- `documentacion/Fusiones_10-09-2026.md`: panel de entradas permitido, fusiones y separación Modelo Profesor/Modelo Estudiante.
- `resultados/modelado/manifiesto_etiquetas.json` y `resultados/modelado/particion_participantes.csv`: etiquetas provisionales y partición congelada.
