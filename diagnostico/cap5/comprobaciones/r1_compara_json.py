"""Compara campo a campo cap5_sarima.json y cap5_datos.js regenerados con los de HEAD.
Uso: python3 r1_compara_json.py <json_HEAD> <js_HEAD>   (desde la raíz del repo)"""
import json, sys
def hojas(x, ruta=""):
    if isinstance(x, dict):
        for k, v in x.items(): yield from hojas(v, f"{ruta}.{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from hojas(v, f"{ruta}[{i}]")
    else:
        yield ruta, x
def compara(a, b, nombre):
    ha, hb = dict(hojas(a)), dict(hojas(b))
    solo_a = sorted(set(ha) - set(hb)); solo_b = sorted(set(hb) - set(ha))
    dif = sorted(k for k in set(ha) & set(hb) if ha[k] != hb[k])
    print(f"== {nombre}: {len(ha)} hojas antes, {len(hb)} después")
    print(f"   solo antes: {len(solo_a)}  {solo_a[:10]}")
    print(f"   nuevas:     {len(solo_b)}  {solo_b[:12]}")
    print(f"   distintas:  {len(dif)}")
    for k in dif: print(f"      {k}: {ha[k]!r} -> {hb[k]!r}")
a = json.load(open(sys.argv[1], encoding="utf-8"))
b = json.load(open("precalculo/salidas/cap5_sarima.json", encoding="utf-8"))
compara(a, b, "cap5_sarima.json")
def js(path):
    t = open(path, encoding="utf-8").read()
    i = t.index("const DATOS_CAP5 = ") + len("const DATOS_CAP5 = "); j = t.index(";\nconst SERIES_CAP5 = ")
    k = j + len(";\nconst SERIES_CAP5 = ")
    return json.loads(t[i:j]), json.loads(t[k:t.rindex(";")])
(da, sa), (db, sb) = js(sys.argv[2]), js("precalculo/salidas/cap5_datos.js")
compara(da, db, "cap5_datos.js · DATOS_CAP5")
compara(sa, sb, "cap5_datos.js · SERIES_CAP5")
print("DATOS_CAP5 del .js igual al .json:", db == b)
