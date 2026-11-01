"""Seleccion interna de mezclas uniformes, etiquetas fijas y fuentes sin futuro."""
import itertools,json
from pathlib import Path
import numpy as np,pandas as pd
from sklearn.metrics import roc_auc_score
from grid_atencion_meta07 import BASE,SCOPES,macro_auc,summarize,write,digest
OUT=BASE/'ensamble_ampliado'

def combine(tables):
    result=tables[0][['source_row','participant','y']].copy()
    for i,table in enumerate(tables):
        if table.source_row.duplicated().any():raise ValueError('Filas duplicadas')
        result=result.merge(table[['source_row','participant','y','prob']].rename(columns={'prob':f'p{i}'}),on=['source_row','participant','y'],validate='one_to_one')
    if any(len(t)!=len(result) for t in tables):raise ValueError('Filas/etiquetas no alineadas')
    return result

def select(table,n):
    trials=[]
    for size in [1,2,3]:
        for subset in itertools.combinations(range(n),size):
            score=table[[f'p{i}' for i in subset]].mean(axis=1)
            trials.append(dict(members=list(subset),auc_inner=macro_auc(table,score)))
    return sorted(trials,key=lambda r:(-r['auc_inner'],len(r['members']),r['members']))[0],trials

def main():
    prior=json.loads((OUT/'protocolo_previo.json').read_text());runs=prior['base_runs']
    protocols=[]
    for run in runs:
        protocols.append(json.loads((BASE/run/'protocolo.json').read_text()))
        assert json.loads((BASE/run/'auditoria_independiente.json').read_text())['passed']
    assert all(p['folds']==protocols[0]['folds'] for p in protocols)
    write(OUT/'protocolo.json',dict(prior,base_protocol_hashes={run:digest(BASE/run/'protocolo.json') for run in runs},source_sha256=digest(Path(__file__))))
    tables=[];selections=[]
    for fold in protocols[0]['folds']:
        scopes={};choices=[]
        for scope in SCOPES:
            inner=[];outer=[];base_candidates=[]
            for run in runs:
                out=BASE/run;task=json.loads((out/'tareas'/f"fold{fold['fold']}_{scope}.json").read_text());c=task['selected']['candidate'];base_candidates.append(c)
                inner.append(pd.read_csv(out/'trials'/f"fold{fold['fold']}_{c['id']}.csv.gz"));outer.append(pd.read_csv(out/'predicciones'/f"fold{fold['fold']}_{scope}.csv.gz"))
            iv=combine(inner);val=combine(outer);best,trials=select(iv,len(runs));members=best['members']
            t=val[['source_row','participant','y']].copy().assign(prob=val[[f'p{i}' for i in members]].mean(axis=1),strategy=scope,fold=fold['fold'],candidate_id='ensemble_'+','.join(map(str,members)))
            tables.append(t);scopes[scope]=t
            record=dict(fold=fold['fold'],strategy=scope,selected=best,trials=trials,base_candidates=base_candidates);selections.append(record);choices.append(record)
        best=sorted(choices,key=lambda r:(-r['selected']['auc_inner'],r['strategy']))[0]
        t=scopes[best['strategy']].copy();t['strategy']='seleccion_interna';tables.append(t);selections.append(dict(best,strategy='seleccion_interna',selected_scope=best['strategy']))
    write(OUT/'selecciones.json',selections);pd.DataFrame(selections).to_csv(OUT/'selecciones.csv',index=False)
    metrics=summarize(OUT,tables,'ensamble ampliado')
    serialized=pd.read_csv(OUT/'predicciones_oof.csv.gz')
    # Reconstruct from serialized base prediction files and redo internal subset selection.
    for recipe in selections:
        scope=recipe.get('selected_scope',recipe['strategy']);fold=recipe['fold'];inner=[];outer=[]
        for run in runs:
            out=BASE/run;task=json.loads((out/'tareas'/f'fold{fold}_{scope}.json').read_text());cid=task['selected']['candidate']['id']
            inner.append(pd.read_csv(out/'trials'/f'fold{fold}_{cid}.csv.gz'));outer.append(pd.read_csv(out/'predicciones'/f'fold{fold}_{scope}.csv.gz'))
        iv=combine(inner);best,_=select(iv,len(runs));assert best==recipe['selected']
        ref=combine(outer);members=best['members'];t=serialized[serialized.fold.eq(fold)&serialized.strategy.eq(recipe['strategy'])]
        np.testing.assert_array_equal(t.source_row,ref.source_row);np.testing.assert_array_equal(t.y,ref.y)
        np.testing.assert_allclose(t.prob,ref[[f'p{i}' for i in members]].mean(axis=1),atol=1e-12)
    for strategy,g in serialized.groupby('strategy'):
        assert len(g)==13498 and not g.source_row.duplicated().any() and g.participant.nunique()==25
        auc=np.mean([roc_auc_score(t.y,t.prob) for _,t in g.groupby('participant')]);np.testing.assert_allclose(auc,metrics[metrics.strategy.eq(strategy)].auc_macro.iloc[0],atol=1e-12)
    write(OUT/'auditoria_independiente.json',dict(passed=True,predictions_verified=len(serialized),inner_subset_selection_recomputed=True,base_audits_passed=True,uses_future_inputs=False,target_07_exceeded_by_strategy={r.strategy:bool(r.auc_macro>.7) for _,r in metrics.iterrows()}))
    path=OUT/'INFORME.md';s=path.read_text();s+='\n\nEnsamble de las seis corridas indicadas en protocolo_previo.json; para cada fold/escenario se probaron las 41 mezclas uniformes de 1/2/3 miembros sobre las personas internas. No se entrenan modelos adicionales y no se incorporan las entradas futuras del contraste retrospectivo. Los scores de regresores destilados llevan sigmoid sin calibración probabilística.\n';path.write_text(s)
if __name__=='__main__':main()
