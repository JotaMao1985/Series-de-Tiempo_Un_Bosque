#!/usr/bin/env python3
"""V3 · minutos por módulo, con un analizador de HTML (html.parser) en vez de expresiones regulares: reimplementación
independiente de r3_minutos.py. Misma fórmula (la de los capítulos 1 a 3): palabras de prosa / 180 + 3 por simulador + 2 por
bloque de código. Convenio «abierto»: cuenta la pista y la solución de los ejercicios; no cuenta <pre>, <script>, <style>, <canvas>,
<svg>, <button>, el <caption class="sr-only">, los desarrollos plegados, la autoevaluación ni el simulacro; $$...$$ fuera y cada
$...$ en línea cuenta como una palabra; el `$` dentro de <code> no es delimitador.
Uso: python3 v3_minutos.py [ruta.html]"""
import html as H, re, sys, pathlib
from html.parser import HTMLParser

RAIZ = pathlib.Path(__file__).resolve().parents[3]
ruta = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "Htmls_Series" / "capitulo-4-modelos-arima.html"
src = ruta.read_text(encoding="utf-8")


class P(HTMLParser):
    def __init__(self, abierto=True):
        super().__init__(convert_charrefs=True)
        self.abierto = abierto
        self.pila = []            # (etiqueta, excluye?) para saber cuándo salimos de un contenedor excluido
        self.excl = 0
        self.en_code = 0
        self.trozos = []
        self.sims = 0
        self.tabs = 0
        self.pres = 0

    def _excluye(self, tag, a):
        cls = (a.get("class") or "").split()
        if tag in ("pre", "script", "style", "canvas", "svg", "button"):
            return True
        if tag == "caption" and "sr-only" in cls:
            return True
        if tag == "div" and any(c in cls for c in ("derivacion", "quiz", "simulacro")):
            return True
        if tag == "div" and not self.abierto and any(c.startswith("ejercicio-panel") for c in cls):
            return True
        return False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("br", "hr", "img", "input", "meta", "link"):
            return
        if tag == "div" and a.get("data-simulador") and not a["data-simulador"].endswith("simulacro"):
            self.sims += 1
        cls = (a.get("class") or "").split()
        if tag == "div" and "code-tabs" in cls:
            self.tabs += 1
        if tag == "pre":
            self.pres += 1
        ex = self._excluye(tag, a)
        self.pila.append((tag, ex))
        if ex:
            self.excl += 1
        if tag == "code":
            self.en_code += 1
        if tag in ("p", "div", "li", "tr", "h3", "h4", "table", "ul"):
            self.trozos.append(" ")

    def handle_endtag(self, tag):
        # cierra hasta la etiqueta correspondiente
        for i in range(len(self.pila) - 1, -1, -1):
            if self.pila[i][0] == tag:
                for t, ex in self.pila[i:]:
                    if ex:
                        self.excl -= 1
                    if t == "code":
                        self.en_code -= 1
                del self.pila[i:]
                break

    def handle_data(self, d):
        if self.excl:
            return
        if self.en_code:
            d = d.replace("$", "¤")
        self.trozos.append(d)

    def palabras(self):
        t = "".join(self.trozos)
        t = re.sub(r"\$\$.*?\$\$", " ", t, flags=re.S)
        t = re.sub(r"\$[^$]*\$", " M ", t)
        t = t.replace("¤", "$").replace("\xa0", " ")
        return len(t.split())


decl = {int(k): int(v) for k, v in re.findall(r'\{ id: (\d+), title: "[^"]*", shortTitle: "[^"]*", duration: "(\d+) min" \}', src)}
print("mód | palabras cerr./abierto | sims | bloques de código | min cerrado | min abierto | declarado | dist.")
tot = [0, 0, 0]
for m in re.finditer(r'<template id="module-(\d+)">(.*?)</template>', src, re.S):
    k = int(m.group(1)); h = m.group(2)
    res = {}
    for abierto in (False, True):
        p = P(abierto); p.feed(h); res[abierto] = p
    pa = res[True]
    cod = pa.tabs + (pa.pres - 2 * pa.tabs)
    w_c, w_a = res[False].palabras(), pa.palabras()
    mc = w_c / 180 + 3 * pa.sims + 2 * cod
    ma = w_a / 180 + 3 * pa.sims + 2 * cod
    d = decl.get(k)
    print(f"M{k:<2} | {w_c:5d} {w_a:5d}          | {pa.sims:3d}  | {cod:3d}               | {mc:5.1f}       | {ma:5.1f}       | {d:3d}       | {ma - d:+5.1f}")
    if k <= 9:
        tot[0] += ma; tot[1] += d
    if k == 10:
        tot[2] = (ma, d)
print(f"M1–M9: medido abierto {tot[0]:.1f}, declarado {tot[1]}; M10: medido abierto {tot[2][0]:.1f}, declarado {tot[2][1]}; M1–M10 medido {tot[0]+tot[2][0]:.1f}, declarado {tot[1]+tot[2][1]}")
