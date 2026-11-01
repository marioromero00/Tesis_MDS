"""Contraste exploratorio fijo de historial sobre etiquetas V2; solo train."""
import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from threadpoolctl import threadpool_limits
from atencion_binaria import ROOT, digest, write
from comparacion_comun_binaria import representation
from diagnostico_busqueda_activacion import weights
from temporales_core import preprocessor, history_indices
from evaluar_temporalidad_eeg_v2 import ci
from reconstruir_profesor_atencion_binaria import KEYS

OUT = ROOT / 'resultados/activacion_v2_historial_01-11-2026'

def main():
    OUT.mkdir(exist_ok=False)
    (OUT / 'modelos').mkdir()
    source = ROOT / 'resultados/preprocesamiento/caracteristicas_multimodales.csv'
    labels_path = ROOT / 'resultados/etiquetas_gsr_calidad_v2_01-11-2026/etiquetas.csv.gz'
    spatial_path = ROOT / 'resultados/eeg_por_canal_v2_29-10-2026/caracteristicas_eeg_por_canal.csv.gz'
    split_path = ROOT / 'resultados/modelado/particion_participantes.csv'
    folds_path = ROOT / 'resultados/profesor_binario_reconstruido_29-10-2026/protocolo.json'
    groups = json.loads((ROOT / 'resultados/comparacion_comun_binaria_30-10-2026/protocolo.json').read_text())['groups']['activacion']
    cols = sum(groups.values(), [])
    assert not any('gsr' in c.lower() or 'arousal' in c.lower() for c in cols)
    folds = json.loads(folds_path.read_text())['folds']
    inputs = {str(p.relative_to(ROOT)): digest(p) for p in [source, labels_path, spatial_path, split_path, folds_path]}
    write(OUT / 'protocolo.json', dict(inputs=inputs, script_sha256=digest(Path(__file__)), contexts=[1,8,32], features=cols, folds=folds, model='LogisticRegression C=1 max_iter=4000 random_state=20261101', selection='fixed, no hyperparameter search or winner selection', metric='mean participant ROC-AUC', train_only=True, history='current plus mean and SD; only retained labelled rows; reset at gaps/recording/segment/stimulus', limitations='exploratory reused train; offline pseudo-labels; not comparable as improvement against old labels; historical aggregation is not order-sensitive sequence modeling'))
    raw = pd.read_csv(source)
    raw['source_row'] = np.arange(len(raw))
    parts = pd.read_csv(split_path).set_index('participant').split
    raw['split'] = raw.participant.map(parts)
    raw = raw[raw.split.eq('train')].copy()
    channel = [c for c in cols if c.startswith(('eegch','eegsp'))]
    raw = raw.merge(pd.read_csv(spatial_path)[['source_row']+channel], on='source_row', validate='one_to_one')
    labels = pd.read_csv(labels_path)
    labels = labels[labels.split.eq('train') & labels.activation_binary_v2.notna()].copy()
    f = raw.merge(labels[['source_row','activation_binary_v2']], on='source_row', validate='one_to_one').rename(columns={'activation_binary_v2':'y'}).sort_values(KEYS).reset_index(drop=True)
    assert len(f) == len(labels) and f.split.eq('train').all()
    assert (f.groupby('participant').y.nunique() == 2).all()
    f['y'] = f.y.astype(int)
    f[['source_row','participant','split','y']].to_csv(OUT/'filas_train.csv.gz',index=False)
    history=[]
    for ctx in [1,8,32]:
        _,length = history_indices(f,ctx)
        for person,ix in f.groupby('participant').indices.items():
            history.append(dict(participant=person,context=ctx,windows=len(ix),mean_history=float(length[ix].mean()),full_history_fraction=float((length[ix]==ctx).mean())))
    pd.DataFrame(history).to_csv(OUT/'cobertura_historial.csv',index=False)
    predictions=[]
    for fold in folds:
        fit=f[f.participant.isin(fold['fit'])].reset_index(drop=True)
        val=f[f.participant.isin(fold['evaluation'])].reset_index(drop=True)
        assert set(fit.participant).isdisjoint(val.participant)
        prep=preprocessor().fit(fit[cols])
        for ctx in [1,8,32]:
            model=LogisticRegression(C=1,max_iter=4000,random_state=20261101)
            model.fit(representation(prep,fit,cols,ctx),fit.y,sample_weight=weights(fit))
            assert model.n_iter_.max()<4000, 'No convergence'
            prob=model.predict_proba(representation(prep,val,cols,ctx))[:,1]
            path=OUT/'modelos'/f"fold{fold['fold']}_ctx{ctx}.joblib"
            joblib.dump(dict(model=model,prep=prep,cols=cols,context=ctx,fit_people=fold['fit']),path,compress=3)
            loaded=joblib.load(path)
            np.testing.assert_allclose(prob,loaded['model'].predict_proba(representation(loaded['prep'],val,cols,ctx))[:,1],atol=1e-12)
            predictions.append(val[['source_row','participant','y']].assign(prob=prob,context=ctx,fold=fold['fold']))
            pd.concat(predictions).to_csv(OUT/'predicciones_oof.csv.gz',index=False)
            print('Completado fold',fold['fold'],'contexto',ctx,flush=True)
    pred=pd.read_csv(OUT/'predicciones_oof.csv.gz')
    people=[]
    for (ctx,person),g in pred.groupby(['context','participant']):
        people.append(dict(context=ctx,participant=person,auc=roc_auc_score(g.y,g.prob),windows=len(g)))
    people=pd.DataFrame(people)
    people.to_csv(OUT/'metricas_personas.csv',index=False)
    summary=[];contrasts=[]
    for ctx,g in pred.groupby('context'):
        assert not g.source_row.duplicated().any() and len(g)==len(f)
        np.testing.assert_array_equal(g.sort_values('source_row').y,f.sort_values('source_row').y)
        np.testing.assert_array_equal(g.sort_values('source_row').source_row,f.sort_values('source_row').source_row)
        mean,low,high=ci(people[people.context.eq(ctx)].auc)
        summary.append(dict(context=ctx,auc=mean,low=low,high=high))
    wide=people.pivot(index='participant',columns='context',values='auc')
    for ctx in [8,32]:
        delta=wide[ctx]-wide[1];mean,low,high=ci(delta)
        contrasts.append(dict(context=ctx,delta=mean,low=low,high=high,improved=int((delta>0).sum())))
    pd.DataFrame(summary).to_csv(OUT/'metricas.csv',index=False)
    pd.DataFrame(contrasts).to_csv(OUT/'contrastes.csv',index=False)
    assert all(digest(ROOT/p)==h for p,h in inputs.items())
    write(OUT/'auditoria.json',dict(passed=True,models=15,rows_per_context=len(f),people=f.participant.nunique(),same_rows_and_labels=True,inputs_unchanged=True,reload_verified=True,validation_evaluated=False,test_evaluated=False))
    lines=['# Activación V2: primer contraste fijo de historial','','Regresión logística C=1 en los cinco folds heredados de train. Mismas filas y etiquetas V2 en los tres contextos; preprocesamiento ajustado solo en personas de entrenamiento de cada fold. Modelo fijo sin búsqueda ni selección por resultados. EEG, mirada y pupila como entradas; GSR reservado al profesor.','','| Contexto | AUC macro persona | IC descriptivo 95% |','|---|---|---|']
    for r in summary:lines.append(f"| {r['context']} | {r['auc']:.4f} | [{r['low']:.4f}; {r['high']:.4f}] |")
    lines+=['','| Historial menos actual | ΔAUC | IC descriptivo 95% | Personas mejoran |','|---|---|---|---|']
    for r in contrasts:lines.append(f"| {r['context']} | {r['delta']:+.4f} | [{r['low']:.4f}; {r['high']:.4f}] | {r['improved']}/{len(wide)} |")
    lines+=['','El historial se limita a ventanas retenidas consecutivas; se reinicia en huecos y cambios de segmento. Consultar cobertura_historial.csv. Son agregados históricos, no modelos sensibles al orden de la secuencia. Los intervalos bootstrap por persona son descriptivos, sin corrección por comparaciones múltiples. Train fue reutilizado históricamente. No se evaluó validation ni test. Las etiquetas offline no validan un constructo psicológico y cambiaron frente a las corridas anteriores: no interpretar diferencias de AUC entre versiones como mejora del modelo.']
    (OUT/'INFORME.md').write_text('\n'.join(lines)+'\n')
    print(pd.DataFrame(summary).to_string(index=False),flush=True)
    print(pd.DataFrame(contrasts).to_string(index=False),flush=True)

if __name__=='__main__':
    with threadpool_limits(limits=2):main()
