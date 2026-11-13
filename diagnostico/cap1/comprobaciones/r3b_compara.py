# R3b · Contrasta el capitulo publicado con lo que calculo R.
#   1. DATOS_CAP1 no cambio; DATOS_CAP1_STL es, caracter a caracter, la salida del guion de R.
#   2. La variante de partida de DATOS_CAP1_STL.stl es DATOS_CAP1.stl_log.
#   3. La desestacionalizada incrustada (R) frente a y / exp(S) calculada con los datos incrustados (4 decimales).
#   4. Cada cifra nueva de la prosa de los Modulos 6, 7, 8 aparece en el HTML y en la salida de R que la respalda.
# Uso: python3 diagnostico/cap1/comprobaciones/r3b_compara.py <copia de antes de la ronda> > r3b_compara.out
import io, json, math, os, re, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(AQUI, "..", "..", "..")
doc = io.open(os.path.join(W, "Htmls_Series", "capitulo-1-componentes-descomposicion.html"), encoding="utf-8").read()
fallos = 0
def ok(cond, texto):
    global fallos
    fallos += 0 if cond else 1
    print(("OK    " if cond else "FALLA ") + texto)

def constante(nombre, texto):
    m = re.search(r"^    const %s = (\{.*\});$" % nombre, texto, re.M)
    return m.group(1)

c1 = constante("DATOS_CAP1", doc)
if len(sys.argv) > 1:
    antes = io.open(sys.argv[1], encoding="utf-8").read()
    ok(constante("DATOS_CAP1", antes) == c1, "DATOS_CAP1 es identica a la de antes de la ronda (%d caracteres)" % len(c1))
js = io.open(os.path.join(W, "precalculo", "salidas", "cap1_stl_variantes.js"), encoding="utf-8").read().strip().split("\n")
c2 = constante("DATOS_CAP1_STL", doc)
ok("const DATOS_CAP1_STL = " + c2 + ";" == js[2], "DATOS_CAP1_STL del capitulo = precalculo/salidas/cap1_stl_variantes.js (%d caracteres)" % len(c2))
ok(c2 == io.open(os.path.join(W, "precalculo", "salidas", "cap1_stl_variantes.json"), encoding="utf-8").read().strip(), "... y = cap1_stl_variantes.json")
D1, D2 = json.loads(c1), json.loads(c2)

b = D2["stl"]["per_orig_norob"]
for k in ("tendencia", "estacional", "residuo"):
    ok(b[k] == D1["stl_log"][k], "variante de partida · %s = DATOS_CAP1.stl_log.%s (144 valores)" % (k, k))
ok(len(D2["stl"]) == 8 and all(len(v[k]) == 144 for v in D2["stl"].values() for k in ("tendencia", "estacional", "residuo")), "ocho variantes, 144 valores por componente")

y, S = D1["observado"], D1["stl_log"]["estacional"]
aj = D2["desestacionalizada"]["stl"]
dif = max(abs(a - v / math.exp(s)) for a, v, s in zip(aj, y, S))
ok(dif < 0.1, "desestacionalizada incrustada (R, 1 decimal) frente a y / exp(S) con el S incrustado a 4 decimales: max |dif| = %.3f" % dif)
r = subprocess.run(["Rscript", "-e", 'cat(round(as.numeric(AirPassengers / exp(stl(log(AirPassengers), s.window = "periodic")$time.series[, "seasonal"])), 1))'], capture_output=True, text=True).stdout.split()
ok([float(x) for x in r] == aj, "desestacionalizada incrustada = AirPassengers / exp(S) recalculada ahora en R, punto a punto (144 de 144)")
ad, mu = D2["clasica"]["aditiva"], D2["clasica"]["multiplicativa_en_miles"]
r = subprocess.run(["Rscript", "-e", 'y <- AirPassengers; a <- decompose(y, "additive"); m <- decompose(y, "multiplicative"); cat(round(as.numeric(a$seasonal), 2), "|", round(as.numeric(a$random), 2), "|", round(as.numeric(m$trend * (m$seasonal - 1)), 2), "|", round(as.numeric(y - m$trend * m$seasonal), 2))'], capture_output=True, text=True).stdout.split("|")
num = lambda t: [None if x == "NA" else float(x) for x in t.split()]
ok(num(r[0]) == ad["estacional"] and num(r[1]) == ad["residuo"], "clasica aditiva incrustada = decompose(type = 'additive') recalculada ahora (estacional y residuo, 144 + 144)")
ok(num(r[2]) == mu["estacional"] and num(r[3]) == mu["residuo"], "multiplicativa en miles incrustada = T(S - 1) e y - TS recalculadas ahora (144 + 144)")

# --- cifras de la prosa: (texto que debe estar en el HTML, archivo de evidencia, texto que debe estar en la evidencia)
ev = {n: io.open(os.path.join(AQUI, n), encoding="utf-8").read() for n in ("r3b_cifras.out", "r3b_genera_variantes.out", "r3b_bloques_publicados.out")}
CIFRAS = [
    ("M7", "julio, un 24.2&nbsp;% por encima de la tendencia", "r3b_cifras.out", "julio, 'periodic': + 24.2 % los doce anios"),
    ("M7", "julio pasa de +20.4&nbsp;% en 1949 a +27.9&nbsp;% en", "r3b_cifras.out", "julio, s.window = 11, 1949..1960 (%): 20.4 20.7 20.9 21.4 22 23.5 25 26.1 27.1 27.4 27.7 27.9"),
    ("M7", "negativo los cinco\n        primeros años y positivo los siete últimos", "r3b_cifras.out", "negativos: 1949 1950 1951 1952 1953 | positivos: 1954 1955 1956 1957 1958 1959 1960"),
    ("M7", "0.040 en 1949–1953 y de 0.036 en 1958–1960, frente a 0.019", "r3b_cifras.out", "sd del residuo por tramo, 'periodic'  : 0.0396 0.0188 0.036"),
    ("M7", "bajan a 0.029 y 0.024 las de los extremos y a 0.016 la del", "r3b_cifras.out", "sd del residuo por tramo, s.window 11 : 0.0289 0.016 0.0239"),
    ("M7", "tampoco con ventanas más estrechas", "r3b_cifras.out", "sd del residuo por tramo, s.window 7 : 0.024 0.0138 0.0195  razon extremos/centro: 1.61"),
    ("M7", "el logaritmo de ese mes sube 0.4055", "r3b_cifras.out", "log(1.5) = 0.4055"),
    ("M7", "sube de +24.2&nbsp;% a +28.1&nbsp;%, la tendencia de ese mes pasa de 283.2 a 294.3", "r3b_cifras.out", "inflada, sin robust                          28.1     294.3        0.3708"),
    ("M7", "y su residuo queda en 0.3708", "r3b_cifras.out", "limpia, sin robust                           24.2     283.2        0.0347"),
    ("M7", "—+24.6&nbsp;% y 282.2 mil—", "r3b_cifras.out", "inflada, robust                              24.6     282.2        0.4404     5 0.0000"),
    ("M7", "el dato, 0.4404", "r3b_cifras.out", "inflada, robust                              24.6     282.2        0.4404"),
    ("M7", "de 12 observaciones sin estimar a <strong>ninguna</strong>", "r3b_cifras.out", "NA en la tendencia de stl() = 0 ; en la de decompose() = 12"),
    ("M7", "—dos pasadas, por defecto—", "r3b_cifras.out", "pasadas interiores 2 | vueltas exteriores 0"),
    ("M7", "da 15 vueltas, cada una con una sola\n        pasada", "r3b_cifras.out", "con robust = TRUE:   pasadas interiores 1 | vueltas exteriores 15"),
    ("M7", "sino de la serie sin la tendencia recién\n            estimada", "r3b_cifras.out", "max |S - medias centradas| = 1.86e-08"),
    ("M7", "así la estacionalidad oscila alrededor de cero", "r3b_cifras.out", "suma de los doce valores estacionales ('periodic') = 1.46e-08"),
    ("M7", "# julio: 1.204 y 1.279", "r3b_bloques_publicados.out", "[1] 1.204 1.279"),
    ("M7", "# [1.204 1.279]", "r3b_bloques_publicados.out", "[1.204 1.279]"),
    ("M7", "# 4 sin peso", "r3b_bloques_publicados.out", "[1] 4\ns11: ventanas 11 21 13"),
    ("M6", "entre unos 54 por debajo y 64 por encima", "r3b_cifras.out", "rangos: S aditiva -53.6 63.8"),
    ("M6", "(lectura) 30.5 · 5.6 · 25.4 / 4.2 · 5.4 · 22.3", "r3b_cifras.out", "sd anual del residuo, multiplicativa: 4.2 5.5 8.6 7.1 8.4 5.4 5.4 4.6 8.2 18.4 12.8 22.3"),
    ("M6", "(lectura) la aditiva es la mayor en los doce años", "r3b_cifras.out", "la aditiva es mayor en 12 de 12 anios"),
    ("M8", "$364 / 1.2416 = 293.2$ mil pasajeros", "r3b_cifras.out", "desestacionalizada, julio de 1955: 364 / exp(S) = 293.2 ; con el indice clasico: 296.8"),
    ("M8", "296.8 en vez de 293.2, y la mayor diferencia entre las dos series ajustadas es de 6.1 mil pasajeros, un\n        1.2&nbsp;%, en julio de 1960", "r3b_cifras.out", "mayor diferencia entre las dos: 6.1 mil ( 1.2 % ) en 1960 mes 7"),
    ("M8", "<td>0.994</td><td>0.937</td>", "r3b_cifras.out", "log(AirPassengers)   FT = 0.994  FS = 0.937"),
    ("M8", "<td>0.205</td><td>0.944</td>", "r3b_cifras.out", "nottem               FT = 0.205  FS = 0.944"),
    ("M8", "<td>0.907</td><td>0.005</td>", "r3b_cifras.out", "sunspots             FT = 0.907  FS = 0.005"),
    ("M8", "<td>0.12</td><td>0.08</td>", "r3b_cifras.out", "mediana FT = 0.12  FS = 0.08"),
    ("M8", "temperatura media mensual en Nottingham, 1920–1939", "r3b_cifras.out", "Average Monthly Temperatures at Nottingham, 1920-1939"),
    ("M8", "manchas solares mensuales, 1749–1983", "r3b_cifras.out", "Monthly Sunspot Numbers, 1749-1983"),
    ("M8", "misma serie en logaritmos salen 0.997 y 0.964", "r3b_bloques_publicados.out", "feat_stl: trend_strength = 0.997  seasonal_strength_year = 0.964"),
    ("M8", "#> 0.994 0.937", "r3b_bloques_publicados.out", "   FT    FS \n0.994 0.937"),
    ("M8", "print(round(FT, 3), round(FS, 3))                # 0.994 0.937", "r3b_bloques_publicados.out", "293.2\n0.994 0.937"),
    ("M8", "Ni siquiera el ruido puro da cero", "r3b_cifras.out", "minimo FT 0.025  FS 0.015"),
]
print()
for mod, en_html, archivo, en_ev in CIFRAS:
    if not en_html.startswith("(lectura)"):
        ok(en_html in doc, "%s · en el capitulo: «%s»" % (mod, en_html.replace("\n", " ").replace("        ", " ")[:95]))
    ok(en_ev in ev[archivo], "      en %s: «%s»" % (archivo, en_ev.replace("\n", " / ")[:100]))
print("\nfallos:", fallos)
