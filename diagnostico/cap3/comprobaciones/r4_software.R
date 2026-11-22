# r4_software.R — ronda R4 (fuentes) del capítulo 3
#
# Lo que el capítulo dice del software (R, forecast) y las cifras de simulación
# que ninguna obra respalda: las entradas `propia` (y el matiz de varias
# `con-matiz`) de bibliografia/contraste/cap3.yml se comprueban aquí,
# ejecutando. Son las comprobaciones que hicieron los lectores de la ronda,
# reunidas; cada bloque dice a qué afirmación corresponde.
#
# Uso (desde la raíz del repo):
#   Rscript diagnostico/cap3/comprobaciones/r4_software.R > diagnostico/cap3/comprobaciones/r4_software.out 2>&1
cat(R.version.string, "· forecast", as.character(packageVersion("forecast")), "\n")
RAIZ <- getwd()
stopifnot(file.exists(file.path(RAIZ, "Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")))

# ==========================================================================
# M1-M2: intercept = media, signo del MA, polyroot, pseudo-periodo, triangulo (c3-m1-07, -36; c3-m2-04, -12, -17)
# ==========================================================================
cat('\n=== M1-M2: intercept = media, signo del MA, polyroot, pseudo-periodo, triangulo (c3-m1-07, -36; c3-m2-04, -12, -17) ===\n')
# (1) arima(): la columna "intercept" es la media mu, no la constante c
set.seed(2026)
phi <- 0.6; mu <- 10
x <- mu + arima.sim(model = list(ar = phi), n = 5000)
fit <- arima(x, order = c(1, 0, 0))
print(round(coef(fit), 3)); print(names(coef(fit)))
cat("c = mu*(1-phi) =", mu*(1-phi), " vs intercept =", round(coef(fit)["intercept"],3), "\n")
cat("media de x:", round(mean(x),3), "\n")
# (2) convenio de signo del MA en arima / arima.sim / ARMAacf
x2 <- arima.sim(model = list(ma = 0.7), n = 3000)
print(round(coef(arima(x2, order = c(0,0,1), include.mean = FALSE)), 3))
print(round(ARMAacf(ma = 0.7, lag.max = 2), 4))
# (3) polyroot: coeficientes en orden ascendente
print(polyroot(c(2, -3, 1)))   # 2 - 3x + x^2 = (x-1)(x-2)
# (4) pseudo-periodo
P <- function(p1, p2) 2*pi/acos(p1/(2*sqrt(-p2)))
cat("P(1.40,-0.69) =", round(P(1.40,-0.69), 3), "\n")
cat("P(1.4027,-0.6853) =", round(P(1.4027,-0.6853), 3), "\n")
cat("P(1.5,-0.75) =", round(P(1.5,-0.75), 3), "\n")
# (5) cifras de la ACF del AR(2) con (1.4,-0.75)
print(round(ARMAacf(ar = c(1.4,-0.75), lag.max = 4), 4))
# (6) PACF teorica AR(2) (0.5,0.3): se corta en 2
print(round(ARMAacf(ar = c(0.5,0.3), lag.max = 5, pacf = TRUE), 4))
# (7) factores de gamma0 AR(2): fuera del triangulo, la formula deja de ser varianza
g0 <- function(p1,p2) (1-p2)/((1+p2)*((1-p2)^2 - p1^2))
cat("gamma0(0.5,0.3)/s2 =", round(g0(0.5,0.3),4), " gamma0(0,2) =", round(g0(0,2),4), " (fuera del triangulo)\n")
for (pp in list(c(0.5,0.3), c(1.4,-0.69), c(0.9,0.1), c(-0.5,0.4))) {
  p1 <- pp[1]; p2 <- pp[2]
  cat(sprintf("(%.2f,%.2f): factores (1+p2)=%.3f (1-p1-p2)=%.3f (1+p1-p2)=%.3f  | raices>1: %s\n", p1,p2,1+p2,1-p1-p2,1+p1-p2, all(Mod(polyroot(c(1,-p1,-p2)))>1)))
}
# (8) rho1, rho2 formula vs ARMAacf
p1<-0.5;p2<-0.3
cat("rho1,rho2 formula:", round(c(p1/(1-p2), p2 + p1^2/(1-p2)),4), " ARMAacf:", round(ARMAacf(ar=c(p1,p2), lag.max=2)[2:3],4), "\n")

# ==========================================================================
# M3-M4: arima() y la raiz invertible, por defecto y con transform.pars = FALSE (c3-m3-32, c3-m4-31)
# ==========================================================================
cat('\n=== M3-M4: arima() y la raiz invertible, por defecto y con transform.pars = FALSE (c3-m3-32, c3-m4-31) ===\n')
set.seed(1)
y <- arima.sim(n = 500, list(ma = 2.0))
for (met in c("CSS-ML","ML","CSS")) {
  m <- arima(y, order = c(0,0,1), method = met)
  cat(sprintf("%-7s transform.pars=TRUE : ma1=%.4f sigma2=%.4f\n", met, coef(m)["ma1"], m$sigma2))
}
for (met in c("CSS-ML","ML","CSS")) {
  m <- tryCatch(arima(y, order = c(0,0,1), method = met, transform.pars = FALSE), error=function(e) NULL)
  if (!is.null(m)) cat(sprintf("%-7s transform.pars=FALSE: ma1=%.4f sigma2=%.4f\n", met, coef(m)["ma1"], m$sigma2))
}
# arrancando en la rama no invertible
m <- arima(y, order=c(0,0,1), method="ML", transform.pars=FALSE, init=c(2.0, 0))
cat(sprintf("ML init ma=2, transform.pars=FALSE: ma1=%.4f sigma2=%.4f\n", coef(m)["ma1"], m$sigma2))
m <- arima(y, order=c(0,0,1), method="ML", transform.pars=FALSE, fixed=c(2.0, NA), include.mean=TRUE)
cat(sprintf("ML fixed ma=2: ma1=%.4f sigma2=%.4f\n", coef(m)["ma1"], m$sigma2))

# ==========================================================================
# M3-M5: cifras de PACF del MA(1), ARMAtoMA, pacf()$acf (c3-m4-09, c3-m5-08)
# ==========================================================================
cat('\n=== M3-M5: cifras de PACF del MA(1), ARMAtoMA, pacf()$acf (c3-m4-09, c3-m5-08) ===\n')
cat("PACF MA(1) theta=0.8:", round(ARMAacf(ma=0.8, lag.max=4, pacf=TRUE),4), "\n")
cat("PACF MA(1) theta=-0.8:", round(ARMAacf(ma=-0.8, lag.max=4, pacf=TRUE),4), "\n")
th <- 0.8; k <- 1:4
cat("formula Cryer (signo cambiado):", round(-(-th)^k*(1-th^2)/(1-th^(2*(k+1))),4), "\n")
cat("cos(pi/4), cos(pi/5):", round(cos(pi/4),3), round(cos(pi/5),3), "\n")
pw <- ARMAtoMA(ar=-0.5, ma=-0.7, lag.max=10)
cat("pi_j:", round(pw,4), "\n"); cat("primer |pi_j|<0.01:", which(abs(pw)<0.01)[1], "\n")
cat("psi:", round(ARMAtoMA(ar=0.7, ma=0.5, lag.max=4),4), "\n")
cat("rho1 ARMA(1,1):", round(ARMAacf(ar=0.7, ma=0.5, lag.max=1)[2],4), "\n")
cat("ARMAacf MA(1) theta=-1:", round(ARMAacf(ma=-1, lag.max=2)[-1],4), " Mod(polyroot(c(1,-1)))=", Mod(polyroot(c(1,-1))), "\n")
y <- ts(rnorm(100)); p <- pacf(y, plot=FALSE); cat("dim(pacf(y)$acf):", dim(p$acf), "\n")
cat("ARMA(2,1) rho:", round(ARMAacf(ar=c(.5,.3), ma=.4, lag.max=5)[2:4],4), "\n")
cat("MA(1) rho1 con theta=2:", ARMAacf(ma=2, lag.max=1)[2], "\n")
cat("1.96/sqrt(60), 1.96/sqrt(1000):", round(1.96/sqrt(60),3), round(1.96/sqrt(1000),3), "\n")
# PACF teorica ARMA(1,1) phi=.7 theta=.5, ARMA(2,1)
cat("PACF ARMA(1,1):", round(ARMAacf(ar=.7, ma=.5, lag.max=8, pacf=TRUE),4), "\n")
cat("PACF ARMA(2,1):", round(ARMAacf(ar=c(.5,.3), ma=.4, lag.max=8, pacf=TRUE),4), "\n")

# ==========================================================================
# M5: redundancia de parametros (c3-m5-32)
# ==========================================================================
cat('\n=== M5: redundancia de parametros (c3-m5-32) ===\n')
set.seed(11)
y <- arima.sim(n = 200, list(ar = 0.5, ma = -0.45))
ajuste <- arima(y, order = c(1, 0, 1))
print(round(cbind(coef = coef(ajuste), ee = sqrt(diag(ajuste$var.coef))), 4))
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
print(c(arma11 = aicc(ajuste, 200), ar1 = aicc(arima(y, order = c(1, 0, 0)), 200), ruido = aicc(arima(y, order = c(0, 0, 0)), 200)))
cat("suma:", round(coef(ajuste)[1]+coef(ajuste)[2],4), "\n")

# ==========================================================================
# M6-M8: arima.sim, varianza sin calentamiento, Yule-Walker, residuales, verosimilitud anidada (c3-m6-05, c3-m7-11, c3-m8-18, c3-m8-24)
# ==========================================================================
cat('\n=== M6-M8: arima.sim, varianza sin calentamiento, Yule-Walker, residuales, verosimilitud anidada (c3-m6-05, c3-m7-11, c3-m8-18, c3-m8-24) ===\n')
cat("R", R.version.string, "\n")
set.seed(3)
r <- try(arima.sim(n = 100, model = list(ar = 1)), silent = TRUE)
cat("ar=1 ->", conditionMessage(attr(r, "condition")), "\n")
x <- arima.sim(n = 100, model = list(order = c(0, 1, 0)))
cat("length order(0,1,0):", length(x), " first value:", as.numeric(x)[1], "\n")
# varianza en t=5 y estacionaria, phi=.95
phi <- .95
cat("Var t=5:", round((1 - phi^10)/(1 - phi^2), 3), " estacionaria:", round(1/(1 - phi^2), 3), "\n")
manchas <- window(sunspot.year, start = 1770, end = 1869)
cat("T =", length(manchas), " sunspot.year:", start(sunspot.year)[1], end(sunspot.year)[1], length(sunspot.year), "\n")
yw <- ar(manchas, order.max = 2, aic = FALSE, method = "yule-walker")
cat("YW:", round(yw$ar, 4), " var.pred:", round(yw$var.pred, 2), "\n")
# divisor n a mano
xc <- manchas - mean(manchas); n <- length(xc)
g <- sapply(0:2, function(k) sum(xc[(k+1):n] * xc[1:(n-k)]) / n)
r1 <- g[2]/g[1]; r2 <- g[3]/g[1]
phi1 <- r1*(1-r2)/(1-r1^2); phi2 <- (r2-r1^2)/(1-r1^2)
cat("YW a mano divisor n:", round(c(phi1, phi2), 4), "\n")
gk <- sapply(0:2, function(k) sum(xc[(k+1):n] * xc[1:(n-k)]) / (n-k))
r1 <- gk[2]/gk[1]; r2 <- gk[3]/gk[1]
cat("YW a mano divisor n-k:", round(c(r1*(1-r2)/(1-r1^2), (r2-r1^2)/(1-r1^2)), 4), "\n")
cat("acf cov lag1 R:", acf(manchas, type="covariance", plot=FALSE)$acf[2], " a mano /n:", g[2], "\n")
ml <- arima(manchas, order = c(2, 0, 0), method = "ML")
css <- arima(manchas, order = c(2, 0, 0), method = "CSS")
cat("ML:", round(coef(ml), 4), " sigma2:", round(ml$sigma2, 2), " CSS sigma2:", round(css$sigma2,2), "\n")
# residuos AR(2) por ML
res <- residuals(ml)
cat("residuals(ml)[1:4]:", round(as.numeric(res)[1:4], 3), "\n")
# gamma0/sigma2 del AR(2)
phis <- coef(ml)[1:2]
g0s2 <- 1/(1 - sum(phis * ARMAacf(ar = phis, lag.max = 2)[2:3]))
cat("gamma0/sigma2:", round(g0s2, 3), " sqrt:", round(sqrt(g0s2), 3), "\n")
# AICc: nested loglik monotone
rejilla <- list(c(1,0), c(2,0), c(3,0), c(4,0), c(0,1), c(0,2), c(0,3), c(1,1), c(2,1), c(1,2), c(2,2))
ll <- sapply(rejilla, function(pq) { a <- arima(manchas, order = c(pq[1], 0, pq[2]), method = "ML"); as.numeric(logLik(a)) })
names(ll) <- sapply(rejilla, function(pq) sprintf("(%d,%d)", pq[1], pq[2]))
print(round(ll, 3))
cat("anidados AR1<=AR2<=AR3<=AR4:", all(diff(ll[c("(1,0)","(2,0)","(3,0)","(4,0)")]) >= 0), "\n")
cat("anidados (2,0)<=(2,1)<=(2,2):", all(diff(ll[c("(2,0)","(2,1)","(2,2)")]) >= 0), " (1,1)<=(2,1)<=(2,2):", all(diff(ll[c("(1,1)","(2,1)","(2,2)")]) >= 0), " (0,1)<=(0,2)<=(0,3):", all(diff(ll[c("(0,1)","(0,2)","(0,3)")]) >= 0), "\n")
# AR(1) caso T=40, phi=.95
set.seed(1)
z <- arima.sim(list(ar = 0.95), n = 40)
cat("CSS:", round(coef(arima(z, order = c(1, 0, 0), include.mean = FALSE, method = "CSS")), 4),
    " ML:", round(coef(arima(z, order = c(1, 0, 0), include.mean = FALSE, method = "ML")), 4), "\n")

# ==========================================================================
# M7-M8: tasa de rechazo con y sin fitdf, sesgo de Yule-Walker, Var(r_k) (c3-m8-15, -35, c3-m7-13, c3-m8-11)
# ==========================================================================
cat('\n=== M7-M8: tasa de rechazo con y sin fitdf, sesgo de Yule-Walker, Var(r_k) (c3-m8-15, -35, c3-m7-13, c3-m8-11) ===\n')
# 1. Monte Carlo de la tasa de rechazo (la del capitulo)
set.seed(8)
p_valores <- replicate(3000, {
  y <- arima.sim(list(ar = c(1.4, -0.7)), n = 100)
  e <- residuals(suppressWarnings(arima(y, order = c(2, 0, 0), method = "ML")))
  c(sin_fitdf = Box.test(e, lag = 12, type = "Ljung-Box")$p.value,
    con_fitdf = Box.test(e, lag = 12, type = "Ljung-Box", fitdf = 2)$p.value)
})
cat("tasa de rechazo al 5%:\n"); print(round(rowMeans(p_valores < 0.05), 4))
# 2. Sesgo de YW en AR(2) corto: coef de ML de las manchas, T = 100
set.seed(11)
phi <- c(1.4059, -0.7111); B <- 2000; T <- 100
est <- replicate(B, {
  y <- arima.sim(list(ar = phi), n = T)
  yw <- ar(y, order.max = 2, aic = FALSE, method = "yule-walker")$ar
  ml <- suppressWarnings(coef(arima(y, order = c(2, 0, 0), method = "ML"))[1:2])
  c(yw, ml, 1/sqrt(-yw[2]), 1/sqrt(-ml[2]))
})
rownames(est) <- c("yw1","yw2","ml1","ml2","mod_yw","mod_ml")
cat("verdadero:", phi, " modulo raiz verdadero:", round(1/sqrt(-phi[2]), 4), "\n")
print(round(rowMeans(est), 4))
cat("media YW - verdadero:", round(rowMeans(est)[1:2] - phi, 4), "\n")
cat("sd:", round(apply(est, 1, sd), 4), "\n")
cat("fraccion de replicas con modulo YW > modulo verdadero:", round(mean(est["mod_yw",] > 1/sqrt(-phi[2])), 3), "\n")
# 3. AR(1) phi=.95, T=100: media de YW
set.seed(111)
e1 <- replicate(2000, { y <- arima.sim(list(ar = .95), n = 100); ar(y, order.max = 1, aic = FALSE, method = "yw")$ar })
cat("AR(1) phi=.95 T=100: media YW =", round(mean(e1), 3), "\n")
# 4. Var(r_k) de ruido blanco frente a (T-k)/(T(T+2))
set.seed(5)
Tn <- 50; ks <- c(1, 2, 5, 10, 20)
R <- replicate(100000, { x <- rnorm(Tn); a <- acf(x, lag.max = 20, plot = FALSE)$acf[-1]; a[ks] })
v <- apply(R, 1, var)
cat("T = 50, Var(r_k) simulada:   ", round(v, 5), "\n")
cat("(T-k)/(T(T+2)):              ", round((Tn - ks)/(Tn*(Tn+2)), 5), "\n")
cat("1/T:                         ", round(rep(1/Tn, length(ks)), 5), "\n")

# ==========================================================================
# M7: CSS frente a ML con T = 40, doce semillas (c3-m7-11, c3-m7-34)
# ==========================================================================
cat('\n=== M7: CSS frente a ML con T = 40, doce semillas (c3-m7-11, c3-m7-34) ===\n')
# 2. CSS frente a ML con T = 40 y phi = 0.95, mil réplicas por semilla, doce semillas
r <- t(sapply(1:12, function(s) {
  set.seed(s)
  rr <- replicate(1000, {
    z <- arima.sim(list(ar = 0.95), n = 40)
    c(css = tryCatch(coef(arima(z, order = c(1, 0, 0), include.mean = FALSE, method = "CSS"))[[1]], error = function(e) NA),
      ml  = tryCatch(coef(arima(z, order = c(1, 0, 0), include.mean = FALSE, method = "ML"))[[1]],  error = function(e) NA))
  })
  c(css_mayor_1 = 100 * mean(rr["css", ] > 1, na.rm = TRUE), ml_999 = 100 * mean(rr["ml", ] >= 0.999, na.rm = TRUE),
    ml_falla = sum(is.na(rr["ml", ])))
}))
print(round(r, 1))
cat("CSS > 1: de", min(r[, 1]), "a", max(r[, 1]), "% | ML >= 0.999: de", min(r[, 2]), "a", max(r[, 2]),
    "% | ML sin estimacion: de", min(r[, 3]), "a", max(r[, 3]), "por mil\n")

# ==========================================================================
# M7: componentes del objeto arima; saturacion de la varianza
# ==========================================================================
cat('\n=== M7: componentes del objeto arima; saturacion de la varianza ===\n')
manchas <- window(sunspot.year, start = 1770, end = 1869)
ml <- arima(manchas, order = c(2,0,0), method = "ML")
print(names(ml))
cat("tiene aicc:", "aicc" %in% names(ml), "\n")
cat("t sat: ", round(((1-0.95^(2*(1:60)))/(1-0.95^2))/(1/(1-0.95^2)),3)[c(5,22)], "\n")
cat("primer t con >= 90 %:", which((1-0.95^(2*(1:100))) >= 0.9)[1], "\n")

# ==========================================================================
# M9: lambda = 1 - b (c3-m9-41)
# ==========================================================================
cat('\n=== M9: lambda = 1 - b (c3-m9-41) ===\n')
# Comprobacion de lambda = 1 - b: si sd ~ media^b, la potencia y^(1-b) deja la desviacion constante
set.seed(2026)
elast <- function(x, k) {
  g <- rep(seq_len(length(x) %/% k), each = k); x <- as.numeric(x)[seq_along(g)]
  niv <- tapply(x, g, mean); amp <- tapply(x, g, sd)
  coef(lm(log(amp) ~ log(niv)))[[2]]
}
sim <- function(b, bloques = 400, k = 25) {
  mu <- exp(seq(log(50), log(2000), length.out = bloques))      # niveles bien separados
  y <- unlist(lapply(mu, function(m) m + 0.05 * m^b * rnorm(k) * 10^(1 - b) / 1))  # sd = 0.05*10^(1-b) * m^b
  # que sd sea proporcional a m^b: se comprueba abajo con la elasticidad de la serie original
  y
}
for (b in c(0.5, 0.75, 1)) {
  y <- sim(b)
  y <- pmax(y, 1e-6)
  lam <- 1 - b
  yt <- if (lam == 0) log(y) else y^lam
  cat(sprintf("b = %.2f: elasticidad en la serie original = %.3f | tras la potencia lambda = 1-b = %.2f: elasticidad de la desviacion frente al nivel = %.3f\n",
              b, elast(y, 25), lam,
              # elasticidad de la amplitud frente al NIVEL ORIGINAL: pendiente de log(sd(yt)) contra log(media(y))
              { g <- rep(seq_len(length(y) %/% 25), each = 25)
                coef(lm(log(tapply(yt, g, sd)) ~ log(tapply(y, g, mean))))[[2]] }))
}

# ==========================================================================
# M9: Guerrero con un cero; cuerpo de forecast:::guer.cv (c3-m9-05, c3-m9-43)
# ==========================================================================
cat('\n=== M9: Guerrero con un cero; cuerpo de forecast:::guer.cv (c3-m9-05, c3-m9-43) ===\n')
suppressMessages(library(forecast))
manchas <- window(sunspot.year, start = 1770, end = 1869)
cat("min:", min(manchas), " ceros en la ventana:", sum(manchas == 0), " ceros serie completa:", sum(sunspot.year == 0), "\n")
cat("--- BoxCox.lambda guerrero sobre la serie cruda (con un cero):\n")
l0 <- withCallingHandlers(BoxCox.lambda(manchas, method = "guerrero"),
  warning = function(w) { cat("AVISO:", conditionMessage(w), "\n"); invokeRestart("muffleWarning") })
cat("lambda cruda:", round(l0, 4), "\n")
cat("lambda desplazada (+1):", round(BoxCox.lambda(manchas + 1, method = "guerrero"), 4), "\n")
cat("--- cuerpo de forecast:::guer.cv:\n")
print(forecast:::guer.cv)

# ==========================================================================
# M9: periodo de FPP3 y pico de la densidad espectral (c3-m9-45)
# ==========================================================================
cat('\n=== M9: periodo de FPP3 y pico de la densidad espectral (c3-m9-45) ===\n')
phi <- c(1.4027, -0.6853)
dens <- function(w) 1 / Mod(1 - phi[1] * exp(-1i * w) - phi[2] * exp(-2i * w))^2
o <- optimize(dens, c(0.01, pi / 2), maximum = TRUE)$maximum
cat("periodo del maximo de la densidad espectral (2*pi/omega_max):", round(2 * pi / o, 4), "\n")
cat("formula FPP3 (9.5):", round(2 * pi / acos(-phi[1] * (1 - phi[2]) / (4 * phi[2])), 4), "\n")
cat("angulo de la raiz:", round(2 * pi / Arg(polyroot(c(1, -phi))[1]), 4), "\n")
# se juntan cuando |raiz| -> 1: AR(2) con angulo fijo w0 = 0.5601 y R = 1/|raiz| creciente
w0 <- 0.5601
for (R in c(0.5, 0.8278, 0.95, 0.99, 0.999)) {
  p1 <- 2 * R * cos(w0); p2 <- -R^2
  f <- function(w) 1 / Mod(1 - p1 * exp(-1i * w) - p2 * exp(-2i * w))^2
  om <- optimize(f, c(0.01, pi / 2), maximum = TRUE)$maximum
  cat(sprintf("R = %.3f: periodo del pico = %.4f ; periodo del angulo = %.4f ; formula FPP3 = %.4f\n", R, 2 * pi / om, 2 * pi / w0, 2 * pi / acos(-p1 * (1 - p2) / (4 * p2))))
}

# ==========================================================================
# M9: auto.arima(): criterio y busqueda por defecto, con y sin media (c3-m9-20, -24, -52)
# ==========================================================================
cat('\n=== M9: auto.arima(): criterio y busqueda por defecto, con y sin media (c3-m9-20, -24, -52) ===\n')
suppressMessages(library(forecast))
W <- RAIZ
trm <- ts(read.csv(file.path(W, "Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv"))$trm, start = c(2015, 1), frequency = 12)
ret <- diff(log(trm)) * 100
cat("n =", length(ret), " frequency =", frequency(ret), "\n")
cat("formals ic:", deparse(formals(auto.arima)$ic), "\n")
cat("formals approximation:", deparse(formals(auto.arima)$approximation), "\n")
cat("formals stepwise:", deparse(formals(auto.arima)$stepwise), "\n")
cat("approximation por defecto con esta serie:", (length(ret) > 150 || frequency(ret) > 12), "\n")
a0 <- auto.arima(ret)
cat("--- defecto:\n"); print(a0)
cat("arimaorder:", arimaorder(a0), "\n")
ex <- auto.arima(ret, stepwise = FALSE, approximation = FALSE)
cat("--- stepwise=FALSE, approximation=FALSE:\n"); print(ex)
ex2 <- auto.arima(ret, stepwise = FALSE)
cat("--- solo stepwise=FALSE:\n"); print(ex2)
cat("coef ma1, ee:", round(coef(ex)[["ma1"]],4), round(sqrt(ex$var.coef[1,1]),4), "\n")
cat("--- trace por defecto:\n")
invisible(auto.arima(ret, trace = TRUE))
cat("--- trace exhaustivo:\n")
invisible(auto.arima(ret, stepwise = FALSE, trace = TRUE))
