#!/usr/bin/env python3
"""Instala el componente `.mapa-estacional` en el capítulo 1 y en la plantilla.

El capítulo 5 lo estrena y lo hereda por construcción (se ensambla desde el 4,
donde `ensambla_cap5.py` lo instala). Los capítulos 2, 3 y 4 no lo reciben: es
un componente para *ver* la estacionalidad, y ninguno de los tres la trata.

Sí lo reciben:
  - el **capítulo 1**, cuyo módulo 3 es justamente el de visualización estacional;
  - la **plantilla**, porque la regla del Checkpoint 0 exige que un componente
    nuevo entre en ella en la misma sesión.

Uso:  python3 retropropaga_mapa.py       (desde ensamblado/)

Es idempotente por abortar: si un archivo ya trae el componente, para.
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
