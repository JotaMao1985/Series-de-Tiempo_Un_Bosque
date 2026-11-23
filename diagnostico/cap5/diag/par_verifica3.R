# par_verifica3.R — M2 l. 3568-3575: ¿la ACF de un MA x SMA se factoriza con q < m o hace falta 2q < m?
suppressMessages(library(forecast))
m <- 12
for (q in c(1, 5, 7)) {
  th <- c(0.5, 0.4, 0.3, 0.2, 0.1, 0.3, 0.6)[1:q]; Th <- 0.5
  ma <- numeric(q + m); ma[1:q] <- th; ma[m] <- Th; ma[m + (1:q)] <- Th * th
  r <- ARMAacf(ma = ma, lag.max = q + m)[-1]
  rreg <- ARMAacf(ma = th, lag.max = q)[-1]; rest <- Th / (1 + Th^2)
  g0 <- sum(c(1, ma)^2); g0f <- sum(c(1, th)^2) * (1 + Th^2)
  k <- 5
  cat(sprintf("q=%d: gamma0 exacta=%.4f factorizada=%.4f | rho_5 exacta=%.4f  rho_reg_5*rho_est_0=%.4f | rho_12 exacta=%.4f rho_reg_0*rho_est_1=%.4f\n",
      q, g0, g0f, r[k], if (k <= q) rreg[k] else 0, r[12], rest))
}
