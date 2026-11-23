suppressMessages(library(forecast))
trm <- ts(read.csv("trm_mensual_2015-01_2026-06.csv")$trm, start = c(2015, 1), frequency = 12)
f <- arima(trm, order = c(2, 1, 2), method = "ML")
cat("R: loglik", round(f$loglik, 2), " sigma2", round(f$sigma2, 1), " nobs", f$nobs, "\n")
for (p in list(c(0.5958, -0.8858, -0.5028, 0.8839), c(0.6612, -0.9917, -0.6226, 0.9999632))) {
  g <- tryCatch(arima(trm, order = c(2, 1, 2), fixed = p, transform.pars = FALSE, method = "ML"), error = function(e) NULL)
  if (!is.null(g)) cat("R en", p, ": loglik", round(g$loglik, 2), " sigma2", round(g$sigma2, 1), "\n")
}
