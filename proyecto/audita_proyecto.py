#!/usr/bin/env python3
"""audita_proyecto.py — Audita la guía del proyecto de pronóstico sobre el ARTEFACTO.

No mira la intención del ensamblador: lee
`Htmls_Series/proyecto-pronostico-corte-iii.html` y vuelve a calcular por su
cuenta cada cosa que afirma. Calcado del auditor del proyecto de Diseño
(`Diseno de experimentos/proyecto/audita_proyecto.py`). Ocho frentes:

  A · Calendario   cada fecha impresa tiene el día de la semana que le toca en
                   2026 y cae en la semana del curso que se le atribuye (ancla:
                   la semana 10 empieza el lunes 5 de octubre, P1); ningún hito
                   cae en festivo; la exposición va en días de clase de la
                   semana 16; no hay fechas sueltas.
  B · Pesos        la rúbrica suma lo que dicen sus encabezados y el total es
                   100; la tabla de pesos y la de hitos dicen lo mismo; el
                   proyecto y los quices suman el 100 % del corte (P2); la tabla
                   del tope y la del retraso se recalculan con la regla que el
                   propio documento imprime, y sus valores son alcanzables.
  C · Decisiones   D1–D10: parejas sin tríos, la serie que vale y su longitud
                   mínima (recalculada), la exposición y su guion, el
                   repositorio privado con una release por hito, el descuento,
                   el Corte III sin examen final ni Talleres 4 y 5, el
                   protocolo que congela el preregistro.
  D · Estructura   CSS idéntico al de la plantilla, ids únicos, aria-controls
                   con destino, tablas con caption, enlaces que resuelven (con
                   sus anclas #modulo-N), ningún «<» sin escapar, sin mojibake
                   ni restos de la plantilla, courseData igual a los módulos.
  E · Código R     los bloques de R de la guía corren en un R limpio, en orden;
                   la plantilla .Rmd publicada es la de la fuente y se renderiza
                   sin serie (avisándolo y sin escribir en datos/) y con una.
  F · Contenido    cada «módulo X.Y» citado existe y trata lo que se le
                   atribuye, el ancla de cada enlace es la del módulo que nombra
                   su texto, las series «del material» están de verdad en el
                   material, y lo que la guía afirma del material está en él.
  G · Módulo 6.12  las seis exigencias del informe (y la nota de la IA) siguen en
                   el capítulo 6 publicado, cada una tiene su criterio en la
                   rúbrica, y la guía no contradice lo que el 6.12 promete.
  H · Conjunta     la autorización escrita, quién puede, hasta cuándo se cambia,
                   solo las preguntas (a) y (b), el rezago ≥ h, dos notas con el
                   mismo peso, un repositorio y una release, dos topes.

    python3 proyecto/audita_proyecto.py

Variables de entorno (las usa el arnés `prueba_audita_proyecto.py`):
  PROYECTO_HTML    ruta del HTML a auditar (por defecto, el del sitio)
  PROYECTO_SIN_R   si vale 1, se salta el frente E (tarda unos segundos)
  PROYECTO_RMD     la plantilla .Rmd que renderiza el frente E (por defecto, la fuente)
"""
from __future__ import annotations

import html as _html
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from itertools import combinations_with_replacement

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent
SITIO = RAIZ / "Htmls_Series"
PLANTILLA = RAIZ / "plantilla" / "plantilla-capitulo.html"
PUBLICADO = SITIO / "proyecto-pronostico-corte-iii.html"
RUTA = pathlib.Path(os.environ.get("PROYECTO_HTML", PUBLICADO))
RMD_FUENTE = AQUI / "plantilla-informe.Rmd"
RMD_PUBLICADO = SITIO / "proyecto-pronostico-plantilla.Rmd"
RMD_PRUEBA = pathlib.Path(os.environ.get("PROYECTO_RMD", RMD_FUENTE))
CAP6 = SITIO / "capitulo-6-pronostico-evaluacion.html"

sys.path.insert(0, str(AQUI))
import datos as D  # noqa: E402

# Los módulos se buscan por el título de su h2, no por su número.
N_MODULOS = 10
T_COMO, T_QUE_VALE, T_REPOSITORIO = "Cómo funciona el proyecto", "Qué serie vale", "El repositorio en GitHub"
T_FICHA, T_PREREGISTRO = "Hito 1 · Ficha de la serie", "Hito 2 · Preregistro"
T_AVANCE, T_INFORME = "Hito 3 · Avance", "Hito 4 · Informe y código"
T_CONJUNTA = "El proyecto conjunto con Estadística Espacial"
T_EXPOSICION, T_RUBRICA = "La exposición", "La rúbrica"

# El calendario, recalculado aquí y no importado: un auditor que usara
# `D.semana_del_curso` comprobaría que datos.py coincide consigo mismo.
ANCLA_SEMANA_10 = date(2026, 10, 5)
FESTIVOS_2026 = {date(2026, 10, 12), date(2026, 11, 2), date(2026, 11, 16), date(2026, 12, 8)}
DIAS_DE_CLASE = {1, 2}          # martes y miércoles
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]

# Los módulos de los capítulos que la guía cita, con una palabra de su título:
# una referencia que apunta a otro módulo cae aquí.
CITADOS = {"1.7": "STL", "2.8": "Box", "4.3": "Elegir", "4.4": "Identificar",
           "4.6": "Estimar y comparar", "4.8": "Diagnóstico", "5.3": "Diferenciación estacional",
           "5.4": "Identificar los órdenes", "5.9": "SARIMAX", "6.1": "Residual no es error",
           "6.3": "RMSE y MAE", "6.4": "MAPE", "6.5": "MASE", "6.6": "fuga",
           "6.7": "origen móvil", "6.8": "Diebold", "6.9": "cobertura", "6.11": "IA",
           "6.12": "proyecto"}


class Auditoria:
    def __init__(self):
        self.ok, self.fallos = 0, []

    def check(self, frente: str, cond: bool, que: str, detalle: str = "") -> None:
        print(f"  {'OK ' if cond else 'MAL'} [{frente}] {que}"
              + ("" if cond or not detalle else f"  {detalle}"))
        if cond:
            self.ok += 1
        else:
            self.fallos.append((frente, que, detalle))


def texto_visible(t: str) -> str:
    t = re.sub(r"<(script|style)\b.*?</\1>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", _html.unescape(t)).strip()


def semana(d: date) -> int:
    return 10 + (d - ANCLA_SEMANA_10).days // 7


def selectores(t: str) -> set:
    return set(re.findall(r"^\s*(\.[a-zA-Z][\w-]*)", t[:t.index("</style>")], re.M)) \
        if "</style>" in t else set()


def numero(s: str) -> float:
    return float(s.replace(",", "."))


def frase(d: date) -> str:
    return f"{DIAS[d.weekday()]} {d.day} de {MESES[d.month - 1]}"


def modulos_de(texto: str) -> dict[int, str]:
    return {int(n): c for n, c in re.findall(r'<template id="module-(\d+)">(.*?)</template>', texto, re.S)}


def main() -> int:
    A = Auditoria()
    if not RUTA.exists():
        print(f"!! no existe {RUTA}")
        return 1
    H = RUTA.read_text(encoding="utf-8")
    M = H[H.index('<template id="module-1">'):H.rindex("\n  <script>")]
    por_modulo = modulos_de(M)
    h2 = re.findall(r'<template id="module-(\d+)">.*?<h2[^>]*>([^<]+)</h2>', M, re.S)
    numero_de = {b.strip(): int(a) for a, b in h2}

    def mod(titulo: str) -> str:
        return por_modulo.get(numero_de.get(titulo, -1), "")

    V = texto_visible(M)

    # ------------------------------------------------------------------ A
    print("\n=== A · Calendario ===")
    fechas = re.findall(r"\b(" + "|".join(DIAS) + r") (\d{1,2})(?: o (?:" + "|".join(DIAS)
                        + r") \d{1,2})? de (" + "|".join(MESES) + r")\b", V)
    # «martes 17 o miércoles 18 de noviembre» lleva dos fechas: se leen las dos.
    for d1, n1, d2, n2, mes in re.findall(r"\b(" + "|".join(DIAS) + r") (\d{1,2}) o (" + "|".join(DIAS)
                                          + r") (\d{1,2}) de (" + "|".join(MESES) + r")\b", V):
        fechas += [(d2, n2, mes)]
    A.check("A", len(fechas) > 0, "el documento imprime fechas", f"({len(fechas)})")
    for dia, n, mes in sorted(set(fechas)):
        d = date(2026, MESES.index(mes) + 1, int(n))
        A.check("A", DIAS[d.weekday()] == dia, f"«{dia} {n} de {mes}» es {dia} en 2026",
                f"(es {DIAS[d.weekday()]})")

    hitos = D.HITOS
    l16 = ANCLA_SEMANA_10 + timedelta(weeks=D.SEMANA_EXPOSICION - 10)
    permitidas = {h["fecha"] for h in hitos} | {l16, l16 + timedelta(days=5)} | set(D.DIAS_EXPOSICION)
    impresas = {date(2026, MESES.index(m) + 1, int(n)) for _d, n, m in fechas}
    sueltas = sorted(impresas - permitidas)
    A.check("A", not sueltas, "ninguna fecha suelta: todas son de un hito o de la semana de la exposición",
            f"({', '.join(map(str, sueltas))})")

    for h in hitos:
        f = h["fecha"]
        A.check("A", semana(f) == h["semana"], f"{h['nombre']}: el {frase(f)} cae en la semana {h['semana']}",
                f"(cae en la {semana(f)})")
        A.check("A", f not in FESTIVOS_2026, f"{h['nombre']}: el {frase(f)} no es festivo")
        fila = re.search(rf"<strong>{re.escape(h['nombre'])}</strong></td>.*?</tr>", M, re.S)
        A.check("A", bool(fila) and frase(f) in fila.group(0) and f"<td>{h['semana']}</td>" in fila.group(0),
                f"{h['nombre']}: su fila de la tabla dice «{frase(f)}» y la semana {h['semana']}")
    for titulo, hid in ((T_FICHA, "ficha"), (T_PREREGISTRO, "preregistro"),
                        (T_AVANCE, "avance"), (T_INFORME, "informe")):
        h = D.HITO[hid]
        cierre = f"{frase(h['fecha'])} a las {D.HORA_ENTREGA}"
        txt = texto_visible(mod(titulo))
        A.check("A", cierre in txt and f"semana {h['semana']}" in txt,
                f"«{titulo}» dice que cierra el «{cierre}», en la semana {h['semana']}")
    orden = [h["fecha"] for h in hitos]
    A.check("A", orden == sorted(orden) and len(set(orden)) == len(orden), "los hitos van en orden")
    A.check("A", all(semana(d) == D.SEMANA_EXPOSICION and d.weekday() in DIAS_DE_CLASE
                     for d in D.DIAS_EXPOSICION) and max(orden) < min(D.DIAS_EXPOSICION),
            "la exposición va en días de clase de la semana 16, después del informe")
    informe = D.HITO["informe"]["fecha"]
    A.check("A", informe.weekday() == 6 and (informe + timedelta(days=1)) in FESTIVOS_2026
            and "domingo" in texto_visible(mod(T_COMO)) and "festivo" in texto_visible(mod(T_COMO)),
            "el informe cierra un domingo porque el lunes siguiente es festivo, y el módulo 1 lo explica")
    frase16 = f"del lunes {l16.day} al sábado {(l16 + timedelta(days=5)).day} de {MESES[l16.month - 1]}"
    A.check("A", V.count(frase16) >= 2 and f"semana {D.SEMANA_EXPOSICION}" in V,
            f"la exposición: «semana {D.SEMANA_EXPOSICION}» y «{frase16}» en dos módulos")
    fila_expo = re.search(r"<strong>Exposición</strong></td>.*?</tr>", M, re.S)
    A.check("A", D.DIA_EXPOSICION in texto_visible(mod(T_COMO))
            and D.DIA_EXPOSICION in texto_visible(mod(T_EXPOSICION))
            and bool(fila_expo) and "<td>se acuerda en clase</td>" in fila_expo.group(0),
            "el día exacto de la exposición se acuerda en clase (módulo 1, su módulo y la tabla)")
    horas = set(re.findall(r"a las (\d{1,2}:\d{2})", V))
    A.check("A", horas == {D.HORA_ENTREGA}, f"todas las entregas cierran a las {D.HORA_ENTREGA}",
            f"({sorted(horas)})")

    # ------------------------------------------------------------------ B
    print("\n=== B · Pesos ===")
    rub = mod(T_RUBRICA)
    encabezados = dict((t, int(p)) for t, p in re.findall(r"<h3>([^<]+?) · (\d+) puntos</h3>", rub))
    criterios = re.findall(r"<caption><strong>([A-Z]\d) · ([^<]+)</strong> — (\d+) puntos\.", rub)
    n_crit = sum(len(b["criterios"]) for b in D.RUBRICA)
    A.check("B", len(criterios) == n_crit, f"la rúbrica publica sus {n_crit} criterios", f"({len(criterios)})")
    prefijo = {"Preregistro": "P", "Avance": "A", "Informe y código": "I", "Exposición": "E"}
    sumas = {}
    for titulo, letra in prefijo.items():
        sumas[titulo] = sum(int(p) for cid, _n, p in criterios if cid.startswith(letra))
        A.check("B", encabezados.get(titulo) == sumas[titulo],
                f"{titulo}: sus criterios suman lo que dice su encabezado",
                f"(encabezado {encabezados.get(titulo)}, criterios {sumas[titulo]})")
    A.check("B", sum(sumas.values()) == 100, "la rúbrica entera suma 100", f"({sum(sumas.values())})")

    m1 = mod(T_COMO)
    pesos = re.findall(r"<td>([^<]+)</td><td>[A-Z0-9, ]+</td><td>(\d+) %</td><td><strong>([\d.]+) %</strong></td>", m1)
    A.check("B", len(pesos) == 4, "la tabla de pesos tiene los cuatro hitos", f"({len(pesos)})")
    corte = re.findall(r"el proyecto vale el <strong>(\d+) %</strong> de la nota del Corte\s+III", m1)
    del_corte = int(corte[0]) if corte else None
    A.check("B", del_corte == D.PROYECTO_DEL_CORTE,
            f"el módulo 1 dice que el proyecto vale el {D.PROYECTO_DEL_CORTE} % del Corte III", f"({corte})")
    quices = re.findall(r"los quices que se hacen en clase, el otro <strong>(\d+) %</strong>", m1)
    A.check("B", quices == [str(D.QUICES_DEL_CORTE)] and del_corte is not None
            and del_corte + int(quices[0]) == 100,
            f"P2 · los quices en clase son el otro {D.QUICES_DEL_CORTE} % y el corte suma 100", f"({quices})")
    banner = re.search(r"SERIES DE TIEMPO \(20948\) • CORTE III •(.*?)• UNBOSQUE", H, re.S)
    A.check("B", bool(banner) and f"{D.PROYECTO_DEL_CORTE}&nbsp;% DE LA NOTA DEL CORTE" in banner.group(1),
            "la cabecera dice el mismo porcentaje")
    for titulo, p_proy, p_corte in pesos:
        A.check("B", sumas.get(titulo) == int(p_proy), f"pesos · {titulo}: {p_proy} % del proyecto, como la rúbrica")
        if del_corte:
            A.check("B", abs(int(p_proy) * del_corte / 100 - float(p_corte)) < 1e-9,
                    f"pesos · {titulo}: {p_proy} % × {del_corte} % = {p_corte} % del corte")
    A.check("B", sum(int(p) for _t, p, _c in pesos) == 100
            and abs(sum(float(c) for *_x, c in pesos) - (del_corte or 0)) < 1e-9,
            "la tabla de pesos suma 100 % del proyecto y el porcentaje del corte")
    curso = re.search(r"Corte III es el (\d+) % del curso, así que el proyecto es el\s+<strong>([\d.]+) %</strong>", m1)
    A.check("B", bool(curso) and del_corte is not None
            and abs(del_corte * int(curso.group(1)) / 100 - float(curso.group(2))) < 1e-9,
            "el porcentaje de la nota final es el del corte por el del Corte III")
    nombre_titulo = {"preregistro": "Preregistro", "avance": "Avance", "informe": "Informe y código"}
    for h in D.HITOS:
        fila = re.search(rf"<strong>{re.escape(h['nombre'])}</strong></td>.*?</tr>", M, re.S)
        esperado = "sin nota" if h["id"] == "ficha" else f"{sumas.get(nombre_titulo[h['id']])} %"
        A.check("B", bool(fila) and f"<td>{esperado}</td>" in fila.group(0), f"hitos · {h['nombre']}: peso «{esperado}»")
    expo = re.search(r"<strong>Exposición</strong></td>.*?</tr>", M, re.S)
    A.check("B", bool(expo) and f"<td>{sumas['Exposición']} %</td>" in expo.group(0),
            f"hitos · Exposición: peso «{sumas['Exposición']} %»")
    for t_mod, titulo in ((T_PREREGISTRO, "Preregistro"), (T_AVANCE, "Avance"),
                          (T_INFORME, "Informe y código"), (T_EXPOSICION, "Exposición")):
        dice = re.findall(r"vale el\s+<strong>(\d+) %</strong> del proyecto", mod(t_mod), re.I)
        A.check("B", dice == [str(sumas[titulo])], f"«{t_mod}» dice que vale el {sumas[titulo]} % del proyecto",
                f"({dice})")
    regla = re.search(r"se descuenta el <strong>(\d+) %</strong> de la nota que\s+habría tenido", m1)
    tasa = int(regla.group(1)) if regla else None
    base = re.search(r"habría sacado\s+(\d,\d+)\.</caption>", m1)
    retraso = re.findall(r"<tr><td>(\d+)</td><td>(\d+) %</td><td>(\d,\d+)</td></tr>", m1)
    A.check("B", tasa is not None and bool(base) and len(retraso) >= 3,
            "el módulo 1 imprime la regla del retraso y su tabla", f"({tasa}, {len(retraso)} filas)")
    for s, desc, queda in retraso:
        s, desc, queda = int(s), int(desc), numero(queda)
        esperado = round(max(0.0, numero(base.group(1)) * (1 - s * (tasa or 0) / 100)), 2) if base else None
        A.check("B", desc == s * (tasa or 0) and esperado is not None and abs(queda - esperado) < 0.006,
                f"retraso · {s} sesión(es): {desc} % y la nota queda en {queda}",
                f"(recalculado: {s * (tasa or 0)} % y {esperado})")
    permitidos = {str(v) for v in sumas.values()} | {"100", str(D.PROYECTO_DEL_CORTE),
                                                     str(D.QUICES_DEL_CORTE), str(D.CORTE_III_DEL_CURSO)}
    permitidos |= {c for *_x, c in pesos} | ({curso.group(2)} if curso else set())
    p_esc = sumas["Preregistro"] + sumas["Avance"] + sumas["Informe y código"]
    permitidos |= {str(p_esc), str(tasa)} | {d for _s, d, _q in retraso}
    permitidos |= {"80", "95"}          # los niveles de los intervalos
    sueltos = sorted(set(re.findall(r"(\d+(?:\.\d+)?) %", V)) - permitidos)
    A.check("B", not sueltos, "ningún porcentaje suelto", f"({sueltos})")

    niveles = re.findall(r"<tr><td>(Insuficiente|Aceptable|Sólido)</td><td>(\d,\d)</td></tr>", rub)
    valor = {n.lower(): numero(v) for n, v in niveles}
    A.check("B", valor == {n: v for n, v in D.NIVELES}, "la tabla de niveles dice lo que vale cada uno", f"({niveles})")

    umbral = re.search(r"\\frac\{\\text\{preguntas\}\}\{([\d.]+)\}", m1)
    u = float(umbral.group(1)) if umbral else None
    A.check("B", u == D.UMBRAL_TOPE, f"la fórmula del tope divide entre {D.divisor(D.UMBRAL_TOPE)}")
    filas = re.findall(r"<tr><td>([^<]+)</td><td>(\d,\d+)</td><td>(\d,\d+)</td><td>(\d,\d+)</td>"
                       r"<td>(\d,\d+)</td><td><strong>(\d,\d+)</strong></td></tr>", m1)
    A.check("B", len(filas) == len(D.EJEMPLOS_TOPE), "la tabla del tope tiene sus filas", f"({len(filas)})")
    alcanzables = {round(sum(c) / k, 2) for k in (1, 2, 3)
                   for c in combinations_with_replacement(valor.values() or [0], k)}
    p_e1 = next((int(p) for cid, _n, p in criterios if cid == "E1"), 0)
    p_e2 = next((int(p) for cid, _n, p in criterios if cid == "E2"), 0)
    leyenda = re.search(r"<caption>Qué cambia el tope\.(.*?)</caption>", m1, re.S)
    ley = re.sub(r"\s+", " ", leyenda.group(1)) if leyenda else ""
    A.check("B", f"Lo escrito vale {p_esc} puntos" in ley and f"(E1) {p_e1}" in ley and f"(E2) {p_e2}" in ley,
            f"tope · la leyenda da los pesos con los que sale la tabla: {p_esc}, {p_e1} y {p_e2}")
    # Lo escrito es una media de niveles ponderada por los puntos de sus
    # criterios: se enumeran las sumas alcanzables por programación dinámica
    # (3^13 combinaciones por fuerza bruta serían 1,6 millones).
    p_escritos = [int(p) for cid, _n, p in criterios if cid[0] in "PAI"]
    sumas_alc = {0.0}
    for p in p_escritos:
        sumas_alc = {round(s + p * v, 4) for s in sumas_alc for v in (valor.values() or [0])}
    escritos = {round(s / sum(p_escritos), 2) for s in sumas_alc} if p_escritos else set()
    for sit, esc, x, q, sin, con in filas:
        A.check("B", numero(x) in set(valor.values()), f"tope · «{sit}»: la exposición (E1) vale un nivel ({x})")
        A.check("B", round(numero(esc), 2) in escritos,
                f"tope · «{sit}»: lo escrito ({esc}) es alcanzable con los niveles y los puntos")
        esc_, x_, q_, sin_, con_ = map(numero, (esc, x, q, sin, con))
        f = min(1.0, q_ / u) if u else 1.0
        sin_ok = round((p_esc * esc_ + p_e1 * x_ + p_e2 * q_) / 100, 2)
        con_ok = round((p_esc * esc_ * f + p_e1 * x_ + p_e2 * q_) / 100, 2)
        A.check("B", abs(sin_ - sin_ok) < 0.006 and abs(con_ - con_ok) < 0.006,
                f"tope · «{sit}»: {sin} sin tope y {con} con tope", f"(recalculado: {sin_ok} y {con_ok})")
        A.check("B", round(q_, 2) in alcanzables,
                f"tope · «{sit}»: una nota de preguntas de {q} es alcanzable con los tres niveles")
    if filas:
        A.check("B", f"pasa de <strong>{filas[0][4]}</strong> a <strong>{filas[0][5]}</strong>" in m1,
                "el texto bajo la tabla del tope cita la primera fila")

    # ------------------------------------------------------------------ C
    print("\n=== C · Decisiones ===")
    A.check("C", "individual o en parejas" in V, "D1 · el proyecto es individual o en parejas")
    trios = [mo.start() for mo in re.finditer(r"tr[ií]os?\b", V)]
    legitimos = [mo.start() + 7 for mo in re.finditer(r"no hay tr[ií]os", V)]
    A.check("C", set(trios) <= set(legitimos), "D1 · «tríos» solo aparece para decir que no los hay")
    vale = texto_visible(mod(T_QUE_VALE))
    formula = re.search(r"n \\;\\ge\\; T_0 \+ h \+ \((\d+) - 1\), \\qquad T_0 \\;\\ge\\; \\max\((\d+)\\,m,\\ (\d+)\)",
                        mod(T_QUE_VALE))
    A.check("C", bool(formula), "D2 · el módulo 2 imprime la condición de longitud")
    if formula:
        org, ciclos, t0min = (int(x) for x in formula.groups())
        frec = re.findall(r"<tr><td>([^<]+)</td><td>\$(\d+)\$</td><td>\$(\d+)\$</td><td>\$(\d+)\$</td>"
                          r"<td><strong>\$(\d+)\$</strong></td></tr>", mod(T_QUE_VALE))
        A.check("C", len(frec) >= 3, "D2 · la tabla de longitudes mínimas tiene sus filas", f"({len(frec)})")
        for f_, m_, h_, t0_, n_ in frec:
            m_, h_, t0_, n_ = int(m_), int(h_), int(t0_), int(n_)
            A.check("C", t0_ == max(ciclos * m_, t0min) and n_ == t0_ + h_ + org - 1,
                    f"D2 · {f_}: T0 = {t0_} y n mínimo = {n_}, con la regla impresa",
                    f"(recalculado: {max(ciclos * m_, t0min)} y {max(ciclos * m_, t0min) + h_ + org - 1})")
        ejemplo = re.search(r"frente a un mínimo de (\d+) para \$h = 12\$", texto_visible(mod(T_FICHA)))
        A.check("C", bool(ejemplo) and int(ejemplo.group(1)) == max(ciclos * 12, t0min) + 12 + org - 1,
                "D2 · el ejemplo de la ficha usa el mínimo mensual que da la regla")
    # La comprobación que caza una serie inventada (RESISTENCIA_IA.md, Javier, 2026-10-21).
    p1 = re.search(r"P1 · .*?</table>", mod(T_RUBRICA), re.S)
    i7 = re.search(r"I7 · .*?</table>", mod(T_RUBRICA), re.S)
    A.check("C", "La serie se vuelve a descargar" in vale and "Si no coincide, P1 e I7 quedan en insuficiente" in vale
            and "fecha de corte" in vale and "no cuentan como diferencia" in vale
            and bool(p1) and "no coincide con la que se vuelve a descargar" in texto_visible(p1.group(0))
            and bool(i7) and "no coincide con la que se vuelve a descargar" in texto_visible(i7.group(0)),
            "la serie se vuelve a descargar: si no coincide, P1 e I7 en insuficiente (módulo 2 y rúbrica)")
    A.check("C", "Las series simuladas" in vale and "Las series que trae R" in vale and "Las series del material" in vale,
            "D2 · no valen las series del material, las de R ni las simuladas")
    A.check("C", "el dado decide quién contesta cada pregunta" in V and "cada integrante contesta al menos una" in V
            and "esa es suya, sin dado" in V,
            "D4 · en pareja, el dado reparte las preguntas y la última va a quien no ha contestado")
    A.check("C", f"{D.MINUTOS_EXPOSICION} minutos" in V and f"{D.MINUTOS_PREGUNTAS} de preguntas" in V,
            f"D4 · {D.MINUTOS_EXPOSICION} minutos de exposición y {D.MINUTOS_PREGUNTAS} de preguntas")
    guion = re.search(r"<caption>Un reparto posible de los minutos de la exposición simple\.</caption>(.*?)</table>",
                      mod(T_EXPOSICION), re.S)
    minutos = [int(x) for x in re.findall(r"</td><td>(\d+)</td></tr>", guion.group(1))] if guion else []
    A.check("C", sum(minutos) == D.MINUTOS_EXPOSICION,
            f"D4 · el guion de la exposición suma {D.MINUTOS_EXPOSICION} minutos", f"({minutos})")
    A.check("C", "La declaración de uso es obligatoria" in V and "Puedes usar IA" in V,
            "D14 · la IA se permite y su declaración es obligatoria")
    repo = texto_visible(mod(T_REPOSITORIO))
    A.check("C", D.CANAL_ENTREGA in V, f"D8 · el canal de entrega: «{D.CANAL_ENTREGA}»")
    A.check("C", "repositorio privado de GitHub" in repo and "Créalo privado" in repo, "D8 · el repositorio es privado")
    A.check("C", f"el usuario {D.USUARIO_DOCENTE}" in repo and "colaborador" in repo,
            f"D8 · se invita al docente ({D.USUARIO_DOCENTE}) como colaborador")
    etiquetas = re.findall(r"con su etiqueta: (.*?)\. En GitHub", repo)
    A.check("C", bool(etiquetas) and all(D.ETIQUETA[h["id"]] in etiquetas[0] for h in D.HITOS),
            "D8 · el módulo del repositorio da la etiqueta de la release de cada hito", f"({etiquetas})")
    for titulo, hid in ((T_FICHA, "ficha"), (T_PREREGISTRO, "preregistro"), (T_AVANCE, "avance"), (T_INFORME, "informe")):
        A.check("C", bool(re.search(rf"release\s+<code>{D.ETIQUETA[hid]}</code>", mod(titulo))),
                f"D8 · «{titulo}» se entrega con la release «{D.ETIQUETA[hid]}»")
    A.check("C", "la hora en que GitHub publica la release" in repo and "no se vuelve a editar" in repo
            and "una etiqueta se puede cambiar de commit" in repo,
            "D8 · cuenta la hora de la release, la release congela el protocolo y la etiqueta no se mueve")
    A.check("C", tasa == D.DESCUENTO_POR_SESION and "sobre la nota original" in V
            and "La primera sesión cuenta desde el cierre" in V,
            f"D9 · {D.DESCUENTO_POR_SESION} % por sesión, sobre la nota original, desde el cierre", f"({tasa})")
    A.check("C", "no tiene examen final ni Talleres 4 y 5" in V
            and V.count("examen") == V.count("no tiene examen final") and V.count("Taller") == V.count("Talleres 4 y 5"),
            "P2 · el Corte III no tiene examen final ni Talleres 4 y 5, y no se nombran para nada más")
    A.check("C", f"{D.PALABRAS_FICHA} palabras" in V and f"{D.PAGINAS_PREREGISTRO} páginas" in V
            and f"{D.PAGINAS_INFORME} páginas" in V, "las extensiones de la ficha, el preregistro y el informe")
    pre = texto_visible(mod(T_PREREGISTRO))
    campos = re.findall(r"<li><strong>(.*?)</strong>", mod(T_PREREGISTRO))
    A.check("C", len(campos) == 10, "D10 · el preregistro tiene diez campos", f"({len(campos)})")
    for cosa in ("El horizonte", "La métrica", "$T_0$ y el número de orígenes", "La ventana",
                 "El método de referencia", "Los candidatos", "El diagnóstico previsto", "Los niveles de los intervalos"):
        A.check("C", any(c.startswith(cosa) for c in campos), f"D10 · el preregistro fija «{cosa}»")
    A.check("C", "solo ese tramo" in pre and "en silencio" in pre and "exploratorio" in pre,
            "D10 · se elige solo con el entrenamiento; cambiar se permite, en silencio no; lo exploratorio aparte")

    frente_contenido(A, M, V, mod)
    frente_m12(A, mod)
    frente_conjunta(A, V, mod)

    # ------------------------------------------------------------------ D
    print("\n=== D · Estructura ===")
    sel = selectores(H)
    A.check("D", sel == selectores(PLANTILLA.read_text(encoding="utf-8")),
            f"el CSS es el de la plantilla ({len(sel)} selectores)")
    ids = re.findall(r' id="([^"]+)"', H)
    repes = sorted({i for i in ids if ids.count(i) > 1})
    A.check("D", not repes, "los identificadores son únicos", f"({repes})")
    huerfanos = sorted(set(re.findall(r'aria-controls="([^"]+)"', H)) - set(ids))
    A.check("D", not huerfanos, "todo aria-controls tiene destino", f"({huerfanos})")
    A.check("D", M.count("<table>") == M.count("<caption"), "toda tabla lleva caption",
            f"({M.count('<table>')} tablas, {M.count('<caption')} captions)")
    locales = [h for h in re.findall(r'href="([^"]+)"', M) if not h.startswith(("http", "mailto", "#"))]
    rotos = []
    for h in locales:
        archivo, _, ancla = h.partition("#")
        ruta = SITIO / archivo
        if archivo == RMD_PUBLICADO.name:
            continue
        if not ruta.exists():
            rotos.append(h)
        elif ancla and (not re.fullmatch(r"modulo-\d+", ancla)
                        or int(ancla.split("-")[1]) not in modulos_de(ruta.read_text(encoding="utf-8"))):
            rotos.append(h)
    A.check("D", not rotos, f"los {len(locales)} enlaces locales resuelven, anclas incluidas", f"({sorted(set(rotos))})")
    A.check("D", f'href="{RMD_PUBLICADO.name}"' in M, "la guía enlaza la plantilla .Rmd")
    sin_codigo = re.sub(r"<pre>.*?</pre>", " ", M, flags=re.S)
    sin_codigo = re.sub(r"\$\$.*?\$\$|\$[^$]+\$", " ", sin_codigo, flags=re.S)
    sueltos = re.findall(r"<(?![a-zA-Z/!])", sin_codigo)
    A.check("D", not sueltos, "ningún «<» sin escapar en el marcado", f"({len(sueltos)})")
    codigos = re.findall(r'<code class="language-r">(.*?)</code>', M, re.S)
    A.check("D", codigos and all("<" not in c for c in codigos), "el R de la guía va escapado")
    moji = [s for s in ("Ã", "Â", "â€", "\ufffd") if s in H]
    A.check("D", not moji, "sin mojibake", f"({moji})")
    sin_tilde = re.findall(r"\b(analisis|pronostico|numero|modulo|pagina|metodo|estadistica|serie temporal)\b",
                           texto_visible(re.sub(r"<code>.*?</code>", " ", sin_codigo, flags=re.S)), re.I)
    A.check("D", not sin_tilde, "sin palabras comunes sin tilde", f"({sorted(set(sin_tilde))})")
    for resto in ("PLANTILLA BASE", "Cajas y tipografía", "demo-deslizadores", "AUTOEVALUACIONES['demo']",
                  "demo-mapa", "demo-rubrica", "Nombre del curso"):
        A.check("D", resto not in H, f"no queda «{resto}»")
    i = H.find("const courseData")
    titulos_cd = re.findall(r'\{ id: (\d+), title: "([^"]+)"', H[i:i + 3000])
    A.check("D", [(int(a), b) for a, b in titulos_cd] == [(int(a), b.strip()) for a, b in h2]
            and len(h2) == N_MODULOS, f"courseData tiene los {N_MODULOS} módulos, con el título de su h2")
    kb = len(H.encode("utf-8")) / 1024
    A.check("D", kb < 500, f"pesa {kb:.0f} KB, dentro de los 500 KB")

    # ------------------------------------------------------------------ E
    if os.environ.get("PROYECTO_SIN_R") == "1":
        print("\n=== E · Código R (saltado: PROYECTO_SIN_R=1) ===")
    else:
        print("\n=== E · Código R ===")
        frente_r(A, M)

    print("\n" + "=" * 62)
    print(f"  {A.ok + len(A.fallos)} comprobaciones · {len(A.fallos)} fallo(s)")
    print("=" * 62)
    if A.fallos:
        print("\nAbiertos:")
        for fr, que, det in A.fallos:
            print(f"  · [{fr}] {que}  {det}")
        return 1
    print("\nTodo limpio.")
    return 0


def frente_contenido(A: Auditoria, M: str, V: str, mod) -> None:
    print("\n=== F · Contenido ===")
    # Cada «módulo X.Y» (y «módulos X.Y a/y Z.W») existe y trata lo que se le atribuye.
    citados = set()
    for a, b in re.findall(r"módulos? (\d+\.\d+)(?: (?:a|y) (\d+\.\d+))?", V):
        citados |= {a} | ({b} if b else set())
    citados |= set(re.findall(r"módulo \d+\.\d+ y (\d+\.\d+)", V))
    titulos = {}
    for p in SITIO.glob("capitulo-*.html"):
        for t in re.findall(r"<h2[^>]*>(.*?)</h2>", p.read_text(encoding="utf-8"), re.S):
            s = texto_visible(t)
            k = re.match(r"(\d+\.\d+)\s", s)
            if k:
                titulos[k.group(1)] = s
    for c in sorted(citados, key=lambda x: [int(n) for n in x.split(".")]):
        A.check("F", c in CITADOS and CITADOS[c].lower() in titulos.get(c, "").lower(),
                f"la guía cita el módulo {c} y ese módulo es el que dice", f"({titulos.get(c, 'no existe')[:60]})")
    # El ancla de cada enlace es la del módulo que nombra su texto.
    for cap, n, texto in re.findall(r'<a href="capitulo-(\d+)-[^"#]+\.html#modulo-(\d+)">(.*?)</a>', M, re.S):
        A.check("F", f"{cap}.{n}" in texto_visible(texto),
                f"el enlace a capitulo-{cap}#modulo-{n} lo nombra su texto («{texto_visible(texto)[:40]}»)")
    # Las series «del material» están de verdad en el material.
    material = " ".join(texto_visible(p.read_text(encoding="utf-8")) for p in SITIO.glob("*.html")
                        if p.name != RUTA.name and p.name != PUBLICADO.name)
    for s in D.SERIES_DEL_MATERIAL:
        A.check("F", re.search(rf"\b{re.escape(s)}\b", material) is not None,
                f"«{s}», que la guía da por serie del material, aparece en el material")
    # Lo que la guía afirma del material.
    cap4 = (SITIO / "capitulo-4-modelos-arima.html").read_text(encoding="utf-8")
    c4 = modulos_de(cap4)
    c6 = modulos_de(CAP6.read_text(encoding="utf-8"))
    A.check("F", "fitdf" in texto_visible(c4.get(8, "")) and "grados de libertad" in texto_visible(mod(T_INFORME)),
            "Ljung–Box: el 4.8 descuenta los parámetros (fitdf), como dice la guía")
    A.check("F", "AICc de distinto d" in texto_visible(c4.get(6, "")) or "distinto d" in texto_visible(c4.get(6, "")),
            "AICc entre distintas d: el 4.6 dice que no son comparables")
    A.check("F", "falla estrepitosamente al" in texto_visible(c6.get(9, "")),
            "cobertura a un solo nivel: el 6.9 muestra un intervalo que pasa al 95 % y falla al 80 %")
    m12 = texto_visible(c6.get(12, ""))
    A.check("F", "se invierte el podio" in m12 and "no coinciden" in m12,
            "una sola partición: en el ejercicio 1 del 6.12 se invierte el orden")
    m5 = _html.unescape(mod(T_PREREGISTRO))
    dm5 = next((l for l in m5.splitlines() if "dm.test(" in l and not l.lstrip().startswith("#")), "")
    A.check("F", "power = 1" in dm5 and "power = 2 con el RMSE" in m5,
            "el Diebold–Mariano del preregistro usa la pérdida de la métrica (MASE, power = 1)")
    A.check("F", "deriva" in texto_visible(mod(T_INFORME)) and "length(coef(modelo))" in _html.unescape(mod(T_INFORME)),
            "la guía avisa de que fitdf no cuenta la deriva")
    A.check("F", "initial = 35" in m12 and "T_0 = 36" in m12 and "initial = T0 - 1" in _html.unescape(mod(T_PREREGISTRO)),
            "tsCV: initial = T0 - 1 deja el primer origen en T0, como en el 6.12")
    A.check("F", "13" in m12 and "veinte datos efectivos" in m12 and "veinte datos" in texto_visible(mod(T_QUE_VALE)),
            "la longitud mínima: el airline y sus trece observaciones en las diferencias (6.12)")


def frente_m12(A: Auditoria, mod) -> None:
    """G · Lo que el Módulo 12 del capítulo 6 promete al estudiante."""
    print("\n=== G · Módulo 6.12 ===")
    m12 = texto_visible(modulos_de(CAP6.read_text(encoding="utf-8")).get(12, ""))
    tabla = re.search(r"<caption>Las exigencias del módulo 6\.12 y los criterios que las califican\.</caption>(.*?)</table>",
                      mod(T_RUBRICA), re.S)
    filas = dict(re.findall(r"<tr><td>([^<]+)</td><td>([A-Z0-9, ]*)</td></tr>", tabla.group(1))) if tabla else {}
    rub = mod(T_RUBRICA)
    ids_rubrica = set(re.findall(r"<caption><strong>([A-Z]\d) · ", rub))
    for clave, texto in D.EXIGENCIAS_M12.items():
        A.check("G", texto in m12, f"«{texto}» sigue en el módulo 6.12 publicado")
        crit = [c.strip() for c in filas.get(_html.escape(texto, quote=False), "").split(",") if c.strip()]
        A.check("G", bool(crit) and set(crit) <= ids_rubrica,
                f"«{texto}» tiene criterio en la rúbrica ({', '.join(crit) or 'ninguno'})")
    V = texto_visible("".join(mod(t) for t in (T_PREREGISTRO, T_INFORME, T_QUE_VALE, T_COMO)))
    A.check("G", "El MASE por defecto" in m12 and "El MASE por defecto" in V,
            "la métrica por defecto es el MASE en los dos sitios")
    A.check("G", "Naïve estacional si hay estación, naïve si no" in m12
            and "Naïve estacional si hay estación; naïve si no" in V,
            "la referencia: naïve estacional si hay estación, naïve si no, en los dos sitios")
    A.check("G", "solo si la serie está lejos del cero" in m12 and "solo si la serie está lejos del cero" in V,
            "el MAPE solo lejos del cero, en los dos sitios")
    A.check("G", "al 80 % y al 95 %" in V, "la cobertura se pide a los dos niveles")
    A.check("G", "si el modelo no le gana, hay que decirlo" in V.lower() or "Si el modelo no le gana" in m12,
            "si el modelo no le gana a la referencia, se dice")


def frente_conjunta(A: Auditoria, V: str, mod) -> None:
    """H · La opción conjunta con Estadística Espacial (D11, D12, P3)."""
    print("\n=== H · Conjunta ===")
    cj = re.sub(r"\s+", " ", mod(T_CONJUNTA))
    t = texto_visible(cj)
    A.check("H", bool(cj), "la guía tiene el módulo de la opción conjunta")
    A.check("H", "única" in t and "autoplagio" in t and "autorizada por escrito" in t,
            "D11 · la autorización escrita: la única excepción, y fuera de ella es autoplagio")
    A.check("H", "no hay parejas mixtas" in t and "los dos cursan las dos" in t,
            "D11 · solo quien curse las dos materias; sin parejas mixtas")
    pre = D.HITO["preregistro"]["fecha"]
    A.check("H", "hasta el preregistro" in t and f"{frase(pre)} a las {D.HORA_ENTREGA}" in t,
            "D11 · se puede pasar al proyecto simple hasta el preregistro, con su fecha")
    lista = re.search(r'<ol type="a">(.*?)</ol>', cj, re.S)
    opciones = re.findall(r"<li>", lista.group(1)) if lista else []
    A.check("H", len(opciones) == len(D.PREGUNTAS_CONJUNTAS) == 2, "P3 · solo dos preguntas propuestas: (a) y (b)",
            f"({len(opciones)})")
    A.check("H", "kriging" not in texto_visible(lista.group(1) if lista else "")
            and "ni del kriging" in t, "P3 · el kriging no es una opción, y la guía dice que no")
    A.check("H", "al menos $h$" in cj and "usa el futuro de los vecinos" in t,
            "la (b) exige un rezago temporal de al menos h, y explica por qué")
    A.check("H", f"el <strong>{D.PROYECTO_DEL_CORTE} %</strong> del Corte III" in cj and "lo mismo en las dos" in t,
            f"P3 · el proyecto pesa lo mismo en las dos materias: el {D.PROYECTO_DEL_CORTE} %")
    A.check("H", f"<code>{D.NOMBRE_REPO_CONJUNTO}</code>" in cj and "la misma release" in t
            and f"<code>{D.NOMBRE_REPO_CONJUNTO}</code>" in mod(T_REPOSITORIO),
            "un repositorio con su nombre y la misma release para las dos materias")
    A.check("H", f"{D.PREGUNTAS_POR_MATERIA} preguntas de cada materia" in t and "por separado" in t,
            "dos topes: al menos tres preguntas por materia, y el tope de cada una por separado")
    A.check("H", f"{D.PAGINAS_INFORME_CONJUNTO} páginas" in t and f"{D.MINUTOS_EXPOSICION_CONJUNTA} minutos" in t
            and f"{D.MINUTOS_PREGUNTAS_CONJUNTA} de preguntas" in t,
            "el tamaño de la conjunta: páginas y minutos")
    A.check("H", "cae la nota de esa materia y no la de la otra" in t, "si falta una parte, cae solo esa nota")
    A.check("H", "La guía de Espacial las enlaza" in t, "D12 · las reglas viven aquí y la guía de Espacial las enlaza")
    A.check("H", "el módulo 8 dice cómo" in texto_visible(mod(T_COMO)) and "(módulo 8)" in texto_visible(mod(T_FICHA)),
            "el módulo 1 y la ficha remiten al módulo 8")


def frente_r(A: Auditoria, M: str) -> None:
    bloques = [_html.unescape(b) for b in re.findall(r'<code class="language-r">(.*?)</code>', M, re.S)]
    A.check("E", len(bloques) >= 2, "la guía trae sus bloques de R", f"({len(bloques)})")
    entorno = dict(os.environ, LANG="en_US.UTF-8", LC_ALL="en_US.UTF-8")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        (tmp / "datos").mkdir()
        escribe_serie(tmp / "datos" / "serie.csv")
        # Los bloques van en orden y cada uno usa lo que dejó el anterior, como en el informe.
        for k in range(1, len(bloques) + 1):
            (tmp / f"bloque{k}.R").write_text(
                "suppressPackageStartupMessages({\n" + "\n".join(bloques[:k]) + "\n})\n", encoding="utf-8")
            r = subprocess.run(["Rscript", "--vanilla", f"bloque{k}.R"], cwd=tmp,
                               capture_output=True, text=True, env=entorno)
            primera = bloques[k - 1].strip().splitlines()[0][:60]
            A.check("E", r.returncode == 0, f"el bloque de R {k} corre («{primera}»)",
                    (r.stderr.strip().splitlines() or [""])[-1][:160])

    A.check("E", RMD_PUBLICADO.exists() and RMD_PUBLICADO.read_bytes() == RMD_FUENTE.read_bytes(),
            "la plantilla .Rmd publicada es idéntica a la de la fuente")
    rmd = RMD_PRUEBA.read_text(encoding="utf-8")
    # En la llamada, no en un comentario: «(fitdf)» en el comentario no descuenta nada.
    A.check("E", bool(re.search(r"^[^#\n]*Box\.test\(.*fitdf\s*=", rmd, re.M)),
            "la plantilla pone los grados de libertad del Ljung–Box (fitdf en Box.test)")
    A.check("E", "length(coef(" not in re.sub(r"#.*", "", rmd) and "arimaorder(" in rmd,
            "la plantilla cuenta solo los parámetros ARMA para fitdf, no la deriva (resistencia, 21 oct)")
    linea_dm = next((l for l in rmd.splitlines() if "dm.test(" in l and not l.lstrip().startswith("#")), "")
    A.check("E", "power = 1" in linea_dm, "la plantilla contrasta con la pérdida de su métrica: MASE, power = 1")
    A.check("E", "initial = T0 - 1" in rmd, "la plantilla usa el mismo primer origen que la guía")
    for con_serie in (False, True):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            shutil.copyfile(RMD_PRUEBA, tmp / "plantilla.Rmd")
            if con_serie:
                (tmp / "datos").mkdir()
                escribe_serie(tmp / "datos" / "serie.csv")
            # En el idioma C: así R no sabe español y la fecha tiene que salir igual.
            r = subprocess.run(["Rscript", "--vanilla", "-e", "rmarkdown::render('plantilla.Rmd', quiet = TRUE)"],
                               cwd=tmp, capture_output=True, text=True, env=dict(os.environ, LC_ALL="C", LANG="C"))
            salida = tmp / "plantilla.html"
            cual = "con una serie" if con_serie else "sin serie"
            A.check("E", r.returncode == 0 and salida.exists(), f"la plantilla .Rmd se renderiza {cual}",
                    (r.stderr.strip().splitlines() or [""])[-1][:160])
            if not con_serie:
                A.check("E", not (tmp / "datos").exists(), "renderizar sin serie no escribe nada en datos/")
            if salida.exists():
                t = re.sub(r"\s+", " ", salida.read_text(encoding="utf-8", errors="replace"))
                aviso = "este informe usa una serie SIMULADA" in t
                A.check("E", aviso != con_serie, f"{cual}, el aviso de la serie simulada {'no ' if con_serie else ''}sale")
                A.check("E", "<U+" not in t, f"{cual}, ningún carácter sale como <U+…>")
                A.check("E", bool(re.search(r"\d{1,2} de (" + "|".join(MESES) + r") de \d{4}", t)),
                        f"{cual}, la fecha sale en español aunque R corra en otro idioma")
                A.check("E", not re.search(r"`r\s", t) and re.search(r"orígenes, el MASE del candidato es \d", t),
                        f"{cual}, las cifras en línea se evaluaron")
                for seccion in ("El protocolo, preregistrado y aplicado", "La evaluación por origen móvil",
                                "Los intervalos", "Lo exploratorio", "Declaración de uso de IA"):
                    A.check("E", seccion in t, f"{cual}, el informe renderizado trae «{seccion}»")
                A.check("E", re.search(r"referencia\s+80", t) and re.search(r"candidato\s+95", t),
                        f"{cual}, la cobertura sale a los dos niveles para los dos métodos")


def escribe_serie(ruta: pathlib.Path) -> None:
    """Una serie mensual de prueba, con tendencia y estación, sin ruido aleatorio."""
    filas = ["fecha,valor"]
    for k in range(132):
        anio, mes = 2012 + k // 12, k % 12 + 1
        v = 200 + 0.8 * k + 15 * [0, 2, 5, 8, 6, 3, -1, -4, -7, -5, -3, -1][mes - 1] / 8 + (k * 37 % 11) / 3
        filas.append(f"{anio}-{mes:02d}-01,{v:.2f}")
    ruta.write_text("\n".join(filas) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
