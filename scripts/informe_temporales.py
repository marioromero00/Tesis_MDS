"""Informe y figuras exportables de TCN, LSTM, BiLSTM y explicacion vs baseline."""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from temporales_core import ROOT,OUT

REPORT=ROOT/'documentacion/Modelos_Temporales_07-09-2026.md'
TASKS={'attention_primary':'Atención','arousal_primary_6s':'Activación'}
KINDS={'classification':'clasificación','regression':'regresión'}


def num(x):
    return f'{x:.4f}'.replace('.',',')


def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+
                     ['| '+' | '.join(map(str,row))+' |' for row in rows])


def matching(frame,choice):
    mask=np.ones(len(frame),dtype=bool)
    for key in ['task','kind','subset','architecture']:
        mask &= frame[key].eq(choice[key])
    return frame.loc[mask]


def main():
    config=json.loads((OUT/'protocolo.json').read_text(encoding='utf-8'))
    choices=json.loads((OUT/'seleccion_antes_test.json').read_text(encoding='utf-8'))['models']
    catalog=json.loads((OUT/'catalogo_modelos.json').read_text(encoding='utf-8'))
    audit=json.loads((OUT/'verificacion_entrega.json').read_text(encoding='utf-8'))
    m=pd.read_csv(OUT/'metricas_temporales.csv');m=m.loc[m.scope.eq('all')]
    b=pd.read_csv(OUT/'metricas_estaticos_mismas_ventanas.csv');b=b.loc[b.scope.eq('all')]
    gains=pd.read_csv(OUT/'ganancias_vs_baseline.csv')
    importance=pd.read_csv(OUT/'importancia_vs_baseline.csv')
    history=pd.read_csv(OUT/'dependencia_del_historial.csv')
    coverage=pd.read_csv(OUT/'cobertura_evaluacion.csv')
    sections=['# TCN, LSTM y BiLSTM — resultados del 07-09-2026',
        'Fuente: ejecución local de `entrenar_temporales.py`, `evaluar_temporales.py` y '
        '`verificar_temporales.py`. Las fechas UTC de los manifiestos pueden corresponder '
        'al 08-09; la fecha local de Chile de esta entrega es 07-09-2026.',
        '## Resultado principal',
        '**La clasificación de activación presenta mejoras puntuales frente a algunos baselines, '
        'pero el experimento no demuestra una ventaja general del historial temporal.** '
        'En el conjunto completo, la BA global de prueba promediada entre semillas es 0,3551 '
        'para TCN, 0,3354 para LSTM y 0,3594 para BiLSTM. La logística estática obtiene '
        '0,3169, RF 0,3365 y el control neuronal sin historial 0,3503. Son configuraciones '
        'predefinidas; no se seleccionó el máximo de test como ganador.',
        'La configuración de clasificación de activación elegida **antes de test** fue '
        'BiLSTM con cinco variables pupilares sin la columna explícita de validez. '
        'Obtiene BA global media de prueba 0,3472, frente a aproximadamente 0,3929 en '
        'validación. Su mejora macro por participante frente a la logística con las mismas '
        'cinco entradas es 0,0192, intervalo descriptivo [-0,0065; 0,0449]. La mejora '
        'puntual no constituye superioridad confirmada.',
        'LSTM completa de activación supera a la logística completa en BA macro por '
        'participante: +0,0212, intervalo [0,0058; 0,0400]. Frente al control neuronal '
        'sin historial, la diferencia es -0,0032, intervalo [-0,0312; 0,0193]. Esta '
        'comparación limita la atribución de la mejora a temporalidad.',
        'En atención, los resultados de clasificación permanecen cerca del nivel trivial. '
        'Los R² de prueba de los scores continuos quedan alrededor de cero; el '
        'experimento no mejora de forma clara esa parte del problema.',
        '## Qué se entrenó y guardó',
        f'**{len(catalog)} redes guardadas**: 32 TCN, 32 LSTM, 32 BiLSTM y 8 controles '
        'MLP_current. Corresponden a dos tareas, clasificación/regresión, los ocho '
        'conjuntos congelados y dos semillas (20260907/20260908). El MLP se usa en los '
        'conjuntos completos. Se guardan pesos, metadatos, preprocesadores, historiales '
        'por época, predicciones y probabilidades, selección anterior a test y métricas.',
        'Se mantuvieron 25 participantes de entrenamiento (13.524 ventanas), ocho de '
        'validación (4.662) y ocho de prueba (4.025). P29 y excluidos no entran en esta '
        'ejecución. Las etiquetas principales y el contexto GSR de 6 s permanecen fijos. '
        'No se construyeron nuevas pseudoetiquetas ni se entrenó sobre señales crudas.',
        '## Secuencias y arquitectura',
        'Cada predicción usa la ventana actual y hasta siete anteriores del mismo '
        'participante, grabación, segmento y estímulo, con avance exacto de 1 s. '
        'La secuencia se reinicia ante cualquier hueco. Ocho ventanas de 2 s solapadas '
        'abarcan un máximo de 9 s. Se conserva cada ventana elegible; las secuencias '
        'cortas llevan padding cero a derecha después del escalado y su longitud real '
        'se pasa al modelo. El padding no puede modificar la predicción.',
        'TCN tiene dos bloques residuales, cada uno con dos convoluciones causales de '
        'kernel 3, dilataciones 1 y 2, 24 canales, ReLU y dropout 0,2. Su campo '
        'receptivo teórico es de 13 pasos y se limita al contexto disponible de hasta '
        'ocho. LSTM tiene una capa de 24 unidades. BiLSTM tiene 24 unidades por '
        'dirección y concatena los estados finales de ambas direcciones. La cabeza '
        'lineal entrega tres logits o un score continuo.',
        'La BiLSTM recorre en ambas direcciones **solo la historia disponible hasta '
        'la ventana objetivo**. No es una BiLSTM centrada que lea ventanas posteriores. '
        'La normalización original de features y etiquetas es, sin embargo, offline '
        'por participante: el sistema completo todavía no representa una validación '
        'de inferencia causal en tiempo real.',
        'MLP_current usa dos capas de 24 unidades y lee únicamente la ventana actual. '
        'Comparte entrenamiento y preprocesamiento; su número de parámetros no es '
        'idéntico al de las redes temporales. Es un control de acceso al historial, '
        'no un aislamiento perfecto de todas las diferencias de arquitectura.',
        'No se entrenó MLP_current para los conjuntos reducidos; por ello la '
        'ventaja de BiLSTM con cinco variables frente a la logística no aísla '
        'por sí sola el efecto del historial de las diferencias entre familias.',
        table(['Objetivo','Split','Ventanas','Historia media','Solo ventana actual','Ocho ventanas'],
              [[TASKS[r.task],r.split,r.rows,num(r.mean_history),f'{100*r.singleton_fraction:.1f} %',
                f'{100*r.full_history_fraction:.1f} %'] for r in coverage.itertuples()]),
        'Las métricas sobre ventanas con ocho pasos también están en los CSV con '
        '`scope=history_8`, tanto para los temporales como para los estáticos, sobre '
        'los mismos endpoints. Las tablas principales usan todas las ventanas.',
        '## Entrenamiento y selección',
        'La mediana de imputación, indicadores de ausencia y StandardScaler se ajustan '
        'solo en train para cada conjunto. AdamW usa learning rate 0,001, weight decay '
        '0,0001, batch 256 y recorte del gradiente a norma 1. Se permiten hasta 30 '
        'épocas, mínimo ocho, paciencia seis y mejora mínima 0,0001. Clasificación '
        'usa entropía cruzada ponderada con frecuencias de train; regresión, MSE.',
        'Se conserva por semilla la época con mejor BA macro por participante '
        '(clasificación) o menor MSE macro (regresión) en validación. Luego se elige '
        'arquitectura/conjunto por la media de esas métricas en las dos semillas, '
        'por separado para el panel y para el conjunto completo. Esta selección se '
        'escribe antes de evaluar test. Las redes se ejecutaron en CPU, cuatro hilos, '
        'PyTorch 2.14.0+cpu y algoritmos deterministas.',
        'El baseline de referencia se elige por validación entre Dummy, logística/Ridge '
        'y RF con las mismas entradas; además se reporta la referencia completa. '
        'Los pesos estáticos son los guardados en la etapa anterior. La búsqueda '
        'temporal tiene más configuraciones y épocas que los baselines estáticos '
        'originales: este es un contraste exploratorio, no un estudio con igual '
        'presupuesto de optimización por familia.',
        '## Comparación con entradas completas',
        'BA y R² son métricas globales por ventana. Para las redes se muestra media ± '
        'desviación estándar de dos semillas; esta desviación no es un intervalo '
        'de confianza. La selección se hizo con la métrica macro por participante, '
        'que puede ordenar los modelos de otra manera.']
    for task,title in TASKS.items():
        for kind,kindlabel in KINDS.items():
            column='balanced_accuracy' if kind=='classification' else 'r2'
            rows=[]
            bs=b.loc[b.task.eq(task)&b.kind.eq(kind)&b.subset.eq('full')]
            for model,g in bs.groupby('model'):
                rows.append([model,num(g.loc[g.split.eq('validation'),column].iloc[0]),num(g.loc[g.split.eq('test'),column].iloc[0])])
            ns=m.loc[m.task.eq(task)&m.kind.eq(kind)&m.subset.eq('full')]
            for architecture,g in ns.groupby('architecture'):
                values=[]
                for split in ['validation','test']:
                    v=g.loc[g.split.eq(split),column]
                    values.append(num(v.mean())+' ± '+num(v.std(ddof=1)))
                rows.append([architecture,*values])
            sections += [f'### {title}: {kindlabel}',table(['Modelo','Validación: '+column,'Prueba: '+column],rows)]
    sections += ['## Configuraciones seleccionadas antes de test y diferencias pareadas',
        'Ganancias positivas indican mejora: aumento de BA macro o reducción del '
        'MSE macro por participante. Se promedian primero ambas semillas de cada '
        'participante y se remuestrean los ocho participantes 2.000 veces. Los '
        'intervalos de 95 % son descriptivos, sin corrección por comparaciones '
        'múltiples ni repetición de la partición de sujetos. No prueban causalidad '
        'ni equivalencia. Test ya había sido evaluado en los baselines anteriores; '
        'esta entrega no lo utiliza para seleccionar ni reajustar modelos.']
    rows=[]
    for choice in choices:
        group=matching(gains,choice)
        group=group.loc[group.split.eq('test')&group.reference_scope.eq('matched')].iloc[0]
        values=matching(m,choice)
        column='balanced_accuracy' if choice['kind']=='classification' else 'r2'
        testvalue=values.loc[values.split.eq('test'),column].mean()
        rows.append([TASKS[choice['task']],KINDS[choice['kind']],choice['scope'],choice['architecture'],choice['subset'],
                     num(testvalue),group.baseline,num(group.mean_gain),f'[{num(group.low)}; {num(group.high)}]'])
    sections += [table(['Objetivo','Tarea','Selección','Red','Entradas','BA / R² test','Baseline mismas entradas','Ganancia macro','Intervalo 95 %'],rows),
        'Las diferencias frente al baseline completo y frente al MLP_current están '
        'en `ganancias_vs_baseline.csv`; las contribuciones de cada participante y '
        'semilla están en `ganancias_por_participante.csv`.',
        '## Qué variables explican la diferencia frente al baseline',
        '**`pupil_std_z`, variabilidad de la pupila, destaca en la BiLSTM seleccionada '
        'para clasificación de activación.** En la semilla principal, su importancia '
        'diferencial es 0,0190 en validación y 0,0342 en prueba. En prueba, alterar '
        'esa entrada empeora la BiLSTM en 0,0125 de BA macro y mejora la logística '
        'en 0,0217: ambos efectos explican la diferencia de 0,0342. No es una '
        'contribución aditiva de 3,42 puntos al desempeño del modelo.',
        'El desplazamiento conjunto de todas las entradas pupilares tiene importancia '
        'diferencial negativa en prueba (-0,0049), aunque positiva en validación '
        '(0,0190). La dependencia de una variable aislada no demuestra que toda '
        'la modalidad sostenga una ventaja estable. Para atención, las amplitudes '
        'EEG aparecen en el ranking, con intervalos amplios y sin mejora clara '
        'generalizable del modelo seleccionado.',
        'Se explican los ocho modelos elegidos por validación (panel y completo), '
        'usando la semilla principal 20260907. La sensibilidad entre semillas se '
        'evalúa para desempeño, no para todos los rankings de importancia. Se '
        'desplaza cada feature cruda dentro de participante/grabación/segmento '
        'cinco veces y se reconstruyen las secuencias; las modalidades se desplazan '
        'conjuntamente. Se conservan longitud y endpoint de las secuencias, no las '
        'relaciones con las otras variables. Son perturbaciones diagnósticas, no '
        'nuevas trayectorias fisiológicas observadas.',
        'Se guarda **I temporal**, caída de score del temporal; **I baseline**, '
        'caída del estático; y **I diferencial = I temporal − I baseline**. Esta '
        'última equivale a la ventaja original menos la ventaja tras perturbar. '
        'Un valor positivo indica dependencia relativa del temporal; no prueba '
        'que haya una mejora global si la ventaja original es nula o negativa. '
        'Los scores son BA macro o MSE con signo invertido para que mayor sea mejor.',
        'Las siguientes tablas son diagnóstico post hoc en prueba de los modelos '
        'del panel. No se usaron para elegir features ni volver a entrenar. '
        'Las tablas completas, modalidades y validación quedan en los CSV.']
    for choice in choices:
        if choice['scope']!='panel':continue
        group=matching(importance,choice)
        group=group.loc[group.split.eq('test')&~group.feature.str.startswith('modalidad:')].nlargest(5,'differential_importance')
        sections += [f'### {TASKS[choice["task"]]} · {KINDS[choice["kind"]]} · {choice["architecture"]} / {choice["subset"]}',
            f'Ventaja original frente al baseline, semilla principal: {num(group.gain_before.iloc[0])}.',
            table(['Variable','I temporal','I baseline','I diferencial','Intervalo diferencial'],
                [[r.feature,num(r.temporal_importance),num(r.baseline_importance),num(r.differential_importance),
                  f'[{num(r.differential_low)}; {num(r.differential_high)}]'] for r in group.itertuples()])]
    sections += ['## Dependencia del historial',
        'Dos controles de inferencia conservan la ventana actual: repetirla en '
        'todas las posiciones anteriores y revertir el orden del pasado. La '
        'diferencia positiva indica pérdida al alterar el historial. No son '
        'modelos reajustados y pueden crear entradas fuera de distribución. '
        'Las longitudes se conservan para no confundir el efecto con el inicio '
        'de un segmento. El MLP_current aporta el control entrenado sin historial.',
        table(['Objetivo','Tarea','Entradas','Red','Control','Pérdida macro','Intervalo'],
              [[TASKS[r.task],KINDS[r.kind],r.subset,r.architecture,r.control,num(r.importance),
                f'[{num(r.low)}; {num(r.high)}]'] for r in history.loc[history.split.eq('test')].itertuples()]),
        'Hay controles en que invertir el pasado mejora el resultado. Esto '
        'impide interpretar cualquier ganancia frente al baseline como prueba '
        'automática de que el orden temporal aprendido es útil.',
        '## Límites y continuidad',
        '- Los objetivos son pseudoetiquetas; no hay validación externa del constructo psicológico.\n'
        '- La normalización offline por participante impide afirmar rendimiento en tiempo real.\n'
        '- Ocho ventanas es un contexto inicial fijo, no una longitud óptima demostrada.\n'
        '- Dos semillas y ocho participantes de prueba dan evidencia limitada de estabilidad.\n'
        '- Las variables correlacionadas y las fracciones de calidad pueden afectar el ranking.\n'
        '- No se repitió CV por participante para cada red; se usó el split 25/8/8 ya fijado.\n'
        '- La presente ejecución usa concatenación temprana de features; no completa aún el '
        'contraste de todas las estrategias de fusión de la tesis.',
        'El siguiente estudio debe fijar hipótesis concretas sobre contexto y '
        'fusión, conservar controles de ventana actual y probarlas sin ajustar '
        'decisiones a estos resultados de test. Esta entrega registra las '
        'mejoras observadas y sus límites; no declara confirmada la hipótesis central.',
        '## Archivos, carga y reproducción',
        'Dependencias y ejecución desde la raíz del repositorio:\n\n```powershell\n'
        'python -m pip install -r requirements_temporales.txt\n'
        'python scripts/entrenar_temporales.py\n'
        'python scripts/evaluar_temporales.py\n'
        'python -m unittest discover -s tests\n'
        'python scripts/verificar_temporales.py\n'
        'python scripts/informe_temporales.py\n```',
        'El entrenamiento rechaza una salida existente. Para reproducir sin '
        'sobrescribir esta entrega, usar otra copia limpia del proyecto y una '
        'ruta nueva con `--output`; los scripts posteriores leen la constante '
        '`OUT` de `temporales_core.py`, que debe apuntar a esa nueva ejecución. '
        'El informe requiere Matplotlib 3.11.1 además de las dependencias del '
        'entrenamiento. No se borran ejecuciones anteriores.',
        '- `protocolo.json`: arquitectura, hiperparámetros, entradas, versiones y hashes.\n'
        '- `catalogo_modelos.json`, `preprocesadores.json`, `modelos/`: pesos `.pt`, '
        'metadatos `.json` y preprocesadores `.joblib`.\n'
        '- `seleccion_antes_test.json`, `referencias_estaticas_antes_test.json`: decisiones congeladas.\n'
        '- `historial_entrenamiento.csv`: pérdidas y selección por época.\n'
        '- `metricas_temporales.csv`, `metricas_estaticos_mismas_ventanas.csv`: desempeño comparable.\n'
        '- `predicciones_temporales.csv.gz`: predicciones, probabilidades, split y fila de origen.\n'
        '- `ganancias_vs_baseline.csv`, `ganancias_por_participante.csv`: comparaciones pareadas.\n'
        '- `importancia_vs_baseline.csv`, `importancia_vs_baseline_por_participante.csv`: rankings y diferencias.\n'
        '- `dependencia_del_historial.csv`: controles de historial.\n'
        '- `secuencias_*.csv.gz`, `cobertura_*.csv`: historial disponible por endpoint.\n'
        '- `verificacion_entrega.json`, `pruebas.txt`: auditoría y resultados de pruebas.',
        'Ejemplo de carga de un modelo propio, desde la raíz del repositorio:\n\n```python\n'
        'import sys, json, joblib\nsys.path.insert(0, "scripts")\n'
        'from temporales_core import OUT, load_net, history_indices, sequence_array, raw_predict, decode\n'
        'catalog = json.loads((OUT / "catalogo_modelos.json").read_text(encoding="utf-8"))\n'
        'meta = catalog[0]  # elegir por task, kind, subset, architecture y seed\n'
        'model = load_net(meta)\nprep = joblib.load(OUT / meta["preprocessor"])\n'
        '# frame: ventanas cronologicas con identidad, split y las features originales\n'
        'indices, lengths = history_indices(frame, meta["context_windows"])\n'
        'x = sequence_array(prep.transform(frame[meta["features"]]), indices)\n'
        'prediction = decode(raw_predict(model, x, lengths), meta["kind"])\n```',
        '## Verificación',
        f'{audit["tests_passed"]} pruebas aprobadas. Se verificaron {audit["models_verified"]} '
        f'modelos, {audit["predictions_verified"]:,} predicciones, '
        f'{audit["metrics_recomputed"]} métricas globales recalculadas y '
        f'{audit["importance_identities_verified"]} identidades de importancia diferencial. '
        'Los pesos recargados reproducen exactamente los logits/scores de validación. '
        'Se auditó que las secuencias no crucen personas, segmentos, estímulos ni huecos '
        'y que nunca incorporen ventanas posteriores al endpoint.',
        '## Referencias',
        '[Bai, Kolter y Koltun (2018)](https://arxiv.org/abs/1803.01271) describen las TCN '
        'residuales con convoluciones causales dilatadas usadas como referencia arquitectónica. '
        'Esta implementación pequeña no replica sus benchmarks.',
        '[Documentación de LSTM de PyTorch](https://docs.pytorch.org/docs/2.14/generated/torch.nn.modules.rnn.LSTM.html) '
        'especifica los estados finales bidireccionales empleados aquí; '
        '[guardado y carga](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html) '
        'documenta la persistencia mediante state_dict.']
    plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(1,2,figsize=(12,5),layout='constrained')
    for ax,(task,title) in zip(axes,TASKS.items()):
        labels=[];values=[];errors=[]
        for arch in ['TCN','LSTM','BiLSTM','MLP_current']:
            v=m.loc[m.task.eq(task)&m.kind.eq('classification')&m.subset.eq('full')&m.architecture.eq(arch)&m.split.eq('test'),'balanced_accuracy']
            labels.append(arch);values.append(v.mean());errors.append(v.std(ddof=1))
        for name in ['dummy_prior','logistic','random_forest']:
            v=b.loc[b.task.eq(task)&b.kind.eq('classification')&b.subset.eq('full')&b.model.eq(name)&b.split.eq('test'),'balanced_accuracy']
            labels.append(name);values.append(v.iloc[0]);errors.append(0)
        ax.errorbar(values,np.arange(len(labels)),xerr=errors,fmt='o',color='#145875',capsize=3)
        ax.set_yticks(np.arange(len(labels)),labels);ax.set_xlim(.29,.39);ax.axvline(1/3,color='#999',ls='--')
        ax.set_title(title);ax.set_xlabel('Balanced accuracy global en prueba');ax.grid(axis='x',alpha=.2)
    fig.suptitle('Entradas completas · media y desviación de dos semillas para redes',fontsize=12)
    for ext in ['png','pdf']:fig.savefig(OUT/f'comparacion_temporales.{ext}',dpi=180)
    plt.close(fig)
    fig,axes=plt.subplots(2,2,figsize=(14,9),layout='constrained')
    for row,task in enumerate(TASKS):
        for col,kind in enumerate(KINDS):
            choice=next(c for c in choices if c['task']==task and c['kind']==kind and c['scope']=='panel')
            group=matching(importance,choice)
            group=group.loc[group.split.eq('test')&~group.feature.str.startswith('modalidad:')].nlargest(5,'differential_importance').sort_values('differential_importance')
            ax=axes[row,col];yy=np.arange(len(group))
            ax.hlines(yy,group.differential_low,group.differential_high,color='#64748b')
            ax.scatter(group.differential_importance,yy,color='#145875');ax.axvline(0,color='#999',ls='--')
            ax.set_yticks(yy,group.feature);ax.grid(axis='x',alpha=.2)
            ax.set_title(f'{TASKS[task]} · {KINDS[kind]} · {choice["architecture"]}\nVentaja original (semilla principal): {num(group.gain_before.iloc[0])}')
            ax.set_xlabel('Importancia diferencial (BA macro)' if kind=='classification' else 'Importancia diferencial (reducción MSE)')
    fig.suptitle('Dependencia relativa frente al baseline · diagnóstico post hoc de prueba\nIntervalos descriptivos 95 %, ocho participantes, semilla principal',fontsize=12)
    for ext in ['png','pdf']:fig.savefig(OUT/f'variables_ventaja_baseline.{ext}',dpi=180)
    plt.close(fig)
    sections.insert(6,'![Comparación de modelos](../resultados/temporales_07-09-2026/comparacion_temporales.png)')
    sections += ['![Importancia diferencial](../resultados/temporales_07-09-2026/variables_ventaja_baseline.png)']
    REPORT.write_text('\n\n'.join(sections)+'\n',encoding='utf-8')
    print(REPORT)


if __name__=='__main__':main()
