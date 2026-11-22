# R5 del capitulo 3 · cifras de la prosa, las pistas, las retros y las claves que NO salen bajo
# un "#>" del propio capitulo. Cada una con su etiqueta, que es la que cita R5_cambios.md.
# Rscript diagnostico/cap3/comprobaciones/r5_cifras.R > diagnostico/cap3/comprobaciones/r5_cifras.out 2>&1
options(width = 110, warn = 1)
e <- function(etq, ...) cat(sprintf("[%s] ", etq), ..., "\n")
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }

cat("==== Para practicar ====\n")
e("M1-01", "discriminante de 0.3 B^2 - 1.1 B + 1:", 1.1^2 - 4 * 0.3, "| raices (1.1 +- 0.1)/0.6:", (1.1 + c(-1, 1) * sqrt(1.1^2 - 1.2)) / 0.6)
e("M1-02", "1 - 1.1 B - 0.3 B^2: raiz de 1.21 + 1.2 =", round(sqrt(1.21 + 1.2), 4), "| raices (-1.1 +- eso)/0.6:", round((-1.1 + c(1, -1) * sqrt(2.41)) / 0.6, 4))
e("M1-03", "raiz de theta(B) = 1 + 0.4 B:", -1 / 0.4)
e("M2-01", "phi1/(2 sqrt(-phi2)) =", round(0.8 / (2 * sqrt(0.6)), 4), "| arccos =", round(acos(0.8 / (2 * sqrt(0.6))), 4), "rad | 2 pi / arccos =", round(2 * pi / acos(0.8 / (2 * sqrt(0.6))), 4))
e("M2-02", "rho1 = 0.8/1.6 =", 0.8 / 1.6, "| rho2 = -0.6 + 0.64/1.6 =", -0.6 + 0.64 / 1.6, "| rho3 = 0.8 rho2 - 0.6 rho1 =", 0.8 * (-0.2) - 0.6 * 0.5)
e("M2-03", "1 - phi1 rho1 - phi2 rho2 =", 1 - 0.8 * 0.5 - (-0.6) * (-0.2), "| gamma0 = 3/eso =", 3 / (1 - 0.4 - 0.12), "| mu = 4/(1 - 0.8 + 0.6) =", 4 / 0.8)
e("M2-04", "formula cerrada: (1.6 x 3)/(0.4 x (1.6^2 - 0.8^2)) =", 1.6 * 3 / (0.4 * (1.6^2 - 0.8^2)), "| 1.6^2 - 0.8^2 =", 1.6^2 - 0.8^2)
e("M2-05", "error de Monte Carlo de la media de 100000 valores de un AR(2): sd de la media ~ sqrt(gamma0 (1 + 2 sum rho)/n) =",
  round(sqrt(6.25 * (1 + 2 * sum(ARMAacf(ar = c(0.8, -0.6), lag.max = 200)[-1])) / 1e5), 4))
e("M3-01", "0.5^c(1,2,5,10,20) =", signif(0.5^c(1, 2, 5, 10, 20), 3), "| 2^c(1,2,5,10,20) =", signif(2^c(1, 2, 5, 10, 20), 3), "| 2^10 =", 2^10)
e("M3-02", "gemelo de theta = 2, sigma2 = 1: theta = 1/2, sigma2 = 4 | gamma0:", 1 * (1 + 2^2), "=", 4 * (1 + 0.5^2), "| gamma1:", 2 * 1, "=", 0.5 * 4)
psi_u <- c(1, ARMAtoMA(ar = -0.5, ma = 2, lag.max = 400))   # u_t = (1 + 2B)/(1 + 0.5B) e_t
e("M3-03", "choques del gemelo invertible, u_t = (1+2B)/(1+0.5B) e_t: pesos", round(psi_u[1:4], 4), "| Var(u) =", round(sum(psi_u^2), 4),
  "| cor(u_t, e_t) =", round(psi_u[1] / sqrt(sum(psi_u^2)), 4), "| cor(u_t, e_{t-1}) =", round(psi_u[2] / sqrt(sum(psi_u^2)), 4))
e("M4-01", "productos del pronostico con 4 terminos:", 0.3 * -1.23, 0.15 * -0.05, 0.075 * 1.00, 0.0375 * 0.69, "| suma:", sum(c(0.3, 0.15, 0.075, 0.0375) * c(-1.23, -0.05, 1.00, 0.69)))
e("M4-02", "primer peso que se deja fuera con 4: 0.3 x 0.5^4 =", 0.3 * 0.5^4, "| con 8: 0.3 x 0.5^8 =", round(0.3 * 0.5^8, 5), "| suma de todos los pesos: 0.3/(1-0.5) =", 0.3 / 0.5)
e("M4-03", "psi: 1,", 0.8 - 0.5, ",", 0.8 * 0.3, "| cuadrados:", 1, 0.3^2, 0.24^2, "| techo 1 + 0.3^2/(1-0.8^2) =", 1 + 0.09 / 0.36, "| 1.1476/1.25 =", round(1.1476 / 1.25, 4))
e("M5-01", "phi = 0.63, theta = 0.53: 1 + phi theta =", 1 + 0.63 * 0.53, "| phi + theta =", 0.63 + 0.53, "| 1 + 2 phi theta + theta^2 =", 1 + 2 * 0.63 * 0.53 + 0.53^2,
  "| rho1 =", round((1 + 0.63 * 0.53) * 1.16 / (1 + 2 * 0.63 * 0.53 + 0.53^2), 4))
w <- diff(WWWusage); a <- acf(w, lag.max = 20, plot = FALSE)$acf[-1]
e("M5-02", "diff(WWWusage): r17..r20 =", round(a[17:20], 3), "| banda", round(1.96 / sqrt(99), 3), "| rango de WWWusage:", range(WWWusage))
ar3 <- arima(w, order = c(3, 0, 0), method = "ML")
e("M5-03", "AR(3): coef", round(coef(ar3), 4), "| t de phi3 =", round(coef(ar3)[3] / sqrt(ar3$var.coef[3, 3]), 2))
e("M5-04", "AICc: AR(3) - ARMA(1,1) =", round(aicc(ar3, 99) - aicc(arima(w, order = c(1, 0, 1), method = "ML"), 99), 3),
  "| BIC: AR(3) - ARMA(1,1) =", round(BIC(ar3) - BIC(arima(w, order = c(1, 0, 1), method = "ML")), 3))
rho1 <- 0.8 / 1.64
e("M6-01", "MA(1) theta = 0.8: rho1 =", round(rho1, 4), "| sqrt(1 + 2 rho1^2) =", round(sqrt(1 + 2 * rho1^2), 4),
  "| P(|r_k| > 1.96/sqrt(T)) con esa desviacion =", round(2 * pnorm(-1.96 / sqrt(1 + 2 * rho1^2)), 4), "| x 19 =", round(19 * 2 * pnorm(-1.96 / sqrt(1 + 2 * rho1^2)), 2))
e("M6-02", "bandas: T = 50:", round(1.96 / sqrt(50), 3), "| 200:", round(1.96 / sqrt(200), 3), "| 1000:", round(1.96 / sqrt(1000), 3))
manchas <- window(sunspot.year, start = 1770, end = 1869)
mlm <- arima(manchas, order = c(2, 0, 0), method = "ML")
e("M7-01", "manchas (modulo): YW-ML en ee =", round((ar(manchas, order.max = 2, aic = FALSE)$ar - coef(mlm)[1:2]) / sqrt(diag(mlm$var.coef))[1:2], 2),
  "| modulo de las raices =", round(Mod(polyroot(c(1, -coef(mlm)[1:2])))[1], 4), "| T =", length(manchas))
x <- window(treering, start = 1880)
e("M7-02", "treering 1880-1979: T =", length(x), "| tsp de treering:", tsp(treering), "| n total:", length(treering),
  "| sigma2 YW/ML =", round(ar(x, order.max = 2, aic = FALSE)$var.pred / arima(x, order = c(2, 0, 0), method = "ML")$sigma2, 3),
  "| en las manchas:", round(298.96 / 229.43, 3))
e("M9-01", "lynx: n =", length(lynx), "| tsp:", tsp(lynx), "| bloques de 10:", length(lynx) %/% 10, "(sobran", length(lynx) %% 10, ")")
f4 <- arima(log(lynx), order = c(4, 0, 0), method = "ML"); f2 <- arima(log(lynx), order = c(2, 0, 0), method = "ML")
e("M9-02", "log(lynx): AICc AR(2) - AR(4) =", round(aicc(f2, 114) - aicc(f4, 114), 2), "| BIC AR(4) - AR(2) =", round(BIC(f4) - BIC(f2), 2),
  "| t de phi4 =", round(coef(f4)[4] / sqrt(f4$var.coef[4, 4]), 2))
g4 <- arima(lynx, order = c(4, 0, 0), method = "ML"); g2 <- arima(lynx, order = c(2, 0, 0), method = "ML")
e("M9-03", "lynx cruda: AICc AR(2) - AR(4) =", round(aicc(g2, 114) - aicc(g4, 114), 2), "| BIC AR(4) - AR(2) =", round(BIC(g4) - BIC(g2), 2))

rej <- list(c(1,0), c(2,0), c(3,0), c(4,0), c(0,1), c(0,2), c(0,3), c(1,1), c(2,1), c(1,2), c(2,2))
lb <- function(x) sapply(rej, function(pq) Box.test(residuals(suppressWarnings(arima(x, order = c(pq[1], 0, pq[2]), method = "ML"))), lag = 12, type = "Ljung-Box", fitdf = sum(pq))$p.value)
e("M9-04", "LB12 de los once candidatos, en logaritmos:", round(lb(log(lynx)), 4), "| maximo:", round(max(lb(log(lynx))), 4), "| en la cruda:", round(lb(lynx), 4))
e("M9-05", "Shapiro-Wilk de los residuales del AR(2) crudo:", signif(shapiro.test(residuals(g2))$p.value, 3), "| AICc en la cruda: ARMA(2,2) - AR(4) =", round(aicc(arima(lynx, order = c(2, 0, 2), method = "ML"), 114) - aicc(g4, 114), 2))
set.seed(34); y4 <- arima.sim(n = 200, model = list(ar = 0.8, ma = -0.5)); ps <- -ARMAtoMA(ar = 0.5, ma = -0.8, lag.max = 200)
e("M4-04", "pronostico con 200 menos pronostico con 4 (sin redondear):", round(sum(ps * rev(y4)) - sum(ps[1:4] * rev(y4)[1:4]), 4), "| con las 4 redondeadas:", round(sum(ps * rev(y4)) - sum(ps[1:4] * round(rev(y4)[1:4], 2)), 4))
e("M2-06", "gamma0/sigma2 =", 6.25 / 3)

cat("\n==== Ejercicios 1 a 3 ====\n")
ar1 <- arima(lh, order = c(1, 0, 0), method = "ML"); ma2 <- arima(lh, order = c(0, 0, 2), method = "ML")
e("E1-01", "lh: AICc AR(1) - MA(2) =", round(aicc(ar1, 48) - aicc(ma2, 48), 3), "| BIC MA(2) - AR(1) =", round(BIC(ma2) - BIC(ar1), 3),
  "| LB(10): AR(1)", round(Box.test(residuals(ar1), lag = 10, type = "Ljung-Box", fitdf = 1)$p.value, 4),
  "MA(2)", round(Box.test(residuals(ma2), lag = 10, type = "Ljung-Box", fitdf = 2)$p.value, 4))
e("E1-02", "MA(2) de lh: theta =", round(coef(ma2)[1:2], 4), "| t =", round(coef(ma2)[1:2] / sqrt(diag(ma2$var.coef))[1:2], 2))
e("E2-01", "MA(2) theta = (0.9, 0.2): 1 + 0.81 + 0.04 =", 1 + 0.81 + 0.04, "| 0.9 + 0.18 =", 0.9 + 0.18, "| rho1 =", round(1.08 / 1.85, 4), "| rho2 =", round(0.2 / 1.85, 4),
  "| triangulo:", 0.9 + 0.2 > -1, 0.2 - 0.9 > -1, abs(0.2) < 1)
e("E2-02", "theta = (2.4, 0.8): 1 + 5.76 + 0.64 =", 1 + 2.4^2 + 0.8^2, "| 2.4 + 1.92 =", 2.4 + 2.4 * 0.8, "| rho1 =", round(4.32 / 7.4, 4), "| rho2 =", round(0.8 / 7.4, 4),
  "| cociente de varianzas 7.4/1.85 =", 7.4 / 1.85)
e("E2-03", "los cuatro MA(2) con esa ACF (se invierte una raiz, la otra o las dos):")
for (th in list(c(0.9, 0.2), c(2.4, 0.8), c(3.0, 1.25)[c(1, 2)], c(4.5, 5))) cat("      theta =", th, "| rho =", round(ARMAacf(ma = th, lag.max = 2)[-1], 4), "| |raices| =", round(sort(Mod(polyroot(c(1, th)))), 4), "\n")
e("E2-04", "techo de rho1 en un MA(2): cos(pi/4) =", round(cos(pi / 4), 4), "(modulo 3, c3-m3-12)")

cat("\n==== Quiz ====\n")
e("Q1-01", "1 - 1.2 B + 0.9 B^2: |raices| =", round(Mod(polyroot(c(1, -1.2, 0.9))), 4), "| phi1 + phi2 con los signos bien =", 1.2 - 0.9, "| leidos mal =", -1.2 + 0.9)
th <- c(0.6, -0.3); s2 <- 4
e("Q2-01", "MA(2) theta = (0.6, -0.3), sigma2 = 4: gamma1 = sigma2 (theta1 + theta1 theta2) =", s2 * (th[1] + th[1] * th[2]), "| gamma0 =", s2 * (1 + sum(th^2)), "| gamma2 =", s2 * th[2])
e("Q2-02", "comprobacion con ARMAacf: gamma0 x rho =", round(s2 * (1 + sum(th^2)) * ARMAacf(ma = th, lag.max = 2)[-1], 4), "| invertible:", all(Mod(polyroot(c(1, th))) > 1))
e("Q2-03", "tropiezos: solo un choque compartido, sigma2 theta1 =", s2 * th[1], "| sin sigma2 =", th[1] + th[1] * th[2], "| rho1 =", round((th[1] + th[1] * th[2]) / (1 + sum(th^2)), 4),
  "| signo de theta2 perdido =", s2 * (th[1] + th[1] * abs(th[2])), "| gamma2 =", s2 * th[2])
phi <- 0.6; theta <- -0.2; s2 <- 5
psi <- c(1, ARMAtoMA(ar = phi, ma = theta, lag.max = 3))
e("Q4-01", "ARMA(1,1) phi = 0.6, theta = -0.2, sigma2 = 5: psi =", psi[1:3], "| Var(e_{T+2}) =", s2 * sum(psi[1:2]^2))
e("Q4-02", "tropiezos: sin sigma2 =", sum(psi[1:2]^2), "| sin psi0 =", s2 * psi[2]^2, "| psi1 = phi =", s2 * (1 + phi^2), "| psi1 = phi - theta (signo) =", s2 * (1 + (phi - theta)^2),
  "| sin cuadrados =", s2 * sum(psi[1:2]), "| hasta j = h =", round(s2 * sum(psi[1:3]^2), 3))
e("Q5-01", "MA(1) theta = -2.5: rho1 =", round(-2.5 / (1 + 2.5^2), 4), "| con theta = -0.4:", round(-0.4 / (1 + 0.4^2), 4), "| sigma2 del gemelo = 2.5^2 =", 2.5^2,
  "| gamma0:", 1 + 2.5^2, "=", 6.25 * (1 + 0.4^2), "| raiz de theta(B):", 1 / 2.5)
e("Q5-02", "pesos pi con theta = -2.5 (pi_j = (-theta)^j):", (2.5)^(1:4))
set.seed(35); y5 <- arima.sim(n = 2000, model = list(ma = -2.5)); m5 <- arima(y5, order = c(0, 0, 1), include.mean = FALSE)
e("Q5-03", "simulado con theta = -2.5, sigma2 = 1, n = 2000 (set.seed(35)): arima() devuelve theta =", round(coef(m5)[["ma1"]], 4), "sigma2 =", round(m5$sigma2, 4))

# Q6: una salida REAL de arima() con el patron phi ~ -theta. Ruido blanco simulado (T = 100) al que
# se ajusta un ARMA(1,1) por ML. Entre las semillas 1 a 400, las que dan |phi| entre 0.5 y 0.9,
# |phi + theta| < 0.1 y errores estandar entre 0.3 y 0.6 son 28 (lista en [Q6-00]); se toma la 329,
# la mas parecida a la salida escrita a mano que traia el item (-0.64 y 0.69, ee 0.38 y 0.36).
busca <- function(s) {
  set.seed(s); y <- rnorm(100); av <- NULL
  f <- withCallingHandlers(arima(y, order = c(1, 0, 1), method = "ML"),
                           warning = function(w) { av <<- conditionMessage(w); invokeRestart("muffleWarning") })
  ee <- suppressWarnings(sqrt(diag(f$var.coef)))
  list(s = s, y = y, f = f, ee = ee, av = av,
       ok = abs(coef(f)[1]) > 0.5 && abs(coef(f)[1]) < 0.9 && abs(coef(f)[1] + coef(f)[2]) < 0.1 && all(ee[1:2] > 0.3) && all(ee[1:2] < 0.6))
}
cand <- Filter(function(r) isTRUE(r$ok), lapply(1:400, function(s) tryCatch(busca(s), error = function(e) list(ok = FALSE))))
e("Q6-00", "semillas de 1 a 400 que cumplen:", sapply(cand, `[[`, "s"))
r <- busca(329); f <- r$f; y <- r$y
e("Q6-01", "set.seed(329); y <- rnorm(100); arima(y, order = c(1,0,1), method = 'ML'): phi =", sprintf("%.2f", coef(f)[["ar1"]]), "(ee", sprintf("%.2f", r$ee[1]), ") theta =", sprintf("%.2f", coef(f)[["ma1"]]), "(ee", sprintf("%.2f", r$ee[2]), ")",
  "| aviso:", if (is.null(r$av)) "ninguno" else r$av)
e("Q6-02", "con mas decimales: phi =", round(coef(f)[["ar1"]], 4), "theta =", round(coef(f)[["ma1"]], 4), "| ee:", round(r$ee[1:2], 4),
  "| cocientes:", round(coef(f)[1:2] / r$ee[1:2], 2), "| suma phi + theta =", round(coef(f)[["ar1"]] + coef(f)[["ma1"]], 4))
e("Q6-03", "con los valores redondeados a 2 decimales: |phi|/ee =", round(0.60 / 0.38, 2), "| |theta|/ee =", round(0.67 / 0.35, 2), "| suma =", -0.60 + 0.67, "(los dos cocientes, por debajo de 1.96 de las dos maneras)")
e("Q6-04", "AICc: ARMA(1,1)", round(aicc(f, 100), 2), "| AR(1)", round(aicc(arima(y, order = c(1, 0, 0), method = "ML"), 100), 2),
  "| MA(1)", round(aicc(arima(y, order = c(0, 0, 1), method = "ML"), 100), 2), "| ruido blanco", round(aicc(arima(y, order = c(0, 0, 0), method = "ML"), 100), 2))
p <- c(0.9, -0.5)
e("Q7-01", "AR(2) phi = (0.9, -0.5): phi1^2 + 4 phi2 =", p[1]^2 + 4 * p[2], "| sqrt(-phi2) =", round(sqrt(-p[2]), 4), "| argumento =", round(p[1] / (2 * sqrt(-p[2])), 4),
  "| arccos =", round(acos(p[1] / (2 * sqrt(-p[2]))), 4), "rad | pseudo-periodo =", round(2 * pi / acos(p[1] / (2 * sqrt(-p[2]))), 4),
  "| por las raices:", round(2 * pi / Arg(polyroot(c(1, -p))[1]), 4), "| triangulo:", p[1] + p[2] < 1, p[2] - p[1] < 1, abs(p[2]) < 1)
e("Q7-02", "tropiezos: arccos en grados =", round(acos(p[1] / (2 * sqrt(-p[2]))) * 180 / pi, 2), "-> 2 pi / grados =", round(2 * pi / (acos(p[1] / (2 * sqrt(-p[2]))) * 180 / pi), 2),
  "| sin la raiz, phi1/(2 x 0.5) =", p[1] / (2 * 0.5), "->", round(2 * pi / acos(p[1] / (2 * 0.5)), 2),
  "| la otra formula (periodo medio, Modulo 9):", round(2 * pi / acos(-p[1] * (1 - p[2]) / (4 * p[2])), 2))
f1 <- arima(manchas, order = c(1, 0, 0), method = "ML"); r1 <- acf(residuals(f1), lag.max = 20, plot = FALSE)$acf[-1]
e("Q9-01", "residuales del AR(1) de las manchas: r1 =", round(r1[1], 4), "| banda", round(1.96 / sqrt(100), 3), "| r1/banda =", round(r1[1] / (1.96 / sqrt(100)), 2),
  "| fuera:", which(abs(r1) > 1.96 / sqrt(100)), "| LB12 p =", signif(Box.test(residuals(f1), lag = 12, type = "Ljung-Box", fitdf = 1)$p.value, 3))
e("Q3-01", "MA(2) theta = (0.6, 0.4), el del grafico (PROCESOS.ma2): ACF =", round(ARMAacf(ma = c(0.6, 0.4), lag.max = 4)[-1], 4))
