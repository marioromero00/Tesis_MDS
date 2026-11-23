# Auditoría independiente de resultados — red sobre EEG crudo — 23-11-2026

Hecha por un agente independiente con código propio, sin reutilizar `report()` y sin modificar el repositorio. Síntesis de su informe.

| Punto | Veredicto |
|---|---|
| 1. Reproducción | Pasa |
| 2. Integridad | Pasa |
| 3. Registro y cronología | Pasa con advertencias menores |
| 4. Robustez | Pasa con advertencias (R1 con poca holgura; R4 inestable) |
| 5. Lecturas | Pasa con advertencias |

## 1. Reproducción

AUC por rangos, bootstrap, inversión de signos, Holm y regla de decisión reimplementados. Diferencia máxima con `confirmatorio.csv` y `auc_por_persona.csv` del orden de 1e-16; las cuatro decisiones coinciden.

| Contraste | Delta | IC95 | IC90 | Mejoran | p | p Holm | Decisión |
|---|---|---|---|---|---|---|---|
| R1 red_orig − eeg_c1 | +0,0350 | [0,0233; 0,0468] | [0,0252; 0,0449] | 32/41 | 5,0e-6 | 2,0e-5 | efecto relevante |
| R2 red_ica3 − ica3_full | +0,0278 | [0,0126; 0,0432] | [0,0150; 0,0407] | 30/41 | 0,00084 | 0,0017 | respaldo |
| R3 red_orig − red_ica3 | +0,0673 | [0,0530; 0,0824] | [0,0553; 0,0798] | 39/41 | 5,0e-6 | 2,0e-5 | efecto relevante |
| R4 red_act − hgb_eeg_act | −0,0252 | [−0,0545; +0,0034] | [−0,0497; −0,0013] | 15/41 | 0,0995 | 0,0995 | inconcluso |

La t pareada y Wilcoxon dan las mismas conclusiones. Los p de R1 y R3 están en el piso de resolución de la prueba; se escriben "< 0,0001".

## 2. Integridad

- 22.176 filas por semilla en atención y 11.796 en activación, en los modelos nuevos y en los comparadores.
- Sin NaN ni filas duplicadas; cada ventana predicha una vez por semilla; 41 personas en todos; ninguna con una sola clase.
- Mismas filas, persona y etiqueta entre cada red y su comparador, y entre semillas. La columna `fold` coincide con `folds_rep` del protocolo.
- Los tres hashes de `tensores.json` coinciden con los tensores locales; los 72 hashes de `inputs` del protocolo coinciden con los archivos actuales.
- 50 ventanas con entrada toda en cero, como declara la enmienda.

## 3. Registro y cronología

- Protocolo registrado a las 10:25 (`0074c60`) y enmienda a las 10:34 (`7e1f1e0`); predicciones de las redes creadas entre 11:29 y 12:08. Ambos commits en `origin/main`.
- El script no cambió desde el registro (`git diff` vacío; sha256 igual al del protocolo). `report()` calcula lo prometido.
- Advertencia: las predicciones de `hgb_eeg_act` son de las 10:32, unos 2 minutos antes del commit de la enmienda. "Antes de ver resultados" vale para las redes. No hay evidencia de que se hayan leído y la enmienda no cambia reglas.
- Advertencia: "se ejecuta una vez" lo apoyan el `assert not dest.exists()` y las fechas de los archivos, pero no hay registro de ejecución.

## 4. Robustez

Delta por partición:

| Contraste | 1101 | 1102 | 1103 | 1104 | 1105 | Signo estable |
|---|---|---|---|---|---|---|
| R1 | +0,033 | +0,036 | +0,039 | +0,037 | +0,030 | sí |
| R2 | +0,028 | +0,024 | +0,030 | +0,032 | +0,026 | sí |
| R3 | +0,068 | +0,068 | +0,068 | +0,067 | +0,065 | sí |
| R4 | −0,039 | −0,042 | −0,021 | +0,002 | −0,028 | no (4/5) |

- Sin P23 y P39: R1 +0,0364 [0,0248; 0,0482]; R2 +0,0282 [0,0126; 0,0439]; R3 +0,0680 [0,0529; 0,0838]; R4 −0,0273 [−0,0574; +0,0026]. Ninguna decisión cambia.
- Dejar una persona fuera: R1 IC95 inferior entre 0,0215 y 0,0257; R2 entre 0,0100 y 0,0173; R3 al menos 0,0508; R4 pasa a "inferior" al quitar una de P10, P24, P33, P34 o P40.
- R1: IC95 inferior entre 0,0230 y 0,0234 con 30 semillas de bootstrap; 0,0232 con BCa; 0,0226 con t de Student. Sin P21 y P18 queda en 0,0199 ("respaldo"); con la partición 1105 sola, 0,0172.
- R4: "inconcluso" es la lectura correcta según la regla registrada. El IC90 excluye el cero por muy poco (límite superior entre −0,0015 y −0,0008 según la semilla de bootstrap; 0,0000 con t de Student). Ambos modelos están en el azar; la desviación entre semillas de la AUC por persona es cercana a 0,045.

## 5. Lecturas que no se sostienen

1. Que la red detecta actividad cerebral de atención: pierde 0,067 al filtrar componentes oculares y su probabilidad se correlaciona con la mirada (0,45–0,48; 0,32 tras el filtro).
2. Que la ventaja en R2 es información neuronal: la limpieza no garantiza quitar todo lo ocular.
3. Que R3 demuestra que la pérdida es específicamente ocular: no hubo red con filtro de control.
4. Que las redes profundas no sirven para activación, o que un modelo más complejo no mejora: es una arquitectura, sin búsqueda ni registro de convergencia.
5. Que el HGB es mejor que la red en activación, o que son equivalentes.
6. Que el EEG crudo no contiene información de activación.
7. Que la red es mejor que el HGB en general: vale frente a un HGB con variables fijas y configuración congelada, en atención.
8. Mezclar la AUC por persona (0,716) con la AUC de todas las ventanas juntas (0,684).

Todas las advertencias están incorporadas en `INFORME.md`.
