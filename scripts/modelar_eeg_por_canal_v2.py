"""Grid por participantes, etiquetas PCA fijas; rondas y calibracion offline separadas."""
from __future__ import annotations
import argparse,itertools,json,time,platform,warnings,gc
from pathlib import Path
import joblib,numpy as np,pandas as pd,sklearn
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score,roc_curve
from catboost import CatBoostClassifier
import catboost
from threadpoolctl import threadpool_limits
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from atencion_binaria import ROOT,FEATURES as LEGACY_FEATURES,preprocessor,write,digest
from eeg_por_canal_v2 import FEATURES as CHANNEL_FEATURES
FEATURES=LEGACY_FEATURES+CHANNEL_FEATURES
HISTORY_COLUMNS=[i for i,c in enumerate(FEATURES) if c in LEGACY_FEATURES or "_relative_" in c]
from temporales_core import history_indices,sequence_array
from nuevos_modelos_atencion_binaria import OLD,labeled_frame,macro_auc,paired
from reconstruir_profesor_atencion_binaria import components,KEYS

SEED=20261101
BASE=ROOT/'resultados/eeg_por_canal_v2_29-10-2026/modelos_grid'
SCOPES=['inductivo','relativo_offline']

def base_features(frame,scope):
    values=frame[FEATURES].astype(float).copy()
    for c in FEATURES:
        if c in ['eeg_rms_uv','eeg_std_uv','eeg_peak_to_peak_uv','gsr_scr_count']:
            values[c]=np.log1p(values[c].clip(lower=0))
        elif c.startswith('eeg_') and c.endswith('_relative'):
            values[c]=np.log(values[c].clip(lower=1e-9))
    if scope=='relativo_offline':
        # Each person's own unlabelled complete session; no between-person calibration.
        means=values.groupby(frame.participant).transform('mean')
        stds=values.groupby(frame.participant).transform('std').replace(0,np.nan)
        values=(values-means)/stds
    elif scope!='inductivo':raise ValueError(scope)
    return values.replace([np.inf,-np.inf],np.nan)

def features(prep,frame,scope,context,multiscale=False):
    z=prep.transform(base_features(frame,scope)).astype('float32')
    if context==1:return z
    ix,lengths=history_indices(frame,context)
    x=sequence_array(z[:,HISTORY_COLUMNS],ix);mask=(np.arange(context)[None,:]<lengths[:,None])[:,:,None]
    mean=x.sum(axis=1)/lengths[:,None]
    variance=((x-mean[:,None,:])**2*mask).sum(axis=1)/lengths[:,None]
    # Temporal means retain channel band powers; temporal SD only for the original EEG/GSR panel.
    return np.column_stack([z,mean,np.sqrt(np.maximum(variance[:,:len(LEGACY_FEATURES)],0))]).astype('float32')


def candidates(round_no):
    result=[]
    for scope,context in itertools.product(SCOPES,[1,8,32]):
        for C in [.1,1.]:result.append(dict(scope=scope,context=context,family='Logistica',multiscale=False,params=dict(C=C)))
        for leaves in [7,15]:result.append(dict(scope=scope,context=context,family='HistBoost',multiscale=False,params=dict(max_leaf_nodes=leaves,max_iter=300,l2_regularization=10.,learning_rate=.05)))
        for depth in [4,6]:result.append(dict(scope=scope,context=context,family='CatBoost',multiscale=False,params=dict(depth=depth,l2_leaf_reg=10.,iterations=400,learning_rate=.05)))
    return [dict(c,id=f'espacial_c{i:03d}') for i,c in enumerate(result)]


def weights(frame):
    n=frame.groupby(['participant','y']).y.transform('size').to_numpy();k=frame.groupby('participant').y.transform('nunique').to_numpy()
    w=1/(n*k);return w/w.mean()

def make_model(c):
    if c['family']=='Logistica':return LogisticRegression(**c['params'],max_iter=2000,random_state=SEED)
    if c['family']=='HistBoost':return HistGradientBoostingClassifier(**c['params'],min_samples_leaf=30,early_stopping=False,random_state=SEED)
    return CatBoostClassifier(**c['params'],loss_function='Logloss',thread_count=2,random_seed=SEED,verbose=False,allow_writing_files=False)

def choose(trials):
    return sorted(trials,key=lambda t:(-t['auc_inner'],t['candidate']['id']))[0]

def score_bundle(bundle,frame):
    c=bundle['candidate'];a=features(bundle['prep'],frame,c['scope'],c['context'],c['multiscale'])
    return bundle['model'].predict_proba(a)[:,1]

def summarize(out,tables,round_no):
    p=pd.concat(tables,ignore_index=True);p.to_csv(out/'predicciones_oof.csv.gz',index=False)
    rows=[];people=[];grid=np.linspace(0,1,201);curves={}
    previous=pd.read_csv(ROOT/'resultados/nuevos_modelos_atencion_binaria_29-10-2026/metricas_participantes.csv')
    reference=previous[previous.teacher.eq('pca')&previous.family.eq('HistBoost')&previous['mode'].eq('history')].set_index('participant').auc
    for strategy,g in p.groupby('strategy',sort=False):
        aucs=[];rocs=[];deltas=[]
        for person,t in g.groupby('participant'):
            value=roc_auc_score(t.y,t.prob);aucs.append(value);deltas.append(value-reference.loc[person])
            people.append(dict(strategy=strategy,participant=person,auc=value))
            fpr,tpr,_=roc_curve(t.y,t.prob);v=np.interp(grid,fpr,tpr);v[0]=0;v[-1]=1;rocs.append(v)
        ci=paired(aucs);diff=paired(deltas)
        rows.append(dict(round=round_no,strategy=strategy,auc_macro=ci['mean'],ci_low=ci['ci_low'],ci_high=ci['ci_high'],auc_pooled=roc_auc_score(g.y,g.prob),delta_previous=diff['mean'],delta_ci_low=diff['ci_low'],delta_ci_high=diff['ci_high'],n=len(g),participants=len(aucs)))
        curves[strategy]=np.mean(rocs,axis=0)
    metrics=pd.DataFrame(rows);metrics.to_csv(out/'metricas.csv',index=False);pd.DataFrame(people).to_csv(out/'metricas_participantes.csv',index=False)
    fig,ax=plt.subplots(figsize=(8,7),layout='constrained')
    names=dict(inductivo='Sin calibración personal',relativo_offline='Calibración personal offline',seleccion_interna='Selección interna (puede usar offline)')
    for strategy,v in curves.items():
        a=metrics[metrics.strategy.eq(strategy)].auc_macro.iloc[0]
        ax.plot(grid,v,label=f'{names[strategy]}: {a:.3f}',lw=2)
    ax.plot([0,1],[0,1],'--',c='#999999');ax.set(title=f'EEG por canal y GSR · grid {round_no}',xlabel='Tasa de falsos positivos',ylabel='Sensibilidad',xlim=(0,1),ylim=(0,1));ax.grid(alpha=.15);ax.legend(loc='lower right',fontsize=9)
    for ext in ['png','pdf']:fig.savefig(out/f'curvas_roc.{ext}',dpi=180)
    plt.close(fig)
    report=[f'# EEG por canal y GSR — grid {round_no}','','Etiquetas y personas fijas del profesor PCA reconstruido. ROC-AUC principal = promedio por persona de predicciones OOF. Selección de parámetros solo en el holdout interno agrupado (16 personas ajuste, 4 selección); cada fold externo evalúa cinco personas distintas.','',
        '| Estrategia | AUC macro | IC descriptivo 95 % | ΔAUC frente a 0,6464 | IC de Δ |','|---|---:|---:|---:|---:|']
    for _,r in metrics.iterrows():report.append(f"| {names[r.strategy]} | {r.auc_macro:.4f} | [{r.ci_low:.4f}; {r.ci_high:.4f}] | {r.delta_previous:+.4f} | [{r.delta_ci_low:+.4f}; {r.delta_ci_high:+.4f}] |")
    report+=['','Se agregan variables EEG por canal, potencia Welch, entropía, Hjorth y calidad calculadas desde el ZIP V2 verificado. Se conservan exactamente las ventanas, etiquetas y folds de los análisis anteriores. Los canales inválidos producen features ausentes sin eliminar ventanas; la imputación se ajusta dentro de cada fold. El historial agrega medias de potencias relativas por canal y del panel EEG/GSR anterior, además de desviaciones del panel anterior. La estrategia inductiva ajusta imputación y escalado únicamente con personas de entrenamiento. La estrategia relativo_offline calcula media y desviación de EEG/GSR usando la sesión completa no etiquetada de cada persona, también de evaluación. Es adaptación transductiva offline; no representa un detector online ni una comparación idéntica de preprocesamiento con la referencia. La fila selección interna escoge entre ambas estrategias usando solo score interno.','',
        'Entradas: solo EEG/GSR y sus transformaciones logarítmicas y resúmenes temporales. Se excluyen mirada, pupila, scores, etiquetas, identidad y tiempo de sesión como predictores. Los scores docentes siguen siendo relativos y offline. Historial reiniciado en cambios de segmento/huecos. Las configuraciones completas constan en protocolo.json y selecciones.csv.','',
        'Búsqueda adaptativa sobre train reutilizado: intervalos descriptivos por bootstrap de personas, sin corrección por búsqueda acumulada ni parada al alcanzar una meta. Test/validation/P29 sin evaluar. AUC mayor que 0,70 aquí, si ocurre, no equivale a generalización confirmada. No se cambia la definición de etiqueta ni la métrica para alcanzar la meta.','',
        '![Curvas ROC](curvas_roc.png)','','[Predicciones](predicciones_oof.csv.gz) · [Selecciones](selecciones.csv) · [Protocolo](protocolo.json)']
    (out/'INFORME.md').write_text('\n'.join(report))
    print(metrics.to_string(index=False),flush=True)
    return metrics

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--round',type=int,choices=[1,2,3],required=True);args=parser.parse_args()
    out=BASE/f'ronda{args.round}';out.mkdir(parents=True,exist_ok=True)
    for sub in ['trials','modelos','predicciones','tareas']:(out/sub).mkdir(exist_ok=True)
    grid=candidates(args.round);source=ROOT/'resultados/preprocesamiento/caracteristicas_multimodales.csv';partition=ROOT/'resultados/modelado/particion_participantes.csv'
    oldplan=json.loads((OLD/'protocolo.json').read_text());raw=pd.read_csv(source);raw['source_row']=np.arange(len(raw));raw['split']=raw.participant.map(pd.read_csv(partition).set_index('participant').split)
    channel_file=ROOT/'resultados/eeg_por_canal_v2_29-10-2026/caracteristicas_eeg_por_canal.csv.gz'
    channel_audit=json.loads((channel_file.parent/'verificacion.json').read_text());assert channel_audit['passed'] and digest(channel_file)==channel_audit['feature_file_sha256']
    spatial=pd.read_csv(channel_file)
    raw=raw.merge(spatial[['source_row']+CHANNEL_FEATURES],on='source_row',how='left',validate='one_to_one')
    frame=raw[raw.split.eq('train')].copy().sort_values(KEYS).reset_index(drop=True);z,_=components(frame)
    plan=dict(round=args.round,grid=grid,source_sha256=digest(source),partition_sha256=digest(partition),old_teacher_protocol_sha256=digest(OLD/'protocolo.json'),
        script_sha256=digest(Path(__file__)),teacher_source_sha256=digest(ROOT/'scripts/reconstruir_profesor_atencion_binaria.py'),history_source_sha256=digest(ROOT/'scripts/temporales_core.py'),
        folds=oldplan['folds'],features=FEATURES,target='unchanged PCA binary attention per outer fold',seed=SEED,
        python=platform.python_version(),sklearn=sklearn.__version__,catboost=catboost.__version__,validation_evaluated=False,test_evaluated=False,
        channel_features_sha256=digest(channel_file),channel_protocol_sha256=digest(channel_file.parent/'protocolo.json'),reference_auc=.6464076199019761,metric='mean participant ROC-AUC',offline_calibration_separate=True)
    assert digest(source)==oldplan['source_sha256']
    if (out/'protocolo.json').exists():
        if json.loads((out/'protocolo.json').read_text())!=plan:raise ValueError('Protocolo cambiado')
    else:write(out/'protocolo.json',plan)
    allpred=[];alltrials=[];selections=[];started=time.monotonic();oldlabels=pd.read_csv(OLD/'pca/etiquetas_profesor_oof.csv.gz').set_index('source_row')
    with threadpool_limits(limits=2):
        for fold in plan['folds']:
            outer=labeled_frame(frame,z,fold['fit'],'pca');inner=labeled_frame(frame,z,fold['inner_fit'],'pca')
            fit=outer[outer.participant.isin(fold['fit'])].reset_index(drop=True);val=outer[outer.participant.isin(fold['evaluation'])].reset_index(drop=True)
            ii=inner[inner.participant.isin(fold['inner_fit'])].reset_index(drop=True);vv=inner[inner.participant.isin(fold['inner_validation'])].reset_index(drop=True)
            assert set(fit.participant).isdisjoint(val.participant) and set(ii.participant).isdisjoint(vv.participant)
            np.testing.assert_array_equal(val.y,oldlabels.loc[val.source_row].y)
            trials=[];cache={};preps={scope:preprocessor().fit(base_features(ii,scope)) for scope in SCOPES}
            for c in grid:
                name=f"fold{fold['fold']}_{c['id']}";done=out/'trials'/f'{name}.json';ppath=out/'trials'/f'{name}.csv.gz'
                if done.exists():
                    trial=json.loads(done.read_text());assert digest(ppath)==trial['prediction_sha256']
                else:
                    key=(c['scope'],c['context'],c['multiscale'])
                    if key not in cache:
                        cache[key]=(features(preps[c['scope']],ii,c['scope'],c['context'],c['multiscale']),features(preps[c['scope']],vv,c['scope'],c['context'],c['multiscale']))
                    a,b=cache[key];model=make_model(c);begin=time.monotonic()
                    with warnings.catch_warnings(record=True) as warns:
                        warnings.simplefilter('always');model.fit(a,ii.y,sample_weight=weights(ii))
                    prob=model.predict_proba(b)[:,1]
                    if not np.isfinite(prob).all():raise ValueError('Prediccion invalida')
                    t=vv[['source_row','participant','y']].copy().assign(prob=prob);t.to_csv(ppath,index=False)
                    trial=dict(fold=fold['fold'],candidate=c,auc_inner=macro_auc(vv,prob),seconds=time.monotonic()-begin,warnings=[str(w.message) for w in warns],prediction_sha256=digest(ppath),inner_fit=fold['inner_fit'],inner_validation=fold['inner_validation'])
                    write(done,trial)
                trials.append(trial);alltrials.append(trial)
                print(f"R{args.round} fold{fold['fold']} {c['id']} {c['family']} {c['scope']} ctx{c['context']} inner={trial['auc_inner']:.4f} · {time.monotonic()-started:.1f}s",flush=True)
            cache.clear();gc.collect()
            candidates_by_scope={scope:choose([t for t in trials if t['candidate']['scope']==scope]) for scope in SCOPES}
            pred_by_scope={}
            for scope,selected in candidates_by_scope.items():
                c=selected['candidate'];done=out/'tareas'/f"fold{fold['fold']}_{scope}.json";modelpath=out/'modelos'/f"fold{fold['fold']}_{scope}.joblib";predpath=out/'predicciones'/f"fold{fold['fold']}_{scope}.csv.gz"
                if done.exists():
                    task=json.loads(done.read_text());assert task['selected']==selected and task['model_sha256']==digest(modelpath) and task['prediction_sha256']==digest(predpath)
                    table=pd.read_csv(predpath)
                else:
                    prep=preprocessor().fit(base_features(fit,scope));a=features(prep,fit,scope,c['context'],c['multiscale']);model=make_model(c);model.fit(a,fit.y,sample_weight=weights(fit))
                    bundle=dict(model=model,prep=prep,candidate=c,fit_participants=fold['fit'],features=FEATURES)
                    joblib.dump(bundle,modelpath,compress=3);prob=score_bundle(bundle,val);again=score_bundle(joblib.load(modelpath),val);np.testing.assert_allclose(prob,again,atol=1e-8,rtol=1e-7)
                    table=val[['source_row','participant','y']].copy().assign(prob=prob,strategy=scope,fold=fold['fold'],candidate_id=c['id'])
                    table.to_csv(predpath,index=False);write(done,dict(selected=selected,model_sha256=digest(modelpath),prediction_sha256=digest(predpath)))
                np.testing.assert_array_equal(table.y,val.y);np.testing.assert_array_equal(table.source_row,val.source_row)
                selections.append(dict(strategy=scope,**selected));allpred.append(table);pred_by_scope[scope]=table
            joint=choose(trials);selected_scope=joint['candidate']['scope'];chosen=pred_by_scope[selected_scope].copy();chosen['strategy']='seleccion_interna';allpred.append(chosen)
            selections.append(dict(strategy='seleccion_interna',**joint))
            pd.DataFrame(selections).to_csv(out/'selecciones.csv',index=False)
            print(f"Fold{fold['fold']} terminado; seleccion conjunta {joint['candidate']['id']}",flush=True)
    pd.DataFrame(alltrials).to_csv(out/'busqueda_interna.csv',index=False)
    metrics=summarize(out,allpred,args.round)
    for _,g in pd.concat(allpred).groupby('strategy'):
        assert len(g)==13498 and not g.source_row.duplicated().any()
    write(out/'verificacion.json',dict(complete=True,inner_fits=len(alltrials),outer_models=10,predictions=sum(len(t) for t in allpred),old_labels_matched=True,group_separation=True,reload_verified=True,coverage_verified=True,target_07_exceeded=bool(metrics.auc_macro.gt(.7).any())))
if __name__=='__main__':main()
