"""v4_sin_marca.py — busca, en la prosa del capítulo 2 que NO está dentro de
ningún `data-afirma`, apellidos y giros de atribución («se recomienda», «es
habitual», «suele», «estándar»…). Salida: v4_sin_marca.out"""
import pathlib, re, sys
RAIZ = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "precalculo"))
from audita_citas import lee_html
H = RAIZ / "Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html"
lec = lee_html(H.read_text("utf-8"))
nombres = r"Box|Cox|Jenkins|Reinsel|Ljung|Pierce|Dickey|Fuller|Durbin|Levinson|Yule|Walker|Quenouille|Bartlett|Granger|Newbold|Engle|Bollerslev|Wold|Akaike|Phillips|Perron|Kwiatkowski|Schmidt|Shin|Guerrero|Hyndman|Athanasopoulos|Cryer|Chan|Hamilton|Shumway|Stoffer|Brockwell|Davis|Cleveland|Tsay|Holt|Winters|Hannan|Said|Bickel|Doksum|FPP3|fpp3"
giros = r"se recomienda|recomiend|es habitual|habitualmente|suele|sueles|estándar|clásic|la literatura|los textos|la mayoría|muchos autores|se sabe|bien sabido|tradicional|se acostumbra|convención|propuest|introduj|debe su nombre|se conoce como|llamad[oa]s? |se llama|regla práctica|regla de oro|por defecto|más usad|el más común|la más común|siempre|nunca"
pat = re.compile(rf"\b({nombres})\b|({giros})", re.I)
# reunir la prosa por línea
por_linea = {}
for linea, dato in lec.prosa:
    por_linea.setdefault(linea, "")
    por_linea[linea] += dato
for linea in sorted(por_linea):
    t = re.sub(r"\s+", " ", por_linea[linea]).strip()
    ms = [m.group(0) for m in pat.finditer(t)]
    if ms:
        print(f"{linea}: [{', '.join(sorted(set(ms)))}] {t[:260]}")
