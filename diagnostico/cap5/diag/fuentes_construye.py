#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construye bibliografia/contraste/cap5_inventario.tsv a partir de fuentes_filas_{a,b,c,d}.py y lo valida.
Resuelve los localizadores @C @S @H @F @R @K contra la caché `bibliografia/_local/` (ruta:línea de la primera línea que
contiene el patrón) y las referencias {clave} a ids de otras filas (c5-mN-XX, N = módulo, XX por orden de línea).
Comprueba: `texto` es subcadena de la línea `linea` del HTML (sin etiquetas, con espacios normalizados); las claves de
fuente_candidata están en referencias.json o son «falta-obra: …»; todo id citado existe; ningún `hallado` ni `r4`.
Uso:  python3 diagnostico/cap5/diag/fuentes_construye.py            (escribe el TSV)
      python3 diagnostico/cap5/diag/fuentes_construye.py --solo-valida
"""
import collections
import csv
import html
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
# Las filas (fuentes_filas_{a,b,c,d}.py) llevan como clave de búsqueda fragmentos literales de los libros:
# viven fuera de git, en bibliografia/_local/herramientas/cap5/diagnostico/ (el repo es público).
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(AQUI))),
                                'bibliografia', '_local', 'herramientas', 'cap5', 'diagnostico'))
RAIZ = os.path.abspath(os.path.join(AQUI, '..', '..', '..'))
HTML = os.path.join(RAIZ, 'Htmls_Series', 'capitulo-5-sarima.html')
TSV = os.path.join(RAIZ, 'bibliografia', 'contraste', 'cap5_inventario.tsv')
LOCAL = os.path.join(RAIZ, 'bibliografia', '_local')
REFS = os.path.join(RAIZ, 'bibliografia', 'referencias.json')

from fuentes_filas_a import FILAS_A  # noqa: E402
from fuentes_filas_b import FILAS_B  # noqa: E402
from fuentes_filas_c import FILAS_C  # noqa: E402
from fuentes_filas_d import FILAS_D  # noqa: E402

TIPOS = {'definicion', 'resultado', 'regla', 'dato', 'atribucion', 'historica'}
PRIO = {'alta', 'media', 'baja'}
COLUMNAS = ['id', 'modulo', 'linea', 'tipo', 'texto', 'fuente_candidata', 'donde_buscar', 'hallado', 'prioridad', 'r4']

lineas = open(HTML, encoding='utf-8').read().split('\n')
claves = {x['id'] for x in json.load(open(REFS, encoding='utf-8'))}
errores = []


def norm(s):
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


def busca(ruta, patron):
    """Primera línea (1-based) de `ruta` (bajo _local) que contiene `patron`; None si no hay."""
    p = os.path.join(LOCAL, ruta)
    if not os.path.exists(p):
        return None
    for n, l in enumerate(open(p, encoding='utf-8', errors='replace'), 1):
        if patron in l:
            return n
    return None


def resuelve(m):
    tipo, arg, patron = m.group(1), m.group(2), m.group(3)
    if tipo == 'C':
        ruta, imp = f'texto/cryer2008time/p{arg}.txt', f' (impr. {int(arg) - 10})'
    elif tipo == 'S':
        ruta, imp = f'texto/shumway2011time/p{arg}.txt', f' (impr. {int(arg) - 13})'
    elif tipo == 'H':
        ruta, imp = f'texto/hyndman2008automatic/p{arg}.txt', f' (impr. {int(arg)})'
    elif tipo == 'F':
        ruta, imp = f'web/hyndman2021forecasting/{arg}.txt', ''
    elif tipo == 'R':
        ruta, imp = f'web/rcoreteam2026r/{arg}.txt', ''
    else:
        ruta, imp = f'web/hyndman2026forecast/{arg}.txt', ''
    n = busca(ruta, patron)
    if n is None:
        errores.append(f'localizador sin hallar: @{tipo}({arg}|{patron})')
        return f'«{ruta}:??»'
    return f'{ruta}:{n}{imp}'


LOCALIZADOR = re.compile(r'@([CSHFRK])\(([^|()]+)\|([^()]+)\)')

filas = [f for grupo in (FILAS_A, FILAS_B, FILAS_C, FILAS_D) for f in grupo]
# orden: módulo, línea; estable dentro de la misma línea
filas = sorted(enumerate(filas), key=lambda x: (x[1][1], x[1][2], x[0]))
filas = [f for _, f in filas]
ids, contador = {}, collections.Counter()
for clave, mod, lin, tipo, texto, fuente, donde, prio in filas:
    if clave in ids:
        errores.append(f'clave repetida: {clave}')
    contador[mod] += 1
    ids[clave] = f'c5-m{mod}-{contador[mod]:02d}'

salida = []
for clave, mod, lin, tipo, texto, fuente, donde, prio in filas:
    i = ids[clave]
    if tipo not in TIPOS:
        errores.append(f'{i}: tipo {tipo}')
    if prio not in PRIO:
        errores.append(f'{i}: prioridad {prio}')
    crudo = norm(re.sub(r'<[^>]+>', '', lineas[lin - 1]))
    if norm(texto) not in crudo:
        errores.append(f'{i} ({clave}): el texto no está en la línea {lin}: {texto[:70]!r}')
    for k in [x.strip() for x in fuente.split(';')]:
        if k.startswith('falta-obra') or ' ' in k or ':' in k or k.startswith('propia'):
            continue
        if k not in claves:
            errores.append(f'{i}: clave fuera de referencias.json: {k}')
    d = LOCALIZADOR.sub(resuelve, donde)

    def sustituye(m):
        k = m.group(1)
        if k in ids:
            return ids[k]
        errores.append(f'{i}: referencia {{{k}}} sin fila')
        return m.group(0)
    d = re.sub(r'\{([A-Za-z0-9_]+)\}', sustituye, d)
    for campo, v in (('texto', texto), ('fuente', fuente), ('donde', d)):
        if '\t' in v or '\n' in v:
            errores.append(f'{i}: tabulador o salto de línea en {campo}')
    salida.append([i, str(mod), str(lin), tipo, norm(texto) if False else texto, fuente, d, '', prio, ''])

# Una fila que solo repite a otra hereda sus etiquetas de estado (para que el recuento las cuente igual).
ETIQ = ['DISCREPA', 'ERROR', 'CON-MATIZ', 'TENSIÓN', 'NO COMPROBABLE', 'EJEMPLAR', 'NO HALLADO', 'SIN GENERADOR', 'PARCIAL']
por_id = {r[0]: r for r in salida}
for r in salida:
    d = r[6]
    if 'REPITE' not in d or any(f'[{e}' in d for e in ETIQ) or 'espaldada' in d:
        continue
    m = re.search(r'REPITE (c5-m\d+-\d+)', d)
    if not m or m.group(1) not in por_id:
        continue
    o = por_id[m.group(1)][6]
    et = [e for e in ETIQ if f'[{e}' in o]
    if et:
        r[6] = d + ' ' + ' '.join(f'[{e}]' for e in et) + f' (heredado de {m.group(1)})'
    elif 'espaldada' in o:
        r[6] = d + f' Respaldada (heredado de {m.group(1)})'

# ids citados en donde_buscar (con «c5-») deben existir
existentes = {r[0] for r in salida}
for r in salida:
    for x in re.findall(r'c5-m\d+-\d+', r[6]):
        if x not in existentes:
            errores.append(f'{r[0]}: cita un id inexistente: {x}')

print(f'{len(salida)} filas · {len(errores)} problemas')
for e in errores:
    print(' ', e)
if errores:
    sys.exit(1)
if '--solo-valida' not in sys.argv:
    with open(TSV, 'w', encoding='utf-8', newline='') as fh:
        fh.write('\t'.join(COLUMNAS) + '\n')
        for r in salida:
            fh.write('\t'.join(r) + '\n')
    print('escrito', os.path.relpath(TSV, RAIZ))
    json.dump(ids, open(os.path.join(AQUI, 'fuentes_ids.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0, sort_keys=True)
