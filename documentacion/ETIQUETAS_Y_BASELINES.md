# Pseudoetiquetas, partición y baselines estáticos

> [!warning] Estado metodológico
> Estas son operacionalizaciones provisionales y análisis exploratorios. La
> redefinición de emoción como activación y el uso de pupila sin corrección
> lumínica todavía requieren aprobación del profesor guía.

## Preguntas que resuelve esta etapa

1. ¿Puede construirse una etiqueta sin usar las mismas señales que luego la
   predicen? Sí: los conjuntos profesor y estudiante son disjuntos.
2. ¿Puede evaluarse fuera de muestra sin mezclar ventanas solapadas de una misma
   persona? Sí: la partición se congela por participante.
3. ¿Los predictores estáticos contienen señal suficiente para superar baselines
   triviales? En esta primera ejecución, no de manera consistente.

## Arquitectura sin circularidad

| Tarea | Profesor: construye etiqueta | Estudiante: predice |
|---|---|---|
| Atención | Eye tracking + pupila | EEG + GSR |
| Activación (*arousal*) | GSR | EEG + eye tracking + pupila |

EEG nunca construye la etiqueta que predice. GSR no predice la etiqueta de
activación que él mismo construye. Eye tracking y pupila no predicen la etiqueta
de atención que construyen.

## Etiqueta provisional de atención

Se calculan por participante componentes normalizados de:

- duración total y media de fijaciones, con dirección positiva;
- dispersión y longitud de la trayectoria de mirada, con dirección negativa;
- diámetro pupilar medio normalizado, con dirección positiva.

La variante primaria promedia primero la evidencia ocular, luego le asigna el
mismo peso que a la componente pupilar. La sensibilidad usa la primera
componente principal, ajustada únicamente con ventanas de entrenamiento. Ambas
se normalizan dentro del participante y conservan el score continuo.

La correlación de Spearman entre ambas variantes fue **0,454**. Es demasiado
baja para afirmar robustez: la construcción de atención sigue siendo una
decisión abierta importante.

## Etiqueta provisional de activación

Combina nivel tónico, componente fásica, número de SCR y prominencia media. Se
generan tres variantes:

- score instantáneo sobre 2 s;
- score primario causal con contexto de 6 s, formado por cinco ventanas
  consecutivas sin cruzar el segmento;
- primera componente principal ajustada solo en entrenamiento.

La correlación Spearman entre contexto de 6 s y PCA fue **0,668**, una
concordancia moderada. No se aplicó un desplazamiento de latencia estimado por
correlación cruzada porque los onsets no constituyen una serie independiente de
arousal verdadero; hacerlo habría optimizado contra un supuesto no observado.

## Discretización

Cada score continuo se convierte además en `bajo`, `medio` y `alto` mediante
terciles dentro de cada participante. El continuo es el producto principal para
trayectorias y regresión. La categoría se usa solo para clasificación robusta
al ruido. Los empates —especialmente ventanas sin SCR— pueden impedir tercios
exactos y se conservan, en vez de romperlos artificialmente.

La normalización dentro del participante describe un protocolo **offline y
transductivo**: utiliza la sesión del participante evaluado para expresar su
estado relativo. No usa EEG ni el objetivo del estudiante, pero no representa
un despliegue causal en tiempo real. Ese alcance debe permanecer explícito.

## Partición congelada

La semilla es `20260822`; el hash SHA-256 de `semilla:participante` define el
orden dentro de cada grupo experimental. La estratificación por `timeline`
produjo:

| División | Participantes | Uso |
|---|---:|---|
| Entrenamiento | 25 | Ajuste de modelos y PCA |
| Validación | 8 | Comparación y decisiones futuras |
| Prueba | 8 | Resultado fuera de muestra |
| Sensibilidad | 1 (P29) | Impacto del offset por aprobar |
| Excluidos | 6 | P1, P7, P14, P17, P25 y P42 |

No existe ningún participante compartido entre divisiones. Los cuatro grupos
SlowWeb aportan exactamente dos participantes a validación y dos a prueba.

## Auditoría de P29

- Tobii comienza a `2025-08-26 14:25:47.650 UTC`.
- EEG comienza 329,912 s antes y dura 1.034,550 s.
- Las 482 ventanas Tobii tienen cobertura EEG completa.
- EEG: frecuencia efectiva 125,146 Hz, sin saltos, 0,031 % en rail y 0,085 %
  de repetición plana.

La evidencia es compatible con un prerregistro EEG largo; no prueba por sí sola
la identidad experimental ni corrige deriva. Por eso P29 queda en sensibilidad,
no en prueba principal.

## Baselines implementados

Para cada score continuo: media de entrenamiento, Ridge y Random Forest. Para
cada etiqueta ternaria: clase prioritaria, regresión logística balanceada y
Random Forest balanceado. La imputación y el escalamiento se ajustan solo con
entrenamiento; `n_jobs=1` mantiene la ejecución secuencial.

### Resultados principales en prueba

| Tarea | Modelo | Métrica principal | Resultado |
|---|---|---|---:|
| Atención continua | Ridge | R² | -0,0025 |
| Atención ternaria | Logística | Balanced accuracy | 0,3240 |
| Atención ternaria | Random Forest | Balanced accuracy | 0,3197 |
| Activación 6 s continua | Ridge | R² | 0,0051 |
| Activación 6 s ternaria | Logística | Balanced accuracy | 0,3169 |
| Activación 6 s ternaria | Random Forest | Balanced accuracy | 0,3365 |

El nivel azar para tres clases balanceadas es aproximadamente 0,333. Ningún
baseline supera de forma consistente al trivial; los R² son cercanos a cero.
Esto no demuestra que las señales carezcan de información. Indica que, bajo
estas pseudoetiquetas y características estáticas agregadas, no hay evidencia
fuera de muestra suficiente para afirmar capacidad predictiva.

## Interpretación antes de modelos temporales

- La dificultad no puede atribuirse todavía a falta de memoria temporal:
  también puede provenir del ruido de las pseudoetiquetas.
- Entrenar LSTM/TCN/Transformer ahora serviría como contraste experimental, no
  como garantía de mejora.
- La baja concordancia de la etiqueta de atención exige resolver luminancia,
  pesos o validación externa antes de convertir resultados en afirmaciones.
- La variante de arousal a 6 s tiene una justificación fisiológica mayor, pero
  tampoco supera claramente el baseline trivial.

## Reproducción

```powershell
python .\scripts\preparar_modelado.py
python .\scripts\baselines_estaticos.py
```

La ejecución completa sigue disponible en `scripts/ejecutar_todo.py`. Código,
dependencias, configuración, partición, métricas, importancias y manifiestos se
versionan. Las predicciones por ventana se regeneran determinísticamente y se
mantienen fuera de Git para evitar inflar el repositorio.

## Productos

- `config/modelado.json`
- `resultados/modelado/dataset_modelado.csv`
- `resultados/modelado/particion_participantes.csv`
- `resultados/modelado/metricas_baselines.csv`
- `resultados/modelado/importancia_features.csv`
- `resultados/modelado/manifiesto_etiquetas.json`
- `resultados/modelado/manifiesto_baselines.json`
