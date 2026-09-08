"""Entrena TCN, LSTM, BiLSTM y control MLP; selecciona usando solo validation."""
from __future__ import annotations
import argparse
import copy
import json
import platform
import time
from datetime import datetime, timezone

import joblib
import numpy as np
import pandas as pd
import sklearn
import torch
from torch import nn

from temporales_core import (ROOT, OUT, STATIC, CLASSES, write_json, digest, seed_all, preprocessor,
    prepare_frame, history_indices, sequence_array, TemporalNet, raw_predict, decode, metric_record, load_net)
from baselines_estaticos import validate_partition, EEG, GSR, EYE, PUPIL


def fit_network(x, lengths, y, validation_x, validation_lengths, frame, target, kind, architecture, seed, config):
    seed_all(seed)
    model = TemporalNet(architecture, x.shape[2], 3 if kind == 'classification' else 1,
                        config['hidden'], config['dropout'])
    if kind == 'classification':
        counts = np.bincount(y, minlength=3)
        if (counts == 0).any():
            raise ValueError('Falta clase en train')
        criterion = nn.CrossEntropyLoss(weight=torch.tensor(len(y)/(3*counts), dtype=torch.float32))
    else:
        criterion = nn.MSELoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=config['learning_rate'], weight_decay=config['weight_decay'])
    xx, ll = torch.from_numpy(x), torch.from_numpy(lengths)
    yy = torch.tensor(y, dtype=torch.long if kind == 'classification' else torch.float32)
    best, best_state, best_epoch, stale, history = -np.inf, None, 0, 0, []
    for epoch in range(1, config['epochs'] + 1):
        model.train()
        order = torch.randperm(len(xx))
        losses = []
        for start in range(0, len(xx), config['batch_size']):
            ix = order[start:start+config['batch_size']]
            optimizer.zero_grad(set_to_none=True)
            result = model(xx[ix], ll[ix])
            loss = criterion(result if kind == 'classification' else result[:, 0], yy[ix])
            if not torch.isfinite(loss):
                raise ValueError('Loss no finita')
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.)
            optimizer.step()
            losses.append((float(loss.detach()), len(ix)))
        predicted = decode(raw_predict(model, validation_x, validation_lengths), kind)
        score = metric_record(frame, target, predicted, kind)['macro_score']
        history.append(dict(epoch=epoch, train_loss=sum(v*n for v,n in losses)/len(xx), validation_macro_score=score))
        if score > best + config['min_delta']:
            best, best_state, best_epoch, stale = score, copy.deepcopy(model.state_dict()), epoch, 0
        else:
            stale += 1
        if epoch >= config['min_epochs'] and stale >= config['patience']:
            break
    model.load_state_dict(best_state)
    return model, history, best_epoch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default=str(OUT.relative_to(ROOT)))
    args = parser.parse_args()
    output = ROOT / args.output
    output.mkdir(parents=True, exist_ok=False)
    (output/'modelos').mkdir()
    frozen_path = STATIC/'conjuntos_congelados.json'
    panel = json.loads(frozen_path.read_text(encoding='utf-8'))
    baseline_manifest_path = ROOT/'resultados/modelado/ejecuciones/baselines_05-09-2026_02/manifiesto_baselines.json'
    baseline_manifest = json.loads(baseline_manifest_path.read_text(encoding='utf-8'))
    dataset = ROOT/'resultados/modelado/dataset_modelado.csv'
    partition = ROOT/'resultados/modelado/particion_participantes.csv'
    assert digest(dataset) == baseline_manifest['dataset_sha256']
    assert digest(partition) == baseline_manifest['partition_sha256']
    data = pd.read_csv(dataset)
    data['source_row'] = np.arange(len(data))
    validate_partition(data, pd.read_csv(partition))
    data = data.loc[data.split.isin(['train', 'validation'])].copy()
    config = dict(context_windows=8, maximum_support_seconds=9, hidden=24, dropout=.2,
        seeds=[20260907, 20260908], architectures=['TCN', 'LSTM', 'BiLSTM'],
        epochs=30, min_epochs=8, patience=6, min_delta=.0001, batch_size=256,
        learning_rate=.001, weight_decay=.0001, gradient_clip=1., device='cpu', threads=4,
        features=panel['features'], targets=panel['targets'], classes=CLASSES,
        preprocessing='median train imputation with missing indicators and train StandardScaler',
        sequence_policy='past and present, up to 8 windows; right zero padding; reset at participant/recording/segment/stimulus/gap !=1s',
        control='MLP_current on full sets; same training protocol, reads only endpoint',
        selection='checkpoint by validation macro BA / negative MSE; configuration by mean over two seeds; never test',
        scope='primary pseudo-labels, inherited offline participant normalization; no raw signal training',
        dataset_sha256=digest(dataset), partition_sha256=digest(partition), panel_sha256=digest(frozen_path),
        source_hashes={n:digest(ROOT/'scripts'/n) for n in ['temporales_core.py','entrenar_temporales.py']},
        created_utc=datetime.now(timezone.utc).isoformat(),
        versions={'python':platform.python_version(),'torch':str(torch.__version__), 'numpy':np.__version__,
                  'pandas':pd.__version__,'sklearn':sklearn.__version__,'joblib':joblib.__version__})
    write_json(output/'protocolo.json', config)
    artifacts, histories, metrics, coverage, prep_catalog = [], [], [], [], []
    for task, sets in panel['features'].items():
        frames = {split:prepare_frame(data, task, panel['targets'], split) for split in ['train','validation']}
        assert set(frames['train'].participant).isdisjoint(frames['validation'].participant)
        identities = {s:history_indices(f, 8) for s,f in frames.items()}
        for split, (idx, lengths) in identities.items():
            coverage.append(dict(task=task, split=split, rows=len(lengths), mean_history=float(lengths.mean()),
                singleton_fraction=float(np.mean(lengths==1)), full_history_fraction=float(np.mean(lengths==8))))
            frame = frames[split]
            audit = frame[['source_row','participant','recording','segment_id','stimulus','window_start_utc']].copy()
            audit['history_length'] = lengths
            audit['history_start_utc'] = frame.iloc[idx[:,0]].window_start_utc.to_numpy()
            audit.to_csv(output/f'secuencias_{task}_{split}.csv.gz', index=False, compression='gzip')
        for subset, columns in sets.items():
            forbidden = EYE+PUPIL if task == 'attention_primary' else GSR
            assert set(columns).isdisjoint(forbidden)
            prep = preprocessor().fit(frames['train'][columns])
            prep_path = output/'modelos'/f'{task}__{subset}__preprocessor.joblib'
            joblib.dump(prep, prep_path, compress=3)
            prep_catalog.append(dict(task=task, subset=subset, features=columns,
                                     path=prep_path.relative_to(output).as_posix(), sha256=digest(prep_path),
                                     transformed_features=prep.get_feature_names_out().tolist()))
            xs = {s:sequence_array(prep.transform(f[columns]), identities[s][0]) for s,f in frames.items()}
            for kind, target in [('classification',panel['targets'][task][1]),('regression',panel['targets'][task][0])]:
                y = frames['train'][target].map({c:i for i,c in enumerate(CLASSES)}).to_numpy() if kind=='classification' else frames['train'][target].to_numpy(np.float32)
                for architecture in config['architectures'] + (['MLP_current'] if subset=='full' else []):
                    for seed in config['seeds']:
                        print(f'{task} {subset} {kind} {architecture} seed={seed}', flush=True)
                        start = time.monotonic()
                        model, history, best_epoch = fit_network(xs['train'], identities['train'][1], y,
                            xs['validation'], identities['validation'][1], frames['validation'],target,kind,architecture,seed,config)
                        path = output/'modelos'/f'{task}__{subset}__{kind}__{architecture}__{seed}.pt'
                        torch.save(model.state_dict(), path)
                        identity = dict(task=task, subset=subset, kind=kind, architecture=architecture, seed=seed)
                        metadata = dict(**identity, path=path.relative_to(output).as_posix(),sha256=digest(path),
                            inputs=xs['train'].shape[2],outputs=3 if kind=='classification' else 1,
                            hidden=config['hidden'],dropout=config['dropout'],features=columns,target=target,
                            preprocessor=prep_path.relative_to(output).as_posix(),preprocessor_sha256=digest(prep_path),
                            context_windows=8,best_epoch=best_epoch,epochs_run=len(history),
                            seconds=time.monotonic()-start,parameters=sum(p.numel() for p in model.parameters()),
                            train_participants=sorted(frames['train'].participant.unique()))
                        raw = raw_predict(model,xs['validation'],identities['validation'][1])
                        restored = load_net(metadata,output)
                        np.testing.assert_array_equal(raw,raw_predict(restored,xs['validation'],identities['validation'][1]))
                        metadata['reload_verified']=True
                        write_json(path.with_suffix('.json'),metadata)
                        artifacts.append(metadata)
                        metrics.append({**identity,**metric_record(frames['validation'],target,decode(raw,kind),kind), 'best_epoch':best_epoch})
                        histories.extend([{**identity,**row} for row in history])
                        pd.DataFrame(metrics).to_csv(output/'metricas_validacion_entrenamiento.csv',index=False)
                        pd.DataFrame(histories).to_csv(output/'historial_entrenamiento.csv',index=False)
                        print(f'  epoch={best_epoch}/{len(history)} val={metrics[-1]["macro_score"]:.5f} {metadata["seconds"]:.1f}s',flush=True)
    write_json(output/'catalogo_modelos.json',artifacts)
    write_json(output/'preprocesadores.json',prep_catalog)
    pd.DataFrame(coverage).to_csv(output/'cobertura_historial.csv',index=False)
    results = pd.DataFrame(metrics)
    averages = results.groupby(['task','kind','subset','architecture']).macro_score.mean().reset_index()
    averages = averages.loc[~averages.architecture.eq('MLP_current')]
    selection = []
    for (task,kind), group in averages.groupby(['task','kind']):
        for scope in ['panel','full']:
            candidates = group if scope=='panel' else group.loc[group.subset.eq('full')]
            best = candidates.sort_values(['macro_score','subset','architecture'],ascending=[False,True,True]).iloc[0]
            selection.append(dict(task=task,kind=kind,scope=scope,subset=best.subset,architecture=best.architecture,
                                  validation_mean=float(best.macro_score),seeds=config['seeds']))
    write_json(output/'seleccion_antes_test.json',dict(frozen_utc=datetime.now(timezone.utc).isoformat(),
        rule=config['selection'],models=selection,test_used=False))
    write_json(output/'entrenamiento_completo.json',dict(models=len(artifacts),completed_utc=datetime.now(timezone.utc).isoformat(),
        protocol_sha256=digest(output/'protocolo.json'),catalog_sha256=digest(output/'catalogo_modelos.json'),
        selection_sha256=digest(output/'seleccion_antes_test.json'),test_used=False))
    print('ENTRENAMIENTO COMPLETO',flush=True)


if __name__=='__main__':
    main()
