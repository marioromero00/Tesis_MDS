"""Resultados y contrastes descriptivos pareados por participante."""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score, balanced_accuracy_score
from entrenar_redes_13 import OUT
from temporales_core import ROOT, CLASSES, write_json


def main():
    audit=json.loads((OUT/'verificacion.json').read_text())
    people=pd.read_csv(OUT/'metricas_participantes.csv')
    pred=pd.read_csv(OUT/'predicciones_oof.csv.gz')
    prior=pd.read_csv(ROOT/'resultados/ablacion_pca_12-09-2026/metricas_participantes.csv')
    reference=prior.loc[prior.variant.eq('reference')].set_index('participant').score.sort_index()
    reduced=prior.loc[prior.variant.eq('drop_fixation_count')].set_index('participant').score.sort_index()
    controls=people.loc[people.scope.eq('repeat_current')].set_index('participant').score.sort_index()
    rows=[]; contrasts=[]; diagnostics=[]
    rng=np.random.default_rng(20260913); draws=rng.integers(0,25,(2000,25))
    for scope, group in people.groupby('scope'):
        values=group.set_index('participant').score.sort_index(); p=pred.loc[pred.scope.eq(scope)]
        assert values.index.equals(reference.index)
        rows.append(dict(scope=scope,ba_macro=values.mean(),ba_global=balanced_accuracy_score(p.true,p.prediction),
                         macro_f1=f1_score(p.true,p.prediction,average='macro',zero_division=0)))
        for label in CLASSES:
            diagnostics.append(dict(scope=scope,label=label,recall=float(p.loc[p.true.eq(label)].prediction.eq(label).mean()),
                                    predicted_fraction=float(p.prediction.eq(label).mean())))
        for name,baseline in [('Ridge',reference),('Ridge_without_fixation_count',reduced),('repeat_current',controls)]:
            delta=(values-baseline).to_numpy(); interval=np.quantile(delta[draws].mean(axis=1),[.025,.975])
            contrasts.append(dict(scope=scope,reference=name,delta=delta.mean(),ci_low=interval[0],ci_high=interval[1],
                improve=int((delta>1e-12).sum()),tie=int((abs(delta)<=1e-12).sum())))
    summary=pd.DataFrame(rows); comparison=pd.DataFrame(contrasts); diagnosis=pd.DataFrame(diagnostics)
    summary.to_csv(OUT/'resumen.csv',index=False); comparison.to_csv(OUT/'contrastes.csv',index=False)
    diagnosis.to_csv(OUT/'diagnostico_clases.csv',index=False)
    selections=pd.read_json(OUT/'selecciones.json')
    internal=pd.read_csv(OUT/'intentos.csv')
    trajectory=internal.groupby(['id','epoch'],as_index=False).score.mean()
    trajectory.to_csv(OUT/'trayectoria_interna.csv',index=False)
    report=['# Transformer y TCN: 13-09-2026','',
        'Esta búsqueda no mejora el Ridge anterior: selección conjunta 0,371558, TCN 0,366822 y '
        'Transformer 0,363442 frente a Ridge 0,374750. Los intervalos de las diferencias incluyen cero. '
        'El control con ventana actual repetida obtiene 0,374911: no hay evidencia clara de aporte del historial. '
        'Recall medio de la selección conjunta: 19,62 %, frente a 23,27 % del Ridge de referencia.','',
        'Se evaluaron redes nuevas para activación, con las mismas 24 variables y arousal_label_6s. '
        'Seis configuraciones, 30 entrenamientos internos, 90 checkpoints y 270 decisiones internas '
        '(época 4/8/12 por suavizado 1/8/32). Se guardaron además 20 modelos externos.','',
        '## Resultados','', '| Modelo | BA macro por persona | BA global | Macro-F1 |', '|---|---:|---:|---:|']
    for r in rows: report.append(f'| {r["scope"]} | {r["ba_macro"]:.6f} | {r["ba_global"]:.6f} | {r["macro_f1"]:.6f} |')
    report += ['',f'Referencia Ridge anterior: {reference.mean():.6f}. Ridge sin fixation_count: {reduced.mean():.6f}; '
        'este último es un máximo exploratorio de la ablación previa, no una referencia confirmatoria.',
        '', '| Contraste frente a Ridge | Ganancia (pp) | IC descriptivo 95 % (pp) | Personas que mejoran |',
        '|---|---:|---:|---:|']
    for r in contrasts:
        if r['reference']=='Ridge': report.append(f'| {r["scope"]} | {100*r["delta"]:+.3f} | [{100*r["ci_low"]:+.3f}; {100*r["ci_high"]:+.3f}] | {r["improve"]}/25 |')
    temporal=next(r for r in contrasts if r['scope']=='all' and r['reference']=='repeat_current')
    report += ['',f'Historial frente al control de ventana actual repetida: {100*temporal["delta"]:+.3f} pp, '
        f'IC [{100*temporal["ci_low"]:+.3f}; {100*temporal["ci_high"]:+.3f}]. '
        'El control se reajusta desde cero con la arquitectura, época y suavizado elegidos para all; '
        'no tiene una búsqueda propia. Ambos pueden aprovechar historial mediante suavizado de salida.',
        '', '## Iteraciones y selección','',
        'Cada arquitectura se probó con (contexto, ancho, dropout, learning rate, weight decay): '
        '(8,16,0.2,0.001,0.01), (32,16,0.3,0.0005,0.01) y (32,32,0.4,0.001,0.1). '
        'Estas variantes cambian varios hiperparámetros a la vez; no identifican efectos aislados. '
        'Las épocas y el suavizado se eligen dentro del fold. No se siguió entrenando en respuesta a métricas externas.',
        '', '| Fold | Selección | Configuración | Época | Suavizado | BA interna |', '|---|---|---|---:|---:|---:|']
    for c in selections.to_dict('records'):
        report.append(f'| {c["fold"]} | {c["scope"]} | {c["id"]} | {c["epoch"]} | {c["smoothing"]} | {c["score"]:.6f} |')
    report += ['', 'Promedio descriptivo interno sobre cinco folds y tres suavizados, por configuración y época. '
        'Resume lo probado; no se usa para volver a elegir un ganador externo.', '',
        '| Configuración | Época 4 | Época 8 | Época 12 |', '|---|---:|---:|---:|']
    for name,g in trajectory.groupby('id'):
        v=g.set_index('epoch').score
        report.append(f'| {name} | {v[4]:.4f} | {v[8]:.4f} | {v[12]:.4f} |')
    report += ['', '## Diagnóstico por clase','', '| Modelo | Clase | Recall | Fracción predicha |', '|---|---|---:|---:|']
    for r in diagnostics: report.append(f'| {r["scope"]} | {r["label"]} | {r["recall"]:.4f} | {r["predicted_fraction"]:.4f} |')
    report += ['', '## Alcance y auditoría','',
        'Cinco folds externos de 20/5 personas; selección en una división interna fija 16/4 de cada fold. '
        'Se conservan las 25 personas de train y sus 13.524 ventanas. Validation y test originales no se reevaluaron. '
        'Una semilla (20260913): los intervalos no incorporan variación entre semillas. '
        'El único split interno puede dar una selección inestable.', '',
        'Imputación con mediana e indicadores de ausencia y escalado ajustados únicamente con personas de fit. '
        'Pérdida ponderada para dar igual peso a cada persona y a sus clases observadas. '
        'BA macro promedia el recall de clases presentes en cada persona; dos personas no tienen las tres clases. '
        'Los controles constantes bajo/alto alcanzan 0,346667 en esta métrica; medio, 0,306667.', '',
        'TCN usa cuatro bloques residuales, dilataciones 1/2/4/8, dos convoluciones de kernel 3 por bloque. '
        'Transformer usa una capa, cuatro cabezas, posiciones aprendidas y máscaras causales y de padding. '
        'Solo se entrega historia hasta la ventana evaluada, reiniciando por persona, grabación o salto distinto de un segundo. '
        'Se permite cruzar límites de estímulo. El contexto máximo de 32 ventanas abarca 33 segundos de señal; '
        'con suavizado de 32 puede abarcar 64 segundos. La normalización original de señales sigue siendo offline.', '',
        'Fuente de implementación: [PyTorch TransformerEncoder](https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoder). '
        'GSR y etiquetas no son entradas del estudiante. La auditoría predice con señales y metadatos únicamente.', '',
        f'Auditoría: {audit["models"]} modelos recargados, preprocesadores reajustados, '
        f'{audit["internal_scores"]} decisiones internas recalculadas y {audit["outer_predictions"]} predicciones externas verificadas. '
        f'Error máximo de scores {audit["max_prediction_error"]:.3g}; tolerancia 1e-7 para float32/CSV, clases idénticas. '
        'Hashes de fuentes, particiones y modelos comprobados; selección reconstruida antes de interpretar resultados. '
        'Las 61 pruebas del proyecto pasaron en 11,760 segundos, incluidas las nuevas pruebas de causalidad, '
        'padding, reinicios y control repetido. Registro en pruebas.json.', '',
        'Intervalos de 2.000 remuestreos pareados de personas, descriptivos, sin corrección por selección múltiple '
        'ni dependencia entre folds. Reutilizar train en muchas rondas hace esta comparación exploratoria. '
        'Los resultados no prueban importancia fisiológica ni superioridad confirmada.', '',
        f'Meta BA macro 0,50: {"alcanzada de forma exploratoria" if summary.ba_macro.max()>.5 else "no alcanzada"}.', '',
        'Artefactos: protocolo.json, intentos.csv, selecciones.json, curvas/, internos/, modelos/, '
        'predicciones_internas/, predicciones_oof.csv.gz, contrastes.csv y verificacion.json. '
        'Carga: joblib.load del bundle y redes_secuencia_13.predict(bundle, frame).']
    path=ROOT/'documentacion/Transformer_TCN_13-09-2026.md'
    path.write_text('\n'.join(report)+'\n',encoding='utf-8',newline='\n')
    fig,ax=plt.subplots(figsize=(8,4.5)); ax.barh(summary.scope,summary.ba_macro,color='#287a8c')
    ax.axvline(reference.mean(),color='#dd9630',label=f'Ridge {reference.mean():.4f}')
    ax.axvline(.5,color='#a33c3c',linestyle='--',label='Meta 0,50')
    ax.set(xlim=(0,.55),xlabel='Balanced accuracy promedio por participante',title='Transformer y TCN: evaluación exploratoria en train')
    ax.legend(); fig.tight_layout(); fig.savefig(OUT/'comparacion.png',dpi=160); fig.savefig(OUT/'comparacion.pdf'); plt.close(fig)
    print(summary.to_string(index=False))


if __name__=='__main__': main()
