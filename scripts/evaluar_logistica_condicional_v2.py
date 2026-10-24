"""Reintento conservador con regresión logística y validación por participante."""
from __future__ import annotations

import json

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold
from threadpoolctl import threadpool_limits

from experimentar_mejora_condicional_v2 import OUT, SOURCE, TASKS, make_inputs, model_for, score
from verificar_mejora_condicional_v2 import participant_comparison, shuffle_within_stimulus


def fit_predict(train: pd.DataFrame, evaluate: pd.DataFrame, target: str,
                modalities: dict, kind: str):
    x_train, x_evaluate, transforms = make_inputs(train, evaluate, modalities, kind,
                                                  return_transforms=True)
    model = model_for("logistic", x_train)
    model.fit(x_train, train[target])
    pred = model.predict(x_evaluate)
    return model, transforms, x_evaluate, pred


def run() -> None:
    data = pd.read_csv(SOURCE / "dataset_pca_senales.csv")
    report = {"protocol": "C=0.3 fijo; GroupKFold(5) en train; ajuste final solo train; test exploratorio", "tasks": {}}
    for task, (target, modalities, eligible) in TASKS.items():
        frame = data.loc[data[eligible] & data.split.isin(["train", "validation", "test"])
                         & data[target].notna()].copy()
        train = frame.loc[frame.split.eq("train")].reset_index(drop=True)
        results = {}
        for fold, (ia, ib) in enumerate(GroupKFold(5).split(train, train[target], train.participant)):
            a, b = train.iloc[ia].reset_index(drop=True), train.iloc[ib].reset_index(drop=True)
            row = {"fold": fold}
            for kind in ["stimulus", "pca"]:
                _, _, _, pred = fit_predict(a, b, target, modalities, kind)
                row[kind] = score(b, pred, target)
            results[f"fold_{fold}"] = row
        results["cv_mean_delta_ba"] = float(np.mean([
            row["pca"]["balanced_accuracy"] - row["stimulus"]["balanced_accuracy"]
            for row in results.values()]))
        for split in ["validation", "test"]:
            part = frame.loc[frame.split.eq(split)].reset_index(drop=True)
            preds = {}
            for kind in ["stimulus", "pca"]:
                model, transforms, x_part, pred = fit_predict(train, part, target, modalities, kind)
                preds[kind] = pred
                if split == "test":
                    joblib.dump({"model": model, "transforms": transforms,
                                 "modalities": modalities, "target": target},
                                OUT / f"{task}__{kind}_logistic.joblib", compress=3)
                if kind == "pca":
                    shuffled = shuffle_within_stimulus(x_part, part)
                    preds["pca_shuffled"] = model.predict(shuffled)
            results[split] = {
                "stimulus": score(part, preds["stimulus"], target),
                "pca": score(part, preds["pca"], target),
                "pca_shuffled": score(part, preds["pca_shuffled"], target),
                "paired": participant_comparison(part, target, preds["stimulus"], preds["pca"]),
            }
            pd.DataFrame({"participant": part.participant, "stimulus": part.stimulus,
                          "true": part[target], "baseline": preds["stimulus"],
                          "pca": preds["pca"], "pca_shuffled": preds["pca_shuffled"]}).to_csv(
                              OUT / f"{task}__{split}_logistic_predictions.csv.gz", index=False,
                              compression="gzip")
        report["tasks"][task] = results
        print(task, "CV delta", results["cv_mean_delta_ba"],
              "val", results["validation"]["pca"]["balanced_accuracy"],
              "test", results["test"]["pca"]["balanced_accuracy"], flush=True)
    (OUT / "reporte_logistica.json").write_text(json.dumps(report, indent=2, ensure_ascii=False),
                                                encoding="utf-8")


if __name__ == "__main__":
    with threadpool_limits(limits=2):
        run()
