# Enmienda v2 — 23-11-2026, antes de ver resultados

Origen: auditoría independiente de código, hecha con los modelos en marcha y sin leer predicciones. Sin hallazgos bloqueantes.

Cambios (solo en `report()`; la limpieza y los modelos no cambian):

1. Sensibilidad descriptiva de L1–L4 sin P23 y P39. En esas personas un canal frontal está plano parte de la sesión (P39: Fp1 el 92 %; P23: F7 el 30 %), por lo que en muchas ventanas la fuente ocular se estima sin sus canales principales.
2. Sensibilidad descriptiva de L1–L4 sin esas dos ni las cinco personas con identificación ocular débil (puntaje del primer componente de 0,14 o menos: P12, P18, P22, P35, P40).
3. Se reporta la fracción de varianza que quita cada condición y los puntajes oculares.

Las listas de personas se fijaron con información sin etiquetas (`personas_limpieza.csv` y los crudos). La familia confirmatoria, los modelos y las reglas de decisión no cambian. Las ejecuciones en marcha verificaron el script del commit 06547f5 al iniciar.

Límites que la auditoría pide declarar en el informe:

- El control `ctrl3` quita mucha más varianza que `ica3` (mediana 72 % frente a 3,5 %): no es un placebo. Si L2 da respaldo es evidencia fuerte de especificidad; si no, no se concluye nada.
- La limpieza es parcial y su calidad se mide en los mismos datos con que se eligieron los componentes. L1 es una cota inferior de lo ocular; L3 incluye residuo ocular.
- Las saturaciones entran en el puntaje ocular de cinco personas (P9, P18, P26, P35, P40) y lo atenúan.
- El modelo completo incluye variables que la limpieza no altera (fracciones de canal plano, saturado o utilizable, e indicadores de faltante). Parte de L3 puede venir de ahí. L4 no tiene ese problema.
- La frase del protocolo "solo puede restar información ligada a la mirada" es demasiado fuerte: quitar componentes también puede subir la AUC.
- `reg12` limpia poco (el acoplamiento horizontal no baja); queda como descriptivo.
