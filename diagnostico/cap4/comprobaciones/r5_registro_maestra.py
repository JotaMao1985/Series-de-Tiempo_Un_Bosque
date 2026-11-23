#!/usr/bin/env python3
"""
r5_registro_maestra.py — ronda R5 del capítulo 4: lo que la práctica cambió en el registro de fuentes

La R5 movió frases marcadas del ejercicio 2 y rehízo el ejercicio 1. Las frases no cambian de texto
(la huella es la misma), pero tres notas del registro quedaron desfasadas y una frase quedó repetida:

- c4-m10-69 se RETIRA. Al volver al párrafo del lince (hallazgo B3 de la verificación) quedó pegada a
  c4-m10-68, que dice lo mismo con la misma cita (FPP3 §9.1). La plantilla ya no la tiene; aquí la
  entrada pasa de `entradas` a `fuera` con su motivo.
- c4-m10-65: el ejercicio 1 ilustra ahora la lección con un modelo cuyos residuales pasan y cuyas
  raíces no (hallazgo B12).
- c4-m10-67: la frase está ahora en el apartado (b) del ejercicio 2, sobre la liebre (hallazgo B13).
- c4-m10-150: el AR(2) de log(lynx) ya no se imprime en ningún bloque de la página (hallazgo B13).

Edita `bibliografia/_local/herramientas/cap4/r4_entradas.json` (fuera de git) y la columna `r4` del
inventario. Es idempotente. Después: `ensambla_cap4.py`, `r4_registro.py` (que retira la firma de las
entradas cuya nota cambia) y la firma de un verificador que no redactó.

Uso:  python3 diagnostico/cap4/comprobaciones/r5_registro_maestra.py [--comprobar]
"""
import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
ENTRADAS = RAIZ / "bibliografia" / "_local" / "herramientas" / "cap4" / "r4_entradas.json"
INVENTARIO = RAIZ / "bibliografia" / "contraste" / "cap4_inventario.tsv"

RETIRA = {
    "c4-m10-69": "Retirada en la R5 (2026-11-23). Al devolver la frase al párrafo del lince del ejercicio 2 "
                 "quedó inmediatamente detrás de c4-m10-68, que dice lo mismo con la misma cita (FPP3 §9.1); "
                 "la página dice ahora solo «las tres pruebas piden d = 0: la serie es estacionaria», que es "
                 "lo que da el bloque.",
}

NOTAS = {
    "c4-m10-65": "La cita respalda lo que dice el campo afirmacion: elegir por AICc y comprobar los residuales "
                 "son pasos distintos del procedimiento. Desde la R5 el ejercicio 1 ilustra la lección con un "
                 "modelo cuyos residuales pasan Ljung–Box y cuya raíz MA está en el círculo unitario: el diagnóstico "
                 "que enseña el capítulo incluye las raíces (resumen del Módulo 10), que es más de lo que dice el "
                 "pasaje; la frase solo afirma la parte respaldada.",
    "c4-m10-67": "Se deduce en el material: Var(y_t − y_{t−1}) = 2γ0 − 2γ1 = 2(1 − ρ1)Var(y) para una serie "
                 "estacionaria; es la misma afirmación que el capítulo 2 registró como c2-m7-08 (propia, verificada "
                 "en su R4). Desde la R5 la frase está en el apartado (b) del ejercicio 2, sobre log(pelt$Hare): "
                 "r1 = 0.666, cociente esperado 2(1 − r1) = 0.669 y medido 0.673 (R 4.6.0, bloque e2).",
    "c4-m10-150": "Sale de un ajuste propio: arima(log(lynx), order = c(2,0,0), method = 'ML') da phi1 = 1.3776 y "
                  "phi2 = -0.7399; el periodo por las raíces es 9.7839 y la fórmula del periodo medio de un AR(2) con "
                  "ciclos (FPP3 §9.5, condición phi1^2 + 4 phi2 < 0, que aquí vale -1.0617) da 10.0236. «Unos 10 años "
                  "en promedio» es el redondeo de ambos. Desde la R5 ese AR(2) no se imprime en ningún bloque de la "
                  "página; la cifra queda respaldada por el guion de comprobación.",
}
SOFTWARE = {
    "c4-m10-67": "diagnostico/cap4/comprobaciones/r5_bloques/e2.R (salida en e2.out): R 4.6.0, r1 = 0.666, "
                 "cociente = 0.673, 2(1 − r1) = 0.669.",
}
AFIRMACION = {
    "c4-m10-150": "Un AR(2) ajustado a log(lynx) tiene ciclos cuyo periodo medio ronda los 10 años (9.78 por las "
                  "raíces del polinomio AR; 10.02 con la fórmula del periodo medio de FPP3 §9.5).",
}


def main() -> int:
    comprobar = "--comprobar" in sys.argv
    d = json.loads(ENTRADAS.read_text("utf-8"))
    cambios = []
    por_id = {e["id"]: e for e in d["entradas"]}
    fuera = d["fuera"]
    for ident, motivo in RETIRA.items():
        if ident in por_id:
            d["entradas"] = [e for e in d["entradas"] if e["id"] != ident]
            cambios.append(f"retira {ident}")
        if fuera.get(ident) != motivo:
            fuera[ident] = motivo
            cambios.append(f"motivo de {ident} en fuera")
    por_id = {e["id"]: e for e in d["entradas"]}
    for campo, tabla in (("nota", NOTAS), ("software", SOFTWARE), ("afirmacion", AFIRMACION)):
        for ident, valor in tabla.items():
            if por_id[ident].get(campo) != valor:
                por_id[ident][campo] = valor
                cambios.append(f"{campo} de {ident}")
    lineas = INVENTARIO.read_text("utf-8").split("\n")
    for i, l in enumerate(lineas):
        c = l.split("\t")
        if c[0] in RETIRA and c[-1] != "retirada en la R5 (repetía c4-m10-68)":
            c[-1] = "retirada en la R5 (repetía c4-m10-68)"
            lineas[i] = "\t".join(c)
            cambios.append(f"inventario de {c[0]}")
    if comprobar:
        print("pendiente: " + ", ".join(cambios) if cambios else "OK  nada que cambiar")
        return 1 if cambios else 0
    ENTRADAS.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", "utf-8")
    INVENTARIO.write_text("\n".join(lineas), "utf-8")
    print("OK  " + (", ".join(cambios) if cambios else "nada que cambiar"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
