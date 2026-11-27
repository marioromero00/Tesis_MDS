# Coherencia final entre documentos — ronda 5 (26-11-2026)

Auditoría de lectura y cotejo, hecha con un asistente automático a pedido del autor; no es la revisión de un tercero. No se editó ningún archivo existente, no se entrenó ningún modelo y no se hizo ningún commit. `HEAD` = `origin/main` = `1abaa70`. En ese commit, las copias de `repos/Tesis_MDS/respaldo_local/` son idénticas a los originales de `documentos/` y `notas/`; después de la tanda de las 20:58 ya no lo son y hay que volver a sincronizarlas.

Numeración: esta carpeta se llama `ronda5` y corresponde a la cuarta ronda del bucle de revisión (las carpetas llevan un número más que las rondas del registro `notas/loop-revision-26-11-2026.md`).

## 1. Resultado

- **Cifras.** 76 hechos cotejados contra los CSV y las fuentes primarias en 11 columnas de documentos. Ninguna cifra vigente difiere de su valor canónico. Las únicas cifras distintas están en entradas antiguas de la bitácora (un límite de intervalo con redondeo doble y un +0,047 que la lámina ya no usa).
- **Correcciones propuestas: 50** — 0 bloqueantes, 13 importantes y 37 menores (49 sustituciones de texto exacto y una entrada nueva en la bitácora, que cuenta como importante).
- **Lo que más separa a los documentos** no son las cifras sino cuatro cosas: (1) el cierre y la lámina 33 todavía dicen "al menos" para la contribución ocular, y los dos README dicen que un tercio "es ocular" y que la auditoría la hizo "un agente independiente"; (2) la presentación y el ensayo cuentan cinco decisiones y los demás siete; (3) dos pendientes no están en el documento donde se actúa: la lista de lo que hay que pedir al proyecto (minuta) no incluye el montaje ni la unidad de la GSR, y la lista de experimentos opcionales del cierre y de la lámina 32 no incluye la sensibilidad con 7 hojas; (4) la bitácora no tiene ninguna entrada del 26-11 y deja como pendientes cuatro cosas que ya se resolvieron.
- **Estado auditado.** Commit `1abaa70` más la tanda de correcciones que se aplicó a las 20:58 del 26-11 sobre RD, CO, SP, la minuta y el ensayo mientras se hacía esta auditoría (sección 5). Todo se volvió a comprobar contra los archivos tal como estaban a las 21:01.
- **Remisiones y enlaces.** Todas las remisiones a secciones de RD (desde CO, SP, la minuta, el ensayo y el registro del bucle) apuntan a secciones que existen con la numeración nueva y con el contenido que se les atribuye. Ningún wikilink ni ruta citada apunta a un archivo inexistente. Tres remisiones apuntan a la versión no vigente (Discusión fisiológica).
- **Presentación.** `index.html` y `GUIÓN.md` coinciden con `relato.py`; 39 láminas, 37 preguntas, 22 con versión corta; el guion hablado tiene 2.717 palabras y ninguna lámina pasa de 150 por minuto; los tiempos suman 1.200 s y 600 s.

## 2. Tabla maestra de hechos

Columnas: RD = Borrador Resultados y Discusión; CO = Conclusiones; SP = Secciones pendientes; CI = cierre del 23-11; MI = minuta; PRES = `relato.py` (y con él `GUIÓN.md`, `index.html`, `LEEME.md`); ENS = `ENSAYO.md`; README = los dos README (del repositorio, solo las secciones vigentes); RES = resumen del último mes; BIT = bitácora desde el 23-11; LOOP = registro del bucle. "igual" = aparece con el valor, el rótulo y el análisis de origen canónicos; "—" = no aparece. `notas/sustento-fisiologico-23-11-2026.md`, el borrador de Discusión fisiológica y los dos documentos reemplazados se tratan en la sección 5.

| # | Hecho | Valor canónico | Fuente | RD | CO | SP | CI | MI | PRES | ENS | README | RES | BIT | LOOP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Atención, historial − sin historial, una partición (16-11) | +0,026 [+0,018; +0,035]; 36/41; p Holm 0,00001; respaldo | resultados/cierre_final_41p_16-11-2026/contrastes.csv | igual | — | igual | igual | — | igual | igual | — | igual | — | — |
| 2 | Atención, historial − sin historial, cinco particiones (22-11) | +0,029 [+0,021; +0,037]; 36/41; efecto relevante | resultados/reapertura_41p_22-11-2026/confirmatorio.csv (P1) | igual | igual | — | igual | — | igual | igual | — | — | igual | — |
| 3 | Activación, historial − sin historial, una partición (16-11) | +0,034 [−0,001; +0,069]; 24/41; p Holm 0,066; inconcluso | resultados/cierre_final_41p_16-11-2026/contrastes.csv | igual | igual | — | igual | — | igual | igual | — | igual | — | — |
| 4 | Activación, historial − sin historial, cinco particiones (22-11) | +0,036 [+0,010; +0,065]; 23/41; p Holm 0,021; respaldo | resultados/reapertura_41p_22-11-2026/confirmatorio.csv (P1) | igual | igual en cifra; rótulo en forma verbal: «quedó respaldado» | — | igual | — | igual | igual | igual | igual | igual | — |
| 5 | Atención con tiempo de sesión (P2, 22-11) | +0,032 [+0,024; +0,040]; 37/41; efecto relevante | resultados/reapertura_41p_22-11-2026/confirmatorio.csv (P2) | igual | — | — | — | — | — | — | — | — | — | — |
| 6 | Activación con tiempo de sesión (P2, 22-11) | +0,026 [−0,006; +0,056]; 27/41; p Holm 0,111; inconcluso | resultados/reapertura_41p_22-11-2026/confirmatorio.csv (P2) | igual | igual | — | igual | — | — | igual | — | — | — | — |
| 7 | Atención con posición, 5 particiones (fase 3, Q1) | +0,001 [−0,002; +0,005]; 21/41; nulo concluyente | resultados/reapertura_fase3_41p_22-11-2026/confirmatorio.csv | igual | igual | — | igual | igual | igual | igual | — | — | — | — |
| 8 | Atención con posición, dentro del estímulo (fase 3, Q2) | −0,000 [−0,003; +0,003]; 22/41; nulo concluyente | resultados/reapertura_fase3_41p_22-11-2026/confirmatorio.csv | igual | — | — | igual | — | — | — | — | — | — | — |
| 9 | Activación con posición, 5 particiones (fase 3, Q1) | +0,032 [+0,004; +0,059]; 28/41; p 0,027; p Holm 0,108; inconcluso | resultados/reapertura_fase3_41p_22-11-2026/confirmatorio.csv | igual | igual | — | igual | — | igual | igual | igual | igual | — | — |
| 10 | Activación con posición, dentro del estímulo (fase 3, Q2) | +0,009 [−0,020; +0,037]; 20/41; inconcluso | resultados/reapertura_fase3_41p_22-11-2026/confirmatorio.csv | igual | igual | — | igual | — | — | igual | — | igual | — | — |
| 11 | Atención, placebo: real − placebo (16-11) | −0,000 [−0,003; +0,003]; nulo concluyente | resultados/cierre_robustez_41p_16-11-2026/resultados.csv | igual | — | — | igual | — | — | igual | — | — | — | — |
| 12 | Atención, la posición sola reproduce la mejora (18-11, post hoc) | +0,028 [+0,021; +0,035]; 36/41 | resultados/explicativo_posicion_41p_18-11-2026/contrastes.csv | igual | — | — | igual | — | — | igual | — | — | — | — |
| 13 | Activación, historial − placebo (16-11) | +0,038 [+0,006; +0,068]; 26/41; p Holm 0,043 | resultados/cierre_robustez_41p_16-11-2026/resultados.csv | igual | — | — | igual | — | — | — | — | — | — | — |
| 14 | Activación, historial desplazado seis ventanas − placebo (16-11, enmienda E1) | +0,046 [+0,018; +0,073]; 28/41; p Holm 0,004; respaldo; una partición, 41 personas | resultados/ampliacion_41p_16-11-2026/enmienda_e1_lag6/contrastes.csv | igual | igual | — | igual | igual | igual | igual | — | cifra igual; rótulo retirado: «el historial sin solapamiento con la etiqueta supera al placebo» | entrada del 23-11 «Lámina 29 al día»: «+0,047 sobre el placebo» (la lámina dice hoy +0,046; no hay entrada posterior que lo registre) | igual (ronda 3: «+0,046, p Holm 0,004, positivo en ambos grupos») |
| 15 | Activación, banda de 6 s de la curva − placebo (22-11) | +0,047 [+0,017; +0,078]; 30/40; p Holm 0,017; respaldo; una partición (la del 16-11), 40 personas | resultados/reapertura_41p_22-11-2026/curva_temporal.csv | igual | igual | — | igual | — | igual | igual | igual | igual | — | — |
| 16 | Activación, banda de 12 s | +0,024 [−0,011; +0,060]; inconcluso | resultados/reapertura_41p_22-11-2026/curva_temporal.csv | igual | igual | — | igual | — | igual | igual | — | — | — | — |
| 17 | Activación, 24 s en adelante | inconcluso: no se distingue del placebo ni se demuestra ausencia (+0,004; −0,023; +0,019) | resultados/reapertura_41p_22-11-2026/curva_temporal.csv | igual | igual | — | igual | — | igual | igual | igual | igual | — | — |
| 18 | Activación, mismo minuto de sesión (fase 2, post hoc) | +0,058 [+0,027; +0,092]; efecto relevante | resultados/reapertura_fase2_41p_22-11-2026/x2_estratificada.csv | igual | — | — | igual | — | — | — | — | igual | — | — |
| 19 | GRU con historial − GRU una ventana, atención | +0,008 [−0,004; +0,020]; 26/41 | resultados/cierre_final_41p_16-11-2026/contrastes.csv | igual | — | — | igual | — | — | igual | — | — | — | — |
| 20 | GRU − HGB, ambos con historial, atención | −0,040 [−0,055; −0,027]; 9/41 | resultados/cierre_final_41p_16-11-2026/contrastes.csv | igual | igual | — | igual | — | igual | igual | — | — | — | — |
| 21 | GRU con historial − GRU una ventana, activación (mide historial, no orden) | +0,051 [+0,021; +0,080]; 28/41; p 0,002; secundario sin corrección | resultados/cierre_final_41p_16-11-2026/contrastes.csv | igual | — | — | igual | — | — | igual | — | igual | — | — |
| 22 | GRU − HGB, ambos con historial, activación (contraste del orden) | +0,020 [−0,017; +0,057]; 22/41; inconcluso | resultados/cierre_final_41p_16-11-2026/contrastes.csv | igual | — | — | igual | — | — | igual | — | — | — | — |
| 23 | Fusión tardía − temprana, MLP, atención | +0,012 [+0,005; +0,021]; secundario sin corrección | resultados/ampliacion_41p_16-11-2026/contrastes.csv (E3) | igual | igual | — | igual | igual | igual | igual | — | igual | — | — |
| 24 | Fusión tardía − temprana, HGB, cierre V3, atención (entrenamiento) | −0,010 [−0,018; −0,003]: signo contrario | resultados/cierre_v3_16-11-2026/INFORME.md | igual | igual | — | igual | — | igual | igual | — | igual | igual | — |
| 25 | Fusión tardía − temprana, MLP, activación | +0,006 [−0,032; +0,042]; inconcluso | resultados/ampliacion_41p_16-11-2026/contrastes.csv (E3) | igual | — | — | igual | — | — | — | — | — | — | — |
| 26 | Detección de atención solo con EEG | AUC 0,681 [0,664; 0,697]; 41/41 sobre el azar | resultados/enfoques_41p_22-11-2026/e2_descriptivos.csv | igual | igual | — | igual | igual | igual | igual | igual | igual | igual | — |
| 27 | EEG sin tres componentes oculares | AUC 0,621; 41/41 sobre el azar | resultados/limpieza_ocular_41p_23-11-2026/descriptivos.csv | igual | igual | — | igual | igual | igual | igual | igual | igual | igual | — |
| 28 | Caída por limpieza ocular (L1) | +0,060 [+0,044; +0,075]; 39/41; efecto relevante | resultados/limpieza_ocular_41p_23-11-2026/confirmatorio.csv | igual | — | — | igual | — | — | igual | — | — | «+0,060 [+0,045; +0,075]» (redondeo doble del INFORME; canónico +0,044) | — |
| 29 | Contribución ocular: rótulo | «cerca de un tercio» de la detección sobre el azar depende de componentes ligados a los ojos (0,060 de 0,181); cota inferior; no es una demostración | limpieza_ocular (L1) y enfoques (B1); vocabulario decidido el 26-11 | igual | igual | — | DIFIERE: «Al menos un tercio de la detección sobre el azar depende…» (tabla, l. 18) y «dependiente, al menos en parte, de la huella ocular» (decisión 5); en el hallazgo 2 sí dice «cerca de un tercio» | igual | igual en láminas 1, 27, 29 y 31; DIFIERE en lámina 33: «ligada, al menos en parte, a la huella ocular» | igual; pregunta 1 abre con «al menos en parte» (sobre la circularidad) | DIFIERE en fondo: «cerca de un tercio de la detección sobre el azar es ocular» (ambos README) | DIFIERE: «cerca de un tercio de lo que tiene sobre el azar es ocular»; «parte de la detección por EEG es ocular» | entrada del 23-11: «al menos 0,06 de AUC viene de componentes oculares»; la del cierre de auditoría sí dice «cerca de un tercio» | igual (registra la decisión) |
| 30 | Control: sin tres componentes no oculares | AUC 0,674 (mediana 72 % de la varianza; los oculares, 3,5 %) | resultados/limpieza_ocular_41p_23-11-2026/descriptivos.csv | igual | igual | — | igual | — | igual | igual | — | igual | igual | — |
| 31 | Alfa y beta, antes y después de limpiar | 0,593 → 0,547 (L4 −0,045; inferior) | resultados/limpieza_ocular_41p_23-11-2026/descriptivos.csv | igual | — | — | igual | — | igual | igual | — | igual | igual | — |
| 32 | Red convolucional, EEG original | AUC 0,716 [0,697; 0,735] | resultados/red_cruda_41p_23-11-2026/descriptivos.csv | igual | igual | — | igual | — | igual | igual | igual | igual | igual | — |
| 33 | Red convolucional, EEG limpio | AUC 0,649 | resultados/red_cruda_41p_23-11-2026/descriptivos.csv | igual | — | — | igual | — | igual | igual | igual | igual | igual | — |
| 34 | Red − HGB, EEG original (R1) | +0,035 [+0,023; +0,047]; 32/41; efecto relevante con holgura mínima | resultados/red_cruda_41p_23-11-2026/confirmatorio.csv | igual | igual | — | igual | — | igual | igual | igual | igual | igual | — |
| 35 | Red − HGB, EEG limpio (R2) | +0,028 [+0,013; +0,043]; respaldo | resultados/red_cruda_41p_23-11-2026/confirmatorio.csv | igual | igual | — | igual | — | igual | igual | igual | igual | igual | — |
| 36 | Red original − red limpia (R3) | +0,067 [+0,053; +0,082]; sin control propio | resultados/red_cruda_41p_23-11-2026/confirmatorio.csv | igual | igual | — | igual | — | igual | igual | — | — | igual | — |
| 37 | Activación en la ventana actual: red frente a HGB solo EEG | 0,498 frente a 0,524 (R4 −0,025; inconcluso) | resultados/red_cruda_41p_23-11-2026/descriptivos.csv | igual | igual | — | igual | — | igual (0,498 frente a 0,524; en tablas «0,52») | igual | igual | igual | igual | — |
| 38 | Etiqueta corregida: la posición sola | AUC 0,504 [0,498; 0,510] (original 0,598) | resultados/enfoques_41p_22-11-2026/e1_descriptivos.csv | igual | — | — | igual | igual | igual | igual | — | igual | — | — |
| 39 | Etiqueta corregida: detección (A1) | 0,675 frente a 0,683; −0,008 [−0,015; −0,001]; p Holm 0,055; decisión registrada «inferior», al filo | resultados/enfoques_41p_22-11-2026/e1_confirmatorio.csv | igual | — | — | igual | igual | igual | igual | — | igual | — | — |
| 40 | Adaptación a la persona, activación, con historial | +0,045 [+0,023; +0,069]; 30/40; p Holm 0,0004; efecto relevante | resultados/enfoques_41p_22-11-2026/e4_confirmatorio.csv | igual | igual | — | igual | — | — | igual | — | igual | — | igual |
| 41 | Activación por estímulo | AUC 0,587 [0,550; 0,622]; no supera de forma demostrable al promedio por ventana (+0,020 [−0,007; +0,046]) | resultados/enfoques_41p_22-11-2026/e3_descriptivos.csv | igual | igual | — | igual | — | — | igual | — | igual | — | — |
| 42 | Fiabilidad por mitades de la detectabilidad | 0,76 (atención) y 0,66 (activación) | resultados/enfoques_41p_22-11-2026/INFORME.md | igual | — | — | igual | — | — | — | — | igual | — | — |
| 43 | Tabla 25/16, principal 16-11 | +0,055 [+0,012; +0,101] frente a +0,001 [−0,052; +0,055] | resultados/cierre_final_41p_16-11-2026/heterogeneidad_por_grupo.csv; c07 | igual | igual | — | igual | igual | igual | igual | — | — | — | igual |
| 44 | Tabla 25/16, principal con 5 particiones | +0,046 [+0,012; +0,086] frente a +0,021 [−0,017; +0,060] | ronda3/comprobaciones/c07_seleccion_y_grupos.py | igual | igual | — | igual | igual | — | igual | — | — | — | — |
| 45 | Tabla 25/16, historial desplazado − placebo | +0,035 [+0,003; +0,064] y +0,064 [+0,015; +0,115] | c07 | igual | igual | — | igual | igual | igual | igual | — | — | — | igual |
| 46 | Tabla 25/16, GRU | +0,045 [+0,007; +0,083] y +0,059 [+0,014; +0,101] | heterogeneidad_por_grupo.csv; c07 | igual | — | — | igual | igual | — | igual | — | — | — | — |
| 47 | Tabla 25/16, p de la diferencia entre grupos | principal 16-11: +0,054, p = 0,15; 5 particiones p = 0,38; tiempo de sesión 0,08; historial − posición 0,09; ninguno de nueve bajo 0,05 | ronda4/VERIFICACION_CORRECCIONES_R2.md (anexo) | igual | sin p: «la diferencia entre grupos no es significativa» no aparece; dice «posible y no está demostrado» | — | sin p: «la diferencia entre grupos no es significativa con 16 personas» | sin p: «no es significativa con 16 personas» | — | sin p: «no es significativa con 16 personas» | — | — | — | igual |
| 48 | Selección de hojas de activación | 15 hojas; la decide el contexto de 32 (0,5311 frente a 0,4994 con 7 hojas); 25 de las 41 personas | resultados/cierre_v3_16-11-2026/busqueda_interna_activacion.csv | igual | — | igual | igual | — | — | igual | — | — | — | — |
| 49 | Soporte del filtro tónico en la etiqueta de activación | 49 % en las ventanas nominales, 25 % antes, 25 % después (3,7 % antes de t−10) | ronda3/comprobaciones/c03_soporte_etiqueta_gsr.py | igual | igual («cerca de un cuarto» en 9.1; 49/25/25 en 9.5) | igual | igual | igual («cerca de un cuarto… y otro cuarto después») | igual («cerca de un cuarto») | igual | — | — | — | — |
| 50 | La etiqueta de activación es en lo esencial el nivel tónico | AUC 0,911 del nivel tónico (0,595 fásica; 0,522 respuestas) | c03 | igual | igual | igual | igual | igual | igual | igual | — | — | — | igual |
| 51 | Pesos del Modelo Profesor con PCA | recorrido 0,557; dispersión 0,520; duración media 0,508; tiempo total 0,398; pupila −0,052 | resultados/profesor_binario_reconstruido_29-10-2026/; c09 | igual en cifras; nombre: «Modelo Profesor de componente principal (PCA)» (encabezado y 6.1) y «Modelo Profesor con PCA» (8.10) | igual en cifra; nombre: «Modelo Profesor de componente principal (PCA)» | igual en cifra (0,40 a 0,56); nombre: «Modelo Profesor de componente principal (PCA…)» | igual | igual | igual (−0,05, redondeado) | igual | — | sin cifra; nombre: «profesor PCA» (tabla) y «Modelo Profesor con PCA» (texto) | sin cifra; nombre: «profesor PCA» | igual en cifra; nombre: «profesor PCA» |
| 52 | Coincidencia entre las dos versiones del Modelo Profesor | 66,28 % de 13.498 ventanas de entrenamiento; kappa 0,3255 | resultados/profesor_binario_reconstruido_29-10-2026/INFORME.md | igual; no dice que son ventanas de entrenamiento | igual (agregado a 9.5 por la tanda de las 20:58); no dice que son ventanas de entrenamiento | igual | — | «66 % de las etiquetas (kappa 0,33)»; fila del objetivo 3: «los dos profesores de atención» | igual («66 %», «dos tercios de las ventanas») | igual | — | — | — | — |
| 53 | Ventanas con etiqueta de activación | 11.796 de 22.211 (53,1 %) | resultados/etiquetas_gsr_calidad_v2_01-11-2026/ | igual | igual | igual | igual | — | igual | igual | — | — | — | — |
| 54 | Personas | 48 registradas; 41 en el análisis; 25 entrenamiento, 8 validación, 8 test; 6 excluidas y P29 en sensibilidad | resultados/modelado/particion_participantes.csv | — | — | igual | — | — | igual | igual | — | — | — | — |
| 55 | Desfase de reloj EEG − seguidor ocular | 0,18 a 0,53 s (0,184 a 0,528; mediana 0,45); 9 a 26 % de la ventana; sin corregir | resultados/montaje_ocular_41p_23-11-2026/personas.csv | igual | igual (sin el porcentaje) | igual | igual (sin el porcentaje) | igual | igual (sin el porcentaje) | igual | igual | igual (sin el porcentaje) | igual (sin el porcentaje) | — |
| 56 | Fijaciones con duración total sobre 2.000 ms | 27,7 % de las ventanas etiquetadas (22.211); 27,8 % de las 25.992 del archivo; 4,0 % sobre 3.000 ms | c09; resultados/preprocesamiento/caracteristicas_multimodales.csv (recalculado en esta auditoría) | igual | — | «27,8 % de las ventanas» (denominador: todas las del archivo, correcto) junto a «4 % de las etiquetadas»: mezcla denominadores | igual | — | — | «cerca del 28 % de las ventanas y … 4 % de las etiquetadas»: mezcla denominadores | — | — | — | «27,7 % de las ventanas» (sin «etiquetadas») |
| 57 | Referencias de la discusión fisiológica | 18; 10 contrastadas en texto completo y 8 solo por resumen (Barry 2005 y 2007, Boucsein 2012, Critchley 2002, Croft y Barry 2000, Iwasaki 2005, Keren 2010, Yuval-Greenberg 2008) | documentacion/auditoria_final_23-11-2026/VERIFICACION_REFERENCIAS.md | igual | — | igual | igual | — | igual | igual | igual | — | igual en el conteo; como pendiente lista solo 4 lecturas (Boucsein, Critchley, Yuval-Greenberg, Iwasaki) | — |
| 58 | Etapas del análisis | 12 (13 filas en el anexo de RD, que separa una comprobación no registrada) | Cierre, tabla de trazabilidad; verificacion.json | igual | igual | — | igual | — | — | igual | igual | — | igual | — |
| 59 | Hashes de la comprobación de reproducibilidad | 288 de 289 coinciden; la diferencia es la enmienda v2 de limpieza ocular | resultados/verificacion_cierre_23-11-2026/verificacion.json | — | — | — | igual | — | — | igual | — | — | igual | — |
| 60 | Valores recalculados por la auditoría final | 2.638, sin discrepancias | documentacion/auditoria_final_23-11-2026/AUDITORIA_EXPERIMENTO.md | — | — | — | igual | — | — | igual | — | — | igual | — |
| 61 | Estimaciones repetidas del contraste principal de activación | nueve; +0,028 a +0,047; 3 de 9 intervalos incluyen el cero; mediana +0,014; 23 de 41 | AUDITORIA_EXPERIMENTO.md (I3); recalculo.json | igual | igual | — | igual | — | — | igual | — | — | igual | — |
| 62 | P4 | 26 ventanas con etiqueta; la persona más influyente del contraste principal de activación | resultados/etiquetas_gsr_calidad_v2_01-11-2026/resumen_personas.csv | igual | igual | igual | igual | — | — | igual | — | — | — | — |
| 63 | Filas que cumplen dos reglas de decisión | ocho, todas de atención: seis «inferior» y dos «respaldo» | protocolos y código; Cierre | igual | igual | igual | igual | — | — | — | — | — | — | — |
| 64 | Tamaño de una cohorte nueva | 72, 101 o 767 según la varianza | resultados/protocolo_hipotesis_reintento_06-11-2026/INFORME.md | — | — | — | — | igual | igual | igual | — | igual | — | — |
| 65 | Margen práctico | 0,02 de AUC; propuesta del 06-11 sin aprobación del profesor guía | protocolo del 06-11 | igual | igual | igual | igual | igual | igual | igual | igual | igual | igual | — |
| 66 | Láminas | 39 = 33 principales + 6 anexos; versión 7 | relato.py (39 llamadas a S); GUIÓN.md; index.html | — | — | — | solo «versión 7» | — | igual (LEEME.md; relato.py tiene 39) | igual | — | — | «37 diapositivas» y, dos entradas después, «39 láminas (33 principales y 6 anexos)» (historial; coherente) | igual |
| 67 | Preguntas del ensayo | 37 (22 con versión corta) | ENSAYO.md (recuento en esta auditoría) | — | — | — | — | — | — | igual | — | — | «20 preguntas difíciles» (entrada del 23-11; no hay entrada posterior) | igual |
| 68 | Decisiones abiertas y su orden | siete: 1 cohorte, 2 margen 0,02, 3 «emociones» como activación, 4 etiqueta original o corregida, 5 encuadre, 6 normalización con la sesión completa, 7 Modelo Profesor con PCA; ninguna tomada | Minuta del 23-11 | igual | igual | igual (además las cinco con casilla del diseño) | igual | igual (fuente) | DIFIERE en el conteo: «cinco decisiones» (nota de portada, índice, título de la lámina 33); 6 y 7 al pie de la lámina 33; orden igual | DIFIERE en el conteo: «Siguen abiertas cinco decisiones… sexto y séptimo punto… la minuta lista las siete»; orden igual | — | igual | «cinco decisiones abiertas» (Conclusiones, 23-11) y «siete decisiones con opciones» (minuta, 23-11) | igual |
| 69 | Decisión 5, alcance | incluye con qué lectura del criterio se llega a «apoyo parcial» (leído al pie de la letra, la ventaja aparece en las dos variables) | RD 8.1 y 8.10; SP 4.8.3 | igual | no lo menciona (9.1 dice «la apoyan de forma parcial» sin la salvedad) | igual | no lo menciona | igual (párrafo agregado a la decisión 5 por la tanda de las 20:58) | no lo menciona | no lo menciona | — | — | — | lo deja como punto para Mario |
| 70 | Etiqueta Git del cierre | `cierre-experimental-2026-11-23` apunta a `aee6ab6`; versión auditada `af345a2` o posterior; `HEAD` = `origin/main` = `1abaa70` | git rev-parse (esta auditoría) | — | — | — | igual | — | — | — | igual | — | igual («anterior a esta auditoría; no se movió»), sin el hash | — |
| 71 | Cierre V3 y registro del análisis con 41 personas | `005a499` 11:35:40 y `1bbb083` 11:39:06 del 16-11 (3 min 26 s) | git log | — | — | — | igual | — | — | igual | — | — | — | — |
| 72 | Commits del bucle de revisión | ronda 1 `aef0f32`, ronda 2 `d2a90e8`, ronda 3 `1abaa70` (26-11, 19:21, 20:17 y 20:45) | git log | — | — | — | — | — | — | — | — | — | — (no hay ninguna entrada del 26-11) | igual para rondas 1 y 2; falta el commit de la ronda 3 (`1abaa70`) |
| 73 | Estado de la aprobación | no hay aprobación registrada del profesor guía sobre los resultados de noviembre, el margen ni el encuadre; solo consta que aprobó usar las etiquetas GSR V2 (01-11) | notas/bitacora.md | igual | igual | igual | igual | igual | igual | igual | — | igual | — | — |
| 74 | Naturaleza de las auditorías | revisiones y recálculos con código separado, hechos con un asistente automático a pedido del autor; no son la revisión de un tercero | Cierre, trazabilidad | igual | igual | igual | igual | igual | igual | igual | DIFIERE: «un agente independiente recalculó las 12 etapas» (ambos README) | DIFIERE: «auditoría independiente de código y de resultados» | «agente independiente», «agentes independientes» (entradas del 23-11) | «tres agentes independientes» (independientes entre sí; aceptable) |
| 75 | Montaje de los electrodos | no documentado; los datos son compatibles con el montaje por defecto (OpenBCI Cyton+Daisy) | resultados/montaje_ocular_41p_23-11-2026/INFORME.md | igual | — | igual | igual | — | igual | igual | DIFIERE en fuerza: «El montaje por defecto queda respaldado por los datos» | igual | igual | — |
| 76 | Experimentos opcionales no corridos | red con filtro de control; corrección del desfase; cohorte nueva; sensibilidad con 7 hojas o selección anidada | Minuta (decisión 1); Cierre | igual (8.9 y 7.5), como trabajo futuro | — | — | lista tres; la sensibilidad con 7 hojas solo aparece como límite («no se corrió»), no en la lista de opcionales | solo lista la sensibilidad con 7 hojas (decisión 1) y la cohorte | lista tres (lámina 32); no menciona la sensibilidad con 7 hojas | igual (preguntas 10, 12 y 37) | — | — | — | solo la sensibilidad con 7 hojas |

Lectura de la tabla. De los 76 hechos, 55 aparecen iguales en todos los documentos que los citan. Los 21 restantes tienen alguna celda con texto. En 6 hay una diferencia real de vocabulario, de conteo, de alcance o de fuerza (hechos 29, 68, 69, 74, 75 y 76). En los otros 15 es una nota de rótulo o de denominador, o una entrada antigua de la bitácora, que no cambia el hecho. Las cifras de los cuatro contrastes de activación que más se confunden están bien separadas en todos los documentos vigentes: +0,034 (16-11, una partición), +0,036 (22-11, cinco particiones), +0,046 (historial desplazado frente a placebo, 16-11, una partición, 41 personas) y +0,047 (banda de 6 s de la curva, 22-11, una partición, 40 personas). Ningún documento vigente describe ya el +0,047 como una repetición con cinco particiones.

## 3. Qué concluye cada documento

Cada bloque tiene cinco líneas: (a) hipótesis, (b) atención, (c) activación, (d) qué detecta el EEG y, al final, lo que lo separa de los demás.

**RD — Borrador Resultados y Discusión (vigente; 8.1 a 8.5)**
- (a) Evidencia mixta con apoyo parcial, que proviene de activación y depende del cambio de diseño posterior al cierre V3. Dice que, leído al pie de la letra y con el segundo diseño, el criterio escrito daría ventaja en las dos variables.
- (b) El modelo con historial rinde mejor (+0,029), pero la ventaja es el tiempo transcurrido en el estímulo: con la posición, +0,001, nulo concluyente.
- (c) Evidencia acotada. El contraste mejor sostenido es +0,046 frente al placebo, con el límite del filtro tónico; el principal (+0,036) es frágil y se concentra en 25 personas; respaldo solo a 6 s.
- (d) Cerca de un tercio de la detección sobre el azar depende de componentes oculares (cota inferior, no demostración); el resto no se atribuye. En activación, nada demostrable en la ventana actual.
- Diferencia: es el más cauto y el más completo. Marca la referencia para los demás.

**CO — Borrador Conclusiones**
- (a) "Los resultados la apoyan de forma parcial", por activación, sin modelo secuencial ni combinación de señales. No menciona la salvedad sobre la lectura del criterio.
- (b) Igual que RD.
- (c) Igual que RD en cifras y límites. En 9.1 afirma en indicativo ("agregar el historial mejora la predicción") y en 9.7 vuelve a "evidencia acotada".
- (d) Igual que RD.
- Diferencia: de fondo, ninguna; de fuerza, la frase inicial de 9.1 sobre activación y la falta de la salvedad del criterio.

**SP — Borrador Secciones pendientes**
- (a) No responde la hipótesis; fija el criterio (4.8.3) y dice que la lectura que lleva a "apoyo parcial" es más exigente que el criterio escrito.
- (b) Solo método: la etiqueta es en la práctica conducta de mirada y su soporte excede los 2 s.
- (c) Solo método: la etiqueta es el nivel tónico de la GSR; soporte 49/25/25.
- (d) Declara que la regla de no-circularidad separa señales, no fuentes fisiológicas.
- Diferencia: ninguna de fondo. Usa "prueba" donde los demás dicen "test".

**CI — Cierre del 23-11**
- (a) "Evidencia mixta, con apoyo parcial", dependiente del cambio de diseño. No menciona la salvedad del criterio.
- (b) Igual que RD.
- (c) Responde "En parte" a si la mejora proviene de las ventanas previas (RD dice "Evidencia acotada"). El resto, igual.
- (d) En la tabla de conclusión dice "Al menos un tercio"; en el hallazgo 2 dice "cerca de un tercio"; en la decisión 5, "al menos en parte".
- Diferencia: el vocabulario de (d) y la fuerza de (c). Su lista de experimentos opcionales omite la sensibilidad con 7 hojas.

**MI — Minuta**
- (a) "La hipótesis tiene apoyo parcial", con tres salvedades explícitas (diseño, resumen del historial, filtro tónico).
- (b) "No la atención", sin más detalle que el +0,001.
- (c) "El historial ayuda a predecir la activación (+0,046 sobre un placebo…; con respaldo solo para los 6 s anteriores)".
- (d) "Cerca de un tercio… depende de componentes ligados a los ojos".
- Diferencia: ninguna de fondo. Desde las 20:58 recoge, dentro de la decisión 5, con qué lectura del criterio se llega a "apoyo parcial". Sigue sin pedir al proyecto el montaje ni la unidad de la GSR.

**PRES — `relato.py`, `GUIÓN.md`, `index.html`**
- (a) "La hipótesis tiene apoyo parcial"; la nota precisa que lo que tiene apoyo es un resumen del historial.
- (b) Igual que RD.
- (c) La tabla de la lámina 29 dice "En parte: +0,046 sobre el placebo" y su nota "sí ayuda a predecir activación, aunque con modelos débiles": algo más fuerte que RD.
- (d) "Cerca de un tercio… (cota inferior)" en las láminas 1, 27, 29 y 31; la lámina 33 dice "ligada, al menos en parte".
- Diferencia: cuenta cinco decisiones (más dos al pie); los demás, siete.

**ENS — `ENSAYO.md`**
- (a) Apoyo parcial "y viene solo de activación"; prohíbe "confirmado" y "confirmatorio".
- (b) Igual que RD, con la precisión de que la posición es tiempo transcurrido (pregunta 3).
- (c) Igual que RD; es el que mejor separa +0,046 de +0,047.
- (d) "Cerca de un tercio", con la lista de lecturas que no deben decirse. La pregunta 1 abre con "al menos en parte".
- Diferencia: "Siguen abiertas cinco decisiones"; cita como fuente el borrador de Discusión fisiológica, que ya no es vigente.

**README (los dos)**
- (a) No la responden en la parte vigente; remiten al cierre.
- (b) "Con la posición como variable, el historial no agrega nada en atención (nulo concluyente)".
- (c) "Pasa a respaldo al promediar 5 particiones…; no es una confirmación. Solo la banda de 6 s tiene respaldo".
- (d) "Cerca de un tercio de la detección sobre el azar **es ocular**": afirma el origen, que los demás evitan.
- Diferencia: "es ocular", "El montaje por defecto queda respaldado por los datos" y "un agente independiente recalculó".

**RES — Resumen del último mes (con aviso de que es anterior a la auditoría)**
- (a) "Apoyo parcial".
- (b) "En atención no hay información temporal: la mejora era el reloj del estímulo": más tajante que RD.
- (c) "El historial ayuda, con respaldo solo para los 6 s anteriores".
- (d) "Cerca de un tercio… es ocular".
- Diferencia: conserva "sin solapamiento con la etiqueta", "auditoría independiente" y "profesor PCA". El aviso lo cubre, pero el texto se corrigió a medias el 26-11 y mezcla las dos épocas.

**BIT — Bitácora desde el 23-11**
- (a) No la responde.
- (b) No la trata desde el 23-11.
- (c) Auditoría final: "el efecto temporal de activación no está confirmado"; "solo hay respaldo a 6 s".
- (d) Primera entrada del 23-11: "al menos 0,06 de AUC viene de componentes oculares"; entrada de la auditoría: "cerca de un tercio… no 'la mayor parte'".
- Diferencia: es un registro por fecha y no se corrige hacia atrás, pero termina el 23-11: no dice nada del 26-11.

**LOOP — Registro del bucle**
- (a) Registra que "apoyo parcial" queda solo para la hipótesis y que el criterio escrito está pendiente de decisión.
- (b) No la trata.
- (c) Registra que el +0,046 estaba descrito con menos fuerza de la que permiten sus datos.
- (d) Registra la decisión de decir "cerca de un tercio".
- Diferencia: ninguna de fondo; ver sección 7.

**Documentos no vigentes.** El borrador de Discusión fisiológica dice lo mismo que RD 8.3 y 8.5 y usa "cerca de un tercio". El borrador del 18-11 y el cierre del 22-11 llevan aviso de reemplazo; el párrafo de actualización del cierre del 22-11 conserva dos lecturas retiradas ("desaparece desde 24 s" y "su ventaja se explica por el tiempo transcurrido"), cubiertas por el aviso. `notas/sustento-fisiologico-23-11-2026.md` declara que conserva el texto original y que dos atribuciones no se comprobaron.

**Diferencias de fuerza, en una línea cada una**
1. Contribución ocular: "al menos" (CI, lámina 33), "es ocular" (README, RES) frente a "cerca de un tercio depende de componentes ligados a los ojos" (los demás).
2. Activación, origen de la mejora: "En parte" (CI, lámina 29) y "sí ayuda" (nota de la lámina 29) frente a "Evidencia acotada" (RD, CO 9.7).
3. Hipótesis: RD, SP y la minuta dicen que "apoyo parcial" depende de una lectura del criterio más exigente que la escrita. CO, CI, PRES y ENS no lo dicen.
4. Atención: "no hay información temporal" (RES) frente a "no proviene de la fisiología de las ventanas previas" (RD, ENS).
5. Montaje: "queda respaldado por los datos" (README) frente a "compatible con" (los demás).

## 4. Vocabulario decidido

| Regla | Cumplen | No cumplen |
|---|---|---|
| "respaldo" solo como rótulo de la regla de decisión | RD, SP, CI, MI, PRES | CO 9.1 ("quedó respaldado"); ENS ("El respaldo bibliográfico", "lo respalda Benedek"); README ("queda respaldado por los datos"). Los tres usos que tenían RD 7.8 y SP 4.5.2 y 4.7 se corrigieron a las 20:58. "Respaldo" como copia de seguridad (README, `AGENTS.md`, registro del bucle) es otra palabra y no se cuenta. |
| "apoyo parcial" solo para la respuesta a la hipótesis | Todos | Ninguno. "El apoyo más sólido", "el apoyo se refiere a…" y "lo que tiene apoyo" (CI, MI, PRES, ENS) hablan del apoyo a la hipótesis. |
| "cerca de un tercio" para la contribución ocular | RD, CO, MI, ENS, LOOP | CI (tabla y decisión 5), PRES (lámina 33), README y RES ("es ocular"). Nadie usa "sobre todo" ni "la mayor parte" para esto. |
| "Modelo Profesor con PCA" | CI, MI (decisión 7), PRES, ENS, RD 8.10 | RD (encabezado y 6.1), CO (encabezado y 9.5) y SP (encabezado): "Modelo Profesor de componente principal (PCA)". LOOP y RES: "profesor PCA". MI (fila del objetivo 3): "los dos profesores de atención". |
| "activación", no "emociones" | Todos | Ninguno. "Emociones" aparece solo entre comillas, al citar la hipótesis o la decisión 3. |
| Observado / Atendido | RD, CO, SP, MI, PRES, ENS | Ninguno. |
| No afirmar aprobación ni cerrar decisiones | Todos | Ninguno. Lo único que consta, y así se dice, es la aprobación de las etiquetas GSR V2 del 01-11. |

## 5. Estado de los documentos, enlaces y remisiones

**Quién dice ser vigente.** RD (vigente; reemplaza al del 18-11 e integra la Discusión fisiológica), CO, SP, CI (reemplaza al del 22-11), MI, la presentación versión 7 y el ensayo. Llevan aviso de reemplazo o de registro: RD del 18-11, Discusión fisiológica, cierre del 22-11, resumen del último mes y nota de sustento fisiológico. No hay dos documentos que se declaren vigentes para lo mismo.

**Enlaces.** Todos los wikilinks de RD, CO, SP y MI resuelven a notas que existen. Todas las rutas entre comillas invertidas existen. `FUENTES.md` coincide con `relato.py`.

**Remisiones a la versión no vigente (tres).**
- MI, "Material de apoyo": enlaza la Discusión fisiológica sin decir que ya no es vigente y no enlaza Secciones pendientes.
- ENS, "Fuentes": cita la Discusión fisiológica y no cita RD.
- ENS, pregunta 7: misma cita.

**Remisiones a secciones de RD tras la reestructuración.** Comprobadas una por una contra los encabezados nuevos (6.1–6.6, 7.1–7.12, 8.1–8.10):
- CO → RD 8.8 (limitaciones), 7.5 (estabilidad entre grupos), 6.1 (variables objetivo) y 7.9 (limpieza ocular): correctas.
- SP → RD 6.1, 6.2, 7.5, 7.8, 8.1 y 8.10: correctas.
- LOOP → RD 8.5 (adaptación a la persona) y 8.8: correctas.
- MI y ENS solo remiten a secciones de CO (9.1, 9.5, 9.6, 9.7), que existen. CI y PRES no remiten a secciones numeradas.
- RD → SP 4.3, 4.5.2, 4.6.1, 4.6.3, 4.6.4, 4.6.5, 4.8.2 y 4.8.3: existen.
- No queda ninguna remisión a la numeración antigua.

**Punto de entrada.** El README del espacio, en "Para continuar", enlaza el esqueleto y no enlaza ninguno de los borradores vigentes ni la minuta. Su enlace a la bitácora dice "hasta el 23-11-2026", lo que es cierto y es parte del problema de la sección 7.

**Edición concurrente.** Esta auditoría empezó sobre el commit `1abaa70`. A las 20:58 del 26-11, mientras se hacía, se aplicó otra tanda de correcciones (las de `ronda5/VERIFICACION_EDITORIAL.md`) sobre RD, CO, SP, la minuta y una respuesta del ensayo; a las 21:01 esos cambios seguían sin commit. Todo lo que dice este informe (tabla maestra, historias, pendientes y texto exacto de las correcciones) se volvió a comprobar contra los archivos tal como quedaron después de esa tanda. Sus efectos sobre la coherencia entre documentos:
- Resolvió tres usos de "respaldar" (RD 7.8; SP 4.5.2 y 4.7) y llevó a la minuta la lectura del criterio de "apoyo parcial". Esas correcciones ya no figuran en la sección 8.
- RD 8.8 pasó de "Tres de ellas" a "Cinco limitaciones condicionan directamente las conclusiones"; el registro del bucle sigue diciendo "las tres limitaciones principales (RD 8.8)".
- CO 9.5 ganó las cifras por grupo, el reparto 49/25/25 y "66 % de las ventanas" (sin decir que son de entrenamiento). CO sigue hablando de "cuatro grupos de límites" y RD de "cinco familias"; no se contradicen, porque CO reparte los límites de los modelos entre sus otros grupos.
- RD 8.4 cambió de título ("con respaldo solo a 6 s"). Nadie lo cita por título.
- RD 7.1 perdió la remisión a la sección 4.5.2. No queda ninguna remisión rota.
- El registro del bucle y la bitácora no mencionan esta tanda.

## 6. Lista única de pendientes

**A. Decisiones con el profesor guía (siete, numeración de la minuta; ninguna tomada)**
1. Cohorte nueva o escribir con las personas ya registradas.
2. Margen práctico de 0,02.
3. "Emociones" presentada como activación.
4. Etiqueta de atención original o corregida por posición.
5. Encuadre: apoyo parcial más advertencia metodológica. Incluye con qué lectura del criterio se llega a "apoyo parcial".
6. Etiquetas normalizadas con la sesión completa.
7. *Modelo Profesor* con PCA como definición del *Attention Score*.

**B. Otras decisiones de diseño, con casilla sin marcar en "Resumen Diseño Etiquetas y Modelos"**
8. Fusión y umbral del *Attention Score*.
9. Combinación de variables y umbral del *Arousal Score*.
10. Ventana de agregación de la GSR.
11. Validación externa de las etiquetas. (La quinta casilla es la decisión 3.)

**C. Texto del esqueleto que quedó en tensión (18 filas de la minuta; el esqueleto no se edita)**
12. Hipótesis; objetivo general y objetivos 1 a 6; contribuciones 2 a 6 y la nota bajo ellas; "Metodología KDD"; "Experiencia Usuario"; 4.5.1; norte del proyecto en `CLAUDE.md`.
13. Secciones no pendientes desactualizadas (SP): 4.4, 4.6.2 (filtros, ±150 µV, 273 características), 4.2 y 1.6, 5.1 y 5.2 ("21 de 48").
14. Métrica principal del manuscrito (AUC frente a BA, macro-F1 y *recall*).

**D. Información que hay que pedir al proyecto**
15. Consentimiento informado y comité de ética.
16. Reclutamiento, criterios de inclusión, edad y sexo.
17. Protocolo de estímulos y criterio con que se armaron los cuatro grupos.
18. Documentación del montaje de los electrodos.
19. Unidad física de la GSR.
20. Revisión del emparejamiento de P29.

**E. Norma del programa**
21. Cómo declarar el uso de asistentes automáticos.

**F. Lecturas y literatura**
22. Leer en texto completo las 8 referencias contrastadas solo por resumen.
23. Confirmar en Critchley (2002) la base anatómica de la hipótesis de RD 8.5; Boucsein (2012) no está citada y está pendiente de lectura.
24. Volumen, número y páginas de las 18 referencias.
25. Marco teórico (2.2 a 2.12) y 3.3, sin literatura verificada.
26. Repetir la búsqueda que sostiene "no encontré estas cuatro señales en navegación web" (lámina 7).
27. Dejar explícito el signo con que entra cada variable en el *Attention Score* (ensayo, pregunta 15).

**G. Elecciones de estilo y de edición que quedaron para el autor**
28. Criterio escrito de "apoyo parcial" frente a la lectura más exigente (ligado a la decisión 5).
29. Párrafo nuevo sobre adaptación a la persona (RD 8.5).
30. Cuáles son las limitaciones principales (RD 8.8, que desde las 20:58 nombra cinco).
31. Definiciones de los dos placebos de la curva, tomadas del informe.
32. "Prueba" (SP) frente a "test" (RD, CO, CI, PRES).
33. Qué es "lo nuevo desde la última reunión" (lámina 2).
34. Duración real de la reunión (el ensayo supone 20 minutos).
35. Redacción de la pregunta de investigación 3 (SP 1.4) y si se mantiene el complemento 5.3.
36. Si se mantienen las subsecciones de CNN, ViT y transferencia del esqueleto.
37. Láminas candidatas a pasar a anexos (9, 12, 15 y 20).

**H. Trabajo de cierre**
38. Revisar RD y pasarlo a LaTeX (redacción, citas, numeración).
39. Ajustar CO según las decisiones (9.1, 9.5, 9.6 y 9.7).

**I. Experimentos opcionales, no corridos**
40. Cohorte nueva.
41. Sensibilidad del modelo de activación con 7 hojas o con selección anidada.
42. Red con el filtro de control.
43. Corrección del desfase entre EEG y seguidor ocular.
44. Modelo de referencia con variables escaladas por persona; evaluación dejando grupos completos fuera; mínimo de ventanas por persona; indicador de movimiento (RD 8.9, como trabajo futuro).
45. Estabilidad de las pseudoetiquetas y evolución en la sesión con el score continuo (objetivos 3 y 6).

**Pendientes que un documento da por resueltos y otro por abiertos**

| Pendiente | Abierto en | Resuelto o distinto en | Qué vale |
|---|---|---|---|
| Predicciones idénticas en el enfoque E1 | BIT ("no se descarta un error sin reentrenar un fold") | CI, RD 7.2 y LOOP (diagnóstico del 26-11: no es un error) | Resuelto. Falta decirlo en la bitácora. |
| Advertencia de "análisis anterior" en los anexos A, B, D y E | BIT ("queda sin hacer") | `relato.py` ya la lleva en los cuatro | Resuelto. |
| Redondeo de dos rótulos de gráficos (−0,002 y +0,006) | BIT ("queda sin hacer") | RD (nota de 7.2): el CSV da −0,0025 y +0,0065; el redondeo doble es del INFORME | No era un error de los gráficos. Resuelto por aclaración. |
| Eje "(OOF)" de la lámina 12 | LOOP, ronda 2 ("pendiente menor") | ENS ("se corrigió en `estilo_tecnico.py`") | Resuelto. El registro no lo cierra. |
| Lecturas pendientes | BIT (4: Boucsein, Critchley, Yuval-Greenberg, Iwasaki) | CI, RD, SP (8) | Valen las 8. |
| Sensibilidad con 7 hojas | MI y LOOP (experimento opcional listado) | CI y lámina 32 (lista de opcionales sin ella) | Es un opcional más. |
| Montaje de los electrodos | RD, SP, PRES ("no documentado; no reemplaza la documentación del experimento") | RES ("resuelto en lo que permiten los datos"); MI no lo pide al proyecto | Sigue faltando el documento. |
| Número de decisiones | PRES y ENS (cinco, más dos al pie) | RD, CO, SP, CI, MI, RES, LOOP (siete) | Siete. |
| Lectura del criterio de "apoyo parcial" | RD, SP, MI y LOOP (abierta, parte de la decisión 5) | CO, CI, PRES y ENS no la mencionan | Abierta. |

## 7. Bitácora y registro del bucle

**Bitácora (`notas/bitacora.md`).**
- Sus entradas del 23-11 describen bien lo que se hizo ese día: commits, cifras y carpetas coinciden con Git y con los CSV, con dos salvedades de redondeo y de época. La entrada de limpieza ocular da el intervalo [+0,045; +0,075] (canónico +0,044, corregido en todos los documentos vigentes). La entrada "Lámina 29 al día" dice "+0,047 sobre el placebo"; desde el 26-11 la lámina dice +0,046.
- No tiene ninguna entrada del 26-11. Los tres commits del bucle (`aef0f32`, `d2a90e8`, `1abaa70`), la reestructuración de RD, el paso de cinco a siete decisiones en CO, las 37 preguntas del ensayo, la integración de la Discusión fisiológica y el diagnóstico de E1 no están. `AGENTS.md` manda leer la bitácora para distinguir el estado reciente; quien lo haga se queda en el 23-11.
- Deja como "queda sin hacer" cuatro cosas ya resueltas (tabla de la sección 6).
- Todos los commits que cita existen.

**Registro del bucle (`notas/loop-revision-26-11-2026.md`).**
- Lo que afirma y se pudo comprobar es cierto: estado inicial en `af345a2`; commits `aef0f32` y `d2a90e8`; 2 bloqueantes, 46 importantes y 53 menores en la auditoría de coherencia; 0 y 12 en la del borrador; 13 errores (4 importantes) en la primera verificación; 7, 24 y 27 en la lectura de comisión; 12 errores menores sobre 391 líneas en la segunda verificación; 0, 8 y 22 en la presentación; guion de 2.717 palabras; versión corta en 22 respuestas; 37 preguntas; 18 filas en la tabla de la minuta; p = 0,15; índice nuevo de RD.
- Le falta el respaldo de la ronda 3: no cita el commit `1abaa70`, que existe y es `HEAD` = `origin/main`.
- Una afirmación no se sostiene: "Vocabulario y numeración de las siete decisiones unificados también en cierre, minuta y READMEs". Los README no listan las decisiones y conservan "es ocular", "respaldado" y "agente independiente"; el cierre conserva "Al menos un tercio" y "al menos en parte". En `1abaa70` el README del repositorio cambió en una sola línea.
- No cierra el pendiente del eje "(OOF)".
- Numeración: sus rondas 1, 2 y 3 dejaron los informes en las carpetas `ronda2`, `ronda3` y `ronda4`. El cierre llama "ronda 3" a la auditoría de código que el registro pone en la ronda 2, y la revisión editorial se titula "ronda 4". No hay dos auditorías distintas; hay dos numeraciones.
- "21 preguntas de defensa sin preparar" y "la sección de preguntas pasó de 22 a 37" (15 nuevas) no se contradicen necesariamente, pero el registro no explica la diferencia.
- Usa "profesor PCA" (H3).
- Dice "cuáles son las tres limitaciones principales (RD 8.8)"; desde las 20:58 RD 8.8 nombra cinco.
- No tiene todavía la ronda 4 (la verificación editorial, sus correcciones de las 20:58 y esta auditoría).
- Todos los commits y cifras que cita existen.

## 8. Tabla de correcciones

Cada "texto actual" se comprobó en su archivo: aparece exactamente una vez. En las celdas, `\|` es una barra vertical del original y `<br>` un salto de línea. Las correcciones de `relato.py` exigen regenerar `index.html` y `GUIÓN.md` con `crear_presentacion.py`; las de `documentos/` y `notas/` exigen volver a sincronizar `respaldo_local/` con `scripts/respaldar_espacio_local.py`.

| # | Archivo | Texto exacto actual | Texto exacto corregido | Gravedad | Motivo |
|---|---|---|---|---|---|
| 1 | `documentacion/Cierre_Experimental_Final_23-11-2026.md` | Al menos un tercio de la detección sobre el azar depende de componentes ligados a los ojos: 0,681, que baja a 0,621 al quitarlos (se lee como cota inferior; no es una demostración) | Cerca de un tercio de la detección sobre el azar depende de componentes ligados a los ojos: 0,681, que baja a 0,621 al quitarlos (0,060 de 0,181; se lee como cota inferior; no es una demostración) | importante | Vocabulario decidido: «cerca de un tercio», no «al menos». Es la tabla de conclusión del documento de referencia. |
| 2 | `documentacion/Cierre_Experimental_Final_23-11-2026.md` | presentada como dependiente, al menos en parte, de la huella ocular, sin atribuir el resto a un origen cerebral ni ocular. | presentada como dependiente, en cerca de un tercio, de la huella ocular, sin atribuir el resto a un origen cerebral ni ocular. Incluye con qué lectura del criterio de la hipótesis se llega a "apoyo parcial" (sección 8.1 del borrador integrado). | importante | Igualar la decisión 5 con RD 8.10 (vocabulario y alcance). |
| 3 | `presentaciones/avances_tesis_06-11-2026/relato.py` | La atención por EEG se presentaría como ligada, al menos en parte, a la huella ocular. | La atención por EEG se presentaría como ligada, en cerca de un tercio, a la huella ocular. | importante | Lámina 33, texto visible. Requiere regenerar index.html y GUIÓN.md con crear_presentacion.py. |
| 4 | `tesis-mds/README.md` | El montaje por defecto queda respaldado por los datos; quitar los componentes oculares baja la AUC de atención por EEG de 0,681 a 0,621: cerca de un tercio de la detección sobre el azar es ocular (0,060 de 0,181, cota inferior), y del resto no se puede afirmar origen cerebral ni ocular. | Los datos son compatibles con el montaje por defecto; quitar los componentes oculares baja la AUC de atención por EEG de 0,681 a 0,621: cerca de un tercio de la detección sobre el azar depende de componentes ligados a los ojos (0,060 de 0,181; se lee como cota inferior y no es una demostración), y del resto no se puede afirmar origen cerebral ni ocular. | importante | «es ocular» es la lectura que el ensayo prohíbe; «respaldado» fuera de la regla de decisión y más fuerte que «compatible». |
| 5 | `repos/Tesis_MDS/README.md` | El montaje por defecto queda respaldado por los datos; quitar los componentes oculares baja la AUC de atención por EEG de 0,681 a 0,621: cerca de un tercio de la detección sobre el azar es ocular (0,060 de 0,181, cota inferior), y del resto no se puede afirmar origen cerebral ni ocular. | Los datos son compatibles con el montaje por defecto; quitar los componentes oculares baja la AUC de atención por EEG de 0,681 a 0,621: cerca de un tercio de la detección sobre el azar depende de componentes ligados a los ojos (0,060 de 0,181; se lee como cota inferior y no es una demostración), y del resto no se puede afirmar origen cerebral ni ocular. | importante | Igual que en el README del espacio. |
| 6 | `tesis-mds/README.md` | un agente independiente recalculó las 12 etapas; cifras reproducidas | un asistente automático, a pedido del autor y con código separado, recalculó las 12 etapas (no es la revisión de un tercero); cifras reproducidas | importante | Los demás documentos declaran que no es una revisión independiente; el ensayo prohíbe «auditoría independiente». |
| 7 | `repos/Tesis_MDS/README.md` | Un agente independiente recalculó las 12 etapas desde las predicciones: cifras reproducidas | Un asistente automático, a pedido del autor y con código separado, recalculó las 12 etapas desde las predicciones (no es la revisión de un tercero): cifras reproducidas | importante | Igual que en el README del espacio. |
| 8 | `documentacion/Cierre_Experimental_Final_23-11-2026.md` | Experimentos opcionales, solo si se piden: red con filtro de control, corrección del desfase entre EEG y seguidor ocular, y cohorte nueva. | Experimentos opcionales, solo si se piden: red con filtro de control, corrección del desfase entre EEG y seguidor ocular, sensibilidad del modelo de activación con 7 hojas o con selección anidada, y cohorte nueva. | importante | La minuta y el registro del bucle listan la sensibilidad con 7 hojas como experimento opcional; el cierre la omitía de la lista. |
| 9 | `presentaciones/avances_tesis_06-11-2026/ENSAYO.md` | - Siguen abiertas cinco decisiones, en el orden de la lámina 33: cohorte nueva o escribir | - Siguen abiertas siete decisiones. Las cinco primeras van en la lámina 33, en el orden de la minuta: cohorte nueva o escribir | importante | Los demás documentos dicen siete; el mismo párrafo termina con «la minuta lista las siete». |
| 10 | `presentaciones/avances_tesis_06-11-2026/ENSAYO.md` | `Escritura/Borrador Conclusiones 23-11-2026.md` y `Escritura/Borrador Discusión fisiológica 23-11-2026.md` del vault | `Escritura/Borrador Conclusiones 23-11-2026.md` y `Escritura/Borrador Resultados y Discusión 23-11-2026.md` (vigente; desde el 26-11 integra la discusión fisiológica) del vault | importante | Las fuentes del ensayo citaban el borrador no vigente y omitían el vigente. |
| 11 | `Avances/Avance - 23-11-2026 (Minuta de decisiones con el profesor).md` | - [[Borrador Resultados y Discusión 23-11-2026]] · [[Borrador Conclusiones 23-11-2026]] · [[Borrador Discusión fisiológica 23-11-2026]]. | - [[Borrador Resultados y Discusión 23-11-2026]] (vigente; desde el 26-11 integra la discusión fisiológica) · [[Borrador Conclusiones 23-11-2026]] · [[Borrador Secciones pendientes 23-11-2026]]. [[Borrador Discusión fisiológica 23-11-2026]] se conserva solo como registro. | importante | La minuta listaba el borrador no vigente como material de apoyo, sin estado, y no listaba Secciones pendientes. |
| 12 | `Avances/Avance - 23-11-2026 (Minuta de decisiones con el profesor).md` | protocolo de estímulos y criterio con que se armaron los cuatro grupos (en los datos, cada grupo corresponde a un orden de presentación de los estímulos). | protocolo de estímulos y criterio con que se armaron los cuatro grupos (en los datos, cada grupo corresponde a un orden de presentación de los estímulos). También faltan la documentación del montaje de los electrodos y la unidad física de la GSR, que la exportación no declara. | importante | RD 7.8, SP 4.5.2 y SP 4.7 dan ambos por pendientes de documentación; la lista de lo que hay que pedir al proyecto no los incluía. |
| 13 | `presentaciones/avances_tesis_06-11-2026/relato.py` | Opcionales, solo si se piden: red con filtro de control, corregir el desfase entre EEG y seguidor ocular, y una cohorte nueva para confirmar. | Opcionales, solo si se piden: red con filtro de control, corregir el desfase entre EEG y seguidor ocular, una sensibilidad con 7 hojas o selección anidada, y una cohorte nueva para confirmar. | menor | Lámina 32, pie. Misma lista que la minuta. Regenerar. |
| 14 | `presentaciones/avances_tesis_06-11-2026/relato.py` | Al final hay cinco decisiones que necesito tomar con usted. | Al final hay siete decisiones que necesito tomar con usted: cinco en la última lámina y dos al pie. | menor | Nota de la portada. Regenerar. |
| 15 | `presentaciones/avances_tesis_06-11-2026/relato.py` | <span>Conclusiones, qué falta y cinco decisiones</span> | <span>Conclusiones, qué falta y las decisiones abiertas</span> | menor | Índice (lámina 2), texto visible. Regenerar. |
| 16 | `presentaciones/avances_tesis_06-11-2026/ENSAYO.md` | Al final traigo cinco decisiones. | Al final traigo siete decisiones. | menor | Guion hablado, lámina 1. Mismo número de palabras: la lámina ya está en 146 palabras por minuto y no admite más. |
| 17 | `presentaciones/avances_tesis_06-11-2026/ENSAYO.md` | `Escritura/Borrador Discusión fisiológica 23-11-2026.md` (vault); `notas/sustento-fisiologico-23-11-2026.md` (verificación de referencias). | `Escritura/Borrador Resultados y Discusión 23-11-2026.md` (vault), sección 8.5; `notas/sustento-fisiologico-23-11-2026.md` (verificación de referencias). | menor | Pregunta 7: misma remisión a la versión no vigente. |
| 18 | `Escritura/Borrador Resultados y Discusión 23-11-2026.md` | (7) el *Modelo Profesor* de componente principal (PCA, por análisis de componentes principales) como definición del *Attention Score* | (7) el *Modelo Profesor* con PCA (análisis de componentes principales) como definición del *Attention Score* | menor | Nombre decidido: «Modelo Profesor con PCA» (así lo dice la sección 8.10 del mismo borrador). |
| 19 | `Escritura/Borrador Resultados y Discusión 23-11-2026.md` | el *Modelo Profesor* de componente principal (PCA) o la fusión con pesos iguales | el *Modelo Profesor* con PCA o la fusión con pesos iguales | menor | Ídem, sección 6.1. |
| 20 | `Escritura/Borrador Conclusiones 23-11-2026.md` | (7) que el *Modelo Profesor* de componente principal (PCA, por análisis de componentes principales) define el *Attention Score* | (7) que el *Modelo Profesor* con PCA (análisis de componentes principales) define el *Attention Score* | menor | Ídem. |
| 21 | `Escritura/Borrador Conclusiones 23-11-2026.md` | la pupila pesa −0,052 en el *Modelo Profesor* de componente principal (PCA), y las variables de fijación | la pupila pesa −0,052 en el *Modelo Profesor* con PCA, y las variables de fijación | menor | Ídem, sección 9.5. |
| 22 | `Escritura/Borrador Conclusiones 23-11-2026.md` | coincide con la de pesos iguales en 66 % de las ventanas, y se siguió con ella | coincide con la de pesos iguales en 66 % de las ventanas de entrenamiento, y se siguió con ella | menor | Frase agregada a 9.5 a las 20:58; mismo denominador que SP y la lámina 12. |
| 23 | `Escritura/Borrador Secciones pendientes 23-11-2026.md` | (7) *Modelo Profesor* de componente principal (PCA, por análisis de componentes principales) como definición del *Attention Score* | (7) *Modelo Profesor* con PCA (análisis de componentes principales) como definición del *Attention Score* | menor | Ídem. |
| 24 | `notas/loop-revision-26-11-2026.md` | H3: en el profesor PCA la pupila casi no pesa | H3: en el *Modelo Profesor* con PCA la pupila casi no pesa | menor | Ídem. |
| 25 | `notas/resumen-ultimo-mes-22-11-2026.md` | Atención binaria con profesor PCA reconstruido | Atención binaria con *Modelo Profesor* con PCA reconstruido | menor | Ídem. |
| 26 | `Avances/Avance - 23-11-2026 (Minuta de decisiones con el profesor).md` | Lo que hay apunta en contra: los dos profesores de atención coinciden en 66 % (kappa 0,33). | Lo que hay apunta en contra: las dos versiones del *Modelo Profesor* de atención coinciden en 66 % de las ventanas de entrenamiento (kappa 0,33). | menor | Término acordado y denominador del 66 %. |
| 27 | `Avances/Avance - 23-11-2026 (Minuta de decisiones con el profesor).md` | Ambos coinciden en 66 % de las etiquetas (kappa 0,33) | Ambos coinciden en 66 % de las ventanas de entrenamiento (kappa 0,33) | menor | El 66,28 % se calculó sobre 13.498 ventanas de las 25 personas de entrenamiento. |
| 28 | `Escritura/Borrador Resultados y Discusión 23-11-2026.md` | Las dos versiones coinciden en 66 % de las ventanas (kappa de Cohen 0,33) | Las dos versiones coinciden en 66 % de las ventanas de entrenamiento (kappa de Cohen 0,33) | menor | Mismo denominador que SP y la lámina 12. |
| 29 | `Escritura/Borrador Conclusiones 23-11-2026.md` | y al promediar cinco particiones quedó respaldado (+0,036 [+0,010; +0,065]) | y al promediar cinco particiones la decisión registrada pasó a respaldo (+0,036 [+0,010; +0,065]) | menor | El rótulo va como nombre de la decisión, igual que en RD y en el cierre. |
| 30 | `presentaciones/avances_tesis_06-11-2026/ENSAYO.md` | El respaldo bibliográfico de las láminas 27 y 28. | El sustento bibliográfico de las láminas 27 y 28. | menor | Ídem. |
| 31 | `presentaciones/avances_tesis_06-11-2026/ENSAYO.md` | El "1 a 5 s" lo respalda Benedek y Kaernbach (2010) | El "1 a 5 s" lo sostiene Benedek y Kaernbach (2010) | menor | Ídem. |
| 32 | `documentacion/Cierre_Experimental_Final_23-11-2026.md` | \| ¿La mejora proviene de la fisiología de las ventanas previas? \| No. Es la posición en el estímulo: con la posición como variable el historial agrega +0,001 [−0,002; +0,005], nulo concluyente \| En parte. El historial | \| ¿La mejora proviene de la fisiología de las ventanas previas? \| No. Es la posición en el estímulo: con la posición como variable el historial agrega +0,001 [−0,002; +0,005], nulo concluyente \| Evidencia acotada. El historial | menor | RD 8.1 responde «Evidencia acotada»; el cierre respondía «En parte», que afirma más. |
| 33 | `presentaciones/avances_tesis_06-11-2026/relato.py` | La respuesta corta: el historial de las señales sí ayuda a predecir activación, aunque con modelos débiles. | La respuesta corta: hay evidencia acotada de que el historial reciente ayuda a predecir activación, con modelos débiles. | menor | Nota de la lámina 29: misma fuerza que CO 9.7 y RD 8.1. Regenerar. |
| 34 | `presentaciones/avances_tesis_06-11-2026/ENSAYO.md` | En el sentido fisiológico, al menos en parte. Cumplo la regla de no usar la misma señal, pero | En el sentido fisiológico, en parte sí. Cumplo la regla de no usar la misma señal, pero | menor | Pregunta 1, versión corta: evitar «al menos» junto a la contribución ocular. |
| 35 | `presentaciones/avances_tesis_06-11-2026/ENSAYO.md` | Si repreguntan: En el sentido fisiológico, al menos en parte. Cumplo | Si repreguntan: En el sentido fisiológico, en parte sí. Cumplo | menor | Pregunta 1, versión larga. |
| 36 | `Escritura/Borrador Resultados y Discusión 23-11-2026.md` | Tres controles quedan inconclusos (el tiempo de sesión como variable, la comparación a igual posición y el contraste con la posición como variable tras la corrección de Holm). | Los controles quedan inconclusos: el tiempo de sesión como variable, el contraste con la posición como variable tras la corrección de Holm, ese mismo contraste dentro de un mismo estímulo y la comparación a igual posición. | menor | RD 8.1 (nota b), CO 9.1 y la pregunta 16 del ensayo nombran otros tres (tiempo de sesión, posición y mismo estímulo); así la lista es una sola. |
| 37 | `Escritura/Borrador Secciones pendientes 23-11-2026.md` | supera los 2.000 ms en el 27,8 % de las ventanas *(calculado desde `caracteristicas_multimodales.csv`)* y los 3.000 ms en el 4 % de las etiquetadas | supera los 2.000 ms en el 27,8 % de las 25.992 ventanas del archivo *(calculado desde `caracteristicas_multimodales.csv`)*, en el 27,7 % de las 22.211 de las 41 personas, y los 3.000 ms en el 4 % de estas últimas | menor | Las dos cifras son correctas pero con denominadores distintos; RD y el cierre dicen «cerca del 28 % de las ventanas etiquetadas». |
| 38 | `Escritura/Borrador Secciones pendientes 23-11-2026.md` | Cumplen a la vez todos los criterios 22.201, cifra que incluye las 482 de P29 y excluye por completo a las seis personas apartadas. | Cumplen a la vez todos los criterios 22.201, cifra que incluye las 482 de P29 y excluye por completo a las seis personas apartadas (21.719 en las 41 personas del análisis principal, que suman 22.211 ventanas en total). | menor | 22.201 y 22.211 son cifras distintas y casi iguales; sin la aclaración parecen una errata. Recalculado desde `caracteristicas_multimodales.csv`. |
| 39 | `notas/loop-revision-26-11-2026.md` | cuáles son las tres limitaciones principales (RD 8.8) | cuáles son las limitaciones principales (RD 8.8; desde la ronda 4 el borrador nombra cinco) | menor | RD 8.8 pasó de «Tres de ellas» a «Cinco limitaciones» a las 20:58; el registro quedó atrás. |
| 40 | `notas/resumen-ultimo-mes-22-11-2026.md` | en activación el historial sin solapamiento con la etiqueta supera al placebo (+0,046 [+0,018; +0,073]) | en activación el historial sin las ventanas de 6 s que promedia la etiqueta supera al placebo (+0,046 [+0,018; +0,073]) | menor | «Sin solapamiento con la etiqueta» es una de las lecturas retiradas. |
| 41 | `notas/resumen-ultimo-mes-22-11-2026.md` | pero cerca de un tercio de lo que tiene sobre el azar es ocular (0,060 de 0,181, cota inferior); del resto | pero cerca de un tercio de lo que tiene sobre el azar depende de componentes ligados a los ojos (0,060 de 0,181; se lee como cota inferior); del resto | menor | Misma lectura que el cierre. |
| 42 | `notas/resumen-ultimo-mes-22-11-2026.md` | Tres fases, cada una registrada antes de correr y con auditoría independiente de código y de resultados. | Tres fases, cada una registrada antes de correr y con una revisión de código y un recálculo de resultados hechos con un asistente automático (no es la revisión de un tercero). | menor | Naturaleza de las auditorías. |
| 43 | `notas/resumen-ultimo-mes-22-11-2026.md` | desde el 22-11 cada etapa pasa además por auditoría independiente. | desde el 22-11 cada etapa pasa además por una revisión de código y un recálculo hechos con un asistente automático. | menor | Ídem. |
| 44 | `notas/resumen-ultimo-mes-22-11-2026.md` | En atención no hay información temporal: la mejora era el reloj del estímulo. | En atención la mejora no proviene de la fisiología de las ventanas previas: era el reloj del estímulo. | menor | RD 8.2: lo que se descarta es el aporte de las ventanas previas, no el contexto temporal. |
| 45 | `documentacion/Cierre_Experimental_Final_23-11-2026.md` | ### Auditoría de código, ronda 3 (26-11-2026) | ### Auditoría de código (26-11-2026; ronda 2 del bucle de revisión, carpeta `ronda3`) | menor | El registro del bucle la llama ronda 2; la carpeta se llama `ronda3`. Evita que parezcan dos auditorías. |
| 46 | `notas/loop-revision-26-11-2026.md` | - Vocabulario y numeración de las siete decisiones unificados también en cierre, minuta y READMEs. | - Vocabulario y numeración de las siete decisiones unificados también en cierre y minuta; en los README solo se tocó el estado de la etiqueta de Git.<br>- Respaldo de la ronda 3: commit `1abaa70`, `HEAD` igual a `origin/main`.<br>- Las carpetas de informes llevan un número más que las rondas de este registro: ronda 1 en `ronda2/`, ronda 2 en `ronda3/`, ronda 3 en `ronda4/` (la auditoría del 23-11 quedó en la raíz de `auditoria_final_23-11-2026/`).<br>- El pendiente del eje "(OOF)" de la lámina 12 quedó corregido en `estilo_tecnico.py` en la ronda 3. | menor | El registro no decía el commit de la ronda 3; los README conservan «es ocular», «respaldado» y «agente independiente»; la numeración de carpetas no coincide con la de las rondas. |
| 47 | `tesis-mds/README.md` | - [Bitácora reciente, hasta el 23-11-2026](notas/bitacora.md). | - [Bitácora reciente, hasta el 26-11-2026](notas/bitacora.md) y [registro del bucle de revisión del 26-11-2026](notas/loop-revision-26-11-2026.md). | menor | Solo si se agrega la entrada del 26-11 a la bitácora (ver abajo). |
| 48 | `repos/Tesis_MDS/README.md` | Estado experimental actualizado al 23-11-2026 (cierre consolidado y auditoría final). Esta entrada reemplaza la descripción anterior del repositorio. | Estado experimental actualizado al 23-11-2026 (cierre consolidado y auditoría final); textos revisados el 26-11-2026, sin resultados nuevos (informes en `documentacion/auditoria_final_23-11-2026/ronda2` a `ronda5`). Esta entrada reemplaza la descripción anterior del repositorio. | menor | El README del repositorio no menciona la revisión del 26-11. |
| 49 | `tesis-mds/README.md` | - [Borrador recuperado](documentos/01%20Tesis%20MDS/Escritura/Estructura%20Tesis.md). | - [Borrador recuperado](documentos/01%20Tesis%20MDS/Escritura/Estructura%20Tesis.md) (esqueleto; no se edita).<br>- Borradores vigentes del 23-11-2026, en `documentos/01 Tesis MDS/Escritura/`: Resultados y Discusión (capítulos 6 a 8), Conclusiones y Secciones pendientes. El de Discusión fisiológica y el de Resultados y Discusión del 18-11 se conservan como registro.<br>- Minuta de decisiones para el profesor guía: `documentos/01 Tesis MDS/Avances/Avance - 23-11-2026 (Minuta de decisiones con el profesor).md` (siete decisiones, ninguna tomada). | menor | "Para continuar" no enlaza ninguno de los borradores vigentes ni la minuta; quien entra por el README llega solo al esqueleto. |
| 50 | `notas/bitacora.md` | (no existe ninguna entrada del 26-11-2026; la última es "## 23-11-2026 — Auditoría final: cierre") | Agregar al final la entrada de la sección 9 de este informe, sin tocar las anteriores | importante | `AGENTS.md` manda leer la bitácora para conocer el estado reciente; hoy termina el 23-11 y deja cuatro pendientes ya resueltos. |

## 9. Entrada propuesta para la bitácora

Para agregar al final de `notas/bitacora.md`, sin tocar las entradas anteriores. Quien la aplique debe completar el commit de la ronda 4.

```markdown
## 26-11-2026 — Bucle de revisión (rondas 1 a 4)

A pedido de Mario. Sin resultados nuevos: no se entrenó ningún modelo ni se agregó ningún contraste. Detalle en `notas/loop-revision-26-11-2026.md`; informes en `repos/Tesis_MDS/documentacion/auditoria_final_23-11-2026/ronda2/`, `ronda3/` y `ronda4/` (las carpetas llevan un número más que las rondas).

- **Ronda 1** (commit `aef0f32`): tres auditorías de segunda pasada y sus correcciones. Error de hecho corregido: el +0,047 de activación a 6 s es la curva temporal en una partición y con 40 personas, no una repetición con cinco particiones. El contraste registrado es +0,046 [+0,018; +0,073] (16-11).
- **Ronda 2** (commit `d2a90e8`): verificación del diff, lectura crítica como comisión y auditoría de código. Cuatro hallazgos del código, declarados como límites: las 15 hojas de activación las decidió el modelo con historial con 25 de las 41 personas evaluadas (+0,055 en esas 25 y +0,001 en las otras 16); la etiqueta de activación es en lo esencial el nivel tónico de la GSR y su soporte excede los 6 s (49 % en las ventanas nominales, 25 % antes y 25 % después); en el *Modelo Profesor* con PCA la pupila pesa −0,052; las fijaciones se suman con su duración completa.
- **Ronda 3** (commit `1abaa70`): verificación, revisión completa de la presentación y revisión editorial. El borrador de Resultados y Discusión tiene índice nuevo (6.1–6.6, 7.1–7.12, 8.1–8.10) e integra la discusión fisiológica; el borrador de Discusión fisiológica queda como registro.
- **Ronda 4** (commit por completar al respaldar): verificación de la edición editorial y auditoría de coherencia entre documentos, con sus correcciones (`ronda5/VERIFICACION_EDITORIAL.md` y `ronda5/COHERENCIA_FINAL.md`).
- **Estado de los documentos**: decisiones abiertas, siete (numeración de la minuta), ninguna tomada. Presentación, versión 7, 39 láminas. `ENSAYO.md`, 37 preguntas.
- **Pendientes de la entrada del 23-11 que quedaron resueltos**: las predicciones idénticas de E1 no son un error (`ronda2/DIAGNOSTICO_E1_POSICION.md`); los anexos A, B, D y E llevan la advertencia de "análisis anterior"; los rótulos −0,002 y +0,006 de los gráficos coinciden con los CSV (el redondeo doble es del INFORME); las referencias por leer en texto completo son 8, no 4.
- **Correcciones a entradas anteriores, que no se editan**: el intervalo de la caída por limpieza ocular es [+0,044; +0,075]; la lámina 29 muestra +0,046 sobre el placebo; la lectura vigente es "cerca de un tercio de la detección sobre el azar depende de componentes ligados a los ojos", no "al menos"; las auditorías se hicieron con un asistente automático a pedido del autor y no son la revisión de un tercero.
```

