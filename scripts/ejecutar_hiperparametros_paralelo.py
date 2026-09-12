"""Misma grilla, cuatro procesos; comparte ajustes identicos entre reglas externas."""
import argparse
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime,timezone
from pathlib import Path
from threadpoolctl import threadpool_limits
import entrenar_hiperparametros as training
from hiperparametros_core import fit_bundle,grid
from temporales_core import ROOT,digest,write_json

_worker_cache=None


def initialize(cache):
    global _worker_cache
    _worker_cache=cache


def worker(indices,frame,definition,seed):
    start=datetime.now(timezone.utc).isoformat()
    with threadpool_limits(limits=1): bundle=fit_bundle(_worker_cache,indices,frame,definition,seed)
    bundle['_execution']=dict(started_utc=start,completed_utc=datetime.now(timezone.utc).isoformat(),
        base_id=definition['base_id'],seed=seed,participants=sorted(frame.participant.unique()),
        components=len(bundle['components']))
    return bundle


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',default='resultados/hiperparametros_11-09-2026_paralelo')
    output=parser.parse_args().output; out=ROOT/output
    if out.exists(): raise FileExistsError(out)
    executor=None; futures={}; active_group=None; executed=[]; seen=set()
    original_write=training.write_json
    def write(path,value):
        if path.name=='protocolo.json':
            value['runtime']=dict(runner=Path(__file__).name,sha256=digest(__file__),workers=4,threads_per_worker=1,
                identical_outer_fits_reused=True,serial_partial='resultados/hiperparametros_11-09-2026',
                serial_interruption_sha256=digest(ROOT/'resultados/hiperparametros_11-09-2026/interrupcion.json'))
        original_write(path,value)
    def fit(cache,indices,frame,definition,seed):
        nonlocal executor,futures,active_group
        if executor is None: executor=ProcessPoolExecutor(max_workers=4,initializer=initialize,initargs=(cache,))
        group=tuple(sorted(frame.participant.unique()))
        if group!=active_group: futures={}; active_group=group
        if seed not in futures:
            candidates=grid()
            if len(group)==20:
                protocol=json.loads((out/'protocolo.json').read_text())
                fold=next(f['fold'] for f in protocol['folds'] if tuple(f['fit'])==group)
                selected=json.loads((out/'selecciones.json').read_text())
                candidates=list({s['definition']['base_id']:s['definition'] for s in selected if s['fold']==fold}.values())
            futures[seed]={d['base_id']:executor.submit(worker,indices,frame,d,seed) for d in candidates}
        bundle=futures[seed][definition['base_id']].result()
        key=(group,seed,definition['base_id'])
        if key not in seen:
            seen.add(key); executed.append(bundle['_execution'])
            write_json(out/'ejecucion_paralela.json',dict(unique_bundles_fitted=len(executed),fits=executed))
        return bundle
    training.fit_bundle=fit; training.write_json=write
    sys.argv=[sys.argv[0],'--output',output]
    try:
        with threadpool_limits(limits=4): training.main()
    finally:
        if executor is not None: executor.shutdown(wait=True,cancel_futures=True)


if __name__=='__main__': main()
