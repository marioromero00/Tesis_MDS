# Tesis MDS — espacio recuperado en este Mac

Restauración verificada: 01-11-2026. Se recuperaron los 80 archivos del respaldo del vault del 24-09-2026, sin modificar su contenido. El código, datos y resultados ya estaban presentes en este computador.

## Organización en este Mac

```text
tesis-mds/
├── repos/
│   ├── Tesis_MDS/               Código, resultados y presentaciones
│   └── 01 Tesis MDS → ../documentos/01 Tesis MDS
├── documentos/
│   └── 01 Tesis MDS/            Vault recuperado: escritura y notas históricas
├── notas/                      Bitácora, planificación y pautas actuales
└── datos/
    └── locales/                Datos de trabajo
```

La ubicación principal del vault es `documentos/01 Tesis MDS`. El enlace en `repos` mantiene compatibles las referencias del código y los informes históricos; apunta a los mismos archivos, sin duplicarlos. Los resultados y presentaciones del repositorio conservan sus rutas originales.

## Último cierre experimental

**Cuatro enfoques nuevos del 22-11-2026 (lo más reciente):** [informe](repos/Tesis_MDS/resultados/enfoques_41p_22-11-2026/INFORME.md). [Resumen del último mes](notas/resumen-ultimo-mes-22-11-2026.md).

**Reapertura del 22-11-2026:** [informe](repos/Tesis_MDS/resultados/reapertura_41p_22-11-2026/INFORME.md). Activación: efecto del historial confirmado (+0,036, respaldo) y de corto alcance (6–12 s). Atención: sin información temporal a ningún desfase. [Fase 3](repos/Tesis_MDS/resultados/reapertura_fase3_41p_22-11-2026/INFORME.md): con la posición como variable, el historial no agrega nada en atención (nulo concluyente) y en activación agrega +0,032, inconcluso tras Holm.

**Experimentación cerrada el 22-11-2026.** [Cierre final](repos/Tesis_MDS/documentacion/Cierre_Experimental_Final_22-11-2026.md): análisis con 41 personas, evidencia mixta con apoyo parcial (información temporal real en activación; en atención la mejora se explica por el tiempo transcurrido en el estímulo). Respaldado en GitHub. Lo pendiente es escritura y decisiones con el profesor guía.

Histórico: [Cierre V2 del 01-11-2026](repos/Tesis_MDS/documentacion/Cierre_Experimental_V2_01-11-2026.md).

## Para continuar

- [Índice original de la tesis](documentos/01%20Tesis%20MDS/Tesis_MDS.md).
- [Borrador recuperado](documentos/01%20Tesis%20MDS/Escritura/Estructura%20Tesis.md).
- [Reglas originales de trabajo](documentos/01%20Tesis%20MDS/CLAUDE.md).
- [Pautas de escritura recuperadas](notas/pautas-escritura-recuperadas.md).
- [Avances históricos](documentos/01%20Tesis%20MDS/Avances/).
- [Marco teórico](documentos/01%20Tesis%20MDS/Marco%20Teorico/).
- [Diseño de etiquetas y modelos](documentos/01%20Tesis%20MDS/Diseno%20Metodologico/).
- [Código y documentación experimental](repos/Tesis_MDS/README.md).
- [Presentaciones](repos/Tesis_MDS/presentaciones/).
- [Bitácora reciente, hasta el 01-11-2026](notas/bitacora.md).
- [Informe de recuperación y hashes](notas/restauracion-vault-01-11-2026.json).

Para usar las notas con sus enlaces `[[...]]`, abrir la carpeta `documentos/01 Tesis MDS` como vault en Obsidian. También se pueden editar como Markdown. Las rutas antiguas `~/tesis/Tesis_MDS` corresponden aquí a `repos/Tesis_MDS`; se conservaron intactas en los documentos históricos.

## Versiones y límites de recuperación

El vault restaurado corresponde al respaldo del **24 de septiembre**, no al manuscrito de octubre. [El registro del 24 de octubre](repos/Tesis_MDS/documentacion/Presentacion_y_Manuscrito_24-10-2026.md) describe ampliaciones de metodología y capítulos 6–8, pero esa versión del manuscrito no fue localizada como archivo suelto ni en los respaldos ZIP disponibles. Recuperarla exactamente requiere una copia del equipo anterior u otro respaldo. No se inventó el texto faltante.

Los avances experimentales posteriores están conservados en `repos/Tesis_MDS/documentacion`, `repos/Tesis_MDS/resultados` y `notas/bitacora.md`. Para el estado actual, consultar esos informes antes del índice histórico del vault o el README del código (actualizado al 24-10).

El repositorio local está en `main`, commit `8ace73d`, con origen `https://github.com/marioromero00/Tesis_MDS.git`. Hay scripts, documentación y resultados locales sin incorporar a Git: conservarlos. No se hicieron commits, push ni cambios a esos experimentos. No se pudo comprobar si GitHub contiene versiones posteriores porque falló la resolución de `github.com`.

El archivo `notas/plan.md` es una plantilla antigua con el tema por definir; no describe el avance real. Usar los objetivos del borrador recuperado y la bitácora reciente.

La recuperación del manuscrito posterior a septiembre queda fuera del trabajo actual por indicación de Mario.
