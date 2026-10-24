"""Audita profesores y crea dos objetivos de sensibilidad sin consultar el rendimiento predictivo."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from preparar_modelado import ternary, zscore

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "resultados/preprocesamiento/caracteristicas_multimodales.csv"
AUDITED = ROOT / "resultados/modelado_auditado_24-10-2026/dataset_modelado.csv"
OUT = ROOT / "resultados/estudio_pseudoetiquetas_24-10-2026"
QUANTILES = [0.3333333333, 0.6666666667]


def label(score: pd.Series, valid: pd.Series, participant: pd.Series, quantiles=QUANTILES) -> pd.Series:
    return score.where(valid).groupby(participant).transform(lambda s: ternary(s, quantiles))


def agreement(a: pd.Series, b: pd.Series, valid: pd.Series) -> float:
    keep = valid & a.notna() & b.notna()
    return float(a[keep].eq(b[keep]).mean()) if keep.any() else float("nan")


def stimulus_eta(frame: pd.DataFrame, column: str) -> float:
    work = frame[["participant", "stimulus", column]].dropna()
    person = work.groupby("participant")[column].transform("mean")
    stimulus = work.groupby(["participant", "stimulus"])[column].transform("mean")
    denominator = ((work[column] - person) ** 2).sum()
    return float(((stimulus - person) ** 2).sum() / denominator) if denominator else float("nan")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source = pd.read_csv(SOURCE)
    data = pd.read_csv(AUDITED)
    keys = ["participant", "recording", "segment_id", "window_start_utc"]
    if len(source) != len(data) or not source[keys].equals(data[keys]):
        raise ValueError("Fuente y dataset auditado no coinciden por ventana")
    valid = data.eligible_attention
    train = valid & data.split.eq("train")
    source["split"] = data.split
    source["eligible"] = valid
    source["attention_eye_component"] = data.attention_eye_component
    source["attention_pupil_component"] = data.attention_pupil_component

    # Los profesores alternativos usan las mismas ventanas, normalización offline y split.
    eye_score = data.groupby("participant")["attention_eye_component"].transform(zscore)
    gsr_current = source.groupby("participant")["gsr_mean_z"].transform(zscore)
    order = source.sort_values(["participant", "recording", "segment_id", "window_start_recording_s"]).index
    gsr_context = (gsr_current.loc[order]
                   .groupby([source.loc[order, "participant"], source.loc[order, "recording"],
                             source.loc[order, "segment_id"]])
                   .transform(lambda s: s.rolling(5, min_periods=1).mean()))
    gsr_context = gsr_context.reindex(source.index).groupby(source.participant).transform(zscore)
    data["attention_score_eye_only"] = eye_score
    data["attention_label_eye_only"] = label(eye_score, valid, data.participant)
    data["arousal_score_gsr_continuous_6s"] = gsr_context
    data["arousal_label_gsr_continuous_6s"] = label(gsr_context, valid, data.participant)

    stability = []
    # Sensibilidad de pesos y cuantiles en train, sin elegir con validation/test.
    for weight in [0.25, 0.5, 0.75, 1.0]:
        score = weight * data.attention_eye_component + (1 - weight) * data.attention_pupil_component
        alt = label(score, valid, data.participant)
        stability.append({"target": "attention", "variant": f"eye_weight_{weight:g}",
                          "agreement_train": agreement(data.attention_label_equal, alt, train)})
    stability.append({"target": "arousal", "variant": "gsr_continuous_6s",
                      "agreement_train": agreement(data.arousal_label_6s, data.arousal_label_gsr_continuous_6s, train)})
    stability.append({"target": "arousal", "variant": "original_2s",
                      "agreement_train": agreement(data.arousal_label_6s, data.arousal_label_2s, train)})
    longer = (data.loc[order, "arousal_score_2s"]
              .groupby([source.loc[order, "participant"], source.loc[order, "recording"],
                        source.loc[order, "segment_id"]])
              .transform(lambda s: s.rolling(9, min_periods=1).mean()))
    longer = longer.reindex(source.index).groupby(source.participant).transform(zscore)
    longer_label = label(longer, valid, data.participant)
    stability.append({"target": "arousal", "variant": "original_10s",
                      "agreement_train": agreement(data.arousal_label_6s, longer_label, train)})
    for target, score, baseline in [
        ("attention", data.attention_score_equal, data.attention_label_equal),
        ("arousal", data.arousal_score_6s, data.arousal_label_6s),
    ]:
        for q in [0.25, 0.40]:
            alt = label(score, valid, data.participant, [q, 1-q])
            stability.append({"target": target, "variant": f"quantiles_{q:g}_{1-q:g}",
                              "agreement_train": agreement(baseline, alt, train)})
    pd.DataFrame(stability).to_csv(OUT / "estabilidad_train.csv", index=False)
    participant_rows = []
    for participant, group in data.loc[train].groupby("participant"):
        for target, base, candidate in [
            ("attention", "attention_label_equal", "attention_label_eye_only"),
            ("arousal", "arousal_label_6s", "arousal_label_gsr_continuous_6s"),
        ]:
            participant_rows.append({"participant": participant, "target": target, "rows": len(group),
                                     "agreement": float(group[base].eq(group[candidate]).mean())})
    pd.DataFrame(participant_rows).to_csv(OUT / "estabilidad_participantes_train.csv", index=False)

    train_source = source.loc[train]
    train_scores = data.loc[train]
    diagnostics = {
        "scr_count_zero_fraction_train": float(train_source.gsr_scr_count.eq(0).mean()),
        "scr_prominence_zero_fraction_train": float(train_source.gsr_scr_mean_prominence_z.eq(0).mean()),
        "stimulus_eta_train": {name: stimulus_eta(train_source, name) for name in
                               ["attention_eye_component", "attention_pupil_component", "pupil_mean_z",
                                "gsr_mean_z", "gsr_scr_count"]},
        "arousal_score_stimulus_eta_train": {
            "audited_6s": stimulus_eta(train_scores, "arousal_score_6s"),
            "gsr_continuous_6s": stimulus_eta(train_scores, "arousal_score_gsr_continuous_6s"),
        },
        "participants_without_middle_train": {
            col: [str(p) for p, group in data.loc[train].groupby("participant")
                  if not group[col].eq("medio").any()]
            for col in ["attention_label_equal", "attention_label_eye_only", "arousal_label_6s",
                        "arousal_label_gsr_continuous_6s"]},
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "audited_sha256": hashlib.sha256(AUDITED.read_bytes()).hexdigest(),
        "candidate_rule": "Candidata de atención: excluir pupila por alta asociación con estímulo sin medición de luminancia. "
                          "Candidata de activación: excluir recuento/prominencia SCR por casi todos los valores cero. "
                          "Variantes definidas con diagnósticos de train antes de comparar modelos; son exploratorias.",
    }
    (OUT / "diagnosticos_train.json").write_text(json.dumps(diagnostics, indent=2, ensure_ascii=False), encoding="utf-8")
    data.to_csv(OUT / "dataset_sensibilidad.csv", index=False, float_format="%.8g")
    print(json.dumps({"diagnostics": diagnostics, "stability": stability}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
