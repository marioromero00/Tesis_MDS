"""Predicciones guardadas: fold de cada persona segun protocolo, mismas filas entre modelos pareados,
ambas clases por persona, y reglas de decision/Holm recalculadas. Sin modelos."""
import json
from c00_carga import *
import cierre_final_41p as F
RES = ROOT / 'resultados'
d = data()
ya = d.set_index('source_row')
def check(path, folds, task, seedcol=None, foldsets=None):
    p = pd.read_csv(path)
    out = []
    groups = [(None, p)] if seedcol is None else list(p.groupby(seedcol))
    for s, g in groups:
        fl = folds if foldsets is None else foldsets[str(s)]
        who = {q: k for k, f in enumerate(fl) for q in f}
        bad = (g.participant.map(who) != g.fold).sum() if 'fold' in g else -1
        rows = g.groupby('strategy').source_row.apply(lambda x: tuple(x))
        same = rows.nunique() == 1
        dup = g.groupby('strategy').source_row.apply(lambda x: x.duplicated().any()).any()
        one = g.groupby(['strategy', 'participant']).y.nunique().lt(2).sum()
        ylab = (ya.loc[g.source_row, f'y_{task}'].to_numpy() == g.y.to_numpy()).mean()
        out.append((s, bad, same, dup, one, round(ylab, 4), g.participant.nunique(), g.strategy.nunique()))
    print(f'  {path.relative_to(RES)}: (semilla, filas con fold≠protocolo, mismas filas y orden entre estrategias, duplicadas, persona-estrategia con 1 clase, y == etiqueta vigente, personas, estrategias)')
    for o in out: print('     ', o)
fm = json.loads((RES/'cierre_final_41p_16-11-2026/protocolo.json').read_text())['folds']
rb = json.loads((RES/'cierre_robustez_41p_16-11-2026/protocolo.json').read_text())
for task in ['atencion', 'activacion']:
    check(RES/f'cierre_final_41p_16-11-2026/predicciones_{task}.csv.gz', fm, task)
    check(RES/f'cierre_robustez_41p_16-11-2026/r1_{task}.csv.gz', fm, task)
    check(RES/f'cierre_robustez_41p_16-11-2026/r3_{task}.csv.gz', None, task, 'seed', rb['folds_r3'])
    check(RES/f'ampliacion_41p_16-11-2026/predicciones_{task}.csv.gz', fm, task)
    check(RES/f'ampliacion_41p_16-11-2026/enmienda_e1_lag6/predicciones_{task}.csv.gz', fm, task)
    check(RES/f'explicativo_posicion_41p_18-11-2026/predicciones_{task}.csv.gz', fm, task)
    a = pd.read_csv(RES/f'cierre_final_41p_16-11-2026/predicciones_{task}.csv.gz'); a = a[a.strategy.eq('hgb_c1')].source_row.to_numpy()
    for f in [f'cierre_robustez_41p_16-11-2026/r1_{task}.csv.gz', f'ampliacion_41p_16-11-2026/predicciones_{task}.csv.gz', f'ampliacion_41p_16-11-2026/enmienda_e1_lag6/predicciones_{task}.csv.gz', f'explicativo_posicion_41p_18-11-2026/predicciones_{task}.csv.gz']:
        b = pd.read_csv(RES/f); b = b[b.strategy.eq(b.strategy.iloc[0])].source_row.to_numpy()
        print('     mismas filas que hgb_c1 del analisis final:', f, bool(len(a) == len(b) and (a == b).all()))
check(RES/'cierre_robustez_41p_16-11-2026/r2_atencion.csv.gz', fm, 'atencion')
r2 = pd.read_csv(RES/'cierre_robustez_41p_16-11-2026/r2_atencion.csv.gz'); r2 = r2[r2.strategy.eq('hgb_c1')]
print('  R2: fraccion de filas cuya etiqueta por fold difiere de la vigente:', round(float((ya.loc[r2.source_row, 'y_atencion'].to_numpy() != r2.y.to_numpy()).mean()), 4), '| filas', len(r2), 'vs', int(d.y_atencion.notna().sum()))
# V3: OOF y externas
for task in ['atencion', 'activacion']:
    o = pd.read_csv(RES/f'cierre_v3_16-11-2026/oof_{task}.csv.gz'); e = pd.read_csv(RES/f'cierre_v3_16-11-2026/externas_{task}.csv.gz')
    v3 = json.loads((RES/'cierre_v3_16-11-2026/protocolo.json').read_text())['folds']
    who = {q: f['fold'] for f in v3 for q in f['evaluation']}
    print(f'  V3 {task}: OOF fold≠protocolo {(o.participant.map(who) != o.fold).sum()}, personas OOF {o.participant.nunique()}, externas split {e.groupby("split").participant.nunique().to_dict()}, '
          f'interseccion OOF/externas {len(set(o.participant) & set(e.participant))}, mismas filas entre estrategias OOF {o.groupby("strategy").source_row.apply(tuple).nunique() == 1}, ext {e.groupby("strategy").source_row.apply(tuple).nunique() == 1}')
    print('     selecciones', pd.read_csv(RES/f'cierre_v3_16-11-2026/selecciones_{task}.csv').leaves.tolist(), '| busqueda media por hojas', pd.read_csv(RES/f'cierre_v3_16-11-2026/busqueda_interna_{task}.csv').groupby('leaves').auc.mean().round(4).to_dict(),
          '| por contexto y hojas', pd.read_csv(RES/f'cierre_v3_16-11-2026/busqueda_interna_{task}.csv').groupby(['context', 'leaves']).auc.mean().round(4).to_dict())
# reglas de decision: casos donde se cumplen dos reglas a la vez
print('== Reglas de decision: filas donde se cumplen a la vez dos reglas (precedencia del codigo: respaldo > inferior > nulo)')
files = ['cierre_final_41p_16-11-2026/contrastes.csv', 'reapertura_41p_22-11-2026/confirmatorio.csv', 'reapertura_41p_22-11-2026/curva_temporal.csv', 'reapertura_fase2_41p_22-11-2026/x1_placebo_bloque.csv',
         'reapertura_fase2_41p_22-11-2026/x2_estratificada.csv', 'reapertura_fase3_41p_22-11-2026/confirmatorio.csv', 'enfoques_41p_22-11-2026/e1_confirmatorio.csv', 'enfoques_41p_22-11-2026/e2_confirmatorio.csv',
         'enfoques_41p_22-11-2026/e3_confirmatorio.csv', 'enfoques_41p_22-11-2026/e4_confirmatorio.csv', 'limpieza_ocular_41p_23-11-2026/confirmatorio.csv', 'red_cruda_41p_23-11-2026/confirmatorio.csv']
for f in files:
    t = pd.read_csv(RES/f)
    ph = t.p_holm.where(t.p_holm.notna(), np.where(t.p < .05, t.p, 1))
    resp = (ph < .05) & (t.low95 > 0); inf = t.high95 < 0; nulo = (t.low90 > -.02) & (t.high90 < .02)
    again = [F.decide(r.delta, r.low95, r.high95, r.low90, r.high90, q) for r, q in zip(t.itertuples(), ph)]
    assert (pd.Series(again) == t.decision).all(), f
    both = t[(resp & nulo) | (inf & nulo)]
    for r in both.itertuples():
        name = ' '.join(str(getattr(r, c)) for c in ['task', 'test', 'strata', 'contrast'] if hasattr(r, c))
        print(f'   {f.split("/")[0]}: {name}: {r.delta:+.4f} IC95 [{r.low95:+.4f}; {r.high95:+.4f}] IC90 [{r.low90:+.4f}; {r.high90:+.4f}] -> "{r.decision}" (tambien cumple nulo concluyente)')
print('   decisiones de los 12 CSV reproducidas con F.decide: OK')
