"""Contraste de subconjuntos mediante cinco folds disjuntos dentro de train.

El protocolo se escribe antes de ajustar. No se usa validation/test para elegir.
Las hipotesis provienen del analisis exploratorio previo; esto no es confirmacion externa.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import GroupKFold
from sklearn.metrics import balanced_accuracy_score, r2_score, mean_squared_error, f1_score

from baselines_estaticos import ROOT, EEG, GSR, EYE, PUPIL, classification_models, regression_models, validate_partition
from analisis_variables import subject_scores, bootstrap_mean

SEED = 20260907
TASKS = {'attention_primary': ('attention_score_equal', 'attention_label_equal'),
         'arousal_primary_6s': ('arousal_score_6s', 'arousal_label_6s')}
# Preferencia explicita, no ranking supervisado: una amplitud y GSR tonico primero.
PRIORITY = ['eeg_rms_uv', 'eeg_alpha_relative', 'eeg_theta_relative', 'eeg_beta_relative',
            'eeg_gamma_relative', 'eeg_delta_relative', 'eeg_std_uv', 'eeg_peak_to_peak_uv',
            'gsr_tonic_mean_z', 'gsr_phasic_mean_z', 'gsr_slope_z_s', 'gsr_std_z',
            'gsr_scr_count', 'gsr_scr_mean_prominence_z', 'gsr_mean_z', 'gsr_min_z', 'gsr_max_z']


def compact_columns(train, threshold=.9):
    corr = train[PRIORITY].corr(method='spearman').abs()
    selected, removed = [], []
    for column in PRIORITY:
        if train[column].nunique() < 2:
            removed.append({'feature': column, 'reason': 'constant_or_missing'})
            continue
        redundant = next((f for f in selected if corr.loc[column, f] >= threshold), None)
        if redundant:
            removed.append({'feature': column, 'reason': 'correlation', 'representative': redundant,
                            'abs_spearman': float(corr.loc[column, redundant])})
        else:
            selected.append(column)
    if not selected:
        raise ValueError('Seleccion compacta vacia')
    return selected, removed


def candidates(task, train):
    if task == 'attention_primary':
        compact, removed = compact_columns(train)
        return {'full': EEG + GSR, 'EEG': EEG, 'compact_no_noise': compact}, removed
    clean_pupil = [f for f in PUPIL if f != 'pupil_both_valid_fraction']
    return {'full': EEG + EYE + PUPIL, 'Pupil': PUPIL, 'Eye_Pupil': EYE + PUPIL,
            'Pupil_no_quality': clean_pupil, 'Eye_Pupil_no_quality': EYE + clean_pupil}, []


def folds_for_train(train):
    if not train.split.eq('train').all():
        raise ValueError('La validacion interna admite exclusivamente train')
    splitter = GroupKFold(n_splits=5, shuffle=True, random_state=SEED)
    return list(splitter.split(train, groups=train.participant))


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def metrics(frame, pred, target, kind):
    ss = subject_scores(frame, pred, target, kind)
    result = {'macro_score': float(ss.mean())}
    if kind == 'classification':
        result.update(balanced_accuracy=balanced_accuracy_score(frame[target], pred),
                      macro_f1=f1_score(frame[target], pred, average='macro', zero_division=0))
    else:
        result.update(r2=r2_score(frame[target], pred), mse=mean_squared_error(frame[target], pred))
    return result, ss


def summarize_subjects(subjects):
    summaries = []
    for (task, kind, model, subset), group in subjects.groupby(['task', 'kind', 'model', 'subset']):
        base = subjects.loc[subjects.task.eq(task) & subjects.kind.eq(kind)]
        full = base.loc[base.model.eq(model) & base.subset.eq('full')].set_index('participant').score
        dummy = base.loc[base.model.eq('dummy')].set_index('participant').score
        ordered = group.set_index('participant').sort_index()
        row = dict(task=task, kind=kind, model=model, subset=subset, n_participants=len(group),
                   mean_score=float(group.score.mean()), sd_participants=float(group.score.std(ddof=1)),
                   mean_features=float(group.n_features.mean()))
        for label, reference in [('full', full), ('dummy', dummy)]:
            if reference.empty:
                continue
            delta = ordered.score - reference.reindex(ordered.index)
            if delta.isna().any():
                raise ValueError('Comparacion sin participante pareado')
            lo, hi = bootstrap_mean(delta.to_numpy())
            row.update({f'delta_{label}': float(delta.mean()), f'low_{label}': lo, f'high_{label}': hi,
                        f'positive_{label}': int((delta > 0).sum())})
        summaries.append(row)
    return pd.DataFrame(summaries)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='resultados/estabilidad_variables_07-09-2026')
    parser.add_argument('--jobs', type=int, default=4)
    args = parser.parse_args()
    output = ROOT / args.output
    output.mkdir(parents=True, exist_ok=False)
    dataset = ROOT / 'resultados/modelado/dataset_modelado.csv'
    partition = ROOT / 'resultados/modelado/particion_participantes.csv'
    source = ROOT / 'resultados/modelado/ejecuciones/baselines_05-09-2026_02/manifiesto_baselines.json'
    original = json.loads(source.read_text(encoding='utf-8'))
    assert digest(dataset) == original['dataset_sha256'] and digest(partition) == original['partition_sha256']
    data = pd.read_csv(dataset)
    validate_partition(data, pd.read_csv(partition))
    train = data.loc[data.split.eq('train')].reset_index(drop=True)
    # Guardar identidades de validation, sin calcular metricas hasta cerrar CV.
    validation = data.loc[data.split.eq('validation')].reset_index(drop=True)
    del data
    folds = folds_for_train(train)
    fold_manifest = [{'fold': i, 'fit': sorted(train.iloc[a].participant.unique()),
                      'evaluation': sorted(train.iloc[b].participant.unique()),
                      'fit_rows': len(a), 'evaluation_rows': len(b)} for i, (a, b) in enumerate(folds)]
    protocol = dict(created_utc=datetime.now(timezone.utc).isoformat(), random_seed=SEED,
        rf_seed=20260822, n_estimators=200, n_jobs=args.jobs, folds=fold_manifest,
        dataset_sha256=digest(dataset), partition_sha256=digest(partition),
        script_sha256=digest(Path(__file__)), compact_priority=PRIORITY, threshold=.9,
        selection_rule='Descriptive paired comparisons to full and dummy; no automatic best-model claim',
        candidate_policy='freeze comparison panels, not universal winner; test never evaluated',
        preprocessing='median imputation + missing indicators in fold; scaler for linear; inherited offline normalization',
        interval='2000 participant bootstrap resamples of paired OOF scores; descriptive, overlapping fit sets',
        caveat='Candidate hypotheses were informed by previous train/validation analysis; not independent confirmation',
        versions={'python': platform.python_version(), 'numpy': np.__version__, 'pandas': pd.__version__,
                  'scikit-learn': sklearn.__version__, 'joblib': joblib.__version__})
    write_json(output / 'protocolo.json', protocol)
    rows, subjects, predictions, selections = [], [], [], []
    for fold, (fit_ix, eval_ix) in enumerate(folds):
        fit_frame, eval_frame = train.iloc[fit_ix], train.iloc[eval_ix]
        assert set(fit_frame.participant).isdisjoint(eval_frame.participant)
        for task, (score_target, label_target) in TASKS.items():
            fitting = fit_frame.loc[fit_frame[score_target].notna() & fit_frame[label_target].notna()]
            evaluation = eval_frame.loc[eval_frame[score_target].notna() & eval_frame[label_target].notna()].reset_index(drop=True)
            sets, removed = candidates(task, fitting)
            selections.append(dict(fold=fold, task=task, subsets=sets, removed=removed))
            for kind, target, factory in [('classification', label_target, classification_models),
                                          ('regression', score_target, regression_models)]:
                for name, model in factory(20260822, 200).items():
                    is_dummy = name.startswith('dummy')
                    model_name = 'dummy' if is_dummy else name
                    if name == 'random_forest':
                        model.set_params(model__n_jobs=args.jobs)
                    for subset, columns in ({'full': sets['full']} if is_dummy else sets).items():
                        print(f'fold {fold+1}/5 | {task} {kind} {model_name} {subset} ({len(columns)})', flush=True)
                        model.fit(fitting[columns], fitting[target])
                        predicted = model.predict(evaluation[columns])
                        scores, ss = metrics(evaluation, predicted, target, kind)
                        identity = dict(fold=fold, task=task, kind=kind, model=model_name, subset=subset, n_features=len(columns))
                        rows.append({**identity, **scores, 'rows': len(evaluation)})
                        for person, value in zip(sorted(evaluation.participant.unique()), ss):
                            subjects.append({**identity, 'participant': person, 'score': float(value)})
                        for i, value in enumerate(predicted):
                            predictions.append({**identity, 'participant': evaluation.iloc[i].participant,
                                'window_start_utc': evaluation.iloc[i].window_start_utc,
                                'actual': evaluation.iloc[i][target], 'predicted': value})
        pd.DataFrame(rows).to_csv(output / 'metricas_folds.csv', index=False)
        pd.DataFrame(subjects).to_csv(output / 'metricas_participantes_oof.csv', index=False)
        write_json(output / 'seleccion_por_fold.json', selections)
    oof = pd.DataFrame(subjects)
    summary = summarize_subjects(oof)
    summary.to_csv(output / 'resumen_cv.csv', index=False)
    pd.DataFrame(predictions).to_csv(output / 'predicciones_oof.csv.gz', index=False, compression='gzip')
    # Congelar columnas y resultados internos ANTES de abrir metricas de validation.
    frozen = {task: candidates(task, train)[0] for task in TASKS}
    write_json(output / 'conjuntos_congelados.json', dict(
        frozen_utc=datetime.now(timezone.utc).isoformat(), status='panel comparativo, no ganador confirmado',
        targets=TASKS, features=frozen, cv_summary_sha256=digest(output / 'resumen_cv.csv'),
        rationale='Preservar controles completos y contrastes de modalidad/calidad; compactacion ajustada en train completo'))
    artifact_dir = output / 'modelos_finales'
    artifact_dir.mkdir()
    final_rows, artifacts = [], []
    for task, (score_target, label_target) in TASKS.items():
        fitting = train.loc[train[score_target].notna() & train[label_target].notna()]
        evaluation = validation.loc[validation[score_target].notna() & validation[label_target].notna()].reset_index(drop=True)
        for kind, target, factory in [('classification', label_target, classification_models),
                                      ('regression', score_target, regression_models)]:
            for name, model in factory(20260822, 200).items():
                is_dummy = name.startswith('dummy')
                for subset, columns in ({'full': frozen[task]['full']} if is_dummy else frozen[task]).items():
                    print(f'final | {task} {kind} {name} {subset}', flush=True)
                    if name == 'random_forest':
                        model.set_params(model__n_jobs=args.jobs)
                    model.fit(fitting[columns], fitting[target])
                    # Serializar prediccion determinista para comprobacion exacta.
                    if name == 'random_forest':
                        model.set_params(model__n_jobs=1)
                    predicted = model.predict(evaluation[columns])
                    path = artifact_dir / f'{task}__{kind}__{name}__{subset}.joblib'
                    joblib.dump(model, path, compress=3)
                    restored = joblib.load(path)
                    np.testing.assert_array_equal(predicted, restored.predict(evaluation[columns]))
                    if hasattr(model, 'predict_proba'):
                        np.testing.assert_array_equal(model.predict_proba(evaluation[columns]), restored.predict_proba(evaluation[columns]))
                    artifact = dict(task=task, kind=kind, model=name, subset=subset, features=columns,
                        target=target, train_participants=sorted(fitting.participant.unique()),
                        path=path.relative_to(output).as_posix(), sha256=digest(path), reload_verified=True)
                    artifacts.append(artifact)
                    scores, _ = metrics(evaluation, predicted, target, kind)
                    final_rows.append(dict(task=task, kind=kind, model=name, subset=subset,
                                           n_features=len(columns), **scores))
    pd.DataFrame(final_rows).to_csv(output / 'validacion_panel_congelado.csv', index=False)
    write_json(output / 'manifiesto.json', dict(completed_utc=datetime.now(timezone.utc).isoformat(),
        protocol_sha256=digest(output / 'protocolo.json'), test_evaluated=False,
        fold_models=len(rows), final_models=artifacts,
        cv_participants=sorted(train.participant.unique()), validation_participants=sorted(validation.participant.unique())))
    print('COMPLETADO', flush=True)


if __name__ == '__main__':
    main()
