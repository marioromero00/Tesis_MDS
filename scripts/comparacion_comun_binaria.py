"""Comparación exploratoria común de temporalidad y ablaciones binarias."""
import json,joblib
from pathlib import Path
import numpy as np,pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from threadpoolctl import threadpool_limits
from temporales_core import preprocessor,history_indices,sequence_array
from baselines_estaticos import EEG,GSR,EYE,PUPIL
from evaluar_test_temporalidad_eeg_v2 import label_with_teacher
from evaluar_temporalidad_eeg_v2 import ci
from atencion_binaria import ROOT,digest,write
from reconstruir_profesor_atencion_binaria import KEYS
from eeg_por_canal_v2 import FEATURES as CHANNELS
OUT=ROOT/'resultados/comparacion_comun_binaria_30-10-2026'
BASE=ROOT/'resultados/temporalidad_eeg_v2_validacion_29-10-2026'

def representation(prep,frame,cols,context):
 z=prep.transform(frame[cols]).astype('float32')
 if context==1:return z
 ix,l=history_indices(frame,context);x=sequence_array(z,ix);mask=np.arange(context)[None,:]<l[:,None]
 mean=x.sum(axis=1)/l[:,None];var=(((x-mean[:,None,:])**2)*mask[:,:,None]).sum(axis=1)/l[:,None]
 return np.column_stack([z,mean,np.sqrt(np.maximum(var,0))])

def main():
 OUT.mkdir(exist_ok=False);(OUT/'modelos').mkdir()
 rawpath=ROOT/'resultados/preprocesamiento/caracteristicas_multimodales.csv';data=pd.read_csv(rawpath);data['source_row']=np.arange(len(data))
 data['split']=data.participant.map(pd.read_csv(ROOT/'resultados/modelado/particion_participantes.csv').set_index('participant').split)
 paths=[ROOT/'resultados/eeg_por_canal_v2_29-10-2026/caracteristicas_eeg_por_canal.csv.gz',BASE/'caracteristicas_validation.csv.gz',ROOT/'resultados/temporalidad_eeg_v2_test_29-10-2026/caracteristicas_test.csv.gz']
 spatial=pd.concat([pd.read_csv(p)[['source_row']+CHANNELS] for p in paths]);assert not spatial.source_row.duplicated().any()
 data=data[data.split.isin(['train','validation','test'])].merge(spatial,on='source_row',validate='one_to_one')
 legacy=ROOT/'resultados/modelado/dataset_modelado.csv';scores=pd.read_csv(legacy)[KEYS+['arousal_score_6s']]
 data=data.merge(scores,on=KEYS,validate='one_to_one').sort_values(KEYS).reset_index(drop=True)
 groups={'atencion':{'EEG':EEG+CHANNELS,'GSR':GSR},'activacion':{'EEG':EEG+CHANNELS,'Eye':EYE,'Pupil':PUPIL}}
 params=dict(max_leaf_nodes=15,max_iter=300,l2_regularization=10.,learning_rate=.05,min_samples_leaf=30,early_stopping=False,random_state=20261101)
 write(OUT/'protocolo.json',dict(created_utc=pd.Timestamp.now(tz='UTC').isoformat(),script_sha256=digest(Path(__file__)),source_sha256=digest(rawpath),legacy_sha256=digest(legacy),spatial_sha256={str(p):digest(p) for p in paths},groups=groups,params=params,contexts=[1,32],attention='frozen PCA teacher from full train',activation='new binary task: arousal_score_6s above participant session median, ties zero, missing excluded',metric='mean participant ROC-AUC',training='fixed parameters inherited from attention, no search or selection on validation/test',representation='current standardized features plus historical mean and SD of all features for context32',scope='exploratory; validation/test previously consulted; aggregation not sequence-order modeling; all ablations are inductive preprocessing; teacher labels offline'))
 teacher=joblib.load(BASE/'profesor_final.joblib');predictions=[];manifest=[]
 for task,modalities in groups.items():
  frame=data.copy()
  if task=='atencion':y,_=label_with_teacher(frame,teacher)
  else:
   score=frame.arousal_score_6s;med=score.groupby(frame.participant).transform('median');y=(score>med).astype(float).where(score.notna())
  frame=frame.assign(y=y).dropna(subset=['y']).copy();frame['y']=frame.y.astype(int);frame=frame.reset_index(drop=True)
  frame[['source_row','participant','split','y']].to_csv(OUT/f'etiquetas_{task}.csv.gz',index=False)
  subsets={'full':sum(modalities.values(),[]),**modalities}
  if task=='activacion':
   subsets.update({f'sin_{name}':sum([v for k,v in modalities.items() if k!=name],[]) for name in modalities})
  fit=frame[frame.split.eq('train')].reset_index(drop=True)
  for subset,cols in subsets.items():
   forbidden=EYE+PUPIL if task=='atencion' else GSR
   assert not set(cols)&set(forbidden)
   prep=preprocessor().fit(fit[cols]);n=fit.groupby(['participant','y']).y.transform('size').to_numpy();k=fit.groupby('participant').y.transform('nunique').to_numpy();weights=1/(n*k);weights/=weights.mean()
   for context in [1,32]:
    ident=f'{task}_{subset}_ctx{context}';path=OUT/'modelos'/f'{ident}.joblib'
    model=HistGradientBoostingClassifier(**params);model.fit(representation(prep,fit,cols,context),fit.y,sample_weight=weights)
    joblib.dump(dict(model=model,prep=prep,cols=cols,context=context,fit_people=sorted(fit.participant.unique())),path,compress=3)
    manifest.append(dict(id=ident,sha256=digest(path),fit_people=sorted(fit.participant.unique())))
    for split in ['validation','test']:
     val=frame[frame.split.eq(split)].reset_index(drop=True);assert set(fit.participant).isdisjoint(val.participant)
     score=model.predict_proba(representation(prep,val,cols,context))[:,1];loaded=joblib.load(path)
     np.testing.assert_allclose(score,loaded['model'].predict_proba(representation(loaded['prep'],val,loaded['cols'],loaded['context']))[:,1],atol=1e-12)
     predictions.append(val[['source_row','participant','y']].assign(prob=score,task=task,subset=subset,context=context,split=split))
    print('Terminado',ident,flush=True)
    pd.concat(predictions).to_csv(OUT/'predicciones.csv.gz',index=False)
 write(OUT/'modelos.json',manifest)
 pred=pd.read_csv(OUT/'predicciones.csv.gz');people=[]
 for (task,subset,ctx,split,person),g in pred.groupby(['task','subset','context','split','participant']):
  assert g.y.nunique()==2
  people.append(dict(task=task,subset=subset,context=ctx,split=split,participant=person,auc=roc_auc_score(g.y,g.prob)))
 people=pd.DataFrame(people);people.to_csv(OUT/'metricas_personas.csv',index=False);summary=[];contrasts=[]
 for (task,subset,ctx,split),g in people.groupby(['task','subset','context','split']):
  mean,lo,hi=ci(g.auc);summary.append(dict(task=task,subset=subset,context=ctx,split=split,auc=mean,low=lo,high=hi))
 for (task,split),g in people.groupby(['task','split']):
  wide=g.pivot(index='participant',columns=['subset','context'],values='auc')
  for subset in g.subset.unique():
   a=wide[subset,32]-wide[subset,1];mean,lo,hi=ci(a);contrasts.append(dict(task=task,split=split,contrast=f'temporal_{subset}',delta=mean,low=lo,high=hi))
   if subset!='full':
    for ctx in [1,32]:
     a=wide['full',ctx]-wide[subset,ctx];mean,lo,hi=ci(a);contrasts.append(dict(task=task,split=split,contrast=f'full_menos_{subset}_ctx{ctx}',delta=mean,low=lo,high=hi))
 summary=pd.DataFrame(summary);con=pd.DataFrame(contrasts);summary.to_csv(OUT/'metricas.csv',index=False);con.to_csv(OUT/'contrastes.csv',index=False)
 write(OUT/'verificacion.json',dict(passed=True,models=len(manifest),reload_verified=True,group_separation=True,teacher_inputs_excluded=True))
 lines=['# Comparación común: atención, activación y ablaciones','', 'Análisis exploratorio binario. Activación se define antes de entrenar como score GSR de 6 s superior a la mediana personal; es una nueva tarea, no una reevaluación de la clasificación ternaria. Atención conserva el profesor PCA congelado. Mismos participantes, ventanas válidas dentro de cada tarea, parámetros y AUC por persona. Contextos 1/32: hasta 2/33 segundos. La representación temporal usa medias y desviaciones de todas las variables: no es idéntica al experimento anterior de atención. No se seleccionan modelos con test.','', '## Resultados test','','| Tarea | Modalidades | Contexto | AUC | IC 95 % |','|---|---|---:|---:|---:|']
 for r in summary[summary.split.eq('test')].itertuples():lines.append(f'| {r.task} | {r.subset} | {r.context} | {r.auc:.4f} | [{r.low:.4f}; {r.high:.4f}] |')
 lines+=['','## Contrastes test','','| Tarea | Contraste | ΔAUC | IC 95 % |','|---|---|---:|---:|']
 for r in con[con.split.eq('test')].itertuples():lines.append(f'| {r.task} | {r.contrast} | {r.delta:+.4f} | [{r.low:.4f}; {r.high:.4f}] |')
 lines+=['','Intervalos descriptivos bootstrap de participantes, 20.000 muestras; no corrigen comparaciones múltiples ni selección histórica. Test/validation fueron consultados anteriormente. Un intervalo que incluye cero no demuestra ausencia de efecto. La comparación es sobre pseudoetiquetas offline, no medición psicológica independiente. Las ablaciones miden contribución de modalidades en fusión temprana; no comparan fusión intermedia/tardía.']
 (OUT/'INFORME.md').write_text('\n'.join(lines));print('COMPLETO',flush=True)
if __name__=='__main__':
 with threadpool_limits(limits=2):main()
