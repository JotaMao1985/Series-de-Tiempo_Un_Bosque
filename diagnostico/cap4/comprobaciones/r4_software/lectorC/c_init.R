# lector C · [c4-m7-22] ¿cambia la verosimilitud con la inicialización del filtro dentro de R? (mismos parámetros)
suppressMessages(library(forecast))
for (s in c("Gardner1980", "Rossignol2011")) {
  b <- arima(Nile, order = c(1,1,1), method = "ML", SSinit = s, fixed = c(0.254370, -0.874135), transform.pars = FALSE)
  cat(sprintf("SSinit = %-14s loglik en (0.254370, -0.874135) = %.6f  nobs = %d\n", s, b$loglik, b$nobs))
}
