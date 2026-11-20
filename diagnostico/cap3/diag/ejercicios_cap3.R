# Diagnóstico cap. 3 · práctica: reproduce E1–E3, las claves del quiz `cap3`,
# las de la actividad `parcial2` y las del simulacro del Módulo 11 (que no
# trae clave en la página), con el código del capítulo cuando lo hay.
# Rscript --vanilla diagnostico/cap3/diag/ejercicios_cap3.R > diagnostico/cap3/diag/ejercicios_cap3.out 2>&1
suppressMessages({library(forecast); library(tseries)})
options(width = 110)
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
sec <- function(s) cat("\n==================== ", s, " ====================\n")
fuera <- function(x, n) { b <- 1.96/sqrt(n); which(abs(x) > b) }

## ------------------------------------------------------------------ E1 · lh
sec("E1 · lh")
n <- length(lh); cat("n =", n, " banda =", round(1.96/sqrt(n), 4), "\n")
a <- acf(lh, lag.max = 20, plot = FALSE)$acf[-1]
p <- as.numeric(pacf(lh, lag.max = 20, plot = FALSE)$acf)
cat("ACF 1:6 ", round(a[1:6], 4), "\n"); cat("PACF 1:6", round(p[1:6], 4), "\n")
cat("ACF fuera (20 rezagos):", fuera(a, n), " PACF fuera:", fuera(p, n), "\n")
for (pq in list(c(1,0), c(2,0), c(3,0), c(0,1), c(0,2), c(1,1))) {
  f <- arima(lh, order = c(pq[1], 0, pq[2]), method = "ML")
  cat(sprintf("ARMA(%d,%d)  AICc=%7.3f  BIC=%7.3f  LB(10) p=%.4f\n", pq[1], pq[2],
      aicc(f, n), BIC(f), Box.test(residuals(f), lag = 10, type = "Ljung-Box", fitdf = sum(pq))$p.value))
}
ma2 <- arima(lh, order = c(0, 0, 2), method = "ML")
cat("MA(2): coef", round(coef(ma2), 4), " t =", round(coef(ma2)/sqrt(diag(ma2$var.coef)), 2), "\n")
ar1 <- arima(lh, order = c(1, 0, 0), method = "ML")
cat("AR(1): phi", round(coef(ar1)[1], 4), " ee", round(sqrt(ar1$var.coef[1,1]), 4),
    " Shapiro p", signif(shapiro.test(residuals(ar1))$p.value, 4), "\n")
cat("Shapiro MA(2) p", signif(shapiro.test(residuals(ma2))$p.value, 4), "\n")
cat("auto.arima(lh):\n"); print(auto.arima(lh))
cat("auto.arima(lh, ic='bic'):\n"); print(auto.arima(lh, ic = "bic"))
cat("Diferencias: AICc(AR1) - AICc(MA2) =", round(aicc(ar1, n) - aicc(ma2, n), 3),
    " BIC(MA2) - BIC(AR1) =", round(BIC(ma2) - BIC(ar1), 3), "\n")
# El AR(1) y el MA(2) frente a la ACF muestral: ¿cuál la reproduce mejor?
cat("ACF teórica AR(1):", round(ARMAacf(ar = coef(ar1)[1], lag.max = 4)[-1], 4), "\n")
cat("ACF teórica MA(2):", round(ARMAacf(ma = coef(ma2)[1:2], lag.max = 4)[-1], 4), "\n")

## ------------------------------------------------------------------ E2 · MA(2)
sec("E2 · MA(2) theta = (0.6, 0.4)")
th <- c(0.6, 0.4)
cat("|raíces|", round(Mod(polyroot(c(1, th))), 4), "\n")
cat("ACF", round(ARMAacf(ma = th, lag.max = 4)[-1], 4), "\n")
cat("techo de rho1 en un MA(2): cos(pi/4) =", round(cos(pi/4), 4), "\n")
cat("Var (sigma2 = 1):", 1 + sum(th^2), "\n")
cat("pi_j", round(ARMAtoMA(ar = -th, lag.max = 8), 4), "\n")

## ------------------------------------------------------------------ E3 · ventanas
sec("E3 · sqrt(manchas), AR(2) por ventanas")
for (v in list(c(1770,1869), c(1700,1988), c(1870,1988), c(1900,1988), c(1700,1769), c(1889,1988))) {
  x <- sqrt(window(sunspot.year, v[1], v[2]))
  f <- arima(x, order = c(2, 0, 0), method = "ML")
  ee <- sqrt(diag(f$var.coef))[1:2]
  r <- polyroot(c(1, -coef(f)[1:2]))
  lb <- sapply(c(6, 10, 12, 20), function(h) Box.test(residuals(f), lag = h, type = "Ljung-Box", fitdf = 2)$p.value)
  cat(sprintf("%d-%d n=%3d phi=(%.4f, %.4f) ee=(%.4f, %.4f) periodo=%6.3f  LB6/10/12/20 p=%s\n",
      v[1], v[2], length(x), coef(f)[1], coef(f)[2], ee[1], ee[2], 2*pi/Arg(r[1]),
      paste(sprintf("%.4f", lb), collapse = " ")))
}
# ¿Es «la potencia» la causa del rechazo? Si el AR(2) fuera el proceso, la tasa
# de rechazo de LB(12) sería ~5 % con cualquier n: la potencia solo crece si
# el modelo está mal especificado. Y la ventana 1900–1988 (n = 89) rechaza con
# MENOS datos que la de Yule (n = 100).
set.seed(20261119)
f0 <- arima(sqrt(window(sunspot.year, 1700, 1988)), order = c(2, 0, 0), method = "ML")
for (nn in c(89, 100, 289)) {
  pv <- replicate(1000, {
    y <- arima.sim(list(ar = coef(f0)[1:2]), n = nn) * sqrt(f0$sigma2)
    tryCatch(Box.test(residuals(suppressWarnings(arima(y, order = c(2, 0, 0), method = "ML"))),
             lag = 12, type = "Ljung-Box", fitdf = 2)$p.value, error = function(e) NA) })
  cat(sprintf("AR(2) verdadero, n = %3d: rechaza LB(12) al 5 %% en %.1f %% (%d ajustes fallidos)\n", nn, 100*mean(pv < 0.05, na.rm = TRUE), sum(is.na(pv))))
}
# Diferencia de coeficientes 1770–1869 frente a 1900–1988, en errores estándar
f1 <- arima(sqrt(window(sunspot.year, 1770, 1869)), order = c(2,0,0), method = "ML")
f2 <- arima(sqrt(window(sunspot.year, 1900, 1988)), order = c(2,0,0), method = "ML")
cat("dif. phi (1900-88 menos 1770-1869) en ee de 1770-1869:",
    round((coef(f2)[1:2] - coef(f1)[1:2]) / sqrt(diag(f1$var.coef))[1:2], 2), "\n")
cat("ARMA(2,1)/AR(3) en 1900-1988 (sqrt): AICc AR2", round(aicc(f2, 89), 2),
    " AR3", round(aicc(arima(sqrt(window(sunspot.year,1900,1988)), order=c(3,0,0), method="ML"), 89), 2),
    " ARMA21", round(aicc(arima(sqrt(window(sunspot.year,1900,1988)), order=c(2,0,1), method="ML"), 89), 2), "\n")
cat("sum(sunspot.year == 0) en 1700-1988:", sum(window(sunspot.year,1700,1988) == 0), "\n")

## ------------------------------------------------------------------ Quiz cap3
sec("Quiz cap3")
cat("Q1 |raíces| de 1-1.2B+0.9B^2:", round(Mod(polyroot(c(1, -1.2, 0.9))), 4), "\n")
cat("Q2 rho1(0.8) =", round(0.8/1.64, 6), "\n")
psi1 <- 0.7 + 0.5
cat("Q4 Var(e_T+2) =", 2*(1 + psi1^2), " distractores: 2.44 =", 1 + psi1^2,
    "; 2.88 =", 2*psi1^2, "; 2.98 =", 2*(1+0.7^2), "; 4.40 =", 2*(1+psi1),
    "; 6.29 =", round(2*(1 + psi1^2 + (0.7*psi1)^2), 4), "\n")
cat("Q6 t:", round(0.64/0.38, 2), round(0.69/0.36, 2), " suma", -0.64 + 0.69, "\n")
cat("Q7 periodo:", round(2*pi/acos(1.4027/(2*sqrt(0.6853))), 4),
    " con grados y 2*pi:", round(2*pi/(acos(1.4027/(2*sqrt(0.6853)))*180/pi), 4),
    " con grados y 360:", round(360/(acos(1.4027/(2*sqrt(0.6853)))*180/pi), 4),
    " con phi crudos ML (1.4059,-0.7111):", round(2*pi/acos(1.4059/(2*sqrt(0.7111))), 4), "\n")
manchas <- window(sunspot.year, start = 1770, end = 1869)
ar2c <- arima(manchas, order = c(2,0,0), method = "ML")
cat("Q8 LB12 AR(2) crudo con/sin fitdf:",
    signif(Box.test(residuals(ar2c), lag = 12, type = "Ljung-Box", fitdf = 2)$p.value, 4),
    signif(Box.test(residuals(ar2c), lag = 12, type = "Ljung-Box")$p.value, 4), "\n")
ar1c <- arima(manchas, order = c(1,0,0), method = "ML")
r1c <- acf(residuals(ar1c), lag.max = 20, plot = FALSE)$acf[-1]
cat("Q9 resid AR(1): r1 =", round(r1c[1], 4), " fuera de ±0.196:", fuera(r1c, 100),
    " LB12 p =", signif(Box.test(residuals(ar1c), lag = 12, type = "Ljung-Box", fitdf = 1)$p.value, 3), "\n")
r2c <- acf(residuals(ar2c), lag.max = 20, plot = FALSE)$acf[-1]
cat("    resid AR(2): r1, r2 =", round(r2c[1:2], 4), " fuera:", fuera(r2c, 100), " máx |r|", round(max(abs(r2c)), 4), "\n")
yw <- ar(manchas, order.max = 2, aic = FALSE, method = "yule-walker")
cat("Q10 YW - ML en ee:", round((yw$ar - coef(ar2c)[1:2]) / sqrt(diag(ar2c$var.coef))[1:2], 2),
    " sigma2 YW / ML:", round(yw$var.pred, 2), round(ar2c$sigma2, 2), "\n")

## ------------------------------------------------------------------ parcial2 (variante 1)
sec("parcial2 · actividad preparatoria (variante 1 del quiz adicional)")
cat("P2 k = floor((96-1)^(1/3)) =", floor(95^(1/3)), "\n")
cat("P4 E =", 100 + 36*0.5, " Var =", 36*4, "\n")
cat("P5 (1-0.3B)(1-B) =", round(Re(polyroot(c(1,-1.3,0.3))), 4), " coef:", c(1, -1.3, 0.3), "\n")
cat("P6 phi=(1,-0.5): phi1+phi2", 0.5, " phi2-phi1", -1.5, " disc", 1 - 2, " |raíz|",
    round(Mod(polyroot(c(1, -1, 0.5))), 4), " periodo", round(2*pi/acos(1/(2*sqrt(0.5))), 3), "\n")
mu <- 50.59; cat("P7 c =", round(mu*(1-0.6256-0.1666), 4), " mu(1-phi1) =", round(mu*(1-0.6256), 4),
    " mu/(1-s) =", round(mu/(1-0.6256-0.1666), 4), " mu*s =", round(mu*(0.6256+0.1666), 4), "\n")
th038 <- (1 - sqrt(1 - 4*0.38^2))/(2*0.38)
cat("P8 theta =", round(th038, 4), round(1/th038, 4), " rho1(0.38) =", round(0.38/(1+0.38^2), 4), "\n")
ps <- c(1, ARMAtoMA(ar = 0.65, ma = 0.4, lag.max = 3))
cat("P9 Var(e_T+3) =", round(sum(ps[1:3]^2), 4), " desfase =", round(sum(ps[2:4]^2), 4),
    " signo =", round(sum(c(1, ARMAtoMA(ar = 0.65, ma = -0.4, lag.max = 2))^2), 4),
    " AR solo =", round(sum(c(1, 0.65, 0.65^2)^2), 4), "\n")
cat("P10 rho =", round(ARMAacf(ar = c(0.6, 0.2), lag.max = 2)[-1], 4),
    " pacf =", round(ARMAacf(ar = c(0.6, 0.2), lag.max = 3, pacf = TRUE), 4), "\n")

## ------------------------------------------------------------------ simulacro (variante 9, sin clave)
sec("Simulacro M11 · variante 9 (claves calculadas aquí)")
cat("S1 estacionarios: (-1)^t e_t y 5 + 0.92 y_{t-1} + e_t  -> opciones b y e\n")
cat("S2 k = floor(115^(1/3)) =", floor(115^(1/3)), " -> a) raíz unitaria\n")
cat("S3 Var = 2*0.81 =", 2*0.81, " -> b)\n")
cat("S4 E =", 120 + 40*1.1, " Var =", 40*2.2^2, " -> c)\n")
cat("S5 (1+0.6B)(1-B) = 1 - 0.4B - 0.6B^2 -> phi = (0.4, 0.6), no estacionario -> d)\n")
cat("S6 phi=(1.4,-0.45): suma", 1.4-0.45, " dif", -0.45-1.4, " disc", 1.4^2 - 4*0.45,
    " |raíces|", round(Mod(polyroot(c(1,-1.4,0.45))), 4), " -> a) estacionario, reales\n")
mu <- 59.9161; s <- 0.7579 - 0.2327
cat("S7 c =", round(mu*(1-s), 4), " mu(1-phi1) =", round(mu*(1-0.7579), 4), " mu/(1-s) =", round(mu/(1-s), 4), " -> b)\n")
t44 <- (1 - sqrt(1 - 4*0.44^2))/(2*0.44)
cat("S8 theta =", round(t44, 4), round(1/t44, 4), " -> c)\n")
ps <- c(1, ARMAtoMA(ar = 0.93, ma = -0.12, lag.max = 3))
cat("S9 psi =", round(ps, 4), " Var(e_T+3) =", round(2.2*sum(ps[1:3]^2), 4),
    " desfase =", round(2.2*sum(ps[2:4]^2), 4),
    " signo MA =", round(2.2*sum(c(1, ARMAtoMA(ar = 0.93, ma = 0.12, lag.max = 2))^2), 4),
    " AR solo =", round(2.2*sum(c(1, 0.93, 0.93^2)^2), 4), " -> d)\n")
cat("S10 rho =", round(ARMAacf(ar = c(0.5, 0.3), lag.max = 2)[-1], 4),
    " pacf =", round(ARMAacf(ar = c(0.5, 0.3), lag.max = 3, pacf = TRUE), 4), " -> a)\n")

## ------------------------------------------------------------------ FPP3 §9.5: otra fórmula del periodo
sec("Periodo del AR(2): fórmula del capítulo (ángulo de la raíz) frente a la de FPP3 §9.5 (arima.txt l. 328)")
per_cap <- function(p1, p2) 2*pi/acos(p1/(2*sqrt(-p2)))
per_fpp <- function(p1, p2) 2*pi/acos(-p1*(1 - p2)/(4*p2))
for (ph in list(c(1.4027, -0.6853), c(1.4059, -0.7111), c(1.4, -0.75), c(1, -0.5), c(1.3776, -0.7399))) {
  cat(sprintf("phi = (%.4f, %.4f): capítulo %.4f · FPP3 %.4f\n", ph[1], ph[2], per_cap(ph[1], ph[2]), per_fpp(ph[1], ph[2])))
}
