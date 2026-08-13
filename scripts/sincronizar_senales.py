#!/usr/bin/env python3
"""Construye un manifiesto reproducible para coordinar Tobii/GSR y EEG OpenBCI.

No altera ni descomprime los datos originales. Lee el TSV por streaming y las
cabeceras de los TXT/CSV dentro del ZIP. El resultado es una tabla de emparejado
por participante y proximidad temporal, más diagnósticos de sesiones.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import zipfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


PARTICIPANT_RE = re.compile(r"(?<![A-Z0-9])P\s*0*(\d{1,3})(?!\d)", re.I)


@dataclass
class TobiiRecording:
    participant: str
    recording: str
    timeline: str
    start_utc: datetime
    duration_s: float


@dataclass
class EEGSession:
    session: str
    participant: str | None
    kind: str
    source_file: str
    format: str
    start_utc: datetime
    sample_rate_hz: float | None
    channels: int | None


def participant_id(text: str) -> str | None:
    match = PARTICIPANT_RE.search(text.replace("_", " "))
    return f"P{int(match.group(1))}" if match else None


def parse_tobii_utc(date_value: str, time_value: str) -> datetime:
    # El export usa mm/dd/yyyy y ofrece columnas UTC explícitas.
    return datetime.strptime(
        f"{date_value.strip()} {time_value.strip()}", "%m/%d/%Y %H:%M:%S.%f"
    ).replace(tzinfo=timezone.utc)


def read_tobii_recordings(path: Path) -> list[TobiiRecording]:
    wanted = {
        "Participant name", "Recording name", "Timeline name",
        "Recording date UTC", "Recording start time UTC", "Recording duration",
    }
    found: dict[tuple[str, str, str, str], TobiiRecording] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        missing = wanted.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Faltan columnas Tobii: {sorted(missing)}")
        for row in reader:
            participant = (row["Participant name"] or "").strip()
            recording = (row["Recording name"] or "").strip()
            date_utc = (row["Recording date UTC"] or "").strip()
            time_utc = (row["Recording start time UTC"] or "").strip()
            if not participant or not recording or not date_utc or not time_utc:
                continue
            key = (participant, recording, date_utc, time_utc)
            if key not in found:
                duration = float(row["Recording duration"] or 0) / 1000.0
                found[key] = TobiiRecording(
                    participant=participant_id(participant) or participant,
                    recording=recording,
                    timeline=(row["Timeline name"] or "").strip(),
                    start_utc=parse_tobii_utc(date_utc, time_utc),
                    duration_s=duration,
                )
    return sorted(found.values(), key=lambda item: item.start_utc)


def session_kind(name: str) -> str:
    low = name.lower()
    if "test" in low or "prueba" in low or "sold" in low:
        return "test"
    if participant_id(name):
        return "principal"
    return "sin_identificador"


def _first_nonempty_lines(stream: Iterable[bytes], limit: int = 12) -> list[str]:
    result: list[str] = []
    for raw in stream:
        line = raw.decode("utf-8-sig", errors="replace").strip()
        if line:
            result.append(line)
        if len(result) >= limit:
            break
    return result


def _parse_txt(lines: list[str]) -> tuple[datetime, float | None, int | None]:
    rate = channels = None
    header_index = None
    for index, line in enumerate(lines):
        if line.startswith("%Sample Rate"):
            rate = float(line.split("=", 1)[1].replace("Hz", "").strip())
        elif line.startswith("%Number of channels"):
            channels = int(line.split("=", 1)[1].strip())
        elif line.startswith("Sample Index"):
            header_index = index
            break
    if header_index is None or header_index + 1 >= len(lines):
        raise ValueError("TXT sin cabecera o primera muestra")
    header = next(csv.reader([lines[header_index]], skipinitialspace=True))
    data = next(csv.reader([lines[header_index + 1]], skipinitialspace=True))
    columns = {name.strip(): i for i, name in enumerate(header)}
    formatted = data[columns["Timestamp (Formatted)"]].strip()
    local_naive = datetime.strptime(formatted, "%Y-%m-%d %H:%M:%S.%f")
    # Los TXT fueron grabados en Chile (UTC-4 en las fechas de agosto de 2025).
    start = local_naive.replace(tzinfo=timezone.utc).timestamp() + 4 * 3600
    return datetime.fromtimestamp(start, timezone.utc), rate, channels


def _parse_brainflow(lines: list[str]) -> tuple[datetime, float | None, int | None]:
    values = lines[0].split("\t")
    if len(values) < 31:
        raise ValueError("CSV BrainFlow con menos de 31 columnas")
    return datetime.fromtimestamp(float(values[30]), timezone.utc), 125.0, 16


def read_eeg_sessions(path: Path) -> tuple[list[EEGSession], list[dict[str, str]]]:
    sessions: dict[str, EEGSession] = {}
    diagnostics: list[dict[str, str]] = []
    with zipfile.ZipFile(path) as archive:
        entries = sorted(archive.infolist(), key=lambda e: (e.filename.count("/"), e.filename))
        # TXT tiene timestamp legible y metadatos; CSV es fallback.
        entries.sort(key=lambda e: 0 if e.filename.lower().endswith(".txt") else 1)
        for entry in entries:
            if entry.is_dir() or not entry.filename.lower().endswith((".txt", ".csv")):
                continue
            session = entry.filename.split("/", 1)[0]
            if entry.file_size == 0:
                diagnostics.append({"file": entry.filename, "status": "vacio"})
                continue
            if session in sessions:
                continue
            try:
                with archive.open(entry) as stream:
                    lines = _first_nonempty_lines(stream)
                if entry.filename.lower().endswith(".txt"):
                    start, rate, channels = _parse_txt(lines)
                    fmt = "OpenBCI TXT"
                else:
                    start, rate, channels = _parse_brainflow(lines)
                    fmt = "BrainFlow TSV"
                sessions[session] = EEGSession(
                    session=session,
                    participant=participant_id(session),
                    kind=session_kind(session),
                    source_file=entry.filename,
                    format=fmt,
                    start_utc=start,
                    sample_rate_hz=rate,
                    channels=channels,
                )
            except Exception as exc:  # deja trazabilidad sin detener todo el inventario
                diagnostics.append({"file": entry.filename, "status": f"error: {exc}"})
    return sorted(sessions.values(), key=lambda item: item.start_utc), diagnostics


def match_sessions(tobii: list[TobiiRecording], eeg: list[EEGSession], max_offset_s: float) -> list[dict]:
    rows: list[dict] = []
    for recording in tobii:
        same_participant = [s for s in eeg if s.participant == recording.participant]
        pool = same_participant or eeg
        ranked = sorted(pool, key=lambda s: abs((recording.start_utc - s.start_utc).total_seconds()))
        best = ranked[0] if ranked else None
        offset = (recording.start_utc - best.start_utc).total_seconds() if best else None
        status = "sin_candidato"
        if best:
            if best.participant != recording.participant:
                status = "revisar_participante"
            elif abs(offset) > max_offset_s:
                status = "revisar_offset"
            elif best.kind != "principal":
                status = "revisar_tipo_sesion"
            else:
                status = "candidato"
        rows.append({
            "participant": recording.participant,
            "tobii_recording": recording.recording,
            "timeline": recording.timeline,
            "tobii_start_utc": recording.start_utc.isoformat(),
            "tobii_duration_s": recording.duration_s,
            "eeg_session": best.session if best else "",
            "eeg_file": best.source_file if best else "",
            "eeg_start_utc": best.start_utc.isoformat() if best else "",
            "offset_tobii_minus_eeg_s": offset,
            "drift_scale": 1.0,
            "match_status": status,
        })
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tobii", type=Path, default=Path("datos/Toma_muestras_v2 Data export.tsv"))
    parser.add_argument("--eeg", type=Path, default=Path("datos/eeg_recordings_exp_V2.zip"))
    parser.add_argument("--output-dir", type=Path, default=Path("resultados/sincronizacion"))
    parser.add_argument("--max-offset-s", type=float, default=180.0)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    print("Indexando grabaciones Tobii/GSR (lectura streaming)...")
    tobii = read_tobii_recordings(args.tobii)
    print("Indexando sesiones EEG dentro del ZIP...")
    eeg, diagnostics = read_eeg_sessions(args.eeg)
    matches = match_sessions(tobii, eeg, args.max_offset_s)

    write_csv(args.output_dir / "coordinacion_sesiones.csv", matches)
    write_csv(args.output_dir / "inventario_tobii.csv", [
        {**asdict(x), "start_utc": x.start_utc.isoformat()} for x in tobii
    ])
    write_csv(args.output_dir / "inventario_eeg.csv", [
        {**asdict(x), "start_utc": x.start_utc.isoformat()} for x in eeg
    ])
    with (args.output_dir / "diagnosticos.json").open("w", encoding="utf-8") as handle:
        json.dump(diagnostics, handle, ensure_ascii=False, indent=2)

    counts: dict[str, int] = {}
    for row in matches:
        counts[row["match_status"]] = counts.get(row["match_status"], 0) + 1
    print(f"Tobii: {len(tobii)} | EEG: {len(eeg)} | Estados: {counts}")
    print(f"Resultados: {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
