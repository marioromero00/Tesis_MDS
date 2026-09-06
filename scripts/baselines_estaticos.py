"""Entrena baselines estaticos con particion congelada por participante."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import shutil
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import balanced_accuracy_score, f1_score, mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]
EEG = ["eeg_rms_uv", "eeg_std_uv", "eeg_peak_to_peak_uv", "eeg_delta_relative",
       "eeg_theta_relative", "eeg_alpha_relative", "eeg_beta_relative",
       "eeg_gamma_relative", "eeg_line_noise_ratio"]
GSR = ["gsr_mean_z", "gsr_std_z", "gsr_min_z", "gsr_max_z", "gsr_tonic_mean_z",
       "gsr_phasic_mean_z", "gsr_slope_z_s", "gsr_scr_count", "gsr_scr_mean_prominence_z"]
PUPIL = ["pupil_both_valid_fraction", "pupil_mean_z", "pupil_std_z", "pupil_min_z",
         "pupil_max_z", "pupil_slope_z_s"]
EYE = ["gaze_dispersion_x_px", "gaze_dispersion_y_px", "gaze_dispersion_2d_px",
       "gaze_path_length_px", "fixation_count", "fixation_total_ms", "fixation_mean_ms",
       "fixation_median_ms", "saccade_count", "saccade_mean_ms"]


def regression_models(seed: int, trees: int):
    preprocessing = [("imputer", SimpleImputer(strategy="median", add_indicator=True)),
                     ("scale", StandardScaler())]
    return {
        "dummy_mean": Pipeline([("imputer", SimpleImputer(strategy="median")),
                                ("model", DummyRegressor(strategy="mean"))]),
        "ridge": Pipeline(preprocessing + [("model", Ridge(alpha=1.0))]),
        "random_forest": Pipeline([("imputer", SimpleImputer(strategy="median", add_indicator=True)),
                                   ("model", RandomForestRegressor(n_estimators=trees, min_samples_leaf=5,
                                                                   random_state=seed, n_jobs=1))]),
    }


def classification_models(seed: int, trees: int):
    preprocessing = [("imputer", SimpleImputer(strategy="median", add_indicator=True)),
                     ("scale", StandardScaler())]
    return {
        "dummy_prior": Pipeline([("imputer", SimpleImputer(strategy="median")),
                                 ("model", DummyClassifier(strategy="prior"))]),
        "logistic": Pipeline(preprocessing + [("model", LogisticRegression(max_iter=2000,
                                                                              class_weight="balanced",
                                                                              random_state=seed))]),
        "random_forest": Pipeline([("imputer", SimpleImputer(strategy="median", add_indicator=True)),
                                   ("model", RandomForestClassifier(n_estimators=trees, min_samples_leaf=5,
                                                                    class_weight="balanced", random_state=seed,
                                                                    n_jobs=1))]),
    }


def regression_metrics(y_true, y_pred) -> dict:
    return {"mae": mean_absolute_error(y_true, y_pred),
            "rmse": mean_squared_error(y_true, y_pred) ** 0.5,
            "r2": r2_score(y_true, y_pred)}


def classification_metrics(y_true, y_pred) -> dict:
    return {"balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
            "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0)}


def participant_macro(participants, y_true, y_pred, kind: str) -> dict:
    frame = pd.DataFrame({"participant": participants, "true": y_true, "pred": y_pred})
    rows = []
    for _, group in frame.groupby("participant"):
        rows.append(regression_metrics(group.true, group.pred) if kind == "regression"
                    else classification_metrics(group.true, group.pred))
    return {f"participant_macro_{key}": float(np.mean([row[key] for row in rows])) for key in rows[0]}


def validate_partition(data: pd.DataFrame, partition: pd.DataFrame) -> None:
    """Impide entrenar si el dataset difiere de la particion congelada."""
    allowed = {"train", "validation", "test", "sensitivity", "excluded"}
    if data[["participant", "split"]].isna().any().any():
        raise ValueError("Participante o split ausente en el dataset")
    if not set(data.split).issubset(allowed):
        raise ValueError("Split desconocido en el dataset")
    if data.groupby("participant").split.nunique().gt(1).any():
        raise ValueError("Un participante aparece en mas de un split")
    if partition.participant.duplicated().any():
        raise ValueError("Participante duplicado en la particion congelada")
    expected = data.participant.map(partition.set_index("participant").split)
    if expected.isna().any() or not expected.eq(data.split).all():
        raise ValueError("El dataset no coincide con la particion congelada")
    for name in ["train", "validation", "test"]:
        if not data.split.eq(name).any():
            raise ValueError(f"Split obligatorio vacio: {name}")


def save_pipeline(model, path: Path, verification: pd.DataFrame) -> dict:
    """Guarda el pipeline completo y verifica predicciones tras recargarlo."""
    path.parent.mkdir(parents=True, exist_ok=True)
    expected = model.predict(verification)
    joblib.dump(model, path, compress=3)
    restored = joblib.load(path)
    np.testing.assert_array_equal(expected, restored.predict(verification))
    if hasattr(model, "predict_proba"):
        np.testing.assert_array_equal(model.predict_proba(verification),
                                      restored.predict_proba(verification))
    return {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size, "reload_verified": True}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config/modelado.json")
    parser.add_argument("--run-dir", help="Directorio nuevo para conservar una ejecucion separada")
    args = parser.parse_args()
    config_path = (ROOT / args.config).resolve() if not Path(args.config).is_absolute() else Path(args.config)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    source_dir = (ROOT / config["output_dir"]).resolve()
    dataset_path = source_dir / "dataset_modelado.csv"
    partition_path = source_dir / "particion_participantes.csv"
    data = pd.read_csv(dataset_path)
    validate_partition(data, pd.read_csv(partition_path))
    output = source_dir
    if args.run_dir:
        output = (ROOT / args.run_dir).resolve()
        output.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(config_path, output / "config_entrenamiento.json")
    if output != source_dir:
        shutil.copyfile(partition_path, output / partition_path.name)
    artifacts = []
    started_at = datetime.now(timezone.utc).isoformat()
    seed = int(config["random_seed"])
    trees = int(config["baselines"]["random_forest_estimators"])
    tasks = {
        "attention_primary": {"score": "attention_score_equal", "label": "attention_label_equal", "features": EEG + GSR},
        "attention_pca_sensitivity": {"score": "attention_score_pca", "label": "attention_label_pca", "features": EEG + GSR},
        "arousal_primary_6s": {"score": "arousal_score_6s", "label": "arousal_label_6s", "features": EEG + EYE + PUPIL},
        "arousal_2s_sensitivity": {"score": "arousal_score_2s", "label": "arousal_label_2s", "features": EEG + EYE + PUPIL},
        "arousal_pca_sensitivity": {"score": "arousal_score_pca", "label": "arousal_label_pca", "features": EEG + EYE + PUPIL},
    }
    metrics_rows, prediction_rows, importance_rows = [], [], []
    train = data[data.split.eq("train")]
    for task_name, task in tasks.items():
        columns = task["features"]
        train_valid = train[train[task["score"]].notna() & train[task["label"]].notna()]
        for kind, target, models in [
            ("regression", task["score"], regression_models(seed, trees)),
            ("classification", task["label"], classification_models(seed, trees)),
        ]:
            x_train, y_train = train_valid[columns], train_valid[target]
            if train_valid.empty:
                raise ValueError(f"Sin datos de entrenamiento para {task_name}")
            for model_name, model in models.items():
                print(f"{task_name} | {kind} | {model_name}", flush=True)
                model.fit(x_train, y_train)
                model_path = output / "modelos" / task_name / f"{kind}__{model_name}.joblib"
                verification = data.loc[data.split.isin(["validation", "test", "sensitivity"])
                                        & data[target].notna(), columns]
                artifact = save_pipeline(model, model_path, verification)
                artifact.update({"path": model_path.relative_to(output).as_posix(),
                                 "task": task_name, "kind": kind, "model": model_name,
                                 "target": target, "features": columns,
                                 "train_rows": len(train_valid),
                                 "train_participants": sorted(train_valid.participant.unique().tolist()),
                                 "estimator_params": model.named_steps["model"].get_params(),
                                 "classes": model.classes_.tolist() if hasattr(model, "classes_") else None})
                model_path.with_suffix(".json").write_text(
                    json.dumps(artifact, indent=2, ensure_ascii=False), encoding="utf-8")
                artifacts.append(artifact)
                for split_name in ["validation", "test", "sensitivity"]:
                    evaluation = data[data.split.eq(split_name) & data[target].notna()]
                    if evaluation.empty:
                        continue
                    predicted = model.predict(evaluation[columns])
                    scores = regression_metrics(evaluation[target], predicted) if kind == "regression" else classification_metrics(evaluation[target], predicted)
                    scores.update(participant_macro(evaluation.participant.to_numpy(), evaluation[target].to_numpy(), predicted, kind))
                    metrics_rows.append({"task": task_name, "kind": kind, "model": model_name,
                                         "split": split_name, "rows": len(evaluation),
                                         "participants": evaluation.participant.nunique(), **scores})
                    for identity, actual, estimate in zip(evaluation[["participant", "window_start_utc"]].itertuples(index=False), evaluation[target], predicted):
                        prediction_rows.append({"task": task_name, "kind": kind, "model": model_name,
                                                "split": split_name, "participant": identity.participant,
                                                "window_start_utc": identity.window_start_utc,
                                                "actual": actual, "predicted": estimate})
                fitted = model.named_steps.get("model")
                transformed_columns = model[:-1].get_feature_names_out(columns)
                if hasattr(fitted, "feature_importances_"):
                    for feature, importance in zip(transformed_columns, fitted.feature_importances_):
                        importance_rows.append({"task": task_name, "kind": kind, "model": model_name,
                                                "feature": feature, "importance": importance})
                elif hasattr(fitted, "coef_"):
                    coefs = np.mean(np.abs(np.atleast_2d(fitted.coef_)), axis=0)
                    for feature, importance in zip(transformed_columns, coefs):
                        importance_rows.append({"task": task_name, "kind": kind, "model": model_name,
                                                "feature": feature, "importance": importance})
    metrics = pd.DataFrame(metrics_rows)
    metrics.to_csv(output / "metricas_baselines.csv", index=False, float_format="%.8g")
    pd.DataFrame(prediction_rows).to_csv(output / "predicciones_baselines.csv", index=False, float_format="%.8g")
    pd.DataFrame(importance_rows).to_csv(output / "importancia_features.csv", index=False, float_format="%.8g")
    manifest = {
        "config_sha256": hashlib.sha256(config_path.read_bytes()).hexdigest(),
        "pipeline_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "requirements_sha256": hashlib.sha256((ROOT / "requirements.txt").read_bytes()).hexdigest(),
        "dataset_sha256": hashlib.sha256(dataset_path.read_bytes()).hexdigest(),
        "partition_sha256": hashlib.sha256(partition_path.read_bytes()).hexdigest(),
        "dataset_path": str(dataset_path),
        "started_at_utc": started_at, "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "versions": {"python": platform.python_version(), "numpy": np.__version__,
                     "pandas": pd.__version__, "scikit-learn": sklearn.__version__,
                     "joblib": joblib.__version__},
        "artifacts": artifacts,
        "sklearn_version": sklearn.__version__, "random_seed": seed,
        "tasks": tasks, "models": ["dummy", "linear", "random_forest"],
        "fit_scope": "train participants only", "parallelism": "disabled (n_jobs=1)",
        "metrics_rows": len(metrics),
    }
    (output / "manifiesto_baselines.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(metrics[metrics.split.eq("test")].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
