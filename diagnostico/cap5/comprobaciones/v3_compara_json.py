"""V3: compara cap5_sarima.json de HEAD con el del arbol: solo hojas nuevas (salvo `generado`)."""
import json, subprocess, sys
viejo = json.loads(subprocess.run(["git", "show", "HEAD:precalculo/salidas/cap5_sarima.json"],
                                  capture_output=True, text=True, check=True).stdout)
nuevo = json.load(open("precalculo/salidas/cap5_sarima.json", encoding="utf-8"))
cambiadas, quitadas, nuevas = [], [], []
def recorre(a, b, ruta):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in a:
            if k not in b: quitadas.append(ruta + "/" + k)
            else: recorre(a[k], b[k], ruta + "/" + k)
        for k in b:
            if k not in a: nuevas.append(ruta + "/" + k)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): cambiadas.append((ruta, "longitud", len(a), len(b)))
        for i, (x, y) in enumerate(zip(a, b)): recorre(x, y, f"{ruta}[{i}]")
    else:
        if a != b: cambiadas.append((ruta, a, b))
recorre(viejo, nuevo, "")
print("hojas cambiadas:", len(cambiadas))
for c in cambiadas: print("  ", c)
print("hojas quitadas:", len(quitadas)); [print("  ", q) for q in quitadas]
print("nuevas:", len(nuevas)); [print("  ", n) for n in nuevas]
for k, m in nuevo["airpassengers"]["comparativa"]["modelos"].items() if "airpassengers" in nuevo and "comparativa" in nuevo["airpassengers"] else []:
    print(k, m.get("exactas"))
