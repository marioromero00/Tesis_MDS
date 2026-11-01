# Avance — 10-09-2026: Nuevos Modelos y Fusiones

Fuente: búsqueda, entrenamiento y auditoría local del 10-09-2026, hora de Chile.
Los manifiestos finales registran UTC del 11-09-2026. Complementa
[[Avance - 08-09-2026 (Iteraciones de Mejora)]] y documenta cada intento nuevo.

## Qué se probó

Clasificación de atención y activación con dos modelos nuevos, LDA regularizada y
Extra Trees, junto con logística. Se comparan fusión temprana de variables y fusión
tardía de probabilidades por media, media geométrica y pesos positivos elegidos
internamente. Hay controles unimodales y logística fija con todas las variables actuales.

Atención usa EEG + GSR (18 entradas actuales). Activación usa pupila + mirada + EEG
(24, sin fracción de validez pupilar). Ninguna señal del profesor entra como predictor
de su propia etiqueta. Se mantienen las etiquetas y la partición original.

Cada familia compara ventana actual con resúmenes causales de ocho ventanas de todas
las modalidades: valores actuales, media, desviación estándar, diferencia con la más
antigua y longitud disponible. El contexto puede cruzar estímulos dentro de la grabación;
reinicia ante huecos distintos de 1 s o cambio de persona/grabación. Máximo soporte: 9 s.

Se congelaron 48 candidatos para atención y 54 para activación. Cinco folds externos
de 20/5 personas dentro de train; tres folds internos seleccionan modelo, contexto,
modalidad o pesos según estrategia. Todas las elecciones se congelan antes de evaluar
los folds externos. Reajuste con semillas 20260910 y 20260911.

## Resultados

Balanced accuracy macro por participante, promediada entre dos semillas:

| Estrategia | Atención | Activación |
|---|---:|---:|
| Logística fija, entradas actuales completas | 0,3335 | 0,3586 |
| Fusión temprana | 0,3389 | 0,3594 |
| Fusión tardía, media | 0,3426 | 0,3646 |
| Fusión tardía, geométrica | 0,3425 | 0,3651 |
| Fusión tardía, pesos internos | 0,3444 | 0,3625 |
| Control unimodal seleccionado internamente | 0,3450 | 0,3475 |

El contraste principal, fusión ponderada frente a temprana, gana +0,55 puntos porcentuales
en atención, intervalo descriptivo [-0,42; +1,60], y +0,31 en activación, [-0,71; +1,36].
Ambos incluyen cero; no se confirma superioridad estable.

En activación, la geométrica tiene el mejor promedio observado: gana +0,57 puntos frente
a temprana, intervalo [-0,32; +1,48], y +0,65 frente a logística con las mismas 24 entradas,
[-1,15; +2,45]. Frente a la logística pupilar anterior, con cinco entradas y BA 0,3536,
gana +1,15 puntos, intervalo [-0,85; +3,31]. Es una mejora numérica, todavía incierta.
Comparar con la logística pupilar cambia también las modalidades; no aísla la fusión.

## Qué enseñan las selecciones

- Activación selecciona contexto de ocho ventanas en todos los folds de fusión. Las
  fusiones tardías eligen logística en tres folds y LDA en dos. La combinación simple
  resulta competitiva frente a aprender pesos en la grilla.
- Atención selecciona Extra Trees con ventana actual en los cinco folds tardíos.
  El control unimodal queda prácticamente igual que la fusión ponderada.
- En activación, la fusión ponderada asigna 0,5 a pupila y 0,25 a mirada/EEG en cuatro
  folds; el restante asigna 0,5 a EEG. En atención, GSR recibe 0,75 en tres folds y se
  usa reparto igual en dos. Son pesos de una grilla, no contribuciones causales.

Las selecciones internas orientan preguntas posteriores. No prueban por sí mismas
que sea necesario el historial o un sensor determinado. Las probabilidades no tienen
una calibración externa adicional, lo que puede influir en su combinación.

## Registro completo y corrección técnica

`bitacora.jsonl` registra inicio/fin de cada grupo de ajustes, congelación y evaluación.
`todos_los_intentos.csv` conserva 1.530 puntuaciones con configuración y participantes.
`configuraciones_elegidas.csv` y `selecciones.json` guardan las elecciones por estrategia.

La primera ejecución se interrumpió al exigir recarga exactamente igual con predicción
paralela de Extra Trees: diferencia máxima de probabilidad 2,22e-16. Se conserva en
`resultados/fusiones_10-09-2026/`, con el modelo parcial y `interrupcion.json`.
La entrega completa reutilizó búsqueda y selecciones congeladas, reajustó los modelos
externos y fijó la predicción a un hilo. Se documentó en `reanudacion.json`.
El comando reproducible corregido usa `scripts/ejecutar_fusiones_estables.py`.

Entrega completa en `resultados/fusiones_10-09-2026_completa/`:

- 630 ajustes internos; 240 componentes externos ajustados en la ejecución completa.
- 120 bundles guardados, con pipelines por modalidad y reglas de fusión.
- 324.576 predicciones reproducidas tras recargar todos los bundles.
- 120 métricas de fold y 600 de participante recalculadas; selecciones auditadas.
- 38 pruebas aprobadas, incluidos causalidad, probabilidades y recarga determinista.
- Figuras PNG/PDF, catálogos, hashes y protocolos. El intento parcial se conserva aparte.

## Límites

El análisis usa las mismas 25 personas de train de iteraciones previas. Validation/test
originales no se vuelven a evaluar. Los intervalos son descriptivos: 2.000 remuestreos
pareados de personas después de promediar semillas, sin ajuste por comparaciones múltiples,
distinto tamaño de búsquedas ni dependencia entre folds. La adaptación entre iteraciones
impide tratar estos resultados como confirmación independiente.

Se conserva normalización offline por participante y pseudoetiquetas. No hay nueva regresión,
TCN/LSTM ni ajuste final sobre las 25 personas en esta entrega; los bundles son de folds.

[Informe completo](../../Tesis_MDS/documentacion/Fusiones_10-09-2026.md).
[Resultados y todos los intentos](../../Tesis_MDS/resultados/fusiones_10-09-2026_completa/).

## Notas relacionadas

Publicación completada en GitHub `main`, commit de resultados `543fd48`, el 10-09-2026.
Se verificaron 151 hashes de código/resultados antes del commit. La entrega contiene
155 archivos e incluye el intento parcial. Las notas se respaldan en
`documentacion/Tesis_Vault_Fusiones_10-09-2026.zip`, con inventario y hashes por archivo.
Se conservan los respaldos anteriores.

- [[Tesis_MDS]]
- [[Avance - 08-09-2026 (Iteraciones de Mejora)]]
- [[Avance - 08-09-2026 (Control del Historial Pupilar)]]
- [[Avance - 07-09-2026 (TCN LSTM y BiLSTM)]]
