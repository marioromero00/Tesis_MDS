# Verificación de las correcciones de la ronda 5 (commit `4202b16`) — ronda 7, 27-11-2026

Verificador independiente. No se editó ningún archivo existente, no se entrenó ni ajustó ningún modelo, no se corrió ningún análisis nuevo y no se hicieron commits. Este informe es el único archivo creado. Las comprobaciones leen CSV, protocolos, informes, scripts y el historial de Git; la presentación se regeneró en una copia temporal fuera del repositorio.

Siglas: RD, CO y SP son los borradores de Resultados y Discusión, Conclusiones y Secciones pendientes del vault (`documentos/01 Tesis MDS/Escritura/`); MI, la minuta (`Avances/`); CI, `documentacion/Cierre_Experimental_Final_23-11-2026.md`; EN, `presentaciones/avances_tesis_06-11-2026/ENSAYO.md`; RE, `relato.py`; PE y LOOP, `notas/pendientes-cierre-26-11-2026.md` y `notas/loop-revision-26-11-2026.md`.

## Resultado

- **Las correcciones de fondo son correctas.** Todos los hechos, cifras y atribuciones nuevos se comprobaron en la fuente primaria y coinciden.
- **Ningún error bloqueante.** 3 errores importantes y 13 menores, casi todos en `ENSAYO.md`.
- **9 puntos sin propagar**, todos menores.
- Las reglas del proyecto se cumplen.

## Recuento de lo revisado

| Qué | Cantidad |
|---|---|
| Bloques de cambio (`@@`) en documentos, leídos completos | 116 |
| — RD | 40 |
| — EN | 39 |
| — CO, MI y SP (juntos) | 17 |
| — RE | 9 |
| — CI | 7 |
| — PE | 3 |
| — LOOP | 1 |
| Archivos generados comparados con una regeneración (`GUIÓN.md`, `index.html`, `FUENTES.md`, `LEEME.md`) | 4, idénticos |
| Gráficos SVG modificados | 28: solo fecha e identificadores internos; contenido igual |
| Archivos nuevos de `ronda6/` | 6 (los dos informes se leyeron; no se auditan aquí) |
| Copias de `respaldo_local/` frente a los originales del vault y de `notas/` | 6, idénticas |
| Errores | 0 bloqueantes, 3 importantes, 13 menores |
| Sin propagar | 9 |

## Hechos comprobados y correctos

| Tema | Fuente consultada | Resultado |
|---|---|---|
| Orden del 16-11 | `git log`: `550f924` 13:25:45 (resultados de robustez), `d2d5530` 14:21:14 (registro de la ampliación), `8beb675` 14:25:57 (enmienda) | Coincide en CI, RD 6.6, EN y LOOP |
| El informe de robustez de las 13:25 ya traía el +0,038 | `git show 550f924:resultados/cierre_robustez_41p_16-11-2026/INFORME.md`; `resultados.csv`: 0,03787 [0,00649; 0,06806], p Holm 0,04264 | +0,038 [+0,006; +0,068], p Holm 0,043: correcto |
| Mismas personas y mismos ocho grupos | `folds_main` (robustez) y `folds` (ampliación) en los dos `protocolo.json` | Idénticos. Semilla del placebo distinta (20261117 y 20261118), como dice la nota de RD 6.6 |
| El protocolo del +0,046 se fijó antes de sus predicciones | Enmienda: protocolo 16-11 14:25; predicciones 18-11 21:39 | Correcto |
| Qué iguala el placebo | `placebo_hist` (`cierre_robustez_41p.py`) y `lag_index` (`ampliacion_41p.py`): sorteo entre las ventanas de la misma persona de otros segmentos, sin restricción de tiempo; `placebo_indices` (`reapertura_41p.py`): a 150 s o más, "antes o después" | "Iguala la persona y el largo; no iguala el estímulo ni la cercanía en la sesión; anteriores o posteriores": correcto. En ningún documento quedó "no controla" |
| +0,049 [+0,027; +0,072] y +0,005 [−0,025; +0,035] | `reapertura_fase3_41p_22-11-2026/descriptivos.csv`, activación, estrato estímulo: 0,04943 [0,02733; 0,07235] y 0,00460 [−0,02549; 0,03514] | Correcto |
| Atención dentro de un mismo estímulo | Mismo CSV: 0,68356 [0,66713; 0,69956]; todas, 0,68297; mismo minuto, 0,67480 [0,66009; 0,68936]. Fracción de pares (fase 2): 0,0220 | 0,684 [0,667; 0,700]; 0,683; 0,675 [0,660; 0,689]; cerca del 2 %: correcto. El estrato es el segmento (persona y presentación), como define RD 6.3 |
| Nulo de atención con posición | `confirmatorio.csv`, Q1: 0,00142; IC 95 % [−0,00180; 0,00470]; IC 90 % [−0,00130; 0,00415] | +0,001 [−0,002; +0,005] es el de 95 %, y así lo dicen EN y LOOP. El límite superior completo (0,00470) es menor que 0,005: "cualquier margen de 0,005 o más" se sostiene. La regla registrada usa el de 90 %, más estrecho |
| "Alta" en el *Attention Score* | `reconstruir_profesor_atencion_binaria.py`: columnas tiempo total, duración media, dispersión, recorrido y pupila; `DIRECTIONS = [1, 1, −1, −1, 1]`; logaritmo en las cuatro oculares. `profesor_final.joblib`: signo +1; pesos 0,398; 0,508; 0,520; 0,557; −0,052; varianza 51,5 % | La frase de RD 6.1, CI, EN 41 y PE 27 describe bien cada signo: fijaciones con su signo, dispersión y recorrido invertidos, "mirada más quieta". Haber descartado la propuesta del lector fue correcto |
| Intervalos | `cierre_final_41p.py`, `ci`: cuantiles de 20.000 medias, semilla 20261029; los demás scripts llaman a `F.ci` | "*Bootstrap* percentil, misma semilla": correcto |
| Límites inferiores 0,021; 0,023; 0,018 | CSV: 0,0212; 0,0233; 0,018 | Correcto |
| Familias de Holm | Protocolos: "Holm sobre los dos principales" (16-11) y "sobre las 4 pruebas (2 contrastes × 2 tareas)" (22-11) | Correcto |
| 40 personas en la curva | Protocolo de la reapertura ("una persona con 26 filas etiquetadas no tiene ninguna… contado antes de correr"); predicciones: falta P4 | Correcto |
| Límites de la curva y del control de sesión | `reapertura_41p_22-11-2026/INFORME.md`, límites: 16–36 %, 30–44 %, "P2 solo corrige la tendencia de sesión común a las personas" | Copiados sin cambio de sentido |
| Adaptación a la persona | `enfoques_41p.py` (`calibration_split`; AUC si hay dos clases); INFORME ("contienen información del resto de la sesión"; "n = 40"; 30/40) | Correcto. "Condiciona" es más prudente que el "fija" que proponía el lector |
| "Efecto relevante" contra 0,5 | `e2_confirmatorio.csv`: B2 0,0452 [0,0299; 0,0617]; B3 +0,0021 | 0,545 y +0,002: correcto. L3 (7.9) y C1 (7.11) son pruebas contra 0,5 |
| 79 % de segmentos con una sola etiqueta; mediana de tres ventanas | INFORME de enfoques | Correcto |
| 22.176 ventanas de atención | `cobertura_atencion.json` | Correcto |
| Desfase 0,28 y 0,48 s | `montaje_ocular_41p_23-11-2026/personas.csv`, parpadeo: medianas 0,280 (19 personas) y 0,480 (22) | Correcto |
| Límite de R1 sin dos personas | `ronda6/registro.csv`: 0,0201 con la semilla registrada; 0,0197 a 0,0202 con otras 30 | "En torno a 0,020 (entre 0,0197 y 0,0202…)": correcto |
| 0,522 en 32 personas; 0,518 con las 41 | `ronda6/registro.csv`: 0,5224 y 0,5175 | Correcto |
| Remisiones a secciones | Encabezados de RD, SP, MI y CI | Todas existen (RD 6.1 a 6.6, 7.1 a 7.3, 7.7, 7.9, 7.11, 8.1, 8.2, 8.4, 8.7 a 8.9; SP 4.3 y 4.8.3; CO 9.7) |

## Errores

| N.º | Archivo | Texto exacto actual | Por qué está mal (fuente) | Texto exacto corregido | Gravedad |
|---|---|---|---|---|---|
| 1 | EN, pregunta 10 | `Hay dos grupos de desfase, uno cerca de 0,27 s (P2 a P21, P36 y P37) y otro cerca de 0,47 s` | La corrección 0,27 → 0,28 y 0,47 → 0,48 se aplicó en RD, SP y CI, pero no aquí. `personas.csv`: medianas del parpadeo 0,280 y 0,480 | `Hay dos grupos de desfase, uno cerca de 0,28 s (P2 a P21, P36 y P37) y otro cerca de 0,48 s` | Importante |
| 2 | EN, guion de la lámina 30 | `Y el orden de las ventanas no aportó.` | Antes decía "no aportó de forma demostrable"; el recorte afirma ausencia. En activación el contraste del orden es inconcluso (+0,020 [−0,017; +0,057]; RD 8.1, "No demostrado") | `Y el orden de las ventanas no mostró aporte.` (quedan 112 palabras en 45 s: 149 por minuto) | Importante |
| 3 | CO 9.7 | `el efecto es pequeño y desigual entre personas, no se separó de pertenecer al mismo estímulo ni del soporte temporal de la etiqueta, sus controles quedaron inconclusos y requiere confirmación en una cohorte nueva.` | El texto anterior atribuía la desigualdad al "contraste simple entre el modelo con y sin historial" (mediana +0,014; 23 de 41). La frase nueva la extiende a la evidencia acotada, que es el contraste contra placebo (28 de 41), y EN 17 dice que ese contraste "es más parejo" | `el efecto es pequeño, no se separó de pertenecer al mismo estímulo ni del soporte temporal de la etiqueta, sus controles quedaron inconclusos y requiere confirmación en una cohorte nueva; el contraste simple entre el modelo con y sin historial es además desigual entre personas.` | Importante |
| 4 | EN, pregunta 4 (segundo "Si repreguntan") | `registré la ampliación a las 14:21 y su enmienda a las 14:25, menos de una hora después, con` | De 13:25:45 a 14:25:57 hay 60 min 12 s; la enmienda es la que fija el +0,046 | `registré la ampliación a las 14:21 y su enmienda a las 14:25, cerca de una hora después, con` | Menor |
| 5 | EN, encabezado | `se corrigieron once respuestas (2, 4, 6, 7, 13, 14, 16, 21, 22, 28 y 34)` | El diff también cambia la respuesta 15 (el signo de cada variable) | `se corrigieron doce respuestas (2, 4, 6, 7, 13, 14, 15, 16, 21, 22, 28 y 34)` | Menor |
| 6 | EN, pregunta 44 | `no es utilizable en línea ni comparable con los demás contrastes. Además` | La introducción de la sección dice que 19 y 44 "se remiten entre sí", y ninguna cita a la otra | `no es utilizable en línea ni comparable con los demás contrastes (pregunta 19). Además` (quedan 68 palabras) | Menor |
| 7 | EN, pregunta 45 (enunciado) | `**45. Los objetivos pedían BA, macro-F1 y *recall*. ¿Por qué decide con AUC, y qué dicen las otras?**` | Los objetivos de `Estructura Tesis.md` no nombran métricas; el compromiso está en "Metodología KDD" (SP 4.8.3, nota; PE 14). La respuesta acepta la premisa | `**45. La metodología comprometía BA, macro-F1 y *recall*. ¿Por qué decide con AUC, y qué dicen las otras?**` | Menor |
| 8 | EN, pregunta 6 (segundo "Si repreguntan") | `frente a los 0,181 que el modelo tiene sobre el azar` | 0,181 es el modelo solo con EEG (B1). El contraste citado usa el modelo con EEG y GSR, que sin historial tiene 0,683 (`descriptivos.csv` de la fase 3) | `frente a los 0,183 que el modelo sin historial tiene sobre el azar` | Menor |
| 9 | EN, pregunta 22 (`Corta:`) | `La hizo un asistente automático de inteligencia artificial, a pedido mío` | La regla del ensayo pide que la versión corta use solo frases de la respuesta completa, que dice "un asistente automático" | `La hizo un asistente automático, a pedido mío` | Menor |
| 10 | EN, tabla final | `\| — \| Ninguna diferencia conocida. La de la lámina 12 (el eje decía "OOF") se corrigió en `estilo_tecnico.py` \| — \|` | La fila siguiente (lámina 31) es una diferencia conocida: las dos filas se contradicen | `\| — \| Ninguna diferencia conocida entre este ensayo y `relato.py`. La de la lámina 12 (el eje decía "OOF") se corrigió en `estilo_tecnico.py` \| — \|` | Menor |
| 11 | EN, guion de la lámina 30 (rótulo) | `**Lámina 30 · Conclusiones: apoyo parcial (45 s).**` | El título cambió para marcar que el encuadre es provisorio, y el rótulo del guion lo perdió. Las dos tablas de tiempo sí lo tienen | `**Lámina 30 · Conclusiones provisorias: apoyo parcial (45 s).**` | Menor |
| 12 | LOOP, ronda 5 | `en las mismas personas y particiones` | La ampliación usa una partición (ocho grupos), la misma del análisis de robustez; RD y CI dicen "la misma partición" | `en las mismas personas y la misma partición` | Menor |
| 13 | RD 8.5, "Escala temporal" | `Este argumento vale para la parte fásica, que pesa poco en la etiqueta usada: el *Arousal Score* es, en lo esencial, el nivel tónico (sección 6.1), que se obtiene con un filtro pasa-bajos de 0,05 Hz, es decir, que cambia en decenas de segundos, y que mira hacia atrás y hacia adelante.` | Se borró la frase que contenía el argumento, y "este argumento" quedó sin antecedente. Además, el que mira hacia atrás y hacia adelante es el filtro, no el nivel | `Esa latencia describe la parte fásica, que pesa poco en la etiqueta usada: el *Arousal Score* es, en lo esencial, el nivel tónico (sección 6.1), que se obtiene con un filtro pasa-bajos de 0,05 Hz aplicado hacia atrás y hacia adelante y cambia en decenas de segundos.` | Menor |
| 14 | RD 6.5 | `"Confirmatorio" designa aquí la familia de contrastes fijada antes de correr dentro de un análisis dirigido; no designa una confirmación independiente.` | RD 7.1 cambió "familia confirmatoria" por "familia fijada de antemano": la palabra que aquí se define ya no aparece en el texto | `Una familia de contrastes "fijada de antemano" es la que se fijó antes de correr dentro de un análisis dirigido; no designa una confirmación independiente.` | Menor |
| 15 | PE, encabezado | `No agrega pendientes nuevos ni resuelve ninguno: dice qué falta y en qué documento está el detalle.` | La sección J se titula "Pendientes agregados el 27-11-2026" | `No resuelve ninguno: dice qué falta y en qué documento está el detalle. La sección J, agregada el 27-11-2026, reúne los pendientes que salieron de la segunda lectura crítica.` | Menor |
| 16 | `crear_presentacion.py` (genera `LEEME.md`) | `texto corregido el 26 de noviembre de 2026` | `relato.py` cambió el 27-11 | `texto corregido el 27 de noviembre de 2026` (y regenerar) | Menor |

## Sin propagar

1. **SP 4.5.2, "Límites".** Sigue diciendo "0,522 del número y de la prominencia de las SCR" sin la precisión de las 32 personas que RD 6.1 sí recibió.
2. **SP 4.5.2, misma frase.** "No se aplicó un desfase para compensar la latencia de las SCR (1 a 5 s); el contexto de 6 s cumple esa función de forma aproximada": es el argumento de latencia que RD 8.5, RD 8.7, la lámina 28 y EN 7 ya moderaron, porque la etiqueta es nivel tónico.
3. **Lámina 29 (RE y guion de EN).** "+0,046 sobre el placebo en el contraste registrado" no recibió ninguna de las dos reservas nuevas. En la versión de 10 minutos la lámina 30 se salta "cubierta por la lámina 29", y la fila 21 de esa tabla conserva "en activación no", sin "con un placebo que viene de otras páginas" que sí tiene la tabla de 20 minutos.
4. **Lámina 32 (RE).** El pie lista cuatro experimentos opcionales; CI, MI y PE listan ahora seis.
5. **Lámina 33 (RE) y guion de EN.** "Apoyo parcial más una advertencia metodológica": PE 53 y la tabla final de EN solo anotan la lámina 31.
6. **Diferencias con los informes, sin nota.** CI y EN dicen que para las cifras mandan los informes y los CSV; el INFORME del montaje dice 0,27 y 0,47, y el de la red, 0,0199. Falta una nota de trabajo en RD 7.8 y 7.10 que diga que el valor vigente sale de `personas.csv` y de `ronda6/registro.csv`.
7. **PE 44 y PE 47.** "Evaluación dejando grupos completos fuera" quedó en los dos.
8. **Frontera de lo dirigido.** CI ("Todo lo posterior al 16-11 es exploratorio o dirigido") y CO 9.5 ("los análisis posteriores al 16-11-2026") fechan la frontera después del 16-11; la ampliación del 16-11 se rotula ahora como dirigida.
9. **RD 6.6, fila "Robustez".** Sigue como "Registrado". Se registró a las 12:47, después del resultado principal de las 11:56: con el criterio que el párrafo nuevo invoca, también es un análisis motivado por un resultado visto. RD 6.5 conserva además "enmiendas registradas antes de ver resultados" para la enmienda del historial desplazado. No es un error del commit; lo deja a la vista.

## Equilibrio

- **Ninguna salvedad nueva está redactada con más fuerza que su fuente**, salvo los errores 2 y 3. "No iguala", "no separa", "no se demostró" y "condiciona" corresponden a lo que permiten el código y los CSV.
- **MI, "Lo que se presenta en una frase".** La frase lleva ahora cinco salvedades en dos párrafos. Se entiende, pero es el pasaje más cargado; convendría una sola lista de cinco.
- **CO 9.7.** Una oración con cinco límites encadenados. Se entiende qué se afirma (evidencia acotada sobre un resumen del historial reciente); el error 3 la aligera.
- **Nota de la lámina 23 (RE).** Tres "Ojo" en una nota. El guion de EN los reduce a "dos reservas" y queda claro.
- **RD 8.4.** El párrafo del segundo límite se lee bien y termina en lo que no se calculó.
- **Resultados firmes.** El nulo de atención que no depende del margen y la detección dentro de un mismo estímulo quedaron dichos una vez en cada documento, sin cautelas de más.

## Presentación

| Comprobación | Resultado |
|---|---|
| Regeneración en copia temporal | `GUIÓN.md`, `index.html`, `FUENTES.md` y `LEEME.md` idénticos a los del repositorio |
| Títulos de las dos tablas de tiempo de EN frente a `GUIÓN.md` | 33 de 33 iguales en cada tabla |
| Rótulos del guion hablado | Abreviados por convención anterior; solo el de la lámina 30 quedó atrasado (error 11) |
| Plan de 20 minutos | 1.200 s; subtotales 195, 130, 125, 280, 220 y 250: correctos |
| Plan de 10 minutos | 600 s; 17 láminas mostradas y 16 saltadas; subtotales 145, 50, 155, 100 y 150: correctos |
| Ritmo del guion hablado | Máximo 150 palabras por minuto (láminas 31 y 33); ninguna lo supera |
| Preguntas | 49, numeradas de corrido |
| Respuestas `Corta:` | 25; la más larga tiene 70 palabras |
| Preguntas 38 a 49 | A lo más 70 palabras cada una |
| Referencias cruzadas | "Pregunta N" y "lámina N" apuntan al contenido correcto; falta la de 19 y 44 (error 6) |

## Reglas del proyecto

- Nada afirma aprobación del profesor guía. Las siete decisiones siguen abiertas: la tabla de tres lecturas de MI dice "sin decidir", y el título de la lámina 30 pasó a "provisorias".
- El diff no toca `Estructura Tesis.md`, ni INFORME, CSV, protocolos o scripts de `resultados/` y `scripts/`.
- No hay archivos nuevos en `resultados/`; el árbol de trabajo está limpio.
- Vocabulario: "respaldo" solo como rótulo de la regla, "apoyo parcial" para la hipótesis, "evidencia acotada", "cerca de un tercio", "*Modelo Profesor* con PCA" y "activación" se usan como corresponde en todas las líneas nuevas.
