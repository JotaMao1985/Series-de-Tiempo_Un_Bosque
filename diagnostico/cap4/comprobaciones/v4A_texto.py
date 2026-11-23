"""Texto plano (sin etiquetas) de un tramo de líneas del HTML del cap. 4, con
[[id]] donde empieza cada data-afirma y {cita} en cada cita visible: para leer
cada afirmación en su párrafo."""
import re, sys, html, pathlib
RAIZ = pathlib.Path(__file__).resolve().parents[3]
L = (RAIZ / "Htmls_Series/capitulo-4-modelos-arima.html").read_text("utf-8").splitlines()
a, b = int(sys.argv[1]), int(sys.argv[2])
for i in range(a - 1, b):
    s = L[i]
    s = re.sub(r'<[^>]*data-afirma="([^"]+)"[^>]*>', r"[[\1]]", s)
    s = re.sub(r'<cite class="cita" data-ref="([^"]+)" data-loc="([^"]*)"[^>]*>.*?</cite>', r"{\1 \2}", s)
    s = re.sub(r"<script.*?</script>", "", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s).strip()
    if s:
        print(f"{i+1}: {s}")
