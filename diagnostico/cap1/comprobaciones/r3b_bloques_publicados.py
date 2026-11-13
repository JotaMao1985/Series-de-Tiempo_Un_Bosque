# R3b · Ejecuta, tal como quedaron publicados en el HTML, los bloques de codigo que esta mitad de la ronda
# cambio (M7, R y Python: las dos lineas que encienden s.window = 11 y robust = TRUE) o anadio (M8, R y Python).
# Se extraen del propio capitulo: lo que se prueba es el texto que lee el estudiante.
#   - R: fpp3 no esta instalado; `library(fpp3)` se sustituye por los paquetes que fpp3 adjunta y que el bloque
#     usa. Nada mas se toca.
#   - Python: `pasajeros` se construye como en el M2, pero leyendo la serie de R para no depender de la red;
#     `plt.show()` se retira y se usa el backend Agg.
# Uso: python3 diagnostico/cap1/comprobaciones/r3b_bloques_publicados.py > .../r3b_bloques_publicados.out
import html, io, os, re, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(AQUI, "..", "..", "..", "Htmls_Series", "capitulo-1-componentes-descomposicion.html")
doc = io.open(CAP, encoding="utf-8").read()

def bloque(marca, lenguaje):
    for m in re.finditer(r'<pre><code class="language-%s">(.*?)</code></pre>' % lenguaje, doc, re.S):
        if marca in m.group(1):
            return html.unescape(m.group(1))
    raise SystemExit("no se encontro el bloque: " + marca)

PAQ = ("suppressPackageStartupMessages({library(tsibble); library(dplyr); library(ggplot2);"
       " library(fabletools); library(feasts)})")

def corre_r(nombre, codigo, cola=""):
    guion = "pdf(NULL)\n" + codigo.replace("library(fpp3)", PAQ) + "\n" + cola + "\n"
    with tempfile.NamedTemporaryFile("w", suffix=".R", delete=False) as f:
        f.write(guion)
    r = subprocess.run(["Rscript", f.name], capture_output=True, text=True)
    print("=" * 70); print(nombre); print("-" * 70); print(codigo.strip()); print("-" * 70)
    print("SALIDA:"); print(r.stdout.strip())
    err = [l for l in r.stderr.splitlines() if "deprecated" not in l and "ggtime" not in l and l.strip()]
    print("codigo de salida:", r.returncode, "| stderr (sin el aviso de autoplot en desuso):", err or "nada")
    os.unlink(f.name)
    return r.returncode

def corre_py(nombre, codigo, cola=""):
    cab = (
        "import subprocess, pandas as pd, matplotlib\nmatplotlib.use('Agg')\n"
        "_v = subprocess.run(['Rscript','-e','cat(as.numeric(AirPassengers))'],capture_output=True,text=True).stdout.split()\n"
        "pasajeros = pd.Series([float(x) for x in _v], index=pd.date_range('1949-01-01', periods=len(_v), freq='MS'), name='pasajeros')\n"
    )
    cuerpo = codigo.replace("plt.legend(); plt.show()", "plt.legend()").replace("plt.show()", "")
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(cab + cuerpo + "\n" + cola + "\n")
    r = subprocess.run([sys.executable, f.name], capture_output=True, text=True, env=dict(os.environ, MPLBACKEND="Agg"))
    print("=" * 70); print(nombre); print("-" * 70); print(codigo.strip()); print("-" * 70)
    print("SALIDA:"); print(r.stdout.strip())
    print("codigo de salida:", r.returncode, "| stderr:", r.stderr.strip() or "nada")
    os.unlink(f.name)
    return r.returncode

fallos = 0
fallos += corre_r("M7 · R · STL, con las dos respuestas encendidas al final",
                  bloque("STL sobre log(AirPassengers): componentes aditivos", "r"),
                  cola='cat("s11: ventanas", s11$win, "| rob: pasadas", rob$inner, "y vueltas", rob$outer, "\\n")')
fallos += corre_py("M7 · Python · STL, con las dos respuestas encendidas al final",
                   bloque("STL sobre log(AirPassengers), con ajustes equivalentes", "python"),
                   cola='print("indice de julio con robust:", round(float(np.exp(rob.seasonal["1955-07-01"])), 4))')
fallos += corre_r("M8 · R · desestacionalizada y fuerzas",
                  bloque("La STL de partida del Modulo 7, sobre el logaritmo (R base)", "r"),
                  cola=('cat("max |ajustada - exp(T + R)| =", max(abs(ajustada - exp(Tt + Rt))), "\\n")\n'
                        'd <- pasajeros |> model(STL(value ~ trend(window = 19) + season(window = "periodic"))) |> components() |> mutate(ajustada = exp(season_adjust))\n'
                        'cat("tidyverts: ajustada de julio de 1955 =", round(d$ajustada[79], 1), "| max |dif| con la de R base =", max(abs(d$ajustada - as.numeric(ajustada))), "\\n")\n'
                        'f <- pasajeros |> features(value, feat_stl)\n'
                        'cat("feat_stl: trend_strength =", round(f$trend_strength, 3), " seasonal_strength_year =", round(f$seasonal_strength_year, 3), "\\n")'))
fallos += corre_py("M8 · Python · desestacionalizada y fuerzas",
                   bloque("La STL de partida del Modulo 7, sobre el logaritmo", "python").replace("XX", "XX"),
                   cola='print("FT, FS sin redondear:", FT, FS)')
print("=" * 70); print("bloques con error:", fallos)
