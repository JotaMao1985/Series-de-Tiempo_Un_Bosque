#!/usr/bin/env python3
"""R5 del capítulo 2 · minutos declarados de cada módulo, con los ejercicios dentro.

Lo importa `r5_edita.py`. Convenio de la R3, sin tocarlo: minutos de LECTURA con la pista y
la solución de cada ejercicio leídas (columna «abierto» de `diag/cuenta_cap2.py`), sin el
tiempo de resolverlo, sin el desarrollo plegado del Módulo 4 y sin la autoevaluación.
Medida: `r5_minutos_despues.out`.
"""
import re

MINUTOS = {1: 11, 2: 12, 3: 13, 4: 14, 5: 14, 6: 18, 7: 17, 8: 13, 9: 34}


def aplica(src):
    for k, m in MINUTOS.items():
        patron = re.compile(r'(\{ id: %d, title: "[^"]*", shortTitle: "[^"]*", duration: ")\d+( min" \})' % k)
        src, n = patron.subn(r"\g<1>%d\g<2>" % m, src)
        assert n == 1, k
    viejo = '''        // No incluyen el tiempo de resolverlo, el desarrollo plegado del
        // Módulo 4 (2 min) ni la autoevaluación del Módulo 9 (unos 9 min).
        // Medida: diagnostico/cap2/diag/cuenta_cap2.py (2026-11-17).'''
    nuevo = '''        // No incluyen el tiempo de resolverlo, el desarrollo plegado del
        // Módulo 4 (2 min) ni la autoevaluación del Módulo 9 (unos 11 min).
        // Desde la R5 cada módulo salvo el 7 trae un ejercicio «Para practicar»,
        // que entra en la cuenta con su pista y su solución.
        // Medida: diagnostico/cap2/diag/cuenta_cap2.py (2026-11-18).'''
    assert src.count(viejo) == 1
    return src.replace(viejo, nuevo)
