#!/usr/bin/env python3
"""Verificador independiente · R1 cap. 2 · paridad de `$` (KaTeX en línea) en los
párrafos, celdas y elementos de lista de los módulos y en las cadenas del quiz,
sin contar los bloques de código ni los `$$`. Un número impar rompe el render."""
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
ini, fin = t.index('<template id="module-1">'), t.index('</template>', t.index('<template id="module-9">'))
mods = re.sub(r"<pre><code.*?</code></pre>", "", t[ini:fin], flags=re.S)
malos = 0
for m in re.finditer(r"<(p|li|td|th|h4)\b[^>]*>(.*?)</\1>", mods, re.S):
    s = m.group(2).replace("$$", "").replace("\\$", "")
    if s.count("$") % 2:
        malos += 1; print("IMPAR:", re.sub(r"\s+", " ", s)[:160])
q0 = t.index("AUTOEVALUACIONES['cap2']"); q = t[q0:t.index("];", q0)]
for m in re.finditer(r"'((?:[^'\\]|\\.)*)'", q):
    s = m.group(1).replace("$$", "")
    if s.count("$") % 2:
        malos += 1; print("IMPAR (quiz):", s[:160])
print("elementos con $ impar:", malos)
