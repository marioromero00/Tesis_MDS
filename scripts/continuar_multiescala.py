"""Conserva intento parcial; repite solo ajustes externos con tolerancia numerica."""
import argparse
import json
import shutil
from datetime import datetime,timezone
import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits
from multiescala_core import feature_cache,fit,raw_scores,predict
from entrenar_hiperparametros import load_train
from hiperparametros_core import TARGET
from optimizar_historial import smooth
from temporales_core import ROOT,CLASSES,digest,write_json,metric_record,individual_scores

SOURCE=ROOT/'resultados/multiescala_11-09-2026'
OUT=ROOT/'resultados/multiescala_11-09-2026_completa'


def main():
    OUT.mkdir(exist_ok=False); (OUT/'modelos').mkdir(); (OUT/'internos').mkdir()
    for path in SOURCE.rglob('*'):
        if path.is_file() and ('internos' in path.parts or path.name in ['protocolo.json','selecciones.json','catalogo_interno.json','intentos.csv']):
            shutil.copy2(path,OUT/path.relative_to(SOURCE))
    selections=json.loads((OUT/'selecciones.json').read_text()); protocol=json.loads((OUT/'protocolo.json').read_text())
    frozen=digest(OUT/'selecciones.json')
    continuation=dict(created_utc=datetime.now(timezone.utc).isoformat(),script_sha256=digest(__file__),
        source_inventory={p.relative_to(SOURCE).as_posix():digest(p) for p in SOURCE.rglob('*') if p.is_file()},
        selection_sha256=frozen,reason='Strict equality stopped at max abs 1.66533454e-16 during reload of ridge. Preserve all source artifacts.',
        policy='rtol=atol=1e-12 for scores AND exact argmax labels; no hyperparameter changes; repeat external fits only')
    write_json(OUT/'continuacion.json',continuation)
    train=load_train(); cache=feature_cache(train); models=[]; rows=[]; metrics=[]; people=[]; max_error=0.
    for choice in selections:
        fold=protocol['folds'][choice['fold']-1]; ti=np.flatnonzero(train.participant.isin(fold['fit'])); vi=np.flatnonzero(train.participant.isin(fold['evaluation']))
        f=train.iloc[ti].reset_index(drop=True); v=train.iloc[vi].reset_index(drop=True); d=choice['definition']
        for seed in protocol['seeds']:
            identity=dict(model_id=f'fold{fold["fold"]}_{choice["scope"]}_{seed}',fold=fold['fold'],scope=choice['scope'],seed=seed)
            bundle=fit(cache[d['representation']][ti],f,d,seed); bundle['smoothing']=choice['smoothing']
            path=OUT/'modelos'/f'{identity["model_id"]}.joblib'; joblib.dump(bundle,path,compress=3)
            proba=smooth(v,raw_scores(bundle,cache[d['representation']][vi]),choice['smoothing'])
            reloaded=predict(joblib.load(path),v)
            np.testing.assert_allclose(proba,reloaded,rtol=1e-12,atol=1e-12)
            np.testing.assert_array_equal(proba.argmax(axis=1),reloaded.argmax(axis=1)); max_error=max(max_error,float(np.max(np.abs(proba-reloaded))))
            pred=np.asarray(CLASSES)[proba.argmax(axis=1)]; p=v[['source_row','participant','window_start_utc']].copy(); p['true']=v[TARGET].to_numpy(); p['prediction']=pred
            for k,value in identity.items(): p[k]=value
            for i,c in enumerate(CLASSES): p['prob_'+c]=proba[:,i]
            rows.append(p); models.append(dict(**identity,path=path.relative_to(OUT).as_posix(),sha256=digest(path),choice=choice,
                train_participants=fold['fit'],evaluation_participants=fold['evaluation']))
            metrics.append(dict(**identity,**metric_record(v,TARGET,pred,'classification')))
            people.extend(dict(**identity,participant=p,score=s) for p,s in individual_scores(v,TARGET,pred,'classification').items())
        write_json(OUT/'catalogo_modelos.json',models); print(f'Continuacion multiescala fold {fold["fold"]}: {choice["scope"]}',flush=True)
    pd.concat(rows).to_csv(OUT/'predicciones_oof.csv.gz',index=False,compression='gzip')
    pd.DataFrame(metrics).to_csv(OUT/'metricas_folds.csv',index=False); pd.DataFrame(people).to_csv(OUT/'metricas_participantes.csv',index=False)
    assert digest(OUT/'selecciones.json')==frozen
    write_json(OUT/'completo.json',dict(models=len(models),predictions=sum(map(len,rows)),inner_fits_reused=360,inner_scores=1080,
        selection_sha256=frozen,max_reload_score_error=max_error,completed_utc=datetime.now(timezone.utc).isoformat(),validation_evaluated=False,test_evaluated=False))
    print(pd.DataFrame(people).groupby('scope').score.mean().to_string(),flush=True)


def audit():
    import auditar_busquedas_05 as a
    continuation=json.loads((OUT/'continuacion.json').read_text())
    assert digest(__file__)==continuation['script_sha256']
    for path,sha in continuation['source_inventory'].items(): assert digest(SOURCE/path)==sha
    for path in (OUT/'internos').glob('*.npz'): assert digest(path)==digest(SOURCE/'internos'/path.name)
    for name in ['protocolo.json','selecciones.json','catalogo_interno.json','intentos.csv']: assert digest(OUT/name)==digest(SOURCE/name)
    a.ROUNDS['multiescala']=(OUT.name,a.multi); a.audit('multiescala')


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--audit',action='store_true'); args=parser.parse_args()
    with threadpool_limits(limits=2):
        if args.audit: audit()
        else: main()
