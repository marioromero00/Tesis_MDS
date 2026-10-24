"""Auditoria interna de pseudoetiquetas; no estima validez psicologica."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score

from temporales_core import ROOT, digest, write_json

DATASET = ROOT / "resultados/modelado/dataset_modelado.csv"
PARTITION = ROOT / "resultados/modelado/particion_participantes.csv"
OUT = ROOT / "resultados/auditoria_pseudoetiquetas_24-10-2026"
SOURCE = ROOT / "scripts/auditar_pseudoetiquetas_24_10_2026.py"
PAIRS = [
    ("attention_equal_vs_pca", "attention_label_equal", "attention_label_pca",
     "attention_score_equal", "attention_score_pca"),
    ("arousal_6s_vs_pca", "arousal_label_6s", "arousal_label_pca",
     "arousal_score_6s", "arousal_score_pca"),
    ("arousal_6s_vs_2s", "arousal_label_6s", "arousal_label_2s",
     "arousal_score_6s", "arousal_score_2s"),
]
LABELS = ["bajo", "medio", "alto"]


def agreement(frame, name, a, b, score_a, score_b):
    clean = frame[[a, b, score_a, score_b]].dropna()
    if clean.empty:
        raise ValueError(f"Sin pares: {name}")
    return {"comparison": name, "rows": len(clean),
            "agreement": float((clean[a] == clean[b]).mean()),
            "kappa": float(cohen_kappa_score(clean[a], clean[b], labels=LABELS)),
            "spearman": float(clean[[score_a, score_b]].corr(method="spearman").iloc[0, 1])}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUT))
    args = parser.parse_args()
    out = ROOT / args.output
    manifest = {"created_utc": datetime.now(timezone.utc).isoformat(),
                "source_sha256": digest(SOURCE), "dataset_sha256": digest(DATASET),
                "partition_sha256": digest(PARTITION), "split": "train",
                "external_construct_validation": False,
                "validation_evaluated": False, "test_evaluated": False}
    if out.exists():
        previous = json.loads((out / "protocolo.json").read_text(encoding="utf-8"))
        manifest["created_utc"] = previous["created_utc"]
        if manifest != previous:
            raise ValueError("Fuentes o protocolo cambiados")
    else:
        out.mkdir(parents=True)
        write_json(out / "protocolo.json", manifest)
    columns = ["participant", "split", "window_start_utc", "attention_eye_component",
               "attention_pupil_component", "pupil_both_valid_fraction", "pupil_coverage",
               "gaze_coverage", "gsr_coverage"] + [item for pair in PAIRS for item in pair[1:]]
    columns = list(dict.fromkeys(columns))
    data = pd.read_csv(DATASET, usecols=columns)
    train = data.loc[data.split.eq("train")].copy()
    if train.participant.nunique() != 25 or len(train) != 13524:
        raise ValueError("Train original cambiado")
    comparisons = [agreement(train, *pair) for pair in PAIRS]
    pd.DataFrame(comparisons).to_csv(out / "concordancia.csv", index=False)
    people = []
    for person, group in train.groupby("participant"):
        for pair in PAIRS:
            people.append({"participant": person, **agreement(group, *pair)})
    pd.DataFrame(people).to_csv(out / "concordancia_participantes.csv", index=False)
    proportions = []
    for label in ["attention_label_equal", "arousal_label_6s"]:
        for category in LABELS:
            proportions.append({"label": label, "class": category,
                                "rows": int(train[label].eq(category).sum()),
                                "fraction": float(train[label].eq(category).mean())})
    pd.DataFrame(proportions).to_csv(out / "distribucion_clases.csv", index=False)
    thresholds = []
    for person, group in train.groupby("participant"):
        for score in ["attention_score_equal", "arousal_score_6s"]:
            low, high = group[score].dropna().quantile([1 / 3, 2 / 3]).tolist()
            thresholds.append({"participant": person, "score": score,
                               "low_tercile": float(low), "high_tercile": float(high)})
    pd.DataFrame(thresholds).to_csv(out / "umbrales_relativos.csv", index=False)
    components = train[["attention_eye_component", "attention_pupil_component"]].corr(method="spearman")
    quality = {}
    for column in ["pupil_both_valid_fraction", "pupil_coverage", "gaze_coverage", "gsr_coverage"]:
        quality[column] = {"missing_fraction": float(train[column].isna().mean()),
                           "median": float(train[column].median())}
    report = {"rows": len(train), "participants": train.participant.nunique(),
              "comparisons": comparisons,
              "eye_pupil_component_spearman": float(components.iloc[0, 1]),
              "quality": quality, "external_construct_validation": False,
              "interpretation": "Concordancia entre reglas derivadas de las mismas senales; no prueba atencion o activacion reales."}
    write_json(out / "resumen.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
