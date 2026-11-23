"""R3 · Módulo 7 (4.7 Dentro de auto.arima).

Notación: los «siete» modelos a menos de 2 puntos (con las variantes con deriva) frente a los «cuatro»
del explorador del Módulo 6 (sin constante): se dice de dónde sale la diferencia."""


def registra(c, mover, entre, esc, T79, **_):
    c("M7 · los siete modelos: el ganador, cuatro sin constante y dos con deriva", T79,
      r'''<strong>Siete modelos a menos de $2$ puntos de AICc.</strong> La regla de referencia habitual es que''',
      r'''<strong>Siete modelos a menos de $2$ puntos de AICc.</strong> Son el ganador, otros cuatro sin
          constante —los del explorador del Módulo 6— y dos variantes con deriva. La regla de referencia habitual es
          que''')
