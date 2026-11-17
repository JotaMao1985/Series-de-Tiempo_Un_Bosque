# R3 · tras la verificacion, punto 3: el desvanecido de la tabla que sigue ya no mide 3.5rem fijos.
# Llega, como mucho, hasta el texto mas cercano al borde que esta a la vista entero: nunca apaga
# un texto que cabe. Armazon: baja por la cadena 3 -> 6.
EDICIONES = [
(
r"""       ajustarTablas() pone y quita las dos clases al medir y cada vez que la
       tabla se desplaza: al llegar al final, el desvanecido desaparece. */
    table.tabla-sigue-der {
      -webkit-mask-image: linear-gradient(to right, #000 calc(100% - 3.5rem), rgba(0, 0, 0, 0.08));
      mask-image: linear-gradient(to right, #000 calc(100% - 3.5rem), rgba(0, 0, 0, 0.08));
    }

    table.tabla-sigue-izq {
      -webkit-mask-image: linear-gradient(to left, #000 calc(100% - 3.5rem), rgba(0, 0, 0, 0.08));
      mask-image: linear-gradient(to left, #000 calc(100% - 3.5rem), rgba(0, 0, 0, 0.08));
    }

    table.tabla-sigue-izq.tabla-sigue-der {
      -webkit-mask-image: linear-gradient(to right, rgba(0, 0, 0, 0.08), #000 3.5rem, #000 calc(100% - 3.5rem), rgba(0, 0, 0, 0.08));
      mask-image: linear-gradient(to right, rgba(0, 0, 0, 0.08), #000 3.5rem, #000 calc(100% - 3.5rem), rgba(0, 0, 0, 0.08));
    }
""",
r"""       ajustarTablas() pone y quita las dos clases al medir y cada vez que la
       tabla se desplaza: al llegar al final, el desvanecido desaparece.
       El ancho de cada desvanecido lo fija avisarContinuacion() en
       --sigue-der y --sigue-izq: llega, como mucho, hasta el texto más cercano
       al borde que está entero a la vista, de modo que solo se apaga lo que
       ya está cortado y el hueco que lo separa de lo que se lee. */
    table.tabla-sigue-der {
      -webkit-mask-image: linear-gradient(to right, #000 calc(100% - var(--sigue-der, 3.5rem)), rgba(0, 0, 0, 0.08));
      mask-image: linear-gradient(to right, #000 calc(100% - var(--sigue-der, 3.5rem)), rgba(0, 0, 0, 0.08));
    }

    table.tabla-sigue-izq {
      -webkit-mask-image: linear-gradient(to left, #000 calc(100% - var(--sigue-izq, 3.5rem)), rgba(0, 0, 0, 0.08));
      mask-image: linear-gradient(to left, #000 calc(100% - var(--sigue-izq, 3.5rem)), rgba(0, 0, 0, 0.08));
    }

    table.tabla-sigue-izq.tabla-sigue-der {
      -webkit-mask-image: linear-gradient(to right, rgba(0, 0, 0, 0.08), #000 var(--sigue-izq, 3.5rem), #000 calc(100% - var(--sigue-der, 3.5rem)), rgba(0, 0, 0, 0.08));
      mask-image: linear-gradient(to right, rgba(0, 0, 0, 0.08), #000 var(--sigue-izq, 3.5rem), #000 calc(100% - var(--sigue-der, 3.5rem)), rgba(0, 0, 0, 0.08));
    }
"""),
(
r"""    // izquierda (el CSS las desvanece hacia ese lado).
    // ================================================================
    function avisarContinuacion(tabla) {
      // Solo se desplaza la tabla convertida en bloque; una tabla corriente
      // puede dar scrollWidth > clientWidth por sus bordes sin desplazarse.
      const desplazable = getComputedStyle(tabla).display === 'block';
      const resto = desplazable ? tabla.scrollWidth - tabla.clientWidth - tabla.scrollLeft : 0;
      tabla.classList.toggle('tabla-sigue-der', resto > 1);
      tabla.classList.toggle('tabla-sigue-izq', desplazable && tabla.scrollLeft > 1);
    }""",
r"""    // izquierda (el CSS las desvanece hacia ese lado).
    //
    // El desvanecido no tiene un ancho fijo: llega desde el borde hasta el
    // texto más cercano que está entero a la vista, con un tope de 3.5rem.
    // Así se apagan el texto ya cortado y el hueco que lo separa del
    // anterior, y nunca una cifra que cabe: si a la tabla le faltan unos
    // píxeles de relleno por enseñar, no se apaga nada.
    // ================================================================
    function avisarContinuacion(tabla) {
      // Solo se desplaza la tabla convertida en bloque; una tabla corriente
      // puede dar scrollWidth > clientWidth por sus bordes sin desplazarse.
      const desplazable = getComputedStyle(tabla).display === 'block';
      const resto = desplazable ? tabla.scrollWidth - tabla.clientWidth - tabla.scrollLeft : 0;
      const sigueDer = resto > 1;
      const sigueIzq = desplazable && tabla.scrollLeft > 1;
      tabla.classList.toggle('tabla-sigue-der', sigueDer);
      tabla.classList.toggle('tabla-sigue-izq', sigueIzq);
      if (!sigueDer && !sigueIzq) {
        tabla.style.removeProperty('--sigue-der');
        tabla.style.removeProperty('--sigue-izq');
        return;
      }
      const caja = tabla.getBoundingClientRect();
      const izquierda = caja.left + tabla.clientLeft;
      const derecha = izquierda + tabla.clientWidth;
      const tope = 3.5 * parseFloat(getComputedStyle(document.documentElement).fontSize);
      let anchoDer = tope;
      let anchoIzq = tope;
      const rango = document.createRange();
      tabla.querySelectorAll('th, td').forEach(celda => {
        rango.selectNodeContents(celda);
        const texto = rango.getBoundingClientRect();
        // Solo cuentan los textos que se ven enteros; los cortados son
        // justamente los que el desvanecido puede cubrir.
        if (!texto.width || texto.left < izquierda - 0.5 || texto.right > derecha + 0.5) return;
        anchoDer = Math.min(anchoDer, derecha - texto.right);
        anchoIzq = Math.min(anchoIzq, texto.left - izquierda);
      });
      tabla.style.setProperty('--sigue-der', Math.max(0, Math.floor(anchoDer)) + 'px');
      tabla.style.setProperty('--sigue-izq', Math.max(0, Math.floor(anchoIzq)) + 'px');
    }"""),
]
