#!/usr/bin/env python3
"""Que el primer módulo espere a las fuentes de sus gráficos.

**El problema.** Chart.js mide y pinta el texto de ejes y leyendas al crear el
gráfico, y no vuelve a pintar cuando llega la fuente web. Los gráficos del curso
piden Montserrat y Fira Code, que llegan de Google Fonts con `display=swap`, y el
módulo de arranque —el 1, o el que pide el ancla `#modulo-K`— se creaba en el
`DOMContentLoaded`, casi siempre antes de que llegaran. Sus gráficos se quedaban
con la letra de respaldo y con otras medidas: el mismo módulo se veía distinto
llegando por enlace que llegando por clic. Comprobado el 2026-10-22 en Chrome,
comparando cada módulo por enlace con el mismo por clic (`#content-area`, píxeles
de cada lienzo y alto). Lo encontró primero Estadística Espacial, con el mismo
motor.

**La corrección**, una sustitución por archivo, en el arranque:

1. `setupEventListeners()` pasa antes del primer `loadModule`: no depende del
   módulo cargado.
2. El primer `loadModule` espera a `fuentesDeLosLienzos()`: las caras normales de
   Montserrat y Fira Code, con un texto de muestra que cubre los tramos de
   Google Fonts que usan los gráficos (latín, latín extendido por «ℓ», griego),
   y un tope de 3 s para que una red lenta, o sin Google Fonts, no deje la
   página en blanco. Si `document.fonts` no existe, no se espera.

Solo el primer módulo: los siguientes se crean al pulsar, con las fuentes ya
cargadas. El reparto de la espera es el de Espacial (`fuentesDeLosLienzos`, el
mismo nombre, para que las copias entre cursos se puedan comparar).

Alcance: los once documentos con el motor de módulos —la plantilla, los seis
capítulos, los dos preparciales, el Taller 2 y la guía del proyecto—, con el
arranque idéntico byte a byte desde `retropropaga_ancla_modulo.py`. La guía del
proyecto no tiene gráficos, pero lleva el mismo motor y lo hereda la próxima que
salga de la plantilla.

Nada que reflejar en `ensamblado/capN/`: el arranque vive en la región que
`ensambla_cap3.py` hereda del capítulo 2 y baja por la cadena 3 → 4 → 5 → 6. La
guía del proyecto y el Taller 2 se ensamblan desde la plantilla.

Escribe en dos fases: si un archivo no se puede transformar, no se escribe
ninguno. Aborta si alguno ya está corregido, así que es seguro reejecutarlo por
error pero NO es reejecutable: está escrito contra el estado anterior.

Uso:  python3 retropropaga_fuentes_lienzos.py       (desde ensamblado/)
"""

from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
HTMLS = RAIZ / "Htmls_Series"
PLANTILLA = RAIZ / "plantilla" / "plantilla-capitulo.html"

# Los once del 2026-10-22. Menos es una carpeta equivocada; más, un documento
# nuevo con el motor que hay que mirar antes de tocarlo.
ESPERADOS = 11

ARRANQUE_VIEJO = """    document.addEventListener('DOMContentLoaded', () => {
      renderNavigation();
      loadModule(moduloDelHash() ?? 1);
      setupEventListeners();
    });
"""

ARRANQUE_NUEVO = """    document.addEventListener('DOMContentLoaded', () => {
      renderNavigation();
      setupEventListeners();
      fuentesDeLosLienzos().then(() => loadModule(moduloDelHash() ?? 1));
    });

    // ================================================================
    // Las fuentes de los gráficos, antes del primer módulo
    //
    // Chart.js mide y pinta el texto al crear el gráfico y no repinta
    // cuando llega la fuente web: el módulo de arranque se quedaba con la
    // letra de respaldo y se veía distinto que llegando por clic. Se
    // espera a las dos caras que piden los gráficos, con un tope para
    // que una red lenta no deje la página en blanco. El texto de muestra
    // pide los tramos de Google Fonts que usan las etiquetas (latín,
    // latín extendido por «ℓ», griego), no solo el primero.
    // ================================================================
    function fuentesDeLosLienzos() {
      if (!document.fonts) return Promise.resolve();
      const muestra = 'Aaá ℓ φθσ 0,5 %';
      const caras = ['400 12px Montserrat', "400 12px 'Fira Code'"];
      return Promise.race([
        Promise.all(caras.map(c => document.fonts.load(c, muestra))),
        new Promise(r => setTimeout(r, 3000))
      ]).catch(() => {});
    }
"""


def corrige(ruta):
    """El texto corregido, o None si el archivo no lleva el motor."""
    nombre = ruta.name
    texto = ruta.read_text(encoding="utf-8")

    if "moduloDelHash" not in texto:
        return None
    if "fuentesDeLosLienzos" in texto:
        raise SystemExit(f"ABORTA [{nombre}]: ya está corregido. "
                         "Este script no es reejecutable.")
    n = texto.count(ARRANQUE_VIEJO)
    if n != 1:
        raise SystemExit(f"ABORTA [{nombre} / arranque]: el marcador aparece {n} "
                         f"veces, se esperaba 1.\n  {ARRANQUE_VIEJO[:90]!r}")
    nuevo = texto.replace(ARRANQUE_VIEJO, ARRANQUE_NUEVO, 1)

    # Comprobaciones de que el resultado contiene lo que debe, y nada más
    faltan = [q for q in ("function fuentesDeLosLienzos()",
                          "fuentesDeLosLienzos().then(() => loadModule(moduloDelHash() ?? 1));",
                          "loadModule(moduloDelHash() ?? 1)")
              if nuevo.count(q) != 1]
    if faltan:
        raise SystemExit(f"ABORTA [{nombre}]: no aparece una sola vez: {faltan}")
    if nuevo.replace(ARRANQUE_NUEVO, ARRANQUE_VIEJO) != texto:
        raise SystemExit(f"ABORTA [{nombre}]: cambiaría algo fuera del arranque.")
    return nuevo


def main():
    if not PLANTILLA.exists():
        raise SystemExit(f"ABORTA: no existe {PLANTILLA}")
    objetivos = [PLANTILLA] + sorted(HTMLS.glob("*.html"))

    # Fase 1: se calcula y se comprueba todo antes de escribir nada.
    por_escribir = []
    for ruta in objetivos:
        nuevo = corrige(ruta)
        if nuevo is None:
            print(f"  {ruta.name}: sin el motor de módulos, se omite")
        else:
            por_escribir.append((ruta, nuevo))
    if len(por_escribir) != ESPERADOS:
        raise SystemExit(f"ABORTA: {len(por_escribir)} archivos con el motor, se "
                         f"esperaban {ESPERADOS}: "
                         f"{', '.join(r.name for r, _ in por_escribir)}")

    # Fase 2: escribir.
    print(f"\nRetropropagando la espera de las fuentes a {len(por_escribir)} archivos:\n")
    for ruta, nuevo in por_escribir:
        ruta.write_text(nuevo, encoding="utf-8")
        print(f"  {ruta.relative_to(RAIZ)}: corregido")
    print(f"\n{len(por_escribir)} archivos corregidos.")


if __name__ == "__main__":
    main()
