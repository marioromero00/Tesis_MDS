"""Recalculo independiente de ablaciones, PCA y contribuciones pareadas."""
import json
from datetime import datetime,timezone
import joblib
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from threadpoolctl import threadpool_limits
from ablacion_pca_core import feature_cache,inputs,design,predict
from entrenar_hiperparametros import load_train
from hiperparametros_core import TARGET
from temporales_core import ROOT,CLASSES,digest,write_json,preprocessor,metric_record,individual_scores
from informe_control_historial import bootstrap

OUT=ROOT/'resultados/ablacion_pca_12-09-2026'


def read(p): return json.loads(p.read_text(encoding='utf-8'))


def main():
    protocol=read(OUT/'protocolo.json'); complete=read(OUT/'completo.json')
    assert digest(OUT/'protocolo.json')==complete['protocol_sha256']
    for path,sha in protocol['sources'].items(): assert digest(ROOT/path)==sha,path
    train=load_train(); catalog=read(OUT/'catalogo_modelos.json'); predictions=pd.read_csv(OUT/'predicciones_oof.csv.gz')
    folds=pd.read_csv(OUT/'metricas_folds.csv').set_index('model_id'); people=pd.read_csv(OUT/'metricas_participantes.csv').set_index(['model_id','participant'])
    variance=pd.read_csv(OUT/'pca_varianza.csv'); loadings=pd.read_csv(OUT/'pca_cargas.csv.gz'); pca_count=0; reference_scores={}
    for fold in protocol['folds']:
        fitting=train.loc[train.participant.isin(fold['fit'])].reset_index(drop=True)
        val=train.loc[train.participant.isin(fold['evaluation'])].reset_index(drop=True)
        assert set(fitting.participant).isdisjoint(val.participant)
        fit_cache=feature_cache(fitting); val_cache=feature_cache(val.drop(columns=[TARGET,'arousal_score_6s']))
        reference=next(v for v in protocol['references'] if v['fold']==fold['fold'])
        items=[v for v in catalog if v['fold']==fold['fold']]
        assert len(items)==len(protocol['variants'])
        for item in items:
            path=OUT/item['path']; assert digest(path)==item['sha256']; bundle=joblib.load(path)
            definition=next(d for d in protocol['variants'] if d['variant']==item['variant'])
            expected=design(reference,definition); assert bundle['spec']==item['spec']==expected
            assert item['train_participants']==fold['fit'] and item['evaluation_participants']==fold['evaluation']
            x=inputs(fit_cache,expected); prep=preprocessor().fit(x); original=bundle['model']['prep']
            np.testing.assert_array_equal(prep['imputer'].statistics_,original['imputer'].statistics_)
            for attr in ['mean_','scale_']: np.testing.assert_allclose(getattr(prep['scale'],attr),getattr(original['scale'],attr),atol=1e-12,rtol=1e-12)
            saved=predictions.loc[predictions.model_id.eq(item['model_id'])].reset_index(drop=True)
            np.testing.assert_array_equal(saved.source_row,val.source_row); np.testing.assert_array_equal(saved.true,val[TARGET])
            scores=predict(bundle,val.drop(columns=[TARGET,'arousal_score_6s']),val_cache)
            np.testing.assert_allclose(scores,saved[['prob_'+c for c in CLASSES]],atol=1e-12,rtol=1e-12)
            pred=np.asarray(CLASSES)[scores.argmax(axis=1)]; np.testing.assert_array_equal(pred,saved.prediction)
            if item['variant']=='reference': reference_scores[fold['fold']]=scores
            if item['variant']=='pca_full':
                np.testing.assert_allclose(scores,reference_scores[fold['fold']],atol=1e-9,rtol=1e-9)
                np.testing.assert_array_equal(pred,np.asarray(CLASSES)[reference_scores[fold['fold']].argmax(axis=1)])
            for key,value in metric_record(val,TARGET,pred,'classification').items(): np.testing.assert_allclose(value,folds.loc[item['model_id'],key],atol=1e-12,rtol=1e-12)
            for person,value in individual_scores(val,TARGET,pred,'classification').items(): np.testing.assert_allclose(value,people.loc[(item['model_id'],person),'score'],atol=1e-12,rtol=1e-12)
            if item['kind']=='pca':
                original=bundle['model']['pca']; n=definition['pca']; pca=PCA(n_components=None if n=='full' else n,svd_solver='full',whiten=False).fit(prep.transform(x))
                assert original.n_samples_==len(fitting) and original.n_components_==pca.n_components_
                np.testing.assert_allclose(original.mean_,pca.mean_,atol=1e-12,rtol=1e-12)
                np.testing.assert_allclose(original.components_.T@original.components_,pca.components_.T@pca.components_,atol=1e-9,rtol=1e-9)
                np.testing.assert_allclose(original.explained_variance_ratio_,pca.explained_variance_ratio_,atol=1e-12,rtol=1e-12)
                v=variance.loc[variance.model_id.eq(item['model_id'])].sort_values('component')
                np.testing.assert_allclose(v.explained_variance_ratio,original.explained_variance_ratio_,atol=1e-12,rtol=1e-12)
                np.testing.assert_allclose(v.cumulative_variance,np.cumsum(original.explained_variance_ratio_),atol=1e-12,rtol=1e-12)
                names=prep.get_feature_names_out(expected['input_names'])
                weights=loadings.loc[loadings.model_id.eq(item['model_id'])].pivot(index='component',columns='feature',values='weight').reindex(columns=names)
                np.testing.assert_allclose(weights,original.components_,atol=1e-12,rtol=1e-12); pca_count+=1
        print(f'Auditoria ablacion/PCA fold {fold["fold"]}: modelos, transformaciones y metricas verificados',flush=True)
    people=people.reset_index(); ref=people.loc[people.variant.eq('reference')].set_index('participant').score
    summary=[]; diagnosis=[]; differences=[]
    for definition in protocol['variants']:
        name=definition['variant']; g=predictions.loc[predictions.variant.eq(name)].reset_index(drop=True)
        assert len(g)==len(train) and g.source_row.is_unique and set(g.source_row)==set(train.source_row)
        metrics=metric_record(g,'true',g.prediction.to_numpy(),'classification')
        values=people.loc[people.variant.eq(name)].set_index('participant').score
        assert set(values.index)==set(ref.index)
        loss=ref-values; lo,hi=bootstrap(loss)
        summary.append(dict(variant=name,kind=definition['kind'],**metrics,loss_vs_reference=float(loss.mean()),ci_low=lo,ci_high=hi,
            people_hurt_by_removal=int((loss>1e-12).sum()),ties=int((loss.abs()<=1e-12).sum())))
        differences.extend(dict(variant=name,participant=p,loss=float(v)) for p,v in loss.items())
        for c in CLASSES:
            diagnosis.append(dict(variant=name,label=c,recall=float(g.loc[g.true.eq(c),'prediction'].eq(c).mean()),predicted_fraction=float(g.prediction.eq(c).mean())))
    summary=pd.DataFrame(summary); summary.to_csv(OUT/'resumen_ablaciones.csv',index=False)
    pd.DataFrame(diagnosis).to_csv(OUT/'diagnostico_clases.csv',index=False); pd.DataFrame(differences).to_csv(OUT/'diferencias_participantes.csv',index=False)
    ranking=summary.loc[summary.kind.eq('variable')].sort_values('loss_vs_reference',ascending=False).copy()
    ranking['feature']=ranking.variant.str.removeprefix('drop_'); ranking.to_csv(OUT/'ranking_variables.csv',index=False)
    pca=variance.groupby(['fold','variant'],as_index=False).agg(dimensions_before=('dimensions_before','first'),dimensions_after=('dimensions_after','first'),retained_variance=('cumulative_variance','max'))
    pca.to_csv(OUT/'resumen_pca.csv',index=False)
    verification=dict(models_reloaded=len(catalog),predictions_verified=len(predictions),preprocessors_refitted=len(catalog),pca_refitted=pca_count,
        pca_loadings_verified=len(loadings),fold_metrics_verified=len(folds),participant_metrics_verified=len(people),
        protocol_sha256=digest(OUT/'protocolo.json'),catalog_sha256=digest(OUT/'catalogo_modelos.json'),predictions_sha256=digest(OUT/'predicciones_oof.csv.gz'),
        audit_script_sha256=digest(__file__),summary_sha256=digest(OUT/'resumen_ablaciones.csv'),completed_utc=datetime.now(timezone.utc).isoformat(),
        validation_evaluated=False,test_evaluated=False)
    write_json(OUT/'verificacion.json',verification)
    print(summary.loc[~summary.kind.eq('variable'),['variant','macro_score','loss_vs_reference','ci_low','ci_high']].to_string(index=False),flush=True)
    print(ranking[['feature','loss_vs_reference','ci_low','ci_high']].head(10).to_string(index=False),flush=True)


if __name__=='__main__':
    with threadpool_limits(limits=2): main()
