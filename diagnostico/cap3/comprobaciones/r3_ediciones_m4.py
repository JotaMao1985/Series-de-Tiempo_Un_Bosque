"""R3 · Módulo 4 · el ARMA se anuncia en una frase; la recursión de ψ y π sale del plegado; las dos
notas de otros capítulos pasan a una sección propia tras el código; «abanico» y «caminata» se fijan."""


def registra(c, mover, MOD, **_):
    c("M4 · el ARMA, anunciado como adelanto del Módulo 5", MOD,
      r'''        de las ideas más útiles del capítulo.</p>

      <div class="definition">
        <h4><i class="fas fa-book mr-2" aria-hidden="true"></i>Las dos representaciones</h4>''',
      r'''        de las ideas más útiles del capítulo.</p>

      <p>Un <strong>ARMA($p,q$)</strong> es lo que sale de pedirle a un proceso las dos memorias a la vez: un AR($p$)
        alimentado por un MA($q$), $\phi(B)\,y_t = \theta(B)\,\varepsilon_t$. El Módulo 5 lo define y lo estudia con
        detalle; aquí basta saber que con $q = 0$ es el AR del Módulo 2, que con $p = 0$ es el MA del Módulo 3, y que
        lleva los dos polinomios, de modo que la dualidad vale para todos.</p>

      <div class="definition">
        <h4><i class="fas fa-book mr-2" aria-hidden="true"></i>Las dos representaciones</h4>''')

    c("M4 · el control h del simulador remite a la sección que explica la varianza del pronóstico", MOD,
      r'''          del pronóstico a $h$ pasos, y la lectura da su suma de cuadrados junto al límite al que tiende.</p>''',
      r'''          del pronóstico a $h$ pasos (la sección «Para qué sirven los $\psi$», más abajo, explica por qué), y la
          lectura da su suma de cuadrados junto al límite al que tiende.</p>''')

    c("M4 · la recursión de ψ y π, a la vista y antes del desarrollo", MOD,
      r'''      <h3>Cómo se calculan los pesos</h3>

      <div class="derivacion">''',
      r'''      <h3>Cómo se calculan los pesos</h3>

      <p>Los pesos salen de comparar coeficientes en dos identidades, $\phi(B)\,\psi(B) = \theta(B)$ y
        $\theta(B)\,\pi(B) = \phi(B)$, que son las definiciones de arriba sin la división. Igualar los coeficientes de
        $B^j$ da dos recursiones:</p>

      $$\begin{gathered}
        \psi_j = \theta_j + \sum_{i=1}^{p}\phi_i\,\psi_{j-i} \\
        \pi_j = -\phi_j - \sum_{i=1}^{q}\theta_i\,\pi_{j-i}
      \end{gathered}$$

      <p>con $\psi_0 = \pi_0 = 1$, $\theta_j = 0$ si $j > q$, $\phi_j = 0$ si $j > p$, y los pesos de índice negativo
        iguales a cero. Cada peso se calcula con los anteriores, que es todo lo que pide el ejemplo de más abajo; el
        desarrollo plegado enseña de dónde salen.</p>

      <div class="derivacion">''')

    c("M4 · el plegado ya no remite al código que el lector no ve (recursión)", MOD,
      r'''              <p>Igualando coeficiente a coeficiente sale una <strong>recursión</strong>, que es lo que implementan el
                simulador de esta página y el precálculo en R:</p>''',
      r'''              <p>Igualando coeficiente a coeficiente sale una <strong>recursión</strong>, la misma de arriba:</p>''')

    c("M4 · el plegado ya no describe la guarda del código", MOD,
      r'''              <p style="margin-bottom:0;">En los primeros rezagos la suma se sale por abajo del rango: se entiende
                $\psi_j = 0$ para $j &lt; 0$, y lo mismo para los $\pi$ del paso siguiente. Es la guarda
                <code>if (j - i &gt;= 0)</code> que aparece en las dos implementaciones.</p>''',
      r'''              <p style="margin-bottom:0;">En los primeros rezagos la suma se sale por abajo del rango: se entiende
                $\psi_j = 0$ para $j &lt; 0$, y lo mismo para los $\pi$ del paso siguiente.</p>''')

    c("M4 · el resultado del plegado habla de lo que el lector ve, no de ocho procesos ni de un error de 6.7e-16", MOD,
      r'''          <p class="derivacion-resultado">Esta última fórmula es la que usa el <strong>laboratorio del Módulo 5</strong>
            para dibujar la ACF teórica en el navegador: trunca la serie en 600 términos y divide entre $\gamma_0$.
            Contrastada contra <code>ARMAacf()</code> de R sobre los ocho procesos del capítulo, el error máximo es de
            $6.7\times10^{-16}$, o sea, el redondeo de la aritmética de punto flotante.</p>''',
      r'''          <p class="derivacion-resultado">Esta última fórmula es la que usa el <strong>laboratorio del Módulo 5</strong>
            para dibujar la ACF teórica: suma los productos de los pesos y divide entre $\gamma_0$. El último bloque de
            código de este módulo hace la misma cuenta, con dos mil términos, y la contrasta con
            <code>ARMAacf()</code>.</p>''')

    c("M4 · sección propia para las notas de los capítulos 4 a 6; «abanico» definido; h = j + 1", MOD,
      r'''      <div class="note">
        <p><strong>Por qué esto reaparece en los capítulos 4, 5 y 6.</strong> La varianza del error de pronóstico a
          $h$ pasos de un ARMA es</p>
        $$\operatorname{Var}(e_{T+h}) = \sigma^2\sum_{j=0}^{h-1}\psi_j^2$$
        <p style="margin-bottom:0;">Los pesos $\psi$ son, literalmente, lo que da su forma de abanico a las bandas de
          un pronóstico. Cuanto más lentamente decaen, más rápido se abre la incertidumbre.''',
      r'''      <h3>Para qué sirven los $\psi$ en los capítulos siguientes</h3>

      <div class="note">
        <p><strong>Por qué esto reaparece en los capítulos 4, 5 y 6.</strong> La varianza del error de pronóstico a
          $h$ pasos de un ARMA es</p>
        $$\operatorname{Var}(e_{T+h}) = \sigma^2\sum_{j=0}^{h-1}\psi_j^2$$
        <p>La suma llega hasta $h-1$ porque el horizonte $h$ usa $h$ pesos, de $\psi_0$ a $\psi_{h-1}$: el peso
          $\psi_j$ es el último del horizonte $h = j+1$.</p>
        <p style="margin-bottom:0;">Los pesos $\psi$ son, literalmente, lo que da su forma de abanico a las bandas de
          un pronóstico (aquí, «abanico» es la banda de incertidumbre que se ensancha con el horizonte, y no el
          abanico de amplitud que crece con el nivel de la serie, de los Capítulos 1 y 2). Cuanto más lentamente
          decaen, más rápido se abre la incertidumbre.''')

    c("M4 · caminata aleatoria, no «paseo» (primera mención)", MOD,
      r'''          MA($\infty$) ya no converge, pero la recursión de los $\psi$ no lo nota: sigue produciendo números. En el
          paseo aleatorio, $\phi(B) = 1 - B$, salen todos iguales,''',
      r'''          MA($\infty$) ya no converge, pero la recursión de los $\psi$ no lo nota: sigue produciendo números. En la
          caminata aleatoria, $\phi(B) = 1 - B$, salen todos iguales,''')

    c("M4 · caminata aleatoria, no «paseo» (segunda mención)", MOD,
      r'''          en el paseo aleatorio da $\sigma^2 h$, un abanico que se abre sin límite.''',
      r'''          en la caminata aleatoria da $\sigma^2 h$, un abanico que se abre sin límite.''')

    # Las dos notas (con su título) van tras el bloque de código y su aviso, y antes de «Dos ideas».
    mover("M4 · «Para qué sirven los ψ», después del código", MOD,
          "      <h3>Para qué sirven los $\\psi$ en los capítulos siguientes</h3>\n",
          "      <div class=\"code-tabs\">\n        <div class=\"code-tabs-nav\" role=\"tablist\" aria-label=\"Pesos psi y pi\">",
          "      <h3>Dos ideas que hereda el Módulo 5</h3>\n")
