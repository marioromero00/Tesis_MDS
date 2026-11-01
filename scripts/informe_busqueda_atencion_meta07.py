"""Consolida exclusivamente metricas completas y auditadas; conserva estados parciales."""
import json
from pathlib import Path
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'resultados/grid_atencion_meta07_29-10-2026'

def main():
    runs=[('Boosting, grid 32',BASE/'ronda1'),('CatBoost, grid 32',BASE/'ronda2'),('Ensamble de grids',BASE/'ensamble_rondas12'),('Multiescala, grid 48',BASE/'ronda3'),('EEG/GSR ampliados',BASE/'caracteristicas_ampliadas/ronda1'),('Retrospectivo: usa ventanas posteriores',BASE/'retrospectivo/ronda1'),('Destilación de score docente',BASE/'destilacion/ronda1'),('Ranking por persona',BASE/'ranking/ronda1'),('Ensamble ampliado',BASE/'ensamble_ampliado')]
    rows=[];states=[]
    for name,out in runs:
        state=dict(name=name,path=str(out.relative_to(BASE)),internal_trials_completed=len(list((out/'trials').glob('*.json'))),outer_models_saved=len(list((out/'modelos').glob('*.joblib'))),complete=(out/'metricas.csv').exists(),audited=(out/'auditoria_independiente.json').exists())
        states.append(state)
        if state['complete'] and state['audited']:
            audit=json.loads((out/'auditoria_independiente.json').read_text())
            assert audit['passed']
            m=pd.read_csv(out/'metricas.csv');m.insert(0,'run',name);m.insert(1,'run_path',str(out.relative_to(BASE)));rows.append(m)
    allm=pd.concat(rows,ignore_index=True);allm.to_csv(BASE/'comparacion_rondas_auditadas.csv',index=False)
    result=dict(target=.7,metric='macro participant ROC-AUC; 25 people OOF',target_exceeded=bool(allm.auc_macro.gt(.7).any()),
        runs=states,total_unique_inner_fits=sum(r['internal_trials_completed'] for r in states),total_outer_models_saved=sum(r['outer_models_saved'] for r in states),best_audited=allm.loc[allm.auc_macro.idxmax()].to_dict())
    (BASE/'estado_busqueda.json').write_text(json.dumps(result,indent=2))
    names=dict(inductivo='Sin calibración adicional',relativo_offline='Z personal offline',rangos_offline='Rangos personales offline',seleccion_interna='Selección interna')
    lines=['# Grid e iteraciones de atención binaria — 29-10-2026','',
        'Meta solicitada: ROC-AUC promedio por persona mayor que 0,70. Solo se considera alcanzada con las predicciones OOF completas y auditadas de las 25 personas; no con una métrica interna, un participante favorable, el conjunto de entrenamiento ni un cambio de etiqueta.','',
        '**Estado de la meta: '+('superada en al menos un escenario auditado.**' if result['target_exceeded'] else 'todavía no alcanzada.**'),'',
        '| Corrida | Escenario | ROC-AUC | IC descriptivo 95 % | Δ frente a 0,6464 |','|---|---|---:|---:|---:|']
    for _,r in allm.iterrows():lines.append(f"| {r.run} | {names[r.strategy]} | {r.auc_macro:.4f} | [{r.ci_low:.4f}; {r.ci_high:.4f}] | {r.delta_previous:+.4f} |")
    lines+=['','Las variantes de normalización y rangos personales requieren toda la sesión no etiquetada y se reportan como adaptación transductiva offline. El historial de variables es causal, pero esa calibración no lo es. El profesor también conserva su definición relativa offline. Ninguno de estos escenarios valida por sí mismo la atención psicológica ni la generalización futura.','',
        'El contraste retrospectivo usa ventanas posteriores explícitamente. Sus resultados se presentan por separado: no constituyen una mejora de detección causal en tiempo real. Se conservan las etiquetas del profesor PCA y los mismos cinco folds de personas. Los parámetros y los pesos de mezcla se eligen con cuatro personas internas, usando 16 para ajuste; luego se reajusta en 20 y evalúa en cinco personas externas por fold. Test/validation/P29 sin evaluar. Los intervalos remuestrean personas, no ventanas. Son descriptivos y no corrigen búsqueda reiterada ni la parada al alcanzar una meta.','',
        '## Estado de las corridas','']
    for state in states:
        status='completa y auditada' if state['complete'] and state['audited'] else 'parcial, sin resultado global auditado'
        lines.append(f"- {state['name']}: {status}; {state['internal_trials_completed']} ajustes internos guardados, {state['outer_models_saved']} modelos externos. [Carpeta]({state['path']}/).")
    lines+=['','Los registros parciales se conservan; no se presentan como una evaluación completa. La ronda 1 tuvo una interrupción al guardar metadatos de selección, corregida sin cambiar datos, modelos o grid; protocolo original y corrección quedan registrados.','',
        '## Fuentes y reproducción','','- [Grid original](../../scripts/grid_atencion_meta07.py)','- [Ensamble](../../scripts/ensamblar_grid_atencion_meta07.py)','- [Grid con características ampliadas](../../scripts/grid_atencion_caracteristicas_ampliadas.py)','- [Comparación CSV](comparacion_rondas_auditadas.csv)','- [Estado estructurado](estado_busqueda.json)','',
        '![Comparación AUC](comparacion_auc_rondas.png)']
    (BASE/'INFORME.md').write_text('\n'.join(lines))
    order=allm.sort_values(['auc_macro']);fig,ax=plt.subplots(figsize=(10,max(6,len(order)*.35)),layout='constrained')
    yy=np.arange(len(order));ax.errorbar(order.auc_macro,yy,xerr=np.vstack([order.auc_macro-order.ci_low,order.ci_high-order.auc_macro]),fmt='o',capsize=3,color='#1874b4')
    ax.set(yticks=yy,yticklabels=[f'{r.run} · {names[r.strategy]}' for _,r in order.iterrows()],xlabel='ROC-AUC macro por participante · IC descriptivo 95 %',title='Grids e iteraciones auditados',xlim=(.5,.75))
    ax.axvline(.7,c='#bb3b3b',ls='--',label='Meta 0,70');ax.axvline(.6464076199019761,c='#777777',ls=':',label='Referencia anterior 0,6464');ax.grid(axis='x',alpha=.15);ax.legend(loc='lower right',fontsize=8)
    for ext in ['png','pdf']:fig.savefig(BASE/f'comparacion_auc_rondas.{ext}',dpi=180)
    plt.close(fig)
    nonretro=allm[~allm.run_path.str.startswith('retrospectivo')]
    pure=nonretro[nonretro.strategy.eq('inductivo')]
    offline=nonretro[~nonretro.strategy.eq('inductivo')]
    retro=allm[allm.run_path.str.startswith('retrospectivo')]
    summary=[]
    for label,subset in [('Sin calibración personal adicional',pure),('Con calibración personal offline disponible',offline),('Retrospectivo: usa señales posteriores',retro)]:
        if len(subset):
            row=subset.loc[subset.auc_macro.idxmax()]
            summary.append(dict(scenario=label,run=row.run,strategy=row.strategy,auc=float(row.auc_macro),ci_low=float(row.ci_low),ci_high=float(row.ci_high)))
    pd.DataFrame(summary).to_csv(BASE/'resumen_escenarios.csv',index=False)
    fig,ax=plt.subplots(figsize=(10,4.2),layout='constrained')
    for i,r in enumerate(summary):
        ax.errorbar(r['auc'],i,xerr=[[r['auc']-r['ci_low']],[r['ci_high']-r['auc']]],fmt='o',capsize=4,color='#1874b4')
        ax.annotate(f" {r['auc']:.3f}",(r['auc'],i),xytext=(0,10),textcoords='offset points',ha='center',fontsize=10)
    ax.set(yticks=list(range(len(summary))),yticklabels=[r['scenario'] for r in summary],xlabel='ROC-AUC macro por participante · IC descriptivo 95 %',title='Máximos observados por escenario · búsqueda exploratoria',xlim=(.5,.75),ylim=(-.7,len(summary)-.3))
    ax.axvline(.7,c='#bb3b3b',ls='--',label='Meta 0,70');ax.axvline(.6464076199019761,c='#777777',ls=':',label='Referencia anterior');ax.grid(axis='x',alpha=.15);ax.legend(loc='lower left',fontsize=8)
    for ext in ['png','pdf']:fig.savefig(BASE/f'resumen_escenarios.{ext}',dpi=180)
    plt.close(fig)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
