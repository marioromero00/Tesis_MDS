# Diagnóstico de activación en train

Se conservan las 25 personas y las etiquetas binarias fijadas. Esta revisión no usa rendimiento de validation/test para cambiar datos.

- P4: GSR válido en 12,64 % de sus ventanas, pero 459/459 tienen etiqueta binaria. Los componentes tónico y fásico solo tienen 59 valores observados; los conteos SCR existen en las 459 ventanas. El profesor anterior promedia componentes disponibles sin aplicar una máscara de GSR válido por ventana. La admisión por persona exige únicamente alguna ventana GSR válida (`preparar_modelado.py`). Esto debilita la interpretación de la etiqueta.
- P34: solo 140 valores distintos de score6s en 536 ventanas; positivos 8,58 %, por los empates con la mediana. Sus componentes SCR son constantes. No se rompe el empate al azar ni se reequilibran las etiquetas.
- P46: positivos 33,33 %, también con valores repetidos. Una regla por mediana con empates a cero no garantiza dos clases de igual tamaño.
- La falta de variables EEG varía por persona: P27 aproximadamente 13,1 %, P35 11,8 %, P9 9,7 %. La imputación se ajusta dentro de cada partición de entrenamiento.
- El historial se reinicia al cambiar estímulo, segmento o ante un hueco. Promediando personas, el contexto8 dispone de 4,90 ventanas y solo 33,2 % alcanza ocho; contexto32 dispone de 7,82 ventanas y apenas 0,95 % alcanza 32. Por tanto, el contexto nominal de 33 segundos casi nunca está disponible íntegro.
- La correlación Spearman entre score2s y score6s varía aproximadamente entre 0,742 y 0,942. Esto mide sensibilidad al suavizado, no validez psicológica.

## Sincronización: alcance de la comprobación

La extracción EEG previa cotejó muestras y ventanas UTC contra los registros originales. Esta revisión conserva sus claves y la misma selección temporal. La cobertura de GSR muestra discontinuidades graves para P4. Ni cobertura ni igualdad de timestamps prueban por sí solas el alineamiento fisiológico de los dispositivos; no se ajustan offsets buscando mejorar AUC.

## Prioridad posterior a esta búsqueda

Definir un protocolo de sensibilidad de calidad docente que exija GSR suficiente y componentes definidos, con criterios basados en señales y antes de mirar su rendimiento. Reconstruir score y etiquetas de forma explícita, con denominadores y empates documentados. Mantener el análisis actual como referencia histórica; la versión corregida será otra definición de la tarea. Revisar también si el contexto elegido refleja la duración real de los segmentos.
