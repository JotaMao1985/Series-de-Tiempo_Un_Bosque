# Par académico cap. 4 · recálculo independiente de las cifras de la prosa (M1-M6)
suppressMessages({library(forecast); library(tseries); library(urca)})
cat("R", R.version.string, "| forecast", as.character(packageVersion("forecast")),
    "| tseries", as.character(packageVersion("tseries")), "| urca", as.character(packageVersion("urca")), "\n")
y <- Nile; n <- length(y)
sec <- function(s) cat("\n==== ", s, " ====\n")

sec("M1 · ARIMA(1,1,1) del Nilo y raíces")
f111 <- arima(y, order = c(1,1,1), method = "ML"); print(round(coef(f111), 4))
cat("raiz MA 1/0.8741 =", round(1/0.8741, 4), "\n")
cat("ACF1 de diff(Nile,2) =", round(acf(diff(y, differences=2), plot=FALSE)$acf[2], 4), "\n")
cat("var por d:", sapply(0:3, function(d) round(var(if (d==0) y else diff(y, differences=d)), 2)), "\n")
cat("razón var d=2/d=1:", round(var(diff(y,differences=2))/var(diff(y)), 3), "\n")
cat("caída relativa d0->d1 (%):", round(100*(1 - var(diff(y))/var(y)), 2), "\n")
# varianza de largo plazo de w relativa a sigma2 (por qué integrar casi no dispara la varianza)
cat("(1+theta)^2/(1-phi)^2 =", round((1-0.8741)^2/(1-0.2544)^2, 4), "\n")

sec("M3 · pruebas sobre el Nilo")
print(adf.test(y)); print(kpss.test(y)); print(PP.test(y))
pp <- pp.test(y); print(pp)
pp2 <- pp.test(y, type = "Z(t_alpha)"); print(pp2)
d1 <- ur.df(as.numeric(y), type = "drift", lags = 1); cat("ur.df drift lags=1 tau_mu =", round(d1@teststat[1],4), " cval:", d1@cval[1,], "\n")
pz <- ur.pp(as.numeric(y), type = "Z-tau", model = "constant", lags = "short"); cat("ur.pp Z-tau constante:", round(pz@teststat,4), " cval:", pz@cval[1,], "\n")
uk <- ur.kpss(as.numeric(y), type = "mu", use.lag = trunc(3*sqrt(n)/13)); cat("ur.kpss (ndiffs) lag", trunc(3*sqrt(n)/13), "stat", round(uk@teststat,4), "\n")
cat("ndiffs:", sapply(c("kpss","adf","pp"), function(t) ndiffs(y, test=t)), "\n")
cat("l_R =", trunc(4*(n/100)^0.25), " l_legacy =", ceiling(12*(n/100)^0.25), "\n")

sec("M3 · modelo de dos medias")
esc <- as.numeric(time(y) >= 1899)
fe <- arima(y, order = c(0,0,0), xreg = esc, method = "ML")
print(round(coef(fe), 3)); cat("sd residuales:", round(sd(residuals(fe)), 3), " beta/sd:", round(abs(coef(fe)[2])/sd(residuals(fe)),3), "\n")
cat("posición 1899:", which(time(y)==1899), " tau = ", round((which(time(y)==1899)-1)/n, 3), "\n")
cat("100/sd =", round(100/sd(residuals(fe)), 3), "\n")

sec("M3 · simulación ARIMA(1,1,1) con raíz unitaria verdadera: PP.test y adf.test (1000 réplicas, semilla 2026)")
set.seed(2026)
rp <- ra <- rpp <- 0
for (i in 1:1000) {
  x <- arima.sim(list(order=c(1,1,1), ar=0.2544, ma=-0.8741), n = 99, sd = sqrt(f111$sigma2)) + 1000
  if (suppressWarnings(PP.test(x)$p.value) <= 0.05) rp <- rp + 1
  if (suppressWarnings(adf.test(x)$p.value) <= 0.05) ra <- ra + 1
}
cat("PP.test rechaza:", rp/1000, " adf.test(k=4) rechaza:", ra/1000, "\n")

sec("M3 · Monte Carlo del escalón (réplica independiente, misma especificación, semilla 2026 y 7)")
mc <- function(beta, reps, seed, sig = sd(residuals(fe))) {
  set.seed(seed); e <- as.numeric(1:100 >= 29)
  r4 <- r12 <- adfnr <- ndk <- nda <- 0; est <- numeric(reps)
  for (i in 1:reps) {
    x <- 1000 + beta*e + rnorm(100, 0, sig)
    k <- suppressWarnings(kpss.test(x)); est[i] <- k$statistic
    r4 <- r4 + (k$p.value <= 0.05)
    r12 <- r12 + (suppressWarnings(kpss.test(x, lshort=FALSE)$p.value) <= 0.05)
    adfnr <- adfnr + (suppressWarnings(adf.test(x)$p.value) > 0.05)
    ndk <- ndk + (ndiffs(x, test="kpss") >= 1); nda <- nda + (ndiffs(x, test="adf") >= 1)
  }
  round(c(beta=beta, kpss_l4=r4/reps, kpss_l12=r12/reps, kpss_medio=mean(est), adf_no_rechaza=adfnr/reps,
          ndiffs_kpss=ndk/reps, ndiffs_adf=nda/reps), 4)
}
for (s in c(2026, 7)) {
  cat("semilla", s, "1000 réplicas\n")
  print(rbind(mc(0, 1000, s), mc(-247.78, 1000, s)))
  cat("semilla", s, "400 réplicas, malla\n")
  print(do.call(rbind, lapply(c(0,100,200,300), function(b) mc(b, 400, s))))
}
