"""Verificador R2 cap. 5: distancia de color (CIEDE2000) entre las líneas del M11, antes y después, y su trazo."""
import math, itertools
def lab(h):
    r, g, b = [int(h[i:i+2], 16) / 255 for i in (1, 3, 5)]
    lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = lin(r), lin(g), lin(b)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047; y = 0.2126 * r + 0.7152 * g + 0.0722 * b; z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    return 116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))
def de2000(c1, c2):
    L1, a1, b1 = lab(c1); L2, a2, b2 = lab(c2)
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2); Cm = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cm ** 7 / (Cm ** 7 + 25 ** 7)))
    a1p, a2p = a1 * (1 + G), a2 * (1 + G); C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1 = math.degrees(math.atan2(b1, a1p)) % 360; h2 = math.degrees(math.atan2(b2, a2p)) % 360
    dL, dC = L2 - L1, C2p - C1p
    dh = h2 - h1 if abs(h2 - h1) <= 180 else (h2 - h1 - 360 if h2 > h1 else h2 - h1 + 360)
    dH = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dh / 2))
    Lm, Cmp = (L1 + L2) / 2, (C1p + C2p) / 2
    hm = (h1 + h2) / 2 if abs(h1 - h2) <= 180 else ((h1 + h2 + 360) / 2 if h1 + h2 < 360 else (h1 + h2 - 360) / 2)
    T = 1 - 0.17 * math.cos(math.radians(hm - 30)) + 0.24 * math.cos(math.radians(2 * hm)) + 0.32 * math.cos(math.radians(3 * hm + 6)) - 0.2 * math.cos(math.radians(4 * hm - 63))
    SL = 1 + 0.015 * (Lm - 50) ** 2 / math.sqrt(20 + (Lm - 50) ** 2); SC = 1 + 0.045 * Cmp; SH = 1 + 0.015 * Cmp * T
    RT = -2 * math.sqrt(Cmp ** 7 / (Cmp ** 7 + 25 ** 7)) * math.sin(math.radians(60 * math.exp(-((hm - 275) / 25) ** 2)))
    return math.sqrt((dL / SL) ** 2 + (dC / SC) ** 2 + (dH / SH) ** 2 + RT * (dC / SC) * (dH / SH))
# Orden de los interruptores y de COLORES en la página (medido en v2_medidas.json), no el del JSON
claves = ['ets_log', 'armonica', 'stl_arima', 'sarima', 'auto_arima', 'sarima_calendario', 'ets', 'snaive']
antes = ['#FB6400', '#0e7490', '#7c3aed', '#be123c', '#0f766e', '#a16207', '#9333ea', '#475569']
ahora = ['#FB6400', '#1d4ed8', '#7c3aed', '#be123c', '#0f766e', '#a16207', '#db2777', '#475569']
trazo = ['[6,3]', 'continua', '[2,3]', '[9,3,2,3]', '[6,3]', 'continua', '[2,3]', '[9,3,2,3]']
for nombre, cols in [('antes', antes), ('ahora', ahora)]:
    trazo = ['[5,3]'] * 8 if nombre == 'antes' else ['[6,3]', 'continua', '[2,3]', '[9,3,2,3]', '[1,4] gruesa (gemelo)', 'continua', '[2,3]', '[9,3,2,3]']
    todos = list(zip(claves, cols)) + [('observado', '#012820')]
    pares = sorted(((de2000(c1, c2), k1, k2) for (k1, c1), (k2, c2) in itertools.combinations(todos, 2)))
    print(nombre, '· los 6 pares más próximos (ΔE2000):')
    for d, k1, k2 in pares[:6]:
        t1 = trazo[claves.index(k1)] if k1 in claves else 'continua 2.4'; t2 = trazo[claves.index(k2)] if k2 in claves else 'continua 2.4'
        print(f'   {d:5.1f}  {k1} ({dict(todos)[k1]}, {t1})  ~  {k2} ({dict(todos)[k2]}, {t2})')
