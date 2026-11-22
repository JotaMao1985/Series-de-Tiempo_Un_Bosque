#!/usr/bin/env python3
"""R5 del capítulo 3 · T5.2: los ejercicios 1, 2 y 3 del Módulo 10.

No se ejecuta solo: lo importa `r5_edita.py`.

Los seis fragmentos con `data-afirma` de los ejercicios (c3-m10-31, -33, -90, -34, -46 y -35)
llevan firma de la R4 y NO se reescriben: se copian byte a byte del archivo de partida
(`marcado()`), y lo que cambia es la prosa de alrededor. El código de los ejercicios 1 y 2 se
lee de `r5_bloques/e1.out` y `e2.out` (salida de `r5_reprex.R`); el del 3 no se toca.
"""
import re

from r5_ediciones_cortos import codigo


def marcado(src, ident):
    """El elemento `<span data-afirma="ident">…</span>` tal como está en el archivo de partida."""
    ini = src.index(f'<span data-afirma="{ident}">')
    fin = src.index("</span>", src.index("</cite>", ini)) + len("</span>")
    trozo = src[ini:fin]
    assert trozo.count("<span") == trozo.count("</span>"), ident
    return trozo


def entre(src, ini_txt, fin_txt, desde=0):
    """(inicio, fin) del tramo que empieza en `ini_txt` y termina justo antes de `fin_txt`."""
    a = src.index(ini_txt, desde)
    b = src.index(fin_txt, a)
    assert src.count(ini_txt) == 1, f"no es único: {ini_txt[:60]!r}"
    return a, b


def uno(src, antes, despues):
    assert src.count(antes) == 1, f"{src.count(antes)} veces: {antes[:70]!r}"
    return src.replace(antes, despues)


def aplica(src):
    # ------------------------------------------------------------------ Ejercicio 1
    # Pista sin el resultado («aquí no lo hacen»), n -> T, y la discusión con los criterios de
    # «Qué confirma el orden elegido». Cifras: bloque e1; [E1-01], [E1-02].
    a, b = entre(src, '        <div class="ejercicio-panel pista" id="c3e1-pista" hidden>',
                 '        <p class="ejercicio-enunciado"><span class="ejercicio-numero">2.</span>')
    m33, m90 = marcado(src, "c3-m10-33"), marcado(src, "c3-m10-90")
    e1 = f'''        <div class="ejercicio-panel pista" id="c3e1-pista" hidden>
          <p style="margin:0;">Con $T = 48$ la banda es ancha: calcúlala antes de mirar los correlogramas y
            cuenta cuántas barras salen de verdad, sin fiarte de las que quedan en el borde. Ajusta más de un
            candidato y, antes de elegir, pon los dos criterios uno al lado del otro y comprueba cuáles pasan
            Ljung–Box. Si los criterios no coinciden, la lista «Qué confirma el orden elegido» de este módulo
            dice qué más mirar.</p>
        </div>
        <div class="ejercicio-panel solucion" id="c3e1-sol" hidden>
          <p><strong>Respuesta: el AICc elige MA(2) y el BIC elige AR(1), por muy poco, y los dos son
              defendibles.</strong></p>
          <pre><code class="language-r">{codigo("e1")}</code></pre>
          <p><strong>Discusión.</strong> Los dos modelos pasan Ljung–Box con holgura ($p = 0.405$ y $0.849$), así
            que ninguno es inadmisible. El AICc prefiere el MA(2) ($63.99$ frente a $65.30$) y el BIC prefiere el
            AR(1) ($70.37$ frente a $70.55$, una diferencia de $0.17$ que no distingue nada). Con $T = 48$ esta
            indeterminación no sorprende.</p>
          <p>La lista «Qué confirma el orden elegido» de este módulo tampoco desempata, pero dice qué pesa en
            cada lado. A favor del MA(2): su coeficiente de mayor orden es significativo
            ($\\hat\\theta_2 = 0.375$, $t = 2.91$) y su ACF teórica se parece más a la muestral en el rezago 2
            ($0.235$ frente a $r_2 = 0.182$; la del AR(1) da $0.329$). A favor del AR(1): la parsimonia —un
            coeficiente en vez de dos— y una lectura directa ($\\hat\\phi = 0.574$: cada medición conserva el
            57 % de la desviación de la anterior respecto a la media). La búsqueda automática refleja la misma
            indecisión: <code>auto.arima(lh)</code> devuelve el AR(1) con la búsqueda por pasos y el MA(2) con la
            exhaustiva. Quien busque identificar el proceso tiene motivos para quedarse con el AR(1), que es
            lo que elige el BIC; quien busque pronosticar, con el MA(2), que es lo que elige el AICc. Lo que no
            vale es elegir sin decir por qué.</p>
          <p style="margin-bottom:0;">Si el objetivo fuera pronosticar, {m33}, que es lo que hará el Capítulo 6. Nota final: la normalidad de los
            residuales se rechaza en los dos ($p = 0.0083$ en el AR(1) y $0.0264$ en el MA(2)), {m90}.</p>
        </div>
      </div>

      <div class="ejercicio-guiado">
'''
    src = src[:a] + e1 + src[b:]

    # ------------------------------------------------------------------ Ejercicio 2
    # Otro MA(2): theta = (0.9, 0.2) en lugar de (0.6, 0.4), que era una opción del simulador del
    # Módulo 3 y lo que daba la retro de la pregunta 3. Apartado nuevo: el MA(2) con una raíz
    # invertida, que el Módulo 3 no resuelve. Cifras: bloque e2; [E2-01] a [E2-04].
    a, b = entre(src, '        <p class="ejercicio-enunciado"><span class="ejercicio-numero">2.</span>',
                 '        <p class="ejercicio-enunciado"><span class="ejercicio-numero">3.</span>')
    m34 = marcado(src, "c3-m10-34")
    e2 = f'''        <p class="ejercicio-enunciado" style="margin-bottom: 0.75rem;"><span class="ejercicio-numero">2.</span>Considera el proceso
          MA(2) con $\\theta = (0.9,\\ 0.2)$. Entrega:</p>
        <ol style="list-style-type: lower-alpha; margin-top: 0.5rem; margin-bottom: 0;">
          <li>¿Es invertible? Compruébalo de dos maneras: con el triángulo del Módulo 3 y con las raíces de
            $\\theta(B)$.</li>
          <li>Su ACF teórica, a mano y con <code>ARMAacf()</code>. ¿Se cumple aquí la cota $|\\rho_1| \\le 0.5$
            del Módulo 3?</li>
          <li>La ACF del MA(2) con $\\theta = (2.4,\\ 0.8)$. Compárala con la anterior y explica el resultado
            factorizando los dos polinomios.</li>
        </ol>
        <div class="ejercicio-acciones">
          <button type="button" class="ejercicio-boton" aria-expanded="false" aria-controls="c3e2-pista">
            <i class="fas fa-lightbulb" aria-hidden="true"></i> Pista <i class="fas fa-chevron-down" aria-hidden="true"></i>
          </button>
          <button type="button" class="ejercicio-boton" aria-expanded="false" aria-controls="c3e2-sol">
            <i class="fas fa-key" aria-hidden="true"></i> Solución <i class="fas fa-chevron-down" aria-hidden="true"></i>
          </button>
        </div>
        <div class="ejercicio-panel pista" id="c3e2-pista" hidden>
          <p style="margin:0;">Para la ACF usa la fórmula general del MA($q$) con el convenio $\\theta_0 = 1$, y
            cuenta cuántos sumandos tiene el numerador en cada rezago. Sobre la cota, relee de dónde salía. Para
            el tercer apartado, escribe $1 + 0.9B + 0.2B^2$ como producto de dos factores de primer grado, haz lo
            mismo con $1 + 2.4B + 0.8B^2$ y mira en qué se diferencian.</p>
        </div>
        <div class="ejercicio-panel solucion" id="c3e2-sol" hidden>
          <p><strong>Respuesta: es invertible, $\\rho_1 = 0.5838$ y $\\rho_2 = 0.1081$, la cota <em>no</em> se
              cumple porque no era aplicable, y el segundo MA(2) tiene exactamente la misma ACF sin ser
              invertible.</strong></p>
          <pre><code class="language-r">{codigo("e2")}</code></pre>
          <p><strong>Invertibilidad.</strong> Por el triángulo: $\\theta_1 + \\theta_2 = 1.1 > -1$,
            $\\theta_2 - \\theta_1 = -0.7 > -1$ y $|\\theta_2| = 0.2 < 1$. Por las raíces:
            $\\theta(B) = (1 + 0.5B)(1 + 0.4B)$ se anula en $B = -2$ y en $B = -2.5$, las dos fuera del círculo
            unitario.</p>
          <p><strong>Sobre la cota.</strong> $\\rho_1 = (0.9 + 0.18)/1.85 = 0.5838 > 0.5$. No hay contradicción: {m34}. Con
            $q = 2$ el numerador de $\\rho_1$ gana el término extra $\\theta_1\\theta_2$ y el techo sube. Es un buen
            recordatorio de que una cota vale exactamente en el modelo del que se dedujo: ver $r_1 = 0.58$ pone en duda un MA(1), <strong>no</strong> un MA(2).</p>
          <p style="margin-bottom:0;"><strong>El otro MA(2).</strong> $1 + 2.4B + 0.8B^2 = (1 + 2B)(1 + 0.4B)$: es
            el polinomio anterior con el factor $(1 + 0.5B)$ cambiado por $(1 + 2B)$, es decir, con la raíz $-2$
            sustituida por su inversa, $-0.5$, que cae dentro del círculo. Es lo que el Módulo 3 hacía con
            $\\theta$ y $1/\\theta$ en el MA(1), aplicado a uno solo de los dos factores: la ACF no cambia
            ($0.5838$ y $0.1081$ otra vez) y el modelo deja de ser invertible. Invirtiendo la otra raíz, o las
            dos, salen otros dos MA(2) con esa misma ACF: cuatro en total, y solo uno invertible. Es el que
            <code>arima()</code> devuelve por defecto: simulados 2000 valores con $\\theta = (2.4,\\ 0.8)$ y
            $\\sigma^2 = 1$, el ajuste da $\\hat\\theta = (0.904,\\ 0.230)$ y $\\hat\\sigma^2 = 4.035$, unas cuatro
            veces la varianza del ruido simulado, como ocurría en el MA(1) con $\\theta = 2$.</p>
        </div>
      </div>

      <div class="ejercicio-guiado">
'''
    src = src[:a] + e2 + src[b:]

    # ------------------------------------------------------------------ Ejercicio 3
    # El enunciado pide ya las ventanas que la solución usa (la R1 añadió 1889-1988) y pregunta
    # por el tamaño de la muestra; la pista deja de adelantar los tres resultados; «periodo» ->
    # «pseudo-periodo» fuera de lo marcado. El código y los elementos c3-m10-46 y c3-m10-35 no cambian.
    src = uno(src,
              '''        <p class="ejercicio-enunciado"><span class="ejercicio-numero">3.</span>El Módulo 9 ajustó un AR(2) a
          $\\sqrt{\\text{manchas}}$ sobre la ventana 1770–1869. Repite el ajuste sobre la serie completa
          (1700–1988) y sobre 1900–1988. ¿Son estables los coeficientes? ¿Y el pseudo-periodo? ¿Sigue pasando
          el diagnóstico?</p>
''',
              '''        <p class="ejercicio-enunciado" style="margin-bottom: 0.75rem;"><span class="ejercicio-numero">3.</span>El Módulo 9 ajustó un AR(2) a
          $\\sqrt{\\text{manchas}}$ sobre la ventana 1770–1869. Repite el ajuste sobre la serie completa
          (1700–1988) y sobre tres tramos que llegan al siglo XX: 1870–1988, 1900–1988 y 1889–1988, que tiene
          los mismos cien años que la ventana del módulo. Entrega tres lecturas, por separado:</p>
        <ol style="list-style-type: lower-alpha; margin-top: 0.5rem; margin-bottom: 0;">
          <li>¿Son estables los coeficientes $\\hat\\phi_1$ y $\\hat\\phi_2$ de una ventana a otra?</li>
          <li>¿Lo es el pseudo-periodo?</li>
          <li>¿Sigue pasando el modelo Ljung–Box en el rezago 12? Si el veredicto cambia, ¿lo explica el número
            de datos de la ventana?</li>
        </ol>
''')
    src = uno(src,
              '''          <p style="margin:0;">Mira <strong>tres</strong> cosas por separado y no las confundas: los coeficientes
            $\\hat\\phi$, la cantidad derivada de ellos (el periodo) y el diagnóstico. Puede pasar perfectamente que los
            coeficientes apenas se muevan, que el periodo sí lo haga y que el diagnóstico se derrumbe. Antes de
            atribuir un cambio del Ljung–Box al tamaño de la muestra, compara ventanas del mismo tamaño: 1889–1988
            tiene cien años, igual que 1770–1869.</p>
''',
              '''          <p style="margin:0;">Son tres cosas distintas —los coeficientes, una cantidad que se deriva de ellos
            y el diagnóstico— y cada una puede comportarse a su manera: anótalas en tres columnas, con una fila
            por ventana. Antes de atribuir un cambio de veredicto al tamaño de la muestra, compara ventanas con
            la misma cantidad de años.</p>
''')
    src = uno(src,
              "<p><strong>Respuesta: los coeficientes son notablemente estables, el periodo se acorta un año y el",
              "<p><strong>Respuesta: los coeficientes son notablemente estables, el pseudo-periodo se acorta un año y el")
    src = uno(src,
              "<li><strong>El periodo sí se mueve:</strong> de $11.22$ años (1770–1869) a $10.13$ (1900–1988).",
              "<li><strong>El pseudo-periodo sí se mueve:</strong> de $11.22$ años (1770–1869) a $10.13$ (1900–1988).")
    return src
