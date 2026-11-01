# Avance — 07-09-2026: TCN, LSTM y BiLSTM

Complementado por [[Avance - 08-09-2026 (Control del Historial Pupilar)]], fuente vigente
del control de ventana actual con las mismas cinco variables. Esta nota conserva los
resultados y el alcance de la ejecución del 07-09-2026.

Fuente: entrenamiento, evaluación y auditoría local completados el 07-09-2026, hora de
Chile. Los manifiestos registran horas UTC del 08-09-2026. Código y resultados en
`C:/Users/MarioRomero/desktop/mds/Tesis_MDS/`.
Complementa [[Avance - 07-09-2026 (Estabilidad y Reduccion de Variables)]].

## Entrega realizada

Se entrenaron y guardaron 104 redes: 32 TCN, 32 LSTM, 32 BiLSTM y ocho controles MLP
que solo leen la ventana actual. Incluye clasificación y regresión de atención y
activación, los ocho conjuntos de entradas congelados y dos semillas por configuración.
Pesos `.pt`, preprocesadores `.joblib`, metadatos, pérdidas por época, predicciones,
probabilidades, métricas y explicaciones quedaron guardados.

Se mantuvieron las etiquetas principales, contexto GSR de 6 s y split 25/8/8. Entrenamiento
ajusta imputación/escalado y redes; validación elige época y arquitectura/conjunto por
media entre semillas. Esa selección se congeló antes de evaluar test. Los resultados
de prueba y sus rankings no se usaron para volver a entrenar.

## Resultados

Balanced accuracy global de prueba, redes completas promediadas entre dos semillas:

| Modelo | Atención | Activación |
|---|---:|---:|
| Logística estática | 0,3240 | 0,3169 |
| Random Forest estático | 0,3197 | 0,3365 |
| TCN | 0,3356 | 0,3551 |
| LSTM | 0,3333 | 0,3354 |
| BiLSTM | 0,3284 | 0,3594 |
| MLP sin historial | 0,3220 | 0,3503 |

La clasificación de activación mejora puntualmente frente a algunos baselines; el
control sin historial sigue siendo competitivo. No se demuestra una ventaja general
de la temporalidad. Los R² de los scores continuos permanecen cerca de cero.

La selección de clasificación de activación anterior a test fue **BiLSTM con cinco
variables pupilares**, sin fracción de validez. BA global media: 0,3929 en validación y
0,3472 en prueba. Frente a logística con esas mismas entradas, la mejora macro por
participante es 0,0192, intervalo descriptivo [-0,0065; 0,0449]. No se confirma superioridad.

En activación completa, LSTM mejora 0,0212 de BA macro frente a logística, intervalo
[0,0058; 0,0400], pero frente al MLP sin historial la diferencia es -0,0032,
intervalo [-0,0312; 0,0193]. Los intervalos son exploratorios, sin ajuste por múltiples
comparaciones, y usan ocho participantes de prueba.

## Variables que sostienen la diferencia

`pupil_std_z`, la variabilidad pupilar, destaca en la BiLSTM seleccionada para activación.
En la semilla principal, su importancia diferencial frente a logística es 0,0190 en
validación y 0,0342 en prueba. La segunda combina caída de 0,0125 en la BiLSTM con
mejora de 0,0217 en la logística al perturbar esa entrada. No es una contribución
aditiva ni un efecto causal.

Se guardan por variable y modalidad: importancia temporal, importancia del baseline,
diferencia entre ambas y cambio de ventaja del modelo, además de intervalos y resultados
por participante. Se explican los ocho modelos seleccionados por validación, semilla
principal, en validación y en prueba como diagnóstico post hoc.

El grupo pupilar completo no conserva una importancia diferencial positiva en prueba,
por lo que la dependencia de `pupil_std_z` no implica una ventaja estable de toda la
modalidad. En atención, los rankings de amplitud EEG tienen incertidumbre amplia.
Las entradas de calidad y las correlaciones deben seguir identificadas como tales.

## Secuencias y límites

Se usan hasta ocho ventanas consecutivas del mismo participante/grabación/segmento/
estímulo, reiniciando ante huecos. El máximo abarca 9 s: ventanas de 2 s, avance de 1 s.
Las secuencias cortas se conservan con longitud explícita; el padding no puede influir.
La BiLSTM recorre en ambas direcciones únicamente la historia hasta el endpoint.
No incorpora ventanas futuras, aunque las features y etiquetas heredan normalización
offline por participante; esto impide afirmar validación en tiempo real.

Las TCN usan bloques residuales causales; las recurrentes tienen 24 unidades por
dirección. Se entrenaron en CPU con hasta 30 épocas y early stopping por validación.
Se mantuvo la separación de modalidades profesor/estudiante. Esta primera ejecución
usa concatenación temprana de features y no completa todas las estrategias de fusión.

Los controles de repetir la ventana actual en el pasado e invertir el historial
muestran resultados mixtos. El MLP se entrenó solo en conjuntos completos; no hay un
MLP con cinco variables para aislar ese contraste reducido. Dos semillas y un único
split de participantes limitan la generalización de las conclusiones.

## Verificación y ubicación

- 26 pruebas aprobadas, incluidas separación temporal, padding y recarga de arquitecturas.
- 104 modelos y 903.448 predicciones verificadas.
- 44.422 ventanas de secuencia auditadas; 208 métricas recalculadas.
- 280 registros de importancia diferencial comprobados algebraicamente.

[Informe completo](../../Tesis_MDS/documentacion/Modelos_Temporales_07-09-2026.md).
[Resultados, modelos y gráficos](../../Tesis_MDS/resultados/temporales_07-09-2026/).

## Publicación en GitHub

Se completó `git push origin main` el 07-09-2026. El remoto confirmó el commit
`23017c30553cd32232708926273a6973d42cff6b` con redes, resultados, informes, código y pruebas.
Antes del commit se verificaron 254 hashes de código, dependencias y resultados contra
los objetos preparados en Git. Se preservan los bytes de las ejecuciones en `.gitattributes`.

Esta nota y el índice se incorporan al respaldo
`documentacion/Tesis_Vault_Temporales_07-09-2026.zip`, con inventario por archivo.
Los respaldos anteriores se conservan. La publicación incluye solo el trabajo de tesis.

## Continuidad

El siguiente contraste debe fijar hipótesis sobre contexto y fusión, manteniendo controles
de ventana actual. Estos resultados de test quedan como evaluación registrada y no como
guía para optimizar hiperparámetros sobre los mismos participantes.

## Notas relacionadas

- [[Tesis_MDS]]
- [[Avance - 07-09-2026 (Estabilidad y Reduccion de Variables)]]
- [[Avance - 07-09-2026 (Importancia de Variables)]]
- [[Avance - 05-09-2026 (Baselines Entrenados y Guardados)]]
