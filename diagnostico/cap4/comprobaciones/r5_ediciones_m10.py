#!/usr/bin/env python3
"""R5 del capítulo 4 · T5.2: los ejercicios 1, 2 y 3 del Módulo 10 y las dos frases de M8 y M9 que los resolvían.

No se ejecuta solo: lo importa `r5_edita.py`.

Las frases con `data-afirma` (firma de la R4) NO se reescriben: `marca(texto, id)` copia el elemento
entero, byte a byte, del archivo de partida, y lo que cambia es la prosa de alrededor. El ejercicio 2
cambia de serie (`log(pelt$Hare)` en lugar de `log(lynx)`); sus siete elementos marcados —tres de ellos
hablan del lince— se conservan: los generales pasan a la discusión de la liebre y los del lince a un
párrafo final de la solución, «El mismo patrón en otra serie», con su bloque (`r5_bloques/e2b`).
"""
import re
from r5_ediciones_cortos import codigo


def marca(texto, ident):
    """El elemento `<span data-afirma="ident">…</span>` del archivo de partida, entero."""
    i = texto.index(f'<span data-afirma="{ident}">')
    j, nivel = i, 0
    for m in re.finditer(r"<span\b|</span>", texto[i:]):
        nivel += 1 if m.group() != "</span>" else -1
        if nivel == 0:
            j = i + m.end()
            break
    assert j > i, ident
    return texto[i:j]


def reemplaza(texto, viejo, nuevo, etiqueta):
    assert texto.count(viejo) == 1, (etiqueta, texto.count(viejo))
    return texto.replace(viejo, nuevo)


def panel(k, pista, solucion):
    return f'''        <div class="ejercicio-acciones">
          <button type="button" class="ejercicio-boton" aria-expanded="false" aria-controls="c4e{k}-pista">
            <i class="fas fa-lightbulb" aria-hidden="true"></i> Pista <i class="fas fa-chevron-down" aria-hidden="true"></i>
          </button>
          <button type="button" class="ejercicio-boton" aria-expanded="false" aria-controls="c4e{k}-sol">
            <i class="fas fa-key" aria-hidden="true"></i> Solución <i class="fas fa-chevron-down" aria-hidden="true"></i>
          </button>
        </div>
        <div class="ejercicio-panel pista" id="c4e{k}-pista" hidden>
          <p style="margin:0;">{pista}</p>
        </div>
        <div class="ejercicio-panel solucion" id="c4e{k}-sol" hidden>
{solucion}
        </div>
      </div>
'''


def cabeza(k, enunciado, entregables):
    items = "\n".join(f"          <li>{e}</li>" for e in entregables)
    return f'''      <div class="ejercicio-guiado">
        <p class="ejercicio-enunciado" style="margin-bottom: 0.75rem;"><span class="ejercicio-numero">{k}.</span>{enunciado}</p>
        <ol style="list-style-type: lower-alpha; margin-top: 0.5rem; margin-bottom: 0;">
{items}
        </ol>
'''


def bloque(nombre):
    return f'          <pre><code class="language-r">{codigo(nombre)}</code></pre>'


def aplica(plantillas):
    t10 = plantillas["templates_10.html"]
    m = lambda ident: marca(t10, ident)                                           # noqa: E731

    # ------------------------------------------------------------------ ejercicio 1
    e1 = cabeza(1,
                f'''Toma {m("c4-m10-61")}. Recorre el ciclo completo partiendo del IMA($1,1$), es decir, del
          ARIMA($0,1,1$), y entrega:''',
                [r'''El $d$ que eliges, y con qué evidencias.''',
                 r'''La rejilla con $p, q \in \{0,1,2\}$ para ese $d$: el puesto del IMA($1,1$) por AICc y su
            diagnóstico, con Ljung–Box y con la ACF de sus residuales barra por barra.''',
                 r'''El modelo con el que te quedas, con sus coeficientes y su diagnóstico.''',
                 r'''La misma rejilla con $d = 2$. Su mejor modelo tiene un AICc más de 17 puntos menor que el
            del IMA($1,1$): ¿es una razón para pasar a $d = 2$? Diagnostica también ese modelo.''']) + panel(
        1,
        r'''Para $d$, mira el gráfico y las pruebas. El $\hat\rho_1$ de la serie diferenciada es solo
            un indicio, que falla en los dos sentidos (Módulo 2.7): no basta para decir que la diferencia sobra ni que
            hace falta. Para (b), no te quedes en el $p$-valor global. Y para (d), mira la fórmula del AICc antes
            de comparar, y recuerda que diagnosticar no es solo mirar los residuales.''',
        f'''          <p><strong>Respuesta: $d = 1$. El IMA($1,1$) de partida no pasa el diagnóstico, y el AICc ya lo dejaba
            penúltimo; queda el ARIMA($1,1,1$). Y el mejor modelo con $d = 2$, pese a su AICc, es ese mismo
            ARIMA($1,1,1$) con una diferencia de más.</strong></p>
{bloque("e1")}
          <p><strong>(a)</strong> ADF no rechaza la raíz unitaria ($p = 0.53$) y <code>ndiffs()</code> pide una
            diferencia; el $\\hat\\rho_1$ de la serie diferenciada una vez es $0.31$, y dos veces, $-0.48$. Se toma
            $d = 1$.</p>
          <p><strong>(b)</strong> El IMA($1,1$) es el octavo de nueve por AICc ($533.35$, a $18.4$ puntos del mejor) y
            no pasa Ljung–Box(20) ($p = 0.034$). Aquí el criterio y el diagnóstico dicen lo mismo, y la ACF de los
            residuales dice por qué: $0.248$ en el rezago 2 y $0.209$ en el 4, con banda $\\pm 0.160$. Queda una
            parte AR sin modelar.</p>
          <p><strong>(c)</strong> El ARIMA($1,1,1$) la recoge con $\\hat\\phi = 0.880$ (e.e. $0.064$) y
            $\\hat\\theta = -0.641$ (e.e. $0.103$). Es el mínimo de AICc y de BIC, pasa Ljung–Box ($p = 0.622$) y
            Shapiro–Wilk ($p = 0.629$), y es el que devuelve <code>auto.arima</code>.</p>
          <p style="margin-bottom:0;"><strong>(d)</strong> Dos lecciones. {m("c4-m10-65")}. El mejor modelo con $d = 2$ es el ARIMA($1,2,2$): AICc $515.86$,
            residuales sin estructura (Ljung–Box $p = 0.565$) y, sin embargo, una raíz MA de módulo $1.000$. Su
            polinomio MA es $1 - 1.625B + 0.625B^2 = (1 - B)(1 - 0.625B)$: lleva dentro el factor que deshace la
            segunda diferencia, y lo que queda es un ARIMA($1,1,1$) con $\\hat\\phi = 0.860$ y
            $\\hat\\theta = -0.625$, prácticamente el de (c). Ni el AICc ni Ljung–Box lo delatan; las raíces, sí. La segunda: los
            $17.5$ puntos que separan al IMA($1,1$) de ese modelo no dicen nada sobre $d$, porque un AICc se
            calcula sobre $149$ observaciones y el otro sobre $148$. Quien los comparase pasaría a $d = 2$ por la
            razón equivocada; el IMA($1,1$) se descarta dentro de $d = 1$, que es donde se puede comparar.</p>''')

    # ------------------------------------------------------------------ ejercicio 2
    e2 = cabeza(2,
                r'''<code>pelt</code>, del paquete <code>tsibbledata</code>, recoge las pieles de liebre americana y de
          lince canadiense que comerció cada año la Compañía de la Bahía de Hudson entre 1845 y 1935 (91 datos).
          Trabaja con el logaritmo de las de liebre, <code>log(pelt$Hare)</code>, una serie de ciclos muy marcados,
          y responde a una sola pregunta: <strong>¿hay que diferenciarla?</strong> Entrega:''',
                [r'''Lo que piden las tres pruebas de raíz unitaria.''',
                 r'''La varianza de la serie y de sus dos primeras diferencias, y el cociente
            $\operatorname{Var}(\nabla y)/\operatorname{Var}(y)$ frente a $2(1 - r_1)$. ¿Dice algo sobre $d$?''',
                 r'''El módulo de la raíz MA de los ARIMA($0,1,1$), ($1,1,1$), ($2,1,1$) y ($3,1,1$). ¿Cuáles
            delatan la diferencia, y por qué no todos?''',
                 r'''Un modelo sin diferenciar que pase el diagnóstico.''']) + panel(
        2,
        r'''Para (a) y (c), la segunda y la tercera evidencia del Módulo 3; para (b), lo que el Módulo 3
            dice de la varianza. Para (c), piensa qué parte del modelo tiene que recoger el ciclo antes de que el
            término MA pueda delatar algo.''',
        f'''          <p><strong>Respuesta: no hay que diferenciarla ($d = 0$). Lo dicen las tres pruebas, y lo confirma la raíz
            MA de los modelos con $d = 1$ que tienen parte AR suficiente. La varianza, que baja un tercio al
            diferenciar, no dice nada.</strong></p>
{bloque("e2")}
          <p><strong>(a)</strong> Las tres pruebas coinciden en $d = 0$: según las tres, la serie es estacionaria.</p>
          <p><strong>(b)</strong> La varianza pasa de $1.323$ a $0.890$ al diferenciar una vez, un $33\\,\\%$ menos, y
            sube a $1.692$ con la segunda diferencia. {m("c4-m10-67")}: con $r_1 = 0.666$ cabe esperar un cociente cercano a $2(1 - r_1) = 0.669$, y el medido es
            $0.673$. El $\\hat\\rho_1$ de la serie diferenciada tampoco avisa: vale $0.043$.</p>
          <p><strong>(c)</strong> El ARIMA($0,1,1$) tiene la raíz MA en $21.84$ y el ARIMA($1,1,1$), en $1.45$: ninguna
            señal. El ARIMA($2,1,1$) la tiene en $1.0000$, con $\\hat\\theta = -1.000$, y el ARIMA($3,1,1$), en
            $1.020$. La firma aparece cuando el modelo tiene parte AR suficiente para el ciclo, y aquí hacen falta
            al menos dos coeficientes; con menos, el término MA se ocupa de otra cosa y la raíz no delata nada. Es
            lo que mostraba la práctica del Módulo 8.</p>
          <p><strong>(d)</strong> El AR(2) se queda en el borde (Ljung–Box(20) $p = 0.055$). El AR(4), que es el que
            elige la búsqueda exhaustiva de <code>auto.arima</code>, pasa con holgura ($p = 0.883$) y tiene mejor AICc ($223.21$ frente a
            $232.47$).</p>
          <p style="margin-bottom:0;"><strong>El mismo patrón en otra serie.</strong> La serie <code>lynx</code> ({m("c4-m10-151")} tiene {m("c4-m10-66")}, {m("c4-m10-150")}. {m("c4-m10-68")}. Con su logaritmo ocurre lo mismo que con la liebre, y más marcado: las tres pruebas piden $d = 0$: la serie es estacionaria. Diferenciar reduce la varianza un $58\\,\\%$ ($1.653 \\to 0.687$), pero esa caída no dice nada de raíces
            unitarias: {m("c4-m10-70")}. El $\\hat\\rho_1$ de la serie diferenciada vale $0.565$, y el ARIMA($2,1,1$) tiene
            $\\hat\\theta = -1.000$, con la raíz MA de módulo $1.000$. Las cifras de las pruebas, de la varianza, de $r_1$ y del ARIMA($2,1,1$) son las del bloque que
            sigue al aviso «La columna de la varianza no decide $d$» del Módulo 8.</p>''')

    # ------------------------------------------------------------------ ejercicio 3
    ini3 = t10.index('<div class="ejercicio-panel pista" id="c4e3-pista" hidden>')
    pista3 = t10[t10.index('<p style="margin:0;">', ini3) + len('<p style="margin:0;">'):t10.index("</p>", ini3)]
    assert 'data-afirma="c4-m10-71"' in pista3
    viejo3 = '''Los $\\psi$ no salen del ARIMA directamente: hay que expandirlo primero como el
            ARMA($2,1$) del Módulo 1, con $\\phi^{*} = (1+\\phi,\\ -\\phi)$.'''
    assert pista3.count(viejo3) == 1 and pista3.index(viejo3) < pista3.index("<span data-afirma")
    pista3 = pista3.replace(viejo3, '''Los $\\psi$ salen de la forma cerrada del Módulo 9, o de expandir el modelo como el
            ARMA($2,1$) del Módulo 1, con $\\phi^{*} = (1+\\phi,\\ -\\phi)$: las dos vías dan lo mismo.''')
    e3 = cabeza(3,
                r'''Sobre el ARIMA($1,1,1$) de <code>BJsales</code> del ejercicio 1, ajustado con
          <code>Arima()</code>, entrega:''',
                [r'''El valor al que tienden los pesos $\psi_j$, con la forma cerrada del Módulo 9 y antes de
            expandir nada. ¿Qué anticipa sobre el intervalo, comparado con el del Nilo?''',
                 r'''El intervalo de pronóstico del $95\,\%$ para $h = 1, \dots, 12$, <strong>construido a
            mano</strong> desde los pesos $\psi$, y su diferencia con el de <code>forecast()</code>.''',
                 r'''$\sigma_{12}/\sigma_1$ frente a $\sqrt{12}$: ¿crece $\sigma_h$ como en una caminata
            aleatoria?''']) + panel(
        3, pista3,
        f'''          <p><strong>Respuesta: $\\psi_\\infty = 2.99$, así que cada choque acaba pesando casi el triple, al revés
            que en el Nilo. El intervalo hecho a mano coincide con el de <code>forecast()</code> (error
            $2.4\\times 10^{{-14}}$), y $\\sigma_h$ crece bastante más rápido que $\\sqrt{{h}}$.</strong></p>
{bloque("e3")}
          <p><strong>(a)</strong> $\\psi_\\infty = (1+\\hat\\theta)/(1-\\hat\\phi) = 2.99$, mayor que $1$: los choques se
            amplifican en vez de amortiguarse. En el Nilo era $0.169$.</p>
          <p><strong>(b)</strong> La fórmula reproduce el intervalo hasta el error de máquina: no hay ninguna magia en
            <code>forecast()</code>.</p>
          <p style="margin-bottom:0;"><strong>(c)</strong> Conviene decir bien contra qué se compara: $\\sigma\\sqrt{{h}}$ no es "el caso de
            errores independientes" sino {m("c4-m10-72")}. Aquí
            $\\sigma_{{12}}$ es $1.96$ veces la de una caminata, porque los $\\psi_j$ no decaen a cero sino que tienden
            a $2.99$; a $h = 12$ van por $2.56$, todavía subiendo, porque $\\hat\\phi = 0.88$ hace
            la convergencia lenta. <strong>Cada nuevo choque se acumula con casi tres veces su peso.</strong> Es el
            contraste exacto del Nilo, donde $\\psi_\\infty = 0.169$ y la incertidumbre crece cuatro veces
            <em>menos</em> que la de una caminata.</p>''')

    i = t10.index('      <div class="ejercicio-guiado">')
    j = t10.index("      <h3>Lecturas</h3>")
    antes = t10[i:j]
    assert antes.count('<div class="ejercicio-guiado">') == 3
    t10 = t10[:i] + e1 + "\n" + e2 + "\n" + e3 + "\n" + t10[j:]
    plantillas["templates_10.html"] = t10

    # ------------------------------------------------------------------ M8 y M9: lo que resolvía E2 y E3
    t79 = plantillas["templates_7_9.html"]
    viejo8 = '''que es la manera en que ese indicio falla (Módulo 2.7).</span> (Es el ejercicio 2 de este
          capítulo.)</p>
      </div>
'''
    t79 = reemplaza(t79, viejo8, '''que es la manera en que ese indicio falla (Módulo 2.7).</span> (El bloque de
          abajo lo calcula.)</p>
      </div>

''' + bloque("e2b").replace("          <pre>", "      <pre>", 1) + "\n", "M8 · lynx")
    t79 = reemplaza(t79,
                    '''        <p style="margin-bottom:0;">No siempre es así. Sobre <code>BJsales</code> (ejercicio 3) el mismo tipo de
          modelo da $\\psi_\\infty = 2.99$: a doce pasos $\\sigma_h$ ya es $1.96$ veces el de una caminata, y el
          cociente sigue subiendo hacia $2.99$. Mirar $\\psi_\\infty$ cuesta una línea y dice más sobre el pronóstico
          a largo plazo que cualquier coeficiente por separado.</p>''',
                    '''        <p style="margin-bottom:0;">No siempre es así. Cuando $\\phi + \\theta > 0$, $\\psi_\\infty$ es mayor que $1$
          y cada choque acaba pesando más que cuando llegó. Mirar $\\psi_\\infty$ cuesta una línea y dice más sobre
          el pronóstico a largo plazo que cualquier coeficiente por separado.</p>''', "M9 · BJsales")
    plantillas["templates_7_9.html"] = t79
    return plantillas
