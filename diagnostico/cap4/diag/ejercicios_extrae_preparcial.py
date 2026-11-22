"""Diagnóstico cap. 4 · copia PREPARCIAL_DATOS (series e ítems) del preparcial a JSON
para que ejercicios_preparcial.R recalcule las claves desde los datos publicados.
    python3 diagnostico/cap4/diag/ejercicios_extrae_preparcial.py
"""
import json, pathlib
raiz = pathlib.Path(__file__).resolve().parents[3]
lin = [l for l in (raiz / 'Htmls_Series/preparcial-corte-2.html').read_text(encoding='utf8').split('\n')
       if l.strip().startswith('const PREPARCIAL_DATOS = ')][0]
datos = json.loads(lin.strip()[len('const PREPARCIAL_DATOS = '):].rstrip(';'))
(pathlib.Path(__file__).parent / 'ejercicios_preparcial_datos.json').write_text(json.dumps(datos), encoding='utf8')
print(len(datos['series']), 'series;', len(datos['items']), 'ítems;', len(datos['simulacro']), 'del simulacro')
