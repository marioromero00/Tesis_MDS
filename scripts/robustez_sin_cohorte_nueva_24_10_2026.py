"""Robustez descriptiva de predicciones fijas frente a variantes del profesor."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score

from baselines_estaticos import validate_partition
from temporales_core import ROOT, CLASSES, digest, write_json

SOURCE = ROOT / "scripts/robustez_sin_cohorte_nueva_24_10_2026.py"
DATASET = ROOT / "resultados/modelado/dataset_modelado.csv"
PARTITION = ROOT / "resultados/modelado/particion_participantes.csv"
TRAIN_PRED = ROOT / "resultados/ablacion_pca_12-09-2026/predicciones_oof.csv.gz"
TEST_PRED = ROOT / "resultados/evaluacion_test_existente_24-10-2026/predicciones_ciegas.csv.gz"
TEST_PROTOCOL = ROOT / "resultados/evaluacion_test_existente_24-10-2026/protocolo.json"
PROTOCOL = ROOT / "documentacion/Protocolo_Robustez_Sin_Cohorte_Nueva_24-10-2026.md"
OUT = ROOT / "resultados/robustez_sin_cohorte_nueva_24-10-2026"
LABELS = {"gsr_6s": "arousal_label_6s", "gsr_2s": "arousal_label_2s",
          "pca_gsr": "arousal_label_pca"}
SEED = 20261024
BOOT = 5000


def person_metrics(frame: pd.DataFrame, truth: str) -> pd.DataFrame:
    rows = []
    for participant, group in frame.groupby("participant", sort=True):
        y = group[truth].to_numpy()
        p = group.prediction.to_numpy()
        present = [c for c in CLASSES if (y == c).any()]
        recall = {c: float((p[y == c] == c).mean()) if c in present else np.nan
                  for c in CLASSES}
        rows.append({"participant": participant, "rows": len(group),
                     "classes_present": len(present),
                     "ba": float(np.mean([recall[c] for c in present])),
                     "constant_ba": 1 / len(present),
                     **{f"recall_{c}": recall[c] for c in CLASSES}})
    return pd.DataFrame(rows)


def interval(values: np.ndarray, seed: int) -> list[float]:
    rng = np.random.default_rng(seed)
    sample = values[rng.integers(0, len(values), size=(BOOT, len(values)))].mean(axis=1)
    return [float(np.quantile(sample, .025)), float(np.quantile(sample, .975))]


def attach(data: pd.DataFrame, predictions: pd.DataFrame, split: str) -> pd.DataFrame:
    if predictions.source_row.isna().any() or predictions.source_row.duplicated().any():
        raise ValueError("source_row invalido o duplicado")
    if not pd.api.types.is_integer_dtype(predictions.source_row):
        raise ValueError("source_row no entero")
    idx = predictions.source_row.to_numpy()
    if len(idx) == 0 or idx.min() < 0 or idx.max() >= len(data):
        raise ValueError("source_row fuera del dataset")
    reference = data.iloc[idx].reset_index(drop=True)
    predictions = predictions.reset_index(drop=True)
    if not (reference.split.eq(split).all() and
            reference.participant.eq(predictions.participant).all() and
            reference.window_start_utc.eq(predictions.window_start_utc).all()):
        raise ValueError("Prediccion y fuente no alineadas")
    if not predictions.prediction.isin(CLASSES).all():
        raise ValueError("Prediccion fuera de clases")
    if split == "train" and not reference[LABELS["gsr_6s"]].eq(predictions.true).all():
        raise ValueError("Etiqueta OOF original no coincide")
    if not reference[LABELS["gsr_6s"]].notna().all():
        raise ValueError("Etiqueta principal ausente")
    result = predictions[["source_row", "participant", "prediction"]].copy()
    for label in LABELS.values():
        result[label] = reference[label].to_numpy()
    return result


def analyse(name: str, frame: pd.DataFrame, out) -> dict:
    expected_rows, expected_people = (13524, 25) if name == "train" else (4025, 8)
    if len(frame) != expected_rows or frame.participant.nunique() != expected_people:
        raise ValueError(f"Cantidad inesperada en {name}")
    summaries = []
    all_people = []
    comparisons = []
    all_person_comparisons = []
    transitions = []
    for index, (variant, column) in enumerate(LABELS.items()):
        subset = frame.dropna(subset=[column]).copy()
        people = person_metrics(subset, column)
        people.insert(0, "reference", variant)
        all_people.append(people)
        values = people.ba.to_numpy()
        summaries.append({"split": name, "reference": variant, "rows": len(subset),
                          "coverage": len(subset) / len(frame), "participants": len(people),
                          "ba_macro": float(values.mean()),
                          "ba_sd_people": float(values.std(ddof=1)),
                          "ba_min": float(values.min()), "ba_max": float(values.max()),
                          "ba_ci_descriptive": interval(values, SEED + index),
                          "constant_ba_macro": float(people.constant_ba.mean()),
                          "people_above_constant": int(people.ba.gt(people.constant_ba).sum()),
                          **{f"recall_{c}": float(subset.loc[subset[column].eq(c), "prediction"].eq(c).mean())
                             for c in CLASSES}})
    pd.concat(all_people).to_csv(out / f"personas_{name}.csv", index=False)
    base = LABELS["gsr_6s"]
    for index, (variant, column) in enumerate(list(LABELS.items())[1:]):
        matched = frame.dropna(subset=[base, column]).copy()
        a = person_metrics(matched, base).set_index("participant")
        b = person_metrics(matched, column).set_index("participant")
        paired = pd.DataFrame({"participant": a.index, "rows": a.rows.to_numpy(),
                               "ba_6s_matched": a.ba.to_numpy(),
                               "ba_variant": b.ba.to_numpy(),
                               "ba_difference_variant_minus_6s": (b.ba - a.ba).to_numpy()})
        paired["agreement"] = [float(group[base].eq(group[column]).mean())
                               for _, group in matched.groupby("participant", sort=True)]
        all_person_comparisons.append(paired.assign(variant=variant))
        diff = paired.ba_difference_variant_minus_6s.to_numpy()
        comparisons.append({"split": name, "variant": variant, "matched_rows": len(matched),
                            "participants": len(paired), "agreement_global": float(matched[base].eq(matched[column]).mean()),
                            "agreement_macro_people": float(paired.agreement.mean()),
                            "kappa_global": float(cohen_kappa_score(matched[base], matched[column], labels=CLASSES)),
                            "ba_6s_matched": float(a.ba.mean()), "ba_variant": float(b.ba.mean()),
                            "ba_difference": float(diff.mean()),
                            "ba_difference_ci_descriptive": interval(diff, SEED + 10 + index),
                            "people_variant_higher": int((diff > 0).sum()),
                            "people_variant_lower": int((diff < 0).sum())})
        count = pd.crosstab(matched[base], matched[column]).reindex(index=CLASSES, columns=CLASSES, fill_value=0)
        for original in CLASSES:
            for alternative in CLASSES:
                transitions.append({"split": name, "variant": variant, "original_6s": original,
                                    "alternative": alternative, "rows": int(count.loc[original, alternative])})
    pd.concat(all_person_comparisons).to_csv(out / f"comparaciones_personas_{name}.csv", index=False)
    pd.DataFrame(transitions).to_csv(out / f"transiciones_{name}.csv", index=False)
    return {"split": name, "summaries": summaries, "comparisons": comparisons}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUT))
    args = parser.parse_args()
    out = ROOT / args.output
    sources = {str(path.relative_to(ROOT)): digest(path) for path in
               [SOURCE, PROTOCOL, DATASET, PARTITION, TRAIN_PRED, TEST_PRED, TEST_PROTOCOL]}
    manifest = {"created_utc": datetime.now(timezone.utc).isoformat(), "sources_sha256": sources,
                "labels": LABELS, "predictions_frozen": True,
                "selection_after_results": False, "bootstrap_seed": SEED,
                "bootstrap_resamples": BOOT, "validation_evaluated": False,
                "new_independent_sample": False, "external_construct_validation": False}
    if out.exists():
        previous = json.loads((out / "protocolo.json").read_text(encoding="utf-8"))
        manifest["created_utc"] = previous["created_utc"]
        if manifest != previous:
            raise ValueError("Fuentes o protocolo cambiados")
    else:
        out.mkdir(parents=True)
        write_json(out / "protocolo.json", manifest)
    data = pd.read_csv(DATASET)
    validate_partition(data, pd.read_csv(PARTITION))
    train = pd.read_csv(TRAIN_PRED)
    train = train.loc[train.variant.eq("drop_fixation_count")].copy()
    test = pd.read_csv(TEST_PRED)
    frames = {"train": attach(data, train, "train"), "test": attach(data, test, "test")}
    if set(frames["train"].participant) & set(frames["test"].participant):
        raise ValueError("Participantes compartidos")
    results = [analyse(name, frame, out) for name, frame in frames.items()]
    report = {"results": results, "prediction_training_target": "arousal_label_6s",
              "interpretation": "Sensibilidad retrospectiva, no validacion independiente ni de constructo"}
    write_json(out / "resumen.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
