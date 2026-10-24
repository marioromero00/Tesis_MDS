"""Evalúa en test la selección PCA+CatBoost fijada con validation."""
from __future__ import annotations

import hashlib
import json

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import balanced_accuracy_score
from threadpoolctl import threadpool_limits

from experimentar_mejora_condicional_v2 import OUT, SOURCE, TASKS, make_inputs, model_for, score


def participant_comparison(frame: pd.DataFrame, target: str, baseline: np.ndarray,
                           combined: np.ndarray) -> dict:
    paired = []
    for person, positions in frame.groupby("participant").indices.items():
        y = frame.iloc[positions][target]
        base = balanced_accuracy_score(y, baseline[positions])
        pca = balanced_accuracy_score(y, combined[positions])
        paired.append({"participant": person, "baseline_ba": base, "pca_ba": pca,
                       "delta_ba": pca - base})
    rng = np.random.default_rng(20260822)
    deltas = np.asarray([row["delta_ba"] for row in paired])
    draws = rng.choice(deltas, size=(10000, len(deltas)), replace=True).mean(axis=1)
    return {"positive_participants": int((deltas > 0).sum()), "total_participants": len(deltas),
            "mean_participant_delta": float(deltas.mean()),
            "participant_bootstrap_ci95": [float(x) for x in np.quantile(draws, [0.025, 0.975])],
            "per_participant": paired}


def shuffle_within_stimulus(x: pd.DataFrame, frame: pd.DataFrame) -> pd.DataFrame:
    """Rompe asociación temporal señal-etiqueta sin cambiar persona ni estímulo."""
    x = x.copy()
    rng = np.random.default_rng(20260822)
    signal = [column for column in x if column != "stimulus"]
    for _, positions in frame.groupby(["participant", "stimulus"]).indices.items():
        x.loc[positions, signal] = x.loc[rng.permutation(positions), signal].to_numpy()
    return x


def run() -> None:
    data_path = SOURCE / "dataset_pca_senales.csv"
    data = pd.read_csv(data_path)
    val_predictions = pd.read_csv(OUT / "predicciones_validation.csv.gz")
    report = {"dataset_sha256": hashlib.sha256(data_path.read_bytes()).hexdigest(),
              "selection": "pca_catboost elegido en validation para ambas tareas; test exploratorio ya observado antes",
              "tasks": {}}
    test_preds = []
    for task, (target, modalities, eligible) in TASKS.items():
        frame = data.loc[data[eligible] & data.split.isin(["train", "validation", "test"])
                         & data[target].notna()].copy()
        train = frame.loc[frame.split.eq("train")].reset_index(drop=True)
        test = frame.loc[frame.split.eq("test")].reset_index(drop=True)
        predictions = {}
        model_paths = {}
        for kind in ["stimulus", "pca"]:
            x_train, x_test, transforms = make_inputs(train, test, modalities, kind,
                                                     return_transforms=True)
            model = model_for("catboost", x_train)
            model.fit(x_train, train[target], cat_features=["stimulus"])
            name = f"{kind}_catboost"
            model_path = OUT / f"{task}__{name}.joblib"
            bundle = {"model": model, "transforms": transforms, "modalities": modalities,
                      "signal_input": kind, "target": target}
            joblib.dump(bundle, model_path, compress=3)
            model_paths[name] = {"path": model_path.name,
                                 "sha256": hashlib.sha256(model_path.read_bytes()).hexdigest()}
            restored = joblib.load(model_path)
            pred = np.asarray(restored["model"].predict(x_test)).ravel()
            np.testing.assert_array_equal(pred, np.asarray(model.predict(x_test)).ravel())
            predictions[name] = pred
            if kind == "pca":
                shuffled = shuffle_within_stimulus(x_test, test)
                predictions["pca_shuffled"] = np.asarray(restored["model"].predict(shuffled)).ravel()
        base, combined = predictions["stimulus_catboost"], predictions["pca_catboost"]
        validation = val_predictions.loc[val_predictions.task.eq(task)]
        val_base = validation.loc[validation.model.eq("stimulus_catboost")].reset_index(drop=True)
        val_pca = validation.loc[validation.model.eq("pca_catboost")].reset_index(drop=True)
        if not val_base[["participant", "stimulus", "true"]].equals(
                val_pca[["participant", "stimulus", "true"]]):
            raise AssertionError("Predicciones de validation desalineadas")
        val_frame = val_base.rename(columns={"true": target})
        report["tasks"][task] = {
            "validation": {"baseline": score(val_frame, val_base.predicted.to_numpy(), target),
                           "pca": score(val_frame, val_pca.predicted.to_numpy(), target),
                           "paired": participant_comparison(val_frame, target,
                                                           val_base.predicted.to_numpy(),
                                                           val_pca.predicted.to_numpy())},
            "test": {"baseline": score(test, base, target),
                     "pca": score(test, combined, target),
                     "pca_shuffled": score(test, predictions["pca_shuffled"], target),
                     "paired": participant_comparison(test, target, base, combined)},
            "models": model_paths,
        }
        for name, pred in predictions.items():
            test_preds.append(pd.DataFrame({"task": task, "model": name,
                                            "participant": test.participant,
                                            "stimulus": test.stimulus,
                                            "true": test[target], "predicted": pred}))
        print(task, json.dumps(report["tasks"][task]["test"], ensure_ascii=False), flush=True)
    pd.concat(test_preds, ignore_index=True).to_csv(OUT / "predicciones_test.csv.gz",
                                                   compression="gzip", index=False)
    (OUT / "reporte_condicional.json").write_text(json.dumps(report, indent=2, ensure_ascii=False),
                                                  encoding="utf-8")


if __name__ == "__main__":
    with threadpool_limits(limits=2):
        run()
