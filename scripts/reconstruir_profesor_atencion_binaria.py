"""Reconstruye profesores binarios desde caracteristicas, nunca desde etiquetas antiguas."""
from __future__ import annotations
import json, time, argparse, hashlib
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
from sklearn.decomposition import PCA
from threadpoolctl import threadpool_limits
from sklearn.metrics import cohen_kappa_score
from atencion_binaria import (ROOT, FEATURES, VARIANTS, SEEDS, EPOCHS, train_predict, summarize, write, digest)

COLUMNS=['fixation_total_ms','fixation_mean_ms','gaze_dispersion_2d_px','gaze_path_length_px','pupil_mean_z']
DIRECTIONS=np.array([1,1,-1,-1,1])
KEYS=['participant','recording','segment_id','stimulus','window_start_utc']

def components(frame):
    """Normalizacion offline por persona, sin usar etiquetas ni features EEG/GSR."""
    z=pd.DataFrame(index=frame.index,columns=COLUMNS,dtype=float); stats=[]
    for person,g in frame.groupby('participant'):
        for c,direction in zip(COLUMNS,DIRECTIONS):
            values=g[c].astype(float)
            if c!='pupil_mean_z': values=np.log1p(values.clip(lower=0))
            mean=values.mean(); sd=values.std(ddof=0)
            z.loc[g.index,c]=((values-mean)/sd*direction if pd.notna(sd) and sd>0 else np.nan)
            stats.append(dict(participant=person,feature=c,mean=mean,sd=sd,direction=int(direction)))
    return z,pd.DataFrame(stats)

def binary(score,frame):
    labels=pd.Series(pd.NA,index=frame.index,dtype='Int64'); thresholds=[]
    for person,idx in frame.groupby('participant').groups.items():
        valid=score.loc[idx].dropna(); threshold=float(valid.median()) if len(valid) else None
        if threshold is not None and valid.nunique()>1:
            labels.loc[valid.index]=valid.gt(threshold).astype(int)
        thresholds.append(dict(participant=person,threshold=threshold,n_valid=len(valid),
            n_missing=int(labels.loc[idx].isna().sum()),n_ties=int(valid.eq(threshold).sum()) if threshold is not None else 0))
    return labels,pd.DataFrame(thresholds)

def fit_teacher(frame,z,fit_people,kind):
    if kind=='igualitario':
        # 50 % ocular (cuatro componentes), 50 % pupila; todos deben estar disponibles.
        score=(z[COLUMNS[:4]].mean(axis=1)+z[COLUMNS[4]])/2
        bundle={'kind':kind,'weights':[.125,.125,.125,.125,.5]}
    else:
        mask=frame.participant.isin(fit_people)&z.notna().all(axis=1)
        pca=PCA(n_components=1,random_state=20261029).fit(z.loc[mask,COLUMNS])
        # Orientacion solo con train del fold, segun direccion fisiologica declarada.
        sign=1 if np.dot(pca.components_[0],np.array([.125]*4+[.5]))>=0 else -1
        score=pd.Series(np.nan,index=frame.index); valid=z.notna().all(axis=1)
        score.loc[valid]=pca.transform(z.loc[valid,COLUMNS]).ravel()*sign
        bundle={'kind':kind,'pca':pca,'sign':sign,'fit_participants':sorted(fit_people)}
    score=score.where(z.notna().all(axis=1))
    labels,thresholds=binary(score,frame)
    bundle.update(columns=COLUMNS,directions=DIRECTIONS.tolist(),threshold_rule='1 if score > participant median; 0 otherwise; ties=0; missing=NA',offline=True)
    return score,labels,thresholds,bundle

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',default='resultados/profesor_binario_reconstruido_29-10-2026'); args=parser.parse_args()
    out=ROOT/args.output; out.mkdir(parents=True,exist_ok=True)
    source=ROOT/'resultados/preprocesamiento/caracteristicas_multimodales.csv'; partition=ROOT/'resultados/modelado/particion_participantes.csv'
    raw=pd.read_csv(source); raw['source_row']=np.arange(len(raw)); mapping=pd.read_csv(partition).set_index('participant').split
    raw['split']=raw.participant.map(mapping)
    if raw.split.isna().any(): raise ValueError('Persona sin particion')
    frame=raw[raw.split.eq('train')].copy().sort_values(KEYS).reset_index(drop=True)
    if frame.participant.nunique()!=25: raise ValueError('Train alterado')
    if frame[KEYS].duplicated().any(): raise ValueError('Ventanas duplicadas')
    z,norms=components(frame)
    folds=json.loads((ROOT/'resultados/contraste_temporalidad_fusion_24-10-2026/protocolo.json').read_text())['folds']['attention']
    protocol={'source_sha256':digest(source),'partition_sha256':digest(partition),
        'source_code_sha256':digest(Path(__file__)),'student_code_sha256':digest(ROOT/'scripts/atencion_binaria.py'),
        'temporal_code_sha256':digest(ROOT/'scripts/temporales_core.py'),
        'teacher_columns':COLUMNS,'directions':DIRECTIONS.tolist(),'old_labels_used':False,'old_scores_used':False,
        'teachers':['igualitario','pca'],'folds':folds,'student_features':FEATURES,'variants':VARIANTS,
        'seeds':SEEDS,'epochs':EPOCHS,'binary_rule':'1 = atento (score > mediana personal); 0 = no atento (score <= mediana); ausentes = NA',
        'offline_person_calibration':True,'pca_fit':'solo participantes de ajuste de cada fold',
        'test_evaluated':False,'validation_evaluated':False,'context_windows':8}
    protocol=json.loads(json.dumps(protocol))
    if (out/'protocolo.json').exists():
        if json.loads((out/'protocolo.json').read_text())!=protocol: raise ValueError('Protocolo cambiado')
    else: write(out/'protocolo.json',protocol)
    norms.to_csv(out/'normalizacion_profesor.csv',index=False)
    results=[]; final_labels={}; all_tables=[]; start=time.monotonic()
    with threadpool_limits(limits=2):
        for kind in protocol['teachers']:
            dest=out/kind
            for sub in ['modelos','predicciones','profesores']: (dest/sub).mkdir(parents=True,exist_ok=True)
            write(dest/'protocolo.json',dict(protocol,binary_definition=protocol['binary_rule'],teacher=kind))
            # Full-train professor is an export; cross-validation below always refits PCA inside each fold.
            sc,lab,thr,bundle=fit_teacher(frame,z,sorted(frame.participant.unique()),kind)
            final_labels[kind]=lab
            bundle['normalization']=norms; bundle['thresholds']=thr
            joblib.dump(bundle,dest/'profesores/profesor_train_completo.joblib',compress=3)
            dataset=frame.copy(); dataset['teacher_score']=sc; dataset['attention_binary']=lab
            dataset.to_csv(dest/'dataset_binario_train.csv.gz',index=False)
            thr.to_csv(dest/'umbrales_train_completo.csv',index=False)
            tables=[]; fold_labels=[]
            for fold in folds:
                assert set(fold['fit']).isdisjoint(fold['evaluation'])
                sc,labels,thresholds,teacher=fit_teacher(frame,z,fold['fit'],kind)
                teacher['normalization']=norms; teacher['thresholds']=thresholds
                joblib.dump(teacher,dest/'profesores'/f"profesor_fold{fold['fold']}.joblib",compress=3)
                labeled=frame.assign(y=labels,teacher_score=sc).dropna(subset=['y']).copy(); labeled['y']=labeled.y.astype(int)
                fit=labeled[labeled.participant.isin(fold['fit'])].reset_index(drop=True)
                val=labeled[labeled.participant.isin(fold['evaluation'])].reset_index(drop=True)
                if fit.y.nunique()!=2: raise ValueError('Sin dos clases')
                lf=val[['source_row','participant','y','teacher_score']].assign(fold=fold['fold']); fold_labels.append(lf)
                for family,mode in VARIANTS:
                    seeds=SEEDS if family in ['MLP_current','TCN','LSTM'] else SEEDS[:1]
                    for seed in seeds:
                        name=f"{family}_{mode}_fold{fold['fold']}_{seed}"; pred=dest/'predicciones'/f'{name}.csv.gz'; model=dest/'modelos'/f'{name}.joblib'
                        if pred.exists():
                            t=pd.read_csv(pred); audit=json.loads((dest/'predicciones'/f'{name}.json').read_text())
                            if digest(pred)!=audit['predictions_sha256'] or digest(model)!=audit['model_sha256']: raise ValueError('Artefactos cambiados')
                        else:
                            probabilities=train_predict(fit,val,family,mode,seed,model)
                            t=val[['source_row','participant','y']].copy().assign(prob=probabilities,family=family,mode=mode,fold=fold['fold'],seed=seed)
                            t.to_csv(pred,index=False); write(dest/'predicciones'/f'{name}.json',{'model_sha256':digest(model),'predictions_sha256':digest(pred)})
                        np.testing.assert_array_equal(t.source_row,val.source_row); np.testing.assert_array_equal(t.y,val.y)
                        tables.append(t)
                        print(f'{kind}: {name} · {time.monotonic()-start:.1f}s',flush=True)
            fl=pd.concat(fold_labels); fl.to_csv(dest/'etiquetas_profesor_oof.csv.gz',index=False)
            summarize(dest,tables)
            # Replace generic report: this experiment has newly constructed labels, including fold-specific PCA.
            metrics=pd.read_csv(dest/'metricas.csv'); metrics.insert(0,'profesor',kind); results.append(metrics)
            predictions=pd.concat(tables); predictions.insert(0,'profesor',kind); all_tables.append(predictions)
            assert not fl.source_row.duplicated().any()
            for (family,mode),g in predictions.groupby(['family','mode']):
                seeds=2 if family in ['MLP_current','TCN','LSTM'] else 1
                counts=g.groupby('source_row').size(); assert len(counts)==len(fl) and counts.eq(seeds).all()
            report=['# Profesor binario reconstruido: '+kind,'',protocol['binary_rule'],
                '', 'Reconstruido desde caracteristicas_multimodales.csv. No se leen etiquetas ni scores antiguos. EEG/GSR predicen etiquetas de mirada/pupila; el profesor PCA se ajusta solo con personas del train de cada fold. Normalización y mediana por persona usan la sesión completa: etiquetado retrospectivo offline, no inferencia online de atención absoluta.', '',
                'Cinco folds originales por participante, dos semillas en redes, ocho épocas fijas. Validación, test y P29 sin evaluar. Resultados exploratorios. El historial puede usar solo entradas pasadas hasta la ventana actual; la referencia docente offline no es causal.', '',
                '| Modelo | Entrada | AUC macro | IC descriptivo 95 % |','|---|---|---:|---:|']
            for _,r in metrics.sort_values('auc_macro',ascending=False).iterrows(): report.append(f"| {r.family} | {r['mode']} | {r.auc_macro:.4f} | [{r.ci_low:.4f}, {r.ci_high:.4f}] |")
            report+=['','AUC: promedio por persona tras promediar semillas. Intervalos por bootstrap de 25 personas, sin corrección por búsqueda previa. Los datasets exportados usan profesor full-train; las etiquetas OOF de PCA pueden diferir porque el profesor se reajusta dentro de cada fold. Las predicciones OOF siempre usan las etiquetas de su profesor de fold. No se ha validado la interpretación psicológica atento/no atento.', '', '![ROC](curvas_roc.png)','', '![AUC](comparacion_auc.png)']
            (dest/'INFORME.md').write_text('\n'.join(report))
            write(dest/'verificacion.json',dict(complete=True,profesor=kind,models=len(list((dest/'modelos').glob('*.joblib'))),teacher_bundles=6,
                rows_oof=len(fl),predictions=len(predictions),positive_rate_oof=float(fl.y.mean()),reload_verified=True,coverage_verified=True))
    combined=pd.concat(results); combined.to_csv(out/'comparacion_profesores_modelos.csv',index=False)
    pd.concat(all_tables).to_csv(out/'predicciones_todos_profesores.csv.gz',index=False)
    mask=final_labels['igualitario'].notna()&final_labels['pca'].notna()
    write(out/'concordancia_profesores.json',{'n':int(mask.sum()),'agreement':float((final_labels['igualitario'][mask]==final_labels['pca'][mask]).mean()),
        'kappa':float(cohen_kappa_score(final_labels['igualitario'][mask].astype(int),final_labels['pca'][mask].astype(int))), 'scope':'profesores full-train; descriptivo'})
    (out/'INFORME.md').write_text('# Reconstrucción binaria de atención\n\n'+protocol['binary_rule']+'\n\nRegla relativa offline por persona, sin etiquetas antiguas; PCA ajustado por fold para predicciones OOF.\n\n- [Profesor igualitario](igualitario/INFORME.md)\n- [Profesor PCA](pca/INFORME.md)\n\n[Comparación completa](comparacion_profesores_modelos.csv). Cada profesor define una referencia distinta: sus AUC no permiten elegir cuál etiqueta representa mejor la atención real.\n')
    print(combined.to_string(index=False),flush=True)
if __name__=='__main__': main()
