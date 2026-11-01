# Atención binaria con y sin temporalidad — 29-10-2026

Nueva tarea exploratoria: `attention_binary = 1` si `attention_label_equal == alto`; `0` para medio o bajo. Los valores ausentes no se convierten a cero. Se conserva la etiqueta ternaria original. Esta definición distingue atención alta del resto; no equivale a una medición externa de estar atento/no estar atento.

## Diseño fijado antes de entrenar

- Solo los 25 participantes del train original, con los mismos cinco folds de atención del contraste de temporalidad de octubre. Validation, test y P29 no se evalúan.
- EEG y GSR como entradas. Mirada, pupila, etiquetas y scores de atención excluidos del modelo estudiante.
- Imputación y escalado ajustados dentro del fold de entrenamiento.
- Referencia Dummy, logística, Random Forest, MLP, TCN y LSTM. Logística y Random Forest comparan ventana actual frente a actual más resúmenes causales. TCN/LSTM comparan historial real frente a ventana actual repetida con igual longitud disponible.
- Hasta ocho ventanas consecutivas; reinicio por participante, registro, segmento, estímulo o hueco temporal. Ventanas de 2 s con avance 1 s: máximo 9 s de cobertura, sin entradas futuras respecto al final de la ventana actual.
- Dos semillas para redes y ocho épocas fijas, sin selección de hiperparámetros ni umbral con los folds externos. Configuración completa en protocolo.json.
- ROC-AUC principal: promedio por participante tras promediar probabilidades de semillas. Se informa además AUC agrupada, BA con umbral 0,5 y average precision agrupada. IC descriptivos y diferencias pareadas: 2.000 remuestreos de personas.

## Ejecutar o reanudar

Desde la raíz del repositorio, con el entorno creado:

```sh
.venv/bin/python scripts/atencion_binaria.py --positive high --output resultados/atencion_binaria_29-10-2026
```

Para un entorno nuevo de macOS Apple Silicon con Python 3.12, instalar `requirements_atencion_binaria_macos.lock.txt`. El archivo registra las versiones realmente usadas; conserva separados los requirements históricos del proyecto.

La reanudación valida protocolo, fuentes y hashes de artefactos. Cada modelo se recarga y sus predicciones se comparan antes de aceptar la tarea. El directorio de resultados contiene modelos, predicciones OOF, métricas, contrastes, curvas PNG/PDF/CSV y el informe final. No sobrescribir ejecuciones con otra definición binaria.

## Alcance

Es una comparación exploratoria en una muestra reutilizada. La AUC binaria no se compara directamente con la balanced accuracy ternaria. No convierte las pseudoetiquetas offline en una validación psicológica externa. El historial agregado cambia la representación y dimensionalidad en logística/RF; el control de arquitectura de TCN/LSTM permite un contraste adicional del aporte temporal. Los intervalos no corrigen la búsqueda acumulada anterior.

[Informe y resultados de la ejecución](../resultados/atencion_binaria_29-10-2026/INFORME.md).
