# Auditoría independiente de resultados — fase 3 (22-11-2026)

Hecha por un agente independiente con código propio, sin usar las funciones de informe de los scripts y sin modificar el repositorio. Remuestreo propio: 20.000 réplicas bootstrap y 200.000 permutaciones de signos.

| Punto | Resultado | Detalle |
|---|---|---|
| 1. Confirmatorio (4 filas) | PASA | Delta, mediana, personas que mejoran, persona más influyente y delta sin ella coinciden exactamente. IC difieren como máximo 3,4e-4 y p 2,1e-3 por el remuestreo. Las cuatro decisiones salen iguales al aplicar las reglas del protocolo. En activación Q1 el p Holm recalculado es 0,105 (publicado 0,108): inconcluso es correcto. |
| 2. Descriptivos (ámbitos todas y mismo estímulo) | PASA | Los cuatro contrastes coinciden exactamente en delta y en personas que mejoran. No se recalcularon sus IC ni p, ni los estratos de minuto y posición. |
| 3. Integridad | PASA | Sin duplicados; mismas filas, etiquetas y personas que los archivos de la fase 1 de la misma semilla; 41 personas, cada una en un solo fold; folds iguales a los del protocolo; sin NaN, sin valores fuera de [0, 1], sin predicciones constantes. |
| 4. Hashes y cronología | PASA | Las 14 entradas del protocolo coinciden con los archivos actuales. Registro a las 21:02:30; archivos de predicciones entre las 21:16:00 y las 21:20:49. |

## Pares dentro del mismo estímulo (activación, partición 1101)

Pares positivo-negativo por persona: mínimo 4, percentil 10 de 208, mediana 432, máximo 1.537. La mediana de estímulos informativos por persona es 8.

La persona con 4 pares es P4, con un solo estímulo informativo: su AUC dentro del estímulo es casi puro ruido. P4 era la persona más influyente del contraste "mismo estímulo" de la fase 2 (+0,450), así que ese valor extremo de la fase 2 no es informativo; sin ella aquel contraste era +0,044 [+0,009; +0,080]. La siguiente persona con menos pares tiene 135.
