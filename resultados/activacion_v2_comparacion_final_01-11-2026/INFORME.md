# Activación V2: comparación final acotada

Etiquetas V2 aprobadas por el profesor según comunicación de Mario. HistGradientBoosting, dos candidatos (7/15 hojas), 30 ajustes internos, 15 modelos externos OOF y tres modelos finales. Configuración común a los contextos seleccionada solo con AUC interna de train. Comparación principal: 32 menos 1; secundaria: 8 menos 1. Modelos finales congelados antes de evaluar validation/test.

| Evaluación | Contexto | AUC macro persona | IC descriptivo 95% |
|---|---|---|---|
| oof_train | 1 | 0.5021 | [0.4581; 0.5439] |
| oof_train | 8 | 0.5001 | [0.4510; 0.5515] |
| oof_train | 32 | 0.5260 | [0.4697; 0.5847] |
| test | 1 | 0.5141 | [0.4510; 0.5788] |
| test | 8 | 0.5470 | [0.4829; 0.6121] |
| test | 32 | 0.5363 | [0.4751; 0.5942] |
| validation | 1 | 0.5182 | [0.4548; 0.5855] |
| validation | 8 | 0.5209 | [0.4495; 0.5951] |
| validation | 32 | 0.5245 | [0.4639; 0.5965] |

| Evaluación | Historial menos actual | ΔAUC | IC descriptivo 95% | Personas mejoran |
|---|---|---|---|---|
| oof_train | 8 | -0.0019 | [-0.0495; 0.0491] | 14/25 |
| oof_train | 32 | +0.0239 | [-0.0333; 0.0881] | 15/25 |
| test | 8 | +0.0329 | [0.0076; 0.0592] | 7/8 |
| test | 32 | +0.0222 | [-0.0130; 0.0585] | 4/8 |
| validation | 8 | +0.0027 | [-0.0260; 0.0333] | 4/8 |
| validation | 32 | +0.0063 | [-0.0243; 0.0369] | 4/8 |

## Alcance
Exploratorio: train, validation y test tienen exposición histórica. Bootstrap descriptivo por participante, sin corrección por búsqueda histórica o multiplicidad. Las pseudoetiquetas son offline y no validan activación psicológica externa. El historial usa media/desviación y solo filas etiquetadas consecutivas; se reinicia ante huecos. No es una arquitectura sensible al orden ni un estudio de ablación de fusión. P4 y todos los participantes se conservan. No comparar métricas entre etiquetas antiguas y V2 como si fuera la misma tarea.

El baseline logístico previo está en ../activacion_v2_historial_01-11-2026/INFORME.md; su comparación con este modelo solo corresponde a OOF train, no a test.

## Interpretación final

El contraste principal predefinido (32 frente a 1 ventana) obtuvo en test ΔAUC +0,0222, IC descriptivo 95% [−0,0130; +0,0585], con mejora en 4/8 personas: resultado inconcluso. En validation la diferencia fue +0,0063 [−0,0243; +0,0369], también inconclusa.

El contraste secundario de 8 ventanas obtuvo en test ΔAUC +0,0329 [+0,0076; +0,0592], con mejora en 7/8 personas. Es una señal exploratoria favorable, pero en validation la diferencia fue +0,0027 [−0,0260; +0,0333] y en OOF train −0,0019 [−0,0495; +0,0491]. No se eleva este contraste secundario a principal ni se elige un nuevo modelo usando test.

Las AUC absolutas de los tres modelos en test tienen intervalos que incluyen 0,50. Por tanto, la diferencia pareada favorable de 8 ventanas no demuestra por sí sola capacidad predictiva robusta ni validez psicológica. No hay evidencia consistente suficiente para afirmar superioridad temporal general en activación V2.

Auditoría desde disco aprobada: 30 puntuaciones internas recalculadas, 123 AUC individuales y 21 comprobaciones de predicción tras recarga. No se ampliará la búsqueda a partir de esta evaluación.
