#!/usr/bin/env python3
"""Ejecuta sincronización y las EDA del proyecto en orden reproducible."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
STEPS = ["sincronizar_senales.py", "eda_eeg.py", "eda_gsr.py", "eda_eye_pupil.py"]

def main() -> None:
    for name in STEPS:
        print(f"\n=== Ejecutando {name} ===", flush=True)
        subprocess.run([sys.executable, str(SCRIPTS / name)], cwd=ROOT, check=True)
    print("\nPipeline terminado. Revise resultados/ y documentacion/.")

if __name__ == "__main__":
    main()
