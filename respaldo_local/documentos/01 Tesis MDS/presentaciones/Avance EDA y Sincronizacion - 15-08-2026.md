# Avance EDA y Sincronizacion — 15-08-2026

Fuente histórica de contenido para la presentación HTML homónima.

> Actualización 06-09-2026: el HTML fue ampliado a 16 diapositivas con los resultados baseline.
> La fuente vigente es [[Avance - 06-09-2026 (Presentacion Resultados Baselines)]].
> El contenido de esta nota conserva el estado del 15-08-2026.

## 1. Portada

**De datos crudos a señales coordinadas**  
Avances en sincronización y EDA multimodal.

## 2. Qué se construyó

Un pipeline reproducible y conservador que inventaría, coordina y evalúa EEG, GSR, pupilometría y eye tracking sin modificar los archivos originales.

## 3. Sincronización

- 47 candidatos directos EEG–Tobii.
- P29 requiere revisión por offset.
- `Test_Participant` no tiene pareja directa.
- Las modalidades se recortan mediante límites UTC comunes y conservan sus frecuencias nativas.
- No se estimó drift artificialmente porque no existen triggers compartidos.

## 4. Panorama multimodal

- EEG: 45/48 sesiones principales utilizables (93,75 %).
- GSR: 47/49 grabaciones disponibles (95,92 %).
- Pupilometría: 90,25 % de muestras con ambos ojos válidos.
- Eye tracking: 94,98 % de muestras de mirada válidas.

## 5. EEG

- 104 sesiones inventariadas; resumen final sobre 48 sesiones principales.
- Frecuencia efectiva estable alrededor de 125 Hz.
- P1, P14 y P17 quedan excluidos con el umbral exploratorio de 30 %.
- El umbral es permisivo y no reemplaza la inspección visual.

## 6. GSR

- 2.984.636 filas procesadas por streaming.
- 530.407 muestras válidas en 47 grabaciones.
- Frecuencia efectiva cercana a 15 Hz.
- P7 y P42 no contienen GSR.

## 7. Pupilometría y eye tracking

- 2.187.110 muestras oculares evaluadas.
- 1.973.941 muestras con ambos ojos válidos (90,25 %).
- 2.077.373 muestras de mirada válidas (94,98 %).
- 122.302 fijaciones únicas; mediana de duración de 183 ms.

## 8. Límites y decisiones

- Sin triggers compartidos solo puede defenderse alineación por reloj absoluto, no sincronización submuestra.
- Las filas no marcadas como `candidato` requieren revisión manual.
- La calidad global no reemplaza criterios por participante, sesión y canal.
- Las señales deben conservar sus frecuencias nativas al recortar epochs comunes.

## 9. Próximos pasos

1. Aprobar el manifiesto de sincronización.
2. Fijar criterios finales de calidad.
3. Recortar ventanas comunes por evento.
4. Preprocesar cada modalidad.
5. Implementar las etiquetas y entrenar los primeros baselines.

## Fuentes

- [[RESUMEN_PROCESO|Resumen del procesamiento]]
- [[SINCRONIZACION_SENALES|Sincronización]]
- [[EDA_SENALES|EDA multimodal]]
- [[GRAFICOS_TESIS|Gráficos]]
