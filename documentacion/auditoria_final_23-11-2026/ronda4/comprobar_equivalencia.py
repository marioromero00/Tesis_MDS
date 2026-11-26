#!/usr/bin/env python3
"""Comprobación de equivalencia de cifras tras la edición editorial (ronda 4).

Compara los cuatro borradores antes (carpeta pre_editorial) y después de la
edición. No modifica ningún archivo.

Reglas:
  - toda cifra de {RD, DF} antes debe estar después en RD (o en DF);
  - toda cifra de CO antes debe estar después en CO o en RD;
  - toda cifra de SP antes debe estar después en SP (o en RD);
  - toda cifra nueva de un archivo debe venir de alguno de los cuatro
    archivos antes de la edición.

"Cifra" = número con coma decimal (con su signo), intervalo entre corchetes,
fracción (28/41, "28 de 41"), porcentaje, valor p, entero con separador de
miles y, como categoría secundaria, entero seguido de unidad ("41 personas").

Además busca términos vetados y remisiones a secciones inexistentes, y cuenta
palabras.

Uso: python3 comprobar_equivalencia.py [-v]
"""
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ANTES = AQUI / "pre_editorial"
DESPUES = Path("/Users/mario/Proyectos/tesis-mds/documentos/01 Tesis MDS/Escritura")

ARCH = {
    "RD": "Borrador Resultados y Discusión 23-11-2026.md",
    "DF": "Borrador Discusión fisiológica 23-11-2026.md",
    "CO": "Borrador Conclusiones 23-11-2026.md",
    "SP": "Borrador Secciones pendientes 23-11-2026.md",
}

MENOS = "−"
SIG = r"[+\-" + MENOS + r"]"
DEC = r"\d+(?:\.\d{3})*,\d+"

UNIDADES = (
    "personas?|participantes?|ventanas?|particiones|partición|hojas|canales|"
    "grupos?|componentes|réplicas|permutaciones|pares|filas|segmentos|"
    "parámetros|variables|columnas|sesiones|grabaciones|muestras|etapas|"
    "divisiones|posiciones|fijaciones|referencias|contrastes|pruebas|"
    "s|ms|Hz|µV|minutos|carpetas"
)

NUM_PAL = {
    "una": "1", "un": "1", "dos": "2", "tres": "3", "cuatro": "4",
    "cinco": "5", "seis": "6", "siete": "7", "ocho": "8", "nueve": "9",
    "diez": "10", "doce": "12", "trece": "13",
}


def limpiar(texto: str) -> str:
    texto = re.sub(r"https?://\S+", " ", texto)
    return texto


def cifras(texto: str) -> dict:
    t = limpiar(texto)
    out = {k: set() for k in ("decimal", "intervalo", "fraccion", "porcentaje", "p", "miles", "conteo")}
    # intervalos entre corchetes (con algún dígito y ; o ,)
    for m in re.finditer(r"\[([^\[\]\n]*\d[^\[\]\n]*)\]", t):
        cuerpo = m.group(1)
        if re.search(r"\d", cuerpo) and (";" in cuerpo or "," in cuerpo) and not cuerpo.startswith("!"):
            out["intervalo"].add("[" + re.sub(r"\s+", "", cuerpo) + "]")
    # decimales con signo
    for m in re.finditer(r"(?<![\d,.])(" + SIG + r")?(" + DEC + r")(?![\d])", t):
        signo = m.group(1) or ""
        # un guion ASCII pegado a un dígito anterior es un rango, no un signo
        if signo == "-":
            signo = MENOS
        out["decimal"].add(signo + m.group(2))
    # fracciones
    for m in re.finditer(r"(?<![\d/.,])(\d+)/(\d+)(?![\d/])", t):
        out["fraccion"].add(f"{m.group(1)}/{m.group(2)}")
    for m in re.finditer(r"(?<![\d.,])(\d+) de (?:las |los |sus )?(\d+(?:\.\d{3})*)(?![\d,])", t):
        out["fraccion"].add(f"{m.group(1)}/{m.group(2)}")
    # porcentajes (número o rango)
    for m in re.finditer(r"(\d+(?:,\d+)?(?:[–-]\d+(?:,\d+)?)?)\s?%", t):
        out["porcentaje"].add(m.group(1) + "%")
    # valores p
    for m in re.finditer(r"\bp(?: de)?(?: \(?Holm\)?| sin ajustar)?\s*(?:=|<|menor que|bajo)?\s*(<\s*)?(\d,\d+)", t):
        out["p"].add("p:" + ("<" if m.group(1) else "") + m.group(2))
    for m in re.finditer(r"<\s*(\d,\d+)", t):
        out["p"].add("p:<" + m.group(1))
    # enteros con separador de miles
    for m in re.finditer(r"(?<![\d.,/])(\d{1,3}(?:\.\d{3})+)(?![\d]|,\d)", t):
        out["miles"].add(m.group(1))
    # conteos: entero (o numeral en palabras) + unidad
    for m in re.finditer(r"(?<![\d.,/+\-" + MENOS + r"])(\d+)\s(?:de las |de los )?(" + UNIDADES + r")\b", t):
        out["conteo"].add(m.group(1) + " " + raiz(m.group(2)))
    for m in re.finditer(r"\b(" + "|".join(NUM_PAL) + r")\s(" + UNIDADES + r")\b", t, flags=re.I):
        out["conteo"].add(NUM_PAL[m.group(1).lower()] + " " + raiz(m.group(2)))
    return out


def raiz(u: str) -> str:
    u = u.lower()
    if u in ("partición", "particiones"):
        return "partición"
    if u in ("s", "ms", "hz", "µv"):
        return u
    return re.sub(r"(es|s)$", "", u) if u.endswith("s") else u


def plano(d: dict, incluir_conteo=True) -> set:
    s = set()
    for k, v in d.items():
        if k == "conteo" and not incluir_conteo:
            continue
        s |= {f"{k}|{x}" for x in v}
    return s


def palabras(texto: str) -> int:
    return len(texto.split())


def main():
    verbose = "-v" in sys.argv
    antes = {k: (ANTES / v).read_text(encoding="utf-8") for k, v in ARCH.items()}
    desp = {k: (DESPUES / v).read_text(encoding="utf-8") for k, v in ARCH.items()}
    ca = {k: plano(cifras(v)) for k, v in antes.items()}
    cd = {k: plano(cifras(v)) for k, v in desp.items()}

    print("== Palabras ==")
    for k in ARCH:
        print(f"  {k}: antes {palabras(antes[k])}, después {palabras(desp[k])}")

    reglas = [
        ("RD+DF", ca["RD"] | ca["DF"], cd["RD"] | cd["DF"], cd["RD"]),
        ("CO", ca["CO"], cd["CO"] | cd["RD"], cd["CO"]),
        ("SP", ca["SP"], cd["SP"] | cd["RD"], cd["SP"]),
    ]
    total_falta = 0
    print("\n== Cifras faltantes ==")
    for nombre, a, d, propio in reglas:
        falta = sorted(a - d)
        fuerte = [x for x in falta if not x.startswith("conteo|")]
        debil = [x for x in falta if x.startswith("conteo|")]
        total_falta += len(fuerte)
        print(f"  {nombre}: {len(a)} cifras antes; faltan {len(fuerte)} (y {len(debil)} conteos con unidad por revisar)")
        for x in fuerte:
            print("     FALTA", x)
        for x in debil:
            print("     conteo?", x)
        if nombre == "RD+DF":
            solo_df = sorted(x for x in a if x in d and x not in propio and not x.startswith("conteo|"))
            print(f"     (presentes solo en DF y no en RD después: {len(solo_df)})")
            for x in solo_df:
                print("        solo DF:", x)
        elif verbose:
            fuera = sorted(x for x in a if x in d and x not in propio)
            print(f"     (presentes después solo en RD: {len(fuera)})")
            for x in fuera:
                print("        en RD:", x)

    print("\n== Cifras nuevas ==")
    todo_antes = set().union(*ca.values())
    total_nuevas = 0
    for k in ARCH:
        nuevas = sorted(cd[k] - ca[k])
        sin_origen = [x for x in nuevas if x not in todo_antes]
        fuerte = [x for x in sin_origen if not x.startswith("conteo|")]
        debil = [x for x in sin_origen if x.startswith("conteo|")]
        total_nuevas += len(fuerte)
        print(f"  {k}: {len(nuevas)} nuevas en el archivo; {len(fuerte)} sin origen en los cuatro archivos (y {len(debil)} conteos por revisar)")
        for x in fuerte:
            print("     NUEVA", x)
        for x in debil:
            print("     conteo?", x)
        if verbose:
            for x in nuevas:
                if x in todo_antes:
                    print("     (viene de otro archivo)", x)

    print("\n== Términos vetados ==")
    vetos = [
        ("profesor PCA", r"profesor PCA"),
        ("al menos un tercio / al menos en un tercio", r"al menos (en )?un tercio"),
        ("la quinta decisión", r"quinta decisión"),
        ("indicio", r"indicio"),
        ("debe presentarse", r"debe presentarse"),
        ("Modelos Profesores", r"Modelos Profesores"),
    ]
    for nombre, pat in vetos:
        for k in ARCH:
            for i, linea in enumerate(desp[k].splitlines(), 1):
                for m in re.finditer(pat, linea):
                    ctx = linea[max(0, m.start() - 70): m.end() + 70]
                    print(f"  [{nombre}] {k}:{i}: …{ctx}…")
    print("  (fin de la búsqueda; sin líneas arriba = sin apariciones)")

    print("\n== Remisiones a secciones ==")
    enc = {}
    for k in ARCH:
        enc[k] = set(re.findall(r"^#{2,4}\s+(\d+(?:\.\d+){1,2})\b", desp[k], flags=re.M))
    conocidas = enc["RD"] | enc["CO"] | enc["SP"]
    # secciones del esqueleto que SP cita sin redactarlas
    esqueleto = {"1.6", "4.2", "4.4", "4.5.1", "4.6.2", "5.1", "5.2", "2.2", "2.3", "2.4", "2.5",
                 "2.6", "2.7", "2.8", "2.9", "2.10", "2.11", "2.12", "3.3"}
    malas = 0
    for k in ARCH:
        for i, linea in enumerate(desp[k].splitlines(), 1):
            if re.match(r"^#{1,4}\s", linea):
                continue
            for m in re.finditer(r"(?:secci[oó]n(?:es)?|en|ver|RD|SP|CO)\s+((?:\d+\.\d+(?:\.\d+)?)(?:(?:,| y| o| a)\s+\d+\.\d+(?:\.\d+)?)*)", linea):
                for n in re.findall(r"\d+\.\d+(?:\.\d+)?", m.group(1)):
                    if n in conocidas or n in esqueleto:
                        continue
                    if k == "DF":
                        continue
                    malas += 1
                    print(f"  REMISIÓN SIN DESTINO {k}:{i}: {n}: …{linea[max(0, m.start()-40): m.end()+40]}…")
    print(f"  encabezados RD: {sorted(enc['RD'], key=lambda s: [int(x) for x in s.split('.')])}")
    print(f"  remisiones sin destino: {malas}")

    print(f"\nRESUMEN: faltantes {total_falta}; nuevas sin origen {total_nuevas}; remisiones sin destino {malas}")


if __name__ == "__main__":
    main()
