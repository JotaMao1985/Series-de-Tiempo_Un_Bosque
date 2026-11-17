# R4 del capítulo 2 · lo que el capítulo dice del software y ninguna obra de la
# biblioteca respalda: se comprueba aquí, ejecutando o leyendo el código de la
# función. Son las afirmaciones registradas como `propia` en cap2.yml.
suppressPackageStartupMessages({library(tseries); library(forecast); library(urca)})
cat("R", R.version.string, "· tseries", as.character(packageVersion("tseries")),
    "· forecast", as.character(packageVersion("forecast")),
    "· urca", as.character(packageVersion("urca")), "\n\n")
y <- AirPassengers; ly <- log(y); n <- length(y)

cat("== c2-m3-06 · acf() divide entre T ==\n")
k <- 5; yb <- mean(ly)
g <- function(k) sum((ly[1:(n-k)] - yb) * (ly[(1+k):n] - yb)) / n
cat("max |acf() - (suma/T)/(suma0/T)| en k=1..24:",
    max(abs(acf(ly, 24, plot = FALSE)$acf[-1] - sapply(1:24, g) / g(0))), "\n\n")

cat("== c2-m4-04, c2-m4-09 · pacf() y la recursión de Durbin-Levinson ==\n")
dl <- function(rho) {            # rho[k] = r_k, k = 1..K
  K <- length(rho); pk <- numeric(K); phi <- numeric(0)
  for (k in 1:K) {
    if (k == 1) { pkk <- rho[1]; phi <- pkk }
    else {
      pkk <- (rho[k] - sum(phi * rho[(k-1):1])) / (1 - sum(phi * rho[1:(k-1)]))
      phi <- c(phi - pkk * rev(phi), pkk)
    }
    pk[k] <- pkk
  }
  pk
}
for (nom in c("ly", "y")) {
  x <- get(nom)
  cat(nom, ": max |pacf() - Durbin-Levinson sobre acf()| en k=1..24:",
      max(abs(as.numeric(pacf(x, 24, plot = FALSE)$acf) - dl(acf(x, 24, plot = FALSE)$acf[-1]))), "\n")
}
cat("\n== c2-m6-04, c2-m6-10 · adf.test(): rezagos por defecto y regresión ==\n")
print(args(adf.test))
cuerpo <- deparse(body(adf.test))
cat(grep("lm\\(|tt|approx|table <-|warning", cuerpo, value = TRUE), sep = "\n")
cat("k por defecto en AirPassengers:", trunc((n - 1)^(1/3)), "\n")
a <- suppressWarnings(adf.test(y))
z <- diff(y); kk <- 5; nn <- length(z); zz <- embed(z, kk + 1)
yt <- zz[, 1]; xt1 <- y[(kk + 1):nn]; tt <- (kk + 1):nn; yt1 <- zz[, 2:(kk + 1)]
aj <- summary(lm(yt ~ xt1 + 1 + tt + yt1))
cat("adf.test:", unname(a$statistic), " · lm con constante y tendencia:",
    aj$coefficients["xt1", "t value"], "\n")
cat("avisos:\n"); for (f in list(function() adf.test(y), function() kpss.test(y), function() kpss.test(diff(ly))))
  tryCatch(f(), warning = function(w) cat("  ", conditionMessage(w), "\n"))

cat("\n== c2-m6-09, c2-m7-15 · kpss.test(): truncamiento y tabla ==\n")
print(args(kpss.test))
cat(grep("trunc|table <-|approx|warning", deparse(body(kpss.test)), value = TRUE), sep = "\n")

cat("\n== c2-m7-18, c2-m7-15 · ndiffs() y nsdiffs() ==\n")
print(args(ndiffs)); print(args(nsdiffs))
cat(grep("ur.kpss|lags|use.lag|trunc|sqrt", deparse(body(ndiffs)), value = TRUE), sep = "\n")
cat(grep("0.64|seas_heuristic|seasonal_strength|stl", c(deparse(body(nsdiffs)),
    deparse(body(forecast:::seas.heuristic))), value = TRUE), sep = "\n")
d12 <- diff(ly, 12)
cat("n =", length(d12), "· kpss.test:", unname(suppressWarnings(kpss.test(d12))$statistic),
    "· ur.kpss con 2 rezagos:", ur.kpss(d12, use.lag = 2)@teststat, "· valores críticos:\n")
print(ur.kpss(d12, use.lag = 2)@cval)

cat("\n== c2-m8-03 · BoxCox() admite negativos con lambda > 0 ==\n")
print(BoxCox(c(-4, -1, 1, 4), 0.5)); cat(grep("sign|abs", deparse(body(BoxCox)), value = TRUE), sep = "\n")

cat("\n== c2-m8-04 · el criterio de Guerrero tal como lo describe el capítulo ==\n")
print(body(forecast:::guer.cv))
crit <- function(lam, x, m = frequency(x)) {
  nb <- floor(length(x) / m); x <- x[(length(x) - nb * m + 1):length(x)]
  b <- matrix(x, nrow = m); r <- apply(b, 2, sd) / colMeans(b)^(1 - lam)
  sd(r) / mean(r)
}
cat("lambda que minimiza el CV de s_i / media_i^(1-lambda):",
    optimize(crit, c(-1, 2), x = y)$minimum, "· BoxCox.lambda(guerrero):",
    BoxCox.lambda(y, method = "guerrero"), "\n")
