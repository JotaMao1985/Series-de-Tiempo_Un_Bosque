#!/bin/sh
# Verificador independiente · R1 cap. 2 · el bloque del M6 leyendo la TRM por HTTP
# (rama «el archivo no esta en la carpeta de trabajo»). Sirve Htmls_Series/ en
# 127.0.0.1:8799 como lo serviria GitHub Pages (datos/ en la raiz) y ejecuta los
# bloques R y Python del M6 en una carpeta vacia, con la URL del sitio cambiada
# por la local. Uso: sh v1_trm_por_url.sh RAIZ_REPO CARPETA_VACIA
RAIZ="$1"; VACIO="$2"
cd "$RAIZ/Htmls_Series" && python3 -m http.server 8799 --bind 127.0.0.1 >/dev/null 2>&1 &
PID=$!; sleep 1
python3 - "$RAIZ/Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html" "$VACIO" <<'PY'
import re, html, sys
t = open(sys.argv[1], encoding="utf-8").read()
bl = re.findall(r'<pre><code class="language-(r|python)">(.*?)</code></pre>', t, re.S)
for lang, c in bl:
    c = html.unescape(c)
    if "trm_mensual_2015-01_2026-06.csv" in c and "descarga_trm" not in c and "pd.read_json" not in c:
        c = c.replace("https://jotamao1985.github.io/Series-de-Tiempo_Un_Bosque/datos/", "http://127.0.0.1:8799/datos/")
        open(f"{sys.argv[2]}/m6.{'R' if lang=='r' else 'py'}", "w").write(c)
PY
cd "$VACIO"; ls
echo "--- R ---";  Rscript --vanilla m6.R 2>&1 | grep -E "^\[1\]|Dickey|KPSS"
echo "--- Python ---"; MPLBACKEND=Agg python3 m6.py 2>&1 | grep -v Warning | grep -E "^\(|^[0-9]"
kill $PID
