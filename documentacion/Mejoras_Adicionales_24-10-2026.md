# Intentos adicionales de mejora — 24-10-2026

Después del contraste de temporalidad y fusión se ejecutaron tres seguimientos focalizados para clasificación de activación. Todos usan la pseudoetiqueta `arousal_label_6s` y solamente las 25 personas del train original. Validation, test y P29 siguen reservados. Estos seguimientos se diseñaron después de observar resultados anteriores, por lo que son **exploratorios**; no se comparan como una nueva competición confirmatoria.

## Resultados observados

| Intento | Referencia BA macro | Nueva BA macro | Diferencia (pp) | IC descriptivo 95 % (pp) | Recall de clase media |
|---|---:|---:|---:|---:|---:|
| Suavizado causal y sesgo de clase media elegidos en 4 folds internos de cada fold externo | TCN temprano 0,3612 | 0,3512 | -1,00 | [-2,24; +0,01] | 23,4 % → 26,4 % |
| Mezcla fija 75 % Ridge sin `fixation_count` + 25 % TCN temprano | Ridge 0,3843 | 0,3806 | -0,37 | [-1,66; +0,97] | 24,0 % → 22,4 % |
| Ridge sin las cuatro variables de fijación, con parámetros anteriores fijos | Ridge sin `fixation_count` 0,3843 | 0,3774 | -0,69 | [-1,45; +0,09] | 24,0 % → 20,3 % |

Ningún intento elevó la BA frente a su referencia correspondiente. El primer ajuste aumenta el recall medio a costa de las clases bajo y alto; su ganancia por clase no se debe presentar como mejora global. La mezcla mejora frente al TCN aislado (+1,94 pp), pero baja frente al Ridge que ya era más fuerte. Quitar toda la familia de fijaciones perjudica más que quitar solo `fixation_count`.

## Diseño y archivos

1. **Ajuste de decisión:** `scripts/ajustar_decision_tcn.py` entrenó 20 TCN internos: cuatro folds de calibración entre los 20 participantes de ajuste de cada fold externo. Probó suavizado causal 1/4/8 y multiplicador de probabilidad media 1/1,25/1,5/2. Seleccionó por BA media por persona, con desempate a favor de menor suavizado y sesgo. Las elecciones quedaron guardadas antes de aplicarse a las predicciones externas de los modelos originales. Resultados, intentos, selecciones y predicciones en `resultados/ajuste_decision_tcn_24-10-2026/`.
2. **Mezcla fija:** `scripts/mezcla_ridge_tcn_24_10_2026.py` alineó por fila y participante las predicciones OOF auditadas de `resultados/ablacion_pca_12-09-2026/` y `resultados/contraste_temporalidad_fusion_24-10-2026/`. El peso 75/25 quedó escrito en `protocolo.json` antes de calcular la mezcla. Se comprobaron hashes, etiquetas, cobertura y probabilidades válidas. Salida: `resultados/mezcla_ridge_tcn_24-10-2026/`.
3. **Ablación agrupada:** `scripts/ablacion_fijaciones_24_10_2026.py` reajustó cinco Ridge con la representación, alpha y suavizado previamente seleccionados para cada fold, quitando `fixation_count`, `fixation_total_ms`, `fixation_mean_ms` y `fixation_median_ms` junto con sus derivados. Se predijo con un frame sin etiqueta ni columnas GSR y se recargaron los cinco modelos. Salida: `resultados/ablacion_fijaciones_24-10-2026/`.

Las diferencias y sus intervalos son de 2.000 remuestreos pareados de 25 personas, promediando semillas antes del cálculo cuando corresponde. No hay corrección por los intentos anteriores ni por elección adaptativa de estas líneas. Las fuentes `protocolo.json`, `resumen.json`, predicciones y modelos permiten revisar cada cifra. La suite del proyecto pasó **71 pruebas**, incluidas dos nuevas sobre causalidad del suavizado y el ajuste de probabilidad.

## Lectura y siguiente decisión

El máximo exploratorio previo, Ridge sin `fixation_count` con BA macro 0,3843, permanece como mejor resultado observado en estas comparaciones. No se obtuvo evidencia nueva para afirmar que una red temporal lo supera o que eliminar todas las fijaciones ayuda. Una búsqueda adicional en las mismas 25 personas, guiada por estos resultados, aumentaría el riesgo de elegir una fluctuación propia de esta muestra. Para afirmar una mejora real hace falta acordar una evaluación independiente y revisar con el profesor el significado y la validez de las pseudoetiquetas; esta ronda no modifica esas decisiones científicas.

Ver [Contraste_Temporalidad_Fusion_24-10-2026.md](Contraste_Temporalidad_Fusion_24-10-2026.md) y [Ablacion_PCA_12-09-2026.md](Ablacion_PCA_12-09-2026.md).
