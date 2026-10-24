"""Evaluacion adicional del Ridge congelado en test previamente consultado."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import balanced_accuracy_score, f1_score
from threadpoolctl import threadpool_limits

from ablacion_pca_core import predict
from baselines_estaticos import validate_partition
from hiperparametros_core import FULL
from temporales_core import ROOT, CLASSES, digest, write_json

SOURCE = ROOT / "scripts" / "evaluar_ridge_test_existente_24_10_2026.py"
DATASET = ROOT / "resultados/modelado/dataset_modelado.csv"
PARTITION = ROOT / "resultados/modelado/particion_participantes.csv"
ABL = ROOT / "resultados/ablacion_pca_12-09-2026"
OUT = ROOT / "resultados/evaluacion_test_existente_24-10-2026"
VARIANT = "drop_fixation_count"
TARGET = "arousal_label_6s"


def macro_per_person(frame):
    result = []
    for person, group in frame.groupby("participant", sort=True):
        truth, pred = group.true.to_numpy(), group.prediction.to_numpy()
        recalls = [(pred[truth == c] == c).mean() for c in np.unique(truth)]
        result.append({"participant": person, "ba": float(np.mean(recalls)), "rows": len(group),
                       "classes_present": len(recalls)})
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUT))
    args = parser.parse_args()
    out = ROOT / args.output
    catalog = json.loads((ABL / "catalogo_modelos.json").read_text(encoding="utf-8"))
    chosen = sorted((x for x in catalog if x["variant"] == VARIANT), key=lambda x: x["fold"])
    if len(chosen) != 5 or [x["fold"] for x in chosen] != [1, 2, 3, 4, 5]:
        raise ValueError("Faltan modelos congelados")
    if not (ABL / "verificacion.json").exists():
        raise ValueError("Falta auditoria previa")
    model_files = [{"fold": x["fold"], "path": x["path"], "sha256": x["sha256"]} for x in chosen]
    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": digest(SOURCE), "dataset_sha256": digest(DATASET),
        "partition_sha256": digest(PARTITION), "catalog_sha256": digest(ABL / "catalogo_modelos.json"),
        "audit_sha256": digest(ABL / "verificacion.json"), "models": model_files,
        "split": "test", "target": TARGET, "variant": VARIANT,
        "prediction_rule": "media aritmetica de probabilidades de los cinco modelos, pesos 0.2, argmax",
        "primary_metric": "media de BA por participante, clases presentes",
        "status": "evaluacion adicional; test fue consultado en investigaciones anteriores",
        "new_independent_sample": False, "external_construct_validation": False,
    }
    if out.exists():
        previous = json.loads((out / "protocolo.json").read_text(encoding="utf-8"))
        manifest["created_utc"] = previous["created_utc"]
        if previous != manifest:
            raise ValueError("Protocolo o fuentes cambiados")
    else:
        out.mkdir(parents=True)
        write_json(out / "protocolo.json", manifest)
    for item in model_files:
        if digest(ABL / item["path"]) != item["sha256"]:
            raise ValueError("Hash de modelo cambiado")
    data = pd.read_csv(DATASET)
    data["source_row"] = np.arange(len(data))
    partition = pd.read_csv(PARTITION)
    validate_partition(data, partition)
    test = data.loc[data.split.eq("test") & data[TARGET].notna()].copy()
    test = test.sort_values(["participant", "recording", "window_start_utc"]).reset_index(drop=True)
    if test.participant.nunique() != 8 or len(test) != 4025:
        raise ValueError("Test original inesperado")
    known = set().union(*(set(x["train_participants"]) for x in chosen))
    if set(test.participant) & known:
        raise ValueError("Participantes compartidos con ajuste")
    blind = test[["participant", "recording", "window_start_utc"] + FULL].copy()
    probabilities = []
    with threadpool_limits(limits=2):
        for item in model_files:
            bundle = joblib.load(ABL / item["path"])
            if set(bundle["spec"]["variant"]["keep"]) & set(c for c in test if c.startswith("gsr_")):
                raise ValueError("Modelo usa GSR")
            probabilities.append(predict(bundle, blind))
    mean_probability = np.mean(probabilities, axis=0)
    if not np.all(np.isfinite(mean_probability)) or not np.allclose(mean_probability.sum(axis=1), 1, atol=1e-6):
        raise ValueError("Probabilidades invalidas")
    output = test[["source_row", "participant", "window_start_utc"]].copy()
    output["prediction"] = np.asarray(CLASSES)[mean_probability.argmax(axis=1)]
    for i, c in enumerate(CLASSES):
        output[f"prob_{c}"] = mean_probability[:, i]
    prediction_file = out / "predicciones_ciegas.csv.gz"
    output.to_csv(prediction_file, index=False, float_format="%.10g")
    # La comparacion con el profesor sucede solo despues de guardar predicciones.
    saved = pd.read_csv(prediction_file)
    np.testing.assert_array_equal(saved.source_row, test.source_row)
    eval_frame = saved[["source_row", "participant", "prediction"]].copy()
    eval_frame["true"] = test[TARGET].to_numpy()
    people = macro_per_person(eval_frame)
    pd.DataFrame(people).to_csv(out / "metricas_participantes.csv", index=False)
    values = np.asarray([x["ba"] for x in people])
    rng = np.random.default_rng(20261024)
    boot = values[rng.integers(0, len(values), size=(2000, len(values)))].mean(axis=1)
    report = {
        "rows": len(test), "participants": len(people), "ba_macro": float(values.mean()),
        "ba_ci_descriptive": [float(np.quantile(boot, .025)), float(np.quantile(boot, .975))],
        "ba_global": float(balanced_accuracy_score(eval_frame.true, eval_frame.prediction)),
        "macro_f1": float(f1_score(eval_frame.true, eval_frame.prediction, average="macro", zero_division=0)),
        "predictions_sha256": digest(prediction_file), "models": len(model_files),
        "new_independent_sample": False, "external_construct_validation": False,
    }
    diagnosis = []
    for c in CLASSES:
        truth = eval_frame.true.eq(c)
        diagnosis.append({"class": c, "rows": int(truth.sum()),
                          "recall": float(eval_frame.loc[truth, "prediction"].eq(c).mean()),
                          "predicted_fraction": float(eval_frame.prediction.eq(c).mean())})
    pd.DataFrame(diagnosis).to_csv(out / "diagnostico_clases.csv", index=False)
    write_json(out / "resumen.json", report)
    print(json.dumps({"resumen": report, "clases": diagnosis}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
