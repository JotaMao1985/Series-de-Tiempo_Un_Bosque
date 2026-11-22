#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Valida bibliografia/contraste/cap4_inventario.tsv contra el capítulo y la biblioteca. No escribe nada.
Comprueba: 10 columnas; ids únicos y bien formados (c4-mN-XX, N = módulo); tipo y prioridad del vocabulario cerrado;
`texto` es subcadena de la línea `linea` del HTML (con las etiquetas quitadas); las claves de fuente_candidata están en
referencias.json o son «falta-obra: …»; todo id citado en donde_buscar existe; `hallado` y `r4` vacíos.
Uso:  python3 diagnostico/cap4/diag/fuentes_valida.py > diagnostico/cap4/diag/fuentes_valida.out
"""
import csv
import html
import json
import os
import re
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
TSV = os.path.join(RAIZ, 'bibliografia', 'contraste', 'cap4_inventario.tsv')
HTML = os.path.join(RAIZ, 'Htmls_Series', 'capitulo-4-modelos-arima.html')
REFS = os.path.join(RAIZ, 'bibliografia', 'referencias.json')
TIPOS = {'definicion', 'resultado', 'regla', 'dato', 'atribucion', 'historica'}
PRIO = {'alta', 'media', 'baja'}

lineas = open(HTML, encoding='utf-8').read().split('\n')
claves = {x['id'] for x in json.load(open(REFS, encoding='utf-8'))}
filas = list(csv.DictReader(open(TSV, encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE))
errores = []
ids = [f['id'] for f in filas]
if len(ids) != len(set(ids)):
    errores.append('ids repetidos')
for f in filas:
    i = f['id']
    if None in f or len(f) != 10:
        errores.append(f'{i}: número de columnas distinto de 10')
        continue
    m = re.fullmatch(r'c4-m(\d+)-(\d+)', i)
    if not m or int(m.group(1)) != int(f['modulo']):
        errores.append(f'{i}: id mal formado o módulo distinto')
    if f['tipo'] not in TIPOS:
        errores.append(f'{i}: tipo {f["tipo"]}')
    if f['prioridad'] not in PRIO:
        errores.append(f'{i}: prioridad {f["prioridad"]}')
    if f['hallado'] or f['r4']:
        errores.append(f'{i}: hallado o r4 no vacíos')
    n = int(f['linea'])
    crudo = re.sub(r'<[^>]+>', '', lineas[n - 1])
    if f['texto'] not in crudo and html.unescape(f['texto']) not in html.unescape(crudo):
        errores.append(f'{i}: el texto no está en la línea {n}')
    for k in [x.strip() for x in f['fuente_candidata'].split(';')]:
        if k.startswith('falta-obra') or ' ' in k or ':' in k or k.startswith('propia'):
            continue
        if k not in claves:
            errores.append(f'{i}: clave fuera de referencias.json: {k}')
    for r in re.findall(r'c4-m\d+-\d+', f['donde_buscar']):
        if r not in set(ids):
            errores.append(f'{i}: cita un id inexistente: {r}')
print(f'{len(filas)} filas · {len(errores)} problemas')
for e in errores:
    print(' ', e)
sys.exit(1 if errores else 0)
