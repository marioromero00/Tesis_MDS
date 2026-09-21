"""Genera cinco láminas HTML autocontenidas usando los resultados guardados."""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT/'presentaciones/Avances-Resumen-Autocontenido-21-09-2026.html'
base = (ROOT/'presentaciones/Presentacion-Tema-Tesis-Autocontenida-20-09-2026.html').read_text(encoding='utf-8')
def rows(path):
    with (ROOT/path).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))
def number(value, digits=4):
    return f'{float(value):.{digits}f}'.replace('.',',')
neural = {r['family']:float(r['ba_macro']) for r in rows('resultados/grids_recurrentes_13-09-2026/resumen.csv') if r['family']==r['scope']}
ablations = {r['variant']:r for r in rows('resultados/ablacion_pca_12-09-2026/resumen_ablaciones.csv')}
contrasts = {r['family']:r for r in rows('resultados/grids_recurrentes_13-09-2026/contrastes.csv') if r['family']==r['scope'] and r['reference']=='Control_repetido'}
# La referencia de Transformer se recupera del contraste auditado contra TCN.
tc = next(r for r in rows('resultados/grids_recurrentes_13-09-2026/contrastes.csv') if r['scope']=='TCN' and r['reference']=='Transformer grid')
transformer = neural['TCN']-float(tc['delta'])
models = [('Ridge de referencia',float(ablations['reference']['macro_score']),5),('TCN',neural['TCN'],4),('Transformer',transformer,4),('BiLSTM',neural['BiLSTM'],4),('LSTM',neural['LSTM'],4)]
bars = ''.join(f'<div class="barrow"><span>{name}</span><div class="track" aria-hidden="true"><div class="fill" style="width:{score/.5*100:.4f}%"></div></div><b>{number(score,digits)}</b></div>' for name,score,digits in models)
def pp(v):
    return f'{float(v)*100:+.2f}'.replace('.',',').replace('-', '−')
controls = ''.join(f'<tr><th scope="row">{name}</th><td>{pp(contrasts[name]["delta"])}</td><td>[{pp(contrasts[name]["ci_low"])}; {pp(contrasts[name]["ci_high"])}]</td></tr>' for name in ['BiLSTM','LSTM','TCN'])
content = f'''
<main id="contenido" tabindex="-1">
<section class="slide" aria-labelledby="s1" data-title="Avance completado">
<p class="eyebrow">Tesis MDS · Mario Romero · 21 septiembre 2026</p>
<h1 id="s1">Avances en modelos temporales y selección de variables</h1>
<p class="lead">Se completaron los grids y las auditorías; todavía no hay una mejora estable sobre Ridge.</p>
<div class="triple metrics-cards"><article><b>32</b><p>configuraciones por familia</p></article><article><b>1.980</b><p>modelos y checkpoints guardados*</p></article><article><b>66</b><p>pruebas aprobadas*</p></article></div>
<p class="note">Foco reciente: <strong>activación (arousal)</strong>. 25 personas de train, cinco folds y dos semillas externas en los grids. Etiquetas fijas; señales del Modelo Profesor excluidas del estudiante.</p>
<p class="source">Experimentos cerrados al 14-09-2026. *BiLSTM, LSTM y TCN; el grid de Transformer se documentó por separado. Fuente: informe Grid_BiLSTM_LSTM_TCN_13-09-2026.</p>
</section>
<section class="slide" aria-labelledby="s2" data-title="Resultados de los grids">
<p class="eyebrow">Activación · comparación fuera del ajuste</p><h2 id="s2">Ningún grid neuronal supera a Ridge</h2>
<figure><figcaption>Balanced accuracy (BA) macro por participante · mayor es mejor</figcaption><div class="bars">{bars}</div><div class="axis" aria-hidden="true"><span>0</span><span>Meta: 0,50</span></div></figure>
<p class="note">La meta 0,50 sigue pendiente. Ridge usa representaciones temporales seleccionadas por fold; no es un baseline puramente estático.</p>
<p class="source">BA: promedio de recalls de las clases presentes por persona, luego promedio entre personas. Constante bajo/alto: 0,3467. Fuentes: resúmenes de los grids recurrentes, Transformer y ablación.</p>
</section>
<section class="slide" aria-labelledby="s3" data-title="Aporte temporal">
<p class="eyebrow">Control del historial</p><h2 id="s3">La ventaja temporal de TCN sigue siendo incierta</h2>
<table><caption>Historia real menos ventana actual repetida · ambos conservan suavizado</caption><thead><tr><th scope="col">Modelo</th><th scope="col">Ganancia BA (pp)</th><th scope="col">IC 95 % (pp)</th></tr></thead><tbody>{controls}</tbody></table>
<div class="question"><strong>La clase media sigue siendo difícil:</strong> recall de 14,5–17,5 % en los cuatro grids, frente a 23,3 % con Ridge.</div>
<p class="source">pp = puntos porcentuales. Control reentrenado con igual configuración. IC descriptivos: bootstrap pareado por persona, 2.000 remuestreos, sin corrección por múltiples búsquedas. Fuentes: contrastes y diagnóstico por clase.</p>
</section>
<section class="slide" aria-labelledby="s4" data-title="Ablación y PCA">
<p class="eyebrow">Acotar el problema · resultados de Ridge</p><h2 id="s4">La reducción de variables requiere confirmación</h2>
<div class="triple findings"><article class="panel"><h3>EEG aporta</h3><p class="score">{number(ablations['without_eeg']['macro_score'])}</p><p>BA al quitar EEG: cae 2,02 pp.</p><p class="small">Solo EEG: BA similar, pero el recall medio cae a 10,8 %.</p></article><article class="panel teal"><h3>Sin conteo de fijaciones</h3><p class="score">{number(ablations['drop_fixation_count']['macro_score'])}</p><p>Mayor BA observada en la ablación.</p><p class="small">Máximo exploratorio entre 24 eliminaciones; pendiente de confirmación.</p></article><article class="panel"><h3>PCA al 90 %</h3><p class="score">{number(ablations['pca_0.9']['macro_score'])}</p><p>13–45 componentes según el fold.</p><p class="small">Comprime las características sin una mejora clara.</p></article></div>
<p class="note">Aporte predictivo condicionado al modelo. Estos resultados no establecen importancia fisiológica ni causalidad.</p>
<p class="source">Fuente: Ablacion_PCA_12-09-2026. Referencia BA 0,37475; recall medio 23,3 %. Los componentes PCA corresponden a variables transformadas, no a sensores.</p>
</section>
<section class="slide" aria-labelledby="s5" data-title="Conclusión y próximos pasos">
<p class="eyebrow">Conclusión y propuesta de continuidad</p><h2 id="s5">El siguiente paso es confirmar hipótesis acotadas</h2>
<ol class="nextsteps"><li><strong>Revisar la clase media</strong><span>Analizar separabilidad y estabilidad de las pseudoetiquetas.</span></li><li><strong>Predefinir pocos paneles</strong><span>Comparar entradas completas y reducidas, seleccionadas dentro del ajuste.</span></li><li><strong>Congelar la evaluación</strong><span>Acordar el protocolo confirmatorio antes de volver a evaluar.</span></li></ol>
<p class="note"><strong>Balance:</strong> modelos reproducibles y evidencia para acotar la búsqueda; la hipótesis temporal aún no se confirma.</p>
<p class="source">Pasos propuestos, no ejecutados. Muchas búsquedas sobre las mismas 25 personas: balance exploratorio y offline. Sin nueva evaluación de validation/test en estas rondas; atención no se reentrenó en los últimos grids.</p>
</section>
</main>'''
style = '''
.lead{font-size:25px;line-height:1.45;max-width:62ch;margin:0 0 30px}h1{max-width:29ch}.metrics-cards{margin:6px 0 24px}.metrics-cards article{border-top:3px solid var(--teal);padding:16px 0}.metrics-cards b{font-size:43px;line-height:1.2;color:var(--blue)}.metrics-cards p{font-size:17px;margin:6px 0}.bars{display:grid;gap:17px;margin-top:22px}.barrow{display:grid;grid-template-columns:215px 1fr 100px;gap:18px;align-items:center;font-size:21px}.barrow b{font-variant-numeric:tabular-nums}.track{height:27px;background:var(--soft);border-right:2px dashed var(--muted)}.fill{height:100%;background:var(--blue)}.axis{display:flex;justify-content:space-between;margin:10px 118px 26px 233px;font-size:13px;color:var(--muted)}figure{margin:0}figcaption{font-size:16px;color:var(--muted)}.findings{margin:10px 0 20px}.findings .score{font-size:35px;font-weight:700;color:var(--blue);margin:18px 0}.findings h3{font-size:20px}.findings p{font-size:18px}.findings .small{font-size:16px}.nextsteps{list-style:none;counter-reset:next;padding:0;display:grid;gap:19px}.nextsteps li{counter-increment:next;display:grid;grid-template-columns:38px 1fr;gap:0 14px;border-bottom:1px solid var(--line);padding-bottom:15px}.nextsteps li::before{content:counter(next);color:var(--teal);font-size:28px;font-weight:700;grid-row:span 2}.nextsteps strong{font-size:22px}.nextsteps span{font-size:19px;color:var(--muted)}
@media(max-width:760px){.barrow{grid-template-columns:1fr 87px;gap:5px 10px;font-size:17px}.barrow>span{grid-column:1}.barrow .track{grid-column:1}.barrow b{grid-column:2;grid-row:span 2}.axis{margin:8px 97px 22px 0}.lead{font-size:21px}.metrics-cards{gap:0}.metrics-cards article{padding:12px 0}.nextsteps strong{font-size:20px}.nextsteps span{font-size:17px}.question{font-size:20px}}
@media print{.lead{font-size:20px}.metrics-cards b{font-size:34px}.metrics-cards p{font-size:15px}.bars{gap:12px}.barrow{font-size:17px}.track{height:22px}.findings p{font-size:16px}.findings .small{font-size:13px}.findings .score{font-size:28px}.nextsteps strong{font-size:19px}.nextsteps span{font-size:16px}.source{font-size:10px}.note{font-size:14px}}
'''
base = re.sub(r'<main id="contenido".*?</main>',content,base,flags=re.S)
base = base.replace('</style>',style+'\n</style>')
base = re.sub(r'<title>.*?</title>','<title>Avances de tesis MDS · Resumen en cinco diapositivas</title>',base)
base = re.sub(r'<meta name="description"[^>]+>','<meta name="description" content="Cinco diapositivas sobre grids temporales, controles, ablación, PCA y próximos pasos.">',base)
DEST.write_text(base,encoding='utf-8',newline='\n')
print(DEST.name)
