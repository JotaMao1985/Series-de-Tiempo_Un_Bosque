#!/bin/zsh
# Ejecuta cada bloque extraido tal cual; R con eco (R -f), Python con MPLBACKEND=Agg
cd "${0:A:h}/par_bloques"
for f in b*.R; do R --no-save --quiet -f "$f" > "${f%.R}.out" 2>&1; echo "$f exit $?"; done
for f in b*.py; do MPLBACKEND=Agg /opt/homebrew/Caskroom/mambaforge/base/bin/python3 "$f" > "${f%.py}.out" 2>&1; echo "$f exit $?"; done
