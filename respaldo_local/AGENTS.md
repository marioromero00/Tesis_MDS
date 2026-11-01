# Contexto de tesis MDS en este Mac

Antes de trabajar, leer README.md en esta carpeta y notas/bitacora.md para distinguir el material histórico del estado experimental reciente.

Para escritura, leer `documentos/01 Tesis MDS/CLAUDE.md` (reglas originales recuperadas) y `notas/pautas-escritura-recuperadas.md`. Conservar los pendientes reales y las decisiones científicas abiertas; no inventar texto histórico, citas, resultados ni aprobación del profesor.

El vault se restauró desde el respaldo del 24-09-2026. El manuscrito ampliado del 24-10-2026 está mencionado en informes, pero no se recuperó su texto exacto. No confundir esas versiones.

Código: `repos/Tesis_MDS`. Escritura: `documentos/01 Tesis MDS`. Datos: `datos`. Notas recientes: `notas`.

Preservar los archivos locales no versionados y los experimentos existentes. No relanzar entrenamientos para recuperar documentación. Registrar las fuentes y la fecha de cualquier síntesis nueva. No modificar las pseudoetiquetas ni el diseño científico como parte de una tarea de restauración.

Organización actual: el vault está en `documentos/01 Tesis MDS`; `repos/01 Tesis MDS` es un enlace de compatibilidad. Usar la ubicación principal para nuevas referencias. Mantener código, resultados y presentaciones versionadas dentro de `repos/Tesis_MDS` y datos locales en `datos/locales`. Mario indicó que no necesita recuperar ahora las ampliaciones del manuscrito de octubre.

## Respaldo obligatorio solicitado por Mario — 01-11-2026

En cada etapa de experimentación: guardar código, configuración, protocolo, resultados, modelos, predicciones e informe; sincronizar notas/documentos con `python3 scripts/respaldar_espacio_local.py`; revisar cambios, crear commit y ejecutar `git push origin main`. Comprobar que `git ls-remote origin refs/heads/main` coincide con HEAD antes de declarar respaldo remoto completado. Si falla, informar explícitamente que solo hay copia local y reintentar en cuanto exista conexión. No usar force push.

No prometer sincronización automática en segundo plano: esta regla se aplica durante el trabajo del agente. Datos crudos externos, entornos, cachés y credenciales no se incluyen; documentar las exclusiones y las fuentes reproducibles. No eliminar resultados para hacer caber un push: resolver almacenamiento y dejar constancia si aparece un límite.
