import sys, subprocess, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent)); sys.path.insert(0, "precalculo")
import r4_entradas as entradas
import audita_citas as a
B = pathlib.Path("bibliografia/_local"); mal = 0; n = 0
for e in entradas.E:
    for f in e["fuentes"]:
        n += 1
        if f["clase"] == "PDF":
            arch = B/"texto"/f["clave"]/f"p{f['pagina_pdf']:04d}.txt"
            texto = arch.read_text("utf-8")
        else:
            arch = B/"web"/f["clave"]/f"{f['instantanea']}.txt"
            texto, falta = a.seccion_de(arch.read_text("utf-8"), f["loc"])
            if falta: print("SIN SECCIÓN", e["id"], f["loc"]); mal += 1; continue
        g = subprocess.run(["grep", "-c", "-F", "--", f["cita"], str(arch)], capture_output=True, text=True).stdout.strip()
        ok = a.normaliza(f["cita"]) in a.normaliza(texto)
        pal = len(f["cita"].split())
        if not ok or g == "0" or pal > 25:
            mal += 1
        print(f"{'OK ' if ok else 'NO '} grep={g} pal={pal:2d} {e['id']} {f['clave'][:10]} {f['loc']:22s} {f['cita'][:60]}")
print(n, "citas;", mal, "con problema")
