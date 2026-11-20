"""R1 del cap. 3 · correcciones de la sesión maestra tras la verificación independiente.
Cifras en comprobaciones/maestra_r1.R · .out. Cada sustitución debe aparecer exactamente una vez."""
from pathlib import Path
F = Path("ensamblado/cap3/cap3_modulos.html"); J = Path("ensamblado/cap3/cap3_js.js")
S = [
 (F, "diagnóstico falla en todas las ventanas que llegan al siglo XX, tengan más datos que la de Yule o\n              menos.</strong></p>",
     "diagnóstico falla en la mayoría de las ventanas de cien años, incluidas todas las que llegan al siglo XX,\n              tengan más datos que la de Yule o menos.</strong></p>"),
 (F, "<li><strong>El diagnóstico se derrumba</strong> en cuanto la ventana llega al siglo XX:",
     "<li><strong>El diagnóstico se derrumba</strong> en todas las ventanas que llegan al siglo XX:"),
 (F, "De las 190 ventanas de cien años\n              que caben entre 1700 y 1988, el AR(2) pasa la prueba en 52, y todas menos una empiezan entre 1734 y\n              1785. La de Yule es una de las favorables;",
     "De las 190 ventanas de cien años\n              que caben entre 1700 y 1988, el AR(2) pasa la prueba en 52, y todas menos una empiezan entre 1734 y\n              1785; falla en las otras 138, también en 49 que acaban antes de 1900. La de Yule es una de las favorables;"),
 (F, "en mil simulaciones iguales CSS pasa de $1$ entre un 3 y un 5&nbsp;% de las\n                veces, según la semilla— y ML no lo hace en ninguna,",
     "en mil simulaciones iguales CSS pasa de $1$ entre un 2.5 y un 4.6&nbsp;% de las\n                veces, según la semilla— y ML no lo hace en ninguna de las que estima,"),
 (F, "Quedarse dentro no es quedarse lejos:\n                en un 13&nbsp;% de esas simulaciones la estimación ML es $\\ge 0.999$.</p>",
     "Quedarse dentro no es quedarse lejos:\n                en un 13 a 17&nbsp;% de las simulaciones la estimación ML es $\\ge 0.999$, y en 4 a 13 de cada mil el\n                optimizador no llega a dar estimación.</p>"),
 (F, "Solo con la búsqueda exhaustiva\n        (<code>stepwise = FALSE, approximation = FALSE</code>), que prueba modelos a los que la búsqueda por pasos\n        no llega, devuelve un MA(1), también sin media:</p>",
     "Solo con la búsqueda exhaustiva\n        (<code>stepwise = FALSE</code>; <code>approximation = FALSE</code> no cambia nada aquí, porque con 137 datos ya\n        es su valor por defecto), que prueba modelos a los que la búsqueda por pasos no llega, devuelve un MA(1),\n        también sin media:</p>"),
 (J, "etiqueta: 'Envolvente ±Rʲ/sen ω:',", "etiqueta: 'Envolvente ±Rʲ/sin ω:',"),
 (J, "y 1/sen ω = ${factor.toFixed(3)}", "y 1/sin ω = ${factor.toFixed(3)}"),
 (F, "<strong>Otra fórmula para «el periodo».</strong> FPP3 (sección 9.5) da",
     "<strong>Otra fórmula para «el periodo».</strong> El texto de Hyndman y Athanasopoulos (FPP3, sección 9.5) da"),
]
for f, a, b in S:
    h = f.read_text(encoding="utf-8")
    assert h.count(a) == 1, (f.name, h.count(a), a[:60])
    f.write_text(h.replace(a, b), encoding="utf-8")
print(len(S), "sustituciones")
