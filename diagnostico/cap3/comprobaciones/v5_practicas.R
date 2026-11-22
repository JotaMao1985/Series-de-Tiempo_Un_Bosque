# Verificador independiente R5 cap. 3: los ocho "Para practicar" (M1-M7, M9)
# Cada bloque recalcula lo que afirma el ejercicio, con nombres propios.
suppressPackageStartupMessages(library(forecast))
h <- function(...) cat("\n##", ..., "\n")

h("M1 · raices")
A <- c(1, -1.1, 0.3); print(polyroot(A)); print(Mod(polyroot(A)))
print(polyroot(c(1, -1.1, -0.3))); print(polyroot(rev(A)))
print(polyroot(c(1, -1.5, 0.5))); print(polyroot(c(1, 0.4)))
cat("discriminante 1.21-1.2 =", 1.1^2 - 4*0.3, "\n")

h("M2 · AR(2) c=4, phi=(0.8,-0.6), s2=3")
f1 <- 0.8; f2 <- -0.6; s2 <- 3
cat("triangulo:", f1+f2, f2-f1, abs(f2), " disc:", f1^2+4*f2, " |raiz|:", Mod(polyroot(c(1,-f1,-f2))), "\n")
w <- acos(f1/(2*sqrt(-f2))); cat("arg acos:", f1/(2*sqrt(-f2)), " acos:", w, " P:", 2*pi/w, "\n")
r <- ARMAacf(ar = c(f1,f2), lag.max = 3); print(r)
cat("mu:", 4/(1-f1-f2), " g0 YW:", s2/(1-f1*r[2]-f2*r[3]), " g0 cerrada:", s2*(1-f2)/((1+f2)*((1-f2)^2-f1^2)), "\n")
set.seed(32); y <- 5 + arima.sim(n = 1e5, model = list(ar = c(f1,f2)), sd = sqrt(s2))
cat("media y var (seed 32):", mean(y), var(y), "\n")

h("M3 · reconstruccion de choques")
set.seed(33); e <- rnorm(501); et <- e[-1]; et1 <- e[-501]
ya <- et + 0.5*et1; yb <- et + 2*et1
rec <- function(y, th) { out <- numeric(length(y)); prev <- 0
  for (t in seq_along(y)) { out[t] <- y[t] - th*prev; prev <- out[t] }; out }
cat("|e0|:", abs(e[1]), "\n")
cat("err th=0.5:", abs(rec(ya,0.5)-et)[c(1,2,5,10,20)], "\n")
cat("teorico |th|^t|e0|:", 0.5^c(1,2,5,10,20)*abs(e[1]), "\n")
cat("err th=2:", abs(rec(yb,2)-et)[c(1,2,5,10,20)], "\n")
cat("teorico:", 2^c(1,2,5,10,20)*abs(e[1]), "\n")
m <- arima(yb, order = c(0,0,1), include.mean = FALSE)
cat("arima th, s2:", coef(m), m$sigma2, "\n")
cat("cor res con e_t, e_t-1:", cor(residuals(m), et), cor(residuals(m), et1), " teoricas 1/2, 1.5/2:", 0.5, 0.75, "\n")
print(acf(residuals(m), lag.max = 3, plot = FALSE)$acf[-1])

h("M4 · ARMA(1,1) phi=0.8 theta=-0.5")
ph <- 0.8; th <- -0.5
pi_w <- ARMAtoMA(ar = -th, ma = -ph, lag.max = 6); print(pi_w)
# comprobacion directa: coeficientes de (1-0.8B)/(1-0.5B)
# (1-0.8B) * sum_j 0.5^j B^j : coef de B^j = 0.5^j - 0.8*0.5^(j-1)
cat("pi por producto de series:", sapply(1:6, function(j) 0.5^j - 0.8*0.5^(j-1)), "\n")
cat("suma de -pi:", sum(-ARMAtoMA(ar = -th, ma = -ph, lag.max = 500)), "\n")
set.seed(34); y <- arima.sim(n = 200, model = list(ar = ph, ma = th))
ult <- rev(y)[1:4]; cat("ultimas:", ult, " redondeadas:", round(ult,2), "\n")
wt <- -ARMAtoMA(ar = -th, ma = -ph, lag.max = 200)
cat("a mano 4 red.:", sum(wt[1:4]*round(ult,2)), " k=4:", sum(wt[1:4]*rev(y)[1:4]),
    " k=8:", sum(wt[1:8]*rev(y)[1:8]), " k=200:", sum(wt*rev(y)), "\n")
mm <- arima(y, order = c(1,0,1), include.mean = FALSE, fixed = c(ph, th), transform.pars = FALSE)
cat("predict:", predict(mm, 1)$pred, "  pi_5:", pi_w[5], "\n")
psi <- c(1, ARMAtoMA(ar = ph, ma = th, lag.max = 2)); cat("psi:", psi, " cumsum psi^2:", cumsum(psi^2), "\n")
g0 <- 1 + (ph+th)^2/(1-ph^2); cat("techo:", g0, " frac h3:", cumsum(psi^2)[3]/g0, "\n")

h("M5 · diff(WWWusage)")
w <- diff(WWWusage); n <- length(w); b <- 1.96/sqrt(n); cat("n, banda:", n, b, "\n")
a <- acf(w, lag.max = 20, plot = FALSE)$acf[-1]; p <- as.numeric(pacf(w, lag.max = 20, plot = FALSE)$acf)
cat("ACF fuera:", which(abs(a) > b), "\n  signos 17-20:", round(a[17:20],3), "\n")
cat("PACF fuera:", which(abs(p) > b), "\n"); print(round(a[1:6],3)); print(round(p[1:6],3))
ar3 <- arima(w, order = c(3,0,0), method = "ML"); a11 <- arima(w, order = c(1,0,1), method = "ML")
print(coef(a11))
ph <- 0.63; th <- 0.53; r1 <- (1+ph*th)*(ph+th)/(1+2*ph*th+th^2)
cat("rho1..3 (0.63,0.53):", r1*ph^(0:2), " partes:", 1+ph*th, ph+th, 1+2*ph*th+th^2, "\n")
print(round(rbind(ARMAacf(ar = coef(ar3)[1:3], lag.max = 6)[-1],
  ARMAacf(ar = coef(a11)[1], ma = coef(a11)[2], lag.max = 6)[-1]), 3))
# AICc del capitulo frente a forecast::Arima
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
cat("AICc cap:", aicc(ar3, n), aicc(a11, n), " BIC:", BIC(ar3), BIC(a11), "\n")
cat("AICc forecast::Arima:", Arima(w, order = c(3,0,0), method = "ML")$aicc, Arima(w, order = c(1,0,1), method = "ML")$aicc, "\n")
cat("LB12:", Box.test(residuals(ar3), 12, "Ljung-Box", fitdf = 3)$p.value, Box.test(residuals(a11), 12, "Ljung-Box", fitdf = 2)$p.value, "\n")
cat("auto.arima sobre WWWusage (contexto):", as.character(auto.arima(WWWusage)), "\n")

h("M6 · regla del 5 %")
cat("binomial: E=1, P0=", dbinom(0,20,0.05), " P>=2=", 1-pbinom(1,20,0.05), "\n")
fuera <- function(x, rez = 1:20) { r <- acf(x, lag.max = 20, plot = FALSE)$acf[-1]; sum(abs(r[rez]) > 1.96/sqrt(length(x))) }
sim_rb <- function(seed) { set.seed(seed); t(sapply(c(50,200,1000), function(n) { k <- replicate(2000, fuera(rnorm(n)))
  c(T = n, media = mean(k), ninguna = mean(k == 0), dos = mean(k >= 2)) })) }
print(round(sim_rb(36), 3)); cat("otra semilla (2026):\n"); print(round(sim_rb(2026), 3))
# Expectativa aproximada con Var(r_k) = (T-k)/(T(T+2)) y media -1/T (Gaussiano)
esp <- function(Tn) sum(sapply(1:20, function(k) { s <- sqrt((Tn-k)/(Tn*(Tn+2))); m <- -1/Tn; c0 <- 1.96/sqrt(Tn)
  pnorm(-c0, m, s) + 1 - pnorm(c0, m, s) }))
cat("esperado aprox. (T-k)/(T(T+2)):", sapply(c(50,200,1000), esp), "\n")
set.seed(36); ma <- replicate(2000, fuera(arima.sim(n = 200, model = list(ma = 0.8)), rez = 2:20))
cat("MA(1): media", mean(ma), " P>=2", mean(ma >= 2), "\n")
r1 <- 0.8/1.64; anch <- 1.96*sqrt((1+2*r1^2)/200); cat("bandas:", 1.96/sqrt(200), anch, "\n")
set.seed(36); ma2 <- replicate(2000, { x <- arima.sim(n = 200, model = list(ma = 0.8)); r <- acf(x, lag.max = 20, plot = FALSE)$acf[-1]; sum(abs(r[2:20]) > anch) })
cat("con banda ancha:", mean(ma2), "\n")
set.seed(99); ma3 <- replicate(2000, fuera(arima.sim(n = 200, model = list(ma = 0.8)), rez = 2:20)); cat("MA(1) otra semilla:", mean(ma3), mean(ma3>=2), "\n")

h("M7 · treering 1880-1979")
x <- window(treering, start = 1880); cat("T:", length(x), "\n")
yw <- ar(x, order.max = 2, aic = FALSE, method = "yule-walker"); css <- arima(x, order = c(2,0,0), method = "CSS"); ml <- arima(x, order = c(2,0,0), method = "ML")
print(rbind(yw$ar, coef(css)[1:2], coef(ml)[1:2]))
ee <- sqrt(diag(ml$var.coef))[1:2]; cat("ee:", ee, " YW-ML/ee:", (yw$ar-coef(ml)[1:2])/ee, " CSS-ML/ee:", (coef(css)[1:2]-coef(ml)[1:2])/ee, "\n")
cat("s2:", yw$var.pred, css$sigma2, ml$sigma2, " ratio YW/ML:", yw$var.pred/ml$sigma2, "  manchas 298.96/229.43:", 298.96/229.43, "\n")
cat("|raices| ML:", Mod(polyroot(c(1,-coef(ml)[1:2]))), "  phi=(1.40,-0.70):", Mod(polyroot(c(1,-1.4,0.7))), " phi=(0.14,0.21):", Mod(polyroot(c(1,-0.14,-0.21))), "\n")
dist <- function(phi) { d <- replicate(500, { s <- arima.sim(n = 100, model = list(ar = phi))
  f <- tryCatch(arima(s, order = c(2,0,0), method = "ML"), error = function(e) NULL)
  yw <- ar(s, order.max = 2, aic = FALSE, method = "yule-walker")$ar
  if (is.null(f)) c(NA,NA) else abs(yw - coef(f)[1:2])/sqrt(diag(f$var.coef))[1:2] }); c(rowMeans(d, na.rm = TRUE), na = sum(is.na(d[1,]))) }
set.seed(37); cat("seed 37 lejos:", dist(c(0.14,0.21)), "\n"); cat("seed 37 cerca:", dist(c(1.40,-0.70)), "\n")
set.seed(4242); cat("seed 4242 lejos:", dist(c(0.14,0.21)), "\n"); cat("seed 4242 cerca:", dist(c(1.40,-0.70)), "\n")

h("M9 · lynx")
elasticidad <- function(x, k) { g <- rep(seq_len(length(x) %/% k), each = k); x <- as.numeric(x)[seq_along(g)]
  niv <- tapply(x, g, mean); amp <- tapply(x, g, sd); aj <- lm(log(amp) ~ log(niv)); c(b = coef(aj)[[2]], confint(aj)[2, ], R2 = summary(aj)$r.squared) }
print(round(elasticidad(lynx, 10), 4)); cat("min:", min(lynx), " guerrero:", BoxCox.lambda(lynx, method = "guerrero"), "\n")
rej <- list(c(1,0), c(2,0), c(3,0), c(4,0), c(0,1), c(0,2), c(0,3), c(1,1), c(2,1), c(1,2), c(2,2))
tabla <- function(x) do.call(rbind, lapply(rej, function(pq) { aj <- arima(x, order = c(pq[1],0,pq[2]), method = "ML")
  data.frame(mod = sprintf("ARMA(%d,%d)", pq[1], pq[2]), AICc = aicc(aj, length(x)), BIC = BIC(aj),
    LB12 = Box.test(residuals(aj), 12, "Ljung-Box", fitdf = sum(pq))$p.value) }))
cat("-- sin suppressWarnings (como el modulo):\n")
cr <- withCallingHandlers(tabla(lynx), warning = function(w) { cat("AVISO:", conditionMessage(w), "\n"); invokeRestart("muffleWarning") })
lg <- withCallingHandlers(tabla(log(lynx)), warning = function(w) { cat("AVISO:", conditionMessage(w), "\n"); invokeRestart("muffleWarning") })
print(cr[order(cr$AICc), ], digits = 7); print(lg[order(lg$AICc), ], digits = 7)
cat("dif AR2-AR4 cruda:", cr$AICc[2]-cr$AICc[4], " log:", lg$AICc[2]-lg$AICc[4], "\n")
cat("max LB12 en log:", max(lg$LB12), " (", lg$mod[which.max(lg$LB12)], ")  pasan en cruda (p>0.05):", cr$mod[cr$LB12 > 0.05], "\n")
mira <- function(x) { f <- arima(x, order = c(2,0,0), method = "ML"); c(coef(f)[1:2], P = 2*pi/Arg(polyroot(c(1,-coef(f)[1:2]))[1]),
  LB = Box.test(residuals(f), 12, "Ljung-Box", fitdf = 2)$p.value, SW = shapiro.test(residuals(f))$p.value) }
print(rbind(mira(lynx), mira(log(lynx))), digits = 6)
