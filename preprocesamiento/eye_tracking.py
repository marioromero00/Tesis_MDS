"""
Extracción de eventos y features de eye tracking.

El Tobii Pro aplica internamente el algoritmo I-VT (Velocity-Threshold
Identification) y clasifica cada muestra en Fixation, Saccade, EyesNotFound o
Unclassified. El pipeline NO reclasifica: agrega los eventos que el tracker ya
entregó. Recalcular el I-VT con otros umbrales produciría una segmentación
distinta de la que se usó para reportar la calidad del dataset.

A diferencia de GSR y pupila, el eye tracking no se resamplea a la grilla de
60 Hz. Sus unidades son eventos con duración propia, y promediarlos sobre una
grilla uniforme destruiría justamente la información de conteo y duración que
alimenta el Attention Score.

Asignación de un evento a una ventana: por su instante de inicio (onset). Una
fijación de 400 ms que empieza en el segundo 1,9 de una ventana de 2 s cuenta
completa en esa ventana y no se reparte. Repartirla obligaría a decidir un
criterio de prorrateo que no está en el diseño.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

# Duración mínima de fijación aceptada, en ms. Por debajo suelen ser
# inestabilidades del tracker, no fijaciones reales.
MIN_FIJACION_MS = 100.0


def extraer_eventos(df: pd.DataFrame, mapa: dict,
                    min_fijacion_ms: float = MIN_FIJACION_MS
                    ) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Agrega las muestras I-VT en dos tablas de eventos: fijaciones y sacadas.

    Fijaciones: onset, duración (ms), punto medio (x, y).
    Sacadas:    onset, duración (ms), amplitud (px) y velocidad pico (px/s).

    La amplitud de la sacada se calcula como la distancia entre el primer y el
    último punto de mirada válido del propio evento, porque el export no trae
    una columna de amplitud.
    """
    col_tipo, col_idx = mapa["mov_tipo"], mapa["mov_indice"]
    col_dur, col_gx, col_gy = mapa["mov_duracion"], mapa["gaze_x"], mapa["gaze_y"]
    col_fx = mapa.get("fix_x") or col_gx
    col_fy = mapa.get("fix_y") or col_gy

    tipo = df[col_tipo].astype("string").str.strip()

    # ---- Fijaciones -------------------------------------------------------
    fij = df[tipo == "Fixation"]
    if fij.empty:
        fijaciones = pd.DataFrame(columns=["onset", "duracion_ms", "x", "y"])
    else:
        fijaciones = (fij.groupby(fij[col_idx], sort=True)
                        .agg(onset=("timestamp", "min"),
                             duracion_ms=(col_dur, "first"),
                             x=(col_fx, "mean"),
                             y=(col_fy, "mean"))
                        .reset_index(drop=True))
        fijaciones["duracion_ms"] = pd.to_numeric(fijaciones["duracion_ms"],
                                                  errors="coerce")
        fijaciones = fijaciones[fijaciones["duracion_ms"] >= min_fijacion_ms]
        fijaciones = fijaciones.sort_values("onset").reset_index(drop=True)

    # ---- Sacadas ----------------------------------------------------------
    sac = df[tipo == "Saccade"]
    if sac.empty:
        sacadas = pd.DataFrame(columns=["onset", "duracion_ms", "amplitud", "vel_pico"])
    else:
        filas = []
        for _, grupo in sac.groupby(sac[col_idx], sort=True):
            x = pd.to_numeric(grupo[col_gx], errors="coerce").values
            y = pd.to_numeric(grupo[col_gy], errors="coerce").values
            ok = np.isfinite(x) & np.isfinite(y)
            amplitud = vel_pico = np.nan
            if ok.sum() >= 2:
                xv, yv = x[ok], y[ok]
                amplitud = float(np.hypot(xv[-1] - xv[0], yv[-1] - yv[0]))
                t = grupo["timestamp"].values[ok].astype("datetime64[ns]").astype(np.int64) / 1e9
                dt = np.diff(t)
                paso = np.hypot(np.diff(xv), np.diff(yv))
                bueno = dt > 0
                if bueno.any():
                    vel_pico = float(np.max(paso[bueno] / dt[bueno]))
            filas.append({
                "onset": grupo["timestamp"].min(),
                "duracion_ms": pd.to_numeric(grupo[col_dur], errors="coerce").iloc[0],
                "amplitud": amplitud,
                "vel_pico": vel_pico,
            })
        sacadas = pd.DataFrame(filas).sort_values("onset").reset_index(drop=True)

    return fijaciones, sacadas


def _agregar(eventos: pd.DataFrame, ventanas: pd.DataFrame,
             columnas: dict[str, tuple[str, str]]) -> pd.DataFrame:
    """Agrega eventos por ventana según su onset."""
    n = len(ventanas)
    if eventos.empty:
        salida = {nombre: np.zeros(n) if op == "count" else np.full(n, np.nan)
                  for nombre, (_, op) in columnas.items()}
        return pd.DataFrame(salida, index=ventanas.index)

    t = eventos["onset"].values
    ini = np.searchsorted(t, ventanas["inicio"].values, side="left")
    fin = np.searchsorted(t, ventanas["fin"].values, side="left")

    salida = {nombre: np.full(n, np.nan) for nombre in columnas}
    for i, (a, b) in enumerate(zip(ini, fin)):
        tramo = eventos.iloc[a:b]
        for nombre, (col, op) in columnas.items():
            if op == "count":
                salida[nombre][i] = float(len(tramo))
                continue
            valores = pd.to_numeric(tramo[col], errors="coerce").values \
                if len(tramo) else np.array([])
            valores = valores[np.isfinite(valores)]
            if valores.size == 0:
                salida[nombre][i] = np.nan
            elif op == "mean":
                salida[nombre][i] = float(valores.mean())
            elif op == "sum":
                salida[nombre][i] = float(valores.sum())
            elif op == "max":
                salida[nombre][i] = float(valores.max())
    return pd.DataFrame(salida, index=ventanas.index)


def features(fijaciones: pd.DataFrame, sacadas: pd.DataFrame,
             ventanas: pd.DataFrame, ventana_s: float = 2.0) -> pd.DataFrame:
    """
    Features de eye tracking por ventana.

      et_n_fijaciones, et_fij_dur_media, et_fij_dur_total, et_pct_tiempo_fijando
      et_n_sacadas, et_sac_amp_media, et_sac_amp_max, et_sac_vel_pico, et_sac_dur_media
      et_disp_x, et_disp_y, et_disp_rms, et_disp_bbox  — dispersión de la mirada
    """
    fij = _agregar(fijaciones, ventanas, {
        "et_n_fijaciones":  ("duracion_ms", "count"),
        "et_fij_dur_media": ("duracion_ms", "mean"),
        "et_fij_dur_total": ("duracion_ms", "sum"),
    })
    sac = _agregar(sacadas, ventanas, {
        "et_n_sacadas":     ("duracion_ms", "count"),
        "et_sac_dur_media": ("duracion_ms", "mean"),
        "et_sac_amp_media": ("amplitud", "mean"),
        "et_sac_amp_max":   ("amplitud", "max"),
        "et_sac_vel_pico":  ("vel_pico", "max"),
    })

    # Proporción de la ventana ocupada por fijaciones. Se recorta a 100 %:
    # una fijación asignada por su onset puede extenderse más allá del borde.
    fij["et_pct_tiempo_fijando"] = np.clip(
        100.0 * fij["et_fij_dur_total"].fillna(0.0) / (ventana_s * 1000.0), 0, 100)

    # Dispersión espacial de la mirada dentro de la ventana.
    n = len(ventanas)
    disp = {k: np.full(n, np.nan) for k in
            ("et_disp_x", "et_disp_y", "et_disp_rms", "et_disp_bbox")}
    if not fijaciones.empty:
        t = fijaciones["onset"].values
        ini = np.searchsorted(t, ventanas["inicio"].values, side="left")
        fin = np.searchsorted(t, ventanas["fin"].values, side="left")
        xs_all = pd.to_numeric(fijaciones["x"], errors="coerce").values
        ys_all = pd.to_numeric(fijaciones["y"], errors="coerce").values
        for i, (a, b) in enumerate(zip(ini, fin)):
            x, y = xs_all[a:b], ys_all[a:b]
            ok = np.isfinite(x) & np.isfinite(y)
            if ok.sum() >= 2:
                x, y = x[ok], y[ok]
                disp["et_disp_x"][i] = float(np.std(x))
                disp["et_disp_y"][i] = float(np.std(y))
                disp["et_disp_rms"][i] = float(
                    np.sqrt(np.mean((x - x.mean()) ** 2 + (y - y.mean()) ** 2)))
                disp["et_disp_bbox"][i] = float((x.max() - x.min()) * (y.max() - y.min()))
            elif ok.sum() == 1:
                disp["et_disp_x"][i] = 0.0
                disp["et_disp_y"][i] = 0.0
                disp["et_disp_rms"][i] = 0.0
                disp["et_disp_bbox"][i] = 0.0

    return pd.concat([fij, sac, pd.DataFrame(disp, index=ventanas.index)], axis=1)
