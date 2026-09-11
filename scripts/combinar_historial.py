"""Segunda iteracion: combinacion de logistica fija y candidato temporal interno."""
import json
from datetime import datetime,timezone
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold
from threadpoolctl import threadpool_limits
from optimizar_historial import OUT as BASE, TARGET, TARGETS, FEATURES, represent, estimator, probabilities, smooth
from temporales_core import ROOT,CLASSES,digest,write_json,prepare_frame,metric_record,individual_scores
from informe_control_historial import bootstrap,markdown

OUT=BASE/'segunda_iteracion'


def main():
    OUT.mkdir(parents=True,exist_ok=False); (OUT/'modelos').mkdir()
    protocol=json.loads((BASE/'protocolo.json').read_text(encoding='utf-8'))
    choices=json.loads((BASE/'selecciones.json').read_text(encoding='utf-8'))
    catalog=json.loads((BASE/'catalogo_modelos.json').read_text(encoding='utf-8'))
    prior=json.loads((BASE/'completo.json').read_text(encoding='utf-8'))
    assert digest(BASE/'selecciones.json')==prior['selection_sha256']
    dataset=ROOT/'resultados/modelado/dataset_modelado.csv'
    assert digest(dataset)==protocol['dataset_sha256']
    data=pd.read_csv(dataset); data['source_row']=np.arange(len(data))
    train=prepare_frame(data.loc[data.split.eq('train')],'arousal_primary_6s',TARGETS,'train')
    train=train.sort_values(['participant','recording','window_start_utc']).reset_index(drop=True); del data
    config=dict(created_utc=datetime.now(timezone.utc).isoformat(),weights=[0.,.25,.5,.75,1.],
        rule='selected maximizes mean internal fold participant BA, ties prefer lower temporal weight; fixed always 0.5',
        primary='selected blend vs fixed logistic; fixed 50/50 is secondary, neither chosen by outer score',
        scope='second exploratory iteration after seeing first search OOF; repeated train research, no independent confirmation',
        previous_protocol_sha256=digest(BASE/'protocolo.json'),previous_selection_sha256=digest(BASE/'selecciones.json'),
        source_sha256=digest(__file__),validation_evaluated=False,test_evaluated=False)
    write_json(OUT/'protocolo.json',config)
    matrices={r:represent(train,r) for r in protocol['representations']}
    search=[]; selected=[]; inner_predictions=[]
    for fold in protocol['folds']:
        choice=next(c for c in choices if c['fold']==fold['fold'] and c['scope']=='temporal')
        fit_ix=np.flatnonzero(train.participant.isin(fold['fit']))
        fit_frame=train.iloc[fit_ix].reset_index(drop=True)
        splits=GroupKFold(n_splits=3,shuffle=True,random_state=20260908+fold['fold'])
        for inner,(ii,vv) in enumerate(splits.split(fit_frame,groups=fit_frame.participant),1):
            fi,vi=fit_ix[ii],fit_ix[vv]; frame=train.iloc[vi].reset_index(drop=True)
            baseline=estimator('logistic_1',20260908,5).fit(matrices['current'][fi],train.iloc[fi][TARGET])
            rep=choice['representation']; temporal=estimator(choice['estimator'],20260908,matrices[rep].shape[1]).fit(matrices[rep][fi],train.iloc[fi][TARGET])
            bp=probabilities(baseline,matrices['current'][vi]); tp=smooth(frame,probabilities(temporal,matrices[rep][vi]),choice['smoothing'])
            ip=frame[['source_row','participant',TARGET]].copy(); ip['fold']=fold['fold']; ip['inner']=inner
            for i,c in enumerate(CLASSES): ip['base_'+c]=bp[:,i]; ip['temporal_'+c]=tp[:,i]
            inner_predictions.append(ip)
            for weight in config['weights']:
                prediction=np.asarray(CLASSES)[((1-weight)*bp+weight*tp).argmax(axis=1)]
                search.append(dict(fold=fold['fold'],inner=inner,weight=weight,
                    score=metric_record(frame,TARGET,prediction,'classification')['macro_score']))
        group=pd.DataFrame(search); group=group.loc[group.fold.eq(fold['fold'])].groupby('weight',as_index=False).score.mean()
        winner=group.sort_values(['score','weight'],ascending=[False,True]).iloc[0]
        selected.append(dict(fold=fold['fold'],weight=float(winner.weight),inner_score=float(winner.score)))
        print(f'Fold {fold["fold"]}: peso temporal elegido={winner.weight}',flush=True)
    pd.DataFrame(search).to_csv(OUT/'busqueda_pesos.csv',index=False)
    pd.concat(inner_predictions).to_csv(OUT/'predicciones_internas.csv.gz',index=False,compression='gzip')
    write_json(OUT/'selecciones.json',selected); frozen=digest(OUT/'selecciones.json')
    predictions=[]; metrics=[]; people=[]; artifacts=[]
    for fold in protocol['folds']:
        vi=np.flatnonzero(train.participant.isin(fold['evaluation'])); frame=train.iloc[vi].reset_index(drop=True)
        for seed in protocol['seeds']:
            base=next(m for m in catalog if m['fold']==fold['fold'] and m['seed']==seed and m['scope']=='fixed_logistic')
            temporal=next(m for m in catalog if m['fold']==fold['fold'] and m['seed']==seed and m['scope']=='temporal')
            for m in [base,temporal]: assert digest(BASE/m['path'])==m['sha256']
            bmodel=joblib.load(BASE/base['path']); tmodel=joblib.load(BASE/temporal['path'])
            bp=probabilities(bmodel,matrices['current'][vi]); tp=smooth(frame,probabilities(tmodel,matrices[temporal['representation']][vi]),temporal['smoothing'])
            for scope,weight in [('selected',next(s['weight'] for s in selected if s['fold']==fold['fold'])),('fixed_half',.5)]:
                name=f'fold{fold["fold"]}__{scope}__{seed}'; path=OUT/'modelos'/f'{name}.joblib'
                bundle=dict(baseline=bmodel,temporal=tmodel,temporal_weight=weight,representation=temporal['representation'],smoothing=temporal['smoothing'],features=FEATURES)
                joblib.dump(bundle,path,compress=3); restored=joblib.load(path)
                prob=(1-weight)*bp+weight*tp
                replay=(1-weight)*probabilities(restored['baseline'],matrices['current'][vi])+weight*smooth(frame,probabilities(restored['temporal'],matrices[restored['representation']][vi]),restored['smoothing'])
                np.testing.assert_array_equal(prob,replay)
                pred=np.asarray(CLASSES)[prob.argmax(axis=1)]
                ident=dict(model_id=name,fold=fold['fold'],scope=scope,seed=seed)
                artifacts.append(dict(**ident,weight=weight,path=path.relative_to(OUT).as_posix(),sha256=digest(path),
                    train_participants=fold['fit'],evaluation_participants=fold['evaluation'],reload_verified=True,
                    baseline_sha256=base['sha256'],temporal_sha256=temporal['sha256']))
                p=frame[['source_row','participant',TARGET]].copy()
                for k,v in ident.items(): p[k]=v
                p['prediction']=pred
                for i,c in enumerate(CLASSES): p['prob_'+c]=prob[:,i]
                predictions.append(p); metrics.append(dict(**ident,**metric_record(frame,TARGET,pred,'classification')))
                people.extend(dict(**ident,participant=p,score=s) for p,s in individual_scores(frame,TARGET,pred,'classification').items())
    assert digest(OUT/'selecciones.json')==frozen
    preds=pd.concat(predictions); preds.to_csv(OUT/'predicciones_oof.csv.gz',index=False,compression='gzip')
    saved=pd.read_csv(OUT/'predicciones_oof.csv.gz')
    np.testing.assert_array_equal(saved.prediction,preds.prediction)
    np.testing.assert_allclose(saved[['prob_'+c for c in CLASSES]],preds[['prob_'+c for c in CLASSES]],rtol=1e-12,atol=1e-12)
    metrics=pd.DataFrame(metrics); metrics.to_csv(OUT/'metricas_folds.csv',index=False)
    people=pd.DataFrame(people); people.to_csv(OUT/'metricas_participantes.csv',index=False)
    write_json(OUT/'catalogo_modelos.json',artifacts)
    summary=[]
    for (scope,seed),g in preds.groupby(['scope','seed']):
        assert len(g)==len(train) and not g.source_row.duplicated().any()
        summary.append(dict(scope=scope,seed=seed,**metric_record(g.reset_index(drop=True),TARGET,g.prediction.to_numpy(),'classification')))
    summary=pd.DataFrame(summary).groupby('scope',as_index=False)[['macro_score','balanced_accuracy','macro_f1']].mean()
    summary.to_csv(OUT/'resumen_oof.csv',index=False)
    scores=people.groupby(['scope','participant']).score.mean().unstack('scope')
    previous=pd.read_csv(BASE/'metricas_participantes.csv')
    for ref in ['all','fixed_logistic']:
        scores[ref]=previous.loc[previous.scope.eq(ref)].groupby('participant').score.mean().reindex(scores.index)
    gains=[]
    for scope in ['selected','fixed_half']:
        for ref in ['all','fixed_logistic']:
            delta=scores[scope]-scores[ref]; low,high=bootstrap(delta)
            gains.append(dict(scope=scope,reference=ref,mean_delta=float(delta.mean()),ci_low=low,ci_high=high,positive_participants=int((delta>0).sum())))
    gains=pd.DataFrame(gains); gains.to_csv(OUT/'ganancias_pareadas.csv',index=False)
    write_json(OUT/'verificacion.json',dict(models_reloaded=20,predictions_verified=len(preds),inner_fits=30,
        selection_sha256=frozen,source_sha256=digest(__file__),validation_evaluated=False,test_evaluated=False))
    report=f'''# Segunda iteración: combinación de probabilidades

08-09-2026. Se ejecuta después de observar la primera búsqueda; es exploratoria.
Se combina logística fija con el candidato temporal de cada fold. Peso temporal elegido
entre 0/0,25/0,5/0,75/1 por los mismos tres folds internos. Un control usa siempre 0,5.
Los pesos se congelan antes de evaluar las combinaciones en los folds externos.
No se usa validation/test original ni se elige entre ambas reglas por sus métricas OOF.

{markdown(summary,['scope','macro_score','balanced_accuracy','macro_f1'])}

{markdown(gains,['scope','reference','mean_delta','ci_low','ci_high','positive_participants'])}

Los intervalos son descriptivos: 2.000 remuestreos pareados de personas, media previa
entre semillas, sin ajuste por dependencia de folds ni por comparaciones múltiples.
La adaptación entre iteraciones sobre train sigue limitando la interpretación.

{markdown(pd.DataFrame(selected),['fold','weight','inner_score'])}

Se conservan 20 bundles `.joblib` con ambos pipelines, representación, suavizado y peso;
54.096 predicciones externas verificadas tras recargar, predicciones internas para
recalcular los 75 puntajes de pesos, catálogo y resultados por persona. Se realizaron
30 ajustes internos adicionales; los componentes externos reutilizan la primera búsqueda.
La combinación usa las probabilidades ordenadas bajo/medio/alto. Antes de combinarlas,
aplicar al componente temporal su representación y su suavizado causal.

Código: `scripts/combinar_historial.py`. Requiere la primera búsqueda completa.
La carpeta de esta segunda ejecución debe ser nueva; el script conserva la anterior.
'''
    (OUT/'Informe.md').write_text(report,encoding='utf-8')
    print(summary.to_string(index=False)); print(gains.to_string(index=False))


if __name__=='__main__':
    with threadpool_limits(limits=4): main()
