#!/usr/bin/env python3
"""R1 del cap. 4 · correcciones de la sesión maestra tras la verificación independiente.

Sustituciones únicas (cada texto viejo debe aparecer exactamente una vez). Cifras:
r1_maestra.out, v1_comprobaciones.out y v1_aic_r.out. El M11 se devolvió aparte a su
texto de 7e9bc58 (hallazgo 1: no consta que el quiz se haya aplicado).
"""
import pathlib, sys
R = pathlib.Path(__file__).resolve().parents[3]
E = R / "ensamblado/cap4"
D = R / "Htmls_Series/diapositivas/fuentes/capitulo_4.md"

CAMBIOS = [
 # 2 · ejercicio 1, pista y solución: r1 positivo no prueba que no sobre la diferencia
 (E/"templates_10.html",
  """Para $d$, mira el gráfico y las pruebas, y comprueba que con $d = 1$ no aparecen
            los síntomas de haber diferenciado de más: el $\\hat\\rho_1$ de la serie diferenciada, lejos de $-0.5$. Para el""",
  """Para $d$, mira el gráfico y las pruebas. El $\\hat\\rho_1$ de la serie diferenciada es solo
            un indicio, que falla en los dos sentidos (Módulo 2.7): no basta para decir que la diferencia sobra ni que
            hace falta. Para el"""),
 (E/"templates_10.html",
  "# con d = 1, r1 positivo: no sobra nada; con d = 2 ya ronda -0.5",
  "# un indicio, no una regla (Modulo 2.7): con d = 1 no avisa; con d = 2 ronda -0.5"),
 # 3 · la tercera evidencia, con la salvedad del cap. 2; 4 · 1.144 frente a 1.364
 (E/"templates_1_3.html",
  """<td>En la serie
              diferenciada, $\\hat\\rho_1$ cerca de $-0.5$ o por debajo; en el modelo ajustado, una raíz MA cerca
              de $1$</td><td>Con $d = 1$, $\\hat\\rho_1 = -0.402$, no muy lejos de $-0.5$; con $d = 2$, $-0.626$, ya
              por debajo. La raíz MA del modelo con $d = 1$ queda en $1.144$, cerca del círculo (Módulo 8).</td></tr>""",
  """<td>En el modelo
              ajustado, una raíz MA cerca de $1$. En la serie diferenciada, un $\\hat\\rho_1$ cerca de $-0.5$ o por debajo es
              solo un indicio: falla en los dos sentidos (Módulo 2.7)</td><td>Con $d = 1$, $\\hat\\rho_1 = -0.402$, no muy
              lejos de $-0.5$; con $d = 2$, $-0.626$, ya por debajo. La raíz MA del ARIMA($1,1,1$) queda en $1.144$
              (Módulo 6), más cerca del círculo que la del MA(1) del Módulo 8, en $1.364$; ninguna está sobre
              él.</td></tr>"""),
 (E/"templates_7_9.html",
  """raíz: el ARIMA($2,1,1$) sobre esa serie da $|\\text{raíz MA}| = 1.000$. <strong>Hay que mirar siempre las
          raíces</strong>, junto con el $\\hat\\rho_1$ de la serie diferenciada. (Es el ejercicio 2 de este
          capítulo.)</p>""",
  """raíz: el ARIMA($2,1,1$) sobre esa serie da $|\\text{raíz MA}| = 1.000$. <strong>Hay que mirar siempre las
          raíces.</strong> El $\\hat\\rho_1$ de la serie diferenciada no avisa aquí: vale $0.565$, positivo y lejos de
          $-0.5$, que es la manera en que ese indicio falla (Módulo 2.7). (Es el ejercicio 2 de este
          capítulo.)</p>"""),
 (E/"templates_10.html",
  """el círculo unitario, sin pareja en el AR. Antes de ajustar ya avisa el $\\hat\\rho_1$ de la serie
            diferenciada, cuando se acerca a $-0.5$ o lo pasa.</li>""",
  """el círculo unitario, sin pareja en el AR. Antes de ajustar puede avisar el $\\hat\\rho_1$ de la serie
            diferenciada, cuando se acerca a $-0.5$ o lo pasa, pero es un indicio que falla en los dos sentidos
            (Módulo 2.7): en <code>log(lynx)</code> no avisa.</li>"""),
 # 5 · el divisor de Arima()
 (E/"templates_10.html",
  "los residuales entre $n^* - k$ y <code>arima()</code>",
  "los residuales entre $n^* - p - q$ ($97$ en el Nilo) y <code>arima()</code>"),
 # 6 · el AIC de R a tres decimales
 (E/"templates_7_9.html", "(1267.219 aqui, 1267.254 en R)", "(1267.219 aqui, 1267.255 en R)"),
 # 7 · quiz, ítem 6
 (E/"chapter.js",
  "pasado el rezago 3, sigue rondando $0.2$ hasta el 20 (aún $0.237$ en el 13)",
  "pasado el rezago 3, sigue fuera de la banda en $8$ de los $17$ rezagos que quedan hasta el 20 (aún $0.237$ en el 13)"),
 # 8 · el paréntesis del Ljung–Box de Python
 (E/"templates_1_3.html",
  """#   R da 0.7997: sus residuales no son los mismos (el primero, 1.12, es el
#   rastro de su propio arranque). La conclusion no cambia: no rechaza.""",
  """#   R da 0.7997 (0.8118 sin su primer residual, 1.12): ni los coeficientes
#   ni el arranque son identicos. La conclusion no cambia: no rechaza."""),
 # 9 · el 1.71 y el 0.76, impresos
 (E/"templates_4_6.html",
  "# AICc prefiere (1,1,1) por 1.71; BIC prefiere (0,1,1) por 0.76</code></pre>",
  """# AICc prefiere (1,1,1) y BIC prefiere (0,1,1), por:
with(subset(rejilla, modelo %in% c("ARIMA(0,1,1)", "ARIMA(1,1,1)")),
     round(c(aicc = -diff(aicc), bic = diff(bic)), 2))
#&gt; aicc  bic 
#&gt; 1.71 0.76 </code></pre>"""),
 # 3 · diapositiva de las tres evidencias
 (D,
  "| **3. Síntomas de diferenciar de más** | \\(\\hat\\rho_1\\) de la serie diferenciada cerca de −0.5 o por debajo; raíz MA cerca de 1 |",
  "| **3. Síntomas de diferenciar de más** | Raíz MA cerca de 1 en el modelo ajustado; \\(\\hat\\rho_1\\) de la diferenciada cerca de −0.5, solo como indicio |"),
]

def main():
    fallos = 0
    textos = {}
    for p, viejo, nuevo in CAMBIOS:
        t = textos.setdefault(p, p.read_text("utf-8"))
        n = t.count(viejo)
        if n != 1:
            print(f"FALLA {p.name}: aparece {n} veces: {viejo[:70]!r}"); fallos += 1; continue
        textos[p] = t.replace(viejo, nuevo, 1)
    if fallos:
        return 1
    for p, t in textos.items():
        p.write_text(t, "utf-8")
    print(f"OK {len(CAMBIOS)} sustituciones en {len(textos)} archivos")
    return 0

sys.exit(main())
