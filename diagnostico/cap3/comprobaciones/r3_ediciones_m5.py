"""R3 · Módulo 5 · la tabla va antes del ciclo que la cita, y el laboratorio que cumple el objetivo
justo después de la tabla; el ciclo anuncia lo que desarrolla el Módulo 8 (AICc, BIC, Ljung–Box,
fitdf) y explica Bartlett; γ₁ y ρ₁ salen del plegado."""


def registra(c, mover, MOD, **_):
    c("M5 · la tabla de identificación se presenta con una frase y fija qué es «identificar»", MOD,
      r'''      <h3>La tabla de identificación</h3>

      <table style="position:relative;">''',
      r'''      <h3>La tabla de identificación</h3>

      <p>Con lo que dejaron los Módulos 2 y 3, la regla para proponer un modelo cabe en una tabla. En ella
        <em>identificar</em> quiere decir proponer los órdenes $p$ y $q$ a partir de los correlogramas; no es lo mismo
        que la identificabilidad de un parámetro, la del Módulo 3.</p>

      <table style="position:relative;">''')

    c("M5 · el laboratorio, con un título y una frase que lo ligan a la tabla", MOD,
      r'''      <div class="simulador" data-simulador="laboratorio-arma">''',
      r'''      <h3>Lo que la tabla promete y lo que da una muestra</h3>

      <p>La tabla describe la teoría: ACF y PACF exactas, sin ruido. Con datos, el correlograma es una muestra, y el
        laboratorio deja ver cuánto se parece a la teoría que la generó.</p>

      <div class="simulador" data-simulador="laboratorio-arma">''')

    c("M5 · el ciclo se presenta tras la tabla y el laboratorio, y anuncia lo que desarrolla el Módulo 8", MOD,
      r'''      <p>Con dos partes mezcladas, identificar deja de ser leer una fila de una tabla. Es un ciclo de cuatro pasos que se
        repite hasta que el diagnóstico queda limpio, y la tabla solo interviene en el tercero:</p>
''',
      r'''      <h3>Identificar es un ciclo</h3>

      <p>Con dos partes mezcladas la tabla no alcanza —su tercera fila no da los órdenes— y con datos el correlograma
        es una muestra ruidosa, como acaba de verse. Identificar deja de ser leer una fila de una tabla: es un ciclo de
        cuatro pasos que se repite hasta que el diagnóstico queda limpio, y la tabla solo interviene en el tercero.</p>

      <p>El ciclo nombra herramientas que el Módulo 8 desarrolla y que aquí solo se anuncian: los criterios de
        información (AICc y BIC) comparan modelos ajustados a los mismos datos y penalizan cada parámetro; la prueba de
        Ljung–Box resume en un solo $p$-valor si los residuales parecen ruido blanco, y su argumento
        <code>fitdf</code> descuenta de los grados de libertad los parámetros que se estimaron.</p>
''')

    c("M5 · el ciclo, paso 1: T en lugar de n, y la banda de Bartlett explicada", MOD,
      r'''La banda $\pm 1.96/\sqrt{n}$ marca qué es ruido. Sin ese argumento, statsmodels dibuja la banda de Bartlett, que se ensancha con el rezago.</p>''',
      r'''La banda $\pm 1.96/\sqrt{T}$ marca qué es ruido. Sin ese argumento, statsmodels dibuja la banda de Bartlett, que no supone ruido blanco y se ensancha con el rezago porque cuenta las autocorrelaciones de los rezagos anteriores.</p>''')

    c("M5 · el ciclo, paso 2: T en lugar de n", MOD,
      r'''con datos reales: con $n$ pequeño, vuelve al paso 1 sabiendo que la banda es ancha.''',
      r'''con datos reales: con $T$ pequeño, vuelve al paso 1 sabiendo que la banda es ancha.''')

    c("M5 · «Media, varianza y autocorrelación» dice lo que trae: autocovarianzas", MOD,
      r'''      <h3>Media, varianza y autocorrelación</h3>

      <p>Antes de mirar qué le pasa a la ACF conviene escribir los momentos del proceso, como se hizo con el AR en el''',
      r'''      <h3>Media, varianza y autocovarianzas</h3>

      <p>Antes de mirar qué le pasa a la ACF conviene escribir los momentos del proceso, como se hizo con el AR en el''')

    c("M5 · γ₁ y ρ₁ del ARMA(1,1), a la vista y no solo en el plegado", MOD,
      r'''Con $\phi = 0.7$ y $\theta = 0.5$ vale $1.95$, y la varianza,
        $1.95/0.51 = 3.8235\,\sigma^2$.</p>''',
      r'''Con $\phi = 0.7$ y $\theta = 0.5$ vale $1.95$, y la varianza,
        $1.95/0.51 = 3.8235\,\sigma^2$. Del mismo modo, $\gamma_1 = 1.62/0.51\,\sigma^2 = 3.1765\,\sigma^2$, y el
        cociente de las dos es $\rho_1 = 3.1765/3.8235 = 0.8308$: la primera de las cuatro cifras que el Módulo 4
        obtuvo sumando pesos $\psi$.</p>''')

    c("M5 · el código de la redundancia anuncia que el AICc es del Módulo 8", MOD,
      r'''# Y el modelo mas pequeno gana:
aicc &lt;- function(f, n)''',
      r'''# Y el modelo mas pequeno gana. El criterio es el AICc, que presenta el
# Modulo 8: por ahora basta saber que menor es mejor.
aicc &lt;- function(f, n)''')

    # Primero la tabla (con su aviso), después el laboratorio, y los dos delante del ciclo.
    mover("M5 · la tabla de identificación y su aviso, antes del ciclo", MOD,
          "      <h3>La tabla de identificación</h3>\n",
          "      <h3>Media, varianza y autocovarianzas</h3>\n",
          "      <h3>Identificar es un ciclo</h3>\n")
    mover("M5 · el laboratorio y su nota, tras la tabla y antes del ciclo", MOD,
          "      <h3>Lo que la tabla promete y lo que da una muestra</h3>\n",
          "      <h3>Redundancia de parámetros: cuando sobra un factor</h3>\n",
          "      <h3>Identificar es un ciclo</h3>\n")
