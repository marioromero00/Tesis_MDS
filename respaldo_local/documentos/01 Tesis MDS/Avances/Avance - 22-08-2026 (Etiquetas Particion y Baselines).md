# Avance - 22-08-2026 (Etiquetas, partición y baselines)

## Qué se hizo

Se completó la primera iteración de modelado después del preprocesamiento:

1. pseudoetiquetas continuas y ternarias para atención y activación;
2. separación explícita entre señales profesor y estudiante;
3. partición congelada por participante y grupo experimental;
4. auditoría profunda de P29;
5. baselines estáticos de regresión y clasificación;
6. análisis de sensibilidad para fusión PCA y ventana GSR de 2 s.

El protocolo técnico completo está en
`Tesis_MDS/documentacion/ETIQUETAS_Y_BASELINES.md`.

## Diseño sin circularidad

| Objetivo | Profesor | Estudiante |
|---|---|---|
| Atención | Eye tracking + pupila | EEG + GSR |
| Activación (*arousal*) | GSR | EEG + eye tracking + pupila |

La misma señal nunca construye y predice su propia etiqueta. Los scores
continuos se conservan para estudiar trayectorias; los terciles solo sirven para
el contraste de clasificación.

## Estado real de las etiquetas

### Atención

La variante primaria combina evidencia ocular y pupilar con pesos iguales. La
sensibilidad usa PCA ajustado solo en entrenamiento. La correlación Spearman
entre ambas fue **0,454**: no existe robustez suficiente al método de fusión.
Esto obliga a resolver la corrección lumínica o conseguir validación externa
antes de tratar la pseudoetiqueta como constructo cerrado.

### Activación

La variante primaria agrega GSR causalmente sobre 6 s; se comparó con 2 s y PCA.
La correlación 6 s–PCA fue **0,668**, moderada. Sigue pendiente que el profesor
acepte reemplazar “emoción” por activación/arousal.

## Partición congelada

| División | Participantes |
|---|---:|
| Entrenamiento | 25 |
| Validación | 8 |
| Prueba | 8 |
| Sensibilidad | P29 |
| Excluidos | P1, P7, P14, P17, P25, P42 |

Cada grupo SlowWeb aporta dos participantes a validación y dos a prueba. No se
mezclan ventanas de un participante entre divisiones.

## P29

EEG comienza 329,912 s antes que Tobii, pero dura 1.034,55 s y cubre las 482
ventanas experimentales al 100 %. La frecuencia efectiva es 125,146 Hz, sin
saltos, con 0,031 % en rail y 0,085 % de repetición plana. Esto es compatible
con un inicio EEG anticipado, pero no reemplaza la aprobación experimental; P29
queda solo como sensibilidad.

## Resultados fuera de muestra

| Tarea | Modelo | Métrica | Test |
|---|---|---|---:|
| Atención continua | Ridge | R² | -0,0025 |
| Atención ternaria | Logística | Balanced accuracy | 0,3240 |
| Atención ternaria | Random Forest | Balanced accuracy | 0,3197 |
| Activación 6 s continua | Ridge | R² | 0,0051 |
| Activación 6 s ternaria | Logística | Balanced accuracy | 0,3169 |
| Activación 6 s ternaria | Random Forest | Balanced accuracy | 0,3365 |

Con tres clases, el nivel de referencia es aproximadamente 0,333. Los modelos
estáticos no muestran una mejora consistente. Los modelos lineales tampoco
explican varianza continua fuera de muestra.

## Interpretación correcta

- No se puede afirmar todavía que EEG y las otras modalidades predicen estas
  pseudoetiquetas en participantes nuevos.
- El resultado tampoco demuestra ausencia de información temporal: los
  baselines destruyen deliberadamente la secuencia.
- Un modelo temporal será una prueba de la hipótesis, pero no arreglará por sí
  mismo una etiqueta ruidosa.
- La prioridad metodológica es validar el profesor de atención; luego se puede
  comparar estático vs. temporal sobre una etiqueta fija.

## Reproducibilidad

```powershell
python .\scripts\preparar_modelado.py
python .\scripts\baselines_estaticos.py
```

Quedaron versionados configuración, partición, dataset, métricas, importancias y
manifiestos. Las predicciones por ventana son regenerables y no se subirán para
evitar inflar innecesariamente Git.

## Próximas decisiones

- [ ] Profesor: aceptar activación/arousal como alcance emocional.
- [ ] Profesor: decidir si P29 entra al análisis principal.
- [ ] Verificar existencia de capturas o luminancia de estímulos.
- [ ] Validar Attention Score contra alguna medida externa, si existe.
- [ ] Solo después, implementar un primer TCN/LSTM con idéntica partición.

## Relacionado

- [[Tesis_MDS]]
- [[Etiqueta Atencion]]
- [[Etiqueta Emocion]]
- [[Modelo Profesor - Decisiones]]
- [[Avance - 22-08-2026 (Pipeline Multimodal Reproducible)]]
