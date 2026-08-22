"""
Ingesta del export de Tobii Pro Lab.

Cubre los pasos 1.2, 3.1 y 3.2 del diseño de `Sincronizacion_señales.ipynb`:
separar el TSV único por participante, reconstruir el timestamp absoluto y
resamplear a una grilla uniforme de 60 Hz.

El stream del Tobii es temporalmente irregular (la frecuencia efectiva oscila
alrededor de los 60 Hz nominales). La grilla uniforme se construye una vez por
participante y la comparten GSR y pupilometría, de modo que ambas señales
quedan sobre el mismo eje temporal. El eye tracking NO se resamplea: sus
eventos ya vienen clasificados por el I-VT del Tobii y se agregan directamente
por ventana.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

import columnas as cols_mod

FS_GRILLA = 60.0
GAP_MAX_MS = 200.0


# ----------------------------------------------------------------------------
# 1 · Separación por participante
# ----------------------------------------------------------------------------

def separar_por_participante(tsv: Path, salida: Path,
                             filas_por_bloque: int = 500_000) -> list[Path]:
    """
    Divide el TSV unificado en un Parquet por participante.

    Se lee por bloques porque el export son ~2,9 millones de filas y 99
    columnas: cargarlo entero satura la memoria de un portátil. Cada bloque se
    reparte a un Parquet por participante y al final se consolidan.
    """
    salida.mkdir(parents=True, exist_ok=True)
    parciales: dict[str, list[pd.DataFrame]] = {}

    lector = pd.read_csv(tsv, sep="\t", chunksize=filas_por_bloque, low_memory=False)
    mapa = None
    for bloque in lector:
        if mapa is None:
            mapa = cols_mod.resolver(bloque.columns)
            cols_mod.validar(mapa, bloque.columns)
        col_p = mapa["participante"]
        for nombre, grupo in bloque.groupby(col_p, sort=False):
            parciales.setdefault(str(nombre), []).append(grupo)

    escritos = []
    for nombre, trozos in parciales.items():
        seguro = re.sub(r"[^\w.-]", "_", nombre)
        destino = salida / f"{seguro}.parquet"
        pd.concat(trozos, ignore_index=True).to_parquet(destino, index=False)
        escritos.append(destino)
    return sorted(escritos)


# ----------------------------------------------------------------------------
# 2 · Timestamps absolutos
# ----------------------------------------------------------------------------

def reconstruir_timestamps(df: pd.DataFrame, mapa: dict,
                           formato_fecha: str = "%m/%d/%Y %H:%M:%S.%f") -> pd.DataFrame:
    """
    Reconstruye el timestamp absoluto combinando fecha de grabación, hora de
    inicio y el offset en microsegundos.

    El Tobii no expone una hora de pared por muestra: entrega la fecha y hora
    de inicio de la grabación más un contador en microsegundos desde ese
    inicio. La fecha viene en formato mm/dd/yyyy.
    """
    df = df.copy()
    fecha = df[mapa["fecha"]].astype(str).str.strip()
    hora = df[mapa["hora_inicio"]].astype(str).str.strip()

    inicio = pd.to_datetime(fecha + " " + hora, format=formato_fecha, errors="coerce")
    if inicio.isna().all():                      # el export puede traer otro orden
        inicio = pd.to_datetime(fecha + " " + hora, errors="coerce", dayfirst=False)
    if inicio.isna().all():
        raise ValueError(
            f"No se pudo interpretar la fecha de grabación. "
            f"Ejemplo leído: {fecha.iloc[0]!r} {hora.iloc[0]!r}")

    df["timestamp"] = inicio + pd.to_timedelta(
        pd.to_numeric(df[mapa["ts_us"]], errors="coerce"), unit="us")

    validos = df["timestamp"].dropna()
    if validos.empty or validos.min().year <= 2000:
        raise ValueError("Error en la reconstrucción de timestamps: el año resultante "
                         "es implausible, revisar el formato de fecha del export.")

    return df.sort_values("timestamp").reset_index(drop=True)


def grilla_uniforme(df: pd.DataFrame, fs: float = FS_GRILLA) -> pd.DatetimeIndex:
    """Grilla temporal uniforme de `fs` Hz que cubre toda la sesión."""
    t0, t1 = df["timestamp"].iloc[0], df["timestamp"].iloc[-1]
    n = int(np.floor((t1 - t0).total_seconds() * fs)) + 1
    return t0 + pd.to_timedelta(np.arange(n) / fs, unit="s")


def resamplear(serie: pd.Series, timestamps: pd.Series,
               grilla: pd.DatetimeIndex,
               gap_max_ms: float = GAP_MAX_MS) -> pd.Series:
    """
    Resamplea una señal irregular a la grilla uniforme por interpolación lineal.

    Los huecos mayores a `gap_max_ms` no se interpolan: quedan como NaN. Un
    hueco largo suele ser desconexión del sensor, y rellenarlo inventaría
    señal donde no la hubo.
    """
    valida = serie.notna().values
    if valida.sum() < 2:
        return pd.Series(np.nan, index=grilla)

    t_src = timestamps.values[valida].astype("datetime64[ns]").astype(np.int64) / 1e9
    y_src = pd.to_numeric(serie[valida], errors="coerce").values
    finito = np.isfinite(y_src)
    t_src, y_src = t_src[finito], y_src[finito]
    if t_src.size < 2:
        return pd.Series(np.nan, index=grilla)

    t_dst = grilla.values.astype("datetime64[ns]").astype(np.int64) / 1e9
    y = interp1d(t_src, y_src, kind="linear",
                 bounds_error=False, fill_value=np.nan)(t_dst)

    # Reintroducir NaN dentro de los huecos largos del origen.
    gaps = np.diff(t_src)
    for i in np.flatnonzero(gaps > gap_max_ms / 1000.0):
        y[(t_dst > t_src[i]) & (t_dst < t_src[i + 1])] = np.nan

    return pd.Series(y, index=grilla)


# ----------------------------------------------------------------------------
# 3 · Segmentos de estímulo
# ----------------------------------------------------------------------------

TAXONOMIA = [
    (re.compile(r"^\s*\d+\s*$"),          "exposicion_imagen"),
    (re.compile(r"^blur_", re.I),          "blur_exposicion"),
    (re.compile(r"^(dise[nñ]o|emotion)_", re.I), "evaluacion_imagen"),
]
TIPOS_UTILES = {"exposicion_imagen"}


def clasificar_estimulo(nombre: object) -> str:
    """Taxonomía de estímulos del protocolo (sección 4.1 del diseño)."""
    if nombre is None or (isinstance(nombre, float) and np.isnan(nombre)):
        return "sin_estimulo"
    texto = str(nombre).strip()
    if not texto or texto.lower() in {"nan", "none"}:
        return "sin_estimulo"
    for patron, tipo in TAXONOMIA:
        if patron.match(texto):
            return tipo
    return "otro"


def segmentos_de_estimulo(df: pd.DataFrame, mapa: dict) -> pd.DataFrame:
    """
    Deriva los segmentos de estímulo como tramos contiguos con el mismo nombre.

    Se prefiere la columna de estímulo presentado por sobre los eventos
    Start/End porque no depende del vocabulario de eventos, que cambia entre
    configuraciones de Tobii Pro Lab. Cada tramo entrega inicio, fin y el tipo
    según la taxonomía del protocolo.
    """
    col = mapa.get("estimulo")
    if col is None or col not in df.columns:
        # Sin columna de estímulo: la sesión completa es un solo segmento.
        return pd.DataFrame([{
            "segmento_id": 0, "estimulo": "sesion_completa", "tipo": "sesion",
            "inicio": df["timestamp"].iloc[0], "fin": df["timestamp"].iloc[-1],
        }])

    nombre = df[col].astype("string")
    cambio = (nombre != nombre.shift()).cumsum()

    seg = (df.assign(_g=cambio, _nombre=nombre)
             .groupby("_g", sort=True)
             .agg(estimulo=("_nombre", "first"),
                  inicio=("timestamp", "min"),
                  fin=("timestamp", "max"))
             .reset_index(drop=True))

    seg["tipo"] = seg["estimulo"].map(clasificar_estimulo)
    seg = seg[seg["tipo"] != "sin_estimulo"].reset_index(drop=True)
    seg.insert(0, "segmento_id", np.arange(len(seg)))
    return seg


def cargar_participante(parquet: Path) -> tuple[pd.DataFrame, dict, dict]:
    """Carga un Parquet de participante y deja listo el timestamp absoluto."""
    df = pd.read_parquet(parquet)
    mapa = cols_mod.resolver(df.columns)
    disponibles = cols_mod.validar(mapa, df.columns)
    df = reconstruir_timestamps(df, mapa)
    return df, mapa, disponibles
