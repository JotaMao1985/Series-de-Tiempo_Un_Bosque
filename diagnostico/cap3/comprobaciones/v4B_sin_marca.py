#!/usr/bin/env python3
"""Verificador B, R4 cap. 3: prosa de los módulos 7-10 FUERA de toda marca
`data-afirma` que nombra autores, años, obras o giros de atribución. Solo lee."""
import pathlib, re, sys
RAIZ = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "precalculo"))
from audita_citas import lee_html  # noqa: E402

texto = (RAIZ / "ensamblado/cap3/cap3_modulos.html").read_text("utf-8")
lineas = texto.splitlines()
ini = next(i for i, l in enumerate(lineas) if 'id="module-7"' in l) + 1
fin = next(i for i, l in enumerate(lineas) if 'id="module-11"' in l) + 1
lector = lee_html(texto)
PATRON = re.compile(
    r"\b(Yule|Walker|Wolf\w*|Box|Jenkins|Pierce|Ljung|Akaike|Schwarz|Hurvich|Tsai|Guerrero|Hyndman|"
    r"Khandakar|Athanasopoulos|Cryer|Chan|Hamilton|Shumway|Stoffer|Reinsel|Durbin|Levinson|Shapiro|Wilk|"
    r"Engle|Bollerslev|Kalman|Brockwell|Davis|Tong|Schuster|FPP3|statsmodels|forecast\b|fable|"
    r"1[89]\d\d|20[0-2]\d|según|propuso|inventó|clásic\w+|documentad\w+|se sabe|se demostró|"
    r"los astrónomos|la literatura|habitual\w*|suele\w*|siempre|nunca)", re.I)
vistos = 0
for linea, dato in lector.prosa:
    if not (ini <= linea <= fin):
        continue
    d = " ".join(dato.split())
    for m in PATRON.finditer(d):
        vistos += 1
        a, b = max(0, m.start() - 70), min(len(d), m.end() + 70)
        print(f"{linea}: «{m.group(0)}» … {d[a:b]}")
print(f"\n{vistos} apariciones fuera de marca en módulos 7-10 (líneas {ini}-{fin}).")
