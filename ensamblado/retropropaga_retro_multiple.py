#!/usr/bin/env python3
"""Retropropaga la retroalimentación por opción en las preguntas `multiple`.

**El problema.** La regla del formato dice que cada opción de una pregunta lleva
su propia retroalimentación, *también las incorrectas*: explicar dónde falla el
razonamiento vale más que decir «incorrecto». En las preguntas de tipo `opcion` y
`grafico` así era. En las de tipo `multiple`, no: `renderAutoevaluacion()` solo
usaba el `retro` de las opciones **correctas**, y encima solo como respaldo
cuando faltaba `retroAcierto`. Quien fallaba una `multiple` veía un comentario
general y **nunca sabía en qué opción concreta se había equivocado**.

Lo que hace visible el fallo: los capítulos 5 y 6 ya tienen **15 explicaciones
escritas** en las opciones de sus preguntas `multiple`, y el estudiante no ha
visto ninguna. Estaban en el archivo, sin camino hasta la pantalla.

**La corrección**, en tres sustituciones por archivo:

1. **CSS** — reglas `.quiz-retro ul` / `li` con `color: inherit`. Sin ellas, la
   regla global `ul li { color: #374151 }` (pensada para las listas del
   contenido) pisa el color de `.quiz-retro.bien/.mal` y el desglose sale gris
   sobre fondo rojo o verde. Es el mismo fallo que ya se corrigió en el pie de
   página, y por eso `.quiz-resumen ul` tiene su propia regla.
2. **JS** — la función `desgloseMultiple()`, que arma la lista de opciones mal
   juzgadas (la que sobra y la que falta) con el `retro` de cada una.
3. **JS** — la rama de segundo fallo pasa ese desglose a `cerrar()`.

Alcance: los 6 capítulos publicados y la plantilla. **El camino de acierto no se
toca**: acertar una `multiple` significa haber juzgado bien todas las opciones,
así que no queda nada que explicar.

Aborta si un archivo ya está corregido, así que es seguro reejecutarlo por error
pero NO es reejecutable: está escrito contra el estado anterior.

Origen: auditoría de la Fase 0 del material de Diseño de Experimentos
(2026-07-30), que heredó esta plantilla. Corregido allí primero y retropropagado
aquí en la misma sesión, como manda la regla de homogeneidad.

Uso:  python3 retropropaga_retro_multiple.py       (desde ensamblado/)
"""

import glob
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
HTMLS = RAIZ / "Htmls_Series"
PLANTILLA = RAIZ / "plantilla" / "plantilla-capitulo.html"

# ---------------------------------------------------------------------------
# 1. CSS
# ---------------------------------------------------------------------------
CSS_ANCLA = """    .quiz-retro[hidden] {
      display: none;
    }
"""

CSS_NUEVO = CSS_ANCLA + """
    /* Desglose por opción dentro de la retroalimentación (preguntas de
       selección múltiple). La regla global `ul li { color: #374151 }`, pensada
       para las listas del contenido, pisaba el color de .quiz-retro.bien/.mal y
       dejaba el desglose en gris sobre fondo rojo o verde: el mismo fallo que ya
       se corrigió en el pie de página. `color: inherit` lo devuelve al color de
       la caja. */
    .quiz-retro ul {
      margin: 0.5rem 0 0 0;
      padding-left: 1.1rem;
    }

    .quiz-retro ul li {
      color: inherit;
      margin-bottom: 0.35rem;
    }

    .quiz-retro ul li:last-child {
      margin-bottom: 0;
    }
"""

# ---------------------------------------------------------------------------
# 2. El ayudante `desgloseMultiple`, justo antes de `mostrarPista`
# ---------------------------------------------------------------------------
JS_ANCLA = "      function mostrarPista(i, bloque) {"

JS_NUEVO = """      // Desglose por opción de una pregunta de selección múltiple: explica CADA
      // opción que el estudiante juzgó mal —la que marcó de más y la que se
      // dejó—, usando el `retro` de esa opción.
      //
      // Antes solo se mostraba el `retro` de las opciones CORRECTAS, y solo como
      // respaldo cuando no había `retroAcierto`: quien fallaba una `multiple`
      // veía un comentario general y nunca sabía en qué opción concreta se
      // equivocó. Contradecía la regla del formato («cada opción lleva su propia
      // retroalimentación, también las incorrectas»). Corregido el 2026-07-30.
      function desgloseMultiple(p, marcadas, correctas) {
        const filas = p.opciones.map((op, j) => {
          const marcada = marcadas.has(j);
          const esCorrecta = correctas.has(j);
          if (marcada === esCorrecta) return null;   // esa opción la juzgó bien
          const etiqueta = marcada ? 'La marcaste y no va' : 'Te faltó marcarla';
          // El texto de la opción ya trae su punto final, así que la retro se
          // concatena con un espacio: con dos puntos saldría «... JSON.: El ...».
          return `<li><strong>${etiqueta}:</strong> ${op.texto}` +
            `${op.retro ? ` ${op.retro}` : ''}</li>`;
        }).filter(Boolean);
        return filas.length ? `<ul>${filas.join('')}</ul>` : '';
      }

""" + JS_ANCLA

# ---------------------------------------------------------------------------
# 3. La llamada de la rama de segundo fallo
# ---------------------------------------------------------------------------
LLAMADA_VIEJA = """              boton.disabled = true;
              cerrar(i, bloque, false, p.retroFallo);"""

LLAMADA_NUEVA = """              boton.disabled = true;
              cerrar(i, bloque, false,
                (p.retroFallo || '') + desgloseMultiple(p, marcadas, correctas));"""


def una_vez(texto, viejo, nuevo, etiqueta, archivo):
    n = texto.count(viejo)
    if n != 1:
        raise SystemExit(f"ABORTA [{archivo} / {etiqueta}]: el marcador aparece "
                         f"{n} veces, se esperaba 1.\n  {viejo[:90]!r}")
    return texto.replace(viejo, nuevo, 1)


def corrige(ruta):
    nombre = ruta.name
    texto = ruta.read_text(encoding="utf-8")

    if "desgloseMultiple" in texto:
        raise SystemExit(f"ABORTA [{nombre}]: ya está corregido. "
                         "Este script no es reejecutable.")
    if "tipo: 'multiple'" not in texto:
        print(f"  {nombre}: sin preguntas 'multiple', se omite")
        return False

    texto = una_vez(texto, CSS_ANCLA, CSS_NUEVO, "CSS", nombre)
    texto = una_vez(texto, JS_ANCLA, JS_NUEVO, "ayudante JS", nombre)
    texto = una_vez(texto, LLAMADA_VIEJA, LLAMADA_NUEVA, "llamada de fallo", nombre)

    # Comprobaciones de que el resultado contiene lo que debe
    faltan = [q for q in (".quiz-retro ul {", "color: inherit;",
                          "function desgloseMultiple(", "desgloseMultiple(p, marcadas, correctas)")
              if q not in texto]
    if faltan:
        raise SystemExit(f"ABORTA [{nombre}]: falta en el resultado: {faltan}")
    if texto.count("function desgloseMultiple(") != 1:
        raise SystemExit(f"ABORTA [{nombre}]: el ayudante quedó duplicado.")

    ruta.write_text(texto, encoding="utf-8")
    n_mult = texto.count("tipo: 'multiple'")
    print(f"  {nombre}: corregido ({n_mult} pregunta(s) 'multiple')")
    return True


def main():
    objetivos = [PLANTILLA] + [Path(p) for p in sorted(glob.glob(str(HTMLS / "capitulo-*.html")))]
    faltantes = [o for o in objetivos if not o.exists()]
    if faltantes:
        raise SystemExit(f"ABORTA: no existen {faltantes}")

    print(f"Retropropagando la retroalimentación por opción a {len(objetivos)} archivos:\n")
    n = sum(corrige(o) for o in objetivos)
    print(f"\n{n} archivos corregidos.")
    print("Recuerda: los capítulos 1–4 y la plantilla aún tienen opciones sin "
          "`retro` en sus preguntas 'multiple'; el desglose dirá cuáles falló, "
          "pero no por qué, hasta que se escriban.")


if __name__ == "__main__":
    main()
