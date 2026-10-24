"""Evalúa el intento de un PC por señal elegido en validation."""
from __future__ import annotations

import json

import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits

from experimentar_mejora_condicional_v2 import OUT, SOURCE, TASKS, make_inputs, model_for, score
from verificar_mejora_condicional_v2 import participant_comparison, shuffle_within_stimulus


def run() -> None:
    data = pd.read_csv(SOURCE / "dataset_pca_senales.csv")
    choices = {"attention": "logistic", "arousal": "catboost"}
    report = {"selection": "1 PC por modalidad; algoritmo de mejor validation entre logística y CatBoost; test exploratorio reiterado",
              "tasks": {}}
    for task, (target, modalities, eligible) in TASKS.items():
        frame = data.loc[data[eligible] & data.split.isin(["train", "test"])
                         & data[target].notna()].copy()
        train = frame.loc[frame.split.eq("train")].reset_index(drop=True)
        test = frame.loc[frame.split.eq("test")].reset_index(drop=True)
        algo = choices[task]
        preds = {}
        for kind in ["stimulus", "pca_one"]:
            x_train, x_test, transforms = make_inputs(train, test, modalities, kind,
                                                      return_transforms=True)
            model = model_for(algo, x_train)
            model.fit(x_train, train[target], **({"cat_features": ["stimulus"]} if algo == "catboost" else {}))
            name = f"{task}__{kind}_{algo}"
            joblib.dump({"model": model, "transforms": transforms, "modalities": modalities,
                         "target": target}, OUT / f"{name}.joblib", compress=3)
            preds[kind] = np.asarray(model.predict(x_test)).ravel()
            if kind == "pca_one":
                preds["pca_shuffled"] = np.asarray(model.predict(
                    shuffle_within_stimulus(x_test, test))).ravel()
        report["tasks"][task] = {"algorithm": algo,
                                 "baseline": score(test, preds["stimulus"], target),
                                 "pca_one": score(test, preds["pca_one"], target),
                                 "pca_shuffled": score(test, preds["pca_shuffled"], target),
                                 "paired": participant_comparison(test, target,
                                                                  preds["stimulus"], preds["pca_one"])}
        print(task, {key: value["balanced_accuracy"] for key, value in report["tasks"][task].items()
                     if isinstance(value, dict) and "balanced_accuracy" in value}, flush=True)
    (OUT / "reporte_un_pc.json").write_text(json.dumps(report, indent=2, ensure_ascii=False),
                                            encoding="utf-8")


if __name__ == "__main__":
    with threadpool_limits(limits=2):
        run()
