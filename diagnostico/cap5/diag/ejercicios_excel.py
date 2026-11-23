"""Diagnóstico cap. 5 · el ejercicio en Excel como práctica (solo lectura, openpyxl).

    python3 diagnostico/cap5/diag/ejercicios_excel.py > diagnostico/cap5/diag/ejercicios_excel.out

Compara celda a celda el libro del estudiante con el de la solución: qué celdas deja en
blanco el del estudiante (lo que se pide), qué fórmula tiene la solución, qué instrucción
lleva al lado y si la comprobación de la hoja la cubre. También: qué series usa el libro,
qué parte de cada hoja ya viene resuelta (fórmulas presentes en el libro del estudiante)
y si hay preguntas abiertas (texto «¿…?») o celdas de respuesta con validación.
No ejecuta Excel ni recalcula: el recálculo real es de precalculo/verifica_excel_cap5.py.
"""
import re, pathlib, collections
import openpyxl
limpia = lambda t, n: re.sub(r'\s+', ' ', t)[:n]
raiz = pathlib.Path(__file__).resolve().parents[3]
d = raiz / 'Htmls_Series/ejercicios'
E = openpyxl.load_workbook(d / 'capitulo-5-sarima-ejercicio.xlsx')
S = openpyxl.load_workbook(d / 'capitulo-5-sarima-solucion.xlsx')
Sv = openpyxl.load_workbook(d / 'capitulo-5-sarima-solucion.xlsx', data_only=True)

def es_formula(v): return isinstance(v, str) and v.startswith('=')
tot = collections.Counter()
print(f"{'Hoja':<20} {'fórm.sol':>8} {'fórm.est':>8} {'en blanco':>9} {'% pedido':>8} {'comprob.':>8} {'¿…?':>4} {'valid.':>6}")
detalle = {}
for ws in S.worksheets:
    we = E[ws.title]
    fs = fe = vac = 0
    pedidas = []
    for fila in ws.iter_rows():
        for c in fila:
            ce = we[c.coordinate]
            if es_formula(c.value):
                fs += 1
                if es_formula(ce.value): fe += 1
                elif ce.value in (None, ''):
                    vac += 1; pedidas.append((c.coordinate, c.value, ce.comment.text if ce.comment else None))
    textos = [str(c.value) for fila in we.iter_rows() for c in fila if isinstance(c.value, str) and not es_formula(c.value)]
    preg = sum(t.count('¿') for t in textos)
    comprob = sum(1 for t in textos if re.search(r'[Cc]omprobaci|coincide', t))
    val = len(we.data_validations.dataValidation)
    detalle[ws.title] = (pedidas, textos)
    tot.update(dict(fs=fs, fe=fe, vac=vac))
    print(f"{ws.title:<20} {fs:>8} {fe:>8} {vac:>9} {(100*vac/fs if fs else 0):>7.1f}% {comprob:>8} {preg:>4} {val:>6}")
print(f"{'TOTAL':<20} {tot['fs']:>8} {tot['fe']:>8} {tot['vac']:>9} {100*tot['vac']/tot['fs']:>7.1f}%")

print("\n### Celdas que se piden (en blanco en el libro del estudiante), por hoja: fórmula de la solución e instrucción del comentario")
for h, (pedidas, _) in detalle.items():
    if not pedidas: continue
    print(f"\n[{h}] {len(pedidas)} celdas")
    vistas = set()
    for coord, f, com in pedidas:
        # agrupa por la forma de la fórmula (sin números de fila) para no listar 100 celdas iguales
        forma = re.sub(r'\d+', '#', f)
        if forma in vistas: continue
        vistas.add(forma)
        print(f"  {coord}: {f[:110]}")
        if com: print(f"      comentario: {limpia(com, 220)}")

print("\n### Series y textos de la portada")
P = E['Portada']
for fila in P.iter_rows():
    for c in fila:
        if isinstance(c.value, str) and len(c.value) > 3:
            print(f"  {c.coordinate}: {limpia(c.value, 240)}")
print("\n### Cabeceras de la hoja Datos")
D = E['Datos']
for c in D[1] + D[2] + D[3]:
    if c.value is not None: print(f"  {c.coordinate}: {str(c.value)[:80]}")

print("\n### Preguntas abiertas (texto con «¿») en las hojas del estudiante")
for h, (_, textos) in detalle.items():
    for t in textos:
        if '¿' in t: print(f"  [{h}] {limpia(t, 260)}")

print("\n### Primeras líneas de instrucciones de cada hoja (filas 1-6, columna A-B)")
for ws in E.worksheets[2:]:
    for r in range(1, 7):
        for col in 'AB':
            v = ws[f'{col}{r}'].value
            if isinstance(v, str) and len(v) > 20: print(f"  [{ws.title}] {col}{r}: {limpia(v, 260)}")

print("\n### Fórmulas distintas que escribe el estudiante (celdas en blanco con instrucción en comentario) y comprobaciones ✔/✘ por hoja")
T = collections.Counter()
for ws in E.worksheets:
    pedidas, _ = detalle[ws.title]
    con_com = sum(1 for _, _, c in pedidas if c)
    T['com'] += con_com
    chk = sum(1 for fila in S[ws.title].iter_rows() for c in fila if es_formula(c.value) and '"✔"' in c.value)
    T['chk'] += chk
    print(f"  {ws.title:<20} celdas {len(pedidas):>5} · fórmulas con instrucción {con_com:>3} · celdas de comprobación ✔/✘ {chk:>3}")
print(f"  TOTAL fórmulas con instrucción {T['com']} · celdas de comprobación {T['chk']} · preguntas «¿» {sum(sum(t.count('¿') for t in tx) for _, tx in detalle.values())}")
series = collections.Counter()
for ws in E.worksheets:
    for fila in ws.iter_rows():
        for c in fila:
            if isinstance(c.value, str):
                for s in ('AirPassengers', 'USAccDeaths', 'TRM', 'co2', 'heladería', 'tienda'):
                    if s.lower() in c.value.lower(): series[s] += 1
print("\n### Menciones de series en el libro del estudiante:", dict(series))

print("\n### ¿La instrucción dicta la fórmula? (comentario con una llamada a función de Excel, «=» seguido de celda, o la ecuación con sus celdas)")
dicta = re.compile(r'([A-Z][A-Z0-9.]+\()|(=\s*[A-Z]{1,2}\$?\d)|(\b[A-Z]{1,2}\$?\d+\s*[−\-+*/]\s*[A-Z]{1,2}\$?\d+)')
tot_c = tot_d = 0
for ws in E.worksheets:
    pedidas, _ = detalle[ws.title]
    coms = [c for _, _, c in pedidas if c]
    dd = [c for c in coms if dicta.search(c)]
    tot_c += len(coms); tot_d += len(dd)
    if coms: print(f"  {ws.title:<20} {len(dd)} de {len(coms)}")
print(f"  TOTAL {tot_d} de {tot_c}")
