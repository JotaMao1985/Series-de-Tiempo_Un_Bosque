# Verificador B, R1 del cap. 5: recálculo independiente, en R 4.6, de las cifras nuevas o
# cambiadas de las diapositivas. No lee cap5_sarima.json: parte de los datos.
# Uso (desde la raíz del worktree): Rscript diagnostico/cap5/comprobaciones/v1b_cifras_deck.R
suppressMessages(library(forecast))
cat(R.version.string, "· forecast", as.character(packageVersion("forecast")), "\n\n")
ap <- log(AirPassengers)

cat("== Diapositiva «Diferenciar de más»: SARIMA(0,1,1)(0,D,1)_12\n")
for (D in 0:2) {
  f <- Arima(ap, order = c(0, 1, 1), seasonal = list(order = c(0, D, 1), period = 12))
  th <- coef(f)["sma1"]; ee <- sqrt(diag(f$var.coef))["sma1"]
  cat(sprintf("D=%d n=%d Theta=%.4f ee=%.4f distancia=(Theta+1)/ee=%.2f  -1 dentro de Theta±1.96ee: %s  |Theta|^(1/12)=%.4f\n",
              D, f$nobs, th, ee, (th + 1) / ee, abs(th + 1) < 1.96 * ee, abs(th)^(1/12)))
}

cat("\n== Airline\n")
fit <- Arima(ap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12))
th <- unname(coef(fit)[1]); TH <- unname(coef(fit)[2]); ee <- sqrt(diag(fit$var.coef))
print(round(c(theta = th, Theta = TH, ee_theta = unname(ee[1]), ee_Theta = unname(ee[2]),
              dist_theta = (th + 1) / unname(ee[1])), 4))

psi_airline <- function(th, TH, H = 240) {
  # (1-B)(1-B^12) psi(B) = (1+thB)(1+TH B^12)
  ma <- numeric(H); ma[1] <- th; if (H >= 12) ma[12] <- TH; if (H >= 13) ma[13] <- th * TH
  psi <- numeric(H + 1); psi[1] <- 1
  for (j in 1:H) {
    v <- ma[j] + psi[j]
    if (j >= 12) v <- v + psi[j - 11]
    if (j >= 13) v <- v - psi[j - 12]
    psi[j + 1] <- v
  }
  psi  # psi[j+1] = psi_j
}
# comprobación independiente con ARMAtoMA del producto expandido (AR con raíces unitarias)
ar_exp <- c(1, rep(0, 10), 1, -1)                 # (1-B)(1-B^12) = 1 - B - B^12 + B^13 -> phi = (1,0..,0,1,-1)
ma_exp <- c(th, rep(0, 10), TH, th * TH)
psi_ref <- c(1, ARMAtoMA(ar = ar_exp, ma = ma_exp, lag.max = 240))
psi <- psi_airline(th, TH)
cat("max |psi recursión - ARMAtoMA| =", signif(max(abs(psi - psi_ref)), 3), "\n")
sh <- sqrt(cumsum(psi[1:240]^2))
cat(sprintf("sigma_12/sigma_1 = %.2f ; sqrt(12) = %.2f\n", sh[12] / sh[1], sqrt(12)))
cat(sprintf("subida anual de psi (psi_240 - psi_228) = %.4f ; (1+th)(1+TH) = %.4f\n", psi[241] - psi[229], (1 + th) * (1 + TH)))
cat(sprintf("psi_240 = %.2f\n", psi[241]))
cat(sprintf("primer h con sigma_h/sigma > sqrt(h): %d\n", min(which(sh > sqrt(seq_along(sh))))))
cat(sprintf("sigma_240/sigma = %.2f ; sqrt(240) = %.2f\n", sh[240], sqrt(240)))
cat(sprintf("sigma_1, sigma_12, sigma_24 = %.6f %.6f %.6f\n", sqrt(fit$sigma2) * sh[1], sqrt(fit$sigma2) * sh[12], sqrt(fit$sigma2) * sh[24]))
cat("crecimiento de sum psi^2: cociente sh[240]^2/sh[120]^2 =", round(sh[240]^2 / sh[120]^2, 2), "(h^3 daría 8)\n")
for (T in c(0, -0.5569, -0.99)) {
  p <- psi_airline(th, T, 30)
  cat(sprintf("Theta=%6.4f: salto psi_12 - psi_11 = %.4f (1+Theta = %.4f)\n", T, p[13] - p[12], 1 + T))
}
cat(sprintf("psi_12 = %.4f ; psi_13 = %.4f\n", psi[13], psi[14]))

cat("\n== TRM congelada: SAR(1)_12 forzado\n")
trm <- ts(read.csv("Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")$trm, start = c(2015, 1), frequency = 12)
cat("n =", length(trm), "\n")
a <- Acf(diff(trm), lag.max = 36, plot = FALSE)$acf
print(round(c(r12 = a[13], r24 = a[25], r36 = a[37], banda = 1.96 / sqrt(length(trm) - 1)), 5))
g <- Arima(trm, order = c(0, 1, 0), seasonal = list(order = c(1, 0, 0), period = 12))
tt <- coef(g)[1] / sqrt(diag(g$var.coef))[1]
print(round(c(Phi = unname(coef(g)[1]), ee = unname(sqrt(diag(g$var.coef))[1]), t = unname(tt)), 5))
cat("t a 3 decimales:", sprintf("%.3f", tt), " ; a 2:", sprintf("%.2f", tt), "\n")
print(round(c(forzado = g$aicc, simple = Arima(trm, order = c(0, 1, 0))$aicc), 3))

cat("\n== auto.arima con m = 365: el tope de P y Q\n")
cuerpo <- paste(deparse(forecast::auto.arima), collapse = "\n")
for (l in grep("max\\.(P|Q) <-", strsplit(cuerpo, "\n")[[1]], value = TRUE)) cat("  código:", trimws(l), "\n")
set.seed(1)
y <- ts(3 * sin(2 * pi * (1:800) / 365) + rnorm(800), frequency = 365)
cat("  floor(800/(3*365)) =", floor(800 / (3 * 365)), "\n")
fa <- auto.arima(y)
cat("  auto.arima:", as.character(fa), "; nobs =", fa$nobs, "; perdidas =", 800 - fa$nobs, "\n")
