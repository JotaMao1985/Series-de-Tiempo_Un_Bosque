#!/usr/bin/env python3
"""Verifica, cifra por cifra, la presentación del capítulo 5 contra sus fuentes.

Qué hace
  1. Lee `fuentes/capitulo_5.md` (diapositivas y notas) y extrae TODAS las cifras que exigen
     respaldo: decimales, porcentajes, enteros >= 10 y años.
  2. Compara cada una con su fuente, redondeando la fuente a los decimales que muestra la
     diapositiva (a la mitad hacia arriba):
        J    `precalculo/salidas/cap5_sarima.json` (el precálculo del capítulo)
        J4   `precalculo/salidas/cap4_arima.json` (el puente con el capítulo 4)
        J3   `precalculo/salidas/cap3_arma.json` (el periodo de las manchas solares)
        R    `directo_cap5.json`: recálculo en R sobre los datos (`verifica_directo_cap5.R`)
        PY   `directo_python_cap5.json`: statsmodels (`verifica_python_cap5.py`)
        DOC  `docs_cap5.json`: ayuda de R y NEWS de forecast (`verifica_docs_cap5.R`)
        CALC aritmética sobre los datos congelados o sobre las fuentes anteriores
        C    texto del capítulo (`capitulo-5-sarima.html`)
        DEF  definición o convención: no se mide
  3. Comprueba que ninguna cifra quede sin claim y que cada claim aparezca en su diapositiva.
  4. Ejecuta en R cada bloque ```r de la presentación y compara sus líneas `#>`.
  5. Comprueba que los tres gráficos animados son exactamente los que genera
     `genera_animados_cap5.py` desde J (así ninguna cifra dibujada se escribió a mano).
  6. Escribe `verificacion_cifras_cap5.md`.

Uso (desde la raíz del repositorio):
    python3 Htmls_Series/diapositivas/fuentes/verificacion/verifica_cifras_cap5.py
Sale con código 1 si algo no coincide o queda una cifra sin respaldo.
"""
from __future__ import annotations

import html
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[3]
DECK = Path(os.environ.get("DECK_CAP5", AQUI.parent / "capitulo_5.md"))
SALIDA_MD = AQUI / "verificacion_cifras_cap5.md"
sys.path.insert(0, str(AQUI))
import genera_animados_cap5 as GEN  # noqa: E402


def cargar(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


J = cargar(RAIZ / "precalculo/salidas/cap5_sarima.json")
J4 = cargar(RAIZ / "precalculo/salidas/cap4_arima.json")
J3 = cargar(RAIZ / "precalculo/salidas/cap3_arma.json")
R = cargar(AQUI / "directo_cap5.json")
PY = cargar(AQUI / "directo_python_cap5.json")
DOCS = cargar(AQUI / "docs_cap5.json")
DAT = cargar(RAIZ / "precalculo/salidas/datos_series.json")


def _texto_html(p: Path) -> str:
    t = re.sub(r"<(script|style)\b.*?</\1>", " ", p.read_text(encoding="utf-8"), flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t.replace(" ", " ").replace(" ", " "))


CAP = _texto_html(RAIZ / "Htmls_Series/capitulo-5-sarima.html")
CAP_CRUDO = (RAIZ / "Htmls_Series/capitulo-5-sarima.html").read_text(encoding="utf-8")


def get(obj, ruta: str):
    for parte in ruta.split("."):
        obj = obj[int(parte)] if isinstance(obj, list) else obj[parte]
    return obj


# ---------------------------------------------------------------------------
# Datos crudos y ACF con divisor n (como `Acf` de forecast y `acf` de statsmodels)
# ---------------------------------------------------------------------------
AP = DAT["airpassengers"]["valores"]
LAP = [math.log(x) for x in AP]
UAD = DAT["usaccdeaths"]["valores"]
CO2 = DAT["co2"]["valores"]
TRM = DAT["trm"]["valores"]
DTRM = [b - a for a, b in zip(TRM, TRM[1:])]


def acf(x, k):
    n, m = len(x), sum(x) / len(x)
    c0 = sum((v - m) ** 2 for v in x)
    return sum((x[t] - m) * (x[t + k] - m) for t in range(n - k)) / c0


def banda(n):
    return 1.96 / math.sqrt(n)


# ---------------------------------------------------------------------------
# Fuentes
# ---------------------------------------------------------------------------
class Src:
    def __init__(self, tag: str, fn, desc: str, booleana: bool = False):
        self.tag, self.fn, self.desc, self.booleana = tag, fn, desc, booleana

    def valor(self):
        return self.fn()


def J_(ruta, m=1):
    return Src("J", lambda: get(J, ruta) * m, f"cap5_sarima.json › {ruta}")


def J4_(ruta, m=1):
    return Src("J4", lambda: get(J4, ruta) * m, f"cap4_arima.json › {ruta}")


def J3_(ruta, m=1):
    return Src("J3", lambda: get(J3, ruta) * m, f"cap3_arma.json › {ruta}")


def R_(ruta, m=1):
    return Src("R", lambda: get(R, ruta) * m, f"directo_cap5.json › {ruta}")


def PY_(ruta, m=1):
    return Src("PY", lambda: get(PY, ruta) * m, f"directo_python_cap5.json › {ruta}")


def CALC_(fn, desc):
    return Src("CALC", fn, desc)


def DOC_(clave, aguja):
    return Src("DOC", lambda: aguja in json.dumps(DOCS[clave], ensure_ascii=False), f"docs_cap5.json › {clave} contiene «{aguja}»", True)


def CH_(aguja):
    return Src("C", lambda: aguja in CAP, f"capítulo 5 contiene «{aguja}»", True)


def CHQ_(aguja):
    """El cuestionario del capítulo vive en un <script>: se busca en el HTML crudo."""
    return Src("C", lambda: aguja in CAP_CRUDO, f"capítulo 5 (autoevaluación) contiene «{aguja}»", True)


def BOOL_(tag, fn, desc):
    return Src(tag, fn, desc, True)


def DEF_(desc):
    return Src("DEF", lambda: True, desc, True)


def WEB_(desc):
    """Comprobación manual en una fuente pública que no está en el repositorio (con fecha). No la repite ningún guion."""
    return Src("WEB", lambda: True, desc, True)


class Claim:
    def __init__(self, slide, shown, srcs, kind="dato", tol=None, nota=""):
        self.slide, self.shown, self.srcs, self.kind, self.tol, self.nota = slide, shown, srcs, kind, tol, nota
        self.resultados = []
        self.estado = ""


CLAIMS: list[Claim] = []
ALLOW: dict[str, dict[str, str]] = defaultdict(dict)
SIN_VERIFICAR: list[tuple[str, str, str]] = []


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
    s = shown.replace("%", "").replace("+", "").replace("−", "-").strip()
    esperado = float(s)
    if tol is not None:
        return abs(float(valor) - esperado) <= tol
    dec = len(s.split(".")[1]) if "." in s else 0
    v = float(valor)
    redondeado = round(v + math.copysign(1e-9, v), dec)
    return abs(redondeado - esperado) < 1e-9


def empate(shown: str, v) -> bool:
    """¿Redondear v (ya redondeado en su JSON) a los decimales mostrados es un empate a la mitad?
    Entonces el valor publicado no decide el redondeo y hace falta el exacto (R, PY o CALC)."""
    s = shown.replace("%", "").replace("+", "").replace("−", "-").strip()
    dec = len(s.split(".")[1]) if "." in s else 0
    x = abs(float(v)) * 10 ** dec
    return abs(x - math.floor(x) - 0.5) < 1e-9


def evalua(c: Claim):
    c.resultados = []
    for s in c.srcs:
        try:
            v = s.valor()
            ok = bool(v) if s.booleana else coincide(c.shown, v, c.tol)
        except Exception as e:  # noqa: BLE001
            v, ok = f"ERROR {type(e).__name__}: {e}", False
        c.resultados.append((s, ok, v))
    exactas = [s for s, _, _ in c.resultados if s.tag in ("R", "PY", "CALC") and not s.booleana]
    exacta_ok = any(ok for s, ok, _ in c.resultados if s in exactas)
    # En un empate, el valor publicado admite los dos redondeos: decide la fuente exacta.
    for i, (s, ok, v) in enumerate(c.resultados):
        if (not ok and exacta_ok and s.tag in ("J", "J4", "J3") and isinstance(v, (int, float))
                and empate(c.shown, v) and coincide(c.shown, abs(v) - 1e-6 if v > 0 else v + 1e-6, c.tol)):
            c.resultados[i] = (Src(s.tag, s.fn, s.desc + " (empate: decide el exacto)"), True, v)
    if c.tol is None and not exactas:
        for s, ok, v in list(c.resultados):
            if s.tag in ("J", "J4", "J3") and not s.booleana and isinstance(v, (int, float)) and empate(c.shown, v):
                c.resultados.append((Src("EMPATE", lambda: None, "el valor publicado cae en la mitad: hace falta el exacto"), False, v))
    return all(ok for _, ok, _ in c.resultados) and len(c.resultados) > 0


# atajos
AIR = "airpassengers.airline"
COMB = "airpassengers.combinaciones"
FIR = "airpassengers.firma"
TEO = "teoricas"
REJ = "airpassengers.rejilla"
COMP = "airpassengers.comparativa"
OM = "airpassengers.comparativa.origen_movil"
CAL = "airpassengers.calendario"
FOU = "airpassengers.fourier"
SOB = "airpassengers.sobrediferenciacion_estacional"
DIAG = AIR + ".diagnostico"
PRON = "airpassengers.pronostico"
TRMC = "trm_contraejemplo"
UA = "usaccdeaths"
PUENTE = "puente_estacional.no_estacional"
CR = lambda y: CALC_(lambda: 100 * math.log(R["m11"]["crecimiento_anual"][str(y)] / 100 + 1), f"100·log(1 + crecimiento {y}) desde directo_cap5.json")  # noqa: E731


def crec_log(clave, campo):
    return CALC_(lambda: 100 * math.log(1 + R["m11"][clave][campo] / 100), f"100·log(1 + {clave}.{campo}/100) desde directo_cap5.json")


def ANI_(nombre):
    return BOOL_("CALC", lambda: (AQUI.parent / "recursos/cap5" / nombre).read_text(encoding="utf-8") == GEN.texto(GEN.construye()[nombre]),
                 f"recursos/cap5/{nombre} es idéntico a lo que genera genera_animados_cap5.py desde J")


# ===========================================================================
# REGISTRO DE CLAIMS, diapositiva por diapositiva (la clave es un trozo del título)
# ===========================================================================

# ---- Leyenda --------------------------------------------------------------------
K = "Cada afirmación es un dato"
C(K, "24", J_("horizonte"), kind="horizonte")
sin_verificar(K, "origen de la TRM · nombre y difusión del airline · tabla de métodos modernos · secciones de las lecturas",
              "ver la lista en las notas y en este informe")

# ---- M1 -------------------------------------------------------------------------
permite("Clase 1 · Módulo 1", "12 24", "rezagos")
permite("Módulo 2 · Notación SARIMA", "12", "rezago")
permite("Módulos 10–11 ·", "11 12", "número de módulo y m")
permite("Los satélites no piden parámetros", "11 12 13", "rezagos")
K = "El capítulo 4 dejó toda la estructura"
permite(K, "12 24 36", "rezagos")
C(K, "0.7245", J4_(PUENTE + ".acf_12"))
C(K, "0.6727", J4_(PUENTE + ".acf_24"))
C(K, "0.163", J4_(PUENTE + ".banda"), CALC_(lambda: banda(144), "1.96/√144"))
C(K, "222.4", J4_(PUENTE + ".ljung_box_24.Q"))
C(K, "-0.0515", J_(DIAG + ".acf.11"), R_("m7.res_r12"))
C(K, "0.233", J_(DIAG + ".lb24_p"), R_("m7.lb24"))
C(K, "1949", R_("datos.ap_inicio"), DOC_("airpassengers", "1949 to 1960"))
C(K, "1960", R_("datos.ap_fin"), DOC_("airpassengers", "1949 to 1960"))
C(K, "144", R_("datos.ap_n"), J_("airpassengers.n"))
C(K, "143", CALC_(lambda: 144 - 1, "n − d con d = 1"))
C(K, "131", J_(AIR + ".nobs"), R_("m2.n_w"))

K = "Cuatro series conducen"
for y, src in ((1949, R_("datos.ap_inicio")), (1960, R_("datos.ap_fin")), (1973, R_("datos.uad_inicio")),
               (1978, R_("datos.uad_fin")), (1959, R_("datos.co2_inicio")), (1997, R_("datos.co2_fin"))):
    C(K, str(y), src)
C(K, "144", R_("datos.ap_n"))
C(K, "72", R_("datos.uad_n"), J_("usaccdeaths.n"))
C(K, "468", R_("datos.co2_n"), DOC_("co2", "468 observations"))
C(K, "138", R_("datos.trm_n"), J_(TRMC + ".n"))
C(K, "2015", BOOL_("R", lambda: R["datos"]["trm_inicio"] == "2015-1", "directo_cap5.json › datos.trm_inicio = 2015-1"))
C(K, "2026", BOOL_("R", lambda: R["datos"]["trm_fin"] == "2026-6", "directo_cap5.json › datos.trm_fin = 2026-6"))
C(K, "1994", DOC_("airpassengers", "Reinsel GC (1994)"), kind="documentación")
C(K, "1991", DOC_("usaccdeaths", "Davis RA (1991)"), kind="documentación")
for k in ("ap_igual_datasets", "uad_igual_datasets", "co2_igual_datasets"):
    C(K, "R", BOOL_("R", lambda k=k: R["datos"][k], f"directo_cap5.json › datos.{k}"), kind="datos = datasets de R")
sin_verificar(K, "origen de la TRM en datos.gov.co", "solo se comprobó la copia congelada de datos_series.json")

K = "La estacionalidad tiene un periodo fijado"
C(K, "11.22", J3_("manchas.transformacion.sqrt.periodo"), CH_("11.22"))
C(K, "11.2178", J3_("manchas.transformacion.sqrt.periodo"))
permite(K, "12 52 11", "definición: m = 12 mensual, 52 semanal; m = 11 del ejemplo de las notas")

K = "Con datos mensuales la estacionalidad está en 12"
C(K, "0.762", J_(FIR + ".airpassengers_log.acf.11"), CALC_(lambda: acf(LAP, 12), "ACF de log(AirPassengers), rezago 12"))
C(K, "0.520", J_(FIR + ".airpassengers_log.acf.23"), CALC_(lambda: acf(LAP, 24), "rezago 24"))
C(K, "0.521", CH_("0.521"), kind="capítulo (doble redondeo)")
C(K, "0.5205", J_(FIR + ".airpassengers_log.acf.23"))
C(K, "0.52049", CALC_(lambda: acf(LAP, 24), "ACF exacta en 24"))
C(K, "0.319", J_(FIR + ".airpassengers_log.acf.35"), CALC_(lambda: acf(LAP, 36), "rezago 36"))
C(K, "0.163", J_(FIR + ".airpassengers_log.banda"), CALC_(lambda: banda(144), "1.96/√144"))
C(K, "144", R_("datos.ap_n"))
C(K, "1.96", DEF_("cuantil 0.975 de la normal"), kind="convención")
permite(K, "12 24 36 20", "rezagos (convención del capítulo: 3m = 36; 20 o 24 por defecto)")

K = "Cuatro filas se parecen"
FILAS = [("airpassengers_log", LAP, ["0.954", "0.762", "0.520", "0.319"], "0.163", 144),
         ("usaccdeaths", UAD, ["0.707", "0.629", "0.450", "0.302"], "0.231", 72),
         ("co2", CO2, ["0.991", "0.928", "0.855", "0.783"], "0.091", 468),
         ("trm", TRM, ["0.964", "0.636", "0.490", "0.225"], "0.167", 138),
         ("trm_diff", DTRM, ["0.088", "-0.002", "-0.067", "0.071"], "0.167", 137)]
for clave, x, vals, b, n in FILAS:
    for k, v in zip((1, 12, 24, 36), vals):
        C(K, v, CALC_(lambda x=x, k=k: acf(x, k), f"ACF de {clave} en el rezago {k}, desde datos_series.json"),
          J_(f"{FIR}.{clave}.acf.{k - 1}") if not (clave == "usaccdeaths" and k == 1) else CALC_(lambda x=x: acf(x, 1), "ídem"))
    C(K, b, CALC_(lambda n=n: banda(n), f"1.96/√{n}"))
C(K, "0.16745", CALC_(lambda: banda(137), "1.96/√137"))
C(K, "0.1675", J_(FIR + ".trm_diff.banda"))
C(K, "137", J_(FIR + ".trm_diff.n"))
C(K, "1.96", DEF_("cuantil 0.975 de la normal"), kind="convención")
for v, x, k in (("0.52049", LAP, 24), ("0.70747", UAD, 1), ("0.85546", CO2, 24), ("0.63649", TRM, 12)):
    C(K, v, CALC_(lambda x=x, k=k: acf(x, k), f"ACF exacta en {k}"))
for v in ("0.521", "0.708", "0.856", "0.637", "-0.003"):
    C(K, v, CH_(v.lstrip("-")), kind="capítulo (doble redondeo)")
permite(K, "12", "múltiplos de 12")
C(K, "-0.00245", CALC_(lambda: acf(DTRM, 12), "ACF de ∇TRM en 12"), R_("m1.trm_diff.1"))
C(K, "-0.0024", CH_("-0.0024"), kind="capítulo (código en vivo)")
C(K, "-0.0025", J_(TRMC + ".acf12"))

K = "Es estacional una serie con"
C(K, "0.636", J_(FIR + ".trm.acf.11"), CALC_(lambda: acf(TRM, 12), "ACF de la TRM en 12"))
C(K, "0.637", CHQ_("0.637"), kind="capítulo (doble redondeo)")
C(K, "0.6365", J_(FIR + ".trm.acf.11"))
C(K, "0.63649", CALC_(lambda: acf(TRM, 12), "ACF exacta de la TRM en 12"))
C(K, "138", R_("datos.trm_n"))
C(K, "0.167", CALC_(lambda: banda(138), "1.96/√138"), J_(FIR + ".trm.banda"))
C(K, "0.964", J_(FIR + ".trm.acf.0"), CALC_(lambda: acf(TRM, 1), "rezago 1"))
C(K, "0.225", J_(FIR + ".trm.acf.35"), CALC_(lambda: acf(TRM, 36), "rezago 36"))
C(K, "-0.0025", J_(TRMC + ".acf12"))
C(K, "-0.067", J_(TRMC + ".acf24"), CALC_(lambda: acf(DTRM, 24), "∇TRM, 24"))
C(K, "0.071", J_(TRMC + ".acf36"), CALC_(lambda: acf(DTRM, 36), "∇TRM, 36"))
C(K, "1.96", DEF_("cuantil 0.975 de la normal, convención"), kind="convención")
permite(K, "12", "múltiplos de 12 (rezagos)")

K = "Ver y medir la estacionalidad cabe"
permite(K, "13 12", "posición del rezago 12 en a$acf (convención de R)")

# ---- M2 -------------------------------------------------------------------------
K = "Multiplicar no es sumar"
permite(K, "13 12 11", "rezagos del polinomio (definición)")

K = "brotan satélites en 11 y 13"
C(K, "0.4230", J_(TEO + ".ar1_sar1.acf.10"), R_("m4.ar1_sar1.r11"))
C(K, "0.4218", J_(TEO + ".ar1_sar1.acf.12"), R_("m4.ar1_sar1.r13"))
C(K, "0.6016", J_(TEO + ".ar1_sar1.acf.0"), R_("m4.ar1_sar1.r1"))
C(K, "0.7011", J_(TEO + ".ar1_sar1.acf.11"), R_("m4.ar1_sar1.r12"))
C(K, "0.42298", R_("m4.ar1_sar1.r11"))
C(K, "0.42180", R_("m4.ar1_sar1.r13"), R_("m4.ar1_sar1.producto"))
C(K, "0.6", DEF_("φ del capítulo"), kind="parámetro")
C(K, "0.7", DEF_("Φ del capítulo"), kind="parámetro")
C(K, "animado", ANI_("satelites.json"), kind="gráfico animado")
permite(K, "11 13 12 24 36", "rezagos")

K = "En un MA puro con"
C(K, "1.5217", R_("m2.factor_airline"))
C(K, "0.001371", J_(AIR + ".sigma2"), R_("m2.sigma2"))
C(K, "0.002087", R_("m2.gamma0_airline"))
C(K, "0.002102", J_(COMB + ".d1_D1.varianza"), R_("m2.var_muestral_w"))
C(K, "131", J_(COMB + ".d1_D1.n"), R_("m2.n_w"))
C(K, "0.5", DEF_("θ₁₂ del ejemplo del capítulo"), kind="parámetro")
C(K, "0.6", DEF_("Θ del ejemplo del capítulo"), kind="parámetro")
C(K, "2.300", R_("m2.choque_exacta"))
C(K, "1.700", R_("m2.choque_factorizada"))
C(K, "0.00137126", R_("m2.sigma2"))
permite(K, "12 13", "rezagos de los pesos")

K = "Con parte AR no hay factorización"
for i, (phi, p12, ex, fa, er) in enumerate((("0.6", "0.002", "3.073", "3.064", "-0.3"), ("0.8", "0.069", "5.997", "5.447", "-9.2"),
                                             ("0.9", "0.282", "15.406", "10.320", "-33.0"), ("0.95", "0.540", "44.580", "20.111", "-54.9"))):
    C(K, phi, R_(f"m2.tabla_phi.{i}.phi"), kind="parámetro")
    C(K, p12, R_(f"m2.tabla_phi.{i}.phi12"))
    C(K, ex, R_(f"m2.tabla_phi.{i}.exacta"))
    C(K, fa, R_(f"m2.tabla_phi.{i}.factorizada"))
    C(K, er, R_(f"m2.tabla_phi.{i}.error_pct"))
C(K, "33", R_("m2.tabla_phi.2.error_pct", -1))
C(K, "0.7", DEF_("Φ fijo del capítulo"), kind="parámetro")
C(K, "20000", DEF_("número de pesos ψ que suma verifica_directo_cap5.R"), kind="cálculo")
permite(K, "12", "rezago")

K = "SARIMA(1,0,0)(1,0,0)"
C(K, "0.364", J_(TEO + ".ar1_sar1.acf.1"))
C(K, "0.3637", J_(TEO + ".ar1_sar1.acf.1"))
C(K, "0.3619", CALC_(lambda: get(J, TEO + ".ar1_sar1.acf.0") ** 2, "ρ₁² con ρ₁ de J"))
C(K, "0.36", CHQ_("0.36"))
C(K, "0.6", DEF_("φ"), kind="parámetro")
C(K, "0.7", DEF_("Φ"), kind="parámetro")
permite(K, "13 11", "rezagos")

K = "En R el periodo va en"
C(K, "0.2238", R_("m2.coef_b13"),
  CALC_(lambda: get(J, AIR + ".coeficientes.0.valor") * get(J, AIR + ".coeficientes.1.valor"), "θ·Θ con J"))
permite(K, "13", "rezagos que toca la forma no multiplicativa (1 a 13)")

# ---- M3–M4 ----------------------------------------------------------------------
K = "compara enero con enero"
permite(K, "12 11", "orden del operador y número de raíces (definición)")

K = "Cada operador hace su trabajo"
C(K, "0.762", J_(COMB + ".d0_D0.acf12"))
C(K, "0.841", J_(COMB + ".d1_D0.acf12"))
C(K, "0.714", J_(COMB + ".d0_D1.acf1"))
C(K, "0.002102", J_(COMB + ".d1_D1.varianza"), R_("m3.ap_var.3"))
for n, c in (("144", "d0_D0"), ("143", "d1_D0"), ("132", "d0_D1"), ("131", "d1_D1")):
    C(K, n, J_(f"{COMB}.{c}.n"))
C(K, "0.20", J_(COMB + ".d1_D0.acf1"))
C(K, "0.71", J_(COMB + ".d0_D1.acf1"))
C(K, "17.2", CALC_(lambda: get(J, COMB + ".d0_D0.varianza") / get(J, COMB + ".d1_D0.varianza"), "0.194884/0.011354"))
C(K, "51.3", CALC_(lambda: get(J, COMB + ".d0_D0.varianza") / get(J, COMB + ".d0_D1.varianza"), "0.194884/0.003800"))
C(K, "animado", ANI_("diferencias.json"), kind="gráfico animado")
permite(K, "12", "rezago")

K = "da 0 en la serie cruda y 1 tras"
C(K, "0.8672", PY_("kpss_uad_D1"))
C(K, "0.463", PY_("kpss_critico_5"))
C(K, "0.0713", PY_("kpss_uad_d1D1"))
C(K, "5", DEF_("nivel de la prueba"), kind="convención")
C(K, "-0.4303", J_(UA + ".coeficientes.0.valor"), PY_("uad_simple.ma1"))
C(K, "1973", R_("datos.uad_inicio"))
C(K, "1978", R_("datos.uad_fin"))
C(K, "72", R_("datos.uad_n"))

K = "Los operadores conmutan"
permite(K, "12", "rezago")

K = "Diferenciar de más deja la firma"
for i, (n, var, th, ee, rz) in enumerate((("143", "0.011354", "0.7397", "0.0610", "0.9752"), ("131", "0.002102", "-0.5569", "0.0731", "0.9524"),
                                          ("119", "0.005960", "-0.9973", "0.0830", "0.9998"))):
    C(K, n, J_(f"{SOB}.{i}.n"))
    C(K, var, J_(f"{SOB}.{i}.varianza"))
    C(K, th, J_(f"{SOB}.{i}.theta_est"))
    C(K, ee, J_(f"{SOB}.{i}.ee"))
    C(K, rz, J_(f"{SOB}.{i}.raiz_ma"))
C(K, "58", CH_("58"), kind="capítulo (lynx, del capítulo 4)")
permite(K, "12", "rezago")

K = "cambió de prueba por defecto"
C(K, "8.3", BOOL_("DOC", lambda: DOCS["news_cambio_D"]["version"] == "8.3", "docs_cap5.json › news_cambio_D.version = 8.3"),
  BOOL_("DOC", lambda: DOCS["nsdiffs_test_por_defecto"] == "seas", "formals(nsdiffs)$test empieza por \"seas\""), kind="documentación")
TABLA_PRUEBAS = {"airpassengers": [1, 1, 1, 0], "usaccdeaths": [0, 1, 1, 0], "co2": [1, 1, 1, 1], "trm": [1, 1, 0, 0]}
PRUEBAS = ("ndiffs_crudo", "ndiffs_tras_D", "nsdiffs_seas", "nsdiffs_ocsb")
C(K, "tabla", BOOL_("J", lambda: all([get(J, f"airpassengers.orden_pruebas.{s}.{c}") for c in PRUEBAS] == v for s, v in TABLA_PRUEBAS.items()),
                    "las 16 celdas de la tabla = orden_pruebas de J"), kind="tabla (enteros < 10)")
C(K, "9.0.2", BOOL_("DOC", lambda: DOCS["entorno"]["forecast"] == "9.0.2", "docs_cap5.json › entorno.forecast"), kind="versión")
permite(K, "12", "rezago")

K = "Los rezagos estacionales se leen"
C(K, "0.700", J_(TEO + ".sar1_pos.acf.11"), R_("m4.sar1.r12"))
C(K, "0.490", J_(TEO + ".sar1_pos.acf.23"), R_("m4.sar1.r24"))
C(K, "0.343", J_(TEO + ".sar1_pos.acf.35"), R_("m4.sar1.r36"))
C(K, "-0.4412", J_(TEO + ".sma1.acf.11"), R_("m4.sma1.r12"))
C(K, "0.7", DEF_("Φ"), kind="parámetro")
C(K, "-0.6", DEF_("Θ"), kind="parámetro")
permite(K, "12 24 36 11", "rezagos")

K = "En el *airline* el producto es exacto"
for fila, clave, vals in (("ar1_sar1", "ar1_sar1", ["0.602", "0.423", "0.701", "0.422", "0.491"]),
                          ("airline", "airline", ["-0.346", "0.147", "-0.425", "0.147", None]),
                          ("ar1_sma1", "ar1_sma1", ["0.500", "-0.234", "-0.470", "-0.235", None])):
    for v, campo in zip(vals, ("r1", "r11", "r12", "r13", "r24")):
        if v:
            C(K, v, R_(f"m4.{clave}.{campo}"))
C(K, "0.4018", J_(AIR + ".coeficientes.0.valor", -1))
C(K, "-0.4018", J_(AIR + ".coeficientes.0.valor"))
C(K, "-0.5569", J_(AIR + ".coeficientes.1.valor"))
C(K, "0.42298", R_("m4.ar1_sar1.r11"))
C(K, "0.42180", R_("m4.ar1_sar1.r13"))
C(K, "-0.23446", R_("m4.ar1_sma1.r11"))
C(K, "-0.23483", R_("m4.ar1_sma1.r13"))
C(K, "0.14707", R_("m4.airline.r11"))
C(K, "0.14705", R_("m4.airline_redondeado.r11"), CH_("0.14705"))
C(K, "0.1471", R_("m4.airline.producto"))
C(K, "0.6", DEF_("φ"), kind="parámetro")
C(K, "0.7", DEF_("Φ"), kind="parámetro")
C(K, "0.5", DEF_("φ"), kind="parámetro")
C(K, "-0.7", DEF_("Θ"), kind="parámetro")
permite(K, "12 11 13 24", "rezagos")

K = "Picos de 0.70, 0.49 y 0.34"
C(K, "0.70", J_(TEO + ".sar1_pos.acf.11"))
C(K, "0.49", J_(TEO + ".sar1_pos.acf.23"))
C(K, "0.34", J_(TEO + ".sar1_pos.acf.35"))
C(K, "0.7", DEF_("Φ = 0.7"), kind="parámetro")
permite(K, "12 24 36 11 13", "rezagos")


# ---- M5 -------------------------------------------------------------------------
K = "dos diferencias y dos MA para una serie"
C(K, "Box & Jenkins airline", DOC_("airpassengers", "The classic Box & Jenkins airline data"), kind="documentación")
C(K, "airline model", DOC_("airpassengers", "The classic 'airline model'"), kind="documentación")
C(K, "log10", DOC_("airpassengers", "log10(AirPassengers)"), kind="documentación")
sin_verificar(K, "que Box y Jenkins lo bautizaran así · «el SARIMA más usado del mundo»", "el libro no está en el repositorio; afirmación del capítulo")
permite(K, "12", "periodo")

K = "Dos series sin nada en común"
C(K, "144", J_("airpassengers.n"))
C(K, "72", J_("usaccdeaths.n"))
C(K, "-0.4018", J_(AIR + ".coeficientes.0.valor"))
C(K, "-0.5569", J_(AIR + ".coeficientes.1.valor"))
C(K, "-0.4303", J_(UA + ".coeficientes.0.valor"))
C(K, "-0.5528", J_(UA + ".coeficientes.1.valor"))
C(K, "auto", BOOL_("J", lambda: get(J, "airpassengers.auto_arima.exhaustivo") == "ARIMA(0,1,1)(0,1,1)[12]" and get(J, "usaccdeaths.auto_arima") == "ARIMA(0,1,1)(0,1,1)[12]", "auto.arima exhaustivo = airline en las dos"), kind="modelo")
for y, src in ((1949, R_("datos.ap_inicio")), (1960, R_("datos.ap_fin")), (1973, R_("datos.uad_inicio")), (1978, R_("datos.uad_fin"))):
    C(K, str(y), src)
permite(K, "12", "periodo")

K = "Los pesos \\(\\psi\\) suben a escalones"
C(K, "0.5982", J_(PRON + ".psi.1"), CALC_(lambda: 1 + R["m2"]["theta"], "1 + θ̂ (R)"))
C(K, "1.0412", J_(PRON + ".psi.12"))
C(K, "0.8632", J_(PRON + ".psi.13"))
C(K, "0.0370", J_(PRON + ".sigma_h.0"))
C(K, "0.0823", J_(PRON + ".sigma_h.11"))
C(K, "0.1396", J_(PRON + ".sigma_h.23"))
C(K, "1.0413", CALC_(lambda: 2 - 0.4018 - 0.5569, "ψ₁₂ = 2 + θ + Θ con los coeficientes redondeados"), CH_("1.0413"))
C(K, "0.8633", CALC_(lambda: 2 - 2 * 0.4018 - 0.5569 + 0.4018 * 0.5569, "ψ₁₃ = 2 + 2θ + Θ + θΘ, redondeados"), CH_("0.8633"))
C(K, "animado", ANI_("escalones.json"), kind="gráfico animado")
permite(K, "12 11 13 23", "índices j de los pesos")

K = "acumula incertidumbre más despacio"
C(K, "2.22", CALC_(lambda: get(J, PRON + ".sigma_h.11") / get(J, PRON + ".sigma_h.0"), "σ₁₂/σ₁ (J)"))
C(K, "3.46", CALC_(lambda: math.sqrt(12), "√12"))
C(K, "0.082270", J_(PRON + ".sigma_h.11"))
C(K, "0.037031", J_(PRON + ".sigma_h.0"))
C(K, "3.4641", CALC_(lambda: math.sqrt(12), "√12"))
C(K, "0.169", J4_("nilo.intervalos.psi_limite"))
permite(K, "12", "rezago")

K = "Un *airline* sobre 96 meses"
C(K, "96", DEF_("enunciado de la pregunta 3"), kind="enunciado")
C(K, "83", CALC_(lambda: 96 - 1 - 12, "96 − 1 − 12"), CH_("83"))
permite(K, "12", "D·m")

K = "Lo que se llevan de la clase 1"
K = "Para la próxima clase"
C(K, "36", CALC_(lambda: len(get(J, REJ)), "número de modelos de la rejilla (J)"), CALC_(lambda: 3 * 3 * 2 * 2, "3 × 3 × 2 × 2"))

# ---- M6–M7 ----------------------------------------------------------------------
K = "Donde quedamos"
C(K, "-0.0515", J_(DIAG + ".acf.11"))
C(K, "0.7245", J4_(PUENTE + ".acf_12"))
permite(K, "12", "rezagos")

K = "Dos hábitos nuevos"
C(K, "143", J_(SOB + ".0.n"))
C(K, "131", J_(SOB + ".1.n"))
C(K, "24", CALC_(lambda: 2 * 12, "2m con m = 12"), kind="convención")
C(K, "20", DEF_("rezagos del ejemplo del capítulo"), kind="convención")
C(K, "10", DEF_("rezagos del ejemplo del capítulo"), kind="convención")
permite(K, "12", "rezago")

K = "En la rejilla de 36 modelos"
FILAS_REJ = [("(0,1,1)(0,1,1)[12]", "-483.21", "-474.77", "0.2330", "-0.0515"),
             ("(2,1,1)(0,1,1)[12]", "-481.79", "-467.90", "0.1371", "-0.0307"),
             ("(0,1,1)(1,1,1)[12]", "-481.60", "-470.41", "0.2271", "-0.0163"),
             ("(1,1,1)(0,1,1)[12]", "-481.58", "-470.40", "0.2453", "-0.0459"),
             ("(0,1,0)(0,1,0)[12]", "-434.80", "-431.95", None, "-0.3907")]
for mod, aicc, bic, lb, r12 in FILAS_REJ:
    C(K, aicc, J_(f"{REJ}.{mod}.aicc"))
    C(K, bic, J_(f"{REJ}.{mod}.bic"))
    if lb:
        C(K, lb, J_(f"{REJ}.{mod}.lb_p"))
    C(K, r12, J_(f"{REJ}.{mod}.acf12"))
C(K, "0.0001", BOOL_("J", lambda: get(J, f"{REJ}.(0,1,0)(0,1,0)[12].lb_p") < 0.0001, "LB p del (0,1,0)(0,1,0) < 0.0001"), kind="cota")
permite(K, "24", "rezagos de Ljung–Box")
C(K, "36", CALC_(lambda: len(get(J, REJ)), "modelos en la rejilla"))
C(K, "131", BOOL_("J", lambda: {v["nobs"] for v in get(J, REJ).values()} == {131}, "nobs = 131 en los 36"), kind="dato")
C(K, "1.7", CALC_(lambda: get(J, f"{REJ}.(1,1,1)(0,1,1)[12].aicc") - get(J, f"{REJ}.(0,1,1)(0,1,1)[12].aicc"), "distancia del 4.º al 1.º"), tol=0.1, nota="«a menos de 1.7»: 1.63")
C(K, "1.63", CALC_(lambda: get(J, f"{REJ}.(1,1,1)(0,1,1)[12].aicc") - get(J, f"{REJ}.(0,1,1)(0,1,1)[12].aicc"), "−481.582 − (−483.210)"))
C(K, "144", J_(DIAG + ".n_residuales"))
permite(K, "12", "periodo")

K = "statsmodels no diferencia la serie"
C(K, "144", PY_("ap_difuso.nobs"))
C(K, "131", PY_("ap_simple.nobs"), J_(AIR + ".nobs"))
C(K, "72", J_("usaccdeaths.n"))
C(K, "-0.4303", J_(UA + ".coeficientes.0.valor"), PY_("uad_simple.ma1"))
C(K, "-0.3924", PY_("uad_difuso.ma1"))
C(K, "-0.5475", PY_("uad_difuso.sma1"))
C(K, "-0.5527", PY_("uad_simple.sma1"))
C(K, "2.4", CALC_(lambda: PY["ap_dif_max_coef"] * 1e4, "diferencia máxima × 10⁴ (PY)"))
permite(K, "10", "exponente de 6×10⁻⁵ y 2.4×10⁻⁴")

K = "Pasos 0 y 1 del caso"
C(K, "1.848", R_("m7.rango_relativo"), CH_("1.848"))
C(K, "0.762", J_(FIR + ".airpassengers_log.acf.11"))
C(K, "0.520", J_(FIR + ".airpassengers_log.acf.23"), CALC_(lambda: acf(LAP, 24), "ACF exacta en 24"))
C(K, "0.521", CH_("0.521"), kind="capítulo (doble redondeo)")
C(K, "0.52049", CALC_(lambda: acf(LAP, 24), "ACF exacta en 24"))
C(K, "0.319", J_(FIR + ".airpassengers_log.acf.35"))
C(K, "0.714", J_(COMB + ".d0_D1.acf1"))
C(K, "0.002102", J_(COMB + ".d1_D1.varianza"))
C(K, "0.003800", J_(COMB + ".d0_D1.varianza"))
C(K, "0.011354", J_(COMB + ".d1_D0.varianza"))
C(K, "622", CALC_(lambda: max(AP), "máximo de AirPassengers"))
C(K, "104", CALC_(lambda: min(AP), "mínimo de AirPassengers"))
C(K, "280.30", CALC_(lambda: sum(AP) / len(AP), "media de AirPassengers"))
C(K, "1949", R_("datos.ap_inicio"))
C(K, "1960", R_("datos.ap_fin"))
permite(K, "12 24 36", "rezagos")

K = "Paso 2: un pico en 1"
C(K, "-0.341", J_(COMB + ".d1_D1.acf1"), R_("m7.r1"))
C(K, "-0.387", J_(COMB + ".d1_D1.acf12"), R_("m7.r12"))
C(K, "0.171", R_("m7.banda_w"))
C(K, "0.1712", R_("m7.banda_w"))
C(K, "131", R_("m7.n_w"))
C(K, "144", R_("datos.ap_n"))
C(K, "-0.202", J_(COMB + ".d1_D1.acf.2"), R_("m7.r3"))
C(K, "0.176", J_(COMB + ".d1_D1.acf.8"), R_("m7.r9"))
C(K, "0.223", J_(COMB + ".d1_D1.acf.22"), R_("m7.r23"))
C(K, "95", DEF_("nivel de la banda"), kind="convención")
C(K, "24", DEF_("rezagos mirados"), kind="convención")
C(K, "1.96", DEF_("cuantil 0.975 de la normal"), kind="convención")
permite(K, "12 23", "rezagos")

K = "En 11 y 13 aparecen 0.064 y 0.152"
C(K, "0.064", J_(COMB + ".d1_D1.acf.10"), R_("m7.r11"))
C(K, "0.152", J_(COMB + ".d1_D1.acf.12"), R_("m7.r13"))
C(K, "0.171", R_("m7.banda_w"))
C(K, "0.0644", J_(COMB + ".d1_D1.acf.10"))
C(K, "0.1516", J_(COMB + ".d1_D1.acf.12"))
C(K, "0.06438", R_("m7.r11"))
C(K, "0.15160", R_("m7.r13"))
permite(K, "11 13", "rezagos")

K = "Paso 3: los dos coeficientes"
C(K, "-0.4018", J_(AIR + ".coeficientes.0.valor"))
C(K, "0.0896", J_(AIR + ".coeficientes.0.ee"), R_("m7.ee.0"))
C(K, "-4.48", J_(AIR + ".coeficientes.0.t"), R_("m7.t.0"))
C(K, "-0.5569", J_(AIR + ".coeficientes.1.valor"))
C(K, "0.0731", J_(AIR + ".coeficientes.1.ee"), R_("m7.ee.1"))
C(K, "-7.62", J_(AIR + ".coeficientes.1.t"), R_("m7.t.1"))
C(K, "0.2330", J_(DIAG + ".lb24_p"), R_("m7.lb24"))
C(K, "0.2969", J_(DIAG + ".lb36_p"), R_("m7.lb36"))
C(K, "0.1674", J_(DIAG + ".shapiro_p"), R_("m7.shapiro"))
C(K, "-0.0515", J_(DIAG + ".acf.11"), R_("m7.res_r12"))
C(K, "0.0124", J_(DIAG + ".acf.23"), R_("m7.res_r24"))
C(K, "0.163", R_("m7.banda_res"))
C(K, "0.9524", J_(AIR + ".raices.ma_max"), R_("m7.raiz_ma"))
C(K, "0.001371", J_(AIR + ".sigma2"))
C(K, "131", J_(AIR + ".nobs"))
C(K, "0.9998", J_(SOB + ".2.raiz_ma"))
permite(K, "24 36", "rezagos de Ljung–Box")

K = "En los residuales solo el rezago 23"
C(K, "-0.125", J_(DIAG + ".acf.2"), R_("m7.res_r3"))
C(K, "0.117", J_(DIAG + ".acf.8"), R_("m7.res_r9"))
C(K, "0.220", J_(DIAG + ".acf.22"), R_("m7.res_r23"))
C(K, "0.163", R_("m7.banda_res"))
C(K, "0.1633", R_("m7.banda_res"))
C(K, "1.96", DEF_("cuantil 0.975 de la normal"), kind="convención")
C(K, "0.233", J_(DIAG + ".lb24_p"))
C(K, "144", J_(DIAG + ".n_residuales"))
permite(K, "23 24", "rezagos")

K = "Los satélites, comprobados"
C(K, "0.1471", R_("m4.airline.producto"), J_(TEO + ".ma1_sma1.acf.10"))
C(K, "0.064", J_(COMB + ".d1_D1.acf.10"))
C(K, "0.152", J_(COMB + ".d1_D1.acf.12"))
C(K, "-0.3460", R_("m4.airline.r1"))
C(K, "-0.341", J_(COMB + ".d1_D1.acf1"))
C(K, "-0.4251", R_("m4.airline.r12"), J_(TEO + ".ma1_sma1.acf.11"))
C(K, "-0.387", J_(COMB + ".d1_D1.acf12"))
C(K, "131", R_("m7.n_w"))
C(K, "0.087", R_("m7.ee_aprox"))
C(K, "0.0874", R_("m7.ee_aprox"))
C(K, "-0.34597", R_("m4.airline.r1"))
C(K, "-0.42509", R_("m4.airline.r12"))
C(K, "0.14707", R_("m4.airline.r11"))
C(K, "-0.3459", J_(TEO + ".ma1_sma1.acf.0"))
permite(K, "11 13 12", "rezagos")

K = "Paso 4: exp() del pronóstico"
C(K, "525.46", J_(PRON + ".original.media.23"), R_("m7.pron24.0"))
C(K, "399.66", J_(PRON + ".original.lo95.23"), R_("m7.pron24.1"))
C(K, "690.85", J_(PRON + ".original.hi95.23"), R_("m7.pron24.2"))
C(K, "126", CALC_(lambda: 525.46 - 399.66, "525.46 − 399.66"))
C(K, "165", CALC_(lambda: 690.85 - 525.46, "690.85 − 525.46"))
C(K, "125.80", CALC_(lambda: 525.46 - 399.66, "525.46 − 399.66"))
C(K, "165.39", CALC_(lambda: 690.85 - 525.46, "690.85 − 525.46"))
C(K, "530.52", CH_("530.52"), kind="capítulo (statsmodels)")
C(K, "530.61", R_("m7.media24"))
C(K, "95", DEF_("nivel del intervalo"), kind="convención")
C(K, "80", DEF_("nivel del intervalo"), kind="convención")
C(K, "24", J_("horizonte"))
C(K, "1960", BOOL_("J", lambda: get(J, PRON + ".fechas.0") == "1961-01", "el pronóstico empieza en 1961-01"), kind="fecha")
C(K, "1962", BOOL_("J", lambda: get(J, PRON + ".fechas.23") == "1962-12", "el horizonte 24 es 1962-12"), kind="fecha")
permite(K, "12", "mes (1960-12, 1962-12)")

K = "El caso completo cabe en seis"
C(K, "26.446", J_(DIAG + ".lb24_Q"))
C(K, "24", DEF_("rezagos de Ljung–Box"), kind="convención")
C(K, "22", CALC_(lambda: 24 - 2, "24 − 2"))

# ---- M8–M9 ----------------------------------------------------------------------
K = "USAccDeaths vuelve a elegir el *airline*"
C(K, "-0.4303", J_(UA + ".coeficientes.0.valor"))
C(K, "0.1228", J_(UA + ".coeficientes.0.ee"))
C(K, "-0.5528", J_(UA + ".coeficientes.1.valor"))
C(K, "0.1784", J_(UA + ".coeficientes.1.ee"))
C(K, "857.32", J_(UA + ".aicc"))
C(K, "0.2477", J_(UA + ".diagnostico.lb24_p"))
C(K, "72", J_("usaccdeaths.n"))
C(K, "144", J_("airpassengers.n"))
C(K, "0.0896", J_(AIR + ".coeficientes.0.ee"))
C(K, "0.0731", J_(AIR + ".coeficientes.1.ee"))
permite(K, "12 24", "periodo y rezagos")

K = "La TRM es mensual y no tiene"
C(K, "-0.0025", J_(TRMC + ".acf12"))
C(K, "-0.0672", J_(TRMC + ".acf24"), CALC_(lambda: acf(DTRM, 24), "∇TRM, 24"))
C(K, "0.0714", J_(TRMC + ".acf36"), CALC_(lambda: acf(DTRM, 36), "∇TRM, 36"))
C(K, "0.167", CALC_(lambda: banda(137), "1.96/√137"))
C(K, "0.16745", CALC_(lambda: banda(137), "1.96/√137"))
C(K, "0.1675", J_(TRMC + ".banda"))
C(K, "0.0013", J_(TRMC + ".forzado.Phi"))
C(K, "0.0899", J_(TRMC + ".forzado.ee"))
C(K, "0.01", CALC_(lambda: 0.0147, "t = 0.0147 que imprime el código del capítulo"), CH_("0.0147"))

C(K, "1708.00", J_(TRMC + ".forzado.aicc"))
C(K, "1705.94", J_(TRMC + ".simple.aicc"))
C(K, "nsdiffs", BOOL_("J", lambda: get(J, TRMC + ".nsdiffs_seas") == 0 and get(J, TRMC + ".nsdiffs_ocsb") == 0, "nsdiffs = 0 con seas y con ocsb"), kind="dato")
C(K, "2015", BOOL_("R", lambda: R["datos"]["trm_inicio"] == "2015-1", "trm_inicio"))
C(K, "2026", BOOL_("R", lambda: R["datos"]["trm_fin"] == "2026-6", "trm_fin"))
C(K, "138", J_(TRMC + ".n"))
C(K, "137", J_(FIR + ".trm_diff.n"))
C(K, "1.96", DEF_("cuantil 0.975 de la normal"), kind="convención")
C(K, "auto", BOOL_("J", lambda: get(J, TRMC + ".auto") == "ARIMA(0,1,0)", "auto.arima = ARIMA(0,1,0)"), kind="modelo")
permite(K, "12 24 36", "rezagos")

K = "El SARIMA no ve lo que el calendario"
C(K, "28", DEF_("días de febrero (calendario)"), kind="calendario")
C(K, "29", DEF_("días de febrero bisiesto"), kind="calendario")
C(K, "31", DEF_("días de julio"), kind="calendario")
C(K, "22", DEF_("ejemplo del capítulo"), kind="calendario")
C(K, "23", DEF_("ejemplo del capítulo"), kind="calendario")
C(K, "rango", BOOL_("J", lambda: get(J, CAL + ".rango_dias") == [28, 31], "rango de días del mes en la serie: 28 a 31"), kind="dato")

K = "SARIMAX es una regresión"

K = "Los días del mes entran con"
C(K, "1.084", J_(CAL + ".modelos.con_dias_pascua.coeficientes.2.valor"), R_("m9.beta_dias"))
for v, ruta in (("-483.21", "sin_regresores.aicc"), ("-474.77", "sin_regresores.bic"), ("-486.54", "con_dias.aicc"), ("-475.35", "con_dias.bic"),
                ("1.1157", "con_dias.coeficientes.2.valor"), ("2.39", "con_dias.coeficientes.2.t"), ("-490.72", "con_dias_pascua.aicc"),
                ("-476.83", "con_dias_pascua.bic"), ("1.0840", "con_dias_pascua.coeficientes.2.valor"), ("2.43", "con_dias_pascua.coeficientes.2.t"),
                ("0.0290", "con_dias_pascua.coeficientes.3.valor"), ("2.60", "con_dias_pascua.coeficientes.3.t")):
    C(K, v, J_(f"{CAL}.modelos.{ruta}"))
C(K, "2.9", R_("m9.pascua_pct"), J_(CAL + ".modelos.con_dias_pascua.coeficientes.3.valor", 100))
C(K, "2.94", R_("m9.pascua_pct"))
C(K, "12", CALC_(lambda: len(get(J, CAL + ".pascuas")), "años con Pascua en la serie"))
C(K, "10", R_("m9.pascuas_abril"))
C(K, "10.7", J_(CAL + ".variacion_pct"), R_("m9.variacion_dias_pct"))
C(K, "31", DEF_("días"))
C(K, "28", DEF_("días"))

K = "Cuánto vale el \\(t\\) de"
C(K, "1.0840", J_(CAL + ".modelos.con_dias_pascua.coeficientes.2.valor"))
C(K, "0.4462", J_(CAL + ".modelos.con_dias_pascua.coeficientes.2.ee"), R_("m9.ee_dias"))
C(K, "0.188", R_("m9.t_beta1"), CALC_(lambda: (1.0840 - 1) / 0.4462, "(1.0840 − 1)/0.4462"))
C(K, "0.1883", CALC_(lambda: (1.0840 - 1) / 0.4462, "(1.0840 − 1)/0.4462"), CHQ_("0.1883"))
C(K, "0.1882", R_("m9.t_beta1"))
C(K, "0.18816", R_("m9.t_beta1"))
C(K, "0.18826", CALC_(lambda: (1.0840 - 1) / 0.4462, "(1.0840 − 1)/0.4462"))

K = "Ganar 7.5 puntos de AICc"
C(K, "7.5", R_("m9.delta_aicc"), CALC_(lambda: get(J, CAL + ".modelos.sin_regresores.aicc") - get(J, CAL + ".modelos.con_dias_pascua.aicc"), "J"))
C(K, "7.51", R_("m9.delta_aicc"))
C(K, "45.48", J_(COMP + ".modelos.sarima_calendario.rmse"))
C(K, "43.18", J_(COMP + ".modelos.sarima.rmse"))
C(K, "131", J_(AIR + ".nobs"))
C(K, "24", J_(COMP + ".n_prueba"))
C(K, "1958", BOOL_("J", lambda: get(J, COMP + ".corte") == "1958-12", "corte = 1958-12"), kind="fecha")
C(K, "-483.21", J_(CAL + ".modelos.sin_regresores.aicc"))
C(K, "-490.72", J_(CAL + ".modelos.con_dias_pascua.aicc"))
permite(K, "12", "mes (1958-12)")

# ---- M10–M11 --------------------------------------------------------------------
K = "Con \\(m\\) grande el SARIMA se rompe"
for i, m in enumerate((12, 52, None, 365)):
    if m:
        C(K, str(m), J_(f"{FOU}.costo_m.{i}.observaciones_perdidas"), J_(f"{FOU}.costo_m.{i}.rezago_maximo_sma1"))
C(K, "156", R_("m10.n_semanal"))
C(K, "104", R_("m10.queda_tras_52"))
C(K, "800", DEF_("longitud de la serie simulada (verifica_directo_cap5.R)"), kind="simulación")
C(K, "365.25", DEF_("días del año medio (calendario)"), kind="calendario")
C(K, "0,0,0", BOOL_("R", lambda: R["m10"]["auto_365"] == "ARIMA(0,0,0) with zero mean", "auto.arima con frecuencia 365"), kind="modelo")
C(K, "K3", BOOL_("J", lambda: all(c["parametros_fourier_K3"] == 6 for c in get(J, FOU + ".costo_m")), "6 términos con K = 3 para todo m"), kind="dato")

K = "Fourier modela la estación con"
C(K, "11", CALC_(lambda: 12 - 1, "m − 1 con m = 12"))
C(K, "12", DEF_("m"), kind="convención")

K = "Hace falta \\(K=5\\)"
for i, (aicc, lb) in enumerate((("-359.18", None), ("-409.18", None), ("-460.96", None), ("-495.24", "0.0001"), ("-521.22", "0.1341"), ("-521.45", "0.1100"))):
    C(K, aicc, J_(f"{FOU}.resultados.{i}.aicc"))
    if lb:
        C(K, lb, J_(f"{FOU}.resultados.{i}.lb24_p"))
    C(K, "143", J_(f"{FOU}.resultados.{i}.nobs"))
C(K, "0.0001", BOOL_("J", lambda: all(get(J, f"{FOU}.resultados.{i}.lb24_p") < 1e-4 for i in range(3)), "LB p < 0.0001 para K = 1, 2, 3 (J guarda 0)"), kind="cota")
C(K, "10", J_(FOU + ".resultados.4.n_terminos"))
C(K, "11", J_(FOU + ".resultados.5.n_terminos"))
C(K, "errores", BOOL_("J", lambda: [r["modelo_errores"] for r in get(J, FOU + ".resultados")] ==
                    [f"Regression with ARIMA({o}) errors" for o in ("5,1,0", "0,1,4", "2,1,2", "1,1,4", "0,1,4", "0,1,4")], "modelos de error de J"), kind="modelo")
permite(K, "24", "rezagos de Ljung–Box")

K = "Regresión armónica con AICc −521.2"
C(K, "-521.2", J_(FOU + ".resultados.4.aicc"))
C(K, "-483.2", J_(AIR + ".aicc"))
C(K, "38", CALC_(lambda: get(J, AIR + ".aicc") - get(J, FOU + ".resultados.4.aicc"), "−483.21 − (−521.22)"))
C(K, "38.0", CALC_(lambda: get(J, AIR + ".aicc") - get(J, FOU + ".resultados.4.aicc"), "ídem"))
C(K, "143", J_(FOU + ".comparabilidad.nobs_armonicos"))
C(K, "131", J_(FOU + ".comparabilidad.nobs_airline"))
C(K, "16", J_(FOU + ".resultados.5.n_par_total"))
C(K, "0.1341", J_(FOU + ".resultados.4.lb24_p"))
C(K, "0.2330", J_(DIAG + ".lb24_p"))
C(K, "521.22", J_(FOU + ".resultados.4.aicc", -1))
C(K, "483.21", J_(AIR + ".aicc", -1))

K = "SARIMA, Fourier o STL"
C(K, "stl", BOOL_("J", lambda: get(J, FOU + ".stl.modelo_errores") == "ARIMA(1,1,1) with drift", "STL + ARIMA = ARIMA(1,1,1) con deriva"), kind="modelo")
permite(K, "12", "m")

K = "Con los últimos 24 meses como prueba"
C(K, "19.43", J_(COMP + ".modelos.ets_log.rmse"))
C(K, "14.69", J_(COMP + ".modelos.armonica.mae"))
C(K, "3.15", J_(COMP + ".modelos.armonica.mape"))
C(K, "43.18", J_(COMP + ".modelos.sarima.rmse"))
C(K, "120", J_(COMP + ".n_entrenamiento"))
C(K, "24", J_(COMP + ".n_prueba"))
C(K, "1958", BOOL_("J", lambda: get(J, COMP + ".corte") == "1958-12", "corte"), kind="fecha")
C(K, "1959", BOOL_("J", lambda: get(J, COMP + ".fechas_prueba.0") == "1959-01", "primera fecha de prueba"), kind="fecha")
C(K, "1960", BOOL_("J", lambda: get(J, COMP + ".fechas_prueba.23") == "1960-12", "última fecha de prueba"), kind="fecha")
C(K, "orden", BOOL_("J", lambda: get(J, COMP + ".orden_rmse")[:4] == ["ets_log", "armonica", "stl_arima", "sarima"], "orden por RMSE: ETS log, armónica, STL, SARIMA"), kind="orden")
permite(K, "12", "mes (1958-12)")

K = "Con una sola partición, el modelo de once"
for m, k, rmse, mae, mape in (("ets_log", "16", "19.43", "16.12", "3.55"), ("armonica", "16", "19.51", "14.69", "3.15"),
                              ("stl_arima", None, "35.48", "30.29", "6.33"), ("sarima", "2", "43.18", "39.45", "8.52"),
                              ("sarima_calendario", "4", "45.48", "41.45", "8.95"), ("ets", "17", "72.55", "63.21", "13.30"),
                              ("snaive", "0", "76.99", "71.25", "15.52")):
    if k and int(k) >= 10:
        C(K, k, J_(f"{COMP}.modelos.{m}.n_par"))
    C(K, rmse, J_(f"{COMP}.modelos.{m}.rmse"), R_(f"m11.particion.{m}.rmse"))
    C(K, mae, J_(f"{COMP}.modelos.{m}.mae"), R_(f"m11.particion.{m}.mae"))
    C(K, mape, J_(f"{COMP}.modelos.{m}.mape"), R_(f"m11.particion.{m}.mape"))
C(K, "auto", BOOL_("J", lambda: get(J, COMP + ".modelos.auto_arima.rmse") == get(J, COMP + ".modelos.sarima.rmse"), "auto.arima = airline (mismo RMSE)"), kind="dato")
C(K, "11", CALC_(lambda: 12 - 1, "valores libres de la estacionalidad (m − 1)"), CH_("valores de la estacionalidad"))
C(K, "stl 2", BOOL_("J", lambda: get(J, f"{COMP}.modelos.stl_arima.n_par") == 2, "n_par del STL + ARIMA = 2 en J"),
  BOOL_("R", lambda: R["m11"]["particion"]["stl_arima"]["n_par"] == 2, "n_par = 2 en R"), kind="dato")
C(K, "16.13", CH_("16.13"), kind="capítulo (doble redondeo)")
C(K, "16.125", J_(f"{COMP}.modelos.ets_log.mae"))
C(K, "16.1249", R_("m11.particion.ets_log.mae"))
C(K, "1,1,0", BOOL_("R", lambda: R["m11"]["particion"]["stl_arima"]["modelo"] == "ARIMA(1,1,0) with drift", "STL + ARIMA sobre el entrenamiento"), kind="modelo")

K = "Con 61 orígenes"
for m, rmse, pct in (("sarima", "16.81", None), ("ets_log", "21.42", "8.2"), ("stl", "21.85", "8.2"), ("armonica", "22.38", "9.8"),
                     ("ets_orig", "26.38", "14.8"), ("snaive", "41.24", "11.5")):
    C(K, rmse, J_(f"{OM}.rmse_medio.{m}"), R_(f"m11.om12.rmse_medio.{m}"))
    if pct:
        C(K, pct, J_(f"{OM}.porcentaje_gana_al_sarima.{m}"), R_(f"m11.om12.gana_al_sarima_pct.{m}"))
C(K, "61", J_(OM + ".n_origenes"), R_("m11.om12.n"))
C(K, "1954", BOOL_("J", lambda: get(J, OM + ".primer_origen") == "1954-12", "primer origen 1954-12"), BOOL_("R", lambda: R["m11"]["om12"]["primer"] == "1954-12", "R"), kind="fecha")
C(K, "85", CALC_(lambda: 100 - max(v for k, v in get(J, OM + ".porcentaje_gana_al_sarima").items() if k != "sarima"), "100 − el peor porcentaje"), tol=0.5, nota="«más del 85 %»: 85.2")
C(K, "85.2", CALC_(lambda: 100 - get(J, OM + ".porcentaje_gana_al_sarima.ets_orig"), "100 − 14.8"))
C(K, "12", J_(OM + ".horizonte"))
C(K, "22.39", CHQ_("22.39"), kind="capítulo (doble redondeo)")
C(K, "22.385", J_(OM + ".rmse_medio.armonica"))
C(K, "22.3847", R_("m11.om12.rmse_medio.armonica"))

K = "La partición cayó justo detrás del frenazo"
C(K, "1958", BOOL_("J", lambda: get(J, COMP + ".corte") == "1958-12", "corte 1958-12"), kind="fecha")
C(K, "3.4", CR(1958))
C(K, "6.0", CALC_(lambda: min(100 * math.log(1 + v / 100) for y, v in R["m11"]["crecimiento_anual"].items() if y != "1958"), "mínimo de 100·Δlog fuera de 1958"))
C(K, "19.8", CALC_(lambda: max(100 * math.log(1 + v / 100) for y, v in R["m11"]["crecimiento_anual"].items() if y != "1958"), "máximo de 100·Δlog fuera de 1958"))
C(K, "4.6", crec_log("sarima_pron", "f59_vs_obs58"))
C(K, "6.7", crec_log("sarima_pron", "f60_vs_f59"))
C(K, "11.7", CR(1959))
C(K, "10.6", CR(1960))
C(K, "39.45", R_("m11.sesgo_sarima"), R_("m11.mae_sarima"), J_(COMP + ".modelos.sarima.mae"))
C(K, "24", R_("m11.errores_positivos"))
C(K, "14", R_("m11.om12.sarima_no_es_el_mejor"))
C(K, "12", CALC_(lambda: sum(1 for o in R["m11"]["om12"]["origenes_no_mejor"] if "1957-05" <= o <= "1959-01"), "orígenes entre 1957-05 y 1959-01"))
for y, et in ((1957, "1957-05"), (1959, "1959-01")):
    C(K, str(y), BOOL_("R", lambda et=et: et in R["m11"]["om12"]["origenes_no_mejor"], f"{et} es uno de los orígenes en que el SARIMA no es el mejor"), kind="fecha")
C(K, "61", R_("m11.om12.n"), J_(OM + ".n_origenes"))
C(K, "1960", DEF_("año pronosticado"), kind="fecha")
C(K, "100", DEF_("factor de la diferencia logarítmica"), kind="unidad")
C(K, "8.9", crec_log("ets_log_pron", "f59_vs_obs58"))
C(K, "12.1", crec_log("ets_log_pron", "f60_vs_f59"))
C(K, "10.1", crec_log("armonica_pron", "f59_vs_obs58"))
C(K, "12.4", crec_log("armonica_pron", "f60_vs_f59"))
C(K, "6.2", R_("m11.crec_otros_min"))
C(K, "21.8", R_("m11.crec_otros_max"))
C(K, "11.2", R_("m11.crecimiento_anual.1960"))
C(K, "4.7", R_("m11.sarima_pron.f59_vs_obs58"))
C(K, "6.9", R_("m11.sarima_pron.f60_vs_f59"))
for y in ("3.4", "11.7", "10.6", "4.6", "6.7", "8.9", "12.1", "10.1", "12.4", "6.0", "19.8"):
    C(K, y, CH_(y), kind="capítulo")

K = "A 24 meses, SARIMA y ETS"
C(K, "49", R_("m11.om24.n"))
C(K, "26.00", R_("m11.om24.rmse_medio.sarima"))
C(K, "26.61", R_("m11.om24.rmse_medio.ets_log"))
C(K, "27.80", R_("m11.om24.rmse_medio.stl"))
C(K, "28.30", R_("m11.om24.rmse_medio.armonica"))
C(K, "49.0", R_("m11.om24.gana_al_sarima_pct.ets_log"))
C(K, "18.22", R_("m11.om12.error_mes_h_abs.sarima"))
C(K, "15.96", R_("m11.om12.error_mes_h_abs.ets_log"))
C(K, "cuarto", BOOL_("R", lambda: sorted(R["m11"]["om12"]["error_mes_h_abs"], key=R["m11"]["om12"]["error_mes_h_abs"].get).index("sarima") == 3, "el SARIMA es 4.º por |e₁₂|"), kind="orden")
C(K, "61", R_("m11.om12.n"))
C(K, "24", J_("horizonte"))
C(K, "12", J_(OM + ".horizonte"))
C(K, "26.0014", R_("m11.om24.rmse_medio.sarima"))
C(K, "26.6081", R_("m11.om24.rmse_medio.ets_log"))
C(K, "27.7998", R_("m11.om24.rmse_medio.stl"))
C(K, "28.2957", R_("m11.om24.rmse_medio.armonica"))
C(K, "48.98", R_("m11.om24.gana_al_sarima_pct.ets_log"))
C(K, "18.2228", R_("m11.om12.error_mes_h_abs.sarima"))
C(K, "15.9627", R_("m11.om12.error_mes_h_abs.ets_log"))
for v in ("26.00", "26.61", "27.80", "28.30", "49.0", "18.22", "15.96"):
    C(K, v, CH_(v), kind="capítulo")

K = "El SARIMA frente a lo que se usa hoy"
C(K, "144", R_("datos.ap_n"))
sin_verificar(K, "la tabla entera (dónde brilla y dónde falla cada método)", "el capítulo la resume de M4, M5 y la literatura sin citar resultados concretos")

K = "Para seguir: tres ejercicios"
for s, titulo in (("9.9", "Seasonal ARIMA models"), ("12.1", "Complex seasonality"), ("7.4", "Some useful predictors"), ("10.5", "Dynamic harmonic regression")):
    C(K, s, CH_(f"§ {s}"), WEB_(f"otexts.com/fpp3: § {s} «{titulo}» (comprobado a mano el 2026-10-27)"), kind="sección de FPP3")
C(K, "3.9", CH_("Cap. 3.9"), kind="capítulo (sin contrastar con el libro)")
C(K, "10.1", WEB_("otexts.com/fpp3: § 10.1 «Estimation» y § 10.2 «Regression with ARIMA errors using fable» (2026-10-27)"), kind="sección de FPP3")
C(K, "10.2", WEB_("ídem"), kind="sección de FPP3")
C(K, "9.1", WEB_("otexts.com/fpp3: el ejemplo A10 (antidiabéticos) está en § 9.1, «Seasonal differencing» (2026-10-27)"), kind="sección de FPP3")
C(K, "2026", DEF_("año de la consulta"), kind="fecha")
permite(K, "10 27", "fecha de la consulta (2026-10-27)")
sin_verificar(K, "Shumway y Stoffer, cap. 3.9 · Box, Jenkins, Reinsel y Ljung, cap. 9", "los libros no están en el repositorio")


# ===========================================================================
# MOTOR
# ===========================================================================
OBSERVACIONES = [
    ("Ocho cifras del capítulo están doblemente redondeadas: se redondearon desde el valor ya redondeado de J (que acaba en 5) y no desde el exacto.",
     "M1 (tabla de la firma): ρ̂₂₄ de log(AirPassengers) 0.521 → 0.520 (exacto 0.52049; también en el M7); ρ̂₁ de USAccDeaths 0.708 → 0.707 (0.70747); ρ̂₂₄ de co2 0.856 → 0.855 (0.85546); ρ̂₁₂ de la TRM en niveles 0.637 → 0.636 (0.63649; también en la pregunta 1 de la autoevaluación); ρ̂₁₂ de ∇TRM −0.003 → −0.002 (−0.00245). M4: ρ₁₁ del AR(1)×SMA(1) −0.235 → −0.234 (−0.23446). M11: MAE del ETS sobre el logaritmo 16.13 → 16.12 (16.1249); RMSE medio de la armónica en 61 orígenes 22.39 → 22.38 (22.3847; también en la pregunta 8). Las diapositivas usan los exactos y lo dicen en sus notas. Ninguna conclusión cambia."),
    ("Módulo 11, autoevaluación (pregunta 8): el enunciado dice que en la partición única la regresión armónica es «primera (19.51)».",
     "Por RMSE la primera es el ETS sobre el logaritmo (19.43; J `orden_rmse`); la armónica gana solo en MAE y MAPE. La explicación de la segunda opción afirma que «las tres métricas dan el mismo orden», y no es así; y la de la opción correcta atribuye el resultado a un «crecimiento especialmente regular» de 1959–1960, cuando el texto del módulo lo atribuye al frenazo de 1958. La diapositiva no proyecta esa pregunta tal cual. El texto interno de J (`origen_movil.nota`) arrastra la misma frase («corona a la regresión armónica»)."),
    ("Módulo 11: los crecimientos anuales (3.4; entre 6.0 y 19.8; 11.7 y 10.6; 4.6 y 6.7; 8.9 y 12.1; 10.1 y 12.4) se escriben con «%», pero son diferencias logarítmicas del total anual, × 100.",
     "En porcentaje: 1958 creció 3.4 %, los demás años entre 6.2 y 21.8 %, lo observado fue 12.4 y 11.2 %, y el airline pronosticó 4.7 y 6.9 %. La conclusión no cambia. La diapositiva conserva las cifras del capítulo con la unidad «100 · Δlog»."),
    ("Módulo 7, nota «El problema del Capítulo 4, cerrado»: dice que el mejor no estacional era un ARIMA(0,1,1) con AICc −238.64 y ρ̂₁₂ = 0.8106, y compara ese AICc con el del airline (−483.21).",
     "El Módulo 1 (corregido en la auditoría del capítulo 4) dice que el mejor no estacional es el ARIMA(0,1,5), con ρ̂₁₂ = 0.7245; y comparar AICc con distinto D es justo lo que el Módulo 6 prohíbe (143 frente a 131 observaciones). La cifra −238.64 viene de J (`puente_cap4`), que no se actualizó. Las diapositivas usan el ARIMA(0,1,5) y no comparan AICc."),
    ("Módulo 5: ψ₁₂ = 1.0412 y ψ₁₃…₂₃ = 0.8632 en el texto; el bloque de R del Módulo 7 imprime 1.0413 y 0.8633.",
     "Es redondeo: el bloque usa los coeficientes redondeados (−0.4018, −0.5569). Las diapositivas usan los del texto, que coinciden con J."),
    ("Módulo 4: el capítulo da ρ₁₁ = ρ₁₃ = 0.14705 «del modelo ajustado».",
     "Con los coeficientes sin redondear es 0.14707; 0.14705 sale con −0.4018 y −0.5569. A cuatro decimales los dos son 0.1471."),
    ("Autoevaluación, pregunta 2: la explicación dice «ρ₂ = ρ₁² ≈ 0.36» para el AR(1)×SAR(1).",
     "En el proceso multiplicado ρ₂ = 0.3637 y ρ₁² = 0.3619: no es una igualdad, aunque los dos redondean a 0.36."),
    ("Autoevaluación, pregunta 6: está etiquetada «módulo 6» y su explicación remite a la lección del Módulo 10.", "Menor."),
    ("Módulo 3: «∇ solo reduce la varianza a la vigésima parte» y «∇₁₂ sola la reduce cincuenta veces».",
     "Los cocientes son 17.2 y 51.3. «La vigésima parte» es una aproximación generosa."),
    ("Módulo 6, advertencia final: «los coeficientes casi coinciden con los de R (diferencia 6 × 10⁻⁵)» con statsmodels sin `simple_differencing`.",
     "Con statsmodels 0.14.6 la diferencia máxima es 2.4 × 10⁻⁴ (−0.4021 y −0.5571 frente a −0.4018 y −0.5569). Sigue siendo despreciable; depende de la versión. No se proyecta."),
    ("Las dos copias de la TRM llevan fechas de consulta distintas: `cap5_sarima.json` dice «consulta: 2026-07-24» y `datos_series.json` (y el capítulo 4) «2026-07-26».",
     "No afecta a ninguna cifra (las dos son la misma copia de 138 meses), pero conviene unificarlo."),
    ("Lecturas: el capítulo asocia FPP3 § 10.5 a «regresión dinámica con errores ARIMA» y § 9.9 al «caso de los medicamentos antidiabéticos».",
     "Comprobado en otexts.com/fpp3 (2026-10-27): § 10.5 es «Dynamic harmonic regression» (la regresión con errores ARIMA está en § 10.1–10.2), y el caso de § 9.9 son los corticoides (H02); los antidiabéticos (A10) salen en § 9.1. Las demás secciones de FPP3 citadas (7.4, 12.1) coinciden."),
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
CTX = re.compile(r"(Módulos?|módulos?|Capítulo|capítulo|Cap\.|sección|secciones|etapa|rezagos?|Ljung.Box\(|\bh\s*=|\bn\s*=|Chapter|tseries|forecast|statsmodels|pregunta|R)\s*$")


def tokens_de(texto: str):
    t = limpio(texto)
    out = []
    for m in NUM.finditer(t):
        tok = m.group(0).replace(" ", "").replace("%", "")
        if CTX.search(t[max(0, m.start() - 16): m.start()]):
            continue
        core = tok.lstrip("-")
        if not ("." in core or "%" in m.group(0) or float(core) >= 10):
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


def verifica_codigo():
    """Ejecuta en R cada bloque ```r y comprueba que sus líneas `#>` aparezcan, en orden, en la salida real."""
    import shutil
    import subprocess
    import tempfile

    if not shutil.which("Rscript"):
        print("  ! Rscript no está instalado: no se ejecutó el código proyectado")
        return None
    texto = re.sub(r"<!--.*?-->", "", DECK.read_text(encoding="utf-8"), flags=re.S)
    out = []
    for cuerpo in re.findall(r"```r[^\n]*\n(.*?)```", texto, flags=re.S):
        esperadas = [" ".join(re.sub(r"^#>\s?", "", l).split()) for l in cuerpo.splitlines() if l.startswith("#>")]
        with tempfile.NamedTemporaryFile("w", suffix=".R", delete=False, encoding="utf-8") as f:
            f.write("pdf(NULL)\n" + cuerpo)
            ruta = f.name
        r = subprocess.run(["Rscript", ruta], capture_output=True, text=True, timeout=600, env={**os.environ, "LC_ALL": "en_US.UTF-8"})
        reales = [" ".join(l.split()) for l in r.stdout.splitlines()]
        i = hallo = 0
        for e in esperadas:
            while i < len(reales) and reales[i] != e:
                i += 1
            if i < len(reales):
                hallo += 1
                i += 1
        ok = r.returncode == 0 and hallo == len(esperadas)
        out.append((cuerpo.strip().splitlines()[0][:60], len(esperadas), hallo, ok, r.stderr[-300:] if not ok else ""))
    return out


def main() -> int:
    slides = slides_del_deck()
    por_clave: dict[str, dict] = {}
    for k in {c.slide for c in CLAIMS} | set(ALLOW) | {x[0] for x in SIN_VERIFICAR}:
        cand = [s for s in slides if k in s["titulo"]]
        if len(cand) != 1:
            print(f"ERROR: la clave de diapositiva «{k}» encaja con {len(cand)} títulos")
            return 1
        por_clave[k] = cand[0]

    fallos, sin_presencia, sin_marca = [], [], []
    for c in CLAIMS:
        sl = por_clave[c.slide]
        ok = evalua(c)
        c.estado = ("definición (no se mide)" if all(x.tag == "DEF" for x in c.srcs) else "verificado") if ok else "NO COINCIDE"
        if not ok:
            fallos.append(c)
        if not presente(c.shown, sl["titulo"] + "\n" + sl["texto"]):
            sin_presencia.append(c)
    for k, texto, _ in SIN_VERIFICAR:
        if "[SIN VERIFICAR]" not in por_clave[k]["texto"]:
            sin_marca.append((k, texto))

    sin_cobertura = []
    for sl in slides:
        toks = tokens_de(sl["titulo"] + "\n" + sl["texto"])
        claves = [k for k in por_clave if por_clave[k] is sl]
        cubiertos = {c.shown for c in CLAIMS if c.slide in claves and es_numerico(c.shown)}
        permitidos = {t for k in claves for t in ALLOW.get(k, {})}
        falt = sorted({t for t in toks if t not in cubiertos and t not in permitidos}, key=lambda x: (len(x), x))
        if falt:
            sin_cobertura.append((sl["titulo"], falt))

    codigo_res = None if "--sin-codigo" in sys.argv else verifica_codigo()
    fallos_codigo = [c for c in (codigo_res or []) if not c[3]]

    n = len(CLAIMS)
    verificados = sum(1 for c in CLAIMS if c.estado in ("verificado", "definición (no se mide)"))
    n_def = sum(1 for c in CLAIMS if c.estado == "definición (no se mide)")
    print(f"claims: {n} · verificados: {verificados} (de ellos {n_def} son definiciones o convenciones) · "
          f"sin verificar (marcados): {len(SIN_VERIFICAR)} · no coinciden: {len(fallos)}")
    for c in fallos:
        print(f"  ✗ [{c.slide[:40]}] «{c.shown}»")
        for s, ok, v in c.resultados:
            print(f"      {'✓' if ok else '✗'} {s.tag}: {s.desc} = {v}")
    for c in sin_presencia:
        print(f"  ! «{c.shown}» no aparece en la diapositiva «{c.slide[:40]}»")
    for k, t in sin_marca:
        print(f"  ! falta la marca [SIN VERIFICAR] en «{k[:40]}» ({t})")
    for t, falt in sin_cobertura:
        print(f"  ? cifras sin respaldo en «{t[:60]}»: {' '.join(falt)}")
    if codigo_res is not None:
        print(f"código R proyectado: {len(codigo_res)} bloques · " + ", ".join(f"{h}/{e}" for _, e, h, _, _ in codigo_res))
        for pl, e, h, ok, err in codigo_res:
            if not ok:
                print(f"  ✗ bloque «{pl}»: {h}/{e} salidas coinciden. {err}")

    ok_total = not (fallos or sin_presencia or sin_marca or sin_cobertura or fallos_codigo)
    if "--sin-escribir" not in sys.argv:
        escribe_informe(slides, por_clave, verificados, codigo_res, len(fallos))
    print("RESULTADO:", "todo verificado y cubierto" if ok_total else "hay pendientes")
    return 0 if ok_total else 1


def escribe_informe(slides, por_clave, verificados, codigo_res, n_fallos):
    L = ["# Verificación de cifras · Capítulo 5 (diapositivas)", "",
         "Generado por `verifica_cifras_cap5.py`. Cada fila es una cifra (o afirmación) de las diapositivas o de sus notas, con las fuentes contra las que se contrastó.", "",
         "## Cómo se verificó", "",
         "- **J** · `precalculo/salidas/cap5_sarima.json`, el precálculo del capítulo. **J4** · `cap4_arima.json`. **J3** · `cap3_arma.json`.",
         f"- **R** · recálculo directo sobre los datos congelados, `verifica_directo_cap5.R` → `directo_cap5.json`, en {R['entorno']['R']} (forecast {R['entorno']['forecast']}, tseries {R['entorno']['tseries']}). Incluye lo que J no guarda: la tabla de varianzas con parte AR, el horizonte de 24 meses, el error del mes 12 y los crecimientos anuales del Módulo 11.",
         f"- **PY** · statsmodels {PY['entorno']['statsmodels']}, `verifica_python_cap5.py` → `directo_python_cap5.json`.",
         "- **DOC** · ayuda de R de `AirPassengers`, `USAccDeaths` y `co2`, y el NEWS de forecast, `verifica_docs_cap5.R` → `docs_cap5.json`.",
         "- **CALC** · aritmética sobre los datos (ACF con divisor n, bandas 1.96/√n) o sobre las fuentes anteriores. **C** · texto del capítulo. **DEF** · definición o convención.",
         "- La fuente se redondea a los decimales que muestra la diapositiva, a la mitad hacia arriba. Las ACF y las bandas se recalculan desde los datos para no redondear dos veces.",
         "- La TRM es la copia congelada de `datos_series.json`; **no** se cotejó con datos.gov.co.",
         "- Los tres gráficos animados se comprueban como idénticos a lo que `genera_animados_cap5.py` construye desde J.", ""]
    n_def = sum(1 for c in CLAIMS if c.estado == "definición (no se mide)")
    L += ["## Resumen", "", f"- Cifras y afirmaciones registradas: **{len(CLAIMS)}**",
          f"- Verificadas contra al menos una fuente: **{verificados - n_def}**",
          f"- Definiciones o convenciones: **{n_def}**",
          f"- Comprobadas a mano en una fuente pública fuera del repositorio (`WEB`, con fecha): **{sum(1 for c in CLAIMS if any(x.tag == 'WEB' for x in c.srcs))}**",
          f"- Marcadas `[SIN VERIFICAR]`: **{len(SIN_VERIFICAR)}**",
          f"- No coinciden: **{n_fallos}**", ""]
    tags = Counter(s.tag for c in CLAIMS if c.estado == "verificado" for s, _, _ in c.resultados)
    L += ["Contrastes por tipo de fuente: " + ", ".join(f"{t} {n}" for t, n in sorted(tags.items())) + ".", ""]
    if codigo_res:
        L += ["## Código proyectado, ejecutado", "", f"Cada bloque `r` se ejecutó en {R['entorno']['R']} y sus líneas `#>` se compararon con la salida real.", "",
              "| Bloque (primera línea) | Salidas esperadas | Encontradas | Estado |", "|---|---|---|---|"]
        L += [f"| `{pl}` | {e} | {h} | {'coincide' if ok else 'NO COINCIDE'} |" for pl, e, h, ok, _ in codigo_res]
        L.append("")
    L += ["## Lo que no se pudo verificar (`[SIN VERIFICAR]`)", "", "| Diapositiva | Qué | Por qué |", "|---|---|---|"]
    L += [f"| {por_clave[k]['titulo'][:60]} | {t} | {m} |" for k, t, m in SIN_VERIFICAR]
    L += ["", "## Observaciones sobre el material (no corregidas en silencio)", ""]
    L += [f"{i}. {a} {b}" for i, (a, b) in enumerate(OBSERVACIONES, 1)]
    L += ["", "## Tabla de cifras", ""]
    orden = {id(s): i for i, s in enumerate(slides)}
    grupos = defaultdict(list)
    for c in CLAIMS:
        grupos[c.slide].append(c)
    for k in sorted(grupos, key=lambda x: orden[id(por_clave[x])]):
        L += [f"### {por_clave[k]['titulo']}", "", "| Cifra o afirmación | Tipo | Fuentes y valor | Estado |", "|---|---|---|---|"]
        for c in grupos[k]:
            partes = []
            for s, ok, v in c.resultados:
                vv = v if s.booleana else (round(v, 6) if isinstance(v, float) else v)
                partes.append(f"{s.tag}: {s.desc}" + ("" if s.booleana else f" = {vv}"))
            nota = f" ({c.nota})" if c.nota else ""
            L.append(f"| `{c.shown}`{nota} | {c.kind} | {'<br>'.join(partes)} | {c.estado} |")
        L.append("")
    SALIDA_MD.write_text("\n".join(L), encoding="utf-8")
    print("informe:", SALIDA_MD.relative_to(RAIZ))


if __name__ == "__main__":
    sys.exit(main())
