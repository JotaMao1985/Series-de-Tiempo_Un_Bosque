# R3b · el desvanecido tampoco mide mas que lo que falta por ensenar: si a la tabla le faltan 13 px,
# se apagan 13 px (cap. 5 M12 a 800 px: las cifras de la ultima columna, cortadas por unos pixeles,
# seguian apagandose enteras con la primera version de r3b_ediciones_armazon.py).
EDICIONES = [
(
r"""    // El desvanecido no tiene un ancho fijo: llega desde el borde hasta el
    // texto más cercano que está entero a la vista, con un tope de 3.5rem.
    // Así se apagan el texto ya cortado y el hueco que lo separa del
    // anterior, y nunca una cifra que cabe: si a la tabla le faltan unos
    // píxeles de relleno por enseñar, no se apaga nada.""",
r"""    // El desvanecido no tiene un ancho fijo. Es el menor de tres: 3.5rem, lo
    // que falta por enseñar hacia ese lado y la distancia del borde al texto
    // más cercano que está entero a la vista. Así nunca apaga una cifra que
    // cabe, y si a la tabla le faltan unos píxeles solo se apagan esos."""),
(
r"""      let anchoDer = tope;
      let anchoIzq = tope;""",
r"""      let anchoDer = Math.min(tope, resto);
      let anchoIzq = Math.min(tope, tabla.scrollLeft);"""),
]
