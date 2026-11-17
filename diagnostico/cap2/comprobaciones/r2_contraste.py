#!/usr/bin/env python3
"""R2 del capítulo 2 · contraste sobre blanco (WCAG 2.x) de los colores de los gráficos."""
def lum(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def contraste(a, b='#ffffff'):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)
for nombre, color in [
        ('naranja de marca (antes: banda, caminata del M1, barras del M6)', '#FF6600'),
        ('gris anterior', '#94a3b8'),
        ('banda de los correlogramas (R2)', '#e05a00'),
        ('secundario (R2, el del capítulo 1)', '#FB6400'),
        ('gris (R2, el del capítulo 1)', '#8795A9'),
        ('primario', '#012820'), ('terciario', '#0e7490'),
        ('línea del 0 de la rejilla (R2)', '#64748b'),
        ('alternativa descartada para la banda', '#c2410c')]:
    print(f'{color}  {contraste(color):5.2f}:1  {nombre}')
