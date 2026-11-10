#!/usr/bin/env python3
"""
prueba_audita_citas.py — el auditor de citas, puesto a prueba

Material de Series de Tiempo 2026-II (20948).

Un auditor que nunca ha visto un defecto no demuestra nada al salir en verde.
Este arnés construye en una carpeta temporal un capítulo mínimo, correcto, con
su biblioteca, su caché de texto y su registro de contraste; comprueba que el
auditor lo aprueba; y después le inyecta, uno por uno, los defectos que el
auditor existe para atrapar. Cada inyección debe producir EXACTAMENTE los
códigos esperados: ni se escapa el defecto, ni salta una alarma que no toca.

No depende de Zotero, de los PDF ni de la red: la biblioteca es de juguete.
Sí usa pandoc, porque F02 compara contra lo que escribe genera_referencias.py.

Uso:  python3 precalculo/prueba_audita_citas.py
Devuelve 1 si alguna inyección no se detecta como se esperaba.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import shutil
import sys
import tempfile

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import audita_citas  # noqa: E402
import genera_referencias  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent

PAGINA_5 = """
        3   Suavizado

  La media móvil centrada de orden m elimina por completo un patrón
  estacional de periodo m, porque cada ventana contiene exactamente un
  ciclo completo y sus efectos se compen-
  san entre sí.
"""
PAGINA_WEB = (
    "1 Introducción\n\nEste artículo presenta un método de ajuste por pasos.\n\n"
    "2 El procedimiento\n\nEl ajuste es robusto frente a observaciones atípicas porque "
    "cada iteración reduce el peso de los residuos grandes.\n\n"
    "3 Ejemplos\n\nSe aplica a tres series mensuales.\n"
)
CITA_1 = "elimina por completo un patrón estacional de periodo m, porque cada ventana contiene exactamente un ciclo completo"
CITA_2 = "El ajuste es robusto frente a observaciones atípicas"

HTML_CAP1 = """<!DOCTYPE html>
<html lang="es">
<body>
  <template id="module-1">
    <div>
      <p data-afirma="c1-m1-01">La media móvil centrada de orden m elimina la estacionalidad de periodo m
        <cite class="cita" data-ref="perez2020series" data-loc="p. 3"></cite>.</p>
      <p data-afirma="c1-m1-02">El procedimiento es robusto frente a valores atípicos, como muestran
        <cite class="cita" data-ref="gomez1990metodo" data-loc="§2" data-modo="narrativa"></cite>.</p>
      <p data-afirma="c1-m1-03">Esta normalización se deduce en el propio material.</p>
      <p data-afirma="c1-m1-04">La regla del pulgar de los siete años sigue sin fuente.</p>
      <aside class="fuentes-modulo">
        <!--FUENTES-MODULO:inicio--><!--FUENTES-MODULO:fin-->
      </aside>
    </div>
  </template>
  <template id="module-2">
    <div>
      <!--REFERENCIAS-CAPITULO:inicio--><!--REFERENCIAS-CAPITULO:fin-->
    </div>
  </template>
  <footer>
    <!--PIE-REFERENCIAS:inicio--><!--PIE-REFERENCIAS:fin-->
  </footer>
</body>
</html>
"""
HTML_CAP3 = """<!DOCTYPE html>
<html lang="es">
<body>
  <template id="module-1">
    <div>
      <p data-afirma="c3-m1-01">Este resultado se demuestra en el propio capítulo.</p>
    </div>
  </template>
</body>
</html>
"""


def sha(dato: bytes) -> str:
    return hashlib.sha256(dato).hexdigest()


def construye(base: pathlib.Path) -> None:
    bib, sitio = base / "bibliografia", base / "Htmls_Series"
    (bib / "contraste").mkdir(parents=True)
    (bib / "_local" / "texto" / "perez2020series").mkdir(parents=True)
    (bib / "_local" / "web" / "gomez1990metodo").mkdir(parents=True)
    (base / "ensamblado" / "cap3").mkdir(parents=True)
    sitio.mkdir()
    shutil.copy(RAIZ / "bibliografia" / "apa-es.csl", bib / "apa-es.csl")

    referencias = [
        {"id": "perez2020series", "type": "book", "title": "Series de tiempo aplicadas",
         "edition": "2", "publisher": "Editorial de Prueba",
         "issued": {"date-parts": [[2020]]},
         "author": [{"family": "Pérez", "given": "Ana"}]},
        {"id": "gomez1990metodo", "type": "article-journal", "title": "Un método robusto de ajuste",
         "container-title": "Revista de Prueba", "volume": "6", "issue": "1", "page": "3-73",
         "issued": {"date-parts": [[1990]]},
         "author": [{"family": "Gómez", "given": "Luis"}, {"family": "Ruiz", "given": "Marta"}]},
    ]
    (bib / "referencias.json").write_text(json.dumps(referencias, ensure_ascii=False), "utf-8")
    candado = {"obras": {
        "perez2020series": {"rol": "basica", "adjuntos": [{"zotero": "AAAA1111", "archivo": "perez.pdf", "sha256": "f" * 64}]},
        "gomez1990metodo": {"rol": "primaria", "adjuntos": []},
    }}
    (bib / "zotero.lock.json").write_text(json.dumps(candado), "utf-8")
    (bib / "ejemplares.yml").write_text(yaml.safe_dump({
        "perez2020series": {"archivo": "perez.pdf", "sha256": "f" * 64, "paginas": 9,
                            "edicion_comprobada": "Segunda edición, 2020", "desfase": 2,
                            "procedencia": "ejemplar de prueba"},
    }, allow_unicode=True), "utf-8")
    (bib / "_local" / "texto" / "perez2020series" / "p0005.txt").write_text(PAGINA_5, "utf-8")
    (bib / "_local" / "texto" / "perez2020series" / "p0006.txt").write_text("otra página\n", "utf-8")
    web = PAGINA_WEB.encode("utf-8")
    (bib / "_local" / "web" / "gomez1990metodo" / "pagina.txt").write_bytes(web)
    (bib / "instantaneas.yml").write_text(yaml.safe_dump({
        "gomez1990metodo": {"pagina": {"url": "https://ejemplo.invalid/pagina",
                                       "consulta": dt.date(2026, 11, 10), "sha256": sha(web)}},
    }), "utf-8")

    genera_referencias.BIB = bib
    biblioteca = {r["id"]: r for r in referencias}
    cap1 = genera_referencias.genera(HTML_CAP1, biblioteca, candado["obras"])
    (sitio / "capitulo-1-prueba.html").write_text(cap1, "utf-8")
    (sitio / "capitulo-3-prueba.html").write_text(HTML_CAP3, "utf-8")
    (base / "ensamblado" / "cap3" / "modulos.html").write_text(HTML_CAP3, "utf-8")

    def h(texto_html: str, ident: str) -> str:
        return audita_citas.huella(audita_citas.lee_html(texto_html).afirmaciones[ident].texto)

    hoy = dt.date(2026, 11, 10)
    comun = {"redactado_por": "sesión maestra", "fecha": hoy}
    escribe_registro(bib, 1, [
        {"id": "c1-m1-01", "tipo": "resultado", "afirmacion": "la MM centrada elimina la estacionalidad",
         "hash_texto": h(cap1, "c1-m1-01"), "veredicto": "respaldada", "verificado_por": "verificador A",
         "fuentes": [{"clave": "perez2020series", "loc": "p. 3", "clase": "PDF", "pagina_pdf": 5, "cita": CITA_1}],
         **comun},
        {"id": "c1-m1-02", "tipo": "atribucion", "afirmacion": "el procedimiento es robusto",
         "hash_texto": h(cap1, "c1-m1-02"), "veredicto": "con-matiz", "verificado_por": "verificador A",
         "nota": "la fuente habla de residuos, no de valores atípicos en general",
         "fuentes": [{"clave": "gomez1990metodo", "loc": "§2", "clase": "WEB", "instantanea": "pagina", "cita": CITA_2}],
         **comun},
        {"id": "c1-m1-03", "tipo": "resultado", "afirmacion": "normalización deducida en el material",
         "hash_texto": h(cap1, "c1-m1-03"), "veredicto": "propia", **comun},
        {"id": "c1-m1-04", "tipo": "regla", "afirmacion": "regla de los siete años",
         "hash_texto": h(cap1, "c1-m1-04"), "veredicto": "pendiente",
         "motivo": "no se ha encontrado en ninguna fuente disponible", **comun},
    ])
    escribe_registro(bib, 3, [
        {"id": "c3-m1-01", "tipo": "resultado", "afirmacion": "demostrado en el capítulo",
         "hash_texto": h(HTML_CAP3, "c3-m1-01"), "veredicto": "propia", **comun},
    ])


def escribe_registro(bib: pathlib.Path, capitulo: int, afirmaciones: list[dict]) -> None:
    (bib / "contraste" / f"cap{capitulo}.yml").write_text(
        yaml.safe_dump({"capitulo": capitulo, "afirmaciones": afirmaciones}, allow_unicode=True, sort_keys=False),
        "utf-8")


# --------------------------------------------------------------------------- #
# Herramientas de inyección
# --------------------------------------------------------------------------- #
def cambia(ruta: pathlib.Path, viejo: str, nuevo: str) -> None:
    texto = ruta.read_text("utf-8")
    assert texto.count(viejo) >= 1, f"la inyección no encontró «{viejo}» en {ruta.name}"
    ruta.write_text(texto.replace(viejo, nuevo, 1), "utf-8")


def edita_registro(base: pathlib.Path, capitulo: int, ident: str, cambio) -> None:
    ruta = base / "bibliografia" / "contraste" / f"cap{capitulo}.yml"
    registro = yaml.safe_load(ruta.read_text("utf-8"))
    cambio(next(e for e in registro["afirmaciones"] if e["id"] == ident))
    ruta.write_text(yaml.safe_dump(registro, allow_unicode=True, sort_keys=False), "utf-8")


def edita_yaml(ruta: pathlib.Path, cambio) -> None:
    dato = yaml.safe_load(ruta.read_text("utf-8"))
    cambio(dato)
    ruta.write_text(yaml.safe_dump(dato, allow_unicode=True), "utf-8")


def regenera(base: pathlib.Path) -> None:
    bib = base / "bibliografia"
    genera_referencias.BIB = bib
    referencias = {r["id"]: r for r in json.loads((bib / "referencias.json").read_text("utf-8"))}
    candado = json.loads((bib / "zotero.lock.json").read_text("utf-8"))["obras"]
    ruta = base / "Htmls_Series" / "capitulo-1-prueba.html"
    ruta.write_text(genera_referencias.genera(ruta.read_text("utf-8"), referencias, candado), "utf-8")


CAP1 = "Htmls_Series/capitulo-1-prueba.html"
BIB = "bibliografia"


def i_clave_inexistente(b):
    cambia(b / CAP1, 'data-ref="gomez1990metodo"', 'data-ref="gomez1991metodo"')


def i_cita_tecleada(b):
    cambia(b / CAP1, "(Pérez, 2020, p. 3)", "(Pérez, 2021, p. 3)")


def i_lista_desfasada(b):
    texto = (b / CAP1).read_text("utf-8")
    inicio = texto.index('<li id="ref-m1-gomez1990metodo">')
    fin = texto.index("</li>", inicio) + len("</li>")
    (b / CAP1).write_text(texto[:inicio] + texto[fin:], "utf-8")


def i_cita_fuera_de_afirmacion(b):
    cambia(b / CAP1, '<p data-afirma="c1-m1-01">', "<p>")


def i_afirmacion_sin_entrada(b):
    cambia(b / CAP1, '<p data-afirma="c1-m1-04">',
           '<p data-afirma="c1-m1-09">Otra afirmación, sin registrar.</p>\n      <p data-afirma="c1-m1-04">')


def i_localizador_distinto(b):
    edita_registro(b, 1, "c1-m1-02", lambda e: e["fuentes"][0].update(loc="§3"))


def i_cita_sobre_pendiente(b):
    def cambio(e):
        e.update(veredicto="pendiente", motivo="se retiró el respaldo")
    edita_registro(b, 1, "c1-m1-02", cambio)


def i_veredicto_desconocido(b):
    edita_registro(b, 1, "c1-m1-03", lambda e: e.update(veredicto="verificada"))


def i_pendiente_sin_motivo(b):
    edita_registro(b, 1, "c1-m1-04", lambda e: e.pop("motivo"))


def i_localizador_libre(b):
    # El mismo sitio, dicho fuera del vocabulario cerrado: en el HTML y en el registro.
    edita_registro(b, 1, "c1-m1-01", lambda e: e["fuentes"][0].update(loc="página 3"))
    cambia(b / CAP1, 'data-loc="p. 3"', 'data-loc="página 3"')
    regenera(b)


def i_cita_alterada(b):
    edita_registro(b, 1, "c1-m1-01", lambda e: e["fuentes"][0].update(cita=CITA_1.replace("exactamente", "casi")))


def i_pagina_equivocada(b):
    def cambio(e):
        e["fuentes"][0].update(pagina_pdf=6, loc="p. 4")
    edita_registro(b, 1, "c1-m1-01", cambio)
    cambia(b / CAP1, 'data-loc="p. 3"', 'data-loc="p. 4"')
    regenera(b)


def i_seccion_equivocada(b):
    # La cita SÍ está en la página, pero en §2; el localizador dice §3.
    edita_registro(b, 1, "c1-m1-02", lambda e: e["fuentes"][0].update(loc="§3"))
    cambia(b / CAP1, 'data-loc="§2"', 'data-loc="§3"')
    regenera(b)


def i_seccion_inexistente(b):
    edita_registro(b, 1, "c1-m1-02", lambda e: e["fuentes"][0].update(loc="§7"))
    cambia(b / CAP1, 'data-loc="§2"', 'data-loc="§7"')
    regenera(b)


def i_instantanea_cambiada(b):
    (b / BIB / "_local" / "web" / "gomez1990metodo" / "pagina.txt").write_text(PAGINA_WEB + "añadido\n", "utf-8")


def i_cache_ausente(b):
    (b / BIB / "_local" / "texto" / "perez2020series" / "p0005.txt").unlink()


def i_otro_ejemplar(b):
    edita_yaml(b / BIB / "ejemplares.yml", lambda d: d["perez2020series"].update(sha256="0" * 64))


def i_edicion_cruzada(b):
    edita_yaml(b / BIB / "ejemplares.yml",
               lambda d: d["perez2020series"].update(edicion_comprobada="Primera edición, 2011"))


def i_portada_sin_comprobar(b):
    edita_yaml(b / BIB / "ejemplares.yml", lambda d: d["perez2020series"].update(edicion_comprobada=None))


def i_desfase_que_no_cuadra(b):
    # La cita está en la página, pero esa página es la 7 impresa y no la 3.
    hoja = b / BIB / "_local" / "texto" / "perez2020series" / "p0005.txt"
    hoja.write_text(hoja.read_text("utf-8").replace("        3   Suavizado", "        7   Suavizado"), "utf-8")
    edita_yaml(b / BIB / "ejemplares.yml", lambda d: d["perez2020series"].update(desfase=None))


def i_autoverificacion(b):
    edita_registro(b, 1, "c1-m1-01", lambda e: e.update(verificado_por="Sesión  maestra"))


def i_prosa_cambiada(b):
    cambia(b / CAP1, "elimina la estacionalidad de periodo m", "atenúa la estacionalidad de periodo m")


def i_cita_larga(b):
    larga = " ".join(audita_citas.normaliza(PAGINA_5).split()[2:])
    edita_registro(b, 1, "c1-m1-01", lambda e: e["fuentes"][0].update(cita=larga))


def i_fuera_del_ensamblado(b):
    (b / "ensamblado" / "cap3" / "modulos.html").write_text("<p>sin la afirmación</p>", "utf-8")


INYECCIONES = [
    # La clave cambiada tampoco coincide ya con la fuente registrada: F03 es legítimo.
    ("clave que no existe en la biblioteca", i_clave_inexistente, {"F01", "F03"}),
    ("texto de una cita tecleado a mano", i_cita_tecleada, {"F02"}),
    ("lista de fuentes del módulo desfasada", i_lista_desfasada, {"F02"}),
    ("cita fuera de toda afirmación", i_cita_fuera_de_afirmacion, {"F03"}),
    ("afirmación marcada sin entrada en el registro", i_afirmacion_sin_entrada, {"F03"}),
    # Con el localizador cambiado solo en el registro, la cita tampoco está ya
    # en la sección que el registro dice: F05 es legítimo.
    ("localizador del HTML distinto del registrado", i_localizador_distinto, {"F03", "F05"}),
    ("cita visible sobre una afirmación pendiente", i_cita_sobre_pendiente, {"F03"}),
    ("veredicto que no existe", i_veredicto_desconocido, {"F04"}),
    ("pendiente sin motivo", i_pendiente_sin_motivo, {"F04"}),
    ("localizador fuera del vocabulario cerrado", i_localizador_libre, {"F04"}),
    ("cita literal alterada en una palabra", i_cita_alterada, {"F05"}),
    ("cita literal buscada en otra página", i_pagina_equivocada, {"F05"}),
    ("cita literal en otra sección de la misma página web", i_seccion_equivocada, {"F05"}),
    ("localizador con una sección que la página no tiene", i_seccion_inexistente, {"F05"}),
    ("instantánea web distinta de la registrada", i_instantanea_cambiada, {"F05"}),
    ("la página no está en la caché", i_cache_ausente, {"F05"}),
    ("el ejemplar no es el de Zotero", i_otro_ejemplar, {"F06"}),
    ("se leyó una edición y se cita otra", i_edicion_cruzada, {"F07"}),
    ("portada del ejemplar sin comprobar", i_portada_sin_comprobar, {"F07"}),
    ("la página impresa no cuadra con la del PDF", i_desfase_que_no_cuadra, {"F07"}),
    ("quien verifica es quien redactó", i_autoverificacion, {"F08"}),
    ("la prosa cambió después del contraste", i_prosa_cambiada, {"F09"}),
    ("cita literal de más de 25 palabras", i_cita_larga, {"F11"}),
    ("afirmación ausente de las fuentes de ensamblado", i_fuera_del_ensamblado, {"F12"}),
]


def codigos(base: pathlib.Path, **opciones) -> set[str]:
    hallazgos, _ = audita_citas.audita(base / BIB, base / "Htmls_Series",
                                       dir_ensamblado=base / "ensamblado", **opciones)
    return {x.codigo for x in hallazgos if not x.aviso}


def main() -> int:
    falla = False
    with tempfile.TemporaryDirectory() as temporal:
        molde = pathlib.Path(temporal) / "molde"
        construye(molde)

        limpio = codigos(molde)
        if limpio:
            print(f"FALLA  el capítulo de prueba, sin defectos, no pasa: {sorted(limpio)}")
            for x in audita_citas.audita(molde / BIB, molde / "Htmls_Series",
                                         dir_ensamblado=molde / "ensamblado")[0]:
                print("       ", x)
            return 1
        print("OK     el capítulo de prueba sin defectos pasa limpio")

        for n, (nombre, inyecta, esperado) in enumerate(INYECCIONES, start=1):
            copia = pathlib.Path(temporal) / f"caso{n:02d}"
            shutil.copytree(molde, copia)
            inyecta(copia)
            obtenido = codigos(copia)
            if obtenido == esperado:
                print(f"OK     {n:>2}. {nombre} → {', '.join(sorted(obtenido))}")
            else:
                falla = True
                print(f"FALLA  {n:>2}. {nombre}: se esperaba {sorted(esperado)} y salió {sorted(obtenido)}")

        # --sin-cache: lo que no se puede comprobar se informa, pero no aprueba ni falla
        copia = pathlib.Path(temporal) / "sin_cache"
        shutil.copytree(molde, copia)
        shutil.rmtree(copia / BIB / "_local")
        hallazgos, cuenta = audita_citas.audita(copia / BIB, copia / "Htmls_Series", sin_cache=True,
                                                dir_ensamblado=copia / "ensamblado")
        if [x for x in hallazgos if not x.aviso] or cuenta["sin_cache"] != 2 or cuenta["comprobadas"] != 0:
            falla = True
            print("FALLA  --sin-cache: debía informar de 2 citas no comprobables y no aprobar ninguna")
        else:
            print("OK     --sin-cache informa de 2 citas no comprobables y no da ninguna por comprobada")

    total = len(INYECCIONES)
    print(f"\n{'FALLA' if falla else 'OK   '}  {total} inyecciones" + ("" if falla else ", todas detectadas con su código exacto"))
    return 1 if falla else 0


if __name__ == "__main__":
    sys.exit(main())
