# Últimos avances en cinco diapositivas — 21-09-2026

- [HTML autocontenido](../presentaciones/Avances-Resumen-Autocontenido-21-09-2026.html).
- [PowerPoint editable](../presentaciones/Avances-Resumen-Autocontenido-21-09-2026.pptx).

Síntesis de los experimentos cerrados al 14-09-2026: trabajo completado, comparación
de grids, control temporal, ablación/PCA y próximos pasos. No hubo nuevos experimentos
entre ese cierre y esta presentación. La versión de 14 diapositivas se conserva.

Los valores de BA, barras e intervalos se generan desde `resumen.csv` y `contrastes.csv`
de los grids recurrentes y `resumen_ablaciones.csv`. El valor de Transformer se recupera
del contraste auditado contra TCN y se cotejó con su informe. Otras fuentes:
`Grid_BiLSTM_LSTM_TCN_13-09-2026.md`, `Grid_Transformer_13-09-2026.md` y
`Ablacion_PCA_12-09-2026.md`. Se distinguen los resultados exploratorios de la
confirmación pendiente, y el alcance reciente de activación frente a atención.

## Verificación

HTML: 35 comprobaciones aprobadas, cinco diapositivas, copia aislada offline, cero
dependencias externas, navegación por teclado, lectura sin JavaScript, contraste
calculado, espaciado ampliado y reflujo a 320/720/1440 píxeles. axe-core 4.10.3 sin
violaciones detectadas en los tres anchos. Impresión de cinco páginas. Revisión
visual de las cinco láminas y de móvil. No se usó lector de pantalla real ni zoom
manual; no se declara certificación integral de accesibilidad.

PPTX: cinco diapositivas 16:9 con texto y formas editables; todo el texto del HTML
preservado, sin imágenes de diapositivas ni relaciones externas. Apertura y renderizado
en PowerPoint, revisión visual y PDF temporal de cinco páginas. Se amplió un cuadro
de texto en la lámina de ablación y se repitió la revisión: cero desbordamientos con
tolerancia de dos puntos. No se realizó una importación en Canva.

Generadores y verificadores fechados 21_09_2026 en `scripts/`; informes JSON
`Verificacion_Avances_Breves_21-09-2026` y `Verificacion_PPTX_Avances_Breves_21-09-2026`.
Los HTML/PPTX entregados funcionan de forma independiente; los generadores usan las
fuentes del repositorio. Capturas y PDF de prueba permanecen en el directorio temporal.
