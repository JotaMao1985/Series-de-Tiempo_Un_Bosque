"""Verificador B · R5 cap. 4: ¿hay texto literal de libro en lo que iría a git?
Compara 7-gramas de palabras de (a) las líneas añadidas en el diff de ensamblado/cap4 y (b) los archivos
nuevos r5_* y v5B_* de diagnostico/cap4 (y R5_cambios.md) contra el texto de los libros y páginas en
bibliografia/_local/texto, bibliografia/_local/web y bibliografia/_local/citas (que no van a git).
Excluye la ayuda de R (rcoreteam2026r) y de los paquetes de software solo en el informe, no en la búsqueda."""
import subprocess, re, glob, os, html, collections
N = 7
def palabras(t):
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t)).lower()
    return re.findall(r"[a-záéíóúñü0-9]+", t)
def ngramas(ws): return {' '.join(ws[i:i+N]) for i in range(len(ws) - N + 1)}
corpus = collections.defaultdict(set)
for f in glob.glob('bibliografia/_local/texto/**/*', recursive=True) + glob.glob('bibliografia/_local/web/**/*', recursive=True) + glob.glob('bibliografia/_local/citas/*'):
    if os.path.isfile(f):
        try: t = open(f, encoding='utf-8', errors='ignore').read()
        except Exception: continue
        for g in ngramas(palabras(t)): corpus[g].add(f.split('/')[2] + '/' + f.split('/')[3])
print('7-gramas en la caché:', len(corpus))
diff = subprocess.run(['git', 'diff', '-U0', '--', 'ensamblado/cap4'], capture_output=True, text=True).stdout
añadido = '\n'.join(l[1:] for l in diff.splitlines() if l.startswith('+') and not l.startswith('+++'))
fuentes = {'diff ensamblado/cap4 (líneas añadidas)': añadido}
for f in sorted(glob.glob('diagnostico/cap4/comprobaciones/r5_*') + glob.glob('diagnostico/cap4/comprobaciones/r5_bloques/*')
                + glob.glob('diagnostico/cap4/comprobaciones/v5B_*') + ['diagnostico/cap4/R5_cambios.md']):
    if os.path.isfile(f) and not f.endswith('.json'):
        fuentes[f] = open(f, encoding='utf-8', errors='ignore').read()
total = 0
for nombre, t in fuentes.items():
    hits = [(g, sorted(corpus[g])) for g in ngramas(palabras(t)) if g in corpus]
    # descartar coincidencias de código o de nombres de funciones (todas las palabras con dígitos o muy cortas)
    hits = [(g, o) for g, o in hits if sum(len(w) > 3 and not w.isdigit() for w in g.split()) >= 4]
    if hits:
        total += len(hits)
        print(f'\n== {nombre}: {len(hits)} 7-gramas coinciden')
        for g, o in sorted(hits)[:15]: print('   ', g, '<-', ', '.join(o[:3]))
print('\ncoincidencias en total:', total)
