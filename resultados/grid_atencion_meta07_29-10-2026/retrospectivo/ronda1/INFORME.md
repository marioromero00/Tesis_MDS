# Clasificación retrospectiva offline de atención — ronda 1

Etiquetas y personas fijas del profesor PCA reconstruido. ROC-AUC principal = promedio por persona de predicciones OOF. Selección de parámetros solo en el holdout interno agrupado (16 personas ajuste, 4 selección); cada fold externo evalúa cinco personas distintas.

| Estrategia | AUC macro | IC descriptivo 95 % | ΔAUC frente a 0,6464 | IC de Δ |
|---|---:|---:|---:|---:|
| Retrospectivo sin calibración | 0.6485 | [0.6283; 0.6693] | +0.0021 | [-0.0080; +0.0118] |
| Retrospectivo con z personal | 0.6590 | [0.6412; 0.6782] | +0.0126 | [+0.0001; +0.0241] |
| Selección interna (puede usar offline) | 0.6520 | [0.6324; 0.6729] | +0.0056 | [-0.0042; +0.0153] |

Este contraste utiliza explícitamente hasta 4/8/16 ventanas posteriores EEG/GSR dentro del mismo segmento y persona. No usa etiquetas futuras como entradas, pero requiere señales posteriores y no es detección online ni una mejora demostrada del escenario causal. La estrategia inductiva ajusta imputación y escalado únicamente con personas de entrenamiento. La estrategia relativo_offline calcula media y desviación de EEG/GSR usando la sesión completa no etiquetada de cada persona, también de evaluación. Es adaptación transductiva offline; no representa un detector online ni una comparación idéntica de preprocesamiento con la referencia. La fila selección interna escoge entre ambas estrategias usando solo score interno.

Entradas: solo EEG/GSR y sus transformaciones logarítmicas y resúmenes temporales. Se excluyen mirada, pupila, scores, etiquetas, identidad y tiempo de sesión como predictores. Los scores docentes siguen siendo relativos y offline. Historial reiniciado en cambios de segmento/huecos. Las configuraciones completas constan en protocolo.json y selecciones.csv.

Búsqueda adaptativa sobre train reutilizado: intervalos descriptivos por bootstrap de personas, sin corrección por búsqueda acumulada ni parada al alcanzar una meta. Test/validation/P29 sin evaluar. AUC mayor que 0,70 aquí, si ocurre, no equivale a generalización confirmada. No se cambia la definición de etiqueta ni la métrica para alcanzar la meta.

![Curvas ROC](curvas_roc.png)

[Predicciones](predicciones_oof.csv.gz) · [Selecciones](selecciones.csv) · [Protocolo](protocolo.json)