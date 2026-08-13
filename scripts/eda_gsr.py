#!/usr/bin/env python3
"""EDA reproducible y por streaming de la señal GSR exportada por Tobii.

No requiere dependencias externas. Genera CSV, JSON y gráficos SVG en
eda_output/gsr sin cargar el TSV completo en memoria.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class Acc:
    participant: str
    recording: str
    timeline: str = ""
    rows_total: int = 0
    rows_gsr_sensor: int = 0
    n: int = 0
    missing: int = 0
    invalid: int = 0
    mean: float = 0.0
    m2: float = 0.0
    min_value: float = math.inf
    max_value: float = -math.inf
    first_us: int | None = None
    last_us: int | None = None
    prev_us: int | None = None
    duplicate_timestamps: int = 0
    nonmonotonic_timestamps: int = 0
    dt_reservoir: list[float] = field(default_factory=list)
    value_reservoir: list[float] = field(default_factory=list)
    trace: list[tuple[int, float]] = field(default_factory=list)

    def add_reservoir(self, array, value, seen, cap, rng):
        if len(array) < cap:
            array.append(value)
        else:
            j = rng.randrange(seen)
            if j < cap:
                array[j] = value

    def add(self, ts: int, value: float, rng: random.Random, reservoir_n: int, trace_n: int):
        self.n += 1
        delta = value - self.mean
        self.mean += delta / self.n
        self.m2 += delta * (value - self.mean)
        self.min_value = min(self.min_value, value)
        self.max_value = max(self.max_value, value)
        self.first_us = ts if self.first_us is None else min(self.first_us, ts)
        self.last_us = ts if self.last_us is None else max(self.last_us, ts)
        if self.prev_us is not None:
            dt = (ts - self.prev_us) / 1_000_000.0
            if dt == 0:
                self.duplicate_timestamps += 1
            elif dt < 0:
                self.nonmonotonic_timestamps += 1
            else:
                self.add_reservoir(self.dt_reservoir, dt, self.n - 1, reservoir_n, rng)
        self.prev_us = ts
        self.add_reservoir(self.value_reservoir, value, self.n, reservoir_n, rng)
        self.add_reservoir(self.trace, (ts, value), self.n, trace_n, rng)


def q(values, p):
    if not values:
        return None
    x = sorted(values)
    pos = (len(x) - 1) * p
    lo, hi = math.floor(pos), math.ceil(pos)
    return x[lo] if lo == hi else x[lo] * (hi - pos) + x[hi] * (pos - lo)


def fmt(x):
    return "" if x is None or not math.isfinite(x) else f"{x:.9g}"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg_bar(path, rows, key, title, ylabel, width=1200, height=650):
    rows = [r for r in rows if isinstance(r.get(key), (int, float)) and math.isfinite(r[key])]
    margin = (85, 35, 70, 190); left, right, top, bottom = margin
    pw, ph = width-left-right, height-top-bottom
    vmax = max([r[key] for r in rows] + [1])
    bw = pw / max(len(rows), 1)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
           '<rect width="100%" height="100%" fill="white"/>', f'<text x="{width/2}" y="28" text-anchor="middle" font-family="sans-serif" font-size="20">{esc(title)}</text>',
           f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+ph}" stroke="#333"/><line x1="{left}" y1="{top+ph}" x2="{left+pw}" y2="{top+ph}" stroke="#333"/>']
    for i, r in enumerate(rows):
        h = ph*r[key]/vmax; x = left+i*bw+bw*.12; y=top+ph-h
        color = "#d95f02" if r.get("quality_status") == "review" else "#1b9e77"
        out.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{bw*.76:.2f}" height="{h:.2f}" fill="{color}"/>')
        out.append(f'<text x="{x+bw*.38:.2f}" y="{top+ph+15}" transform="rotate(60 {x+bw*.38:.2f},{top+ph+15})" font-family="sans-serif" font-size="10">{esc(r["participant"])}</text>')
    for j in range(6):
        v=vmax*j/5; y=top+ph-ph*j/5
        out.append(f'<text x="{left-8}" y="{y+4}" text-anchor="end" font-family="sans-serif" font-size="11">{v:.3g}</text><line x1="{left}" y1="{y}" x2="{left+pw}" y2="{y}" stroke="#ddd"/>')
    out.append(f'<text x="18" y="{top+ph/2}" transform="rotate(-90 18,{top+ph/2})" text-anchor="middle" font-family="sans-serif" font-size="13">{esc(ylabel)}</text></svg>')
    path.write_text("\n".join(out), encoding="utf-8")


def svg_traces(path, accs, width=1200, height=760):
    traces=[]
    for a in accs:
        if len(a.trace) < 2: continue
        pts=sorted(a.trace); t0=pts[0][0]; dur=max(pts[-1][0]-t0,1)
        med=q([v for _,v in pts],.5); lo=q([v for _,v in pts],.05); hi=q([v for _,v in pts],.95)
        scale=max((hi or 0)-(lo or 0),1e-12)
        traces.append((a.participant, [((t-t0)/dur, (v-med)/scale) for t,v in pts]))
    left,right,top,bottom=70,30,45,50; pw=width-left-right; ph=height-top-bottom
    colors=["#1b9e77","#d95f02","#7570b3","#e7298a","#66a61e","#e6ab02"]
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"><rect width="100%" height="100%" fill="white"/>',
         f'<text x="{width/2}" y="25" text-anchor="middle" font-family="sans-serif" font-size="19">Trazas GSR robustamente centradas (muestra de puntos)</text>']
    ymin,ymax=-2,2
    for j in range(5):
        y=top+ph*j/4; val=ymax-(ymax-ymin)*j/4
        out.append(f'<line x1="{left}" y1="{y}" x2="{left+pw}" y2="{y}" stroke="#ddd"/><text x="{left-7}" y="{y+4}" text-anchor="end" font-family="sans-serif" font-size="10">{val:g}</text>')
    for i,(name,pts) in enumerate(traces):
        coords=[]
        for x,y in pts:
            y=max(ymin,min(ymax,y)); coords.append(f'{left+x*pw:.1f},{top+(ymax-y)/(ymax-ymin)*ph:.1f}')
        out.append(f'<polyline points="{" ".join(coords)}" fill="none" stroke="{colors[i%len(colors)]}" opacity="0.28" stroke-width="0.8"><title>{esc(name)}</title></polyline>')
    out.append(f'<text x="{left+pw/2}" y="{height-12}" text-anchor="middle" font-family="sans-serif" font-size="12">Tiempo normalizado dentro de la grabación (0–1)</text></svg>')
    path.write_text("\n".join(out), encoding="utf-8")


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, default=Path("datos/Toma_muestras_v2 Data export.tsv"))
    ap.add_argument("--manifest", type=Path, default=Path("resultados/sincronizacion/inventario_tobii.csv"))
    ap.add_argument("--output", type=Path, default=Path("resultados/eda/gsr"))
    ap.add_argument("--reservoir", type=int, default=10000)
    ap.add_argument("--trace-points", type=int, default=1800)
    ap.add_argument("--seed", type=int, default=20260812)
    args=ap.parse_args(); args.output.mkdir(parents=True, exist_ok=True)
    rng=random.Random(args.seed); accs={}; total_rows=0
    with args.input.open("r",encoding="utf-8-sig",newline="",errors="replace") as f:
        header=f.readline().rstrip("\r\n").split("\t"); ix={name:i for i,name in enumerate(header)}
        required=["Recording timestamp","Sensor","Participant name","Recording name","Timeline name","Galvanic skin response (GSR)"]
        missing=[x for x in required if x not in ix]
        if missing: raise SystemExit("Faltan columnas: "+", ".join(missing))
        maxix=max(ix[x] for x in required)
        for line in f:
            total_rows+=1; parts=line.rstrip("\r\n").split("\t")
            if len(parts)<=maxix: continue
            participant=parts[ix["Participant name"]].strip() or "(sin participante)"
            recording=parts[ix["Recording name"]].strip() or "(sin grabación)"
            key=(participant,recording); a=accs.get(key)
            if a is None:
                a=accs[key]=Acc(participant,recording,parts[ix["Timeline name"]].strip())
            a.rows_total+=1
            sensor=parts[ix["Sensor"]].strip(); raw=parts[ix["Galvanic skin response (GSR)"]].strip()
            if sensor.casefold()=="gsr": a.rows_gsr_sensor+=1
            if not raw:
                if sensor.casefold()=="gsr": a.missing+=1
                continue
            try: value=float(raw); ts=int(float(parts[ix["Recording timestamp"]]))
            except (ValueError,OverflowError): a.invalid+=1; continue
            if not math.isfinite(value): a.invalid+=1; continue
            a.add(ts,value,rng,args.reservoir,args.trace_points)
    manifest={}
    if args.manifest.exists():
        with args.manifest.open(encoding="utf-8-sig",newline="") as f:
            for r in csv.DictReader(f): manifest[(r.get("participant",""),r.get("recording",""))]=r
    rows=[]
    for a in sorted(accs.values(),key=lambda z:(z.participant,z.recording)):
        if not (a.n or a.rows_gsr_sensor): continue
        med=q(a.value_reservoir,.5); q1=q(a.value_reservoir,.25); q3=q(a.value_reservoir,.75)
        dtmed=q(a.dt_reservoir,.5); duration=(a.last_us-a.first_us)/1e6 if a.first_us is not None and a.last_us is not None else None
        miss_rate=a.missing/max(a.rows_gsr_sensor,1); frequency=1/dtmed if dtmed and dtmed>0 else None
        reasons=[]
        if a.n<100: reasons.append("menos_de_100_muestras")
        if miss_rate>.05: reasons.append("faltantes_mayores_5pct")
        if a.nonmonotonic_timestamps: reasons.append("timestamps_no_monotonicos")
        if frequency is not None and not (.5<=frequency<=2000): reasons.append("frecuencia_atipica")
        rows.append({"participant":a.participant,"recording":a.recording,"timeline":a.timeline,
          "manifest_start_utc":manifest.get((a.participant,a.recording),{}).get("start_utc",""),
          "n_valid":a.n,"n_sensor_rows":a.rows_gsr_sensor,"n_missing":a.missing,"n_invalid":a.invalid,
          "missing_rate":miss_rate,"duration_s":duration,"sampling_hz_est":frequency,
          "mean":a.mean if a.n else None,"sd":math.sqrt(a.m2/(a.n-1)) if a.n>1 else None,
          "min":a.min_value if a.n else None,"q25_approx":q1,"median_approx":med,"q75_approx":q3,"max":a.max_value if a.n else None,
          "iqr_approx":q3-q1 if q1 is not None and q3 is not None else None,
          "duplicate_timestamps":a.duplicate_timestamps,"nonmonotonic_timestamps":a.nonmonotonic_timestamps,
          "quality_status":"review" if reasons else "ok","quality_reasons":";".join(reasons)})
    fields=list(rows[0]) if rows else []
    with (args.output/"gsr_por_grabacion.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for r in rows: w.writerow({k:fmt(v) if isinstance(v,float) else v for k,v in r.items()})
    with (args.output/"gsr_muestra_trazas.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f); w.writerow(["participant","recording","recording_timestamp_us","time_s","gsr"])
        for a in sorted(accs.values(),key=lambda z:z.participant):
            if a.first_us is None: continue
            for t,v in sorted(a.trace): w.writerow([a.participant,a.recording,t,fmt((t-a.first_us)/1e6),fmt(v)])
    valid=sum(r["n_valid"] for r in rows); review=sum(r["quality_status"]=="review" for r in rows)
    report={"generated_utc":datetime.now(timezone.utc).isoformat(),"input":str(args.input.resolve()),"input_bytes":args.input.stat().st_size,
      "rows_scanned":total_rows,"recordings_with_gsr":len(rows),"valid_gsr_samples":valid,"recordings_review":review,
      "method":{"streaming":True,"seed":args.seed,"reservoir_per_recording":args.reservoir,"quantiles":"aproximados por reservoir sampling determinista","units":"no confirmadas por metadatos"}}
    (args.output/"resumen_gsr.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    svg_bar(args.output/"01_muestras_validas.svg",rows,"n_valid","Muestras GSR válidas por participante","Número de muestras")
    svg_bar(args.output/"02_frecuencia_muestreo.svg",rows,"sampling_hz_est","Frecuencia de muestreo GSR estimada","Hz (1 / mediana Δt)")
    svg_bar(args.output/"03_mediana_gsr.svg",rows,"median_approx","Mediana aproximada de GSR","Valor GSR (unidad no confirmada)")
    svg_traces(args.output/"04_trazas_normalizadas.svg",list(accs.values()))
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=="__main__": main()
