"""R3 · minutos medidos (D7) en `courseData` de `ensambla_cap4.py`.

Los minutos son la columna «abierto» de `r3_minutos.py` (pista y solución de los ejercicios a la vista;
sin plegados ni quizzes), redondeada, como en los capítulos 2 y 3. El Módulo 11 conserva sus 40 (el reloj
del ensayo). La medida está en `r3_minutos_despues.out`."""


def registra(c, mover, entre, esc, ENS, **_):
    c("minutos · courseData del capítulo 4: lo medido, con su convenio", ENS,
      '''      modules: [
        { id: 1, title: "De ARMA a ARIMA", shortTitle: "ARIMA", duration: "12 min" },
        { id: 2, title: "La metodología Box–Jenkins", shortTitle: "Box–Jenkins", duration: "10 min" },
        { id: 3, title: "Elegir el orden d", shortTitle: "Elegir d", duration: "16 min" },
        { id: 4, title: "Identificar p y q", shortTitle: "Identificar p,q", duration: "14 min" },
        { id: 5, title: "La constante: media y deriva", shortTitle: "Media y deriva", duration: "12 min" },
        { id: 6, title: "Estimar y comparar modelos", shortTitle: "Explorador", duration: "16 min" },
        { id: 7, title: "Dentro de auto.arima", shortTitle: "auto.arima", duration: "14 min" },
        { id: 8, title: "Diagnóstico y errores comunes", shortTitle: "Diagnóstico", duration: "16 min" },
        { id: 9, title: "Pronóstico: forma e intervalos", shortTitle: "Pronóstico", duration: "16 min" },
        { id: 10, title: "Caso TRM, puente y cierre", shortTitle: "Cierre", duration: "24 min" },
        { id: 11, title: "Simulacro del quiz", shortTitle: "Simulacro", duration: "40 min" },
        { id: 12, title: "Preparcial del Corte II", shortTitle: "Preparcial", duration: "5 min" }
''',
      '''      modules: [
        // `duration` son minutos de LECTURA, medidos con la fórmula de los capítulos
        // 1 a 3 (palabras / 180 + 3 por simulador + 2 por bloque de código),
        // leyendo también la pista y la solución de cada ejercicio. No incluyen el
        // tiempo de resolverlos, los desarrollos plegados (unos 4 min entre tres
        // módulos), la autoevaluación del Módulo 10 (unos 18 min de lectura) ni,
        // en el Módulo 11, nada de lo escrito: sus 40 min son el reloj del ensayo.
        // Medida: diagnostico/cap4/comprobaciones/r3_minutos.py (2026-11-22).
        { id: 1, title: "De ARMA a ARIMA", shortTitle: "ARIMA", duration: "11 min" },
        { id: 2, title: "La metodología Box–Jenkins", shortTitle: "Box–Jenkins", duration: "7 min" },
        { id: 3, title: "Elegir el orden d", shortTitle: "Elegir d", duration: "14 min" },
        { id: 4, title: "Identificar p y q", shortTitle: "Identificar p,q", duration: "9 min" },
        { id: 5, title: "La constante: media y deriva", shortTitle: "Media y deriva", duration: "6 min" },
        { id: 6, title: "Estimar y comparar modelos", shortTitle: "Explorador", duration: "10 min" },
        { id: 7, title: "Dentro de auto.arima", shortTitle: "auto.arima", duration: "10 min" },
        { id: 8, title: "Diagnóstico y errores comunes", shortTitle: "Diagnóstico", duration: "11 min" },
        { id: 9, title: "Pronóstico: forma e intervalos", shortTitle: "Pronóstico", duration: "14 min" },
        { id: 10, title: "Caso TRM, puente y cierre", shortTitle: "Cierre", duration: "43 min" },
        { id: 11, title: "Simulacro del quiz", shortTitle: "Simulacro", duration: "40 min" },
        { id: 12, title: "Preparcial del Corte II", shortTitle: "Preparcial", duration: "3 min" }
''')
