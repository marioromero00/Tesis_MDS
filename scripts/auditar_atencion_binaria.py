import json,sys,hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
root=Path(__file__).resolve().parents[1]; out=root/'resultados/atencion_binaria_29-10-2026'
p=pd.read_csv(out/'predicciones_oof.csv.gz'); d=pd.read_csv(root/'resultados/modelado/dataset_modelado.csv'); plan=json.loads((out/'protocolo.json').read_text())
rows=d.iloc[p.source_row.to_numpy()]
assert rows.split.eq('train').all()
np.testing.assert_array_equal(rows.attention_label_equal.eq('alto').astype(int),p.y)
np.testing.assert_array_equal(rows.participant,p.participant)
for fold in plan['folds']:
    assert set(fold['fit']).isdisjoint(fold['evaluation'])
    assert set(p[p.fold.eq(fold['fold'])].participant)==set(fold['evaluation'])
for path in (out/'predicciones').glob('*.json'):
    a=json.loads(path.read_text()); name=path.stem
    assert hashlib.sha256((out/'modelos'/f'{name}.joblib').read_bytes()).hexdigest()==a['model_sha256']
    assert hashlib.sha256((out/'predicciones'/f'{name}.csv.gz').read_bytes()).hexdigest()==a['predictions_sha256']
avg=p.groupby(['family','mode','source_row','participant','y'],as_index=False).prob.mean()
m=pd.read_csv(out/'metricas.csv')
for _,r in m.iterrows():
    t=avg[avg.family.eq(r.family)&avg['mode'].eq(r['mode'])]
    auc=np.mean([roc_auc_score(g.y,g.prob) for _,g in t.groupby('participant')])
    np.testing.assert_allclose(auc,r.auc_macro,atol=1e-12)
labels=d.loc[d.split.eq('train')&d.attention_label_equal.notna(),['participant','recording','segment_id','stimulus','window_start_utc','attention_label_equal']].copy()
labels.insert(0,'source_row',labels.index)
labels['attention_binary']=labels.attention_label_equal.eq('alto').astype(int)
labels.to_csv(out/'etiquetas_binarias_train.csv.gz',index=False)
(out/'auditoria_independiente.json').write_text(json.dumps({'passed':True,'predictions_checked':len(p),'train_only':True,'labels_and_participants_match_source':True,'folds_disjoint':True,'artifact_hashes_verified':True,'auc_recomputed':True},indent=2))
print('Auditoria independiente aprobada:',len(p),'predicciones; AUC, etiquetas, folds y hashes verificados.')
