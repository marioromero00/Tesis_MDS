"""Describe errores de predicciones congeladas por persona y estimulo."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from baselines_estaticos import validate_partition
from temporales_core import ROOT, CLASSES, digest, write_json

SOURCE = ROOT / "scripts/diagnosticar_errores_24_10_2026.py"
PROTOCOL = ROOT / "documentacion/Protocolo_Control_Negativo_Temporal_24-10-2026.md"
DATASET = ROOT / "resultados/modelado/dataset_modelado.csv"
PARTITION = ROOT / "resultados/modelado/particion_participantes.csv"
TRAIN_PRED = ROOT / "resultados/ablacion_pca_12-09-2026/predicciones_oof.csv.gz"
TEST_PRED = ROOT / "resultados/evaluacion_test_existente_24-10-2026/predicciones_ciegas.csv.gz"
OUT = ROOT / "resultados/diagnostico_errores_24-10-2026"
TARGET = "arousal_label_6s"
SHARED = ["Meg", "diario_financiero", "temu", "Despega"]


def summarize(group: pd.DataFrame) -> dict:
    truth = group.true.to_numpy()
    prediction = group.prediction.to_numpy()
    present = [c for c in CLASSES if (truth == c).any()]
    recalls = {f"recall_{c}": float((prediction[truth == c] == c).mean())
               if c in present else np.nan for c in CLASSES}
    return {"rows": len(group), "people": group.participant.nunique(),
            "classes_present": len(present), "accuracy": float((truth == prediction).mean()),
            "ba": float(np.nanmean(list(recalls.values()))),
            **{f"true_{c}": int((truth == c).sum()) for c in CLASSES},
            **{f"predicted_{c}": int((prediction == c).sum()) for c in CLASSES},
            **recalls}


def attach(data: pd.DataFrame, predictions: pd.DataFrame, split: str) -> pd.DataFrame:
    if predictions.source_row.duplicated().any() or predictions.source_row.isna().any():
        raise ValueError("Predicciones duplicadas")
    idx = predictions.source_row.to_numpy(int)
    if len(idx) == 0 or idx.min() < 0 or idx.max() >= len(data):
        raise ValueError("Identificador de ventana fuera de rango")
    original = data.iloc[idx].reset_index(drop=True)
    predictions = predictions.reset_index(drop=True)
    if not (original.split.eq(split).all() and
            original.participant.eq(predictions.participant).all() and
            original.window_start_utc.eq(predictions.window_start_utc).all()):
        raise ValueError("Predicciones no alineadas")
    if split == "train" and not original[TARGET].eq(predictions.true).all():
        raise ValueError("Etiquetas originales cambiadas")
    result = predictions[["source_row", "participant", "prediction"]].copy()
    result["true"] = original[TARGET].to_numpy()
    result["stimulus"] = original.stimulus.to_numpy()
    if result[["true", "prediction"]].isna().any().any():
        raise ValueError("Faltan etiquetas o predicciones")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUT))
    args = parser.parse_args()
    out = ROOT / args.output
    paths = [SOURCE, PROTOCOL, DATASET, PARTITION, TRAIN_PRED, TEST_PRED]
    manifest = {"created_utc": datetime.now(timezone.utc).isoformat(),
                "sources_sha256": {str(p.relative_to(ROOT)): digest(p) for p in paths},
                "shared_stimuli": SHARED, "target": TARGET,
                "new_independent_sample": False, "external_construct_validation": False}
    if out.exists():
        old = json.loads((out / "protocolo.json").read_text(encoding="utf-8"))
        manifest["created_utc"] = old["created_utc"]
        if old != manifest:
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
    expected = {"train": (13524, 25), "test": (4025, 8)}
    if any((len(f), f.participant.nunique()) != expected[s] for s, f in frames.items()):
        raise ValueError("Cobertura de predicciones inesperada")
    people_rows = []
    stimulus_rows = []
    confusion_rows = []
    summaries = []
    for split, frame in frames.items():
        summaries.append({"split": split, **summarize(frame)})
        for participant, group in frame.groupby("participant", sort=True):
            people_rows.append({"split": split, "participant": participant, **summarize(group)})
        for stimulus, group in frame.groupby("stimulus", sort=True):
            stimulus_rows.append({"split": split, "stimulus": stimulus, **summarize(group)})
        count = pd.crosstab(frame.true, frame.prediction).reindex(index=CLASSES, columns=CLASSES, fill_value=0)
        for true in CLASSES:
            for predicted in CLASSES:
                confusion_rows.append({"split": split, "true": true, "prediction": predicted,
                                       "rows": int(count.loc[true, predicted])})
    people = pd.DataFrame(people_rows)
    stimuli = pd.DataFrame(stimulus_rows)
    people.to_csv(out / "errores_personas.csv", index=False)
    stimuli.to_csv(out / "errores_estimulos.csv", index=False)
    pd.DataFrame(confusion_rows).to_csv(out / "confusion.csv", index=False)
    shared = stimuli.loc[stimuli.stimulus.isin(SHARED)].copy()
    if len(shared) != 2 * len(SHARED):
        raise ValueError("Faltan estimulos compartidos")
    shared.to_csv(out / "estimulos_compartidos.csv", index=False)
    report = {"summaries": summaries,
              "person_ba_range": {split: [float(x.ba.min()), float(x.ba.max())]
                                  for split, x in people.groupby("split")},
              "shared_stimuli": SHARED,
              "interpretation": "Descriptivo; diferencias por estimulo confundidas por persona, orden y duracion"}
    write_json(out / "resumen.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
