#!/usr/bin/env python3
"""R1 del capítulo 5 · correcciones de la sesión maestra tras los verificadores A y B.

Cada edición es (archivo, antes, después, hallazgo). Es idempotente: si `después` ya está y `antes`
no, la salta; si `antes` no aparece exactamente una vez, se detiene. Después hay que reensamblar
(`ensambla_cap5.py`, `ensambla_cap6.py`) y reconstruir el deck.

Uso (desde la raíz del repo):  python3 diagnostico/cap5/comprobaciones/r1_ediciones_maestra.py
"""
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
T13 = "ensamblado/cap5/templates_1_3.html"
T46 = "ensamblado/cap5/templates_4_6.html"
T79 = "ensamblado/cap5/templates_7_9.html"
T1011 = "ensamblado/cap5/templates_10_11.html"
JS = "ensamblado/cap5/chapter.js"
ENS = "ensamblado/ensambla_cap5.py"
DECK = "Htmls_Series/diapositivas/fuentes/capitulo_5.md"
VER = "Htmls_Series/diapositivas/fuentes/verificacion/verifica_cifras_cap5.py"

EDICIONES = [
    # --- A1 · el criterio del error estándar es una señal, no un veredicto ---------------------------
    (JS,
     "valor: alarma ? '⚠ −1 dentro de Θ̂ ± 1.96 e.e.: sobra una diferencia estacional' : 'Θ̂ lejos de −1: no sobra ninguna diferencia' }",
     "valor: alarma ? '⚠ −1 dentro de Θ̂ ± 1.96 e.e.: señal de que puede sobrar una diferencia estacional; vuelve a mirar D'\n"
     "            : (D === 0 ? 'Θ̂ lejos de −1: no sobra nada, pero falta ∇₁₂ (la estacionalidad sigue en la serie)'\n"
     "                       : 'Θ̂ lejos de −1: ninguna señal de diferencia de más') }",
     "A1"),
    (T13,
     "y avisa cuando $-1$ cae dentro del intervalo $\\hat\\Theta \\pm 1.96\\,\\text{e.e.}$</p>",
     "y avisa cuando $-1$ cae dentro del intervalo $\\hat\\Theta \\pm 1.96\\,\\text{e.e.}$ El aviso es una señal para\n"
     "          volver a mirar $D$, no un veredicto: un $\\Theta$ verdadero cercano a $-1$, sin ninguna diferencia de más,\n"
     "          también da distancias pequeñas, y en la frontera el error estándar es poco fiable.</p>",
     "A1"),
    (T13,
     "$\\hat\\Theta = -0.5569$ está a $6.06$ errores estándar de $-1$, y no sobra nada.",
     "$\\hat\\Theta = -0.5569$ está a $6.06$ errores estándar de $-1$, y no sobra nada. Con $D=0$ la distancia también\n"
     "        es grande, pero por otra razón: ahí no sobra nada, <em>falta</em> $\\nabla_{12}$, como dice el\n"
     "        $\\hat\\rho_{12} = 0.841$ de la tabla de las cuatro combinaciones. La distancia es una señal, no un veredicto: con una serie de\n"
     "        esta longitud, un $\\Theta$ verdadero cercano a $-1$ tampoco se distingue de $-1$ aunque no sobre nada, y\n"
     "        cerca de $-1$ el error estándar deja de ser fiable. Si salta, se vuelve a la etapa 2 y se mira $D$ con\n"
     "        <code>nsdiffs()</code> y la ACF.",
     "A1"),
    (ENS,
     "\"vuelta\": \"<p>Si al estimar sale $\\\\hat\\\\Theta$ pegado a $-1$ —tan cerca que su error \"\n"
     "                  \"estándar no lo distingue de $-1$—, sobraba una diferencia estacional.</p>\",",
     "\"vuelta\": \"<p>Si al estimar sale $\\\\hat\\\\Theta$ pegado a $-1$ —tan cerca que su error \"\n"
     "                  \"estándar no lo distingue de $-1$—, puede sobrar una diferencia estacional: \"\n"
     "                  \"se vuelve a mirar $D$ con la ACF y la prueba. Es una señal, no un veredicto: \"\n"
     "                  \"un $\\\\Theta$ verdadero cercano a $-1$ da lo mismo.</p>\",",
     "A1"),
    (ENS,
     "\"vuelta\": \"<p>Si $\\\\hat\\\\theta$ sale pegado a $-1$, sobra la diferencia regular. La \"",
     "\"vuelta\": \"<p>Si $\\\\hat\\\\theta$ sale pegado a $-1$, puede sobrar la diferencia regular. La \"",
     "A1"),
    (T1011,
     "<tr><td>Sobrediferenciar deja firma algebraica: $\\hat\\Theta$ (o $\\hat\\theta$) pegado a $-1$, indistinguible de $-1$ con su error estándar; la varianza no decide</td>",
     "<tr><td>Sobrediferenciar deja firma algebraica: $\\hat\\Theta$ (o $\\hat\\theta$) pegado a $-1$, indistinguible de $-1$ con su error estándar. Es una señal para volver a mirar $D$ o $d$, no un veredicto; la varianza no decide</td>",
     "A1"),
    # --- A2 · E3(b): el p-valor no ordena modelos; los armónicos quedan en el borde --------------------
    (T1011,
     "(b) El\n            <em>airline</em>, pero no por el AICc: esos dos AICc no son comparables. Lo que lo decide es el\n"
     "            diagnóstico: el mejor armónico por AICc no pasa Ljung–Box y el <em>airline</em> sí.</strong></p>",
     "(b) El\n            <em>airline</em>, pero no por el AICc: esos dos AICc no son comparables. Dentro de muestra, el\n"
     "            diagnóstico inclina la balanza sin cerrarla: el <em>airline</em> pasa Ljung–Box con holgura y los armónicos\n"
     "            quedan en el borde; la decisión firme se toma fuera de muestra.</strong></p>",
     "A2"),
    (T1011,
     "# Lo que SI se compara entre familias: el diagnostico (no depende del n efectivo)",
     "# Lo que si se puede mirar en las dos familias: el diagnostico (no depende del n\n"
     "# efectivo). No ordena modelos: dice si en los residuales queda estructura.",
     "A2"),
    (T1011,
     "Lo\n            que sí se puede comparar entre familias es el diagnóstico, porque Ljung–Box no depende del $n$ efectivo de\n"
     "            la verosimilitud: el mejor armónico por AICc ($K=4$) lo rechaza al $5\\,\\%$ ($p = 0.0439$), ninguno de los\n"
     "            seis llega al $p = 0.4081$ del <em>airline</em>, y el <em>airline</em> lo pasa. Por eso se elige el\n"
     "            <em>airline</em>. Para decidir de verdad entre las dos familias, fuera de muestra, hace falta el\n"
     "            Capítulo 6.</p>",
     "Lo\n            que sí se puede mirar en las dos familias es el diagnóstico, que no depende del $n$ efectivo de la\n"
     "            verosimilitud: el <em>airline</em> pasa Ljung–Box sin apuros ($p = 0.4081$), y los armónicos quedan en el\n"
     "            borde —el $K=4$, el de menor AICc, lo rechaza al $5\\,\\%$ ($p = 0.0439$), y los $K=5$ y $K=6$ lo pasan\n"
     "            por poco ($p = 0.0516$ y $0.0515$)—. Ese $p$-valor no ordena modelos: solo dice si en los residuales queda\n"
     "            estructura. Con lo que hay dentro de muestra, el <em>airline</em> —dos parámetros y residuales sin\n"
     "            estructura— es la elección prudente; decidir de verdad entre las dos familias exige compararlas fuera de\n"
     "            muestra, que es el Capítulo 6.</p>",
     "A2"),
    # --- A3, A4 · M5 -------------------------------------------------------------------------------------
    (T46,
     "Aquí no: $(1-B^{12})$ ya contiene a $(1-B)$\n        (Módulo 3), así que",
     "Aquí no: $(1-B^{12}) = (1-B)(1+B+\\dots+B^{11})$ ya\n        contiene a $(1-B)$, así que",
     "A4"),
    (T46,
     "La varianza del error crece entonces como $h^3$, no como $h$,",
     "La varianza del error crece entonces, a la larga, como $h^3$, no como $h$,",
     "A3"),
    # --- A5 · M6: el 13.º residual de arranque no es casi nulo --------------------------------------------
    (T46,
     "# Los d + D*m = 13 primeros residuales de R son de arranque, casi nulos: sin\n"
     "# ellos el p-valor cambia, y la conclusion no.",
     "# Los d + D*m = 13 primeros residuales de R son de arranque (los doce primeros,\n"
     "# casi nulos): sin ellos el p-valor cambia, y la conclusion no.",
     "A5"),
    (T46,
     "R deja 13 residuales casi\n# nulos y statsmodels",
     "R deja 13 residuales de\n# arranque (los doce primeros, casi nulos) y statsmodels",
     "A5"),
    # --- A6, A7, A8 · M3 -----------------------------------------------------------------------------------
    (T13,
     "<td>$\\mathbf{0.002102}$</td>",
     "<td>$0.002102$</td>",
     "A6"),
    (T13,
     "se acerca a $2(1-\\hat\\rho_1)$ —y, por la misma cuenta, el\n"
     "        de $\\nabla_{12}$ a $2(1-\\hat\\rho_{12})$—, así que la varianza repite lo que ya dice la ACF; por eso el\n"
     "        Capítulo 4 no la cuenta como evidencia.",
     "se acerca a $2(1-\\hat\\rho_1)$: la varianza repite lo que ya dice la ACF y no aporta una\n"
     "        evidencia aparte (la cuenta es para series estacionarias, y por eso no cuadra con las filas de esta tabla); por\n"
     "        eso el Capítulo 4 no la cuenta como evidencia.",
     "A7"),
    (T13,
     "# |raiz MA|^-1 = |Theta|^(1/12): cerca de 1 en las tres filas, no separa nada.",
     "# |raiz MA|^-1 = |Theta|^(1/12) comprime la escala hacia 1 y separa mal; Theta no.",
     "A8"),
    # --- A11, A12 · M1 y M2 --------------------------------------------------------------------------------
    (T13,
     "y unas pocas menores sin patrón, que el\n          Módulo 7 discute.",
     "y unas pocas menores sin patrón; el\n          Módulo 7 discute las que caen dentro de los $24$ rezagos que mira Ljung–Box.",
     "A11"),
    (T13,
     "phi &lt;- 0.9                     # el caso de la fila en negrita",
     "phi &lt;- 0.9                     # el caso phi = 0.9 de la tabla",
     "A12"),
    # --- A9, A10 · Python del M8 y del M9 --------------------------------------------------------------------
    (T79,
     "# 1.0844, con menor verosimilitud); con BFGS llega.",
     "# 1.0844, con menor verosimilitud), y aun asi mle_retvals dice que convergio: el\n"
     "# aviso no basta, conviene repetir con otro optimizador y comparar la\n"
     "# verosimilitud. Con BFGS llega.",
     "A9"),
    (T79,
     "import numpy as np, pandas as pd, statsmodels.api as sm, warnings\nfrom statsmodels.tsa.statespace.sarimax import SARIMAX\n"
     "warnings.filterwarnings(\"ignore\")\n\n# --- USAccDeaths ---",
     "import numpy as np, pandas as pd, statsmodels.api as sm, warnings\nfrom statsmodels.tsa.statespace.sarimax import SARIMAX\n"
     "warnings.simplefilter(\"ignore\", RuntimeWarning)   # avisos de numpy; los de convergencia, no\n\n# --- USAccDeaths ---",
     "A10"),
    (T79,
     "#&gt; 0.0013 0.015\n# t practicamente cero: el parametro estacional no aporta nada.",
     "#&gt; 0.0013 0.015\n# t practicamente cero: el parametro estacional no aporta nada.\n"
     "print(f.mle_retvals[\"converged\"], g.mle_retvals[\"converged\"])\n#&gt; True True",
     "A10"),
    # --- B1 · SARIMAX: el mismo modelo; diferenciar literalmente, solo con simple_differencing=True ----------
    (T79,
     "<code>SARIMAX</code> con <code>exog</code> ajusta este\n"
     "          mismo modelo, igual que <code>Arima(…, xreg = )</code> en R; con $d$ o $D$ mayores que $0$, los dos\n"
     "          diferencian a la vez la serie y los regresores.</p>",
     "<code>SARIMAX</code> con <code>exog</code> es este\n"
     "          mismo modelo, igual que <code>Arima(…, xreg = )</code> en R. Con $d$ o $D$ mayores que $0$, equivale a\n"
     "          regresar la serie diferenciada sobre los regresores diferenciados; R lo estima así, y <code>statsmodels</code>\n"
     "          también si se le pide <code>simple_differencing=True</code>. Sin esa opción no diferencia los datos: lleva $d$\n"
     "          y $D$ dentro del espacio de estados con un <em>prior</em> difuso (Módulo 6), y con series cortas la estimación\n"
     "          se mueve (Módulo 8).</p>",
     "B1"),
    (DECK,
     "- <kbd>Definición</kbd> En statsmodels, `SARIMAX` con `exog` ajusta este mismo modelo, igual que `Arima(…, xreg = )` en R: con \\(d\\) o \\(D\\) mayores que 0, los dos diferencian la serie y los regresores",
     "- <kbd>Definición</kbd> En statsmodels, `SARIMAX` con `exog` es este mismo modelo, igual que `Arima(…, xreg = )` en R; con \\(d\\) o \\(D\\) mayores que 0 equivale a diferenciar la serie y los regresores, y statsmodels solo lo hace así con `simple_differencing=True`",
     "B1"),
    # --- deck: el criterio como señal (A1), M5 (A3, A4), diapositivas 25, 41 y 51 (B2, B3, B5), 1.96 (B7) --
    (DECK,
     "<kbd>Interpretación</kbd> La alarma se lee en la escala de \\(\\Theta\\), no en la varianza.",
     "<kbd>Interpretación</kbd> Es una señal, no un veredicto, y se lee en la escala de \\(\\Theta\\), no en la varianza.",
     "A1"),
    (DECK,
     "El simulador del Módulo 3 avisa cuando −1 cae dentro de Θ̂ ± 1.96 e. e. La varianza",
     "El simulador del Módulo 3 avisa cuando −1 cae dentro de Θ̂ ± 1.96 e. e. Es una señal para volver a mirar D, no un veredicto: un Θ verdadero cercano a −1, sin ninguna diferencia de más, también da distancias pequeñas, y cerca de −1 el error estándar es poco fiable. Con D = 0 la distancia es grande porque falta ∇₁₂, no porque sobre algo. La varianza",
     "A1"),
    (DECK,
     "- Sobrediferenciar deja firma: \\(\\hat\\Theta\\) pegado a −1, a la vista de su error estándar; la varianza no decide",
     "- Sobrediferenciar deja una señal: \\(\\hat\\Theta\\) pegado a −1, a la vista de su error estándar; la varianza no decide",
     "A1"),
    (DECK,
     "aquí (1 − B¹²) ya contiene a (1 − B), los ψ crecen como (1 + θ)(1 + Θ) = 0.265 por año y la varianza del error crece como h³.",
     "aquí (1 − B¹²) = (1 − B)(1 + B + … + B¹¹) ya contiene a (1 − B), los ψ crecen como (1 + θ)(1 + Θ) = 0.265 por año y la varianza del error crece, a la larga, como h³.",
     "A3, A4"),
    (DECK,
     "- <kbd>Definición</kbd> El salto en el rezago 12 vale \\(1+\\Theta\\)",
     "- <kbd>Interpretación</kbd> El salto en el rezago 12 vale \\(1+\\Theta\\)",
     "B3"),
    (DECK,
     "| Señal de vuelta (etapa 5) | \\(\\hat\\Theta=-0.5569\\) (e. e. 0.0731) y \\(\\hat\\theta=-0.4018\\), lejos de −1 | No sobra ninguna diferencia |",
     "| Comprobación al estimar (etapa 5) | \\(\\hat\\Theta=-0.5569\\) (e. e. 0.0731) y \\(\\hat\\theta=-0.4018\\), lejos de −1 | Ninguna señal de diferencia de más |",
     "B2"),
    (DECK,
     "Fuente: J `firma`, `orden_pruebas`, `combinaciones` · R (rango relativo: (máx − mín)/media)",
     "Fuente: J `firma`, `orden_pruebas`, `airline` · R (rango relativo: (máx − mín)/media)",
     "B2"),
    (DECK,
     "<kbd>Interpretación</kbd> La varianza de cada combinación describe; no decide \\(D\\) ni \\(d\\).",
     "<kbd>Interpretación</kbd> La varianza describe; no decide \\(D\\) ni \\(d\\).",
     "B5"),
    (VER,
     "C(K, \"1.96\", DEF_(\"cuantil 0.975 de la normal\"), kind=\"convención\")\n"
     "C(K, \"capítulo\", CH_(\"Distancia a $-1$, en e.e.\")",
     "C(K, \"1.96\", DEF_(\"cuantil 0.975 de la normal\"), CH_(\"\\\\hat\\\\Theta \\\\pm 1.96\\\\,\\\\text{e.e.}\"),\n"
     "  BOOL_(\"C\", lambda: \"a_menos_1_en_ee < 1.96\" in CAP_CRUDO, \"el simulador del Módulo 3 avisa con ese umbral\"), kind=\"convención\")\n"
     "C(K, \"capítulo\", CH_(\"Distancia a $-1$, en e.e.\")",
     "B7"),
]


def main() -> int:
    textos = {}
    hechas = saltadas = 0
    for ruta, antes, despues, hallazgo in EDICIONES:
        t = textos.setdefault(ruta, (RAIZ / ruta).read_text(encoding="utf-8"))
        if despues in t:
            saltadas += 1
            continue
        n = t.count(antes)
        if n != 1:
            print(f"FALLA {hallazgo} en {ruta}: «{antes[:70]}…» aparece {n} veces")
            return 1
        textos[ruta] = t.replace(antes, despues)
        hechas += 1
    for ruta, t in textos.items():
        (RAIZ / ruta).write_text(t, encoding="utf-8")
    print(f"OK  {hechas} ediciones aplicadas, {saltadas} ya estaban")
    return 0


if __name__ == "__main__":
    sys.exit(main())
