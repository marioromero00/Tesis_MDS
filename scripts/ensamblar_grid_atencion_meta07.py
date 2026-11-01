"""Pesos de mezcla seleccionados internamente entre dos rondas, sin ajuste OOF."""
import json
import numpy as np,pandas as pd
from pathlib import Path
from sklearn.metrics import roc_auc_score
from grid_atencion_meta07 import BASE,SCOPES,choose,macro_auc,summarize,digest,write

OUT=BASE/'ensamble_rondas12'

def merge(a,b):
    if a.source_row.duplicated().any() or b.source_row.duplicated().any():raise ValueError('Filas duplicadas')
    c=a.merge(b,on=['source_row','participant','y'],suffixes=('_r1','_r2'),validate='one_to_one')
    if len(c)!=len(a) or len(c)!=len(b):raise ValueError('Etiquetas o filas no coinciden')
    return c

def best_weight(table,weights):
    trials=[]
    for weight in weights:
        score=weight*table.prob_r1.to_numpy()+(1-weight)*table.prob_r2.to_numpy()
        trials.append(dict(weight_round1=weight,auc_inner=macro_auc(table,score)))
    return sorted(trials,key=lambda r:(-r['auc_inner'],abs(r['weight_round1']-.5),r['weight_round1']))[0],trials

def main():
    prior=json.loads((OUT/'protocolo_previo.json').read_text())
    protocols=[json.loads((BASE/f'ronda{i}'/'protocolo.json').read_text()) for i in [1,2]]
    assert protocols[0]['folds']==protocols[1]['folds']
    for i in [1,2]:assert json.loads((BASE/f'ronda{i}'/'auditoria_independiente.json').read_text())['passed']
    write(OUT/'protocolo.json',dict(prior,round1_protocol_sha256=digest(BASE/'ronda1/protocolo.json'),round2_protocol_sha256=digest(BASE/'ronda2/protocolo.json'),source_code_sha256=digest(Path(__file__))))
    tables=[];selections=[]
    for fold in protocols[0]['folds']:
        by_scope={};choices=[]
        for scope in SCOPES:
            selected=[];inner=[];outer=[]
            for i in [1,2]:
                root=BASE/f'ronda{i}'
                task=json.loads((root/'tareas'/f"fold{fold['fold']}_{scope}.json").read_text())
                selected.append(task['selected'])
                inner.append(pd.read_csv(root/'trials'/f"fold{fold['fold']}_{task['selected']['candidate']['id']}.csv.gz"))
                outer.append(pd.read_csv(root/'predicciones'/f"fold{fold['fold']}_{scope}.csv.gz"))
            iv=merge(*inner);val=merge(*outer)
            best,attempts=best_weight(iv,prior['weights_round1']);w=best['weight_round1']
            table=val[['source_row','participant','y']].copy().assign(prob=w*val.prob_r1+(1-w)*val.prob_r2,strategy=scope,fold=fold['fold'],candidate_id=f'ensemble_w{w}')
            tables.append(table);by_scope[scope]=table
            record=dict(fold=fold['fold'],strategy=scope,selected=best,trials=attempts,base_candidates=[s['candidate'] for s in selected])
            selections.append(record);choices.append(record)
        best=sorted(choices,key=lambda r:(-r['selected']['auc_inner'],r['strategy']))[0]
        joint=by_scope[best['strategy']].copy();joint['strategy']='seleccion_interna';tables.append(joint)
        selections.append(dict(best,strategy='seleccion_interna',selected_scope=best['strategy']))
    write(OUT/'selecciones.json',selections);pd.DataFrame(selections).to_csv(OUT/'selecciones.csv',index=False)
    metrics=summarize(OUT,tables,'1+2')
    # Re-read serialized artifacts and verify independent reconstruction of all mixtures.
    predictions=pd.read_csv(OUT/'predicciones_oof.csv.gz')
    for record in selections:
        scope=record.get('selected_scope',record['strategy']);fold=record['fold'];a=pd.read_csv(BASE/'ronda1/predicciones'/f'fold{fold}_{scope}.csv.gz');b=pd.read_csv(BASE/'ronda2/predicciones'/f'fold{fold}_{scope}.csv.gz')
        pair=merge(a,b);w=record['selected']['weight_round1'];observed=predictions[predictions.fold.eq(fold)&predictions.strategy.eq(record['strategy'])]
        np.testing.assert_array_equal(observed.source_row,pair.source_row);np.testing.assert_array_equal(observed.y,pair.y)
        np.testing.assert_allclose(observed.prob,w*pair.prob_r1+(1-w)*pair.prob_r2,atol=1e-12)
    for strategy,g in predictions.groupby('strategy'):
        assert len(g)==13498 and not g.source_row.duplicated().any() and g.participant.nunique()==25
        auc=np.mean([roc_auc_score(t.y,t.prob) for _,t in g.groupby('participant')])
        np.testing.assert_allclose(auc,metrics[metrics.strategy.eq(strategy)].auc_macro.iloc[0],atol=1e-12)
    write(OUT/'auditoria_independiente.json',dict(passed=True,predictions_verified=len(predictions),mixtures_reconstructed=True,base_audits_passed=True,target_07_exceeded_by_strategy={r.strategy:bool(r.auc_macro>.7) for _,r in metrics.iterrows()}))
    report=OUT/'INFORME.md';text=report.read_text();text=text.replace('Parámetros completos','Parámetros completos')
    text+='\n\nEsta corrida combina predicciones de los grids de boosting y CatBoost. Para cada fold/escenario se probaron pesos 0/0,25/0,5/0,75/1 usando solamente las cuatro personas internas. No hay modelos adicionales entrenados; se reutilizan los modelos externos auditados de ambas rondas. Ver selecciones.json y protocolo_previo.json.\n'
    report.write_text(text)
if __name__=='__main__':main()
