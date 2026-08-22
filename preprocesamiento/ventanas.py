"""
Grilla de ventanas compartida por las cuatro señales.

El EEG ya está epochado en ventanas de 2 s con 50 % de solapamiento
(250 muestras a 125 Hz, paso de 125). Para que las features de GSR,
pupilometría y eye tracking se puedan unir a esa tabla, las ventanas del
Tobii se construyen con los mismos 2 s y el mismo paso de 1 s, ancladas
al reloj absoluto UTC.

La ventana es semiabierta [inicio, fin): una muestra en el borde pertenece
a una sola ventana.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

VENTANA_S = 2.0
PASO_S = 1.0


def grilla(t_inicio: pd.Timestamp, t_fin: pd.Timestamp,
           ventana_s: float = VENTANA_S,
           paso_s: float = PASO_S) -> pd.DataFrame:
    """
    Ventanas de `ventana_s` cada `paso_s` dentro de [t_inicio, t_fin].

    Solo se emiten ventanas completas: la última ventana termina en o antes
    de t_fin. Una ventana truncada tendría menos muestras y sesgaría las
    features de conteo (número de fijaciones, número de picos SCR).
    """
    dur = (t_fin - t_inicio).total_seconds()
    if dur < ventana_s:
        return pd.DataFrame(columns=["idx_ventana", "inicio", "fin", "inicio_s"])

    n = int(np.floor((dur - ventana_s) / paso_s)) + 1
    offsets = np.arange(n) * paso_s
    inicios = t_inicio + pd.to_timedelta(offsets, unit="s")
    fines = inicios + pd.Timedelta(seconds=ventana_s)
    return pd.DataFrame({
        "idx_ventana": np.arange(n),
        "inicio": inicios,
        "fin": fines,
        "inicio_s": offsets,
    })


def grilla_por_segmento(segmentos: pd.DataFrame,
                        ventana_s: float = VENTANA_S,
                        paso_s: float = PASO_S) -> pd.DataFrame:
    """
    Construye la grilla dentro de cada segmento y no a través de ellos.

    `segmentos` debe traer al menos: segmento_id, tipo, inicio, fin.

    Una ventana nunca cruza el borde de un estímulo. Si cruzara, mezclaría
    dos condiciones experimentales dentro de la misma etiqueta y la
    comparación dejaría de ser interpretable.
    """
    partes = []
    for _, seg in segmentos.iterrows():
        g = grilla(seg["inicio"], seg["fin"], ventana_s, paso_s)
        if g.empty:
            continue
        g["segmento_id"] = seg["segmento_id"]
        g["tipo"] = seg["tipo"]
        if "estimulo" in seg.index:
            g["estimulo"] = seg["estimulo"]
        partes.append(g)

    if not partes:
        return pd.DataFrame(
            columns=["segmento_id", "tipo", "estimulo",
                     "idx_ventana", "inicio", "fin", "inicio_s"])

    out = pd.concat(partes, ignore_index=True)
    cols = ["segmento_id", "tipo", "estimulo", "idx_ventana", "inicio", "fin", "inicio_s"]
    return out[[c for c in cols if c in out.columns]]


def indices_por_ventana(marcas: pd.Series, ventanas: pd.DataFrame) -> list[np.ndarray]:
    """
    Para cada ventana, las posiciones de `marcas` (timestamps ordenados)
    que caen en [inicio, fin).

    Usa searchsorted en vez de una comparación por ventana: con ~800 000
    muestras por participante y ~13 000 ventanas, la versión ingenua es
    O(n·m) y no termina.
    """
    t = marcas.values
    ini = np.searchsorted(t, ventanas["inicio"].values, side="left")
    fin = np.searchsorted(t, ventanas["fin"].values, side="left")
    return [np.arange(a, b) for a, b in zip(ini, fin)]
