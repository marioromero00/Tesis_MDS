#!/usr/bin/env python3
"""EDA reproducible de EEG OpenBCI almacenado en un ZIP.

Solo usa la biblioteca estandar. Lee cada archivo por streaming y produce CSV,
JSON y SVG en eda_output/eeg sin extraer el ZIP.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import zipfile
from collections import defaultdict
from pathlib import Path

NCH = 16
RAIL = 187500.0


class Moments:
    def __init__(self):
        self.n = 0; self.mean = 0.0; self.m2 = 0.0; self.lo = math.inf; self.hi = -math.inf
    def add(self, x):
        self.n += 1
        d = x - self.mean; self.mean += d / self.n; self.m2 += d * (x - self.mean)
        self.lo = min(self.lo, x); self.hi = max(self.hi, x)
    def sd(self): return math.sqrt(self.m2 / (self.n - 1)) if self.n > 1 else 0.0


def manifest_rows(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def percentile(xs, p):
    if not xs: return None
    a = sorted(xs); k = (len(a)-1)*p; i = int(k); d = k-i
    return a[i]*(1-d) + a[min(i+1, len(a)-1)]*d


def analyze_member(zf, info, meta, stride):
    moms = [Moments() for _ in range(NCH)]
    sampled = rails = flat = bad = rows = 0
    first_t = last_t = prev_t = None
    positive_dt, gaps = [], 0
    prev = [None] * NCH
    is_txt = info.filename.lower().endswith(".txt")
    with zf.open(info) as raw:
        for bline in raw:
            if not bline.strip() or (is_txt and bline.startswith(b"%")): continue
            if is_txt and bline.startswith(b"Sample Index"): continue
            rows += 1
            if rows % stride != 1 % stride: continue
            try:
                parts = bline.decode("utf-8", "replace").strip().split("," if is_txt else "\t")
                vals = [float(parts[i]) for i in range(1, 17)]
                ts = float(parts[30 if is_txt else 29])
            except (ValueError, IndexError):
                bad += 1; continue
            sampled += 1
            if first_t is None: first_t = ts
            last_t = ts
            if prev_t is not None:
                dt = ts-prev_t
                if dt > 0: positive_dt.append(dt)
            prev_t = ts
            for i, x in enumerate(vals):
                moms[i].add(x)
                if abs(x) >= RAIL-1: rails += 1
                if prev[i] is not None and x == prev[i]: flat += 1
                prev[i] = x
    med_dt = statistics.median(positive_dt) if positive_dt else None
    if med_dt:
        gaps = sum(d > max(0.1, 5*med_dt) for d in positive_dt)
    duration = last_t-first_t if first_t is not None and last_t is not None else None
    effective = ((sampled-1)*stride/duration) if duration and sampled > 1 else None
    rail_pct = 100*rails/(sampled*NCH) if sampled else None
    flat_pct = 100*flat/(max(1, (sampled-1)*NCH)) if sampled else None
    ch = []
    for i, m in enumerate(moms):
        ch.append({"channel": i, "n_sampled": m.n, "mean_uv": m.mean if m.n else None,
                   "sd_uv": m.sd() if m.n else None, "min_uv": m.lo if m.n else None,
                   "max_uv": m.hi if m.n else None})
    # Criterio flexible acordado: excluir solo daño extremo (>30%).
    quality = "sin_datos" if not sampled else (
        "excluir" if rail_pct > 30 or flat_pct > 30 else "utilizable"
    )
    return ({"session": meta.get("session", info.filename.split('/')[0]),
             "participant": meta.get("participant", ""), "kind": meta.get("kind", ""),
             "source_file": info.filename, "format": "OpenBCI TXT" if is_txt else "BrainFlow CSV",
             "compressed_bytes": info.compress_size, "uncompressed_bytes": info.file_size,
             "rows": rows, "sampled_rows": sampled, "stride": stride,
             "duration_s": duration, "effective_hz": effective, "median_dt_s_sampled": med_dt,
             "timestamp_gaps_sampled": gaps, "parse_errors_sampled": bad,
             "rail_pct": rail_pct, "flat_repeat_pct": flat_pct, "quality": quality}, ch)


def svg_bar(path, title, labels, values, ylabel, color="#3568a8"):
    valid = [v for v in values if v is not None and math.isfinite(v)]
    vmax = max(valid, default=1); vmax = vmax if vmax > 0 else 1
    w = max(900, 80 + len(values)*12); h = 480; left=65; top=55; bottom=100; ph=h-top-bottom
    bars=[]
    for i,(lab,v) in enumerate(zip(labels,values)):
        x=left+i*12; bh=0 if v is None else ph*max(0,v)/vmax; y=top+ph-bh
        bars.append(f'<rect x="{x}" y="{y:.1f}" width="9" height="{bh:.1f}" fill="{color}"><title>{lab}: {v}</title></rect>')
    ticks=[]
    for j in range(6):
        y=top+ph-j*ph/5; val=j*vmax/5
        ticks.append(f'<line x1="{left}" y1="{y}" x2="{w-15}" y2="{y}" stroke="#ddd"/><text x="58" y="{y+4}" text-anchor="end" font-size="11">{val:.2g}</text>')
    rot=[]
    for i,lab in enumerate(labels):
        if i % max(1, len(labels)//30)==0: rot.append(f'<text transform="translate({left+i*12+7},{top+ph+8}) rotate(60)" font-size="9">{lab}</text>')
    body=''.join(ticks+bars+rot)
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" fill="white"/><text x="{w/2}" y="28" text-anchor="middle" font-family="sans-serif" font-size="18">{title}</text><text transform="translate(15,{h/2}) rotate(-90)" text-anchor="middle" font-family="sans-serif" font-size="12">{ylabel}</text><g font-family="sans-serif">{body}</g></svg>', encoding="utf-8")


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--zip", default="datos/eeg_recordings_exp_V2.zip")
    ap.add_argument("--manifest", default="resultados/sincronizacion/inventario_eeg.csv")
    ap.add_argument("--coordination", default="resultados/sincronizacion/coordinacion_sesiones.csv")
    ap.add_argument("--output", default="resultados/eda/eeg")
    ap.add_argument("--stride", type=int, default=10, help="Una de cada N filas para estadisticas (default 10)")
    ap.add_argument("--limit", type=int, default=0, help="Limitar sesiones (0=todas; util para prueba)")
    args=ap.parse_args(); out=Path(args.output); out.mkdir(parents=True, exist_ok=True)
    mani=manifest_rows(Path(args.manifest)); indexed={r["source_file"]:r for r in mani}
    coord={r.get("eeg_file",""):r for r in manifest_rows(Path(args.coordination))}
    summaries=[]; channel_rows=[]
    with zipfile.ZipFile(args.zip) as zf:
        infos={i.filename:i for i in zf.infolist()}
        selected=[r for r in mani if r.get("source_file") in infos]
        if args.limit: selected=selected[:args.limit]
        for n,r in enumerate(selected,1):
            s,ch=analyze_member(zf, infos[r["source_file"]], r, max(1,args.stride))
            c=coord.get(r["source_file"],{}); s["sync_status"]=c.get("match_status", "no_manifestado")
            s["sync_offset_s"]=c.get("offset_tobii_minus_eeg_s", "")
            summaries.append(s)
            for x in ch: channel_rows.append({"session":s["session"],"participant":s["participant"],**x})
            print(f"[{n}/{len(selected)}] {s['session']}: {s['quality']}", flush=True)
    def write_csv(name, rows):
        if not rows:return
        with (out/name).open("w",encoding="utf-8-sig",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    write_csv("eeg_resumen_sesiones.csv",summaries); write_csv("eeg_estadisticas_canales.csv",channel_rows)
    labels=[s["session"] for s in summaries]
    svg_bar(out/"eeg_frecuencia_efectiva.svg","Frecuencia efectiva por sesion",labels,[s["effective_hz"] for s in summaries],"Hz")
    svg_bar(out/"eeg_saturacion.svg","Muestras en rail por sesion",labels,[s["rail_pct"] for s in summaries],"% canal-muestras","#b64b45")
    svg_bar(out/"eeg_repeticion_plana.svg","Repeticiones exactas consecutivas",labels,[s["flat_repeat_pct"] for s in summaries],"%","#7a5aa6")
    counts=defaultdict(int)
    for s in summaries: counts[s["quality"]]+=1
    report={"parameters":{"zip":args.zip,"manifest":args.manifest,"coordination":args.coordination,"stride":max(1,args.stride),"rail_uv":RAIL,
                          "quality_rule":"utilizable si rail_pct <= 30 y flat_repeat_pct <= 30"},
            "sessions_analyzed":len(summaries),"quality_counts":dict(counts),
            "effective_hz":{"median":percentile([s["effective_hz"] for s in summaries if s["effective_hz"]],.5),"p05":percentile([s["effective_hz"] for s in summaries if s["effective_hz"]],.05),"p95":percentile([s["effective_hz"] for s in summaries if s["effective_hz"]],.95)},
            "rail_pct_median":percentile([s["rail_pct"] for s in summaries if s["rail_pct"] is not None],.5)}
    (out/"eeg_resumen.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False))

if __name__=="__main__": main()
