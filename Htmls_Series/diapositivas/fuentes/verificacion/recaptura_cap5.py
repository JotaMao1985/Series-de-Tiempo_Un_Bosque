#!/usr/bin/env python3
"""Vuelve a fotografiar cuatro gráficas de los simuladores del capítulo 5, con ajustes de lectura.

Las fotos m1-1, m6-1, m7-1 y m11-1 salieron de `extraer.py` tal como el simulador las pinta al cargar.
Proyectadas, tenían estos defectos (auditoría del 2026-10-28, `auditoria_cap5.md`, G1–G3 y sección 2):

    m1-1  ACF de log(AirPassengers): eje y de −1 a 1 (media gráfica vacía) y los rezagos
          12, 24 y 36, que son el mensaje de la diapositiva, del mismo color que el resto
    m6-1  ACF de los residuales del airline: el mismo eje de −1 a 1, que deja las barras diminutas
    m7-1  pronóstico del airline: la leyenda trae dos cuadros sin rótulo (los bordes de las bandas)
    m11-1 pronósticos de cinco métodos: la leyenda escribe el airline como (0,1,1)(0,1,1)[12], a la
          manera de R, y el resto del deck usa el subíndice ₁₂

Este guion sirve el capítulo por HTTP, abre cada módulo con `loadModule(k)`, toma el gráfico de
Chart.js del simulador y SOLO cambia la presentación (rango del eje y, color de tres barras,
filtro y rótulos de la leyenda); los datos son los que el simulador calcula. Luego guarda el lienzo como PNG.

Uso (desde la raíz del repositorio):
    python3 Htmls_Series/diapositivas/fuentes/verificacion/recaptura_cap5.py
    python3 Htmls_Series/diapositivas/fuentes/verificacion/recaptura_cap5.py --inspeccionar
"""
from __future__ import annotations

import base64
import html
import json
import re
import sys
import tempfile
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[3]
CAPITULO = RAIZ / "Htmls_Series/capitulo-5-sarima.html"
DESTINO = AQUI.parent / "recursos" / "cap5"
sys.path.insert(0, str(Path.home() / ".claude/skills/diapositivas-clase/scripts"))
import revisar  # noqa: E402  (lanza Chrome sin ventana; es de la skill diapositivas-clase)

# Cada ajuste recibe el gráfico `ch` de Chart.js y solo toca su presentación.
AJUSTES = {
    "m1-1.png": (1, """
        ch.options.scales.y.min = -0.2; ch.options.scales.y.max = 1;
        ch.data.datasets.forEach(d => {
          if (d.type === 'bar' || ch.config.type === 'bar' && !d.type) {
            const base = Array.isArray(d.backgroundColor) ? d.backgroundColor[0] : d.backgroundColor;
            d.backgroundColor = ch.data.labels.map(l => [12, 24, 36].includes(Number(l)) ? '#FF6600' : base);
          }
        });"""),
    "m6-1.png": (6, "ch.options.scales.y.min = -0.3; ch.options.scales.y.max = 0.3;"),
    "m7-1.png": (7, "ch.options.plugins.legend.labels.filter = (it) => !!(it.text && it.text.trim());"),
    "m11-1.png": (11, "ch.data.datasets.forEach(d => { if (d.label) d.label = d.label.replace('[12]', '₁₂'); });"),
}

PAGINA = """<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0">
<iframe id="f" style="width:1180px;height:900px;border:0"></iframe>
<script>
const TAREAS = __TAREAS__, INSPECCIONAR = __INSP__, salida = [];
const esperar = (ms) => new Promise((r) => setTimeout(r, ms));
const f = document.getElementById('f');
f.onload = async () => {
  const w = f.contentWindow;
  await esperar(1500);
  w.Chart.defaults.animation = false;
  for (const [nombre, k, ajuste] of TAREAS) {
    w.loadModule(k);
    await esperar(1500);
    const c = w.document.getElementById('content-area').querySelector('.simulador canvas');
    const ch = w.Chart.getChart(c);
    const info = {nombre, tipo: ch.config.type, etiquetas: ch.data.labels.slice(0, 40),
                  datasets: ch.data.datasets.map(d => ({label: d.label, type: d.type || '', n: d.data.length,
                                                       color: String(d.backgroundColor).slice(0, 60)})),
                  y: [ch.options.scales.y.min, ch.options.scales.y.max]};
    if (!INSPECCIONAR) { (new Function('ch', ajuste))(ch); ch.update('none'); await esperar(300); }
    salida.push({...info, url: c.toDataURL('image/png'), ancho: c.width, alto: c.height});
  }
  const pre = document.createElement('pre'); pre.id = 'salida'; pre.textContent = JSON.stringify(salida);
  document.body.appendChild(pre);
};
f.src = '__CAPITULO__#modulo-1';
</script></body></html>"""


def main() -> int:
    inspeccionar = "--inspeccionar" in sys.argv
    tareas = [[n, k, a] for n, (k, a) in AJUSTES.items()]
    pagina = (PAGINA.replace("__TAREAS__", json.dumps(tareas)).replace("__INSP__", "true" if inspeccionar else "false")
              .replace("__CAPITULO__", CAPITULO.name)).encode()

    class Manejador(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path.startswith("/__recaptura__"):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(pagina)
                return
            super().do_GET()

        def log_message(self, *a):
            pass

    srv = ThreadingHTTPServer(("127.0.0.1", 0), partial(Manejador, directory=str(CAPITULO.parent)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        with tempfile.TemporaryDirectory() as perfil:
            dom = revisar.correr(["--force-device-scale-factor=2", "--window-size=1200,950", "--virtual-time-budget=15000",
                                  "--dump-dom", f"http://127.0.0.1:{srv.server_address[1]}/__recaptura__.html"], perfil, timeout=120)
    finally:
        srv.shutdown()
    m = re.search(r'<pre id="salida">(.*?)</pre>', dom, re.S)
    if not m:
        print("ERROR: la página no devolvió capturas")
        return 1
    for c in json.loads(html.unescape(m.group(1))):
        url = c.pop("url")
        print(json.dumps(c, ensure_ascii=False))
        if not inspeccionar:
            (DESTINO / c["nombre"]).write_bytes(base64.b64decode(url.split(",", 1)[1]))
            print("escrito:", (DESTINO / c["nombre"]).relative_to(RAIZ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
