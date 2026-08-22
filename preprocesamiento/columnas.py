"""
Resolución de nombres de columna del export de Tobii Pro Lab.

El export trae 99 columnas y los nombres cambian entre versiones de Tobii Pro Lab
y entre configuraciones de exportación. En vez de asumir un nombre, cada campo
declara una lista de candidatos y se resuelve contra las columnas reales del
archivo. Si un campo obligatorio no aparece, el pipeline falla de inmediato y
muestra qué encontró, en vez de arrastrar un NaN silencioso.
"""
from __future__ import annotations


# Cada entrada: campo interno -> candidatos, en orden de preferencia.
CANDIDATOS: dict[str, list[str]] = {
    "participante":   ["Participant name", "Participant", "Participant ID"],
    "grabacion":      ["Recording name", "Recording"],
    "fecha":          ["Recording date"],
    "hora_inicio":    ["Recording start time", "Recording start time UTC"],
    "ts_us":          ["Recording timestamp", "Recording timestamp [μs]",
                       "Recording timestamp microseconds"],
    "gsr":            ["Galvanic skin response (GSR)", "GSR", "Galvanic skin response"],
    "pupila":         ["Pupil diameter filtered", "Pupil diameter"],
    "pupila_izq":     ["Pupil diameter left", "Pupil diameter left [mm]"],
    "pupila_der":     ["Pupil diameter right", "Pupil diameter right [mm]"],
    "validez_izq":    ["Validity left", "Pupil validity left"],
    "validez_der":    ["Validity right", "Pupil validity right"],
    "mov_tipo":       ["Eye movement type"],
    "mov_indice":     ["Eye movement type index"],
    "mov_duracion":   ["Gaze event duration", "Gaze event duration [ms]"],
    "fix_x":          ["Fixation point X", "Fixation point X (MCSnorm)"],
    "fix_y":          ["Fixation point Y", "Fixation point Y (MCSnorm)"],
    "gaze_x":         ["Gaze point X", "Gaze point X (MCSnorm)", "Fixation point X"],
    "gaze_y":         ["Gaze point Y", "Gaze point Y (MCSnorm)", "Fixation point Y"],
    "evento":         ["Event"],
    "evento_valor":   ["Event value"],
    "estimulo":       ["Presented Stimulus name", "Presented Media name", "Stimulus name"],
}

# Sin estos el pipeline no puede correr.
OBLIGATORIAS = ["participante", "fecha", "hora_inicio", "ts_us", "mov_tipo"]

# Sin estas se degrada, pero sigue: se marca la modalidad como no disponible.
POR_MODALIDAD = {
    "gsr":    ["gsr"],
    "pupila": ["pupila"],
    "mirada": ["mov_indice", "mov_duracion", "gaze_x", "gaze_y"],
}


def resolver(columnas_reales) -> dict[str, str | None]:
    """Mapea campo interno -> nombre real de columna (o None si no está)."""
    disponibles = set(columnas_reales)
    mapa: dict[str, str | None] = {}
    for campo, candidatos in CANDIDATOS.items():
        mapa[campo] = next((c for c in candidatos if c in disponibles), None)
    return mapa


def validar(mapa: dict[str, str | None], columnas_reales) -> dict[str, bool]:
    """
    Verifica las columnas obligatorias y reporta qué modalidades quedan
    disponibles. Lanza ValueError si falta una obligatoria.
    """
    faltan = [c for c in OBLIGATORIAS if mapa.get(c) is None]
    if faltan:
        raise ValueError(
            "Faltan columnas obligatorias en el export de Tobii: "
            + ", ".join(f"{c} (candidatos: {CANDIDATOS[c]})" for c in faltan)
            + f"\nColumnas encontradas en el archivo: {sorted(columnas_reales)}"
        )
    return {
        modalidad: all(mapa.get(c) is not None for c in campos)
        for modalidad, campos in POR_MODALIDAD.items()
    }


def informe(mapa: dict[str, str | None], disponibles: dict[str, bool]) -> str:
    lineas = ["Mapeo de columnas Tobii:"]
    for campo, real in mapa.items():
        lineas.append(f"  {campo:14s} -> {real if real else '(no encontrada)'}")
    lineas.append("Modalidades disponibles:")
    for modalidad, ok in disponibles.items():
        lineas.append(f"  {modalidad:8s} {'sí' if ok else 'NO — se omite'}")
    return "\n".join(lineas)
