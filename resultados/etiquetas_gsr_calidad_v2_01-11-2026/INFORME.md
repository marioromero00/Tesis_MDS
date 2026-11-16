# Etiquetas GSR de activación V2

Versión nueva basada en calidad del profesor. Conserva todas las filas y particiones originales; una fila descartada para aprendizaje conserva su motivo y etiqueta nueva ausente. No se entrenaron modelos.

Cobertura mínima heredada: 50%. Se requieren cuatro componentes finitos y SCR no negativos. La normalización personal usa solo ventanas válidas. El score6s exige cinco ventanas consecutivas válidas del mismo estímulo/segmento/registro; se reinicia tras huecos. Componentes constantes observados aportan cero; ausencias no se rellenan con cero. Scores sin variación no generan etiquetas. Empates numéricos con la mediana (tolerancia1e-8) quedan sin etiqueta.

## Retención por partición

| Partición | Ventanas | GSR válido | Etiqueta anterior | Etiqueta V2 |
|---|---:|---:|---:|---:|
| test | 4025 | 4025 | 4025 | 2184 |
| train | 13524 | 13123 | 13524 | 7028 |
| validation | 4662 | 4662 | 4662 | 2584 |

## Personas

| Persona | Partición | Total | V2 | Positivos | Negativos | Cambios en filas comunes |
|---|---|---:|---:|---:|---:|---:|
| P10 | test | 500 | 280 | 140 | 140 | 132/280 |
| P11 | test | 483 | 266 | 133 | 133 | 135/266 |
| P15 | test | 496 | 278 | 139 | 139 | 116/278 |
| P16 | test | 489 | 272 | 136 | 136 | 131/272 |
| P37 | test | 561 | 318 | 159 | 159 | 156/318 |
| P39 | test | 480 | 240 | 120 | 120 | 124/240 |
| P45 | test | 548 | 284 | 142 | 142 | 120/284 |
| P5 | test | 468 | 246 | 123 | 123 | 187/246 |
| P12 | train | 463 | 246 | 123 | 123 | 144/246 |
| P13 | train | 542 | 288 | 144 | 144 | 166/288 |
| P18 | train | 471 | 258 | 129 | 129 | 122/258 |
| P19 | train | 478 | 266 | 133 | 133 | 155/266 |
| P2 | train | 643 | 340 | 170 | 170 | 217/340 |
| P20 | train | 695 | 406 | 203 | 203 | 263/406 |
| P21 | train | 557 | 310 | 155 | 155 | 224/310 |
| P22 | train | 518 | 316 | 158 | 158 | 140/316 |
| P24 | train | 518 | 264 | 132 | 132 | 131/264 |
| P26 | train | 525 | 272 | 136 | 136 | 141/272 |
| P27 | train | 463 | 238 | 119 | 119 | 128/238 |
| P3 | train | 483 | 246 | 123 | 123 | 116/246 |
| P30 | train | 595 | 298 | 149 | 149 | 115/298 |
| P33 | train | 512 | 270 | 135 | 135 | 146/270 |
| P34 | train | 536 | 288 | 144 | 144 | 126/288 |
| P35 | train | 540 | 278 | 139 | 139 | 56/278 |
| P36 | train | 509 | 280 | 140 | 140 | 173/280 |
| P4 | train | 459 | 26 | 13 | 13 | 12/26 |
| P40 | train | 488 | 296 | 148 | 148 | 125/296 |
| P43 | train | 664 | 350 | 175 | 175 | 170/350 |
| P44 | train | 547 | 290 | 145 | 145 | 108/290 |
| P46 | train | 588 | 322 | 161 | 161 | 71/322 |
| P48 | train | 591 | 306 | 153 | 153 | 139/306 |
| P8 | train | 628 | 320 | 160 | 160 | 206/320 |
| P9 | train | 511 | 254 | 127 | 127 | 141/254 |
| P23 | validation | 414 | 224 | 112 | 112 | 107/224 |
| P28 | validation | 445 | 242 | 121 | 121 | 126/242 |
| P31 | validation | 585 | 326 | 163 | 163 | 179/326 |
| P32 | validation | 509 | 272 | 136 | 136 | 181/272 |
| P38 | validation | 757 | 440 | 220 | 220 | 177/440 |
| P41 | validation | 523 | 280 | 140 | 140 | 50/280 |
| P47 | validation | 753 | 420 | 210 | 210 | 179/420 |
| P6 | validation | 676 | 380 | 190 | 190 | 189/380 |

Esta versión modifica score, soporte temporal y manejo de empates: las métricas de versiones anteriores no pueden atribuirse a estas etiquetas. Las comparaciones futuras deben usar exactamente las mismas filas V2 en todos los modelos y reconstruir los índices temporales sin cruzar los huecos. Ninguna persona se elimina por su AUC. Revisar personas con una sola clase o sin etiquetas y reportar sus denominadores.

Limitaciones: la cobertura mínima50% proviene del protocolo anterior y no equivale a una garantía fisiológica. Esta corrección usa características derivadas; no incorpora un detector nuevo de artefactos sobre señal cruda ni certifica sincronización externa. Normalización y mediana por sesión siguen siendo offline; no son etiquetas clínicas ni autorreportes.

## Auditoría independiente del 2 de noviembre de 2026

Se confirmó un error de alineación en el generador histórico `scripts/preparar_modelado.py`: `groupby(..., group_keys=False).apply(...).reset_index(level=0, drop=True)` sustituye los índices originales por posiciones en el orden de los grupos. En estas entradas, 25.498 de 25.992 posiciones de componentes quedan desplazadas. Este denominador corresponde al archivo completo, incluyendo personas fuera de las particiones principales; no equivale al número de etiquetas binarias que cambian.

El generador histórico reprodujo los scores archivados de activación con errores máximos absolutos de 4,82e-7 (2 s) y 2,92e-7 (6 s), compatibles con la precisión de exportación. Por tanto, el problema afecta efectivamente a esos resultados guardados. Los AUC anteriores de activación basados en esas etiquetas no permiten respaldar ni rechazar la hipótesis; deben recalcularse con el profesor corregido. El patrón también aparece en el profesor histórico de atención, pero esta auditoría no certifica ni invalida las reconstrucciones posteriores de atención.

La V2 conserva la identidad de las ventanas mediante asignación por índice. Se reprodujeron sus scores y etiquetas guardadas a tolerancia 1e-12, se verificó la normalización con un cálculo independiente y se comprobó el soporte temporal de cada etiqueta. Se preservaron hashes de la fuente y partición. Evidencia: `auditoria_independiente_02-11-2026.json`; ejecución reproducible: `.venv/bin/python scripts/auditar_etiquetas_gsr_v2.py`. El generador histórico se conserva como evidencia y no debe utilizarse para nuevas etiquetas de activación; usar `reconstruir_etiquetas_gsr_calidad_v2.py`.

Quedan 11.796 etiquetas de 22.211 ventanas (53,1%). Las otras 10.415 corresponden a 9.995 con historial insuficiente, 401 con cobertura/flag inválido y 19 empates. La mayor pérdida proviene de exigir cinco ventanas consecutivas dentro del mismo estímulo/segmento, no de mala calidad GSR. P4 conserva 26 de 459 ventanas. Las 41 personas conservan ambas clases. Las clases aproximadamente equilibradas son consecuencia del umbral por mediana y no demuestran validez psicológica.

Siguiente evaluación: entrenar desde cero los modelos estático y temporal sobre las mismas filas V2 y particiones, sin cruzar huecos, y comparar AUC y diferencias con incertidumbre por participante. No se calcularon nuevos AUC en esta reconstrucción; el test previamente consultado continúa siendo exploratorio.
