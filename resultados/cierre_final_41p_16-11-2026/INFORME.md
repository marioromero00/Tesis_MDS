# Análisis final con 41 personas — 16-11-2026

Script: `scripts/cierre_final_41p.py`. Protocolo registrado y publicado antes de correr (commit `1bbb083`), ejecutado una sola vez. Validación cruzada agrupada por persona (8 folds) sobre las 41 personas del análisis principal, con la configuración congelada del cierre V3 (HGB 7 hojas en atención y 15 en activación, elegidas solo con train; GRU fija). Sin búsqueda de ningún tipo. Revisión independiente del script: sin bloqueantes.

## Resultado principal (fijado de antemano)

Contraste: HGB con hasta 32 ventanas de historial − HGB solo con la ventana actual. Diferencia de AUC por persona (n = 41), IC bootstrap por persona, permutación de signos, Holm sobre las dos tareas.

| Tarea | ΔAUC | IC 95 % | IC 90 % | Personas que mejoran | p Holm | Decisión |
|---|---|---|---|---|---|---|
| Atención | **+0,026** | [+0,018; +0,035] | [+0,019; +0,033] | 36/41 | 0,00001 | **Respaldo** |
| Activación | +0,034 | [−0,001; +0,069] | [+0,005; +0,064] | 24/41 | 0,066 | Inconcluso |

En atención el efecto es positivo y no se explica por azar; no alcanza el umbral de "efecto relevante" (límite inferior 0,018 < 0,02). En activación el intervalo toca cero.

## AUC absolutas (media por persona, 41 personas)

| Tarea | HGB sin historial | HGB hasta 5 | HGB hasta 32 | GRU 1 ventana | GRU hasta 32 |
|---|---|---|---|---|---|
| Atención | 0,684 [0,667; 0,700] | 0,702 [0,686; 0,718] | 0,710 [0,694; 0,727] | 0,662 [0,642; 0,681] | 0,670 [0,649; 0,691] |
| Activación | 0,529 [0,501; 0,558] | 0,547 [0,515; 0,579] | 0,563 [0,524; 0,602] | 0,533 [0,501; 0,567] | 0,583 [0,541; 0,626] |

## Secundarios (descriptivos, p sin corregir)

| Tarea | Contraste | ΔAUC | IC 95 % | Mejoran | p | Lectura |
|---|---|---|---|---|---|---|
| Atención | HGB 5 − sin historial | +0,018 | [+0,012; +0,024] | 34/41 | <0,001 | Casi toda la ganancia aparece con 5 ventanas |
| Atención | GRU 32 − GRU 1 | +0,008 | [−0,004; +0,020] | 26/41 | 0,21 | IC 90 % dentro de ±0,02: el orden no agrega un efecto relevante |
| Atención | GRU 32 − HGB 32 | −0,040 | [−0,055; −0,027] | 9/41 | <0,001 | La GRU rinde peor que el resumen |
| Activación | HGB 5 − sin historial | +0,018 | [−0,006; +0,041] | 23/41 | 0,15 | Inconcluso |
| Activación | GRU 32 − GRU 1 | +0,051 | [+0,021; +0,080] | 28/41 | 0,002 | Positivo, pero secundario y sin corrección |
| Activación | GRU 32 − HGB 32 | +0,020 | [−0,017; +0,057] | 22/41 | 0,31 | Inconcluso |

## Heterogeneidad por grupo (`heterogeneidad_por_grupo.csv`)

| Tarea | Contraste | 25 de train | 16 de validación + test |
|---|---|---|---|
| Atención | HGB 32 − sin historial | +0,023 [+0,014; +0,031] · 22/25 | +0,032 [+0,016; +0,048] · 14/16 |
| Activación | HGB 32 − sin historial | +0,055 [+0,012; +0,101] · 17/25 | +0,001 [−0,052; +0,055] · 7/16 |
| Activación | GRU 32 − GRU 1 | +0,045 [+0,007; +0,083] · 17/25 | +0,059 [+0,014; +0,102] · 11/16 |

El efecto en atención se repite en ambos grupos. En activación, el resumen del historial funciona en un grupo y no en el otro.

## Conclusión respecto de la hipótesis

Con los criterios de interpretación del manuscrito: **evidencia mixta, apoyo parcial.** En atención, agregar historial mejora la predicción de forma consistente (+0,026 AUC, 36 de 41 personas, p Holm < 0,001), aunque el efecto es pequeño y casi todo aparece con 5 ventanas (unos 6 s). El modelo que usa el orden (GRU) no agrega sobre el resumen. En activación el resultado principal es inconcluso; la GRU muestra una señal secundaria que habría que confirmar con datos nuevos.

## Límites

- Las 16 personas de validación y test ya se habían consultado; la configuración se eligió solo con train y no se cambió. Es una estimación con más potencia, no una confirmación independiente.
- Etiquetas de atención del Modelo Profesor PCA ajustado con las 25 personas de train; afecta por igual a ambos modelos del contraste, y el efecto se repite en las 16 que no participaron en ese ajuste.
- Variables transductivas por persona y etiquetas offline (ver protocolo V3).
- Bootstrap percentil; con 41 personas la cobertura puede ser algo menor al nominal.
- Las reglas de decisión tienen precedencia fija en el código (respaldo, inferior, nulo); los indicadores de equivalencia e inferioridad están en `contrastes.csv` para cada contraste.
