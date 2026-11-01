# Avance - 22-08-2026 (Preprocesamiento GSR, Pupila y Eye Tracking)

> [!warning] Estado histórico
> Esta nota describe el diseño previo probado con datos sintéticos. La implementación real,
> la integración EEG y los resultados finales están en
> [[Avance - 22-08-2026 (Pipeline Multimodal Reproducible)]].

Corresponde al paso 1 de los próximos pasos de [[Tesis_MDS]]: preprocesar las tres señales del
Tobii, que era lo único del pipeline sin especificar (el EEG ya lo estaba).

**El código vive fuera del vault**, en `~/Tesis_MDS/preprocesamiento/`. Acá queda el
razonamiento y lo que se decidió.

## Qué se construyó

Un módulo que lleva GSR, pupilometría y eye tracking desde el export crudo del Tobii hasta una
tabla de features en **ventanas de 2 s con 50 % de solapamiento**, el mismo soporte que ya tienen
las épocas del EEG. Ocho archivos: resolución de columnas, ingesta, grilla de ventanas, un módulo
por señal, runner de línea de comandos y una prueba de extremo a extremo.

Continúa el diseño de `Sincronizacion_señales.ipynb` (secciones 1.2 y 3.1 a 3.5) y agrega **la
pieza que faltaba: la extracción de features por ventana**. Sin ella las señales quedaban limpias
pero no comparables con el EEG, que es el requisito para que el Modelo Estudiante reciba las
cuatro modalidades sobre el mismo eje.

| Señal | Features | Correspondencia con el Cap. 4 |
|---|---|---|
| GSR | 10 por ventana + 4 sobre ventana de contexto | Número de picos SCR, amplitud de respuesta, nivel tónico SCL, variabilidad |
| Pupilometría | 8 | Diámetro, dilatación relativa a la línea base, validez |
| Eye tracking | 13 | Número y duración de fijaciones, amplitud y velocidad de sacadas, dispersión de la mirada |

## Verificación

**El pipeline todavía no toca los datos reales**: el export de Tobii está en Drive, no en el
equipo. Lo verificado es la mecánica, con `test_sintetico.py`: fabrica un export con picos SCR,
parpadeos, fijaciones y sacadas inyectados y comprueba que el pipeline los recupera. Pasan todas
las comprobaciones, incluida la duración media de fijación (300,0 ms sobre 300 inyectados) y el
invariante de la grilla (paso de 1 s exacto, ninguna ventana truncada).

## Decisiones tomadas

- **Una ventana nunca cruza el borde de un estímulo.** Mezclaría dos condiciones experimentales
  dentro de la misma etiqueta y la comparación dejaría de ser interpretable.
- **El eye tracking no se resamplea a la grilla de 60 Hz.** Sus unidades son eventos con duración
  propia; promediarlos sobre una grilla uniforme destruiría la información de conteo y duración
  que alimenta el Attention Score. GSR y pupila sí se resamplean.
- **Un evento se asigna a una ventana por su instante de inicio**, sin prorratear. Prorratear
  exigiría un criterio que no está en el diseño.
- **La descomposición tónico/fásica por defecto es un pasa-bajos Butterworth de 0,05 Hz**, no
  cvxEDA. El diseño previo prefiere cvxEDA por la restricción de no-negatividad de los impulsos
  sudomotores, pero `cvxopt` no está instalado. Queda como opción por bandera.
- **La pupilometría pasó a ser fuente propia**, separada del eye tracking, en línea con el cuadro
  de [[Resumen Diseño Etiquetas y Modelos]].

## Decisiones abiertas que este avance NO cerró

- **La ventana de agregación del GSR.** Sigue abierta. En vez de elegir, el módulo emite las
  features de SCR sobre los dos soportes: la ventana de 2 s alineada con el EEG y una ventana de
  contexto de 6 s que termina en el mismo instante. Así la decisión se puede cerrar **con
  evidencia** —cuál de las dos predice mejor— en vez de por argumento. Es el mismo punto que
  aparece en limitaciones del Cap. 1 por la latencia de SCR de 1 a 5 s.
- **La corrección por luminancia de la pupila.** `pupila.corregir_luminancia` está declarada y
  lanza `NotImplementedError` a propósito, para que nadie la rellene con una aproximación sin
  decidirlo. Requiere la luminancia de la página observada por instante, que exige conservar las
  capturas de los estímulos.

## Sobre la fuga de información

El z-score de GSR y pupila se estima sobre la sesión completa del participante. Con partición por
participante eso **no** filtra información entre entrenamiento y evaluación, porque un
participante entra entero a un lado o al otro. Sí es **no causal dentro de la sesión**, lo que es
consistente con el alcance declarado en el Cap. 1: modelos evaluados *offline*, sin sistema en
tiempo real. Si ese alcance cambiara, la normalización habría que rehacerla causal.

## Pendientes que esto deja

- [ ] **Bajar el export de Tobii desde Drive** y correr el pipeline sobre los 48 participantes.
- [ ] **Confirmar los nombres de columna del export real.** `columnas.py` declara candidatos por
  campo y falla con un mensaje explícito si falta uno obligatorio; los nombres provienen del
  diseño previo, no de haber abierto el archivo.
- [ ] Confirmar que el formato de fecha del export es `mm/dd/yyyy`.
- [ ] Cerrar la ventana del GSR comparando las dos variantes de features.
- [ ] Unir la tabla de features del Tobii con las épocas del EEG usando los manifiestos de
  sincronización. El módulo deja timestamps absolutos UTC pero **no hace la unión**: la corrección
  de deriva es una decisión aparte.

## Notas relacionadas

- [[Tesis_MDS]]
- [[Estructura Tesis]] — Cap. 4, Fuentes de Información y Preprocesamiento
- [[Resumen Diseño Etiquetas y Modelos]]
- [[Avance EDA y Sincronizacion - 15-08-2026]]
- [[Avance - 22-08-2026 (Frecuencia EEG y Limpieza de Expresion Facial)]]
