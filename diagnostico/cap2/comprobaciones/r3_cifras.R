# R3 · cada cifra nueva de la prosa del capitulo 2, recalculada (una linea por cifra).
# Uso: Rscript diagnostico/cap2/comprobaciones/r3_cifras.R > diagnostico/cap2/comprobaciones/r3_cifras.out 2>&1
suppressMessages({library(forecast); library(tseries)})
options(warn = -1)
f <- function(et, x) cat(sprintf("%-58s %s\n", et, paste(format(x, digits = 8), collapse = "  ")))
banda <- function(x) 1.96 / sqrt(length(x))

cat("== M3 · el residuo de la descomposicion clasica multiplicativa ==\n")
res <- na.omit(decompose(AirPassengers, type = "multiplicative")$random)
rr <- acf(res, lag.max = 24, plot = FALSE)$acf[-1]
f("n (prosa: 132)", length(res)); f("banda (prosa: 0.171)", banda(res))
f("r1, r12 (prosa: 0.403, 0.294)", rr[c(1, 12)]); f("fuera de 24 (prosa: 14)", sum(abs(rr) > banda(res)))

cat("\n== M4 · PACF y ACF de la serie de memoria corta ==\n")
set.seed(1); corta <- arima.sim(list(ar = 0.5), n = 200)
pc <- pacf(corta, lag.max = 24, plot = FALSE)$acf; rc <- acf(corta, lag.max = 24, plot = FALSE)$acf[-1]
f("ACF 1-3 (prosa: 0.474, 0.235, 0.106)", rc[1:3]); f("PACF 1-4 (prosa: 0.474, 0.014, -0.014, 0.033)", pc[1:4])
f("PACF fuera (prosa: 1 y 9)", which(abs(pc) > banda(corta)))
f("PACF de AirPassengers fuera (prosa: seis)", which(abs(pacf(AirPassengers, lag.max = 24, plot = FALSE)$acf) > banda(AirPassengers)))

cat("\n== M6 · determinista frente a estocastica; la cuarta fila ==\n")
set.seed(1); recta <- 10 + 0.5 * (1:138) + rnorm(138, sd = 5)
a <- adf.test(recta); k <- kpss.test(recta, null = "Trend")
f("recta: ADF, p (prosa: -5.744, < 0.01)", c(a$statistic, a$p.value)); f("recta: KPSS Trend, p (prosa: 0.052, > 0.10)", c(k$statistic, k$p.value))
for (s in 2:6) { set.seed(s); x <- 10 + 0.5 * (1:138) + rnorm(138, sd = 5)
  f(sprintf("  otra semilla (%d): p del ADF, p del KPSS Trend", s), c(adf.test(x)$p.value, kpss.test(x, null = "Trend")$p.value)) }
a <- adf.test(AirPassengers); k1 <- kpss.test(AirPassengers); k2 <- kpss.test(AirPassengers, null = "Trend")
f("AirPassengers: ADF (prosa: -7.32)", a$statistic); f("AirPassengers: KPSS nivel, p (prosa: 2.739, < 0.01)", c(k1$statistic, k1$p.value))
f("AirPassengers: KPSS tendencia, p (prosa: 0.096, > 0.10)", c(k2$statistic, k2$p.value))
f("AirPassengers: ADF k = 12 (prosa: -1.51, 0.781)", unlist(adf.test(AirPassengers, k = 12)[c("statistic", "p.value")]))
f("log(AirPassengers): ADF k = 5 (prosa: -6.42)", adf.test(log(AirPassengers))$statistic)

cat("\n== M7 · la regla del orden ==\n")
f("identidad (1-B^4) = (1-B)(1+B+B^2+B^3): max |dif|", { g <- log(UKgas)
  max(abs(diff(g, lag = 4) - stats::filter(diff(g), rep(1, 4), sides = 1)[-(1:3)])) })
f("nsdiffs por defecto: umbral de seas.heuristic", "ver body(nsdiffs): seas.heuristic(x) > 0.64")
g <- log(UKgas)
f("UKgas: n, m, inicio, fin", c(length(UKgas), frequency(UKgas), start(UKgas), end(UKgas)))
f("regla: nsdiffs(g), ndiffs(nabla_4 g) (prosa: 1, 0)", c(nsdiffs(g), ndiffs(diff(g, lag = 4))))
f("al reves: ndiffs(g), nsdiffs(nabla g) (prosa: 1, 1)", c(ndiffs(g), nsdiffs(diff(g))))
gs <- diff(g, lag = 4); gsd <- diff(diff(g), lag = 4)
f("observaciones (prosa: 104, 103)", c(length(gs), length(gsd)))
f("r1 (prosa: -0.178, -0.576)", c(acf(gs, plot = FALSE)$acf[2], acf(gsd, plot = FALSE)$acf[2]))
f("tras la regla no piden mas: ndiffs, nsdiffs", c(ndiffs(gs), nsdiffs(gs)))
l <- log(AirPassengers)
f("log AP: nsdiffs, ndiffs(nabla_12), ndiffs y nsdiffs finales", c(nsdiffs(l), ndiffs(diff(l, 12)), ndiffs(diff(diff(l, 12))), nsdiffs(diff(diff(l, 12)))))
f("log AP al reves: ndiffs(nabla), nsdiffs(nabla), r12", c(ndiffs(diff(l)), nsdiffs(diff(l)), acf(diff(l), lag.max = 12, plot = FALSE)$acf[13]))

cat("\n== M9 · el pipeline con logaritmo y el cierre ==\n")
w <- diff(diff(l, 12)); r <- acf(w, lag.max = 24, plot = FALSE)$acf[-1]
f("n, p del KPSS (prosa: 131, 0.1)", c(length(w), kpss.test(w)$p.value))
f("r1, r12 (prosa: -0.341, -0.387)", r[c(1, 12)]); f("fuera de 24 (prosa: 5)", sum(abs(r) > banda(w)))
f("lambda de Guerrero (codigo: -0.2947)", BoxCox.lambda(AirPassengers, method = "guerrero"))
