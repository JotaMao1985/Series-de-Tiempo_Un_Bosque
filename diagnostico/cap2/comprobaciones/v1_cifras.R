# Verificador independiente · R1 del cap. 2 · cifras nuevas o cambiadas en la prosa
suppressMessages({library(tseries); library(forecast); library(urca); library(jsonlite)})
options(digits = 10)
raiz <- normalizePath(file.path(dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE))), "..", "..", ".."))
cat("R", R.version$major, R.version$minor, "· tseries", as.character(packageVersion("tseries")),
    "· forecast", as.character(packageVersion("forecast")), "· urca", as.character(packageVersion("urca")), "\n")

cat("\n== TRM: CSV publicado frente a datos_series.json ==\n")
csv <- read.csv(file.path(raiz, "Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv"))
js  <- fromJSON(file.path(raiz, "precalculo/salidas/datos_series.json"))
str(js$trm[setdiff(names(js$trm), "valores")])
cat("n csv", nrow(csv), " n json", length(js$trm$valores), "\n")
cat("max |csv - json|:", max(abs(csv$trm - as.numeric(js$trm$valores))), "\n")
cat("identicos:", identical(csv$trm, as.numeric(js$trm$valores)), "\n")
cat("meses csv:", csv$mes[1], "...", tail(csv$mes, 1), "; consecutivos:",
    all(diff(as.integer(substr(csv$mes,1,4))*12 + as.integer(substr(csv$mes,6,7))) == 1), "\n")
trm <- ts(csv$trm, start = c(2015, 1), frequency = 12)

cat("\n== M6: cifras de la TRM sin redondear ==\n")
a <- adf.test(trm); print(c(a$statistic, p = a$p.value))
k <- kpss.test(diff(trm)); print(c(k$statistic, p = k$p.value))
kt  <- suppressWarnings(kpss.test(trm, null = "Trend")); print(c(kt$statistic, p = kt$p.value))
ktd <- suppressWarnings(kpss.test(diff(trm), null = "Trend")); print(c(ktd$statistic, p = ktd$p.value))
ad <- adf.test(diff(trm)); print(c(ad$statistic, p = ad$p.value))

cat("\n== M6: AirPassengers y log, con k = 5 y k = 12, sin redondear ==\n")
for (s in list(list("AP", AirPassengers), list("logAP", log(AirPassengers))))
  for (kk in c(5, 12)) { r <- suppressWarnings(adf.test(s[[2]], k = kk)); cat(s[[1]], "k =", kk, ":", r$statistic, r$p.value, "\n") }

cat("\n== M3: AR(1) phi = 0.5 sobre el ruido de set.seed(2026) ==\n")
set.seed(2026); e <- rnorm(200)
ar1 <- function(phi, e) { y <- numeric(length(e)); y[1] <- e[1]; for (t in 2:length(e)) y[t] <- phi*y[t-1] + e[t]; y }
r <- acf(ar1(0.5, e), lag.max = 24, plot = FALSE)$acf[-1]
print(round(r[1:6], 4)); cat("banda", 1.96/sqrt(200), " fuera:", which(abs(r) > 1.96/sqrt(200)), "\n")
cat("r1 ruido:", acf(e, plot = FALSE)$acf[2], "\n")
cat("json ruido_blanco identico a rnorm(2026)?\n")
d2 <- fromJSON(file.path(raiz, "precalculo/salidas/cap2_estacionariedad.json"))
cat(" claves:", paste(head(names(d2), 30), collapse = " "), "\n")

cat("\n== M7: AR(1) phi = 0.8, set.seed(1), n = 200 ==\n")
set.seed(1); y <- arima.sim(list(ar = 0.8), n = 200)
cat("ndiffs:", ndiffs(y), " var:", var(y), var(diff(y)), " r1(diff):", acf(diff(y), plot = FALSE)$acf[2], "\n")
cat("ndiffs con test adf/pp:", ndiffs(y, test = "adf"), ndiffs(y, test = "pp"), "\n")
cat("teoria: 2(1-rho1) =", 2*(1-0.8), " razon muestral:", var(diff(y))/var(y), "\n")

cat("\n== M7: recuadro, d12 = diff(log AP, 12) ==\n")
lx <- log(AirPassengers); d12 <- diff(lx, lag = 12); n12 <- length(d12)
r12 <- acf(d12, lag.max = 24, plot = FALSE)$acf[-1]
cat("n", n12, " banda", 1.96/sqrt(n12), "\n"); print(round(r12[1:12], 4))
cat("rezagos fuera:", which(abs(r12) > 1.96/sqrt(n12)), "\n")
cat("var d12", var(d12), " var diff(d12)", var(diff(d12)), " r1 diff(d12)", acf(diff(d12), plot = FALSE)$acf[2], "\n")
cat("nsdiffs(lx)", nsdiffs(lx), " ndiffs(d12)", ndiffs(d12), " ndiffs(diff(d12))", ndiffs(diff(d12)), " nsdiffs(diff(d12))", nsdiffs(diff(d12)), "\n")
kd <- kpss.test(d12); print(c(kd$statistic, p = kd$p.value))
cat("trunc(3*sqrt(132)/13) =", trunc(3*sqrt(132)/13), " ur.kpss lags=2:", ur.kpss(d12, use.lag = 2)@teststat, "\n")
d1 <- diff(lx); cat("r12 de d1:", acf(d1, lag.max = 12, plot = FALSE)$acf[13], " ndiffs(d1)", ndiffs(d1), " nsdiffs(d1)", nsdiffs(d1), "\n")
k1 <- suppressWarnings(kpss.test(d1)); cat("kpss d1 p:", k1$p.value, "\n")
cat("varianzas lx por d:", sapply(0:3, function(d) if (d == 0) var(lx) else var(diff(lx, differences = d))), "\n")

cat("\n== Contraejemplo a «si la varianza sube, la diferencia sobraba» ==\n")
cat("ARIMA(0,1,1) y_t = y_{t-1} + e_t + theta e_{t-1}: una raiz unitaria de verdad\n")
for (th in c(-0.5, -0.7, -0.8, -0.9)) {
  set.seed(2026)
  res <- t(replicate(500, { y <- arima.sim(list(order = c(0,1,1), ma = th), n = 143)
                            c(var(diff(y)) > var(y), ndiffs(y)) }))
  cat(sprintf("theta = %.1f, n = 144: la varianza SUBE al diferenciar en %.1f %% de 500 series; ndiffs = 1 en %.1f %%; de las que suben, ndiffs = 1 en %.1f %%\n",
              th, 100*mean(res[,1]), 100*mean(res[,2] == 1), 100*mean(res[res[,1] == 1, 2] == 1)))
}
set.seed(7); y <- arima.sim(list(order = c(0,1,1), ma = -0.8), n = 143)
cat("Un caso: var(y) =", var(y), " var(diff y) =", var(diff(y)), " ndiffs =", ndiffs(y), "\n")

cat("\n== Ej. 2 y Monte Carlo del M6 ==\n")
mc <- d2$trampa_estacionalidad$montecarlo; str(mc[setdiff(names(mc), "resultados")]); print(mc$resultados)

cat("\n== Ej. 3: USAccDeaths, r1 sin redondear ==\n")
cat(acf(USAccDeaths, plot = FALSE)$acf[2], "\n")

cat("\n== Ej. 4: ventana desde 2022 ==\n")
w <- window(trm, start = c(2022, 1)); cat(length(w), adf.test(w)$p.value, "\n")
cat("p de la TRM con 3 decimales:", round(c(adf.test(trm)$p.value, adf.test(diff(trm))$p.value), 3), "\n")

cat("\n== M8: variantes con signo ==\n")
print(BoxCox(c(-2, 4), 0.5)); print(fabletools::box_cox(c(-2, 4), 0.5)); print(fabletools::box_cox(c(-2, 4), -0.5))
print(body(forecast::BoxCox))
cat("Guerrero anual por defecto (Nile):", BoxCox.lambda(Nile, method = "guerrero"), "\n")
print(formals(forecast:::guerrero))

cat("\n== Quiz P3: d_log_airpassengers ==\n")
rd <- acf(d1, lag.max = 24, plot = FALSE)$acf[-1]; cat("n", length(d1), "banda", 1.96/sqrt(length(d1)), "fuera:", which(abs(rd) > 1.96/sqrt(length(d1))), "(", sum(abs(rd) > 1.96/sqrt(length(d1))), ")\n")
