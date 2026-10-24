"""Verifica la presentación final y sus números contra los resultados v2."""
import hashlib
import json
from pathlib import Path
import zipfile

import pandas as pd
from pptx import Presentation

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / "presentaciones/Presentacion-Final-Tesis-PCA-24-10-2026.pptx"
RESULTS = ROOT / "resultados/pca_senales_v2_24-10-2026"
OUTPUT = ROOT / "documentacion/Verificacion_Presentacion_Final_PCA_24-10-2026.json"


def slide_text(slide) -> str:
    return " ".join(shape.text for shape in slide.shapes if shape.has_text_frame)


def decimal(value: float) -> str:
    return f"{value:.4f}".replace(".", ",")


def main() -> None:
    prs = Presentation(DECK)
    if len(prs.slides) != 11:
        raise ValueError("Se esperaban diez láminas")
    with zipfile.ZipFile(DECK) as archive:
        if archive.testzip() is not None:
            raise ValueError("PowerPoint ZIP dañado")
    for slide in list(prs.slides)[7:]:
        for shape in slide.shapes:
            if (shape.left < 0 or shape.top < 0 or shape.left + shape.width > prs.slide_width
                    or shape.top + shape.height > prs.slide_height):
                raise ValueError("Forma fuera de la lámina")
    manifest = json.loads((RESULTS / "manifiesto_estudiante.json").read_text(encoding="utf-8"))
    metrics = pd.read_csv(RESULTS / "metricas_estudiante.csv")
    control = pd.read_csv(RESULTS / "control_estimulo.csv")
    slide9 = slide_text(prs.slides[8])
    slide10 = slide_text(prs.slides[9])
    slide11 = slide_text(prs.slides[10])
    for task in ["attention", "arousal"]:
        components = manifest["models"][task]["retained_components"]
        total = sum(entry["components"] for entry in components.values())
        if f"{total} componentes" not in slide9:
            raise ValueError(f"Faltan componentes de {task}")
        for model in ["full_logistic", "pca_logistic", "pca_1pc_logistic"]:
            value = metrics.loc[metrics.task.eq(task) & metrics.model.eq(model)
                                & metrics.split.eq("test"), "balanced_accuracy"].iloc[0]
            if decimal(value) not in slide10:
                raise ValueError(f"Falta BA de {task}/{model}")
        stimulus = control.loc[control.task.eq(task) & control.split.eq("test"),
                               "balanced_accuracy"].iloc[0]
        if decimal(stimulus) not in slide10:
            raise ValueError(f"Falta control de estímulo de {task}")
    retry_dir = ROOT / "resultados/mejora_condicional_v2_24-10-2026"
    retry = json.loads((retry_dir / "reporte_condicional.json").read_text(encoding="utf-8"))
    one_pc = json.loads((retry_dir / "reporte_un_pc.json").read_text(encoding="utf-8"))
    for task in ["attention", "arousal"]:
        for split in ["validation", "test"]:
            for key in ["baseline", "pca"]:
                value = retry["tasks"][task][split][key]["balanced_accuracy"]
                if decimal(value) not in slide11:
                    raise ValueError(f"Falta BA reintento {task}/{split}/{key}")
    for key in ["pca_one", "pca_shuffled"]:
        value = one_pc["tasks"]["attention"][key]["balanced_accuracy"]
        if decimal(value) not in slide11:
            raise ValueError(f"Falta BA un PC atención/{key}")
    result = {"slides": len(prs.slides), "added_slides": 4,
              "pptx_sha256": hashlib.sha256(DECK.read_bytes()).hexdigest(),
              "metricas_sha256": hashlib.sha256((RESULTS / "metricas_estudiante.csv").read_bytes()).hexdigest(),
              "control_sha256": hashlib.sha256((RESULTS / "control_estimulo.csv").read_bytes()).hexdigest(),
              "retry_sha256": hashlib.sha256((retry_dir / "reporte_condicional.json").read_bytes()).hexdigest(),
              "numbers_verified": True, "bounds_verified": True, "zip_verified": True}
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
