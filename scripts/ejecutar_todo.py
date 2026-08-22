#!/usr/bin/env python3
"""Ejecuta el flujo completo MDS, estrictamente en orden y deteniendose al fallar."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
CONFIG = ROOT / "config" / "preprocesamiento.json"


def run(label: str, *arguments: str) -> None:
    print(f"\n=== {label} ===", flush=True)
    subprocess.run([sys.executable, *arguments], cwd=ROOT, check=True)


def main() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    tobii = str((ROOT / config["inputs"]["tobii_tsv"]).resolve())
    eeg = str((ROOT / config["inputs"]["eeg_zip"]).resolve())
    sync = ROOT / "resultados" / "sincronizacion"
    run("1/6 Sincronizacion", str(SCRIPTS / "sincronizar_senales.py"),
        "--tobii", tobii, "--eeg", eeg, "--output-dir", str(sync))
    run("2/6 EDA EEG", str(SCRIPTS / "eda_eeg.py"),
        "--zip", eeg, "--manifest", str(sync / "inventario_eeg.csv"),
        "--coordination", str(sync / "coordinacion_sesiones.csv"),
        "--output", str(ROOT / "resultados" / "eda" / "eeg"))
    run("3/6 EDA GSR", str(SCRIPTS / "eda_gsr.py"),
        "--input", tobii, "--manifest", str(sync / "inventario_tobii.csv"),
        "--output", str(ROOT / "resultados" / "eda" / "gsr"))
    run("4/6 EDA pupila y mirada", str(SCRIPTS / "eda_eye_pupil.py"),
        "--input", tobii, "--manifest", str(sync / "inventario_tobii.csv"),
        "--output", str(ROOT / "resultados" / "eda" / "eye_pupil"))
    run("5/6 Figuras de tesis", str(SCRIPTS / "graficos_tesis.py"))
    run("6/6 Preprocesamiento multimodal", str(SCRIPTS / "preprocesamiento_secuencial.py"),
        "--config", str(CONFIG))
    print("\nPipeline completo terminado. Revise resultados/ y el manifiesto de ejecucion.")


if __name__ == "__main__":
    main()
