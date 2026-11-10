#!/usr/bin/env python3
"""
audita_citas.py — ninguna cita de memoria

Material de Series de Tiempo 2026-II (20948).

El material ya tenía una norma dura para las cifras: ninguna se escribe a mano,
todas salen de R y un verificador lo comprueba. Para las fuentes no había nada:
se podía escribir «(Cleveland et al., 1990)» sin haber abierto el artículo, y
nadie lo habría notado. Este guion es el equivalente para las citas.

La pieza que lo sostiene es F05: cada afirmación contrastada guarda una cita
LITERAL del pasaje leído, y el auditor la busca en el texto de la fuente
(extraído por `extrae_fuente.py` a una caché local). Una cita inventada, o un
localizador que no corresponde, no pasa.

Qué comprueba, por capítulo:

  F01  toda clave citada (`data-ref`) existe en bibliografia/referencias.json
  F02  citas, listas de fuentes y pie son exactamente lo que escribiría
       genera_referencias.py (nadie los tecleó ni quedaron desfasados)
  F03  cada `data-afirma` del HTML tiene su entrada en contraste/capN.yml y al
       revés; ninguna cita cuelga fuera de una afirmación; una cita visible
       exige veredicto `respaldada` o `con-matiz` y coincide en clave y
       localizador con una fuente de la entrada
  F04  esquema: campos obligatorios, enumerados, identificadores únicos, y
       localizadores del vocabulario cerrado de la norma común
  F05  la cita literal está en el texto de la fuente, en ese localizador
  F06  el ejemplar leído es el que está en Zotero (sha256)
  F07  se cita la edición que se leyó: la portada está comprobada, el año
       coincide y la página impresa es la que lleva esa página del PDF
  F08  quien verifica no es quien redactó
  F09  la prosa no cambió desde que se contrastó (huella del texto)
  F10  --red: los DOI existen en Crossref con el mismo título y año, y los
       enlaces externos responden
  F11  cita ≤ 25 palabras; tope de palabras citadas por obra
  F12  capítulos 3–6: la afirmación está en las fuentes de ensamblado/capN/
  A01  aviso, no falla: apellidos de la biblioteca en la prosa sin <cite>

Uso:  python3 precalculo/audita_citas.py                # los 6 capítulos
      python3 precalculo/audita_citas.py --red          # además, la red
      python3 precalculo/audita_citas.py --cierre       # falla si queda algo
                                                        # pendiente o por reverificar
      python3 precalculo/audita_citas.py --sin-cache    # en un clon sin las
                                                        # fuentes: F05 informa, no falla
      python3 precalculo/audita_citas.py --huella c1-m7-01
                                                        # la huella actual de esa afirmación
      python3 precalculo/audita_citas.py --uso          # escribe uso_fuentes.json, el
                                                        # contrato curso → vault

Devuelve 1 si algo falla.
"""
from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import hashlib
import html.parser
import json
import pathlib
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import genera_referencias  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent

TIPOS = {"definicion", "resultado", "regla", "historica", "atribucion", "dato"}
VEREDICTOS = {"respaldada", "con-matiz", "discrepa", "propia", "pendiente", "por-reverificar"}
CITABLES = {"respaldada", "con-matiz"}
ABIERTOS = {"pendiente", "por-reverificar", "discrepa"}
# Clases de evidencia. PDF, WEB y DOC las comprueba este guion contra la caché;
# MAN (un libro en papel, con página) y REPO (derivación o cifra del propio
# repositorio) no las ejecuta ningún guion y se cuentan aparte.
CLASES_CON_TEXTO = {"PDF", "WEB", "DOC"}
CLASES = CLASES_CON_TEXTO | {"MAN", "REPO"}
MAX_PALABRAS_CITA = 25
TOPE_PALABRAS_OBRA = 400
RE_ID = re.compile(r"^c(\d+)-m(\d+)-(\d{2,})$")
# Vocabulario cerrado de localizadores, el de la norma común de los cuatro cursos
# (Vault/Estandar/Capa de fuentes.md). Varios se separan con «; »; los rangos de
# página llevan raya corta. La edición nunca va aquí: va en la clave de la obra.
_NUM = r"\d+(?:\.\d+)*[a-z]?"
RE_LOCALIZADOR = re.compile(
    rf"(?:cap\. \d+|§{_NUM}|ejemplo {_NUM}|ejercicio {_NUM}|problema {_NUM}|ec\. {_NUM}"
    rf"|tabla {_NUM}|fig\. {_NUM}|p\. \d+|pp\. \d+–\d+|ap\. [A-Z0-9]+)"
)


def localizador_valido(loc: str) -> bool:
    partes = str(loc).split("; ")
    return bool(loc) and all(RE_LOCALIZADOR.fullmatch(p) for p in partes)
VACIOS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
          "source", "track", "wbr"}
AGENTE = "auditor-bibliografico/0.1"
CURSO = 20948


@dataclasses.dataclass
class Hallazgo:
    codigo: str
    donde: str
    que: str
    aviso: bool = False

    def __str__(self) -> str:
        marca = "AVISO " if self.aviso else "FALLA "
        return f"{marca} [{self.codigo}] {self.donde}: {self.que}"


# --------------------------------------------------------------------------- #
# Texto
# --------------------------------------------------------------------------- #
def normaliza(texto: str) -> str:
    """Forma canónica para comparar una cita con el texto de la fuente."""
    t = unicodedata.normalize("NFKC", texto)
    t = re.sub(r"[‐‑‒–—−]", "-", t)
    t = re.sub(r"[“”„«»]", '"', t)
    t = re.sub(r"[‘’‚`´]", "'", t)
    t = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "", t)      # palabra par-\ntida
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def huella(texto: str) -> str:
    return hashlib.sha256(normaliza(texto).encode("utf-8")).hexdigest()[:16]


# --------------------------------------------------------------------------- #
# Lectura del HTML
# --------------------------------------------------------------------------- #
@dataclasses.dataclass
class Cita:
    clave: str
    loc: str
    afirma: str | None
    linea: int


@dataclasses.dataclass
class Afirmacion:
    id: str
    linea: int
    texto: str = ""


class Lector(html.parser.HTMLParser):
    """Recoge las afirmaciones (`data-afirma`), sus textos y todas las citas.

    El texto de una afirmación excluye lo que hay dentro de sus <cite>: eso lo
    escribe el generador y puede cambiar si en Zotero se corrige un apellido,
    sin que la prosa contrastada haya cambiado.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.pila: list[tuple[str, str | None, bool]] = []   # (etiqueta, id afirma, es cita)
        self.afirmaciones: dict[str, Afirmacion] = {}
        self.citas: list[Cita] = []
        self.problemas: list[tuple[int, str]] = []
        self.prosa: list[tuple[int, str]] = []               # texto fuera de afirmaciones

    def _afirma_actual(self) -> str | None:
        return next((a for _, a, _ in reversed(self.pila) if a), None)

    def _en_cita(self) -> bool:
        return any(c for _, _, c in self.pila)

    def handle_starttag(self, etiqueta, atributos):
        a = dict(atributos)
        linea = self.getpos()[0]
        id_afirma = a.get("data-afirma")
        es_cita = etiqueta == "cite" and "cita" in (a.get("class") or "").split()
        if id_afirma:
            if self._afirma_actual():
                self.problemas.append((linea, f"`data-afirma=\"{id_afirma}\"` anidada dentro de otra"))
            if id_afirma in self.afirmaciones:
                self.problemas.append((linea, f"`data-afirma=\"{id_afirma}\"` repetida"))
            self.afirmaciones[id_afirma] = Afirmacion(id_afirma, linea)
        if es_cita:
            self.citas.append(Cita(a.get("data-ref", ""), a.get("data-loc", ""),
                                   id_afirma or self._afirma_actual(), linea))
        if etiqueta not in VACIOS:
            self.pila.append((etiqueta, id_afirma, es_cita))

    def handle_endtag(self, etiqueta):
        for i in range(len(self.pila) - 1, -1, -1):
            if self.pila[i][0] == etiqueta:
                del self.pila[i:]
                return

    def handle_data(self, dato):
        if self.pila and self.pila[-1][0] in ("script", "style"):
            return
        actual = self._afirma_actual()
        if actual and not self._en_cita():
            self.afirmaciones[actual].texto += dato
        elif not actual and not self._en_cita() and dato.strip():
            self.prosa.append((self.getpos()[0], dato))


def lee_html(texto: str) -> Lector:
    lector = Lector()
    lector.feed(texto)
    lector.close()
    return lector


# --------------------------------------------------------------------------- #
# Biblioteca
# --------------------------------------------------------------------------- #
@dataclasses.dataclass
class Biblioteca:
    dir: pathlib.Path
    referencias: dict[str, dict]
    candado: dict[str, dict]
    ejemplares: dict[str, dict]
    instantaneas: dict[str, dict]

    @classmethod
    def carga(cls, directorio: pathlib.Path) -> "Biblioteca":
        def y(nombre: str) -> dict:
            ruta = directorio / nombre
            return (yaml.safe_load(ruta.read_text("utf-8")) or {}) if ruta.exists() else {}
        referencias = json.loads((directorio / "referencias.json").read_text("utf-8"))
        candado = json.loads((directorio / "zotero.lock.json").read_text("utf-8"))["obras"]
        return cls(directorio, {r["id"]: r for r in referencias}, candado,
                   y("ejemplares.yml"), y("instantaneas.yml"))

    def anio(self, clave: str) -> str:
        partes = (self.referencias[clave].get("issued") or {}).get("date-parts") or [[None]]
        return str(partes[0][0]) if partes[0] and partes[0][0] else ""

    def texto_pdf(self, clave: str, pagina: int) -> str | None:
        """Texto de la página y de la siguiente (una cita puede cruzar el salto)."""
        base = self.dir / "_local" / "texto" / clave
        primera = base / f"p{pagina:04d}.txt"
        if not primera.is_file():
            return None
        siguiente = base / f"p{pagina + 1:04d}.txt"
        cola = siguiente.read_text("utf-8") if siguiente.is_file() else ""
        return primera.read_text("utf-8") + "\n" + cola

    def texto_instantanea(self, clave: str, nombre: str) -> tuple[str | None, bool]:
        """(texto, la huella coincide con instantaneas.yml)."""
        ruta = self.dir / "_local" / "web" / clave / f"{nombre}.txt"
        if not ruta.is_file():
            return None, False
        crudo = ruta.read_bytes()
        esperado = ((self.instantaneas.get(clave) or {}).get(nombre) or {}).get("sha256")
        return crudo.decode("utf-8", "replace"), hashlib.sha256(crudo).hexdigest() == esperado


# --------------------------------------------------------------------------- #
# Comprobaciones
# --------------------------------------------------------------------------- #
def f04_esquema(registro: dict, nombre: str, capitulo: int) -> list[Hallazgo]:
    h: list[Hallazgo] = []
    vistos: set[str] = set()
    for e in registro.get("afirmaciones") or []:
        ident = str(e.get("id", "¿sin id?"))
        donde = f"{nombre} · {ident}"
        m = RE_ID.match(ident)
        if not m:
            h.append(Hallazgo("F04", donde, "el id no tiene la forma c<cap>-m<mod>-<nn>"))
        elif int(m.group(1)) != capitulo:
            h.append(Hallazgo("F04", donde, f"el id es de otro capítulo (este es el {capitulo})"))
        if ident in vistos:
            h.append(Hallazgo("F04", donde, "id repetido en el registro"))
        vistos.add(ident)
        for campo in ("tipo", "afirmacion", "hash_texto", "veredicto", "redactado_por", "fecha"):
            if e.get(campo) in (None, ""):
                h.append(Hallazgo("F04", donde, f"falta `{campo}`"))
        if e.get("tipo") not in TIPOS:
            h.append(Hallazgo("F04", donde, f"`tipo` desconocido: {e.get('tipo')!r}"))
        veredicto = e.get("veredicto")
        if veredicto not in VEREDICTOS:
            h.append(Hallazgo("F04", donde, f"`veredicto` desconocido: {veredicto!r}"))
        if not isinstance(e.get("fecha"), dt.date):
            h.append(Hallazgo("F04", donde, "`fecha` no es una fecha AAAA-MM-DD"))
        fuentes = e.get("fuentes") or []
        if veredicto in CITABLES and not fuentes:
            h.append(Hallazgo("F04", donde, f"veredicto `{veredicto}` sin ninguna fuente"))
        if veredicto in ("pendiente", "discrepa") and not e.get("motivo"):
            h.append(Hallazgo("F04", donde, f"veredicto `{veredicto}` sin `motivo`"))
        for n, f in enumerate(fuentes, start=1):
            aqui = f"{donde} · fuente {n}"
            for campo in ("clave", "loc", "clase", "cita"):
                if not f.get(campo):
                    h.append(Hallazgo("F04", aqui, f"falta `{campo}`"))
            if f.get("loc") and not localizador_valido(f["loc"]):
                h.append(Hallazgo("F04", aqui, f"el localizador «{f['loc']}» no usa el vocabulario cerrado "
                                               "(§3.4 · cap. 3 · p. 15 · pp. 15–17 · tabla 3.1 · fig. 3.1 · ec. 3.3 · "
                                               "ejemplo 3.2 · ejercicio 3.12 · ap. A; varios con «; »)"))
            clase = f.get("clase")
            if clase not in CLASES:
                h.append(Hallazgo("F04", aqui, f"`clase` desconocida: {clase!r}"))
            if clase == "PDF" and not isinstance(f.get("pagina_pdf"), int):
                h.append(Hallazgo("F04", aqui, "clase PDF sin `pagina_pdf` (entero)"))
            if clase in ("WEB", "DOC") and not f.get("instantanea"):
                h.append(Hallazgo("F04", aqui, f"clase {clase} sin `instantanea`"))
    return h


def seccion_de(texto: str, loc: str) -> tuple[str, str | None]:
    """Si el localizador nombra una sección («§3.6»), acota el texto a ella.

    Devuelve (texto acotado, sección buscada y no hallada). Una instantánea de
    FPP3 es un capítulo entero: sin esto, «§3.6» y «§4.3» serían indistinguibles
    y el localizador no estaría comprobado, solo el capítulo.
    """
    m = re.search(r"§\s*(\d+(?:\.\d+)*)", loc or "")
    if not m:
        return texto, None
    numero = m.group(1)
    lineas = texto.splitlines()
    encabezado = re.compile(r"^(\d+(?:\.\d+)*)\s{1,4}\S")
    inicio = next((i for i, l in enumerate(lineas)
                   if (e := encabezado.match(l)) and e.group(1) == numero), None)
    if inicio is None:
        return "", numero
    fin = next((i for i in range(inicio + 1, len(lineas))
                if (e := encabezado.match(lineas[i])) and not e.group(1).startswith(numero + ".")
                and re.match(r"^\d+(?:\.\d+)*\s{1,4}[A-ZÁÉÍÓÚ¿]", lineas[i])), len(lineas))
    return "\n".join(lineas[inicio:fin]), None


def f05_cita_literal(bib: Biblioteca, f: dict, donde: str, sin_cache: bool,
                     cuenta: dict) -> list[Hallazgo]:
    clave, clase, cita = f.get("clave", ""), f.get("clase"), f.get("cita") or ""
    if clase not in CLASES_CON_TEXTO:
        cuenta["sin_guion"] += 1
        return []
    if clase == "PDF":
        pagina = f.get("pagina_pdf")
        texto = bib.texto_pdf(clave, pagina) if isinstance(pagina, int) else None
        sitio = f"p. {pagina} del PDF"
    else:
        texto, coincide = bib.texto_instantanea(clave, str(f.get("instantanea")))
        sitio = f"instantánea «{f.get('instantanea')}»"
        if texto is not None and not coincide:
            return [Hallazgo("F05", donde, f"la {sitio} no es la registrada en instantaneas.yml (sha256)")]
        if texto is not None:
            texto, falta = seccion_de(texto, str(f.get("loc") or ""))
            if falta:
                return [Hallazgo("F05", donde, f"la sección §{falta} no está en la {sitio} de «{clave}»")]
            sitio = f"{f.get('loc')} de la {sitio}"
    if texto is None:
        cuenta["sin_cache"] += 1
        if sin_cache:
            return []
        return [Hallazgo("F05", donde, f"no está en la caché la {sitio} de «{clave}»: "
                                      "no comprobable aquí (extrae_fuente.py, o --sin-cache)")]
    if normaliza(cita) not in normaliza(texto):
        return [Hallazgo("F05", donde, f"la cita literal NO está en la {sitio} de «{clave}»")]
    cuenta["comprobadas"] += 1
    return []


def f06_f07_ejemplar(bib: Biblioteca, f: dict, donde: str) -> list[Hallazgo]:
    if f.get("clase") != "PDF":
        return []
    clave = f.get("clave", "")
    h: list[Hallazgo] = []
    ficha = bib.ejemplares.get(clave)
    adjuntos = (bib.candado.get(clave) or {}).get("adjuntos") or []
    if not ficha:
        return [Hallazgo("F06", donde, f"«{clave}» no tiene ficha en ejemplares.yml")]
    # El texto de la caché tiene que haber salido del ejemplar registrado, y si
    # la obra tiene PDF adjunto en Zotero, ese ejemplar tiene que ser ese PDF.
    origen = bib.dir / "_local" / "texto" / clave / "_origen.json"
    huellas = []
    if adjuntos:
        huellas.append(("el PDF adjunto en Zotero", adjuntos[0].get("sha256")))
    if origen.is_file():
        huellas.append(("el PDF del que se extrajo el texto", json.loads(origen.read_text("utf-8")).get("sha256")))
    if not huellas:
        h.append(Hallazgo("F06", donde, f"no consta de qué PDF salió el texto de «{clave}»"))
    for cual, huella_pdf in huellas:
        if ficha.get("sha256") != huella_pdf:
            h.append(Hallazgo("F06", donde, f"el ejemplar de «{clave}» no es {cual} (sha256)"))
    edicion = str(ficha.get("edicion_comprobada") or "")
    if not edicion:
        h.append(Hallazgo("F07", donde, f"la portada de «{clave}» no está comprobada (`edicion_comprobada`)"))
    elif bib.anio(clave) and bib.anio(clave) not in edicion:
        h.append(Hallazgo("F07", donde, f"la portada dice «{edicion}» y la obra citada es de {bib.anio(clave)}: "
                                       "se leyó una edición y se cita otra"))
    # La página impresa que ve el lector tiene que ser la de esa página del PDF.
    # Se comprueba en el propio texto: el número aparece en el encabezado o en
    # el pie de la página. El `desfase` del ejemplar (página del PDF − página
    # impresa) solo sirve de respaldo, porque no siempre es constante: un PDF
    # sin las páginas en blanco de fin de capítulo lo va cambiando.
    m = re.search(r"\bpp?\.\s*(\d+)", str(f.get("loc") or ""))
    pagina = f.get("pagina_pdf")
    if m and isinstance(pagina, int):
        impresa = m.group(1)
        hoja = bib.dir / "_local" / "texto" / clave / f"p{pagina:04d}.txt"
        lineas = [l for l in hoja.read_text("utf-8").splitlines() if l.strip()] if hoja.is_file() else []
        bordes = " ".join(lineas[:1] + lineas[-1:])
        en_el_borde = re.search(rf"(?<!\d){impresa}(?!\d)", bordes) is not None
        desfase = ficha.get("desfase")
        por_desfase = isinstance(desfase, int) and int(impresa) + desfase == pagina
        if lineas and not en_el_borde and not por_desfase:
            h.append(Hallazgo("F07", donde, f"la página {pagina} del PDF de «{clave}» no lleva el número {impresa} "
                                            "en el encabezado ni en el pie: el localizador no es de esa página"))
    return h


def audita_capitulo(bib: Biblioteca, ruta_html: pathlib.Path, registro: dict, nombre: str,
                    capitulo: int, sin_cache: bool, cuenta: dict,
                    dir_ensamblado: pathlib.Path | None) -> list[Hallazgo]:
    h: list[Hallazgo] = []
    texto = ruta_html.read_text("utf-8")
    lector = lee_html(texto)
    entradas = {str(e.get("id")): e for e in registro.get("afirmaciones") or []}

    for linea, que in lector.problemas:
        h.append(Hallazgo("F03", f"{ruta_html.name}:{linea}", que))

    # F01 — claves
    for c in lector.citas:
        if c.clave not in bib.referencias:
            h.append(Hallazgo("F01", f"{ruta_html.name}:{c.linea}",
                              f"la clave «{c.clave}» no está en referencias.json"))
    for ident, e in entradas.items():
        for f in e.get("fuentes") or []:
            if f.get("clave") and f["clave"] not in bib.referencias:
                h.append(Hallazgo("F01", f"{nombre} · {ident}",
                                  f"la clave «{f['clave']}» no está en referencias.json"))

    for c in lector.citas:
        if c.loc and not localizador_valido(c.loc):
            h.append(Hallazgo("F04", f"{ruta_html.name}:{c.linea}",
                              f"`data-loc=\"{c.loc}\"` no usa el vocabulario cerrado de localizadores"))

    # F02 — regenerado
    if not any(x.codigo == "F01" for x in h):
        genera_referencias.BIB = bib.dir
        try:
            if genera_referencias.genera(texto, bib.referencias, bib.candado) != texto:
                h.append(Hallazgo("F02", ruta_html.name,
                                  "citas, listas o pie no coinciden con lo que escribe genera_referencias.py"))
        except genera_referencias.ErrorDeCita as e:
            h.append(Hallazgo("F02", ruta_html.name, str(e)))

    # F04 — esquema
    h += f04_esquema(registro, nombre, capitulo)

    # F03 — correspondencia
    for ident, a in lector.afirmaciones.items():
        if ident not in entradas:
            h.append(Hallazgo("F03", f"{ruta_html.name}:{a.linea}",
                              f"`data-afirma=\"{ident}\"` no tiene entrada en {nombre}"))
    for ident in entradas:
        if ident not in lector.afirmaciones:
            h.append(Hallazgo("F03", f"{nombre} · {ident}", "no hay ningún `data-afirma` con ese id en el HTML"))
    for c in lector.citas:
        donde = f"{ruta_html.name}:{c.linea}"
        if not c.afirma:
            h.append(Hallazgo("F03", donde, f"la cita de «{c.clave}» no está dentro de ninguna afirmación (`data-afirma`)"))
            continue
        e = entradas.get(c.afirma)
        if not e:
            continue
        if e.get("veredicto") not in CITABLES:
            h.append(Hallazgo("F03", donde, f"cita visible sobre {c.afirma}, cuyo veredicto es `{e.get('veredicto')}`"))
        if not any(f.get("clave") == c.clave and str(f.get("loc")) == c.loc for f in e.get("fuentes") or []):
            h.append(Hallazgo("F03", donde, f"la cita ({c.clave}, «{c.loc}») no coincide con ninguna fuente de {c.afirma}"))
    for ident, e in entradas.items():
        if e.get("veredicto") in CITABLES and ident in lector.afirmaciones \
                and not any(c.afirma == ident for c in lector.citas):
            h.append(Hallazgo("F03", f"{nombre} · {ident}", "está respaldada pero no lleva ninguna cita visible", aviso=True))

    # F05 a F09, F11 — por entrada
    for ident, e in entradas.items():
        donde = f"{nombre} · {ident}"
        veredicto = e.get("veredicto")
        cuenta["veredictos"][veredicto] = cuenta["veredictos"].get(veredicto, 0) + 1
        if veredicto in CITABLES:
            if not e.get("verificado_por"):
                h.append(Hallazgo("F08", donde, "falta `verificado_por`"))
            elif normaliza(str(e["verificado_por"])).lower() == normaliza(str(e.get("redactado_por"))).lower():
                h.append(Hallazgo("F08", donde, "quien verifica es quien redactó"))
        a = lector.afirmaciones.get(ident)
        if a and e.get("hash_texto") and veredicto != "por-reverificar" and huella(a.texto) != e["hash_texto"]:
            h.append(Hallazgo("F09", donde, f"la prosa cambió desde que se contrastó (huella actual {huella(a.texto)}): "
                                            "pasa a `por-reverificar`"))
        for n, f in enumerate(e.get("fuentes") or [], start=1):
            aqui = f"{donde} · fuente {n}"
            if veredicto in CITABLES:
                h += f05_cita_literal(bib, f, aqui, sin_cache, cuenta)
                h += f06_f07_ejemplar(bib, f, aqui)
            palabras = len(str(f.get("cita") or "").split())
            if palabras > MAX_PALABRAS_CITA:
                h.append(Hallazgo("F11", aqui, f"la cita tiene {palabras} palabras (máximo {MAX_PALABRAS_CITA})"))
            cuenta["palabras"][f.get("clave")] = cuenta["palabras"].get(f.get("clave"), 0) + palabras

    # F12 — capítulos ensamblados
    if capitulo >= 3 and dir_ensamblado is not None and lector.afirmaciones:
        fuentes = "".join(p.read_text("utf-8", "replace")
                          for p in sorted((dir_ensamblado / f"cap{capitulo}").glob("*"))
                          if p.suffix in (".html", ".js"))
        for ident in lector.afirmaciones:
            if f'data-afirma="{ident}"' not in fuentes:
                h.append(Hallazgo("F12", f"{ruta_html.name} · {ident}",
                                  f"no está en ensamblado/cap{capitulo}/: se perderá al reensamblar"))

    # A01 — apellidos sin cita
    apellidos = {a.get("family") for r in bib.referencias.values() for a in r.get("author") or []}
    apellidos = {a for a in apellidos if a and len(a) > 3}
    if apellidos:
        patron = re.compile(r"\b(" + "|".join(sorted(map(re.escape, apellidos))) + r")\b")
        sueltos: dict[str, int] = {}
        for linea, dato in lector.prosa:
            for m in patron.finditer(dato):
                sueltos.setdefault(m.group(1), linea)
        cuenta["a01"][ruta_html.name] = sueltos
    return h


def f10_red(bib: Biblioteca, htmls: list[pathlib.Path]) -> list[Hallazgo]:
    h: list[Hallazgo] = []

    def abre(url: str) -> tuple[int, bytes]:
        pedido = urllib.request.Request(url, headers={"User-Agent": AGENTE})
        try:
            with urllib.request.urlopen(pedido, timeout=25) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            return e.code, b""
        except (urllib.error.URLError, OSError):
            return 0, b""

    for clave, r in sorted(bib.referencias.items()):
        doi = r.get("DOI")
        if not doi:
            continue
        estado, cuerpo = abre("https://api.crossref.org/works/" + urllib.parse.quote(doi))
        if estado != 200:
            h.append(Hallazgo("F10", clave, f"Crossref no conoce el DOI {doi} (HTTP {estado})"))
            continue
        m = json.loads(cuerpo)["message"]
        titulo = normaliza(" ".join(m.get("title") or [])).lower()
        propio = normaliza(re.sub(r"<[^>]+>", "", r.get("title", ""))).lower()
        corto = re.split(r"[:.?]", propio)[0].strip()
        if corto and corto not in titulo:
            h.append(Hallazgo("F10", clave, f"el título no coincide con Crossref: «{' '.join(m.get('title') or [])}»"))
        anios = {str(p[0][0]) for p in (
            (m.get(k) or {}).get("date-parts") for k in ("published-print", "published-online", "published", "issued")
        ) if p and p[0] and p[0][0]}
        if bib.anio(clave) and anios and bib.anio(clave) not in anios:
            h.append(Hallazgo("F10", clave, f"el año {bib.anio(clave)} no coincide con Crossref ({', '.join(sorted(anios))})"))

    vistos: set[str] = set()
    for ruta in htmls:
        for url in re.findall(r'href="(https?://[^"]+)"', ruta.read_text("utf-8")):
            if url in vistos or re.search(r"fonts\.|cdnjs\.|cdn\.jsdelivr|unpkg\.com", url):
                continue
            vistos.add(url)
            estado, _ = abre(url)
            if estado == 0 or estado >= 400:
                h.append(Hallazgo("F10", ruta.name, f"el enlace {url} respondió {estado or 'sin conexión'}",
                                  aviso=estado in (401, 403, 429)))
    return h


# --------------------------------------------------------------------------- #
def audita(dir_bib: pathlib.Path, dir_sitio: pathlib.Path, *, red: bool = False,
           sin_cache: bool = False, dir_ensamblado: pathlib.Path | None = None
           ) -> tuple[list[Hallazgo], dict]:
    bib = Biblioteca.carga(dir_bib)
    cuenta = {"veredictos": {}, "comprobadas": 0, "sin_cache": 0, "sin_guion": 0,
              "palabras": {}, "a01": {}, "capitulos": 0, "citas": 0}
    h: list[Hallazgo] = []
    htmls: list[pathlib.Path] = []
    registros = {int(re.search(r"cap(\d+)", p.name).group(1)): p
                 for p in sorted((dir_bib / "contraste").glob("cap*.yml"))}
    for ruta_html in sorted(dir_sitio.glob("capitulo-*.html")):
        capitulo = int(re.search(r"capitulo-(\d+)", ruta_html.name).group(1))
        ruta_registro = registros.get(capitulo)
        registro = (yaml.safe_load(ruta_registro.read_text("utf-8")) or {}) if ruta_registro else {}
        nombre = f"contraste/cap{capitulo}.yml"
        htmls.append(ruta_html)
        cuenta["capitulos"] += 1
        h += audita_capitulo(bib, ruta_html, registro, nombre, capitulo, sin_cache, cuenta, dir_ensamblado)
        cuenta["citas"] += len(lee_html(ruta_html.read_text("utf-8")).citas)
    for clave, palabras in cuenta["palabras"].items():
        if palabras > TOPE_PALABRAS_OBRA:
            h.append(Hallazgo("F11", str(clave), f"{palabras} palabras citadas de una sola obra (tope {TOPE_PALABRAS_OBRA})"))
    if red:
        h += f10_red(bib, htmls)
    return h, cuenta


def uso_de_fuentes(dir_bib: pathlib.Path, dir_sitio: pathlib.Path, curso: int) -> dict:
    """El contrato curso → vault de la norma común: lo único que el vault lee.

    Por cada obra de la biblioteca: su rol, si hay texto leído en el corpus
    local (un PDF o una instantánea web), la edición comprobada en la portada,
    en qué capítulos se usa, cuántas citas visibles tiene y cuántas afirmaciones
    respalda, por veredicto. No lleva fecha por obra ni nada que cambie sin que
    cambie el material: `generado` solo se mueve cuando se mueve lo demás.
    """
    bib = Biblioteca.carga(dir_bib)
    obras = {
        clave: {
            "rol": (bib.candado.get(clave) or {}).get("rol"),
            "ejemplar": clave in bib.ejemplares or clave in bib.instantaneas,
            "edicion_comprobada": (bib.ejemplares.get(clave) or {}).get("edicion_comprobada"),
            "capitulos": set(),
            "citas": 0,
            "afirmaciones": {},
        }
        for clave in sorted(bib.referencias)
    }
    for ruta_html in sorted(dir_sitio.glob("capitulo-*.html")):
        capitulo = int(re.search(r"capitulo-(\d+)", ruta_html.name).group(1))
        for c in lee_html(ruta_html.read_text("utf-8")).citas:
            if c.clave in obras:
                obras[c.clave]["citas"] += 1
                obras[c.clave]["capitulos"].add(capitulo)
    for ruta in sorted((dir_bib / "contraste").glob("cap*.yml")):
        registro = yaml.safe_load(ruta.read_text("utf-8")) or {}
        capitulo = int(re.search(r"cap(\d+)", ruta.name).group(1))
        for e in registro.get("afirmaciones") or []:
            for clave in {f.get("clave") for f in e.get("fuentes") or []}:
                if clave in obras:
                    cuenta = obras[clave]["afirmaciones"]
                    cuenta[e.get("veredicto")] = cuenta.get(e.get("veredicto"), 0) + 1
                    obras[clave]["capitulos"].add(capitulo)
    for o in obras.values():
        o["capitulos"] = sorted(o["capitulos"])
    return {"norma": 1, "curso": curso, "obras": obras}


def escribe_uso(dir_bib: pathlib.Path, dir_sitio: pathlib.Path, curso: int, comprobar: bool) -> int:
    ruta = dir_bib / "uso_fuentes.json"
    nuevo = uso_de_fuentes(dir_bib, dir_sitio, curso)
    viejo = json.loads(ruta.read_text("utf-8")) if ruta.exists() else {}
    igual = {k: v for k, v in viejo.items() if k != "generado"} == nuevo
    if comprobar:
        print("OK     uso_fuentes.json está al día" if igual
              else "FALLA  uso_fuentes.json no está al día: python3 precalculo/audita_citas.py --uso")
        return 0 if igual else 1
    if igual:
        print("OK     uso_fuentes.json: sin cambios")
        return 0
    # `generado` va el primero, como en el ejemplo de la norma
    salida = {"norma": nuevo["norma"], "curso": nuevo["curso"],
              "generado": dt.date.today().isoformat(), "obras": nuevo["obras"]}
    ruta.write_text(json.dumps(salida, ensure_ascii=False, indent=2) + "\n", "utf-8")
    usadas = sum(1 for o in nuevo["obras"].values() if o["citas"] or o["afirmaciones"])
    print(f"OK     uso_fuentes.json: {len(nuevo['obras'])} obras, {usadas} en uso → {ruta.relative_to(dir_bib.parent)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--uso", action="store_true",
                    help="escribe bibliografia/uso_fuentes.json, el contrato curso → vault")
    ap.add_argument("--uso-comprobar", action="store_true",
                    help="sale con 1 si uso_fuentes.json no está al día")
    ap.add_argument("--bib", type=pathlib.Path, default=RAIZ / "bibliografia")
    ap.add_argument("--sitio", type=pathlib.Path, default=RAIZ / "Htmls_Series")
    ap.add_argument("--red", action="store_true", help="comprueba DOI y enlaces externos")
    ap.add_argument("--cierre", action="store_true",
                    help="falla si queda algo pendiente, por reverificar o que discrepa")
    ap.add_argument("--sin-cache", action="store_true",
                    help="F05 informa de lo que no puede comprobar, en vez de fallar")
    ap.add_argument("--avisos", action="store_true", help="lista los apellidos sin cita (A01)")
    ap.add_argument("--huella", metavar="ID", help="imprime la huella actual de una afirmación")
    args = ap.parse_args()

    if args.uso or args.uso_comprobar:
        return escribe_uso(args.bib, args.sitio, CURSO, comprobar=args.uso_comprobar)

    if args.huella:
        for ruta in sorted(args.sitio.glob("capitulo-*.html")):
            a = lee_html(ruta.read_text("utf-8")).afirmaciones.get(args.huella)
            if a:
                print(f"{args.huella}  {huella(a.texto)}  ({ruta.name}:{a.linea})")
                print(f"  texto: {normaliza(a.texto)}")
                return 0
        print(f"FALLA  no hay ninguna `data-afirma=\"{args.huella}\"`")
        return 1

    hallazgos, cuenta = audita(args.bib, args.sitio, red=args.red, sin_cache=args.sin_cache,
                               dir_ensamblado=RAIZ / "ensamblado" if args.bib == RAIZ / "bibliografia" else None)
    fallas = [x for x in hallazgos if not x.aviso]
    for x in hallazgos:
        print(x)

    v = cuenta["veredictos"]
    total = sum(v.values())
    abiertos = sum(v.get(k, 0) for k in ABIERTOS)
    print(f"\n{cuenta['capitulos']} capítulos · {cuenta['citas']} citas visibles · {total} afirmaciones registradas")
    if total:
        print("  " + " · ".join(f"{k}: {v[k]}" for k in sorted(v)))
        print(f"  citas literales comprobadas contra la fuente: {cuenta['comprobadas']}"
              f" · sin caché aquí: {cuenta['sin_cache']} · sin guion (MAN/REPO): {cuenta['sin_guion']}")
    sueltos = sum(len(s) for s in cuenta["a01"].values())
    if sueltos:
        print(f"  [A01] {sueltos} apellidos de la biblioteca aparecen en la prosa sin <cite>"
              + ("" if args.avisos else " (--avisos para verlos)"))
        if args.avisos:
            for archivo, s in cuenta["a01"].items():
                for apellido, linea in sorted(s.items(), key=lambda par: par[1]):
                    print(f"         {archivo}:{linea}  {apellido}")
    if args.cierre and abiertos:
        print(f"FALLA  [cierre] quedan {abiertos} afirmaciones pendientes, por reverificar o que discrepan")
        return 1
    print("OK     auditoría de citas" if not fallas else f"FALLA  {len(fallas)} hallazgos")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())
