"""Carga reducida: solo requiere las señales retenidas y metadatos temporales."""
import numpy as np
from hiperparametros_core import FULL
from ablacion_pca_core import predict as original_predict


def predict(bundle,frame):
    required=bundle['spec']['variant']['keep']+['participant','recording','window_start_utc']
    missing=[c for c in required if c not in frame]
    if missing: raise ValueError(f'Entradas necesarias ausentes: {missing}')
    working=frame.copy()
    for column in FULL:
        if column not in working: working[column]=np.nan
    # Missing columns are discarded with every derived feature before preprocessing.
    return original_predict(bundle,working)
