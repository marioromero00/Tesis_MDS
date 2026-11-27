# Recálculo independiente de las cifras descriptivas — ronda 6 (27-11-2026)

Cierra la brecha que dejó `../AUDITORIA_EXPERIMENTO.md` (23-11-2026). Esa auditoría recalculó los contrastes confirmatorios y dejó sin recalcular varias cifras descriptivas que los documentos de la tesis citan: E6 por tipo de página, los correlatos E4b, el kappa de la etiqueta corregida, las correlaciones de Spearman con el puntaje ocular, la calidad de la limpieza y el montaje desde los crudos, entre otras.

Hecho por un agente independiente con código propio: `recalcular_descriptivos.py`, en esta carpeta. El script no importa ningún script del repositorio, no ajusta ni entrena ningún modelo (tampoco la ICA), no modifica archivos existentes y solo escribe en esta carpeta (`registro.csv`, `registro.json`, `salida.txt`). No se hicieron commits. Tarda unos 2,5 minutos:

`.venv/bin/python documentacion/auditoria_final_23-11-2026/ronda6/recalcular_descriptivos.py`

## Resultado

**Las cifras descriptivas se reproducen.** De 928 valores registrados:

| Veredicto | Valores |
|---|---|
| Coincide | 884 |
| Coincide con redondeo | 19 |
| Difiere | 5 |
| Sin cifra informada (descriptivo adicional; se deja el valor) | 20 |
| No recalculable sin entrenar | 5 grupos de cifras (lista al final; no entran en el registro) |
| No recalculable por falta de archivo | 0 |

- Ninguna diferencia cambia una decisión ni una lectura.
- De las 5 que difieren, 4 están en los `INFORME.md` de etapa y ya estaban detectadas; los borradores vigentes usan el valor correcto. La quinta sí llega a un borrador: el límite "0,0199" de la red sin sus dos personas más favorables depende de la semilla del remuestreo.
- De las 19 con redondeo, solo una llega a los documentos vigentes con efecto: los dos valores en torno a los que se agrupa el desfase (0,27 y 0,47 s; las medianas son 0,28 y 0,48 s).
- Se resuelve un pendiente del 23-11: los IC de `heterogeneidad_por_grupo.csv` sí se reproducen con la semilla registrada cuando las personas van en orden alfabético (diferencia máxima 0,00005, la del redondeo a 4 decimales del CSV).
- Lo que el encargo pedía comprobar desde los crudos para 5 personas se hizo para las 41: el montaje y la calidad de la limpieza se reproducen con diferencia máxima del orden de 1e-13.

Por sección:

| Sección | Coincide | Con redondeo | Difiere | Sin cifra informada |
|---|---|---|---|---|
| 1 Ampliación | 53 | 0 | 0 | 0 |
| 2 Enfoques | 135 | 0 | 0 | 4 |
| 3 Reapertura | 204 | 7 | 0 | 7 |
| 4 Limpieza | 94 | 2 | 1 | 2 |
| 5 Red cruda | 102 | 7 | 1 | 2 |
| 6 Montaje | 52 | 2 | 2 | 0 |
| 7 Etapas del 16-11 | 199 | 1 | 1 | 1 |
| 8 Etiquetas | 45 | 0 | 0 | 4 |

## Cómo se hizo

- **Fuentes.** Predicciones guardadas de cada etapa; `resultados/preprocesamiento/caracteristicas_multimodales.csv` (ventanas y variables); tablas de etiquetas; y, para montaje, limpieza y red, los crudos en caché, los filtros espaciales guardados y los tensores de `datos/locales/v2_2025` (solo lectura).
- **Reconstrucciones propias, sin leer las tablas del proyecto.**
  - Posición en el estímulo, segmento, minuto de sesión y quintil.
  - Etiqueta de activación GSR V2 completa desde las variables: idéntica a la guardada en las 22.211 ventanas.
  - Puntaje ocular y etiqueta de atención: idéntica a la de las predicciones en las 22.176.
  - Etiqueta corregida por posición: idéntica a la de los archivos `e1_*`.
  - Filas con cobertura completa de la curva temporal: las mismas 6.268 y 12.613 de las predicciones.
- **Pesos del Modelo Profesor.** Recalculados con una descomposición propia de la covarianza de las cinco variables en las 25 personas de entrenamiento; coinciden con el archivo guardado hasta el decimal 15. Es álgebra sobre la construcción de la etiqueta, no un modelo predictivo.
- **Limpieza desde los crudos.** Sin reajustar la ICA: se aplican los filtros guardados en `filtros/*.npz` a la señal cruda. La fracción de varianza retirada se obtiene como traza(P Σ Pᵀ) / traza(Σ), equivalente a la definición del script.
- **Estadística.** AUC por rangos medios, bootstrap percentil sobre personas (20.000 réplicas, semilla 20261029), permutación de signos (200.000, semilla 20261116) y Spearman como Pearson de rangos, todo reimplementado. Uso las semillas declaradas en los protocolos para comparar los intervalos decimal por decimal; donde el resultado depende de la semilla, lo digo.
- **Veredictos.**
  - *Coincide*: el valor completo, redondeado a los decimales con que se informa, da la cifra informada y, si hay CSV, lo reproduce.
  - *Coincide con redondeo*: la cifra informada difiere en una unidad del último decimal (redondeo doble, truncamiento o expresión aproximada).
  - *Difiere*: más que eso.

## Todo lo que difiere

| # | Cifra | Informado | Recalculado | Dónde está | Estado en los documentos vigentes |
|---|---|---|---|---|---|
| 1 | Red, R1 sin las dos personas más favorables (P21 y P18), IC 95 % inferior | 0,0199 | 0,020111620478254995 con la semilla registrada; entre 0,01974 y 0,02018 con otras 30 semillas (bajo 0,02 en 23 de 30); 0,01944 con t de Student | INFORME de la red (límites) y su auditoría | **Llega al borrador de resultados.** Corrección abajo |
| 2 | Montaje: corrimiento de las ventanas, mínimo | 12 % | 9,2 % (0,184 s de 2 s) | INFORME del montaje | Los borradores ya dicen 9 % a 26 % |
| 3 | Montaje: corrimiento de las ventanas, máximo | 25 % | 26,4 % (0,528 s de 2 s) | INFORME del montaje | Ídem |
| 4 | Limpieza: desfase "0,25–0,5 s" (mínimo) | 0,25 | 0,232 en `personas_limpieza.csv` (máximo 0,544); 0,184 a 0,528 en el montaje | INFORME de limpieza, dos veces | Borradores y cierre usan 0,18 a 0,53 |
| 5 | Robustez R3, activación, "+0,042 en las tres" | 0,042 | 0,04324225569377088; 0,04159122433475006; 0,04160077890079201 | INFORME de robustez (texto; su tabla dice +0,042 a +0,043) | El borrador dice +0,042 a +0,043 |

Las filas 2 a 5 ya estaban en la auditoría del 23-11 o en la ronda 2. Los `INFORME.md` no se modifican, por decisión registrada en el cierre.

## Todo lo que coincide solo con redondeo

| # | Cifra | Informado | Valor completo | Correcto | Dónde está | ¿Llega a los documentos vigentes? |
|---|---|---|---|---|---|---|
| 1 | Desfase del grupo P2 a P21, P36 y P37 | "cerca de 0,27 s" | mediana 0,280; media 0,2787; rango 0,184 a 0,352 (19 personas) | 0,28 | INFORME del montaje | **Sí**: borrador de resultados, secciones pendientes y cierre |
| 2 | Desfase del resto | "cerca de 0,47 s" | mediana 0,480; media 0,4840; rango 0,440 a 0,528 (22 personas) | 0,48 | INFORME del montaje | **Sí**, los mismos tres |
| 3 | Limpieza: AUC de potencia lenta y amplitud tras limpiar | 0,603 | 0,6024864146219344 | 0,602 | INFORME de limpieza (tabla) | No: el borrador ya dice 0,602 |
| 4 | D1 atención, misma posición, IC inferior | 0,655 | 0,654498699558234 | 0,654 | INFORME de la reapertura | No: el borrador ya dice 0,654 |
| 5 | D1 activación, posición sola, IC inferior | 0,492 | 0,49149911651531 | 0,491 | INFORME de la reapertura | No aparece |
| 6 | X2 atención, mismo estímulo, IC inferior | 0,007 | 0,006459840179053 | 0,006 | INFORME de la reapertura | No: el borrador ya dice 0,006 |
| 7 | Fase 3 activación, mismo estímulo, historial − (actual + posición), IC inferior | −0,026 | −0,025491 | −0,025 | INFORME de la fase 3 | No: el borrador ya dice −0,025 |
| 8 | Fase 3 activación, igual posición, IC superior | +0,052 | 0,051468 | +0,051 | INFORME de la fase 3 | No aparece |
| 9 | Activación, mismo estímulo, sin la persona más influyente, IC inferior | +0,009 | 0,008456 con la semilla registrada | +0,008 | AUDITORIA_RESULTADOS de la reapertura (su propio remuestreo) | No aparece |
| 10 | Pares de una persona dentro de un mismo minuto | 7 % | atención 7,52 %; activación 7,18 % | 7 % en activación, 8 % en atención | INFORME de la reapertura | El borrador lo cita en el párrafo de activación: correcto ahí |
| 11 | Red: AUC del HGB con EEG original, IC inferior | 0,665 | 0,664452 | 0,664 | INFORME de la red | No (detectado el 23-11) |
| 12 | Red: AUC del HGB solo EEG en activación, IC superior | 0,551 | 0,550493 | 0,550 | INFORME de la red | No: el borrador ya dice 0,550 |
| 13 | Red, R4 en la partición 1102 | −0,042 | −0,04147999331434641 | −0,041 | INFORME de la red y su auditoría | No aparece |
| 14 | Red, R4 en la partición 1103 | −0,021 | −0,020456632021463517 | −0,020 | Ídem | No aparece |
| 15 | Red, R2 en la partición 1104 | +0,032 | 0,031494750672035 | +0,031 | Ídem | No aparece |
| 16 | Red, R4 en la partición 1105 | −0,028 | −0,027479446886032616 | −0,027 | Ídem | No aparece |
| 17 | Red, R1, IC inferior con 30 semillas: mínimo | 0,0230 | 0,0229 con mis 30 semillas (máximo 0,0234) | — | Auditoría de la red (otras semillas) | No aparece |
| 18 | Heterogeneidad, GRU en activación, 16 personas, IC superior | +0,102 | 0,10149637 (el CSV guarda 0,1015) | +0,101 | INFORME del análisis final | No: cierre y borrador ya dicen +0,101 |
| 19 | Varianza del control frente a la ocular | "veinte veces más" | 20,6 veces (72,07 % / 3,50 %) | unas veinte | INFORME de limpieza; presentación | Sí, como aproximación; no requiere cambio |

Las filas 13 a 16 son nuevas: cuatro celdas de la tabla de robustez por partición de la red tienen redondeo doble.

## Correcciones para los documentos vigentes

Formato: archivo · texto actual exacto → texto nuevo exacto. Los números de línea son los del 27-11.

1. `Escritura/Borrador Resultados y Discusión 23-11-2026.md` (línea 456, límites de la red) · `sin las dos personas más favorables, queda en 0,0199` → `sin las dos personas más favorables, queda en torno a 0,020 (entre 0,0197 y 0,0202 según la semilla del remuestreo)`
   - Motivo: con la semilla registrada en el protocolo el límite es 0,0201, sobre el margen; con otras semillas cae a uno u otro lado. La lectura ("holgura mínima") no cambia y queda mejor respaldada así.
2. `Escritura/Borrador Resultados y Discusión 23-11-2026.md` (línea 401) · `cerca de 0,27 s en P2 a P21, P36 y P37, y cerca de 0,47 s en el resto` → `cerca de 0,28 s en P2 a P21, P36 y P37, y cerca de 0,48 s en el resto`
3. `Escritura/Borrador Secciones pendientes 23-11-2026.md` (línea 107) · `cerca de 0,27 s en P2 a P21, P36 y P37, y cerca de 0,47 s en el resto` → `cerca de 0,28 s en P2 a P21, P36 y P37, y cerca de 0,48 s en el resto`
4. `documentacion/Cierre_Experimental_Final_23-11-2026.md` (línea 145) · `cerca de 0,27 s en P2 a P21, P36 y P37; cerca de 0,47 s en el resto` → `cerca de 0,28 s en P2 a P21, P36 y P37; cerca de 0,48 s en el resto`
   - Motivo de 2 a 4: el desfase que los documentos informan (0,18 a 0,53 s; mediana 0,45) es el del parpadeo, y sus medianas por grupo son 0,280 y 0,480 s. Los valores 0,27 y 0,47 corresponden a la mirada vertical (medianas 0,272 y 0,472). Los grupos están bien separados: el máximo del primero (0,352) es menor que el mínimo del segundo (0,440).

Opcional; no es un error:

5. `Escritura/Borrador Resultados y Discusión 23-11-2026.md` (línea 23) · `0,522 del número y de la prominencia de las respuestas` → `0,522 del número y de la prominencia de las respuestas (en las 32 personas en que esas variables varían; 0,518 con las 41)`
   - La cifra es correcta, pero promedia 32 personas: en las otras 9 las dos variables son constantes y la AUC vale 0,5 por definición.

Sin corrección necesaria en `Borrador Conclusiones 23-11-2026.md` ni en `presentaciones/avances_tesis_06-11-2026/relato.py`. Las cifras de este alcance que citan coinciden: 0,37 en el último quinto; 3,5 % y 72 %; +0,055 y +0,001; +0,046 y +0,021; 0,18 a 0,53 s; 150 y 20 µV; 34 a 41 personas por quinto; 66 %; 11.796 de 22.211; 0,716, 0,649 y 0,498; 53 %; 26 ventanas. Los gráficos de la presentación no se recalcularon: solo el texto de `relato.py`.

## Observaciones que no son cifras

- **La correlación "con el recorrido de la mirada" es con el recorrido invertido.** Los Spearman de 0,41, 0,28, 0,48 y 0,33 se calculan contra el componente del *Modelo Profesor*, que entra con signo cambiado (menos recorrido, valor más alto). Con el recorrido en píxeles el signo es negativo: a mayor probabilidad de atención alta, menos recorrido. Los borradores dicen "se asocia con el recorrido", que es correcto; conviene no escribir "correlación positiva con el recorrido". El cierre ya declara la inversión.
- **"0,62 desde los 12 s en adelante" depende del corte.** Con posición de 12 s o más la prevalencia es 0,620; con 13 s o más (los dos últimos tramos de la tabla) es 0,626. El borrador dice "desde los 12 s": correcto.
- **E6, activación con imágenes de emoción.** El informe pone "—", pero `por_categoria.csv` tiene valor: 0,594 sin historial y 0,487 con historial, con 5 personas y 401 ventanas. Omitirlo es razonable; no es un dato faltante.
- **Dos listas distintas de cinco personas en la limpieza.** Identificación ocular débil (puntaje del primer componente bajo 0,15): P12, P18, P22, P35 y P40, la que usa la sensibilidad. Saturaciones que atenúan el puntaje: P9, P18, P26, P35 y P40. El informe usa cada una en su lugar; no es un error, pero se confunden con facilidad.
- **Las 50 ventanas con entrada en cero** tienen todas etiqueta de atención y 23 tienen etiqueta de activación; se reparten en 23 personas.
- **AUC de la red juntando todas las ventanas.** 0,684 es la media de las cinco particiones (0,689; 0,683; 0,681; 0,683; 0,682). Con la probabilidad promediada sobre particiones da 0,690.
- **Diferencia entre grupos del contraste principal de activación (16-11).** +0,054 entre las 25 y las 16; p 0,151 con una permutación de grupo propia (el borrador informa 0,15 con Welch). Coherente con "no es significativa".

## Lo que sigue sin verificar y por qué

| Cifra | Por qué |
|---|---|
| Importancias por permutación E5 de la ampliación (atención: EEG 0,207, GSR 0,004, ventana actual 0,157; activación: EEG 0,053, media del historial 0,050, pupila 0,021) | Requieren los modelos ajustados de cada fold, que no se guardaron, y volver a predecir con entradas permutadas. Solo es comprobable la agregación de `importancia_*.csv`, hecha el 23-11 |
| Que cada predicción provenga de la configuración declarada, y qué personas entraron al ajuste de cada modelo | Exige reentrenar. Comprobado solo para un fold del enfoque E1 (ronda 2) y para el fold 0 del análisis final (ronda 3) |
| AUC por fold de la búsqueda de hojas del cierre V3 | Las predicciones de la validación interna no se guardaron. Solo se comprobó la agregación de `busqueda_interna_activacion.csv`: 0,5311 con 15 hojas y 0,4994 con 7, que coincide |
| Puntajes oculares de los componentes (0,38; 0,23; 0,17; 0,13; control 0,06) y la elección de qué componentes se quitan | Recalcularlos exige reajustar la ICA por persona. Se comprobaron las medianas de `personas_limpieza.csv` y el efecto de los filtros ya guardados sobre los crudos, no la selección |
| "La red aprende una señal sintética (AUC 1,0) y da azar con etiquetas barajadas"; coincidencia del tensor con `extract_window` (6e-7) | Son comprobaciones de la auditoría de código que entrenan una red o vuelven a extraer variables; no se repitieron |

Además, fuera del alcance de este encargo y sin recalcular aquí:

- Proporción de ventanas futuras en el placebo de la curva (16–36 %): depende del sorteo del placebo. Reproducirla exige copiar el generador y el orden de filas del script, lo que no sería un recálculo independiente.
- Soporte del filtro tónico de la GSR (49 %, 25 % y 25 %; 3,7 % antes de t−10): sale del análisis de la respuesta del filtro de la ronda 3.
- Gráficos de la presentación.
- Los crudos originales (ZIP de EEG y exportación del seguidor ocular) no se abrieron: se usó la caché `cache_ocular/*.npz`, cuyos hashes están comprobados en `verificacion_cierre_23-11-2026`. Que la caché reproduzca los crudos no se verificó.

## Notas de proceso

- Las personas elegidas para el detalle por persona (semilla 20261127) son P18, P23, P26, P40 y P44. Los valores agregados se recalcularon con las 41.
- En esta carpeta hay otro archivo, `SEGUNDA_LECTURA_COMITE.md`, que no es de esta tarea.
- `AGENTS.md` pide commit y push al cerrar cada etapa. No se hizo porque el encargo lo excluye.

## Tablas completas

Una fila por valor comparado. Para aligerar, se omiten aquí los límites de intervalo que coinciden; están en `registro.csv` con todos los decimales, junto con el valor guardado en el CSV de origen y su diferencia. Los porcentajes se muestran ya multiplicados por 100. Las filas con "0 = sí" son comprobaciones lógicas: 0 significa que se cumple.

### 1. Ampliación E1–E6 (`ampliacion_41p_16-11-2026`)

| Cifra | Informado | Dónde | Recalculado | Veredicto | Nota |
|---|---|---|---|---|---|
| E4: diferencia máxima con fatiga_por_quintil.csv (20 filas × prevalencia, prob. media, AUC, personas) | 0,000000000 | fatiga_por_quintil.csv | 0 | coincide |  |
| E6: diferencia máxima con por_categoria.csv (26 filas × ventanas, AUC, personas) | 0,000000000 | por_categoria.csv | 0 | coincide |  |
| E4 atención, AUC sin historial, quintil 1 | 0,65 | INFORME ampliación E4 | 0,652841731609 | coincide |  |
| E4 atención, AUC sin historial, quintil 5 | 0,71 | INFORME ampliación E4 | 0,712721752111 | coincide |  |
| E4 atención, AUC con historial, quintil 1 | 0,69 | INFORME ampliación E4 | 0,68867707499 | coincide |  |
| E4 atención, AUC con historial, quintil 5 | 0,74 | INFORME ampliación E4 | 0,744833440851 | coincide |  |
| E4 atención, prevalencia de alta, quintil 3 | 0,32 | INFORME ampliación E4 | 0,317689530686 | coincide |  |
| E4 activación, prevalencia de alta, quintil 5 | 0,37 | INFORME ampliación E4 | 0,369289340102 | coincide |  |
| E4 activación, AUC con historial, quintil 5 | 0,64 | INFORME ampliación E4 | 0,64040680376 | coincide |  |
| E4 atencion hgb_c1 quintil 1: prevalencia / AUC / personas | — | fatiga_por_quintil.csv | 0,652841731609 | coincide | prevalencia np.float64(0.5489887640449438); personas 41 |
| E4 atencion hgb_c1 quintil 2: prevalencia / AUC / personas | — | fatiga_por_quintil.csv | 0,657890213538 | coincide | prevalencia np.float64(0.5914124293785311); personas 40 |
| E4 atencion hgb_c1 quintil 3: prevalencia / AUC / personas | — | fatiga_por_quintil.csv | 0,658573302755 | coincide | prevalencia np.float64(0.3176895306859206); personas 41 |
| E4 atencion hgb_c1 quintil 4: prevalencia / AUC / personas | — | fatiga_por_quintil.csv | 0,704046086937 | coincide | prevalencia np.float64(0.5236158192090395); personas 41 |
| E4 atencion hgb_c1 quintil 5: prevalencia / AUC / personas | — | fatiga_por_quintil.csv | 0,712721752111 | coincide | prevalencia np.float64(0.5157515751575158); personas 41 |
| E4 atencion hgb_c32 quintil 1: prevalencia / AUC / personas | — | fatiga_por_quintil.csv | 0,68867707499 | coincide | prevalencia np.float64(0.5489887640449438); personas 41 |
| E4 atencion hgb_c32 quintil 2: prevalencia / AUC / personas | — | fatiga_por_quintil.csv | 0,693955120532 | coincide | prevalencia np.float64(0.5914124293785311); personas 40 |
| E4 atencion hgb_c32 quintil 3: prevalencia / AUC / personas | — | fatiga_por_quintil.csv | 0,658352610121 | coincide | prevalencia np.float64(0.3176895306859206); personas 41 |
| E4 atencion hgb_c32 quintil 4: prevalencia / AUC / personas | — | fatiga_por_quintil.csv | 0,710670172589 | coincide | prevalencia np.float64(0.5236158192090395); personas 41 |
| E4 atencion hgb_c32 quintil 5: prevalencia / AUC / personas | — | fatiga_por_quintil.csv | 0,744833440851 | coincide | prevalencia np.float64(0.5157515751575158); personas 41 |
| E4 activacion hgb_c1 quintil 1: prevalencia / AUC / personas | — | fatiga_por_quintil.csv | 0,570804753713 | coincide | prevalencia np.float64(0.5574736842105263); personas 34 |
| E4 activacion hgb_c1 quintil 2: prevalencia / AUC / personas | — | fatiga_por_quintil.csv | 0,526698311049 | coincide | prevalencia np.float64(0.44491705657167163); personas 36 |
| E4 activacion hgb_c1 quintil 3: prevalencia / AUC / personas | — | fatiga_por_quintil.csv | 0,477039717592 | coincide | prevalencia np.float64(0.6101910828025477); personas 41 |
| E4 activacion hgb_c1 quintil 4: prevalencia / AUC / personas | — | fatiga_por_quintil.csv | 0,505026469847 | coincide | prevalencia np.float64(0.5180774138664398); personas 35 |
| E4 activacion hgb_c1 quintil 5: prevalencia / AUC / personas | — | fatiga_por_quintil.csv | 0,525103296682 | coincide | prevalencia np.float64(0.36928934010152287); personas 34 |
| E4 activacion hgb_c32 quintil 1: prevalencia / AUC / personas | — | fatiga_por_quintil.csv | 0,554386525073 | coincide | prevalencia np.float64(0.5574736842105263); personas 34 |
| E4 activacion hgb_c32 quintil 2: prevalencia / AUC / personas | — | fatiga_por_quintil.csv | 0,545045941469 | coincide | prevalencia np.float64(0.44491705657167163); personas 36 |
| E4 activacion hgb_c32 quintil 3: prevalencia / AUC / personas | — | fatiga_por_quintil.csv | 0,480467833226 | coincide | prevalencia np.float64(0.6101910828025477); personas 41 |
| E4 activacion hgb_c32 quintil 4: prevalencia / AUC / personas | — | fatiga_por_quintil.csv | 0,522169401438 | coincide | prevalencia np.float64(0.5180774138664398); personas 35 |
| E4 activacion hgb_c32 quintil 5: prevalencia / AUC / personas | — | fatiga_por_quintil.csv | 0,64040680376 | coincide | prevalencia np.float64(0.36928934010152287); personas 34 |
| E6 atencion hgb_c1 sitio web: AUC | 0,707 | INFORME ampliación E6 | 0,706696901332 | coincide | 41 personas; 6423 ventanas |
| E6 atencion hgb_c1 numerado: AUC | 0,681 | INFORME ampliación E6 | 0,681031790108 | coincide | 41 personas; 6637 ventanas |
| E6 atencion hgb_c1 diseño: AUC | 0,649 | INFORME ampliación E6 | 0,648648840799 | coincide | 41 personas; 4082 ventanas |
| E6 atencion hgb_c1 imagen emotion: AUC | 0,668 | INFORME ampliación E6 | 0,668042608599 | coincide | 30 personas; 1792 ventanas |
| E6 atencion hgb_c1 imagen blur: AUC | 0,696 | INFORME ampliación E6 | 0,695525951242 | coincide | 25 personas; 891 ventanas |
| E6 atencion hgb_c1 texto: AUC | 0,604 | INFORME ampliación E6 | 0,604435368626 | coincide | 41 personas; 2255 ventanas |
| E6 atencion hgb_c32 sitio web: AUC | 0,710 | INFORME ampliación E6 | 0,709585251078 | coincide | 41 personas; 6423 ventanas |
| E6 atencion hgb_c32 numerado: AUC | 0,698 | INFORME ampliación E6 | 0,697831028634 | coincide | 41 personas; 6637 ventanas |
| E6 atencion hgb_c32 diseño: AUC | 0,637 | INFORME ampliación E6 | 0,637012640215 | coincide | 41 personas; 4082 ventanas |
| E6 atencion hgb_c32 imagen emotion: AUC | 0,667 | INFORME ampliación E6 | 0,667237746958 | coincide | 30 personas; 1792 ventanas |
| E6 atencion hgb_c32 imagen blur: AUC | 0,599 | INFORME ampliación E6 | 0,598965549309 | coincide | 25 personas; 891 ventanas |
| E6 atencion hgb_c32 texto: AUC | 0,633 | INFORME ampliación E6 | 0,632829354893 | coincide | 41 personas; 2255 ventanas |
| E6 activacion hgb_c1 sitio web: AUC | 0,525 | INFORME ampliación E6 | 0,525015483847 | coincide | 40 personas; 5457 ventanas |
| E6 activacion hgb_c1 numerado: AUC | 0,588 | INFORME ampliación E6 | 0,588419404438 | coincide | 34 personas; 3291 ventanas |
| E6 activacion hgb_c1 diseño: AUC | 0,506 | INFORME ampliación E6 | 0,506146141686 | coincide | 20 personas; 1316 ventanas |
| E6 activacion hgb_c1 texto: AUC | 0,506 | INFORME ampliación E6 | 0,505773650501 | coincide | 30 personas; 1285 ventanas |
| E6 activacion hgb_c32 sitio web: AUC | 0,588 | INFORME ampliación E6 | 0,587879253748 | coincide | 40 personas; 5457 ventanas |
| E6 activacion hgb_c32 numerado: AUC | 0,591 | INFORME ampliación E6 | 0,591304039835 | coincide | 34 personas; 3291 ventanas |
| E6 activacion hgb_c32 diseño: AUC | 0,506 | INFORME ampliación E6 | 0,506023825649 | coincide | 20 personas; 1316 ventanas |
| E6 activacion hgb_c32 texto: AUC | 0,524 | INFORME ampliación E6 | 0,523744812741 | coincide | 30 personas; 1285 ventanas |
| E6 activacion hgb_c1 imagen emotion: AUC (el informe pone "—") | — | por_categoria.csv | 0,594075722085 | coincide | 5 personas; 401 ventanas; el informe la omite |
| E6 activacion hgb_c32 imagen emotion: AUC (el informe pone "—") | — | por_categoria.csv | 0,487363432688 | coincide | 5 personas; 401 ventanas; el informe la omite |
| E1: % de filas de activacion con historial desplazado 6 ventanas | 73 % | INFORME ampliación E1 | 73,448626653103 % | coincide |  |
| E1: % de filas de atencion con historial desplazado 6 ventanas | 40 % | INFORME ampliación E1 | 39,817821067821 % | coincide |  |

### 2. Cuatro enfoques (`enfoques_41p_22-11-2026`)

| Cifra | Informado | Dónde | Recalculado | Veredicto | Nota |
|---|---|---|---|---|---|
| E1: etiquetas corregidas de las predicciones distintas de mi reconstrucción | 0 | — | 0 | coincide |  |
| E1: kappa por persona entre etiqueta original y corregida | 0,81 | INFORME enfoques E1 | 0,808348593621 | coincide |  |
| E1: % de ventanas en que coinciden ambas etiquetas | 90,6 % | INFORME enfoques E1 | 90,638528138528 % | coincide |  |
| E1: % de etiquetas que cambian | 9,4 % | INFORME enfoques E1 | 9,361471861472 % | coincide |  |
| E1: % de etiquetas que cambian (auditorías: 9,36 %) | 9,36 % | AUDITORIA_RESULTADOS enfoques | 9,361471861472 % | coincide |  |
| E1: personas con algún cambio de etiqueta | 41 | AUDITORIA_RESULTADOS enfoques | 41 | coincide |  |
| E1/posición: prevalencia de atención alta, primer segundo | 0,51 | Borrador Resultados §7.2; INFORME explicativo | 0,508634646519 | coincide |  |
| E1/posición: prevalencia de atención alta, segundo 2 | 0,37 | Borrador Resultados §7.2; INFORME explicativo | 0,37404885863 | coincide |  |
| E1/posición: prevalencia de atención alta, segundo 3 | 0,38 | Borrador Resultados §7.2; INFORME explicativo | 0,38106565176 | coincide |  |
| E1/posición: prevalencia de atención alta, 9 a 12 s | 0,53 | Borrador Resultados §7.2; INFORME explicativo | 0,534756097561 | coincide |  |
| E1/posición: prevalencia de atención alta, 12 s o más | 0,62 | Borrador Resultados §7.2; INFORME explicativo | 0,619865884325 | coincide |  |
| Posición: prevalencia de atención alta, 13 s o más (tramos 13–20 y 21–32 juntos) | — | — | 0,625591349403 | sin cifra informada |  |
| E1: prevalencia de atención alta, etiqueta original, tramo 1 s | — | e1_descriptivos.csv | 0,508634646519 | coincide | corregida np.float64(0.4970318402590394); n=3706 |
| E1: prevalencia de atención alta, etiqueta original, tramo 2 s | — | e1_descriptivos.csv | 0,37404885863 | coincide | corregida np.float64(0.49539447336804165); n=2497 |
| E1: prevalencia de atención alta, etiqueta original, tramo 3 s | — | e1_descriptivos.csv | 0,38106565176 | coincide | corregida np.float64(0.4933396764985728); n=2102 |
| E1: prevalencia de atención alta, etiqueta original, tramo 4 s | — | e1_descriptivos.csv | 0,425876010782 | coincide | corregida np.float64(0.4948787061994609); n=1855 |
| E1: prevalencia de atención alta, etiqueta original, tramo 5 s | — | e1_descriptivos.csv | 0,466305655836 | coincide | corregida np.float64(0.49458483754512633); n=1662 |
| E1: prevalencia de atención alta, etiqueta original, tramo 6–8 s | — | e1_descriptivos.csv | 0,52350877193 | coincide | corregida np.float64(0.49777777777777776); n=4275 |
| E1: prevalencia de atención alta, etiqueta original, tramo 9–12 s | — | e1_descriptivos.csv | 0,534756097561 | coincide | corregida np.float64(0.49390243902439024); n=1640 |
| E1: prevalencia de atención alta, etiqueta original, tramo 13–20 s | — | e1_descriptivos.csv | 0,590555014606 | coincide | corregida np.float64(0.4961051606621227); n=2054 |
| E1: prevalencia de atención alta, etiqueta original, tramo 21–32 s | — | e1_descriptivos.csv | 0,655765199161 | coincide | corregida np.float64(0.4964360587002096); n=2385 |
| E1: AUC hgb_c1 con etiqueta corregida | 0,675 | INFORME enfoques E1 | 0,675029968949 | coincide |  |
| E1: AUC hgb_c32 con etiqueta corregida | 0,685 | INFORME enfoques E1 | 0,685228692857 | coincide |  |
| E1: AUC pos_c1 con etiqueta corregida | 0,681 | INFORME enfoques E1 | 0,680792199838 | coincide |  |
| E1: AUC pos_only con etiqueta corregida | 0,504 | INFORME enfoques E1 | 0,504422696497 | coincide |  |
| E1: AUC hgb_c1 con etiqueta original | 0,683 | INFORME enfoques E1 | 0,682971346292 | coincide |  |
| E1: mejora del historial con etiqueta original | 0,029 | INFORME enfoques E1 | 0,029013237597 | coincide |  |
| E1: mejora del historial con etiqueta corregida (A2) | 0,010 | INFORME enfoques E1 | 0,010198723908 | coincide |  |
| E1: A1 detección corregida − original | −0,008 | INFORME enfoques E1 | −0,007941377344 | coincide |  |
| E2: AUC Todo el EEG | 0,681 | INFORME enfoques E2 | 0,680894562585 | coincide | 41/41 sobre 0,5 |
| E2: AUC Todo el EEG, a igual posición | 0,675 | INFORME enfoques E2 | 0,674548664602 | coincide |  |
| E2: AUC Potencia lenta y amplitud | 0,673 | INFORME enfoques E2 | 0,672596839313 | coincide | 41/41 sobre 0,5 |
| E2: AUC Potencia lenta y amplitud, a igual posición | 0,659 | INFORME enfoques E2 | 0,658569042248 | coincide |  |
| E2: AUC Canales frontales | 0,675 | INFORME enfoques E2 | 0,674835435148 | coincide | 41/41 sobre 0,5 |
| E2: AUC Canales frontales, a igual posición | 0,667 | INFORME enfoques E2 | 0,666643978896 | coincide |  |
| E2: AUC Canales posteriores | 0,602 | INFORME enfoques E2 | 0,602193492235 | coincide | 38/41 sobre 0,5 |
| E2: AUC Canales posteriores, a igual posición | 0,600 | INFORME enfoques E2 | 0,599939637331 | coincide |  |
| E2: AUC Solo alfa y beta | 0,593 | INFORME enfoques E2 | 0,592679698571 | coincide | 40/41 sobre 0,5 |
| E2: AUC Solo alfa y beta, a igual posición | 0,593 | INFORME enfoques E2 | 0,592539145593 | coincide |  |
| E2: AUC Solo GSR | 0,545 | INFORME enfoques E2 | 0,545226243716 | coincide | 36/41 sobre 0,5 |
| E2: AUC Solo GSR, a igual posición | 0,547 | INFORME enfoques E2 | 0,547061564535 | coincide |  |
| E2: B7 (lento y amplitud) − (alfa y beta) | 0,080 | INFORME enfoques E2 | 0,079917140742 | coincide | 40/41 |
| E2: B8 frontales − posteriores | 0,073 | INFORME enfoques E2 | 0,072641942913 | coincide | 38/41 |
| E2: B3 (EEG + GSR) − solo EEG | 0,002 | INFORME enfoques E2 | 0,002076783707 | coincide | 24/41 |
| E2: B4 solo EEG − solo GSR | 0,136 | INFORME enfoques E2 | 0,135668318869 | coincide | 40/41 |
| E2: control con etiquetas barajadas, AUC | 0,496 | INFORME enfoques E2 | 0,496403393954 | coincide |  |
| E2: Spearman medio por persona, prob. eeg_c1 con recorrido de la mirada (invertido) | 0,41 | INFORME enfoques E2 | 0,414305366441 | coincide |  |
| E2: Spearman medio por persona, prob. eeg_c1 con dispersión (invertida) | 0,30 | INFORME enfoques E2 | 0,298939640154 | coincide |  |
| E2: Spearman medio por persona, prob. eeg_c1 con duración total de fijaciones | 0,29 | INFORME enfoques E2 | 0,292401957397 | coincide |  |
| E2: Spearman medio por persona, prob. eeg_c1 con pupila | −0,09 | INFORME enfoques E2 | −0,091938060079 | coincide |  |
| E2: Spearman medio por persona, prob. eeg_c1 con puntaje ocular | — | INFORME enfoques E2 | 0,379517291944 | sin cifra informada |  |
| E2: Spearman medio por persona, prob. eeg_alfa_beta con recorrido (invertido) | — | INFORME enfoques E2 | 0,224394187249 | sin cifra informada |  |
| E3: segmentos con objetivo (sin empates) | 1589 | INFORME enfoques E3 | 1589 | coincide |  |
| E3: segmentos excluidos por empate | 47 | INFORME enfoques E3 | 47 | coincide |  |
| E3: % de segmentos con etiqueta unánime | 79 % | INFORME enfoques E3 | 79,483952171177 % | coincide |  |
| E3: mediana de segmentos por persona | 36 | INFORME enfoques E3 | 36 | coincide |  |
| E3: segmentos con 3 o más ventanas etiquetadas | 1348 | INFORME enfoques E3 | 1348 | coincide |  |
| E3: segmentos con dos o menos ventanas etiquetadas | 241 | INFORME enfoques E3 | 241 | coincide |  |
| E3: filas por estrategia y partición en las predicciones | 1589 | INFORME enfoques E3 | 1589 | coincide |  |
| E3: AUC seg | 0,587 | INFORME enfoques E3 | 0,586580391649 | coincide |  |
| E3: AUC agg_c32 | 0,567 | INFORME enfoques E3 | 0,56703700158 | coincide |  |
| E3: AUC agg_c1 | 0,532 | INFORME enfoques E3 | 0,532443972415 | coincide |  |
| E3: AUC dur_only | 0,535 | INFORME enfoques E3 | 0,535411281837 | coincide |  |
| E3: personas con AUC del modelo de estímulo sobre 0,5 | 32 | INFORME enfoques E3 | 32 | coincide |  |
| E3: C2 modelo de estímulo − promedio por ventana con historial | 0,020 | INFORME enfoques E3 | 0,019543390069 | coincide | 23/41; p 0.1606 |
| E3: modelo de estímulo − promedio por ventana sin historial | 0,054 | INFORME enfoques E3 | 0,054136419234 | coincide | 27/41; p 0.0135 |
| E3: C3 (estímulo + duración) − solo duración | 0,048 | INFORME enfoques E3 | 0,048369056664 | coincide | 25/41; p 0.1332 |
| E3: C1 modelo de estímulo − 0,5 | 0,087 | INFORME enfoques E3 | 0,086580391649 | coincide | p 0.00004 |
| E3: la numeración de segmentos del archivo coincide con mi reconstrucción (0 = sí) | 0 | — | 0 | coincide |  |
| E3 (3+ ventanas): estímulo − 0,5 | 0,099 | INFORME enfoques E3 | 0,098506537346 | coincide |  |
| E3 (3+ ventanas): estímulo − promedio por ventana | 0,020 | INFORME enfoques E3 | 0,020217692059 | coincide |  |
| E3 (3+ ventanas): (estímulo + duración) − solo duración | 0,054 | INFORME enfoques E3 | 0,053612751932 | coincide |  |
| E4a atencion: fiabilidad entre mitades, AUC sin historial | 0,76 | INFORME enfoques E4 | 0,756097560976 | coincide | n=41 |
| E4a atencion: fiabilidad entre mitades, AUC con historial | 0,64 | INFORME enfoques E4 | 0,642857142857 | coincide | n=41 |
| E4a atencion: fiabilidad entre mitades, ganancia del historial | 0,30 | INFORME enfoques E4 | 0,299825783972 | coincide | n=41 |
| E4b atencion: diferencia máxima con e4_descriptivos.csv (14 correlaciones, p y p Holm) | 0,000000000 | e4_descriptivos.csv | 0 | coincide |  |
| E4c atención: pers_c1 − hgb_c1 | 0,006 | INFORME enfoques E4 | 0,005734126654 | coincide | 25/41 |
| E4c atención: pers_c32 − hgb_c32 | 0,000 | INFORME enfoques E4 | 0,000140010988 | coincide | 19/41 |
| E4c atencion: fracción mínima de sesión de una fila de evaluación | 0,40 | AUDITORIA_RESULTADOS enfoques ("ninguna anterior al 40 %") | 0,412859360217 | coincide |  |
| E4a activacion: fiabilidad entre mitades, AUC sin historial | 0,66 | INFORME enfoques E4 | 0,660225140713 | coincide | n=40 |
| E4a activacion: fiabilidad entre mitades, AUC con historial | 0,58 | INFORME enfoques E4 | 0,575797373358 | coincide | n=40 |
| E4a activacion: fiabilidad entre mitades, ganancia del historial | 0,25 | INFORME enfoques E4 | 0,25234521576 | coincide | n=40 |
| E4b activacion: diferencia máxima con e4_descriptivos.csv (14 correlaciones, p y p Holm) | 0,000000000 | e4_descriptivos.csv | 0 | coincide |  |
| E4c activación: personas con evaluación | 40 | INFORME enfoques E4 | 40 | coincide |  |
| E4c activación: AUC general sin historial en la parte final de la sesión | 0,502 | INFORME enfoques E4 | 0,501715936108 | coincide |  |
| E4c activación: AUC adaptado sin historial en la parte final de la sesión | 0,530 | INFORME enfoques E4 | 0,529533923005 | coincide |  |
| E4c activación: AUC general con historial en la parte final de la sesión | 0,543 | INFORME enfoques E4 | 0,542649960644 | coincide |  |
| E4c activación: AUC adaptado con historial en la parte final de la sesión | 0,587 | INFORME enfoques E4 | 0,587407982915 | coincide |  |
| E4c activación: historial en el modelo adaptado (adaptado con − adaptado sin) | 0,058 | INFORME enfoques E4 | 0,05787405991 | coincide | 33/40 |
| E4c activación: pers_c1 − hgb_c1 | 0,028 | INFORME enfoques E4 | 0,027817986897 | coincide | 29/40; p sin ajuste 0.016485 |
| E4c activación: pers_c32 − hgb_c32 | 0,045 | INFORME enfoques E4 | 0,044758022271 | coincide | 30/40; p sin ajuste 0.000100 |
| E4c activación: historial en el modelo general, mismas filas | — | e4_descriptivos.csv | 0,040934024536 | sin cifra informada |  |
| E4c activación: AUC "de 0,50 a 0,59" (extremos) | 0,59 | INFORME enfoques E4 | 0,587407982915 | coincide |  |
| E4c activacion: fracción mínima de sesión de una fila de evaluación | 0,40 | AUDITORIA_RESULTADOS enfoques ("ninguna anterior al 40 %") | 0,41787387534 | coincide |  |
| E4b: p Holm mínimo entre todos los correlatos | 0,23 | INFORME enfoques E4 ("todos los p Holm ≥ 0,23") | 0,230843682066 | coincide |  |

### 3. Reapertura, fases 1, 2 y 3

| Cifra | Informado | Dónde | Recalculado | Veredicto | Nota |
|---|---|---|---|---|---|
| D2 atencion: AUC de la etiqueta 6 s antes en el mismo estímulo | 0,535 | INFORME reapertura | 0,535067196035 | coincide |  |
| D2 atencion: pares | 8818 | INFORME reapertura | 8818 | coincide |  |
| D2 atencion: personas | 41 | INFORME reapertura | 41 | coincide |  |
| atencion: AUC absoluta hgb_c1 (5 particiones) | 0,683 | INFORME reapertura | 0,682971346292 | coincide |  |
| atencion: AUC absoluta hgb_c32 (5 particiones) | 0,712 | INFORME reapertura | 0,711984583889 | coincide |  |
| atencion: AUC absoluta c1_ts | — | auc_absolutas.csv | 0,708364115591 | coincide |  |
| atencion: AUC absoluta c32_ts | — | auc_absolutas.csv | 0,740307632407 | coincide |  |
| atencion: P1 por partición, mínimo | 0,028 | INFORME reapertura | 0,027908643039 | coincide | por partición: 0.027909; 0.029764; 0.029379; 0.028322; 0.029692 |
| atencion: P1 por partición, máximo | 0,030 | INFORME reapertura | 0,02976435495 | coincide |  |
| atencion: tiempo de sesión solo (c1_ts − hgb_c1) | 0,025 | INFORME reapertura | 0,025392769299 | coincide |  |
| Curva atencion: filas con cobertura completa (reconstrucción propia) | 12613 | INFORME reapertura | 12613 | coincide |  |
| Curva atencion: filas reconstruidas que no están en las predicciones guardadas, o al revés | 0 | — | 0 | coincide |  |
| Curva atencion: personas con filas comunes | 41 | INFORME reapertura | 41 | coincide |  |
| Curva atencion: % de las filas etiquetadas | 57 % | INFORME reapertura | 56,876803751804 % | coincide |  |
| Curva atencion: mínimo de filas comunes por persona | 149 | cobertura_atencion.json | 149 | coincide |  |
| Curva atencion: % de las ventanas de la banda de 6 s que son del mismo estímulo | — | INFORME reapertura, límites | 37,465145347906 % | sin cifra informada |  |
| Curva atencion: % de las ventanas de la banda de 12 s que son del mismo estímulo | — | INFORME reapertura, límites | 26,124816206502 % | sin cifra informada |  |
| Curva atencion: % de las ventanas de la banda de 24 s que son del mismo estímulo | — | INFORME reapertura, límites | 6,564087860977 % | sin cifra informada |  |
| Curva atencion: % de las ventanas de la banda de 48 s que son del mismo estímulo | — | INFORME reapertura, límites | 0,115892760566 % | sin cifra informada |  |
| Curva atencion: % de las ventanas de la banda de 96 s que son del mismo estímulo | — | INFORME reapertura, límites | 0 % | sin cifra informada |  |
| Curva atencion: pendiente del contraste por duplicación del desfase | −0,002 | INFORME reapertura | −0,002046870545 | coincide |  |
| Curva atencion: p de la pendiente | 0,071 | INFORME reapertura | 0,070624646877 | coincide |  |
| Curva atencion: AUC absoluta c1_common | — | auc_absolutas.csv | 0,688675458958 | coincide |  |
| Curva atencion: AUC absoluta lag12 | — | auc_absolutas.csv | 0,689323137409 | coincide |  |
| Curva atencion: AUC absoluta lag24 | — | auc_absolutas.csv | 0,68660578547 | coincide |  |
| Curva atencion: AUC absoluta lag48 | — | auc_absolutas.csv | 0,680873685503 | coincide |  |
| Curva atencion: AUC absoluta lag6 | — | auc_absolutas.csv | 0,689599365436 | coincide |  |
| Curva atencion: AUC absoluta lag96 | — | auc_absolutas.csv | 0,683589738664 | coincide |  |
| Curva atencion: AUC absoluta placebo | — | auc_absolutas.csv | 0,693334397143 | coincide |  |
| X1 atencion: placebo de bloque − placebo disperso | −0,001 | INFORME reapertura | −0,000577444229 | coincide |  |
| X2 atencion: historial − sin historial, mismo estímulo | 0,013 | INFORME reapertura | 0,013449234637 | coincide | 27/41; p 0.000670 |
| X2 atencion: historial − sin historial, mismo estímulo · IC 95 % inferior | 0,007 | INFORME reapertura | 0,006459840179 | coincide con redondeo |  |
| X2 atencion: AUC estratificada hgb_c1, mismo estímulo | — | INFORME reapertura | 0,683557710476 | coincide |  |
| X2 atencion: AUC estratificada hgb_c32, mismo estímulo | — | INFORME reapertura | 0,697006945114 | coincide |  |
| X2 atencion: % de pares dentro de mismo estímulo | 2 % | INFORME reapertura ("2–3 %" y "7 %") | 2,199460750998 % | coincide |  |
| X2 atencion: historial − sin historial, mismo minuto | 0,023 | INFORME reapertura | 0,023053228991 | coincide | 34/41; p 0.000005 |
| X2 atencion: AUC estratificada hgb_c1, mismo minuto | — | INFORME reapertura | 0,674797084115 | coincide |  |
| X2 atencion: AUC estratificada hgb_c32, mismo minuto | — | INFORME reapertura | 0,697850313106 | coincide |  |
| X2 atencion: % de pares dentro de mismo minuto | 7 % | INFORME reapertura ("2–3 %" y "7 %") | 7,516201430192 % | coincide con redondeo |  |
| X2 atencion: historial − sin historial, misma posición | 0,017 | INFORME reapertura | 0,017162973202 | coincide | 35/41; p 0.000010 |
| X2 atencion: AUC estratificada hgb_c1, misma posición | — | INFORME reapertura | 0,678107039556 | coincide |  |
| X2 atencion: AUC estratificada hgb_c32, misma posición | — | INFORME reapertura | 0,695270012758 | coincide |  |
| X2 atencion: % de pares dentro de misma posición | — | INFORME reapertura ("2–3 %" y "7 %") | 7,477098237882 % | sin cifra informada |  |
| D1 atencion: AUC de la posición sola | 0,598 | INFORME reapertura | 0,597820919502 | coincide |  |
| D1 atención: AUC sin historial entre ventanas de la misma posición (partición 1101) | 0,677 | INFORME reapertura | 0,677128945811 | coincide |  |
| D1 atención: AUC sin historial entre ventanas de la misma posición (partición 1101) · IC 95 % inferior | 0,655 | INFORME reapertura | 0,654498699558 | coincide con redondeo |  |
| D1 atención: AUC sin historial sin estratificar (partición 1101) | 0,684 | INFORME reapertura | 0,683638729159 | coincide |  |
| Fase 3 atencion: AUC hgb_c1 | 0,683 | INFORME fase 3 | 0,682971346292 | coincide |  |
| Fase 3 atencion: AUC pos_c1 | 0,711 | INFORME fase 3 | 0,711286350517 | coincide |  |
| Fase 3 atencion: AUC hgb_c32 | 0,712 | INFORME fase 3 | 0,711984583889 | coincide |  |
| Fase 3 atencion: AUC c32_pos | 0,713 | INFORME fase 3 | 0,712703760471 | coincide |  |
| Fase 3 atencion: pos_c1 − hgb_c1 (todas) | 0,028 | INFORME fase 3 | 0,028315004224 | coincide |  |
| Fase 3 atencion: hgb_c32 − pos_c1 (todas) | 0,001 | INFORME fase 3 | 0,000698233373 | coincide |  |
| Fase 3 atencion: c32_pos − pos_c1 (bloque60) | −0,000 | INFORME fase 3 | −0,000410204902 | coincide |  |
| Fase 3 atencion: c32_pos − pos_c1 (posicion) | 0,005 | INFORME fase 3 | 0,005387045754 | coincide |  |
| Fase 3 atencion Q1: delta | 0,001 | INFORME fase 3 | 0,001417409954 | coincide |  |
| Fase 3 atencion Q1: mediana | 0,001 | INFORME fase 3 | 0,000944170772 | coincide |  |
| Fase 3 atencion Q1: persona más influyente es P36 (0 = sí) | 0 | INFORME fase 3 | 0 | coincide | P36 (+0.038) |
| Fase 3 atencion Q1: sin la persona más influyente | 0,001 | INFORME fase 3 | 0,0005015308 | coincide | p 0.7272 |
| Fase 3 atencion Q2: delta | −0,000 | INFORME fase 3 | −6,1175944e−05 | coincide |  |
| Fase 3 atencion Q2: mediana | 0,001 | INFORME fase 3 | 0,00116194626 | coincide |  |
| Fase 3 atencion Q2: persona más influyente es P46 (0 = sí) | 0 | INFORME fase 3 | 0 | coincide | P46 (-0.024) |
| Fase 3 atencion Q2: sin la persona más influyente | 0,001 | INFORME fase 3 | 0,000536815041 | coincide | p 0.7243 |
| D2 activacion: AUC de la etiqueta 6 s antes en el mismo estímulo | 0,680 | INFORME reapertura | 0,679862026998 | coincide |  |
| D2 activacion: pares | 5035 | INFORME reapertura | 5035 | coincide |  |
| D2 activacion: personas | 40 | INFORME reapertura | 40 | coincide |  |
| activacion: AUC absoluta hgb_c1 (5 particiones) | 0,518 | INFORME reapertura | 0,517629996138 | coincide |  |
| activacion: AUC absoluta hgb_c32 (5 particiones) | 0,554 | INFORME reapertura | 0,554079198496 | coincide |  |
| activacion: AUC absoluta c1_ts | — | auc_absolutas.csv | 0,536401931445 | coincide |  |
| activacion: AUC absoluta c32_ts | — | auc_absolutas.csv | 0,562671170803 | coincide |  |
| activacion: P1 por partición, mínimo | 0,028 | INFORME reapertura | 0,028140049786 | coincide | por partición: 0.033944; 0.041318; 0.046914; 0.031930; 0.028140 |
| activacion: P1 por partición, máximo | 0,047 | INFORME reapertura | 0,04691408712 | coincide |  |
| activacion: tiempo de sesión solo (c1_ts − hgb_c1) | 0,019 | INFORME reapertura | 0,018771935307 | coincide |  |
| Curva activacion: filas con cobertura completa (reconstrucción propia) | 6268 | INFORME reapertura | 6268 | coincide |  |
| Curva activacion: filas reconstruidas que no están en las predicciones guardadas, o al revés | 0 | — | 0 | coincide |  |
| Curva activacion: personas con filas comunes | 40 | INFORME reapertura | 40 | coincide |  |
| Curva activacion: % de las filas etiquetadas | 53 % | INFORME reapertura | 53,136656493727 % | coincide |  |
| Curva activacion: mínimo de filas comunes por persona | 62 | cobertura_activacion.json | 62 | coincide |  |
| Curva activacion: % de las ventanas de la banda de 6 s que son del mismo estímulo | 73 % | INFORME reapertura, límites | 73,037661678925 % | coincide |  |
| Curva activacion: % de las ventanas de la banda de 12 s que son del mismo estímulo | 48 % | INFORME reapertura, límites | 48,401042465123 % | coincide |  |
| Curva activacion: % de las ventanas de la banda de 24 s que son del mismo estímulo | 13 % | INFORME reapertura, límites | 12,77850183082 % | coincide |  |
| Curva activacion: % de las ventanas de la banda de 48 s que son del mismo estímulo | 0 % | INFORME reapertura, límites | 0,272539314579 % | coincide |  |
| Curva activacion: % de las ventanas de la banda de 96 s que son del mismo estímulo | 0 % | INFORME reapertura, límites | 0 % | coincide |  |
| Curva activacion: pendiente del contraste por duplicación del desfase | −0,010 | INFORME reapertura | −0,010353935641 | coincide |  |
| Curva activacion: p de la pendiente | 0,009 | INFORME reapertura | 0,00930995345 | coincide |  |
| Curva activacion: personas con pendiente negativa | 27 | INFORME reapertura | 27 | coincide | de 40 |
| Curva activacion: AUC absoluta c1_common | — | auc_absolutas.csv | 0,525327078851 | coincide |  |
| Curva activacion: AUC absoluta lag12 | — | auc_absolutas.csv | 0,558790824554 | coincide |  |
| Curva activacion: AUC absoluta lag24 | — | auc_absolutas.csv | 0,538546791961 | coincide |  |
| Curva activacion: AUC absoluta lag48 | — | auc_absolutas.csv | 0,512205397189 | coincide |  |
| Curva activacion: AUC absoluta lag6 | — | auc_absolutas.csv | 0,581848372211 | coincide |  |
| Curva activacion: AUC absoluta lag96 | — | auc_absolutas.csv | 0,55337140769 | coincide |  |
| Curva activacion: AUC absoluta placebo | — | auc_absolutas.csv | 0,534724710509 | coincide |  |
| Curva activación: placebo − ventana actual | 0,009 | INFORME reapertura | 0,009397631658 | coincide |  |
| Curva activación: 6 s − placebo | 0,047 | Cierre (el INFORME dice +0,018) | 0,047123661703 | coincide | 30/40; mediana 0.0416 |
| Curva activación: 6 s − placebo, mediana | 0,042 | INFORME reapertura, sensibilidad | 0,041590917592 | coincide |  |
| Curva activación: 6 s − placebo, personas a favor | 30 | INFORME reapertura | 30 | coincide |  |
| Sensibilidad activación: 6 s − placebo, sin la persona más influyente | 0,039 | INFORME reapertura | 0,039365614567 | coincide | persona P24 (+0.350); p 0.0063 |
| Sensibilidad activación: 6 s − placebo de bloque, sin la persona más influyente | 0,046 | INFORME reapertura | 0,045796769024 | coincide | persona P24 (+0.325); p 0.0011 |
| X1 activación: 6 s − placebo de bloque, mediana | 0,056 | INFORME reapertura | 0,055512993519 | coincide | media 0.052769; 31/40 |
| X1 activacion: placebo de bloque − placebo disperso | −0,006 | INFORME reapertura | −0,005645375596 | coincide |  |
| X2 activacion: historial − sin historial, mismo estímulo | 0,054 | INFORME reapertura | 0,054032690076 | coincide | 26/41; p 0.011180 |
| X2 activacion: AUC estratificada hgb_c1, mismo estímulo | 0,501 | INFORME reapertura | 0,501008278993 | coincide |  |
| X2 activacion: AUC estratificada hgb_c32, mismo estímulo | 0,555 | INFORME reapertura | 0,55504096907 | coincide |  |
| X2 activacion: % de pares dentro de mismo estímulo | 3 % | INFORME reapertura ("2–3 %" y "7 %") | 2,568914606452 % | coincide |  |
| X2 activacion: historial − sin historial, mismo minuto | 0,058 | INFORME reapertura | 0,058400532418 | coincide | 24/41; p 0.001005 |
| X2 activacion: AUC estratificada hgb_c1, mismo minuto | 0,501 | INFORME reapertura | 0,501151837921 | coincide |  |
| X2 activacion: AUC estratificada hgb_c32, mismo minuto | 0,560 | INFORME reapertura | 0,559552370339 | coincide |  |
| X2 activacion: % de pares dentro de mismo minuto | 7 % | INFORME reapertura ("2–3 %" y "7 %") | 7,182597634668 % | coincide |  |
| X2 activacion: historial − sin historial, misma posición | 0,027 | INFORME reapertura | 0,027365692966 | coincide | 24/41; p 0.092470 |
| X2 activacion: AUC estratificada hgb_c1, misma posición | — | INFORME reapertura | 0,524478999716 | coincide |  |
| X2 activacion: AUC estratificada hgb_c32, misma posición | — | INFORME reapertura | 0,551844692682 | coincide |  |
| X2 activacion: % de pares dentro de misma posición | — | INFORME reapertura ("2–3 %" y "7 %") | 6,560450492733 % | sin cifra informada |  |
| D1 activacion: AUC de la posición sola | 0,543 | INFORME reapertura | 0,543052789164 | coincide |  |
| D1 activacion: AUC de la posición sola · IC 95 % inferior | 0,492 | INFORME reapertura | 0,491499116515 | coincide con redondeo |  |
| Sensibilidad activación: P1 historial − sin historial, sin la persona más influyente | 0,028 | INFORME reapertura / AUDITORIA_RESULTADOS | 0,027745047801 | coincide | persona P4 (+0.385); p 0.0196 |
| Sensibilidad activación: P1 historial − sin historial, mediana | 0,014 | INFORME reapertura | 0,014296653304 | coincide |  |
| Sensibilidad activación: P1 historial − sin historial, personas a favor | 23 | INFORME reapertura | 23 | coincide |  |
| Sensibilidad activación: mismo minuto, sin la persona más influyente | 0,050 | INFORME reapertura / AUDITORIA_RESULTADOS | 0,050377787108 | coincide | persona P4 (+0.379); p 0.0018 |
| Sensibilidad activación: mismo minuto, mediana | 0,042 | INFORME reapertura | 0,041521918941 | coincide |  |
| Sensibilidad activación: mismo minuto, personas a favor | 24 | INFORME reapertura | 24 | coincide |  |
| Sensibilidad activación: mismo estímulo, sin la persona más influyente | 0,044 | INFORME reapertura / AUDITORIA_RESULTADOS | 0,044133507328 | coincide | persona P4 (+0.450); p 0.0215 |
| Sensibilidad activación: mismo estímulo, sin la persona más influyente · IC 95 % inferior | 0,009 | INFORME reapertura / AUDITORIA_RESULTADOS | 0,008456453489 | coincide con redondeo |  |
| Sensibilidad activación: mismo estímulo, mediana | 0,052 | INFORME reapertura | 0,052314814815 | coincide |  |
| Sensibilidad activación: mismo estímulo, personas a favor | 26 | INFORME reapertura | 26 | coincide |  |
| P1 activación: aporte de P4 a la media (0,009 de 0,036) | 0,009 | INFORME reapertura | 0,009380863039 | coincide | delta de P4 +0.3846 |
| P1 activación: media | 0,036 | INFORME reapertura | 0,036449202357 | coincide |  |
| Fase 3 activacion: AUC hgb_c1 | 0,518 | INFORME fase 3 | 0,517629996138 | coincide |  |
| Fase 3 activacion: AUC hgb_c1, mismo estímulo | 0,501 | INFORME fase 3 | 0,501008278993 | coincide |  |
| Fase 3 activacion: AUC pos_c1 | 0,523 | INFORME fase 3 | 0,523180161519 | coincide |  |
| Fase 3 activacion: AUC pos_c1, mismo estímulo | 0,550 | INFORME fase 3 | 0,550438183673 | coincide |  |
| Fase 3 activacion: AUC hgb_c32 | 0,554 | INFORME fase 3 | 0,554079198496 | coincide |  |
| Fase 3 activacion: AUC hgb_c32, mismo estímulo | 0,555 | INFORME fase 3 | 0,55504096907 | coincide |  |
| Fase 3 activacion: AUC c32_pos | 0,555 | INFORME fase 3 | 0,55543348904 | coincide |  |
| Fase 3 activacion: AUC c32_pos, mismo estímulo | 0,559 | INFORME fase 3 | 0,558975660435 | coincide |  |
| Fase 3 activacion: pos_c1 − hgb_c1 (todas) | 0,006 | INFORME fase 3 | 0,005550165381 | coincide |  |
| Fase 3 activacion: hgb_c32 − pos_c1 (todas) | 0,031 | INFORME fase 3 | 0,030899036976 | coincide |  |
| Fase 3 activacion: pos_c1 − hgb_c1 (estimulo) | 0,049 | INFORME fase 3 | 0,049429904679 | coincide |  |
| Fase 3 activacion: hgb_c32 − pos_c1 (estimulo) | 0,005 | INFORME fase 3 | 0,004602785397 | coincide |  |
| Fase 3 activacion: hgb_c32 − pos_c1 (estimulo) · IC 95 % inferior | −0,026 | INFORME fase 3 | −0,025490581588 | coincide con redondeo |  |
| Fase 3 activacion: c32_pos − pos_c1 (bloque60) | 0,033 | INFORME fase 3 | 0,033030733612 | coincide |  |
| Fase 3 activacion: c32_pos − pos_c1 (posicion) | 0,026 | INFORME fase 3 | 0,026033198339 | coincide |  |
| Fase 3 activacion: c32_pos − pos_c1 (posicion) · IC 95 % superior | 0,052 | INFORME fase 3 | 0,051468362444 | coincide con redondeo |  |
| Fase 3 activacion Q1: delta | 0,032 | INFORME fase 3 | 0,032253327521 | coincide |  |
| Fase 3 activacion Q1: mediana | 0,031 | INFORME fase 3 | 0,030878318928 | coincide |  |
| Fase 3 activacion Q1: persona más influyente es P10 (0 = sí) | 0 | INFORME fase 3 | 0 | coincide | P10 (-0.241) |
| Fase 3 activacion Q1: sin la persona más influyente | 0,039 | INFORME fase 3 | 0,039074456627 | coincide | p 0.0036 |
| Fase 3 activacion Q2: delta | 0,009 | INFORME fase 3 | 0,008537476762 | coincide |  |
| Fase 3 activacion Q2: mediana | −0,001 | INFORME fase 3 | −0,000925925926 | coincide |  |
| Fase 3 activacion Q2: persona más influyente es P44 (0 = sí) | 0 | INFORME fase 3 | 0 | coincide | P44 (-0.231) |
| Fase 3 activacion Q2: sin la persona más influyente | 0,015 | INFORME fase 3 | 0,01452014445 | coincide | p 0.3034 |
| Curva: % de filas en que el placebo iguala el nº de ventanas de la banda, mínimo (bandas 12–96 s, ambas tareas) | 30 % | INFORME reapertura, límites ("30–44 %") | 30,064219456117 % | coincide | atencion 12 s 0.3846; atencion 24 s 0.3164; atencion 48 s 0.3394; atencion 96 s 0.3006; activacion 12 s 0.4407; activacion 24 s 0.3409; activacion 48 s 0.4118; activacion 96 s 0.3330 |
| Curva: ídem, máximo | 44 % | INFORME reapertura, límites ("30–44 %") | 44,065092533504 % | coincide |  |
| P4: pares positivo-negativo dentro del mismo estímulo en activación | 4 | INFORME fase 3, auditorías | 4 | coincide |  |

### 4. Limpieza ocular (`limpieza_ocular_41p_23-11-2026`)

| Cifra | Informado | Dónde | Recalculado | Veredicto | Nota |
|---|---|---|---|---|---|
| AUC eeg_c1 | 0,681 | INFORME limpieza | 0,680894562585 | coincide | 41/41 sobre 0,5 |
| AUC ica1_full | 0,661 | INFORME limpieza | 0,660772924178 | coincide | 41/41 sobre 0,5 |
| AUC ica2_full | 0,638 | INFORME limpieza | 0,637683211897 | coincide | 41/41 sobre 0,5 |
| AUC ica3_full | 0,621 | INFORME limpieza | 0,620779147224 | coincide | 41/41 sobre 0,5 |
| AUC ica4_full | 0,613 | INFORME limpieza | 0,613354424402 | coincide | 41/41 sobre 0,5 |
| AUC ctrl3_full | 0,674 | INFORME limpieza | 0,674300491174 | coincide | 41/41 sobre 0,5 |
| AUC ica3_lento_amp | 0,603 | INFORME limpieza | 0,602486414622 | coincide con redondeo | 41/41 sobre 0,5 |
| AUC ica3_frontal | 0,621 | INFORME limpieza | 0,620507747363 | coincide | 41/41 sobre 0,5 |
| AUC ica3_posterior | 0,562 | INFORME limpieza | 0,562001804108 | coincide | 38/41 sobre 0,5 |
| AUC ica3_alfa_beta | 0,547 | INFORME limpieza | 0,547411958379 | coincide | 38/41 sobre 0,5 |
| AUC orig12 | 0,646 | INFORME limpieza | 0,645756154226 | coincide | 40/41 sobre 0,5 |
| AUC reg12 | 0,634 | INFORME limpieza | 0,633893646651 | coincide | 40/41 sobre 0,5 |
| Personas con alfa y beta limpio sobre el azar | 38 | INFORME limpieza | 38 | coincide |  |
| Personas con canales posteriores limpios sobre el azar | — | — | 38 | sin cifra informada |  |
| eeg_c1 − ica1_full | 0,020 | INFORME limpieza | 0,020121638407 | coincide | 33/41 |
| eeg_c1 − ica2_full | 0,043 | INFORME limpieza | 0,043211350689 | coincide | 37/41 |
| eeg_c1 − ica3_full | 0,060 | INFORME limpieza | 0,060115415362 | coincide | 39/41 |
| eeg_c1 − ica4_full | 0,068 | INFORME limpieza | 0,067540138184 | coincide | 37/41 |
| eeg_c1 − ctrl3_full | 0,007 | INFORME limpieza | 0,006594071412 | coincide | 22/41 |
| eeg_lento_amp − ica3_lento_amp | 0,070 | INFORME limpieza | 0,070110424691 | coincide | 39/41 |
| eeg_frontal − ica3_frontal | 0,054 | INFORME limpieza | 0,054327687785 | coincide | 37/41 |
| eeg_posterior − ica3_posterior | 0,040 | INFORME limpieza | 0,040191688127 | coincide | 34/41 |
| eeg_alfa_beta − ica3_alfa_beta | 0,045 | INFORME limpieza | 0,045267740192 | coincide | 35/41 |
| ica3_frontal − ica3_posterior | 0,059 | INFORME limpieza | 0,058505943255 | coincide | 36/41 |
| ica3_lento_amp − ica3_alfa_beta | 0,055 | INFORME limpieza | 0,055074456243 | coincide | 38/41 |
| orig12 − reg12 | 0,012 | INFORME limpieza | 0,011862507576 | coincide | 28/41 |
| ica3_full − ica4_full | 0,007 | INFORME limpieza | 0,007424722822 | coincide | 23/41 |
| Caída de alfa y beta sobre el azar: de +0,093 a +0,047 — después | 0,047 | AUDITORIA_RESULTADOS limpieza | 0,047411958379 | coincide |  |
| Control con etiquetas barajadas − 0,5 (una partición) | −0,011 | INFORME limpieza | −0,010952537581 | coincide |  |
| Control con etiquetas barajadas, AUC | 0,489 | AUDITORIA_RESULTADOS limpieza | 0,489047462419 | coincide |  |
| Control barajado: IC 90 % inferior | −0,021 | AUDITORIA_RESULTADOS limpieza | −0,021212701138 | coincide |  |
| Control barajado: IC 90 % superior | −0,001 | AUDITORIA_RESULTADOS limpieza | −0,000661241794 | coincide |  |
| Máxima diferencia de probabilidad entre el filtro identidad y eeg_c1 | 0,000000000000 | INFORME limpieza | 0 | coincide |  |
| Spearman medio por persona de la prob. eeg_c1 con el recorrido de la mirada (invertido) | 0,41 | INFORME limpieza | 0,414305366441 | coincide |  |
| Spearman medio por persona de la prob. ica3_full con el recorrido de la mirada (invertido) | 0,28 | INFORME limpieza | 0,280360726397 | coincide |  |
| Spearman medio por persona de la prob. ica3_alfa_beta con el recorrido de la mirada (invertido) | 0,11 | INFORME limpieza | 0,113800169253 | coincide |  |
| Spearman medio por persona de la prob. reg12 con el recorrido de la mirada (invertido) | — | INFORME limpieza | 0,304755267978 | sin cifra informada |  |
| L1 sin P23 y P39 | 0,060 | INFORME limpieza | 0,059832655914 | coincide |  |
| L2 sin P23 y P39 | 0,052 | INFORME limpieza | 0,051662478847 | coincide |  |
| L1 sin P23, P39 ni las cinco de identificación débil | 0,061 | INFORME limpieza | 0,061065315113 | coincide |  |
| L2 sin P23, P39 ni las cinco de identificación débil | 0,054 | INFORME limpieza | 0,053720013766 | coincide |  |
| L1: mediana | 0,060 | AUDITORIA_RESULTADOS limpieza ("0,060 y 0,053") | 0,060104586052 | coincide | media 0.060115 |
| L1: sin la persona más influyente | 0,064 | AUDITORIA_RESULTADOS limpieza | 0,064386529913 | coincide | persona P9 (-0.111) |
| L2: mediana | 0,053 | AUDITORIA_RESULTADOS limpieza ("0,060 y 0,053") | 0,053426812902 | coincide | media 0.053521 |
| L2: sin la persona más influyente | 0,058 | AUDITORIA_RESULTADOS limpieza | 0,057701136127 | coincide | persona P9 (-0.114) |
| P9: AUC original | 0,569 | INFORME limpieza | 0,569350490196 | coincide |  |
| P9: AUC tras la limpieza | 0,680 | INFORME limpieza | 0,680079656863 | coincide |  |
| Spearman entre la caída por persona y el puntaje del primer componente | 0,12 | INFORME limpieza | 0,118989547038 | coincide | p 0.459 |
| Spearman entre la caída por persona y la AUC de partida | 0,55 | INFORME limpieza | 0,551393728223 | coincide |  |
| Correlación máxima canal–parpadeo, mediana entre personas, identidad | 0,28 | INFORME limpieza | 0,277943161385 | coincide |  |
| Correlación máxima canal–parpadeo, mediana entre personas, ica3 | 0,08 | INFORME limpieza | 0,077716404984 | coincide |  |
| Correlación máxima canal–parpadeo, mediana entre personas, ctrl3 | 0,31 | INFORME limpieza | 0,310580335434 | coincide |  |
| Correlación máxima canal–mirada horizontal, mediana entre personas, identidad | 0,21 | INFORME limpieza | 0,209204868755 | coincide |  |
| Correlación máxima canal–mirada horizontal, mediana entre personas, ica3 | 0,11 | INFORME limpieza | 0,109017531024 | coincide |  |
| Correlación máxima canal–mirada horizontal, mediana entre personas, ctrl3 | 0,22 | INFORME limpieza | 0,217442465448 | coincide |  |
| Correlación máxima canal–mirada vertical, mediana entre personas, identidad | 0,18 | INFORME limpieza | 0,175864782855 | coincide |  |
| Correlación máxima canal–mirada vertical, mediana entre personas, ica3 | 0,07 | INFORME limpieza | 0,073825571158 | coincide |  |
| Correlación máxima canal–mirada vertical, mediana entre personas, ctrl3 | 0,18 | INFORME limpieza | 0,176570384493 | coincide |  |
| % de la varianza en los 3 componentes oculares (mediana) | 3,5 % | INFORME limpieza | 3,496596810299 % | coincide | rango 0.0012–0.3493 |
| % de la varianza en los 3 componentes de control (mediana) | 72 % | INFORME limpieza | 72,070165774427 % | coincide | rango 0.3550–0.9576 |
| Razón de varianza control / ocular ("veinte veces más") | 20 | INFORME limpieza | 20,611517336559 | coincide con redondeo |  |
| Puntaje ocular mediano del componente 1 | 0,38 | INFORME limpieza | 0,380816010502 | coincide |  |
| Puntaje ocular mediano del componente 2 | 0,23 | INFORME limpieza | 0,230599672943 | coincide |  |
| Puntaje ocular mediano del componente 3 | 0,17 | INFORME limpieza | 0,169230080605 | coincide |  |
| Puntaje ocular mediano del componente 4 | 0,13 | INFORME limpieza | 0,132467714311 | coincide |  |
| Puntaje ocular del control (mediana del máximo por persona) | 0,06 | INFORME limpieza ("0,06 como máximo") | 0,059412542509 | coincide | máximo entre personas 0.1547 |
| Canales utilizables por persona: mínimo | 11 | INFORME limpieza | 11 | coincide |  |
| Canales utilizables por persona: máximo | 16 | INFORME limpieza | 16 | coincide |  |
| 3 componentes como % de las dimensiones: mínimo | 19 % | INFORME limpieza | 18,75 % | coincide |  |
| 3 componentes como % de las dimensiones: máximo | 27 % | INFORME limpieza | 27,272727272727 % | coincide |  |
| Personas con puntaje del primer componente bajo 0,15 son P12, P18, P22, P35 y P40 (0 = sí) | 0 | enmienda_v2 limpieza | 0 | coincide | ['P12', 'P18', 'P22', 'P35', 'P40']; P18 0.1424; siguiente 0.2066 |
| Desfase usado en la limpieza: mínimo, s | 0,25 | INFORME limpieza ("0,25–0,5 s") | 0,232 | difiere |  |
| Desfase usado en la limpieza: máximo, s | 0,5 | INFORME limpieza ("0,25–0,5 s") | 0,544 | coincide |  |
| Ventanas en que el filtro identidad reproduce la tabla vigente | 22211 | INFORME limpieza | 22211 | coincide |  |
| Crudos, 41 personas: discrepancias en canales utilizables frente a personas_limpieza.csv | 0 | crudos en caché + filtros guardados (41 personas, sin reajustar la ICA) | 0 | coincide |  |
| Crudos, 41 personas: diferencia máxima del desfase, s | 0,000000000 | crudos en caché + filtros guardados (41 personas, sin reajustar la ICA) | 0 | coincide |  |
| Crudos, 41 personas: diferencia máxima de la fracción de varianza retirada por ica3 | 0,000000 | crudos en caché + filtros guardados (41 personas, sin reajustar la ICA) | 0 | coincide |  |
| Crudos, 41 personas: diferencia máxima de la fracción de varianza retirada por ctrl3 | 0,000000 | crudos en caché + filtros guardados (41 personas, sin reajustar la ICA) | 0 | coincide |  |
| Crudos: % de varianza retirada por los 3 componentes oculares (mediana) | 3,5 % | crudos en caché + filtros guardados (41 personas, sin reajustar la ICA) | 3,496596810298 % | coincide |  |
| Crudos: % de varianza retirada por el control (mediana) | 72 % | crudos en caché + filtros guardados (41 personas, sin reajustar la ICA) | 72,070165774427 % | coincide |  |
| Crudos, 41 personas: diferencia máxima de las correlaciones canal–referencia (3 condiciones × 3 referencias) | 0,000000000 | crudos en caché + filtros guardados (41 personas, sin reajustar la ICA) | 0 | coincide |  |
| Crudos: correlación máxima canal–parpadeo, mediana, identidad | 0,28 | crudos en caché + filtros guardados (41 personas, sin reajustar la ICA) | 0,277943161385 | coincide |  |
| Crudos: correlación máxima canal–parpadeo, mediana, ica3 | 0,08 | crudos en caché + filtros guardados (41 personas, sin reajustar la ICA) | 0,077716404984 | coincide |  |
| Crudos: correlación máxima canal–parpadeo, mediana, ctrl3 | 0,31 | crudos en caché + filtros guardados (41 personas, sin reajustar la ICA) | 0,310580335434 | coincide |  |
| Crudos: canales utilizables, mínimo | 11 | crudos en caché + filtros guardados (41 personas, sin reajustar la ICA) | 11 | coincide |  |
| Crudos: canales utilizables, máximo | 16 | crudos en caché + filtros guardados (41 personas, sin reajustar la ICA) | 16 | coincide |  |
| Detalle P18: fracción de varianza retirada por ica3 | 0,014387 | personas_limpieza.csv | 0,01438702525 | coincide | control 0.788396; parpadeo 0.1652 → 0.0645 (control 0.1482); 15 canales; desfase 0.264 s |
| Detalle P23: fracción de varianza retirada por ica3 | 0,011555 | personas_limpieza.csv | 0,011554840714 | coincide | control 0.676980; parpadeo 0.3191 → 0.1161 (control 0.3725); 14 canales; desfase 0.448 s |
| Detalle P26: fracción de varianza retirada por ica3 | 0,002928 | personas_limpieza.csv | 0,002928261656 | coincide | control 0.882491; parpadeo 0.0899 → 0.0918 (control 0.0981); 15 canales; desfase 0.504 s |
| Detalle P40: fracción de varianza retirada por ica3 | 0,019935 | personas_limpieza.csv | 0,019934687806 | coincide | control 0.800780; parpadeo 0.0708 → 0.0698 (control 0.0706); 16 canales; desfase 0.496 s |
| Detalle P44: fracción de varianza retirada por ica3 | 0,037285 | personas_limpieza.csv | 0,037284607915 | coincide | control 0.589487; parpadeo 0.4613 → 0.0689 (control 0.5378); 16 canales; desfase 0.472 s |

### 5. Red sobre la señal cruda (`red_cruda_41p_23-11-2026`)

| Cifra | Informado | Dónde | Recalculado | Veredicto | Nota |
|---|---|---|---|---|---|
| AUC red_orig | 0,716 | INFORME red cruda | 0,715915858407 | coincide |  |
| Personas con AUC red_orig sobre 0,5 | 41 | INFORME red cruda | 41 | coincide |  |
| AUC eeg_c1 | 0,681 | INFORME red cruda | 0,680894562585 | coincide |  |
| AUC eeg_c1 · IC 95 % inferior | 0,665 | INFORME red cruda | 0,66445168477 | coincide con redondeo |  |
| Personas con AUC eeg_c1 sobre 0,5 | 41 | INFORME red cruda | 41 | coincide |  |
| AUC red_ica3 | 0,649 | INFORME red cruda | 0,64861863345 | coincide |  |
| Personas con AUC red_ica3 sobre 0,5 | 41 | INFORME red cruda | 41 | coincide |  |
| AUC ica3_full | 0,621 | INFORME red cruda | 0,620779147224 | coincide |  |
| Personas con AUC ica3_full sobre 0,5 | 41 | INFORME red cruda | 41 | coincide |  |
| AUC red_act | 0,498 | INFORME red cruda | 0,498491277361 | coincide |  |
| Personas con AUC red_act sobre 0,5 | 20 | INFORME red cruda | 20 | coincide |  |
| AUC hgb_eeg_act | 0,524 | INFORME red cruda | 0,523695689888 | coincide |  |
| AUC hgb_eeg_act · IC 95 % superior | 0,551 | INFORME red cruda | 0,550493483975 | coincide con redondeo |  |
| Personas con AUC hgb_eeg_act sobre 0,5 | 26 | INFORME red cruda | 26 | coincide |  |
| AUC hgb_c1 | 0,518 | INFORME red cruda | 0,517629996138 | coincide |  |
| Personas con AUC hgb_c1 sobre 0,5 | 22 | INFORME red cruda | 22 | coincide |  |
| R1 | 0,035 | INFORME red cruda | 0,035021295822 | coincide | 32/41; p 0.000005; IC90 [0.0252; 0.0449] |
| R2 | 0,028 | INFORME red cruda | 0,027839486226 | coincide | 30/41; p 0.000845; IC90 [0.0150; 0.0407] |
| R3 | 0,067 | INFORME red cruda | 0,067297224957 | coincide | 39/41; p 0.000005; IC90 [0.0553; 0.0798] |
| R4 | −0,025 | INFORME red cruda | −0,025204412527 | coincide | 15/41; p 0.099500; IC90 [-0.0497; -0.0013] |
| R1 en la partición 1101 | 0,033 | INFORME red cruda, robustez | 0,033440889598 | coincide |  |
| R2 en la partición 1101 | 0,028 | INFORME red cruda, robustez | 0,02801147591 | coincide |  |
| R3 en la partición 1101 | 0,068 | INFORME red cruda, robustez | 0,067509634365 | coincide |  |
| R4 en la partición 1101 | −0,039 | INFORME red cruda, robustez | −0,038741941947 | coincide |  |
| R1 en la partición 1102 | 0,036 | INFORME red cruda, robustez | 0,036075616083 | coincide |  |
| R2 en la partición 1102 | 0,024 | INFORME red cruda, robustez | 0,023795720209 | coincide |  |
| R3 en la partición 1102 | 0,068 | INFORME red cruda, robustez | 0,068429140695 | coincide |  |
| R4 en la partición 1102 | −0,042 | INFORME red cruda, robustez | −0,041479993314 | coincide con redondeo |  |
| R1 en la partición 1103 | 0,039 | INFORME red cruda, robustez | 0,038723133765 | coincide |  |
| R2 en la partición 1103 | 0,030 | INFORME red cruda, robustez | 0,029926323406 | coincide |  |
| R3 en la partición 1103 | 0,068 | INFORME red cruda, robustez | 0,067906180918 | coincide |  |
| R4 en la partición 1103 | −0,021 | INFORME red cruda, robustez | −0,020456632021 | coincide con redondeo |  |
| R1 en la partición 1104 | 0,037 | INFORME red cruda, robustez | 0,037366346475 | coincide |  |
| R2 en la partición 1104 | 0,032 | INFORME red cruda, robustez | 0,031494750672 | coincide con redondeo |  |
| R3 en la partición 1104 | 0,067 | INFORME red cruda, robustez | 0,067363526096 | coincide |  |
| R4 en la partición 1104 | 0,002 | INFORME red cruda, robustez | 0,002135951532 | coincide |  |
| R1 en la partición 1105 | 0,030 | INFORME red cruda, robustez | 0,029500493187 | coincide |  |
| R2 en la partición 1105 | 0,026 | INFORME red cruda, robustez | 0,025969160935 | coincide |  |
| R3 en la partición 1105 | 0,065 | INFORME red cruda, robustez | 0,065277642711 | coincide |  |
| R4 en la partición 1105 | −0,028 | INFORME red cruda, robustez | −0,027479446886 | coincide con redondeo |  |
| R1 con la partición 1105 sola: IC 95 % inferior | 0,017 | INFORME red cruda, límites | 0,017226340912 | coincide |  |
| R1 sin P23 y P39 | 0,0364 | AUDITORIA_RESULTADOS red | 0,036415007586 | coincide |  |
| R1 sin P23 y P39 (informe, 3 decimales) | 0,036 | INFORME red cruda | 0,036415007586 | coincide |  |
| R2 sin P23 y P39 | 0,0282 | AUDITORIA_RESULTADOS red | 0,02824550689 | coincide |  |
| R2 sin P23 y P39 (informe, 3 decimales) | 0,028 | INFORME red cruda | 0,02824550689 | coincide |  |
| R3 sin P23 y P39 | 0,0680 | AUDITORIA_RESULTADOS red | 0,068002156609 | coincide |  |
| R3 sin P23 y P39 (informe, 3 decimales) | 0,068 | INFORME red cruda | 0,068002156609 | coincide |  |
| R4 sin P23 y P39 | −0,0273 | AUDITORIA_RESULTADOS red | −0,027316014836 | coincide |  |
| R4 sin P23 y P39 (informe, 3 decimales) | −0,027 | INFORME red cruda | −0,027316014836 | coincide |  |
| R1 dejando una persona fuera: IC 95 % inferior mínimo | 0,0215 | AUDITORIA_RESULTADOS red | 0,021475393369 | coincide |  |
| R1 dejando una persona fuera: IC 95 % inferior máximo | 0,0257 | AUDITORIA_RESULTADOS red | 0,025731905378 | coincide |  |
| R2 dejando una persona fuera: IC 95 % inferior mínimo | 0,0100 | AUDITORIA_RESULTADOS red | 0,010027364667 | coincide |  |
| R2 dejando una persona fuera: IC 95 % inferior máximo | 0,0173 | AUDITORIA_RESULTADOS red | 0,017263757691 | coincide |  |
| R3 dejando una persona fuera: IC 95 % inferior mínimo | 0,0508 | AUDITORIA_RESULTADOS red | 0,050758343275 | coincide |  |
| R4 pasa a "inferior" al quitar a P10, P24, P33, P34 o P40 (0 = exactamente esas cinco) | 0 | INFORME red cruda | 0 | coincide | ['P10', 'P24', 'P33', 'P34', 'P40']; IC superior al quitarlas: P10 -0.00145; P24 -0.00075; P33 -0.00077; P34 -0.00081; P40 -0.00070 |
| R1 mantiene "efecto relevante" al quitar cualquier persona (0 = sí) | 0 | INFORME red cruda | 0 | coincide |  |
| R3 mantiene "efecto relevante" al quitar cualquier persona (0 = sí) | 0 | INFORME red cruda | 0 | coincide |  |
| R2 mantiene IC 95 % inferior > 0 al quitar cualquier persona (0 = sí) | 0 | INFORME red cruda | 0 | coincide |  |
| Las dos personas más favorables a R1 son P21 y P18 (0 = sí) | 0 | INFORME red cruda | 0 | coincide | ['P21', 'P18'] |
| R1 sin P21 y P18: IC 95 % inferior | 0,0199 | INFORME red cruda | 0,020111620478 | difiere |  |
| R1 sin P21 y P18: IC 95 % inferior con otras 30 semillas de remuestreo (mínimo) | — | — | 0,019743183538 | sin cifra informada | máximo 0.02018; bajo 0,02 en 23 de 30; t de Student 0.01944 |
| R1: IC 95 % inferior con 30 semillas, mínimo | 0,0230 | AUDITORIA_RESULTADOS red ("entre 0,0230 y 0,0234") | 0,02290259658 | coincide con redondeo | máximo 0.02337 |
| R1 − R2 (cambio de la ventaja de la red al limpiar) | 0,007 | Auditoría 23-11, I1 | 0,007181809595 | coincide | p 0.288; 20/41; IC90 [-0.0034; 0.0182] |
| R1 − R2: p | 0,29 | Auditoría 23-11, I1 | 0,287713561432 | coincide |  |
| R1 − R2: personas | 20 | Auditoría 23-11, I1 | 20 | coincide |  |
| (EEG + mirada + pupila) − solo EEG, activación | −0,006 | Auditoría 23-11, I6 | −0,00606569375 | coincide |  |
| HGB solo EEG en activación − 0,5: p | 0,09 | INFORME red cruda | 0,092674536627 | coincide |  |
| Desviación entre semillas de la AUC por persona, red de activación (media) | 0,045 | AUDITORIA_RESULTADOS red ("cercana a 0,045") | 0,045164992176 | coincide | HGB solo EEG 0.0396 |
| AUC de la red original juntando todas las ventanas (media de 5 particiones) | 0,684 | INFORME red cruda | 0,683719895744 | coincide | por partición: 0.68912; 0.68334; 0.68075; 0.68349; 0.68189 |
| Ídem, con la probabilidad promediada sobre particiones | — | — | 0,690381106631 | sin cifra informada |  |
| Spearman medio por persona, prob. red_orig con el recorrido de la mirada (invertido) | 0,48 | INFORME red cruda | 0,484655511167 | coincide |  |
| Spearman medio por persona, prob. eeg_c1 con el recorrido de la mirada (invertido) | 0,41 | INFORME red cruda | 0,414305366441 | coincide |  |
| Spearman medio por persona, prob. red_ica3 con el recorrido de la mirada (invertido) | 0,33 | INFORME red cruda | 0,329782724232 | coincide |  |
| Spearman medio por persona, prob. red_orig con el puntaje ocular | 0,45 | AUDITORIA_RESULTADOS red | 0,454042033751 | coincide |  |
| Spearman medio por persona, prob. red_ica3 con el puntaje ocular | 0,32 | AUDITORIA_RESULTADOS red | 0,319691434188 | coincide |  |
| Parámetros entrenables de la red (conteo analítico) | 1217 | INFORME red cruda | 1217 | coincide | capa lineal con 112 entradas |
| Duración del núcleo temporal, s | 0,26 | INFORME red cruda | 0,256 | coincide |  |
| Ventanas con la entrada toda en cero (tensor original, 22.211 ventanas) | 50 | INFORME red cruda | 50 | coincide | con etiqueta de atención 50; con etiqueta de activación 23; personas ['P11', 'P12', 'P13', 'P16', 'P20', 'P21', 'P22', 'P26', 'P27', 'P28', 'P30', 'P31', 'P32', 'P34', 'P36', 'P37', 'P38', 'P39', 'P4', 'P40', 'P46', 'P47', 'P6'] |
| Ventanas con la entrada toda en cero (tensor limpio) | 50 | INFORME red cruda | 50 | coincide |  |
| Forma del tensor: ventanas | 22211 | INFORME red cruda | 22211 | coincide | (22211, 16, 240) |

### 6. Montaje (`montaje_ocular_41p_23-11-2026`)

| Cifra | Informado | Dónde | Recalculado | Veredicto | Nota |
|---|---|---|---|---|---|
| Desfase EEG–seguidor ocular (parpadeo): mínimo, s | 0,18 | INFORME montaje | 0,184 | coincide |  |
| Desfase: máximo, s | 0,53 | INFORME montaje | 0,528 | coincide |  |
| Desfase: mediana, s | 0,45 | INFORME montaje | 0,448 | coincide |  |
| Desfase: cuartil inferior, s | 0,28 | INFORME montaje | 0,28 | coincide |  |
| Desfase: cuartil superior, s | 0,48 | INFORME montaje | 0,48 | coincide |  |
| Personas con desfase positivo (parpadeo) | 41 | INFORME montaje | 41 | coincide |  |
| Personas con desfase positivo (mirada horizontal) | 41 | Auditoría 23-11, M9 | 41 | coincide |  |
| Personas con desfase no positivo (mirada vertical) | 4 | Auditoría 23-11, M9 | 4 | coincide | mínimo -0.808 s |
| Desfase como % de la ventana de 2 s: mínimo | 9 % | Borradores ("9–26 %"); el INFORME dice 12 % | 9,2 % | coincide |  |
| Desfase como % de la ventana de 2 s: máximo | 26 % | Borradores ("9–26 %"); el INFORME dice 25 % | 26,4 % | coincide |  |
| Desfase como % de la ventana de 2 s: mediana | 22 % | Borradores | 22,4 % | coincide |  |
| INFORME montaje: "entre un 12 % y un 25 %" — mínimo | 12 % | INFORME montaje | 9,2 % | difiere |  |
| INFORME montaje: "entre un 12 % y un 25 %" — máximo | 25 % | INFORME montaje | 26,4 % | difiere |  |
| Grupo 1 (P2 a P21, P36, P37): mediana del desfase, s | 0,27 | INFORME montaje; cierre | 0,28 | coincide con redondeo | n=19; rango 0.184–0.352; media 0.2787 |
| Grupo 2 (resto): mediana del desfase, s | 0,47 | INFORME montaje; cierre | 0,48 | coincide con redondeo | n=22; rango 0.440–0.528; media 0.4840 |
| Separación limpia entre grupos (0 = el máximo del grupo 1 es menor que el mínimo del grupo 2) | 0 | INFORME montaje | 0 | coincide |  |
| Amplitud del parpadeo, canal 0 (Fp1), mediana µV | 148 | INFORME montaje | 148,362792083205 | coincide |  |
| Amplitud del parpadeo, canal 1 (Fp2), mediana µV | 151 | INFORME montaje | 151,023700331505 | coincide |  |
| Amplitud del parpadeo, canal 8 (F7), mediana µV | 74 | INFORME montaje | 73,562597960738 | coincide |  |
| Amplitud del parpadeo, canal 9 (F8), mediana µV | 77 | INFORME montaje | 77,424503976093 | coincide |  |
| Amplitud del parpadeo, canal 10 (F3), mediana µV | 57 | INFORME montaje | 57,486473034337 | coincide |  |
| Amplitud del parpadeo, canal 11 (F4), mediana µV | 56 | INFORME montaje | 56,405281919059 | coincide |  |
| Central y temporal (2, 3, 12, 13): mínimo µV | 25 | INFORME montaje | 24,720440841375 | coincide |  |
| Central y temporal: máximo µV | 29 | INFORME montaje | 28,877592592036 | coincide |  |
| Parietal y occipital (4–7, 14, 15): mínimo µV | 18 | INFORME montaje | 18,45668517256 | coincide |  |
| Parietal y occipital: máximo µV | 24 | INFORME montaje | 23,875706416723 | coincide |  |
| Frontopolar "unos 150 µV": media de Fp1 y Fp2 | 150 | Borradores | 149,693246207355 | coincide |  |
| Posterior "unos 20 µV": mediana de las 6 medianas posteriores | 20 | Borradores | 19,8867287509 | coincide |  |
| Personas cuyo canal de mayor respuesta al parpadeo es 0 o 1 | 27 | INFORME montaje | 27 | coincide |  |
| Personas con F7 y F8 utilizables | 37 | INFORME montaje | 37 | coincide |  |
| Personas con signo opuesto de la mirada horizontal en F7 y F8 | 31 | INFORME montaje | 31 | coincide |  |
| Canales con mayor acoplamiento horizontal son 9, 13, 5 y 3 (0 = sí) | 0 | INFORME montaje | 0 | coincide | [9, 13, 5, 3] |
| Canales utilizables por persona: mínimo | 11 | INFORME montaje | 11 | coincide |  |
| Canales utilizables por persona: máximo | 16 | INFORME montaje | 16 | coincide |  |
| Canales utilizables por persona: mediana | 15 | INFORME montaje | 15 | coincide |  |
| Canales con más pérdidas son P4, O1, P7 y P3 (0 = sí) | 0 | INFORME montaje | 0 | coincide | ['P4', 'O1', 'P3', 'P7'] |
| Parpadeos detectados por persona: mínimo | 19 | INFORME montaje | 19 | coincide |  |
| Parpadeos detectados por persona: máximo | 393 | INFORME montaje | 393 | coincide |  |
| Frecuencia de muestreo efectiva, Hz | 125,1 | INFORME montaje | 125,135943388302 | coincide | rango 125.008–125.167 |
| Mayor hueco entre muestras, s | 0,19 | INFORME montaje | 0,190080165863 | coincide |  |
| Correlación máxima más baja entre personas (parpadeo) — "cercana a 0,1" | 0,1 | INFORME montaje | 0,080276322247 | coincide |  |
| Crudos, 41 personas: diferencia máxima del desfase del parpadeo frente a personas.csv, s | 0,000000000 | crudos en caché (41 personas) | 0 | coincide |  |
| Crudos, 41 personas: discrepancias en canales utilizables, parpadeos o canal utilizable | 0 | crudos en caché (41 personas) | 0 | coincide |  |
| Crudos, 41 personas: diferencia máxima de amplitud del parpadeo por canal, µV | 0,000000 | crudos en caché (41 personas) | 0 | coincide |  |
| Crudos, 41 personas: diferencia máxima de la correlación horizontal por canal | 0,000000000 | crudos en caché (41 personas) | 0 | coincide |  |
| Crudos: desfase mínimo, s | 0,18 | crudos en caché (41 personas) | 0,184 | coincide |  |
| Crudos: desfase máximo, s | 0,53 | crudos en caché (41 personas) | 0,528 | coincide |  |
| Crudos: desfase mediano, s | 0,45 | crudos en caché (41 personas) | 0,448 | coincide |  |
| Crudos: amplitud mediana del parpadeo en Fp1, µV | 148 | crudos en caché (41 personas) | 148,362792083205 | coincide |  |
| Crudos: amplitud mediana del parpadeo en Fp2, µV | 151 | crudos en caché (41 personas) | 151,023700331505 | coincide |  |
| Crudos: personas con signo opuesto en F7 y F8 | 31 | crudos en caché (41 personas) | 31 | coincide | de 37 |
| Detalle P18: desfase del parpadeo, s | 0,264 | personas.csv | 0,264 | coincide | 15 canales; 73 parpadeos; Fp1 90.10 µV; Fp2 95.80 µV; F7 +0.1431; F8 -0.2167 |
| Detalle P23: desfase del parpadeo, s | 0,448 | personas.csv | 0,448 | coincide | 14 canales; 208 parpadeos; Fp1 215.24 µV; Fp2 271.17 µV; F7 -0.0079; F8 -0.2342 |
| Detalle P26: desfase del parpadeo, s | 0,496 | personas.csv | 0,496 | coincide | 15 canales; 131 parpadeos; Fp1 59.88 µV; Fp2 70.93 µV; F7 +0.0128; F8 -0.0895 |
| Detalle P40: desfase del parpadeo, s | 0,520 | personas.csv | 0,52 | coincide | 16 canales; 86 parpadeos; Fp1 85.12 µV; Fp2 107.91 µV; F7 +0.0231; F8 -0.0195 |
| Detalle P44: desfase del parpadeo, s | 0,472 | personas.csv | 0,472 | coincide | 16 canales; 144 parpadeos; Fp1 263.23 µV; Fp2 288.59 µV; F7 +0.1552; F8 -0.1809 |

### 7. Etapas del 16-11 (cierre V3, análisis final, robustez)

| Cifra | Informado | Dónde | Recalculado | Veredicto | Nota |
|---|---|---|---|---|---|
| V3: diferencia máxima de AUC media frente a metricas.csv (54 filas) | 0,000000000 | cierre_v3 metricas.csv | 0 | coincide |  |
| V3: diferencia máxima de BA media frente a metricas.csv (54 filas) | 0,000000000 | cierre_v3 metricas.csv | 0 | coincide |  |
| V3: diferencia máxima de macro-F1 media frente a metricas.csv (54 filas) | 0,000000000 | cierre_v3 metricas.csv | 0 | coincide |  |
| V3: diferencia máxima de recall de la clase alta media frente a metricas.csv (54 filas) | 0,000000000 | cierre_v3 metricas.csv | 0 | coincide |  |
| V3: diferencia máxima de recall de la clase baja media frente a metricas.csv (54 filas) | 0,000000000 | cierre_v3 metricas.csv | 0 | coincide |  |
| V3: diferencia máxima de los IC 95 % de las cinco métricas (misma semilla) | 0,000000000 | cierre_v3 metricas.csv | 0 | coincide |  |
| V3: personas por partición — entrenamiento | 25 | INFORME cierre V3 | 25 | coincide |  |
| V3: personas por partición — validación | 8 | INFORME cierre V3 | 8 | coincide |  |
| V3: personas por partición — test | 8 | INFORME cierre V3 | 8 | coincide |  |
| V3 test atencion hgb_c1: BA / macro-F1 / recall alta / recall baja (se registra BA) | — | cierre_v3 metricas.csv | 0,610248274421 | coincide | macro-F1 0.598675; recall alta 0.531235; recall baja 0.689261 |
| V3 test atencion hgb_c32: BA / macro-F1 / recall alta / recall baja (se registra BA) | — | cierre_v3 metricas.csv | 0,621125403225 | coincide | macro-F1 0.609302; recall alta 0.561708; recall baja 0.680543 |
| V3 test atencion gru_c32: BA / macro-F1 / recall alta / recall baja (se registra BA) | — | cierre_v3 metricas.csv | 0,576464530035 | coincide | macro-F1 0.533244; recall alta 0.436958; recall baja 0.715971 |
| V3 test activacion hgb_c1: BA / macro-F1 / recall alta / recall baja (se registra BA) | — | cierre_v3 metricas.csv | 0,50388643813 | coincide | macro-F1 0.485815; recall alta 0.619252; recall baja 0.388521 |
| V3 test activacion hgb_c32: BA / macro-F1 / recall alta / recall baja (se registra BA) | — | cierre_v3 metricas.csv | 0,541818815317 | coincide | macro-F1 0.520787; recall alta 0.666072; recall baja 0.417566 |
| V3 test activacion gru_c32: BA / macro-F1 / recall alta / recall baja (se registra BA) | — | cierre_v3 metricas.csv | 0,53706813099 | coincide | macro-F1 0.488032; recall alta 0.387981; recall baja 0.686155 |
| V3 test atencion hgb_c1: AUC | 0,662 | INFORME cierre V3 | 0,661566434765 | coincide |  |
| V3 test atencion hgb_c32: AUC | 0,690 | INFORME cierre V3 | 0,690273362995 | coincide |  |
| V3 test atencion gru_c32: AUC | 0,640 | INFORME cierre V3 | 0,640271446222 | coincide |  |
| V3 test activacion hgb_c1: AUC | 0,514 | INFORME cierre V3 | 0,514086623161 | coincide |  |
| V3 test activacion hgb_c32: AUC | 0,547 | INFORME cierre V3 | 0,547005505658 | coincide |  |
| V3 test activacion gru_c32: AUC | 0,583 | INFORME cierre V3 | 0,583054438126 | coincide |  |
| V3 activación, entrenamiento: AUC mínima entre estrategias ("entre 0,50 y 0,53") | 0,50 | INFORME cierre V3 | 0,496464835029 | coincide | máxima 0.5316 |
| V3 activación, entrenamiento: AUC máxima entre estrategias | 0,53 | INFORME cierre V3 | 0,531580189037 | coincide |  |
| V3 atencion hgb_c32 − hgb_c1, oof_train | 0,018 | INFORME cierre V3 | 0,018453021956 | coincide |  |
| V3 atencion hgb_c32 − hgb_c1, oof_train: personas que mejoran | 20 | INFORME cierre V3 | 20 | coincide |  |
| V3 atencion hgb_c32 − hgb_c1, validation | 0,020 | INFORME cierre V3 | 0,020417293294 | coincide |  |
| V3 atencion hgb_c32 − hgb_c1, validation: personas que mejoran | 6 | INFORME cierre V3 | 6 | coincide |  |
| V3 atencion hgb_c32 − hgb_c1, test | 0,029 | INFORME cierre V3 | 0,028706928229 | coincide |  |
| V3 atencion hgb_c32 − hgb_c1, test: personas que mejoran | 7 | INFORME cierre V3 | 7 | coincide |  |
| V3 atencion gru_c32 − gru_c1, oof_train | 0,001 | INFORME cierre V3 | 0,0008876746 | coincide |  |
| V3 atencion gru_c32 − gru_c1, oof_train: personas que mejoran | 11 | INFORME cierre V3 | 11 | coincide |  |
| V3 atencion gru_c32 − gru_c1, validation | −0,004 | INFORME cierre V3 | −0,003505218481 | coincide |  |
| V3 atencion gru_c32 − gru_c1, validation: personas que mejoran | 4 | INFORME cierre V3 | 4 | coincide |  |
| V3 atencion gru_c32 − gru_c1, test | 0,010 | INFORME cierre V3 | 0,009512610675 | coincide |  |
| V3 atencion gru_c32 − gru_c1, test: personas que mejoran | 5 | INFORME cierre V3 | 5 | coincide |  |
| V3 activacion hgb_c32 − hgb_c1, oof_train | 0,016 | INFORME cierre V3 | 0,016204841039 | coincide |  |
| V3 activacion hgb_c32 − hgb_c1, oof_train: personas que mejoran | 15 | INFORME cierre V3 | 15 | coincide |  |
| V3 activacion hgb_c32 − hgb_c1, validation | 0,059 | INFORME cierre V3 | 0,058721977152 | coincide |  |
| V3 activacion hgb_c32 − hgb_c1, validation: personas que mejoran | 5 | INFORME cierre V3 | 5 | coincide |  |
| V3 activacion hgb_c32 − hgb_c1, test | 0,033 | INFORME cierre V3 | 0,032918882497 | coincide |  |
| V3 activacion hgb_c32 − hgb_c1, test: personas que mejoran | 4 | INFORME cierre V3 | 4 | coincide |  |
| V3 activacion gru_c32 − gru_c1, oof_train | −0,016 | INFORME cierre V3 | −0,015782854578 | coincide |  |
| V3 activacion gru_c32 − gru_c1, oof_train: personas que mejoran | 13 | INFORME cierre V3 | 13 | coincide |  |
| V3 activacion gru_c32 − gru_c1, validation | 0,091 | INFORME cierre V3 | 0,090692660217 | coincide |  |
| V3 activacion gru_c32 − gru_c1, validation: personas que mejoran | 6 | INFORME cierre V3 | 6 | coincide |  |
| V3 activacion gru_c32 − gru_c1, test | 0,084 | INFORME cierre V3 | 0,084312580131 | coincide |  |
| V3 activacion gru_c32 − gru_c1, test: personas que mejoran | 7 | INFORME cierre V3 | 7 | coincide |  |
| V3 atencion tardia_c32 − hgb_c32, oof_train | −0,010 | INFORME cierre V3 | −0,010392843689 | coincide |  |
| V3 atencion tardia_c32 − hgb_c32, oof_train: personas que mejoran | 7 | INFORME cierre V3 | 7 | coincide |  |
| V3 atencion tardia_c32 − hgb_c32, validation | −0,008 | INFORME cierre V3 | −0,007531077559 | coincide |  |
| V3 atencion tardia_c32 − hgb_c32, test | −0,002 | INFORME cierre V3 | −0,002168425387 | coincide |  |
| V3 atencion gru_c32 − hgb_c32, oof_train | −0,042 | INFORME cierre V3 | −0,042073840484 | coincide |  |
| V3 atencion gru_c32 − hgb_c32, validation | −0,044 | INFORME cierre V3 | −0,044332240137 | coincide |  |
| V3 atencion gru_c32 − hgb_c32, test | −0,050 | INFORME cierre V3 | −0,050001916772 | coincide |  |
| V3: diferencia máxima de los 54 contrastes (delta, IC, personas) frente a contrastes.csv | 0,000000000 | cierre_v3 contrastes.csv | 0 | coincide |  |
| V3: selección de hojas de activación, AUC media del modelo de 32 ventanas con 15 hojas (solo agregación del CSV) | 0,5311 | Cierre, límites | 0,531066448568 | coincide |  |
| V3: ídem con 7 hojas (solo agregación del CSV) | 0,4994 | Cierre, límites | 0,499414265615 | coincide |  |
| V3: hojas elegidas con la media de los tres largos de historial (0 = 15 hojas) | 0 | INFORME cierre V3 | 0 | coincide | 7 hojas 0.515242; 15 hojas 0.524758 |
| Análisis final: diferencia máxima de AUC y BA medias frente a metricas.csv (10 filas) | 0,000000000 | cierre_final metricas.csv | 0 | coincide |  |
| Heterogeneidad atencion HGB 32 − 1, 25 de entrenamiento: delta | 0,023 | INFORME análisis final; cierre | 0,022790957794 | coincide | n=25 |
| Heterogeneidad atencion HGB 32 − 1, 25 de entrenamiento: IC 95 % inferior (semilla registrada) | 0,014 | INFORME análisis final; cierre | 0,013921824104 | coincide | el CSV guarda 0.0139; diferencia +0.00002 |
| Heterogeneidad atencion HGB 32 − 1, 25 de entrenamiento: IC 95 % superior (semilla registrada) | 0,031 | INFORME análisis final; cierre | 0,031366903856 | coincide | el CSV guarda 0.0314; diferencia -0.00003 |
| Heterogeneidad atencion HGB 32 − 1, 25 de entrenamiento: personas que mejoran | 22 | INFORME análisis final | 22 | coincide | de 25 |
| Heterogeneidad atencion HGB 32 − 1, 16 de validación y test: delta | 0,032 | INFORME análisis final; cierre | 0,032064482949 | coincide | n=16 |
| Heterogeneidad atencion HGB 32 − 1, 16 de validación y test: IC 95 % inferior (semilla registrada) | 0,016 | INFORME análisis final; cierre | 0,015926519969 | coincide | el CSV guarda 0.0159; diferencia +0.00003 |
| Heterogeneidad atencion HGB 32 − 1, 16 de validación y test: IC 95 % superior (semilla registrada) | 0,048 | INFORME análisis final; cierre | 0,048084618492 | coincide | el CSV guarda 0.0481; diferencia -0.00002 |
| Heterogeneidad atencion HGB 32 − 1, 16 de validación y test: personas que mejoran | 14 | INFORME análisis final | 14 | coincide | de 16 |
| Heterogeneidad activacion HGB 32 − 1, 25 de entrenamiento: delta | 0,055 | INFORME análisis final; cierre | 0,055142569981 | coincide | n=25 |
| Heterogeneidad activacion HGB 32 − 1, 25 de entrenamiento: IC 95 % inferior (semilla registrada) | 0,012 | INFORME análisis final; cierre | 0,012167968151 | coincide | el CSV guarda 0.0122; diferencia -0.00003 |
| Heterogeneidad activacion HGB 32 − 1, 25 de entrenamiento: IC 95 % superior (semilla registrada) | 0,101 | INFORME análisis final; cierre | 0,100505291663 | coincide | el CSV guarda 0.1005; diferencia +0.00001 |
| Heterogeneidad activacion HGB 32 − 1, 25 de entrenamiento: personas que mejoran | 17 | INFORME análisis final | 17 | coincide | de 25 |
| Heterogeneidad activacion HGB 32 − 1, 16 de validación y test: delta | 0,001 | INFORME análisis final; cierre | 0,001441403213 | coincide | n=16 |
| Heterogeneidad activacion HGB 32 − 1, 16 de validación y test: IC 95 % inferior (semilla registrada) | −0,052 | INFORME análisis final; cierre | −0,052044608545 | coincide | el CSV guarda -0.052; diferencia -0.00004 |
| Heterogeneidad activacion HGB 32 − 1, 16 de validación y test: IC 95 % superior (semilla registrada) | 0,055 | INFORME análisis final; cierre | 0,054902642772 | coincide | el CSV guarda 0.0549; diferencia +0.00000 |
| Heterogeneidad activacion HGB 32 − 1, 16 de validación y test: personas que mejoran | 7 | INFORME análisis final | 7 | coincide | de 16 |
| Heterogeneidad activacion GRU 32 − 1, 25 de entrenamiento: delta | 0,045 | INFORME análisis final; cierre | 0,04533274498 | coincide | n=25 |
| Heterogeneidad activacion GRU 32 − 1, 25 de entrenamiento: IC 95 % inferior (semilla registrada) | 0,007 | INFORME análisis final; cierre | 0,006544383125 | coincide | el CSV guarda 0.0065; diferencia +0.00004 |
| Heterogeneidad activacion GRU 32 − 1, 25 de entrenamiento: IC 95 % superior (semilla registrada) | 0,083 | INFORME análisis final; cierre | 0,082786156312 | coincide | el CSV guarda 0.0828; diferencia -0.00001 |
| Heterogeneidad activacion GRU 32 − 1, 25 de entrenamiento: personas que mejoran | 17 | INFORME análisis final | 17 | coincide | de 25 |
| Heterogeneidad activacion GRU 32 − 1, 16 de validación y test: delta | 0,059 | INFORME análisis final; cierre | 0,058654773767 | coincide | n=16 |
| Heterogeneidad activacion GRU 32 − 1, 16 de validación y test: IC 95 % inferior (semilla registrada) | 0,014 | INFORME análisis final; cierre | 0,014286265093 | coincide | el CSV guarda 0.0143; diferencia -0.00001 |
| Heterogeneidad activacion GRU 32 − 1, 16 de validación y test: IC 95 % superior (semilla registrada) | 0,102 | INFORME análisis final; cierre | 0,101496370908 | coincide con redondeo | el CSV guarda 0.1015; diferencia -0.00000 |
| Heterogeneidad activacion GRU 32 − 1, 16 de validación y test: personas que mejoran | 11 | INFORME análisis final | 11 | coincide | de 16 |
| Heterogeneidad atencion GRU 32 − 1, 25 de entrenamiento: delta | 0,0040 | heterogeneidad_por_grupo.csv | 0,003956813559 | coincide |  |
| Heterogeneidad atencion GRU 32 − 1, 25 de entrenamiento: personas que mejoran | 15 | INFORME análisis final | 15 | coincide | de 25 |
| Heterogeneidad atencion GRU 32 − 1, 16 de validación y test: delta | 0,0146 | heterogeneidad_por_grupo.csv | 0,014637802305 | coincide |  |
| Heterogeneidad atencion GRU 32 − 1, 16 de validación y test: personas que mejoran | 11 | INFORME análisis final | 11 | coincide | de 16 |
| Tabla por grupo · Principal, 16-11: todas | 0,034 | Cierre, tabla de la auditoría de código | 0,034186017096 | coincide | n=41 |
| Tabla por grupo · Principal, 16-11: 25 de la búsqueda | 0,055 | Cierre, tabla de la auditoría de código | 0,055142569981 | coincide | n=25; 17 a favor |
| Tabla por grupo · Principal, 16-11: 16 restantes | 0,001 | Cierre, tabla de la auditoría de código | 0,001441403213 | coincide | n=16; 7 a favor |
| Tabla por grupo · Principal, 5 particiones: todas | 0,036 | Cierre, tabla de la auditoría de código | 0,036449202357 | coincide | n=41 |
| Tabla por grupo · Principal, 5 particiones: 25 de la búsqueda | 0,046 | Cierre, tabla de la auditoría de código | 0,046137883066 | coincide | n=25; 16 a favor |
| Tabla por grupo · Principal, 5 particiones: 16 restantes | 0,021 | Cierre, tabla de la auditoría de código | 0,02131063875 | coincide | n=16; 7 a favor |
| Tabla por grupo · Con tiempo de sesión: todas | 0,026 | Cierre, tabla de la auditoría de código | 0,026269239358 | coincide | n=41 |
| Tabla por grupo · Con tiempo de sesión: 25 de la búsqueda | 0,050 | Cierre, tabla de la auditoría de código | 0,049954138418 | coincide | n=25; 19 a favor |
| Tabla por grupo · Con tiempo de sesión: 16 restantes | −0,011 | Cierre, tabla de la auditoría de código | −0,010738415423 | coincide | n=16; 8 a favor |
| Tabla por grupo · Con posición (Q1): todas | 0,032 | Cierre, tabla de la auditoría de código | 0,032253327521 | coincide | n=41 |
| Tabla por grupo · Con posición (Q1): 25 de la búsqueda | 0,049 | Cierre, tabla de la auditoría de código | 0,049335377184 | coincide | n=25; 18 a favor |
| Tabla por grupo · Con posición (Q1): 16 restantes | 0,006 | Cierre, tabla de la auditoría de código | 0,005562624922 | coincide | n=16; 10 a favor |
| Tabla por grupo · Historial − posición (18-11): todas | 0,038 | Cierre, tabla de la auditoría de código | 0,038148733652 | coincide | n=41 |
| Tabla por grupo · Historial − posición (18-11): 25 de la búsqueda | 0,063 | Cierre, tabla de la auditoría de código | 0,06327945208 | coincide | n=25; 17 a favor |
| Tabla por grupo · Historial − posición (18-11): 16 restantes | −0,001 | Cierre, tabla de la auditoría de código | −0,00111801389 | coincide | n=16; 7 a favor |
| Tabla por grupo · Historial − placebo (16-11): todas | 0,038 | Cierre, tabla de la auditoría de código | 0,037872581339 | coincide | n=41 |
| Tabla por grupo · Historial − placebo (16-11): 25 de la búsqueda | 0,057 | Cierre, tabla de la auditoría de código | 0,056851698739 | coincide | n=25; 17 a favor |
| Tabla por grupo · Historial − placebo (16-11): 16 restantes | 0,008 | Cierre, tabla de la auditoría de código | 0,0082177104 | coincide | n=16; 9 a favor |
| Tabla por grupo · Historial desplazado 6 − placebo: todas | 0,046 | Cierre, tabla de la auditoría de código | 0,046037714642 | coincide | n=41 |
| Tabla por grupo · Historial desplazado 6 − placebo: 25 de la búsqueda | 0,035 | Cierre, tabla de la auditoría de código | 0,034579090986 | coincide | n=25; 17 a favor |
| Tabla por grupo · Historial desplazado 6 − placebo: 16 restantes | 0,064 | Cierre, tabla de la auditoría de código | 0,063941814105 | coincide | n=16; 11 a favor |
| Tabla por grupo · Banda de 6 s − placebo: todas | 0,047 | Cierre, tabla de la auditoría de código | 0,047123661703 | coincide | n=40 |
| Tabla por grupo · Banda de 6 s − placebo: 25 de la búsqueda | 0,058 | Cierre, tabla de la auditoría de código | 0,058324358936 | coincide | n=24; 19 a favor |
| Tabla por grupo · Banda de 6 s − placebo: 16 restantes | 0,030 | Cierre, tabla de la auditoría de código | 0,030322615852 | coincide | n=16; 11 a favor |
| Tabla por grupo · GRU hasta 32 − GRU una ventana: todas | 0,051 | Cierre, tabla de la auditoría de código | 0,050531585483 | coincide | n=41 |
| Tabla por grupo · GRU hasta 32 − GRU una ventana: 25 de la búsqueda | 0,045 | Cierre, tabla de la auditoría de código | 0,04533274498 | coincide | n=25; 17 a favor |
| Tabla por grupo · GRU hasta 32 − GRU una ventana: 16 restantes | 0,059 | Cierre, tabla de la auditoría de código | 0,058654773767 | coincide | n=16; 11 a favor |
| Principal 16-11 de activación: diferencia entre grupos (25 − 16) y p por permutación de grupo | — | Cierre, límites ("no es significativa con 16 personas") | 0,053701166769 | sin cifra informada | p bilateral 0.1510 (20.000 permutaciones, semilla 20261127) |
| Robustez R3 activación, partición 101 | 0,042 | INFORME robustez ("+0,042 en las tres") | 0,043242255694 | difiere |  |
| Robustez R3 activación, partición 202 | 0,042 | INFORME robustez ("+0,042 en las tres") | 0,041591224335 | coincide |  |
| Robustez R3 activación, partición 303 | 0,042 | INFORME robustez ("+0,042 en las tres") | 0,041600778901 | coincide |  |

### 8. Etiquetas

| Cifra | Informado | Dónde | Recalculado | Veredicto | Nota |
|---|---|---|---|---|---|
| Ventanas de las 41 personas | 22211 | INFORME etiquetas_gsr_calidad_v2 | 22211 | coincide |  |
| Ventanas en train | 13524 | INFORME etiquetas_gsr_calidad_v2 | 13524 | coincide |  |
| Ventanas en validation | 4662 | INFORME etiquetas_gsr_calidad_v2 | 4662 | coincide |  |
| Ventanas en test | 4025 | INFORME etiquetas_gsr_calidad_v2 | 4025 | coincide |  |
| Ventanas con etiqueta de activación (tabla guardada) | 11796 | INFORME etiquetas_gsr_calidad_v2 | 11796 | coincide |  |
| Ventanas con etiqueta de activación (reconstrucción propia desde las variables) | 11796 | INFORME etiquetas_gsr_calidad_v2 | 11796 | coincide |  |
| Etiquetas de activación reconstruidas idénticas a las guardadas (ventanas distintas) | 0 | INFORME etiquetas_gsr_calidad_v2 | 0 | coincide |  |
| % de ventanas que conserva la etiqueta de activación | 53,1 % | INFORME etiquetas_gsr_calidad_v2 | 53,108819954077 % | coincide |  |
| % de ventanas que conserva la etiqueta (cierre: "53 %") | 53 % | Cierre, límites | 53,108819954077 % | coincide |  |
| Ventanas sin etiqueta | 10415 | INFORME etiquetas_gsr_calidad_v2 | 10415 | coincide |  |
| Sin etiqueta por cobertura/flag inválido | 401 | INFORME etiquetas_gsr_calidad_v2 | 401 | coincide |  |
| Sin etiqueta por empate con la mediana | 19 | INFORME etiquetas_gsr_calidad_v2 | 19 | coincide |  |
| Sin etiqueta por historial insuficiente | 9995 | INFORME etiquetas_gsr_calidad_v2 | 9995 | coincide |  |
| Etiquetas de activación en train | 7028 | INFORME etiquetas_gsr_calidad_v2 | 7028 | coincide |  |
| Etiquetas de activación en validation | 2584 | INFORME etiquetas_gsr_calidad_v2 | 2584 | coincide |  |
| Etiquetas de activación en test | 2184 | INFORME etiquetas_gsr_calidad_v2 | 2184 | coincide |  |
| P4: ventanas con etiqueta de activación | 26 | INFORME etiquetas_gsr_calidad_v2 | 26 | coincide |  |
| P4: ventanas totales | 459 | INFORME etiquetas_gsr_calidad_v2 | 459 | coincide |  |
| Personas con ambas clases de activación | 41 | INFORME etiquetas_gsr_calidad_v2 | 41 | coincide |  |
| Ventanas con etiqueta de atención (reconstrucción propia del puntaje) | 22176 | Auditoría 23-11, integridad | 22176 | coincide |  |
| Ventanas de atención en las predicciones guardadas | 22176 | Auditoría 23-11 | 22176 | coincide |  |
| Etiquetas de atención de las predicciones distintas de las reconstruidas | 0 | — | 0 | coincide |  |
| Ventanas válidas de entrenamiento del Modelo Profesor | 13498 | INFORME profesor_binario | 13498 | coincide |  |
| Ventanas de entrenamiento omitidas por componentes incompletos | 26 | INFORME profesor_binario | 26 | coincide |  |
| % de varianza de la primera componente | 51,5 % | Borrador Resultados §2 | 51,515276969822 % | coincide |  |
| Peso PCA: duración total de fijaciones | 0,398 | Borrador Resultados §2; cierre H3 | 0,397604072037 | coincide |  |
| Peso PCA: duración media de fijación | — | Borrador Resultados §2; cierre H3 | 0,508486178763 | sin cifra informada |  |
| Peso PCA: dispersión de la mirada | — | Borrador Resultados §2; cierre H3 | 0,520441092703 | sin cifra informada |  |
| Peso PCA: recorrido de la mirada | — | Borrador Resultados §2; cierre H3 | 0,556603694266 | sin cifra informada |  |
| Peso PCA: pupila | −0,052 | Borrador Resultados §2; cierre H3 | −0,051828606604 | coincide |  |
| Peso mínimo de las cuatro variables de mirada | 0,40 | INFORME enfoques ("0,40 a 0,56") | 0,397604072037 | coincide |  |
| Peso máximo de las cuatro variables de mirada | 0,56 | INFORME enfoques ("0,40 a 0,56") | 0,556603694266 | coincide |  |
| % de concordancia entre profesor igualitario y PCA | 66,28 % | INFORME profesor_binario | 66,276485405245 % | coincide |  |
| Kappa entre profesor igualitario y PCA | 0,3255 | INFORME profesor_binario | 0,325528982533 | coincide |  |
| Ventanas comparadas entre profesores | 13498 | INFORME profesor_binario | 13498 | coincide |  |
| % de ventanas con etiqueta de atención y fijaciones > 2.000 ms | 28 % | Cierre, límites ("cerca del 28 %") | 27,741702741703 % | coincide |  |
| AUC del nivel tónico de la ventana contra la etiqueta de activación (media por persona) | 0,911 | Cierre H2 | 0,910604694567 | coincide |  |
| Ídem, juntando todas las ventanas | — | — | 0,881993177564 | sin cifra informada |  |
| AUC de la componente fásica de la ventana contra la etiqueta de activación (media de las personas en que la variable varía) | 0,595 | Borrador Resultados §2; AUDITORIA_CODIGO | 0,594618708079 | coincide | 41 personas; con las 41 (constante = 0,5): 0.594619 |
| AUC de la número de respuestas de la ventana contra la etiqueta de activación (media de las personas en que la variable varía) | 0,522 | Borrador Resultados §2; AUDITORIA_CODIGO | 0,522441096336 | coincide | 32 personas; con las 41 (constante = 0,5): 0.517515 |
| AUC de la prominencia de las respuestas de la ventana contra la etiqueta de activación (media de las personas en que la variable varía) | 0,522 | Borrador Resultados §2; AUDITORIA_CODIGO | 0,5224628252 | coincide | 32 personas; con las 41 (constante = 0,5): 0.517532 |
| Ventanas de activación de clase alta | 5898 | Borrador Secciones pendientes §4.6 | 5898 | coincide |  |
| Ventanas de activación de clase baja | 5898 | Borrador Secciones pendientes §4.6 | 5898 | coincide |  |
| P4: ventanas con GSR válida | 58 | Borrador Secciones pendientes §4.6 | 58 | coincide |  |
| Ventanas del archivo completo | 25992 | Borrador Secciones pendientes §4.7 | 25992 | coincide |  |
| % de ventanas del archivo con fijaciones > 2.000 ms | 27,8 % | Borrador Secciones pendientes §4.7 | 27,750846414281 % | coincide |  |
| % de ventanas de las 41 personas con fijaciones > 2.000 ms | 27,7 % | Borrador Secciones pendientes §4.7 | 27,697987483679 % | coincide |  |
| % de ventanas de las 41 personas con fijaciones > 3.000 ms | 4 % | Borrador Secciones pendientes §4.7 | 4,016028094188 % | coincide |  |
| Duración total máxima de fijaciones en una ventana, ms | 11365 | Borrador Secciones pendientes §4.7 | 11365 | coincide |  |
