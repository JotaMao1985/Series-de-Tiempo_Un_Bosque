"""R3 · Módulo 4 (4.4 Identificar p y q).

D5: la introducción del simulador deja de dar el resultado (las cifras y la conclusión pasan a un
recuadro posterior a la actividad); el IMA(1,1) ajustado dice cuánto vale su α de suavizamiento
exponencial simple (0.267) y el bloque lo calcula."""


def registra(c, mover, entre, esc, T46, **_):
    c("M4 · la introducción del simulador pide hacer; la lectura de lo que enseña va después", T46,
      r'''        <p class="simulador-intro">Cambia el orden y lee las dos funciones, no solo la ACF. En $d = 0$ la ACF decae
          despacio, que es lo que deja un nivel que se mueve —por una raíz unitaria o por un cambio de nivel como el
          de 1899— y no dice nada de $p$ ni de $q$. La trampa está en la PACF: solo se sale el rezago 1, como en un
          AR(1) con $\phi \approx 0.5$, pero ese AR(1) tendría la ACF dentro de la banda desde el rezago 3. En
          $d = 1$ la ACF corta en 1 y la PACF decae con signo negativo, la firma de un MA(1). El rezago 8 de la ACF
          ($0.231$) se sale por poco, aislado y sin patrón; con 20 rezagos al $5\,\%$, uno fuera por azar es lo
          esperable. En $d = 2$, $\hat\rho_1 = -0.626$ cae por debajo de $-0.5$, el valor que tendría la diferencia
          de un ruido blanco: la huella de haber diferenciado de más. Y fíjate en el $-0.402$ de $d = 1$: un pico
          negativo en el rezago 1, no muy lejos de $-0.5$, es también lo que deja diferenciar una serie que no lo
          necesitaba. La tabla elige $p$ y $q$; no confirma $d$.</p>''',
      r'''        <p class="simulador-intro">Cambia el orden y lee las dos funciones, no solo la ACF. Con cada $d$, ¿cuál de
          las dos corta y cuál decae? ¿Qué signo tiene el rezago 1? ¿Qué barras se salen de la banda, y con qué
          patrón? La lectura de abajo da $\hat\rho_1$ y cuenta las barras de la ACF y de la PACF que salen de la
          banda.</p>''')
    c("M4 · recuadro tras el simulador: lo que enseña (antes iba en la introducción)", T46,
      r'''        <div class="simulador-lectura"></div>
      </div>

      <h3>La tabla, aplicada a $\nabla$Nilo</h3>''',
      r'''        <div class="simulador-lectura"></div>
      </div>

      <div class="note">
        <p style="margin-bottom:0;"><strong>Lo que enseña el simulador.</strong> Con $d = 0$ la trampa está en la
          PACF: solo se sale el rezago 1, como en un AR(1) con $\phi \approx 0.5$, pero ese AR(1) tendría la ACF
          dentro de la banda desde el rezago 3, y esta decae despacio: es lo que deja un nivel que se mueve, por
          una raíz unitaria o por un cambio de nivel como el de 1899. Con $d = 2$, $\hat\rho_1 = -0.626$ cae por debajo de $-0.5$, el valor que tendría la diferencia de un ruido
          blanco: la huella de haber diferenciado de más. Y el $-0.402$ de $d = 1$, un pico negativo en el
          rezago 1 no muy lejos de $-0.5$, es también lo que deja diferenciar una serie que no lo necesitaba. La
          tabla elige $p$ y $q$; no confirma $d$.</p>
      </div>

      <h3>La tabla, aplicada a $\nabla$Nilo</h3>''')

    c("M4 · el rezago 8 aislado: el azar lo explica (antes lo decía la introducción)", T46,
      r'''el único otro que sale de la banda de
        $\pm 0.197$ es el 8 ($0.231$), aislado y sin patrón— y la PACF decae con signo negativo''',
      r'''el único otro que sale de la banda de
        $\pm 0.197$ es el 8 ($0.231$), aislado y sin patrón; con 20 rezagos al $5\,\%$, uno fuera por azar es lo
        esperable— y la PACF decae con signo negativo''')

    c("M4 · el IMA(1,1) dice su α", T46,
      r'''Es el IMA(1,1) del Módulo 1, el equivalente del suavizamiento exponencial
        simple.</p>''',
      r'''Es el IMA(1,1) del Módulo 1, el equivalente del suavizamiento exponencial
        simple con $\alpha = 1 + \hat\theta = 0.267$.</p>''')

    c("M4 · R: α del suavizamiento exponencial simple", T46,
      esc('''#>   theta      ee
#> -0.7329  0.1143
Box.test('''),
      esc('''#>   theta      ee
#> -0.7329  0.1143
# el IMA(1,1) es el suavizamiento exponencial simple, con alfa = 1 + theta
round(1 + coef(ma1)[["ma1"]], 3)
#> [1] 0.267
Box.test('''))
    c("M4 · Python: α del suavizamiento exponencial simple", T46,
      esc('''#> -0.7334
#   R da -0.7329
'''),
      esc('''#> -0.7334
#   R da -0.7329
print(round(1 + ma1.params[0], 3))
#> 0.267
'''))
