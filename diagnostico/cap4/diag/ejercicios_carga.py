"""Diagnóstico cap. 4 · carga de lectura por módulo y dónde aparece la primera tarea.

    python3 diagnostico/cap4/diag/ejercicios_carga.py > diagnostico/cap4/diag/ejercicios_carga.out

Por módulo: palabras de prosa (sin <pre>, sin <script>, sin comentarios), líneas de
código, simuladores, duración declarada en courseData y minutos de lectura a 150 y
200 palabras por minuto (prosa técnica con fórmulas). Luego, las tareas: el primer
`data-quiz`, los `ejercicio-guiado` y las consignas imperativas dentro de las
lecturas de los simuladores (frases con «Empieza», «Cambia», «Mueve», «Sube», «busca»,
«mira», «Fíjate» o una pregunta con «¿»).
"""
import re, pathlib
raiz = pathlib.Path(__file__).resolve().parents[3]
html = (raiz / 'Htmls_Series/capitulo-4-modelos-arima.html').read_text(encoding='utf8')
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

print(f"{'Mód':>3} {'líneas':>11} {'palabras':>8} {'código':>6} {'simul':>5} {'dur.decl':>8} {'min@150':>7} {'min@200':>7}")
acum = {'pal': 0, 'dur': 0}
filas = []
for k, a in enumerate(ini, start=1):
    b = next(f for f in fin if f > a)
    trozo = '\n'.join(L[a:b + 1])
    # en el M10, solo hasta la autoevaluación (lo que se lee antes de la primera tarea)
    palabras = len(re.findall(r'[A-Za-zÁÉÍÓÚáéíóúñÑü]+', prosa(trozo)))
    codigo = sum(len(p.split('\n')) for p in re.findall(r'<pre.*?</pre>', trozo, flags=re.S))
    sims = len(re.findall(r'data-simulador="', trozo))
    filas.append((k, a + 1, b + 1, palabras, codigo, sims))
    print(f"{k:>3} {a+1:>5}-{b+1:<5} {palabras:>8} {codigo:>6} {sims:>5} {dur.get(k, 0):>8} {palabras/150:>7.1f} {palabras/200:>7.1f}")

q = next(i for i, l in enumerate(L) if 'data-quiz="cap4"' in l) + 1
ej = [i + 1 for i, l in enumerate(L) if 'class="ejercicio-guiado"' in l]
m10 = filas[9]
antes_quiz = len(re.findall(r'[A-Za-zÁÉÍÓÚáéíóúñÑü]+', prosa('\n'.join(L[m10[1] - 1:q - 1]))))
tot_m1_m9 = sum(f[3] for f in filas[:9])
print(f"\nPrimera tarea con respuesta comprobable: quiz cap4 en la línea {q} (M10); ejercicios en {ej}")
print(f"Prosa antes de esa tarea: M1-M9 {tot_m1_m9} palabras + M10 hasta el quiz {antes_quiz} = {tot_m1_m9 + antes_quiz}")
print(f"  a 150 ppm: {(tot_m1_m9 + antes_quiz)/150:.0f} min; a 200 ppm: {(tot_m1_m9 + antes_quiz)/200:.0f} min")
print(f"  duración declarada M1-M9: {sum(dur[k] for k in range(1, 10))} min; M10 entero: {dur[10]} min")

print("\nConsignas en las lecturas de los simuladores y del ciclo (no recogen respuesta):")
verbo = re.compile(r'(Empieza|Cambia|Mueve|Sube|busca|Busca|mira|Mira|Fíjate|fíjate|Al pulsar|compara|observa|Recuerda)')
for k, a, b, *_ in filas[:10]:
    for i in range(a - 1, b):
        t = re.sub(r'<[^>]+>', '', L[i]).strip()
        if verbo.search(t) and ('simulador' in ''.join(L[max(a-1, i-12):i+1]) or 'ciclo' in ''.join(L[max(a-1, i-6):i+1])):
            print(f"  M{k} l.{i+1}: {t[:110]}")
print("\nPreguntas retóricas (¿…?) en la prosa de M1-M10, por módulo:")
for k, a, b, *_ in filas[:10]:
    n = sum(1 for i in range(a - 1, b) if '¿' in re.sub(r'<[^>]+>', '', L[i]) and '<pre' not in L[i])
    print(f"  M{k}: {n}")
