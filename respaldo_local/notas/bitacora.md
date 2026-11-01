# Bitácora de tesis

Registrar fecha, avances, decisiones y próximos pasos en cada sesión.

## 29-10-2026 — Evaluación EEG por canal con temporalidad

Completada selección de 36 candidatos en cinco folds (180 ajustes) y evaluación de seis modelos en ocho personas de validation. Principal congelado: HistBoost, contexto32, AUC 0,694068; offline secundario: CatBoost profundidad4, contexto32, AUC 0,703861. Temporalidad inductiva +0,014318 frente a contexto1, intervalo pareado incluye cero. Validación previamente consultada; test/P29 no evaluados. Auditoría independiente aprobada.

Resultados: ../repos/Tesis_MDS/resultados/temporalidad_eeg_v2_validacion_29-10-2026/INFORME.md. Scripts: evaluar_temporalidad_eeg_v2.py, auditar_temporalidad_eeg_v2.py, graficar_temporalidad_eeg_v2.py. La comparación ya concluyó; no relanzar buscando elevar el resultado en validation. Modelos, profesor, protocolo previo y predicciones quedan guardados.

## 29-10-2026 — Test temporalidad y contraste de hipótesis

Por solicitud explícita se evaluaron ocho personas de test (4.024 ventanas etiquetadas). Se conservaron los seis modelos congelados y se añadieron dos controles estáticos con familia/parámetros emparejados, ajustados solo en train antes de consultar test. Inductivo ctx32 AUC 0,687901 vs estático pareado 0,660179: Δ0,027722, IC descriptivo [-0,004095; 0,050523], mejora en 7/8. Offline ctx32 AUC 0,691865. Todos los intervalos de contrastes temporales incluyen cero. Conclusión: indicios favorables, evidencia inconclusa; no confirmar ni rechazar definitivamente la hipótesis. Esta corrida solo analiza atención, no activación/fusión. Test ya expuesto históricamente. Auditoría independiente aprobada. No reajustar modelos a partir de test.

Informe: ../repos/Tesis_MDS/resultados/temporalidad_eeg_v2_test_29-10-2026/INFORME.md. Scripts: evaluar_test_temporalidad_eeg_v2.py, auditar_test_temporalidad_eeg_v2.py, graficar_test_temporalidad_eeg_v2.py.

## Comparación común binaria completada
20 modelos nuevos: atención y activación, contextos 1/32, ablaciones unimodales y leave-one-modality-out. Resultados en ../repos/Tesis_MDS/resultados/comparacion_comun_binaria_30-10-2026/INFORME.md. Atención temporal mejora; activación temporal empeora; fusión no supera claramente a EEG individual. Parámetros fijos, etiquetas activación binaria nuevas, todas las evaluaciones exploratorias.

## 30-10-2026 — Diagnóstico y búsqueda propia de activación completados

60 ajustes internos, 15 modelos externos, folds congelados y etiquetas binarias idénticas. AUC OOF: actual 0,536599, ctx8 0,534243, ctx32 0,540102. Diferencias temporales inconclusas. Hallazgos críticos: P4 GSR válido12,6 % con todas sus ventanas etiquetadas; P34 positivos8,6 % por empates; contexto32 completo0,95 %. No se evaluaron validation/test. Auditorías aprobadas. Informe en ../repos/Tesis_MDS/resultados/activacion_diagnostico_nested_30-10-2026/INFORME.md y diagnóstico separado. Priorizar protocolo de calidad docente antes de nuevos ajustes.

## 01-11-2026 — Reintento completo de activación
Por solicitud del usuario se reentrenaron 60 ajustes internos y 15 modelos externos en carpeta nueva. Predicciones OOF, métricas, contrastes, selecciones y diagnóstico coinciden con la corrida original con tolerancia1e-10. AUC contextos1/8/32:0,536599/0,534243/0,540102. No se modificaron etiquetas ni se evaluaron validation/test. Evidencia: ../repos/Tesis_MDS/resultados/activacion_diagnostico_nested_reintento_01-11-2026/reproduccion.json.

## 01-11-2026 — Organización de carpetas en el Mac

Vault recuperado movido a `../documentos/01 Tesis MDS`, con enlace de compatibilidad en `../repos/01 Tesis MDS`. Índices y pautas actualizados. Se verificaron los hashes de los 80 archivos y el estado Git sin cambios. Código, datos y experimentos conservan sus ubicaciones. Recuperar la redacción posterior no es una prioridad actual para Mario. Detalle: `organizacion-carpetas-01-11-2026.json`.
