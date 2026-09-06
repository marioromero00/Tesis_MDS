# Tesis MDS — Baselines multimodales

Estado al 06-09-2026. Esta entrada reemplaza la descripción anterior del repositorio.

Detección temporal multimodal de atención y activación durante navegación web, con EEG,
GSR, eye tracking y pupilometría. Los baselines estáticos están entrenados y guardados;
la comparación temporal es el siguiente paso.

## Entrega actual

- [Presentación HTML, 16 diapositivas](presentaciones/avance-eda-sincronizacion-15-08-2026.html).
- [30 modelos entrenados](resultados/modelado/ejecuciones/baselines_05-09-2026_02/modelos/).
- [Métricas](resultados/modelado/ejecuciones/baselines_05-09-2026_02/metricas_baselines.csv).
- [Guía de carga](resultados/modelado/ejecuciones/baselines_05-09-2026_02/COMO_CARGAR.txt).
- [Manifiesto de entrenamiento](resultados/modelado/ejecuciones/baselines_05-09-2026_02/manifiesto_baselines.json).
- [Verificación de entrega](resultados/modelado/ejecuciones/baselines_05-09-2026_02/verificacion_entrega.json).
- [Respaldo completo de la sección de tesis del vault](documentacion/Tesis_Vault_06-09-2026.zip).
- [Inventario y hashes del respaldo](documentacion/inventario_vault_06-09-2026.json).
- [Auditoría de la presentación](documentacion/auditoria_presentacion_06-09-2026.json).

Para visualizar el HTML, descargar o clonar el repositorio y abrir el archivo local.
Las imágenes están en `attachments/Analisis de Datos/`; conservar esa estructura.
GitHub muestra el código del HTML, no una presentación alojada.

## Reproducción

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/baselines_estaticos.py --run-dir resultados/modelado/ejecuciones/NOMBRE_NUEVO
```

El entrenamiento utiliza `resultados/modelado/dataset_modelado.csv` y comprueba la
partición congelada por participante. El directorio de ejecución debe ser nuevo.
Solo entrenamiento ajusta imputadores, escaladores y estimadores; validación, prueba
y P29 se evalúan por separado. El protocolo de etiquetas es offline por participante.

## Modelos y resultados

Cinco objetivos: atención principal, activación principal de 6 s, atención PCA,
activación de 2 s y activación PCA. Cada objetivo incluye Dummy, Ridge y Random Forest
para regresión, y Dummy, logística y Random Forest para clasificación.

La clasificación principal en prueba obtiene balanced accuracy de 0,3240/0,3197
para atención (logística/Random Forest), y 0,3169/0,3365 para activación de 6 s.
La referencia Dummy es 0,3333. Los resultados estáticos permanecen cerca de esa referencia.
Diez pruebas aprobadas; los 30 pipelines producen las mismas predicciones tras recargarse.

## Documentación del vault

Las notas Markdown de trabajo se mantienen en la sección `01 Tesis MDS` del vault.
El ZIP conserva su estructura completa, notas, presentaciones y adjuntos. Reemplaza como
snapshot documental a las copias antiguas que fueron retiradas del árbol de trabajo durante
la consolidación del vault. El archivo no incluye Vinson, inglés ni configuración personal.
El inventario registra SHA256 y tamaño de cada archivo para verificar la copia.

Los modelos y predicciones de la ejecución final se versionan por solicitud expresa del
06-09-2026. Datos crudos, credenciales, cachés e intentos incompletos permanecen excluidos.
