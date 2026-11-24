"""R3 · Módulo 2 (5.2 Notación SARIMA y el polinomio multiplicativo).

D6: el airline ajustado se muestra antes de usarse. «Cómo se escribe en la práctica» (el bloque que
ajusta el airline e imprime θ̂, Θ̂, σ̂² y B13) pasa de ser la última sección a ir justo después de la
definición; la derivación plegada que usa θ̂ y Θ̂ y la nota que usa σ̂² quedan después. El módulo
cierra apuntando al 3.
T3.2: el satélite se explica una vez bien (la heladería); la primera viñeta, la apertura de
«Multiplicar no es sumar» y el paso 4 de su desarrollo dejan de repetirlo y remiten. La remisión
falsa al Módulo 6 en un comentario del bloque de momentos (el divisor de σ̂²) se corrige."""


def registra(c, mover, entre, despues, esc, T13, **_):
    # ------------------------------------------------------------ «Cómo se escribe», al principio
    c("M2 · «Cómo se escribe en la práctica» gana un párrafo que dice qué trae y para qué", T13,
      r'''      <h3>Cómo se escribe en la práctica</h3>

      <div class="code-tabs">''',
      r'''      <h3>Cómo se escribe en la práctica</h3>

      <p>Antes de los ejemplos, cómo se pide un SARIMA en R y en Python, con el modelo que recorre todo el capítulo:
        el <em>airline</em>, SARIMA($0,1,1$)($0,1,1$)$_{12}$, ajustado a $\log(\text{AirPassengers})$; el Módulo 5
        lo estudia con su nombre. El bloque da sus dos coeficientes, $\hat\theta$ y $\hat\Theta$, y la varianza de
        sus innovaciones, $\hat\sigma^2$, que el resto del módulo usa. Que el coeficiente del rezago $13$ salga del
        producto, sin estimarse, es lo que explica el ejemplo siguiente.</p>

      <div class="code-tabs">''')
    c("M2 · el bloque imprime σ̂² (la nota del airline exacto lo usa)", T13,
      esc('''#>       -0.4018  -0.5569
#> s.e.   0.0896   0.0731

# Que la parte estacional MULTIPLICA'''),
      esc('''#>       -0.4018  -0.5569
#> s.e.   0.0896   0.0731
round(fit$sigma2, 6)                    # varianza de las innovaciones
#> [1] 0.001371

# Que la parte estacional MULTIPLICA'''))
    mover("M2 · «Cómo se escribe en la práctica» pasa tras la definición", T13,
          '      <h3>Cómo se escribe en la práctica</h3>',
          '    </div>\n  </template>\n\n  <template id="module-3">',
          '      <h3>Un ejemplo para seguir a mano: pronosticar un mes</h3>')
    despues("M2 · línea en blanco entre el bloque trasladado y el ejemplo", T13,
            '      </div>\n      <h3>Un ejemplo para seguir a mano: pronosticar un mes</h3>',
            '      </div>\n\n      <h3>Un ejemplo para seguir a mano: pronosticar un mes</h3>')

    c("M2 · la derivación del airline remite al bloque, que ya está arriba", T13,
      r'''                <code>B13</code> que imprime el bloque de «Cómo se escribe en la práctica»: no se estima, sale del
                producto.</p>''',
      r'''                <code>B13</code> que imprime el bloque de «Cómo se escribe en la práctica», al principio del módulo:
                no se estima, sale del producto.</p>''')

    # ------------------------------------------------------------ el satélite, una vez
    c("M2 · primera viñeta: sin repetir el peso del satélite", T13,
      r'''        <li><strong>El rezago 13 no es un parámetro nuevo.</strong> Su peso, $-\phi\Phi$, sale de los otros dos: el
          modelo toca tres meses con solo dos parámetros. Es el «AR($13$) con dos parámetros libres» del desarrollo
          de más abajo.</li>''',
      r'''        <li><strong>El rezago 13 no es un parámetro nuevo:</strong> el modelo toca tres meses con dos parámetros. El
          desarrollo de la sección siguiente hace la misma cuenta con letras.</li>''')
    c("M2 · «Multiplicar no es sumar»: remite a la heladería en vez de repetirla", T13,
      r'''      <p>La sección siguiente generaliza la cuenta a cualquier par de órdenes y la escribe para todo el
        polinomio.</p>

      <h3>Multiplicar no es sumar: los rezagos satélite</h3>

      <p>Aquí está lo único genuinamente nuevo. Si en vez de multiplicar los polinomios se sumaran los términos, un
        modelo con $p = 1$ y $P = 1$ tocaría los rezagos $1$ y $12$, y nada más. Al multiplicarlos aparece un término
        cruzado en el rezago $13$ que <strong>nadie ha puesto ahí</strong>: sale solo, y con un coeficiente que no es
        libre, sino el producto de los otros dos.</p>''',
      r'''      <h3>Multiplicar no es sumar: los rezagos satélite</h3>

      <p>El satélite es lo único genuinamente nuevo del SARIMA, y la heladería ya lo mostró con números: si los dos
        modelos se sumaran, uno con $p = 1$ y $P = 1$ tocaría solo los rezagos $1$ y $12$; al multiplicarlos aparece
        el $13$, con un coeficiente atado a los otros dos. El desarrollo siguiente repite la cuenta con letras, para
        cualquier $\phi$ y $\Phi$, y el constructor de más abajo la hace con cualquier orden.</p>''')
    c("M2 · paso 4 del desarrollo: la ACF de la heladería, sin repetir sus cifras", T13,
      r'''              <p>Con $\phi = 0.6$ y $\Phi = 0.7$, la ACF teórica vale $\rho_1 = 0.6016$, $\rho_{12} = 0.7011$ y —esto
                es lo que hay que reconocer en un correlograma real— $\rho_{11} = 0.4230$ y $\rho_{13} = 0.4218$,
                aproximadamente $\rho_1 \cdot \rho_{12}$.</p>''',
      r'''              <p>Con $\phi = 0.6$ y $\Phi = 0.7$ es la heladería, y su ACF es la de la tercera viñeta de arriba:
                picos en $1$ y $12$, y en $11$ y $13$ dos satélites que valen aproximadamente $\rho_1 \cdot \rho_{12}$.
                Eso es lo que hay que reconocer en un correlograma real.</p>''')

    # ------------------------------------------------------------ remisión falsa en un comentario
    c("M2 · Python de momentos: el divisor de σ̂² no es lo que el Módulo 6 discute", T13,
      esc('''# MISMA varianza teorica. No es un error de ninguno de los dos: es el mismo
# reparto de grados de libertad que el Modulo 6 discute para el AIC.'''),
      esc('''# MISMA varianza teorica. No es un error de ninguno de los dos: es un
# convenio distinto para el divisor de sigma2.'''))

    # ------------------------------------------------------------ cierre
    despues("M2 · cierre que apunta al Módulo 3", T13,
            '\n\n    </div>\n  </template>\n\n  <template id="module-3">',
            '''

      <p>Lo que este módulo deja montado es el modelo escrito y su lectura: dos polinomios que se multiplican,
        satélites que no cuestan parámetros y momentos que se calculan sobre la serie ya diferenciada. Falta decidir
        cuántas diferencias lleva —el $(1-B)^d$ y el $(1-B^m)^D$ de la definición— y en qué orden: es el
        Módulo 3.</p>
    </div>
  </template>

  <template id="module-3">''')
