# Revisión de objetivos y metodología KDD — 22-09-2026

A solicitud de Mario, se reemplazaron en sus rutas originales el [HTML del tema de tesis](../presentaciones/Presentacion-Tema-Tesis-Autocontenida-20-09-2026.html) y el [PowerPoint editable](../presentaciones/Presentacion-Tema-Tesis-Autocontenida-20-09-2026.pptx). Se mantienen seis diapositivas. La fecha del nombre identifica el entregable original; el contenido declara la revisión del 22-09-2026.

## Objetivos revisados

El objetivo general pasa a evaluar el aporte predictivo de la temporalidad y la fusión, con comparación en participantes no utilizados para ajustar los modelos. La formulación hace explícito que se predicen pseudoetiquetas y permite contrastar la hipótesis sin presuponer superioridad de los modelos temporales.

Los siete específicos articulan revisión de evidencia, caracterización de señales, operacionalización de las variables, comparación predictiva, cuantificación de aportes por ablación, descripción intra-sesión y contraste con incertidumbre entre participantes. Se conserva el análisis descriptivo de fatiga/habituación y la separación entre señales de etiquetado y predicción. La estabilidad de una pseudoetiqueta no se presenta como validación fisiológica externa.

La redacción íntegra del HTML coincide con `01 Tesis MDS/Escritura/Estructura Tesis.md`. El índice `Tesis_MDS.md` incorpora el mismo objetivo general. Se reemplaza la formulación del 17-08-2026 por solicitud del usuario; no se atribuye aprobación académica formal al profesor guía.

## Elección y adaptación de KDD

Se eligió KDD porque ya estaba previsto en el esquema de la tesis y permite organizar la investigación sobre un corpus existente, desde la selección de registros hasta la evaluación e interpretación. Esta elección es una adaptación al trabajo, no una exigencia del artículo original.

La diapositiva resume cinco bloques: **selección → preprocesamiento → transformación → minería de datos → interpretación y evaluación**. El proceso es iterativo dentro del desarrollo. El capítulo metodológico documenta las particiones por participante, el ajuste interno de hiperparámetros y transformaciones aprendidas, las comparaciones con etiquetas fijas y la reserva de la evaluación final.

**Fuente primaria consultada:** Fayyad, U., Piatetsky-Shapiro, G., & Smyth, P. (1996). *From Data Mining to Knowledge Discovery in Databases*. AI Magazine, 17(3), 37–54. DOI: [10.1609/aimag.v17i3.1230](https://doi.org/10.1609/aimag.v17i3.1230). [Texto en el sitio del autor](https://fayyad.com/from-data-mining-to-knowledge-discovery-in-databases/), consultado el 22-09-2026. El artículo desarrolla nueve pasos; la presentación utiliza una síntesis en cinco bloques y la identifica como adaptación.

Se corrigió además la remisión del apartado «Modelos Profesores» a un enfoque facial descartado: ahora señala el diseño vigente de la Toma de Muestra 2. Esta revisión documental no ejecuta nuevos experimentos ni cambia etiquetas o resultados. Las búsquedas adaptativas previas conservan su carácter exploratorio; el marco KDD no las transforma en evidencia confirmatoria.

## Verificación

- HTML: 31 comprobaciones aprobadas, funcionamiento offline, navegación y seis páginas de impresión. axe-core no detectó violaciones a 320, 720 y 1440 píxeles.
- PPTX: seis láminas 16:9 con textos y formas editables; todo el texto visible del HTML preservado. Apertura y renderizado con Microsoft PowerPoint y PDF temporal de seis páginas.
- Se corrigieron el ancho de los textos de las etapas KDD y el espaciado entre objetivos. Renderizado final sin desbordamientos de texto con tolerancia de dos puntos.
- Se cotejaron el objetivo general y los siete específicos con las notas; se verificaron los hashes del HTML y del PPTX. Se revisaron visualmente las láminas modificadas y la vista móvil.
- No se probó la importación dentro de Canva ni un lector de pantalla real. Las versiones anteriores permanecen en el historial de Git.

Informes: `Verificacion_Presentacion_Tema_22-09-2026.json` y `Verificacion_PPTX_Tema_22-09-2026.json`. Los informes del 20-09 se conservan como evidencia histórica.

Reproducción: `python scripts/verificar_presentacion_20_09_2026.py`, `python scripts/convertir_tema_tesis_pptx_20_09_2026.py` y `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verificar_pptx_tema_20_09_2026.ps1`. Los scripts conservan sus nombres y generan los informes de la revisión del 22-09. Capturas y PDF de prueba quedan en el directorio temporal.
