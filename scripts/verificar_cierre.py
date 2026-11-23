"""Comprobación de reproducibilidad para el cierre de la experimentación (23-11-2026).

No entrena ni recalcula resultados. Para cada etapa registrada entre el 16 y el 23-11-2026 comprueba:
  1. que cada archivo con hash en el protocolo (entradas, crudos, tensores, variables) coincide hoy con ese hash;
     si no coincide, si coincidía en el commit en que se registró el protocolo (cambio posterior) o nunca;
  2. que el protocolo entró a Git antes que el informe de resultados de la misma carpeta;
  3. que la carpeta de resultados no tiene archivos sin versionar ni modificados.
Además: HEAD igual a origin/main y sin procesos de entrenamiento activos.
Salida: resultados/verificacion_cierre_23-11-2026/verificacion.json y resumen por pantalla.
"""
from __future__ import annotations
import hashlib, json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'resultados/verificacion_cierre_23-11-2026'
LOCAL = ROOT.parents[1] / 'datos/locales/v2_2025'
STAGES = ['cierre_v3_16-11-2026', 'cierre_final_41p_16-11-2026', 'cierre_robustez_41p_16-11-2026', 'ampliacion_41p_16-11-2026',
          'ampliacion_41p_16-11-2026/enmienda_e1_lag6', 'explicativo_posicion_41p_18-11-2026', 'reapertura_41p_22-11-2026',
          'reapertura_fase2_41p_22-11-2026', 'reapertura_fase3_41p_22-11-2026', 'enfoques_41p_22-11-2026',
          'limpieza_ocular_41p_23-11-2026', 'red_cruda_41p_23-11-2026']
# Dónde buscar los archivos que el protocolo nombra sin ruta (crudos en caché, tensores, variables recalculadas).
EXTRA = {'raw': LOCAL / 'cache_ocular', 'tensores.json': LOCAL / 'red_cruda_tensores', 'limpieza.json': LOCAL / 'limpieza_ocular_variables'}


def git(*a):
    return subprocess.run(['git', *a], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def is_hash(v):
    return isinstance(v, str) and len(v) == 64 and all(c in '0123456789abcdef' for c in v)


def hashes(obj, key=''):
    """Pares (grupo, nombre, hash) de todos los diccionarios nombre→sha256 del JSON."""
    out = []
    if isinstance(obj, dict):
        out += [(key, k, v) for k, v in obj.items() if is_hash(v)]
        for k, v in obj.items():
            out += hashes(v, k)
    return out


def locate(group, name, source):
    cands = [ROOT / name, ROOT / 'scripts' / name, ROOT.parents[1] / name]
    for k in (group, source):
        if k in EXTRA:
            cands += [EXTRA[k] / name, EXTRA[k] / (name + '.csv.gz'), EXTRA[k] / (name + '.csv'), EXTRA[k] / (name + '.pkl')]
    return next((c for c in cands if c.is_file()), None)


def at_commit(commit, path):
    r = subprocess.run(['git', 'show', f'{commit}:{path}'], cwd=ROOT, capture_output=True)
    return hashlib.sha256(r.stdout).hexdigest() if r.returncode == 0 else None


def first_commit(path):
    return git('log', '--diff-filter=A', '--format=%h %ct', '--', path).splitlines()[-1].split() if git('log', '--format=%h', '--', path) else None


def stage(name):
    d = ROOT / 'resultados' / name
    rel = f'resultados/{name}'
    reg = git('log', '-1', '--format=%h', '--', f'{rel}/protocolo.json')   # último commit que tocó el protocolo
    rows = []
    for source in ['protocolo.json', 'tensores.json', 'limpieza.json']:
        if not (d / source).is_file():
            continue
        for group, fname, h in hashes(json.loads((d / source).read_text())):
            p = locate(group, fname, source)
            if p is None:
                rows.append(dict(source=source, group=group, file=fname, status='no encontrado'))
                continue
            if sha(p) == h:
                status = 'coincide'
            else:
                try:
                    old = at_commit(reg, str(p.relative_to(ROOT)))
                except ValueError:
                    old = None
                status = 'cambió después del registro' if old == h else 'no coincide'
            rows.append(dict(source=source, group=group, file=fname, status=status))
    prot, inf = first_commit(f'{rel}/protocolo.json'), first_commit(f'{rel}/INFORME.md')
    dirty = git('status', '--porcelain', '--', rel).splitlines()
    return dict(stage=name, protocol_commit=prot[0] if prot else None, report_commit=inf[0] if inf else None,
                protocol_before_report=bool(prot and inf and int(prot[1]) < int(inf[1])) if inf else None,
                tracked_files=len(git('ls-files', '--', rel).splitlines()), dirty=dirty,
                counts={s: sum(r['status'] == s for r in rows) for s in sorted({r['status'] for r in rows})},
                problems=[r for r in rows if r['status'] != 'coincide'])


def main():
    OUT.mkdir(exist_ok=True)
    git('fetch', '-q', 'origin')
    res = dict(head=git('rev-parse', 'HEAD'), origin_main=git('rev-parse', 'origin/main'),
               training_processes=[l for l in subprocess.run(['ps', '-axo', 'command'], capture_output=True, text=True).stdout.splitlines()
                                   if '_41p.py' in l or 'cierre_experimental' in l],
               stages=[stage(s) for s in STAGES])
    (OUT / 'verificacion.json').write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print('HEAD == origin/main:', res['head'] == res['origin_main'], '| procesos de entrenamiento:', len(res['training_processes']))
    for s in res['stages']:
        print(f"{s['stage']:48s} prot {s['protocol_commit']} inf {s['report_commit']} antes={s['protocol_before_report']} "
              f"archivos={s['tracked_files']} sucio={len(s['dirty'])} {s['counts']}")
        for p in s['problems']:
            print('     ', p)


if __name__ == '__main__':
    main()
