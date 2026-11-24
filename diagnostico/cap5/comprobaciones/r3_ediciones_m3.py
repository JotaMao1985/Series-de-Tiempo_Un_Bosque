"""R3 · Módulo 3 (5.3 Diferenciación estacional).

D6: la introducción de `cuatro-combinaciones` dice el estado inicial (las dos diferencias encendidas)
y deja de adelantar el resultado (el 0.841 está en la tabla y en el párrafo de después); la «Trampa
de versión» tiene ya su bloque (`nsdiffs` con «seas» y con «ocsb» sobre las dos series); el módulo
cierra apuntando al 4."""


def registra(c, mover, entre, despues, esc, T13, **_):
    c("M3 · intro de cuatro-combinaciones: estado inicial y una pregunta, sin el resultado", T13,
      r'''        <p class="simulador-intro">Los dos interruptores dan las cuatro combinaciones. Mira sobre todo la
          <strong>ACF en el rezago 12</strong>: con solo la diferencia regular baja de $0.762$ a… $0.841$, es decir
          <em>sube</em>. Diferenciar de forma regular no toca la estacionalidad; concentrarla es incluso más fácil de
          ver después.</p>''',
      r'''        <p class="simulador-intro">Los dos interruptores dan las cuatro combinaciones; se abre con los dos
          encendidos. Mira sobre todo la <strong>ACF en el rezago 12</strong>: apaga los dos para ver la serie sin
          diferenciar, con $\hat\rho_{12} = 0.762$, y enciende después solo la diferencia regular. ¿Baja
          $\hat\rho_{12}$, como bajaría si fuera solo tendencia, o no?</p>''')

    c("M3 · R: nsdiffs con las dos pruebas, la de la «Trampa de versión»", T13,
      esc('''# |raiz MA|^-1 = |Theta|^(1/12) comprime la escala hacia 1 y separa mal; Theta no.''') + '</code></pre>',
      esc('''# |raiz MA|^-1 = |Theta|^(1/12) comprime la escala hacia 1 y separa mal; Theta no.

# --- Trampa de version: que prueba usa nsdiffs() importa -------------------
sapply(list(ap = ap, uad = uad), function(x)
  c(seas = nsdiffs(x), ocsb = nsdiffs(x, test = "ocsb")))
#>      ap uad
#> seas  1   1
#> ocsb  0   0''') + '</code></pre>')

    c("M3 · la «Trampa de versión» remite al bloque y el módulo cierra apuntando al 4", T13,
      r'''          <code>"ocsb"</code> devuelve $0$. Es la misma clase de trampa que la de <code>ndiffs()</code> y
          <code>kpss.test()</code> del Capítulo 2: <strong>al comparar dos salidas, mira primero qué prueba usa
          cada una</strong>. Aquí manda la evidencia del correlograma, no el número que devuelve la función.</p>
      </div>''',
      r'''          <code>"ocsb"</code> devuelve $0$ (el bloque de arriba imprime las dos). Es la misma clase de trampa que la
          de <code>ndiffs()</code> y <code>kpss.test()</code> del Capítulo 2: <strong>al comparar dos salidas, mira
          primero qué prueba usa cada una</strong>. Aquí manda la evidencia del correlograma, no el número que
          devuelve la función.</p>
      </div>

      <p>Con $D$ y $d$ decididos queda una serie estacionaria, que se identifica como cualquier ARMA con una
        salvedad: los órdenes estacionales se leen en los rezagos $m, 2m, 3m$. Es el Módulo 4.</p>''')
