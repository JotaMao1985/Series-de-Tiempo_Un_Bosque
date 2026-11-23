# Compara las cifras de los comentarios '#>' (R) y '# ' tras print (Python) con la salida real
import re, pathlib
d = pathlib.Path(__file__).parent / "par_bloques"
num = re.compile(r'-?\d+\.\d+|-?\d+e-?\d+|\b\d+\b')
for src in sorted(d.glob("b*.*")):
    if src.suffix not in (".R", ".py"): continue
    out = src.with_suffix(".out").read_text()
    # para R: quitar las lineas de eco (las que empiezan por '>' o '+')
    if src.suffix == ".R":
        real = "\n".join(l for l in out.splitlines() if not l.startswith(("> ", "+ ", ">")))
        esperadas = [l for l in src.read_text().splitlines() if l.strip().startswith("#>")]
    else:
        real = out
        esperadas = [l.split("#",1)[1] for l in src.read_text().splitlines()
                     if "#" in l and re.search(r'\d\.\d', l.split("#",1)[1])]
    reales = set(num.findall(real))
    faltan = []
    for l in esperadas:
        for t in num.findall(l):
            if "." not in t: continue
            if t not in reales and t.lstrip("-") not in reales and ("-"+t) not in reales:
                faltan.append((t, l.strip()[:90]))
    print(f"{src.name}: {len(esperadas)} lineas con cifras; no halladas en la salida: {len(faltan)}")
    for t, l in faltan: print(f"    {t:>12}  <- {l}")
