"""Ejecuta y audita BiLSTM, LSTM y TCN en ese orden; conserva progreso."""
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import subprocess
import sys
from temporales_core import ROOT,digest,write_json

OUT=ROOT/'resultados/grids_recurrentes_13-09-2026'
ORDER=['BiLSTM','LSTM','TCN']


def event(stage,**values):
    record=dict(utc=datetime.now(timezone.utc).isoformat(),stage=stage,**values)
    with (OUT/'orden_ejecucion.jsonl').open('a',encoding='utf-8') as f: f.write(json.dumps(record)+'\n')
    print(record,flush=True)


def run(script,family,resume=False):
    env=os.environ.copy(); env['MDS_GRID_FAMILY']=family
    args=[sys.executable,'-W','ignore::DeprecationWarning','-u',str(ROOT/'scripts'/script)]
    if resume: args.append('--resume')
    event('started',family=family,script=script,resume=resume)
    with (OUT/'logs'/f'{family}_{script}.log').open('a',encoding='utf-8') as log:
        p=subprocess.Popen(args,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        for line in p.stdout:
            log.write(line); log.flush(); print(f'[{family}] {line}',end='',flush=True)
        status=p.wait()
    event('finished',family=family,script=script,exit_code=status)
    if status: raise RuntimeError(f'{family} {script}: exit {status}; completed files preserved')


def main():
    OUT.mkdir(exist_ok=True); (OUT/'logs').mkdir(exist_ok=True)
    plan=OUT/'plan.json'
    sources=['ejecutar_grids_recurrentes.py','recurrentes_grid_core.py','entrenar_recurrentes_grid.py','auditar_recurrentes_grid.py']
    if plan.exists():
        frozen=json.loads(plan.read_text())
        assert frozen['order']==ORDER
        for n,h in frozen['sources'].items(): assert digest(ROOT/'scripts'/n)==h
    else:
        write_json(plan,dict(order=ORDER,created_utc=datetime.now(timezone.utc).isoformat(),
            sources={n:digest(ROOT/'scripts'/n) for n in sources},configs_per_family=32,
            primary='each family versus fixed references; no global post-hoc family winner',
            stages='training and audit complete before starting next family'))
    for family in ORDER:
        folder=OUT/family
        if (folder/'verificacion.json').exists():
            audit=json.loads((folder/'verificacion.json').read_text())
            assert audit['auditor_sha256']==digest(ROOT/'scripts/auditar_recurrentes_grid.py')
            protocol=json.loads((folder/'protocolo.json').read_text())
            for n,h in protocol['sources'].items(): assert digest(ROOT/'scripts'/n)==h
            event('already_audited',family=family)
            continue
        if not (folder/'completo.json').exists():
            run('entrenar_recurrentes_grid.py',family,resume=(folder/'protocolo.json').exists())
        run('auditar_recurrentes_grid.py',family)
    event('all_completed',order=ORDER)


if __name__=='__main__': main()
