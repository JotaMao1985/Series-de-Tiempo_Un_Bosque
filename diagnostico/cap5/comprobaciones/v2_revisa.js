#!/usr/bin/env node
// VERIFICADOR INDEPENDIENTE R2 cap. 5: copia adaptada de diagnostico/cap5/diag/graficas_revisa.js (que venía del cap. 4): capturas por elemento, estados extremos
// de los simuladores y medidas, a 1200, 800 y 375 px. Chrome sin ventana por CDP.
// Uso: node diagnostico/cap5/diag/graficas_revisa.js   (BASE=http://127.0.0.1:<puerto>/capitulo-5-sarima.html)
// Añadidos respecto del cap. 4: medidas del componente .mapa-estacional (desplazamiento, contraste de cada
// celda, guiones), de la tabla de la receta y de los lienzos del quiz del M11.
const fs = require('fs');
const path = require('path');
const { Chrome, espera } = require('../diag/chrome');

const DIAG = __dirname;
const OUT = path.resolve(DIAG, '..', 'capturas', 'v2');
const BASE = process.env.BASE || 'http://127.0.0.1:8769/capitulo-5-sarima.html';
const PUERTO = 9281;

// ---------------------------------------------------------------- en página
// Medidas de un lienzo con Chart.js: escalas, rótulos solapados, leyenda, área.
const AYUDANTES = `
window.__r1 = x => Math.round(x * 10) / 10;
window.__medirGrafico = function (cv) {
  const r1 = window.__r1;
  const ch = Chart.getChart(cv);
  const r = cv.getBoundingClientRect();
  const info = { aria: cv.getAttribute('aria-label'), role: cv.getAttribute('role'), w: r1(r.width), h: r1(r.height), right: r1(r.right) };
  if (!ch) return info;
  info.tipo = ch.config.type;
  info.datasets = ch.data.datasets.map((d, k) => ({ label: d.label, type: d.type || ch.config.type, color: d.borderColor, bg: d.backgroundColor,
    bw: d.borderWidth, dash: d.borderDash || null, visible: ch.isDatasetVisible(k), n: (d.data || []).length,
    primero: (d.data || [])[0], pr: d.pointRadius,
    datos: (d.data || []).length <= 30 ? (d.data || []).map(v => typeof v === 'number' ? Math.round(v * 1e4) / 1e4 : v) : null,
    rango: (() => { const v = (d.data || []).map(x => x && typeof x === 'object' ? x.y : x).filter(x => x !== null && x !== undefined);
      if (!v.length) return null; if (v.some(x => typeof x !== 'number' || !Number.isFinite(x))) return [null, null]; return [Math.min(...v), Math.max(...v)]; })(),
    nulos: (d.data || []).filter(x => x === null).length }));
  // Puntos de dispersión: ¿dentro del área de dibujo?
  info.version = Chart.version;
  {
    const rr = v => Array.isArray(v) ? Math.max(0, ...v) : (v || 0);
    info.puntos = ch.data.datasets.map((d, k) => ({ k, d })).filter(o => ch.isDatasetVisible(o.k) && (o.d.showLine === false || rr(o.d.pointRadius) >= 4)).map(o => {
      const meta = ch.getDatasetMeta(o.k);
      return { label: o.d.label, datos: o.d.data, px: meta.data.map(p => [r1(p.x), r1(p.y)]),
        dentro: meta.data.map(p => p.x >= ch.chartArea.left - 0.5 && p.x <= ch.chartArea.right + 0.5 && p.y >= ch.chartArea.top - 0.5 && p.y <= ch.chartArea.bottom + 0.5),
        recorte: meta.data.map((p, j) => { const rad = (Array.isArray(o.d.pointRadius) ? o.d.pointRadius[j] : (o.d.pointRadius ?? 3)) || 0;
          if (!rad || p.skip || p.y == null || Number.isNaN(p.y)) return null;
          return Math.min(p.x - ch.chartArea.left, ch.chartArea.right - p.x, p.y - ch.chartArea.top, ch.chartArea.bottom - p.y) < rad; }) };
    }).map(p => Object.assign(p, { datos: null, px: p.px.filter((_, j) => p.recorte[j] !== null), dentro: p.dentro.filter((_, j) => p.recorte[j] !== null), recorte: p.recorte.filter(x => x !== null) }));
  }
  const lg = ch.legend;
  info.legend = { display: ch.options.plugins.legend.display !== false,
    items: lg && lg.legendItems ? lg.legendItems.map(x => x.text) : [], h: lg ? r1(lg.height) : 0,
    lineas: lg && lg.lineWidths ? lg.lineWidths.length : 0,
    cajas: lg && lg.legendHitBoxes ? lg.legendHitBoxes.length : 0,
    cortadas: lg && lg.legendHitBoxes ? lg.legendHitBoxes.map((b, j) => ({ t: lg.legendItems[j] && lg.legendItems[j].text, fuera: b.top + b.height > lg.top + lg.height + 0.5 || b.left + b.width > lg.left + lg.width + 0.5 })).filter(o => o.fuera).map(o => o.t) : [],
    fuente: ch.options.plugins.legend.labels.font ? ch.options.plugins.legend.labels.font.size : null };
  info.area = { w: r1(ch.chartArea.width), h: r1(ch.chartArea.height), left: r1(ch.chartArea.left), right: r1(ch.chartArea.right) };
  const ctx = ch.ctx;
  info.escalas = Object.values(ch.scales).map(s => {
    const e = { id: s.id, type: s.type, title: s.options.title?.display ? s.options.title.text : null,
      min: s.min, max: s.max, nTicks: s.ticks.length,
      ticks: s.ticks.map(t => t.label).filter(x => x !== '' && x != null).map(String).slice(0, 40),
      valoresTicks: s.ticks.map(t => t.value).slice(0, 40),
      w: r1(s.width), h: r1(s.height),
      guion: s.ticks.map(t => String(t.label)).filter(x => /^-\d|^-\./.test(x)),
      rejillaCero: typeof s.options.grid.color === 'function',
      maxTicksLimit: s.options.ticks.maxTicksLimit ?? null, autoSkip: s.options.ticks.autoSkip };
    // Solapes de rótulos en el eje horizontal
    if (s.isHorizontal()) {
      const items = s.getLabelItems ? s.getLabelItems(ch.chartArea) : [];
      const cajas = items.map(it => {
        ctx.save(); ctx.font = it.font.string;
        const lab = Array.isArray(it.label) ? it.label.join(' ') : String(it.label);
        const w = ctx.measureText(lab).width; ctx.restore();
        const x = it.options.translation[0];
        const al = it.options.textAlign;
        const left = al === 'left' ? x : al === 'right' ? x - w : x - w / 2;
        return { lab, left: r1(left), right: r1(left + w), font: it.font.string };
      }).sort((a, b) => a.left - b.left);
      let minGap = Infinity; const solapes = [];
      for (let i = 1; i < cajas.length; i++) {
        const g = cajas[i].left - cajas[i - 1].right;
        minGap = Math.min(minGap, g);
        if (g < 3) solapes.push(cajas[i - 1].lab + '|' + cajas[i].lab + ' (' + r1(g) + ' px)');
      }
      e.minGap = cajas.length > 1 ? r1(minGap) : null;
      e.solapes = solapes;
      e.fuenteTicks = cajas[0]?.font || null;
      e.fuenteCargada = cajas[0] ? document.fonts.check(cajas[0].font) : null;
      e.fuera = cajas.filter(c => c.left < 0 || c.right > r.width + 1).map(c => c.lab);
    } else {
      const items = s.getLabelItems ? s.getLabelItems(ch.chartArea) : [];
      e.fuenteTicks = items[0]?.font?.string || null;
      e.fuenteCargada = items[0] ? document.fonts.check(items[0].font.string) : null;
    }
    return e;
  });
  // Bandas del correlograma: rectas de referencia (datasets de línea dentro de un gráfico de barras)
  if (ch.config.type === 'bar') {
    info.rectas = ch.data.datasets.map((d, k) => ({ k, d })).filter(o => (o.d.type || 'bar') === 'line').map(o => {
      const meta = ch.getDatasetMeta(o.k);
      const xs = meta.data.map(p => p.x);
      return { label: o.d.label, valor: o.d.data[0], color: o.d.borderColor,
        x0: r1(Math.min(...xs)), x1: r1(Math.max(...xs)), y: r1(meta.data[0]?.y) };
    });
    info.barras = ch.data.datasets.filter(d => (d.type || 'bar') === 'bar').map(d => ({ label: d.label, color: d.backgroundColor,
      max: Math.max(...d.data.map(Math.abs)), n: d.data.length }));
    // ancho de una barra en píxeles
    const m0 = ch.getDatasetMeta(0);
    info.anchoBarra = m0.data[0] ? r1(m0.data[0].width) : null;
  }
  return info;
};
window.__lum = c => { const m = /rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)/.exec(c); if (!m) return null;
  const [r, g, b] = [1, 2, 3].map(i => Number(m[i]) / 255).map(v => v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4));
  return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
window.__contraste = (a, b) => { const x = window.__lum(a), y = window.__lum(b); if (x == null || y == null) return null;
  return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
window.__medirMapa = function (raiz) {
  const r1 = window.__r1;
  const marco = raiz.querySelector('.mapa-estacional-marco');
  const rej = raiz.querySelector('.mapa-estacional-rejilla');
  const celdas = [...raiz.querySelectorAll('.mapa-estacional-celda')];
  const mr = marco.getBoundingClientRect();
  const cab = [...raiz.querySelectorAll('.mapa-estacional-cabecera[role=columnheader]')];
  const visibles = cab.filter(c => { const r = c.getBoundingClientRect(); return r.right <= mr.right + 0.5; }).map(c => c.textContent);
  const cont = celdas.filter(c => c.textContent && c.textContent !== '·').map(c => {
    const cs = getComputedStyle(c); return { t: c.textContent, k: window.__contraste(cs.color, cs.backgroundColor), bg: cs.backgroundColor, fg: cs.color }; });
  const ks = cont.map(x => x.k).filter(x => x != null);
  const peores = cont.slice().sort((a, b) => a.k - b.k).slice(0, 3);
  const c0 = celdas[0] ? celdas[0].getBoundingClientRect() : null;
  // ¿Cabe el número en la celda?
  const desbordaCelda = celdas.filter(c => c.scrollWidth > c.clientWidth + 0.5).length;
  return { marcoW: r1(mr.width), sw: marco.scrollWidth, cw: marco.clientWidth, desplaza: marco.scrollWidth > marco.clientWidth + 1,
    mesesVisibles: visibles, filas: raiz.querySelectorAll('.mapa-estacional-anio').length, celdas: celdas.length,
    conNumero: cont.length, vacias: raiz.querySelectorAll('.mapa-estacional-vacia').length,
    celda: c0 ? { w: r1(c0.width), h: r1(c0.height) } : null, desbordaCelda,
    contrasteMin: ks.length ? Math.round(Math.min(...ks) * 100) / 100 : null,
    bajo45: ks.filter(k => k < 4.5).length, bajo3: ks.filter(k => k < 3).length, peores,
    guiones: cont.filter(x => /^-/.test(x.t)).length,
    leyenda: raiz.querySelector('.mapa-estacional-leyenda')?.textContent.replace(/\\s+/g, ' ').trim(),
    nota: raiz.querySelector('.mapa-estacional-nota')?.textContent.replace(/\\s+/g, ' ').trim(),
    aria: rej.getAttribute('aria-label'), primeras: celdas.slice(0, 14).map(c => c.getAttribute('aria-label')) };
};
true;
`;

const MEDIDAS = ancho => `(() => {
  const W = ${ancho};
  const mc = mainContent;
  const r1 = window.__r1;
  const canv = [...mc.querySelectorAll('canvas')].map((cv, i) => Object.assign({ i,
    sim: cv.closest('[data-simulador]')?.dataset.simulador || (cv.closest('.quiz') ? 'quiz' : null) }, window.__medirGrafico(cv)));
  const katex = [...mc.querySelectorAll('.katex-display')].map((d, i) => {
    const k = d.querySelector('.katex');
    const cont = d.closest('.formula, .definition, .note, .warning, .simulador') || d.parentElement;
    const r = d.getBoundingClientRect();
    return { i, sw: k ? k.scrollWidth : 0, cw: d.clientWidth, contCw: cont.clientWidth, ox: getComputedStyle(d).overflowX,
      right: r1(r.right), dentro: cont.className.split(' ')[0],
      txt: d.textContent.replace(/\\s+/g, ' ').slice(0, 70) };
  }).filter(x => x.sw > x.cw + 1);
  const katexLinea = [...mc.querySelectorAll('.katex')].filter(k => !k.closest('.katex-display')).map(k => {
    const r = k.getBoundingClientRect();
    const host = k.closest('p, li, td, th, h4, .simulador-intro, label, span') || k.parentElement;
    const hr = host.getBoundingClientRect();
    return { right: r1(r.right), w: r1(r.width), hostRight: r1(hr.right), txt: k.textContent.slice(0, 50) };
  }).filter(x => x.w && x.right > x.hostRight + 1);
  const tablas = [...mc.querySelectorAll('table')].map((t, i) => ({ i, sw: t.scrollWidth, cw: t.clientWidth,
    parentCw: t.parentElement.clientWidth, caption: (t.caption?.textContent || '').trim().slice(0, 60) })).filter(t => t.sw > t.cw + 1 || t.sw > t.parentCw + 1);
  const desbordan = [];
  mc.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width && r.right > W + 1) {
      let p = el.parentElement, externo = true;
      while (p && p !== mc) { if (p.getBoundingClientRect().right > W + 1) { externo = false; break; } p = p.parentElement; }
      if (externo) desbordan.push({ tag: el.tagName, cls: String(el.className).slice(0, 50), right: r1(r.right),
        txt: (el.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 50) });
    }
  });
  // Lo que asoma por la derecha de <main> (overflow:hidden) sin un contenedor desplazable que lo recoja
  const main = document.getElementById('main-content');
  const mR = main.getBoundingClientRect().right;
  const recortados = [];
  mc.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect();
    if (!r.width || r.right <= mR + 1) return;
    let p = el.parentElement, recogido = false, externo = true;
    while (p && p !== main) {
      const ox = getComputedStyle(p).overflowX;
      const pr = p.getBoundingClientRect().right;
      if (pr > mR + 1) { externo = false; break; }
      if (ox === 'auto' || ox === 'scroll' || ox === 'hidden') { recogido = true; break; }
      p = p.parentElement;
    }
    if (externo && !recogido) recortados.push({ tag: el.tagName, cls: String(el.className).slice(0, 40), sobra: r1(r.right - mR),
      txt: (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 50) });
  });
  const sims = [...mc.querySelectorAll('[data-simulador]')].map(s => {
    const h4 = s.querySelector('h4');
    const hijos = h4 ? [...h4.childNodes].filter(n => n.nodeType === 1 || n.textContent.trim()).length : 0;
    const lect = s.querySelector('.simulador-lectura');
    const r = s.getBoundingClientRect();
    return { sim: s.dataset.simulador, w: r1(r.width), right: r1(r.right), sw: s.scrollWidth, cw: s.clientWidth,
      h4: h4 ? { txt: h4.textContent.trim(), h: r1(h4.getBoundingClientRect().height), hijos } : null,
      lectura: lect ? { ariaLive: lect.getAttribute('aria-live'), role: lect.getAttribute('role'),
        txt: lect.textContent.replace(/\\s+/g, ' ').trim(), h: r1(lect.getBoundingClientRect().height) } : null,
      controles: [...s.querySelectorAll('input, select')].map(inp => ({ tipo: inp.type || inp.tagName, id: inp.id,
        label: inp.id ? (document.querySelector('label[for="' + inp.id + '"]')?.textContent || null) : (inp.closest('label')?.textContent || null),
        min: inp.min, max: inp.max, step: inp.step, value: inp.value, w: r1(inp.getBoundingClientRect().width) })),
      etiquetas: [...s.querySelectorAll('.grafico-etiqueta')].map(e => e.textContent.replace(/\\s+/g, ' ').trim()),
      alturas: [...s.querySelectorAll('.grafico-wrapper')].map(g => r1(g.getBoundingClientRect().height)) };
  });
  return { modulo: currentModuleId, ancho: W, innerWidth: window.innerWidth,
    docSw: document.documentElement.scrollWidth, mainW: Math.round(mc.getBoundingClientRect().width),
    mainCw: mc.clientWidth, mainRight: r1(mR), recortados, canv, katex, katexLinea, tablas, desbordan, sims };
})()`;

// Estados por simulador: [nombre, [acciones]] con acción = ['range', índice, valor] | ['select', índice, valor] | ['check', índice, bool]
// Acción: ['range', índice, valor] | ['select', índice, valor] | ['check', índice, bool] | ['click', texto del botón]
const R = (...pares) => pares.map(([i, v]) => ['range', i, v]);
// Tercer elemento opcional {captura:false}: solo se mide (barridos completos).
const PQD = [];
for (let pp = 0; pp <= 2; pp++) for (let dd = 0; dd <= 2; dd++) for (let qq = 0; qq <= 2; qq++) PQD.push([pp, dd, qq]);
const CAPTURA_PQD = ['000', '111', '011', '101', '020', '122', '222', '202', '212', '021'];
const SERIES = ['airpassengers', 'usaccdeaths', 'co2', 'trm'];
const DIFS = ['ninguna', 'd1', 'D1', 'd1D1'];
const CAPTURA_MAPA = ['airpassengers-log-ninguna', 'airpassengers-log-d1D1', 'airpassengers-log-d1', 'airpassengers-log-D1',
  'airpassengers-nolog-ninguna', 'trm-nolog-d1', 'trm-log-ninguna', 'co2-nolog-ninguna', 'co2-log-d1D1', 'usaccdeaths-nolog-D1',
  'usaccdeaths-nolog-ninguna'];
const MAPA = [];
for (const se of SERIES) for (const lg of [true, false]) for (const df of DIFS) {
  const nombre = `${se}-${lg ? 'log' : 'nolog'}-${df}`;
  MAPA.push([nombre, [['select', 0, se], ['select', 1, df], ['check', 0, lg]], { captura: CAPTURA_MAPA.includes(nombre) }]);
}
const EXPL = [];
const CAPTURA_EXPL = ['0011', '0000', '2211', '1010', '2101', '0001', '0010', '2200'];
for (const p of ['0', '1', '2']) for (const q of ['0', '1', '2']) for (const P of ['0', '1']) for (const Q of ['0', '1']) {
  EXPL.push([`pqPQ${p}${q}${P}${Q}`, [['select', 0, p], ['select', 1, q], ['select', 2, P], ['select', 3, Q]],
    { captura: CAPTURA_EXPL.includes(`${p}${q}${P}${Q}`) }]);
}
const CAPT = new Set(['mapa-firma:airpassengers-log-d1D1', 'mapa-firma:trm-nolog-D1', 'mapa-firma:trm-nolog-d1',
  'receta-mes:phi1-Phi1', 'receta-mes:phi-1-Phi-1', 'constructor-polinomio:todo0', 'constructor-polinomio:todo2',
  'tienda-cuadricula:fijo-d1', 'cuatro-combinaciones:d1D1', 'sobrediferenciacion-estacional:D2', 'firma-teorica:phi05-Phi07',
  'airline-pesos:theta-095-Theta-095', 'airline-pesos:Theta0', 'explorador-sarima:pqPQ0000', 'pronostico-estacional:log-h13',
  'contraejemplo-trm:trm', 'calendario-regresores:dias0-pascua1', 'calendario-regresores:dias1-pascua1', 'armonicos-K:K1',
  'comparativa-particion:todos', 'comparativa-particion:mape', 'comparativa-particion:todos-mape']);
const ESTADOS = {
  'mapa-firma': MAPA,
  'receta-mes': [[0, 0], [0.6, 0], [0, 0.7], [1, 1], [-1, -1], [1, -1], [-0.5, 0.3], [-1, 1]].map(([a, b]) =>
    [`phi${a}-Phi${b}`, R([0, a], [1, b])]),
  'constructor-polinomio': [
    ['todo0', R([0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0])],
    ['D0', R([0, 1], [1, 1], [2, 1], [3, 1], [4, 0], [5, 1])],
    ['P2D2', R([0, 0], [1, 0], [2, 0], [3, 2], [4, 2], [5, 0])],
    ['todo2', R([0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [5, 2])],
    ['p2d2', R([0, 2], [1, 2], [2, 0], [3, 0], [4, 0], [5, 0])],
  ],
  'tienda-cuadricula': [].concat(...['fijo', 'acelera'].map(e => DIFS.map(d => [`${e}-${d}`, [['select', 0, e], ['select', 1, d]]]))),
  'cuatro-combinaciones': [[false, false], [true, false], [false, true], [true, true]].map(([a, b]) =>
    [`d${+a}D${+b}`, [['check', 0, a], ['check', 1, b]]]),
  'sobrediferenciacion-estacional': [0, 1, 2].map(D => [`D${D}`, R([0, D])]),
  'firma-teorica': [
    ['todo0', R([0, 0], [1, 0], [2, 0], [3, 0])],
    ['Phi085', R([0, 0], [1, 0], [2, 0.85], [3, 0])],
    ['Phim085', R([0, 0], [1, 0], [2, -0.85], [3, 0])],
    ['phi05-Phi07', R([0, 0.5], [1, 0], [2, 0.7], [3, 0])],
    ['phi085-Phi085', R([0, 0.85], [1, 0], [2, 0.85], [3, 0])],
    ['Theta-085', R([0, 0], [1, 0], [2, 0], [3, -0.85])],
    ['theta-085-Theta-085', R([0, 0], [1, -0.85], [2, 0], [3, -0.85])],
    ['todo085', R([0, 0.85], [1, 0.85], [2, 0.85], [3, 0.85])],
    ['todom085', R([0, -0.85], [1, -0.85], [2, -0.85], [3, -0.85])],
    ['phi085-solo', R([0, 0.85], [1, 0], [2, 0], [3, 0])],
  ],
  'airline-pesos': [
    ['Theta0', R([0, -0.4], [1, 0])],
    ['Theta-095', R([0, -0.4], [1, -0.95])],
    ['theta-095-Theta-095', R([0, -0.95], [1, -0.95])],
    ['theta05-Theta05', R([0, 0.5], [1, 0.5])],
    ['theta0-Theta0', R([0, 0], [1, 0])],
    ['theta-095-Theta05', R([0, -0.95], [1, 0.5])],
  ],
  'explorador-sarima': EXPL,
  'pronostico-estacional': [
    ['h1', R([0, 1])], ['h12', R([0, 12])], ['h13', R([0, 13])], ['h24', R([0, 24])],
    ['log-h24', [['check', 0, false]]], ['log-h12', R([0, 12])], ['log-h13', R([0, 13])], ['log-h1', R([0, 1])],
  ],
  'contraejemplo-trm': ['trm', 'ap'].map(v => [v, [['select', 0, v]]]),
  'calendario-regresores': [[false, false], [true, false], [false, true], [true, true]].map(([a, b]) =>
    [`dias${+a}-pascua${+b}`, [['check', 0, a], ['check', 1, b]]]),
  'armonicos-K': [1, 2, 3, 4, 5, 6].map(k => [`K${k}`, R([0, k])]),
  'comparativa-particion': [
    ['mae', [['select', 0, 'mae']]], ['mape', [['select', 0, 'mape']]],
    ['todos', [0, 1, 2, 3, 4, 5, 6, 7].map(i => ['check', i, true])],
    ['ninguno', [0, 1, 2, 3, 4, 5, 6, 7].map(i => ['check', i, false])],
    ['todos-mape', [0, 1, 2, 3, 4, 5, 6, 7].map(i => ['check', i, true]).concat([['select', 0, 'mape']])],
  ],
};

async function aplicar(c, sim, acciones) {
  for (const [tipo, idx, val] of acciones) {
    const ix = JSON.stringify(idx), v = JSON.stringify(val);
    const cuerpo = {
      range: `const i = raiz.querySelectorAll('input[type=range]')[${ix}]; i.value = ${v}; i.dispatchEvent(new Event('input', { bubbles: true }));`,
      select: `const s = raiz.querySelectorAll('select')[${ix}]; s.value = ${v}; s.dispatchEvent(new Event('change', { bubbles: true }));`,
      check: `const k = raiz.querySelectorAll('input[type=checkbox]')[${ix}]; if (k.checked !== ${v}) { k.checked = ${v}; k.dispatchEvent(new Event('change', { bubbles: true })); }`,
      click: `[...raiz.querySelectorAll('button')].find(x => x.textContent.trim() === ${ix}).click();`,
    }[tipo];
    await c.evalua(`(() => { const raiz = document.querySelector('[data-simulador="${sim}"]'); ${cuerpo} return 1; })()`);
    await espera(120);
  }
  await espera(250);
}

async function capturar(c, sel, archivo, { padre = null, indice = 0 } = {}) {
  const rect = await c.evalua(`(() => {
    let el = document.querySelectorAll(${JSON.stringify(sel)})[${indice}];
    if (!el) return null;
    ${padre ? `el = el.closest(${JSON.stringify(padre)}) || el;` : ''}
    el.scrollIntoView({ behavior: 'instant', block: 'start' });
    const r = el.getBoundingClientRect();
    return { x: r.left + window.scrollX, y: r.top + window.scrollY, w: r.width, h: r.height };
  })()`);
  if (!rect) return null;
  await espera(200);
  const pad = 6;
  const r = await c.enviar('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
    clip: { x: Math.max(0, rect.x - pad), y: Math.max(0, rect.y - pad), width: rect.w + 2 * pad, height: rect.h + 2 * pad, scale: 1 } });
  fs.writeFileSync(path.join(OUT, archivo), Buffer.from(r.data, 'base64'));
  return archivo;
}

async function vistaPantalla(c, archivo) {
  const v = await c.enviar('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(OUT, archivo), Buffer.from(v.data, 'base64'));
}

async function cargarModulo(c, n) {
  c.contexto = `M${n}`;
  await c.evalua(`loadModule(${n}), 'ok'`);
  await espera(1100);
  // scrollIntoView() puede desplazar en horizontal un ancestro con overflow:hidden (main) al capturar una tabla
  await c.evalua(`(() => { let e = mainContent; while (e) { e.scrollLeft = 0; e = e.parentElement; } return 1; })()`);
  await c.evalua(`window.scrollTo({top:0, behavior:'instant'}), 1`);
  await espera(200);
}

const QUITAR_FIJOS = `(() => { if (!document.getElementById('quitar-fijos')) { const st = document.createElement('style'); st.id = 'quitar-fijos';
  st.textContent = 'header.usta-header{position:static!important} #sidebarToggle,#scrollToTopBtn{visibility:hidden!important}'; document.head.appendChild(st); } return 1; })()`;
const PONER_FIJOS = `(() => { document.getElementById('quitar-fijos')?.remove(); return 1; })()`;

const LECTURA_SIM = sim => `(() => {
  const raiz = document.querySelector('[data-simulador="${sim}"]');
  const p = raiz.querySelector('.simulador-lectura');
  return { lectura: p ? p.textContent.replace(/\\s+/g, ' ').trim() : null,
    outputs: [...raiz.querySelectorAll('output')].map(o => o.textContent),
    graficos: [...raiz.querySelectorAll('canvas')].map(cv => window.__medirGrafico(cv)),
    mapas: [...raiz.querySelectorAll('.mapa-estacional')].map(m => window.__medirMapa(m)),
    receta: raiz.querySelector('.receta-cuadrado') ? { txt: raiz.querySelector('.receta-cuadrado').textContent.replace(/\\s+/g, ' ').trim(),
      sw: raiz.querySelector('.receta-cuadrado').scrollWidth, cw: raiz.querySelector('.receta-cuadrado').clientWidth } : null };
})()`;

// ---------------------------------------------------------------- principal
async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const c = await Chrome.lanzar(PUERTO);
  const salida = { base: BASE, fecha: new Date().toISOString(), medidas: {}, estados: {}, eventos: null };
  try {
    await c.enviar('Page.enable');
    await c.enviar('Runtime.enable');
    await c.enviar('Log.enable');
    await c.enviar('Network.enable');

    // 1) Fuentes del módulo de arranque
    // (la prueba de fuentes del módulo de arranque vive en fuentes.js)

    // 2) Recorrido por anchos
    const modos = [
      { nombre: '1200', width: 1200, height: 1000, dsf: 1, mobile: false },
      { nombre: '800', width: 800, height: 1000, dsf: 1, mobile: false },
      { nombre: '375', width: 375, height: 812, dsf: 2, mobile: true },
    ];
    for (const modo of modos) {
      c.contexto = `carga ${modo.nombre}`;
      await c.enviar('Emulation.setDeviceMetricsOverride', { width: modo.width, height: modo.height,
        deviceScaleFactor: modo.dsf, mobile: modo.mobile });
      await c.enviar('Page.navigate', { url: BASE + '#modulo-1' });
      await espera(600);
      await c.esperaHasta("typeof courseData !== 'undefined' && typeof Chart !== 'undefined' && typeof renderMathInElement === 'function'", 30000);
      await c.evalua('document.fonts.ready.then(() => 1)');
      await c.evalua(`(() => { Chart.defaults.animation = false; Chart.defaults.animations = {}; return 1; })()`);
      await c.evalua(AYUDANTES);
      await espera(400);
      salida.medidas[modo.nombre] = {};
      salida.estados[modo.nombre] = {};
      for (let n = 1; n <= 12; n++) {
        await c.evalua(PONER_FIJOS);
        await cargarModulo(c, n);
        const med = await c.evalua(MEDIDAS(modo.width));
        salida.medidas[modo.nombre][n] = med;
        // Vista real (cabecera fija incluida) sobre el primer simulador, en teléfono y a 800
        if (modo.width < 1200) {
          const conLienzo = await c.evalua(`[...document.querySelectorAll('[data-simulador], .quiz-grafico')].filter(e => e.querySelector('canvas') || e.tagName === 'CANVAS' || e.classList.contains('quiz-grafico')).length`);
          for (let k = 0; k < conLienzo; k++) {
            await c.evalua(`(() => { const e = [...document.querySelectorAll('[data-simulador], .quiz-grafico')].filter(e => e.querySelector('canvas'))[${k}]; (e.querySelector('.simulador-controles') || e).scrollIntoView({behavior:'instant', block:'start'}); window.scrollBy(0, -70); return 1; })()`);
            await espera(300);
            if (n === 1 || n === 11) await vistaPantalla(c, `m${n}-vista${k + 1}-${modo.nombre}.png`);
          }
        }
        await c.evalua(QUITAR_FIJOS);
        await espera(150);
        for (const s of med.sims) {
          const sim = s.sim;
          await capturar(c, `[data-simulador="${sim}"]`, `m${n}-${sim}-${modo.nombre}.png`);
          salida.estados[modo.nombre][`${sim}:inicial`] = await c.evalua(LECTURA_SIM(sim));
          for (const [estado, acciones, op] of (ESTADOS[sim] || [])) {
            await aplicar(c, sim, acciones);
            if (CAPT.has(sim + ':' + estado)) await capturar(c, `[data-simulador="${sim}"]`, `m${n}-${sim}-${estado}-${modo.nombre}.png`);
            salida.estados[modo.nombre][`${sim}:${estado}`] = await c.evalua(LECTURA_SIM(sim));
          }
          if (ESTADOS[sim]) { await cargarModulo(c, n); await c.evalua(QUITAR_FIJOS); }
        }
        // Gráficos del quiz
        const nq = await c.evalua(`document.querySelectorAll('.quiz-grafico').length`);
        for (let q = 0; q < nq; q++) {
          await capturar(c, '.quiz-grafico', `m${n}-quiz-grafico${q + 1}-${modo.nombre}.png`, { indice: q, padre: '.quiz-pregunta' });
        }
        // Fórmulas en display que desbordan (las cinco primeras)
        for (const k of []) {
          await capturar(c, '.katex-display', `m${n}-formula${k.i}-${modo.nombre}.png`, { indice: k.i, padre: '.definition, .note, .warning, .formula' });
        }
        // Tablas que desbordan
        for (const t of []) {
          await capturar(c, 'table', `m${n}-tabla${t.i}-${modo.nombre}.png`, { indice: t.i });
        }
        console.log(`  ${modo.nombre} M${n}: ${med.sims.length} sim, ${med.canv.length} lienzos, ${med.katex.length} fórmulas que desbordan, docSw ${med.docSw}`);
      }
    }
    salida.eventos = c.eventos;
  } finally {
    await c.cerrar();
  }
  fs.writeFileSync(path.join(DIAG, 'v2_medidas.json'), JSON.stringify(salida, null, 1));
  console.log('listo; eventos de consola:', salida.eventos ? salida.eventos.length : 'n/d');
}
main().then(() => process.exit(0)).catch(e => { console.error('✗ ' + e.stack); process.exit(1); });
