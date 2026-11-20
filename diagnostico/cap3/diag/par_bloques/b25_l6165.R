for (v in list(c(1770,1869), c(1700,1988), c(1870,1988), c(1900,1988))) {
  x <- sqrt(window(sunspot.year, v[1], v[2]))
  f <- arima(x, order = c(2, 0, 0), method = "ML")
  r <- polyroot(c(1, -coef(f)[1:2]))
  cat(sprintf("%d-%d (n=%3d): phi=(%.4f, %.4f)  |raiz|=%.4f  periodo=%6.3f  LB12 p=%.4f\n",
      v[1], v[2], length(x), coef(f)[1], coef(f)[2], Mod(r)[1],
      2*pi/Arg(r[1]),
      Box.test(residuals(f), lag = 12, type = "Ljung-Box", fitdf = 2)$p.value))
}
#> 1770-1869 (n=100): phi=(1.4027, -0.6853)  |raiz|=1.2080  periodo=11.218  LB12 p=0.1644
#> 1700-1988 (n=289): phi=(1.4086, -0.7006)  |raiz|=1.1947  periodo=11.007  LB12 p=0.0000
#> 1870-1988 (n=119): phi=(1.4219, -0.7321)  |raiz|=1.1687  periodo=10.648  LB12 p=0.0007
#> 1900-1988 (n= 89): phi=(1.4146, -0.7556)  |raiz|=1.1504  periodo=10.129  LB12 p=0.0010