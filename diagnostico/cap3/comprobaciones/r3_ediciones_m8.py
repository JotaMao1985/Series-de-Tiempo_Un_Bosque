"""R3 · Módulo 8 · el porqué de `fitdf` y el Monte Carlo salen del plegado y se dicen a la vista; el
código ya no cita «el paso 4»; T, no n, en los criterios y en el pie de la tabla ordenable."""


def registra(c, mover, MOD, JS, **_):
    c("M8 · AIC, AICc y BIC con T, la longitud de la serie", MOD,
      r'''          \text{AICc} &= \text{AIC} + \frac{2k(k+1)}{n-k-1} \\[0.3em]
          \text{BIC} &= -2\log L + k\log n
        \end{aligned}$$
        <p style="margin-bottom:0;">donde $k$ es el número de parámetros estimados —incluido $\sigma^2$— y $n$ el
          número de observaciones.</p>''',
      r'''          \text{AICc} &= \text{AIC} + \frac{2k(k+1)}{T-k-1} \\[0.3em]
          \text{BIC} &= -2\log L + k\log T
        \end{aligned}$$
        <p style="margin-bottom:0;">donde $k$ es el número de parámetros estimados —incluido $\sigma^2$— y $T$ el
          número de observaciones.</p>''')

    c("M8 · «cuál usar» con T", MOD,
      r'''<p><strong>Cuál usar.</strong> El AICc corrige el sesgo del AIC en muestras pequeñas y converge a él cuando
          $n$ crece, así que <strong>no hay razón para preferir el AIC</strong>. El BIC penaliza más
          ($\log n > 2$ en cuanto $n > 7$) y por eso tiende a elegir modelos más pequeños.''',
      r'''<p><strong>Cuál usar.</strong> El AICc corrige el sesgo del AIC en muestras pequeñas y converge a él cuando
          $T$ crece, así que <strong>no hay razón para preferir el AIC</strong>. El BIC penaliza más
          ($\log T > 2$ en cuanto $T > 7$) y por eso tiende a elegir modelos más pequeños.''')

    c("M8 · la trampa del Capítulo 4 con T", MOD,
      r'''ajusta sobre $n-1$ observaciones distintas de las del modelo con $d=0$.''',
      r'''ajusta sobre $T-1$ observaciones distintas de las del modelo con $d=0$.''')

    c("M8 · por qué Ljung–Box lleva fitdf, a la vista y antes del plegado", MOD,
      r'''          significa que <strong>queda estructura sin modelar</strong>: el modelo no basta.</p>
      </div>

      <div class="derivacion">''',
      r'''          significa que <strong>queda estructura sin modelar</strong>: el modelo no basta.</p>
      </div>

      <p>Los grados de libertad son $h-p-q$ y no $h$ porque los residuales no son ruido blanco observado, sino lo que
        queda tras estimar $p+q$ parámetros, y esa estimación los deja menos correlacionados de lo que estarían por
        azar. Si no se descuentan, la prueba rechaza menos de lo que debería. En R el descuento es el argumento
        <code>fitdf = p + q</code> de <code>Box.test()</code>, que <strong>no</strong> se aplica solo, y solo tiene
        sentido evaluar en $h > p+q$. El efecto se mide en el último bloque de código de este módulo: con tres mil
        series que de verdad son AR(2), $T = 100$ y $h = 12$, la prueba al 5&nbsp;% rechaza el $4.9$&nbsp;% de las
        veces con <code>fitdf = 2</code> y solo el $2.6$&nbsp;% sin él.</p>

      <div class="derivacion">''')

    c("M8 · la rejilla es una elección del capítulo, no un resultado de la lectura de los correlogramas", MOD,
      r'''# La rejilla no es un producto cartesiano: son ordenes bajos en las dos partes
# mas dos AR largos. Es lo que justifica la lectura de los correlogramas, y son
# los once candidatos de la tabla ordenable de arriba.''',
      r'''# La rejilla no es un producto cartesiano: son ordenes bajos en las dos partes
# mas dos AR largos. Es una eleccion de este capitulo, no un resultado de la
# lectura de los correlogramas, y son los once candidatos de la tabla ordenable
# de arriba.''')

    c("M8 · el comentario del Monte Carlo ya no cita «el paso 4 del desarrollo»", MOD,
      r'''# El paso 4 del desarrollo: sin fitdf la prueba rechaza la mitad de lo debido''',
      r'''# Sin fitdf la prueba rechaza la mitad de lo debido: 3000 series AR(2), T = 100, h = 12''')

    c("M8 · el pie de la tabla ordenable: el mismo T", JS,
      r'''          'Los once comparten $d = 0$ y el mismo $n$, así que sus criterios son ' +''',
      r'''          'Los once comparten $d = 0$ y el mismo $T$, así que sus criterios son ' +''')
