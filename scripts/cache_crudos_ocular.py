"""Caché local de crudos por persona para el análisis de artefactos oculares (23-11-2026).

Lee el ZIP de EEG y el export de Tobii (fuera de Git) y deja, por persona, un .npz con:
  eeg_t (s, UTC), eeg (n x 16, µV), gaze_t (s, UTC), gaze_x, gaze_y (px; NaN si no hay mirada),
  both_invalid (ambos ojos no válidos), movement (0 fijación, 1 sacada, 2 ojos no encontrados, 3 otro).
No usa etiquetas ni modifica nada del repositorio. Los tiempos de Tobii se pasan a UTC igual que en
`preprocesamiento_secuencial.py` (inicio UTC de la grabación + marca de tiempo de la grabación en µs).
"""
from __future__ import annotations
import zipfile
from pathlib import Path
import numpy as np
import pandas as pd
from preprocesamiento_secuencial import read_eeg_entry, normalize_participant, parse_recording_start

ROOT = Path(__file__).resolve().parents[1]
RAW = (ROOT / '../../datos/locales/v2_2025').resolve()
CACHE = RAW / 'cache_ocular'
COLS = ['Recording timestamp', 'Participant name', 'Recording date UTC', 'Recording start time UTC', 'Sensor',
        'Validity left', 'Validity right', 'Gaze point X', 'Gaze point Y', 'Eye movement type']
MOVE = {'Fixation': 0, 'Saccade': 1, 'EyesNotFound': 2}


def people():
    parts = pd.read_csv(ROOT / 'resultados/modelado/particion_participantes.csv')
    return sorted(parts[parts.split.isin(['train', 'validation', 'test'])].participant)


def main():
    CACHE.mkdir(exist_ok=True)
    keep = set(people())
    gaze = {p: [] for p in keep}
    for chunk in pd.read_csv(RAW / 'Toma_muestras_v2 Data export.tsv', sep='\t', usecols=COLS, chunksize=500_000,
                             low_memory=False, dtype=str):
        chunk = chunk[chunk.Sensor.eq('Eye Tracker')]
        chunk = chunk.assign(participant=chunk['Participant name'].map(normalize_participant))
        for p, g in chunk[chunk.participant.isin(keep)].groupby('participant', sort=False):
            gaze[p].append(g)
    mapping = pd.read_csv(ROOT / 'resultados/sincronizacion/coordinacion_sesiones.csv').set_index('participant')
    with zipfile.ZipFile(RAW / 'eeg_recordings_exp_V2.zip') as archive:
        for p in sorted(keep):
            g = pd.concat(gaze[p])
            starts = (g['Recording date UTC'] + ' ' + g['Recording start time UTC']).unique()
            assert len(starts) == 1, (p, starts)
            start = parse_recording_start(g['Recording date UTC'].iloc[0], g['Recording start time UTC'].iloc[0]).timestamp()
            t = start + pd.to_numeric(g['Recording timestamp']).to_numpy(float) / 1e6
            order = np.argsort(t, kind='stable')
            invalid = (~g['Validity left'].str.lower().eq('valid') & ~g['Validity right'].str.lower().eq('valid')).to_numpy()
            ts, signal = read_eeg_entry(archive, mapping.loc[p].eeg_file, 16)
            ok = np.isfinite(ts)
            ts, signal = ts[ok], signal[ok]
            o = np.argsort(ts, kind='stable')
            np.savez_compressed(
                CACHE / f'{p}.npz', eeg_t=ts[o], eeg=signal[o], gaze_t=t[order],
                gaze_x=pd.to_numeric(g['Gaze point X'], errors='coerce').to_numpy(float)[order],
                gaze_y=pd.to_numeric(g['Gaze point Y'], errors='coerce').to_numpy(float)[order],
                both_invalid=invalid[order],
                movement=g['Eye movement type'].map(MOVE).fillna(3).to_numpy(int)[order])
            print(p, len(ts), 'muestras EEG', len(t), 'muestras de mirada', flush=True)


if __name__ == '__main__':
    main()
