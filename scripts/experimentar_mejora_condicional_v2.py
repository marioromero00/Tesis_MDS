"""Compara señal fisiológica adicional frente al control por estímulo en v2."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from threadpoolctl import threadpool_limits

from baselines_estaticos import EEG, EYE, GSR, PUPIL
from predecir_pseudoetiquetas_pca_senales import modality_pca, pca_features

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "resultados/pca_senales_v2_24-10-2026"
OUT = ROOT / "resultados/mejora_condicional_v2_24-10-2026"
TASKS = {
    "attention": ("attention_label_teacher_pca", {"EEG": EEG, "GSR": GSR}, "eligible_attention"),
    "arousal": ("arousal_label_teacher_pca_6s", {"EEG": EEG, "Eye": EYE, "Pupil": PUPIL}, "eligible_arousal"),
}


def make_inputs(train: pd.DataFrame, other: pd.DataFrame, modalities: dict, kind: str,
                return_transforms: bool = False):
    if kind == "stimulus":
        pair = (train[["stimulus"]].copy(), other[["stimulus"]].copy())
        return (*pair, None) if return_transforms else pair
    transforms = None
    if kind == "raw":
        cols = sum(modalities.values(), [])
        imputer = SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True)
        a = imputer.fit_transform(train[cols])
        b = imputer.transform(other[cols])
    elif kind in {"pca", "pca_history", "pca_one"}:
        variance = 1 if kind == "pca_one" else 0.90
        transforms = {name: modality_pca(variance).fit(train[cols]) for name, cols in modalities.items()}
        a = pca_features(train, modalities, transforms)
        b = pca_features(other, modalities, transforms)
    else:
        raise ValueError(kind)
    names = [f"signal_{i}" for i in range(a.shape[1])]
    x_train = pd.DataFrame(a, columns=names, index=train.index)
    x_other = pd.DataFrame(b, columns=names, index=other.index)
    x_train.insert(0, "stimulus", train.stimulus)
    x_other.insert(0, "stimulus", other.stimulus)
    if kind == "pca_history":
        x_train = add_history(x_train, train)
        x_other = add_history(x_other, other)
    return (x_train, x_other, transforms) if return_transforms else (x_train, x_other)


def add_history(x: pd.DataFrame, frame: pd.DataFrame) -> pd.DataFrame:
    """Media causal t-5..t, reiniciada por grabación, segmento y huecos."""
    work = x.copy()
    work["_pos"] = np.arange(len(work))
    work["_time"] = pd.to_datetime(frame.window_start_utc, utc=True)
    for key in ["participant", "recording", "segment_id"]:
        work[key] = frame[key].to_numpy()
    keys = ["participant", "recording", "segment_id"]
    work = work.sort_values(keys + ["_time"])
    gap = work.groupby(keys)["_time"].diff().dt.total_seconds()
    work["_block"] = (gap.isna() | ~np.isclose(gap.fillna(1), 1.0, atol=1e-4, rtol=0)).groupby(
        [work[key] for key in keys]).cumsum()
    for col in [c for c in x if c != "stimulus"]:
        work[f"history6_{col}"] = work.groupby(keys + ["_block"])[col].transform(
            lambda series: series.rolling(6, min_periods=1).mean())
    return work.sort_values("_pos")[list(x) + [f"history6_{c}" for c in x if c != "stimulus"]].reset_index(drop=True)


def model_for(algorithm: str, x: pd.DataFrame):
    if algorithm == "logistic":
        numeric = [c for c in x if c != "stimulus"]
        encoder = ColumnTransformer([
            ("stimulus", OneHotEncoder(handle_unknown="ignore"), ["stimulus"]),
            ("signal", StandardScaler(), numeric),
        ])
        return Pipeline([("encoder", encoder), ("model", LogisticRegression(
            C=0.3, max_iter=2000, class_weight="balanced", random_state=20260822))])
    if algorithm == "catboost":
        return CatBoostClassifier(iterations=350, depth=5, learning_rate=0.05,
                                  loss_function="MultiClass", auto_class_weights="Balanced",
                                  verbose=False, thread_count=2, allow_writing_files=False,
                                  random_seed=20260822, l2_leaf_reg=5)
    raise ValueError(algorithm)


def score(frame: pd.DataFrame, pred: np.ndarray, target: str) -> dict:
    per_person = []
    for _, group in frame.assign(_pred=pred).groupby("participant"):
        per_person.append(balanced_accuracy_score(group[target], group._pred))
    return {"balanced_accuracy": float(balanced_accuracy_score(frame[target], pred)),
            "participant_macro_ba": float(np.mean(per_person))}


def run(one_pc_only: bool = False) -> None:
    OUT.mkdir(exist_ok=True)
    data = pd.read_csv(SOURCE / "dataset_pca_senales.csv")
    specs = [("stimulus", "logistic"), ("pca", "logistic"),
             ("stimulus", "catboost"), ("pca", "catboost"), ("raw", "catboost"),
             ("pca_history", "catboost")]
    if one_pc_only:
        specs = [("pca_one", "logistic"), ("pca_one", "catboost")]
    results, predictions = [], []
    for task, (target, modalities, eligible) in TASKS.items():
        frame = data.loc[data[eligible] & data.split.isin(["train", "validation"])
                         & data[target].notna()].copy()
        train = frame.loc[frame.split.eq("train")].reset_index(drop=True)
        val = frame.loc[frame.split.eq("validation")].reset_index(drop=True)
        for kind, algorithm in specs:
            x_train, x_val = make_inputs(train, val, modalities, kind)
            model = model_for(algorithm, x_train)
            fit_kwargs = {"cat_features": ["stimulus"]} if algorithm == "catboost" else {}
            model.fit(x_train, train[target], **fit_kwargs)
            pred = np.asarray(model.predict(x_val)).ravel()
            name = f"{kind}_{algorithm}"
            row = {"task": task, "model": name, "split": "validation", "rows": len(val),
                   "participants": val.participant.nunique(), **score(val, pred, target)}
            results.append(row)
            predictions.append(pd.DataFrame({"task": task, "model": name, "participant": val.participant,
                                             "stimulus": val.stimulus, "true": val[target], "predicted": pred}))
            print(json.dumps(row), flush=True)
    suffix = "_one_pc" if one_pc_only else ""
    pd.DataFrame(results).to_csv(OUT / f"metricas_validation{suffix}.csv", index=False)
    pd.concat(predictions, ignore_index=True).to_csv(OUT / f"predicciones_validation{suffix}.csv.gz",
                                                    compression="gzip", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--one-pc-only", action="store_true")
    args = parser.parse_args()
    with threadpool_limits(limits=2):
        run(args.one_pc_only)
