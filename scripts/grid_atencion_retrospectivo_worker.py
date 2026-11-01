"""Ejecuta un fold independiente del grid original sin modificar su protocolo."""
import argparse,json,time,warnings,gc
from pathlib import Path
import numpy as np,pandas as pd,joblib
from threadpoolctl import threadpool_limits
from grid_atencion_retrospectivo import (ROOT,BASE,OLD,SCOPES,FEATURES,KEYS,candidates,components,labeled_frame,preprocessor,base_features,features,make_model,weights,macro_auc,choose,score_bundle,write,digest)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--round',type=int,required=True);parser.add_argument('--fold',type=int,required=True);args=parser.parse_args()
    out=BASE/f'ronda{args.round}';plan=json.loads((out/'protocolo.json').read_text())
    assert plan['script_sha256']==digest(ROOT/'scripts/grid_atencion_retrospectivo.py')
    grid=candidates(args.round);assert grid==plan['grid']
    fold=next(f for f in plan['folds'] if f['fold']==args.fold)
    source=ROOT/'resultados/preprocesamiento/caracteristicas_multimodales.csv';partition=ROOT/'resultados/modelado/particion_participantes.csv'
    assert digest(source)==plan['source_sha256'] and digest(partition)==plan['partition_sha256']
    raw=pd.read_csv(source);raw['source_row']=np.arange(len(raw));raw['split']=raw.participant.map(pd.read_csv(partition).set_index('participant').split)
    frame=raw[raw.split.eq('train')].copy().sort_values(KEYS).reset_index(drop=True);z,_=components(frame)
    outer=labeled_frame(frame,z,fold['fit'],'pca');inner=labeled_frame(frame,z,fold['inner_fit'],'pca')
    fit=outer[outer.participant.isin(fold['fit'])].reset_index(drop=True);val=outer[outer.participant.isin(fold['evaluation'])].reset_index(drop=True)
    ii=inner[inner.participant.isin(fold['inner_fit'])].reset_index(drop=True);vv=inner[inner.participant.isin(fold['inner_validation'])].reset_index(drop=True)
    assert set(ii.participant).isdisjoint(vv.participant) and set(fit.participant).isdisjoint(val.participant)
    oldlabels=pd.read_csv(OLD/'pca/etiquetas_profesor_oof.csv.gz').set_index('source_row');np.testing.assert_array_equal(val.y,oldlabels.loc[val.source_row].y)
    write(out/f'worker_fold{args.fold}.json',dict(worker_source_sha256=digest(Path(__file__)),grid_source_sha256=plan['script_sha256'],fold=args.fold,execution='independent fold; original grid/model/feature functions'))
    trials=[];cache={};preps={s:preprocessor().fit(base_features(ii,s)) for s in SCOPES};started=time.monotonic()
    with threadpool_limits(limits=2):
        for c in grid:
            name=f"fold{args.fold}_{c['id']}";done=out/'trials'/f'{name}.json';ppath=out/'trials'/f'{name}.csv.gz'
            if done.exists():
                trial=json.loads(done.read_text());assert digest(ppath)==trial['prediction_sha256']
            else:
                key=(c['scope'],c['context'],c['multiscale'],c['future'])
                if key not in cache:cache[key]=(features(preps[c['scope']],ii,c['scope'],c['context'],c['multiscale'],c['future']),features(preps[c['scope']],vv,c['scope'],c['context'],c['multiscale'],c['future']))
                a,b=cache[key];model=make_model(c);begin=time.monotonic()
                with warnings.catch_warnings(record=True) as warns:
                    warnings.simplefilter('always');model.fit(a,ii.y,sample_weight=weights(ii))
                prob=model.predict_proba(b)[:,1]
                if not np.isfinite(prob).all():raise ValueError('Probabilidad invalida')
                t=vv[['source_row','participant','y']].copy().assign(prob=prob);t.to_csv(ppath,index=False)
                trial=dict(fold=args.fold,candidate=c,auc_inner=macro_auc(vv,prob),seconds=time.monotonic()-begin,warnings=[str(w.message) for w in warns],prediction_sha256=digest(ppath),inner_fit=fold['inner_fit'],inner_validation=fold['inner_validation']);write(done,trial)
            trials.append(trial);print(f"fold{args.fold} {c['id']} inner={trial['auc_inner']:.4f} · {time.monotonic()-started:.1f}s",flush=True)
        cache.clear();gc.collect()
        for scope in SCOPES:
            selected=choose([t for t in trials if t['candidate']['scope']==scope]);c=selected['candidate']
            done=out/'tareas'/f'fold{args.fold}_{scope}.json';modelpath=out/'modelos'/f'fold{args.fold}_{scope}.joblib';predpath=out/'predicciones'/f'fold{args.fold}_{scope}.csv.gz'
            if done.exists():
                task=json.loads(done.read_text());assert task['selected']==selected and task['model_sha256']==digest(modelpath) and task['prediction_sha256']==digest(predpath)
            else:
                prep=preprocessor().fit(base_features(fit,scope));a=features(prep,fit,scope,c['context'],c['multiscale'],c['future']);model=make_model(c);model.fit(a,fit.y,sample_weight=weights(fit))
                bundle=dict(model=model,prep=prep,candidate=c,fit_participants=fold['fit'],features=FEATURES);joblib.dump(bundle,modelpath,compress=3)
                prob=score_bundle(bundle,val);again=score_bundle(joblib.load(modelpath),val);np.testing.assert_allclose(prob,again,atol=1e-8,rtol=1e-7)
                t=val[['source_row','participant','y']].copy().assign(prob=prob,strategy=scope,fold=args.fold,candidate_id=c['id']);t.to_csv(predpath,index=False)
                write(done,dict(selected=selected,model_sha256=digest(modelpath),prediction_sha256=digest(predpath)))
    print(f'Fold {args.fold} completo',flush=True)
if __name__=='__main__':main()
