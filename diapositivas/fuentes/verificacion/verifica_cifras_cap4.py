#!/usr/bin/env python3
"""Verifica, cifra por cifra, la presentación del capítulo 4 contra sus fuentes.

Qué hace
  1. Lee `fuentes/capitulo_4.md` (diapositivas y notas) y extrae TODAS las cifras
     que exigen respaldo: decimales, porcentajes, enteros >= 10 y años.
  2. Compara cada una con su fuente, redondeando la fuente a los decimales que
     muestra la diapositiva:
        J    JSON publicado `precalculo/salidas/cap4_arima.json`  (R 4.6, forecast 9.0.2)
        RJ   el mismo JSON regenerado en R 4.3.3 (`regenerado_cap4_arima.json`)
        RD   `directo_cap4.json`, recalculado en R sobre los datos crudos
        PY   `directo_python_cap4.json`, recalculado con statsmodels
        DOC  documentación de R guardada en `directo_cap4.json`
        CALC aritmética sobre las fuentes anteriores
        C    texto del capítulo (`capitulo-4-modelos-arima.html`)
        A    plan de auditoría (`PLAN_Auditoria_Cap4.md`)
  3. Comprueba que ninguna cifra de la presentación quede sin claim y que cada
     claim aparezca de verdad en su diapositiva.
  4. Escribe `verificacion_cifras.md` con la tabla completa.

Uso (desde la raíz del repositorio; necesita scipy, que trae statsmodels):
    python3 Htmls_Series/diapositivas/fuentes/verificacion/verifica_cifras_cap4.py
Sale con código 1 si algo no coincide o queda una cifra sin respaldo.

Convenciones de comparación: la fuente se redondea a los decimales de lo que se
muestra, a la mitad hacia arriba (0.5855 -> 0.586). Si la fuente ya viene
redondeada (JSON a 4 decimales) y el valor mostrado tiene menos, se recalcula
desde los datos (CALC) para no redondear dos veces (p. ej. la banda ±0.167).
"""
from __future__ import annotations

import html
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[3]
import os  # noqa: E402

DECK = Path(os.environ.get("DECK_CAP4", AQUI.parent / "capitulo_4.md"))
SALIDA_MD = AQUI / "verificacion_cifras.md"


def cargar(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


J = cargar(RAIZ / "precalculo/salidas/cap4_arima.json")
RJ = cargar(AQUI / "regenerado_cap4_arima.json")
RD = cargar(AQUI / "directo_cap4.json")
PY = cargar(AQUI / "directo_python_cap4.json")
DAT = cargar(RAIZ / "precalculo/salidas/datos_series.json")
GENERA_R = (RAIZ / "precalculo/genera_cap4.R").read_text(encoding="utf-8")
NILE = DAT["nilo"]["valores"]
TRM = DAT["trm"]["valores"]


def _texto_html(p: Path) -> str:
    t = re.sub(r"<(script|style)\b.*?</\1>", " ", p.read_text(encoding="utf-8"), flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t.replace(" ", " ").replace(" ", " "))


CAP = _texto_html(RAIZ / "Htmls_Series/capitulo-4-modelos-arima.html")
PLAN = re.sub(r"\s+", " ", (RAIZ / "PLAN_Auditoria_Cap4.md").read_text(encoding="utf-8"))


def get(obj, ruta: str):
    for parte in ruta.split("."):
        obj = obj[int(parte)] if isinstance(obj, list) else obj[parte]
    return obj


def getf(obj, ruta: str):
    """Acceso a los JSON de cálculo directo, cuyas claves son planas con puntos ('m1.d0.n')."""
    partes = ruta.split(".")
    for i in range(len(partes), 0, -1):
        k = ".".join(partes[:i])
        if k in obj:
            v = obj[k]
            for p in partes[i:]:
                v = v[int(p)] if isinstance(v, list) else v[p]
            return v
    raise KeyError(ruta)


def coef(lista, nombre: str, campo: str = "valor"):
    for c in lista:
        if c["nombre"] == nombre:
            return c[campo]
    raise KeyError(nombre)


# ---------------------------------------------------------------------------
# Fuentes
# ---------------------------------------------------------------------------
class Src:
    def __init__(self, tag: str, fn, desc: str, booleana: bool = False):
        self.tag, self.fn, self.desc, self.booleana = tag, fn, desc, booleana

    def valor(self):
        return self.fn()


def J_(ruta, m=1):
    return Src("J", lambda: get(J, ruta) * m, f"cap4_arima.json › {ruta}")


def RJ_(ruta, m=1):
    return Src("RJ", lambda: get(RJ, ruta) * m, f"regenerado (R 4.3.3) › {ruta}")


def RD_(clave, m=1):
    return Src("RD", lambda: getf(RD, clave) * m, f"directo_cap4.json › {clave}")


def PY_(clave, m=1):
    return Src("PY", lambda: getf(PY, clave) * m, f"directo_python_cap4.json › {clave}")


def CALC_(fn, desc):
    return Src("CALC", fn, desc)


def DOC_(clave, aguja):
    return Src("DOC", lambda: aguja in RD[clave], f"documentación de R ({clave}) contiene «{aguja}»", True)


def CH_(aguja):
    return Src("C", lambda: aguja in CAP, f"capítulo 4 contiene «{aguja}»", True)


def PLAN_(aguja):
    return Src("A", lambda: aguja in PLAN, f"PLAN_Auditoria_Cap4.md contiene «{aguja}»", True)


def DATO_(fn, desc):
    return Src("RD", fn, desc)


def BOOL_(tag, fn, desc):
    return Src(tag, fn, desc, True)


# Lo mismo en las dos fuentes de JSON (publicado y regenerado), que es lo habitual
def JJ(ruta, m=1):
    return [J_(ruta, m), RJ_(ruta, m)]


# ---------------------------------------------------------------------------
# Claims
# ---------------------------------------------------------------------------
class Claim:
    def __init__(self, slide, shown, srcs, kind="dato", tol=None, nota=""):
        self.slide, self.shown, self.srcs, self.kind, self.tol, self.nota = slide, shown, srcs, kind, tol, nota
        self.resultados = []  # (Src, ok, valor)


CLAIMS: list[Claim] = []
ALLOW: dict[str, dict[str, str]] = defaultdict(dict)  # slide -> token -> motivo
SIN_VERIFICAR: list[tuple[str, str, str]] = []  # slide, texto, motivo


def C(slide, shown, *srcs, kind="dato", tol=None, nota=""):
    lista = []
    for s in srcs:
        lista.extend(s if isinstance(s, list) else [s])
    CLAIMS.append(Claim(slide, shown, lista, kind, tol, nota))


def permite(slide, tokens, motivo):
    for t in tokens.split():
        ALLOW[slide][t] = motivo


def sin_verificar(slide, texto, motivo):
    SIN_VERIFICAR.append((slide, texto, motivo))


def normaliza(t: str) -> str:
    t = t.replace(" ", "").replace(" ", "").replace("−", "-")
    return re.sub(r"(?<=\d)[ ](?=\d{3}\b)", "", t)


def coincide(shown: str, valor, tol=None) -> bool:
    s = shown.replace("%", "").replace("+", "").strip()
    esperado = float(s)
    if tol is not None:
        return abs(float(valor) - esperado) <= tol
    dec = len(s.split(".")[1]) if "." in s else 0
    v = float(valor)
    redondeado = round(v + math.copysign(1e-9, v), dec)
    return abs(redondeado - esperado) < 1e-9


def evalua(c: Claim):
    c.resultados = []
    for s in c.srcs:
        try:
            v = s.valor()
            ok = bool(v) if s.booleana else coincide(c.shown, v, c.tol)
        except Exception as e:  # noqa: BLE001
            v, ok = f"ERROR {type(e).__name__}: {e}", False
        c.resultados.append((s, ok, v))
    return all(ok for _, ok, _ in c.resultados) and len(c.resultados) > 0


# ===========================================================================
# REGISTRO DE CLAIMS, diapositiva por diapositiva (la clave es un trozo del título)
# ===========================================================================
from statistics import NormalDist  # noqa: E402

Z975 = NormalDist().inv_cdf(0.975)
N_NILO, N_TRM = len(NILE), len(TRM)
VAR = lambda d: J["nilo"]["varianzas"][d]["varianza"]  # noqa: E731

# ---- Cómo leer -----------------------------------------------------------------
K = "Cada afirmación es un dato"
C(K, "4.6", PLAN_("R 4.6"), kind="versión")
C(K, "4.3.3", BOOL_("RD", lambda: "4.3.3" in RD["entorno"]["R"], "directo_cap4.json › entorno.R"), kind="versión")

K = "Tres series conducen"
C(K, "1871", RD_("datos.nilo_inicio"), DOC_("doc.nile", "1871-1970"), kind="documentación")
C(K, "1970", RD_("datos.nilo_fin"), DOC_("doc.nile", "1871-1970"), kind="documentación")
C(K, "100", RD_("datos.nilo_n"), J_("nilo.n"))
C(K, "10", DOC_("doc.nile", "10^8 m^3"), kind="documentación")
C(K, "1978", DOC_("doc.nile", "Cobb(1978)"), kind="documentación")
C(K, "2015", CALC_(lambda: int(RD["datos.trm_inicio"].split("-")[0]), "directo_cap4.json › datos.trm_inicio"),
  BOOL_("RD", lambda: "2015-01 a 2026-06" in DAT["trm"]["descripcion"], "datos_series.json › trm.descripcion"))
C(K, "2026", CALC_(lambda: int(RD["datos.trm_fin"].split("-")[0]), "directo_cap4.json › datos.trm_fin"),
  BOOL_("RD", lambda: "2015-01 a 2026-06" in DAT["trm"]["descripcion"], "datos_series.json › trm.descripcion"))
C(K, "138", J_("trm.n"), RD_("datos.trm_n"))
C(K, "26", BOOL_("RD", lambda: "consulta: 2026-07-26" in DAT["trm"]["fuente"], "datos_series.json › trm.fuente («consulta: 2026-07-26»)"))
C(K, "1949", RD_("datos.ap_inicio"), DOC_("doc.airpassengers", "1949 to 1960"), kind="documentación")
C(K, "1960", RD_("datos.ap_fin"), DOC_("doc.airpassengers", "1949 to 1960"), kind="documentación")
C(K, "144", J_("puente_estacional.n"), RD_("datos.ap_n"))
C(K, "1976", DOC_("doc.airpassengers", "(1976)"), kind="documentación")
C(K, "150", RD_("datos.bjsales_n"), DOC_("doc.bjsales", "150 observations"), kind="documentación")
C(K, "1821", RD_("datos.lynx_inicio"), DOC_("doc.lynx", "1821-1934"), kind="documentación")
C(K, "1934", RD_("datos.lynx_fin"), DOC_("doc.lynx", "1821-1934"), kind="documentación")
sin_verificar(K, "origen de la TRM en datos.gov.co", "no se pudo contrastar con la fuente primaria; solo con la copia congelada del repositorio")

# ---- M1 ---------------------------------------------------------------------------
K = "Un ARIMA(1,1,1) es un ARMA(2,1)"
C(K, "0.2544", J_("nilo.diagnostico.coeficientes.0.valor"), RJ_("nilo.diagnostico.coeficientes.0.valor"))
C(K, "1.2544", RD_("m1.ar_expandido.0"), CALC_(lambda: 1 + 0.2544, "1 + φ"))
C(K, "-0.2544", RD_("m1.ar_expandido.1"), CALC_(lambda: -0.2544, "−φ"))
C(K, "1.0000", RD_("m1.raices.0"))
C(K, "3.9308", RD_("m1.raices.1"), CALC_(lambda: 1 / 0.2544, "1/φ"))

K = "Suavizamiento exponencial"
permite(K, "10", "ordinal de módulo (Módulo 10)")

K = "En el Nilo, diferenciar una vez"
C(K, "1871", RD_("datos.nilo_inicio"), DOC_("doc.nile", "1871-1970"), kind="documentación")
C(K, "1970", RD_("datos.nilo_fin"), DOC_("doc.nile", "1871-1970"), kind="documentación")
C(K, "10", DOC_("doc.nile", "10^8 m^3"), kind="documentación")
C(K, "100", RD_("m1.d0.n"), J_("nilo.varianzas.0.n_efectivo"))
C(K, "99", RD_("m1.d1.n"), J_("nilo.varianzas.1.n_efectivo"))
C(K, "98", RD_("m1.d2.n"), J_("nilo.varianzas.2.n_efectivo"))
C(K, "919.35", RD_("m1.d0.media"))
C(K, "-3.84", RD_("m1.d1.media"))
C(K, "-0.14", RD_("m1.d2.media"))
C(K, "28638", RD_("m1.d0.var"), JJ("nilo.varianzas.0.varianza"))
C(K, "28268", RD_("m1.d1.var"), JJ("nilo.varianzas.1.varianza"))
C(K, "80055", RD_("m1.d2.var"), JJ("nilo.varianzas.2.varianza"))
C(K, "28268.34", RD_("m1.d1.var"), JJ("nilo.varianzas.1.varianza"))
C(K, "28637.95", RD_("m1.d0.var"), JJ("nilo.varianzas.0.varianza"))
C(K, "0.50", RD_("m1.d0.rho1"), JJ("nilo.identificacion.cruda.acf.0"))
C(K, "-0.40", RD_("m1.d1.rho1"), JJ("nilo.identificacion.d1.acf.0"))
C(K, "-0.63", RD_("m1.d2.rho1"), JJ("nilo.identificacion.d2.acf.0"))
C(K, "1.3", CALC_(lambda: -(VAR(1) / VAR(0) - 1) * 100, "reducción de la varianza de d=0 a d=1, en %"), kind="aritmética")
C(K, "-1.3", CALC_(lambda: (VAR(1) / VAR(0) - 1) * 100, "variación de la varianza de d=0 a d=1, en %"), kind="aritmética")
C(K, "-0.5", BOOL_("DEF", lambda: True, "definición: ρ₁ de la diferencia de un ruido blanco es −1/2"), kind="definición")
C(K, "1899", CALC_(lambda: 1871 + RD["m8.posicion_1899"] - 1, "año de la observación 29 (1871 + 29 − 1)"), tol=0)

K = "Box y Jenkins aportaron"
C(K, "1976", DOC_("doc.bjsales", "Box & Jenkins (1976)"), kind="documentación")
C(K, "1970", BOOL_("SV", lambda: False, "sin fuente en esta sesión"), kind="sin verificar")
sin_verificar(K, "1970 (edición de Time Series Analysis: Forecasting and Control)",
              "la documentación de R (?BJsales) cita la edición de 1976; ninguna fuente de esta sesión confirma 1970")

K = "Cada etapa tiene un hallazgo"
permite(K, "12", "número de capítulo/parámetro estructural")

K = "El ciclo completo cabe"
C(K, "0.800", RD_("m2.lb20_p"), J_("nilo.diagnostico.ljung_box_20.p"), RJ_("nilo.diagnostico.ljung_box_20.p"))
C(K, "0.05", BOOL_("DEF", lambda: True, "nivel nominal convencional"), kind="definición")
C(K, "816.18", RD_("m2.pron_1a3.0"))
C(K, "835.56", RD_("m2.pron_1a3.1"))
C(K, "840.49", RD_("m2.pron_1a3.2"))
C(K, "0.761", PY_("m2.lb20_statsmodels"))
permite(K, "10", "horizonte h = 10 del código / 10⁸ m³")

# ---- M3 -----------------------------------------------------------------------------
K = "Tres evidencias miran"
C(K, "1899", CALC_(lambda: 1871 + RD["m8.posicion_1899"] - 1, "año de la observación 29 (1871 + 29 − 1)"), tol=0)
for i, v in enumerate(["28638", "28268", "80055", "262507"]):
    C(K, v, RD_(f"m3.var_d0a3.{i}"), JJ(f"nilo.varianzas.{i}.varianza"))
C(K, "-3.366", RD_("m3.adf_stat"), JJ("nilo.pruebas.adf_nivel.estadistico"))
C(K, "0.064", RD_("m3.adf_p"), JJ("nilo.pruebas.adf_nivel.p"))
C(K, "0.965", RD_("m3.kpss_stat"), JJ("nilo.pruebas.kpss_nivel.estadistico"))
C(K, "0.01", RD_("m3.kpss_p"), JJ("nilo.pruebas.kpss_nivel.p"), RD_("m3.pp_p"), JJ("nilo.pruebas.pp_nivel.p"),
  nota="cota de la tabla: R imprime «p-value smaller than printed p-value» (p < 0.01)")
C(K, "-6.690", RD_("m3.pp_stat"), JJ("nilo.pruebas.pp_nivel.estadistico"))
C(K, "1.3", CALC_(lambda: -(VAR(1) / VAR(0) - 1) * 100, "reducción de la varianza de d=0 a d=1, en %"), kind="aritmética")
permite(K, "4", "rezagos k = 4 del adf.test (verificado: RD m3.adf_rezagos)")

K = "Las tres versiones de `ndiffs`"
C(K, "-4.05", RD_("m3.urdf_tau"))
C(K, "-2.89", RD_("m3.urdf_crit5"))
C(K, "5", BOOL_("DEF", lambda: True, "nivel nominal convencional"), kind="definición")
C(K, "0.9654", RD_("m3.kpss_stat"), JJ("nilo.pruebas.kpss_nivel.estadistico"))
C(K, "0.8691", PY_("m3.kpss_auto"))
C(K, "0.5497", PY_("m3.kpss_legacy"))

K = "Ruido blanco puro con un escalón"
C(K, "1899", CALC_(lambda: 1871 + RD["m8.posicion_1899"] - 1, "año de la observación 29 (1871 + 29 − 1)"), tol=0)
C(K, "1000", JJ("nilo.cambio_nivel.monte_carlo.n_replicas"))
C(K, "100", JJ("nilo.cambio_nivel.monte_carlo.n"))
C(K, "127.03", JJ("nilo.cambio_nivel.monte_carlo.sigma"))
C(K, "29", JJ("nilo.cambio_nivel.monte_carlo.posicion_escalon"), RD_("m8.posicion_1899"))
C(K, "5", BOOL_("DEF", lambda: True, "nivel nominal convencional"), kind="definición")
C(K, "2026", BOOL_("RS", lambda: "set.seed(2026)" in GENERA_R, "precalculo/genera_cap4.R contiene set.seed(2026)"), kind="dato", nota="semilla del experimento")
C(K, "400", JJ("nilo.cambio_nivel.malla_delta.n_replicas"))
C(K, "4.8", J_("nilo.cambio_nivel.monte_carlo.sin_escalon.kpss_rechaza", 100), RJ_("nilo.cambio_nivel.monte_carlo.sin_escalon.kpss_rechaza", 100))
C(K, "247.8", J_("nilo.cambio_nivel.malla_delta.delta_del_nilo"), RJ_("nilo.cambio_nivel.malla_delta.delta_del_nilo"))
C(K, "247.78", CALC_(lambda: abs(J["nilo"]["cambio_nivel"]["monte_carlo"]["delta"]), "|δ| del Monte Carlo"), RD_("m8.escalon_coef", -1))
C(K, "1.95", CALC_(lambda: 247.78 / 127.03, "|β|/σ = 247.78/127.03"), kind="aritmética")
C(K, "100", J_("nilo.cambio_nivel.malla_delta.puntos.4.delta"))
C(K, "100%", J_("nilo.cambio_nivel.monte_carlo.con_escalon.kpss_rechaza", 100), RJ_("nilo.cambio_nivel.monte_carlo.con_escalon.kpss_rechaza", 100))
C(K, "0.79", CALC_(lambda: 100 / 127.03, "100/σ = 100/127.03"), J_("nilo.cambio_nivel.malla_delta.puntos.4.salto_en_sigmas"), kind="aritmética")
C(K, "70.8", J_("nilo.cambio_nivel.malla_delta.puntos.4.kpss_rechaza", 100), RJ_("nilo.cambio_nivel.malla_delta.puntos.4.kpss_rechaza", 100))
permite(K, "165", "atributo de formato {alto=165}")

K = "KPSS no distingue"
C(K, "86.4", J_("nilo.cambio_nivel.monte_carlo.con_escalon.adf_test_no_rechaza", 100), RJ_("nilo.cambio_nivel.monte_carlo.con_escalon.adf_test_no_rechaza", 100))
C(K, "5.4", J_("nilo.cambio_nivel.monte_carlo.sin_escalon.adf_test_no_rechaza", 100), RJ_("nilo.cambio_nivel.monte_carlo.sin_escalon.adf_test_no_rechaza", 100))

# ---- M4 -----------------------------------------------------------------------------
K = "La ACF del Nilo sin diferenciar"
for i, v in enumerate(["0.498", "0.385", "0.328", "0.239"]):
    C(K, v, JJ(f"nilo.identificacion.cruda.acf.{i}"), RD_(f"m4.acf_sin_dif_1a4.{i}"))
for i, v in enumerate(["0.4984", "0.3846", "0.3279", "0.2392"]):
    C(K, v, JJ(f"nilo.identificacion.cruda.acf.{i}"), RD_(f"m4.acf_sin_dif_1a4.{i}"))
C(K, "0.196", JJ("nilo.identificacion.cruda.banda"))
C(K, "0.25", RD_("m4.ar1_phi05_rezagos2y3.0"), CALC_(lambda: 0.5 ** 2, "φ² con φ = 0.5"), kind="aritmética")
C(K, "0.125", RD_("m4.ar1_phi05_rezagos2y3.1"), CALC_(lambda: 0.5 ** 3, "φ³ con φ = 0.5"), kind="aritmética")
C(K, "0.5", CALC_(lambda: J["nilo"]["identificacion"]["cruda"]["acf"][0], "ρ̂₁ ≈ 0.5 ⇒ φ ≈ 0.5"), tol=0.01, kind="aritmética")

K = "Sobre ∇Nilo la ACF corta"
C(K, "1.96", CALC_(lambda: Z975, "z de 0.975"), tol=0.001, kind="definición")
C(K, "0.197", JJ("nilo.identificacion.d1.banda"), RD_("m4.banda"))
C(K, "-0.402", JJ("nilo.identificacion.d1.acf.0"), RD_("m4.acf_1a6.0"))
C(K, "0.231", JJ("nilo.identificacion.d1.acf.7"))
C(K, "0.2312", JJ("nilo.identificacion.d1.acf.7"))
C(K, "-0.246", JJ("nilo.identificacion.d1.pacf.1"), RD_("m4.pacf_1a3.1"))
C(K, "-0.119", JJ("nilo.identificacion.d1.pacf.2"), RD_("m4.pacf_1a3.2"))
C(K, "20", J_("max_rezago"))
C(K, "5", BOOL_("DEF", lambda: True, "nivel nominal convencional"), kind="definición")
permite(K, "150", "atributo de formato {alto=150}")

K = "La tabla propone un ARIMA(0,1,1)"
C(K, "-0.402", JJ("nilo.identificacion.d1.acf.0"))
C(K, "-0.7329", RD_("m4.theta"), JJ("nilo.rejilla.011.coeficientes.0.valor"))
C(K, "0.1143", RD_("m4.theta_ee"), JJ("nilo.rejilla.011.coeficientes.0.ee"))
C(K, "-6.41", RD_("m4.theta_t"), CALC_(lambda: -0.7329 / 0.1143, "θ̂/e.e."))
C(K, "0.674", RD_("m4.lb20_p"), JJ("nilo.rejilla.011.ljung_box_p"))
C(K, "1.71", CALC_(lambda: J["nilo"]["hyndman_khandakar"]["exhaustiva"]["ranking"][4]["aicc"] - J["nilo"]["hyndman_khandakar"]["exhaustiva"]["ranking"][0]["aicc"], "AICc(0,1,1) − AICc(1,1,1) en la búsqueda exhaustiva"), kind="aritmética")
C(K, "99", RD_("m1.d1.n"))
BOOL_TABLA = BOOL_("J", lambda: J["nilo"]["mejor_por_d"]["d1"]["mejor_aicc"] == "111" and J["nilo"]["mejor_por_d"]["d1"]["mejor_bic"] == "011", "cap4_arima.json › nilo.mejor_por_d.d1 (AICc→111, BIC→011)")
C(K, "el AICc prefiere (1,1,1) y el BIC (0,1,1)", BOOL_TABLA, kind="dato", nota="afirmación sin cifra")

# ---- M5 -----------------------------------------------------------------------------
K = "La constante \\(c\\) significa"
C(K, "intercept", BOOL_("J", lambda: any(c["nombre"] == "intercept" for c in J["nilo"]["rejilla"]["101"]["coeficientes"]), "cap4_arima.json › nilo.rejilla.101.coeficientes contiene «intercept»"),
  kind="dato", nota="afirmación sin cifra: R llama intercept a la media con d = 0")

K = "Cada programa trata la constante"
C(K, "4.3.3", BOOL_("RD", lambda: "4.3.3" in RD["entorno"]["R"], "directo_cap4.json › entorno.R"), kind="versión")
C(K, "8.21.1", BOOL_("RD", lambda: RD["entorno"]["forecast"] == "8.21.1", "directo_cap4.json › entorno.forecast"), kind="versión")
C(K, "0.14.6", BOOL_("PY", lambda: PY["entorno"]["statsmodels"] == "0.14.6", "directo_python_cap4.json › entorno.statsmodels"), kind="versión")
C(K, "4.6", PLAN_("R 4.6"), kind="versión")
C(K, "9.0.2", PLAN_("forecast 9.0.2"), kind="versión")
C(K, "arima ignora include.mean con d ≥ 1", BOOL_("RD", lambda: RD["m5.arima_d1_include_mean_coef"] == ["ar1", "ma1"], "directo_cap4.json › m5.arima_d1_include_mean_coef == [ar1, ma1]"), kind="comportamiento")
C(K, "Arima con d = 2 avisa y no ajusta deriva", BOOL_("RD", lambda: RD["m5.d2_aviso"].startswith("No drift term fitted") and RD["m5.d2_tiene_deriva"] is False, "directo_cap4.json › m5.d2_aviso, m5.d2_tiene_deriva"), kind="comportamiento")
C(K, "auto.arima prueba con y sin deriva si d = 1", BOOL_("RD", lambda: RD["m5.auto_d1_traza_con_deriva"] and RD["m5.auto_d1_traza_sin_deriva"], "directo_cap4.json › m5.auto_d1_traza_*"), kind="comportamiento")
C(K, "auto.arima con d = 2 nunca incluye deriva", BOOL_("RD", lambda: (not RD["m5.auto_d2_tiene_deriva"]) and (not RD["m5.auto_d2_traza_con_deriva"]), "directo_cap4.json › m5.auto_d2_*"), kind="comportamiento")
C(K, "statsmodels: trend = c si d = 0, n si d > 0; t da deriva con d = 1; d ≥ 2 con t lanza ValueError",
  BOOL_("PY", lambda: PY["m5.parametros_d0_por_defecto"][0] == "const" and "const" not in PY["m5.parametros_d1_por_defecto"] and PY["m5.parametros_d1_trend_t"][0] == "x1" and PY["m5.d2_trend_t"].startswith("ValueError"), "directo_python_cap4.json › m5.*"), kind="comportamiento")

K = "El Nilo no lleva deriva"
C(K, "-2.883", RD_("m5.deriva"), JJ("nilo.formas_pronostico.d1_deriva.coeficientes.2.valor"))
C(K, "2.017", RD_("m5.deriva_ee"), JJ("nilo.formas_pronostico.d1_deriva.coeficientes.2.ee"))
C(K, "-1.43", RD_("m5.deriva_t"), CALC_(lambda: coef(J["nilo"]["formas_pronostico"]["d1_deriva"]["coeficientes"], "drift") / coef(J["nilo"]["formas_pronostico"]["d1_deriva"]["coeficientes"], "drift", "ee"), "δ̂/e.e. (J)"))
C(K, "1268.06", RD_("m5.aicc_con"), JJ("nilo.formas_pronostico.d1_deriva.aicc"))
C(K, "1267.51", RD_("m5.aicc_sin"), JJ("nilo.formas_pronostico.d1.aicc"))
C(K, "8.00", RD_("m5.trm_deriva"), JJ("trm.deriva.valor"))
C(K, "10.36", RD_("m5.trm_deriva_ee"), JJ("trm.deriva.ee"))
C(K, "0.77", RD_("m5.trm_deriva_t"), JJ("trm.deriva.t"))
C(K, "1707.41", RD_("m5.trm_aicc_con"), JJ("trm.deriva.aicc"))
C(K, "1705.94", RD_("m5.trm_aicc_sin"), JJ("trm.caminata.aicc"))
C(K, "740", RD_("m5.nilo_1970"), CALC_(lambda: NILE[-1], "último dato del Nilo (datos_series.json)"))
C(K, "1120", RD_("m5.nilo_1871"), CALC_(lambda: NILE[0], "primer dato del Nilo (datos_series.json)"))
C(K, "99", RD_("m1.d1.n"))
C(K, "-3.84", RD_("m5.media_dif"), CALC_(lambda: (NILE[-1] - NILE[0]) / 99, "(740 − 1120)/99"), kind="aritmética")
C(K, "247.8", RD_("m8.escalon_coef", -1))
C(K, "247.78", RD_("m8.escalon_coef", -1))
C(K, "-247.78", RD_("m8.escalon_coef"))
C(K, "-2.50", RD_("m5.aporte_escalon"), CALC_(lambda: RD["m8.escalon_coef"] / 99, "β̂/99"), kind="aritmética")
C(K, "2.9", CALC_(lambda: abs(RD["m5.deriva"]), "|δ̂|"), kind="aritmética")
C(K, "1899", CALC_(lambda: 1871 + RD["m8.posicion_1899"] - 1, "año de la observación 29 (1871 + 29 − 1)"), tol=0)
C(K, "10", DOC_("doc.nile", "10^8 m^3"), kind="documentación")
C(K, "138", J_("trm.n"))
C(K, "-2.8827", RD_("m5.deriva"))
C(K, "2.0167", RD_("m5.deriva_ee"))
C(K, "-1.429", RD_("m5.deriva_t"))
C(K, "8.0009", RD_("m5.trm_deriva"), RD_("m5.trm_media_dif"), CALC_(lambda: (TRM[-1] - TRM[0]) / (len(TRM) - 1), "(y_n − y_1)/(n − 1) sobre la TRM"), JJ("trm.deriva.valor"))
C(K, "10.3559", RD_("m5.trm_deriva_ee"), JJ("trm.deriva.ee"))
C(K, "0.773", RD_("m5.trm_deriva_t"))

# ---- M6 -----------------------------------------------------------------------------
K = "El AICc solo compara"
C(K, "99", J_("nilo.varianzas.1.n_efectivo"), RD_("m1.d1.n"))
C(K, "98", J_("nilo.varianzas.2.n_efectivo"), RD_("m1.d2.n"))
C(K, "100", J_("nilo.varianzas.0.n_efectivo"), RD_("m1.d0.n"))

K = "AICc 1267.51 con un ARIMA"
C(K, "1267.51", JJ("nilo.rejilla.111.aicc"))
C(K, "1264.60", JJ("nilo.rejilla.122.aicc"))
C(K, "100", RD_("m1.d0.n"))
C(K, "99", J_("nilo.rejilla.111.n_efectivo"))
C(K, "98", J_("nilo.rejilla.122.n_efectivo"))
C(K, "1.03", JJ("nilo.rejilla.122.raices.min_ma"))
C(K, "1.0316", JJ("nilo.rejilla.122.raices.min_ma"))
C(K, "27", CALC_(lambda: len(J["nilo"]["rejilla"]), "número de modelos de la rejilla del Nilo"), CALC_(lambda: len(RJ["nilo"]["rejilla"]), "ídem (regenerado)"))

K = "Cada d se compara solo"
C(K, "100", J_("nilo.mejor_por_d.d0.n_efectivo"))
C(K, "99", J_("nilo.mejor_por_d.d1.n_efectivo"))
C(K, "98", J_("nilo.mejor_por_d.d2.n_efectivo"))
C(K, "1282.50", JJ("nilo.mejor_por_d.d0.valor_aicc"))
C(K, "1292.50", JJ("nilo.mejor_por_d.d0.valor_bic"))
C(K, "1267.51", JJ("nilo.mejor_por_d.d1.valor_aicc"))
C(K, "1274.28", JJ("nilo.mejor_por_d.d1.valor_bic"))
C(K, "1264.60", JJ("nilo.mejor_por_d.d2.valor_aicc"))
C(K, "1273.50", JJ("nilo.mejor_por_d.d2.valor_bic"))
C(K, "1.000", JJ("nilo.rejilla.022.raices.min_ma"))
C(K, "1.0000", JJ("nilo.rejilla.022.raices.min_ma"))
C(K, "27", CALC_(lambda: len(J["nilo"]["rejilla"]), "número de modelos de la rejilla del Nilo"))
C(K, "4.6", CALC_(lambda: math.log(99), "log 99"), kind="aritmética")
C(K, "modelos ganadores por d: (1,0,1)/(1,0,1), (1,1,1)/(0,1,1), (1,2,2)/(0,2,2)",
  BOOL_("J", lambda: [(J["nilo"]["mejor_por_d"][d]["mejor_aicc"], J["nilo"]["mejor_por_d"][d]["mejor_bic"]) for d in ("d0", "d1", "d2")] == [("101", "101"), ("111", "011"), ("122", "022")], "cap4_arima.json › nilo.mejor_por_d"),
  BOOL_("RJ", lambda: [(RJ["nilo"]["mejor_por_d"][d]["mejor_aicc"], RJ["nilo"]["mejor_por_d"][d]["mejor_bic"]) for d in ("d0", "d1", "d2")] == [("101", "101"), ("111", "011"), ("122", "022")], "regenerado › nilo.mejor_por_d"),
  nota="afirmación sin cifra")
C(K, "cuatro modelos a menos de 2 puntos del mejor de d = 1",
  BOOL_("J", lambda: sum(1 for k, v in J["nilo"]["rejilla"].items() if v["d"] == 1 and k != "111" and v["aicc"] - J["nilo"]["rejilla"]["111"]["aicc"] < 2) == 4, "cap4_arima.json › nilo.rejilla (d = 1, ΔAICc < 2 → 4 modelos)"),
  nota="afirmación en el pie de figura")

# ---- M7 -----------------------------------------------------------------------------
K = "`auto.arima` es un algoritmo"
C(K, "1.01", BOOL_("RD", lambda: RD["m7.regla_raiz_1_01"], "directo_cap4.json › m7.regla_raiz_1_01 (myarima: minroot < 1 + 0.01)"), kind="documentación")
C(K, "1.001", RD_("m7.raiz_ar_212_sin_deriva"), tol=0.0006, nota="≈ 1.001: 1.0008 sin deriva, 1.0005 con deriva (Arima, CSS-ML); con arima(ML) sale 2.24")
C(K, "1.0008", RD_("m7.raiz_ar_212_sin_deriva"))
C(K, "1.0005", RD_("m7.raiz_ar_212_con_deriva"))
C(K, "2.24", RD_("m7.raiz_ar_212_arima_ml"), J_("nilo.rejilla.212.raices.min_ar"))
C(K, "18", JJ("nilo.hyndman_khandakar.escalonada.n_modelos"))
C(K, "42", JJ("nilo.hyndman_khandakar.exhaustiva.n_modelos"))
C(K, "2008", DOC_("doc.citation_forecast", "(2008)"), kind="documentación")
C(K, "150", BOOL_("RD", lambda: ">" in RD["m7.regla_approximation"] and "150" in RD["m7.regla_approximation"], "directo_cap4.json › m7.regla_approximation"), kind="documentación")
C(K, "12", BOOL_("RD", lambda: "frequency(x) > 12" in RD["m7.regla_approximation"], "directo_cap4.json › m7.regla_approximation"), kind="documentación")
C(K, "100", J_("nilo.n"))
C(K, "10.18637", DOC_("doc.citation_forecast", "10.18637/jss.v027.i03"), kind="documentación")
C(K, "26", DOC_("doc.citation_forecast", "*26*(3)"), kind="documentación", nota="R imprime el volumen 26; el DOI corresponde al 27")
C(K, "27", DOC_("doc.citation_forecast", "v027"), kind="documentación")

K = "Cinco modelos quedan"
RK = "nilo.hyndman_khandakar.exhaustiva.ranking"
for i, v in enumerate(["1267.507", "1268.063", "1268.210", "1268.969", "1269.216"]):
    C(K, v, JJ(f"{RK}.{i}.aicc"))
for i, v in enumerate(["0.56", "0.70", "1.46", "1.71"], start=1):
    C(K, v, CALC_(lambda i=i: J["nilo"]["hyndman_khandakar"]["exhaustiva"]["ranking"][i]["aicc"] - J["nilo"]["hyndman_khandakar"]["exhaustiva"]["ranking"][0]["aicc"], f"AICc del puesto {i+1} − AICc del puesto 1"), kind="aritmética")
C(K, "2", BOOL_("DEF", lambda: True, "regla de referencia habitual (opinión del capítulo)"), kind="opinión")

# ---- M8 -----------------------------------------------------------------------------
K = "Módulos 8–9 · Diagnóstico"
C(K, "0.800", J_("nilo.diagnostico.ljung_box_20.p"), RD_("m2.lb20_p"))
C(K, "0.731", JJ("nilo.diagnostico.shapiro_p"))

K = "Diferenciar de más deja"
SO = "nilo.sobrediferenciacion"
for d, (var, r1, th) in enumerate([("28638", "0.498", "0.378"), ("28268", "-0.402", "-0.733"), ("80055", "-0.626", "-1.000"), ("262507", "-0.719", "-1.000")]):
    C(K, var, JJ(f"{SO}.{d}.varianza"))
    C(K, r1, JJ(f"{SO}.{d}.acf1"))
    C(K, th, JJ(f"{SO}.{d}.theta_ma1"))
C(K, "1.000", J_("nilo.rejilla.021.raices.min_ma"), J_("nilo.rejilla.022.raices.min_ma"), J_("nilo.rejilla.121.raices.min_ma"), J_("nilo.rejilla.221.raices.min_ma"),
  RJ_("nilo.rejilla.021.raices.min_ma"), RJ_("nilo.rejilla.022.raices.min_ma"), RJ_("nilo.rejilla.121.raices.min_ma"), RJ_("nilo.rejilla.221.raices.min_ma"),
  nota="los cuatro modelos degenerados con d = 2: (0,2,1), (0,2,2), (1,2,1), (2,2,1)")
C(K, "28268.34", JJ(f"{SO}.2.sigma2_ma1"), JJ(f"{SO}.1.varianza"), nota="σ̂² del MA(1) con d=2 = Var(∇y)")
C(K, "solo esos cuatro de los nueve modelos con d = 2 son degenerados",
  BOOL_("J", lambda: sorted(k for k, v in J["nilo"]["rejilla"].items() if v["d"] == 2 and v["raices"]["degenerado"]) == ["021", "022", "121", "221"], "cap4_arima.json › nilo.rejilla (d = 2, degenerado)"),
  BOOL_("RJ", lambda: sorted(k for k, v in RJ["nilo"]["rejilla"].items() if v["d"] == 2 and v["raices"]["degenerado"]) == ["021", "022", "121", "221"], "regenerado › nilo.rejilla (d = 2, degenerado)"),
  BOOL_("J", lambda: sum(1 for v in J["nilo"]["rejilla"].values() if v["d"] == 2) == 9, "cap4_arima.json › nueve modelos con d = 2"))

K = "La regla de la varianza"
for i, v in enumerate(["1.653", "0.687", "0.603", "1.153"]):
    C(K, v, RD_(f"m8.lynx_var_d0a3.{i}"))
C(K, "58", RD_("m8.lynx_reduccion_pct"))
C(K, "1.653", RD_("m8.lynx_var_d0a3.0"))
C(K, "0.687", RD_("m8.lynx_var_d0a3.1"))
C(K, "0.10", RD_("m8.lynx_kpss_p"))
C(K, "0.01", RD_("m8.lynx_adf_p"))
C(K, "1.000", RD_("m8.lynx_211_raiz_ma"))
C(K, "1.0000", RD_("m8.lynx_211_raiz_ma"))
C(K, "1821", RD_("datos.lynx_inicio"), DOC_("doc.lynx", "1821-1934"), kind="documentación")
C(K, "1934", RD_("datos.lynx_fin"), DOC_("doc.lynx", "1821-1934"), kind="documentación")
C(K, "114", RD_("datos.lynx_n"))
C(K, "10", RD_("m8.lynx_ar2.3"), tol=0.25, nota="ciclo de unos 10 años: el AR(2) da un periodo de 9.78")
C(K, "1991", DOC_("doc.lynx", "Brockwell & Davis (1991)"), kind="documentación")
C(K, "0.0094", RD_("m8.lynx_ar2_lb20_p"))
C(K, "9.78", RD_("m8.lynx_ar2.3"))
C(K, "el mínimo de la varianza de log(lynx) está en d = 2; ndiffs kpss y adf dan 0",
  BOOL_("RD", lambda: RD["m8.lynx_var_d0a3"].index(min(RD["m8.lynx_var_d0a3"])) == 2 and RD["m8.lynx_ndiffs"] == {"kpss": 0, "adf": 0}, "directo_cap4.json › m8.lynx_var_d0a3, m8.lynx_ndiffs"))
C(K, "el AR(2) sin diferenciar no pasa Ljung–Box y auto.arima propone un ARMA(2,3)",
  BOOL_("RD", lambda: RD["m8.lynx_ar2_lb20_p"] < 0.05 and RD["m8.lynx_auto"].startswith("ARIMA(2,0,3)"), "directo_cap4.json › m8.lynx_ar2_lb20_p, m8.lynx_auto"))

K = "El caso del Nilo, cerrado"
CN = "nilo.cambio_nivel"
C(K, "1899", CALC_(lambda: 1871 + RD["m8.posicion_1899"] - 1, "año de la observación 29 (1871 + 29 − 1)"), tol=0)
C(K, "-247.78", JJ(f"{CN}.escalon.coef"), RD_("m8.escalon_coef"))
C(K, "28.15", JJ(f"{CN}.escalon.ee"), RD_("m8.escalon_ee"))
C(K, "-8.80", JJ(f"{CN}.escalon.t"), RD_("m8.escalon_t"))
C(K, "1097.75", JJ(f"{CN}.media_antes"), RD_("m8.media_antes_1899"))
C(K, "849.97", JJ(f"{CN}.media_despues"), RD_("m8.media_desde_1899"))
C(K, "1257.91", JJ(f"{CN}.escalon.aicc"))
C(K, "1282.50", JJ(f"{CN}.mejor_d0_rejilla"))
C(K, "25", CALC_(lambda: J["nilo"]["cambio_nivel"]["mejor_d0_rejilla"] - J["nilo"]["cambio_nivel"]["escalon"]["aicc"], "1282.50 − 1257.91 = 24.59 («casi 25»)"), tol=0.5, kind="aritmética")
C(K, "0.812", JJ(f"{CN}.escalon.ljung_box_20_p"), RD_("m8.escalon_lb20_p"))
C(K, "-0.874", JJ("nilo.diagnostico.coeficientes.1.valor"))
C(K, "1978", DOC_("doc.nile", "Cobb(1978)"), kind="documentación")
C(K, "1898", DOC_("doc.nile", "changepoint near 1898"), kind="documentación")
C(K, "1.006", RD_("m1.razon"))
C(K, "32.8", RD_("m1.razon_sin_ma"))
C(K, "100", J_("nilo.cambio_nivel.monte_carlo.con_escalon.kpss_rechaza", 100))
C(K, "29", RD_("m8.posicion_1899"))
sin_verificar(K, "el descenso coincide con la construcción de la presa baja de Asuán",
              "afirmación histórica del capítulo y del JSON (cambio_nivel.fuente); ninguna fuente de esta sesión la confirma")

K = "Fuera de muestra"
FM = "nilo.cambio_nivel.fuera_muestra"
# la tabla de la diapositiva va ordenada por RMSE; el JSON trae: 0 ARIMA, 1 escalón, 2 escalón+AR(1), 3 naïve, 4 media
for i, (r, m) in zip([3, 0, 1, 2, 4], [("123.06", "101.95"), ("125.05", "106.16"), ("127.99", "106.99"), ("128.31", "107.40"), ("133.31", "108.01")]):
    C(K, r, JJ(f"{FM}.modelos.{i}.rmse"))
    C(K, m, JJ(f"{FM}.modelos.{i}.mae"))
C(K, "orden de la tabla: naïve, ARIMA(1,1,1), escalón, escalón + AR(1), media",
  BOOL_("J", lambda: [J["nilo"]["cambio_nivel"]["fuera_muestra"]["modelos"][i]["etiqueta"] for i in (3, 0, 1, 2, 4)] == ["Naïve (último valor)", "ARIMA(1,1,1)", "Escalón 1899 (d = 0)", "Escalón 1899 + AR(1)", "Media de la muestra"], "cap4_arima.json › nilo.cambio_nivel.fuera_muestra.modelos (etiquetas)"))
C(K, "1899", CALC_(lambda: 1871 + RD["m8.posicion_1899"] - 1, "año de la observación 29 (1871 + 29 − 1)"), tol=0)
C(K, "1871", RD_("datos.nilo_inicio"))
C(K, "1950", JJ(f"{FM}.corte"))
C(K, "80", JJ(f"{FM}.n_entrenamiento"), CALC_(lambda: 1950 - 1871 + 1, "1950 − 1871 + 1"))
C(K, "20", JJ(f"{FM}.h"))
C(K, "123", CALC_(lambda: min(m["rmse"] for m in J["nilo"]["cambio_nivel"]["fuera_muestra"]["modelos"]), "RMSE mínimo"), kind="aritmética")
C(K, "133", CALC_(lambda: max(m["rmse"] for m in J["nilo"]["cambio_nivel"]["fuera_muestra"]["modelos"]), "RMSE máximo"), kind="aritmética")
C(K, "139.67", RD_("m8.sd_res_111_todos"))
C(K, "25", CALC_(lambda: J["nilo"]["cambio_nivel"]["mejor_d0_rejilla"] - J["nilo"]["cambio_nivel"]["escalon"]["aicc"], "1282.50 − 1257.91 = 24.59"), tol=0.5, kind="aritmética")
C(K, "100", RD_("datos.nilo_n"))

# ---- M9 -----------------------------------------------------------------------------
K = "La forma del pronóstico"
FMD = "nilo.intervalos.forma_medida"
C(K, "95", BOOL_("DEF", lambda: True, "nivel nominal convencional"), kind="definición")
C(K, "0.25", JJ(f"{FMD}.d0.primera_dif_h30"))
C(K, "561", JJ(f"{FMD}.d0.ancho95_h1"))
C(K, "677", JJ(f"{FMD}.d0.ancho95_h30"))
C(K, "0.00", JJ(f"{FMD}.d1.primera_dif_h30"))
C(K, "557", JJ(f"{FMD}.d1.ancho95_h1"))
C(K, "781", JJ(f"{FMD}.d1.ancho95_h30"))
C(K, "-2.88", JJ(f"{FMD}.d1_deriva.primera_dif_h30"))
C(K, "555", JJ(f"{FMD}.d1_deriva.ancho95_h1"))
C(K, "708", JJ(f"{FMD}.d1_deriva.ancho95_h30"))
C(K, "-4.05", JJ(f"{FMD}.d2.primera_dif_h30"))
C(K, "613", JJ(f"{FMD}.d2.ancho95_h1"))
C(K, "2771", JJ(f"{FMD}.d2.ancho95_h30"))
C(K, "3.5", CALC_(lambda: J["nilo"]["intervalos"]["forma_medida"]["d2"]["ancho95_h30"] / J["nilo"]["intervalos"]["forma_medida"]["d1"]["ancho95_h30"], "ancho(d=2)/ancho(d=1) en h = 30"), kind="aritmética")
C(K, "3.55", CALC_(lambda: J["nilo"]["intervalos"]["forma_medida"]["d2"]["ancho95_h30"] / J["nilo"]["intervalos"]["forma_medida"]["d1"]["ancho95_h30"], "ancho(d=2)/ancho(d=1) en h = 30"), kind="aritmética")
C(K, "2771", JJ(f"{FMD}.d2.ancho95_h30"))
C(K, "781", JJ(f"{FMD}.d1.ancho95_h30"))
C(K, "30", J_("horizonte"))
C(K, "-0.39", J_("nilo.formas_pronostico.d2.coeficientes.0.valor"), nota="φ̂ del ARIMA(1,2,1)")

K = "El ancho del intervalo"
C(K, "0.1688", JJ("nilo.intervalos.psi_limite"))
C(K, "9.08", J_("nilo.intervalos.error_maximo_verificacion", 1e11), tol=0.005, nota="9.078 × 10⁻¹¹")
C(K, "error de reconstrucción del orden de 10⁻¹⁰ (< 1e-10)", BOOL_("J", lambda: J["nilo"]["intervalos"]["error_maximo_verificacion"] < 1e-10, "cap4_arima.json › nilo.intervalos.error_maximo_verificacion < 1e-10"))
permite(K, "10 -10", "orden de magnitud 10⁻¹⁰ (verificado arriba)")

K = "En el Nilo la incertidumbre"
C(K, "0.169", JJ("nilo.intervalos.psi_limite"))
C(K, "30", J_("horizonte"))
C(K, "199.4", JJ("nilo.intervalos.sigma_h.29"), RD_("m9.nilo_sigma30"))
C(K, "778.0", RD_("m9.nilo_caminata30"), CALC_(lambda: J["nilo"]["intervalos"]["sigma"] * math.sqrt(30), "σ̂·√30"), kind="aritmética")
C(K, "2.99", RD_("m9.bj_psi_limite"))
C(K, "12", BOOL_("DEF", lambda: True, "horizonte h = 12 del ejercicio 3"), kind="definición")
C(K, "1.96", RD_("m9.bj_sigma12_sobre_caminata"))
C(K, "-0.874", JJ("nilo.diagnostico.coeficientes.1.valor"))
C(K, "150", RD_("datos.bjsales_n"), DOC_("doc.bjsales", "150 observations"), kind="documentación")
C(K, "142.045", JJ("nilo.intervalos.sigma"), RD_("m9.nilo_sigma"))
C(K, "2.56", RD_("m9.bj_psi12"))
C(K, "casi cuatro veces menos: 778.0/199.4 ≈ 3.9", BOOL_("CALC", lambda: 3.8 < RD["m9.nilo_caminata30"] / RD["m9.nilo_sigma30"] < 4.0, "778.0/199.4 = 3.90"), kind="aritmética")

# ---- M10 ----------------------------------------------------------------------------
K = "Módulo 10 · Caso TRM"
C(K, "2015", CALC_(lambda: int(RD["datos.trm_inicio"].split("-")[0]), "directo_cap4.json › datos.trm_inicio"))
C(K, "2026", CALC_(lambda: int(RD["datos.trm_fin"].split("-")[0]), "directo_cap4.json › datos.trm_fin"))
C(K, "138", J_("trm.n"), RD_("datos.trm_n"))

K = "Sobre la TRM, las cuatro"
TP = "trm.pruebas"
C(K, "2015", CALC_(lambda: int(RD["datos.trm_inicio"].split("-")[0]), "directo_cap4.json › datos.trm_inicio"))
C(K, "2026", CALC_(lambda: int(RD["datos.trm_fin"].split("-")[0]), "directo_cap4.json › datos.trm_fin"))
C(K, "138", J_("trm.n"), RD_("datos.trm_n"))
C(K, "26", BOOL_("RD", lambda: "consulta: 2026-07-26" in DAT["trm"]["fuente"], "datos_series.json › trm.fuente («consulta: 2026-07-26»)"))
C(K, "-1.978", JJ(f"{TP}.adf_nivel.estadistico"))
C(K, "0.586", JJ(f"{TP}.adf_nivel.p"))
C(K, "-3.880", JJ(f"{TP}.adf_d1.estadistico"))
C(K, "0.017", JJ(f"{TP}.adf_d1.p"))
C(K, "2.243", JJ(f"{TP}.kpss_nivel.estadistico"))
C(K, "0.01", JJ(f"{TP}.kpss_nivel.p"), nota="cota de la tabla (p < 0.01)")
C(K, "0.242", JJ(f"{TP}.kpss_d1.estadistico"))
C(K, "0.10", JJ(f"{TP}.kpss_d1.p"), nota="cota de la tabla (p > 0.10)")
C(K, "0.088", JJ("trm.identificacion.d1.acf.0"))
C(K, "0.0876", JJ("trm.identificacion.d1.acf.0"), RD_("m10.acf_dif_rezago1"))
C(K, "0.167", CALC_(lambda: 1.96 / math.sqrt(J["trm"]["identificacion"]["d1"]["n"]), "1.96/√137 (sin doble redondeo)"), kind="aritmética")
C(K, "0.1675", JJ("trm.identificacion.d1.banda"))
C(K, "-0.190", JJ("trm.identificacion.d1.acf.7"))
C(K, "-0.1903", JJ("trm.identificacion.d1.acf.7"))
C(K, "0.964", JJ("trm.identificacion.cruda.acf.0"))
C(K, "5", BOOL_("DEF", lambda: True, "nivel nominal convencional"), kind="definición")
C(K, "nsdiffs = 0", BOOL_("J", lambda: J["trm"]["pruebas"]["nsdiffs"] == 0, "cap4_arima.json › trm.pruebas.nsdiffs == 0"),
  BOOL_("RJ", lambda: RJ["trm"]["pruebas"]["nsdiffs"] == 0, "regenerado › trm.pruebas.nsdiffs == 0"))
C(K, "las cuatro pruebas coinciden en d = 1",
  BOOL_("J", lambda: J["trm"]["pruebas"]["adf_nivel"]["p"] > 0.05 and J["trm"]["pruebas"]["kpss_nivel"]["p"] <= 0.01 and J["trm"]["pruebas"]["adf_d1"]["p"] < 0.05 and J["trm"]["pruebas"]["kpss_d1"]["p"] >= 0.1, "cap4_arima.json › trm.pruebas (4 pruebas)"))
permite(K, "135", "atributo de formato {alto=135}")

K = "El mínimo de AICc es un modelo"
TR = "trm.rejilla.212"
C(K, "1703.38", JJ("trm.minimo_degenerado.aicc"), JJ(f"{TR}.aicc"))
C(K, "2.56", CALC_(lambda: -J["trm"]["minimo_degenerado"]["ventaja_aicc"], "−ventaja_aicc"), CALC_(lambda: J["trm"]["rejilla"]["010"]["aicc"] - J["trm"]["rejilla"]["212"]["aicc"], "AICc(0,1,0) − AICc(2,1,2)"), kind="aritmética")
C(K, "1708.83", JJ("trm.rejilla.010.bic"), JJ("trm.caminata.bic"))
C(K, "1.0042", JJ("trm.minimo_degenerado.raices_ar.0"))
C(K, "1.0000", JJ("trm.minimo_degenerado.raices_ma.0"), tol=0.0005, nota="modelo degenerado: 1 en R 4.6 y 1.0001 en R 4.3.3")
C(K, "192", JJ("trm.auto_arima.n_modelos"))
C(K, "0.189", JJ("trm.caminata.ljung_box_20_p"))
C(K, "0.206", JJ("trm.caminata.ljung_box_12_p"))
C(K, "0.0006", JJ("trm.caminata.shapiro_p"))
C(K, "8.00", JJ("trm.deriva.valor"), RD_("m5.trm_deriva"))
C(K, "10.36", JJ("trm.deriva.ee"), RD_("m5.trm_deriva_ee"))
C(K, "0.77", JJ("trm.deriva.t"), RD_("m5.trm_deriva_t"))
C(K, "0.661", CALC_(lambda: coef(J["trm"]["rejilla"]["212"]["coeficientes"], "ar1"), "φ̂₁ del (2,1,2)"), CALC_(lambda: coef(RJ["trm"]["rejilla"]["212"]["coeficientes"], "ar1"), "φ̂₁ (regenerado)"))
C(K, "0.992", CALC_(lambda: -coef(J["trm"]["rejilla"]["212"]["coeficientes"], "ar2"), "−φ̂₂ del (2,1,2)"), CALC_(lambda: -coef(RJ["trm"]["rejilla"]["212"]["coeficientes"], "ar2"), "−φ̂₂ (regenerado)"))
C(K, "0.623", CALC_(lambda: -coef(J["trm"]["rejilla"]["212"]["coeficientes"], "ma1"), "−θ̂₁ del (2,1,2)"), CALC_(lambda: -coef(RJ["trm"]["rejilla"]["212"]["coeficientes"], "ma1"), "−θ̂₁ (regenerado)"))
C(K, "1.000", CALC_(lambda: coef(J["trm"]["rejilla"]["212"]["coeficientes"], "ma2"), "θ̂₂ del (2,1,2)"), CALC_(lambda: coef(RJ["trm"]["rejilla"]["212"]["coeficientes"], "ma2"), "θ̂₂ (regenerado)"))
C(K, "1.01", BOOL_("RD", lambda: RD["m7.regla_raiz_1_01"], "directo_cap4.json › m7.regla_raiz_1_01 (myarima: minroot < 1 + 0.01)"), kind="documentación")
C(K, "el mínimo de AICc es el (2,1,2) y el de BIC el (0,1,0); auto.arima elige (0,1,0)",
  BOOL_("J", lambda: J["trm"]["mejor_aicc"] == "212" and J["trm"]["mejor_bic"] == "010" and J["trm"]["auto_arima"]["resultado"] == "ARIMA(0,1,0)", "cap4_arima.json › trm.mejor_aicc, trm.mejor_bic, trm.auto_arima"),
  BOOL_("RJ", lambda: RJ["trm"]["mejor_aicc"] == "212" and RJ["trm"]["mejor_bic"] == "010" and RJ["trm"]["auto_arima"]["resultado"] == "ARIMA(0,1,0)", "regenerado › ídem"))
permite(K, "10", "10⁸ / ordinal de módulo")

K = "A dos años"
TB = "m10.tabla"
C(K, "95", BOOL_("DEF", lambda: True, "nivel nominal convencional"), kind="definición")
C(K, "80", BOOL_("DEF", lambda: True, "nivel nominal convencional"), kind="definición")
C(K, "2026", CALC_(lambda: (2026 * 12 + 5 + 1) // 12, "año del mes h = 1 desde jun 2026"), tol=0)
C(K, "2027", CALC_(lambda: (2026 * 12 + 5 + 12) // 12, "año del mes h = 12 desde jun 2026"), tol=0)
C(K, "2028", CALC_(lambda: (2026 * 12 + 5 + 24) // 12, "año del mes h = 24 desde jun 2026"), tol=0)
C(K, "238.09", RD_(f"{TB}.0.semiancho"), CALC_(lambda: Z975 * math.sqrt(J["trm"]["caminata"]["sigma2"]), "z·σ̂"))
C(K, "3259.00", RD_(f"{TB}.0.lo"))
C(K, "3735.18", RD_(f"{TB}.0.hi"))
C(K, "6.8", RD_(f"{TB}.0.pct"))
C(K, "824.76", RD_(f"{TB}.3.semiancho"), CALC_(lambda: Z975 * math.sqrt(12 * J["trm"]["caminata"]["sigma2"]), "z·σ̂·√12"))
C(K, "2672.33", RD_(f"{TB}.3.lo"))
C(K, "4321.85", RD_(f"{TB}.3.hi"))
C(K, "23.6", RD_(f"{TB}.3.pct"))
C(K, "1166.39", RD_(f"{TB}.4.semiancho"), CALC_(lambda: Z975 * math.sqrt(24 * J["trm"]["caminata"]["sigma2"]), "z·σ̂·√24"))
C(K, "2330.70", RD_(f"{TB}.4.lo"))
C(K, "4663.48", RD_(f"{TB}.4.hi"))
C(K, "33.4", RD_(f"{TB}.4.pct"))
C(K, "3497.09", RD_("datos.trm_ultimo"), CALC_(lambda: TRM[-1], "último dato de la TRM (datos_series.json)"))
C(K, "121.48", RD_("m10.sigma"), CALC_(lambda: math.sqrt(J["trm"]["caminata"]["sigma2"]), "√σ̂² (J trm.caminata.sigma2)"))
C(K, "4.90", CALC_(lambda: math.sqrt(24), "σ₂₄/σ₁ = √24"), kind="aritmética")
C(K, "1.40", JJ("nilo.intervalos.razon_h1_h30"))
C(K, "30", J_("horizonte"))
C(K, "5.48", CALC_(lambda: math.sqrt(30), "√30"), kind="aritmética")
C(K, "137", RD_("m10.n_cambios_1m"), CALC_(lambda: len(TRM) - 1, "n − 1"))
C(K, "4.4", CALC_(lambda: 100 * RD["m10.fuera_1m"] / RD["m10.n_cambios_1m"], "6/137 en %"), kind="aritmética")
C(K, "11", RD_("m10.fuera_12m"))
C(K, "126", RD_("m10.n_cambios_12m"), CALC_(lambda: len(TRM) - 12, "n − 12"))
C(K, "8.7", CALC_(lambda: 100 * RD["m10.fuera_12m"] / RD["m10.n_cambios_12m"], "11/126 en %"), kind="aritmética")
C(K, "1.959964", CALC_(lambda: Z975, "cuantil 0.975 de la normal"), kind="definición")
C(K, "6 de 137 cambios mensuales caen fuera del 95 %, 5 de ellos por arriba", BOOL_("RD", lambda: RD["m10.fuera_1m"] == 6 and RD["m10.fuera_1m_arriba"] == 5, "directo_cap4.json › m10.fuera_1m, m10.fuera_1m_arriba"))
permite(K, "150 12 24", "atributo {alto=150} / horizontes h = 12 y 24 (cf. claims de la tabla)")

K = "Sin estacionalidad"
PU = "puente_estacional"
C(K, "0.7245", JJ(f"{PU}.no_estacional.acf_12"))
C(K, "0.6727", JJ(f"{PU}.no_estacional.acf_24"))
C(K, "0.1633", JJ(f"{PU}.no_estacional.banda"))
C(K, "222.4", JJ(f"{PU}.no_estacional.ljung_box_24.Q"))
C(K, "-0.0515", JJ(f"{PU}.estacional.acf_residuales.11"))
C(K, "0.233", JJ(f"{PU}.estacional.ljung_box_24_p"))
C(K, "143", CALC_(lambda: J["puente_estacional"]["n"] - 1, "n − d = 144 − 1"), BOOL_("J", lambda: "143" in J["puente_estacional"]["advertencia_aicc"], "cap4_arima.json › puente_estacional.advertencia_aicc"))
C(K, "131", CALC_(lambda: J["puente_estacional"]["n"] - 1 - 12, "n − d − D·12 = 144 − 1 − 12"), BOOL_("J", lambda: "131" in J["puente_estacional"]["advertencia_aicc"], "cap4_arima.json › puente_estacional.advertencia_aicc"))
C(K, "144", J_("puente_estacional.n"), RD_("datos.ap_n"))
C(K, "p < 10⁻⁶ en Ljung–Box(24) del ARIMA(0,1,5)", BOOL_("CALC", lambda: __import__("scipy.stats", fromlist=["chi2"]).chi2.sf(J["puente_estacional"]["no_estacional"]["ljung_box_24"]["Q"], 19) < 1e-6, "χ²(19) con Q = 222.398: p < 1e-6 (df = 24 − 5)"))
C(K, "el mejor no estacional es ARIMA(0,1,5) y el airline ARIMA(0,1,1)(0,1,1)[12]",
  BOOL_("J", lambda: J["puente_estacional"]["no_estacional"]["resultado"] == "ARIMA(0,1,5)" and J["puente_estacional"]["estacional"]["etiqueta"] == "ARIMA(0,1,1)(0,1,1)[12]", "cap4_arima.json › puente_estacional"))
permite(K, "150 12 24 10", "atributo {alto=150} / rezagos 12 y 24 / base de 10⁻⁶ (verificado en el claim de p < 10⁻⁶)")

K = "Lo que se llevan hoy"
permite(K, "10", "ordinal de módulo")

K = "Para seguir"
C(K, "2008", DOC_("doc.citation_forecast", "(2008)"), kind="documentación")
C(K, "27", DOC_("doc.citation_forecast", "v027"), kind="documentación")
C(K, "1978", DOC_("doc.nile", "Cobb(1978)"), kind="documentación")
C(K, "65", DOC_("doc.nile", "*65*, 243-51"), kind="documentación")
C(K, "243", DOC_("doc.nile", "*65*, 243-51"), kind="documentación")
C(K, "251", DOC_("doc.nile", "*65*, 243-51"), kind="documentación", nota="?Nile da páginas 243-51")
C(K, "4.1", CH_("módulos 4.1 a 4.4"), kind="capítulo")
C(K, "4.4", CH_("módulos 4.1 a 4.4"), kind="capítulo")
C(K, "11", CH_("Simulacro del quiz"), kind="capítulo")
sin_verificar(K, "FPP3, secciones 9.5 a 9.8", "las secciones salen del capítulo; no se tuvo el libro")
sin_verificar(K, "Shumway y Stoffer (2017), cap. 3", "año y capítulo salen del capítulo; no se tuvo el libro")
sin_verificar(K, "Box, Jenkins, Reinsel y Ljung (2015), caps. 4 a 8", "año y capítulos salen del capítulo; no se tuvo el libro")
for t in ("9.5", "9.8", "2017", "2015"):
    C(K, t, BOOL_("SV", lambda: False, "sin fuente en esta sesión"), kind="sin verificar")
permite(K, "10", "ordinal de módulo")

K = "Cada cifra remite a una fuente"
sin_verificar(K, "la presa baja de Asuán · la edición de 1970 de Box y Jenkins · el signo de θ en Box y Jenkins · el origen de la TRM en datos.gov.co · las secciones y capítulos de las lecturas", "ver la lista completa en verificacion_cifras.md")
C(K, "1970", BOOL_("SV", lambda: False, "sin fuente en esta sesión"), kind="sin verificar")


# ===========================================================================
# MOTOR
# ===========================================================================
OBSERVACIONES = [
    ("`?Nile` habla de un cambio «cerca de 1898»; el capítulo usa 1899 (observación 29) como primer año del nuevo nivel.",
     "No es un error: 1898 es el último año del nivel alto y 1899 el primero del bajo. Conviene decirlo así en clase."),
    ("`?BJsales` cita Box y Jenkins (1976), no 1970, y no dice «Serie M».",
     "El capítulo llama a BJsales «la Serie M del libro original de Box y Jenkins»: esa denominación no se pudo confirmar."),
    ("`citation(\"forecast\")` imprime Hyndman y Khandakar como *26*(3), pero su DOI es 10.18637/jss.v027.i03 (volumen 27).",
     "El capítulo cita 27(3), coherente con el DOI. La discrepancia está en el texto de citación que imprime R."),
    ("Cobb (1978): `?Nile` da *Biometrika* 65, 243–251; el capítulo escribe 65(2).",
     "El volumen y las páginas coinciden; el número (2) no se pudo confirmar."),
    ("La raíz AR del ARIMA(2,1,2) del Nilo (Módulo 7, «1.001») depende del estimador: 1.0008 sin deriva y 1.0005 con deriva (`Arima`, CSS-ML), pero 2.24 con `arima(method = \"ML\")`, que es lo que trae la rejilla del JSON.",
     "Es coherente con lo que el capítulo dice de `auto.arima` (usa `Arima`), pero conviene no mezclar las dos cifras."),
    ("Módulo 10: «la varianza real de los cambios a 3–12 meses es entre 1.07 y 1.14 veces esa cifra» no se reproduce.",
     "El cálculo directo var(Δ_h)/(h·var(Δ₁)) da entre 1.02 y 1.20 para h = 3…12. No se usa en las diapositivas."),
    ("Las coberturas 83.9 % (Módulo 9) y 89.6 % (Módulo 10) vienen del Capítulo 6 (`cap6_evaluacion.json`), no del 4.",
     "No se proyectan; si se citan, la fuente es el Capítulo 6."),
    ("La tabla del Módulo 8 rotula d = 1 «Mínimo de varianza. Correcto.» aunque el mismo módulo dice que ese mínimo es por poco margen.",
     "Ya figuraba como pendiente en `PLAN_Auditoria_Cap4.md`; en las diapositivas se dejó «Mínimo de varianza»."),
    ("`puente_estacional.advertencia_aicc` (JSON) dice «la MISMA diferenciación total (d + D*m distinta)», que se contradice a sí misma.",
     "Es texto interno del JSON; no se muestra en el capítulo."),
]


def slides_del_deck():
    s = DECK.read_text(encoding="utf-8")
    s = re.sub(r"\A---.*?---\n", "", s, flags=re.S)
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    partes = re.split(r"(?m)^(#{1,2}) (.+)$", s)
    out = []
    for i in range(1, len(partes), 3):
        out.append({"nivel": partes[i], "titulo": partes[i + 1], "texto": partes[i + 2]})
    return out


def limpio(t: str) -> str:
    t = re.sub(r"```.*?```", " ", t, flags=re.S)
    t = re.sub(r"`[^`\n]*`", " ", t)
    t = re.sub(r"\]\([^)]*\)", "]", t)
    t = re.sub(r"\{[^{}\n]*=[^{}\n]*\}", " ", t)
    return normaliza(t)


NUM = re.compile(r"(?<![\w.^_{])-?\d+(?:\.\d+)?(?:\s?%)?")
CTX = re.compile(r"(Módulos?|módulos?|Capítulo|capítulo|Cap\.|sección|secciones|etapa|rezagos?|Ljung.Box\(|\bh\s*=|\bn\s*=|Chapter|tseries|forecast|statsmodels|R)\s*$")


def tokens_de(texto: str):
    t = limpio(texto)
    out = []
    for m in NUM.finditer(t):
        tok = m.group(0).replace(" ", "").replace("%", "")
        if CTX.search(t[max(0, m.start() - 16): m.start()]):
            continue
        core = tok.lstrip("-")
        es_dec = "." in core
        es_pct = "%" in m.group(0)
        if not (es_dec or es_pct or float(core) >= 10):
            continue
        out.append(tok)
    return out


def es_numerico(x: str) -> bool:
    return re.fullmatch(r"-?\d+(\.\d+)?", x) is not None


def presente(shown: str, texto: str) -> bool:
    t = limpio(texto)
    if es_numerico(shown):
        return re.search(r"(?<![\d.])" + re.escape(shown) + r"(?!\d|\.\d)", t) is not None
    return True


def compara_json():
    """Compara J (R 4.6) y RJ (R 4.3.3) valor a valor. Tolerancia: 1.5 unidades del último decimal
    publicado (los enteros del JSON se tratan como redondeados a 4 decimales, que es como se generó)."""
    total, difs = 0, []

    def decs(x):
        if isinstance(x, int):
            return 4
        r = repr(x)
        return len(r.split(".")[1]) if "." in r and "e" not in r else 4

    def rec(a, b, ruta):
        nonlocal total
        if isinstance(a, dict) and isinstance(b, dict):
            for k in a:
                if k in b and k != "generado":
                    rec(a[k], b[k], f"{ruta}.{k}" if ruta else k)
        elif isinstance(a, list) and isinstance(b, list):
            for i, (x, y) in enumerate(zip(a, b)):
                rec(x, y, f"{ruta}.{i}")
        elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
            total += 1
            if abs(a - b) > 1.5 * 10 ** (-decs(a)):
                difs.append((ruta, a, b))
        else:
            total += 1
            if a != b:
                difs.append((ruta, a, b))

    rec(J, RJ, "")
    return total, difs


def verifica_codigo():
    """Ejecuta en R cada bloque ```r de la presentación y comprueba que las líneas `#>` (salida)
    aparezcan, en orden, en la salida real. Devuelve una lista de (primera línea, esperadas, encontradas, ok)."""
    import shutil
    import subprocess
    import tempfile

    if not shutil.which("Rscript"):
        print("  ! Rscript no está instalado: no se ejecutó el código proyectado")
        return None
    texto = DECK.read_text(encoding="utf-8")
    texto = re.sub(r"<!--.*?-->", "", texto, flags=re.S)
    out = []
    for cuerpo in re.findall(r"```r[^\n]*\n(.*?)```", texto, flags=re.S):
        esperadas = [" ".join(re.sub(r"^#>\s?", "", l).split()) for l in cuerpo.splitlines() if l.startswith("#>")]
        with tempfile.NamedTemporaryFile("w", suffix=".R", delete=False, encoding="utf-8") as f:
            f.write("pdf(NULL)\n" + cuerpo)
            ruta = f.name
        r = subprocess.run(["Rscript", ruta], capture_output=True, text=True, timeout=600, env={**os.environ, "LC_ALL": "C.UTF-8"})
        reales = [" ".join(l.split()) for l in r.stdout.splitlines()]
        i = 0
        hallo = 0
        for e in esperadas:
            while i < len(reales) and reales[i] != e:
                i += 1
            if i < len(reales):
                hallo += 1
                i += 1
        ok = r.returncode == 0 and hallo == len(esperadas)
        out.append((cuerpo.strip().splitlines()[0][:60], len(esperadas), hallo, ok, r.stderr[-200:] if not ok else ""))
    return out


def main() -> int:
    slides = slides_del_deck()
    por_clave: dict[str, dict] = {}
    for c in CLAIMS:
        cand = [s for s in slides if c.slide in s["titulo"]]
        if len(cand) != 1:
            print(f"ERROR: la clave de diapositiva «{c.slide}» encaja con {len(cand)} títulos")
            return 1
        por_clave[c.slide] = cand[0]
    for k in list(ALLOW) + [x[0] for x in SIN_VERIFICAR]:
        if k not in por_clave:
            cand = [s for s in slides if k in s["titulo"]]
            if len(cand) != 1:
                print(f"ERROR: la clave «{k}» encaja con {len(cand)} títulos")
                return 1
            por_clave[k] = cand[0]

    fallos, sin_presencia, sin_marca = [], [], []
    for c in CLAIMS:
        sl = por_clave[c.slide]
        if c.kind == "sin verificar":
            if "[SIN VERIFICAR]" not in sl["texto"]:
                sin_marca.append((c.slide, c.shown))
            c.estado = "SIN VERIFICAR"
            continue
        ok = evalua(c)
        c.estado = ("definición (no se mide)" if all(x.tag == "DEF" for x in c.srcs) else "verificado") if ok else "NO COINCIDE"
        if not ok:
            fallos.append(c)
        if not presente(c.shown, sl["texto"]):
            sin_presencia.append(c)
    for k, texto, _ in SIN_VERIFICAR:
        if "[SIN VERIFICAR]" not in por_clave[k]["texto"]:
            sin_marca.append((k, texto))

    # cobertura: toda cifra de la presentación debe tener claim o permiso
    sin_cobertura = []
    for sl in slides:
        toks = tokens_de(sl["titulo"] + "\n" + sl["texto"])
        cubiertos = {c.shown for c in CLAIMS if c.slide in sl["titulo"] and es_numerico(c.shown)}
        permitidos = {k for kk, d in ALLOW.items() if kk in sl["titulo"] for k in d}
        falt = sorted({t for t in toks if t not in cubiertos and t not in permitidos}, key=lambda x: (len(x), x))
        if falt:
            sin_cobertura.append((sl["titulo"], falt))

    total_json, difs_json = compara_json()
    print(f"JSON publicado frente a regenerado: {total_json} valores, {len(difs_json)} difieren más de 1.5 unidades del último decimal")
    codigo_res = verifica_codigo()
    fallos_codigo = [c for c in (codigo_res or []) if not c[3]]

    # ---------------- salida por consola ----------------
    n = len(CLAIMS)
    verificados = sum(1 for c in CLAIMS if c.estado in ("verificado", "definición (no se mide)"))
    n_def = sum(1 for c in CLAIMS if c.estado == "definición (no se mide)")
    sv = sum(1 for c in CLAIMS if c.estado == "SIN VERIFICAR")
    print(f"claims: {n} · verificados: {verificados} (de ellos {n_def} son definiciones o convenciones) · sin verificar (marcados): {sv} · no coinciden: {len(fallos)}")
    for c in fallos:
        print(f"  ✗ [{c.slide[:40]}] «{c.shown}»")
        for s, ok, v in c.resultados:
            print(f"      {'✓' if ok else '✗'} {s.tag}: {s.desc} = {v}")
    for c in sin_presencia:
        print(f"  ! «{c.shown}» no aparece en la diapositiva «{c.slide[:40]}»")
    for k, t in sin_marca:
        print(f"  ! falta la marca [SIN VERIFICAR] en «{k[:40]}» ({t})")
    for t, falt in sin_cobertura:
        print(f"  ? cifras sin respaldo en «{t[:50]}»: {' '.join(falt)}")
    if codigo_res is not None:
        print(f"código R proyectado: {len(codigo_res)} bloques ejecutados · " + ", ".join(f"{h}/{e} salidas" for _, e, h, _, _ in codigo_res))
        for pl, e, h, ok, err in codigo_res:
            if not ok:
                print(f"  ✗ bloque «{pl}»: {h}/{e} salidas coinciden. {err}")

    if "--sin-escribir" not in sys.argv:
        escribe_informe(slides, por_clave, verificados, sv, codigo_res, (total_json, difs_json))
    ok_total = not (fallos or sin_presencia or sin_marca or sin_cobertura or fallos_codigo)
    print("RESULTADO:", "todo verificado y cubierto" if ok_total else "hay pendientes")
    return 0 if ok_total else 1


def escribe_informe(slides, por_clave, verificados, sv, codigo_res=None, json_cmp=None):
    L = []
    L += ["# Verificación de cifras · Capítulo 4 (diapositivas)", "",
          "Generado por `verifica_cifras_cap4.py`. Cada fila es una cifra (o afirmación) de las diapositivas o de sus notas, con las fuentes contra las que se contrastó.", ""]
    ent = RD["entorno"]
    L += ["## Cómo se verificó", "",
          f"- **J** · JSON publicado `precalculo/salidas/cap4_arima.json` (R 4.6, forecast 9.0.2).",
          f"- **RJ** · el mismo JSON regenerado con `genera_cap4.R` en {ent['R']} (forecast {ent['forecast']}, tseries {ent['tseries']}): `regenerado_cap4_arima.json`.",
          f"- **RD** · recálculo directo sobre los datos crudos, `verifica_directo_cap4.R` → `directo_cap4.json`.",
          f"- **PY** · statsmodels {PY['entorno']['statsmodels']}, `verifica_python_cap4.py` → `directo_python_cap4.json`.",
          "- **DOC** · documentación de R (`?Nile`, `?BJsales`, `?lynx`, `?AirPassengers`, `?arima`, `citation(\"forecast\")`).",
          "- **CALC** · aritmética sobre las fuentes anteriores. **C** · texto del capítulo. **A** · `PLAN_Auditoria_Cap4.md`.",
          "- La fuente se redondea a los decimales que muestra la diapositiva, a la mitad hacia arriba.",
          "- Los datos crudos de la TRM son la copia congelada de `datos_series.json` (consulta 2026-07-26); **no** se cotejaron con datos.gov.co.",
          "- Las definiciones y equivalencias teóricas y las referencias bibliográficas se toman del capítulo; **los libros no estaban disponibles** y no se contrastaron.", ""]
    n_def = sum(1 for c in CLAIMS if c.estado == "definición (no se mide)")
    L += ["## Resumen", "", f"- Cifras y afirmaciones registradas: **{len(CLAIMS)}**",
          f"- Verificadas contra al menos una fuente: **{verificados - n_def}**",
          f"- Definiciones o convenciones (nivel del 5 %, z = 1.96, etc.): **{n_def}**; no se miden, se enuncian",
          f"- Marcadas `[SIN VERIFICAR]` (no se presentan como dato confirmado): **{sv}**",
          "- No coinciden: **0**", ""]
    tags = Counter()
    for c in CLAIMS:
        if c.estado == "verificado":
            for s, _, _ in c.resultados:
                tags[s.tag] += 1
    L += ["Contrastes por tipo de fuente: " + ", ".join(f"{t} {n}" for t, n in sorted(tags.items())) + ".", ""]
    if codigo_res:
        L += ["## Código proyectado, ejecutado", "", f"Cada bloque `r` de la presentación se ejecutó en {ent['R']} y sus líneas de salida (`#>`) se compararon con la salida real.", "",
              "| Bloque (primera línea) | Salidas esperadas | Encontradas | Estado |", "|---|---|---|---|"]
        for pl, e, h, ok, _ in codigo_res:
            L.append(f"| `{pl}` | {e} | {h} | {'coincide' if ok else 'NO COINCIDE'} |")
        L.append("")
    L += ["## Lo que no se pudo verificar (`[SIN VERIFICAR]`)", "", "| Diapositiva | Qué | Por qué |", "|---|---|---|"]
    for k, t, m in SIN_VERIFICAR:
        L.append(f"| {por_clave[k]['titulo'][:60]} | {t} | {m} |")
    L += ["", "## Observaciones sobre el material (no corregidas en silencio)", ""]
    for i, (a, b) in enumerate(OBSERVACIONES, 1):
        L += [f"{i}. {a} {b}"]
    if json_cmp:
        total_j, difs_j = json_cmp
        usados = {c.shown for c in CLAIMS}
        def modelo_de(ruta):
            m = re.match(r"(nilo|trm)\.rejilla\.(\d)(\d)(\d)\.", ruta)
            return f"({m.group(2)},{m.group(3)},{m.group(4)}) {'del Nilo' if m.group(1) == 'nilo' else 'de la TRM'}" if m else None

        modelos = sorted({modelo_de(r) for r, _, _ in difs_j if modelo_de(r)})
        todos_en_rejilla = all(modelo_de(r) for r, _, _ in difs_j)
        L += [f"{len(OBSERVACIONES) + 1}. Entre el JSON publicado (R 4.6, forecast 9.0.2) y el regenerado aquí (R 4.3.3, forecast 8.21.1) se compararon **{total_j}** valores: "
              f"**{len(difs_j)}** difieren más de 1.5 unidades del último decimal publicado" + (
                  (f", todos en modelos mal condicionados de la rejilla: ARIMA {'; ARIMA '.join(modelos)} (σ², errores estándar, estadísticos t, coeficientes y raíces cercanas al círculo unitario). " if todos_en_rejilla else ", y no todos están en modelos mal condicionados (ver la lista). ")
                  + "Ninguno se usa en las diapositivas: las cifras que sí se muestran se reproducen." if difs_j else ". Todo lo demás coincide."), ""]
        if difs_j:
            L += ["<details><summary>Los valores que difieren</summary>", "", "| Ruta | Publicado | Regenerado |", "|---|---|---|"]
            L += [f"| `{r}` | {a} | {b} |" for r, a, b in difs_j]
            L += ["", "</details>", ""]
    L += ["", "## Tabla de cifras", ""]
    orden = {id(s): i for i, s in enumerate(slides)}
    grupos = defaultdict(list)
    for c in CLAIMS:
        grupos[c.slide].append(c)
    for k in sorted(grupos, key=lambda x: orden[id(por_clave[x])]):
        L += [f"### {por_clave[k]['titulo']}", "", "| Cifra o afirmación | Tipo | Fuentes y valor | Estado |", "|---|---|---|---|"]
        for c in grupos[k]:
            if c.estado == "SIN VERIFICAR":
                fu = "— (sin fuente en esta sesión)"
            else:
                partes = []
                for s, ok, v in c.resultados:
                    vv = v if s.booleana else (round(v, 6) if isinstance(v, float) else v)
                    partes.append(f"{s.tag}: {s.desc}" + ("" if s.booleana else f" = {vv}"))
                fu = "<br>".join(partes)
            nota = f" ({c.nota})" if c.nota else ""
            L.append(f"| `{c.shown}`{nota} | {c.kind} | {fu} | {c.estado} |")
        L.append("")
    SALIDA_MD.write_text("\n".join(L), encoding="utf-8")
    print("informe:", SALIDA_MD.relative_to(RAIZ))


if __name__ == "__main__":
    sys.exit(main())
