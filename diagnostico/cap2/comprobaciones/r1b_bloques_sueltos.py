#!/usr/bin/env python3
"""R1 del capítulo 2, tras la verificación · los 21 bloques, cada uno SOLO.

[1] Cada bloque de Python, ejecutado SOLO en un proceso nuevo y en una carpeta vacía:
    si usa `pasajeros` (o cualquier otro objeto) sin crearlo, falla aquí. El bloque de
    Python del ejercicio 4 se excluye: declara que usa `adf_como_en_r()` del Módulo 6.
[2] El camino de la URL del bloque del Módulo 6 (R y Python), que el verificador nunca
    recorre porque encuentra el archivo en `precalculo/`. La página aún no está
    publicada, así que se sirve `Htmls_Series/` en un puerto local y se sustituye la base
    `https://jotamao1985.github.io/Series-de-Tiempo_Un_Bosque/` por la local: prueba que
    la lectura por HTTP del mismo CSV da las mismas cifras, no que la URL pública exista.

Desde la raíz del repo:
  MPLBACKEND=Agg python3 diagnostico/cap2/comprobaciones/r1b_bloques_sueltos.py \
      > diagnostico/cap2/comprobaciones/r1b_bloques_sueltos.out 2>&1
"""
import subprocess, sys, tempfile, time, os
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "precalculo"))
import verifica_bloques_cap6 as v

HTML = RAIZ / "Htmls_Series" / "capitulo-2-estacionariedad-acf-pacf.html"
bloques = v.extrae([(HTML.name, HTML.read_text(encoding="utf-8"))])
BASE = "https://jotamao1985.github.io/Series-de-Tiempo_Un_Bosque/"
PUERTO = 8799
srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PUERTO), "--bind", "127.0.0.1",
                        "--directory", str(RAIZ / "Htmls_Series")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
mal = 0
try:
    print("[1] los 21 bloques, cada uno solo, en proceso nuevo y carpeta vacía (la TRM fija, por HTTP local; el ejercicio 4 descarga de datos.gov.co)")
    for i, b in enumerate(bloques):
        if False:
            continue
        primera = next(l for l in b["codigo"].splitlines() if l.strip()).strip()[:60]
        cuerpo = v.limpia(b["codigo"]).replace(BASE, f"http://127.0.0.1:{PUERTO}/")
        with tempfile.TemporaryDirectory() as d:
            if b["lang"] == "python":
                r = subprocess.run([sys.executable, "-c", "import warnings; warnings.filterwarnings('ignore')\n" + cuerpo],
                                   cwd=d, capture_output=True, text=True, env={**os.environ, "MPLBACKEND": "Agg"}, timeout=900)
            else:
                Path(d, "b.R").write_text("options(warn = 1)\n" + cuerpo, encoding="utf-8")
                r = subprocess.run(["Rscript", "--vanilla", "b.R"], cwd=d, capture_output=True, text=True, timeout=900)
        esp = v.esperados(b["codigo"])
        faltan = [e for e in esp if e not in r.stdout]
        ok = r.returncode == 0 and not faltan
        mal += not ok
        print(f"  #{i:<2} {b['lang']:<6} {'OK   ' if ok else 'FALLA'} código {r.returncode} · {len(esp) - len(faltan)} de {len(esp)} cifras · {primera}")
        if not ok:
            print("      " + "\n      ".join((r.stdout + r.stderr).strip().splitlines()[-6:]))

    print("\n[2] bloque de R del Módulo 6, en una carpeta vacía: lee la TRM por HTTP")
    b = next(b for b in bloques if b["lang"] == "r" and "trm_mensual_2015-01_2026-06.csv" in b["codigo"])
    assert BASE in b["codigo"]
    codigo = "options(warn = 1)\n" + v.limpia(b["codigo"]).replace(BASE, f"http://127.0.0.1:{PUERTO}/")
    with tempfile.TemporaryDirectory() as d:
        Path(d, "b.R").write_text(codigo, encoding="utf-8")
        r = subprocess.run(["Rscript", "--vanilla", "b.R"], cwd=d, capture_output=True, text=True, timeout=600)
    esp = v.esperados(b["codigo"])
    faltan = [e for e in esp if e not in r.stdout]
    ok = r.returncode == 0 and not faltan
    mal += not ok
    print(f"  {'OK   ' if ok else 'FALLA'} código {r.returncode} · {len(esp) - len(faltan)} de {len(esp)} cifras; faltan: {faltan}")
    if not ok:
        print("      " + "\n      ".join((r.stdout + r.stderr).strip().splitlines()[-8:]))
finally:
    srv.terminate()
print("\n=== sin fallos ===" if not mal else f"\n=== {mal} fallos ===")
sys.exit(1 if mal else 0)
