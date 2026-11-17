# R3 · Modulo 6: gamma y k con un solo sentido; la TRM remitida a su presentacion; la distincion
# determinista/estocastica que prometio el M5; el caso tramposo dice sobre que serie se calcula cada
# cifra y es el caso de la cuarta fila (las dos rechazan); la regla de trabajo cita la del M7.
EDICIONES = [
(
r"""        <p style="margin-bottom:0;">y se contrasta $H_0: \gamma = 0$ (equivalente a $\phi = 1$: <strong>hay raíz
            unitaria</strong>) contra $H_1: \gamma &lt; 0$ (estacionaria alrededor de la tendencia $\alpha + \beta t$ que
          la propia regresión incluye; sin el término $\beta t$, estacionaria en nivel). Los términos
          $\nabla y_{t-i}$ son la parte "aumentada": absorben la autocorrelación que quede en los errores. Un
          <strong>p-valor pequeño rechaza la raíz unitaria</strong>, es decir, favorece la estacionariedad.
          <code>adf.test()</code> de R estima siempre la regresión completa, con constante y tendencia.</p>""",
r"""        <p>y se contrasta $H_0: \gamma = 0$ (equivalente a $\phi = 1$: <strong>hay raíz
            unitaria</strong>) contra $H_1: \gamma &lt; 0$ (estacionaria alrededor de la tendencia $\alpha + \beta t$ que
          la propia regresión incluye, o <em>estacionaria en tendencia</em>; sin el término $\beta t$, estacionaria
          en nivel). Un <strong>p-valor pequeño rechaza la raíz unitaria</strong>, es decir, favorece la
          estacionariedad. <code>adf.test()</code> de R estima siempre la regresión completa, con constante y
          tendencia.</p>
        <p style="margin-bottom:0;">Dos letras cambian aquí de oficio. $\nabla y_t = y_t - y_{t-1}$ es la primera
          diferencia del Módulo 3, y $\gamma$ no es la autocovarianza $\gamma_k$ de los Módulos 1 y 3, sino el
          coeficiente de $y_{t-1}$: al restar $y_{t-1}$ en los dos lados del proceso del Módulo 5 queda
          $\nabla y_t = (\phi - 1)\,y_{t-1} + \varepsilon_t$, de modo que $\gamma = \phi - 1$. Los $k$ términos
          $\nabla y_{t-i}$ son la parte "aumentada": absorben la autocorrelación que quede en los errores. Esa $k$
          es el número de términos —el argumento <code>k</code> de <code>adf.test()</code>—, no el rezago de un
          correlograma, y en todo este módulo significa eso.</p>"""),
(
r"""            <td>Contradicción: revisa la especificación (tendencia, rezagos, estacionalidad).</td>""",
r"""            <td>Las dos rechazan: se contradicen. Hay que revisar la especificación (tendencia, rezagos,
              estacionalidad), como en el caso tramposo de más abajo.</td>"""),
(
r"""      <p>Apliquemos las dos pruebas a la Tasa Representativa del Mercado (COP/USD), promedio mensual de enero de 2015 a
        junio de 2026 ($T = 138$), y a su primera diferencia:</p>""",
r"""      <p>Las dos pruebas, aplicadas a la TRM —la tasa de cambio que presentó el Módulo 4: pesos por dólar, promedio
        mensual de enero de 2015 a junio de 2026, $T = 138$— y a su primera diferencia:</p>"""),
(
r"""el KPSS rechaza la estacionariedad) y basta <strong>una</strong> diferencia para arreglarla. Esto es lo que uno
        espera ver en un caso bien portado.</p>""",
r"""el KPSS rechaza la estacionariedad) y basta <strong>una</strong> diferencia para arreglarla. Es lo que se espera
        ver en un caso bien portado.</p>"""),
(
r"""        tampoco la rechaza en su diferencia (0.070, $p &gt; 0.10$).</p>
""",
r"""        tampoco la rechaza en su diferencia (0.070, $p &gt; 0.10$).</p>

      <p>Con las dos pruebas en su variante de tendencia se resuelve la distinción que el Módulo 5 dejó pendiente. En
        el ADF la hipótesis nula es la tendencia estocástica y la alternativa, la determinista; en el KPSS de
        tendencia, al revés. En la TRM el ADF no rechaza y el KPSS rechaza: su tendencia es estocástica y se corrige
        diferenciando. En una recta con ruido de la misma longitud, simulada en el código de más abajo, ocurre lo
        contrario: el ADF rechaza la raíz unitaria ($-5.744$, $p &lt; 0.01$) y el KPSS de tendencia no rechaza (0.052,
        $p &gt; 0.10$). Su tendencia es determinista y se corrige restando la recta.</p>
"""),
(
r"""interpolan en tablas publicadas y avisan cuando el valor cae fuera del rango tabulado. Por eso escribimos
          "&lt; 0.01" y "&gt; 0.10" en lugar de un número""",
r"""interpolan en tablas publicadas y avisan cuando el valor cae fuera del rango tabulado. Por eso aquí se escribe
          "&lt; 0.01" y "&gt; 0.10" en lugar de un número"""),
(
r"""      <p>Ahora el mismo procedimiento sobre <code>AirPassengers</code>, una serie con tendencia y estacionalidad
        evidentes. El ADF devuelve un estadístico de <strong>−7.32 con p &lt; 0.01</strong>: rechaza rotundamente la
        raíz unitaria y proclama que la serie es estacionaria alrededor de una tendencia.</p>
""",
r"""      <p>El mismo procedimiento, ahora sobre <code>AirPassengers</code> sin transformar, una serie con tendencia y
        estacionalidad evidentes. El ADF devuelve un estadístico de <strong>−7.32 con p &lt; 0.01</strong>: rechaza
        rotundamente la raíz unitaria y proclama que la serie es estacionaria alrededor de una tendencia. El KPSS de
        nivel rechaza a su vez la estacionariedad (2.739, $p &lt; 0.01$). Es la cuarta fila de la tabla: las dos
        pruebas rechazan y se contradicen. Lo primero que esa fila manda revisar es la tendencia, y con el KPSS de
        tendencia la contradicción desaparece (0.096, $p &gt; 0.10$: no rechaza), pero a cambio de un acuerdo peor:
        ahora las dos pruebas dicen que la serie es estacionaria alrededor de una recta.</p>
"""),
(
r"""      <p>Tres evidencias de que el problema es ese y no otro. Primero, el resultado se da la vuelta en cuanto los
        rezagos cubren un ciclo completo. Sobre la serie sin transformar, con $k = 12$ el estadístico pasa de −7.32 a
        −1.51 ($p = 0.781$). La tabla lo recorre sobre <code>log(AirPassengers)</code>, que es la serie del resto de
        este módulo y en la que el $k = 5$ por defecto da −6.42:</p>""",
r"""      <p>Tres evidencias de que el problema es ese y no otro. Primero, el resultado se da la vuelta en cuanto los
        rezagos cubren un periodo estacional completo. Sobre la misma serie sin transformar, con $k = 12$ el
        estadístico pasa de −7.32 a −1.51 ($p = 0.781$). La tabla repite la cuenta con varios $k$, pero sobre
        <code>log(AirPassengers)</code>: el logaritmo iguala la amplitud de las oscilaciones, que en esta serie crece
        con el nivel (Capítulo 1; el Módulo 8 lo retoma), y es la escala en que se trabaja desde aquí hasta el final
        del capítulo. En logaritmos el $k = 5$ por defecto da −6.42 en lugar de −7.32, y la conclusión es la
        misma:</p>"""),
(
r"""            <th scope="col">Rezagos $k$</th>
            <th scope="col">Estadístico ADF</th>""",
r"""            <th scope="col">Rezagos $k$</th>
            <th scope="col">ADF de <code>log(AirPassengers)</code></th>"""),
(
r"""      <p>Segundo, si desestacionalizamos la serie con STL y volvemos a aplicar el ADF con los mismos 5 rezagos, el
        estadístico pasa a""",
r"""      <p>Segundo, al desestacionalizar esa serie en logaritmos con STL (Capítulo 1) y volver a aplicar el ADF con los
        mismos 5 rezagos, el estadístico pasa a"""),
(
r"""      <p>Tercero —y es la prueba más contundente— podemos simular series donde <strong>sabemos con certeza</strong> que
        hay raíz unitaria, porque las construimos como caminatas aleatorias, y añadirles un componente estacional de
        amplitud creciente. Si la prueba fuera inmune""",
r"""      <p>Tercero —y es la evidencia más contundente— se pueden simular series en las que hay raíz unitaria
        <strong>con certeza</strong>, porque se construyen como caminatas aleatorias, y sumarles una oscilación anual
        de amplitud $A$ fija, probando amplitudes cada vez mayores: 0, 0.5, 1, 2 y 4. Si la prueba fuera inmune"""),
(
r"""        <p><strong>Regla de trabajo.</strong> Con series estacionales, <strong>no</strong> apliques ADF o KPSS a la
          serie cruda. El orden correcto (que seguiremos en el Módulo 9 y en el Capítulo 5) es: estabilizar la varianza
          → decidir la diferencia <em>estacional</em> → y solo entonces contrastar la raíz unitaria regular. Las
          funciones <code>nsdiffs()</code> y <code>ndiffs()</code> del Módulo 7 hacen esos dos contrastes, pero el
          orden lo pone quien las usa: primero <code>nsdiffs()</code>, se diferencia, y después <code>ndiffs()</code>
          sobre la serie ya diferenciada.</p>""",
r"""        <p><strong>Regla de trabajo.</strong> Con series estacionales, ni el ADF ni el KPSS se aplican a la serie
          cruda: antes hay que quitar la estacionalidad, y la herramienta es la diferencia estacional. El orden
          completo —estabilizar la varianza, decidir la diferencia <em>estacional</em> y solo entonces contrastar la
          raíz unitaria regular— es la <strong>regla del orden</strong> del Módulo 7, que presenta las funciones
          <code>nsdiffs()</code> y <code>ndiffs()</code> con que se toman esas dos decisiones. El Módulo 9 la
          encadena en un procedimiento y el Capítulo 5 la aplica.</p>"""),
(
r"""# --- Caso tramposo: una serie estacional ----------------------------------
adf.test(AirPassengers)               # (!!) rechaza la raiz unitaria
#> Dickey-Fuller = -7.3186, Lag order = 5, p-value = 0.01
#> Warning: p-value smaller than printed p-value
trunc((length(AirPassengers) - 1)^(1/3))   # rezagos por defecto: menos que m = 12
#> [1] 5

# Con rezagos que cubren un ciclo completo, el resultado se invierte""",
r"""# --- Tendencia determinista: una recta con ruido, tan larga como la TRM ----
set.seed(1)
recta &lt;- 10 + 0.5 * (1:138) + rnorm(138, sd = 5)
adf.test(recta)                       # rechaza la raiz unitaria
kpss.test(recta, null = "Trend")      # no rechaza: estacionaria en tendencia

# --- Caso tramposo: una serie estacional ----------------------------------
adf.test(AirPassengers)               # (!!) rechaza la raiz unitaria
#> Dickey-Fuller = -7.3186, Lag order = 5, p-value = 0.01
#> Warning: p-value smaller than printed p-value
trunc((length(AirPassengers) - 1)^(1/3))   # rezagos por defecto: menos que m = 12
#> [1] 5
kpss.test(AirPassengers)              # rechaza la estacionariedad: se contradicen
kpss.test(AirPassengers, null = "Trend")   # no rechaza: coinciden, y las dos fallan

# Con rezagos que cubren un periodo estacional completo, el resultado se invierte"""),
(
r"""# opciones por defecto NO reproduce adf.test() de R; los estadisticos difieren.</code></pre>
        </div>
      </div>
""",
r"""# opciones por defecto NO reproduce adf.test() de R; los estadisticos difieren.</code></pre>
        </div>
      </div>

      <p>Las pruebas dicen si la serie necesita corrección, y el caso tramposo, que no se les puede preguntar en
        cualquier orden. El Módulo 7 presenta la corrección y fija ese orden.</p>
"""),
]
