"""Verifica selecciones, metricas y artefactos de las iteraciones segunda y tercera."""
import json
import numpy as np
import pandas as pd
from temporales_core import ROOT,CLASSES,digest,write_json,metric_record,individual_scores
from optimizar_historial import OUT as BASE,TARGET


def main():
    base_protocol=json.loads((BASE/'protocolo.json').read_text(encoding='utf-8'))
    results=[]
    for directory,expected in [('segunda_iteracion',20),('tercera_iteracion',30)]:
        out=BASE/directory
        catalog=json.loads((out/'catalogo_modelos.json').read_text(encoding='utf-8'))
        protocol=json.loads((out/'protocolo.json').read_text(encoding='utf-8'))
        verified=json.loads((out/'verificacion.json').read_text(encoding='utf-8'))
        source='combinar_historial.py' if directory=='segunda_iteracion' else 'fusion_modalidades.py'
        assert digest(ROOT/'scripts'/source)==protocol['source_sha256']==verified['source_sha256']
        assert len(catalog)==expected and len({m['model_id'] for m in catalog})==expected
        preds=pd.read_csv(out/'predicciones_oof.csv.gz')
        folds=pd.read_csv(out/'metricas_folds.csv').set_index('model_id')
        people=pd.read_csv(out/'metricas_participantes.csv').set_index(['model_id','participant'])
        for meta in catalog:
            fold=base_protocol['folds'][meta['fold']-1]
            assert set(fold['fit']).isdisjoint(fold['evaluation'])
            assert meta['train_participants']==fold['fit'] and meta['evaluation_participants']==fold['evaluation']
            assert digest(out/meta['path'])==meta['sha256'] and meta['reload_verified']
            p=preds.loc[preds.model_id.eq(meta['model_id'])].reset_index(drop=True)
            assert set(p.participant)==set(fold['evaluation'])
            prob=p[['prob_'+c for c in CLASSES]].to_numpy()
            assert np.isfinite(prob).all() and (prob>=0).all()
            np.testing.assert_allclose(prob.sum(axis=1),1,atol=1e-12)
            np.testing.assert_array_equal(np.asarray(CLASSES)[prob.argmax(axis=1)],p.prediction)
            metric=metric_record(p,TARGET,p.prediction.to_numpy(),'classification')
            for k in ['macro_score','balanced_accuracy','macro_f1']:
                np.testing.assert_allclose(metric[k],folds.loc[meta['model_id'],k],rtol=1e-12,atol=1e-12)
            for person,score in individual_scores(p,TARGET,p.prediction.to_numpy(),'classification').items():
                np.testing.assert_allclose(score,people.loc[(meta['model_id'],person),'score'],rtol=1e-12,atol=1e-12)
        choices=json.loads((out/'selecciones.json').read_text(encoding='utf-8'))
        assert digest(out/'selecciones.json')==verified['selection_sha256']
        if directory=='segunda_iteracion':
            inner=pd.read_csv(out/'predicciones_internas.csv.gz')
            search=pd.read_csv(out/'busqueda_pesos.csv')
            for (fold,part),p in inner.groupby(['fold','inner']):
                p=p.reset_index(drop=True)
                assert set(p.participant).issubset(base_protocol['folds'][fold-1]['fit'])
                b=p[['base_'+c for c in CLASSES]].to_numpy(); t=p[['temporal_'+c for c in CLASSES]].to_numpy()
                for weight in protocol['weights']:
                    pred=np.asarray(CLASSES)[((1-weight)*b+weight*t).argmax(axis=1)]
                    score=metric_record(p,TARGET,pred,'classification')['macro_score']
                    row=search.loc[search.fold.eq(fold)&search.inner.eq(part)&search.weight.eq(weight)].iloc[0]
                    np.testing.assert_allclose(score,row.score,rtol=1e-12,atol=1e-12)
            for choice in choices:
                group=search.loc[search.fold.eq(choice['fold'])].groupby('weight',as_index=False).score.mean()
                best=group.sort_values(['score','weight'],ascending=[False,True]).iloc[0]
                assert best.weight==choice['weight']
            internal=75
        else:
            search=pd.read_csv(out/'busqueda_interna.csv'); assert len(search)==720
            for row in search.itertuples():
                fit=set(row.fit_participants.split('|')); val=set(row.evaluation_participants.split('|'))
                assert fit.isdisjoint(val) and fit|val==set(base_protocol['folds'][row.fold-1]['fit'])
            for choice in choices:
                group=search.loc[search.fold.eq(choice['fold'])].groupby(['representation','estimator','smoothing'],as_index=False).score.mean()
                current=group.representation.str.endswith('__current')&group.smoothing.eq(1)
                if choice['scope']=='current': group=group.loc[current]
                if choice['scope']=='temporal': group=group.loc[~current]
                best=group.sort_values(['score','representation','estimator','smoothing'],ascending=[False,True,True,True]).iloc[0]
                assert [choice[k] for k in ['representation','estimator','smoothing']]==[best.representation,best.estimator,int(best.smoothing)]
            internal=720
        results.append(dict(iteration=directory,models=expected,predictions=len(preds),selections=len(choices),internal_scores=internal,
            catalog_sha256=digest(out/'catalogo_modelos.json'),predictions_sha256=digest(out/'predicciones_oof.csv.gz')))
    write_json(BASE/'auditoria_iteraciones.json',dict(results=results,source_sha256=digest(__file__),validation_evaluated=False,test_evaluated=False))
    print(json.dumps(results,indent=2))


if __name__=='__main__': main()
