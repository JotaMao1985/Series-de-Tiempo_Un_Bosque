# R3 · tras la verificacion (R3_verificacion.md): los 5 «corregir» de contenido y los menores.
# Se aplica con r3_edita.py. La pista de las tablas (armazon) va en r3b_ediciones_armazon.py.
EDICIONES = [
# --- 1 y 6 · M7, caja de la regla: que hace ndiffs() y sobre que STL mide nsdiffs(); 16 · FPP3 sin «por eso»
(
r"""        <p><code>nsdiffs()</code> y <code>ndiffs()</code> son funciones del paquete <code>forecast</code> de R.
          La segunda repite el KPSS del Módulo 6 —diferenciar, volver a probar— hasta que deja de rechazar, y
          devuelve cuántas diferencias hicieron falta; la primera mide la fuerza de la estacionalidad, el $F_S$ del
          Capítulo 1, y pide una diferencia estacional si pasa de 0.64. Cada una decide una sola clase de
          diferencia: el orden lo pone quien las usa.</p>
        <p style="margin-bottom:0;">El orden no cambia la serie a la que se llega si se aplican las dos diferencias
          —$\nabla\nabla_{12} y_t = \nabla_{12}\nabla y_t$, algebraicamente—, pero sí lo que se decide por el camino,
          por dos razones. La primera es que a veces con la diferencia estacional basta y la serie ya queda
          estacionaria, con lo que se ahorra una diferencia regular que solo añadiría ruido: por eso la
          recomendación de FPP3 es aplicar primero la estacional. Tiene su explicación: la diferencia estacional ya
          lleva dentro una regular, porque $1 - B^m = (1-B)(1 + B + \cdots + B^{m-1})$. La segunda es la del
          Módulo 6: las pruebas de raíz unitaria regular no son
          fiables sobre una serie que todavía es estacional. La sección «El orden, en dos series», más abajo,
          muestra las dos.</p>""",
r"""        <p><code>nsdiffs()</code> y <code>ndiffs()</code> son funciones del paquete <code>forecast</code> de R.
          La segunda repite una prueba KPSS —diferenciar, volver a probar— hasta que deja de rechazar o llega a
          dos diferencias, y devuelve cuántas hicieron falta. No es el <code>kpss.test()</code> del Módulo 6: usa
          la versión del paquete <code>urca</code>, con otro truncamiento de rezagos, y las dos pueden no
          coincidir, como muestra el recuadro del final de este módulo. La primera mide la fuerza de la
          estacionalidad con la fórmula del $F_S$ del Capítulo 1, calculada sobre su propia descomposición STL, y
          pide una diferencia estacional si pasa de 0.64. Cada una decide una sola clase de diferencia: el orden
          lo pone quien las usa.</p>
        <p>El orden no cambia la serie a la que se llega si se aplican las dos diferencias
          —$\nabla\nabla_{12} y_t = \nabla_{12}\nabla y_t$, algebraicamente—, pero sí lo que se decide por el camino,
          por dos razones:</p>
        <ul>
          <li>La recomendación de FPP3 es aplicar primero la diferencia estacional: a veces con ella basta y la
            serie ya queda estacionaria, y se ahorra una diferencia regular que solo añadiría ruido. Que baste
            tiene su explicación: la diferencia estacional ya lleva dentro una regular, porque
            $1 - B^m = (1-B)(1 + B + \cdots + B^{m-1})$.</li>
          <li>Las pruebas de raíz unitaria regular no son fiables sobre una serie que todavía es estacional
            (Módulo 6).</li>
        </ul>
        <p style="margin-bottom:0;">La sección «El orden, en dos series», más abajo, muestra las dos.</p>"""),
(
r"""repetir. Eso es exactamente lo que hace <code>ndiffs()</code>.</li>""",
r"""repetir. Es lo que hace <code>ndiffs()</code>, con su propia versión del KPSS.</li>"""),
# --- 2 · M5, cierre
(
r"""      <p>Con $\phi = 0.95$ y con $\phi = 1$ las series se parecen, y sus correlogramas también: a ojo la decisión es
        frágil. El Módulo 6 le pone un número.</p>""",
r"""      <p>Con $\phi = 0.95$ y con $\phi = 1$ las series se parecen, y sus correlogramas también: a ojo la decisión es
        frágil. El Módulo 6 cambia el ojo por pruebas, que deciden con una regla y con un margen de error
        declarado. No vuelven fácil el caso difícil —con $\phi$ tan cerca de 1 y doscientos datos, lo habitual es
        que tampoco ellas lo separen de la raíz unitaria—, pero sí dicen cuándo la evidencia alcanza y cuándo
        no.</p>"""),
# --- 4 · M9, resumen
(
r"""            <td>Con menos rezagos que el periodo estacional rechaza la raíz unitaria sin motivo: no se aplica a
              una serie estacional cruda</td>""",
r"""            <td>Con menos rezagos que el periodo estacional puede rechazar la raíz unitaria sin motivo, tanto más
              cuanto más marcada es la estacionalidad: no se aplica a una serie estacional cruda</td>"""),
# --- 5 (7 del informe) · M9, paso 4
(
r"""              <span class="ciclo-resumen">$\nabla$ si queda tendencia</span>""",
r"""              <span class="ciclo-resumen">$\nabla$ si queda raíz unitaria</span>"""),
(
r"""            <p>Comprobar si queda tendencia o raíz unitaria y aplicar $\nabla$. Nunca sobre una serie estacional cruda:""",
r"""            <p>Comprobar si queda una raíz unitaria y, si queda, aplicar $\nabla$. Una tendencia determinista —una recta con ruido— no se diferencia: se le resta la recta, y el Módulo 6 enseña a distinguir los dos casos. Nunca sobre una serie estacional cruda:"""),
# --- 9 del informe · M9, apertura
(
r"""Los pasos 2 a 4 son la regla del
        orden del Módulo 7; los otros tres la rodean de lo que ninguna función hace sola: mirar antes, comprobar
        después y dejar constancia.</p>""",
r"""Los pasos 2 a 5 son la regla del
        orden del Módulo 7; el 1 y el 6 la rodean de lo que ninguna función hace sola: mirar antes y dejar
        constancia.</p>"""),
# --- 5 del informe · M3, «una o dos»
(
r"""<strong>14 de sus 24 barras</strong> salen de la banda $\pm 0.171$, cuando por azar se esperaría una o dos.
        No es ruido blanco:""",
r"""<strong>14 de sus 24 barras</strong> salen de la banda $\pm 0.171$. Son demasiadas para el azar, incluso
        contando con que la media móvil con que se calcula ese residuo ya le deja algo de autocorrelación propia.
        No es ruido blanco:"""),
# --- 13 del informe · M3, «el remedio de la segunda fila»
(
r"""Es el remedio de la segunda fila; el
        símbolo $\nabla$ reaparece""",
r"""Es el remedio de la segunda fila cuando lo que
        hay es una raíz unitaria —una tendencia que es una recta fija se trata de otro modo, como explican los
        Módulos 5 y 6—; el símbolo $\nabla$ reaparece"""),
# --- 15 del informe · M4, el glosario en prosa pasa a lista
(
r"""      <p>El explorador de abajo ofrece ocho series, y varias se adelantan a su módulo. La <strong>TRM</strong> es la
        Tasa Representativa del Mercado: la tasa de cambio del peso colombiano frente al dólar, en pesos por dólar.
        Aquí es su promedio mensual de enero de 2015 a junio de 2026, 138 meses, calculado con la serie diaria que
        publica datos.gov.co; es la segunda serie real del capítulo y vuelve en los Módulos 6 y 7. Un $\nabla$
        delante de un nombre indica la serie diferenciada (Módulo 3), y $\nabla_{12}$, la diferencia con el mismo mes
        del año anterior, $y_t - y_{t-12}$, que presenta el Módulo 7. El <strong>logaritmo</strong> de
        <code>AirPassengers</code> es la transformación con la que el Capítulo 1 cerró el abanico de una serie cuya
        amplitud crece con el nivel; el Módulo 8 la retoma. Y <code>ndiffs</code> y <code>nsdiffs</code>, al final de
        la lectura numérica, son dos funciones de R que dicen cuántas diferencias regulares y estacionales pide la
        serie (Módulo 7).</p>
""",
r"""      <p>El explorador de abajo ofrece ocho series, y varias se adelantan a su módulo. Para consultar mientras se
        mueve el selector:</p>

      <ul>
        <li>La <strong>TRM</strong> es la Tasa Representativa del Mercado: la tasa de cambio del peso colombiano
          frente al dólar, en pesos por dólar. Aquí es su promedio mensual de enero de 2015 a junio de 2026, 138
          meses, calculado con la serie diaria que publica datos.gov.co. Es la segunda serie real del capítulo y
          vuelve en los Módulos 6 y 7.</li>
        <li>Un $\nabla$ delante de un nombre indica la serie diferenciada (Módulo 3), y $\nabla_{12}$, la
          diferencia con el mismo mes del año anterior, $y_t - y_{t-12}$, que presenta el Módulo 7.</li>
        <li>El <strong>logaritmo</strong> de <code>AirPassengers</code> es la transformación con la que el
          Capítulo 1 cerró el abanico de una serie cuya amplitud crece con el nivel; el Módulo 8 la retoma.</li>
        <li><code>ndiffs</code> y <code>nsdiffs</code>, al final de la lectura numérica, son dos funciones de R
          que dicen cuántas diferencias regulares y estacionales pide la serie (Módulo 7).</li>
      </ul>
"""),
# --- 11 del informe · M6: el KPSS de tendencia en el acuerdo falso
(
r"""      <p>Tres evidencias de que el problema es ese y no otro. Primero,""",
r"""      <p>Tres evidencias de que el problema es la estacionalidad y no otra cosa. Primero,"""),
(
r"""misma serie desestacionalizada da <strong>0.386 con p &lt; 0.01</strong>, o sea, rechaza la estacionariedad. Sin""",
r"""misma serie desestacionalizada da <strong>0.386 con p &lt; 0.01</strong>, o sea, rechaza la estacionariedad,
        cosa que no hacía con la estacionalidad dentro: también al KPSS lo confundía la oscilación anual, aunque
        por un camino distinto del de los rezagos del ADF, que aquí no se desarrolla. Sin"""),
# --- 14 del informe · M8
(
r"""Es la razón por la que los Módulos 6 y 7 trabajaron con <code>log(AirPassengers)</code>.</p>""",
r"""Es la razón por la que la tabla de rezagos del Módulo 6 y todo el Módulo 7 trabajaron con
        <code>log(AirPassengers)</code>.</p>"""),
# --- 10 del informe · M7, Python
(
r"""# El orden se pone a mano, como en R: primero la estacional (Modulo 9).""",
r"""# El orden se pone a mano, como en R: primero la estacional (la regla de
# este modulo; el Modulo 9 la programa)."""),
# --- 18 del informe · M7, UKgas
(
r"""<code>UKgas</code>, que viene con R, es el consumo trimestral
        de gas del Reino Unido de 1960 a 1986: 108 trimestres, con $m = 4$.""",
r"""<code>UKgas</code>, la serie de un ejercicio del
        Capítulo 1, es el consumo trimestral de gas del Reino Unido de 1960 a 1986: 108 trimestres, con $m = 4$."""),
# --- 8 y 12 del informe · M9, cierre
(
r"""$r_{12} = -0.387$ y 5 de sus 24 autocorrelaciones fuera de la banda. Queda dependencia, y describirla es el
        trabajo del Capítulo 3.</p>""",
r"""$r_{12} = -0.387$ y 5 de sus 24 autocorrelaciones fuera de la banda. Ese $r_1$ negativo no es el rastro de una
        diferencia de más —las pruebas pedían las dos, y con ellas dejaron de pedir—: es dependencia que queda por
        describir, de un mes al siguiente y de un año al siguiente. El Capítulo 3 da las herramientas para la
        primera; el Capítulo 5 las extiende a la segunda y las aplica a esta serie.</p>"""),
(
r"""como uno de los casos reales del capítulo.
        <code>AirPassengers</code> espera al Capítulo 5, que""",
r"""como uno de los casos reales del capítulo.
        <code>AirPassengers</code> espera, como se ha dicho, al Capítulo 5, que"""),
]
