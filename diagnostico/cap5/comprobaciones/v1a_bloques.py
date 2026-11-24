"""Verificador A, R1 cap. 5: ejecuta cada bloque de Python (y los de R que leen la TRM)
del capítulo, solo, en una carpeta vacía y en una carpeta con el CSV de la TRM, y compara
sus líneas `#>` con la salida. Señala cualquier ConvergenceWarning en stderr.

Uso (desde la raíz del repo):
  MPLBACKEND=Agg /opt/homebrew/Caskroom/mambaforge/base/bin/python3 \
      diagnostico/cap5/comprobaciones/v1a_bloques.py > diagnostico/cap5/comprobaciones/v1a_bloques.out
"""
import html, os, re, shutil, subprocess, sys, tempfile

RAIZ = os.getcwd()
HTML = os.path.join(RAIZ, "Htmls_Series/capitulo-5-sarima.html")
CSV = os.path.join(RAIZ, "Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")
PY = sys.executable

texto = open(HTML, encoding="utf-8").read()
# Solo el cuerpo del capítulo, no el JS
patron = re.compile(r'<code class="language-(python|r)">(.*?)</code>', re.S)
bloques = [(m.group(1), html.unescape(m.group(2)), texto[:m.start()].count("\n") + 1)
           for m in patron.finditer(texto)]


def esperado(codigo):
    return [l[2:].strip() for l in codigo.splitlines() if l.startswith("#>")]


def norm(l):
    return re.sub(r"\s+", " ", l.strip())


def ejecutar(lang, codigo, con_csv):
    d = tempfile.mkdtemp(prefix="v1a_")
    if con_csv:
        shutil.copy(CSV, d)
    if lang == "python":
        f = os.path.join(d, "b.py"); open(f, "w").write(codigo)
        cmd = [PY, "-W", "default", f]
    else:
        f = os.path.join(d, "b.R"); open(f, "w").write(codigo)
        cmd = ["Rscript", f]
    env = dict(os.environ, MPLBACKEND="Agg", LC_ALL="en_US.UTF-8")
    try:
        r = subprocess.run(cmd, cwd=d, capture_output=True, text=True, timeout=900, env=env)
        out, err, rc = r.stdout, r.stderr, r.returncode
    except subprocess.TimeoutExpired:
        out, err, rc = "", "TIMEOUT", -1
    shutil.rmtree(d, ignore_errors=True)
    return out, err, rc


def compara(exp, out):
    salida = [norm(l) for l in out.splitlines()]
    faltan = []
    for e in exp:
        ne = norm(e)
        # el comentario a la derecha de la cifra se ignora: se compara el prefijo
        if not any(s and (ne.startswith(s) or s.startswith(ne) or s == ne) for s in salida):
            faltan.append(e)
    return faltan


for i, (lang, codigo, linea) in enumerate(bloques, 1):
    usa_trm = "trm_mensual" in codigo
    if lang == "r" and not usa_trm:
        continue
    exp = esperado(codigo)
    for con_csv in ((False, True) if usa_trm else (False,)):
        out, err, rc = ejecutar(lang, codigo, con_csv)
        faltan = compara(exp, out)
        conv = [l for l in err.splitlines() if "ConvergenceWarning" in l or "failed to converge" in l.lower()]
        print(f"=== bloque {i} ({lang}, l. {linea}, {'con' if con_csv else 'sin'} CSV) rc={rc} "
              f"esperadas={len(exp)} sin_coincidencia={len(faltan)} avisos_convergencia={len(conv)}")
        for f in faltan:
            print("   FALTA #>", f)
        if faltan:
            print("   --- salida real ---")
            for l in out.splitlines()[:60]:
                print("   |", l)
        for c in conv[:5]:
            print("   AVISO", c.strip()[:200])
        if rc != 0:
            print("   STDERR:", err.strip()[-800:])
        sys.stdout.flush()
