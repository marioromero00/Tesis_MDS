"""Planificación prospectiva, no una nueva prueba confirmatoria sobre test reutilizado."""
from pathlib import Path
import json, math, hashlib
import numpy as np
import pandas as pd
from scipy.stats import t, nct
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'resultados/protocolo_hipotesis_02-11-2026'

def required_n(sd, distance, power=.9):
    def prob(n):return nct.sf(t.ppf(.9875,n-1),n-1,distance*np.sqrt(n)/sd)
    lo,hi=3,4
    while prob(hi)<power:hi*=2
    while lo<hi:
        mid=(lo+hi)//2
        if prob(mid)>=power:hi=mid
        else:lo=mid+1
    assert prob(lo)>=power and (lo==3 or prob(lo-1)<power)
    return lo,float(prob(lo))

def main():
    OUT.mkdir(exist_ok=True)
    ap=ROOT/'resultados/activacion_gsr_v2_recalculo_02-11-2026/metricas_personas.csv'
    tp=ROOT/'resultados/temporalidad_eeg_v2_test_29-10-2026/metricas_participantes.csv'
    a=pd.read_csv(ap);rows=[];diff=[]
    for split,g in a.groupby('split'):
        w=g.pivot(index='participant',columns='context',values='auc');d=w[32]-w[1]
        rows.append(dict(task='activacion',pilot=split,n=len(d),sd=d.std(ddof=1),mean=d.mean()))
        diff.extend(dict(task='activacion',pilot=split,participant=p,delta=v) for p,v in d.items())
    w=pd.read_csv(tp).pivot(index='participant',columns='strategy',values='auc')
    d=w.inductivo_ctx32-w.inductivo_estatico_pareado
    rows.append(dict(task='atencion',pilot='test_historico',n=len(d),sd=d.std(ddof=1),mean=d.mean()))
    diff.extend(dict(task='atencion',pilot='test_historico',participant=p,delta=v) for p,v in d.items())
    pilot=pd.DataFrame(rows);pilot.to_csv(OUT/'dispersion_piloto.csv',index=False)
    sensitivity=[]
    for r in pilot.itertuples():
        n,power=required_n(r.sd,.02)
        sensitivity.append(dict(task=r.task,pilot=r.pilot,sd=r.sd,distance=.02,n_evaluable=n,power=power))
    pd.DataFrame(sensitivity).to_csv(OUT/'sensibilidad_fuente_varianza.csv',index=False)
    assert abs(nct.sf(t.ppf(.9875,99),99,0)-.0125)<1e-10
    assert required_n(.1,.01)[0]>required_n(.1,.02)[0]
    assert required_n(.2,.02)[0]>required_n(.1,.02)[0]
    manifests=[]
    configs=[(ROOT/'resultados/temporalidad_eeg_v2_test_29-10-2026/congelacion_pre_test.json',['inductivo_estatico_pareado','inductivo_ctx32']),
             (ROOT/'resultados/activacion_gsr_v2_recalculo_02-11-2026/congelacion.json',['1','32'])]
    for config,keys in configs:
        models=json.loads(config.read_text())['models']
        for key in keys:
            path=Path(models[key]['path']);path=path if path.is_absolute() else ROOT/path
            sha=hashlib.sha256(path.read_bytes()).hexdigest();assert sha==models[key]['sha256']
            manifests.append(dict(id=key,path=str(path.relative_to(ROOT)),sha256=sha))
    for path in [ROOT/'resultados/temporalidad_eeg_v2_validacion_29-10-2026/profesor_final.joblib',ROOT/'scripts/reconstruir_etiquetas_gsr_calidad_v2.py',ROOT/'scripts/temporales_core.py',ROOT/'scripts/comparacion_comun_binaria.py']:
        manifests.append(dict(path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    (OUT/'manifiesto_modelos.json').write_text(json.dumps(manifests,indent=2))
    pd.DataFrame(diff).to_csv(OUT/'diferencias_piloto.csv',index=False)
    # Scenarios, not observed-power calculations: true effects are set independently of observed means.
    sizes=[]
    for task,g in pilot.groupby('task'):
        sd=g.sd.max()
        for inflation in [1.,1.5]:
            for margin in [.01,.02,.03]:
                for distance in [.01,.02,.03]:
                    n,p=required_n(sd*inflation,distance)
                    sizes.append(dict(task=task,pilot_sd=sd,sd_factor=inflation,margin=margin,distance_from_margin=distance,true_effect_if_support=margin+distance,true_effect_if_refute=margin-distance,n_evaluable=n,n_recruit_if_20pct_loss=math.ceil(n/.8),power_per_endpoint=p))
    sizes=pd.DataFrame(sizes);sizes.to_csv(OUT/'escenarios_muestra.csv',index=False)
    p=dict(status='propuesta prospectiva; margen y N aún no definitivos',margin_candidate=.02,
           claim='Delta AUC > margen en atención Y activación; restringida a modelos y pseudoetiquetas especificados',
           original_claim='superioridad >0; el margen práctico >0 es una reformulación explícita, no reemplazo retrospectivo',
           primary_context=32,secondary_context=8,unit='participante independiente',
           familywise_alpha=.05,ci_each=.975,tail_alpha=.0125,target_power_each=.9,
           joint_power_lower_bound=.8,dropout_scenario=.2,
           decision=dict(support='ambos límites inferiores > margen',refute='al menos un límite superior < margen',inconclusive='cualquier otro caso'),
           sources={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in [ap,tp,Path(__file__)]},
           references=['https://www.stat.math.ethz.ch/R-manual/R-patched/RHOME/library/stats/html/power.t.test.html','https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm'])
    (OUT/'protocolo.json').write_text(json.dumps(p,indent=2,ensure_ascii=False))
    selected=sizes[sizes.margin.eq(.02)&sizes.distance_from_margin.eq(.02)]
    print(pilot.to_string(index=False));print(selected[['task','sd_factor','n_evaluable','n_recruit_if_20pct_loss']].to_string(index=False))
    lines=['# Protocolo prospectivo para contrastar la hipótesis','','Estado: propuesta concreta y reproducible; no es un preregistro retrospectivo ni una nueva confirmación. Margen candidato +0,02 AUC, sin justificación sustantiva independiente todavía. No se modificó el manuscrito original.','',
    '## El modelo cercano a 0,67','El candidato localizado es CatBoost estático de atención: AUC test 0,6744 y validación 0,6798. No es el modelo de activación. La comparación histórica de temporalidad con familia emparejada fue HistBoost 0,687901 frente a HistBoost estático 0,660179; no se debe atribuir toda la diferencia frente al CatBoost a temporalidad. La identificación del modelo mencionado por Mario es provisional.', '',
    '## Afirmación y regla de decisión',
    'Para modelos previamente fijados y personas nuevas de la misma población, definir D por persona = AUC temporal menos AUC estático. Evaluar media de D por tarea. Propuesta de relevancia práctica: ambas medias superan +0,02. La hipótesis original dice mejor (>0): no se puede rechazar esa superioridad original solamente porque se descarta una mejora de +0,02. Reportar también la relación del intervalo con cero.',
    'Intervalos t bilaterales de 97,5% por tarea, con cobertura simultánea de al menos 95% por Bonferroni. Respaldar la afirmación práctica si ambos límites inferiores superan el margen; refutarla para estos modelos si al menos un límite superior queda por debajo. Si los intervalos cruzan el margen, mantener indeterminación. Esta regla no prueba equivalencia (que exigiría un intervalo contenido en una banda bilateral) ni descarta toda arquitectura temporal.', '',
    '## Evaluación propuesta',
    '1. Fijar contexto principal hasta 32 ventanas; 8 queda secundario sin sustituir al principal según resultados. Para atención usar la pareja HistBoost inductiva emparejada de temporalidad_eeg_v2_test_29-10-2026; para activación usar final_ctx1 y final_ctx32 del recálculo GSR V2. Conservar pesos y parámetros, y no entrenar con la cohorte nueva.',
    '2. Conservar el profesor PCA reconstruido de atención y el GSR V2 auditado; mismo etiquetado, entradas, ventanas por tarea y preprocesamiento ajustado en train para ambos modelos. Registrar versiones, hashes y modelos en el manifiesto adjunto. El objetivo queda explícitamente como pseudoetiqueta offline: la normalización personal del profesor usa la sesión completa. Esto requiere reconciliar la redacción del manuscrito que exige normalización solo en train; no presentar como inferencia psicológica online.',
    '3. Reclutar participantes nuevos; los 41 existentes no cuentan como una nueva cohorte independiente. No reciclar exclusiones por mala señal ni P29 como reemplazo. No aumentar N contando ventanas, semillas o folds. Mantener protocolo de estímulos y adquisición comparable.',
    '4. Definir elegibilidad antes de analizar: calidad y sincronización aprobadas, al menos 100 ventanas etiquetadas y 20 por clase en cada tarea, sin filtrar por AUC. Son umbrales operativos propuestos, no validados; una fase de factibilidad ciega a predicciones debe confirmar su viabilidad. Para cierre conjunto usar personas elegibles en ambas tareas; reportar exclusiones y su efecto sobre generalización.',
    '5. Registrar N final y reglas antes de evaluar; sin consultas intermedias de AUC ni ampliación de muestra después de mirar el efecto. Se permite controlar reclutamiento/calidad sin resultados predictivos. Separar consentimiento y adquisición de cualquier análisis automático.',
    '6. Calcular diferencias pareadas y los intervalos preespecificados una sola vez. Usar bootstrap de participantes como sensibilidad, sin elegir el método que favorezca el resultado. Documentar historial efectivo y no afirmar secuencias completas de 32 si no están disponibles.', '',
    '## Tamaño de muestra por escenarios',
    'Se usa la desviación de diferencias individuales, no la desviación de ventanas. Para activación se toma la mayor desviación entre OOF train, validación y test; OOF comparte modelos y solo sirve como estimación piloto aproximada. Atención dispone aquí de ocho personas de test histórico. Estas varianzas son inciertas y la diferencia entre protocolos puede cambiar la dispersión. Se incluye inflación 1,5 como sensibilidad, no como cota de confianza.',
    'Cálculo mediante t no central: potencia 90% por resultado, umbral unilateral 0,0125 consistente con los intervalos simultáneos. Si ambos efectos verdaderos están a la distancia planeada sobre el margen, la potencia conjunta es al menos 80% por la cota de unión, sin suponer independencia entre tareas. No es potencia observada ni garantía de precisión real.',
    'Ejemplo: margen 0,02; efecto verdadero 0,04 para respaldar o 0,00 para refutar. Ambos están a distancia 0,02 del límite. Si el efecto verdadero es 0,02, ningún tamaño finito garantiza una decisión; un efecto de 0,03 está a distancia 0,01 y exige mucho más N.','',
    '| Tarea | Inflación SD | Personas evaluables nuevas | Reclutar con 20% pérdidas |','|---|---:|---:|---:|']
    for r in selected.itertuples():lines.append(f'| {r.task} | {r.sd_factor:.1f} | {r.n_evaluable} | {r.n_recruit_if_20pct_loss} |')
    lines+=['','Para el estudio conjunto se toma el mayor N de ambas tareas, no se suman si las mismas personas aportan ambos resultados. El 20% es un supuesto de planificación; no proviene de una tasa observada. No hay compromiso de recolectar estos datos.','',
    '## Decisiones pendientes y alcance',
    'El margen 0,02 necesita una justificación de relevancia independiente (uso, reproducibilidad del instrumento o criterio académico); no se convierte en válido porque produzca un N conveniente. Los escenarios 0,01/0,02/0,03 están en escenarios_muestra.csv. Falta confirmar factibilidad de nueva cohorte, elegibilidad y alcance de activación con el profesor. Sin nueva cohorte, este diseño queda preparado pero no ejecutado; repetir el test existente no lo vuelve confirmatorio.',
    'Este protocolo evalúa agregación de historial (media/desviación), no sensibilidad al orden, ni fusión intermedia/tardía. Por tanto, su cierre se limita a la proposición operacionalizada y no cubre todos los mecanismos descritos por la hipótesis general de la tesis.','',
    'Método: [potencia de pruebas pareadas, documentación de R](https://www.stat.math.ethz.ch/R-manual/R-patched/RHOME/library/stats/html/power.t.test.html) y [intervalos t, NIST](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm). Ejecución: `.venv/bin/python scripts/planificar_contraste_hipotesis.py`.']
    (OUT/'INFORME.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':main()
