"""Diagnóstico cap. 5 · ¿están en pantalla, antes del instrumento, las cifras y frases que
responden cada pregunta del quiz y cada ejercicio guiado?

    python3 diagnostico/cap5/diag/ejercicios_en_pantalla.py > diagnostico/cap5/diag/ejercicios_en_pantalla.out

Busca cada marca en los módulos M1-M11 (plantillas), fuera del quiz y de los ejercicios
(líneas < 5895), e informa la línea y el módulo. Las marcas son las cifras de la clave y las
frases de la solución, copiadas del propio instrumento.
"""
import re, pathlib
raiz = pathlib.Path(__file__).resolve().parents[3]
L = (raiz / 'Htmls_Series/capitulo-5-sarima.html').read_text(encoding='utf8').split('\n')
ini = [i + 1 for i, l in enumerate(L) if re.search(r'<template id="module-\d+">', l)]
quiz = next(i + 1 for i, l in enumerate(L) if 'data-quiz="cap5"' in l)
def modulo(n): return max(k for k, a in enumerate(ini, 1) if a <= n)
def busca(etq, patrones, hasta=quiz):
    print(f"\n{etq}")
    for p in patrones:
        hits = [(i + 1) for i, l in enumerate(L[:hasta - 1]) if i + 1 >= ini[0] and re.search(p, l)]
        txt = ', '.join(f"M{modulo(h)} l.{h}" for h in hits[:8]) + (f" (+{len(hits) - 8})" if len(hits) > 8 else '')
        print(f"  {p!r}: {len(hits)} → {txt or '—'}")

print(f"Quiz en la línea {quiz}; se busca en las líneas {ini[0]}–{quiz - 1}")
busca('Q1 (M1) TRM en niveles: ρ12 0.636, ρ1 0.964, ρ36 0.225; ∇TRM −0.0025/−0.067/0.071; «nunca en niveles»',
      [r'0\.636', r'0\.964', r'0\.225', r'-0\.0025|−0\.0025', r'0\.0714|0\.071\b', r'nunca se hace en niveles|en niveles'])
busca('Q2 (M2) SAR(1)×AR(1): rezago 13, 2 parámetros, AR(13)', [r'rezago \$13\$|rezago 13', r'parámetros libres', r'satélite', r'AR\(\$?13'])
busca('Q3 (M2) n efectivo = n − d − Dm', [r'cuesta \$m\$|cuesta \$m\$ observaciones|D\s*\\times\s*m|Dm|d \+ Dm|- 13|− 13', r'131', r'143'])
busca('Q4 (M3) USAccDeaths ndiffs 0 → 1; «Primero D, después d»', [r'ndiffs\(USAccDeaths\)', r'Primero \$D\$, después \$d\$|Primero <strong>\$D\$', r'0\.8672', r'-0\.4303|−0\.4303'])
busca('Q5 (M4) SAR(1) Φ = 0.7: picos 0.70, 0.49, 0.34', [r'0\.49\b', r'0\.343|0\.34\b', r'sube solo \$\\Phi\$', r'decae'])
busca('Q6 (M6/M10) armónica −521.2 vs airline −483.2; 143 y 131', [r'521\.2', r'483\.2', r'0\.1341', r'0\.2330|0\.233\b', r'\$143\$', r'\$131\$'])
busca('Q7 (M9) β̂ 1.0840, e.e. 0.4462, t(β=1) 0.1883', [r'1\.0840|1\.084\b', r'0\.4462', r'0\.1883|0\.188\b', r'2\.4291|2\.43\b'])
busca('Q8 (M11) 43.18, 19.51, 16.81, 22.38, 61 orígenes, 85 %', [r'43\.18', r'19\.51', r'16\.81', r'22\.38', r'\$61\$|61 orígenes', r'85\s*\\?,?\\?%|85 %'])
busca('E1 (co2): d = D = 1; varianzas 223.99, 1.4555, 0.3882, 0.1543; nobs 467 vs 455', [r'co2', r'223\.9|1\.4555|0\.3882|0\.1543', r'\$467\$|\$455\$'])
busca('E2 (USAccDeaths): caminos (a) y (b), airline −0.4303/−0.5528, LB 0.2477, ocsb', [r'ndiffs\(diff\(USAccDeaths', r'0\.2477', r'-0\.5528|−0\.5528', r'ocsb'])
busca('E3(a) (TRM): tres evidencias; Φ 0.0013, t 0.01; AICc 1708.00 / 1705.94', [r'0\.0013', r'1708\.0', r'1705\.94', r'evidencias'])
busca('E3(b) (Fourier en co2): 180.200, 178.209', [r'180\.2', r'178\.2'])
