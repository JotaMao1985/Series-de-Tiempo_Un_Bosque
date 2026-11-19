"""R5 del cap. 2 · correcciones de la sesión maestra tras la verificación independiente.
Cada sustitución debe aparecer exactamente una vez."""
from pathlib import Path
F = Path("Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html")
h = F.read_text(encoding="utf-8")
S = [
 # 1-2 · M8 (c): diferencias sin redondear antes de restar; centavos respecto de la mediana
 ("5.15 por debajo y 7.70 por encima", "5.16 por debajo y 7.69 por encima"),
 ("y su media, 15.97, unos 33 centavos más.", "y su media, 15.97, unos 31 centavos por encima de ella."),
 # 3 · E2: 3.0 queda fuera del intervalo [3.1, 6.9]
 ("El 3.0&nbsp;% de aquí y el 3.2&nbsp;% del Módulo 6 —que es este mismo\n              experimento con otra semilla— caen en el borde de abajo.",
  "El 3.0&nbsp;% de aquí queda justo por debajo, y el 3.2&nbsp;% del Módulo 6 —que es este mismo\n              experimento con otra semilla—, justo dentro, en el borde de abajo."),
 # 4 · P5: la retro del segundo distractor explica el error real
 ("retro: 'Eso es lo que dice el ADF al rechazar la raíz unitaria, pero el KPSS de nivel rechaza la estacionariedad. No coinciden.'",
  "retro: 'Eso diría el ADF si su rechazo fuera fiable, y aquí no lo es: con 120 datos usa $k = 4$ términos, menos que el periodo, 12, y la estacionalidad que queda en el residuo puede fabricar el rechazo, como en el caso tramposo. Que el KPSS de nivel rechace no prueba nada en ningún sentido, porque no admite tendencia. Antes de leer una tendencia lineal hay que corregir las dos especificaciones.'"),
 # 5 · P6: la pista ya no remite a la fila con los números del gráfico
 ("pista: 'Compara la altura de la primera barra con la del rezago 12 y describe con tus palabras cómo se pasa de una a otra. Después busca esa descripción en la tabla del Módulo 3.'",
  "pista: 'Mira cómo baja la ACF de un rezago al siguiente, no solo lo alta que empieza, y pregúntate qué clase de serie conserva tanta memoria a doce rezagos de distancia.'"),
 # 6 · P2: quien no redondea no acierta
 ("respuesta: 171,\n        tolerancia: 0.5,", "respuesta: 171,\n        tolerancia: 0.2,"),
 ("Si respondiste 170, redondeaste hacia abajo:", "Si respondiste 170.7, el despeje está bien, pero $T$ cuenta observaciones y hay que redondear hacia arriba. Si respondiste 170, redondeaste hacia abajo:"),
 # 7 · M3 (d)
 ("con diez datos el azar solo puede fabricar una autocorrelación de ese tamaño,", "con diez datos el azar, por sí solo, puede fabricar una autocorrelación de ese tamaño,"),
 # 8 · M6 (a): cita literal de la fila
 ("Es la segunda fila de la tabla, «no estacionaria: hay que diferenciar».", "Es la segunda fila de la tabla: «No estacionaria. Las dos coinciden: hay que diferenciar»."),
 # 9 · comentario
 ("Desde la R5 cada módulo salvo el 7 trae", "Desde la R5 cada módulo salvo el 7 y el 9 trae"),
 # 10 · E4: nsdiffs con su salida
 ("trm &lt;- ts(read.csv(archivo)$trm, start = c(2015, 1), frequency = 12)\n",
  "trm &lt;- ts(read.csv(archivo)$trm, start = c(2015, 1), frequency = 12)\nforecast::nsdiffs(trm)   # no es estacional: los 5 rezagos por defecto bastan\n#> [1] 0\n"),
 # 11 · LakeHuron: la PACF sugiere, pendiente la estacionariedad
 ("<code>LakeHuron</code>, un AR(2), con una comprobación pendiente.</strong>", "<code>LakeHuron</code>, un AR(2) si resulta estacionaria, cosa que queda por comprobar.</strong>"),
 ("Primera línea otra vez: un AR(2). La barra 10", "Primera línea otra vez: la PACF sugiere un AR(2). La barra 10"),
 # 12 · co2: el logaritmo cambiaría poco, no «nada que estabilizar»
 ("el nivel apenas cambia de escala y no hay nada que\n                  estabilizar. <code>logaritmo = FALSE</code>",
  "el nivel apenas cambia de escala y el logaritmo\n                  cambiaría poco la serie. <code>logaritmo = FALSE</code>"),
 # 13 · nhtemp: ndiffs por defecto pide una diferencia
 ("y dejar dicho con qué especificación se decidió y que el ADF no fue concluyente.</p>",
  "y dejar dicho con qué especificación se decidió y que el ADF no fue concluyente. Ojo al automatizarlo: <code>ndiffs(nhtemp)</code>, con el KPSS de nivel que usa por defecto —como en <code>preparar()</code>, en el Módulo 9—, pide una diferencia; con <code>type = \"trend\"</code>, ninguna. Cuando las pruebas no concluyen, decide el analista, y la decisión se escribe.</p>"),
]
for a, b in S:
    n = h.count(a)
    assert n == 1, (n, a[:70])
    h = h.replace(a, b)
F.write_text(h, encoding="utf-8")
print(len(S), "sustituciones")
