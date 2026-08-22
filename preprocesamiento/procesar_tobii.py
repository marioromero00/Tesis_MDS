#!/usr/bin/env python3
"""
Runner del preprocesamiento de GSR, pupilometría y eye tracking.

Uso:
    python procesar_tobii.py --tsv "datos/Toma_muestras_v2 Data export.tsv" \
                             --salida resultados/tobii

    # Si el TSV ya fue separado por participante:
    python procesar_tobii.py --parquets resultados/tobii/interim --salida resultados/tobii

Produce, por participante, una tabla de features en ventanas de 2 s con 50 %
de solapamiento, con el mismo paso que las épocas del EEG y anclada al reloj
absoluto UTC. La unión con la tabla del EEG se hace después, con los
manifiestos de sincronización: este módulo no la hace, porque la corrección de
deriva es una decisión aparte.

Columnas clave de la salida:
    participante, segmento_id, estimulo, tipo, idx_ventana,
    inicio, fin, inicio_s
"""
from __future__ import annotations

import argparse
import sys
import traceback
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

import columnas as cols_mod          # noqa: E402
import eye_tracking                  # noqa: E402
import gsr as gsr_mod                # noqa: E402
import pupila as pupila_mod          # noqa: E402
import tobii_io                      # noqa: E402
import ventanas as ventanas_mod      # noqa: E402

CLAVES = ["participante", "segmento_id", "estimulo", "tipo",
          "idx_ventana", "inicio", "fin", "inicio_s"]


def procesar_participante(parquet: Path, tipos: set[str] | None,
                          fs: float, contexto_s: float,
                          metodo_eda: str, verbose: bool = True) -> pd.DataFrame:
    """Procesa un participante y devuelve su tabla de features por ventana."""
    df, mapa, disponibles = tobii_io.cargar_participante(parquet)
    nombre = str(df[mapa["participante"]].iloc[0])
    if verbose:
        print(f"\n--- {nombre} ({len(df):,} filas) ---")
        print("  modalidades:", ", ".join(
            f"{k}={'sí' if v else 'NO'}" for k, v in disponibles.items()))

    segmentos = tobii_io.segmentos_de_estimulo(df, mapa)
    if tipos:
        segmentos = segmentos[segmentos["tipo"].isin(tipos)].reset_index(drop=True)
    if segmentos.empty:
        print(f"  sin segmentos de los tipos pedidos: se omite")
        return pd.DataFrame()

    v = ventanas_mod.grilla_por_segmento(segmentos)
    if v.empty:
        print("  ningún segmento alcanza los 2 s: se omite")
        return pd.DataFrame()
    if verbose:
        print(f"  {len(segmentos)} segmentos -> {len(v):,} ventanas de 2 s")

    grilla = tobii_io.grilla_uniforme(df, fs)
    partes = [v.reset_index(drop=True)]

    if disponibles["gsr"]:
        senal = gsr_mod.preparar(df, mapa, grilla, fs, metodo=metodo_eda)
        partes.append(gsr_mod.features(senal, v.reset_index(drop=True), fs, contexto_s))
    if disponibles["pupila"]:
        senal = pupila_mod.preparar(df, mapa, grilla)
        partes.append(pupila_mod.features(senal, v.reset_index(drop=True), fs))
    if disponibles["mirada"]:
        fij, sac = eye_tracking.extraer_eventos(df, mapa)
        if verbose:
            print(f"  {len(fij):,} fijaciones · {len(sac):,} sacadas")
        partes.append(eye_tracking.features(fij, sac, v.reset_index(drop=True)))

    tabla = pd.concat(partes, axis=1)
    tabla.insert(0, "participante", nombre)
    return tabla


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    fuente = p.add_mutually_exclusive_group(required=True)
    fuente.add_argument("--tsv", type=Path, help="Export unificado de Tobii Pro Lab")
    fuente.add_argument("--parquets", type=Path,
                        help="Carpeta con un Parquet por participante ya separado")
    p.add_argument("--salida", type=Path, required=True)
    p.add_argument("--tipos", default="exposicion_imagen",
                   help="Tipos de segmento a procesar, separados por coma. "
                        "'todos' para no filtrar. Por defecto solo la exposición "
                        "a imagen, que es la entrada de entrenamiento.")
    p.add_argument("--fs", type=float, default=tobii_io.FS_GRILLA)
    p.add_argument("--contexto-gsr", type=float, default=gsr_mod.CONTEXTO_S,
                   help="Ventana de contexto para las features de SCR, en segundos. "
                        "Se emite además de la ventana de 2 s: la decisión sobre "
                        "cuál usar sigue abierta.")
    p.add_argument("--metodo-eda", choices=["butter", "cvxeda"], default="butter")
    p.add_argument("--participante", action="append",
                   help="Procesar solo estos participantes. Repetible.")
    args = p.parse_args()

    args.salida.mkdir(parents=True, exist_ok=True)
    tipos = None if args.tipos.strip().lower() == "todos" else \
        {t.strip() for t in args.tipos.split(",") if t.strip()}

    if args.tsv:
        if not args.tsv.exists():
            print(f"No existe el TSV: {args.tsv}", file=sys.stderr)
            return 2
        interim = args.salida / "interim"
        print(f"Separando {args.tsv.name} por participante -> {interim}")
        parquets = tobii_io.separar_por_participante(args.tsv, interim)
    else:
        parquets = sorted(args.parquets.glob("*.parquet"))
    if not parquets:
        print("No se encontraron Parquet de participante.", file=sys.stderr)
        return 2

    if args.participante:
        pedidos = set(args.participante)
        parquets = [q for q in parquets if q.stem in pedidos]

    print(f"{len(parquets)} participantes por procesar.")
    tablas, fallidos = [], []
    for q in parquets:
        try:
            t = procesar_participante(q, tipos, args.fs, args.contexto_gsr,
                                      args.metodo_eda)
            if not t.empty:
                t.to_parquet(args.salida / f"{q.stem}_features.parquet", index=False)
                tablas.append(t)
        except Exception as e:                      # un participante malo no corta la corrida
            fallidos.append((q.stem, repr(e)))
            print(f"  ERROR en {q.stem}: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

    if not tablas:
        print("Ningún participante produjo features.", file=sys.stderr)
        return 1

    todo = pd.concat(tablas, ignore_index=True)
    destino = args.salida / "features_tobii.parquet"
    todo.to_parquet(destino, index=False)

    resumen = (todo.groupby("participante")
                   .agg(ventanas=("idx_ventana", "size"),
                        segmentos=("segmento_id", "nunique"))
                   .reset_index())
    for col, nombre in [("gsr_pct_valido", "gsr_pct_valido_medio"),
                        ("pup_pct_valido", "pup_pct_valido_medio")]:
        if col in todo.columns:
            resumen[nombre] = (todo.groupby("participante")[col]
                                   .mean().round(2).values)
    resumen.to_csv(args.salida / "resumen_tobii.csv", index=False)

    print(f"\n{'='*62}")
    print(f"Features: {destino}  ({todo.shape[0]:,} ventanas x {todo.shape[1]} columnas)")
    print(f"Resumen:  {args.salida / 'resumen_tobii.csv'}")
    print(resumen.to_string(index=False))
    if fallidos:
        print(f"\n{len(fallidos)} participantes con error:")
        for nombre, err in fallidos:
            print(f"  {nombre}: {err}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
