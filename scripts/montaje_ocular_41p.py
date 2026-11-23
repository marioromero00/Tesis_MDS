"""Comprobación empírica del montaje EEG y de la sincronía EEG–mirada (23-11-2026).

Descriptivo, sin etiquetas ni modelos. Usa la caché de `cache_crudos_ocular.py`.
Por persona:
  - desfase EEG–Tobii: el que maximiza la correlación (en valor absoluto, sobre canales utilizables) entre el
    EEG y tres referencias del seguidor ocular: mirada horizontal, mirada vertical y parpadeo;
  - por canal: correlación con cada referencia en ese desfase y amplitud pico a pico del promedio del EEG
    alineado al inicio de los parpadeos.
Todo en la banda 1–15 Hz. Parpadeo = tramo de 50 a 500 ms con ambos ojos no válidos.

Montaje por defecto de OpenBCI Cyton+Daisy (el que se supuso el 22-11):
  0 Fp1, 1 Fp2, 2 C3, 3 C4, 4 P7, 5 P8, 6 O1, 7 O2, 8 F7, 9 F8, 10 F3, 11 F4, 12 T7, 13 T8, 14 P3, 15 P4.
Qué se espera si el montaje es ese: los parpadeos pegan más en 0 y 1 (Fp1, Fp2) y luego en los frontales;
la mirada horizontal entra con signo opuesto en 8 y 9 (F7, F8); los posteriores (4–7, 14, 15) quedan al final.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.signal import butter, sosfiltfilt
from cache_crudos_ocular import CACHE, ROOT, people

OUT = ROOT / 'resultados/montaje_ocular_41p_23-11-2026'
FS = 125.
SOS = butter(2, [1, 15], btype='bandpass', fs=FS, output='sos')
NAMES = ['Fp1', 'Fp2', 'C3', 'C4', 'P7', 'P8', 'O1', 'O2', 'F7', 'F8', 'F3', 'F4', 'T7', 'T8', 'P3', 'P4']
LAGS = np.arange(-125, 126)
REFS = ['horizontal', 'vertical', 'parpadeo']


def good_channels(x):
    finite = np.isfinite(x).mean(0)
    rail = (np.abs(x) >= 180000).mean(0)
    flat = (np.abs(np.diff(x, axis=0)) < 1e-12).mean(0)
    return (finite >= .95) & (rail <= .01) & (flat < .99)


def blink_onsets(gt, invalid):
    """Inicio (s) de los tramos de 50 a 500 ms con ambos ojos no válidos."""
    edge = np.diff(np.r_[0, invalid.astype(int), 0])
    a, b = np.flatnonzero(edge == 1), np.flatnonzero(edge == -1) - 1
    dur = gt[b] - gt[a]
    keep = (dur >= .05) & (dur <= .5)
    return gt[a][keep], dur[keep]


def references(d):
    """Referencias oculares remuestreadas a los tiempos del EEG (sin desfase), filtradas 1–15 Hz."""
    t, gt = d['eeg_t'], d['gaze_t']
    ok = np.isfinite(d['gaze_x']) & np.isfinite(d['gaze_y'])
    on, dur = blink_onsets(gt, d['both_invalid'])
    blink = np.zeros(len(gt))
    for a, w in zip(on, dur):
        blink[(gt >= a) & (gt <= a + w)] = 1
    raw = np.column_stack([np.interp(t, gt[ok], d['gaze_x'][ok]), np.interp(t, gt[ok], d['gaze_y'][ok]), np.interp(t, gt, blink)])
    return sosfiltfilt(SOS, raw, axis=0), on


def lagged_corr(ref, x, lag):
    """Correlación de ref(t) con x(t + lag muestras), por columna de x."""
    a = ref[max(0, -lag):len(ref) - max(0, lag)]
    b = x[max(0, lag):len(x) - max(0, -lag)]
    a = (a - a.mean()) / (a.std() + 1e-12)
    b = (b - b.mean(0)) / (b.std(0) + 1e-12)
    return (a[:, None] * b).mean(0)


def person(p):
    d = np.load(CACHE / f'{p}.npz')
    t, x = d['eeg_t'], d['eeg']
    inside = (t >= d['gaze_t'][0]) & (t <= d['gaze_t'][-1])   # solo el tramo con seguimiento ocular
    d = dict(d, eeg_t=t[inside], eeg=x[inside])
    t, x = d['eeg_t'], d['eeg']
    good = good_channels(x)
    xf = sosfiltfilt(SOS, np.nan_to_num(x), axis=0)
    ref, onsets = references(d)
    rows, best = [], {}
    for j, name in enumerate(REFS):
        cc = np.array([lagged_corr(ref[:, j], xf, L) for L in LAGS])
        cc[:, ~good] = 0
        i = np.abs(cc).max(1).argmax()
        best[name] = dict(lag_s=float(LAGS[i] / FS), r=cc[i])
    lag = best['parpadeo']['lag_s']
    pre, post = int(.3 * FS), int(.7 * FS)
    idx = np.searchsorted(t, onsets + lag)
    idx = idx[(idx > pre) & (idx < len(t) - post)]
    erp = np.mean([xf[i - pre:i + post] for i in idx], axis=0) if len(idx) else np.full((pre + post, 16), np.nan)
    amp = np.ptp(erp, axis=0)
    for c in range(16):
        rows.append(dict(participant=p, channel=c, name_default=NAMES[c], usable=bool(good[c]),
                         **{f'r_{k}': float(v['r'][c]) if good[c] else np.nan for k, v in best.items()},
                         blink_ptp_uv=float(amp[c]) if good[c] else np.nan))
    info = dict(participant=p, usable_channels=int(good.sum()), blinks=int(len(idx)),
                fs_effective=float(len(t) / (t[-1] - t[0])), max_gap_s=float(np.diff(t).max()),
                **{f'lag_{k}_s': v['lag_s'] for k, v in best.items()},
                **{f'maxabs_r_{k}': float(np.abs(v['r']).max()) for k, v in best.items()})
    return rows, info


def main():
    OUT.mkdir(exist_ok=True)
    rows, infos = [], []
    for p in people():
        r, i = person(p)
        rows += r
        infos.append(i)
        print(i, flush=True)
    ch, pe = pd.DataFrame(rows), pd.DataFrame(infos)
    ch.to_csv(OUT / 'canales_por_persona.csv', index=False)
    pe.to_csv(OUT / 'personas.csv', index=False)
    ch['abs_parpadeo'], ch['abs_horizontal'], ch['abs_vertical'] = ch.r_parpadeo.abs(), ch.r_horizontal.abs(), ch.r_vertical.abs()
    ch['rank_blink'] = ch.groupby('participant').blink_ptp_uv.rank(ascending=False)
    summary = ch.groupby(['channel', 'name_default']).agg(
        usable=('usable', 'sum'), blink_ptp_uv_median=('blink_ptp_uv', 'median'), rank_blink_median=('rank_blink', 'median'),
        abs_r_parpadeo=('abs_parpadeo', 'median'), abs_r_horizontal=('abs_horizontal', 'median'),
        abs_r_vertical=('abs_vertical', 'median')).reset_index()
    summary.to_csv(OUT / 'resumen_canales.csv', index=False)
    wide = ch.pivot(index='participant', columns='channel', values='r_horizontal')
    both = wide[[8, 9]].dropna()
    top = ch[ch.usable].sort_values('blink_ptp_uv', ascending=False).groupby('participant').head(2)
    checks = dict(
        people=len(pe), lag_parpadeo_median_s=float(pe.lag_parpadeo_s.median()),
        lag_parpadeo_iqr_s=[float(pe.lag_parpadeo_s.quantile(q)) for q in (.25, .75)],
        f7_f8_both_usable=len(both), f7_f8_opposite_sign=int((np.sign(both[8]) != np.sign(both[9])).sum()),
        top2_blink_channels_counts=top.channel.value_counts().sort_index().to_dict(),
        people_top_blink_is_fp=int(ch[ch.usable].sort_values('blink_ptp_uv', ascending=False).groupby('participant').head(1).channel.isin([0, 1]).sum()))
    (OUT / 'comprobaciones.json').write_text(json.dumps(checks, indent=2, ensure_ascii=False))
    pd.set_option('display.width', 250)
    print(summary.round(3).to_string(index=False))
    print(json.dumps(checks, indent=2))
    print(pe.round(3).to_string(index=False))


if __name__ == '__main__':
    main()
