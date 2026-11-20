# fuentes_comprobaciones.R · comprobaciones en R detrás del inventario de fuentes del capítulo 3.
# No escribe nada fuera de la salida estándar. Uso (desde cualquier carpeta):
#   Rscript diagnostico/cap3/diag/fuentes_comprobaciones.R > diagnostico/cap3/diag/fuentes_comprobaciones_r.out
# R 4.6.0 · forecast 9.0.2. De la ayuda de R solo se imprimen booleanos: el texto de la ayuda no se copia.
suppressMessages(library(forecast))

ayuda <- function(tema) {
  f <- utils:::.getHelpFile(help(tema))
  tf <- tempfile(); tools::Rd2txt(f, out = tf, options = list(underline_titles = FALSE)); gsub("\\s+", " ", paste(readLines(tf), collapse = " "))
}
cat("== Ayuda de R: ¿dice lo que el capítulo le atribuye? (solo booleanos)\n")
a <- ayuda("arima")
cat("?arima Details: MA con signo distinto de S-PLUS:", grepl("differ in sign from those used in documentation written for S-PLUS", a), "\n")
cat("?arima: CSS-ML por defecto (CSS para arrancar, luego ML):", grepl("conditional-sum-of-squares to find starting values, then maximum likelihood", a), "\n")
cat("?arima: MA convertidos a forma invertible 'if transform.pars is true':", grepl("converted to invertible form after optimization if .transform.pars. is true", a), "\n")
cat("?arima: aic 'Only valid for method = ML':", grepl("Only valid for .method = \"ML\". fits", a), "\n")
cat("?arima: intercept = media (la fórmula se aplica a X - m):", grepl("this formula applies to X - m rather than X", a), "\n")
cat("?arima: matriz de varianzas 'may only be a rough guide':", grepl("may only be a rough guide", a), "\n")
b <- ayuda("arima.sim")
cat("?arima.sim: admite order = c(p,d,q) (modelos integrados):", grepl("ARIMA models are specified via the .order. component", b), "\n")
cat("?arima.sim: n.start = burn-in, NA por defecto:", grepl("n.start: length of .burn-in. period. If .NA., the default", b), "\n")
cat("?polyroot: coeficientes en orden creciente:", grepl("polynomial coefficients in increasing order", ayuda("polyroot")), "\n")
cat("?Box.test: fitdf = p+q, 'provided of course that lag > fitdf':", grepl("fitdf = p\\+q., provided of course that .lag > fitdf", ayuda("Box.test")), "\n")
cat("?sunspot.year dice 'Wolf'?:", grepl("Wolf", ayuda("sunspot.year"), ignore.case = TRUE), " · dice 'rounded to one digit':", grepl("rounded to one digit", ayuda("sunspot.year")), "\n")
cat("?lh: 48 muestras cada 10 minutos:", grepl("10 mins intervals", ayuda("lh")) && grepl("48 samples", ayuda("lh")), "\n")

cat("\n== c3-m6-03: arima.sim sí simula una caminata aleatoria con order = c(0,1,0)\n")
set.seed(1); x <- arima.sim(list(order = c(0, 1, 0)), n = 100)
cat("clase:", class(x), " longitud:", length(x), " (n=100 más el valor inicial 0)\n")

cat("\n== c3-m3-13: ¿arima() devuelve siempre la raíz invertible? MA(1) con theta = 2\n")
set.seed(1); y <- arima.sim(n = 500, list(ma = 2.0))
for (m in c("CSS", "ML", "CSS-ML")) { f <- arima(y, order = c(0, 0, 1), method = m); cat(sprintf("%-7s ma1 = %.4f  sigma2 = %.3f\n", m, coef(f)["ma1"], f$sigma2)) }
f <- arima(y, order = c(0, 0, 1), method = "ML", transform.pars = FALSE); cat(sprintf("%-7s ma1 = %.4f  (transform.pars = FALSE)\n", "ML", coef(f)["ma1"]))

cat("\n== c3-m9-04 y c3-m9-05: ceros de sunspot.year y aviso de Guerrero\n")
cat("ceros en 1770-1869:", sum(window(sunspot.year, 1770, 1869) == 0), " en 1700-1988:", sum(sunspot.year == 0), " años:", which(sunspot.year == 0) + 1699, "\n")
m <- window(sunspot.year, 1770, 1869)
r1 <- withCallingHandlers(BoxCox.lambda(m, method = "guerrero"), warning = function(w) { cat("AVISO de forecast:", conditionMessage(w), "\n"); invokeRestart("muffleWarning") })
cat(sprintf("lambda sobre la serie cruda = %.4f · sobre manchas + 1 = %.4f\n", r1, BoxCox.lambda(m + 1, method = "guerrero")))

cat("\n== c3-m8-18: primer residual de arima(): ¿innovación cruda o estandarizada?\n")
f <- arima(m, order = c(2, 0, 0), method = "ML"); mu <- coef(f)["intercept"]; ph <- coef(f)[1:2]; y1 <- as.numeric(m)[1]
g0 <- 1 / (1 - sum(ph * ARMAacf(ar = ph, lag.max = 2)[-1]))
cat(sprintf("residuals()[1:3] = %s\n", paste(round(residuals(f)[1:3], 3), collapse = " ")))
cat(sprintf("y1 - mu = %.3f · gamma0/sigma2 = %.3f · (y1 - mu)/sqrt(gamma0/sigma2) = %.3f\n", y1 - mu, g0, (y1 - mu) / sqrt(g0)))

cat("\n== c3-m3-12: techo de rho_1 en un MA(q) frente a cos(pi/(q+2))\n")
maxrho1 <- function(q) { f <- function(th) { th <- c(1, th); sum(th[-length(th)] * th[-1]) / sum(th^2) }
  best <- -Inf; set.seed(1); for (i in 1:200) { o <- suppressWarnings(optim(runif(q, -1.5, 1.5), function(t) -f(t))); best <- max(best, -o$value) }; best }
for (q in 1:4) cat(sprintf("q = %d  máximo numérico = %.5f  cos(pi/(q+2)) = %.5f\n", q, maxrho1(q), cos(pi / (q + 2))))

cat("\n== c3-m2-12 y c3-m10-76: dos fórmulas para el periodo del ciclo de un AR(2)\n")
for (p in list(c(1.4027, -0.6853), c(1.40, -0.69), c(1.4, -0.75), c(1, -0.5))) {
  raiz <- 2 * pi / acos(p[1] / (2 * sqrt(-p[2]))); fpp3 <- 2 * pi / acos(-p[1] * (1 - p[2]) / (4 * p[2]))
  cat(sprintf("phi = (%.4f, %.4f)  ángulo de la raíz (Cryer, Shumway, capítulo) = %.3f  FPP3 9.5 = %.3f\n", p[1], p[2], raiz, fpp3))
}

cat("\n== c3-m2-17: la varianza del AR(2) solo vale dentro del triángulo\n")
g <- function(p1, p2) (1 - p2) / ((1 + p2) * ((1 - p2)^2 - p1^2))
cat(sprintf("phi = (0, 2): gamma0/sigma2 por la fórmula cerrada = %.4f (negativo: no es una varianza)\n", g(0, 2)))
cat(sprintf("phi = (0.5, 0.3), dentro: %.4f\n", g(0.5, 0.3)))

cat("\n== c3-m10-28: ARMA(2,2) (1.1,-0.28; 0.1,-0.20) frente a ARMA(1,1) (0.7; 0.5)\n")
cat("máxima diferencia de las ACF a 8 rezagos:", signif(max(abs(ARMAacf(ar = c(1.1, -0.28), ma = c(0.1, -0.20), lag.max = 8) - ARMAacf(ar = 0.7, ma = 0.5, lag.max = 8))), 3), "\n")

cat("\n== c3-m3-14, c3-m4-10 y c3-m4-08: cifras del Módulo 3 y 4\n")
cat("PACF del MA(1) con theta = 0.8:", round(ARMAacf(ma = 0.8, lag.max = 4, pacf = TRUE), 4), "\n")
pj <- ARMAtoMA(ar = -0.5, ma = -0.7, lag.max = 12)
cat("pesos pi del ARMA(1,1) (0.7; 0.5):", round(pj[1:9], 4), "· primer j con |pi_j| < 0.01:", which(abs(pj) < 0.01)[1] + 1, "\n")
n <- 1:10; cat("ejemplo de ?ARMAtoMA: ARMAtoMA(c(1,-0.25),1,10) = (1+3n)2^-n (empieza en psi_1):", isTRUE(all.equal(ARMAtoMA(c(1.0, -0.25), 1.0, 10), (1 + 3 * n) * 2^(-n))), "\n")

cat("\n== Hallazgo colateral (caso TRM): promediar un paseo aleatorio induce autocorrelación en las primeras diferencias\n")
m <- 21; set.seed(1); n <- 20000; rw <- cumsum(rnorm(n * m)); a <- colMeans(matrix(rw, nrow = m)); d <- diff(a)
cat(sprintf("rho_1 de las diferencias de promedios de %d pasos de un paseo aleatorio = %.3f (teoría asintótica 0.25) · r1 observado en los log-retornos de la TRM = 0.105\n", m, acf(d, plot = FALSE)$acf[2]))
