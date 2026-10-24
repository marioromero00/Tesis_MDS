"""Resume diferencias pareadas entre fusiones con remuestreo de participantes."""
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "resultados/fusion_pseudoetiquetas_24-10-2026"


def main() -> None:
    people = pd.read_csv(OUT / "metricas_participantes.csv")
    rng = np.random.default_rng(20261024)
    rows = []
    for (task, context, split), group in people.groupby(["task", "context", "split"]):
        scores = group.pivot(index="participant", columns="strategy", values="balanced_accuracy")
        for alternative in ["intermediate_pca90", "late_mean", "late_geometric"]:
            delta = (scores[alternative] - scores["early"]).to_numpy()
            samples = rng.choice(delta, size=(10000, len(delta)), replace=True).mean(axis=1)
            low, high = np.quantile(samples, [0.025, 0.975])
            rows.append({"task": task, "context": context, "split": split,
                         "contrast": f"{alternative}_minus_early", "mean_delta": float(delta.mean()),
                         "ci_low": float(low), "ci_high": float(high),
                         "positive_people": int((delta > 0).sum()), "participants": len(delta)})
    result = pd.DataFrame(rows)
    result.to_csv(OUT / "ganancias_pareadas.csv", index=False)
    print(result.loc[result.split.eq("test")].to_string(index=False))


if __name__ == "__main__":
    main()
