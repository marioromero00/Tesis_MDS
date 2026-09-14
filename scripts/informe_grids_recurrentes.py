"""Sintesis auditada de las grillas ejecutadas BiLSTM -> LSTM -> TCN."""
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import balanced_accuracy_score,f1_score
from temporales_core import ROOT,CLASSES,digest,write_json

OUT=ROOT/'resultados/grids_recurrentes_13-09-2026'
ORDER=['BiLSTM','LSTM','TCN']


def main():
    plan=json.loads((OUT/'plan.json').read_text()); assert plan['order']==ORDER
    for n,h in plan['sources'].items(): assert digest(ROOT/'scripts'/n)==h
    events=[json.loads(line) for line in (OUT/'orden_ejecucion.jsonl').read_text().splitlines()]
    for prev,nxt in zip(ORDER,ORDER[1:]):
        done=min(i for i,e in enumerate(events) if e['stage']=='finished' and e['family']==prev and e['script']=='auditar_recurrentes_grid.py' and e['exit_code']==0)
        start=min(i for i,e in enumerate(events) if e['stage']=='started' and e['family']==nxt and e['script']=='entrenar_recurrentes_grid.py')
        assert done<start
    old=pd.read_csv(ROOT/'resultados/ablacion_pca_12-09-2026/metricas_participantes.csv')
    transformer=pd.read_csv(ROOT/'resultados/transformer_grid_13-09-2026/metricas_participantes.csv')
    references={'Ridge':old.loc[old.variant.eq('reference')].set_index('participant').score.sort_index(),
        'Ridge sin fixation_count':old.loc[old.variant.eq('drop_fixation_count')].set_index('participant').score.sort_index(),
        'Transformer grid':transformer.loc[transformer.scope.eq('Transformer')].groupby('participant').score.mean().sort_index()}
    summary=[]; seed_rows=[]; contrasts=[]; diagnostics=[]; choices=[]; audits=[]
    rng=np.random.default_rng(20260914); draws=rng.integers(0,25,(2000,25))
    for family in ORDER:
        folder=OUT/family; audit=json.loads((folder/'verificacion.json').read_text())
        assert audit['auditor_sha256']==digest(ROOT/'scripts/auditar_recurrentes_grid.py'); audits.append(dict(family=family,**audit))
        p=pd.read_csv(folder/'predicciones_oof.csv.gz'); people=pd.read_csv(folder/'metricas_participantes.csv')
        protocol=json.loads((folder/'protocolo.json').read_text()); configs=pd.DataFrame(protocol['grid'])
        controls=people.loc[people.scope.eq('repeat_current')].groupby('participant').score.mean().sort_index()
        for scope in [family,'repeat_current']:
            group=people.loc[people.scope.eq(scope)]; values=group.groupby('participant').score.mean().sort_index()
            pred=p.loc[p.scope.eq(scope)]
            summary.append(dict(family=family,scope=scope,ba_macro=values.mean(),ba_global=balanced_accuracy_score(pred.true,pred.prediction),
                                macro_f1=f1_score(pred.true,pred.prediction,average='macro',zero_division=0)))
            seed_rows.extend(dict(family=family,scope=scope,seed=int(seed),ba_macro=g.score.mean()) for seed,g in group.groupby('seed'))
            for label in CLASSES:
                diagnostics.append(dict(family=family,scope=scope,label=label,recall=float(pred.loc[pred.true.eq(label)].prediction.eq(label).mean()),
                                        predicted_fraction=float(pred.prediction.eq(label).mean())))
            for name,ref in dict(references,Control_repetido=controls).items():
                assert values.index.equals(ref.index); delta=(values-ref).to_numpy(); ci=np.quantile(delta[draws].mean(axis=1),[.025,.975])
                contrasts.append(dict(family=family,scope=scope,reference=name,delta=delta.mean(),ci_low=ci[0],ci_high=ci[1],
                                      improve=int((delta>1e-12).sum()),ties=int((abs(delta)<=1e-12).sum())))
        for choice in json.loads((folder/'selecciones.json').read_text()):
            config=next(c for c in protocol['grid'] if c['id']==choice['id'])
            path=folder/'modelos'/f'fold{choice["fold"]}_{family}_20260913.joblib'
            b=joblib.load(path); count=sum(t.numel() for t in b['state'].values())
            choices.append(dict(**config,**{k:v for k,v in choice.items() if k!='id'},parameters=count))
        attempts=pd.read_csv(folder/'intentos.csv')
        merged=attempts.merge(configs,on='id',validate='many_to_one')
        effects=pd.concat([merged.groupby(k,as_index=False).score.mean().rename(columns={k:'value'}).assign(parameter=k)
                           for k in ['context','hidden','layers','lr','dropout','epoch','smoothing']],ignore_index=True)
        effects.to_csv(folder/'efectos_internos_descriptivos.csv',index=False)
        ranking=attempts.groupby(['fold','id'],as_index=False).score.max().groupby('id',as_index=False).score.mean().merge(configs,on='id').sort_values('score',ascending=False)
        ranking.to_csv(folder/'ranking_interno.csv',index=False)
        heat=attempts.groupby(['id','epoch']).score.mean().unstack().reindex(configs.id)
        fig,ax=plt.subplots(figsize=(7,10)); im=ax.imshow(heat,aspect='auto',cmap='viridis')
        ax.set(xticks=range(4),xticklabels=[2,4,8,16],yticks=range(32),yticklabels=heat.index,
               xlabel='Época',ylabel='Configuración',title=f'{family}: BA interna media sobre folds y suavizados')
        fig.colorbar(im,ax=ax,label='BA macro'); fig.tight_layout()
        fig.savefig(folder/'grilla.png',dpi=150); fig.savefig(folder/'grilla.pdf'); plt.close(fig)
    for name,data in [('resumen',summary),('resumen_semillas',seed_rows),('contrastes',contrasts),('diagnostico_clases',diagnostics),('selecciones_ampliadas',choices)]:
        pd.DataFrame(data).to_csv(OUT/f'{name}.csv',index=False)
    write_json(OUT/'verificacion_conjunta.json',dict(order_verified=True,order=ORDER,
        audits=audits,models=sum(a['models'] for a in audits),internal_scores=sum(a['internal_scores'] for a in audits),
        outer_predictions=sum(a['outer_predictions'] for a in audits),report_script_sha256=digest(__file__)))
    report=['# Grid Search de BiLSTM, LSTM y TCN: 13-09-2026','',
        'Se completaron y auditaron las tres familias en el orden solicitado: BiLSTM, LSTM y TCN. '
        'Cada familia se evaluó con 32 configuraciones, cinco folds y dos semillas externas. '
        'Se conservan todos los intentos; cada familia tiene su propio contraste frente a referencias fijas.', '',
        '## Resultados externos','', '| Familia | BA macro por persona | BA global | Macro-F1 agrupada | BA del control repetido |',
        '|---|---:|---:|---:|---:|']
    for family in ORDER:
        r=next(r for r in summary if r['scope']==family); control=next(r for r in summary if r['family']==family and r['scope']=='repeat_current')
        report.append(f'| {family} | {r["ba_macro"]:.6f} | {r["ba_global"]:.6f} | {r["macro_f1"]:.6f} | {control["ba_macro"]:.6f} |')
    report += ['',f'Referencias: Ridge {references["Ridge"].mean():.6f}, Transformer grid {references["Transformer grid"].mean():.6f}, '
        f'Ridge sin fixation_count {references["Ridge sin fixation_count"].mean():.6f}. Este último es un máximo exploratorio de una ablación previa.', '',
        'BA macro se calcula por persona y semilla y después se promedia. BA global y macro-F1 de la tabla '
        'agrupan las predicciones de ambas semillas: no son un ensamble ni 50 personas independientes.', '',
        '| Familia | Referencia | Ganancia BA (pp) | IC descriptivo 95 % (pp) | Personas que mejoran |','|---|---|---:|---:|---:|']
    for r in contrasts:
        if r['scope']==r['family']:
            report.append(f'| {r["family"]} | {r["reference"]} | {100*r["delta"]:+.3f} | [{100*r["ci_low"]:+.3f}; {100*r["ci_high"]:+.3f}] | {r["improve"]}/25 |')
    reached=[r['family'] for r in summary if r['scope']==r['family'] and r['ba_macro']>.5]
    report += ['', 'Meta BA macro 0,50: '+('alcanzada de forma exploratoria por '+', '.join(reached) if reached else 'no alcanzada por ninguna familia')+'.',
        '', '## Grillas y selección','',
        'Producto cartesiano por familia: contexto 8/32 ventanas, hidden size 16/32, profundidad 1/2, '
        'learning rate 0,0003/0,001 y dropout 0,1/0,4. En LSTM/BiLSTM profundidad es número de capas recurrentes. '
        'En TCN profundidad 1 significa dos bloques con dilataciones 1/2; profundidad 2, cuatro bloques con 1/2/4/8. '
        'Cada bloque tiene dos convoluciones de kernel 3: campo receptivo de 13 o 61 pasos, limitado por la historia disponible.', '',
        'Épocas candidatas 2/4/8/16 y suavizado causal 1/8/32: 384 decisiones por fold, 1.920 por familia, '
        '5.760 en total. Fijos: AdamW, weight decay 0,01, batch 256 y clip de gradiente 1. '
        'Dropout en la cabeza de todas las redes, entre capas recurrentes cuando hay dos, y dentro de cada bloque TCN. '
        'Igual hidden size no implica igual cantidad de parámetros entre familias; se registra el número para cada selección.', '',
        '| Familia | Fold | ID | Contexto | Hidden | Profundidad | LR | Dropout | Época | Suavizado | Parámetros | BA interna |',
        '|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for c in choices:
        report.append(f'| {c["family"]} | {c["fold"]} | {c["id"]} | {c["context"]} | {c["hidden"]} | {c["layers"]} | {c["lr"]} | {c["dropout"]} | {c["epoch"]} | {c["smoothing"]} | {c["parameters"]} | {c["score"]:.6f} |')
    report += ['', '## Semillas y clase media','', '| Familia | Modo | Semilla | BA macro |','|---|---|---:|---:|']
    for r in seed_rows: report.append(f'| {r["family"]} | {r["scope"]} | {r["seed"]} | {r["ba_macro"]:.6f} |')
    report += ['', '| Familia | Modo | Clase | Recall | Fracción predicha |','|---|---|---|---:|---:|']
    for r in diagnostics: report.append(f'| {r["family"]} | {r["scope"]} | {r["label"]} | {r["recall"]:.4f} | {r["predicted_fraction"]:.4f} |')
    report += ['', '## Diseño y auditoría','',
        'Activación, etiqueta arousal_label_6s fija, mismas 24 variables de EEG/pupila/mirada y 25 personas '
        '(13.524 ventanas) de train. GSR sigue siendo exclusivo del Modelo Profesor. Atención no se reentrenó. '
        'Mismos cinco folds externos 20/5. Cada fold selecciona con una división interna fija 16/4; '
        'desempate por ID, época y suavizado. Se congelan las cinco elecciones de cada familia antes de su '
        'evaluación externa. Las grillas de las tres familias quedaron definidas antes del primer entrenamiento.', '',
        'Una semilla interna (20260913), dos externas (20260913/20260914). Las dos externas miden variación '
        'del reajuste, no estabilidad de la búsqueda. El control repite la ventana actual en todas las posiciones '
        'reales, se entrena desde cero con la configuración/época/semilla elegidas y conserva el mismo suavizado '
        'de salida. No tiene búsqueda propia; mide aporte de la secuencia de entrada, no de toda temporalidad.', '',
        'BiLSTM recorre en ambos sentidos solamente el bloque pasado que termina en la ventana predicha. '
        'Se concatenan los estados finales forward/reverse de la última capa; las secuencias empaquetadas excluyen padding. '
        'Esto no utiliza ventanas posteriores al endpoint, pero requiere recomputar el bloque pasado y no equivale a '
        'un estado recurrente incremental. LSTM usa el estado final de su última capa; TCN aplica padding izquierdo causal. '
        'Fuente: [PyTorch LSTM 2.14](https://docs.pytorch.org/docs/2.14/generated/torch.nn.modules.rnn.LSTM.html).', '',
        'Preprocesadores ajustados solo con fit. Historial reiniciado por participante, grabación o salto distinto de un segundo; '
        'puede cruzar estímulos. Hasta 64 segundos de soporte combinado de contexto y suavizado. La normalización '
        'original de señales sigue siendo offline: no se valida el pipeline completo en tiempo real.', '',
        '480 entrenamientos internos, 1.920 checkpoints y 60 modelos externos: 1.980 modelos guardados y recargados. '
        'Se recalcularon los 5.760 scores internos, el preprocesado, las elecciones y 162.288 predicciones externas, '
        'además de métricas por fold/persona. Tolerancia 1e-7 para float32/CSV y clases idénticas. '
        'Se verificaron hashes de fuentes/datos/modelos y el orden efectivo en orden_ejecucion.jsonl. '
        'Las 66 pruebas del proyecto pasaron en 14,740 segundos, incluidas exclusión de futuro/padding y preservación del RNG.', '',
        'Validation/test originales no se reevaluaron. IC descriptivos de 2.000 remuestreos pareados de las 25 personas, '
        'promediando semillas antes del bootstrap. Sin corrección por búsqueda múltiple ni dependencia entre folds. '
        'Usar repetidamente train mantiene el estudio exploratorio, sin confirmación independiente. Un único split '
        'interno de cuatro personas puede seleccionar configuraciones inestables. Los scores internos no son desempeño externo.', '',
        'La métrica principal promedia recalls de clases presentes en cada persona. Dos personas carecen de una clase; '
        'constantes bajo/alto alcanzan 0,346667, medio 0,306667. El ranking interno maximiza época/suavizado dentro '
        'de cada fold y configuración; los efectos descriptivos promedian todas las épocas/suavizados. '
        'Ninguno redefine el ganador externo ni prueba importancia causal de un hiperparámetro.', '',
        'Artefactos por familia: protocolo, intentos, selecciones, curvas, checkpoints, modelos, predicciones y auditoría. '
        'Carga: joblib.load y recurrentes_grid_core.predict(bundle, frame); la familia se conserva en el bundle. '
        'Reanudar: python scripts/ejecutar_grids_recurrentes.py. Las tareas terminadas se conservan y se comprueban las fuentes.']
    (ROOT/'documentacion/Grid_BiLSTM_LSTM_TCN_13-09-2026.md').write_text('\n'.join(report)+'\n',encoding='utf-8',newline='\n')
    fig,ax=plt.subplots(figsize=(8,4.5)); vals=[next(r['ba_macro'] for r in summary if r['scope']==f) for f in ORDER]
    ax.barh(ORDER,vals,color='#287a8c'); ax.axvline(references['Ridge'].mean(),color='#d38a23',label='Ridge previo')
    ax.axvline(.5,color='#a33c3c',linestyle='--',label='Meta 0,50')
    ax.set(xlim=(0,max(.55,max(vals)+.04)),xlabel='BA promedio por persona y semilla',title='Grillas temporales: evaluación exploratoria en train')
    ax.invert_yaxis(); ax.legend()
    fig.tight_layout(); fig.savefig(OUT/'comparacion.png',dpi=160); fig.savefig(OUT/'comparacion.pdf'); plt.close(fig)
    print(pd.DataFrame(summary).to_string(index=False))


if __name__=='__main__': main()
