# Auditoría independiente de código — etapas del 16 al 23-11-2026 (ronda 3)

Fecha: 26-11-2026. Versión auditada: `main` en `aef0f32`, árbol limpio.

Alcance: el código que generó las predicciones del 16 al 18-11 (sin auditoría transversal previa), más una lectura completa de los scripts del 22 y 23-11 y de los que construyen etiquetas y variables. No se editó ningún archivo existente, no se entrenó ningún modelo completo y no se escribió en `resultados/`. Los scripts de comprobación están en `comprobaciones/` y se ejecutan con `.venv/bin/python cNN_*.py`.

Ajustes hechos, todos de un solo fold y en memoria: fold 0 del análisis final (HGB sin historial y con historial en ambas tareas, GRU de una ventana en activación) y el mismo fold de activación con 7 hojas.

## Resumen

**No hay fuga entre personas ni fuga directa de la etiqueta a las entradas.** Las particiones, el preprocesamiento por fold, los pesos, el historial, la posición, los placebos, la igualdad de filas entre modelos pareados, el bootstrap, la permutación de signos, Holm y las reglas de decisión hacen lo que dicen los protocolos. El fold 0 del análisis final se reproduce bit a bit.

Cuatro hallazgos pueden afectar una cifra o una conclusión. Ninguno invalida una cifra publicada; los cuatro se resuelven declarándolos, y solo H1 admite además una corrida de sensibilidad, que es decisión del autor.

| # | Hallazgo | Afecta a | Resolución |
|---|---|---|---|
| H1 | Las 15 hojas de activación se eligieron con las 25 personas de entrenamiento y la elección la decidió el modelo con historial; esas 25 personas se evalúan después en los análisis de 41 | Contraste principal de activación (16-11, P1, P2, Q1, explicativo) | Declarar. Sensibilidad opcional: decisión del autor |
| H2 | La etiqueta de activación es, en la práctica, el nivel tónico del GSR, y su soporte temporal real excede los 6 s nominales hacia el pasado y el futuro | Lectura de "historial sin los 6 s de la etiqueta" y de la banda de 6 s | Declarar y corregir dos frases |
| H3 | En el profesor PCA la pupila pesa −0,05: la etiqueta de atención es solo conducta de mirada | Descripción de la etiqueta ("mirada y pupila") y decisión 7 con el profesor guía | Declarar |
| H4 | Las variables de fijación suman la duración completa de las fijaciones que tocan la ventana: el 28 % de las ventanas etiquetadas supera los 2 s | Soporte temporal de la etiqueta de atención | Declarar |

Recuento del resto: 14 hallazgos menores (sección 4) y 7 hallazgos ya conocidos revisados, ninguno más grave de lo declarado salvo el filtro tónico, que pasa a H2 (sección 5).

## 1. Veredicto por script

| Script | Veredicto | Detalle |
|---|---|---|
| `cierre_experimental_v3.py` | Hallazgo que puede afectar una cifra o conclusión | H1. Menores M1, M2 |
| `cierre_final_41p.py` | Hallazgo que puede afectar una cifra o conclusión | Hereda H1. Menores M3, M4 |
| `cierre_robustez_41p.py` | Hallazgos menores | M5, M6 |
| `ampliacion_41p.py` y `ampliacion_e1_lag6.py` | Hallazgo que puede afectar una conclusión | H2. Menores M7, M8 |
| `explicativo_posicion_41p.py` | Hallazgos menores | Hereda H1 en activación. M9 |
| `reapertura_41p.py` | Hallazgo que puede afectar una conclusión | H1 (P1, P2) y H2 (banda de 6 s). Menores M3, M10 |
| `reapertura_fase2_41p.py`, `reapertura_posthoc_estratos.py` | Hallazgos menores | M3 |
| `reapertura_fase3_41p.py` | Hallazgos menores | Hereda H1 (Q1 de activación). M9 |
| `enfoques_41p.py` | Hallazgos menores | M3, M11 |
| `limpieza_ocular_41p.py` | Sin hallazgos nuevos | Límites ya declarados |
| `red_cruda_41p.py` | Sin hallazgos nuevos | Límites ya declarados |
| `reconstruir_etiquetas_gsr_calidad_v2.py` | Hallazgo que puede afectar una conclusión | H2. El script hace lo que su protocolo dice |
| `reconstruir_profesor_atencion_binaria.py` y `label_with_teacher` | Hallazgo que puede afectar una conclusión | H3 |
| `preprocesamiento_secuencial.py` | Hallazgo que puede afectar una conclusión | H2 (filtro tónico) y H4 (fijaciones). Menor M12 |
| `eeg_por_canal_v2.py` | Sin hallazgos | Filtros dentro de la ventana; ZIP verificado contra el manifiesto |
| `preparar_modelado.py` | Sin hallazgos | Partición determinista por persona; sus etiquetas ternarias no se usan en estas etapas |
| `temporales_core.py` (`history_indices`, `preprocessor`) | Sin hallazgos | Menor M13 |
| `cache_crudos_ocular.py` | Hallazgos menores | M14 |

## 2. Lo que se comprobó y pasa

### Fuga entre personas (`c01`, `c05`, `c06`)

- Las 9 particiones de 8 grupos (análisis final, 3 de robustez, 5 de reapertura) cubren a las 41 personas exactamente una vez. `F.folds()` regenera la partición registrada.
- Los 5 folds de V3 están dentro de las 25 personas de entrenamiento; la validación interna queda dentro del ajuste de cada fold.
- En todas las predicciones del 16 al 18-11, el grupo guardado de cada persona coincide con el protocolo (0 filas distintas).
- Imputación, indicadores de faltantes y escalado se ajustan con las filas etiquetadas del fold de ajuste (`cierre_final_41p.py:94`, `cierre_robustez_41p.py:98`, `ampliacion_41p.py:207`, `explicativo_posicion_41p.py:50`, `reapertura_41p.py:183`, `cierre_experimental_v3.py:264`).
- Pesos (`cierre_experimental_v3.py:98-100`): en el fold 0 cada persona suma lo mismo (296,0 en activación; 545,2 en atención) y las dos clases suman igual.
- V3: las 16 personas externas no aparecen en el OOF y los modelos finales se ajustan con las 25 de entrenamiento.

### Fuga de la etiqueta a las entradas (`c01`, `c02`)

- Atención: 360 columnas, todas `eeg_*`, `eegchNN_*`, `eegsp_*` o `gsr_*`. Ninguna de mirada, fijación, sacada o pupila.
- Activación: 367 columnas, EEG más 10 de mirada y 6 de pupila. Ninguna de GSR.
- AUC de cada columna sola dentro de cada persona:
  - Activación: ninguna columna no-EEG se aleja más de 0,033 de 0,5. Las de mayor desvío son `rail_fraction` de canales que solo varían en 1 a 4 personas.
  - Atención: las más informativas son potencia delta/theta y varianza de los canales 9, 1, 13, 11 y 0 (AUC 0,37 a 0,39, con el mismo signo en todas las personas con el canal utilizable, 38 a 40). Es la firma ocular ya declarada.
- Los indicadores de faltantes no predicen la etiqueta (máximo desvío 0,042, en 12 personas).
- `pupil_both_valid_fraction`: el GSR aporta 30 filas constantes por ventana, así que la variable no codifica el valor del GSR. AUC sola contra activación 0,513. No es más grave de lo declarado.

### Historial, posición y controles (`c01`)

- El historial hasta 32 usa solo ventanas del mismo segmento, nunca posteriores, con antigüedad máxima de 31 s, y termina en la ventana actual. No hay huecos dentro de ninguno de los 3.714 segmentos.
- La posición coincide con `min(window_index + 1, 32)` en las 22.211 filas. Se satura en 32 en el 0,8 % de las filas etiquetadas de atención y el 1,6 % de activación.
- Placebo R1: mismo largo, misma persona, siempre otro segmento.
- Historial desplazado: todas las ventanas quedan a 5 s o más (6 en la enmienda) de la actual.
- Las filas son idénticas y están en el mismo orden entre todos los modelos pareados, y las etiquetas guardadas coinciden con las vigentes. En R2 el 0,8 % de las etiquetas cambia al reajustar el profesor por fold, como corresponde.

### Evaluación (`c06`)

- Ninguna combinación persona-estrategia tiene una sola clase en las predicciones del 16 al 18-11.
- Donde una persona queda sin AUC se declara: 40 personas en la curva de activación y en E4c de activación. En E3 y E4 ninguna persona tiene AUC en solo algunas de las 5 particiones.
- Bootstrap por persona, permutación de signos bilateral con corrección +1 y Holm descendente están bien implementados. Las familias de Holm coinciden con las declaradas en las 12 etapas.
- Las decisiones de los 12 CSV se reproducen con `F.decide`.

### Reproducibilidad (`c05`)

- Fold 0 del análisis final reentrenado con el código del repositorio: diferencia máxima de probabilidad 0,00 en HGB sin historial y con historial (ambas tareas) y en GRU de una ventana (activación).
- Los hashes de hoy del TSV de Tobii y del ZIP de EEG coinciden con `manifiesto_ejecucion.json`, y el hash de `preprocesamiento_secuencial.py` coincide con el `pipeline_sha256` registrado.
- Las tablas de entrada de `resultados/` están versionadas y con hash en cada protocolo.

## 3. Hallazgos que pueden afectar una cifra o una conclusión

### H1. La configuración de activación se eligió con el modelo con historial, sobre personas que después se evalúan

**Evidencia.**

- `cierre_experimental_v3.py:314-321` elige las hojas por la AUC media sobre los contextos 1, 8 y 32. La línea 334 fija el valor final con la media de todos los folds.
- `cierre_final_41p.py:32` congela 15 hojas para activación y evalúa a las 41 personas, 25 de las cuales son las de esa búsqueda.
- En `busqueda_interna_activacion.csv` la elección la decide el contexto 32:

| Contexto | 7 hojas | 15 hojas |
|---|---|---|
| 1 | 0,5123 | 0,5121 |
| 8 | 0,5341 | 0,5311 |
| 32 | 0,4994 | 0,5311 |
| Media (criterio) | 0,5152 | 0,5248 |

- En esa búsqueda, historial − sin historial vale −0,013 con 7 hojas y +0,019 con 15. Se congeló la configuración en la que el historial gana.
- En atención la elección no importa: +0,0135 con 7 hojas y +0,0124 con 15.

**Qué podría afectar y en qué sentido.** Todos los contrastes de activación entre un HGB con historial hasta 32 y uno sin historial: principal del 16-11, P1, P2, Q1 y el explicativo. El sesgo posible es a favor del historial y recae en las 25 personas de la búsqueda. Separando las predicciones guardadas por grupo (`c07`):

| Contraste de activación | 41 | 25 de la búsqueda | 16 restantes |
|---|---|---|---|
| Principal 16-11 | +0,034 | +0,055 [+0,012; +0,101] | +0,001 [−0,052; +0,055] |
| P1 (5 particiones) | +0,036 | +0,046 [+0,012; +0,086] | +0,021 [−0,017; +0,060] |
| P2 con tiempo de sesión | +0,026 | +0,050 [+0,013; +0,085] | −0,011 [−0,066; +0,038] |
| Q1 con posición | +0,032 | +0,049 [+0,018; +0,081] | +0,006 [−0,043; +0,049] |
| Explicativo, historial − posición | +0,038 | +0,063 [+0,021; +0,109] | −0,001 [−0,056; +0,054] |
| Historial desplazado 6 − placebo | +0,046 | +0,035 [+0,003; +0,064] | +0,064 [+0,015; +0,115] |
| Banda de 6 s − placebo | +0,047 | +0,058 [+0,015; +0,101] | +0,030 [−0,003; +0,068] |
| GRU 32 − GRU 1 (sin búsqueda) | +0,051 | +0,045 [+0,007; +0,083] | +0,059 [+0,014; +0,102] |

Los contrastes del HGB con historial hasta 32 se concentran en las 25 personas de la búsqueda. Los que no dependen de esa elección de la misma forma (GRU sin búsqueda, historial desplazado frente a placebo) son positivos en ambos grupos.

**Evidencia en contra de que el sesgo sea grande.**

- En V3, con modelos ajustados solo con las 25, el mismo contraste fue +0,059 en validación y +0,033 en test, con 8 personas cada uno e intervalos que incluyen el cero.
- El OOF de entrenamiento de V3, con selección anidada por fold, dio +0,016 [−0,036; +0,070].
- La diferencia entre grupos no es significativa con 16 personas.
- Diagnóstico de un fold (`c08`, 6 personas, no es un resultado): +0,029 con 7 hojas y +0,057 con 15.

**Lectura.** El riesgo es de diseño y está sin declarar. La frase "configuración elegida solo con train" es cierta, pero no implica independencia cuando esas 25 personas son 25 de las 41 evaluadas y el criterio incluyó al modelo con historial. La heterogeneidad por grupo ya estaba en el informe del 16-11, sin vincularla a la selección. No cambia la conclusión general del cierre (apoyo parcial, con el sostén más sólido en el historial desplazado frente al placebo), pero debilita el "respaldo" de P1.

**Resolución.** Declararlo como límite junto a P1. Una sensibilidad con 7 hojas o con selección anidada lo resolvería; requiere volver a correr y es decisión del autor.

### H2. La etiqueta de activación es el nivel tónico del GSR y su soporte real excede los 6 s

**Evidencia.**

- `preprocesamiento_secuencial.py:119-127`: z del GSR con toda la grabación y componente tónica con Butterworth de orden 2 a 0,05 Hz aplicado con `filtfilt`.
- `reconstruir_etiquetas_gsr_calidad_v2.py:28-42`: promedio de cuatro componentes y media de 5 ventanas.
- `c03`, núcleo del filtro: el 25 % de su masa está a más de 5 s del centro y el 6,5 % a más de 10 s.
- `c03`, peso del GSR sobre la parte tónica de la etiqueta de la ventana t: 49 % dentro de [t−4, t+2), 25 % antes de t−4 y 25 % después de t+2. Antes de t−10 queda el 3,7 %.
- AUC de cada componente de la misma ventana contra la etiqueta, por persona: tónico 0,911, `gsr_mean_z` 0,921, fásico 0,595, número y prominencia de respuestas 0,522.
- AUC de `gsr_mean_z` desplazado contra la etiqueta en t: 0,87 a −6 s, 0,85 a −12 s, 0,80 a −30 s, 0,86 a +8 s y 0,76 a +30 s.

**Qué podría afectar.** Ninguna cifra, y no es fuga: el GSR no entra en activación. Afecta tres lecturas:

1. "Historial sin tocar los 6 s que definen la etiqueta" (E1 con desplazamiento 6, +0,046) y "son contiguas, sin solapamiento" (banda de 6 s, límites del informe del 22-11). Las entradas en [t−31, t−4) coinciden en el tiempo con GSR que pesa cerca de un cuarto en la componente dominante de la etiqueta. El informe del 22-11 dejó escrito "no se verificó si los filtros del GSR aguas arriba tienen un soporte más largo": lo tienen.
2. La etiqueta en t incluye GSR hasta unos 10 s después de t. Parte de la tarea es anticipar el GSR inmediato.
3. D2 (etiqueta de 6 s antes, AUC 0,680) subestima la persistencia: el GSR continuo de 30 s antes da 0,80. D2 se recalculó de forma independiente y coincide (0,680 y 0,535; `c04`). La etiqueta binaria cambia cerca de la mediana, no el estado.

**Sentido.** Refuerza la lectura prudente que el cierre ya hace: el historial estima mejor un estado lento. Debilita la frase "más allá del soporte de la etiqueta".

**Resolución.** Declarar. Sustituir "sin solapamiento" por el soporte real y describir la etiqueta como nivel tónico relativo a la sesión. No requiere correr nada.

### H3. En el profesor PCA la pupila no pesa

**Evidencia.** `profesor_final.joblib`, usado por `cierre_experimental_v3.py:89-90` (`c09`):

| Componente | Peso orientado | AUC del componente solo contra la etiqueta |
|---|---|---|
| Recorrido de la mirada | 0,557 | 0,934 |
| Dispersión | 0,520 | 0,877 |
| Duración media de fijación | 0,508 | 0,852 |
| Tiempo total de fijación | 0,398 | 0,835 |
| Pupila | −0,052 | 0,435 |

`reconstruir_profesor_atencion_binaria.py:14` declara dirección positiva para la pupila. El componente explica el 51,5 % de la varianza.

**Qué podría afectar.** Ninguna cifra. La etiqueta se describe como "mirada y pupila", pero es conducta oculomotora, y la pupila va levemente en contra. Refuerza la lectura de huella ocular en el EEG y es un dato para la decisión 7 (PCA frente a fusión igualitaria). No encontré esto declarado en el cierre ni en `Profesor_Binario_Reconstruido_29-10-2026.md`.

**Resolución.** Declarar.

### H4. Las fijaciones se suman con su duración completa

**Evidencia.** `preprocesamiento_secuencial.py:204-212` toma `Gaze event duration` de cada fijación que toca la ventana, sin recortarla. En las ventanas etiquetadas (`c09`): `fixation_total_ms` supera 2.000 ms en el 27,7 % y 3.000 ms en el 4,0 %; percentil 99 de 4.430 ms, máximo 11.365 ms.

**Qué podría afectar.** Ninguna cifra, y no es fuga: la mirada no entra en atención. Dos componentes de la etiqueta de atención incluyen conducta ocular anterior y posterior a la ventana, de modo que su soporte no es de 2 s. En activación esas dos variables son entradas y arrastran hasta segundos de mirada posterior a la ventana; es menor, porque la etiqueta de activación ya incluye futuro por H2 y esas columnas solas dan AUC 0,48.

**Resolución.** Declarar junto al hallazgo conocido de la deduplicación de eventos.

## 4. Hallazgos menores

Ninguno cambia una cifra.

| # | Dónde | Hallazgo | Resolución |
|---|---|---|---|
| M1 | `cierre_experimental_v3.py:346-348` | `macro_auc` falla si una persona tiene una sola clase, en vez de omitirla. No ocurrió | Ninguna |
| M2 | `cierre_experimental_v3.py:354` | La GRU usa 3 hilos sin `use_deterministic_algorithms`. En este Mac el fold 0 se reproduce exacto; en otro equipo no está garantizado | Declarar |
| M3 | `cierre_final_41p.py:127-134` | Precedencia respaldo > inferior > nulo. El docstring y los `protocolo.json` listan nulo antes que inferior, sin fijar precedencia. Ocho filas cumplen dos reglas (lista abajo) | Ya declarado el 16-11; conviene repetirlo en el cierre |
| M4 | `cierre_final_41p.py:168-169` | Los secundarios reciben una decisión con p sin ajustar ("efecto relevante" en GRU de activación), aunque el protocolo los declara descriptivos. El informe lo redacta bien | Ninguna |
| M5 | `cierre_robustez_41p.py:67-83` | El placebo conserva el largo del historial, que es la posición. El propio proyecto lo detectó el 18-11. El 35 % de sus ventanas son posteriores a la actual y el 6 % queda a menos de 33 s | Declarado en parte |
| M6 | `cierre_robustez_41p.py:134-142` | En R2 `components()` normaliza con la sesión completa de las 41 personas; solo el PCA se reajusta por fold | Cubierto por el límite general |
| M7 | `ampliacion_41p.py:119` | Los modelos de historial desplazado reciben una columna extra con el número de ventanas desplazadas, que codifica la posición. Es igual en real y placebo, pero entra en "desplazado − sin historial" (+0,053) y no está en el informe | Declarar |
| M8 | `ampliacion_41p.py:90` | Con desplazamiento 5, el 53 % de las filas de atención y el 14 % de las de activación no tienen ventanas desplazadas; ahí real y placebo son idénticos. El informe da la cobertura con 6 | Ninguna |
| M9 | `explicativo_posicion_41p.py:45`, `reapertura_41p.py:122-124` | La posición se satura en 32. Declarado en la fase 3 | Ninguna |
| M10 | `reapertura_41p.py:148-166`, `:229` | El placebo de la curva iguala el número de ventanas de la banda de 6 s, no el de cada banda, e incluye futuro. Declarado | Ninguna |
| M11 | `enfoques_41p.py:321-327` | `mean_auc` promediaría sobre menos particiones sin avisar si una persona quedara sin AUC en alguna. No ocurre | Ninguna |
| M12 | `preprocesamiento_secuencial.py:114`, `:146` | `drop_duplicates("t_us")` en GSR y pupila conserva la primera fila con esa marca de tiempo. Al construir la pupila con todas las filas de la exportación, una fila de otro sensor con la misma marca desplazaría a la del ojo. No lo cuantifiqué | Declarar junto a `pupil_both_valid_fraction` |
| M13 | `temporales_core.py:42` | `keep_empty_features=True` más indicadores: la matriz sin historial tiene 653 columnas en activación (367 variables y 286 indicadores) y 1.959 con historial. Con 15 hojas y `min_samples_leaf=30` es mucha dimensión para unas 10.000 filas | Contexto de H1 |
| M14 | `cache_crudos_ocular.py:33-44` | Lee el TSV y el ZIP sin verificar su hash. Los `.npz` resultantes sí llevan hash en los protocolos, y hoy ambos crudos coinciden con el manifiesto | Ninguna |

Filas que cumplen dos reglas a la vez (M3). Todas cumplen también "nulo concluyente":

| Etapa | Contraste | Δ | Decisión del código |
|---|---|---|---|
| Curva temporal, atención | Banda 24 s − placebo | −0,007 | inferior (p Holm 0,16) |
| Curva temporal, atención | Banda 48 s − placebo | −0,012 | inferior |
| Curva temporal, atención | Banda 96 s − placebo | −0,010 | inferior |
| Fase 2 X1, atención | Banda 48 s − placebo de bloque | −0,012 | inferior |
| Fase 2 X1, atención | Banda 96 s − placebo de bloque | −0,009 | inferior |
| Fase 2 X2, atención | Mismo estímulo | +0,013 | respaldo |
| Enfoques E1 | A1 corregida − original | −0,008 | inferior |
| Enfoques E1 | A2 historial − sin historial (corregida) | +0,010 | respaldo |

Con la precedencia inversa las seis "inferior" serían "nulo concluyente". Ninguna está en la tabla de conclusión general salvo A1, que el cierre ya marca "al filo".

## 5. Hallazgos ya conocidos: ¿más graves de lo declarado?

| Conocido | Revisión | ¿Más grave? |
|---|---|---|
| Etiquetas y variables z con la sesión completa | Confirmado en `preprocesamiento_secuencial.py:118-119`, `:150-152`, `reconstruir_profesor_atencion_binaria.py:17-27`, `reconstruir_etiquetas_gsr_calidad_v2.py:19-51`. Son transformaciones por persona sin etiquetas de otras personas | No |
| Filtro tónico bidireccional | Su alcance (±10 s) y el dominio tónico de la etiqueta no estaban cuantificados | Sí: es H2 |
| ICA y escala por persona con toda la sesión | Sin etiquetas; solo resta información | No |
| EEG atrasado 0,18 a 0,53 s | No revisado de nuevo | No evaluado |
| `pupil_both_valid_fraction` sobre todas las filas | 30 filas de GSR constantes por ventana; AUC sola 0,513 | No |
| Deduplicación de eventos oculares | Se suma H4 (duración completa) | Algo: ver H4 |
| E1: el modelo no usa la columna de posición | No revisado de nuevo | No evaluado |

## 6. Diferencias entre código y documentos

1. "Configuración elegida solo con train" no menciona que el criterio incluyó al modelo con historial ni que esas personas se evalúan después (H1).
2. "Sin solapamiento con la etiqueta" y "contiguas, sin solapamiento" valen para el soporte nominal, no para el real (H2).
3. Etiqueta de atención "con mirada y pupila": la pupila pesa −0,05 (H3).
4. Precedencia de reglas distinta del orden en que se listan (M3).
5. Decisión asignada a secundarios declarados descriptivos (M4).
6. Columna de número de ventanas en los modelos desplazados, sin declarar (M7).

No encontré ninguna diferencia en la que el código haga algo distinto de lo registrado en un contraste confirmatorio.

## 7. Qué no cubre esta auditoría

- No se reentrenó nada más que el fold 0 del análisis final. La reproducción exacta de los demás folds y etapas se infiere de que comparten funciones, no se comprobó.
- No se regeneró `caracteristicas_multimodales.csv` desde los crudos; se verificaron los hashes del script y de los crudos contra el manifiesto.
- `montaje_ocular_41p.py` no se leyó entero. `limpieza_ocular_41p.py` y `red_cruda_41p.py` se leyeron enteros, sin comprobación numérica nueva.
- H1 se apoya en predicciones guardadas y en un diagnóstico de 6 personas. No demuestra que el contraste esté inflado; demuestra que el diseño lo permite y que los datos son compatibles con ello.

## Comprobaciones

| Script | Qué hace |
|---|---|
| `c00_carga.py` | Carga común con `V3.load_data()` |
| `c01_estructura.py` | Particiones, columnas, historial, posición, placebos |
| `c02_fuga_columnas.py` | AUC por persona de cada columna sola y de cada indicador de faltantes |
| `c03_soporte_etiqueta_gsr.py` | Núcleo del filtro tónico, composición de la etiqueta, GSR desplazado |
| `c04_autocorrelacion.py` | D2 recalculado de forma independiente |
| `c05_reproducir_fold.py` | Fold 0 del análisis final frente a las predicciones guardadas |
| `c06_predicciones.py` | Integridad de predicciones, V3, reglas de decisión |
| `c07_seleccion_y_grupos.py` | Búsqueda interna de V3 y contrastes por grupo de personas |
| `c08_diagnostico_hojas.py` | Un fold de activación con 7 y 15 hojas |
| `c09_fijaciones_y_profesor.py` | Duración de fijaciones y pesos del profesor PCA |

Todos aceptan como argumento opcional la ruta de un pickle para no recargar los datos.
