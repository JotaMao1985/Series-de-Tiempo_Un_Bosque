#!/usr/bin/env python3
"""Lector-estudiante (cap. 5) · «dicho pero no mostrado»: cifras de la prosa que ningun bloque de codigo produce.

Uso:  python3 -I lector_cifras.py ruta/capitulo-5-sarima.html

Mismo metodo que `diagnostico/cap4/diag/lector_cifras.py`. Para cada cifra citada en la prosa (lista a mano, leida del
marcado de los doce modulos) se busca su cadena en (a) los bloques <pre> del MISMO modulo, (b) los <pre> de CUALQUIER
otro modulo, y (c) el JSON de precalculos (`const DATOS_CAP5`), que alimenta los simuladores. Una cifra que solo vive
en el JSON se ve moviendo un simulador (si el simulador la pinta) pero no se reproduce con el codigo que el estudiante
ejecuta. La busqueda es por prefijo numerico (ver `esta`): «sin codigo» significa que el
literal no esta impreso en ninguna salida `#>` ni en ningun comentario de ningun bloque; una cifra que el codigo calcula
y no imprime tambien sale «sin codigo», por eso cada una se revisa a ojo despues (columna de notas).
Cuando la prosa redondea una salida (0.0370 frente a 0.037031) se da como cadena alternativa la salida completa.
"""
import html
import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
mods = {int(m.group(1)): m.group(2) for m in re.finditer(r'<template id="module-(\d+)">(.*?)</template>', src, re.S)}


def esta(c, texto):
    """Casa por PREFIJO numerico (la prosa redondea: 486.538 casa con 486.5380), sin digitos ni punto pegados antes
    (0.231 no casa con 10.2311). Puede dar algun falso «si» cuando la cadena es corta; cada «no» se revisa a ojo."""
    return re.search(r"(?<![\d.])" + re.escape(c) + r"\d*", texto) is not None


def pres(h):
    return html.unescape(" ".join(re.findall(r"<pre\b.*?</pre>", h, flags=re.S)))


code = {k: pres(h) for k, h in mods.items()}
jm = re.search(r"const DATOS_CAP5 = (\{.*?\});\n", src, re.S)
datos = jm.group(1) if jm else ""

CLAIMS = [
    # M1
    (1, "tabla: USAccDeaths rho1 0.707, rho12 0.629, rho24 0.450, rho36 0.302", ["0.707", "0.629", "0.450", "0.302"]),
    (1, "tabla: co2 rho12 0.928, rho24 0.855, rho36 0.783", ["0.928", "0.855", "0.783"]),
    (1, "tabla: TRM niveles rho12 0.636, rho24 0.490, rho36 0.225", ["0.636", "0.490", "0.225"]),
    (1, "tabla: dTRM rho1 0.088 y rho12 -0.002 (el bloque imprime -0.0024; las tablas -0.0025)", ["0.088", "-0.0025"]),
    (1, "ARIMA(0,1,5): rho12 0.7245, rho24 0.6727 (sale del cap. 4)", ["0.7245", "0.6727"]),
    # M2
    (2, "theta12 = 0.5 y Theta = 0.6: varianza 2.300 frente a 1.700 (factorizada)", ["2.300", "1.700"]),
    (2, "airline: gamma0 = 1.5217 sigma^2", ["1.5217"]),
    (2, "airline: gamma0 = 0.002087 y varianza muestral 0.002102 (131 obs.)", ["0.002087", "0.002102"]),
    (2, "tabla phi = 0.6/0.8/0.95: exacta 3.073/5.997/44.580 y factorizada 3.064/5.447/20.111", ["3.073", "5.997", "44.580", "3.064", "5.447", "20.111"]),
    (2, "tabla phi = 0.9: exacta 15.406, factorizada 10.320, psi12 0.98243", ["15.406", "10.320", "0.98243"]),
    # M3
    (3, "log(AP): crecimiento anual medio 0.032 (1958) y 0.201 (1951)", ["0.032", "0.201"]),
    (3, "nsdiffs «seas» = 1 y «ocsb» = 0 sobre log(AP) y USAccDeaths (prosa M3 4205)", ["ocsb"]),
    (3, "la varianza se divide entre 17 y 51 (cociente de dos varianzas de la tabla)", ["0.194884", "0.011354", "0.003800"]),
    (3, "KPSS Python 0.8672 y 0.0713; valor critico 0.463", ["0.8672", "0.0713", "0.463"]),
    (3, "lynx del cap. 4: la varianza baja 58 %", ["58"]),
    # M4
    (4, "SAR(1) Phi 0.7: rho36 = 0.343", ["0.343"]),
    (4, "SMA(1) Theta -0.6: rho12 = -0.4412 (la tabla dice -0.441)", ["0.4412", "0.441"]),
    (4, "fila AR(1)xSMA(1): rho11 -0.234, rho12 -0.470, rho13 -0.235", ["0.234", "0.470", "0.235"]),
    (4, "airline: rho11 = rho13 = 0.14705 «iguales a precision de maquina»", ["0.14705", "0.1470662"]),
    (4, "AR(1)xSAR(1): rho11 = 0.42298 y rho13 = 0.42180", ["0.42298", "0.42180", "0.4230", "0.4218"]),
    # M5
    (5, "psi12 = 1.0412 y psi13..23 = 0.8632 (el bloque del M7 da 1.0413 y 0.8633)", ["1.0412", "0.8632"]),
    (5, "sigma1 = 0.0370, sigma12 = 0.0823, sigma24 = 0.1396", ["0.037031", "0.082273", "0.139634"]),
    (5, "sigma12/sigma1 = 2.22 frente a 3.46", ["2.22"]),
    (5, "USAccDeaths: airline -0.4303 y -0.5528", ["-0.4303", "-0.5528", "0.4303", "0.5528"]),
    (5, "psi_inf = 0.169 del Nilo (cap. 4)", ["0.169"]),
    # M6
    (6, "fila (0,1,0)(0,1,0): AICc -434.80, LB < 1e-4", ["434.80", "434.8"]),
    (6, "las cuatro primeras filas: -483.2101, -481.7923, -481.5957, -481.5820", ["483.2101", "481.7923", "481.5957", "481.5820"]),
    (6, "Python: simple_differencing=False nobs 144 ma1 -0.4019", ["0.4019"]),
    (6, "USAccDeaths en Python: theta pasa de -0.4303 a -0.3924", ["0.3924"]),
    # M7
    (7, "rango relativo de AirPassengers = 1.848", ["1.848"]),
    (7, "ACF de la serie diferenciada: lag 3 -0.202, 9 0.176, 23 0.223", ["0.202", "0.176", "0.223"]),
    (7, "residuales: lag 3 -0.125, 9 0.117, 23 0.220", ["0.125", "0.117", "0.220"]),
    (7, "t = -4.48 y -7.62", ["4.48", "7.62"]),
    (7, "|Theta|^(1/12) con Theta = 0.1 vale 0.825", ["0.825"]),
    (7, "satelites 11 y 13 muestrales: 0.064 y 0.152", ["0.0644", "0.1516", "0.064", "0.152"]),
    (7, "pronostico 24 meses: 525.46, 399.66, 690.85", ["525.46", "399.66", "690.85"]),
    (7, "ARIMA(0,1,5): Q = 222.4", ["222.4"]),
    # M8
    (8, "tabla de pruebas: filas co2 (1,1,1,1) y AP/USAcc ocsb = 0", ["ocsb"]),
    (8, "USAccDeaths: AICc 857.32, LB 0.2477", ["857.32", "0.2477", "857.316"]),
    (8, "SE 1.4 y 2.4 veces mayores (0.1228/0.0896 y 0.1784/0.0731)", ["0.1228", "0.1784", "0.0896", "0.0731"]),
    (8, "TRM n = 138 y banda 0.1675", ["138", "0.1675"]),
    (8, "TRM: Phi 0.0013, e.e. 0.0899, t 0.01 (el bloque da 0.0147)", ["0.0013", "0.0899", "0.0147"]),
    (8, "TRM: AICc 1708.00 frente a 1705.94", ["1708.001", "1705.941"]),
    # M9
    (9, "Pascua: 2 veces en marzo y 10 en abril en los 12 anios", ["meses_pascua_marzo"]),
    (9, "AICc -486.54 y -490.72; mejora de 7.5 puntos", ["486.538", "490.7221"]),
    (9, "BIC -475.35 y -476.83", ["475.35", "476.83", "475.3547"]),
    (9, "beta log(dias) 1.1157 (t = 2.39) en el modelo con solo los dias", ["1.1157"]),
    (9, "beta = 1.084, e.e. 0.4462, t = 0.19 contra beta = 1", ["1.084", "0.4462", "0.1882"]),
    (9, "RMSE 45.48 frente a 43.18 (comparacion del M11)", ["45.48", "43.18"]),
    # M10
    (10, "tabla de K = 1..6 (AICc -359.18 ... -521.45; LB)", ["359.18", "521.22", "521.45"]),
    (10, "STL en R: AIC -542.95 (el bloque imprime solo el orden); Python -643.05", ["542.95", "643.05"]),
    (10, "ARIMA(0,0,0)(0,1,0)[365] sobre una serie simulada", ["0,1,0)[365]"]),
    # M11
    (11, "tabla 8 metodos: RMSE 19.43, 19.51, 35.48, 43.18, 72.55, 76.99", ["19.43", "19.505", "35.48", "43.18", "72.55", "76.99"]),
    (11, "tabla 61 origenes: RMSE medio 16.81, 21.42, 21.85, 22.38, 26.38, 41.24", ["16.81", "21.42", "21.85", "22.38", "26.38", "41.24", "16.812"]),
    (11, "% de origenes en que le gana al SARIMA: 8.2, 8.2, 9.8, 14.8, 11.5", ["8.2", "9.8", "14.8", "11.5"]),
    (11, "total anual +3.4 % en 1958 frente a 6.2-21.8 % en los demas", ["3.4", "6.2", "21.8"]),
    (11, "pronostico del airline +4.7 % y +6.9 %; observado 12.4 y 11.2; ETS log 9.4/12.8; armonica 10.6/13.1", ["4.7", "6.9", "12.4", "11.2", "9.4", "12.8", "10.6", "13.1"]),
    (11, "14 origenes en que no es el mejor, 12 entre 1957-05 y 1959-01", ["1957-05", "1959-01"]),
    (11, "24 meses: 49 origenes, 26.00 / 26.61 / 27.80 / 28.30; 49.0 %; mes 12: 18.22 vs 15.96", ["26.00", "26.61", "27.80", "28.30", "49.0", "18.22", "15.96"]),
    (11, "sesgo medio 39.45 = MAE", ["39.45"]),
    (11, "k = 16, 17, 2 + 11 (parametros por metodo)", ["16", "17"]),
    (11, "ejercicio 1 (co2): 223.9877, 1.4555, 0.3882, 0.1543; 988.100 y 178.209", ["223.9877", "1.4555", "0.3882", "0.1543", "988.100", "178.209"]),
    (11, "ejercicio 3: LB del airline sobre co2 p = 0.4081", ["0.4081"]),
    (11, "ejercicio 1: AICc 176.9982 y airline 178.2089 (escrito a mano en el bloque)", ["176.9982", "178.2089"]),
]

print("mod | cifra citada en la prosa | en codigo del mismo modulo | en codigo de otro modulo | en el JSON de precalculos")
sin = solo_json = 0
filas = []
for k, desc, cads in CLAIMS:
    mismo = [c for c in cads if esta(c, code.get(k, ""))]
    otro = sorted({j for j in code if j != k and any(esta(c, code[j]) for c in cads)})
    enjson = any(esta(c, datos) for c in cads)
    marca = ""
    todas_mismo = len(mismo) == len(cads)
    if not mismo and not otro:
        sin += 1
        marca = " <- SIN CODIGO" + (" (esta en el JSON de precalculos)" if enjson else " (ni en el JSON)")
        if enjson:
            solo_json += 1
    elif not todas_mismo and not mismo:
        marca = " <- solo en otro modulo"
    elif not todas_mismo:
        marca = f" <- parcial: en el modulo solo {mismo}"
    print(f"M{k:<2}| {desc} | {'si' if mismo else 'no'} | {','.join('M' + str(j) for j in otro) or '—'} | "
          f"{'si' if enjson else 'no'}{marca}")
    filas.append((k, bool(mismo or otro)))
print()
print(f"Cifras (grupos) revisadas: {len(CLAIMS)}; sin codigo en ningun modulo: {sin} (de ellas {solo_json} estan en el JSON de precalculos).")
for k in sorted(mods):
    tot = [f for f in filas if f[0] == k]
    if tot:
        print(f"  M{k}: {sum(1 for f in tot if not f[1])} sin codigo de {len(tot)}")
