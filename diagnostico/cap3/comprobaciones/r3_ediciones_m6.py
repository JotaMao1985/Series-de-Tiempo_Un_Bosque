"""R3 · Módulo 6 · las promesas del objetivo y del párrafo del simulador dicen lo que el módulo da:
ver cuánto se separa la muestra de la teoría (no medirlo ni cuantificarlo)."""


def registra(c, mover, MOD, **_):
    c("M6 · el objetivo promete ver, no medir", MOD,
      r'''              y medir cuánto se separa una ACF muestral de la teórica que la generó.</p>''',
      r'''              y ver cuánto se separa una ACF muestral de la teórica que la generó.</p>''')

    c("M6 · el simulador muestra tres realizaciones; no las cuantifica", MOD,
      r'''      <p>El laboratorio del módulo anterior lo insinuaba; aquí lo cuantificamos con tres realizaciones concretas de
        longitud 200 generadas con <code>set.seed(3)</code>.''',
      r'''      <p>El laboratorio del módulo anterior lo insinuaba; aquí se ve con tres realizaciones concretas de
        longitud 200 generadas con <code>set.seed(3)</code>.''')
