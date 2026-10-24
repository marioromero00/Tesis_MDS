"""Predice las nuevas etiquetas comparando entradas completas con PCA por modalidad."""
from __future__ import annotations

import hashlib
import json
import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from threadpoolctl import threadpool_limits

from baselines_estaticos import EEG, GSR, EYE, PUPIL

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/pca_senales_v2.json"
CLASSES = np.asarray(["bajo", "medio", "alto"])
TASKS = {
    "attention": ("attention_label_teacher_pca", {"EEG": EEG, "GSR": GSR}, "eligible_attention"),
    "arousal": ("arousal_label_teacher_pca_6s", {"EEG": EEG, "Eye": EYE, "Pupil": PUPIL}, "eligible_arousal"),
}


def full_pipeline() -> Pipeline:
    return Pipeline([
        ("imputer", SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True)),
        ("scale", StandardScaler()),
        ("model", LogisticRegression(max_iter=2000, class_weight="balanced", random_state=20260822)),
    ])


def modality_pca(variance: float | int) -> Pipeline:
    return Pipeline([
        ("imputer", SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True)),
        ("scale", StandardScaler()),
        ("pca", PCA(n_components=variance, svd_solver="full")),
    ])


def score(frame: pd.DataFrame, pred: np.ndarray) -> dict:
    actual = frame["_target"].to_numpy()
    per_person = []
    for _, positions in frame.groupby("participant").indices.items():
        y, yhat = actual[positions], pred[positions]
        per_person.append(np.mean([(yhat[y == c] == c).mean() for c in np.unique(y)]))
    return {"rows": len(frame), "participants": frame.participant.nunique(),
            "balanced_accuracy": float(balanced_accuracy_score(actual, pred)),
            "macro_f1": float(f1_score(actual, pred, average="macro", zero_division=0)),
            "participant_macro_ba": float(np.mean(per_person))}


def pca_features(frame: pd.DataFrame, modalities: dict[str, list[str]], transforms: dict) -> np.ndarray:
    return np.column_stack([transforms[name].transform(frame[columns]) for name, columns in modalities.items()])


def predict_saved(bundle: dict, frame: pd.DataFrame) -> np.ndarray:
    if bundle["kind"] == "pca":
        values = pca_features(frame, bundle["modalities"], bundle["transforms"])
    else:
        values = frame[bundle["features"]]
    return bundle["model"].predict(values)


def main(config_path: Path = CONFIG) -> None:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    output = ROOT / config["output_dir"]
    data_path = output / "dataset_pca_senales.csv"
    teacher = json.loads((output / "manifiesto_profesor.json").read_text(encoding="utf-8"))
    if teacher["dataset_sha256"] != hashlib.sha256(data_path.read_bytes()).hexdigest():
        raise ValueError("Dataset y manifiesto del profesor no coinciden")
    models_dir = output / "student_models"
    models_dir.mkdir(exist_ok=True)
    data = pd.read_csv(data_path)
    results, predictions, models_meta = [], [], {}
    for task, (target, modalities, eligible) in TASKS.items():
        frame = data.loc[data[eligible] & data.split.isin(["train", "validation", "test"])
                         & data[target].notna()].copy().reset_index(drop=True)
        frame["_target"] = frame[target]
        train = frame.split.eq("train")
        features = sum(modalities.values(), [])
        if task == "attention":
            assert not set(features).intersection(EYE + PUPIL)
        else:
            assert not set(features).intersection(GSR)
        fitted = {}
        dummy = DummyClassifier(strategy="prior").fit(frame.loc[train, features], frame.loc[train, target])
        fitted["dummy"] = {"kind": "full", "features": features, "model": dummy}
        full = full_pipeline().fit(frame.loc[train, features], frame.loc[train, target])
        fitted["full_logistic"] = {"kind": "full", "features": features, "model": full}
        transforms = {name: modality_pca(config["student"]["variance_retained_per_modality"]).fit(
            frame.loc[train, columns]) for name, columns in modalities.items()}
        x_train = pca_features(frame.loc[train], modalities, transforms)
        reduced = LogisticRegression(max_iter=2000, class_weight="balanced", random_state=20260822)
        reduced.fit(x_train, frame.loc[train, target])
        fitted["pca_logistic"] = {"kind": "pca", "modalities": modalities,
                                  "transforms": transforms, "model": reduced}
        transforms_one = {name: modality_pca(1).fit(frame.loc[train, columns])
                          for name, columns in modalities.items()}
        one = LogisticRegression(max_iter=2000, class_weight="balanced", random_state=20260822)
        one.fit(pca_features(frame.loc[train], modalities, transforms_one), frame.loc[train, target])
        fitted["pca_1pc_logistic"] = {"kind": "pca", "modalities": modalities,
                                      "transforms": transforms_one, "model": one}
        models_meta[task] = {"target": target, "raw_features": len(features), "retained_components": {},
                             "one_pc_variance": {}, "models": {}}
        for name, pipeline in transforms.items():
            pca = pipeline.named_steps["pca"]
            models_meta[task]["retained_components"][name] = {
                "raw_features": len(modalities[name]),
                "transformed_input_dimension": int(pca.n_features_in_),
                "components": int(pca.n_components_),
                "variance_retained": float(pca.explained_variance_ratio_.sum()),
            }
            models_meta[task]["one_pc_variance"][name] = float(
                transforms_one[name].named_steps["pca"].explained_variance_ratio_[0])
        for model_name, bundle in fitted.items():
            model_path = models_dir / f"{task}__{model_name}.joblib"
            joblib.dump(bundle, model_path, compress=3)
            restored = joblib.load(model_path)
            models_meta[task]["models"][model_name] = {
                "path": model_path.relative_to(output).as_posix(),
                "sha256": hashlib.sha256(model_path.read_bytes()).hexdigest(),
                "reload_verified": True,
            }
            for split in ["validation", "test"]:
                part = frame.loc[frame.split.eq(split)].copy().reset_index(drop=True)
                pred = predict_saved(bundle, part)
                np.testing.assert_array_equal(pred, predict_saved(restored, part))
                results.append({"task": task, "model": model_name, "split": split, **score(part, pred)})
                predictions.append(pd.DataFrame({"task": task, "model": model_name, "split": split,
                                                 "participant": part.participant,
                                                 "window_start_utc": part.window_start_utc,
                                                 "true": part[target], "predicted": pred}))
            print(task, model_name, "completo", flush=True)
    pd.DataFrame(results).to_csv(output / "metricas_estudiante.csv", index=False)
    pd.concat(predictions, ignore_index=True).to_csv(output / "predicciones_estudiante.csv.gz", index=False, compression="gzip")
    manifest = {"config_sha256": hashlib.sha256(config_path.read_bytes()).hexdigest(),
                "dataset_sha256": hashlib.sha256(data_path.read_bytes()).hexdigest(),
                "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "models": models_meta,
                "comparison": "PCA versus variables completas sobre las mismas pseudoetiquetas nuevas; mismo train/validation/test",
                "test_scope": "Exploratorio: test ya se había inspeccionado en estudios anteriores"}
    (output / "manifiesto_estudiante.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(pd.DataFrame(results).to_string(index=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(CONFIG))
    args = parser.parse_args()
    with threadpool_limits(limits=2):
        main(Path(args.config).resolve())
