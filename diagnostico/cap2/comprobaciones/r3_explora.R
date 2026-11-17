# R3 · exploracion: cifras candidatas para la ronda de estructura del capitulo 2.
# Uso: Rscript diagnostico/cap2/comprobaciones/r3_explora.R > r3_explora.out 2>&1
suppressMessages({library(forecast); library(tseries)})
options(warn = 1)
cat("== 1. KPSS sobre AirPassengers (la cuarta fila: las dos rechazan?) ==\n")
print(adf.test(AirPassengers))
print(kpss.test(AirPassengers))
print(kpss.test(AirPassengers, null = "Trend"))
print(adf.test(log(AirPassengers)))
print(kpss.test(log(AirPassengers)))
print(kpss.test(log(AirPassengers), null = "Trend"))

cat("\n== 2. Tendencia determinista frente a estocastica ==\n")
for (s in 1:6) {
  set.seed(s)
  x <- 10 + 0.5 * (1:138) + rnorm(138, sd = 5)
  a <- suppressWarnings(adf.test(x)); k <- suppressWarnings(kpss.test(x, null = "Trend"))
  cat(sprintf("semilla %d: ADF %.4f p %.4f | KPSS Trend %.4f p %.4f | ndiffs %d\n", s,
              a$statistic, a$p.value, k$statistic, k$p.value, ndiffs(x)))
}

cat("\n== 3. El residuo de una descomposicion, con el correlograma ==\n")
fuera <- function(x) { x <- na.omit(x); r <- acf(x, lag.max = 24, plot = FALSE)$acf[-1]
  b <- 1.96 / sqrt(length(x))
  cat(sprintf("n %d banda %.4f r1 %.4f r12 %.4f fuera %d de 24: %s\n", length(x), b, r[1], r[12],
              sum(abs(r) > b), paste(which(abs(r) > b), collapse = " "))) }
cat("decompose aditiva:        "); fuera(decompose(AirPassengers)$random)
cat("decompose multiplicativa: "); fuera(decompose(AirPassengers, "multiplicative")$random)
cat("stl(log) periodic:        "); fuera(remainder(stl(log(AirPassengers), s.window = "periodic")))
cat("stl(log) s.window 13:     "); fuera(remainder(stl(log(AirPassengers), s.window = 13)))
cat("stl(log) 13 robust:       "); fuera(remainder(stl(log(AirPassengers), s.window = 13, robust = TRUE)))

cat("\n== 4. PACF de la serie de memoria corta del M3 ==\n")
set.seed(1); corta <- arima.sim(list(ar = 0.5), n = 200)
p <- pacf(corta, lag.max = 24, plot = FALSE)$acf
print(round(p[1:4], 3)); print(which(abs(p) > 1.96 / sqrt(200)))
r <- acf(corta, lag.max = 24, plot = FALSE)$acf[-1]; print(round(r[1:4], 3)); print(which(abs(r) > 1.96/sqrt(200)))

cat("\n== 5. Series donde el orden cambia la cuenta: ndiffs(cruda), nsdiffs, ndiffs(tras nabla_m), nsdiffs(tras nabla) ==\n")
cand <- list(USAccDeaths = USAccDeaths, UKDriverDeaths = UKDriverDeaths, ldeaths = ldeaths, mdeaths = mdeaths,
             fdeaths = fdeaths, nottem = nottem, co2 = co2, UKgas = UKgas, logUKgas = log(UKgas),
             AirPassengers = AirPassengers, logAP = log(AirPassengers), wineind = wineind, gas = gas,
             loggas = log(gas), woolyrnq = woolyrnq, austres = austres, JohnsonJohnson = JohnsonJohnson,
             logJJ = log(JohnsonJohnson), sunspot.month = sunspot.month, lynx = lynx, presidents = na.interp(presidents),
             UKDriverlog = log(UKDriverDeaths), euretail = tryCatch(fpp2::euretail, error = function(e) NULL),
             h02 = tryCatch(fpp2::h02, error = function(e) NULL), logh02 = tryCatch(log(fpp2::h02), error = function(e) NULL),
             a10 = tryCatch(fpp2::a10, error = function(e) NULL), loga10 = tryCatch(log(fpp2::a10), error = function(e) NULL),
             ausbeer = tryCatch(fpp2::ausbeer, error = function(e) NULL), qauselec = tryCatch(fpp2::qauselec, error = function(e) NULL))
for (nm in names(cand)) { y <- cand[[nm]]; if (is.null(y) || frequency(y) < 2) next
  m <- frequency(y)
  D <- tryCatch(nsdiffs(y), error = function(e) NA)
  cat(sprintf("%-16s m %2d n %4d | ndiffs(y) %d | nsdiffs(y) %s | ndiffs(nabla_m y) %d | ndiffs(nabla y) %d nsdiffs(nabla y) %s\n",
      nm, m, length(y), ndiffs(y), D, ndiffs(diff(y, lag = m)), ndiffs(diff(y)),
      tryCatch(nsdiffs(diff(y)), error = function(e) NA)))
}

cat("\n== 6. Pipeline con logaritmo ==\n")
w <- log(AirPassengers); cat("nsdiffs", nsdiffs(w), "\n"); w <- diff(w, 12); cat("ndiffs", ndiffs(w), "\n"); w <- diff(w)
cat("n", length(w), "var", var(w), "kpss p", suppressWarnings(kpss.test(w)$p.value), "\n")
cat("ndiffs/nsdiffs final", ndiffs(w), nsdiffs(w), "\n")
r <- acf(w, lag.max = 24, plot = FALSE)$acf[-1]; cat("r1", r[1], "r12", r[12], "fuera", which(abs(r) > 1.96/sqrt(length(w))), "\n")
p <- pacf(w, lag.max = 24, plot = FALSE)$acf; cat("pacf fuera", which(abs(p) > 1.96/sqrt(length(w))), "\n")
cat("lambda", BoxCox.lambda(AirPassengers, method = "guerrero"), "\n")
cat("\n== 7. Monte Carlo del M6 (amplitudes) ==\n")

cat("\n== 8. Candidatas para el caso en que el orden cambia la cuenta ==\n")
det <- function(y, nm) { m <- frequency(y)
  s <- diff(y, lag = m); r <- diff(y); b <- diff(s)
  f <- function(x) { a <- acf(x, lag.max = 2 * m, plot = FALSE)$acf[-1]; bb <- 1.96 / sqrt(length(x))
    sprintf("n %d r1 %.3f r2 %.3f r3 %.3f r_m %.3f fuera %d de %d (%s)", length(x), a[1], a[2], a[3], a[m],
            sum(abs(a) > bb), 2 * m, paste(which(abs(a) > bb), collapse = " ")) }
  cat("---", nm, "m", m, "n", length(y), "\n")
  cat(" estacional primero: nsdiffs(y)", nsdiffs(y), "| ndiffs(nabla_m y)", ndiffs(s), "| nsdiffs(nabla_m y)", nsdiffs(s), "\n")
  cat("   nabla_m y:", f(s), "\n")
  k1 <- suppressWarnings(kpss.test(s)); cat(sprintf("   kpss.test(nabla_m y): %.4f p %.4f | ur.kpss(lag de ndiffs): %.4f (5%%: 0.463)\n",
      k1$statistic, k1$p.value, urca::ur.kpss(s, use.lag = trunc(3 * sqrt(length(s)) / 13))@teststat))
  cat(" regular primero:    ndiffs(y)", ndiffs(y), "| nsdiffs(nabla y)", nsdiffs(r), "| ndiffs(nabla_m nabla y)", ndiffs(b), "\n")
  cat("   nabla y:  ", f(r), "\n")
  cat("   nabla_m nabla y:", f(b), "\n")
}
det(UKDriverDeaths, "UKDriverDeaths"); det(log(UKgas), "log(UKgas)"); det(woolyrnq, "woolyrnq")
det(log(JohnsonJohnson), "log(JohnsonJohnson)"); det(USAccDeaths, "USAccDeaths"); det(log(AirPassengers), "log(AirPassengers)")
