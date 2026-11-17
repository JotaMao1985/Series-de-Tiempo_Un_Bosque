# R3 · Modulo 1: adelantos (ruido blanco, caminata), AirPassengers presentada, voz impersonal.
EDICIONES = [
(
"""      <p>En el Capítulo 1 descompusimos una serie en tendencia, estacionalidad y residuo. Ahora damos el paso siguiente:
        para <em>modelar</em> la dependencia temporal necesitamos que las reglas del juego no cambien con el tiempo. Esa
        es la idea de <strong>estacionariedad</strong> (<em>stationarity</em>).</p>

      <p>La intuición es simple. Si observamos una serie durante 1949–1954 y otra vez durante 1955–1960 y las dos
        ventanas se ven""",
"""      <p>En el Capítulo 1 se descompuso una serie en tendencia, estacionalidad y residuo. El paso siguiente es otro:
        para <em>modelar</em> la dependencia temporal hace falta que las reglas del juego no cambien con el tiempo. Esa
        es la idea de <strong>estacionariedad</strong> (<em>stationarity</em>).</p>

      <p>La intuición es simple. Si se observa una serie durante 1949–1954 y otra vez durante 1955–1960 y las dos
        ventanas se ven"""),
(
"""conjunta queda determinada por medias y covarianzas, y entonces las dos nociones coinciden. En este curso,
          cuando digamos "estacionaria" sin más, nos referiremos a la <strong>débil</strong>.</p>""",
"""conjunta queda determinada por medias y covarianzas, y entonces las dos nociones coinciden. En este curso,
          «estacionaria» sin más quiere decir estacionaria en sentido <strong>débil</strong>.</p>"""),
(
"""      <p>Veamos las tres condiciones en acción. Abajo hay tres series: solo la primera es estacionaria.</p>
""",
"""      <p>Las tres condiciones se entienden mejor en acción. Abajo hay tres series, y solo la primera es
        estacionaria. Dos de ellas se adelantan a su módulo: el <strong>ruido blanco</strong> —valores aleatorios sin
        relación entre sí— se define en el Módulo 2, y la <strong>caminata aleatoria</strong> —cada valor es el
        anterior más un ruido nuevo—, en el Módulo 5. La tercera es <code>AirPassengers</code>, la serie del
        Capítulo 1: miles de pasajeros de aerolíneas internacionales por mes, de 1949 a 1960.</p>
"""),
(
"""            <td>(2) y (3): la varianza <em>crece</em> con $t$ ($\\operatorname{Var}(y_t) = t\\sigma^2$)</td>""",
"""            <td>(2) y (3): la varianza <em>crece</em> con $t$ ($\\operatorname{Var}(y_t) = t\\sigma^2$, como se
              deduce en el Módulo 5), y la covarianza entre dos instantes crece con ella</td>"""),
(
"""estimados no significan lo que creemos, los errores estándar están mal y los pronósticos heredan el problema.
          Buena parte de este capítulo consiste en dos preguntas: <em>¿es estacionaria?</em> y, si no, <em>¿cómo la
            transformo para que lo sea?</em></p>""",
"""estimados no significan lo que parecen, los errores estándar están mal y los pronósticos heredan el problema.
          Buena parte de este capítulo consiste en dos preguntas: <em>¿es estacionaria?</em> y, si no, <em>¿cómo se
            transforma para que lo sea?</em></p>"""),
]
