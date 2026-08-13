#!/usr/bin/env python3
"""EDA reproducible y en streaming para eye tracking y pupilometria de Tobii."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

COLS = [
    "Recording timestamp", "Participant name", "Sensor", "Gaze point X", "Gaze point Y",
    "Gaze point X (MCSnorm)", "Gaze point Y (MCSnorm)", "Pupil diameter left",
    "Pupil diameter right", "Pupil diameter filtered", "Validity left", "Validity right",
    "Eye movement type", "Gaze event duration", "Eye movement type index",
    "Fixation point X", "Fixation point Y", "Presented Stimulus name",
]
NUM = [c for c in COLS if c not in {"Participant name", "Sensor", "Validity left", "Validity right", "Eye movement type", "Presented Stimulus name"}]


def args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, default=Path("datos/Toma_muestras_v2 Data export.tsv"))
    p.add_argument("--manifest", type=Path, default=Path("resultados/sincronizacion/inventario_tobii.csv"))
    p.add_argument("--output", type=Path, default=Path("resultados/eda/eye_pupil"))
    p.add_argument("--chunksize", type=int, default=250_000)
    p.add_argument("--sample-per-chunk", type=int, default=1500)
    return p.parse_args()


def add_stats(store, name, series):
    x = pd.to_numeric(series, errors="coerce").dropna().to_numpy(float)
    if not len(x): return
    s = store[name]
    s["n"] += len(x); s["sum"] += float(x.sum()); s["sumsq"] += float(x @ x)
    s["min"] = min(s["min"], float(x.min())); s["max"] = max(s["max"], float(x.max()))


def main():
    a = args(); a.output.mkdir(parents=True, exist_ok=True)
    stats = defaultdict(lambda: {"n": 0, "sum": 0., "sumsq": 0., "min": np.inf, "max": -np.inf})
    participant = defaultdict(Counter); movement = Counter(); left = Counter(); right = Counter()
    samples, fix_parts = [], []
    total = eye_rows = 0
    for k, ch in enumerate(pd.read_csv(a.input, sep="\t", usecols=COLS, chunksize=a.chunksize,
                                        dtype=str, low_memory=False)):
        total += len(ch)
        ch["Participant name"] = ch["Participant name"].fillna("SIN_ID")
        is_eye = ch["Sensor"].eq("Eye Tracker") | ch["Gaze point X"].notna() | ch["Pupil diameter left"].notna()
        e = ch.loc[is_eye].copy(); eye_rows += len(e)
        for c in NUM: e[c] = pd.to_numeric(e[c], errors="coerce")
        for c in ["Gaze point X", "Gaze point Y", "Gaze point X (MCSnorm)", "Gaze point Y (MCSnorm)",
                  "Pupil diameter left", "Pupil diameter right", "Pupil diameter filtered", "Gaze event duration"]:
            add_stats(stats, c, e[c])
        left.update(e["Validity left"].fillna("Missing")); right.update(e["Validity right"].fillna("Missing"))
        movement.update(e["Eye movement type"].fillna("Missing"))
        for pid, g in e.groupby("Participant name", sort=False):
            q = participant[pid]; q["rows"] += len(g)
            q["gaze_valid"] += int(g[["Gaze point X", "Gaze point Y"]].notna().all(axis=1).sum())
            q["pupil_left_valid"] += int(g["Pupil diameter left"].notna().sum())
            q["pupil_right_valid"] += int(g["Pupil diameter right"].notna().sum())
            q["both_eyes_valid"] += int(g[["Pupil diameter left", "Pupil diameter right"]].notna().all(axis=1).sum())
        n = min(a.sample_per_chunk, len(e))
        if n: samples.append(e.sample(n=n, random_state=20260812 + k))
        f = e.loc[e["Eye movement type"].eq("Fixation") & e["Eye movement type index"].notna(),
                  ["Participant name", "Eye movement type index", "Gaze event duration", "Fixation point X", "Fixation point Y"]]
        if len(f): fix_parts.append(f.drop_duplicates(["Participant name", "Eye movement type index"]))

    sample = pd.concat(samples, ignore_index=True) if samples else pd.DataFrame(columns=COLS)
    fixes = pd.concat(fix_parts, ignore_index=True).drop_duplicates(["Participant name", "Eye movement type index"]) if fix_parts else pd.DataFrame()
    rows = []
    for name, s in stats.items():
        mean = s["sum"] / s["n"]; var = max(0., s["sumsq"] / s["n"] - mean**2)
        x = pd.to_numeric(sample[name], errors="coerce").dropna()
        rows.append({"variable": name, "n": s["n"], "missing_eye_rows": eye_rows-s["n"], "mean": mean,
                     "std": var**.5, "min": s["min"], "p05_sample": x.quantile(.05),
                     "median_sample": x.median(), "p95_sample": x.quantile(.95), "max": s["max"]})
    pd.DataFrame(rows).to_csv(a.output / "resumen_numerico.csv", index=False)
    prows = []
    for pid, q in sorted(participant.items()):
        r = {"participant": pid, **q}
        for key in ["gaze_valid", "pupil_left_valid", "pupil_right_valid", "both_eyes_valid"]:
            r[key + "_pct"] = 100*q[key]/q["rows"] if q["rows"] else np.nan
        prows.append(r)
    pd.DataFrame(prows).to_csv(a.output / "calidad_por_participante.csv", index=False)
    pd.DataFrame({"validity": sorted(set(left)|set(right)),
                  "left_count": [left[x] for x in sorted(set(left)|set(right))],
                  "right_count": [right[x] for x in sorted(set(left)|set(right))]}).to_csv(a.output / "validez_ojos.csv", index=False)
    pd.DataFrame(movement.most_common(), columns=["eye_movement_type", "rows"]).to_csv(a.output / "movimientos_oculares.csv", index=False)
    if len(fixes):
        fixes.to_csv(a.output / "fijaciones_unicas.csv", index=False)
        fd = pd.to_numeric(fixes["Gaze event duration"], errors="coerce").dropna()
        pd.DataFrame([{"unique_fixations": len(fixes), "duration_n": len(fd), "duration_mean_ms": fd.mean(),
                       "duration_std_ms": fd.std(), "duration_median_ms": fd.median(),
                       "duration_p05_ms": fd.quantile(.05), "duration_p95_ms": fd.quantile(.95),
                       "duration_min_ms": fd.min(), "duration_max_ms": fd.max()}]).to_csv(
                           a.output / "resumen_fijaciones.csv", index=False)
    if a.manifest.exists():
        pd.read_csv(a.manifest).to_csv(a.output / "manifiesto_tobii_usado.csv", index=False)

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
    for c, color in [("Pupil diameter left", "#2878B5"), ("Pupil diameter right", "#D95319")]:
        x = pd.to_numeric(sample[c], errors="coerce").dropna(); x = x[x.between(1, 10)]
        ax[0].hist(x, bins=60, density=True, alpha=.5, label=c.replace("Pupil diameter ", ""), color=color)
    ax[0].set(xlabel="Diámetro pupilar (mm)", ylabel="Densidad", title="Distribución pupilar (muestra)"); ax[0].legend()
    mv = pd.Series(movement).sort_values(ascending=False).head(8)
    ax[1].barh(mv.index[::-1], mv.values[::-1], color="#3A923A"); ax[1].set(title="Tipos de movimiento ocular", xlabel="Filas")
    fig.tight_layout(); fig.savefig(a.output / "pupila_y_movimientos.png", dpi=160); plt.close(fig)

    g = sample.dropna(subset=["Gaze point X", "Gaze point Y"])
    fig, ax = plt.subplots(figsize=(9, 5)); h = ax.hexbin(g["Gaze point X"], g["Gaze point Y"], gridsize=70, bins="log", mincnt=1, cmap="viridis")
    ax.invert_yaxis(); ax.set(xlabel="X (px)", ylabel="Y (px)", title="Densidad de mirada (muestra)"); fig.colorbar(h, ax=ax, label="log10(N)")
    fig.tight_layout(); fig.savefig(a.output / "densidad_mirada.png", dpi=160); plt.close(fig)

    ptab = pd.DataFrame(prows)
    fig, ax = plt.subplots(figsize=(12, 5)); ax.bar(ptab["participant"], ptab["gaze_valid_pct"], color="#6F4E7C")
    ax.set(ylabel="Mirada válida (%)", xlabel="Participante", ylim=(0, 100), title="Completitud de coordenadas por participante"); ax.tick_params(axis="x", rotation=90)
    fig.tight_layout(); fig.savefig(a.output / "calidad_por_participante.png", dpi=160); plt.close(fig)

    meta = {"input": str(a.input), "input_bytes": a.input.stat().st_size, "manifest": str(a.manifest),
            "rows_total": total, "eye_rows": eye_rows, "participants": len(participant),
            "sample_rows": len(sample), "unique_fixations": len(fixes), "chunksize": a.chunksize,
            "quantiles_are_from_deterministic_sample": True}
    (a.output / "metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False))

if __name__ == "__main__": main()
