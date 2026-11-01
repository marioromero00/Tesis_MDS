"""Repetición completa preservando el experimento original y comparando salidas."""
import json,sys,shutil,subprocess,os
from pathlib import Path
import numpy as np,pandas as pd
from threadpoolctl import threadpool_limits
import diagnostico_busqueda_activacion as experiment
old=experiment.OUT
experiment.OUT=experiment.ROOT/'resultados/activacion_diagnostico_nested_reintento_01-11-2026'
keepawake=subprocess.Popen(['/usr/bin/caffeinate','-i','-w',str(os.getpid())])
try:
 with threadpool_limits(limits=2):experiment.main()
 for name in ['DIAGNOSTICO.md']:shutil.copy2(old/name,experiment.OUT/name)
 oldplan=json.loads((old/'protocolo.json').read_text());newplan=json.loads((experiment.OUT/'protocolo.json').read_text())
 for key in oldplan:
  if key!='created_utc':assert oldplan[key]==newplan[key],key
 results={}
 for name in ['predicciones_oof.csv.gz','metricas.csv','contrastes.csv','selecciones.csv','diagnostico_personas.csv']:
  a=pd.read_csv(old/name);b=pd.read_csv(experiment.OUT/name);pd.testing.assert_frame_equal(a,b,check_exact=False,atol=1e-10,rtol=1e-10)
  results[name]=True
 (experiment.OUT/'reproduccion.json').write_text(json.dumps(dict(passed=True,rerun_from_scratch=True,outputs_match=results,tolerance=1e-10),indent=2))
 with (experiment.OUT/'INFORME.md').open('a') as f:f.write('\n\nRepetición completa del 01-11-2026: predicciones, métricas, contrastes, selecciones y diagnóstico coinciden con la ejecución original, tolerancia 1e-10. Se entrenaron nuevamente los 60 ajustes internos y 15 modelos externos. [Diagnóstico](DIAGNOSTICO.md).\n')
 print('REPRODUCCIÓN COMPLETA VERIFICADA',flush=True)
finally:keepawake.terminate()
