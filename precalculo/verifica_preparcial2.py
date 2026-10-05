#!/usr/bin/env python3
"""verifica_preparcial2.py — rehace cada cifra del preparcial del Corte II.

Uso (desde la raíz del repositorio):

    python3 precalculo/verifica_preparcial2.py              # todas las secciones
    python3 precalculo/verifica_preparcial2.py --inyecta    # además, sabotea y exige cazarlo

Es INDEPENDIENTE del generador: no ejecuta `genera_preparcial2.R` ni resimula
nada. Lee la página publicada —el texto que el estudiante ve, extraído con
`extrae_preparcial2.js` con cada cifra ya interpolada— y los valores publicados
de cada serie, y rehace desde ahí, en Python (numpy, scipy, statsmodels), todo
lo que se puede rehacer. Otro lenguaje y otras bibliotecas: un error del
generador no se copia aquí por construcción.

Las estimaciones de R y de statsmodels no coinciden en el tercer o cuarto
decimal (verosimilitud exacta frente a espacio de estados, primeros residuales),
así que las cifras que dependen de un ajuste se comprueban con tolerancias
medidas, y las que son aritmética sobre cifras impresas, exactas.

Secciones:
  §1 El JSON incrustado frente a salidas/preparcial2_datos.json
  §2 Las series: forma y coherencia con lo que citan los ítems
  §3 Las cifras de los 38 ítems, rehechas
  §4 La procedencia de cada número impreso en la prosa
  §5 Las claves numéricas: decimales pedidos y errores que la tolerancia debe dejar fuera
  §6 La tabla de especificaciones y los 20 módulos
  §7 La posición de la opción correcta
  §8 Casi-duplicados contra lo que el estudiante ya vio
  §9 La prueba del propio verificador (--inyecta)
"""
import hashlib
import html as htmlmod
import json
import math
import pathlib
import re
import subprocess
import sys
import tempfile
import unicodedata
import warnings

import numpy as np
from scipy import stats

warnings.filterwarnings("ignore")
from statsmodels.stats.diagnostic import acorr_ljungbox  # noqa: E402
from statsmodels.tsa.arima.model import ARIMA  # noqa: E402
from statsmodels.tsa.arima_process import arma2ma, arma_acf  # noqa: E402
from statsmodels.tsa.stattools import adfuller, kpss  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent
HTML = RAIZ / "Htmls_Series" / "preparcial-corte-2.html"
DATOS = RAIZ / "precalculo" / "salidas" / "preparcial2_datos.json"
EXTRACTOR = RAIZ / "precalculo" / "extrae_preparcial2.js"

MODULOS = ["3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8", "3.9", "3.10",
           "4.1", "4.2", "4.3", "4.4", "4.5", "4.6", "4.7", "4.8", "4.9", "4.10"]
OBJETIVO_DE = {"3.1": "O1", "3.2": "O1", "3.3": "O1", "3.4": "O2", "3.5": "O2", "3.6": "O2",
               "3.7": "O3", "3.8": "O3", "3.9": "O3", "3.10": "O3",
               "4.1": "O4", "4.3": "O4", "4.5": "O4", "4.2": "O5", "4.4": "O5", "4.6": "O5",
               "4.7": "O5", "4.8": "O6", "4.9": "O6", "4.10": "O6"}
PESOS = {"O1": 15, "O2": 15, "O3": 20, "O4": 15, "O5": 15, "O6": 20}


class Registro:
    def __init__(self, silencioso=False):
        self.n = 0
        self.fallos = []
        self.seccion = ""
        self.silencioso = silencioso
        self.por_seccion = {}

    def abre(self, titulo):
        self.seccion = titulo.split(" ")[0]
        self.por_seccion.setdefault(self.seccion, 0)
        if not self.silencioso:
            print(f"\n{titulo}")

    def ok(self, condicion, mensaje):
        self.n += 1
        self.por_seccion[self.seccion] = self.por_seccion.get(self.seccion, 0) + 1
        if not condicion:
            self.fallos.append((self.seccion, mensaje))
            if not self.silencioso:
                print(f"  FALLA  {mensaje}")
        return bool(condicion)

    def cerca(self, a, b, tol, mensaje):
        return self.ok(a is not None and b is not None and abs(float(a) - float(b)) <= tol,
                       f"{mensaje}: {a} frente a {b} (tolerancia {tol})")


# ---------------------------------------------------------------------------
# Herramientas numéricas, escritas desde su definición
# ---------------------------------------------------------------------------
def acf(x, k=20):
    x = np.asarray(x, float)
    d = x - x.mean()
    den = np.sum(d * d)
    return np.array([np.sum(d[:-h] * d[h:]) / den for h in range(1, k + 1)])


def pacf_dl(r):
    """PACF por Durbin–Levinson sobre la ACF r[1..K] (la definición de stats::pacf)."""
    K = len(r)
    phi = np.zeros((K + 1, K + 1))
    out = []
    for k in range(1, K + 1):
        if k == 1:
            phi[1, 1] = r[0]
        else:
            num = r[k - 1] - sum(phi[k - 1, j] * r[k - 1 - j] for j in range(1, k))
            den = 1 - sum(phi[k - 1, j] * r[j - 1] for j in range(1, k))
            phi[k, k] = num / den
            for j in range(1, k):
                phi[k, j] = phi[k - 1, j] - phi[k, k] * phi[k - 1, k - j]
        out.append(phi[k, k])
    return np.array(out)


def acf_teorica(ar=(), ma=(), k=20):
    return arma_acf(np.r_[1, -np.asarray(ar, float)], np.r_[1, np.asarray(ma, float)], k + 1)[1:]


def psi(ar=(), ma=(), k=10):
    return arma2ma(np.r_[1, -np.asarray(ar, float)], np.r_[1, np.asarray(ma, float)], k + 1)[1:]


def raices_B(coef_phi):
    """Módulos de las raíces de 1 - phi1 B - ... (polinomio en B)."""
    p = np.r_[1, -np.asarray(coef_phi, float)]
    return np.sort(np.abs(np.roots(p[::-1])))


def raices_MA(coef_theta):
    p = np.r_[1, np.asarray(coef_theta, float)]
    return np.sort(np.abs(np.roots(p[::-1])))


def ajusta(y, orden, tendencia="n"):
    return ARIMA(np.asarray(y, float), order=orden, trend=tendencia).fit()


def aicc_sm(f, n_ef):
    k = len(f.params)          # statsmodels cuenta sigma2 entre los parámetros
    return -2 * f.llf + 2 * k + 2 * k * (k + 1) / (n_ef - k - 1)


def banda(n):
    return 1.96 / math.sqrt(n)


def var_r(x):
    return float(np.var(np.asarray(x, float), ddof=1))


def parsea_salida(texto):
    """Coeficientes y errores estándar de una salida impresa de arima()/Arima()."""
    lineas = texto.split("\n")
    i = next(j for j, l in enumerate(lineas) if l.startswith("Coefficients"))
    nombres = lineas[i + 1].split()
    valores = [float(v) for v in lineas[i + 2].split()]
    ees = [float(v) for v in lineas[i + 3].split()[1:]]
    return dict(zip(nombres, valores)), dict(zip(nombres, ees))


# ---------------------------------------------------------------------------
# Lectura de la página
# ---------------------------------------------------------------------------
def extrae(ruta):
    r = subprocess.run(["node", str(EXTRACTOR), str(ruta)], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("No pude extraer los ítems:\n" + r.stderr[-2000:])
    return json.loads(r.stdout)


def limpia(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return htmlmod.unescape(s)


def textos_de(p):
    """Todo lo que el estudiante puede leer de un ítem, en un solo texto."""
    partes = [p.get("pregunta", ""), p.get("pista", ""), p.get("retroAcierto", ""),
              p.get("retroFallo", "")]
    for o in p.get("opciones", []) or []:
        partes += [o.get("texto", ""), o.get("retro", "")]
    return limpia(" \n ".join(partes))


def todos_los_items(E):
    """(etiqueta, clave del precálculo, ítem). El mapa ítem → clave se declara aquí
    y se comprueba: el motor no numera los ítems."""
    mapa = {
        "bloque-a": ["i05", "i09", "i15", "i26", "i23", "i32"],
        "bloque-b": ["i01", "i03", "i06", "i10", "i11", "i12", "i17", "i19", "i25", "i27", "i28", "i31"],
        "bloque-c": ["i04", "i13", "i14", "i21", "i18", "i20", "i24", "i30"],
        "bloque-d": ["i02", "i07", "i08", "i16", "i22", "i29"],
    }
    out = []
    for b, claves in mapa.items():
        items = E["bloques"][b]
        if len(items) != len(claves):
            raise SystemExit(f"{b} tiene {len(items)} ítems y el mapa declara {len(claves)}")
        for i, (p, k) in enumerate(zip(items, claves)):
            out.append((f"{b}#{i + 1}", k, p))
    for i, p in enumerate(E["simulacro"]["items"]):
        out.append((f"simulacro#{i + 1}", f"s{i + 1}", p))
    return out


# ---------------------------------------------------------------------------
# §1 Anclas
# ---------------------------------------------------------------------------
def seccion1(R, E, html_txt):
    R.abre("§1 · El JSON incrustado frente a salidas/preparcial2_datos.json")
    disco = json.loads(DATOS.read_text(encoding="utf-8"))
    R.ok(E["datos"] == disco, "el PREPARCIAL_DATOS de la página no es el de salidas/")
    m = re.search(r"const PREPARCIAL_DATOS = (\{.*?\});\n", html_txt)
    R.ok(m is not None, "no encuentro la línea de PREPARCIAL_DATOS")
    if m:
        js = (DATOS.parent / "preparcial2_datos.js").read_text(encoding="utf-8").strip()
        R.ok(js == f"const PREPARCIAL_DATOS = {m.group(1)};",
             "la línea incrustada no es byte a byte la de preparcial2_datos.js")
    meta = disco["meta"]
    R.ok(meta["semilla"] == 20261013, f"semilla {meta['semilla']}")
    R.ok(meta["n_items"] == 32 and meta["n_simulacro"] == 6, "el precálculo no declara 32 + 6 ítems")
    return disco


# ---------------------------------------------------------------------------
# §2 Series
# ---------------------------------------------------------------------------
def seccion2(R, D):
    R.abre("§2 · Las series: forma y coherencia")
    S = D["series"]
    for nombre, s in S.items():
        R.ok(len(s["valores"]) == s["n"], f"{nombre}: n = {s['n']} y {len(s['valores'])} valores")
        R.ok(all(isinstance(v, (int, float)) and math.isfinite(v) for v in s["valores"]),
             f"{nombre}: valores no finitos")
    I = D["items"]
    R.ok(S["ventas_semanales"]["valores"][-1] == I["i17"]["yT"], "i17: y_T no es el último dato")
    R.ok(S["suscriptores"]["valores"][0] == I["i19"]["y1"] and
         S["suscriptores"]["valores"][-1] == I["i19"]["yn"], "i19: y_1 o y_n no son los extremos")
    R.ok(S["nivel_embalse"]["valores"][-2:] == [I["i27"]["yT_1"], I["i27"]["yT"]],
         "i27: los dos últimos datos no son los citados")
    R.ok(abs(S["indice_bursatil"]["valores"][-1] - I["i31"]["yT"]) < 0.006, "i31: y_T no es el último cierre")
    for k, nombre in [("i07", "humedad"), ("i08", "errores_sensor"), ("i11", "vibracion"),
                      ("i13", "nivel_tanque"), ("i14", "rendimientos"), ("i16", "trafico"),
                      ("i18", "pedidos"), ("i19", "suscriptores"), ("i21", "cotizacion"),
                      ("i22", "consumo"), ("i24", "exportaciones"), ("i25", "turistas"),
                      ("i29", "usuarios"), ("i30", "llamadas")]:
        R.ok(S[nombre]["n"] == I[k]["n"], f"{k}: n = {I[k]['n']} y la serie {nombre} tiene {S[nombre]['n']}")


# ---------------------------------------------------------------------------
# §3 Las cifras, rehechas
# ---------------------------------------------------------------------------
def seccion3(R, D):
    R.abre("§3 · Las cifras de los 38 ítems, rehechas desde las series y los parámetros")
    I, S, M = D["items"], D["series"], D["simulacro"]
    v = lambda nombre: np.asarray(S[nombre]["valores"], float)  # noqa: E731

    # i01 · (1 - 0.8B)(1 + 0.5B)
    pol = np.polymul([1, -0.8], [1, 0.5])
    R.cerca(-pol[1], I["i01"]["phi"][0], 1e-12, "i01 phi1")
    R.cerca(-pol[2], I["i01"]["phi"][1], 1e-12, "i01 phi2")
    rz = np.sort(np.roots(pol[::-1]).real)
    R.ok(np.allclose(rz, I["i01"]["raices"], atol=1e-4), f"i01 raíces {rz}")
    R.ok(all(abs(r) > 1 for r in rz), "i01 no es estacionario")

    # i02 · ACF teórica de un AR(2) (1, -0.6) y sus tres alternativas
    a = acf_teorica([1.0, -0.6], k=20)
    R.ok(np.allclose(a, I["i02"]["acf"], atol=6e-5), "i02 ACF teórica")
    R.cerca(1 / math.sqrt(0.6), I["i02"]["modulo"], 6e-4, "i02 módulo")
    R.cerca(2 * math.pi / math.acos(1 / (2 * math.sqrt(0.6))), I["i02"]["periodo"], 6e-3, "i02 periodo")
    R.ok(1.0 + 4 * -0.2 > 0, "i02: la alternativa (1, -0.2) debería tener raíces reales")
    R.ok(np.allclose(acf_teorica([1.0, -0.2], k=6), I["i02"]["alternativas"]["reales"]["acf"], atol=6e-5),
         "i02 ACF de (1, -0.2)")
    R.ok(np.allclose(acf_teorica([-1.0, -0.6], k=6), I["i02"]["alternativas"]["negativo"]["acf"], atol=6e-5),
         "i02 ACF de (-1, -0.6)")
    R.cerca(2 * math.pi / math.acos(-1 / (2 * math.sqrt(0.6))),
            I["i02"]["alternativas"]["negativo"]["periodo"], 6e-3, "i02 periodo de (-1, -0.6)")
    R.ok(not (-1 < -1.1 < 1), "i02: la alternativa fuera del triángulo debería violar |phi2| < 1")

    # i03 · MA(2) (-0.5, 0.3)
    t1, t2 = -0.5, 0.3
    den = 1 + t1 ** 2 + t2 ** 2
    R.cerca((t1 + t1 * t2) / den, I["i03"]["rho1"], 6e-5, "i03 rho1")
    R.cerca(t2 / den, I["i03"]["rho2"], 6e-5, "i03 rho2")
    R.ok(np.allclose(acf_teorica(ma=[t1, t2], k=3), I["i03"]["acf_R"], atol=6e-5), "i03 ACF teórica")
    R.cerca(t1 / den, I["i03"]["rho1_sin_producto"], 6e-5, "i03 distractor sin producto")
    R.cerca((t1 + t1 * t2) / (1 + t1 ** 2), I["i03"]["rho1_sin_theta2"], 6e-5, "i03 distractor sin theta2")
    R.ok(all(raices_MA([t1, t2]) > 1), "i03: el MA(2) no es invertible")

    # i04 · theta y 1/theta
    i4 = I["i04"]
    R.cerca(1 / i4["theta_R"], i4["theta_otro"], 1e-3, "i04 1/theta")
    R.cerca(i4["sigma2_R"] * i4["theta_R"] ** 2, i4["sigma2_otro"], 1e-3, "i04 theta^2 sigma^2")
    R.cerca(i4["theta_R"] / (1 + i4["theta_R"] ** 2), i4["rho1_R"], 1e-4, "i04 rho1")
    R.cerca(i4["theta_otro"] / (1 + i4["theta_otro"] ** 2), i4["rho1_R"], 2e-4, "i04 rho1 con 1/theta")
    R.cerca(i4["sigma2_R"] * (1 + i4["theta_R"] ** 2), i4["gamma0_R"], 1e-3, "i04 gamma0")
    R.cerca(i4["sigma2_otro"] * (1 + i4["theta_otro"] ** 2), i4["gamma0_R"], 2e-3, "i04 gamma0 con la otra pareja")
    R.cerca(1 / i4["theta_R"], i4["raiz_R"], 1e-3, "i04 módulo de la raíz")

    # i05
    R.cerca(-0.45 / (1 + 0.45 ** 2), I["i05"]["rho1"], 6e-5, "i05 rho1")

    # i06 · techo del ARMA(1,1)
    ph, th, s2 = 0.6, -0.3, 4
    g0 = s2 * (1 + 2 * ph * th + th ** 2) / (1 - ph ** 2)
    R.cerca(g0, I["i06"]["gamma0"], 6e-5, "i06 gamma0")
    R.cerca(s2 * (1 + np.sum(psi([ph], [th], 3000) ** 2)), g0, 1e-9, "i06 gamma0 por los psi")
    R.cerca(1.96 * math.sqrt(g0), I["i06"]["semiancho"], 6e-5, "i06 semiancho")
    R.cerca(1.96 * math.sqrt(s2 * (1 - 2 * ph * th + th ** 2) / (1 - ph ** 2)), I["i06"]["semiancho_signo"], 6e-5,
            "i06 distractor de signo")
    R.cerca(1.96 * g0, I["i06"]["semiancho_sin_raiz"], 6e-5, "i06 distractor sin raíz")
    R.ok(np.allclose(psi([ph], [th], 5), I["i06"]["psi"], atol=6e-5), "i06 psi")

    # i07 · humedad
    y = v("humedad")
    R.ok(np.allclose(acf(y), I["i07"]["acf"], atol=6e-4), "i07 ACF")
    R.ok(np.allclose(pacf_dl(acf(y)), I["i07"]["pacf"], atol=6e-4), "i07 PACF")
    R.cerca(banda(200), I["i07"]["banda"], 6e-4, "i07 banda")
    p = pacf_dl(acf(y))
    b = banda(200)
    R.ok(all(abs(p[:3]) > b) and all(abs(p[3:]) < b) and p[0] > p[1] > p[2] > 0,
         "i07: la PACF no tiene la forma que el ítem describe (tres fuera, decreciendo, luego dentro)")
    ar3, a11, ar1 = ajusta(y, (3, 0, 0), "c"), ajusta(y, (1, 0, 1), "c"), ajusta(y, (1, 0, 0), "c")
    R.cerca(aicc_sm(ar3, 200), I["i07"]["aicc"]["ar3"], 0.6, "i07 AICc del AR(3)")
    R.cerca(aicc_sm(a11, 200), I["i07"]["aicc"]["arma11"], 0.6, "i07 AICc del ARMA(1,1)")
    R.cerca(aicc_sm(ar1, 200), I["i07"]["aicc"]["ar1"], 0.6, "i07 AICc del AR(1)")
    R.cerca(-2 * ar3.llf + 5 * math.log(200), I["i07"]["bic"]["ar3"], 0.6, "i07 BIC del AR(3)")
    R.cerca(-2 * a11.llf + 4 * math.log(200), I["i07"]["bic"]["arma11"], 0.6, "i07 BIC del ARMA(1,1)")
    R.ok(I["i07"]["bic"]["arma11"] < I["i07"]["bic"]["ar3"], "i07: el BIC no prefiere el ARMA(1,1)")
    R.ok(abs(I["i07"]["aicc"]["ar3"] - I["i07"]["aicc"]["arma11"]) < 2 and
         I["i07"]["aicc"]["ar1"] > max(I["i07"]["aicc"]["ar3"], I["i07"]["aicc"]["arma11"]) + 5,
         "i07: el empate AR(3)–ARMA(1,1) o el descarte del AR(1) no se sostienen")

    # i08 · errores_sensor
    y = v("errores_sensor")
    a = acf(y)
    R.ok(np.allclose(a, I["i08"]["acf"], atol=6e-4), "i08 ACF")
    fuera = [k + 1 for k in range(20) if abs(a[k]) > banda(100)]
    R.ok(fuera == I["i08"]["fuera"] == [1, 19], f"i08 barras fuera {fuera}")
    R.ok(pacf_dl(a)[1] < -banda(100), "i08: la PACF en 2 no sale por abajo")
    R.cerca(0.55 / (1 + 0.55 ** 2), I["i08"]["rho1_teorico"], 6e-5, "i08 rho1 teórico")

    # i09 · factor común
    rz = np.sort(np.abs(np.roots([0.15, -0.8, 1])))
    R.ok(np.allclose(rz, [2, 1 / 0.3], atol=1e-9), f"i09 raíces AR {rz}")
    R.ok(np.allclose(np.polymul([1, -0.5], [1, -0.3]), [1, -0.8, 0.15]), "i09 factorización")

    # i10 · de psi a theta
    R.ok(np.allclose(psi([0.9], [-0.7], 4), I["i10"]["psi"], atol=6e-5), "i10 psi")

    # i11 · vibracion: Yule–Walker
    y = v("vibracion")
    g0_ = np.sum((y - y.mean()) ** 2) / len(y)
    R.cerca(g0_, I["i11"]["gamma0"], 0.006, "i11 gamma0 (divisor n)")
    R.cerca(acf(y, 1)[0], I["i11"]["r1"], 6e-4, "i11 r1")
    R.cerca(I["i11"]["gamma0"] * (1 - I["i11"]["r1"] ** 2), I["i11"]["sigma2"], 6e-5, "i11 sigma2")
    R.cerca(I["i11"]["sigma2"] * 90 / 88, I["i11"]["sigma2_ar_R"], 0.01, "i11 lo que imprime ar()")

    # i12 · Q de Ljung–Box
    r = np.asarray(I["i12"]["r"])
    Q = 100 * 102 * np.sum(r ** 2 / (100 - np.arange(1, 5)))
    R.cerca(Q, I["i12"]["Q"], 6e-5, "i12 Q(4)")
    R.cerca(100 * np.sum(r ** 2), I["i12"]["Q_box_pierce"], 6e-5, "i12 Box–Pierce")
    R.cerca(stats.chi2.ppf(0.95, 2), I["i12"]["critico_gl2"], 6e-4, "i12 crítico 2 gl")
    R.cerca(stats.chi2.ppf(0.95, 4), I["i12"]["critico_gl4"], 6e-4, "i12 crítico 4 gl")
    R.ok(I["i12"]["critico_gl2"] < Q < I["i12"]["critico_gl4"], "i12: Q no cae entre los dos críticos")
    R.ok(all(abs(r) < banda(100)), "i12: alguna barra sale de la banda")
    R.cerca(stats.chi2.sf(I["i12"]["Q_R"], 2), I["i12"]["p_R"], 6e-5, "i12 p de R")

    # i13 · nivel_tanque: CSS, ML, YW
    y = v("nivel_tanque")
    X = np.c_[np.ones(len(y) - 1), y[:-1]]
    beta = np.linalg.lstsq(X, y[1:], rcond=None)[0]
    R.cerca(beta[1], I["i13"]["css"]["phi"], 0.002, "i13 phi de CSS (MCO condicionado)")
    R.ok(I["i13"]["css"]["phi"] >= 1, "i13: CSS no se sale de la región estacionaria")
    ml = ajusta(y, (1, 0, 0), "c")
    R.cerca(ml.params[1], I["i13"]["ml"]["phi"], 0.01, "i13 phi de ML")
    R.cerca(acf(y, 1)[0], I["i13"]["yw"]["phi"], 6e-4, "i13 phi de YW = r1")
    R.ok("non-stationary" in I["i13"]["por_defecto"], "i13: arima() por defecto no falla en esta serie")
    R.ok((I["i13"]["css"]["phi"] - I["i13"]["yw"]["phi"]) / I["i13"]["ml"]["se"] > 4, "i13: la distancia no pasa de cuatro e.e.")
    R.cerca((I["i13"]["ml"]["phi"] - I["i13"]["yw"]["phi"]) / I["i13"]["ml"]["se"],
            I["i13"]["distancia_ml_yw_ee"], 0.01, "i13 distancia en e.e.")

    # i14 · rendimientos
    y = v("rendimientos")
    a = acf(y)
    R.ok(np.allclose(a, I["i14"]["acf"], atol=6e-4), "i14 ACF")
    fuera = [k + 1 for k in range(20) if abs(a[k]) > banda(120)]
    R.ok(fuera == [I["i14"]["fuera"]], f"i14 barras fuera {fuera}")
    lb = acorr_ljungbox(y, lags=[12])["lb_pvalue"].iloc[0]
    R.cerca(lb, I["i14"]["lb12"], 0.002, "i14 Ljung–Box(12)")
    f0, f1 = ajusta(y, (0, 0, 0), "c"), ajusta(y, (0, 0, 1), "c")
    R.cerca(aicc_sm(f0, 120), I["i14"]["aicc_rb"], 0.2, "i14 AICc del ruido blanco")
    R.cerca(aicc_sm(f1, 120), I["i14"]["aicc_ma1"], 0.2, "i14 AICc del MA(1)")
    R.cerca(I["i14"]["aicc_rb"] - I["i14"]["aicc_ma1"], I["i14"]["dif_aicc"], 0.011, "i14 diferencia")
    R.ok(0 < I["i14"]["dif_aicc"] < 2 and abs(I["i14"]["t_ma1"]) < 1.96, "i14: el MA(1) no queda empatado")
    R.cerca(I["i14"]["ma1"] / I["i14"]["se_ma1"], I["i14"]["t_ma1"], 0.006, "i14 t del MA(1) = coeficiente / e.e.")
    R.cerca(f1.params[1], I["i14"]["ma1"], 0.03, "i14 theta del MA(1)")
    R.ok(I["i14"]["bic_rb"] < I["i14"]["bic_ma1"], "i14: el BIC no prefiere el ruido blanco")

    # i16 · trafico
    y = v("trafico")
    f = ajusta(y, (1, 0, 0), "c")
    e = f.resid[1:]
    R.ok(np.allclose(acf(e), I["i16"]["acf_res"], atol=0.01), "i16 ACF de residuales")
    R.ok(max(abs(np.asarray(I["i16"]["acf_res"]))) < banda(150), "i16: alguna barra sale de la banda")
    pv = acorr_ljungbox(e, lags=list(range(2, 21)), model_df=1)["lb_pvalue"].values
    R.ok(all(pv[:9] < 0.06) and pv[-1] > 0.1, f"i16 patrón de Ljung–Box por rezago {np.round(pv, 3)}")
    R.ok(all(np.asarray(I["i16"]["p_lb"][:9]) < 0.05) and all(np.asarray(I["i16"]["p_lb"][9:]) > 0.05),
         "i16: los p publicados no cambian de lado en el rezago 11")
    R.ok(I["i16"]["ar3"]["aicc"] < I["i16"]["aicc_ar1"] and I["i16"]["ar3"]["p_min"] > 0.05, "i16: el AR(3) no lo arregla")

    # i17 · SES
    i17 = I["i17"]
    R.cerca(1 + i17["theta"], i17["alfa"], 1e-9, "i17 alfa")
    R.cerca(i17["alfa"] * i17["yT"] + (1 - i17["alfa"]) * i17["yhat_T"], i17["pronostico"], 0.006, "i17 pronóstico")
    R.cerca(i17["pronostico"], i17["pronostico_R"], 0.011, "i17 frente a forecast()")
    R.cerca(ajusta(v("ventas_semanales"), (0, 1, 1)).params[0], i17["theta"], 0.03, "i17 theta")

    # i18 · pedidos
    y = v("pedidos")
    var = [var_r(y), var_r(np.diff(y)), var_r(np.diff(y, 2))]
    R.ok(np.allclose(var, I["i18"]["varianzas"], atol=0.006), f"i18 varianzas {np.round(var, 2)}")
    R.cerca(acf(y, 1)[0], I["i18"]["r1"], 6e-4, "i18 r1")
    R.cerca(2 * (1 - I["i18"]["r1"]), I["i18"]["razon_teorica"], 6e-5, "i18 2(1 - r1)")
    R.ok(adfuller(y, regression="ct")[1] < 0.05, "i18: ADF no rechaza")
    R.ok(kpss(y, regression="c", nlags=4)[1] >= 0.1, "i18: KPSS rechaza")
    f = ajusta(y, (2, 0, 0), "c")
    R.cerca(min(raices_B(f.params[1:3])), I["i18"]["ar2"]["modulo"], 0.05, "i18 módulo del AR(2)")
    c1, c2 = I["i18"]["ar2"]["coef"]
    R.ok(c1 ** 2 + 4 * c2 < 0, "i18: las raíces no son complejas")
    R.cerca(2 * math.pi / math.acos(c1 / (2 * math.sqrt(-c2))), I["i18"]["periodo"], 0.01, "i18 periodo")

    # i19 · deriva
    R.cerca((I["i19"]["yn"] - I["i19"]["y1"]) / 59, I["i19"]["deriva"], 6e-5, "i19 deriva")
    R.cerca(np.mean(np.diff(v("suscriptores"))), I["i19"]["deriva"], 6e-5, "i19 media de las diferencias")
    R.cerca((I["i19"]["yn"] - I["i19"]["y1"]) / 60, I["i19"]["deriva_n"], 6e-5, "i19 distractor /60")

    # i20 · matriculas
    cf, ee = parsea_salida(I["i20"]["salida"])
    R.cerca(cf["ar1"], I["i20"]["phi"], 6e-5, "i20 ar1 de la salida")
    R.cerca(cf["drift"], I["i20"]["deriva"], 6e-5, "i20 drift de la salida")
    R.cerca(I["i20"]["deriva"] * (1 - I["i20"]["phi"]), I["i20"]["c"], 3e-4, "i20 c")
    R.cerca(I["i20"]["deriva"] / (1 - I["i20"]["phi"]), I["i20"]["deriva_sobre"], 3e-4, "i20 distractor")
    R.cerca(cf["drift"] / ee["drift"], I["i20"]["t_deriva"], 0.02, "i20 t de la deriva")
    R.cerca(np.mean(np.diff(v("matriculas"))), I["i20"]["deriva"], 0.15, "i20 deriva frente a la media de las diferencias")
    R.cerca(I["i20"]["pendiente_final"], I["i20"]["deriva"], 1e-3, "i20 pendiente final")

    # i21 · cotizacion
    y = v("cotizacion")
    f = ajusta(y, (2, 0, 0), "c")
    R.cerca(f.params[1], I["i21"]["ar2"]["coef"][0], 0.02, "i21 phi1")
    R.cerca(f.params[2], I["i21"]["ar2"]["coef"][1], 0.02, "i21 phi2")
    R.ok(np.allclose(raices_B(I["i21"]["ar2"]["coef"]), I["i21"]["ar2"]["raices"], atol=2e-4), "i21 raíces")
    R.cerca(sum(I["i21"]["ar2"]["coef"]), I["i21"]["ar2"]["suma"], 2e-4, "i21 suma")
    R.cerca(ajusta(y, (1, 1, 0)).params[0], I["i21"]["arima110"]["phi"], 0.02, "i21 ARIMA(1,1,0)")
    R.ok(adfuller(y, regression="ct")[1] > 0.1 and kpss(y, regression="c", nlags=4)[1] <= 0.01,
         "i21: las pruebas no apuntan a la raíz unitaria")

    # i22 · consumo
    y = v("consumo")
    dy = np.diff(y)
    R.ok(np.allclose(acf(dy), I["i22"]["acf"], atol=6e-4), "i22 ACF de la diferencia")
    p = pacf_dl(acf(dy))
    R.ok(np.allclose(p, I["i22"]["pacf"], atol=6e-4), "i22 PACF de la diferencia")
    R.ok(np.allclose(acf(y, 6), I["i22"]["acf_nivel"], atol=6e-4), "i22 ACF en niveles")
    b = banda(159)
    R.ok(all(abs(p[:2]) > b) and all(abs(p[2:]) < b), "i22: la PACF no se corta en 2")

    # i24 · exportaciones
    y = v("exportaciones")
    filas = I["i24"]["d1"]
    R.ok([f["AICc"] for f in filas] == sorted(f["AICc"] for f in filas), "i24: la rejilla no va ordenada")
    deg = [min(f["raiz_ar"] or 9, f["raiz_ma"] or 9) < 1.01 for f in filas]
    R.ok(deg[0] and not any(deg[1:]), f"i24: degenerados {deg}")
    dy = np.diff(y)
    s2 = np.mean(dy ** 2)
    ll = -len(dy) / 2 * (math.log(2 * math.pi * s2) + 1)
    rw = next(f for f in filas if (f["p"], f["q"]) == (0, 0))
    R.cerca(-2 * ll + 2 + 2 * 1 * 2 / (139 - 1 - 1), rw["AICc"], 0.006, "i24 AICc de la caminata, exacto")
    c = I["i24"]["coef_212"]
    R.cerca(min(raices_B(c[:2])), filas[0]["raiz_ar"], 0.01, "i24 raíz AR del (2,1,2) desde sus coeficientes")
    R.cerca(min(raices_MA(c[2:])), filas[0]["raiz_ma"], 0.01, "i24 raíz MA del (2,1,2) desde sus coeficientes")
    dy = np.diff(y)
    lb = acorr_ljungbox(dy, lags=[10, 20])["lb_pvalue"].values
    R.cerca(lb[0], I["i24"]["lb_caminata"]["p10"], 0.002, "i24 Ljung–Box(10) de la caminata")
    R.cerca(lb[1], I["i24"]["lb_caminata"]["p20"], 0.002, "i24 Ljung–Box(20) de la caminata")
    R.ok(min(lb) > 0.15, "i24: la caminata que el ítem da por buena no pasa su diagnóstico")
    R.ok(sum(abs(acf(dy, 24)) > banda(len(dy))) == I["i24"]["lb_caminata"]["fuera24"] <= 1,
         "i24: barras fuera en la ACF de las diferencias")
    z = np.roots(np.r_[1, -np.asarray(c[:2])][::-1])
    R.ok(abs(z[0].imag) > 1e-6 and I["i24"]["raices_ar_212"]["compleja"], "i24: las raíces AR del (2,1,2) no son complejas")
    R.cerca(2 * math.pi / abs(np.angle(z[0])), I["i24"]["raices_ar_212"]["periodo"], 0.15, "i24 periodo del ciclo del (2,1,2)")
    R.ok(filas[1]["p"] == 0 and filas[1]["q"] == 0, "i24: el mejor de los sanos no es la caminata")
    fd = ajusta(y, (0, 1, 0), "t")
    R.cerca(fd.params[0] / fd.bse[0], I["i24"]["deriva"]["t"], 0.2, "i24 t de la deriva")

    # i25 · AICc a mano
    i25 = I["i25"]
    R.cerca(-2 * i25["logL"] + 2 * 4 + 40 / 114, i25["aicc"], 0.006, "i25 AICc")
    R.cerca(i25["aicc"], i25["aicc_R"], 0.011, "i25 frente a Arima()")
    R.cerca(-2 * i25["logL"] + 2 * 3 + 24 / 115, i25["aicc_k_menos_1"], 0.006, "i25 distractor k - 1")
    f = ajusta(v("turistas"), (1, 1, 1), "t")
    R.cerca(f.llf, i25["logL"], 1.0, "i25 log L")

    # i27 · pronóstico del ARIMA(1,1,0)
    i27 = I["i27"]
    p1 = i27["yT"] + i27["phi"] * (i27["yT"] - i27["yT_1"])
    p2 = p1 + i27["phi"] * (p1 - i27["yT"])
    R.cerca(p1, i27["paso1"], 6e-5, "i27 paso 1")
    R.cerca(p2, i27["paso2"], 6e-5, "i27 paso 2")
    R.cerca(p2, i27["paso2_R"], 0.006, "i27 frente a predict()")
    R.cerca(ajusta(v("nivel_embalse"), (1, 1, 0)).params[0], i27["phi"], 0.02, "i27 phi")

    # i28 · ARIMA(0,1,1), h = 3
    i28 = I["i28"]
    ps = 1 + i28["theta"]
    R.cerca(1.96 * i28["sigma"] * math.sqrt(1 + 2 * ps ** 2), i28["semiancho"], 6e-5, "i28 semiancho")
    R.cerca(i28["semiancho"], i28["semiancho_R"], 0.006, "i28 frente a forecast()")
    R.cerca(1.96 * i28["sigma"] * math.sqrt(3), i28["semiancho_caminata"], 6e-5, "i28 caminata")
    R.cerca(1.96 * i28["sigma"] * math.sqrt(2 * ps ** 2), i28["semiancho_sin_psi0"], 6e-5, "i28 sin psi0")
    f = ajusta(v("visitas"), (0, 1, 1))
    R.cerca(f.params[0], i28["theta"], 0.03, "i28 theta")

    # i29 · usuarios, ARIMA(0,2,1)
    i29 = I["i29"]
    f = ajusta(v("usuarios"), (0, 2, 1))
    fc = f.get_forecast(24)
    se = fc.se_mean
    R.cerca(f.params[0], i29["theta"], 0.03, "i29 theta")
    R.cerca(1.96 * se[23] / (1.96 * se[0]), i29["razon_24"], 0.6, "i29 razón de semianchos")
    R.ok(i29["razon_24"] > 3 * math.sqrt(24), "i29: la banda no crece mucho más deprisa que raíz de h")
    th = i29["theta"]
    R.ok(np.allclose([1 + j * (1 + th) for j in range(6)], i29["psi"], atol=6e-4), "i29 psi = 1 + j(1 + theta)")
    R.cerca(np.diff(fc.predicted_mean)[-1], i29["pendiente"], 0.3, "i29 pendiente")
    f2 = ajusta(v("usuarios"), (0, 1, 1), "t")
    se2 = f2.get_forecast(24).se_mean
    R.cerca(se2[23] / se2[0], i29["razon_011_deriva"], 0.6, "i29 razón del ARIMA(0,1,1) con deriva")
    R.ok(i29["razon_011_deriva"] < 2 * math.sqrt(24) < i29["razon_24"], "i29: las dos razones no se separan")

    # i30 · llamadas
    y = v("llamadas")
    f = ajusta(y, (1, 0, 0), "c")
    e = f.resid[1:]
    R.cerca(acorr_ljungbox(e, lags=[10], model_df=1)["lb_pvalue"].iloc[0], I["i30"]["lb10"], 0.06, "i30 Ljung–Box")
    R.ok(stats.shapiro(e).pvalue < 1e-5 and I["i30"]["shapiro"] < 1e-6, "i30 Shapiro–Wilk")
    k = np.mean((e - e.mean()) ** 4) / np.mean((e - e.mean()) ** 2) ** 2
    R.cerca(k, I["i30"]["curtosis"], 0.3, "i30 curtosis")
    s = math.sqrt(f.params[-1])
    for clave, z in (("n80", 1.2816), ("n95", 1.96), ("n99", 2.5758)):
        R.cerca(np.mean(np.abs(e) > z * s), I["i30"]["fuera"][clave], 0.016, f"i30 fuera del {clave}")

    # i31 · caminata, 80 %
    i31 = I["i31"]
    dy = np.diff(v("indice_bursatil"))
    R.cerca(math.sqrt(np.mean(dy ** 2)), i31["sigma"], 0.15, "i31 sigma de la caminata")
    R.cerca(1.282 * i31["sigma"] * 2, i31["semiancho"], 0.006, "i31 semiancho")
    R.cerca(i31["semiancho"], i31["semiancho_R"], 0.05, "i31 frente a forecast()")

    # i32 · techo frente a caminata
    R.cerca(1.96 * 50 * math.sqrt(60), I["i32"]["caminata_60"], 0.06, "i32 caminata")
    R.cerca(1.96 * 50 / math.sqrt(1 - 0.64), I["i32"]["ar1_techo"], 0.06, "i32 techo")
    R.cerca(1.96 * 50 * math.sqrt((1 - 0.8 ** 120) / 0.36), I["i32"]["ar1_60"], 0.06, "i32 AR(1) a 60")

    # Simulacro
    ph1, ph2, s2 = 0.6, -0.35, 2
    g0 = (1 - ph2) * s2 / ((1 + ph2) * ((1 - ph2) ** 2 - ph1 ** 2))
    R.cerca(g0, M["s1"]["gamma0"], 6e-5, "s1 gamma0")
    R.cerca(s2 * (1 + np.sum(psi([ph1, ph2], (), 3000) ** 2)), g0, 1e-9, "s1 gamma0 por los psi")
    R.cerca(s2 / (1 - ph1 ** 2), M["s1"]["gamma0_ar1"], 6e-5, "s1 distractor AR(1)")
    pi2 = -(0.5 + 0.4) * (-0.4)
    R.cerca(pi2, M["s2"]["pi"][1], 1e-9, "s2 pi2")
    pis = arma2ma(np.r_[1, 0.4], np.r_[1, -0.5], 3)[1:]   # pi(B) = phi(B)/theta(B)
    R.ok(np.allclose(pis, M["s2"]["pi"], atol=1e-9), f"s2 pi por la recursión {pis}")
    cf, ee = parsea_salida(M["s3"]["salida"])
    R.cerca(cf["ar3"] / ee["ar3"], M["s3"]["t_ar3"], 0.01, "s3 t de ar3")
    R.cerca(cf["ar2"] / ee["ar2"], M["s3"]["t_ar2"], 0.01, "s3 t de ar2")
    R.ok(M["s3"]["aicc_ar2"] < M["s3"]["aicc_ar3"], "s3: el AR(2) no gana")
    cf, _ = parsea_salida(M["s4"]["salida"])
    R.cerca(cf["intercept"], M["s4"]["media"], 6e-3, "s4 intercept")
    R.cerca(cf["intercept"] * (1 - cf["ar1"]), M["s4"]["c"], 6e-3, "s4 c")
    R.cerca(M["s4"]["pronostico_200"], M["s4"]["media"], 6e-3, "s4 el pronóstico vuelve a la media")
    R.cerca(-2 * M["s5"]["logL"] + 2 * math.log(100), M["s5"]["bic"], 6e-3, "s5 BIC")
    R.cerca(-2 * M["s5"]["logL"] + math.log(100), M["s5"]["bic_k1"], 6e-3, "s5 distractor k = 1")
    ps = psi([1.4, -0.4], (), 2)
    R.ok(np.allclose(np.r_[1, ps], M["s6"]["psi"], atol=1e-9), "s6 psi")
    R.cerca(1.96 * 2 * math.sqrt(1 + ps[0] ** 2 + ps[1] ** 2), M["s6"]["semiancho"], 6e-5, "s6 semiancho")
    R.cerca(1.96 * 2 * math.sqrt(1 + 0.16 + 0.0256), M["s6"]["semiancho_ar1"], 6e-5, "s6 distractor AR(1)")


# ---------------------------------------------------------------------------
# §4 Procedencia
# ---------------------------------------------------------------------------
NUMERO = re.compile(r"(?<![\w.^_{])-?\d+(?:\\,\d{3})*(?:\.\d+)?")


def numeros(texto):
    """Cifras que se vigilan: decimales y enteros de dos o más dígitos. Los
    enteros de un dígito (órdenes, rezagos, subíndices) no se vigilan, como en
    el verificador del Corte I."""
    t = re.sub(r"ARIMA\(\d,\d,\d\)|ARMA\(\d,\d\)|AR\(\d\)|MA\(\d\)|AR\(\\infty\)|MA\(\\infty\)", " ", texto)
    t = re.sub(r"[_^]\{[^}]*\}|[_^]\d", " ", t)
    out = []
    for m in NUMERO.finditer(t):
        s = m.group(0).replace("\\,", "")
        if "." in s or len(s.lstrip("-")) >= 2:
            out.append(s)
    return out


def hojas(x, pref=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from hojas(v, f"{pref}.{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from hojas(v, f"{pref}[{i}]")
    elif isinstance(x, (int, float)) and not isinstance(x, bool):
        yield pref, float(x)


def representaciones(v):
    out = set()
    for k in range(0, 7):
        r = round(v, k)
        for x in (r, -r):
            s = f"{x:.{k}f}"
            out.add(s)
    return out


# Cifras que no son hojas del JSON de su ítem: cuentas intermedias que la prosa
# muestra y que aquí se REHACEN (no se copian), y constantes del material.
GLOBALES = [1.96, 1.282, 1.2816, 2.576, 0.05, 0.5, 20, 24, 60, 95, 80, 99] + \
    [float(m) for m in MODULOS]


def derivadas(D):
    I, M = D["items"], D["simulacro"]
    filas = I["i24"]["d1"]
    sanos = [f for f in filas if min(f["raiz_ar"] or 9, f["raiz_ma"] or 9) >= 1.01]
    mixto = next(f for f in sanos if f["p"] > 0 and f["q"] > 0)
    i17, i27, i21 = I["i17"], I["i27"], I["i21"]["ar2"]
    return {
        "i05": [1 / 0.45],
        "i09": [1 / 0.3],
        "i26": [0.4, 0.9],
        "i32": [1.96 * 50, 0.36],
        "i02": [0.8, 2.4, 1.6, 0.6, 1 / 1.6, -1.0, 1.0],
        "i03": [-0.65, 0.25, 0.09, math.cos(math.pi / 4)],
        "i06": [0.64, 0.36, 0.09, 1.0 - 0.36],
        "i11": [I["i11"]["r1"] ** 2, 1 - I["i11"]["r1"] ** 2],
        "i12": [100, 102, 99, 98, 97, 96, 10200, banda(100)],
        "i17": [1 - i17["alfa"], abs(i17["yT"] - i17["yhat_T"]), abs(i17["alfa"] * (i17["yT"] - i17["yhat_T"]))],
        "i19": [59, I["i19"]["yn"] - I["i19"]["y1"]],
        "i25": [-2 * I["i25"]["logL"], 8, 40, 114, 40 / 114],
        "i27": [i27["yT"] - i27["yT_1"], i27["paso1"] - i27["yT"],
                i27["yT"] + (i27["yT"] - i27["yT_1"]) * i27["phi"] / (1 - i27["phi"])],
        "i28": [math.sqrt(I["i28"]["suma_psi2"])],
        "i13": [I["i13"]["css"]["phi"] - I["i13"]["yw"]["phi"]],
        "i21": [i21["coef"][0] - 1, i21["raices"][0] - 1, 1.01],
        "i24": [1.01, 10, 20, sanos[0]["AICc"] - filas[0]["AICc"], mixto["AICc"] - sanos[0]["AICc"],
                sanos[1]["AICc"] - sanos[0]["AICc"], sanos[2]["AICc"] - sanos[0]["AICc"]],
        "i30": [100 * x for x in I["i30"]["fuera"].values()] + [10],
        "i07": [abs(I["i07"]["aicc"]["arma11"] - I["i07"]["aicc"]["ar3"])],
        "i08": [round(I["i08"]["acf"][0], 2) ** 2, round(I["i08"]["acf"][0], 2) ** 3, 19, 18],   # «del rezago 2 al 18»
        "i16": [11],
        "i14": [12],                                   # Ljung–Box(12)
        "i20": [len(D["series"]["matriculas"]["valores"])],   # «100 años»
        "i31": [],
        "s1": [1.35, 0.65, 1.4625, 2.7, 0.9506, 0.6],
        "s2": [0.9, 0.45],
        "s3": [120],
        "s4": [150],
        "s5": [-2 * M["s5"]["logL"], math.log(100)],
        "s6": [1.4, 1.56, 2.4336, 2 * math.sqrt(5.3936), 1 / 0.6, 0.4],
    }


def seccion4(R, E, D, lista):
    R.abre("§4 · La procedencia de cada número impreso en la prosa")
    base = set()
    for x in GLOBALES:
        base |= representaciones(float(x))
    deriv = derivadas(D)
    revisadas = 0
    for etiqueta, clave, p in lista:
        propio = D["simulacro"][clave] if clave.startswith("s") else D["items"][clave]
        permitidos = set(base)
        for _, x in hojas(propio):
            permitidos |= representaciones(x)
        for x in deriv.get(clave, []):
            permitidos |= representaciones(float(x))
        partes = [p.get("pregunta", ""), p.get("pista", ""), p.get("retroAcierto", ""), p.get("retroFallo", "")]
        for o in p.get("opciones", []) or []:
            partes += [o.get("texto", ""), o.get("retro", "")]
        # Las salidas de R se publican tal cual: sus cifras se comprueban en §3.
        texto = limpia(re.sub(r"<pre[^>]*>.*?</pre>", " ", " \n ".join(partes), flags=re.S))
        cifras = numeros(texto)
        revisadas += len(cifras)
        malos = sorted({n for n in cifras if n not in permitidos})
        R.ok(not malos, f"{etiqueta} ({clave}): cifras impresas sin procedencia {malos}")
    if not R.silencioso:
        print(f"  {revisadas} cifras impresas revisadas en {len(lista)} ítems")


# ---------------------------------------------------------------------------
# §5 Claves numéricas
# ---------------------------------------------------------------------------
def seccion5(R, lista):
    R.abre("§5 · Las claves numéricas: decimales pedidos y errores que la tolerancia debe dejar fuera")
    for etiqueta, clave, p in lista:
        if p.get("tipo") != "numerica":
            continue
        resp, tol = float(p["respuesta"]), float(p["tolerancia"])
        m = re.search(r"Da (un|dos|tres|cuatro) decimal", p["pregunta"])
        R.ok(m is not None, f"{etiqueta}: no dice cuántos decimales dar")
        if m:
            k = {"un": 1, "dos": 2, "tres": 3, "cuatro": 4}[m.group(1)]
            exacta = abs(round(resp, k) - resp) < 1e-12
            R.ok(exacta or tol >= 0.5 * 10 ** -k,
                 f"{etiqueta}: pide {k} decimales y la tolerancia {tol} no cubre el redondeo")
            R.ok(tol <= 6 * 10 ** -k + 1e-12, f"{etiqueta}: tolerancia {tol} demasiado ancha para {k} decimales")
        # Cada error con nombre de la retro de fallo tiene que quedar fuera.
        for s in re.findall(r"te sali[óo] \$(-?[\d.]+)\$", p.get("retroFallo", "")):
            x = float(s)
            R.ok(abs(x - resp) > tol, f"{etiqueta}: el error {x} cae dentro de la tolerancia de {resp}")
        R.ok(not p.get("retroFallo", "").lstrip().startswith(("Es ", "La respuesta")),
             f"{etiqueta}: la retro de fallo repite la cifra que el motor ya anuncia")


# ---------------------------------------------------------------------------
# §6 Tabla de especificaciones
# ---------------------------------------------------------------------------
def seccion6(R, E, html_txt, lista):
    R.abre("§6 · La tabla de especificaciones y los 20 módulos")
    diag = [x for x in lista if not x[0].startswith("simulacro")]
    R.ok(len(diag) == 32, f"{len(diag)} ítems de diagnóstico, no 32")
    cuenta = {o: 0 for o in PESOS}
    tocados = set()
    for etiqueta, clave, p in diag:
        cuenta[p["objetivo"]] += 1
        for k in (p.get("clave"), p.get("claveExtra")):
            if k:
                tocados.add(k)
        R.ok(OBJETIVO_DE.get(p["clave"]) == p["objetivo"],
             f"{etiqueta}: clave {p['clave']} es de {OBJETIVO_DE.get(p['clave'])} y declara {p['objetivo']}")
    R.ok(cuenta == {"O1": 5, "O2": 5, "O3": 6, "O4": 5, "O5": 5, "O6": 6}, f"reparto por objetivo {cuenta}")
    desv = max(abs(100 * cuenta[o] / 32 - PESOS[o]) for o in PESOS)
    R.ok(desv <= 2, f"desviación máxima entre peso e ítems {desv:.2f} > 2 puntos")
    R.ok(set(MODULOS) <= tocados, f"módulos sin ítem: {sorted(set(MODULOS) - tocados)}")
    R.ok({o: v["peso"] for o, v in E["objetivos"].items()} == PESOS, "OBJETIVOS no lleva los pesos aprobados")
    R.ok([m["clave"] for m in E["modulos"]] == MODULOS, "MODULOS_DEL_CORTE no son los 20 módulos en orden")
    for m in E["modulos"]:
        R.ok(OBJETIVO_DE[m["clave"]] == m["objetivo"], f"el módulo {m['clave']} declara {m['objetivo']}")
    # La tabla publicada en el módulo 1
    filas = re.findall(r"<td><strong>(O\d)</strong>.*?<td style=\"text-align:center;\"><strong>(\d+) %</strong></td>",
                       html_txt, re.S)
    R.ok({o: int(p) for o, p in filas} == PESOS, f"la tabla del módulo 1 dice {filas}")
    R.ok(sum(PESOS.values()) == 100, "los pesos no suman 100")
    # La misma tabla vive en el Módulo 12 del capítulo 4: dos copias que no pueden divergir.
    cap4 = (RAIZ / "Htmls_Series" / "capitulo-4-modelos-arima.html").read_text(encoding="utf-8")
    m12 = cap4[cap4.find('<template id="module-12">'):]
    m12 = m12[:m12.find("</template>")]
    filas12 = re.findall(r"<td><strong>(O\d)</strong>.*?<td style=\"text-align:center;\"><strong>(\d+) %</strong></td>",
                         m12, re.S)
    R.ok({o: int(p) for o, p in filas12} == PESOS, f"la tabla del Módulo 12 del capítulo 4 dice {filas12}")
    R.ok(m12.count('href="preparcial-corte-2.html"') == 1, "el Módulo 12 no enlaza el preparcial")
    portada = (RAIZ / "Htmls_Series" / "index.html").read_text(encoding="utf-8")
    R.ok(portada.count('href="preparcial-corte-2.html"') == 2, "la portada no enlaza el preparcial dos veces (héroe y tarjeta)")
    sim = [x for x in lista if x[0].startswith("simulacro")]
    R.ok(sorted(p["objetivo"] for _, _, p in sim) == list(PESOS), "el simulacro no lleva uno por objetivo")
    for etiqueta, clave, p in sim:
        R.ok(OBJETIVO_DE.get(p["clave"]) == p["objetivo"], f"{etiqueta}: clave y objetivo no casan")


# ---------------------------------------------------------------------------
# §7 Posición de la correcta
# ---------------------------------------------------------------------------
def seccion7(R, lista):
    R.abre("§7 · La posición de la opción correcta")
    pos = []
    for etiqueta, clave, p in lista:
        ops = p.get("opciones") or []
        if not ops:
            continue
        correctas = [j for j, o in enumerate(ops) if o.get("correcta")]
        if p.get("tipo") == "multiple":
            R.ok(2 <= len(correctas) <= 3, f"{etiqueta}: {len(correctas)} correctas en una de varias respuestas")
            R.ok(all(b - a > 1 for a, b in zip(correctas, correctas[1:])),
                 f"{etiqueta}: correctas en posiciones seguidas {correctas}")
            continue
        R.ok(len(correctas) == 1, f"{etiqueta}: {len(correctas)} correctas")
        if correctas:
            pos.append(correctas[0])
    n = len(pos)
    for j in range(4):
        R.ok(pos.count(j) / n <= 0.40, f"la posición {'abcd'[j]} tiene {pos.count(j)} de {n}")
    racha = max(len(list(g)) for _, g in __import__("itertools").groupby(pos))
    R.ok(racha <= 2, f"racha de {racha} en la misma posición: {''.join('abcd'[j] for j in pos)}")
    # La correcta no puede ser sistemáticamente la más larga.
    mas_larga = 0
    total = 0
    for etiqueta, clave, p in lista:
        ops = p.get("opciones") or []
        if not ops or p.get("tipo") == "multiple":
            continue
        largos = [len(limpia(o["texto"])) for o in ops]
        total += 1
        if largos.index(max(largos)) == next(j for j, o in enumerate(ops) if o.get("correcta")):
            mas_larga += 1
    R.ok(mas_larga / total <= 0.40, f"la correcta es la opción más larga en {mas_larga} de {total} ítems")
    if not R.silencioso:
        print(f"  posiciones: {''.join('abcd'[j] for j in pos)} · la correcta es la más larga en {mas_larga} de {total}")


# ---------------------------------------------------------------------------
# §8 Casi-duplicados
# ---------------------------------------------------------------------------
def normaliza(s):
    # Las fórmulas se quitan: dos enunciados que escriben el mismo modelo con la
    # misma notación no son el mismo enunciado, y sus tokens inflaban la tirada.
    s = re.sub(r"\$\$.*?\$\$|\$[^$]*\$", " formula ", limpia(s), flags=re.S).lower()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def previos():
    """Enunciados que el estudiante ya vio sobre los caps. 3 y 4, leídos del sitio."""
    out = []
    def js_strings(texto, clave):
        for m in re.finditer(clave + r"\s*:\s*(['`])((?:\\.|(?!\1).)*)\1", texto, re.S):
            yield m.group(2).replace("\\'", "'").replace("\\\\", "\\")
    sitio = RAIZ / "Htmls_Series"
    for nombre in ["capitulo-3-modelos-ar-ma-arma.html", "capitulo-4-modelos-arima.html",
                   "preparcial-corte-1.html"]:
        t = (sitio / nombre).read_text(encoding="utf-8")
        for s in js_strings(t, "pregunta"):
            out.append((nombre.split("-")[0] + nombre.split("-")[1] + " pregunta", s))
        for s in js_strings(t, "enunciado"):
            out.append((nombre.split("-")[0] + nombre.split("-")[1] + " simulacro", s))
        for m in re.finditer(r'<div class="ejercicio-guiado">(.*?)<div class="ejercicio-', t, re.S):
            out.append((nombre.split("-")[1] + " ejercicio", m.group(1)[:1500]))
    t = (sitio / "taller-2-modulo-2.html").read_text(encoding="utf-8")
    for m in re.finditer(r"<li[^>]*>(.*?)</li>", t, re.S):
        s = limpia(m.group(1))
        if len(s.split()) >= 8:
            out.append(("taller 2", s))
    return out


def trigramas(p):
    w = p.split()
    return {" ".join(w[i:i + 3]) for i in range(len(w) - 2)}


def tirada(a, b):
    a, b = a.split(), b.split()
    mejor = 0
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                mejor = max(mejor, cur[j])
        prev = cur
    return mejor


def seccion8(R, lista, extra_previos=()):
    R.abre("§8 · Casi-duplicados contra lo que el estudiante ya vio")
    P = [(f, normaliza(s)) for f, s in list(previos()) + list(extra_previos)]
    P = [(f, s) for f, s in P if len(s.split()) >= 6]
    R.ok(len(P) > 100, f"solo {len(P)} enunciados previos: el corpus no se leyó bien")
    peores = []
    for etiqueta, clave, p in lista:
        s = normaliza(re.sub(r"<pre[^>]*>.*?</pre>", " ", p["pregunta"], flags=re.S))
        T = trigramas(s)
        jac, tir, fuente = 0, 0, ""
        for f, q in P:
            U = trigramas(q)
            j = len(T & U) / max(1, len(T | U))
            t = tirada(s, q)
            if j > jac or t > tir:
                jac, tir, fuente = max(jac, j), max(tir, t), f
        peores.append((jac, tir, etiqueta, fuente))
        R.ok(jac < 0.25 and tir < 8, f"{etiqueta}: Jaccard {jac:.3f}, tirada {tir} contra {fuente}")
    if not R.silencioso:
        for jac, tir, etiqueta, fuente in sorted(peores, reverse=True)[:5]:
            print(f"  más cercano: {etiqueta} · Jaccard {jac:.3f} · tirada {tir} · {fuente}")


# ---------------------------------------------------------------------------
# Ejecución
# ---------------------------------------------------------------------------
def verifica(ruta, silencioso=False, extra_previos=()):
    R = Registro(silencioso)
    html_txt = ruta.read_text(encoding="utf-8")
    E = extrae(ruta)
    D = seccion1(R, E, html_txt)
    D = E["datos"]
    seccion2(R, D)
    seccion3(R, D)
    lista = todos_los_items(E)
    seccion4(R, E, D, lista)
    seccion5(R, lista)
    seccion6(R, E, html_txt, lista)
    seccion7(R, lista)
    seccion8(R, lista, extra_previos)
    return R


def inyecta():
    print("\n§9 · La prueba del propio verificador: cada siembra tiene que cazarse en su sección")
    base = HTML.read_text(encoding="utf-8")
    siembras = [
        ("§1", "una cifra del JSON incrustado", lambda t: t.replace('"rho1":-0.4851', '"rho1":-0.4815', 1)),
        ("§4", "una cifra inventada en la prosa",
         lambda t: t.replace("denominador $1 + 0.25 + 0.09 = ", "denominador $1 + 0.25 + 0.09 = 1.43 \\\\approx ", 1)),
        ("§5", "una tolerancia ensanchada",
         lambda t: t.replace("respuesta: Number(fx(D.i12.Q, 2)), tolerancia: 0.02",
                             "respuesta: Number(fx(D.i12.Q, 2)), tolerancia: 0.5", 1)),
        ("§6", "un peso descuadrado", lambda t: t.replace("O3: { titulo: 'Estimar, comparar y diagnosticar un ARMA', peso: 20 }",
                                                         "O3: { titulo: 'Estimar, comparar y diagnosticar un ARMA', peso: 25 }", 1)),
        ("§7", "una correcta movida a la primera posición",
         lambda t: t.replace("{ texto: `(i) subir $d$; (ii) bajar $d$; (iii) subir $p$ y $q$.`, correcta: false",
                             "{ texto: `(i) subir $d$; (ii) bajar $d$; (iii) subir $p$ y $q$.`, correcta: true", 1)),
    ]
    cazadas = 0
    for seccion, que, cambio in siembras:
        t = cambio(base)
        if t == base:
            print(f"  NO SE PUDO SEMBRAR: {que}")
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(t)
        R = verifica(pathlib.Path(f.name), silencioso=True)
        ok = any(s == seccion for s, _ in R.fallos)
        cazadas += ok
        print(f"  {'CAZADA' if ok else 'NO CAZADA'}  {seccion} · {que}")
    # §8: un enunciado previo pegado tal cual dentro de un ítem
    R = verifica(HTML, silencioso=True, extra_previos=[("siembra", "Un compañero propone para una serie el ARMA(2,1) "
                                                         "y es decir qué modelo es en realidad cuando factoriza")])
    ok = any(s == "§8" for s, _ in R.fallos)
    cazadas += ok
    print(f"  {'CAZADA' if ok else 'NO CAZADA'}  §8 · un enunciado previo casi idéntico")
    return cazadas, len(siembras) + 1


if __name__ == "__main__":
    R = verifica(HTML)
    print(f"\n{R.n} comprobaciones · {len(R.fallos)} fallos · por sección: "
          + ", ".join(f"{k} {v}" for k, v in R.por_seccion.items()))
    codigo = 1 if R.fallos else 0
    if "--inyecta" in sys.argv:
        c, t = inyecta()
        print(f"  {c} de {t} siembras cazadas")
        codigo = codigo or (0 if c == t else 1)
    sys.exit(codigo)
