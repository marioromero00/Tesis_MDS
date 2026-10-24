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
NAVY, BLUE, TEAL = "102B42", "215C80", "087F86"
PALE, PAPER, INK = "EAF3F4", "F7F9FB", "173047"
MUTED, ORANGE, WHITE, LINE = "536675", "A45A22", "FFFFFF", "D4DFE5"

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
        p.line_spacing = 1.08
        p.font.name = "Arial"
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = color(fill)
    return box


def base(index, section, title, source):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color(WHITE)
    shape(slide, 0, 0, 960, 7, NAVY, MSO_SHAPE.RECTANGLE)
    text(slide, section.upper(), 48, 27, 820, 22, 11, True, TEAL)
    text(slide, title, 48, 57, 864, 74, 30, True, NAVY)
    shape(slide, 48, 480, 864, 1, LINE, MSO_SHAPE.RECTANGLE)
    text(slide, source, 48, 488, 805, 37, 9, False, MUTED)
    text(slide, f"{index} / {TOTAL}", 858, 489, 52, 22, 10, True,
         MUTED, PP_ALIGN.RIGHT)
    return slide


def card(slide, x, y, w, h, heading, body, accent=TEAL, heading_size=16,
         body_size=17):
    shape(slide, x, y, w, h, PAPER)
    shape(slide, x, y, 5, h, accent, MSO_SHAPE.RECTANGLE)
    compact = h < 140
    text(slide, heading, x + 19, y + (8 if compact else 12), w - 36,
         28 if compact else 30, heading_size, True, accent)
    text(slide, body, x + 19, y + (39 if compact else 48), w - 38,
         h - (44 if compact else 59), body_size)


def strip(slide, value, y=406, accent=ORANGE, size=17):
    shape(slide, 48, y, 864, 58, PALE)
    text(slide, value, 65, y + 5, 829, 48, size, True, accent)


def notes(slide, value):
    slide.notes_slide.notes_text_frame.text = value


s = base(1, "Tesis MDS · 24 de octubre de 2026",
         "¿Qué muestran los experimentos recientes?",
         "Fuentes: informes experimentales del 24-10-2026; Toma de Muestra 2")
text(s, "Predicción de pseudoetiquetas de activación y atención", 48, 148, 860, 42, 23, True)
card(s, 48, 218, 864, 155, "PREGUNTA CENTRAL",
     "¿Pueden EEG, mirada y pupila anticipar una etiqueta calculada con otras señales, y aportan valor el historial temporal o la fusión por modalidad?",
     TEAL, body_size=20)
strip(s, "Conclusión actual: hay señal alineada en train; la generalización y la validez psicológica siguen abiertas.", 395, NAVY, 17)
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
card(s, 48, 148, 260, 124, "TRAIN · 25 PERSONAS",
     "13.524 ventanas. Cinco folds; cada persona se predice fuera del fold donde se ajustó el modelo.", TEAL, body_size=15)
card(s, 326, 148, 260, 124, "VALIDATION · 8",
     "Ya se usó para comparar entradas en rondas anteriores.", BLUE, body_size=16)
card(s, 604, 148, 308, 124, "TEST · 8 PERSONAS",
     "4.025 ventanas. Ya consultado: evaluación adicional, sin confirmación independiente.", ORANGE, body_size=15)
card(s, 48, 292, 864, 95, "BA MACRO POR PERSONA",
     "Para cada persona se promedia el recall de las clases presentes; luego se promedian las personas con igual peso.", TEAL, body_size=17)
strip(s, "Los intervalos descriptivos remuestrean personas, no ventanas.", 402, NAVY, 17)
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
card(s, 48, 150, 405, 163, "ACTIVACIÓN · CLASE MEDIA",
     "Al pasar de fusión temprana con historial (E-R) a tardía (T-R), el recall cae de 23,4 % a 8,2 %.", ORANGE, body_size=19)
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
card(s, 48, 149, 405, 213, "CONTROL TEMPORAL · TRAIN",
     "Ridge original: BA 0,3843. Al desplazar circularmente la etiqueta GSR en el ajuste: media 0,3268 en 12 controles. Diferencia +5,76 pp; 0/12 alcanzan el original.", TEAL, body_size=17)
card(s, 507, 149, 405, 213, "OTRAS REGLAS · TEST",
     "Con predicciones fijas, GSR 2 s cambia 19,7 % de etiquetas; PCA GSR cambia 30,5 %. Las diferencias de BA tienen intervalos que incluyen cero.", BLUE, body_size=17)
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
