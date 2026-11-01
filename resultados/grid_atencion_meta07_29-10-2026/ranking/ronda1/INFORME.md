# Ranking por participante — ronda 1

Etiquetas y personas fijas del profesor PCA reconstruido. ROC-AUC principal = promedio por persona de predicciones OOF. Selección de parámetros solo en el holdout interno agrupado (16 personas ajuste, 4 selección); cada fold externo evalúa cinco personas distintas.

| Estrategia | AUC macro | IC descriptivo 95 % | ΔAUC frente a 0,6464 | IC de Δ |
|---|---:|---:|---:|---:|
| Sin calibración personal | 0.6405 | [0.6238; 0.6570] | -0.0059 | [-0.0154; +0.0042] |
| Calibración personal offline | 0.6445 | [0.6285; 0.6599] | -0.0019 | [-0.0147; +0.0097] |
| Selección interna (puede usar offline) | 0.6384 | [0.6223; 0.6544] | -0.0080 | [-0.0185; +0.0018] |

CatBoostRanker aprende pares positivo/negativo dentro de cada persona con PairLogit y máximo 1.000 pares por grupo. El identificador define los pares solo durante entrenamiento y no es una entrada del modelo. Se compensan grupos con menos de 1.000 pares posibles. La sigmoid del margen exportado no es una probabilidad calibrada. Las etiquetas y folds externos permanecen idénticos. La estrategia inductiva ajusta imputación y escalado únicamente con personas de entrenamiento. La estrategia relativo_offline calcula media y desviación de EEG/GSR usando la sesión completa no etiquetada de cada persona, también de evaluación. Es adaptación transductiva offline; no representa un detector online ni una comparación idéntica de preprocesamiento con la referencia. La fila selección interna escoge entre ambas estrategias usando solo score interno.

Entradas: solo EEG/GSR y sus transformaciones logarítmicas y resúmenes temporales. Se excluyen mirada, pupila, scores, etiquetas, identidad y tiempo de sesión como predictores. Los scores docentes siguen siendo relativos y offline. Historial reiniciado en cambios de segmento/huecos. Las configuraciones completas constan en protocolo.json y selecciones.csv.

Búsqueda adaptativa sobre train reutilizado: intervalos descriptivos por bootstrap de personas, sin corrección por búsqueda acumulada ni parada al alcanzar una meta. Test/validation/P29 sin evaluar. AUC mayor que 0,70 aquí, si ocurre, no equivale a generalización confirmada. No se cambia la definición de etiqueta ni la métrica para alcanzar la meta.

![Curvas ROC](curvas_roc.png)

[Predicciones](predicciones_oof.csv.gz) · [Selecciones](selecciones.csv) · [Protocolo](protocolo.json)