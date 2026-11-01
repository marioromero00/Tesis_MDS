# Avance — 06-09-2026: Presentación de resultados baseline

> Fuente: `metricas_baselines.csv`, `manifiesto_baselines.json` y `verificacion_entrega.json`
> de `Tesis_MDS/resultados/modelado/ejecuciones/baselines_05-09-2026_02/`;
> documentación del pipeline del 22-08-2026; revisión del HTML el 06-09-2026.
> Reemplaza como fuente de contenido vigente del HTML a
> [[Avance EDA y Sincronizacion - 15-08-2026]].

## Resultado

Se actualizó el HTML existente `presentaciones/avance-eda-sincronizacion-15-08-2026.html`,
conservando su nombre y diseño académico azul. Pasó de diez a **16 diapositivas**.
La portada ahora dice «De datos crudos a baselines evaluados» y está fechada 06-09-2026.
Los resultados mantienen la fecha de entrenamiento, 05-09-2026.

Las nueve primeras láminas conservan contexto, pipeline, sincronización y EDA. Se actualizaron
el EEG a 44/48 (91,67 %), la exclusión P25 y recuperación P48, el estado de P29 como
sensibilidad y el contexto GSR de 6 s. Se corrigieron cuatro rutas de imágenes que todavía
apuntaban a una subcarpeta eliminada durante la consolidación.

## Nuevas láminas

| Diapositiva | Contenido |
|---|---|
| 10 | Profesor/estudiante, partición 25/8/8 y alcance offline |
| 11 | Dummy, Ridge, logística y Random Forest; 30 modelos en cinco tareas |
| 12 | Clasificación: BA de validación y prueba, F1 macro de prueba, objetivos principales |
| 13 | Regresión: R², MAE y RMSE de prueba, objetivos principales |
| 14 | Sensibilidad: atención PCA, activación 2 s y activación PCA |
| 15 | Guardado: 30 pipelines, recarga idéntica, diez pruebas y 90 filas de métricas |
| 16 | Próximo contraste con TCN, manteniendo etiquetas y partición |

Las tablas distinguen métricas agregadas sobre ventanas de métricas por participante.
P29 no entra en las tablas de prueba. El cierre reporta desempeño estático cercano al Dummy;
no presenta estos resultados como evidencia a favor o en contra de la hipótesis temporal.

## Verificación

- Las 45 celdas numéricas fueron contrastadas con el CSV de métricas, a cuatro decimales.
- Chrome mediante Playwright: 16 diapositivas revisadas en 1280×720 y 320×800.
- Sin errores JavaScript, imágenes rotas, desbordamientos de contenido ni títulos recortados
  detectados en esos tamaños.
- axe-core: cero infracciones de las reglas WCAG 2 A/AA, 2.1 AA y 2.2 AA evaluadas.
- Revisión visual de portada, protocolo, resultados, sensibilidad y próximos pasos.
- Teclado: Tab, Espacio, flechas, Inicio y Fin; foco visible y botones de 44×44 px.
- Las diapositivas inactivas quedan ocultas para tecnologías de asistencia; el cambio de
  diapositiva se anuncia y la numeración muestra 16 páginas.
- Movimiento reducido respetado; impresión muestra las 16 diapositivas.
- Comprobación adicional de reflow en 640×360 sin desbordamiento horizontal.

El reporte conserva la huella SHA256 del HTML:
[[Auditoria Presentacion Baselines - 06-09-2026.json]]. Los controles automatizados se
complementaron con inspección visual; no constituyen una certificación integral de accesibilidad.

## Notas relacionadas

- [[Tesis_MDS]]
- [[Avance - 05-09-2026 (Baselines Entrenados y Guardados)]]
- [[ETIQUETAS_Y_BASELINES]]
- [[Avance EDA y Sincronizacion - 15-08-2026]]
