"""Compara fusión temprana, intermedia y tardía con protocolo fijo por participante."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from threadpoolctl import threadpool_limits

from baselines_estaticos import EEG, GSR, EYE, PUPIL
from comparar_pseudoetiquetas import temporal_features

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "resultados/estudio_pseudoetiquetas_24-10-2026/dataset_sensibilidad.csv"
OUT = ROOT / "resultados/fusion_pseudoetiquetas_24-10-2026"
CLASSES = np.asarray(["bajo", "medio", "alto"])
TASKS = {
    "attention_audited": ("attention_label_equal", {"EEG": EEG, "GSR": GSR}),
    "attention_eye_only": ("attention_label_eye_only", {"EEG": EEG, "GSR": GSR}),
    "arousal_audited": ("arousal_label_6s", {"EEG": EEG, "Eye": EYE, "Pupil": PUPIL}),
    "arousal_gsr_continuous": ("arousal_label_gsr_continuous_6s", {"EEG": EEG, "Eye": EYE, "Pupil": PUPIL}),
}


def classifier() -> Pipeline:
    return Pipeline([
        ("imputer", SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True)),
        ("scale", StandardScaler()),
        ("model", LogisticRegression(max_iter=2000, class_weight="balanced", random_state=20260822)),
    ])


def align_proba(model: Pipeline, values: pd.DataFrame | np.ndarray) -> np.ndarray:
    raw = model.predict_proba(values)
    return raw[:, [list(model.classes_).index(c) for c in CLASSES]]


def geometric_mean(probabilities: list[np.ndarray]) -> np.ndarray:
    logs = np.mean(np.log(np.clip(np.stack(probabilities), 1e-12, 1.0)), axis=0)
    shifted = np.exp(logs - logs.max(axis=1, keepdims=True))
    return shifted / shifted.sum(axis=1, keepdims=True)


def metric_rows(frame: pd.DataFrame, prediction: np.ndarray) -> tuple[dict, list[dict]]:
    actual = frame["_target"].to_numpy()
    participant_rows = []
    for participant, positions in frame.groupby("participant").indices.items():
        y, pred = actual[positions], prediction[positions]
        observed = np.unique(y)
        participant_rows.append({"participant": participant, "rows": len(y),
                                 "observed_classes": len(observed),
                                 "balanced_accuracy": float(np.mean([(pred[y == c] == c).mean() for c in observed]))})
    summary = {"rows": len(frame), "participants": len(participant_rows),
               "balanced_accuracy": float(balanced_accuracy_score(actual, prediction)),
               "macro_f1": float(f1_score(actual, prediction, average="macro", zero_division=0)),
               "participant_macro_ba": float(np.mean([r["balanced_accuracy"] for r in participant_rows]))}
    return summary, participant_rows


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(SOURCE)
    frame = data.loc[data.eligible_attention & data.split.isin(["train", "validation", "test"])].copy().reset_index(drop=True)
    all_columns = list(dict.fromkeys(EEG + GSR + EYE + PUPIL))
    history = temporal_features(frame, all_columns)
    history.columns = [f"history6_{c}" for c in all_columns]
    for col in history:
        frame[col] = history[col].to_numpy()
    protocol = {
        "dataset_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "train_participants": sorted(frame.loc[frame.split.eq("train"), "participant"].unique().tolist()),
        "validation_participants": sorted(frame.loc[frame.split.eq("validation"), "participant"].unique().tolist()),
        "test_participants": sorted(frame.loc[frame.split.eq("test"), "participant"].unique().tolist()),
        "contexts": {"current": "2 s current window", "history6": "current plus mean of six 2 s windows, maximum support 7 s"},
        "strategies": {
            "early": "Concatenate all allowed modality features, one logistic pipeline",
            "intermediate_pca90": "Per-modality imputer, scaler and unsupervised PCA retaining 90% train variance; concatenate embeddings, logistic classifier",
            "late_mean": "Separate logistic pipeline per modality; arithmetic mean of class probabilities",
            "late_geometric": "Separate logistic pipeline per modality; normalized geometric mean of class probabilities",
            "unimodal": "Separate logistic pipeline for each allowed modality",
        },
        "selection": "No model, weight, PCA threshold or context selected from validation or test metrics",
        "evaluation": "Same eligible rows and frozen participant split for all strategies; exploratory because test was previously inspected",
    }
    (OUT / "protocolo.json").write_text(json.dumps(protocol, indent=2, ensure_ascii=False), encoding="utf-8")
    metrics, people, predictions = [], [], []
    for task, (target, modalities) in TASKS.items():
        work = frame.loc[frame[target].notna()].copy().reset_index(drop=True)
        work["_target"] = work[target]
        train = work.split.eq("train")
        for context in ["current", "history6"]:
            panels = {name: columns if context == "current" else columns + [f"history6_{c}" for c in columns]
                      for name, columns in modalities.items()}
            if task.startswith("attention"):
                assert not set(sum(panels.values(), [])).intersection(EYE + PUPIL)
            else:
                assert not set(sum(panels.values(), [])).intersection(GSR)
            combined = sum(panels.values(), [])
            early = classifier().fit(work.loc[train, combined], work.loc[train, target])
            experts = {name: classifier().fit(work.loc[train, columns], work.loc[train, target])
                       for name, columns in panels.items()}
            transforms = {}
            for name, columns in panels.items():
                transformer = Pipeline([
                    ("imputer", SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True)),
                    ("scale", StandardScaler()),
                    ("pca", PCA(n_components=0.90, svd_solver="full")),
                ]).fit(work.loc[train, columns])
                transforms[name] = transformer
            embedded_train = np.column_stack([transforms[name].transform(work.loc[train, columns])
                                              for name, columns in panels.items()])
            intermediate = LogisticRegression(max_iter=2000, class_weight="balanced", random_state=20260822)
            intermediate.fit(embedded_train, work.loc[train, target])
            for split in ["validation", "test"]:
                part = work.loc[work.split.eq(split)].copy().reset_index(drop=True)
                modality_proba = {name: align_proba(experts[name], part[columns]) for name, columns in panels.items()}
                embedding = np.column_stack([transforms[name].transform(part[columns])
                                             for name, columns in panels.items()])
                embedded_proba = intermediate.predict_proba(embedding)[:,
                    [list(intermediate.classes_).index(c) for c in CLASSES]]
                probabilities = {
                    "early": align_proba(early, part[combined]),
                    "intermediate_pca90": embedded_proba,
                    "late_mean": np.mean(np.stack(list(modality_proba.values())), axis=0),
                    "late_geometric": geometric_mean(list(modality_proba.values())),
                    **{f"unimodal_{name}": value for name, value in modality_proba.items()},
                }
                for strategy, proba in probabilities.items():
                    pred = CLASSES[proba.argmax(axis=1)]
                    ident = {"task": task, "context": context, "strategy": strategy, "split": split}
                    summary, participant_rows = metric_rows(part, pred)
                    metrics.append({**ident, **summary})
                    people.extend({**ident, **row} for row in participant_rows)
                    for i, row in part[["participant", "window_start_utc"]].reset_index(drop=True).iterrows():
                        predictions.append({**ident, "participant": row.participant, "window_start_utc": row.window_start_utc,
                                            "true": part.iloc[i][target], "predicted": pred[i]})
            print(task, context, "completo", flush=True)
    pd.DataFrame(metrics).to_csv(OUT / "metricas_fusion.csv", index=False)
    pd.DataFrame(people).to_csv(OUT / "metricas_participantes.csv", index=False)
    pd.DataFrame(predictions).to_csv(OUT / "predicciones.csv.gz", index=False, compression="gzip")
    print(pd.DataFrame(metrics).loc[lambda x:x.split.eq("test")].to_string(index=False))


if __name__ == "__main__":
    with threadpool_limits(limits=2):
        main()
