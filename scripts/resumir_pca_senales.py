"""Resume reducción y cambios pareados entre modelos del nuevo pipeline PCA."""
from pathlib import Path
import json
import argparse

import numpy as np
import pandas as pd

from generar_pseudoetiquetas_pca_senales import normalized_inputs

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "resultados/pca_senales_v2_24-10-2026"


def participant_ba(group: pd.DataFrame) -> float:
    y = group["true"].to_numpy()
    pred = group.predicted.to_numpy()
    return float(np.mean([(pred[y == cls] == cls).mean() for cls in np.unique(y)]))


def main(output: Path = OUT) -> None:
    predictions = pd.read_csv(output / "predicciones_estudiante.csv.gz")
    rows = []
    for (task, split), group in predictions.groupby(["task", "split"]):
        person = group.groupby(["participant", "model"]).apply(participant_ba, include_groups=False).unstack()
        for model in ["pca_logistic", "pca_1pc_logistic"]:
            delta = (person[model] - person["full_logistic"]).to_numpy()
            rng = np.random.default_rng(20261024)
            sample = rng.choice(delta, size=(10000, len(delta)), replace=True).mean(axis=1)
            low, high = np.quantile(sample, [0.025, 0.975])
            rows.append({"task": task, "split": split, "model_minus_full": model,
                         "participant_mean_delta": float(delta.mean()),
                         "ci_low": float(low), "ci_high": float(high),
                         "positive_people": int((delta > 0).sum()), "participants": len(delta)})
    result = pd.DataFrame(rows)
    result.to_csv(output / "ganancias_pca.csv", index=False)

    source = pd.read_csv(ROOT / "resultados/preprocesamiento/caracteristicas_multimodales.csv")
    historical = pd.read_csv(ROOT / "resultados/modelado_auditado_24-10-2026/dataset_modelado.csv")
    corrected_pupil = normalized_inputs(source, ["pupil_mean_z"]).pupil_mean_z
    valid = historical.eligible_attention & historical.split.isin(["train", "validation", "test"])
    mismatch = ~np.isclose(historical.attention_pupil_component, corrected_pupil, rtol=0, atol=1e-6, equal_nan=True)
    audit = {"primary_valid_rows": int(valid.sum()),
             "historical_pupil_component_mismatched_rows": int((valid & mismatch).sum()),
             "cause": "groupby.apply ordenó participantes lexicográficamente y reset_index reasignó valores a otras filas",
             "historical_results_comparable": False}
    (output / "desalineacion_historica.json").write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")
    print(result.to_string(index=False))
    print(json.dumps(audit, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(ROOT / "config/pca_senales_v2.json"))
    args = parser.parse_args()
    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    main(ROOT / config["output_dir"])
