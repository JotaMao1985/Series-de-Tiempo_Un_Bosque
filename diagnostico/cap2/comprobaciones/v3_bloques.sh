#!/bin/zsh
# Verificador de bloques sobre los cinco capitulos, en serie (comparten /tmp/verifica_cap6)
cd "$(dirname $0)/../../.."
for c in 2-estacionariedad-acf-pacf 3-modelos-ar-ma-arma 4-modelos-arima 5-sarima 6-pronostico-evaluacion; do
  n=${c%%-*}
  MPLBACKEND=Agg python3 precalculo/verifica_bloques_cap6.py --html Htmls_Series/capitulo-$c.html > diagnostico/cap2/comprobaciones/v3_bloques_cap$n.out 2>&1
  echo "cap$n: $(tail -3 diagnostico/cap2/comprobaciones/v3_bloques_cap$n.out | tr '\n' ' ')"
done
git status --short precalculo/serie.csv
