#!/usr/bin/env python3
"""R5 del capítulo 4 · cada bloque de código del capítulo, ejecutado SOLO.

Adaptado de `diagnostico/cap3/comprobaciones/r5_bloques_sueltos.py`. El verificador de bloques
los encadena en una sesión, así que un bloque que use un objeto creado por otro pasa sin que se
note. Aquí cada uno corre en un proceso nuevo y en una carpeta vacía: si le falta algo, falla.
La copia fija de la TRM (Módulo 10) se sirve por HTTP local, sustituyendo la dirección
pública. Además de que corra, se comprueba que cada cifra anunciada tras `#>` esté en su salida.

Desde la raíz del repo:
  MPLBACKEND=Agg python3 diagnostico/cap4/comprobaciones/r5_bloques_sueltos.py \
      > diagnostico/cap4/comprobaciones/r5_bloques_sueltos.out 2>&1
"""
import os, subprocess, sys, tempfile, time
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "precalculo"))
import verifica_bloques_cap6 as v

HTML = RAIZ / "Htmls_Series" / "capitulo-4-modelos-arima.html"
bloques = v.extrae([(HTML.name, HTML.read_text(encoding="utf-8"))])
BASE = "https://jotamao1985.github.io/Series-de-Tiempo_Un_Bosque/"
PUERTO = 8797
srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PUERTO), "--bind", "127.0.0.1",
                        "--directory", str(RAIZ / "Htmls_Series")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
mal = 0
try:
    print(f"{len(bloques)} bloques, cada uno solo, en proceso nuevo y carpeta vacía")
    for i, b in enumerate(bloques):
        primera = next(l for l in b["codigo"].splitlines() if l.strip()).strip()[:64]
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
            print("      faltan:", faltan[:12])
            print("      " + "\n      ".join((r.stdout + r.stderr).strip().splitlines()[-6:]))
finally:
    srv.terminate()
print(f"\n{'TODOS BIEN' if not mal else str(mal) + ' CON PROBLEMAS'}")
sys.exit(1 if mal else 0)
