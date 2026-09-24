# Presentación visual del tema de tesis — 23-09-2026

Se reemplazaron el HTML y el PowerPoint del tema de tesis a solicitud de Mario. La nueva presentación tiene siete láminas y separa la explicación de KDD, la construcción de las etiquetas y la comparación de modelos. Se añadió una versión PDF.

Archivos: `presentaciones/Presentacion-Tema-Tesis-Autocontenida-20-09-2026` con extensiones `.html`, `.pptx` y `.pdf`. Se conserva el nombre para reemplazar las versiones que ya usa Mario; la portada declara la revisión del 23-09. La versión anterior permanece en Git, commit `da6152d`.

## Contenido

1. Tema, estudiante, profesor guía y antecedentes, con un esquema de señales a lo largo de una sesión.
2. Datos disponibles: cuatro modalidades, 48 registros de participantes, conjunto principal de 41 y partición 25/8/8. Se explican EEG, GSR, seguimiento ocular y pupilometría.
3. Objetivo general, acompañado por un dibujo que compara una ventana con una secuencia.
4. Siete objetivos específicos, conservados íntegros desde `Estructura Tesis.md`. Se define ablación.
5. KDD: cada etapa indica qué se hace en la tesis y qué se obtiene. Una flecha de retorno muestra que el proceso admite revisión dentro del desarrollo.
6. Dos rutas de pseudoetiquetado: señales del Modelo Profesor y señales del Modelo Estudiante para atención y activación. Se define pseudoetiqueta y se explica la separación de señales.
7. Fusión temprana, intermedia y tardía mediante esquemas; condiciones de comparación y significado de BA, recall y macro-F1.

Los dibujos explican el diseño. Las curvas de la portada son ilustrativas y están identificadas como tales; no representan registros ni resultados experimentales. Los conteos proceden de los archivos guardados. Los modelos y las métricas de experimentos anteriores no se modificaron.

## Diseño y fuentes

Se usaron Cambria para títulos y Arial para cuerpo, fondo blanco, texto azul oscuro y diagramas en azul y verde azulado. La presentación cambia bloques de prosa por conexiones, secuencias y relaciones entre señales. Los números se reservan para los objetivos, el orden de KDD y los conteos de datos. La redacción formal de objetivos se mantiene; se simplifican las explicaciones que los rodean.

KDD se presenta como adaptación en cinco bloques de Fayyad, Piatetsky-Shapiro y Smyth (1996), *From Data Mining to Knowledge Discovery in Databases*, AI Magazine 17(3), 37–54. DOI: [10.1609/aimag.v17i3.1230](https://doi.org/10.1609/aimag.v17i3.1230). [Fuente primaria consultada el 22-09](https://fayyad.com/from-data-mining-to-knowledge-discovery-in-databases/). Las cinco etapas de la lámina sintetizan el proceso; no reemplazan su carácter iterativo.

Fuentes internas: `Estructura Tesis`, `Tesis_MDS`, `CLAUDE.md` de tesis, `PREPROCESAMIENTO_MULTIMODAL`, `particion_participantes.csv` y `caracteristicas_multimodales.csv`. Se aplicaron las guías locales `frontend-design`, `no-ai-slop` y `a11y-audit`.

## Archivos y reproducción

El HTML contiene estilos, navegación y gráficos vectoriales; funciona sin conexión ni archivos auxiliares. En pantallas pequeñas, el contenido se presenta como lectura continua dentro de cada lámina y los diagramas se explican en texto. El PPTX contiene texto, formas y conectores editables, generados desde la misma composición que el HTML. El PDF permite compartir la presentación con su formato fijo.

- Generar: `python scripts/generar_tema_visual_23_09_2026.py`.
- Verificar HTML: `python scripts/verificar_presentacion_20_09_2026.py`.
- Renderizar y exportar PDF: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verificar_pptx_tema_20_09_2026.ps1`.

La entrada `convertir_tema_tesis_pptx_20_09_2026.py` delega en el generador vigente. Para regenerar se requieren python-pptx, el vault contiguo con `Escritura/Estructura Tesis.md` y, para las verificaciones, Playwright, Edge, PyMuPDF, axe-core y PowerPoint. Los archivos entregados no requieren esas herramientas para su uso.

## Verificación

HTML: 34 comprobaciones aprobadas, incluyendo funcionamiento offline, cero peticiones HTTP, siete diagramas vectoriales incluidos, siete objetivos, cinco etapas KDD, texto dentro de los espacios asignados y PDF de siete páginas. Se comprobaron navegación por teclado, foco, contraste, reflujo y espaciado de texto. axe-core no detectó violaciones en 1440, 720 y 320 píxeles.

PowerPoint: apertura y renderizado real de siete láminas, con texto y formas editables. Se corrigieron el espacio de los objetivos y las sombras heredadas del tema; el renderizado final no presenta texto desbordado con tolerancia de dos puntos. El generador verifica el contenido de todos los cuadros y los límites del lienzo. Se revisaron visualmente las láminas y las versiones móviles de KDD, etiquetas y fusión. PDF final de siete páginas y hashes verificados.

Informes: `Verificacion_Presentacion_Tema_23-09-2026.json` y `Verificacion_PPTX_Tema_23-09-2026.json`. No se probó un lector de pantalla real ni la importación en Canva; la revisión automatizada no certifica accesibilidad integral.
