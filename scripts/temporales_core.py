"""Redes temporales sobre historia disponible de features por ventana (CPU)."""
from __future__ import annotations
import hashlib
import json
import random
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.nn import functional as F
from torch.nn.utils.rnn import pack_padded_sequence
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import balanced_accuracy_score, f1_score, mean_absolute_error, r2_score

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'resultados/temporales_07-09-2026'
STATIC = ROOT / 'resultados/estabilidad_variables_07-09-2026'
CLASSES = ['bajo', 'medio', 'alto']


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')


def seed_all(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(4)
    torch.use_deterministic_algorithms(True)


def preprocessor():
    return Pipeline([('imputer', SimpleImputer(strategy='median', add_indicator=True, keep_empty_features=True)),
                     ('scale', StandardScaler())])


def prepare_frame(data, task, targets, split):
    score, label = targets[task]
    frame = data.loc[data.split.eq(split) & data[score].notna() & data[label].notna()].copy()
    keys = ['participant', 'recording', 'segment_id', 'stimulus']
    if frame[keys].isna().any().any():
        raise ValueError('Identidad de secuencia ausente')
    frame = frame.sort_values(keys + ['window_start_utc']).reset_index(drop=True)
    return frame


def history_indices(frame, context=8):
    """Indices cronologicos, padding -1 a derecha; reinicia al cambiar segmento o hueco."""
    if context < 1:
        raise ValueError('Contexto debe ser positivo')
    index = np.full((len(frame), context), -1, dtype=np.int64)
    lengths = np.zeros(len(frame), dtype=np.int64)
    keys = ['split', 'participant', 'recording', 'segment_id', 'stimulus']
    timestamps = pd.to_datetime(frame.window_start_utc, utc=True).dt.as_unit('ns').astype('int64').to_numpy() / 1e9
    if frame.duplicated(keys + ['window_start_utc']).any():
        raise ValueError('Ventana duplicada')
    for positions in frame.groupby(keys, sort=False).indices.values():
        history = []
        for ix in positions:
            if history:
                gap = timestamps[ix] - timestamps[history[-1]]
                if gap <= 0:
                    raise ValueError('Secuencia no ordenada')
                if not np.isclose(gap, 1.0, atol=1e-4, rtol=0):
                    history = []
            history = (history + [ix])[-context:]
            lengths[ix] = len(history)
            index[ix, :len(history)] = history
    if (lengths == 0).any():
        raise ValueError('Ventana sin secuencia')
    return index, lengths


def sequence_array(transformed, indices):
    result = transformed[np.maximum(indices, 0)].astype(np.float32)
    result[indices < 0] = 0
    return result


class CausalBlock(nn.Module):
    def __init__(self, inputs, hidden, dilation, dropout):
        super().__init__()
        self.left = 2 * dilation
        self.conv1 = nn.Conv1d(inputs, hidden, 3, dilation=dilation)
        self.conv2 = nn.Conv1d(hidden, hidden, 3, dilation=dilation)
        self.skip = nn.Conv1d(inputs, hidden, 1) if inputs != hidden else nn.Identity()
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        z = self.dropout(F.relu(self.conv1(F.pad(x, (self.left, 0)))))
        z = self.dropout(F.relu(self.conv2(F.pad(z, (self.left, 0)))))
        return F.relu(z + self.skip(x))


class TemporalNet(nn.Module):
    def __init__(self, architecture, inputs, outputs, hidden=24, dropout=.2):
        super().__init__()
        self.architecture = architecture
        if architecture == 'TCN':
            self.body = nn.Sequential(CausalBlock(inputs, hidden, 1, dropout),
                                      CausalBlock(hidden, hidden, 2, dropout))
            width = hidden
        elif architecture in ['LSTM', 'BiLSTM']:
            self.body = nn.LSTM(inputs, hidden, batch_first=True, bidirectional=architecture == 'BiLSTM')
            width = hidden * (2 if architecture == 'BiLSTM' else 1)
        elif architecture == 'MLP_current':
            self.body = nn.Sequential(nn.Linear(inputs, hidden), nn.ReLU(), nn.Dropout(dropout),
                                      nn.Linear(hidden, hidden), nn.ReLU())
            width = hidden
        else:
            raise ValueError(architecture)
        self.head = nn.Sequential(nn.Dropout(dropout), nn.Linear(width, outputs))

    def forward(self, x, lengths):
        if self.architecture == 'TCN':
            z = self.body(x.transpose(1, 2)).transpose(1, 2)
            z = z[torch.arange(len(x)), lengths - 1]
        elif self.architecture in ['LSTM', 'BiLSTM']:
            packed = pack_padded_sequence(x, lengths.cpu(), batch_first=True, enforce_sorted=False)
            _, (h, _) = self.body(packed)
            z = torch.cat([h[-2], h[-1]], dim=1) if self.architecture == 'BiLSTM' else h[-1]
        else:
            z = self.body(x[torch.arange(len(x)), lengths - 1])
        return self.head(z)


def raw_predict(model, x, lengths, batch=512):
    model.eval()
    result = []
    with torch.inference_mode():
        for start in range(0, len(x), batch):
            result.append(model(torch.as_tensor(x[start:start+batch]),
                                torch.as_tensor(lengths[start:start+batch])).numpy())
    return np.concatenate(result)


def decode(raw, kind):
    return np.asarray(CLASSES)[raw.argmax(axis=1)] if kind == 'classification' else raw[:, 0]


def individual_scores(frame, target, prediction, kind):
    rows = []
    for person, positions in frame.groupby('participant', sort=True).indices.items():
        y, p = frame.iloc[positions][target].to_numpy(), prediction[positions]
        if kind == 'classification':
            value = np.mean([np.mean(p[y == c] == c) for c in np.unique(y)])
        else:
            value = -np.mean((y.astype(float) - p) ** 2)
        rows.append((person, float(value)))
    return dict(rows)


def metric_record(frame, target, prediction, kind):
    scores = individual_scores(frame, target, prediction, kind)
    row = dict(macro_score=float(np.mean(list(scores.values()))), rows=len(frame), participants=len(scores))
    if kind == 'classification':
        row.update(balanced_accuracy=balanced_accuracy_score(frame[target], prediction),
                   macro_f1=f1_score(frame[target], prediction, average='macro', zero_division=0))
    else:
        row.update(r2=r2_score(frame[target], prediction), mae=mean_absolute_error(frame[target], prediction),
                   mse=float(np.mean((frame[target].to_numpy(float)-prediction)**2)))
    return row


def load_net(metadata, output=OUT):
    model = TemporalNet(metadata['architecture'], metadata['inputs'], metadata['outputs'],
                        metadata['hidden'], metadata['dropout'])
    weights = output / metadata['path']
    if digest(weights) != metadata['sha256']:
        raise ValueError('Hash de pesos no coincide')
    model.load_state_dict(torch.load(weights, map_location='cpu', weights_only=True))
    model.eval()
    return model
