"""V3: primera aparicion de terminos en el HTML ensamblado del cap. 5 (plantillas en orden, texto y codigo aparte)."""
import re, html, sys
src = open(sys.argv[1] if len(sys.argv) > 1 else "Htmls_Series/capitulo-5-sarima.html", encoding="utf-8").read()
tpls = re.findall(r'<template id="module-(\d+)">(.*?)</template>', src, re.S)
terms = {"ETS": r"\bETS\b", "naïve estacional": r"[Nn]a[iï]ve estacional", "RMSE": r"\bRMSE\b", "MAE": r"\bMAE\b",
         "MAPE": r"\bMAPE\b", "fuera de muestra": r"fuera de muestra", "biasadj": r"biasadj",
         "theta-hat -0.4018": r"-0\.4018", "Theta-hat -0.5569": r"-0\.5569", "airline (palabra)": r"airline",
         "sigma2 0.001371": r"0\.001371", "Holt": r"\bHolt\b", "eta_t": r"\\eta_t", "n_t": r"\bn_t\b",
         "r_k": r"\br_k\b", "2/\\sqrt{n}": r"\\pm 2/\\sqrt", "rejilla": r"rejilla"}
for nombre, pat in terms.items():
    hits = []
    for num, body in tpls:
        code = "".join(re.findall(r"<pre>.*?</pre>", body, re.S))
        prose = re.sub(r"<pre>.*?</pre>", " ", body, flags=re.S)
        prose = re.sub(r"<!--.*?-->", " ", prose, flags=re.S)
        prose_txt = html.unescape(re.sub(r"<[^>]+>", " ", prose))
        np_, nc = len(re.findall(pat, prose_txt)), len(re.findall(pat, html.unescape(code)))
        if np_ or nc: hits.append(f"M{num}: prosa {np_}, codigo {nc}")
    print(f"{nombre:22s} -> " + ("; ".join(hits) if hits else "ninguna"))
# primera frase en prosa con cada uno de los terminos del M11/M9
for nombre in ["ETS", "naïve estacional", "RMSE", "MAE", "MAPE", "fuera de muestra", "biasadj"]:
    for num, body in tpls:
        prose = re.sub(r"<pre>.*?</pre>", " ", body, flags=re.S)
        prose = re.sub(r"<!--.*?-->", " ", prose, flags=re.S)
        t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", prose)))
        m = re.search(terms[nombre], t)
        if m:
            print(f"\n[{nombre}] primera en M{num}: …{t[max(0, m.start()-160):m.end()+160]}…"); break
