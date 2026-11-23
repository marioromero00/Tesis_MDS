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
BLUE='#1559a6';LIGHT='#5e9bd6';DARK='#163550';GRAY='#65758a';ORANGE='#c46a1b'
plt.rcParams.update({'font.family':'Arial','font.size':14,'axes.labelcolor':DARK,'text.color':DARK,'xtick.color':'#3e5268','ytick.color':'#3e5268','xtick.labelsize':13,'ytick.labelsize':13,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#cbd5e1','grid.color':'#e5ebf2','axes.titlesize':14,'figure.facecolor':'white','axes.facecolor':'white','savefig.facecolor':'white'})
from matplotlib.ticker import FuncFormatter
def c(x,d=3,sign=False):
 s=(f'{x:+.{d}f}' if sign else f'{x:.{d}f}').replace('-','−').replace('.',',')
 return s
def miles(x,_=None):return f'{x:,.0f}'.replace(',','.')
def comma_axis(ax,axis='y',d=2):
 f=FuncFormatter(lambda v,_:c(v,d))
 (ax.yaxis if axis=='y' else ax.xaxis).set_major_formatter(f)
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
def fmt(x):return c(x,3)
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
 ax.plot([0,1],[0,1],'--',color='#9ca9b7',lw=1,label='Azar')
 ax.set(xlim=(0,1),ylim=(0,1),xlabel='Tasa de falsos positivos (1 − especificidad)',ylabel='Sensibilidad')
 comma_axis(ax,'x',1);comma_axis(ax,'y',1)
 ax.grid(alpha=.6);ax.legend(loc='lower right',frameon=False,fontsize=12);save(f,name)

def dots(ax,xs,y,lo,hi,color,ms=8):
 ax.errorbar(xs,y,yerr=np.vstack([y-lo,hi-y]),fmt='o',color=color,ecolor=color,capsize=5,lw=1.8,ms=ms,zorder=3)

def apply(slides):
 a=read('resultados/temporalidad_eeg_v2_test_29-10-2026/metricas.csv').set_index('strategy')
 p=read('resultados/temporalidad_eeg_v2_test_29-10-2026/predicciones_test.csv.gz')
 roc(p,'strategy',[('inductivo_ctx1','CatBoost · solo ventana actual',GRAY),('inductivo_estatico_pareado','HGB · solo ventana actual',LIGHT),('inductivo_ctx32','HGB · hasta 32 ventanas',BLUE)],'roc_atencion',[a.loc[k,'auc_macro'] for k in ['inductivo_ctx1','inductivo_estatico_pareado','inductivo_ctx32']])
 act=read('resultados/activacion_gsr_v2_recalculo_02-11-2026/metricas.csv')
 pred=read('resultados/activacion_gsr_v2_recalculo_02-11-2026/predicciones_externas.csv.gz')
 roc(pred[pred.split.eq('test')],'context',[(1,'Solo ventana actual',GRAY),(8,'Hasta 8',LIGHT),(32,'Hasta 32 (principal)',BLUE)],'roc_activacion',[act[act.split.eq('test')&act.context.eq(c_)].auc.item() for c_ in [1,8,32]])
 # Activation AUC: points with participant-bootstrap CIs, zoomed around chance.
 f,axes=plt.subplots(1,2,figsize=(11,4),sharey=True,layout='constrained')
 for ax,split,title in zip(axes,['validation','test'],['Validación · 8 personas','Test · 8 personas']):
  g=act[act.split.eq(split)].sort_values('context');y=g.auc.to_numpy()
  for i,(yy,lo,hi,col) in enumerate(zip(y,g.low,g.high,[GRAY,LIGHT,BLUE])):
   dots(ax,[i],np.array([yy]),np.array([lo]),np.array([hi]),col,9)
   ax.text(i+.12,yy,c(yy),va='center',fontsize=13,color=DARK)
  ax.axhline(.5,color=ORANGE,ls='--',lw=1.2);ax.text(-.35,.503,'azar',color=ORANGE,va='bottom',ha='left',fontsize=12)
  ax.set(ylim=(.40,.66),xlim=(-.4,2.5),xticks=range(3),xticklabels=['Solo ventana actual','Hasta 8','Hasta 32'],title=title);ax.grid(axis='y',zorder=0)
 comma_axis(axes[0],'y',2);axes[0].set_ylabel('AUC media por persona');save(f,'auc_activacion')
 # Paired contrasts, test first.
 con=read('resultados/activacion_gsr_v2_recalculo_02-11-2026/contrastes.csv')
 f,ax=fig(11,4);labels=[]
 order=[(s,c_) for s in ['test','validation','oof_train'] for c_ in [32,8]]
 for j,(split,c_) in enumerate(order):
  r=con[con.split.eq(split)&con.context.eq(c_)].iloc[0];color=BLUE if c_==32 else LIGHT
  ax.errorbar(r.delta,j,xerr=[[r.delta-r.low],[r.high-r.delta]],fmt='o',color=color,capsize=5,ms=8,lw=2)
  labels.append({'oof_train':'Entrenamiento (OOF)','validation':'Validación','test':'Test'}[split]+(' · hasta 32 (principal)' if c_==32 else ' · hasta 8'))
  ax.text(.103,j,f'{c(r.delta,3,True)}   [{c(r.low,3,True)}; {c(r.high,3,True)}]',va='center',fontsize=14)
 [ax.axhspan(k-.5,k+1.5,color='#f1f5fa',zorder=0) for k in (0,4)];ax.axvline(0,color=ORANGE,ls='--',lw=1.2);ax.set(yticks=range(6),yticklabels=labels,ylim=(5.5,-.5),xlim=(-.075,.18),xlabel='Diferencia de AUC por persona: con historial − solo ventana actual')
 ax.set_xticks([-.05,0,.05,.1]);comma_axis(ax,'x',2);ax.grid(axis='x');save(f,'contrastes_activacion')
 f,ax=fig(11,4)
 ac=read('resultados/temporalidad_eeg_v2_test_29-10-2026/contrastes.csv')
 r1=ac[ac.temporal.eq('inductivo_ctx32')&ac.baseline.eq('inductivo_estatico_pareado')].iloc[0]
 cc=read('resultados/comparacion_comun_binaria_30-10-2026/contrastes.csv')
 r2=cc[cc.task.eq('atencion')&cc.split.eq('test')&cc.contrast.eq('temporal_full')].iloc[0]
 values=[(r1.delta_auc,r1.ci_low,r1.ci_high),(r2.delta,r2.low,r2.high)]
 for i,(v,lo,hi) in enumerate(values):
  ax.errorbar(v,i,xerr=[[v-lo],[hi-v]],fmt='o',color=BLUE,capsize=6,lw=2,ms=9)
  ax.text(.064,i,f'{c(v,3,True)}\n[{c(lo,3,True)}; {c(hi,3,True)}]',va='center',fontsize=14)
 ax.axvline(0,ls='--',color=ORANGE,lw=1.2);ax.set(yticks=[0,1],yticklabels=['Comparación fijada','Media y desviación de todo (después)'],xlim=(-.02,.09),ylim=(1.7,-.7),xlabel='Diferencia de AUC en test: HGB con historial − HGB solo ventana actual');ax.set_xticks([-.02,0,.02,.04,.06]);comma_axis(ax,'x',2);ax.grid(axis='x');save(f,'contrastes_atencion')
 # Label retention with absolute counts.
 q=read('resultados/etiquetas_gsr_calidad_v2_01-11-2026/resumen_personas.csv').groupby('split')[['total','new_labelled']].sum().loc[['train','validation','test']]
 f,ax=fig(11,3.8);ys=np.arange(3)
 ax.barh(ys,q.new_labelled,color=BLUE,label='Con etiqueta V2',height=.5)
 ax.barh(ys,q.total-q.new_labelled,left=q.new_labelled,color='#b9cde3',label='Sin etiqueta V2',height=.5)
 for i,r in enumerate(q.itertuples()):
  ax.text(r.new_labelled/2,i,miles(r.new_labelled),ha='center',va='center',color='white',weight='bold',fontsize=13)
  ax.text(r.total+200,i,c(r.new_labelled/r.total*100,1)+' % con etiqueta',va='center',fontsize=13)
 ax.xaxis.set_major_formatter(FuncFormatter(miles))
 ax.set(yticks=ys,yticklabels=['Entrenamiento','Validación','Test'],xlabel='Número de ventanas',xlim=(0,17500));ax.invert_yaxis();ax.legend(frameon=False,loc='lower right');ax.grid(axis='x',zorder=0);ax.set_axisbelow(True);save(f,'retencion')
 ab=read('resultados/ablacion_modalidades_v2_01-11-2026/metricas.csv')
 cf=read('resultados/ablacion_modalidades_v2_01-11-2026/contrastes_fusion.csv');f,ax=fig(11,4)
 mods=[('EEG','EEG'),('Eye','mirada'),('Pupil','pupila')]
 for j,c_ in enumerate([1,8,32]):
  for k,(m,lab) in enumerate(mods):
   r=cf[cf.split.eq('test')&cf.context.eq(c_)&cf.contrast.eq('full_minus_'+m)].iloc[0]
   x=k+(j-1)*.24
   ax.errorbar(x,r.delta,yerr=[[r.delta-r.low],[r.high-r.delta]],fmt='o',color=[GRAY,LIGHT,BLUE][j],capsize=5,ms=8,lw=1.8,zorder=3)
  
 for j,lab in enumerate(['Solo ventana actual','Hasta 8','Hasta 32 (principal)']):ax.plot([],[],'o',ms=8,color=[GRAY,LIGHT,BLUE][j],label=lab)
 ax.axhline(0,ls='--',color=ORANGE,lw=1.2)
 ax.set(xticks=range(3),xticklabels=['Fusión − EEG','Fusión − mirada','Fusión − pupila'],xlim=(-.5,2.6),ylabel='Diferencia de AUC en test');comma_axis(ax,'y',2);ax.legend(frameon=False,loc='lower center',bbox_to_anchor=(.5,1.0),ncol=3);ax.grid(axis='y',zorder=0);save(f,'ablaciones')
 cov=read('resultados/activacion_gsr_v2_recalculo_02-11-2026/cobertura_test.csv');f,axes=plt.subplots(1,2,figsize=(11,3.9),layout='constrained')
 stats=[]
 for c_,g in cov.groupby('context'):stats.append((c_,np.average(g.mean_history,weights=g.windows),np.average(g.full_fraction,weights=g.windows)*100))
 cols=[GRAY,LIGHT,BLUE]
 axes[0].bar(range(3),[v[1] for v in stats],color=cols,width=.55)
 for nominal,i in [(8,1),(32,2)]:
  axes[0].plot([i-.38,i+.38],[nominal,nominal],ls='--',color=ORANGE,lw=1.4)
 axes[0].text(2,33.2,'máximo: 32',ha='center',color=ORANGE,fontsize=11);axes[0].text(1,9.2,'máximo: 8',ha='center',color=ORANGE,fontsize=11)
 for i,v in enumerate(stats):axes[0].text(i,v[1]+.8,c(v[1],1),ha='center',fontsize=13)
 axes[1].bar(range(3),[v[2] for v in stats],color=['#d5dde7',LIGHT,BLUE],width=.55)
 for i,v in enumerate(stats):axes[1].text(i,v[2]+3,c(v[2],1).replace(',0','')+' %',ha='center',fontsize=13)
 for ax,title,limit in [(axes[0],'Ventanas usadas, incluida la actual (media)',37),(axes[1],'Ventanas con el historial completo',115)]:
  ax.set(xticks=range(3),xticklabels=['Solo ventana actual','Hasta 8','Hasta 32'],title=title,ylim=(0,limit));ax.grid(axis='y');ax.set_axisbelow(True)
 axes[1].yaxis.set_major_formatter(FuncFormatter(lambda v,_:f'{v:.0f} %'))
 save(f,'historial')
 # ---- Gráficos nuevos v5 ----
 E=read('resultados/etiquetas_gsr_calidad_v2_01-11-2026/etiquetas.csv.gz')
 U=read('resultados/etiquetas_gsr_calidad_v2_01-11-2026/umbrales.csv').set_index('participant')
 # 1) Ejemplo de pseudoetiqueta: P22, segmento más largo.
 seg=E[(E.participant.eq('P22'))&(E.segment_id.eq(185))].copy()
 t0=pd.to_datetime(seg.window_start_utc).min();seg['t']=(pd.to_datetime(seg.window_start_utc)-t0).dt.total_seconds()
 med=U.loc['P22','median'];f,ax=fig(11,3.6)
 ax.plot(seg.t,seg.score6s_quality,color='#c3cfdc',lw=1.5,zorder=1)
 hi=seg[seg.activation_binary_v2.eq(1)];lo=seg[seg.activation_binary_v2.eq(0)]
 ax.scatter(hi.t,hi.score6s_quality,color=BLUE,s=34,zorder=3,label='Alta (sobre la mediana)')
 ax.scatter(lo.t,lo.score6s_quality,color='#9aa8b8',s=34,zorder=3,label='Baja')
 ax.axhline(med,color=DARK,ls='--',lw=1.4);ax.text(seg.t.max()+1,med+.12,'mediana de P22',color=DARK,va='bottom',fontsize=12)
 ax.set(xlabel='Segundos desde el inicio del estímulo',ylabel='Puntaje GSR de 6 s');comma_axis(ax,'y',1)
 ax.set_xlim(seg.t.min()-1,seg.t.max()+9);ax.legend(frameon=False,loc='upper left',ncol=2);ax.grid(axis='y');save(f,'ejemplo_etiqueta')
 # 2) Participantes por partición.
 P=read('resultados/modelado/particion_participantes.csv')
 order=['train','validation','test','sensitivity','excluded'];names={'train':'Entrenamiento','validation':'Validación','test':'Test','sensitivity':'Sensibilidad (P29)','excluded':'Excluidas'}
 colors={'train':BLUE,'validation':LIGHT,'test':DARK,'sensitivity':'#7b8b9b','excluded':'#d5dde7'}
 f,ax=fig(11,3.4);x0=0
 for sp in order:
  ids=P[P.split.eq(sp)].participant.tolist();ncol=5
  for k,pid in enumerate(ids):
   ax.scatter(x0+k%ncol,-(k//ncol),s=420,color=colors[sp],zorder=3,edgecolor='white')
  w=min(len(ids),ncol)
  ax.text(x0+(w-1)/2,1.0,names[sp],ha='center',va='bottom',fontsize=14,color=DARK,weight='bold')
  ax.text(x0+(w-1)/2,.62,f'{len(ids)} persona'+('s' if len(ids)>1 else '')+({'train':' · 13.524 ventanas','validation':' · 4.662','test':' · 4.025'}.get(sp,'')),ha='center',va='bottom',fontsize=12,color=GRAY)
  x0+=w+2.2
 ax.set(xlim=(-.8,x0-1.2),ylim=(-4.6,1.6));ax.axis('off');save(f,'particiones')
 # 3) Profesor igualitario vs PCA (AUC OOF train, modelos sin historial).
 Q=read('resultados/profesor_binario_reconstruido_29-10-2026/comparacion_profesores_modelos.csv')
 fams=[('Logistica','current','Logística'),('RandomForest','current','Random Forest'),('TCN','repeat_current','TCN'),('LSTM','repeat_current','LSTM')]
 f,ax=fig(11,3.7)
 for j,(prof,col,lab) in enumerate([('igualitario','#9aa8b8','Pesos iguales'),('pca',BLUE,'PCA')]):
  vals=[Q[Q.profesor.eq(prof)&Q.family.eq(fa)&Q['mode'].eq(mo)].iloc[0] for fa,mo,_ in fams]
  xs=np.arange(4)+(j-.5)*.36
  ax.bar(xs,[v.auc_macro-.5 for v in vals],.34,bottom=.5,color=col,label=lab,zorder=2)
  for xx,v in zip(xs,vals):ax.text(xx,v.auc_macro+.004,c(v.auc_macro),ha='center',fontsize=12)
 ax.axhline(.5,color=ORANGE,ls='--',lw=1.2);ax.set(xticks=range(4),xticklabels=[l for *_,l in fams],ylim=(.48,.66),yticks=[.50,.55,.60,.65],ylabel='AUC en entrenamiento (OOF)');comma_axis(ax,'y',2)
 ax.legend(frameon=False,loc='upper left',ncol=2);ax.grid(axis='y',zorder=0);save(f,'profesores')
 # 4) Atención por persona: HGB sin historial vs hasta 32.
 M=read('resultados/temporalidad_eeg_v2_test_29-10-2026/metricas_participantes.csv')
 a0=M[M.strategy.eq('inductivo_estatico_pareado')].set_index('participant').auc;a1=M[M.strategy.eq('inductivo_ctx32')].set_index('participant').auc
 f,ax=fig(11,3.9)
 ys={}
 last=-9
 order_=list(a1.sort_values().index);pos=[a1[q] for q in order_]
 for _ in range(200):
  for q in range(1,len(pos)):
   if pos[q]-pos[q-1]<.026:
    m=(pos[q]+pos[q-1])/2;pos[q-1]=m-.026/2;pos[q]=m+.026/2
 ys=dict(zip(order_,pos))
 for pid in a0.index:
  up=a1[pid]>a0[pid];col=BLUE if up else '#7b8b9b'
  ax.plot([0,1],[a0[pid],a1[pid]],color=col,lw=2,marker='o',ms=7,alpha=.9)
  ax.plot([1.005,1.06],[a1[pid],ys[pid]],color=col,lw=.8)
  ax.text(1.07,ys[pid],pid,va='center',fontsize=12,color=col)
 ax.plot([0,1],[a0.mean(),a1.mean()],color=DARK,lw=4,marker='o',ms=10,zorder=4)
 ax.text(-.04,a0.mean(),'media',ha='right',va='center',fontsize=13,color=DARK,weight='bold')
 ax.axhline(.5,color='#c3cfdc',ls='--',lw=1)
 ax.set(xticks=[0,1],xticklabels=['HGB · solo ventana actual','HGB · hasta 32 ventanas'],xlim=(-.3,1.25),ylabel='AUC por persona (test)');comma_axis(ax,'y',2);ax.grid(axis='y');save(f,'atencion_personas')
 # 5) Diagnóstico de la etiqueta antigua (25 personas de entrenamiento): dos paneles.
 Dg=read('resultados/activacion_diagnostico_nested_30-10-2026/diagnostico_personas.csv');Dg['u']=Dg.score6s_unique/Dg.windows*100;Dg['pos']=Dg.positive_rate*100
 f,(a1_,a2_)=plt.subplots(1,2,figsize=(11,3.9),layout='constrained',gridspec_kw=dict(width_ratios=[1,1]))
 cv=Dg.sort_values('gsr_window_valid_mean')
 a1_.bar(range(len(cv)),cv.gsr_window_valid_mean*100,color=[DARK if p_=='P4' else '#b9cde3' for p_ in cv.participant],width=.8)
 i4_=list(cv.participant).index('P4');a1_.annotate('P4: solo 12,6 %',(i4_,12.6),xytext=(4,112),fontsize=13,color=DARK,weight='bold',arrowprops=dict(arrowstyle='-',color=DARK,lw=1))
 a1_.set(xticks=[],ylim=(0,125),yticks=[0,25,50,75,100],title='GSR válido por persona');a1_.yaxis.set_major_formatter(FuncFormatter(lambda v,_:f'{v:.0f} %'));a1_.grid(axis='y');a1_.set_axisbelow(True)
 sc=Dg.sort_values('pos')
 a2_.bar(range(len(sc)),sc.pos,color=[DARK if p_ in ('P34','P46') else '#b9cde3' for p_ in sc.participant],width=.8)
 a2_.axhline(50,color=ORANGE,ls='--',lw=1.2)
 for k_,p_ in enumerate(sc.participant):
  if p_=='P34':a2_.text(k_-.6,sc.pos.iloc[k_]+1,'P34',ha='right',fontsize=13,color=DARK,weight='bold')
  if p_=='P46':a2_.text(k_-.6,sc.pos.iloc[k_]+1,'P46',ha='right',fontsize=13,color=DARK,weight='bold')
 a2_.set(xticks=[],xlim=(-4,len(sc)),ylim=(0,60),title='Ventanas con clase "alta" por persona');a2_.yaxis.set_major_formatter(FuncFormatter(lambda v,_:f'{v:.0f} %'));a2_.grid(axis='y');a2_.set_axisbelow(True)
 save(f,'calidad_gsr')
 # 6) Cambio de clase entre etiqueta antigua y V2.
 Rp=read('resultados/etiquetas_gsr_calidad_v2_01-11-2026/resumen_personas.csv')
 Rp['ch']=Rp.changed_on_common/Rp.common*100;Rc=Rp[Rp.common>0].sort_values('ch')
 f,ax=fig(11,3.6);ax.bar(range(len(Rc)),Rc.ch,color=BLUE,width=.75)
 tot=Rp.changed_on_common.sum()/Rp.common.sum()*100
 ax.axhline(50,color=ORANGE,ls='--',lw=1.2);ax.text(0,52,'50 %',ha='left',color=ORANGE,fontsize=12,bbox=dict(fc='white',ec='none',pad=2),zorder=5)
 ax.set(xticks=[],ylim=(0,80),xlabel=f'{len(Rc)} personas, ordenadas',ylabel='Ventanas que cambian de clase');ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_:f'{v:.0f} %'))
 ax.text(0,76,f'En total: {miles(Rp.changed_on_common.sum())} de {miles(Rp.common.sum())} ventanas ({c(tot,1)} %)',fontsize=14,color=DARK,weight='bold',va='top')
 ax.grid(axis='y');ax.set_axisbelow(True);save(f,'cambio_etiquetas')
 # 7) Síntesis: contrastes clave en un solo gráfico.
 rows=[('Atención · comparación fijada',r1.delta_auc,r1.ci_low,r1.ci_high,BLUE),('Atención · media y desviación de todo (después)',r2.delta,r2.low,r2.high,LIGHT)]
 for split,cc_,lab,col in [('test',32,'Activación · principal · test',BLUE),('validation',32,'Activación · principal · validación',BLUE),('test',8,'Activación · hasta 8 · test',LIGHT),('validation',8,'Activación · hasta 8 · validación',LIGHT)]:
  r=con[con.split.eq(split)&con.context.eq(cc_)].iloc[0];rows.append((lab,r.delta,r.low,r.high,col))
 f,ax=fig(11,3.9)
 for j,(lab,d,lo,hi,col) in enumerate(rows):
  ax.errorbar(d,j,xerr=[[d-lo],[hi-d]],fmt='o',color=col,capsize=5,ms=9,lw=2)
  ax.text(.085,j,c(d,3,True),va='center',fontsize=14,color=DARK)
 ax.axhspan(1.5,5.5,color='#f1f5fa',zorder=0)
 ax.axvline(0,color=ORANGE,ls='--',lw=1.2);ax.set(yticks=range(len(rows)),yticklabels=[r[0] for r in rows],ylim=(len(rows)-.5,-.5),xlim=(-.04,.1),xlabel='Diferencia de AUC: con historial − sin historial');ax.set_xticks([-.025,0,.025,.05,.075]);comma_axis(ax,'x',3);ax.grid(axis='x');save(f,'sintesis')
 # 8) Tamaño de muestra.
 f,ax=fig(11,3.2);labs=['Atención · variabilidad de test','Activación · variabilidad de validación','Activación · variabilidad de test','Activación · variabilidad de entrenamiento (OOF)'];ns=[62,72,101,767]
 ax.barh(range(4),ns,color=[GRAY,BLUE,BLUE,BLUE],height=.55)
 for i,n in enumerate(ns):ax.text(n+12,i,str(n),va='center',fontsize=15,color=DARK,weight='bold')
 ax.set(yticks=range(4),yticklabels=labs,xlim=(0,880),ylim=(3.6,-.6),xlabel='Personas nuevas evaluables');ax.grid(axis='x');ax.set_axisbelow(True);save(f,'muestra')
 # 9) Cascada de ventanas GSR V2.
 Mo=read('resultados/etiquetas_gsr_calidad_v2_01-11-2026/motivos.csv').groupby('label_reason').windows.sum()
 total=int(Mo.sum());steps=[('Ventanas\noriginales',total,None),('1 · Calidad GSR\n(cobertura ≥ 50 %)',-int(Mo.get('cobertura_o_flag_invalido',0)),None),('3 · Contexto: 5 ventanas\nválidas seguidas',-int(Mo.get('historial_insuficiente',0)),None),('4 · Empates con\nla mediana',-int(Mo.get('empate_mediana',0)),None)]
 f,ax=fig(11,3.9);level=0
 for k,(lab,v,_) in enumerate(steps):
  if k==0:ax.bar(k,v,color='#b9cde3',width=.6);level=v;ax.text(k,v+250,miles(v),ha='center',fontsize=14,color=DARK)
  else:
   ax.bar(k,max(-v,180),bottom=level+v,color='#9aa8b8',width=.6);ax.text(k,level+400,'−'+miles(-v)+(' (P4)' if k==1 else ''),ha='center',fontsize=14,color=DARK);level+=v
 ax.bar(len(steps),level,color=BLUE,width=.6);ax.text(len(steps),level+250,miles(level),ha='center',fontsize=15,color=DARK,weight='bold')
 assert level==int(Mo.get('etiquetada'))
 ax.set(xticks=range(len(steps)+1),xticklabels=[s_[0] for s_ in steps]+['Con etiqueta\nV2'],ylim=(0,26000));ax.yaxis.set_major_formatter(FuncFormatter(miles));ax.grid(axis='y');ax.set_axisbelow(True);save(f,'cascada')
 # 10) Activación por persona: solo ventana actual vs hasta 32 (test).
 Mp=read('resultados/activacion_gsr_v2_recalculo_02-11-2026/metricas_personas.csv');Mt=Mp[Mp.split.eq('test')]
 b0=Mt[Mt.context.eq(1)].set_index('participant').auc;b1=Mt[Mt.context.eq(32)].set_index('participant').auc
 f,ax=fig(11,3.9);ys={};last=-9
 order_=list(b1.sort_values().index);pos=[b1[q] for q in order_]
 for _ in range(200):
  for q in range(1,len(pos)):
   if pos[q]-pos[q-1]<.034:
    m=(pos[q]+pos[q-1])/2;pos[q-1]=m-.034/2;pos[q]=m+.034/2
 ys=dict(zip(order_,pos))
 for pid in b0.index:
  up=b1[pid]>b0[pid];col=BLUE if up else '#7b8b9b'
  ax.plot([0,1],[b0[pid],b1[pid]],color=col,lw=2,marker='o',ms=7,alpha=.9)
  ax.plot([1.005,1.06],[b1[pid],ys[pid]],color=col,lw=.8);ax.text(1.07,ys[pid],pid,va='center',fontsize=12,color=col)
 ax.plot([0,1],[b0.mean(),b1.mean()],color=DARK,lw=4,marker='o',ms=10,zorder=4)
 ax.text(-.04,b0.mean(),'media',ha='right',va='center',fontsize=13,color=DARK,weight='bold')
 ax.axhline(.5,color=ORANGE,ls='--',lw=1.2)
 ax.set(xticks=[0,1],xticklabels=['Solo ventana actual','Hasta 32 ventanas'],xlim=(-.3,1.25),ylabel='AUC por persona (test)');comma_axis(ax,'y',2);ax.grid(axis='y');save(f,'activacion_personas')
 # 11) Historial real por persona (test).
 Cv=read('resultados/activacion_gsr_v2_recalculo_02-11-2026/cobertura_test.csv')
 f,ax=fig(11,3.9)
 for j,(ctx,col) in enumerate([(8,LIGHT),(32,BLUE)]):
  g=Cv[Cv.context.eq(ctx)].sort_values('participant');xs=np.arange(len(g))+(j-.5)*.3
  ax.bar(xs,g.mean_history,.28,color=col,label=f'Hasta {ctx}',zorder=2)
  ax.axhline(ctx,color=col,ls=':',lw=1.5);ax.text(-.45,ctx+.6,f'máximo {ctx}',ha='left',color=col,fontsize=12)
 ax.set(xticks=range(len(g)),xticklabels=g.participant,ylim=(0,35),ylabel='Ventanas usadas en promedio\n(incluida la actual)');ax.legend(frameon=False,loc='upper right',bbox_to_anchor=(1,.86),ncol=2);ax.grid(axis='y',zorder=0);save(f,'historial_personas')
 # ---- Gráficos de resultados finales (v6, 18-11-2026) ----
 import sys as _sys
 _sys.path.insert(0,str(ROOT/'scripts'))
 RF=ROOT/'resultados'
 fin=read('resultados/cierre_final_41p_16-11-2026/contrastes.csv');rob=read('resultados/cierre_robustez_41p_16-11-2026/resultados.csv')
 lag6=read('resultados/ampliacion_41p_16-11-2026/enmienda_e1_lag6/contrastes.csv');pos=read('resultados/explicativo_posicion_41p_18-11-2026/contrastes.csv')
 amp=read('resultados/ampliacion_41p_16-11-2026/contrastes.csv')
 def row(df,task,col,val):
  r=df[df.task.eq(task)&df[col].eq(val)].iloc[0];return r.delta,r.low95,r.high95
 # A) Resultado principal y robustez de la partición
 f,ax=fig(11,3.6);items=[]
 for task,lab in [('atencion','Atención'),('activacion','Activación')]:
  items.append((f'{lab} · partición registrada',*row(fin[fin.role.eq('principal')],task,'contrast','hgb_c32 − hgb_c1'),BLUE))
  for s_ in ['101','202','303']:
   r=rob[rob.task.eq(task)&rob.prueba.eq(f'R3 partición {s_}')].iloc[0];items.append((f'{lab} · otra partición',r.delta,r.low95,r.high95,LIGHT))
 for j,(lab,d_,lo,hi,col) in enumerate(items):
  ax.errorbar(d_,j,xerr=[[d_-lo],[hi-d_]],fmt='o',color=col,capsize=5,ms=8,lw=2);ax.text(.095,j,c(d_,3,True),va='center',fontsize=13)
 ax.axhspan(3.5,7.5,color='#f1f5fa',zorder=0);ax.axvline(0,color=ORANGE,ls='--',lw=1.2)
 ax.set(yticks=range(len(items)),yticklabels=[i[0] for i in items],ylim=(len(items)-.5,-.5),xlim=(-.02,.105),xlabel='Diferencia de AUC por persona: hasta 32 ventanas − sin historial (41 personas)');comma_axis(ax,'x',2);ax.grid(axis='x');save(f,'final_principal')
 # B) ¿De dónde viene la mejora?
 f,axes=plt.subplots(1,2,figsize=(11,3.9),sharex=True,layout='constrained')
 for ax,(task,lab) in zip(axes,[('atencion','Atención'),('activacion','Activación')]):
  its=[('Historial real',*row(fin,task,'contrast','hgb_c32 − hgb_c1'),BLUE),
       ('Historial placebo',*row(rob,task,'prueba','R1 referencia'),GRAY),
       ('Solo segundos en la página',*row(pos,task,'contrast','pos_c1 − hgb_c1'),ORANGE if False else DARK),
       ('Historial sin los 6 s de la etiqueta',*row(lag6,task,'contrast','lag6_real − hgb_c1'),LIGHT)]
  for j,(l_,d_,lo,hi,col) in enumerate(its):
   ax.errorbar(d_,j,xerr=[[d_-lo],[hi-d_]],fmt='o',color=col,capsize=5,ms=9,lw=2);ax.text(d_,j-.3,c(d_,3,True),ha='center',fontsize=12)
  ax.axvline(0,color=ORANGE,ls='--',lw=1.2);ax.set(title=lab,yticks=range(4),yticklabels=[i[0] for i in its],ylim=(3.6,-.7));ax.grid(axis='x');comma_axis(ax,'x',2)
 axes[1].tick_params(labelleft=False);fig_=f;f.supxlabel('Mejora de AUC frente al modelo sin historial (41 personas)',fontsize=12);save(f,'origen_mejora')
 # C) Etiqueta según segundos en la página
 import cierre_experimental_v3 as V3m
 d0=V3m.load_data();f,ax=fig(11,3.6)
 for task,lab,col in [('atencion','Atención',BLUE),('activacion','Activación',GRAY)]:
  T=V3m.Task(d0,task);l=np.minimum(T.hist[32][1][T.lab_pos],12)
  g=pd.DataFrame(dict(p=T.lab.participant,y=T.lab.y,pos=l)).groupby(['p','pos']).y.mean().groupby('pos').mean()
  ax.plot(g.index,g.values*100,marker='o',color=col,lw=2.4,ms=7,label=lab)
 ax.axhline(50,color='#c3cfdc',ls='--',lw=1);ax.set(xlabel='Segundos transcurridos en la página (12 = 12 o más)',ylabel='Ventanas con clase "alta"',xticks=range(1,13),ylim=(30,68))
 ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_:f'{v:.0f} %'));ax.legend(frameon=False,loc='lower right');ax.grid(axis='y');save(f,'posicion_etiqueta')
 # D) Activación: real vs placebo sin solapamiento
 f,ax=fig(11,3.2);its=[]
 for task,lab in [('activacion','Activación'),('atencion','Atención')]:
  its.append((f'{lab} · historial real − placebo',*row(lag6,task,'contrast','lag6_real − lag6_placebo'),BLUE if task=='activacion' else GRAY))
 its.append(('Activación · historial − solo segundos en la página',*row(pos,'activacion','contrast','hgb_c32 − pos_c1'),LIGHT))
 its.append(('Atención · historial − solo segundos en la página',*row(pos,'atencion','contrast','hgb_c32 − pos_c1'),GRAY))
 for j,(l_,d_,lo,hi,col) in enumerate(its):
  ax.errorbar(d_,j,xerr=[[d_-lo],[hi-d_]],fmt='o',color=col,capsize=5,ms=9,lw=2);ax.text(.085,j,f'{c(d_,3,True)}  [{c(lo,3,True)}; {c(hi,3,True)}]',va='center',fontsize=12)
 ax.axvline(0,color=ORANGE,ls='--',lw=1.2);ax.set(yticks=range(4),yticklabels=[i[0] for i in its],ylim=(3.5,-.5),xlim=(-.02,.12),xlabel='Diferencia de AUC por persona (41 personas)');comma_axis(ax,'x',2);ax.grid(axis='x');save(f,'activacion_temporal')
 # E) Fusión con la misma familia
 f,ax=fig(11,3.2);its=[]
 for task,lab in [('atencion','Atención'),('activacion','Activación')]:
  for a_,b_,txt in [('mlp_tardia','mlp_temprana','tardía − temprana'),('mlp_intermedia','mlp_temprana','intermedia − temprana')]:
   r=amp[amp.task.eq(task)&amp.contrast.eq(f'{a_} − {b_}')].iloc[0];its.append((f'{lab} · {txt}',r.delta,r.low95,r.high95,BLUE if task=='atencion' else GRAY))
 for j,(l_,d_,lo,hi,col) in enumerate(its):
  ax.errorbar(d_,j,xerr=[[d_-lo],[hi-d_]],fmt='o',color=col,capsize=5,ms=9,lw=2);ax.text(.05,j,c(d_,3,True),va='center',fontsize=13)
 ax.axvline(0,color=ORANGE,ls='--',lw=1.2);ax.set(yticks=range(4),yticklabels=[i[0] for i in its],ylim=(3.5,-.5),xlim=(-.045,.06),xlabel='Diferencia de AUC por persona (MLP, 41 personas)');comma_axis(ax,'x',2);ax.grid(axis='x');save(f,'fusion_final')
 # F) Sesión y tipo de página
 fq=read('resultados/ampliacion_41p_16-11-2026/fatiga_por_quintil.csv');pc=read('resultados/ampliacion_41p_16-11-2026/por_categoria.csv')
 f,(a1_,a2_)=plt.subplots(1,2,figsize=(11,3.9),layout='constrained')
 for task,lab,col in [('atencion','Atención',BLUE),('activacion','Activación',GRAY)]:
  g=fq[fq.task.eq(task)&fq.strategy.eq('hgb_c32')];a1_.plot(g.quintil,g.auc,marker='o',color=col,lw=2.4,ms=7,label=lab)
  a1_.text(5.12,g.auc.iloc[-1],lab,va='center',fontsize=12,color=col)
 a1_.axhline(.5,color=ORANGE,ls='--',lw=1.2);a1_.set(title='AUC a lo largo de la sesión',xlabel='Quinto de la sesión',xticks=range(1,6),xlim=(.8,6.1),ylim=(.45,.78));comma_axis(a1_,'y',2);a1_.grid(axis='y')
 cats=['sitio web','numerado','diseño','texto'];g=pc[pc.task.eq('atencion')&pc.categoria.isin(cats)]
 xs=np.arange(len(cats))
 for j,(s_,col,lab) in enumerate([('hgb_c1',GRAY,'Sin historial'),('hgb_c32',BLUE,'Con historial')]):
  v=[g[g.strategy.eq(s_)&g.categoria.eq(k)].auc.item() for k in cats];a2_.bar(xs+(j-.5)*.36,v,.34,color=col,label=lab)
  for x_,y_ in zip(xs+(j-.5)*.36,v):a2_.text(x_,y_+.005,c(y_,2),ha='center',fontsize=11)
 a2_.set(title='Atención por tipo de página',xticks=xs,xticklabels=cats,ylim=(.5,.76));comma_axis(a2_,'y',2);a2_.legend(frameon=False,loc='upper right',ncol=2);a2_.grid(axis='y');a2_.set_axisbelow(True)
 save(f,'sesion_pagina')
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
