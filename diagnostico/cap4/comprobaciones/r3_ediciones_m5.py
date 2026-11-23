"""R3 · Módulo 5 (4.5 La constante).

D5: la nota de la TRM, que usaba la serie y un resultado («la caminata que elige auto.arima») antes
de que el capítulo los presente, se va al Módulo 10 (a la nota «El resultado, aceptado tal cual»,
donde el bloque de código de la TRM la respalda). Notación: T es el origen del pronóstico, el último
dato; el $\\hat y_{n+h}$ de la regla mnemotécnica pasa a $\\hat y_{T+h}$."""


def registra(c, mover, entre, esc, T46, **_):
    c("M5 · T es el origen del pronóstico (antes ŷ_{n+h})", T46,
      r'''a largo plazo, $\hat y_{n+h}$ crece como''',
      r'''a largo plazo, $\hat y_{T+h}$ (con $T$ el último dato) crece como''')
    entre("M5 · la nota de la TRM sale (pasa al Módulo 10)", T46,
          '''      <div class="note">
        <p><strong>El mismo cálculo en la TRM.</strong>''',
          '''      <div class="code-tabs">
        <div class="code-tabs-nav" role="tablist" aria-label="Media y deriva">''',
          '''''')
        # (el bloque que sale queda en el commit base y su contenido, reescrito, en templates_10.html)
