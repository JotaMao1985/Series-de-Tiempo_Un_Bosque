"""R3 del cap. 4 · correcciones de la sesión maestra tras la verificación independiente.

Se aplica DESPUÉS de r3_edita.py (el del redactor). Cada marcador debe aparecer una sola
vez; con --comprobar solo dice si el árbol ya las tiene. Atiende V1–V9 de
`diagnostico/cap4/R3_verificacion.md` (V10 es del informe, no del capítulo). Después hay
que reensamblar el cap. 4 (`python3 ensamblado/ensambla_cap4.py`) y los caps. 5 y 6.
"""
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
CAP4 = RAIZ / 'ensamblado/cap4'

SUST = [
    # V1 · la deriva del ARIMA(1,1,1) del Nilo NO es la media de las diferencias (−2.883 frente a
    # −3.84); solo en el ARIMA(0,1,0) coinciden.
    ('templates_10.html',
     """Como en el Nilo
          (Módulo 5), esa deriva es la media de las diferencias, $(y_n - y_1)/(n-1)$: depende solo del primer mes y
          del último.""",
     """En un
          ARIMA($0,1,0$) esa deriva es exactamente la media de las diferencias, $(y_n - y_1)/(n-1)$: depende solo
          del primer mes y del último. (En el ARIMA($1,1,1$) del Nilo no coinciden: el Módulo 5 lo muestra.)"""),
    # V2 · las introducciones de simulador del M1, el M8 y el M10 dejan de dar el resultado.
    ('templates_1_3.html',
     """Luego sube $d$ y lee los números de
          abajo, no solo el gráfico. La media cae a casi cero, porque diferenciar convierte el caudal en su cambio de
          un año al siguiente. Fíjate sobre todo en $\\hat\\rho_1$: cambia de signo, y con $d = 2$ queda por debajo
          de $-0.5$, el valor que tendría la diferencia de un ruido blanco. La varianza apenas baja con $d = 1$ y
          casi se triplica con $d = 2$, pero no es una pista aparte: el Módulo 3 explica por qué repite lo que ya
          dice $\\hat\\rho_1$. ¿Hacía falta diferenciar?</p>""",
     """Luego sube $d$ y lee los números de
          abajo, no solo el gráfico. ¿Qué le pasa a la media, si diferenciar convierte el caudal en su cambio de un
          año al siguiente? Fíjate sobre todo en $\\hat\\rho_1$: ¿cambia de signo? ¿Con qué $d$ baja de $-0.5$, el
          valor que tendría la diferencia de un ruido blanco? La varianza también cambia, pero no es una pista
          aparte: el Módulo 3 explica por qué repite lo que ya dice $\\hat\\rho_1$. ¿Hacía falta diferenciar?</p>"""),
    ('templates_7_9.html',
     """Sube el orden $d$ sobre el Nilo y ajusta un MA(1) a cada resultado. En $d = 2$ y
          $d = 3$ el $\\hat\\theta$ se clava en $-1$ y $|\\text{raíz MA}| = 1$: el término MA está deshaciendo la
          diferencia que acabas de imponer.</p>""",
     """Sube el orden $d$ sobre el Nilo y ajusta un MA(1) a cada resultado. ¿Con qué $d$
          llega $\\hat\\theta$ a $-1$? ¿Qué le pasa entonces a $|\\text{raíz MA}|$, y qué dice el diagnóstico?</p>"""),
    ('templates_7_9.html',
     """      <p>Hay una prueba más de que el MA está deshaciendo la diferencia.""",
     """      <p>En $d = 2$ y $d = 3$ el $\\hat\\theta$ se clava en $-1$ y la raíz MA queda sobre el círculo unidad: el
        término MA está deshaciendo la diferencia que se acaba de imponer.</p>

      <p>Hay una prueba más de que el MA está deshaciendo la diferencia."""),
    ('templates_10.html',
     """La ACF de la serie en niveles arranca en $0.964$ y decae lentísimo: el retrato
          de un proceso no estacionario. Tras una diferencia solo una barra de veinte se sale, y por poco:
          $\\hat\\rho_8 = -0.190$ frente a $\\pm 0.167$, que es lo que el azar da al $5\\,\\%$. Cambia de serie y
          compara.</p>""",
     """Empieza por la serie en niveles: ¿cómo arranca su ACF y a qué ritmo decae?
          Cambia luego a la diferencia y cuenta cuántas de las veinte barras salen de la banda, que es lo que el azar
          da al $5\\,\\%$, y por cuánto.</p>"""),
    ('templates_10.html',
     """                <strong>1. Identificación de $d$</strong></td>
              <td class="block lg:table-cell pt-0 lg:pt-4">
                ADF""",
     """                <strong>1. Identificación de $d$</strong></td>
              <td class="block lg:table-cell pt-0 lg:pt-4">
                La ACF en niveles arranca en $0.964$ y decae lentísimo: el retrato de un proceso no estacionario.
                ADF"""),
    # V3 · «estimados», como el M1.
    ('templates_7_9.html',
     """        coeficientes reales <em>casi no cambia la varianza</em>""",
     """        coeficientes estimados <em>casi no cambia la varianza</em>"""),
    # V4 · auto.arima, presentado en su propia oración.
    ('templates_1_3.html',
     """Y el valor por
          defecto de <code>ndiffs()</code> —y por tanto el que usa <code>auto.arima()</code>, la función de
          <code>forecast</code> que ajusta sola varios ARIMA y se queda con el de menor AICc, y que el Módulo 7
          abre— es KPSS, la única que dice que sí.""",
     """Y el valor por
          defecto de <code>ndiffs()</code> es KPSS, la única que dice que sí. Es también el que usa
          <code>auto.arima()</code>, la función de <code>forecast</code> que ajusta sola varios ARIMA y se queda
          con el de menor AICc; el Módulo 7 la abre."""),
    # V5 · la raíz 1.144 ya la imprime el M1.
    ('templates_1_3.html',
     """queda en $1.144$
              (Módulo 6), más cerca""",
     """queda en $1.144$
              (Módulos 1 y 6), más cerca"""),
    # V6 · la trampa de la PACF la dice el párrafo previo al simulador; el recuadro no la repite.
    ('templates_4_6.html',
     """<strong>Lo que enseña el simulador.</strong> Con $d = 0$ la trampa está en la
          PACF: solo se sale el rezago 1, como en un AR(1) con $\\phi \\approx 0.5$, pero ese AR(1) tendría la ACF
          dentro de la banda desde el rezago 3, y esta decae despacio: es lo que deja un nivel que se mueve, por
          una raíz unitaria o por un cambio de nivel como el de 1899. Con $d = 2$,""",
     """<strong>Lo que enseña el simulador.</strong> Con $d = 0$, la trampa del párrafo
          de arriba: un AR(1) con $\\phi \\approx 0.5$ tendría la ACF dentro de la banda desde el rezago 3, y esta
          decae despacio. Con $d = 2$,"""),
    # V7 · 127.03 es la desviación típica de los residuales (divisor n − 1), no el σ̂ de ML (126.39).
    ('templates_1_3.html',
     """($n = 100$,
        $\\hat\\sigma = 127.0$)""",
     """($n = 100$,
        desviación típica $127.0$)"""),
    ('templates_1_3.html',
     """        beta = coef(dos_medias)[["escalon"]], sigma = sd(residuals(dos_medias))), 2)
#&gt;   antes despues    beta   sigma
#&gt; 1097.75  849.97 -247.78  127.03""",
     """        beta = coef(dos_medias)[["escalon"]], sd_resid = sd(residuals(dos_medias))), 2)
#&gt;    antes  despues     beta sd_resid
#&gt;  1097.75   849.97  -247.78   127.03"""),
    ('templates_1_3.html',
     """rnorm(100, 0, 127.03)    # sigma de arriba""",
     """rnorm(100, 0, 127.03)    # sd_resid de arriba"""),
    # V8 · el α del IMA(1,1) es el implícito; ses() estima el suyo.
    ('templates_4_6.html',
     """        simple con $\\alpha = 1 + \\hat\\theta = 0.267$.</p>""",
     """        simple con $\\alpha = 1 + \\hat\\theta = 0.267$: es el $\\alpha$ implícito en el modelo; <code>ses()</code>
        lo estima por su cuenta y da un valor algo distinto.</p>"""),
    # V9 · «termina» y «se cumplen».
    ('templates_10.html',
     """El capítulo termina con un
        experimento que muestra""",
     """El puente es un
        experimento que muestra"""),
    ('templates_10.html',
     """A un mes, los dos intervalos se cumplen dentro
        de la muestra:""",
     """A un mes, ninguno de los dos intervalos queda
        corto dentro de la muestra:"""),
]


def main():
    comprobar = '--comprobar' in sys.argv
    textos = {}
    faltan = 0
    for archivo, viejo, nuevo in SUST:
        ruta = CAP4 / archivo
        texto = textos.setdefault(archivo, ruta.read_text(encoding='utf-8'))
        n_viejo, n_nuevo = texto.count(viejo), texto.count(nuevo)
        if comprobar:
            if n_nuevo != 1:
                faltan += 1
                print('FALTA:', archivo, nuevo.strip().splitlines()[0][:90])
            continue
        if n_nuevo == 1 and n_viejo == 0:
            continue
        if n_viejo != 1:
            sys.exit(f'marcador no único ({n_viejo}) en {archivo}: {viejo.strip().splitlines()[0][:90]}')
        textos[archivo] = texto.replace(viejo, nuevo)
    if comprobar:
        print('OK' if not faltan else f'{faltan} sin aplicar')
        sys.exit(1 if faltan else 0)
    for archivo, texto in textos.items():
        (CAP4 / archivo).write_text(texto, encoding='utf-8')
    print(f'{len(SUST)} sustituciones aplicadas')


if __name__ == '__main__':
    main()
