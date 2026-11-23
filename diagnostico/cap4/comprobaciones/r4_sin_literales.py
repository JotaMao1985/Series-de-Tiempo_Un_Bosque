#!/usr/bin/env python3
"""
r4_sin_literales.py — ningún literal de cita del capítulo 4 en un archivo que vaya a git

Toma los literales de `bibliografia/_local/citas/cap4.yml` (fuera de git) y los
busca, normalizados, en los archivos de la ronda que sí se versionan. Un literal
de menos de cuatro palabras no se busca (sería un título o un término).

Uso:  python3 diagnostico/cap4/comprobaciones/r4_sin_literales.py
"""
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import r4_lib as L  # noqa: E402

A = L.A
ARCHIVOS = ["bibliografia/contraste/cap4.yml", "bibliografia/contraste/cap4_inventario.tsv",
            "Htmls_Series/capitulo-4-modelos-arima.html", "precalculo/genera_cap4.R",
            "ensamblado/ensambla_cap4.py", "ensamblado/ensambla_cap5.py",
            "diagnostico/cap4/R4_cambios.md"]
ARCHIVOS += sorted(str(p.relative_to(L.RAIZ)) for p in (L.RAIZ / "ensamblado/cap4").glob("*"))
ARCHIVOS += sorted(str(p.relative_to(L.RAIZ)) for p in (L.RAIZ / "diagnostico/cap4/comprobaciones").rglob("r4_*")
                   if p.is_file())
ARCHIVOS += sorted(str(p.relative_to(L.RAIZ)) for p in (L.RAIZ / "diagnostico/cap4/comprobaciones/r4_software").rglob("*")
                   if p.is_file())


def main() -> int:
    citas = yaml.safe_load((L.RAIZ / "bibliografia/_local/citas/cap4.yml").read_text("utf-8"))["citas"]
    literales = {(i, n): A.normaliza(str(t)).lower() for i, d in citas.items() for n, t in d.items()
                 if len(str(t).split()) >= 4}
    fallos = 0
    for nombre in ARCHIVOS:
        ruta = L.RAIZ / nombre
        if not ruta.is_file():
            continue
        texto = A.normaliza(ruta.read_text("utf-8", "replace")).lower()
        for (i, n), lit in literales.items():
            if lit in texto:
                print(f"FALLA  {nombre}: lleva el literal de {i} · fuente {n}")
                fallos += 1
    print(f"{'FALLA' if fallos else 'OK'}: {len(literales)} literales buscados en {len(ARCHIVOS)} archivos; {fallos} hallados")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
