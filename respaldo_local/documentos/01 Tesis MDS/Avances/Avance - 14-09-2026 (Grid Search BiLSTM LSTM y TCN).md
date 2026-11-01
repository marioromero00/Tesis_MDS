# Avance: 14-09-2026, Grid Search BiLSTM LSTM y TCN

Continúa [[Avance - 13-09-2026 (Grid Search Transformer)]]. Cierre documental del
14-09-2026 para las grillas ejecutadas el 13-09-2026, hora de Santiago.
Fuentes: `documentacion/Grid_BiLSTM_LSTM_TCN_13-09-2026.md` y
`resultados/grids_recurrentes_13-09-2026/` del repositorio de código.

## Ejecución completada

Se entrenó y auditó BiLSTM, después LSTM y finalmente TCN. El registro
orden_ejecucion.jsonl confirma que cada auditoría terminó antes de iniciar
el entrenamiento de la siguiente familia. No se modificaron las grillas
después de observar los resultados de una familia.

Cada familia probó 32 configuraciones cartesianas de contexto 8/32 ventanas,
hidden size 16/32, profundidad 1/2, learning rate 0,0003/0,001 y dropout 0,1/0,4.
En LSTM/BiLSTM, profundidad es número de capas; en TCN, corresponde a dos o
cuatro bloques residuales, con dilataciones 1/2 o 1/2/4/8. Se evaluaron épocas
2/4/8/16 y suavizado causal 1/8/32. AdamW, weight decay 0,01 y batch 256 fijos.

Por familia: 160 entrenamientos internos, 640 checkpoints, 1.920 puntuaciones
de decisiones internas y 20 modelos externos. Total: 480 entrenamientos internos,
1.920 checkpoints y 60 modelos externos; 5.760 puntuaciones internas y 162.288
predicciones externas. Todos los intentos y curvas se conservaron.

## Resultados

BA macro promedia las clases observadas por persona y después las dos semillas.
Macro-F1 de la tabla agrupa ambas semillas; no representa un ensamble.

| Familia | BA macro | Macro-F1 | Recall medio | BA del control repetido |
|---|---:|---:|---:|---:|
| BiLSTM | 0,341003 | 0,321478 | 16,22 % | 0,347688 |
| LSTM | 0,333267 | 0,312699 | 14,48 % | 0,350505 |
| TCN | 0,352902 | 0,329343 | 14,50 % | 0,345768 |

Ninguna grilla supera al Ridge anterior, 0,374750. TCN queda próxima al
Transformer grid, 0,352601, con diferencia de +0,030 pp e IC descriptivo
[-1,937; +1,894]. La meta BA macro 0,50 no se alcanzó.

Frente a Ridge, las diferencias son BiLSTM -3,375 pp, IC [-6,065; -0,513];
LSTM -4,148 pp, IC [-6,563; -1,643]; TCN -2,185 pp, IC [-4,815; +0,771].
Son contrastes descriptivos de esta búsqueda adaptativa, sin corrección múltiple.

## Aporte del historial

Cada control repite la ventana actual en todas las posiciones reales, mantiene
longitud/padding y se entrena desde cero con configuración, época, semilla y
suavizado emparejados. Conserva suavizado de salida y no tiene búsqueda propia.
El contraste mide la secuencia de entrada, no toda temporalidad.

- BiLSTM: -0,668 pp frente al control, IC [-1,997; +0,711].
- LSTM: -1,724 pp, IC [-2,959; -0,618].
- TCN: +0,713 pp, IC [-0,134; +1,515], mejora en 20/25 personas.

TCN muestra una ganancia media frente a su control, pero el intervalo incluye
cero. LSTM pierde BA con historial en esta configuración de búsqueda. No se
demuestra superioridad temporal estable ni importancia fisiológica de las entradas.

## Diseño y límites

Mismas 25 personas de train, 13.524 ventanas, etiqueta arousal_label_6s fija y
24 variables de EEG/pupila/mirada. GSR queda reservado al Modelo Profesor.
Atención no se reentrenó; validation/test originales no se reevaluaron.

Cinco folds externos de 20/5 personas; selección en un split interno fijo 16/4.
Las cinco elecciones por familia se congelaron antes de su evaluación externa.
Una semilla interna y dos externas: 20260913 y 20260914. Las dos externas
miden variación del reajuste, no estabilidad de la búsqueda. Las configuraciones
y cantidades de parámetros seleccionadas por fold se conservan en el informe.

BiLSTM recorre en ambos sentidos solo la historia que termina en la ventana
predicha. Usa los estados finales forward/reverse de la última capa y excluye
padding mediante secuencias empaquetadas. No recibe ventanas futuras al endpoint;
requiere recomputar el bloque pasado. TCN usa convoluciones con padding izquierdo.

Preprocesado ajustado solo con fit; reinicios por persona, grabación o salto
distinto de un segundo. Puede cruzar estímulos. La normalización original sigue
siendo offline; no se valida un pipeline completo en tiempo real.

IC de 2.000 remuestreos pareados de personas después de promediar semillas,
sin corrección por búsqueda múltiple ni dependencia entre folds. Las muchas
rondas sobre train siguen siendo exploratorias, sin confirmación independiente.
Un split interno de cuatro personas puede producir selección inestable.

## Auditoría y documentación

1.980 modelos recargados, preprocesado y selección reconstruidos, métricas por
fold/persona y predicciones recalculadas. Tolerancia de scores 1e-7 para float32/CSV;
clases idénticas. Predicción auditada sin etiquetas ni señales del profesor.
Las 66 pruebas del proyecto pasaron en 14,740 segundos; incluyen exclusión de
futuro/padding y conservación del RNG al guardar/evaluar checkpoints.

Cuatro figuras PNG/PDF: una comparación y una matriz por familia. Rankings y
efectos internos descriptivos guardados; no redefinen un ganador externo.
Inventario de entrega con 5.118 hashes de archivos.

## Publicación

Código, resultados, modelos e informe en el commit `40cfa2f`. Los 5.118 hashes
se verificaron también contra los archivos preparados para Git. Se conservaron
los logs originales, incluido el espaciado de las tablas de consola.
Respaldo: `documentacion/Tesis_Vault_Grids_Recurrentes_14-09-2026.zip`, con
inventario `documentacion/inventario_vault_grids_recurrentes_14-09-2026.json`.

Ver [[Tesis_MDS]], [[Avance - 13-09-2026 (Grid Search Transformer)]] y
[[Avance - 12-09-2026 (Ablacion y PCA)]].
