# Red convolucional sobre el EEG crudo — 23-11-2026

Script `scripts/red_cruda_41p.py`. Protocolo registrado y publicado antes de correr (commit `0074c60`), enmienda v2 tras la auditoría de código y antes de ver resultados de las redes (commit `7e1f1e0`), ejecutado una vez. Pedido por Mario el 23-11 ("probar otros modelos más complejos"). Análisis dirigido, no confirmación independiente.

**Pregunta:** ¿un modelo que aprende directamente de la señal cruda del EEG detecta mejor que el modelo de referencia (HGB sobre variables calculadas)? ¿Y esa detección también depende de los componentes oculares?

**Respuesta corta:** en atención sí supera al modelo de referencia (0,716 frente a 0,681), pero la ventaja está ligada a la señal ocular: al quitar los componentes oculares la red cae a 0,649. En activación la red queda en el azar (0,498).

## Método

- **Modelo.** Red convolucional tipo EEGNet de 1.217 parámetros: entrada de 16 canales × 240 muestras (2 s), con el mismo filtrado que la extracción de variables y escala por persona y canal. Una sola arquitectura y configuración, fijadas de antemano, sin búsqueda.
- **Tres redes.** Atención con el EEG original (`red_orig`), atención con el EEG sin 3 componentes oculares (`red_ica3`, mismos filtros del experimento de limpieza) y activación con el EEG original (`red_act`).
- **Comparadores.** HGB con las variables de EEG, configuración congelada: `eeg_c1` (22-11), `ica3_full` (limpieza del 23-11) y `hgb_eeg_act` (nuevo, activación solo con EEG).
- **Evaluación.** Las mismas 41 personas, ventanas y 5 particiones por persona de los experimentos anteriores. AUC por persona promediada sobre las particiones; Holm sobre las 4 pruebas; margen 0,02.

## Resultado confirmatorio

| Prueba | Contraste | ΔAUC | IC 95 % | A favor | p Holm | Decisión |
|---|---|---|---|---|---|---|
| R1 | Red − HGB, atención, EEG original | +0,035 | [+0,023; +0,047] | 32/41 | < 0,0001 | **Efecto relevante** |
| R2 | Red − HGB, atención, EEG limpio | +0,028 | [+0,013; +0,043] | 30/41 | 0,0017 | **Respaldo** |
| R3 | Red original − red limpia, atención | +0,067 | [+0,053; +0,082] | 39/41 | < 0,0001 | **Efecto relevante** |
| R4 | Red − HGB, activación | −0,025 | [−0,055; +0,003] | 15/41 | 0,0995 | **Inconcluso** |

AUC por persona (media e IC 95 %):

| Etiqueta | Modelo | AUC | Personas sobre 0,5 |
|---|---|---|---|
| Atención | Red, EEG original | 0,716 [0,697; 0,735] | 41/41 |
| Atención | HGB, EEG original | 0,681 [0,665; 0,697] | 41/41 |
| Atención | Red, EEG limpio | 0,649 [0,630; 0,667] | 41/41 |
| Atención | HGB, EEG limpio | 0,621 [0,607; 0,635] | 41/41 |
| Activación | Red, EEG original | 0,498 [0,478; 0,518] | 20/41 |
| Activación | HGB, solo EEG | 0,524 [0,497; 0,551] | 26/41 |
| Activación | HGB, EEG + mirada + pupila (22-11) | 0,518 [0,491; 0,545] | 22/41 |

## Lectura

1. **En atención, la red sobre la señal cruda supera al modelo de referencia en unos 0,035 de AUC.** Es el primer modelo más complejo que lo logra. El signo se mantiene en las 5 particiones. Supera el margen de relevancia por poco (ver límites).
2. **La ventaja de la red está ligada a la señal ocular.** Al quitar los 3 componentes oculares pierde 0,067, algo más que el HGB (0,060). Su probabilidad se asocia con el recorrido de la mirada más que la del HGB (Spearman 0,48 frente a 0,41) y, tras la limpieza, esa asociación sigue en 0,33. La red aprovecha mejor la huella de los ojos en el EEG; no hay base para leerla como detección cerebral.
3. **La ventaja persiste, menor, con el EEG limpio (+0,028).** No prueba información neuronal: la limpieza es parcial, y la red puede estar aprovechando mejor el residuo ocular.
4. **En activación la red no detecta nada** (0,498). Tampoco el HGB con solo EEG queda claramente sobre el azar (0,524; p = 0,09). La comparación entre ambos es inconclusa: los datos descartan que la red supere al HGB por 0,02 o más, y apuntan a igual o peor.

Para la tesis: un modelo más complejo sube la detección de atención por EEG, pero refuerza la conclusión del experimento de limpieza —lo que se detecta es sobre todo la conducta ocular— y no cambia el resultado de activación.

## Robustez (auditoría de resultados)

| Contraste | 1101 | 1102 | 1103 | 1104 | 1105 |
|---|---|---|---|---|---|
| R1 | +0,033 | +0,036 | +0,039 | +0,037 | +0,030 |
| R2 | +0,028 | +0,024 | +0,030 | +0,032 | +0,026 |
| R3 | +0,068 | +0,068 | +0,068 | +0,067 | +0,065 |
| R4 | −0,039 | −0,042 | −0,021 | +0,002 | −0,028 |

- Sin P23 y P39 ninguna decisión cambia (R1 +0,036; R2 +0,028; R3 +0,068; R4 −0,027).
- Dejando una persona fuera, R1, R2 y R3 mantienen su decisión. R4 pasa a "inferior" al quitar una de cinco personas (P10, P24, P33, P34 o P40).
- La t pareada y Wilcoxon dan las mismas conclusiones.

## Límites

- Análisis dirigido sobre personas y resultados ya vistos.
- **R1 es "efecto relevante" con holgura mínima.** El límite inferior del IC 95 % es 0,023; sin las dos personas más favorables (P21 y P18) queda en 0,0199, y con la partición 1105 sola en 0,017. La lectura segura es "ventaja respaldada de unos 0,035, que supera el margen por poco".
- **R3 no tiene control.** No se entrenó una red con el filtro de control. R3 muestra que la red pierde con el filtro ocular; que la pérdida sea propia de lo ocular descansa en el control del experimento de limpieza (L2).
- **Una sola arquitectura.** 1.217 parámetros, sin búsqueda, una inicialización por grupo, sin validación interna ni curva de convergencia. El resultado de activación vale para "esta red con esta configuración"; no permite decir que las redes profundas no sirven ni que el EEG crudo no contiene información de activación.
- **R4 es inestable.** El signo cambia en la partición 1104, el IC 90 % [−0,050; −0,001] excluye el cero solo marginalmente, y compara dos modelos sin señal demostrada. No se puede afirmar que el HGB sea mejor ni que sean equivalentes.
- **Núcleo temporal corto.** 0,26 s; la red representa mal la banda de 1–4 Hz.
- **Comparador fijo.** R1 y R2 valen frente a un HGB con variables fijas y configuración congelada.
- La escala por persona y el filtro ocular usan toda la sesión de cada persona, también de las evaluadas (sin etiquetas).
- 50 ventanas entran a la red con la entrada en cero (sin canales utilizables); el HGB dispone ahí de indicadores de calidad.
- La AUC es por persona. Juntando todas las ventanas es menor (red original 0,684) y no debe mezclarse con la anterior.
- Las predicciones del comparador `hgb_eeg_act` terminaron unos 2 minutos antes del commit de la enmienda. No se calculó ninguna cifra con ellas hasta el reporte final; "antes de ver resultados" se refiere estrictamente a las redes. La enmienda no cambia reglas.
- Los valores p de R1 y R3 están en el piso de resolución de la prueba.

## Auditorías

- Código, por un agente independiente con los entrenamientos en marcha y sin leer predicciones: sin hallazgos bloqueantes. Verificó que el tensor coincide con el tratamiento de la extracción de variables, que no hay fuga entre personas, y que la red aprende una señal sintética y da azar con etiquetas barajadas. Sus advertencias están en `enmienda_v2.md`.
- Resultados, por otro agente independiente con código propio: cifras reproducidas, integridad y registro correctos; advertencias de lectura incorporadas arriba. Detalle en `AUDITORIA_RESULTADOS.md`.

Archivos: `confirmatorio.csv`, `descriptivos.csv`, `auc_por_persona.csv`, `{modelo}_{semilla}.csv.gz` (predicciones), `protocolo.json`, `enmienda_v2.md`, `tensores.json`. Los tensores quedan fuera de Git (`datos/locales/v2_2025/red_cruda_tensores/`, hashes en `tensores.json`) y se regeneran con la fase `tensors`.
