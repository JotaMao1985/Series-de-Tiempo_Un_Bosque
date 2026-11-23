"""Diagnóstico cap. 5 · carga de lectura por módulo y dónde aparece la primera tarea.

    python3 diagnostico/cap5/diag/ejercicios_carga.py > diagnostico/cap5/diag/ejercicios_carga.out

Adaptado de diagnostico/cap4/diag/ejercicios_carga.py. Por módulo: palabras de prosa
(sin <pre>, sin <script>, sin comentarios, fórmulas en bloque como una palabra), líneas
de código, simuladores, bloques code-tabs, duración declarada en courseData y minutos a
150 y 200 palabras por minuto. Luego, las tareas: el primer `data-quiz`, los
`ejercicio-guiado`, «Para practicar», y las consignas imperativas de los simuladores.
"""
import re, pathlib
raiz = pathlib.Path(__file__).resolve().parents[3]
html = (raiz / 'Htmls_Series/capitulo-5-sarima.html').read_text(encoding='utf8')
L = html.split('\n')

ini = [i for i, l in enumerate(L) if re.search(r'<template id="module-\d+">', l)]
fin = [i for i, l in enumerate(L) if '</template>' in l]
dur = {int(m.group(1)): int(m.group(2)) for m in re.finditer(r'\{ id: (\d+), title: "[^"]*", shortTitle: "[^"]*", duration: "(\d+) min"', html)}

def prosa(trozo):
    t = re.sub(r'<!--.*?-->', ' ', trozo, flags=re.S)
    t = re.sub(r'<pre.*?</pre>', ' ', t, flags=re.S)
    t = re.sub(r'<script.*?</script>', ' ', t, flags=re.S)
    t = re.sub(r'\$\$.*?\$\$', ' FORMULA ', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    return t
pal = lambda t: len(re.findall(r'[A-Za-zÁÉÍÓÚáéíóúñÑü]+', prosa(t)))

print(f"{'Mód':>3} {'líneas':>11} {'palabras':>8} {'código':>6} {'simul':>5} {'tabs':>4} {'dur.decl':>8} {'min@150':>7} {'min@200':>7}")
filas = []
for k, a in enumerate(ini, start=1):
    b = next(f for f in fin if f > a)
    trozo = '\n'.join(L[a:b + 1])
    palabras = pal(trozo)
    codigo = sum(len(p.split('\n')) for p in re.findall(r'<pre.*?</pre>', trozo, flags=re.S))
    sims = len(re.findall(r'data-simulador="', trozo))
    tabs = len(re.findall(r'class="code-tabs', trozo))
    filas.append((k, a + 1, b + 1, palabras, codigo, sims))
    print(f"{k:>3} {a+1:>5}-{b+1:<5} {palabras:>8} {codigo:>6} {sims:>5} {tabs:>4} {dur.get(k, 0):>8} {palabras/150:>7.1f} {palabras/200:>7.1f}")

q = next(i for i, l in enumerate(L) if 'data-quiz="cap5"' in l) + 1
ej = [i + 1 for i, l in enumerate(L) if 'class="ejercicio-guiado"' in l]
pp = [i + 1 for i, l in enumerate(L) if 'Para practicar' in l]
xl = [i + 1 for i, l in enumerate(L) if '.xlsx' in l]
m11 = filas[10]
antes_quiz = pal('\n'.join(L[m11[1] - 1:q - 1]))
tot_m1_m10 = sum(f[3] for f in filas[:10])
print(f"\nPrimera tarea con respuesta comprobable: quiz cap5 en la línea {q} (M11); ejercicios en {ej}")
print(f"«Para practicar» en el capítulo: {len(pp)} {pp}")
print(f"Enlaces al Excel: líneas {xl}")
print(f"Prosa antes de esa tarea: M1-M10 {tot_m1_m10} palabras + M11 hasta el quiz {antes_quiz} = {tot_m1_m10 + antes_quiz}")
print(f"  a 150 ppm: {(tot_m1_m10 + antes_quiz)/150:.0f} min; a 200 ppm: {(tot_m1_m10 + antes_quiz)/200:.0f} min")
print(f"  duración declarada M1-M10: {sum(dur[k] for k in range(1, 11))} min; M11 entero: {dur[11]} min")
print(f"  líneas de código M1-M10: {sum(f[4] for f in filas[:10])}; simuladores M1-M10: {sum(f[5] for f in filas[:10])}")

print("\nConsignas de los simuladores (párrafo simulador-intro) por módulo:")
for k, a, b, *_ in filas[:11]:
    trozo = '\n'.join(L[a - 1:b])
    for m in re.finditer(r'data-simulador="([^"]+)".*?<p class="simulador-intro">(.*?)</p>', trozo, flags=re.S):
        lin = a + trozo[:m.start()].count('\n')
        t = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(2))).strip()
        print(f"  M{k} l.{lin} [{m.group(1)}]: {t}")
print("\nPreguntas (¿…?) en la prosa por módulo (fuera de <pre>):")
for k, a, b, *_ in filas[:11]:
    t = prosa('\n'.join(L[a - 1:b]))
    print(f"  M{k}: {t.count('¿')}")
