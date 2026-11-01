"""Protocolo acotado: selección agrupada en train, congelación y evaluación V2."""
import argparse
import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from threadpoolctl import threadpool_limits
from atencion_binaria import ROOT, digest, write
from comparacion_comun_binaria import representation
from diagnostico_busqueda_activacion import weights
from temporales_core import preprocessor, history_indices
from evaluar_temporalidad_eeg_v2 import ci
from reconstruir_profesor_atencion_binaria import KEYS

OUT=ROOT/'resultados/activacion_v2_comparacion_final_01-11-2026'
SOURCE=ROOT/'resultados/preprocesamiento/caracteristicas_multimodales.csv'
LABELS=ROOT/'resultados/etiquetas_gsr_calidad_v2_01-11-2026/etiquetas.csv.gz'
PARTS=ROOT/'resultados/modelado/particion_participantes.csv'
FOLDS=ROOT/'resultados/profesor_binario_reconstruido_29-10-2026/protocolo.json'
SPATIAL={'train':ROOT/'resultados/eeg_por_canal_v2_29-10-2026/caracteristicas_eeg_por_canal.csv.gz','validation':ROOT/'resultados/temporalidad_eeg_v2_validacion_29-10-2026/caracteristicas_validation.csv.gz','test':ROOT/'resultados/temporalidad_eeg_v2_test_29-10-2026/caracteristicas_test.csv.gz'}
CONTEXTS=[1,8,32]
PARAMS=dict(max_iter=300,l2_regularization=10.,learning_rate=.05,min_samples_leaf=30,early_stopping=False,random_state=20261101)

def plan():return json.loads((OUT/'protocolo.json').read_text())
def prepare():
 OUT.mkdir(exist_ok=False);(OUT/'modelos').mkdir()
 groups=json.loads((ROOT/'resultados/comparacion_comun_binaria_30-10-2026/protocolo.json').read_text())['groups']['activacion']
 cols=sum(groups.values(),[])
 assert not any('gsr' in x.lower() or 'arousal' in x.lower() for x in cols)
 paths=[SOURCE,LABELS,PARTS,FOLDS,*SPATIAL.values(),Path(__file__),ROOT/'scripts/comparacion_comun_binaria.py',ROOT/'scripts/temporales_core.py']
 write(OUT/'protocolo.json',dict(created_utc=pd.Timestamp.now(tz='UTC').isoformat(),approval='Mario comunica aprobación de etiquetas V2 por su profesor en esta sesión, 01-11-2026',inputs={str(p.relative_to(ROOT)):digest(p) for p in paths},features=cols,contexts=CONTEXTS,grid=[7,15],params=PARAMS,folds=json.loads(FOLDS.read_text())['folds'],selection='Shared leaf count across contexts, maximizing mean inner participant AUC across contexts within each outer fold. Final shared count: maximum mean inner AUC across all five folds/contexts; ties fewer leaves. Never use outer/validation/test for selection.',primary='context32 minus context1, identical family and hyperparameters',secondary='context8 minus context1',history='retained labelled rows only; reset at gaps and recording/segment/stimulus boundaries; historical mean and SD, not order-sensitive',evaluation='OOF train plus fixed final models on validation and test after freeze; all are exploratory due to historical reuse',metric='macro participant ROC-AUC, paired participant bootstrap 20000 descriptive 95% CI; no multiplicity adjustment',stop='one predefined grid, no extra search after external evaluation',limits='offline pseudo-labels; no psychological validation; no direct comparison with legacy label metrics; no modality ablation in this task'))

def verify_inputs():
 for path,h in plan()['inputs'].items():assert digest(ROOT/path)==h,path

def load(split):
 p=plan();cols=p['features'];raw=pd.read_csv(SOURCE);raw['source_row']=np.arange(len(raw))
 raw['split']=raw.participant.map(pd.read_csv(PARTS).set_index('participant').split)
 raw=raw[raw.split.eq(split)].copy()
 labels=pd.read_csv(LABELS);labels=labels[labels.split.eq(split)&labels.activation_binary_v2.notna()]
 channel=[c for c in cols if c.startswith(('eegch','eegsp'))]
 raw=raw.merge(pd.read_csv(SPATIAL[split])[['source_row']+channel],on='source_row',validate='one_to_one')
 f=raw.merge(labels[['source_row','activation_binary_v2']],on='source_row',validate='one_to_one').rename(columns={'activation_binary_v2':'y'}).sort_values(KEYS).reset_index(drop=True)
 assert len(f)==len(labels) and not f.source_row.duplicated().any()
 assert (f.groupby('participant').y.nunique()==2).all()
 f.y=f.y.astype(int)
 return f

def score(f,p):return float(np.mean([roc_auc_score(f.iloc[ix].y,np.asarray(p)[ix]) for ix in f.groupby('participant').indices.values()]))
def estimator(leaves):return HistGradientBoostingClassifier(max_leaf_nodes=int(leaves),**plan()['params'])
def fit_bundle(f,prep,ctx,leaves,path):
 cols=plan()['features'];m=estimator(leaves);m.fit(representation(prep,f,cols,ctx),f.y,sample_weight=weights(f))
 b=dict(model=m,prep=prep,cols=cols,context=ctx,fit_people=sorted(f.participant.unique()),leaves=int(leaves))
 joblib.dump(b,path,compress=3);return b

def predict(b,f):return b['model'].predict_proba(representation(b['prep'],f,b['cols'],b['context']))[:,1]
def coverage(f,split):
 rows=[]
 for ctx in CONTEXTS:
  ix,l=history_indices(f,ctx)
  for row,indices in enumerate(ix):
   indices=indices[indices>=0]
   assert indices[-1]==row and np.all(indices<=row)
   for key in ['participant','recording','segment_id','stimulus','split']:assert f.iloc[indices][key].eq(f.iloc[row][key]).all()
  for person,indices in f.groupby('participant').indices.items():rows.append(dict(split=split,context=ctx,participant=person,windows=len(indices),mean_history=float(l[indices].mean()),full_fraction=float((l[indices]==ctx).mean())))
 pd.DataFrame(rows).to_csv(OUT/f'cobertura_{split}.csv',index=False)

def train():
 verify_inputs();assert not (OUT/'congelacion.json').exists()
 f=load('train');cols=plan()['features'];trials=[];preds=[];selections=[]
 f[['source_row','participant','split','y']].to_csv(OUT/'filas_train.csv.gz',index=False)
 for fold in plan()['folds']:
  inner=f[f.participant.isin(fold['inner_fit'])].reset_index(drop=True);iv=f[f.participant.isin(fold['inner_validation'])].reset_index(drop=True)
  fit=f[f.participant.isin(fold['fit'])].reset_index(drop=True);val=f[f.participant.isin(fold['evaluation'])].reset_index(drop=True)
  assert set(inner.participant).isdisjoint(iv.participant) and set(fit.participant).isdisjoint(val.participant)
  assert set(inner.participant)|set(iv.participant)==set(fit.participant)
  prep=preprocessor().fit(inner[cols]);local=[]
  for ctx in CONTEXTS:
   a=representation(prep,inner,cols,ctx);b=representation(prep,iv,cols,ctx)
   for leaves in plan()['grid']:
    m=estimator(leaves);m.fit(a,inner.y,sample_weight=weights(inner));prob=m.predict_proba(b)[:,1]
    r=dict(fold=fold['fold'],context=ctx,leaves=leaves,auc=score(iv,prob));local.append(r);trials.append(r)
    pd.DataFrame(trials).to_csv(OUT/'busqueda_interna.csv',index=False)
    iv[['source_row','participant','y']].assign(prob=prob).to_csv(OUT/f'interna_fold{fold["fold"]}_ctx{ctx}_h{leaves}.csv.gz',index=False)
    print('Interno',fold['fold'],ctx,leaves,flush=True)
  shared=int(pd.DataFrame(local).groupby('leaves').auc.mean().sort_index().idxmax());selections.append(dict(fold=fold['fold'],leaves=shared))
  prep=preprocessor().fit(fit[cols])
  for ctx in CONTEXTS:
   path=OUT/'modelos'/f'fold{fold["fold"]}_ctx{ctx}.joblib';bundle=fit_bundle(fit,prep,ctx,shared,path);prob=predict(bundle,val)
   np.testing.assert_allclose(prob,predict(joblib.load(path),val),atol=1e-12)
   preds.append(val[['source_row','participant','y']].assign(prob=prob,context=ctx,fold=fold['fold'],split='oof_train'))
   pd.concat(preds).to_csv(OUT/'predicciones_oof.csv.gz',index=False)
  print('Fold completo',fold['fold'],flush=True)
 pd.DataFrame(selections).to_csv(OUT/'selecciones.csv',index=False)
 final=int(pd.DataFrame(trials).groupby('leaves').auc.mean().sort_index().idxmax())
 prep=preprocessor().fit(f[cols]);models={}
 for ctx in CONTEXTS:
  path=OUT/'modelos'/f'final_ctx{ctx}.joblib';fit_bundle(f,prep,ctx,final,path);models[str(ctx)]=dict(path=str(path.relative_to(ROOT)),sha256=digest(path))
 verify_inputs()
 write(OUT/'congelacion.json',dict(created_utc=pd.Timestamp.now(tz='UTC').isoformat(),protocol_sha256=digest(OUT/'protocolo.json'),search_sha256=digest(OUT/'busqueda_interna.csv'),leaves=final,models=models,validation_evaluated=False,test_evaluated=False))
 print('CONGELADO: hojas',final,flush=True)

def evaluate():
 verify_inputs();frozen=json.loads((OUT/'congelacion.json').read_text());assert not (OUT/'predicciones_externas.csv.gz').exists()
 assert digest(OUT/'protocolo.json')==frozen['protocol_sha256']
 frames=[]
 for split in ['validation','test']:
  f=load(split)
  for ctx in CONTEXTS:
   meta=frozen['models'][str(ctx)];path=ROOT/meta['path'];assert digest(path)==meta['sha256'];bundle=joblib.load(path)
   assert set(f.participant).isdisjoint(bundle['fit_people'])
   frames.append(f[['source_row','participant','y']].assign(prob=predict(bundle,f),context=ctx,split=split))
 pd.concat(frames).to_csv(OUT/'predicciones_externas.csv.gz',index=False)
 report()

def report():
 preds=pd.concat([pd.read_csv(OUT/'predicciones_oof.csv.gz'),pd.read_csv(OUT/'predicciones_externas.csv.gz')],ignore_index=True)
 people=[];summ=[];contr=[]
 for (split,ctx,person),g in preds.groupby(['split','context','participant']):people.append(dict(split=split,context=ctx,participant=person,windows=len(g),auc=roc_auc_score(g.y,g.prob)))
 people=pd.DataFrame(people);people.to_csv(OUT/'metricas_personas.csv',index=False)
 for (split,ctx),g in people.groupby(['split','context']):
  mean,lo,hi=ci(g.auc);summ.append(dict(split=split,context=ctx,auc=mean,low=lo,high=hi))
 for split,g in people.groupby('split'):
  wide=g.pivot(index='participant',columns='context',values='auc')
  for ctx in [8,32]:
   d=wide[ctx]-wide[1];mean,lo,hi=ci(d);contr.append(dict(split=split,context=ctx,delta=mean,low=lo,high=hi,improved=int((d>0).sum()),people=len(d)))
 pd.DataFrame(summ).to_csv(OUT/'metricas.csv',index=False);pd.DataFrame(contr).to_csv(OUT/'contrastes.csv',index=False)
 for split in ['train','validation','test']:
  f=load(split);coverage(f,split)
  for ctx in CONTEXTS:
   g=preds[preds.split.eq('oof_train' if split=='train' else split)&preds.context.eq(ctx)].sort_values('source_row')
   assert not g.source_row.duplicated().any() and g.prob.between(0,1).all()
   np.testing.assert_array_equal(g.source_row,f.sort_values('source_row').source_row);np.testing.assert_array_equal(g.y,f.sort_values('source_row').y)
 verify_inputs();write(OUT/'auditoria.json',dict(passed=True,internal_fits=30,outer_models=15,final_models=3,same_rows_labels=True,inputs_unchanged=True,freeze_sha256=digest(OUT/'congelacion.json'),train_windows=7028,validation_windows=2584,test_windows=2184))
 lines=['# Activación V2: comparación final acotada','','Etiquetas V2 aprobadas por el profesor según comunicación de Mario. HistGradientBoosting, dos candidatos (7/15 hojas), 30 ajustes internos, 15 modelos externos OOF y tres modelos finales. Configuración común a los contextos seleccionada solo con AUC interna de train. Comparación principal: 32 menos 1; secundaria: 8 menos 1. Modelos finales congelados antes de evaluar validation/test.','','| Evaluación | Contexto | AUC macro persona | IC descriptivo 95% |','|---|---|---|---|']
 for r in summ:lines.append(f"| {r['split']} | {r['context']} | {r['auc']:.4f} | [{r['low']:.4f}; {r['high']:.4f}] |")
 lines+=['','| Evaluación | Historial menos actual | ΔAUC | IC descriptivo 95% | Personas mejoran |','|---|---|---|---|---|']
 for r in contr:lines.append(f"| {r['split']} | {r['context']} | {r['delta']:+.4f} | [{r['low']:.4f}; {r['high']:.4f}] | {r['improved']}/{r['people']} |")
 lines+=['','## Alcance','Exploratorio: train, validation y test tienen exposición histórica. Bootstrap descriptivo por participante, sin corrección por búsqueda histórica o multiplicidad. Las pseudoetiquetas son offline y no validan activación psicológica externa. El historial usa media/desviación y solo filas etiquetadas consecutivas; se reinicia ante huecos. No es una arquitectura sensible al orden ni un estudio de ablación de fusión. P4 y todos los participantes se conservan. No comparar métricas entre etiquetas antiguas y V2 como si fuera la misma tarea.','', 'El baseline logístico previo está en ../activacion_v2_historial_01-11-2026/INFORME.md; su comparación con este modelo solo corresponde a OOF train, no a test.']
 (OUT/'INFORME.md').write_text('\n'.join(lines)+'\n');print(pd.DataFrame(summ).to_string(index=False));print(pd.DataFrame(contr).to_string(index=False))

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['prepare','train','evaluate','report']);args=parser.parse_args()
 with threadpool_limits(limits=2):globals()[args.phase]()
