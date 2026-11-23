# Comprobación empírica del montaje EEG y de la sincronía con el seguidor ocular — 23-11-2026

Script `scripts/montaje_ocular_41p.py` (caché de crudos con `scripts/cache_crudos_ocular.py`). Descriptivo: no usa etiquetas ni modelos. Responde al pendiente del 22-11: el montaje de los electrodos no estaba documentado y la comparación frontal/posterior se hizo con el montaje por defecto del equipo.

**Método.** Por persona se compara el EEG crudo (1–15 Hz) con tres señales del seguidor ocular llevadas al reloj del EEG: mirada horizontal, mirada vertical y parpadeos (tramos de 50 a 500 ms con ambos ojos no válidos). Por canal se mide la correlación con cada señal y la amplitud del EEG promediado alrededor de los parpadeos.

## Resultado 1: los datos son compatibles con el montaje por defecto

Montaje por defecto de OpenBCI Cyton+Daisy: 0 Fp1, 1 Fp2, 2 C3, 3 C4, 4 P7, 5 P8, 6 O1, 7 O2, 8 F7, 9 F8, 10 F3, 11 F4, 12 T7, 13 T8, 14 P3, 15 P4.

Amplitud del parpadeo (pico a pico del promedio, mediana entre personas):

| Zona según montaje por defecto | Canales | Amplitud |
|---|---|---|
| Frontopolar (Fp1, Fp2) | 0, 1 | 148 y 151 µV |
| Frontal lateral (F7, F8) | 8, 9 | 74 y 77 µV |
| Frontal (F3, F4) | 10, 11 | 57 y 56 µV |
| Central y temporal (C3, C4, T7, T8) | 2, 3, 12, 13 | 25 a 29 µV |
| Parietal y occipital (P7, P8, O1, O2, P3, P4) | 4–7, 14, 15 | 18 a 24 µV |

- El gradiente es el esperado para un parpadeo: máximo sobre los ojos y decreciente hacia atrás, simétrico entre izquierda y derecha.
- En 27 de 41 personas el canal con mayor respuesta al parpadeo es el 0 o el 1.
- La mirada horizontal entra con signo opuesto en los canales 8 y 9 (F7 y F8) en 31 de las 37 personas con ambos canales utilizables, como corresponde a dos electrodos a cada lado de los ojos. Los canales con mayor acoplamiento horizontal son 9, 13, 5 y 3, todos del lado derecho según el montaje por defecto.

**Lectura.** No reemplaza la documentación del experimento, pero el patrón espacial de los artefactos oculares coincide con el montaje por defecto y no con una asignación arbitraria de canales. La división frontal/posterior usada el 22-11 queda respaldada por los datos.

## Resultado 2: el EEG va desfasado respecto del seguidor ocular

- El desfase que maximiza el acoplamiento es positivo en las 41 personas: el EEG va entre 0,18 y 0,53 s atrasado respecto del reloj del seguidor ocular (mediana 0,45 s; cuartiles 0,28 y 0,48 s).
- Las tres señales de referencia dan el mismo desfase en casi todas las personas, lo que indica una diferencia de relojes y no un efecto fisiológico.
- Hay dos grupos: cerca de 0,27 s (personas P2 a P21, P36, P37) y cerca de 0,47 s (el resto).

**Consecuencia.** Las ventanas de 2 s del EEG están corridas entre un 12 % y un 25 % respecto de las ventanas con que se calcularon la mirada, la pupila y el GSR. No invalida los resultados, pero atenúa cualquier relación entre el EEG y las otras señales, incluidas las etiquetas. No se corrigió: las ventanas vigentes se mantienen congeladas.

## Calidad

- Canales utilizables por persona: entre 11 y 16 (mediana 15). Los canales con más pérdidas son P4, O1, P7 y P3.
- Frecuencia de muestreo efectiva 125,1 Hz; el mayor hueco entre muestras es de 0,19 s.
- Parpadeos detectados por persona: entre 19 y 393.

## Límites

- El acoplamiento se mide con correlaciones lineales en 1–15 Hz; es bajo en algunas personas (correlación máxima cercana a 0,1), donde el desfase estimado es menos seguro.
- "Parpadeo" se define por pérdida breve de ambos ojos en el seguidor ocular; incluye pérdidas de seguimiento que no son parpadeos.
- La compatibilidad con el montaje por defecto no distingue entre electrodos vecinos (por ejemplo F3 frente a F7); sí distingue zonas.

Archivos: `resumen_canales.csv`, `canales_por_persona.csv`, `personas.csv`, `comprobaciones.json`.
