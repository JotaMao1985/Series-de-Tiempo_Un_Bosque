# R3 · Modulos 2 y 3: la banda y el correlograma, anunciados; diferenciar y raiz unitaria, definidos
# donde aparecen; el residuo del Capitulo 1, medido.
EDICIONES = [
# ---------------------------------------------------------------- M2
(
r"""aleatoriedad sin memoria. Es el ladrillo con el que se construyen todos los modelos del curso.</p>""",
r"""aleatoriedad sin memoria. Es el ladrillo con el que se construyen todos los modelos del curso; el primero aparece
        en el Módulo 5.</p>"""),
(
r"""      <div class="simulador" data-simulador="ruido-blanco">""",
r"""      <p>El simulador de abajo dibuja la serie y, debajo, un gráfico que el Módulo 3 define con calma: el
        <strong>correlograma</strong>. Por ahora basta con saber leerlo. Cada barra es una <strong>autocorrelación
          muestral</strong> $r_k$: mide, entre $-1$ y $1$, cuánto se parece la serie a ella misma $k$ instantes
        atrás. Las dos líneas horizontales son la <strong>banda</strong> dentro de la cual caen casi todas las barras
        cuando ese parecido no existe.</p>

      <div class="simulador" data-simulador="ruido-blanco">"""),
# ---------------------------------------------------------------- M3
(
r"""instantes. Es la traducción cuantitativa del gráfico de rezagos que vimos en el Módulo 3 del Capítulo 1.</p>""",
r"""instantes. Es la traducción cuantitativa del gráfico de rezagos del Módulo 3 del Capítulo 1, y es también el
        número que el Módulo 2 dibujó sin definirlo.</p>"""),
(
r"""      <div class="code-tabs">
        <div class="code-tabs-nav" role="tablist" aria-label="Calcular y graficar la ACF">""",
r"""      <p>Tres avisos sobre la tabla. <strong>Diferenciar</strong> es restar a cada valor el anterior: se pasa de la
        serie de los niveles a la de los cambios, $\nabla y_t = y_t - y_{t-1}$. Es el remedio de la segunda fila; el
        símbolo $\nabla$ reaparece en los módulos siguientes y el Módulo 7 lo desarrolla. La <strong>raíz
          unitaria</strong> es el nombre técnico de lo que le ocurre a la caminata aleatoria, y se define en el
        Módulo 5. Y las fórmulas de este módulo suponen una serie estacionaria: en una caminata o en
        <code>AirPassengers</code> no existe un $\rho_k$ que valga lo mismo en todo instante, así que sus $r_k$ no
        estiman ninguna cantidad fija. Su correlograma se lee como una huella: la que delata la no
        estacionariedad.</p>

      <h3>El residuo del Capítulo 1, ahora con número</h3>

      <p>El Capítulo 1 dejó un cabo suelto: el residuo de una descomposición se juzgaba a ojo. El correlograma lo
        mide. El residuo de la descomposición clásica multiplicativa de <code>AirPassengers</code> —132 valores,
        porque la media móvil deja sin estimar seis en cada extremo— tiene $r_1 = 0.403$ y $r_{12} = 0.294$, y
        <strong>14 de sus 24 barras</strong> salen de la banda $\pm 0.171$, cuando por azar se esperaría una o dos.
        No es ruido blanco: la descomposición separó la tendencia y la estacionalidad, pero en lo que sobra queda
        dependencia entre un mes y los siguientes. Describir esa dependencia es el trabajo de los modelos del
        Capítulo 3, que además cambia el recuento de barras por una prueba formal, la de Ljung–Box, que las resume
        todas en un solo p-valor.</p>

      <div class="code-tabs">
        <div class="code-tabs-nav" role="tablist" aria-label="Calcular y graficar la ACF">"""),
(
r"""which(abs(rc) > 1.96 / sqrt(200))     # los unicos rezagos fuera de la banda
#> [1] 1 2
""",
r"""which(abs(rc) > 1.96 / sqrt(200))     # los unicos rezagos fuera de la banda
#> [1] 1 2

# El residuo de la descomposicion clasica multiplicativa del Capitulo 1. La
# media movil deja 6 valores sin estimar en cada extremo: quedan 132
residuo &lt;- na.omit(decompose(AirPassengers, type = "multiplicative")$random)
rr &lt;- acf(residuo, lag.max = 24, plot = FALSE)$acf[-1]
c(n = length(residuo), banda = round(1.96 / sqrt(length(residuo)), 3))
round(rr[c(1, 12)], 3)
sum(abs(rr) > 1.96 / sqrt(length(residuo)))     # de 24 rezagos
"""),
(
r"""r = acf(pasajeros, nlags=24, adjusted=False)[1:]
print(np.round(r[[0, 1, 11]], 4))
#> [0.948  0.8756 0.7604]</code></pre>""",
r"""r = acf(pasajeros, nlags=24, adjusted=False)[1:]
print(np.round(r[[0, 1, 11]], 4))
#> [0.948  0.8756 0.7604]

# El residuo de la descomposicion clasica multiplicativa del Capitulo 1
from statsmodels.tsa.seasonal import seasonal_decompose
residuo = seasonal_decompose(pasajeros, model="multiplicative", period=12).resid.dropna()
rr = acf(residuo, nlags=24, adjusted=False)[1:]
print(len(residuo), np.round(rr[[0, 11]], 3))
print(int(np.sum(np.abs(rr) > 1.96 / np.sqrt(len(residuo)))))   # de 24 rezagos</code></pre>"""),
]
