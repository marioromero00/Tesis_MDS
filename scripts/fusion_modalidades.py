"""Tercera iteracion exploratoria: mirada y EEG con pupila, seleccion anidada."""
import json
from datetime import datetime,timezone
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold
from threadpoolctl import threadpool_limits
from optimizar_historial import OUT as BASE, TARGET, TARGETS, FEATURES, represent, estimator, probabilities, smooth
from temporales_core import ROOT,CLASSES,digest,write_json,prepare_frame,metric_record,individual_scores
from control_historial import nested_folds
from baselines_estaticos import EYE,EEG,GSR
from informe_control_historial import bootstrap,markdown

OUT=BASE/'tercera_iteracion'


def inputs(frame,representation):
    panel,mode=representation.split('__')
    extra=EYE+(EEG if panel=='full' else [])
    assert set(extra+FEATURES).isdisjoint(GSR)
    return np.column_stack([represent(frame,mode),frame[extra].to_numpy(float)])


def main():
    OUT.mkdir(parents=True,exist_ok=False); (OUT/'modelos').mkdir()
    protocol=json.loads((BASE/'protocolo.json').read_text(encoding='utf-8'))
    dataset=ROOT/'resultados/modelado/dataset_modelado.csv'
    assert digest(dataset)==protocol['dataset_sha256']
    data=pd.read_csv(dataset); data['source_row']=np.arange(len(data))
    train=prepare_frame(data.loc[data.split.eq('train')],'arousal_primary_6s',TARGETS,'train')
    train=train.sort_values(['participant','recording','window_start_utc']).reset_index(drop=True); del data
    reps=[f'{p}__{r}' for p in ['eye','full'] for r in ['current','recording_8']]
    names=['logistic_0.1','logistic_1','hgb','rbf']; folds=nested_folds(train)
    config=dict(created_utc=datetime.now(timezone.utc).isoformat(),representations=reps,estimators=names,
        smoothing=[1,4,8],seeds=protocol['seeds'],folds=folds,features=dict(pupil=FEATURES,eye=EYE,eeg=EEG),
        source_sha256=digest(__file__),dataset_sha256=digest(dataset),
        scope='third exploratory iteration after two pupil-only searches; no independent confirmation',
        primary='nested all multimodal vs fixed pupil logistic',secondary='nested multimodal current and temporal rules',
        selection='mean BA macro of three internal participant folds; freeze all choices before outer evaluation',
        fusion='early concatenation: current gaze/EEG plus current pupil or causal pupil summaries; no GSR predictor',
        validation_evaluated=False,test_evaluated=False)
    write_json(OUT/'protocolo.json',config)
    xs={r:inputs(train,r) for r in reps}; search=[]; choices=[]
    for fold in folds:
        fit_ix=np.flatnonzero(train.participant.isin(fold['fit'])); fit_frame=train.iloc[fit_ix]
        splits=GroupKFold(n_splits=3,shuffle=True,random_state=20260908+fold['fold'])
        for inner,(ii,vv) in enumerate(splits.split(fit_frame,groups=fit_frame.participant),1):
            fi,vi=fit_ix[ii],fit_ix[vv]; frame=train.iloc[vi].reset_index(drop=True)
            for rep in reps:
                for name in names:
                    model=estimator(name,20260908,xs[rep].shape[1]).fit(xs[rep][fi],train.iloc[fi][TARGET])
                    raw=probabilities(model,xs[rep][vi])
                    for window in config['smoothing']:
                        prediction=np.asarray(CLASSES)[smooth(frame,raw,window).argmax(axis=1)]
                        search.append(dict(fold=fold['fold'],inner=inner,representation=rep,estimator=name,smoothing=window,
                            score=metric_record(frame,TARGET,prediction,'classification')['macro_score'],
                            fit_participants='|'.join(sorted(train.iloc[fi].participant.unique())),
                            evaluation_participants='|'.join(sorted(frame.participant.unique()))))
            pd.DataFrame(search).to_csv(OUT/'busqueda_interna.csv',index=False)
            print(f'Fusion fold {fold["fold"]}/5 interno {inner}/3',flush=True)
        scores=pd.DataFrame(search); scores=scores.loc[scores.fold.eq(fold['fold'])].groupby(['representation','estimator','smoothing'],as_index=False).score.mean()
        current=scores.representation.str.endswith('__current')&scores.smoothing.eq(1)
        for scope,eligible in [('all',scores),('current',scores.loc[current]),('temporal',scores.loc[~current])]:
            winner=eligible.sort_values(['score','representation','estimator','smoothing'],ascending=[False,True,True,True]).iloc[0]
            choices.append(dict(fold=fold['fold'],scope=scope,representation=winner.representation,estimator=winner.estimator,
                                smoothing=int(winner.smoothing),inner_score=float(winner.score)))
        write_json(OUT/'selecciones.json',choices)
    frozen=digest(OUT/'selecciones.json'); artifacts=[]; predictions=[]; metrics=[]; people=[]
    for choice in choices:
        fold=folds[choice['fold']-1]; fi=np.flatnonzero(train.participant.isin(fold['fit']))
        vi=np.flatnonzero(train.participant.isin(fold['evaluation'])); frame=train.iloc[vi].reset_index(drop=True)
        x=xs[choice['representation']]
        for seed in config['seeds']:
            model=estimator(choice['estimator'],seed,x.shape[1]).fit(x[fi],train.iloc[fi][TARGET])
            name=f'fold{fold["fold"]}__{choice["scope"]}__{seed}'; path=OUT/'modelos'/f'{name}.joblib'
            joblib.dump(model,path,compress=3); raw=probabilities(model,x[vi])
            np.testing.assert_array_equal(raw,probabilities(joblib.load(path),x[vi]))
            prob=smooth(frame,raw,choice['smoothing']); pred=np.asarray(CLASSES)[prob.argmax(axis=1)]
            ident=dict(model_id=name,fold=fold['fold'],scope=choice['scope'],seed=seed)
            artifacts.append(dict(**choice,model_id=name,seed=seed,path=path.relative_to(OUT).as_posix(),sha256=digest(path),
                train_participants=fold['fit'],evaluation_participants=fold['evaluation'],reload_verified=True))
            p=frame[['source_row','participant',TARGET]].copy()
            for k,v in ident.items(): p[k]=v
            p['prediction']=pred
            for i,c in enumerate(CLASSES): p['prob_'+c]=prob[:,i]
            predictions.append(p); metrics.append(dict(**ident,**metric_record(frame,TARGET,pred,'classification')))
            people.extend(dict(**ident,participant=p,score=s) for p,s in individual_scores(frame,TARGET,pred,'classification').items())
    assert digest(OUT/'selecciones.json')==frozen
    preds=pd.concat(predictions); preds.to_csv(OUT/'predicciones_oof.csv.gz',index=False,compression='gzip')
    saved=pd.read_csv(OUT/'predicciones_oof.csv.gz'); np.testing.assert_array_equal(saved.prediction,preds.prediction)
    np.testing.assert_allclose(saved[['prob_'+c for c in CLASSES]],preds[['prob_'+c for c in CLASSES]],rtol=1e-12,atol=1e-12)
    people=pd.DataFrame(people); people.to_csv(OUT/'metricas_participantes.csv',index=False)
    pd.DataFrame(metrics).to_csv(OUT/'metricas_folds.csv',index=False)
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
        scores['previous_'+ref]=previous.loc[previous.scope.eq(ref)].groupby('participant').score.mean().reindex(scores.index)
    gains=[]
    for scope in ['all','temporal','current']:
        for ref in ['previous_all','previous_fixed_logistic']:
            delta=scores[scope]-scores[ref]; low,high=bootstrap(delta)
            gains.append(dict(scope=scope,reference=ref,mean_delta=float(delta.mean()),ci_low=low,ci_high=high,positive_participants=int((delta>0).sum())))
    gains=pd.DataFrame(gains); gains.to_csv(OUT/'ganancias_pareadas.csv',index=False)
    write_json(OUT/'verificacion.json',dict(models_reloaded=30,predictions_verified=len(preds),inner_fits=240,
        selection_sha256=frozen,source_sha256=digest(__file__),validation_evaluated=False,test_evaluated=False))
    report=f'''# Tercera iteración: fusión temprana con mirada y EEG

08-09-2026. Seguimiento exploratorio después de ver los dos intentos pupilares.
Se mantiene la etiqueta GSR de activación y la división original. Inputs actuales de mirada
(10) más pupila (5), con/sin EEG (9). Alternativa temporal: los cinco valores pupilares
actuales más sus 16 estadísticas de historia, concatenados con mirada/EEG actuales.
No se incluye GSR ni fracción de validez pupilar en las entradas.

48 candidatos: cuatro representaciones, cuatro estimadores y suavizado causal 1/4/8.
Los estimadores y las reglas causales son los de la primera búsqueda. Cinco folds externos,
tres internos, selección por media de BA macro interna y dos semillas de reajuste externo.
Se congelan las 15 selecciones antes de evaluar. `all` busca en 48, `current` en ocho
y `temporal` en 40. No se selecciona una regla usando sus resultados externos.

{markdown(summary,['scope','macro_score','balanced_accuracy','macro_f1'])}

{markdown(gains,['scope','reference','mean_delta','ci_low','ci_high','positive_participants'])}

{markdown(pd.DataFrame(choices),['fold','scope','representation','estimator','smoothing','inner_score'])}

240 ajustes internos, 720 puntuaciones guardadas y 30 pipelines externos recargados;
81.144 predicciones verificadas. Cada pipeline usa 20 participantes. Reconstruir entradas
con `inputs(frame, meta['representation'])`, cargar `.joblib`, aplicar `probabilities`
y `smooth` con el contexto del catálogo. Ordenar frame por persona/grabación/timestamp.
Imputación, escalado y aproximación RBF se ajustan dentro de cada pipeline en entrenamiento.

Intervalos descriptivos del 95%, 2.000 remuestreos pareados de personas tras promediar semillas.
No corrigen adaptación entre iteraciones, comparaciones múltiples ni dependencia de folds.
Validation/test originales sin nueva evaluación. Normalización y pseudoetiquetas offline.
Los conjuntos mayores prueban una ampliación del problema, no demuestran que más sensores
sean necesarios. Una mejora sobre pupila no aislaría el aporte de historial frente al de
modalidades. Código reproducible: `scripts/fusion_modalidades.py`, carpeta nueva obligatoria.
'''
    (OUT/'Informe.md').write_text(report,encoding='utf-8')
    print(summary.to_string(index=False)); print(gains.to_string(index=False))


if __name__=='__main__':
    with threadpool_limits(limits=4): main()
