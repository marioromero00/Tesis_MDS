"""Entrada compatible: genera la presentacion visual vigente en HTML y PPTX."""
from pathlib import Path
import runpy

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).with_name("generar_tema_visual_23_09_2026.py")), run_name="__main__")
