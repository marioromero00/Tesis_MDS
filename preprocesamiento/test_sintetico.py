#!/usr/bin/env python3
"""
Prueba de extremo a extremo con datos sintéticos.

Los datos reales del Tobii viven en Drive y no están en esta máquina, de modo
que el pipeline se verifica contra un export fabricado con propiedades
conocidas: número de picos SCR inyectados, número de parpadeos, número de
fijaciones y de sacadas. Si el pipeline los recupera, la mecánica está bien
aunque los datos reales todavía no se hayan tocado.

    python test_sintetico.py
"""
from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

import eye_tracking            # noqa: E402
import gsr as gsr_mod          # noqa: E402
import procesar_tobii          # noqa: E402
import pupila as pupila_mod    # noqa: E402
import tobii_io                # noqa: E402
import ventanas as ventanas_mod  # noqa: E402

FS = 60.0
DUR_ESTIMULO_S = 20.0
N_PICOS_SCR = 4
N_PARPADEOS = 5


def fabricar_participante(nombre: str, semilla: int) -> pd.DataFrame:
    """Un participante con dos estímulos numéricos y uno blur_ intercalado."""
    rng = np.random.default_rng(semilla)
    estimulos = [("7", DUR_ESTIMULO_S), ("blur_1", 3.0), ("14", DUR_ESTIMULO_S)]

    filas, t_us, idx_mov = [], 0, 0
    for estimulo, dur in estimulos:
        n = int(dur * FS)
        # Stream irregular: el Tobii no entrega muestras equiespaciadas.
        pasos = (1e6 / FS) * rng.uniform(0.92, 1.08, n)

        # --- GSR: ~8 Hz efectivos dentro del stream de 60 Hz ---------------
        base = 5.0 + 0.4 * np.sin(np.linspace(0, 2 * np.pi, n))
        fasico = np.zeros(n)
        if estimulo != "blur_1":
            for k in range(N_PICOS_SCR):
                c = int((k + 0.5) * n / N_PICOS_SCR)
                t = np.arange(n)
                fasico += 0.9 * np.exp(-((t - c) ** 2) / (2 * (FS * 0.7) ** 2))
        gsr_full = base + fasico + rng.normal(0, 0.004, n)
        valido_gsr = np.zeros(n, dtype=bool)
        valido_gsr[::max(int(FS / 8), 1)] = True

        # --- Pupila: parpadeos como caídas abruptas ------------------------
        pupil = 3.2 + 0.25 * np.sin(np.linspace(0, 4 * np.pi, n)) + rng.normal(0, 0.01, n)
        if estimulo != "blur_1":
            for k in range(N_PARPADEOS):
                c = int((k + 0.5) * n / N_PARPADEOS)
                pupil[c:c + 4] *= 0.4

        # --- Eye tracking: fijación de 300 ms, sacada de 40 ms, alternadas --
        tipo = np.empty(n, dtype=object)
        indice = np.zeros(n, dtype=int)
        duracion = np.zeros(n)
        i = 0
        while i < n:
            largo_fij = int(0.30 * FS)
            largo_sac = int(0.04 * FS)
            j = min(i + largo_fij, n)
            tipo[i:j], indice[i:j], duracion[i:j] = "Fixation", idx_mov, 300.0
            idx_mov += 1
            i = j
            j = min(i + largo_sac, n)
            if i < n:
                tipo[i:j], indice[i:j], duracion[i:j] = "Saccade", idx_mov, 40.0
                idx_mov += 1
                i = j

        gx = np.where(tipo == "Fixation", rng.normal(960, 60, n), rng.normal(960, 300, n))
        gy = np.where(tipo == "Fixation", rng.normal(540, 40, n), rng.normal(540, 200, n))

        for k in range(n):
            t_us += pasos[k]
            filas.append({
                "Participant name": nombre,
                "Recording date": "08/08/2025",
                "Recording start time": "12:21:50.131",
                "Recording timestamp": t_us,
                "Presented Stimulus name": estimulo,
                "Galvanic skin response (GSR)": gsr_full[k] if valido_gsr[k] else np.nan,
                "Pupil diameter filtered": pupil[k],
                "Eye movement type": tipo[k],
                "Eye movement type index": indice[k],
                "Gaze event duration": duracion[k],
                "Fixation point X": gx[k] if tipo[k] == "Fixation" else np.nan,
                "Fixation point Y": gy[k] if tipo[k] == "Fixation" else np.nan,
                "Gaze point X": gx[k],
                "Gaze point Y": gy[k],
                "Event": np.nan,
                "Event value": np.nan,
            })
    return pd.DataFrame(filas)


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="tobii_sintetico_"))
    fallos: list[str] = []
    try:
        tsv = tmp / "export_sintetico.tsv"
        pd.concat([fabricar_participante("P01", 1), fabricar_participante("P02", 2)],
                  ignore_index=True).to_csv(tsv, sep="\t", index=False)
        print(f"TSV sintético: {tsv}  ({tsv.stat().st_size/1e6:.1f} MB)")

        salida = tmp / "out"
        rc = procesar_tobii.main.__wrapped__ if hasattr(procesar_tobii.main, "__wrapped__") else None
        sys.argv = ["procesar_tobii.py", "--tsv", str(tsv), "--salida", str(salida)]
        rc = procesar_tobii.main()
        if rc != 0:
            fallos.append(f"el runner devolvió código {rc}")

        tabla = pd.read_parquet(salida / "features_tobii.parquet")
        print(f"\nTabla: {tabla.shape[0]} ventanas x {tabla.shape[1]} columnas")

        # --- Comprobaciones -------------------------------------------------
        # Dos estímulos útiles por participante, dos participantes.
        # No se fija el número de ventanas: el stream es irregular, de modo que
        # un estímulo de 20 s nominales dura ~19,98 s reales y la última ventana
        # no cabe. Lo que se verifica es el invariante de la grilla.
        n_segmentos = tabla.groupby(["participante", "segmento_id"]).ngroups
        if n_segmentos != 4:
            fallos.append(f"segmentos: esperaba 4, obtuve {n_segmentos}")

        for (part, seg), g in tabla.groupby(["participante", "segmento_id"]):
            g = g.sort_values("idx_ventana")
            if len(g) < 17:
                fallos.append(f"{part}/{seg}: solo {len(g)} ventanas para ~20 s")
            pasos = g["inicio"].diff().dropna().dt.total_seconds()
            if not pasos.empty and not np.allclose(pasos, 1.0):
                fallos.append(f"{part}/{seg}: el paso entre ventanas no es 1 s")

        if set(tabla["tipo"].unique()) != {"exposicion_imagen"}:
            fallos.append(f"el filtro de tipo dejó pasar {set(tabla['tipo'].unique())}")

        if not (tabla["fin"] - tabla["inicio"]).eq(pd.Timedelta(seconds=2)).all():
            fallos.append("hay ventanas que no duran 2 s")

        for prefijo, minimo in [("gsr_", 8), ("pup_", 8), ("et_", 12)]:
            n = sum(c.startswith(prefijo) for c in tabla.columns)
            if n < minimo:
                fallos.append(f"faltan features {prefijo}*: {n} < {minimo}")

        picos = tabla["gsr_scr_n_picos"].sum()
        if not picos > 0:
            fallos.append("no se detectó ningún pico SCR")
        if "gsr_scr_n_picos_ctx6s" not in tabla.columns:
            fallos.append("falta la variante de contexto de SCR")

        fij = tabla["et_n_fijaciones"].sum()
        if not fij > 0:
            fallos.append("no se contó ninguna fijación")
        dur = tabla["et_fij_dur_media"].dropna()
        if not dur.empty and not np.isclose(dur.mean(), 300.0, atol=1.0):
            fallos.append(f"duración media de fijación {dur.mean():.1f} ms, esperaba 300")

        if tabla["et_n_sacadas"].sum() <= 0:
            fallos.append("no se contó ninguna sacada")

        pct = tabla["pup_pct_valido"]
        if not (pct.between(0, 100).all()):
            fallos.append("pup_pct_valido fuera de [0,100]")
        if not (pct < 100).any():
            fallos.append("los parpadeos inyectados no bajaron pup_pct_valido")

        if tabla["gsr_scl_media"].isna().all():
            fallos.append("el componente tónico salió todo NaN")

        # La corrección por luminancia debe seguir explícitamente sin implementar.
        try:
            pupila_mod.corregir_luminancia(None, None)
            fallos.append("corregir_luminancia no debería estar implementada")
        except NotImplementedError:
            pass

        print("\n--- Muestra ---")
        muestra = ["participante", "estimulo", "inicio_s", "gsr_scr_n_picos",
                   "gsr_scr_n_picos_ctx6s", "gsr_scl_media", "pup_media",
                   "pup_pct_valido", "et_n_fijaciones", "et_fij_dur_media",
                   "et_n_sacadas", "et_disp_rms"]
        print(tabla[[c for c in muestra if c in tabla.columns]].head(6).to_string(index=False))
        print(f"\nPicos SCR totales: {picos:.0f} · fijaciones: {fij:.0f} · "
              f"sacadas: {tabla['et_n_sacadas'].sum():.0f}")

    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("\n" + "=" * 62)
    if fallos:
        print(f"FALLÓ — {len(fallos)} comprobaciones:")
        for f in fallos:
            print(f"  · {f}")
        return 1
    print("Todas las comprobaciones pasaron.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
