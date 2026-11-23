# Cierre consolidado de la experimentación — 23-11-2026

Este documento reemplaza como referencia a `Cierre_Experimental_Final_22-11-2026.md`, que es anterior a la reapertura. Reúne todas las etapas registradas entre el 16 y el 23 de noviembre de 2026, sus decisiones, su trazabilidad y la comprobación de reproducibilidad. No contiene resultados nuevos. Ante cualquier diferencia mandan los `INFORME.md` y los CSV de cada carpeta de resultados.

Estado: Mario Romero pidió este cierre el 23-11-2026. No hay aprobación del profesor guía registrada sobre estos resultados, sobre el margen práctico de 0,02 ni sobre el encuadre de la tesis. Etiqueta de Git: `cierre-experimental-2026-11-23`.

## Conclusión general

Evidencia mixta, con **apoyo parcial** a la hipótesis de temporalidad, que proviene de activación.

| Pregunta | Atención | Activación |
|---|---|---|
| ¿Mejora el modelo con historial? | Sí: +0,029 [+0,021; +0,037], efecto relevante | Sí: +0,036 [+0,010; +0,065], respaldo |
| ¿La mejora es información temporal? | No. Es la posición en el estímulo: con la posición como variable el historial agrega +0,001 [−0,002; +0,005], nulo concluyente | En parte. La información está en los 6 a 12 s anteriores (+0,047 [+0,018; +0,078] frente a un placebo) y desaparece desde 24 s |
| ¿Queda algo al controlar la posición? | Nada | +0,032 [+0,004; +0,059], inconcluso tras Holm; dentro de un mismo estímulo se explica por el tiempo transcurrido |
| ¿Aporta el orden de las ventanas (GRU)? | No: +0,008 [−0,004; +0,020], y rinde 0,040 bajo el HGB | Indicio secundario, sin corrección |
| ¿Qué fusión? | Tardía sobre temprana: +0,012 [+0,005; +0,021] | Sin diferencias |
| ¿Qué detecta el EEG en la ventana actual? | Sobre todo la conducta ocular: 0,681, que baja a 0,621 al quitar los componentes oculares | Nada demostrable: 0,524 |
| ¿Ayuda un modelo más complejo? | Red sobre la señal cruda: 0,716, +0,035 sobre el HGB; su ventaja también es ocular | No: 0,498 |

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
| Ampliación E1–E6 y enmienda | Activación, historial sin los 6 s de la etiqueta frente a placebo: +0,046 [+0,018; +0,073]. Fusión tardía mejor en atención |
| Explicativo de posición (post hoc) | En atención los segundos en el estímulo reproducen la mejora: +0,028 [+0,021; +0,035] |

### 22-11 — Reapertura

| Etapa | Resultado principal |
|---|---|
| Fase 1, confirmatoria (5 particiones) | Atención +0,029 [+0,021; +0,037], efecto relevante. Activación +0,036 [+0,010; +0,065], respaldo; con tiempo de sesión en ambos modelos +0,026 [−0,006; +0,056], inconcluso |
| Fase 1, curva temporal | Activación: 6 s +0,047 [+0,018; +0,078], respaldo; 12 s +0,024, inconcluso; desde 24 s no se distingue del placebo. Atención: nulo concluyente a 6 y 12 s |
| Fase 2, controles post hoc | El resultado no depende del tipo de placebo. Dentro del mismo minuto de sesión, activación +0,058 [+0,027; +0,092] |
| Fase 3, historial frente a posición | Atención: nulo concluyente (+0,001; dentro del estímulo −0,000). Activación: +0,032 [+0,004; +0,059], inconcluso tras Holm; dentro del estímulo +0,009, inconcluso |

### 22-11 — Cuatro enfoques

| Enfoque | Resultado principal |
|---|---|
| E1 Etiqueta de atención corregida por posición | La posición sola deja de predecir (0,504). La detección se conserva (0,675 frente a 0,683). El historial queda en nulo concluyente con la posición como variable |
| E2 Detección cruzada | El EEG solo detecta la etiqueta ocular con 0,681; el GSR no le agrega nada (+0,002, nulo concluyente). Potencia lenta y amplitud 0,673; alfa y beta 0,593 |
| E3 Activación por estímulo | AUC 0,587, la más alta en activación; no supera de forma demostrable a promediar el modelo por ventana (+0,020, inconcluso) |
| E4 Diferencias entre personas | La detectabilidad de cada persona es estable (fiabilidad 0,76 y 0,66); la ganancia del historial no lo es. Adaptar el modelo a la persona mejora activación en +0,045 [+0,023; +0,069] |

### 23-11 — Qué detecta el EEG

| Etapa | Resultado principal |
|---|---|
| Montaje (descriptivo) | Los datos son compatibles con el montaje por defecto del equipo. El EEG va entre 0,18 y 0,53 s atrasado respecto del seguidor ocular; no se corrigió |
| Limpieza ocular | Quitar 3 componentes oculares (3,5 % de la varianza) baja la AUC de 0,681 a 0,621: +0,060 [+0,045; +0,075], efecto relevante. El control (72 % de la varianza) la deja en 0,674. Alfa y beta baja de 0,593 a 0,547 |
| Red sobre la señal cruda | Atención: red 0,716 frente a HGB 0,681, +0,035 [+0,023; +0,047], efecto relevante con holgura mínima. Con EEG limpio 0,649 frente a 0,621. Activación: 0,498 frente a 0,524, inconcluso |

## Trazabilidad

Cada etapa confirmatoria se registró y publicó antes de correr y se ejecutó una vez.

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
| Montaje | `montaje_ocular_41p_23-11-2026` | descriptivo | — | `441bae9` | — |
| Limpieza ocular | `limpieza_ocular_41p_23-11-2026` | `06547f5` | `441bae9` | `afe7e98` | `afe7e98` |
| Red sobre la señal cruda | `red_cruda_41p_23-11-2026` | `0074c60` | `7e1f1e0` | `4789942` | `4789942` |

Desde la reapertura, cada etapa tuvo además una auditoría independiente de código antes de ver resultados.

## Comprobación de reproducibilidad

Hecha el 23-11-2026 con `scripts/verificar_cierre.py`; detalle en `resultados/verificacion_cierre_23-11-2026/verificacion.json`. No entrena ni recalcula.

- **Hashes.** De los 289 archivos con hash en los protocolos de las 12 etapas (scripts, tablas de entrada, predicciones de comparadores, crudos en caché, tensores y variables recalculadas), 288 coinciden hoy con el hash registrado.
- **La única diferencia está documentada.** `scripts/limpieza_ocular_41p.py` cambió después del registro: es la enmienda v2 (`441bae9`), hecha antes de ver resultados y limitada a la función de reporte. En el commit de registro su hash coincidía.
- **Orden del registro.** En las 10 etapas con informe propio, el protocolo entró a Git antes que el informe de resultados. Las otras dos (enmienda E1 y fase 2) reportan en el informe de su etapa principal.
- **Integridad del repositorio.** Las 12 carpetas no tienen archivos sin versionar ni modificados. `HEAD` coincide con `origin/main`. No había procesos de entrenamiento activos.

Lo que esta comprobación no cubre: no vuelve a entrenar los modelos, así que no verifica que una nueva ejecución dé las mismas cifras. Los datos locales fuera de Git (crudos, caché, tensores y variables recalculadas) se comprobaron en este Mac; su respaldo depende de las copias de `datos/locales`.

## Límites que deben ir en la tesis

- Las 41 personas incluyen las de validación y test consultadas en etapas anteriores. Todo lo posterior al 16-11 es exploratorio o dirigido; nada es una confirmación independiente en una cohorte nueva.
- Las etiquetas son pseudoetiquetas calculadas offline y relativas a la sesión de cada persona; no validan una medida externa de atención ni de activación.
- La etiqueta de atención se define con la conducta ocular, y el EEG contiene la huella eléctrica de esa conducta. La regla de no-circularidad entre señales no asegura independencia fisiológica. Con estos datos no se puede afirmar detección cerebral de atención.
- La limpieza ocular es parcial; 0,060 es una cota inferior de la contribución ocular.
- El EEG y el seguidor ocular tienen un desfase de reloj de 0,18 a 0,53 s sin corregir.
- La red sobre la señal cruda es una sola arquitectura sin búsqueda; su pérdida al limpiar no tiene control propio.
- El explicativo de posición y la fase 2 son post hoc. Los contrastes secundarios no llevan corrección por multiplicidad.
- En activación las AUC absolutas son bajas (0,52 a 0,59).

## Queda abierto (no es experimentación)

Decisiones con el profesor guía:

1. Si la etiqueta de atención corregida por posición reemplaza a la original.
2. Si el margen práctico de 0,02 queda como criterio.
3. Si "emociones" se presenta como activación (*arousal*).
4. El encuadre: apoyo parcial, con la atención por EEG presentada como huella ocular.
5. Si se planifica una cohorte nueva para confirmar activación.

Trabajo de cierre:

1. Integrar los resultados del 22 y 23-11 al borrador de Resultados y Discusión del 18-11 (`Escritura/Borrador Discusión fisiológica 23-11-2026.md` ya cubre la parte fisiológica).
2. Escribir Conclusiones, que depende de las decisiones anteriores.
3. Confirmar en el texto completo las 18 referencias de `notas/sustento-fisiologico-23-11-2026.md`.

Experimentos opcionales, solo si se piden: red con filtro de control, corrección del desfase entre EEG y seguidor ocular, y cohorte nueva.

Presentación vigente: `presentaciones/avances_tesis_06-11-2026` (versión 7).
