# Presentación breve del tema de tesis — 20-09-2026

Entregable: [HTML autocontenido](../presentaciones/Presentacion-Tema-Tesis-Autocontenida-20-09-2026.html).

Seis diapositivas: tema y profesor guía; antecedentes; objetivo general; síntesis
de los siete objetivos específicos; metodología; datos disponibles. Responde al
formato solicitado para presentar el tema, sin ampliar a resultados de los grids.

La portada identifica al Dr. Juan D. Velásquez como profesor guía, tal como indican
las notas y presentaciones previas. No se atribuye una coguía de tesis a la Dra.
Flavia Guiñazú: las fuentes revisadas documentan su codirección del proyecto Fondecyt.
La consulta opcional sobre ese rol no recibió respuesta durante la preparación.

El título sintetiza el tema vigente. El objetivo general sigue el alcance operacional
del índice Tesis_MDS; los siete específicos se resumen desde Estructura Tesis,
conservando el análisis descriptivo de fatiga/habituación. No se modifican los objetivos
originales ni se atribuye aprobación formal a una nueva redacción.

## Fuentes internas

- `01 Tesis MDS/CLAUDE.md`: contexto, profesor guía y separación de señales.
- `01 Tesis MDS/Tesis_MDS.md`: objetivo y estado vigente.
- `Escritura/Estructura Tesis.md`: antecedentes y siete objetivos específicos.
- `Marco Teorico/Problema e hipótesis.md`: problema temporal y de medición.
- `Analisis de Datos/DOCUMENTACION_DATOS_MDS.md`: registros y dispositivos.
- `Analisis de Datos/PREPROCESAMIENTO_MULTIMODAL.md`: señales, frecuencias y conteos.
- `Analisis de Datos/ETIQUETAS_Y_BASELINES.md`: pseudoetiquetas, evaluación y partición.
- CSV de características y partición guardados: cotejo de dimensiones y participantes.

## Verificación de entrega y accesibilidad

31 comprobaciones aprobadas mediante Edge, Playwright y axe-core 4.10.3.
El detalle está en `Verificacion_Presentacion_Tema_20-09-2026.json`, con hash del HTML.

- Copia del HTML en un directorio temporal, navegador offline y cero peticiones HTTP:
  el contenido funciona sin recursos, fuentes ni archivos externos.
- Navegación con botones, flechas, Inicio/Fin, selector, Tab/Shift+Tab y Espacio;
  orden y foco visibles comprobados. Todo el contenido permanece legible sin JavaScript.
- axe-core sin violaciones detectadas a 1440, 720 y 320 px. Contraste mínimo calculado
  de texto: 5,92:1. Foco verde azulado con el mismo contraste sobre el fondo claro.
- Revisión visual de las seis diapositivas y vista móvil. La tabla de datos se adapta
  a bloques por señal en pantallas estrechas para evitar palabras fragmentadas.
- Reflujo y espaciado de texto ampliado sin desborde horizontal; PDF temporal de seis
  páginas, una por diapositiva. Los límites de la auditoría se declaran en el JSON:
  no incluye lector de pantalla real ni zoom manual del navegador.

Hallazgo de usabilidad corregido: la tabla estrecha fragmentaba nombres de señales;
se agregó la presentación por bloques a 480 px o menos y se repitió la verificación.
No se detectaron hallazgos de accesibilidad pendientes en el alcance comprobado;
el resultado no constituye una certificación integral WCAG.

Reproducción: `python scripts/verificar_presentacion_20_09_2026.py`, con sus dependencias
y axe-core indicados en la cabecera. Capturas y PDF de prueba quedan en el directorio
temporal; solo el HTML es necesario para abrir y compartir la presentación.
