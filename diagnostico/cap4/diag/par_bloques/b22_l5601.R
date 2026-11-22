library(forecast); library(tseries)
ly <- log(lynx); n <- length(ly)   # 114

# --- Las pruebas: las dos dicen d = 0 ------------------------------------
c(ndiffs_kpss = ndiffs(ly, test = "kpss"), ndiffs_adf = ndiffs(ly, test = "adf"))
#> ndiffs_kpss  ndiffs_adf
#>           0           0
c(kpss_p = kpss.test(ly)$p.value, adf_p = adf.test(ly)$p.value)
#> kpss_p  adf_p
#>   0.10   0.01     KPSS no rechaza estacionariedad; ADF rechaza raiz unitaria

# --- El criterio de la varianza: AQUI FALLA ------------------------------
round(sapply(0:3, function(d) var(if (d == 0) ly else diff(ly, differences = d))), 4)
#> [1] 1.6532 0.6871 0.6026 1.1532
# la varianza BAJA al diferenciar (-58 %) y su minimo esta en d = 2:
# la regla no solo no avisa, sino que propone diferenciar DOS veces

# --- Las raices sí lo detectan -------------------------------------------
for (o in list(c(2,1,0), c(2,1,1), c(0,1,1))) {
  f <- arima(ly, order = o, method = "ML")
  ma <- coef(f)[grepl("^ma", names(coef(f)))]
  cat(sprintf("ARIMA(%d,%d,%d)  |raiz MA| = %s\n", o[1], o[2], o[3],
      if (length(ma)) sprintf("%.4f", min(Mod(polyroot(c(1, ma))))) else "-"))
}
#> ARIMA(2,1,0)  |raiz MA| = -
#> ARIMA(2,1,1)  |raiz MA| = 1.0000     <- el MA cancela la diferencia
#> ARIMA(0,1,1)  |raiz MA| = 1.5076

# --- El modelo sin diferenciar: el ciclo, recuperado ----------------------
f <- arima(ly, order = c(2, 0, 0), method = "ML")
r <- polyroot(c(1, -coef(f)[1:2]))
round(c(phi1 = coef(f)[["ar1"]], phi2 = coef(f)[["ar2"]],
        modulo = Mod(r)[1], periodo = 2*pi/Arg(r[which.max(Im(r))])), 4)
#>    phi1    phi2  modulo periodo
#>  1.3776 -0.7399  1.1626  9.7839
Box.test(residuals(f), lag = 20, type = "Ljung-Box", fitdf = 2)$p.value
#> [1] 0.009434283     el AR(2) tampoco basta
as.character(auto.arima(ly, stepwise = FALSE, approximation = FALSE, seasonal = FALSE))
#> [1] "ARIMA(2,0,3) with non-zero mean"