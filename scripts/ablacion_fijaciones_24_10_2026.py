"""Contraste fijo: quitar conjuntamente las cuatro variables de fijacion."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone

import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits

from ablacion_pca_core import design, feature_cache, fit, inputs, predict
from entrenar_hiperparametros import load_train
from hiperparametros_core import FULL, TARGET
from temporales_core import ROOT, CLASSES, digest, individual_scores, write_json

SOURCE = ROOT / "scripts" / "ablacion_fijaciones_24_10_2026.py"
OLD = ROOT / "resultados" / "ablacion_pca_12-09-2026"
OUT = ROOT / "resultados" / "ablacion_fijaciones_24-10-2026"
REMOVED = ["fixation_count", "fixation_total_ms", "fixation_mean_ms", "fixation_median_ms"]
REFERENCE = "drop_fixation_count"
VARIANT = {"variant": "drop_fixation_group", "kind": "group", "removed": REMOVED,
           "keep": [x for x in FULL if x not in REMOVED]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUT))
    args = parser.parse_args()
    out = ROOT / args.output
    old_protocol = json.loads((OLD / "protocolo.json").read_text(encoding="utf-8"))
    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": digest(SOURCE),
        "old_protocol_sha256": digest(OLD / "protocolo.json"),
        "old_catalog_sha256": digest(OLD / "catalogo_modelos.json"),
        "old_predictions_sha256": digest(OLD / "predicciones_oof.csv.gz"),
        "old_verification_sha256": digest(OLD / "verificacion.json"),
        "dataset_sha256": digest(ROOT / "resultados/modelado/dataset_modelado.csv"),
        "partition_sha256": digest(ROOT / "resultados/modelado/particion_participantes.csv"),
        "reference": REFERENCE, "variant": VARIANT,
        "comparison": "BA macro de grupo sin fijaciones menos Ridge sin fixation_count",
        "no_new_hyperparameter_selection": True,
        "validation_evaluated": False, "test_evaluated": False,
    }
    if out.exists():
        previous = json.loads((out / "protocolo.json").read_text(encoding="utf-8"))
        manifest["created_utc"] = previous["created_utc"]
        if manifest != previous:
            raise ValueError("Protocolo cambiado")
    else:
        out.mkdir(parents=True)
        (out / "modelos").mkdir()
        write_json(out / "protocolo.json", manifest)
    data = load_train()
    old_predictions = pd.read_csv(OLD / "predicciones_oof.csv.gz")
    old_predictions = old_predictions.loc[old_predictions.variant.eq(REFERENCE)]
    catalog, rows, people = [], [], []
    references = {x["fold"]: x for x in old_protocol["references"]}
    with threadpool_limits(limits=2):
        for fold in old_protocol["folds"]:
            fit_frame = data.loc[data.participant.isin(fold["fit"])].reset_index(drop=True)
            val = data.loc[data.participant.isin(fold["evaluation"])].reset_index(drop=True)
            if set(fit_frame.participant) & set(val.participant):
                raise ValueError("Participantes compartidos")
            spec = design(references[fold["fold"]], VARIANT)
            name = f"fold{fold['fold']}_drop_fixation_group"
            path = out / "modelos" / f"{name}.joblib"
            if path.exists():
                bundle = joblib.load(path)
                if bundle["spec"] != spec:
                    raise ValueError("Especificacion cambiada")
            else:
                fit_cache = feature_cache(fit_frame)
                bundle = fit(inputs(fit_cache, spec), fit_frame, spec)
                joblib.dump(bundle, path, compress=3)
            # La inferencia no recibe objetivo ni GSR, la fuente de la etiqueta.
            blind = val.drop(columns=[TARGET, "arousal_score_6s", *[c for c in val if c.startswith("gsr_")]], errors="ignore")
            group_probability = predict(joblib.load(path), blind)
            reference = old_predictions.loc[old_predictions.fold.eq(fold["fold"])].reset_index(drop=True)
            np.testing.assert_array_equal(reference.source_row, val.source_row)
            if not (reference.true.to_numpy() == val[TARGET].to_numpy()).all():
                raise ValueError("Etiquetas de referencia desalineadas")
            ref_probability = reference[[f"prob_{c}" for c in CLASSES]].to_numpy(float)
            result = val[["source_row", "participant", "window_start_utc", TARGET]].copy().rename(columns={TARGET: "true"})
            result["fold"] = fold["fold"]
            result["prediction_group"] = np.asarray(CLASSES)[group_probability.argmax(axis=1)]
            result["prediction_reference"] = np.asarray(CLASSES)[ref_probability.argmax(axis=1)]
            for i, c in enumerate(CLASSES):
                result[f"prob_{c}_group"] = group_probability[:, i]
            rows.append(result)
            for mode in ["group", "reference"]:
                table = result[["participant", "true", f"prediction_{mode}"]].rename(columns={f"prediction_{mode}": "prediction"})
                people += [{"fold": fold["fold"], "mode": mode, **row} for row in
                           [{"participant": p, "score": s} for p, s in individual_scores(table, "true", table.prediction.to_numpy(), "classification").items()]]
            catalog.append({"fold": fold["fold"], "path": str(path.relative_to(out)).replace("\\", "/"),
                            "sha256": digest(path), "spec": spec, "fit": fold["fit"],
                            "evaluation": fold["evaluation"]})
            print(f"fold {fold['fold']}/5 completado", flush=True)
    write_json(out / "catalogo_modelos.json", catalog)
    all_rows = pd.concat(rows, ignore_index=True)
    all_rows.to_csv(out / "predicciones_oof.csv.gz", index=False, float_format="%.10g")
    pd.DataFrame(people).to_csv(out / "metricas_participantes.csv", index=False)
    wide = pd.DataFrame(people).pivot(index="participant", columns="mode", values="score")
    delta = (wide.group - wide.reference).to_numpy()
    rng = np.random.default_rng(20261028)
    samples = delta[rng.integers(0, len(delta), size=(2000, len(delta)))].mean(axis=1)
    summary = {"ba_reference": float(wide.reference.mean()), "ba_group": float(wide.group.mean()),
               "delta_ba": float(delta.mean()), "ci_low": float(np.quantile(samples, .025)),
               "ci_high": float(np.quantile(samples, .975)), "positive_participants": int((delta > 0).sum()),
               "models": len(catalog), "predictions": len(all_rows)}
    for mode in ["reference", "group"]:
        for c in CLASSES:
            subset = all_rows.loc[all_rows.true.eq(c)]
            summary[f"recall_{c}_{mode}"] = float(subset[f"prediction_{mode}"].eq(c).mean())
    write_json(out / "resumen.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
