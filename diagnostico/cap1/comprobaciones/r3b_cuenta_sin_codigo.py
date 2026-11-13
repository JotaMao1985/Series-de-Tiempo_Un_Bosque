"""R3b · variante de cuenta_cap1_v2.py que SI quita los bloques <pre> antes de contar (la original no los quita,
y ademas el `$` de un `x$y` del codigo se empareja con el de una formula y se come la prosa que hay entre los dos).
Cuenta palabras de prosa por modulo del capitulo 1 (sin codigo, sin marcado, sin matematicas display).
Uso: python3 -I cuenta_cap1_v2.py ruta.html"""
import re, html, sys
src = open(sys.argv[1], encoding='utf-8').read()
decl = {int(k): int(v) for k, v in re.findall(r'\{ id: (\d+), title: "[^"]*", shortTitle: "[^"]*", duration: "(\d+) min" \}', src)}
INLINE = r'(?:code|strong|em|a|span|cite|sub|sup|i|b|kbd)'
def texto(h):
    h = re.sub(r"<pre\b.*?</pre>", " ", h, flags=re.S)
    h = re.sub(r'<(script|style|canvas|svg)\b.*?</\1>', ' ', h, flags=re.S)
    h = re.sub(r'<aside class="fuentes-modulo".*?</aside>', ' ', h, flags=re.S)
    h = re.sub(r'<caption class="sr-only".*?</caption>', ' ', h, flags=re.S)
    h = re.sub(r'<button\b.*?</button>', ' ', h, flags=re.S)      # botones de derivacion/pistas/pestañas
    h = re.sub(r'<div class="quiz".*?<div class="quiz-marcador">.*?</div>\s*</div>', ' ', h, flags=re.S)
    h = re.sub(r'<(/?)' + INLINE + r'\b[^>]*>', '', h)             # inline: se pegan al texto
    h = re.sub(r'<[^>]+>', ' ', h)                                 # el resto separa
    h = html.unescape(h).replace('\xa0', ' ')
    h = h.replace('$seasonal', 'seasonal')
    h = re.sub(r'\$\$.*?\$\$', ' ', h, flags=re.S)
    h = re.sub(r'\$[^$]*\$', ' M ', h)                             # inline = 1 token
    return h
def n(h): return len(texto(h).split())
print('M | prosa | deriv | sims | mapa | ciclo | codeTabs | preSueltos | min lectura | min formula | min c/deriv | declarado')
tot = 0; totd = 0
filas = []
for m in re.finditer(r'<template id="module-(\d+)">(.*?)</template>', src, re.S):
    k = int(m.group(1)); h = m.group(2)
    ders = re.findall(r'<div class="derivacion-panel".*?</p>\s*</div>', h, flags=re.S)
    h_sin = h
    for d in ders: h_sin = h_sin.replace(d, ' ')
    # pre sueltos = pre fuera de code-tabs
    tabs = len(re.findall(r'<div class="code-tabs"', h_sin))
    pre_sueltos = len(re.findall(r'<pre\b', h_sin)) - 2*tabs
    sims = len(re.findall(r'data-simulador=', h)); mapas = len(re.findall(r'data-mapa=', h)); ciclos = len(re.findall(r'data-ciclo=', h))
    w = n(h_sin); wd = sum(n(d) for d in ders)
    lect = w/180; form = lect + 3*sims + 2*(tabs+pre_sueltos); formd = form + wd/180
    filas.append((k,w,wd,sims,mapas,ciclos,tabs,pre_sueltos,lect,form,formd,decl[k]))
    tot += form; totd += formd
    print(f'M{k} | {w} | {wd} | {sims} | {mapas} | {ciclos} | {tabs} | {pre_sueltos} | {lect:.1f} | {form:.1f} | {formd:.1f} | {decl[k]}')
print('TOTAL formula', round(tot,1), 'con derivaciones', round(totd,1), 'declarado', sum(decl.values()))
