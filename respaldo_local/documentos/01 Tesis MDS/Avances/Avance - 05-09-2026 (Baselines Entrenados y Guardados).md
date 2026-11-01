# Avance — 05-09-2026: Baselines entrenados y guardados

> Fuente: confirmación de Mario en la conversación del 05-09-2026, ejecución local de
> `Tesis_MDS/scripts/baselines_estaticos.py`, manifiesto y verificación de entrega.
> Esta nota es la fuente vigente para localizar y cargar los baselines entrenados.

## Confirmación de continuidad

Mario confirmó que la validación metodológica discutida ya estaba resuelta y pidió entrenar
y guardar los baselines. Se continuó con las etiquetas y parámetros existentes. Esa validación
deja de bloquear esta ejecución; las observaciones históricas conservan su fecha y contexto.
La conversación no especificó nuevos parámetros ni una reinterpretación de la ventana anotada
el 25-08-2026.

## Resultado

Se entrenaron y guardaron **30 pipelines completos** en formato `.joblib`: cinco tareas,
cada una con tres regresores y tres clasificadores.

| Tipo | Modelos |
|---|---|
| Regresión | Dummy de media, Ridge, Random Forest |
| Clasificación | Dummy de prior, regresión logística balanceada, Random Forest balanceado |

| Tarea | Predictores | Rol |
|---|---|---|
| `attention_primary` | EEG + GSR | Atención principal |
| `arousal_primary_6s` | EEG + mirada + pupila | Activación principal, contexto 6 s |
| `attention_pca_sensitivity` | EEG + GSR | Sensibilidad de atención |
| `arousal_2s_sensitivity` | EEG + mirada + pupila | Sensibilidad de contexto GSR |
| `arousal_pca_sensitivity` | EEG + mirada + pupila | Sensibilidad de activación |

Cada archivo incluye imputación, escalado cuando corresponde y estimador ajustado. Su JSON
adyacente contiene columnas en orden, objetivo, clases, participantes de entrenamiento,
hiperparámetros, tamaño, SHA256 y resultado de recarga. Los modelos requieren las características
preprocesadas del proyecto, no señales crudas.

## Ubicación y reproducción

En esta máquina el repositorio ejecutable ya está en:

`C:/Users/MarioRomero/desktop/mds/Tesis_MDS/`

Las rutas históricas `~/tesis/Tesis_MDS` corresponden al contexto anterior. No se trasladaron
archivos durante esta ejecución.

Carpeta de entrega, relativa al repositorio:

`resultados/modelado/ejecuciones/baselines_05-09-2026_02/`

- `modelos/`: 30 `.joblib` y 30 metadatos `.json`, 131.686.305 bytes en modelos.
- `metricas_baselines.csv`: 90 filas, validación, prueba y sensibilidad.
- `predicciones_baselines.csv`: predicciones por ventana.
- `importancia_features.csv`: coeficientes/importancias con nombres posteriores a imputación.
- `config_entrenamiento.json` y `particion_participantes.csv`: configuración y partición utilizadas.
- `manifiesto_baselines.json`: versiones, hashes de entradas, código y catálogo de modelos.
- `verificacion_entrega.json`: comprobación final de integridad y reproducción.
- `COMO_CARGAR.txt`: ejemplo ejecutable de carga y predicción.

Desde la raíz del repositorio, para una ejecución nueva:

```powershell
python scripts/baselines_estaticos.py --run-dir resultados/modelado/ejecuciones/NOMBRE_NUEVO
```

El directorio solicitado debe ser nuevo para evitar sobrescribir una ejecución. El intento
`baselines_05-09-2026/` quedó incompleto por un error al escribir el sufijo del primer JSON;
se corrigió y se marcó con `ESTADO.txt`. La entrega completa es exclusivamente la carpeta `_02`.
Los modelos y las predicciones pesadas se guardaron inicialmente solo en local.
El 06-09-2026 Mario pidió subir también estos artefactos: la ejecución completa `_02`
se incorporó al conjunto preparado para Git; el intento incompleto conserva su exclusión.

## Protocolo conservado

- Semilla `20260822`; Random Forest con 200 árboles, hoja mínima de cinco y `n_jobs=1`.
- Partición por participante verificada contra el CSV congelado: 25 entrenamiento,
  8 validación, 8 prueba; P29 permanece en sensibilidad.
- Cada estimador y su preprocesamiento se ajustan únicamente con entrenamiento.
- Las etiquetas siguen el protocolo offline por participante documentado previamente.
- Dataset, etiquetas y resultados históricos permanecen intactos.
- No se seleccionaron variantes por su desempeño en prueba ni se reentrenó con prueba.

## Resultados principales en prueba

| Objetivo | Modelo | Balanced accuracy | Macro F1 |
|---|---|---:|---:|
| Atención | Dummy | 0,3333 | 0,1667 |
| Atención | Logística | 0,3240 | 0,3238 |
| Atención | Random Forest | 0,3197 | 0,3191 |
| Activación 6 s | Dummy | 0,3333 | 0,1978 |
| Activación 6 s | Logística | 0,3169 | 0,3098 |
| Activación 6 s | Random Forest | 0,3365 | 0,3359 |

En regresión, Ridge obtuvo R² de −0,002526 para atención y 0,005101 para activación 6 s.
Los resultados reproducen la ejecución anterior dentro de tolerancia numérica y permanecen
cerca del baseline trivial. Ahora los estimadores ajustados están disponibles para reutilizar.

Algunos participantes no presentan todas las clases de activación; sklearn emite avisos al
calcular métricas por participante. La tabla anterior corresponde a métricas agregadas en prueba;
el CSV distingue esas métricas de las medias por participante.

## Verificación

- Diez pruebas aprobadas, incluyendo el flujo completo de 30 exportaciones con datos sintéticos.
- Predicciones y probabilidades idénticas después de recargar cada modelo sobre las entradas
  elegibles de validación, prueba y sensibilidad.
- SHA256 de los 30 artefactos, del script, del dataset y de la partición comprobados.
- Métricas contrastadas con la ejecución anterior con `rtol=1e-7`, `atol=1e-8`.
- Python 3.13.15, NumPy 2.5.2, pandas 3.0.5, scikit-learn 1.9.0 y joblib 1.5.3.

## Continuidad

Los baselines están listos para comparar con un primer modelo temporal manteniendo fija
la etiqueta y la partición. Los modelos temporales no forman parte de esta ejecución.

## Notas relacionadas

- [[Tesis_MDS]]
- [[ETIQUETAS_Y_BASELINES]]
- [[Avance - 22-08-2026 (Etiquetas Particion y Baselines)]]
- [[Resumen Diseño Etiquetas y Modelos]]
