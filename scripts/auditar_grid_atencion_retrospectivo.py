"""Audita seleccion por grupos y la meta sobre AUC OOF de 25 participantes."""
import argparse,json
import numpy as np,pandas as pd,joblib
from sklearn.metrics import roc_auc_score
from grid_atencion_retrospectivo import ROOT,BASE,OLD,SCOPES,digest,choose,score_bundle,macro_auc

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--round',type=int,required=True);args=parser.parse_args();out=BASE/f'ronda{args.round}'
    plan=json.loads((out/'protocolo.json').read_text());p=pd.read_csv(out/'predicciones_oof.csv.gz');metrics=pd.read_csv(out/'metricas.csv')
    source=ROOT/'resultados/preprocesamiento/caracteristicas_multimodales.csv';raw=pd.read_csv(source);raw['source_row']=np.arange(len(raw));raw['split']=raw.participant.map(pd.read_csv(ROOT/'resultados/modelado/particion_participantes.csv').set_index('participant').split)
    assert digest(source)==plan['source_sha256']
    assert digest(ROOT/'scripts/grid_atencion_retrospectivo.py')==plan['script_sha256']
    assert digest(ROOT/'scripts/reconstruir_profesor_atencion_binaria.py')==plan['teacher_source_sha256']
    labels=pd.read_csv(OLD/'pca/etiquetas_profesor_oof.csv.gz').set_index('source_row')
    total_trials=0;models=0
    for fold in plan['folds']:
        assert set(fold['fit']).isdisjoint(fold['evaluation'])
        assert set(fold['inner_fit']).isdisjoint(fold['inner_validation'])
        assert set(fold['inner_fit'])|set(fold['inner_validation'])==set(fold['fit'])
        trials=[]
        for path in (out/'trials').glob(f"fold{fold['fold']}_*.json"):
            record=json.loads(path.read_text());tpath=path.with_suffix('.csv.gz');assert digest(tpath)==record['prediction_sha256']
            t=pd.read_csv(tpath);assert set(t.participant)==set(fold['inner_validation'])
            assert record['inner_fit']==fold['inner_fit'];assert record['inner_validation']==fold['inner_validation']
            np.testing.assert_allclose(macro_auc(t,t.prob),record['auc_inner'],atol=1e-12)
            trials.append(record);total_trials+=1
        assert len(trials)==len(plan['grid'])
        for scope in SCOPES:
            record=json.loads((out/'tareas'/f"fold{fold['fold']}_{scope}.json").read_text());selected=choose([t for t in trials if t['candidate']['scope']==scope])
            assert selected==record['selected']
            modelpath=out/'modelos'/f"fold{fold['fold']}_{scope}.joblib";predpath=out/'predicciones'/f"fold{fold['fold']}_{scope}.csv.gz"
            assert digest(modelpath)==record['model_sha256'];assert digest(predpath)==record['prediction_sha256']
            bundle=joblib.load(modelpath);assert set(bundle['fit_participants'])==set(fold['fit']);assert bundle['candidate']==selected['candidate'];assert bundle['features']==plan['features']
            t=pd.read_csv(predpath);ref=labels.loc[t.source_row];np.testing.assert_array_equal(t.y,ref.y);np.testing.assert_array_equal(t.participant,ref.participant)
            assert set(t.participant)==set(fold['evaluation'])
            val=raw.set_index('source_row',drop=False).loc[t.source_row].reset_index(drop=True);assert val.split.eq('train').all()
            np.testing.assert_allclose(score_bundle(bundle,val),t.prob,atol=1e-8,rtol=1e-7);models+=1
        joint=choose(trials);scope=joint['candidate']['scope']
        a=p[p.fold.eq(fold['fold'])&p.strategy.eq(scope)];b=p[p.fold.eq(fold['fold'])&p.strategy.eq('seleccion_interna')]
        np.testing.assert_array_equal(a.source_row,b.source_row);np.testing.assert_array_equal(a.prob,b.prob)
    for strategy,g in p.groupby('strategy'):
        assert len(g)==13498 and not g.source_row.duplicated().any() and g.participant.nunique()==25
        assert np.isfinite(g.prob).all() and g.prob.between(0,1).all()
        np.testing.assert_array_equal(g.y,labels.loc[g.source_row].y)
        auc=np.mean([roc_auc_score(t.y,t.prob) for _,t in g.groupby('participant')])
        np.testing.assert_allclose(auc,metrics[metrics.strategy.eq(strategy)].auc_macro.iloc[0],atol=1e-12)
    result=dict(passed=True,inner_trials=total_trials,outer_models_reloaded=models,predictions_verified=len(p),labels_unchanged=True,participants=25,fold_groups_disjoint=True,inner_selection_verified=True,
        target_07_exceeded_by_strategy={r.strategy:bool(r.auc_macro>.7) for _,r in metrics.iterrows()},offline_calibration_identified=True,uses_future_input=True,scenario='retrospective offline only')
    (out/'auditoria_independiente.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
