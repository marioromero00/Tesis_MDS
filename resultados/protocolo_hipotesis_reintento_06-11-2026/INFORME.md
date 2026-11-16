# Protocolo prospectivo para contrastar la hipótesis

Estado: propuesta concreta y reproducible; no es un preregistro retrospectivo ni una nueva confirmación. Margen candidato +0,02 AUC, sin justificación sustantiva independiente todavía. No se modificó el manuscrito original.

## El modelo cercano a 0,67
El candidato localizado es CatBoost estático de atención: AUC test 0,6744 y validación 0,6798. No es el modelo de activación. La comparación histórica de temporalidad con familia emparejada fue HistBoost 0,687901 frente a HistBoost estático 0,660179; no se debe atribuir toda la diferencia frente al CatBoost a temporalidad. La identificación del modelo mencionado por Mario es provisional.

## Afirmación y regla de decisión
Para modelos previamente fijados y personas nuevas de la misma población, definir D por persona = AUC temporal menos AUC estático. Evaluar media de D por tarea. Propuesta de relevancia práctica: ambas medias superan +0,02. La hipótesis original dice mejor (>0): no se puede rechazar esa superioridad original solamente porque se descarta una mejora de +0,02. Reportar también la relación del intervalo con cero.
Intervalos t bilaterales de 97,5% por tarea, con cobertura simultánea de al menos 95% por Bonferroni. Respaldar la afirmación práctica si ambos límites inferiores superan el margen; refutarla para estos modelos si al menos un límite superior queda por debajo. Si los intervalos cruzan el margen, mantener indeterminación. Esta regla no prueba equivalencia (que exigiría un intervalo contenido en una banda bilateral) ni descarta toda arquitectura temporal.

## Evaluación propuesta
1. Fijar contexto principal hasta 32 ventanas; 8 queda secundario sin sustituir al principal según resultados. Para atención usar la pareja HistBoost inductiva emparejada de temporalidad_eeg_v2_test_29-10-2026; para activación usar final_ctx1 y final_ctx32 del recálculo GSR V2. Conservar pesos y parámetros, y no entrenar con la cohorte nueva.
2. Conservar el profesor PCA reconstruido de atención y el GSR V2 auditado; mismo etiquetado, entradas, ventanas por tarea y preprocesamiento ajustado en train para ambos modelos. Registrar versiones, hashes y modelos en el manifiesto adjunto. El objetivo queda explícitamente como pseudoetiqueta offline: la normalización personal del profesor usa la sesión completa. Esto requiere reconciliar la redacción del manuscrito que exige normalización solo en train; no presentar como inferencia psicológica online.
3. Reclutar participantes nuevos; los 41 existentes no cuentan como una nueva cohorte independiente. No reciclar exclusiones por mala señal ni P29 como reemplazo. No aumentar N contando ventanas, semillas o folds. Mantener protocolo de estímulos y adquisición comparable.
4. Definir elegibilidad antes de analizar: calidad y sincronización aprobadas, al menos 100 ventanas etiquetadas y 20 por clase en cada tarea, sin filtrar por AUC. Son umbrales operativos propuestos, no validados; una fase de factibilidad ciega a predicciones debe confirmar su viabilidad. Para cierre conjunto usar personas elegibles en ambas tareas; reportar exclusiones y su efecto sobre generalización.
5. Registrar N final y reglas antes de evaluar; sin consultas intermedias de AUC ni ampliación de muestra después de mirar el efecto. Se permite controlar reclutamiento/calidad sin resultados predictivos. Separar consentimiento y adquisición de cualquier análisis automático.
6. Calcular diferencias pareadas y los intervalos preespecificados una sola vez. Usar bootstrap de participantes como sensibilidad, sin elegir el método que favorezca el resultado. Documentar historial efectivo y no afirmar secuencias completas de 32 si no están disponibles.

## Tamaño de muestra por escenarios
Se usa la desviación de diferencias individuales, no la desviación de ventanas. Para activación se toma la mayor desviación entre OOF train, validación y test; OOF comparte modelos y solo sirve como estimación piloto aproximada. Atención dispone aquí de ocho personas de test histórico. Estas varianzas son inciertas y la diferencia entre protocolos puede cambiar la dispersión. Se incluye inflación 1,5 como sensibilidad, no como cota de confianza.
Cálculo mediante t no central: potencia 90% por resultado, umbral unilateral 0,0125 consistente con los intervalos simultáneos. Si ambos efectos verdaderos están a la distancia planeada sobre el margen, la potencia conjunta es al menos 80% por la cota de unión, sin suponer independencia entre tareas. No es potencia observada ni garantía de precisión real.
Ejemplo: margen 0,02; efecto verdadero 0,04 para respaldar o 0,00 para refutar. Ambos están a distancia 0,02 del límite. Si el efecto verdadero es 0,02, ningún tamaño finito garantiza una decisión; un efecto de 0,03 está a distancia 0,01 y exige mucho más N.

| Tarea | Inflación SD | Personas evaluables nuevas | Reclutar con 20% pérdidas |
|---|---:|---:|---:|
| activacion | 1.0 | 767 | 959 |
| activacion | 1.5 | 1723 | 2154 |
| atencion | 1.0 | 62 | 78 |
| atencion | 1.5 | 135 | 169 |

Para el estudio conjunto se toma el mayor N de ambas tareas, no se suman si las mismas personas aportan ambos resultados. El 20% es un supuesto de planificación; no proviene de una tasa observada. No hay compromiso de recolectar estos datos.

## Decisiones pendientes y alcance
El margen 0,02 necesita una justificación de relevancia independiente (uso, reproducibilidad del instrumento o criterio académico); no se convierte en válido porque produzca un N conveniente. Los escenarios 0,01/0,02/0,03 están en escenarios_muestra.csv. Falta confirmar factibilidad de nueva cohorte, elegibilidad y alcance de activación con el profesor. Sin nueva cohorte, este diseño queda preparado pero no ejecutado; repetir el test existente no lo vuelve confirmatorio.
Este protocolo evalúa agregación de historial (media/desviación), no sensibilidad al orden, ni fusión intermedia/tardía. Por tanto, su cierre se limita a la proposición operacionalizada y no cubre todos los mecanismos descritos por la hipótesis general de la tesis.

Método: [potencia de pruebas pareadas, documentación de R](https://www.stat.math.ethz.ch/R-manual/R-patched/RHOME/library/stats/html/power.t.test.html) y [intervalos t, NIST](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm). Ejecución: `.venv/bin/python scripts/planificar_contraste_hipotesis.py`.


## Cierre del reintento — 6 de noviembre de 2026

Los cálculos se reprodujeron y se contrastaron mediante 100.000 simulaciones por escenario de varianza bajo el supuesto normal del diseño. Los cuatro modelos seleccionados conservan sus hashes. No se adquirieron participantes ni se ejecutó una evaluación confirmatoria nueva.

El N de activación es muy sensible a la fuente de dispersión: 72 con la varianza de validación, 101 con la de test y 767 con la de OOF train. No son límites de un intervalo ni opciones para escoger por conveniencia. OOF mezcla modelos entrenados en distintos folds, mientras que la cohorte futura evalúa un par fijo; por tanto, 767 debe tratarse como escenario conservador de sensibilidad, no como requerimiento de reclutamiento demostrado. Las estimaciones externas se basan en solo ocho personas cada una. El diseño final necesita una estimación de variabilidad más defendible y factibilidad de adquisición antes de fijar N.

La referencia al AUC 0,67 corresponde provisionalmente al CatBoost de atención con 0,6744 en test. Su buen desempeño relativo al azar y la superioridad de un modelo temporal son afirmaciones distintas. El resultado de atención no desapareció al corregir GSR: el recálculo de activación trabaja sobre otra variable objetivo y otras entradas. Esta revisión verifica la procedencia de las métricas, no constituye una nueva auditoría completa del profesor de atención.

El margen práctico 0,02 sigue siendo una propuesta, no un umbral aprobado ni deducido de los resultados. Rechazar una mejora de al menos ese tamaño no equivale a rechazar cualquier mejora positiva. Si se mantiene la hipótesis original de superioridad >0, la frontera debe ser 0 y la potencia se calcula para un efecto verdadero separado de 0, sin cambiarla después de observar el test.
