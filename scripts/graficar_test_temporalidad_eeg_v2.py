"""Gráfico de AUC y diferencias temporales pareadas en test."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd,numpy as np
from evaluar_test_temporalidad_eeg_v2 import OUT
m=pd.read_csv(OUT/'metricas.csv').set_index('strategy');c=pd.read_csv(OUT/'contrastes.csv')
fig,(ax,bx)=plt.subplots(1,2,figsize=(13,5),layout='constrained',gridspec_kw={'width_ratios':[1,1.35]})
for scope,label,color in [('inductivo','Inductivo','#176a9c'),('relativo_offline','Offline','#b46518')]:
    keys=[f'{scope}_ctx{i}' for i in [1,8,32]];y=m.loc[keys].auc_macro.to_numpy()
    ax.plot([0,1,2],y,'o-',lw=2,color=color,label=label)
    for i,v in enumerate(y):ax.annotate(f'{v:.4f}',(i,v),xytext=(0,8 if scope=='relativo_offline' else -17),textcoords='offset points',ha='center',color=color)
ax.set_xticks([0,1,2],['Actual\n2 s','Historial\nhasta 9 s','Historial\nhasta 33 s']);ax.set_ylim(.65,.72);ax.set_ylabel('ROC-AUC promedio por persona');ax.set_title('Comparación con estáticos seleccionados');ax.grid(axis='y',alpha=.2);ax.legend(loc='upper left')
keep=c[~c.baseline.str.endswith('_ctx8')].copy();labels=[]
for r in keep.itertuples():
    scope='Inductivo' if r.temporal.startswith('inductivo') else 'Offline';context='33 s' if r.temporal.endswith('32') else '9 s';base='estático pareado' if 'pareado' in r.baseline else 'estático seleccionado'
    labels.append(f'{scope}: {context} − {base}')
for i,r in enumerate(keep.itertuples()):
    color='#176a9c' if r.temporal.startswith('inductivo') else '#b46518'
    bx.errorbar(r.delta_auc,i,xerr=[[r.delta_auc-r.ci_low],[r.ci_high-r.delta_auc]],fmt='o',capsize=4,color=color)
bx.axvline(0,color='#333333',ls='--');bx.set_yticks(range(len(labels)),labels,fontsize=9);bx.invert_yaxis();bx.set_xlabel('Diferencia de AUC · IC pareado descriptivo 95 %');bx.set_title('Todos los intervalos incluyen cero');bx.grid(axis='x',alpha=.2)
fig.suptitle('Test: indicios favorables al historial, evidencia todavía inconclusa',fontsize=14)
fig.savefig(OUT/'comparacion_test.png',dpi=180)
print(OUT/'comparacion_test.png')
