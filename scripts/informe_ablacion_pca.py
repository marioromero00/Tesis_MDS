"""Informe y figuras de contribucion predictiva, separados de varianza PCA."""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from temporales_core import ROOT,digest,write_json
from informe_control_historial import markdown

OUT=ROOT/'resultados/ablacion_pca_12-09-2026'


def plot_loss(frame,filename,title):
    fig,ax=plt.subplots(figsize=(10,max(4,len(frame)*.29+1.5)))
    y=np.arange(len(frame)); delta=100*frame.loss_vs_reference.to_numpy()
    ax.errorbar(delta,y,xerr=np.vstack([delta-100*frame.ci_low,100*frame.ci_high-delta]),fmt='o',capsize=3,color='#185d8b')
    ax.set_yticks(y,frame.variant); ax.invert_yaxis(); ax.axvline(0,color='#555555',linestyle='--'); ax.grid(axis='x',alpha=.2)
    ax.set_xlabel('Pérdida frente al modelo completo (puntos de BA macro)\nPositivo: quitar perjudica; negativo: la variante mejora')
    ax.set_title(title,loc='left'); fig.tight_layout()
    for extension in ['png','pdf']: fig.savefig(OUT/f'{filename}.{extension}',dpi=180,bbox_inches='tight')
    plt.close(fig)


def main():
    verification=json.loads((OUT/'verificacion.json').read_text()); assert digest(ROOT/'scripts/auditar_ablacion_pca.py')==verification['audit_script_sha256']
    assert digest(OUT/'resumen_ablaciones.csv')==verification['summary_sha256']
    table=pd.read_csv(OUT/'resumen_ablaciones.csv'); ranking=pd.read_csv(OUT/'ranking_variables.csv'); pca=pd.read_csv(OUT/'resumen_pca.csv')
    variables=ranking.copy(); variables['variant']=variables.feature
    plot_loss(table.loc[table.kind.isin(['modality','temporal'])],'ablacion_modalidades_historial','Ablación de modalidades y temporalidad\nIC descriptivos, 25 participantes')
    plot_loss(variables,'ablacion_variables','Ablación de cada variable y todas sus derivadas\nIC descriptivos; orden por pérdida media')
    plot_loss(table.loc[table.kind.eq('pca')],'pca_prediccion','PCA: cambio de capacidad predictiva\nVarianza conservada y predicción son criterios distintos')
    variance=pd.read_csv(OUT/'pca_varianza.csv'); fig,ax=plt.subplots(figsize=(8,5))
    for fold,g in variance.loc[variance.variant.eq('pca_full')].groupby('fold'):
        ax.plot(g.component,g.cumulative_variance,label=f'Fold {fold} ({g.dimensions_before.iloc[0]} entradas)')
    for v in [.8,.9,.95]: ax.axhline(v,color='#777777',alpha=.4,linestyle=':')
    ax.set(xlabel='Número de componentes',ylabel='Varianza acumulada del ajuste',title='PCA ajustado solo en las personas de entrenamiento',ylim=(0,1.02)); ax.legend(); ax.grid(alpha=.2); fig.tight_layout()
    for extension in ['png','pdf']: fig.savefig(OUT/f'pca_varianza.{extension}',dpi=180,bbox_inches='tight')
    plt.close(fig)
    condensed=pca.groupby('variant',as_index=False).agg(min_components=('dimensions_after','min'),max_components=('dimensions_after','max'),mean_retained=('retained_variance','mean'))
    columns=['variant','macro_score','loss_vs_reference','ci_low','ci_high','people_hurt_by_removal']
    report=f'''# Ablación y PCA para activación: 12-09-2026

Se completaron 38 variantes en cinco folds: **190 modelos reentrenados y guardados**,
513.912 predicciones verificadas, 190 preprocesadores reajustados y 20 PCA reajustados
en auditoría. La referencia reproduce el Ridge anterior: BA macro 0,37475. El estudio
mantiene arousal_label_6s, las 25 personas de train, las tres clases y los hiperparámetros
elegidos previamente dentro de cada fold. No se volvió a evaluar validation/test.

## Qué se compara y qué significa

Se quita cada modalidad, se conserva cada modalidad por separado y se elimina cada una
de las 24 variables originales con TODAS sus derivadas temporales e indicadores de
ausencia. Cada variante reajusta imputación, escalado y Ridge solo con las 20 personas
de ajuste; las cinco externas se usan para medir el resultado. GSR y las etiquetas no
entran al estudiante. No se prueban nuevas variantes de atención en esta ronda.

La contribución se define como **BA del modelo completo menos BA de la variante**.
Una pérdida positiva significa que quitar esa entrada perjudica al modelo; una negativa
significa que quitarla mejoró el promedio observado. Se informa contribución predictiva
condicionada a este modelo e hiperparámetros, no importancia fisiológica ni causalidad.
Variables correlacionadas pueden compensarse. Las modalidades aisladas evalúan suficiencia,
mientras que quitar una modalidad evalúa su aporte adicional al resto.

Los contrastes principales declarados son quitar EEG, mirada o pupila y quitar conjuntamente
historial/suavizado. Las variables individuales y los niveles de PCA son secundarios.
Los IC son descriptivos: 2.000 remuestreos pareados por persona; no corrigen múltiples
comparaciones, búsquedas previas ni dependencia entre folds. No se elige retrospectivamente
un nuevo panel final usando estos resultados externos.

## Modalidades y temporalidad

{markdown(table.loc[table.kind.isin(['reference','modality','unimodal','temporal'])],columns)}

![Modalidades e historial](../resultados/ablacion_pca_12-09-2026/ablacion_modalidades_historial.png)

Quitar EEG produce la mayor pérdida media entre modalidades: 0,37475 a 0,35456. Solo EEG
mantiene 0,37222, cercano al modelo completo; sin embargo, su recall medio cae de 0,2327
a 0,1079 y macro-F1 de 0,3646 a 0,3385. Acotar a EEG requiere resolver ese intercambio,
además de confirmación independiente. Quitar mirada da 0,37058 y quitar pupila 0,37397.
La pérdida al quitar EEG es +2,019 puntos de BA, IC descriptivo [+0,045; +4,116].
No se aplica una corrección por múltiples comparaciones. Los intervalos de las otras
modalidades y de las variables individuales no permiten establecer un orden firme.

Usar ventana actual con el mismo suavizado obtiene 0,36699; quitar solo el suavizado,
0,37191; quitar ambos, 0,36041. No son modelos temporales idénticos en los cinco folds:
la referencia elegida usa actual en fold 1, multiescala en 2/4, desfase en 3 y variables
relativas en 5. El fold 1 ya carece de historial de entradas y el fold 5 ya carece de
suavizado. Cambiar a actual elimina también la transformación/desfase correspondiente.
Estos controles no aíslan una arquitectura de red específica.

## Variables originales

Ranking completo por pérdida al quitar cada variable; las cifras están en unidades de BA,
no en porcentaje. Los intervalos amplios impiden interpretar diferencias pequeñas como
un orden definitivo de importancia.

{markdown(ranking,['feature','macro_score','loss_vs_reference','ci_low','ci_high','people_hurt_by_removal'])}

![Variables](../resultados/ablacion_pca_12-09-2026/ablacion_variables.png)

Las mayores pérdidas medias individuales corresponden a amplitud pico a pico EEG,
media pupilar, recorrido de la mirada y máximo pupilar. Quitar fixation_count produce
el mayor aumento puntual: 0,38433, ganancia +0,957 puntos, IC descriptivo [+0,287; +1,702],
con mejora en 17/25 personas. Macro-F1 sube a 0,3733 y recall medio a 0,2400. Es una
observación secundaria después de comparar
24 eliminaciones; no demuestra que esa variable sea perjudicial fuera de esta muestra.
No se combinan automáticamente las eliminaciones que mejoran, porque sus efectos pueden
interactuar y el panel resultante necesitaría seleccionarse dentro de entrenamiento.

## PCA

PCA se ajusta después de imputación y estandarización, incluye los indicadores de
ausencia generados por el preprocesador y no usa etiquetas para elegir componentes.
Se conserva 80 %, 90 % o 95 % de varianza de ajuste; no hay whitening ni reescalado
posterior. Ridge mantiene alpha=1. Los hiperparámetros no se reajustan por variante.

{markdown(table.loc[table.kind.eq('pca')],columns)}

{markdown(condensed,list(condensed.columns))}

![PCA y predicción](../resultados/ablacion_pca_12-09-2026/pca_prediccion.png)

![PCA y varianza](../resultados/ablacion_pca_12-09-2026/pca_varianza.png)

PCA al 90 % obtiene BA macro 0,37640; al 95 %, 0,36439; al 80 %, 0,35539. Conservar
más varianza no ordena el rendimiento predictivo. PCA completo reproduce la referencia,
como control de la rotación de Ridge. El máximo de 90 % es exploratorio; no constituye
una selección validada de dimensionalidad.

Las cargas y varianzas por componente/fold están en pca_cargas.csv.gz y pca_varianza.csv.
Una carga grande explica una dirección de variación de las entradas, no demuestra
importancia para predecir activación. El signo de las componentes es arbitrario y sus
bases difieren entre folds; no se promedian cargas de componentes supuestamente equivalentes.

## Auditoría, archivos y reproducción

Protocolo y 38 definiciones congelados antes de entrenar. La auditoría recarga los 190
modelos, verifica disjunción de participantes, reconstruye las especificaciones,
reajusta los 190 imputadores/escaladores y los 20 PCA. Comprueba sus subespacios, varianza
y todas las cargas guardadas; recalcula 190 métricas de fold y 950 por participante.
Verifica scores con rtol=atol=1e-12 y clases exactamente iguales; la equivalencia de
PCA completo usa 1e-9 en scores y clases idénticas. El script original compara además
los cinco modelos completos con las predicciones de la ronda anterior.

Entrenamiento: `python scripts/entrenar_ablacion_pca.py`, en una copia sin el directorio
de salida existente. Auditoría: `python scripts/auditar_ablacion_pca.py`. Informe:
`python scripts/informe_ablacion_pca.py`. Carga: agregar scripts al path, joblib.load y
`predecir_ablacion_pca.predict(bundle, frame)` con frame ordenado por persona/grabación/tiempo.
No requiere etiquetas al predecir. El predictor calcula features por variable y después
selecciona las columnas; las pruebas verifican que alterar entradas eliminadas o GSR
no cambia las entradas efectivas. Se conserva la limitación de normalización original offline.
El adaptador de carga requiere solo las señales retenidas y los metadatos temporales;
rellena con NaN las señales eliminadas antes de descartarlas junto con sus derivadas.
Las 59 pruebas finales del proyecto pasan; el registro está en pruebas.json.

Estos resultados ayudan a priorizar un panel reducido para una futura selección interna.
No alcanzan 0,50 ni convierten el máximo observado en una confirmación independiente.

Fuentes metodológicas: [PCA de scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)
y [efecto de variables correlacionadas en la importancia](https://scikit-learn.org/stable/auto_examples/inspection/plot_permutation_importance_multicollinear.html).
'''
    (ROOT/'documentacion/Ablacion_PCA_12-09-2026.md').write_text(report,encoding='utf-8')
    write_json(OUT/'verificacion_informe.json',dict(source_verification_sha256=digest(OUT/'verificacion.json'),script_sha256=digest(__file__),
        reduced_predictor_sha256=digest(ROOT/'scripts/predecir_ablacion_pca.py'),
        figures={p.name:digest(p) for p in OUT.glob('*.png')},report='documentacion/Ablacion_PCA_12-09-2026.md'))
    print(condensed.to_string(index=False))


if __name__=='__main__': main()
