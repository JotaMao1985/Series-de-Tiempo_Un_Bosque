"""Constructor del HTML del componente `.mapa-estacional`.

Igual que `ciclo_html.py`: una sola función genera el marcado de todas las
instancias del proyecto, para que la plantilla y los capítulos tengan
exactamente la misma estructura y la comparación de selectores CSS no
encuentre diferencias.

El contenido de la rejilla lo pinta el JavaScript desde
`MAPAS_ESTACIONALES['<id_base>']`; aquí solo va el andamiaje.
"""


def mapa_estacional_html(id_base, titulo, nota="", sangria="      ",
                         etiqueta_aria=None):
    """Devuelve el HTML de un `.mapa-estacional` completo, ya sangrado.

    `nota` es el párrafo bajo la leyenda; puede quedar vacío y rellenarlo el
    JS (los mapas que dependen de un control cambian de nota al repintarse).
    """
    if not id_base:
        raise ValueError("un mapa estacional necesita un id")

    s = sangria
    aria = etiqueta_aria or titulo
    lineas = [
        f'{s}<div class="mapa-estacional" data-mapa="{id_base}">',
        f'{s}  <p class="mapa-estacional-titulo">{titulo}</p>',
        f'{s}  <div class="mapa-estacional-marco">',
        f'{s}    <div class="mapa-estacional-rejilla" role="table" '
        f'aria-label="{aria}"></div>',
        f'{s}  </div>',
        f'{s}  <div class="mapa-estacional-leyenda"></div>',
        f'{s}  <p class="mapa-estacional-nota">{nota}</p>',
        f'{s}</div>',
    ]
    return "\n".join(lineas) + "\n"


def comprueba_mapa_estacional(html, id_base):
    """Aserciones sobre una instancia ya insertada en un documento.

    Comprueba el andamiaje interno, no solo el contenedor: `pintarMapa-
    Estacional()` sale sin hacer nada si falta la rejilla, y el componente se
    vería vacío sin lanzar ningún error — exactamente la clase de fallo
    silencioso que ya costó una sesión con el `.quiz`.
    """
    fallos = []
    if f'data-mapa="{id_base}"' not in html:
        fallos.append(f"falta el contenedor data-mapa={id_base}")
        return fallos

    inicio = html.index(f'data-mapa="{id_base}"')
    fin = html.find("</div>", html.find("mapa-estacional-nota", inicio))
    bloque = html[inicio:fin if fin > inicio else inicio + 1200]
    for clase in ("mapa-estacional-titulo", "mapa-estacional-marco",
                  "mapa-estacional-rejilla", "mapa-estacional-leyenda",
                  "mapa-estacional-nota"):
        if clase not in bloque:
            fallos.append(f"{id_base}: falta {clase}")
    if 'role="table"' not in bloque:
        fallos.append(f"{id_base}: la rejilla no declara role=table")
    return fallos
