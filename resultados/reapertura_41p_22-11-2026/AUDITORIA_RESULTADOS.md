# Auditoría independiente de resultados — reapertura del 22-11-2026

Hecha por un agente independiente con código propio escrito desde cero, sin usar las funciones de informe de los scripts y sin modificar el repositorio. Remuestreo propio: 20.000 réplicas bootstrap y 200.000 permutaciones de signos.

| Punto | Resultado | Detalle |
|---|---|---|
| 1. Familia confirmatoria (4 filas) | PASA | Delta idénticos (diferencia máxima 1e-17). Los IC difieren como máximo 4e-4 y los p 0,002 por el remuestreo; ninguno cambia de lado respecto de 0 ni de 0,05. Las 20 filas por partición coinciden. |
| 2. Curva temporal y placebo de bloque (20 filas) | PASA | Delta, número de personas y personas que mejoran coinciden. No se recalcularon IC ni p de estas filas. |
| 3. AUC estratificada (estímulo y minuto, ambas tareas) | PASA | Delta idénticos; IC y p coherentes. No se recalculó el estrato de posición. |
| 4. Integridad | PASA | Cada fila aparece una vez por estrategia; mismas filas y etiquetas entre estrategias y semillas; 41 personas, cada una en un solo fold por semilla; folds iguales a los del protocolo; filas de la curva iguales a las de `cobertura_*.json`. |
| 5. Sanidad | PASA, con nota | Sin NaN, sin valores fuera de [0, 1], sin predicciones constantes. Ver influencia abajo. |
| 6. Hashes y cronología | PASA | Los 14 insumos de la fase 1 y los 3 de la fase 2 coinciden con los archivos actuales. Registro de la fase 1 a las 19:59:57 y de la fase 2 a las 20:08:14; el primer archivo de predicciones de la fase 1 es de las 20:31:28. |

## Influencia de personas individuales (activación)

Calculada por el auditor y repetida con el código del análisis.

| Contraste | Media | Mediana | Mejoran | Persona más influyente | Sin esa persona |
|---|---|---|---|---|---|
| P1 historial − sin historial | +0,036 | +0,014 | 23/41 | P4 (+0,385) | +0,028 [+0,006; +0,050], p 0,020 |
| Mismo estímulo | +0,054 | +0,052 | 26/41 | P4 (+0,450) | +0,044 [+0,009; +0,080], p 0,022 |
| Mismo minuto | +0,058 | +0,042 | 24/41 | P4 (+0,379) | +0,050 [+0,021; +0,081], p 0,002 |
| Desfase 6 s − placebo | +0,047 | +0,042 | 30/40 | P24 (+0,350) | +0,039 [+0,012; +0,065], p 0,006 |
| Desfase 6 s − placebo de bloque | +0,053 | +0,056 | 31/40 | P24 (+0,325) | +0,046 [+0,021; +0,070], p 0,001 |

Todos los contrastes siguen siendo positivos sin la persona más influyente. En P1 la media es 2,5 veces la mediana y mejoran 23 de 41 personas: el efecto promedio es real pero desigual entre personas. El contraste del desfase de 6 s es el más parejo (30 de 40).

Otras notas: el modelo sin historial con tiempo de sesión (`c1_ts`) tiene dos personas con AUC bajo 0,2 en activación (P21 y P47), lo que ensancha el intervalo de P2. El modelo de solo posición existe únicamente en la partición 1101, como indica el protocolo. La comprobación post hoc no registrada no fue auditada.
