"""Genera pseudoetiquetas con un PC por modalidad profesora, ajustado solo en train."""
from __future__ import annotations

import hashlib
import json
import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from preparar_modelado import ternary, transformed_feature, zscore

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/pca_senales_v2.json"
EYE_DIRECTIONS = {"fixation_total_ms": 1, "fixation_mean_ms": 1,
                  "gaze_dispersion_2d_px": -1, "gaze_path_length_px": -1}


def eligible_zscore(values: pd.Series, participant: pd.Series, eligible: pd.Series) -> pd.Series:
    return values.where(eligible).groupby(participant).transform(zscore).where(eligible)


def normalized_inputs(frame: pd.DataFrame, columns: list[str], eligible: pd.Series | None = None) -> pd.DataFrame:
    if eligible is None:
        eligible = pd.Series(True, index=frame.index)
    result = pd.DataFrame(index=frame.index)
    for column in columns:
        values = transformed_feature(frame, column)
        result[column] = eligible_zscore(values, frame.participant, eligible) * EYE_DIRECTIONS.get(column, 1)
    return result


def causal_context(frame: pd.DataFrame, score: pd.Series, eligible: pd.Series, windows: int) -> tuple[pd.Series, int]:
    """Promedio causal de inicios consecutivos; reinicia ante cualquier hueco."""
    ordered = frame.loc[eligible].sort_values(
        ["participant", "recording", "segment_id", "window_start_recording_s"])
    keys = [ordered.participant, ordered.recording, ordered.segment_id]
    gap = ordered.groupby(["participant", "recording", "segment_id"]).window_start_recording_s.diff()
    reset = gap.notna() & ~np.isclose(gap.fillna(1), 1.0, rtol=0, atol=1e-4)
    block = reset.groupby(keys).cumsum()
    context = score.loc[ordered.index].groupby(keys + [block]).transform(
        lambda s: s.rolling(windows, min_periods=1).mean())
    result = pd.Series(np.nan, index=frame.index)
    result.loc[ordered.index] = context
    return result, int(reset.sum())


def fit_teacher_pc(values: pd.DataFrame, train: pd.Series, reference: pd.Series) -> tuple[Pipeline, np.ndarray, dict]:
    pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median", keep_empty_features=True)),
        ("scale", StandardScaler()),
        ("pca", PCA(n_components=1, random_state=0)),
    ]).fit(values.loc[train])
    scores = pipeline.transform(values).ravel()
    correlation = float(np.corrcoef(scores[train], reference.loc[train])[0, 1])
    if not np.isfinite(correlation) or abs(correlation) < 0.05:
        raise ValueError("Orientación del PC inestable frente a la referencia de train")
    direction = -1 if correlation < 0 else 1
    scores *= direction
    metadata = {"features": values.columns.tolist(), "raw_features": len(values.columns),
                "components": 1, "explained_variance_ratio": float(pipeline.named_steps["pca"].explained_variance_ratio_[0]),
                "train_orientation_correlation": correlation, "direction": direction,
                "train_rows": int(train.sum())}
    return pipeline, scores, metadata


def main(config_path: Path = CONFIG) -> None:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    source_path = ROOT / config["source_features"]
    partition_path = ROOT / config["source_partition"]
    output = ROOT / config["output_dir"]
    output.mkdir(parents=True, exist_ok=True)
    (output / "teacher_models").mkdir(exist_ok=True)
    source = pd.read_csv(source_path)
    partition = pd.read_csv(partition_path)
    if partition.participant.duplicated().any():
        raise ValueError("Participante duplicado en la partición congelada")
    data = source.copy()
    data["split"] = data.participant.map(partition.set_index("participant").split)
    if data.split.isna().any():
        raise ValueError("Falta participante en la partición congelada")
    eligible = data.multimodal_window_valid & data.split.isin(["train", "validation", "test", "sensitivity"])
    data["eligible_attention"] = eligible
    data["eligible_arousal"] = eligible
    train = data.split.eq("train") & eligible
    valid = eligible
    scores = {}
    teacher_info = {}
    for name in ["attention_eye", "attention_pupil", "arousal_gsr"]:
        values = normalized_inputs(source, config["teacher"][name], eligible)
        # La referencia de signo se reconstruye de estas mismas ventanas; los scores
        # históricos no se usan porque su generación anterior perdió alineación de filas.
        pipeline, pc_score, info = fit_teacher_pc(values, train, values.mean(axis=1))
        path = output / "teacher_models" / f"{name}.joblib"
        joblib.dump(pipeline, path, compress=3)
        restored = joblib.load(path)
        np.testing.assert_allclose(pipeline.transform(values), restored.transform(values), rtol=0, atol=0)
        info["model_path"] = path.relative_to(output).as_posix()
        info["model_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        teacher_info[name] = info
        scores[name] = eligible_zscore(pd.Series(pc_score, index=data.index), data.participant, eligible)
        data[f"teacher_pc_{name}"] = scores[name]

    attention = ((scores["attention_eye"] + scores["attention_pupil"]) / 2)
    data["attention_score_teacher_pca"] = eligible_zscore(attention, data.participant, eligible)
    arousal_2s = scores["arousal_gsr"]
    arousal_6s, gap_resets = causal_context(source, arousal_2s, eligible, config["teacher"]["arousal_context_windows"])
    data["arousal_score_teacher_pca_6s"] = eligible_zscore(arousal_6s, data.participant, eligible)
    for stem in ["attention", "arousal"]:
        score = "attention_score_teacher_pca" if stem == "attention" else "arousal_score_teacher_pca_6s"
        label = score.replace("score", "label")
        data[label] = data[score].where(valid).groupby(data.participant).transform(
            lambda s: ternary(s, config["teacher"]["label_quantiles"]))
    dataset_path = output / "dataset_pca_senales.csv"
    data.to_csv(dataset_path, index=False, float_format="%.8g")
    summary = {
        "config_sha256": hashlib.sha256(config_path.read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "partition_sha256": hashlib.sha256(partition_path.read_bytes()).hexdigest(),
        "dataset_sha256": hashlib.sha256(dataset_path.read_bytes()).hexdigest(),
        "teacher": teacher_info,
        "eligible_gap_resets": gap_resets,
        "primary_rows": {split: int((data.split.eq(split) & valid).sum()) for split in ["train", "validation", "test"]},
        "class_counts": {label: {split: data.loc[data.split.eq(split) & valid, label].value_counts().to_dict()
                                 for split in ["train", "validation", "test"]}
                         for label in ["attention_label_teacher_pca", "arousal_label_teacher_pca_6s"]},
        "notes": "PCA y signo ajustados con train elegible; normalización por participante solo en ventanas elegibles; contexto reiniciado ante huecos. Etiquetas offline por participante.",
    }
    (output / "manifiesto_profesor.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(CONFIG))
    args = parser.parse_args()
    main(Path(args.config).resolve())
