# Avance - 22-08-2026 (Pipeline multimodal reproducible)

## Resultado

Se implementó, probó y ejecutó con los datos reales el pipeline secuencial de
EEG, GSR, pupilometría y eye tracking. El código oficial está versionado en el
repositorio `Tesis_MDS`; el protocolo completo está en
`documentacion/PREPROCESAMIENTO_MULTIMODAL.md` del repo.

El flujo ejecutado fue:

```text
validación y hashes → sincronización → EDA → ventanas Tobii
→ EEG sobre límites UTC comunes → calidad → auditoría y manifiesto
```

## Resultados verificados

| Resultado | Valor |
|---|---:|
| Participantes | 48 |
| Ventanas de 2 s, salto 1 s | 25.992 |
| Ventanas multimodales válidas | 22.201 |
| Ventanas GSR válidas | 24.541 |
| Ventanas pupila válidas | 25.964 |
| Ventanas mirada válidas | 25.887 |
| Ventanas EEG con cobertura válida | 25.958 |
| Emparejamiento candidato | 25.510 |
| Ventanas P29 con offset por revisar | 482 |

La tabla final contiene 59 columnas y queda en
`resultados/preprocesamiento/caracteristicas_multimodales.csv`. La auditoría por
participante, configuración efectiva y hashes están en la misma carpeta.

## Correcciones descubiertas

- El inventario EEG elegía el primer TXT de una sesión. P48 tenía un fragmento
  de 13 s y una adquisición principal de 846 s. Ahora se selecciona el TXT más
  largo de cada sesión.
- La misma corrección reveló que P25 tiene 36,05 % de repetición plana en su
  registro principal. El resultado EEG correcto es 44/48 utilizables; quedan
  marcados P1, P14, P17 y P25.
- P7 y P42 no tienen GSR, por lo que no producen ventanas completas de cuatro
  modalidades.
- P29 conserva el estado `revisar_offset`; no se ocultó ni se aprobó
  automáticamente.

## Reproducibilidad

La ejecución completa se reproduce desde la raíz de `Tesis_MDS` con:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python .\scripts\ejecutar_todo.py
```

El pipeline guarda SHA-256 de ambos originales, del manifiesto de
sincronización, de las salidas y de la configuración, además de versiones de
Python, NumPy, pandas y SciPy. Los originales no se modifican ni se suben a Git.

## Próximo hito

La ingeniería de datos queda cerrada para una primera iteración. El siguiente
paso es resolver las etiquetas objetivo sin circularidad, congelar una división
por participante y entrenar baselines estáticos antes de los modelos temporales.

## Notas relacionadas

- [[Tesis_MDS]]
- [[Avance - 22-08-2026 (Preprocesamiento GSR Pupila y Eye Tracking)]] — diseño previo, reemplazado por esta ejecución real.
- [[Resumen Diseño Etiquetas y Modelos]]
- [[Modelo Profesor - Decisiones]]
