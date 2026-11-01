"""Comparación por persona en validation: temporalidad y calibración separadas."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from evaluar_temporalidad_eeg_v2 import OUT
m=pd.read_csv(OUT/'metricas_participantes.csv');summary=pd.read_csv(OUT/'metricas.csv').set_index('strategy')
fig,axes=plt.subplots(1,2,figsize=(12,5),sharey=True,layout='constrained')
for ax,scope,title in zip(axes,['inductivo','relativo_offline'],['Principal: sin calibración personal','Secundario: normalización offline']):
    cols=[f'{scope}_ctx{c}' for c in [1,8,32]]
    w=m[m.strategy.isin(cols)].pivot(index='participant',columns='strategy',values='auc')[cols]
    for p,r in w.iterrows():ax.plot([0,1,2],r,alpha=.55,lw=1,marker='o',ms=3,label=p)
    avg=summary.loc[cols,'auc_macro'].to_numpy();ax.plot([0,1,2],avg,color='black',lw=3,marker='D',ms=6,label='Promedio')
    for i,v in enumerate(avg):ax.annotate(f'{v:.3f}',(i,v),xytext=(0,9),textcoords='offset points',ha='center',fontweight='bold')
    ax.set_xticks([0,1,2],['Actual\n2 s','8 ventanas\nhasta 9 s','32 ventanas\nhasta 33 s']);ax.set_title(title,fontsize=12)
    ax.axhline(.5,color='gray',ls=':',lw=1);ax.grid(axis='y',alpha=.2);ax.set_ylim(.45,.9)
axes[0].set_ylabel('ROC-AUC por persona');axes[1].legend(loc='upper left',bbox_to_anchor=(1,1),frameon=False)
fig.suptitle('Aporte del historial EEG/GSR · 8 participantes de validación',fontsize=15)
fig.savefig(OUT/'comparacion_temporalidad.png',dpi=180)
print(OUT/'comparacion_temporalidad.png')
