"""Transformer y TCN: secuencias pasadas, seleccion interna y bundles portables."""
import numpy as np
import torch
from torch import nn
from temporales_core import CausalBlock, preprocessor, seed_all, raw_predict
from hiperparametros_core import FULL, TARGET
from avanzados_core import sample_weights
from optimizar_historial import histories, smooth


def grid():
    return [dict(id=f'{family}_{i}', family=family, context=context, hidden=hidden,
                 dropout=dropout, lr=lr, decay=decay)
            for family in ['Transformer', 'TCN']
            for i, (context, hidden, dropout, lr, decay) in enumerate([
                (8, 16, .2, .001, .01), (32, 16, .3, .0005, .01),
                (32, 32, .4, .001, .1)])]


class SequenceNet(nn.Module):
    def __init__(self, inputs, config):
        super().__init__()
        self.config = config
        h = config['hidden']; d = config['dropout']
        if config['family'] == 'Transformer':
            self.project = nn.Linear(inputs, h)
            self.position = nn.Parameter(torch.randn(1, config['context'], h) * .02)
            self.body = nn.TransformerEncoder(nn.TransformerEncoderLayer(
                h, 4, h*2, d, batch_first=True, norm_first=True), 1,
                norm=nn.LayerNorm(h), enable_nested_tensor=False)
        else:
            self.body = nn.Sequential(CausalBlock(inputs, h, 1, d),
                CausalBlock(h, h, 2, d), CausalBlock(h, h, 4, d), CausalBlock(h, h, 8, d))
        self.head = nn.Linear(h, 3)

    def forward(self, x, lengths):
        if self.config['family'] == 'Transformer':
            padding = torch.arange(x.shape[1])[None, :] >= lengths[:, None]
            causal = torch.ones(x.shape[1], x.shape[1], dtype=torch.bool).triu(1)
            z = self.body(self.project(x) + self.position[:, :x.shape[1]],
                          mask=causal, src_key_padding_mask=padding)
        else:
            z = self.body(x.transpose(1, 2)).transpose(1, 2)
        return self.head(z[torch.arange(len(x)), lengths - 1])


def sequences(prep, frame, config, repeat=False):
    values = prep.transform(frame[FULL]).astype(np.float32)
    x = np.zeros((len(frame), config['context'], values.shape[1]), np.float32)
    lengths = np.zeros(len(frame), np.int64)
    for i, indices in histories(frame, config['context'], 'recording'):
        lengths[i] = len(indices)
        x[i, :len(indices)] = values[i] if repeat else values[indices]
    return x, lengths


def train(frame, config, seed, epochs, callback=None, repeat=False):
    seed_all(seed); torch.set_num_threads(2)
    prep = preprocessor().fit(frame[FULL])
    x, lengths = sequences(prep, frame, config, repeat)
    model = SequenceNet(x.shape[2], config)
    xx = torch.from_numpy(x); ll = torch.from_numpy(lengths)
    yy = torch.tensor(frame[TARGET].map({'bajo': 0, 'medio': 1, 'alto': 2}).to_numpy(), dtype=torch.long)
    weights = torch.tensor(sample_weights(frame, 'participant'), dtype=torch.float32)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config['lr'], weight_decay=config['decay'])
    curve = []
    for epoch in range(1, epochs+1):
        model.train(); order = torch.randperm(len(frame)); total = 0.
        for start in range(0, len(frame), 256):
            ix = order[start:start+256]; optimizer.zero_grad(set_to_none=True)
            loss = (nn.functional.cross_entropy(model(xx[ix], ll[ix]), yy[ix], reduction='none') * weights[ix]).mean()
            if not torch.isfinite(loss):
                raise ValueError('Nonfinite loss')
            loss.backward(); nn.utils.clip_grad_norm_(model.parameters(), 1.); optimizer.step()
            total += loss.item() * len(ix)
        curve.append(dict(epoch=epoch, loss=total/len(frame)))
        if callback is not None:
            callback(epoch, bundle(model, prep, config, seed, epoch, repeat), curve)
    return bundle(model, prep, config, seed, epochs, repeat), curve


def bundle(model, prep, config, seed, epoch, repeat):
    return dict(state={k: v.detach().clone() for k, v in model.state_dict().items()},
                prep=prep, config=config, inputs=model.head.in_features,
                input_features=len(prep.get_feature_names_out()), seed=seed,
                epoch=epoch, repeat=repeat, smoothing=1, features=FULL)


def predict(b, frame):
    model = SequenceNet(b['input_features'], b['config']); model.load_state_dict(b['state']); model.eval()
    x, lengths = sequences(b['prep'], frame, b['config'], b['repeat'])
    raw = raw_predict(model, x, lengths, batch=256)
    prob = torch.softmax(torch.from_numpy(raw), dim=1).numpy()
    return smooth(frame, prob, b['smoothing'])
