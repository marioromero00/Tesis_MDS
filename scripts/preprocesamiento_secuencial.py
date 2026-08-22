"""Pipeline secuencial y reproducible para EEG, GSR, pupila y eye tracking.

El TSV y el ZIP se leen sin modificarlos. Tobii define segmentos de estimulo y
ventanas UTC; EEG se extrae exactamente sobre esas ventanas. La salida principal
es un CSV multimodal, acompanado por auditoria, hashes y configuracion efectiva.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import re
import shutil
import sys
import tempfile
import time
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy.signal import butter, filtfilt, find_peaks


TOBII_COLUMNS = [
    "Recording timestamp", "Participant name", "Recording name",
    "Recording date UTC", "Recording start time UTC", "Timeline name",
    "Event", "Event value", "Presented Stimulus name", "Sensor",
    "Galvanic skin response (GSR)", "Pupil diameter left",
    "Pupil diameter right", "Validity left", "Validity right",
    "Gaze point X", "Gaze point Y", "Eye movement type",
    "Gaze event duration", "Eye movement type index",
]


def sha256_file(path: Path, block_size: int = 8 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(block_size):
            digest.update(block)
    return digest.hexdigest()


def participant_number(value: str) -> int | None:
    match = re.fullmatch(r"P0*(\d+)", str(value).strip(), re.IGNORECASE)
    return int(match.group(1)) if match else None


def normalize_participant(value: str) -> str | None:
    number = participant_number(value)
    return f"P{number}" if number is not None and 1 <= number <= 48 else None


def resolve(repo: Path, value: str) -> Path:
    path = Path(value)
    return path.resolve() if path.is_absolute() else (repo / path).resolve()


def parse_recording_start(date_value: str, time_value: str) -> pd.Timestamp:
    text = f"{date_value} {time_value}"
    return pd.to_datetime(text, format="%m/%d/%Y %H:%M:%S.%f", utc=True)


def slope(values: np.ndarray, seconds: np.ndarray) -> float:
    mask = np.isfinite(values) & np.isfinite(seconds)
    if mask.sum() < 2 or np.ptp(seconds[mask]) == 0:
        return math.nan
    return float(np.polyfit(seconds[mask], values[mask], 1)[0])


def safe_stat(values: np.ndarray, fn) -> float:
    finite = values[np.isfinite(values)]
    return float(fn(finite)) if finite.size else math.nan


def partition_tobii(tsv: Path, work: Path, chunk_rows: int) -> dict[str, Path]:
    """Etapa 1: particiona columnas necesarias por participante, conservando orden."""
    paths: dict[str, Path] = {}
    written: set[str] = set()
    for chunk in pd.read_csv(
        tsv, sep="\t", usecols=TOBII_COLUMNS, chunksize=chunk_rows,
        low_memory=False, dtype=str,
    ):
        chunk["participant"] = chunk["Participant name"].map(normalize_participant)
        chunk = chunk[chunk["participant"].notna()]
        for participant, part in chunk.groupby("participant", sort=False):
            path = work / f"{participant}.csv"
            part.to_csv(path, mode="a", header=participant not in written, index=False)
            paths[participant] = path
            written.add(participant)
    return paths


def stimulus_segments(frame: pd.DataFrame) -> pd.DataFrame:
    """Propaga el estimulo Tobii y crea segmentos contiguos sin cruzar cambios."""
    frame = frame.sort_values("Recording timestamp", kind="stable").copy()
    frame["t_us"] = pd.to_numeric(frame["Recording timestamp"], errors="coerce")
    stimulus = frame["Presented Stimulus name"].replace(r"^\s*$", np.nan, regex=True)
    frame["stimulus"] = stimulus.ffill()
    frame["segment_id"] = frame["stimulus"].ne(frame["stimulus"].shift()).cumsum()
    return frame[frame["t_us"].notna() & frame["stimulus"].notna()]


def prepare_gsr(frame: pd.DataFrame, config: dict) -> pd.DataFrame:
    gsr = frame[["t_us", "Galvanic skin response (GSR)"]].copy()
    gsr["value"] = pd.to_numeric(gsr.pop("Galvanic skin response (GSR)"), errors="coerce")
    gsr = gsr.dropna().drop_duplicates("t_us").sort_values("t_us")
    if gsr.empty:
        return gsr.assign(z=np.nan, tonic=np.nan, phasic=np.nan)
    values = gsr["value"].to_numpy(float)
    std = np.nanstd(values)
    z = (values - np.nanmean(values)) / std if std > 0 else np.zeros_like(values)
    tonic = np.full_like(z, np.nan)
    hz = float(config["gsr"]["nominal_hz"])
    cutoff = float(config["gsr"]["tonic_lowpass_hz"])
    if z.size > 3 * 2:
        b, a = butter(2, cutoff / (hz / 2), btype="low")
        pad = 3 * max(len(a), len(b))
        if z.size > pad:
            tonic = filtfilt(b, a, z)
    if not np.isfinite(tonic).any():
        tonic = np.full_like(z, np.nanmean(z))
    gsr["z"] = z
    gsr["tonic"] = tonic
    gsr["phasic"] = z - tonic
    return gsr


def prepare_pupil(frame: pd.DataFrame, max_gap_s: float) -> pd.DataFrame:
    pupil = frame[["t_us", "Pupil diameter left", "Pupil diameter right", "Validity left", "Validity right"]].copy()
    left = pd.to_numeric(pupil["Pupil diameter left"], errors="coerce")
    right = pd.to_numeric(pupil["Pupil diameter right"], errors="coerce")
    valid_left = pupil["Validity left"].astype(str).str.lower().eq("valid")
    valid_right = pupil["Validity right"].astype(str).str.lower().eq("valid")
    left = left.where(valid_left)
    right = right.where(valid_right)
    pupil["both_valid"] = valid_left & valid_right
    pupil["value"] = pd.concat([left, right], axis=1).mean(axis=1, skipna=True)
    pupil = pupil.drop_duplicates("t_us").sort_values("t_us")
    # Interpolacion solo cuando la separacion entre observaciones validas no supera el limite.
    limit = max(1, int(round(max_gap_s * 60)))
    pupil["value_interp"] = pupil["value"].interpolate(limit=limit, limit_area="inside")
    values = pupil["value_interp"].to_numpy(float)
    std = np.nanstd(values)
    pupil["z"] = (values - np.nanmean(values)) / std if std > 0 else np.nan
    return pupil


def modality_features(frame: pd.DataFrame, start_us: float, end_us: float, config: dict,
                      gsr: pd.DataFrame, pupil: pd.DataFrame) -> dict:
    duration = (end_us - start_us) / 1e6
    result: dict[str, float | int] = {}

    gw = gsr[(gsr.t_us >= start_us) & (gsr.t_us < end_us)]
    expected_gsr = duration * config["gsr"]["nominal_hz"]
    result["gsr_n"] = int(len(gw))
    result["gsr_coverage"] = min(1.0, len(gw) / expected_gsr) if expected_gsr else 0.0
    for name, column, fn in [
        ("gsr_mean_z", "z", np.mean), ("gsr_std_z", "z", np.std),
        ("gsr_min_z", "z", np.min), ("gsr_max_z", "z", np.max),
        ("gsr_tonic_mean_z", "tonic", np.mean), ("gsr_phasic_mean_z", "phasic", np.mean),
    ]:
        result[name] = safe_stat(gw[column].to_numpy(float), fn) if not gw.empty else math.nan
    result["gsr_slope_z_s"] = slope(gw.z.to_numpy(float), gw.t_us.to_numpy(float) / 1e6) if len(gw) else math.nan
    phasic = gw.phasic.to_numpy(float) if len(gw) else np.array([])
    peaks, props = find_peaks(phasic, prominence=config["gsr"]["scr_prominence_z"]) if phasic.size >= 3 else (np.array([]), {})
    result["gsr_scr_count"] = int(peaks.size)
    result["gsr_scr_mean_prominence_z"] = float(np.mean(props["prominences"])) if peaks.size else 0.0

    pw = pupil[(pupil.t_us >= start_us) & (pupil.t_us < end_us)]
    expected_pupil = duration * config["pupil"]["nominal_hz"]
    result["pupil_n"] = int(len(pw))
    result["pupil_coverage"] = min(1.0, pw.value_interp.notna().sum() / expected_pupil) if expected_pupil else 0.0
    result["pupil_both_valid_fraction"] = float(pw.both_valid.mean()) if len(pw) else math.nan
    for name, column, fn in [
        ("pupil_mean_z", "z", np.mean), ("pupil_std_z", "z", np.std),
        ("pupil_min_z", "z", np.min), ("pupil_max_z", "z", np.max),
    ]:
        result[name] = safe_stat(pw[column].to_numpy(float), fn) if len(pw) else math.nan
    result["pupil_slope_z_s"] = slope(pw.z.to_numpy(float), pw.t_us.to_numpy(float) / 1e6) if len(pw) else math.nan

    ew = frame[(frame.t_us >= start_us) & (frame.t_us < end_us)]
    gx = pd.to_numeric(ew["Gaze point X"], errors="coerce").to_numpy(float)
    gy = pd.to_numeric(ew["Gaze point Y"], errors="coerce").to_numpy(float)
    gaze_valid = np.isfinite(gx) & np.isfinite(gy)
    expected_gaze = duration * config["pupil"]["nominal_hz"]
    result["gaze_n"] = int(gaze_valid.sum())
    result["gaze_coverage"] = min(1.0, gaze_valid.sum() / expected_gaze) if expected_gaze else 0.0
    result["gaze_dispersion_x_px"] = safe_stat(gx, np.std)
    result["gaze_dispersion_y_px"] = safe_stat(gy, np.std)
    result["gaze_dispersion_2d_px"] = float(np.hypot(result["gaze_dispersion_x_px"], result["gaze_dispersion_y_px"]))
    if gaze_valid.sum() >= 2:
        coords = np.column_stack([gx[gaze_valid], gy[gaze_valid]])
        result["gaze_path_length_px"] = float(np.linalg.norm(np.diff(coords, axis=0), axis=1).sum())
    else:
        result["gaze_path_length_px"] = math.nan
    events = ew.dropna(subset=["Eye movement type index"]).drop_duplicates("Eye movement type index")
    event_type = events["Eye movement type"].astype(str).str.lower()
    durations = pd.to_numeric(events["Gaze event duration"], errors="coerce")
    fix = event_type.eq("fixation")
    sac = event_type.eq("saccade")
    result["fixation_count"] = int(fix.sum())
    result["fixation_total_ms"] = float(durations[fix].sum()) if fix.any() else 0.0
    result["fixation_mean_ms"] = float(durations[fix].mean()) if fix.any() else math.nan
    result["fixation_median_ms"] = float(durations[fix].median()) if fix.any() else math.nan
    result["saccade_count"] = int(sac.sum())
    result["saccade_mean_ms"] = float(durations[sac].mean()) if sac.any() else math.nan
    return result


def build_tobii_windows(partition: Path, participant: str, config: dict) -> pd.DataFrame:
    raw = pd.read_csv(partition, low_memory=False)
    rows: list[dict] = []
    window_us = config["window_seconds"] * 1e6
    step_us = config["step_seconds"] * 1e6
    for recording, rec in raw.groupby("Recording name", sort=False):
        frame = stimulus_segments(rec)
        frame = frame[~frame["stimulus"].isin(config.get("excluded_stimuli", []))]
        if frame.empty:
            continue
        first = rec.iloc[0]
        recording_start = parse_recording_start(first["Recording date UTC"], first["Recording start time UTC"])
        gsr = prepare_gsr(frame, config)
        pupil = prepare_pupil(frame, config["pupil"]["maximum_interpolation_gap_seconds"])
        for segment_id, segment in frame.groupby("segment_id", sort=False):
            segment_start = float(segment.t_us.min())
            segment_end = float(segment.t_us.max())
            if segment_end - segment_start < window_us:
                continue
            starts = np.arange(segment_start, segment_end - window_us + 1, step_us)
            for window_index, start_us in enumerate(starts):
                end_us = start_us + window_us
                start_utc = recording_start + pd.to_timedelta(start_us, unit="us")
                end_utc = recording_start + pd.to_timedelta(end_us, unit="us")
                base = {
                    "participant": participant, "recording": recording,
                    "timeline": first.get("Timeline name", ""),
                    "stimulus": str(segment.stimulus.iloc[0]),
                    "segment_id": int(segment_id), "window_index": int(window_index),
                    "window_start_recording_s": start_us / 1e6,
                    "window_end_recording_s": end_us / 1e6,
                    "window_start_utc": start_utc.isoformat(),
                    "window_end_utc": end_utc.isoformat(),
                }
                base.update(modality_features(frame, start_us, end_us, config, gsr, pupil))
                rows.append(base)
    return pd.DataFrame(rows)


def read_eeg_entry(zf: zipfile.ZipFile, member: str, channels: int) -> tuple[np.ndarray, np.ndarray]:
    with zf.open(member) as source:
        frame = pd.read_csv(source, comment="%", low_memory=False)
    channel_cols = [f" EXG Channel {i}" for i in range(channels)]
    if not set(channel_cols).issubset(frame.columns):
        channel_cols = [f"EXG Channel {i}" for i in range(channels)]
    timestamp_col = " Timestamp" if " Timestamp" in frame.columns else "Timestamp"
    signal = frame[channel_cols].apply(pd.to_numeric, errors="coerce").to_numpy(float)
    timestamps = pd.to_numeric(frame[timestamp_col], errors="coerce").to_numpy(float)
    return timestamps, signal


def eeg_features(signal: np.ndarray, hz: float, bands: dict) -> dict:
    result: dict[str, float | int] = {"eeg_n": int(signal.shape[0])}
    if signal.shape[0] < 4 or signal.shape[1] == 0:
        for name in ["eeg_rms_uv", "eeg_std_uv", "eeg_peak_to_peak_uv", "eeg_line_noise_ratio", *[f"eeg_{b}_relative" for b in bands]]:
            result[name] = math.nan
        return result
    centered = signal - np.nanmedian(signal, axis=0, keepdims=True)
    centered = np.nan_to_num(centered)
    result["eeg_rms_uv"] = float(np.sqrt(np.mean(centered ** 2)))
    result["eeg_std_uv"] = float(np.mean(np.std(centered, axis=0)))
    result["eeg_peak_to_peak_uv"] = float(np.mean(np.ptp(centered, axis=0)))
    tapered = centered * np.hanning(centered.shape[0])[:, None]
    power = np.abs(np.fft.rfft(tapered, axis=0)) ** 2
    freqs = np.fft.rfftfreq(centered.shape[0], 1 / hz)
    total_mask = (freqs >= 1) & (freqs <= 45)
    total = float(power[total_mask].sum())
    for band, limits in bands.items():
        mask = (freqs >= limits[0]) & (freqs < limits[1])
        result[f"eeg_{band}_relative"] = float(power[mask].sum() / total) if total > 0 else math.nan
    line = (freqs >= 49) & (freqs <= 51)
    result["eeg_line_noise_ratio"] = float(power[line].sum() / power.sum()) if power.sum() > 0 else math.nan
    return result


def add_eeg(windows: pd.DataFrame, config: dict, manifest_path: Path, eeg_zip: Path) -> pd.DataFrame:
    """Etapa 3: agrega EEG a las ventanas UTC ya definidas por Tobii."""
    manifest = pd.read_csv(manifest_path)
    manifest = manifest[manifest["participant"].map(participant_number).between(1, 48)]
    manifest = manifest.sort_values("match_status").drop_duplicates("participant", keep="first")
    mapping = manifest.set_index("participant").to_dict("index")
    output: list[pd.DataFrame] = []
    hz = float(config["eeg"]["nominal_hz"])
    min_coverage = config["minimum_coverage"]["eeg"]
    excluded = set(config["eeg"]["excluded_quality_participants"])
    with zipfile.ZipFile(eeg_zip) as zf:
        for participant, part in windows.groupby("participant", sort=False):
            part = part.copy()
            info = mapping.get(participant)
            part["eeg_match_status"] = info["match_status"] if info else "sin_candidato"
            part["eeg_quality_usable"] = participant not in excluded and bool(info)
            features: list[dict] = []
            if not info:
                empty = eeg_features(np.empty((0, 0)), hz, config["eeg"]["bands_hz"])
                empty["eeg_coverage"] = 0.0
                empty["eeg_window_valid"] = False
                features = [empty.copy() for _ in range(len(part))]
            else:
                timestamps, signal = read_eeg_entry(zf, info["eeg_file"], int(config["eeg"]["channels"]))
                for row in part.itertuples(index=False):
                    start = pd.Timestamp(row.window_start_utc).timestamp()
                    end = pd.Timestamp(row.window_end_utc).timestamp()
                    mask = (timestamps >= start) & (timestamps < end)
                    feat = eeg_features(signal[mask], hz, config["eeg"]["bands_hz"])
                    feat["eeg_coverage"] = min(1.0, feat["eeg_n"] / (config["window_seconds"] * hz))
                    feat["eeg_window_valid"] = feat["eeg_coverage"] >= min_coverage
                    features.append(feat)
            part = pd.concat([part.reset_index(drop=True), pd.DataFrame(features)], axis=1)
            output.append(part)
    return pd.concat(output, ignore_index=True) if output else windows


def quality_flags(frame: pd.DataFrame, config: dict) -> pd.DataFrame:
    frame = frame.copy()
    for modality, column in [("gsr", "gsr_coverage"), ("pupil", "pupil_coverage"), ("gaze", "gaze_coverage")]:
        frame[f"{modality}_window_valid"] = frame[column] >= config["minimum_coverage"][modality]
    required = ["gsr_window_valid", "pupil_window_valid", "gaze_window_valid", "eeg_window_valid"]
    frame["multimodal_window_valid"] = frame[required].all(axis=1) & frame["eeg_quality_usable"]
    return frame


def audit(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    ordered = sorted(frame["participant"].unique(), key=lambda x: participant_number(x) or 999)
    for participant in ordered:
        part = frame[frame["participant"] == participant]
        rows.append({
            "participant": participant, "windows": len(part),
            "stimuli": part["stimulus"].nunique(),
            "gsr_valid_windows": int(part.gsr_window_valid.sum()),
            "pupil_valid_windows": int(part.pupil_window_valid.sum()),
            "gaze_valid_windows": int(part.gaze_window_valid.sum()),
            "eeg_valid_windows": int(part.eeg_window_valid.sum()),
            "multimodal_valid_windows": int(part.multimodal_window_valid.sum()),
            "eeg_quality_usable": bool(part.eeg_quality_usable.iloc[0]),
            "eeg_match_status": part.eeg_match_status.iloc[0],
        })
    return pd.DataFrame(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config/preprocesamiento.json")
    parser.add_argument("--chunk-rows", type=int, default=250_000)
    parser.add_argument("--only-participants", nargs="*", help="P1 P2 ...; para prueba controlada")
    parser.add_argument("--skip-hashes", action="store_true", help="Solo para prueba; ejecucion final debe calcularlos")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    config_path = resolve(repo, args.config)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    tobii = resolve(repo, config["inputs"]["tobii_tsv"])
    eeg_zip = resolve(repo, config["inputs"]["eeg_zip"])
    manifest_path = resolve(repo, config["inputs"]["session_manifest"])
    output = resolve(repo, config["output_dir"])
    for path in [tobii, eeg_zip, manifest_path]:
        if not path.exists():
            raise FileNotFoundError(path)
    output.mkdir(parents=True, exist_ok=True)
    work = output / ".work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    started = time.time()
    print("[1/6] Validando insumos y registrando procedencia", flush=True)
    provenance = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "config_sha256": sha256_file(config_path),
        "pipeline_sha256": sha256_file(Path(__file__).resolve()),
        "requirements_sha256": sha256_file(repo / "requirements.txt"),
        "inputs": {},
    }
    configured_paths = config["inputs"]
    for name, path in [("tobii_tsv", tobii), ("eeg_zip", eeg_zip), ("session_manifest", manifest_path)]:
        provenance["inputs"][name] = {
            "configured_path": configured_paths[name], "bytes": path.stat().st_size,
            "sha256": None if args.skip_hashes else sha256_file(path),
        }
    print("[2/6] Particionando TSV Tobii por participante", flush=True)
    partitions = partition_tobii(tobii, work, args.chunk_rows)
    selected = {normalize_participant(p) for p in (args.only_participants or [])}
    if selected:
        partitions = {p: path for p, path in partitions.items() if p in selected}
    print("[3/6] Extrayendo GSR, pupila y eye tracking por ventanas", flush=True)
    parts = []
    for participant in sorted(partitions, key=lambda p: participant_number(p) or 999):
        print(f"      {participant}", flush=True)
        parts.append(build_tobii_windows(partitions[participant], participant, config))
    windows = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()
    if windows.empty:
        raise RuntimeError("No se generaron ventanas Tobii")
    print("[4/6] Extrayendo EEG sobre las mismas ventanas UTC", flush=True)
    windows = add_eeg(windows, config, manifest_path, eeg_zip)
    windows = quality_flags(windows, config)
    print("[5/6] Escribiendo productos y auditoria", flush=True)
    windows_path = output / "caracteristicas_multimodales.csv"
    audit_path = output / "auditoria_participantes.csv"
    windows.to_csv(windows_path, index=False, float_format="%.8g")
    audit_frame = audit(windows)
    audit_frame.to_csv(audit_path, index=False)
    shutil.copy2(config_path, output / "configuracion_efectiva.json")
    provenance.update({
        "runtime_seconds": round(time.time() - started, 3),
        "python": sys.version, "platform": platform.platform(),
        "versions": {"numpy": np.__version__, "pandas": pd.__version__, "scipy": scipy.__version__},
        "parameters": config,
        "outputs": {
            "caracteristicas_multimodales.csv": {"rows": len(windows), "sha256": sha256_file(windows_path)},
            "auditoria_participantes.csv": {"rows": len(audit_frame), "sha256": sha256_file(audit_path)},
        },
        "status_counts": {str(k): int(v) for k, v in Counter(windows.eeg_match_status).items()},
        "valid_multimodal_windows": int(windows.multimodal_window_valid.sum()),
    })
    (output / "manifiesto_ejecucion.json").write_text(json.dumps(provenance, indent=2, ensure_ascii=False), encoding="utf-8")
    shutil.rmtree(work)
    print(f"[6/6] Listo: {len(windows):,} ventanas; {provenance['valid_multimodal_windows']:,} multimodales validas", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
