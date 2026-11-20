# R1 del capítulo 3 · comprobaciones de los errores e imprecisiones (T1.1, T1.2, T1.4)
# Ejecutar desde la raíz del repo:
#   Rscript diagnostico/cap3/comprobaciones/r1_errores.R > diagnostico/cap3/comprobaciones/r1_errores.out 2>&1
suppressPackageStartupMessages(library(forecast))
options(width = 110)
tit <- function(s) cat("\n==== ", s, " ", strrep("=", max(3, 90 - nchar(s))), "\n", sep = "")
cat(R.version.string, "· forecast", as.character(packageVersion("forecast")), "\n")

manchas <- window(sunspot.year, start = 1770, end = 1869)

# ---------------------------------------------------------------------------
tit("E1 · Ejercicio 3: Ljung-Box(12) del AR(2) en raíz, por ventana")
ventana <- function(a, b) {
  x <- sqrt(window(sunspot.year, a, b))
  f <- arima(x, order = c(2, 0, 0), method = "ML")
  r <- polyroot(c(1, -coef(f)[1:2]))
  p <- Box.test(residuals(f), lag = 12, type = "Ljung-Box", fitdf = 2)$p.value
  ee <- sqrt(diag(f$var.coef))[1:2]
  cat(sprintf("%d-%d (n=%3d): phi=(%.4f, %.4f) ee=(%.4f, %.4f) |raiz|=%.4f periodo=%6.3f LB12 p=%.6f  s2=%.4f\n",
              a, b, length(x), coef(f)[1], coef(f)[2], ee[1], ee[2], Mod(r)[1], 2 * pi / Arg(r[1]), p, f$sigma2))
  invisible(p)
}
cat("-- las cuatro del ejercicio y la de control (misma n que 1770-1869)\n")
for (v in list(c(1770, 1869), c(1700, 1988), c(1870, 1988), c(1900, 1988), c(1889, 1988))) ventana(v[1], v[2])
cat("-- otras ventanas de exactamente 100 años\n")
for (a in c(1700, 1720, 1750, 1789, 1800, 1820, 1850, 1880)) ventana(a, a + 99)
cat("-- todas las ventanas de 100 años (inicio 1700..1889): cuántas no rechazan al 5 %\n")
pp <- sapply(1700:1889, function(a) {
  x <- sqrt(window(sunspot.year, a, a + 99)); f <- arima(x, order = c(2, 0, 0), method = "ML")
  Box.test(residuals(f), lag = 12, type = "Ljung-Box", fitdf = 2)$p.value })
cat("ventanas:", length(pp), " con p > 0.05:", sum(pp > 0.05), " inicios:", (1700:1889)[pp > 0.05], "\n")
cat("p máximo:", round(max(pp), 4), "en inicio", (1700:1889)[which.max(pp)], "\n")

# ---------------------------------------------------------------------------
tit("E2 · ARMA(2,1) phi=(0.5,0.3) theta=0.4: la recursión del AR en k = 1")
r <- ARMAacf(ar = c(0.5, 0.3), ma = 0.4, lag.max = 5)
cat("rho_1 verdadero:", round(unname(r[2]), 4), "\n")
cat("con rho_{-1} = 1 (mal planteada):  0.5*1 + 0.3*1       =", round(unname(0.5 * r[1] + 0.3 * r[1]), 4), "\n")
cat("con rho_{-1} = rho_1 (bien):       0.5*rho_0 + 0.3*rho_1 =", round(unname(0.5 * r[1] + 0.3 * r[2]), 4), "\n")
cat("resuelta como AR puro: 0.5/(1-0.3) =", round(0.5 / 0.7, 4), "\n")
cat("rho_2..rho_5:", round(r[3:6], 4), " | recursión:", round(unname(0.5 * r[2:5] + 0.3 * r[1:4]), 4), "\n")

# ---------------------------------------------------------------------------
tit("E3 · Envolvente de los psi del AR(2) final")
ar2s <- arima(sqrt(manchas), order = c(2, 0, 0), method = "ML")
phi <- coef(ar2s)[1:2]; raices <- polyroot(c(1, -phi))
Rmod <- unname(sqrt(-phi[2])); w <- Arg(raices)[1]
psi <- c(1, ARMAtoMA(ar = phi, ma = numeric(0), lag.max = 24))
j <- 0:24
cat("R =", round(Rmod, 4), " omega =", round(w, 4), " sin(omega) =", round(sin(w), 4),
    " 1/sin(omega) =", round(1 / sin(w), 4), "\n")
cat("|psi_j| > R^j en", sum(abs(psi) > Rmod^j + 1e-12), "de 25; j =", j[abs(psi) > Rmod^j + 1e-12], "\n")
cat("|psi_j| > R^j/sin(omega) en", sum(abs(psi) > Rmod^j / sin(w) + 1e-12), "de 25\n")
cat("max |psi_j| / (R^j/sin w) =", round(max(abs(psi) / (Rmod^j / sin(w))), 4), "\n")
cat("vida media del envolvente: log(0.5)/log(R) =", round(log(0.5) / log(Rmod), 2), "\n")
cat("psi_0..psi_5:", round(psi[1:6], 4), "\n")
cat("cruces por cero: (j+1)*omega = k*pi -> j+1 =", round(pi / w, 2), round(2 * pi / w, 2),
    " j =", round(pi / w - 1, 2), round(2 * pi / w - 1, 2), "\n")

# ---------------------------------------------------------------------------
tit("E4/E6 · TRM: auto.arima, MA(1) con y sin media, AICc con y sin media")
d <- read.csv("Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")
trm <- ts(d$trm, start = c(2015, 1), frequency = 12)
ret <- diff(log(trm)) * 100
cat("n =", length(ret), " banda =", round(1.96 / sqrt(length(ret)), 4), "\n")
cat("ACF 1..8:", round(acf(ret, lag.max = 8, plot = FALSE)$acf[-1], 3), "\n")
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2 * k * (k + 1) / (n - k - 1) }
m_cm <- arima(ret, order = c(0, 0, 1), method = "ML")
m_sm <- arima(ret, order = c(0, 0, 1), include.mean = FALSE, method = "ML")
w_cm <- arima(ret, order = c(0, 0, 0), method = "ML")
w_sm <- arima(ret, order = c(0, 0, 0), include.mean = FALSE, method = "ML")
cat(sprintf("MA(1) con media: theta=%.4f ee=%.4f t=%.2f | media=%.4f ee=%.4f t=%.2f | AICc=%.3f\n",
            coef(m_cm)[1], sqrt(m_cm$var.coef[1, 1]), coef(m_cm)[1] / sqrt(m_cm$var.coef[1, 1]),
            coef(m_cm)[2], sqrt(m_cm$var.coef[2, 2]), coef(m_cm)[2] / sqrt(m_cm$var.coef[2, 2]), aicc(m_cm, 137)))
cat(sprintf("MA(1) sin media: theta=%.4f ee=%.4f t=%.2f | AICc=%.3f\n",
            coef(m_sm)[1], sqrt(m_sm$var.coef[1, 1]), coef(m_sm)[1] / sqrt(m_sm$var.coef[1, 1]), aicc(m_sm, 137)))
cat(sprintf("ruido blanco con media: media=%.4f ee=%.4f t=%.2f | AICc=%.3f\n",
            coef(w_cm)[1], sqrt(w_cm$var.coef[1, 1]), coef(w_cm)[1] / sqrt(w_cm$var.coef[1, 1]), aicc(w_cm, 137)))
cat(sprintf("ruido blanco sin media: AICc=%.3f\n", aicc(w_sm, 137)))
cat("\n-- auto.arima(ret), argumentos por defecto\n"); print(auto.arima(ret))
cat("\n-- auto.arima(ret, trace = TRUE): compara con y sin media\n"); invisible(auto.arima(ret, trace = TRUE))
cat("\n-- auto.arima(ret, stepwise = FALSE, approximation = FALSE)\n")
print(a2 <- auto.arima(ret, stepwise = FALSE, approximation = FALSE))
cat("\n-- la llamada de genera_cap3.R\n")
print(auto.arima(ret, d = 0, seasonal = FALSE, stepwise = FALSE, approximation = FALSE, max.p = 4, max.q = 4))
cat("\nLjung-Box(12) de ret^2:", round(Box.test(ret^2, lag = 12, type = "Ljung-Box")$p.value, 4), "\n")

tit("E6b · TRM: promedio mensual de datos diarios (rho_1 inducido)")
# y_t = promedio de m valores consecutivos de una caminata aleatoria; d_t = y_t - y_{t-1}.
# Cov exacta de (d_t, d_{t+1}) con álgebra de pesos: d_t = sum_k c_k e_k.
rho1_promedio <- function(m) {
  # pesos de los 2m-1 choques que entran en la diferencia de dos promedios contiguos
  cw <- c(1:m, (m - 1):1) / m
  g0 <- sum(cw^2); g1 <- sum(cw[1:(m - 1)] * cw[(m + 1):(2 * m - 1)])
  g1 / g0
}
for (m in c(2, 5, 20, 21, 30)) cat(sprintf("m = %2d valores por mes: rho_1 = %.4f | (m^2-1)/(2(2m^2+1)) = %.4f\n",
                                          m, rho1_promedio(m), (m^2 - 1) / (2 * (2 * m^2 + 1))))
set.seed(2026)
sim <- replicate(2000, { p <- cumsum(rnorm(138 * 21)); y <- colMeans(matrix(p, nrow = 21))
                         acf(diff(y), lag.max = 2, plot = FALSE)$acf[2:3] })
cat("simulación (2000 caminatas, 138 meses de 21 días): media de r_1 =", round(mean(sim[1, ]), 3),
    " media de r_2 =", round(mean(sim[2, ]), 3), "\n")
cat("r_1 observado en los log-retornos de la TRM:", round(acf(ret, plot = FALSE)$acf[2], 3),
    " error estándar aprox. 1/sqrt(n) =", round(1 / sqrt(137), 3), "\n")
cat("distancia de r_1 a 0.2492 en errores estándar:", round((rho1_promedio(21) - acf(ret, plot = FALSE)$acf[2]) * sqrt(137), 2), "\n")
cat("theta de un MA(1) con rho_1 = 0.25: ", round((1 - sqrt(1 - 4 * 0.25^2)) / (2 * 0.25), 4), "\n")

# ---------------------------------------------------------------------------
tit("E7 · PACF de la serie cruda y de la raíz: qué rezagos salen de la banda")
banda <- 1.96 / sqrt(100)
for (nm in c("cruda", "raiz")) {
  x <- if (nm == "cruda") manchas else sqrt(manchas)
  p <- as.numeric(pacf(x, lag.max = 20, plot = FALSE)$acf)
  cat(sprintf("%-5s banda ±%.3f | fuera: %s | PACF 3,4 = %.4f, %.4f | 6, 9, 16 = %.3f, %.3f, %.3f\n", nm, banda,
              paste(which(abs(p) > banda), collapse = " "), p[3], p[4], p[6], p[9], p[16]))
}

# ---------------------------------------------------------------------------
tit("I1 · Límites del 95 % del AR(2) en raíz desde 1869 y la vuelta al cuadrado")
f <- forecast(ar2s, h = 12, level = 95)
print(round(data.frame(h = 1:12, media = as.numeric(f$mean), inf = as.numeric(f$lower), sup = as.numeric(f$upper),
                       inf_cuadrado = as.numeric(f$lower)^2,
                       inf_truncado = pmax(as.numeric(f$lower), 0)^2,
                       sup_cuadrado = as.numeric(f$upper)^2), 3), row.names = FALSE)
cat("semianchos h = 1..12:", round(as.numeric((f$upper - f$lower) / 2), 2), "\n")

# ---------------------------------------------------------------------------
tit("I2 · Causalidad: AR(1) con phi = 2 tiene solución estacionaria no causal")
set.seed(7); n <- 5000; e <- rnorm(n + 200)
# y_t = -sum_{j>=1} phi^{-j} e_{t+j}
y <- sapply(1:n, function(t) -sum(2^-(1:60) * e[t + 1:60]))
cat("comprueba y_t = 2 y_{t-1} + e_t: max |y_t - 2 y_{t-1} - e_t| =",
    signif(max(abs(y[2:n] - 2 * y[1:(n - 1)] - e[2:n])), 3), "\n")
cat("varianza muestral:", round(var(y), 4), " teórica sigma^2/(phi^2-1) =", round(1 / 3, 4), "\n")
cat("Mod(polyroot(c(1, 1))) (phi = -1) =", Mod(polyroot(c(1, 1))), "\n")

# ---------------------------------------------------------------------------
tit("I3 · Residuales de arima(): R devuelve la innovación estandarizada")
ar2 <- arima(manchas, order = c(2, 0, 0), method = "ML")
ph <- coef(ar2)[1:2]; mu <- coef(ar2)[3]; s2 <- ar2$sigma2
g0s <- sum(c(1, ARMAtoMA(ar = ph, lag.max = 3000))^2)        # gamma_0 / sigma^2
rho1 <- ARMAacf(ar = ph, lag.max = 1)[2]
inn1 <- manchas[1] - mu
inn2 <- (manchas[2] - mu) - rho1 * (manchas[1] - mu)
cat("gamma_0/sigma^2 =", round(g0s, 3), "\n")
cat("t = 1: innovación cruda =", round(inn1, 2), " /sqrt(gamma_0/sigma^2) =", round(inn1 / sqrt(g0s), 2),
    " residuals(ar2)[1] =", round(residuals(ar2)[1], 2), "\n")
cat("t = 2: innovación cruda =", round(inn2, 2), " /sqrt((1-rho1^2) gamma_0/sigma^2) =",
    round(inn2 / sqrt((1 - rho1^2) * g0s), 2), " residuals(ar2)[2] =", round(residuals(ar2)[2], 2), "\n")
cat("t = 3, 4: residuals =", round(residuals(ar2)[3:4], 3), "\n")
lb <- function(e, fd = 2) Box.test(e, lag = 12, type = "Ljung-Box", fitdf = fd)$p.value
crudo <- as.numeric(residuals(ar2)); crudo[1] <- inn1; crudo[2] <- inn2
cat("Ljung-Box(12): residuales de R =", round(lb(residuals(ar2)), 4),
    " | con las dos primeras innovaciones crudas =", round(lb(crudo), 4),
    " | descartando las dos primeras =", round(lb(residuals(ar2)[-(1:2)]), 4), "\n")
a21 <- arima(manchas, order = c(2, 0, 1), method = "ML")
cat("ARMA(2,1) descartando las dos primeras:", round(lb(residuals(a21)[-(1:2)], 3), 4), "\n")

# ---------------------------------------------------------------------------
tit("I4 · CSS frente a ML con T = 40 y phi = 0.95, mil réplicas por semilla")
for (s in c(1, 2, 3, 2026)) {
  set.seed(s)
  rr <- replicate(1000, {
    z <- arima.sim(list(ar = 0.95), n = 40)
    c(css = tryCatch(coef(arima(z, order = c(1, 0, 0), include.mean = FALSE, method = "CSS"))[[1]], error = function(e) NA),
      ml  = tryCatch(coef(arima(z, order = c(1, 0, 0), include.mean = FALSE, method = "ML"))[[1]],  error = function(e) NA))
  })
  cat(sprintf("semilla %4d: CSS > 1 en %.1f %% | ML > 1 en %.1f %% | ML >= 0.999 en %.1f %% | ML falla en %d | max ML = %.6f\n",
              s, 100 * mean(rr["css", ] > 1, na.rm = TRUE), 100 * mean(rr["ml", ] > 1, na.rm = TRUE),
              100 * mean(rr["ml", ] >= 0.999, na.rm = TRUE), sum(is.na(rr["ml", ])), max(rr["ml", ], na.rm = TRUE)))
}
set.seed(1); z <- arima.sim(list(ar = 0.95), n = 40)
cat("ejemplo del capítulo (set.seed(1)): CSS =",
    round(coef(arima(z, order = c(1, 0, 0), include.mean = FALSE, method = "CSS")), 4), " ML =",
    round(coef(arima(z, order = c(1, 0, 0), include.mean = FALSE, method = "ML")), 4), "\n")
cat("ML con transform.pars = FALSE sobre el mismo ejemplo: ")
print(tryCatch(round(coef(arima(z, order = c(1, 0, 0), include.mean = FALSE, method = "ML", transform.pars = FALSE)), 4),
               error = function(e) conditionMessage(e), warning = function(w) conditionMessage(w)))
cat("-- lo que dice ?arima de transform.pars (texto de la ayuda instalada):\n")
rd <- utils:::.getHelpFile(help("arima", package = "stats"))
txt <- capture.output(tools::Rd2txt(rd, options = list(underline_titles = FALSE)))
i <- grep("transform.pars:", txt); cat(txt[i:(i + 4)], sep = "\n")
txt2 <- capture.output(tools::Rd2txt(utils:::.getHelpFile(help("arima.sim", package = "stats")),
                                     options = list(underline_titles = FALSE)))
i <- grep("n.start:", txt2); cat("-- ?arima.sim, n.start:\n"); cat(txt2[i:(i + 1)], sep = "\n")
cat("-- sin calentamiento, un AR(1) con phi = 0.95 que arranca en cero (5000 réplicas): media y varianza por t\n")
set.seed(11); M <- replicate(5000, as.numeric(stats::filter(rnorm(200), 0.95, method = "recursive")))
for (t in c(1, 5, 20, 50, 200)) cat(sprintf("t = %3d: media = %6.3f  varianza = %6.3f  (teórica (1-phi^(2t))/(1-phi^2) = %6.3f; estacionaria = %.3f)\n",
    t, mean(M[t, ]), var(M[t, ]), (1 - 0.95^(2 * t)) / (1 - 0.95^2), 1 / (1 - 0.95^2)))

# ---------------------------------------------------------------------------
tit("I5 · Elasticidades amplitud-nivel: qué contiene cada intervalo")
j3 <- jsonlite::fromJSON("precalculo/salidas/cap3_arma.json")
busca <- function(x) { if (!is.list(x)) return(NULL); if (!is.null(x$elasticidades)) return(x$elasticidades)
  for (v in x) { r <- busca(v); if (!is.null(r)) return(r) }; NULL }
el <- busca(j3)
for (nm in names(el)) cat(sprintf("%-10s b=%.4f IC=[%.3f, %.3f] contiene 0.5: %s  contiene 1: %s\n", nm, el[[nm]]$b,
                                   el[[nm]]$ic[1], el[[nm]]$ic[2], el[[nm]]$ic[1] <= 0.5 & 0.5 <= el[[nm]]$ic[2],
                                   el[[nm]]$ic[1] <= 1 & 1 <= el[[nm]]$ic[2]))

# ---------------------------------------------------------------------------
tit("I6 · arima.sim con order = c(0, 1, 0)")
set.seed(4); e <- rnorm(10)
set.seed(4); x <- arima.sim(list(order = c(0, 1, 0)), n = 10)
cat("largo:", length(x), " | igual a c(0, cumsum(rnorm(10))):", isTRUE(all.equal(as.numeric(x), c(0, cumsum(e)))), "\n")
cat("arima.sim(list(ar = 1)): ", tryCatch(arima.sim(n = 100, model = list(ar = 1)), error = function(e) conditionMessage(e)), "\n")

# ---------------------------------------------------------------------------
tit("D5 · Dos nociones de periodo en el AR(2) de la ventana 1770-1869 (raíz)")
p_arg  <- 2 * pi / Arg(raices[1])
p_fpp  <- 2 * pi / acos(-phi[1] * (1 - phi[2]) / (4 * phi[2]))
cat("2*pi/Arg(raíz)                                  =", round(p_arg, 4), "\n")
cat("2*pi/acos(phi1/(2 sqrt(-phi2)))                 =", round(2 * pi / acos(phi[1] / (2 * sqrt(-phi[2]))), 4), "\n")
cat("2*pi/acos(-phi1 (1-phi2)/(4 phi2))  [FPP3 §9.5] =", round(p_fpp, 4), "\n")
# densidad espectral del AR(2): f(w) ∝ 1/|1 - phi1 e^{-iw} - phi2 e^{-2iw}|^2
fw <- function(w) 1 / Mod(1 - phi[1] * exp(-1i * w) - phi[2] * exp(-2i * w))^2
wmax <- optimize(fw, c(0.01, pi - 0.01), maximum = TRUE, tol = 1e-10)$maximum
cat("periodo en que es máxima la densidad espectral  =", round(2 * pi / wmax, 4), "\n")
# periodo de la ACF teórica: distancia entre cruces por cero consecutivos x 2
rho <- ARMAacf(ar = phi, lag.max = 400)
cat("ACF teórica: primeros máximos locales en k =", which(diff(sign(diff(rho))) == -2)[1:3], "\n")
cat("serie cruda (ML): 2*pi/Arg =", round(2 * pi / Arg(polyroot(c(1, -ph))[1]), 4),
    " FPP3 =", round(2 * pi / acos(-ph[1] * (1 - ph[2]) / (4 * ph[2])), 4), "\n")
cat("con módulo de la raíz -> 1 las dos se juntan; phi = (1.6, -0.99):",
    round(2 * pi / acos(1.6 / (2 * sqrt(0.99))), 3), round(2 * pi / acos(-1.6 * 1.99 / (4 * -0.99)), 3), "\n")

# ---------------------------------------------------------------------------
tit("Menores")
cat("t del AR(2) final sin redondear:", round(coef(ar2s)[1:2] / sqrt(diag(ar2s$var.coef))[1:2], 2),
    " | parámetros (phi1, phi2, media, sigma2):", length(coef(ar2s)) + 1, "\n")
cat("LB(12) del AR(2) en raíz:", format(Box.test(residuals(ar2s), lag = 12, type = "Ljung-Box", fitdf = 2)$p.value, digits = 7), "\n")
cat("LB(12) descartando los dos primeros residuales:", round(lb(residuals(ar2s)[-(1:2)]), 4), "\n")
lam <- BoxCox.lambda(manchas + 1, method = "guerrero")
g1 <- arima(BoxCox(manchas + 1, lam), order = c(2, 0, 0), method = "ML")
g0 <- arima(manchas^lam, order = c(2, 0, 0), method = "ML")
cat(sprintf("Guerrero lambda=%.4f | sobre manchas^lambda: periodo=%.2f p=%.4f | sobre la desplazada: periodo=%.2f p=%.5f\n", lam,
            2 * pi / Arg(polyroot(c(1, -coef(g0)[1:2]))[1]), lb(residuals(g0)),
            2 * pi / Arg(polyroot(c(1, -coef(g1)[1:2]))[1]), lb(residuals(g1))))
lhf <- arima(lh, order = c(1, 0, 0), method = "ML")
cat("lh AR(1): phi =", round(coef(lhf)[1], 4), "\n")
cat("suma psi^2 =", round(sum(c(1, ARMAtoMA(ar = phi, lag.max = 600))^2), 4), " techo ±",
    round(qnorm(0.975) * sqrt(ar2s$sigma2 * sum(c(1, ARMAtoMA(ar = phi, lag.max = 600))^2)), 2), "\n")

# ---------------------------------------------------------------------------
tit("E1b · Ventanas de 100 años: detalle de las que no rechazan")
ini <- 1700:1889
cat("no rechazan:", sum(pp > 0.05), "| de ellas, con inicio entre 1734 y 1785:", sum(pp > 0.05 & ini >= 1734 & ini <= 1785),
    "| inicio 1735: p =", round(pp[ini == 1735], 4), "\n")
cat("ventanas que alcanzan 1900 (inicio >= 1801):", sum(ini >= 1801), "| de ellas no rechazan:", sum(pp[ini >= 1801] > 0.05), "\n")
cat("ventanas con inicio >= 1786:", sum(ini >= 1786), "| no rechazan:", sum(pp[ini >= 1786] > 0.05), "\n")
