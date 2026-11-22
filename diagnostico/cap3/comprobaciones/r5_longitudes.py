#!/usr/bin/env python3
"""R5 · longitud de las opciones del quiz del capítulo 3, en caracteres de texto visible.

El diagnóstico (ejercicios.md, §2) midió que en los cinco ítems de una sola
respuesta la correcta era la opción más larga: elegir siempre la más larga daba
5 de 5. Este guion repite la medida sobre la versión publicada antes de la ronda
(`git show HEAD:...`) y sobre el archivo de trabajo.

Texto visible = lo que el estudiante lee en el botón de la opción:
  · se quitan las etiquetas HTML y se resuelven las entidades (&nbsp; cuenta 1);
  · en las fórmulas `$...$` se quitan los delimitadores, `\\operatorname{X}` deja X,
    `\\,` cuenta como un espacio, y se quitan las barras, las llaves y los `_`
    (así `$\\operatorname{Var}(T_t + R_t)$` cuenta «Var(Tt + Rt)», 12 caracteres).
Además de la más larga se mira la más corta: igualar no puede consistir en dejar la
correcta siempre como la más breve.

Uso:  python3 diagnostico/cap3/comprobaciones/r5_longitudes.py
"""
import html
import pathlib
import re
import subprocess

RAIZ = pathlib.Path(__file__).resolve().parents[3]
RUTA = "ensamblado/cap3/cap3_js.js"


def visible(texto: str) -> str:
    t = texto.replace("\\\\", "\\")              # el JS escribe \\ por cada \ de LaTeX
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)

    def formula(m):
        f = m.group(1)
        f = re.sub(r"\\operatorname\{([^}]*)\}", r"\1", f)
        f = f.replace("\\,", " ")
        f = re.sub(r"\\[a-zA-Z]+", "", f)
        return re.sub(r"[{}_\\]", "", f)

    t = re.sub(r"\$([^$]*)\$", formula, t)
    return re.sub(r"\s+", " ", t).strip()


def preguntas(fuente: str):
    ini = fuente.index("AUTOEVALUACIONES['cap3'] = [")
    cuerpo = fuente[ini:fuente.index("\n    ];", ini)]
    # cada pregunta empieza por «tipo: '...'» al nivel de sangría del objeto
    trozos = re.split(r"\n      \{\n        tipo: '", cuerpo)[1:]
    salida = []
    for tr in trozos:
        tipo = tr.split("'", 1)[0]
        ops = re.findall(
            r"texto: '((?:[^'\\]|\\.)*)',\s*correcta: (true|false)", tr)
        salida.append((tipo, [(visible(t), c == "true") for t, c in ops]))
    return salida


def informe(nombre: str, fuente: str):
    print(f"\n=== {nombre} ===")
    print(f"{'ítem':<5}{'tipo':<10}{'longitudes (✔ = correcta)':<44}{'correcta':>9}{'más larga':>10}"
          f"{'media dist.':>12}  ¿la correcta es la más larga?")
    acierta_larga = acierta_corta = n_unica = 0
    for i, (tipo, ops) in enumerate(preguntas(fuente), 1):
        if not ops:
            print(f"Q{i:<4}{tipo:<10}(sin opciones)")
            continue
        largos = [len(t) for t, _ in ops]
        marcas = "  ".join(f"{n}{'✔' if c else ''}" for n, (_, c) in zip(largos, ops))
        corr = [n for n, (_, c) in zip(largos, ops) if c]
        dist = [n for n, (_, c) in zip(largos, ops) if not c]
        if tipo in ("opcion", "grafico"):
            n_unica += 1
            es = corr[0] == max(largos) and largos.count(max(largos)) == 1
            acierta_larga += es
            corta = corr[0] == min(largos) and largos.count(min(largos)) == 1
            acierta_corta += corta
            veredicto = ("SÍ" if es else "no") + (" · y es la MÁS CORTA" if corta else "")
            c = str(corr[0])
        else:
            veredicto = (f"(múltiple) media correctas {sum(corr)/len(corr):.1f} · "
                         f"media falsas {sum(dist)/len(dist):.1f}")
            c = "-"
        print(f"Q{i:<4}{tipo:<10}{marcas:<44}{c:>9}{max(largos):>10}{sum(dist)/len(dist):>12.1f}  {veredicto}")
    print(f"-> eligiendo siempre la opción más larga se aciertan {acierta_larga} de {n_unica} "
          f"ítems de una sola respuesta; eligiendo siempre la más corta, {acierta_corta}")
    # En las de varias respuestas: ¿las k más largas (o las k más cortas) son justo las k correctas?
    for i, (tipo, ops) in enumerate(preguntas(fuente), 1):
        if tipo != "multiple":
            continue
        k = sum(c for _, c in ops)
        orden = sorted(range(len(ops)), key=lambda j: -len(ops[j][0]))
        largas = all(ops[j][1] for j in orden[:k]); cortas = all(ops[j][1] for j in orden[-k:])
        print(f"   Q{i} (múltiple, {k} correctas): las {k} más largas son las correctas: {'SÍ' if largas else 'no'}; "
              f"las {k} más cortas: {'SÍ' if cortas else 'no'}")
    for i, (tipo, ops) in enumerate(preguntas(fuente), 1):
        for t, c in ops:
            print(f"   Q{i} {'✔' if c else ' '} {len(t):>3}  {t}")


antes = subprocess.run(["git", "show", f"5c2fdb3:{RUTA}"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout
informe("ANTES de la R5 (5c2fdb3)", antes)
informe("DESPUÉS de la R5 (archivo de trabajo)", (RAIZ / RUTA).read_text(encoding="utf-8"))
