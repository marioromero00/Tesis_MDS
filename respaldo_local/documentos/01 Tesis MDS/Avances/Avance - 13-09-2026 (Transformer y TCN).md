# Avance: 13-09-2026, Transformer y TCN

Continúa [[Avance - 12-09-2026 (Ablacion y PCA)]]. Fuente: informe
`documentacion/Transformer_TCN_13-09-2026.md` y resultados en
`resultados/redes_13-09-2026/` del repositorio de código, commit `4427064`.

## Trabajo completado

Se probaron Transformer y TCN para activación con las mismas 24 variables de EEG,
mirada y pupila. GSR permanece reservado al Modelo Profesor; etiqueta arousal_label_6s
sin cambios. Atención no se reentrenó en esta ronda.

Seis configuraciones: tres por arquitectura, con contextos de 8/32 ventanas,
anchos de 16/32, dropout de 0,2/0,3/0,4, learning rate de 0,001/0,0005 y
weight decay de 0,01/0,1. Se evaluaron épocas 4/8/12 y suavizado 1/8/32.
Los valores se combinaron en tres recetas; no fue una grilla cartesiana completa.

Cinco folds externos con las mismas 25 personas de train. Cada selección usa una
división interna fija de 16/4 personas; después se reajusta con 20 y se evalúa en 5.
Se congelaron las 15 selecciones antes de evaluar los folds externos. Una semilla.
La selección conjunta es el contraste principal; cada familia y el control repetido
son secundarios. Validation y test originales no se reevaluaron.

## Resultados

| Modelo | BA macro por persona | Macro-F1 |
|---|---:|---:|
| Selección conjunta | 0,371558 | 0,354706 |
| Transformer | 0,363442 | 0,344896 |
| TCN | 0,366822 | 0,353388 |
| Control de ventana actual repetida | 0,374911 | 0,350649 |
| Ridge anterior | 0,374750 | 0,364596 |

La selección conjunta pierde 0,319 puntos porcentuales frente a Ridge, IC descriptivo
[-2,612; +1,993], con mejora en 12/25 personas y un empate. No hay mejora clara.
Tampoco supera al máximo exploratorio anterior sin fixation_count, 0,384325.

El historial frente al control repetido da -0,335 pp, IC [-1,466; +0,863]. El control
se entrena desde cero con la arquitectura, época y suavizado elegidos para la selección
conjunta. Ambos conservan suavizado temporal de salida: este contraste mide el aporte
de la secuencia de entrada. El control no tiene una búsqueda de hiperparámetros propia.

Recall medio de la selección conjunta: 19,62 %, frente a 23,27 % de Ridge. Transformer
alcanza 18,14 % y TCN 18,63 %. Aumentar capacidad no resolvió la clase media ni alcanzó
la meta BA macro 0,50. No se modificaron etiquetas o métricas para obtener ese valor.

## Auditoría y límites

Se conservaron 30 entrenamientos internos con 90 checkpoints, 270 puntuaciones de
decisiones internas, 20 modelos externos, curvas y 54.096 predicciones externas.
La auditoría recargó los 110 modelos, reajustó preprocesadores solo con fit, reconstruyó
selecciones y recalculó las métricas por fold y persona. Error máximo de scores
2,98e-8, dentro de tolerancia 1e-7 para float32/CSV; clases idénticas.

Las 61 pruebas del proyecto pasaron en 11,760 segundos. Se verificaron máscaras,
padding, exclusión de ventanas futuras, reinicios y predicción sin señales del profesor.
Transformer tiene una capa y cuatro cabezas; TCN, cuatro bloques residuales con
dilataciones 1/2/4/8. Se reinicia historial por persona, grabación o discontinuidad;
puede cruzar estímulos. La normalización original sigue siendo offline.

Los intervalos usan 2.000 remuestreos pareados por persona, sin corrección por búsqueda
múltiple ni dependencia entre folds. Una sola semilla y un split interno por fold
limitan la estabilidad de la selección. Las muchas rondas sobre train siguen siendo
exploratorias, sin confirmación independiente.

## Artefactos y publicación

Código, modelos, checkpoints, predicciones, informe y figura PNG/PDF quedaron en el
commit `4427064`. Se verificaron 281 hashes contra los archivos preparados para Git.
Respaldo de esta sección: `documentacion/Tesis_Vault_Redes_13-09-2026.zip`, con
inventario `documentacion/inventario_vault_redes_13-09-2026.json`.

Ver [[Tesis_MDS]], [[Resumen Diseño Etiquetas y Modelos]] y
[[Avance - 12-09-2026 (Ablacion y PCA)]].
