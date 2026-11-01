# Avance — 07-09-2026: Importancia de variables

> Actualización posterior del 07-09-2026: [[Avance - 07-09-2026 (Estabilidad y Reduccion de Variables)]]
> reemplaza esta nota para las decisiones del panel. La mejora inicial de pupila no se
> sostuvo en el contraste interno; este documento conserva los resultados exploratorios.

Fuente: ejecución local de `scripts/analisis_variables.py` sobre los modelos guardados
del 05-09-2026, en `C:/Users/MarioRomero/desktop/mds/Tesis_MDS/`.
Complementa [[Avance - 05-09-2026 (Baselines Entrenados y Guardados)]].

## Resultado

Se analizaron las entradas del Modelo Estudiante para atención (18) y activación (25),
manteniendo las etiquetas principales y el contexto GSR de 6 s. Se contrastaron
importancias por desplazamiento temporal dentro de segmento, correlaciones de train
y modelos reducidos. Test no se volvió a evaluar.

**Activación permite acotar el próximo experimento a pupila sola (6 variables),
mirada + pupila (16) y la referencia completa (25).** En validación, la regresión
logística pasa de balanced accuracy 0,3626 con todas las entradas a 0,3713 con pupila;
Random Forest pasa de 0,3243 a 0,3563. Los intervalos de diferencia macro por participante
cruzan cero: la mejora puntual no confirma superioridad. Para el score continuo,
Ridge con mirada + pupila conserva R² cercano al completo (0,00577 frente a 0,00543).

En atención, cinco variables conservan aproximadamente la clasificación, pero el
desempeño permanece cerca de 1/3. El top-5 incluye amplitudes EEG redundantes y ruido
eléctrico; no se adopta como conjunto fisiológico definitivo.

## Entradas destacadas

- Atención: componente tónica GSR y amplitud RMS EEG en RF; mínimo GSR en logística.
  El ruido eléctrico también aparece, por lo que debe revisarse como posible confusor.
- Activación: dispersión de mirada en logística y mínimo/máximo pupilar en RF.
- Las seis entradas del candidato pupila son media, desviación estándar, mínimo,
  máximo, pendiente y fracción de validez binocular. La última representa calidad.

RMS, desviación estándar y pico a pico EEG presentan Spearman entre 0,947 y 0,985.
Media, mínimo, máximo y componente tónica GSR presentan Spearman entre 0,985 y 0,996.
La perturbación individual puede inflarse al romper estas dependencias. Los resultados
son exploratorios sobre pseudoetiquetas; no prueban causalidad ni validez psicológica.
Reducir entradas del estudiante no elimina sensores requeridos por el profesor.

## Entrega y protocolo

Informe completo con resultados, interpretación, límites, referencias y figuras:
[Analisis de variables](../../Tesis_MDS/documentacion/Analisis_Variables_07-09-2026.md).

Resultados en `Tesis_MDS/resultados/analisis_variables_07-09-2026/`: rankings globales y
por participante, correlaciones, calidad, comparación de subconjuntos, columnas exactas,
pipelines reducidos y manifiesto de hashes. Figuras en PNG y PDF.

Se verificaron 192 importancias, 56 comparaciones y 48 pipelines reducidos con hashes
y recarga exacta. Pasaron las 14 pruebas, incluidas cuatro nuevas de este análisis.

Se conservaron 25 participantes de train y 8 de validación, con 13.524 y 4.662 ventanas.
La importancia promedia por participante diez desplazamientos circulares por segmento;
los intervalos remuestrean participantes, no ventanas solapadas. Los top-k se eligieron
solo con la importancia de RF ajustado en train. Las recomendaciones usan validación
y requieren comprobar estabilidad antes de congelar una selección definitiva.

No se modificaron los baselines originales, las pseudoetiquetas ni el split. El análisis
hereda normalización por participante offline. Se guardó el trabajo localmente.

## Siguiente contraste

Para activación: 6/16/25 entradas. Para atención: 18 completas y EEG solo (9), más un
candidato sin redundancias ni ruido que todavía debe construirse y evaluarse.
Antes de TCN/LSTM, comprobar estabilidad con particiones internas por participante.
Mantener el modelo temporal con entradas completas como control del efecto de reducir.

## Notas relacionadas

- [[Tesis_MDS]]
- [[ETIQUETAS_Y_BASELINES]]
- [[Avance - 05-09-2026 (Baselines Entrenados y Guardados)]]
