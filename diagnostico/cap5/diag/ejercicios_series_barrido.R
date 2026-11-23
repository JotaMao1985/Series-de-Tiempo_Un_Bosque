# Diagnóstico cap. 5 · barrido de series mensuales de tsibbledata/fpp3 para tres huecos
# que ejercicios_series_candidatas.R no cubrió con las doce candidatas:
#   (a) la trampa del orden del M3/M8: ndiffs(crudo) = 0 y ndiffs(∇12 y) = 1 (como USAccDeaths)
#   (b) la trampa del AICc entre D del M6: un SARIMA(0,1,1)(1,0,1)12 (D = 0) con MENOR AICc
#       que el airline (D = 1), como el S3 del simulacro
#   (c) identificación del M4: el airline no pasa y el (0,1,1)(1,1,0)12 sí (SAR en vez de SMA)
#   LC_ALL=en_US.UTF-8 Rscript diagnostico/cap5/diag/ejercicios_series_barrido.R > diagnostico/cap5/diag/ejercicios_series_barrido.out 2>&1
suppressPackageStartupMessages({ library(forecast); library(fpp3) })
options(width = 200, warn = -1)
a_ts <- function(idx, y) { idx <- as.Date(idx); o <- order(idx); y <- y[o]; idx <- idx[o]
  ts(y, start = c(as.numeric(format(idx[1], "%Y")), as.numeric(format(idx[1], "%m"))), frequency = 12) }
lb <- function(f) round(Box.test(residuals(f), lag = 24, type = "Ljung-Box", fitdf = sum(f$arma[1:4]))$p.value, 4)
seguro <- function(e) tryCatch(e, error = function(x) NULL)
L <- list()
r <- as_tibble(aus_retail); for (k in unique(paste(r$State, r$Industry, sep = " | "))) {
  s <- r[paste(r$State, r$Industry, sep = " | ") == k, ]; L[[paste("aus_retail:", k)]] <- a_ts(s$Month, s$Turnover) }
l <- as_tibble(aus_livestock); for (k in unique(paste(l$State, l$Animal, sep = " | "))) {
  s <- l[paste(l$State, l$Animal, sep = " | ") == k, ]; if (nrow(s) >= 120 && all(s$Count > 0)) L[[paste("aus_livestock:", k)]] <- a_ts(s$Month, s$Count) }
for (k in unique(nsw_offences$Type)) { s <- as_tibble(filter(nsw_offences, Type == k)); if (all(s$Count > 0)) L[[paste("nsw_offences:", k)]] <- a_ts(s$Month, s$Count) }
for (k in unique(aus_vehicle_sales$Type)) { s <- as_tibble(filter(aus_vehicle_sales, Type == k)); L[[paste("aus_vehicle_sales:", k)]] <- a_ts(s$Month, s$Count) }
cat("series barridas:", length(L), "\n")
out <- list()
for (nm in names(L)) {
  y0 <- na.omit(L[[nm]]); if (length(y0) < 120 || any(y0 <= 0)) next
  y <- log(y0)
  nd <- ndiffs(y); nd2 <- ndiffs(diff(y, lag = 12)); nsd <- nsdiffs(y)
  air <- seguro(Arima(y, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12)))
  d0 <- seguro(Arima(y, order = c(0, 1, 1), seasonal = list(order = c(1, 0, 1), period = 12)))
  sar <- seguro(Arima(y, order = c(0, 1, 1), seasonal = list(order = c(1, 1, 0), period = 12)))
  if (is.null(air) || is.null(d0) || is.null(sar)) next
  out[[nm]] <- data.frame(serie = nm, n = length(y), nd = nd, nsd = nsd, nd_trasD = nd2,
    aicc_air = round(air$aicc, 2), lb_air = lb(air), aicc_D0 = round(d0$aicc, 2), lb_D0 = lb(d0),
    aicc_sar = round(sar$aicc, 2), lb_sar = lb(sar))
}
T <- do.call(rbind, out); rownames(T) <- NULL
cat("series con los tres ajustes:", nrow(T), "\n")
cat("\n(a) trampa del orden: ndiffs crudo 0 y tras ∇12 1\n"); print(T[T$nd == 0 & T$nd_trasD == 1, ], row.names = FALSE)
cat("\n(b) AICc(D = 0) < AICc(airline), con nsdiffs = 1\n"); bb <- T[T$aicc_D0 < T$aicc_air & T$nsd == 1, ]
print(head(bb[order(bb$aicc_D0 - bb$aicc_air), ], 12), row.names = FALSE)
cat("   de ellas, con el airline que pasa LB(24) y el D = 0 que no:", sum(bb$lb_air >= 0.05 & bb$lb_D0 < 0.05), "\n")
print(bb[bb$lb_air >= 0.05 & bb$lb_D0 < 0.05, ], row.names = FALSE)
cat("\n(c) airline rechaza LB y (0,1,1)(1,1,0) no, con AICc menor\n")
cc <- T[T$lb_air < 0.05 & T$lb_sar >= 0.05 & T$aicc_sar < T$aicc_air, ]; print(head(cc, 12), row.names = FALSE)
