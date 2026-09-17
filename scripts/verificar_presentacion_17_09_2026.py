"""Verifica el HTML sin modificar experimentos. Requiere playwright y Edge."""
import csv
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / 'presentaciones/Avances-Tesis-MDS-17-09-2026.html'
TEMP = Path(os.environ['TEMP']) / 'mds-presentation-audit'
TEMP.mkdir(exist_ok=True)
REPORT = ROOT / 'documentacion/Verificacion_Presentacion_17-09-2026.json'
report = {'date': '2026-09-17', 'checks': [], 'axe': [], 'limitations': ['Sin prueba con lector de pantalla real. La auditoria no certifica cumplimiento WCAG completo.']}
def check(name, condition):
    report['checks'].append({'name': name, 'passed': bool(condition)})
    assert condition, name

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(HTML.as_uri())
    check('14 diapositivas', page.locator('.slide').count() == 14)
    check('Primera visible', page.locator('.slide:visible').count() == 1)
    page.keyboard.press('ArrowRight')
    check('Flecha siguiente', page.locator('#status').inner_text() == '2 / 14')
    page.keyboard.press('End')
    check('Fin', page.locator('#status').inner_text() == '14 / 14')
    page.keyboard.press('Home')
    page.locator('#jump').select_option('6')
    check('Selector', page.locator('#s7').is_visible())
    page.locator('#all').click()
    check('Lectura continua', page.locator('.slide:visible').count() == 14)
    page.add_script_tag(path=str(TEMP / 'axe.min.js'))
    for width, height in [(1440,900), (720,450), (320,700)]:
        page.set_viewport_size({'width': width, 'height': height})
        check(f'Sin desborde a {width}px', page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
        result = page.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return {version:axe.version,violations:r.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)})),incomplete:r.incomplete.map(v=>v.id)}}")
        report['axe'].append({'width': width, **result})
        check(f'axe sin violaciones a {width}px', not result['violations'])
    page.add_style_tag(content='p{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important;margin-bottom:2em!important}')
    check('Espaciado ampliado sin desborde', page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
    page.reload()
    page.set_viewport_size({'width':1440,'height':900})
    for index in [0,4,7,12]:
        page.locator('#jump').select_option(str(index))
        page.screenshot(path=str(TEMP / f'slide-{index+1}.png'), full_page=True)
    page.set_viewport_size({'width':320,'height':700})
    page.locator('#jump').select_option('4')
    page.screenshot(path=str(TEMP / 'mobile.png'), full_page=True)
    page.set_viewport_size({'width':1440,'height':900})
    page.emulate_media(media='print')
    check('Impresion incluye 14', page.locator('.slide:visible').count() == 14)
    page.pdf(path=str(TEMP/'presentacion.pdf'), prefer_css_page_size=True, print_background=True)
    page.emulate_media(media='screen', reduced_motion='reduce')
    page.locator('#all').click()
    page.locator('#prev').focus()
    focus = []
    for _ in range(13):
        page.keyboard.press('Tab')
        focus.append(page.evaluate('document.activeElement.tagName'))
    check('Tab alcanza fuentes', 'A' in focus)
    check('Foco visible definido', ':focus-visible' in HTML.read_text(encoding='utf-8'))
    check('Sin errores JavaScript', not errors)
    check('Enlaces relativos existen', all((HTML.parent / href).resolve().exists() for href in page.locator('a[href^="../"]').evaluate_all('(els)=>els.map(e=>e.getAttribute("href"))')))
    text = HTML.read_text(encoding='utf-8')
    with (ROOT/'resultados/grids_recurrentes_13-09-2026/resumen.csv').open() as f:
        for row in csv.DictReader(f):
            if row['family'] == row['scope']:
                check(f"BA {row['family']} coincide CSV", f"{float(row['ba_macro']):.4f}".replace('.',',') in text)
    nojs = browser.new_page(java_script_enabled=False)
    nojs.goto(HTML.as_uri())
    check('Sin JavaScript se lee todo', nojs.locator('.slide:visible').count() == 14)
    browser.close()
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'passed':len(report['checks']), 'report':str(REPORT), 'screenshots':str(TEMP)}))
