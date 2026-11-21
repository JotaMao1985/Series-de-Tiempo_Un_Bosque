"""R3 · Módulo 7 · lo que el código citaba del plegado («el paso 6») se dice a la vista; T, no n."""


def registra(c, mover, MOD, **_):
    c("M7 · T, no n, para la longitud de la serie de manchas solares", MOD,
      r'''1869</strong>, $n = 100$ observaciones.''',
      r'''1869</strong>, $T = 100$ observaciones.''')

    c("M7 · por qué CSS y ML difieren, a la vista y antes del plegado", MOD,
      r'''            fiables.</li>
        </ul>
      </div>

      <div class="derivacion">
        <button type="button" class="derivacion-boton" aria-expanded="false" aria-controls="der-verosimilitud">''',
      r'''            fiables.</li>
        </ul>
      </div>

      <p>Entre CSS y máxima verosimilitud la diferencia está en la primera observación: ML incluye su densidad y CSS la
        ignora, y ese término <strong>penaliza</strong> los $\phi$ cercanos a la frontera de la región estacionaria. Con
        $T$ grande pesa poco y los dos métodos coinciden; con $T$ pequeño o $\phi$ cerca de $1$, no, y CSS puede incluso
        salirse de la región estacionaria, cosa que ML no hace en el ejemplo. El último bloque de código de abajo lo
        reproduce con $T = 40$ y $\phi = 0.95$, y el desarrollo plegado deduce el término.</p>

      <div class="derivacion">
        <button type="button" class="derivacion-boton" aria-expanded="false" aria-controls="der-verosimilitud">''')

    c("M7 · el comentario del bloque R ya no cita «el paso 6 del desarrollo»", MOD,
      r'''# El paso 6 del desarrollo: CSS puede salirse de la region estacionaria''',
      r'''# Una serie corta con phi cerca de 1 (T = 40, phi = 0.95): CSS puede salirse de la
# region estacionaria; ML, no''')

    c("M7 · el comentario del bloque R: T, no n", MOD,
      r'''window(sunspot.year, start = 1770, end = 1869)   # n = 100''',
      r'''window(sunspot.year, start = 1770, end = 1869)   # T = 100''')

    c("M7 · el aviso de Yule–Walker: divisores T−k y T", MOD,
      r'''por defecto <code>method="adjusted"</code> (divisor $n-k$) y <code>ar()</code> de R usa el divisor $n$. Con''',
      r'''por defecto <code>method="adjusted"</code> (divisor $T-k$) y <code>ar()</code> de R usa el divisor $T$. Con''')
