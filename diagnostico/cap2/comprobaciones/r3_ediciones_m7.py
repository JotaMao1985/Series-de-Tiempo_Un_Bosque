# R3 · Modulo 7: la regla del orden, escrita una vez (D5); el caso en que el orden cambia la cuenta
# (log(UKgas)); MA(1), theta e invertibilidad como adelanto del Capitulo 3; d y D definidos.
EDICIONES = [
# retoque de una frase del M6 (la escala logaritmica)
(
r"""con el nivel (Capítulo 1; el Módulo 8 lo retoma), y es la escala en que se trabaja desde aquí hasta el final
        del capítulo. En logaritmos""",
r"""con el nivel (Capítulo 1; el Módulo 8 lo retoma), y es la escala en que esta serie se diferencia en los módulos
        que siguen. En logaritmos"""),
(
r"""      <p>La <strong>diferenciación</strong> es la herramienta estándar para eliminar una raíz unitaria: en vez de
        modelar el nivel de la serie, modelamos sus <em>cambios</em>.</p>""",
r"""      <p>La <strong>diferenciación</strong> es la herramienta estándar para eliminar una raíz unitaria: en vez de
        modelar el nivel de la serie, se modelan sus <em>cambios</em>. El Módulo 3 la presentó como una resta; aquí
        recibe su notación, se cuenta lo que cuesta y se fija en qué orden se aplica.</p>"""),
(
r"""        <p>La <strong>diferencia estacional</strong> de periodo $m$ compara cada observación con la del mismo periodo
          del ciclo anterior:</p>
        $$\nabla_m y_t = y_t - y_{t-m} = (1 - B^m)\, y_t$$
        <p style="margin-bottom:0;">Diferenciar $d$ veces se escribe $(1-B)^d y_t$. Cada diferencia cuesta
          observaciones: $\nabla$ deja $T-1$ datos, $\nabla_{12}$ deja $T-12$.</p>
      </div>

      <div class="warning">
        <p><strong>El orden no da lo mismo en la práctica.</strong> Aunque $\nabla\nabla_{12} y_t = \nabla_{12}\nabla
          y_t$ algebraicamente, la recomendación de FPP3 es aplicar <strong>primero la diferencia estacional</strong>:
          a veces con ella basta y la serie ya queda estacionaria, ahorrándose una diferencia regular que solo añadiría
          ruido.</p>
      </div>
""",
r"""        <p>La <strong>diferencia estacional</strong> de periodo $m$ compara cada observación con la de la misma
          estación del año anterior —el mismo mes, si $m = 12$—:</p>
        $$\nabla_m y_t = y_t - y_{t-m} = (1 - B^m)\, y_t$$
        <p style="margin-bottom:0;">Diferenciar $d$ veces se escribe $(1-B)^d y_t$. En todo el curso, $d$ es el
          número de diferencias regulares que se aplican a una serie y $D$, el de diferencias estacionales. Cada
          diferencia cuesta observaciones: $\nabla$ deja $T-1$ datos, $\nabla_{12}$ deja $T-12$.</p>
      </div>

      <div class="definition">
        <h4><i class="fas fa-list-ol mr-2" aria-hidden="true"></i>Regla del orden: la diferencia estacional,
          primero</h4>
        <p>Con una serie estacional, este curso aplica siempre el mismo orden:</p>
        <ol>
          <li>si la dispersión crece con el nivel, se transforma la serie (el logaritmo, Módulo 8);</li>
          <li>se decide la diferencia estacional con <code>nsdiffs()</code> y, si la pide, se aplica $\nabla_m$;</li>
          <li>se decide la diferencia regular con <code>ndiffs()</code> <strong>sobre la serie que dejó el paso
              anterior</strong> y, si la pide, se aplica $\nabla$;</li>
          <li>se comprueba el resultado con el correlograma y las pruebas.</li>
        </ol>
        <p><code>nsdiffs()</code> y <code>ndiffs()</code> son funciones del paquete <code>forecast</code> de R.
          La segunda repite el KPSS del Módulo 6 —diferenciar, volver a probar— hasta que deja de rechazar, y
          devuelve cuántas diferencias hicieron falta; la primera mide la fuerza de la estacionalidad, el $F_S$ del
          Capítulo 1, y pide una diferencia estacional si pasa de 0.64. Cada una decide una sola clase de
          diferencia: el orden lo pone quien las usa.</p>
        <p style="margin-bottom:0;">El orden no cambia la serie a la que se llega si se aplican las dos diferencias
          —$\nabla\nabla_{12} y_t = \nabla_{12}\nabla y_t$, algebraicamente—, pero sí lo que se decide por el camino,
          por dos razones. La primera es que la diferencia estacional ya lleva dentro una regular:
          $1 - B^m = (1-B)(1 + B + \cdots + B^{m-1})$. Por eso, como recomienda FPP3, conviene aplicar primero la
          estacional: a veces con ella basta y la serie ya queda estacionaria, y se ahorra una diferencia regular
          que solo añadiría ruido. La segunda es la del Módulo 6: las pruebas de raíz unitaria regular no son
          fiables sobre una serie que todavía es estacional. La sección «El orden, en dos series», más abajo,
          muestra las dos.</p>
      </div>
"""),
(
r"""      <p>Conviene detenerse en esa última frase, porque el costo no es un detalle contable. Una diferencia no""",
r"""      <p>Conviene detenerse en la última frase de la definición —cada diferencia cuesta observaciones—, porque ese
        costo no es un detalle contable. Una diferencia no"""),
(
r"""sobre lo que queda. Ese es el argumento cuantitativo detrás de la advertencia anterior, y también el motivo
          por el que sobrediferenciar no solo añade ruido: además achica la evidencia con la que se decide.</p>""",
r"""sobre lo que queda. Ese es el argumento cuantitativo detrás de la regla del orden —una diferencia que se ahorra
          son datos que se conservan—, y también el motivo por el que sobrediferenciar no solo añade ruido: además
          achica la evidencia con la que se decide.</p>"""),
(
r"""        <p>La razón es algebraica. Si $y_t$ ya es ruido blanco y se diferencia, se obtiene
          $\nabla y_t = \varepsilon_t - \varepsilon_{t-1}$, que es un MA(1) —con la convención
          $y_t = \varepsilon_t + \theta\varepsilon_{t-1}$, $\theta = -1$; con la convención del signo contrario,
          $\theta = 1$— cuya autocorrelación teórica en el rezago 1 vale $-0.5$. Es decir: se
          <strong>fabrica</strong> un modelo MA donde no había nada. Y ese MA es <em>no invertible</em>, lo que le
          da problemas al estimador. En la duda, conviene diferenciar de menos.</p>""",
r"""        <p>La razón es algebraica. Si $y_t$ ya es ruido blanco y se diferencia, se obtiene
          $\nabla y_t = \varepsilon_t - \varepsilon_{t-1}$: cada valor mezcla el ruido de hoy con el de ayer, y dos
          valores seguidos comparten un $\varepsilon$ con el signo cambiado. Su covarianza es $-\sigma^2$ y su
          varianza, $2\sigma^2$: de ahí el $-0.5$. Es decir: se <strong>fabrica</strong> dependencia donde no había
          nada.</p>
        <p><strong>Adelanto del Capítulo 3.</strong> Esa serie fabricada tiene nombre: es un proceso de media
          móvil de orden 1, o MA(1), que el Capítulo 3 escribe $y_t = \varepsilon_t + \theta\varepsilon_{t-1}$
          —aquí, $\theta = -1$; con la convención del signo contrario, $\theta = 1$—. Con ese valor de $\theta$ el
          MA(1) es <em>no invertible</em>, una propiedad que también se define allí y que le da problemas al
          estimador. En la duda, conviene diferenciar de menos.</p>"""),
(
r"""      <h3>Diferenciación estacional en la práctica</h3>

      <p>Sobre <code>log(AirPassengers)</code> el diagnóstico secuencial es instructivo. Con la diferencia estacional
        primero, <code>nsdiffs()</code> pide 1; sobre $\nabla_{12}\log y_t$, <code>ndiffs()</code> pide 1 más, y así se
        llega a $\nabla\nabla_{12}\log y_t$, con <code>ndiffs = 0</code> y <code>nsdiffs = 0</code>: la serie del
        modelo <em>airline</em> que ajustaremos en el Capítulo 5.</p>

      <p>El orden contrario enseña por qué no basta con las pruebas. Tras <strong>una diferencia regular</strong>, el
        KPSS de nivel ya no rechaza la estacionariedad ($p &gt; 0.10$) y <code>ndiffs()</code> devuelve 0 — pero la ACF
        todavía tiene un pico enorme en el rezago 12 ($r_{12} = 0.841$) y <code>nsdiffs()</code> sigue pidiendo 1. Las
        pruebas de raíz unitaria regular <strong>no ven la estacionalidad</strong>; hay que mirar el correlograma.</p>
""",
r"""      <h3>El orden, en dos series</h3>

      <p>Sobre <code>log(AirPassengers)</code>, con la regla: <code>nsdiffs()</code> pide 1; sobre
        $\nabla_{12}\log y_t$, <code>ndiffs()</code> pide 1 más, y así se llega a $\nabla\nabla_{12}\log y_t$, donde
        las dos funciones devuelven 0. Son $D = 1$ y $d = 1$: la serie del modelo <em>airline</em> que se ajusta en
        el Capítulo 5, y una de las que ofrece el explorador del Módulo 4.</p>

      <p>En el orden contrario aquí se llega al mismo sitio, pero el camino enseña por qué no basta con las pruebas.
        Tras <strong>una diferencia regular</strong>, el KPSS de nivel ya no rechaza la estacionariedad
        ($p &gt; 0.10$) y <code>ndiffs()</code> devuelve 0 — pero la ACF todavía tiene un pico enorme en el rezago 12
        ($r_{12} = 0.841$) y <code>nsdiffs()</code> sigue pidiendo 1. Las pruebas de raíz unitaria regular
        <strong>no ven la estacionalidad</strong>; hay que mirar el correlograma.</p>

      <p>En otras series el orden sí cambia la cuenta. <code>UKgas</code>, que viene con R, es el consumo trimestral
        de gas del Reino Unido de 1960 a 1986: 108 trimestres, con $m = 4$. Se toma en logaritmos, porque su amplitud
        crece con el nivel:</p>

      <table>
        <caption class="sr-only">Las diferencias que se aplican a log(UKgas) según el orden en que se decidan</caption>
        <thead>
          <tr>
            <th scope="col"><code>log(UKgas)</code></th>
            <th scope="col">Estacional primero (la regla)</th>
            <th scope="col">Regular primero</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Primera decisión</td>
            <td><code>nsdiffs()</code> pide 1: se aplica $\nabla_4$</td>
            <td><code>ndiffs()</code> pide 1: se aplica $\nabla$</td>
          </tr>
          <tr>
            <td>Segunda decisión</td>
            <td><code>ndiffs()</code> devuelve 0: no hace falta más</td>
            <td><code>nsdiffs()</code> pide 1: se aplica $\nabla_4$</td>
          </tr>
          <tr>
            <td>Diferencias aplicadas</td>
            <td>$D = 1$, $d = 0$</td>
            <td>$D = 1$, $d = 1$</td>
          </tr>
          <tr>
            <td>Observaciones que quedan</td>
            <td>104</td>
            <td>103</td>
          </tr>
          <tr>
            <td>$r_1$ de la serie final</td>
            <td>−0.178</td>
            <td>−0.576</td>
          </tr>
        </tbody>
      </table>

      <p>Con la regla basta una diferencia: $\nabla_4$ ya lleva dentro la regular que hacía falta. Preguntando
        primero por la regular se aplican las dos, y la que sobra deja su rastro: $r_1 = -0.576$, el indicio de
        sobrediferenciación del recuadro anterior.</p>
"""),
(
r"""#> KPSS Level = 0.36816, Truncation lag parameter = 4, p-value = 0.09088
""",
r"""#> KPSS Level = 0.36816, Truncation lag parameter = 4, p-value = 0.09088

# El orden, en otra serie: log(UKgas), trimestral (m = 4)
g &lt;- log(UKgas)
nsdiffs(g); ndiffs(diff(g, lag = 4))        # con la regla: D = 1 y d = 0
ndiffs(g); nsdiffs(diff(g))                 # regular primero: d = 1 y D = 1
gs  &lt;- diff(g, lag = 4)                     # lo que deja la regla
gsd &lt;- diff(diff(g), lag = 4)               # lo que deja el orden contrario
c(length(gs), length(gsd))
round(c(acf(gs, lag.max = 1, plot = FALSE)$acf[2],
        acf(gsd, lag.max = 1, plot = FALSE)$acf[2]), 3)
"""),
(
r"""# (b) Serie con raiz unitaria cuyos cambios se compensan en parte (theta = -0.8):""",
r"""# (b) Serie con raiz unitaria cuyos cambios se compensan en parte. Es un
#     ARIMA(0,1,1) con theta = -0.8, un modelo que presenta el Capitulo 4:"""),
(
r"""#   nsdiffs(lap, m=12, test="ocsb") -> 1
""",
r"""#   nsdiffs(lap, m=12, test="ocsb") -> 1
# El orden se pone a mano, como en R: primero la estacional (Modulo 9).
"""),
(
r"""#> 3 0.04691 -0.5335</code></pre>
        </div>
      </div>
""",
r"""#> 3 0.04691 -0.5335</code></pre>
        </div>
      </div>

      <p>Queda una pieza. La diferenciación corrige una media que cambia; una dispersión que crece con el nivel no la
        corrige ninguna diferencia, y es el asunto del Módulo 8.</p>
"""),
]
