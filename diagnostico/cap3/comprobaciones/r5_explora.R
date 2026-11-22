# R5 del capitulo 3 · exploracion previa: que series de datasets sirven para cada hueco.
# Antes de elegir se busco con grep -lw, en Htmls_Series/*.html, cada serie temporal de datasets:
#   cap. 1: AirPassengers, nottem, mdeaths, sunspots, UKgas, USAccDeaths, co2
#   cap. 2: AirPassengers, LakeHuron, UKgas, USAccDeaths, co2, nhtemp, discoveries, EuStockMarkets,
#           JohnsonJohnson, UKDriverDeaths
#   cap. 3: sunspot.year, lh (y la TRM)      cap. 4: Nile, BJsales, lynx (su ejercicio 2)
#   sin usar en ningun capitulo: WWWusage, treering, airmiles, austres, uspop, presidents,
#           ldeaths, fdeaths, freeny.y, sunspot.month, Seatbelts (y los data.frame con orden temporal)
# Se eligieron WWWusage (M5), treering (M7) y lynx (M9; ver R5_cambios.md, 7.1).
# Rscript diagnostico/cap3/comprobaciones/r5_explora.R > diagnostico/cap3/comprobaciones/r5_explora.out 2>&1
suppressMessages(library(forecast))
options(width = 110)
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
fuera <- function(v, n) which(abs(v) > 1.96/sqrt(n))
resumen <- function(x, nombre, lag = 20) {
  x <- as.numeric(x); n <- length(x)
  cat("\n=====", nombre, "| n =", n, "| banda", round(1.96/sqrt(n), 4), "\n")
  a <- acf(x, lag.max = lag, plot = FALSE)$acf[-1]; p <- as.numeric(pacf(x, lag.max = lag, plot = FALSE)$acf)
  cat("ACF fuera:", fuera(a, n), "\nACF 1-6:", round(a[1:6], 3), "\nPACF fuera:", fuera(p, n), "\nPACF 1-6:", round(p[1:6], 3), "\n")
  rej <- list(c(0,0), c(1,0), c(2,0), c(3,0), c(4,0), c(0,1), c(0,2), c(0,3), c(1,1), c(2,1), c(1,2), c(2,2))
  t <- do.call(rbind, lapply(rej, function(pq) {
    f <- tryCatch(arima(x, order = c(pq[1], 0, pq[2]), method = "ML"), error = function(e) NULL)
    if (is.null(f)) return(NULL)
    data.frame(m = sprintf("ARMA(%d,%d)", pq[1], pq[2]), AICc = round(aicc(f, n), 2), BIC = round(BIC(f), 2),
               LB = if (sum(pq) < 10) round(Box.test(residuals(f), lag = 10, type = "Ljung-Box", fitdf = sum(pq))$p.value, 4) else NA)
  }))
  print(t[order(t$AICc), ][1:6, ], row.names = FALSE)
  cat("min BIC:", t$m[which.min(t$BIC)], "\n")
}
elasticidad <- function(x, k) {
  g <- rep(seq_len(length(x) %/% k), each = k); x <- as.numeric(x)[seq_along(g)]
  niv <- tapply(x, g, mean); amp <- tapply(x, g, sd); aj <- lm(log(amp) ~ log(niv))
  round(c(b = coef(aj)[[2]], confint(aj)[2, ], R2 = summary(aj)$r.squared), 3)
}
resumen(diff(WWWusage), "diff(WWWusage)")
resumen(treering, "treering completa")
resumen(window(treering, start = 1880), "treering 1880-1979")
resumen(window(treering, start = 1780), "treering 1780-1979")
cat("treering elasticidad k=20:", elasticidad(treering, 20), " min:", min(treering), "\n")
resumen(airquality$Wind, "airquality$Wind")
resumen(airquality$Temp, "airquality$Temp")
resumen(beaver1$temp, "beaver1$temp"); resumen(beaver2$temp, "beaver2$temp")
resumen(diff(log(austres)), "diff(log(austres))")
resumen(diff(log(freeny.y)), "diff(log(freeny.y))")
resumen(diff(log(airmiles)), "diff(log(airmiles))")
pr <- na.interp(presidents); resumen(pr, "presidents (na.interp)")
resumen(ldeaths, "ldeaths", 24)
resumen(faithful$eruptions, "faithful$eruptions"); resumen(faithful$waiting, "faithful$waiting")
resumen(rivers, "rivers"); resumen(precip, "precip")
resumen(longley$Unemployed, "longley$Unemployed")

cat("\n\n######## M7: los tres estimadores sobre otras series ########\n")
tres <- function(x, p, nombre) {
  x <- as.numeric(x)
  yw <- ar(x, order.max = p, aic = FALSE, method = "yule-walker")
  css <- arima(x, order = c(p, 0, 0), method = "CSS"); ml <- arima(x, order = c(p, 0, 0), method = "ML")
  ee <- sqrt(diag(ml$var.coef))[1:p]
  cat("\n--", nombre, "| n =", length(x), "| AR(", p, ")\n")
  print(round(rbind(YW = yw$ar, CSS = coef(css)[1:p], ML = coef(ml)[1:p], ee_ML = ee,
                    `(YW-ML)/ee` = (yw$ar - coef(ml)[1:p]) / ee, `(CSS-ML)/ee` = (coef(css)[1:p] - coef(ml)[1:p]) / ee), 4))
  cat("sigma2: YW", round(yw$var.pred, 4), " CSS", round(css$sigma2, 4), " ML", round(ml$sigma2, 4),
      " | modulos de las raices (ML):", round(Mod(polyroot(c(1, -coef(ml)[1:p]))), 4), "\n")
}
tres(diff(WWWusage), 3, "diff(WWWusage)")
tres(treering, 2, "treering completa"); tres(window(treering, start = 1880), 2, "treering 1880-1979")
tres(window(treering, start = 1780), 1, "treering 1780-1979")
tres(log(lynx), 2, "log(lynx)")
tres(beaver1$temp, 1, "beaver1$temp"); tres(beaver2$temp, 1, "beaver2$temp")
tres(airquality$Temp, 1, "airquality$Temp"); tres(na.interp(presidents), 1, "presidents")
tres(faithful$waiting, 1, "faithful$waiting")

cat("\n\n######## M5: diff(WWWusage), AR(3) frente a ARMA(1,1) ########\n")
w <- diff(WWWusage); n <- length(w)
ar3 <- arima(w, order = c(3, 0, 0), method = "ML"); a11 <- arima(w, order = c(1, 0, 1), method = "ML")
print(ar3); print(a11)
a <- acf(w, lag.max = 20, plot = FALSE)$acf[-1]
print(round(rbind(muestral = a[1:8], AR3 = ARMAacf(ar = coef(ar3)[1:3], lag.max = 8)[-1],
                  ARMA11 = ARMAacf(ar = coef(a11)[1], ma = coef(a11)[2], lag.max = 8)[-1]), 3))
cat("auto.arima:", as.character(auto.arima(w)), "|", as.character(auto.arima(w, stepwise = FALSE, approximation = FALSE)), "\n")
cat("WWWusage: ndiffs", ndiffs(WWWusage), " rango", range(WWWusage), "\n")

cat("\n\n######## M9: lynx, cruda y en logaritmos ########\n")
cat("min:", min(lynx), " n:", length(lynx), "\n")
for (k in c(10, 19, 5)) cat("elasticidad k =", k, ":", elasticidad(lynx, k), "\n")
cat("Guerrero:", round(BoxCox.lambda(lynx, method = "guerrero"), 4), "\n")
resumen(lynx, "lynx cruda"); resumen(log(lynx), "log(lynx)"); resumen(sqrt(lynx), "sqrt(lynx)")
for (tr in list(identity, log, sqrt)) { x <- tr(lynx); f <- arima(x, order = c(2,0,0), method = "ML")
  cat(round(coef(f), 4), "| periodo", round(2*pi/Arg(polyroot(c(1, -coef(f)[1:2]))[1]), 3),
      "| LB12", round(Box.test(residuals(f), lag = 12, type = "Ljung-Box", fitdf = 2)$p.value, 4),
      "| LB10", round(Box.test(residuals(f), lag = 10, type = "Ljung-Box", fitdf = 2)$p.value, 4),
      "| LB20", round(Box.test(residuals(f), lag = 20, type = "Ljung-Box", fitdf = 2)$p.value, 4),
      "| Shapiro", round(shapiro.test(residuals(f))$p.value, 4), "\n") }
cat("PACF fuera cruda:", fuera(as.numeric(pacf(lynx, lag.max = 20, plot = FALSE)$acf), 114), "| log:", fuera(as.numeric(pacf(log(lynx), lag.max = 20, plot = FALSE)$acf), 114), "\n")
