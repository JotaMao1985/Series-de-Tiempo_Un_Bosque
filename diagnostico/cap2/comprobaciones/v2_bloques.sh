#!/bin/zsh
# Verificador independiente R2: verifica_bloques_cap6.py sobre los capítulos 2-6, HEAD frente al árbol de trabajo.
# Uso: v2_bloques.sh <carpeta con Htmls_Series de HEAD>
cd "$(dirname $0)/../../.."
HEADDIR=$1
OUT=diagnostico/cap2/comprobaciones
for f in capitulo-2-estacionariedad-acf-pacf capitulo-3-modelos-ar-ma-arma capitulo-4-modelos-arima capitulo-5-sarima capitulo-6-pronostico-evaluacion; do
  MPLBACKEND=Agg python3 precalculo/verifica_bloques_cap6.py --html Htmls_Series/$f.html > $OUT/v2_bloques_ahora_$f.out 2>&1
  MPLBACKEND=Agg python3 precalculo/verifica_bloques_cap6.py --html $HEADDIR/Htmls_Series/$f.html > $OUT/v2_bloques_head_$f.out 2>&1
  echo "$f  ahora: $(tail -3 $OUT/v2_bloques_ahora_$f.out | tr '\n' ' ')"
  echo "$f  HEAD : $(tail -3 $OUT/v2_bloques_head_$f.out | tr '\n' ' ')"
done
