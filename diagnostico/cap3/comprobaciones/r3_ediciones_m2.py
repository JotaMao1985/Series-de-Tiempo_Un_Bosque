"""R3 · Módulo 2 · las remisiones apuntan a donde está lo que remiten; la PACF en el rezago p se
dice donde se describe la firma del AR; φ_kk en lugar de ρ_k; una sola palabra para el periodo."""


def registra(c, mover, MOD, **_):
    c("M2 · RB(0, σ²) se presenta en la definición", MOD,
      r'''        <p style="margin-bottom:0;">En forma compacta, $\phi(B)\, y_t = c + \varepsilon_t$.</p>
      </div>

      <p>El nombre lo dice todo:''',
      r'''        <p style="margin-bottom:0;">En forma compacta, $\phi(B)\, y_t = c + \varepsilon_t$. La abreviatura
          $\text{RB}(0,\sigma^2)$ es la del ruido blanco del Capítulo 2: media cero y varianza $\sigma^2$.</p>
      </div>

      <p>El nombre lo dice todo:''')

    c("M2 · la última barra de la PACF es el coeficiente, en el recuadro de la firma", MOD,
      r'''        <p style="margin-bottom:0;">Para un proceso AR($p$): $\;\phi_{kk} = 0\;$ para todo $k > p$, <strong>exactamente
            cero</strong>, no aproximadamente. Y la ACF decae hacia cero sin cortarse nunca.</p>''',
      r'''        <p style="margin-bottom:0;">Para un proceso AR($p$): $\;\phi_{kk} = 0\;$ para todo $k > p$, <strong>exactamente
            cero</strong>, no aproximadamente; y la última barra distinta de cero, la del rezago $p$, vale el propio
            coeficiente: $\phi_{pp} = \phi_p$. La ACF, en cambio, decae hacia cero sin cortarse nunca.</p>''')

    c("M2 · la serie de las manchas solares entra en el Módulo 7 (comentario tras los cuatro casos)", MOD,
      r'''        ($0.800,\,0.370,\,-0.082,\,-0.392$), cruzando el cero y volviendo. Esa oscilación es un
        <em>pseudo-ciclo</em>, y es el fenómeno que hará interesante el caso real del Módulo 9.</p>''',
      r'''        ($0.800,\,0.370,\,-0.082,\,-0.392$), cruzando el cero y volviendo. Esa oscilación es un
        <em>pseudo-ciclo</em> —su longitud, que da la fórmula de más abajo, es el <em>pseudo-periodo</em>—, y es el
        fenómeno que hará interesante el caso real de las manchas solares, que entra en el Módulo 7 y se cierra en el
        9.</p>''')

    c("M2 · el simulador del triángulo: pseudo-periodo y la remisión a las manchas solares", MOD,
      r'''          la serie desarrolla un pseudo-ciclo cuyo periodo aparece en la lectura. Prueba
          $\phi_1 = 1.40$ y $\phi_2 = -0.69$, que es —redondeado al paso del deslizador— el modelo de las manchas
          solares del Módulo 9: sale un ciclo de unos 11 periodos.</p>''',
      r'''          la serie desarrolla un pseudo-ciclo cuyo pseudo-periodo aparece en la lectura. Prueba
          $\phi_1 = 1.40$ y $\phi_2 = -0.69$, que es —redondeado al paso del deslizador— el modelo con que termina el
          caso de las manchas solares (la serie entra en el Módulo 7 y el modelo final se obtiene en el 9): sale un
          pseudo-ciclo de unos 11 periodos.</p>''')

    c("M2 · la nota de las raíces complejas llama pseudo-periodo a la longitud", MOD,
      r'''        <p><strong>Raíces complejas y ciclos.</strong> Cuando $\phi_1^2 + 4\phi_2 < 0$ las raíces son complejas
          conjugadas y la ACF oscila con un periodo medio de</p>
        $$\text{periodo} = \frac{2\pi}{\arccos\!\left(\dfrac{\phi_1}{2\sqrt{-\phi_2}}\right)}$$''',
      r'''        <p><strong>Raíces complejas y ciclos.</strong> Cuando $\phi_1^2 + 4\phi_2 < 0$ las raíces son complejas
          conjugadas y la ACF oscila con un pseudo-periodo $P$ de</p>
        $$P = \frac{2\pi}{\arccos\!\left(\dfrac{\phi_1}{2\sqrt{-\phi_2}}\right)}$$''')

    c("M2 · los intervalos de pronóstico los deduce el Capítulo 4", MOD,
      r'''la varianza para los intervalos de pronóstico del Capítulo 6, y las autocorrelaciones para identificar el''',
      r'''la varianza para los intervalos de pronóstico (que deduce el Capítulo 4), y las autocorrelaciones para identificar el''')

    c("M2 · φ_kk, no ρ_k, en el contraste de la firma", MOD,
      r'''        no llega. Ese contraste con el $\rho_k = 0$ exacto de la PACF es toda la firma del AR.</p>''',
      r'''        no llega. Ese contraste con el $\phi_{kk} = 0$ exacto de la PACF es toda la firma del AR.</p>''')

    c("M2 · el comentario del bloque R dice que la última barra es φ₂", MOD,
      r'''#   la PACF se corta EXACTAMENTE en el rezago p = 2

# Comprobacion de la formula de Yule-Walker para el AR(2)''',
      r'''#   la PACF se corta EXACTAMENTE en el rezago p = 2, y su ultima barra, 0.3000, es phi_2

# Comprobacion de la formula de Yule-Walker para el AR(2)''')
