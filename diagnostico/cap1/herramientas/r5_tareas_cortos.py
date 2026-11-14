#!/usr/bin/env python3
"""R5, segundo encargo · tareas para r3bis_elemento.js: los cinco ejercicios
cortos de módulo (M2, M3, M6, M7, M8), con la pista y la solución abiertas, a
1200 y 375 px. De paso recorre los nueve módulos buscando errores y desbordes.

Uso:
  python3 diagnostico/cap1/herramientas/r5_tareas_cortos.py > /tmp/r5_cortos.json
  OUT=diagnostico/cap1/capturas/r5 node diagnostico/cap1/herramientas/r3bis_elemento.js /tmp/r5_cortos.json
"""
import json

URL = "http://localhost:8731/capitulo-1-componentes-descomposicion.html"

ABRE = r"""
(async () => {
  const antes = { botones: mainContent.querySelectorAll('.exercise .ejercicio-boton').length,
                  ocultos: [...mainContent.querySelectorAll('.exercise .ejercicio-panel')].map(p => p.hidden),
                  preEnunciado: [...mainContent.querySelectorAll('.ejercicio-guiado > .code-block-wrapper pre')].map(p => p.className) };
  mainContent.querySelectorAll('.exercise .ejercicio-boton').forEach(b => b.click());
  await new Promise(r => setTimeout(r, 900));
  const W = %d;
  const fuera = [...mainContent.querySelectorAll('.exercise *')].filter(el => { const r = el.getBoundingClientRect(); if (!r.width || r.right <= W + 1) return false; if (el.closest('.katex')) return false; let p = el.parentElement; while (p && p !== mainContent) { const o = getComputedStyle(p).overflowX; if (o === 'auto' || o === 'scroll' || o === 'hidden') return false; p = p.parentElement; } return true; }).map(el => el.tagName + '.' + String(el.className).slice(0, 30));
  return { modulo: currentModuleId, antes,
           abiertos: [...mainContent.querySelectorAll('.exercise .ejercicio-panel')].map(p => [p.id, !p.hidden]),
           aria: [...mainContent.querySelectorAll('.exercise .ejercicio-boton')].map(b => b.getAttribute('aria-expanded')),
           pre: [...mainContent.querySelectorAll('.exercise pre')].map(p => [p.className.replace(/language-\w+/, '').trim(), p.scrollWidth, p.clientWidth, p.scrollHeight, p.clientHeight]),
           katexErr: mainContent.querySelectorAll('.katex-error').length,
           katex: mainContent.querySelectorAll('.exercise .katex').length,
           docSw: document.documentElement.scrollWidth, W, nFuera: fuera.length, fuera: fuera.slice(0, 10) };
})()
"""

CIERRA = r"""
(async () => {
  mainContent.querySelectorAll('.exercise .ejercicio-boton').forEach(b => b.click());
  await new Promise(r => setTimeout(r, 400));
  return [...mainContent.querySelectorAll('.exercise .ejercicio-panel')].map(p => p.hidden);
})()
"""

TODOS = r"""
(async () => { const out = []; const W = %d;
  for (let n = 1; n <= 9; n++) { loadModule(n); await new Promise(r => setTimeout(r, 1200));
    out.push({ n, ejercicios: mainContent.querySelectorAll('.ejercicio-guiado').length, katexErr: mainContent.querySelectorAll('.katex-error').length,
               canv: mainContent.querySelectorAll('canvas').length, docSw: document.documentElement.scrollWidth,
               idsRepetidos: [...document.querySelectorAll('[id]')].map(e => e.id).filter((x, i, a) => a.indexOf(x) !== i) }); }
  return out; })()
"""


def tarea(ancho):
    pasos = [{"js": TODOS % ancho, "espera": 300}]
    for m in (2, 3, 6, 7, 8):
        pasos += [
            {"js": f"loadModule({m}), new Promise(r => setTimeout(() => r({m}), 1400))"},
            {"sel": ".exercise", "archivo": f"corto-m{m}-cerrado-{ancho}.png"},
            {"js": ABRE % ancho, "espera": 500},
            {"sel": ".exercise", "archivo": f"corto-m{m}-abierto-{ancho}.png"},
            {"js": CIERRA, "espera": 300},
        ]
    return {"url": URL + "#modulo-1", "ancho": ancho, "pasos": pasos}


print(json.dumps([tarea(1200), tarea(375)], ensure_ascii=False, indent=1))
