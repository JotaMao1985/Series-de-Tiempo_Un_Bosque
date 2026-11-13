#!/usr/bin/env python3
"""
extrae_fuente.py — el texto de las fuentes, página a página, fuera de git

Material de Series de Tiempo 2026-II (20948).

Contrastar una afirmación exige haber LEÍDO el pasaje. Para que eso lo pueda
comprobar un guion y no haya que creerle a nadie, el texto de cada fuente se
extrae a una caché local y el auditor busca ahí, literalmente, la cita que el
registro de contraste dice haber leído.

Dos clases de fuente:

  · PDF escaneado          → `--ocr`: pdftoppm a 300 ppp y tesseract por página.
                             El texto sale con erratas de reconocimiento, así que una cita
                             literal correcta puede no coincidir: hay que copiarla del texto
                             extraído y preferir tramos que hayan salido limpios. Queda
                             anotado en `ejemplares.yml` como `texto_por: ocr`.
  · PDF adjunto en Zotero  → `pdftotext -layout`, un archivo por página:
                             bibliografia/_local/texto/<clave>/p0001.txt
                             Si la obra no tiene PDF adjunto en Zotero, se
                             busca bibliografia/_local/pdf/<clave>.pdf (puede
                             ser un enlace simbólico al archivo de verdad).
                             Junto al texto queda `_origen.json` con el sha256
                             del PDF del que salió: el auditor exige que sea
                             el del ejemplar registrado.
  · página web (FPP3)      → instantánea en texto plano:
                             bibliografia/_local/web/<clave>/<nombre>.txt
  · ayuda de R             → `--doc CLAVE TEMA`: la página de ayuda tal como la
                             imprime R, en el mismo sitio que una instantánea web. Queda
                             anotada con la versión de R y de su paquete, no con una URL:
                             la ayuda cambia de una versión a otra, y por eso la versión
                             es la referencia (el capítulo 4 ya se topó con que
                             `?AirPassengers` cita 1976 en R 4.3.3 y 1994 en R 4.6).

`bibliografia/_local/` está ignorado por git: el repo es público y los libros
tienen derechos de autor. Lo que SÍ se versiona es la huella de lo que se leyó:

  · ejemplares.yml     — por cada PDF: archivo, sha256, número de páginas. Y
                         tres campos que se llenan a mano y este guion respeta:
                         `edicion_comprobada` (lo que dice la portada),
                         `desfase` (página del PDF − página impresa) y
                         `procedencia`
  · instantaneas.yml   — por cada página web: URL, fecha de consulta y sha256
                         del texto guardado

Uso:  python3 precalculo/extrae_fuente.py                    # todos los PDF
      python3 precalculo/extrae_fuente.py --clave cryer2008time
      python3 precalculo/extrae_fuente.py --web hyndman2021forecasting \\
              https://otexts.com/fpp3/stlfeatures.html
      python3 precalculo/extrae_fuente.py --doc rcore2026r stl
      python3 precalculo/extrae_fuente.py --web CLAVE URL --desde archivo.html
              (si la página no abre desde aquí: se guarda con el navegador)

La URL que se registra es la final, después de las redirecciones: FPP3 sirve hoy
un capítulo entero por página, y `stl.html` lleva a la página del capítulo 3.
El auditor acota la búsqueda a la sección que diga el localizador («§3.6»).

Requiere `pdftotext`, `pdfinfo` (poppler) y `pandoc`.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import urllib.request

import yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent
BIB = RAIZ / "bibliografia"
LOCAL = BIB / "_local"
ALMACEN = pathlib.Path.home() / "Zotero" / "storage"
MANUALES = ("edicion_comprobada", "desfase", "procedencia", "nota")
AGENTE = "auditor-bibliografico/0.1"


def sha256_bytes(dato: bytes) -> str:
    return hashlib.sha256(dato).hexdigest()


def lee_yaml(ruta: pathlib.Path) -> dict:
    return (yaml.safe_load(ruta.read_text("utf-8")) or {}) if ruta.exists() else {}


def escribe_yaml(ruta: pathlib.Path, dato: dict, cabecera: str) -> None:
    cuerpo = yaml.safe_dump(dato, allow_unicode=True, sort_keys=True, width=100)
    ruta.write_text(cabecera + cuerpo, "utf-8")


def candado() -> dict:
    ruta = BIB / "zotero.lock.json"
    if not ruta.exists():
        sys.exit("FALLA  falta bibliografia/zotero.lock.json: corre exporta_zotero.py")
    return json.loads(ruta.read_text("utf-8"))["obras"]


def sha256_archivo(ruta: pathlib.Path) -> str:
    h = hashlib.sha256()
    with ruta.open("rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def pdf_de(clave: str, obra: dict) -> pathlib.Path | None:
    """El PDF adjunto en Zotero o, si no hay, bibliografia/_local/pdf/<clave>.pdf."""
    if obra["adjuntos"]:
        if len(obra["adjuntos"]) > 1:
            print(f"AVISO  {clave}: tiene {len(obra['adjuntos'])} PDF en Zotero; se usa el primero")
        a = obra["adjuntos"][0]
        ruta = ALMACEN / a["zotero"] / a["archivo"]
    else:
        ruta = LOCAL / "pdf" / f"{clave}.pdf"
    return ruta if ruta.is_file() else None


def ocr(pdf: pathlib.Path, paginas: int) -> list[str]:
    """Texto por página de un PDF sin capa de texto, con tesseract."""
    import tempfile
    hojas = []
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-r", "300", "-gray", "-png", str(pdf), f"{tmp}/p"], check=True)
        for n in range(1, paginas + 1):
            img = sorted(pathlib.Path(tmp).glob(f"p-*{n}.png"))
            img = [i for i in pathlib.Path(tmp).glob("p-*.png") if int(i.stem.split("-")[-1]) == n]
            if not img:
                hojas.append("")
                continue
            r = subprocess.run(["tesseract", str(img[0]), "-", "-l", "eng", "--psm", "6"],
                               capture_output=True)
            hojas.append(r.stdout.decode("utf-8", "replace"))
            print(f"       OCR página {n}/{paginas}", end="\r", flush=True)
    print()
    return hojas


def extrae_pdf(clave: str, pdf: pathlib.Path, con_ocr: bool = False) -> dict | None:
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    paginas = int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1))
    if con_ocr:
        hojas = ocr(pdf, paginas)
    else:
        texto = subprocess.run(
            ["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"],
            capture_output=True, check=True,
        ).stdout.decode("utf-8", "replace")
        hojas = texto.split("\f")
        if hojas and not hojas[-1].strip():
            hojas = hojas[:-1]
        if not any(h.strip() for h in hojas):
            print(f"AVISO  {clave}: el PDF no tiene capa de texto; hace falta --ocr")
            return None
    destino = LOCAL / "texto" / clave
    destino.mkdir(parents=True, exist_ok=True)
    for viejo in destino.glob("p*.txt"):
        viejo.unlink()
    for n, hoja in enumerate(hojas, start=1):
        (destino / f"p{n:04d}.txt").write_text(hoja, "utf-8")
    huella = sha256_archivo(pdf)
    (destino / "_origen.json").write_text(
        json.dumps({"sha256": huella, "archivo": pdf.resolve().name}, ensure_ascii=False), "utf-8")
    vacias = sum(1 for h in hojas if not h.strip())
    print(f"OK     {clave}: {len(hojas)} páginas de texto ({vacias} vacías) → _local/texto/{clave}/")
    return {
        "archivo": pdf.resolve().name,
        "sha256": huella,
        "paginas": paginas,
        "paginas_sin_texto": vacias,
        "texto_por": "ocr" if con_ocr else "pdftotext",
    }


def extrae_pdfs(solo: str | None, con_ocr: bool = False) -> int:
    obras = candado()
    ruta = BIB / "ejemplares.yml"
    previo = lee_yaml(ruta)
    nuevo = {}
    for clave, obra in obras.items():
        if solo and clave != solo:
            if clave in previo:
                nuevo[clave] = previo[clave]
            continue
        pdf = pdf_de(clave, obra)
        if pdf is None:
            if clave in previo:               # el PDF no está aquí, pero la ficha se conserva
                nuevo[clave] = previo[clave]
            continue
        ficha = extrae_pdf(clave, pdf, con_ocr=con_ocr)
        for campo in MANUALES:
            ficha[campo] = (previo.get(clave) or {}).get(campo)
        nuevo[clave] = ficha
    escribe_yaml(ruta, nuevo, (
        "# Ejemplares leídos: la huella de cada PDF, nunca el PDF.\n"
        "# `archivo`, `sha256` y `paginas` los escribe extrae_fuente.py.\n"
        "# `edicion_comprobada`, `desfase` (página del PDF − página impresa, si es\n"
        "# constante), `procedencia` y `nota` se llenan a mano mirando la portada;\n"
        "# el guion los respeta.\n"
    ))
    print(f"OK     bibliografia/ejemplares.yml: {len(nuevo)} ejemplares")
    return 0


def extrae_doc_r(clave: str, tema: str) -> int:
    """Instantánea de una página de ayuda de R, con la versión que la imprimió."""
    if clave not in candado():
        sys.exit(f"FALLA  «{clave}» no está en la biblioteca del curso")
    # El paquete se deduce del archivo de ayuda: `environment(get(...))` sirve para
    # una función pero falla con un conjunto de datos, que no lo es.
    guion = r"""
      h <- utils:::.getHelpFile(help("%s"))
      ruta <- attr(h, "Rdfile")
      paq <- if (is.null(ruta)) "" else basename(dirname(dirname(ruta)))
      ver <- if (nzchar(paq)) tryCatch(paste(paq, utils::packageVersion(paq)),
                                       error = function(e) paq) else ""
      cat("@@VERSION@@", R.version.string, if (nzchar(ver)) paste("·", ver) else "", "
")
      tools::Rd2txt(h, options = list(underline_titles = FALSE))
    """ % tema
    r = subprocess.run(["Rscript", "-e", guion], capture_output=True)
    if r.returncode != 0:
        sys.exit(f"FALLA  R no pudo imprimir la ayuda de «{tema}»: {r.stderr.decode()[:300]}")
    salida = r.stdout.decode("utf-8", "replace")
    if not salida.startswith("@@VERSION@@"):
        sys.exit(f"FALLA  la salida de R para «{tema}» no trae la línea de versión")
    version, _, cuerpo = salida.partition("\n")
    plano = cuerpo.encode("utf-8")
    destino = LOCAL / "web" / clave
    destino.mkdir(parents=True, exist_ok=True)
    (destino / f"{tema}.txt").write_bytes(plano)

    ruta = BIB / "instantaneas.yml"
    registro = lee_yaml(ruta)
    registro.setdefault(clave, {})[tema] = {
        "origen": f"ayuda de R: help({tema})",
        "version": " ".join(version.replace("@@VERSION@@", "").split()),
        "consulta": dt.date.today().isoformat(),
        "sha256": sha256_bytes(plano),
        "palabras": len(plano.split()),
    }
    escribe_yaml(ruta, registro, (
        "# Páginas web y ayudas de R leídas: de dónde salieron, cuándo y la huella del\n"
        "# texto guardado. El texto vive en bibliografia/_local/web/ (fuera de git).\n"
    ))
    print(f"OK     {clave}/{tema}: {len(plano.split())} palabras · {registro[clave][tema]['version']}")
    return 0


def nombre_de(url: str) -> str:
    cola = url.rstrip("/").rsplit("/", 1)[-1] or "indice"
    return re.sub(r"[^A-Za-z0-9_-]", "-", re.sub(r"\.html?$", "", cola))


def extrae_web(clave: str, url: str, desde: str | None, nombre: str | None) -> int:
    if clave not in candado():
        sys.exit(f"FALLA  «{clave}» no está en la biblioteca del curso")
    url_final = url
    if desde:
        crudo = pathlib.Path(desde).read_bytes()
    else:
        pedido = urllib.request.Request(url, headers={"User-Agent": AGENTE})
        with urllib.request.urlopen(pedido, timeout=30) as r:
            crudo = r.read()
            url_final = r.geturl()          # tras las redirecciones
    plano = subprocess.run(
        ["pandoc", "-f", "html", "-t", "plain", "--wrap=none"],
        input=crudo, capture_output=True, check=True,
    ).stdout
    nombre = nombre or nombre_de(url_final)
    destino = LOCAL / "web" / clave
    destino.mkdir(parents=True, exist_ok=True)
    (destino / f"{nombre}.txt").write_bytes(plano)

    ruta = BIB / "instantaneas.yml"
    registro = lee_yaml(ruta)
    registro.setdefault(clave, {})[nombre] = {
        "url": url_final,
        "consulta": dt.date.today().isoformat(),
        "sha256": sha256_bytes(plano),
        "palabras": len(plano.split()),
    }
    escribe_yaml(ruta, registro, (
        "# Páginas web leídas: URL, fecha de consulta y huella del texto guardado.\n"
        "# El texto vive en bibliografia/_local/web/ (fuera de git).\n"
    ))
    print(f"OK     {clave}/{nombre}: {len(plano.split())} palabras → _local/web/{clave}/{nombre}.txt")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--clave", help="extrae solo el PDF de esta obra")
    ap.add_argument("--ocr", action="store_true",
                    help="el PDF es un escaneo sin capa de texto: pdftoppm + tesseract")
    ap.add_argument("--web", nargs=2, metavar=("CLAVE", "URL"),
                    help="guarda la instantánea de una página web")
    ap.add_argument("--desde", help="con --web: HTML ya descargado, en vez de pedirlo")
    ap.add_argument("--nombre", help="con --web: nombre de la instantánea (por defecto, el de la URL)")
    ap.add_argument("--doc", nargs=2, metavar=("CLAVE", "TEMA"),
                    help="instantánea de una página de ayuda de R")
    args = ap.parse_args()
    if args.doc:
        return extrae_doc_r(args.doc[0], args.doc[1])
    if args.web:
        return extrae_web(args.web[0], args.web[1], args.desde, args.nombre)
    return extrae_pdfs(args.clave, con_ocr=args.ocr)


if __name__ == "__main__":
    sys.exit(main())
