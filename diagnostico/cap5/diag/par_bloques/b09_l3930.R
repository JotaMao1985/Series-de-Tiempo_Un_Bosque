# Tienda inventada: nivel 100, una mas al mes y un patron anual de suma cero
t      <- 1:48
patron <- c(-6, -8, -4, -2, 0, 4, 6, 4, 0, -2, 2, 6)
mes    <- (t - 1) %% 12 + 1
y      <- ts(100 + (t - 1) + patron[mes], start = c(2022, 1), frequency = 12)
y                              # una serie mensual se imprime como cuadricula
#>      Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
#> 2022  94  93  98 101 104 109 112 111 108 107 112 117
#> 2023 106 105 110 113 116 121 124 123 120 119 124 129
#> 2024 118 117 122 125 128 133 136 135 132 131 136 141
#> 2025 130 129 134 137 140 145 148 147 144 143 148 153
diff(y, lag = 12)              # nabla_12: menos la celda de arriba
#>      Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
#> 2023  12  12  12  12  12  12  12  12  12  12  12  12
#> 2024  12  12  12  12  12  12  12  12  12  12  12  12
#> 2025  12  12  12  12  12  12  12  12  12  12  12  12
diff(y)                        # nabla: menos la celda de la izquierda
#>      Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
#> 2022      -1   5   3   3   5   3  -1  -3  -1   5   5
#> 2023 -11  -1   5   3   3   5   3  -1  -3  -1   5   5
#> 2024 -11  -1   5   3   3   5   3  -1  -3  -1   5   5
#> 2025 -11  -1   5   3   3   5   3  -1  -3  -1   5   5
diff(diff(y, lag = 12))        # las dos
#>      Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
#> 2023       0   0   0   0   0   0   0   0   0   0   0
#> 2024   0   0   0   0   0   0   0   0   0   0   0   0
#> 2025   0   0   0   0   0   0   0   0   0   0   0   0
max(abs(diff(diff(y, lag = 12)) - diff(diff(y), lag = 12)))   # orden: da igual
#> [1] 0

# Desde enero de 2024 la tienda crece tres unidades al mes
tend2 <- ifelse(t <= 24, t - 1, 23 + 3 * (t - 24))
y2    <- ts(100 + tend2 + patron[mes], start = c(2022, 1), frequency = 12)
diff(y2, lag = 12)
#>      Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
#> 2023  12  12  12  12  12  12  12  12  12  12  12  12
#> 2024  14  16  18  20  22  24  26  28  30  32  34  36
#> 2025  36  36  36  36  36  36  36  36  36  36  36  36
diff(diff(y2, lag = 12))
#>      Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
#> 2023       0   0   0   0   0   0   0   0   0   0   0
#> 2024   2   2   2   2   2   2   2   2   2   2   2   2
#> 2025   0   0   0   0   0   0   0   0   0   0   0   0