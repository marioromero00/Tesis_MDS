"""Audita desde disco la selección, particiones, etiquetas y predicciones guardadas."""
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from threadpoolctl import threadpool_limits
from activacion_v2_comparacion_final import OUT, ROOT, LABELS, plan, load, predict
from atencion_binaria import digest, write

def main():
 p=plan();frozen=json.loads((OUT/'congelacion.json').read_text())
 assert digest(OUT/'protocolo.json')==frozen['protocol_sha256']
 assert digest(OUT/'busqueda_interna.csv')==frozen['search_sha256']
 trials=pd.read_csv(OUT/'busqueda_interna.csv');selections=pd.read_csv(OUT/'selecciones.csv')
 labels=pd.read_csv(LABELS).set_index('source_row');checked=0
 for row in trials.itertuples():
  f=pd.read_csv(OUT/f'interna_fold{row.fold}_ctx{row.context}_h{row.leaves}.csv.gz')
  fold=next(v for v in p['folds'] if v['fold']==row.fold)
  assert set(f.participant)==set(fold['inner_validation'])
  assert set(f.participant).isdisjoint(fold['inner_fit'])
  np.testing.assert_array_equal(f.y,labels.loc[f.source_row].activation_binary_v2)
  actual=np.mean([roc_auc_score(g.y,g.prob) for _,g in f.groupby('participant')])
  assert abs(actual-row.auc)<1e-12
  checked+=1
 for fold in p['folds']:
  choice=int(trials[trials.fold.eq(fold['fold'])].groupby('leaves').auc.mean().sort_index().idxmax())
  assert choice==selections[selections.fold.eq(fold['fold'])].leaves.item()
 assert int(trials.groupby('leaves').auc.mean().sort_index().idxmax())==frozen['leaves']
 oof=pd.read_csv(OUT/'predicciones_oof.csv.gz');external=pd.read_csv(OUT/'predicciones_externas.csv.gz')
 models=0
 with threadpool_limits(limits=2):
  train=load('train')
  for fold in p['folds']:
   f=train[train.participant.isin(fold['evaluation'])].reset_index(drop=True)
   for ctx in p['contexts']:
    bundle=joblib.load(OUT/'modelos'/f'fold{fold["fold"]}_ctx{ctx}.joblib')
    assert set(bundle['fit_people'])==set(fold['fit']) and set(f.participant).isdisjoint(bundle['fit_people'])
    assert bundle['leaves']==selections[selections.fold.eq(fold['fold'])].leaves.item()
    saved=oof[oof.fold.eq(fold['fold'])&oof.context.eq(ctx)].set_index('source_row').loc[f.source_row]
    np.testing.assert_allclose(predict(bundle,f),saved.prob,atol=1e-12,rtol=1e-12);models+=1
  for split in ['validation','test']:
   f=load(split)
   for ctx in p['contexts']:
    meta=frozen['models'][str(ctx)];assert digest(ROOT/meta['path'])==meta['sha256']
    bundle=joblib.load(ROOT/meta['path']);assert bundle['leaves']==frozen['leaves']
    assert set(bundle['fit_people'])==set(train.participant) and set(f.participant).isdisjoint(bundle['fit_people'])
    saved=external[external.split.eq(split)&external.context.eq(ctx)].set_index('source_row').loc[f.source_row]
    np.testing.assert_array_equal(saved.y,f.y)
    np.testing.assert_allclose(predict(bundle,f),saved.prob,atol=1e-12,rtol=1e-12);models+=1
 metrics=pd.read_csv(OUT/'metricas_personas.csv');pred=pd.concat([oof,external]);auc_count=0
 for r in metrics.itertuples():
  f=pred[pred.split.eq(r.split)&pred.context.eq(r.context)&pred.participant.eq(r.participant)]
  assert abs(roc_auc_score(f.y,f.prob)-r.auc)<1e-12;auc_count+=1
 for path,h in p['inputs'].items():assert digest(ROOT/path)==h
 write(OUT/'auditoria_desde_disco.json',dict(passed=True,inner_selections_recomputed=checked,participant_auc_recomputed=auc_count,model_prediction_checks=models,all_labels_verified=True,final_models_frozen=True,inputs_unchanged=True))
 print('AUDITORÍA APROBADA:',checked,'scores internos;',auc_count,'AUC por persona;',models,'recargas predictivas')

if __name__=='__main__':main()
