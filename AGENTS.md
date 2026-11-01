# Trabajo con la tesis MDS

Leer `respaldo_local/AGENTS.md`, `respaldo_local/notas/bitacora.md` y los protocolos de la corrida antes de experimentar. En este Mac, el espacio principal está dos niveles por encima del repositorio.

Mantener separadas las señales del profesor y estudiante. Comparar modelos sobre etiquetas y filas idénticas, con particiones por persona y selección interna. No ajustar modelos a partir de test. Registrar cada protocolo antes de entrenar y conservar corridas anteriores.

## Respaldo obligatorio solicitado por Mario — 01-11-2026

En cada etapa de experimentación: guardar código, configuración, protocolo, resultados, modelos, predicciones e informe; sincronizar notas/documentos con `python3 scripts/respaldar_espacio_local.py`; revisar cambios, crear commit y ejecutar `git push origin main`. Comprobar que `git ls-remote origin refs/heads/main` coincide con HEAD antes de declarar respaldo remoto completado. Si falla, informar explícitamente que solo hay copia local y reintentar en cuanto exista conexión. No usar force push.

No prometer sincronización automática en segundo plano: esta regla se aplica durante el trabajo del agente. Datos crudos externos, entornos, cachés y credenciales no se incluyen; documentar las exclusiones y las fuentes reproducibles. No eliminar resultados para hacer caber un push: resolver almacenamiento y dejar constancia si aparece un límite.
