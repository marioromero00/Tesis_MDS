"""Carga comun para las comprobaciones de la auditoria de codigo (ronda 3). Solo lectura."""
import sys, time, pickle
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'scripts'))
import numpy as np, pandas as pd
import cierre_experimental_v3 as V3
CACHE = Path(sys.argv[1]) if len(sys.argv) > 1 else None

def data():
    if CACHE and CACHE.exists():
        return pd.read_pickle(CACHE)
    d = V3.load_data()
    if CACHE:
        d.to_pickle(CACHE)
    return d

if __name__ == '__main__':
    t = time.time(); d = data(); print(d.shape, round(time.time() - t, 1), 's')
    print(d.split.value_counts().to_dict(), d.participant.nunique())
    print('etiquetadas atencion', int(d.y_atencion.notna().sum()), 'activacion', int(d.y_activacion.notna().sum()))
