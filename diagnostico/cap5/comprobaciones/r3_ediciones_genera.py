"""R3 · `precalculo/genera_cap5.R`: las métricas de la comparativa del M11, también sin redondear.

La tabla ordenable del M11 pasa a ser la única que muestra las tres métricas de los ocho métodos, con
dos decimales. El JSON las traía redondeadas a tres, y redondear dos veces sube dos de ellas: el MAE
del ETS sobre el logaritmo (16.1249… → 16.125 → 16.13) y el RMSE del naïve estacional
(76.9946… → 76.995 → 77.00), cuando R —y el bloque nuevo del M11— dan 16.12 y 76.99. Se añade
`exactas` a cada método (y a la salvedad de la armónica, que usa la misma función); los campos que
ya existían no cambian."""

GEN = "precalculo/genera_cap5.R"


def registra(c, mover, entre, despues, esc, **_):
    registra_v(c)
    c("genera_cap5.R · metricas(): también sin redondear", GEN,
      '''metricas <- function(pred) {
  pred <- as.numeric(pred)
  e <- prueba_orig - pred
  list(rmse = round(sqrt(mean(e^2)), 3),
       mae  = round(mean(abs(e)), 3),
       mape = round(100 * mean(abs(e / prueba_orig)), 3))
}''',
      '''metricas <- function(pred) {
  pred <- as.numeric(pred)
  e <- prueba_orig - pred
  list(rmse = round(sqrt(mean(e^2)), 3),
       mae  = round(mean(abs(e)), 3),
       mape = round(100 * mean(abs(e / prueba_orig)), 3),
       # Las mismas, sin redondear (el JSON guarda 8 cifras): la tabla ordenable del
       # módulo 11 las muestra con 2 decimales, y redondear dos veces (a 3 y luego a
       # 2) sube 16.1249 a 16.13 y 76.9946 a 77.00 (R3 de la Fase 5).
       exactas = list(rmse = sqrt(mean(e^2)), mae = mean(abs(e)),
                      mape = 100 * mean(abs(e / prueba_orig))))
}''')


def registra_v(c, **_):
    """Correcciones tras el verificador (V5 y V15)."""
    c("genera_cap5.R · «Naïve estacional», con diéresis como en la prosa (V15)", GEN,
      '''comp[["snaive"]] <- c(list(nombre = "Naive estacional", escala = "original", n_par = 0,''',
      '''comp[["snaive"]] <- c(list(nombre = "Naïve estacional", escala = "original", n_par = 0,''')
    c("genera_cap5.R · la armónica de los orígenes, también con búsqueda exhaustiva (V5)", GEN,
      '''comparativa$origen_movil <- origen_movil
''',
      '''comparativa$origen_movil <- origen_movil

# La armónica de los orígenes se busca por pasos (el valor por defecto de
# auto.arima), por tiempo; la de la partición y la del módulo 10, con búsqueda
# exhaustiva. Con la exhaustiva también aquí, su RMSE medio a h = 12 queda por
# delante del ETS sobre el logaritmo: el capítulo lo dice con estas cifras (R3 de
# la Fase 5, hallazgo V5 del verificador). Tarda minuto y medio.
err_arm_ex <- list(); err_sar_24 <- list()
for (o in origenes) {
  h_o   <- min(24, n_ap - o)
  e_log <- window(ap, end = time(ap)[o])
  obs   <- as.numeric(ap_bruta)[o + seq_len(h_o)]
  p_ex  <- desde_log(forecast(auto.arima(e_log, xreg = fourier(e_log, K = 6), seasonal = FALSE,
                                         stepwise = FALSE, approximation = FALSE),
                              xreg = fourier(e_log, K = 6, h = h_o))$mean)
  err_arm_ex[[length(err_arm_ex) + 1]] <- obs - p_ex
  err_sar_24[[length(err_sar_24) + 1]] <- obs - pronosticadores$sarima(e_log, NULL, h_o)
}
r12_ex  <- vapply(err_arm_ex, function(e) sqrt(mean(e[1:12]^2)), numeric(1))
con24   <- origenes <= n_ap - 24
r24_ex  <- vapply(err_arm_ex[con24], function(e) sqrt(mean(e^2)), numeric(1))
r24_sar <- vapply(err_sar_24[con24], function(e) sqrt(mean(e^2)), numeric(1))
comparativa$origen_movil$armonica_exhaustiva <- list(
  rmse_medio_h12 = round(mean(r12_ex), 3),
  porcentaje_gana_al_sarima_h12 = round(100 * mean(r12_ex < errores_om[["sarima"]]), 1),
  n_origenes_h24 = sum(con24),
  rmse_medio_h24 = round(mean(r24_ex), 3),
  porcentaje_gana_al_sarima_h24 = round(100 * mean(r24_ex < r24_sar), 1),
  error_mes12_abs = round(mean(vapply(err_arm_ex, function(e) abs(e[12]), numeric(1))), 3),
  nota = paste("La armónica de los orígenes con la búsqueda exhaustiva de la partición",
               "(stepwise = FALSE, approximation = FALSE), en lugar de por pasos."))
cat(sprintf("   Armónica con búsqueda exhaustiva en los orígenes: RMSE medio h = 12 %.3f (gana al SARIMA en %.1f %%), h = 24 %.3f, mes 12 %.3f\\n",
            mean(r12_ex), 100 * mean(r12_ex < errores_om[["sarima"]]), mean(r24_ex),
            mean(vapply(err_arm_ex, function(e) abs(e[12]), numeric(1)))))
''')
