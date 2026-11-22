#!/bin/bash
cd "$(dirname "$0")"
carril() {  # $1 = puerto CDP, resto = trabajos "nom:pto:cap:ancho"
  p=$1; shift
  for t in "$@"; do
    IFS=: read nom pto cap ancho <<< "$t"
    BASE="http://127.0.0.1:$pto/capitulo-$cap.html" ETIQ="$nom-cap${cap%%-*}" ANCHO=$ancho PUERTO=$p node v2_regresion.js > "v2_regresion_${nom}-cap${cap%%-*}-$ancho.log" 2>&1
  done
}
carril 9280 nuevo:8766:2-estacionariedad-acf-pacf:1200 viejo:8767:2-estacionariedad-acf-pacf:1200 nuevo:8766:2-estacionariedad-acf-pacf:375 viejo:8767:2-estacionariedad-acf-pacf:375 &
carril 9281 nuevo:8766:3-modelos-ar-ma-arma:1200 viejo:8767:3-modelos-ar-ma-arma:1200 nuevo:8766:3-modelos-ar-ma-arma:375 viejo:8767:3-modelos-ar-ma-arma:375 &
carril 9282 nuevo:8766:5-sarima:1200 viejo:8767:5-sarima:1200 nuevo:8766:5-sarima:375 viejo:8767:5-sarima:375 &
carril 9283 nuevo:8766:6-pronostico-evaluacion:1200 viejo:8767:6-pronostico-evaluacion:1200 nuevo:8766:6-pronostico-evaluacion:375 viejo:8767:6-pronostico-evaluacion:375 &
wait
echo FIN > v2_regresion_FIN.txt
