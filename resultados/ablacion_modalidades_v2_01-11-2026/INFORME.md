# Ablación controlada de modalidades — activación V2

HistGradientBoosting, mismos hiperparámetros por fold/contexto que la fusión completa, elegidos previamente solo en train. EEG, mirada y pupila por separado frente a fusión temprana completa. Modelos completos reutilizados sin cambios. 45 ajustes OOF y nueve modelos finales nuevos, congelados antes de evaluación externa.

| Evaluación | Modalidad | Contexto máximo | AUC | IC descriptivo 95% |
|---|---|---|---|---|
| oof_train | EEG | 1 | 0.5231 | [0.4926; 0.5531] |
| oof_train | EEG | 8 | 0.4938 | [0.4431; 0.5454] |
| oof_train | EEG | 32 | 0.5299 | [0.4828; 0.5806] |
| oof_train | Eye | 1 | 0.5118 | [0.4904; 0.5323] |
| oof_train | Eye | 8 | 0.5496 | [0.5166; 0.5806] |
| oof_train | Eye | 32 | 0.5294 | [0.4959; 0.5601] |
| oof_train | Pupil | 1 | 0.5122 | [0.4799; 0.5420] |
| oof_train | Pupil | 8 | 0.5089 | [0.4679; 0.5468] |
| oof_train | Pupil | 32 | 0.4880 | [0.4420; 0.5314] |
| oof_train | full | 1 | 0.5021 | [0.4581; 0.5439] |
| oof_train | full | 8 | 0.5001 | [0.4510; 0.5515] |
| oof_train | full | 32 | 0.5260 | [0.4697; 0.5847] |
| test | EEG | 1 | 0.4982 | [0.4357; 0.5586] |
| test | EEG | 8 | 0.5123 | [0.4365; 0.5856] |
| test | EEG | 32 | 0.5173 | [0.4473; 0.5790] |
| test | Eye | 1 | 0.5151 | [0.4922; 0.5391] |
| test | Eye | 8 | 0.5129 | [0.4576; 0.5708] |
| test | Eye | 32 | 0.5215 | [0.4405; 0.5999] |
| test | Pupil | 1 | 0.5172 | [0.4743; 0.5655] |
| test | Pupil | 8 | 0.5461 | [0.5040; 0.5856] |
| test | Pupil | 32 | 0.5386 | [0.4922; 0.5813] |
| test | full | 1 | 0.5141 | [0.4510; 0.5788] |
| test | full | 8 | 0.5470 | [0.4829; 0.6121] |
| test | full | 32 | 0.5363 | [0.4751; 0.5942] |
| validation | EEG | 1 | 0.5236 | [0.4636; 0.5974] |
| validation | EEG | 8 | 0.4996 | [0.4108; 0.6112] |
| validation | EEG | 32 | 0.5242 | [0.4592; 0.6195] |
| validation | Eye | 1 | 0.4799 | [0.4442; 0.5116] |
| validation | Eye | 8 | 0.4834 | [0.4238; 0.5452] |
| validation | Eye | 32 | 0.4807 | [0.4023; 0.5634] |
| validation | Pupil | 1 | 0.4957 | [0.4495; 0.5410] |
| validation | Pupil | 8 | 0.5053 | [0.4231; 0.5873] |
| validation | Pupil | 32 | 0.5022 | [0.4137; 0.5928] |
| validation | full | 1 | 0.5182 | [0.4548; 0.5855] |
| validation | full | 8 | 0.5209 | [0.4495; 0.5951] |
| validation | full | 32 | 0.5245 | [0.4639; 0.5965] |

## Contrastes de fusión

| Evaluación | Contexto | Fusión menos | ΔAUC | IC descriptivo 95% | Personas mejoran |
|---|---|---|---|---|---|
| oof_train | 1 | full_minus_EEG | -0.0210 | [-0.0522; 0.0078] | 12/25 |
| oof_train | 1 | full_minus_Eye | -0.0097 | [-0.0472; 0.0279] | 11/25 |
| oof_train | 1 | full_minus_Pupil | -0.0102 | [-0.0464; 0.0295] | 11/25 |
| oof_train | 8 | full_minus_EEG | +0.0064 | [-0.0330; 0.0438] | 15/25 |
| oof_train | 8 | full_minus_Eye | -0.0495 | [-0.1082; 0.0140] | 7/25 |
| oof_train | 8 | full_minus_Pupil | -0.0087 | [-0.0569; 0.0407] | 10/25 |
| oof_train | 32 | full_minus_EEG | -0.0040 | [-0.0432; 0.0325] | 12/25 |
| oof_train | 32 | full_minus_Eye | -0.0035 | [-0.0673; 0.0700] | 11/25 |
| oof_train | 32 | full_minus_Pupil | +0.0380 | [-0.0237; 0.1036] | 16/25 |
| test | 1 | full_minus_EEG | +0.0159 | [-0.0293; 0.0647] | 3/8 |
| test | 1 | full_minus_Eye | -0.0010 | [-0.0627; 0.0569] | 4/8 |
| test | 1 | full_minus_Pupil | -0.0032 | [-0.0536; 0.0419] | 5/8 |
| test | 8 | full_minus_EEG | +0.0347 | [-0.0157; 0.0891] | 4/8 |
| test | 8 | full_minus_Eye | +0.0341 | [-0.0690; 0.1294] | 5/8 |
| test | 8 | full_minus_Pupil | +0.0008 | [-0.0824; 0.0772] | 5/8 |
| test | 32 | full_minus_EEG | +0.0190 | [-0.0185; 0.0535] | 5/8 |
| test | 32 | full_minus_Eye | +0.0149 | [-0.1129; 0.1360] | 5/8 |
| test | 32 | full_minus_Pupil | -0.0022 | [-0.0916; 0.0811] | 5/8 |
| validation | 1 | full_minus_EEG | -0.0054 | [-0.0351; 0.0292] | 3/8 |
| validation | 1 | full_minus_Eye | +0.0382 | [-0.0108; 0.0839] | 5/8 |
| validation | 1 | full_minus_Pupil | +0.0224 | [-0.0308; 0.0720] | 5/8 |
| validation | 8 | full_minus_EEG | +0.0213 | [-0.0287; 0.0646] | 6/8 |
| validation | 8 | full_minus_Eye | +0.0375 | [-0.0059; 0.0831] | 6/8 |
| validation | 8 | full_minus_Pupil | +0.0156 | [-0.0472; 0.0854] | 5/8 |
| validation | 32 | full_minus_EEG | +0.0003 | [-0.0375; 0.0426] | 3/8 |
| validation | 32 | full_minus_Eye | +0.0438 | [0.0095; 0.0835] | 7/8 |
| validation | 32 | full_minus_Pupil | +0.0223 | [-0.0251; 0.0675] | 6/8 |

## Límites
Resultados exploratorios sobre particiones consultadas históricamente. Todos los nueve contrastes por partición se reportan; intervalos descriptivos sin corrección múltiple. No se escoge modalidad ni contexto para reajustar usando test. Esta es una ablación con configuración controlada, no una búsqueda del máximo alcanzable por cada modalidad. Solo evalúa fusión temprana, no tardía/intermedia ni todas las parejas.

Mismas filas y etiquetas V2: 7.028 train, 2.584 validation y 2.184 test. Las ausencias de predictores se imputan desde train; no se eliminan filas por modalidad. Pseudoetiquetas GSR offline no equivalen a activación psicológica validada. Contexto32 es un límite máximo: no hay 32 ventanas consecutivas retenidas en validation/test. Consultar ../activacion_v2_comparacion_final_01-11-2026/INFORME.md para interpretación temporal y cobertura.

## Conclusión de la ablación

No se demuestra una ventaja de la fusión temprana completa sobre las modalidades individuales en test: los nueve intervalos pareados incluyen cero. En el contexto8, fusión obtiene AUC 0,5470 frente a pupila 0,5461: diferencia +0,0008, IC descriptivo [−0,0824; +0,0772]. Esa proximidad no prueba equivalencia; la incertidumbre permite diferencias en ambas direcciones. Con contexto32, pupila obtiene 0,5386 frente a fusión 0,5363, también sin diferencia concluyente.

La única diferencia de fusión cuyo intervalo no incluye cero entre los 27 contrastes reportados es contexto32 frente a mirada en validation: +0,0438 [0,0095; 0,0835]. No se reproduce en test y no supera todas las modalidades; no demuestra superioridad general de la fusión. Todos los contrastes OOF train y test incluyen cero.

Pupila con contexto8 tiene AUC test 0,5461 [0,5040; 0,5856], mientras que su validation es 0,5053 [0,4231; 0,5873]. Se reporta como resultado exploratorio, sin elegir retrospectivamente este modelo como ganador para un nuevo ajuste. En OOF train, mirada contexto8 obtiene 0,5496 [0,5166; 0,5806], pero su validation/test no mantienen esa magnitud. El patrón cambia entre particiones y no establece un ganador robusto.

La configuración fue elegida para el modelo completo dentro de train y mantenida para las ablaciones. Esto responde al aporte de retirar modalidades bajo una configuración controlada; no establece el máximo rendimiento posible de cada modalidad con búsquedas específicas.

Auditoría aprobada: 54 modelos nuevos, 63 comprobaciones de predicción tras recarga, 492 AUC individuales y 27 intervalos/contrastes recalculados desde disco; mismas filas/etiquetas y fuentes originales intactas. La corrida queda cerrada, sin búsqueda adicional a partir de sus resultados.
