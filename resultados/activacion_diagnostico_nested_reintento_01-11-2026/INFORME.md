# Activación: diagnóstico y búsqueda anidada en train

Las etiquetas binarias y las modalidades EEG/Eye/Pupil se conservan. Cuatro configuraciones por contexto (1/8/32 ventanas), seleccionadas con personas internas disjuntas de las externas. AUC promediada por persona; intervalos descriptivos bootstrap. Búsqueda exploratoria sobre train reutilizado; no es una confirmación independiente.

## AUC OOF

| Contexto | AUC | IC 95 % |
|---|---:|---:|
| 1 | 0.5366 | [0.4997; 0.5773] |
| 8 | 0.5342 | [0.4873; 0.5869] |
| 32 | 0.5401 | [0.4897; 0.5958] |

## Temporal menos estático

| Contexto | ΔAUC | IC 95 % | Personas mejoran |
|---|---:|---:|---:|
| 8 | -0.0024 | [-0.0273; 0.0249] | 13/25 |
| 32 | +0.0035 | [-0.0292; 0.0359] | 14/25 |

Diagnóstico por persona: diagnostico_personas.csv; cobertura real del historial: cobertura_historial.csv. La concordancia 2s/6s es sensibilidad al suavizado del profesor; no valida activación psicológica. No se ajustaron offsets ni se eliminaron personas según rendimiento. Verificar cobertura y timestamps detecta problemas documentables, pero no prueba alineamiento fisiológico externo.

Repetición completa del 01-11-2026: predicciones, métricas, contrastes, selecciones y diagnóstico coinciden con la ejecución original, tolerancia 1e-10. Se entrenaron nuevamente los 60 ajustes internos y 15 modelos externos. [Diagnóstico](DIAGNOSTICO.md).

Conclusión: el reentrenamiento reprodujo las AUC y diferencias originales. Ningún contexto temporal supera concluyentemente al estático. Repetir con los mismos datos y semillas comprueba reproducibilidad, no añade evidencia independiente. Permanecen los problemas de calidad docente de P4 y empates de P34.
