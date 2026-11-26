# Bucle de revisión — 26-11-2026

Pedido por Mario el 26-11-2026 a las 18:57 (hora de Chile): revisar todo una y otra vez durante 15 horas, encontrar fallas, corregirlas y volver a revisar, hasta dejar todo cerrado. **Termina el 27-11-2026 a las 09:57.**

Reglas del bucle: no se entrenan modelos ni se agregan análisis; no se cierran decisiones del profesor; cada ronda termina con respaldo, commit y push verificado. Cada ronda la revisa un agente distinto del que corrigió.

## Rondas

### Ronda 1 — 26-11, 18:57

- Estado inicial: repositorio limpio, `HEAD` igual a `origin/main` (`af345a2`), sin cambios desde el 23-11.
- **Resuelto:** la duda de E1 (predicciones idénticas con y sin posición). Un ajuste de diagnóstico de un fold muestra que el modelo recibe la columna de posición y no la usa en ninguna de sus 1.800 divisiones; reproduce exactamente las predicciones guardadas. No es un error. Detalle en `documentacion/auditoria_final_23-11-2026/ronda2/DIAGNOSTICO_E1_POSICION.md`.
- En curso: tres auditorías independientes de segunda pasada (cifras del borrador de Resultados y Discusión; borrador de Secciones pendientes; coherencia entre cierre, conclusiones, discusión fisiológica, minuta y presentación).
- **Auditorías de segunda pasada (tres agentes independientes), sin tocar archivos:**
  - Borrador de Resultados y Discusión: ~1.015 cifras, ~990 coinciden; 0 bloqueantes, 12 importantes, 17 redondeos del tercer decimal. Error de hecho corregido: las cinco particiones del 22-11 son nuevas (no "tres ya vistas").
  - Borrador de Secciones pendientes: ~150 cifras contra código y datos, 3 difieren; 0 bloqueantes, 17 importantes (seis pasajes de método distintos del código), 20 menores. Dos imprecisiones del procesamiento congelado, ahora declaradas como límites: fracción de pupila con ambos ojos válidos calculada sobre todas las filas de la exportación; deduplicación de eventos oculares que pierde cerca de 0,2 % de las fijaciones.
  - Coherencia entre cierre, conclusiones, discusión fisiológica, minuta, presentación, READMEs y notas: cifras coinciden con los CSV; 2 bloqueantes, 46 importantes, 53 menores. Los bloqueantes eran un error introducido al corregir el 23-11: el +0,047 de activación a 6 s se describía como repetición con cinco particiones; es la curva temporal en una sola partición y 40 personas (verificado en `scripts/reapertura_41p.py`).
- **Correcciones aplicadas por agentes distintos de los auditores**, cada una comprobada en su fuente: 99 de 101 de coherencia más las dos del generador; 36 de 37 de Secciones pendientes (queda unificar "prueba"/"test", elección de estilo de Mario); todas las de Resultados y Discusión salvo dos de estilo global. La presentación se regeneró y se revisaron visualmente las láminas cambiadas. Las láminas 13 a 17 pasaron al capítulo "Las etiquetas". El cierre y las conclusiones listan ahora las siete decisiones de la minuta.
- Informes: `repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/ronda2/`.
- Respaldo de la ronda 1: commit `aef0f32`, `HEAD` igual a `origin/main`.

### Ronda 2 — 26-11, lanzada tras el respaldo

Tres revisiones con enfoques distintos de los de la ronda 1, por agentes nuevos y sin tocar archivos:

1. Verificación del diff `af345a2..aef0f32`: cada cambio contra la fuente primaria, por si alguna corrección introdujo errores.
2. Lectura crítica como miembro de comisión: argumento, validez, explicaciones alternativas, preguntas de defensa no preparadas.
3. Auditoría transversal del código que generó las predicciones (fugas entre personas, no-circularidad columna por columna, historial y controles, evaluación).

Resultados de la ronda 2:

- **Verificación del diff:** ~240 cambios revisados, 13 errores (0 bloqueantes, 4 importantes), casi todos correcciones no propagadas entre documentos. Aplicadas las 20 sustituciones.
- **Lectura crítica como comisión:** 7 bloqueantes, 24 importantes, 27 menores, 21 preguntas de defensa sin preparar. Los principales: el diseño con 41 personas se adoptó tras el resultado nulo del cierre V3 y no se decía al responder la hipótesis; la etiqueta PCA se eligió por ser más predecible; "sin los 6 s de la etiqueta" no vale para la señal porque el filtro tónico usa toda la sesión; "modelo temporal multimodal" sin operacionalización declarada; la contribución 3 del esqueleto queda refutada por la conclusión principal (va a la minuta, el esqueleto no se edita); falta información de participantes y ética.
- **Auditoría de código:** sin fuga entre personas ni fuga directa de etiqueta a entradas; reproduce el fold 0 del análisis final con diferencia 0,00. Cuatro hallazgos que afectan lecturas:
  - H1: las 15 hojas de activación se eligieron con el modelo con historial (contexto 32) sobre 25 de las 41 personas evaluadas; el efecto es +0,055 en esas 25 y +0,001 en las otras 16 (principal del 16-11). El contraste del historial desplazado frente al placebo es positivo en ambos grupos (+0,035 y +0,064). Sesgo posible, no demostrado.
  - H2: la etiqueta de activación es en lo esencial el nivel tónico de la GSR (AUC 0,911 solo con la componente tónica) y su soporte temporal excede los 6 s.
  - H3: en el profesor PCA la pupila casi no pesa (−0,052): la etiqueta de atención es conducta de mirada.
  - H4: las fijaciones se suman con su duración completa (27,7 % de las ventanas sobre 2.000 ms).
- **Aplicado** por un agente distinto de los auditores, verificando cada hecho en su fuente (INFORME, CSV, scripts, `git log`): los 7 bloqueantes y 24 importantes de la lectura de comisión y los hallazgos H1 a H4 del código, propagados a Resultados y Discusión, Conclusiones, Discusión fisiológica, Secciones pendientes, minuta, cierre, presentación y ensayo. El esqueleto `Estructura Tesis` no se tocó: lo que afecta a hipótesis, objetivos y contribuciones quedó en una sección nueva de la minuta (18 filas, sin decidir), junto con la información de participantes y ética que hay que pedir al proyecto. La sensibilidad con 7 hojas o selección anidada quedó listada como experimento opcional, sin correr.
- Dato nuevo comprobado al aplicar: dentro de cada grupo experimental el orden de los estímulos comunes coincide entre personas; la validación cruzada separa personas, no grupos (declarado como límite).
- `ENSAYO.md` quedó con 37 preguntas difíciles. Pendiente menor: el eje del gráfico de la lámina 12 dice "(OOF)".
- Respaldo de la ronda 2: commit `d2a90e8`, `HEAD` igual a `origin/main`.

### Ronda 3 — 26-11, 20:20

Tres revisiones nuevas, sin tocar archivos:

1. Verificación del diff `aef0f32..d2a90e8` contra las fuentes primarias (el agente que lo aplicó se interrumpió a medias: se busca además lo duplicado o a medio aplicar).
2. Revisión completa de las 39 láminas, visual y de contenido, y del ensayo con sus 37 preguntas.
3. Revisión editorial de los cuatro borradores y del cierre: tras cinco tandas de salvedades, buscar repeticiones, contradicciones de tono, frases a medio editar, material de proceso dentro de los capítulos y resultados descritos con menos fuerza de la que sus datos permiten.

Resultados de la ronda 3:

- **Verificación del diff de la ronda 2:** 391 líneas revisadas, 12 errores menores (un redondeo, cuatro frases desordenadas por la interrupción, propagaciones menores). Ningún hecho falso. Aplicados. Quedó confirmada en el script la dirección del desfase de reloj, y calculada la significación de la diferencia entre las 25 personas de la búsqueda y las otras 16 (p = 0,15 en el contraste principal; ninguno de nueve bajo 0,05).
- **Presentación completa:** 0 bloqueantes, 8 importantes, 22 menores. Sin texto cortado ni cifras erradas. El guion de 20 minutos tenía 3.120 palabras (no cabe) y 22 de 37 respuestas eran demasiado largas. En aplicación por un agente aparte.
- **Revisión editorial de los borradores:** el fondo coincide entre documentos, pero el resultado de activación se nombraba de seis maneras, cada límite se repetía hasta ocho veces y había material de proceso dentro de los capítulos. También encontró resultados descritos con MENOS fuerza de la que permiten sus datos: el contraste registrado del historial desplazado frente al placebo (+0,046, p Holm 0,004, positivo en ambos grupos de personas), la detección del *Attention Score* desde el EEG (41 de 41 personas antes y después de la limpieza) y la adaptación a la persona en activación (+0,045, registrado), que no se discutía.
- **Decisiones editoriales tomadas en el bucle (reversibles; copia previa en `documentacion/auditoria_final_23-11-2026/ronda4/pre_editorial/`):** una sola versión de la discusión fisiológica, integrada al capítulo 8 del borrador de Resultados y Discusión (el archivo de Discusión fisiológica se conserva como registro); "cerca de un tercio" para la contribución ocular; "respaldo" solo como rótulo de la regla registrada y "apoyo parcial" solo para la hipótesis; una sola numeración de las siete decisiones abiertas, la de la minuta; material de proceso a notas de trabajo y a un anexo de trazabilidad, sin borrar nada.
- **Aplicado en la ronda 3:** las 12 correcciones de la verificación; los 8 importantes y 22 menores de la presentación (guion hablado de 3.120 a 2.717 palabras, máximo 150 palabras por minuto; versión corta en 22 respuestas; pie con las decisiones 6 y 7 en la lámina 33; 16 láminas revisadas visualmente); y la revisión editorial de los cuatro borradores. El borrador de Resultados y Discusión tiene índice nuevo (6.1–6.6, 7.1–7.12, 8.1–8.10, referencias y anexo de trazabilidad) e integra la discusión fisiológica. Comprobación de equivalencia del editor: 0 cifras faltantes y 0 cifras nuevas de fondo (`ronda4/comprobar_equivalencia.py`).
- Vocabulario y numeración de las siete decisiones unificados también en cierre, minuta y READMEs.
- **Puntos que quedan para Mario** (no se resolvieron): criterio escrito de "apoyo parcial" frente a la lectura más exigente que usa el borrador; el párrafo nuevo sobre adaptación a la persona (RD 8.5); cuáles son las tres limitaciones principales (RD 8.8); definiciones de los dos placebos tomadas del informe; "prueba" frente a "test"; qué es "lo nuevo desde la última reunión" (lámina 2).
