"""Figura de BA por persona para el informe de robustez."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "resultados/robustez_sin_cohorte_nueva_24-10-2026"
VARIANTS = [("gsr_6s", "GSR 6 s"), ("gsr_2s", "GSR 2 s"),
            ("pca_gsr", "PCA GSR")]
COLORS = ["#154c79", "#db7b2b", "#43866e"]


def main():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True, constrained_layout=True)
    for axis, split, title in zip(axes, ["train", "test"],
                                   ["Train: predicciones fuera de fold (25 personas)",
                                    "Test ya consultado: ensamble fijo (8 personas)"]):
        frame = pd.read_csv(OUT / f"personas_{split}.csv")
        baseline = frame.loc[frame.reference.eq("gsr_6s"), "constant_ba"].mean()
        axis.axhline(baseline, color="#5b626a", linestyle="--", linewidth=1.2,
                     label="Referencia 1/k" if split == "train" else None)
        for i, (variant, label) in enumerate(VARIANTS):
            group = frame.loc[frame.reference.eq(variant)].sort_values("participant")
            rng = np.random.default_rng(20261024 + i)
            jitter = rng.uniform(-.16, .16, len(group))
            axis.scatter(np.full(len(group), i) + jitter, group.ba, s=21,
                         color=COLORS[i], alpha=.62, linewidths=0)
            axis.scatter(i, group.ba.mean(), s=112, color=COLORS[i], marker="D",
                         edgecolors="white", linewidths=1.1, zorder=5)
        axis.set_xticks(range(3), [label for _, label in VARIANTS])
        axis.set_ylim(0, .65)
        axis.set_title(title, fontsize=10)
        axis.grid(axis="y", alpha=.2)
        axis.spines[["top", "right"]].set_visible(False)
        if split == "train":
            axis.legend(frameon=False, loc="upper right", fontsize=8)
    axes[0].set_ylabel("Balanced accuracy por participante")
    fig.suptitle("Sensibilidad a la regla de pseudoetiquetado", fontsize=13)
    fig.text(.5, -.015,
             "Cada punto es una persona; rombos = promedio. Modelo entrenado para GSR 6 s; etiquetas alternativas solo para sensibilidad.",
             ha="center", fontsize=8)
    for extension in ["png", "pdf"]:
        fig.savefig(OUT / f"robustez_participantes.{extension}", dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
