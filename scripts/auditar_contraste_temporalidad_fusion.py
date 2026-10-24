"""Recalcula predicciones desde modelos guardados, sin etiquetas ni senales profesor."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits

from contraste_temporalidad_fusion import (
    OUT, ROOT, DATASET, PARTITION, SOURCE, SPECS, CLASSES,
    digest, frame_for, predict, write_json,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUT))
    args = parser.parse_args()
    out = Path(args.output)
    if not out.is_absolute():
        out = ROOT / out
    protocol = json.loads((out / "protocolo.json").read_text(encoding="utf-8"))
    if protocol["source_sha256"] != digest(SOURCE):
        raise ValueError("Codigo de entrenamiento cambiado")
    if protocol["dataset_sha256"] != digest(DATASET) or protocol["partition_sha256"] != digest(PARTITION):
        raise ValueError("Fuentes cambiadas")
    data = pd.read_csv(DATASET)
    data["source_row"] = np.arange(len(data))
    tasks = sorted((out / "tareas").glob("*.json"))
    if len(tasks) != 80:
        raise ValueError("Faltan tareas")
    rows = 0
    models = 0
    with threadpool_limits(limits=2):
        for path in tasks:
            task = json.loads(path.read_text(encoding="utf-8"))
            spec = SPECS[task["task"]]
            frame = frame_for(data, task["task"])
            val = frame.loc[frame.participant.isin(task["evaluation"])].reset_index(drop=True)
            if set(val.participant) != set(task["evaluation"]):
                raise ValueError("Participantes incompletos")
            allowed = sum(spec["modalities"].values(), [])
            keys = ["split", "participant", "recording", "segment_id", "stimulus", "window_start_utc"]
            # Deliberadamente se quitan el objetivo y las senales que lo construyen.
            blind = val[keys + allowed].copy()
            scores = []
            for item in task["models"]:
                model_path = out / item["path"]
                if digest(model_path) != item["sha256"]:
                    raise ValueError("Hash de modelo cambiado")
                bundle = joblib.load(model_path)
                if not set(bundle["features"]) <= set(allowed):
                    raise ValueError("Modelo usa senal del profesor")
                scores.append(predict(bundle, blind))
                models += 1
            actual = np.mean(scores, axis=0)
            prediction_path = out / task["predictions"]["path"]
            if digest(prediction_path) != task["predictions"]["sha256"]:
                raise ValueError("Hash de predicciones cambiado")
            saved = pd.read_csv(prediction_path)
            np.testing.assert_array_equal(saved.source_row, val.source_row)
            np.testing.assert_allclose(
                actual, saved[[f"prob_{c}" for c in CLASSES]].to_numpy(float),
                rtol=0, atol=5e-10,
            )
            np.testing.assert_array_equal(np.asarray(CLASSES)[actual.argmax(axis=1)], saved.prediction)
            rows += len(saved)
    if rows != 216384 or models != 140:
        raise ValueError("Conteos inesperados")
    report = {"tasks": len(tasks), "models_reloaded": models, "predictions_recomputed": rows,
              "teacher_signals_absent": True, "labels_absent_at_prediction": True,
              "validation_evaluated": False, "test_evaluated": False,
              "source_sha256": digest(SOURCE), "dataset_sha256": digest(DATASET)}
    write_json(out / "auditoria_independiente.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
