"""Importancia exploratoria y reduccion de entradas, sin evaluar el split test.

Ejecutar desde el repositorio: python scripts/analisis_variables.py
Las perturbaciones son desplazamientos circulares dentro de participante/segmento.
Los top-k se eligen exclusivamente con importancia RF ajustada en train.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import balanced_accuracy_score, r2_score, mean_absolute_error

from baselines_estaticos import ROOT, EEG, GSR, EYE, PUPIL, validate_partition

SOURCE = ROOT / 'resultados/modelado/ejecuciones/baselines_05-09-2026_02'
TASKS = {
    'attention_primary': ('attention_score_equal', 'attention_label_equal', {'EEG': EEG, 'GSR': GSR}),
    'arousal_primary_6s': ('arousal_score_6s', 'arousal_label_6s', {'EEG': EEG, 'Eye': EYE, 'Pupil': PUPIL}),
}


def shift_indices(frame, seed):
    """Mantiene segmento, marginales y orden circular; misma permutacion para un grupo.

    Desplazamiento entre 25 y 75% del segmento para evitar vecinos solapados.
    Segmentos de una ventana quedan intactos; se informa la fraccion modificada.
    """
    rng = np.random.default_rng(seed)
    result = np.arange(len(frame))
    for positions in frame.groupby(['participant', 'recording', 'segment_id'], sort=True).indices.values():
        n = len(positions)
        if n > 1:
            lower = max(1, int(np.ceil(n * .25)))
            upper = min(n - 1, int(np.floor(n * .75)))
            result[positions] = np.roll(positions, int(rng.integers(lower, upper + 1)))
    return result


def score(y, pred, kind):
    if kind == 'regression':
        return -float(np.mean((np.asarray(y, float) - pred) ** 2))
    y = np.asarray(y)
    return float(np.mean([np.mean(pred[y == c] == c) for c in np.unique(y)]))


def subject_scores(frame, pred, target, kind):
    return np.array([score(frame.iloc[ix][target].to_numpy(), pred[ix], kind)
                     for ix in frame.groupby('participant', sort=True).indices.values()])


def bootstrap_mean(values, seed=20260907):
    values = np.asarray(values)
    draws = np.random.default_rng(seed).choice(values, (2000, len(values)), replace=True).mean(axis=1)
    return np.quantile(draws, [.025, .975]).tolist()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='resultados/analisis_variables_07-09-2026')
    parser.add_argument('--repeats', type=int, default=10)
    args = parser.parse_args()
    if args.repeats < 2:
        raise ValueError('Se necesitan al menos dos repeticiones')
    output = ROOT / args.output
    output.mkdir(parents=True, exist_ok=False)
    (output / 'modelos_reducidos').mkdir()
    dataset = ROOT / 'resultados/modelado/dataset_modelado.csv'
    partition = ROOT / 'resultados/modelado/particion_participantes.csv'
    data = pd.read_csv(dataset)
    validate_partition(data, pd.read_csv(partition))
    # Eliminar test/sensibilidad/excluidos antes de cualquier analisis o ajuste.
    data = data.loc[data.split.isin(['train', 'validation'])].copy()
    manifest = json.loads((SOURCE / 'manifiesto_baselines.json').read_text(encoding='utf-8'))
    assert hashlib.sha256(dataset.read_bytes()).hexdigest() == manifest['dataset_sha256']
    assert hashlib.sha256(partition.read_bytes()).hexdigest() == manifest['partition_sha256']
    importance, per_subject, metrics, correlations, quality, subsets, artifacts = [], [], [], [], [], [], []
    for task, (continuous, label, modalities) in TASKS.items():
        features = sum(modalities.values(), [])
        train = data.loc[data.split.eq('train') & data[continuous].notna() & data[label].notna()].copy()
        valid = data.loc[data.split.eq('validation') & data[continuous].notna() & data[label].notna()].sort_values(
            ['participant', 'recording', 'segment_id', 'window_start_utc']).reset_index(drop=True)
        assert set(train.participant).isdisjoint(valid.participant)
        rho = train[features].corr(method='spearman')
        for i, f in enumerate(features):
            quality.append(dict(task=task, feature=f, train_missing=float(train[f].isna().mean()),
                                validation_missing=float(valid[f].isna().mean()), train_unique=int(train[f].nunique())))
            for g in features[i + 1:]:
                correlations.append(dict(task=task, feature_a=f, feature_b=g, spearman=float(rho.loc[f, g])))
        permutations = [shift_indices(valid, 20260907 + i) for i in range(args.repeats)]
        for kind, target, names in [('classification', label, ['logistic', 'random_forest']),
                                    ('regression', continuous, ['ridge', 'random_forest'])]:
            forest_meta = json.loads((SOURCE / 'modelos' / task / f'{kind}__random_forest.json').read_text())
            forest_path = SOURCE / forest_meta['path']
            assert hashlib.sha256(forest_path.read_bytes()).hexdigest() == forest_meta['sha256']
            forest = joblib.load(forest_path)
            # Indicadores de ausencia se atribuyen a su entrada original.
            weights = dict.fromkeys(features, 0.0)
            for name, value in zip(forest[:-1].get_feature_names_out(), forest[-1].feature_importances_):
                weights[name.removeprefix('missingindicator_')] += float(value)
            ranking = sorted(features, key=lambda f: (-weights[f], f))
            candidates = {**modalities, 'top5_train': ranking[:5], 'top10_train': ranking[:10]}
            if len(modalities) == 3:
                candidates.update({'EEG_Eye': EEG + EYE, 'EEG_Pupil': EEG + PUPIL, 'Eye_Pupil': EYE + PUPIL})
            for subset, columns in candidates.items():
                subsets.append(dict(task=task, kind=kind, subset=subset, features=columns,
                                    selection='RF impurity train only' if subset.startswith('top') else 'modalidad predefinida'))
            for name in names:
                print(f'{task} {kind} {name}: importancia', flush=True)
                meta = json.loads((SOURCE / 'modelos' / task / f'{kind}__{name}.json').read_text())
                model_path = SOURCE / meta['path']
                assert hashlib.sha256(model_path.read_bytes()).hexdigest() == meta['sha256']
                assert meta['features'] == features
                model = joblib.load(model_path)
                x = valid[features]
                baseline = model.predict(x)
                original_scores = subject_scores(valid, baseline, target, kind)
                groups = {f: [f] for f in features} | {f'modalidad:{m}': fs for m, fs in modalities.items()}
                for group, columns in groups.items():
                    drops, pooled_drops = [], []
                    for indices in permutations:
                        altered = x.copy()
                        altered.loc[:, columns] = x.iloc[indices][columns].to_numpy()
                        prediction = model.predict(altered)
                        drops.append(original_scores - subject_scores(valid, prediction, target, kind))
                        pooled_drops.append(score(valid[target], baseline, kind) - score(valid[target], prediction, kind))
                    drops = np.array(drops)
                    means = drops.mean(axis=0)
                    low, high = bootstrap_mean(means)
                    importance.append(dict(task=task, kind=kind, model=name, feature=group,
                        importance=float(means.mean()), bootstrap_low=low, bootstrap_high=high,
                        repeat_sd=float(drops.mean(axis=1).std(ddof=1)), positive_participants=int((means > 0).sum()),
                        participants=len(means), pooled_importance=float(np.mean(pooled_drops)),
                        shifted_fraction=float(np.mean(permutations[0] != np.arange(len(valid)))),
                        metric='delta_balanced_accuracy' if kind == 'classification' else 'increase_mse'))
                    for person, value in zip(sorted(valid.participant.unique()), means):
                        per_subject.append(dict(task=task, kind=kind, model=name, feature=group,
                                                participant=person, importance=float(value)))
                for subset, columns in {'full': features, **candidates}.items():
                    print(f'  ajuste {subset} ({len(columns)})', flush=True)
                    if subset == 'full':
                        predicted = baseline
                    else:
                        reduced = clone(model).fit(train[columns], train[target])
                        predicted = reduced.predict(valid[columns])
                        path = output / 'modelos_reducidos' / f'{task}__{kind}__{name}__{subset}.joblib'
                        joblib.dump(reduced, path, compress=3)
                        np.testing.assert_array_equal(predicted, joblib.load(path).predict(valid[columns]))
                        artifacts.append(dict(path=path.relative_to(output).as_posix(), features=columns,
                            target=target, task=task, kind=kind, model=name, subset=subset,
                            sha256=hashlib.sha256(path.read_bytes()).hexdigest(), reload_verified=True))
                    ss = subject_scores(valid, predicted, target, kind)
                    low, high = bootstrap_mean(ss - original_scores)
                    row = dict(task=task, kind=kind, model=name, subset=subset, n_features=len(columns),
                        rows=len(valid), participants=valid.participant.nunique(), macro_score=float(ss.mean()),
                        delta_vs_full=float((ss - original_scores).mean()), delta_low=low, delta_high=high)
                    if kind == 'classification':
                        row['balanced_accuracy'] = balanced_accuracy_score(valid[target], predicted)
                    else:
                        row.update(r2=r2_score(valid[target], predicted), mae=mean_absolute_error(valid[target], predicted),
                                   mse=-score(valid[target], predicted, kind))
                    metrics.append(row)
                # Guardado incremental para inspeccion sin esperar toda la ejecucion.
                pd.DataFrame(importance).to_csv(output / 'importancia_validacion.csv', index=False)
                pd.DataFrame(metrics).to_csv(output / 'comparacion_subconjuntos.csv', index=False)
    pd.DataFrame(per_subject).to_csv(output / 'importancia_por_participante.csv', index=False)
    pd.DataFrame(correlations).to_csv(output / 'correlaciones_train.csv', index=False)
    pd.DataFrame(quality).to_csv(output / 'calidad_variables.csv', index=False)
    (output / 'subconjuntos.json').write_text(json.dumps(subsets, indent=2), encoding='utf-8')
    final = dict(seed=20260907, repeats=args.repeats, test_evaluated=False,
        dataset_sha256=manifest['dataset_sha256'], partition_sha256=manifest['partition_sha256'],
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), versions=manifest['versions'],
        source=str(SOURCE.relative_to(ROOT)), artifacts=artifacts,
        train_participants=sorted(data.loc[data.split.eq('train'), 'participant'].unique()),
        validation_participants=sorted(data.loc[data.split.eq('validation'), 'participant'].unique()),
        importance_method='circular shift 25-75% within participant/recording/segment; 10 repeats default',
        uncertainty='percentile bootstrap 2000 resamples of participant means; exploratory, not simultaneous',
        scope='primary labels only; offline normalized features inherited; validation used for exploration')
    (output / 'manifiesto.json').write_text(json.dumps(final, indent=2), encoding='utf-8')
    print(f'Completado: {output}', flush=True)


if __name__ == '__main__':
    main()
