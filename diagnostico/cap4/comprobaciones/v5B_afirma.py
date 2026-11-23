"""Verificador B · R5 cap. 4: compara, entre HEAD y el árbol de trabajo, el texto de cada elemento con
data-afirma y de cada <cite> del capítulo 4 ensamblado (y de las fuentes de ensamblado/cap4/).
Los <template> se parsean como HTML normal (lxml no entra en su contenido): se quitan las etiquetas
<template> antes de parsear."""
import subprocess, re, collections
from bs4 import BeautifulSoup

def cargar(ruta, rev=None):
    if rev:
        return subprocess.run(['git', 'show', f'{rev}:{ruta}'], capture_output=True, text=True, check=True).stdout
    return open(ruta, encoding='utf-8').read()

def extrae(html):
    html = re.sub(r'</?template[^>]*>', '', html)
    s = BeautifulSoup(html, 'lxml')
    af = collections.OrderedDict()
    for el in s.select('[data-afirma]'):
        k = el['data-afirma']
        t = re.sub(r'\s+', ' ', el.get_text()).strip()
        af.setdefault(k, []).append(t)
    cites = collections.Counter()
    for c in s.find_all('cite'):
        cites[(c.get('data-ref'), c.get('data-loc'), c.get('data-modo'), re.sub(r'\s+', ' ', c.get_text()).strip())] += 1
    return af, cites

for ruta in ['Htmls_Series/capitulo-4-modelos-arima.html']:
    a0, c0 = extrae(cargar(ruta, 'HEAD')); a1, c1 = extrae(cargar(ruta))
    print(f'== {ruta}')
    print(f'ids data-afirma: HEAD {len(a0)} · ahora {len(a1)}; elementos: {sum(map(len, a0.values()))} · {sum(map(len, a1.values()))}')
    print('ids que faltan ahora:', sorted(set(a0) - set(a1)))
    print('ids nuevos:', sorted(set(a1) - set(a0)))
    cambian = [k for k in a0 if k in a1 and a0[k] != a1[k]]
    print('ids cuyo texto cambia:', cambian)
    for k in cambian:
        print('  ', k, '\n    ANTES:', a0[k], '\n    AHORA:', a1[k])
    print(f'<cite>: HEAD {sum(c0.values())} · ahora {sum(c1.values())}')
    print('  cites que faltan:', list((c0 - c1).items()))
    print('  cites nuevos:', list((c1 - c0).items()))
    # posición: orden de aparición de los ids
    o0 = list(a0); o1 = list(a1)
    movidos = [k for k in o0 if k in o1 and abs(o0.index(k) - o1.index(k)) > 0]
    print('ids cuyo orden relativo cambia (índice antes -> ahora):',
          [(k, o0.index(k), o1.index(k)) for k in movidos if o0.index(k) != o1.index(k)][:40])
