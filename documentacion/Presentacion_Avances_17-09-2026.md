# Presentación de avances — 17-09-2026

Archivo: [Avances-Tesis-MDS-17-09-2026.html](../presentaciones/Avances-Tesis-MDS-17-09-2026.html).

14 diapositivas autónomas, sin dependencias de red, con navegación por botones,
flechas, selector, lectura continua e impresión completa. Conserva el lenguaje
visual académico de la presentación del 06-09: blanco, azul oscuro y verde azulado.
No reemplaza presentaciones anteriores ni modifica modelos o resultados.

Contenido: objetivos profesor/estudiante, evaluación por participantes, recorrido
experimental, comparación de grids, control de historia, ablación, PCA, clase media,
reproducibilidad y propuestas pendientes. Distingue activación de atención y el
máximo secundario de ablación de una mejora confirmada. Fuentes enlazadas al cierre.

## Verificación

- Microsoft Edge headless mediante Playwright: 22 comprobaciones aprobadas.
- axe-core 4.10.3: cero violaciones detectadas en lectura completa a 1440, 720 y
  320 píxeles, con reglas WCAG 2 A/AA, 2.1 AA y 2.2 AA.
- Navegación por flechas, Inicio/Fin, selector, lectura continua y recorrido Tab
  hasta los enlaces de fuentes. Foco visible y controles nativos con nombre.
- Revisión visual de capturas de comparación, modalidades, portada y conclusiones;
  comparación también revisada a 320 píxeles. Sin recortes horizontales.
- Reflujo a 720 píxeles como aproximación de viewport al zoom 200 % y espaciado
  de texto ampliado a 320 píxeles. No se hizo una prueba manual del zoom del navegador.
- PDF temporal verificado: 14 páginas con contenido, una por diapositiva.
- Enlaces locales existentes, sin errores JavaScript, lectura completa sin JavaScript.
- BA de los tres grids cotejada automáticamente con CSV; ablaciones, PCA y
  contrastes cotejados con los informes y tablas guardados.

No se observaron hallazgos bloqueantes en el alcance revisado. La revisión de teclado
se ejecutó por automatización del navegador; no se probó un lector de pantalla real.
Esta verificación no es una certificación integral de accesibilidad.

El script `scripts/verificar_presentacion_17_09_2026.py` guarda el detalle en
`Verificacion_Presentacion_17-09-2026.json`. Requiere Python, Playwright, Microsoft Edge
y una copia de axe-core 4.10.3 en `%TEMP%/mds-presentation-audit/axe.min.js`.
Las capturas y el PDF de prueba quedan en ese directorio temporal.

No se ejecutaron nuevos entrenamientos ni se reevaluaron validation/test.
