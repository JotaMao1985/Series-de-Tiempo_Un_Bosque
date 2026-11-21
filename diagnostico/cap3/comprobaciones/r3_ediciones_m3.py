"""R3 · Módulo 3 · «invertible» se dice antes de usarse; «identificable» y «identificación» dejan de
compartir sentido; θ = −1 se conecta con la sobrediferenciación que prometió el Capítulo 2."""


def registra(c, mover, MOD, **_):
    c("M3 · el significado de «invertible» sale del plegado y precede al simulador; «identificable»", MOD,
      r'''        producen exactamente las mismas autocovarianzas —y, con ruido gaussiano, la misma distribución—, y como
        $\sigma^2$ también se estima, ningún dato puede separarlos. Si no se impone una regla, el modelo no está
        identificado.</p>''',
      r'''        producen exactamente las mismas autocovarianzas —y, con ruido gaussiano, la misma distribución—, y como
        $\sigma^2$ también se estima, ningún dato puede separarlos: el parámetro $\theta$ no es <em>identificable</em>
        (no hay que confundirlo con la <em>identificación</em> del Módulo 5, que consiste en proponer los órdenes $p$ y
        $q$). Hace falta una regla que elija uno de los dos, y se elige el de $|\theta| < 1$, que se llama
        <strong>invertible</strong>: es el único con el que se puede reconstruir cada choque a partir de lo observado,
        como muestra el final del módulo.</p>''')

    c("M3 · la sobrediferenciación del Capítulo 2 es el caso θ = −1", MOD,
      r'''          están fuera del círculo unitario. Es la misma condición que la estacionariedad del AR, aplicada al otro
          polinomio.</p>
      </div>
''',
      r'''          están fuera del círculo unitario. Es la misma condición que la estacionariedad del AR, aplicada al otro
          polinomio.</p>
      </div>

      <p>El caso frontera, $|\theta| = 1$, ya apareció en el Capítulo 2. Allí, diferenciar un ruido blanco
        —sobrediferenciarlo— daba $\nabla\varepsilon_t = \varepsilon_t - \varepsilon_{t-1}$, que es un MA(1) con
        $\theta = -1$: su raíz, la de $1 - B$, cae justo sobre el círculo unitario, así que no es invertible, y su
        $\rho_1 = \theta/(1+\theta^2)$ vale $-0.5$, el mínimo que un MA(1) puede alcanzar. Es el $-0.5$ que el
        Capítulo 2 daba como indicio de sobrediferenciación, y es el punto que el simulador de arriba marca como
        «frontera».</p>
''')

    c("M3 · el comentario del bloque R: θ no es identificable", MOD,
      r'''#&gt; [1] 0.4 0.0 0.0     <- identicas: el modelo no esta identificado''',
      r'''#&gt; [1] 0.4 0.0 0.0     <- identicas: theta no es identificable''')

    c("M3 · bloque R: θ = −1, la sobrediferenciación", MOD,
      r'''#&gt; [1] 0.5

# arima() devuelve siempre la version invertible''',
      r'''#&gt; [1] 0.5

# Sobrediferenciar un ruido blanco (Capitulo 2) da un MA(1) con theta = -1:
# rho_1 = -0.5, y la raiz de 1 - B cae justo SOBRE el circulo (frontera)
round(ARMAacf(ma = -1, lag.max = 3)[-1], 4)
#&gt;    1    2    3
#&gt; -0.5  0.0  0.0
Mod(polyroot(c(1, -1)))
#&gt; [1] 1

# arima() devuelve siempre la version invertible''')

    c("M3 · bloque Python: θ = −1, la sobrediferenciación", MOD,
      r'''print(np.max(np.abs(th / (1 + th**2))))   # 0.5

# statsmodels tambien devuelve la version invertible, con sigma2 reescalado''',
      r'''print(np.max(np.abs(th / (1 + th**2))))   # 0.5

# Sobrediferenciar un ruido blanco (Capitulo 2): theta = -1, rho_1 = -0.5 y la
# raiz de 1 - B cae justo SOBRE el circulo (frontera)
print(np.round(arma_acf(np.r_[1], np.r_[1, -1.0], lags=4)[1:], 4))   # [-0.5  0.   0. ]
print(np.abs(ArmaProcess(np.r_[1], np.r_[1, -1.0]).maroots))          # [1.]

# statsmodels tambien devuelve la version invertible, con sigma2 reescalado''')

    c("M3 · el ARMA se nombra con una frase al remitir al Módulo 4", MOD,
      r'''      <p>El Módulo 4 generaliza esta reescritura a cualquier ARMA, y la recorre también en el sentido contrario.</p>''',
      r'''      <p>El Módulo 4 generaliza esta reescritura a cualquier ARMA —el modelo que combina un AR y un MA—, y la
        recorre también en el sentido contrario.</p>''')
