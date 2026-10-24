"""Genera una presentacion autocontenida de los avances del 24-10-2026."""
from __future__ import annotations

import json
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "presentaciones/Avances-Experimentales-Simplificados-24-10-2026.pptx"
TOTAL = 8
NAVY, BLUE, TEAL = "102A3D", "376B91", "087E83"
PALE, PAPER, INK = "DDF0ED", "F7F8F5", "173348"
MUTED, ORANGE, WHITE, LINE = "5D7180", "C66A44", "FFFFFF", "D9E2E3"
CORAL_PALE = "F9EBE5"
BLUE_PALE = "E7F0F5"

prs = Presentation()
prs.slide_width, prs.slide_height = Pt(960), Pt(540)
prs.core_properties.title = "Avances experimentales autocontenidos — tesis MDS"
prs.core_properties.subject = "Temporalidad, fusión, robustez y control negativo"
prs.core_properties.author = "Mario Romero"
prs.core_properties.language = "es-CL"


def color(code):
    return RGBColor.from_string(code)


def shape(slide, x, y, w, h, fill, kind=MSO_SHAPE.ROUNDED_RECTANGLE):
    item = slide.shapes.add_shape(kind, Pt(x), Pt(y), Pt(w), Pt(h))
    item.fill.solid()
    item.fill.fore_color.rgb = color(fill)
    item.line.fill.background()
    if kind == MSO_SHAPE.ROUNDED_RECTANGLE:
        item.adjustments[0] = 0.10
    return item


def text(slide, value, x, y, w, h, size=17, bold=False, fill=INK,
         align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(Pt(x), Pt(y), Pt(w), Pt(h))
    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = frame.margin_right = Pt(0)
    frame.margin_top = frame.margin_bottom = Pt(0)
    frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    for index, line in enumerate(value.split("\n")):
        p = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        p.text = line
        p.alignment = align
        p.space_before = p.space_after = Pt(0)
        p.line_spacing = 1.04
        p.font.name = "Aptos"
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = color(fill)
    return box


def base(index, section, title, source):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    dark = index == 1
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color(NAVY if dark else PAPER)
    shape(slide, 0, 0, 960, 6, TEAL, MSO_SHAPE.RECTANGLE)
    text(slide, f"{index:02d}  /  {section.upper()}", 48, 27, 820, 22, 11, True,
         PALE if dark else TEAL)
    text(slide, title, 48, 57, 864, 78, 32, True, WHITE if dark else NAVY)
    shape(slide, 48, 483, 864, 1, BLUE if dark else LINE, MSO_SHAPE.RECTANGLE)
    shape(slide, 48, 479, 864 * index / TOTAL, 3, TEAL, MSO_SHAPE.RECTANGLE)
    text(slide, source, 48, 491, 805, 35, 9, False, PALE if dark else MUTED)
    text(slide, f"{index:02d} / {TOTAL:02d}", 852, 491, 58, 22, 10, True,
         PALE if dark else MUTED, PP_ALIGN.RIGHT)
    return slide


def card(slide, x, y, w, h, heading, body, accent=TEAL, heading_size=16,
         body_size=17):
    shape(slide, x, y, w, h, WHITE)
    shape(slide, x, y, w, 5, accent, MSO_SHAPE.RECTANGLE)
    compact = h < 140
    text(slide, heading, x + 19, y + (12 if compact else 17), w - 36,
         28 if compact else 30, heading_size, True, accent)
    text(slide, body, x + 19, y + (43 if compact else 54), w - 38,
         h - (48 if compact else 63), body_size)


def strip(slide, value, y=406, accent=ORANGE, size=17):
    shape(slide, 48, y, 864, 58, CORAL_PALE if accent == ORANGE else PALE)
    shape(slide, 48, y, 5, 58, accent, MSO_SHAPE.RECTANGLE)
    text(slide, value, 68, y + 5, 824, 48, size, True, accent)


def notes(slide, value):
    slide.notes_slide.notes_text_frame.text = value


s = base(1, "Tesis MDS · 24 de octubre de 2026",
         "¿Qué muestran los experimentos recientes?",
         "Fuentes: informes experimentales del 24-10-2026; Toma de Muestra 2")
text(s, "Predicción de pseudoetiquetas de activación y atención", 48, 148, 860, 42,
     23, True, WHITE)
shape(s, 48, 218, 864, 155, BLUE)
shape(s, 48, 218, 7, 155, TEAL, MSO_SHAPE.RECTANGLE)
text(s, "PREGUNTA CENTRAL", 69, 232, 796, 28, 15, True, PALE)
text(s, "¿Pueden EEG, mirada y pupila anticipar una etiqueta calculada con otras señales? ¿Aportan valor el historial o la fusión?",
     69, 273, 797, 77, 23, True, WHITE)
shape(s, 48, 394, 864, 63, PALE)
text(s, "Hay señal alineada en train; la generalización y la validez psicológica siguen abiertas.",
     67, 399, 825, 52, 18, True, NAVY)
notes(s, "La etiqueta es una referencia computacional, no una medida directa del estado psicológico.")

s = base(2, "Diseño y significado de la etiqueta",
         "Profesor y estudiante usan señales separadas",
         "Fuente: metodología del manuscrito; Evaluacion_Independiente_y_Validez_24-10-2026.md")
card(s, 48, 148, 405, 174, "PROFESOR · DEFINE EL OBJETIVO",
     "GSR genera la pseudoetiqueta principal de activación: bajo, medio o alto. Se usan terciles relativos a cada persona y toda su sesión.", TEAL, body_size=17)
card(s, 507, 148, 405, 174, "ESTUDIANTE · HACE LA PREDICCIÓN",
     "EEG, mirada y pupila predicen esa etiqueta. GSR no entra al predictor. Atención es un objetivo secundario con otra etiqueta.", BLUE, body_size=17)
strip(s, "“Alto” significa alto para esa persona; no es un umbral fisiológico común ni una etiqueta causal en tiempo real.", 350, ORANGE, 17)
notes(s, "La construcción de las etiquetas es offline. La etiqueta de atención depende de mirada y pupila.")

s = base(3, "Muestra, evaluación y lectura de la métrica",
         "La partición es por persona",
         "Fuente: Evaluacion_Independiente_y_Validez_24-10-2026.md; protocolo de robustez")
for x, w, label, count, detail, accent in [
    (48, 260, "TRAIN", "25", "13.524 ventanas · 5 folds", TEAL),
    (326, 260, "VALIDATION", "8", "Ya usada para comparar entradas", BLUE),
    (604, 308, "TEST", "8", "4.025 ventanas · ya consultado", ORANGE),
]:
    shape(s, x, 148, w, 190, WHITE)
    shape(s, x, 148, w, 6, accent, MSO_SHAPE.RECTANGLE)
    text(s, label, x + 18, 167, w - 36, 24, 13, True, accent)
    text(s, count, x + 16, 197, w - 32, 74, 58, True, NAVY)
    text(s, detail, x + 18, 285, w - 36, 38, 15, False, MUTED)
shape(s, 48, 356, 864, 91, NAVY)
text(s, "BA macro por persona", 68, 367, 770, 31, 20, True, WHITE)
text(s, "Recall por clase presente, promediado por persona con igual peso.",
     68, 401, 795, 33, 16, False, PALE)
notes(s, "P29 se reserva solo para sensibilidad; seis personas fueron excluidas. La BA global por ventana es otra métrica.")

s = base(4, "Contraste factorial 2 × 2 · train",
         "El historial aporta poco en activación",
         "Fuente: Contraste_Temporalidad_Fusion_24-10-2026.md; 25 personas, 5 folds, 2 semillas")
text(s, "TCN: historial real (R) o ventana actual repetida (C); fusión temprana (E) o tardía (T).", 48, 140, 864, 38, 17)
for x, label, value, col in [(48, "E-C", "0,3524", MUTED), (269, "E-R", "0,3612", TEAL),
                             (490, "T-C", "0,3596", BLUE), (711, "T-R", "0,3630", BLUE)]:
    shape(s, x, 197, 201, 87, PAPER)
    text(s, label, x + 14, 207, 172, 25, 16, True, col)
    text(s, value, x + 14, 237, 172, 35, 26, True, NAVY)
text(s, "BA macro por persona fuera de fold", 48, 290, 864, 23, 13, False, MUTED)
card(s, 48, 327, 405, 70, "HISTORIAL: E-R − E-C", "+0,88 pp · intervalo [−0,28; +2,00]", TEAL, 15, 16)
card(s, 507, 327, 405, 70, "FUSIÓN: T-R − E-R", "+0,18 pp · intervalo [−0,80; +1,37]", BLUE, 15, 16)
strip(s, "Ambos intervalos incluyen cero; no hay ventaja general confirmada.", 411, ORANGE, 18)
notes(s, "El historial puede abarcar hasta nueve segundos. La fusión tardía usa expertos por modalidad y distinta capacidad.")

s = base(5, "Diagnóstico del contraste",
         "Una media similar oculta diferencias por clase",
         "Fuente: Contraste_Temporalidad_Fusion_24-10-2026.md; diagnóstico por clase")
shape(s, 48, 150, 405, 163, WHITE)
shape(s, 48, 150, 405, 5, ORANGE, MSO_SHAPE.RECTANGLE)
text(s, "ACTIVACIÓN · CLASE MEDIA", 67, 165, 365, 27, 15, True, ORANGE)
text(s, "23,4 %", 68, 203, 170, 49, 31, True, NAVY)
text(s, "→", 231, 207, 40, 41, 25, True, ORANGE)
text(s, "8,2 %", 280, 203, 152, 49, 31, True, ORANGE)
text(s, "E-R · fusión temprana       T-R · fusión tardía", 68, 262, 355, 31,
     13, False, MUTED)
card(s, 507, 150, 405, 163, "ATENCIÓN · OBJETIVO SECUNDARIO",
     "El historial temprano baja BA en 0,65 pp. La fusión tardía con historial sube 1,01 pp; resultados exploratorios.", BLUE, body_size=18)
strip(s, "La pequeña diferencia media de activación no representa una mejora uniforme de las tres clases.", 346, NAVY, 18)
text(s, "Los contrastes usan solo train y pseudoetiquetas; no verifican activación o atención psicológica.", 50, 418, 860, 43, 15, False, MUTED)
notes(s, "Para atención, los intervalos descriptivos de esos contrastes fueron [-1,20; -0,05] y [+0,13; +1,86] pp. No corrigen búsqueda previa ni comparaciones múltiples.")

s = base(6, "Ridge de activación · evaluación adicional",
         "En test, la BA queda cerca de la referencia",
         "Fuentes: Evaluacion_Independiente_y_Validez_24-10-2026.md; Robustez_Sin_Cohorte_Nueva_24-10-2026.md")
for y, label, value, col in [(156, "Train · fuera de fold", "0,3843", TEAL),
                             (228, "Test · ensamble fijo", "0,3557", BLUE),
                             (300, "Referencia matemática 1/k · test", "0,3542", MUTED)]:
    text(s, label, 48, y, 323, 32, 17, True)
    shape(s, 379, y + 5, 396, 22, PALE)
    shape(s, 379, y + 5, 396 * float(value.replace(",", ".")) / .5, 22, col)
    text(s, value, 796, y - 2, 113, 39, 23, True, NAVY)
text(s, "1/k = BA de predecir siempre una clase presente; en test la media es 0,3542 porque una persona tiene dos clases.", 48, 363, 864, 45, 15, False, MUTED)
strip(s, "Solo 4/8 personas superan 1/k. El recall de la clase media en test es 21,8 %.", 412, ORANGE, 18)
notes(s, "Train usa un modelo por fold; test promedia probabilidades de cinco modelos. La diferencia train-test es descriptiva. La referencia 1/k no es un clasificador desplegable.")

s = base(7, "Control negativo y sensibilidad",
         "La alineación importa; la etiqueta influye",
         "Fuentes: Control_Negativo_Temporal_y_Errores_24-10-2026.md; Robustez_Sin_Cohorte_Nueva_24-10-2026.md")
shape(s, 48, 149, 405, 213, WHITE)
shape(s, 48, 149, 405, 5, TEAL, MSO_SHAPE.RECTANGLE)
text(s, "CONTROL TEMPORAL · TRAIN", 67, 167, 362, 26, 15, True, TEAL)
text(s, "+5,76 pp", 67, 205, 363, 55, 35, True, NAVY)
text(s, "BA 0,3843 original vs. 0,3268 con etiqueta desplazada.",
     67, 272, 360, 47, 16)
text(s, "Ninguno de 12 controles alcanzó el original.",
     67, 326, 360, 24, 13, True, MUTED)
shape(s, 507, 149, 405, 213, WHITE)
shape(s, 507, 149, 405, 5, BLUE, MSO_SHAPE.RECTANGLE)
text(s, "OTRAS REGLAS · TEST", 526, 167, 362, 26, 15, True, BLUE)
text(s, "19,7–30,5 %", 526, 205, 365, 55, 31, True, NAVY)
text(s, "de etiquetas cambian con GSR de 2 s o PCA GSR.",
     526, 272, 360, 47, 16)
text(s, "Las diferencias de BA son inciertas.",
     526, 326, 360, 24, 13, True, MUTED)
strip(s, "El control apoya dependencia de la pseudoetiqueta GSR, no validez psicológica ni rendimiento en personas nuevas.", 389, ORANGE, 17)
notes(s, "El control preserva frecuencias de clase; el modelo original fue seleccionado con etiquetas de train. Las reglas alternativas de test no reentrenan el predictor.")

s = base(8, "Balance y siguiente evidencia necesaria",
         "Qué se puede afirmar ahora",
         "Fuentes: informes del 24-10-2026; Evaluacion_Independiente_y_Validez_24-10-2026.md")
card(s, 48, 145, 864, 88, "OBSERVADO",
     "En train, la predicción Ridge depende de la alineación temporal con su pseudoetiqueta GSR.", TEAL, body_size=18)
card(s, 48, 244, 864, 88, "LÍMITE DE LA CONCLUSIÓN",
     "No se confirma una ventaja general del historial o la fusión; test ya se había consultado y falta una medida externa del estado psicológico.", ORANGE, body_size=17)
card(s, 48, 343, 864, 109, "PARA CONFIRMAR",
     "Fijar predictor y protocolo antes de evaluar personas no utilizadas en decisiones previas; contrastar la pseudoetiqueta con una medida independiente y apropiada a su escala temporal.", BLUE, body_size=17)
notes(s, "Conservar la distinción entre evaluación de la pseudoetiqueta y validez del constructo. La disponibilidad de datos externos sigue pendiente de confirmación.")

prs.save(DEST)
opened = Presentation(DEST)
assert len(opened.slides) == TOTAL
report = {"slides": TOTAL, "size_points": [960, 540], "visible_text": [],
          "out_of_bounds": []}
for index, slide in enumerate(opened.slides, 1):
    values = [item.text for item in slide.shapes if item.has_text_frame and item.text.strip()]
    report["visible_text"].append({"slide": index, "items": len(values),
                                   "characters": sum(map(len, values))})
    for item in slide.shapes:
        if (item.left < 0 or item.top < 0 or
                item.left + item.width > opened.slide_width or
                item.top + item.height > opened.slide_height):
            report["out_of_bounds"].append({"slide": index, "shape_id": item.shape_id})
assert not report["out_of_bounds"]
(ROOT / "documentacion/Verificacion_Avances_Simplificados_24-10-2026.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Presentación creada: {DEST}")
