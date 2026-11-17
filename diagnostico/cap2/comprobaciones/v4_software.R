# v4_software.R — verificador independiente de la R4 del capítulo 2.
# Repite por su cuenta, sin leer r4_software.R, lo que las entradas `propia`
# y las frases sobre software afirman. Salida: v4_software.out
suppressPackageStartupMessages({library(tseries); library(forecast); library(urca)})
cat(R.version.string, "· tseries", as.character(packageVersion("tseries")),
    "· forecast", as.character(packageVersion("forecast")),
    "· urca", as.character(packageVersion("urca")), "\n\n")
y <- AirPassengers; ly <- log(y); n <- length(y)

cat("== c2-m3-06: acf() con divisor T\n")
gam <- function(x, k) { m <- mean(x); T <- length(x); sum((x[1:(T-k)]-m)*(x[(1+k):T]-m))/T }
r_T <- sapply(1:24, function(k) gam(ly, k)/gam(ly, 0))
cat("max|acf - divisor T| =", max(abs(acf(ly, 24, plot = FALSE)$acf[-1] - r_T)), "\n")
r_Tk <- sapply(1:24, function(k) gam(ly, k)*length(ly)/(length(ly)-k)/gam(ly, 0))
cat("max|acf - divisor T-k| =", max(abs(acf(ly, 24, plot = FALSE)$acf[-1] - r_Tk)), "\n\n")

cat("== c2-m4-04/05/09: pacf() frente a Durbin-Levinson y frente a regresiones MCO\n")
dl <- function(r) { K <- length(r); phi <- matrix(0, K, K); out <- numeric(K)
  phi[1,1] <- r[1]; out[1] <- r[1]
  if (K > 1) for (k in 2:K) { j <- 1:(k-1)
    phi[k,k] <- (r[k] - sum(phi[k-1,j]*r[k-j]))/(1 - sum(phi[k-1,j]*r[j]))
    phi[k,j] <- phi[k-1,j] - phi[k,k]*phi[k-1,k-j]; out[k] <- phi[k,k] }
  out }
p_r <- as.numeric(pacf(ly, 24, plot = FALSE)$acf)
cat("max|pacf - DL(acf)| =", max(abs(p_r - dl(r_T))), "\n")
ols <- sapply(1:24, function(k) { z <- ly - mean(ly); X <- embed(z, k+1)
  coef(lm(X[,1] ~ X[,-1] - 1))[k] })
cat("max|pacf - último coef. MCO de k regresiones| =", max(abs(p_r - ols)), "\n")
cat("k=1..6  pacf:", round(p_r[1:6], 4), "\n        MCO :", round(ols[1:6], 4), "\n\n")

cat("== c2-m6-10: k por defecto de adf.test\n")
print(formals(adf.test)$k); cat("T =", n, "→ k =", trunc((n-1)^(1/3)), "\n\n")

cat("== c2-m6-04: adf.test con constante y tendencia (reproducción manual)\n")
k <- trunc((n-1)^(1/3)); x <- as.numeric(y); dy <- diff(x)
Z <- embed(dy, k+1); yt <- Z[,1]; xt1 <- x[(k+1):(n-1)]; tt <- (k+1):(n-1)
fit <- lm(yt ~ xt1 + tt + Z[,-1])
cat("t de xt1 =", coef(summary(fit))["xt1","t value"], "· adf.test =",
    suppressWarnings(adf.test(y)$statistic), "\n")
cat("adf.test con k = 12:", suppressWarnings(adf.test(y, k = 12)$statistic),
    " p =", suppressWarnings(adf.test(y, k = 12)$p.value), "\n\n")

cat("== c2-m6-09: avisos de tablas en adf.test y kpss.test\n")
w <- character(); withCallingHandlers({adf.test(y); kpss.test(diff(ly)); kpss.test(ly)},
  warning = function(e) { w <<- c(w, conditionMessage(e)); invokeRestart("muffleWarning") })
print(unique(w)); cat("\n")

cat("== c2-m7-15 / c2-m7-18: KPSS sobre diff(log y, 12)\n")
s <- diff(ly, lag = 12); ns <- length(s)
cat("n =", ns, "· trunc(4(n/100)^(1/4)) =", trunc(4*(ns/100)^0.25),
    "· trunc(3 sqrt(n)/13) =", trunc(3*sqrt(ns)/13), "\n")
kt <- suppressWarnings(kpss.test(s)); cat("kpss.test:", kt$statistic, "p =", kt$p.value, "\n")
u <- ur.kpss(s, type = "mu", use.lag = trunc(3*sqrt(ns)/13))
cat("ur.kpss(use.lag=2):", u@teststat, "· crítico 5 %:", u@cval[,"5pct"], "\n")
cat("ndiffs(s) =", ndiffs(s), "· nsdiffs(ly) =", nsdiffs(ly), "· ndiffs(diff(s)) =", ndiffs(diff(s)),
    "· nsdiffs(diff(s)) =", nsdiffs(diff(s)), "\n")
cat("max.d por defecto:", formals(ndiffs)$max.d, "· umbral de nsdiffs en el código:",
    grepl("0.64", paste(deparse(forecast:::seas.heuristic), collapse = "")) ||
    grepl("0.64", paste(deparse(nsdiffs), collapse = "")), "\n\n")

cat("== c2-m7-08: Var(diff y)/Var(y) frente a 2(1 - r1)\n")
for (nom in c("ly", "s")) { z <- get(nom); r1 <- acf(z, 1, plot = FALSE)$acf[2]
  cat(nom, ": cociente =", var(diff(z))/var(z), "· 2(1-r1) =", 2*(1-r1), "\n") }
cat("\n== c2-m8-03: BoxCox con lambda > 0 admite negativos\n")
print(BoxCox(c(-4, -1, 1, 4), 0.5))
cat("\n== c2-m8-04 (pendiente, solo lo calculable): BoxCox.lambda guerrero =",
    BoxCox.lambda(y, method = "guerrero"), "\n")
