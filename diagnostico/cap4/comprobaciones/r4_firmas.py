#!/usr/bin/env python3
"""
r4_firmas.py — ronda R4 del capítulo 4: las firmas de los verificadores, al registro

Los dos verificadores independientes no tocan `bibliografia/contraste/cap4.yml`:
dejan la lista de lo que firman en `v4_firmas_A.txt` (M1–M6) y `v4_firmas_B.txt`
(M7–M10), un id por línea. Este guion pone `verificado_por` en esas entradas,
justo después de `redactado_por`, sin tocar nada más. Después, `r4_registro.py`
conserva cada firma solo mientras no cambie lo que se firmó (prosa, veredicto,
fuentes, nota), y la retira si cambia.

Cada aparición de un id en la lista es UNA firma, y se aplica una sola vez: las ya
aplicadas se apuntan en `r4_firmas_puestas.txt`. Así una firma que `r4_registro.py`
retiró no vuelve sola; para firmar otra vez lo cambiado, el verificador añade el id
otra vez al final de su lista (segunda lectura). Es reejecutable.

Uso:  python3 diagnostico/cap4/comprobaciones/r4_firmas.py
"""
import collections
import pathlib
import re
import sys

import yaml

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
REGISTRO = RAIZ / "bibliografia" / "contraste" / "cap4.yml"
# Entradas retiradas después de firmarse (p. ej. c4-m10-69 en la R5): sus firmas viejas se ignoran.
RETIRADAS = {"c4-m10-69"}
FIRMAS = {
    "A": ("v4_firmas_A.txt", "verificador independiente A de la R4 del capítulo 4 (subagente, M1–M6), "
                             "leyó el pasaje en la caché el 2026-11-23"),
    "B": ("v4_firmas_B.txt", "verificador independiente B de la R4 del capítulo 4 (subagente, M7–M10), "
                             "leyó el pasaje en la caché el 2026-11-23"),
    # Ronda R5: lo que la práctica movió o cambió de nota lo vuelve a firmar su verificador B,
    # que no redactó la R5 ni las notas (las escribió la maestra en r5_registro_maestra.py).
    "R5B": ("v5_firmas_B.txt", "verificador independiente B de la R5 del capítulo 4 (subagente, E1–E3 y quiz), "
                               "leyó el pasaje en la caché el 2026-11-23"),
}


def main() -> int:
    texto = REGISTRO.read_text("utf-8")
    entradas = {e["id"]: e for e in yaml.safe_load(texto)["afirmaciones"]}
    ruta_puestas = AQUI / "r4_firmas_puestas.txt"
    aplicadas = collections.Counter(ruta_puestas.read_text("utf-8").split() if ruta_puestas.exists() else [])
    nuevas_aplicadas = []
    puestas, ya, faltan = 0, 0, []
    for lote, (archivo, firma) in FIRMAS.items():
        if not (AQUI / archivo).exists():
            continue
        ids = [x.strip() for x in (AQUI / archivo).read_text("utf-8").split() if x.strip()]
        for ident, veces in collections.Counter(ids).items():
            if ident not in entradas:
                if ident not in RETIRADAS:          # una firma de algo que una ronda posterior retiró
                    faltan.append(f"{lote}: {ident}")
                continue
            if veces <= aplicadas[f"{lote}:{ident}"]:
                ya += 1
                continue                      # esa firma ya se aplicó (y quizá se retiró después)
            nuevas_aplicadas += [f"{lote}:{ident}"] * (veces - aplicadas[f"{lote}:{ident}"])
            if entradas[ident].get("verificado_por"):
                ya += 1
                continue
            patron = re.compile(r"(\n- id: " + re.escape(ident) + r"\n(?:(?!\n- id: ).)*?\n  redactado_por: [^\n]*\n)",
                                re.S)
            m = list(patron.finditer(texto))
            if len(m) != 1:
                sys.exit(f"ABORTA: la entrada {ident} aparece {len(m)} veces con su redactado_por")
            texto = texto[:m[0].end()] + f'  verificado_por: "{firma}"\n' + texto[m[0].end():]
            puestas += 1
    if faltan:
        sys.exit("ABORTA: ids firmados que no están en el registro: " + ", ".join(faltan))
    relee = yaml.safe_load(texto)["afirmaciones"]
    assert [e["id"] for e in relee] == list(entradas), "el orden de las entradas cambió"
    REGISTRO.write_text(texto, "utf-8")
    ruta_puestas.write_text("".join(f"{x}\n" for x in sorted((aplicadas + collections.Counter(nuevas_aplicadas)).elements())), "utf-8")
    firmadas = sum(1 for e in relee if e.get("verificado_por"))
    print(f"OK  {puestas} firmas puestas, {ya} ya estaban; {firmadas} de {len(relee)} entradas firmadas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
