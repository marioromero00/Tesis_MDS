"""
EDA MVP — Datos EEG OpenBCI (16 canales, 125 Hz, 48 participantes)
Genera figuras en EDA/figuras/ y un resumen en EDA/resumen_eda.txt
"""

import os
import glob
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import signal as sp_signal

# ── Config ────────────────────────────────────────────────────────────────────
DATA_DIR   = os.path.join(os.path.dirname(__file__), "Datos EEG")
FIG_DIR    = os.path.join(os.path.dirname(__file__), "figuras")
REPORT     = os.path.join(os.path.dirname(__file__), "resumen_eda.txt")
FS         = 125          # Hz
SAT_THRESH = 90_000       # µV — umbral de saturación
EEG_COLS   = [f"EXG Channel {i}" for i in range(16)]
# Nombres de canales 10-20 (orden OpenBCI Cyton+Daisy 16ch)
CH_NAMES   = ["Fp1","Fp2","C3","C4","P7","P8","O1","O2",
               "F7","F8","F3","F4","T7","T8","P3","P4"]

os.makedirs(FIG_DIR, exist_ok=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def list_files():
    files = sorted(glob.glob(os.path.join(DATA_DIR, "P*.txt")))
    return files


def load_eeg(fpath):
    df = pd.read_csv(fpath, comment="%", skipinitialspace=True)
    df.columns = df.columns.str.strip()
    return df


def participant_id(fpath):
    return os.path.basename(fpath).replace(".txt", "")


def duration_s(df):
    return len(df) / FS


def saturation_pct(series):
    return (series.abs() > SAT_THRESH).mean() * 100


# ── Paso 1: estadísticas por participante ─────────────────────────────────────
print("Cargando todos los archivos…")
files = list_files()
n_parts = len(files)

rows = []
for fpath in files:
    pid   = participant_id(fpath)
    df    = load_eeg(fpath)
    n_samp = len(df)
    dur    = duration_s(df)
    n_nan  = df[EEG_COLS].isna().sum().sum()
    sat_per_ch = {ch: saturation_pct(df[col]) for ch, col in zip(CH_NAMES, EEG_COLS)}
    n_sat_chs  = sum(v == 100.0 for v in sat_per_ch.values())
    mean_good  = df[[col for col, ch in zip(EEG_COLS, CH_NAMES)
                      if sat_per_ch[ch] < 1]].stack().mean()
    rows.append({
        "participant":   pid,
        "n_samples":     n_samp,
        "duration_min":  dur / 60,
        "n_nan":         n_nan,
        "n_sat_channels": n_sat_chs,
        **{f"sat_{ch}": v for ch, v in sat_per_ch.items()},
        "mean_signal_uV": mean_good,
    })
    print(f"  {pid}: {n_samp} muestras, {dur/60:.1f} min, {n_sat_chs} ch saturados")

meta = pd.DataFrame(rows)
meta.to_csv(os.path.join(os.path.dirname(__file__), "meta_participantes.csv"), index=False)

# ── Figura 1: Duración por participante ───────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 4))
colors = ["tomato" if "REVISAR" in p else "steelblue" for p in meta["participant"]]
bars = ax.bar(meta["participant"], meta["duration_min"], color=colors)
ax.axhline(meta["duration_min"].median(), color="black", ls="--", lw=1.2, label=f"Mediana {meta['duration_min'].median():.1f} min")
ax.set_xlabel("Participante")
ax.set_ylabel("Duración (min)")
ax.set_title("Duración de grabación por participante")
ax.tick_params(axis="x", rotation=90)
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig1_duracion.png"), dpi=150)
plt.close()
print("Fig 1 guardada.")

# ── Figura 2: Canales saturados por participante ──────────────────────────────
sat_cols = [f"sat_{ch}" for ch in CH_NAMES]
sat_matrix = meta[sat_cols].values  # (48, 16)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Heatmap participantes × canales
im = axes[0].imshow(sat_matrix, aspect="auto", cmap="RdYlGn_r", vmin=0, vmax=100)
axes[0].set_xticks(range(16))
axes[0].set_xticklabels(CH_NAMES, rotation=45, ha="right", fontsize=8)
axes[0].set_yticks(range(n_parts))
axes[0].set_yticklabels(meta["participant"], fontsize=7)
axes[0].set_title("% saturación por canal y participante")
plt.colorbar(im, ax=axes[0], label="% saturado")

# N° canales saturados (100%) por participante
axes[1].barh(meta["participant"], meta["n_sat_channels"], color="tomato")
axes[1].set_xlabel("N° canales al 100% saturados")
axes[1].set_title("Canales completamente saturados")
axes[1].invert_yaxis()
axes[1].tick_params(axis="y", labelsize=7)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig2_saturacion.png"), dpi=150)
plt.close()
print("Fig 2 guardada.")

# ── Figura 3: Señal de ejemplo — P01 primeros 10 s ───────────────────────────
df_ex = load_eeg(files[0])
pid_ex = participant_id(files[0])
n_show = FS * 10
t = np.arange(n_show) / FS

# Solo canales sin saturación completa
sat_ex = {ch: saturation_pct(df_ex[col]) for ch, col in zip(CH_NAMES, EEG_COLS)}
good_chs = [(ch, col) for ch, col in zip(CH_NAMES, EEG_COLS) if sat_ex[ch] < 1]

fig, axes = plt.subplots(len(good_chs), 1, figsize=(14, max(6, len(good_chs) * 0.8)),
                          sharex=True)
if len(good_chs) == 1:
    axes = [axes]
for ax, (ch, col) in zip(axes, good_chs):
    sig = df_ex[col].values[:n_show]
    ax.plot(t, sig, lw=0.6, color="steelblue")
    ax.set_ylabel(ch, fontsize=7, rotation=0, labelpad=28)
    ax.tick_params(labelsize=6)
    ax.set_ylim(np.percentile(sig, 1) - 50, np.percentile(sig, 99) + 50)
axes[-1].set_xlabel("Tiempo (s)")
fig.suptitle(f"Señal EEG cruda — {pid_ex} — primeros 10 s (canales buenos)", y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig3_senal_ejemplo.png"), dpi=150, bbox_inches="tight")
plt.close()
print("Fig 3 guardada.")

# ── Figura 4: PSD promedio de canales buenos (Welch) ─────────────────────────
fig, axes = plt.subplots(2, 4, figsize=(16, 8), sharey=False)
axes = axes.flatten()

# Bandas EEG
bands = {"Delta\n(1-4)": (1, 4), "Theta\n(4-8)": (4, 8),
         "Alpha\n(8-13)": (8, 13), "Beta\n(13-30)": (13, 30),
         "Gamma\n(30-45)": (30, 45)}

# Seleccionar hasta 8 participantes espaciados para representatividad
step = max(1, n_parts // 8)
sample_files = files[::step][:8]
colors_psd = plt.cm.tab10(np.linspace(0, 1, len(sample_files)))

for idx, (fpath, color) in enumerate(zip(sample_files, colors_psd)):
    pid = participant_id(fpath)
    df_p = load_eeg(fpath)
    sat_p = {ch: saturation_pct(df_p[col]) for ch, col in zip(CH_NAMES, EEG_COLS)}
    good = [(ch, col) for ch, col in zip(CH_NAMES, EEG_COLS) if sat_p[ch] < 1]

    if not good:
        continue

    ax = axes[idx]
    psds = []
    for ch, col in good:
        sig = df_p[col].values.astype(float)
        freqs, psd = sp_signal.welch(sig, fs=FS, nperseg=FS * 4)
        psds.append(psd)
    mean_psd = np.mean(psds, axis=0)
    ax.semilogy(freqs, mean_psd, color=color, lw=1.2)
    ax.set_xlim(0, 60)
    ax.set_title(pid, fontsize=9)
    ax.set_xlabel("Hz", fontsize=7)
    ax.set_ylabel("PSD (µV²/Hz)", fontsize=7)
    ax.tick_params(labelsize=6)
    for bname, (flo, fhi) in bands.items():
        ax.axvspan(flo, fhi, alpha=0.05, color="gray")

for ax in axes[len(sample_files):]:
    ax.set_visible(False)

fig.suptitle("PSD promedio por participante (canales sin saturación) — Welch", fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig4_psd.png"), dpi=150)
plt.close()
print("Fig 4 guardada.")

# ── Figura 5: Potencia por banda EEG — todos los participantes ───────────────
band_limits = {"Delta": (1, 4), "Theta": (4, 8),
               "Alpha": (8, 13), "Beta": (13, 30), "Gamma": (30, 45)}
band_rows = []

for fpath in files:
    pid = participant_id(fpath)
    df_p = load_eeg(fpath)
    sat_p = {ch: saturation_pct(df_p[col]) for ch, col in zip(CH_NAMES, EEG_COLS)}
    good = [(ch, col) for ch, col in zip(CH_NAMES, EEG_COLS) if sat_p[ch] < 1]
    if not good:
        band_rows.append({"participant": pid, **{b: np.nan for b in band_limits}})
        continue
    all_psds = []
    for ch, col in good:
        sig = df_p[col].values.astype(float)
        freqs, psd = sp_signal.welch(sig, fs=FS, nperseg=FS * 4)
        all_psds.append(psd)
    mean_psd = np.mean(all_psds, axis=0)
    brow = {"participant": pid}
    for bname, (flo, fhi) in band_limits.items():
        mask = (freqs >= flo) & (freqs <= fhi)
        brow[bname] = np.trapz(mean_psd[mask], freqs[mask])
    band_rows.append(brow)

band_df = pd.DataFrame(band_rows)
band_df.to_csv(os.path.join(os.path.dirname(__file__), "potencia_bandas.csv"), index=False)

fig, axes = plt.subplots(1, len(band_limits), figsize=(16, 5), sharey=False)
for ax, bname in zip(axes, band_limits):
    vals = band_df[bname].dropna()
    parts = band_df.loc[band_df[bname].notna(), "participant"]
    bar_colors = ["tomato" if "REVISAR" in p else "steelblue" for p in parts]
    ax.bar(range(len(vals)), vals.values, color=bar_colors, edgecolor="none")
    ax.set_title(f"{bname}", fontsize=9)
    ax.set_xlabel("")
    ax.set_ylabel("Potencia (µV²)" if bname == "Delta" else "")
    ax.tick_params(axis="x", which="both", bottom=False, labelbottom=False)
    ax.axhline(vals.median(), color="black", ls="--", lw=1, label="Mediana")
    ax.legend(fontsize=6)

fig.suptitle("Potencia por banda EEG — todos los participantes", fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig5_bandas.png"), dpi=150)
plt.close()
print("Fig 5 guardada.")

# ── Figura 6: Distribución de amplitud (boxplot por canal) ───────────────────
# Muestra un participante representativo (sin saturaciones)
clean_files = [f for f, pid_row in zip(files, meta["participant"])
               if meta.loc[meta["participant"] == participant_id(f), "n_sat_channels"].values[0] == 0]

if clean_files:
    rep_file = clean_files[len(clean_files) // 2]
    df_rep = load_eeg(rep_file)
    pid_rep = participant_id(rep_file)

    data_bp = [df_rep[col].values for col in EEG_COLS]
    fig, ax = plt.subplots(figsize=(14, 5))
    bp = ax.boxplot(data_bp, labels=CH_NAMES, showfliers=False, patch_artist=True,
                    medianprops=dict(color="red", lw=2))
    for patch in bp["boxes"]:
        patch.set_facecolor("lightsteelblue")
    ax.set_xlabel("Canal")
    ax.set_ylabel("Amplitud (µV)")
    ax.set_title(f"Distribución de amplitud por canal — {pid_rep} (sin outliers extremos)")
    ax.tick_params(axis="x", rotation=30)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "fig6_boxplot_canales.png"), dpi=150)
    plt.close()
    print("Fig 6 guardada.")

# ── Figura 7: Correlación entre canales (participante representativo) ─────────
if clean_files:
    corr = df_rep[EEG_COLS].corr()
    corr.index = CH_NAMES
    corr.columns = CH_NAMES

    fig, ax = plt.subplots(figsize=(8, 7))
    im2 = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(16)); ax.set_xticklabels(CH_NAMES, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(16)); ax.set_yticklabels(CH_NAMES, fontsize=8)
    plt.colorbar(im2, ax=ax, label="Correlación de Pearson")
    ax.set_title(f"Correlación entre canales EEG — {pid_rep}")
    for i in range(16):
        for j in range(16):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center",
                    fontsize=5, color="black" if abs(corr.iloc[i, j]) < 0.7 else "white")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "fig7_correlacion.png"), dpi=150)
    plt.close()
    print("Fig 7 guardada.")

# ── Figura 8: SNR aproximado por canal (todos los participantes) ──────────────
# SNR proxy = std señal / std diferencia de primer orden (ruido de alta frecuencia)
snr_rows = []
for fpath in files:
    pid = participant_id(fpath)
    df_p = load_eeg(fpath)
    row = {"participant": pid}
    for ch, col in zip(CH_NAMES, EEG_COLS):
        sig = df_p[col].values.astype(float)
        if saturation_pct(df_p[col]) > 50:
            row[ch] = np.nan
        else:
            noise = np.diff(sig)
            row[ch] = sig.std() / (noise.std() + 1e-9)
    snr_rows.append(row)

snr_df = pd.DataFrame(snr_rows)
snr_matrix = snr_df[CH_NAMES].values

fig, ax = plt.subplots(figsize=(12, 7))
im3 = ax.imshow(snr_matrix, aspect="auto", cmap="YlOrRd", vmin=0)
ax.set_xticks(range(16)); ax.set_xticklabels(CH_NAMES, rotation=45, ha="right", fontsize=8)
ax.set_yticks(range(n_parts)); ax.set_yticklabels(meta["participant"], fontsize=7)
ax.set_title("SNR proxy por canal y participante (NaN = canal saturado)")
plt.colorbar(im3, ax=ax, label="SNR proxy")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig8_snr.png"), dpi=150)
plt.close()
print("Fig 8 guardada.")

# ── Reporte de texto ──────────────────────────────────────────────────────────
report_lines = []
report_lines.append("=" * 60)
report_lines.append("RESUMEN EDA — Datos EEG OpenBCI")
report_lines.append("=" * 60)
report_lines.append(f"\nN° participantes      : {n_parts}")
report_lines.append(f"Canales EEG           : 16  ({', '.join(CH_NAMES)})")
report_lines.append(f"Frecuencia de muestreo: {FS} Hz")
report_lines.append(f"\n--- Duración de grabación ---")
report_lines.append(f"  Mínima  : {meta['duration_min'].min():.1f} min  ({meta.loc[meta['duration_min'].idxmin(),'participant']})")
report_lines.append(f"  Máxima  : {meta['duration_min'].max():.1f} min  ({meta.loc[meta['duration_min'].idxmax(),'participant']})")
report_lines.append(f"  Mediana : {meta['duration_min'].median():.1f} min")
report_lines.append(f"  Media   : {meta['duration_min'].mean():.1f} min  (±{meta['duration_min'].std():.1f})")

report_lines.append(f"\n--- Calidad de señal (saturación >90 000 µV) ---")
fully_sat = meta[meta["n_sat_channels"] > 0][["participant", "n_sat_channels"]]
report_lines.append(f"  Participantes con ≥1 canal saturado: {len(fully_sat)}/{n_parts}")
report_lines.append("  Detalle:")
for _, r in fully_sat.iterrows():
    report_lines.append(f"    {r['participant']}: {int(r['n_sat_channels'])} canales al 100%")

report_lines.append(f"\n--- Canales más frecuentemente saturados ---")
sat_freq = (meta[[f"sat_{ch}" for ch in CH_NAMES]] == 100).sum()
sat_freq.index = CH_NAMES
for ch, n in sat_freq.sort_values(ascending=False).items():
    if n > 0:
        report_lines.append(f"  {ch}: saturado en {n}/{n_parts} participantes")

report_lines.append(f"\n--- Valores atípicos ---")
flag_p25 = meta[meta["participant"].str.contains("REVISAR")]
if not flag_p25.empty:
    report_lines.append(f"  P25_REVISAR marcado manualmente. Duración: {flag_p25['duration_min'].values[0]:.1f} min, "
                        f"canales saturados: {int(flag_p25['n_sat_channels'].values[0])}")

report_lines.append(f"\n--- Potencia por banda (mediana sobre participantes válidos) ---")
for b in band_limits:
    m = band_df[b].median()
    report_lines.append(f"  {b:7s}: {m:.2e} µV²")

report_lines.append(f"\n--- Archivos generados ---")
for fig_name in sorted(os.listdir(FIG_DIR)):
    report_lines.append(f"  figuras/{fig_name}")

report_lines.append("\n" + "=" * 60)

report_text = "\n".join(report_lines)
print("\n" + report_text)

with open(REPORT, "w") as f:
    f.write(report_text + "\n")

print(f"\nReporte guardado en {REPORT}")
print(f"Figuras guardadas en {FIG_DIR}/")
