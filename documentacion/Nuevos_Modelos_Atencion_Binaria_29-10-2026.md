# Nueva búsqueda de modelos para atención binaria — 29-10-2026

Se conservan los dos profesores reconstruidos y sus etiquetas binarias offline, la población de train, los cinco folds de personas y las entradas EEG/GSR. La corrida compara LDA con shrinkage, QDA regularizado, Extra Trees, HistGradientBoosting y SVM con aproximación RBF Nyström, cada uno con ventana actual e historial de hasta ocho ventanas.

Se fijaron dos configuraciones por familia antes de entrenar. Dentro de cada fold, 16 personas ajustan candidatos y cuatro personas eligen parámetros por ROC-AUC macro; las cinco personas externas solo se usan después de seleccionar. El PCA docente se reajusta con las 16 personas del nivel interno para no emplear las cuatro personas de selección en su ajuste. La evaluación externa utiliza exactamente las etiquetas del profesor del fold anterior.

Se guardan 200 modelos internos y 100 modelos externos. Además, una estrategia elige familia, representación y parámetros por el score interno y reutiliza sus predicciones externas: no elige el ganador mirando AUC externa. La búsqueda interna es un holdout agrupado, no una validación cruzada interna completa; sus elecciones pueden ser inestables.

Referencias anteriores fijadas antes de ejecutar: TCN con historial para igualitario (AUC 0,6127), TCN control de ventana actual para PCA (AUC 0,6254). Se calculan diferencias pareadas por participante e intervalos descriptivos. No se evalúan validation, test ni P29. Se conserva el carácter exploratorio de rondas adaptativas sobre train; no se presenta el máximo observado como confirmación independiente.

LDA/QDA usan priors iguales. Los demás usan balanceo por participante/clase. Nyström se ajusta solo en el train correspondiente y entrega 128 componentes a LinearSVC. Sus predicciones guardadas como `score` son márgenes, sin calibración probabilística. Boosting tiene 200 iteraciones fijas y early stopping automático desactivado, evitando particiones aleatorias por ventana.

Las versiones del entorno se conservan en `requirements_atencion_binaria_macos.lock.txt` y el protocolo de la corrida. No se modifican resultados anteriores.

```sh
.venv/bin/python -m unittest discover -s tests -p test_nuevos_modelos_atencion_binaria.py -v
.venv/bin/python scripts/nuevos_modelos_atencion_binaria.py
.venv/bin/python scripts/auditar_nuevos_modelos_atencion_binaria.py
```

[Informe, curvas y métricas](../resultados/nuevos_modelos_atencion_binaria_29-10-2026/INFORME.md).
