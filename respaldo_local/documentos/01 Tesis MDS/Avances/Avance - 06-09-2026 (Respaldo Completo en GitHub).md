# Avance — 06-09-2026: Respaldo completo de tesis en GitHub

> Fuente: estado local de Git, consulta del remoto y `git push origin main` completado
> el 06-09-2026. Solicitud expresa de Mario de subir todo el trabajo de la tesis.

## Publicación verificada

Repositorio: https://github.com/marioromero00/Tesis_MDS, público, rama `main`.
El commit `8757e98470724947884b138f006ae2f9d86ba56b` se publicó y su hash se verificó
mediante `git ls-remote`.

Incluye código de entrenamiento, diez pruebas, los 30 modelos `.joblib`, sus metadatos,
predicciones, métricas, manifiestos y configuración. La presentación de 16 diapositivas
está en `presentaciones/`, con las cuatro imágenes que utiliza en `attachments/`.

`documentacion/Tesis_Vault_06-09-2026.zip` contiene una copia completa de la sección
`01 Tesis MDS`, con notas y adjuntos. El inventario adyacente registra tamaño y SHA256
de cada archivo. Se actualiza también para incluir esta bitácora de publicación.
Las ausencias previas de documentos y figuras en el árbol del repositorio quedaron
registradas como parte de la consolidación; el contenido del vault está preservado en el ZIP.

## Integridad

- Se verificaron 35 hashes contra los objetos preparados en Git: 30 modelos y cinco
  entradas/archivos del entrenamiento.
- `.gitattributes` preserva los bytes de dataset, partición y artefactos de ejecución.
  Esto evita que la conversión CRLF/LF invalide los hashes al descargar desde otro sistema.
- HTML copiado idéntico al del vault; archivo ZIP reabierto y verificado entrada por entrada.
- La ejecución incompleta queda solo en local. Datos crudos, credenciales y cachés conservan
  su exclusión.

## Diferencia entre respaldo y sincronización

Este Git pertenece a `C:/Users/MarioRomero/Desktop/MDS/Tesis_MDS`, no a la raíz de la bóveda.
El ZIP es una copia del contexto de tesis en esa fecha; no mantiene sincronizados los archivos
que Obsidian abre en dos equipos. Las secciones Vinson e Inglés y `.obsidian` no se publicaron.

La bóveda abierta en este PC es `C:/Users/MarioRomero/Desktop/MDS`. El complemento de
Obsidian Sync figura habilitado, pero no se verificó su conexión a una bóveda remota ni la
configuración del otro equipo. Por eso no se afirma que ambas copias estén sincronizadas.

## Notas relacionadas

- [[Tesis_MDS]]
- [[Avance - 05-09-2026 (Baselines Entrenados y Guardados)]]
- [[Avance - 06-09-2026 (Presentacion Resultados Baselines)]]
