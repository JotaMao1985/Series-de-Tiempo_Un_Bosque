# Diagnóstico cap. 5 · complemento del barrido: (a) la trampa del orden en la escala CRUDA
# (USAccDeaths no lleva logaritmo) y (c) candidatas con parte SAR para el M4.
#   LC_ALL=en_US.UTF-8 Rscript diagnostico/cap5/diag/ejercicios_series_barrido2.R > diagnostico/cap5/diag/ejercicios_series_barrido2.out 2>&1
suppressPackageStartupMessages({ library(forecast); library(fpp3); library(tseries) })
options(width = 200, warn = -1)
a_ts <- function(idx, y) { idx <- as.Date(idx); o <- order(idx); y <- y[o]; idx <- idx[o]
  ts(y, start = c(as.numeric(format(idx[1], "%Y")), as.numeric(format(idx[1], "%m"))), frequency = 12) }
lb <- function(f) round(Box.test(residuals(f), lag = 24, type = "Ljung-Box", fitdf = sum(f$arma[1:4]))$p.value, 4)
L <- list()
r <- as_tibble(aus_retail); for (k in unique(paste(r$State, r$Industry, sep = " | "))) {
  s <- r[paste(r$State, r$Industry, sep = " | ") == k, ]; L[[paste("aus_retail:", k)]] <- a_ts(s$Month, s$Turnover) }
l <- as_tibble(aus_livestock); for (k in unique(paste(l$State, l$Animal, sep = " | "))) {
  s <- l[paste(l$State, l$Animal, sep = " | ") == k, ]; if (nrow(s) >= 120) L[[paste("aus_livestock:", k)]] <- a_ts(s$Month, s$Count) }
for (k in unique(nsw_offences$Type)) { s <- as_tibble(filter(nsw_offences, Type == k)); L[[paste("nsw_offences:", k)]] <- a_ts(s$Month, s$Count) }
for (k in unique(aus_births$State)) { s <- as_tibble(filter(aus_births, State == k)); L[[paste("aus_births:", k)]] <- a_ts(s$Month, s$Births) }
cat("(a) escala cruda: ndiffs(y) = 0 y ndiffs(∇12 y) = 1, entre", length(L), "series\n")
for (nm in names(L)) { y <- na.omit(L[[nm]]); if (length(y) < 72) next
  if (ndiffs(y) == 0 && ndiffs(diff(y, lag = 12)) == 1)
    cat(sprintf("  %-70s n=%d nsdiffs=%d ocsb=%d\n", nm, length(y), nsdiffs(y), nsdiffs(y, test = "ocsb"))) }
cat("\n(c) candidatas con parte SAR (auto.arima, búsqueda por defecto)\n")
data(nino, package = "tseries")
C <- list(nino3 = nino3, vic_cerdos = L[["aus_livestock: Victoria | Pigs"]],
          nsw_nacimientos = L[["aus_births: NSW"]], wa_ganado = L[["aus_livestock: Western Australia | Cattle (excl. calves)"]])
for (nm in names(C)) { y <- C[[nm]]; f <- auto.arima(y)
  a <- Acf(diff(y, lag = 12), lag.max = 36, plot = FALSE)$acf; p <- Pacf(diff(y, lag = 12), lag.max = 36, plot = FALSE)$acf
  cat(sprintf("  %-16s n=%d nsdiffs=%d auto=%s LB=%.4f | ∇12: ACF 12/24/36 = %.3f %.3f %.3f ; PACF 12/24/36 = %.3f %.3f %.3f ; banda %.3f\n",
      nm, length(y), nsdiffs(y), as.character(f), lb(f), a[13], a[25], a[37], p[12], p[24], p[36], 1.96 / sqrt(length(y) - 12))) }
