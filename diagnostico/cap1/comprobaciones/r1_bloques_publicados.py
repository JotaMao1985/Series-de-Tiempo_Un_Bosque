# R1 · Ejecuta, tal como quedaron publicados en el HTML, los bloques de codigo
# que esta ronda cambio (M5 R y Python, M7 Python) y el bloque R del M7 cuyo
# comentario cambio. Se extraen del propio capitulo, de modo que lo que se
# prueba es el texto que lee el estudiante.
#   - R: fpp3 no esta instalado; `library(fpp3)` se sustituye por los paquetes
#     que fpp3 adjunta y que el bloque usa. Nada mas se toca.
#   - Python: `pasajeros` se construye como en el M2, pero leyendo la serie de R
#     para no depender de la red; `plt.show()` se retira y se usa el backend Agg.
import html, io, os, re, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(AQUI, "..", "..", "..", "Htmls_Series", "capitulo-1-componentes-descomposicion.html")
doc = io.open(CAP, encoding="utf-8").read()

def bloque(marca, lenguaje):
    """Devuelve el <pre><code> del lenguaje dado cuyo texto contiene `marca`."""
    for m in re.finditer(r'<pre><code class="language-%s">(.*?)</code></pre>' % lenguaje, doc, re.S):
        if marca in m.group(1):
            return html.unescape(m.group(1))
    raise SystemExit("no se encontro el bloque: " + marca)

PAQ = ("suppressPackageStartupMessages({library(tsibble); library(dplyr); library(ggplot2);"
       " library(fabletools); library(feasts)})")

def corre_r(nombre, codigo, cola=""):
    codigo = codigo.replace("library(fpp3)", PAQ)
    # autoplot()/plot() dibujan en un dispositivo nulo
    guion = "pdf(NULL)\n" + codigo + "\n" + cola + "\n"
    with tempfile.NamedTemporaryFile("w", suffix=".R", delete=False) as f:
        f.write(guion)
    r = subprocess.run(["Rscript", f.name], capture_output=True, text=True)
    print("=" * 70); print(nombre); print("-" * 70); print(codigo.strip()); print("-" * 70)
    print("SALIDA:"); print(r.stdout.strip())
    err = [l for l in r.stderr.splitlines() if "deprecated" not in l and "ggtime" not in l and l.strip()]
    print("codigo de salida:", r.returncode, "| stderr (sin el aviso de autoplot en desuso):", err or "nada")
    os.unlink(f.name)
    return r.returncode

def corre_py(nombre, codigo):
    cab = (
        "import subprocess, pandas as pd, matplotlib\nmatplotlib.use('Agg')\n"
        "_v = subprocess.run(['Rscript','-e','cat(as.numeric(AirPassengers))'],capture_output=True,text=True).stdout.split()\n"
        "pasajeros = pd.Series([float(x) for x in _v], index=pd.date_range('1949-01-01', periods=len(_v), freq='MS'), name='pasajeros')\n"
    )
    cuerpo = codigo.replace("plt.legend(); plt.show()", "plt.legend()").replace("plt.show()", "")
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(cab + cuerpo + "\n")
    r = subprocess.run([sys.executable, f.name], capture_output=True, text=True, env=dict(os.environ, MPLBACKEND="Agg"))
    print("=" * 70); print(nombre); print("-" * 70); print(codigo.strip()); print("-" * 70)
    print("SALIDA:"); print(r.stdout.strip())
    print("codigo de salida:", r.returncode, "| stderr:", r.stderr.strip() or "nada")
    os.unlink(f.name)
    return r.returncode

fallos = 0
fallos += corre_r("M5 · R · media movil 2x12 en dos pasos",
                  bloque("Media movil centrada 2x12 en dos pasos", "r"),
                  cola='cat("NA en tendencia:", sum(is.na(pasajeros$tendencia)), "\\n")')
fallos += corre_py("M5 · Python · media movil 2x12 con pandas",
                   bloque("Media movil centrada 2x12 con pandas", "python"))
fallos += corre_r("M7 · R · STL (solo cambio el comentario)",
                  bloque("STL sobre log(AirPassengers): componentes aditivos", "r"),
                  cola=('s <- as_tsibble(log(AirPassengers)) |> model(stl = STL(value ~ trend(window = 19) + '
                        'season(window = "periodic"))) |> components()\n'
                        'cat("S julio (log):", round(s$season_year[7], 4), " exp:", round(exp(s$season_year[7]), 4), "\\n")'))
fallos += corre_py("M7 · Python · STL que reproduce la figura",
                   bloque("STL sobre log(AirPassengers), con los mismos ajustes", "python"))
# M6 · el filtro que nombra la ficha del paso 2
m = re.search(r"<code>(stats::filter\(y, [^<]*)</code>", doc)
filtro = html.unescape(m.group(1))
fallos += corre_r("M6 · R · filtro del paso 2: " + filtro,
                  "y <- AirPassengers; m <- 12\nf <- " + filtro +
                  '\ncat("jul-1955:", f[79], " NA:", sum(is.na(f)), " igual a decompose()$trend:", '
                  'isTRUE(all.equal(as.numeric(f), as.numeric(decompose(y)$trend))), "\\n")')
# M6 · seasonal_decompose de statsmodels usa la misma media movil
fallos += corre_py("M6 · Python · seasonal_decompose (bloque del capitulo, sin cambios)",
                   bloque("Descomposicion clasica multiplicativa", "python") +
                   '\nprint("tendencia jul-1955:", dc.trend["1955-07-01"], " NaN:", int(dc.trend.isna().sum()),'
                   ' " indice julio:", round(dc.seasonal["1955-07-01"], 4))')
print("=" * 70); print("bloques con error:", fallos)
