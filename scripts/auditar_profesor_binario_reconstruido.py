"""Auditoria independiente de etiquetas nuevas, profesores por fold y AUC."""
import json, hashlib
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
from sklearn.metrics import roc_auc_score
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'resultados/profesor_binario_reconstruido_29-10-2026'

def main():
    plan=json.loads((OUT/'protocolo.json').read_text()); source=ROOT/'resultados/preprocesamiento/caracteristicas_multimodales.csv'
    assert hashlib.sha256(source.read_bytes()).hexdigest()==plan['source_sha256']
    raw=pd.read_csv(source); raw['source_row']=np.arange(len(raw))
    mapping=pd.read_csv(ROOT/'resultados/modelado/particion_participantes.csv').set_index('participant').split
    f=raw[raw.participant.map(mapping).eq('train')].copy()
    cols=plan['teacher_columns']; z=pd.DataFrame(index=f.index)
    for c,direction in zip(cols,plan['directions']):
        v=f[c].astype(float)
        if c!='pupil_mean_z': v=np.log1p(v.clip(lower=0))
        mean=v.groupby(f.participant).transform('mean'); std=v.groupby(f.participant).transform(lambda x:x.std(ddof=0))
        z[c]=(v-mean)/std.replace(0,np.nan)*direction
    outputs=[]
    for kind in plan['teachers']:
        out=OUT/kind; p=pd.read_csv(out/'predicciones_oof.csv.gz'); labels=pd.read_csv(out/'etiquetas_profesor_oof.csv.gz')
        assert not labels.source_row.duplicated().any()
        for fold in plan['folds']:
            teacher=joblib.load(out/'profesores'/f"profesor_fold{fold['fold']}.joblib")
            assert set(fold['fit']).isdisjoint(fold['evaluation'])
            if kind=='igualitario': score=z.mul([.125,.125,.125,.125,.5],axis=1).sum(axis=1,min_count=5)
            else:
                assert set(teacher['fit_participants'])==set(fold['fit'])
                fit=f.participant.isin(fold['fit'])&z.notna().all(axis=1)
                np.testing.assert_allclose(teacher['pca'].mean_,z.loc[fit].mean().to_numpy(),atol=1e-12)
                score=pd.Series(np.nan,index=f.index); valid=z.notna().all(axis=1)
                score.loc[valid]=(z.loc[valid].to_numpy()-teacher['pca'].mean_)@teacher['pca'].components_[0]*teacher['sign']
            expected=score.gt(score.groupby(f.participant).transform('median')).astype(int)
            observed=labels[labels.fold.eq(fold['fold'])]
            assert set(observed.participant)==set(fold['evaluation'])
            np.testing.assert_array_equal(observed.y,expected.loc[observed.source_row])
            np.testing.assert_allclose(observed.teacher_score,score.loc[observed.source_row],rtol=1e-10,atol=1e-10)
            pp=p[p.fold.eq(fold['fold'])]
            assert set(pp.participant)==set(fold['evaluation'])
            np.testing.assert_array_equal(pp.y,expected.loc[pp.source_row])
        for a in (out/'predicciones').glob('*.json'):
            metadata=json.loads(a.read_text()); name=a.stem
            for filename,key in [(out/'modelos'/f'{name}.joblib','model_sha256'),(out/'predicciones'/f'{name}.csv.gz','predictions_sha256')]:
                assert hashlib.sha256(filename.read_bytes()).hexdigest()==metadata[key]
        avg=p.groupby(['family','mode','source_row','participant','y'],as_index=False).prob.mean()
        metrics=pd.read_csv(out/'metricas.csv')
        for _,r in metrics.iterrows():
            g=avg[avg.family.eq(r.family)&avg['mode'].eq(r['mode'])]
            value=np.mean([roc_auc_score(t.y,t.prob) for _,t in g.groupby('participant') if t.y.nunique()==2])
            np.testing.assert_allclose(value,r.auc_macro,atol=1e-12)
        outputs.append({'profesor':kind,'predictions_verified':len(p),'labels_verified':len(labels),'auc_verified':True,'hashes_verified':True,'train_only':True})
    (OUT/'auditoria_independiente.json').write_text(json.dumps({'passed':True,'teachers':outputs},indent=2))
    print(json.dumps(outputs,indent=2))

if __name__=='__main__':main()
