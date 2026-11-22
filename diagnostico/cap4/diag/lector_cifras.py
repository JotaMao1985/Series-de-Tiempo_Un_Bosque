#!/usr/bin/env python3
"""Lector-estudiante · «dicho pero no mostrado»: cifras de la prosa que ningun bloque de codigo produce.

Uso:  python3 -I lector_cifras.py ruta/capitulo-4-modelos-arima.html

Para cada cifra citada en la prosa de un modulo (lista a mano, leida del marcado) busca su cadena en
(a) los bloques <pre> del MISMO modulo, (b) los <pre> de CUALQUIER otro modulo del capitulo, y (c) en el
JSON de precalculos (const DATOS_CAP4 / NILO / TRM / PUENTE, que alimenta los simuladores). Una cifra
que solo vive en el JSON se ve moviendo un simulador, pero no se puede reproducir con el codigo
que el estudiante ejecuta (y puede ni mostrarse en ellos: el JSON guarda mas de lo que los simuladores
pintan). La busqueda es por ficha numerica (sin digitos pegados antes ni despues) y por cadena: «sin codigo» significa que el literal no aparece
impreso en ninguna salida #> ni en ningun comentario del bloque; una cifra que el codigo calcula pero no
imprime tambien sale como «sin codigo» (por eso cada una se revisa a ojo despues).
"""
import html
import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
mods = {int(m.group(1)): m.group(2) for m in re.finditer(r'<template id="module-(\d+)">(.*?)</template>', src, re.S)}


def esta(c, texto):
    """True si la cadena c aparece en texto sin digitos pegados (0.231 no casa con 10.2311)."""
    return re.search(r"(?<![\d])" + re.escape(c) + r"(?!\d)", texto) is not None


def pres(h):
    return html.unescape(" ".join(re.findall(r"<pre\b.*?</pre>", h, flags=re.S)))


code = {k: pres(h) for k, h in mods.items()}
# precalculos: el bloque <script> con las constantes de datos
json_m = re.search(r"const DATOS_CAP4 = (\{.*?\});\n", src, re.S)
datos = json_m.group(1) if json_m else ""

# (modulo, descripcion, [cadenas alternativas que cuentan como «aparece»])
CLAIMS = [
    (1, "razon 1.006 (R)", ["1.006"]),
    (1, "razon 32.8 sin MA", ["32.8"]),
    (1, "los coeficientes 0.2544 / -0.8741 como estimados (e.e.)", ["0.1194", "0.0605"]),
    (3, "PP: Z(t_alpha) = -6.690", ["6.690", "6.69"]),
    (3, "ndiffs-ADF: tau_mu = -4.05", ["4.05"]),
    (3, "valor critico -2.89", ["2.89"]),
    (3, "PP.test rechaza en el 100 % de 1000 replicas con raiz unitaria verdadera (se llama a PP.test)", ["PP.test"]),
    (3, "ndiffs pide diferenciar en el 100 % de las replicas con escalon", ["ndiffs(x", "ndiffs(1000"]),
    (3, "adf.test (k=4) rechaza 51.3 %", ["51.3", "0.513"]),
    (3, "con escalon, adf.test NO rechaza 86.4 %", ["86.4", "0.864"]),
    (3, "sin escalon adf.test no rechaza 5.4 %", ["5.4 %", "0.054"]),
    (3, "ndiffs-ADF se deja enganar en 0.5 %", ["0.5 %", "0.005"]),
    (3, "KPSS sin escalon 4.8 % (1000 reps)", ["0.048", "4.8"]),
    (3, "KPSS con |beta| = 100: 70.8 %", ["70.8", "0.708"]),
    (3, "KPSS l = 12 con |beta| = 100: 44.5 %", ["44.5", "0.445"]),
    (3, "estadistico medio 1.07 y 1.23 (|beta| = 200 y 300)", ["1.07", "1.23"]),
    (3, "sigma-hat = 127.0 (residuales del modelo de dos medias)", ["127.03", "127.0"]),
    (4, "rezago 8 de la ACF: 0.231", ["0.231"]),
    (4, "ACF del nivel 0.498 0.385 0.328 0.239", ["0.3846", "0.385"]),
    (4, "sigma2 = 20 599.87 del MA(1)", ["20599", "20 599"]),
    (5, "phi-hat = 0.271 del modelo con deriva", ["0.271"]),
    (5, "TRM: deriva 8.00, e.e. 10.36, t = 0.77", ["10.36"]),
    (5, "media de las diferencias -3.84 (aritmetica en la prosa)", ["3.84"]),
    (6, "'cuatro modelos a menos de 2 puntos' en d=1 (explorador)", ["1269.22"]),
    (7, "podio de siete modelos (1268.210, 1268.969, 1269.322, 1269.348)", ["1268.210", "1268.969", "1269.322", "1269.348"]),
    (8, "Shapiro p = 0.731 del ARIMA(1,1,1) del Nilo", ["0.731"]),
    (8, "sigma2 del MA(1) sobre d=2: 28 268.34 y d=3: 80 055.05", ["28268.34", "80055.05"]),
    (8, "log(lynx): 1.653 -> 0.687 (cuenta como ejercicio 2)", ["1.6532", "0.6871"]),
    (8, "medias 1097.75 y 849.97", ["1097.75", "849.97"]),
    (8, "AICc del escalon 1257.91", ["1257.91"]),
    (8, "MAE de la tabla fuera de muestra (101.95, 106.16, 106.99...)", ["101.95", "106.16", "106.99"]),
    (8, "RMSE de la tabla fuera de muestra (123.06 ... 133.31)", ["123.06", "133.31"]),
    (9, "media 920.56 a h = 30 del ARIMA(1,0,1)", ["920.56"]),
    (9, "anchos del 95 %: 561 -> 677, 557 -> 781, 555 -> 708", ["677", "781", "708"]),
    (9, "ancho del ARIMA(1,2,1): 613 -> 2771", ["2771.45", "2771"]),
    (9, "phi-hat = -0.39 del ARIMA(1,2,1)", ["0.39"]),
    (9, "sigma_30 = 199.4 frente a 778.0 de la caminata", ["778.0", "778.0"]),
    (9, "psi_inf = 0.169 (Nilo)", ["0.169"]),
    (9, "cobertura del 80 % a un mes en la TRM: 83.9 %", ["83.9"]),
    (10, "el pronostico 842.17 'a los pocos anios' (Nilo, sin constante)", ["842.17"]),
    (10, "semianchos +-278 (h=1) y +-391 (h=30)", ["278", "391"]),
    (10, "pronostico 816.18 para 1971", ["816.18"]),
    (10, "TRM: 192 modelos de auto.arima con la parte estacional", ["192"]),
    (10, "AirPassengers: rho12 = 0.7245, rho24 = 0.6727, banda 0.1633", ["0.7245", "0.6727", "0.1633"]),
    (10, "AirPassengers: Q_LB(24) = 222.4", ["222.4"]),
    (10, "AirPassengers: mejor no estacional ARIMA(0,1,5); busqueda amplia ARIMA(8,1,3) con rho12 = 0.437", ["0,1,5", "8,1,3", "0.437"]),
    (10, "airline: rho12 = -0.0515, LB(24) p = 0.233", ["0.0515", "0.233"]),
    (10, "143 y 131 observaciones (no estacional vs airline)", ["143", "131"]),
    (10, "TRM: ADF -1.978 / KPSS 2.243 / curtosis 5.1 y 2.8", ["1.978", "2.243", "5.1"]),
    (10, "TRM: Ljung-Box(20) p = 0.189, Shapiro 0.0006", ["0.189", "0.0006"]),
]

print("mod | cifra citada en la prosa | en codigo del mismo modulo | en codigo de otro modulo | en el JSON de precalculos")
sin = 0
solo_json = 0
for k, desc, cads in CLAIMS:
    mismo = any(esta(c, code.get(k, "")) for c in cads)
    otro = [j for j in code if j != k and any(esta(c, code[j]) for c in cads)]
    enjson = any(esta(c, datos) for c in cads)
    marca = ""
    if not mismo and not otro:
        sin += 1
        marca = " <- SIN CODIGO" + (" (esta en el JSON de precalculos; no necesariamente se pinta en un simulador)" if enjson else " (ni en el JSON)")
        if enjson:
            solo_json += 1
    print(f"M{k:<2}| {desc} | {'si' if mismo else 'no'} | {','.join('M' + str(j) for j in otro) or '—'} | "
          f"{'si' if enjson else 'no'}{marca}")
print()
print(f"Cifras revisadas: {len(CLAIMS)}; sin codigo en ningun modulo: {sin} (de ellas {solo_json} estan en el JSON de precalculos).")
