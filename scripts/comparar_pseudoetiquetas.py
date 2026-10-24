"""Comparación fija: Dummy, logística actual y logística con seis ventanas de historial."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from baselines_estaticos import EEG, GSR, EYE, PUPIL

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "resultados/estudio_pseudoetiquetas_24-10-2026/dataset_sensibilidad.csv"
OUT = DATA.parent
TASKS = {
    "attention_audited": ("attention_label_equal", EEG + GSR),
    "attention_eye_only": ("attention_label_eye_only", EEG + GSR),
    "arousal_audited": ("arousal_label_6s", EEG + EYE + PUPIL),
    "arousal_gsr_continuous": ("arousal_label_gsr_continuous_6s", EEG + EYE + PUPIL),
}


def temporal_features(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Promedio causal t-5..t; reinicia en grabación, segmento y saltos distintos de 1 s."""
    work = frame.copy()
    work["_position"] = np.arange(len(work))
    work["_time"] = pd.to_datetime(work.window_start_utc, utc=True)
    keys = ["participant", "recording", "segment_id"]
    work = work.sort_values(keys + ["_time"])
    gap = work.groupby(keys)["_time"].diff().dt.total_seconds()
    work["_block"] = (gap.isna() | ~np.isclose(gap.fillna(1), 1.0, atol=1e-4, rtol=0)).groupby(
        [work[k] for k in keys]).cumsum()
    for col in columns:
        work[f"history6_{col}"] = work.groupby(keys + ["_block"])[col].transform(
            lambda s: s.rolling(6, min_periods=1).mean())
    return work.sort_values("_position")[[f"history6_{col}" for col in columns]].reset_index(drop=True)


def metrics(frame: pd.DataFrame, prediction: np.ndarray) -> dict:
    actual = frame["_target"].to_numpy()
    per_person = []
    missing_middle = []
    for participant, positions in frame.groupby("participant").indices.items():
        y, pred = actual[positions], prediction[positions]
        observed = np.unique(y)
        per_person.append(float(np.mean([(pred[y == c] == c).mean() for c in observed])))
        if "medio" not in observed:
            missing_middle.append(participant)
    return {"rows": len(frame), "participants": frame.participant.nunique(),
            "balanced_accuracy": float(balanced_accuracy_score(actual, prediction)),
            "macro_f1": float(f1_score(actual, prediction, average="macro", zero_division=0)),
            "participant_macro_ba_observed_classes": float(np.mean(per_person)),
            "participants_without_middle": ",".join(missing_middle)}


def main() -> None:
    data = pd.read_csv(DATA)
    rows = []
    config = {"seed": 20260822, "temporal_context_windows": 6,
              "selection": "No se ajustaron hiperparámetros ni se eligió una variante por validación o test.",
              "dataset_sha256": hashlib.sha256(DATA.read_bytes()).hexdigest()}
    for task, (target, columns) in TASKS.items():
        frame = data.loc[data.eligible_attention & data.split.isin(["train", "validation", "test"])
                         & data[target].notna()].copy().reset_index(drop=True)
        frame["_target"] = frame[target]
        extra = temporal_features(frame, columns)
        for col in extra:
            frame[col] = extra[col].to_numpy()
        train = frame.split.eq("train")
        for model_name, features in [("dummy", columns), ("static_logistic", columns),
                                     ("temporal_logistic_6w", columns + extra.columns.tolist())]:
            if model_name == "dummy":
                model = Pipeline([("imputer", SimpleImputer(strategy="median")),
                                  ("model", DummyClassifier(strategy="prior"))])
            else:
                model = Pipeline([("imputer", SimpleImputer(strategy="median", add_indicator=True)),
                                  ("scale", StandardScaler()),
                                  ("model", LogisticRegression(max_iter=2000, class_weight="balanced",
                                                               random_state=20260822))])
            model.fit(frame.loc[train, features], frame.loc[train, target])
            for split in ["validation", "test"]:
                part = frame.loc[frame.split.eq(split)].copy().reset_index(drop=True)
                pred = model.predict(part[features])
                rows.append({"task": task, "model": model_name, "split": split, **metrics(part, pred)})
            print(task, model_name, "completo", flush=True)
    pd.DataFrame(rows).to_csv(OUT / "comparacion_modelos.csv", index=False)
    (OUT / "protocolo_comparacion.json").write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    print(pd.DataFrame(rows).loc[lambda x:x.split.eq("test")].to_string(index=False))


if __name__ == "__main__":
    main()
