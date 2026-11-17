"""v4_firma.py — pone `verificado_por` en las entradas de cap2.yml que el
verificador independiente de la R4 sostiene. No toca ningún otro campo: inserta
una línea tras `redactado_por` de cada entrada firmada. Idempotente."""
import pathlib, re, sys
RAIZ = pathlib.Path(__file__).resolve().parents[3]
REG = RAIZ / "bibliografia/contraste/cap2.yml"
FIRMA = ("verificador independiente de la R4 del capítulo 2 (subagente), "
         "leyó el pasaje en la caché el 2026-11-17")
# Primera lectura (2026-11-17): estas 23 quedaron sin firmar.
NO_FIRMADAS_1 = {
    "c2-m1-06", "c2-m1-15", "c2-m2-01", "c2-m2-08", "c2-m2-09", "c2-m3-01",
    "c2-m3-13", "c2-m4-01", "c2-m4-02", "c2-m4-04", "c2-m4-05", "c2-m5-01",
    "c2-m5-07", "c2-m5-09", "c2-m5-11", "c2-m6-04", "c2-m7-01", "c2-m7-06",
    "c2-m7-08", "c2-m7-11", "c2-m8-01", "c2-m8-05", "c2-m9-01",
}
# Segunda lectura (2026-11-17, tras la corrección del redactor): se firman las 80.
NO_FIRMADAS: set[str] = set()
lineas = REG.read_text("utf-8").split("\n")
salida, actual, firmadas = [], None, []
for i, l in enumerate(lineas):
    m = re.match(r"^- id: (c2-m\d+-\d+)$", l)
    if m:
        actual = m.group(1)
    salida.append(l)
    if l.startswith("  redactado_por:") and actual and actual not in NO_FIRMADAS:
        if not (i + 1 < len(lineas) and lineas[i + 1].startswith("  verificado_por:")):
            salida.append(f"  verificado_por: {FIRMA}")
        firmadas.append(actual)
REG.write_text("\n".join(salida), "utf-8")
ids = re.findall(r"^- id: (c2-m\d+-\d+)$", "\n".join(lineas), re.M)
assert NO_FIRMADAS <= set(ids), NO_FIRMADAS - set(ids)
print(f"{len(ids)} entradas · {len(firmadas)} firmadas · {len(NO_FIRMADAS)} sin firmar")
