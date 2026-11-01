# Grid atención binaria PCA — ronda ensamble ampliado

Etiquetas y personas fijas del profesor PCA reconstruido. ROC-AUC principal = promedio por persona de predicciones OOF. Selección de parámetros solo en el holdout interno agrupado (16 personas ajuste, 4 selección); cada fold externo evalúa cinco personas distintas.

| Estrategia | AUC macro | IC descriptivo 95 % | ΔAUC frente a 0,6464 | IC de Δ |
|---|---:|---:|---:|---:|
| Sin calibración personal | 0.6515 | [0.6349; 0.6685] | +0.0051 | [-0.0027; +0.0124] |
| Calibración personal offline | 0.6515 | [0.6349; 0.6680] | +0.0051 | [-0.0072; +0.0158] |
| Selección interna (puede usar offline) | 0.6509 | [0.6341; 0.6679] | +0.0045 | [-0.0036; +0.0119] |

La estrategia inductiva ajusta imputación y escalado únicamente con personas de entrenamiento. La estrategia relativo_offline calcula media y desviación de EEG/GSR usando la sesión completa no etiquetada de cada persona, también de evaluación. Es adaptación transductiva offline; no representa un detector online ni una comparación idéntica de preprocesamiento con la referencia. La fila selección interna escoge entre ambas estrategias usando solo score interno.

Entradas: solo EEG/GSR y sus transformaciones logarítmicas y resúmenes temporales. Se excluyen mirada, pupila, scores, etiquetas, identidad y tiempo de sesión como predictores. Los scores docentes siguen siendo relativos y offline. Historial reiniciado en cambios de segmento/huecos. Las configuraciones completas constan en protocolo.json y selecciones.csv.

Búsqueda adaptativa sobre train reutilizado: intervalos descriptivos por bootstrap de personas, sin corrección por búsqueda acumulada ni parada al alcanzar una meta. Test/validation/P29 sin evaluar. AUC mayor que 0,70 aquí, si ocurre, no equivale a generalización confirmada. No se cambia la definición de etiqueta ni la métrica para alcanzar la meta.

![Curvas ROC](curvas_roc.png)

[Predicciones](predicciones_oof.csv.gz) · [Selecciones](selecciones.csv) · [Protocolo](protocolo.json)

Ensamble de las seis corridas indicadas en protocolo_previo.json; para cada fold/escenario se probaron las 41 mezclas uniformes de 1/2/3 miembros sobre las personas internas. No se entrenan modelos adicionales y no se incorporan las entradas futuras del contraste retrospectivo. Los scores de regresores destilados llevan sigmoid sin calibración probabilística.
