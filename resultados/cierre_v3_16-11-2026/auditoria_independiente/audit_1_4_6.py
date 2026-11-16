import hashlib, json, os, sys
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.metrics import roc_auc_score, balanced_accuracy_score, f1_score, recall_score
ROOT = Path('/Users/mario/Proyectos/tesis-mds/repos/Tesis_MDS'); OUT = ROOT/'resultados/cierre_v3_16-11-2026'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
P = json.loads((OUT/'protocolo.json').read_text())
print('== 1 integridad')
bad = [k for k,v in P['inputs'].items() if sha(ROOT/k)!=v]; print('inputs', len(P['inputs']), 'mismatch', bad)
for t in ['atencion','activacion']:
    c = json.loads((OUT/f'congelacion_{t}.json').read_text())
    mb = [k for k,v in c['models'].items() if sha(ROOT/k)!=v]
    ondisk = sorted(str(p.relative_to(ROOT)) for p in (OUT/'modelos'/t).iterdir())
    print(t, 'models', len(c['models']), 'mismatch', mb, 'set_equal_disk', ondisk==sorted(c['models']),
          'externas', sha(OUT/f'externas_{t}.csv.gz')==c['external_sha256'])
    pv = json.loads((OUT/f'congelacion_previa_{t}.json').read_text())
    print(t, 'previa', {k: sha(OUT/f)==pv[k] for k,f in [('protocol_sha256','protocolo.json'),('search_sha256',f'busqueda_interna_{t}.csv'),
          ('oof_sha256',f'oof_{t}.csv.gz'),('selections_sha256',f'selecciones_{t}.csv')]},
          'oof_listo', json.loads((OUT/f'oof_{t}_listo.json').read_text())['sha256']==sha(OUT/f'oof_{t}.csv.gz'))
print('== 2 orden temporal / busqueda')
parts = pd.read_csv(ROOT/'resultados/modelado/particion_participantes.csv').set_index('participant').split
train = set(parts[parts=='train'].index); val=set(parts[parts=='validation'].index); test=set(parts[parts=='test'].index)
print('n train/val/test', len(train), len(val), len(test))
for t in ['atencion','activacion']:
    pv = json.loads((OUT/f'congelacion_previa_{t}.json').read_text()); c = json.loads((OUT/f'congelacion_{t}.json').read_text())
    tp = pd.Timestamp(pv['created_utc']); tc = pd.Timestamp(c['created_utc'])
    mt = lambda f: pd.Timestamp(os.stat(OUT/f).st_mtime, unit='s', tz='UTC')
    models_min = min(pd.Timestamp(os.stat(ROOT/k).st_mtime, unit='s', tz='UTC') for k in c['models'])
    print(t, 'previa', tp, 'mtime', mt(f'congelacion_previa_{t}.json'), '| externas mtime', mt(f'externas_{t}.csv.gz'),
          '| primer modelo mtime', models_min, '| congel', tc, '| oof_listo', json.loads((OUT/f'oof_{t}_listo.json').read_text())['created_utc'],
          'ok', tp < models_min and mt(f'congelacion_previa_{t}.json') < mt(f'externas_{t}.csv.gz') and tp < tc)
folds = P['folds']
allp = set()
for f in folds:
    s = {k:set(f[k]) for k in ['fit','evaluation','inner_fit','inner_validation']}
    assert s['inner_fit']|s['inner_validation']==s['fit'] and not s['inner_fit']&s['inner_validation'] and not s['fit']&s['evaluation']
    assert set().union(*s.values()) <= train
    allp |= s['evaluation']
print('folds: union eval == train', allp==train, 'eval disjoint', sum(len(f['evaluation']) for f in folds)==len(train))
for t in ['atencion','activacion']:
    b = pd.read_csv(OUT/f'busqueda_interna_{t}.csv'); print(t, 'busqueda filas', len(b), 'folds', sorted(b.fold.unique()), 'contexts', sorted(b.context.unique()),
          'leaves', sorted(b.leaves.unique()))
    # recompute selection
    sel = pd.read_csv(OUT/f'selecciones_{t}.csv')
    re = b.groupby(['fold','leaves']).auc.mean().unstack().idxmax(axis=1)
    print(t, 'selecciones reproducen', (re.values==sel.leaves.values).all(), 'final leaves', int(b.groupby('leaves').auc.mean().idxmax()),
          'congel', json.loads((OUT/f'congelacion_{t}.json').read_text())['leaves'])
print('== 3 solapamiento')
pred = {}
for t in ['atencion','activacion']:
    o = pd.read_csv(OUT/f'oof_{t}.csv.gz'); e = pd.read_csv(OUT/f'externas_{t}.csv.gz'); pred[t]=(o,e)
    print(t, 'oof people subset train', set(o.participant)<=train, 'n', o.participant.nunique(), 'oof ∩ val/test', set(o.participant)&(val|test))
    pf = o.groupby('participant').fold.nunique(); print(t, 'cada persona 1 fold', (pf==1).all())
    fmap = {p:f['fold'] for f in folds for p in f['evaluation']}
    print(t, 'fold coincide con protocolo', (o.participant.map(fmap)==o.fold).all())
    print(t, 'oof dup (strategy,source_row)', o.duplicated(['strategy','source_row']).sum(), 'estrategias', o.strategy.nunique(),
          'filas por estrategia', o.groupby('strategy').size().unique())
    print(t, 'ext split por persona correcto', (e.participant.map(parts)==e.split).all(), 'ext ∩ train', set(e.participant)&train,
          'dup', e.duplicated(['strategy','split','source_row']).sum(), 'filas/estr', e.groupby('strategy').size().unique(),
          'personas val/test', e[e.split=='validation'].participant.nunique(), e[e.split=='test'].participant.nunique())
    print(t, 'source_row oof ∩ ext', len(set(o.source_row)&set(e.source_row)))
print('== 6 etiquetas')
la = pd.read_csv(ROOT/'resultados/comparacion_comun_binaria_30-10-2026/etiquetas_atencion.csv.gz')
lg = pd.read_csv(ROOT/'resultados/etiquetas_gsr_calidad_v2_01-11-2026/etiquetas.csv.gz')
for t, ref, col in [('atencion', la, 'y'), ('activacion', lg, 'activation_binary_v2')]:
    o, e = pred[t]; a = pd.concat([o[['source_row','participant','y']], e[['source_row','participant','y']]]).drop_duplicates()
    assert not a.source_row.duplicated().any()
    r = ref[['source_row','participant',col]].rename(columns={col:'yr','participant':'pr'})
    m = a.merge(r, on='source_row', how='left')
    print(t, 'filas', len(a), 'sin ref', m.yr.isna().sum(), 'y distinto', (m.y!=m.yr).sum(), 'persona distinta', (m.participant!=m.pr).sum())
    refl = r[r.yr.notna() & r.pr.map(parts).isin(['train','validation','test'])]
    print(t, 'ref etiquetadas (train/val/test)', len(refl), 'no usadas', len(set(refl.source_row)-set(a.source_row)))
print('== 4 metricas')
def ci(v):
    v=np.asarray(v);rng=np.random.default_rng(20261029)
    b=v[rng.integers(0,len(v),(20000,len(v)))].mean(axis=1)
    return float(v.mean()),*map(float,np.quantile(b,[.025,.975]))
allpred = pd.concat([x for t in pred for x in pred[t]], ignore_index=True)
rows=[]
for (task, split, strat, person), g in allpred.groupby(['task','split','strategy','participant']):
    yh=(g.prob>=.5).astype(int)
    rows.append(dict(task=task, split=split, strategy=strat, participant=person, windows=len(g), auc=roc_auc_score(g.y,g.prob),
        ba=balanced_accuracy_score(g.y,yh), f1_macro=f1_score(g.y,yh,average='macro',zero_division=0),
        recall_alta=recall_score(g.y,yh,pos_label=1,zero_division=0), recall_baja=recall_score(g.y,yh,pos_label=0,zero_division=0)))
pp = pd.DataFrame(rows)
K=['task','split','strategy','participant']; M=['windows','auc','ba','f1_macro','recall_alta','recall_baja']
ref = pd.read_csv(OUT/'metricas_personas.csv'); j = pp.merge(ref, on=K, suffixes=('','_r'), how='outer', indicator=True)
print('personas filas', len(pp), len(ref), 'no emparejadas', (j._merge!='both').sum(), 'maxdiff', {m: float((j[m]-j[m+'_r']).abs().max()) for m in M})
summ=[]
for (task, split, strat), g in pp.groupby(['task','split','strategy']):
    r=dict(task=task, split=split, strategy=strat, people=len(g))
    for m in M[1:]:
        a,lo,hi=ci(g[m]); r.update({m:a, f'{m}_low':lo, f'{m}_high':hi})
    summ.append(r)
summ=pd.DataFrame(summ); ref=pd.read_csv(OUT/'metricas.csv'); j=summ.merge(ref,on=K[:3],suffixes=('','_r'),how='outer',indicator=True)
cols=[c for c in summ.columns if c not in K[:3]]
print('metricas filas', len(summ), len(ref), 'no emparejadas', (j._merge!='both').sum(), 'maxdiff', max(float((j[c]-j[c+'_r']).abs().max()) for c in cols))
con=[]
for (task, split), g in pp.groupby(['task','split']):
    wide=g.pivot(index='participant', columns='strategy', values='auc')
    for name,a,b,role in P['contrasts']:
        d=(wide[a]-wide[b]).dropna(); mu,lo,hi=ci(d)
        con.append(dict(task=task,split=split,contrast=name,role=role,delta=mu,low=lo,high=hi,improved=int((d>0).sum()),people=len(d)))
con=pd.DataFrame(con); ref=pd.read_csv(OUT/'contrastes.csv'); j=con.merge(ref,on=['task','split','contrast'],suffixes=('','_r'),how='outer',indicator=True)
print('contrastes filas', len(con), len(ref), 'no emparejadas', (j._merge!='both').sum(), 'role eq', (j.role==j.role_r).all(),
      'maxdiff', {c: float((j[c]-j[c+'_r']).abs().max()) for c in ['delta','low','high','improved','people']})
con.to_csv(Path(__file__).parent/'contrastes_recalc.csv', index=False)
print(con[con.split!='oof_train'][['task','split','contrast','delta','low','high','improved','people']].to_string())
