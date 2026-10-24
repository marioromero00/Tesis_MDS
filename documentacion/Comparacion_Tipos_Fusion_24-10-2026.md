# Comparación de tipos de fusión sobre pseudoetiquetas auditadas

**Corrección posterior:** las pseudoetiquetas usadas aquí tienen componentes del profesor desalineados entre ventanas. Esta comparación se conserva como registro histórico y no constituye evidencia válida sobre los tipos de fusión. Véase [Pipeline_PCA_Senales_24-10-2026.md](Pipeline_PCA_Senales_24-10-2026.md).

## Protocolo

Se mantienen las 21.719 ventanas primarias elegibles y el split congelado de 25/8/8 participantes. Atención usa EEG y GSR; activación usa EEG, mirada y pupila. Ningún modelo recibe la señal que construye su etiqueta. Se evaluaron las etiquetas auditadas principales y, por separado, las dos candidatas exploratorias del estudio de pseudoetiquetas.

Para cada etiqueta se usaron dos contextos: ventana actual y ventana actual más promedio causal de seis ventanas de 2 s separadas por 1 s (soporte máximo de 7 s). El historial reinicia en cambios de grabación, segmento o huecos temporales. Todas las modalidades usan el mismo contexto, participantes y filas. Los imputadores, escaladores, PCA y modelos se ajustan solo con train; se evalúan validation y test sin seleccionar configuraciones a partir de sus resultados.

- **Temprana:** concatenar características y ajustar una regresión logística.
- **Intermedia:** imputar, escalar y reducir cada modalidad con PCA no supervisado al 90 % de varianza de train; concatenar representaciones y ajustar una regresión logística.
- **Tardía:** ajustar una regresión logística por modalidad y combinar probabilidades con media aritmética o geométrica, con pesos iguales.
- **Controles:** cada modalidad por separado, mismo estimador.

Todas las regresiones logísticas usan el mismo `class_weight='balanced'` y parámetros fijos. No hay búsqueda de hiperparámetros. Este es un contraste exploratorio: test y las etiquetas alternativas ya se habían inspeccionado en el trabajo anterior.

## Resultados principales

Precisión balanceada global en test; Dummy = 0,3333. Cada fila usa 4.017 ventanas y ocho participantes.

| Etiqueta y contexto | Temprana | Intermedia | Tardía media | Tardía geométrica | Mejor unimodal observado | Solo estímulo |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Atención auditada, actual | 0,3164 | 0,3164 | 0,3137 | 0,3134 | GSR 0,3234 | 0,3209 |
| Atención auditada, historial | 0,3331 | 0,3279 | 0,3343 | 0,3336 | GSR 0,3386 | 0,3209 |
| Activación auditada, actual | 0,3171 | 0,3241 | 0,3201 | 0,3200 | Pupila 0,3428 | 0,3874 |
| Activación auditada, historial | 0,3234 | 0,3262 | 0,3200 | 0,3208 | Mirada 0,3516 | 0,3874 |
| Atención solo mirada, actual | 0,3465 | 0,3510 | 0,3445 | 0,3453 | EEG 0,3433 | 0,3485 |
| Atención solo mirada, historial | 0,3381 | 0,3398 | 0,3346 | 0,3338 | GSR 0,3376 | 0,3485 |
| Activación GSR continuo, actual | 0,3722 | 0,3595 | 0,3737 | 0,3774 | EEG 0,3580 | 0,3991 |
| Activación GSR continuo, historial | 0,3861 | 0,3826 | 0,3966 | 0,3943 | Pupila 0,3659 | 0,3991 |

En las **etiquetas auditadas**, la mayor BA de una fusión es 0,3343 para atención y 0,3262 para activación. El mejor control unimodal observado en esas mismas filas llega respectivamente a 0,3386 y 0,3516. Por tanto, no aparece un aporte consistente de combinar modalidades. El control de solo estímulo obtiene 0,3874 en activación auditada, por encima de todas las fusiones con señales.

La mayor ganancia numérica de una fusión tardía sobre temprana es **+0,0105 BA global** para activación GSR continuo con historial (0,3966 frente a 0,3861). En ocho participantes, la diferencia media pareada de BA por participante es +0,0109, con intervalo descriptivo de remuestreo del 95 % de **−0,0057 a +0,0284**; mejora en cuatro de ocho. El control de solo estímulo obtiene 0,3991. Esa etiqueta alternativa coincide en solo 32,2 % con la auditada y está muy asociada al estímulo: la cifra no demuestra mejor predicción del constructo psicológico.

Para atención auditada con historial, tardía media supera a temprana por **+0,0012 BA global** (0,3343 frente a 0,3331). La diferencia pareada media por participante es +0,0012, intervalo **−0,0020 a +0,0043**, con mejora en cuatro de ocho. Es un cambio pequeño e incierto.

Los intervalos son descriptivos, remuestrean participantes y no corrigen comparaciones múltiples ni el uso previo de test. En P37 falta la clase media para activación auditada; la BA por participante promedia solo clases observadas. La tabla principal usa BA global. Una etiqueta diferente cambia el problema, por lo que sus BA no miden una mejora directa respecto de la referencia original.

## Artefactos y reproducción

- `resultados/fusion_pseudoetiquetas_24-10-2026/protocolo.json`
- `resultados/fusion_pseudoetiquetas_24-10-2026/metricas_fusion.csv`
- `resultados/fusion_pseudoetiquetas_24-10-2026/metricas_participantes.csv`
- `resultados/fusion_pseudoetiquetas_24-10-2026/ganancias_pareadas.csv`
- `resultados/fusion_pseudoetiquetas_24-10-2026/predicciones.csv.gz`

```powershell
python scripts/comparar_tipos_fusion.py
python scripts/resumir_tipos_fusion.py
python -m unittest tests.test_tipos_fusion tests.test_estudio_pseudoetiquetas -v
```
