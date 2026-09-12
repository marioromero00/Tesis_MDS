"""Resumen de todas las busquedas, sin ocultar contrastes principales negativos."""
import json
from datetime import datetime,timezone
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from temporales_core import ROOT,digest,write_json
from informe_control_historial import bootstrap,markdown

ROUNDS=[('Persistencia','persistencia_11-09-2026','Busqueda_persistencia_11-09-2026.md'),
        ('Multiescala','multiescala_11-09-2026_completa','Busqueda_multiescala_11-09-2026.md'),
        ('Adaptación offline','adaptacion_offline_11-09-2026','Busqueda_adaptacion_11-09-2026.md'),
        ('Regresión ordinal','regresion_ordinal_12-09-2026_completa','Regresion_Ordinal_12-09-2026.md')]
OUT=ROOT/'resultados/meta_05_12-09-2026'


def read(p): return json.loads(p.read_text(encoding='utf-8'))


def main():
    OUT.mkdir(exist_ok=False); rows=[]; total_models=total_predictions=total_scores=0; hashes={}
    for title,dirname,report in ROUNDS:
        directory=ROOT/'resultados'/dirname; verification=read(directory/'verificacion.json')
        script='auditar_regresion_ordinal.py' if title=='Regresión ordinal' else 'auditar_busquedas_05.py'
        assert digest(ROOT/'scripts'/script)==verification['audit_script_sha256']
        for field,path in [('protocol_sha256','protocolo.json'),('catalog_sha256','catalogo_modelos.json'),('predictions_sha256','predicciones_oof.csv.gz')]:
            assert digest(directory/path)==verification[field]
        for path,sha in read(directory/'protocolo.json')['sources'].items(): assert digest(ROOT/path)==sha
        hashes[dirname]=digest(directory/'verificacion.json')
        if dirname.endswith('_completa'):
            continuation=read(directory/'continuacion.json')
            script='continuar_regresion_ordinal.py' if title=='Regresión ordinal' else 'continuar_multiescala.py'
            assert digest(ROOT/'scripts'/script)==continuation['script_sha256']
            partial=ROOT/'resultados'/dirname.removesuffix('_completa')
            for path,sha in continuation['source_inventory'].items(): assert digest(partial/path)==sha
            hashes[dirname+'/continuacion']=digest(directory/'continuacion.json')
        total_models+=verification['models_reloaded']; total_predictions+=verification['predictions_verified']; total_scores+=verification['inner_scores_verified']
        summary=pd.read_csv(directory/'resumen_oof.csv'); people=pd.read_csv(directory/'metricas_participantes.csv')
        for _,item in summary.iterrows():
            values=people.loc[people.scope.eq(item.scope)].groupby('participant').score.mean()
            lo,hi=bootstrap(values)
            rows.append(dict(round=title,scope=item.scope,primary=item.scope=='all',BA_macro=item.macro_score,BA_global=item.balanced_accuracy,
                macro_F1=item.macro_f1,ci_low=lo,ci_high=hi,report=report))
    table=pd.DataFrame(rows); table.to_csv(OUT/'comparacion_completa.csv',index=False)
    best=table.sort_values('BA_macro',ascending=False).iloc[0]; previous=.3716042472822324
    fig,ax=plt.subplots(figsize=(10,8.5)); positions=np.arange(len(table))
    for i,row in table.iterrows():
        color='#145da0' if row.primary else '#666666'
        ax.errorbar(row.BA_macro,i,xerr=[[row.BA_macro-row.ci_low],[row.ci_high-row.BA_macro]],fmt='o',color=color,capsize=3)
    ax.set_yticks(positions,[f'{r["round"]} · {r["scope"]}' for _,r in table.iterrows()]); ax.invert_yaxis()
    ax.axvline(.5,color='#a63603',linestyle='--',label='Meta 0,50'); ax.axvline(previous,color='#40826d',linestyle=':',label='Máximo anterior 0,3716')
    ax.set_xlim(min(.27,table.ci_low.min()-.01),max(.53,table.ci_high.max()+.01)); ax.set_xlabel('BA macro por participante (IC descriptivo 95 %)')
    ax.set_title('Activación: cuatro búsquedas con etiquetas fijas\nAzul: selección principal; gris: familias secundarias',loc='left')
    ax.grid(axis='x',alpha=.2); ax.legend(loc='lower right'); fig.tight_layout()
    for suffix in ['png','pdf']: fig.savefig(OUT/f'comparacion.{suffix}',dpi=180,bbox_inches='tight')
    plt.close(fig)
    report=f'''# Búsqueda de BA macro sobre 0,50: 12-09-2026

**Meta {'alcanzada solo como observación exploratoria' if best.BA_macro>.5 else 'no alcanzada'}.** Máximo observado de estas rondas:
{best.BA_macro:.4f}, {best['round']} / {best.scope}. Es un contraste {'principal' if best.primary else 'secundario'}.
La referencia previa era 0,3716, también secundaria. El resultado no demuestra que
0,50 sea imposible ni confirma generalización independiente.

## Qué se probó

1. Persistencia: 16 filtros sobre el promedio fijo con historial. Media causal, EMA y
   Markov con transiciones aprendidas solo dentro de ajuste. 240 puntuaciones internas.
2. Multiescala: 24 configuraciones con Ridge, RBF y Extra Trees; señales actuales,
   estadísticas de 4/16/64 ventanas, desfase de cuatro ventanas y desviaciones relativas.
   360 ajustes internos y 1.080 puntuaciones con suavizado 1/8/32.
3. Adaptación offline: 60 reglas de centrado/rango por persona sin etiquetas; 900
   puntuaciones internas. Requiere la sesión completa y no sirve para afirmar desempeño
   causal o en tiempo real.
4. Regresión ordinal: 12 modelos base con Ridge, RBF, HGB y Extra Trees. Codificación
   -1/0/1, 18 reglas de umbral/suavizado, 180 ajustes internos y 3.240 puntuaciones.

Todas mantienen arousal_label_6s y EEG + mirada + pupila como entradas. GSR no entra
al estudiante. La regresión cambia la función de entrenamiento, no la etiqueta evaluada.
Cinco folds externos por participante dentro de train y tres internos. Se congelan
las elecciones antes de evaluar cada ronda externamente. No se reevaluaron validation/test.

## Comparación completa

{markdown(table,['round','scope','primary','BA_macro','BA_global','macro_F1'])}

![Comparación de todas las reglas](../resultados/meta_05_12-09-2026/comparacion.png)

Los IC de la figura son descriptivos: 2.000 remuestreos por participante, tras promediar
semillas. No corrigen selección adaptativa ni dependencia entre folds. Se han probado
muchos enfoques sobre las mismas 25 personas: escoger retrospectivamente el máximo
es una exploración, no evidencia de superioridad confirmada. No se cambia BA macro por
accuracy, por la métrica de un fold favorable ni por una clasificación binaria.

## Hallazgos de auditoría

- El mejor Ridge multiescala da 0,37475 frente a 0,37160: +0,315 puntos porcentuales,
  IC pareado [-2,262; +2,770], mejora en 14/25 personas. La selección conjunta da 0,36485.
- Su recall medio es 0,2327; bajo, 0,4995; alto, 0,3758. La mezcla anterior tenía recall
  medio 0,2881. Una BA mayor puede ocultar un intercambio desfavorable entre clases.
- Las etiquetas originales usan cuantiles por persona. Un mismo Arousal Score puede
  corresponder a clases diferentes entre personas; no se usa un umbral global inventado
  para reinterpretarlas. Fuente: scripts/preparar_modelado.py, función ternary y aplicación
  por participante. Este diagnóstico no altera el diseño ya validado.
- La igualdad exacta de scores detuvo el primer intento multiescala con diferencias
  de 1,67e-16. Se conserva completo en multiescala_11-09-2026; la continuación reutiliza
  idénticas elecciones y predicciones internas, y repite solo ajustes externos. Tolera
  rtol=atol=1e-12 en scores, exigiendo clases idénticas. La diferencia máxima en la
  continuación fue 4,94e-13. El escalado reajustado se verifica con esa misma tolerancia
  relativa/absoluta; sus unidades pueden producir diferencias absolutas mayores.
- La regresión ordinal se detuvo también en RBF con diferencia de 2,83e-11. Se comprobó
  que las variables eran exactamente iguales y que el origen era la disposición en
  memoria. Con entradas C-contiguas la diferencia fue cero; se conserva la tolerancia
  1e-12 y se repiten solo ajustes externos. La continuación mantiene los 180 ajustes
  internos y umbrales congelados. Se guarda también el intento ordinal parcial.
- Una prueba de dependencia futura de la adaptación usaba un umbral que no cruzaba
  con el ejemplo; se corrigió el ejemplo antes de entrenar. Las 56 pruebas finales pasan.
  Joblib emite advertencias de deprecación de NumPy al recargar; las comprobaciones pasan.

## Artefactos y reproducción

{total_models} archivos de modelos completos recargados; {total_predictions:,} predicciones
verificadas; {total_scores:,} puntuaciones internas recalculadas. Se conservan además
los modelos del intento parcial, que no se cuentan como una ronda externa completa.
540 ajustes internos nuevos en los dos enfoques que entrenan clasificadores/regresores.
Los filtros reutilizan modelos base auditados. Los informes individuales detallan
configuraciones, métricas por clase/persona, intervalos y comandos.

Multiescala completa: scripts/continuar_multiescala.py; auditoría:
scripts/continuar_multiescala.py --audit. El script original reproduce también el intento
interrumpido; no debe ejecutarse encima de los artefactos existentes. Los originales
permanecen conservados y el manifiesto continuacion.json explica la corrección.
Regresión ordinal completa y predictor canónico: scripts/continuar_regresion_ordinal.py;
auditoría: scripts/continuar_regresion_ordinal.py --audit. Para cargar los modelos usar
continuar_regresion_ordinal.predict(bundle, frame); el controlador de auditoría utiliza
ese mismo predictor y verifica además el inventario y las elecciones de la fuente parcial.

Reproducir las otras rondas con sus scripts entrenar_* y auditar_* indicados en los
informes. Para regenerar este resumen, usar scripts/informe_meta_05.py en una copia sin
el directorio meta_05_12-09-2026 existente. Pesos, predicciones, selecciones, hashes y
protocolos se conservan en resultados. La normalización original sigue siendo offline.

## Qué implica no llegar a 0,50

Estas búsquedas no respaldan prometer 0,50 mediante más ajuste de hiperparámetros. El
desempeño puede estar limitado por la relación entre señales del estudiante y la
pseudoetiqueta GSR, la variación entre personas o la calidad/sincronización. Son hipótesis
pendientes de comprobar, no causas demostradas. El siguiente paso con valor metodológico
es auditar esas relaciones y la calidad temporal antes de ampliar otra grilla; cualquier
cambio futuro de etiqueta requeriría un experimento separado y dejaría de ser comparable.

Informes: [persistencia](Busqueda_persistencia_11-09-2026.md),
[multiescala](Busqueda_multiescala_11-09-2026.md),
[adaptación offline](Busqueda_adaptacion_11-09-2026.md),
[regresión ordinal](Regresion_Ordinal_12-09-2026.md).
'''
    (ROOT/'documentacion/Busqueda_Meta_05_12-09-2026.md').write_text(report,encoding='utf-8')
    write_json(OUT/'verificacion_resumen.json',dict(created_utc=datetime.now(timezone.utc).isoformat(),source_verifications=hashes,
        script_sha256=digest(__file__),models=total_models,predictions=total_predictions,inner_scores=total_scores,
        best_macro=float(best.BA_macro),target=.5,target_reached=bool(best.BA_macro>.5),tests_passed=56,
        validation_evaluated=False,test_evaluated=False))
    print(table.to_string(index=False)); print('Total models',total_models,'predictions',total_predictions,'inner scores',total_scores)


if __name__=='__main__': main()
