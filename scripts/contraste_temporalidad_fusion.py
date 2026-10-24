"""Contraste 2x2 de historial y fusion, exclusivamente en train original."""
from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone

import joblib
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import balanced_accuracy_score, f1_score
from threadpoolctl import threadpool_limits
from torch import nn

from baselines_estaticos import EEG, GSR, EYE, validate_partition
from control_historial import FEATURES, nested_folds
from recurrentes_grid_core import GridSequenceNet
from temporales_core import (
    ROOT, CLASSES, digest, history_indices, preprocessor, raw_predict,
    seed_all, write_json,
)

OUT = ROOT / "resultados" / "contraste_temporalidad_fusion_24-10-2026"
DATASET = ROOT / "resultados" / "modelado" / "dataset_modelado.csv"
PARTITION = ROOT / "resultados" / "modelado" / "particion_participantes.csv"
SOURCE = ROOT / "scripts" / "contraste_temporalidad_fusion.py"
SPECS = {
    "arousal": {"target": "arousal_label_6s", "modalities": {"pupil": FEATURES, "eye": EYE, "eeg": EEG}, "forbidden": GSR},
    "attention": {"target": "attention_label_equal", "modalities": {"eeg": EEG, "gsr": GSR}, "forbidden": FEATURES + EYE},
}
CONFIG = {"id": "fixed_tcn", "family": "TCN", "context": 8, "hidden": 32,
          "layers": 1, "lr": .001, "dropout": .1, "decay": .01, "batch": 256}
SEEDS = [20261024, 20261025]
SCOPES = ["E-R", "E-C", "T-R", "T-C"]
EPOCHS = 8


def frame_for(data: pd.DataFrame, task: str) -> pd.DataFrame:
    spec = SPECS[task]
    frame = data.loc[data.split.eq("train") & data[spec["target"]].notna()].copy()
    frame = frame.sort_values(["participant", "recording", "segment_id", "stimulus", "window_start_utc"])
    frame = frame.reset_index(drop=True)
    if set(frame.split) != {"train"} or frame.participant.nunique() != 25:
        raise ValueError("Particion de train inesperada")
    if not frame[spec["target"]].isin(CLASSES).all():
        raise ValueError("Etiquetas invalidas")
    columns = sum(spec["modalities"].values(), [])
    if set(columns) & set(spec["forbidden"]):
        raise ValueError("Circularidad entre profesor y estudiante")
    return frame


def sequences(prep, frame: pd.DataFrame, features: list[str], repeat: bool):
    values = prep.transform(frame[features]).astype(np.float32)
    indices, lengths = history_indices(frame, CONFIG["context"])
    x = np.zeros((len(frame), CONFIG["context"], values.shape[1]), np.float32)
    for i, count in enumerate(lengths):
        x[i, :count] = values[i] if repeat else values[indices[i, :count]]
    return x, lengths


def participant_weights(frame: pd.DataFrame, target: str) -> np.ndarray:
    groups = frame.groupby(["participant", target])[target].transform("size").to_numpy(float)
    classes = frame.groupby("participant")[target].transform("nunique").to_numpy(float)
    weights = 1 / (groups * classes)
    return weights / weights.mean()


def fit_model(fit: pd.DataFrame, target: str, features: list[str], seed: int, repeat: bool):
    seed_all(seed)
    torch.set_num_threads(2)
    prep = preprocessor().fit(fit[features])
    x, lengths = sequences(prep, fit, features, repeat)
    model = GridSequenceNet(x.shape[2], CONFIG)
    xx, ll = torch.from_numpy(x), torch.from_numpy(lengths)
    yy = torch.tensor(fit[target].map({c: i for i, c in enumerate(CLASSES)}).to_numpy(), dtype=torch.long)
    weights = torch.tensor(participant_weights(fit, target), dtype=torch.float32)
    optimizer = torch.optim.AdamW(model.parameters(), lr=CONFIG["lr"], weight_decay=CONFIG["decay"])
    curve = []
    for epoch in range(1, EPOCHS + 1):
        model.train()
        order = torch.randperm(len(fit))
        total = 0.
        for start in range(0, len(fit), CONFIG["batch"]):
            ix = order[start:start + CONFIG["batch"]]
            optimizer.zero_grad(set_to_none=True)
            loss = (nn.functional.cross_entropy(model(xx[ix], ll[ix]), yy[ix], reduction="none") * weights[ix]).mean()
            if not torch.isfinite(loss):
                raise ValueError("Perdida no finita")
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.)
            optimizer.step()
            total += float(loss.item()) * len(ix)
        curve.append({"epoch": epoch, "loss": total / len(fit)})
    bundle = {"state": {k: v.detach().clone() for k, v in model.state_dict().items()},
              "prep": prep, "config": CONFIG, "seed": seed, "repeat": repeat,
              "features": features, "input_features": x.shape[2]}
    return bundle, curve


def predict(bundle, frame: pd.DataFrame) -> np.ndarray:
    with torch.random.fork_rng(devices=[]):
        model = GridSequenceNet(bundle["input_features"], bundle["config"])
        model.load_state_dict(bundle["state"])
        x, lengths = sequences(bundle["prep"], frame, bundle["features"], bundle["repeat"])
        raw = raw_predict(model, x, lengths, batch=CONFIG["batch"])
        return torch.softmax(torch.from_numpy(raw), dim=1).numpy()


def run_task(out, frame, fold, task, scope, seed):
    name = f"{task}_fold{fold['fold']}_{scope}_{seed}"
    done = out / "tareas" / f"{name}.json"
    if done.exists():
        result = json.loads(done.read_text(encoding="utf-8"))
        if result["source_sha256"] != digest(SOURCE):
            raise ValueError(f"Fuente cambiada en {name}")
        for item in result["models"]:
            if digest(out / item["path"]) != item["sha256"]:
                raise ValueError(f"Modelo cambiado en {name}")
        if digest(out / result["predictions"]["path"]) != result["predictions"]["sha256"]:
            raise ValueError(f"Predicciones cambiadas en {name}")
        return result
    spec = SPECS[task]
    fit = frame.loc[frame.participant.isin(fold["fit"])].reset_index(drop=True)
    val = frame.loc[frame.participant.isin(fold["evaluation"])].reset_index(drop=True)
    if set(fit.participant) & set(val.participant):
        raise ValueError("Participantes compartidos")
    early = scope.startswith("E")
    repeat = scope.endswith("C")
    panels = {"early": sum(spec["modalities"].values(), [])} if early else spec["modalities"]
    scores, models, curves = [], [], {}
    started = time.monotonic()
    for modality, features in panels.items():
        bundle, curve = fit_model(fit, spec["target"], features, seed, repeat)
        rel = f"modelos/{name}_{modality}.joblib"
        path = out / rel
        joblib.dump(bundle, path, compress=3)
        original = predict(bundle, val)
        loaded = predict(joblib.load(path), val)
        np.testing.assert_array_equal(original, loaded)
        scores.append(loaded)
        models.append({"modality": modality, "path": rel, "sha256": digest(path)})
        curves[modality] = curve
    probability = np.mean(scores, axis=0)
    if not np.isfinite(probability).all() or not np.allclose(probability.sum(axis=1), 1, atol=1e-6):
        raise ValueError("Probabilidades invalidas")
    pred = np.asarray(CLASSES)[probability.argmax(axis=1)]
    table = val[["source_row", "participant", "window_start_utc"]].copy()
    table["true"] = val[spec["target"]].to_numpy()
    table["prediction"] = pred
    for i, c in enumerate(CLASSES):
        table[f"prob_{c}"] = probability[:, i]
    rel = f"predicciones/{name}.csv.gz"
    table.to_csv(out / rel, index=False, float_format="%.10g")
    result = {"task": task, "scope": scope, "seed": seed, "fold": fold["fold"],
              "fit": fold["fit"], "evaluation": fold["evaluation"], "rows": len(val),
              "source_sha256": digest(SOURCE), "models": models,
              "predictions": {"path": rel, "sha256": digest(out / rel)},
              "curves": curves, "seconds": time.monotonic() - started}
    write_json(done, result)
    return result


def person_scores(table):
    rows = []
    for person, group in table.groupby("participant", sort=True):
        truth = group.true.to_numpy()
        pred = group.prediction.to_numpy()
        score = np.mean([(pred[truth == c] == c).mean() for c in np.unique(truth)])
        rows.append({"participant": person, "ba": float(score)})
    return rows


def summarize(out, results):
    metrics, people, all_predictions = [], [], []
    for result in results:
        table = pd.read_csv(out / result["predictions"]["path"])
        if len(table) != result["rows"]:
            raise ValueError("Numero de predicciones cambiado")
        identity = {k: result[k] for k in ["task", "scope", "seed", "fold"]}
        score = person_scores(table)
        metrics.append({**identity, "ba_macro": float(np.mean([x["ba"] for x in score])),
                        "ba_global": float(balanced_accuracy_score(table.true, table.prediction)),
                        "macro_f1": float(f1_score(table.true, table.prediction, average="macro", zero_division=0))})
        people += [{**identity, **x} for x in score]
        table = table.assign(**identity)
        all_predictions.append(table)
    pd.DataFrame(metrics).to_csv(out / "metricas_folds.csv", index=False)
    persons = pd.DataFrame(people)
    persons.to_csv(out / "metricas_participantes.csv", index=False)
    prediction = pd.concat(all_predictions, ignore_index=True)
    prediction.to_csv(out / "predicciones_oof.csv.gz", index=False, float_format="%.10g")
    expected = len(SEEDS) * len(SCOPES)
    for task in SPECS:
        subset = prediction.loc[prediction.task.eq(task)]
        counts = subset.groupby("source_row").size()
        if counts.nunique() != 1 or int(counts.iloc[0]) != expected:
            raise ValueError(f"Cobertura OOF incompleta: {task}")
    grouped = persons.groupby(["task", "scope", "participant"], as_index=False).ba.mean()
    summary = grouped.groupby(["task", "scope"], as_index=False).ba.mean().rename(columns={"ba": "ba_macro"})
    summary.to_csv(out / "resumen.csv", index=False)
    comparisons = [("temporal_early", "E-R", "E-C"), ("fusion_history", "T-R", "E-R"),
                   ("temporal_late", "T-R", "T-C"), ("fusion_control", "T-C", "E-C")]
    contrasts = []
    for task in SPECS:
        wide = grouped.loc[grouped.task.eq(task)].pivot(index="participant", columns="scope", values="ba")
        if set(wide.columns) != set(SCOPES) or wide.isna().any().any() or len(wide) != 25:
            raise ValueError("Contrastes sin pareo completo")
        deltas = [(label, wide[a].to_numpy() - wide[b].to_numpy()) for label, a, b in comparisons]
        deltas.append(("interaction", (wide["T-R"] - wide["T-C"] - wide["E-R"] + wide["E-C"]).to_numpy()))
        for label, values in deltas:
            rng = np.random.default_rng(20261024)
            resampled = values[rng.integers(0, len(values), size=(2000, len(values)))].mean(axis=1)
            contrasts.append({"task": task, "contrast": label, "delta_ba": float(values.mean()),
                              "ci_low": float(np.quantile(resampled, .025)),
                              "ci_high": float(np.quantile(resampled, .975)),
                              "positive_participants": int((values > 0).sum())})
    pd.DataFrame(contrasts).to_csv(out / "contrastes.csv", index=False)
    diagnostics = []
    for (task, scope), group in prediction.groupby(["task", "scope"]):
        for c in CLASSES:
            truth = group.true.eq(c)
            diagnostics.append({"task": task, "scope": scope, "class": c,
                                "recall": float(group.loc[truth, "prediction"].eq(c).mean()),
                                "predicted_fraction": float(group.prediction.eq(c).mean())})
    pd.DataFrame(diagnostics).to_csv(out / "diagnostico_clases.csv", index=False)
    write_json(out / "verificacion.json",
               {"tasks": len(results), "models": sum(len(r["models"]) for r in results),
                "predictions": len(prediction), "source_sha256": digest(SOURCE),
                "dataset_sha256": digest(DATASET), "partition_sha256": digest(PARTITION),
                "train_only": True, "validation_evaluated": False, "test_evaluated": False})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUT))
    parser.add_argument("--limit", type=int, default=0, help="Solo para prueba de ejecucion y reanudacion")
    args = parser.parse_args()
    out = ROOT / args.output
    dataset_hash, partition_hash, source_hash = digest(DATASET), digest(PARTITION), digest(SOURCE)
    partition = pd.read_csv(PARTITION)
    data = pd.read_csv(DATASET)
    data["source_row"] = np.arange(len(data))
    validate_partition(data, partition)
    frames = {task: frame_for(data, task) for task in SPECS}
    folds = {task: nested_folds(frame) for task, frame in frames.items()}
    manifest = {"created_utc": datetime.now(timezone.utc).isoformat(), "specs": SPECS,
                "config": CONFIG, "seeds": SEEDS, "scopes": SCOPES, "epochs": EPOCHS,
                "folds": folds, "dataset_sha256": dataset_hash, "partition_sha256": partition_hash,
                "source_sha256": source_hash, "train_only": True,
                "validation_evaluated": False, "test_evaluated": False}
    if out.exists():
        previous = json.loads((out / "protocolo.json").read_text(encoding="utf-8"))
        manifest["created_utc"] = previous["created_utc"]
        if manifest != previous:
            raise ValueError("Protocolo o fuentes cambiados; no reanudar")
    else:
        out.mkdir(parents=True)
        for sub in ["modelos", "predicciones", "tareas"]:
            (out / sub).mkdir()
        write_json(out / "protocolo.json", manifest)
    tasks = [(task, fold, scope, seed) for task in SPECS for fold in folds[task]
             for seed in SEEDS for scope in SCOPES]
    completed = []
    with threadpool_limits(limits=2):
        for task, fold, scope, seed in tasks:
            result = run_task(out, frames[task], fold, task, scope, seed)
            completed.append(result)
            print(f"{len(completed)}/{len(tasks)} {task} fold={fold['fold']} {scope} seed={seed} {result['seconds']:.1f}s", flush=True)
            if args.limit and len(completed) >= args.limit:
                return
    summarize(out, completed)
    print("Contraste completado", flush=True)


if __name__ == "__main__":
    main()
