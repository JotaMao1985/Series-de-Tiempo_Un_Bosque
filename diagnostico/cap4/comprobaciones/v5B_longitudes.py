"""Verificador B · R5 cap. 4: longitud de las opciones del quiz AUTOEVALUACIONES['cap4'] y posición de la correcta.
Mide el texto visible aproximado: sin etiquetas HTML y con cada fórmula $...$ contada por sus caracteres
sin comandos de LaTeX (\\hat, \\phi -> 1 carácter)."""
import re, sys
src = open('ensamblado/cap4/chapter.js', encoding='utf-8').read()
ini = src.index("AUTOEVALUACIONES['cap4'] = [")
fin = src.index("\n    ];", ini)
bloque = src[ini:fin]
def visible(t):
    t = t.replace("\\\\", "\\")
    t = re.sub(r'<[^>]+>', '', t)
    def mat(m):
        f = m.group(1)
        f = re.sub(r'\\(operatorname|text|mathrm)\{([^}]*)\}', r'\2', f)
        f = re.sub(r'\\[a-zA-Z]+', 'x', f)      # un comando = un símbolo
        f = re.sub(r'[{}^_ ]', '', f)
        return f
    t = re.sub(r'\$(.+?)\$', mat, t)
    return t
preguntas = re.split(r"\n      \{\n        tipo: ", bloque)[1:]
for i, p in enumerate(preguntas, 1):
    tipo = p.split("'")[1]
    ops = re.findall(r"texto: '((?:[^'\\]|\\.)*)',\s*correcta: (true|false)", p)
    if not ops:
        continue
    L = [(len(visible(t)), c == 'true', visible(t)) for t, c in ops]
    lens = [l for l, _, _ in L]
    corr = [k + 1 for k, (_, c, _) in enumerate(L) if c]
    orden = sorted(range(len(L)), key=lambda k: -lens[k])
    larga = orden[0] + 1
    print(f"P{i} ({tipo}) longitudes {lens}  correcta(s) {corr}  mas larga {larga}"
          f"  cociente max/min {max(lens)/min(lens):.2f}")
    if tipo == 'multiple':
        nc = len(corr)
        print(f"    las {nc} mas largas: {sorted(k+1 for k in orden[:nc])}; las {nc} mas cortas: {sorted(k+1 for k in orden[-nc:])}")
    for l, c, t in L:
        print(f"    {'*' if c else ' '} {l:3d}  {t}")
