"""Auditoria de umbrales ordinales y predicciones fuera de participante."""
import json
from datetime import datetime,timezone
import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits
from regresion_ordinal_core import feature_cache,raw_scores,decide,predict
from entrenar_hiperparametros import load_train
from hiperparametros_core import TARGET
from avanzados_core import sample_weights
from optimizar_historial import smooth
from temporales_core import ROOT,CLASSES,digest,write_json,preprocessor,metric_record,individual_scores
from informe_control_historial import bootstrap,markdown

OUT=ROOT/'resultados/regresion_ordinal_12-09-2026'


def read(p): return json.loads(p.read_text(encoding='utf-8'))


def main():
    train=load_train(); protocol=read(OUT/'protocolo.json'); complete=read(OUT/'completo.json')
    for path,sha in protocol['sources'].items(): assert digest(ROOT/path)==sha,path
    assert digest(OUT/'selecciones.json')==complete['selection_sha256']
    attempts=pd.read_csv(OUT/'intentos.csv'); expected=[]
    for item in read(OUT/'catalogo_interno.json'):
        path=OUT/item['path']; assert digest(path)==item['sha256']; fold=protocol['folds'][item['fold']-1]
        assert set(item['train_participants']).isdisjoint(item['evaluation_participants'])
        assert set(item['train_participants']+item['evaluation_participants'])==set(fold['fit'])
        with np.load(path) as saved:
            val=train.set_index('source_row',drop=False).loc[saved['source_row']].reset_index(drop=True)
            assert set(val.participant)==set(item['evaluation_participants']) and val.source_row.is_unique
            weight=sample_weights(val,'participant'); y=val[TARGET].to_numpy()
            for i,d in enumerate(protocol['grid']):
                raw=saved[f'm{i}']; assert np.isfinite(raw).all()
                smoothed={w:smooth(val,raw.reshape(-1,1),w)[:,0] for w in [1,16]}
                for w,lo,hi in protocol['rules']:
                    pred=np.asarray(CLASSES)[decide(val,smoothed[w],1,lo,hi)]
                    expected.append(dict(fold=item['fold'],inner=item['inner'],candidate_id=f'{d["base_id"]}_w{w}_l{lo}_h{hi}',score=float(np.average(pred==y,weights=weight))))
    keys=['fold','inner','candidate_id']; a=attempts.set_index(keys).sort_index(); b=pd.DataFrame(expected).set_index(keys).sort_index()
    assert a.index.equals(b.index); np.testing.assert_allclose(a.score,b.score,atol=1e-12,rtol=1e-12)
    selections=read(OUT/'selecciones.json')
    for choice in selections:
        scores=attempts.loc[attempts.fold.eq(choice['fold'])]
        if choice['scope']!='all': scores=scores.loc[scores.family.eq(choice['scope'])]
        winner=scores.groupby('candidate_id',as_index=False).score.mean().sort_values(['score','candidate_id'],ascending=[False,True]).iloc[0]
        assert winner.candidate_id==choice['candidate_id']; np.testing.assert_allclose(winner.score,choice['inner_score'],rtol=1e-12,atol=1e-12)
    events=[json.loads(line) for line in (OUT/'bitacora.jsonl').read_text().splitlines()]
    freeze=next(e for e in events if e['stage']=='selection_frozen')
    assert sum(e['stage']=='fit_completed' for e in events)==180
    assert all(e['utc']>freeze['utc'] for e in events if e['stage']=='outer_started')
    predictions=pd.read_csv(OUT/'predicciones_oof.csv.gz'); catalog=read(OUT/'catalogo_modelos.json')
    foldmetrics=pd.read_csv(OUT/'metricas_folds.csv').set_index('model_id'); people=pd.read_csv(OUT/'metricas_participantes.csv').set_index(['model_id','participant'])
    feature_bank={}
    for item in catalog:
        path=OUT/item['path']; assert digest(path)==item['sha256']; bundle=joblib.load(path); fold=protocol['folds'][item['fold']-1]
        assert item['train_participants']==fold['fit'] and item['evaluation_participants']==fold['evaluation']
        fit=train.loc[train.participant.isin(fold['fit'])].reset_index(drop=True); val=train.loc[train.participant.isin(fold['evaluation'])].reset_index(drop=True)
        if item['fold'] not in feature_bank:
            feature_bank[item['fold']]=(feature_cache(fit),feature_cache(val))
        fit_features,val_features=feature_bank[item['fold']]
        x=np.ascontiguousarray(fit_features[bundle['definition']['representation']]); prep=preprocessor().fit(x); old=bundle['model']['prep']
        np.testing.assert_array_equal(old['imputer'].statistics_,prep['imputer'].statistics_)
        for attr in ['mean_','scale_']: np.testing.assert_allclose(getattr(old['scale'],attr),getattr(prep['scale'],attr),rtol=1e-12,atol=1e-12)
        if bundle['definition']['family']=='rbf':
            kernel=bundle['model']['kernel']; np.testing.assert_allclose(kernel.components_,prep.transform(x)[kernel.component_indices_],rtol=1e-12,atol=1e-12)
        saved=predictions.loc[predictions.model_id.eq(item['model_id'])].reset_index(drop=True)
        np.testing.assert_array_equal(saved.source_row,val.source_row); np.testing.assert_array_equal(saved.true,val[TARGET])
        pred=predict(bundle,val.drop(columns=[TARGET,'arousal_score_6s'])); np.testing.assert_array_equal(pred,saved.prediction)
        np.testing.assert_allclose(raw_scores(bundle,val_features[bundle['definition']['representation']]),saved.ordinal_score,rtol=1e-12,atol=1e-12)
        for k,v in metric_record(val,TARGET,pred,'classification').items(): np.testing.assert_allclose(v,foldmetrics.loc[item['model_id'],k],rtol=1e-12,atol=1e-12)
        for person,v in individual_scores(val,TARGET,pred,'classification').items(): np.testing.assert_allclose(v,people.loc[(item['model_id'],person),'score'],rtol=1e-12,atol=1e-12)
    summary=[]; diagnosis=[]
    for scope,g in predictions.groupby('scope'):
        assert len(g)==len(train) and set(g.source_row)==set(train.source_row)
        summary.append(dict(scope=scope,**metric_record(g.reset_index(drop=True),'true',g.prediction.to_numpy(),'classification')))
        for c in CLASSES: diagnosis.append(dict(scope=scope,label=c,recall=float(g.loc[g.true.eq(c),'prediction'].eq(c).mean()),predicted_fraction=float(g.prediction.eq(c).mean())))
    summary=pd.DataFrame(summary); summary.to_csv(OUT/'resumen_oof.csv',index=False); pd.DataFrame(diagnosis).to_csv(OUT/'diagnostico_clases.csv',index=False)
    refpath=ROOT/'resultados/mezclas_ensambles_11-09-2026/metricas_participantes.csv'; ref=pd.read_csv(refpath); ref=ref.loc[ref.scope.eq('stack_weight_0.25')].groupby('participant').score.mean()
    gains=[]
    for scope in protocol['scopes']:
        values=people.reset_index().query('scope == @scope').groupby('participant').score.mean(); assert set(values.index)==set(ref.index)
        delta=values-ref; lo,hi=bootstrap(delta)
        gains.append(dict(scope=scope,mean_delta=float(delta.mean()),ci_low=lo,ci_high=hi,improved=int((delta>1e-12).sum()),tied=int((delta.abs()<=1e-12).sum())))
    gains=pd.DataFrame(gains); gains.to_csv(OUT/'ganancias_pareadas.csv',index=False)
    verification=dict(models_reloaded=len(catalog),predictions_verified=len(predictions),inner_scores_verified=len(expected),selections_verified=len(selections),
        preprocessors_refitted=len(catalog),fold_metrics_verified=len(foldmetrics),participant_metrics_verified=len(people),
        protocol_sha256=digest(OUT/'protocolo.json'),catalog_sha256=digest(OUT/'catalogo_modelos.json'),predictions_sha256=digest(OUT/'predicciones_oof.csv.gz'),
        audit_script_sha256=digest(__file__),reference_sha256=digest(refpath),completed_utc=datetime.now(timezone.utc).isoformat(),validation_evaluated=False,test_evaluated=False)
    write_json(OUT/'verificacion.json',verification)
    report=f'''# Regresion ordinal: 12-09-2026

Se evalua la misma etiqueta arousal_label_6s. Para entrenar se codifica bajo=-1,
medio=0 y alto=1; no se introduce GSR ni el score del profesor como predictor.
Se prueban Ridge (alpha=100), Nystroem RBF con Ridge (alpha=1, 192 componentes,
gamma=0,1/dimensiones), HistGradientBoostingRegressor y ExtraTreesRegressor.
Tres representaciones: actual, multiescala y relativa. Parametros completos en codigo
y fuentes congeladas en protocolo.json. No se cambia la etiqueta ni se elimina medio.

12 modelos base, 18 reglas por modelo (suavizado 1/16, umbral bajo -0,3/-0,1/-0,03,
alto 0,03/0,1/0,3). 180 ajustes internos y 3.240 puntuaciones. Seleccion conjunta all
como contraste principal, familias como secundarios. Se congelaron 25 elecciones antes
de los 25 ajustes externos; una semilla. Particiones: mismos cinco folds de train,
tres internos por persona, sin reevaluar validation/test originales.

## Resultados

{markdown(summary,list(summary.columns))}

Diferencias pareadas frente a la mezcla previa 0,3716:

{markdown(gains,list(gains.columns))}

IC descriptivos: 2.000 remuestreos pareados por persona; no corrigen busqueda adaptativa
ni dependencia de folds. Esta comparacion tampoco es confirmacion independiente.

La auditoria verifica {len(expected)} puntuaciones, 25 elecciones, 25 preprocesadores
reajustados, 25 modelos recargados, {len(predictions)} predicciones y metricas por fold
y persona. Scores y escalado con rtol=atol=1e-12; clases exactamente iguales.
La codificacion ordinal no garantiza distancias fisiologicas iguales entre clases.

Reproduccion: scripts/entrenar_regresion_ordinal.py en una copia sin directorio de salida
existente; scripts/auditar_regresion_ordinal.py para verificar. Carga: agregar scripts
al path, joblib.load y regresion_ordinal_core.predict(bundle, frame), ordenado por
participant/recording/window_start_utc. No requiere etiquetas al predecir.
'''
    (ROOT/'documentacion/Regresion_Ordinal_12-09-2026.md').write_text(report,encoding='utf-8')
    print(verification,flush=True); print(summary.to_string(index=False),flush=True)


if __name__=='__main__':
    with threadpool_limits(limits=2): main()
