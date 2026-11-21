"""R3 · Módulo 10 · tres partes ordenadas (el puente a las redes y el material nuevo; el resumen,
último antes de la evaluación; la evaluación), un solo nombre, y la actividad del Parcial 2 con su
nuevo título de práctica de repaso (sin tocar sus preguntas)."""


def registra(c, mover, MOD, **_):
    c("M10 · un solo nombre: marcador del módulo", MOD,
      r'''  <!-- MÓDULO 10 · Cierre: ciencia de datos, resumen y evaluación    -->''',
      r'''  <!-- MÓDULO 10 · Cierre: redes, resumen y evaluación                -->''')

    c("M10 · un solo nombre: encabezado", MOD,
      r'''3.10 Autorregresión, redes
          neuronales y cierre <span class="text-gray-400 font-normal text-2xl">/ Autoregression &amp; sequence
            models</span></h2>''',
      r'''3.10 Cierre: redes, resumen y
          evaluación <span class="text-gray-400 font-normal text-2xl">/ Closing: sequence models, summary &amp;
            assessment</span></h2>''')

    c("M10 · el objetivo dice las tres partes", MOD,
      r'''              secuenciales del aprendizaje profundo, y saber cuándo el modelo pequeño sigue siendo la mejor opción.</p>''',
      r'''              secuenciales del aprendizaje profundo, saber cuándo el modelo pequeño sigue siendo la mejor opción y
              cerrar el capítulo con un resumen y su evaluación.</p>''')

    c("M10 · una frase al empezar dice cómo se ordena el módulo", MOD,
      r'''      <h3>El AR es la idea original</h3>''',
      r'''      <p>El módulo cierra el capítulo en tres partes: primero, el puente entre el AR y las redes neuronales y la regla
        para elegir el modelo y fijar sus órdenes; después, el resumen; y al final, la evaluación —autoevaluación,
        ejercicios y una práctica de repaso—.</p>

      <h3>El AR es la idea original</h3>''')

    c("M10 · T, no n, en las razones para quedarse con un ARMA", MOD,
      r'''<li><strong>Pocos datos.</strong> El caso de este capítulo tiene $n = 100$.''',
      r'''<li><strong>Pocos datos.</strong> El caso de este capítulo tiene $T = 100$.''')

    c("M10 · el 11.22 es un pseudo-periodo", MOD,
      r'''es un <strong>periodo en años</strong> que se puede contrastar con la astronomía.''',
      r'''es un <strong>pseudo-periodo en años</strong> que se puede contrastar con la astronomía.''')

    c("M10 · el resumen, pseudo-periodo", MOD,
      r'''produce un <strong>pseudo-ciclo</strong>
            de periodo $2\pi/\arccos\!\big(\phi_1/(2\sqrt{-\phi_2})\big)$.</li>''',
      r'''produce un <strong>pseudo-ciclo</strong>
            de pseudo-periodo $2\pi/\arccos\!\big(\phi_1/(2\sqrt{-\phi_2})\big)$.</li>''')

    c("M10 · la tabla de órdenes se presenta sin el «Esta» ambiguo", MOD,
      r'''      <p>El Módulo 5 dio la tabla de identificación: qué forma tienen la ACF y la PACF de cada familia. Esta la
        completa con lo que viene después, que es donde se decide el capítulo — de dónde sale el número, y qué hacer
        cuando la lectura de los correlogramas no lo da.</p>''',
      r'''      <p>La tabla de identificación del Módulo 5 dice qué forma tienen la ACF y la PACF de cada familia. Esta nueva
        tabla la completa con lo que vino después, que es donde se decide el capítulo: de dónde sale el número $p$ o
        $q$, y qué hacer cuando la lectura de los correlogramas no lo da.</p>''')

    c("M10 · la fila del AR: √T, y la última barra vale φ_p (como dice el Módulo 2)", MOD,
      r'''            <td>$p$ es el rezago tras el cual la PACF entra en $\pm 1.96/\sqrt{n}$ <em>y se queda</em>. Esa última
              barra además <strong>estima $\phi_p$</strong>: en el AR(2) del Módulo 9 la PACF teórica en $2$ vale
              $-0.6853$, el coeficiente mismo</td>''',
      r'''            <td>$p$ es el rezago tras el cual la PACF entra en $\pm 1.96/\sqrt{T}$ <em>y se queda</em>. Esa última
              barra además <strong>estima $\phi_p$</strong>, que es lo que la teórica vale (Módulo 2): en el AR(2) del
              Módulo 9 la PACF teórica en $2$ vale $-0.6853$, el coeficiente mismo</td>''')

    c("M10 · T, no n, en el aviso de las dos primeras filas", MOD,
      r'''propiedad del proceso; lo que se ve es una muestra, y con $n$ moderado las barras posteriores al corte no''',
      r'''propiedad del proceso; lo que se ve es una muestra, y con $T$ moderado las barras posteriores al corte no''')

    c("M10 · el aviso del ARMA(2,2): identificables, y quién lo advertía", MOD,
      r'''se cancela, como advertía el Módulo 4. El daño no lo recibe el criterio de información,''',
      r'''se cancela, como advertían los Módulos 4 y 5. El daño no lo recibe el criterio de información,''')

    c("M10 · el aviso del ARMA(2,2): los coeficientes no son identificables", MOD,
      r'''modelo grande no quedan identificados, sus errores estándar se disparan y ninguno parece significativo.''',
      r'''modelo grande no son identificables, sus errores estándar se disparan y ninguno parece significativo.''')

    c("M10 · los ejercicios ya no remiten a un script que el lector no ve", MOD,
      r'''      <p>Tres ejercicios con pista y solución comentada. Las cifras de las soluciones están calculadas en R con el
        script <code>precalculo/genera_soluciones.R</code>: ninguna está escrita de memoria, y puedes contrastar las
        tuyas contra ellas.</p>''',
      r'''      <p>Tres ejercicios con pista y solución comentada. Las cifras de cada solución salen de ejecutar el código que
        la acompaña, ninguna está escrita de memoria, y puedes contrastar las tuyas con ellas.</p>''')

    c("M10 · la actividad del Parcial 2, con su nuevo título y su presentación", MOD,
      r'''      <h3>Actividad preparatoria · Parcial 2</h3>

      <p>Diez preguntas para preparar el Parcial 2 por tu cuenta, sobre el <a
          href="capitulo-2-estacionariedad-acf-pacf.html" class="text-primary underline">capítulo 2</a> y los cuatro
        primeros módulos de este: estacionariedad débil, caminata con deriva, ADF y KPSS, sobrediferenciación, operador
        de rezago, el triángulo del AR(2), el <code>intercept</code> de <code>arima()</code>, la invertibilidad del
        MA(1), los pesos $\psi$ y Yule–Walker. No tienen nota ni se entregan. Los módulos 3.5 a 3.10 no entran aquí: para
        ellos están la autoevaluación y los ejercicios de más arriba.</p>''',
      r'''      <h3>Práctica de repaso · capítulo 2 y módulos 3.1–3.4</h3>

      <p>Diez preguntas para repasar por tu cuenta, sobre el <a
          href="capitulo-2-estacionariedad-acf-pacf.html" class="text-primary underline">capítulo 2</a> y los cuatro
        primeros módulos de este: estacionariedad débil, caminata con deriva, ADF y KPSS, sobrediferenciación, operador
        de rezago, el triángulo del AR(2), el <code>intercept</code> de <code>arima()</code>, la invertibilidad del
        MA(1), los pesos $\psi$ y Yule–Walker. Se escribieron como preparación del Parcial 2, que ya se aplicó, y
        siguen sirviendo de repaso. No tienen nota ni se entregan. Los módulos 3.5 a 3.10 no entran aquí: para ellos
        están la autoevaluación y los ejercicios de más arriba.</p>''')

    c("M10 · la actividad, título del recuadro", MOD,
      r'''        <h4><i class="fas fa-clipboard-check" aria-hidden="true"></i> Actividad preparatoria · Parcial 2</h4>''',
      r'''        <h4><i class="fas fa-clipboard-check" aria-hidden="true"></i> Práctica de repaso · capítulo 2 y módulos 3.1–3.4</h4>''')

    c("M10 · «Lo que viene» dice dónde vuelve AirPassengers", MOD,
      r'''        <p style="margin-bottom:0;"><strong>Lo que viene.</strong> Todo este capítulo ha supuesto que la serie ya era
          estacionaria. En el <strong>Capítulo 4</strong> se añade la pieza que falta —la integración, el orden
          $d$— para llegar a los modelos <strong>ARIMA</strong> y a la metodología completa de Box–Jenkins, con el
          algoritmo de Hyndman–Khandakar que automatiza la búsqueda. Y allí volverá, ahora con consecuencias, la
          advertencia sobre comparar criterios de información entre modelos con distinto $d$.</p>''',
      r'''        <p><strong>Lo que viene.</strong> Todo este capítulo ha supuesto que la serie ya era
          estacionaria. En el <strong>Capítulo 4</strong> se añade la pieza que falta —la integración, el orden
          $d$— para llegar a los modelos <strong>ARIMA</strong> y a la metodología completa de Box–Jenkins, con el
          algoritmo de Hyndman–Khandakar que automatiza la búsqueda. Y allí volverá, ahora con consecuencias, la
          advertencia sobre comparar criterios de información entre modelos con distinto $d$.</p>
        <p style="margin-bottom:0;"><code>AirPassengers</code>, la serie con que terminó el Capítulo 2, no aparece en
          este capítulo: la dependencia que quedó en $\nabla\nabla_{12}\log y_t$ vuelve en el
          <strong>Capítulo 5</strong>, que extiende las herramientas de este a la estacionalidad y le ajusta el modelo
          <em>airline</em> (módulos 5.5 y 5.7).</p>''')

    # Primero el material nuevo (órdenes), después el resumen, y la evaluación al final.
    mover("M10 · «Elegir el modelo y fijar sus órdenes», antes del resumen", MOD,
          "      <h3>Elegir el modelo y fijar sus órdenes</h3>\n",
          "      <h3>Autoevaluación</h3>\n",
          "      <h3>Resumen del capítulo</h3>\n")
