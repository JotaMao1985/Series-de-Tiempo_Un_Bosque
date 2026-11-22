# Diagnóstico cap. 4 · ejercicios, autoevaluación y simulacro
#   Rscript diagnostico/cap4/diag/ejercicios_cap4.R > diagnostico/cap4/diag/ejercicios_cap4.out 2>&1
# Reproduce las tres soluciones (E1-E3), recalcula las claves del quiz `cap4`,
# calcula las del simulacro del M11 (que no trae clave) y mide lo que el
# informe afirma sobre ellas. Nada de esto toca el HTML.
suppressPackageStartupMessages({ library(forecast); library(tseries) })
options(width = 110)
cat("R:", R.version.string, "· forecast", as.character(packageVersion("forecast")),
    "· tseries", as.character(packageVersion("tseries")), "\n")
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
raizMA <- function(f) { ma <- coef(f)[grepl("^ma", names(coef(f)))]
  if (length(ma)) min(Mod(polyroot(c(1, ma)))) else NA }
raizAR <- function(f) { ar <- coef(f)[grepl("^ar", names(coef(f)))]
  if (length(ar)) min(Mod(polyroot(c(1, -ar)))) else NA }
titulo <- function(s) cat("\n=====", s, "=====\n")

# ---------------------------------------------------------------------------
titulo("E1 · BJsales: varianzas, pruebas, rejilla d = 1")
n <- length(BJsales); print(n)
print(round(sapply(0:3, function(d) var(if (d == 0) BJsales else diff(BJsales, differences = d))), 4))
print(round(c(adf = adf.test(BJsales)$p.value, ndiffs = ndiffs(BJsales),
              ndiffs_adf = ndiffs(BJsales, test = "adf"), ndiffs_pp = ndiffs(BJsales, test = "pp")), 4))
print(suppressWarnings(c(kpss_p = kpss.test(BJsales)$p.value, kpss_d1_p = kpss.test(diff(BJsales))$p.value,
                         adf_d1_p = adf.test(diff(BJsales))$p.value)))
rej1 <- do.call(rbind, lapply(0:2, function(q) do.call(rbind, lapply(0:2, function(p) {
  f <- arima(BJsales, order = c(p, 1, q), method = "ML")
  data.frame(p, q, aicc = round(aicc(f, n - 1), 3), bic = round(BIC(f), 3),
             lb20 = round(Box.test(residuals(f), lag = 20, type = "Ljung-Box", fitdf = p + q)$p.value, 4),
             rAR = round(raizAR(f), 4), rMA = round(raizMA(f), 4))
}))))
print(rej1)
cat("rango AICc del (0,1,1) entre los 9 (1 = mejor):", rank(rej1$aicc)[rej1$p == 0 & rej1$q == 1], "\n")
f011 <- arima(BJsales, order = c(0, 1, 1), method = "ML")
cat("ACF residuos (0,1,1), rezagos 1-10:\n"); print(round(as.numeric(acf(residuals(f011), lag.max = 10, plot = FALSE)$acf)[-1], 4))
print(round(1.96 / sqrt(length(residuals(f011))), 4))
cat("Ljung-Box del (0,1,1) a 10 y 20 rezagos:\n")
print(round(sapply(c(10, 20), function(h) Box.test(residuals(f011), lag = h, type = "Ljung-Box", fitdf = 1)$p.value), 4))
f111 <- arima(BJsales, order = c(1, 1, 1), method = "ML")
print(round(c(phi = coef(f111)[["ar1"]], ee_phi = sqrt(f111$var.coef[1,1]),
              theta = coef(f111)[["ma1"]], ee_theta = sqrt(f111$var.coef[2,2])), 4))
print(shapiro.test(residuals(f111))$p.value)
print(as.character(auto.arima(BJsales, stepwise = FALSE, approximation = FALSE)))
print(as.character(auto.arima(BJsales)))
titulo("E1 · la rejilla con d = 2 (p, q en 0:2)")
rej2 <- do.call(rbind, lapply(0:2, function(q) do.call(rbind, lapply(0:2, function(p) {
  f <- tryCatch(arima(BJsales, order = c(p, 2, q), method = "ML"), error = function(e) NULL)
  if (is.null(f)) return(NULL)
  data.frame(p, q, aicc = round(aicc(f, n - 2), 3), rMA = round(raizMA(f), 4))
}))))
print(rej2[order(rej2$aicc), ])
f122 <- arima(BJsales, order = c(1, 2, 2), method = "ML")
print(round(c(d1 = aicc(f111, n - 1), d2 = aicc(f122, n - 2)), 3))
cat("¿el menor AICc de d=2 es menor que el de d=1? ", min(rej2$aicc) < min(rej1$aicc), "\n")
cat("Lectura literal del enunciado («su AICc» = el del IMA(1,1)) frente al mejor de d = 2:\n")
print(round(c(aicc_IMA = aicc(f011, n - 1), mejor_d2 = min(rej2$aicc), IMA_menos_d2 = aicc(f011, n - 1) - min(rej2$aicc),
              IMA_menos_mejor_d1 = aicc(f011, n - 1) - min(rej1$aicc)), 3))

# ---------------------------------------------------------------------------
titulo("E2 · log(lynx)")
ly <- log(lynx); print(length(ly))
print(c(ndiffs_kpss = ndiffs(ly, test = "kpss"), ndiffs_adf = ndiffs(ly, test = "adf"), ndiffs_pp = ndiffs(ly, test = "pp")))
print(suppressWarnings(c(kpss_p = kpss.test(ly)$p.value, adf_p = adf.test(ly)$p.value, pp_p = pp.test(ly)$p.value)))
v <- sapply(0:3, function(d) var(if (d == 0) ly else diff(ly, differences = d)))
print(round(v, 4)); cat("caída d0->d1:", round(100 * (1 - v[2] / v[1]), 1), "%\n")
for (o in list(c(2,1,0), c(2,1,1), c(0,1,1), c(1,1,1), c(3,1,1))) {
  f <- arima(ly, order = o, method = "ML")
  cat(sprintf("ARIMA(%d,%d,%d)  |raiz MA| = %s  |raiz AR| = %s\n", o[1], o[2], o[3],
              format(round(raizMA(f), 4)), format(round(raizAR(f), 4))))
}
f <- arima(ly, order = c(2, 0, 0), method = "ML"); r <- polyroot(c(1, -coef(f)[1:2]))
print(round(c(phi1 = coef(f)[["ar1"]], phi2 = coef(f)[["ar2"]], modulo = Mod(r)[1],
              periodo = 2*pi/Arg(r[which.max(Im(r))])), 4))
print(Box.test(residuals(f), lag = 20, type = "Ljung-Box", fitdf = 2)$p.value)
print(as.character(auto.arima(ly, stepwise = FALSE, approximation = FALSE, seasonal = FALSE)))
print(as.character(auto.arima(ly)))

# ---------------------------------------------------------------------------
titulo("E3 · BJsales, intervalo desde los psi")
f  <- Arima(BJsales, order = c(1, 1, 1))
ph <- coef(f)[["ar1"]]; th <- coef(f)[["ma1"]]; s <- sqrt(f$sigma2); H <- 12
psi <- c(1, ARMAtoMA(ar = c(1 + ph, -ph), ma = th, lag.max = H))
sigma_h <- s * sqrt(cumsum(psi^2))[1:H]
print(round(psi[1:5], 4)); print(round(sigma_h[1:5], 4))
fc <- forecast(f, h = H, level = 95); semi <- as.numeric((fc$upper - fc$lower) / 2)
print(round(semi[1:5], 4)); print(max(abs(semi - qnorm(0.975) * sigma_h)))
print(round(c(s12_s1 = sigma_h[H] / sigma_h[1], raiz12 = sqrt(H), frente_caminata = sigma_h[H] / (s * sqrt(H))), 4))
print(round(c(psi_12 = psi[H + 1], limite = (1 + th) / (1 - ph)), 4))
cat("Arima (CSS-ML) frente a arima(ML): phi, theta, aicc\n")
print(round(rbind(Arima = c(ph, th, f$aicc), arimaML = c(coef(f111), aicc(f111, n - 1))), 4))
fd <- Arima(BJsales, order = c(1, 1, 1), include.drift = TRUE)
print(round(c(deriva = coef(fd)[["drift"]], ee = sqrt(diag(fd$var.coef))[["drift"]],
              t = coef(fd)[["drift"]] / sqrt(diag(fd$var.coef))[["drift"]]), 4))
print(round(c(aicc_con = fd$aicc, aicc_sin = f$aicc), 3))
print(round(c(h12_con = forecast(fd, h = H)$mean[H], h12_sin = forecast(f, h = H)$mean[H]), 2))

# ---------------------------------------------------------------------------
titulo("Quiz cap4 · claves")
fn <- Arima(Nile, order = c(1, 1, 1))
psiN <- c(1, ARMAtoMA(ar = c(1 + coef(fn)[1], -coef(fn)[1]), ma = coef(fn)[2], lag.max = 3))
cat("Q2 · sigma, psi1, sigma_2:\n")
print(round(c(sigma = sqrt(fn$sigma2), psi1_nilo = psiN[2], sigma2 = sqrt(fn$sigma2) * sqrt(1 + psiN[2]^2),
              con_psi1_redondeado = 142.045 * sqrt(1 + 0.3802^2), sin_psi0 = 142.045 * 0.3802,
              sin_cuadrado = 142.045 * sqrt(1 + 0.3802), caminata = 142.045 * sqrt(2)), 4))
cat("Q1 · AICc d=1 y d=2 de la rejilla del Nilo:\n")
print(round(c(a111 = aicc(arima(Nile, order = c(1,1,1), method = "ML"), 99),
              a122 = aicc(arima(Nile, order = c(1,2,2), method = "ML"), 98),
              rMA122 = raizMA(arima(Nile, order = c(1,2,2), method = "ML"))), 3))
cat("Q3 · log(AirPassengers), mejor no estacional exhaustivo; ACF residual 12 y 24, LB(24):\n")
ap <- auto.arima(log(AirPassengers), seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
print(as.character(ap)); ra <- acf(residuals(ap), lag.max = 24, plot = FALSE)$acf[-1]
print(round(c(r12 = ra[12], r24 = ra[24], banda = 1.96 / sqrt(length(AirPassengers)),
              Q24 = unname(Box.test(residuals(ap), lag = 24, type = "Ljung-Box")$statistic)), 4))
cat("Q4 · intercept con d=0, coef con d=1 e include.mean, deriva con d=2:\n")
print(round(coef(arima(Nile, order = c(1, 0, 1), method = "ML"))[["intercept"]], 4))
print(names(coef(arima(Nile, order = c(1, 1, 1), include.mean = TRUE, method = "ML"))))
w <- tryCatch(Arima(Nile, order = c(1, 2, 1), include.drift = TRUE), warning = function(w) conditionMessage(w)); print(w)
m2 <- as.numeric(forecast(Arima(Nile, order = c(1, 2, 1)), h = 30)$mean)
print(round(c(d2_h30 = m2[30] - 2*m2[29] + m2[28]), 6))
cat("Q5 · KPSS sobre RB + escalón en 29, 1000 réplicas (semilla 2026):\n")
set.seed(2026); esc <- as.numeric(1:100 >= 29)
tasa <- function(beta, reps = 1000) mean(replicate(reps, suppressWarnings(kpss.test(1000 + beta*esc + rnorm(100, 0, 127.03))$p.value) <= 0.05))
print(c(b0 = tasa(0), b100 = tasa(-100), nilo = tasa(-247.78)))
cat("Q6 · ACF del Nilo sin diferenciar, rezagos 1-4 y 20:\n")
an <- acf(Nile, lag.max = 20, plot = FALSE)$acf[-1]; print(round(an[c(1:4, 20)], 3))
cat("Q7 · podio de la exhaustiva:\n")
tr <- capture.output(invisible(auto.arima(Nile, trace = TRUE, seasonal = FALSE, stepwise = FALSE, approximation = FALSE)))
tr <- grep("^ ARIMA.*:", tr, value = TRUE)
val <- suppressWarnings(as.numeric(sub(".*:\\s*", "", tr)))
o <- order(val); print(data.frame(modelo = trimws(sub(":.*", "", tr[o[1:8]])), aicc = val[o[1:8]]))
cat("distancia 1.º-7.º:", round(val[o[7]] - val[o[1]], 3), "\n")
cat("Q8 · MA(1) sobre diff(Nile, 2):\n")
f8 <- arima(diff(Nile, differences = 2), order = c(0, 0, 1), include.mean = FALSE, method = "ML")
print(round(c(theta = coef(f8)[[1]], raiz = Mod(polyroot(c(1, coef(f8)[[1]])))), 4))

# ---------------------------------------------------------------------------
titulo("Simulacro M11 (variante 9) · claves calculadas")
cat("P1 · rho2 del ARMA(1,1) phi = 0.57, theta = 0.25:\n")
print(round(ARMAacf(ar = 0.57, ma = 0.25, lag.max = 2), 4))
cat("P2 · polyroot del informe y el correcto; c = mu(1 - phi1 - phi2):\n")
print(round(Mod(polyroot(c(67.1246, -1.2254, 0.3688))), 4)); print(round(Mod(polyroot(c(1, -1.2254, 0.3688))), 4))
print(round(67.1246 * (1 - 1.2254 + 0.3688), 4))
cat("P4 · Yule-Walker desde gamma0, gamma1, gamma2:\n")
g <- c(16.0539, 11.8658, 4.9091); r1 <- g[2]/g[1]; r2 <- g[3]/g[1]
phiYW <- solve(matrix(c(1, r1, r1, 1), 2), c(r1, r2)); print(round(phiYW, 4))
cat("   distractores: phi1 = r1 sin corregir, PACF(2):", round(r1, 4), round((r2 - r1^2)/(1 - r1^2), 4), "\n")
cat("P5 · AICc con n = 40, k = parámetros + media + sigma2:\n")
lL <- c(MA1 = -54.460, AR1 = -59.190, MA2 = -52.821, ARMA11 = -53.428); k <- c(3, 3, 4, 4)
a5 <- -2*lL + 2*k + 2*k*(k+1)/(40 - k - 1); print(round(sort(a5), 3))
cat("P6 · límite superior en la escala original, raíz cuadrada:\n")
s2 <- 2.14 * (1 + 1.22^2); print(round(c(sigma_2 = sqrt(s2), sup_raiz = 5.83 + 1.96*sqrt(s2),
  sup_original = (5.83 + 1.96*sqrt(s2))^2, error_sin_psi = (5.83 + 1.96*sqrt(2.14))^2), 2))
cat("P7 · raíces y coeficientes en niveles:\n")
print(round(c(raiz_fila2 = 1/0.96, phi1_fila3 = 1.65, phi2_fila3 = -0.65,
              modulo_fila5 = min(Mod(polyroot(c(1, -1.25, 0.45))))), 4))
cat("P8 · Ljung-Box, fitdf = 3:\n")
print(round(c(gl = 16 - 3, critico = qchisq(0.95, 13), p13 = 1 - pchisq(23.329, 13), p16 = 1 - pchisq(23.329, 16)), 4))
cat("P10 · razón de varianzas d1/d0 y d2/d1; PACF teórica de un MA(1) con rho1 = 0.411:\n")
th10 <- (1 - sqrt(1 - 4*0.411^2)) / (2*0.411)
print(round(c(theta = th10, ARMAacf(ma = th10, lag.max = 3, pacf = TRUE)), 3))
