#!/usr/bin/env python3
"""R5 del capítulo 3 · T5.1: los ocho ejercicios cortos «Para practicar» (D9).

No se ejecuta solo: lo importa `r5_edita.py`. El código de cada solución NO está escrito aquí:
se lee de `r5_bloques/<id>.out`, que es la salida de `r5_reprex.R` sobre `r5_bloques/<id>.R`,
con cada resultado real bajo su línea tras `#> `. Las cifras de la prosa que no salen bajo un
`#>` están en `r5_cifras.out`, con la etiqueta que se anota en el comentario de cada párrafo.

Cada ejercicio se inserta justo antes de la lista de fuentes de su módulo
(`<aside class="fuentes-modulo"`), como en el capítulo 2.
"""
import html
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def codigo(nombre):
    """El bloque ejecutado, escapado como el resto del capítulo 3 (`<`, `>` y `&`)."""
    t = (AQUI / "r5_bloques" / f"{nombre}.out").read_text(encoding="utf-8")
    t = "\n".join(l.rstrip() for l in t.rstrip("\n").splitlines())
    return html.escape(t, quote=False)


def ejercicio(mid, enunciado, entregables, pista, solucion):
    items = "\n".join(f"            <li>{e}</li>" for e in entregables)
    return f'''      <div class="exercise">
        <h4><i class="fas fa-pen-to-square mr-2" aria-hidden="true"></i>Para practicar</h4>
        <div class="ejercicio-guiado">
          <p class="ejercicio-enunciado" style="margin-bottom: 0.75rem;">{enunciado}</p>
          <ol style="list-style-type: lower-alpha; margin-top: 0.5rem; margin-bottom: 0;">
{items}
          </ol>
          <div class="ejercicio-acciones">
            <button type="button" class="ejercicio-boton" aria-expanded="false" aria-controls="c3m{mid}-pista">
              <i class="fas fa-lightbulb" aria-hidden="true"></i> Pista <i class="fas fa-chevron-down" aria-hidden="true"></i>
            </button>
            <button type="button" class="ejercicio-boton" aria-expanded="false" aria-controls="c3m{mid}-sol">
              <i class="fas fa-key" aria-hidden="true"></i> Solución <i class="fas fa-chevron-down" aria-hidden="true"></i>
            </button>
          </div>
          <div class="ejercicio-panel pista" id="c3m{mid}-pista" hidden>
            <p style="margin:0;">{pista}</p>
          </div>
          <div class="ejercicio-panel solucion" id="c3m{mid}-sol" hidden>
{solucion}
          </div>
        </div>
      </div>

'''


def sol(respuesta, bloque, parrafos):
    cuerpo = [f"            <p><strong>Respuesta: {respuesta}</strong></p>",
              f'            <pre><code class="language-r">{codigo(bloque)}</code></pre>']
    for i, p in enumerate(parrafos):
        estilo = ' style="margin-bottom:0;"' if i == len(parrafos) - 1 else ""
        cuerpo.append(f"            <p{estilo}>{p}</p>")
    return "\n".join(cuerpo)


CORTOS = {}

# ---------------------------------------------------------------- Módulo 1
# Escribir un modelo con B (de la recursión al polinomio, con los dos convenios de signo) y leer
# sus raíces. Procesos teóricos; ninguno coincide con los del módulo ni con los de la práctica de
# repaso o el simulacro. Cifras: bloque m1; [M1-01], [M1-02], [M1-03].
CORTOS[1] = ejercicio(
    1,
    "Dos modelos están escritos como recursión, con $\\varepsilon_t$ ruido blanco. El modelo A es "
    "$y_t = 1.1\\,y_{t-1} - 0.3\\,y_{t-2} + \\varepsilon_t + 0.4\\,\\varepsilon_{t-1}$, y el modelo B, "
    "$y_t = 1.5\\,y_{t-1} - 0.5\\,y_{t-2} + \\varepsilon_t$. Entrega cuatro cosas:",
    [
        "Cada modelo en la forma $\\phi(B)\\,y_t = \\theta(B)\\,\\varepsilon_t$, con los dos polinomios "
        "escritos término a término.",
        "Las raíces de $\\phi(B) = 0$ en el modelo A, a mano (es una ecuación de segundo grado), y el "
        "veredicto: ¿es estacionario?",
        "Alguien escribe el polinomio autorregresivo de A como $1 - 1.1B - 0.3B^2$. Calcula las raíces "
        "de ese polinomio y escribe la recursión a la que corresponde de verdad.",
        "El polinomio $\\phi(B)$ del modelo B, factorizado. ¿Qué dice uno de sus dos factores, y qué "
        "modelo sigue $\\nabla y_t$?",
    ],
    "Pasa al lado izquierdo todo lo que lleve $y$ y deja en el derecho lo que lleve $\\varepsilon$; "
    "después cambia cada $y_{t-k}$ por $B^k y_t$ y saca factor común. Los signos se deciden en ese paso, "
    "no después. Para factorizar un polinomio de segundo grado sirven sus raíces: si son $B_1$ y $B_2$, "
    "el polinomio es $(1 - B/B_1)(1 - B/B_2)$.",
    sol(
        "A es estacionario, con raíces $1.667$ y $2$; el polinomio con el signo cambiado es otro proceso, "
        "que no lo es; y B tiene una raíz unitaria: es un AR(1) sobre $\\nabla y_t$.",
        "m1",
        [
            "<strong>(a)</strong> Con las $y$ a la izquierda, A queda "
            "$y_t - 1.1\\,y_{t-1} + 0.3\\,y_{t-2} = \\varepsilon_t + 0.4\\,\\varepsilon_{t-1}$, es decir, "
            "$\\phi(B) = 1 - 1.1B + 0.3B^2$ y $\\theta(B) = 1 + 0.4B$. El $-0.3$ de la recursión aparece "
            "<strong>sumando</strong> en $\\phi(B)$ y el $+0.4$ de los choques conserva su signo: los "
            "$\\phi$ entran restando y los $\\theta$, sumando. En B, $\\phi(B) = 1 - 1.5B + 0.5B^2$ y "
            "$\\theta(B) = 1$.",
            "<strong>(b)</strong> $0.3B^2 - 1.1B + 1 = 0$ tiene discriminante $1.21 - 1.2 = 0.01$, así que "
            "$B = (1.1 \\pm 0.1)/0.6$: las raíces son $1.667$ y $2$. Las dos caen fuera del círculo "
            "unitario y A es estacionario. La raíz de $\\theta(B)$, que es $-2.5$, no interviene en esa "
            "pregunta.",
            "<strong>(c)</strong> $1 - 1.1B - 0.3B^2$ tiene raíces $0.754$ y $-4.421$, y la primera cae "
            "<em>dentro</em> del círculo. Es el polinomio de "
            "$y_t = 1.1\\,y_{t-1} + 0.3\\,y_{t-2} + \\cdots$, otro proceso, que no es estacionario. Nada "
            "avisa del cambio: el signo se pierde al escribir, no al calcular. Hay un segundo fallo igual "
            "de silencioso, el del orden: con los coeficientes al revés, <code>polyroot()</code> devuelve "
            "$0.5$ y $0.6$, las inversas de las raíces de A, y el veredicto sale al contrario.",
            "<strong>(d)</strong> Las raíces son $1$ y $2$, así que $\\phi(B) = (1 - B)(1 - 0.5B)$. El "
            "factor $(1 - B)$ es una raíz unitaria: B no es estacionario. Pero $(1 - B)\\,y_t$ es "
            "$\\nabla y_t$, de modo que el modelo dice $(1 - 0.5B)\\,\\nabla y_t = \\varepsilon_t$: la "
            "serie diferenciada sigue $\\nabla y_t = 0.5\\,\\nabla y_{t-1} + \\varepsilon_t$, cuyo "
            "polinomio tiene la raíz $2$, fuera del círculo. Es el enlace con el Capítulo 2 leído en el "
            "otro sentido: la diferencia no se aplica a los datos, se encuentra dentro del polinomio.",
        ],
    ),
)

# ---------------------------------------------------------------- Módulo 2
# Los momentos de un AR(2) a mano: mu (con la trampa de la constante), rho_1..rho_3 y gamma_0 por
# los dos caminos. Cifras: bloque m2; [M2-01] a [M2-04], [M2-06].
CORTOS[2] = ejercicio(
    2,
    "Un AR(2) tiene $c = 4$, $\\phi_1 = 0.8$, $\\phi_2 = -0.6$ y $\\sigma^2 = 3$: "
    "$y_t = 4 + 0.8\\,y_{t-1} - 0.6\\,y_{t-2} + \\varepsilon_t$. Con papel y calculadora, entrega:",
    [
        "La comprobación de que es estacionario y de si sus raíces son reales o complejas; si son "
        "complejas, el pseudo-periodo.",
        "La media $\\mu$ y las autocorrelaciones $\\rho_1$, $\\rho_2$ y $\\rho_3$.",
        "La varianza $\\gamma_0$, por la fórmula general y por la fórmula cerrada del AR(2).",
        "Una comprobación en R: <code>ARMAacf()</code> para las autocorrelaciones, y la media y la "
        "varianza muestrales de una realización de 100 000 valores.",
    ],
    "Sitúa primero el punto $(\\phi_1, \\phi_2)$ en el triángulo. Para los momentos, sigue el orden que el "
    "módulo llama obligatorio, y antes de escribir la media vuelve a la nota sobre la constante. En (d), "
    "<code>arima.sim()</code> simula el proceso con media cero y recibe en <code>sd</code> la desviación "
    "estándar del ruido, no su varianza.",
    sol(
        "es estacionario, con raíces complejas y un pseudo-periodo de $6.11$ periodos; $\\mu = 5$, "
        "$\\rho_1 = 0.5$, $\\rho_2 = -0.2$, $\\rho_3 = -0.46$ y $\\gamma_0 = 6.25$.",
        "m2",
        [
            "<strong>(a)</strong> Las tres desigualdades del triángulo se cumplen: "
            "$\\phi_1 + \\phi_2 = 0.2 < 1$, $\\phi_2 - \\phi_1 = -1.4 < 1$ y $|\\phi_2| = 0.6 < 1$. Como "
            "$\\phi_1^2 + 4\\phi_2 = -1.76$ es negativo, las raíces son complejas (de módulo $1.291$) y la "
            "ACF oscila con un pseudo-periodo de $2\\pi/\\arccos(0.5164) = 2\\pi/1.0282 = 6.11$ periodos.",
            "<strong>(b)</strong> $\\mu = c/(1 - \\phi_1 - \\phi_2) = 4/0.8 = 5$, y no $4$: la constante "
            "no es la media. $\\rho_1 = 0.8/1.6 = 0.5$; $\\rho_2 = -0.6 + 0.64/1.6 = -0.2$; y con la "
            "recursión, $\\rho_3 = 0.8\\,(-0.2) - 0.6\\,(0.5) = -0.46$. La ACF cambia de signo en el "
            "segundo rezago: es la oscilación que anunciaban las raíces complejas.",
            "<strong>(c)</strong> "
            "$\\gamma_0 = \\sigma^2/(1 - \\phi_1\\rho_1 - \\phi_2\\rho_2) = 3/(1 - 0.4 - 0.12) = 3/0.48 = 6.25$. "
            "Por la fórmula cerrada, $(1.6 \\times 3)/(0.4 \\times 1.92) = 4.8/0.768 = 6.25$. El proceso "
            "tiene algo más del doble de la varianza del ruido que lo alimenta.",
            "<strong>(d)</strong> <code>ARMAacf()</code> devuelve las mismas tres autocorrelaciones. La "
            "realización de 100 000 valores da una media de $5.01$ y una varianza de $6.31$: cerca de $5$ "
            "y de $6.25$, y no iguales, porque son estimaciones.",
        ],
    ),
)

# ---------------------------------------------------------------- Módulo 3
# La invertibilidad como «poder reconstruir los choques» (c3-m3-08, sin tocar), vista con números.
# Simulado con semilla. Cifras: bloque m3; [M3-01], [M3-02], [M3-03].
CORTOS[3] = ejercicio(
    3,
    "El módulo define el MA(1) invertible como el único con el que se puede reconstruir cada choque a "
    "partir de lo observado. Para verlo, simula 500 choques y construye con <strong>los mismos "
    "choques</strong> dos series $y_t = \\varepsilon_t + \\theta\\,\\varepsilon_{t-1}$: una con "
    "$\\theta = 0.5$ y otra con $\\theta = 2$. Los choques se reconstruyen despejando, "
    "$\\hat\\varepsilon_t = y_t - \\theta\\,\\hat\\varepsilon_{t-1}$, y como $\\varepsilon_0$ no se "
    "observa se arranca con $\\hat\\varepsilon_0 = 0$. Entrega:",
    [
        "A mano: cómo depende el error de reconstrucción, $\\hat\\varepsilon_t - \\varepsilon_t$, del "
        "error del periodo anterior, y qué le pasa al cabo de $t$ periodos con cada $\\theta$.",
        "En R: el tamaño de ese error en $t = 1, 2, 5, 10$ y $20$ para las dos series, usando en cada una "
        "su $\\theta$ verdadero.",
        "Lo que devuelve <code>arima()</code> al ajustar un MA(1) a la serie de $\\theta = 2$, y la "
        "correlación de sus residuales con los choques que se usaron para simularla. ¿Los reconstruye?",
    ],
    "En (a), escribe una debajo de la otra la ecuación del modelo, "
    "$y_t = \\varepsilon_t + \\theta\\,\\varepsilon_{t-1}$, y la de la reconstrucción, "
    "$y_t = \\hat\\varepsilon_t + \\theta\\,\\hat\\varepsilon_{t-1}$, y réstalas. En (c), antes de ejecutar "
    "nada, calcula con qué $\\theta$ y con qué $\\sigma^2$ describe el mismo proceso el MA(1) invertible.",
    sol(
        "con $\\theta = 0.5$ el error de reconstrucción se reduce a la mitad en cada periodo; con "
        "$\\theta = 2$ se duplica; y <code>arima()</code> devuelve el otro MA(1), el invertible, cuyos "
        "residuales no son los choques simulados.",
        "m3",
        [
            "<strong>(a)</strong> Al restar, $y_t$ desaparece y queda "
            "$\\hat\\varepsilon_t - \\varepsilon_t = -\\theta\\,(\\hat\\varepsilon_{t-1} - \\varepsilon_{t-1})$: "
            "cada error es el anterior multiplicado por $-\\theta$. El primero es el de haber puesto $0$ "
            "donde iba $\\varepsilon_0$, así que tras $t$ periodos el error mide "
            "$|\\theta|^{\\,t}\\,|\\varepsilon_0|$. Con $\\theta = 0.5$ se apaga; con $\\theta = 2$ crece "
            "sin límite.",
            "<strong>(b)</strong> En esta simulación $|\\varepsilon_0| = 0.136$. Con $\\theta = 0.5$ el "
            "error es $0.068$ en $t = 1$ y $0.00013$ en $t = 10$: el arranque se olvida y los choques "
            "quedan reconstruidos. Con $\\theta = 2$ es $0.272$ en $t = 1$, $139$ en $t = 10$ y unos "
            "$143\\,000$ en $t = 20$. Se está usando el $\\theta$ verdadero y aun así la reconstrucción no "
            "sirve, porque cualquier error de partida, por pequeño que sea, se duplica en cada periodo. "
            "Eso es no ser invertible.",
            "<strong>(c)</strong> El MA(1) invertible que describe el mismo proceso que "
            "$(\\theta, \\sigma^2) = (2, 1)$ es $(1/2,\\ 4)$, y eso es lo que estima <code>arima()</code>: "
            "$\\hat\\theta = 0.451$ y $\\hat\\sigma^2 = 4.03$. Sus residuales son ruido blanco "
            "(autocorrelaciones de $0.012$, $0.034$ y $-0.011$), pero no son los choques con que se simuló "
            "la serie: su correlación con $\\varepsilon_t$ es $0.451$ y con $\\varepsilon_{t-1}$, $0.778$ "
            "(los valores teóricos son $0.5$ y $0.75$). Los mismos datos admiten dos parejas de "
            "coeficiente y choques, y solo la invertible se deja reconstruir desde lo observado: por eso "
            "es la que el software devuelve por defecto.",
        ],
    ),
)

# ---------------------------------------------------------------- Módulo 4
# Los pesos pi como pronóstico a un paso (el hueco del módulo) y los psi como varianza, con un
# ARMA(1,1) de theta negativo. Simulado con semilla. Cifras: bloque m4; [M4-01] a [M4-04].
CORTOS[4] = ejercicio(
    4,
    "Un ARMA(1,1) tiene $\\phi = 0.8$ y $\\theta = -0.5$, sin constante: "
    "$y_t = 0.8\\,y_{t-1} + \\varepsilon_t - 0.5\\,\\varepsilon_{t-1}$. Entrega:",
    [
        "A mano, los pesos $\\pi_1$ a $\\pi_4$ con la recursión del módulo, y el pronóstico a un paso "
        "escrito como una suma ponderada de las cuatro últimas observaciones.",
        "Ese pronóstico para una serie cuyas cuatro últimas observaciones son, de la más reciente a la "
        "más antigua, $-1.23$, $-0.05$, $1.00$ y $0.69$ (salen de simular 200 valores del proceso con "
        "<code>set.seed(34)</code>). Compáralo en R con el que usa las 200 observaciones: ¿cuánto se "
        "pierde por truncar la suma?",
        "Los pesos $\\psi_1$ y $\\psi_2$, la varianza del error de pronóstico a 1, 2 y 3 pasos en unidades "
        "de $\\sigma^2$, y el techo al que tiende.",
    ],
    "Con $\\theta$ negativo los signos de los $\\pi$ no salen como en el ejemplo del módulo: calcula "
    "$\\pi_1$ con cuidado y deja que la recursión haga el resto. El pronóstico lleva $-\\pi_j$, no "
    "$\\pi_j$. Para el techo, los $\\psi$ forman una progresión geométrica desde $j = 1$.",
    sol(
        "el pronóstico a un paso es $0.3\\,y_T + 0.15\\,y_{T-1} + 0.075\\,y_{T-2} + 0.0375\\,y_{T-3} + \\cdots$; "
        "con cuatro observaciones da $-0.276$ y con las doscientas, $-0.293$.",
        "m4",
        [
            "<strong>(a)</strong> $\\pi_1 = -\\phi - \\theta = -0.8 + 0.5 = -0.3$, y desde ahí cada peso es "
            "el anterior por $-\\theta = 0.5$: $\\pi_2 = -0.15$, $\\pi_3 = -0.075$ y $\\pi_4 = -0.0375$. "
            "Todos negativos: con $\\theta < 0$ los $\\pi$ no alternan. El pronóstico les cambia el signo, "
            "$\\hat y_{T+1\\mid T} = 0.3\\,y_T + 0.15\\,y_{T-1} + 0.075\\,y_{T-2} + 0.0375\\,y_{T-3} + \\cdots$: "
            "un promedio de las observaciones pasadas con pesos que se reducen a la mitad a cada paso "
            "atrás y que suman $0.6$.",
            "<strong>(b)</strong> Con las cuatro observaciones, "
            "$0.3\\,(-1.23) + 0.15\\,(-0.05) + 0.075\\,(1.00) + 0.0375\\,(0.69) = -0.276$. Con ocho da "
            "$-0.291$ y con las doscientas, $-0.293$, que es también lo que devuelve "
            "<code>predict()</code> con los coeficientes verdaderos. Truncar en cuatro términos cuesta "
            "menos de dos centésimas, porque el primer peso que se deja fuera ya es $0.01875$: es la "
            "invertibilidad la que permite cortar la suma.",
            "<strong>(c)</strong> $\\psi_1 = \\phi + \\theta = 0.3$ y $\\psi_2 = 0.8 \\times 0.3 = 0.24$. "
            "La varianza del error es $\\sigma^2$ a un paso, $1.09\\,\\sigma^2$ a dos y "
            "$1.1476\\,\\sigma^2$ a tres. El techo es "
            "$\\gamma_0 = \\sigma^2\\,[1 + 0.09/(1 - 0.64)] = 1.25\\,\\sigma^2$: a tres pasos la varianza "
            "del pronóstico ya es el $92\\,\\%$ de la del proceso.",
        ],
    ),
)

# ---------------------------------------------------------------- Módulo 5
# El ciclo de identificación sobre una serie real y la rho_1 de un ARMA(1,1) nuevo a mano.
# Serie: diff(WWWusage) (ayuda de R en r5_ayuda_datasets.out). Cifras: bloque m5; [M5-01] a [M5-04].
CORTOS[5] = ejercicio(
    5,
    "<code>WWWusage</code> trae el número de usuarios conectados a Internet a través de un servidor, "
    "minuto a minuto, durante 100 minutos. Trabaja con sus cambios de un minuto al siguiente, "
    "<code>w &lt;- diff(WWWusage)</code>, que son 99 valores, y recorre con ellos el ciclo del módulo. "
    "Entrega:",
    [
        "Pasos 1 a 3: los rezagos de la ACF y de la PACF que salen de la banda entre los 20 primeros, la "
        "fila de la tabla que corresponde y dos candidatos, uno puro y uno mixto.",
        "A mano: $\\rho_1$, $\\rho_2$ y $\\rho_3$ de un ARMA(1,1) con $\\phi = 0.63$ y $\\theta = 0.53$, "
        "que es el ajustado a esta serie, redondeado. Compáralas con $r_1$, $r_2$ y $r_3$.",
        "Paso 4: la ACF teórica de los dos candidatos ajustados frente a la muestral, en los seis primeros "
        "rezagos. ¿Cuál la reproduce mejor, y desde qué rezago se separa el otro?",
    ],
    "La tabla se lee por la función que se corta: mira primero si alguna lo hace, y en qué rezago. Para "
    "(b), la fórmula de $\\rho_1$ del ARMA(1,1) está en la sección «Por qué la tabla no da los órdenes de "
    "un ARMA»; desde $\\rho_1$, cada rezago sale del anterior. En (c), <code>ARMAacf()</code> recibe los "
    "coeficientes de un ajuste con <code>coef()</code>.",
    sol(
        "la tabla propone un AR(3); un ARMA(1,1) acierta en $r_1$, se acerca a $r_2$ y se queda corto "
        "desde el rezago 3.",
        "m5",
        [
            "<strong>(a)</strong> La banda es $\\pm 0.197$. La PACF sale de ella en los rezagos 1, 2 y 3 "
            "($0.792$, $-0.287$ y $0.303$) y después se queda dentro; la ACF decae sin cortarse: sale en "
            "los rezagos 1 a 6 y otra vez, con signo negativo, del 17 al 20. Es la primera fila de la "
            "tabla, la del AR($p$), con $p = 3$. Como candidato mixto, el más pequeño: un ARMA(1,1), "
            "cuya ACF también decae.",
            "<strong>(b)</strong> "
            "$\\rho_1 = (1 + \\phi\\theta)(\\phi + \\theta)/(1 + 2\\phi\\theta + \\theta^2) = "
            "1.3339 \\times 1.16/1.9487 = 0.794$, y después $\\rho_2 = 0.63 \\times 0.794 = 0.500$ y "
            "$\\rho_3 = 0.63 \\times 0.500 = 0.315$. Las muestrales son $0.792$, $0.520$ y $0.406$: el "
            "modelo mixto reproduce la primera, se acerca a la segunda y en la tercera ya va por debajo.",
            "<strong>(c)</strong> La ACF teórica del AR(3) sigue a la muestral: $0.404$, $0.387$ y $0.351$ "
            "frente a $0.406$, $0.382$ y $0.332$ en los rezagos 3 a 5. La del ARMA(1,1) no puede hacerlo: "
            "desde $\\rho_1$ es geométrica, de razón $\\hat\\phi$, y cae a $0.321$, $0.203$ y $0.129$ "
            "mientras la muestral se detiene en una meseta cerca de $0.4$. Esa meseta es lo que recogen "
            "los tres coeficientes del AR(3), y el paso 4 se inclina por él.",
            "Como adelanto del Módulo 8: los residuales de los dos modelos pasan Ljung–Box ($p = 0.702$ y "
            "$0.515$), el AICc prefiere el AR(3) ($514.31$ frente a $516.00$) y el BIC, por menos de un "
            "punto, el ARMA(1,1) ($525.96$ frente a $526.64$). La tabla propuso un orden, el paso 4 lo "
            "sostuvo, y los dos criterios no se ponen de acuerdo con 99 datos.",
        ],
    ),
)

# ---------------------------------------------------------------- Módulo 6
# Predecir y después simular cuántas barras caen fuera de la banda: ruido blanco con tres T y los
# rezagos «vacíos» de un MA(1). Simulado con semilla. Cifras: bloque m6; [M6-01], [M6-02].
CORTOS[6] = ejercicio(
    6,
    "La regla del 5 % dice cuántas barras de un correlograma salen de la banda por puro azar. Antes de "
    "simular, escribe una predicción; después, compruébala. Entrega:",
    [
        "La predicción: en los 20 primeros rezagos de un ruido blanco, cuántas barras se esperan fuera de "
        "la banda y con qué probabilidad saldrán dos o más, suponiendo que cada una sale con probabilidad "
        "$0.05$ sin depender de las demás.",
        "La comprobación: 2000 series de ruido blanco de longitud $T = 50$, otras 2000 con $T = 200$ y "
        "otras 2000 con $T = 1000$; para cada longitud, el número medio de barras fuera y la proporción "
        "de series con dos o más. ¿Se cumple la predicción?",
        "Lo mismo con 2000 series de un MA(1) con $\\theta = 0.8$ y $T = 200$, contando solo los rezagos "
        "2 a 20, donde su ACF teórica vale exactamente cero. ¿Salen las barras que saldrían en un ruido "
        "blanco?",
    ],
    "Para (a) basta una distribución binomial. Para (b) y (c), escribe una función que reciba una serie y "
    "devuelva cuántas barras salen de $\\pm 1.96/\\sqrt{T}$, y repítela con <code>replicate()</code>. "
    "Antes de ejecutar (c), anota tu apuesta y el porqué.",
    sol(
        "en un ruido blanco sale, de media, menos de una barra de cada 20, y bastante menos con $T$ "
        "pequeña; en los rezagos donde un MA(1) no tiene nada salen casi el doble de las que anuncia la "
        "regla.",
        "m6",
        [
            "<strong>(a)</strong> Con 20 barras y probabilidad $0.05$ cada una se espera "
            "$20 \\times 0.05 = 1$ barra fuera; ninguna, con probabilidad $0.358$, y dos o más, con "
            "probabilidad $0.264$.",
            "<strong>(b)</strong> La simulación da menos: de media, $0.528$ barras con $T = 50$, $0.845$ "
            "con $T = 200$ y $0.984$ con $T = 1000$; y dos o más en el $10.4\\,\\%$, el $20.6\\,\\%$ y el "
            "$24.1\\,\\%$ de las series. La predicción solo se acerca a cumplirse con la serie larga. La banda "
            "$\\pm 1.96/\\sqrt{T}$ es una aproximación para $T$ grande: con series cortas las "
            "autocorrelaciones muestrales varían menos que eso, tanto menos cuanto mayor es el rezago (el "
            "Módulo 8 dice por qué), y la banda resulta holgada. Con 50 datos, dos barras fuera son "
            "más raras de lo que sugiere la cuenta de (a).",
            "<strong>(c)</strong> En los 19 rezagos donde la teoría dice cero, un ruido blanco dejaría "
            "fuera $19 \\times 0.05 = 0.95$ barras. El MA(1) deja $1.782$ de media, y dos o más en el "
            "$49.8\\,\\%$ de las series. No hay estructura en esos rezagos: lo que ocurre es que $r_k$ "
            "varía más cuando la serie está autocorrelacionada, y la banda del ruido blanco se queda "
            "estrecha. Ensanchándola con $\\rho_1$, a $\\pm 1.96\\sqrt{(1 + 2\\rho_1^2)/T} = \\pm 0.168$ "
            "en lugar de $\\pm 0.139$, el recuento baja a $0.79$ barras, parecido al $0.845$ del ruido "
            "blanco con esa misma $T$. Es la idea de la banda que <code>statsmodels</code> dibuja por "
            "defecto, la que según el Módulo 5 cuenta las autocorrelaciones de los rezagos anteriores. "
            "En la práctica: una vez que el correlograma muestra un corte, las barras sueltas que asoman "
            "después merecen menos crédito del que la banda les da.",
        ],
    ),
)

# ---------------------------------------------------------------- Módulo 7
# Los tres estimadores sobre otra serie con la MISMA T que las manchas: lo que separa a los
# métodos no es T sino la cercanía de las raíces al círculo. Serie: treering, 1880-1979 (ayuda de
# R en r5_ayuda_datasets.out). Cifras: bloque m7; [M7-01], [M7-02].
CORTOS[7] = ejercicio(
    7,
    "<code>treering</code> trae anchos de anillos de árbol, normalizados y sin unidades, uno por año: "
    "7980 valores que terminan en 1979. Los cien últimos, <code>window(treering, start = 1880)</code>, "
    "dan $T = 100$, lo mismo que la ventana de las manchas solares. Ajústales un AR(2) —el orden que usa "
    "el módulo, para poder comparar— y entrega:",
    [
        "Los coeficientes por Yule–Walker, por CSS y por máxima verosimilitud, y las tres $\\hat\\sigma^2$.",
        "La distancia de Yule–Walker y de CSS a máxima verosimilitud, en errores estándar. En las manchas, "
        "Yule–Walker quedó a $1.26$ y $1.10$ errores estándar: ¿qué es distinto aquí, si $T$ es la misma?",
        "Una comprobación por simulación: 500 series de $T = 100$ de un AR(2) parecido al de los anillos, "
        "$\\phi = (0.14,\\ 0.21)$, y 500 de uno parecido al de las manchas, $\\phi = (1.40,\\ -0.70)$; en "
        "cada grupo, la distancia media entre Yule–Walker y máxima verosimilitud.",
    ],
    "El código del módulo sirve cambiando la serie. Lo que cambia de una serie a otra no es $T$: compara "
    "lo que el módulo dice sobre cuándo se separan los métodos con lo que cada ajuste deja a la vista, "
    "sus coeficientes y sus raíces.",
    sol(
        "aquí los tres métodos coinciden: Yule–Walker queda a menos de $0.05$ errores estándar de máxima "
        "verosimilitud. La diferencia con las manchas no está en $T$, sino en lo cerca que quedan las "
        "raíces del círculo unitario.",
        "m7",
        [
            "<strong>(a)</strong> Yule–Walker da $(0.1386,\\ 0.2092)$; CSS, $(0.1384,\\ 0.2179)$; y máxima "
            "verosimilitud, $(0.1388,\\ 0.2140)$. Las $\\hat\\sigma^2$ son $0.0658$, $0.0647$ y $0.0637$.",
            "<strong>(b)</strong> Con errores estándar de $0.097$ y $0.098$, Yule–Walker queda a $0.002$ y "
            "$0.049$ errores estándar de máxima verosimilitud, y CSS, a $0.004$ y $0.040$: a efectos "
            "prácticos, el mismo ajuste. En las manchas, con la misma $T = 100$, Yule–Walker quedaba a "
            "$1.26$ y $1.10$. Lo que cambia es el proceso: las raíces del AR(2) de los anillos tienen "
            "módulo $1.86$ y $2.51$, lejos del círculo unitario, y las de las manchas, $1.19$. El módulo "
            "decía que CSS y máxima verosimilitud se separan con $T$ pequeña o con los coeficientes cerca "
            "de la frontera, y que Yule–Walker está sesgado hacia el interior de la región estacionaria: "
            "con las raíces lejos de la frontera, ese sesgo apenas se nota. Lo mismo pasa con las "
            "$\\hat\\sigma^2$: la de Yule–Walker es aquí un $3\\,\\%$ mayor que la de máxima "
            "verosimilitud; en las manchas lo era un $30\\,\\%$.",
            "<strong>(c)</strong> La simulación lo confirma. Con $\\phi = (0.14,\\ 0.21)$, cuya raíz más "
            "cercana al círculo tiene módulo $1.87$, la distancia media entre Yule–Walker y máxima "
            "verosimilitud es de $0.03$ y $0.05$ errores estándar; con $\\phi = (1.40,\\ -0.70)$, de módulo "
            "$1.20$, es de $0.66$ y $0.57$, con la misma $T$ (en una de las 500 series de este grupo "
            "<code>arima()</code> no llegó a dar estimación). Si el AR(2) es o no un buen modelo para "
            "estos cien años es otra pregunta, la del Módulo 8; aquí solo se comparan estimadores.",
        ],
    ),
)

# ---------------------------------------------------------------- Módulo 9
# Transferir la lección del caso 1 («la escala antes que el parámetro») a otra serie, con un
# resultado distinto: aquí transformar es necesario y NO cambia el modelo elegido ni arregla el
# diagnóstico. Serie: lynx (ayuda de R en r5_ayuda_datasets.out). Cifras: bloque m9; [M9-01] a [M9-05].
CORTOS[9] = ejercicio(
    9,
    "<code>lynx</code> trae el número de linces capturados cada año en Canadá entre 1821 y 1934: 114 "
    "valores. El caso de las manchas enseñó a mirar la escala antes de añadir un parámetro; se trata de "
    "aplicar esa lección a otra serie y ver qué pasa. Entrega:",
    [
        "¿Hay que transformar, y con qué? La elasticidad amplitud–nivel en bloques de 10 años, el mínimo "
        "de la serie y el $\\lambda$ de Guerrero.",
        "La rejilla de once candidatos del Módulo 8 sobre la serie cruda y sobre su logaritmo: el mejor "
        "por AICc y el mejor por BIC en cada escala. ¿Cambia el modelo elegido al transformar?",
        "El AR(2) en las dos escalas: pseudo-periodo, Ljung–Box en el rezago 12 y Shapiro–Wilk de los "
        "residuales. ¿Qué arregla la transformación y qué no?",
    ],
    "Las funciones <code>elasticidad()</code>, <code>aicc()</code> y <code>compara()</code> están en el "
    "código del caso 1 y sirven tal cual cambiando la serie. No compares el AICc de una escala con el de "
    "la otra: son datos distintos. Y no des por hecho que la historia de las manchas se repite: escribe "
    "tu apuesta para (b) antes de ejecutar.",
    sol(
        "hay que tomar logaritmos, y hacerlo no cambia el modelo elegido —AR(4) por AICc y AR(2) por BIC "
        "en las dos escalas— ni arregla Ljung–Box; lo que arregla es la normalidad de los residuales.",
        "m9",
        [
            "<strong>(a)</strong> La elasticidad es $\\hat b = 0.904$, con un intervalo de $0.542$ a "
            "$1.266$: excluye el $0$, así que hay que transformar; contiene el $1$, que es el logaritmo, y "
            "deja fuera por poco el $0.5$ de la raíz cuadrada. El mínimo de la serie es 39: no hay ceros "
            "que impidan el logaritmo, a diferencia de las manchas. El $\\lambda$ de Guerrero, $0.152$, "
            "queda también cerca de cero. Se toman logaritmos.",
            "<strong>(b)</strong> En las dos escalas el AICc elige el AR(4) y el BIC, el AR(2): el modelo "
            "elegido no cambia con la transformación. Cambia el orden de los que vienen detrás: en la "
            "serie cruda el segundo por AICc es el ARMA(2,2) y el AR(2) queda a $3.39$ puntos del mejor; "
            "en logaritmos el AR(2) pasa a ser el segundo, a $1.96$. Aquí no había un parámetro tapando "
            "un problema de escala: el AR(4) se pide con la escala corregida y sin corregir.",
            "<strong>(c)</strong> El pseudo-periodo del AR(2) pasa de $8.53$ a $9.78$ años. La normalidad "
            "de los residuales, que en la serie cruda se rechaza sin duda ($p < 0.0001$ en Shapiro–Wilk), "
            "deja de rechazarse en logaritmos ($p = 0.640$). Ljung–Box, en cambio, no mejora: el AR(2) da "
            "$p = 0.031$ en la serie cruda y $p = 0.013$ en logaritmos, y en logaritmos ninguno de los "
            "once candidatos pasa la prueba (el AR(4) da $p = 0.009$). La transformación era necesaria y "
            "arregló lo que era de escala; la autocorrelación que queda en los residuales no es de "
            "escala, y ningún ARMA de la rejilla la recoge. Lo que se puede entregar es un modelo que "
            "describe el ciclo y no pasa el diagnóstico, diciéndolo.",
        ],
    ),
)

ANCLA = '      <aside class="fuentes-modulo" aria-label="Fuentes citadas en este módulo">'


def aplica(src):
    """Inserta cada ejercicio antes de la lista de fuentes de su módulo."""
    for mid in (1, 2, 3, 4, 5, 6, 7, 9):
        ini = src.index(f'<template id="module-{mid}">')
        fin = src.index("</template>", ini)
        pos = src.index(ANCLA, ini)
        assert pos < fin, f"módulo {mid}: no se encontró la lista de fuentes dentro de su plantilla"
        assert src.count(ANCLA, ini, fin) == 1, f"módulo {mid}: la lista de fuentes no es única"
        assert f'id="c3m{mid}-sol"' not in src, f"módulo {mid}: el ejercicio ya está"
        src = src[:pos] + CORTOS[mid] + src[pos:]
    return src
