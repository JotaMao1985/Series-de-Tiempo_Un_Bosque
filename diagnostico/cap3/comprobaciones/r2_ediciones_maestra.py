"""R2 del cap. 3 · corrección de la sesión maestra tras la segunda pasada (se aplica después de r2_edita.py).
La lectura del M6 decía «rezagos con ACF teórica nula: 15», que se lee como el rezago 15; ahora da el tramo y el recuento."""
from pathlib import Path
j = Path("ensamblado/cap3/cap3_js.js"); h = j.read_text(encoding="utf-8")
a = "              : `${ceros}, y ${lista.length} de ellos se salen de la banda en la muestra` +"
b = "              : `del ${corte[tipo] + 1} al ${muestral.length} (${ceros} rezagos), y ${lista.length} de ellos se salen de la banda en la muestra` +"
assert h.count(a) == 1, h.count(a)
j.write_text(h.replace(a, b), encoding="utf-8")
print("1 sustitución")
