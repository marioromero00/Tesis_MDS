"""Estudio controlado de entradas; no selecciona variantes por el resultado externo."""
import json
from datetime import datetime,timezone
import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits
from ablacion_pca_core import variants,design,feature_cache,inputs,fit,predict
from entrenar_hiperparametros import load_train
from hiperparametros_core import TARGET
from temporales_core import ROOT,CLASSES,digest,write_json,metric_record,individual_scores

OUT=ROOT/'resultados/ablacion_pca_12-09-2026'
SOURCE=ROOT/'resultados/multiescala_11-09-2026_completa'


def main():
    OUT.mkdir(exist_ok=False); (OUT/'modelos').mkdir()
    train=load_train(); previous=json.loads((SOURCE/'protocolo.json').read_text()); choices=json.loads((SOURCE/'selecciones.json').read_text())
    references=[v for v in choices if v['scope']=='ridge']; definitions=variants()
    source_predictions=pd.read_csv(SOURCE/'predicciones_oof.csv.gz')
    protocol=dict(created_utc=datetime.now(timezone.utc).isoformat(),target=TARGET,folds=previous['folds'],references=references,variants=definitions,
        seed=20260911,primary='three leave-one-modality-out contrasts and current_no_smooth; remaining fixed contrasts secondary',
        selection='no new hyperparameter selection; fixed reference settings for paired retraining',
        pca='after training-only median imputation with missing indicators and standardization; full SVD; no whitening; 80/90/95 percent and full rotation control',
        interpretation='conditional predictive contribution, not causal effect; correlated inputs can compensate; original normalization offline',
        sources={str(p.relative_to(ROOT)):digest(p) for p in [ROOT/'scripts/ablacion_pca_core.py',ROOT/'scripts/entrenar_ablacion_pca.py',
            ROOT/'scripts/multiescala_core.py',ROOT/'scripts/persistencia_core.py',ROOT/'scripts/temporales_core.py',ROOT/'scripts/avanzados_core.py',
            ROOT/'scripts/entrenar_hiperparametros.py',ROOT/'scripts/hiperparametros_core.py',ROOT/'scripts/optimizar_historial.py',
            SOURCE/'protocolo.json',SOURCE/'selecciones.json',SOURCE/'verificacion.json',SOURCE/'predicciones_oof.csv.gz',
            ROOT/'resultados/modelado/dataset_modelado.csv',ROOT/'resultados/modelado/particion_participantes.csv']},
        validation_evaluated=False,test_evaluated=False,scope='exploratory adaptive training cohort; no new claim about attention')
    write_json(OUT/'protocolo.json',protocol)
    catalog=[]; rows=[]; metrics=[]; people=[]; pca_rows=[]; loadings=[]; max_error=0.
    for fold in protocol['folds']:
        f=train.loc[train.participant.isin(fold['fit'])].reset_index(drop=True); v=train.loc[train.participant.isin(fold['evaluation'])].reset_index(drop=True)
        assert set(f.participant).isdisjoint(v.participant)
        fit_cache=feature_cache(f); val_cache=feature_cache(v); ref=next(r for r in references if r['fold']==fold['fold'])
        # Separate construction on unlabeled frame verifies feature-cache independence.
        fresh=feature_cache(v.drop(columns=[TARGET,'arousal_score_6s']))
        for k in fresh: np.testing.assert_array_equal(fresh[k],val_cache[k])
        for definition in definitions:
            spec=design(ref,definition); bundle=fit(inputs(fit_cache,spec),f,spec)
            identity=dict(model_id=f'fold{fold["fold"]}_{definition["variant"]}',fold=fold['fold'],variant=definition['variant'],kind=definition['kind'])
            path=OUT/'modelos'/f'{identity["model_id"]}.joblib'; joblib.dump(bundle,path,compress=3)
            scores=predict(bundle,v,val_cache); restored=joblib.load(path); reloaded=predict(restored,v,fresh)
            np.testing.assert_allclose(scores,reloaded,rtol=1e-12,atol=1e-12)
            np.testing.assert_array_equal(scores.argmax(axis=1),reloaded.argmax(axis=1)); max_error=max(max_error,float(np.max(abs(scores-reloaded))))
            if definition['variant']=='reference':
                old=source_predictions.loc[source_predictions.fold.eq(fold['fold'])&source_predictions.scope.eq('ridge')&source_predictions.seed.eq(20260911)]
                np.testing.assert_array_equal(v.source_row,old.source_row)
                np.testing.assert_allclose(scores,old[['prob_'+c for c in CLASSES]],rtol=1e-12,atol=1e-12)
                np.testing.assert_array_equal(np.asarray(CLASSES)[scores.argmax(axis=1)],old.prediction)
                reference_scores=scores.copy()
            if definition['variant']=='pca_full':
                np.testing.assert_allclose(scores,reference_scores,rtol=1e-9,atol=1e-9)
                np.testing.assert_array_equal(scores.argmax(axis=1),reference_scores.argmax(axis=1))
            estimator=bundle['model']; transformed_names=estimator['prep'].get_feature_names_out(spec['input_names'])
            if definition['kind']=='pca':
                pca=estimator['pca']; cumulative=np.cumsum(pca.explained_variance_ratio_)
                for component,ratio in enumerate(pca.explained_variance_ratio_):
                    pca_rows.append(dict(**identity,component=component+1,dimensions_before=len(transformed_names),dimensions_after=pca.n_components_,
                        explained_variance_ratio=float(ratio),cumulative_variance=float(cumulative[component])))
                    for name,weight in zip(transformed_names,pca.components_[component]):
                        loadings.append(dict(**identity,component=component+1,feature=name,weight=float(weight)))
            pred=np.asarray(CLASSES)[scores.argmax(axis=1)]; p=v[['source_row','participant','window_start_utc']].copy(); p['true']=v[TARGET].to_numpy(); p['prediction']=pred
            for k,value in identity.items(): p[k]=value
            for i,c in enumerate(CLASSES): p['prob_'+c]=scores[:,i]
            rows.append(p); metrics.append(dict(**identity,**metric_record(v,TARGET,pred,'classification')))
            people.extend(dict(**identity,participant=p,score=s) for p,s in individual_scores(v,TARGET,pred,'classification').items())
            catalog.append(dict(**identity,path=path.relative_to(OUT).as_posix(),sha256=digest(path),spec=spec,
                train_participants=fold['fit'],evaluation_participants=fold['evaluation'],dimensions_raw=len(spec['indices']),dimensions_imputed=len(transformed_names)))
        write_json(OUT/'catalogo_modelos.json',catalog)
        print(f'Ablacion/PCA fold {fold["fold"]}/5: {len(definitions)} modelos guardados y recargados',flush=True)
    pd.concat(rows).to_csv(OUT/'predicciones_oof.csv.gz',index=False,compression='gzip')
    pd.DataFrame(metrics).to_csv(OUT/'metricas_folds.csv',index=False); pd.DataFrame(people).to_csv(OUT/'metricas_participantes.csv',index=False)
    pd.DataFrame(pca_rows).to_csv(OUT/'pca_varianza.csv',index=False); pd.DataFrame(loadings).to_csv(OUT/'pca_cargas.csv.gz',index=False,compression='gzip')
    write_json(OUT/'completo.json',dict(models=len(catalog),predictions=sum(map(len,rows)),variants=len(definitions),max_reload_error=max_error,
        protocol_sha256=digest(OUT/'protocolo.json'),completed_utc=datetime.now(timezone.utc).isoformat(),validation_evaluated=False,test_evaluated=False))
    print(pd.DataFrame(people).groupby('variant').score.mean().sort_values(ascending=False).to_string(),flush=True)


if __name__=='__main__':
    with threadpool_limits(limits=2): main()
