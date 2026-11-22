# Extrae los dos bloques de la TRM del capítulo 4 y los ejecuta dos veces:
# en una carpeta vacía (leen de la página del curso) y con la copia en la carpeta.
# python3 diagnostico/cap4/comprobaciones/v1_trm_bloques.py > .../v1_trm_bloques.out 2>&1
import html, re, shutil, subprocess, tempfile, os, difflib
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[3]
txt = (RAIZ / "Htmls_Series/capitulo-4-modelos-arima.html").read_text(encoding="utf-8")
bloques = re.findall(r'<pre><code class="language-(r|python)">(.*?)</code></pre>', txt, re.S)
trm = [(l, html.unescape(c)) for l, c in bloques if "trm_mensual_2015-01_2026-06.csv" in c]
print("bloques de la TRM:", [l for l, _ in trm])
csv = RAIZ / "Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv"
def anunciado(codigo):
    return [ln[3:].rstrip() for ln in codigo.splitlines() if ln.startswith("#> ")]
for lang, cod in trm:
    salidas = {}
    for modo in ("vacia", "con_archivo"):
        d = Path(tempfile.mkdtemp(prefix=f"v1trm_{modo}_"))
        if modo == "con_archivo":
            shutil.copy(csv, d / csv.name)
        f = d / ("b.R" if lang == "r" else "b.py")
        f.write_text(cod, encoding="utf-8")
        cmd = ["Rscript", str(f)] if lang == "r" else ["python3", str(f)]
        env = dict(os.environ, MPLBACKEND="Agg")
        r = subprocess.run(cmd, cwd=d, capture_output=True, text=True, timeout=1800, env=env)
        salidas[modo] = r.stdout
        print(f"\n===== {lang} · {modo} · código {r.returncode} =====")
        print(r.stdout)
        if r.stderr.strip():
            print("[stderr]", r.stderr[-1500:])
    print(f"\n----- {lang}: vacía == con_archivo ? {salidas['vacia'] == salidas['con_archivo']}")
    if salidas['vacia'] != salidas['con_archivo']:
        print("\n".join(difflib.unified_diff(salidas['vacia'].splitlines(), salidas['con_archivo'].splitlines(), lineterm="")))
    # cada línea anunciada (#>) aparece tal cual en la salida
    sal = salidas["con_archivo"]
    faltan = [a for a in anunciado(cod) if a.strip() and a.split("  ")[0].strip() not in sal]
    print(f"----- {lang}: líneas #> cuyo primer trozo no aparece en la salida: {faltan}")
