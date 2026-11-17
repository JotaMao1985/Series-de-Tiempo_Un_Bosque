# R3 · Modulos 4 y 5: el objetivo del M4 y su primer caso; las series del explorador, presentadas
# (TRM, nabla, nabla_12, logaritmo, ndiffs); puentes M3 -> M4 -> M5 -> M6; la promesa del M5.
EDICIONES = [
# ---------------------------------------------------------------- M4
(
r"""            <p class="text-gray-600 text-sm" style="margin:0;">Entender qué mide la PACF y en qué se diferencia de la
              ACF, y usar las dos juntas como instrumento de identificación.</p>""",
r"""            <p class="text-gray-600 text-sm" style="margin:0;">Entender qué mide la PACF y en qué se diferencia de la
              ACF, y leer las dos juntas en un primer caso: es el instrumento de identificación que desarrolla el
              Capítulo 3.</p>"""),
(
r"""      <p>La ACF tiene un problema de <em>doble conteo</em>. Supongamos que hoy depende de ayer, y ayer de anteayer.
        Entonces hoy y anteayer aparecerán correlacionados""",
r"""      <p>El correlograma del Módulo 3 tiene un punto ciego: la ACF hace un <em>doble conteo</em>. Si hoy depende de
        ayer, y ayer de anteayer, hoy y anteayer aparecerán correlacionados"""),
(
r"""        <p>La <strong>autocorrelación parcial</strong> en el rezago $k$, que denotamos $\phi_{kk}$, es la correlación""",
r"""        <p>La <strong>autocorrelación parcial</strong> en el rezago $k$, que se denota $\phi_{kk}$, es la correlación"""),
(
r"""                  explican</strong> los rezagos anteriores. Justamente la parte "parcial" que buscábamos.</p>""",
r"""                  explican</strong> los rezagos anteriores. Justamente la parte "parcial" que se buscaba.</p>"""),
# La nota «Verificación» (cómo se construyó la página) sale del cuerpo y entra en el desarrollo plegado.
(
r"""            rezago. Todos coinciden hasta el redondeo con que se guardó el precálculo.</p>
        </div>
      </div>

      <div class="note">
        <p><strong>Verificación.</strong> El correlograma de abajo no lo calcula el navegador: se obtuvo en R con
          <code>stats::pacf()</code> y se incrustó ya resuelto en esta página. La misma recursión implementada en
          JavaScript, aplicada a las series crudas del precálculo, reproduce esos valores con una diferencia máxima de
          $6.2 \times 10^{-5}$: el orden del redondeo con el que se guardó el JSON. R, Python
          (<code>statsmodels</code>, método <code>ywm</code>) y el navegador coinciden.</p>
      </div>
""",
r"""            rezago. Todos coinciden hasta el redondeo con que se guardó el precálculo.</p>
          <p style="margin-bottom:0;"><strong>Verificación.</strong> El correlograma del explorador no lo calcula el
            navegador: se obtuvo en R con <code>stats::pacf()</code> y se incrustó ya resuelto en esta página. La
            misma recursión implementada en JavaScript, aplicada a las series crudas del precálculo, reproduce esos
            valores con una diferencia máxima de $6.2 \times 10^{-5}$: el orden del redondeo con el que se guardó el
            JSON. R, Python (<code>statsmodels</code>, método <code>ywm</code>) y el navegador coinciden.</p>
        </div>
      </div>

      <p>El explorador de abajo ofrece ocho series, y varias se adelantan a su módulo. La <strong>TRM</strong> es la
        Tasa Representativa del Mercado: la tasa de cambio del peso colombiano frente al dólar, en pesos por dólar.
        Aquí es su promedio mensual de enero de 2015 a junio de 2026, 138 meses, calculado con la serie diaria que
        publica datos.gov.co; es la segunda serie real del capítulo y vuelve en los Módulos 6 y 7. Un $\nabla$
        delante de un nombre indica la serie diferenciada (Módulo 3), y $\nabla_{12}$, la diferencia con el mismo mes
        del año anterior, $y_t - y_{t-12}$, que presenta el Módulo 7. El <strong>logaritmo</strong> de
        <code>AirPassengers</code> es la transformación con la que el Capítulo 1 cerró el abanico de una serie cuya
        amplitud crece con el nivel; el Módulo 8 la retoma. Y <code>ndiffs</code> y <code>nsdiffs</code>, al final de
        la lectura numérica, son dos funciones de R que dicen cuántas diferencias regulares y estacionales pide la
        serie (Módulo 7).</p>
"""),
(
r"""        cuenta la historia acumulada; la PACF, la conexión directa.</p>
""",
r"""        cuenta la historia acumulada; la PACF, la conexión directa.</p>

      <p>En <code>AirPassengers</code>, la serie con la que abre el explorador, la PACF tiene seis barras fuera de la
        banda, pero todavía no hay nada que identificar en ellas: mezclan la tendencia con la estacionalidad. Antes de
        leer un modelo en una PACF hay que volver estacionaria la serie, y de eso se ocupa el resto del capítulo.</p>
"""),
(
r"""          modelos ARMA. La regla, que desarrollaremos en detalle, es:</p>""",
r"""          modelos ARMA. La regla, que allí se desarrolla en detalle, es:</p>"""),
(
r"""            cuánto valen $p$ y $q$.</li>
        </ul>
      </div>
""",
r"""            cuánto valen $p$ y $q$.</li>
        </ul>
      </div>

      <p>La primera línea de la regla ya se puede ver en un caso. La serie de memoria corta del Módulo 3 —cada valor,
        la mitad del anterior más un ruido nuevo— tiene una ACF que decae ($0.474$, $0.235$, $0.106$) y una PACF que
        se corta tras el rezago 1: $0.474$ y, enseguida, $0.014$, $-0.014$ y $0.033$. De sus 24 autocorrelaciones
        parciales solo otra, la del rezago 9, asoma fuera de la banda, que es lo que se espera por azar. Es la huella
        de un AR(1), el proceso que presenta el Módulo 5; el código de abajo la calcula.</p>
"""),
(
r"""round(p[1:3], 4)
#> [1]  0.9480 -0.2294  0.0381
""",
r"""round(p[1:3], 4)
#> [1]  0.9480 -0.2294  0.0381

# Un caso en que la PACF se corta: la serie de memoria corta del Modulo 3
set.seed(1)
corta &lt;- arima.sim(list(ar = 0.5), n = 200)
pc &lt;- pacf(corta, lag.max = 24, plot = FALSE)$acf
round(pc[1:4], 3)
which(abs(pc) > 1.96 / sqrt(200))     # el rezago 9 asoma por azar
"""),
(
r"""azar. No construyas un modelo AR(17) porque el rezago 17 se asomó.</p>""",
r"""azar. Un rezago 17 que se asoma no justifica un modelo AR(17).</p>"""),
# ---------------------------------------------------------------- M5
(
r"""      <p>Casi toda la no estacionariedad interesante cabe en una sola ecuación. Consideremos el proceso autorregresivo
        de primer orden:</p>""",
r"""      <p>Los módulos anteriores enseñaron a leer la dependencia; falta un proceso que la produzca. El más simple
        basta para separar lo estacionario de lo que no lo es, porque casi toda la no estacionariedad interesante cabe
        en una sola ecuación. Es el proceso autorregresivo de primer orden, o <strong>AR(1)</strong>, en el que cada
        valor es una fracción $\phi$ del anterior más un ruido blanco nuevo:</p>"""),
(
r"""equivale a que esa raíz esté <strong>fuera</strong> del círculo unitario; con $\phi = 1$ la raíz vale
          exactamente 1.</p>""",
r"""equivale a que esa raíz esté <strong>fuera</strong> del círculo unitario; con $\phi = 1$ la raíz vale
          exactamente 1. El Capítulo 3 vuelve con calma sobre el operador $B$ y sobre esa condición.</p>"""),
(
r"""recta, y esa es la huella de la raíz unitaria. Luego activa la primera diferencia y comprueba qué pasa.</p>""",
r"""recta, y esa es la huella de la raíz unitaria. Luego activa la <strong>primera diferencia</strong> —la serie
          $\nabla y_t = y_t - y_{t-1}$ del Módulo 3— y comprueba qué pasa.</p>"""),
(
r"""      <p>Si añadimos una constante obtenemos la <strong>caminata aleatoria con deriva</strong> (<em>random walk with
          drift</em>):</p>""",
r"""      <p>Al añadir una constante se obtiene la <strong>caminata aleatoria con deriva</strong> (<em>random walk with
          drift</em>):</p>"""),
(
r"""que describe el Módulo 7—. Distinguirlas es justamente el trabajo de las pruebas del Módulo 6.</p>""",
r"""que describe el Módulo 7—. A ojo no se distinguen; las pruebas del Módulo 6 lo hacen con un número, y allí se
          aplican a un caso de cada clase.</p>"""),
(
r"""deriva = np.cumsum(0.3 + e)   # caminata con deriva</code></pre>
        </div>
      </div>
""",
r"""deriva = np.cumsum(0.3 + e)   # caminata con deriva</code></pre>
        </div>
      </div>

      <p>Con $\phi = 0.95$ y con $\phi = 1$ las series se parecen, y sus correlogramas también: a ojo la decisión es
        frágil. El Módulo 6 le pone un número.</p>
"""),
]
