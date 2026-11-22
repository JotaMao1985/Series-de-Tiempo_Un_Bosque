#!/usr/bin/env python3
"""Lector-estudiante · terminos usados antes de definirse, remisiones, notacion y voz (capitulo 4).

Uso:  python3 -I lector_terminos.py ruta/capitulo-4-modelos-arima.html

Adaptado de diagnostico/cap3/diag/lector_terminos.py (mismo metodo). Lee SOLO los doce
<template id="module-N"> (lo que el estudiante lee), no el JS ni el CSS. Para cada termino da la
primera linea en que aparece (con su modulo), la linea de su presentacion (fijada a mano tras leer
el marcado: la columna «def.» no es un hallazgo del guion, es lo que se leyo) y la distancia.
Despues: remisiones «Modulo N» hacia delante y hacia atras, variantes de notacion y de
vocabulario por modulo, y la voz (segunda persona del singular) por modulo.
"""
import html as _html
import re
import sys

ruta = sys.argv[1]
lineas = open(ruta, encoding="utf-8").read().split("\n")

rangos = {}
ini = None
for i, l in enumerate(lineas, 1):
    m = re.search(r'<template id="module-(\d+)">', l)
    if m:
        ini = (int(m.group(1)), i)
    if "</template>" in l and ini:
        rangos[ini[0]] = (ini[1], i)
        ini = None


def modulo(i):
    for k, (a, b) in rangos.items():
        if a <= i <= b:
            return k
    return None


def primera(regex, desde=1):
    pat = re.compile(regex)
    for i, l in enumerate(lineas, 1):
        if i < desde or modulo(i) is None:
            continue
        if pat.search(l):
            return i
    return None


def todas(regex):
    pat = re.compile(regex)
    return [i for i, l in enumerate(lineas, 1) if modulo(i) and pat.search(l)]


# (termino, regex del primer uso, linea de la presentacion leida a mano, nota)
TERMINOS = [
    ("PP / Phillips–Perron (la prueba)", r"\bPP\b|PP\.test", 4387,
     "M3 3251 (tabla) la usa con la sigla; se describe en prosa en 3259 («corrige la autocorrelacion de forma no parametrica»); el nombre completo solo en M8 4387; no esta en el cap. 2"),
    ("modelo de dos medias / escalon", r"dos medias", 4404,
     "M3 3314 «el modelo de dos medias del Nilo»; el modelo y(t) = mu + beta*1{t>=1899} se escribe en M8 4405 (el escalon como hipotesis, M3 3307)"),
    ("Holt (metodo)", r"Holt", None, "M1 2853 («incluye al metodo de Holt»); no se define en ningun modulo; no esta en cap. 1-3 (grep)"),
    ("suavizamiento exponencial simple", r"suavizamiento", 2851, "M1 2851 lo define con una recursion en la misma celda; no esta en los caps. 1-3 (grep)"),
    ("checkresiduals()", r"checkresiduals", None, "M2 3116 (lista «Con que»); no se usa en ningun bloque de codigo ni se explica"),
    ("auto.arima", r"auto\.arima", 4094, "M3 3291 (y M2 no); lo presenta el M7 (4094); el cap. 3 ya lo nombra en «Lo que viene»"),
    ("0.2544 y -0.8741 (coeficientes del ARIMA(1,1,1) del Nilo)", r"0\.2544", 4942,
     "M1 2894 como constantes del codigo; M1 2966 «coeficientes reales del Nilo»; se estiman y se dan con sus e.e. en M10 4942"),
    ("TRM (la serie)", r"TRM", 4960, "M5 3806 la usa en una nota; la serie se presenta en M10 4960; ya venia de los caps. 1-3"),
    ("naive (metodo de referencia)", r"[Nn]a[iï]ve", 5057, "M8 4438 (tabla fuera de muestra); se dice que es la caminata en M10 5057"),
    ("RMSE / MAE", r"RMSE", None, "M8 4425 (tabla); no se definen en el cap. 4 (el cap. 6 los trata)"),
    ("cobertura (real frente a nominal)", r"cobertura", None, "M9 4733; no se define en el cap. 4 (el cap. 6 la mide)"),
    ("«fuera de muestra»", r"fuera de muestra", 4423, "M6 3938 la nombra como remedio; M8 4423 la hace (entrenar hasta 1950, pronosticar 20 anios)"),
    ("lynx (serie)", r"lynx", 5578, "M8 4386 (caja de aviso, con cifras); se presenta como ejercicio 2 en M10 5578"),
    ("BJsales (serie)", r"BJsales", 5490, "M9 4662 (nota, con cifras); se presenta como ejercicio 1 en M10 5490"),
    ("nsdiffs", r"nsdiffs", None, "M10 4994; el cap. 2 lo presenta (grep: 31 lineas)"),
    ("estacional / SARIMA / airline", r"estacional", 5413, "M2 3123 («eso es el Capitulo 5»); M10 5413 lo presenta como avance"),
    ("«los coeficientes no estan identificados»", r"identificad", None, "M10 5042; «identificacion» es en este cap. la etapa 1 (M2, M4): dos sentidos, uno por modulo"),
    ("ARMA(2,1) (la expansion del ARIMA(1,1,1))", r"ARMA\(\$2,1\$\)", 2817, "M1 2817 (plegado); la usa M9 4624 y el ejercicio 3"),
    ("sobrediferenciacion", r"sobrediferenci", 4327, "M1 2978 («sintoma clasico de sobrediferenciacion»); la firma se presenta en M8 4325-4335"),
    ("cancelacion de raices", r"cancelaci[oó]n", 2977, "M1 2977 la nombra; ya viene explicada ahi mismo"),
    ("n efectivo (n* = n - d)", r"n\^\{\*\}|n efectivo", 3925, "primer uso = presentacion (M6 3925)"),
    ("varianza de largo plazo / truncamiento (KPSS)", r"varianza de largo plazo|truncamiento", 3506, "M3 3326 (intro del simulador: «el truncamiento ℓ»); M3 3371 (plegado); la define el recuadro 3500-3519"),
    ("puente browniano / sumas parciales", r"browniano|sumas parciales", 3365, "M3 3365 (plegado); sin definicion fuera del plegado"),
]

print("termino | primer uso (linea, modulo) | presentacion (linea, modulo) | distancia en lineas | nota")
for nombre, rx, defin, nota in TERMINOS:
    p = primera(rx)
    mp = modulo(p) if p else None
    md = modulo(defin) if defin else None
    dist = (defin - p) if (p and defin) else None
    print(f"{nombre} | {p} (M{mp}) | {defin if defin else '—'} (M{md if md else '—'}) | "
          f"{dist if dist is not None else '—'} | {nota}")

# --- Remisiones «Modulo N» -------------------------------------------------------------------
print()
print("== Remisiones «Modulo N» por modulo (hacia delante / hacia atras); sin las de los titulos ==")
pat = re.compile(r"M[oó]dulos? (\d+)(?:\s*(?:,|y|a)\s*(\d+))?")
adelante = {}
atras = {}
lista = []
for i in todas(r"M[oó]dulos? \d"):
    k = modulo(i)
    l = lineas[i - 1]
    if "<span>Módulo" in l:
        continue
    for m in pat.finditer(l):
        for g in (m.group(1), m.group(2)):
            if g is None:
                continue
            n = int(g)
            if n == k:
                continue
            (adelante if n > k else atras).setdefault(k, []).append((i, n))
            lista.append((k, i, n))
for k in sorted(rangos):
    a = adelante.get(k, [])
    b = atras.get(k, [])
    print(f"M{k}: hacia delante {len(a)} {[f'{i}->M{n}' for i, n in a]} ; hacia atras {len(b)}")
print()
print("Remisiones a M8 desde los modulos 1-7 (lineas):",
      [i for (k, i, n) in lista if n == 8 and k < 8])
print("Remisiones a M9 desde los modulos 1-8 (lineas):",
      [i for (k, i, n) in lista if n == 9 and k < 9])

# --- Notacion y vocabulario por modulo ---------------------------------------------------------
print()
print("== Notacion y vocabulario por modulo (numero de apariciones) ==")


def por_modulo(regex):
    c = {}
    pat2 = re.compile(regex)
    for i, l in enumerate(lineas, 1):
        k = modulo(i)
        if k is None:
            continue
        n = len(pat2.findall(l))
        if n:
            c[k] = c.get(k, 0) + n
    return (sum(c.values()), " ".join(f"M{k}:{v}" for k, v in sorted(c.items())) or "—")


GRUPOS = [
    ("tamano de muestra «n» (math)", r"\$n\$|\$n\s*=|\bn\s*=\s*\d|\\sqrt\{n\}|\bn\^\{\*\}"),
    ("tamano de muestra «T» (math)", r"\$T\$|\\sqrt\{T\}|\bT\s*=\s*\d"),
    ("«caminata (aleatoria)»", r"[Cc]aminata"),
    ("«paseo aleatorio»", r"paseo aleatorio"),
    ("«residuales»", r"residuales"),
    ("«residuos»", r"residuos\b"),
    ("«abanico»", r"abanico"),
    ("«periodo» (sin tilde)", r"(?<![a-z])[Pp]eriodo"),
    ("«período» (con tilde)", r"per[ií]odo".replace("[ií]", "í")),
    ("«naive»/«naïve»", r"[Nn]a[iï]ve"),
    ("«deriva»", r"deriva"),
    ("«drift» (ingles)", r"\bdrift\b"),
    ("«sobrediferenciacion»", r"sobrediferenci"),
    ("«diferenciar de mas / una de mas»", r"de más"),
    ("«Modulo N» en prosa", r"M[oó]dulo \d"),
    ("«4.N»/«3.N» como cita de modulo", r"\b[34]\.\d{1,2}\b(?!\d)"),
    ("«Capitulo N»", r"Cap[ií]tulo \d"),
    ("«criterio de la varianza» / «regla de la varianza»", r"(criterio|regla) de la varianza"),
]
for nombre, rx in GRUPOS:
    tot, det = por_modulo(rx)
    print(f"{nombre}: total {tot}  {det}")

print()
print("== «abanico»: sentidos (lineas de prosa del modulo) ==")
for i in todas(r"abanico"):
    l = _html.unescape(re.sub(r"<[^>]+>", " ", lineas[i - 1])).strip()
    print(f"  {i} (M{modulo(i)}): {l[:110]}")

# --- Anglicismos e ingles sin traducir en prosa (revision a ojo de esta lista) --------------
print()
print("== Ingles en la prosa (fuera de <pre>, <code>, titulos «/ English» y componentes de codigo) ==")
EN = re.compile(r"\b(trace|stepwise|drift|airline|backtesting|lag|default|feedback|input|output|setup|performance|"
                r"benchmark|overfitting|burn-in|forecast|naïve|rolling|cut-off|outlier|trend|fit|plot)\b", re.I)
vistos = {}
texto_mod = {}
for m in re.finditer(r'<template id="module-(\d+)">(.*?)</template>', "\n".join(lineas), re.S):
    k = int(m.group(1))
    h = m.group(2)
    h = re.sub(r"<pre\b.*?</pre>", " ", h, flags=re.S)
    h = re.sub(r"<code\b.*?</code>", " ", h, flags=re.S)
    h = re.sub(r'<span class="text-gray-400 font-normal text-2xl">.*?</span>', " ", h, flags=re.S)
    h = re.sub(r"\$\$.*?\$\$", " ", h, flags=re.S)
    h = re.sub(r"\$[^$]*\$", " ", h)
    t = _html.unescape(re.sub(r"<[^>]+>", " ", h))
    texto_mod[k] = t
    for w in EN.findall(t):
        vistos.setdefault(w.lower(), {}).setdefault(k, 0)
        vistos[w.lower()][k] += 1
for w, d in sorted(vistos.items()):
    print(f"  {w}: " + " ".join(f"M{k}:{v}" for k, v in sorted(d.items())))
# expresiones en cursiva en ingles, entre <em>
print("  Expresiones entre <em> con aspecto de ingles (revisadas a ojo):")
for m in re.finditer(r'<template id="module-(\d+)">(.*?)</template>', "\n".join(lineas), re.S):
    k = int(m.group(1))
    h = re.sub(r"<pre\b.*?</pre>", " ", m.group(2), flags=re.S)
    cand = re.findall(r"<em[^>]*>([^<]{3,60})</em>", h)
    ing = [c for c in cand if re.search(r"\b(the|of|and|integrated|autoregressive|moving|average|drift|airline|seasonality|cycle|No drift|naïve|naive)\b", c, re.I)]
    if ing:
        print(f"   M{k}: {ing}")

# --- Voz -----------------------------------------------------------------------------------------
# Formas de segunda persona del singular SIN ambiguedad con la tercera (te, tu, puedes, tienes...) mas los
# imperativos al INICIO de oracion o tras «:» / «—» (Cambia, Sube, Mira...). «usa», «deja», «prueba»,
# «cambia» en minuscula se excluyen: pueden ser tercera persona o sustantivo.
tu_fijo = re.compile(r"\b(te|tu|tus|tú|fíjate|puedes|tienes|necesitas|quieres|verás|podrás|tendrás|aprendiste|"
                     r"respondiste|resolviste|acabas|contrástalo|repítelo|hazlo|haz|relee|piensa|comprueba)\b", re.I)
tu_imper = re.compile(r"(?:(?<=[.:¿¡—»])|^)\s*(Cambia|Sube|Baja|Mira|Empieza|Mueve|Elige|Prueba|Busca|Lee|Marca|Responde|"
                      r"Anota|Toma|Trabaja|Aplica|Ajusta|Apunta|Usa|Recuerda|Compara|Ordena|Pide|Deja|Calcula|Escribe|"
                      r"Haz|Pon|Ten|Hazlo|Repítelo|Cuidado)\b")
nos = re.compile(r"\b(pongamos|apliquemos|retomemos|empecemos|volvamos|miremos|veamos|recordemos|tomemos|"
                 r"consideremos|supongamos|llamemos|escribamos|calculemos)\b", re.I)
print()
print("== Voz (formas inequivocas de segunda persona del singular / primera del plural) por modulo ==")
print("   (prosa y notas, sin codigo; los «simulador-intro» y los ejercicios del M10 van aparte)")
ejemplos_voz = {}
for m in re.finditer(r'<template id="module-(\d+)">(.*?)</template>', "\n".join(lineas), re.S):
    k = int(m.group(1))
    h = m.group(2)
    intros = " ".join(re.findall(r'<p class="simulador-intro">(.*?)</p>', h, flags=re.S))
    h = re.sub(r'<p class="simulador-intro">.*?</p>', " ", h, flags=re.S)
    ejer = ""
    if k == 10:
        mm = re.search(r'<h3>Ejercicios propuestos</h3>(.*?)<h3>Lecturas</h3>', h, flags=re.S)
        if mm:
            ejer = mm.group(1)
            h = h.replace(mm.group(1), " ")
    h = re.sub(r"<pre\b.*?</pre>", " ", h, flags=re.S)
    h = re.sub(r"<button\b.*?</button>", " ", h, flags=re.S)

    def limpia(x):
        x = re.sub(r"<pre\b.*?</pre>", " ", x, flags=re.S)
        x = _html.unescape(re.sub(r"<[^>]+>", " ", x))
        x = re.sub(r"\$\$.*?\$\$", " ", x, flags=re.S)
        x = re.sub(r"\$[^$]*\$", " ", x)
        return re.sub(r"\s+", " ", x)

    def cuenta(t):
        a = [x.lower() for x in tu_fijo.findall(t)]
        b = [x for x in tu_imper.findall(t)]
        return len(a) + len(b), (a + b)[:6]

    t, ti, te = limpia(h), limpia(intros), limpia(ejer)
    n1, e1 = cuenta(t)
    n2, e2 = cuenta(ti)
    n3, e3 = cuenta(te)
    print(f"M{k}: prosa {n1} {e1} | plural {len(nos.findall(t))} | intros de simulador {n2} {e2} | ejercicios {n3}")
