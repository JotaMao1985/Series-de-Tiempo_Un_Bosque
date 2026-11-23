"""Verificador A, R5 cap. 4: extrae el bloque R de c4m1..c4m9, lo corre en un proceso
nuevo y una carpeta vacia, sin red, y compara con lo que hay bajo #>."""
import html, os, re, subprocess, sys, tempfile, pathlib
RAIZ = pathlib.Path(__file__).resolve().parents[3]
import sys
SAL = pathlib.Path(__file__).parent / ("v5A2_bloques" if "--segunda" in sys.argv else "v5A_bloques")
SAL.mkdir(exist_ok=True)
fuentes = "".join((RAIZ / "ensamblado/cap4" / f).read_text() for f in
                  ["templates_1_3.html", "templates_4_6.html", "templates_7_9.html"])
env = {k: v for k, v in os.environ.items() if "proxy" not in k.lower()}
env.update(http_proxy="http://127.0.0.1:9", https_proxy="http://127.0.0.1:9",
           HTTP_PROXY="http://127.0.0.1:9", HTTPS_PROXY="http://127.0.0.1:9", R_LIBS_USER=env.get("R_LIBS_USER", ""))
norm = lambda s: [re.sub(r"\s+", " ", l).strip() for l in s.splitlines() if l.strip()]
total = 0
for i in range(1, 10):
    m = re.search(rf'id="c4m{i}-sol".*?<pre><code class="language-r">(.*?)</code></pre>', fuentes, re.S)
    bloque = html.unescape(m.group(1))
    codigo = "\n".join(l for l in bloque.splitlines() if not l.startswith("#>"))
    esperado = [l[2:] for l in bloque.splitlines() if l.startswith("#>")]
    d = tempfile.mkdtemp(prefix="v5A_")
    (pathlib.Path(d) / "b.R").write_text(codigo)
    r = subprocess.run(["Rscript", "--vanilla", "-e",
                        "source('b.R', echo=FALSE, print.eval=TRUE, max.deparse.length=Inf)"],
                       cwd=d, capture_output=True, text=True, env=env)
    (SAL / f"m{i}.R").write_text(codigo)
    (SAL / f"m{i}.out").write_text(r.stdout + ("\n--- stderr ---\n" + r.stderr if r.stderr else ""))
    a, b = norm(r.stdout), norm("\n".join(x[1:] if x.startswith(" ") else x for x in esperado))
    ok = a == b
    total += ok
    print(f"c4m{i}: {'OK' if ok else 'DISCREPA'}  ({len(b)} lineas #>)  rc={r.returncode}")
    if not ok:
        for x, y in zip(a + [''] * 50, b + [''] * 50):
            if x != y: print("   R  :", x); print("   HTML:", y)
            if not x and not y: break
# segunda lectura: el <pre> suelto del M8 (lince), tras «La columna de la varianza no decide»
m = re.search(r'abajo lo calcula\.\)</p>\s*</div>\s*<pre><code class="language-r">(.*?)</code></pre>', fuentes, re.S)
if m:
    bloque = html.unescape(m.group(1)); codigo = "\n".join(l for l in bloque.splitlines() if not l.startswith("#>"))
    esperado = [l[2:] for l in bloque.splitlines() if l.startswith("#>")]
    d = tempfile.mkdtemp(prefix="v5A_"); (pathlib.Path(d) / "b.R").write_text(codigo)
    r = subprocess.run(["Rscript", "--vanilla", "-e", "source('b.R', echo=FALSE, print.eval=TRUE)"], cwd=d, capture_output=True, text=True, env=env)
    (SAL / "m8_lince.R").write_text(codigo); (SAL / "m8_lince.out").write_text(r.stdout + r.stderr)
    ok = norm(r.stdout) == norm("\n".join(x[1:] if x.startswith(" ") else x for x in esperado))
    print(f"M8 lince (pre suelto): {'OK' if ok else 'DISCREPA'}  ({len(esperado)} lineas #>)"); total += ok
print(f"{total} bloques identicos")
