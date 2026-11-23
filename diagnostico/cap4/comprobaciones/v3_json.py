"""V3 · compara la rejilla del explorador (DATOS_CAP4 en la página, de genera_cap4.R) con mi propia rejilla de v3_cifras.R."""
import json, re, sys, csv, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from v3_modulos import lee, HTML
h = lee(HTML)
m = re.search(r"const DATOS_CAP4 = (\{.*?\});\n", h, re.S)
D = json.loads(m.group(1))
nilo = D["nilo"]
print("claves nilo:", list(nilo.keys()))
rej = nilo.get("rejilla") or nilo.get("modelos")
print("tipo rejilla:", type(rej).__name__, len(rej))
fila0 = rej[0] if isinstance(rej, list) else list(rej.values())[0]
print("campos de una fila:", list(fila0.keys()))
mine = {(int(r["p"]), int(r["d"]), int(r["q"])): r for r in csv.DictReader(open(sys.argv[1]))}
mal = 0
for f in (rej if isinstance(rej, list) else rej.values()):
    k = (f["p"], f["d"], f["q"])
    r = mine.get(k)
    if r is None or r["aicc"] in ("NA", ""):
        print("   sin ajuste propio:", k, f.get("aicc")); continue
    da = abs(float(r["aicc"]) - f["aicc"]) if f.get("aicc") is not None else 9
    lbk = [x for x in f if x.startswith("lb") or "ljung" in x.lower()]
    lbv = f[lbk[0]] if lbk else None
    dl = abs(float(r["lb"]) - lbv) if lbv is not None and r["lb"] != "NA" else None
    flag = "" if da < 0.01 and (dl is None or dl < 0.005) else "  <-- DIFIERE"
    if flag: mal += 1
    print(f"   {k} aicc json {f['aicc']:.3f} mío {float(r['aicc']):.3f} | lb json {lbv} mío {float(r['lb']):.4f}{flag}")
print("modelos que difieren:", mal)
