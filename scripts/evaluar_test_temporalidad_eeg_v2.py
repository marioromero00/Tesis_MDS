"""Test congelado y contraste del aporte temporal con controles emparejados."""
from pathlib import Path
import json,zipfile
import numpy as np,pandas as pd,joblib
from sklearn.metrics import roc_auc_score
from threadpoolctl import threadpool_limits
from evaluar_temporalidad_eeg_v2 import (ROOT,KEYS,components,binary,COLUMNS,score_bundle,digest,write,ci,RAW,FS,BANDS,extract_window,read_eeg_entry,eeg_features)
from modelar_eeg_por_canal_v2 import CHANNEL_FEATURES,FEATURES,preprocessor,base_features,features,make_model,weights
from reconstruir_profesor_atencion_binaria import fit_teacher
BASE=ROOT/'resultados/temporalidad_eeg_v2_validacion_29-10-2026'
OUT=ROOT/'resultados/temporalidad_eeg_v2_test_29-10-2026'

def test_features(raw):
    dest=OUT/'caracteristicas_test.csv.gz'
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
            print('Extracción test',person,flush=True)
    result=pd.DataFrame(rows);assert len(result)==len(raw) and not result.source_row.duplicated().any()
    result.to_csv(dest,index=False);write(OUT/'auditoria_extraccion.json',dict(passed=True,rows=len(result),legacy_checks=checks,sha256=digest(dest)))
    return result
def label_with_teacher(frame,teacher):
    z,_=components(frame);ok=z.notna().all(axis=1);score=pd.Series(np.nan,index=frame.index)
    score.loc[ok]=teacher['pca'].transform(z.loc[ok,COLUMNS]).ravel()*teacher['sign']
    y,thresholds=binary(score,frame)
    return y,thresholds

def main():
    OUT.mkdir(exist_ok=True);(OUT/'modelos_controles').mkdir(exist_ok=True)
    freeze=json.loads((BASE/'congelacion_pre_validation.json').read_text());oldplan=json.loads((BASE/'protocolo.json').read_text())
    for ident,h in freeze['models_sha256'].items():assert digest(BASE/'modelos'/f'{ident}.joblib')==h
    assert digest(BASE/'profesor_final.joblib')==freeze['teacher_sha256']
    for n,h in oldplan['dependencies'].items():assert digest(ROOT/'scripts'/n)==h
    source=ROOT/'resultados/preprocesamiento/caracteristicas_multimodales.csv';partition=ROOT/'resultados/modelado/particion_participantes.csv'
    assert digest(source)==oldplan['source_sha256'] and digest(partition)==oldplan['partition_sha256']
    plan=dict(created_utc=pd.Timestamp.now(tz='UTC').isoformat(),script_sha256=digest(Path(__file__)),previous_freeze_sha256=digest(BASE/'congelacion_pre_validation.json'),
        hypothesis='Temporal multimodal models outperform comparable static models for attention and activation; this run assesses attention only.',
        primary_contrast='inductivo_ctx32 minus inductivo_estatico_pareado (same family and hyperparameters, no history)',
        secondary_contrasts='ctx8 and ctx32 vs original selected static, separately inductive/offline; offline matched static',
        primary_metric='mean ROC-AUC per participant',uncertainty='paired participant bootstrap percentile 95%, 20000 draws, seed20261029, descriptive; no multiplicity correction',
        decision='CI above zero: descriptive support; CI below zero: descriptive contrary evidence; CI includes zero: inconclusive, not proof of equality',
        test_previously_consulted=True,validation_previously_consulted=True,no_test_selection=True,activation_evaluated=False,fusion_ablation=False,
        caveats='session-relative offline teacher, overlapping windows; no psychological ground truth; histogram aggregation is not sequence-order modeling')
    # Never overwrite an existing test evaluation or silently change its protocol.
    if (OUT/'protocolo_pre_test.json').exists():raise RuntimeError('Evaluación test ya iniciada; revisar antes de repetir')
    write(OUT/'protocolo_pre_test.json',plan)
    raw=pd.read_csv(source);raw['source_row']=np.arange(len(raw));raw['split']=raw.participant.map(pd.read_csv(partition).set_index('participant').split)
    teacher=joblib.load(BASE/'profesor_final.joblib');train_people=set(raw[raw.split.eq('train')].participant)
    assert set(teacher['fit_participants'])==train_people
    channel=ROOT/'resultados/eeg_por_canal_v2_29-10-2026/caracteristicas_eeg_por_canal.csv.gz';assert digest(channel)==oldplan['channel_sha256']
    train=raw[raw.split.eq('train')].merge(pd.read_csv(channel)[['source_row']+CHANNEL_FEATURES],on='source_row',validate='one_to_one').sort_values(KEYS).reset_index(drop=True)
    y,_=label_with_teacher(train,teacher);train=train.assign(y=y).dropna(subset=['y']).copy();train['y']=train.y.astype(int);train=train.reset_index(drop=True)
    paths={name:BASE/'modelos'/f'{ident}.joblib' for name,ident in freeze['selected'].items() if not name.endswith('_seleccionado')}
    for scope in ['inductivo','relativo_offline']:
        original=joblib.load(paths[f'{scope}_ctx32']);c=dict(original['candidate']);c.update(context=1,id=f'{scope}_estatico_pareado')
        prep=preprocessor().fit(base_features(train,scope));model=make_model(c)
        model.fit(features(prep,train,scope,1),train.y,sample_weight=weights(train))
        path=OUT/'modelos_controles'/f'{scope}.joblib';joblib.dump(dict(model=model,prep=prep,candidate=c,fit_participants=sorted(train_people),features=FEATURES),path,compress=3)
        paths[c['id']]=path
    model_hashes={name:digest(path) for name,path in paths.items()}
    write(OUT/'congelacion_pre_test.json',dict(timestamp_utc=pd.Timestamp.now(tz='UTC').isoformat(),models={name:dict(path=str(path),sha256=model_hashes[name]) for name,path in paths.items()},teacher_sha256=digest(BASE/'profesor_final.joblib'),test_evaluated=False))
    print('Controles entrenados; todos los modelos congelados antes de test',flush=True)
    test=raw[raw.split.eq('test')].copy();spatial=test_features(test)
    test=test.merge(spatial,on='source_row',validate='one_to_one').sort_values(KEYS).reset_index(drop=True)
    assert test.participant.nunique()==8 and set(test.participant).isdisjoint(train_people)
    y,thresholds=label_with_teacher(test,teacher);thresholds.to_csv(OUT/'umbrales_test.csv',index=False)
    test.assign(label_available=y.notna()).groupby('participant').label_available.agg(['size','sum']).to_csv(OUT/'cobertura_test.csv')
    test=test.assign(y=y).dropna(subset=['y']).copy();test['y']=test.y.astype(int);test=test.reset_index(drop=True)
    predictions=[];rows=[]
    for name,path in paths.items():
        assert digest(path)==model_hashes[name];bundle=joblib.load(path)
        assert set(bundle['fit_participants'])==train_people
        prob=score_bundle(bundle,test);assert np.isfinite(prob).all() and ((prob>=0)&(prob<=1)).all()
        predictions.append(test[['source_row','participant','y']].assign(strategy=name,prob=prob))
        for person,g in predictions[-1].groupby('participant'):
            assert g.y.nunique()==2
            rows.append(dict(strategy=name,participant=person,n=len(g),auc=roc_auc_score(g.y,g.prob)))
    pred=pd.concat(predictions);pred.to_csv(OUT/'predicciones_test.csv.gz',index=False)
    m=pd.DataFrame(rows);m.to_csv(OUT/'metricas_participantes.csv',index=False);wide=m.pivot(index='participant',columns='strategy',values='auc')
    summary=[]
    for name,g in m.groupby('strategy'):
        mean,lo,hi=ci(g.auc);summary.append(dict(strategy=name,auc_macro=mean,ci_low=lo,ci_high=hi))
    summary=pd.DataFrame(summary);summary.to_csv(OUT/'metricas.csv',index=False)
    contrasts=[]
    for scope in ['inductivo','relativo_offline']:
        pairs=[(f'{scope}_ctx32',f'{scope}_estatico_pareado'),(f'{scope}_ctx8',f'{scope}_ctx1'),(f'{scope}_ctx32',f'{scope}_ctx1'),(f'{scope}_ctx32',f'{scope}_ctx8')]
        for temporal,baseline in pairs:
            d=wide[temporal]-wide[baseline];mean,lo,hi=ci(d)
            verdict='apoyo descriptivo' if lo>0 else 'evidencia contraria descriptiva' if hi<0 else 'inconcluso'
            contrasts.append(dict(temporal=temporal,baseline=baseline,delta_auc=mean,ci_low=lo,ci_high=hi,improved_people=int((d>0).sum()),verdict=verdict))
    con=pd.DataFrame(contrasts);con.to_csv(OUT/'contrastes.csv',index=False)
    validation=pd.read_csv(BASE/'metricas.csv');comparison=validation.merge(summary,on='strategy',suffixes=('_validation','_test'));comparison.to_csv(OUT/'comparacion_validation_test.csv',index=False)
    # Reload all saved models and independently recalculate metrics from saved predictions.
    disk=pd.read_csv(OUT/'predicciones_test.csv.gz')
    for name,path in paths.items():
        t=disk[disk.strategy.eq(name)].reset_index(drop=True)
        pd.testing.assert_frame_equal(t[['source_row','participant','y']],test[['source_row','participant','y']])
        np.testing.assert_allclose(score_bundle(joblib.load(path),test),t.prob,atol=1e-8,rtol=1e-7)
        values=[roc_auc_score(g.y,g.prob) for _,g in t.groupby('participant')]
        np.testing.assert_allclose(np.mean(values),summary[summary.strategy.eq(name)].auc_macro.item(),atol=1e-12)
    write(OUT/'auditoria.json',dict(passed=True,test_people=8,rows_per_model=len(test),models=len(paths),identical_labels_rows=True,reload_verified=True,hashes_verified=True,train_test_disjoint=True,teacher_fit_train_only=True,matched_controls_fit_train_only=True,test_evaluated=True))
    lines=['# Test: atención y contraste de temporalidad','','## Hipótesis y alcance','',
    'Hipótesis de la tesis: los modelos temporales multimodales superan a los estáticos comparables en atención y activación emocional. Fuente: Problema e hipótesis.md, vault del 24-09-2026. Esta corrida aborda atención binaria mediante EEG/GSR y pseudoetiquetas de mirada/pupila. No evalúa activación ni aísla el aporte de la fusión.',
    '', 'Antes de evaluar test se fijó como contraste principal el modelo inductivo de 32 ventanas frente a un control estático de la misma familia y parámetros (HistGradientBoosting, 15 hojas, 300 iteraciones, l2=10, learning_rate=0,05). Se reutilizan los modelos temporales seleccionados solo en train. Los dos controles estáticos pareados se ajustaron solo en train, sin búsqueda adicional. Test y validation ya habían sido consultados en investigaciones anteriores: interpretación exploratoria.',
    '', '## AUC macro por persona en test','','| Estrategia | AUC | IC descriptivo 95 % |','|---|---:|---:|']
    for r in summary.itertuples():lines.append(f'| {r.strategy} | {r.auc_macro:.4f} | [{r.ci_low:.4f}; {r.ci_high:.4f}] |')
    lines+=['','## Diferencias pareadas','','| Temporal | Referencia | ΔAUC | IC 95 % | Personas que mejoran | Interpretación |','|---|---|---:|---:|---:|---|']
    for r in con.itertuples():lines.append(f'| {r.temporal} | {r.baseline} | {r.delta_auc:+.4f} | [{r.ci_low:.4f}; {r.ci_high:.4f}] | {r.improved_people}/8 | {r.verdict} |')
    principal=contrasts[0]
    lines+=['','## Conclusión para la hipótesis','',f'Contraste principal: {principal["verdict"]}; ΔAUC {principal["delta_auc"]:+.4f}, IC [{principal["ci_low"]:.4f}; {principal["ci_high"]:.4f}].',
    '', 'Un intervalo que incluye cero no confirma superioridad ni demuestra equivalencia o ausencia de efecto. Un intervalo negativo constituye evidencia contraria para esta comparación, no rechazo universal de cualquier arquitectura temporal. Superar AUC 0,70 no prueba la hipótesis, que exige mejora frente al estático. La hipótesis central completa no queda contrastada por esta corrida porque falta el resultado de activación emocional bajo un protocolo comparable.',
    '', 'Los intervalos son bootstrap pareado de ocho participantes, 20.000 remuestreos, semilla 20261029. Son descriptivos, sin ajuste de comparaciones múltiples ni corrección de la búsqueda histórica. No se utilizan ventanas solapadas como observaciones independientes. El contexto contiene ventanas de 2 s con paso de 1 s: ctx1=2 s, ctx8=hasta9 s, ctx32=hasta33 s. Historial de medias/variabilidad, sin modelado explícito del orden. El control pareado conserva familia e hiperparámetros; cambiar la representación temporal cambia su dimensión.',
    '', 'La normalización offline de predictores usa la sesión completa de cada persona y se reporta como secundaria. Incluso el profesor del análisis inductivo usa normalización y umbrales relativos por sesión; son pseudoetiquetas offline y no validación psicológica externa. Se conservan todas las personas y se omiten únicamente las filas sin etiqueta según la regla previa.',
    '', '## Validation y test, mismos modelos','','| Estrategia | Validation | Test |','|---|---:|---:|']
    for r in comparison.itertuples():lines.append(f'| {r.strategy} | {r.auc_macro_validation:.4f} | {r.auc_macro_test:.4f} |')
    lines+=['','## Por participante','','| Persona | '+' | '.join(wide.columns)+' |','|---|'+'|'.join(['---:']*len(wide.columns))+'|']
    for person,r in wide.iterrows():lines.append('| '+person+' | '+' | '.join(f'{v:.4f}' for v in r)+' |')
    (OUT/'INFORME.md').write_text('\n'.join(lines)+'\n')
    print(summary.to_string(index=False),flush=True);print(con.to_string(index=False),flush=True);print('TEST COMPLETO Y AUDITADO',flush=True)
if __name__=='__main__':
    with threadpool_limits(limits=2):main()
