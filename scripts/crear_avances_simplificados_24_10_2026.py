"""Presentación académica de avances: 24 de octubre de 2026."""
from __future__ import annotations

import json
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Pt

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "presentaciones/Avances-Experimentales-Simplificados-24-10-2026.pptx"
AUDIT = ROOT / "documentacion/Verificacion_Avances_Simplificados_24-10-2026.json"
W, H, N = 960, 540, 8

# Paleta deliberadamente corta: papel, tinta, gris y un solo color de énfasis.
PAPER, INK, MUTED, RULE, ACCENT = "FAFAF7", "17252D", "53636B", "C9D2D3", "12686C"
WHITE = "FFFFFF"
prs = Presentation()
prs.slide_width, prs.slide_height = Pt(W), Pt(H)
prs.core_properties.title = "Avances experimentales — tesis MDS"
prs.core_properties.subject = "Temporalidad, fusión, robustez y control negativo"
prs.core_properties.author = "Mario Romero"
prs.core_properties.language = "es-CL"


def rgb(code):
    return RGBColor.from_string(code)


def box(slide, x, y, w, h, fill):
    item = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(x), Pt(y), Pt(w), Pt(h))
    item.fill.solid()
    item.fill.fore_color.rgb = rgb(fill)
    item.line.fill.background()
    return item


def text(slide, value, x, y, w, h, size=18, color=INK, bold=False,
         align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.MIDDLE):
    item = slide.shapes.add_textbox(Pt(x), Pt(y), Pt(w), Pt(h))
    frame = item.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = frame.margin_right = Pt(0)
    frame.margin_top = frame.margin_bottom = Pt(0)
    frame.vertical_anchor = valign
    for i, value_line in enumerate(value.split("\n")):
        paragraph = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        paragraph.text = value_line
        paragraph.alignment = align
        paragraph.space_before = paragraph.space_after = Pt(0)
        paragraph.line_spacing = 1.08
        paragraph.font.name = "Arial"
        paragraph.font.size = Pt(size)
        paragraph.font.bold = bold
        paragraph.font.color.rgb = rgb(color)
    return item


def rule(slide, x, y, w, color=RULE, weight=1):
    box(slide, x, y, w, weight, color)


def base(number, section, title, source):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = rgb(PAPER)
    text(slide, section.upper(), 60, 27, 760, 23, 11, ACCENT, True)
    text(slide, f"{number:02d} / {N:02d}", 831, 27, 69, 23, 11, MUTED,
         align=PP_ALIGN.RIGHT)
    rule(slide, 60, 60, 840)
    text(slide, title, 60, 76, 840, 70, 32, INK, True)
    rule(slide, 60, 483, 840)
    text(slide, source, 60, 490, 840, 37, 9, MUTED)
    return slide


def notes(slide, value):
    slide.notes_slide.notes_text_frame.text = value


# 1. Pregunta de investigación y lectura honesta del estado actual.
s = base(1, "Tesis MDS · 24 de octubre de 2026",
         "Avances experimentales",
         "Fuentes: informes experimentales del 24-10-2026; Toma de Muestra 2.")
text(s, "Pseudoetiquetas de activación y atención", 60, 162, 840, 40,
     21, MUTED)
rule(s, 60, 225, 840, ACCENT, 3)
text(s, "¿Pueden EEG, mirada y pupila predecir una etiqueta calculada con otras señales?",
     60, 242, 790, 91, 29, INK, True)
text(s, "También se evaluó si ayudan el historial temporal y la fusión por modalidad.",
     60, 352, 786, 59, 19, MUTED)
text(s, "Resultado hasta ahora: hay señal alineada en train. La generalización y la validez psicológica siguen abiertas.",
     60, 431, 840, 45, 17, ACCENT, True)
notes(s, "La etiqueta es una referencia computacional, no una medida directa del estado psicológico.")

# 2. Diagrama con entradas y etiqueta, sin lenguaje de 'profesor/estudiante'
# que dificultaba la lectura fuera del contexto del manuscrito.
s = base(2, "Diseño de la tarea",
         "La señal que define la etiqueta no entra al predictor",
         "Fuente: metodología del manuscrito; Evaluacion_Independiente_y_Validez_24-10-2026.md.")
text(s, "ETIQUETA", 60, 163, 323, 25, 12, ACCENT, True)
text(s, "GSR", 60, 194, 323, 52, 38, INK, True)
text(s, "Activación baja, media o alta, según terciles de cada persona y de toda su sesión.",
     60, 263, 335, 91, 18)
rule(s, 451, 163, 1, RULE, 230)
text(s, "PREDICTOR", 506, 163, 394, 25, 12, ACCENT, True)
text(s, "EEG + mirada + pupila", 506, 194, 394, 52, 27, INK, True)
text(s, "El modelo intenta recuperar la etiqueta de GSR. GSR no figura entre sus entradas.",
     506, 263, 374, 91, 18)
rule(s, 60, 393, 840)
text(s, "“Alto” es relativo a esa persona. La etiqueta se calcula offline; no es una medición causal en tiempo real.",
     60, 403, 840, 61, 17, MUTED)
notes(s, "Atención es un objetivo secundario con otra etiqueta, dependiente de mirada y pupila.")

# 3. Tamaño de muestra y unidad de análisis.
s = base(3, "Muestra y evaluación",
         "Train, validation y test se separan por persona",
         "Fuente: Evaluacion_Independiente_y_Validez_24-10-2026.md; protocolo de robustez.")
for x, label, value, detail in [
    (60, "TRAIN", "25", "13.524 ventanas\n5 folds"),
    (348, "VALIDATION", "8", "Usado antes para\ncomparar entradas"),
    (635, "TEST", "8", "4.025 ventanas\nya consultado"),
]:
    text(s, label, x, 168, 236, 28, 12, ACCENT, True)
    text(s, value, x, 199, 222, 95, 69, INK, True)
    text(s, detail, x, 303, 237, 65, 17, MUTED)
rule(s, 327, 169, 1, RULE, 196)
rule(s, 615, 169, 1, RULE, 196)
rule(s, 60, 391, 840)
text(s, "Métrica principal: BA macro por persona", 60, 402, 840, 29, 19, INK, True)
text(s, "Se promedia el recall de las clases presentes en cada persona y luego se promedian las personas con igual peso.",
     60, 432, 840, 40, 15, MUTED)
notes(s, "Los intervalos descriptivos remuestrean personas, no ventanas. P29 se reserva solo para sensibilidad; seis personas fueron excluidas. La BA global por ventana es otra métrica.")

# 4. Tabla factorial compacta. Cada cifra lleva su condición.
s = base(4, "Contraste factorial · train",
         "Historial y fusión: ventajas pequeñas e inciertas",
         "Fuente: Contraste_Temporalidad_Fusion_24-10-2026.md; 25 personas, 5 folds, 2 semillas.")
text(s, "BA macro por persona, fuera de fold", 60, 151, 840, 26, 15, MUTED)
text(s, "Fusión", 60, 197, 170, 27, 13, ACCENT, True)
text(s, "Ventana repetida (C)", 304, 197, 230, 27, 13, ACCENT, True)
text(s, "Historial real (R)", 654, 197, 246, 27, 13, ACCENT, True)
rule(s, 60, 234, 840)
for y, label, c, r in [
    (243, "Temprana (E)", "0,3524", "0,3612"),
    (304, "Tardía (T)", "0,3596", "0,3630"),
]:
    text(s, label, 60, y, 208, 44, 18, INK)
    text(s, c, 304, y, 202, 44, 24, INK, True)
    text(s, r, 654, y, 202, 44, 24, INK, True)
    rule(s, 60, y + 51, 840)
text(s, "Historial E: +0,88 pp  [−0,28; +2,00]", 60, 379, 420, 34, 17, INK, True)
text(s, "Fusión con R: +0,18 pp  [−0,80; +1,37]", 497, 379, 403, 34, 17, INK, True)
text(s, "Ambos intervalos descriptivos incluyen cero.", 60, 437, 840, 30,
     16, ACCENT, True)
notes(s, "R significa historial real; C, ventana actual repetida. E significa fusión temprana; T, tardía. El historial puede abarcar hasta nueve segundos. La fusión tardía usa expertos por modalidad y distinta capacidad.")

# 5. El contraste por clase evita que la media tape un daño concreto.
s = base(5, "Diagnóstico por clase",
         "La clase media cae con fusión tardía",
         "Fuente: Contraste_Temporalidad_Fusion_24-10-2026.md; diagnóstico por clase.")
text(s, "RECALL DE ACTIVACIÓN, CLASE MEDIA", 60, 157, 840, 25, 12, ACCENT, True)
text(s, "23,4 %", 60, 199, 340, 81, 49, INK, True)
text(s, "8,2 %", 560, 199, 340, 81, 49, INK, True, PP_ALIGN.RIGHT)
rule(s, 60, 293, 840)
text(s, "E-R · fusión temprana", 60, 307, 345, 33, 16, MUTED)
text(s, "T-R · fusión tardía", 555, 307, 345, 33, 16, MUTED,
     align=PP_ALIGN.RIGHT)
text(s, "La BA media no refleja una mejora uniforme de las tres clases.",
     60, 363, 840, 37, 21, INK, True)
rule(s, 60, 413, 840)
text(s, "Atención, objetivo secundario: historial temprano −0,65 pp; fusión tardía con historial +1,01 pp. Resultados exploratorios.",
     60, 424, 840, 48, 16, MUTED)
notes(s, "Los intervalos descriptivos de atención fueron [−1,20; −0,05] y [+0,13; +1,86] pp. No corrigen búsqueda previa ni comparaciones múltiples. Los contrastes usan solo train y pseudoetiquetas; no verifican activación o atención psicológica.")

# 6. Barras con la misma escala y la referencia junto al resultado de test.
s = base(6, "Ridge · evaluación adicional",
         "El test queda prácticamente en la referencia",
         "Fuentes: Evaluacion_Independiente_y_Validez_24-10-2026.md; Robustez_Sin_Cohorte_Nueva_24-10-2026.md.")
for y, label, value in [
    (190, "Train, fuera de fold", 0.3843),
    (269, "Test, ensamble fijo", 0.3557),
    (348, "Referencia 1/k en test", 0.3542),
]:
    text(s, label, 60, y - 5, 270, 35, 17, INK)
    box(s, 362, y + 2, 385, 16, RULE)
    box(s, 362, y + 2, 385 * value / .5, 16, ACCENT if y == 269 else MUTED)
    text(s, f"{value:.4f}".replace(".", ","), 774, y - 10, 126, 44, 24,
         INK, True, PP_ALIGN.RIGHT)
text(s, "Escala 0–0,5", 362, 404, 385, 25, 12, MUTED)
rule(s, 60, 438, 840)
text(s, "Solo 4 de 8 personas superan 1/k. Recall de la clase media en test: 21,8 %.",
     60, 445, 840, 31, 16, ACCENT, True)
notes(s, "1/k es la BA de predecir siempre una clase presente. En test, su media es 0,3542 porque una persona tiene dos clases. Train usa un modelo por fold; test promedia probabilidades de cinco modelos. La diferencia train-test es descriptiva; test ya había sido consultado.")

# 7. Dos resultados con sus límites, sin recuadros de métricas.
s = base(7, "Control negativo y sensibilidad",
         "La alineación con GSR importa",
         "Fuentes: Control_Negativo_Temporal_y_Errores_24-10-2026.md; Robustez_Sin_Cohorte_Nueva_24-10-2026.md.")
text(s, "CONTROL TEMPORAL · TRAIN", 60, 158, 392, 26, 12, ACCENT, True)
text(s, "+5,76 pp", 60, 190, 392, 73, 43, INK, True)
text(s, "BA 0,3843 original frente a 0,3268 con la etiqueta GSR desplazada.",
     60, 275, 385, 63, 18)
text(s, "0 de 12 controles alcanzó el original.", 60, 344, 385, 41, 15, MUTED)
rule(s, 478, 159, 1, RULE, 229)
text(s, "DEFINICIÓN DE ETIQUETA · TEST", 516, 158, 384, 26, 12, ACCENT, True)
text(s, "19,7 % y 30,5 %", 516, 190, 384, 73, 34, INK, True)
text(s, "de etiquetas cambian con GSR de 2 s o PCA GSR, respectivamente.",
     516, 275, 384, 63, 18)
text(s, "Las diferencias de BA incluyen cero.", 516, 344, 384, 41, 15, MUTED)
rule(s, 60, 408, 840)
text(s, "El control mide dependencia de la pseudoetiqueta. Aún falta una medida externa del estado psicológico.",
     60, 420, 840, 51, 17, ACCENT, True)
notes(s, "El control preserva frecuencias de clase; el modelo original fue seleccionado con etiquetas de train. Las reglas alternativas de test usan predicciones fijas y no reentrenan el predictor. El control no prueba rendimiento en personas nuevas.")

# 8. Cierre completo: evidencia, alcance y siguiente evaluación.
s = base(8, "Balance",
         "Qué permite concluir esta evidencia",
         "Fuentes: informes del 24-10-2026; Evaluacion_Independiente_y_Validez_24-10-2026.md.")
for y, number, heading, body in [
    (158, "01", "En train", "Ridge capta una relación temporal con la pseudoetiqueta GSR."),
    (255, "02", "Alcance", "No se confirma una ventaja general del historial o la fusión. El test ya se había consultado."),
    (352, "03", "Siguiente paso", "Fijar modelo y protocolo antes de evaluar personas nuevas y contrastar la etiqueta con una medida independiente."),
]:
    text(s, number, 60, y, 62, 56, 23, ACCENT, True)
    text(s, heading, 135, y, 170, 33, 18, INK, True)
    text(s, body, 314, y - 2, 586, 59, 17, INK)
    rule(s, 60, y + 72, 840)
notes(s, "Conservar la distinción entre evaluación de la pseudoetiqueta y validez del constructo. La disponibilidad de datos externos sigue pendiente de confirmación.")

prs.save(DEST)
opened = Presentation(DEST)
assert len(opened.slides) == N
report = {"slides": N, "size_points": [W, H], "visible_text": [], "out_of_bounds": []}
for number, slide in enumerate(opened.slides, 1):
    values = [obj.text for obj in slide.shapes if obj.has_text_frame and obj.text.strip()]
    report["visible_text"].append({"slide": number, "items": len(values),
                                   "characters": sum(map(len, values))})
    for obj in slide.shapes:
        if (obj.left < 0 or obj.top < 0 or obj.left + obj.width > opened.slide_width
                or obj.top + obj.height > opened.slide_height):
            report["out_of_bounds"].append({"slide": number, "shape_id": obj.shape_id})
assert not report["out_of_bounds"]
AUDIT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Presentación creada: {DEST}")
