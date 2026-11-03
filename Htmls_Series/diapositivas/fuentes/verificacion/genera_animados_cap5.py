#!/usr/bin/env python3
"""Genera los tres gráficos animados de las diapositivas del capítulo 5 desde el JSON del precálculo.

Ninguna cifra se escribe a mano: todas salen de `precalculo/salidas/cap5_sarima.json`
(R 4.6, forecast 9.0.2), con los decimales que usa el capítulo.

    diferencias.json  M3 · ρ̂₁ y ρ̂₁₂ de log(AirPassengers) con cada combinación de ∇ y ∇₁₂
    satelites.json    M2 · ACF teórica de un SAR(1) y de un AR(1)×SAR(1): brotan 11 y 13
    escalones.json    M5 · pesos ψ_j del airline y σ_h, por tramos

Uso (desde la raíz del repositorio):
    python3 Htmls_Series/diapositivas/fuentes/verificacion/genera_animados_cap5.py
`verifica_cifras_cap5.py` llama a `construye()` y exige que lo escrito en disco sea idéntico.
"""
from __future__ import annotations

import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[3]
DESTINO = AQUI.parent / "recursos" / "cap5"
J = json.loads((RAIZ / "precalculo/salidas/cap5_sarima.json").read_text(encoding="utf-8"))


def f(x: float, d: int) -> str:
    """Redondeo a la mitad hacia arriba, como el resto de la verificación."""
    s = f"{abs(x) + 1e-12:.{d}f}"
    return ("−" if x < 0 and float(s) != 0 else "") + s


def diferencias() -> dict:
    comb = J["airpassengers"]["combinaciones"]
    orden = [("d0_D0", "log y_{t}"), ("d1_D0", "∇ log y_{t}"), ("d0_D1", "∇_{12} log y_{t}"), ("d1_D1", "∇∇_{12} log y_{t}")]
    etapas = []
    for clave, rotulo in orden:
        c = comb[clave]
        etapas.append([
            {"tipo": "barra", "serie": 1, "x": rotulo, "y": c["acf1"], "texto": f(c["acf1"], 2), "ancho": 0.3, "desplazamiento": -0.17},
            {"tipo": "barra", "serie": 2, "x": rotulo, "y": c["acf12"], "texto": f(c["acf12"], 2), "ancho": 0.3, "desplazamiento": 0.17},
            {"tipo": "texto", "serie": 0, "x": rotulo, "y": -0.66, "texto": f"var = {f(c['varianza'], 6)}"},
        ])
    return {
        "tipo": "animado",
        "titulo": "ACF en los rezagos 1 y 12 de log(AirPassengers) con cada combinación de diferencias",
        "alto": 460,
        "x": {"categorias": [r for _, r in orden]},
        "y": {"titulo": "Autocorrelación muestral", "min": -0.75, "max": 1.3, "marcas": [-0.5, 0, 0.5, 1]},
        "base": [
            {"tipo": "texto", "serie": 1, "x": -0.42, "y": 1.2, "texto": "■ ρ̂ en el rezago 1 (tendencia)", "ancla": "inicio"},
            {"tipo": "texto", "serie": 2, "x": 1.55, "y": 1.2, "texto": "■ ρ̂ en el rezago 12 (estación)", "ancla": "inicio"},
        ],
        "etapas": etapas,
    }


def satelites() -> dict:
    t = J["teoricas"]
    sar, mix = t["sar1_pos"]["acf"], t["ar1_sar1"]["acf"]
    e1 = [{"tipo": "barra", "serie": 1, "x": k, "y": sar[k - 1], "ancho": 0.42, "desplazamiento": -0.22,
           "texto": f(sar[k - 1], 2)} for k in (12, 24, 36)]
    e1.append({"tipo": "texto", "serie": 1, "x": 1, "y": 0.98, "texto": "SAR(1), Φ = 0.7: picos en 12, 24, 36 y nada entre ellos", "ancla": "inicio"})
    e2 = [{"tipo": "barra", "serie": 2, "x": k, "y": mix[k - 1], "ancho": 0.42, "desplazamiento": 0.22} for k in range(1, 37)]
    e2.append({"tipo": "texto", "serie": 2, "x": 1, "y": 0.89, "texto": "AR(1)×SAR(1), φ = 0.6 y Φ = 0.7: la parte regular llena los rezagos bajos", "ancla": "inicio"})
    e3 = [
        {"tipo": "marca", "x": 11.2, "y": mix[10], "radio": 20, "texto": f"ρ_{{11}} = {f(mix[10], 4)}", "lado": "izquierda"},
        {"tipo": "marca", "x": 13.2, "y": mix[12], "radio": 20, "texto": f"ρ_{{13}} = {f(mix[12], 4)}", "lado": "derecha"},
        {"tipo": "texto", "serie": 6, "x": 15.5, "y": 0.6, "texto": f"satélites ≈ ρ_{{1}}·ρ_{{12}} = {f(mix[0], 4)} × {f(mix[11], 4)} = {f(mix[0] * mix[11], 4)}", "ancla": "inicio"},
    ]
    return {
        "tipo": "animado",
        "titulo": "ACF teórica de un SAR(1) y de un AR(1)×SAR(1) con m = 12",
        "alto": 460,
        "x": {"titulo": "Rezago", "min": 0.3, "max": 36.7, "marcas": [1, 12, 24, 36]},
        "y": {"titulo": "ACF teórica", "min": 0, "max": 1.02, "marcas": [0, 0.2, 0.4, 0.6, 0.8]},
        "etapas": [e1, e2, e3],
    }


def escalones() -> dict:
    p = J["airpassengers"]["pronostico"]
    psi, sig = p["psi"], p["sigma_h"]

    def barras(js, serie=1, texto_en=None):
        out = []
        for j in js:
            b = {"tipo": "barra", "serie": serie, "panel": 0, "x": j, "y": psi[j], "ancho": 0.62}
            if j == texto_en:
                b["texto"] = f(psi[j], 4)
            out.append(b)
        return out

    def linea(hs):
        return {"tipo": "linea", "serie": 2, "panel": 1, "x": hs, "y": [sig[h - 1] for h in hs], "radio": 5}

    def rotulo(h, dx, dy):
        return {"tipo": "texto", "serie": 2, "panel": 1, "x": h + dx, "y": sig[h - 1] + dy,
                "texto": f"σ_{{{h}}} = {f(sig[h - 1], 4)}", "ancla": "inicio"}

    e1 = barras(range(0, 12), texto_en=6) + [linea(list(range(1, 13))), rotulo(1, 0.8, -0.012), rotulo(12, 0.6, -0.016)]
    e2 = barras([12], serie=6, texto_en=12) + [linea([12, 13])]
    e3 = barras(range(13, 24), texto_en=18) + [linea(list(range(13, 25))), rotulo(24, -9.5, 0.008)]
    return {
        "tipo": "animado",
        "titulo": "Pesos psi del modelo airline y desviación del error de pronóstico",
        "alto": 460,
        "separacion": 120,
        "paneles": [
            {"titulo": "Pesos ψ_{j}", "x": {"titulo": "j", "min": -0.7, "max": 23.7, "marcas": [0, 6, 12, 18, 23]},
             "y": {"min": 0, "max": 1.2, "marcas": [0, 0.5, 1]}},
            {"titulo": "σ_{h} (en unidades de log y)", "x": {"titulo": "h (meses)", "min": 0.3, "max": 24.7, "marcas": [1, 6, 12, 18, 24]},
             "y": {"min": 0, "max": 0.17, "marcas": [0, 0.05, 0.1, 0.15]}},
        ],
        "etapas": [e1, e2, e3],
    }


def construye() -> dict[str, dict]:
    return {"diferencias.json": diferencias(), "satelites.json": satelites(), "escalones.json": escalones()}


def texto(d: dict) -> str:
    return json.dumps(d, ensure_ascii=False, indent=1) + "\n"


if __name__ == "__main__":
    DESTINO.mkdir(parents=True, exist_ok=True)
    for nombre, d in construye().items():
        (DESTINO / nombre).write_text(texto(d), encoding="utf-8")
        print("escrito:", (DESTINO / nombre).relative_to(RAIZ))
