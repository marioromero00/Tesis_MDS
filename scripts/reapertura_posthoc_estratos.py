"""Comprobación POST HOC NO REGISTRADA (22-11-2026), hecha después de ver los resultados de la reapertura.

Motivo: en la fase 2 (X2) la AUC estratificada por posición dio una ganancia del historial en atención
(+0,017), en aparente tensión con el explicativo del 18-11 (el historial no agrega nada sobre la posición
como variable). Aquí se aplica la misma estratificación a las predicciones ya guardadas del 16 y 18-11
(partición del análisis final, una sola partición), que incluyen el modelo con posición `pos_c1`.
No entrena nada. Es descriptivo y se reporta como tal.
"""
import pandas as pd
from atencion_binaria import ROOT
import cierre_experimental_v3 as V3
import cierre_final_41p as F
import reapertura_41p as R
import reapertura_fase2_41p as X

E = ROOT / 'resultados/explicativo_posicion_41p_18-11-2026'
rows = []
d = V3.load_data()
for task in F.LEAVES:
    st = X.strata_table(V3.Task(d, task))
    p = pd.concat([pd.read_csv(F.OUT / f'predicciones_{task}.csv.gz'), pd.read_csv(E / f'predicciones_{task}.csv.gz')])
    p = p[p.strategy.isin(['hgb_c1', 'hgb_c32', 'pos_c1', 'hgb_c32pos'])].join(st, on='source_row')
    for col in X.STRATA:
        w = p.groupby(['strategy', 'participant']).apply(lambda g: R.stratified_auc(g, col)).unstack(0)
        for a, b in [('hgb_c32', 'hgb_c1'), ('pos_c1', 'hgb_c1'), ('hgb_c32', 'pos_c1'), ('hgb_c32pos', 'pos_c1')]:
            rows.append(dict(task=task, strata=col, contrast=f'{a} − {b}', **R.contrast(w, a, b)))
out = pd.DataFrame(rows)
out.to_csv(X.OUT / 'posthoc_no_registrado_estratos_con_posicion.csv', index=False)
print(out.round(4).to_string(index=False))
