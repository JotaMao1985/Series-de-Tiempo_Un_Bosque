# R1 · T1.1 · Los bloques de media movil del M5 (R tidyverts) y del M6 (R base)
# calculan de verdad la 2x12. Cifra de control: julio de 1955 = 285.75.
# fpp3 no esta instalado en este equipo: se cargan los paquetes que fpp3 adjunta
# y que el bloque usa. El bloque publicado deja library(fpp3).
suppressPackageStartupMessages({
  library(tsibble); library(dplyr); library(ggplot2); library(fabletools); library(feasts)
})
AP <- AirPassengers

cat("== ANTES (lo publicado) ==\n")
cat("slide_dbl(.before=6,.after=6) = 13-MA, jul-1955:", stats::filter(AP, rep(1/13, 13))[79], "\n")
cat("stats::filter(y, rep(1/12,12)), jul-1955:", stats::filter(AP, rep(1/12, 12))[79],
    " NA:", sum(is.na(stats::filter(AP, rep(1/12, 12)))), "\n")

cat("\n== BLOQUE NUEVO DEL M5 (R) ==\n")
pasajeros <- as_tsibble(AirPassengers)
pasajeros <- pasajeros |>
  mutate(
    `12-MA`   = slider::slide_dbl(value, mean,
                  .before = 5, .after = 6, .complete = TRUE),
    tendencia = slider::slide_dbl(`12-MA`, mean,
                  .before = 1, .after = 0, .complete = TRUE)
  )
g <- pasajeros |>
  autoplot(value) +
  geom_line(aes(y = tendencia), colour = "#FF6600", linewidth = 1)
invisible(ggplot_build(g))   # el grafico se construye sin error
ctrl <- pasajeros |> filter(index == yearmonth("1955 Jul")) |> pull(tendencia)
cat("pasajeros |> filter(index == yearmonth('1955 Jul')) |> pull(tendencia):", ctrl, "\n")
na <- which(is.na(pasajeros$tendencia))
cat("NA en tendencia:", length(na), " posiciones:", na, "\n")
cat("NA en 12-MA:", sum(is.na(pasajeros$`12-MA`)), "\n")
dc <- decompose(AP, type = "multiplicative")
cat("max |tendencia - decompose()$trend|:", max(abs(pasajeros$tendencia - as.numeric(dc$trend)), na.rm = TRUE), "\n")

cat("\n== FILTRO DEL M6 (R base) ==\n")
m <- 12
f <- stats::filter(AP, c(0.5, rep(1, m - 1), 0.5) / m)
cat("stats::filter(y, c(0.5, rep(1, m - 1), 0.5) / m), jul-1955:", f[79], " NA:", sum(is.na(f)), "\n")
cat("max |filtro - decompose()$trend|:", max(abs(f - dc$trend), na.rm = TRUE), "\n")
cat("identical NA pattern:", identical(is.na(as.numeric(f)), is.na(as.numeric(dc$trend))), "\n")
cat("linea de decompose() que define el filtro:\n")
print(grep("filter <-|rep_len", deparse(body(decompose)), value = TRUE))
cat("\nVentana de julio de 1955 (ene-1955 a ene-1956):", AP[73:85], "\n")
cat("cuenta a mano de la 2x12:", (0.5 * AP[73] + sum(AP[74:84]) + 0.5 * AP[85]) / 12, "\n")
