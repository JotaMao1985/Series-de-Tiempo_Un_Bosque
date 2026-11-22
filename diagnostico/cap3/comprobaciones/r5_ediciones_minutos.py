#!/usr/bin/env python3
"""R5 del capítulo 3 · minutos declarados en `courseData.modules` (D7), en `ensambla_cap3.py`.

Son la columna «abierto» de `r3_minutos.py` (pista y solución de cada ejercicio leídas; sin
desarrollos plegados ni quizzes), redondeada, como en la R3 y en el capítulo 2. El Módulo 11
conserva sus 30 (el reloj del ensayo). Medidas: `r5_minutos_antes.out` (sobre 5c2fdb3) y
`r5_minutos_despues.out`.

    módulo            1     2     3     4     5     6     7     8     9    10
    medido antes   10.7  15.0  15.7  13.5  18.9   7.1   9.7  11.2  32.5  23.8
    medido ahora   15.2  18.6  20.2  17.5  23.7  11.9  14.4  11.2  37.3  25.9
"""
import re

NUEVOS = {1: 15, 2: 19, 3: 20, 4: 18, 5: 24, 6: 12, 7: 14, 8: 11, 9: 37, 10: 26}

COMENTARIO = [
    ("        // repaso del Módulo 10 (unos 17 y 29 min de lectura) ni, en el\n",
     "        // repaso del Módulo 10 (unos 23 y 29 min de lectura) ni, en el\n"),
    ("        // Medida: diagnostico/cap3/comprobaciones/r3_minutos.py (2026-11-21).\n",
     "        // Medida: diagnostico/cap3/comprobaciones/r3_minutos.py (2026-11-21, tras la\n"
     "        // R5: cada módulo del 1 al 9, salvo el 8, lleva un «Para practicar»).\n"),
]


def aplica(ens):
    for mid, minutos in NUEVOS.items():
        patron = re.compile(r'(\{ id: %d, title: "[^"]+", shortTitle: "[^"]+", duration: ")(\d+)( min" \})' % mid)
        assert len(patron.findall(ens)) == 1, mid
        ens = patron.sub(lambda m: f"{m.group(1)}{minutos}{m.group(3)}", ens)
    for antes, despues in COMENTARIO:
        assert ens.count(antes) == 1, antes
        ens = ens.replace(antes, despues)
    return ens
