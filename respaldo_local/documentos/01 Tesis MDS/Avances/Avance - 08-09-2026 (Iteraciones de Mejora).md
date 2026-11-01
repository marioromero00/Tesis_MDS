# Avance — 08-09-2026: Iteraciones de Mejora

Fuente: tres búsquedas y auditorías locales del 08-09-2026 en
`C:/Users/MarioRomero/desktop/mds/Tesis_MDS/`.
Complementa [[Avance - 08-09-2026 (Control del Historial Pupilar)]] y registra el seguimiento
solicitado para mejorar el desempeño. El contraste controlado anterior se conserva.

## Resultado

El mejor promedio observado pasa de 0,3536 a 0,3546 de balanced accuracy macro por
participante: **+0,11 puntos porcentuales**, intervalo descriptivo del 95%
[-1,03; +1,16]. Mejora en 16/25 personas. Es una mejora numérica mínima e incierta;
no se obtiene evidencia de superioridad estable sobre la logística.

| Procedimiento | BA macro por participante | Diferencia frente a logística, pp |
|---|---:|---:|
| Logística fija, cinco entradas pupilares | 0,3536 | 0 |
| Primera búsqueda, selección entre 105 candidatos | 0,3546 | +0,11 |
| Segunda iteración, combinación con peso elegido internamente | 0,3525 | -0,11 |
| Segunda iteración, combinación fija 50/50 | 0,3534 | -0,02 |
| Tercera iteración, búsqueda con mirada y EEG | 0,3527 | -0,09 |

La primera búsqueda supera en promedio al MLP pupilar anterior por +0,96 puntos,
intervalo [-0,16; +2,15], y a LSTM por +0,12, intervalo [-1,45; +1,52]. El resultado
sigue dependiendo de la referencia. No se selecciona un nuevo ganador confirmado
comparando los máximos obtenidos entre iteraciones.

## Primera iteración

Se mantienen las cinco entradas pupilares. Se prueban la ventana actual y resúmenes
causales de 4/8/16 ventanas, limitados al segmento o continuos dentro de la grabación.
Cada resumen agrega media, desviación estándar, diferencia entre actual y más antigua
y longitud disponible: 21 columnas derivadas de cinco variables originales.

Se comparan logística con C=0,01/0,1/1, HistGradientBoosting regularizado y aproximación
RBF Nyström con logística. Suavizado causal de probabilidades en 1/4/8 ventanas.
Son 105 candidatos y 525 ajustes internos; se guardan 40 pipelines externos.

Se evalúan por separado las reglas de selección entre todos los candidatos, solo los
temporales, solo los actuales y la logística fija anterior. La selección temporal sola
obtiene 0,3519, por debajo de la logística. Parte de la búsqueda puede mejorar por
regularización o modelo, sin que eso pruebe un aporte del historial.

## Segunda iteración

Se combina la logística fija con el candidato temporal de cada fold. Se elige peso temporal
entre 0/0,25/0,5/0,75/1 usando las particiones internas; un control conserva siempre 0,5.
Se realizan 30 ajustes internos adicionales y se guardan 20 combinaciones con ambos
pipelines y sus parámetros. Ninguna regla de combinación mejora a logística en promedio.

## Tercera iteración

Se amplía a pupila + mirada (15 entradas actuales) y pupila + mirada + EEG (24), con o
sin resumen temporal pupilar de ocho ventanas. Se prueban 48 candidatos, se realizan
240 ajustes internos y se guardan 30 pipelines externos. El mejor procedimiento
predefinido de esta iteración obtiene 0,3527. Añadir modalidades no mejora el promedio.

Se usa fusión temprana de features. GSR construye la etiqueta y no entra como predictor.
No se incluye fracción de validez pupilar; los indicadores de ausencias pueden conservar
información de calidad. Las features y pseudoetiquetas heredan normalización offline.

## Evaluación y límites

Las tres iteraciones usan exclusivamente los 25 participantes originales de train,
con los mismos cinco folds externos de 20/5 personas. Cada selección se realiza mediante
tres folds internos agrupados y media de las BA macro internas, con igual peso por fold.
Todas las configuraciones elegidas se congelan antes de evaluar externamente esa iteración.
Dos semillas de reajuste; algunos modelos son deterministas y coinciden entre semillas.

Las representaciones y el suavizado acceden solo a pasado y presente, reiniciando ante
cambio de persona/grabación o hueco distinto de 1 s. El contexto de grabación puede cruzar
estímulos. No se usan etiquetas pasadas como entradas. Imputación, escalado y aproximación
RBF se ajustan únicamente en las personas de entrenamiento correspondientes.

Validation y test originales no se vuelven a evaluar. Aun así, estas personas de train
ya se usaron en investigaciones previas: la validación anidada no elimina la adaptación
entre iteraciones. Los intervalos usan 2.000 remuestreos pareados de personas, tras promediar
semillas, sin ajuste por comparaciones múltiples ni dependencia entre folds.
Se necesita confirmación con participantes nuevos antes de afirmar superioridad.
Esta búsqueda se limita a clasificación de activación; no reentrena atención ni regresión.

## Entrega verificada

- 795 ajustes internos y 70 pipelines externos entrenados.
- 90 archivos de modelos: 70 pipelines y 20 combinaciones con sus componentes.
- 243.432 predicciones externas verificadas tras recargar modelos.
- Selecciones internas auditadas; se conservan todos los puntajes, incluidos intentos fallidos.
- 33 pruebas aprobadas, incluidas causalidad, separación de participantes y exclusión de GSR.

[Informe conjunto](../../Tesis_MDS/documentacion/Optimizacion_Historial_08-09-2026.md).
[Resultados, modelos y protocolos](../../Tesis_MDS/resultados/optimizacion_historial_08-09-2026/).

## Notas relacionadas

- [[Avance - 10-09-2026 (Publicacion de Iteraciones)]] — cierre de publicación en GitHub.
- [[Tesis_MDS]]
- [[Avance - 08-09-2026 (Control del Historial Pupilar)]]
- [[Avance - 07-09-2026 (TCN LSTM y BiLSTM)]]
