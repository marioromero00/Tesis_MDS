"""Ablación controlada V2 con hiperparámetros heredados de selección en train."""
import argparse
import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from threadpoolctl import threadpool_limits
import activacion_v2_comparacion_final as base
from atencion_binaria import ROOT, digest, write
from comparacion_comun_binaria import representation
from diagnostico_busqueda_activacion import weights
from temporales_core import preprocessor
from evaluar_temporalidad_eeg_v2 import ci

OUT=ROOT/'resultados/ablacion_modalidades_v2_01-11-2026'
MODALITIES=['EEG','Eye','Pupil']
CONTEXTS=[1,8,32]

def plan():return json.loads((OUT/'protocolo.json').read_text())
def verify():
 for path,h in plan()['inputs'].items():assert digest(ROOT/path)==h,path

def prepare():
 base.verify_inputs();OUT.mkdir(exist_ok=False);(OUT/'modelos').mkdir()
 groups=json.loads((ROOT/'resultados/comparacion_comun_binaria_30-10-2026/protocolo.json').read_text())['groups']['activacion']
 assert list(groups)==MODALITIES and sum(groups.values(),[])==base.plan()['features']
 assert not any('gsr' in c.lower() or 'arousal' in c.lower() for cols in groups.values() for c in cols)
 sources=[base.OUT/'protocolo.json',base.OUT/'congelacion.json',base.OUT/'selecciones.csv',base.OUT/'busqueda_interna.csv',base.OUT/'predicciones_oof.csv.gz',base.OUT/'predicciones_externas.csv.gz',Path(__file__),ROOT/'scripts/diagnostico_busqueda_activacion.py',ROOT/'scripts/evaluar_temporalidad_eeg_v2.py']
 sources+=sorted((base.OUT/'modelos').glob('*.joblib'))
 hashes={**base.plan()['inputs'],**{str(p.relative_to(ROOT)):digest(p) for p in sources}}
 write(OUT/'protocolo.json',dict(created_utc=pd.Timestamp.now(tz='UTC').isoformat(),inputs=hashes,groups=groups,contexts=CONTEXTS,folds=base.plan()['folds'],params=base.plan()['params'],selection='Controlled ablation: identical parameters to full fusion for each outer fold and final model. Leaf counts inherited exclusively from prior inner-train selection; no new tuning, no external-score selection.',comparisons='Full early fusion minus each single modality at every context; all nine predefined paired contrasts reported, no selection of best modality from test.',reused='Full models and predictions reused byte-for-byte; no retraining of full fusion.',rows='identical V2 labelled rows across all modalities and contexts; imputation fit only on fitting persons; no modality-specific exclusions',history='same retained-row history as prior run; 32 is maximum, often unavailable fully; current plus mean/SD, not order-sensitive',metric='macro participant ROC-AUC; paired participant bootstrap 20000, descriptive 95% intervals, no multiplicity correction',stop='one controlled ablation without extra searches based on evaluation results',scope='exploratory reused train/validation/test; offline GSR pseudo-labels, not psychological validation; early fusion only; no pairwise modalities or late/intermediate fusion'))

def fit(f,cols,ctx,leaves,path):
 prep=preprocessor().fit(f[cols]);m=HistGradientBoostingClassifier(max_leaf_nodes=int(leaves),**plan()['params'])
 m.fit(representation(prep,f,cols,ctx),f.y,sample_weight=weights(f))
 bundle=dict(model=m,prep=prep,cols=cols,context=ctx,leaves=int(leaves),fit_people=sorted(f.participant.unique()))
 joblib.dump(bundle,path,compress=3);return bundle

def train():
 verify();assert not (OUT/'congelacion.json').exists()
 f=base.load('train');choices=pd.read_csv(base.OUT/'selecciones.csv').set_index('fold').leaves
 frozen=json.loads((base.OUT/'congelacion.json').read_text());preds=[];models=[]
 f[['source_row','participant','split','y']].to_csv(OUT/'filas_train.csv.gz',index=False)
 for name,cols in plan()['groups'].items():
  for fold in plan()['folds']:
   train=f[f.participant.isin(fold['fit'])].reset_index(drop=True);val=f[f.participant.isin(fold['evaluation'])].reset_index(drop=True)
   assert set(train.participant).isdisjoint(val.participant)
   for ctx in CONTEXTS:
    path=OUT/'modelos'/f'{name}_fold{fold["fold"]}_ctx{ctx}.joblib'
    b=fit(train,cols,ctx,choices.loc[fold['fold']],path);prob=base.predict(b,val)
    np.testing.assert_allclose(prob,base.predict(joblib.load(path),val),atol=1e-12)
    preds.append(val[['source_row','participant','y']].assign(prob=prob,modality=name,context=ctx,fold=fold['fold'],split='oof_train'))
    pd.concat(preds).to_csv(OUT/'predicciones_oof_unimodales.csv.gz',index=False)
    models.append(dict(path=str(path.relative_to(ROOT)),sha256=digest(path),modality=name,context=ctx,fold=fold['fold']))
    print('Modelo guardado',name,'fold',fold['fold'],'contexto',ctx,flush=True)
  for ctx in CONTEXTS:
   path=OUT/'modelos'/f'{name}_final_ctx{ctx}.joblib';fit(f,cols,ctx,frozen['leaves'],path)
   models.append(dict(path=str(path.relative_to(ROOT)),sha256=digest(path),modality=name,context=ctx,fold='final'))
   print('Final guardado',name,ctx,flush=True)
 verify();write(OUT/'congelacion.json',dict(created_utc=pd.Timestamp.now(tz='UTC').isoformat(),protocol_sha256=digest(OUT/'protocolo.json'),models=models,validation_evaluated=False,test_evaluated=False,final_leaves=frozen['leaves']))
 print('CONGELADOS',len(models),'modelos nuevos',flush=True)

def evaluate():
 verify();freeze=json.loads((OUT/'congelacion.json').read_text());assert not (OUT/'predicciones_externas_unimodales.csv.gz').exists()
 assert digest(OUT/'protocolo.json')==freeze['protocol_sha256'];preds=[]
 for split in ['validation','test']:
  f=base.load(split)
  for meta in freeze['models']:
   if meta['fold']!='final':continue
   path=ROOT/meta['path'];assert digest(path)==meta['sha256'];b=joblib.load(path)
   assert set(f.participant).isdisjoint(b['fit_people'])
   preds.append(f[['source_row','participant','y']].assign(prob=base.predict(b,f),modality=meta['modality'],context=meta['context'],split=split))
 pd.concat(preds).to_csv(OUT/'predicciones_externas_unimodales.csv.gz',index=False)
 report()

def predictions():
 return pd.concat([pd.read_csv(OUT/'predicciones_oof_unimodales.csv.gz'),pd.read_csv(OUT/'predicciones_externas_unimodales.csv.gz'),pd.read_csv(base.OUT/'predicciones_oof.csv.gz').assign(modality='full'),pd.read_csv(base.OUT/'predicciones_externas.csv.gz').assign(modality='full')],ignore_index=True)

def report():
 pred=predictions();people=[];summary=[];contrasts=[]
 for (split,mod,ctx,person),g in pred.groupby(['split','modality','context','participant']):
  people.append(dict(split=split,modality=mod,context=ctx,participant=person,windows=len(g),auc=roc_auc_score(g.y,g.prob)))
 people=pd.DataFrame(people);people.to_csv(OUT/'metricas_personas.csv',index=False)
 for (split,mod,ctx),g in people.groupby(['split','modality','context']):
  mean,lo,hi=ci(g.auc);summary.append(dict(split=split,modality=mod,context=ctx,auc=mean,low=lo,high=hi))
 for (split,ctx),g in people.groupby(['split','context']):
  wide=g.pivot(index='participant',columns='modality',values='auc')
  for mod in MODALITIES:
   d=wide.full-wide[mod];mean,lo,hi=ci(d);contrasts.append(dict(split=split,context=ctx,contrast=f'full_minus_{mod}',delta=mean,low=lo,high=hi,improved=int((d>0).sum()),people=len(d)))
 pd.DataFrame(summary).to_csv(OUT/'metricas.csv',index=False);pd.DataFrame(contrasts).to_csv(OUT/'contrastes_fusion.csv',index=False)
 lines=['# Ablación controlada de modalidades — activación V2','','HistGradientBoosting, mismos hiperparámetros por fold/contexto que la fusión completa, elegidos previamente solo en train. EEG, mirada y pupila por separado frente a fusión temprana completa. Modelos completos reutilizados sin cambios. 45 ajustes OOF y nueve modelos finales nuevos, congelados antes de evaluación externa.','','| Evaluación | Modalidad | Contexto máximo | AUC | IC descriptivo 95% |','|---|---|---|---|---|']
 for r in summary:lines.append(f"| {r['split']} | {r['modality']} | {r['context']} | {r['auc']:.4f} | [{r['low']:.4f}; {r['high']:.4f}] |")
 lines+=['','## Contrastes de fusión','','| Evaluación | Contexto | Fusión menos | ΔAUC | IC descriptivo 95% | Personas mejoran |','|---|---|---|---|---|---|']
 for r in contrasts:lines.append(f"| {r['split']} | {r['context']} | {r['contrast']} | {r['delta']:+.4f} | [{r['low']:.4f}; {r['high']:.4f}] | {r['improved']}/{r['people']} |")
 lines+=['','## Límites','Resultados exploratorios sobre particiones consultadas históricamente. Todos los nueve contrastes por partición se reportan; intervalos descriptivos sin corrección múltiple. No se escoge modalidad ni contexto para reajustar usando test. Esta es una ablación con configuración controlada, no una búsqueda del máximo alcanzable por cada modalidad. Solo evalúa fusión temprana, no tardía/intermedia ni todas las parejas.','', 'Mismas filas y etiquetas V2: 7.028 train, 2.584 validation y 2.184 test. Las ausencias de predictores se imputan desde train; no se eliminan filas por modalidad. Pseudoetiquetas GSR offline no equivalen a activación psicológica validada. Contexto32 es un límite máximo: no hay 32 ventanas consecutivas retenidas en validation/test. Consultar ../activacion_v2_comparacion_final_01-11-2026/INFORME.md para interpretación temporal y cobertura.']
 (OUT/'INFORME.md').write_text('\n'.join(lines)+'\n');print(pd.DataFrame(summary).query("split == 'test'").to_string(index=False),flush=True)


def audit():
 verify();freeze=json.loads((OUT/'congelacion.json').read_text());assert digest(OUT/'protocolo.json')==freeze['protocol_sha256']
 pred=predictions();metrics=pd.read_csv(OUT/'metricas_personas.csv');checks=0;rows={}
 choices=pd.read_csv(base.OUT/'selecciones.csv').set_index('fold').leaves
 train=base.load('train');frames={'oof_train':train,'validation':base.load('validation'),'test':base.load('test')}
 for split,f in frames.items():
  rows[split]=len(f)
  for (mod,ctx),g in pred[pred.split.eq(split)].groupby(['modality','context']):
   assert not g.source_row.duplicated().any() and g.prob.between(0,1).all()
   a=g.sort_values('source_row');b=f.sort_values('source_row')
   np.testing.assert_array_equal(a.source_row,b.source_row);np.testing.assert_array_equal(a.y,b.y)
   np.testing.assert_array_equal(a.participant,b.participant)
 for meta in freeze['models']:
  path=ROOT/meta['path'];assert digest(path)==meta['sha256'];bundle=joblib.load(path)
  assert bundle['cols']==plan()['groups'][meta['modality']]
  assert bundle['model'].get_params()['max_leaf_nodes']==bundle['leaves']
  for key,value in plan()['params'].items():assert bundle['model'].get_params()[key]==value
  if meta['fold']=='final':
   assert bundle['leaves']==freeze['final_leaves'];assert set(bundle['fit_people'])==set(train.participant)
   evals=[('validation',frames['validation']),('test',frames['test'])]
  else:
   fold=next(v for v in plan()['folds'] if v['fold']==meta['fold']);assert bundle['leaves']==choices.loc[meta['fold']]
   assert set(bundle['fit_people'])==set(fold['fit'])
   evals=[('oof_train',train[train.participant.isin(fold['evaluation'])].reset_index(drop=True))]
  for split,f in evals:
   assert set(f.participant).isdisjoint(bundle['fit_people'])
   saved=pred[pred.split.eq(split)&pred.modality.eq(meta['modality'])&pred.context.eq(meta['context'])].set_index('source_row').loc[f.source_row]
   np.testing.assert_allclose(base.predict(bundle,f),saved.prob,rtol=1e-12,atol=1e-12);checks+=1
 for row in metrics.itertuples():
  f=pred[pred.split.eq(row.split)&pred.modality.eq(row.modality)&pred.context.eq(row.context)&pred.participant.eq(row.participant)]
  assert abs(roc_auc_score(f.y,f.prob)-row.auc)<1e-12
 # Recompute paired intervals directly from saved predictions, not exported summaries.
 for row in pd.read_csv(OUT/'contrastes_fusion.csv').itertuples():
  mod=row.contrast.removeprefix('full_minus_');d=[]
  sub=pred[pred.split.eq(row.split)&pred.context.eq(row.context)]
  for person,g in sub.groupby('participant'):
   full=g[g.modality.eq('full')];single=g[g.modality.eq(mod)]
   d.append(roc_auc_score(full.y,full.prob)-roc_auc_score(single.y,single.prob))
  np.testing.assert_allclose(ci(d),[row.delta,row.low,row.high],rtol=1e-12,atol=1e-12)
 write(OUT/'auditoria.json',dict(passed=True,new_models=len(freeze['models']),prediction_reload_checks=checks,participant_auc_verified=len(metrics),paired_contrasts_verified=27,same_rows_labels=True,rows=rows,full_models_unchanged=True,source_hashes_unchanged=True))
 print('AUDITORÍA APROBADA',checks,'recargas;',len(metrics),'AUC; 27 contrastes',flush=True)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['prepare','train','evaluate','report','audit']);args=parser.parse_args()
 with threadpool_limits(limits=2):globals()[args.phase]()
