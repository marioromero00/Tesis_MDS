"""Modelo más complejo: red convolucional sobre el EEG crudo (23-11-2026).

Pedido por Mario el 23-11-2026 ("probar otros modelos más complejos"). Registrado antes de correr; se ejecuta
una vez. Análisis dirigido: las 41 personas y todos los resultados previos ya se vieron.

Contexto: los modelos complejos sobre las variables calculadas (GRU, TCN, Transformer, CatBoost, redes) ya se
probaron entre septiembre y el 16-11 y no superaron al HGB. Lo que no se había probado es aprender directamente
de la señal cruda, que podría aprovechar información que las variables resumidas pierden.

Pregunta: ¿una red convolucional sobre el EEG crudo de la ventana detecta mejor que el HGB con las variables
de EEG, en atención y en activación? ¿Y sigue dependiendo de los componentes oculares?

Entrada: los primeros 240 puntos (1,92 s) de la ventana de 16 canales, con el mismo tratamiento que la
extracción de variables (tendencia lineal, notch 50 Hz, 1–45 Hz dentro de la ventana). Un canal no utilizable
en la ventana va en cero. Cada canal se divide por la mediana de su desviación estándar en las ventanas de la
persona (sin etiquetas; transductivo como la normalización por persona) y se recorta a ±8.
Dos versiones de la señal: original, y limpia con el filtro ica3 de `limpieza_ocular_41p.py`.

Red (fijada de antemano, sin búsqueda de hiperparámetros): tipo EEGNet. Convolución temporal (8 filtros,
32 puntos), convolución espacial en profundidad sobre los 16 canales (multiplicador 2), promedio cada 4 puntos,
convolución separable (16 filtros, 16 puntos), promedio cada 8, capa lineal. Abandono 0,5. AdamW, tasa 0,001,
decaimiento 0,01, 30 épocas, lotes de 128, pérdida ponderada con los mismos pesos por persona y clase que el
HGB. Sin parada temprana ni conjunto de validación: se usa el modelo de la última época.

Evaluación: las mismas 5 particiones por persona (semillas 1101–1105, 8 grupos) y las mismas ventanas.
Modelos nuevos: red_orig y red_ica3 (atención), red_act (activación) y hgb_eeg_act (HGB solo con variables de
EEG en activación, configuración congelada de 15 hojas, como comparador equivalente).
Comparadores ya corridos: eeg_c1 (22-11) e ica3_full (23-11).

Familia confirmatoria (Holm sobre 4), AUC por persona promediada sobre las 5 particiones:
  R1 red_orig − eeg_c1        atención: red sobre crudo frente a HGB sobre variables
  R2 red_ica3 − ica3_full     atención con EEG limpio: lo mismo
  R3 red_orig − red_ica3      atención: la red también pierde al quitar los componentes oculares
  R4 red_act − hgb_eeg_act    activación: red sobre crudo frente a HGB sobre variables de EEG
Lectura fijada: R1, R2 o R4 con respaldo = la señal cruda contiene información que las variables pierden;
nulo concluyente o inferior = un modelo más complejo no mejora la detección. R3 con respaldo = la dependencia
ocular no es propia del HGB ni de las variables elegidas.

Descriptivos: AUC de cada modelo y contraste con 0,5; red_act frente a hgb_c1 de activación (EEG + mirada +
pupila, fase 1); Spearman de la probabilidad de la red con las variables oculares.

Reglas de decisión (las mismas, margen 0,02): respaldo: p Holm < 0,05 e IC 95 % inferior > 0; efecto relevante:
además IC 95 % inferior > 0,02; nulo concluyente: IC 90 % dentro de (−0,02; +0,02); inferior: IC 95 % superior
< 0; resto: inconcluso.
"""
from __future__ import annotations
import argparse, json
from multiprocessing import Pool
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from torch import nn
from scipy.signal import detrend, sosfiltfilt, filtfilt
from scipy.stats import spearmanr
from threadpoolctl import threadpool_limits
from atencion_binaria import ROOT, digest, write
from eeg_por_canal_v2 import SOS, NOTCH
from reconstruir_profesor_atencion_binaria import COLUMNS
import cierre_experimental_v3 as V3
import cierre_final_41p as F
import reapertura_41p as R
import enfoques_41p as E
import montaje_ocular_41p as M
import limpieza_ocular_41p as L

OUT = ROOT / 'resultados/red_cruda_41p_23-11-2026'
TENS = M.CACHE.parent / 'red_cruda_tensores'   # fuera de Git; se registran sus hashes
SEEDS = R.REP_SEEDS
N, CLIP = 240, 8.
NET = dict(f1=8, depth=2, f2=16, k1=32, k2=16, dropout=.5, epochs=30, batch=128, lr=1e-3, weight_decay=.01)
MODELS = {'red_orig': ('atencion', 'orig'), 'red_ica3': ('atencion', 'ica3'), 'red_act': ('activacion', 'orig')}


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        f1, d, f2 = NET['f1'], NET['depth'], NET['f2']
        self.body = nn.Sequential(
            nn.Conv2d(1, f1, (1, NET['k1']), padding=(0, NET['k1'] // 2), bias=False), nn.BatchNorm2d(f1),
            nn.Conv2d(f1, f1 * d, (16, 1), groups=f1, bias=False), nn.BatchNorm2d(f1 * d), nn.ELU(),
            nn.AvgPool2d((1, 4)), nn.Dropout(NET['dropout']),
            nn.Conv2d(f1 * d, f1 * d, (1, NET['k2']), padding=(0, NET['k2'] // 2), groups=f1 * d, bias=False),
            nn.Conv2d(f1 * d, f2, 1, bias=False), nn.BatchNorm2d(f2), nn.ELU(),
            nn.AvgPool2d((1, 8)), nn.Dropout(NET['dropout']), nn.Flatten())
        with torch.no_grad():
            n = self.body(torch.zeros(1, 1, 16, N)).shape[1]
        self.out = nn.Linear(n, 1)

    def forward(self, x):
        return self.out(self.body(x[:, None])).squeeze(1)


def plan():
    return json.loads((OUT / 'protocolo.json').read_text())


def inputs():
    paths = [Path(__file__), *(ROOT / f'scripts/{n}.py' for n in
             ['limpieza_ocular_41p', 'montaje_ocular_41p', 'eeg_por_canal_v2', 'enfoques_41p', 'reapertura_41p',
              'cierre_final_41p', 'cierre_experimental_v3']),
             R.OUT / 'protocolo.json', V3.SOURCE, V3.PARTS, V3.LABELS_ACT, V3.TEACHER, *V3.SPATIAL,
             *(E.OUT / f'e2_{s}.csv.gz' for s in SEEDS), *(L.OUT / f'pred_{s}.csv.gz' for s in SEEDS),
             *(R.OUT / f'rep_activacion_{s}.csv.gz' for s in SEEDS), *sorted((L.OUT / 'filtros').glob('*.npz'))]
    return {str(p.relative_to(ROOT)): digest(p) for p in paths}


def prepare():
    OUT.mkdir(exist_ok=False)
    write(OUT / 'protocolo.json', dict(
        created_utc=pd.Timestamp.now(tz='UTC').isoformat(),
        approval='Mario pide probar modelos más complejos, 23-11-2026. Registrado antes de correr.',
        directed=True, inputs=inputs(), raw={p.name: digest(p) for p in sorted(M.CACHE.glob('*.npz'))},
        leaves=F.LEAVES, folds_rep=R.plan()['folds_rep'], margin=F.MARGIN, net=NET, samples=N, clip=CLIP,
        models={k: list(v) for k, v in MODELS.items()} | {'hgb_eeg_act': ['activacion', 'variables EEG']},
        init_seed='semilla de partición * 100 + grupo',
        confirmatory=['R1 red_orig − eeg_c1', 'R2 red_ica3 − ica3_full', 'R3 red_orig − red_ica3',
                      'R4 red_act − hgb_eeg_act'], holm='sobre las 4 pruebas',
        decision=dict(respaldo='p Holm < 0,05 e IC95 inferior > 0', relevante='además IC95 inferior > 0,02',
                      nulo='IC90 dentro de (−0,02; +0,02)', inferior='IC95 superior < 0', resto='inconcluso'),
        limits='Análisis dirigido. Una sola arquitectura y una sola configuración, sin búsqueda: un resultado '
               'nulo no descarta que otra red rinda más. Una inicialización por grupo. La escala por persona '
               'usa toda su sesión. La red ve 1,92 s de los 2 s. Las variables del HGB incluyen indicadores de '
               'calidad de canal que la red no recibe de forma explícita.'))
    print('Registrado', OUT / 'protocolo.json')


def verify():
    p = plan()
    for path, h in p['inputs'].items():
        assert digest(ROOT / path) == h, path
    return p


# ---------------------------------------------------------------- tensores (sin etiquetas)
def person(args):
    p, windows = args
    with threadpool_limits(limits=1):
        d = np.load(M.CACHE / f'{p}.npz')
        t, x = d['eeg_t'], d['eeg']
        filt = {'orig': np.zeros((16, 16)), 'ica3': np.load(L.OUT / 'filtros' / f'{p}.npz')['ica3']}
        out = {k: np.zeros((len(windows), 16, N), 'float32') for k in filt}
        used = np.zeros((len(windows), 16), bool)
        for i, w in enumerate(windows.itertuples(index=False)):
            lo, hi = np.searchsorted(t, [pd.Timestamp(w.window_start_utc).timestamp(), pd.Timestamp(w.window_end_utc).timestamp()])
            xs = x[lo:hi]
            assert len(xs) == int(w.eeg_n) and len(xs) >= N, (p, w.source_row)
            ok = L.window_usable(xs) & (float(np.diff(t[lo:hi]).max()) <= .1)
            used[i] = ok
            for k, m in filt.items():
                y = sosfiltfilt(SOS, filtfilt(*NOTCH, detrend(L.clean_window(xs, m), axis=0, type='linear'), axis=0), axis=0)
                out[k][i] = (y[:N] * ok).T
        for k in out:   # escala por canal: mediana de la desviación estándar en las ventanas utilizables de la persona
            sd = out[k].std(axis=2)
            scale = np.array([np.median(sd[used[:, c], c]) if used[:, c].any() else 1. for c in range(16)])
            out[k] = np.clip(out[k] / np.maximum(scale, 1e-6)[None, :, None], -CLIP, CLIP).astype('float32')
    print(p, len(windows), 'ventanas', flush=True)
    return windows.source_row.to_numpy(), out


def tensors():
    p = verify()
    for name, h in p['raw'].items():
        assert digest(M.CACHE / name) == h, name
    TENS.mkdir(exist_ok=False)
    d = V3.load_data()
    jobs = [(q, g[['source_row', 'window_start_utc', 'window_end_utc', 'eeg_n']]) for q, g in d.groupby('participant')]
    with Pool(10) as pool:
        res = pool.map(person, jobs, chunksize=1)
    rows = np.concatenate([r[0] for r in res])
    assert len(rows) == len(d) and len(set(rows)) == len(rows)
    np.save(TENS / 'source_row.npy', rows)
    for k in ['orig', 'ica3']:
        np.save(TENS / f'{k}.npy', np.concatenate([r[1][k] for r in res]))
    write(OUT / 'tensores.json', {f: digest(TENS / f) for f in ['source_row.npy', 'orig.npy', 'ica3.npy']})
    print('Tensores listos')


def load_tensor(kind, rows):
    done = json.loads((OUT / 'tensores.json').read_text())
    for f in ['source_row.npy', f'{kind}.npy']:
        assert digest(TENS / f) == done[f], f
    pos = pd.Series(np.arange(len(np.load(TENS / 'source_row.npy'))), index=np.load(TENS / 'source_row.npy'))
    return np.load(TENS / f'{kind}.npy')[pos.loc[rows].to_numpy()]


# ---------------------------------------------------------------- red
def fit_net(X, y, w, seed):
    torch.manual_seed(seed)
    net = Net()
    opt = torch.optim.AdamW(net.parameters(), lr=NET['lr'], weight_decay=NET['weight_decay'])
    Xt, Yt, Wt = torch.from_numpy(X), torch.from_numpy(y.astype('float32')), torch.from_numpy(w.astype('float32'))
    loss = nn.BCEWithLogitsLoss(reduction='none')
    gen = torch.Generator().manual_seed(seed)
    for _ in range(NET['epochs']):
        net.train()
        for b in torch.randperm(len(Xt), generator=gen).split(NET['batch']):
            opt.zero_grad()
            (loss(net(Xt[b]), Yt[b]) * Wt[b]).mean().backward()
            opt.step()
    return net


@torch.no_grad()
def predict_net(net, X):
    net.eval()
    return np.concatenate([torch.sigmoid(net(b)).numpy() for b in torch.from_numpy(X).split(2048)])


def run(model, seed):
    p = verify()
    dest = OUT / f'{model}_{seed}.csv.gz'
    assert not dest.exists()
    task = 'activacion' if model == 'hgb_eeg_act' else MODELS[model][0]
    T = V3.Task(V3.load_data(), task)
    X = None if model == 'hgb_eeg_act' else load_tensor(MODELS[model][1], T.lab.source_row.to_numpy())
    preds = []
    for k, test_people in enumerate(E.folds_of(p, seed)):
        test = T.lab.participant.isin(test_people).to_numpy()
        fit, ev = np.flatnonzero(~test), np.flatnonzero(test)
        y, w = T.lab.y.to_numpy()[fit], V3.weights(T.lab.iloc[fit])
        if model == 'hgb_eeg_act':
            prep = V3.preprocessor().fit(T.lab.iloc[fit][L.FULL])
            Xf, Xe = (prep.transform(T.lab.iloc[r][L.FULL]).astype('float32') for r in (fit, ev))
            prob = V3.fit_hgb(Xf, y, w, p['leaves'][task]).predict_proba(Xe)[:, 1]
        else:
            prob = predict_net(fit_net(X[fit], y, w, seed * 100 + k), X[ev])
        preds.append(E.base_of(T, ev).assign(prob=prob, strategy=model, fold=k, seed=seed))
        print(model, seed, 'fold', k, flush=True)
    pd.concat(preds).to_csv(dest, index=False)


def report():
    d = V3.load_data()
    read = lambda m: pd.concat([pd.read_csv(OUT / f'{m}_{s}.csv.gz') for s in SEEDS])
    old = E.load('e2')
    clean = pd.concat([pd.read_csv(L.OUT / f'pred_{s}.csv.gz') for s in SEEDS])
    att = pd.concat([read('red_orig'), read('red_ica3'), old[old.strategy.eq('eeg_c1')], clean[clean.strategy.eq('ica3_full')]])
    act = pd.concat([read('red_act'), read('hgb_eeg_act'), E.rep('activacion', ('hgb_c1',))])
    for pred in (att, act):
        key = pred.groupby(['seed', 'strategy']).source_row.apply(lambda s: tuple(sorted(s)))
        assert key.nunique() == 1 and pred.groupby(['seed', 'source_row']).y.nunique().eq(1).all()
    wa, wc = E.mean_auc(att), E.mean_auc(act)
    assert len(wa) == 41 and len(wc) == 41
    wa['azar'], wc['azar'] = .5, .5
    conf = E.family([dict(test='R1', contrast='red_orig − eeg_c1', **R.contrast(wa, 'red_orig', 'eeg_c1')),
                     dict(test='R2', contrast='red_ica3 − ica3_full', **R.contrast(wa, 'red_ica3', 'ica3_full')),
                     dict(test='R3', contrast='red_orig − red_ica3', **R.contrast(wa, 'red_orig', 'red_ica3')),
                     dict(test='R4', contrast='red_act − hgb_eeg_act', **R.contrast(wc, 'red_act', 'hgb_eeg_act'))])
    desc = E.absolute(wa, ['red_orig', 'red_ica3', 'eeg_c1', 'ica3_full'], label='atención')
    desc += E.absolute(wc, ['red_act', 'hgb_eeg_act', 'hgb_c1'], label='activación')
    desc += [dict(label='atención', item=f'{s} − 0,5', **R.contrast(wa, s, 'azar')) for s in ['red_orig', 'red_ica3']]
    desc += [dict(label='activación', item=f'{s} − 0,5', **R.contrast(wc, s, 'azar')) for s in ['red_act', 'hgb_eeg_act']]
    desc.append(dict(label='activación', item='red_act − hgb_c1 (EEG + mirada + pupila)', **R.contrast(wc, 'red_act', 'hgb_c1')))
    desc.append(dict(label='activación', item='hgb_c1 − hgb_eeg_act', **R.contrast(wc, 'hgb_c1', 'hgb_eeg_act')))
    score, z = E.ocular(d)
    ref = z.assign(puntaje=score, source_row=d.source_row.to_numpy(), participant=d.participant.to_numpy())
    for strat in ['red_orig', 'red_ica3']:
        m = att[att.strategy.eq(strat)].groupby('source_row').prob.mean().rename('prob').reset_index().merge(ref, on='source_row')
        for c in ['puntaje'] + COLUMNS:
            rho = m.groupby('participant').apply(lambda g: spearmanr(g.prob, g[c]).statistic).dropna()
            lo, hi = F.ci(rho)
            desc.append(dict(label='atención', item=f'Spearman prob {strat} con {c}', delta=float(rho.mean()), low95=lo, high95=hi,
                             people=len(rho), improved=int((rho > 0).sum()), p=F.sign_flip(rho.to_numpy())))
    conf.to_csv(OUT / 'confirmatorio.csv', index=False)
    pd.DataFrame(desc).to_csv(OUT / 'descriptivos.csv', index=False)
    wa.drop(columns='azar').join(wc.drop(columns='azar'), rsuffix='_act').to_csv(OUT / 'auc_por_persona.csv')
    pd.set_option('display.width', 280)
    print(conf.round(4).to_string(index=False))
    print(pd.DataFrame(desc).round(4).to_string(index=False))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['prepare', 'tensors', 'run', 'report'])
    ap.add_argument('--model', choices=list(MODELS) + ['hgb_eeg_act'])
    ap.add_argument('--seed', type=int)
    a = ap.parse_args()
    if a.phase == 'run':
        torch.set_num_threads(1)
        with threadpool_limits(limits=1):
            run(a.model, a.seed)
    else:
        globals()[a.phase]()
