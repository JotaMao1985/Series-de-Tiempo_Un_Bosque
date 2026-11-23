"""R3 · Módulo 2 (4.2 La metodología de Box–Jenkins).

D5: el esqueleto del ciclo imprime el `d` que decide `ndiffs()`, de modo que la etapa 1 muestra una
cifra y el cierre del módulo («despacha la etapa 1 en una línea») habla de algo que se vio."""


def registra(c, mover, entre, esc, T13, **_):
    c("M2 · R: el esqueleto imprime d", T13,
      esc('''d <- ndiffs(Nile)                       # cuantas diferencias
w <- if (d == 0)'''),
      esc('''d <- ndiffs(Nile)                       # cuantas diferencias
d
#> [1] 1
w <- if (d == 0)'''))
