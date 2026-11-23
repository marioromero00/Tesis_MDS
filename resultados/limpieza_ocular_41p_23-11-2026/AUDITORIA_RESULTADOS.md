# Auditoría independiente de resultados — limpieza ocular, 23-11-2026

Hecha por un agente independiente con código propio, sin importar los scripts del experimento y sin modificar el repositorio.

| Punto | Resultado |
|---|---|
| 1. Reproducción de cifras | **Pasa.** Las 4 pruebas confirmatorias, las AUC por persona y 296 valores descriptivos se reproducen con diferencia máxima de 1e-16. Decisiones idénticas. |
| 2. Integridad | **Pasa.** Mismas 22.176 ventanas, 41 personas y etiquetas en todas las estrategias y semillas, iguales a las del enfoque 2. Cada persona en un solo fold. El filtro identidad reproduce exactamente las probabilidades de `eeg_c1`. Control barajado en 0,489. |
| 3. Registro | **Pasa.** El protocolo (09:40) y la enmienda (09:47) se confirmaron antes de que existiera cualquier predicción (10:05). El hash registrado del script corresponde al commit `06547f5`; la enmienda agrega 9 líneas, solo en el informe. Hashes de crudos y de variables recalculadas coinciden. |
| 4. Robustez | **Pasa.** L1 y L2 no dependen de pocas personas: media y mediana coinciden (0,060 y 0,053), y sin la persona más influyente quedan en 0,064 y 0,058. |

## Advertencias

1. **L4 contradice la lectura prevista.** Se esperaba que la detección por alfa y beta no cambiara; cayó cerca de la mitad sobre el azar (de +0,093 a +0,047). Sigue sobre el azar en 38 de 41 personas.
2. **Valores p en el piso de resolución.** Los cuatro valen 1/200.001; deben reportarse como p < 0,00001.
3. **P9 es un caso atípico en contra del efecto.** La limpieza le sube la AUC de 0,569 a 0,680. Es una de las personas con saturaciones.
4. **La caída no se relaciona con la calidad de la identificación ocular.** Spearman entre la caída por persona y el puntaje del primer componente: +0,12 (p 0,46). La caída se asocia sobre todo con la AUC de partida (+0,55): pierde más quien más detección tenía.
5. **La curva por número de componentes no ha tocado fondo de forma demostrable.** El cuarto componente agrega +0,007 [−0,000; +0,015]. L1 es una cota inferior.
6. **El control no es un placebo igualado** (lo selecciona la varianza), y **L3 no prueba origen cerebral.** Ambos puntos están en los límites del informe.
7. **Imprecisión en la enmienda.** Dice "puntaje de 0,14 o menos" para las cinco personas de identificación débil; P18 tiene 0,142. El corte real es "bajo 0,15" (la siguiente persona tiene 0,207). La sensibilidad no cambia.
8. El control barajado tiene el IC 90 % apenas bajo cero (−0,021; −0,001) en una sola partición.

No se encontró ninguna otra discrepancia numérica.
