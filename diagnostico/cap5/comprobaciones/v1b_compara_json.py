"""Verificador B, R1 del cap. 5: qué hojas cambian en cap5_sarima.json y en cap5_datos.js
entre 7686d33 y el árbol de trabajo, y (si se le pasa) entre el árbol y una regeneración
hecha fuera del repo.

Uso: python3 v1b_compara_json.py [ruta_json_regenerado ruta_js_regenerado]
"""
import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]


def hojas(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from hojas(v, f"{p}.{k}" if p else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from hojas(v, f"{p}[{i}]")
    else:
        yield p, o


def compara(a, b, titulo):
    ha, hb = dict(hojas(a)), dict(hojas(b))
    solo_a = sorted(set(ha) - set(hb))
    solo_b = sorted(set(hb) - set(ha))
    cambian = sorted(k for k in set(ha) & set(hb) if ha[k] != hb[k])
    print(f"== {titulo}")
    print(f"   hojas: {len(ha)} -> {len(hb)}; nuevas {len(solo_b)}, retiradas {len(solo_a)}, cambiadas {len(cambian)}")
    raices = {}
    for k in solo_b:
        r = re.sub(r"\[\d+\]", "[]", k)
        r = ".".join(r.split(".")[:4])
        raices[r] = raices.get(r, 0) + 1
    for r, n in sorted(raices.items()):
        print(f"   + {r}  ({n} hojas)")
    for k in solo_a:
        print(f"   - {k}")
    for k in cambian:
        print(f"   ~ {k}: {ha[k]!r} -> {hb[k]!r}")
    return ha, hb


def js_objetos(texto):
    out = {}
    for nombre in ("DATOS_CAP5", "SERIES_CAP5"):
        m = re.search(r"const " + nombre + r" = (.*?);\n", texto, flags=re.S)
        out[nombre] = json.loads(m.group(1))
    return out, texto.splitlines()[0]


def main():
    viejo = json.loads(subprocess.run(["git", "show", "7686d33:precalculo/salidas/cap5_sarima.json"],
                                      cwd=RAIZ, capture_output=True, text=True, check=True).stdout)
    nuevo = json.loads((RAIZ / "precalculo/salidas/cap5_sarima.json").read_text(encoding="utf-8"))
    compara(viejo, nuevo, "cap5_sarima.json: 7686d33 -> árbol")

    jv, cab_v = js_objetos(subprocess.run(["git", "show", "7686d33:precalculo/salidas/cap5_datos.js"],
                                          cwd=RAIZ, capture_output=True, text=True, check=True).stdout)
    jn, cab_n = js_objetos((RAIZ / "precalculo/salidas/cap5_datos.js").read_text(encoding="utf-8"))
    print(f"   cabecera js: {cab_v!r} -> {cab_n!r}")
    compara(jv["SERIES_CAP5"], jn["SERIES_CAP5"], "SERIES_CAP5 (cap5_datos.js): 7686d33 -> árbol")
    print("   DATOS_CAP5 del js == cap5_sarima.json del árbol:", jn["DATOS_CAP5"] == nuevo)
    for nombre, txt in (("cap5_datos.js", (RAIZ / "precalculo/salidas/cap5_datos.js").read_text(encoding="utf-8")),
                        ("cap5_sarima.json", (RAIZ / "precalculo/salidas/cap5_sarima.json").read_text(encoding="utf-8")),
                        ("capitulo-5-sarima.html", (RAIZ / "Htmls_Series/capitulo-5-sarima.html").read_text(encoding="utf-8"))):
        print(f"   secuencias <c3>… literales en {nombre}: {len(re.findall(r'<[cdef][0-9a-f]>', txt))}")

    # El HTML: los datos incrustados son exactamente los del js?
    html = (RAIZ / "Htmls_Series/capitulo-5-sarima.html").read_text(encoding="utf-8")
    html_v = subprocess.run(["git", "show", "7686d33:Htmls_Series/capitulo-5-sarima.html"],
                            cwd=RAIZ, capture_output=True, text=True, check=True).stdout
    for nombre in ("DATOS_CAP5", "SERIES_CAP5"):
        a = json.loads(re.search(r"const " + nombre + r" = (.*?);\n", html_v, flags=re.S).group(1))
        b = json.loads(re.search(r"const " + nombre + r" = (.*?);\n", html, flags=re.S).group(1))
        print(f"   HTML {nombre} == js del árbol: {b == jn[nombre]}")
        compara(a, b, f"HTML {nombre}: 7686d33 -> árbol")
    otros = sorted(set(re.findall(r"const ([A-Z][A-Z0-9_]+) = [\[{]", html)) - {"DATOS_CAP5", "SERIES_CAP5"})
    for nombre in otros:
        pa = re.search(r"const " + nombre + r" = (.*?);\n", html_v, flags=re.S)
        pb = re.search(r"const " + nombre + r" = (.*?);\n", html, flags=re.S)
        if pa and pb:
            print(f"   otro dato incrustado {nombre}: {'igual' if pa.group(1) == pb.group(1) else 'CAMBIA'}")

    if len(sys.argv) > 2:
        regen = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        compara(nuevo, regen, "cap5_sarima.json: árbol -> regenerado fuera del repo")
        jr, cab_r = js_objetos(Path(sys.argv[2]).read_text(encoding="utf-8"))
        print(f"   cabecera js regenerado: {cab_r!r}")
        compara(jn["SERIES_CAP5"], jr["SERIES_CAP5"], "SERIES_CAP5: árbol -> regenerado")
        print("   DATOS_CAP5 regenerado == cap5_sarima.json regenerado:", jr["DATOS_CAP5"] == regen)


if __name__ == "__main__":
    main()
