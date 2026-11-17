# R3 · las salidas bajo `#>` del codigo nuevo o cambiado, copiadas de la ejecucion
# (r3_bloques_publicados.out, que es la salida integra de cada bloque).
EDICIONES = [
# M3 (R)
(
r"""c(n = length(residuo), banda = round(1.96 / sqrt(length(residuo)), 3))
round(rr[c(1, 12)], 3)
sum(abs(rr) > 1.96 / sqrt(length(residuo)))     # de 24 rezagos
""",
r"""c(n = length(residuo), banda = round(1.96 / sqrt(length(residuo)), 3))
#>       n   banda 
#> 132.000   0.171 
round(rr[c(1, 12)], 3)
#> [1] 0.403 0.294
sum(abs(rr) > 1.96 / sqrt(length(residuo)))     # de 24 rezagos
#> [1] 14
"""),
# M3 (Python)
(
r"""print(len(residuo), np.round(rr[[0, 11]], 3))
print(int(np.sum(np.abs(rr) > 1.96 / np.sqrt(len(residuo)))))   # de 24 rezagos</code></pre>""",
r"""print(len(residuo), np.round(rr[[0, 11]], 3))
#> 132 [0.403 0.294]
print(int(np.sum(np.abs(rr) > 1.96 / np.sqrt(len(residuo)))))   # de 24 rezagos
#> 14</code></pre>"""),
# M4 (R)
(
r"""round(pc[1:4], 3)
which(abs(pc) > 1.96 / sqrt(200))     # el rezago 9 asoma por azar
""",
r"""round(pc[1:4], 3)
#> [1]  0.474  0.014 -0.014  0.033
which(abs(pc) > 1.96 / sqrt(200))     # el rezago 9 asoma por azar
#> [1] 1 9
"""),
# M6 (R)
(
r"""adf.test(recta)                       # rechaza la raiz unitaria
kpss.test(recta, null = "Trend")      # no rechaza: estacionaria en tendencia
""",
r"""adf.test(recta)                       # rechaza la raiz unitaria
#> Dickey-Fuller = -5.7441, Lag order = 5, p-value = 0.01
#> Warning: p-value smaller than printed p-value
kpss.test(recta, null = "Trend")      # no rechaza: estacionaria en tendencia
#> KPSS Trend = 0.051544, Truncation lag parameter = 4, p-value = 0.1
#> Warning: p-value greater than printed p-value
"""),
(
r"""kpss.test(AirPassengers)              # rechaza la estacionariedad: se contradicen
kpss.test(AirPassengers, null = "Trend")   # no rechaza: coinciden, y las dos fallan
""",
r"""kpss.test(AirPassengers)              # rechaza la estacionariedad: se contradicen
#> KPSS Level = 2.7395, Truncation lag parameter = 4, p-value = 0.01
#> Warning: p-value smaller than printed p-value
kpss.test(AirPassengers, null = "Trend")   # no rechaza: coinciden, y las dos fallan
#> KPSS Trend = 0.09615, Truncation lag parameter = 4, p-value = 0.1
#> Warning: p-value greater than printed p-value
"""),
# M7 (R)
(
r"""nsdiffs(g); ndiffs(diff(g, lag = 4))        # con la regla: D = 1 y d = 0
ndiffs(g); nsdiffs(diff(g))                 # regular primero: d = 1 y D = 1
gs  &lt;- diff(g, lag = 4)                     # lo que deja la regla
gsd &lt;- diff(diff(g), lag = 4)               # lo que deja el orden contrario
c(length(gs), length(gsd))
round(c(acf(gs, lag.max = 1, plot = FALSE)$acf[2],
        acf(gsd, lag.max = 1, plot = FALSE)$acf[2]), 3)
""",
r"""nsdiffs(g); ndiffs(diff(g, lag = 4))        # con la regla: D = 1 y d = 0
#> [1] 1
#> [1] 0
ndiffs(g); nsdiffs(diff(g))                 # regular primero: d = 1 y D = 1
#> [1] 1
#> [1] 1
gs  &lt;- diff(g, lag = 4)                     # lo que deja la regla
gsd &lt;- diff(diff(g), lag = 4)               # lo que deja el orden contrario
c(length(gs), length(gsd))
#> [1] 104 103
round(c(acf(gs, lag.max = 1, plot = FALSE)$acf[2],
        acf(gsd, lag.max = 1, plot = FALSE)$acf[2]), 3)
#> [1] -0.178 -0.576
"""),
# M9 (R)
(
r"""res$d; res$D                 # el modelo airline
# El p-valor del KPSS es el tope de la tabla (sin suppressWarnings() saldria
# el aviso "greater than printed p-value"): ya no se rechaza la estacionariedad
res$kpss_p
length(res$serie)            # 144 - 12 - 1: cada diferencia cuesta datos
""",
r"""res$d; res$D                 # el modelo airline
#> [1] 1
#> [1] 1
# El p-valor del KPSS es el tope de la tabla (sin suppressWarnings() saldria
# el aviso "greater than printed p-value"): ya no se rechaza la estacionariedad
res$kpss_p
#> [1] 0.1
length(res$serie)            # 144 - 12 - 1: cada diferencia cuesta datos
#> [1] 131
"""),
(
r"""round(BoxCox.lambda(AirPassengers, method = "guerrero"), 4)

# Lo que queda""",
r"""round(BoxCox.lambda(AirPassengers, method = "guerrero"), 4)
#> [1] -0.2947

# Lo que queda"""),
(
r"""round(r[c(1, 12)], 3)                                # r1 y r12
sum(abs(r) > 1.96 / sqrt(length(res$serie)))         # de 24 rezagos</code></pre>""",
r"""round(r[c(1, 12)], 3)                                # r1 y r12
#> [1] -0.341 -0.387
sum(abs(r) > 1.96 / sqrt(length(res$serie)))         # de 24 rezagos
#> [1] 5</code></pre>"""),
# M9 (Python)
(
r"""print(res["d"], res["D"], round(res["kpss_p"], 3), len(res["serie"]))
""",
r"""print(res["d"], res["D"], round(res["kpss_p"], 3), len(res["serie"]))
#> 1 1 0.1 131
"""),
(
r"""print(np.round(r[[0, 11]], 3))
print(int(np.sum(np.abs(r) > 1.96 / np.sqrt(len(res["serie"])))))   # de 24 rezagos</code></pre>""",
r"""print(np.round(r[[0, 11]], 3))
#> [-0.341 -0.387]
print(int(np.sum(np.abs(r) > 1.96 / np.sqrt(len(res["serie"])))))   # de 24 rezagos
#> 5</code></pre>"""),
]
