"""Busqueda acotada con seleccion interna agrupada y comparacion OOF pareada."""
from __future__ import annotations
import json,time,platform,warnings
from pathlib import Path
import joblib,numpy as np,pandas as pd,sklearn
from scipy.special import expit
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis,QuadraticDiscriminantAnalysis
from sklearn.ensemble import ExtraTreesClassifier,HistGradientBoostingClassifier
from sklearn.kernel_approximation import Nystroem
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score,roc_curve
from threadpoolctl import threadpool_limits
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from atencion_binaria import FEATURES,representation,preprocessor,write,digest,ROOT
from reconstruir_profesor_atencion_binaria import components,fit_teacher,KEYS

OLD=ROOT/'resultados/profesor_binario_reconstruido_29-10-2026'
OUT=ROOT/'resultados/nuevos_modelos_atencion_binaria_29-10-2026'
SEED=20261031
GRIDS={
 'LDA':[{'shrinkage':'auto'},{'shrinkage':.5}],
 'QDA':[{'reg_param':.1},{'reg_param':.5}],
 'ExtraTrees':[{'min_samples_leaf':10,'max_depth':None},{'min_samples_leaf':25,'max_depth':8}],
 'HistBoost':[{'max_leaf_nodes':7,'l2_regularization':5.},{'max_leaf_nodes':15,'l2_regularization':15.}],
 'SVM_RBF_aprox':[{'C':.1},{'C':1.}],
}
BASELINES={'igualitario':('TCN','history'),'pca':('TCN','repeat_current')}

def macro_auc(frame,score):
    return float(np.mean([roc_auc_score(frame.iloc[ix].y,np.asarray(score)[ix]) for ix in frame.groupby('participant').indices.values() if frame.iloc[ix].y.nunique()==2]))

def choose(records):
    return sorted(records,key=lambda r:(-r['auc_inner'],r['family'],r['mode'],r['config_index']))[0]

def estimator(family,config,n_features):
    if family=='LDA':return LinearDiscriminantAnalysis(solver='lsqr',priors=[.5,.5],**config)
    if family=='QDA':return QuadraticDiscriminantAnalysis(priors=[.5,.5],**config)
    if family=='ExtraTrees':return ExtraTreesClassifier(n_estimators=250,max_features='sqrt',n_jobs=2,random_state=SEED,**config)
    if family=='HistBoost':return HistGradientBoostingClassifier(max_iter=200,learning_rate=.05,min_samples_leaf=30,early_stopping=False,random_state=SEED,**config)
    return Pipeline([('kernel',Nystroem(kernel='rbf',gamma=1/n_features,n_components=128,random_state=SEED,n_jobs=2)),
                     ('svm',LinearSVC(max_iter=10000,random_state=SEED,**config))])

def fit_estimator(fit,prep,mode,family,config):
    a,_,_=representation(prep,fit,mode); model=estimator(family,config,a.shape[1])
    counts=fit.groupby(['participant','y']).y.transform('size').to_numpy(); k=fit.groupby('participant').y.transform('nunique').to_numpy()
    weights=1/(counts*k); weights=weights/weights.mean()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        if family in ['LDA','QDA']:model.fit(a,fit.y)
        elif family=='SVM_RBF_aprox':model.fit(a,fit.y,svm__sample_weight=weights)
        else:model.fit(a,fit.y,sample_weight=weights)
    return model,[str(w.message) for w in caught]

def predict(bundle,frame):
    a,_,_=representation(bundle['prep'],frame,bundle['mode'])
    if bundle['family']=='SVM_RBF_aprox':return bundle['model'].decision_function(a)
    return bundle['model'].predict_proba(a)[:,1]

def labeled_frame(frame,z,people,kind):
    _,lab,_,_=fit_teacher(frame,z,people,kind)
    result=frame.assign(y=lab).dropna(subset=['y']).copy(); result['y']=result.y.astype(int)
    return result

def paired(values):
    values=np.asarray(values); rng=np.random.default_rng(SEED)
    boot=values[rng.integers(0,len(values),(2000,len(values)))].mean(axis=1)
    return dict(mean=float(values.mean()),ci_low=float(np.quantile(boot,.025)),ci_high=float(np.quantile(boot,.975)))

def summarize(tables):
    p=pd.concat(tables,ignore_index=True); p.to_csv(OUT/'predicciones_oof.csv.gz',index=False)
    metrics=[]; persons=[]; curves={}; grid=np.linspace(0,1,201)
    for (teacher,family,mode),g in p.groupby(['teacher','family','mode'],sort=False):
        scores=[]; rocs=[]
        for person,t in g.groupby('participant'):
            if t.y.nunique()!=2:raise ValueError('AUC indefinida')
            auc=roc_auc_score(t.y,t.score);scores.append(auc)
            persons.append(dict(teacher=teacher,family=family,mode=mode,participant=person,auc=auc))
            fpr,tpr,_=roc_curve(t.y,t.score);v=np.interp(grid,fpr,tpr);v[0]=0;v[-1]=1;rocs.append(v)
        ci=paired(scores)
        metrics.append(dict(teacher=teacher,family=family,mode=mode,auc_macro=ci['mean'],ci_low=ci['ci_low'],ci_high=ci['ci_high'],auc_pooled=roc_auc_score(g.y,g.score),n=len(g),participants=len(scores)))
        curves[(teacher,family,mode)]=np.mean(rocs,axis=0)
    m=pd.DataFrame(metrics); people=pd.DataFrame(persons);m.to_csv(OUT/'metricas.csv',index=False);people.to_csv(OUT/'metricas_participantes.csv',index=False)
    contrasts=[]; refs=[]
    for teacher,baseline in BASELINES.items():
        old=pd.read_csv(OLD/teacher/'metricas_participantes.csv');ref=old[old.family.eq(baseline[0])&old['mode'].eq(baseline[1])].set_index('participant').auc
        for (family,mode),g in people[people.teacher.eq(teacher)].groupby(['family','mode']):
            d=g.set_index('participant').auc-ref;ci=paired(d)
            refs.append(dict(teacher=teacher,family=family,mode=mode,reference_family=baseline[0],reference_mode=baseline[1],delta_auc=ci['mean'],ci_low=ci['ci_low'],ci_high=ci['ci_high'],improved_people=int(d.gt(0).sum())))
        for family in GRIDS:
            wide=people[people.teacher.eq(teacher)&people.family.eq(family)].pivot(index='participant',columns='mode',values='auc')
            d=wide['history']-wide['current'];ci=paired(d)
            contrasts.append(dict(teacher=teacher,family=family,delta_auc=ci['mean'],ci_low=ci['ci_low'],ci_high=ci['ci_high']))
    pd.DataFrame(refs).to_csv(OUT/'comparacion_referencia.csv',index=False);pd.DataFrame(contrasts).to_csv(OUT/'contrastes_temporalidad.csv',index=False)
    # Two panels per teacher; include the fixed previous reference in both panels.
    colors=dict(LDA='#1874b4',QDA='#b05caf',ExtraTrees='#d58320',HistBoost='#159c80',SVM_RBF_aprox='#c74c63',Seleccion_interna='#252525')
    fig,axes=plt.subplots(2,2,figsize=(13,11),layout='constrained')
    curve_rows=[]
    for row,teacher in enumerate(BASELINES):
        oldcurves=pd.read_csv(OLD/teacher/'curvas_roc.csv'); a,b=BASELINES[teacher]
        oldmetric=pd.read_csv(OLD/teacher/'metricas.csv');baseauc=oldmetric[oldmetric.family.eq(a)&oldmetric['mode'].eq(b)].auc_macro.iloc[0]
        for col,mode in enumerate(['current','history']):
            ax=axes[row,col]
            for family in GRIDS:
                tpr=curves[(teacher,family,mode)];auc=m[m.teacher.eq(teacher)&m.family.eq(family)&m['mode'].eq(mode)].auc_macro.iloc[0]
                ax.plot(grid,tpr,label=f'{family}: {auc:.3f}',color=colors[family],lw=1.6)
                curve_rows+= [dict(teacher=teacher,family=family,mode=mode,fpr=float(fpr),tpr=float(t)) for fpr,t in zip(grid,tpr)]
            ax.plot(oldcurves.fpr,oldcurves[f'{a}_{b}'],c='#222222',ls='--',label=f'TCN referencia: {baseauc:.3f}',lw=2)
            ax.plot([0,1],[0,1],':',c='#999999');ax.set(title=f"{teacher.upper() if teacher=='pca' else teacher} · {'actual' if mode=='current' else 'historial'}",xlabel='Tasa de falsos positivos',ylabel='Sensibilidad',xlim=(0,1),ylim=(0,1));ax.legend(fontsize=8,loc='lower right');ax.grid(alpha=.15)
    fig.suptitle('Nuevos modelos · atención binaria con etiquetas fijas\nROC media por participante; leyenda = ROC-AUC macro',fontsize=13)
    for ext in ['png','pdf']:fig.savefig(OUT/f'curvas_roc.{ext}',dpi=180)
    plt.close(fig);pd.DataFrame(curve_rows).to_csv(OUT/'curvas_roc.csv',index=False)
    report=['# Nuevos modelos de atención binaria — 29-10-2026','','Se conservan exactamente las etiquetas binarias reconstruidas y los folds externos de la corrida anterior. Solo train original; validation, test y P29 no se evalúan. Cinco familias nuevas × dos representaciones × dos profesores × cinco folds: 100 modelos externos y 200 ajustes internos. Parámetros escogidos por AUC macro en cuatro personas de validación interna, usando 16 personas para ajuste interno. PCA docente reajustado únicamente con personas del ajuste interno al seleccionar parámetros; en evaluación externa se conserva el profesor de fold anterior.','',
        '| Profesor | Modelo | Entrada | AUC macro | IC descriptivo 95 % |','|---|---|---|---:|---:|']
    for _,r in m.sort_values(['teacher','auc_macro'],ascending=[True,False]).iterrows():report.append(f"| {r.teacher} | {r.family} | {r['mode']} | {r.auc_macro:.4f} | [{r.ci_low:.4f}; {r.ci_high:.4f}] |")
    report+=['','## Frente a referencias anteriores fijas','','Igualitario: TCN con historial (0,6127). PCA: TCN con ventana actual repetida (0,6254). Estas referencias fueron escogidas antes de la corrida nueva. La fila Seleccion_interna muestra una selección de familia, representación y parámetros dentro de cada fold; no el máximo elegido mirando las predicciones externas.','',
        '| Profesor | Modelo / entrada | ΔAUC | IC descriptivo 95 % |','|---|---|---:|---:|']
    for r in sorted(refs,key=lambda r:(r['teacher'],-r['delta_auc'])):report.append(f"| {r['teacher']} | {r['family']} / {r['mode']} | {r['delta_auc']:+.4f} | [{r['ci_low']:+.4f}; {r['ci_high']:+.4f}] |")
    report+=['','## Alcance y reproducción','','Las etiquetas continúan siendo relativas a la mediana de cada persona y offline. Las dos tareas de profesores son distintas; mayor AUC para una no demuestra mejor validez de su etiqueta. Los intervalos remuestrean personas (2.000 réplicas), son descriptivos y no corrigen la búsqueda acumulada ni la selección adaptativa entre rondas.','',
        'LDA/QDA usan priors 0,5/0,5. Extra Trees, boosting y SVM reciben pesos inversos a participante/clase. SVM usa Nyström con 128 componentes y gamma=1/d seguido de LinearSVC: es una aproximación al kernel RBF. Sus salidas guardadas como score son márgenes, no probabilidades calibradas. AUC usa score continuo. Boosting usa 200 iteraciones fijas sin early stopping automático por ventanas. No se prueban umbrales de decisión. Los nuevos modelos usan una semilla fija; no se ha medido su variación entre semillas.','',
        'Historial = actual, media, desviación y cambio en hasta ocho ventanas consecutivas, reiniciado por segmento/hueco; preprocesamiento ajustado solo con train del nivel correspondiente. Los scores agrupados de SVM mezclan márgenes de modelos distintos; la métrica principal permanece AUC por persona.','',
        'Ejecutar `.venv/bin/python scripts/nuevos_modelos_atencion_binaria.py`. Reanuda tareas verificando hashes y protocolo. `busqueda_interna.csv` conserva los 200 intentos, hiperparámetros y advertencias; `selecciones.csv` registra elecciones previas a la evaluación externa. Los modelos internos y externos se guardan y se verifica recarga de externos.','',
        '[Protocolo](protocolo.json) · [Predicciones](predicciones_oof.csv.gz) · [Diferencias temporales](contrastes_temporalidad.csv)','','![ROC](curvas_roc.png)']
    (OUT/'INFORME.md').write_text('\n'.join(report)); print(m.sort_values(['teacher','auc_macro'],ascending=[True,False]).to_string(index=False),flush=True)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for sub in ['modelos','internos','predicciones','tareas']:(OUT/sub).mkdir(exist_ok=True)
    source=ROOT/'resultados/preprocesamiento/caracteristicas_multimodales.csv';partition=ROOT/'resultados/modelado/particion_participantes.csv'
    oldplan=json.loads((OLD/'protocolo.json').read_text()); raw=pd.read_csv(source);raw['source_row']=np.arange(len(raw));mapping=pd.read_csv(partition).set_index('participant').split
    raw['split']=raw.participant.map(mapping);frame=raw[raw.split.eq('train')].copy().sort_values(KEYS).reset_index(drop=True);z,_=components(frame)
    plan=dict(source_sha256=digest(source),partition_sha256=digest(partition),teacher_protocol_sha256=digest(OLD/'protocolo.json'),
        script_sha256=digest(Path(__file__)),representation_sha256=digest(ROOT/'scripts/atencion_binaria.py'),teacher_source_sha256=digest(ROOT/'scripts/reconstruir_profesor_atencion_binaria.py'),
        grids=GRIDS,folds=oldplan['folds'],features=FEATURES,baseline_references=BASELINES,seed=SEED,train_only=True,test_evaluated=False,validation_evaluated=False,
        selection='one grouped inner holdout per outer fold; family/mode/config chosen without outer scores',python=platform.python_version(),sklearn=sklearn.__version__)
    plan=json.loads(json.dumps(plan))
    assert digest(source)==oldplan['source_sha256'] and digest(partition)==oldplan['partition_sha256']
    if (OUT/'protocolo.json').exists():
        if json.loads((OUT/'protocolo.json').read_text())!=plan:raise ValueError('Protocolo cambiado')
    else:write(OUT/'protocolo.json',plan)
    allpred=[];allsearch=[];allselect=[];started=time.monotonic()
    with threadpool_limits(limits=2):
        for teacher in BASELINES:
            oldlabels=pd.read_csv(OLD/teacher/'etiquetas_profesor_oof.csv.gz').set_index('source_row')
            for fold in plan['folds']:
                outer=labeled_frame(frame,z,fold['fit'],teacher);inner=labeled_frame(frame,z,fold['inner_fit'],teacher)
                fit=outer[outer.participant.isin(fold['fit'])].reset_index(drop=True);val=outer[outer.participant.isin(fold['evaluation'])].reset_index(drop=True)
                ii=inner[inner.participant.isin(fold['inner_fit'])].reset_index(drop=True);vv=inner[inner.participant.isin(fold['inner_validation'])].reset_index(drop=True)
                assert set(ii.participant).isdisjoint(vv.participant);assert set(fit.participant).isdisjoint(val.participant)
                np.testing.assert_array_equal(val.y,oldlabels.loc[val.source_row].y)
                assert set(val.source_row)==set(oldlabels[oldlabels.fold.eq(fold['fold'])].index)
                innerprep=preprocessor().fit(ii[FEATURES]);outerprep=preprocessor().fit(fit[FEATURES]);foldchoices=[];foldpred={}
                for family,grid in GRIDS.items():
                    for mode in ['current','history']:
                        name=f"{teacher}_{family}_{mode}_fold{fold['fold']}";done=OUT/'tareas'/f'{name}.json'
                        if done.exists():
                            record=json.loads(done.read_text());predpath=OUT/record['prediction_path'];modelpath=OUT/record['model_path']
                            if digest(predpath)!=record['prediction_sha256'] or digest(modelpath)!=record['model_sha256']:raise ValueError('Artefacto alterado')
                            trials=record['trials'];selected=record['selected'];table=pd.read_csv(predpath)
                        else:
                            trials=[]
                            for index,config in enumerate(grid):
                                model,warns=fit_estimator(ii,innerprep,mode,family,config)
                                bundle=dict(model=model,prep=innerprep,mode=mode,family=family,config=config,fit_participants=sorted(ii.participant.unique()),features=FEATURES)
                                ipath=OUT/'internos'/f'{name}_config{index}.joblib';joblib.dump(bundle,ipath,compress=3)
                                score=predict(bundle,vv)
                                if not np.isfinite(score).all():raise ValueError('Score interno invalido')
                                trials.append(dict(teacher=teacher,fold=fold['fold'],family=family,mode=mode,config_index=index,config=config,auc_inner=macro_auc(vv,score),warnings=warns,
                                    inner_fit=fold['inner_fit'],inner_validation=fold['inner_validation'],model_path=str(ipath.relative_to(OUT)),model_sha256=digest(ipath)))
                            selected=choose(trials);model,warns=fit_estimator(fit,outerprep,mode,family,selected['config'])
                            bundle=dict(model=model,prep=outerprep,mode=mode,family=family,config=selected['config'],fit_participants=sorted(fit.participant.unique()),features=FEATURES,warnings=warns)
                            modelpath=OUT/'modelos'/f'{name}.joblib';joblib.dump(bundle,modelpath,compress=3)
                            score=predict(bundle,val);again=predict(joblib.load(modelpath),val);np.testing.assert_allclose(score,again,rtol=1e-7,atol=1e-9)
                            if not np.isfinite(score).all():raise ValueError('Score externo invalido')
                            table=val[['source_row','participant','y']].copy().assign(score=score,teacher=teacher,family=family,mode=mode,fold=fold['fold'])
                            predpath=OUT/'predicciones'/f'{name}.csv.gz';table.to_csv(predpath,index=False)
                            record=dict(selected=selected,trials=trials,outer_warnings=warns,model_path=str(modelpath.relative_to(OUT)),model_sha256=digest(modelpath),prediction_path=str(predpath.relative_to(OUT)),prediction_sha256=digest(predpath))
                            write(done,record)
                        np.testing.assert_array_equal(table.source_row,val.source_row);np.testing.assert_array_equal(table.y,val.y)
                        allpred.append(table);allsearch+=trials;allselect.append(selected);foldchoices.append(selected);foldpred[(family,mode)]=table
                        print(f'{name} · config={selected["config_index"]} inner={selected["auc_inner"]:.4f} · {time.monotonic()-started:.1f}s',flush=True)
                joint=choose(foldchoices);chosen=foldpred[(joint['family'],joint['mode'])].copy();chosen['family']='Seleccion_interna';chosen['mode']='selected'
                allpred.append(chosen);allselect.append(dict(joint,selection_type='joint_family_mode'))
                pd.DataFrame(allsearch).to_csv(OUT/'busqueda_interna.csv',index=False);pd.DataFrame(allselect).to_csv(OUT/'selecciones.csv',index=False)
    summarize(allpred)
    p=pd.concat(allpred)
    for key,g in p.groupby(['teacher','family','mode']):
        assert len(g)==13498 and not g.source_row.duplicated().any()
    write(OUT/'verificacion.json',dict(complete=True,outer_models=100,inner_models=200,predictions=len(p),teachers=2,participants=25,rows_per_variant=13498,outer_reload_verified=True,old_labels_matched=True,oof_coverage_verified=True))
if __name__=='__main__':main()
