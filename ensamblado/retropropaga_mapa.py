#!/usr/bin/env python3
"""Instala el componente `.mapa-estacional` en el capítulo 1 y en la plantilla.

El capítulo 5 lo estrena y lo hereda por construcción (se ensambla desde el 4,
donde `ensambla_cap5.py` lo instala). Los capítulos 2, 3 y 4 no lo reciben: es
un componente para *ver* la estacionalidad, y ninguno de los tres la trata.

Sí lo reciben:
  - el **capítulo 1**, cuyo módulo 3 es justamente el de visualización estacional;
  - la **plantilla**, porque la regla del Checkpoint 0 exige que un componente
    nuevo entre en ella en la misma sesión.

Uso:  python3 retropropaga_mapa.py                (desde ensamblado/)
      python3 retropropaga_mapa.py --actualiza     (lleva un cambio del componente)
      python3 retropropaga_mapa.py --comprobar     (dice si están al día; no escribe)

Sin opciones INSTALA, y es idempotente por abortar: si un archivo ya trae el
componente, salta. Con `--actualiza` SUSTITUYE el componente ya instalado por el
de `componentes/`: el bloque CSS (del comentario «Componente .mapa-estacional»
al cierre de su media query de 640 px) y el bloque JS (del rótulo del componente
al cierre de `iniciarMapasEstacionales`). Nada fuera de esos dos bloques cambia
—se comprueba—, y los retoques locales que un destino haya hecho dentro del
bloque se vuelven a aplicar (`AJUSTES_LOCALES`). Reejecutarlo no cambia nada.
El capítulo 5 no pasa por aquí: lo recibe al reensamblarse (`ensambla_cap5.py`).
"""

import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
COMPONENTES = AQUI / "componentes"

sys.path.insert(0, str(COMPONENTES))
from mapa_estacional_html import (mapa_estacional_html,   # noqa: E402
                                  comprueba_mapa_estacional)

DESTINOS = {
    "cap1": RAIZ / "Htmls_Series" / "capitulo-1-componentes-descomposicion.html",
    "plantilla": RAIZ / "plantilla" / "plantilla-capitulo.html",
}

ANCLA_CSS = """      .ciclo-etapa:not(:last-child)::after {
        content: "\\2193";
        align-self: center;
        margin: 0.15rem 0;
      }
    }
  </style>"""

ANCLA_JS = """        const inicial = botones.findIndex(b => b.getAttribute('aria-selected') === 'true');
        seleccionar(inicial >= 0 ? inicial : 0, false);
      });
    }
"""

# Registro del capítulo 1: AirPassengers cruda, que es la serie que ya tiene
# incrustada. Se registra como FUNCIÓN para que se evalúe al cargar el módulo,
# cuando `DATOS_CAP1` ya existe.
REGISTRO_CAP1 = """
    // Instancia del capítulo 1: la serie del capítulo, vista como mes x año.
    MAPAS_ESTACIONALES['cap1-airpassengers'] = function () {
      const datos = matrizMesAnio(DATOS_CAP1.observado, 1949, 1);
      return Object.assign(datos, {
        escala: 'secuencial',
        decimales: 0,
        unidad: 'pasajeros',
        nota: 'Cada fila es un año y cada columna un mes. Las bandas verticales de julio y ' +
          'agosto son la estacionalidad; que se oscurezcan hacia abajo a la vez que toda la ' +
          'fila es la tendencia. Y que la <em>diferencia</em> entre el mes alto y el bajo ' +
          'crezca con los años es lo que hace multiplicativa a esta serie.'
      });
    };
"""

# Registro de la plantilla: serie sintética con semilla fija, como el resto de
# sus demostraciones. No incrusta ningún dato.
REGISTRO_PLANTILLA = """
    // Demostración del componente .mapa-estacional. Como el resto de la
    // plantilla, no incrusta datos: genera la serie con semilla fija.
    MAPAS_ESTACIONALES['demo-mapa'] = function () {
      const ruido = generarRuidoNormal(96, 20260727);
      const estacional = [-8, -10, 2, 0, 1, 9, 18, 17, 5, -6, -17, -9];
      const valores = [];
      for (let t = 0; t < 96; t++) {
        valores.push(100 + 0.45 * t + estacional[t % 12] + 3 * ruido[t]);
      }
      return Object.assign(matrizMesAnio(valores, 2018, 1), {
        escala: 'secuencial',
        decimales: 1,
        unidad: '',
        nota: 'Serie simulada con tendencia y estacionalidad aditiva (semilla fija). ' +
          'Las columnas de julio y agosto forman una banda vertical clara: eso es la ' +
          'estacionalidad. Para una serie ya diferenciada se pasa <code>escala: ' +
          '\\'divergente\\'</code> y la paleta se centra en cero.'
      });
    };
"""

# Dónde va la instancia en cada archivo, y con qué ancla.
INSTANCIAS = {
    "cap1": {
        "id": "cap1-airpassengers",
        "titulo": "AirPassengers, mes × año",
        "nota": "",
        "ancla": '      <div class="simulador" data-simulador="grafico-estacional">',
        "sangria": "      ",
        "antes": True,
    },
    "plantilla": {
        "id": "demo-mapa",
        "titulo": "Mapa estacional (demostración)",
        "nota": "",
        "ancla": '      <div class="simulador" data-simulador="demo-interruptores">',
        "sangria": "      ",
        "antes": True,
    },
}

REGISTROS = {"cap1": REGISTRO_CAP1, "plantilla": REGISTRO_PLANTILLA}


def una_vez(texto, viejo, nuevo, etiqueta):
    n = texto.count(viejo)
    if n != 1:
        raise SystemExit(f"ABORTA [{etiqueta}]: el marcador aparece {n} veces, "
                         f"se esperaba 1.\n  marcador: {viejo[:110]!r}")
    return texto.replace(viejo, nuevo, 1)


css = (COMPONENTES / "mapa_estacional.css").read_text(encoding="utf-8").rstrip("\n")
js = (COMPONENTES / "mapa_estacional.js").read_text(encoding="utf-8").rstrip("\n")

# ---------------------------------------------------------------------------
# Modo --actualiza / --comprobar
# ---------------------------------------------------------------------------
INICIO_CSS = ("    /* ------------------------------------------------------------------\n"
              "       Componente .mapa-estacional — mapa de calor mes x año")
FIN_CSS = "    @media (max-width: 640px) {\n      .mapa-estacional-rejilla {"
INICIO_JS = ("    // ================================================================\n"
             "    // Componente .mapa-estacional — mapa de calor mes x año")
FIN_JS = "    function iniciarMapasEstacionales() {"

# Retoques que un destino haga a mano DENTRO del bloque del componente y que
# haya que conservar, como pares (texto del componente, texto local). Hoy no
# hay ninguno: el único, la nota alineada a la izquierda del capítulo 1 (su R2:
# justificada, en el teléfono abría huecos), pasó al componente en la R2 del
# capítulo 5. La variante `--entero` del capítulo 1 va DESPUÉS del bloque y no
# se toca.
AJUSTES_LOCALES = {
    "cap1": [],
    "plantilla": [],
}


def bloque(html, inicio, fin_marca, cierre, etiqueta):
    """(i, j) del bloque que empieza en `inicio` (único) y acaba en el `cierre`
    que sigue a `fin_marca`; j apunta justo detrás de ese cierre."""
    if html.count(inicio) != 1:
        raise SystemExit(f"ABORTA [{etiqueta}]: el inicio del bloque aparece "
                         f"{html.count(inicio)} veces, se esperaba 1.")
    i = html.index(inicio)
    k = html.find(fin_marca, i)
    if k == -1:
        raise SystemExit(f"ABORTA [{etiqueta}]: no encuentro {fin_marca[:60]!r} tras el inicio.")
    j = html.find(cierre, k)
    if j == -1:
        raise SystemExit(f"ABORTA [{etiqueta}]: no encuentro el cierre del bloque.")
    return i, j + len(cierre)


def trozo(texto, i, j):
    return texto[i:j]


def actualiza(nombre, html):
    """Devuelve el HTML con el componente al día y la lista de fallos."""
    nuevo_css = css.lstrip("\n")
    for viejo, nuevo in AJUSTES_LOCALES[nombre]:
        if nuevo_css.count(viejo) != 1:
            raise SystemExit(f"ABORTA [{nombre}/ajuste local]: {viejo[:50]!r} aparece "
                             f"{nuevo_css.count(viejo)} veces en el componente.")
        nuevo_css = nuevo_css.replace(viejo, nuevo)
    i, j = bloque(html, INICIO_CSS, FIN_CSS, "\n      }\n    }", f"{nombre}/CSS")
    salida = html[:i] + nuevo_css + html[j:]
    a, b = bloque(salida, INICIO_JS, FIN_JS, "\n    }", f"{nombre}/JS")
    salida = salida[:a] + js + salida[b:]

    fallos = []
    # Fuera de los dos bloques, el archivo no cambia
    i2, j2 = bloque(salida, INICIO_CSS, FIN_CSS, "\n      }\n    }", f"{nombre}/CSS nuevo")
    a2, b2 = bloque(salida, INICIO_JS, FIN_JS, "\n    }", f"{nombre}/JS nuevo")
    a0, b0 = bloque(html, INICIO_JS, FIN_JS, "\n    }", f"{nombre}/JS viejo")
    # (Los cortes van por trozo(): el compilador de Tailwind lee este archivo y
    # tomaría un corte de dos variables por una clase de propiedad arbitraria.)
    if (salida[:i2] != html[:i] or trozo(salida, j2, a2) != trozo(html, j, a0)
            or salida[b2:] != html[b0:]):
        fallos.append("ha cambiado algo fuera de los bloques del componente")
    if trozo(salida, i2, j2) != nuevo_css or trozo(salida, a2, b2) != js:
        fallos.append("los bloques no quedaron iguales al componente")
    inst = INSTANCIAS[nombre]
    fallos += comprueba_mapa_estacional(salida, inst["id"])
    # (`.mapa-estacional-nota {` y otras salen más de una vez en el capítulo 1,
    # por su variante `--entero`: se cuentan solo las que son únicas en todos.)
    componente = css + js
    for pieza, esperadas in [(".mapa-estacional {", 1),
                             (".mapa-estacional-fila {", componente.count(".mapa-estacional-fila {")),
                             ("function pintarMapaEstacional", 1),
                             ("function ajustarMapaEstacional",
                              componente.count("function ajustarMapaEstacional")),
                             ("function matrizMesAnio", 1),
                             ("function iniciarMapasEstacionales", 1),
                             ("const MAPAS_ESTACIONALES", 1),
                             ("        iniciarMapasEstacionales();", 1),
                             (f"MAPAS_ESTACIONALES['{inst['id']}']", 1)]:
        if salida.count(pieza) != esperadas:
            fallos.append(f"'{pieza}' aparece {salida.count(pieza)} veces, se esperaban {esperadas}")
    return salida, fallos


if "--actualiza" in sys.argv or "--comprobar" in sys.argv:
    escribir = "--actualiza" in sys.argv
    pendientes = 0
    for nombre, ruta in DESTINOS.items():
        html = ruta.read_text(encoding="utf-8")
        if ".mapa-estacional {" not in html:
            raise SystemExit(f"ABORTA [{nombre}]: no trae el componente; instálalo sin opciones.")
        salida, fallos = actualiza(nombre, html)
        if fallos:
            raise SystemExit(f"ABORTA [{nombre}]:\n  - " + "\n  - ".join(fallos))
        # Idempotencia: aplicado sobre su propio resultado no cambia nada
        if actualiza(nombre, salida)[0] != salida:
            raise SystemExit(f"ABORTA [{nombre}]: la actualización no es idempotente.")
        if salida == html:
            print(f"AL DÍA {ruta.name}")
            continue
        pendientes += 1
        if escribir:
            ruta.write_text(salida, encoding="utf-8")
            print(f"OK     {ruta.name}: componente sustituido "
                  f"({len(html.encode('utf-8'))} → {len(salida.encode('utf-8'))} bytes)")
        else:
            print(f"PENDIENTE {ruta.name}: el componente instalado no es el de componentes/")
    if not escribir and pendientes:
        sys.exit(1)
    print("Listo.")
    sys.exit(0)

for nombre, ruta in DESTINOS.items():
    if not ruta.exists():
        raise SystemExit(f"ABORTA: falta {ruta}")
    html = ruta.read_text(encoding="utf-8")

    if ".mapa-estacional {" in html:
        print(f"SALTA  {ruta.name}: ya trae el componente")
        continue

    html = una_vez(html, ANCLA_CSS,
                   ANCLA_CSS.replace("  </style>", css + "\n  </style>"),
                   f"{nombre}/CSS")
    html = una_vez(html, ANCLA_JS,
                   ANCLA_JS + "\n" + js + "\n" + REGISTROS[nombre],
                   f"{nombre}/JS")
    html = una_vez(html, "        iniciarCiclos();\n",
                   "        iniciarCiclos();\n        iniciarMapasEstacionales();\n",
                   f"{nombre}/arranque")

    inst = INSTANCIAS[nombre]
    bloque = mapa_estacional_html(inst["id"], inst["titulo"], inst["nota"],
                                  sangria=inst["sangria"])
    html = una_vez(html, inst["ancla"],
                   (bloque + "\n" + inst["ancla"]) if inst["antes"]
                   else (inst["ancla"] + "\n" + bloque),
                   f"{nombre}/instancia")

    fallos = comprueba_mapa_estacional(html, inst["id"])
    for pieza, esperadas in [(".mapa-estacional {", 1), (".mapa-estacional-rejilla {", 2),
                             (".mapa-estacional-celda {", 2), (".mapa-estacional-nota {", 1),
                             ("function pintarMapaEstacional", 1),
                             ("function matrizMesAnio", 1),
                             ("function iniciarMapasEstacionales", 1),
                             ("        iniciarMapasEstacionales();", 1),
                             (f"MAPAS_ESTACIONALES['{inst['id']}']", 1)]:
        if html.count(pieza) != esperadas:
            fallos.append(f"'{pieza}' aparece {html.count(pieza)} veces, "
                          f"se esperaban {esperadas}")
    # Nada de lo que ya había puede haberse perdido
    for regla in [".ciclo-boton {", ".derivacion {", ".quiz {", ".simulador-lectura"]:
        if regla not in html:
            fallos.append(f"se perdió la regla CSS {regla}")
    if fallos:
        raise SystemExit(f"ABORTA [{nombre}]:\n  - " + "\n  - ".join(fallos))

    ruta.write_text(html, encoding="utf-8")
    print(f"OK     {ruta.name} ({len(html.encode('utf-8')) / 1024:.1f} KB) "
          f"· instancia '{inst['id']}'")

print("Listo.")
