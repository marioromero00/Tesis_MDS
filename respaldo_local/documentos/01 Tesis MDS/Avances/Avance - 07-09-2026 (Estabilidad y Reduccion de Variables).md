# Avance — 07-09-2026: Estabilidad y reduccion de variables

> Reemplaza como fuente vigente para el panel de entradas a
> [[Avance - 07-09-2026 (Importancia de Variables)]]. Conserva ese análisis como exploración previa.

Fuente: ejecución local de `scripts/estabilidad_variables.py`, informe generado desde CSV
y auditoría `scripts/verificar_estabilidad.py`, completados el 07-09-2026.
Repositorio: `C:/Users/MarioRomero/desktop/mds/Tesis_MDS/`.

## Resultado y decisión

La mejora de activación con pupila sola observada en la validación inicial no se sostuvo
en las cinco particiones internas. Balanced accuracy macro sobre 25 participantes:

| Activación | Completo, 25 entradas | Pupila, 6 | Pupila sin validez, 5 |
|---|---:|---:|---:|
| Logística | 0,3520 | 0,3452 | 0,3536 |
| Random Forest | 0,3538 | 0,3389 | 0,3386 |

El Dummy macro de activación fue 0,3467. P34 y P46 solo presentan dos clases, por lo que
el promedio de BA por participante del Dummy no es exactamente 1/3. Las diferencias
de los modelos de activación frente al Dummy incluyen cero en sus intervalos descriptivos.
Las cinco variables pupilares quedan como candidato mínimo, no como ganador confirmado.

Para atención, el algoritmo de redundancia seleccionó las mismas nueve entradas en los
cinco folds (Jaccard 1). Sin embargo, RF baja de 0,3492 completo a 0,3382 compacto:
Δ = -0,0110, intervalo descriptivo [-0,0211; -0,0008]. EEG solo con logística obtiene
0,3445, frente a 0,3335 completo, pero conserva el indicador de ruido del baseline.
No se adopta una reducción universal para todos los modelos.

Los scores continuos siguen débilmente predichos. Ridge con cinco entradas pupilares
tiene MSE macro prácticamente 1, igual al predictor de la media; los RF de regresión
son peores que el Dummy en todos los conjuntos evaluados.

## Panel congelado

- Atención: completo EEG + GSR (18), EEG (9) y compacto sin ruido eléctrico (9).
- Activación: completo (25), pupila (6), mirada + pupila (16), pupila sin fracción de
  validez binocular (5) y mirada + pupila sin esa fracción (15).

Compacto de atención: `eeg_rms_uv`, `eeg_alpha_relative`, `eeg_theta_relative`,
`eeg_beta_relative`, `gsr_tonic_mean_z`, `gsr_phasic_mean_z`, `gsr_slope_z_s`,
`gsr_std_z`, `gsr_scr_count`.

Pupila sin validez: `pupil_mean_z`, `pupil_std_z`, `pupil_min_z`, `pupil_max_z`,
`pupil_slope_z_s`. Se retira la columna explícita de calidad, pero el imputador conserva
indicadores de ausencia: no se elimina toda información de adquisición.

Las columnas exactas quedaron en `conjuntos_congelados.json` antes de calcular las
métricas finales de validación. Es un panel comparativo, no una selección definitiva
de un ganador. Se mantienen las entradas completas como control del futuro modelo temporal.
Reducir entradas del estudiante no elimina sensores necesarios para el profesor.

## Procedimiento

Se ejecutó GroupKFold con cinco folds exclusivamente dentro de train: 20 participantes
para ajustar y cinco para evaluar en cada fold; 25 en total y 13.524 ventanas.
Cada participante se evaluó fuera de entrenamiento una vez por configuración.
Se mantuvieron pseudoetiquetas, contexto GSR de 6 s, partición original y baselines.

Imputación y escalado se ajustaron dentro de cada fold. La reducción de atención usa
Spearman absoluto ≥0,90 solo en los participantes de ajuste, con prioridad explícita
por RMS y nivel tónico GSR; excluye ruido eléctrico, constantes y redundancias.
Los intervalos remuestrean participantes, no ventanas. Son descriptivos, sin corrección
por comparaciones múltiples y con conjuntos de ajuste compartidos entre folds.

Este contraste hereda hipótesis sugeridas por la exploración anterior de train/validación;
no constituye confirmación externa independiente. También hereda normalización offline
por participante. Test no se volvió a evaluar. TCN/LSTM no se entrenó en esta etapa.

## Entrega verificada

- 180 ajustes internos y 36 pipelines finales guardados con columnas y hashes.
- 486.864 predicciones fuera de fold y 900 métricas por participante recalculadas.
- Recarga exacta de predicciones y probabilidades de los modelos finales.
- 18 pruebas aprobadas; auditoría de cobertura y separación por participante.
- Informe completo, tablas generadas desde CSV, figuras PNG/PDF y protocolo reproducible.

[Informe de estabilidad y decisiones](../../Tesis_MDS/documentacion/Estabilidad_Variables_07-09-2026.md).
[Resultados y modelos](../../Tesis_MDS/resultados/estabilidad_variables_07-09-2026/).

Actualización posterior del 07-09-2026: el trabajo se publicó en GitHub, commit `2575183`.
El respaldo de notas del 07-09-2026 incorpora este avance; el del 06-09-2026 queda histórico.
Registro: [[Avance - 07-09-2026 (Publicacion de Analisis en GitHub)]].

## Siguiente paso

Implementar el contraste temporal con este panel, manteniendo pseudoetiquetas, split y
modelo completo de referencia. El panel permite estudiar reducción y modalidad sin
atribuir una mejora que estos resultados no confirman.

## Notas relacionadas

- [[Tesis_MDS]]
- [[Avance - 07-09-2026 (Importancia de Variables)]]
- [[Avance - 05-09-2026 (Baselines Entrenados y Guardados)]]
