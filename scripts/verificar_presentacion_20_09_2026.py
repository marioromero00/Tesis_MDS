"""Auditoría del HTML breve. Requiere Playwright, Edge, PyMuPDF y axe-core 4.10.3.

Colocar axe.min.js en %TEMP%/mds-presentation-audit/ antes de ejecutar.
Capturas y PDF de comprobación se guardan en el directorio temporal.
"""
import csv
import hashlib
import json
import os
import shutil
from collections import Counter
from pathlib import Path

import pymupdf
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / 'presentaciones/Presentacion-Tema-Tesis-Autocontenida-20-09-2026.html'
TEMP = Path(os.environ['TEMP']) / 'mds-presentation-20-09-2026'
TEMP.mkdir(exist_ok=True)
AXE = TEMP.parent / 'mds-presentation-audit/axe.min.js'
report = {'date': '2026-09-20', 'html_sha256': hashlib.sha256(HTML.read_bytes()).hexdigest(), 'checks': [], 'axe': []}

def check(name, ok):
    report['checks'].append({'name': name, 'passed': bool(ok)})
    assert ok, name

def luminance(h):
    c = [int(h[i:i+2], 16)/255 for i in (1, 3, 5)]
    c = [x/12.92 if x <= .04045 else ((x+.055)/1.055)**2.4 for x in c]
    return sum(x*w for x,w in zip(c, [.2126,.7152,.0722]))

report['contrast'] = []
for fg in ['#12243b','#46556b','#003d73','#09686b']:
    for bg in ['#ffffff','#eff4f9']:
        ratio = (luminance(bg)+.05)/(luminance(fg)+.05)
        report['contrast'].append({'foreground':fg,'background':bg,'ratio':round(ratio,2)})
check('Contraste de texto >= 4.5', all(x['ratio'] >= 4.5 for x in report['contrast']))
with (ROOT/'resultados/modelado/particion_participantes.csv').open(encoding='utf-8') as f:
    splits = Counter(r['split'] for r in csv.DictReader(f))
check('Particion 25/8/8, seis excluidos y sensibilidad', sorted(splits.values()) == [1,6,8,8,25])
with (ROOT/'resultados/preprocesamiento/caracteristicas_multimodales.csv').open(encoding='utf-8') as f:
    reader = csv.reader(f)
    check('Tabla de 59 columnas', len(next(reader)) == 59)
    check('25992 ventanas', sum(1 for _ in reader) == 25992)

copy = TEMP / 'presentacion.html'
shutil.copyfile(HTML, copy)
with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    context = browser.new_context(offline=True, viewport={'width':1440,'height':900})
    page = context.new_page()
    errors, requests = [], []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('request', lambda r: requests.append(r.url))
    page.goto(copy.as_uri())
    check('Autocontenida sin recursos externos', page.locator('[src],link[href],a[href]:not([href^="#"])').count() == 0)
    check('Seis diapositivas, una visible', page.locator('.slide').count() == 6 and page.locator('.slide:visible').count() == 1)
    page.keyboard.press('ArrowRight')
    check('Flecha siguiente', page.locator('#status').inner_text() == '2 / 6')
    page.keyboard.press('End')
    check('Fin', page.locator('#s6').is_visible())
    page.keyboard.press('Home')
    check('Inicio', page.locator('#s1').is_visible())
    page.locator('#jump').select_option('3')
    check('Selector', page.locator('#s4').is_visible())
    page.locator('#all').click()
    check('Lectura continua', page.locator('.slide:visible').count() == 6)
    page.add_script_tag(path=str(AXE))
    for w,h in [(1440,900),(720,450),(320,700)]:
        page.set_viewport_size({'width':w,'height':h})
        check(f'Sin desborde horizontal {w}', page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
        r = page.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return {version:axe.version,violations:r.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)})),incomplete:r.incomplete.map(v=>v.id)}}")
        report['axe'].append({'width':w,**r})
        check(f'axe sin violaciones {w}', not r['violations'])
    page.add_style_tag(content='p,li{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important}p{margin-bottom:2em!important}')
    check('Texto espaciado sin desborde', page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
    page.reload()
    page.set_viewport_size({'width':1440,'height':900})
    for i in range(6):
        page.locator('#jump').select_option(str(i))
        page.screenshot(path=str(TEMP/f'slide-{i+1}.png'), full_page=True)
    page.set_viewport_size({'width':320,'height':700})
    page.screenshot(path=str(TEMP/'mobile.png'), full_page=True)
    page.set_viewport_size({'width':1440,'height':900})
    page.emulate_media(media='print')
    check('Impresion de seis diapositivas', page.locator('.slide:visible').count() == 6)
    page.pdf(path=str(TEMP/'presentacion.pdf'), prefer_css_page_size=True, print_background=True)
    doc = pymupdf.open(TEMP/'presentacion.pdf')
    check('PDF seis paginas completas', len(doc) == 6 and all(len(x.get_text())>200 for x in doc))
    page.emulate_media(media='screen', reduced_motion='reduce')
    page.locator('#jump').select_option('2')
    page.locator('#prev').focus()
    focus = []
    for _ in range(4):
        page.keyboard.press('Tab')
        focus.append(page.evaluate('document.activeElement.id'))
        check('Indicador foco ' + focus[-1], page.evaluate('getComputedStyle(document.activeElement).outlineStyle') != 'none')
    check('Orden teclado de controles', focus == ['next','jump','all','print'])
    page.keyboard.press('Shift+Tab')
    check('Retroceso de foco', page.evaluate('document.activeElement.id') == 'all')
    page.locator('#all').focus()
    page.keyboard.press('Space')
    check('Espacio activa lectura', page.locator('.slide:visible').count() == 6)
    page.keyboard.press('Space')
    check('Espacio vuelve al deck', page.locator('.slide:visible').count() == 1)
    check('Sin errores JavaScript', not errors)
    check('Cero peticiones HTTP', not any(x.startswith('http') for x in requests))
    nojs = browser.new_page(java_script_enabled=False)
    nojs.goto(copy.as_uri())
    check('Contenido completo sin JavaScript', nojs.locator('.slide:visible').count() == 6)
    browser.close()
report['limitations'] = ['Sin lector de pantalla real.', '720 px aproxima reflujo al 200%; no se opero el zoom manual del navegador.', 'La auditoria no certifica cumplimiento integral de WCAG.']
(ROOT/'documentacion/Verificacion_Presentacion_Tema_20-09-2026.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':len(report['checks']),'screenshots':str(TEMP)}))
