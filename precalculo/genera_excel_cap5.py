#!/usr/bin/env python3
"""
genera_excel_cap5.py — el capítulo 5 (Modelos SARIMA), celda a celda, en Excel

Material de Series de Tiempo 2026-II (20948), Universidad El Bosque.

Escribe dos libros en `Htmls_Series/ejercicios/`:

  · `capitulo-5-sarima-ejercicio.xlsx`, el del estudiante: datos, instrucciones y
    las fórmulas clave en blanco, con su instrucción al lado y en un comentario.
    Sus comprobaciones salen en rojo hasta que se completan.
  · `capitulo-5-sarima-solucion.xlsx`, el mismo libro con todo resuelto.

Una hoja por módulo del capítulo (M1 a M11), más la portada y los datos.

De dónde sale cada número:
  · las series, de `precalculo/salidas/datos_series.json`;
  · los coeficientes que estima R y las cifras con que se compara cada resultado,
    de `precalculo/salidas/cap5_sarima.json` (J);
  · los dos ejemplos inventados del capítulo —la heladería del M2 y la tienda del
    M3— son datos del enunciado: están en EJEMPLOS, y `verifica_excel_cap5.py`
    comprueba que coinciden con el texto del capítulo;
  · lo que el capítulo no trae (la recursión CSS, la ACF de ∇USAccDeaths, la
    regresión armónica por MCO, la serie simulada) lo calcula este guion con la
    misma aritmética que el libro y lo deja en gris como «referencia». El
    verificador lo recalcula por su cuenta.

Excel no estima un SARIMA por máxima verosimilitud: la estimación se queda en R
y el libro toma θ̂, Θ̂, σ̂² y el log-verosimilitud como datos.

Compatibilidad: solo funciones clásicas, que existen en Excel 2016+, LibreOffice y
Google Sheets, aunque solo se ha probado en Excel. Nada de LET, LAMBDA, SEQUENCE
ni matrices dinámicas. Las fórmulas que operan sobre rangos van dentro de
SUMPRODUCT, LINEST, SUMXMY2 o de una función de agregado, para que ningún Excel
les aplique la intersección implícita. CHISQ.DIST.RT y NORM.S.INV (Excel 2010)
se escriben con el prefijo `_xlfn.` que exige el formato de archivo.

Determinista: mismas entradas, mismos bytes (las fechas internas del .xlsx van
fijas).

Uso (desde la raíz del repositorio):
    python3 precalculo/genera_excel_cap5.py              # escribe los dos libros
    python3 precalculo/genera_excel_cap5.py --comprobar  # sale con 1 si difieren
"""

import argparse
import io
import json
import math
import random
import re
import sys
import zipfile
from datetime import date, datetime
from pathlib import Path

import numpy as np
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference, Series
from openpyxl.chart.data_source import NumFmt
from openpyxl.chart.legend import LegendEntry
from openpyxl.chart.marker import DataPoint, Marker
from openpyxl.comments import Comment
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo

RAIZ = Path(__file__).resolve().parent.parent
SALIDAS = RAIZ / "precalculo" / "salidas"
DESTINO = RAIZ / "Htmls_Series" / "ejercicios"
ARCHIVOS = {
    "ejercicio": "capitulo-5-sarima-ejercicio.xlsx",
    "solucion": "capitulo-5-sarima-solucion.xlsx",
}
FECHA_FIJA = (2026, 11, 3, 0, 0, 0)

# Los datos de los dos ejemplos para seguir a mano. Son del enunciado, no
# resultados: el verificador los busca en ensamblado/cap5/templates_1_3.html.
EJEMPLOS = {
    # M2 · «Un ejemplo para seguir a mano: pronosticar un mes»
    "heladeria": {"feb24": 15, "mar24": 20, "feb25": 10},
    # M3 · «Un ejemplo para seguir a mano: la tienda inventada»
    "tienda": {
        "inicio": 100, "pendiente": 1, "anio0": 2022, "anios": 4,
        "patron": [-6, -8, -4, -2, 0, 4, 6, 4, 0, -2, 2, 6],
        "anio_cambio": 2024, "pendiente_nueva": 3,
    },
}
# La serie simulada del M2: ruido N(0, 1) fijo, por Box–Muller sobre
# random.Random(semilla), redondeado a 4 decimales (estable entre versiones).
SIMULACION = {"semilla": 20261103, "n": 720, "quemado": 120}
# Los valores de φ con que el M2 del capítulo tabula la varianza.
PHIS_TABLA = (0.6, 0.8, 0.9, 0.95)
N_PSI = 720          # pesos ψ con que se aproxima la suma infinita del M2

MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
         "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

# ------------------------------------------------------------------- estilo
VERDE = "012820"
NARANJA = "FF6600"
AMARILLO = "FFF2CC"
GRIS = "EDEDED"
F_TITULO = Font(name="Calibri", size=16, bold=True, color=VERDE)
F_OBJ = Font(name="Calibri", size=11, italic=True, color="444444")
F_SECCION = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
F_NEGRITA = Font(name="Calibri", size=11, bold=True)
F_DATO = Font(name="Calibri", size=11, italic=True, color="555555")
F_GUION = Font(name="Calibri", size=11, color="999999")
F_CHECK = Font(name="Calibri", size=12, bold=True)
F_NOTA = Font(name="Calibri", size=11, color="9A3412")
F_ENC = Font(name="Calibri", size=11, bold=True, color=VERDE)
R_SECCION = PatternFill("solid", fgColor=VERDE)
R_ENTRADA = PatternFill("solid", fgColor=AMARILLO)
R_DATO = PatternFill("solid", fgColor=GRIS)
R_ENC = PatternFill("solid", fgColor="E3EFEA")
R_NOTA = PatternFill("solid", fgColor="FFF7ED")
R_OK = PatternFill(fill_type="solid", start_color="C6EFCE", end_color="C6EFCE")
R_MAL = PatternFill(fill_type="solid", start_color="FFC7CE", end_color="FFC7CE")
fino = Side(style="thin", color="BBBBBB")
grueso = Side(style="medium", color=NARANJA)
B_FINO = Border(left=fino, right=fino, top=fino, bottom=fino)
B_CLAVE = Border(left=grueso, right=grueso, top=grueso, bottom=grueso)
CENTRO = Alignment(horizontal="center", vertical="center")
AJUSTE = Alignment(wrap_text=True, vertical="top")

F4 = "0.0000"
F6 = "0.000000"
F2 = "0.00"
FMES = "yyyy-mm"


def L(col):
    return get_column_letter(col)


def ab(col, fila):
    return f"${L(col)}${fila}"


# ----------------------------------------------------------- aritmética base
# Lo que el capítulo no trae lo calcula el guion con la misma aritmética que el
# libro. Python puro donde basta; numpy solo para mínimos cuadrados.

def acf(x, kmax):
    n = len(x)
    m = sum(x) / n
    d = [v - m for v in x]
    den = sum(v * v for v in d)
    return [sum(d[i] * d[i + k] for i in range(n - k)) / den for k in range(1, kmax + 1)]


def var_muestral(x):
    m = sum(x) / len(x)
    return sum((v - m) ** 2 for v in x) / (len(x) - 1)


def chi2_cola_par(q, gl):
    """P(χ²_gl > q) para gl par: e^{-q/2} Σ_{i<gl/2} (q/2)^i / i!."""
    assert gl % 2 == 0
    x = q / 2
    termino, suma = 1.0, 1.0
    for i in range(1, gl // 2):
        termino *= x / i
        suma += termino
    return math.exp(-x) * suma


def ljung_box(res, h):
    n = len(res)
    r = acf(res, h)
    return n * (n + 2) * sum(r[k - 1] ** 2 / (n - k) for k in range(1, h + 1))


def ruido_fijo(n, semilla):
    gen = random.Random(semilla)
    salida = []
    while len(salida) < n:
        u1, u2 = gen.random(), gen.random()
        if u1 <= 0:
            continue
        radio = math.sqrt(-2 * math.log(u1))
        salida += [radio * math.cos(2 * math.pi * u2), radio * math.sin(2 * math.pi * u2)]
    return [round(v, 4) for v in salida[:n]]


def psi_ar1_sar1(phi, Phi, n):
    psi = []
    for j in range(n):
        v = 1.0 if j == 0 else 0.0
        if j >= 1:
            v += phi * psi[j - 1]
        if j >= 12:
            v += Phi * psi[j - 12]
        if j >= 13:
            v -= phi * Phi * psi[j - 13]
        psi.append(v)
    return psi


def tienda(acelera):
    t_ = EJEMPLOS["tienda"]
    tc = 12 * (t_["anio_cambio"] - t_["anio0"])
    y = []
    for t in range(1, 12 * t_["anios"] + 1):
        if acelera and t > tc:
            tend = (tc - 1) * t_["pendiente"] + t_["pendiente_nueva"] * (t - tc)
        else:
            tend = (t - 1) * t_["pendiente"]
        y.append(t_["inicio"] + tend + t_["patron"][(t - 1) % 12])
    return y


def w_exacta(D):
    """∇∇₁₂ log(AirPassengers) desde la serie, sin el redondeo a 5 decimales de J."""
    ly = [math.log(v) for v in D["airpassengers"]["valores"]]
    d12 = [ly[t] - ly[t - 12] for t in range(12, len(ly))]
    return [d12[t] - d12[t - 1] for t in range(1, len(d12))]


def css_residuales(w, th, Th):
    e = []
    for t in range(len(w)):
        v = w[t]
        if t >= 1:
            v -= th * e[t - 1]
        if t >= 12:
            v -= Th * e[t - 12]
        if t >= 13:
            v -= th * Th * e[t - 13]
        e.append(v)
    return e


def pronostico_airline(ly, e144, th, Th, h=24):
    y, e = list(ly), list(e144)
    for _ in range(h):
        T = len(y)
        y.append(y[T - 1] + y[T - 12] - y[T - 13]
                 + th * e[T - 1] + Th * e[T - 12] + th * Th * e[T - 13])
        e.append(0.0)
    return y[len(ly):]


def psi_airline(th, Th, n):
    ma = {0: 1.0, 1: th, 12: Th, 13: th * Th}
    psi = []
    for j in range(n):
        v = ma.get(j, 0.0)
        if j >= 1:
            v += psi[j - 1]
        if j >= 12:
            v += psi[j - 12]
        if j >= 13:
            v -= psi[j - 13]
        psi.append(v)
    return psi


def pascua(anio):
    a, b, c = anio % 19, anio // 100, anio % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    return date(anio, (h + l_ - 7 * m + 114) // 31, (h + l_ - 7 * m + 114) % 31 + 1)


def fourier_ssr(ly, K, con_indicadoras=False):
    n = len(ly)
    t = np.arange(1, n + 1, dtype=float)
    cols = [np.ones(n), t]
    if con_indicadoras:
        for mes in range(2, 13):
            cols.append(((t - 1) % 12 + 1 == mes).astype(float))
    else:
        for k in range(1, K + 1):
            if not (k == 6):
                cols.append(np.sin(2 * np.pi * k * t / 12))
            cols.append(np.cos(2 * np.pi * k * t / 12))
    X = np.column_stack(cols)
    y = np.asarray(ly)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - (X * beta).sum(axis=1)   # sin matmul: evita avisos espurios de Accelerate
    return float(res @ res), beta


# --------------------------------------------------------------- el libro
class Libro:
    def __init__(self, modo, D, J):
        assert modo in ARCHIVOS
        self.modo = modo
        self.D, self.J = D, J
        self.wb = Workbook()
        self.wb.remove(self.wb.active)
        self.hojas = []
        self.claves = []          # (hoja, celda): en blanco en el del estudiante
        self.comprobaciones = []  # (hoja, celda, qué comprueba)
        self.resultados = []      # (hoja, celda, nombre, tolerancia)

    @property
    def estudiante(self):
        return self.modo == "ejercicio"


class Hoja:
    def __init__(self, libro, nombre, titulo, objetivo, anchos=None, ancho_texto=14):
        self.L = libro
        self.nombre = nombre
        self.ws = libro.wb.create_sheet(nombre)
        self.ws.sheet_properties.tabColor = NARANJA if nombre.startswith("M") else VERDE
        self.ancho_texto = ancho_texto
        self.cf_checks = []
        anchos = anchos or {}
        for col in range(1, 60):
            self.ws.column_dimensions[L(col)].width = anchos.get(L(col), 11)
        self.ws["A1"] = titulo
        self.ws["A1"].font = F_TITULO
        self.ws.row_dimensions[1].height = 24
        if objetivo:
            self.ws["A2"] = objetivo
            self.ws["A2"].font = F_OBJ
        libro.hojas.append(self)

    # --- referencias
    @property
    def q(self):
        return f"'{self.nombre}'!"

    # --- escritura básica
    def put(self, ref, valor, fmt=None, font=None, fill=None, border=None, align=None):
        celda = self.ws[ref]
        celda.value = valor
        if fmt:
            celda.number_format = fmt
        if font:
            celda.font = font
        if fill:
            celda.fill = fill
        if border:
            celda.border = border
        if align:
            celda.alignment = align
        return celda

    def texto(self, ref, s, negrita=False, gris=False, align=None):
        return self.put(ref, s, font=F_NEGRITA if negrita else (F_GUION if gris else None),
                        align=align)

    def guion(self, ref):
        return self.put(ref, "—", font=F_GUION, fill=R_DATO, align=CENTRO)

    def entrada(self, ref, v, fmt=None):
        return self.put(ref, v, fmt=fmt, fill=R_ENTRADA, border=B_FINO)

    def dato(self, ref, v, fmt=None):
        return self.put(ref, v, fmt=fmt, font=F_DATO, fill=R_DATO)

    def formula(self, ref, f, fmt=None, negrita=False):
        return self.put(ref, f, fmt=fmt, font=F_NEGRITA if negrita else None)

    def clave(self, ref, f, instr=None, fmt=None, comentario=True):
        """Una fórmula que el estudiante escribe: en su libro va en blanco."""
        celda = self.put(ref, None if self.L.estudiante else f, fmt=fmt, border=B_CLAVE)
        self.L.claves.append((self.nombre, ref))
        if instr and comentario:
            alto = 40 + 15 * (len(instr) // 45)
            celda.comment = Comment(instr, "Capítulo 5", width=330, height=alto)
        return celda

    def check(self, ref, cond, que, guardia=None):
        """✔ si `cond` se cumple; con `guardia`, «—» mientras no se cumpla."""
        if guardia:
            f = f'=IFERROR(IF({guardia},IF({cond},"✔","✘"),"—"),"✘")'
        else:
            f = f'=IFERROR(IF({cond},"✔","✘"),"✘")'
        self.put(ref, f, font=F_CHECK, align=CENTRO, border=B_FINO)
        self.cf_checks.append(ref)
        self.L.comprobaciones.append((self.nombre, ref, que))

    def resultado(self, ref, nombre, tol):
        self.L.resultados.append((self.nombre, ref, nombre, tol))

    # --- bloques de texto
    def seccion(self, fila, s, c1=1, c2=None):
        c2 = c2 or self.ancho_texto
        for col in range(c1, c2 + 1):
            self.ws.cell(fila, col).fill = R_SECCION
        self.put(f"{L(c1)}{fila}", s, font=F_SECCION)
        self.ws.row_dimensions[fila].height = 20

    def parrafo(self, fila, s, c1=1, c2=None, nota=False):
        c2 = c2 or self.ancho_texto
        self.ws.merge_cells(start_row=fila, start_column=c1, end_row=fila, end_column=c2)
        celda = self.put(f"{L(c1)}{fila}", s, font=F_NOTA if nota else None, align=AJUSTE)
        if nota:
            celda.fill = R_NOTA
        ancho = sum(self.ws.column_dimensions[L(c)].width for c in range(c1, c2 + 1))
        por_linea = max(20, int(ancho * 1.12))
        lineas = sum(max(1, math.ceil(len(trozo) / por_linea)) for trozo in s.split("\n"))
        self.ws.row_dimensions[fila].height = 15.5 * lineas + 3

    def completa(self, fila, s, c1=1, c2=None):
        self.parrafo(fila, "✎ Completa: " + s, c1, c2, nota=True)

    def encabezados(self, fila, col0, nombres, ajuste=False):
        for i, s in enumerate(nombres):
            self.put(f"{L(col0 + i)}{fila}", s, font=F_ENC, fill=R_ENC, border=B_FINO,
                     align=Alignment(horizontal="center", vertical="center",
                                     wrap_text=ajuste))
        if ajuste:
            lineas = max(math.ceil(len(s) / max(4, self.ws.column_dimensions[L(col0 + i)].width - 1))
                         for i, s in enumerate(nombres))
            self.ws.row_dimensions[fila].height = max(30, 15 * lineas + 2)

    def cerrar(self):
        if self.cf_checks:
            rango = " ".join(self.cf_checks)
            self.ws.conditional_formatting.add(
                rango, CellIsRule(operator="equal", formula=['"✔"'], fill=R_OK,
                                  font=Font(bold=True, color="006100")))
            self.ws.conditional_formatting.add(
                rango, CellIsRule(operator="equal", formula=['"✘"'], fill=R_MAL,
                                  font=Font(bold=True, color="9C0006")))


# ------------------------------------------------------------------ gráficos
def _ejes(ch, fmt_y):
    """Ejes visibles (openpyxl 3.1 los oculta si no se dice) y con formato propio."""
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    ch.y_axis.numFmt = NumFmt(formatCode=fmt_y, sourceLinked=False)
    # sin overlay explícito, Excel monta la leyenda y el título sobre el gráfico
    ch.legend.position = "b"
    ch.legend.overlay = False
    if ch.title is not None:
        ch.title.overlay = False


def etiquetas(h, col, f1, f2, col_k, paso):
    """Una columna de rótulos para el eje: el k si es múltiplo de `paso`, vacío si no."""
    for f in range(f1, f2 + 1):
        h.put(f"{L(col)}{f}", f'=IF(MOD({L(col_k)}{f},{paso})=0,{L(col_k)}{f},"")', font=F_GUION)
    return col


def grafico_barras(h, ancla, col_k, col_v, f1, f2, titulo, nombre="ACF muestral",
                   resaltar=(12, 24, 36), banda=None, teorica=None, ancho=17, alto=7.5,
                   eje_x="rezago k", eje_y=None, color=VERDE, fmt_y="0.0"):
    """Barras con los rezagos de `resaltar` en naranja; `col_k` da los rótulos del eje."""
    ws = h.ws
    ch = BarChart()
    ch.type = "col"
    ch.gapWidth = 60
    ch.varyColors = False
    ch.title = titulo
    ch.width, ch.height = ancho, alto
    s = Series(Reference(ws, min_col=col_v, min_row=f1, max_row=f2), title=nombre)
    s.invertIfNegative = False
    s.graphicalProperties.solidFill = color
    s.graphicalProperties.line.solidFill = color
    for k in resaltar:
        if 1 <= k <= f2 - f1 + 1:
            pt = DataPoint(idx=k - 1, invertIfNegative=False)
            pt.graphicalProperties.solidFill = NARANJA
            pt.graphicalProperties.line.solidFill = NARANJA
            s.dPt.append(pt)
    ch.series.append(s)
    cats = Reference(ws, min_col=col_k, min_row=f1, max_row=f2)
    ch.set_categories(cats)
    if banda or teorica:
        ln = LineChart()
        ln.varyColors = False
        if banda:
            for col, nom in ((banda[0], "banda ±1.96/√n"), (banda[1], None)):
                s2 = Series(Reference(ws, min_col=col, min_row=f1, max_row=f2), title=nom or "")
                s2.graphicalProperties.line.solidFill = "7F7F7F"
                s2.graphicalProperties.line.dashStyle = "dash"
                s2.graphicalProperties.line.width = 15000
                s2.marker = Marker(symbol="none")
                s2.smooth = False
                ln.series.append(s2)
        if teorica:
            col, nom = teorica
            s3 = Series(Reference(ws, min_col=col, min_row=f1, max_row=f2), title=nom)
            s3.graphicalProperties.line.solidFill = NARANJA
            s3.graphicalProperties.line.width = 22000
            s3.marker = Marker(symbol="circle", size=4)
            s3.smooth = False
            ln.series.append(s3)
        ln.set_categories(cats)
        ch += ln
    if eje_x:
        ch.x_axis.title = eje_x
    if eje_y:
        ch.y_axis.title = eje_y
    ch.x_axis.tickLblPos = "low"
    ch.x_axis.tickLblSkip = 1
    _ejes(ch, fmt_y)
    if banda:
        # la segunda línea de la banda no necesita entrada en la leyenda
        ch.legend.legendEntry = [LegendEntry(idx=2, delete=True)]
    ws.add_chart(ch, ancla)
    return ch


def grafico_lineas(h, ancla, col_x, series, f1, f2, titulo, ancho=18, alto=8,
                   eje_x=None, eje_y=None, salto=12, fmt_x=None, fmt_y="0.00"):
    ws = h.ws
    ch = LineChart()
    ch.varyColors = False
    ch.title = titulo
    ch.width, ch.height = ancho, alto
    for col, nom, color, discontinua in series:
        s = Series(Reference(ws, min_col=col, min_row=f1, max_row=f2), title=nom)
        s.graphicalProperties.line.solidFill = color
        s.graphicalProperties.line.width = 19000
        if discontinua:
            s.graphicalProperties.line.dashStyle = "dash"
        s.marker = Marker(symbol="none")
        s.smooth = False
        ch.series.append(s)
    ch.set_categories(Reference(ws, min_col=col_x, min_row=f1, max_row=f2))
    if eje_x:
        ch.x_axis.title = eje_x
    if eje_y:
        ch.y_axis.title = eje_y
    if fmt_x:
        ch.x_axis.numFmt = NumFmt(formatCode=fmt_x, sourceLinked=False)
    ch.x_axis.tickLblSkip = salto
    ch.x_axis.tickLblPos = "low"
    _ejes(ch, fmt_y)
    ws.add_chart(ch, ancla)
    return ch


def f_acf(col, f1, f2, kref, hoja=""):
    """ρ̂_k con el divisor de R: Σ(x_t − x̄)(x_{t+k} − x̄) / Σ(x_t − x̄)²."""
    c = L(col)
    r = f"{hoja}${c}${f1}:${c}${f2}"
    n = f2 - f1 + 1
    return (f"=SUMPRODUCT(({hoja}${c}${f1}:INDEX({r},{n}-{kref})-AVERAGE({r}))*"
            f"(INDEX({r},1+{kref}):{hoja}${c}${f2}-AVERAGE({r})))/DEVSQ({r})")


def check_lista(h, ref, col, f1, f2, col_ref, tol, que):
    """Los f2−f1+1 valores de `col` coinciden con los de `col_ref`, ± tol."""
    n = f2 - f1 + 1
    cond = (f"SUMPRODUCT(--(ABS({L(col)}{f1}:{L(col)}{f2}-"
            f"{L(col_ref)}{f1}:{L(col_ref)}{f2})<={tol}))={n}")
    h.check(ref, cond, que)


# =================================================================== hojas
def hoja_portada(lb):
    h = Hoja(lb, "Portada", "Capítulo 5 · Modelos SARIMA, celda a celda", None,
             anchos={"A": 4, "B": 30, "C": 16, "D": 16, "E": 16, "F": 16, "G": 16, "H": 16},
             ancho_texto=8)
    h.ws.sheet_view.showGridLines = False
    if lb.estudiante:
        sub = ("Libro del estudiante: las fórmulas clave están en blanco, con borde naranja. "
               "La solución es el libro hermano, capitulo-5-sarima-solucion.xlsx.")
    else:
        sub = ("Solución: todas las fórmulas resueltas. Conviene abrirla después de intentarlo "
               "en el libro del estudiante, capitulo-5-sarima-ejercicio.xlsx.")
    h.put("A2", sub, font=F_OBJ)
    return h


def portada_contenido(h, lb, ref):
    """Se escribe al final: el tablero cuenta las comprobaciones de cada hoja."""
    J = lb.J
    air = J["airpassengers"]["airline"]
    th, Th = [c_["valor"] for c_ in air["coeficientes"]]
    f = 4
    h.seccion(f, "Para qué sirve")
    h.parrafo(f + 1, "En R, diff(), Acf() o Arima() devuelven el resultado y esconden la cuenta. "
              "Aquí cada número es una celda con su fórmula a la vista: restar la celda de arriba es "
              "∇₁₂, restar las cuatro esquinas de un cuadrado de 2 × 2 es ∇∇₁₂, y los pesos ψ, la ACF, "
              "Ljung–Box y las métricas de error se ven calcular paso a paso. Cada hoja sigue un "
              "módulo del capítulo 5 y reproduce sus cifras.")
    h.parrafo(f + 2, "Lo que Excel no hace. Excel no estima un SARIMA por máxima verosimilitud. "
              f"La estimación se queda en R: el libro toma θ̂ = {th}, Θ̂ = {Th}, "
              f"σ̂² = {air['sigma2']} y el log-verosimilitud ({air['loglik']}) como datos, en gris, "
              "y muestra lo que implican: residuales, Ljung–Box, pronósticos y bandas. Donde la "
              "cuenta de Excel no coincide con la de R, la hoja lo dice y da la diferencia.")
    f += 4
    h.seccion(f, "Cómo se usa")
    pasos = [
        "1. Las hojas van en el orden del capítulo, de M1 a M11. Conviene tener el capítulo abierto al lado.",
        "2. Las celdas con borde naranja son las que se completan. Su instrucción está al lado o en el "
        "comentario de la celda (el triángulo rojo de la esquina).",
        "3. En un bloque de celdas basta escribir la primera fórmula y arrastrarla: los $ de las "
        "fórmulas ya resueltas muestran qué se fija y qué se mueve.",
        "4. Cada resultado tiene una comprobación al lado. Se pone en verde (✔) cuando coincide con el "
        "capítulo; hasta entonces sale en rojo (✘). Unas pocas comprueban lo que el libro ya trae resuelto "
        "(los datos, los ejemplos hechos) y salen en verde desde el principio.",
        "5. Las celdas amarillas se pueden cambiar para explorar. Mientras no tengan los valores del "
        "capítulo, las comprobaciones que dependen de ellas muestran «—».",
        "6. Las celdas que dependen de una que falta muestran #¡DIV/0! o #¡VALOR! (#DIV/0! o #VALUE! en "
        "un Excel en inglés) hasta que se completa. Es normal, y vale también entre hojas: el M4 y el M6 leen "
        "el M3, el M7 lee el M5 y el M6, y el M8 lee el M1.",
        "7. Si al abrir el libro las celdas salen vacías o en cero, pulsa «Habilitar edición»: en la vista "
        "protegida Excel no calcula.",
    ]
    for i, p in enumerate(pasos):
        h.parrafo(f + 1 + i, p)
    f += len(pasos) + 2
    h.seccion(f, "Colores")
    muestras = [
        ("Entrada: se puede cambiar", "fill", R_ENTRADA, None),
        ("Completa aquí: la fórmula es tuya", "border", None, B_CLAVE),
        ("Dato de R o del capítulo: no se toca", "fill", R_DATO, None),
        ("✔ coincide con el capítulo", "ok", R_OK, None),
        ("✘ revisar, o falta completar", "mal", R_MAL, None),
        ("— comprobación en pausa (otra entrada)", "pausa", None, None),
    ]
    for i, (s, tipo, relleno, borde) in enumerate(muestras):
        fila = f + 1 + i
        c_ = h.ws.cell(fila, 2, s)
        c_.border = borde or B_FINO
        if relleno:
            c_.fill = relleno
        if tipo == "ok":
            c_.font = Font(bold=True, color="006100")
        elif tipo == "mal":
            c_.font = Font(bold=True, color="9C0006")
        elif tipo == "fill" and relleno is R_DATO:
            c_.font = F_DATO
    f += len(muestras) + 2

    h.seccion(f, "Avance por hoja")
    h.encabezados(f + 1, 2, ["Hoja", "Comprobaciones en verde", "de", "Qué cubre"], ajuste=True)
    for i, (hoja, que) in enumerate(ref):
        fila = f + 2 + i
        celdas = [c_ for (n_, c_, _) in lb.comprobaciones if n_ == hoja.nombre]
        c_ = h.ws.cell(fila, 2, hoja.nombre)
        c_.hyperlink = f"#'{hoja.nombre}'!A1"
        c_.font = Font(color="0563C1", underline="single")
        if celdas:
            suma = "+".join(f'({hoja.q}{x}="✔")' for x in celdas)
            h.put(f"C{fila}", f"={suma}", align=CENTRO, font=F_NEGRITA)
            h.put(f"D{fila}", len(celdas), align=CENTRO)
        h.put(f"E{fila}", que)
    total = f + 2 + len(ref)
    h.put(f"B{total}", "Total", font=F_NEGRITA)
    h.put(f"C{total}", f"=SUM(C{f + 2}:C{total - 1})", align=CENTRO, font=F_NEGRITA)
    h.put(f"D{total}", f"=SUM(D{f + 2}:D{total - 1})", align=CENTRO, font=F_NEGRITA)
    f = total + 2

    h.seccion(f, "Dónde la cuenta de Excel no es la de R, medido")
    h.encabezados(f + 1, 2, ["Qué", "R (capítulo)", "Este libro", "Por qué"], ajuste=False)
    for i, fila_ in enumerate(lb.diferencias):
        for j, v in enumerate(fila_):
            c_ = h.ws.cell(f + 2 + i, 2 + j, v)
            c_.alignment = AJUSTE
        h.ws.row_dimensions[f + 2 + i].height = 46
    h.ws.column_dimensions["E"].width = 16
    f += len(lb.diferencias) + 3

    h.seccion(f, "Funciones que usa el libro (Excel en español · en inglés)")
    funciones = [
        ("SUMAPRODUCTO · SUMPRODUCT", "ACF, Ljung–Box, MAE, MAPE"),
        ("INDICE · INDEX", "recortar un rango: INDEX(r,1):INDEX(r,n−k)"),
        ("DESVIA2 · DEVSQ", "Σ(x − x̄)², el denominador de la ACF"),
        ("VAR · VAR", "varianza muestral (divisor n − 1), como var() de R"),
        ("SUMA.CUADRADOS · SUMSQ", "Σψ²"),
        ("SUMAXMENOSY2 · SUMXMY2", "Σ(y − ŷ)², para el RMSE"),
        ("DISTR.CHICUAD.CD · CHISQ.DIST.RT", "valor p de Ljung–Box"),
        ("INV.NORM.ESTAND · NORM.S.INV", "z de las bandas: 1.2816 y 1.9600"),
        ("ESTIMACION.LINEAL · LINEST", "la regresión armónica (M10)"),
        ("DESREF · OFFSET", "elegir 2K columnas de Fourier"),
        ("DIA · DAY, FIN.MES · EOMONTH", "días del mes (M9)"),
        ("RESIDUO · MOD, ENTERO · INT", "el algoritmo de la Pascua (M9)"),
        ("JERARQUIA · RANK", "ordenar modelos y métodos"),
    ]
    for i, (a, b) in enumerate(funciones):
        h.put(f"B{f + 1 + i}", a)
        h.put(f"D{f + 1 + i}", b)
    f += len(funciones) + 2
    h.parrafo(f, "En un Excel en español las funciones aparecen con su nombre en español y el "
              "separador de argumentos suele ser el punto y coma (;). Las instrucciones las escriben "
              "con su nombre en inglés y la coma, como las guarda el archivo. Excel traduce las ya "
              "escritas al abrir el libro.")
    f += 2
    h.seccion(f, "Compatibilidad y datos")
    h.parrafo(f + 1, "Está comprobado en Microsoft Excel. Solo usa funciones clásicas, sin LET, LAMBDA, SEQUENCE "
              "ni matrices dinámicas, que también existen en LibreOffice Calc y en Google Sheets (Archivo › "
              "Importar), aunque en ellos todavía no se ha probado.")
    D = lb.D
    h.parrafo(f + 2, "Datos: AirPassengers y USAccDeaths, de los datasets de R; la TRM mensual, de la "
              f"{D['trm']['fuente']}. Coeficientes y cifras de comparación: los que el capítulo calcula en R "
              f"(precalculo/salidas/cap5_sarima.json, generado el {J['generado']}). Libro generado por "
              "precalculo/genera_excel_cap5.py; nada se tecleó a mano.")


def hoja_datos(lb):
    D = lb.D
    h = Hoja(lb, "Datos", "Datos · las tres series del capítulo",
             "AirPassengers (1949–1960), USAccDeaths (1973–1978) y la TRM (2015–2026), tal como las usa el capítulo.",
             anchos={"A": 10, "B": 12, "C": 13, "D": 3, "E": 10, "F": 12, "G": 3, "H": 10, "I": 12, "J": 3,
                     "K": 60})
    f0 = 5
    series = [
        ("airpassengers", 1, ["Fecha", "Pasajeros", "log(Pasajeros)"], "AirPassengers"),
        ("usaccdeaths", 5, ["Fecha", "Muertes"], "USAccDeaths"),
        ("trm", 8, ["Fecha", "TRM"], "TRM"),
    ]
    for clave_, col, enc, nombre in series:
        s = D[clave_]
        anio, mes = s["inicio"]
        h.encabezados(f0 - 1, col, enc)
        for i, v in enumerate(s["valores"]):
            fila = f0 + i
            m = mes - 1 + i
            h.put(f"{L(col)}{fila}", date(anio + m // 12, m % 12 + 1, 1), fmt=FMES)
            h.put(f"{L(col + 1)}{fila}", v, fmt="0" if isinstance(v, int) else F2)
            if len(enc) == 3:
                h.put(f"{L(col + 2)}{fila}", f"=LN({L(col + 1)}{fila})", fmt="0.00000")
        ultima = f0 + len(s["valores"]) - 1
        tabla = Table(displayName=f"Tabla_{nombre}",
                      ref=f"{L(col)}{f0 - 1}:{L(col + len(enc) - 1)}{ultima}")
        tabla.tableStyleInfo = TableStyleInfo(name="TableStyleLight9", showRowStripes=True)
        h.ws.add_table(tabla)
    h.ws.freeze_panes = "A5"
    notas = [
        f"AirPassengers · {D['airpassengers']['descripcion']} ({D['airpassengers']['unidad']}). "
        f"Fuente: {D['airpassengers']['fuente']}.",
        f"USAccDeaths · {D['usaccdeaths']['descripcion']} ({D['usaccdeaths']['unidad']}). "
        f"Fuente: {D['usaccdeaths']['fuente']}.",
        f"TRM · {D['trm']['descripcion']} ({D['trm']['unidad']}). Fuente: {D['trm']['fuente']}. "
        "Copia congelada, redondeada a dos decimales.",
        "Las demás hojas leen estas columnas. No se ordenan, no se filtran y no se borran filas: las "
        "fórmulas cuentan con que la fila 5 es el primer mes.",
    ]
    for i, s in enumerate(notas):
        c_ = h.put(f"K{f0 + 2 * i}", s, align=AJUSTE)
        h.ws.row_dimensions[f0 + 2 * i].height = 46
    h.put("K3", "Comprobación de los datos", font=F_NEGRITA)
    for ref, rango, clave_, n_ in (("L5", "B5:B148", "airpassengers", 144), ("L7", "F5:F76", "usaccdeaths", 72),
                                   ("L9", "I5:I142", "trm", 138)):
        suma = round(sum(D[clave_]["valores"]), 6)
        h.check(ref, f"AND(COUNT({rango})={n_},ABS(SUM({rango})-{suma})<1E-6)",
                f"{D[clave_]['nombre']} trae sus {n_} meses, con la suma de datos_series.json")
    return h


# ------------------------------------------------------------------- M1
def hoja_m1(lb):
    J = lb.J
    A = J["airpassengers"]
    h = Hoja(lb, "M1 Firma", "M1 · La firma de la estacionalidad",
             "Ver la estacionalidad en el mapa mes × año y medirla en la ACF, en los rezagos 12, 24 y 36.",
             anchos={"A": 7, "B": 9, "H": 9}, ancho_texto=17)
    for col in range(3, 14):
        h.ws.column_dimensions[L(col)].width = 9
    h.seccion(4, "1 · Verla antes de medirla: el mapa mes × año")
    h.parrafo(5, "La fila es el año y la columna el mes. La celda del año a y el mes m es la observación "
              "número 12·(a − 1949) + m de la columna de Datos. Si un mes es siempre alto aparece una "
              "banda vertical; si el patrón crece con el nivel, las bandas se ensanchan hacia abajo.")
    for nombre_mapa, f_enc, col_datos in (("AirPassengers", 7, "B"), ("log(AirPassengers)", 22, "C")):
        h.put(f"A{f_enc - 1}", "mes →", font=F_GUION)
        for m in range(12):
            h.put(f"{L(2 + m)}{f_enc - 1}", m + 1, font=F_GUION, align=CENTRO)
        h.encabezados(f_enc, 1, ["Año"] + MESES)
        h.put(f"O{f_enc}", nombre_mapa, font=F_NEGRITA)
        for i in range(12):
            fila = f_enc + 1 + i
            h.put(f"A{fila}", 1949 + i, font=F_NEGRITA, align=CENTRO)
            for m in range(12):
                col = L(2 + m)
                h.put(f"{col}{fila}",
                      f"=INDEX(Datos!${col_datos}$5:${col_datos}$148,12*($A{fila}-$A${f_enc + 1})+{col}${f_enc - 1})",
                      fmt="0" if col_datos == "B" else "0.00", align=CENTRO)
        rango = f"B{f_enc + 1}:M{f_enc + 12}"
        h.ws.conditional_formatting.add(rango, ColorScaleRule(
            start_type="min", start_color="F1F5F3", mid_type="percentile", mid_value=50,
            mid_color="FDBA74", end_type="max", end_color="C2410C"))
    h.parrafo(36, "Lectura. En la serie cruda las bandas de julio y agosto se ensanchan año a año: la "
              "amplitud estacional crece con el nivel. En log(AirPassengers) el ancho se mantiene: el "
              "logaritmo vuelve aditiva una estacionalidad multiplicativa, que es la que un SARIMA modela.")

    h.seccion(38, "2 · Medirla: la ACF por fórmula, hasta el rezago 36")
    h.parrafo(39, "ρ̂_k = Σ (x_t − x̄)(x_{t+k} − x̄) / Σ (x_t − x̄)², con la media y el denominador de toda "
              "la serie, como Acf() de R. En la fórmula, INDEX(r,1):INDEX(r,n−k) es la serie sin sus últimas k "
              "observaciones e INDEX(r,1+k):INDEX(r,n) la serie sin las primeras k. COEF.DE.CORREL (CORREL) "
              "no sirve: centra cada tramo con su propia media y divide por su propio tamaño, así que da "
              "otro número.")
    h.completa(40, "(1) ∇log y en la columna D: la celda menos la de arriba. (2) ∇TRM en la columna F. "
               "(3) Las ACF de las columnas J y L: la columna I es el ejemplo resuelto; copia su fórmula "
               "y cambia el rango por el de tu serie y 144 por su n (D48:D190 y 143; F48:F184 y 137).")
    # n, media y banda de cada serie
    f1, n_ap = 47, 144
    series = [  # columna de la serie, primera y última fila, columna de su ACF
        (3, f1, f1 + 143, 9),        # log y
        (4, f1 + 1, f1 + 143, 10),   # ∇ log y
        (5, f1, f1 + 137, 11),       # TRM
        (6, f1 + 1, f1 + 137, 12),   # ∇TRM
    ]
    h.put("H42", "n", font=F_NEGRITA)
    h.put("H43", "banda", font=F_NEGRITA)
    for col, a, b, col_acf in series:
        c_ = L(col)
        h.formula(f"{L(col_acf)}42", f"=COUNT({c_}{f1}:{c_}{f1 + 143})", fmt="0")
        h.formula(f"{L(col_acf)}43", f"=1.96/SQRT({L(col_acf)}42)", fmt=F4)
    h.encabezados(46, 1, ["t", "Fecha", "log y", "∇ log y", "TRM", "∇TRM"])
    h.encabezados(46, 8, ["k", "ρ̂ log y", "ρ̂ ∇log y", "ρ̂ TRM", "ρ̂ ∇TRM"])
    h.encabezados(46, 14, ["R: log y", "R: ∇log y", "R: TRM", "R: ∇TRM"])
    for i in range(n_ap):
        fila = f1 + i
        h.put(f"A{fila}", i + 1)
        h.put(f"B{fila}", f"=Datos!A{5 + i}", fmt=FMES)
        h.put(f"C{fila}", f"=Datos!C{5 + i}", fmt="0.00000")
        if i == 0:
            h.guion(f"D{fila}")
        else:
            h.clave(f"D{fila}", f"=C{fila}-C{fila - 1}",
                    "∇ log y_t = log y_t − log y_{t−1}: =C48-C47, el log y de esta fila menos el de la fila "
                    "de arriba. Escríbela en D48 y arrástrala hasta D190." if i == 1 else None, fmt="0.00000")
        if i < 138:
            h.put(f"E{fila}", f"=Datos!I{5 + i}", fmt=F2)
            if i == 0:
                h.guion(f"F{fila}")
            else:
                h.clave(f"F{fila}", f"=E{fila}-E{fila - 1}",
                        "∇TRM_t = TRM_t − TRM_{t−1}. Escríbela en F48 y arrástrala hasta F184."
                        if i == 1 else None, fmt=F2)
    fuentes_r = [A["firma"]["airpassengers_log"]["acf"], A["combinaciones"]["d1_D0"]["acf"],
                 A["firma"]["trm"]["acf"], A["firma"]["trm_diff"]["acf"]]
    for k in range(1, 37):
        fila = f1 + k - 1
        h.put(f"H{fila}", k, align=CENTRO)
        for (col, a, b, col_acf) in series:
            f = f_acf(col, a, b, f"$H{fila}")
            if col_acf in (10, 12):
                instr = None
                if k == 1:
                    instr = ("Copia la fórmula de I47 y cambia $C$47:$C$190 por el rango de tu serie, y 144 "
                             "por su n: D48:D190 y 143 para ∇log y; F48:F184 y 137 para ∇TRM. Luego "
                             "arrástrala hasta el rezago 36.")
                h.clave(f"{L(col_acf)}{fila}", f, instr, fmt=F4)
            else:
                h.formula(f"{L(col_acf)}{fila}", f, fmt=F4)
        for j, fuente in enumerate(fuentes_r):
            h.dato(f"{L(14 + j)}{fila}", fuente[k - 1], fmt=F4)
        # bandas para los gráficos
        h.put(f"AE{fila}", "=I$43", fmt=F4)
        h.put(f"AF{fila}", "=-I$43", fmt=F4)
        h.put(f"AG{fila}", "=J$43", fmt=F4)
        h.put(f"AH{fila}", "=-J$43", fmt=F4)
        h.put(f"AI{fila}", "=L$43", fmt=F4)
        h.put(f"AJ{fila}", "=-L$43", fmt=F4)
    h.encabezados(46, 31, ["+banda I", "−banda I", "+banda J", "−banda J", "+banda L", "−banda L"])
    h.put("AE45", "Columnas para los gráficos", font=F_GUION)
    fk = f1 + 35
    h.put(f"H{fk + 1}", "¿= R?", font=F_NEGRITA)
    for j, (col, a, b, col_acf) in enumerate(series):
        check_lista(h, f"{L(col_acf)}{fk + 1}", col_acf, f1, fk, 14 + j, 0.000051,
                    f"ACF de la columna {L(col_acf)} = la de R en los 36 rezagos (± 5·10⁻⁵, el redondeo a 4 decimales)")
    # lectura: la tabla del capítulo
    f = fk + 4
    h.encabezados(f, 8, ["Serie", "ρ̂₁", "ρ̂₁₂", "ρ̂₂₄", "ρ̂₃₆", "Banda", "Lectura (capítulo)"])
    h.ws.column_dimensions["N"].width = 11
    lecturas = [("log(AirPassengers)", 9, "Tendencia y estacionalidad"),
                ("∇ log(AirPassengers)", 10, "Sin tendencia: quedan los picos en 12, 24, 36"),
                ("TRM (niveles)", 11, "Solo tendencia: ρ̂₁₂ grande y ninguna estación"),
                ("∇TRM", 12, "Nada: ni tendencia ni estación")]
    for i, (s, col_acf, lect) in enumerate(lecturas):
        fila = f + 1 + i
        h.put(f"H{fila}", s)
        for j, k in enumerate((1, 12, 24, 36)):
            h.put(f"{L(9 + j)}{fila}", f"={L(col_acf)}{f1 + k - 1}", fmt="0.000")
        h.put(f"M{fila}", f"={L(col_acf)}43", fmt="0.000")
        h.put(f"N{fila}", lect)
    h.parrafo(f + 6, "La trampa de la tabla: en niveles, la TRM tiene ρ̂₁₂ grande sin tener ninguna "
              "estacionalidad, porque una serie con tendencia da ρ̂_k grande en todos los rezagos. El "
              "diagnóstico se hace sobre la serie sin tendencia: la fila de ∇TRM es la que dice algo.",
              c1=8, c2=17)
    etiquetas(h, 37, f1, fk, 8, 6)
    h.put("AK46", "eje", font=F_GUION)
    grafico_barras(h, "S4", 37, 9, f1, fk, "ACF de log(AirPassengers): decae despacio",
                   banda=(31, 32))
    grafico_barras(h, "S20", 37, 10, f1, fk, "ACF de ∇log(AirPassengers): picos en 12, 24, 36",
                   banda=(33, 34))
    grafico_barras(h, "S47", 37, 12, f1, fk, "ACF de ∇TRM: ningún pico estacional",
                   banda=(35, 36))
    return h


# ------------------------------------------------------------------- M2
def hoja_m2(lb):
    J = lb.J
    T = J["teoricas"]
    he = EJEMPLOS["heladeria"]
    air = J["airpassengers"]["airline"]
    th, Th = [c_["valor"] for c_ in air["coeficientes"]]
    phi0, Phi0 = T["ar1_sar1"]["phi"], T["ar1_sar1"]["Phi"]
    h = Hoja(lb, "M2 Multiplicativo", "M2 · Notación SARIMA y el polinomio multiplicativo",
             "La parte estacional multiplica a la regular: el rezago 13 aparece solo, con un peso que no es libre.",
             anchos={"A": 6, "B": 38, "C": 13, "D": 13, "E": 7, "F": 60}, ancho_texto=12)
    guardia = f"AND($C$8={phi0},$C$9={Phi0})"
    # 1 · la heladería
    h.seccion(4, "1 · La heladería: pronosticar marzo de 2025 con un SARIMA(1,0,0)(1,0,0)₁₂")
    h.parrafo(5, "(1 − φB)(1 − ΦB¹²) y_t = ε_t. Ventas inventadas, medidas como desvío de su promedio. "
              "Se conocen tres meses y se pronostica marzo de 2025 por dos rutas: dos preguntas una "
              "detrás de otra, o una sola cuenta con el polinomio ya multiplicado.")
    h.completa(6, "los cinco pasos de C16:C20 y el peso del satélite en D27. La instrucción de cada uno está "
               "en la columna F.")
    h.put("B8", "φ (parte regular)")
    h.entrada("C8", phi0)
    h.put("B9", "Φ (parte estacional)")
    h.entrada("C9", Phi0)
    h.encabezados(11, 2, ["Ventas", "Febrero", "Marzo"])
    h.put("B12", 2024, align=CENTRO)
    h.entrada("C12", he["feb24"])
    h.entrada("D12", he["mar24"])
    h.put("B13", 2025, align=CENTRO)
    h.entrada("C13", he["feb25"])
    h.put("D13", "=C19", fmt="0.00", font=Font(bold=True, color=NARANJA))
    h.encabezados(15, 2, ["Paso", "Tu cálculo", "Capítulo", "✔", "Cómo se calcula"])
    sorpresa = he["mar24"] - phi0 * he["feb24"]
    pasos = [
        (16, "Sorpresa de marzo de 2024", "=D12-C8*C12", round(sorpresa, 10),
         "u = y(mar 24) − φ·y(feb 24): lo que febrero no explica de marzo."),
        (17, "Sorpresa esperada para marzo de 2025", "=C9*C16", round(Phi0 * sorpresa, 10),
         "Φ·u: la pregunta estacional, ¿se repite la sorpresa de hace un año?"),
        (18, "Pronóstico, ruta 2: dos preguntas", "=C8*C13+C17",
         round(phi0 * he["feb25"] + Phi0 * sorpresa, 10),
         "φ·y(feb 25) más la sorpresa esperada."),
        (19, "Pronóstico, ruta 1: el polinomio multiplicado", "=C8*C13+C9*D12-C8*C9*C12",
         round(phi0 * he["feb25"] + Phi0 * he["mar24"] - phi0 * Phi0 * he["feb24"], 10),
         "φ·y(t−1) + Φ·y(t−12) − φΦ·y(t−13). El satélite pesa −φΦ."),
        (20, "Si los dos modelos se sumaran", "=C8*C13+C9*D12",
         round(phi0 * he["feb25"] + Phi0 * he["mar24"], 10),
         "φ·y(feb 25) + Φ·y(mar 24): sin satélite, usa marzo de 2024 entero."),
    ]
    for fila, que, f, cap, instr in pasos:
        h.put(f"B{fila}", que)
        h.clave(f"C{fila}", f, instr, fmt="0.00")
        h.dato(f"D{fila}", cap, fmt="0.00")
        h.check(f"E{fila}", f"ABS(C{fila}-D{fila})<1E-9", f"heladería: {que}", guardia)
        h.put(f"F{fila}", instr)
        h.resultado(f"C{fila}", f"heladeria_{fila}", 1e-9)
    h.put("B21", "Diferencia entre sumar y multiplicar")
    h.formula("C21", "=C20-C19", fmt="0.00")
    h.dato("D21", round(Phi0 * phi0 * he["feb24"], 10), fmt="0.00")
    h.check("E21", "ABS(C21-D21)<1E-9", "heladería: la diferencia es Φ·φ·y(feb 24)", guardia)
    h.put("F21", "Es Φ·(φ·y(feb 24)): lo que marzo de 2024 traía de febrero, por Φ.")
    h.put("B22", "¿Las dos rutas dan lo mismo?")
    h.check("E22", "AND(COUNT(C18:C19)=2,ABS(C18-C19)<1E-9)",
            "heladería: las dos rutas coinciden con cualquier φ y Φ")
    h.put("F22", "Cambia φ y Φ: esta comprobación sigue en verde. Prueba Φ = 0, luego φ = 0 y luego φ = Φ = 1.")
    h.encabezados(24, 2, ["Mes conocido", "Rezago", "Peso"])
    pesos = [("Febrero de 2025", 1, "=C8"), ("Marzo de 2024", 12, "=C9")]
    for i, (s, k, f) in enumerate(pesos):
        h.put(f"B{25 + i}", s)
        h.put(f"C{25 + i}", k, align=CENTRO)
        h.formula(f"D{25 + i}", f, fmt="0.00")
    h.put("B27", "Febrero de 2024 (el satélite)")
    h.put("C27", 13, align=CENTRO)
    h.clave("D27", "=-C8*C9", "El satélite pesa −φΦ: sale de los otros dos, no es un parámetro nuevo.",
            fmt="0.00")
    h.check("E27", f"ABS(D27-({round(-phi0 * Phi0, 10)}))<1E-9", "heladería: el satélite pesa −φΦ", guardia)
    h.put("F27", "−φΦ: con φ = 0.6 y Φ = 0.7, −0.42.")

    # 2 · el polinomio
    h.seccion(30, "2 · El polinomio multiplicado, rezago a rezago")
    h.parrafo(31, "Multiplicar dos polinomios es multiplicar cada término del primero por cada término del "
              "segundo. En la tabla, la fila es un término regular y la columna uno estacional; el producto "
              "cae en el rezago que suma los dos. La celda de abajo a la derecha es el satélite.")
    h.completa(32, "el término cruzado de cada producto: D35 en la parte AR y D39 en la MA del airline.")
    h.encabezados(33, 2, ["AR: (1 − φB) × (1 − ΦB¹²)", "1·B⁰", "−Φ·B¹²"])
    h.put("B34", "1·B⁰", align=CENTRO)
    h.formula("C34", "=1*1", fmt="0.00")
    h.formula("D34", "=1*(-C9)", fmt="0.00")
    h.put("B35", "−φ·B", align=CENTRO)
    h.formula("C35", "=(-C8)*1", fmt="0.00")
    h.clave("D35", "=(-C8)*(-C9)", "El término cruzado: (−φ)·(−Φ), en el rezago 1 + 12 = 13.", fmt="0.00")
    h.encabezados(33, 7, ["rezago", "rezago"])
    h.dato("G34", 0)
    h.dato("H34", 12)
    h.dato("G35", 1)
    h.dato("H35", 13)
    h.encabezados(37, 2, ["MA del airline: (1 + θB) × (1 + ΘB¹²)", "1·B⁰", "Θ·B¹²"])
    h.put("B38", "1·B⁰", align=CENTRO)
    h.formula("C38", "=1*1", fmt=F4)
    h.formula("D38", "=1*C42", fmt=F4)
    h.put("B39", "θ·B", align=CENTRO)
    h.formula("C39", "=C41*1", fmt=F4)
    h.clave("D39", "=C41*C42", "θ·Θ: el coeficiente B13 del airline. No se estima, sale del producto.", fmt=F4)
    h.encabezados(37, 7, ["rezago", "rezago"])
    h.dato("G38", 0)
    h.dato("H38", 12)
    h.dato("G39", 1)
    h.dato("H39", 13)
    h.put("B41", "θ̂ (estimado en R)")
    h.dato("C41", th, fmt=F4)
    h.put("B42", "Θ̂ (estimado en R)")
    h.dato("C42", Th, fmt=F4)
    h.put("B43", "B13 del airline: θ̂·Θ̂")
    h.formula("C43", "=D39", fmt=F4)
    b13 = T["ma1_sma1"]["ma_expandido"][12]
    h.dato("D43", b13, fmt=F4)
    h.check("E43", "ABS(C43-D43)<=0.000051", "M2: el satélite MA del airline vale θΘ = 0.2238")
    h.encabezados(45, 2, ["Polinomio ya multiplicado", "j", "AR: coef. de Bʲ", "peso de y(t−j)"])
    h.put("F45", "MA del airline: coef. de Bʲ", font=F_ENC, fill=R_ENC, border=B_FINO)
    for j in range(14):
        fila = 46 + j
        h.put(f"C{fila}", j, align=CENTRO)
        h.formula(f"D{fila}", f"=SUMIF($G$34:$H$35,C{fila},$C$34:$D$35)", fmt="0.00")
        if j == 0:
            h.guion(f"E{fila}")
        else:
            h.formula(f"E{fila}", f"=-D{fila}", fmt="0.00")
        h.formula(f"F{fila}", f"=SUMIF($G$38:$H$39,C{fila},$C$38:$D$39)", fmt=F4)
    h.put("B46", f"Con φ = {phi0} y Φ = {Phi0}: y_t = {phi0}·y(t−1) + {Phi0}·y(t−12) − "
                 f"{round(phi0 * Phi0, 4)}·y(t−13) + ε_t", font=F_GUION)
    h.put("B47", "Los rezagos 2 a 11 valen cero: un AR(13) con dos parámetros libres.", font=F_GUION)

    # 3 · momentos con los pesos ψ
    fpsi0 = 169                           # fila de ψ_0 (y de t = 1 en la simulación)
    fpsi1 = fpsi0 + N_PSI - 1
    rpsi = f"$B${fpsi0}:$B${fpsi1}"
    h.seccion(62, "3 · Media, varianza y autocorrelación: los pesos ψ")
    h.parrafo(63, "El polinomio ya multiplicado es un ARMA corriente: y_t = Σ ψ_j ε_{t−j}, con "
              "ψ_j = φψ_{j−1} + Φψ_{j−12} − φΦψ_{j−13} y ψ_0 = 1. Entonces γ₀/σ² = Σψ_j² y "
              "ρ_k = Σψ_jψ_{j+k} / Σψ_j². Excel suma 720 pesos: con los valores del capítulo (Φ = 0.7, "
              "φ hasta 0.95) lo que queda fuera es despreciable; con Φ cerca de 1 harían falta muchos más. "
              f"Los pesos van en la columna B, desde la fila {fpsi0 - 13}.")
    h.completa(64, f"(1) La recursión de ψ en B{fpsi0 + 1}:B{fpsi1} (columnas de cálculo, más abajo). "
               "(2) La ACF teórica ρ_k en J70:J105. (3) γ₀/σ² exacta y factorizada.")
    h.encabezados(66, 2, ["Magnitud", "Tu cálculo", "Capítulo", "✔", "Cómo se calcula"])
    psi0 = psi_ar1_sar1(phi0, Phi0, N_PSI)
    exacta = sum(v * v for v in psi0)
    fact = 1 / ((1 - phi0 ** 2) * (1 - Phi0 ** 2))
    filas3 = [
        (67, "γ₀/σ² exacta = Σψ²", f"=SUMSQ({rpsi})", round(exacta, 3), 0.0005,
         "Σψ_j²: SUMSQ (SUMA.CUADRADOS) de la columna de ψ."),
        (68, "γ₀/σ² factorizada", "=1/((1-C8^2)*(1-C9^2))", round(fact, 3), 0.0005,
         "1 / ((1 − φ²)(1 − Φ²)): multiplicar las dos varianzas por separado."),
    ]
    for fila, que, f, cap, tol, instr in filas3:
        h.put(f"B{fila}", que)
        h.clave(f"C{fila}", f, instr, fmt="0.000")
        h.dato(f"D{fila}", cap, fmt="0.000")
        h.check(f"E{fila}", f"ABS(C{fila}-D{fila})<={tol}", f"M2: {que}", guardia)
        h.put(f"F{fila}", instr)
    h.put("B69", "Error de la factorización")
    h.formula("C69", "=(C68-C67)/C67", fmt="0.0%")
    h.dato("D69", round((fact - exacta) / exacta, 3), fmt="0.0%")
    h.check("E69", "ABS(C69-D69)<=0.0005", "M2: error de la factorización", guardia)
    h.put("F69", "Negativo: la factorización se queda corta. Con parte AR no hay regalo.")
    h.put("B70", "ψ₁₂ = φ¹² + Φ (dos caminos al rezago 12)")
    h.formula("C70", f"=INDEX({rpsi},13)", fmt="0.00000")
    h.formula("D70", "=C8^12+C9", fmt="0.00000")
    h.check("E70", "ABS(C70-D70)<1E-12", "M2: ψ₁₂ = φ¹² + Φ, con cualquier φ y Φ")
    h.put("F70", "Doce pasos regulares (φ¹²) o uno estacional (Φ): el peso del rezago 12 suma los dos.")
    # ACF teórica, k = 1..36 (columna J)
    h.encabezados(66, 9, ["k", "ρ_k teórica", "R (ARMAacf)"])
    for k in range(1, 37):
        fila = 69 + k
        h.put(f"I{fila}", k, align=CENTRO)
        instr = ("ρ_k = Σψ_jψ_{j+k} / Σψ_j²: SUMPRODUCT de la columna de ψ sin sus últimos k pesos "
                 "por la columna sin sus primeros k, dividido por SUMSQ. Arrástrala hasta k = 36.") if k == 1 else None
        h.clave(f"J{fila}",
                f"=SUMPRODUCT($B${fpsi0}:INDEX({rpsi},{N_PSI}-I{fila}),INDEX({rpsi},1+I{fila}):$B${fpsi1})/SUMSQ({rpsi})",
                instr, fmt=F4)
        h.dato(f"K{fila}", T["ar1_sar1"]["acf"][k - 1], fmt=F4)
    h.ws.column_dimensions["I"].width = 6
    h.ws.column_dimensions["J"].width = 13
    h.ws.column_dimensions["K"].width = 13
    h.put("I106", "¿= R?", font=F_NEGRITA)
    h.check("J106", f"SUMPRODUCT(--(ABS(J70:J105-K70:K105)<=0.000051))=36",
            "M2: ACF teórica del AR(1)×SAR(1) = ARMAacf de R en los 36 rezagos", guardia)
    h.encabezados(72, 2, ["Los satélites", "ρ", "Capítulo"])
    sat = [("ρ₁", 1), ("ρ₁₁ (satélite izquierdo)", 11), ("ρ₁₂", 12), ("ρ₁₃ (satélite derecho)", 13), ("ρ₂₄", 24)]
    for i, (s, k) in enumerate(sat):
        fila = 73 + i
        h.put(f"B{fila}", s)
        h.formula(f"C{fila}", f"=J{69 + k}", fmt=F4)
        h.dato(f"D{fila}", T["ar1_sar1"]["acf"][k - 1], fmt=F4)
    h.put("B78", "ρ₁·ρ₁₂ (el producto de los dos caminos)")
    h.formula("C78", "=C73*C75", fmt=F4)
    h.dato("D78", round(T["ar1_sar1"]["acf"][0] * T["ar1_sar1"]["acf"][11], 4), fmt=F4)
    h.parrafo(79, "ρ₁₃ ≈ ρ₁·ρ₁₂: subir un año y retroceder un mes lleva al rezago 13. Con parte AR la "
              "igualdad es solo aproximada; en el airline, que es solo MA, es exacta (M4).", c2=6)
    h.encabezados(81, 2, ["La tabla del capítulo (Φ = 0.7)", "φ¹²", "γ₀/σ² exacta", "factorizada"])
    h.put("F81", "error", font=F_ENC, fill=R_ENC, border=B_FINO)
    for i, phi in enumerate(PHIS_TABLA):
        p = psi_ar1_sar1(phi, Phi0, N_PSI)
        ex = sum(v * v for v in p)
        fa = 1 / ((1 - phi ** 2) * (1 - Phi0 ** 2))
        fila = 82 + i
        h.dato(f"B{fila}", f"φ = {phi}")
        h.dato(f"C{fila}", round(phi ** 12, 3), fmt="0.000")
        h.dato(f"D{fila}", round(ex, 3), fmt="0.000")
        h.dato(f"E{fila}", round(fa, 3), fmt="0.000")
        h.dato(f"F{fila}", round((fa - ex) / ex, 3), fmt="0.0%")
    h.parrafo(86, "Para reproducirla: cambia φ en C8 a 0.8, 0.9 y 0.95 y lee las filas 67 a 69. Con φ "
              "cerca de 1 la colisión φ¹² domina y la factorización se queda muy por debajo: la varianza de "
              "un SARIMA con parte AR se calcula expandiendo el polinomio, no multiplicando varianzas.", c2=6)

    # 4 · la serie simulada
    S = SIMULACION
    fsim0 = fpsi0                          # fila de t = 1
    fs_a = fsim0 + S["quemado"]            # primera fila que entra en la ACF
    fs_b = fsim0 + S["n"] - 1
    h.seccion(108, "4 · Una serie simulada con el mismo modelo y un ruido fijo")
    h.parrafo(109, f"La columna E trae {S['n']} valores de un ruido N(0, 1) fijo (Box–Muller sobre "
              f"random.Random({S['semilla']}) de Python, redondeado a 4 decimales: no cambia al recalcular). "
              "La columna F lo pasa por el modelo: y_t = φy_{t−1} + Φy_{t−12} − φΦy_{t−13} + ε_t, desde 13 "
              f"ceros. La ACF usa los últimos {S['n'] - S['quemado']} valores: los {S['quemado']} primeros se "
              "descartan para que el arranque en cero no pese.")
    h.completa(110, f"la recursión de y en F{fsim0}:F{fs_b}. Después mira cómo asoman los satélites en 11 y 13.")
    h.encabezados(112, 9, ["k", "ρ̂_k simulada", "ρ_k teórica", "+banda", "−banda"])
    n_sim = S["n"] - S["quemado"]
    for k in range(1, 37):
        fila = 112 + k
        h.put(f"I{fila}", k, align=CENTRO)
        h.formula(f"J{fila}", f_acf(6, fs_a, fs_b, f"I{fila}"), fmt=F4)
        h.formula(f"K{fila}", f"=J{69 + k}", fmt=F4)
        h.formula(f"L{fila}", f"=1.96/SQRT({n_sim})", fmt=F4)
        h.formula(f"M{fila}", f"=-L{fila}", fmt=F4)
    ruido = ruido_fijo(S["n"], S["semilla"])
    y = [0.0] * 13
    for t in range(S["n"]):
        y.append(phi0 * y[-1] + Phi0 * y[-12] - phi0 * Phi0 * y[-13] + ruido[t])
    y = y[13:]
    usados = y[S["quemado"]:]
    r_sim = acf(usados, 36)
    h.encabezados(113, 2, ["Comprobación", "Tu serie", "Referencia"])
    h.put("B114", f"Suma de y en los {n_sim} valores usados")
    h.formula("C114", f"=SUM(F{fs_a}:F{fs_b})", fmt="0.0000")
    h.dato("D114", round(sum(usados), 6), fmt="0.0000")
    h.check("E114", "ABS(C114-D114)<=0.000001", "M2: la serie simulada coincide con la de referencia", guardia)
    h.put("B115", "ρ̂₁₁ y ρ̂₁₃ fuera de la banda")
    h.formula("C115", f'=IF(AND(J123>L123,J125>L125),"sí","no")')
    h.dato("D115", "sí")
    h.check("E115", 'C115="sí"', "M2: los satélites asoman en la ACF simulada", guardia)
    h.put("F114", "La referencia la calcula genera_excel_cap5.py con la misma recursión.")
    h.put("F115", f"ρ̂₁₁ = {r_sim[10]:.3f} y ρ̂₁₃ = {r_sim[12]:.3f} en la simulación de referencia.")
    etiquetas(h, 26, 70, 105, 9, 6)
    etiquetas(h, 26, 113, 148, 9, 6)
    grafico_barras(h, "N66", 26, 10, 70, 105, "ACF teórica del AR(1)×SAR(1)", nombre="ρ_k teórica",
                   resaltar=(11, 12, 13, 24, 36))
    grafico_barras(h, "N112", 26, 10, 113, 148, "ACF de la serie simulada frente a la teórica",
                   nombre="ρ̂_k simulada", resaltar=(11, 12, 13, 24, 36), banda=(12, 13),
                   teorica=(11, "ρ_k teórica"))

    # columnas de cálculo
    h.seccion(fpsi0 - 17, "Columnas de cálculo")
    h.parrafo(fpsi0 - 16, "ψ: las 13 primeras filas son ψ_j = 0 para j < 0, para que la misma fórmula valga desde "
              "j = 1. La serie simulada arranca igual, con 13 ceros.")
    h.encabezados(fpsi0 - 14, 1, ["j", "ψ_j"])
    h.encabezados(fpsi0 - 14, 4, ["t", "ε_t (fijo)", "y_t"])
    for i in range(13):
        fila = fpsi0 - 13 + i
        h.put(f"A{fila}", -13 + i, font=F_GUION)
        h.dato(f"B{fila}", 0)
        h.put(f"D{fila}", -12 + i, font=F_GUION)
        h.dato(f"F{fila}", 0)
    for j in range(N_PSI):
        fila = fpsi0 + j
        h.put(f"A{fila}", j)
        if j == 0:
            h.formula(f"B{fila}", "=1", fmt="0.000000")
        else:
            h.clave(f"B{fila}", f"=$C$8*B{fila - 1}+$C$9*B{fila - 12}-$C$8*$C$9*B{fila - 13}",
                    "ψ_j = φ·ψ_{j−1} + Φ·ψ_{j−12} − φΦ·ψ_{j−13}. Con $ en φ y Φ; arrástrala hasta j = 719."
                    if j == 1 else None, fmt="0.000000")
    for t in range(S["n"]):
        fila = fsim0 + t
        h.put(f"D{fila}", t + 1)
        h.dato(f"E{fila}", ruido[t], fmt=F4)
        h.clave(f"F{fila}", f"=$C$8*F{fila - 1}+$C$9*F{fila - 12}-$C$8*$C$9*F{fila - 13}+E{fila}",
                "y_t = φ·y_{t−1} + Φ·y_{t−12} − φΦ·y_{t−13} + ε_t. Arrástrala hasta t = 720."
                if t == 0 else None, fmt=F4)
    return h


# ------------------------------------------------------------------- M3
def hoja_m3(lb):
    J = lb.J
    A = J["airpassengers"]
    T_ = EJEMPLOS["tienda"]
    h = Hoja(lb, "M3 Diferenciar", "M3 · Diferenciación estacional: cuántas y en qué orden",
             "∇₁₂ resta la celda de arriba, ∇ la de la izquierda; las dos juntas, las cuatro esquinas de un cuadrado.",
             anchos={"A": 30, "B": 8}, ancho_texto=15)
    for col in range(3, 15):
        h.ws.column_dimensions[L(col)].width = 8
    h.seccion(4, "1 · La tienda inventada, celda a celda")
    h.parrafo(5, "y_t = 100 + (t − 1) + s_mes: la tienda parte de un nivel de 100 unidades en enero de 2022 (con "
              "el −6 de enero vende 94), gana una unidad por mes y repite cada año el mismo patrón, que suma "
              "cero. Con el interruptor en 1, desde 2024 crece tres unidades al mes.")
    h.completa(6, "las rejillas de ∇₁₂ (C30:N32), ∇ (C35:N38) y ∇∇₁₂ (C42:N44), y las dos cuentas de marzo de "
               "2024 (B57 y B58). La instrucción está en el comentario de la primera celda de cada rejilla.",
               c2=14)
    entradas = [(7, "Nivel inicial", T_["inicio"]), (8, "Crecimiento por mes", T_["pendiente"]),
                (9, "¿Acelera? (0 = no, 1 = sí)", 0), (10, "Año en que acelera", T_["anio_cambio"]),
                (11, "Crecimiento después", T_["pendiente_nueva"])]
    for fila, s, v in entradas:
        h.put(f"A{fila}", s)
        h.entrada(f"B{fila}", v)
    dv = DataValidation(type="whole", operator="between", formula1="0", formula2="1", allow_blank=False)
    h.ws.add_data_validation(dv)
    dv.add("B9")
    h.put("A12", "t en que acelera")
    h.formula("B12", f"=12*(B10-{T_['anio0']})")
    h.put("A13", "Patrón s_mes (suma cero)")
    for m in range(12):
        h.put(f"{L(3 + m)}12", MESES[m], font=F_ENC, align=CENTRO)
        h.entrada(f"{L(3 + m)}13", T_["patron"][m])
    h.put("A14", "mes →", font=F_GUION)
    for m in range(12):
        h.put(f"{L(3 + m)}14", m + 1, font=F_GUION, align=CENTRO)
    h.check("O13", "SUM(C13:N13)=0", "M3: el patrón de la tienda suma cero")
    guardia_t = ("AND($B$7={},$B$8={},$B$10={},$B$11={},SUMPRODUCT(ABS($C$13:$N$13-{{{}}}))=0)"
                 .format(T_["inicio"], T_["pendiente"], T_["anio_cambio"], T_["pendiente_nueva"],
                         ",".join(str(v) for v in T_["patron"])))
    anios = [T_["anio0"] + i for i in range(T_["anios"])]

    def rejilla(f_enc, titulo):
        h.put(f"A{f_enc}", titulo, font=F_NEGRITA)
        h.encabezados(f_enc, 2, ["Año"] + MESES)
        for i, a in enumerate(anios):
            h.put(f"B{f_enc + 1 + i}", a, align=CENTRO, font=F_NEGRITA)

    rejilla(16, "t (cuenta los meses)")
    for i in range(4):
        for m in range(12):
            h.formula(f"{L(3 + m)}{17 + i}", f"=12*($B{17 + i}-{T_['anio0']})+{L(3 + m)}$14")
    rejilla(22, "y_t")
    for i in range(4):
        for m in range(12):
            tc = f"{L(3 + m)}{17 + i}"
            h.formula(f"{L(3 + m)}{23 + i}",
                      f"=$B$7+IF(AND($B$9=1,{tc}>$B$12),($B$12-1)*$B$8+$B$11*({tc}-$B$12),({tc}-1)*$B$8)+{L(3 + m)}$13",
                      fmt="0")
    rejilla(28, "∇₁₂ y_t: menos la celda de arriba")
    rejilla(34, "∇ y_t: menos la celda de la izquierda")
    rejilla(40, "∇∇₁₂ y_t: ∇ aplicada a ∇₁₂")
    rejilla(46, "∇₁₂∇ y_t: el otro orden")
    for m in range(12):
        h.guion(f"{L(3 + m)}29")              # ∇₁₂ en 2022
        h.guion(f"{L(3 + m)}41")              # ∇∇₁₂ en 2022
        h.guion(f"{L(3 + m)}47")
    h.guion("C35")                            # ∇ en enero de 2022
    h.guion("C42")                            # ∇∇₁₂ en enero de 2023
    h.guion("C48")
    for i in range(1, 4):
        for m in range(12):
            c_ = L(3 + m)
            h.clave(f"{c_}{29 + i}", f"={c_}{23 + i}-{c_}{22 + i}",
                    "∇₁₂: la celda de y de la misma posición menos la de arriba (el mismo mes del año "
                    "anterior). Escríbela en C30 y arrástrala a C30:N32." if (i, m) == (1, 0) else None, fmt="0")
    for i in range(4):
        for m in range(12):
            c_ = L(3 + m)
            if i == 0 and m == 0:
                continue
            if m == 0:
                f = f"=C{23 + i}-N{22 + i}"
            else:
                f = f"={c_}{23 + i}-{L(2 + m)}{23 + i}"
            instr = None
            if (i, m) == (0, 1):
                instr = ("∇: la celda de y menos la de su izquierda. Escríbela en D35 y arrástrala a D35:N38.")
            if (i, m) == (1, 0):
                instr = ("A enero le toca el diciembre de la fila de arriba: C36 = C24 − N23. "
                         "Arrástrala a C37:C38.")
            h.clave(f"{c_}{35 + i}", f, instr, fmt="0")
    for i in range(1, 4):
        for m in range(12):
            c_ = L(3 + m)
            if i == 1 and m == 0:
                continue
            # ∇∇₁₂: ∇ aplicada a la rejilla de ∇₁₂; ∇₁₂∇: ∇₁₂ aplicada a la de ∇
            f = (f"=C{29 + i}-N{28 + i}" if m == 0 else f"={c_}{29 + i}-{L(2 + m)}{29 + i}")
            f2 = f"={c_}{35 + i}-{c_}{34 + i}"
            instr = ("∇∇₁₂: aplica ∇ a la rejilla de ∇₁₂ (la celda menos la de su izquierda; en enero, "
                     "menos el diciembre de arriba). Empieza en D42." if (i, m) == (1, 1) else None)
            h.clave(f"{c_}{41 + i}", f, instr, fmt="0")
            h.formula(f"{c_}{47 + i}", f2, fmt="0")
    # comprobaciones de las rejillas
    h.check("O30", "AND(COUNT(C30:N32)=36,SUMPRODUCT(ABS(C30:N32-(C24:N26-C23:N25)))<1E-9)",
            "M3: ∇₁₂ = la celda de arriba, en las 36 celdas")
    h.check("O36", "AND(COUNT(C35:N38)=47,SUMPRODUCT(ABS(D35:N38-(D23:N26-C23:M26)))"
                   "+SUMPRODUCT(ABS(C36:C38-(C24:C26-N23:N25)))<1E-9)",
            "M3: ∇ = la celda de la izquierda (enero, el diciembre de arriba)")
    h.check("O42", "AND(COUNT(C42:N44)=35,SUMPRODUCT(ABS(D42:N42-D48:N48))"
                   "+SUMPRODUCT(ABS(C43:N44-C49:N50))<1E-9)",
            "M3: ∇∇₁₂ = ∇₁₂∇: el orden de las restas no importa")
    y0, y1 = tienda(False), tienda(True)
    d12 = lambda y: [y[t] - y[t - 12] for t in range(12, 48)]
    dd = lambda y: [d12(y)[t] - d12(y)[t - 1] for t in range(1, 36)]
    sums = {0: (sum(d12(y0)), sum(abs(v) for v in dd(y0))),
            1: (sum(d12(y1)), sum(abs(v) for v in dd(y1)))}
    cond = (f"IF($B$9=0,AND(SUM(C30:N32)={sums[0][0]},SUMPRODUCT(ABS(D42:N44))+SUMPRODUCT(ABS(C43:C44))={sums[0][1]}),"
            f"AND(SUM(C30:N32)={sums[1][0]},SUMPRODUCT(ABS(D42:N44))+SUMPRODUCT(ABS(C43:C44))={sums[1][1]}))")
    h.check("O44", cond, "M3: las rejillas son las que imprime R en el capítulo", guardia_t)
    for ref, s in (("P30", "¿= celda de arriba?"), ("P36", "¿= celda de la izquierda?"),
                   ("P42", "¿= el otro orden?"), ("P44", "¿= R en el capítulo?"), ("P13", "¿suma cero?")):
        h.put(ref, s, font=F_GUION)
    # marzo de 2024
    h.seccion(52, "La cuenta de marzo de 2024", c2=15)
    t_mar = 12 * (2024 - T_["anio0"]) + 3
    filas = [(53, "y_t (marzo de 2024)", "=E25"), (54, "y_{t−1} (febrero de 2024)", "=D25"),
             (55, "y_{t−12} (marzo de 2023)", "=E24"), (56, "y_{t−13} (febrero de 2023)", "=D24")]
    for fila, s, f in filas:
        h.put(f"A{fila}", s)
        h.formula(f"B{fila}", f, fmt="0")
    h.put("A57", "∇₁₂ y_t = y_t − y_{t−12}")
    h.clave("B57", "=B53-B55", "y_t − y_{t−12}: marzo de 2024 menos marzo de 2023.", fmt="0")
    h.put("A58", "∇∇₁₂ y_t: las cuatro esquinas")
    h.clave("B58", "=B53-B54-B55+B56", "y_t − y_{t−1} − y_{t−12} + y_{t−13}: (1 − B)(1 − B¹²) = 1 − B − B¹² + B¹³.",
            fmt="0")
    h.put("C57", "capítulo:", font=F_GUION)
    h.put("C58", "capítulo:", font=F_GUION)
    h.dato("D57", f"=IF($B$9=0,{y0[t_mar - 1] - y0[t_mar - 13]},{y1[t_mar - 1] - y1[t_mar - 13]})", fmt="0")
    h.dato("D58", f"=IF($B$9=0,{y0[t_mar - 1] - y0[t_mar - 2] - y0[t_mar - 13] + y0[t_mar - 14]},"
                  f"{y1[t_mar - 1] - y1[t_mar - 2] - y1[t_mar - 13] + y1[t_mar - 14]})", fmt="0")
    h.check("E57", "AND(COUNT(B57)=1,B57=D57)", "M3: ∇₁₂ en marzo de 2024 (122 − 110 = 12)", guardia_t)
    h.check("E58", "AND(COUNT(B58)=1,B58=D58)", "M3: las cuatro esquinas en marzo de 2024 (128 − 121 − 110 + 105 = 2)", guardia_t)
    h.parrafo(59, "Sin aceleración: ∇₁₂ vale 12 en todas las celdas (lo que la tienda gana en un año) y "
              "∇∇₁₂ solo deja ceros. Con el interruptor en 1, ∇₁₂ sube de 14 a 36 a lo largo de 2024 y ∇∇₁₂ "
              "recoge el cambio: 2 en cada mes de 2024. ∇ sola nunca quita el patrón: cada año repite los "
              "mismos doce números, de −11 en enero a 5 en diciembre.")

    # 2 · las cuatro combinaciones
    fa0 = 90                              # fila de t = 1 en las columnas de cálculo
    fa1 = fa0 + 143
    h.seccion(61, "2 · Las cuatro combinaciones sobre log(AirPassengers)")
    h.parrafo(62, "Las columnas de cálculo, desde la fila 88, aplican cada diferencia a log y. La tabla "
              "mide cada serie: n, varianza (VAR, divisor n − 1 como var() de R), ρ̂₁ y ρ̂₁₂.")
    h.completa(63, "∇₁₂ log y en D102:D233 (la celda de doce filas más arriba) y ∇∇₁₂ log y en "
               "F103:F233 (∇ de la columna D). La tabla y sus comprobaciones se rellenan solas.")
    h.encabezados(65, 1, ["Serie", "d", "D", "n", "Varianza", "ρ̂₁", "ρ̂₁₂", "R: n", "R: var.",
                          "R: ρ̂₁", "R: ρ̂₁₂", "✔"], ajuste=True)
    for col in range(4, 12):
        h.ws.column_dimensions[L(col)].width = 10
    comb = [("log y", 0, 0, 3, fa0, "d0_D0"), ("∇ log y", 1, 0, 5, fa0 + 1, "d1_D0"),
            ("∇₁₂ log y", 0, 1, 4, fa0 + 12, "d0_D1"), ("∇∇₁₂ log y", 1, 1, 6, fa0 + 13, "d1_D1")]
    sobre = {s["D"]: s for s in A["sobrediferenciacion_estacional"]}
    comb.append(("∇∇₁₂² log y (D = 2)", 1, 2, 9, fa0 + 25, None))
    for i, (s, d, D_, col, fini, clave_j) in enumerate(comb):
        fila = 66 + i
        c_ = L(col)
        rng = f"{c_}{fini}:{c_}{fa1}"
        h.put(f"A{fila}", s)
        h.put(f"B{fila}", d, align=CENTRO)
        h.put(f"C{fila}", D_, align=CENTRO)
        h.formula(f"D{fila}", f"=COUNT({rng})", fmt="0")
        h.formula(f"E{fila}", f"=VAR({rng})", fmt=F6)
        h.formula(f"F{fila}", f_acf(col, fini, fa1, "1"), fmt=F4)
        h.formula(f"G{fila}", f_acf(col, fini, fa1, "12"), fmt=F4)
        if clave_j:
            cj = A["combinaciones"][clave_j]
            h.dato(f"H{fila}", cj["n"], fmt="0")
            h.dato(f"I{fila}", cj["varianza"], fmt=F6)
            h.dato(f"J{fila}", cj["acf1"], fmt=F4)
            h.dato(f"K{fila}", cj["acf12"], fmt=F4)
            cond = (f"AND(D{fila}=H{fila},ABS(E{fila}-I{fila})<=0.00000051,"
                    f"ABS(F{fila}-J{fila})<=0.000051,ABS(G{fila}-K{fila})<=0.000051)")
        else:
            h.dato(f"H{fila}", sobre[2]["n"], fmt="0")
            h.dato(f"I{fila}", sobre[2]["varianza"], fmt=F6)
            h.guion(f"J{fila}")
            h.guion(f"K{fila}")
            cond = f"AND(D{fila}=H{fila},ABS(E{fila}-I{fila})<=0.0000051)"
        h.check(f"L{fila}", cond, f"M3: n, varianza, ρ̂₁ y ρ̂₁₂ de {s} = R")
    h.put("A72", "¿∇∇₁₂ = ∇₁₂∇? (columnas F y G)")
    h.check("L72", f"AND(COUNT(F{fa0 + 13}:F{fa1})=131,SUMPRODUCT(ABS(F{fa0 + 13}:F{fa1}-G{fa0 + 13}:G{fa1}))<1E-12)",
            "M3: los operadores conmutan sobre log(AirPassengers)")
    h.parrafo(73, "La varianza mínima está en d = 1, D = 1 (0.002102). ∇ sola divide la varianza por 17 "
              "y sube ρ̂₁₂ a 0.84: no toca la estacionalidad. ∇₁₂ sola la reduce cincuenta veces y deja "
              "ρ̂₁ = 0.71, tendencia sin resolver. Con D = 2 la varianza vuelve a subir: sobra una diferencia.",
              c2=12)
    # columnas de cálculo
    h.seccion(86, "Columnas de cálculo", c2=10)
    h.encabezados(88, 1, ["Fecha", "t", "log y", "∇₁₂ log y", "∇ log y", "∇∇₁₂ log y", "∇₁₂∇ log y",
                          "∇₁₂² log y", "∇∇₁₂² log y"], ajuste=True)
    for i in range(144):
        fila = fa0 + i
        t = i + 1
        h.put(f"A{fila}", f"=Datos!A{5 + i}", fmt=FMES)
        h.put(f"B{fila}", t)
        h.put(f"C{fila}", f"=Datos!C{5 + i}", fmt="0.00000")
        if t <= 12:
            h.guion(f"D{fila}")
        else:
            h.clave(f"D{fila}", f"=C{fila}-C{fila - 12}",
                    "∇₁₂ log y_t = log y_t − log y_{t−12}: la celda de doce filas más arriba (el mismo mes "
                    "del año anterior). Escríbela en D102 y arrástrala hasta D233." if t == 13 else None,
                    fmt="0.00000")
        if t <= 1:
            h.guion(f"E{fila}")
        else:
            h.formula(f"E{fila}", f"=C{fila}-C{fila - 1}", fmt="0.00000")
        if t <= 13:
            h.guion(f"F{fila}")
            h.guion(f"G{fila}")
        else:
            h.clave(f"F{fila}", f"=D{fila}-D{fila - 1}",
                    "∇∇₁₂ log y_t: ∇ aplicada a la columna D, la celda menos la de arriba. Escríbela en "
                    "F103 y arrástrala hasta F233." if t == 14 else None, fmt="0.00000")
            h.formula(f"G{fila}", f"=E{fila}-E{fila - 12}", fmt="0.00000")
        if t <= 24:
            h.guion(f"H{fila}")
        else:
            h.formula(f"H{fila}", f"=D{fila}-D{fila - 12}", fmt="0.00000")
        if t <= 25:
            h.guion(f"I{fila}")
        else:
            h.formula(f"I{fila}", f"=H{fila}-H{fila - 1}", fmt="0.00000")
    return h


# ------------------------------------------------------------------- M4
def hoja_m4(lb):
    J = lb.J
    A = J["airpassengers"]
    T = J["teoricas"]
    th, Th = [c_["valor"] for c_ in A["airline"]["coeficientes"]]
    cj = A["combinaciones"]["d1_D1"]
    h = Hoja(lb, "M4 Identificar", "M4 · Identificar los órdenes estacionales",
             "Leer P y Q en los rezagos 12, 24 y 36 con la tabla del capítulo 3, y no contar un satélite como parámetro.",
             anchos={"A": 32, "B": 7}, ancho_texto=8)
    m3 = "'M3 Diferenciar'!"
    fw0, fw1 = 160, 290                 # columna local de w = ∇∇₁₂ log y (131 valores)
    h.seccion(4, "1 · La ACF de ∇∇₁₂ log y, con su banda")
    h.parrafo(5, "La serie ya diferenciada es la de la columna F del M3, copiada abajo (fila 158). La banda "
              "se calcula con las observaciones que quedan después de diferenciar, no con las 144 de partida.")
    h.completa(6, "la banda en C9, la marca «fuera» en D13:D48 (IF: si el valor absoluto de ρ̂ pasa la banda) y "
               "la ACF teórica del airline en D58:D60. La serie viene del M3: si allí falta, aquí sale en error.")
    h.put("A8", "n (observaciones de ∇∇₁₂ log y)")
    h.formula("C8", f"=COUNT(B{fw0}:B{fw1})", fmt="0")
    h.put("A9", "banda ±1.96/√n")
    h.clave("C9", "=1.96/SQRT(C8)", "1.96/√n con n = 131: la banda se mide sobre la serie que queda.", fmt=F4)
    h.dato("D9", cj["banda"], fmt=F4)
    h.check("E9", "ABS(C9-D9)<=0.000051", "M4: la banda con n = 131 (0.1712)")
    h.encabezados(12, 2, ["k", "ρ̂_k", "¿fuera?", "R", "teórica airline", "+banda", "−banda"])
    for k in range(1, 37):
        fila = 12 + k
        h.put(f"B{fila}", k, align=CENTRO)
        h.formula(f"C{fila}", f_acf(2, fw0, fw1, f"B{fila}"), fmt=F4)
        h.clave(f"D{fila}", f'=IF(ABS(C{fila})>$C$9,"fuera","")',
                'IF(ABS(ρ̂) > banda, "fuera", ""). Con $ en la banda; arrástrala hasta k = 36.' if k == 1 else None)
        h.dato(f"E{fila}", cj["acf"][k - 1], fmt=F4)
        teo = {1: "$D$58", 11: "$D$60", 12: "$D$59", 13: "$D$60"}.get(k, "0")
        h.formula(f"F{fila}", f"={teo}", fmt=F4)
        h.formula(f"G{fila}", "=$C$9", fmt=F4)
        h.formula(f"H{fila}", "=-$C$9", fmt=F4)
    check_lista(h, "C49", 3, 13, 48, 5, 0.000051, "M4: ACF de ∇∇₁₂ log y = R en los 36 rezagos")
    h.put("B49", "¿= R?", font=F_NEGRITA)
    fuera24 = [k for k in range(1, 25) if abs(cj["acf"][k - 1]) > cj["banda"]]
    h.put("A50", "Rezagos fuera de la banda entre 1 y 24")
    h.formula("C50", '=COUNTIF(D13:D36,"fuera")', fmt="0")
    h.dato("D50", len(fuera24), fmt="0")
    h.check("E50", "C50=D50", "M4: cinco rezagos fuera entre 1 y 24 (1, 3, 9, 12 y 23)")
    h.put("F50", "Son " + ", ".join(str(k) for k in fuera24) + ".", font=F_GUION)
    h.encabezados(52, 1, ["Rezago", "k", "ρ̂_k", "Capítulo", "Lectura"])
    for i, (k, lect) in enumerate(((11, "Satélite de la izquierda, dentro de la banda"),
                                   (12, "El pico estacional: pide Q = 1"),
                                   (13, "Satélite de la derecha, dentro de la banda"))):
        fila = 53 + i
        h.put(f"A{fila}", "Rezago estacional y sus satélites" if i == 0 else "")
        h.put(f"B{fila}", k, align=CENTRO)
        h.formula(f"C{fila}", f"=C{12 + k}", fmt="0.000")
        h.dato(f"D{fila}", round(cj["acf"][k - 1], 3), fmt="0.000")
        h.put(f"E{fila}", lect)

    h.seccion(57, "2 · La ACF teórica del airline ajustado", c2=8)
    h.put("A58", "ρ₁ = θ/(1 + θ²)")
    h.put("A59", "ρ₁₂ = Θ/(1 + Θ²)")
    h.put("A60", "ρ₁₁ = ρ₁₃ = ρ₁·ρ₁₂")
    h.put("B62", "θ̂")
    h.dato("C62", th, fmt=F4)
    h.put("B63", "Θ̂")
    h.dato("C63", Th, fmt=F4)
    h.clave("D58", "=C62/(1+C62^2)", "θ/(1 + θ²): en ρ₁ el factor estacional se cancela.", fmt=F4)
    h.clave("D59", "=C63/(1+C63^2)", "Θ/(1 + Θ²): la misma fórmula, en el rezago 12.", fmt=F4)
    h.clave("D60", "=D58*D59", "ρ₁·ρ₁₂: en un airline (solo MA) el satélite es exactamente el producto.", fmt=F4)
    acf_teo = T["ma1_sma1"]["acf"]
    for fila, k in ((58, 1), (59, 12), (60, 13)):
        h.dato(f"E{fila}", acf_teo[k - 1], fmt=F4)
        h.check(f"F{fila}", f"ABS(D{fila}-E{fila})<=0.0001", f"M4: ρ_{k} teórica del airline")
    h.put("G58", "muestral", font=F_GUION)
    h.formula("H58", "=C13", fmt="0.000")
    h.formula("H59", "=C24", fmt="0.000")
    h.formula("H60", "=C25", fmt="0.000")
    h.parrafo(64, "El rezago 13 cae a cinco milésimas de lo que el modelo predice y el 11 se queda corto. Con "
              "n = 131 el error típico de una autocorrelación ronda 1/√n = 0.087: los dos son compatibles con "
              "el mismo 0.1471. Dos parámetros explican cuatro autocorrelaciones.", c2=8)
    h.encabezados(66, 1, ["Proceso teórico", "", "ρ₁₂", "ρ₂₄", "ρ₃₆", "R: ρ₁₂", "✔"])
    sar = T["sar1_pos"]
    sma = T["sma1"]
    h.put("A67", f"SAR(1) con Φ = {sar['Phi']}")
    h.dato("B67", sar["Phi"])
    h.formula("C67", "=B67", fmt="0.000")
    h.formula("D67", "=B67^2", fmt="0.000")
    h.formula("E67", "=B67^3", fmt="0.000")
    h.dato("F67", sar["acf"][11], fmt=F4)
    h.check("G67", "AND(ABS(C67-F67)<=0.000051,ABS(D67-" + str(sar["acf"][23]) + ")<=0.000051)",
            "M4: SAR(1), la geométrica estirada doce veces")
    h.put("A68", f"SMA(1) con Θ = {sma['Theta']}")
    h.dato("B68", sma["Theta"])
    h.formula("C68", "=B68/(1+B68^2)", fmt=F4)
    h.formula("D68", "=0", fmt="0.000")
    h.formula("E68", "=0", fmt="0.000")
    h.dato("F68", sma["acf"][11], fmt=F4)
    h.check("G68", "ABS(C68-F68)<=0.000051", "M4: SMA(1), se corta tras el rezago 12")
    etiquetas(h, 26, 13, 48, 2, 6)
    grafico_barras(h, "J4", 26, 3, 13, 48, "ACF de ∇∇₁₂ log(AirPassengers) y la del airline",
                   banda=(7, 8), teorica=(6, "teórica airline"), resaltar=(11, 12, 13, 24, 36))

    # 3 · PACF por Durbin–Levinson (opcional)
    fj, fr, frr = 76, 77, 78           # filas de j, de ρ_j y de ρ al revés
    fk0 = 81                           # fila de k = 1
    h.seccion(72, "3 · Para afianzar (opcional): la PACF por Durbin–Levinson", c2=13)
    h.parrafo(73, "φ_11 = ρ₁. Para k ≥ 2: φ_kk = (ρ_k − Σ_{j<k} φ_{k−1,j} ρ_{k−j}) / (1 − Σ_{j<k} φ_{k−1,j} ρ_j) "
              f"y φ_kj = φ_{{k−1,j}} − φ_kk φ_{{k−1,k−j}}. La PACF es la diagonal, φ_kk. La fila {fr} lleva "
              f"ρ₁…ρ₃₆ y la {frr} los mismos al revés (ρ₃₆…ρ₁), para que Σ φ_{{k−1,j}} ρ_{{k−j}} sea un "
              "SUMPRODUCT de dos tramos de fila.", c2=13)
    h.completa(74, f"la diagonal φ_kk en la columna AN (filas {fk0} a {fk0 + 35}) y el resto de la fila k en "
               "C:AL. Opcional: su comprobación se queda en rojo si no se hace.", c2=13)
    h.put(f"B{fj}", "j →", font=F_GUION)
    h.put(f"B{fr}", "ρ_j", font=F_NEGRITA)
    h.put(f"B{frr}", "ρ al revés", font=F_NEGRITA)
    for j in range(1, 37):
        col = 2 + j
        h.put(f"{L(col)}{fj}", j, font=F_GUION, align=CENTRO)
        h.formula(f"{L(col)}{fr}", f"=INDEX($C$13:$C$48,{L(col)}${fj})", fmt=F4)
        h.formula(f"{L(col)}{frr}", f"=INDEX($C${fr}:$AL${fr},37-{L(col)}${fj})", fmt=F4)
    h.encabezados(fk0 - 1, 2, ["k"])
    h.put(f"AN{fk0 - 1}", "φ_kk (PACF)", font=F_ENC, fill=R_ENC)
    h.put(f"AO{fk0 - 1}", "R: PACF", font=F_ENC, fill=R_ENC)
    rr = f"$C${fr}:$AL${fr}"
    rrv = f"$C${frr}:$AL${frr}"
    for k in range(1, 37):
        fila = fk0 + k - 1
        h.put(f"B{fila}", k, align=CENTRO)
        prev = f"$C{fila - 1}:$AL{fila - 1}"   # fila relativa: la fórmula se arrastra
        if k == 1:
            fd = f"=C{fr}"
            instr = "φ_11 = ρ₁."
        else:
            fd = (f"=(INDEX({rr},$B{fila})-SUMPRODUCT($C{fila - 1}:INDEX({prev},$B{fila}-1),"
                  f"INDEX({rrv},38-$B{fila}):$AL${frr}))/(1-SUMPRODUCT($C{fila - 1}:INDEX({prev},$B{fila}-1),"
                  f"$C${fr}:INDEX({rr},$B{fila}-1)))")
            instr = ("φ_kk = (ρ_k − SUMPRODUCT(fila k−1 de 1 a k−1, ρ al revés de 38−k a 36)) / "
                     "(1 − SUMPRODUCT(fila k−1 de 1 a k−1, ρ de 1 a k−1)). La fila de arriba va con $ en la "
                     "columna y sin $ en la fila ($C81:$AL81), para poder arrastrarla hasta k = 36."
                     ) if k == 2 else None
        h.clave(f"AN{fila}", fd, instr, fmt=F4)
        h.dato(f"AO{fila}", cj["pacf"][k - 1], fmt=F4)
        for j in range(1, 37):
            col = 2 + j
            if k == 1:
                f = f'=IF({L(col)}${fj}>$B{fila},"",$AN{fila})'
            else:
                f = (f'=IF({L(col)}${fj}>$B{fila},"",IF({L(col)}${fj}=$B{fila},$AN{fila},'
                     f'INDEX({prev},{L(col)}${fj})-$AN{fila}*INDEX({prev},$B{fila}-{L(col)}${fj})))')
            instr = None
            if (k, j) == (2, 1):
                instr = ("φ_kj = φ_{k−1,j} − φ_kk·φ_{k−1,k−j}; vacía si j > k y φ_kk si j = k. Una sola "
                         f"fórmula para todo el cuadro: escríbela en C{fk0 + 1} y arrástrala a "
                         f"C{fk0 + 1}:AL{fk0 + 35}. La fila {fk0} es IF(j > 1, \"\", AN{fk0}).")
            h.clave(f"{L(col)}{fila}", f, instr, fmt="0.000")
    h.put(f"AM{fk0 + 36}", "¿= R?", font=F_NEGRITA)
    check_lista(h, f"AN{fk0 + 36}", 40, fk0, fk0 + 35, 41, 0.000051,
                "M4 (opcional): PACF de ∇∇₁₂ log y por Durbin–Levinson = pacf() de R")
    # columna local de w
    h.seccion(156, "Columnas de cálculo", c2=4)
    h.encabezados(158, 1, ["Fecha", "∇∇₁₂ log y"])
    for i in range(131):
        fila = fw0 + i
        h.put(f"A{fila}", f"={m3}A{103 + i}", fmt=FMES)
        h.put(f"B{fila}", f"={m3}F{103 + i}", fmt="0.00000")
    return h


# ------------------------------------------------------------------- M5
def hoja_m5(lb):
    J = lb.J
    A = J["airpassengers"]
    air = A["airline"]
    th, Th = [c_["valor"] for c_ in air["coeficientes"]]
    P = A["pronostico"]
    h = Hoja(lb, "M5 Airline", "M5 · El modelo airline",
             "Los pesos ψ del airline suben a escalones, y con ellos la incertidumbre del pronóstico.",
             anchos={"A": 36, "B": 13, "C": 13, "D": 7, "E": 40, "G": 6, "H": 9, "I": 11, "J": 11, "K": 6,
                     "L": 11}, ancho_texto=12)
    guardia = f"AND($B$6={th},$B$7={Th})"
    h.seccion(4, "1 · (1 − B)(1 − B¹²) y_t = (1 + θB)(1 + ΘB¹²) ε_t")
    h.put("A6", "θ (MA regular)")
    h.entrada("B6", th)
    h.put("A7", "Θ (MA estacional)")
    h.entrada("B7", Th)
    h.put("A8", "σ̂² (R)")
    h.dato("B8", air["sigma2"], fmt=F6)
    h.parrafo(9, "ψ(B) = (1 + θB)(1 + ΘB¹²) / ((1 − B)(1 − B¹²)). Despejando, ψ_j = ψ_{j−1} + ψ_{j−12} − "
              "ψ_{j−13} + c_j, donde c_j es el coeficiente MA del rezago j (1, θ, Θ o θΘ). Y σ_h² = σ² Σ_{j<h} ψ_j²: "
              "la varianza del error de pronóstico a h meses.", c2=5)
    h.completa(10, "ψ_j en I21:I56 y σ_h en L21:L56. Cambia θ y Θ para ver el escalón; vuelve a los "
               "valores de R para las comprobaciones.", c2=5)
    h.encabezados(12, 1, ["Magnitud", "Tu cálculo", "Capítulo (R)", "✔", "Lectura"])
    filas = [
        (13, "ψ₁ = 1 + θ", "=I22", P["psi"][1], 0.0001, "Dentro del primer año, constante."),
        (14, "ψ₁₁", "=I32", P["psi"][11], 0.0001, "Sigue en 1 + θ."),
        (15, "ψ₁₂ (el escalón)", "=I33", P["psi"][12], 0.0001, "Salta al cruzar el rezago estacional."),
        (16, "ψ₁₃ … ψ₂₃", "=I34", P["psi"][13], 0.0001, "Se instala en un nivel más alto."),
        (17, "σ₁", "=L21", P["sigma_h"][0], 0.00002, "Escala logarítmica."),
        (18, "σ₁₂", "=L32", P["sigma_h"][11], 0.00002, ""),
        (19, "σ₂₄", "=L44", P["sigma_h"][23], 0.00002, ""),
    ]
    for fila, s, f, cap, tol, lect in filas:
        h.put(f"A{fila}", s)
        h.formula(f"B{fila}", f, fmt=F6)
        h.dato(f"C{fila}", cap, fmt=F6)
        h.check(f"D{fila}", f"ABS(B{fila}-C{fila})<={tol}", f"M5: {s}", guardia)
        h.put(f"E{fila}", lect)
        h.resultado(f"B{fila}", f"m5_{fila}", tol)
    h.put("A20", "σ₁₂ / σ₁ (frente a √12 = 3.46 de una caminata)")
    h.formula("B20", "=B18/B17", fmt="0.00")
    h.dato("C20", round(P["sigma_h"][11] / P["sigma_h"][0], 2), fmt="0.00")
    h.check("D20", "ABS(B20-C20)<=0.005", "M5: σ₁₂/σ₁ = 2.22", guardia)
    h.put("E20", "Los dos MA negativos amortiguan las dos raíces unitarias.")
    h.parrafo(22, "El capítulo da ψ₁₂ = 1.0412 y ψ₁₃ = 0.8632 con los coeficientes completos de R; con los "
              "cuatro decimales de θ̂ y Θ̂ salen 1.0413 y 0.8633. Por eso la tolerancia es 10⁻⁴. σ̂² viene "
              "redondeado a 0.001371, y σ_h difiere de R en menos de 2·10⁻⁵.", c2=5)
    # columnas ψ (a la derecha)
    h.encabezados(7, 7, ["c_j (MA)", "j", "ψ_j", "ψ_j²", "h", "σ_h"])
    for i in range(13):
        fila = 8 + i
        h.put(f"H{fila}", -13 + i, font=F_GUION, align=CENTRO)
        h.dato(f"I{fila}", 0)
    for j in range(36):
        fila = 21 + j
        h.put(f"H{fila}", j, align=CENTRO)
        h.formula(f"G{fila}", f"=IF(H{fila}=0,1,IF(H{fila}=1,$B$6,IF(H{fila}=12,$B$7,IF(H{fila}=13,$B$6*$B$7,0))))",
                  fmt=F4)
        h.clave(f"I{fila}", f"=I{fila - 1}+I{fila - 12}-I{fila - 13}+G{fila}",
                "ψ_j = ψ_{j−1} + ψ_{j−12} − ψ_{j−13} + c_j: la división de polinomios, rezago a rezago. "
                "Escríbela en I21 (j = 0) y arrástrala hasta j = 35." if j == 0 else None, fmt=F6)
        h.formula(f"J{fila}", f"=I{fila}^2", fmt=F6)
        h.put(f"K{fila}", j + 1, align=CENTRO)
        h.clave(f"L{fila}", f"=SQRT($B$8*SUM($J$21:J{fila}))",
                "σ_h = √(σ² · Σ_{j<h} ψ_j²): la raíz de σ² por la suma acumulada de ψ² hasta esta fila. "
                "Con $ en el primer ψ²; arrástrala hasta h = 36." if j == 0 else None, fmt=F6)
    h.put("G6", "Columnas de cálculo", font=F_GUION)
    etiquetas(h, 26, 21, 56, 8, 12)
    etiquetas(h, 27, 21, 56, 11, 12)
    grafico_barras(h, "N4", 26, 9, 21, 56, "Pesos ψ_j del airline: escalones en 12 y 24",
                   nombre="ψ_j", resaltar=(13, 25), eje_x="j (la barra 1 es j = 0)")
    grafico_lineas(h, "N21", 27, [(12, "σ_h", NARANJA, False)], 21, 56,
                   "σ_h: la incertidumbre crece a escalones", eje_x="h (meses)", salto=1, fmt_y="0.00")
    # la varianza del proceso (M2): γ₀ = σ²(1 + θ²)(1 + Θ²)
    h.seccion(25, "2 · El regalo del M2: la varianza del airline se factoriza", c2=5)
    h.put("A26", "γ₀/σ² = (1 + θ²)(1 + Θ²)")
    h.formula("B26", "=(1+B6^2)*(1+B7^2)", fmt=F4)
    h.dato("C26", round((1 + th ** 2) * (1 + Th ** 2), 4), fmt=F4)
    h.put("A27", "γ₀ = σ²(1 + θ²)(1 + Θ²)")
    h.formula("B27", "=B8*B26", fmt=F6)
    h.put("A28", "varianza muestral de ∇∇₁₂ log y (la lee del M3)")
    h.formula("B28", "='M3 Diferenciar'!E69", fmt=F6)
    h.parrafo(29, "Con q < m los pesos MA no chocan y la varianza es exactamente el producto: 0.002087 del "
              "modelo frente a 0.002102 de los datos. Con parte AR no hay factorización (M2).", c2=5)
    return h


# ------------------------------------------------------------------- M6
def hoja_m6(lb):
    J = lb.J
    A = J["airpassengers"]
    air = A["airline"]
    dg = air["diagnostico"]
    (c1, c2_) = air["coeficientes"]
    th, Th = c1["valor"], c2_["valor"]
    h = Hoja(lb, "M6 Diagnóstico", "M6 · Estimar, comparar y diagnosticar",
             "Residuales, Ljung–Box con 2m = 24 rezagos y el AICc de la rejilla, celda a celda.",
             anchos={"A": 40, "B": 13, "C": 13, "D": 13, "E": 7, "F": 13}, ancho_texto=12)
    m3 = "'M3 Diferenciar'!"
    fr0 = 100                         # fila de t = 1 en las columnas de cálculo
    fr1 = fr0 + 143
    datos = [(5, "θ̂ (ma1)", th, c1["ee"]), (6, "Θ̂ (sma1)", Th, c2_["ee"])]
    h.encabezados(4, 2, ["valor", "e.e.", "t = valor/e.e.", "", "R: t"])
    h.seccion(4, "1 · Lo que estimó R (datos)", c2=1)
    for fila, s, v, ee in datos:
        h.put(f"A{fila}", s)
        h.dato(f"B{fila}", v, fmt=F4)
        h.dato(f"C{fila}", ee, fmt=F4)
    h.clave("D5", "=B5/C5", "t = coeficiente / error estándar.", fmt="0.00")
    h.clave("D6", "=B6/C6", "t = coeficiente / error estándar.", fmt="0.00")
    t_sin = A["calendario"]["modelos"]["sin_regresores"]["coeficientes"]
    h.dato("F5", t_sin[0]["t"], fmt="0.000")
    h.dato("F6", t_sin[1]["t"], fmt="0.000")
    h.check("E5", "ABS(D5-F5)<=0.005", "M6: t de θ̂ = −4.48")
    h.check("E6", "ABS(D6-F6)<=0.005", "M6: t de Θ̂ = −7.62")
    h.completa(11, "los estadísticos t en D5 y D6.")
    for fila, s, v, fmt in ((7, "σ̂²", air["sigma2"], F6), (8, "log-verosimilitud", air["loglik"], F4),
                            (9, "nobs (131: 144 − 1 − 12)", air["nobs"], "0"),
                            (10, "fitdf = p + q + P + Q", dg["fitdf"], "0")):
        h.put(f"A{fila}", s)
        h.dato(f"B{fila}", v, fmt=fmt)

    h.seccion(12, "2 · Residuales: la recursión CSS frente a los de R")
    h.parrafo(13, "Con w_t = ∇∇₁₂ log y_t, el modelo dice w_t = e_t + θe_{t−1} + Θe_{t−12} + θΘe_{t−13}. "
              "Despejando, e_t = w_t − θe_{t−1} − Θe_{t−12} − θΘe_{t−13}, desde e = 0 antes de empezar: es la "
              "suma de cuadrados condicional (CSS). R usa la verosimilitud exacta (filtro de Kalman), así que "
              "su primer año de residuales es otro; la diferencia se olvida al ritmo de |Θ| por año.")
    h.completa(14, f"los residuales CSS en D{fr0 + 13}:D{fr1} (columnas de cálculo, fila {fr0 - 2}). La "
               "columna C lee ∇∇₁₂ log y del M3: si allí falta, aquí sale en error.")
    h.put("A16", "|CSS − R| máximo en los últimos 24 meses")
    h.formula("B16", f"=MAX(F{fr1 - 23}:F{fr1})", fmt="0.000000")
    h.put("C16", "< 0.0005", font=F_GUION)
    h.check("E16", f"AND(COUNT(D{fr0 + 13}:D{fr1})=131,B16<0.0005)",
            "M6: al final de la muestra los residuales CSS y los de R casi coinciden")
    h.put("A17", "|CSS − R| máximo en el primer año (t = 14 a 25)")
    h.formula("B17", f"=MAX(F{fr0 + 13}:F{fr0 + 24})", fmt="0.000000")
    e_css = css_residuales(w_exacta(lb.D), th, Th)
    h.put("A18", "Suma de los residuales CSS (referencia)")
    h.formula("B18", f"=SUM(D{fr0 + 13}:D{fr1})", fmt="0.000000")
    h.dato("C18", round(sum(e_css), 6), fmt="0.000000")
    h.check("E18", "ABS(B18-C18)<=0.0000051", "M6: los residuales CSS coinciden con los de referencia")

    h.seccion(20, "3 · Ljung–Box con 2m rezagos")
    h.parrafo(21, "Q = n(n + 2) Σ_{k=1}^{h} ρ̂_k² / (n − k), que se compara con una χ² de h − fitdf grados de "
              "libertad. R lo calcula sobre sus 144 residuales, incluidos los 13 primeros, casi nulos por el "
              "arranque difuso: n = 144. Las ACF están en las columnas de cálculo (H, I y J).")
    h.completa(22, "Q y su valor p, con h = 24 y con h = 36 sobre los residuales de R, y con h = 24 sobre los CSS.")
    h.encabezados(24, 1, ["", "Tu cálculo", "R (capítulo)", "", "✔", "Cómo se calcula"])
    q_css = ljung_box(e_css, 24)
    p_css = chi2_cola_par(q_css, 22)
    lb.cifras["q_css"], lb.cifras["p_css"] = q_css, p_css
    racf = f"I{fr0}:I{fr0 + 35}"
    filas = [
        (25, "Q(24), residuales de R (n = 144)", f"=144*(144+2)*SUMPRODUCT(I{fr0}:I{fr0 + 23}^2/(144-H{fr0}:H{fr0 + 23}))",
         dg["lb24_Q"], 0.001, "n(n+2)·SUMPRODUCT(ρ̂² / (n − k)) con k = 1…24."),
        (26, "valor p, χ² con 24 − 2 = 22 g.l.", "=_xlfn.CHISQ.DIST.RT(B25,24-$B$10)", dg["lb24_p"], 0.0001,
         "CHISQ.DIST.RT(Q, 24 − fitdf), en español DISTR.CHICUAD.CD."),
        (27, "Q(36), residuales de R", f"=144*(144+2)*SUMPRODUCT(I{fr0}:I{fr0 + 35}^2/(144-H{fr0}:H{fr0 + 35}))",
         dg["lb36_Q"], 0.001, "Lo mismo con k = 1…36."),
        (28, "valor p, 36 − 2 = 34 g.l.", "=_xlfn.CHISQ.DIST.RT(B27,36-$B$10)", dg["lb36_p"], 0.0001, ""),
        (29, "Q(24), residuales CSS (n = 131)", f"=131*(131+2)*SUMPRODUCT(J{fr0}:J{fr0 + 23}^2/(131-H{fr0}:H{fr0 + 23}))",
         round(q_css, 4), 0.001, "Con la ACF de los residuales CSS (columna J) y n = 131."),
        (30, "valor p", "=_xlfn.CHISQ.DIST.RT(B29,24-$B$10)", round(p_css, 4), 0.0001, ""),
    ]
    for fila, s, f, cap, tol, instr in filas:
        h.put(f"A{fila}", s)
        h.clave(f"B{fila}", f, instr or None, fmt=F4)
        h.dato(f"C{fila}", cap, fmt=F4)
        h.check(f"E{fila}", f"ABS(B{fila}-C{fila})<={tol}", f"M6: {s}")
        h.put(f"F{fila}", instr)
        h.resultado(f"B{fila}", f"m6_{fila}", tol)
    h.put("D29", "(referencia)", font=F_GUION)
    h.put("D30", "(referencia)", font=F_GUION)
    h.parrafo(31, f"Con los residuales CSS, Q = {q_css:.2f} y p = {p_css:.3f}; con los de R, Q = {dg['lb24_Q']} "
              f"y p = {dg['lb24_p']}. El primer año de la recursión arrastra el arranque en cero y rebaja Q, "
              "pero la conclusión es la misma: no se rechaza la blancura de los residuales.")
    h.put("A33", "ρ̂₁₂ y ρ̂₂₄ de los residuales (banda ±0.163)")
    h.formula("B33", f"=I{fr0 + 11}", fmt=F4)
    h.formula("C33", f"=I{fr0 + 23}", fmt=F4)
    h.check("E33", f"SUMPRODUCT(--(ABS(I{fr0}:I{fr0 + 35}-K{fr0}:K{fr0 + 35})<=0.0001))=36",
            "M6: ACF de los residuales de R = la del capítulo en los 36 rezagos (± 10⁻⁴: J guarda "
            "los residuales con 5 decimales)")
    h.put("F33", f"capítulo: {dg['acf12']} y {dg['acf24']}")

    # 4 · la rejilla
    rej = A["rejilla"]
    fg0 = 40
    fg1 = fg0 + len(rej) - 1
    h.seccion(35, "4 · La rejilla SARIMA(p,1,q)(P,1,Q)₁₂ y el AICc")
    h.parrafo(36, "Los 36 modelos tienen d = 1 y D = 1, así que todos se evalúan sobre las mismas 131 "
              "observaciones: solo así el AICc compara. Con k parámetros estimados más σ² (k + 1 en total) y "
              "log-verosimilitud ℓ: AIC = −2ℓ + 2(k + 1); AICc = AIC + 2(k + 1)(k + 2)/(n − k − 2); "
              "BIC = −2ℓ + (k + 1)·ln n.")
    h.completa(37, "AICc en H40:H75, BIC en I40:I75 y el puesto por AICc y por BIC en J y K (RANK, en español "
               "JERARQUIA, de menor a mayor).")
    h.encabezados(39, 1, ["Modelo", "k", "nobs", "log-verosimilitud", "LB(24) p", "ρ̂₁₂ resid.", "", "AICc",
                          "BIC", "Puesto AICc", "Puesto BIC", "R: AICc", "R: BIC"], ajuste=True)
    for col in range(8, 14):
        h.ws.column_dimensions[L(col)].width = 12
    for i, (nombre, v) in enumerate(rej.items()):
        fila = fg0 + i
        h.put(f"A{fila}", nombre)
        h.dato(f"B{fila}", v["n_par"], fmt="0")
        h.dato(f"C{fila}", v["nobs"], fmt="0")
        h.dato(f"D{fila}", v["loglik"], fmt=F4)
        h.dato(f"E{fila}", v["lb_p"], fmt=F4)
        h.dato(f"F{fila}", v["acf12"], fmt=F4)
        primera = i == 0
        h.clave(f"H{fila}", f"=-2*D{fila}+2*(B{fila}+1)+2*(B{fila}+1)*(B{fila}+2)/(C{fila}-B{fila}-2)",
                "AICc = −2ℓ + 2(k+1) + 2(k+1)(k+2)/(n − k − 2), con k + 1 porque σ² también se estima. "
                "Arrástrala por los 36 modelos." if primera else None, fmt="0.0000")
        h.clave(f"I{fila}", f"=-2*D{fila}+(B{fila}+1)*LN(C{fila})",
                "BIC = −2ℓ + (k + 1)·LN(n)." if primera else None, fmt="0.0000")
        h.clave(f"J{fila}", f"=RANK(H{fila},$H${fg0}:$H${fg1},1)",
                "RANK(AICc, columna de AICc, 1): 1 al menor." if primera else None, fmt="0")
        h.clave(f"K{fila}", f"=RANK(I{fila},$I${fg0}:$I${fg1},1)",
                "Lo mismo con el BIC." if primera else None, fmt="0")
        h.dato(f"L{fila}", v["aicc"], fmt="0.0000")
        h.dato(f"M{fila}", v["bic"], fmt="0.0000")
    fila_air = fg0 + list(rej).index("(0,1,1)(0,1,1)[12]")
    fc = fg1 + 2
    h.put(f"A{fc}", "AICc y BIC de los 36 = R (± 0.001)")
    h.check(f"E{fc}", f"AND(SUMPRODUCT(--(ABS(H{fg0}:H{fg1}-L{fg0}:L{fg1})<=0.001))={len(rej)},"
                      f"SUMPRODUCT(--(ABS(I{fg0}:I{fg1}-M{fg0}:M{fg1})<=0.001))={len(rej)})",
            "M6: AICc y BIC de la rejilla, desde el log-verosimilitud")
    h.put(f"A{fc + 1}", "El airline, primero por AICc y por BIC")
    h.check(f"E{fc + 1}", f"AND(J{fila_air}=1,K{fila_air}=1)", "M6: el airline gana por AICc y por BIC")
    h.put(f"A{fc + 3}", "Los cuatro mejores por AICc", font=F_NEGRITA)
    h.encabezados(fc + 4, 1, ["Puesto", "Modelo", "AICc", "Capítulo"])
    for i in range(4):
        fila = fc + 5 + i
        h.put(f"A{fila}", i + 1, align=CENTRO)
        h.formula(f"B{fila}", f"=INDEX($A${fg0}:$A${fg1},MATCH(SMALL($H${fg0}:$H${fg1},A{fila}),$H${fg0}:$H${fg1},0))")
        h.formula(f"C{fila}", f"=SMALL($H${fg0}:$H${fg1},A{fila})", fmt="0.00")
        h.dato(f"D{fila}", A["mejores_aicc"][i])
    h.check(f"E{fc + 5}", "AND(" + ",".join(f'B{fc + 5 + i}=D{fc + 5 + i}' for i in range(4)) + ")",
            "M6: los cuatro mejores son los del capítulo")
    h.parrafo(fc + 10, "Los cuatro primeros están dentro de 1.7 puntos de AICc: la evidencia no los separa "
              "mucho. Decide el diagnóstico: los tres rivales gastan uno o dos parámetros más sin mejorarlo.")

    # columnas de cálculo
    h.seccion(fr0 - 4, "Columnas de cálculo")
    h.encabezados(fr0 - 2, 1, ["Fecha", "t", "w = ∇∇₁₂ log y", "e CSS", "e de R", "|CSS − R|"])
    h.encabezados(fr0 - 2, 8, ["k", "ρ̂ resid. R", "ρ̂ resid. CSS", "R: ρ̂"])
    for i in range(144):
        fila = fr0 + i
        t = i + 1
        h.put(f"A{fila}", f"=Datos!A{5 + i}", fmt=FMES)
        h.put(f"B{fila}", t)
        if t <= 13:
            h.guion(f"C{fila}")
            h.dato(f"D{fila}", 0)
        else:
            h.put(f"C{fila}", f"={m3}F{90 + i}", fmt="0.00000")
            h.clave(f"D{fila}", f"=C{fila}-$B$5*D{fila - 1}-$B$6*D{fila - 12}-$B$5*$B$6*D{fila - 13}",
                    "e_t = w_t − θ·e_{t−1} − Θ·e_{t−12} − θΘ·e_{t−13}, con $ en θ̂ (B5) y Θ̂ (B6). Las 13 filas "
                    "de arriba son el arranque en cero. Arrástrala hasta t = 144." if t == 14 else None,
                    fmt="0.00000")
            h.formula(f"F{fila}", f"=ABS(D{fila}-E{fila})", fmt="0.000000")
        h.dato(f"E{fila}", air["residuales"][i], fmt="0.00000")
    for k in range(1, 37):
        fila = fr0 + k - 1
        h.put(f"H{fila}", k, align=CENTRO)
        h.formula(f"I{fila}", f_acf(5, fr0, fr1, f"H{fila}"), fmt=F4)
        h.formula(f"J{fila}", f_acf(4, fr0 + 13, fr1, f"H{fila}"), fmt=F4)
        h.dato(f"K{fila}", dg["acf"][k - 1], fmt=F4)
        h.formula(f"L{fila}", "=1.96/SQRT(144)", fmt=F4)
        h.formula(f"M{fila}", f"=-L{fila}", fmt=F4)
    etiquetas(h, 26, fr0, fr0 + 35, 8, 6)
    grafico_barras(h, "O4", 26, 9, fr0, fr0 + 35, "ACF de los residuales del airline (R)",
                   banda=(12, 13), resaltar=(12, 24, 36))
    grafico_lineas(h, "O22", 2, [(6, "|CSS − R|", NARANJA, False)], fr0 + 13, fr1,
                   "La recursión CSS olvida el arranque", eje_x="t", salto=12, fmt_y="0.000")
    return h


# ------------------------------------------------------------------- M7
def hoja_m7(lb):
    J = lb.J
    A = J["airpassengers"]
    air = A["airline"]
    P = A["pronostico"]
    th, Th = [c_["valor"] for c_ in air["coeficientes"]]
    h = Hoja(lb, "M7 Pronóstico", "M7 · El pronóstico a 24 meses",
             "La recursión del airline en logaritmos, las bandas con σ_h y la vuelta a pasajeros con exp.",
             anchos={"A": 42, "B": 13, "C": 13, "D": 13, "E": 7, "F": 58}, ancho_texto=6)
    m5, m6 = "'M5 Airline'!", "'M6 Diagnóstico'!"
    ft0 = 60                          # fila de t = 1
    ft_fin = ft0 + 167                # t = 168
    fh1 = ft0 + 144                   # t = 145, h = 1
    h.seccion(4, "1 · Datos y elecciones")
    h.put("A5", "Residuales: 1 = recursión CSS (M6), 2 = los de R")
    h.entrada("B5", 1)
    dv = DataValidation(type="whole", operator="between", formula1="1", formula2="2", allow_blank=False)
    h.ws.add_data_validation(dv)
    dv.add("B5")
    h.put("A6", "θ̂ (M6)")
    h.formula("B6", f"={m6}B5", fmt=F4)
    h.put("A7", "Θ̂ (M6)")
    h.formula("B7", f"={m6}B6", fmt=F4)
    h.put("A8", "z del 80 % = NORM.S.INV(0.9)")
    h.clave("B8", "=_xlfn.NORM.S.INV(0.9)", "NORM.S.INV(0.9), en español INV.NORM.ESTAND: el cuantil 0.9 de la normal.",
            fmt=F4)
    h.put("A9", "z del 95 % = NORM.S.INV(0.975)")
    h.clave("B9", "=_xlfn.NORM.S.INV(0.975)", "NORM.S.INV(0.975): 1.9600.", fmt=F4)
    h.formula("C8", f'=IF(AND({m5}B6={th},{m5}B7={Th}),"","⚠ El M5 tiene otros θ y Θ: las bandas no son las del modelo estimado.")')
    h.ws["C8"].font = F_NOTA
    h.parrafo(10, "ŷ_{T+h} = y_{T+h−1} + y_{T+h−12} − y_{T+h−13} + θe_{T+h−1} + Θe_{T+h−12} + θΘe_{T+h−13}, "
              "con e = 0 en el futuro: el polinomio (1 − B)(1 − B¹²) despejado. Las bandas, ŷ ± z·σ_h con los σ_h "
              "del M5. Y exp devuelve la MEDIANA en pasajeros; la media es exp(ŷ + σ_h²/2).")
    h.completa(11, "z en B8 y B9, y en las columnas de cálculo (fila 58): ŷ en C204:C227, las bandas en "
               "logaritmos en G:J, mediana y media en pasajeros en K y L, y los límites en pasajeros en M:P. Lee los "
               "σ_h del M5 y los residuales del M6: complétalos antes.")
    h.seccion(13, "2 · Resultado y comparación con R")
    h.encabezados(14, 1, ["", "Este libro", "R (capítulo)", "", "✔", "Lectura"])
    t24 = ft_fin
    filas = [
        (15, "Pronóstico a 1 mes, log", f"=C{fh1}", P["log"]["media"][0], 0.0003),
        (16, "Pronóstico a 24 meses, log", f"=C{t24}", P["log"]["media"][23], 0.0003),
        (17, "Mediana a 24 meses (pasajeros)", f"=K{t24}", P["original"]["media"][23], 0.2),
        (18, "Límite inferior 95 % a 24 meses", f"=O{t24}", P["original"]["lo95"][23], 0.2),
        (19, "Límite superior 95 % a 24 meses", f"=P{t24}", P["original"]["hi95"][23], 0.2),
    ]
    for fila, s, f, cap, tol in filas:
        h.put(f"A{fila}", s)
        h.formula(f"B{fila}", f, fmt="0.00000" if "log" in s else "0.00")
        h.dato(f"C{fila}", cap, fmt="0.00000" if "log" in s else "0.00")
        h.check(f"E{fila}", f"ABS(B{fila}-C{fila})<={tol}", f"M7: {s}")
        h.resultado(f"B{fila}", f"m7_{fila}", tol)
    h.put("F15", "CSS: hasta 3·10⁻⁴ de R en logaritmos; con los residuales de R, 10⁻⁵.")
    h.put("F17", "525.34 con CSS frente a 525.46 de R: un 0.02 %.")
    h.put("A20", "Distancia al límite inferior (abajo)")
    h.formula("B20", "=B17-B18", fmt="0.00")
    h.dato("C20", round(P["original"]["media"][23] - P["original"]["lo95"][23], 2), fmt="0.00")
    h.put("A21", "Distancia al límite superior (arriba)")
    h.formula("B21", "=B19-B17", fmt="0.00")
    h.dato("C21", round(P["original"]["hi95"][23] - P["original"]["media"][23], 2), fmt="0.00")
    h.check("E21", "AND(B21>B20,ABS(B20-C20)<=0.1,ABS(B21-C21)<=0.1)",
            "M7: el intervalo en pasajeros no es simétrico (126 abajo, 165 arriba)")
    h.put("F21", "Es del logaritmo, no un error: exp respeta los cuantiles, no la simetría.")
    # media frente a mediana: referencia con cada fuente de residuales
    ly = [math.log(v) for v in lb.D["airpassengers"]["valores"]]
    e_css = [0.0] * 13 + css_residuales(w_exacta(lb.D), th, Th)
    s2 = air["sigma2"]
    psi = psi_airline(th, Th, 24)
    sh24 = math.sqrt(s2 * sum(v * v for v in psi))
    medias = {}
    for fuente, e in ((1, e_css), (2, air["residuales"])):
        fc = pronostico_airline(ly, e, th, Th)
        medias[fuente] = (math.exp(fc[23]), math.exp(fc[23] + sh24 ** 2 / 2))
    lb.cifras["m7_mediana_css"] = medias[1][0]
    h.put("A22", "Media a 24 meses: exp(ŷ + σ²/2)")
    h.formula("B22", f"=L{t24}", fmt="0.00")
    h.dato("C22", f"=IF($B$5=1,{round(medias[1][1], 4)},{round(medias[2][1], 4)})", fmt="0.00")
    h.check("E22", "ABS(B22-C22)<=0.001", "M7: la media en pasajeros, exp(ŷ + σ²/2)")
    h.put("D22", "(referencia)", font=F_GUION)
    h.put("F22", "Un 1 % por encima de la mediana. El capítulo no da esta media con R: la columna C trae la "
                 "de referencia, con la misma cuenta.")
    h.put("A23", "Los 24 pronósticos en log = R (± 3·10⁻⁴)")
    h.check("E23", f"SUMPRODUCT(--(ABS(C{fh1}:C{t24}-R{fh1}:R{t24})<=0.0003))=24",
            "M7: los 24 pronósticos en logaritmos, frente a R")
    h.put("A24", "Las bandas del 95 % en log = R (± 4·10⁻⁴)")
    h.check("E24", f"AND(SUMPRODUCT(--(ABS(I{fh1}:I{t24}-S{fh1}:S{t24})<=0.0004))=24,"
                   f"SUMPRODUCT(--(ABS(J{fh1}:J{t24}-T{fh1}:T{t24})<=0.0004))=24)",
            "M7: las bandas del 95 % en logaritmos, frente a R")
    h.put("A25", "Las bandas del 80 % en log = R (± 4·10⁻⁴)")
    h.check("E25", f"AND(SUMPRODUCT(--(ABS(G{fh1}:G{t24}-U{fh1}:U{t24})<=0.0004))=24,"
                   f"SUMPRODUCT(--(ABS(H{fh1}:H{t24}-V{fh1}:V{t24})<=0.0004))=24)",
            "M7: las bandas del 80 % en logaritmos, frente a R")
    # columnas de cálculo
    h.seccion(ft0 - 4, "Columnas de cálculo")
    h.encabezados(ft0 - 2, 1, ["Fecha", "t", "log y / ŷ", "e", "h", "σ_h", "lo 80", "hi 80", "lo 95", "hi 95",
                               "mediana", "media", "lo 80", "hi 80", "lo 95", "hi 95"], ajuste=True)
    h.put(f"G{ft0 - 3}", "en logaritmos", font=F_GUION)
    h.put(f"K{ft0 - 3}", "en pasajeros", font=F_GUION)
    h.encabezados(ft0 - 2, 18, ["R: log", "R: lo 95", "R: hi 95", "R: lo 80", "R: hi 80"], ajuste=True)
    h.encabezados(ft0 - 2, 24, ["gráfico: observado", "mediana", "lo 95", "hi 95"], ajuste=True)
    for i in range(168):
        fila = ft0 + i
        t = i + 1
        h.put(f"A{fila}", f"=DATE(1949,B{fila},1)", fmt=FMES)
        h.put(f"B{fila}", t)
        if t <= 144:
            h.put(f"C{fila}", f"=Datos!C{5 + i}", fmt="0.00000")
            if t <= 13:
                h.put(f"D{fila}", f"=IF($B$5=1,0,{m6}E{100 + i})", fmt="0.00000")
            else:
                h.put(f"D{fila}", f"=IF($B$5=1,{m6}D{100 + i},{m6}E{100 + i})", fmt="0.00000")
        else:
            hh = t - 144
            h.clave(f"C{fila}", f"=C{fila - 1}+C{fila - 12}-C{fila - 13}+$B$6*D{fila - 1}+$B$7*D{fila - 12}"
                                f"+$B$6*$B$7*D{fila - 13}",
                    "ŷ_t = y_{t−1} + y_{t−12} − y_{t−13} + θ·e_{t−1} + Θ·e_{t−12} + θΘ·e_{t−13}, con $ en θ̂ (B6) y "
                    "Θ̂ (B7). Arrástrala hasta t = 168: ya usa los pronósticos como si fueran datos." if hh == 1 else None,
                    fmt="0.00000")
            h.put(f"D{fila}", 0, font=F_GUION)
            h.put(f"E{fila}", hh, align=CENTRO)
            h.formula(f"F{fila}", f"=INDEX({m5}$L$21:$L$56,E{fila})", fmt=F6)
            instr80 = ("ŷ − z₈₀·σ_h, con $ en z₈₀ (B8). Las columnas H, I y J son ŷ + z₈₀·σ_h, ŷ − z₉₅·σ_h "
                       "y ŷ + z₉₅·σ_h, con z₉₅ en B9." if hh == 1 else None)
            instr95 = None
            h.clave(f"G{fila}", f"=C{fila}-$B$8*F{fila}", instr80, fmt="0.00000")
            h.clave(f"H{fila}", f"=C{fila}+$B$8*F{fila}", None, fmt="0.00000")
            h.clave(f"I{fila}", f"=C{fila}-$B$9*F{fila}", instr95, fmt="0.00000")
            h.clave(f"J{fila}", f"=C{fila}+$B$9*F{fila}", None, fmt="0.00000")
            h.clave(f"K{fila}", f"=EXP(C{fila})", "EXP(ŷ): la mediana en pasajeros." if hh == 1 else None, fmt="0.00")
            h.clave(f"L{fila}", f"=EXP(C{fila}+F{fila}^2/2)",
                    "EXP(ŷ + σ_h²/2): la media. Si log y ~ N(μ, σ²), E[y] = e^{μ + σ²/2}." if hh == 1 else None,
                    fmt="0.00")
            for col_o, col_l in (("M", "G"), ("N", "H"), ("O", "I"), ("P", "J")):
                h.clave(f"{col_o}{fila}", f"=EXP({col_l}{fila})",
                        "EXP de cada límite de G:J. Los límites sí se transforman sin más: exp es monótona y "
                        "respeta los cuantiles." if (hh, col_o) == (1, "M") else None, fmt="0.00")
            for col_r, clave_r in (("R", "media"), ("S", "lo95"), ("T", "hi95"), ("U", "lo80"), ("V", "hi80")):
                h.dato(f"{col_r}{fila}", P["log"][clave_r][hh - 1], fmt="0.00000")
        # columnas del gráfico (de 1957 en adelante)
        h.formula(f"X{fila}", f"=IF(B{fila}<=144,Datos!B{5 + i},NA())" if t <= 144 else "=NA()", fmt="0.00")
        if t < 144:
            for col in ("Y", "Z", "AA"):
                h.formula(f"{col}{fila}", "=NA()")
        elif t == 144:
            for col in ("Y", "Z", "AA"):
                h.formula(f"{col}{fila}", f"=Datos!B{5 + i}", fmt="0.00")
        else:
            h.formula(f"Y{fila}", f"=K{fila}", fmt="0.00")
            h.formula(f"Z{fila}", f"=O{fila}", fmt="0.00")
            h.formula(f"AA{fila}", f"=P{fila}", fmt="0.00")
    f_ini = ft0 + 96                  # 1957-01
    grafico_lineas(h, "H4", 1, [(24, "observado", VERDE, False), (25, "mediana", NARANJA, False),
                               (26, "límite inferior 95 %", "7F7F7F", True),
                               (27, "límite superior 95 %", "7F7F7F", True)],
                   f_ini, ft_fin, "AirPassengers: pronóstico a 24 meses con banda del 95 %",
                   ancho=22, alto=10, eje_y="pasajeros (miles)", salto=12, fmt_x=FMES, fmt_y="0")
    return h


# ------------------------------------------------------------------- M8
def hoja_m8(lb):
    J = lb.J
    TR = J["trm_contraejemplo"]
    UA = J["usaccdeaths"]
    A = J["airpassengers"]
    h = Hoja(lb, "M8 Contraejemplo", "M8 · Segundo caso y contraejemplo",
             "Sobre la serie sin tendencia, una serie estacional tiene picos en 12, 24, 36 y la TRM no tiene ninguno.",
             anchos={"A": 38, "B": 8, "C": 12, "D": 12, "E": 12, "F": 12, "G": 7}, ancho_texto=12)
    m1 = "'M1 Firma'!"
    fu0, fu1 = 100, 171                 # USAccDeaths, t = 1..72
    h.seccion(4, "1 · ∇TRM frente a ∇USAccDeaths: la ACF de las dos series sin tendencia")
    h.parrafo(5, "Las dos llevan una diferencia regular. En niveles las dos parecían estacionales, porque "
              "una tendencia infla todos los rezagos; sin ella, USAccDeaths conserva sus picos en 12 y 24 y la "
              "TRM no tiene ninguno. La ACF de ∇TRM viene del M1.")
    h.completa(6, "∇USAccDeaths en D101:D171 (columnas de cálculo), su ACF en D10:D45, la marca «fuera» de la "
               "tabla de rezagos estacionales y, más abajo, el t de C61, la diferencia de AICc de C62 y los "
               "cocientes de F67:F68. La ACF de ∇TRM viene del M1: si allí falta, la columna C sale en error.")
    h.encabezados(9, 2, ["k", "ρ̂ ∇TRM", "ρ̂ ∇USAccD.", "referencia", "R: ∇TRM"], ajuste=True)
    uad = UA["valores"]
    d_uad = [uad[i] - uad[i - 1] for i in range(1, len(uad))]
    r_uad = acf(d_uad, 36)
    for k in range(1, 37):
        fila = 9 + k
        h.put(f"B{fila}", k, align=CENTRO)
        h.formula(f"C{fila}", f"={m1}L{46 + k}", fmt=F4)
        h.clave(f"D{fila}", f_acf(4, fu0 + 1, fu1, f"B{fila}"),
                "La ACF del M1, con el rango de ∇USAccDeaths: $D$101:$D$171 (n = 71)." if k == 1 else None, fmt=F4)
        h.dato(f"E{fila}", round(r_uad[k - 1], 6), fmt=F4)
        h.dato(f"F{fila}", TR["correlogramas"]["acf"][k - 1], fmt=F4)
        h.formula(f"H{fila}", "=$C$48", fmt=F4)
        h.formula(f"I{fila}", "=-$C$48", fmt=F4)
        h.formula(f"J{fila}", "=$D$48", fmt=F4)
        h.formula(f"K{fila}", "=-$D$48", fmt=F4)
    h.put("B46", "¿=?", font=F_NEGRITA)
    check_lista(h, "D46", 4, 10, 45, 5, 0.000001, "M8: ACF de ∇USAccDeaths = la de referencia")
    check_lista(h, "C46", 3, 10, 45, 6, 0.000051, "M8: ACF de ∇TRM = R (viene del M1)")
    h.put("A47", "n")
    h.formula("C47", f"=COUNT({m1}F47:F184)", fmt="0")
    h.formula("D47", f"=COUNT(D{fu0}:D{fu1})", fmt="0")
    h.put("A48", "banda ±1.96/√n")
    h.formula("C48", "=1.96/SQRT(C47)", fmt=F4)
    h.formula("D48", "=1.96/SQRT(D47)", fmt=F4)
    h.encabezados(50, 1, ["Rezago estacional", "k", "ρ̂ ∇TRM", "¿fuera?", "ρ̂ ∇USAccD.", "¿fuera?"])
    for i, k in enumerate((12, 24, 36)):
        fila = 51 + i
        h.put(f"B{fila}", k, align=CENTRO)
        h.formula(f"C{fila}", f"=C{9 + k}", fmt="0.000")
        h.clave(f"D{fila}", f'=IF(ABS(C{fila})>$C$48,"fuera","")',
                'IF(ABS(ρ̂) > banda, "fuera", ""), con la banda de cada serie.' if i == 0 else None)
        h.formula(f"E{fila}", f"=D{9 + k}", fmt="0.000")
        h.clave(f"F{fila}", f'=IF(ABS(E{fila})>$D$48,"fuera","")', None)
    h.put("A54", "Rezagos estacionales fuera de la banda")
    h.formula("D54", '=COUNTIF(D51:D53,"fuera")', fmt="0")
    h.formula("F54", '=COUNTIF(F51:F53,"fuera")', fmt="0")
    n_fuera_uad = sum(1 for k in (12, 24, 36) if abs(r_uad[k - 1]) > 1.96 / math.sqrt(len(d_uad)))
    h.dato("C55", TR["estacionales_fuera_de_banda"], fmt="0")
    h.dato("E55", n_fuera_uad, fmt="0")
    h.put("A55", "R / referencia")
    h.check("G54", "AND(D54=C55,F54=E55)", "M8: la TRM no tiene ningún rezago estacional fuera; USAccDeaths sí")
    etiquetas(h, 26, 10, 45, 2, 6)
    grafico_barras(h, "M4", 26, 3, 10, 45, "ACF de ∇TRM: ningún pico estacional", banda=(8, 9))
    grafico_barras(h, "M21", 26, 4, 10, 45, "ACF de ∇USAccDeaths: los picos siguen ahí", banda=(10, 11))

    h.seccion(57, "2 · Cuatro evidencias de que la TRM no tiene estacionalidad")
    h.encabezados(58, 1, ["Evidencia", "", "Este libro", "R", "", "", "✔"])
    h.put("A59", "1. nsdiffs(), con las dos pruebas (seas, ocsb)")
    h.dato("D59", f"{TR['nsdiffs_seas']} y {TR['nsdiffs_ocsb']}")
    h.put("A60", "2. ρ̂₁₂, ρ̂₂₄ y ρ̂₃₆ de ∇TRM frente a la banda")
    h.formula("C60", "=D54", fmt="0")
    h.dato("D60", TR["estacionales_fuera_de_banda"], fmt="0")
    h.put("A61", f"3. Forzar un SAR(1): Φ̂ = {TR['forzado']['Phi']}, e.e. {TR['forzado']['ee']}; t =")
    h.dato("E61", TR["forzado"]["Phi"], fmt=F4)
    h.dato("F61", TR["forzado"]["ee"], fmt=F4)
    h.clave("C61", "=E61/F61", "t = Φ̂ / e.e.: prácticamente cero.", fmt="0.000")
    h.dato("D61", TR["forzado"]["t"], fmt="0.000")
    h.check("G61", "ABS(C61-D61)<=0.001", "M8: el t del SAR(1) forzado sobre la TRM")
    h.put("A62", "4. AICc del forzado menos el del simple")
    h.dato("E62", TR["forzado"]["aicc"], fmt="0.000")
    h.dato("F62", TR["simple"]["aicc"], fmt="0.000")
    h.clave("C62", "=E62-F62", "AICc(forzado) − AICc(simple): positivo, el forzado es peor. Aquí sí se comparan: "
            "los dos tienen d = 1 y D = 0.", fmt="0.000")
    h.dato("D62", round(TR["forzado"]["aicc"] - TR["simple"]["aicc"], 3), fmt="0.000")
    h.check("G62", "ABS(C62-D62)<=0.0005", "M8: el AICc del modelo forzado es peor")
    h.put("A63", "auto.arima devuelve")
    h.dato("D63", TR["auto"])

    h.seccion(65, "3 · USAccDeaths: el mismo airline, casi los mismos coeficientes")
    h.encabezados(66, 1, ["", "AirPassengers", "e.e.", "USAccDeaths", "e.e.", "e.e. UAD / e.e. AP", "✔"],
                  ajuste=True)
    ca = A["airline"]["coeficientes"]
    cu = UA["coeficientes"]
    for i, s in enumerate(("θ̂ (ma1)", "Θ̂ (sma1)")):
        fila = 67 + i
        h.put(f"A{fila}", s)
        h.dato(f"B{fila}", ca[i]["valor"], fmt=F4)
        h.dato(f"C{fila}", ca[i]["ee"], fmt=F4)
        h.dato(f"D{fila}", cu[i]["valor"], fmt=F4)
        h.dato(f"E{fila}", cu[i]["ee"], fmt=F4)
        h.clave(f"F{fila}", f"=E{fila}/C{fila}",
                "Cociente de los errores estándar: con la mitad de observaciones, mayores." if i == 0 else None,
                fmt="0.00")
    h.check("G67", "AND(F67>1.3,F67<1.45,F68>2.35,F68<2.5)",
            "M8: los e.e. de USAccDeaths son entre 1.4 y 2.4 veces los de AirPassengers")
    h.parrafo(70, "Primero D, después d: ndiffs() sobre USAccDeaths crudo devuelve 0 y sobre ∇₁₂ "
              "USAccDeaths devuelve 1. La varianza estacional es tan grande que tapa la tendencia.")
    # columnas de cálculo
    h.seccion(fu0 - 4, "Columnas de cálculo", c2=5)
    h.encabezados(fu0 - 2, 1, ["Fecha", "t", "USAccDeaths", "∇USAccDeaths"])
    for i in range(72):
        fila = fu0 + i
        h.put(f"A{fila}", f"=Datos!E{5 + i}", fmt=FMES)
        h.put(f"B{fila}", i + 1)
        h.put(f"C{fila}", f"=Datos!F{5 + i}", fmt="0")
        if i == 0:
            h.guion(f"D{fila}")
        else:
            h.clave(f"D{fila}", f"=C{fila}-C{fila - 1}",
                    "∇: la celda menos la de arriba. Arrástrala hasta D171." if i == 1 else None, fmt="0")
    return h


# ------------------------------------------------------------------- M9
def hoja_m9(lb):
    J = lb.J
    C = J["airpassengers"]["calendario"]
    h = Hoja(lb, "M9 Calendario", "M9 · Regresores de calendario",
             "Lo que el término estacional no ve: la longitud del mes y una fiesta que cambia de mes.",
             anchos={"A": 40, "B": 11, "C": 11, "D": 11, "E": 7}, ancho_texto=14)
    fc0, fc1 = 60, 203                  # t = 1..144
    h.seccion(4, "1 · Días del mes y Semana Santa")
    h.parrafo(5, "Un SARIMA supone que el patrón cae en la misma posición cada 12 meses. Febrero dura 28 o 29 "
              "días y la Pascua cae en marzo o en abril: dos efectos que se mueven de año en año y que ningún "
              "Φ ni Θ puede absorber. Van como regresores: log(días del mes) y una indicadora del mes que "
              "contiene el Domingo de Pascua.")
    h.completa(6, "en las columnas de cálculo (fila 58), los días del mes con DAY(EOMONTH(fecha, 0)) (en español "
               "DIA y FIN.MES), su logaritmo y la indicadora de Pascua; en la tabla de Meeus (fila 20), las "
               "columnas h, l, mes y día; y la diferencia de duración en B11 y el t de β = 1 en B41.")
    h.encabezados(8, 1, ["", "Este libro", "R / capítulo", "", "✔"])
    h.put("A9", "Días del mes: los 144 = R")
    h.formula("B9", f"=SUMPRODUCT(--(C{fc0}:C{fc1}=H{fc0}:H{fc1}))", fmt="0")
    h.dato("C9", 144, fmt="0")
    h.check("E9", "B9=C9", "M9: los días de cada mes, con DAY(EOMONTH())")
    h.put("A10", "Rango de días")
    h.formula("B10", f'=MIN(C{fc0}:C{fc1})&" a "&MAX(C{fc0}:C{fc1})')
    h.dato("C10", f"{C['rango_dias'][0]} a {C['rango_dias'][1]}")
    h.check("E10", "B10=C10", "M9: de 28 a 31 días")
    h.put("A11", "Diferencia de duración, (31 − 28)/28")
    h.clave("B11", f"=(MAX(C{fc0}:C{fc1})-MIN(C{fc0}:C{fc1}))/MIN(C{fc0}:C{fc1})",
            "(máximo − mínimo) / mínimo: aritmética del calendario, no de los pasajeros.", fmt="0.0%")
    h.dato("C11", C["variacion_pct"] / 100, fmt="0.0%")
    h.check("E11", "ABS(B11-C11)<=0.0005", "M9: un 10.7 % de diferencia de duración")
    h.put("A12", "Meses marcados como Pascua")
    h.formula("B12", f"=SUM(G{fc0}:G{fc1})", fmt="0")
    h.dato("C12", 12, fmt="0")
    h.check("E12", f"AND(B12=C12,COUNT(G{fc0}:G{fc1})=144)", "M9: un mes de Pascua por año")
    h.put("A13", "Pascuas en marzo")
    h.formula("B13", '=COUNTIF(N21:N32,3)', fmt="0")
    h.dato("C13", C["meses_pascua_marzo"], fmt="0")
    h.check("E13", "B13=C13", "M9: en estos 12 años la Pascua cayó en marzo 2 veces")
    h.put("A14", "Fechas de Pascua: las 12 = R")
    h.formula("B14", "=SUMPRODUCT(--(P21:P32=Q21:Q32))", fmt="0")
    h.dato("C14", 12, fmt="0")
    h.check("E14", "B14=C14", "M9: el algoritmo de Meeus en fórmulas")

    h.seccion(17, "2 · La Pascua por el algoritmo de Meeus/Butcher (calendario gregoriano)")
    h.parrafo(18, "a = MOD(año, 19), b = INT(año/100), c = MOD(año, 100), d = INT(b/4), e = MOD(b, 4), "
              "f = INT((b + 8)/25), g = INT((b − f + 1)/3), h = MOD(19a + b − d − g + 15, 30), "
              "i = INT(c/4), k = MOD(c, 4), l = MOD(32 + 2e + 2i − h − k, 7), m = INT((a + 11h + 22l)/451), "
              "mes = INT((h + l − 7m + 114)/31), día = MOD(h + l − 7m + 114, 31) + 1. Cada letra es una columna "
              "de la tabla: a en B, b en C, c en D, d en E, e en F, f en G, g en H, h en I, i en J, k en K, l en L "
              "y m en M. En español, INT es ENTERO y MOD es RESIDUO.")
    cols = ["Año", "a", "b", "c", "d", "e", "f", "g", "h", "i", "k", "l", "m", "mes", "día", "Pascua", "R"]
    for i, s in enumerate(cols):
        h.ws.column_dimensions[L(2 + i)].width = max(h.ws.column_dimensions[L(2 + i)].width, 6)
    h.ws.column_dimensions["P"].width = 12
    h.ws.column_dimensions["Q"].width = 12
    h.encabezados(20, 1, ["Año"] + cols[1:])
    for i in range(12):
        fila = 21 + i
        a_ = f"$A{fila}"
        h.put(f"A{fila}", 1949 + i, align=CENTRO)
        formulas = {
            "B": f"=MOD({a_},19)", "C": f"=INT({a_}/100)", "D": f"=MOD({a_},100)", "E": f"=INT(C{fila}/4)",
            "F": f"=MOD(C{fila},4)", "G": f"=INT((C{fila}+8)/25)", "H": f"=INT((C{fila}-G{fila}+1)/3)",
            "I": f"=MOD(19*B{fila}+C{fila}-E{fila}-H{fila}+15,30)", "J": f"=INT(D{fila}/4)",
            "K": f"=MOD(D{fila},4)", "L": f"=MOD(32+2*F{fila}+2*J{fila}-I{fila}-K{fila},7)",
            "M": f"=INT((B{fila}+11*I{fila}+22*L{fila})/451)",
            "N": f"=INT((I{fila}+L{fila}-7*M{fila}+114)/31)",
            "O": f"=MOD(I{fila}+L{fila}-7*M{fila}+114,31)+1",
        }
        claves_m = {"I": "h = MOD(19a + b − d − g + 15, 30), con a en B, b en C, d en E y g en H.",
                    "L": "l = MOD(32 + 2e + 2i − h − k, 7), con e en F, i en J, h en I y k en K.",
                    "N": "mes = INT((h + l − 7m + 114)/31), con h en I, l en L y m en M.",
                    "O": "día = MOD(h + l − 7m + 114, 31) + 1, con h en I, l en L y m en M."}
        for col, f in formulas.items():
            if col in claves_m:
                h.clave(f"{col}{fila}", f, claves_m[col] if i == 0 else None, fmt="0")
            else:
                h.formula(f"{col}{fila}", f, fmt="0")
        h.formula(f"P{fila}", f"=DATE({a_},N{fila},O{fila})", fmt="yyyy-mm-dd")
        anio = 1949 + i
        y_, m_, d_ = (int(v) for v in C["pascuas"][str(anio)].split("-"))
        h.dato(f"Q{fila}", date(y_, m_, d_), fmt="yyyy-mm-dd")

    h.seccion(35, "3 · Lo que estima R: el airline con los regresores")
    M = C["modelos"]
    h.encabezados(36, 1, ["Modelo", "AICc", "BIC", "β log(días)", "e.e.", "β Pascua", "e.e."], ajuste=True)
    for i, clave_ in enumerate(("sin_regresores", "con_dias", "con_dias_pascua")):
        fila = 37 + i
        m = M[clave_]
        h.put(f"A{fila}", m["nombre"])
        h.dato(f"B{fila}", m["aicc"], fmt="0.00")
        h.dato(f"C{fila}", m["bic"], fmt="0.00")
        co = {c_["nombre"]: c_ for c_ in m["coeficientes"]}
        if "log_dias" in co:
            h.dato(f"D{fila}", co["log_dias"]["valor"], fmt=F4)
            h.dato(f"E{fila}", co["log_dias"]["ee"], fmt=F4)
        if "pascua" in co:
            h.dato(f"F{fila}", co["pascua"]["valor"], fmt=F4)
            h.dato(f"G{fila}", co["pascua"]["ee"], fmt=F4)
    h.put("A41", "¿Pasajeros proporcionales a los días? t de β = 1")
    h.clave("B41", "=(D39-1)/E39", "(β̂ − 1) / e.e.: si los pasajeros fueran proporcionales a los días, β = 1.",
            fmt="0.00")
    h.dato("C41", round((M["con_dias_pascua"]["coeficientes"][2]["valor"] - 1)
                        / M["con_dias_pascua"]["coeficientes"][2]["ee"], 4), fmt="0.00")
    h.check("E41", "ABS(B41-C41)<=0.001", "M9: t de β = 1 vale 0.19: no se rechaza")
    h.put("A42", "Puntos de AICc que gana el calendario")
    h.formula("B42", "=B37-B39", fmt="0.0")
    h.parrafo(43, "β̂ = 1.084 con e.e. 0.446: no se rechaza β = 1, el coeficiente es el que predice la aritmética. "
              "La Pascua suma un 2.9 % de pasajeros. Y aunque el AICc mejora 7.5 puntos, fuera de muestra (M11) "
              "el modelo con calendario sale peor que el airline: el criterio de información y el error de "
              "pronóstico responden preguntas distintas.")
    # columnas de cálculo
    h.seccion(fc0 - 4, "Columnas de cálculo", c2=8)
    h.encabezados(fc0 - 2, 1, ["Fecha", "t", "días", "log(días)", "año", "mes", "Pascua", "R: días"])
    for i in range(144):
        fila = fc0 + i
        h.put(f"A{fila}", f"=DATE(1949,B{fila},1)", fmt=FMES)
        h.put(f"B{fila}", i + 1)
        h.clave(f"C{fila}", f"=DAY(EOMONTH(A{fila},0))",
                "DAY(EOMONTH(A60, 0)): el último día del mes es su número de días. En español, DIA y "
                "FIN.MES." if i == 0 else None, fmt="0")
        h.clave(f"D{fila}", f"=LN(C{fila})", "LN(días): el regresor entra en logaritmos." if i == 0 else None,
                fmt=F4)
        h.formula(f"E{fila}", f"=YEAR(A{fila})", fmt="0")
        h.formula(f"F{fila}", f"=MONTH(A{fila})", fmt="0")
        h.clave(f"G{fila}", f"=IF(F{fila}=INDEX($N$21:$N$32,MATCH(E{fila},$A$21:$A$32,0)),1,0)",
                "1 si el mes es el de la Pascua de su año: IF(F60 = INDEX(columna mes de Meeus, "
                "MATCH(E60, años de Meeus, 0)), 1, 0), con $ en los dos rangos. En español, SI, INDICE y "
                "COINCIDIR." if i == 0 else None, fmt="0")
        h.dato(f"H{fila}", C["dias_mes"][i], fmt="0")
    return h


# ------------------------------------------------------------------- M10
def hoja_m10(lb):
    J = lb.J
    FO = J["airpassengers"]["fourier"]
    ly = [math.log(v) for v in lb.D["airpassengers"]["valores"]]
    h = Hoja(lb, "M10 Fourier", "M10 · Cuando m es grande: los términos de Fourier",
             "La estacionalidad como suma de senos y cosenos: 2K parámetros, sea cual sea m.",
             anchos={"A": 40, "B": 12, "C": 12, "D": 12, "E": 7, "F": 12}, ancho_texto=6)
    f0, f1 = 60, 203
    h.seccion(4, "1 · log y = β₀ + β₁t + Σ_k [α_k sen(2πkt/12) + δ_k cos(2πkt/12)] + error")
    h.put("A5", "K, número de armónicos (1 a 6)")
    h.entrada("B5", FO["mejor_K"])
    dv = DataValidation(type="whole", operator="between", formula1="1", formula2="6", allow_blank=False)
    h.ws.add_data_validation(dv)
    dv.add("B5")
    h.parrafo(6, "Excel no ajusta los errores ARIMA del capítulo, pero sí la parte que importa aquí: la "
              "regresión por mínimos cuadrados de log y sobre una tendencia y 2K columnas de Fourier, con "
              "LINEST (ESTIMACION.LINEAL). Con K = m/2 = 6, sen(2π·6t/12) = sen(πt) vale cero siempre: los términos "
              "son 11, tantos como las indicadoras de 11 meses, y las dos regresiones dan el mismo ajuste.")
    h.completa(7, "las 12 columnas de Fourier en C60:N203, con el k de la fila 57. El seno va en C, E, G, I, K "
               "y N; el coseno en D, F, H, J, L y M: en k = 6 el orden se invierte para que el seno, que vale cero, "
               "quede último y B11 tome t y C:M. Después, la SSR en B11 con INDEX(LINEST(…, TRUE, TRUE), 5, 2), "
               "el R² en B12 y la tabla de K en C17:C22.")
    h.encabezados(9, 1, ["", "Este libro", "Referencia", "", "✔"])
    h.put("A10", "Columnas que entran: t y MIN(2K, 11) de Fourier")
    h.formula("B10", "=1+MIN(2*B5,11)", fmt="0")
    xr = f"OFFSET($B${f0},0,0,144,B10)"
    yr = f"$O${f0}:$O${f1}"
    ssr6, _ = fourier_ssr(ly, 6)
    ssr_d, _ = fourier_ssr(ly, 6, con_indicadoras=True)
    ssr_k = {K: fourier_ssr(ly, K)[0] for K in range(1, 7)}
    h.put("A11", "Suma de cuadrados de los residuos (SSR)")
    h.clave("B11", f"=INDEX(LINEST({yr},{xr},TRUE,TRUE),5,2)",
            "INDEX(LINEST(log y, OFFSET(B60, 0, 0, 144, B10), TRUE, TRUE), 5, 2): la fila 5, columna 2 de "
            "la salida de LINEST es la suma de cuadrados de los residuos. OFFSET (DESREF) elige t y las "
            "primeras 2K columnas de Fourier.", fmt="0.000000")
    h.dato("C11", f"=CHOOSE($B$5,{','.join(str(round(ssr_k[K], 8)) for K in range(1, 7))})", fmt="0.000000")
    h.check("E11", "ABS(B11-C11)<=0.0000001", "M10: SSR de la regresión armónica con el K elegido")
    h.put("D11", "(referencia)", font=F_GUION)
    h.put("A12", "R²")
    h.clave("B12", f"=INDEX(LINEST({yr},{xr},TRUE,TRUE),3,1)",
            "La misma salida de LINEST: la fila 3, columna 1 es el R².", fmt=F6)
    h.put("A13", "SSR con tendencia + 11 indicadoras de mes")
    h.formula("B13", f"=INDEX(LINEST({yr},$P${f0}:$AA${f1},TRUE,TRUE),5,2)", fmt="0.000000")
    h.dato("C13", round(ssr_d, 8), fmt="0.000000")
    h.check("E13", "ABS(B13-C13)<=0.0000001", "M10: SSR con 11 indicadoras de mes")
    h.put("A14", "Con K = 6, ¿Fourier = indicadoras?")
    h.check("E14", "ABS(B11-B13)<=0.0000001", "M10: con K = 6 los términos de Fourier equivalen a 11 indicadoras",
            "$B$5=6")
    lb.cifras["ssr6"] = ssr6
    h.encabezados(16, 1, ["K", "términos", "SSR (MCO)", "R: términos", "", "R: AICc (errores ARIMA)",
                          "R: LB(24) p"], ajuste=True)
    for i, r in enumerate(FO["resultados"]):
        fila = 17 + i
        K = r["K"]
        h.put(f"A{fila}", K, align=CENTRO)
        h.formula(f"B{fila}", f"=MIN(2*A{fila},11)", fmt="0")
        h.clave(f"C{fila}", f"=INDEX(LINEST({yr},OFFSET($B${f0},0,0,144,1+B{fila}),TRUE,TRUE),5,2)",
                "La SSR de B11 con 1 + B17 columnas en vez de B10. Arrástrala hasta K = 6." if i == 0 else None,
                  fmt="0.000000")
        h.dato(f"D{fila}", r["n_terminos"], fmt="0")
        h.dato(f"F{fila}", r["aicc"], fmt="0.00")
        h.dato(f"G{fila}", r["lb24_p"], fmt=F4)
    h.check("E17", "SUMPRODUCT(--(B17:B22=D17:D22))=6", "M10: 2K términos, salvo K = 6, que tiene 11")
    h.parrafo(23, "La trampa del capítulo: el AICc de la regresión armónica (D = 0, 143 observaciones) y el del "
              "airline (D = 1, 131) no viven en la misma escala. Dentro de la familia armónica sí se comparan "
              "entre sí, y por eso se elige K; entre familias, solo fuera de muestra (M11).")
    # el componente estacional
    h.encabezados(25, 1, ["Mes", "s(mes) con K armónicos", "indicadoras, centradas"], ajuste=True)
    h.put("A39", "Coeficientes de cada columna de Fourier (0 si no entra)", font=F_GUION)
    for j in range(12):
        col = 3 + j
        # posición en la salida de LINEST: la columna j+1 de X va en B10 − j
        h.formula(f"{L(col)}40", f"=IF({j + 1}<=$B$10-1,INDEX(LINEST({yr},{xr},TRUE,TRUE),1,$B$10-{j + 1}),0)",
                  fmt="0.00000")
        h.put(f"{L(col)}39", f"col. {j + 1}", font=F_GUION)
    for j in range(11):
        col = 3 + j
        h.formula(f"{L(col)}42", f"=INDEX(LINEST({yr},$P${f0}:$AA${f1},TRUE,TRUE),1,{11 - j})", fmt="0.00000")
        h.put(f"{L(col)}41", f"mes {j + 2}", font=F_GUION)
    for m in range(12):
        fila = 26 + m
        h.put(f"A{fila}", MESES[m], align=CENTRO)
        h.formula(f"B{fila}", f"=SUMPRODUCT($C$40:$N$40,C{f0 + m}:N{f0 + m})", fmt="0.0000")
        efecto = "0" if m == 0 else f"{L(3 + m - 1)}$42"
        h.formula(f"C{fila}", f"={efecto}-(SUM($C$42:$M$42)/12)", fmt="0.0000")
    grafico_lineas(h, "H4", 1, [(2, "Fourier con K armónicos", NARANJA, False),
                                (3, "11 indicadoras (centradas)", VERDE, True)], 26, 37,
                   "El componente estacional: K controla la suavidad", eje_x="mes", salto=1, fmt_y="0.00")
    # columnas de cálculo
    h.seccion(f0 - 5, "Columnas de cálculo", c2=16)
    h.put(f"C{f0 - 3}", "k →", font=F_GUION)
    nombres = []
    ks = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]
    tipos = ["sen", "cos"] * 5 + ["cos", "sen"]
    for j in range(12):
        nombres.append(f"{tipos[j]} k={ks[j]}")
        h.put(f"{L(3 + j)}{f0 - 3}", ks[j], font=F_GUION, align=CENTRO)
    h.encabezados(f0 - 2, 1, ["Fecha", "t"] + nombres + ["log y", "t"] + [f"mes {m}" for m in range(2, 13)],
                  ajuste=True)
    h.ws[f"N{f0 - 2}"].value = "sen k=6 (≡ 0)"
    for i in range(144):
        fila = f0 + i
        t = i + 1
        h.put(f"A{fila}", f"=Datos!A{5 + i}", fmt=FMES)
        h.put(f"B{fila}", t)
        for j in range(12):
            c_ = L(3 + j)
            fun = "SIN" if tipos[j] == "sen" else "COS"
            instr = None
            if i == 0 and j == 0:
                instr = ("SIN(2·PI()·k·t/12), con k de la fila 57 (C$57) y t de la columna B ($B60). Va en "
                         "las columnas de seno: C, E, G, I, K y N (en k = 6, el seno es la última).")
            if i == 0 and j == 1:
                instr = ("COS(2·PI()·k·t/12): lo mismo con el coseno, en D, F, H, J, L y M. Ojo: en k = 6 "
                         "el coseno va en M y el seno en N.")
            h.clave(f"{c_}{fila}", f"={fun}(2*PI()*{c_}${f0 - 3}*$B{fila}/12)", instr, fmt="0.0000")
        h.put(f"O{fila}", f"=Datos!C{5 + i}", fmt="0.00000")
        h.put(f"P{fila}", f"=B{fila}")
        for m in range(2, 13):
            h.formula(f"{L(15 + m)}{fila}", f"=IF(MOD(B{fila}-1,12)+1={m},1,0)", fmt="0")
    return h


# ------------------------------------------------------------------- M11
def hoja_m11(lb):
    J = lb.J
    CO = J["airpassengers"]["comparativa"]
    modelos = list(CO["modelos"].items())
    h = Hoja(lb, "M11 Métricas", "M11 · Panorama comparativo: RMSE, MAE y MAPE",
             "Ocho métodos sobre los últimos 24 meses, y por qué una sola partición no decide nada.",
             anchos={"A": 30, "B": 11}, ancho_texto=12)
    for col in range(3, 11):
        h.ws.column_dimensions[L(col)].width = 14
    h.seccion(4, f"1 · Los pronósticos de R para 1959–1960 (entrenamiento hasta {CO['corte']})", c2=10)
    h.parrafo(5, "Cada método se ajustó en R con los primeros 120 meses. Las métricas se calculan en "
              "pasajeros, la única escala en que los ocho son comparables: RMSE = √(Σ(y − ŷ)²/n), "
              "MAE = Σ|y − ŷ|/n y MAPE = 100·Σ|y − ŷ|/y / n.", c2=10)
    h.completa(6, "RMSE, MAE y MAPE en C35:J37 (escribe la columna C y arrástrala a la derecha) y el puesto por "
               "RMSE en C39:J39 con RANK (JERARQUIA).", c2=10)
    nombres_cortos = {"snaive": "Naïve estacional", "sarima": "SARIMA airline", "auto_arima": "auto.arima",
                      "ets": "ETS sobre la serie cruda", "ets_log": "ETS sobre el log",
                      "armonica": "Armónica K = 6", "stl_arima": "STL + ARIMA",
                      "sarima_calendario": "SARIMA + calendario"}
    h.encabezados(8, 1, ["Fecha", "Observado"] + [nombres_cortos[k] for k, _ in modelos], ajuste=True)
    for i in range(24):
        fila = 9 + i
        a, m = (int(v) for v in CO["fechas_prueba"][i].split("-"))
        h.put(f"A{fila}", date(a, m, 1), fmt=FMES)
        h.dato(f"B{fila}", CO["observado"][i], fmt="0")
        for j, (_, mo) in enumerate(modelos):
            h.dato(f"{L(3 + j)}{fila}", mo["pronostico"][i], fmt="0.00")
    obs = "$B$9:$B$32"
    h.put("A34", "", font=F_NEGRITA)
    etiquetas = [(35, "RMSE"), (36, "MAE"), (37, "MAPE (%)"), (38, "Sesgo medio (y − ŷ)"), (39, "Puesto por RMSE"),
                 (41, "R: RMSE"), (42, "R: MAE"), (43, "R: MAPE"), (44, "k (parámetros)"), (45, "Escala del ajuste"),
                 (46, "¿= R?")]
    for fila, s in etiquetas:
        h.put(f"A{fila}", s, font=F_NEGRITA)
    for j, (clave_, mo) in enumerate(modelos):
        c_ = L(3 + j)
        pr = f"{c_}$9:{c_}$32"
        primera = j == 0
        h.clave(f"{c_}35", f"=SQRT(SUMXMY2({obs},{pr})/COUNT({obs}))",
                "√(SUMXMY2(observado, pronóstico)/n). SUMXMY2 (SUMAXMENOSY2) suma los cuadrados de las "
                "diferencias. Arrástrala a la derecha." if primera else None, fmt="0.000")
        h.clave(f"{c_}36", f"=SUMPRODUCT(ABS({obs}-{pr}))/COUNT({obs})",
                "SUMPRODUCT(ABS(observado − pronóstico))/n." if primera else None, fmt="0.000")
        h.clave(f"{c_}37", f"=100*SUMPRODUCT(ABS(({obs}-{pr})/{obs}))/COUNT({obs})",
                "100·SUMPRODUCT(ABS((observado − pronóstico)/observado))/n." if primera else None, fmt="0.000")
        h.formula(f"{c_}38", f"=AVERAGE({obs})-AVERAGE({pr})", fmt="0.00")
        h.clave(f"{c_}39", f"=RANK({c_}35,$C$35:$J$35,1)",
                "RANK(RMSE, fila de RMSE, 1): 1 al menor." if primera else None, fmt="0")
        h.dato(f"{c_}41", mo["rmse"], fmt="0.000")
        h.dato(f"{c_}42", mo["mae"], fmt="0.000")
        h.dato(f"{c_}43", mo["mape"], fmt="0.000")
        if clave_ == "stl_arima":
            # el capítulo cuenta también los m − 1 valores de la estacionalidad
            h.dato(f"{c_}44", f"{mo['n_par']} + {J['m'] - 1}")
        else:
            h.dato(f"{c_}44", mo["n_par"], fmt="0")
        h.dato(f"{c_}45", mo["escala"])
        h.check(f"{c_}46", f"AND(ABS({c_}35-{c_}41)<=0.002,ABS({c_}36-{c_}42)<=0.002,ABS({c_}37-{c_}43)<=0.002)",
                f"M11: RMSE, MAE y MAPE de {nombres_cortos[clave_]} = R (± 0.002)")
    j_sar = [k for k, _ in modelos].index("sarima")
    j_ets = [k for k, _ in modelos].index("ets_log")
    h.put("A47", "Gana el ETS sobre el log; el SARIMA, cuarto", font=F_NEGRITA)
    h.check(f"C47", f"AND({L(3 + j_ets)}39=1,{L(3 + j_sar)}39=4)",
            "M11: con una sola partición el SARIMA queda cuarto por RMSE")
    h.parrafo(48, "El sesgo medio del SARIMA es igual a su MAE: se queda corto en los 24 meses. El corte cae justo "
              "detrás de 1958, el único año en que el tráfico casi no creció, y el airline ajusta su pendiente a lo "
              "último que ve. Las diferencias de RMSE con 24 puntos no separan métodos con seguridad.", c2=10)
    # origen móvil
    OM = CO["origen_movil"]
    h.seccion(50, f"2 · La misma comparación sobre {OM['n_origenes']} orígenes (capítulo 6)", c2=10)
    h.encabezados(51, 1, ["Método", "RMSE medio", "% que gana al SARIMA", "Puesto"], ajuste=True)
    nombres_om = {"snaive": "Naïve estacional", "sarima": "SARIMA airline", "armonica": "Armónica K = 6",
                  "ets_log": "ETS sobre el log", "ets_orig": "ETS sobre la serie cruda", "stl": "STL + ARIMA"}
    claves_om = list(OM["rmse_medio"])
    for i, k in enumerate(claves_om):
        fila = 52 + i
        h.put(f"A{fila}", nombres_om.get(k, k))
        h.dato(f"B{fila}", OM["rmse_medio"][k], fmt="0.000")
        h.dato(f"C{fila}", OM["porcentaje_gana_al_sarima"][k] / 100, fmt="0.0%")
        h.formula(f"D{fila}", f"=RANK(B{fila},$B$52:$B${51 + len(claves_om)},1)", fmt="0")
    f_sar = 52 + claves_om.index("sarima")
    h.check(f"E{f_sar}", f"D{f_sar}=1", "M11: sobre 61 orígenes, el SARIMA es primero")
    h.parrafo(59, "La conclusión se invierte: el SARIMA pasa de cuarto a primero y le gana a cada rival en más del "
              "85 % de los orígenes. Con una sola partición, el azar de dónde cae el corte pesa más que la "
              "diferencia entre los métodos. Eso es lo que el capítulo 6 enseña a medir.", c2=10)
    cols_g = [(2, "observado", VERDE, False), (3 + j_sar, "SARIMA airline", NARANJA, False),
              (3 + j_ets, "ETS sobre el log", "1F77B4", True),
              (3 + [k for k, _ in modelos].index("armonica"), "Armónica K = 6", "7F7F7F", True),
              (3, "Naïve estacional", "BBBBBB", True)]
    grafico_lineas(h, "L4", 1, cols_g, 9, 32, "1959–1960: observado y pronósticos", ancho=20, alto=9,
                   eje_y="pasajeros (miles)", salto=3, fmt_x=FMES, fmt_y="0")
    return h


# ------------------------------------------------------------------- todo
def construir(modo, D=None, J=None):
    D = D or json.loads((SALIDAS / "datos_series.json").read_text(encoding="utf-8"))
    J = J or json.loads((SALIDAS / "cap5_sarima.json").read_text(encoding="utf-8"))
    lb = Libro(modo, D, J)
    lb.cifras = {}
    portada = hoja_portada(lb)
    datos = hoja_datos(lb)
    modulos = [
        (hoja_m1, "Mapa mes × año, ACF por fórmula, banda"),
        (hoja_m2, "Heladería, polinomio multiplicado, pesos ψ, satélites"),
        (hoja_m3, "Tienda: ∇, ∇₁₂, ∇∇₁₂; las cuatro combinaciones"),
        (hoja_m4, "ACF de ∇∇₁₂ log y, airline teórico, PACF (opcional)"),
        (hoja_m5, "Pesos ψ del airline y σ_h a escalones"),
        (hoja_m6, "Residuales CSS, Ljung–Box, AICc de la rejilla"),
        (hoja_m7, "Pronóstico a 24 meses, bandas, mediana y media"),
        (hoja_m8, "∇TRM frente a ∇USAccDeaths; evidencias"),
        (hoja_m9, "Días del mes, Pascua (Meeus), regresores"),
        (hoja_m10, "Fourier con K armónicos frente a indicadoras"),
        (hoja_m11, "RMSE, MAE, MAPE y el ranking que se invierte"),
    ]
    refs = [(datos, "Las tres series y su comprobación")]
    for fun, que in modulos:
        refs.append((fun(lb), que))
    A = J["airpassengers"]
    air = A["airline"]
    lb.diferencias = [
        ("Ljung–Box(24) del airline (M6)", f"Q = {air['diagnostico']['lb24_Q']}, p = {air['diagnostico']['lb24_p']}",
         f"Q = {lb.cifras['q_css']:.2f}, p = {lb.cifras['p_css']:.3f} con los residuales CSS; idéntico con los de R",
         "La recursión arranca con e = 0 y su primer año es otro: R usa la verosimilitud exacta."),
        ("Pronóstico a 24 meses (M7)", f"{A['pronostico']['original']['media'][23]} pasajeros",
         f"{lb.cifras['m7_mediana_css']:.2f} con CSS; {A['pronostico']['original']['media'][23]} con los residuales de R",
         "Los últimos residuales CSS difieren de los de R en 2·10⁻⁴: un 0.02 %."),
        ("ψ₁₂ y ψ₁₃ del airline (M5)", "1.0412 y 0.8632", "1.0413 y 0.8633",
         "El libro usa θ̂ y Θ̂ con 4 decimales; R, todos."),
        ("ρ₁ del airline teórico (M4)", "−0.3460", "−0.3459",
         "−0.34595 queda en el empate del redondeo; el capítulo lo calcula con θ̂ completo."),
    ]
    portada_contenido(portada, lb, refs)
    for h in lb.hojas:
        h.cerrar()
    lb.wb.calculation.fullCalcOnLoad = True
    lb.wb.properties.creator = "Series de Tiempo 2026-II · Universidad El Bosque"
    lb.wb.properties.title = "Capítulo 5 · Modelos SARIMA, celda a celda"
    lb.wb.active = 0
    return lb


def a_bytes(lb):
    """El .xlsx con fechas internas fijas: mismas entradas, mismos bytes."""
    crudo = io.BytesIO()
    lb.wb.save(crudo)
    zin = zipfile.ZipFile(io.BytesIO(crudo.getvalue()))
    salida = io.BytesIO()
    with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            datos = zin.read(info.filename)
            if info.filename == "docProps/core.xml":
                datos = re.sub(rb"(<dcterms:(?:created|modified)[^>]*>)[^<]*",
                               rb"\g<1>2026-11-03T00:00:00Z", datos)
            zi = zipfile.ZipInfo(info.filename, date_time=FECHA_FIJA)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            zout.writestr(zi, datos)
    return salida.getvalue()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--comprobar", action="store_true",
                    help="no escribe: sale con 1 si los libros del disco no son los que generaría")
    args = ap.parse_args()
    distintos = 0
    DESTINO.mkdir(parents=True, exist_ok=True)
    for modo, nombre in ARCHIVOS.items():
        lb = construir(modo)
        datos = a_bytes(lb)
        ruta = DESTINO / nombre
        if args.comprobar:
            igual = ruta.exists() and ruta.read_bytes() == datos
            print(f"{'igual   ' if igual else 'DISTINTO'} {ruta.relative_to(RAIZ)}")
            distintos += not igual
        else:
            ruta.write_bytes(datos)
            print(f"escrito {ruta.relative_to(RAIZ)}  ({len(datos) // 1024} KB, "
                  f"{len(lb.claves)} celdas clave, {len(lb.comprobaciones)} comprobaciones)")
    sys.exit(1 if distintos else 0)


if __name__ == "__main__":
    main()
