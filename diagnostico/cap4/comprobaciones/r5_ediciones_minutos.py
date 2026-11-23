#!/usr/bin/env python3
"""R5 del capítulo 4 · minutos declarados (D7) y el recuento de ejercicios de `ensambla_cap4.py`.

No se ejecuta solo: lo importa `r5_edita.py`. Toca dos sitios de `ensamblado/ensambla_cap4.py`:
  · `courseData.modules`: la duración de M1 a M10 y el comentario que dice cómo se midió;
  · la comprobación final, que exigía exactamente 3 `.ejercicio-guiado` y ahora exige 12 (los 3
    del Módulo 10 y los 9 «Para practicar»), con sus paneles `c4mN-pista` y `c4mN-sol`. Sin este
    cambio el ensamblado aborta. Es lo único que se toca fuera de `courseData`.
Medida: `r3_minutos.py`, columna «abierto» (pista y solución leídas); salidas `r5_minutos_antes.out`
y `r5_minutos_despues.out`.
"""
import re

MINUTOS = {1: 16, 2: 12, 3: 19, 4: 14, 5: 10, 6: 14, 7: 14, 8: 18, 9: 20, 10: 49}

COMENTARIO_VIEJO = """        // Medida: diagnostico/cap4/comprobaciones/r3_minutos.py (2026-11-22; de nuevo
        // el 2026-11-23, tras la R4: el texto de las citas suma minutos a M1, M2, M8–M10).
"""
COMENTARIO_NUEVO = """        // Medida: diagnostico/cap4/comprobaciones/r3_minutos.py (2026-11-22; de nuevo
        // el 2026-11-23, tras la R4: el texto de las citas suma minutos a M1, M2, M8–M10;
        // y otra vez el 2026-11-23, tras la R5: cada módulo del 1 al 9 gana un ejercicio
        // «Para practicar», que se cuenta con su pista y su solución leídas).
"""
AUTO_VIEJO = "módulos), la autoevaluación del Módulo 10 (unos 18 min de lectura) ni,"

CHEQUEO_VIEJO = """n_ej = html.count('<div class="ejercicio-guiado">')
if n_ej != 3:
    fallos.append(f"hay {n_ej} ejercicios guiados, se esperaban 3")
for k in (1, 2, 3):
    for suf in ("pista", "sol"):
        if html.count(f'id="c4e{k}-{suf}"') != 1:
            fallos.append(f"falta el panel c4e{k}-{suf}")
"""
CHEQUEO_NUEVO = """# (3 en el Módulo 10 y, desde la ronda R5, un «Para practicar» en cada módulo del 1 al 9)
n_ej = html.count('<div class="ejercicio-guiado">')
if n_ej != 12:
    fallos.append(f"hay {n_ej} ejercicios guiados, se esperaban 12")
for ident in [f"c4e{k}" for k in (1, 2, 3)] + [f"c4m{k}" for k in range(1, 10)]:
    for suf in ("pista", "sol"):
        if html.count(f'id="{ident}-{suf}"') != 1:
            fallos.append(f"falta el panel {ident}-{suf}")
"""


def aplica(fuente, minutos_quiz):
    for k, m in MINUTOS.items():
        fuente, n = re.subn(rf'(\{{ id: {k}, title: "[^"]+", shortTitle: "[^"]+", duration: ")\d+ min(" \}})',
                            rf"\g<1>{m} min\g<2>", fuente)
        assert n == 1, k
    for viejo, nuevo in ((COMENTARIO_VIEJO, COMENTARIO_NUEVO), (CHEQUEO_VIEJO, CHEQUEO_NUEVO),
                         (AUTO_VIEJO, AUTO_VIEJO.replace("unos 18 min", f"unos {minutos_quiz} min")),
                         ('f"3 ejercicios · 8 preguntas de autoevaluación', 'f"12 ejercicios · 8 preguntas de autoevaluación')):
        assert fuente.count(viejo) == 1, viejo
        fuente = fuente.replace(viejo, nuevo)
    return fuente
