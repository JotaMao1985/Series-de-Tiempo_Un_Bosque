#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cuenta el inventario cap4_inventario.tsv: tipo × prioridad, etiquetas de donde_buscar, obras citadas, filas por módulo y estado de la lectura.
Adaptado de diagnostico/cap3/diag/fuentes_cuenta.py.
Uso:  python3 diagnostico/cap4/diag/fuentes_cuenta.py > diagnostico/cap4/diag/fuentes_cuenta.out
"""
import collections
import csv
import os
import re

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
TSV = os.path.join(RAIZ, 'bibliografia', 'contraste', 'cap4_inventario.tsv')
filas = list(csv.DictReader(open(TSV, encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE))
assert all(len(f) == 10 and None not in f for f in filas), 'hay filas con un número de columnas distinto de 10'
print('filas:', len(filas), '· columnas:', list(filas[0].keys()))
print('hallado y r4 vacíos:', all(f['hallado'] == '' and f['r4'] == '' for f in filas))

TIPOS = ['definicion', 'resultado', 'regla', 'dato', 'atribucion', 'historica']
t = collections.defaultdict(collections.Counter)
for f in filas:
    t[f['tipo']][f['prioridad']] += 1
print('\n| tipo | alta | media | baja | total |\n|---|---:|---:|---:|---:|')
tot = collections.Counter()
for k in TIPOS:
    c = t[k]
    print(f"| {k} | {c['alta']} | {c['media']} | {c['baja']} | {sum(c.values())} |")
    tot.update(c)
print(f"| **total** | **{tot['alta']}** | **{tot['media']}** | **{tot['baja']}** | **{sum(tot.values())}** |")

mods = collections.Counter(int(f['modulo']) for f in filas)
print('\nfilas por módulo:', dict(sorted(mods.items())))

ETIQ = ['[DISCREPA', '[ERROR', '[CON-MATIZ', '[TENSIÓN', '[NO HALLADO', '[PARCIAL', '[NO COMPROBABLE', '[SIN GENERADOR',
        '[EJEMPLAR', '[SIN LEER', '[= c', 'REPITE']
print('\netiquetas en donde_buscar (filas que la llevan; alta entre paréntesis):')
for e in ETIQ:
    fs = [f for f in filas if e in f['donde_buscar']]
    print(f"  {e:18} {len(fs):3}  ({sum(1 for f in fs if f['prioridad'] == 'alta')})")

print('\nobras candidatas (filas que las nombran):')
obras = collections.Counter()
for f in filas:
    cont = False
    for k in [x.strip() for x in f['fuente_candidata'].split(';')]:
        if k.startswith('falta-obra'):
            cont = True
            obras['falta-obra'] += 1
        elif re.fullmatch(r'[a-z]+\d{4}[a-z]+', k):
            cont = False
            obras[k] += 1
        elif not cont:
            obras[k] += 1
for k, n in obras.most_common():
    print(f'  {k:40} {n}')

print('\nfalta-obra (texto tras «falta-obra:», distintas):')
faltan = collections.Counter()
for f in filas:
    for m in re.finditer(r'falta-obra:\s*([^;]+)', f['fuente_candidata']):
        faltan[m.group(1).strip()] += 1
for k, n in sorted(faltan.items(), key=lambda x: (-x[1], x[0])):
    print(f'  {n:3}  {k}')


def estado(f):
    d, fu = f['donde_buscar'], f['fuente_candidata']
    if any(e in d for e in ('[DISCREPA', '[ERROR')):
        return 'discrepa o error'
    if any(e in d for e in ('[CON-MATIZ', '[TENSIÓN')):
        return 'con matiz o tensión'
    if any(e in d for e in ('[NO COMPROBABLE', '[SIN LEER', '[EJEMPLAR')):
        return 'no comprobable aquí (obra sin texto en disco)'
    if '[NO HALLADO' in d:
        return 'no hallado en lo leído'
    if '[SIN GENERADOR' in d:
        return 'sin generador (norma 1)'
    if '[PARCIAL' in d:
        return 'parcial'
    if 'Respaldada' in d or 'respaldada' in d:
        return 'respaldada en lo leído'
    if fu.startswith('falta-obra: ninguna') or 'declarar propia' in fu or 'la cifra sale de R' in fu:
        return 'propia o sin fuente necesaria'
    return 'localizada, sin veredicto'


ORDEN = ['respaldada en lo leído', 'parcial', 'con matiz o tensión', 'discrepa o error', 'no hallado en lo leído',
         'no comprobable aquí (obra sin texto en disco)', 'sin generador (norma 1)', 'propia o sin fuente necesaria',
         'localizada, sin veredicto']
e = collections.defaultdict(collections.Counter)
for f in filas:
    e[estado(f)][f['prioridad']] += 1
print('\n| estado de la lectura | alta | media | baja | total |\n|---|---:|---:|---:|---:|')
tt = collections.Counter()
for k in ORDEN:
    c = e[k]
    print(f"| {k} | {c['alta']} | {c['media']} | {c['baja']} | {sum(c.values())} |")
    tt.update(c)
print(f"| **total** | **{tt['alta']}** | **{tt['media']}** | **{tt['baja']}** | **{sum(tt.values())}** |")

print('\nfilas por módulo × tipo de afirmación atribuida (atribucion + historica):')
for m in sorted(mods):
    n = sum(1 for f in filas if int(f['modulo']) == m and f['tipo'] in ('atribucion', 'historica'))
    print(f'  M{m:<2} {n}')
