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
