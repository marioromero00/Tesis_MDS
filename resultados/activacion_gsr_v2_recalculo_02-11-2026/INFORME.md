# Activación V2: comparación final acotada

Etiquetas GSR V2 verificadas por auditoría de alineación y calidad; repetición desde cero del protocolo existente. HistGradientBoosting, dos candidatos (7/15 hojas), 30 ajustes internos, 15 modelos externos OOF y tres modelos finales. Configuración común a los contextos seleccionada solo con AUC interna de train. Comparación principal: 32 menos 1; secundaria: 8 menos 1. Modelos finales congelados antes de evaluar validation/test.

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


## Interpretación de la hipótesis y cierre de auditoría (02-11-2026)

Reentrenamiento completo: 30 ajustes internos, 15 modelos OOF y tres finales, con las mismas etiquetas GSR V2, filas y particiones. La auditoría independiente recalculó 123 AUC por participante, verificó 30 scores internos y realizó 21 comprobaciones de predicciones desde modelos guardados. Búsqueda, predicciones y métricas reproducen exactamente la ejecución V2 previa; ver `reproducibilidad.json` y `auditoria_desde_disco.json`.

La comparación principal (hasta 32 ventanas frente a actual) obtiene ΔAUC test +0,02223, IC descriptivo 95% [-0,01300; +0,05852]. No permite afirmar superioridad temporal ni demostrar ausencia de efecto. La secundaria (hasta 8 ventanas) obtiene +0,03288 [+0,00763; +0,05916], con mejora en 7/8 personas, pero no se confirma en validación: +0,00269 [-0,02600; +0,03325], ni en OOF train. Es una señal exploratoria, no validación robusta de la hipótesis general. Los AUC absolutos siguen próximos a 0,5 y sus intervalos incluyen 0,5. Los intervalos de diferencias son pareados por participante; no se infieren de la superposición de los intervalos individuales.

Las etiquetas son pseudoetiquetas GSR relativas a la sesión y normalizadas offline; este resultado no valida una medida psicológica externa. La reutilización histórica de test impide presentarlo como confirmación independiente. No se alteró el protocolo según estos resultados.

### Historial efectivo en test

- Contexto 1: historial medio 1.00 ventanas; 100.0% con contexto completo.
- Contexto 8: historial medio 5.06 ventanas; 40.8% con contexto completo.
- Contexto 32: historial medio 8.73 ventanas; 0.0% con contexto completo.

Ninguna fila de test dispone de 32 ventanas completas: la comparación principal prueba agregación sobre el historial disponible, no secuencias completas de 32. El historial usa solo filas etiquetadas consecutivas, por lo que omite ventanas iniciales válidas sin etiqueta. Mantener esta limitación explícita en la tesis. Las medias y desviaciones temporales tampoco prueban una arquitectura sensible al orden.
