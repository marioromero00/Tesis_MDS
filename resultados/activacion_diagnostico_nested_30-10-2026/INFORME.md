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

## Interpretación

La búsqueda propia de activación no establece una ventaja temporal: contexto8 ΔAUC −0,0024, IC [−0,0273; 0,0249]; contexto32 ΔAUC +0,0035, IC [−0,0292; 0,0359]. Las tres AUC están cerca de 0,54 y sus intervalos descriptivos incluyen 0,50. Estos resultados son OOF de train; no se comparan como una mejora directa con el test de la corrida anterior.

La selección usó 60 ajustes internos y 15 modelos externos. Una comprobación adicional recalculó 75 AUC por persona desde disco, cotejó todas las etiquetas con las originales y verificó las 15 selecciones contra sus cuatro candidatos internos.

La prioridad es la calidad del profesor: P4 tiene GSR válido en solo 12,6 % de sus ventanas pese a recibir etiquetas en todas; los empates de P34 generan apenas 8,6 % de positivos. El contexto32 está completo en solo 0,95 % de las ventanas, promediando personas. Estos hallazgos requieren un protocolo de calidad de señales fijado independientemente del rendimiento. No se eliminaron participantes ni se modificaron etiquetas en esta corrida.

[Diagnóstico detallado](DIAGNOSTICO.md). No se evaluaron validation ni test. La búsqueda es exploratoria debido a la reutilización histórica de train.
