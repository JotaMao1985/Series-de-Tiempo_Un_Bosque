"""R3 del cap. 3 · correcciones de la sesión maestra tras la verificación independiente.

Se aplica después de r3_edita.py. Cada texto de partida debe aparecer exactamente una vez.
"""
from pathlib import Path

F = Path(__file__).resolve().parents[3] / "ensamblado" / "cap3" / "cap3_modulos.html"

EDICIONES = [
    # 1 · el cap. 2 adelantó el MA(1) con theta = -1, no con +0.7
    ("""un MA(1) de $\\theta = +0.7$, el modelo
        que el Capítulo 2 adelantó; el estimador""",
     """un MA(1) de $\\theta = +0.7$; el estimador"""),
    # 2 · M7: cada módulo tiene un solo bloque, y el ejemplo solo está en la pestaña R
    ("""El último bloque de código de abajo lo
        reproduce con $T = 40$""",
     """El código R de abajo lo
        reproduce con $T = 40$"""),
    # 2 · M8: ídem
    ("""El efecto se mide en el último bloque de código de este módulo: con tres mil""",
     """El efecto se mide en el código R de este módulo: con tres mil"""),
    # 3 · M5: la cifra ya se dijo en el párrafo que precede al plegado
    ("""su cociente,
            $\\rho_1 = 0.8308$ — la primera de las cuatro cifras que el Módulo 4 había obtenido sumando pesos
            $\\psi$.</p>""",
     """su cociente,
            $\\rho_1 = 0.8308$.</p>"""),
    # 4 · M8: el Monte Carlo ya está a la vista antes del plegado
    ("""<p>El efecto es medible. Ajustando un AR(2) a $3000$ series que de verdad son AR(2), con $T = 100$ y
                $h = 12$, la prueba al 5&nbsp;% rechaza el $4.9$&nbsp;% de las veces con <code>fitdf = 2</code> y solo
                el $2.6$&nbsp;% sin él: la mitad de lo que debería. El código R de abajo lo reproduce.</p>""",
     """<p>Sin el descuento la prueba rechaza cerca de la mitad de lo que debería: es el Monte Carlo del
                párrafo anterior a este desarrollo.</p>"""),
    # 7 · M9: el bloque también calcula cifras de la serie cruda
    ("""<p>Las cifras del caso sobre la raíz cuadrada salen de este bloque, en el orden en que aparecen; las de la serie cruda, de los bloques de los Módulos 7 y 8.</p>""",
     """<p>Las cifras del caso salen de este bloque, en el orden en que aparecen, incluidas las de la serie cruda que el
        caso añade (el ARMA(2,1), la asimetría y Shapiro–Wilk); las demás de la serie cruda, de los bloques de los
        Módulos 7 y 8.</p>"""),
]

texto = F.read_text(encoding="utf-8")
for viejo, nuevo in EDICIONES:
    n = texto.count(viejo)
    assert n == 1, (n, viejo[:70])
    texto = texto.replace(viejo, nuevo)
F.write_text(texto, encoding="utf-8")
print(f"{len(EDICIONES)} sustituciones aplicadas")
