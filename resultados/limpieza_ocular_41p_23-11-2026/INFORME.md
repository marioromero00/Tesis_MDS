# Limpieza de artefactos oculares en el EEG y detección de atención — 23-11-2026

Script `scripts/limpieza_ocular_41p.py`. Protocolo registrado y publicado antes de correr (commit `06547f5`), enmienda v2 tras la auditoría de código y antes de ver resultados (commit `441bae9`), ejecutado una vez. Continuación pedida por Mario el 23-11; aborda el pendiente 2 de los cuatro enfoques. Análisis dirigido, no confirmación independiente.

**Pregunta:** ¿cuánto de la detección de la etiqueta de atención desde el EEG se sostiene al quitar del EEG los componentes ligados a los movimientos de ojos y parpadeos?

**Respuesta corta:** la detección cae de 0,681 a 0,621 al quitar tres componentes oculares, que son solo el 3,5 % de la varianza. Quitar tres componentes no oculares, con el 72 % de la varianza, casi no la cambia (0,674). La detección por alfa y beta, que el 22-11 parecía la parte más defendible, también cae: de 0,593 a 0,547.

## Método

- **Limpieza por persona, sin etiquetas.** ICA sobre los canales utilizables de toda la sesión. Cada componente recibe un puntaje ocular: su correlación máxima con la mirada horizontal, la mirada vertical o los parpadeos del seguidor ocular. Se quitan los 3 de mayor puntaje (`ica3`; con 1, 2 y 4 como descriptivos).
- **Control (`ctrl3`).** Se quitan los 3 componentes de mayor varianza entre los que no son oculares.
- **Segundo método (`reg12`).** A cada canal se le resta su regresión sobre Fp1, Fp2, F7 y F8, y esos cuatro se descartan. Se compara con los mismos 12 canales sin regresión (`orig12`).
- **Variables y modelos.** La limpieza es un filtro espacial fijo por persona aplicado a cada ventana cruda; las variables se recalculan con el mismo código de extracción. Modelos de atención solo con EEG, ventana actual, configuración congelada, las mismas 5 particiones y ventanas del 22-11.
- **Verificación.** Con el filtro identidad se reproduce la tabla de variables vigente en las 22.211 ventanas, y el modelo resultante da las mismas probabilidades que `eeg_c1` del 22-11.

## Resultado confirmatorio

AUC por persona promediada sobre 5 particiones; 41 personas; Holm sobre las 4 pruebas.

| Prueba | Contraste | ΔAUC | IC 95 % | A favor | p Holm | Decisión |
|---|---|---|---|---|---|---|
| L1 | EEG original − EEG limpio | +0,060 | [+0,045; +0,075] | 39/41 | < 0,00001 | **Efecto relevante** |
| L2 | Control − EEG limpio | +0,054 | [+0,037; +0,070] | 37/41 | < 0,00001 | **Efecto relevante** |
| L3 | EEG limpio − 0,5 | +0,121 | [+0,107; +0,135] | 41/41 | < 0,00001 | **Efecto relevante** |
| L4 | Alfa y beta limpio − alfa y beta original | −0,045 | [−0,059; −0,033] | 6/41 | < 0,00001 | **Inferior** |

- **L1 y L2:** una parte de la detección viaja en los componentes oculares, y la caída es propia de ellos. El control quita veinte veces más varianza y solo baja la AUC en 0,007 [−0,001; +0,015].
- **L3:** queda detección tras la limpieza (0,621, sobre el azar en las 41 personas).
- **L4:** la lectura fijada de antemano solo contemplaba que alfa y beta no cambiaran. Cambiaron: la detección por alfa y beta también dependía en parte de los componentes oculares.

Las sensibilidades de la enmienda no cambian nada: sin P23 y P39, L1 +0,060 y L2 +0,052; sin esas ni las cinco personas de identificación ocular débil, L1 +0,061 y L2 +0,054.

## Curva por número de componentes quitados

| Condición | AUC | Caída frente al original |
|---|---|---|
| EEG original | 0,681 | — |
| 1 componente ocular | 0,661 | 0,020 |
| 2 componentes oculares | 0,638 | 0,043 |
| 3 componentes oculares | 0,621 | 0,060 |
| 4 componentes oculares | 0,613 | 0,068 |
| 3 componentes no oculares (control) | 0,674 | 0,007 |

La caída se va frenando: el cuarto componente agrega 0,007 [−0,000; +0,015], sin que se pueda afirmar que tocó fondo. Los puntajes oculares medianos de los componentes 1 a 4 son 0,38, 0,23, 0,17 y 0,13; los del control, 0,06 como máximo.

## Por subconjunto de variables

| Variables | Original (22-11) | Limpio (3 componentes) | Caída |
|---|---|---|---|
| Todo el EEG | 0,681 | 0,621 | 0,060 |
| Potencia lenta y amplitud | 0,673 | 0,603 | 0,070 |
| Canales frontales | 0,675 | 0,621 | 0,054 |
| Canales posteriores | 0,602 | 0,562 | 0,040 |
| Alfa y beta | 0,593 | 0,547 | 0,045 |

Tras la limpieza se mantiene el mismo orden: frontales por sobre posteriores (+0,059) y potencia lenta por sobre alfa y beta (+0,055). Ese patrón es el de un artefacto ocular residual.

## Segundo método: regresión con los canales frontales

- Descartar Fp1, Fp2, F7 y F8 sin regresión ya baja la AUC de 0,681 a 0,646.
- La regresión baja otros 0,012 [−0,000; +0,024], hasta 0,634. Coincide en sentido con la ICA pero limpia poco: el acoplamiento con la mirada horizontal no baja.

## Qué tan bien limpió

Correlación máxima (mediana entre personas) entre algún canal y las señales del seguidor ocular:

| Señal | Original | Limpio (3 componentes) | Control |
|---|---|---|---|
| Parpadeo | 0,28 | 0,08 | 0,31 |
| Mirada horizontal | 0,21 | 0,11 | 0,22 |
| Mirada vertical | 0,18 | 0,07 | 0,18 |

La limpieza es parcial. La probabilidad del modelo limpio sigue asociada al recorrido de la mirada (Spearman 0,28, antes 0,41). En el modelo limpio de alfa y beta esa asociación es 0,11.

## Lectura

1. **Al menos 0,06 de AUC de la detección de atención por EEG viene de componentes oculares.** Es una cota inferior: la limpieza es parcial y lo que queda conserva la firma espacial y espectral de un artefacto ocular.
2. **La cifra defendible como no ocular baja.** El 22-11 se estimó en 0,59–0,60 (alfa y beta, canales posteriores). Con la limpieza queda en 0,55–0,56, sobre el azar en 38 de 41 personas.
3. **No se puede afirmar detección cerebral de atención con estos datos.** Lo que queda sobre el azar puede ser residuo ocular, actividad muscular asociada a las sacadas, actividad cerebral ligada al movimiento de los ojos, o variables de calidad de canal que la limpieza no toca. El diseño no los separa, porque la etiqueta se define con los ojos.
4. **El montaje por defecto queda respaldado por los datos** (ver `resultados/montaje_ocular_41p_23-11-2026/INFORME.md`), y el EEG va 0,25–0,5 s desfasado respecto del seguidor ocular.

Para la tesis: el resultado de atención con EEG debe presentarse como detección de la conducta ocular a través de su huella en el EEG, no como un marcador cerebral de atención.

## Límites

- Análisis dirigido sobre personas y resultados ya vistos.
- La limpieza usa toda la sesión de cada persona, también de las evaluadas, y usa la mirada para elegir qué componentes quitar.
- Con 11 a 16 canales, 3 componentes son entre el 19 % y el 27 % de las dimensiones y arrastran actividad frontal no ocular. L1 no prueba que todo lo quitado fuera ocular; el control acota esa objeción pero no la elimina.
- El control no es un placebo: quita mucha más varianza (mediana 72 % frente a 3,5 %). Eso hace más fuerte el resultado de L2.
- La calidad de la limpieza se mide en los mismos datos con que se eligieron los componentes; las correlaciones "después" son optimistas.
- En cinco personas (P9, P18, P26, P35, P40) las saturaciones atenúan el puntaje ocular. En P39 y P23 un canal frontal está plano parte de la sesión y la limpieza es ineficaz en muchas ventanas.
- El modelo completo incluye variables que la limpieza no altera (fracción de canal plano, saturado o utilizable, e indicadores de dato faltante). Parte de L3 puede venir de ahí. Los subconjuntos de alfa y beta no tienen ese problema.
- La frase del protocolo "solo puede restar información ligada a la mirada" es demasiado fuerte; quitar componentes también podría subir la AUC.
- Las ventanas de EEG conservan el desfase de 0,25–0,5 s respecto de la mirada.
- La caída por persona no se relaciona con la calidad de la identificación ocular (Spearman +0,12 con el puntaje del primer componente); se asocia con la AUC de partida (+0,55). P9 va en contra: la limpieza le sube la AUC de 0,569 a 0,680.
- La enmienda describe a las cinco personas de identificación débil como "puntaje de 0,14 o menos"; el corte real es bajo 0,15.
- Control con etiquetas barajadas (una partición): −0,011 [−0,023; +0,001] respecto de 0,5.

## Auditorías

- Código, por un agente independiente con los modelos en marcha y sin leer predicciones: sin hallazgos bloqueantes. Verificó con una prueba sintética que limpiar la ventana cruda equivale a quitar los componentes de la señal filtrada, y que particiones, filas, pesos y configuración son los del 22-11. Sus advertencias están en la enmienda v2 y en la sección de límites.
- Resultados, por otro agente independiente con código propio: pasa los cuatro puntos (cifras reproducidas, integridad, registro y robustez). Sus advertencias están incorporadas arriba. Detalle en `AUDITORIA_RESULTADOS.md`.

Archivos: `confirmatorio.csv`, `descriptivos.csv`, `auc_por_persona.csv`, `calidad_limpieza.csv`, `personas_limpieza.csv`, `filtros/` (filtro espacial de cada persona), `pred_*.csv.gz`. Las variables recalculadas quedan fuera de Git (`datos/locales/v2_2025/limpieza_ocular_variables/`, hashes en `limpieza.json`) y se regeneran con la fase `clean`.
