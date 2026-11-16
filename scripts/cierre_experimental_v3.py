"""Cierre experimental V3 (16-11-2026).

Cuatro mejoras sobre la corrida V2, en ambas tareas (atención y activación):
  A. Historial completo: las ventanas previas se toman de todas las ventanas del segmento
     (no solo de las etiquetadas). Las etiquetas solo definen qué filas se entrenan/evalúan.
  B. Modelo sensible al orden: GRU sobre la secuencia ordenada, contra la misma GRU con
     una sola ventana (control emparejado).
  C. Métricas del manuscrito: BA, macro-F1 y recall por clase con umbral fijo 0,5.
  D. Fusión tardía: promedio de probabilidades de modelos por señal vs fusión temprana.

Fases: prepare -> train (selección solo en train, OOF, congelación) -> evaluate (validación
y test una sola vez) -> report. Ninguna decisión usa validación ni test.
"""
from __future__ import annotations
import argparse, json, time
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import torch
from torch import nn
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score, balanced_accuracy_score, f1_score, recall_score
from threadpoolctl import threadpool_limits
from atencion_binaria import ROOT, digest, write
from temporales_core import preprocessor, history_indices
from baselines_estaticos import EEG, GSR, EYE, PUPIL
from evaluar_test_temporalidad_eeg_v2 import label_with_teacher
from evaluar_temporalidad_eeg_v2 import ci
from reconstruir_profesor_atencion_binaria import KEYS
from eeg_por_canal_v2 import FEATURES as CHANNELS

OUT = ROOT / 'resultados/cierre_v3_16-11-2026'
SOURCE = ROOT / 'resultados/preprocesamiento/caracteristicas_multimodales.csv'
PARTS = ROOT / 'resultados/modelado/particion_participantes.csv'
LABELS_ACT = ROOT / 'resultados/etiquetas_gsr_calidad_v2_01-11-2026/etiquetas.csv.gz'
TEACHER = ROOT / 'resultados/temporalidad_eeg_v2_validacion_29-10-2026/profesor_final.joblib'
FOLDS = ROOT / 'resultados/profesor_binario_reconstruido_29-10-2026/protocolo.json'
SPATIAL = [ROOT / 'resultados/eeg_por_canal_v2_29-10-2026/caracteristicas_eeg_por_canal.csv.gz',
           ROOT / 'resultados/temporalidad_eeg_v2_validacion_29-10-2026/caracteristicas_validation.csv.gz',
           ROOT / 'resultados/temporalidad_eeg_v2_test_29-10-2026/caracteristicas_test.csv.gz']
GROUPS = {'atencion': {'EEG': EEG + CHANNELS, 'GSR': GSR},
          'activacion': {'EEG': EEG + CHANNELS, 'Eye': EYE, 'Pupil': PUPIL}}
FORBIDDEN = {'atencion': EYE + PUPIL, 'activacion': GSR}
HGB = dict(max_iter=300, l2_regularization=10., learning_rate=.05, min_samples_leaf=30,
           early_stopping=False, random_state=20261116)
LEAVES = [7, 15]
GRU = dict(hidden=64, dropout=.3, epochs=12, batch=256, lr=1e-3, weight_decay=1e-2, seeds=[1, 2, 3])
THRESHOLD = .5
STRATEGIES = ['hgb_c1', 'hgb_c5', 'hgb_c8', 'hgb_c32', 'hgb_c32_etiq', 'gru_c1', 'gru_c32', 'tardia_c1', 'tardia_c32']
CONTRASTS = [  # (nombre, con historial, sin historial, rol)
    ('gru_orden', 'gru_c32', 'gru_c1', 'principal A'),
    ('hgb_resumen', 'hgb_c32', 'hgb_c1', 'principal B'),
    ('hgb_c8', 'hgb_c8', 'hgb_c1', 'secundario'),
    ('hgb_c5_soporte', 'hgb_c5', 'hgb_c1', 'control: iguala el soporte de 6 s de la etiqueta de activación'),
    ('hgb_c32_vs_c5', 'hgb_c32', 'hgb_c5', 'secundario: historial más allá del soporte de la etiqueta'),
    ('historial_completo', 'hgb_c32', 'hgb_c32_etiq', 'secundario'),
    ('tardia_vs_temprana_c1', 'tardia_c1', 'hgb_c1', 'secundario'),
    ('tardia_vs_temprana_c32', 'tardia_c32', 'hgb_c32', 'secundario'),
    ('gru_vs_hgb_c32', 'gru_c32', 'hgb_c32', 'secundario')]


def plan():
    return json.loads((OUT / 'protocolo.json').read_text())


def inputs():
    paths = [SOURCE, PARTS, LABELS_ACT, TEACHER, FOLDS, *SPATIAL, Path(__file__),
             ROOT / 'scripts/temporales_core.py', ROOT / 'scripts/evaluar_test_temporalidad_eeg_v2.py',
             ROOT / 'scripts/reconstruir_profesor_atencion_binaria.py', ROOT / 'scripts/evaluar_temporalidad_eeg_v2.py',
             ROOT / 'scripts/baselines_estaticos.py', ROOT / 'scripts/eeg_por_canal_v2.py', ROOT / 'scripts/atencion_binaria.py']
    return {str(p.relative_to(ROOT)): digest(p) for p in paths}


def verify_inputs():
    for path, h in plan()['inputs'].items():
        assert digest(ROOT / path) == h, path


# ---------------------------------------------------------------- datos
def load_data():
    data = pd.read_csv(SOURCE)
    data['source_row'] = np.arange(len(data))
    data['split'] = data.participant.map(pd.read_csv(PARTS).set_index('participant').split)
    spatial = pd.concat([pd.read_csv(p)[['source_row'] + CHANNELS] for p in SPATIAL])
    assert not spatial.source_row.duplicated().any()
    data = data[data.split.isin(['train', 'validation', 'test'])].merge(spatial, on='source_row', validate='one_to_one')
    data = data.sort_values(KEYS).reset_index(drop=True)
    teacher = joblib.load(TEACHER)
    y_att, _ = label_with_teacher(data, teacher)
    act = pd.read_csv(LABELS_ACT)[['source_row', 'activation_binary_v2']]
    data = data.merge(act, on='source_row', how='left', validate='one_to_one')
    data['y_atencion'] = y_att.astype('float')
    data['y_activacion'] = data.activation_binary_v2.astype('float')
    return data.sort_values(KEYS).reset_index(drop=True)


def weights(f):
    w = 1 / (f.groupby(['participant', 'y']).y.transform('size') * f.groupby('participant').y.transform('nunique'))
    return (w / w.mean()).to_numpy()


class Task:
    """Todas las ventanas de una tarea (para historial) y sus filas etiquetadas."""

    def __init__(self, data, task):
        self.task = task
        self.cols = sum(GROUPS[task].values(), [])
        assert not set(self.cols) & set(FORBIDDEN[task])
        self.all = data[KEYS + ['split', 'source_row'] + self.cols].copy().reset_index(drop=True)
        self.all['y'] = data[f'y_{task}'].to_numpy()
        self.hist = {c: history_indices(self.all, c) for c in [5, 8, 32]}
        lab = self.all[self.all.y.notna()].copy()
        self.lab_pos = lab.index.to_numpy()  # posición de cada fila etiquetada en self.all
        lab = lab.reset_index(drop=True)
        lab['y'] = lab.y.astype(int)
        self.lab = lab
        # historial solo con filas etiquetadas (protocolo V2), como referencia
        self.hist_etiq = history_indices(lab, 32)

    def rows(self, people):
        m = self.lab.participant.isin(people).to_numpy()
        return np.flatnonzero(m)


def summary_rep(Z, ix, lengths):
    x = Z[np.maximum(ix, 0)]
    mask = (ix >= 0)[:, :, None]
    x = np.where(mask, x, 0)
    mean = x.sum(axis=1) / lengths[:, None]
    var = (((x - mean[:, None, :]) ** 2) * mask).sum(axis=1) / lengths[:, None]
    return mean, np.sqrt(np.maximum(var, 0))


def hgb_matrix(T, Z_all, Z_lab, rows, kind, cols_idx=None):
    """Representación HGB para filas etiquetadas `rows`."""
    sel = slice(None) if cols_idx is None else cols_idx
    cur = Z_lab[rows][:, sel]
    if kind == 1:
        return cur
    if kind == 'etiq':
        ix, l = T.hist_etiq
        ix, l = ix[rows], l[rows]
        mean, sd = summary_rep(Z_lab[:, sel], ix, l)
        return np.column_stack([cur, mean, sd]).astype('float32')
    ix, l = T.hist[kind]
    pos = T.lab_pos[rows]
    mean, sd = summary_rep(Z_all[:, sel], ix[pos], l[pos])
    return np.column_stack([cur, mean, sd]).astype('float32')


def fit_hgb(X, y, w, leaves):
    m = HistGradientBoostingClassifier(max_leaf_nodes=int(leaves), **HGB)
    m.fit(X, y, sample_weight=w)
    return m


# ---------------------------------------------------------------- GRU
class Net(nn.Module):
    def __init__(self, d):
        super().__init__()
        h = GRU['hidden']
        self.inp = nn.Sequential(nn.Linear(d, h), nn.ReLU())
        self.gru = nn.GRU(h, h, batch_first=True)
        self.out = nn.Sequential(nn.Dropout(GRU['dropout']), nn.Linear(h, 1))

    def forward(self, x, lengths):
        z = self.inp(x)
        packed = nn.utils.rnn.pack_padded_sequence(z, lengths.cpu(), batch_first=True, enforce_sorted=False)
        _, h = self.gru(packed)
        return self.out(h[-1]).squeeze(-1)


def sequences(T, Z_all, rows, ctx):
    """Secuencias cronológicas (antigua -> actual) desde todas las ventanas; padding a la derecha."""
    pos = T.lab_pos[rows]
    if ctx == 1:
        return Z_all[pos][:, None, :].astype('float32'), np.ones(len(pos), dtype=np.int64)
    ix, l = T.hist[ctx]
    ix, l = ix[pos], l[pos]
    x = Z_all[np.maximum(ix, 0)].astype('float32')
    x[ix < 0] = 0
    return x, l


def fit_gru(x, l, y, w, seed):
    torch.manual_seed(seed)
    np.random.seed(seed)
    net = Net(x.shape[2])
    opt = torch.optim.AdamW(net.parameters(), lr=GRU['lr'], weight_decay=GRU['weight_decay'])
    X, L, Y, W = map(torch.from_numpy, [x, l, y.astype('float32'), w.astype('float32')])
    loss = nn.BCEWithLogitsLoss(reduction='none')
    gen = torch.Generator().manual_seed(seed)
    for _ in range(GRU['epochs']):
        net.train()
        for b in torch.randperm(len(X), generator=gen).split(GRU['batch']):
            opt.zero_grad()
            v = (loss(net(X[b], L[b]), Y[b]) * W[b]).mean()
            v.backward()
            opt.step()
    return net


@torch.no_grad()
def predict_gru(net, x, l):
    net.eval()
    out = []
    X, L = torch.from_numpy(x), torch.from_numpy(l)
    for b in torch.arange(len(X)).split(2048):
        out.append(torch.sigmoid(net(X[b], L[b])).numpy())
    return np.concatenate(out)


# ---------------------------------------------------------------- fases
def prepare():
    OUT.mkdir(exist_ok=False)
    (OUT / 'modelos').mkdir()
    folds = json.loads(FOLDS.read_text())['folds']
    write(OUT / 'protocolo.json', dict(
        created_utc=pd.Timestamp.now(tz='UTC').isoformat(),
        approval='Mario solicita cerrar la experimentación con las mejoras A-D, 16-11-2026',
        inputs=inputs(), groups=GROUPS, hgb=HGB, leaves_grid=LEAVES, gru=GRU, threshold=THRESHOLD,
        strategies=STRATEGIES, contrasts=CONTRASTS, folds=folds,
        labels=dict(atencion='Modelo Profesor PCA congelado (29-10) aplicado a todas las ventanas',
                    activacion='GSR V2 auditada (01-11)'),
        history=dict(full='ventanas previas del mismo segmento/estímulo, consecutivas (1 s), etiquetadas o no; '
                          'sus variables nunca incluyen etiquetas ni señales del Modelo Profesor',
                     etiq='solo filas etiquetadas consecutivas (protocolo V2), como referencia'),
        selection='Hojas HGB [7,15] elegidas en validación interna de train por fold (compartidas entre contextos 1/8/32 '
                  'con historial completo) y para el final con la media de todos los folds. GRU sin búsqueda: '
                  'configuración fija; 3 semillas promediadas. Fusión tardía: promedio simple de HGB por señal con las hojas '
                  'del fold. Nada se elige con validación ni test.',
        metrics='AUC macro por persona; BA, macro-F1 y recall por clase con umbral 0,5; IC 95 % bootstrap por persona '
                '(20000), diferencias pareadas por persona. Exploratorio: validación y test ya consultados.',
        decision='Métrica de decisión: AUC macro por persona. Ventaja consistente = IC 95 % de la diferencia pareada sobre 0 '
                 'en validación y en test (criterios del manuscrito); se reporta además cuántas personas mejoran. '
                 'BA, macro-F1 y recall son descriptivos.',
        amendment='Versión 2 del protocolo (16-11-2026), registrada antes de cualquier evaluación externa. La versión 1 '
                  '(resultados/cierre_v3_16-11-2026_abortado_fusion) se detuvo durante el fold 1 de train por una auditoría '
                  'de código: la fusión tardía no recibía los indicadores de faltantes que sí recibía la temprana. Se corrige y '
                  'se agrega el control hgb_c5, que iguala el soporte de 6 s de la etiqueta de activación.',
        limitations=['Variables transductivas por persona: z de GSR y pupila normalizadas con la sesión completa y componente '
                     'tónica GSR con filtro bidireccional; el historial es causal a nivel de ventana, no de muestra.',
                     'La etiqueta de activación integra 5 ventanas (6 s): parte de la ventaja de c8/c32 puede deberse a igualar '
                     'ese soporte; por eso el control hgb_c5.',
                     'El PCA del Modelo Profesor de atención se ajustó con las 25 personas de train: el OOF de atención tiene '
                     'una fuga leve de etiquetas entre folds; validación y test no se ven afectados.',
                     'En atención casi todas las ventanas tienen etiqueta: el contraste historial_completo solo es informativo '
                     'en activación. Los segmentos son cortos, así que c32 rara vez se completa.',
                     'Validación y test (8 personas cada uno) ya se consultaron en V2; todo es exploratorio y el bootstrap '
                     'percentil con 8 personas puede tener cobertura menor al 95 %.']))
    print('Protocolo registrado', OUT / 'protocolo.json')


def run_task(task, final=False, external=None):
    """Entrena una tarea. final=False -> OOF en train; final=True -> modelos finales congelados."""
    data = load_data()
    T = Task(data, task)
    folds = plan()['folds']
    train_people = sorted(T.lab[T.lab.split.eq('train')].participant.unique())
    preds, trials, sel = [], [], []

    def zfit(fit_rows):
        prep = preprocessor().fit(T.lab.iloc[fit_rows][T.cols])
        return prep, prep.transform(T.all[T.cols]).astype('float32'), prep.transform(T.lab[T.cols]).astype('float32')

    def modality_columns(prep):
        """Columnas de salida de cada señal: sus variables y sus propios indicadores de faltantes."""
        ind = prep.named_steps['imputer'].indicator_.features_
        n = len(T.cols)
        out = {}
        for k, v in GROUPS[task].items():
            own = [T.cols.index(c) for c in v]
            out[k] = own + [n + j for j, f in enumerate(ind) if f in set(own)]
        assert sorted(sum(out.values(), [])) == list(range(n + len(ind)))
        return out

    def strategies(fit_rows, ev_rows, leaves, Z_all, Z_lab, tag, prep, save=None):
        y, w = T.lab.y.to_numpy()[fit_rows], weights(T.lab.iloc[fit_rows])
        mods = modality_columns(prep)
        out = {}
        for name, kind in [('hgb_c1', 1), ('hgb_c5', 5), ('hgb_c8', 8), ('hgb_c32', 32), ('hgb_c32_etiq', 'etiq')]:
            m = fit_hgb(hgb_matrix(T, Z_all, Z_lab, fit_rows, kind), y, w, leaves)
            out[name] = m.predict_proba(hgb_matrix(T, Z_all, Z_lab, ev_rows, kind))[:, 1]
            if save: joblib.dump(m, save / f'{name}.joblib', compress=3)
            print(task, tag, name, flush=True)
        for c in [1, 32]:
            probs = []
            for mod, idx in mods.items():
                m = fit_hgb(hgb_matrix(T, Z_all, Z_lab, fit_rows, c, idx), y, w, leaves)
                probs.append(m.predict_proba(hgb_matrix(T, Z_all, Z_lab, ev_rows, c, idx))[:, 1])
                if save: joblib.dump(m, save / f'tardia_c{c}_{mod}.joblib', compress=3)
            out[f'tardia_c{c}'] = np.mean(probs, axis=0)
            print(task, tag, f'tardia_c{c}', flush=True)
        for c in [1, 32]:
            xf, lf = sequences(T, Z_all, fit_rows, c)
            xe, le = sequences(T, Z_all, ev_rows, c)
            probs = []
            for seed in GRU['seeds']:
                net = fit_gru(xf, lf, y, w, seed)
                probs.append(predict_gru(net, xe, le))
                if save: torch.save(net.state_dict(), save / f'gru_c{c}_s{seed}.pt')
            out[f'gru_c{c}'] = np.mean(probs, axis=0)
            print(task, tag, f'gru_c{c}', flush=True)
        return out

    if not final:
        for fold in folds:
            inner, iv = T.rows(fold['inner_fit']), T.rows(fold['inner_validation'])
            fit, ev = T.rows(fold['fit']), T.rows(fold['evaluation'])
            assert set(fold['fit']).isdisjoint(fold['evaluation'])
            _, Za, Zl = zfit(inner)
            local = []
            for c in [1, 8, 32]:
                for leaves in LEAVES:
                    m = fit_hgb(hgb_matrix(T, Za, Zl, inner, c), T.lab.y.to_numpy()[inner], weights(T.lab.iloc[inner]), leaves)
                    p = m.predict_proba(hgb_matrix(T, Za, Zl, iv, c))[:, 1]
                    auc = macro_auc(T.lab.iloc[iv], p)
                    local.append(dict(fold=fold['fold'], context=c, leaves=leaves, auc=auc))
            trials += local
            leaves = int(pd.DataFrame(local).groupby('leaves').auc.mean().sort_index().idxmax())
            sel.append(dict(fold=fold['fold'], leaves=leaves))
            prep, Za, Zl = zfit(fit)
            out = strategies(fit, ev, leaves, Za, Zl, f'fold{fold["fold"]}', prep)
            base = T.lab.iloc[ev][['source_row', 'participant', 'y']]
            for name, p in out.items():
                preds.append(base.assign(prob=p, strategy=name, fold=fold['fold'], split='oof_train', task=task))
            pd.concat(preds).to_csv(OUT / f'oof_{task}.csv.gz', index=False)
        pd.DataFrame(trials).to_csv(OUT / f'busqueda_interna_{task}.csv', index=False)
        pd.DataFrame(sel).to_csv(OUT / f'selecciones_{task}.csv', index=False)
        return
    # modelos finales: entrenados en todo train; predicción externa solo en evaluate()
    trials = pd.read_csv(OUT / f'busqueda_interna_{task}.csv')
    leaves = int(trials.groupby('leaves').auc.mean().sort_index().idxmax())
    fit = T.rows(train_people)
    prep, Za, Zl = zfit(fit)
    ev_rows = np.flatnonzero(T.lab.split.isin(external).to_numpy())
    assert set(T.lab.iloc[ev_rows].participant).isdisjoint(train_people)
    save = OUT / 'modelos' / task
    save.mkdir(exist_ok=True)
    out = strategies(fit, ev_rows, leaves, Za, Zl, 'final', prep, save=save)
    base = T.lab.iloc[ev_rows][['source_row', 'participant', 'y', 'split']]
    return leaves, pd.concat([base.assign(prob=p, strategy=n, task=task) for n, p in out.items()])


def macro_auc(f, p):
    p = np.asarray(p)
    return float(np.mean([roc_auc_score(f.y.iloc[ix], p[ix]) for ix in f.groupby('participant').indices.values()]))


def train(task):
    verify_inputs()
    assert not (OUT / f'oof_{task}.csv.gz').exists()
    torch.set_num_threads(3)
    run_task(task)
    write(OUT / f'oof_{task}_listo.json', dict(created_utc=pd.Timestamp.now(tz='UTC').isoformat(),
                                               sha256=digest(OUT / f'oof_{task}.csv.gz')))


def evaluate(task):
    """Entrena el modelo final en todo train y evalúa una sola vez en validación y test."""
    verify_inputs()
    assert (OUT / f'oof_{task}_listo.json').exists()
    dest = OUT / f'externas_{task}.csv.gz'
    assert not dest.exists(), 'validación/test ya evaluados para esta tarea'
    torch.set_num_threads(3)
    write(OUT / f'congelacion_previa_{task}.json', dict(
        created_utc=pd.Timestamp.now(tz='UTC').isoformat(), protocol_sha256=digest(OUT / 'protocolo.json'),
        search_sha256=digest(OUT / f'busqueda_interna_{task}.csv'), oof_sha256=digest(OUT / f'oof_{task}.csv.gz'),
        selections_sha256=digest(OUT / f'selecciones_{task}.csv'),
        note='Decisiones cerradas antes de mirar validación/test; el modelo final se entrena con todo train.'))
    leaves, pred = run_task(task, final=True, external=['validation', 'test'])
    pred.to_csv(dest, index=False)
    models = {str(p.relative_to(ROOT)): digest(p) for p in sorted((OUT / 'modelos' / task).iterdir())}
    write(OUT / f'congelacion_{task}.json', dict(created_utc=pd.Timestamp.now(tz='UTC').isoformat(), leaves=leaves,
                                                models=models, external_sha256=digest(dest)))


def person_metrics(pred):
    rows = []
    for (task, split, strat, person), g in pred.groupby(['task', 'split', 'strategy', 'participant']):
        yhat = (g.prob >= THRESHOLD).astype(int)
        rows.append(dict(task=task, split=split, strategy=strat, participant=person, windows=len(g),
                         auc=roc_auc_score(g.y, g.prob), ba=balanced_accuracy_score(g.y, yhat),
                         f1_macro=f1_score(g.y, yhat, average='macro', zero_division=0),
                         recall_alta=recall_score(g.y, yhat, pos_label=1, zero_division=0),
                         recall_baja=recall_score(g.y, yhat, pos_label=0, zero_division=0)))
    return pd.DataFrame(rows)


def report():
    parts = []
    for task in GROUPS:
        if (OUT / f'oof_{task}.csv.gz').exists():
            parts.append(pd.read_csv(OUT / f'oof_{task}.csv.gz'))
        if (OUT / f'externas_{task}.csv.gz').exists():
            parts.append(pd.read_csv(OUT / f'externas_{task}.csv.gz'))
    pred = pd.concat(parts, ignore_index=True)
    people = person_metrics(pred)
    people.to_csv(OUT / 'metricas_personas.csv', index=False)
    summ, contr = [], []
    for (task, split, strat), g in people.groupby(['task', 'split', 'strategy']):
        r = dict(task=task, split=split, strategy=strat, people=len(g))
        for m in ['auc', 'ba', 'f1_macro', 'recall_alta', 'recall_baja']:
            mean, lo, hi = ci(g[m])
            r.update({m: mean, f'{m}_low': lo, f'{m}_high': hi})
        summ.append(r)
    for (task, split), g in people.groupby(['task', 'split']):
        wide = g.pivot(index='participant', columns='strategy', values='auc')
        for name, a, b, role in CONTRASTS:
            if a in wide and b in wide:
                d = (wide[a] - wide[b]).dropna()
                mean, lo, hi = ci(d)
                contr.append(dict(task=task, split=split, contrast=name, role=role, delta=mean, low=lo, high=hi,
                                  improved=int((d > 0).sum()), people=len(d)))
    summ, contr = pd.DataFrame(summ), pd.DataFrame(contr)
    summ.to_csv(OUT / 'metricas.csv', index=False)
    contr.to_csv(OUT / 'contrastes.csv', index=False)
    coverage()
    print(summ[['task', 'split', 'strategy', 'auc', 'auc_low', 'auc_high', 'ba']].to_string(index=False))
    print(contr.to_string(index=False))


def coverage():
    data = load_data()
    rows = []
    for task in GROUPS:
        T = Task(data, task)
        for split in ['train', 'validation', 'test']:
            r = np.flatnonzero(T.lab.split.eq(split).to_numpy())
            pos = T.lab_pos[r]
            for name, (ix, l), idx in [('completo_c8', T.hist[8], pos), ('completo_c32', T.hist[32], pos),
                                       ('etiquetado_c32', T.hist_etiq, r)]:
                ctx = 8 if name.endswith('c8') else 32
                g = pd.DataFrame(dict(participant=T.lab.participant.iloc[r].to_numpy(), n=l[idx]))
                per = g.groupby('participant').n.agg(['mean', lambda s: (s == ctx).mean()])
                rows.append(dict(task=task, split=split, history=name, mean_windows=float(g.n.mean()),
                                 full_fraction=float((g.n == ctx).mean()), people=len(per)))
    pd.DataFrame(rows).to_csv(OUT / 'cobertura_historial.csv', index=False)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['prepare', 'train', 'evaluate', 'report'])
    ap.add_argument('--task', choices=list(GROUPS))
    a = ap.parse_args()
    with threadpool_limits(limits=3):
        if a.phase in ('train', 'evaluate'):
            globals()[a.phase](a.task)
        else:
            globals()[a.phase]()
