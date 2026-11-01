# Reconstrucción de profesores de atención binaria — 29-10-2026

El usuario pidió reconstruir las etiquetas desde el profesor y volver a entrenar, sustituyendo el agrupamiento de las antiguas clases alta/media/baja. Esta corrida es independiente de `atencion_binaria_29-10-2026` y conserva sus resultados.

## Fuente y regla

Se leen únicamente características de `resultados/preprocesamiento/caracteristicas_multimodales.csv` y la partición congelada. No se leen scores ni etiquetas de atención anteriores. Se trabaja en las 25 personas de train.

Se transforman `fixation_total_ms`, `fixation_mean_ms`, `gaze_dispersion_2d_px` y `gaze_path_length_px` con log1p tras truncar negativos a cero; `pupil_mean_z` se conserva. Cada variable se normaliza por persona con media y desviación poblacional de la sesión. Las dos dispersiones/movimiento llevan signo negativo; fijaciones y pupila, positivo. Si falta algún componente, no se genera etiqueta para esa ventana. Una variable constante produce componente ausente; no se inventa una clase.

- **Profesor igualitario:** promedio ocular de cuatro componentes, combinado 50/50 con el componente pupilar. Pesos finales: 0,125 para cada ocular y 0,5 para pupila.
- **Profesor PCA:** primer componente de los cinco componentes normalizados. Ajuste solo sobre las personas de entrenamiento de cada fold; orientación fijada por producto escalar con los pesos del profesor igualitario, sin consultar resultados predictivos.

Para ambos, **1 = atento si el nuevo score supera su mediana personal; 0 = no atento si es menor o igual**. Empates quedan en 0; ausentes permanecen ausentes. No se fuerza exactamente 50/50 por desempate arbitrario.

Esta es una operacionalización relativa y offline de atención. “No atento” significa score inferior o igual a la referencia de esa persona en esta sesión; no es una verdad psicológica externa. Normalización y mediana usan la sesión completa, incluidas ventanas futuras respecto a cada instante: no presentar el profesor como detector online. Las entradas temporales del estudiante sí se limitan a pasado y ventana actual.

## Modelos y evaluación

Cinco folds de atención originales, sin participantes compartidos entre ajuste y evaluación. EEG/GSR como entradas del estudiante; mirada/pupila y scores del profesor excluidos. Dummy, logística, Random Forest, MLP, TCN y LSTM; mismos hiperparámetros y semillas que la comparación binaria previa, ahora entrenados desde cero para las etiquetas nuevas. La suite comprueba ausencia de dependencia de etiquetas antiguas, corte mediano y empates, datos ausentes y PCA ajustado sin personas de evaluación.

Logística/RF: actual frente a actual+media+desviación+cambio del historial. TCN/LSTM: actual repetida frente a historial real, preservando longitud y arquitectura. Hasta ocho ventanas consecutivas. Imputador y escalador ajustados solo dentro del fold.

Se exportan etiquetas de cada profesor de fold y predicciones OOF. El profesor full-train se guarda para uso posterior; sus etiquetas PCA pueden diferir de las de los profesores de fold y no se sustituyen en las evaluaciones OOF.

ROC-AUC promedio por participante, AUC agrupada, average precision y BA con umbral fijo 0,5. Dos semillas en redes. Intervalos descriptivos y contrastes pareados por bootstrap de personas (2.000 réplicas). Validation, test y P29 sin evaluar. Cada profesor define una referencia distinta; comparar AUC entre profesores no valida qué referencia representa mejor atención real.

## Reproducción

```sh
.venv/bin/python -m unittest discover -s tests -p test_profesor_binario_reconstruido.py -v
.venv/bin/python scripts/reconstruir_profesor_atencion_binaria.py
```

Entorno: `requirements_atencion_binaria_macos.lock.txt`.

[Resultados y predicciones](../resultados/profesor_binario_reconstruido_29-10-2026/INFORME.md).
