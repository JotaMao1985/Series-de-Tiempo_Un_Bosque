#!/usr/bin/env python3
"""Lector-estudiante (cap. 5) · terminos usados antes de definirse, remisiones, notacion, registro y voz.

Uso:  python3 -I lector_terminos.py ruta/capitulo-5-sarima.html

Adaptado de `diagnostico/cap4/diag/lector_terminos.py` (mismo metodo). Lee SOLO los doce <template id="module-N">
(lo que el estudiante lee), no el JS ni el CSS; el texto que genera el JS (lecturas, rotulos) se mira aparte, a mano.
Para cada termino: primera linea de uso (con su modulo), linea de su presentacion (fijada a mano tras leer el marcado:
la columna «def.» no es un hallazgo del guion) y la distancia. Despues: remisiones «Modulo N» hacia delante y atras,
atribuciones a otros capitulos, variantes de notacion y de vocabulario por modulo, ingles, registro informal y voz.
"""
import html as _html
import re
import sys

ruta = sys.argv[1]
texto_total = open(ruta, encoding="utf-8").read()
lineas = texto_total.split("\n")

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


def fuera_de_estructura(l):
    """Lineas que son clases CSS / atributos aria / comentarios y no prosa."""
    return bool(re.search(r'class="mapa-estacional|aria-label=|data-simulador|<canvas', l)) and "<p" not in l


def primera(regex, desde=1):
    pat = re.compile(regex)
    for i, l in enumerate(lineas, 1):
        if i < desde or modulo(i) is None or fuera_de_estructura(l):
            continue
        if pat.search(l):
            return i
    return None


def todas(regex):
    pat = re.compile(regex)
    return [i for i, l in enumerate(lineas, 1) if modulo(i) and pat.search(l) and not fuera_de_estructura(l)]


# (termino, regex del primer uso, linea de la presentacion leida a mano, nota)
TERMINOS = [
    ("airline (el modelo)", r"airline", 4527,
     "M1 3080 («el modelo airline, con solo dos parametros»); M2 lo usa 6 veces antes del M5; el cap. 4 (puente) ya lo dio como «avance»; la caja que lo define con su nombre de origen esta en el M5"),
    ("∇ (diferencia regular)", r"\\nabla", None,
     "M1 3145 («∇TRM») y los selectores del simulador del M1; nunca se define en el capitulo como objeto (∇ = 1 - B); solo ∇_m se define (M3 3776). M2 3548 escribe w_t = ∇^d ∇_m^D y_t"),
    ("∇_m (diferencia estacional) y ∇∇₁₂", r"\\nabla_\{?m|\\nabla_\{12|nabla\\nabla_", 3776,
     "primer uso M2 (3360 «∇∇₁₂ del Modulo 3» y 3548); M1 ya habla de «las dos diferencias» en el simulador (3109)"),
    ("ETS / ETS(M,A,M)", r"\bETS\b", None,
     "M11 5712 («el ETS, en las dos escalas»); no se presenta en ningun modulo; solo la tabla de 5832 lo glosa («Holt–Winters y familia», «suavizamiento exponencial»); la notacion (M,A,M) y A_d no se explica"),
    ("naïve estacional", r"[Nn]a[iï]ve", None,
     "M11 5750 (fila de la tabla); no se define en el cap. 5 (el cap. 4 lo nombra; el cap. 6 lo desarrolla)"),
    ("USAccDeaths (la serie)", r"USAccDeaths", 4549,
     "M1 3142 (fila de la tabla), M3 4078; se describe por primera vez en la tabla del M5 4549 («Muertes accidentales en EE. UU., 1973–1978»); el M8 5097 la «presenta» de nuevo"),
    ("co2 (la serie)", r"\bco2\b", 5912,
     "M1 3143 (fila de la tabla, «Mauna Loa»), M8 5117 (tabla); se presenta como ejercicio 1 en M11 5912 (n = 468)"),
    ("RMSE / MAE / MAPE", r"RMSE", None,
     "M9 5373 («RMSE 45.48 frente a 43.18»); la tabla del M11 5740 las da sin definirlas; el cap. 4 usa RMSE/MAE en su M8; el cap. 6 las desarrolla"),
    ("«fuera de muestra»", r"fuera de muestra", 5711,
     "M9 5372 (advertencia que remite al M11); M10 5574 («solo fuera de muestra, que es el Modulo 11»); M11 5711 lo hace (entrenar 120, medir 24)"),
    ("«origen(es)» / origen movil", r"or[ií]genes|origen m[oó]vil", 5761,
     "M11 5761 («61 orígenes… avanzando el corte mes a mes»): se explica en la misma frase; el cap. 6 lo desarrolla"),
    ("Fourier (regresion armonica)", r"Fourier", 5524,
     "primer uso M10 5485 (titulo) y la tabla de 5509; la definicion es 5524"),
    ("STL", r"\bSTL\b", None, "M3 4204 (la trampa de nsdiffs «fuerza estacional de la descomposicion STL»); cap. 1 la desarrolla; M10 5580 la usa con remision al Capitulo 1"),
    ("Box–Cox / BoxCox.lambda()", r"Box.Cox|BoxCox", None, "M4 4332 y 4376 (ciclo, «¿Log o Box–Cox?»); no se usa en ningun bloque; cap. 2 (2.8) lo presenta"),
    ("checkresiduals()", r"checkresiduals", 4998, "primer uso = M7 4998, con su glosa en el comentario del bloque («grafico + Ljung-Box en una sola llamada»)"),
    ("rango relativo (1.848)", r"rango relativo", None, "M7 4815; no se define en ningun modulo; ningun bloque lo calcula (resulta ser (max - min)/media)"),
    ("rejilla (de candidatos)", r"rejilla de candidatos|La rejilla|rejilla de abajo|rejilla SARIMA", 4650,
     "M4 4428 (ciclo, etapa 5) la usa antes de que el M6 (4650) la presente; en M1 y M3 «rejilla» es una clase CSS del mapa, no prosa"),
    ("satelite(s) (rezagos satelite)", r"sat[eé]lite", 3331, "primer uso = presentacion (M2 3331, con ejemplo numerico)"),
    ("n efectivo", r"n efectivo|observaciones que quedan", 4648,
     "M3 4056 (tabla con la columna n); M6 4648 lo explica; el cap. 4 presenta n* = n - d (aqui no se reutiliza el simbolo)"),
    ("ndiffs() / nsdiffs()", r"ndiffs|nsdiffs", None, "M3 4078/4125; cap. 2 (4120–4130) los presenta; nsdiffs con test = 'seas'/'ocsb': M3 4203 (trampa de version)"),
    ("SARIMAX (clase de statsmodels)", r"SARIMAX", 5318,
     "M2 3663 (bloque Python: `SARIMAX(...)` para ajustar el airline); el M9 (5318) lo define como «regresion con errores SARIMA» y avisa que el nombre engana"),
    ("Holt–Winters / suavizamiento exponencial", r"Holt|suavizamiento", None, "solo M11 5832–5833 (tabla); ni el cap. 5 ni los caps. 1–3 lo presentan"),
    ("Prophet / LSTM / Transformers / TBATS", r"Prophet|LSTM|Transformer|TBATS", None, "solo M11 5844–5859 y la lista de lecturas (TBATS 6180); sin presentacion"),
    ("competencias M4 y M5", r"competencias M4", None, "M11 5869: sin presentar (que son, quien las organizo)"),
    ("cobertura (empirica / nominal)", r"cobertura", None, "M11 5807 (nota puente); la desarrolla el cap. 6"),
    ("«once módulos» (M11 5755)", r"once m[oó]dulos", None, "M11 5755: «el modelo que ha ocupado once módulos»; hay diez antes del 11"),
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
print("== Remisiones «Modulo N» (hacia delante / hacia atras) por modulo, con linea ==")
pat = re.compile(r"M[oó]dulos? (\d+)(?:\s*(?:,|y|a)\s*(\d+))?")
adelante, atras, lista = {}, {}, []
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
    a, b = adelante.get(k, []), atras.get(k, [])
    print(f"M{k}: hacia delante {len(a)} {[f'{i}->M{n}' for i, n in a]} ; hacia atras {len(b)} {[f'{i}->M{n}' for i, n in b]}")
print()
print("Veces que cada modulo es citado desde otro (hacia delante / hacia atras):")
for n in range(1, 13):
    d = [i for (k, i, t) in lista if t == n and k < n]
    a = [i for (k, i, t) in lista if t == n and k > n]
    print(f"  M{n}: desde modulos anteriores {len(d)} {d} | desde posteriores {len(a)}")

# --- Atribuciones a otros capitulos -------------------------------------------------------------
print()
print("== «Capitulo N» en la prosa (linea, modulo, fragmento) ==")
for i in todas(r"Cap[ií]tulos? \d"):
    l = _html.unescape(re.sub(r"<[^>]+>", " ", lineas[i - 1]))
    l = re.sub(r"\s+", " ", l).strip()
    for m in re.finditer(r"Cap[ií]tulos? \d[^.;]{0,90}", l):
        print(f"  {i} (M{modulo(i)}): {m.group(0)[:110]}")
        break

# --- Notacion y vocabulario por modulo ---------------------------------------------------------
print()
print("== Notacion y vocabulario por modulo (numero de apariciones, solo el marcado de los modulos) ==")


def por_modulo(regex):
    c = {}
    pat2 = re.compile(regex)
    for i, l in enumerate(lineas, 1):
        k = modulo(i)
        if k is None or fuera_de_estructura(l):
            continue
        n = len(pat2.findall(l))
        if n:
            c[k] = c.get(k, 0) + n
    return (sum(c.values()), " ".join(f"M{k}:{v}" for k, v in sorted(c.items())) or "—")


GRUPOS = [
    ("autocorrelacion muestral «\\hat\\rho_k»", r"\\hat\\rho"),
    ("autocorrelacion muestral «r_k» / «\\hat r»", r"\\hat r_|\$r_\{?\d|\br_\{?1"),
    ("tamano de muestra «n» (math)", r"\$n\$|\$n\s*=|\bn\s*=\s*\d|\\sqrt\{n\}"),
    ("tamano de muestra «T» (math)", r"\$T\$|\\sqrt\{T\}|\bT\s*=\s*\d"),
    ("proceso de errores «n_t» (choca con n; sin contar \\varepsilon_t)", r"(?<![A-Za-z\\])n_t\b"),
    ("«residuales»", r"residuales"),
    ("«residuos»", r"residuos\b"),
    ("«periodo» (sin tilde)", r"(?<![a-z])[Pp]eriodo"),
    ("«período» (con tilde)", r"per[ií]odo".replace("[ií]", "í")),
    ("«diferencia doble / doble diferencia»", r"diferencia doble|doble diferencia"),
    ("«las dos diferencias»", r"las dos diferencias|ambas diferencias"),
    ("«caminata (aleatoria)»", r"[Cc]aminata"),
    ("«satélite(s)»", r"sat[eé]lite"),
    ("«airline» en cursiva", r"<em>[Aa]irline</em>"),
    ("«airline» sin cursiva", r"(?<![>\w])airline(?![\w<])"),
    ("«estacionalidad»", r"estacionalidad"),
    ("«estación» (corto)", r"\bestación\b"),
    ("«parte estacional / término estacional»", r"parte estacional|t[eé]rmino estacional"),
    ("«tendencia» / «deriva»", r"tendencia"),
    ("«|raíz MA|^-1» o «módulo inverso»", r"raíz MA\|\^|m[oó]dulo inverso"),
    ("«Módulo N» en prosa", r"M[oó]dulo \d"),
    ("«5.N»/«4.N» como cita de modulo", r"\b[45]\.\d{1,2}\b(?!\d)"),
    ("«Capítulo N»", r"Cap[ií]tulo \d"),
    ("«evidencias» / «pruebas»", r"evidencias?|pruebas?"),
    ("«tres/cuatro evidencias»", r"(tres|cuatro|dos) evidencias"),
]
for nombre, rx in GRUPOS:
    tot, det = por_modulo(rx)
    print(f"{nombre}: total {tot}  {det}")

# --- Ingles y registro ------------------------------------------------------------------------
print()
print("== Ingles en la prosa (fuera de <pre>, <code>, titulos «/ English» y formulas) ==")
EN = re.compile(r"\b(trace|stepwise|drift|airline|backtesting|lag|default|feedback|input|output|setup|performance|"
                r"benchmark|overfitting|burn-in|forecast|forecasting|naïve|rolling|cut-off|outlier|trend|fit|plot|tuneo|"
                r"brilla|seasonal|seasonality|cycle|warning|spike|check|score|boost)\b", re.I)
texto_mod = {}
for m in re.finditer(r'<template id="module-(\d+)">(.*?)</template>', texto_total, re.S):
    k = int(m.group(1))
    h = m.group(2)
    h = re.sub(r"<pre\b.*?</pre>", " ", h, flags=re.S)
    h = re.sub(r"<code\b.*?</code>", " ", h, flags=re.S)
    h = re.sub(r'<span class="text-gray-400 font-normal text-2xl">.*?</span>', " ", h, flags=re.S)
    h = re.sub(r"\$\$.*?\$\$", " ", h, flags=re.S)
    h = re.sub(r"\$[^$]*\$", " ", h)
    t = _html.unescape(re.sub(r"<[^>]+>", " ", h))
    texto_mod[k] = t
vistos = {}
for k, t in texto_mod.items():
    for w in EN.findall(t):
        vistos.setdefault(w.lower(), {}).setdefault(k, 0)
        vistos[w.lower()][k] += 1
for w, d in sorted(vistos.items()):
    print(f"  {w}: " + " ".join(f"M{k}:{v}" for k, v in sorted(d.items())))
print("  Expresiones entre <em> con aspecto de ingles:")
for m in re.finditer(r'<template id="module-(\d+)">(.*?)</template>', texto_total, re.S):
    k = int(m.group(1))
    h = re.sub(r"<pre\b.*?</pre>", " ", m.group(2), flags=re.S)
    cand = re.findall(r"<em[^>]*>([^<]{3,60})</em>", h)
    ing = [c for c in cand if re.search(r"\b(the|of|and|seasonality|cycle|signature|notation|model|drift|forecast)\b", c, re.I)]
    if ing:
        print(f"   M{k}: {ing}")
print()
print("== Registro informal o coloquial en la prosa (lineas) ==")
INFORMAL = [r"algo bonito", r"de otro planeta", r"demoledora", r"hacer trampa", r"un lector razonable", r"tuneo",
            r"brilla", r"de cabeza", r"a mano", r"el error m[aá]s caro", r"rar[ií]simo", r"por goleada", r"no es un fallo"]
for rx in INFORMAL:
    ls = todas(rx)
    if ls:
        print(f"  «{rx}»: " + ", ".join(f"{i}(M{modulo(i)})" for i in ls))

# --- Voz -----------------------------------------------------------------------------------------
tu_fijo = re.compile(r"\b(te|tu|tus|tú|fíjate|puedes|tienes|necesitas|quieres|verás|podrás|tendrás|aprendiste|"
                     r"respondiste|resolviste|acabas|contrástalo|repítelo|hazlo|haz|relee|piensa|comprueba|habrías|"
                     r"mira|sales|cierres|pulsa|teclea|hazlo)\b", re.I)
tu_imper = re.compile(r"(?:(?<=[.:¿¡—»])|^)\s*(Cambia|Sube|Baja|Mira|Empieza|Mueve|Elige|Prueba|Busca|Lee|Marca|Responde|"
                      r"Anota|Toma|Trabaja|Aplica|Ajusta|Apunta|Usa|Recuerda|Compara|Ordena|Pide|Deja|Calcula|Escribe|"
                      r"Haz|Pon|Ten|Hazlo|Repítelo|Cuidado|Lleva|Fíjate|Pulsa|Teclea|Descarga)\b")
nos = re.compile(r"\b(pongamos|apliquemos|retomemos|empecemos|volvamos|miremos|veamos|recordemos|tomemos|consideremos|"
                 r"supongamos|llamemos|escribamos|calculemos|tomamos|multiplicamos|escribimos|hemos|acabamos|"
                 r"construimos|obtenemos|vemos|usamos|imponemos|estimamos|llegamos|dejamos|queremos|sabemos|podemos)\b", re.I)
print()
print("== Voz: 2.ª persona del singular y 1.ª del plural (formas inequivocas) por modulo ==")
for m in re.finditer(r'<template id="module-(\d+)">(.*?)</template>', texto_total, re.S):
    k = int(m.group(1))
    h = m.group(2)
    intros = " ".join(re.findall(r'<p class="simulador-intro">(.*?)</p>', h, flags=re.S))
    h = re.sub(r'<p class="simulador-intro">.*?</p>', " ", h, flags=re.S)
    ciclo = " ".join(re.findall(r'<div class="ciclo".*?(?=\n      <div class="code-tabs">)', h, flags=re.S))
    h = re.sub(r'<div class="ciclo".*?(?=\n      <div class="code-tabs">)', " ", h, flags=re.S)
    ejer = ""
    if k == 11:
        mm = re.search(r'<h3>Ejercicios propuestos</h3>(.*?)<h3>Lecturas</h3>', h, flags=re.S)
        if mm:
            ejer = mm.group(1)
            h = h.replace(mm.group(1), " ")

    def limpia(x):
        x = re.sub(r"<pre\b.*?</pre>", " ", x, flags=re.S)
        x = re.sub(r"<button\b.*?</button>", " ", x, flags=re.S)
        x = _html.unescape(re.sub(r"<[^>]+>", " ", x))
        x = re.sub(r"\$\$.*?\$\$", " ", x, flags=re.S)
        x = re.sub(r"\$[^$]*\$", " ", x)
        return re.sub(r"\s+", " ", x)

    def cuenta(t):
        a = [x.lower() for x in tu_fijo.findall(t)]
        b = [x for x in tu_imper.findall(t)]
        return len(a) + len(b), (a + b)[:7]

    t, ti, tc, te = limpia(h), limpia(intros), limpia(ciclo), limpia(ejer)
    n1, e1 = cuenta(t)
    n2, e2 = cuenta(ti)
    n3, e3 = cuenta(tc)
    n4, e4 = cuenta(te)
    pl = [x.lower() for x in nos.findall(t)]
    print(f"M{k}: prosa {n1} {e1} | plural {len(pl)} {pl[:6]} | intros de simulador {n2} {e2} | ciclo {n3} | ejercicios {n4}")
