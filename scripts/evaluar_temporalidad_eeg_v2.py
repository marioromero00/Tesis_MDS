"""Selección en train y comparación temporal congelada antes de validation."""
from pathlib import Path
import json,time,zipfile,warnings
import joblib,numpy as np,pandas as pd
from sklearn.metrics import roc_auc_score
from threadpoolctl import threadpool_limits
from modelar_eeg_por_canal_v2 import (ROOT,FEATURES,CHANNEL_FEATURES,SCOPES,base_features,features,preprocessor,candidates,make_model,weights,score_bundle,KEYS,components,OLD)
from reconstruir_profesor_atencion_binaria import fit_teacher,binary,COLUMNS
from nuevos_modelos_atencion_binaria import labeled_frame,macro_auc
from atencion_binaria import write,digest
from eeg_por_canal_v2 import RAW,FS,BANDS,extract_window
from preprocesamiento_secuencial import read_eeg_entry,eeg_features
OUT=ROOT/'resultados/temporalidad_eeg_v2_validacion_29-10-2026'

def ci(v):
    v=np.asarray(v);rng=np.random.default_rng(20261029)
    b=v[rng.integers(0,len(v),(20000,len(v)))].mean(axis=1)
    return float(v.mean()),*map(float,np.quantile(b,[.025,.975]))

def validation_features(raw):
    dest=OUT/'caracteristicas_validation.csv.gz'
    if dest.exists():return pd.read_csv(dest)
    expected=json.loads((ROOT/'resultados/preprocesamiento/manifiesto_ejecucion.json').read_text())['inputs']['eeg_zip']
    assert digest(RAW)==expected['sha256']
    mapping=pd.read_csv(ROOT/'resultados/sincronizacion/coordinacion_sesiones.csv').set_index('participant')
    rows=[];checks=0
    with zipfile.ZipFile(RAW) as archive:
        for person,g in raw.groupby('participant'):
            ts,x=read_eeg_entry(archive,mapping.loc[person].eeg_file,16)
            ok=np.isfinite(ts);ts,x=ts[ok],x[ok];order=np.argsort(ts,kind='stable');ts,x=ts[order],x[order]
            sampled=set(np.linspace(0,len(g)-1,10,dtype=int))
            for i,r in enumerate(g.itertuples(index=False)):
                lo,hi=np.searchsorted(ts,[pd.Timestamp(r.window_start_utc).timestamp(),pd.Timestamp(r.window_end_utc).timestamp()],side='left')
                t,s=ts[lo:hi],x[lo:hi];assert len(s)==int(r.eeg_n)
                if i in sampled:
                    old=eeg_features(s,FS,BANDS)
                    for k in ['eeg_rms_uv','eeg_std_uv','eeg_alpha_relative']:
                        np.testing.assert_allclose(old[k],getattr(r,k),rtol=2e-6,atol=1e-8,equal_nan=True)
                    checks+=1
                rows.append(dict(source_row=r.source_row,**extract_window(s,float(np.diff(t).max()) if len(t)>1 else 2.)))
            print('Extracción validation',person,flush=True)
    result=pd.DataFrame(rows);assert len(result)==len(raw) and not result.source_row.duplicated().any()
    result.to_csv(dest,index=False);write(OUT/'auditoria_extraccion.json',dict(passed=True,rows=len(result),legacy_checks=checks,sha256=digest(dest)))
    return result

def main():
    OUT.mkdir(exist_ok=True)
    for d in ['cv','modelos']:(OUT/d).mkdir(exist_ok=True)
    source=ROOT/'resultados/preprocesamiento/caracteristicas_multimodales.csv';partition=ROOT/'resultados/modelado/particion_participantes.csv'
    channel=ROOT/'resultados/eeg_por_canal_v2_29-10-2026/caracteristicas_eeg_por_canal.csv.gz'
    assert digest(channel)==json.loads((channel.parent/'verificacion.json').read_text())['feature_file_sha256']
    raw=pd.read_csv(source);raw['source_row']=np.arange(len(raw));raw['split']=raw.participant.map(pd.read_csv(partition).set_index('participant').split)
    train=raw[raw.split.eq('train')].merge(pd.read_csv(channel)[['source_row']+CHANNEL_FEATURES],on='source_row',validate='one_to_one').sort_values(KEYS).reset_index(drop=True)
    people=sorted(train.participant.unique());folds=json.loads((OLD/'protocolo.json').read_text())['folds'];grid=candidates(1)
    plan=dict(source_sha256=digest(source),partition_sha256=digest(partition),channel_sha256=digest(channel),script_sha256=digest(Path(__file__)),
        dependencies={n:digest(ROOT/'scripts'/n) for n in ['modelar_eeg_por_canal_v2.py','eeg_por_canal_v2.py','reconstruir_profesor_atencion_binaria.py','temporales_core.py']},
        folds=folds,grid=grid,primary='inductivo',secondary='relativo_offline',contexts=[1,8,32],span_seconds=[2,9,33],
        selection='highest macro participant AUC across five fixed train folds; ties candidate id',validation_previously_used=True,test_evaluated=False,
        teacher='PCA fit on training persons only; same relative offline components and participant median rule',comparison='Six context-specific models plus two scope-selected aliases; no reselection on validation')
    pp=OUT/'protocolo.json'
    if pp.exists():assert json.loads(pp.read_text())==plan
    else:write(pp,plan)
    z,_=components(train);records=[]
    oldlabels=pd.read_csv(OLD/'pca/etiquetas_profesor_oof.csv.gz').set_index('source_row')
    with threadpool_limits(limits=2):
        for fold in folds:
            f=labeled_frame(train,z,fold['fit'],'pca');fit=f[f.participant.isin(fold['fit'])].reset_index(drop=True);val=f[f.participant.isin(fold['evaluation'])].reset_index(drop=True)
            assert set(fit.participant).isdisjoint(val.participant)
            np.testing.assert_array_equal(val.y,oldlabels.loc[val.source_row].y)
            for scope in SCOPES:
                prep=preprocessor().fit(base_features(fit,scope))
                for context in [1,8,32]:
                    a=features(prep,fit,scope,context);b=features(prep,val,scope,context)
                    for c in [c for c in grid if c['scope']==scope and c['context']==context]:
                        path=OUT/'cv'/f"fold{fold['fold']}_{c['id']}.csv.gz"
                        if path.exists():t=pd.read_csv(path);np.testing.assert_array_equal(t.source_row,val.source_row);np.testing.assert_array_equal(t.y,val.y)
                        else:
                            model=make_model(c);model.fit(a,fit.y,sample_weight=weights(fit))
                            t=val[['source_row','participant','y']].assign(prob=model.predict_proba(b)[:,1]);t.to_csv(path,index=False)
                        for person,g in t.groupby('participant'):
                            records.append(dict(candidate_id=c['id'],scope=scope,context=context,fold=fold['fold'],participant=person,auc=roc_auc_score(g.y,g.prob)))
                        print('CV',fold['fold'],c['id'],f'{macro_auc(t,t.prob):.4f}',flush=True)
        scores=pd.DataFrame(records);scores.to_csv(OUT/'cv_personas.csv',index=False)
        means=scores.groupby(['candidate_id','scope','context'],as_index=False).auc.mean().sort_values(['auc','candidate_id'],ascending=[False,True]);means.to_csv(OUT/'seleccion_train.csv',index=False)
        selected={}
        for scope in SCOPES:
            for context in [1,8,32]:selected[f'{scope}_ctx{context}']=means[(means.scope==scope)&(means.context==context)].iloc[0].candidate_id
            selected[f'{scope}_seleccionado']=means[means.scope==scope].iloc[0].candidate_id
        write(OUT/'seleccion_congelada.json',dict(selected=selected,validation_evaluated=False,selection_train_sha256=digest(OUT/'seleccion_train.csv')))
        score,labels,thresholds,teacher=fit_teacher(train,z,people,'pca')
        joblib.dump(teacher,OUT/'profesor_final.joblib');fit=train.assign(y=labels).dropna(subset=['y']).copy();fit['y']=fit.y.astype(int)
        fit=fit.reset_index(drop=True);bundles={};hashes={}
        for ident in sorted(set(selected.values())):
            c=next(c for c in grid if c['id']==ident);prep=preprocessor().fit(base_features(fit,c['scope']));model=make_model(c)
            model.fit(features(prep,fit,c['scope'],c['context']),fit.y,sample_weight=weights(fit))
            bundle=dict(model=model,prep=prep,candidate=c,fit_participants=people,features=FEATURES)
            path=OUT/'modelos'/f'{ident}.joblib';joblib.dump(bundle,path,compress=3);bundles[ident]=bundle;hashes[ident]=digest(path)
        write(OUT/'congelacion_pre_validation.json',dict(models_sha256=hashes,teacher_sha256=digest(OUT/'profesor_final.joblib'),selected=selected,validation_evaluated=False,timestamp_utc=pd.Timestamp.now(tz='UTC').isoformat()))
        print('Modelos y profesor congelados; comienza validation',flush=True)
        vraw=raw[raw.split.eq('validation')].copy();spatial=validation_features(vraw)
        val=vraw.merge(spatial,on='source_row',validate='one_to_one').sort_values(KEYS).reset_index(drop=True)
        assert set(val.participant).isdisjoint(people) and val.participant.nunique()==8
        vz,_=components(val);valid=vz.notna().all(axis=1);vs=pd.Series(np.nan,index=val.index)
        loaded_teacher=joblib.load(OUT/'profesor_final.joblib')
        vs.loc[valid]=loaded_teacher['pca'].transform(vz.loc[valid,COLUMNS]).ravel()*loaded_teacher['sign']
        yl,thresholds=binary(vs,val);thresholds.to_csv(OUT/'umbrales_validation.csv',index=False)
        coverage=val.assign(label_available=yl.notna()).groupby('participant').label_available.agg(['size','sum']);coverage.to_csv(OUT/'cobertura_validation.csv')
        val=val.assign(y=yl).dropna(subset=['y']).copy();val['y']=val.y.astype(int);val=val.reset_index(drop=True)
        tables=[];metrics=[]
        for strategy,ident in selected.items():
            path=OUT/'modelos'/f'{ident}.joblib';assert digest(path)==hashes[ident]
            prob=score_bundle(joblib.load(path),val);np.testing.assert_allclose(prob,score_bundle(bundles[ident],val),atol=1e-8,rtol=1e-7)
            tables.append(val[['source_row','participant','y']].assign(prob=prob,strategy=strategy,candidate_id=ident))
            for person,g in tables[-1].groupby('participant'):
                metrics.append(dict(strategy=strategy,participant=person,n=len(g),auc=roc_auc_score(g.y,g.prob) if g.y.nunique()==2 else np.nan))
        predictions=pd.concat(tables);predictions.to_csv(OUT/'predicciones_validation.csv.gz',index=False)
        m=pd.DataFrame(metrics);assert m.auc.notna().all();m.to_csv(OUT/'metricas_participantes.csv',index=False)
        summary=[]
        for s,g in m.groupby('strategy'):
            mean,lo,hi=ci(g.auc);summary.append(dict(strategy=s,auc_macro=mean,ci_low=lo,ci_high=hi))
        summary=pd.DataFrame(summary);summary.to_csv(OUT/'metricas.csv',index=False)
        wide=m.pivot(index='participant',columns='strategy',values='auc');contrasts=[]
        for scope in SCOPES:
            for context in [8,32]:
                d=wide[f'{scope}_ctx{context}']-wide[f'{scope}_ctx1'];mean,lo,hi=ci(d)
                contrasts.append(dict(scope=scope,context=context,delta_auc=mean,ci_low=lo,ci_high=hi,improved_people=int((d>0).sum())))
        pd.DataFrame(contrasts).to_csv(OUT/'contrastes_temporalidad.csv',index=False)
        # Independent disk-based recomputation and identical paired rows/labels.
        disk=pd.read_csv(OUT/'predicciones_validation.csv.gz');reference=None
        for s,g in disk.groupby('strategy'):
            assert not g.source_row.duplicated().any()
            identity=g[['source_row','participant','y']].reset_index(drop=True)
            if reference is None:reference=identity
            else:pd.testing.assert_frame_equal(reference,identity)
            for person,t in g.groupby('participant'):
                np.testing.assert_allclose(roc_auc_score(t.y,t.prob),m[(m.strategy==s)&(m.participant==person)].auc.item(),atol=1e-12)
        write(OUT/'auditoria.json',dict(passed=True,participants=8,unique_models=len(bundles),predictions=len(disk),reload_verified=True,identical_rows_labels=True,train_validation_disjoint=True,test_evaluated=False))
        report=['# Evaluación adicional y temporalidad EEG por canal','','Selección completa en los 25 participantes de train; profesor PCA, seis modelos y contextos congelados antes de consultar validation. Validation contiene ocho participantes y ya se utilizó en investigaciones previas. Test y P29 no se evalúan.','',
        'Los contextos contienen 1, 8 o 32 ventanas de 2 s con paso de 1 s: abarcan hasta 2, 9 o 33 s. El historial incluye la ventana actual y solo ventanas anteriores del mismo segmento, reiniciándose ante huecos. Se agregan medias y desviaciones; no es una red recurrente ni un modelo del orden temporal. Las diferencias comparan procedimientos seleccionados por contexto y pueden reflejar cambios de modelo y dimensionalidad.','',
        'La estrategia inductiva es principal; offline es secundaria y normaliza con la sesión completa no etiquetada. El profesor utiliza mirada/pupila y umbrales relativos offline, por lo que los resultados no validan por sí solos un detector psicológico online.','',
        '## AUC macro en validation','','| Estrategia | Modelo seleccionado en train | AUC | IC descriptivo 95 % |','|---|---|---:|---:|']
        for r in summary.itertuples():
            c=next(c for c in grid if c['id']==selected[r.strategy]);report.append(f'| {r.strategy} | {c["family"]}, contexto {c["context"]}, {c["params"]} | {r.auc_macro:.4f} | [{r.ci_low:.4f}, {r.ci_high:.4f}] |')
        report+=['','## Diferencia temporal frente a ventana actual','','| Estrategia | Contexto | ΔAUC | IC pareado 95 % | Personas que mejoran |','|---|---:|---:|---:|---:|']
        for r in contrasts:report.append(f'| {r["scope"]} | {r["context"]} | {r["delta_auc"]:+.4f} | [{r["ci_low"]:.4f}, {r["ci_high"]:.4f}] | {r["improved_people"]}/8 |')
        report+=['','Intervalos descriptivos bootstrap de personas, 20.000 muestras, semilla 20261029; no corrigen comparaciones múltiples ni búsqueda acumulada. No se cambia el modelo principal según estos resultados. Los scores CV usados para seleccionar no son una estimación independiente de la configuración ganadora.','',
        '## Por persona','','| Persona | '+ ' | '.join(wide.columns)+' |','|---|'+ '|'.join(['---:']*len(wide.columns))+'|']
        for person,row in wide.iterrows():report.append('| '+person+' | '+' | '.join(f'{v:.4f}' for v in row)+' |')
        (OUT/'INFORME.md').write_text('\n'.join(report)+'\n')
        print(summary.to_string(index=False),flush=True);print(pd.DataFrame(contrasts).to_string(index=False),flush=True);print('COMPLETO Y AUDITADO',flush=True)
if __name__=='__main__':main()
