# Auditoría independiente de resultados — cuatro enfoques (22-11-2026)

Hecha por un agente independiente con código propio a partir de las predicciones crudas, sin usar las funciones de informe del script y sin modificar el repositorio. Remuestreo propio: 20.000 réplicas bootstrap y 200.000 permutaciones de signos.

| Punto | Resultado | Detalle |
|---|---|---|
| 1. Las 18 filas confirmatorias | PASA | Delta, número de personas y personas que mejoran coinciden (diferencia menor que 5e-6). IC, p y Holm recalculados para las 18: difieren solo por el remuestreo (IC hasta 0,001) y ninguna decisión cambia. El contraste C2 se verificó de forma exacta. |
| 2. Integridad | PASA | Sin duplicados en los 25 archivos; 41 personas (40 en la adaptación de activación: P4 no tiene filas de evaluación); cada persona en un solo fold y folds iguales a los del protocolo; sin NaN ni valores fuera de rango. La etiqueta corregida difiere de la original en el 9,36 % de las filas, con cambios en las 41 personas. Ninguna fila de evaluación de la adaptación es anterior al 40 % de la sesión; la separación mínima con la calibración es de 10,3 s. |
| 3. Hashes y registro | PASA | Los 24 insumos del protocolo coinciden con los archivos actuales. El registro (22:15:08) es anterior al primer archivo de resultados (22:30). |
| 4. Sanidad e influencia | PASA | Ninguna conclusión depende de una persona. Ninguna AUC promedio por persona bajo 0,2 ni sobre 0,95. |
| 5. Controles negativos | PASA | Etiquetas barajadas: AUC 0,496. Posición sola con la etiqueta corregida: 0,504. |

## Decisiones cercanas al umbral

- E1, A1 y A3: p Holm entre 0,055 y 0,056 en ambos cálculos.
- E4, adaptación de activación sin historial: p Holm entre 0,048 y 0,049.

No cruzan el umbral de 0,05 al recalcular, pero están pegadas a él y deben leerse con cautela.

## Influencia

| Contraste | Media | Mediana | Persona más influyente | Sin ella |
|---|---|---|---|---|
| Adaptación de activación con historial | +0,045 | +0,033 | P24 (+0,298) | +0,038 |
| Activación por estímulo − 0,5 | +0,087 | +0,096 | P21 (−0,198) | +0,094 |
| Solo alfa y beta − 0,5 | +0,093 | +0,100 | P37 (−0,004) | +0,095 |

Otros casos: estímulo + duración frente a solo duración sube de +0,048 a +0,062 sin P13; frontales − posteriores baja de +0,073 a +0,068 sin P47; adaptación de activación sin historial baja de +0,028 a +0,023 sin P27.

Nota menor: la columna `cal_rows` de los archivos `e4_*` es el total de filas de calibración del fold, no de la persona.
