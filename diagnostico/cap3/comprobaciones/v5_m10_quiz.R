# Verificador independiente R5 cap. 3: ejercicios 1-3 del M10, quiz cap3 y avisos de lynx
suppressPackageStartupMessages(library(forecast))
h <- function(...) cat("\n##", ..., "\n")
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }

h("lynx: que ajuste da el aviso de convergencia")
rej <- list(c(1,0), c(2,0), c(3,0), c(4,0), c(0,1), c(0,2), c(0,3), c(1,1), c(2,1), c(1,2), c(2,2))
for (x in list(cruda = lynx, log = log(lynx))) for (pq in rej) withCallingHandlers(
  arima(x, order = c(pq[1],0,pq[2]), method = "ML"),
  warning = function(w) { cat("AVISO en ARMA(", pq[1], ",", pq[2], ") escala n=", length(x), " media=", round(mean(x),1), ":", conditionMessage(w), "\n"); invokeRestart("muffleWarning") })

h("Ejercicio 1 · lh")
n <- length(lh); cat("banda:", 1.96/sqrt(n), "\n")
ar1 <- arima(lh, order = c(1,0,0), method = "ML"); ma2 <- arima(lh, order = c(0,0,2), method = "ML")
cat("AICc:", aicc(ar1,n), aicc(ma2,n), " BIC:", BIC(ar1), BIC(ma2), "\n")
cat("LB10:", Box.test(residuals(ar1), 10, "Ljung-Box", fitdf = 1)$p.value, Box.test(residuals(ma2), 10, "Ljung-Box", fitdf = 2)$p.value, "\n")
cat("theta2, t:", coef(ma2)[2], coef(ma2)[2]/sqrt(ma2$var.coef[2,2]), "\n")
print(round(rbind(acf(lh, 3, plot = FALSE)$acf[-1], ARMAacf(ar = coef(ar1)[1], lag.max = 3)[-1], ARMAacf(ma = coef(ma2)[1:2], lag.max = 3)[-1]), 4))
cat("SW:", shapiro.test(residuals(ar1))$p.value, shapiro.test(residuals(ma2))$p.value, "\n")
cat("auto.arima:", as.character(auto.arima(lh)), "|", as.character(auto.arima(lh, stepwise = FALSE, approximation = FALSE)), "\n")
cat("phi y ee AR(1):", coef(ar1)[1], sqrt(ar1$var.coef[1,1]), coef(ar1)[2], "\n")

h("Ejercicio 2 · MA(2)")
for (th in list(c(0.9,0.2), c(2.4,0.8), c(0.9*0+0.5+2, 0.5*2*0+1), c(0.4+2.5, 1))) NULL
th <- c(0.9, 0.2); cat("triangulo:", sum(th), th[2]-th[1], abs(th[2]), " raices:", polyroot(c(1,th)), "\n")
cat("rho a mano:", (th[1]+th[1]*th[2])/(1+sum(th^2)), th[2]/(1+sum(th^2)), "\n")
print(ARMAacf(ma = th, lag.max = 4)); print(ARMAacf(ma = c(2.4, 0.8), lag.max = 4))
cat("(1+2B)(1+0.4B):", c(1, 2+0.4, 2*0.4), " raices:", polyroot(c(1,2.4,0.8)), "\n")
# los otros dos MA(2) con la misma ACF: (1+0.5B)(1+2.5B) y (1+2B)(1+2.5B)
for (pr in list(c(1+0.5*0, 0.5+2.5, 0.5*2.5), c(1, 2+2.5, 2*2.5))) { cat("theta=", pr[2:3], "ACF:", round(ARMAacf(ma = pr[2:3], lag.max = 2)[-1], 4), " |raices|:", Mod(polyroot(pr)), "\n") }
set.seed(2); y <- arima.sim(n = 2000, model = list(ma = c(2.4, 0.8))); m <- arima(y, order = c(0,0,2), include.mean = FALSE)
cat("seed 2 arima:", coef(m), m$sigma2, "\n")

h("Ejercicio 3 · ventanas")
for (v in list(c(1770,1869), c(1700,1988), c(1870,1988), c(1900,1988), c(1889,1988))) {
  x <- sqrt(window(sunspot.year, v[1], v[2])); f <- arima(x, order = c(2,0,0), method = "ML"); r <- polyroot(c(1,-coef(f)[1:2]))
  cat(v, length(x), round(coef(f)[1:2],4), round(sqrt(diag(f$var.coef))[1:2],4), round(2*pi/Arg(r[1]),3), signif(Box.test(residuals(f), 12, "Ljung-Box", fitdf = 2)$p.value,4), "\n") }

h("Quiz")
cat("P1 |raiz|:", Mod(polyroot(c(1,-1.2,0.9))), " triangulo:", 1.2-0.9, -0.9-1.2, "\n")
th1 <- 0.6; th2 <- -0.3; s2 <- 4
cat("P2 gamma1:", s2*(th1+th1*th2), " distractores: solo e_t-1", s2*th1, " sin s2", th1+th1*th2, " signo", s2*(th1-th1*th2), " rho1", (th1+th1*th2)/(1+th1^2+th2^2), " gamma2", s2*th2, "\n")
cat("P2 comprobacion por simulacion:", {set.seed(1); z <- arima.sim(n=1e6, list(ma=c(th1,th2)), sd=2); acf(z,1,type="covariance",plot=FALSE)$acf[2]}, "\n")
cat("P3 PROCESOS.ma2 ACF teorica:", round(ARMAacf(ma = c(0.6,0.4), lag.max = 4)[-1],4), "\n")
ph <- 0.6; th <- -0.3; s2 <- 5; p1 <- ph+th; p2 <- ph*p1
cat("P4:", s2*(1+p1^2), " sin s2", 1+p1^2, " sin psi0", s2*p1^2, " psi1=phi", s2*(1+ph^2), " signo", s2*(1+(ph-th)^2), " sin cuadrado", s2*(1+p1), " hasta h", s2*(1+p1^2+p2^2), "\n")
cat("P4 con psi de ARMAtoMA:", s2*sum(c(1,ARMAtoMA(ph,th,1))^2), "\n")
cat("M4 practica: phi+theta =", 0.8-0.5, " factor h=2:", 1+0.3^2, " => P4 = 5 x", 1+0.3^2, "\n")
cat("P5 rho1:", -2.5/(1+2.5^2), -0.4/1.16, " raiz:", polyroot(c(1,-2.5)), " pi:", 2.5^(1:3), " g0,g1:", 1+2.5^2, -2.5, 6.25*1.16, -0.4*6.25, "\n")
set.seed(35); y5 <- arima.sim(n = 2000, model = list(ma = -2.5)); m5 <- arima(y5, order = c(0,0,1), include.mean = FALSE)
cat("P5 seed35:", coef(m5), m5$sigma2, "\n")
res <- t(sapply(1:200, function(s) { set.seed(1000+s); y <- arima.sim(n = 2000, model = list(ma = -2.5)); m <- arima(y, order = c(0,0,1), include.mean = FALSE); c(coef(m), m$sigma2) }))
cat("P5 200 semillas: theta media", mean(res[,1]), " rango", range(res[,1]), " s2 media", mean(res[,2]), " rango", range(res[,2]), "\n")
set.seed(329); y6 <- rnorm(100); f6 <- arima(y6, order = c(1,0,1), method = "ML")
cat("P6:", coef(f6), sqrt(diag(f6$var.coef)), "\n")
cat("P6 t:", coef(f6)[1:2]/sqrt(diag(f6$var.coef))[1:2], " suma:", sum(coef(f6)[1:2]), "\n")
cat("P6 AICc: RB", aicc(arima(y6, order = c(0,0,0), method = "ML"),100), " MA1", aicc(arima(y6, order = c(0,0,1), method = "ML"),100),
    " AR1", aicc(arima(y6, order = c(1,0,0), method = "ML"),100), " ARMA11", aicc(f6,100), "\n")
w7 <- acos(0.9/(2*sqrt(0.5))); cat("P7:", 2*pi/w7, " grados:", 2*pi/(w7*180/pi), " sin raiz:", 2*pi/acos(0.9/(2*0.5)), " pico espectral:", 2*pi/acos(0.9*(-0.5-1)/(4*-0.5)), " pasos:", sqrt(0.5), 0.9/(2*sqrt(0.5)), w7, "\n")
man <- window(sunspot.year, 1770, 1869); a2 <- arima(sqrt(man), order = c(2,0,0), method = "ML"); a2c <- arima(man, order = c(2,0,0), method = "ML")
cat("P8 AR(2) crudo LB12 fitdf=2:", Box.test(residuals(a2c), 12, "Ljung-Box", fitdf = 2)$p.value, " sin fitdf:", Box.test(residuals(a2c), 12, "Ljung-Box")$p.value, "\n")
a1 <- arima(man, order = c(1,0,0), method = "ML"); r <- acf(residuals(a1), 20, plot = FALSE)$acf[-1]
cat("P9 r1:", r[1], " banda:", 1.96/sqrt(100), " fuera:", which(abs(r) > 1.96/sqrt(100)), " (", sum(abs(r) > 1.96/sqrt(100)), ")  LB:", Box.test(residuals(a1), 12, "Ljung-Box", fitdf = 1)$p.value, " r1/banda:", r[1]/0.196, "\n")
cat("P9 AR(2) residuales r1 r2:", acf(residuals(a2c), 2, plot = FALSE)$acf[2:3], "\n")
cat("P10 YW/ML manchas:", ar(man, order.max = 2, aic = FALSE)$var.pred, a2c$sigma2, "\n")
h("Propuesta para la P4 (psi_1 distinto de 0.3)")
for (pt in list(c(0.6,-0.2), c(0.7,-0.3), c(0.5,-0.1))) { ph <- pt[1]; th <- pt[2]; p1 <- ph+th; p2 <- ph*p1
  cat("phi", ph, "theta", th, ": Var =", s2*(1+p1^2), " sin s2", 1+p1^2, " sin psi0", s2*p1^2, " psi1=phi", s2*(1+ph^2), " signo", s2*(1+(ph-th)^2), " sin cuadrado", s2*(1+p1), " hasta h", round(s2*(1+p1^2+p2^2),4), "\n") }
