"""Diagnóstico cap. 5 · lee las figuras SVG del simulacro (S8 = GI, S9 = GD) y devuelve
los valores que dibujan, para comprobar la clave sin mirar la imagen.

    node diagnostico/cap5/diag/ejercicios_vuelca.js > diagnostico/cap5/diag/ejercicios_vuelca.json
    python3 diagnostico/cap5/diag/ejercicios_simulacro_figuras.py > diagnostico/cap5/diag/ejercicios_simulacro_figuras.out

Cada panel declara su escala con `grid-y` (data-v, y1). Barra: valor = (y_cero - y2)/px_por_unidad.
Puntos del panel de residuales: idem con cy.
"""
import json, re, pathlib, statistics as st
aqui = pathlib.Path(__file__).resolve().parent
J = json.load(open(aqui / 'ejercicios_vuelca.json'))

def paneles(html):
    return re.findall(r"(<svg[^>]*data-panel='([^']+)'.*?</svg>)", html, flags=re.S)

def escala(svg):
    g = [(float(v), float(y)) for v, y in re.findall(r"class='grid-y' data-v='([-\d.]+)'[^>]*y1='([-\d.]+)'", svg)]
    (v0, y0), (v1, y1) = g[0], g[-1]
    k = (y1 - y0) / (v1 - v0)            # px por unidad (negativo: y crece hacia abajo)
    return lambda y: v0 + (float(y) - y0) / k

for p in J['simulacro']:
    if p['id'] not in ('GI', 'GD'):
        continue
    print(f"\n######## {p['n']} · {p['id']} · {p['etiqueta']}")
    for svg, nombre in paneles(p['enunciado_html']):
        a = escala(svg)
        banda = re.findall(r"class='banda' data-v='([-\d.]+)'", svg)
        barras = [(int(k), a(y2)) for k, y2 in re.findall(r"class='barra' data-k='(\d+)'[^>]*y2='([-\d.]+)'", svg)]
        pts = [(int(t), a(cy)) for t, cy in re.findall(r"class='pt' data-t='(\d+)'[^>]*cy='([-\d.]+)'", svg)]
        print(f"panel {nombre}: banda {banda}")
        if barras:
            b = abs(float(banda[0])) if banda else None
            fuera = [(k, round(v, 3)) for k, v in barras if b and abs(v) > b]
            print('  fuera de banda:', fuera)
            print('  rezagos 1,2,3,11,12,13,24,36:', [(k, round(v, 3)) for k, v in barras if k in (1, 2, 3, 11, 12, 13, 23, 24, 25, 36)])
        if pts:
            v = [x for _, x in pts]
            n = len(v); t = n // 3
            sd = [st.pstdev(v[i * t:(i + 1) * t]) for i in range(3)]
            print(f'  {n} puntos; desviación por tercios: {[round(s, 3) for s in sd]}; razón último/primero {sd[2]/sd[0]:.2f}')
            print(f'  |z| > 2: {sum(abs(x) > 2 for x in v)}; |z| > 3: {sum(abs(x) > 3 for x in v)}; max |z| {max(abs(x) for x in v):.2f}')
