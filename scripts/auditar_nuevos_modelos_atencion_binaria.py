"""Comprueba modelos, eleccion interna, etiquetas fijas y metricas nuevas."""
import json,hashlib
from pathlib import Path
import joblib,numpy as np,pandas as pd
from sklearn.metrics import roc_auc_score
from nuevos_modelos_atencion_binaria import ROOT,OUT,OLD,choose,predict

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    plan=json.loads((OUT/'protocolo.json').read_text());p=pd.read_csv(OUT/'predicciones_oof.csv.gz');m=pd.read_csv(OUT/'metricas.csv')
    folds={f['fold']:f for f in plan['folds']};checked=0;inner=0
    oldlabels={t:pd.read_csv(OLD/t/'etiquetas_profesor_oof.csv.gz').set_index('source_row') for t in ['igualitario','pca']}
    raw=pd.read_csv(ROOT/'resultados/preprocesamiento/caracteristicas_multimodales.csv');raw['source_row']=np.arange(len(raw))
    parts=pd.read_csv(ROOT/'resultados/modelado/particion_participantes.csv').set_index('participant').split
    raw['split']=raw.participant.map(parts)
    assert sha(ROOT/'resultados/preprocesamiento/caracteristicas_multimodales.csv')==plan['source_sha256']
    for path in (OUT/'tareas').glob('*.json'):
        task=json.loads(path.read_text());s=task['selected'];fold=folds[s['fold']]
        chosen=choose(task['trials']);assert chosen==s
        assert set(fold['inner_fit']).isdisjoint(fold['inner_validation']);assert set(fold['fit']).isdisjoint(fold['evaluation'])
        assert set(fold['inner_fit'])|set(fold['inner_validation'])==set(fold['fit'])
        for trial in task['trials']:
            assert sha(OUT/trial['model_path'])==trial['model_sha256']
            bundle=joblib.load(OUT/trial['model_path']);assert set(bundle['fit_participants'])==set(fold['inner_fit'])
            assert set(bundle['features'])==set(plan['features']);inner+=1
        assert sha(OUT/task['model_path'])==task['model_sha256'];assert sha(OUT/task['prediction_path'])==task['prediction_sha256']
        bundle=joblib.load(OUT/task['model_path']);assert set(bundle['fit_participants'])==set(fold['fit'])
        t=pd.read_csv(OUT/task['prediction_path']);ref=oldlabels[s['teacher']].loc[t.source_row]
        np.testing.assert_array_equal(t.y,ref.y);np.testing.assert_array_equal(t.participant,ref.participant)
        assert set(t.participant)==set(fold['evaluation'])
        val=raw.set_index('source_row',drop=False).loc[t.source_row].reset_index(drop=True)
        np.testing.assert_allclose(predict(bundle,val),t.score,atol=1e-8,rtol=1e-7)
        assert val.split.eq('train').all();checked+=1
    assert checked==100 and inner==200
    for (teacher,family,mode),g in p.groupby(['teacher','family','mode']):
        assert len(g)==13498 and not g.source_row.duplicated().any()
        ref=oldlabels[teacher].loc[g.source_row];np.testing.assert_array_equal(g.y,ref.y)
        auc=np.mean([roc_auc_score(t.y,t.score) for _,t in g.groupby('participant')])
        reported=m[m.teacher.eq(teacher)&m.family.eq(family)&m['mode'].eq(mode)].auc_macro.iloc[0]
        np.testing.assert_allclose(auc,reported,atol=1e-12)
        if family=='Seleccion_interna':
            for fold,gf in g.groupby('fold'):
                candidates=[json.loads(path.read_text())['selected'] for path in (OUT/'tareas').glob('*.json')]
                best=choose([v for v in candidates if v['teacher']==teacher and v['fold']==fold])
                original=p[p.teacher.eq(teacher)&p.family.eq(best['family'])&p['mode'].eq(best['mode'])&p.fold.eq(fold)]
                np.testing.assert_array_equal(gf.source_row,original.source_row);np.testing.assert_array_equal(gf.score,original.score)
    audit=dict(passed=True,outer_models_reloaded=checked,inner_models_verified=inner,predictions_verified=len(p),labels_unchanged=True,group_separation_verified=True,inner_selection_verified=True,auc_recomputed=True)
    (OUT/'auditoria_independiente.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit,indent=2))
if __name__=='__main__':main()
