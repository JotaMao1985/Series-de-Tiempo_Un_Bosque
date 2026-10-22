#!/usr/bin/env python3
"""Que el «Saltar al contenido» no devuelva al lector al módulo 1.

**El problema.** Todos los documentos abren con el enlace de accesibilidad
`<a href="#main-content" class="skip-link">`, el primer elemento al que se llega
con el tabulador. Activarlo cambia el ancla a `#main-content` y dispara el
`hashchange` que desde el 2026-09-02 atiende los enlaces `#modulo-K`. Como
`moduloDelHash()` devolvía 1 para cualquier ancla que no fuera de un módulo, el
oyente cargaba el módulo 1: quien leía el 4 y usaba el enlace con el teclado
aterrizaba en «4.1 De ARMA a ARIMA», con la barra reescrita a `#modulo-1`.
Comprobado por HTTP el 2026-10-21 en el capítulo 4, llegando por
`#modulo-4`, Tab y Enter.

**La corrección**, en tres sustituciones por archivo:

1. `moduloDelHash()` devuelve `null`, y no 1, cuando el ancla no es de un
   módulo: no tiene la forma `#modulo-K`, o K se sale de `courseData.modules`.
2. El arranque traduce ese `null` a 1: `loadModule(moduloDelHash() ?? 1)`. Sin
   ancla, o con una ajena, se sigue abriendo el 1, como antes.
3. El oyente de `hashchange` solo carga si el ancla es de un módulo. La del
   «Saltar al contenido», o cualquier otra ajena, no mueve nada.

`fijarHashDelModulo()` y `loadModule()` no se tocan. El nombre de
`moduloDelHash()` tampoco: `precalculo/ensambla_proyecto.py` lo exige en el
motor y `proyecto/README.md` lo cita.

Alcance: los once documentos que llevan el motor —la plantilla, los seis
capítulos, los dos preparciales, el Taller 2 y la guía del proyecto—, todos con
el bloque idéntico byte a byte. `index.html` y el Taller 1 tienen el enlace
pero no el motor, así que el ancla hace ahí lo que hace el navegador.

Nada que reflejar en `ensamblado/capN/`: el motor de navegación vive en la
región que `ensambla_cap3.py` hereda del capítulo 2, y de ahí baja por la
cadena 3 → 4 → 5 → 6. La guía del proyecto (`precalculo/ensambla_proyecto.py`)
y el Taller 2 se ensamblan desde la plantilla.

Escribe en dos fases: si un archivo no se puede transformar, no se escribe
ninguno. Aborta si alguno ya está corregido, así que es seguro reejecutarlo por
error pero NO es reejecutable: está escrito contra el estado anterior.

Origen: la auditoría del mismo motor en Diseño de Experimentos
(`ensamblado/retropropaga_enlace_modulo.py`, 2026-10-21), que lo copió de aquí
y dejó escrito que no se llevaba el repliegue al 1 del `hashchange`.

Uso:  python3 retropropaga_ancla_modulo.py       (desde ensamblado/)
"""

from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
HTMLS = RAIZ / "Htmls_Series"
PLANTILLA = RAIZ / "plantilla" / "plantilla-capitulo.html"

# Los once del 2026-10-21. Menos es una carpeta equivocada; más, un documento
# nuevo con el motor que hay que mirar antes de tocarlo.
ESPERADOS = 11

# ---------------------------------------------------------------------------
# 1. El arranque
# ---------------------------------------------------------------------------
ARRANQUE_VIEJO = """      renderNavigation();
      loadModule(moduloDelHash());
      setupEventListeners();
"""

ARRANQUE_NUEVO = """      renderNavigation();
      loadModule(moduloDelHash() ?? 1);
      setupEventListeners();
"""

# ---------------------------------------------------------------------------
# 2. `moduloDelHash()`: null, y no 1, para un ancla que no es de un módulo
# ---------------------------------------------------------------------------
FUNCION_VIEJA = """    function moduloDelHash() {
      const m = /^#modulo-(\\d+)$/.exec(window.location.hash || '');
      if (!m) return 1;
      const id = parseInt(m[1], 10);
      return (id >= 1 && id <= courseData.modules.length) ? id : 1;
    }
"""

FUNCION_NUEVA = """    function moduloDelHash() {
      // null, y no 1, si el ancla no es de un módulo: el arranque lo traduce
      // a 1 y el oyente de hashchange lo ignora.
      const m = /^#modulo-(\\d+)$/.exec(window.location.hash || '');
      if (!m) return null;
      const id = parseInt(m[1], 10);
      return (id >= 1 && id <= courseData.modules.length) ? id : null;
    }
"""

# ---------------------------------------------------------------------------
# 3. El oyente de `hashchange`
# ---------------------------------------------------------------------------
OYENTE_VIEJO = """    window.addEventListener('hashchange', () => {
      const id = moduloDelHash();
      if (id !== currentModuleId) loadModule(id);
    });
"""

OYENTE_NUEVO = """    // Un ancla que no es de un módulo no mueve nada. Antes cargaba el 1, y el
    // «Saltar al contenido» (#main-content) sacaba al lector del que leía.
    window.addEventListener('hashchange', () => {
      const id = moduloDelHash();
      if (id !== null && id !== currentModuleId) loadModule(id);
    });
"""

SUSTITUCIONES = [
    ("arranque", ARRANQUE_VIEJO, ARRANQUE_NUEVO),
    ("moduloDelHash", FUNCION_VIEJA, FUNCION_NUEVA),
    ("oyente de hashchange", OYENTE_VIEJO, OYENTE_NUEVO),
]


def una_vez(texto, viejo, nuevo, etiqueta, archivo):
    n = texto.count(viejo)
    if n != 1:
        raise SystemExit(f"ABORTA [{archivo} / {etiqueta}]: el marcador aparece "
                         f"{n} veces, se esperaba 1.\n  {viejo[:90]!r}")
    return texto.replace(viejo, nuevo, 1)


def corrige(ruta):
    """El texto corregido, o None si el archivo no lleva el motor."""
    nombre = ruta.name
    texto = ruta.read_text(encoding="utf-8")

    if "moduloDelHash" not in texto:
        return None
    if "moduloDelHash() ?? 1" in texto or "id !== null && id !== currentModuleId" in texto:
        raise SystemExit(f"ABORTA [{nombre}]: ya está corregido. "
                         "Este script no es reejecutable.")

    nuevo = texto
    for etiqueta, viejo, reemplazo in SUSTITUCIONES:
        nuevo = una_vez(nuevo, viejo, reemplazo, etiqueta, nombre)

    # Comprobaciones de que el resultado contiene lo que debe, y nada más
    faltan = [q for q in ("loadModule(moduloDelHash() ?? 1);", "if (!m) return null;",
                          "? id : null;", "if (id !== null && id !== currentModuleId)")
              if nuevo.count(q) != 1]
    if faltan:
        raise SystemExit(f"ABORTA [{nombre}]: no aparece una sola vez: {faltan}")
    if "loadModule(moduloDelHash());" in nuevo or "? id : 1;" in nuevo:
        raise SystemExit(f"ABORTA [{nombre}]: queda una pieza del motor viejo.")
    deshecho = nuevo
    for _, viejo, reemplazo in SUSTITUCIONES:
        deshecho = deshecho.replace(reemplazo, viejo)
    if deshecho != texto:
        raise SystemExit(f"ABORTA [{nombre}]: cambiaría algo fuera de las tres "
                         "sustituciones.")
    return nuevo


def main():
    objetivos = [PLANTILLA] + sorted(HTMLS.glob("*.html"))
    if not PLANTILLA.exists():
        raise SystemExit(f"ABORTA: no existe {PLANTILLA}")

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
    print(f"\nRetropropagando el arreglo del ancla a {len(por_escribir)} archivos:\n")
    for ruta, nuevo in por_escribir:
        ruta.write_text(nuevo, encoding="utf-8")
        print(f"  {ruta.relative_to(RAIZ)}: corregido")
    print(f"\n{len(por_escribir)} archivos corregidos.")


if __name__ == "__main__":
    main()
