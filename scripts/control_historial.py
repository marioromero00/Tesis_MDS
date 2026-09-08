"""Contraste pupilar anidado, exclusivamente en participantes del train original."""
from __future__ import annotations

import argparse
import json
import platform
import time
from datetime import datetime, timezone

import joblib
import numpy as np
import pandas as pd
import sklearn
import torch
from sklearn.model_selection import GroupKFold, GroupShuffleSplit
from torch import nn

from baselines_estaticos import validate_partition, classification_models, regression_models
from entrenar_temporales import fit_network
from temporales_core import (ROOT, CLASSES, digest, write_json, seed_all, preprocessor,
    prepare_frame, history_indices, sequence_array, TemporalNet, raw_predict, decode,
    metric_record, individual_scores, load_net)

OUT = ROOT / 'resultados/control_historial_08-09-2026'
FEATURES = ['pupil_mean_z', 'pupil_std_z', 'pupil_min_z', 'pupil_max_z', 'pupil_slope_z_s']
TARGETS = {'arousal_primary_6s': ['arousal_score_6s', 'arousal_label_6s']}
VARIANTS = [(a, mode) for a in ['TCN', 'LSTM', 'BiLSTM']
            for mode in ['history', 'repeat_current']] + [('MLP_current', 'current')]


def current_control(x, lengths, mode):
    """Repite endpoint en posiciones reales; conserva padding, longitud y arquitectura."""
    if mode not in ['history', 'repeat_current', 'current']:
        raise ValueError(mode)
    if mode != 'repeat_current':
        return x
    result = np.zeros_like(x)
    endpoint = x[np.arange(len(x)), lengths - 1]
    mask = np.arange(x.shape[1])[None, :] < lengths[:, None]
    result[mask] = np.broadcast_to(endpoint[:, None, :], x.shape)[mask]
    return result


def nested_folds(frame, seed=20260907):
    if set(frame.split) != {'train'}:
        raise ValueError('Solo se permite train original')
    outer = GroupKFold(n_splits=5, shuffle=True, random_state=seed)
    result = []
    for fold, (fit, evaluation) in enumerate(outer.split(frame, groups=frame.participant), 1):
        candidate = frame.iloc[fit]
        inner = GroupShuffleSplit(n_splits=1, test_size=.2, random_state=seed + fold)
        ii, vv = next(inner.split(candidate, groups=candidate.participant))
        groups = dict(fit=sorted(candidate.participant.unique()),
                      evaluation=sorted(frame.iloc[evaluation].participant.unique()),
                      inner_fit=sorted(candidate.iloc[ii].participant.unique()),
                      inner_validation=sorted(candidate.iloc[vv].participant.unique()))
        assert set(groups['inner_fit']).isdisjoint(groups['inner_validation'])
        assert set(groups['fit']).isdisjoint(groups['evaluation'])
        assert set(groups['inner_fit']) | set(groups['inner_validation']) == set(groups['fit'])
        result.append(dict(fold=fold, **groups))
    return result


def fixed_fit(x, lengths, y, kind, architecture, seed, epochs, config):
    """Reajuste desde cero: no recibe resultados del fold externo ni early stopping."""
    seed_all(seed)
    model = TemporalNet(architecture, x.shape[2], 3 if kind == 'classification' else 1,
                        config['hidden'], config['dropout'])
    if kind == 'classification':
        counts = np.bincount(y, minlength=3)
        if (counts == 0).any():
            raise ValueError('Clase ausente en ajuste')
        criterion = nn.CrossEntropyLoss(weight=torch.tensor(len(y)/(3*counts), dtype=torch.float32))
    else:
        criterion = nn.MSELoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=config['learning_rate'],
                                 weight_decay=config['weight_decay'])
    xx, ll = torch.from_numpy(x), torch.from_numpy(lengths)
    yy = torch.tensor(y, dtype=torch.long if kind == 'classification' else torch.float32)
    history = []
    for epoch in range(1, epochs + 1):
        model.train()
        order, total = torch.randperm(len(xx)), 0.
        for start in range(0, len(xx), config['batch_size']):
            ix = order[start:start+config['batch_size']]
            optimizer.zero_grad(set_to_none=True)
            raw = model(xx[ix], ll[ix])
            loss = criterion(raw if kind == 'classification' else raw[:, 0], yy[ix])
            if not torch.isfinite(loss):
                raise ValueError('Loss no finita')
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.)
            optimizer.step()
            total += float(loss.detach()) * len(ix)
        history.append(dict(epoch=epoch, train_loss=total/len(xx)))
    return model, history


def encode(frame, target, kind):
    return (frame[target].map({c: i for i, c in enumerate(CLASSES)}).to_numpy()
            if kind == 'classification' else frame[target].to_numpy(np.float32))


def prediction_table(frame, target, kind, prediction, raw, metadata, lengths):
    result = frame[['source_row', 'participant', 'recording', 'segment_id', 'stimulus',
                    'window_start_utc']].copy()
    for key in ['model_id', 'fold', 'kind', 'architecture', 'mode', 'seed']:
        result[key] = metadata[key]
    result['split'] = 'train_oof'
    result['history_length'] = lengths
    result['true'] = frame[target].to_numpy()
    result['prediction'] = prediction
    if kind == 'classification':
        for i, name in enumerate(CLASSES):
            result['prob_' + name] = raw[:, i]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default=str(OUT.relative_to(ROOT)))
    args = parser.parse_args()
    output = ROOT / args.output
    dataset = ROOT / 'resultados/modelado/dataset_modelado.csv'
    partition = ROOT / 'resultados/modelado/particion_participantes.csv'
    frozen = ROOT / 'resultados/estabilidad_variables_07-09-2026/conjuntos_congelados.json'
    manifest = json.loads((ROOT/'resultados/modelado/ejecuciones/baselines_05-09-2026_02/manifiesto_baselines.json').read_text(encoding='utf-8'))
    assert digest(dataset) == manifest['dataset_sha256']
    assert digest(partition) == manifest['partition_sha256']
    assert FEATURES == json.loads(frozen.read_text(encoding='utf-8'))['features']['arousal_primary_6s']['Pupil_no_quality']
    data = pd.read_csv(dataset)
    data['source_row'] = np.arange(len(data))
    validate_partition(data, pd.read_csv(partition))
    # Nunca preparar, transformar, predecir ni puntuar validation/test originales.
    train = prepare_frame(data.loc[data.split.eq('train')].copy(), 'arousal_primary_6s', TARGETS, 'train')
    del data
    folds = nested_folds(train)
    config = dict(context_windows=8, hidden=24, dropout=.2, seeds=[20260907, 20260908],
        epochs=30, min_epochs=8, patience=6, min_delta=.0001, batch_size=256,
        learning_rate=.001, weight_decay=.0001, gradient_clip=1., device='cpu', threads=4,
        features=FEATURES, targets=TARGETS, variants=VARIANTS, classes=CLASSES,
        folds=folds, train_rows=len(train), train_participants=sorted(train.participant.unique()),
        primary='classification: paired participant macro BA, history minus trained repeat_current',
        secondary='history minus matched five-feature MLP, logistic/Ridge, RF and Dummy; regression negative MSE',
        epoch_rule='select on inner 16/4 participant split; restart same seed and refit outer 20 for that epoch count',
        preprocessing='fit imputer and scaler separately on inner16 and outer20; inherited offline per-person feature normalization',
        scope='exploratory follow-up motivated by previously observed validation/test; no fresh confirmatory holdout',
        control='repeat current trained from scratch; retains lengths and capacity, replaces every real history vector by endpoint',
        uncertainty='2000 paired participant bootstrap resamples after seed averaging; descriptive, overlapping fold fits, no multiplicity correction',
        validation_evaluated=False, test_evaluated=False, dataset_sha256=digest(dataset),
        partition_sha256=digest(partition), panel_sha256=digest(frozen),
        source_hashes={n: digest(ROOT/'scripts'/n) for n in ['control_historial.py', 'temporales_core.py',
            'entrenar_temporales.py', 'baselines_estaticos.py']},
        versions={'python':platform.python_version(), 'torch':str(torch.__version__),
                  'numpy':np.__version__, 'pandas':pd.__version__, 'sklearn':sklearn.__version__},
        created_utc=datetime.now(timezone.utc).isoformat())
    output.mkdir(parents=True, exist_ok=False)
    for name in ['modelos', 'predicciones', 'historiales']:
        (output/name).mkdir()
    write_json(output/'protocolo.json', config)
    artifacts, preps, metrics, people = [], [], [], []
    for fold in folds:
        frames = {stage:train.loc[train.participant.isin(fold[stage])].reset_index(drop=True)
                  for stage in ['fit', 'evaluation', 'inner_fit', 'inner_validation']}
        indices = {stage:history_indices(f, 8) for stage, f in frames.items()}
        fitted_preps = {}
        for stage in ['fit', 'inner_fit']:
            prep = preprocessor().fit(frames[stage][FEATURES])
            path = output/'modelos'/f'fold{fold["fold"]}__{stage}__preprocessor.joblib'
            joblib.dump(prep, path, compress=3)
            np.testing.assert_array_equal(prep.transform(frames[stage][FEATURES]),
                                          joblib.load(path).transform(frames[stage][FEATURES]))
            preps.append(dict(fold=fold['fold'], stage=stage, path=path.relative_to(output).as_posix(),
                sha256=digest(path), participants=fold[stage], features=FEATURES,
                transformed_features=prep.get_feature_names_out().tolist(), reload_verified=True))
            fitted_preps[stage] = prep
        xs = {stage:sequence_array(fitted_preps['inner_fit' if stage.startswith('inner_') else 'fit'].transform(f[FEATURES]),
                                  indices[stage][0]) for stage, f in frames.items()}
        for kind, target in [('classification', TARGETS['arousal_primary_6s'][1]),
                             ('regression', TARGETS['arousal_primary_6s'][0])]:
            for architecture, mode in VARIANTS:
                transformed = {stage:current_control(x, indices[stage][1], mode) for stage, x in xs.items()}
                for seed in config['seeds']:
                    model_id = f'fold{fold["fold"]}__{kind}__{architecture}__{mode}__{seed}'
                    print(f'{len(artifacts)+1}/170 {model_id}', flush=True)
                    start = time.monotonic()
                    _, inner_history, epoch = fit_network(transformed['inner_fit'], indices['inner_fit'][1],
                        encode(frames['inner_fit'], target, kind), transformed['inner_validation'],
                        indices['inner_validation'][1], frames['inner_validation'], target, kind, architecture, seed, config)
                    model, outer_history = fixed_fit(transformed['fit'], indices['fit'][1],
                        encode(frames['fit'], target, kind), kind, architecture, seed, epoch, config)
                    path = output/'modelos'/f'{model_id}.pt'
                    torch.save(model.state_dict(), path)
                    metadata = dict(model_id=model_id, fold=fold['fold'], kind=kind,
                        architecture=architecture, mode=mode, seed=seed, path=path.relative_to(output).as_posix(),
                        sha256=digest(path), inputs=xs['fit'].shape[2], outputs=3 if kind=='classification' else 1,
                        hidden=config['hidden'], dropout=config['dropout'], features=FEATURES, target=target,
                        train_participants=fold['fit'], evaluation_participants=fold['evaluation'],
                        preprocessor=f'modelos/fold{fold["fold"]}__fit__preprocessor.joblib',
                        best_epoch=epoch, inner_epochs_run=len(inner_history),
                        parameters=sum(p.numel() for p in model.parameters()), seconds=time.monotonic()-start)
                    metadata['preprocessor_sha256'] = digest(output/metadata['preprocessor'])
                    raw = raw_predict(model, transformed['evaluation'], indices['evaluation'][1])
                    np.testing.assert_array_equal(raw, raw_predict(load_net(metadata, output),
                        transformed['evaluation'], indices['evaluation'][1]))
                    metadata['reload_verified'] = True
                    write_json(path.with_suffix('.json'), metadata)
                    pd.DataFrame([dict(stage='inner', **r) for r in inner_history] +
                                 [dict(stage='outer_refit', **r) for r in outer_history]).to_csv(
                                     output/'historiales'/f'{model_id}.csv', index=False)
                    predicted = decode(raw, kind)
                    probabilities = torch.softmax(torch.from_numpy(raw), dim=1).numpy() if kind=='classification' else raw
                    record(output, artifacts, metrics, people, frames['evaluation'], target, kind,
                           predicted, probabilities, metadata, indices['evaluation'][1])
                    print(f'  epoca={epoch}, OOF={metrics[-1]["macro_score"]:.5f}, {metadata["seconds"]:.1f}s', flush=True)
            models = classification_models(config['seeds'][0], 200) if kind=='classification' else regression_models(config['seeds'][0], 200)
            for name, model in models.items():
                model.fit(frames['fit'][FEATURES], frames['fit'][target])
                model_id = f'fold{fold["fold"]}__{kind}__{name}__current__{config["seeds"][0]}'
                path = output/'modelos'/f'{model_id}.joblib'
                joblib.dump(model, path, compress=3)
                prediction = model.predict(frames['evaluation'][FEATURES])
                restored = joblib.load(path)
                np.testing.assert_array_equal(prediction, restored.predict(frames['evaluation'][FEATURES]))
                metadata = dict(model_id=model_id, fold=fold['fold'], kind=kind, architecture=name,
                    mode='current', seed=config['seeds'][0], path=path.relative_to(output).as_posix(),
                    sha256=digest(path), features=FEATURES, target=target, train_participants=fold['fit'],
                    evaluation_participants=fold['evaluation'], reload_verified=True)
                raw = np.zeros((len(prediction), 1))
                if kind=='classification':
                    np.testing.assert_array_equal(model.predict_proba(frames['evaluation'][FEATURES]),
                                                  restored.predict_proba(frames['evaluation'][FEATURES]))
                    raw = model.predict_proba(frames['evaluation'][FEATURES])[:, [list(model.classes_).index(c) for c in CLASSES]]
                write_json(path.with_suffix('.json'), metadata)
                record(output, artifacts, metrics, people, frames['evaluation'], target, kind,
                       prediction, raw, metadata, indices['evaluation'][1])
        write_json(output/'preprocesadores.json', preps)
    write_json(output/'entrenamiento_completo.json', dict(models=len(artifacts),
        protocol_sha256=digest(output/'protocolo.json'), catalog_sha256=digest(output/'catalogo_modelos.json'),
        validation_evaluated=False, test_evaluated=False, completed_utc=datetime.now(timezone.utc).isoformat()))
    print('ENTRENAMIENTO COMPLETO', flush=True)


def record(output, artifacts, metrics, people, frame, target, kind, prediction, raw, metadata, lengths):
    predictions = prediction_table(frame, target, kind, prediction, raw, metadata, lengths)
    path = output/'predicciones'/f'{metadata["model_id"]}.csv.gz'
    predictions.to_csv(path, index=False, compression='gzip')
    metadata.update(predictions=path.relative_to(output).as_posix(), predictions_sha256=digest(path))
    artifacts.append(metadata)
    identity = {k:metadata[k] for k in ['model_id', 'fold', 'kind', 'architecture', 'mode', 'seed']}
    metrics.append(dict(**identity, **metric_record(frame, target, prediction, kind)))
    people.extend(dict(**identity, participant=p, score=s) for p, s in individual_scores(frame, target, prediction, kind).items())
    write_json(output/'catalogo_modelos.json', artifacts)
    pd.DataFrame(metrics).to_csv(output/'metricas_folds.csv', index=False)
    pd.DataFrame(people).to_csv(output/'metricas_participantes.csv', index=False)


if __name__ == '__main__':
    main()
