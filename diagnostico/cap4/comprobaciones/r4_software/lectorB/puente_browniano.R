# Lector B · derivación del Módulo 3, paso 2: con ruido blanco estacionario alrededor de una media única,
# las sumas parciales de los residuales se comportan como un puente browniano
set.seed(2026)
n <- 400; reps <- 4000
S <- replicate(reps, { x <- rnorm(n); e <- x - mean(x); cumsum(e) / sqrt(n) })    # n x reps
cat("S_n (suma completa) vale 0 en todas las réplicas:", all(abs(S[n, ]) < 1e-9), "\n")
for (r in c(0.1, 0.25, 0.5, 0.75)) {
  t <- r * n
  cat(sprintf("r = %.2f: var(S_t/sqrt(n)) = %.4f  frente a r(1-r) = %.4f\n", r, var(S[t, ]), r * (1 - r)))
}
cat("max|S_t|/sqrt(n) medio:", round(mean(apply(abs(S), 2, max)), 3), " (puente browniano: sqrt(pi/2) * log(2) = ", round(sqrt(pi/2) * log(2), 3), ")\n")
# y con un escalón sin ruido: max|S_t| = tau (1 - tau) n |beta|
n <- 100; beta <- 1; y <- as.numeric(seq_len(n) >= 29) * beta; e <- y - mean(y)
cat("escalón sin ruido: max|S_t| =", max(abs(cumsum(e))), " tau(1-tau) n |beta| con tau = 28/100 =", 0.28 * 0.72 * 100, "\n")
