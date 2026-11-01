# Grid atención binaria PCA — ronda 1+2

Etiquetas y personas fijas del profesor PCA reconstruido. ROC-AUC principal = promedio por persona de predicciones OOF. Selección de parámetros solo en el holdout interno agrupado (16 personas ajuste, 4 selección); cada fold externo evalúa cinco personas distintas.

| Estrategia | AUC macro | IC descriptivo 95 % | ΔAUC frente a 0,6464 | IC de Δ |
|---|---:|---:|---:|---:|
| Sin calibración personal | 0.6452 | [0.6272; 0.6642] | -0.0012 | [-0.0107; +0.0076] |
| Calibración personal offline | 0.6549 | [0.6375; 0.6720] | +0.0085 | [-0.0034; +0.0192] |
| Selección interna (puede usar offline) | 0.6491 | [0.6293; 0.6681] | +0.0027 | [-0.0058; +0.0106] |

La estrategia inductiva ajusta imputación y escalado únicamente con personas de entrenamiento. La estrategia relativo_offline calcula media y desviación de EEG/GSR usando la sesión completa no etiquetada de cada persona, también de evaluación. Es adaptación transductiva offline; no representa un detector online ni una comparación idéntica de preprocesamiento con la referencia. La fila selección interna escoge entre ambas estrategias usando solo score interno.

Entradas: solo EEG/GSR y sus transformaciones logarítmicas y resúmenes temporales. Se excluyen mirada, pupila, scores, etiquetas, identidad y tiempo de sesión como predictores. Los scores docentes siguen siendo relativos y offline. Historial reiniciado en cambios de segmento/huecos. Las configuraciones completas constan en protocolo.json y selecciones.csv.

Búsqueda adaptativa sobre train reutilizado: intervalos descriptivos por bootstrap de personas, sin corrección por búsqueda acumulada ni parada al alcanzar una meta. Test/validation/P29 sin evaluar. AUC mayor que 0,70 aquí, si ocurre, no equivale a generalización confirmada. No se cambia la definición de etiqueta ni la métrica para alcanzar la meta.

![Curvas ROC](curvas_roc.png)

[Predicciones](predicciones_oof.csv.gz) · [Selecciones](selecciones.csv) · [Protocolo](protocolo.json)

Esta corrida combina predicciones de los grids de boosting y CatBoost. Para cada fold/escenario se probaron pesos 0/0,25/0,5/0,75/1 usando solamente las cuatro personas internas. No hay modelos adicionales entrenados; se reutilizan los modelos externos auditados de ambas rondas. Ver selecciones.json y protocolo_previo.json.
