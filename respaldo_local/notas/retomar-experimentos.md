# Retomar experimentos en Mac mini — 29-10-2026

## Punto de partida verificado

Repositorio: ../repos/Tesis_MDS
Commit revisado: 8ace73d (24-10-2026).
Dataset procesado disponible: resultados/modelado/dataset_modelado.csv (aprox. 15 MB).
Python del sistema: 3.9.6. Se requiere preparar y verificar un entorno local compatible con las dependencias fijadas. requirements_temporales.txt fija torch==2.14.0+cpu con índice CPU; revisar la distribución compatible con macOS antes de instalar. Conservar los requirements originales y documentar cualquier adaptación local.

## Estado científico documentado

- Mejor BA macro por persona exploratoria para activación: 0,3843, Ridge sin fixation_count.
- Evaluación en ocho personas de test previamente consultadas: BA 0,3557; no constituye confirmación independiente nueva.
- Control negativo temporal: media 0,3268 para 12 desplazamientos, frente a 0,3843 original. No valida por sí solo el constructo psicológico.
- Los tres intentos adicionales del 24 de octubre no superaron la referencia Ridge.

Fuentes: README.md y documentacion/Mejoras_Adicionales_24-10-2026.md, Control_Negativo_Temporal_y_Errores_24-10-2026.md, Evaluacion_Independiente_y_Validez_24-10-2026.md.

## Secuencia para retomar

1. Elegir si se reproduce una corrida existente, se retoma una pendiente o se diseña un experimento nuevo.
2. Crear un entorno aislado para Apple Silicon y registrar versiones efectivamente instaladas.
3. Ejecutar la suite pertinente y una reproducción pequeña de referencia antes de entrenamientos largos.
4. Guardar nuevas salidas en directorios nuevos; conservar modelos y resultados anteriores.
5. Mantener la partición congelada por participante y registrar el protocolo antes de la corrida. No usar test para seleccionar modelos.

No se inició entrenamiento ni se modificaron archivos del repositorio durante esta revisión.
