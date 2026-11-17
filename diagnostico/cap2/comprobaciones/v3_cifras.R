# Verificador independiente de la R3 del capitulo 2: cada cifra nueva, rehecha.
# Rscript diagnostico/cap2/comprobaciones/v3_cifras.R > .../v3_cifras.out 2>&1
suppressPackageStartupMessages({library(forecast); library(tseries); library(urca)})
cat("R", R.version$major, R.version$minor, "| forecast", as.character(packageVersion("forecast")),
    "| tseries", as.character(packageVersion("tseries")), "\n")
sec <- function(x) cat("\n==== ", x, " ====\n")

sec("M1 · AirPassengers: unidades y rango")
print(tsp(AirPassengers)); print(length(AirPassengers))

sec("M3 · residuo de decompose multiplicativo")
residuo <- na.omit(decompose(AirPassengers, type = "multiplicative")$random)
rr <- acf(residuo, lag.max = 24, plot = FALSE)$acf[-1]
b <- 1.96 / sqrt(length(residuo))
print(c(n = length(residuo), banda = round(b, 3)))
print(round(rr[c(1, 12)], 3)); print(sum(abs(rr) > b)); print(which(abs(rr) > b))
# caso limite: cuantas barras saca el residuo de decompose cuando la serie SI es
# ruido alrededor de tendencia y estacionalidad fija (no deberia haber dependencia)
set.seed(20261117)
fuera_wn <- replicate(500, {
  t <- 1:144
  y <- ts(exp(log(100) + 0.01 * t + 0.1 * sin(2 * pi * t / 12) + rnorm(144, sd = 0.03)), frequency = 12)
  r <- na.omit(decompose(y, type = "multiplicative")$random)
  a <- acf(r, lag.max = 24, plot = FALSE)$acf[-1]
  c(sum(abs(a) > 1.96 / sqrt(length(r))), a[1], a[12])
})
cat("Residuo de decompose sobre serie con R_t i.i.d.: barras fuera (media, p95):",
    round(mean(fuera_wn[1, ]), 2), quantile(fuera_wn[1, ], 0.95),
    "| r1 medio", round(mean(fuera_wn[2, ]), 3), "| r12 medio", round(mean(fuera_wn[3, ]), 3), "\n")

sec("M4 · PACF de AirPassengers y de la serie de memoria corta")
p <- pacf(AirPassengers, lag.max = 24, plot = FALSE)$acf
cat("PACF AP fuera de la banda:", sum(abs(p) > 1.96 / sqrt(144)), "rezagos", which(abs(p) > 1.96 / sqrt(144)), "\n")
set.seed(1); corta <- arima.sim(list(ar = 0.5), n = 200)
pc <- pacf(corta, lag.max = 24, plot = FALSE)$acf
ac <- acf(corta, lag.max = 24, plot = FALSE)$acf[-1]
print(round(pc[1:4], 3)); print(which(abs(pc) > 1.96 / sqrt(200)))
print(round(ac[1:4], 3)); print(which(abs(ac) > 1.96 / sqrt(200)))

sec("M5 · potencia del ADF para phi = 0.95 frente a phi = 1 (n = 200)")
set.seed(7)
pw <- replicate(400, suppressWarnings(adf.test(arima.sim(list(ar = 0.95), n = 200))$p.value) < 0.05)
cat("ADF rechaza la raiz unitaria con phi = 0.95, n = 200:", mean(pw), "\n")

sec("M6 · recta con ruido")
set.seed(1)
recta <- 10 + 0.5 * (1:138) + rnorm(138, sd = 5)
print(adf.test(recta)); print(kpss.test(recta, null = "Trend"))
# caso limite: con que frecuencia sale la misma conclusion en otras semillas
ok <- sapply(1:300, function(s) { set.seed(s); r <- 10 + 0.5 * (1:138) + rnorm(138, sd = 5)
  c(adf = suppressWarnings(adf.test(r)$p.value) < 0.05,
    kpss = suppressWarnings(kpss.test(r, null = "Trend")$p.value) > 0.05) })
cat("Otras 300 semillas: ADF rechaza", mean(ok[1, ]), "| KPSS tendencia no rechaza", mean(ok[2, ]), "\n")

sec("M6 · TRM")
trm_df <- read.csv("Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")
trm <- ts(trm_df$trm, start = c(2015, 1), frequency = 12)
print(length(trm)); print(range(trm_df$mes))
print(suppressWarnings(adf.test(trm))); print(suppressWarnings(kpss.test(trm)))
print(suppressWarnings(kpss.test(trm, null = "Trend"))); print(suppressWarnings(kpss.test(diff(trm), null = "Trend")))

sec("M6 · AirPassengers: ADF y KPSS de nivel y de tendencia")
print(suppressWarnings(adf.test(AirPassengers)))
print(suppressWarnings(kpss.test(AirPassengers)))
print(suppressWarnings(kpss.test(AirPassengers, null = "Trend")))
print(suppressWarnings(adf.test(log(AirPassengers))))
print(suppressWarnings(adf.test(AirPassengers, k = 12)))
print(suppressWarnings(kpss.test(log(AirPassengers), null = "Trend")))

sec("M7 · regla del orden en log(AirPassengers)")
la <- log(AirPassengers)
cat("nsdiffs(la) =", nsdiffs(la), "| ndiffs(diff(la,12)) =", ndiffs(diff(la, lag = 12)),
    "| ndiffs/nsdiffs de dd =", ndiffs(diff(diff(la, lag = 12))), nsdiffs(diff(diff(la, lag = 12))), "\n")
cat("orden contrario: ndiffs(la) =", ndiffs(la), "| ndiffs(diff(la)) =", ndiffs(diff(la)),
    "| nsdiffs(diff(la)) =", nsdiffs(diff(la)), "| r12 de diff(la) =",
    round(acf(diff(la), lag.max = 12, plot = FALSE)$acf[13], 3), "\n")
print(suppressWarnings(kpss.test(diff(la))))

sec("M7 · UKgas")
print(tsp(UKgas)); print(length(UKgas))
g <- log(UKgas)
cat("nsdiffs(g) =", nsdiffs(g), "| ndiffs(diff(g,4)) =", ndiffs(diff(g, lag = 4)), "\n")
cat("ndiffs(g) =", ndiffs(g), "| nsdiffs(diff(g)) =", nsdiffs(diff(g)), "\n")
gs <- diff(g, lag = 4); gsd <- diff(diff(g), lag = 4)
print(c(length(gs), length(gsd)))
print(round(c(acf(gs, lag.max = 1, plot = FALSE)$acf[2], acf(gsd, lag.max = 1, plot = FALSE)$acf[2]), 3))
cat("F_S (seas.heuristic) de g:", round(forecast:::seas.heuristic(g), 3),
    "| de diff(g):", round(forecast:::seas.heuristic(diff(g)), 3), "\n")
# casos limite de la conclusion: otras pruebas y otros niveles
cat("ndiffs(gs, test='adf') =", ndiffs(gs, test = "adf"), "| ndiffs(gs, test='pp') =", ndiffs(gs, test = "pp"),
    "| ndiffs(gs, alpha=0.1) =", ndiffs(gs, alpha = 0.1), "| ndiffs(gs, type='trend') =", ndiffs(gs, type = "trend"), "\n")
cat("nsdiffs(g, test='ocsb') =", nsdiffs(g, test = "ocsb"), "\n")
print(suppressWarnings(kpss.test(gs))); print(suppressWarnings(adf.test(gs)))
fit_g <- auto.arima(g); print(fit_g)
fit_g2 <- auto.arima(g, stepwise = FALSE, approximation = FALSE); print(arimaorder(fit_g2))
cat("r1 y r4 de gs:", round(acf(gs, lag.max = 4, plot = FALSE)$acf[c(2, 5)], 3), "\n")
cat("r1 y r4 de gsd:", round(acf(gsd, lag.max = 4, plot = FALSE)$acf[c(2, 5)], 3), "\n")
# UKgas en niveles, sin log
cat("UKgas sin log: nsdiffs", nsdiffs(UKgas), "ndiffs(diff(.,4))", ndiffs(diff(UKgas, lag = 4)),
    "ndiffs", ndiffs(UKgas), "\n")

sec("M7 · F_S de nsdiffs frente al del cap. 1 (0.937 log AP / 0.783 AP)")
cat("seas.heuristic(log AP) =", round(forecast:::seas.heuristic(la), 3),
    "| seas.heuristic(AP) =", round(forecast:::seas.heuristic(AirPassengers), 3), "\n")

sec("M7 · KPSS de ndiffs frente a tseries::kpss.test (truncamiento)")
x <- c(diff(la, lag = 12))
cat("trunc(3*sqrt(n)/13) con n =", length(x), "=", trunc(3 * sqrt(length(x)) / 13), "\n")
print(suppressWarnings(kpss.test(diff(la, lag = 12))))
k1 <- ur.kpss(x, type = "mu", use.lag = trunc(3 * sqrt(length(x)) / 13)); print(k1@teststat)

sec("M9 · pipeline con logaritmo")
preparar <- function(y, logaritmo = TRUE, m = frequency(y)) {
  w <- if (logaritmo) log(y) else y
  D <- if (m > 1) nsdiffs(w) else 0
  if (D > 0) w <- diff(w, lag = m, differences = D)
  d <- ndiffs(w)
  if (d > 0) w <- diff(w, differences = d)
  list(serie = w, logaritmo = logaritmo, d = d, D = D,
       kpss_p = suppressWarnings(kpss.test(w)$p.value))
}
res <- preparar(AirPassengers)
print(c(res$d, res$D, res$kpss_p, length(res$serie)))
r <- acf(res$serie, lag.max = 24, plot = FALSE)$acf[-1]
print(round(r[c(1, 12)], 3)); print(sum(abs(r) > 1.96 / sqrt(length(res$serie)))); print(which(abs(r) > 1.96 / sqrt(length(res$serie))))
print(round(BoxCox.lambda(AirPassengers, method = "guerrero"), 4))
# caso limite: el pipeline con logaritmo = FALSE sobre AirPassengers y sobre co2
res2 <- preparar(AirPassengers, logaritmo = FALSE); print(c(res2$d, res2$D, length(res2$serie)))
res3 <- preparar(co2, logaritmo = FALSE); print(c(res3$d, res3$D, res3$kpss_p))
# una serie no estacional (m = 1): el argumento por defecto
res4 <- preparar(Nile, logaritmo = FALSE); print(c(res4$d, res4$D))
# una serie con ceros o negativos y logaritmo = TRUE por defecto
cat("preparar(UKDriverDeaths) =", unlist(preparar(UKDriverDeaths)[c("d", "D")]), "\n")
cat("preparar(log UKgas por defecto) d, D =", unlist(preparar(UKgas)[c("d", "D")]), "\n")
