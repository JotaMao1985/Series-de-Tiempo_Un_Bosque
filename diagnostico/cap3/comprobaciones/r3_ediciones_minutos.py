"""R3 · minutos medidos y el título del Módulo 10 en `courseData`, y su copia en el preparcial.

Los minutos son la columna «abierto» de `r3_minutos.py` (pista y solución de los ejercicios a la
vista; sin plegados ni quizzes), redondeada, como en el capítulo 2. El Módulo 11 conserva sus 30
(el reloj del ensayo). La medida está en `r3_minutos_despues.out`."""


def registra(c, mover, ENS, PRE, **_):
    c("minutos · courseData del capítulo 3: lo medido, con su convenio y el nuevo título del Módulo 10", ENS,
      r'''        { id: 1, title: "Operador de rezago", shortTitle: "Operador B", duration: "12 min" },
        { id: 2, title: "Procesos AR(p)", shortTitle: "AR(p)", duration: "14 min" },
        { id: 3, title: "Procesos MA(q)", shortTitle: "MA(q)", duration: "12 min" },
        { id: 4, title: "Dualidad AR ↔ MA", shortTitle: "Dualidad", duration: "12 min" },
        { id: 5, title: "ARMA e identificación", shortTitle: "ARMA", duration: "14 min" },
        { id: 6, title: "Simular y reconocer procesos", shortTitle: "Simulación", duration: "10 min" },
        { id: 7, title: "Estimación de parámetros", shortTitle: "Estimación", duration: "14 min" },
        { id: 8, title: "Criterios de información y diagnóstico", shortTitle: "Diagnóstico", duration: "14 min" },
        { id: 9, title: "Dos casos reales", shortTitle: "Casos reales", duration: "19 min" },
        { id: 10, title: "Cierre, resumen y autoevaluación", shortTitle: "Cierre", duration: "14 min" },
        { id: 11, title: "Simulacro del quiz", shortTitle: "Simulacro", duration: "30 min" }
''',
      r'''        // `duration` son minutos de LECTURA, medidos con la fórmula del
        // capítulo 1 (palabras / 180 + 3 por simulador + 2 por bloque de
        // código), leyendo también la pista y la solución de cada ejercicio.
        // No incluyen el tiempo de resolverlos, los desarrollos plegados
        // (unos 9 min entre siete módulos), la autoevaluación y la práctica de
        // repaso del Módulo 10 (unos 17 y 29 min de lectura) ni, en el
        // Módulo 11, nada de lo escrito: sus 30 min son el reloj del ensayo.
        // Medida: diagnostico/cap3/comprobaciones/r3_minutos.py (2026-11-21).
        { id: 1, title: "Operador de rezago", shortTitle: "Operador B", duration: "10 min" },
        { id: 2, title: "Procesos AR(p)", shortTitle: "AR(p)", duration: "14 min" },
        { id: 3, title: "Procesos MA(q)", shortTitle: "MA(q)", duration: "15 min" },
        { id: 4, title: "Dualidad AR ↔ MA", shortTitle: "Dualidad", duration: "13 min" },
        { id: 5, title: "ARMA e identificación", shortTitle: "ARMA", duration: "18 min" },
        { id: 6, title: "Simular y reconocer procesos", shortTitle: "Simulación", duration: "7 min" },
        { id: 7, title: "Estimación de parámetros", shortTitle: "Estimación", duration: "9 min" },
        { id: 8, title: "Criterios de información y diagnóstico", shortTitle: "Diagnóstico", duration: "11 min" },
        { id: 9, title: "Dos casos reales", shortTitle: "Casos reales", duration: "31 min" },
        { id: 10, title: "Cierre: redes, resumen y evaluación", shortTitle: "Cierre", duration: "22 min" },
        { id: 11, title: "Simulacro del quiz", shortTitle: "Simulacro", duration: "30 min" }
''')

    c("preparcial del Corte II · el título del módulo 3.10 es el de la barra lateral del capítulo", PRE,
      r'''archivo: CAP3, titulo: 'Cierre, resumen y autoevaluación', objetivo: 'O3' },''',
      r'''archivo: CAP3, titulo: 'Cierre: redes, resumen y evaluación', objetivo: 'O3' },''')
