#!/usr/bin/env python3
"""Correcciones de la sesion maestra a la R5 del cap. 3, tras la verificacion independiente
(diagnostico/cap3/R5_verificacion.md). Cada sustitucion debe aparecer exactamente una vez.
Cifras: diagnostico/cap3/comprobaciones/maestra_r5.R · .out."""
import pathlib, sys
R = pathlib.Path(__file__).resolve().parents[3]
M = R / "ensamblado/cap3/cap3_modulos.html"
J = R / "ensamblado/cap3/cap3_js.js"
B = R / "diagnostico/cap3/comprobaciones/r5_bloques"
C = R / "diagnostico/cap3/comprobaciones/r5_cifras.R"

EDICIONES = {
M: [
 # 1 · M7: sin comparar las sigma^2 de YW y ML (el modulo lo desaconseja, c3-m7-14)
 ("<li>Los coeficientes por Yule–Walker, por CSS y por máxima verosimilitud, y las tres $\\hat\\sigma^2$.</li>",
  "<li>Los coeficientes por Yule–Walker, por CSS y por máxima verosimilitud.</li>"),
 ("round(c(YW = yw$var.pred, CSS = css$sigma2, ML = ml$sigma2), 4)   # las tres sigma^2\n#&gt;     YW    CSS     ML\n#&gt; 0.0658 0.0647 0.0637\n", ""),
 ("$(0.1388,\\ 0.2140)$. Las $\\hat\\sigma^2$ son $0.0658$, $0.0647$ y $0.0637$.</p>", "$(0.1388,\\ 0.2140)$.</p>"),
 # 1 y 9 · M7 (b)
 ("y que Yule–Walker está sesgado hacia el interior de la región estacionaria: con las raíces lejos de la frontera, ese sesgo apenas se nota. Lo mismo pasa con las $\\hat\\sigma^2$: la de Yule–Walker es aquí un $3\\,\\%$ mayor que la de máxima verosimilitud; en las manchas lo era un $30\\,\\%$.</p>",
  "y que Yule–Walker está sesgado hacia el interior de la región estacionaria con muestras cortas. Aquí la muestra es igual de corta y el sesgo apenas se nota: lo que cambia es lo lejos que están las raíces de la frontera, y (c) lo comprueba. Las $\\hat\\sigma^2$ no entran en la comparación: como advierte el módulo, la de Yule–Walker y la de máxima verosimilitud no salen del mismo cálculo.</p>"),
 # 8 · M4 (a)
 ("un promedio de las observaciones pasadas con pesos que se reducen a la mitad a cada paso atrás y que suman $0.6$.</p>",
  "una suma ponderada de las observaciones pasadas, con pesos que se reducen a la mitad a cada paso atrás y que suman $0.6$, no $1$: el pronóstico se encoge hacia la media del proceso, que aquí es $0$.</p>"),
 # 5 · M9: Ljung-Box dicho entero
 ("ni arregla Ljung–Box; lo que arregla es la normalidad de los residuales.</strong></p>",
  "ni arregla Ljung–Box —en logaritmos no lo pasa ningún candidato, y el AR(4), que lo pasaba en la serie cruda, deja de pasarlo—; lo que arregla es la normalidad de los residuales.</strong></p>"),
 ("Ljung–Box, en cambio, no mejora: el AR(2) da $p = 0.031$ en la serie cruda y $p = 0.013$ en logaritmos, y en logaritmos ninguno de los once candidatos pasa la prueba (el AR(4) da $p = 0.009$). La transformación era necesaria y arregló lo que era de escala; la autocorrelación que queda en los residuales no es de escala, y ningún ARMA de la rejilla la recoge.",
  "Ljung–Box, en cambio, no mejora, y en el modelo que elige el AICc empeora: el AR(2) da $p = 0.031$ en la serie cruda y $p = 0.013$ en logaritmos; el AR(4) pasa en la serie cruda ($p = 0.064$) y deja de pasar en logaritmos ($p = 0.009$), y en logaritmos ninguno de los once candidatos pasa la prueba. La transformación era necesaria y arregló la normalidad; la autocorrelación que queda en los residuales de la serie transformada no la recoge ningún ARMA de la rejilla."),
 # 6 · M9: el aviso que suppressWarnings esconde, dicho
 ("compara &lt;- function(x) do.call(rbind, lapply(rejilla, function(pq) {\n  aj &lt;- suppressWarnings(",
  "# en log(lynx), el ARMA(2,1) avisa de un posible problema de convergencia (optim code = 1);\n# no lo elige ningun criterio, y suppressWarnings() solo calla ese aviso\ncompara &lt;- function(x) do.call(rbind, lapply(rejilla, function(pq) {\n  aj &lt;- suppressWarnings("),
 # 7 · M6 (c): la banda ensanchada, con su fuente (Cryer y Chan, ec. 6.1.9)
 ("y la banda del ruido blanco se queda estrecha. Ensanchándola con $\\rho_1$, a $\\pm 1.96\\sqrt{(1 + 2\\rho_1^2)/T} = \\pm 0.168$ en lugar de $\\pm 0.139$, el recuento baja",
  "y la banda del ruido blanco se queda estrecha. <span data-afirma=\"c3-m6-09\">En un MA(1), la varianza de $r_k$ para $k > 1$ es aproximadamente $(1 + 2\\rho_1^2)/T$ <cite class=\"cita\" data-ref=\"cryer2008time\" data-loc=\"p. 111\"></cite>, y la banda ensanchada es $\\pm 1.96\\sqrt{(1 + 2\\rho_1^2)/T}$.</span> Con ella, $\\pm 0.168$ en lugar de $\\pm 0.139$, el recuento baja"),
 # 12 · E3: el control lo descubre el apartado (c), no el enunciado
 ("1870–1988, 1900–1988 y 1889–1988, que tiene\n          los mismos cien años que la ventana del módulo. Entrega",
  "1870–1988, 1900–1988 y 1889–1988. Entrega"),
],
J: [
 # 3 · P2: la retro no adelanta la P3
 (" Entonces $\\\\gamma_1 = 4\\\\,(0.6 - 0.18) = 1.68$. Dos observaciones separadas por más de dos periodos ya no comparten ninguno: es la memoria finita del MA.'",
  " Entonces $\\\\gamma_1 = 4\\\\,(0.6 - 0.18) = 1.68$.'"),
 # 2 · P4: otro proceso (psi1 = 0.4; la practica del M4 tiene psi1 = 0.3)
 ("$\\\\phi = 0.6$, $\\\\theta = -0.3$ y $\\\\sigma^2 = 5$. ¿Cuánto vale la varianza", "$\\\\phi = 0.6$, $\\\\theta = -0.2$ y $\\\\sigma^2 = 5$. ¿Cuánto vale la varianza"),
 ("        respuesta: 5.45,", "        respuesta: 5.80,"),
 ("retroAcierto: '$\\\\psi_1 = \\\\theta + \\\\phi = 0.3$, así que $\\\\operatorname{Var}(e_{T+2}) = 5\\\\,(1 + 0.3^2) = 5 \\\\times 1.09 = 5.45$.",
  "retroAcierto: '$\\\\psi_1 = \\\\theta + \\\\phi = 0.4$, así que $\\\\operatorname{Var}(e_{T+2}) = 5\\\\,(1 + 0.4^2) = 5 \\\\times 1.16 = 5.80$."),
 ("retroFallo: 'Es $\\\\sigma^2(\\\\psi_0^2 + \\\\psi_1^2) = 5\\\\,(1 + 0.3^2) = 5.45$, con $\\\\psi_1 = \\\\theta + \\\\phi = 0.3$. Cada tropiezo habitual deja una cifra distinta: $1.09$ es olvidar $\\\\sigma^2$; $0.45$, olvidar $\\\\psi_0 = 1$; $6.80$, tomar $\\\\psi_1 = \\\\phi$ como si fuera un AR(1); $9.05$, perder el signo de $\\\\theta$ y tomar $\\\\psi_1 = 0.9$; $6.50$, sumar los $\\\\psi$ sin elevarlos al cuadrado; y $5.61$,",
  "retroFallo: 'Es $\\\\sigma^2(\\\\psi_0^2 + \\\\psi_1^2) = 5\\\\,(1 + 0.4^2) = 5.80$, con $\\\\psi_1 = \\\\theta + \\\\phi = 0.4$. Cada tropiezo habitual deja una cifra distinta: $1.16$ es olvidar $\\\\sigma^2$; $0.80$, olvidar $\\\\psi_0 = 1$; $6.80$, tomar $\\\\psi_1 = \\\\phi$ como si fuera un AR(1); $8.20$, perder el signo de $\\\\theta$ y tomar $\\\\psi_1 = 0.8$; $7.00$, sumar los $\\\\psi$ sin elevarlos al cuadrado; y $6.09$,"),
 # 4 · P7: la pista pide la precision y la retro explica el redondeo intermedio
 ("después el arcocoseno— y comprueba que la calculadora trabaja en <strong>radianes</strong>.'",
  "después el arcocoseno—, conserva cuatro decimales en cada paso y comprueba que la calculadora trabaja en <strong>radianes</strong>.'"),
 ("(sale $7.57$). Y hace falta la precisión pedida: $7.1$ no basta.'",
  "(sale $7.57$). Si sale $7.06$, $7.10$ o $7.17$, se redondeó un paso intermedio a dos decimales. Y hace falta la precisión pedida: $7.1$ no basta.'"),
],
B / "m7.R": [("round(c(YW = yw$var.pred, CSS = css$sigma2, ML = ml$sigma2), 4)   # las tres sigma^2\n", "")],
B / "m9.R": [("compara <- function(x) do.call(rbind, lapply(rejilla, function(pq) {\n  aj <- suppressWarnings(",
              "# en log(lynx), el ARMA(2,1) avisa de un posible problema de convergencia (optim code = 1);\n# no lo elige ningun criterio, y suppressWarnings() solo calla ese aviso\ncompara <- function(x) do.call(rbind, lapply(rejilla, function(pq) {\n  aj <- suppressWarnings(")],
C: [("phi <- 0.6; theta <- -0.3; s2 <- 5", "phi <- 0.6; theta <- -0.2; s2 <- 5"),
    ("\"ARMA(1,1) phi = 0.6, theta = -0.3, sigma2 = 5: psi =\"", "\"ARMA(1,1) phi = 0.6, theta = -0.2, sigma2 = 5: psi =\"")],
}

fallos = []
for ruta, subs in EDICIONES.items():
    t = ruta.read_text("utf-8")
    for a, b in subs:
        n = t.count(a)
        if n != 1:
            fallos.append(f"{ruta.name}: {n} apariciones de {a[:70]!r}")
            continue
        t = t.replace(a, b)
    if not fallos:
        ruta.write_text(t, "utf-8")
if fallos:
    print("\n".join(fallos)); sys.exit(1)
print("OK: todas las sustituciones aplicadas")
