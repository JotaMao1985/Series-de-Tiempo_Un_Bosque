# Lector B · c4-m3-15: reproduce el Monte Carlo de la raíz unitaria verdadera
# (misma receta que genera_cap4.R §11b, copiada aquí; NO se reejecuta el generador).
suppressMessages({library(tseries)})
cat("R", R.version.string, " tseries", as.character(packageVersion("tseries")), "\n")
phi_sim <- 0.2544; theta_sim <- -0.8741; n_nilo <- 100; N <- 1000
set.seed(2026)
rech_pp <- 0; rech_adf <- 0
for (i in seq_len(N)) {
  x <- 900 + cumsum(arima.sim(list(ar = phi_sim, ma = theta_sim), n = n_nilo))
  if (suppressWarnings(PP.test(x)$p.value) < 0.05) rech_pp <- rech_pp + 1
  if (suppressWarnings(adf.test(x, k = 4)$p.value) < 0.05) rech_adf <- rech_adf + 1
}
cat(sprintf("PP.test rechaza %.1f%% | adf.test(k=4) rechaza %.1f%%\n", 100*rech_pp/N, 100*rech_adf/N))
# comprobación: el JSON del repo
j <- readLines("precalculo/salidas/cap4_arima.json")
i <- grep("sim_raiz_unitaria", j)[1]; cat(j[i:(i+10)], sep = "\n")
