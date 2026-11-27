# Cierre consolidado de la experimentación — 23-11-2026

Este documento reemplaza como referencia a `Cierre_Experimental_Final_22-11-2026.md`, que es anterior a la reapertura. Reúne todas las etapas registradas entre el 16 y el 23 de noviembre de 2026, sus decisiones, su trazabilidad y la comprobación de reproducibilidad. No contiene resultados nuevos. Ante cualquier diferencia de cifras mandan los `INFORME.md` y los CSV de cada carpeta de resultados; para las lecturas manda este documento y los borradores del 23-11, que moderan varias frases de los informes. Ajustado el 27-11-2026 a una segunda lectura crítica (`documentacion/auditoria_final_23-11-2026/ronda6/SEGUNDA_LECTURA_COMITE.md`), sin cifras ni análisis nuevos.

Estado: Mario Romero pidió este cierre el 23-11-2026. No hay aprobación del profesor guía registrada sobre estos resultados, sobre el margen práctico de 0,02 ni sobre el encuadre de la tesis. Etiqueta de Git: `cierre-experimental-2026-11-23` (anterior a la auditoría final; el texto vigente es el de `main`). Apunta a `aee6ab6`; la versión auditada es `af345a2` o posterior.

## Conclusión general

Evidencia mixta, con **apoyo parcial** a la hipótesis de temporalidad, que proviene de activación. Con el diseño original (entrenamiento, validación y test por separado), el cierre V3 del 16-11 no había mostrado una ventaja consistente en ninguna de las dos variables; el análisis con validación cruzada sobre 41 personas se registró menos de cuatro minutos después del commit de ese resultado (`005a499`, 11:35:40, y `1bbb083`, 11:39:06). El apoyo parcial depende de ese cambio de diseño y se refiere al historial reciente resumido con estadísticos, no a un modelo secuencial ni a la combinación de señales.

| Pregunta | Atención | Activación |
|---|---|---|
| ¿Mejora el modelo con historial? | Sí: +0,029 [+0,021; +0,037], efecto relevante | Sí: +0,036 [+0,010; +0,065], respaldo; concentrado en las 25 personas con que se eligió la configuración (+0,046, frente a +0,021 en las otras 16) |
| ¿La mejora proviene de la fisiología de las ventanas previas? | No. Es la posición en el estímulo: con la posición como variable el historial agrega +0,001 [−0,002; +0,005], nulo concluyente | Evidencia acotada. El historial sin las ventanas de 6 s que promedia la etiqueta supera a un placebo en +0,046 [+0,018; +0,073] (contraste registrado el 16-11, después de ver que el historial completo superaba al placebo); ese contraste no excluye el soporte del filtro tónico de la GSR, que usa toda la sesión, y su placebo proviene de otros estímulos. En la curva del 22-11 solo hay respaldo para los 6 s anteriores (+0,047 [+0,017; +0,078]; una partición, 40 personas); a 12 s es inconcluso y desde 24 s no se distingue del placebo, sin demostrar ausencia |
| ¿Queda algo al controlar la posición? | No: nulo concluyente dentro de ±0,02 | +0,032 [+0,004; +0,059], inconcluso tras Holm; dentro de un mismo estímulo, +0,009, también inconcluso |
| ¿Aporta el orden de las ventanas (GRU)? | No: +0,008 [−0,004; +0,020], y rinde 0,040 bajo el HGB | No demostrado: GRU − HGB, ambos con historial, +0,020 [−0,017; +0,057], inconcluso. La GRU con historial supera a su control de una ventana (+0,051, secundario sin corrección), lo que mide el historial y no el orden |
| ¿Qué fusión? | Tardía sobre temprana con MLP: +0,012 [+0,005; +0,021], secundario; con HGB (cierre V3) el signo es el contrario | Sin diferencias demostradas (inconcluso: +0,006 [−0,032; +0,042]) |
| ¿Qué detecta el EEG en la ventana actual? | Cerca de un tercio de la detección sobre el azar depende de componentes ligados a los ojos: 0,681, que baja a 0,621 al quitarlos (0,060 de 0,181; se lee como cota inferior; no es una demostración) | Nada demostrable: 0,524 |
| ¿Ayuda un modelo más complejo? | Red sobre la señal cruda: 0,716, +0,035 sobre el HGB; pierde 0,067 al limpiar, y su ventaja se mantiene con el EEG limpio (+0,028) | No demostrado: 0,498 frente a 0,524, inconcluso |

Las AUC son por persona. Las decisiones siguen las reglas registradas, con margen de 0,02.

## Qué queda cerrado

- No se entrenan modelos nuevos ni se agregan contrastes sobre estos datos.
- Quedan congeladas las etiquetas (atención binaria original y pseudoetiquetas GSR V2 de activación), las ventanas, las particiones por persona y la configuración de los modelos.
- La etiqueta de atención corregida por posición (22-11) existe como análisis; no reemplaza a la original mientras no se decida.
- Reabrir requiere una decisión explícita y un protocolo registrado antes de correr.

## Resultados por etapa

### 16 al 18-11 — Análisis final con 41 personas

| Etapa | Resultado principal |
|---|---|
| Cierre V3 | Configuración elegida solo con las 25 personas de entrenamiento y congelada |
| Análisis final | Historial − sin historial: atención +0,026 [+0,018; +0,035]; activación +0,034 [−0,001; +0,069] |
| Robustez | En atención un placebo de la misma persona reproduce la mejora (diferencia −0,000 [−0,003; +0,003]); en activación no (+0,038 [+0,006; +0,068]) |
| Ampliación E1–E6 y enmienda | Activación, historial sin las ventanas de 6 s que promedia la etiqueta frente a placebo: +0,046 [+0,018; +0,073]. Fusión tardía sobre temprana en atención solo entre redes MLP (+0,012, secundario sin corrección) |
| Explicativo de posición (post hoc) | En atención los segundos en el estímulo reproducen la mejora: +0,028 [+0,021; +0,035] |

### 22-11 — Reapertura

| Etapa | Resultado principal |
|---|---|
| Fase 1, registrada (5 particiones nuevas; el contraste ya se había visto el 16-11 en la partición registrada y en otras tres alternativas) | Atención +0,029 [+0,021; +0,037], efecto relevante. Activación +0,036 [+0,010; +0,065], respaldo; con tiempo de sesión en ambos modelos +0,026 [−0,006; +0,056], inconcluso |
| Fase 1, curva temporal (una partición, la registrada el 16-11; 40 personas en activación) | Activación: 6 s +0,047 [+0,017; +0,078], respaldo; 12 s +0,024, inconcluso; desde 24 s inconcluso (no se distingue del placebo ni se demuestra ausencia). Atención: nulo concluyente a 6 y 12 s |
| Fase 2, controles post hoc | El resultado no depende del tipo de placebo. Dentro del mismo minuto de sesión, activación +0,058 [+0,027; +0,092] |
| Fase 3, historial frente a posición | Atención: nulo concluyente (+0,001; dentro del estímulo −0,000). Activación: +0,032 [+0,004; +0,059], inconcluso tras Holm; dentro del estímulo +0,009, inconcluso |

### 22-11 — Cuatro enfoques

| Enfoque | Resultado principal |
|---|---|
| E1 Etiqueta de atención corregida por posición | La posición sola deja de predecir (0,504). La detección baja poco (0,675 frente a 0,683; decisión registrada "inferior", al filo). El historial queda en nulo concluyente con la posición como variable |
| E2 Detección cruzada | El EEG solo detecta la etiqueta ocular con 0,681; el GSR no le agrega nada (+0,002, nulo concluyente). Potencia lenta y amplitud 0,673; alfa y beta 0,593 |
| E3 Activación por estímulo | AUC 0,587, la más alta en activación; no supera de forma demostrable a promediar el modelo por ventana (+0,020, inconcluso) |
| E4 Diferencias entre personas | La detectabilidad de cada persona es estable dentro de la sesión (fiabilidad por mitades 0,76 y 0,66); la ganancia del historial no lo es. Adaptar el modelo a la persona mejora activación en +0,045 [+0,023; +0,069] |

### 23-11 — Qué detecta el EEG

| Etapa | Resultado principal |
|---|---|
| Montaje (descriptivo) | Los datos son compatibles con el montaje por defecto del equipo. El EEG va entre 0,18 y 0,53 s atrasado respecto del seguidor ocular; no se corrigió |
| Limpieza ocular | Quitar 3 componentes oculares (3,5 % de la varianza) baja la AUC de 0,681 a 0,621: +0,060 [+0,044; +0,075], efecto relevante. El control (72 % de la varianza) la deja en 0,674. Alfa y beta baja de 0,593 a 0,547 |
| Red sobre la señal cruda | Atención: red 0,716 frente a HGB 0,681, +0,035 [+0,023; +0,047], efecto relevante con holgura mínima. Con EEG limpio 0,649 frente a 0,621. Activación: 0,498 frente a 0,524, inconcluso |

## Trazabilidad

Cada etapa con protocolo entró a Git antes que sus predicciones (orden de commits verificado; que se publicara antes de correr no es verificable desde el repositorio) y se ejecutó una vez. Salvedades: la versión 1 del cierre V3 se detuvo en el primer fold de entrenamiento por una auditoría de código y se conserva en `cierre_v3_16-11-2026_abortado_fusion`; la enmienda E1 se registró el 16-11 y se corrió el 18-11; la fase 2 se registró con la fase 1 en marcha y es post hoc. La ampliación E1–E6 se registró a las 14:21:14 del 16-11 (`d2d5530`) y su enmienda a las 14:25:57 (`8beb675`), después del commit de resultados de la robustez (`550f924`, 13:25:45), cuyo informe ya mostraba que en activación el historial completo superaba al placebo (+0,038, p Holm 0,043). Usa las mismas 41 personas y la misma partición (los ocho grupos de los dos `protocolo.json` son idénticos): es un análisis dirigido por ese resultado, como el explicativo de posición, y no una evidencia independiente.

| Etapa | Carpeta en `resultados/` | Registro | Enmienda previa a resultados | Resultados | Auditoría de resultados |
|---|---|---|---|---|---|
| Cierre V3 | `cierre_v3_16-11-2026` | `dfbd93d` | `82affdb` | `005a499` | en la carpeta |
| Análisis final | `cierre_final_41p_16-11-2026` | `1bbb083` | — | `7435fec` | — |
| Robustez | `cierre_robustez_41p_16-11-2026` | `6447236` | — | `550f924` | — |
| Ampliación E1–E6 | `ampliacion_41p_16-11-2026` | `d2d5530` | `8beb675` | `8c7a6d4` | — |
| Explicativo de posición | `explicativo_posicion_41p_18-11-2026` | `b3eacdc` | — | `8c7a6d4` | — |
| Reapertura, fase 1 | `reapertura_41p_22-11-2026` | `5076307` | — | `99630ed` | `617afb1` |
| Reapertura, fase 2 | `reapertura_fase2_41p_22-11-2026` | `e3d9c71` | — | `99630ed` | `617afb1` |
| Reapertura, fase 3 | `reapertura_fase3_41p_22-11-2026` | `7046d92` | — | `9ce5745` | `9ec22b0` |
| Cuatro enfoques | `enfoques_41p_22-11-2026` | `cd25134` | `4a4798c` | `5f806df` | `e8d6add` |
| Montaje | `montaje_ocular_41p_23-11-2026` | descriptivo | — | `06547f5` (CSV), `441bae9` (informe) | — |
| Limpieza ocular | `limpieza_ocular_41p_23-11-2026` | `06547f5` | `441bae9` | `afe7e98` | `afe7e98` |
| Red sobre la señal cruda | `red_cruda_41p_23-11-2026` | `0074c60` | `7e1f1e0` | `4789942` | `4789942` |

Desde la reapertura, cada etapa tuvo además una revisión adicional del código antes de ver resultados. Esas revisiones, y las auditorías de resultados que cita este documento, se hicieron con un asistente automático a pedido del autor y con código separado; no son revisiones de un tercero. No hay un registro externo con sello de tiempo: el orden de commits ordena el trabajo, pero no equivale a un prerregistro.

## Comprobación de reproducibilidad

Hecha el 23-11-2026 con `scripts/verificar_cierre.py`; detalle en `resultados/verificacion_cierre_23-11-2026/verificacion.json`. No entrena ni recalcula.

- **Hashes.** De los 289 archivos con hash en los protocolos de las 12 etapas (scripts, tablas de entrada, predicciones de comparadores, crudos en caché, tensores y variables recalculadas), 288 coinciden hoy con el hash registrado.
- **La única diferencia está documentada.** `scripts/limpieza_ocular_41p.py` cambió después del registro: es la enmienda v2 (`441bae9`), hecha antes de ver resultados y limitada a la función de reporte. En el commit de registro su hash coincidía.
- **Orden del registro.** En las 10 etapas con informe propio, el protocolo entró a Git antes que el informe de resultados. Las otras dos (enmienda E1 y fase 2) reportan en el informe de su etapa principal.
- **Integridad del repositorio.** Las 12 carpetas no tienen archivos sin versionar ni modificados. `HEAD` coincide con `origin/main`. No había procesos de entrenamiento activos.

Lo que esta comprobación no cubre: no vuelve a entrenar los modelos, así que no verifica que una nueva ejecución dé las mismas cifras. Los datos locales fuera de Git (crudos, caché, tensores y variables recalculadas) se comprobaron en este Mac; su respaldo depende de las copias de `datos/locales`.

## Auditoría final de resultados (23-11-2026)

Un asistente automático, a pedido del autor, recalculó con código separado las 12 etapas desde las predicciones (`documentacion/auditoria_final_23-11-2026/AUDITORIA_EXPERIMENTO.md`).

- **Cifras.** 2.638 valores comparados con los CSV, sin discrepancias. Los intervalos y los p difieren solo por la semilla del bootstrap y ninguna decisión cambia. El montaje no tiene predicciones y no se pudo recalcular.
- **Integridad.** Mismas personas, ventanas y etiquetas entre modelos pareados; cada persona en un solo grupo de evaluación.
- **Sin hallazgos bloqueantes.** Seis hallazgos importantes, todos de lectura; este documento ya los incorpora:
  1. La red depende de lo ocular en su detección, no en su ventaja sobre el HGB.
  2. La limpieza ocular quita cerca de un tercio de la detección sobre el azar (0,060 de 0,181); que el resto sea ocular es una inferencia.
  3. El efecto temporal en activación no está confirmado: el contraste principal se estimó nueve veces sobre las mismas personas (entre +0,028 y +0,047; 3 de 9 intervalos incluyen el cero) y es desigual entre personas (mediana +0,014; 23 de 41). El contraste mejor sostenido es el historial sin las ventanas de 6 s que promedia la etiqueta frente al placebo (+0,046, p Holm 0,004; protocolo fijado antes de sus predicciones, pero después de ver que el historial completo superaba al placebo en las mismas personas y la misma partición).
  4. Solo la banda de 6 s tiene respaldo; de 12 s en adelante los resultados son inconclusos, no nulos.
  5. La ventaja de la fusión tardía es un secundario entre redes MLP; con HGB el signo es el contrario.
  6. El aporte por señal en activación descansa en importancias descriptivas y ruidosas.
- **Menores.** Algunos informes redondean dos veces (a 4 y luego a 3 decimales); aquí se corrigieron dos límites de intervalo (+0,017 y +0,044). En el enfoque E1 las predicciones del modelo con historial y posición son idénticas a las del modelo con historial: un diagnóstico del 26-11 (`documentacion/auditoria_final_23-11-2026/ronda2/DIAGNOSTICO_E1_POSICION.md`) mostró, al reajustar un fold (partición 1101, fold 0), que el modelo recibe la columna de posición y no la usa en ninguna de sus 1.800 divisiones; no es un error y la cifra no cambia. La enmienda E1 del 16-11 se registró antes de sus predicciones, pero se corrió el 18-11.
- **No verificable sin reentrenar.** Que las predicciones provengan de la configuración declarada (comprobado para un fold del enfoque E1 el 26-11), qué personas entraron al ajuste de cada modelo y las importancias por permutación.

### Auditoría de código (26-11-2026; ronda 2 del bucle de revisión, carpeta `ronda3`)

Una revisión del código del 16 al 23-11, hecha con un asistente automático a pedido del autor (`documentacion/auditoria_final_23-11-2026/ronda3/AUDITORIA_CODIGO.md`, con comprobaciones ejecutables en `comprobaciones/`), no encontró fuga entre personas ni fuga directa de la etiqueta a las entradas, y reprodujo bit a bit el fold 0 del análisis final. Ningún hallazgo cambia una cifra. Cuatro afectan lecturas y este documento los declara en "Límites"; se listan bajo la tabla, que separa los contrastes de activación por grupo de personas (descriptiva, no registrada):

| Contraste de activación | 41 personas | 25 de la búsqueda | 16 restantes |
|---|---|---|---|
| Principal, 16-11 | +0,034 | +0,055 [+0,012; +0,101] | +0,001 [−0,052; +0,055] |
| Principal, 5 particiones | +0,036 | +0,046 [+0,012; +0,086] | +0,021 [−0,017; +0,060] |
| Con tiempo de sesión | +0,026 | +0,050 [+0,013; +0,085] | −0,011 [−0,066; +0,038] |
| Con posición (Q1) | +0,032 | +0,049 [+0,018; +0,081] | +0,006 [−0,043; +0,049] |
| Historial − posición (18-11) | +0,038 | +0,063 [+0,021; +0,109] | −0,001 [−0,056; +0,054] |
| Historial − placebo (16-11) | +0,038 | +0,057 [+0,023; +0,092] | +0,008 [−0,048; +0,058] |
| Historial desplazado 6 − placebo | +0,046 | +0,035 [+0,003; +0,064] | +0,064 [+0,015; +0,115] |
| Banda de 6 s − placebo (40 personas: 24 y 16) | +0,047 | +0,058 [+0,015; +0,101] | +0,030 [−0,003; +0,068] |
| GRU hasta 32 − GRU una ventana | +0,051 | +0,045 [+0,007; +0,083] | +0,059 [+0,014; +0,101] |

1. **H1.** La selección de hojas de activación la decidió el modelo con historial, sobre 25 de las 41 personas evaluadas. La tabla (reproducida el 26-11 con `c07_seleccion_y_grupos.py`, desde las predicciones guardadas) muestra dónde se concentran los contrastes. Sesgo posible, no demostrado.
2. **H2.** La etiqueta de activación es en lo esencial el nivel tónico de la GSR (AUC 0,911 del nivel tónico de la ventana contra la etiqueta) y su soporte excede los 6 s.
3. **H3.** En el *Modelo Profesor* con PCA la pupila pesa −0,052.
4. **H4.** Las fijaciones se suman con su duración completa.

Los `INFORME.md` de cada etapa no se modificaron: conservan su redacción original, incluidas las palabras "confirmado" y los redondeos señalados.

## Límites que deben ir en la tesis

- Las 41 personas incluyen las de validación y test consultadas en etapas anteriores. Todo lo posterior al 16-11 es exploratorio o dirigido; nada es una confirmación independiente en una cohorte nueva.
- Las etiquetas son pseudoetiquetas calculadas offline y relativas a la sesión de cada persona; no validan una medida externa de atención ni de activación.
- La etiqueta de atención se define con la conducta ocular, y el EEG contiene la huella eléctrica de esa conducta. La regla de no-circularidad entre señales no asegura independencia fisiológica. Con estos datos no se puede afirmar detección cerebral de atención.
- La limpieza ocular es parcial; 0,060 se lee como cota inferior de la contribución ocular. Es la lectura más defendible y no una demostración: los componentes se eligen con la mirada, que también define la etiqueta, el control no está igualado en esa relación y tres componentes arrastran actividad frontal no ocular.
- El EEG y el seguidor ocular tienen un desfase de reloj de 0,18 a 0,53 s sin corregir; su efecto no se midió. Se agrupa en dos valores (cerca de 0,28 s en P2 a P21, P36 y P37; cerca de 0,48 s en el resto), lo que sugiere una causa sistemática de adquisición que no se investigó.
- El diseño de evaluación cambió después de un resultado nulo (cierre V3).
- **Selección de la configuración (límite destacado).** Las 15 hojas del modelo de activación se eligieron con la AUC media de los modelos con 1, 8 y 32 ventanas; la elección la decidió el de 32 (0,5311 con 15 hojas frente a 0,4994 con 7), y las 25 personas de esa búsqueda son 25 de las 41 evaluadas. Los contrastes del HGB con historial hasta 32 se concentran en ellas. El sesgo a favor del historial es posible y no está demostrado: la diferencia entre grupos no es significativa con 16 personas, y el historial desplazado frente al placebo y la GRU son positivos en ambos grupos. No se corrió una sensibilidad con 7 hojas ni con selección anidada.
- La etiqueta de atención (*Modelo Profesor* con PCA) se siguió usando tras observar que los modelos la predecían mejor que la de pesos iguales; eso no es un argumento de validez.
- La etiqueta de activación es en lo esencial el nivel tónico de la GSR relativo a la sesión, y su soporte real excede los 6 s nominales: el filtro tónico (pasa-bajos de 0,05 Hz aplicado en ambos sentidos sobre la sesión completa) deja el 49 % del peso de la parte tónica en las ventanas nominales, el 25 % antes y el 25 % después. El contraste "sin las ventanas de la etiqueta" no excluye ese soporte.
- El efecto de activación no es estable entre subconjuntos de personas ni entre diseños: +0,055 en las 25 de entrenamiento y +0,001 en las otras 16 en el análisis con 41 personas, y el patrón inverso en el cierre V3 (descriptivo, no registrado).
- La etiqueta de atención es, en la práctica, conducta de mirada: en el *Modelo Profesor* con PCA la pupila pesa −0,052. Las variables de fijación suman la duración completa de las fijaciones que tocan la ventana (más de 2.000 ms en cerca del 28 % de las ventanas etiquetadas).
- Ocho filas, todas de atención, cumplen dos reglas de decisión a la vez; la precedencia del código (respaldo, inferior, nulo concluyente), que los protocolos no fijan, deja seis como "inferior" y dos como "respaldo". Los modelos de historial desplazado reciben una columna no declarada con el número de ventanas.
- La AUC por persona pesa igual a todas las personas, sin mínimo de ventanas: P4, la más influyente del contraste principal de activación, conserva 26 ventanas con etiqueta. Los resultados de activación se refieren al 53 % de las ventanas que conserva la etiqueta.
- La validación cruzada separa personas, no grupos experimentales; las personas de un mismo grupo vieron los estímulos en el mismo orden y no se evaluó dejando grupos completos fuera.
- La corrección de Holm se aplica dentro de cada etapa y no entre las doce etapas, todas sobre las mismas 41 personas.
- La red recibe la señal escalada por persona y canal y el modelo de referencia no: su ventaja no puede atribuirse a la arquitectura sin separar ese factor.
- La red sobre la señal cruda es una sola arquitectura sin búsqueda; su pérdida al limpiar no tiene control propio.
- El explicativo de posición y la fase 2 son post hoc. Los contrastes secundarios no llevan corrección por multiplicidad.
- La ampliación con el historial desplazado es un análisis dirigido: se registró después de ver el placebo de la robustez (ver "Trazabilidad").
- El placebo iguala la persona y el largo del historial, pero no el estímulo ni la cercanía en la sesión: sus ventanas se sortean entre las de la misma persona en otros estímulos, anteriores o posteriores. El contraste entre el historial real y el placebo no separa la fisiología previa de pertenecer a la misma página; dentro de un mismo estímulo no se demostró que el historial supere al tiempo transcurrido.
- Los intervalos son percentiles de un *bootstrap* de personas: no recogen la dependencia entre las AUC por persona de una validación cruzada ni la variación por conjunto de entrenamiento.
- El control del tiempo de sesión solo corrige la tendencia común a las personas.
- La adaptación a la persona no es comparable con los demás contrastes: sus etiquetas de calibración se definen con la mediana de toda la sesión e informan sobre la parte evaluada.
- "Alta" en el *Attention Score* designa una mirada más quieta (fijaciones más largas, menos dispersión y recorrido): la dispersión y el recorrido entran invertidos antes de la componente.
- En las pruebas contra 0,5, "efecto relevante" solo indica que el límite inferior de la AUC supera 0,52.
- El detalle de cada uno de estos límites está en el borrador de Resultados y Discusión (secciones 6.1, 6.2, 6.4, 6.6, 7.1, 7.7, 7.11 y 8.4).
- En activación las AUC absolutas son bajas (0,50 a 0,59).

## Queda abierto (no es experimentación)

Decisiones con el profesor guía:

1. Si se planifica una cohorte nueva para confirmar activación.
2. Si el margen práctico de 0,02 queda como criterio.
3. Si "emociones" se presenta como activación (*arousal*).
4. Si la etiqueta de atención corregida por posición reemplaza a la original.
5. El encuadre: apoyo parcial, con la detección de atención por EEG presentada como dependiente, en cerca de un tercio, de la huella ocular, sin atribuir el resto a un origen cerebral ni ocular. Incluye con qué lectura del criterio de la hipótesis se llega a "apoyo parcial" (sección 8.1 del borrador integrado).
6. Si se aceptan las etiquetas normalizadas con la sesión completa de cada persona (el manuscrito pide normalizar solo con entrenamiento).
7. Si el *Modelo Profesor* con PCA queda como definición del *Attention Score* (la nota de diseño proponía la fusión igualitaria como principal).

Ninguna de las siete está tomada. Las opciones de cada una están en la minuta del 23-11 (`Avances/Avance - 23-11-2026 (Minuta de decisiones con el profesor).md`), que desde el 26-11 lista además las hipótesis, objetivos y contribuciones del esqueleto que conviene revisar, la información de participantes y ética que hay que pedir al proyecto, y la pregunta de cómo declarar el uso de asistentes automáticos.

Trabajo de cierre:

1. Revisar el borrador integrado `Escritura/Borrador Resultados y Discusión 23-11-2026.md` (reemplaza al del 18-11) y pasarlo a LaTeX.
2. Ajustar `Escritura/Borrador Conclusiones 23-11-2026.md` según las decisiones anteriores.
3. Leer en texto completo las 8 referencias contrastadas solo por resumen (Barry 2005 y 2007, Boucsein 2012, Critchley 2002, Croft y Barry 2000, Iwasaki 2005, Keren 2010 y Yuval-Greenberg 2008); detalle en `documentacion/auditoria_final_23-11-2026/VERIFICACION_REFERENCIAS.md`.

Experimentos opcionales, solo si se piden: red con filtro de control, corrección del desfase entre EEG y seguidor ocular, sensibilidad del modelo de activación con 7 hojas o con selección anidada, historial desplazado menos placebo dentro de un mismo estímulo (saldría de predicciones guardadas, sin entrenar; requiere orden del autor y protocolo registrado), evaluación dejando grupos experimentales fuera (requiere volver a entrenar), y cohorte nueva.

Presentación vigente: `presentaciones/avances_tesis_06-11-2026` (versión 7).
