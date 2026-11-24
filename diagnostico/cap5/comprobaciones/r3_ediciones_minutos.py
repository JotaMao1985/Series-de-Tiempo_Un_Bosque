"""R3 · D8: los minutos de `courseData` pasan a ser los medidos, con el convenio de los caps. 2 a 4.

Medida: `r3_minutos.py` sobre el capítulo ya editado (`r3_minutos_despues.out`), columna «abierto»
(pista y solución de los ejercicios leídas), redondeada al minuto (las medias, hacia arriba). El
Módulo 12 conserva sus 50 minutos: son el reloj del ensayo, no lectura."""


def registra(c, mover, entre, despues, esc, ENS, **_):
    c("courseData · minutos medidos y su convenio", ENS,
      '''      modules: [
        { id: 1, title: "La firma de la estacionalidad", shortTitle: "Firma estacional", duration: "14 min" },
        { id: 2, title: "Notación SARIMA y polinomio multiplicativo", shortTitle: "Notación", duration: "12 min" },
        { id: 3, title: "Diferenciación estacional", shortTitle: "Diferenciar", duration: "16 min" },
        { id: 4, title: "Identificar los órdenes estacionales", shortTitle: "Identificar P,Q", duration: "16 min" },
        { id: 5, title: "El modelo airline", shortTitle: "Airline", duration: "14 min" },
        { id: 6, title: "Estimar, comparar y diagnosticar", shortTitle: "Explorador", duration: "16 min" },
        { id: 7, title: "Caso completo: AirPassengers", shortTitle: "Caso completo", duration: "21 min" },
        { id: 8, title: "Segundo caso y contraejemplo", shortTitle: "Contraejemplo", duration: "16 min" },
        { id: 9, title: "Regresores de calendario y SARIMAX", shortTitle: "Calendario", duration: "14 min" },
        { id: 10, title: "Cuando m es grande: Fourier y STL", shortTitle: "Fourier y STL", duration: "16 min" },
        { id: 11, title: "Panorama comparativo y cierre", shortTitle: "Cierre", duration: "20 min" },''',
      '''      modules: [
        // `duration` son minutos de LECTURA, medidos con la fórmula de los capítulos
        // 1 a 4 (palabras / 180 + 3 por simulador + 2 por bloque de código),
        // leyendo también la pista y la solución de cada ejercicio. No incluyen el
        // tiempo de resolverlos ni de ejecutar el código, los desarrollos plegados
        // (unos 4 min entre M2, M3 y M5), la autoevaluación del Módulo 11 (unos 17 min
        // de lectura) ni, en el Módulo 12, nada de lo escrito: sus 50 min son el reloj
        // del ensayo. Medida: diagnostico/cap5/comprobaciones/r3_minutos.py (2026-11-24, de nuevo tras las correcciones del verificador).
        { id: 1, title: "La firma de la estacionalidad", shortTitle: "Firma estacional", duration: "9 min" },
        { id: 2, title: "Notación SARIMA y polinomio multiplicativo", shortTitle: "Notación", duration: "21 min" },
        { id: 3, title: "Diferenciación estacional", shortTitle: "Diferenciar", duration: "21 min" },
        { id: 4, title: "Identificar los órdenes estacionales", shortTitle: "Identificar P,Q", duration: "12 min" },
        { id: 5, title: "El modelo airline", shortTitle: "Airline", duration: "8 min" },
        { id: 6, title: "Estimar, comparar y diagnosticar", shortTitle: "Explorador", duration: "9 min" },
        { id: 7, title: "Caso completo: AirPassengers", shortTitle: "Caso completo", duration: "12 min" },
        { id: 8, title: "Segundo caso y contraejemplo", shortTitle: "Contraejemplo", duration: "9 min" },
        { id: 9, title: "Regresores de calendario y SARIMAX", shortTitle: "Calendario", duration: "10 min" },
        { id: 10, title: "Cuando m es grande: Fourier y STL", shortTitle: "Fourier y STL", duration: "10 min" },
        { id: 11, title: "Panorama comparativo y cierre", shortTitle: "Cierre", duration: "28 min" },''')
