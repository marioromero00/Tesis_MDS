"""
Preprocesamiento y extracción de features de GSR.

La conductancia de la piel tiene dos componentes fisiológicamente distintos:

- SCL (Skin Conductance Level): tónico, varía lento, nivel basal de activación
  simpática sostenida.
- SCR (Skin Conductance Response): fásico, picos rápidos ante estímulos.

Orden del pipeline: rechazo de artefactos -> resampleo -> descomposición
tónico/fásica -> features por ventana. La descomposición va ANTES de cualquier
normalización: los algoritmos de descomposición asumen que los impulsos del
nervio sudomotor no son negativos, y el z-score centra en cero e introduce
valores negativos.

Sobre la ventana de agregación
------------------------------
La latencia típica de una SCR es de 1 a 5 s, y la ventana del diseño es de 2 s.
Una SCR disparada por un estímulo puede caer varias ventanas después del
estímulo que la causó. Esta decisión sigue abierta, de modo que el módulo
calcula las features de SCR sobre dos soportes:

- la ventana de 2 s, alineada con el EEG (sufijo ninguno);
- una ventana de contexto que termina en el mismo instante pero mira hacia
  atrás `contexto_s` segundos (sufijo `_ctx{N}s`).

Las dos se emiten juntas para poder comparar cuál predice mejor. El módulo no
elige por su cuenta.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import signal as sp_signal

# Corte del filtro que separa el componente tónico del fásico.
CORTE_TONICO_HZ = 0.05
# Amplitud mínima para contar un pico como SCR, en µS. Criterio habitual en la
# literatura de EDA; por debajo de esto no se distingue de la deriva del sensor.
AMP_MIN_SCR_US = 0.01
SIGMA_ARTEFACTO = 5.0
CONTEXTO_S = 6.0


def rechazar_artefactos(gsr: pd.Series, sigma: float = SIGMA_ARTEFACTO) -> pd.Series:
    """
    Marca como NaN las muestras con un salto abrupto respecto de la anterior.

    Umbral adaptativo sobre la derivada absoluta (media + sigma·desviación).
    Un salto así corresponde a desconexión o recolocación del sensor, no a
    fisiología: la conductancia de la piel no cambia a esa velocidad.
    """
    x = pd.to_numeric(gsr, errors="coerce")
    delta = x.diff().abs()
    if delta.notna().sum() < 2:
        return x
    umbral = delta.mean() + sigma * delta.std()
    return x.where(delta.isna() | (delta <= umbral))


def descomponer(x: np.ndarray, fs: float,
                corte_hz: float = CORTE_TONICO_HZ) -> tuple[np.ndarray, np.ndarray]:
    """
    Separa el componente tónico del fásico con un pasa-bajos de fase cero.

    Devuelve (tonico, fasico). Los NaN se interpolan solo para poder filtrar y
    se reponen después, de modo que un tramo sin señal no aparezca como si
    tuviera valor.
    """
    x = np.asarray(x, dtype=float)
    faltan = ~np.isfinite(x)
    if faltan.all():
        return np.full_like(x, np.nan), np.full_like(x, np.nan)

    idx = np.arange(x.size)
    relleno = np.interp(idx, idx[~faltan], x[~faltan])

    nyq = fs / 2.0
    wn = min(corte_hz / nyq, 0.99)
    b, a = sp_signal.butter(2, wn, btype="low")
    # padlen por defecto puede exceder señales cortas (ventanas de pocos segundos)
    padlen = min(3 * max(len(a), len(b)), max(relleno.size - 1, 0))
    tonico = sp_signal.filtfilt(b, a, relleno, padlen=padlen)

    fasico = relleno - tonico
    tonico[faltan] = np.nan
    fasico[faltan] = np.nan
    return tonico, fasico


def descomponer_cvxeda(x: np.ndarray, fs: float):
    """
    Descomposición por cvxEDA, si está instalado (requiere cvxopt).

    Es la opción preferida del diseño original porque impone explícitamente la
    no-negatividad de los impulsos sudomotores. Si la dependencia no está, el
    llamador debe caer en `descomponer`.
    """
    import cvxEDA  # noqa: F401  (import diferido: dependencia opcional)

    r, p, t, l, d, e, obj = cvxEDA.cvxEDA(np.asarray(x, dtype=float), 1.0 / fs)
    return np.asarray(t), np.asarray(r)


def preparar(df: pd.DataFrame, mapa: dict, grilla: pd.DatetimeIndex,
             fs: float = 60.0, metodo: str = "butter") -> pd.DataFrame:
    """
    Deja la GSR sobre la grilla uniforme, con sus componentes ya separados.

    Devuelve un DataFrame indexado por la grilla con columnas:
    gsr (µS), scl (µS), scr (µS), gsr_z (z-score por sujeto).
    """
    from tobii_io import resamplear

    limpia = rechazar_artefactos(df[mapa["gsr"]])
    sobre_grilla = resamplear(limpia, df["timestamp"], grilla)

    x = sobre_grilla.values
    if metodo == "cvxeda":
        try:
            tonico, fasico = descomponer_cvxeda(x, fs)
        except ImportError:
            tonico, fasico = descomponer(x, fs)
    else:
        tonico, fasico = descomponer(x, fs)

    sd = np.nanstd(x)
    z = (x - np.nanmean(x)) / sd if sd and np.isfinite(sd) and sd > 0 else np.full_like(x, np.nan)

    return pd.DataFrame({"gsr": x, "scl": tonico, "scr": fasico, "gsr_z": z},
                        index=grilla)


def _features_scr(fasico: np.ndarray, fs: float) -> dict:
    """Conteo y amplitud de picos SCR dentro de un tramo."""
    valido = fasico[np.isfinite(fasico)]
    if valido.size < 3:
        return {"n_picos": np.nan, "amp_media": np.nan,
                "amp_max": np.nan, "auc": np.nan}

    picos, props = sp_signal.find_peaks(valido, height=AMP_MIN_SCR_US,
                                        prominence=AMP_MIN_SCR_US)
    alturas = props["peak_heights"] if picos.size else np.array([])
    return {
        "n_picos": float(picos.size),
        "amp_media": float(alturas.mean()) if alturas.size else 0.0,
        "amp_max": float(alturas.max()) if alturas.size else 0.0,
        "auc": float(np.trapz(np.clip(valido, 0, None)) / fs),
    }


def features(senal: pd.DataFrame, ventanas: pd.DataFrame, fs: float = 60.0,
             contexto_s: float = CONTEXTO_S) -> pd.DataFrame:
    """
    Features de GSR por ventana.

    Sobre la ventana de 2 s alineada con el EEG:
      gsr_scl_media, gsr_scl_pendiente, gsr_scl_z, gsr_std, gsr_rango,
      gsr_scr_n_picos, gsr_scr_amp_media, gsr_scr_amp_max, gsr_scr_auc,
      gsr_pct_valido

    Sobre la ventana de contexto que termina en el mismo instante:
      gsr_scr_n_picos_ctx{N}s, gsr_scr_amp_media_ctx{N}s,
      gsr_scr_amp_max_ctx{N}s, gsr_scr_auc_ctx{N}s
    """
    t = senal.index.values
    ini = np.searchsorted(t, ventanas["inicio"].values, side="left")
    fin = np.searchsorted(t, ventanas["fin"].values, side="left")
    ini_ctx = np.searchsorted(
        t, (ventanas["fin"] - pd.Timedelta(seconds=contexto_s)).values, side="left")

    scl, scr, bruta, z = (senal["scl"].values, senal["scr"].values,
                          senal["gsr"].values, senal["gsr_z"].values)
    sufijo = f"_ctx{int(contexto_s)}s"
    filas = []

    for a, b, c in zip(ini, fin, ini_ctx):
        tramo_scl, tramo_bruta, tramo_z = scl[a:b], bruta[a:b], z[a:b]
        n = tramo_bruta.size
        finito = np.isfinite(tramo_bruta)

        if n and finito.any():
            xs = np.arange(n)[np.isfinite(tramo_scl)]
            ys = tramo_scl[np.isfinite(tramo_scl)]
            pendiente = float(np.polyfit(xs, ys, 1)[0] * fs) if xs.size >= 2 else np.nan
            fila = {
                "gsr_scl_media": float(np.nanmean(tramo_scl)),
                "gsr_scl_pendiente": pendiente,
                "gsr_scl_z": float(np.nanmean(tramo_z)),
                "gsr_std": float(np.nanstd(tramo_bruta)),
                "gsr_rango": float(np.nanmax(tramo_bruta) - np.nanmin(tramo_bruta)),
                "gsr_pct_valido": float(100.0 * finito.mean()),
            }
        else:
            fila = {k: np.nan for k in
                    ("gsr_scl_media", "gsr_scl_pendiente", "gsr_scl_z",
                     "gsr_std", "gsr_rango")}
            fila["gsr_pct_valido"] = 0.0

        for clave, valor in _features_scr(scr[a:b], fs).items():
            fila[f"gsr_scr_{clave}"] = valor
        for clave, valor in _features_scr(scr[c:b], fs).items():
            fila[f"gsr_scr_{clave}{sufijo}"] = valor

        filas.append(fila)

    return pd.DataFrame(filas, index=ventanas.index)
