"""Crea pseudoetiquetas y una particion congelada, siempre por participante."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA


ROOT = Path(__file__).resolve().parents[1]


def stable_key(seed: int, participant: str) -> str:
    return hashlib.sha256(f"{seed}:{participant}".encode()).hexdigest()


def participant_split(metadata: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Particion determinista y estratificada; nunca divide ventanas de una persona."""
    seed = int(config["random_seed"])
    sensitive = set(config["split"]["sensitivity_only_participants"])
    rows = []
    eligible = metadata[metadata["eligible_primary"]].copy()
    for timeline, group in eligible.groupby("timeline", sort=True):
        participants = sorted(group.participant, key=lambda p: stable_key(seed, p))
        n = len(participants)
        n_test = max(1, round(n * config["split"]["test_fraction"]))
        n_val = max(1, round(n * config["split"]["validation_fraction"]))
        if n_test + n_val >= n:
            n_test = n_val = 1
        for index, participant in enumerate(participants):
            split = "test" if index < n_test else "validation" if index < n_test + n_val else "train"
            rows.append({"participant": participant, "timeline": timeline, "split": split,
                         "eligible_primary": True, "reason": "calidad_y_sincronizacion_aprobadas"})
    for row in metadata.itertuples(index=False):
        if row.eligible_primary:
            continue
        if row.participant in sensitive and row.quality_eligible:
            reason = "sensibilidad_offset_P29"
            split = "sensitivity"
        else:
            reason = row.exclusion_reason
            split = "excluded"
        rows.append({"participant": row.participant, "timeline": row.timeline, "split": split,
                     "eligible_primary": False, "reason": reason})
    return pd.DataFrame(rows).sort_values("participant", key=lambda s: s.str.extract(r"(\d+)")[0].astype(int))


def zscore(series: pd.Series) -> pd.Series:
    std = series.std(ddof=0)
    return (series - series.mean()) / std if pd.notna(std) and std > 0 else pd.Series(0.0, index=series.index)


def transformed_feature(frame: pd.DataFrame, column: str) -> pd.Series:
    values = frame[column].astype(float)
    if column in {"fixation_total_ms", "fixation_mean_ms", "gaze_dispersion_2d_px",
                  "gaze_path_length_px", "gsr_scr_count", "gsr_scr_mean_prominence_z"}:
        values = np.log1p(values.clip(lower=0))
    return values


def teacher_components(frame: pd.DataFrame, config: dict) -> tuple[pd.DataFrame, list[str], list[str]]:
    result = frame.copy()
    attention = config["attention_teacher"]
    attention_cols = attention["eye_features"] + attention["pupil_features"]
    attention_component_cols = []
    for column, direction in zip(attention_cols, attention["direction"]):
        target = f"teacher_z_{column}"
        result[target] = result.groupby("participant", group_keys=False).apply(
            lambda group: zscore(transformed_feature(group, column)), include_groups=False
        ).reset_index(level=0, drop=True)
        result[target] *= direction
        attention_component_cols.append(target)
    eye_cols = attention_component_cols[:len(attention["eye_features"])]
    pupil_cols = attention_component_cols[len(attention["eye_features"]):]
    result["attention_eye_component"] = result[eye_cols].mean(axis=1)
    result["attention_pupil_component"] = result[pupil_cols].mean(axis=1)
    result["attention_score_equal"] = result[["attention_eye_component", "attention_pupil_component"]].mean(axis=1)
    result["attention_score_equal"] = result.groupby("participant")["attention_score_equal"].transform(zscore)

    arousal_cols = []
    for column in config["arousal_teacher"]["features"]:
        target = f"teacher_z_{column}"
        result[target] = result.groupby("participant", group_keys=False).apply(
            lambda group: zscore(transformed_feature(group, column)), include_groups=False
        ).reset_index(level=0, drop=True)
        arousal_cols.append(target)
    result["arousal_score_2s"] = result[arousal_cols].mean(axis=1)
    result["arousal_score_2s"] = result.groupby("participant")["arousal_score_2s"].transform(zscore)
    # Cinco inicios separados por 1 s cubren una ventana causal de 6 s.
    result["arousal_score_6s"] = (
        result.sort_values(["participant", "recording", "segment_id", "window_start_recording_s"])
        .groupby(["participant", "recording", "segment_id"])["arousal_score_2s"]
        .transform(lambda s: s.rolling(5, min_periods=1).mean())
    )
    result["arousal_score_6s"] = result.groupby("participant")["arousal_score_6s"].transform(zscore)
    return result, attention_component_cols, arousal_cols


def add_pca_sensitivity(frame: pd.DataFrame, split_map: dict, attention_cols: list[str], arousal_cols: list[str]) -> pd.DataFrame:
    result = frame.copy()
    train = result.participant.map(split_map).eq("train")
    for label, columns, reference in [
        ("attention_score_pca", attention_cols, "attention_score_equal"),
        ("arousal_score_pca", arousal_cols, "arousal_score_6s"),
    ]:
        complete_train = train & result[columns].notna().all(axis=1)
        pca = PCA(n_components=1, random_state=0).fit(result.loc[complete_train, columns])
        values = np.full(len(result), np.nan)
        complete = result[columns].notna().all(axis=1)
        values[complete] = pca.transform(result.loc[complete, columns]).ravel()
        correlation = np.corrcoef(values[complete], result.loc[complete, reference])[0, 1]
        if correlation < 0:
            values *= -1
        result[label] = values
        result[label] = result.groupby("participant")[label].transform(zscore)
    return result


def ternary(series: pd.Series, quantiles: list[float]) -> pd.Series:
    valid = series.dropna()
    if valid.empty:
        return pd.Series(pd.NA, index=series.index, dtype="string")
    low, high = valid.quantile(quantiles).tolist()
    labels = np.select([series <= low, series >= high], ["bajo", "alto"], default="medio")
    return pd.Series(labels, index=series.index, dtype="string").where(series.notna())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config/modelado.json")
    args = parser.parse_args()
    config_path = (ROOT / args.config).resolve() if not Path(args.config).is_absolute() else Path(args.config)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    source = (ROOT / config["input_features"]).resolve()
    output = (ROOT / config["output_dir"]).resolve()
    output.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(source)
    participant_meta = []
    for participant, part in frame.groupby("participant", sort=False):
        timeline = part.timeline.mode().iloc[0]
        eeg_ok = bool(part.eeg_quality_usable.iloc[0])
        gsr_ok = bool(part.gsr_window_valid.any())
        sync_ok = part.eeg_match_status.iloc[0] == "candidato"
        quality_ok = eeg_ok and gsr_ok
        reasons = []
        if not eeg_ok: reasons.append("eeg_no_utilizable")
        if not gsr_ok: reasons.append("sin_gsr")
        if not sync_ok: reasons.append("sincronizacion_por_revisar")
        participant_meta.append({"participant": participant, "timeline": timeline,
                                 "quality_eligible": quality_ok,
                                 "eligible_primary": quality_ok and sync_ok,
                                 "exclusion_reason": "+".join(reasons) or "ninguna"})
    metadata = pd.DataFrame(participant_meta)
    split = participant_split(metadata, config)
    split_map = split.set_index("participant").split.to_dict()
    frame["split"] = frame.participant.map(split_map)
    frame, attention_cols, arousal_cols = teacher_components(frame, config)
    frame = add_pca_sensitivity(frame, split_map, attention_cols, arousal_cols)
    quantiles = config["labels"]["quantiles"]
    for score in ["attention_score_equal", "attention_score_pca", "arousal_score_2s", "arousal_score_6s", "arousal_score_pca"]:
        frame[score.replace("score", "label")] = frame.groupby("participant")[score].transform(lambda s: ternary(s, quantiles))
    frame["eligible_attention"] = frame.multimodal_window_valid & frame.split.isin(["train", "validation", "test"])
    frame["eligible_arousal"] = frame["eligible_attention"]
    keep_identity = ["participant", "recording", "timeline", "stimulus", "segment_id", "window_index",
                     "window_start_utc", "window_end_utc", "split", "eeg_match_status"]
    teacher_outputs = ["attention_eye_component", "attention_pupil_component", "attention_score_equal",
                       "attention_score_pca", "attention_label_equal", "attention_label_pca",
                       "arousal_score_2s", "arousal_score_6s", "arousal_score_pca",
                       "arousal_label_2s", "arousal_label_6s", "arousal_label_pca",
                       "eligible_attention", "eligible_arousal"]
    feature_cols = [c for c in frame.columns if c.startswith(("eeg_", "gsr_", "pupil_", "gaze_", "fixation_", "saccade_"))]
    dataset = frame[keep_identity + feature_cols + teacher_outputs]
    dataset.to_csv(output / "dataset_modelado.csv", index=False, float_format="%.8g")
    split.to_csv(output / "particion_participantes.csv", index=False)
    audit = {
        "config_sha256": hashlib.sha256(config_path.read_bytes()).hexdigest(),
        "pipeline_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "requirements_sha256": hashlib.sha256((ROOT / "requirements.txt").read_bytes()).hexdigest(),
        "input_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "rows": len(dataset), "participants": int(dataset.participant.nunique()),
        "split_participants": split.groupby("split").size().to_dict(),
        "eligible_attention_rows": int(dataset.eligible_attention.sum()),
        "eligible_arousal_rows": int(dataset.eligible_arousal.sum()),
        "attention_equal_vs_pca_spearman": float(dataset[["attention_score_equal", "attention_score_pca"]].corr(method="spearman").iloc[0, 1]),
        "arousal_6s_vs_pca_spearman": float(dataset[["arousal_score_6s", "arousal_score_pca"]].corr(method="spearman").iloc[0, 1]),
        "notes": ["P29 solo sensibilidad", "Pupila sin correccion luminica", "Etiquetas provisionales hasta aprobacion del profesor"],
    }
    (output / "manifiesto_etiquetas.json").write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(audit, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
