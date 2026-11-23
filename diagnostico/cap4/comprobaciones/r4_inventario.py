#!/usr/bin/env python3
"""
r4_inventario.py — rehace `bibliografia/contraste/cap4_inventario.tsv` contra el texto de hoy

El inventario del diagnóstico (357 filas, commit 880e0a3) se hizo antes de las
rondas R1–R3. Este guion lo reescribe y le llena la columna `r4`:

  registrada: <veredicto>            tiene `data-afirma` y entrada en cap4.yml
  registrada: <veredicto>, en <id>   la cubre la afirmación <id>
  sin marcar: <por qué>              sigue en el capítulo y no se registró
De una afirmación registrada, `linea` y `texto` son los de hoy (el texto marcado,
sin las citas, hasta 200 caracteres); de una fila sin marcar se conserva el
texto del diagnóstico, y si ya no está literal en el capítulo se dice. Las
afirmaciones nuevas (texto que entró en R1–R3 o que esta ronda separó) se
añaden. Las filas viejas que salen del inventario (la frase ya no existe o la
absorbió otra) se listan en la salida.

Qué fue de cada fila lo dijeron los lectores de la ronda (campos `inventario`,
`sin_marcar` y `fuera` de `bibliografia/_local/herramientas/cap4/r4_entradas.json`,
fuera de git).

Uso:  python3 diagnostico/cap4/comprobaciones/r4_inventario.py
"""
import csv
import html
import io
import json
import pathlib
import re
import subprocess
import sys
import unicodedata

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import r4_lib as L  # noqa: E402

A = L.A
VIEJO = "21b311b"
TSV = L.RAIZ / "bibliografia" / "contraste" / "cap4_inventario.tsv"
HTML = L.RAIZ / "Htmls_Series" / "capitulo-4-modelos-arima.html"
REGISTRO = L.RAIZ / "bibliografia" / "contraste" / "cap4.yml"
ENTRADAS = L.RAIZ / "bibliografia" / "_local" / "herramientas" / "cap4" / "r4_entradas.json"

PIE = {}   # las filas c4-m0-* (pie, metadatos y JSON de datos) las decidió el lector F (`sin_marcar`)


def plano(t: str) -> str:
    return A.normaliza(html.unescape(re.sub(r"<[^>]+>", "", t)))


def main() -> int:
    viejo = subprocess.run(["git", "show", f"{VIEJO}:bibliografia/contraste/cap4_inventario.tsv"], cwd=L.RAIZ,
                           capture_output=True, check=True).stdout.decode("utf-8")
    filas = list(csv.DictReader(io.StringIO(viejo), delimiter="\t"))
    campos = list(filas[0].keys())
    dato = json.loads(ENTRADAS.read_text("utf-8"))
    registro = {e["id"]: e for e in yaml.safe_load(REGISTRO.read_text("utf-8"))["afirmaciones"]}
    texto_html = HTML.read_text("utf-8")
    lector = A.lee_html(texto_html)
    todo = plano(texto_html)
    cubre = {}
    for e in dato["entradas"]:
        for i in e.get("inventario") or []:
            cubre.setdefault(i, e["id"])
    for e in dato["entradas"]:                       # la entrada con el mismo id manda
        cubre[e["id"]] = e["id"]
    sin = dict(dato["sin_marcar"])
    sin.update(PIE)

    salida, fuera, no_literal, vistos = [], [], 0, set()
    cuenta = {}
    for f in filas:
        ident = f["id"]
        if ident in cubre:
            destino = cubre[ident]
            a, e = lector.afirmaciones[destino], registro[destino]
            f["linea"] = str(a.linea)
            f["texto"] = A.normaliza(a.texto)[:200]
            f["r4"] = f"registrada: {e['veredicto']}" + ("" if destino == ident else f", en {destino}")
            vistos.add(destino)
            clave = "registrada"
        elif ident in dato["fuera"]:
            fuera.append((ident, dato["fuera"][ident]))
            continue
        elif ident in sin:
            f["r4"] = "sin marcar: " + " ".join(sin[ident].split())
            if plano(f["texto"]) not in todo:
                f["r4"] += " [el texto es el del diagnóstico: ya no está literal en el capítulo]"
                no_literal += 1
            clave = "sin marcar"
        else:
            sys.exit(f"ABORTA: nadie dijo qué fue de la fila {ident}")
        cuenta[(clave, f["prioridad"])] = cuenta.get((clave, f["prioridad"]), 0) + 1
        salida.append(f)
    nuevas = 0
    for ident, a in lector.afirmaciones.items():
        if ident in vistos or ident in {f["id"] for f in salida}:
            continue
        e = registro[ident]
        fila = dict.fromkeys(campos, "")
        fila.update({"id": ident, "modulo": str(int(A.RE_ID.match(ident).group(2))), "linea": str(a.linea),
                     "tipo": e["tipo"], "texto": A.normaliza(a.texto)[:200],
                     "fuente_candidata": "; ".join(dict.fromkeys(x["clave"] for x in e.get("fuentes") or [])),
                     "donde_buscar": "afirmación nueva de la R4 (no estaba en el inventario del diagnóstico)",
                     "prioridad": "", "r4": f"registrada: {e['veredicto']}"})
        salida.append(fila)
        nuevas += 1
    # Ningún literal de cita en el inventario (va a git): dos pasajes del diagnóstico
    # coinciden con citas de esta ronda y se sustituyen por el puntero de siempre.
    citas = yaml.safe_load((L.RAIZ / "bibliografia/_local/citas/cap4.yml").read_text("utf-8"))["citas"]
    literales = [str(t) for d in citas.values() for t in d.values() if len(str(t).split()) >= 4]
    quitados = 0
    for f in salida:
        for k, v in f.items():
            if not v:
                continue
            if "\t" in v or "\n" in v:
                v = " ".join(v.split())
            if k in ("donde_buscar", "hallado", "r4"):
                for lit in literales:
                    # NFKC, como el auditor: «…» y «...» son el mismo texto
                    vn = unicodedata.normalize("NFKC", v)
                    if re.search(L.flexible(unicodedata.normalize("NFKC", lit)), vn, flags=re.I):
                        v, n = re.subn(L.flexible(unicodedata.normalize("NFKC", lit)), "[literal en _local]", vn,
                                       flags=re.I)
                        quitados += n
            f[k] = v
    with TSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=campos, delimiter="\t", lineterminator="\n",
                           quoting=csv.QUOTE_NONE, escapechar=None, quotechar=None)
        w.writeheader()
        w.writerows(salida)
    print(f"{TSV.relative_to(L.RAIZ)}: {len(salida)} filas ({len(filas)} en el diagnóstico; {len(fuera)} salen; "
          f"{nuevas} nuevas)")
    for pri in ("alta", "media", "baja"):
        print(f"  prioridad {pri}: {cuenta.get(('registrada', pri), 0)} registradas, "
              f"{cuenta.get(('sin marcar', pri), 0)} sin marcar")
    print(f"  filas sin marcar cuyo texto ya no está literal: {no_literal}")
    print(f"  literales de cita sustituidos por «[literal en _local]»: {quitados}")
    print(f"  afirmaciones en el registro: {len(registro)}; todas con fila: "
          f"{all(i in {f['id'] for f in salida} or i in vistos for i in registro)}")
    print("\nFilas del diagnóstico que salen del inventario:")
    for ident, por_que in fuera:
        print(f"  {ident}: {' '.join(por_que.split())}")
    print("\nFilas de prioridad alta sin marcar:")
    for f in salida:
        if f["prioridad"] == "alta" and f["r4"].startswith("sin marcar"):
            print(f"  {f['id']}: {f['r4'][12:230]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
