# Enmienda v2 — 23-11-2026, antes de ver resultados

Origen: auditoría independiente de código, hecha con los entrenamientos en marcha y sin leer predicciones. Sin hallazgos bloqueantes. No cambia el código, los modelos, la familia confirmatoria ni las reglas; solo acota la lectura.

Lo verificado: el tensor coincide con el tratamiento de `extract_window` (diferencia máxima 6e-7), las filas no pueden desalinearse de su etiqueta, no hay fuga más allá de la escala y el filtro transductivos, la red aprende una señal sintética con la configuración registrada (AUC 1,0) y da azar con etiquetas barajadas, y particiones, filas, etiquetas y pesos son los de los comparadores.

Límites que se agregan a la lectura fijada:

1. **R3 no tiene control.** No se entrenó una red con el filtro de control. Si R3 da respaldo, muestra que la red pierde al aplicar el filtro ocular, no que la pérdida sea específicamente ocular; la especificidad descansa en L2 del experimento de limpieza. R3 solo se interpreta si la red original queda claramente sobre el azar.
2. **El nulo se lee acotado.** "Esta red, con esta configuración, no supera al HGB", no "un modelo más complejo no mejora". Es una sola arquitectura de 1.217 parámetros, sin búsqueda, con una inicialización por grupo.
3. **No queda registro de convergencia.** Sin validación interna, un nulo no distingue entre falta de información en la señal cruda y falta de ajuste de la red. Si hace falta, se reproducirá un grupo para reportar la curva de entrenamiento como descriptivo declarado a posteriori.
4. **Núcleo temporal corto.** 32 puntos son 0,26 s; la red representa mal la banda de 1–4 Hz, donde estaban las variables más predictivas del HGB. Pesa sobre todo si R1 sale inferior.
5. **Ventanas sin canales utilizables.** 50 ventanas entran con la entrada en cero; el HGB dispone ahí de indicadores de calidad. Además el último lote de algunos grupos tiene entre 2 y 7 ventanas.
