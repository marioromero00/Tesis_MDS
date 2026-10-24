"""Mezcla fija de Ridge sin fixation_count y TCN temprano con historial."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from contraste_temporalidad_fusion import ROOT, OUT as TCN, DATASET, PARTITION, CLASSES, digest, person_scores, write_json

ABL = ROOT / "resultados" / "ablacion_pca_12-09-2026"
OUT = ROOT / "resultados" / "mezcla_ridge_tcn_24-10-2026"
SOURCE = ROOT / "scripts" / "mezcla_ridge_tcn_24_10_2026.py"
RIDGE_WEIGHT = .75
TCN_WEIGHT = .25
VARIANT = "drop_fixation_count"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUT))
    args = parser.parse_args()
    out = ROOT / args.output
    if digest(DATASET) != json.loads((TCN / "protocolo.json").read_text(encoding="utf-8"))["dataset_sha256"]:
        raise ValueError("Dataset cambiado")
    if digest(PARTITION) != json.loads((TCN / "protocolo.json").read_text(encoding="utf-8"))["partition_sha256"]:
        raise ValueError("Particion cambiada")
    if not (TCN / "auditoria_independiente.json").exists() or not (ABL / "verificacion.json").exists():
        raise ValueError("Falta auditoria fuente")
    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": digest(SOURCE), "dataset_sha256": digest(DATASET),
        "partition_sha256": digest(PARTITION),
        "ridge_predictions_sha256": digest(ABL / "predicciones_oof.csv.gz"),
        "tcn_predictions_sha256": digest(TCN / "predicciones_oof.csv.gz"),
        "ridge_audit_sha256": digest(ABL / "verificacion.json"),
        "tcn_audit_sha256": digest(TCN / "auditoria_independiente.json"),
        "ridge_variant": VARIANT, "tcn_scope": "E-R",
        "ridge_weight": RIDGE_WEIGHT, "tcn_weight": TCN_WEIGHT,
        "primary": "BA macro de mezcla menos Ridge sin fixation_count",
        "secondary": "BA macro de mezcla menos TCN E-R; recall de medio",
        "validation_evaluated": False, "test_evaluated": False,
    }
    if out.exists():
        previous = json.loads((out / "protocolo.json").read_text(encoding="utf-8"))
        manifest["created_utc"] = previous["created_utc"]
        if manifest != previous:
            raise ValueError("Protocolo o fuentes cambiados")
    else:
        out.mkdir(parents=True)
        write_json(out / "protocolo.json", manifest)
    ridge = pd.read_csv(ABL / "predicciones_oof.csv.gz")
    ridge = ridge.loc[ridge.variant.eq(VARIANT)].copy()
    tcn = pd.read_csv(TCN / "predicciones_oof.csv.gz")
    tcn = tcn.loc[tcn.task.eq("arousal") & tcn.scope.eq("E-R")].copy()
    if len(ridge) != 13524 or len(tcn) != 27048:
        raise ValueError("Cobertura fuente inesperada")
    if ridge.source_row.duplicated().any() or tcn.duplicated(["source_row", "seed"]).any():
        raise ValueError("Predicciones fuente duplicadas")
    combined = tcn.merge(
        ridge[["source_row", "participant", "true"] + [f"prob_{c}" for c in CLASSES]],
        on="source_row", how="inner", validate="many_to_one", suffixes=("_tcn", "_ridge"),
    )
    if len(combined) != len(tcn):
        raise ValueError("Predicciones sin correspondencia")
    if not (combined.participant_tcn == combined.participant_ridge).all():
        raise ValueError("Participantes desalineados")
    if not (combined.true_tcn == combined.true_ridge).all():
        raise ValueError("Etiquetas desalineadas")
    p_ridge = combined[[f"prob_{c}_ridge" for c in CLASSES]].to_numpy(float)
    p_tcn = combined[[f"prob_{c}_tcn" for c in CLASSES]].to_numpy(float)
    p_mix = RIDGE_WEIGHT * p_ridge + TCN_WEIGHT * p_tcn
    if not np.isfinite(p_mix).all() or not np.allclose(p_mix.sum(axis=1), 1, atol=1e-6):
        raise ValueError("Probabilidades invalidas")
    result = combined[["source_row", "seed", "fold", "window_start_utc"]].copy()
    result["participant"] = combined.participant_tcn
    result["true"] = combined.true_tcn
    for mode, p in [("ridge", p_ridge), ("tcn", p_tcn), ("mezcla", p_mix)]:
        result[f"prediction_{mode}"] = np.asarray(CLASSES)[p.argmax(axis=1)]
    for i, c in enumerate(CLASSES):
        result[f"prob_{c}"] = p_mix[:, i]
    result.to_csv(out / "predicciones_oof.csv.gz", index=False, float_format="%.10g")
    people = []
    for (seed, fold), group in result.groupby(["seed", "fold"]):
        for mode in ["ridge", "tcn", "mezcla"]:
            table = group[["participant", "true", f"prediction_{mode}"]].rename(columns={f"prediction_{mode}": "prediction"})
            people += [{"seed": seed, "fold": fold, "mode": mode, **row} for row in person_scores(table)]
    people = pd.DataFrame(people)
    people.to_csv(out / "metricas_participantes.csv", index=False)
    wide = people.groupby(["participant", "mode"], as_index=False).ba.mean().pivot(index="participant", columns="mode", values="ba")
    report = {"ba_ridge": float(wide.ridge.mean()), "ba_tcn": float(wide.tcn.mean()), "ba_mezcla": float(wide.mezcla.mean()),
              "predictions": len(result)}
    rng = np.random.default_rng(20261027)
    for reference in ["ridge", "tcn"]:
        delta = (wide.mezcla - wide[reference]).to_numpy()
        samples = delta[rng.integers(0, len(delta), size=(2000, len(delta)))].mean(axis=1)
        report[f"delta_vs_{reference}"] = float(delta.mean())
        report[f"ci_vs_{reference}"] = [float(np.quantile(samples, .025)), float(np.quantile(samples, .975))]
        report[f"positive_vs_{reference}"] = int((delta > 0).sum())
    for mode in ["ridge", "tcn", "mezcla"]:
        for c in CLASSES:
            group = result.loc[result.true.eq(c)]
            report[f"recall_{c}_{mode}"] = float(group[f"prediction_{mode}"].eq(c).mean())
    write_json(out / "resumen.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
