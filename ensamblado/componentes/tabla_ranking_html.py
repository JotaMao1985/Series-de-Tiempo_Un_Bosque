"""Constructor del HTML del componente `.tabla-ranking`.

Igual que `ciclo_html.py` y `mapa_estacional_html.py`: una sola función genera
el marcado de todas las instancias del proyecto, para que la plantilla y los
capítulos tengan exactamente la misma estructura y la comparación de selectores
CSS no encuentre diferencias.

El contenido de la tabla lo pinta el JavaScript desde `TABLAS_RANKING['<id>']`;
aquí solo va el andamiaje. El `<table>` se construye entero en JS porque el
número de columnas y el orden cambian con cada pulsación de cabecera.
"""


def tabla_ranking_html(id_base, titulo, pie="", sangria="      ",
                       etiqueta_aria=None):
    """Devuelve el HTML de una `.tabla-ranking` completa, ya sangrada.

    `pie` es el párrafo bajo la tabla; puede quedar vacío y rellenarlo el JS
    desde el campo `pie` del registro.
    """
    if not id_base:
        raise ValueError("una tabla de ranking necesita un id")

    s = sangria
    aria = etiqueta_aria or titulo
    lineas = [
        f'{s}<div class="tabla-ranking" data-ranking="{id_base}">',
        f'{s}  <p class="tabla-ranking-titulo">{titulo}</p>',
        f'{s}  <div class="tabla-ranking-marco" aria-label="{aria}"></div>',
        f'{s}  <p class="tabla-ranking-estado" role="status" aria-live="polite"></p>',
        f'{s}  <p class="tabla-ranking-pie">{pie}</p>',
        f'{s}</div>',
    ]
    return "\n".join(lineas) + "\n"


def comprueba_tabla_ranking(html, id_base):
    """Aserciones sobre una instancia ya insertada en un documento.

    Comprueba el andamiaje interno, no solo el contenedor: `pintarTablaRanking()`
    sale sin hacer nada si falta el marco, y el componente se vería vacío sin
    lanzar ningún error — exactamente la clase de fallo silencioso que ya costó
    una sesión con el `.quiz`.
    """
    fallos = []
    if f'data-ranking="{id_base}"' not in html:
        fallos.append(f"falta el contenedor data-ranking={id_base}")
        return fallos

    inicio = html.index(f'data-ranking="{id_base}"')
    fin = html.find("</div>", html.find("tabla-ranking-pie", inicio))
    bloque = html[inicio:fin if fin > inicio else inicio + 1200]
    for clase in ("tabla-ranking-titulo", "tabla-ranking-marco",
                  "tabla-ranking-estado", "tabla-ranking-pie"):
        if clase not in bloque:
            fallos.append(f"{id_base}: falta {clase}")
    if 'role="status"' not in bloque:
        fallos.append(f"{id_base}: el anuncio de reordenación no declara role=status")
    if f"TABLAS_RANKING['{id_base}']" not in html:
        fallos.append(f"{id_base}: no está registrado en TABLAS_RANKING")
    return fallos
