"""Busqueda anidada de representaciones y suavizado causal para activacion pupilar."""
import argparse
import json
from datetime import datetime, timezone

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.kernel_approximation import Nystroem
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from threadpoolctl import threadpool_limits

from control_historial import FEATURES, TARGETS, nested_folds
from temporales_core import ROOT, CLASSES, digest, write_json, preprocessor, prepare_frame, metric_record, individual_scores
from baselines_estaticos import validate_partition

OUT = ROOT/'resultados/optimizacion_historial_08-09-2026'
TARGET = 'arousal_label_6s'


def histories(frame, context, scope):
    keys = ['participant', 'recording'] + (['segment_id', 'stimulus'] if scope=='segment' else [])
    times = pd.to_datetime(frame.window_start_utc, utc=True).dt.as_unit('ns').astype('int64').to_numpy()/1e9
    result = []
    for positions in frame.groupby(keys, sort=False).indices.values():
        history = []
        for i in positions:
            if history:
                gap = times[i]-times[history[-1]]
                if gap <= 0:
                    raise ValueError('Cronologia duplicada o desordenada')
                if not np.isclose(gap, 1., atol=.0001, rtol=0):
                    history = []
            history = (history+[int(i)])[-context:]
            result.append((int(i), history.copy()))
    return sorted(result)


def represent(frame, representation):
    if representation=='current':
        return frame[FEATURES].to_numpy(float)
    scope, context = representation.split('_')
    raw = frame[FEATURES].to_numpy(float)
    output = []
    for i, indices in histories(frame, int(context), scope):
        values = raw[indices]
        count = np.isfinite(values).sum(axis=0)
        mean = np.divide(np.nansum(values, axis=0), count, out=np.full(5, np.nan), where=count>0)
        variance = np.divide(np.nansum((values-mean)**2, axis=0), count,
                             out=np.full(5, np.nan), where=count>0)
        output.append(np.r_[raw[i], mean, np.sqrt(variance), raw[i]-values[0], len(indices)/int(context)])
    return np.asarray(output)


def smooth(frame, probabilities, windows):
    if windows==1:
        return probabilities
    return np.asarray([probabilities[ix].mean(axis=0) for _, ix in histories(frame, windows, 'recording')])


def estimator(name, seed, dimensions):
    steps = [('prep', preprocessor())]
    if name=='hgb':
        model = HistGradientBoostingClassifier(max_iter=100, max_leaf_nodes=7, learning_rate=.05,
            min_samples_leaf=50, l2_regularization=10., early_stopping=False,
            class_weight='balanced', random_state=seed)
    else:
        if name=='rbf':
            steps.append(('kernel', Nystroem(kernel='rbf', gamma=1/dimensions, n_components=128, random_state=seed)))
            c = .1
        else:
            c = float(name.split('_')[1])
        model = LogisticRegression(C=c, class_weight='balanced', max_iter=2000, random_state=seed)
    return Pipeline(steps+[('model', model)])


def probabilities(model, x):
    return model.predict_proba(x)[:, [list(model.classes_).index(c) for c in CLASSES]]


def select(scores, scope):
    eligible = scores
    if scope=='current':
        eligible = scores.loc[scores.representation.eq('current') & scores.smoothing.eq(1)]
    elif scope=='temporal':
        eligible = scores.loc[~(scores.representation.eq('current') & scores.smoothing.eq(1))]
    return eligible.sort_values(['score','representation','estimator','smoothing'],
                                ascending=[False,True,True,True]).iloc[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default=str(OUT.relative_to(ROOT)))
    args = parser.parse_args()
    out = ROOT/args.output
    out.mkdir(parents=True, exist_ok=False)
    (out/'modelos').mkdir()
    dataset = ROOT/'resultados/modelado/dataset_modelado.csv'
    partition = ROOT/'resultados/modelado/particion_participantes.csv'
    data = pd.read_csv(dataset)
    data['source_row'] = np.arange(len(data))
    validate_partition(data, pd.read_csv(partition))
    train = prepare_frame(data.loc[data.split.eq('train')], 'arousal_primary_6s', TARGETS, 'train')
    train = train.sort_values(['participant','recording','window_start_utc']).reset_index(drop=True)
    del data
    representations = ['current']+[f'{s}_{c}' for s in ['segment','recording'] for c in [4,8,16]]
    estimators = ['logistic_0.01','logistic_0.1','logistic_1','hgb','rbf']
    folds = nested_folds(train)
    protocol = dict(created_utc=datetime.now(timezone.utc).isoformat(), features=FEATURES, target=TARGET,
        representations=representations, estimators=estimators, smoothing=[1,4,8], seeds=[20260908,20260909],
        folds=folds, inner_folds=3, candidates=105, selection='mean participant BA over three internal grouped folds',
        primary='nested selected all vs fixed logistic C1 on current five features',
        secondary='nested selected temporal vs independently selected current and previous OOF MLP/LSTM/BiLSTM',
        stopping='one frozen grid; evaluate selected pipelines after completing all inner searches; report even if no improvement',
        scope='exploratory repeated research on original train; no fresh independent confirmation',
        features_policy='current, past inclusive mean/std, endpoint minus oldest and normalized available length; no future or targets',
        recording_policy='may cross stimulus/segment boundaries only within same recording and person with consecutive 1s timestamps',
        validation_evaluated=False, test_evaluated=False, dataset_sha256=digest(dataset), partition_sha256=digest(partition),
        sources={n:digest(ROOT/'scripts'/n) for n in ['optimizar_historial.py','control_historial.py','temporales_core.py']})
    write_json(out/'protocolo.json', protocol)
    all_scores, choices, artifacts, predictions, people, metrics = [], [], [], [], [], []
    # Each representation is a deterministic causal function of one participant's predictors.
    matrices = {r:represent(train, r) for r in representations}
    for fold in folds:
        outer_fit = np.flatnonzero(train.participant.isin(fold['fit']))
        fit_frame = train.iloc[outer_fit].reset_index(drop=True)
        splitter = GroupKFold(n_splits=3, shuffle=True, random_state=20260908+fold['fold'])
        for inner, (ii, vv) in enumerate(splitter.split(fit_frame, groups=fit_frame.participant), 1):
            fit_ix, val_ix = outer_fit[ii], outer_fit[vv]
            val = train.iloc[val_ix].reset_index(drop=True)
            for representation in representations:
                for name in estimators:
                    x = matrices[representation]
                    model = estimator(name, 20260908, x.shape[1]).fit(x[fit_ix], train.iloc[fit_ix][TARGET])
                    raw = probabilities(model, x[val_ix])
                    for window in protocol['smoothing']:
                        prob = smooth(val, raw, window)
                        prediction = np.asarray(CLASSES)[prob.argmax(axis=1)]
                        all_scores.append(dict(fold=fold['fold'],inner=inner,representation=representation,
                            estimator=name,smoothing=window,score=metric_record(val,TARGET,prediction,'classification')['macro_score'],
                            evaluation_participants='|'.join(sorted(val.participant.unique())),
                            fit_participants='|'.join(sorted(train.iloc[fit_ix].participant.unique()))))
            pd.DataFrame(all_scores).to_csv(out/'busqueda_interna.csv',index=False)
            print(f'Fold {fold["fold"]}/5, busqueda interna {inner}/3 completada',flush=True)
        scores = pd.DataFrame(all_scores)
        scores = scores.loc[scores.fold.eq(fold['fold'])].groupby(['representation','estimator','smoothing'],as_index=False).score.mean()
        for scope in ['all','temporal','current']:
            best = select(scores, scope)
            choices.append(dict(fold=fold['fold'],scope=scope,representation=best.representation,
                                estimator=best.estimator,smoothing=int(best.smoothing),inner_score=float(best.score)))
        choices.append(dict(fold=fold['fold'],scope='fixed_logistic',representation='current',estimator='logistic_1',smoothing=1,inner_score=None))
        write_json(out/'selecciones.json',choices)
    # All choices are frozen before the first outer evaluation.
    frozen_sha = digest(out/'selecciones.json')
    for choice in choices:
        fold = folds[choice['fold']-1]
        fit_ix = np.flatnonzero(train.participant.isin(fold['fit']))
        val_ix = np.flatnonzero(train.participant.isin(fold['evaluation']))
        frame = train.iloc[val_ix].reset_index(drop=True)
        x = matrices[choice['representation']]
        for seed in protocol['seeds']:
            model = estimator(choice['estimator'],seed,x.shape[1]).fit(x[fit_ix],train.iloc[fit_ix][TARGET])
            name = f'fold{choice["fold"]}__{choice["scope"]}__{seed}'
            path = out/'modelos'/f'{name}.joblib'
            joblib.dump(model,path,compress=3)
            raw = probabilities(model,x[val_ix])
            np.testing.assert_array_equal(raw,probabilities(joblib.load(path),x[val_ix]))
            prob = smooth(frame,raw,choice['smoothing'])
            pred = np.asarray(CLASSES)[prob.argmax(axis=1)]
            meta = dict(**choice,seed=seed,model_id=name,path=path.relative_to(out).as_posix(),sha256=digest(path),
                        train_participants=fold['fit'],evaluation_participants=fold['evaluation'],reload_verified=True)
            artifacts.append(meta)
            p = frame[['source_row','participant','window_start_utc',TARGET]].copy()
            p['model_id'],p['scope'],p['seed'],p['fold'],p['prediction'] = name,choice['scope'],seed,choice['fold'],pred
            for i,c in enumerate(CLASSES):
                p['prob_'+c] = prob[:,i]
            predictions.append(p)
            metrics.append(dict(model_id=name,scope=choice['scope'],seed=seed,fold=choice['fold'],
                                **metric_record(frame,TARGET,pred,'classification')))
            people.extend(dict(model_id=name,scope=choice['scope'],seed=seed,fold=choice['fold'],participant=p,score=s)
                          for p,s in individual_scores(frame,TARGET,pred,'classification').items())
        print(f'Evaluado fold {choice["fold"]}, {choice["scope"]}: {choice["representation"]} {choice["estimator"]} smooth={choice["smoothing"]}',flush=True)
    assert digest(out/'selecciones.json') == frozen_sha
    pd.concat(predictions).to_csv(out/'predicciones_oof.csv.gz',index=False,compression='gzip')
    pd.DataFrame(metrics).to_csv(out/'metricas_folds.csv',index=False)
    pd.DataFrame(people).to_csv(out/'metricas_participantes.csv',index=False)
    write_json(out/'catalogo_modelos.json',artifacts)
    write_json(out/'completo.json',dict(models=len(artifacts),inner_fits=525,selection_sha256=frozen_sha,
        protocol_sha256=digest(out/'protocolo.json'),catalog_sha256=digest(out/'catalogo_modelos.json'),
        predictions_sha256=digest(out/'predicciones_oof.csv.gz'),validation_evaluated=False,test_evaluated=False))
    print(pd.DataFrame(people).groupby('scope').score.mean().to_string(),flush=True)


if __name__=='__main__':
    with threadpool_limits(limits=4):
        main()
