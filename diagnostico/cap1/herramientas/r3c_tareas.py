#!/usr/bin/env python3
"""R3c · tareas de medida y captura de las correcciones tras la verificación (B1–B7) para r3_elemento.js.
Uso: python3 r3c_tareas.py medidas|capturas|pasada [anchos…] > x.json ; OUT=…/capturas/r3/correcciones node r3_elemento.js x.json"""
import json, sys
U = 'http://localhost:8731/capitulo-1-componentes-descomposicion.html'
SUF = {1200: '1200', 800: '800', 375: '375'}

def abre(panel):
    return {'js': "(() => { const b = document.querySelector('[aria-controls=\"%s\"]'); if (b.getAttribute('aria-expanded') !== 'true') b.click(); return 'abierto ' + b.getAttribute('aria-controls'); })()" % panel,
            'espera': 600}

def radio(sim, i):
    return {'js': "(() => { const r = document.querySelector('[data-simulador=\"%s\"]'); r.querySelectorAll('input[type=radio]')[%d].click();"
                  " return r.querySelector('.simulador-lectura').textContent.replace(/\\s+/g, ' ').trim(); })()" % (sim, i)}

def rezago(k):
    return {'js': "(() => { const r = document.querySelector('[data-simulador=\"grafico-rezagos\"]'); const i = r.querySelector('input[type=range]');"
                  " i.value = %d; i.dispatchEvent(new Event('input', { bubbles: true })); return r.querySelector('.simulador-lectura').textContent.replace(/\\s+/g, ' ').trim(); })()" % k}

# --- medidas ---------------------------------------------------------------
# Fórmulas: anchura del contenido frente a la caja que lo recorta o lo desplaza.
FORMULAS = r"""(() => {
  const r1 = x => Math.round(x * 10) / 10;
  const W = document.documentElement.clientWidth;
  const sel = %s;
  return [...mainContent.querySelectorAll(sel)].map(d => {
    const k = d.querySelector('.katex-html') || d.querySelector('.katex') || d;
    // la caja que se desplaza: el primer ancestro (o el propio elemento) con overflow-x auto o scroll
    let caja = d; while (caja && caja !== mainContent && !/auto|scroll/.test(getComputedStyle(caja).overflowX)) caja = caja.parentElement;
    const tiene = caja && caja !== mainContent;
    const kr = k.getBoundingClientRect(), dr = (tiene ? caja : d).getBoundingClientRect();
    // lo que recorta sin desplazar: un ancestro con overflow hidden por el que el contenido sobresale
    let rec = d.parentElement, cortada = false;
    while (rec && rec !== document.body) { const cs = getComputedStyle(rec); if (/hidden|clip/.test(cs.overflowX) && kr.right > rec.getBoundingClientRect().right + 1 && !(tiene && rec.contains(caja) && rec !== caja)) { cortada = true; break; } rec = rec.parentElement; }
    return { formula: d.textContent.replace(/\s+/g, ' ').slice(0, 34), anchoFormula: r1(k.scrollWidth), cajaQueDesplaza: tiene ? (caja.className || caja.tagName).toString().slice(0, 30) : null,
      cajaCw: tiene ? caja.clientWidth : null, cajaSw: tiene ? caja.scrollWidth : null,
      seDesplaza: tiene ? caja.scrollWidth > caja.clientWidth + 1 : false,
      sobresaleDeLaPagina: kr.right > W + 1 && !tiene, cortadaSinDesplazamiento: !tiene && k.scrollWidth > d.clientWidth + 1,
      sombra: tiene ? getComputedStyle(caja).backgroundAttachment : null };
  });
})()"""

TABLA = r"""(() => {
  const r1 = x => Math.round(x * 10) / 10;
  const t = [...mainContent.querySelectorAll('table')].find(x => /cuatro series/.test(x.caption ? x.caption.textContent : ''));
  let caja = t; while (caja && caja !== mainContent && !/auto|scroll/.test(getComputedStyle(caja).overflowX)) caja = caja.parentElement;
  const tiene = caja && caja !== mainContent;
  const col = t.parentElement.closest('#content-area, .derivacion-panel') || t.parentElement;
  const cr = (tiene ? caja : t).getBoundingClientRect();
  const celdas = [...t.querySelectorAll('th, td')];
  const fuera = celdas.filter(c => c.getBoundingClientRect().right > cr.right + 1).length;
  return { ancho: document.documentElement.clientWidth, columna: t.parentElement.clientWidth, display: getComputedStyle(t).display,
    tablaCw: t.clientWidth, tablaSw: t.scrollWidth, cajaQueDesplaza: tiene ? (caja === t ? 'la propia tabla' : caja.className) : null,
    cajaCw: tiene ? caja.clientWidth : null, cajaSw: tiene ? caja.scrollWidth : null,
    seDesplaza: tiene ? caja.scrollWidth > caja.clientWidth + 1 : false,
    celdasFueraDeLaCaja: fuera + ' de ' + celdas.length,
    cuartaColumna: (() => { const c = t.querySelector('tbody tr td:nth-child(4)').getBoundingClientRect(); return { izq: r1(c.left), der: r1(c.right), limite: r1(cr.right) }; })(),
    sombra: tiene ? getComputedStyle(caja).backgroundAttachment : null,
    otrasTablas: [...mainContent.querySelectorAll('table')].filter(x => x !== t).map(x => ({ cw: x.clientWidth, sw: x.scrollWidth, display: getComputedStyle(x).display })) };
})()"""

REZAGOS = r"""(() => {
  const r1 = x => Math.round(x * 10) / 10;
  const cv = document.querySelector('[data-simulador="grafico-rezagos"] canvas'), ch = Chart.getChart(cv), a = ch.chartArea;
  const x = ch.scales.x, y = ch.scales.y;
  // pendiente en pantalla de la recta y_t = y_{t-k}: 45 grados si el área es cuadrada
  const dx = x.getPixelForValue(x.max) - x.getPixelForValue(x.min), dy = y.getPixelForValue(y.min) - y.getPixelForValue(y.max);
  const w = cv.parentElement.getBoundingClientRect();
  return { ancho: document.documentElement.clientWidth, caja: [r1(w.width), r1(w.height)], lienzo: [cv.clientWidth, cv.clientHeight],
    area: [r1(a.width), r1(a.height)], ejeX: [x.min, x.max], ejeY: [y.min, y.max],
    anguloDiagonal: r1(Math.atan2(dy, dx) * 180 / Math.PI),
    series: ch.data.datasets.map(d => ({ label: d.label, forma: d.pointStyle || 'circle', radio: d.pointRadius, n: d.data.length })),
    leyenda: [...cv.closest('.simulador').querySelectorAll('.grafico-leyenda li')].map(li => li.textContent.trim() + ' [' + li.querySelector('span').className.replace('grafico-leyenda-muestra', '').trim() + ']'),
    aria: cv.getAttribute('aria-label') };
})()"""

STL = r"""(() => {
  const sim = document.querySelector('[data-simulador="descomp-stl"]');
  const ch = Chart.getChart(sim.querySelectorAll('canvas')[2]);
  return { series: ch.data.datasets.map((d, i) => ({ label: d.label, color: d.borderColor, grosor: d.borderWidth, trazo: d.borderDash || null, orden: d.order, visible: ch.isDatasetVisible(i) })),
    leyenda: [...sim.querySelectorAll('.grafico-leyenda li')].map(li => li.textContent.trim() + (li.hidden ? ' (oculta)' : '')),
    lectura: sim.querySelector('.simulador-lectura').textContent.replace(/\s+/g, ' ').trim(),
    aria: sim.querySelectorAll('canvas')[2].getAttribute('aria-label') };
})()"""

ALINEA = r"""(() => {
  const m = sel => [...mainContent.querySelectorAll(sel)].map(p => ({ en: (p.closest('[data-simulador]') || {dataset:{}}).dataset.simulador || sel, ancho: Math.round(p.getBoundingClientRect().width), alineacion: getComputedStyle(p).textAlign }));
  return { ancho: document.documentElement.clientWidth, lecturas: m('.simulador-lectura'), pasos: m('ol.pasos-metodo > li > p').slice(0, 2) };
})()"""

PASADA = ("(() => { const W = document.documentElement.clientWidth; const fuera = [...mainContent.querySelectorAll("
          "'.simulador, .simulador > *, canvas, .mapa-estacional, .grafico-wrapper, fieldset, .grafico-pila, table, .formula, ol.pasos-metodo, .derivacion')]"
          ".filter(el => { const r = el.getBoundingClientRect(); return r.width && r.right > W + 1; }).map(el => el.tagName + '.' + String(el.className).slice(0, 30));"
          " const sinPintar = [...mainContent.querySelectorAll('canvas')].filter(c => !Chart.getChart(c)).length;"
          " return { modulo: currentModuleId, ancho: W, docSw: document.documentElement.scrollWidth, fuera: fuera.slice(0, 5),"
          " katexError: document.querySelectorAll('.katex-error').length, simuladores: mainContent.querySelectorAll('[data-simulador]').length,"
          " lienzos: mainContent.querySelectorAll('canvas').length, lienzosSinGrafico: sinPintar,"
          " lecturasVacias: [...mainContent.querySelectorAll('.simulador-lectura')].filter(p => !p.textContent.trim()).length,"
          " duraciones: courseData.modules.map(m => m.duration).join(' · ') }; })()")

def formulas(sel):
    return {'js': FORMULAS % json.dumps(sel)}

def medidas(anchos):
    t = []
    for a in anchos:
        t.append({'url': U, 'ancho': a, 'modulo': 3, 'pasos': [{'js': REZAGOS}, rezago(12), {'js': REZAGOS}, {'js': ALINEA}]})
        t.append({'url': U, 'ancho': a, 'modulo': 6, 'pasos': [{'js': ALINEA}]})
        t.append({'url': U, 'ancho': a, 'modulo': 7, 'pasos': [
            {'js': ALINEA}, abre('der-robustez'), formulas('#der-robustez .katex-display'),
            {'js': STL}, radio('descomp-stl', 1), {'js': STL}, radio('descomp-stl', 5), {'js': STL}]})
        t.append({'url': U, 'ancho': a, 'modulo': 8, 'pasos': [
            {'js': TABLA}, abre('der-fuerza-ft'), formulas('#der-fuerza-ft .katex-display'), formulas('.formula .katex-display')]})
    return t

def capturas(anchos):
    t = []
    for a in anchos:
        s = SUF[a]
        rez = '[data-simulador="grafico-rezagos"]'
        stl = '[data-simulador="descomp-stl"]'
        t.append({'url': U, 'ancho': a, 'modulo': 3, 'pasos': [
            {'sel': rez, 'archivo': f'B3-B4-rezagos-k1-{s}.png'},
            rezago(6), {'sel': rez, 'archivo': f'B3-B4-rezagos-k6-{s}.png'},
            rezago(12), {'sel': rez, 'archivo': f'B3-B4-rezagos-k12-{s}.png'},
            {'sel': '[data-simulador="subseries-estacionales"] .simulador-lectura', 'archivo': f'B6-lectura-subseries-{s}.png'},
        ]})
        t.append({'url': U, 'ancho': a, 'modulo': 6, 'pasos': [
            {'sel': '[data-simulador="escala-aditiva"] .simulador-lectura', 'archivo': f'B6-lectura-escala-aditiva-{s}.png'},
        ]})
        t.append({'url': U, 'ancho': a, 'modulo': 7, 'pasos': [
            {'sel': 'ol.pasos-metodo', 'archivo': f'B6-pasos-stl-{s}.png'},
            {'sel': stl, 'archivo': f'B5-stl-partida-{s}.png'},
            radio('descomp-stl', 1), {'sel': stl, 'archivo': f'B5-stl-s11-{s}.png'},
            radio('descomp-stl', 5), {'sel': stl, 'archivo': f'B2-B5-stl-s11-robust-{s}.png'},
            radio('descomp-stl', 0), radio('descomp-stl', 3), radio('descomp-stl', 4), {'sel': stl, 'archivo': f'B5-stl-atipico-norob-{s}.png'},
            {'sel': '[data-simulador="loess-local"] .simulador-lectura', 'archivo': f'B6-lectura-loess-{s}.png'},
            abre('der-robustez'), {'sel': '#der-robustez .formula', 'archivo': f'B7-m7-bicuadrada-{s}.png'},
            {'js': "(() => { const f = document.querySelector('#der-robustez .formula'); f.scrollLeft = f.scrollWidth; return [f.scrollLeft, f.scrollWidth, f.clientWidth]; })()"},
            {'sel': '#der-robustez .formula', 'archivo': f'B7-m7-bicuadrada-desplazada-{s}.png'},
        ]})
        t.append({'url': U, 'ancho': a, 'modulo': 8, 'pasos': [
            {'sel': '#content-area table', 'archivo': f'B1-tabla-fuerzas-{s}.png'},
            {'js': "(() => { const t = document.querySelector('#content-area table'); let c = t; while (c && !/auto|scroll/.test(getComputedStyle(c).overflowX)) c = c.parentElement; if (c) c.scrollLeft = c.scrollWidth; return c ? [c.scrollLeft, c.scrollWidth, c.clientWidth] : null; })()"},
            {'sel': '#content-area table', 'archivo': f'B1-tabla-fuerzas-desplazada-{s}.png'},
            abre('der-fuerza-ft'), {'sel': '#der-fuerza-ft', 'archivo': f'B7-m8-desarrollo-ft-{s}.png'},
            {'js': "(() => [...document.querySelectorAll('#der-fuerza-ft .katex-display')].map(d => { let c = d; while (c && !/auto|scroll/.test(getComputedStyle(c).overflowX)) c = c.parentElement; if (c) c.scrollLeft = c.scrollWidth; return c ? [c.scrollLeft, c.scrollWidth, c.clientWidth] : null; }))()"},
            {'sel': '#der-fuerza-ft', 'archivo': f'B7-m8-desarrollo-ft-desplazado-{s}.png'},
        ]})
    return t

def pasada(anchos):
    return [{'url': U, 'ancho': a, 'modulo': m, 'pasos': [{'js': PASADA}]} for a in anchos for m in range(1, 10)]

if __name__ == '__main__':
    que = sys.argv[1]
    anchos = [int(x) for x in sys.argv[2:]] or [1200, 800, 375]
    json.dump({'medidas': medidas, 'capturas': capturas, 'pasada': pasada}[que](anchos), sys.stdout, ensure_ascii=False, indent=1)
