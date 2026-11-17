# Verificador independiente R2: contraste WCAG de los colores de los gráficos sobre el blanco del lienzo
def lum(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def cr(a, b='#ffffff'):
    la, lb = sorted([lum(a), lum(b)], reverse=True); return (la + 0.05) / (lb + 0.05)
for nombre, col in [('naranja de marca anterior', '#FF6600'), ('secundario nuevo', '#FB6400'), ('gris anterior', '#94a3b8'),
                    ('gris nuevo', '#8795A9'), ('banda nueva', '#e05a00'), ('primario', '#012820'), ('terciario', '#0e7490'),
                    ('línea del 0', '#64748b')]:
    print(f'{nombre:28s} {col}  {cr(col):.2f}:1 sobre blanco')
# rejilla normal: rgba(148,163,184,0.2) sobre blanco
r, g, b = [round(255 * 0.8 + x * 0.2) for x in (148, 163, 184)]
print(f'rejilla (compuesta)          #{r:02x}{g:02x}{b:02x}  {cr(f"#{r:02x}{g:02x}{b:02x}"):.2f}:1')
