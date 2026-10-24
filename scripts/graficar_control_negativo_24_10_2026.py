"""Figura reproducible del control negativo temporal."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "resultados/control_negativo_temporal_24-10-2026"


def main():
    original = pd.read_csv(OUT / "metricas_personas_limpio.csv")
    controls = pd.read_csv(OUT / "metricas_personas_control.csv")
    repetitions = pd.read_csv(OUT / "metricas_repeticiones.csv")
    mean_null = controls.groupby("participant").ba.mean()
    people = original.assign(null=original.participant.map(mean_null))
    people = people.sort_values("ba").reset_index(drop=True)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), constrained_layout=True)
    ax = axes[0]
    ax.scatter(repetitions.repetition + 1, repetitions.ba_macro, color="#c37b2c", s=65, label="Etiquetas desplazadas")
    ax.axhline(original.ba.mean(), color="#205a7d", linewidth=2.2, label="Etiquetas originales")
    ax.axhline(repetitions.ba_macro.mean(), color="#c37b2c", linestyle="--", linewidth=1.5,
               label="Promedio de controles")
    ax.set(xlabel="Repetición de control", ylabel="BA promedio por persona", xticks=np.arange(1, 13),
           ylim=(.25, .44), title="Cinco folds, misma configuración por fold")
    ax.legend(frameon=False, fontsize=8)
    ax.grid(axis="y", alpha=.2)
    ax = axes[1]
    y = np.arange(len(people))
    ax.plot(np.c_[people.null, people.ba].T, np.vstack([y, y]), color="#a9aeb4", linewidth=.9)
    ax.scatter(people.null, y, color="#c37b2c", s=23, label="Control promedio", zorder=3)
    ax.scatter(people.ba, y, color="#205a7d", s=23, label="Original", zorder=3)
    ax.set(xlabel="BA individual", yticks=y, yticklabels=people.participant, xlim=(.12, .62),
           title="Variación entre las 25 personas")
    ax.tick_params(axis="y", labelsize=7)
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    ax.grid(axis="x", alpha=.2)
    for axis in axes:
        axis.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Control negativo: desplazar etiquetas GSR dentro de cada registro", fontsize=12)
    for extension in ["png", "pdf"]:
        fig.savefig(OUT / f"control_negativo_temporal.{extension}", dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
