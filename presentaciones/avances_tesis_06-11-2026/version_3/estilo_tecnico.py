from pathlib import Path
import base64,json,hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve,roc_auc_score
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
ASSETS=HERE/'graficos';ASSETS.mkdir(exist_ok=True)
BLUE='#1559a6';LIGHT='#80aeda';DARK='#163550';GRAY='#65758a'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.labelcolor':DARK,'text.color':DARK,'xtick.color':GRAY,'ytick.color':GRAY,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#cbd5e1','grid.color':'#e5ebf2','axes.titlesize':14,'figure.facecolor':'white','axes.facecolor':'white','savefig.facecolor':'white'})
inputs={};metrics_checks=[]
def read(path):
 p=ROOT/path;inputs[path]=hashlib.sha256(p.read_bytes()).hexdigest();return pd.read_csv(p)
def fig(width=11,height=4):return plt.subplots(figsize=(width,height),layout='constrained')
def save(f,name):
 f.savefig(ASSETS/(name+'.png'),dpi=180);f.savefig(ASSETS/(name+'.svg'));plt.close(f)
 return name

def img(name,caption):
 b=base64.b64encode((ASSETS/(name+'.png')).read_bytes()).decode()
 return f'<figure class="data-figure"><img src="data:image/png;base64,{b}" alt="{caption}"><figcaption>{caption}</figcaption></figure>'
def table(headers,rows):
 return '<table><thead><tr>'+''.join('<th>'+x+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+x+'</td>' for x in r)+'</tr>' for r in rows)+'</tbody></table>'
def fmt(x):return f'{x:.4f}'.replace('.',',')
def roc(pred,key,models,name,expected):
 f,ax=fig(10.5,4.05);grid=np.linspace(0,1,501)
 for (value,label,color),exp in zip(models,expected):
  part=pred[pred[key].eq(value)];curves=[];scores=[]
  for _,g in part.groupby('participant'):
   assert g.y.nunique()==2
   x,y,_=roc_curve(g.y,g.prob);curves.append(np.interp(grid,x,y));scores.append(roc_auc_score(g.y,g.prob))
  mean=np.mean(scores);assert abs(mean-exp)<1e-10
  metrics_checks.append(dict(chart=name,model=str(value),auc=float(mean),participants=len(scores)))
  ax.plot(grid,np.mean(curves,axis=0),color=color,lw=2.4,label=f'{label}  ·  AUC {fmt(mean)}')
 ax.plot([0,1],[0,1],'--',color='#9ca9b7',lw=1,label='Referencia aleatoria')
 ax.set(xlim=(0,1),ylim=(0,1),xlabel='Tasa de falsos positivos (1 − especificidad)',ylabel='Sensibilidad')
 ax.grid(alpha=.6);ax.legend(loc='lower right',frameon=False,fontsize=11);save(f,name)

def apply(slides):
 a=read('resultados/temporalidad_eeg_v2_test_29-10-2026/metricas.csv').set_index('strategy')
 p=read('resultados/temporalidad_eeg_v2_test_29-10-2026/predicciones_test.csv.gz')
 roc(p,'strategy',[('inductivo_ctx1','CatBoost estático',GRAY),('inductivo_estatico_pareado','HistBoost estático',LIGHT),('inductivo_ctx32','HistBoost temporal',BLUE)],'roc_atencion',[a.loc[k,'auc_macro'] for k in ['inductivo_ctx1','inductivo_estatico_pareado','inductivo_ctx32']])
 act=read('resultados/activacion_gsr_v2_recalculo_02-11-2026/metricas.csv')
 pred=read('resultados/activacion_gsr_v2_recalculo_02-11-2026/predicciones_externas.csv.gz')
 roc(pred[pred.split.eq('test')],'context',[(1,'Actual',GRAY),(8,'Hasta 8 ventanas',BLUE),(32,'Hasta 32 ventanas',LIGHT)],'roc_activacion',[act[act.split.eq('test')&act.context.eq(c)].auc.item() for c in [1,8,32]])
 # AUC bars use zero baseline and fixed range 0..1; CIs are participant bootstrap intervals.
 f,axes=plt.subplots(1,2,figsize=(11,4),sharey=True,layout='constrained')
 for ax,split,title in zip(axes,['validation','test'],['Validación · 8 personas','Test · 8 personas']):
  g=act[act.split.eq(split)].sort_values('context');y=g.auc.to_numpy()
  ax.bar(range(3),y,color=[GRAY,BLUE,LIGHT],width=.55,zorder=2)
  ax.errorbar(range(3),y,yerr=np.vstack([y-g.low,g.high-y]),fmt='none',ecolor=DARK,capsize=5,lw=1.4,zorder=3)
  for i,v in enumerate(y):ax.text(i,.04,fmt(v),ha='center',color='white',weight='bold',fontsize=13)
  ax.axhline(.5,color=GRAY,ls='--',lw=1);ax.set(ylim=(0,1),xticks=range(3),xticklabels=['Actual','Hasta 8','Hasta 32'],title=title);ax.grid(axis='y',zorder=0)
 axes[0].set_ylabel('ROC-AUC macro por participante');save(f,'auc_activacion')
 # Paired contrasts; no inference from overlap of individual AUC CIs.
 con=read('resultados/activacion_gsr_v2_recalculo_02-11-2026/contrastes.csv')
 f,ax=fig(11,4);labels=[]
 for j,(split,c) in enumerate([(s,c) for s in ['oof_train','validation','test'] for c in [8,32]]):
  r=con[con.split.eq(split)&con.context.eq(c)].iloc[0];color=BLUE if c==32 else LIGHT
  ax.errorbar(r.delta,j,xerr=[[r.delta-r.low],[r.high-r.delta]],fmt='o',color=color,capsize=5,ms=6,lw=2)
  labels.append({'oof_train':'OOF train','validation':'Validación','test':'Test'}[split]+f' · {c} − actual')
  ax.text(.105,j,f'{r.delta:+.4f}  [{r.low:+.4f}; {r.high:+.4f}]',va='center',fontsize=10)
 ax.axvline(0,color=GRAY,ls='--',lw=1);ax.set(yticks=range(6),yticklabels=labels,xlim=(-.075,.245),xlabel='Diferencia pareada de AUC (temporal − estático)');ax.set_xticks([-.05,0,.05,.1]);ax.invert_yaxis();ax.grid(axis='x');save(f,'contrastes_activacion')
 f,ax=fig(11,4)
 ac=read('resultados/temporalidad_eeg_v2_test_29-10-2026/contrastes.csv')
 r1=ac[ac.temporal.eq('inductivo_ctx32')&ac.baseline.eq('inductivo_estatico_pareado')].iloc[0]
 cc=read('resultados/comparacion_comun_binaria_30-10-2026/contrastes.csv')
 r2=cc[cc.task.eq('atencion')&cc.split.eq('test')&cc.contrast.eq('temporal_full')].iloc[0]
 values=[(r1.delta_auc,r1.ci_low,r1.ci_high),(r2.delta,r2.low,r2.high)]
 for i,(v,lo,hi) in enumerate(values):
  ax.errorbar(v,i,xerr=[[v-lo],[hi-v]],fmt='o',color=BLUE,capsize=6,lw=2,ms=8)
  ax.text(.067,i,f'{v:+.4f}\n[{lo:+.4f}; {hi:+.4f}]',va='center',fontsize=12)
 ax.axvline(0,ls='--',color=GRAY);ax.set(yticks=[0,1],yticklabels=['29 oct · representación original','30 oct · historial de todas las variables'],xlim=(-.02,.115),ylim=(1.7,-.7),xlabel='ΔAUC test · HistBoost temporal − HistBoost estático');ax.set_xticks([-.02,0,.02,.04,.06]);ax.grid(axis='x');save(f,'contrastes_atencion')
 # Label retention with absolute counts.
 q=read('resultados/etiquetas_gsr_calidad_v2_01-11-2026/resumen_personas.csv').groupby('split')[['total','new_labelled']].sum().loc[['train','validation','test']]
 f,ax=fig(11,3.8);ys=np.arange(3)
 ax.barh(ys,q.new_labelled,color=BLUE,label='Con etiqueta V2',height=.5)
 ax.barh(ys,q.total-q.new_labelled,left=q.new_labelled,color='#dce7f3',label='Sin etiqueta V2',height=.5)
 for i,r in enumerate(q.itertuples()):
  ax.text(r.new_labelled/2,i,f'{r.new_labelled:,}'.replace(',','.'),ha='center',va='center',color='white',weight='bold')
  ax.text(r.total+200,i,f'{r.new_labelled/r.total:.1%}',va='center',fontsize=12)
 ax.set(yticks=ys,yticklabels=['Entrenamiento','Validación','Test'],xlabel='Número de ventanas',xlim=(0,15400));ax.invert_yaxis();ax.legend(frameon=False,loc='lower right');ax.grid(axis='x',zorder=0);ax.set_axisbelow(True);save(f,'retencion')
 ab=read('resultados/ablacion_modalidades_v2_01-11-2026/metricas.csv');f,ax=fig(11,4)
 for j,c in enumerate([1,8,32]):
  g=ab[ab.split.eq('test')&ab.context.eq(c)].set_index('modality').loc[['EEG','Eye','Pupil','full']];y=g.auc.to_numpy();x=np.arange(4)+(j-1)*.23
  ax.bar(x,y,.21,color=[GRAY,BLUE,LIGHT][j],label=['Actual','Hasta 8','Hasta 32'][j],zorder=2)
  ax.errorbar(x,y,yerr=np.vstack([y-g.low,g.high-y]),fmt='none',ecolor=DARK,capsize=3,lw=1,zorder=3)
 ax.set(xticks=range(4),xticklabels=['EEG','Mirada','Pupila','Fusión completa'],ylim=(0,1),ylabel='AUC test · macro por participante');ax.axhline(.5,ls='--',color=GRAY,lw=1);ax.legend(frameon=False,loc='upper right',ncol=3);ax.grid(axis='y',zorder=0);save(f,'ablaciones')
 cov=read('resultados/activacion_gsr_v2_recalculo_02-11-2026/cobertura_test.csv');f,axes=plt.subplots(1,2,figsize=(11,3.9),layout='constrained')
 stats=[]
 for c,g in cov.groupby('context'):stats.append((c,np.average(g.mean_history,weights=g.windows),np.average(g.full_fraction,weights=g.windows)*100))
 axes[0].bar(range(3),[v[1] for v in stats],color=[GRAY,BLUE,LIGHT],width=.55);axes[1].bar(range(3),[v[2] for v in stats],color=[GRAY,BLUE,LIGHT],width=.55)
 for ax,k,title,limit in [(axes[0],1,'Historial medio disponible',35),(axes[1],2,'Ventanas con contexto completo (%)',115)]:
  for i,v in enumerate(stats):ax.text(i,v[k]+limit*.025,f'{v[k]:.2f}',ha='center',fontsize=12)
  ax.set(xticks=range(3),xticklabels=['Actual','Hasta 8','Hasta 32'],title=title,ylim=(0,limit));ax.grid(axis='y');ax.set_axisbelow(True)
 save(f,'historial')
 # Editorial changes: direct technical titles, no repeating promotional conclusions.
 titles={0:'Predicción multimodal de<br>atención y activación',1:'Problema y objetivo de investigación',2:'Hipótesis y variables objetivo',3:'Modalidades y características',4:'Arquitectura profesor–estudiante',5:'Particiones y unidad de evaluación',6:'Etapas del desarrollo experimental',7:'Modelos y controles evaluados',8:'Pseudoetiquetas binarias de atención',9:'Extracción EEG por canal',10:'Atención: curvas ROC en test',11:'Atención: comparación controlada',12:'Atención: sensibilidad a la representación',13:'Diagnóstico de las etiquetas GSR originales',14:'Error de alineación en el generador histórico',15:'Criterios de calidad de GSR V2',16:'GSR V2: retención de ventanas',17:'Activación V2: AUC e intervalos de confianza',18:'Activación V2: contrastes temporales pareados',19:'Activación V2: ablación de modalidades',20:'Cobertura efectiva del historial',21:'Interpretación de la hipótesis',22:'Protocolo de evaluación prospectiva',23:'Conclusiones y trabajo pendiente',24:'Definición de la métrica ROC-AUC',25:'Sensibilidad del tamaño de muestra',26:'Referencias y trazabilidad'}
 for i,s in enumerate(slides):
  s['title']=titles[i]
  s['body']=s['body'].replace('class="takeaway"','class="technical-note"')
 slides[0]['chapter']='MAGÍSTER EN CIENCIA DE DATOS · INFORME DE AVANCE'
 slides[0]['body']='<p class="lead">Modelos estáticos y temporales sobre señales<br>EEG, GSR, mirada y pupilometría</p><div class="cover-meta">Mario<br>Avance experimental · noviembre de 2026<br>Resultados hasta el 6 de noviembre · versión técnica del 8 de noviembre</div>'
 slides[10]['body']=img('roc_atencion','ROC promedio por participante en test (n = 8). Leyenda: AUC media individual; interpolación común para visualizar las curvas.')
 slides[10]['source']+='; resultados/temporalidad_eeg_v2_test_29-10-2026/predicciones_test.csv.gz'
 slides[10]['notes']+=' Las curvas se calculan por participante y se interpolan en una malla FPR de 501 puntos. No son curvas sobre ventanas agrupadas; la AUC de la leyenda se calcula antes de interpolar y se verifica contra metricas.csv.'
 slides[11]['body']=table(['Configuración','AUC test','IC95% descriptivo'],[['CatBoost estático · referencia','0,6744','[0,6349; 0,7116]'],['HistBoost estático · control emparejado','0,6602','[0,6139; 0,7043]'],['HistBoost temporal · hasta 32','0,6879','[0,6434; 0,7304]']])+'<p class="technical-note">Contraste emparejado: ΔAUC = +0,0277; IC95% [−0,0041; +0,0505]. Mismas modalidades y ventanas; test reutilizado.</p>'
 slides[12]['body']=img('contrastes_atencion','Diferencias pareadas por participante · IC95% bootstrap descriptivos. Experimentos distintos; sin confirmación externa independiente.')
 slides[16]['body']=img('retencion','Retención: 7.028 / 13.524 en train; 2.584 / 4.662 en validación; 2.184 / 4.025 en test. Total etiquetado: 11.796 (53,1%).')
 slides[17]['body']=img('auc_activacion','Barras desde cero; línea de referencia AUC = 0,50. IC95% bootstrap por participante. Misma familia, hiperparámetros y filas V2 en cada contexto.')
 slides[18]['body']=img('contrastes_activacion','Contraste principal: 32 − actual (azul oscuro). Secundario: 8 − actual. Los IC son descriptivos y no corrigen la búsqueda histórica.')
 slides[19]['body']=img('ablaciones','Test · n = 8 participantes · IC95% descriptivos. Los nueve IC de las diferencias fusión − modalidad individual incluyen cero.')
 slides[20]['body']=img('historial','Promedios ponderados por ventanas de test. El contexto 32 no tiene secuencias completas. La representación usa media y desviación, no orden temporal.')
 slides[5]['body']=table(['Partición','Participantes','Ventanas originales','Ventanas GSR V2'],[['Entrenamiento','25','13.524','7.028'],['Validación','8','4.662','2.584'],['Test','8','4.025','2.184']])+'<p class="technical-note">Ventana de 2 s, paso de 1 s. Separación por participante. Particiones históricamente reutilizadas; P29 fuera del análisis principal.</p>'
 slides[7]['body']=table(['Familia','Modelos / variantes','Control metodológico'],[['Estáticos','Logística, Random Forest, HistBoost, CatBoost','Ventana actual; preprocesamiento ajustado en train'],['Redes temporales','TCN, LSTM, BiLSTM','Controles sin historial; secuencias sin entradas futuras'],['Fusión','Temprana, tardía; ablaciones unimodales','Mismas modalidades permitidas por tarea']])+'<p class="technical-note">Los experimentos iniciales utilizaron otros objetivos y etiquetas. Sus métricas no son directamente comparables con las de GSR V2.</p>'
 # Additional methods and ROC slides inserted without dropping existing content.
 methods=dict(chapter='06 · RESULTADOS CORREGIDOS',title='Activación V2: protocolo de entrenamiento',body=table(['Componente','Configuración'],[['Estimador','HistGradientBoostingClassifier'],['Búsqueda interna','7 / 15 hojas; 5 folds por participante; contextos 1 / 8 / 32'],['Parámetros finales','15 hojas · 300 iteraciones · learning rate 0,05 · L2 = 10'],['Selección','Promedio de AUC interna; configuración compartida entre contextos'],['Verificación','30 ajustes internos · 15 modelos OOF · 3 modelos finales']])+'<p class="technical-note">Ponderación por participante y clase. Imputación y escalado ajustados solo con train. Modelos finales congelados antes de la evaluación externa de esta corrida.</p>',notes='min_samples_leaf=30; early_stopping=False; random_state=20261101. Preprocesamiento: mediana, indicadores de ausencia y StandardScaler. La representación temporal concatena ventana actual, media y desviación del historial disponible. Exposición histórica de test: esta congelación no restaura independencia.',source='resultados/activacion_gsr_v2_recalculo_02-11-2026/protocolo.json',kind='')
 rocslide=dict(chapter='06 · RESULTADOS CORREGIDOS',title='Activación V2: curvas ROC en test',body=img('roc_activacion','ROC promedio de 8 participantes · 2.184 ventanas. AUC por persona verificada contra las métricas guardadas. Rendimiento próximo a la referencia aleatoria.'),notes='Curvas individuales interpoladas sobre una malla FPR común y promediadas. La leyenda presenta media de AUC calculadas directamente por participante, no el área aproximada bajo la curva interpolada. Los IC de los tres AUC absolutos incluyen 0,50.',source='resultados/activacion_gsr_v2_recalculo_02-11-2026/predicciones_externas.csv.gz; resultados/activacion_gsr_v2_recalculo_02-11-2026/metricas.csv',kind='')
 slides.insert(17,methods);slides.insert(19,rocslide)
 (ASSETS/'auditoria_graficos.json').write_text(json.dumps(dict(source_sha256=inputs,roc_auc_checks=metrics_checks,confidence_intervals='from archived participant bootstrap; no new inference',rendering='Matplotlib; SVG editable and embedded PNG for offline HTML'),indent=2))
 return slides

CSS='''
:root{--paper:#fff;--ink:#17334f;--muted:#62748b;--line:#d7e1ed;--accent:#1559a6}
body{background:#e9edf2}.slide{padding:52px 74px 48px;border-top:7px solid #1559a6}.chapter{font-size:14px;letter-spacing:1.5px;color:#1559a6;margin-bottom:24px}h1{font-size:43px;line-height:1.13;letter-spacing:-1.1px;font-weight:600;margin-bottom:28px}h3{color:#1559a6}p{font-size:23px;line-height:1.42}.lead{font-size:29px}.technical-note{font-size:19px;line-height:1.4;color:#53677d;border-left:3px solid #98bade;padding-left:16px;margin-top:25px;max-width:1080px}th{color:#1559a6;font-size:14px;font-weight:700;border-bottom:2px solid #1559a6}td{padding:17px 20px 17px 0;font-size:22px}tbody tr:nth-child(even){background:#f6f9fc}table td:first-child{width:35%}.numbers strong{color:#1559a6;font-size:92px}.hero-metric{color:#1559a6}.timeline div{border-color:#1559a6}.timeline b{color:#1559a6}.cover,.closing{background:#fff;color:#17334f}.cover{border-top:12px solid #1559a6}.cover .chapter{color:#1559a6}.cover h1{color:#17334f;font-size:62px;margin-top:65px}.cover .lead{color:#53677d}.cover-meta{color:#62748b;margin-top:45px}.cover .folio{color:#62748b}.data-figure{margin:0;width:100%}.data-figure img{display:block;width:100%;height:400px;object-fit:contain}.data-figure figcaption{font-size:17px;line-height:1.4;margin-top:12px;color:#53677d;border-top:1px solid #d7e1ed;padding-top:12px}nav button:hover{background:#eaf1f8}.steps b{font-size:25px}.steps span{font-size:20px}.steps li{padding-bottom:19px}.delta{color:#1559a6}blockquote{font-size:33px}#progress{background:#1559a6}.dialog{box-shadow:0 25px 100px #17334f30}.question{font-size:29px}.sources{font-size:23px}
@media(max-width:650px){.reading .data-figure img{height:auto;min-height:170px}.reading .data-figure figcaption{font-size:14px}.reading .technical-note{font-size:16px}.reading .cover h1{font-size:37px}.reading td{font-size:14px}.reading table{table-layout:fixed}.reading td,.reading th{overflow-wrap:anywhere}.reading .steps span{font-size:17px}}
'''
