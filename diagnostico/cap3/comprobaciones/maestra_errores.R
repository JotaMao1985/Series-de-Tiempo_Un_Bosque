# Capítulo 3 · comprobaciones de la sesión maestra sobre el diagnóstico (2026-11-19)
# E3 (Ljung–Box por ventana) y periodo del AR(2) con las dos fórmulas
for (v in list(c(1770,1869), c(1889,1988), c(1900,1988))) {
  x <- sqrt(window(sunspot.year, v[1], v[2])); f <- arima(x, order=c(2,0,0), method="ML")
  cat(v, length(x), round(Box.test(residuals(f), 12, "Ljung-Box", fitdf=2)$p.value,4), "\n")
}
p <- c(1.4027,-0.6853); cat("arg:", 2*pi/acos(p[1]/(2*sqrt(-p[2]))), " FPP3 §9.5 (periodo medio):", 2*pi/acos(-p[1]*(1-p[2])/(4*p[2])), "\n")

# M9: PACF de la serie cruda y de la raíz; envolvente de los psi
x <- window(sunspot.year, 1770, 1869); b <- 1.96/sqrt(length(x))
for (s in list(list("cruda", x), list("raiz", sqrt(x)))) { p <- pacf(s[[2]], 25, plot=FALSE)$acf; cat(s[[1]], "banda", round(b,3), "fuera:", which(abs(p) > b), "| r6,r9,r16:", round(p[c(6,9,16)],3), "\n") }
R <- 0.8278; w <- 0.5601; j <- 0:24; psi <- R^j*sin((j+1)*w)/sin(w); cat("1/sin w", round(1/sin(w),3), "fuera de R^j:", sum(abs(psi) > R^j + 1e-12), "de", length(j), "\n")

# M8: primer residual de R frente al crudo; arima.sim de una caminata
x <- window(sunspot.year, 1770, 1869); f <- arima(x, order=c(2,0,0), method="ML")
mu <- coef(f)["intercept"]; ph <- coef(f)[1:2]
g0 <- ARMAacf(ar=ph, lag.max=0); v <- 1/(1-sum(ph*ARMAacf(ar=ph,lag.max=2)[2:3]))  # gamma0/sigma2
cat("res1 R", round(residuals(f)[1],2), " x1-mu", round(x[1]-mu,2), " (x1-mu)/sqrt(g0/s2)", round((x[1]-mu)/sqrt(v),2), " g0/s2", round(v,3), "\n")
y <- arima.sim(list(order=c(0,1,0)), n=10); cat("arima.sim 0,1,0 largo", length(y), " es caminata:", isTRUE(all.equal(class(y),"ts")), "\n")

# M5: la recursión del AR aplicada a rho_1 del ARMA(2,1) phi = (0.5, 0.3), theta = 0.4
r <- ARMAacf(ar = c(0.5, 0.3), ma = 0.4, lag.max = 2); cat("rho1", round(r[2], 4), " mal (rho_-1 = 1):", 0.5 + 0.3, " bien (rho_-1 = rho_1):", round(0.5 + 0.3 * r[2], 4), "
")
