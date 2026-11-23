# Verificador A, segunda lectura: el c4m9 nuevo (austres), resuelto por otra via
suppressPackageStartupMessages(library(forecast))
f <- utils:::index.search("austres", find.package("datasets"))
tools::Rd2txt(utils:::.getHelpFile(f), options = list(underline_titles = FALSE))
y <- austres; print(tsp(y)); cat("n =", length(y), " inicio:", start(y), " fin:", end(y), "\n")
cat("ndiffs kpss/adf/pp:", sapply(c("kpss","adf","pp"), function(t) ndiffs(y, test = t)), "  nsdiffs:", nsdiffs(y), "\n")
A <- Arima(y, order = c(0,1,1)); B <- Arima(y, order = c(0,1,1), include.drift = TRUE); C <- Arima(y, order = c(0,2,1))
print(round(rbind(theta = c(A = coef(A)[["ma1"]], B = coef(B)[["ma1"]], C = coef(C)[["ma1"]]),
                  sigma = sqrt(c(A$sigma2, B$sigma2, C$sigma2))), 4))
# pendiente de C por su forma cerrada: SES de las diferencias con alpha = 1 + theta
al <- 1 + coef(C)[["ma1"]]; w <- diff(y); cat("alpha de C =", round(al, 4), "\n")
pesos <- al * (1 - al)^(0:(length(w) - 1)); cat("peso de las 8 ultimas diferencias en la pendiente de C:", round(sum(pesos[1:8]), 3),
   "  de las 20 ultimas:", round(sum(pesos[1:20]), 3), "\n")
# anchos a mano desde los psi (y los de forecast)
sig <- function(f, psi, h) 2 * qnorm(.975) * sqrt(f$sigma2 * sum(psi[1:h]^2))
psiA <- c(1, rep(1 + coef(A)[["ma1"]], 39)); psiB <- c(1, rep(1 + coef(B)[["ma1"]], 39))
psiC <- c(1, ARMAtoMA(ar = c(2, -1), ma = coef(C)[["ma1"]], lag.max = 39))
print(round(rbind(A = c(sig(A, psiA, 1), sig(A, psiA, 40)), B = c(sig(B, psiB, 1), sig(B, psiB, 40)), C = c(sig(C, psiC, 1), sig(C, psiC, 40))), 1))
cat("cocientes: C/B a 40 =", round(sig(C, psiC, 40) / sig(B, psiB, 40), 2), " B 40/1 =", round(sig(B, psiB, 40) / sig(B, psiB, 1), 2),
    " C 40/1 =", round(sig(C, psiC, 40) / sig(C, psiC, 1), 2), "\n")
pb <- forecast(B, h = 40); pc <- forecast(C, h = 40); cat("B - C a 40:", round(pb$mean[40] - pc$mean[40], 1), "\n")
for (L in c(8, 10, 20)) cat("Ljung-Box lag", L, ":", round(sapply(list(A, B, C), function(f) Box.test(residuals(f), lag = L, type = "Ljung-Box", fitdf = 1)$p.value), 4), "\n")
print(round(acf(residuals(B), lag.max = 8, plot = FALSE)$acf[-1], 3))
# un modelo de B que pase: ARIMA(p,1,q) con deriva
print(auto.arima(y, seasonal = FALSE))
