"""Diagnóstico train y selección anidada acotada de activación binaria."""
import json,joblib
from pathlib import Path
import numpy as np,pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from threadpoolctl import threadpool_limits
from comparacion_comun_binaria import representation
from temporales_core import preprocessor,history_indices
from evaluar_temporalidad_eeg_v2 import ci
from atencion_binaria import ROOT,digest,write
from reconstruir_profesor_atencion_binaria import KEYS
OUT=ROOT/'resultados/activacion_diagnostico_nested_30-10-2026'
COMMON=ROOT/'resultados/comparacion_comun_binaria_30-10-2026'

def model(c):
 if c['family']=='logistica':return LogisticRegression(C=c['value'],max_iter=2000,random_state=20261101)
 return HistGradientBoostingClassifier(max_leaf_nodes=c['value'],max_iter=300,l2_regularization=10,learning_rate=.05,min_samples_leaf=30,early_stopping=False,random_state=20261101)
def weights(f):
 w=1/(f.groupby(['participant','y']).y.transform('size')*f.groupby('participant').y.transform('nunique'));return w/w.mean()
def auc(f,p):return np.mean([roc_auc_score(f.iloc[ix].y,np.asarray(p)[ix]) for ix in f.groupby('participant').indices.values()])

def main():
 OUT.mkdir(exist_ok=False);(OUT/'modelos').mkdir()
 common=json.loads((COMMON/'protocolo.json').read_text());groups=common['groups']['activacion'];cols=sum(groups.values(),[])
 source=ROOT/'resultados/preprocesamiento/caracteristicas_multimodales.csv';raw=pd.read_csv(source);raw['source_row']=np.arange(len(raw))
 partition=ROOT/'resultados/modelado/particion_participantes.csv';parts=pd.read_csv(partition).set_index('participant').split
 raw['split']=raw.participant.map(parts);raw=raw[raw.split.eq('train')].copy()
 spatial=ROOT/'resultados/eeg_por_canal_v2_29-10-2026/caracteristicas_eeg_por_canal.csv.gz'
 s=pd.read_csv(spatial);channel=[c for c in cols if c.startswith(('eegch','eegsp'))]
 raw=raw.merge(s[['source_row']+channel],on='source_row',validate='one_to_one')
 legacy=ROOT/'resultados/modelado/dataset_modelado.csv';old=pd.read_csv(legacy);old=old[old.split.eq('train')]
 raw=raw.merge(old[KEYS+['arousal_score_6s','arousal_score_2s']],on=KEYS,validate='one_to_one').sort_values(KEYS).reset_index(drop=True)
 labels=pd.read_csv(COMMON/'etiquetas_activacion.csv.gz');labels=labels[labels.split.eq('train')]
 f=raw.merge(labels[['source_row','y']],on='source_row',validate='one_to_one').sort_values(KEYS).reset_index(drop=True)
 folds=json.loads((ROOT/'resultados/profesor_binario_reconstruido_29-10-2026/protocolo.json').read_text())['folds']
 grid=[dict(id=f'{fam}_{v}',family=fam,value=v) for fam,values in [('logistica',[.1,1.]),('histboost',[7,15])] for v in values]
 write(OUT/'protocolo.json',dict(created_utc=pd.Timestamp.now(tz='UTC').isoformat(),source_sha256=digest(source),partition_sha256=digest(partition),script_sha256=digest(Path(__file__)),labels_sha256=digest(COMMON/'etiquetas_activacion.csv.gz'),spatial_sha256=digest(spatial),features=cols,grid=grid,contexts=[1,8,32],folds=folds,selection='4 candidates per context independently, inner grouped 16/4 people, outer 20/5 people; no selection across contexts using outer scores',metric='mean participant ROC-AUC',train_only=True,labels='unchanged binary arousal score6s above personal median',limits='exploratory reused train; no validation/test reads for evaluation; inherited offline GSR teacher'))
 diagnostic=[]
 for person,g in raw.groupby('participant'):
  a=g.arousal_score_6s;b=g.arousal_score_2s
  r=dict(participant=person,windows=len(g),labelled=int(f.participant.eq(person).sum()),score6s_std=float(a.std()),score6s_unique=int(a.nunique()),score2s_6s_spearman=float(a.corr(b,method='spearman')),positive_rate=float(f[f.participant.eq(person)].y.mean()))
  for c in ['eeg_coverage','gsr_coverage','eeg_window_valid','gsr_window_valid','eegsp_usable_channels']:
   if c in g:r[c+'_mean']=float(g[c].mean())
  for name,features in groups.items():r[name+'_missing_fraction']=float(g[features].isna().to_numpy().mean())
  diagnostic.append(r)
 pd.DataFrame(diagnostic).to_csv(OUT/'diagnostico_personas.csv',index=False)
 history=[]
 for ctx in [8,32]:
  _,length=history_indices(f,ctx)
  for person,ix in f.groupby('participant').indices.items():history.append(dict(participant=person,context=ctx,mean_history=float(length[ix].mean()),full_history_fraction=float((length[ix]==ctx).mean())))
 pd.DataFrame(history).to_csv(OUT/'cobertura_historial.csv',index=False)
 trials=[];predictions=[];selection=[]
 for fold in folds:
  ii=f[f.participant.isin(fold['inner_fit'])].reset_index(drop=True);iv=f[f.participant.isin(fold['inner_validation'])].reset_index(drop=True)
  fit=f[f.participant.isin(fold['fit'])].reset_index(drop=True);val=f[f.participant.isin(fold['evaluation'])].reset_index(drop=True)
  assert set(ii.participant).isdisjoint(iv.participant) and set(fit.participant).isdisjoint(val.participant)
  pre=preprocessor().fit(ii[cols]);outer=preprocessor().fit(fit[cols])
  for ctx in [1,8,32]:
   a=representation(pre,ii,cols,ctx);b=representation(pre,iv,cols,ctx);local=[]
   for c in grid:
    est=model(c);est.fit(a,ii.y,sample_weight=weights(ii));prob=est.predict_proba(b)[:,1]
    record=dict(fold=fold['fold'],context=ctx,candidate=c['id'],auc_inner=float(auc(iv,prob)));trials.append(record);local.append(record)
    print('inner',fold['fold'],ctx,c['id'],round(record['auc_inner'],4),flush=True)
   chosen=sorted(local,key=lambda r:(-r['auc_inner'],r['candidate']))[0];selection.append(chosen);c=next(c for c in grid if c['id']==chosen['candidate'])
   est=model(c);est.fit(representation(outer,fit,cols,ctx),fit.y,sample_weight=weights(fit));path=OUT/'modelos'/f"fold{fold['fold']}_ctx{ctx}.joblib"
   joblib.dump(dict(model=est,prep=outer,cols=cols,context=ctx,fit_people=fold['fit'],candidate=c),path,compress=3)
   prob=est.predict_proba(representation(outer,val,cols,ctx))[:,1];loaded=joblib.load(path);np.testing.assert_allclose(prob,loaded['model'].predict_proba(representation(loaded['prep'],val,cols,ctx))[:,1],atol=1e-12)
   predictions.append(val[['source_row','participant','y']].assign(prob=prob,context=ctx,fold=fold['fold']))
   pd.concat(predictions).to_csv(OUT/'predicciones_oof.csv.gz',index=False);pd.DataFrame(trials).to_csv(OUT/'busqueda.csv',index=False)
   print('outer terminado',fold['fold'],ctx,flush=True)
 pd.DataFrame(selection).to_csv(OUT/'selecciones.csv',index=False);pred=pd.read_csv(OUT/'predicciones_oof.csv.gz');people=[];summ=[];contr=[]
 for (ctx,person),g in pred.groupby(['context','participant']):people.append(dict(context=ctx,participant=person,auc=roc_auc_score(g.y,g.prob)))
 people=pd.DataFrame(people);people.to_csv(OUT/'metricas_personas.csv',index=False)
 for ctx,g in people.groupby('context'):
  mean,lo,hi=ci(g.auc);summ.append(dict(context=ctx,auc=mean,low=lo,high=hi))
 wide=people.pivot(index='participant',columns='context',values='auc')
 for ctx in [8,32]:
  d=wide[ctx]-wide[1];mean,lo,hi=ci(d);contr.append(dict(context=ctx,delta=mean,low=lo,high=hi,improved=int((d>0).sum())))
 pd.DataFrame(summ).to_csv(OUT/'metricas.csv',index=False);pd.DataFrame(contr).to_csv(OUT/'contrastes.csv',index=False)
 for ctx,g in pred.groupby('context'):
  assert not g.source_row.duplicated().any() and len(g)==len(f)
  a=g.sort_values('source_row');b=f.sort_values('source_row');np.testing.assert_array_equal(a.source_row,b.source_row);np.testing.assert_array_equal(a.y,b.y)
 write(OUT/'auditoria.json',dict(passed=True,inner_fits=len(trials),outer_models=15,people=25,labels_unchanged=True,coverage_verified=True,reload_verified=True,validation_evaluated=False,test_evaluated=False))
 lines=['# Activación: diagnóstico y búsqueda anidada en train','','Las etiquetas binarias y las modalidades EEG/Eye/Pupil se conservan. Cuatro configuraciones por contexto (1/8/32 ventanas), seleccionadas con personas internas disjuntas de las externas. AUC promediada por persona; intervalos descriptivos bootstrap. Búsqueda exploratoria sobre train reutilizado; no es una confirmación independiente.','', '## AUC OOF','','| Contexto | AUC | IC 95 % |','|---|---:|---:|']
 for r in summ:lines.append(f'| {r["context"]} | {r["auc"]:.4f} | [{r["low"]:.4f}; {r["high"]:.4f}] |')
 lines+=['','## Temporal menos estático','','| Contexto | ΔAUC | IC 95 % | Personas mejoran |','|---|---:|---:|---:|']
 for r in contr:lines.append(f'| {r["context"]} | {r["delta"]:+.4f} | [{r["low"]:.4f}; {r["high"]:.4f}] | {r["improved"]}/25 |')
 lines+=['','Diagnóstico por persona: diagnostico_personas.csv; cobertura real del historial: cobertura_historial.csv. La concordancia 2s/6s es sensibilidad al suavizado del profesor; no valida activación psicológica. No se ajustaron offsets ni se eliminaron personas según rendimiento. Verificar cobertura y timestamps detecta problemas documentables, pero no prueba alineamiento fisiológico externo.']
 (OUT/'INFORME.md').write_text('\n'.join(lines));print(pd.DataFrame(summ).to_string(index=False),flush=True);print(pd.DataFrame(contr).to_string(index=False),flush=True);print('COMPLETO',flush=True)
if __name__=='__main__':
 with threadpool_limits(limits=2):main()
