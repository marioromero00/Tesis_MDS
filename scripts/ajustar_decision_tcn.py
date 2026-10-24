"""Seleccion interna de suavizado causal y sesgo medio para TCN de activacion."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold
from threadpoolctl import threadpool_limits

from contraste_temporalidad_fusion import (
    ROOT, OUT as BASE, DATASET, PARTITION, SOURCE as BASE_SOURCE, SPECS,
    CLASSES, digest, fit_model, frame_for, person_scores, predict, write_json,
)
from temporales_core import history_indices

OUT = ROOT / "resultados" / "ajuste_decision_tcn_24-10-2026"
SOURCE = ROOT / "scripts" / "ajustar_decision_tcn.py"
TARGET = SPECS["arousal"]["target"]
FEATURES = sum(SPECS["arousal"]["modalities"].values(), [])
SMOOTHING = [1, 4, 8]
MEDIUM_BIAS = [1.0, 1.25, 1.5, 2.0]
INNER_SEED = 20261026


def adjust(frame, probabilities, smoothing, medium_bias):
    if smoothing not in SMOOTHING or medium_bias not in MEDIUM_BIAS:
        raise ValueError("Candidato no declarado")
    if smoothing == 1:
        smoothed = probabilities.copy()
    else:
        indices, lengths = history_indices(frame, smoothing)
        smoothed = np.asarray([
            probabilities[indices[i, :count]].mean(axis=0)
            for i, count in enumerate(lengths)
        ])
    weighted = smoothed * np.asarray([1., medium_bias, 1.])[None, :]
    return weighted / weighted.sum(axis=1, keepdims=True)


def score(frame, probabilities):
    table = frame[["participant"]].copy()
    table["true"] = frame[TARGET].to_numpy()
    table["prediction"] = np.asarray(CLASSES)[probabilities.argmax(axis=1)]
    return float(np.mean([row["ba"] for row in person_scores(table)]))


def inner_predictions(frame, fold, out):
    file = out / "internos" / f"fold{fold['fold']}.csv.gz"
    if file.exists():
        return pd.read_csv(file)
    fit = frame.loc[frame.participant.isin(fold["fit"])].reset_index(drop=True)
    splitter = GroupKFold(n_splits=4, shuffle=True, random_state=INNER_SEED + fold["fold"])
    rows = []
    for inner, (ii, vv) in enumerate(splitter.split(fit, groups=fit.participant), 1):
        train = fit.iloc[ii].reset_index(drop=True)
        held = fit.iloc[vv].reset_index(drop=True)
        if set(train.participant) & set(held.participant):
            raise ValueError("Fuga de participantes interna")
        bundle, curve = fit_model(train, TARGET, FEATURES, INNER_SEED, repeat=False)
        prob = predict(bundle, held)
        row = held[["source_row", "participant", "recording", "segment_id", "stimulus", "split", "window_start_utc", TARGET]].copy()
        row["inner_fold"] = inner
        for i, c in enumerate(CLASSES):
            row[f"prob_{c}"] = prob[:, i]
        rows.append(row)
        print(f"fold externo {fold['fold']} interno {inner}/4: {len(held)} ventanas", flush=True)
    saved = pd.concat(rows, ignore_index=True)
    if len(saved) != len(fit) or set(saved.source_row) != set(fit.source_row):
        raise ValueError("Cobertura OOF interna incompleta")
    saved.to_csv(file, index=False, float_format="%.12g")
    return pd.read_csv(file)


def choose(inner, fold):
    attempts = []
    for smoothing in SMOOTHING:
        for bias in MEDIUM_BIAS:
            parts = []
            for _, block in inner.groupby("inner_fold", sort=True):
                block = block.sort_values(["participant", "recording", "segment_id", "stimulus", "window_start_utc"]).reset_index(drop=True)
                p = block[[f"prob_{c}" for c in CLASSES]].to_numpy(float)
                parts.append((block, adjust(block, p, smoothing, bias)))
            full = pd.concat([block.assign(prediction=np.asarray(CLASSES)[p.argmax(axis=1)]) for block, p in parts])
            table = full[["participant", TARGET, "prediction"]].rename(columns={TARGET: "true"})
            value = float(np.mean([r["ba"] for r in person_scores(table)]))
            attempts.append({"fold": fold["fold"], "smoothing": smoothing, "medium_bias": bias, "ba_macro": value})
    ranking = sorted(attempts, key=lambda x: (-x["ba_macro"], x["smoothing"], x["medium_bias"]))
    return attempts, ranking[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUT))
    args = parser.parse_args()
    out = ROOT / args.output
    base_protocol = json.loads((BASE / "protocolo.json").read_text(encoding="utf-8"))
    if base_protocol["source_sha256"] != digest(BASE_SOURCE):
        raise ValueError("Fuente base cambiada")
    if base_protocol["dataset_sha256"] != digest(DATASET) or base_protocol["partition_sha256"] != digest(PARTITION):
        raise ValueError("Datos cambiados")
    base_audit = BASE / "auditoria_independiente.json"
    if not base_audit.exists():
        raise ValueError("Falta auditoria de la corrida base")
    manifest = {"created_utc": datetime.now(timezone.utc).isoformat(),
                "source_sha256": digest(SOURCE), "base_source_sha256": digest(BASE_SOURCE),
                "base_protocol_sha256": digest(BASE / "protocolo.json"),
                "base_audit_sha256": digest(base_audit), "dataset_sha256": digest(DATASET),
                "partition_sha256": digest(PARTITION), "target": TARGET, "features": FEATURES,
                "smoothing": SMOOTHING, "medium_bias": MEDIUM_BIAS, "inner_seed": INNER_SEED,
                "selection": "BA macro por participante en cuatro folds internos; empate: menor suavizado y sesgo",
                "comparison": "TCN E-R sin ajuste, mismos cinco folds y dos semillas",
                "validation_evaluated": False, "test_evaluated": False}
    if out.exists():
        previous = json.loads((out / "protocolo.json").read_text(encoding="utf-8"))
        manifest["created_utc"] = previous["created_utc"]
        if manifest != previous:
            raise ValueError("Protocolo cambiado")
    else:
        out.mkdir(parents=True)
        (out / "internos").mkdir()
        write_json(out / "protocolo.json", manifest)
    data = pd.read_csv(DATASET)
    data["source_row"] = np.arange(len(data))
    frame = frame_for(data, "arousal")
    folds = base_protocol["folds"]["arousal"]
    attempts, choices, predictions = [], [], []
    with threadpool_limits(limits=2):
        for fold in folds:
            inner = inner_predictions(frame, fold, out)
            trial, choice = choose(inner, fold)
            attempts += trial
            choices.append(choice)
            print(f"fold externo {fold['fold']} elegido: suavizado={choice['smoothing']} sesgo={choice['medium_bias']} BA interna={choice['ba_macro']:.4f}", flush=True)
    pd.DataFrame(attempts).to_csv(out / "intentos_internos.csv", index=False)
    write_json(out / "selecciones.json", choices)
    frozen = digest(out / "selecciones.json")
    for fold, choice in zip(folds, choices):
        val = frame.loc[frame.participant.isin(fold["evaluation"])].reset_index(drop=True)
        for seed in base_protocol["seeds"]:
            path = BASE / "predicciones" / f"arousal_fold{fold['fold']}_E-R_{seed}.csv.gz"
            task_path = BASE / "tareas" / f"arousal_fold{fold['fold']}_E-R_{seed}.json"
            task = json.loads(task_path.read_text(encoding="utf-8"))
            if digest(path) != task["predictions"]["sha256"]:
                raise ValueError("Predicciones base cambiadas")
            original = pd.read_csv(path)
            np.testing.assert_array_equal(original.source_row, val.source_row)
            p = original[[f"prob_{c}" for c in CLASSES]].to_numpy(float)
            adjusted = adjust(val, p, choice["smoothing"], choice["medium_bias"])
            row = original[["source_row", "participant", "window_start_utc", "true"]].copy()
            row["prediction_original"] = original.prediction
            row["prediction_ajustada"] = np.asarray(CLASSES)[adjusted.argmax(axis=1)]
            row["fold"] = fold["fold"]
            row["seed"] = seed
            for i, c in enumerate(CLASSES):
                row[f"prob_{c}"] = adjusted[:, i]
            predictions.append(row)
    full = pd.concat(predictions, ignore_index=True)
    full.to_csv(out / "predicciones_oof.csv.gz", index=False, float_format="%.10g")
    people = []
    for (seed, fold), group in full.groupby(["seed", "fold"]):
        for mode in ["original", "ajustada"]:
            table = group[["participant", "true", f"prediction_{mode}"]].rename(columns={f"prediction_{mode}": "prediction"})
            people.extend({"seed": seed, "fold": fold, "mode": mode, **r} for r in person_scores(table))
    people = pd.DataFrame(people)
    people.to_csv(out / "metricas_participantes.csv", index=False)
    wide = people.groupby(["participant", "mode"], as_index=False).ba.mean().pivot(index="participant", columns="mode", values="ba")
    delta = (wide["ajustada"] - wide["original"]).to_numpy()
    rng = np.random.default_rng(20261026)
    boots = delta[rng.integers(0, len(delta), size=(2000, len(delta)))].mean(axis=1)
    report = {"ba_original": float(wide["original"].mean()), "ba_ajustada": float(wide["ajustada"].mean()),
              "delta_ba": float(delta.mean()), "ci_low": float(np.quantile(boots, .025)),
              "ci_high": float(np.quantile(boots, .975)), "positive_participants": int((delta > 0).sum()),
              "selection_sha256": frozen, "predictions": len(full)}
    for mode in ["original", "ajustada"]:
        for c in CLASSES:
            subset = full.loc[full.true.eq(c)]
            report[f"recall_{c}_{mode}"] = float(subset[f"prediction_{mode}"].eq(c).mean())
    write_json(out / "resumen.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
