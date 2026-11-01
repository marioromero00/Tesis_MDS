"""Espera descargas reanudables, valida crudos V2 y ejecuta experimento EEG nuevo."""
from __future__ import annotations
import argparse,json,os,signal,subprocess,sys,time,hashlib,zipfile,importlib.metadata
from datetime import datetime,timezone
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
BASE=(ROOT/'../../datos/locales/v2_2025').resolve()
PYTHON=ROOT/'.venv/bin/python'
INPUTS={'eeg_zip':{'name':'eeg_recordings_exp_V2.zip','id':'1SOui6TmWXjhdHbZbzJg3K26GJhiP341z','initial_pid':6030},'tobii_tsv':{'name':'Toma_muestras_v2 Data export.tsv','id':'1yQnHiCpa25Wo7F94Z9X0Vew_c5EqBv4t','initial_pid':6029}}
SOURCES=['pipeline_crudos_v2.py','eeg_por_canal_v2.py','modelar_eeg_por_canal_v2.py','auditar_modelos_eeg_por_canal_v2.py','preprocesamiento_secuencial.py','temporales_core.py','atencion_binaria.py','reconstruir_profesor_atencion_binaria.py','nuevos_modelos_atencion_binaria.py']

def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()

def write(path,value):
 temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(json.dumps(value,indent=2,ensure_ascii=False));temp.replace(path)

def process_matches(pid,ident):
 try:
  command=subprocess.check_output(['/bin/ps','-p',str(pid),'-o','command='],text=True,stderr=subprocess.DEVNULL)
  return 'gdown' in command and ident in command
 except (subprocess.CalledProcessError,ProcessLookupError):return False

def status(state):
 state['updated_utc']=datetime.now(timezone.utc).isoformat();write(BASE/'estado_pipeline.json',state)
 lines=['# Estado de crudos y experimento V2','',f"Fase: **{state['phase']}**",'',f"Actualización UTC: {state['updated_utc']}",'']
 for key,d in state.get('downloads',{}).items():
  pct=100*d['bytes_observed']/d['expected_bytes'];lines.append(f"- {INPUTS[key]['name']}: {pct:.2f} % ({d['bytes_observed']:,}/{d['expected_bytes']:,} bytes); SHA-256 verificado: {d.get('verified',False)}.")
 lines+=['','Flujo: descarga → hashes/tamaños → integridad de ZIP y columnas Tobii → EEG por canal en train → grid agrupado → auditoría de predicciones.','',
  'Los archivos parciales no se consideran listos. Etiquetas y folds se conservan; validation/test no se evalúan. La meta AUC > 0,70 permanece pendiente hasta tener métricas completas y auditadas.']
 if state.get('error'):lines+=['',f"Error: {state['error']}"]
 if state.get('model_metrics'):lines+=['','Métricas finales:',json.dumps(state['model_metrics'],ensure_ascii=False)]
 (BASE/'ESTADO.md').write_text('\n'.join(lines))

def run_stage(state,name,args,log):
 state['phase']=name;status(state)
 with log.open('a') as f:
  result=subprocess.run([str(PYTHON),*args],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT)
 if result.returncode:raise RuntimeError(f'{name} terminó con código {result.returncode}; revisar {log}')

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--interval',type=int,default=30);args=parser.parse_args();BASE.mkdir(parents=True,exist_ok=True)
 expected=json.loads((ROOT/'resultados/preprocesamiento/manifiesto_ejecucion.json').read_text())['inputs']
 fingerprints={name:sha(ROOT/'scripts'/name) for name in SOURCES};packages={p:importlib.metadata.version(p) for p in ['numpy','pandas','scipy','scikit-learn','catboost','gdown']}
 launch={'created_utc':datetime.now(timezone.utc).isoformat(),'pid':os.getpid(),'sources_sha256':fingerprints,'packages':packages,'folder_url':'https://drive.google.com/drive/folders/1REsfSQWiiPp7BKubdHa2A7VNeBjlELAD','automatic_next_steps':['eeg_por_canal_v2.py','modelar_eeg_por_canal_v2.py --round 1','auditar_modelos_eeg_por_canal_v2.py --round 1']}
 write(BASE/'ejecucion_pipeline.json',launch);(BASE/'pipeline.pid').write_text(str(os.getpid()))
 state={'phase':'descargando','downloads':{},'model_metrics':None};verified={};pids={k:v['initial_pid'] for k,v in INPUTS.items()};restarts={k:0 for k in INPUTS};children=[]
 caffeine=subprocess.Popen(['/usr/bin/caffeinate','-i','-w',str(os.getpid())],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 try:
  while len(verified)<len(INPUTS):
   for key,info in INPUTS.items():
    path=BASE/info['name'];parts=list(BASE.glob(info['name']+'*.part'))
    observed=path.stat().st_size if path.exists() else max([p.stat().st_size for p in parts] or [0])
    state['downloads'][key]={'bytes_observed':observed,'expected_bytes':expected[key]['bytes'],'verified':key in verified,'pid':pids[key]}
    if key in verified:continue
    if path.exists() and path.stat().st_size==expected[key]['bytes']:
     before=path.stat();actual=sha(path);after=path.stat()
     if before.st_mtime_ns!=after.st_mtime_ns:continue
     if actual!=expected[key]['sha256']:raise RuntimeError(f'SHA-256 distinto para {info["name"]}; no se procesará')
     verified[key]={'path':str(path),'bytes':after.st_size,'sha256':actual};state['downloads'][key]['verified']=True
     if process_matches(pids[key],info['id']):os.kill(pids[key],signal.SIGTERM)
    elif not process_matches(pids[key],info['id']):
     if restarts[key]>=3:raise RuntimeError(f'Descarga incompleta tras reintentos: {info["name"]}')
     log=(BASE/f'descarga_{key}_reintentos.log').open('a')
     child=subprocess.Popen([str(PYTHON),'-m','gdown',info['id'],'-O',str(path),'--continue','--retries','3','--timeout','60'],cwd=ROOT,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True);log.close();children.append(child);pids[key]=child.pid;restarts[key]+=1
   status(state)
   if len(verified)<len(INPUTS):time.sleep(args.interval)
  state['phase']='validando_integridad';status(state)
  with zipfile.ZipFile(BASE/INPUTS['eeg_zip']['name']) as z:
   missing=[p for p in pd.read_csv(ROOT/'resultados/sincronizacion/coordinacion_sesiones.csv').eeg_file.dropna().unique() if p not in z.namelist()]
   if missing:raise RuntimeError('Archivos del manifiesto ausentes del ZIP')
   bad=z.testzip()
   if bad:raise RuntimeError('CRC inválido en ZIP: '+bad)
  header=pd.read_csv(BASE/INPUTS['tobii_tsv']['name'],sep='\t',nrows=3)
  from preprocesamiento_secuencial import TOBII_COLUMNS
  if not set(TOBII_COLUMNS).issubset(header.columns):raise RuntimeError('Faltan columnas Tobii requeridas')
  write(BASE/'verificacion_crudos_completa.json',{'passed':True,'inputs':verified,'zip_crc_passed':True,'all_manifest_members_present':True,'tobii_columns_valid':True})
  for name,expected_sha in fingerprints.items():
   if sha(ROOT/'scripts'/name)!=expected_sha:raise RuntimeError('Código cambió durante la espera: '+name)
  for p,v in packages.items():
   if importlib.metadata.version(p)!=v:raise RuntimeError('El entorno cambió durante la espera: '+p)
  run_stage(state,'extrayendo_eeg_por_canal',['scripts/eeg_por_canal_v2.py'],BASE/'extraccion_eeg_por_canal.log')
  run_stage(state,'entrenando_grid_eeg_por_canal',['scripts/modelar_eeg_por_canal_v2.py','--round','1'],BASE/'modelos_eeg_por_canal.log')
  run_stage(state,'auditando_predicciones',['scripts/auditar_modelos_eeg_por_canal_v2.py','--round','1'],BASE/'auditoria_modelos.log')
  out=ROOT/'resultados/eeg_por_canal_v2_29-10-2026/modelos_grid/ronda1';audit=json.loads((out/'auditoria_independiente.json').read_text());assert audit['passed']
  metrics=pd.read_csv(out/'metricas.csv');state['model_metrics']=metrics.to_dict('records');state['phase']='completo_meta_superada' if metrics.auc_macro.gt(.7).any() else 'completo_meta_pendiente';state['results']=str(out);status(state)
 except Exception as e:
  state['phase']='requiere_revision';state['error']=str(e);status(state);raise
 finally:
  caffeine.terminate()
if __name__=='__main__':main()
