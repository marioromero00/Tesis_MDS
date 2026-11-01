# Profesor binario reconstruido: igualitario

1 = atento (score > mediana personal); 0 = no atento (score <= mediana); ausentes = NA

Reconstruido desde caracteristicas_multimodales.csv. No se leen etiquetas ni scores antiguos. EEG/GSR predicen etiquetas de mirada/pupila; el profesor PCA se ajusta solo con personas del train de cada fold. Normalización y mediana por persona usan la sesión completa: etiquetado retrospectivo offline, no inferencia online de atención absoluta.

Cinco folds originales por participante, dos semillas en redes, ocho épocas fijas. Validación, test y P29 sin evaluar. Resultados exploratorios. El historial puede usar solo entradas pasadas hasta la ventana actual; la referencia docente offline no es causal.

| Modelo | Entrada | AUC macro | IC descriptivo 95 % |
|---|---|---:|---:|
| TCN | history | 0.6127 | [0.5894, 0.6353] |
| TCN | repeat_current | 0.6048 | [0.5785, 0.6303] |
| LSTM | history | 0.6026 | [0.5780, 0.6271] |
| LSTM | repeat_current | 0.5932 | [0.5691, 0.6176] |
| Logistica | history | 0.5790 | [0.5591, 0.5981] |
| RandomForest | history | 0.5778 | [0.5555, 0.6000] |
| MLP_current | current | 0.5645 | [0.5361, 0.5934] |
| Logistica | current | 0.5633 | [0.5363, 0.5892] |
| RandomForest | current | 0.5569 | [0.5354, 0.5782] |
| Dummy | current | 0.5000 | [0.5000, 0.5000] |

AUC: promedio por persona tras promediar semillas. Intervalos por bootstrap de 25 personas, sin corrección por búsqueda previa. Los datasets exportados usan profesor full-train; las etiquetas OOF de PCA pueden diferir porque el profesor se reajusta dentro de cada fold. Las predicciones OOF siempre usan las etiquetas de su profesor de fold. No se ha validado la interpretación psicológica atento/no atento.

![ROC](curvas_roc.png)

![AUC](comparacion_auc.png)