"""R1 del capítulo 3 · reaplica sobre HEAD las ediciones de precalculo/genera_cap3.R y
de precalculo/genera_soluciones.R (solo el ejercicio 3 del capítulo 3).
Cada sustitución debe aparecer exactamente una vez. Uso (desde la raíz del repo, con los
dos guiones como en HEAD):
  python3 diagnostico/cap3/comprobaciones/r1_edita_generador.py
y después:  (cd precalculo && Rscript genera_cap3.R && Rscript genera_soluciones.R)
"""
import pathlib, sys
RAIZ = pathlib.Path(__file__).resolve().parents[3]
p = RAIZ / "precalculo" / "genera_cap3.R"
CAMBIOS = [
# 1. auto.arima: además de la búsqueda exhaustiva, la llamada por defecto
('''ma1_ret  <- arima(ret, order = c(0, 0, 1), method = "ML")
auto_ret <- auto.arima(ret, d = 0, seasonal = FALSE, stepwise = FALSE,
                       approximation = FALSE, max.p = 4, max.q = 4)
''',
'''ma1_ret  <- arima(ret, order = c(0, 0, 1), method = "ML")
# El MA(1) SIN media: es el que devuelve la búsqueda exhaustiva de auto.arima.
ma1_sm_ret <- arima(ret, order = c(0, 0, 1), include.mean = FALSE, method = "ML")
# auto.arima con sus argumentos por defecto (lo que corre quien copia la
# llamada sin más) y con la búsqueda exhaustiva. NO dan lo mismo: la primera
# devuelve ruido blanco con media cero; la segunda, un MA(1) con media cero.
auto_def <- auto.arima(ret)
auto_ret <- auto.arima(ret, d = 0, seasonal = FALSE, stepwise = FALSE,
                       approximation = FALSE, max.p = 4, max.q = 4)
'''),
# 2. el comentario y los campos del MA(1) sin media
('''    # auto.arima devuelve un MA(1) SIN media. No es un capricho: la media mensual
    # estimada tiene t = 0.84, y al quitarla el AICc mejora. Comparados en igualdad
    # de condiciones (los dos sin media), el MA(1) y el ruido blanco puro se
    # distinguen en una centésima de AICc: son indistinguibles.
    sin_media = list(
''',
'''    # La búsqueda exhaustiva de auto.arima devuelve un MA(1) SIN media, y la
    # llamada por defecto, ruido blanco sin media. La media mensual estimada
    # tiene t = 0.84, y al quitarla el AICc mejora (el AICc SÍ compara modelos
    # con y sin media: se ajustan a los mismos datos). Sin media, el MA(1) y el
    # ruido blanco puro se distinguen en una centésima de AICc.
    sin_media = list(
      ma1_theta = round(coef(ma1_sm_ret)[["ma1"]], 4),
      ma1_se    = round(sqrt(ma1_sm_ret$var.coef[1, 1]), 4),
      ma1_t     = round(coef(ma1_sm_ret)[["ma1"]] / sqrt(ma1_sm_ret$var.coef[1, 1]), 3),
'''),
('''    auto_arima = list(
      orden = as.integer(arimaorder(auto_ret)),
      aicc  = round(as.numeric(auto_ret$aicc), 3),
      incluye_media = "intercept" %in% names(coef(auto_ret))
    ),
''',
'''    auto_arima = list(
      argumentos = "d = 0, seasonal = FALSE, stepwise = FALSE, approximation = FALSE, max.p = 4, max.q = 4",
      orden = as.integer(arimaorder(auto_ret)),
      aicc  = round(as.numeric(auto_ret$aicc), 3),
      incluye_media = "intercept" %in% names(coef(auto_ret))
    ),
    auto_arima_defecto = list(
      argumentos = "(los de auto.arima por defecto)",
      orden = as.integer(arimaorder(auto_def)[c("p", "d", "q")]),
      aicc  = round(as.numeric(auto_def$aicc), 3),
      incluye_media = "intercept" %in% names(coef(auto_def))
    ),
'''),
# 3. el error de la ACF por pesos psi, también con los 600 términos del navegador
('''error_psi_global <- signif(max(sapply(verificacion, `[[`, "error_max")), 3)
''',
'''error_psi_global <- signif(max(sapply(verificacion, `[[`, "error_max")), 3)
# El navegador trunca en 600 términos, no en 2000: se mide también así.
error_psi_600 <- signif(max(sapply(catalogo, function(p) {
  exacta <- as.numeric(ARMAacf(ar = p$ar, ma = p$ma, lag.max = MAX_REZAGO_T))[-1]
  max(abs(exacta - acf_por_psi(p$ar, p$ma, MAX_REZAGO_T, n_terminos = 600)))
})), 3)
'''),
('''    por_proceso = verificacion,
    error_max = error_psi_global
''',
'''    por_proceso = verificacion,
    error_max = error_psi_global,
    error_max_600_terminos = error_psi_600
'''),
# 4. el resumen por consola
('''cat(sprintf("auto.arima(d=0) propone ARMA(%d,%d) y SIN media (incluye media: %s)\\n",
            retornos$auto_arima$orden[1], retornos$auto_arima$orden[3],
            retornos$auto_arima$incluye_media))
''',
'''cat(sprintf("auto.arima(ret) por defecto propone ARMA(%d,%d) (incluye media: %s)\\n",
            retornos$auto_arima_defecto$orden[1], retornos$auto_arima_defecto$orden[3],
            retornos$auto_arima_defecto$incluye_media))
cat(sprintf("auto.arima(%s) propone ARMA(%d,%d) (incluye media: %s)\\n",
            retornos$auto_arima$argumentos,
            retornos$auto_arima$orden[1], retornos$auto_arima$orden[3],
            retornos$auto_arima$incluye_media))
cat(sprintf("   MA(1) sin media: theta = %.4f (e.e. %.4f, t = %.2f)\\n",
            retornos$sin_media$ma1_theta, retornos$sin_media$ma1_se, retornos$sin_media$ma1_t))
'''),
('''cat("   -> comparados en igualdad de condiciones son INDISTINGUIBLES.\\n")
''',
'''cat("   -> sin media, el MA(1) y el ruido blanco son INDISTINGUIBLES.\\n")
'''),
('''cat("Error maximo de la ACF teorica por pesos psi vs. ARMAacf:", error_psi_global, "\\n")
''',
'''cat("Error maximo de la ACF teorica por pesos psi vs. ARMAacf:", error_psi_global,
    "(2000 terminos) |", error_psi_600, "(600 terminos, los del navegador)\\n")
'''),
]
SOLUCIONES = [
("""# Tres lecturas distintas: coeficientes estables, periodo sensible y
# diagnostico que se derrumba al crecer n (la prueba gana potencia).
""",
"""# Tres lecturas distintas: coeficientes estables, periodo sensible y un
# diagnostico que se derrumba en las ventanas que llegan al siglo XX. NO es
# cuestion de potencia: 1889-1988 tiene la misma n que 1770-1869 y rechaza.
"""),
("""ventanas <- list(c(1770, 1869), c(1700, 1988), c(1870, 1988), c(1900, 1988))
""",
"""ventanas <- list(c(1770, 1869), c(1700, 1988), c(1870, 1988), c(1900, 1988),
                 c(1889, 1988))
"""),
("""  rango_periodo = round(range(tabla_vent$periodo), 3),
  nota = paste("Los coeficientes apenas se mueven, el periodo cae de 11.22 a",
               "10.13 anios y el diagnostico falla fuera de la ventana de Yule",
               "porque la prueba gana potencia con n, no porque el modelo empeore.")
)
""",
"""  rango_periodo = round(range(tabla_vent$periodo), 3),
  # Cuantas de las ventanas de 100 anios que caben en 1700-1988 pasan la prueba
  cien_anios = local({
    ini <- 1700:1889
    p <- sapply(ini, function(a) {
      x <- sqrt(window(sunspot.year, a, a + 99))
      Box.test(residuals(arima(x, order = c(2, 0, 0), method = "ML")), lag = 12,
               type = "Ljung-Box", fitdf = 2)$p.value
    })
    list(ventanas = length(ini), no_rechazan = sum(p > 0.05),
         inicios_no_rechazan = ini[p > 0.05])
  }),
  nota = paste("Los coeficientes apenas se mueven, el periodo cae de 11.22 a",
               "10.13 anios y el diagnostico falla en las ventanas que llegan al",
               "siglo XX, con n = 89, 100, 119 o 289: no es cuestion de potencia.")
)
"""),
("""print(tabla_vent, row.names = FALSE)
""",
"""print(tabla_vent, row.names = FALSE)
cat(sprintf("  ventanas de 100 anios: %d; no rechazan al 5 %%: %d (una empieza en 1700; las demas, entre %s)\\n",
            sol$cap3_ej3$cien_anios$ventanas, sol$cap3_ej3$cien_anios$no_rechazan,
            paste(range(sol$cap3_ej3$cien_anios$inicios_no_rechazan[-1]), collapse = "-")))
"""),
]


def aplica(ruta, cambios):
    s = ruta.read_text(encoding="utf-8")
    for i, (a, b) in enumerate(cambios, 1):
        n = s.count(a)
        if n != 1:
            sys.exit(f"{ruta.name}, cambio {i}: el texto original aparece {n} veces (se esperaba 1)")
        s = s.replace(a, b)
    ruta.write_text(s, encoding="utf-8")
    print(f"{len(cambios)} sustituciones aplicadas a {ruta.relative_to(RAIZ)}")


aplica(p, CAMBIOS)
aplica(RAIZ / "precalculo" / "genera_soluciones.R", SOLUCIONES)
