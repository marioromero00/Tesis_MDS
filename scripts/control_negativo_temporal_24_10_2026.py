"""Control negativo: desplazar solo etiquetas de ajuste dentro de cada persona."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits

from ablacion_pca_core import feature_cache, fit, inputs, predict
from entrenar_hiperparametros import load_train
from hiperparametros_core import FULL, TARGET
from temporales_core import ROOT, CLASSES, digest, write_json

SOURCE = ROOT / "scripts/control_negativo_temporal_24_10_2026.py"
PROTOCOL = ROOT / "documentacion/Protocolo_Control_Negativo_Temporal_24-10-2026.md"
ABL = ROOT / "resultados/ablacion_pca_12-09-2026"
DATASET = ROOT / "resultados/modelado/dataset_modelado.csv"
PARTITION = ROOT / "resultados/modelado/particion_participantes.csv"
OUT = ROOT / "resultados/control_negativo_temporal_24-10-2026"
VARIANT = "drop_fixation_count"
REPS = 12
MIN_SHIFT = 120
SEED = 20261024


def person_ba(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for person, group in frame.groupby("participant", sort=True):
        y = group.true.to_numpy()
        p = group.prediction.to_numpy()
        present = [c for c in CLASSES if (y == c).any()]
        rows.append({"participant": person, "rows": len(group),
                     "classes_present": len(present),
                     "ba": float(np.mean([(p[y == c] == c).mean() for c in present]))})
    return pd.DataFrame(rows)


def shifted_labels(frame: pd.DataFrame, rng: np.random.Generator):
    result = frame[TARGET].to_numpy().copy()
    shifts = []
    for participant, indices in frame.groupby("participant", sort=True).indices.items():
        group = frame.iloc[indices]
        if group.recording.nunique() != 1 or len(group) < 2 * MIN_SHIFT + 1:
            raise ValueError(f"Registro demasiado corto o ambiguo: {participant}")
        if not group.window_start_utc.is_monotonic_increasing:
            raise ValueError(f"Tiempo desordenado: {participant}")
        offset = int(rng.integers(MIN_SHIFT, len(group) - MIN_SHIFT + 1))
        original = frame.iloc[indices][TARGET].to_numpy()
        rotated = np.roll(original, offset)
        np.testing.assert_array_equal(np.sort(original), np.sort(rotated))
        result[indices] = rotated
        shifts.append({"participant": participant, "recording": group.recording.iloc[0],
                       "rows": len(group), "shift_rows": offset})
    if np.array_equal(result, frame[TARGET].to_numpy()):
        raise ValueError("El control no modifico etiquetas")
    return result, shifts


def score_frame(fold, val: pd.DataFrame, probability: np.ndarray, repetition: int):
    result = val[["source_row", "participant", "window_start_utc"]].copy()
    result["fold"] = fold
    result["repetition"] = repetition
    result["true"] = val[TARGET].to_numpy()
    result["prediction"] = np.asarray(CLASSES)[probability.argmax(axis=1)]
    for i, c in enumerate(CLASSES):
        result[f"prob_{c}"] = probability[:, i]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUT))
    args = parser.parse_args()
    out = ROOT / args.output
    paths = [SOURCE, PROTOCOL, DATASET, PARTITION, ABL / "protocolo.json",
             ABL / "catalogo_modelos.json", ABL / "predicciones_oof.csv.gz"]
    manifest = {"created_utc": datetime.now(timezone.utc).isoformat(),
                "sources_sha256": {str(p.relative_to(ROOT)): digest(p) for p in paths},
                "variant": VARIANT, "target": TARGET, "repetitions": REPS,
                "min_shift_rows": MIN_SHIFT, "seed": SEED,
                "validation_evaluated": False, "test_evaluated": False,
                "new_independent_sample": False, "external_construct_validation": False}
    if out.exists():
        old = json.loads((out / "protocolo.json").read_text(encoding="utf-8"))
        manifest["created_utc"] = old["created_utc"]
        if old != manifest:
            if {p.name for p in out.iterdir()} == {"protocolo.json"}:
                write_json(out / "protocolo_intento_invalido.json",
                           {**old, "aborted_reason": "suposicion erronea de especificaciones identicas entre folds; sin ajustes de control"})
                manifest["created_utc"] = datetime.now(timezone.utc).isoformat()
                write_json(out / "protocolo.json", manifest)
            else:
                raise ValueError("Fuente o protocolo cambiados")
    else:
        out.mkdir(parents=True)
        write_json(out / "protocolo.json", manifest)
    protocol = json.loads((ABL / "protocolo.json").read_text(encoding="utf-8"))
    catalog = json.loads((ABL / "catalogo_modelos.json").read_text(encoding="utf-8"))
    catalog = {x["fold"]: x for x in catalog if x["variant"] == VARIANT}
    if len(catalog) != 5 or len(protocol["folds"]) != 5:
        raise ValueError("Folds originales incompletos")
    if [(catalog[i]["spec"]["representation"], catalog[i]["spec"]["smoothing"])
            for i in range(1, 6)] != [("current", 32), ("multiscale", 8), ("delayed4", 32),
                                       ("multiscale", 8), ("relative", 1)]:
        raise ValueError("Representaciones originales inesperadas")
    if any(x["spec"]["alpha"] != 1.0 for x in catalog.values()):
        raise ValueError("Alpha original inesperada")
    if any(c.startswith("gsr_") for x in catalog.values() for c in x["spec"]["variant"]["keep"]) or any(c.startswith("gsr_") for c in FULL):
        raise ValueError("Entrada GSR invalida")
    train = load_train()
    if len(train) != 13524 or train.participant.nunique() != 25:
        raise ValueError("Train original inesperado")
    old_predictions = pd.read_csv(ABL / "predicciones_oof.csv.gz")
    old_predictions = old_predictions.loc[old_predictions.variant.eq(VARIANT)]
    if len(old_predictions) != len(train) or old_predictions.source_row.duplicated().any():
        raise ValueError("Predicciones antiguas incompletas")
    fold_frames = []
    clean = []
    with threadpool_limits(limits=2):
        for fold in protocol["folds"]:
            number = fold["fold"]
            spec = catalog[number]["spec"]
            fit_frame = train.loc[train.participant.isin(fold["fit"])].reset_index(drop=True)
            val = train.loc[train.participant.isin(fold["evaluation"])].reset_index(drop=True)
            if set(fit_frame.participant) & set(val.participant):
                raise ValueError("Fuga de participantes")
            if sorted(fit_frame.participant.unique()) != sorted(catalog[number]["train_participants"]):
                raise ValueError("Participantes de ajuste cambiados")
            fit_cache = feature_cache(fit_frame)
            val_cache = feature_cache(val)
            bundle = fit(inputs(fit_cache, spec), fit_frame, spec)
            probability = predict(bundle, val, val_cache)
            stored = old_predictions.loc[old_predictions.fold.eq(number)]
            np.testing.assert_array_equal(val.source_row, stored.source_row)
            np.testing.assert_allclose(probability, stored[[f"prob_{c}" for c in CLASSES]].to_numpy(),
                                       rtol=1e-10, atol=1e-10)
            clean.append(score_frame(number, val, probability, -1))
            fold_frames.append((number, spec, fit_frame, val, fit_cache, val_cache))
            print(f"Fold {number}/5 limpio reproducido", flush=True)
        clean = pd.concat(clean, ignore_index=True)
        clean.to_csv(out / "predicciones_limpias_reproducidas.csv.gz", index=False, float_format="%.12g")
        controls = []
        shifts = []
        for repetition in range(REPS):
            rng = np.random.default_rng(SEED + repetition)
            for number, spec, fit_frame, val, fit_cache, val_cache in fold_frames:
                labels, offsets = shifted_labels(fit_frame, rng)
                surrogate = fit_frame.copy()
                surrogate[TARGET] = labels
                bundle = fit(inputs(fit_cache, spec), surrogate, spec)
                probability = predict(bundle, val, val_cache)
                controls.append(score_frame(number, val, probability, repetition))
                shifts.extend(dict(repetition=repetition, fold=number, **row) for row in offsets)
            print(f"Control {repetition + 1}/{REPS} completado", flush=True)
    controls = pd.concat(controls, ignore_index=True)
    if len(controls) != REPS * len(clean):
        raise ValueError("Predicciones de control incompletas")
    controls.to_csv(out / "predicciones_control.csv.gz", index=False, float_format="%.12g")
    pd.DataFrame(shifts).to_csv(out / "desplazamientos.csv", index=False)
    clean_people = person_ba(clean)
    clean_people.to_csv(out / "metricas_personas_limpio.csv", index=False)
    all_people = []
    all_reps = []
    for repetition, frame in controls.groupby("repetition", sort=True):
        people = person_ba(frame)
        all_people.append(people.assign(repetition=repetition))
        all_reps.append({"repetition": int(repetition), "ba_macro": float(people.ba.mean()),
                         "min_ba_person": float(people.ba.min()),
                         "max_ba_person": float(people.ba.max())})
    null_people = pd.concat(all_people, ignore_index=True)
    null_people.to_csv(out / "metricas_personas_control.csv", index=False)
    pd.DataFrame(all_reps).to_csv(out / "metricas_repeticiones.csv", index=False)
    mean_null_person = null_people.groupby("participant").ba.mean().reindex(clean_people.participant).to_numpy()
    differences = clean_people.ba.to_numpy() - mean_null_person
    rng = np.random.default_rng(SEED)
    boot = differences[rng.integers(0, len(differences), size=(5000, len(differences)))].mean(axis=1)
    null_ba = np.asarray([row["ba_macro"] for row in all_reps])
    report = {"clean_ba_macro": float(clean_people.ba.mean()),
              "null_ba_mean": float(null_ba.mean()), "null_ba_range": [float(null_ba.min()), float(null_ba.max())],
              "null_ba_quantile_descriptive": [float(np.quantile(null_ba, .025)), float(np.quantile(null_ba, .975))],
              "clean_minus_mean_null": float(differences.mean()),
              "difference_people_ci_descriptive": [float(np.quantile(boot, .025)), float(np.quantile(boot, .975))],
              "people_clean_above_mean_null": int((differences > 0).sum()),
              "null_repetitions_at_or_above_clean": int((null_ba >= clean_people.ba.mean()).sum()),
              "repetitions": REPS, "models_retrained": 5 * (REPS + 1),
              "rows_per_repetition": len(clean), "clean_predictions_sha256": digest(out / "predicciones_limpias_reproducidas.csv.gz"),
              "control_predictions_sha256": digest(out / "predicciones_control.csv.gz"),
              "interpretation": "Control interno retrospectivo; no valida constructo ni confirma generalizacion nueva"}
    write_json(out / "resumen.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
