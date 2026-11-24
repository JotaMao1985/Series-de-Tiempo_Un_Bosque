"""R3 · correcciones tras el verificador en la fuente del deck (autorizadas por la sesión maestra):
«cuatro evidencias» → «cuatro comprobaciones» (V3), n_t → η_t como el capítulo (V3), y la nota de los
61 orígenes, cierta con las dos búsquedas de la armónica (V5). El título cambia solo después del
prefijo con que lo ancla `verifica_cifras_cap5.py` («La TRM es mensual y no tiene»): no hay que
reanclar nada."""

DECK = "Htmls_Series/diapositivas/fuentes/capitulo_5.md"


def registra(c, mover, entre, despues, esc, **_):
    c("deck · nota de la tabla del M1: cuatro comprobaciones", DECK,
      "El Módulo 8 vuelve sobre la TRM con cuatro evidencias.",
      "El Módulo 8 vuelve sobre la TRM con cuatro comprobaciones.")
    c("deck · título de la TRM: cuatro comprobaciones", DECK,
      "## La TRM es mensual y no tiene estacionalidad: cuatro evidencias coinciden",
      "## La TRM es mensual y no tiene estacionalidad: cuatro comprobaciones coinciden")
    c("deck · SARIMAX: η_t", DECK,
      r"$$y_t=\beta' x_t+n_t,\qquad n_t\sim\text{SARIMA}(p,d,q)(P,D,Q)_m$$",
      r"$$y_t=\beta' x_t+\eta_t,\qquad \eta_t\sim\text{SARIMA}(p,d,q)(P,D,Q)_m$$")
    c("deck · Fourier: η_t", DECK,
      r"\delta_k\cos\tfrac{2\pi kt}{m}\Big]+n_t$$",
      r"\delta_k\cos\tfrac{2\pi kt}{m}\Big]+\eta_t$$")
    c("deck · Fourier: η_t en la definición", DECK,
      r"<kbd>Definición</kbd> \(n_t\) es un ARIMA **no** estacional",
      r"<kbd>Definición</kbd> \(\eta_t\) es un ARIMA **no** estacional")
    c("deck · nota de los 61 orígenes: el orden tras el SARIMA, con las dos búsquedas", DECK,
      "El resto del orden apenas se mueve: ETS sobre el logaritmo por delante del STL y de la armónica; ETS sobre la cruda y *naïve*, últimos.",
      "Detrás del SARIMA, el ETS sobre el logaritmo, el STL y la armónica quedan cerca; ETS sobre la cruda y *naïve*, últimos. La armónica de los orígenes se busca por pasos; con la búsqueda exhaustiva de la partición baja a 21.06 y queda por delante del ETS sobre el logaritmo (21.42): entre esos dos, el orden depende de la búsqueda (capítulo, Módulo 11).")
    c("verificador del deck · el 21.06 nuevo de la nota, con su fuente en el JSON (claim nuevo; nada se relaja)",
      "Htmls_Series/diapositivas/fuentes/verificacion/verifica_cifras_cap5.py",
      '''C(K, "22.3847", R_("m11.om12.rmse_medio.armonica"))
''',
      '''C(K, "22.3847", R_("m11.om12.rmse_medio.armonica"))
C(K, "21.06", J_(OM + ".armonica_exhaustiva.rmse_medio_h12"))   # la armónica con búsqueda exhaustiva (R3, V5)
''')
