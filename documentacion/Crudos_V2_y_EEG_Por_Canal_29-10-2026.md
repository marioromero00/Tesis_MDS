# Crudos V2 y nuevo experimento espacial EEG — 29-10-2026

Carpeta confirmada: https://drive.google.com/drive/folders/1REsfSQWiiPp7BKubdHa2A7VNeBjlELAD

## Insumos

- EEG: `eeg_recordings_exp_V2.zip`, Drive ID `1SOui6TmWXjhdHbZbzJg3K26GJhiP341z`, 1.666.099.115 bytes; SHA-256 esperado `152ceddb9bb06a05b0701d276e867729836518448cf597ab3c6f74b39d933e79`.
- Tobii: `Toma_muestras_v2 Data export.tsv`, Drive ID `1yQnHiCpa25Wo7F94Z9X0Vew_c5EqBv4t`, 1.470.821.789 bytes; SHA-256 esperado `0e7f2461495ded0c260f5474266bb526897643763bf1fca4b9cc3796ab8c2203`.

Ambos tamaños y hashes proceden del manifiesto histórico de preprocesamiento. La inspección remota parcial del directorio ZIP encontró 270 miembros, con los 49 archivos del manifiesto presentes; la cabecera Tobii identifica P1, 08/08/2025 16:22:37.297 UTC, SlowWeb G1. La inspección parcial no sustituye al hash completo ni al CRC del ZIP.

Los crudos quedan en `../../datos/locales/v2_2025/`, fuera del repositorio Git. La descarga pública desde Google Drive mostró velocidades bajas, por lo que se deja un flujo local reanudable. Estado en `ESTADO.md` y `estado_pipeline.json` dentro de esa carpeta. Si se copia allí una versión completa desde el Air o disco, el verificador reconoce los hashes y detiene únicamente las descargas redundantes que identifica como propias.

## Flujo automático

`pipeline_crudos_v2.py` vigila las descargas actuales, reintenta interrupciones de forma acotada, verifica tamaños/SHA-256, todos los miembros del manifiesto, CRC de ZIP y columnas Tobii. Solo después ejecuta:

1. `eeg_por_canal_v2.py`: nuevas características sobre las 13.524 ventanas de los 25 participantes de train.
2. `modelar_eeg_por_canal_v2.py --round 1`: grid por participante con las etiquetas binarias PCA congeladas.
3. `auditar_modelos_eeg_por_canal_v2.py --round 1`: recarga, grupos disjuntos, etiquetas originales y AUC recalculada.

El proceso conserva hashes del código y versiones del entorno al iniciarse. Si cambian antes de procesar, se detiene con estado `requiere_revision`. Mantiene el mini disponible mediante una inhibición temporal de reposo ligada al proceso; no cambia preferencias permanentes. No publica resultados ni modifica Drive.

## Variables nuevas y controles

Las representaciones anteriores agregaban EEG entre canales. La nueva extracción conserva los 16 canales por separado: potencias absolutas logarítmicas y relativas de cinco bandas, entropía y centro/borde espectral, Hjorth, amplitud y controles de calidad. Se agregan correlación entre canales, dominancia de covarianza y número de canales utilizables: 342 entradas EEG nuevas, más el panel EEG/GSR original.

Mismas ventanas UTC de 2 s, sin añadir offsets del inicio de grabación. En todas las ventanas se verifica el número de muestras contra el CSV original, y en diez ventanas por persona se reproduce el EEG agregado anterior para comprobar la selección temporal. No se asigna anatomía a los canales sin mapa de electrodos.

Dentro de cada ventana: detrend lineal, notch 50 Hz/Q30 y bandpass Butterworth orden 4, 1–45 Hz, forward-backward limitado a la ventana actual. PSD Welch: fs125 Hz, nperseg125, noverlap62, nfft256. Se calcula potencia por suma de densidad × paso de frecuencia. Referencias de implementación: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html y https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.sosfiltfilt.html.

Un canal se marca ausente si tiene menos de 95 % de valores finitos, más de 1 % en rail (|x|≥180.000 µV), al menos 99 % de diferencias exactamente planas, menos de 200 muestras o huecos mayores de 0,1 s. Estas reglas se fijaron antes de observar el resultado de los modelos. No se eliminan ventanas ni participantes para subir AUC: los canales inválidos generan features ausentes, imputadas únicamente con train de cada fold.

## Comparación predefinida

Logística C0,1/1, HistGradientBoosting hojas7/15 y CatBoost profundidad4/6. Contextos actual/8/32 ventanas; con/sin normalización personal offline. Total: 36 configuraciones por fold, 180 ajustes internos y diez modelos externos seleccionados (más estrategia que elige escenario internamente).

El historial agrega medias del panel anterior y de potencias relativas por canal, y desviación del panel anterior, manteniendo acotada la dimensionalidad. La normalización personal offline se reporta aparte porque usa la sesión completa no etiquetada. Mirada, pupila, scores y etiquetas no se incluyen como predictores. Los profesores PCA se reconstruyen con personas de ajuste en cada nivel, conservando exactamente las etiquetas externas del estudio previo.

Meta: ROC-AUC macro por persona >0,70 en las 25 personas OOF, con etiquetas y folds fijos. Los resultados continúan siendo exploratorios por reutilización de train. Validation, test y P29 no se evalúan. La meta solo se declara alcanzada después de auditoría; no se garantiza que las nuevas variables permitan superarla.

## Pruebas previas

Cuatro tests de señales sintéticas verifican bandas por canal, suma de potencias relativas, saturación y huecos. Tres tests del modelado verifican causalidad del historial, exclusión de inputs docentes y grid completo. La verificación contra los registros reales queda pendiente de la descarga íntegra y se ejecuta automáticamente antes del modelado.
