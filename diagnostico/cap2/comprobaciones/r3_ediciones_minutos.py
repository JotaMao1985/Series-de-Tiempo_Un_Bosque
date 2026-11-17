# R3 · minutos declarados = minutos medidos (diagnostico/cap2/diag/cuenta_cap2.py, columna «abierto»).
EDICIONES = [
(
r"""      modules: [
        { id: 1, title: "Estacionariedad", shortTitle: "Estacionariedad", duration: "10 min" },
        { id: 2, title: "Ruido blanco", shortTitle: "Ruido blanco", duration: "8 min" },
        { id: 3, title: "Autocorrelación y correlograma", shortTitle: "ACF", duration: "12 min" },
        { id: 4, title: "Autocorrelación parcial (PACF)", shortTitle: "PACF", duration: "10 min" },
        { id: 5, title: "Caminata aleatoria y raíz unitaria", shortTitle: "Raíz unitaria", duration: "12 min" },
        { id: 6, title: "Pruebas ADF y KPSS", shortTitle: "ADF / KPSS", duration: "14 min" },
        { id: 7, title: "Diferenciación", shortTitle: "Diferenciación", duration: "12 min" },
        { id: 8, title: "Logaritmo y Box–Cox", shortTitle: "Box–Cox", duration: "10 min" },
        { id: 9, title: "Pipeline, resumen y autoevaluación", shortTitle: "Cierre", duration: "10 min" }
      ]""",
r"""      modules: [
        // `duration` son minutos de LECTURA, medidos con la fórmula del
        // capítulo 1 (palabras / 180 + 3 por simulador + 2 por bloque de
        // código), leyendo también la pista y la solución de cada ejercicio.
        // No incluyen el tiempo de resolverlo, el desarrollo plegado del
        // Módulo 4 (2 min) ni la autoevaluación del Módulo 9 (unos 9 min).
        // Medida: diagnostico/cap2/diag/cuenta_cap2.py (2026-11-17).
        { id: 1, title: "Estacionariedad", shortTitle: "Estacionariedad", duration: "6 min" },
        { id: 2, title: "Ruido blanco", shortTitle: "Ruido blanco", duration: "8 min" },
        { id: 3, title: "Autocorrelación y correlograma", shortTitle: "ACF", duration: "9 min" },
        { id: 4, title: "Autocorrelación parcial (PACF)", shortTitle: "PACF", duration: "9 min" },
        { id: 5, title: "Caminata aleatoria y raíz unitaria", shortTitle: "Raíz unitaria", duration: "10 min" },
        { id: 6, title: "Pruebas ADF y KPSS", shortTitle: "ADF / KPSS", duration: "13 min" },
        { id: 7, title: "Diferenciación", shortTitle: "Diferenciación", duration: "16 min" },
        { id: 8, title: "Logaritmo y Box–Cox", shortTitle: "Box–Cox", duration: "8 min" },
        { id: 9, title: "Pipeline, resumen y autoevaluación", shortTitle: "Cierre", duration: "27 min" }
      ]"""),
]
