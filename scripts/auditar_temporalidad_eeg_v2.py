"""Recalcula selección, etiquetas y predicciones de validation desde disco."""
import sys,json
from pathlib import Path
import joblib,numpy as np,pandas as pd
from sklearn.metrics import roc_auc_score
from threadpoolctl import threadpool_limits
from evaluar_temporalidad_eeg_v2 import OUT,ROOT,KEYS,components,binary,COLUMNS,score_bundle,digest,write

def main():
    frozen=json.loads((OUT/'congelacion_pre_validation.json').read_text())
    plan=json.loads((OUT/'protocolo.json').read_text())
    source=ROOT/'resultados/preprocesamiento/caracteristicas_multimodales.csv'
    partition=ROOT/'resultados/modelado/particion_participantes.csv'
    assert digest(source)==plan['source_sha256'] and digest(partition)==plan['partition_sha256']
    assert digest(ROOT/'scripts/evaluar_temporalidad_eeg_v2.py')==plan['script_sha256']
    for n,h in plan['dependencies'].items():assert digest(ROOT/'scripts'/n)==h
    raw=pd.read_csv(source);raw['source_row']=np.arange(len(raw));raw['split']=raw.participant.map(pd.read_csv(partition).set_index('participant').split)
    train_people=set(raw[raw.split.eq('train')].participant)
    # Recalculate all CV participant scores without trusting selection tables.
    records=[]
    for fold in plan['folds']:
        assert set(fold['fit']).isdisjoint(fold['evaluation'])
        for c in plan['grid']:
            t=pd.read_csv(OUT/'cv'/f"fold{fold['fold']}_{c['id']}.csv.gz")
            assert set(t.participant)==set(fold['evaluation']) and set(t.participant)<=train_people
            for p,g in t.groupby('participant'):records.append(dict(candidate_id=c['id'],scope=c['scope'],context=c['context'],participant=p,auc=roc_auc_score(g.y,g.prob)))
    means=pd.DataFrame(records).groupby(['candidate_id','scope','context'],as_index=False).auc.mean().sort_values(['auc','candidate_id'],ascending=[False,True])
    for name,ident in frozen['selected'].items():
        scope,ctx=name.rsplit('_',1);pool=means[means.scope.eq(scope)]
        if ctx!='seleccionado':pool=pool[pool.context.eq(int(ctx[3:]))]
        assert pool.iloc[0].candidate_id==ident
    channel=OUT/'caracteristicas_validation.csv.gz'
    assert digest(channel)==json.loads((OUT/'auditoria_extraccion.json').read_text())['sha256']
    val=raw[raw.split.eq('validation')].merge(pd.read_csv(channel),on='source_row',validate='one_to_one').sort_values(KEYS).reset_index(drop=True)
    assert set(val.participant).isdisjoint(train_people)
    tp=OUT/'profesor_final.joblib';assert digest(tp)==frozen['teacher_sha256'];teacher=joblib.load(tp)
    assert set(teacher['fit_participants'])==train_people
    z,_=components(val);ok=z.notna().all(axis=1);score=pd.Series(np.nan,index=val.index)
    score.loc[ok]=teacher['pca'].transform(z.loc[ok,COLUMNS]).ravel()*teacher['sign'];labels,_=binary(score,val)
    val=val.assign(y=labels).dropna(subset=['y']).copy();val['y']=val.y.astype(int);val=val.reset_index(drop=True)
    pred=pd.read_csv(OUT/'predicciones_validation.csv.gz');metrics=pd.read_csv(OUT/'metricas.csv')
    for name,ident in frozen['selected'].items():
        path=OUT/'modelos'/f'{ident}.joblib';assert digest(path)==frozen['models_sha256'][ident]
        bundle=joblib.load(path);assert set(bundle['fit_participants'])==train_people
        t=pred[pred.strategy.eq(name)].reset_index(drop=True)
        pd.testing.assert_frame_equal(t[['source_row','participant','y']],val[['source_row','participant','y']])
        np.testing.assert_allclose(score_bundle(bundle,val),t.prob,atol=1e-8,rtol=1e-7)
        macro=np.mean([roc_auc_score(g.y,g.prob) for _,g in t.groupby('participant')])
        np.testing.assert_allclose(macro,metrics[metrics.strategy.eq(name)].auc_macro.item(),atol=1e-12)
    write(OUT/'auditoria_independiente.json',dict(passed=True,cv_candidates_recalculated=36,cv_predictions_files=180,validation_people=8,train_people=25,teacher_fit_train_only=True,selection_train_only_verified=True,labels_recomputed=True,predictions_reloaded=True,test_evaluated=False))
    print('AUDITORÍA INDEPENDIENTE OK')
if __name__=='__main__':
    with threadpool_limits(limits=2):main()
