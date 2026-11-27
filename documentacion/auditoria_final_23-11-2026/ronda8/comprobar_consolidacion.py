#!/usr/bin/env python3
"""Comprobación de la consolidación de legibilidad (ronda 8, 27-11-2026).

Compara la versión previa (carpeta pre_consolidacion) con la actual de los tres
borradores y comprueba que la consolidación no perdió ni agregó contenido:

a) cifras: toda cifra presente antes en un archivo sigue en ese archivo; lista
   faltantes, nuevas y las que bajaron de frecuencia;
b) citas (autor, año) y notas de trabajo;
c) tablas Markdown con igual número de celdas por fila y remisiones
   "sección X.Y" que apuntan a un encabezado existente;
d) palabras antes y después, y frecuencia en RD de cinco frases.

No modifica ningún archivo. Uso: python3 comprobar_consolidacion.py
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PREVIO = AQUI / "pre_consolidacion"
ACTUAL = Path("/Users/mario/Proyectos/tesis-mds/documentos/01 Tesis MDS/Escritura")
ARCHIVOS = {
    "RD": "Borrador Resultados y Discusión 23-11-2026.md",
    "SP": "Borrador Secciones pendientes 23-11-2026.md",
    "CO": "Borrador Conclusiones 23-11-2026.md",
}
FRASES = [
    "no es una confirmación independiente",
    "personas ya consultadas",
    "cerca de un tercio",
    "soporte",
    "25 de las 41",
]


def normalizar(texto: str) -> str:
    texto = texto.replace("\u00a0", " ").replace("\u202f", " ")
    texto = texto.replace("\u2212", "-")  # signo menos tipográfico
    return texto


NUM = r"\d+(?:\.\d{3})*(?:,\d+)?"
PATRONES = {
    "decimal": re.compile(r"(?<![\d.,])[+\-]?\d+(?:\.\d{3})*,\d+(?![\d])"),
    "intervalo": re.compile(r"\[[+\-]?\d[^\[\]]*\]|\[t[+\-]\d[^\[\]\(\)]*[\)\]]"),
    "fraccion_de": re.compile(rf"(?<![\d.,]){NUM} de (?:las |los |sus |esas |estas )?{NUM}(?![\d])"),
    "fraccion_barra": re.compile(r"(?<![\d.,/\-])\d+/\d+(?![\d/])"),
    "porcentaje": re.compile(rf"(?<![\d.,]){NUM}(?:[–\-]{NUM})? ?%"),
    "p": re.compile(r"\bp(?: de)?(?: \(?Holm\)?)? ?(?:=|<)? ?\d+,\d+"),
    "miles": re.compile(r"(?<![\d.,])\d{1,3}(?:\.\d{3})+(?![\d,]|\.\d)"),
    "rango": re.compile(rf"(?<![\d.,])[+\-]?{NUM}[–]{NUM}(?![\d])"),
    "entero_con_unidad": re.compile(
        r"(?<![\d.,+\-–/])\d+(?: a \d+)? (?:s|ms|Hz|µV|mm|personas?|ventanas|particiones|hojas|"
        r"canales|componentes|grupos|pares|segmentos|filas|parámetros|réplicas|permutaciones|"
        r"etapas|referencias|muestras|sesiones|grabaciones|participantes|variables|columnas|"
        r"píxeles|minutos|divisiones|nombres|categorías|pruebas)\b"
    ),
}


def cifras(texto: str) -> Counter:
    c: Counter = Counter()
    for clase, patron in PATRONES.items():
        for m in patron.finditer(texto):
            c[(clase, re.sub(r"\s+", " ", m.group(0)).strip())] += 1
    return c


CITA = re.compile(
    r"[A-ZÁÉÍÓÚ][a-záéíóúñöô\-]+"
    r"(?:(?:, | y | )(?:[A-ZÁÉÍÓÚ][a-záéíóúñöô\-]+)| et al\.)*"
    r",? \(?(?:19|20)\d{2}(?:, (?:19|20)\d{2})?\)?"
)


def citas(texto: str) -> Counter:
    # solo el cuerpo: la lista de referencias se compara aparte, línea a línea
    return Counter(m.group(0).strip("()") for m in CITA.finditer(texto))


def notas(texto: str) -> list[str]:
    return [l.strip() for l in texto.splitlines() if l.strip().startswith("> Nota de trabajo (no va en la tesis):")]


def referencias(texto: str) -> list[str]:
    return [l.strip() for l in texto.splitlines() if l.startswith("- ") and "https://doi.org/" in l]


def tablas(texto: str) -> list[str]:
    problemas = []
    lineas = texto.splitlines()
    i = 0
    n_tablas = 0
    while i < len(lineas):
        if lineas[i].lstrip("> ").startswith("|"):
            j = i
            anchos = []
            while j < len(lineas) and lineas[j].lstrip("> ").startswith("|"):
                fila = lineas[j].lstrip("> ").strip()
                fila = re.sub(r"`[^`]*`", "x", fila)  # el código puede traer barras
                celdas = fila.strip("|").split("|")
                anchos.append((j + 1, len(celdas), fila.endswith("|")))
                j += 1
            n_tablas += 1
            base = anchos[0][1]
            for linea, ancho, cierra in anchos:
                if ancho != base or not cierra:
                    problemas.append(f"línea {linea}: {ancho} celdas (la cabecera tiene {base}) cierre={cierra}")
            if len(anchos) < 2 or not re.fullmatch(r"\|?[\s:\-|]+\|?", lineas[i + 1].lstrip("> ").strip()):
                problemas.append(f"línea {i + 1}: tabla sin fila separadora")
            i = j
        else:
            i += 1
    return [f"{n_tablas} tablas"] + problemas


ENCABEZADO = re.compile(r"^#{2,5} (?:Capítulo )?(\d+(?:\.\d+)*)\b", re.M)
REMISION = re.compile(
    r"\bsecci(?:ón|ones) (\d+(?:\.\d+)+(?:(?:, | y | a |, y )\d+(?:\.\d+)+)*)"
)


def encabezados(texto: str) -> set[str]:
    return set(ENCABEZADO.findall(texto))


def remisiones(texto: str) -> Counter:
    c: Counter = Counter()
    for m in REMISION.finditer(texto):
        for n in re.findall(r"\d+(?:\.\d+)+", m.group(1)):
            c[n] += 1
    return c


def main() -> int:
    fallos = 0
    antes = {k: normalizar((PREVIO / v).read_text(encoding="utf-8")) for k, v in ARCHIVOS.items()}
    ahora = {k: normalizar((ACTUAL / v).read_text(encoding="utf-8")) for k, v in ARCHIVOS.items()}
    enc_antes = set().union(*(encabezados(t) for t in antes.values()))
    enc_ahora = set().union(*(encabezados(t) for t in ahora.values()))

    print("== Encabezados numerados ==")
    print("  desaparecidos:", sorted(enc_antes - enc_ahora) or "ninguno")
    print("  nuevos:", sorted(enc_ahora - enc_antes) or "ninguno")
    for k in ARCHIVOS:
        tit_a = [l for l in antes[k].splitlines() if l.startswith("#")]
        tit_d = [l for l in ahora[k].splitlines() if l.startswith("#")]
        print(f"  {k}: títulos idénticos y en el mismo orden: {tit_a == tit_d}")
        if tit_a != tit_d:
            fallos += 1

    for k in ARCHIVOS:
        a, d = antes[k], ahora[k]
        print(f"\n================ {k} ================")
        ca, cd = cifras(a), cifras(d)
        faltan = sorted(x for x in ca if x not in cd)
        nuevas = sorted(x for x in cd if x not in ca)
        bajan = sorted((x, ca[x], cd[x]) for x in ca if x in cd and cd[x] < ca[x])
        suben = sorted((x, ca[x], cd[x]) for x in cd if x in ca and cd[x] > ca[x])
        print(f"a) cifras distintas: antes {len(ca)}, ahora {len(cd)}")
        print(f"   FALTANTES ({len(faltan)}):")
        for x in faltan:
            print(f"     {x[0]}: {x[1]!r} (antes {ca[x]} veces)")
        print(f"   NUEVAS ({len(nuevas)}):")
        for x in nuevas:
            print(f"     {x[0]}: {x[1]!r} (ahora {cd[x]} veces)")
        print(f"   bajan de frecuencia ({len(bajan)}):")
        for x, na, nd in bajan:
            print(f"     {x[0]}: {x[1]!r} {na} -> {nd}")
        print(f"   suben de frecuencia ({len(suben)}):")
        for x, na, nd in suben:
            print(f"     {x[0]}: {x[1]!r} {na} -> {nd}")

        cia, cid = citas(a), citas(d)
        print(f"b) citas distintas: antes {len(cia)}, ahora {len(cid)}")
        for x in sorted(cia):
            if cid[x] < cia[x]:
                print(f"     cita con menos apariciones: {x!r} {cia[x]} -> {cid[x]}")
        for x in sorted(cid):
            if x not in cia:
                print(f"     cita nueva: {x!r} ({cid[x]})")
        ra, rd = referencias(a), referencias(d)
        print(f"   lista de referencias: antes {len(ra)}, ahora {len(rd)}, idéntica: {ra == rd}")
        na_, nd_ = notas(a), notas(d)
        perdidas = [n for n in na_ if n not in nd_]
        agregadas = [n for n in nd_ if n not in na_]
        print(f"   notas de trabajo: antes {len(na_)}, ahora {len(nd_)}; perdidas o cambiadas {len(perdidas)}; nuevas {len(agregadas)}")
        for n in perdidas:
            print("     PERDIDA:", n[:160])
        for n in agregadas:
            print("     NUEVA:", n[:160])
        if perdidas:
            fallos += 1

        t = tablas(d)
        print(f"c) tablas: {t[0]}; problemas: {t[1:] or 'ninguno'}")
        if t[1:]:
            fallos += 1
        rema, remd = remisiones(a), remisiones(d)
        rotas_d = sorted(n for n in remd if n not in enc_ahora)
        rotas_a = sorted(n for n in rema if n not in enc_antes)
        print(f"   remisiones: antes {sum(rema.values())} ({len(rema)} destinos), ahora {sum(remd.values())} ({len(remd)} destinos)")
        print(f"   sin encabezado en los tres borradores: antes {rotas_a or 'ninguna'}; ahora {rotas_d or 'ninguna'}")
        if set(rotas_d) - set(rotas_a):
            fallos += 1
        print(f"   destinos que ya no se citan: {sorted(set(rema) - set(remd)) or 'ninguno'}; destinos nuevos: {sorted(set(remd) - set(rema)) or 'ninguno'}")

        print(f"d) palabras: antes {len(a.split())}, ahora {len(d.split())} ({len(d.split()) - len(a.split()):+d})")
        if k == "RD":
            for f in FRASES:
                print(f"   {f!r}: {a.count(f)} -> {d.count(f)}")
            for f in ("soporte del filtro", "soporte de la etiqueta", "soporte temporal", "soporte real", "soporte nominal"):
                print(f"     ({f!r}: {a.count(f)} -> {d.count(f)})")
            for sec in ("6.1", "6.2", "6.3", "7.8", "7.9", "8.2", "8.3", "8.4", "8.5", "8.8"):
                def tramo(t: str) -> int:
                    m = re.search(rf"^### {re.escape(sec)} .*?(?=^### |^## )", t, re.M | re.S)
                    return len(m.group(0).split()) if m else -1
                print(f"   palabras sección {sec}: {tramo(a)} -> {tramo(d)}")

    print("\nRESULTADO:", "con fallos estructurales" if fallos else "sin fallos estructurales (revisar faltantes y nuevas arriba)")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
