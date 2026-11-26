# Diagnóstico: predicciones idénticas en el enfoque E1 (26-11-2026)

**Duda de la auditoría del 23-11.** En `resultados/enfoques_41p_22-11-2026`, las predicciones del modelo con historial y posición (`c32_pos`) son idénticas a las del modelo con historial (`hgb_c32`). No se podía descartar un error sin reentrenar un fold.

**Qué se hizo.** Un único ajuste de diagnóstico, sin guardar resultados: partición 1101, fold 0, etiqueta de atención corregida por posición, con las mismas funciones de `scripts/enfoques_41p.py` (`corrected_attention`, `fold_setup`, `hgb_matrix`, `fit_hgb`). No es un análisis nuevo ni cambia ninguna cifra.

**Resultado.**

- La columna de posición sí entra a la matriz del modelo (1.924 columnas: 1.923 del historial más la posición).
- El modelo hace 1.800 divisiones en 300 iteraciones y **ninguna usa la columna de posición**.
- Las predicciones del ajuste coinciden exactamente con las guardadas en `e1_1101.csv.gz` (diferencia máxima 0,0 en 3.097 filas).

**Lectura.** No es un error. La etiqueta corregida se construye para que la posición no la prediga (la posición sola da AUC 0,504), así que el modelo nunca elige esa columna y sus predicciones quedan iguales a las del modelo sin ella. El contraste A3 equivale, en la práctica, a comparar el modelo con historial contra el modelo de la ventana actual con posición. La cifra no cambia.

De paso, el ajuste confirma para este fold que las predicciones guardadas provienen de la configuración declarada (reproducción exacta).
