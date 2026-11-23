# Tema visual tipo Beamer (barra lateral y franja superior azules), pedido por Mario el 23-11-2026.
# Se aplica al final, sobre los estilos de estilo_tecnico.py y relato.py.
AZUL='#3333b3';OSCURO='#262686'
CSS='''
body{background:#e6e6ea;font-family:Helvetica,Arial,sans-serif}
.slide{padding:140px 46px 40px 216px;border:0;background:#fff}
.slide:before{content:'';display:block;position:absolute;left:0;right:0;top:0;height:112px;background:#3333b3}
.bside{position:absolute;left:0;top:0;bottom:0;width:172px;background:#3333b3;color:#fff;padding:136px 14px 20px;text-align:center;font-size:15px;line-height:1.3;z-index:1}
.bside:before{content:'';position:absolute;left:0;top:0;width:172px;height:112px;background:#262686}
.bside b{display:block;font-weight:400;font-size:16px}.bside i{display:block;font-style:normal;color:#b9b9ea;margin:14px 0 26px}
.bside ul{list-style:none;margin:0;padding:0}.bside li{color:#a9a9e4;font-size:13.5px;line-height:1.25;margin:0 0 11px}.bside li.on{color:#fff;font-weight:700}
.slide .chapter{position:absolute;left:216px;top:17px;height:auto;margin:0;color:#c9c9ee;font-size:12px;letter-spacing:1.4px;font-weight:400;z-index:1}
.slide h1{position:absolute;left:216px;right:46px;top:36px;height:68px;display:flex;align-items:center;margin:0;max-width:none;color:#fff;font-family:Helvetica,Arial,sans-serif;font-size:30px;line-height:1.14;letter-spacing:0;font-weight:400;z-index:1}
.slide h3{color:#3333b3}.folio{color:#8a8aa0;right:26px;bottom:16px}
th{color:#3333b3;border-bottom:2px solid #3333b3}table td:first-child{color:#262686}
.data-figure img{height:380px}.data-figure figcaption{border-top:1px solid #d5d5ee}
.takeaway,.next-step{background:#ebebf7;border:0;border-left:5px solid #3333b3;border-radius:4px;padding:12px 16px}
.slide.story-cover .chapter{color:#fff;font-size:14px;top:48px}
.slide.story-cover h1{position:relative;left:auto;right:auto;top:auto;height:auto;display:block;margin:80px 0 46px;padding:28px 30px;background:#3333b3;border-radius:14px;box-shadow:7px 8px 12px #00000055;text-align:center;font-size:40px;line-height:1.2}
.story-cover .cover-sub{text-align:center;color:#222;font-size:26px}
.story-cover .byline{display:block;border:0;text-align:center;margin-top:44px;width:auto;color:#111}.story-cover .byline b{display:block;font-weight:400;font-size:30px;margin-bottom:22px}.story-cover .byline span{display:block;font-size:22px;line-height:1.5}
#progress{background:#3333b3}
.slide *,.slide *:before{font-family:Helvetica,Arial,sans-serif!important}
.compact td{padding-top:11px;padding-bottom:11px;font-size:21px}
@media(max-width:650px){.reading .bside,.reading .slide:before{display:none}.reading .slide{padding:14px 14px 30px}.reading .slide .chapter{position:static;color:#3333b3;margin-bottom:8px}.reading .slide h1,.reading .slide.story-cover h1{position:static;display:block;height:auto;background:#3333b3;padding:12px 14px;margin:0 0 16px;font-size:22px;border-radius:6px}}
@media print{.bside,.slide:before{-webkit-print-color-adjust:exact;print-color-adjust:exact}.slide h1{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
'''
def recolor(css):
 for old in ('#145ac7','#1559a6','#185bac'):css=css.replace(old,AZUL)
 return css
