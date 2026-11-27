# Pendientes para cerrar la tesis — lista única (26-11-2026)

**Qué es.** La lista de todo lo que sigue abierto, reunida en un solo lugar a partir de los documentos vigentes. No agrega pendientes nuevos ni resuelve ninguno: dice qué falta y en qué documento está el detalle.

**Cuándo se armó.** El 26-11-2026, durante el bucle de revisión (`notas/loop-revision-26-11-2026.md`), a partir de la auditoría de coherencia entre documentos (`repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/ronda5/COHERENCIA_FINAL.md`, sección 6) y con el estado de los documentos después de aplicar sus correcciones.

**Estado de las decisiones.** Ninguna decisión está tomada. No hay aprobación registrada del profesor guía sobre los resultados de noviembre, el margen de 0,02 ni el encuadre. Lo único que consta en la bitácora es que Mario comunicó el 01-11-2026 que el profesor aprobó usar las etiquetas GSR V2.

**Abreviaturas de las rutas** (relativas a `tesis-mds/`):

| Sigla | Documento |
|---|---|
| MI | `documentos/01 Tesis MDS/Avances/Avance - 23-11-2026 (Minuta de decisiones con el profesor).md` |
| RD | `documentos/01 Tesis MDS/Escritura/Borrador Resultados y Discusión 23-11-2026.md` |
| CO | `documentos/01 Tesis MDS/Escritura/Borrador Conclusiones 23-11-2026.md` |
| SP | `documentos/01 Tesis MDS/Escritura/Borrador Secciones pendientes 23-11-2026.md` |
| CI | `repos/Tesis_MDS/documentacion/Cierre_Experimental_Final_23-11-2026.md` |
| DIS | `documentos/01 Tesis MDS/Diseno Metodologico/Resumen Diseño Etiquetas y Modelos.md` |
| ENS | `repos/Tesis_MDS/presentaciones/avances_tesis_06-11-2026/ENSAYO.md` |
| PRES | `repos/Tesis_MDS/presentaciones/avances_tesis_06-11-2026/relato.py` (genera `index.html` y `GUIÓN.md`) |
| REF | `repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/VERIFICACION_REFERENCIAS.md` |
| LOOP | `notas/loop-revision-26-11-2026.md` |
| ED | `repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/ronda4/REVISION_EDITORIAL.md` |

## A. Decisiones con el profesor guía

Son siete, con la numeración de la minuta. Ninguna está tomada. Opciones y consecuencias de cada una: MI, sección "Decisiones". Resumen: RD 8.10 y CI, "Queda abierto".

| # | Decisión | Detalle |
|---|---|---|
| 1 | Cohorte nueva o escribir con las personas ya registradas. | MI (decisión 1); tamaño de la cohorte en `repos/Tesis_MDS/resultados/protocolo_hipotesis_reintento_06-11-2026/INFORME.md` |
| 2 | Margen práctico de 0,02. | MI (decisión 2) |
| 3 | "Emociones" presentada como activación. | MI (decisión 3) |
| 4 | Etiqueta de atención original o corregida por posición. | MI (decisión 4); RD 7.2 |
| 5 | Encuadre: apoyo parcial más advertencia metodológica. Incluye con qué lectura del criterio de la hipótesis se llega a "apoyo parcial". | MI (decisión 5); RD 8.1; SP 4.8.3 |
| 6 | Etiquetas normalizadas con la sesión completa. | MI (decisión 6) |
| 7 | *Modelo Profesor* con PCA como definición del *Attention Score*. | MI (decisión 7); RD 6.1 |

## B. Otras decisiones de diseño

Casillas sin marcar en DIS. La quinta casilla de esa nota es la decisión 3.

| # | Pendiente | Detalle |
|---|---|---|
| 8 | Fusión y umbral del *Attention Score*. | DIS; MI, "Otros puntos abiertos del diseño" |
| 9 | Combinación de variables y umbral del *Arousal Score*. | DIS; MI, "Otros puntos abiertos del diseño" |
| 10 | Ventana de agregación de la GSR. | DIS; MI, "Otros puntos abiertos del diseño" |
| 11 | Validación externa de las etiquetas. | DIS; MI, "Otros puntos abiertos del diseño" |

## C. Texto del esqueleto que quedó en tensión con los resultados

El esqueleto (`documentos/01 Tesis MDS/Escritura/Estructura Tesis.md`) no se edita; lo que habría que cambiar está listado, sin decidir.

| # | Pendiente | Detalle |
|---|---|---|
| 12 | Hipótesis; objetivo general y objetivos 1 a 6; contribuciones 2 a 6 y la nota bajo ellas; "Metodología KDD"; "Experiencia Usuario"; 4.5.1; norte del proyecto en `CLAUDE.md` del vault. | MI, "Hipótesis, objetivos y contribuciones que conviene revisar" (18 filas) |
| 13 | Secciones no pendientes del esqueleto que quedaron desactualizadas: 4.4, 4.6.2 (filtros, ±150 µV, 273 características), 4.2 y 1.6, 5.1 y 5.2 ("21 de 48"). | SP, "Secciones no pendientes cuyo texto quedó desactualizado" |
| 14 | Métrica principal del manuscrito: AUC frente a BA, macro-F1 y *recall*. | SP 4.8.3 (nota sobre "Metodología KDD") |

## D. Información que hay que pedir al proyecto

Los datos son del proyecto Fondecyt 1231122. Sin estos documentos no se puede escribir la sección de participantes ni las consideraciones éticas.

| # | Pendiente | Detalle |
|---|---|---|
| 15 | Consentimiento informado y aprobación del comité de ética. | MI, "Información que hay que pedir al proyecto" |
| 16 | Reclutamiento, criterios de inclusión, edad y sexo. | MI, misma sección |
| 17 | Protocolo de estímulos y criterio con que se armaron los cuatro grupos. | MI, misma sección |
| 18 | Documentación del montaje de los electrodos. Los datos son compatibles con el montaje por defecto, pero eso no reemplaza el documento. | MI, misma sección (agregado el 26-11); RD 7.8; SP 4.5.2; `repos/Tesis_MDS/resultados/montaje_ocular_41p_23-11-2026/INFORME.md` |
| 19 | Unidad física de la GSR, que la exportación no declara. | MI, misma sección (agregado el 26-11); SP 4.7 |
| 20 | Revisión del emparejamiento de P29. | SP 4.3 y 4.6.1 |

## E. Norma del programa

| # | Pendiente | Detalle |
|---|---|---|
| 21 | Cómo declarar en la tesis el uso de asistentes automáticos. Las "auditorías" son revisiones y recálculos hechos con un asistente automático a pedido del autor; no son la revisión de un tercero. | MI, "Pregunta adicional: cómo declarar el uso de asistentes automáticos" |

## F. Lecturas y literatura

| # | Pendiente | Detalle |
|---|---|---|
| 22 | Leer en texto completo las 8 referencias contrastadas solo por resumen: Barry 2005 y 2007, Boucsein 2012, Critchley 2002, Croft y Barry 2000, Iwasaki 2005, Keren 2010 y Yuval-Greenberg 2008. | REF; CI, "Trabajo de cierre" |
| 23 | Confirmar en Critchley (2002) la base anatómica de la hipótesis de RD 8.5. Boucsein (2012) no está citada y está pendiente de lectura. | RD 8.5; REF |
| 24 | Volumen, número y páginas de las 18 referencias. | RD, "Referencias"; REF |
| 25 | Marco teórico (2.2 a 2.12) y 3.3, sin literatura verificada. | SP, "Secciones que siguen pendientes" |
| 26 | Repetir la búsqueda que sostiene "no encontré estas cuatro señales en navegación web" (lámina 7). | ENS; PRES (lámina 7) |
| 27 | Dejar explícito el signo con que entra cada variable en el *Attention Score*. | ENS, pregunta 15 |

## G. Elecciones de estilo y de edición que quedaron para el autor

| # | Pendiente | Detalle |
|---|---|---|
| 28 | Criterio escrito de "apoyo parcial" frente a la lectura más exigente que usa el borrador (ligado a la decisión 5). | RD 8.1; SP 4.8.3; MI (decisión 5); LOOP, "Puntos que quedan para Mario" |
| 29 | Párrafo nuevo sobre adaptación a la persona. | RD 8.5; LOOP |
| 30 | Cuáles son las limitaciones principales (RD 8.8 nombra cinco desde la ronda 4). | RD 8.8; LOOP |
| 31 | Definiciones de los dos placebos de la curva, tomadas del informe. | RD 6.2 (nota de trabajo); `repos/Tesis_MDS/resultados/reapertura_41p_22-11-2026/INFORME.md` |
| 32 | "Prueba" (SP) frente a "test" (RD, CO, CI, PRES). | SP; LOOP |
| 33 | Qué es "lo nuevo desde la última reunión" (lámina 2). | PRES (lámina 2); LOOP |
| 34 | Duración real de la reunión (el ensayo supone 20 minutos). | ENS, "Supuesto de duración" |
| 35 | Redacción de la pregunta de investigación 3 (SP 1.4) y si se mantiene el complemento 5.3. | SP 1.4 y 5.3; ED |
| 36 | Si se mantienen las subsecciones de CNN, ViT y transferencia del esqueleto. | SP, "Secciones que siguen pendientes" (2.7); ED |
| 37 | Láminas candidatas a pasar a anexos: 9, 12, 15 y 20. | ENS, "Plan de tiempo" |

## H. Trabajo de cierre

| # | Pendiente | Detalle |
|---|---|---|
| 38 | Revisar RD y pasarlo a LaTeX (redacción, citas, numeración). | CI, "Trabajo de cierre"; RD |
| 39 | Ajustar CO según las decisiones (9.1, 9.5, 9.6 y 9.7). | CO; MI, "Qué cambia en el texto según lo que se decida" |

## I. Experimentos opcionales, no corridos

No se propone correr ninguno. Solo si se piden.

| # | Pendiente | Detalle |
|---|---|---|
| 40 | Cohorte nueva. | MI (decisión 1); CI, "Queda abierto" |
| 41 | Sensibilidad del modelo de activación con 7 hojas o con selección anidada. | MI (decisión 1); CI, "Queda abierto"; PRES (lámina 32); RD 7.5 |
| 42 | Red con el filtro de control. | CI, "Queda abierto"; RD 7.10 y 8.9 |
| 43 | Corrección del desfase entre EEG y seguidor ocular. | CI, "Queda abierto"; RD 7.8 y 8.9 |
| 44 | Modelo de referencia con variables escaladas por persona; evaluación dejando grupos completos fuera; mínimo de ventanas por persona; indicador de movimiento. | RD 8.9 (como trabajo futuro) |
| 45 | Estabilidad de las pseudoetiquetas y evolución en la sesión con el score continuo (objetivos 3 y 6). | MI, "Hipótesis, objetivos y contribuciones que conviene revisar" (filas del objetivo 3 y de la contribución 6) |

## Pendientes que un documento daba por resueltos y otro por abiertos

Estado después de las correcciones del 26-11 (ronda 4 del bucle).

| Pendiente | Dónde estaba la diferencia | Qué vale hoy |
|---|---|---|
| Predicciones idénticas en el enfoque E1 | La bitácora del 23-11 no descartaba un error; CI, RD 7.2 y LOOP ya tenían el diagnóstico. | Resuelto: no es un error (`repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/ronda2/DIAGNOSTICO_E1_POSICION.md`). La entrada del 26-11 de `notas/bitacora.md` lo deja dicho. |
| Advertencia de "análisis anterior" en los anexos A, B, D y E | La bitácora del 23-11 la daba por no hecha; PRES ya la lleva en los cuatro. | Resuelto. Registrado en la entrada del 26-11 de la bitácora. |
| Redondeo de dos rótulos de gráficos (−0,002 y +0,006) | La bitácora del 23-11 lo daba por no hecho. | No era un error de los gráficos: los CSV dan −0,0025 y +0,0065, y el redondeo doble es del INFORME. Registrado en la entrada del 26-11 de la bitácora. |
| Eje "(OOF)" de la lámina 12 | LOOP lo dejaba como pendiente menor; ENS decía que estaba corregido. | Resuelto: se corrigió en `estilo_tecnico.py` en la ronda 3 (commit `1abaa70`). LOOP ya lo cierra. |
| Lecturas pendientes | La bitácora del 23-11 listaba 4; CI, RD y SP, 8. | Valen las 8 (pendiente 22). |
| Sensibilidad con 7 hojas | MI y LOOP la listaban como experimento opcional; CI y la lámina 32, no. | Es un opcional más (pendiente 41). CI y la lámina 32 ya la listan. |
| Montaje de los electrodos | RD, SP y PRES lo dan por no documentado; MI no lo pedía al proyecto; `notas/resumen-ultimo-mes-22-11-2026.md` dice "resuelto en lo que permiten los datos". | Sigue faltando el documento (pendiente 18). MI ya lo pide. El resumen del mes conserva su frase: es un registro anterior a la auditoría y lleva aviso. |
| Número de decisiones | PRES y ENS contaban cinco, más dos al pie; los demás, siete. | Siete. La nota de la portada y la lista de "lo que no se puede decir" del ensayo ya dicen siete; el índice dice "las decisiones abiertas". La lámina 33 sigue mostrando cinco preguntas y las otras dos al pie, y conserva su título ("Necesito decidir cinco cosas con usted"). El plan de tiempo y el guion de la lámina 33 en ENS siguen hablando de "cinco decisiones", por las cinco de esa lámina. |
| Lectura del criterio de "apoyo parcial" | RD, SP, MI y LOOP la dan por abierta, dentro de la decisión 5; CO, CI, PRES y ENS no la mencionaban. | Abierta (pendiente 28). CI ya la menciona en la decisión 5. CO, PRES y ENS siguen sin mencionarla. |
