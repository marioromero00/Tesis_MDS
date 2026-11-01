"""Auditoría separada de test, etiquetas, controles y contrastes por persona."""
import json
from pathlib import Path
import pandas as pd,numpy as np,joblib
from sklearn.metrics import roc_auc_score
from threadpoolctl import threadpool_limits
from evaluar_test_temporalidad_eeg_v2 import ROOT,OUT,BASE,KEYS,digest,label_with_teacher,score_bundle,ci,write

def main():
    plan=json.loads((OUT/'protocolo_pre_test.json').read_text());frozen=json.loads((OUT/'congelacion_pre_test.json').read_text())
    assert digest(ROOT/'scripts/evaluar_test_temporalidad_eeg_v2.py')==plan['script_sha256']
    assert digest(BASE/'congelacion_pre_validation.json')==plan['previous_freeze_sha256']
    teacher=joblib.load(BASE/'profesor_final.joblib');assert digest(BASE/'profesor_final.joblib')==frozen['teacher_sha256']
    raw=pd.read_csv(ROOT/'resultados/preprocesamiento/caracteristicas_multimodales.csv');raw['source_row']=np.arange(len(raw))
    raw['split']=raw.participant.map(pd.read_csv(ROOT/'resultados/modelado/particion_participantes.csv').set_index('participant').split)
    fit_people=set(raw[raw.split.eq('train')].participant);assert set(teacher['fit_participants'])==fit_people
    channel=OUT/'caracteristicas_test.csv.gz';assert digest(channel)==json.loads((OUT/'auditoria_extraccion.json').read_text())['sha256']
    test=raw[raw.split.eq('test')].merge(pd.read_csv(channel),on='source_row',validate='one_to_one').sort_values(KEYS).reset_index(drop=True)
    assert test.participant.nunique()==8 and set(test.participant).isdisjoint(fit_people)
    labels,_=label_with_teacher(test,teacher);test=test.assign(y=labels).dropna(subset=['y']).copy();test['y']=test.y.astype(int);test=test.reset_index(drop=True)
    pred=pd.read_csv(OUT/'predicciones_test.csv.gz');metrics=pd.read_csv(OUT/'metricas.csv');people=[];bundles={}
    for name,meta in frozen['models'].items():
        path=Path(meta['path']);assert digest(path)==meta['sha256'];bundle=joblib.load(path);bundles[name]=bundle
        assert set(bundle['fit_participants'])==fit_people
        t=pred[pred.strategy.eq(name)].reset_index(drop=True);assert not t.source_row.duplicated().any()
        pd.testing.assert_frame_equal(t[['source_row','participant','y']],test[['source_row','participant','y']])
        np.testing.assert_allclose(score_bundle(bundle,test),t.prob,atol=1e-8,rtol=1e-7)
        vals=[]
        for person,g in t.groupby('participant'):
            a=roc_auc_score(g.y,g.prob);vals.append(a);people.append(dict(strategy=name,participant=person,auc=a))
        r=metrics[metrics.strategy.eq(name)].iloc[0];np.testing.assert_allclose(ci(vals),[r.auc_macro,r.ci_low,r.ci_high],atol=1e-12)
    for scope in ['inductivo','relativo_offline']:
        temporal=bundles[f'{scope}_ctx32']['candidate'];static=bundles[f'{scope}_estatico_pareado']['candidate']
        assert temporal['params']==static['params'] and temporal['family']==static['family'] and static['context']==1
    wide=pd.DataFrame(people).pivot(index='participant',columns='strategy',values='auc')
    for r in pd.read_csv(OUT/'contrastes.csv').itertuples():
        d=wide[r.temporal]-wide[r.baseline];np.testing.assert_allclose(ci(d),[r.delta_auc,r.ci_low,r.ci_high],atol=1e-12);assert sum(d>0)==r.improved_people
    write(OUT/'auditoria_independiente.json',dict(passed=True,labels_recomputed=True,models_reloaded=8,participant_metrics_recomputed=64,contrasts_recomputed=8,matched_family_params_verified=True,train_test_disjoint=True))
    print('AUDITORÍA TEST INDEPENDIENTE OK')
if __name__=='__main__':
    with threadpool_limits(limits=2):main()
