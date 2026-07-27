"""Constructor del HTML del componente `.ciclo`.

Una sola función genera el marcado de todas las instancias del proyecto, para
que la plantilla y los cuatro capítulos tengan exactamente la misma estructura
y las comprobaciones de selectores CSS no encuentren diferencias.

Una etapa se declara así:

    {
        "clave":   "identificacion",           # sufijo del id del panel
        "numero":  "Etapa 1",                  # cintillo superior del botón
        "titulo":  "Identificación",
        "resumen": "¿Qué (p, d, q)?",
        "campos":  [("Qué haces", "<p>...</p>"), ("Con qué", "<p>...</p>")],
        "vuelta":  "<p>Vuelves aquí si ...</p>",   # opcional
    }
"""


def ciclo_html(id_base, etapas, retorno, sangria="      "):
    """Devuelve el HTML de un `.ciclo` completo, ya sangrado."""
    if not etapas:
        raise ValueError("un ciclo necesita al menos una etapa")

    s = sangria
    lineas = [f'{s}<div class="ciclo" data-ciclo="{id_base}">']
    lineas.append(f'{s}  <ol class="ciclo-etapas" role="tablist" '
                  f'aria-label="Etapas del ciclo">')

    for i, etapa in enumerate(etapas):
        panel_id = f"ciclo-{id_base}-{etapa['clave']}"
        seleccionado = "true" if i == 0 else "false"
        tabindex = "0" if i == 0 else "-1"
        lineas += [
            f'{s}    <li class="ciclo-etapa" role="presentation">',
            f'{s}      <button type="button" class="ciclo-boton" role="tab"',
            f'{s}        aria-selected="{seleccionado}" aria-controls="{panel_id}" '
            f'tabindex="{tabindex}">',
            f'{s}        <span class="ciclo-numero">{etapa["numero"]}</span>',
            f'{s}        <span class="ciclo-titulo">{etapa["titulo"]}</span>',
            f'{s}        <span class="ciclo-resumen">{etapa["resumen"]}</span>',
            f'{s}      </button>',
            f'{s}    </li>',
        ]

    lineas.append(f'{s}  </ol>')
    lineas.append(f'{s}  <p class="ciclo-retorno">{retorno}</p>')

    for i, etapa in enumerate(etapas):
        panel_id = f"ciclo-{id_base}-{etapa['clave']}"
        oculto = "" if i == 0 else " hidden"
        lineas.append(f'{s}  <div class="ciclo-panel" id="{panel_id}" '
                      f'role="tabpanel"{oculto}>')
        for etiqueta, contenido in etapa["campos"]:
            lineas.append(f'{s}    <div class="ciclo-campo">')
            lineas.append(f'{s}      <span class="ciclo-etiqueta">{etiqueta}</span>')
            for linea in contenido.strip().splitlines():
                lineas.append(f'{s}      {linea.strip()}')
            lineas.append(f'{s}    </div>')
        if etapa.get("vuelta"):
            lineas.append(f'{s}    <div class="ciclo-campo ciclo-vuelta">')
            lineas.append(f'{s}      <span class="ciclo-etiqueta">Qué te devuelve atrás</span>')
            for linea in etapa["vuelta"].strip().splitlines():
                lineas.append(f'{s}      {linea.strip()}')
            lineas.append(f'{s}    </div>')
        lineas.append(f'{s}  </div>')

    lineas.append(f'{s}</div>')
    return "\n".join(lineas) + "\n"


def comprueba_ciclo(html, id_base, n_etapas):
    """Aserciones sobre una instancia ya insertada en un documento."""
    fallos = []
    if f'data-ciclo="{id_base}"' not in html:
        fallos.append(f"falta el contenedor data-ciclo={id_base}")
    n_botones = html.count(f'aria-controls="ciclo-{id_base}-')
    n_paneles = html.count(f'id="ciclo-{id_base}-')
    if n_botones != n_etapas:
        fallos.append(f"{id_base}: {n_botones} botones, se esperaban {n_etapas}")
    if n_paneles != n_etapas:
        fallos.append(f"{id_base}: {n_paneles} paneles, se esperaban {n_etapas}")
    if n_botones != n_paneles:
        fallos.append(f"{id_base}: botones y paneles descuadrados")
    return fallos
