#!/usr/bin/env python3
"""Lector-estudiante · terminos usados antes de definirse y notacion que cambia (capitulo 3).

Uso:  python3 -I lector_terminos.py ruta/capitulo-3-modelos-ar-ma-arma.html

Lee SOLO los once <template id="module-N"> (lo que el estudiante lee), no el JS ni el CSS.
Para cada termino da: primera linea en que aparece (con su modulo), la linea de su definicion
(fijada a mano tras leer el marcado: la columna «def.» no es un hallazgo del guion, es lo que se
leyo) y cuantas lineas la separan. Despues cuenta variantes de notacion y de vocabulario por modulo.
"""
import re
import sys

ruta = sys.argv[1]
lineas = open(ruta, encoding="utf-8").read().split("\n")

# rangos de cada modulo (linea 1-based de <template id="module-N"> a </template>)
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


# (termino, regex del primer uso, linea de la definicion leida a mano, nota)
TERMINOS = [
    ("AR(p) / «un AR» como modelo", r"un AR queda|AR\(\$?p", 2965, "M1 2740 «un AR queda… un MA queda»; se define en M2 (2965)"),
    ("MA(q) / «un MA» como modelo", r"un MA queda|\bMA\(\$?q|y_t = \\theta\(B\)", 3293, "M1 2740; se define en M3 (3293)"),
    ("ARMA(1,1) (estimado con arima())", r"ARMA\(1,1\)|ar = 0\.6, ma = 0\.7", 3902, "M1 2764 (codigo con salida); se define en M5 (3902)"),
    ("φ(B), θ(B) «autorregresivo/medias moviles»", r"autorregresivo</strong> de orden", 2731, "M1 2731 los define; AR y MA aun no existen"),
    ("raiz unitaria / caminata (cap. 2)", r"ra[ií]z unitaria", 2887, "ya viene del cap. 2 (M5, 3402); aqui se recuerda en M1 2887"),
    ("invertible / invertibilidad", r"invertib", 3431, "M3 objetivo (3281) y simulador (3370) la usan; definicion en 3431"),
    ("MA(∞) / AR(∞)", r"MA\(\$?\\infty|AR\(\$?\\infty", 3598, "M1 2880 y M3 3426 la citan «del Modulo 4»; se define en M4 (3598)"),
    ("pseudo-ciclo / pseudo-periodo", r"pseudo-ciclo|pseudo-periodo", 3023, "M2 3023 lo nombra; M2 3043 «cuyo periodo aparece en la lectura»"),
    ("Yule–Walker (nombre)", r"Yule", 3128, "M2 3126 es el titulo; el modelo de Yule (1927) llega en M7"),
    ("Ljung–Box", r"Ljung", 4875, "M5 4007 (ciclo, paso 4, con fitdf); M6 4532; se define en M8 (4875)"),
    ("fitdf", r"fitdf", 4917, "M5 4007; explicado en el plegado de M8 (4917)"),
    ("AICc / BIC", r"AICc|BIC", 4839, "M5 3993 (ciclo) y 4377 (codigo, funcion aicc propia); M7 4707; se define en M8 (4839)"),
    ("banda de Bartlett", r"Bartlett", None, "M5 3965; no se define en ningun sitio"),
    ("auto.arima", r"auto\.arima", None, "M9 5533 y 5550; sin definicion y sin llamada en el codigo del modulo"),
    ("psi / pi (pesos)", r"\\psi|\\pi_", 3610, "M4 los nombra (3585, 3610); M3 ya los usa en 3555 (pesos de la reescritura AR(inf)) sin nombrarlos"),
    ("«identificar» (orden) / «identificado» (parametros)", r"identificad", 3919, "M3 3363 «el modelo no esta identificado» (identificabilidad); M5 3919 «identificar» (elegir p y q)"),
    ("AirPassengers", r"AirPassengers", None, "no aparece en los once modulos: el hilo del cap. 2 (∇∇12 log AirPassengers) no vuelve"),
    ("sobrediferenciacion", r"sobrediferenci", None, "solo en la actividad preparatoria (6223); el «adelanto» del cap. 2 (θ = −1) no se retoma en M3"),
]

print("termino | primer uso (linea, modulo) | definicion (linea, modulo) | distancia en lineas | nota")
for nombre, rx, defin, nota in TERMINOS:
    p = primera(rx)
    mp = modulo(p) if p else None
    md = modulo(defin) if defin else None
    dist = (defin - p) if (p and defin) else None
    print(f"{nombre} | {p} (M{mp}) | {defin if defin else '—'} (M{md if md else '—'}) | "
          f"{dist if dist is not None else '—'} | {nota}")

print()
print("== Notacion y vocabulario por modulo (numero de lineas con la forma) ==")


def por_modulo(regex):
    c = {}
    for i in todas(regex):
        k = modulo(i)
        c[k] = c.get(k, 0) + 1
    return " ".join(f"M{k}:{v}" for k, v in sorted(c.items())) or "—"


GRUPOS = [
    ("tamano de muestra «T» (math)", r"\$T\$|\bT =|\bT = |\\sqrt\{T\}|T\s*=\s*\d"),
    ("tamano de muestra «n» (math)", r"\$n\$|\bn =|\\sqrt\{n\}|\$n\s*=\s*\d|n = \d"),
    ("banda con √T", r"1\.96/\\sqrt\{T\}"),
    ("banda con √n", r"1\.96/\\sqrt\{n\}"),
    ("«caminata aleatoria»", r"caminata aleatoria"),
    ("«paseo aleatorio»", r"paseo aleatorio"),
    ("«residuales»", r"residuales"),
    ("«residuos»", r"residuos\b"),
    ("«abanico»", r"abanico"),
    ("«periodo» (sin pseudo)", r"(?<!pseudo-)\bperiodo"),
    ("«pseudo-ciclo»", r"pseudo-ciclo"),
    ("«pseudo-periodo»", r"pseudo-periodo"),
    ("«envolvente» (genero)", r"envolvente"),
    ("«Modulo N» en prosa", r"M[oó]dulo \d"),
    ("«3.N» / «2.N» como cita de modulo", r"\b[23]\.\d\b"),
]
for nombre, rx in GRUPOS:
    print(f"{nombre}: {por_modulo(rx)}")

print()
print("== «ARMA» como concepto (no como nombre de funcion: ARMAacf, ARMAtoMA) antes de la definicion en M5 (3902) ==")
usos = [i for i in todas(r"\bARMA\b(?!acf|toMA)|ARMA\(") if modulo(i) and modulo(i) < 5]
por = {}
for i in usos:
    por.setdefault(modulo(i), []).append(i)
for k, v in sorted(por.items()):
    print(f"  M{k}: {len(v)} lineas (primera {v[0]})")


# --- Voz: recuento aproximado sobre el texto de cada modulo ---------------------------------
# Se quitan las introducciones de simulador, el codigo y los botones; en el M10 tambien los
# ejercicios guiados. Segunda persona del singular y primera del plural, por expresion regular.
import html as _html
texto = "\n".join(lineas)
tu = re.compile(r"\b(te|tu|tus|tú|ves|f[ií]jate|recuerda|comprueba|compru[eé]balo|mira|pon|relee|piensa|"
                r"verás|podrás|puedes|tienes|tendrás|necesitas|quieres)\b", re.I)
nos = re.compile(r"\b(\w+(?:amos|emos)|pongamos|apliquemos|retomemos|empecemos|volvamos|miremos|veamos|"
                 r"recordemos)\b", re.I)
print()
print("== Voz (aproximada): segunda persona del singular / primera del plural por modulo ==")
for m in re.finditer(r'<template id="module-(\d+)">(.*?)</template>', texto, re.S):
    k = int(m.group(1))
    h = m.group(2)
    h = re.sub(r'<p class="simulador-intro">.*?</p>', " ", h, flags=re.S)
    if k == 10:
        h = re.sub(r'<div class="ejercicio-guiado".*?(?=<h3>|<div class="exercise"|<div class="note">|$)', " ", h, flags=re.S)
    h = re.sub(r"<pre\b.*?</pre>", " ", h, flags=re.S)
    h = re.sub(r"<button\b.*?</button>", " ", h, flags=re.S)
    t = _html.unescape(re.sub(r"<[^>]+>", " ", h))
    t = re.sub(r"\$\$.*?\$\$", " ", t, flags=re.S)
    t = re.sub(r"\$[^$]*\$", " ", t)
    ej = [x.lower() for x in tu.findall(t)][:6]
    print(f"M{k}: tu {len(tu.findall(t))}, plural {len(nos.findall(t))}  {ej}")
