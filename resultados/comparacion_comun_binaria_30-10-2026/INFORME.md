# Comparación común: atención, activación y ablaciones

Análisis exploratorio binario. Activación se define antes de entrenar como score GSR de 6 s superior a la mediana personal; es una nueva tarea, no una reevaluación de la clasificación ternaria. Atención conserva el profesor PCA congelado. Mismos participantes, ventanas válidas dentro de cada tarea, parámetros y AUC por persona. Contextos 1/32: hasta 2/33 segundos. La representación temporal usa medias y desviaciones de todas las variables: no es idéntica al experimento anterior de atención. No se seleccionan modelos con test.

## Resultados test

| Tarea | Modalidades | Contexto | AUC | IC 95 % |
|---|---|---:|---:|---:|
| activacion | EEG | 1 | 0.5375 | [0.4780; 0.5966] |
| activacion | EEG | 32 | 0.4713 | [0.3709; 0.5697] |
| activacion | Eye | 1 | 0.5172 | [0.4788; 0.5520] |
| activacion | Eye | 32 | 0.4976 | [0.4675; 0.5298] |
| activacion | Pupil | 1 | 0.4724 | [0.4202; 0.5256] |
| activacion | Pupil | 32 | 0.4632 | [0.3664; 0.5492] |
| activacion | full | 1 | 0.5501 | [0.4998; 0.6044] |
| activacion | full | 32 | 0.4707 | [0.3877; 0.5546] |
| activacion | sin_EEG | 1 | 0.4865 | [0.4269; 0.5355] |
| activacion | sin_EEG | 32 | 0.4804 | [0.4260; 0.5314] |
| activacion | sin_Eye | 1 | 0.5372 | [0.4918; 0.5887] |
| activacion | sin_Eye | 32 | 0.4729 | [0.3877; 0.5602] |
| activacion | sin_Pupil | 1 | 0.5439 | [0.4911; 0.6013] |
| activacion | sin_Pupil | 32 | 0.4965 | [0.4080; 0.5853] |
| atencion | EEG | 1 | 0.6644 | [0.6234; 0.7004] |
| atencion | EEG | 32 | 0.6963 | [0.6496; 0.7381] |
| atencion | GSR | 1 | 0.5457 | [0.4987; 0.5944] |
| atencion | GSR | 32 | 0.6084 | [0.5797; 0.6352] |
| atencion | full | 1 | 0.6602 | [0.6139; 0.7043] |
| atencion | full | 32 | 0.6927 | [0.6478; 0.7358] |

## Contrastes test

| Tarea | Contraste | ΔAUC | IC 95 % |
|---|---|---:|---:|
| activacion | temporal_EEG | -0.0662 | [-0.1532; 0.0120] |
| activacion | full_menos_EEG_ctx1 | +0.0126 | [-0.0229; 0.0474] |
| activacion | full_menos_EEG_ctx32 | -0.0006 | [-0.0239; 0.0265] |
| activacion | temporal_Eye | -0.0196 | [-0.0445; 0.0049] |
| activacion | full_menos_Eye_ctx1 | +0.0329 | [0.0064; 0.0646] |
| activacion | full_menos_Eye_ctx32 | -0.0269 | [-0.0997; 0.0509] |
| activacion | temporal_Pupil | -0.0092 | [-0.0739; 0.0499] |
| activacion | full_menos_Pupil_ctx1 | +0.0776 | [0.0055; 0.1445] |
| activacion | full_menos_Pupil_ctx32 | +0.0075 | [-0.0974; 0.1118] |
| activacion | temporal_full | -0.0794 | [-0.1287; -0.0304] |
| activacion | temporal_sin_EEG | -0.0062 | [-0.0478; 0.0271] |
| activacion | full_menos_sin_EEG_ctx1 | +0.0635 | [0.0277; 0.1005] |
| activacion | full_menos_sin_EEG_ctx32 | -0.0096 | [-0.0702; 0.0631] |
| activacion | temporal_sin_Eye | -0.0643 | [-0.1106; -0.0183] |
| activacion | full_menos_sin_Eye_ctx1 | +0.0129 | [-0.0119; 0.0339] |
| activacion | full_menos_sin_Eye_ctx32 | -0.0022 | [-0.0197; 0.0160] |
| activacion | temporal_sin_Pupil | -0.0474 | [-0.0990; -0.0001] |
| activacion | full_menos_sin_Pupil_ctx1 | +0.0062 | [-0.0113; 0.0247] |
| activacion | full_menos_sin_Pupil_ctx32 | -0.0257 | [-0.0676; 0.0103] |
| atencion | temporal_EEG | +0.0319 | [0.0037; 0.0562] |
| atencion | full_menos_EEG_ctx1 | -0.0042 | [-0.0171; 0.0075] |
| atencion | full_menos_EEG_ctx32 | -0.0036 | [-0.0180; 0.0097] |
| atencion | temporal_GSR | +0.0627 | [-0.0070; 0.1235] |
| atencion | full_menos_GSR_ctx1 | +0.1145 | [0.0603; 0.1654] |
| atencion | full_menos_GSR_ctx32 | +0.0843 | [0.0499; 0.1204] |
| atencion | temporal_full | +0.0325 | [0.0059; 0.0591] |

Intervalos descriptivos bootstrap de participantes, 20.000 muestras; no corrigen comparaciones múltiples ni selección histórica. Test/validation fueron consultados anteriormente. Un intervalo que incluye cero no demuestra ausencia de efecto. La comparación es sobre pseudoetiquetas offline, no medición psicológica independiente. Las ablaciones miden contribución de modalidades en fusión temprana; no comparan fusión intermedia/tardía.

## Conclusión conjunta

Con esta representación común, atención mejora de 0,6602 a 0,6927 (ΔAUC +0,0325; IC descriptivo [0,0059; 0,0591]); activación disminuye de 0,5501 a 0,4707 (ΔAUC −0,0794; IC [−0,1287; −0,0304]). Hay evidencia exploratoria favorable para atención y contraria para activación bajo estas configuraciones. La hipótesis de superioridad temporal en ambos resultados no recibe apoyo conjunto. Esto no descarta todas las arquitecturas temporales posibles.

En atención, EEG temporal solo obtiene 0,6963 frente a 0,6927 con EEG+GSR; Δ de añadir GSR −0,0036, IC [−0,0180; 0,0097]. La fusión no muestra ventaja sobre EEG solo. En activación estática, la fusión completa obtiene 0,5501 frente a EEG solo 0,5375; la diferencia +0,0126 incluye cero. Por tanto tampoco se demuestra superioridad sobre la mejor modalidad individual observada. No se selecciona una modalidad ganadora para un nuevo ajuste usando estos resultados.

Se verificaron los hashes de los 20 modelos y se recalcularon las 320 AUC por persona desde las predicciones guardadas. Dentro de cada tarea y partición todas las ablaciones conservan idénticas filas y etiquetas. Validation y test se reportan por separado. Esta auditoría comprueba ejecución y métricas; no elimina la exposición histórica de las particiones ni valida las pseudoetiquetas como medición psicológica.
