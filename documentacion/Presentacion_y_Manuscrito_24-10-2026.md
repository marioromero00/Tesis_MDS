# Presentación simplificada y avance del manuscrito — 24-10-2026

## Entregables

- `presentaciones/Avances-Experimentales-Simplificados-24-10-2026.pptx`: ocho diapositivas editables y autocontenidas. Explican el objetivo, el diseño profesor/estudiante, la partición y la BA macro por persona, los contrastes de temporalidad y fusión, la referencia Ridge, el control negativo, la sensibilidad a la etiqueta y el alcance de las conclusiones.
- `presentaciones/Avances-Experimentales-Simplificados-24-10-2026.pdf`: versión para compartir o proyectar.
- `../01 Tesis MDS/Escritura/Estructura Tesis.md`: borrador del manuscrito en el vault, con metodología ampliada y capítulos de experimentos, resultados y discusión.

La presentación resume resultados de `Contraste_Temporalidad_Fusion_24-10-2026.md`, `Evaluacion_Independiente_y_Validez_24-10-2026.md`, `Robustez_Sin_Cohorte_Nueva_24-10-2026.md` y `Control_Negativo_Temporal_y_Errores_24-10-2026.md`. Las definiciones y cautelas necesarias para interpretar las cifras están visibles; las notas agregan contexto para la exposición oral.

## Avance de redacción

En el capítulo 4 se documentaron participantes y partición, construcción de pseudoetiquetas, sincronización, preprocesamiento EEG/GSR/mirada/pupila, extracción de variables, evaluación por participante y control negativo. Se corrigió una descripción EEG de un diseño previo: el pipeline usado calculó nueve variables agregadas con FFT, sin notch, Welch ni 273 variables por época. En los capítulos 6–8 se redactaron los experimentos recientes, sus cifras y una discusión de alcance. Permanecen apartados anteriores marcados como pendientes y las decisiones científicas abiertas del diseño de etiquetas.

El modelado de activación usó filas con etiqueta no nula; no filtró adicionalmente todas las ventanas por `eligible_arousal`. Se declara en el manuscrito para que el criterio de inclusión sea reproducible. El conjunto de test ya se había consultado antes; sus cifras son evaluación adicional y no confirmación independiente.

## Verificación

El generador `scripts/crear_avances_simplificados_24_10_2026.py` comprobó ocho diapositivas y ausencia de objetos fuera de la página. `scripts/verificar_avances_simplificados_24_10_2026.ps1` renderizó las ocho diapositivas con PowerPoint y no encontró desbordamiento de texto con tolerancia de 3 pt. El PDF contiene ocho páginas. Se revisaron visualmente las láminas de evaluación, contraste y conclusión. Auditorías: `documentacion/Verificacion_Avances_Simplificados_24-10-2026.json` y `resultados/presentacion_avances_simplificados_24-10-2026/renderizado.json`.
