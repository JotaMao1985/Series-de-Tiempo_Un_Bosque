"""v4_firma.py — pone `verificado_por` en las entradas de cap3.yml que los dos
verificadores independientes de la R4 firmaron (listas `v4_firmas_A.txt`, M1–M6,
y `v4_firmas_B.txt`, M7–M10). No toca ningún otro campo: inserta una línea tras
`redactado_por` de cada entrada firmada. Idempotente."""
import pathlib, re
AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
REG = RAIZ / "bibliografia/contraste/cap3.yml"
FIRMAS = {
    "A": "verificador independiente A de la R4 del capítulo 3 (subagente, M1–M6), leyó el pasaje en la caché el 2026-11-21",
    "B": "verificador independiente B de la R4 del capítulo 3 (subagente, M7–M10), leyó el pasaje en la caché el 2026-11-21",
}
# Primera lectura: v4_firmas_A.txt y _B.txt. Segunda lectura, tras la corrección
# del redactor (las entradas cuya prosa cambió perdieron la firma al regenerar el
# registro): v4_firmas_A2.txt y _B2.txt, si existen.
# Las 20 que cambiaron en la segunda pasada solo se firman con la segunda lectura.
RELEER = {
    "c3-m1-04", "c3-m1-15", "c3-m2-30", "c3-m3-11", "c3-m3-15", "c3-m4-31",
    "c3-m5-08", "c3-m5-13", "c3-m5-18", "c3-m5-20", "c3-m6-06", "c3-m6-07",
    "c3-m6-08", "c3-m7-02", "c3-m7-35", "c3-m8-09", "c3-m8-24", "c3-m8-36",
    "c3-m9-20", "c3-m9-23",
}
quien = {}
for lote in "AB":
    for sufijo in ("", "2"):
        ruta = AQUI / f"v4_firmas_{lote}{sufijo}.txt"
        if not ruta.exists():
            continue
        for l in ruta.read_text("utf-8").split():
            if sufijo == "" and l in RELEER:
                continue
            quien[l] = lote
lineas = REG.read_text("utf-8").split("\n")
ids = re.findall(r"^- id: (c3-m\d+-\d+)$", "\n".join(lineas), re.M)
assert set(quien) <= set(ids), set(quien) - set(ids)
salida, actual, firmadas = [], None, 0
for i, l in enumerate(lineas):
    m = re.match(r"^- id: (c3-m\d+-\d+)$", l)
    if m:
        actual = m.group(1)
    salida.append(l)
    if l.startswith("  redactado_por:") and actual in quien:
        if not (i + 1 < len(lineas) and lineas[i + 1].startswith("  verificado_por:")):
            salida.append(f"  verificado_por: {FIRMAS[quien[actual]]}")
        firmadas += 1
REG.write_text("\n".join(salida), "utf-8")
print(f"{len(ids)} entradas · {firmadas} firmadas · sin firmar: {sorted(set(ids) - set(quien))}")
