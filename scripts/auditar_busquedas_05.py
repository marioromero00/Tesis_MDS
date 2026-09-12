"""Recalcula seleccion, transformaciones y metricas desde artefactos persistidos."""
import argparse
import json
from datetime import datetime,timezone
import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits
import persistencia_core as persistence
import multiescala_core as multi
import adaptacion_core as adaptation
from ensambles_core import BASES
from hiperparametros_core import grid as base_grid,TARGET
from entrenar_hiperparametros import load_train
from avanzados_core import sample_weights
from optimizar_historial import smooth
from temporales_core import ROOT,CLASSES,digest,write_json,preprocessor,metric_record,individual_scores
from informe_control_historial import bootstrap,markdown

ROUNDS={'persistencia':('persistencia_11-09-2026',persistence),
        'multiescala':('multiescala_11-09-2026',multi),
        'adaptacion':('adaptacion_offline_11-09-2026',adaptation)}


def read(path): return json.loads(path.read_text(encoding='utf-8'))


def audit(name):
    dirname,core=ROUNDS[name]; out=ROOT/'resultados'/dirname
    protocol=read(out/'protocolo.json'); complete=read(out/'completo.json'); selections=read(out/'selecciones.json')
    assert digest(out/'selecciones.json')==complete['selection_sha256']
    for path,sha in protocol['sources'].items(): assert digest(ROOT/path)==sha,path
    train=load_train(); attempts=pd.read_csv(out/'intentos.csv'); inner_catalog=read(out/'catalogo_interno.json')
    recomputed=[]; processed=0
    for item in inner_catalog:
        path=out/item.get('saved_path',item.get('path')); sha=item.get('saved_sha256',item.get('sha256'))
        assert digest(path)==sha
        fold=protocol['folds'][item['fold']-1]
        assert set(item['train_participants']).isdisjoint(item['evaluation_participants'])
        assert set(item['train_participants']+item['evaluation_participants'])==set(fold['fit'])
        fit=train.loc[train.participant.isin(item['train_participants'])].reset_index(drop=True)
        with np.load(path) as saved:
            val=train.set_index('source_row',drop=False).loc[saved['source_row']].reset_index(drop=True)
            assert set(val.participant)==set(item['evaluation_participants'])
            assert val.source_row.is_unique
            weights=sample_weights(val,'participant'); y=val[TARGET].to_numpy()
            if name=='persistencia':
                origin=ROOT/'resultados/hiperparametros_11-09-2026_paralelo'/item['source_path']
                assert digest(origin)==item['source_sha256']
                lookup={d['base_id']:i for i,d in enumerate(base_grid())}
                with np.load(origin) as upstream:
                    np.testing.assert_array_equal(upstream['source_row'],saved['source_row'])
                    raw=np.mean([upstream[f'm{lookup[d["base_id"]]}'] for d in BASES if d['context']==8],axis=0)
                    np.testing.assert_array_equal(raw,saved['raw'])
                matrix=core.transitions(fit); np.testing.assert_array_equal(matrix,saved['transition'])
            elif name=='adaptacion':
                origin=ROOT/'resultados/persistencia_11-09-2026'/item['source_path']
                assert digest(origin)==item['source_sha256']
                with np.load(origin) as upstream:
                    np.testing.assert_array_equal(upstream['source_row'],saved['source_row'])
                    np.testing.assert_array_equal(upstream['raw'],saved['raw'])
                raw=saved['raw']
            for i,d in enumerate(protocol['grid']):
                if name=='multiescala':
                    for w in protocol['smoothing']:
                        probabilities=smooth(val,saved[f'm{i}'],w)
                        value=float(np.average(np.asarray(CLASSES)[probabilities.argmax(axis=1)]==y,weights=weights))
                        recomputed.append(dict(fold=item['fold'],inner=item['inner'],candidate_id=f'{d["base_id"]}_s{w}',score=value))
                else:
                    probabilities=core.decode(val,raw,matrix,d) if name=='persistencia' else core.adapt(val,raw,d)
                    np.testing.assert_array_equal(probabilities,saved[f'p{i}'])
                    value=float(np.average(np.asarray(CLASSES)[probabilities.argmax(axis=1)]==y,weights=weights))
                    recomputed.append(dict(fold=item['fold'],inner=item['inner'],candidate_id=d['candidate_id'],score=value))
        processed+=1
    keys=['fold','inner','candidate_id']; a=attempts.set_index(keys).sort_index(); b=pd.DataFrame(recomputed).set_index(keys).sort_index()
    assert a.index.equals(b.index); np.testing.assert_allclose(a.score,b.score,atol=1e-12,rtol=1e-12)
    for choice in selections:
        scores=attempts.loc[attempts.fold.eq(choice['fold'])]
        if choice['scope']!='all': scores=scores.loc[scores.family.eq(choice['scope'])]
        winner=scores.groupby('candidate_id',as_index=False).score.mean().sort_values(['score','candidate_id'],ascending=[False,True]).iloc[0]
        selected=choice['candidate_id'] if name=='multiescala' else choice['choice']['candidate_id']
        assert winner.candidate_id==selected
        np.testing.assert_allclose(winner.score,choice['inner_score'],atol=1e-12,rtol=1e-12)
    predictions=pd.read_csv(out/'predicciones_oof.csv.gz'); catalog=read(out/'catalogo_modelos.json')
    folds=pd.read_csv(out/'metricas_folds.csv').set_index('model_id'); people=pd.read_csv(out/'metricas_participantes.csv').set_index(['model_id','participant'])
    source=ROOT/'resultados/ensambles_11-09-2026'; source_catalog=read(source/'catalogo_modelos.json')
    prep_count=0
    for item in catalog:
        path=out/item['path']; assert digest(path)==item['sha256']; bundle=joblib.load(path)
        fold=protocol['folds'][item['fold']-1]
        assert item['train_participants']==fold['fit'] and item['evaluation_participants']==fold['evaluation']
        fit=train.loc[train.participant.isin(fold['fit'])].reset_index(drop=True)
        val=train.loc[train.participant.isin(fold['evaluation'])].reset_index(drop=True)
        saved=predictions.loc[predictions.model_id.eq(item['model_id'])].reset_index(drop=True)
        np.testing.assert_array_equal(saved.source_row,val.source_row); np.testing.assert_array_equal(saved.true,val[TARGET])
        if name=='multiescala':
            x=np.ascontiguousarray(core.feature_cache(fit)[bundle['definition']['representation']]); prep=preprocessor().fit(x)
            old=bundle['model']['prep']
            np.testing.assert_array_equal(old['imputer'].statistics_,prep['imputer'].statistics_)
            np.testing.assert_allclose(old['scale'].mean_,prep['scale'].mean_,atol=1e-12,rtol=1e-12)
            np.testing.assert_allclose(old['scale'].scale_,prep['scale'].scale_,atol=1e-12,rtol=1e-12)
            if bundle['definition']['family']=='rbf':
                kernel=bundle['model']['kernel']; np.testing.assert_allclose(kernel.components_,prep.transform(x)[kernel.component_indices_],atol=1e-12,rtol=1e-12)
            prep_count+=1
        else:
            origin=next(x for x in source_catalog if x['fold']==fold['fold'] and x['scope']=='pool_fixed_history' and x['seed']==20260911)
            assert digest(source/origin['path'])==item['source_sha256']==origin['sha256']
            assert joblib.hash(bundle['base'])==joblib.hash(joblib.load(source/origin['path']))
            if name=='persistencia': np.testing.assert_array_equal(bundle['transition'],core.transitions(fit))
        probabilities=core.predict(bundle,val.drop(columns=[TARGET,'arousal_score_6s']))
        assert np.isfinite(probabilities).all(); np.testing.assert_allclose(probabilities.sum(axis=1),1)
        np.testing.assert_allclose(probabilities,saved[['prob_'+c for c in CLASSES]],atol=1e-12,rtol=1e-12)
        pred=np.asarray(CLASSES)[probabilities.argmax(axis=1)]; np.testing.assert_array_equal(pred,saved.prediction)
        for k,v in metric_record(val,TARGET,pred,'classification').items(): np.testing.assert_allclose(v,folds.loc[item['model_id'],k],atol=1e-12,rtol=1e-12)
        for person,v in individual_scores(val,TARGET,pred,'classification').items(): np.testing.assert_allclose(v,people.loc[(item['model_id'],person),'score'],atol=1e-12,rtol=1e-12)
    summary=[]; classes=[]
    for (scope,seed),g in predictions.groupby(['scope','seed']):
        assert len(g)==len(train) and set(g.source_row)==set(train.source_row)
        summary.append(dict(scope=scope,seed=seed,**metric_record(g.reset_index(drop=True),'true',g.prediction.to_numpy(),'classification')))
        for label in CLASSES:
            mask=g.true.eq(label)
            classes.append(dict(scope=scope,seed=seed,label=label,recall=float(g.loc[mask,'prediction'].eq(label).mean()),predicted_fraction=float(g.prediction.eq(label).mean())))
    summary=pd.DataFrame(summary); summary.to_csv(out/'resumen_semillas.csv',index=False)
    mean=summary.groupby('scope',as_index=False)[['macro_score','balanced_accuracy','macro_f1']].mean(); mean.to_csv(out/'resumen_oof.csv',index=False)
    pd.DataFrame(classes).to_csv(out/'diagnostico_clases.csv',index=False)
    references=[('geometric_0.3651','fusiones_10-09-2026_completa','late_geometric'),('mixture_0.3716','mezclas_ensambles_11-09-2026','stack_weight_0.25')]
    gains=[]; refhash={}
    person_mean=people.reset_index().groupby(['scope','participant']).score.mean()
    for refname,directory,scope in references:
        path=ROOT/'resultados'/directory/'metricas_participantes.csv'; refhash[str(path.relative_to(ROOT))]=digest(path)
        ref=pd.read_csv(path); ref=ref.loc[ref.scope.eq(scope)]
        if 'task' in ref: ref=ref.loc[ref.task.eq('arousal')]
        ref=ref.groupby('participant').score.mean()
        for current in protocol['scopes']:
            values=person_mean.loc[current]; assert set(values.index)==set(ref.index)
            delta=values-ref; lo,hi=bootstrap(delta)
            gains.append(dict(scope=current,reference=refname,mean_delta=float(delta.mean()),ci_low=lo,ci_high=hi,improved=int((delta>1e-12).sum()),tied=int((delta.abs()<=1e-12).sum())))
    gains=pd.DataFrame(gains); gains.to_csv(out/'ganancias_pareadas.csv',index=False)
    verification=dict(models_reloaded=len(catalog),predictions_verified=len(predictions),inner_scores_verified=len(recomputed),
        inner_files_verified=processed,selections_verified=len(selections),preprocessors_refitted=prep_count,
        fold_metrics_verified=len(folds),participant_metrics_verified=len(people),protocol_sha256=digest(out/'protocolo.json'),
        catalog_sha256=digest(out/'catalogo_modelos.json'),predictions_sha256=digest(out/'predicciones_oof.csv.gz'),
        audit_script_sha256=digest(__file__),references=refhash,completed_utc=datetime.now(timezone.utc).isoformat(),
        validation_evaluated=False,test_evaluated=False)
    write_json(out/'verificacion.json',verification)
    report=f'''# Busqueda {name}: 11-09-2026

Meta solicitada: superar 0,50 de BA macro de activacion. Etiqueta fija arousal_label_6s;
25 participantes de train, cinco folds externos por persona y tres internos. Estos
participantes ya se usaron en exploraciones anteriores: no es confirmacion independiente.
Contraste principal: seleccion interna conjunta (all); familias separadas son secundarias.

## Resultados

{markdown(mean,list(mean.columns))}

{markdown(gains,list(gains.columns))}

Los intervalos son descriptivos, con 2.000 remuestreos pareados de participantes despues
de promediar semillas; no corrigen busquedas repetidas ni dependencia entre folds. Una
semilla en filtros deterministas; dos en multiescala, con seleccion usando la primera.
La referencia 0,3716 tambien es un maximo secundario exploratorio. No se alcanzo 0,50
si ninguna fila de BA macro supera ese valor; no se sustituye por accuracy o un fold aislado.

## Protocolo y auditoria

Configuraciones y semillas en protocolo.json; todas las puntuaciones en intentos.csv,
elecciones en selecciones.json. Se congelaron antes de la evaluacion externa. Se conserva
la prediccion interna de cada modelo y su linaje por persona. La auditoria recalcula
{len(recomputed)} puntuaciones y {len(selections)} elecciones; recarga {len(catalog)} modelos,
verifica {len(predictions)} predicciones, {len(folds)} metricas de fold y {len(people)} por persona.
Se reajustaron {prep_count} preprocesadores para comprobar que usan solo personas de ajuste.
Scores y estadisticas de escalado usan rtol=atol=1e-12; etiquetas predichas coinciden exactamente.
Cada archivo guardado incluye sus componentes necesarios para predecir.

Persistencia compara media causal, EMA y filtrado de Markov con transiciones aprendidas
solo de etiquetas de ajuste, sin etiquetas al predecir. Multiescala compara Ridge,
Nystroem RBF (192 componentes) y Extra Trees; entradas actuales, estadisticas de 4/16/64
ventanas, desfase de cuatro ventanas o desviaciones locales relativas. Se excluyen GSR,
etiquetas, identidad de participante y metadatos del estimador. Los grupos solo reinician
el historial. El soporte de 64 ventanas de 2 s y salto 1 s es 65 s; desfase 4 y suavizado
32 pueden ampliarlo a 100 s. Los huecos y cambios de persona/grabacion reinician el historial.

Adaptacion usa la sesion completa SIN etiquetas para centrar log-probabilidades o
clasificar rangos del log-cociente alto/bajo. Es OFFLINE y transductiva: utiliza entradas
futuras de la misma persona; no debe presentarse como prediccion causal o en tiempo real.
Los rangos producen decisiones one-hot, no probabilidades calibradas. Ridge tambien
produce scores transformados por softmax, sin calibracion probabilistica.

Validation y test originales no se reevaluaron. Las pseudoetiquetas y la normalizacion
offline original siguen limitando todas las comparaciones. No se modificaron etiquetas,
participantes, clases o metrica para perseguir 0,50.

Reproduccion: scripts/entrenar_{'adaptacion' if name=='adaptacion' else name}.py en una copia
sin el directorio de salida existente; scripts/auditar_busquedas_05.py --round {name}.
Carga: agregar scripts al path, joblib.load(archivo) y {core.__name__}.predict(bundle, frame),
con frame ordenado por participant/recording/window_start_utc y señales originales.

Fuentes metodologicas: [aproximacion de kernels](https://scikit-learn.org/1.9/modules/kernel_approximation.html)
y [prevencion de fugas](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage).
'''
    (ROOT/'documentacion'/f'Busqueda_{name}_11-09-2026.md').write_text(report,encoding='utf-8')
    print(name,verification,flush=True); print(mean.to_string(index=False),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--round',choices=ROUNDS,required=True)
    with threadpool_limits(limits=2): audit(parser.parse_args().round)
