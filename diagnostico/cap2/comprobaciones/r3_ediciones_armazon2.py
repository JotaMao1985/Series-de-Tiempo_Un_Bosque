# R3 · armazon, correccion: solo avisa la tabla que de verdad se desplaza (display: block).
# Una tabla con display: table y bordes colapsados puede dar scrollWidth > clientWidth sin desplazarse.
EDICIONES = [
(
r"""    function avisarContinuacion(tabla) {
      const resto = tabla.scrollWidth - tabla.clientWidth - tabla.scrollLeft;
      tabla.classList.toggle('tabla-sigue-der', resto > 1);
      tabla.classList.toggle('tabla-sigue-izq', tabla.scrollLeft > 1);
    }""",
r"""    function avisarContinuacion(tabla) {
      // Solo se desplaza la tabla convertida en bloque; una tabla corriente
      // puede dar scrollWidth > clientWidth por sus bordes sin desplazarse.
      const desplazable = getComputedStyle(tabla).display === 'block';
      const resto = desplazable ? tabla.scrollWidth - tabla.clientWidth - tabla.scrollLeft : 0;
      tabla.classList.toggle('tabla-sigue-der', resto > 1);
      tabla.classList.toggle('tabla-sigue-izq', desplazable && tabla.scrollLeft > 1);
    }"""),
]
