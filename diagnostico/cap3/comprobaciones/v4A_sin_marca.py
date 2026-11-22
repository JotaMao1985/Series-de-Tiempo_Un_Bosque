"""Verificador A · R4 cap. 3: prosa de los módulos 1-6 FUERA de todo data-afirma
que contiene un patrón de atribución (nombres, «se llama», software, «siempre»…)."""
import re, sys, pathlib
RAIZ = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "precalculo"))
import audita_citas as A
htm = (RAIZ / "Htmls_Series/capitulo-3-modelos-ar-ma-arma.html").read_text("utf-8")
ini = htm[:htm.find('<template id="module-1">')].count("\n") + 1
fin = htm[:htm.find('<template id="module-7">')].count("\n") + 1
lec = A.lee_html(htm)
PAT = re.compile(r"Box|Jenkins|Wold|Slutsky|Yule|Walker|Bartlett|Ljung|Pierce|Durbin|Levinson|Akaike|Schwarz|Hannan|Kalman|"
                 r"Shumway|Stoffer|Hyndman|Cryer|Hamilton|Brockwell|S-PLUS|SAS|Stata|EViews|statsmodels|forecast|fable|"
                 r"auto\.arima|se (?:llama|conoce|denomina)|llamad[oa]|conocid[oa]|nombre|histór|clásic|siempre|nunca|"
                 r"en la práctica|habitual|estándar|por defecto|suele|la mayoría|casi siempre|airline|Wolfer|manchas", re.I)
buf = {}
for linea, dato in lec.prosa:
    if ini <= linea < fin:
        buf.setdefault(linea, []).append(dato)
for linea in sorted(buf):
    t = re.sub(r"\s+", " ", " ".join(buf[linea])).strip()
    if PAT.search(t):
        print(f"{linea}: {t[:400]}")
