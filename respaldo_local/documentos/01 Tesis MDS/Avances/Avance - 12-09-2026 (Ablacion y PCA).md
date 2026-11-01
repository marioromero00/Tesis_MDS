# Avance: 12-09-2026, Ablacion y PCA

Continúa [[Avance - 12-09-2026 (Busqueda Meta 05)]]. Estudio de contribución predictiva
de modalidades, variables y contexto temporal, más reducción con PCA para activación.
Fuente: `documentacion/Ablacion_PCA_12-09-2026.md` y
`resultados/ablacion_pca_12-09-2026/` del repositorio de código.

## Diseño ejecutado

38 variantes, cinco folds con las mismas 25 personas de train. Se mantiene la etiqueta
arousal_label_6s y se usa Ridge con los hiperparámetros elegidos previamente dentro de
cada fold. La referencia reproduce BA macro 0,37475. Cada ablación reajusta imputación,
escalado y clasificador; no se vuelve a buscar hiperparámetros por variante.

- Quitar EEG, mirada o pupila; conservar cada modalidad por separado.
- Quitar historial, suavizado o ambos.
- Quitar cada una de las 24 variables con todas sus derivadas e indicadores de ausencia.
- PCA después del escalado, conservando 80 %, 90 % o 95 % de varianza, más PCA completo
  como control de rotación. Solo se ajusta con las personas de entrenamiento.

Los contrastes principales declarados son quitar cada modalidad y quitar ambos usos
temporales. Las variables individuales y PCA son secundarios. GSR sigue reservado al
Modelo Profesor. No se entrenaron modelos nuevos de atención ni se reevaluó validation/test.

## Modalidades e historial

| Variante | BA macro |
|---|---:|
| Completo | 0,3748 |
| Sin EEG | 0,3546 |
| Sin mirada | 0,3706 |
| Sin pupila | 0,3740 |
| Solo EEG | 0,3722 |
| Solo pupila | 0,3616 |
| Solo mirada | 0,3470 |
| Ventana actual, con el mismo suavizado | 0,3670 |
| Sin suavizado | 0,3719 |
| Ventana actual y sin suavizado | 0,3604 |

Quitar EEG produce la mayor pérdida media por modalidad: 2,019 puntos porcentuales,
IC descriptivo [+0,045; +4,116], con pérdida en 17/25 personas. Los intervalos de las
otras dos modalidades incluyen cero. Las variables correlacionadas pueden compensarse;
estos resultados no demuestran importancia causal ni fisiológica.

Solo EEG conserva una BA cercana, pero reduce recall medio de 0,2327 a 0,1079 y macro-F1
de 0,3646 a 0,3385. No basta la BA para recomendar ese recorte como modelo final.
Quitar historial y suavizado pierde 1,434 puntos, IC [-0,814; +3,527]. La referencia
usa representaciones distintas por fold, incluido uno ya estático y otro sin suavizado.

## Variables individuales

Las mayores pérdidas medias al quitar una variable son:

| Variable | Pérdida de BA (pp) |
|---|---:|
| eeg_peak_to_peak_uv | +0,421 |
| pupil_mean_z | +0,356 |
| gaze_path_length_px | +0,260 |
| pupil_max_z | +0,234 |

Sus intervalos incluyen cero: no hay un orden definitivo entre ellas. Quitar una
variable mide su aporte adicional condicionado al resto y a este clasificador.

Quitar fixation_count sube la BA a 0,38433, +0,957 puntos frente a 0,37475; IC
descriptivo [+0,287; +1,702], mejora en 17/25 personas. Macro-F1 sube a 0,3733 y
recall medio a 0,2400. Es un máximo secundario entre 24 eliminaciones: no se corrigió
por comparaciones múltiples ni exploraciones previas, y no se confirmó en otro conjunto.
No se combinaron automáticamente las eliminaciones favorables para formar un panel final.

## PCA

| Varianza retenida | Componentes según fold | BA macro |
|---|---:|---:|
| 80 % | 9–27 | 0,3554 |
| 90 % | 13–45 | 0,3764 |
| 95 % | 16–64 | 0,3644 |
| Completa | 28–324 | 0,3748 |

Los números de entrada incluyen derivados temporales e indicadores de ausencia;
no son 324 sensores. PCA completo reproduce las clases de referencia y sus scores
con tolerancia 1e-9. El 90 % mejora solo +0,165 puntos, con intervalo de ganancia
[-2,032; +2,433]. Su recall medio es 0,2177 y macro-F1 0,3614.

PCA comprime varianza, no selecciona relevancia para la etiqueta. Se conservaron
cargas y varianzas por componente/fold; los signos son arbitrarios y las componentes
de distintos folds no se trataron como equivalentes.

## Auditoría y artefactos

190 modelos guardados y recargados, 513.912 predicciones verificadas, 190 preprocesadores
y 20 PCA reajustados en auditoría. Se verificaron 489.630 cargas, 190 métricas de fold
y 950 por participante. Las 59 pruebas del proyecto pasaron en 6,958 segundos.
Los modelos reducidos se pueden cargar con `predecir_ablacion_pca.predict(bundle, frame)`:
solo requieren señales retenidas y metadatos temporales, sin etiquetas.

Informe y cuatro figuras PNG/PDF: modalidades/contexto, variables, desempeño con PCA
y varianza acumulada. Scripts: `ablacion_pca_core.py`, `entrenar_ablacion_pca.py`,
`auditar_ablacion_pca.py`, `informe_ablacion_pca.py` y `predecir_ablacion_pca.py`.

IC descriptivos de 2.000 remuestreos pareados por persona; no corrigen dependencia de
folds ni búsqueda adaptativa. La normalización original sigue siendo offline.
La meta 0,50 no se alcanzó. La reducción de entradas requiere selección interna futura
y confirmación independiente, manteniendo también recall medio y macro-F1.

Ver [[Tesis_MDS]], [[Resumen Diseño Etiquetas y Modelos]] y
[[Avance - 12-09-2026 (Busqueda Meta 05)]].

## Publicación

Modelos, resultados, código e informe publicados en GitHub `main`, commit `3bbedf1`.
Se comprobaron 221 hashes frente a los archivos preparados para Git. Respaldo de
esta sección: `documentacion/Tesis_Vault_Ablacion_PCA_12-09-2026.zip`, con inventario
`documentacion/inventario_vault_ablacion_pca_12-09-2026.json`.
