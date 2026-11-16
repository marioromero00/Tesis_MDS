"""Reproduce planificación y comprueba potencia por simulación bajo normalidad."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import t
import planificar_contraste_hipotesis as plan

plan.OUT=plan.ROOT/'resultados/protocolo_hipotesis_reintento_06-11-2026'
plan.main()
rng=np.random.default_rng(20261106)
rows=[]
for r in pd.read_csv(plan.OUT/'sensibilidad_fuente_varianza.csv').itertuples():
    n=r.n_evaluable;reps=100000;critical=t.ppf(.9875,n-1)
    # Independent sample mean and SD under the planning normal model.
    statistic=(rng.normal(size=reps)+.02*np.sqrt(n)/r.sd)/np.sqrt(rng.chisquare(n-1,size=reps)/(n-1))
    simulated=float((statistic>critical).mean())
    assert abs(simulated-r.power)<.006
    rows.append(dict(task=r.task,pilot=r.pilot,n=n,analytic=r.power,simulated=simulated))
(plan.OUT/'verificacion_simulada.json').write_text(json.dumps(dict(passed=True,replications=100000,assumption='iid normal participant differences; does not validate this assumption empirically',checks=rows),indent=2))
notes='''

## Cierre del reintento — 6 de noviembre de 2026

Los cálculos se reprodujeron y se contrastaron mediante 100.000 simulaciones por escenario de varianza bajo el supuesto normal del diseño. Los cuatro modelos seleccionados conservan sus hashes. No se adquirieron participantes ni se ejecutó una evaluación confirmatoria nueva.

El N de activación es muy sensible a la fuente de dispersión: 72 con la varianza de validación, 101 con la de test y 767 con la de OOF train. No son límites de un intervalo ni opciones para escoger por conveniencia. OOF mezcla modelos entrenados en distintos folds, mientras que la cohorte futura evalúa un par fijo; por tanto, 767 debe tratarse como escenario conservador de sensibilidad, no como requerimiento de reclutamiento demostrado. Las estimaciones externas se basan en solo ocho personas cada una. El diseño final necesita una estimación de variabilidad más defendible y factibilidad de adquisición antes de fijar N.

La referencia al AUC 0,67 corresponde provisionalmente al CatBoost de atención con 0,6744 en test. Su buen desempeño relativo al azar y la superioridad de un modelo temporal son afirmaciones distintas. El resultado de atención no desapareció al corregir GSR: el recálculo de activación trabaja sobre otra variable objetivo y otras entradas. Esta revisión verifica la procedencia de las métricas, no constituye una nueva auditoría completa del profesor de atención.

El margen práctico 0,02 sigue siendo una propuesta, no un umbral aprobado ni deducido de los resultados. Rechazar una mejora de al menos ese tamaño no equivale a rechazar cualquier mejora positiva. Si se mantiene la hipótesis original de superioridad >0, la frontera debe ser 0 y la potencia se calcula para un efecto verdadero separado de 0, sin cambiarla después de observar el test.
'''
p=plan.OUT/'INFORME.md';p.write_text(p.read_text()+notes)
with (plan.ROOT/'../../notas/bitacora.md').resolve().open('a') as f:
    f.write('\n\n## 2026-11-06 — Protocolo de hipótesis reproducido\n'+str(plan.OUT)+'\n'+notes)
print('VERIFICACIÓN POR SIMULACIÓN APROBADA')
