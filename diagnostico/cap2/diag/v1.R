# diag/v1.R — Par académico, capítulo 2: cifras de los módulos 2 a 8.
# Uso (desde la raíz del repo):  Rscript diagnostico/cap2/diag/v1.R
# Recalcula desde cero (no lee cap2_estacionariedad.json salvo la TRM, que se
# toma de precalculo/salidas/datos_series.json, la misma que usa genera_cap2.R).
suppressMessages({ library(jsonlite); library(tseries); library(forecast); library(urca) })
options(width = 120)
sd_json <- fromJSON("precalculo/salidas/datos_series.json")
trm <- ts(as.numeric(sd_json$trm$valores), start = as.integer(sd_json$trm$inicio), frequency = 12)
AP <- AirPassengers; lx <- log(AP)
set.seed(2026); e <- rnorm(200); cam <- cumsum(e)
cat("== M2 ruido blanco ==\n")
r <- acf(e, lag.max = 24, plot = FALSE)$acf[-1]
cat("banda", 1.96/sqrt(200), " fuera:", sum(abs(r) > 1.96/sqrt(200)), " r1", round(r[1],4), "\n")
cat("24*0.05 =", 24*0.05, "\n")

cat("== M3 ACF ==\n")
ra <- acf(AP, lag.max = 24, plot = FALSE)$acf[-1]
cat("AP r1 r2 r12:", round(ra[c(1,2,12)],4), " r11 r13:", round(ra[c(11,13)],4), "\n")
rc <- acf(cam, lag.max = 24, plot = FALSE)$acf[-1]
cat("caminata r1 r12:", round(rc[c(1,12)],4), "\n")
dtrm <- diff(trm); rt <- acf(dtrm, lag.max = 24, plot = FALSE)$acf[-1]
cat("dTRM r1:", round(rt[1],4), " banda", round(1.96/sqrt(length(dtrm)),4),
    " fuera de banda (rezagos):", which(abs(rt) > 1.96/sqrt(length(dtrm))), "\n")
cat("dTRM r1..r6:", round(rt[1:6],4), "\n")

cat("== M4 PACF ==\n")
pc <- pacf(cam, lag.max = 24, plot = FALSE)$acf
cat("caminata PACF 1..6:", round(pc[1:6],4), " fuera de banda:", which(abs(pc) > 1.96/sqrt(200)), "\n")
cat("AP PACF 1..3:", round(pacf(AP, lag.max=24, plot=FALSE)$acf[1:3],4), "\n")
# Recursión de Durbin-Levinson (la de calcularPACF del JS) sobre las series tal como
# están en el JSON (valores redondeados a 5 decimales) frente a la PACF guardada (4 decimales)
dl <- function(rho) { K <- length(rho); phi <- matrix(0, K, K); out <- numeric(K)
  phi[1,1] <- rho[1]; out[1] <- rho[1]
  for (k in 2:K) { num <- rho[k] - sum(phi[k-1,1:(k-1)] * rho[(k-1):1])
    den <- 1 - sum(phi[k-1,1:(k-1)] * rho[1:(k-1)]); phi[k,k] <- num/den; out[k] <- phi[k,k]
    phi[k,1:(k-1)] <- phi[k-1,1:(k-1)] - phi[k,k]*phi[k-1,(k-1):1] }
  out }
J <- fromJSON("precalculo/salidas/cap2_estacionariedad.json")
difmax <- sapply(J$series, function(s) { x <- s$valores
  n <- length(x); xc <- x - mean(x); g <- sapply(0:24, function(k) sum(xc[1:(n-k)]*xc[(1+k):n])/n)
  max(abs(dl(g[-1]/g[1]) - s$pacf)) })
print(signif(difmax, 3)); cat("max:", signif(max(difmax),3), "\n")
# sin redondear: DL exacto vs pacf() de R
cat("DL vs stats::pacf (sin redondeo), caminata:", signif(max(abs(dl(acf(cam,24,plot=FALSE)$acf[-1]) - pc)),3), "\n")

cat("== M5 AR(1) diferenciada: rho1 teórico de nabla y = -(1-phi)/2 ==\n")
for (ph in c(0, 0.5, 0.7, 0.95)) cat("phi", ph, " rho1(nabla) =", -(1-ph)/2,
  " Var(nabla y)/Var(y) =", 2*(1-ph), "\n")

cat("== M6 ADF/KPSS ==\n")
f <- function(z) { a <- suppressWarnings(adf.test(z)); k <- suppressWarnings(kpss.test(z))
  c(ADF = unname(round(a$statistic,4)), pADF = round(a$p.value,4), KPSS = unname(round(k$statistic,4)), pKPSS = round(k$p.value,4)) }
cat("n TRM:", length(trm), start(trm), end(trm), "\n")
print(rbind(TRM = f(trm), dTRM = f(dtrm)))
cat("ADF AP crudo:", round(suppressWarnings(adf.test(AP))$statistic,4), "\n")
cat("k por defecto:", trunc((144-1)^(1/3)), "\n")
for (kk in c(5,11,12,13)) { a <- suppressWarnings(adf.test(lx, k = kk)); cat("log AP k=", kk, round(a$statistic,4), round(a$p.value,4), "\n") }
for (kk in c(5,11,12,13)) { a <- suppressWarnings(adf.test(AP, k = kk)); cat("AP (nivel) k=", kk, round(a$statistic,4), round(a$p.value,4), "\n") }
sa <- seasadj(stl(lx, s.window = "periodic"))
a <- adf.test(sa); k <- suppressWarnings(kpss.test(sa, null = "Trend"))
cat("SA: ADF", round(a$statistic,4), round(a$p.value,4), " KPSS-T", round(k$statistic,4), k$p.value, "\n")
cat("KPSS-T AP:", round(suppressWarnings(kpss.test(AP, null="Trend"))$statistic,4), "  log AP:",
    round(suppressWarnings(kpss.test(lx, null="Trend"))$statistic,4), "\n")
# Monte Carlo (mismo código que genera_cap2.R)
mc <- sapply(c(0, 0.5, 1, 2, 4), function(amp) { set.seed(7)
  100*mean(replicate(500, { x <- ts(cumsum(rnorm(144)) + amp*sin(2*pi*(1:144)/12), frequency = 12)
    suppressWarnings(adf.test(x))$p.value < 0.05 })) })
cat("Monte Carlo % rechazo:", mc, "\n")
# misma tasa con k = 12 (¿lo arregla cubrir el ciclo?)
mc12 <- sapply(c(0, 4), function(amp) { set.seed(7)
  100*mean(replicate(500, { x <- ts(cumsum(rnorm(144)) + amp*sin(2*pi*(1:144)/12), frequency = 12)
    suppressWarnings(adf.test(x, k = 12))$p.value < 0.05 })) })
cat("Monte Carlo con k = 12, amplitudes 0 y 4:", mc12, "\n")
cat("binomial: IC95 de 3.2% con 500 réplicas:", round(100*binom.test(16, 500)$conf.int, 2), "\n")

cat("== M7 diferenciación ==\n")
cat("AP 1949-01..1950-02:", AP[1:14], "\n")
dd <- diff(diff(lx), lag = 12); cat("length dd:", length(dd), " primer valor nabla nabla12 (nivel):",
  diff(diff(AP), lag = 12)[1], "\n")
difn <- function(x, d) if (d == 0) x else diff(x, differences = d)
tab <- t(sapply(0:3, function(d) { y <- difn(lx, d); z <- difn(trm, d)
  c(d = d, var_lx = round(var(y), 5), r1_lx = round(acf(y, 1, plot = FALSE)$acf[2], 4),
    var_trm = round(var(z), 0), r1_trm = round(acf(z, 1, plot = FALSE)$acf[2], 4)) }))
print(tab)
print(try(diff(1:5, differences = 0), silent = TRUE))
d1 <- diff(lx); d12 <- diff(lx, lag = 12)
cat("ndiffs/nsdiffs lx:", ndiffs(lx), nsdiffs(lx), " d1:", ndiffs(d1), nsdiffs(d1),
    " dd:", ndiffs(dd), nsdiffs(dd), " d12:", ndiffs(d12), nsdiffs(d12), "\n")
cat("KPSS nivel d1 (tseries):", round(suppressWarnings(kpss.test(d1))$statistic,4), suppressWarnings(kpss.test(d1))$p.value, "\n")
cat("r12 de d1:", round(acf(d1, 24, plot = FALSE)$acf[13], 4), "  r12 de d12:", round(acf(d12, 24, plot = FALSE)$acf[13], 4),
    "  r1 de d12:", round(acf(d12, 24, plot = FALSE)$acf[2], 4), "\n")
k12 <- suppressWarnings(kpss.test(d12)); cat("kpss.test(d12):", round(k12$statistic,4), round(k12$p.value,4), " lag", k12$parameter, " n", length(d12), "\n")
u <- ur.kpss(d12, type = "mu", use.lag = trunc(3*sqrt(length(d12))/13))
cat("ur.kpss(d12, lag=", trunc(3*sqrt(length(d12))/13), "):", round(u@teststat,4), " crit:", u@cval, "\n")
cat("4(n/100)^.25 =", trunc(4*(132/100)^0.25), "\n")
cat("cuerpo de forecast:::kpss_test? -> ver abajo\n")
print(body(forecast::ndiffs))

cat("== M7 contraejemplo: AR(1) estacionaria con phi = 0.8, ¿la varianza sube al diferenciar? ==\n")
set.seed(1); x <- arima.sim(list(ar = 0.8), n = 2000)
cat("var d=0..2:", round(sapply(0:2, function(d) var(difn(x, d))), 3), " ndiffs:", ndiffs(x), "\n")

cat("== M8 Box-Cox ==\n")
lam <- BoxCox.lambda(AP, method = "guerrero"); lt <- BoxCox.lambda(trm, method = "guerrero")
cat("lambda AP", round(lam,4), " TRM", round(lt,4), "\n")
g <- function(L) forecast:::guer.cv(L, AP)
cat("cv sin/log/opt:", round(c(g(1), g(0), g(lam)),5), " exceso log %:", round(100*(g(0)/g(lam)-1),1),
    " mejora captada %:", round(100*(g(1)-g(0))/(g(1)-g(lam)),1), "\n")
rej <- seq(-1, 2, by = 0.005); b <- rej[sapply(rej, g) <= 1.2*g(lam)]; cat("zona 20%:", range(b), "\n")
print(body(forecast:::guer.cv))
cat("lambda guerrero serie anual (frecuencia 1, Nile):", round(BoxCox.lambda(Nile, method = "guerrero"),4), "\n")
w <- BoxCox(AP, lam); cat("max|InvBoxCox - AP|:", max(abs(InvBoxCox(w, lam) - AP)), "\n")
