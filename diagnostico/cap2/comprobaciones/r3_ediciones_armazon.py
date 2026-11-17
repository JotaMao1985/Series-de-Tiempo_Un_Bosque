# R3 · armazon (baja por la cadena 3 -> 6): la tabla que se desplaza avisa de que sigue.
EDICIONES = [
(
r"""    table.tabla-ancha {
      display: block;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
    }
""",
r"""    table.tabla-ancha {
      display: block;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
    }

    /* Una tabla que se desplaza y aún tiene columnas por enseñar se desvanece
       hacia ese lado. Es una máscara sobre la caja de la tabla y no una
       sombra, porque las celdas tienen fondo y taparían cualquier sombra
       puesta debajo; así no hace falta envolver la tabla ni tocar su marcado.
       ajustarTablas() pone y quita las dos clases al medir y cada vez que la
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
"""),
(
r"""    // componer las fórmulas de las celdas. Las tablas ordenables
    // (`.tabla-ranking`) tienen su propio marco desplazable y se saltan.
    // ================================================================
    function ajustarTablas() {""",
r"""    // componer las fórmulas de las celdas. Las tablas ordenables
    // (`.tabla-ranking`) tienen su propio marco desplazable y se saltan.
    //
    // Toda tabla que se desplaza —la ancha y, por debajo de 768 px, cualquiera
    // que no quepa— avisa de que sigue: `tabla-sigue-der` mientras queden
    // columnas a la derecha y `tabla-sigue-izq` mientras queden a la
    // izquierda (el CSS las desvanece hacia ese lado).
    // ================================================================
    function avisarContinuacion(tabla) {
      const resto = tabla.scrollWidth - tabla.clientWidth - tabla.scrollLeft;
      tabla.classList.toggle('tabla-sigue-der', resto > 1);
      tabla.classList.toggle('tabla-sigue-izq', tabla.scrollLeft > 1);
    }

    function ajustarTablas() {"""),
(
r"""        if (ancha) tabla.classList.add('tabla-ancha');
      });
    }""",
r"""        if (ancha) tabla.classList.add('tabla-ancha');
        avisarContinuacion(tabla);
        if (!tabla.dataset.avisaContinuacion) {
          tabla.dataset.avisaContinuacion = 'si';
          tabla.addEventListener('scroll', () => avisarContinuacion(tabla), { passive: true });
        }
      });
    }"""),
]
