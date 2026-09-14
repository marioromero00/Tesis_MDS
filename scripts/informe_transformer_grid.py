"""Informe de grilla, variacion entre semillas y contrastes por persona."""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import balanced_accuracy_score,f1_score
from entrenar_transformer_grid import OUT
from temporales_core import ROOT,CLASSES


def main():
    protocol=json.loads((OUT/'protocolo.json').read_text()); audit=json.loads((OUT/'verificacion.json').read_text())
    people=pd.read_csv(OUT/'metricas_participantes.csv'); pred=pd.read_csv(OUT/'predicciones_oof.csv.gz')
    prior=pd.read_csv(ROOT/'resultados/redes_13-09-2026/metricas_participantes.csv')
    ablation=pd.read_csv(ROOT/'resultados/ablacion_pca_12-09-2026/metricas_participantes.csv')
    refs={'Transformer previo':prior.loc[prior.scope.eq('Transformer')].set_index('participant').score.sort_index(),
          'Ridge':ablation.loc[ablation.variant.eq('reference')].set_index('participant').score.sort_index(),
          'Ridge sin fixation_count':ablation.loc[ablation.variant.eq('drop_fixation_count')].set_index('participant').score.sort_index(),
          'Control repetido':people.loc[people.scope.eq('repeat_current')].groupby('participant').score.mean().sort_index()}
    rows=[]; contrasts=[]; diagnostics=[]
    rng=np.random.default_rng(20260914); draws=rng.integers(0,25,(2000,25))
    for scope,g in people.groupby('scope'):
        vals=g.groupby('participant').score.mean().sort_index(); p=pred.loc[pred.scope.eq(scope)]
        rows.append(dict(scope=scope,ba_macro=vals.mean(),ba_global=balanced_accuracy_score(p.true,p.prediction),
                         macro_f1=f1_score(p.true,p.prediction,average='macro',zero_division=0)))
        for label in CLASSES:
            diagnostics.append(dict(scope=scope,label=label,recall=float(p.loc[p.true.eq(label)].prediction.eq(label).mean()),
                                    predicted_fraction=float(p.prediction.eq(label).mean())))
        for name,ref in refs.items():
            assert vals.index.equals(ref.index); delta=(vals-ref).to_numpy()
            ci=np.quantile(delta[draws].mean(axis=1),[.025,.975])
            contrasts.append(dict(scope=scope,reference=name,delta=delta.mean(),ci_low=ci[0],ci_high=ci[1],
                                  improve=int((delta>1e-12).sum()),ties=int((abs(delta)<=1e-12).sum())))
    summary=pd.DataFrame(rows); comparisons=pd.DataFrame(contrasts); diag=pd.DataFrame(diagnostics)
    seeds=people.groupby(['scope','seed'],as_index=False).score.mean()
    summary.to_csv(OUT/'resumen.csv',index=False); comparisons.to_csv(OUT/'contrastes.csv',index=False)
    diag.to_csv(OUT/'diagnostico_clases.csv',index=False); seeds.to_csv(OUT/'resumen_semillas.csv',index=False)
    attempts=pd.read_csv(OUT/'intentos.csv'); configs=pd.DataFrame(protocol['grid'])
    # Marginal descriptive scores average ALL epochs and smoothing levels.
    merged=attempts.merge(configs,on='id',validate='many_to_one')
    marginal=pd.concat([merged.groupby(k,as_index=False).score.mean().rename(columns={k:'value'}).assign(parameter=k)
                        for k in ['context','hidden','layers','lr','dropout','epoch','smoothing']],ignore_index=True)
    marginal.to_csv(OUT/'efectos_internos_descriptivos.csv',index=False)
    ranking=attempts.groupby(['fold','id'],as_index=False).score.max().groupby('id',as_index=False).score.mean().merge(configs,on='id').sort_values('score',ascending=False)
    ranking.to_csv(OUT/'ranking_interno.csv',index=False)
    selected=json.loads((OUT/'selecciones.json').read_text())
    mainrow=summary.loc[summary.scope.eq('Transformer')].iloc[0]
    report=['# Grid Search de Transformer: 13-09-2026','',
        f'El Transformer seleccionado dentro de cada fold obtiene BA macro por persona {mainrow.ba_macro:.6f}, '
        f'promediando dos semillas. La ronda anterior obtuvo {refs["Transformer previo"].mean():.6f}; '
        f'Ridge, {refs["Ridge"].mean():.6f}. La meta 0,50 '
        f'{"se alcanza solo de forma exploratoria" if mainrow.ba_macro>.5 else "no se alcanza"}.','',
        '## Grilla ejecutada','',
        'Producto cartesiano completo de cinco ejes binarios: 32 configuraciones de arquitectura y optimización. '
        'Cada configuración se entrena una vez por fold hasta 16 épocas y se guardan cuatro checkpoints. '
        'Evaluar checkpoints y suavizado produce 384 decisiones candidatas por fold y 1.920 en total.', '',
        '| Parámetro | Valores |','|---|---|',
        '| Contexto | 8, 32 ventanas |','| Ancho d_model | 16, 32 |','| Capas | 1, 2 |',
        '| Learning rate | 0,0003; 0,001 |','| Dropout | 0,1; 0,4 |',
        '| Épocas candidatas | 2, 4, 8, 16 |','| Suavizado causal de salida | 1, 8, 32 ventanas |','',
        'Fijos: cuatro cabezas, feedforward de dos veces d_model, AdamW con weight decay 0,01, '
        'batch 256, clip de gradiente 1, posiciones aprendidas, pre-norm y pérdida ponderada '
        'por persona/clase observada. No se buscaron cabezas, batch o weight decay en esta grilla.', '',
        '## Evaluación externa','', '| Modelo | BA macro por persona | BA global | Macro-F1 agrupada |','|---|---:|---:|---:|']
    for r in rows: report.append(f'| {r["scope"]} | {r["ba_macro"]:.6f} | {r["ba_global"]:.6f} | {r["macro_f1"]:.6f} |')
    report += ['', 'BA macro se calcula primero por persona y semilla y luego se promedia. '
        'BA global y macro-F1 de la tabla agrupan las predicciones de ambas semillas; '
        'no representan un ensamble ni 50 participantes independientes.', '',
        '| Referencia | Ganancia Transformer (pp) | IC descriptivo 95 % (pp) | Personas que mejoran |','|---|---:|---:|---:|']
    for r in contrasts:
        if r['scope']=='Transformer': report.append(f'| {r["reference"]} | {100*r["delta"]:+.3f} | [{100*r["ci_low"]:+.3f}; {100*r["ci_high"]:+.3f}] | {r["improve"]}/25 |')
    report += ['', '| Modelo | Semilla | BA macro |','|---|---:|---:|']
    for r in seeds.to_dict('records'): report.append(f'| {r["scope"]} | {r["seed"]} | {r["score"]:.6f} |')
    report += ['', 'El control se reajusta con la ventana actual repetida en todas las posiciones reales, '
        'con la misma configuración, época, suavizado y semilla seleccionados. Conserva suavizado de salida; '
        'el contraste mide el aporte de la secuencia de entrada y no el de toda temporalidad. '
        'El control no tiene selección interna propia.', '',
        '## Configuraciones elegidas','', '| Fold | ID | Contexto | Ancho | Capas | LR | Dropout | Época | Suavizado | BA interna |',
        '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for c in selected:
        g=next(g for g in protocol['grid'] if g['id']==c['id'])
        report.append(f'| {c["fold"]} | {c["id"]} | {g["context"]} | {g["hidden"]} | {g["layers"]} | {g["lr"]} | {g["dropout"]} | {c["epoch"]} | {c["smoothing"]} | {c["score"]:.6f} |')
    report += ['', '## Clases y estabilidad','', '| Modelo | Clase | Recall | Fracción predicha |','|---|---|---:|---:|']
    for r in diagnostics: report.append(f'| {r["scope"]} | {r["label"]} | {r["recall"]:.4f} | {r["predicted_fraction"]:.4f} |')
    report += ['', '## Protocolo, auditoría y límites','',
        'Mismas 25 personas y 13.524 ventanas de train; etiqueta arousal_label_6s fija y 24 variables de '
        'EEG, pupila y mirada. GSR sigue siendo exclusivo del Modelo Profesor. Atención no se reentrenó. '
        'Cinco folds externos 20/5; cada uno contiene un split interno fijo 16/4. '
        'Se eligió por BA media de las clases observadas de cada persona, con desempate ID, época y suavizado. '
        'Todas las elecciones quedaron congeladas antes de evaluar fuera del fit. Validation/test no se reevaluaron.', '',
        '160 entrenamientos internos, 640 checkpoints, 20 modelos externos (cinco folds por dos semillas '
        'por dos modos) y 54.096 predicciones externas. La búsqueda interna usa una semilla; '
        'las dos externas miden variación del reajuste, no estabilidad de la búsqueda. '
        'Un único split interno de cuatro personas puede producir selección inestable. '
        'Un score interno alto no equivale a desempeño en personas nuevas.', '',
        'Preprocesadores ajustados solo con fit. Capas inicializadas independientemente. '
        'Predicción y callbacks conservan el RNG: una prueba confirma que checkpoints no cambian pesos finales. '
        'La nueva implementación cambia este detalle respecto a la ronda previa, que consumía RNG al crear '
        'una red para predecir dentro del callback. Se conserva aquella ejecución sin modificar; '
        'la comparación entre rondas no aísla exclusivamente el tamaño de grilla.', '',
        'Máscaras causales y de padding; historial reiniciado por participante, grabación o salto distinto de un segundo. '
        'Se puede cruzar estímulos. Contexto y suavizado máximos abarcan 64 segundos de señal. '
        'La normalización original sigue siendo offline; esto no valida un sistema completo en tiempo real.', '',
        f'Auditoría: {audit["models"]} modelos recargados, preprocesado reajustado, {audit["internal_scores"]} '
        f'scores internos y {audit["outer_predictions"]} predicciones externas recalculadas. '
        f'Error máximo {audit["max_prediction_error"]:.3g}, tolerancia 1e-7 float32/CSV, clases idénticas. '
        'Se verifican hashes de fuentes, datos, modelos, splits y elecciones; predicción sin profesor o etiquetas. '
        'Las 64 pruebas del proyecto pasaron en 16,737 segundos; registro completo en pruebas.json.', '',
        'IC de 2.000 remuestreos pareados de las 25 personas después de promediar semillas. '
        'Son descriptivos: no corrigen selección múltiple ni dependencia entre folds. '
        'La repetición adaptativa de experimentos sobre train impide interpretar el resultado como confirmación independiente. '
        'Ridge sin fixation_count es un máximo exploratorio anterior. Constantes bajo/alto obtienen '
        '0,346667 en BA macro, medio 0,306667, porque dos personas carecen de alguna clase.', '',
        'El ranking interno toma el máximo sobre épocas/suavizados por configuración y fold; '
        'resume la búsqueda y no elige un nuevo ganador externo. Los efectos marginales promedian '
        'todas las épocas y suavizados y no prueban importancia causal de un hiperparámetro.', '',
        'Fuentes: [PyTorch TransformerEncoderLayer](https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html), '
        'protocolo.json, intentos.csv, selecciones.json, verificacion.json y pruebas.json. '
        'Carga: joblib.load y transformer_grid_core.predict(bundle, frame). '
        'Reanudación: entrenar_transformer_grid.py --resume comprueba las fuentes y reutiliza tareas terminadas.']
    (ROOT/'documentacion/Grid_Transformer_13-09-2026.md').write_text('\n'.join(report)+'\n',encoding='utf-8',newline='\n')
    heat=attempts.groupby(['id','epoch']).score.mean().unstack().reindex(configs.id)
    fig,ax=plt.subplots(figsize=(7,10)); im=ax.imshow(heat,aspect='auto',cmap='viridis')
    ax.set(xticks=range(4),xticklabels=[2,4,8,16],yticks=range(32),yticklabels=heat.index,
           xlabel='Época',ylabel='Configuración',title='BA interna media sobre folds y suavizados')
    fig.colorbar(im,ax=ax,label='BA macro'); fig.tight_layout()
    fig.savefig(OUT/'grilla.png',dpi=150); fig.savefig(OUT/'grilla.pdf'); plt.close(fig)
    print(summary.to_string(index=False)); print(seeds.to_string(index=False))


if __name__=='__main__': main()
