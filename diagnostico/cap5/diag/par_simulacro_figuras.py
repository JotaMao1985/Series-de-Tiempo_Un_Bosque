# Lee las barras y la serie de las figuras SVG de las preguntas 8 y 9 del simulacro
# (extraídas con par_simulacro_svg.js) y reconstruye los valores que dibujan.
import re, sys, statistics as st
d = sys.argv[1]
for n in (8, 9):
    t = open(f"{d}/p{n}.svg.txt").read()
    for svg in re.findall(r"<svg.*?</svg>", t, re.S):
        mp = re.search(r"data-panel='(\w+)'", svg); panel = mp.group(1) if mp else re.search(r"aria-label='([^']*)'", svg).group(1)
        ticks = [(float(v), float(y)) for v, y in re.findall(r"class='grid-y' data-v='([-\d.]+)'[^>]*y1='([\d.]+)'", svg)]
        (v0, y0), (v1, y1) = ticks[0], ticks[-1]
        val = lambda y: v0 + (float(y) - y0) * (v1 - v0) / (y1 - y0)
        barras = re.findall(r"class='barra' data-k='(\d+)'[^>]*y2='([-\d.]+)'", svg)
        banda = re.findall(r"class='banda' data-v='([-\d.]+)'", svg)
        print(f"P{n} panel {panel}: banda {banda}")
        if barras:
            vals = {int(k): round(val(y), 3) for k, y in barras}
            print("   ", {k: vals[k] for k in sorted(vals) if k in (1,2,3,4,11,12,13,24,36) or abs(vals[k]) > float(banda[0] if banda else 9)})
        pts = re.findall(r"points='([^']+)'", svg)
        if pts:
            ys = [val(p.split(',')[1]) for p in pts[0].split()]
            k = len(ys) // 3
            print(f"    serie: {len(ys)} puntos; desv. típica primer tercio {st.pstdev(ys[:k]):.3f}, último tercio {st.pstdev(ys[-k:]):.3f}, razón {st.pstdev(ys[-k:])/st.pstdev(ys[:k]):.2f}")
        circ = re.findall(r"<circle[^>]*cy='([-\d.]+)'", svg)
        if circ:
            ys = [val(c) for c in circ]; k = len(ys) // 3
            print(f"    puntos: {len(ys)}; razón de desviaciones último/primer tercio {st.pstdev(ys[-k:])/st.pstdev(ys[:k]):.2f}")
