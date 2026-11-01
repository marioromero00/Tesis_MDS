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

## 01-11-2026 — Primer contraste fijo de activación V2 y respaldo Git

15 regresiones logísticas C=1, cinco folds y contextos 1/8/32; 7.028 filas de train con etiquetas V2 idénticas entre modelos. AUC macro persona 0,526132 / 0,518344 / 0,513917. Diferencias frente a ventana actual −0,007788 y −0,012215, con intervalos descriptivos que incluyen cero. No hay mejora temporal clara en esta comparación. No se evaluaron validation/test. Auditoría de recarga y verificación de 75 AUC desde disco aprobadas; cuatro pruebas de calidad de etiquetas aprobadas.

Informe: ../repos/Tesis_MDS/resultados/activacion_v2_historial_01-11-2026/INFORME.md. Script: experimento_activacion_v2.py. La representación temporal agrega media y desviación: no evalúa modelos sensibles al orden. No comparar directamente esta AUC con etiquetas anteriores.

Mario pidió guardar y subir cada etapa a Git. Se incorporaron los avances pendientes y copia verificable de documentos/notas al commit 6c02bb3. El envío a GitHub falló por resolución DNS (`Could not resolve host: github.com`); el respaldo remoto queda pendiente. Datos crudos externos, entornos, cachés y logs externos no están incluidos en esta copia Git.

## 01-11-2026 — Aprobación de etiquetas V2 y protocolo final

Mario comunica que su profesor aprobó usar las etiquetas V2 y solicita completar la comparación no lineal con/sin historial. Se fijó HistGradientBoosting, contextos 1/8/32 y dos candidatos de máximo de hojas (7/15), con los cinco folds heredados. Configuración compartida elegida por promedio de AUC internas entre contextos; ajuste final elegido solo desde las puntuaciones internas de train. Contraste principal 32−1 y secundario 8−1. Modelos se congelan antes de consultar validation/test; una corrida acotada sin ampliación posterior por rendimiento.

Protocolo: ../repos/Tesis_MDS/resultados/activacion_v2_comparacion_final_01-11-2026/protocolo.json. La aprobación de uso no implica validación psicológica externa ni elimina la exposición histórica de las particiones. El estudio de ablación de modalidades queda fuera de esta solicitud (punto 2).

## 01-11-2026 — Comparación final no lineal V2 completada

30 ajustes internos HistGradientBoosting; 15 modelos OOF y tres finales. La selección interna fijó 15 hojas compartidas entre contextos. Modelos finales guardados y comprometidos en Git antes de evaluar validation/test. Test AUC contextos 1/8/32: 0,514087 / 0,546964 / 0,536320. Contraste principal 32−1: +0,022233, IC [−0,013004; +0,058518], inconcluso. Secundario 8−1: +0,032878, IC [+0,007625; +0,059155], 7/8 mejoran; validation y OOF no confirman esa mejora. No seleccionar contexto usando test. No hay evidencia consistente de superioridad temporal general; intervalos de AUC absoluta incluyen 0,50.

Se evaluaron 7.028 ventanas train, 2.584 validation y 2.184 test, con idénticas etiquetas/filas por contexto. Auditoría desde disco: 30 scores internos, 123 AUC por persona y 21 recargas predictivas aprobadas. Informe: ../repos/Tesis_MDS/resultados/activacion_v2_comparacion_final_01-11-2026/INFORME.md. Regla de parada cumplida, sin nueva búsqueda. Subida a GitHub continúa pendiente por fallo DNS; commits locales conservados.

Limitación de cobertura de la corrida final: ninguna ventana validation/test dispone de 32 ventanas consecutivas retenidas; ctx32 en test tiene longitud media por persona de 8,75. Contexto es máximo disponible, no longitud completa garantizada. Registrado en el informe.
