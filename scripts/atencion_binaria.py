"""Atencion binaria: ROC/AUC OOF por participante, sin consultar validation/test."""
from __future__ import annotations
import argparse, json, time, platform
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import sklearn
import torch
from torch import nn
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, roc_curve, balanced_accuracy_score, average_precision_score
from threadpoolctl import threadpool_limits
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from baselines_estaticos import EEG, GSR, validate_partition
from temporales_core import ROOT, history_indices, sequence_array, preprocessor, TemporalNet, raw_predict, seed_all, digest

FEATURES = EEG + GSR
SEEDS = [20261029, 20261030]
EPOCHS = 8
VARIANTS = [('Dummy','current'), ('Logistica','current'), ('Logistica','history'),
            ('RandomForest','current'), ('RandomForest','history'), ('MLP_current','current'),
            ('TCN','repeat_current'), ('TCN','history'), ('LSTM','repeat_current'), ('LSTM','history')]
LABELS = {'current':'actual', 'history':'historial', 'repeat_current':'actual repetida'}

def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False))

def representation(prep, frame, mode):
    z = prep.transform(frame[FEATURES]).astype('float32')
    ix, lengths = history_indices(frame, 8)
    x = sequence_array(z, ix)
    if mode == 'repeat_current':
        for i, n in enumerate(lengths): x[i,:n] = z[i]
    mask = np.arange(8)[None,:] < lengths[:,None]
    mean = x.sum(axis=1) / lengths[:,None]
    var = ((x-mean[:,None,:])**2 * mask[:,:,None]).sum(axis=1)/lengths[:,None]
    first = x[:,0]
    classical = np.column_stack([z, mean, np.sqrt(np.maximum(var,0)), z-first]) if mode == 'history' else z
    return classical, x, lengths

def train_predict(fit, val, family, mode, seed, path):
    prep = preprocessor().fit(fit[FEATURES])
    a,x,l = representation(prep,fit,mode)
    b,v,ll = representation(prep,val,mode)
    y = fit.y.to_numpy()
    loss_curve=[]
    if family == 'Dummy':
        score=np.full(len(val),y.mean()); bundle={'prior':float(y.mean()),'prep':prep}
    elif family in ['Logistica','RandomForest']:
        model = (LogisticRegression(C=1,max_iter=2000,class_weight='balanced',random_state=seed)
                 if family=='Logistica' else RandomForestClassifier(n_estimators=200,min_samples_leaf=10,
                    max_features='sqrt',class_weight='balanced',random_state=seed,n_jobs=2))
        model.fit(a,y); score=model.predict_proba(b)[:,1]
        bundle={'model':model,'prep':prep,'mode':mode}
    else:
        seed_all(seed); torch.set_num_threads(2)
        model=TemporalNet(family,x.shape[2],2,hidden=24,dropout=.2)
        optimizer=torch.optim.AdamW(model.parameters(),lr=.001,weight_decay=.01)
        counts=fit.groupby(['participant','y']).y.transform('size').to_numpy()
        k=fit.groupby('participant').y.transform('nunique').to_numpy()
        weights=1/(counts*k); weights=weights/weights.mean()
        xx, yy, lens = torch.from_numpy(x),torch.tensor(y,dtype=torch.long),torch.from_numpy(l)
        ww=torch.tensor(weights,dtype=torch.float32)
        for epoch in range(EPOCHS):
            model.train(); order=torch.randperm(len(y)); total=0.
            for start in range(0,len(y),256):
                ids=order[start:start+256]; optimizer.zero_grad(set_to_none=True)
                loss=(nn.functional.cross_entropy(model(xx[ids],lens[ids]),yy[ids],reduction='none')*ww[ids]).mean()
                if not torch.isfinite(loss): raise ValueError('Loss no finita')
                loss.backward(); nn.utils.clip_grad_norm_(model.parameters(),1.); optimizer.step()
                total+=loss.item()*len(ids)
            loss_curve.append(total/len(y))
        score=torch.softmax(torch.from_numpy(raw_predict(model,v,ll)),dim=1).numpy()[:,1]
        bundle={'state':model.state_dict(),'prep':prep,'family':family,'mode':mode,'inputs':x.shape[2], 'hidden':24,'dropout':.2}
    bundle.update(features=FEATURES,seed=seed,fit_participants=sorted(fit.participant.unique()),loss=loss_curve)
    joblib.dump(bundle,path,compress=3)
    loaded=joblib.load(path)
    # Independent reconstruction from saved preprocessing and weights.
    bb,vv,lll=representation(loaded['prep'],val,mode)
    if family=='Dummy': again=np.full(len(val),loaded['prior'])
    elif family in ['Logistica','RandomForest']: again=loaded['model'].predict_proba(bb)[:,1]
    else:
        restored=TemporalNet(loaded['family'],loaded['inputs'],2,loaded['hidden'],loaded['dropout'])
        restored.load_state_dict(loaded['state'])
        again=torch.softmax(torch.from_numpy(raw_predict(restored,vv,lll)),dim=1).numpy()[:,1]
    np.testing.assert_allclose(score,again,atol=1e-7,rtol=1e-6)
    if not np.isfinite(score).all() or ((score<0)|(score>1)).any(): raise ValueError('Probabilidad invalida')
    return score

def summarize(out, frames):
    predictions=pd.concat(frames,ignore_index=True)
    predictions.to_csv(out/'predicciones_oof.csv.gz',index=False)
    # Average seeds on identical held-out rows, never across train/evaluation.
    avg=predictions.groupby(['family','mode','source_row','participant','fold','y'],as_index=False).prob.mean()
    people=[]; rows=[]; grid=np.linspace(0,1,201); curves={}
    for (family,mode), table in avg.groupby(['family','mode'],sort=False):
        person_curves=[]
        for person,g in table.groupby('participant'):
            valid=g.y.nunique()==2
            auc=roc_auc_score(g.y,g.prob) if valid else np.nan
            people.append(dict(family=family,mode=mode,participant=person,auc=auc,
                ba=balanced_accuracy_score(g.y,g.prob>=.5),n=len(g),positive_rate=g.y.mean()))
            if valid:
                fpr,tpr,_=roc_curve(g.y,g.prob); interp=np.interp(grid,fpr,tpr); interp[0]=0; interp[-1]=1
                person_curves.append(interp)
        p=pd.DataFrame([r for r in people if r['family']==family and r['mode']==mode])
        values=p.auc.dropna().to_numpy(); rng=np.random.default_rng(20261029)
        boot=values[rng.integers(0,len(values),(2000,len(values)))].mean(axis=1)
        rows.append(dict(family=family,mode=mode,auc_macro=values.mean(),ci_low=np.quantile(boot,.025),
            ci_high=np.quantile(boot,.975),auc_pooled=roc_auc_score(table.y,table.prob),
            average_precision_pooled=average_precision_score(table.y,table.prob),ba_macro=p.ba.mean(),
            participants=len(p),participants_auc=len(values),n=len(table)))
        curves[(family,mode)]=np.mean(person_curves,axis=0)
    metrics=pd.DataFrame(rows); persons=pd.DataFrame(people)
    metrics.to_csv(out/'metricas.csv',index=False); persons.to_csv(out/'metricas_participantes.csv',index=False)
    contrasts=[]
    for family in ['Logistica','RandomForest','TCN','LSTM']:
        baseline='repeat_current' if family in ['TCN','LSTM'] else 'current'
        wide=persons[persons.family.eq(family)].pivot(index='participant',columns='mode',values='auc').dropna()
        delta=(wide['history']-wide[baseline]).to_numpy(); rng=np.random.default_rng(20261029)
        boot=delta[rng.integers(0,len(delta),(2000,len(delta)))].mean(axis=1)
        contrasts.append(dict(family=family,baseline=baseline,delta_auc=delta.mean(),
            ci_low=np.quantile(boot,.025),ci_high=np.quantile(boot,.975),participants=len(delta)))
    pd.DataFrame(contrasts).to_csv(out/'contrastes_temporalidad.csv',index=False)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(1,2,figsize=(14,6),layout='constrained')
    colors={'Dummy':'#888888','Logistica':'#1874b4','RandomForest':'#dd7c16','MLP_current':'#9270b2','TCN':'#169878','LSTM':'#cf4d70'}
    for (family,mode), tpr in curves.items():
        ax=axes[1 if mode=='history' else 0]
        row=metrics[(metrics.family==family)&(metrics['mode']==mode)].iloc[0]
        name='MLP' if family=='MLP_current' else family
        suffix=' (control)' if mode=='repeat_current' else ''
        ax.plot(grid,tpr,color=colors[family],label=f'{name}{suffix}: {row.auc_macro:.3f}',lw=2)
    for ax,title in zip(axes,['Sin historial: ventana actual','Con historial causal: hasta 8 ventanas']):
        ax.plot([0,1],[0,1],'--',c='#999999',lw=1); ax.set(xlabel='Tasa de falsos positivos',ylabel='Sensibilidad',title=title,xlim=(0,1),ylim=(0,1))
        ax.legend(loc='lower right',fontsize=9); ax.grid(alpha=.15)
    fig.suptitle('Atención binaria · ROC media por participante\nPredicciones fuera de fold en train; leyenda = AUC macro por persona',fontsize=13)
    for ext in ['png','pdf']: fig.savefig(out/f'curvas_roc.{ext}',dpi=180)
    plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,6),layout='constrained')
    order=metrics.sort_values('auc_macro'); labels=[('MLP' if r.family=='MLP_current' else r.family)+' · '+LABELS[r['mode']] for _,r in order.iterrows()]
    ax.errorbar(order.auc_macro,np.arange(len(order)),xerr=np.vstack([order.auc_macro-order.ci_low,order.ci_high-order.auc_macro]),fmt='o',color='#1874b4',capsize=3)
    ax.set(yticks=np.arange(len(order)),yticklabels=labels,xlabel='ROC-AUC macro por participante · IC descriptivo 95 %',title='Comparación de modelos para atención binaria')
    ax.axvline(.5,color='#999999',ls='--'); ax.grid(axis='x',alpha=.2)
    for ext in ['png','pdf']: fig.savefig(out/f'comparacion_auc.{ext}',dpi=180)
    plt.close(fig)
    curve_table=pd.DataFrame({'fpr':grid,**{f'{a}_{b}':c for (a,b),c in curves.items()}}); curve_table.to_csv(out/'curvas_roc.csv',index=False)
    report=['# Atención binaria — 29-10-2026','', 'Definición: '+json.loads((out/'protocolo.json').read_text())['binary_definition'], '',
        'Entradas: EEG y GSR; mirada/pupila excluidas porque generan la pseudoetiqueta. Cinco folds originales de atención por participante, solo train. Predicciones de dos semillas promediadas en redes; hiperparámetros y ocho épocas fijados antes de evaluar. Historial: hasta ocho ventanas consecutivas, reiniciado en cambios de segmento o huecos; incluye la ventana actual. Las ventanas duran 2 s y avanzan 1 s: cobertura máxima 9 s.', '',
        '| Modelo | Entrada | AUC macro | IC descriptivo 95 % | AUC agrupada |', '|---|---|---:|---:|---:|']
    for _,r in metrics.sort_values('auc_macro',ascending=False).iterrows(): report.append(f"| {r.family} | {LABELS[r['mode']]} | {r.auc_macro:.4f} | [{r.ci_low:.4f}, {r.ci_high:.4f}] | {r.auc_pooled:.4f} |")
    report+=['','## Efecto pareado del historial','']
    for r in contrasts: report.append(f"- {r['family']}: ΔAUC {r['delta_auc']:+.4f}, IC [{r['ci_low']:+.4f}, {r['ci_high']:+.4f}].")
    report+=['','Las curvas promedian ROC por persona; el AUC principal promedia AUC individuales (no el área numérica de la curva interpolada). Los intervalos remuestrean participantes, no ventanas. Personas con una sola clase se excluyen de AUC y se cuentan en metricas.csv. El control temporal repite la ventana actual conservando arquitectura y longitud disponible. Logística/RF con historial reciben actual, media, desviación y cambio respecto a la primera ventana. Umbral 0,5 solo para BA; AUC usa puntuaciones continuas. No se seleccionaron umbrales con evaluación externa.', '',
        'Resultado exploratorio sobre train ya reutilizado en estudios anteriores. La nueva tarea binaria no se compara directamente con la BA ternaria. No demuestra atención psicológica validada ni mejora confirmatoria en personas nuevas. Validation, test y P29 no se evaluaron. Preprocesamiento previo y pseudoetiquetas offline conservan las limitaciones del dataset original.','', '![Curvas ROC](curvas_roc.png)','', '![Comparación AUC](comparacion_auc.png)']
    (out/'INFORME.md').write_text('\n'.join(report),encoding='utf-8')
    print(metrics.to_string(index=False),flush=True)

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--positive',choices=['high','medium-high'],default='high'); parser.add_argument('--output',required=True); args=parser.parse_args()
    out=Path(args.output).resolve(); out.mkdir(parents=True,exist_ok=True)
    for sub in ['modelos','predicciones']: (out/sub).mkdir(exist_ok=True)
    dataset=ROOT/'resultados/modelado/dataset_modelado.csv'; partition=ROOT/'resultados/modelado/particion_participantes.csv'
    data=pd.read_csv(dataset); data['source_row']=np.arange(len(data)); validate_partition(data,pd.read_csv(partition))
    frame=data[data.split.eq('train')&data.attention_label_equal.notna()].copy()
    if not frame.attention_label_equal.isin(['bajo','medio','alto']).all(): raise ValueError('Etiqueta invalida')
    frame['y']=(frame.attention_label_equal.eq('alto') if args.positive=='high' else frame.attention_label_equal.ne('bajo')).astype(int)
    frame=frame.sort_values(['participant','recording','segment_id','stimulus','window_start_utc']).reset_index(drop=True)
    folds=json.loads((ROOT/'resultados/contraste_temporalidad_fusion_24-10-2026/protocolo.json').read_text())['folds']['attention']
    if set(frame.participant)!=set(p for f in folds for p in f['evaluation']): raise ValueError('Participantes inesperados')
    plan={'binary_definition':'1 = alta; 0 = media/baja' if args.positive=='high' else '1 = media/alta; 0 = baja',
          'target_original':'attention_label_equal','positive':args.positive,'features':FEATURES,'folds':folds,'variants':VARIANTS,
          'seeds':SEEDS,'epochs':EPOCHS,'context_windows':8,'dataset_sha256':digest(dataset),'partition_sha256':digest(partition),
          'source_sha256':digest(Path(__file__)),'train_only':True,'validation_evaluated':False,'test_evaluated':False,
          'python':platform.python_version(),'sklearn':sklearn.__version__,'torch':torch.__version__,
          'classical_config':{'logistic_C':1,'rf_trees':200,'rf_min_leaf':10},'neural_config':{'hidden':24,'dropout':.2,'lr':.001,'weight_decay':.01,'batch':256}}
    # JSON roundtrip normalizes tuples for strict resume comparison.
    plan=json.loads(json.dumps(plan))
    if (out/'protocolo.json').exists():
        if json.loads((out/'protocolo.json').read_text())!=plan: raise ValueError('No reanudar con protocolo cambiado')
    else: write(out/'protocolo.json',plan)
    tables=[]; started=time.time()
    with threadpool_limits(limits=2):
        for fold in folds:
            fit=frame[frame.participant.isin(fold['fit'])].reset_index(drop=True)
            val=frame[frame.participant.isin(fold['evaluation'])].reset_index(drop=True)
            assert set(fit.participant).isdisjoint(val.participant)
            for family,mode in VARIANTS:
                seeds=SEEDS if family in ['MLP_current','TCN','LSTM'] else SEEDS[:1]
                for seed in seeds:
                    name=f"{family}_{mode}_fold{fold['fold']}_{seed}"; pred=out/'predicciones'/f'{name}.csv.gz'; model=out/'modelos'/f'{name}.joblib'
                    if pred.exists():
                        t=pd.read_csv(pred)
                        audit=json.loads((out/'predicciones'/f'{name}.json').read_text())
                        if digest(pred)!=audit['predictions_sha256'] or digest(model)!=audit['model_sha256']: raise ValueError('Artefacto alterado')
                    else:
                        score=train_predict(fit,val,family,mode,seed,model)
                        t=val[['source_row','participant','y']].copy(); t['prob']=score
                        t=t.assign(family=family,mode=mode,fold=fold['fold'],seed=seed); t.to_csv(pred,index=False)
                        write(out/'predicciones'/f'{name}.json',{'model_sha256':digest(model),'predictions_sha256':digest(pred)})
                    np.testing.assert_array_equal(t.source_row,val.source_row)
                    np.testing.assert_array_equal(t.y,val.y)
                    tables.append(t)
                    print(f'{name} completado · {time.time()-started:.1f}s acumulados',flush=True)
    summarize(out,tables)
    allp=pd.concat(tables); expected={(a,b):len(SEEDS) if a in ['MLP_current','TCN','LSTM'] else 1 for a,b in VARIANTS}
    for (a,b),n in expected.items():
        counts=allp[(allp.family==a)&(allp['mode']==b)].groupby('source_row').size()
        assert len(counts)==len(frame) and counts.eq(n).all()
    write(out/'verificacion.json',{'complete':True,'rows_train':len(frame),'participants':frame.participant.nunique(),
        'positive_rate':float(frame.y.mean()),'models':len(list((out/'modelos').glob('*.joblib'))),
        'predictions':len(allp),'reload_predictions_verified':True,'oof_coverage_verified':True})

if __name__=='__main__': main()
