"""Etiquetas GSR V2: componentes completos, soporte temporal y empates explícitos."""
from pathlib import Path
import json
import numpy as np,pandas as pd
from atencion_binaria import ROOT,digest,write
COLS=['gsr_tonic_mean_z','gsr_phasic_mean_z','gsr_scr_count','gsr_scr_mean_prominence_z']
KEYS=['participant','recording','segment_id','stimulus']
OUT=ROOT/'resultados/etiquetas_gsr_calidad_v2_01-11-2026'
TOL=1e-8

def rebuild(frame,coverage=.5):
 f=frame.copy().sort_values(KEYS+['window_start_utc']).reset_index(drop=True)
 assert not f.duplicated(KEYS+['window_start_utc']).any()
 finite=np.isfinite(f[COLS].to_numpy()).all(axis=1)
 covered=f.gsr_coverage.ge(coverage)&f.gsr_n.gt(0)&f.gsr_window_valid.eq(True)
 plausible=f.gsr_scr_count.ge(0)&f.gsr_scr_mean_prominence_z.ge(0)
 f['gsr_quality_valid']=covered&finite&plausible
 f['quality_reason']=np.select([~covered,~finite,~plausible],['cobertura_o_flag_invalido','componentes_ausentes','scr_invalido'],default='valida')
 z=pd.DataFrame(np.nan,index=f.index,columns=COLS);stats=[]
 for person,g in f.groupby('participant'):
  ix=g.index[g.gsr_quality_valid]
  for c in COLS:
   v=f.loc[ix,c].astype(float)
   if c in COLS[2:]:v=np.log1p(v)
   mean=v.mean();sd=v.std(ddof=0);active=len(v)>=2 and np.isfinite(sd) and sd>TOL
   if len(v):z.loc[ix,c]=(v-mean)/sd if active else 0.
   stats.append(dict(participant=person,component=c,n=len(v),mean=float(mean) if np.isfinite(mean) else None,sd=float(sd) if np.isfinite(sd) else None,variable=bool(active)))
 score=z.mean(axis=1,skipna=False)
 f['score2s_quality']=np.nan
 for person,ix in f.groupby('participant').groups.items():
  v=score.loc[ix];sd=v.std(ddof=0)
  if np.isfinite(sd) and sd>TOL:f.loc[ix,'score2s_quality']=(v-v.mean())/sd
 f['score6s_quality']=np.nan;f['history_valid_windows']=0
 for _,g in f.groupby(KEYS,sort=False):
  history=[];previous=None
  for i in g.index:
   ts=pd.Timestamp(f.loc[i,'window_start_utc']).timestamp()
   if previous is None or abs(ts-previous-1)>1e-4:history=[]
   previous=ts
   if not f.loc[i,'gsr_quality_valid'] or not np.isfinite(f.loc[i,'score2s_quality']):history=[];continue
   history=(history+[i])[-5:];f.loc[i,'history_valid_windows']=len(history)
   if len(history)==5:f.loc[i,'score6s_quality']=f.loc[history,'score2s_quality'].mean()
 f['activation_binary_v2']=pd.Series(pd.NA,index=f.index,dtype='Int64');f['label_reason']='historial_insuficiente'
 f.loc[~f.gsr_quality_valid,'label_reason']=f.loc[~f.gsr_quality_valid,'quality_reason']
 thresholds=[]
 for person,ix in f.groupby('participant').groups.items():
  valid=f.loc[ix,'score6s_quality'].dropna();sd=valid.std(ddof=0);median=valid.median()
  if len(valid)<2 or not np.isfinite(sd) or sd<=TOL:
   f.loc[valid.index,'label_reason']='score_sin_variacion';thresholds.append(dict(participant=person,n_score=len(valid),median=float(median) if np.isfinite(median) else None,labelable=False));continue
  score=(valid-valid.mean())/sd;f.loc[valid.index,'score6s_quality']=score;median=score.median();tie=(score-median).abs().le(TOL)
  eligible=score.index[~tie];f.loc[eligible,'activation_binary_v2']=(score.loc[eligible]>median).astype(int);f.loc[eligible,'label_reason']='etiquetada';f.loc[score.index[tie],'label_reason']='empate_mediana'
  thresholds.append(dict(participant=person,n_score=len(valid),median=float(median),labelable=True,ties=int(tie.sum())))
 return f,pd.DataFrame(stats),pd.DataFrame(thresholds)

def main():
 OUT.mkdir(exist_ok=False)
 source=ROOT/'resultados/preprocesamiento/caracteristicas_multimodales.csv';partition=ROOT/'resultados/modelado/particion_participantes.csv';old=ROOT/'resultados/comparacion_comun_binaria_30-10-2026/etiquetas_activacion.csv.gz'
 config=ROOT/'config/preprocesamiento_macos_v2.json';coverage=json.loads(config.read_text())['minimum_coverage']['gsr']
 plan=dict(version='gsr_quality_v2',created_utc=pd.Timestamp.now(tz='UTC').isoformat(),source_sha256=digest(source),partition_sha256=digest(partition),old_labels_sha256=digest(old),script_sha256=digest(Path(__file__)),coverage_threshold=coverage,coverage_origin=str(config),components=COLS,finite_components_required=4,context_windows=5,window_seconds=2,step_seconds=1,context_reset=KEYS+['invalid_window','gap_not_1s'],normalization='within participant offline, valid windows only; constant observed components zero; missing remain missing',ties='abs(score - median)<=1e-8 in standardized units excluded, not forced balanced',scope='label reconstruction on frozen train/validation/test; no model fitting or predictive evaluation',limitations='derived-feature QA; no new raw artifact detection or psychological validation; new task version')
 write(OUT/'protocolo.json',plan)
 raw=pd.read_csv(source);raw['source_row']=np.arange(len(raw));raw['split']=raw.participant.map(pd.read_csv(partition).set_index('participant').split);raw=raw[raw.split.isin(['train','validation','test'])]
 f,stats,thresholds=rebuild(raw,coverage);previous=pd.read_csv(old).rename(columns={'y':'activation_binary_old'})
 f=f.merge(previous[['source_row','activation_binary_old']],on='source_row',how='left',validate='one_to_one')
 output=f[['source_row']+KEYS+['window_start_utc','window_end_utc','split','gsr_quality_valid','quality_reason','history_valid_windows','score2s_quality','score6s_quality','activation_binary_v2','label_reason','activation_binary_old']]
 output.to_csv(OUT/'etiquetas.csv.gz',index=False);stats.to_csv(OUT/'normalizacion.csv',index=False);thresholds.to_csv(OUT/'umbrales.csv',index=False)
 rows=[]
 for (split,person),g in output.groupby(['split','participant']):
  both=g.activation_binary_v2.notna()&g.activation_binary_old.notna();valid=g.activation_binary_v2.dropna()
  rows.append(dict(split=split,participant=person,total=len(g),quality_valid=int(g.gsr_quality_valid.sum()),old_labelled=int(g.activation_binary_old.notna().sum()),new_labelled=len(valid),positive=int(valid.eq(1).sum()),negative=int(valid.eq(0).sum()),ties=int(g.label_reason.eq('empate_mediana').sum()),changed_on_common=int((g.loc[both,'activation_binary_v2']!=g.loc[both,'activation_binary_old']).sum()),common=int(both.sum())))
 summary=pd.DataFrame(rows);summary.to_csv(OUT/'resumen_personas.csv',index=False);output.groupby(['split','label_reason']).size().rename('windows').to_csv(OUT/'motivos.csv')
 labelled=output.activation_binary_v2.notna();assert output.loc[labelled,'gsr_quality_valid'].all() and output.loc[labelled,'history_valid_windows'].eq(5).all()
 assert len(output)==len(raw) and output.source_row.is_unique
 write(OUT/'auditoria.json',dict(passed=True,all_rows_preserved=True,all_labelled_windows_quality_valid=True,all_labelled_windows_five_valid_consecutive=True,original_source_unchanged=digest(source)==plan['source_sha256'],partition_unchanged=digest(partition)==plan['partition_sha256'],label_file_sha256=digest(OUT/'etiquetas.csv.gz'),predictive_metrics_evaluated=False))
 lines=['# Etiquetas GSR de activación V2','','Versión nueva basada en calidad del profesor. Conserva todas las filas y particiones originales; una fila descartada para aprendizaje conserva su motivo y etiqueta nueva ausente. No se entrenaron modelos.','',f'Cobertura mínima heredada: {coverage:.0%}. Se requieren cuatro componentes finitos y SCR no negativos. La normalización personal usa solo ventanas válidas. El score6s exige cinco ventanas consecutivas válidas del mismo estímulo/segmento/registro; se reinicia tras huecos. Componentes constantes observados aportan cero; ausencias no se rellenan con cero. Scores sin variación no generan etiquetas. Empates numéricos con la mediana (tolerancia1e-8) quedan sin etiqueta.', '', '## Retención por partición','','| Partición | Ventanas | GSR válido | Etiqueta anterior | Etiqueta V2 |','|---|---:|---:|---:|---:|']
 for split,g in summary.groupby('split'):lines.append(f'| {split} | {g.total.sum()} | {g.quality_valid.sum()} | {g.old_labelled.sum()} | {g.new_labelled.sum()} |')
 lines+=['','## Personas','','| Persona | Partición | Total | V2 | Positivos | Negativos | Cambios en filas comunes |','|---|---|---:|---:|---:|---:|---:|']
 for r in summary.itertuples():lines.append(f'| {r.participant} | {r.split} | {r.total} | {r.new_labelled} | {r.positive} | {r.negative} | {r.changed_on_common}/{r.common} |')
 lines+=['','Esta versión modifica score, soporte temporal y manejo de empates: las métricas de versiones anteriores no pueden atribuirse a estas etiquetas. Las comparaciones futuras deben usar exactamente las mismas filas V2 en todos los modelos y reconstruir los índices temporales sin cruzar los huecos. Ninguna persona se elimina por su AUC. Revisar personas con una sola clase o sin etiquetas y reportar sus denominadores.', '', 'Limitaciones: la cobertura mínima50% proviene del protocolo anterior y no equivale a una garantía fisiológica. Esta corrección usa características derivadas; no incorpora un detector nuevo de artefactos sobre señal cruda ni certifica sincronización externa. Normalización y mediana por sesión siguen siendo offline; no son etiquetas clínicas ni autorreportes.']
 (OUT/'INFORME.md').write_text('\n'.join(lines));print(summary.to_string(index=False));print('ETIQUETAS V2 COMPLETAS')
if __name__=='__main__':main()
