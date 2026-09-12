"""Prediccion canonica C-contigua: elimina variacion por layout del kernel RBF."""
import argparse
import json
import shutil
from datetime import datetime,timezone
import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits
import regresion_ordinal_core as core
from entrenar_hiperparametros import load_train
from hiperparametros_core import TARGET
from temporales_core import ROOT,CLASSES,digest,write_json,metric_record,individual_scores

SOURCE=ROOT/'resultados/regresion_ordinal_12-09-2026'
OUT=ROOT/'resultados/regresion_ordinal_12-09-2026_completa'


def feature_cache(frame): return {k:np.ascontiguousarray(v) for k,v in core.feature_cache(frame).items()}


def raw_scores(bundle,x): return core.raw_scores(bundle,np.ascontiguousarray(x))


def predict(bundle,frame):
    raw=raw_scores(bundle,feature_cache(frame)[bundle['definition']['representation']])
    return np.asarray(CLASSES)[core.decide(frame,raw,bundle['smoothing'],bundle['low'],bundle['high'])]


def main():
    OUT.mkdir(exist_ok=False); (OUT/'modelos').mkdir(); (OUT/'internos').mkdir()
    for p in SOURCE.rglob('*'):
        if p.is_file() and ('internos' in p.parts or p.name in ['protocolo.json','selecciones.json','catalogo_interno.json','intentos.csv','bitacora.jsonl']):
            shutil.copy2(p,OUT/p.relative_to(SOURCE))
    selections=json.loads((OUT/'selecciones.json').read_text()); protocol=json.loads((OUT/'protocolo.json').read_text()); frozen=digest(OUT/'selecciones.json')
    write_json(OUT/'continuacion.json',dict(created_utc=datetime.now(timezone.utc).isoformat(),script_sha256=digest(__file__),selection_sha256=frozen,
        source_inventory={p.relative_to(SOURCE).as_posix():digest(p) for p in SOURCE.rglob('*') if p.is_file()},
        reason='RBF scores differed by 2.8263724694e-11 with identical feature values but different array layout. C-contiguous input reproduced scores exactly.',
        policy='Canonical contiguous input for deployed predictor and audit; rtol=atol=1e-12 remains, labels exact. Reuse all 180 inner fits and frozen thresholds.'))
    def log(stage,**kw):
        with (OUT/'bitacora.jsonl').open('a',encoding='utf-8') as f: f.write(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),stage=stage,**kw))+'\n')
    train=load_train(); cache=feature_cache(train); rows=[]; models=[]; metrics=[]; people=[]; max_error=0.
    for choice in selections:
        fold=protocol['folds'][choice['fold']-1]; ti=np.flatnonzero(train.participant.isin(fold['fit'])); vi=np.flatnonzero(train.participant.isin(fold['evaluation']))
        f=train.iloc[ti].reset_index(drop=True); v=train.iloc[vi].reset_index(drop=True); d=choice['definition']
        identity=dict(model_id=f'fold{fold["fold"]}_{choice["scope"]}',fold=fold['fold'],scope=choice['scope'],seed=20260912)
        log('outer_started',**identity); bundle=core.fit(cache[d['representation']][ti],f,d,20260912); bundle.update({k:choice[k] for k in ['smoothing','low','high']})
        path=OUT/'modelos'/f'{identity["model_id"]}.joblib'; joblib.dump(bundle,path,compress=3); restored=joblib.load(path)
        raw=raw_scores(bundle,cache[d['representation']][vi]); again=raw_scores(restored,feature_cache(v)[d['representation']])
        np.testing.assert_allclose(raw,again,rtol=1e-12,atol=1e-12); max_error=max(max_error,float(np.max(np.abs(raw-again))))
        pred=np.asarray(CLASSES)[core.decide(v,raw,choice['smoothing'],choice['low'],choice['high'])]; np.testing.assert_array_equal(pred,predict(restored,v.drop(columns=[TARGET])))
        p=v[['source_row','participant','window_start_utc']].copy(); p['true']=v[TARGET].to_numpy(); p['prediction']=pred; p['ordinal_score']=raw
        for k,value in identity.items(): p[k]=value
        rows.append(p); models.append(dict(**identity,path=path.relative_to(OUT).as_posix(),sha256=digest(path),choice=choice,train_participants=fold['fit'],evaluation_participants=fold['evaluation']))
        metrics.append(dict(**identity,**metric_record(v,TARGET,pred,'classification')))
        people.extend(dict(**identity,participant=p,score=s) for p,s in individual_scores(v,TARGET,pred,'classification').items())
        write_json(OUT/'catalogo_modelos.json',models); log('outer_completed',**identity); print(f'Continuacion ordinal fold {fold["fold"]}: {choice["scope"]}',flush=True)
    pd.concat(rows).to_csv(OUT/'predicciones_oof.csv.gz',index=False,compression='gzip')
    pd.DataFrame(metrics).to_csv(OUT/'metricas_folds.csv',index=False); pd.DataFrame(people).to_csv(OUT/'metricas_participantes.csv',index=False)
    assert digest(OUT/'selecciones.json')==frozen
    write_json(OUT/'completo.json',dict(models=len(models),predictions=sum(map(len,rows)),inner_fits_reused=180,inner_scores=3240,
        selection_sha256=frozen,max_reload_score_error=max_error,completed_utc=datetime.now(timezone.utc).isoformat(),validation_evaluated=False,test_evaluated=False))
    print(pd.DataFrame(people).groupby('scope').score.mean().to_string(),flush=True)


def audit():
    import auditar_regresion_ordinal as a
    continuation=json.loads((OUT/'continuacion.json').read_text()); assert digest(__file__)==continuation['script_sha256']
    for p,sha in continuation['source_inventory'].items(): assert digest(SOURCE/p)==sha
    for name in ['protocolo.json','selecciones.json','catalogo_interno.json','intentos.csv']: assert digest(OUT/name)==digest(SOURCE/name)
    for p in (OUT/'internos').glob('*.npz'): assert digest(p)==digest(SOURCE/'internos'/p.name)
    # Audit uses the actual deployed canonical predictor, including its feature transforms.
    a.OUT=OUT; a.feature_cache=feature_cache; a.raw_scores=raw_scores; a.predict=predict; a.main()


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--audit',action='store_true'); args=parser.parse_args()
    with threadpool_limits(limits=2):
        if args.audit: audit()
        else: main()
