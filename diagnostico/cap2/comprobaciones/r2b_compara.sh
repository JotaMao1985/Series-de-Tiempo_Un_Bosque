#!/bin/sh
# R2b · las comparaciones del verificador independiente (v2_compara.py y v2_doce_perdido.py),
# con su recorrido de HEAD y el recorrido del árbol ya corregido (v2_recorrido_r2b.json, hecho
# con su mismo v2_recorrido.js). No toca ningún archivo v2_*.
cd "$(dirname "$0")"
sed 's/v2_recorrido_ahora.json/v2_recorrido_r2b.json/g' v2_compara.py > /tmp/r2b_compara_tmp.py
sed "s#open('v2_recorrido_head.json')#open('$PWD/v2_recorrido_head.json')#; s#open('v2_recorrido_ahora.json')#open('$PWD/v2_recorrido_r2b.json')#" v2_doce_perdido.py > /tmp/r2b_doce_tmp.py
cp /tmp/r2b_compara_tmp.py ./_r2b_compara_tmp.py && python3 ./_r2b_compara_tmp.py > r2b_compara.out; rm -f ./_r2b_compara_tmp.py
python3 /tmp/r2b_doce_tmp.py > r2b_doce_perdido.out
grep -c . r2b_doce_perdido.out; grep "^## " r2b_compara.out
